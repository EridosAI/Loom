"""Read-only segment custody, native sequence and exact physical accounting."""
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from . import codec, evidence
from loom_developmental import core
from .runner import file_hash

def catalog(store):
    """Read the small receipt chain only; payloads are verified on interval access."""
    store=Path(store);parent=None;chunks=[];checkpoints=[];identity=None
    if list(store.glob('*.partial')) or list(store.glob('failure-*')):raise ValueError('incomplete/failure store')
    receipts=sorted(store.glob('segment-*.json'))
    if not receipts:raise ValueError('no complete segment')
    for seq,path in enumerate(receipts):
        r=json.loads(path.read_bytes())
        if not r['complete'] or r['segment']!=seq or r['parent_receipt_sha256']!=parent:
            raise ValueError('segment chain mismatch')
        asset=store/r['asset_path']/(r['identity_sha256']+'.json')
        if file_hash(asset)!=r['identity_sha256']:raise ValueError('asset checksum mismatch')
        if identity is not None and identity!=r['identity_sha256']:raise ValueError('segment identity changed')
        identity=r['identity_sha256'];chunks.extend(r['chunks']);checkpoints.extend(r['checkpoints']);parent=file_hash(path)
    return {'chunks':chunks,'checkpoints':checkpoints,'identity_sha256':identity,'last_receipt_sha256':parent}

def verify_store(store):
    start=time.perf_counter();store=Path(store)
    if list(store.glob('*.partial')) or list(store.glob('failure-*')):
        raise ValueError('incomplete/failure store; no automatic continuation')
    receipts=sorted(store.glob('segment-*.json'))
    if not receipts:raise ValueError('no complete segment')
    parent=None;previous=None;allowed=set();native_count=0;wave_count=0;event_count=0;maximum=0.
    families={'native':0,'waves':0,'events':0,'checkpoint':0,'chunks_stored':0,'metadata':0}
    all_chunks=[];checkpoint_refs=[]
    for seq,path in enumerate(receipts):
        r=json.loads(path.read_bytes());attempt=store/f'attempt-{seq:03d}.json';a=json.loads(attempt.read_bytes())
        allowed.update((path.name,attempt.name));families['metadata']+=path.stat().st_size+attempt.stat().st_size
        if r['segment']!=seq or r['parent_receipt_sha256']!=parent or not r['complete']:
            raise ValueError('segment lineage mismatch')
        if a!={'grant':r['grant'],'identity_sha256':r['identity_sha256'],'parent':parent}:
            raise ValueError('attempt/grant mismatch')
        asset=store/r['asset_path']/(r['identity_sha256']+'.json')
        if file_hash(asset)!=r['identity_sha256']:raise ValueError('immutable asset checksum mismatch')
        initial=codec.read(store/r['initial_checkpoint']['file'],r['initial_checkpoint']['sha256'])['engine']
        final=codec.read(store/r['final_checkpoint']['file'],r['final_checkpoint']['sha256'])['engine']
        if previous is not None and codec.digest(core.causal_state(initial))!=previous:
            raise ValueError('continuation state changed')
        if initial.native_index!=r['initial_index'] or final.native_index!=r['final_index']:
            raise ValueError('checkpoint index mismatch')
        if codec.digest(core.causal_state(initial))!=r['grant']['initial_causal_sha256'] or codec.digest(core.causal_state(final))!=r['final_causal_sha256']:
            raise ValueError('checkpoint state binding mismatch')
        initial.validate_state();final.validate_state()
        index=initial.native_index;t=initial.time;waves=initial.organism.wave_count
        for f in r['files']:
            allowed.add(f['file'])
            if file_hash(store/f['file'])!=f['sha256']:raise ValueError('file checksum mismatch')
        for f in r['checkpoints']:
            families['checkpoint']+=f['bytes'];checkpoint_refs.append(f)
        for f in r['chunks']:
            data=codec.read(store/f['file'],f['sha256']);rows=data['native']
            if rows.dtype!=np.dtype('<f8') or rows.ndim!=2 or rows.shape[1]!=evidence.WIDTH or not np.isfinite(rows).all():
                raise ValueError('native array schema/finiteness mismatch')
            if data['first_index']!=index+1 or data['last_index']!=index+len(rows) or data['start_time']!=t:
                raise ValueError('chunk index/time discontinuity')
            for row in rows:
                dt=float(row[evidence.SLICES['elapsed']][0]);t+=dt;index+=1
                if not 0<dt<=initial.c.native_dt or t!=row[0]:raise ValueError('native elapsed mismatch')
            if int(rows[:,evidence.SLICES['event_count']].sum())!=len(data['events']):raise ValueError('event/native alignment mismatch')
            for w in data['waves']:
                waves+=1;wave_count+=1
                if w['wave']!=waves or w['index']%20:raise ValueError('wave discontinuity')
            event_count+=len(data['events']);maximum=max(maximum,evidence.check_ledger(data['events'],initial.c.arithmetic_tol))
            for family in ('native','waves','events'):families[family]+=len(codec.encode(data[family]))
            families['chunks_stored']+=f['bytes'];native_count+=len(rows);all_chunks.append(f)
        if index!=final.native_index or t!=final.time or waves!=final.organism.wave_count:
            raise ValueError('final sequence mismatch')
        if r['status']=='stage_complete' and index!=r['grant']['end_index']:raise ValueError('premature ceiling')
        if (r['status']=='terminal')!=(final.status=='terminal'):raise ValueError('terminal stop mismatch')
        if index>r['grant']['end_index']:raise ValueError('deadline exceeded')
        previous=r['final_causal_sha256'];parent=file_hash(path)
    actual={p.name for p in store.iterdir() if p.is_file()}
    if actual!=allowed:raise ValueError('unsealed/extra evidence tail')
    return {'segments':len(receipts),'native_steps':native_count,'waves':wave_count,'events':event_count,
        'ledger_maximum':maximum,'family_bytes':families,'verification_wall_seconds':time.perf_counter()-start,
        'chunks':all_chunks,'checkpoints':checkpoint_refs,'last_receipt_sha256':parent,
        'final_causal_sha256':previous,'physical_replay':False,'P_execution':False}
