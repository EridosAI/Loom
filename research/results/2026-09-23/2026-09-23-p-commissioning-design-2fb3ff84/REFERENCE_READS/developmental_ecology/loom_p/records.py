"""Lossless strict records and versioned all-state snapshots. No pickle execution."""
import base64
import gzip
import hashlib
import json
import os
from pathlib import Path
import platform
import sys
import time
import numpy as np

def registry():
    from .schema import Config,Streams
    from .neural import Cortex,Association,Regulator,Motor,Organism
    from .physics import Body
    from .chemistry import FieldSolver
    from .engine import Engine
    return {cls.__name__:cls for cls in (Config,Streams,Cortex,Association,Regulator,Motor,Organism,Body,FieldSolver,Engine)}

def pack(value):
    if isinstance(value,np.ndarray):
        if value.dtype.kind not in 'fiu' or (value.dtype.kind=='f' and not np.isfinite(value).all()): raise ValueError('Invalid snapshot array')
        return {'$array':base64.b64encode(np.ascontiguousarray(value).tobytes()).decode('ascii'),'dtype':value.dtype.str,'shape':list(value.shape)}
    if isinstance(value,np.generic): return pack(value.item())
    if isinstance(value,slice): return {'$slice':[value.start,value.stop,value.step]}
    if isinstance(value,tuple): return {'$tuple':[pack(v) for v in value]}
    if isinstance(value,list): return [pack(v) for v in value]
    if isinstance(value,dict): return {'$dict':[[pack(k),pack(v)] for k,v in value.items()]}
    if value is None or isinstance(value,(str,int,bool,float)):
        if isinstance(value,float) and not np.isfinite(value): raise ValueError('Nonfinite scalar')
        return value
    if value.__class__.__name__ in registry(): return {'$class':value.__class__.__name__,'attrs':pack(vars(value))}
    raise ValueError(f'Unsupported snapshot object {type(value)}')

def unpack(value):
    if isinstance(value,list): return [unpack(x) for x in value]
    if not isinstance(value,dict): return value
    if '$array' in value:
        dtype=np.dtype(value['dtype']); shape=tuple(value['shape'])
        if dtype.kind not in 'fiu' or any(not isinstance(x,int) or x<0 for x in shape): raise ValueError('Unsafe array schema')
        raw=base64.b64decode(value['$array'],validate=True)
        if len(raw)!=int(np.prod(shape))*dtype.itemsize: raise ValueError('Array byte count mismatch')
        result=np.frombuffer(raw,dtype=dtype).reshape(shape).copy()
        if dtype.kind=='f' and not np.isfinite(result).all(): raise ValueError('Nonfinite snapshot')
        return result
    if '$slice' in value: return slice(*value['$slice'])
    if '$tuple' in value: return tuple(unpack(x) for x in value['$tuple'])
    if '$dict' in value: return {unpack(k):unpack(v) for k,v in value['$dict']}
    if '$class' in value:
        cls=registry().get(value['$class'])
        if cls is None: raise ValueError('Unknown state class')
        obj=cls.__new__(cls); obj.__dict__.update(unpack(value['attrs'])); return obj
    raise ValueError('Malformed snapshot tags')

def strict_bytes(value): return json.dumps(value,allow_nan=False,separators=(',',':'),ensure_ascii=False).encode('utf-8')
def state_bytes(engine): return strict_bytes(pack(engine))
def state_hash(engine): return hashlib.sha256(state_bytes(engine)).hexdigest()

def code_identity():
    root=Path(__file__).parent
    entries={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.glob('*.py'))}
    return {'sha256':hashlib.sha256(strict_bytes(entries)).hexdigest(),'files':entries}

