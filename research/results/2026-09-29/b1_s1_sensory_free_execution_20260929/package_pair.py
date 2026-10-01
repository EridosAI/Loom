"""Preserve and package the completed single case; no simulator/controller calls."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,zipfile
S=Path(__file__).resolve().parent;ROOT=S.parent;PRIOR=ROOT/'b1_minimal_execution_20260929'
W=ROOT/'worktrees/loom-p-b1-minimal-20260929';D=W/'developmental_ecology'
R=ROOT/'exports/2026-09-29-B1-S1-sensory-free-900s-proposal'
DEST=ROOT/'exports/2026-09-29-B1-S1-paired-closure-a8cdd75';Z=DEST.with_suffix('.zip')
COMPANION=ROOT/'exports/2026-09-29-B1-minimal-closure-results-a8cdd75.zip'
COMPANION_SHA='6f81433c1102a3d008be9a7243951213c0396b805e6a5674f7ee89212df8fd66'
APP='a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad';CASE='B1-MINIMAL-S1-SENSORY-FREE'
def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def check(ok,why):
    if not ok:raise ValueError(why)
def write(p,v):
    with Path(p).open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
def inventory(p):return {x.relative_to(p).as_posix():{'sha256':sha(x),'bytes':x.stat().st_size} for x in sorted(p.rglob('*')) if x.is_file()}
def size(p):return p.stat().st_size if p.is_file() else sum(x.stat().st_size for x in p.rglob('*') if x.is_file()) if p.exists() else 0
pre=read(S/'run-001/PREFLIGHT.json');COUNT=[Path(p) for p in pre['counted_roots']]
start=datetime.datetime.fromisoformat(read(S/'review/REVIEW_START.json')['utc'])
def budget():
    check((datetime.datetime.now(datetime.timezone.utc)-start).total_seconds()<1800,'reporting deadline')
    total=sum(size(p) for p in COUNT);check(total<19000000000,'storage stop threshold');return total
budget();execution=read(S/'run-001/EXECUTION_RESULT.json')
check(execution['attempts']==1 and execution['only_case']==CASE,'wrong execution count/scope')
check([p.name for p in (S/'run-001/cases').iterdir()]==[CASE],'extra output case')
preserved=read(S/'run-001/PRESERVED_FULL_AND_PRIOR_INVENTORY.json')
check(inventory(PRIOR)==preserved,'prior FULL/first-batch evidence changed')
check(sha(COMPANION)==COMPANION_SHA,'existing FULL companion archive changed')
for rel,v in read(R/'FILE_MANIFEST.json')['files'].items():check(sha(R/rel)==v['sha256'],'prepared proposal changed: '+rel)
for rel,v in read(R/'SOURCE_IDENTITIES.json')['files'].items():check(sha(D/rel)==v['sha256'],'runtime source changed: '+rel)
claim=read(S/'run-001/ONE_ATTEMPT_CLAIM.json')
check(sha(S/'execute_once.py')==claim['supervisor_sha256'],'execution wrapper changed after start')
check(sha(S/'USER_AUTHORIZATION.md')==claim['authorization_sha256'],'authorization record changed')
check(sha(S/'review_pair.py')==read(S/'review/REVIEW_START.json')['script_sha256'],'reviewer changed after use')
def git(*args):return subprocess.check_output(['git','-c',f'safe.directory={W.as_posix()}',
 '-c',f'core.excludesFile={ROOT / "a5_regeneration_20260926/empty-excludes"}','-C',str(W),*args],
 env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),text=True).strip()
check(git('rev-parse','HEAD')==APP and git('status','--porcelain=v1','--untracked-files=all')=='','wrong/dirty checkpoint')
write(S/'review/POSTFLIGHT_IDENTITY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'checkpoint':APP,'git_status':'clean','branch':git('branch','--show-current'),
 'proposal_and_runtime_source_bytes_unchanged':True,'prior_FULL_and_first_batch_file_inventory_unchanged':True,
 'FULL_companion_archive_sha256_verified':COMPANION_SHA,'single_new_case_only':CASE,
 'execution_wrapper_authorization_reviewer_unchanged':True,'old_sealed_human_B1_accessed':False})
shutil.copy2(PRIOR/'review_saved_records.py',S/'review/REUSED_SAVED_RECORD_AUDITOR.py')
write(S/'review/FULL_COMPANION.json',{'archive_name':COMPANION.name,'archive_path':str(COMPANION),
 'archive_sha256':COMPANION_SHA,'primary_directory':str(PRIOR/'run-001/cases/B1-MINIMAL-S1-FULL'),
 'reason_not_recopied':'Preserve existing complete archive; do not create another full trajectory duplicate.',
 'receipt_sha256':'84fc5325b49ccf047c5b4c8699127bee26eb7caf79b25741928fea3be06aea27'})
DEST.mkdir(exist_ok=False)
for name in ('B1_MINIMAL_CLOSURE_REPORT.md','PAIRED_CLOSURE_RESULTS.json','FULL_COMPANION.json'):
    shutil.copy2(S/'review'/name,DEST/name)
intro='''# B1 S1 matched closure — finished and stopped

**The existing B1 minimal-closure rule is satisfied for this S1 pair.**

Read [the bounded report](execution/review/B1_MINIMAL_CLOSURE_REPORT.md) and [machine-readable comparison](execution/review/PAIRED_CLOSURE_RESULTS.json).

S1-SENSORY-FREE ran once for 30 simulated seconds, 3,000 native steps and 300 fixed (0.30,0.30) commands, with no controller input and zero recorded source transfer. The accepted preserved S1-FULL witness recorded productive source interaction and active permitted feedback from the exact same complete initial state. FULL remains at its original 29.79-second wall cutoff.

`execution/run-001/` contains all new physical records, snapshots, authority grant, preflight, attempt and completion records. `prepared-proposal/` contains the unchanged single-case authority, start, source/configuration/runtime bindings and resource plan. `execution/review/` contains accounting, input/hold verification, command trace, paired results and the FULL preservation inventory. FILE_MANIFEST.json binds all archived files.

The FULL raw trajectory remains in the existing companion archive named in `execution/review/FULL_COMPANION.json`; retain both archives for a complete portable paired review. No new FULL trajectory duplicate was made. Original host paths in grants/cache provenance are retained as evidence.

No retry, continuation, next case, batch restart, chemistry-hidden case, S2/S3, Founder Search, C1/C2 or nursery work is authorized by this archive. No old sealed human B1 material is included. No world replay was performed. P and the Base World were unchanged. The result is a bounded external-controller access witness, not evidence of P learning or broad competence.
'''
(DEST/'README.md').write_text(intro,encoding='utf-8')
members=[('README.md',DEST/'README.md')]
for prefix,directory in [('execution',S),('prepared-proposal',R)]:
    members.extend((prefix+'/'+p.relative_to(directory).as_posix(),p) for p in sorted(directory.rglob('*')) if p.is_file())
manifest={'files':{name:{'sha256':sha(p),'bytes':p.stat().st_size} for name,p in members},
 'excludes':['FILE_MANIFEST.json (self)','external DELIVERY_VERIFICATION.json and ARCHIVE.sha256 (created after ZIP verification)'],
 'checkpoint':APP,'FULL_companion_archive_sha256':COMPANION_SHA,'new_cases':1,'physical_replays':0}
write(DEST/'FILE_MANIFEST.json',manifest)
with zipfile.ZipFile(Z,'x',zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
    for name,p in members:budget();z.write(p,name)
    z.write(DEST/'FILE_MANIFEST.json','FILE_MANIFEST.json')
with zipfile.ZipFile(Z) as z:
    check(z.testzip() is None,'ZIP CRC mismatch')
    for name,v in manifest['files'].items():
        b=z.read(name);check(len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],'ZIP content mismatch')
    check(z.read('FILE_MANIFEST.json')==(DEST/'FILE_MANIFEST.json').read_bytes(),'ZIP manifest mismatch')
total=budget()
delivery={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':str(Z),'archive_sha256':sha(Z),
 'archive_bytes':Z.stat().st_size,'archived_files_verified':len(members)+1,'all_archive_hashes_and_CRC_verified':True,
 'combined_counted_bytes_before_this_small_receipt':total,'combined_cap_bytes':20000000000,
 'free_bytes':shutil.disk_usage(ROOT).free,'read_only_review_and_packaging_seconds':(datetime.datetime.now(datetime.timezone.utc)-start).total_seconds(),
 'reporting_limit_seconds':1800,'new_complete_null_trajectory_archival_copies':1,'new_complete_FULL_trajectory_copies':0,
 'execution_process_exited':True,'all_execution_stopped':True,'no_next_case':True}
write(DEST/'DELIVERY_VERIFICATION.json',delivery)
(DEST/'ARCHIVE.sha256').write_text(delivery['archive_sha256']+'  '+Z.name+'\n',encoding='ascii')
budget();print(json.dumps(delivery,indent=2))
