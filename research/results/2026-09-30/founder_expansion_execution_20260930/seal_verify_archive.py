"""Run only after the execution worker has stopped. No simulation or P calls."""
import hashlib
from datetime import datetime, timezone
import numpy as np
import json
from pathlib import Path
import sys
import time
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
W=ROOT/'worktrees/loom-p-b1-minimal-20260929'
D=W/'developmental_ecology'
PACKET=ROOT/'exports/2026-09-30-Founder-Search-expansion-48'
ARCHIVE=ROOT/'exports/2026-09-30-Founder-Search-expansion-48-results.zip'
sys.path.insert(0,str(D))
from loom_developmental.verify import verify_store
from loom_developmental import codec,core,evidence
from loom_developmental.runner import atomic_json,canonical,file_hash

def main():
    seal=json.loads((HERE/'DENOMINATOR_SEALED.json').read_bytes())
    ledger=[json.loads(x) for x in (HERE/'EXECUTION_LEDGER.jsonl').read_bytes().splitlines()]
    assert ledger[-1]['kind']=='STAGE_STOPPED' or (HERE/'INTERRUPTION_CUSTODY_SEAL.json').exists(), 'execution is not stopped'
    interrupted=json.loads((HERE/'INTERRUPTION_CUSTODY_SEAL.json').read_bytes()) if (HERE/'INTERRUPTION_CUSTODY_SEAL.json').exists() else None
    assert len(seal['roster'])==48
    if (HERE/'POSTRUN_VERIFICATION.json').exists() or ARCHIVE.exists():
        raise FileExistsError('No repeated verification/archive operation')
    start=time.perf_counter(); results=[]
    if interrupted:
        start-=max(0.,(datetime.now(timezone.utc)-datetime.fromisoformat(interrupted['validation_phase_first_observation_utc'])).total_seconds())
    prior=ROOT/'founder_initial_execution_20260930'
    old=json.loads((prior/'DENOMINATOR_SEALED.json').read_bytes())
    assert file_hash(prior/'DENOMINATOR_SEALED.json')=='1d3950dc462d2e003016fdb511d21871e8d3c4f6bd7caa5f81bfed1d51ed1d5a'
    def streaming_hash(p):
        h=hashlib.sha256()
        with p.open('rb') as f:
            for block in iter(lambda:f.read(8*1024*1024),b''):h.update(block)
        return h.hexdigest()
    old_archive=ROOT/'exports/2026-09-30-Founder-Search-initial-stage-results.zip'
    assert streaming_hash(old_archive)=='e3377cb965f6801b2e9a53831af6afddffe9814eea7ba78cb1ba71da9fcfbb29'
    for row in old['roster']:
        assert file_hash(prior/'lives'/row['life_id']/'segment-000.json')==row['receipt_sha256']
    atomic_json(HERE/'COMBINED_DENOMINATOR_SEALED.json',dict(schema=1,denominator=60,
        roster=[dict(x,evidence_cohort='preserved_initial_12') for x in old['roster']]+[dict(x,evidence_cohort='expansion_48') for x in seal['roster']],
        prior_seal_sha256=file_hash(prior/'DENOMINATOR_SEALED.json'),expansion_seal_sha256=file_hash(HERE/'DENOMINATOR_SEALED.json'),
        preserved_archive_sha256=streaming_hash(old_archive),no_selection=True))
    for row in seal['roster']:
        name=row['life_id'];store=HERE/'lives'/name
        if row['state']=='NOT_STARTED':
            assert not store.exists()
            results.append(dict(life_id=name,status='NOT_STARTED',scientific_steps=0));continue
        if time.perf_counter()-start>=720:
            results.append(dict(life_id=name,status='VALIDATION_BUDGET_NOT_REACHED'));continue
        try:
            if not row.get('complete'):
                assert name=='FS-060' and interrupted and not (store/'segment-000.json').exists()
                assert {p.name for p in store.iterdir() if p.is_file()}=={f['file'] for f in interrupted['files']}
                for f in interrupted['files']:assert file_hash(store/f['file'])==f['sha256']
                initial_ref=next(f for f in interrupted['files'] if f['file'].endswith('-initial.ld'))
                initial=codec.read(store/initial_ref['file'],initial_ref['sha256'])['engine']
                attempt=json.loads((store/'attempt-000.json').read_bytes())
                assert codec.digest(core.causal_state(initial))==attempt['grant']['initial_causal_sha256']
                index=0;t=0.;waves=0;events=0;maximum=0.
                for f in sorted(interrupted['files'],key=lambda f:f['file']):
                    if not f['file'].startswith('chunk-'):continue
                    chunk=codec.read(store/f['file'],f['sha256']);a=chunk['native']
                    assert chunk['first_index']==index+1 and chunk['start_time']==t
                    assert a.dtype==np.dtype('<f8') and a.ndim==2 and a.shape[1]==evidence.WIDTH and np.isfinite(a).all()
                    for n in a:
                        dt=float(n[evidence.SLICES['elapsed']][0]);assert 0<dt<=initial.c.native_dt
                        t+=dt;index+=1;assert t==n[0]
                    assert chunk['last_index']==index and int(a[:,evidence.SLICES['event_count']].sum())==len(chunk['events'])
                    for w in chunk['waves']:
                        waves+=1;assert w['wave']==waves and w['index']%20==0
                    events+=len(chunk['events']);maximum=max(maximum,evidence.check_ledger(chunk['events'],initial.c.arithmetic_tol))
                assert (index,waves,t)==(row['native_steps'],row['waves'],row['simulated_seconds'])
                results.append(dict(life_id=name,status='PREFIX_CUSTODY_PASS_UNCLOSED',native_steps=index,waves=waves,events=events,
                    observed_through_seconds=t,ledger_maximum=maximum,complete_life=False,exact_execution_end_unknown=True,
                    claim='Verified preserved files, sequence and event accounting only; no runner closure or unrecorded-tail claim.'))
                print(json.dumps(results[-1]),flush=True);continue
            v=verify_store(store)
            assert v['segments']==1 and v['native_steps']==row['native_steps'] and v['waves']==row['waves']
            assert v['last_receipt_sha256']==row['receipt_sha256']
            results.append(dict(life_id=name,status='PASS',**v))
        except Exception as e:
            results.append(dict(life_id=name,status='FAIL',error=f'{type(e).__name__}: {e}'))
        print(json.dumps({k:v for k,v in results[-1].items() if k in ('life_id','status','verification_wall_seconds','error')}),flush=True)
    verification=dict(denominator=48,results=results,wall_seconds=time.perf_counter()-start,
        passive_only=True,physics_executed=False,P_execution=False,
        incomplete_stores_separately_marked=True,all_available_complete_stores_verified=all(r['status'] in ('PASS','NOT_STARTED','PREFIX_CUSTODY_PASS_UNCLOSED') for r in results))
    atomic_json(HERE/'POSTRUN_VERIFICATION.json',verification)
    # All original records stay in place. The sole complete evidence copy is this archive.
    paths={}
    for p in HERE.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts and 'analysis' not in p.relative_to(HERE).parts:
            paths['execution/'+p.relative_to(HERE).as_posix()]=p
    for p in PACKET.rglob('*'):
        if p.is_file():paths['launch_packet/'+p.relative_to(PACKET).as_posix()]=p
    for folder in ('loom_p','loom_developmental','loom_commissioning'):
        for p in (D/folder).glob('*.py'):paths['source/developmental_ecology/'+folder+'/'+p.name]=p
    paths['source/developmental_ecology/configuration.json']=D/'configuration.json'
    for name in ('pyproject.toml','requirements.txt'):
        if (D/name).is_file():paths['source/developmental_ecology/'+name]=D/name
    manifest=dict(schema=1,combined_denominator=60,preserved_prior_archive_sha256='e3377cb965f6801b2e9a53831af6afddffe9814eea7ba78cb1ba71da9fcfbb29',denominator=48,checkpoint=seal['checkpoint'],P_commit=seal['P_commit'],
        sealed_denominator_sha256=file_hash(HERE/'DENOMINATOR_SEALED.json'),
        verification_sha256=file_hash(HERE/'POSTRUN_VERIFICATION.json'),
        files=[dict(path=k,bytes=p.stat().st_size,sha256=file_hash(p)) for k,p in sorted(paths.items())],
        analysis='Subsequent passive A/B/C reports are separate, linked by this archive SHA256; no second complete evidence copy.',
        prior_engineering_archive='The launch-packet archive is preserved separately; historical engineering payloads are not duplicated here.')
    manifest_bytes=canonical(manifest)
    atomic_json(HERE/'EVIDENCE_ARCHIVE_MANIFEST.json',manifest)
    archive_start=time.perf_counter()
    with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
        z.writestr('EVIDENCE_ARCHIVE_MANIFEST.json',manifest_bytes)
        for key,p in sorted(paths.items()):
            if time.perf_counter()-archive_start>=480:raise RuntimeError('Archive time limit reached; preserve partial artifact')
            z.write(p,key)
    assert ARCHIVE.stat().st_size<=4100000000
    with zipfile.ZipFile(ARCHIVE) as z:
        assert set(z.namelist())==set(paths)|{'EVIDENCE_ARCHIVE_MANIFEST.json'}
        for item in manifest['files']:
            if time.perf_counter()-archive_start>=480:raise RuntimeError('Archive verification time limit reached')
            data=z.read(item['path'])
            assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
    result=dict(path=str(ARCHIVE),sha256=streaming_hash(ARCHIVE),bytes=ARCHIVE.stat().st_size,
        manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),verified_members=len(paths),
        archive_wall_seconds=time.perf_counter()-archive_start,single_complete_archive=True)
    atomic_json(HERE/'ARCHIVE_VERIFICATION.json',result)
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