def save_snapshot(path,engine):
    path=Path(path); payload=state_bytes(engine)
    wrapper={'schema_version':1,'code':code_identity(),'configuration':engine.c.identity(),'state_sha256':hashlib.sha256(payload).hexdigest(),'state':json.loads(payload)}
    data=gzip.compress(strict_bytes(wrapper),mtime=0)
    temp=path.with_name(path.name+'.partial')
    with temp.open('xb') as handle: handle.write(data); handle.flush(); os.fsync(handle.fileno())
    os.replace(temp,path)
    return {'path':str(path),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'state_sha256':wrapper['state_sha256']}

def load_snapshot(path,allow_code_mismatch=False):
    raw=gzip.decompress(Path(path).read_bytes())
    wrapper=json.loads(raw,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('Nonfinite JSON token')))
    if wrapper.get('schema_version')!=1: raise ValueError('Unknown snapshot version')
    if not allow_code_mismatch and wrapper['code']['sha256']!=code_identity()['sha256']: raise ValueError('Snapshot code identity mismatch')
    payload=strict_bytes(wrapper['state'])
    if hashlib.sha256(payload).hexdigest()!=wrapper['state_sha256']: raise ValueError('Snapshot checksum mismatch')
    engine=unpack(wrapper['state'])
    if engine.__class__.__name__!='Engine' or engine.c.identity()!=wrapper['configuration']: raise ValueError('Snapshot configuration mismatch')
    engine.validate_state()
    return engine

def view(value):
    """JSON observation representation; copies arrays, never mutates state."""
    if isinstance(value,np.ndarray): return value.tolist()
    if isinstance(value,np.generic): return value.item()
    if isinstance(value,dict): return {str(k):view(v) for k,v in value.items()}
    if isinstance(value,(list,tuple)): return [view(v) for v in value]
    return value

def scalar_count(value):
    if isinstance(value,np.ndarray): return int(value.size)
    if isinstance(value,dict): return sum(scalar_count(v) for v in value.values())
    if isinstance(value,(list,tuple)): return sum(scalar_count(v) for v in value)
    return int(isinstance(value,(float,int,np.generic)))

class Recorder:
    def __init__(self,directory,manifest,storage_limit=None):
        self.path=Path(directory); self.path.mkdir(parents=True,exist_ok=False)
        self.started=time.perf_counter(); self.counts={}; self.widths={}; self.bytes_uncompressed=0; self.storage_limit=storage_limit
        self.streams={name:gzip.open(self.path/(name+'.jsonl.gz'),'wb') for name in ('native','wave','events')}
        self.manifest=dict(manifest,schema_version=1,complete=False,status='open',runtime={'python':sys.version,'executable':sys.executable,'platform':platform.platform(),'numpy':np.__version__},code=code_identity())
        self._manifest()
    def _manifest(self): (self.path/'manifest.json').write_bytes(strict_bytes(view(self.manifest)))
    def append(self,kind,record):
        data=strict_bytes(view(record))+b'\n'
        if self.storage_limit is not None and self.bytes_uncompressed+len(data)>self.storage_limit: raise OSError('Injected storage limit reached')
        self.streams[kind].write(data); self.streams[kind].flush()
        self.bytes_uncompressed+=len(data); self.counts[kind]=self.counts.get(kind,0)+1
        width=scalar_count(record); self.widths.setdefault(kind,{'min':width,'max':width})
        self.widths[kind]['min']=min(width,self.widths[kind]['min']); self.widths[kind]['max']=max(width,self.widths[kind]['max'])
    def close(self,status,complete,error=None):
        for stream in self.streams.values(): stream.close()
        elapsed=time.perf_counter()-self.started
        files={p.name:{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in self.path.iterdir() if p.name!='manifest.json' and p.is_file()}
        self.manifest.update(status=status,complete=complete,error=error,records=self.counts,scalar_widths=self.widths,uncompressed_bytes=self.bytes_uncompressed,wall_seconds=elapsed,uncompressed_bytes_per_wall_second=self.bytes_uncompressed/max(elapsed,1e-12),files=files)
        self._manifest()
