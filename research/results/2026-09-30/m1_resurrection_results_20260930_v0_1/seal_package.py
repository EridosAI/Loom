"""NON-CANONICAL RESURRECTION SANDBOX. Single post-stop archive and byte verification."""
from pathlib import Path
import hashlib,json,sys,time,zipfile
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
PREP=ROOT/'m1_resurrection_sandbox_20260930_v0_1';EX=PREP/'execution'
LABEL='NON-CANONICAL RESURRECTION SANDBOX'
ARCHIVE=ROOT/'M1_RESURRECTION_SANDBOX_20260930_v0_1.zip'
def h(p):
    dig=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):dig.update(b)
    return dig.hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf8')
def main():
    began=time.perf_counter();assert ((EX/'DENOMINATOR.json').exists() or (OUT/'HOST_STOP_DENOMINATOR.json').exists()) and not ARCHIVE.exists()
    assert (OUT/'SANDBOX_REPORT.md').exists()
    assert json.loads((OUT/'PASSIVE_VERIFICATION.json').read_bytes())['status']=='PASS'
    seal=json.loads((OUT/'EXECUTION_CUSTODY_SEAL.json').read_bytes())
    for r in seal['files']:assert h(EX/r['path'])==r['sha256']
    receipt_count=0
    for receipt in (EX/'lives').glob('*/*-RECEIPT.json'):
        r=json.loads(receipt.read_bytes());assert r['complete']
        for ref in r['files']:assert h(receipt.parent/ref['file'])==ref['sha256']
        receipt_count+=1
    prep=json.loads((PREP/'PREPARATION_MANIFEST.json').read_bytes())
    for r in prep['files']:assert h(PREP/r['path'])==r['sha256']
    sys.path.insert(0,str(PREP));from sandbox_runner import runtime_check
    batch=json.loads((PREP/'BATCH_AUTHORITY.json').read_bytes());runtime_check(batch['runtime'])
    historical={}
    for v,sha in [('v0_1','73873228bbc26d9d5de65eb16ee68cd108c61a4691098141be47fe8a29901446'),('v0_2','94a76ee327d257b3902e6f120ddd75300949ab7066015db057b0f4eb2a5228c5')]:
        p=ROOT/('MOTOR_COMMISSIONING_RESULT_20260930_'+v+'.zip');assert h(p)==sha
        oldseal=json.loads((ROOT/('motor_commissioning_results_20260930_'+v)/'EXECUTION_CUSTODY_SEAL.json').read_bytes())
        oldexecution=ROOT/('motor_commissioning_preparation_20260930_'+v)/'execution'
        for row in oldseal['files']:assert h(oldexecution/row['path'])==row['sha256']
        historical[v]=dict(archive_sha256=sha,unchanged_execution_files=len(oldseal['files']))
    save(OUT/'FINAL_VERIFICATION.json',dict(label=LABEL,status='PASS_AVAILABLE_EVIDENCE',runtime=batch['runtime'],
        execution_files=len(seal['files']),execution_bytes=sum(r['bytes'] for r in seal['files']),preparation_files_unchanged=len(prep['files']),
        historical_motor_archives_unchanged=historical,canonical_source_unchanged=True,passive_only_after_stop=True,
        completed_receipts_verified=receipt_count,native_host_failure=(OUT/'HOST_STOP.json').exists(),
        full_state_at_crashed_durable_endpoint_available=False if (OUT/'HOST_STOP.json').exists() else True,
        no_retry_or_replacement=True,no_canonical_amendment=True))
    items=[]
    for directory,prefix in [(PREP,'sandbox'),(OUT,'review')]:
        for p in sorted(directory.rglob('*')):
            if p.is_file() and '__pycache__' not in p.parts and p.name not in ('PACKAGE_MANIFEST.json','ARCHIVE_VERIFICATION.json'):
                items.append((p,prefix+'/'+p.relative_to(directory).as_posix()))
    base=ROOT/'worktrees/loom-contact-release-20260930/developmental_ecology'
    for sub in ('loom_p','loom_developmental'):
        for p in sorted((base/sub).rglob('*.py')):items.append((p,'frozen_source/'+sub+'/'+p.relative_to(base/sub).as_posix()))
    items.append((base/'configuration.json','frozen_source/configuration.json'))
    motor=ROOT/'motor_commissioning_preparation_20260930_v0_2/loom_motor_commissioning'
    for p in sorted(motor.glob('*.py')):items.append((p,'frozen_source/loom_motor_commissioning/'+p.name))
    entries=[dict(path=name,bytes=p.stat().st_size,sha256=h(p)) for p,name in items]
    save(OUT/'PACKAGE_MANIFEST.json',dict(label=LABEL,files=entries,runtime=batch['runtime'],
        note='Frozen source copies are references. Numerical dependency identities are recorded; no dependency installation or automatic relaunch is provided.'))
    items.append((OUT/'PACKAGE_MANIFEST.json','review/PACKAGE_MANIFEST.json'))
    with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_STORED,allowZip64=True) as z:
        for p,name in items:z.write(p,name)
    hashes={r['path']:r['sha256'] for r in entries};hashes['review/PACKAGE_MANIFEST.json']=h(OUT/'PACKAGE_MANIFEST.json')
    with zipfile.ZipFile(ARCHIVE) as z:
        assert len(z.namelist())==len(hashes)==len(set(z.namelist()))
        for name,sha in hashes.items():
            dig=hashlib.sha256()
            with z.open(name) as f:
                for b in iter(lambda:f.read(1<<20),b''):dig.update(b)
            assert dig.hexdigest()==sha
    save(OUT/'ARCHIVE_VERIFICATION.json',dict(label=LABEL,status='PASS',archive=str(ARCHIVE),bytes=ARCHIVE.stat().st_size,
        sha256=h(ARCHIVE),verified_members=len(hashes),single_archive=True,seconds=time.perf_counter()-began))
    print((OUT/'ARCHIVE_VERIFICATION.json').read_text())
if __name__=='__main__':main()
