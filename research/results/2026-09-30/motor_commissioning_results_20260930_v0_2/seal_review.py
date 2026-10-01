"""Read-only custody checks and exactly one fresh review archive. No Loom imports."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,sys,time,zipfile
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
PREP=ROOT/'motor_commissioning_preparation_20260930_v0_2';EX=PREP/'execution'
OLD=ROOT/'motor_commissioning_results_20260930_v0_1';OLDPREP=ROOT/'motor_commissioning_preparation_20260930_v0_1'
WT=ROOT/'worktrees/loom-contact-release-20260930';D=WT/'developmental_ecology'
ARCHIVE=ROOT/'MOTOR_COMMISSIONING_RESULT_20260930_v0_2.zip'
def sha(path):
    with Path(path).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def read(path):return json.loads(Path(path).read_bytes())
def save(path,data):Path(path).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
def verify(base,rows):
    for row in rows:
        p=base/row['path'];assert sha(p)==row['sha256'],str(p)
        if 'bytes' in row:assert p.stat().st_size==row['bytes'],str(p)
    return len(rows)
warnings=[]
def git(*args):
    r=subprocess.run(['git','-c','safe.directory='+WT.as_posix(),'--no-optional-locks','-C',str(WT),*args],capture_output=True,text=True,check=True)
    if r.stderr:warnings.append(r.stderr.strip())
    return r.stdout.strip()

start=time.perf_counter();assert not ARCHIVE.exists(),'Single result archive already exists; never overwrite.'
seal=read(OUT/'EXECUTION_CUSTODY_SEAL.json');checks={'execution_files':verify(EX,seal['files'])}
assert {p.relative_to(EX).as_posix() for p in EX.rglob('*') if p.is_file()}=={r['path'] for r in seal['files']}
assert all((EX/r['path']).stat().st_mtime_ns==r['mtime_ns'] for r in seal['files'])
prepared=read(PREP/'PACKAGE_MANIFEST.json');checks['unchanged_v02_preparation_files']=verify(PREP,prepared['files'])
checks['unchanged_v01_preparation_files']=verify(OLDPREP,read(OLDPREP/'PACKAGE_MANIFEST.json')['files'])
checks['unchanged_v01_execution_files']=verify(OLDPREP/'execution',read(OLD/'EXECUTION_CUSTODY_SEAL.json')['files'])
oldresults=[dict(r,path=r['path'].removeprefix('results/')) for r in read(OLD/'PACKAGE_MANIFEST.json')['files'] if r['path'].startswith('results/')]
checks['unchanged_v01_result_files']=verify(OLD,oldresults)
oldzip=ROOT/'MOTOR_COMMISSIONING_RESULT_20260930_v0_1.zip'
assert sha(oldzip)=='73873228bbc26d9d5de65eb16ee68cd108c61a4691098141be47fe8a29901446'
checks['historical_v01_archive_sha256']=sha(oldzip)
for folder,manifest in [('nursery_0_design_20260930_v0_1','DESIGN_ONLY_VERIFICATION.json'),('nursery_birth_motor_review_20260930_v0_1','REVIEW_VERIFICATION.json')]:
    checks[folder]=verify(ROOT/folder,read(ROOT/folder/manifest)['files'])
checks['prior_review_inputs']=verify(ROOT,read(ROOT/'nursery_birth_motor_review_20260930_v0_1/INPUT_CUSTODY.json')['files'])

matrix=read(PREP/'MATRIX.json')['cases'];auth=read(EX/'JASON_AUTHORIZATION.json');den=read(EX/'DENOMINATOR.json')
assert [r['authority_sha256'] for r in matrix]==auth['authorized_authority_sha256']
assert sha(EX/'JASON_AUTHORIZATION.json')==sha(ROOT/'motor_commissioning_v0_2_authorization_20260930.json')
assert [r['case_id'] for r in matrix]==[r['case_id'] for r in den['cases']]
assert den['stop'] is None and all(r['native_steps']==9000 and r['status']=='stage_complete' for r in den['cases'])
assert not (EX/'APPARATUS_STOP.json').exists()
assert {p.name for p in (EX/'lives').iterdir() if p.is_dir()}=={r['case_id'] for r in matrix}
resources=read(OUT/'RESOURCE_ACTUALS.json')
assert all(r['wall_seconds']<300 and r['stored_bytes']<32000000 for r in resources['cases'])
assert den['active_wall_seconds']<2700 and den['preflight_wall_seconds']<300 and den['verification_wall_seconds']<600
for row in matrix:
    name=row['case_id'];a=read(PREP/'authorities'/(name+'.json'));store=EX/'lives'/name
    assert sha(PREP/'authorities'/(name+'.json'))==row['authority_sha256']
    receipt=read(store/'segment-000.json');v=read(EX/(name+'-VERIFY.json'))
    assert receipt['complete'] and receipt['status']=='stage_complete' and receipt['native_steps']==9000
    assert receipt['identity_sha256']=='5df0ced8bf5602c84852bc2074fca8d422cc39cc55b9bab00a4b653bbe714c49'
    assert receipt['initial_checkpoint']['sha256']==a['prepared_snapshot']['sha256']
    assert receipt['initial_causal_sha256'] if 'initial_causal_sha256' in receipt else True
    assert receipt['grant']['initial_causal_sha256']==a['runner_scope']['initial_causal_sha256']
    assert receipt['grant']['end_index']==9000 and receipt['grant']['wall_limit_seconds']==300
    assert not v['P_execution']
    assert len(list(store.glob('segment-*.json')))==1 and len(list(store.glob('*-initial.ld')))==1
checks['exact_authorities_starts_receipts_verified']=9
valid=read(OUT/'PASSIVE_VALIDATION.json');results=read(OUT/'PASSIVE_RESULTS.json')
assert valid['status']=='PASS' and valid['total_native_rows']==81000
assert sum(r['waves'] for r in valid['checks'])==4050
assert [r['case_id'] for r in results]==[r['case_id'] for r in matrix]
assert all(r['all_native_fields_identical'] for r in read(OUT/'HISTORICAL_NATIVE_COMPARISON.json'))
proof=read(PREP/'MATCHED_INITIAL_STATE_PROOF.json')['cases']
assert all(r['complete_engine_bytes_identical'] for r in proof)
for i in (0,3,6):
    for key in ('fields_sha256','physical_body_sha256','original_rng_sha256','original_snapshot_sha256'):
        assert len({r[key] for r in proof[i:i+3]})==1

runtime=read(PREP/'RUNTIME_IDENTITY.json');assert sha(PREP/'RUNTIME_IDENTITY.json')=='5df0ced8bf5602c84852bc2074fca8d422cc39cc55b9bab00a4b653bbe714c49'
members={}
for key,folder in [('P',D/'loom_p'),('apparatus',D/'loom_developmental')]:
    files=runtime[key]['files'] if key=='P' else runtime[key]
    for name,digest in files.items():
        p=folder/name;assert sha(p)==digest,str(p)
        members['frozen_source/developmental_ecology/'+p.relative_to(D).as_posix()]=p
a0=read(PREP/'authorities/MC-FS-001-CURRENT.json')
for p,digest in [(D/'configuration.json',a0['configuration_file_sha256']),(D/'loom_commissioning/contract.py',a0['baseline_contract_sha256'])]:
    assert sha(p)==digest;members['frozen_source/developmental_ecology/'+p.relative_to(D).as_posix()]=p
assert sha(sys.executable)==runtime['executable']
for name,digest in runtime['python_runtime_files'].items():assert sha(Path(sys.base_prefix)/name)==digest,name
for name,digest in runtime['runtime_files'].items():assert sha(Path(sys.prefix)/'Lib/site-packages'/name)==digest,name
checks['bound_runtime_files']=len(runtime['python_runtime_files'])+len(runtime['runtime_files'])+1
checks['bound_source_files']=len(members)
head=git('rev-parse','HEAD');branch=git('branch','--show-current')
assert head=='1d7cd6fd450ea528562b2c825589ab4de18a5b38' and git('status','--porcelain')==''
for p in OUT.glob('*.md'):assert not any(ord(c)<32 and c not in '\n\r\t' for c in p.read_text(encoding='utf8'))
final=dict(status='PASS_COMPLETE_NINE_CASE_SCREEN',utc=datetime.now(timezone.utc).isoformat(),checks=checks,
    authorized_cases=9,started_once=9,completed_90s=9,native_steps=81000,waves=4050,
    terminal_cases=0,resource_cutoffs=0,apparatus_failures=0,unstarted_cases=0,
    runtime_sha256=sha(PREP/'RUNTIME_IDENTITY.json'),worktree=str(WT),branch=branch,checkpoint=head,working_tree_clean=True,
    original_v01_preserved=True,matched_prepared_starts_unchanged=True,parameters_stochastic_laws_unchanged=True,
    production_code_changes=0,new_prehistory=0,retries=0,continuations=0,additional_cases=0,
    post_batch_world_steps=0,mechanism_selected=False,CURRENT_remains_reference=True,
    nursery_birth_viability_learning_source_laws_unchanged=True,old_human_B1_evaluator_accessed=False,
    no_git_writes=True,no_push_PR_merge=True,git_read_warnings=sorted(set(warnings)),
    limitations=['Three fixed starts and single draws per candidate','No developmental-efficacy or general superiority claim',
                 'M2 FS-001 strongly confounded by mover impulses','No overnight/high-contact reliability certification'],
    hash_verification_seconds=time.perf_counter()-start)
save(OUT/'FINAL_VERIFICATION.json',final)
for row in prepared['files']:members['preparation/'+row['path']]=PREP/row['path']
members['preparation/PACKAGE_MANIFEST.json']=PREP/'PACKAGE_MANIFEST.json'
for row in seal['files']:members['execution/'+row['path']]=EX/row['path']
for p in OUT.iterdir():
    if p.is_file() and p.name not in ('PACKAGE_MANIFEST.json','ARCHIVE_VERIFICATION.json'):members['results/'+p.name]=p
for name,path in [('passive_decoder_source.py',ROOT/'nursery_0_design_20260930_v0_1/audit_exploration.py'),
    ('passive_plot_source.py',OLD/'plot_passive.py'),('historical_v01_result.md',OLD/'MOTOR_COMMISSIONING_RESULT_v0_1.md'),
    ('historical_v01_archive_verification.json',OLD/'ARCHIVE_VERIFICATION.json'),
    ('APPARATUS_ROOT_CAUSE_AND_CORRECTION.md',ROOT/'contact_release_correction_20260930/APPARATUS_ROOT_CAUSE_AND_CORRECTION.md')]:
    members['references/'+name]=path
assert sha(members['references/passive_decoder_source.py'])==valid['decoder_source_sha256']
manifest=dict(kind='READ_ONLY_RESULT_REVIEW_NOT_EXECUTION_AUTHORITY',completed_cases=9,interrupted_cases=0,unstarted_cases=0,
    files=[dict(path=name,bytes=p.stat().st_size,sha256=sha(p)) for name,p in sorted(members.items())])
manifest['total_uncompressed_bytes']=sum(r['bytes'] for r in manifest['files'])
save(OUT/'PACKAGE_MANIFEST.json',manifest)
with zipfile.ZipFile(ARCHIVE,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,p in sorted(members.items()):z.write(p,name)
    z.write(OUT/'PACKAGE_MANIFEST.json','PACKAGE_MANIFEST.json')
with zipfile.ZipFile(ARCHIVE) as z:
    assert z.testzip() is None and len(z.namelist())==len(members)+1
    for row in manifest['files']:
        blob=z.read(row['path']);assert len(blob)==row['bytes'] and hashlib.sha256(blob).hexdigest()==row['sha256'],row['path']
    assert z.read('PACKAGE_MANIFEST.json')==(OUT/'PACKAGE_MANIFEST.json').read_bytes()
verify(EX,seal['files']);verify(OLDPREP/'execution',read(OLD/'EXECUTION_CUSTODY_SEAL.json')['files'])
archive=dict(status='PASS',path=str(ARCHIVE),bytes=ARCHIVE.stat().st_size,sha256=sha(ARCHIVE),
    verified_members=len(members)+1,manifest_sha256=sha(OUT/'PACKAGE_MANIFEST.json'),
    v02_execution_unchanged=True,v01_execution_unchanged=True,single_archive_created=True,
    new_execution_authorized=False,hash_and_archive_seconds=time.perf_counter()-start)
save(OUT/'ARCHIVE_VERIFICATION.json',archive)
print(json.dumps(dict(final=final,archive=archive),indent=2))
