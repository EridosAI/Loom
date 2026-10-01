"""Read-only arithmetic reconstruction of the three saved cases; no complete-loop run."""
import gzip
import hashlib
import json
from pathlib import Path
import time
import numpy as np
from loom_p.records import load_snapshot,state_hash,strict_bytes,code_identity
from loom_p.reconstruction import reconstruct
from loom_p.smokes import CASES

ROOT=Path(__file__).resolve().parent

def verify(root):
    start=time.perf_counter(); m=json.loads((root/'manifest.json').read_text())
    assert m['complete'] and m['status'] in ('administrative_pause','terminal')
    assert m['code']==code_identity()
    for name,row in m['files'].items():
        data=(root/name).read_bytes()
        assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
    initial=load_snapshot(root/'initial.snapshot.json.gz'); final=load_snapshot(root/'final.snapshot.json.gz')
    rows={}
    for kind in ('native','wave','events'):
        with gzip.open(root/(kind+'.jsonl.gz'),'rt',encoding='utf-8') as handle: rows[kind]=[json.loads(line) for line in handle]
        assert len(rows[kind])==m['records'].get(kind,0)
    native=rows['native']; assert final.time<=m['simulated_seconds_cap']+1e-10
    assert [r['native_index'] for r in native]==list(range(1,len(native)+1))
    assert all(b['time']>a['time'] for a,b in zip(native,native[1:]))
    o,reconstruction=reconstruct(root,len(native)-1)
    assert state_hash(o)==state_hash(final.organism)
    assert native[-1]['random_counters']==final.organism.rng.counters
    assert final.organism.rng.counters['life/motor-noise']==1+(len(native)-1)//50
    assert final.organism.rng.counters['life/regulation-E']==1+len(rows['wave'])
    fields=initial.fields.copy()
    for row in native:
        fields=initial.solver.step(fields,np.asarray(row['stocks']),row['time'],initial.phase,row['elapsed'],np.asarray(row['position']))
    assert np.array_equal(fields,final.fields)
    max_balance=0.
    for ev in rows['events']:
        before=np.asarray(ev['stock_before']); after=np.asarray(ev['stock_after'])
        renewal=np.asarray(ev['renewal_first'])+np.asarray(ev['renewal_second'])
        transfer=np.asarray(ev['transfer'])
        error=max(abs(ev['energy_after']-ev['energy_before']-transfer.sum()+ev['expenditure']),float(np.max(abs(after-before-renewal+transfer))))
        max_balance=max(max_balance,error); assert error<1e-12
        if ev['impact']: assert ev['duration']==0 and transfer.sum()==0 and ev['repair']==0
    return dict(case=m['case'],path=str(root),complete=True,native=len(native),wave=len(rows['wave']),events=len(rows['events']),time=final.time,status=m['status'],snapshot_initial_hash=state_hash(load_snapshot(root/'initial.snapshot.json.gz')),snapshot_final_hash=state_hash(final),reconstruction=reconstruction,field_reconstruction_bit_identical=True,max_accounting_error=max_balance,final_reserves=final.body.reserves.tolist(),record_scalar_widths=m['scalar_widths'],uncompressed_bytes=m['uncompressed_bytes'],stored_bytes=sum(r['bytes'] for r in m['files'].values()),execution_wall_seconds=m['wall_seconds'],verification_wall_seconds=time.perf_counter()-start,noise_clock_checked=True,archive_checksums_checked=True)

if __name__=='__main__':
    results=[]
    for case in CASES:
        matches=sorted((ROOT/'artifacts').glob(f'smoke-{case}-attempt-*/manifest.json'),reverse=True)
        valid=[p.parent for p in matches if json.loads(p.read_text()).get('complete')]
        if not valid: raise ValueError(f'No completed named case: {case}')
        results.append(verify(valid[0])); print(json.dumps(results[-1]),flush=True)
    target=ROOT/'artifacts'/'verification'/'record-reconstruction.json'
    with target.open('xb') as handle: handle.write(strict_bytes(dict(cases=results,method='Detached neural and field arithmetic from recorded actual inputs; no complete body/world/organism loop executed.')))
