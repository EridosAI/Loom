"""Final read-only source/custody verification and one portable review archive."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,zipfile,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
OLD=ROOT/'motor_commissioning_preparation_20260930_v0_1';EX=OLD/'execution'
RESULT=ROOT/'motor_commissioning_results_20260930_v0_1'
NEW=ROOT/'motor_commissioning_preparation_20260930_v0_2'
WT=ROOT/'worktrees/loom-contact-release-20260930';D=WT/'developmental_ecology'
ARCHIVE=ROOT/'MOTOR_CONTACT_CORRECTION_AND_SCREEN_v0_2_20260930.zip'
def sha(p):
    with Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def read(p):return json.loads(p.read_bytes())
def save(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf8')
def verify(base,rows):
    for r in rows:
        p=base/r['path'];assert sha(p)==r['sha256'],str(p)
        if 'bytes' in r:assert p.stat().st_size==r['bytes'],str(p)
    return len(rows)
def git(*args):return subprocess.check_output(['git','-c','safe.directory='+WT.as_posix(),'--no-optional-locks','-C',str(WT),*args],text=True).strip()
assert not ARCHIVE.exists()
seal=read(RESULT/'EXECUTION_CUSTODY_SEAL.json');checks={}
checks['historical_execution_files']=verify(EX,seal['files'])
assert {p.relative_to(EX).as_posix() for p in EX.rglob('*') if p.is_file()}=={r['path'] for r in seal['files']}
for r in seal['files']:assert (EX/r['path']).stat().st_mtime_ns==r['mtime_ns']
oldmanifest=read(OLD/'PACKAGE_MANIFEST.json');checks['historical_preparation_files']=verify(OLD,oldmanifest['files'])
oldresultmanifest=read(RESULT/'PACKAGE_MANIFEST.json')
checks['historical_result_files']=verify(RESULT,[dict(r,path=r['path'][8:]) for r in oldresultmanifest['files'] if r['path'].startswith('results/')])
oldzip=read(RESULT/'ARCHIVE_VERIFICATION.json');assert sha(Path(oldzip['path']))==oldzip['sha256']
checks['historical_result_archive_sha256']=oldzip['sha256']
assert not (NEW/'execution').exists()
assert git('rev-parse','HEAD')=='1d7cd6fd450ea528562b2c825589ab4de18a5b38'
assert git('status','--porcelain')==''
changed=git('diff','--name-only','87abae34e19d4e46234402a6b1ba776814956ec1','HEAD').splitlines()
assert set(x for x in changed if '/loom_' in x)=={'developmental_ecology/loom_p/physics.py','developmental_ecology/loom_developmental/runner.py'}
patch=subprocess.check_output(['git','-c','safe.directory='+WT.as_posix(),'--no-optional-locks','-C',str(WT),'diff','--binary','87abae34e19d4e46234402a6b1ba776814956ec1','HEAD'])
(HERE/'EXACT_IMPLEMENTATION.diff').write_bytes(patch)
runtime=read(NEW/'RUNTIME_IDENTITY.json');oldruntime=read(OLD/'RUNTIME_IDENTITY.json')
assert [k for k,v in runtime['P']['files'].items() if v!=oldruntime['P']['files'][k]]==['physics.py']
assert [k for k,v in runtime['apparatus'].items() if v!=oldruntime['apparatus'][k]]==['runner.py']
for k in ('runtime_files','python_runtime_files','executable','numpy','scipy','native_fields'):assert runtime[k]==oldruntime[k]
assert sha(D/'configuration.json')=='985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9'
for name in ('motor.py','codec.py','evidence.py','verify.py','__init__.py'):
    assert sha(NEW/'loom_motor_commissioning'/name)==sha(OLD/'loom_motor_commissioning'/name)
for name in ('PARAMETERS.json','ANALYSIS_PLAN.md','RESOURCE_PLAN.json'):assert sha(NEW/name)==sha(OLD/name)
diff=read(NEW/'SEMANTIC_DIFF.json');assert diff['unexpected_semantic_changes']==[]
matrix=read(NEW/'MATRIX.json')['cases'];oldmatrix=read(OLD/'MATRIX.json')['cases']
for row,prior in zip(matrix,oldmatrix):
    assert row['case_id']==prior['case_id'] and row['authority_sha256']!=prior['authority_sha256']
    assert sha(NEW/'authorities'/(row['case_id']+'.json'))==row['authority_sha256']
    a=read(NEW/'authorities'/(row['case_id']+'.json'))
    for path,h in a['execution_files'].items():assert sha(NEW/path)==h
    assert a['runtime_sha256']==sha(NEW/'RUNTIME_IDENTITY.json')
    assert a['corrected_apparatus_checkpoint']==git('rev-parse','HEAD')
test_counts={}
for path in (HERE/'MECHANICS_GREEN_03.xml',HERE/'IDENTITY_TESTS.xml',NEW/'COMPONENT_TESTS.xml'):
    suite=ET.parse(path).getroot().find('testsuite')
    assert int(suite.get('failures'))==int(suite.get('errors'))==0
    test_counts[path.name]=int(suite.get('tests'))
regression=read(HERE/'HISTORICAL_REGRESSION.json');assert regression['status']=='PASS'
assert [r['steps'] for r in regression['cases']]==[9000,9000,1025]
final=dict(status='PASS_FOR_FRESH_BOUNDED_SCREEN_PREPARATION',utc=datetime.now(timezone.utc).isoformat(),
    checks=checks,component_test_counts=test_counts,exact_failed_geometry_reproduced=True,
    old_guard_still_rejects_invalid_free_path=True,physical_tolerances_unchanged=True,
    historical_trajectory_regression=regression,corrected_restart_bit_identical=True,
    apparatus_checkpoint=git('rev-parse','HEAD'),branch=git('branch','--show-current'),worktree=str(WT),
    changed_files=changed,runtime_sha256=sha(NEW/'RUNTIME_IDENTITY.json'),new_authorities=9,
    new_packet_static_preflight=read(NEW/'STATIC_PREFLIGHT_REPORT.json')['status'],
    all_initial_engine_bytes_unchanged=True,motor_process_and_distribution_unchanged=True,
    new_motor_screen_executions=0,long_runs=0,new_prehistory=0,
    old_records_modified=False,source_or_configuration_tuning=False,automatic_selection=False,
    nursery_changes=False,P_neural_learning_changes=False,world_constitutive_parameter_changes=False,
    overnight_sandbox_readiness='NOT_ESTABLISHED_NOT_READY_FOR_LAUNCH',
    test_attempt_qualification='First replay harness passed all prefixes then failed before corrected physical step in a tracing hook; engineering replay repeated successfully. Two prefix reconstructions, no scientific retries.',
    historical_prefix_reconstruction_passes=2,engineering_committed_replay_steps_both_attempts=38052,
    engineering_step_after_1025=1026,no_later_M2_step_attempted=True,push=False,merge=False)
save(HERE/'FINAL_VERIFICATION.json',final)
save(NEW/'FINAL_VERIFICATION.json',{k:v for k,v in final.items() if k!='historical_trajectory_regression'})
packetfiles=[dict(path=p.relative_to(NEW).as_posix(),bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(NEW.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='PACKAGE_MANIFEST.json']
save(NEW/'PACKAGE_MANIFEST.json',dict(kind='NINE_UNAUTHORIZED_PROPOSALS',files=packetfiles))
members={}
for row in packetfiles:members['new_packet/'+row['path']]=NEW/row['path']
members['new_packet/PACKAGE_MANIFEST.json']=NEW/'PACKAGE_MANIFEST.json'
for p in HERE.iterdir():
    if p.is_file() and p.name not in ('PACKAGE_MANIFEST.json','ARCHIVE_VERIFICATION.json'):members['correction_review/'+p.name]=p
for p in D.rglob('*.py'):
    if 'artifacts' not in p.parts and 'worktrees' not in p.relative_to(D).parts and '__pycache__' not in p.parts:
        members['corrected_source/developmental_ecology/'+p.relative_to(D).as_posix()]=p
for rel in ('developmental_ecology/configuration.json','developmental_ecology/tests/fixtures/fs001_m2_step1026.json','docs/developmental_ecology/CONTACT_FACE_RELEASE_CORRECTION_20260930.md'):
    members['corrected_source/'+rel]=WT/rel
for row in seal['files']:members['historical_v0_1/execution/'+row['path']]=EX/row['path']
for row in oldmanifest['files']:members['historical_v0_1/preparation/'+row['path']]=OLD/row['path']
members['historical_v0_1/preparation/PACKAGE_MANIFEST.json']=OLD/'PACKAGE_MANIFEST.json'
for name in ('MOTOR_COMMISSIONING_RESULT_v0_1.md','FS001_PATHS.png','FS001_TIMING.png','DENOMINATOR_RECONCILIATION.json','EXECUTION_CUSTODY_SEAL.json','PASSIVE_VALIDATION.json','ARCHIVE_VERIFICATION.json'):
    members['historical_v0_1/result/'+name]=RESULT/name
# Preserve input references needed by preflight/reconstruction, without generating anything.
founder=ROOT/'exports/2026-09-30-Founder-Search-initial-stage'
for row in matrix:
    a=read(NEW/'authorities'/(row['case_id']+'.json'))
    paths={a['original_snapshot']['path']:a['original_snapshot']['sha256'],**a['preserved_preparation_files']}
    for rel,digest in paths.items():
        assert sha(founder/rel)==digest
        members['preserved_founder_inputs/'+rel]=founder/rel
manifest=dict(kind='CONTACT_ENGINEERING_REVIEW_AND_UNAUTHORIZED_SCREEN',
    files=[dict(path=n,bytes=p.stat().st_size,sha256=sha(p)) for n,p in sorted(members.items())])
save(HERE/'PACKAGE_MANIFEST.json',manifest)
with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,p in sorted(members.items()):z.write(p,name)
    z.write(HERE/'PACKAGE_MANIFEST.json','PACKAGE_MANIFEST.json')
with zipfile.ZipFile(ARCHIVE) as z:
    assert z.testzip() is None
    for row in manifest['files']:
        data=z.read(row['path']);assert len(data)==row['bytes'] and hashlib.sha256(data).hexdigest()==row['sha256']
verify(EX,seal['files']);verify(NEW,packetfiles)
archive=dict(path=str(ARCHIVE),bytes=ARCHIVE.stat().st_size,sha256=sha(ARCHIVE),verified_members=len(members)+1,status='PASS')
save(HERE/'ARCHIVE_VERIFICATION.json',archive)
print(json.dumps(dict(verification_status=final['status'],archive=archive),indent=2))
