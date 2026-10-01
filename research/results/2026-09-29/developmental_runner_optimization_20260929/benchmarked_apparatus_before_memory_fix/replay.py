"""Tier 2: exact P reconstruction from realized sensory inputs, never physics.

Optional field reconstruction uses recorded stocks/poses, not a new trajectory.
Returned objects are detached. There is no path back into the live recorder.
"""
import copy
import hashlib
import json
from pathlib import Path
import numpy as np
from loom_commissioning.diagnostics import passive
from loom_commissioning.contract import INTACT
from . import codec,core,evidence
from .verify import catalog
from .runner import identity,canonical

def apply_body(e,row):
    s=evidence.SLICES;b=e.body
    for field,key in [('position','position'),('velocity','velocity'),('command','commands'),('force','forces'),('contact_rates','contact_rates')]:
        setattr(b,field,row[s[key]].copy())
    b.angle=float(row[s['angle']][0]);b.omega=float(row[s['omega']][0])
    b.energy,b.integrity=map(float,row[s['reserves']]);e.stocks=row[s['stocks']].copy()

def reconstruct(store,*,first_index=None,last_index=None,deep=False,fields=False,callback=None):
    """Read complete custody; decompress only the interval from its nearest checkpoint.

    callback receives detached reconstructed states/diagnostics for engineering
    checks or analysis. It is never supplied a live Life or engine reference.
    """
    store=Path(store);custody=catalog(store)
    if hashlib.sha256(canonical(identity())).hexdigest()!=custody['identity_sha256']:
        raise ValueError('reconstruction runtime/code changed')
    checkpoints=custody['checkpoints'];chunks=custody['chunks']
    first=first_index if first_index is not None else min(x['index'] for x in checkpoints)+1
    last=last_index if last_index is not None else max(x['last_index'] for x in chunks)
    cp=max((x for x in checkpoints if x['index']<first),key=lambda x:x['index'])
    e=codec.read(store/cp['file'],cp['sha256'])['engine'];count=0;checked_chunks=0
    for chunk in chunks:
        if chunk['last_index']<=e.native_index or chunk['first_index']>last:continue
        data=codec.read(store/chunk['file'],chunk['sha256']);waves={w['index']:w for w in data['waves']};event_offset=0
        for index,row in enumerate(data['native'],data['first_index']):
            count_events=int(row[evidence.SLICES['event_count']][0])
            events=data['events'][event_offset:event_offset+count_events];event_offset+=count_events
            if index<=e.native_index:continue
            if index>last:break
            before=copy.deepcopy(e) if deep else None
            dt=float(row[evidence.SLICES['elapsed']][0]);old_index=e.native_index
            refresh=old_index>0 and old_index%round(e.c.noise_refresh/e.c.native_dt)==0
            command=e.organism.native(e.raw,dt,refresh_noise=refresh)
            if not np.array_equal(command,row[evidence.SLICES['commands']]):raise ValueError('P command reconstruction mismatch')
            apply_body(e,row);e.time=float(row[0]);e.native_index=index
            if fields:e.fields=e.solver.step(e.fields,e.stocks,e.time,e.phase,dt,e.body.position)
            e.raw=evidence.raw_tuple(row);e.last_native={'elapsed':dt,'time':e.time,'native_index':index};e.last_wave=None
            e.last_events=events
            terminal=index==data['last_index'] and data['endpoint_status']=='terminal'
            if terminal:e.status='terminal';e.terminal_dimension=data['terminal_dimension']
            elif index%round(e.c.wave_dt/e.c.native_dt)==0:
                e.last_wave=e.organism.handoff(e.body.reserves)
                if index not in waves or codec.encode(evidence.wave_row(e,e.last_wave))!=codec.encode(waves[index]):
                    raise ValueError('actual wave output reconstruction mismatch')
            actual=[e.organism.rng.counters[k] for k in evidence.DYNAMIC]
            if not np.array_equal(actual,row[evidence.SLICES['rng_dynamic']]):raise ValueError('native RNG reconstruction mismatch')
            if index>=first:
                count+=1
                diag=passive(before,e,e.last_wave,INTACT,None) if deep else None
                if callback is not None:callback(index,e,diag)
        if e.native_index==data['last_index']:
            if codec.digest(e.organism)!=data['P_endpoint_sha256'] or e.organism.rng.counters!=data['rng_endpoint']:
                raise ValueError('exact P/RNG chunk endpoint mismatch')
            if fields and hashlib.sha256(e.fields.tobytes()).hexdigest()!=data['field_endpoint_sha256']:
                raise ValueError('realized field reconstruction mismatch')
            checked_chunks+=1
    return {'engine':e,'native_reconstructed':count,'checked_chunks':checked_chunks,
        'physics_executed':False,'fields_reconstructed':fields,'live_state_modified':False}
