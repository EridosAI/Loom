"""Detached structural reconstruction from saved actual inputs; no world run or live mutation."""
import gzip
import hashlib
import json
from pathlib import Path
import numpy as np
from .records import load_snapshot,state_bytes

def reconstruct(directory,index):
    root=Path(directory); e=load_snapshot(root/'initial.snapshot.json.gz')
    if index<0: return e.organism,dict(snapshot_time=e.time,time=e.time,records_checked=0,identical=True)
    checked=0; raw=e.raw; c=e.c; o=e.organism
    with gzip.open(root/'native.jsonl.gz','rt',encoding='utf-8') as handle:
        for i,line in enumerate(handle):
            if i>index: break
            row=json.loads(line); native_index=row['native_index']-1
            refresh=native_index>0 and native_index%round(c.noise_refresh/c.native_dt)==0
            command=o.native(raw,row['elapsed'],refresh)
            if not np.array_equal(command,np.asarray(row['commands'])):
                raise ValueError(f'Reconstruction command mismatch at native {native_index+1}')
            if row['status']!='terminal' and row['native_index']%round(c.wave_dt/c.native_dt)==0:
                o.handoff(np.asarray(row['reserves']))
            digest=hashlib.sha256(state_bytes(o)).hexdigest()
            if digest!=row['organism_sha256']:
                raise ValueError(f'Reconstruction structural mismatch at native {native_index+1}')
            raw=tuple(np.asarray(x,dtype=np.float64) for x in row['raw']); checked+=1
    if checked!=index+1: raise ValueError('Requested reconstruction is beyond the saved record')
    return o,dict(snapshot_time=e.time,time=row['time'],records_checked=checked,identical=True,
                  provenance='Detached reconstruction from initial full snapshot and each saved actual receptor/reserve input; every complete neural-state hash matched. No body/world simulation or live-state change.')
