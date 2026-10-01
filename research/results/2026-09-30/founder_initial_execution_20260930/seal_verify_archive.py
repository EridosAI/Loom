"""Run only after the execution worker has stopped. No simulation or P calls."""
import hashlib
import json
from pathlib import Path
import sys
import time
import zipfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
W=ROOT/'worktrees/loom-p-b1-minimal-20260929'
D=W/'developmental_ecology'
PACKET=ROOT/'exports/2026-09-30-Founder-Search-initial-stage'
ARCHIVE=ROOT/'exports/2026-09-30-Founder-Search-initial-stage-results.zip'
sys.path.insert(0,str(D))
from loom_developmental.verify import verify_store
from loom_developmental.runner import atomic_json,canonical,file_hash

def main():
    seal=json.loads((HERE/'DENOMINATOR_SEALED.json').read_bytes())
    ledger=[json.loads(x) for x in (HERE/'EXECUTION_LEDGER.jsonl').read_bytes().splitlines()]
    assert ledger[-1]['kind']=='STAGE_STOPPED', 'execution is not yet stopped'
    assert len(seal['roster'])==12
    if (HERE/'POSTRUN_VERIFICATION.json').exists() or ARCHIVE.exists():
        raise FileExistsError('No repeated verification/archive operation')
    start=time.perf_counter(); results=[]
    for row in seal['roster']:
        name=row['life_id'];store=HERE/'lives'/name
        if row['state']=='NOT_STARTED':
            assert not store.exists()
            results.append(dict(life_id=name,status='NOT_STARTED',scientific_steps=0));continue
        if time.perf_counter()-start>=180:
            results.append(dict(life_id=name,status='VALIDATION_BUDGET_NOT_REACHED'));continue
        try:
            v=verify_store(store)
            assert v['segments']==1 and v['native_steps']==row['native_steps'] and v['waves']==row['waves']
            assert v['last_receipt_sha256']==row['receipt_sha256']
            results.append(dict(life_id=name,status='PASS',**v))
        except Exception as e:
            results.append(dict(life_id=name,status='FAIL',error=f'{type(e).__name__}: {e}'))
        print(json.dumps({k:v for k,v in results[-1].items() if k in ('life_id','status','verification_wall_seconds','error')}),flush=True)
    verification=dict(denominator=12,results=results,wall_seconds=time.perf_counter()-start,
        passive_only=True,physics_executed=False,P_execution=False,
        all_available_complete_stores_verified=all(r['status'] in ('PASS','NOT_STARTED') for r in results))
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
    manifest=dict(schema=1,denominator=12,checkpoint=seal['checkpoint'],P_commit=seal['P_commit'],
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
            if time.perf_counter()-archive_start>=120:raise RuntimeError('Archive time limit reached; preserve partial artifact')
            z.write(p,key)
    assert ARCHIVE.stat().st_size<=1000000000
    with zipfile.ZipFile(ARCHIVE) as z:
        assert set(z.namelist())==set(paths)|{'EVIDENCE_ARCHIVE_MANIFEST.json'}
        for item in manifest['files']:
            if time.perf_counter()-archive_start>=120:raise RuntimeError('Archive verification time limit reached')
            data=z.read(item['path'])
            assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
    result=dict(path=str(ARCHIVE),sha256=file_hash(ARCHIVE),bytes=ARCHIVE.stat().st_size,
        manifest_sha256=hashlib.sha256(manifest_bytes).hexdigest(),verified_members=len(paths),
        archive_wall_seconds=time.perf_counter()-archive_start,single_complete_archive=True)
    atomic_json(HERE/'ARCHIVE_VERIFICATION.json',result)
    print(json.dumps(result),flush=True)

if __name__=='__main__':main()
