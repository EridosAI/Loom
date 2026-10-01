"""Lossless typed binary trees, bounded decoding; no pickle or executable payloads."""
import hashlib
import os
from pathlib import Path
import struct
import zlib
import numpy as np
from loom_p.records import registry

MAGIC=b'LOOMDEV1'
LIMIT=512_000_000
U=struct.Struct('<Q')
F=struct.Struct('<d')

def encode(value):
    parts=[]
    def put(x):
        if isinstance(x,np.ndarray):
            if x.dtype.kind not in 'fiu':raise ValueError('unsupported array dtype')
            parts.append(b'a');put(x.dtype.str);put(tuple(x.shape))
            raw=np.ascontiguousarray(x).tobytes();parts.extend((U.pack(len(raw)),raw))
        elif isinstance(x,np.generic):put(x.item())
        elif x is None:parts.append(b'n')
        elif x is True:parts.append(b't')
        elif x is False:parts.append(b'f')
        elif isinstance(x,int):
            raw=str(x).encode('ascii');parts.extend((b'i',U.pack(len(raw)),raw))
        elif isinstance(x,float):parts.extend((b'r',F.pack(x)))
        elif isinstance(x,str):
            raw=x.encode('utf8');parts.extend((b's',U.pack(len(raw)),raw))
        elif isinstance(x,(bytes,bytearray)):
            parts.extend((b'b',U.pack(len(x)),bytes(x)))
        elif isinstance(x,slice):parts.append(b'/');put((x.start,x.stop,x.step))
        elif isinstance(x,(list,tuple)):
            parts.extend((b'l' if isinstance(x,list) else b'u',U.pack(len(x))))
            for item in x:put(item)
        elif isinstance(x,dict):
            parts.extend((b'd',U.pack(len(x))))
            for k,v in x.items():put(k);put(v)
        elif type(x).__name__ in registry() and type(x) is registry()[type(x).__name__]:
            parts.append(b'o');put(type(x).__name__);put(vars(x))
        else:raise ValueError(f'unsupported binary type {type(x)}')
    put(value)
    return b''.join(parts)

def decode(raw):
    if len(raw)>LIMIT:raise ValueError('oversize binary object')
    data=memoryview(raw);offset=0
    def take(n):
        nonlocal offset
        if n<0 or offset+n>len(data):raise ValueError('truncated binary object')
        result=data[offset:offset+n];offset+=n;return result
    def count():return U.unpack(take(8))[0]
    def get(depth=0):
        if depth>100:raise ValueError('binary nesting limit')
        tag=bytes(take(1))
        if tag==b'n':return None
        if tag==b't':return True
        if tag==b'f':return False
        if tag==b'r':return F.unpack(take(8))[0]
        if tag in (b's',b'i',b'b'):
            value=bytes(take(count()))
            if tag==b'b':return value
            if tag==b'i':return int(value)
            return value.decode('utf8')
        if tag in (b'l',b'u',b'd'):
            n=count()
            if n>len(raw):raise ValueError('invalid binary count')
            if tag==b'd':
                result={}
                for _ in range(n):
                    k=get(depth+1);v=get(depth+1)
                    if k in result:raise ValueError('duplicate binary key')
                    result[k]=v
                return result
            result=[get(depth+1) for _ in range(n)]
            return tuple(result) if tag==b'u' else result
        if tag==b'/':return slice(*get(depth+1))
        if tag==b'a':
            dtype=np.dtype(get(depth+1));shape=get(depth+1);n=count()
            if dtype.kind not in 'fiu' or not isinstance(shape,tuple) or any(type(i)!=int or i<0 for i in shape):raise ValueError('unsafe array')
            expected=dtype.itemsize
            for i in shape:expected*=i
            if n!=expected:raise ValueError('array size mismatch')
            return np.frombuffer(take(n),dtype=dtype).reshape(shape).copy()
        if tag==b'o':
            name=get(depth+1);attrs=get(depth+1);cls=registry().get(name)
            if cls is None or not isinstance(attrs,dict):raise ValueError('unknown binary class')
            obj=cls.__new__(cls);obj.__dict__.update(attrs);return obj
        raise ValueError('unknown binary tag')
    value=get()
    if offset!=len(data):raise ValueError('binary trailing data')
    return value

def digest(value):return hashlib.sha256(encode(value)).hexdigest()

def write(path,value,level=1):
    path=Path(path)
    if path.exists():raise FileExistsError(path)
    raw=encode(value)
    if len(raw)>LIMIT:raise ValueError('oversize binary object')
    payload=zlib.compress(raw,level) if level else raw
    header=MAGIC+bytes([level])+U.pack(len(raw))+hashlib.sha256(raw).digest()
    temporary=path.with_name(path.name+'.partial')
    with temporary.open('xb') as f:
        f.write(header);f.write(payload);f.flush();os.fsync(f.fileno())
    os.replace(temporary,path)
    return {'file':path.name,'bytes':path.stat().st_size,'raw_bytes':len(raw),
            'sha256':hashlib.sha256(header+payload).hexdigest(),'raw_sha256':hashlib.sha256(raw).hexdigest()}

def read(path,expected=None):
    blob=Path(path).read_bytes()
    if expected and hashlib.sha256(blob).hexdigest()!=expected:raise ValueError('binary file checksum mismatch')
    if blob[:8]!=MAGIC or len(blob)<49:raise ValueError('binary file header')
    level=blob[8];size=U.unpack(blob[9:17])[0]
    if level>9 or size>LIMIT:raise ValueError('binary compression/size bound')
    if level:
        d=zlib.decompressobj();raw=d.decompress(blob[49:],size+1)
        if not d.eof or d.unused_data or d.unconsumed_tail:raise ValueError('truncated/oversize compressed payload')
    else:raw=blob[49:]
    if len(raw)!=size or hashlib.sha256(raw).digest()!=blob[17:49]:raise ValueError('binary payload checksum mismatch')
    return decode(raw)
