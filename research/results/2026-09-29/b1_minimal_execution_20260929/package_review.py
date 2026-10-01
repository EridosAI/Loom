"""Package existing evidence only; never execute or replay an assay."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import zipfile

S=Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-minimal-20260929';D=W/'developmental_ecology'
R=ROOT/'exports/2026-09-29-B1-minimal-apparatus-a8cdd75'
DEST=ROOT/'exports/2026-09-29-B1-minimal-closure-results-a8cdd75'
Z=DEST.with_suffix('.zip')
APP='a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad'
read=lambda p:json.loads(Path(p).read_text(encoding='utf-8'))
def require(ok,why):
    if not ok:raise RuntimeError(why)
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()
def write(p,data):
    with Path(p).open('x',encoding='utf-8',newline='\n') as f:json.dump(data,f,indent=2,allow_nan=False);f.write('\n')
def size(p):return p.stat().st_size if p.is_file() else sum(x.stat().st_size for x in p.rglob('*') if x.is_file()) if p.exists() else 0
def budget():
    started=dt.datetime.fromisoformat(read(S/'review/REVIEW_START.json')['utc'])
    require((dt.datetime.now(dt.timezone.utc)-started).total_seconds()<1800,'reporting budget reached')
    total=sum(size(p) for p in COUNT)
    require(total<19_000_000_000,'combined storage stop threshold')
    return total
COUNT=[S,ROOT/'b1_minimal_implementation_20260929',ROOT/'b1_minimal_closure_design_20260929',R,R.with_suffix('.zip'),DEST,Z]

budget();execution=read(S/'run-001/EXECUTION_RESULT.json')
require(execution['attempted']==['B1-MINIMAL-S1-FULL'],'unexpected attempt set')
require(execution['batch_stop']['cause']=='wall_time_limit','unexpected batch stop')
require([p.name for p in (S/'run-001/cases').iterdir()]==execution['attempted'],'unexpected output case')
source=read(R/'SOURCE_IDENTITIES.json')['files']
for name,expected in source.items():
    require(sha(D/name)==expected['sha256'] and (D/name).stat().st_size==expected['bytes'],'changed runtime file: '+name)
for name,expected in read(R/'FILE_MANIFEST.json')['files'].items():
    require(sha(R/name)==expected['sha256'] and (R/name).stat().st_size==expected['bytes'],'changed prepared packet: '+name)
claim=read(S/'run-001/ONE_ATTEMPT_CLAIM.json')
require(sha(S/'execute_once.py')==claim['supervisor_sha256'],'supervisor changed after claim')
require(sha(S/'USER_AUTHORIZATION.md')==claim['authorization_sha256'],'authorization record changed')
require(sha(S/'review_saved_records.py')==read(S/'review/REVIEW_START.json')['script_sha256'],'review script changed after use')
def git(*args):return subprocess.check_output(['git','-c',f'safe.directory={W.as_posix()}',
    '-c',f'core.excludesFile={ROOT / "a5_regeneration_20260926/empty-excludes"}','-C',str(W),*args],
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),text=True).strip()
head=git('rev-parse','HEAD');status=git('status','--porcelain=v1','--untracked-files=all')
require(head==APP and status=='','checkpoint no longer clean/exact')
write(S/'review/POSTFLIGHT_IDENTITY.json',{'utc':dt.datetime.now(dt.timezone.utc).isoformat(),
 'checkpoint':head,'git_status':status,'branch':git('branch','--show-current'),'runtime_source_files_verified':len(source),
 'prepared_packet_unchanged':True,'supervisor_and_authorization_unchanged':True,'one_attempt_only':True,
 'remaining_eight_destinations_absent':True,'old_human_B1_material_accessed':False,'world_replays':0})
DEST.mkdir(exist_ok=False)
shutil.copy2(S/'review/B1_MINIMAL_CLOSURE_REPORT.md',DEST/'B1_MINIMAL_CLOSURE_REPORT.md')
shutil.copy2(S/'review/BOUNDED_RESULTS.json',DEST/'BOUNDED_RESULTS.json')
intro='''# B1 minimal closure — preserved administrative cutoff

Full-runtime preflight passed for all nine authorities. S1-FULL ran once, then hit its original 600-second wall limit at 29.79 simulated seconds. The other eight cases were not started. Source contact and positive transfer were recorded, but the required matched null comparison is unavailable: **B1 remains unresolved**.

Read [the bounded report](execution/review/B1_MINIMAL_CLOSURE_REPORT.md) and [machine-readable results](execution/review/BOUNDED_RESULTS.json).

`execution/run-001/` contains the complete partial trajectory, genuine grants, immutable attempt claim, all-case preflight and batch-stop receipt. `prepared-packet/` preserves all nine original objects, starts, accepted design, checkpoint, exact instrument source/configuration/runtime identities and component report. `FILE_MANIFEST.json` verifies every archived input. Original absolute paths in approvals are retained as evidence.

This is a passive review archive. Its scripts and pending final hold do not authorize execution, retry or continuation. No old sealed human B1 evaluator material is included. P and the Base World were unchanged; no physical replay was performed. No subsequent assay or developmental work was started.
'''
(DEST/'README.md').write_text(intro,encoding='utf-8')
members=[('README.md',DEST/'README.md')]
for prefix,directory in [('execution',S),('prepared-packet',R)]:
    members.extend((prefix+'/'+p.relative_to(directory).as_posix(),p) for p in sorted(directory.rglob('*')) if p.is_file())
manifest={'files':{name:{'sha256':sha(p),'bytes':p.stat().st_size} for name,p in members},
 'excludes':['FILE_MANIFEST.json (self)','external DELIVERY_VERIFICATION.json and archive checksum (created after ZIP verification)'],
 'checkpoint':APP,'physical_replays':0,'old_human_B1_material_included':False}
write(DEST/'FILE_MANIFEST.json',manifest)
budget()
with zipfile.ZipFile(Z,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
    for name,p in members:
        budget();z.write(p,name)
    z.write(DEST/'FILE_MANIFEST.json','FILE_MANIFEST.json')
with zipfile.ZipFile(Z) as z:
    require(z.testzip() is None,'archive CRC failure')
    for name,expected in manifest['files'].items():
        h=hashlib.sha256();count=0
        with z.open(name) as f:
            for block in iter(lambda:f.read(1024*1024),b''):h.update(block);count+=len(block)
        require(h.hexdigest()==expected['sha256'] and count==expected['bytes'],'archive content mismatch: '+name)
    require(z.read('FILE_MANIFEST.json')==(DEST/'FILE_MANIFEST.json').read_bytes(),'archive manifest mismatch')
total=budget();archive_sha=sha(Z)
started=dt.datetime.fromisoformat(read(S/'review/REVIEW_START.json')['utc'])
delivery={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'archive':str(Z),'archive_sha256':archive_sha,
 'archive_bytes':Z.stat().st_size,'archived_files_verified':len(members)+1,'CRC_verified':True,
 'every_archived_file_sha256_verified':True,'combined_counted_bytes_before_this_small_receipt':total,
 'combined_cap_bytes':20_000_000_000,'free_bytes':shutil.disk_usage(ROOT).free,
 'read_only_review_and_packaging_elapsed_seconds':(dt.datetime.now(dt.timezone.utc)-started).total_seconds(),
 'reporting_limit_seconds':1800,'complete_trajectory_archival_duplicates':1,
 'execution_process_exited':True,'batch_stopped':True,'no_retry_continuation_or_additional_case':True}
write(DEST/'DELIVERY_VERIFICATION.json',delivery)
(DEST/'ARCHIVE.sha256').write_text(archive_sha+'  '+Z.name+'\n',encoding='ascii')
require(budget()<20_000_000_000,'final artifact cap exceeded')
print(json.dumps(delivery,indent=2))
