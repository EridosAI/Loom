"""One append-only continuing life; immutable grants, strong segment boundaries.

No controller, UI, observer callback, automatic continuation or population launch.
"""
import copy
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import sys
import time
import numpy as np
import scipy
from loom_p.records import code_identity
from loom_commissioning.contract import P_CODE,CONFIG
from . import codec, evidence
from loom_developmental import core

def file_hash(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def canonical(value):return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()

def identity():
    from loom_developmental.runner import identity as baseline_identity
    result=baseline_identity()
    root=Path(__file__).parent
    result['motor_commissioning_overlay']={f.name:file_hash(f) for f in sorted(root.glob('*.py'))}
    result['claim']='frozen P core/world with explicitly identified experimental spontaneous motor overlay'
    return result

def validate_grant(g,e,parent):
    keys={'schema','kind','life_id','initial_causal_sha256','initial_index','end_index',
        'parent_receipt_sha256','request_path','request_sha256','wall_limit_seconds','storage_limit_bytes',
        'checkpoint_stride','chunk_steps','compression_level','process','parameters_sha256'}
    if set(g)!=keys or g['schema']!=1 or g['kind']!='motor-temporal-commissioning':
        raise ValueError('explicit motor commissioning grant required')
    if parent is not None or g['parent_receipt_sha256'] is not None:
        raise ValueError('no continuation')
    if e.c.identity()!=CONFIG or e.status not in ('paused','ready'):
        raise ValueError('configuration/status mismatch')
    if e.native_index!=0 or e.time!=0 or e.organism.native_count!=0 or e.organism.wave_count!=0:
        raise ValueError('original blank birth required')
    if g['initial_index']!=0 or g['end_index']!=9000 or type(g['end_index']) is not int:
        raise ValueError('fixed ninety-second scope')
    if g['initial_causal_sha256']!=codec.digest(core.causal_state(e)):
        raise ValueError('initial state mismatch')
    from .motor import PARAMETERS
    if g['parameters_sha256']!=hashlib.sha256(canonical(PARAMETERS)).hexdigest():
        raise ValueError('process parameters changed')
    m=e.organism.motor
    process=getattr(m,'commissioning',{}).get('process','CURRENT')
    if process not in ('CURRENT','M1','M2') or g['process']!=process:
        raise ValueError('process mismatch')
    if g['life_id'] not in [f'MC-FS-{i:03d}-{process}' for i in (1,2,3)]:
        raise ValueError('case not in fixed matrix')
    if e.organism.rng.life!=int(g['life_id'][6:9]):
        raise ValueError('original life stream mismatch')
    limits=(g['wall_limit_seconds'],g['storage_limit_bytes'],g['checkpoint_stride'],g['chunk_steps'],g['compression_level'])
    if limits!=(300,32000000,6000,100,1):
        raise ValueError('fixed resource/recording envelope')
    request=json.loads(Path(g['request_path']).read_bytes())
    if file_hash(g['request_path'])!=g['request_sha256']:
        raise ValueError('approval checksum mismatch')
    bound={k:v for k,v in g.items() if k not in ('request_path','request_sha256')}
    if set(request)!={'notice','approved_scope'} or request['approved_scope']!=bound or not request['notice']:
        raise ValueError('exact separate approval required')

def atomic_json(path,value):
    if path.exists():raise FileExistsError(path)
    temporary=path.with_name(path.name+'.partial')
    with temporary.open('xb') as f:f.write(canonical(value));f.flush();os.fsync(f.fileno())
    os.replace(temporary,path)

class Life:
    def __init__(self,e,store,grant,*,parent=None,asset_root=None):
        self.engine=e;self.store=Path(store);self.grant=copy.deepcopy(grant)
        self.parent=parent;self.closed=False;self.clock_started=time.perf_counter()
        validate_grant(self.grant,e,parent);e.validate_state()
        self.binding=identity();self.identity_sha256=hashlib.sha256(canonical(self.binding)).hexdigest()
        self.asset_root=Path(asset_root) if asset_root else self.store.parent/'shared-assets'
        self.asset_root.mkdir(parents=True,exist_ok=True)
        asset=self.asset_root/(self.identity_sha256+'.json')
        if asset.exists():
            if asset.read_bytes()!=canonical(self.binding):raise ValueError('shared immutable asset changed')
        else:atomic_json(asset,self.binding)
        if parent is None:self.store.mkdir(parents=True,exist_ok=False)
        elif not self.store.is_dir():raise ValueError('missing continuing-life store')
        existing=sorted(self.store.glob('segment-*.json'))
        self.segment=len(existing);self.files=[];self.checkpoints=[];self.chunk_refs=[]
        atomic_json(self.store/f'attempt-{self.segment:03d}.json',{
            'grant':self.grant,'identity_sha256':self.identity_sha256,'parent':parent})
        self.rows=np.empty((self.grant['chunk_steps'],evidence.WIDTH),dtype='<f8');self.used=0
        self.waves=[];self.events=[];self.chunk_start=e.native_index;self.chunk_start_time=e.time
        self.last_index=e.native_index;self.last_time=e.time;self.ledger_maximum=0.;self.event_count=0
        self.blocks=[];self.chunk_started=time.perf_counter();self.bytes_written=0;self.timings={'checkpoint':0.,'chunk_write':0.}
        self.initial_checkpoint=self.checkpoint('initial') if parent is None else self._parent_checkpoint()
        self.run_started=time.perf_counter()

    def _parent_checkpoint(self):
        previous=json.loads(sorted(self.store.glob('segment-*.json'))[-1].read_bytes())
        return previous['final_checkpoint']

    def checkpoint(self,label):
        start=time.perf_counter();e=self.engine
        name=f'checkpoint-{e.native_index:09d}-s{self.segment:03d}-{label}.ld'
        record=codec.write(self.store/name,{'engine':e,'identity':self.identity_sha256,
            'index':e.native_index,'wave':e.organism.wave_count,'life_id':self.grant['life_id']},self.grant['compression_level'])
        record.update(index=e.native_index,wave=e.organism.wave_count,seconds=time.perf_counter()-start)
        self.files.append(record);self.checkpoints.append(record);self.bytes_written+=record['bytes']
        self.timings['checkpoint']+=record['seconds'];return record

    def flush(self):
        if not self.used:return
        e=self.engine;start=time.perf_counter()
        value={'first_index':self.chunk_start+1,'last_index':e.native_index,'start_time':self.chunk_start_time,
            'native':self.rows[:self.used].copy(),'waves':self.waves,'events':self.events,
            'P_endpoint_sha256':codec.digest(e.organism),'rng_endpoint':e.organism.rng.counters.copy(),
            'field_endpoint_sha256':hashlib.sha256(e.fields.tobytes()).hexdigest(),
            'endpoint_status':e.status,'terminal_dimension':e.terminal_dimension}
        name=f'chunk-{self.chunk_start+1:09d}-{e.native_index:09d}.ld'
        record=codec.write(self.store/name,value,self.grant['compression_level'])
        record.update(first_index=self.chunk_start+1,last_index=e.native_index)
        self.files.append(record);self.chunk_refs.append(record);self.bytes_written+=record['bytes']
        self.timings['chunk_write']+=time.perf_counter()-start
        self.blocks.append({'first_index':self.chunk_start+1,'last_index':e.native_index,
            'simulated_seconds':e.time-self.chunk_start_time,'wall_seconds':time.perf_counter()-self.chunk_started})
        self.chunk_start=e.native_index;self.chunk_start_time=e.time;self.used=0;self.waves=[];self.events=[]
        self.chunk_started=time.perf_counter()

    def advance(self,steps=None):
        if self.closed:raise RuntimeError('closed segment')
        remaining=self.grant['end_index']-self.engine.native_index
        steps=remaining if steps is None else steps
        if type(steps)!=int or not 0<=steps<=remaining:raise ValueError('deadline exceeded')
        try:
            for _ in range(steps):
                if time.perf_counter()-self.clock_started>=self.grant['wall_limit_seconds']:
                    self.close('resource_pause','wall_time');break
                # Reserve checkpoint + final chunk before evolution. A failure
                # still becomes an apparatus failure, never biological death.
                if self.bytes_written+16_000_000>=self.grant['storage_limit_bytes']:
                    self.close('resource_pause','storage_reserve');break
                e=self.engine;dt,w,events=core.step(e)
                if e.native_index!=self.last_index+1 or e.time!=self.last_time+dt:
                    raise ArithmeticError('native sequence mismatch')
                self.ledger_maximum=max(self.ledger_maximum,evidence.check_ledger(events,e.c.arithmetic_tol))
                self.event_count+=len(events);self.rows[self.used]=evidence.native_row(e,dt);self.used+=1
                if w is not None:self.waves.append(evidence.wave_row(e,w))
                self.events.extend(events);self.last_index=e.native_index;self.last_time=e.time
                if self.used==len(self.rows):self.flush()
                if e.status=='terminal':self.close('terminal');break
                if e.native_index==self.grant['end_index']:self.close('stage_complete');break
                if e.native_index%self.grant['checkpoint_stride']==0:
                    self.flush();self.checkpoint('periodic')
        except Exception as error:
            # Do not mutate physical/P state to turn an I/O/observer fault into
            # a biological event. Keep a best-effort failure record and stop.
            self.closed=True
            fault={'kind':'apparatus_failure','error':f'{type(error).__name__}: {error}',
                'native_index':self.engine.native_index,'last_recorded_index':self.last_index,
                'complete':False,'parent':self.parent}
            try:atomic_json(self.store/f'failure-s{self.segment:03d}.json',fault)
            except OSError:pass
            try:codec.write(self.store/f'failure-tail-s{self.segment:03d}.ld',{
                'engine':self.engine,'unclosed_native':self.rows[:self.used].copy(),
                'unclosed_waves':self.waves,'unclosed_events':self.events,'failure':fault})
            except (OSError,ValueError):pass
            raise

    def close(self,status='administrative_pause',cause=None):
        if self.closed:raise RuntimeError('segment already closed')
        e=self.engine
        if status not in ('administrative_pause','resource_pause','stage_complete','terminal'):raise ValueError('unknown stop')
        if (status=='terminal')!=(e.status=='terminal'):raise ValueError('terminal label mismatch')
        if status=='stage_complete' and e.native_index!=self.grant['end_index']:raise ValueError('premature stage completion')
        self.flush();e.validate_state();final=self.checkpoint('final')
        value={'schema':1,'life_id':self.grant['life_id'],'segment':self.segment,'parent_receipt_sha256':self.parent,
            'grant':self.grant,'identity_sha256':self.identity_sha256,'asset_path':os.path.relpath(self.asset_root,self.store),
            'status':status,'cause':cause,'complete':True,'initial_checkpoint':self.initial_checkpoint,
            'final_checkpoint':final,'initial_index':self.grant['initial_index'],'final_index':e.native_index,
            'native_steps':e.native_index-self.grant['initial_index'],'wave_index':e.organism.wave_count,
            'final_causal_sha256':codec.digest(core.causal_state(e)),'files':self.files,'chunks':self.chunk_refs,
            'checkpoints':self.checkpoints,'blocks':self.blocks,'event_count':self.event_count,
            'ledger_maximum':self.ledger_maximum,'timings':self.timings,
            'wall_seconds':time.perf_counter()-self.clock_started,'execution_wall_seconds':time.perf_counter()-self.run_started,
            'final_time':e.time,'bytes_written':self.bytes_written}
        # Immutable source checks at segment end; no live function rebinding.
        root=Path(__file__).parent
        if self.binding['motor_commissioning_overlay']!={p.name:file_hash(p) for p in sorted(root.glob('*.py'))} or self.binding['apparatus']!={p.name:file_hash(p) for p in sorted((Path(__import__('loom_developmental').__file__).parent).glob('*.py'))} or code_identity()!=self.binding['P']:
            raise ValueError('execution source changed during segment')
        atomic_json(self.store/f'segment-{self.segment:03d}.json',value)
        self.closed=True;self.receipt=value

    @classmethod
    def continue_life(cls,*args,**kwargs):
        raise ValueError('No continuation/retry in motor commissioning')
