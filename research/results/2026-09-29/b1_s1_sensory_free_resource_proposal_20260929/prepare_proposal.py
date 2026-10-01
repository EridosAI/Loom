"""Static single-object preparation. Standard library only; no Loom imports.

Reads JSON and hashes/copies existing bytes. Never creates an execution grant,
loads an Engine, calls a controller, evolves/replays a world or writes Git.
"""
from pathlib import Path
import copy
import datetime
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import zipfile

S=Path(__file__).resolve().parent;ROOT=S.parent
R=ROOT/'exports/2026-09-29-B1-minimal-apparatus-a8cdd75'
DEST=ROOT/'exports/2026-09-29-B1-S1-sensory-free-900s-proposal'
W=ROOT/'worktrees/loom-p-b1-minimal-20260929';D=W/'developmental_ecology'
PREVIOUS=ROOT/'b1_minimal_execution_20260929/run-001'
CASE='B1-MINIMAL-S1-SENSORY-FREE'
APP='a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad'
OLD='394dfc775fc1c6dc93820384a79f4fd63291f06ee03bb28f80e464c989861dbc'

def check(ok,why):
    if not ok:raise ValueError(why)
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
def read(p):
    def unique(pairs):
        d={}
        for k,v in pairs:
            check(k not in d,'duplicate JSON key');d[k]=v
        return d
    def nonfinite(x):raise ValueError('nonfinite JSON')
    return json.loads(Path(p).read_bytes(),object_pairs_hook=unique,parse_constant=nonfinite)
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:json.dump(v,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
def text(p,s):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(s)
def cp(src,relative):
    p=DEST/relative;p.parent.mkdir(parents=True,exist_ok=True);check(not p.exists(),'copy destination exists');shutil.copy2(src,p)
def inventory(path):return {p.relative_to(path).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(path.rglob('*')) if p.is_file()}
def diff(a,b,path=''):
    if type(a) is dict and type(b) is dict:
        out=[]
        for k in sorted(set(a)|set(b)):
            if k not in a:out.append({'path':path+'/'+k,'operation':'add','after':b[k]})
            elif k not in b:out.append({'path':path+'/'+k,'operation':'remove','before':a[k]})
            else:out.extend(diff(a[k],b[k],path+'/'+k))
        return out
    if a!=b or type(a) is not type(b):return [{'path':path,'operation':'replace','before':a,'after':b}]
    return []
def git(*args):return subprocess.check_output(['git','-c',f'safe.directory={W.as_posix()}',
    '-c',f'core.excludesFile={ROOT / "a5_regeneration_20260926/empty-excludes"}','-C',str(W),*args],
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),text=True).strip()

check(git('rev-parse','HEAD')==APP and git('status','--porcelain=v1','--untracked-files=all')=='','wrong or dirty checkpoint')
before=inventory(PREVIOUS)
old_dir=R/'cases'/CASE
old=read(old_dir/'AUTHORITY_OBJECT.json')
check(canonical(old)==(old_dir/'AUTHORITY_OBJECT.canonical.json').read_bytes() and digest(canonical(old))==OLD,'original authority mismatch')
old_manifest=read(old_dir/'MANIFEST.json')
check(old_manifest['execution_authority'] is None,'original proposal has grant')
check({k:v for k,v in old_manifest.items() if k!='execution_authority'}==old['execution_object'],'original execution mismatch')
check(old['apparatus_checkpoint']==APP and old['case_id']==CASE and old['reference_arm']=='SENSORY-FREE','wrong original case')
check(old['execution_sha256']==digest(canonical(old['execution_object'])),'original execution hash mismatch')
for name,v in read(R/'SOURCE_IDENTITIES.json')['files'].items():
    check(sha(D/name)==v['sha256'] and (D/name).stat().st_size==v['bytes'],'changed source/configuration: '+name)
for name,expected in old['bound_documents'].items():check(sha(R/name)==expected,'original bound document mismatch: '+name)
check(sha(R/old['initial_snapshot']['file'])==old['initial_snapshot']['sha256'],'initial snapshot bytes mismatch')
snapshot=json.loads(gzip.decompress((R/old['initial_snapshot']['file']).read_bytes()))
state_bytes=json.dumps(snapshot['state'],separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
check(digest(state_bytes)==snapshot['state_sha256']==old['initial_snapshot']['state_sha256'],'packed snapshot state mismatch')
previous=read(PREVIOUS/'EXECUTION_RESULT.json')
check(previous['attempted']==['B1-MINIMAL-S1-FULL'] and CASE in previous['not_attempted'],'case no longer untouched')
check(not (PREVIOUS/'cases'/CASE).exists(),'sensory-free output already exists')
full=read(ROOT/'b1_minimal_execution_20260929/review/B1-MINIMAL-S1-FULL.json')
check(full['initial_state_sha256']==snapshot['state_sha256'],'not the matched FULL initial state')
new=copy.deepcopy(old)
new['execution_object']['execution']['resources']['wall_limit_seconds']=900
new['execution_sha256']=digest(canonical(new['execution_object']))
new['shared_resource_limits']['wall_per_case_seconds']=900
expected_diff=[{'path':'/execution/resources/wall_limit_seconds','operation':'replace','before':600,'after':900}]
check(diff(old['execution_object'],new['execution_object'])==expected_diff,'unexpected execution semantic change')
manifest=copy.deepcopy(old_manifest);manifest['execution']['resources']['wall_limit_seconds']=900
check({k:v for k,v in manifest.items() if k!='execution_authority'}==new['execution_object'],'new manifest mismatch')

DEST.mkdir(exist_ok=False)
for name in old['bound_documents']:cp(R/name,name)
cp(R/old['initial_snapshot']['file'],old['initial_snapshot']['file'])
cp(R/old['start_manifest']['file'],old['start_manifest']['file'])
for source in sorted((R/'instrument').rglob('*')):
    if source.is_file():cp(source,source.relative_to(R))
for source in sorted((R/'verified-cache').rglob('*')):
    if source.is_file():cp(source,source.relative_to(R))
for name in ('AUTHORITY_OBJECT.json','AUTHORITY_OBJECT.canonical.json','MANIFEST.json','EXECUTION_OBJECT.canonical.json'):
    cp(old_dir/name,'provenance/original-S1-SENSORY-FREE/'+name)
cp(S/'JASON_REQUEST.md','JASON_REQUEST.md')
cp(ROOT/'b1_minimal_execution_20260929/review/B1-MINIMAL-S1-FULL.json','provenance/S1-FULL_OBSERVED_RESULT.json')
cp(PREVIOUS/'EXECUTION_RESULT.json','provenance/STOPPED_BATCH_RESULT.json')
cp(Path(__file__),'preparation/prepare_proposal.py')

rates=read(R/'RESOURCE_PROJECTION.json')['rate_source']
full_receipt=read(PREVIOUS/'cases/B1-MINIMAL-S1-FULL/manifest.json')
projection={'case_id':CASE,'maximum_cases':1,'maximum_attempts':1,'simulated_seconds':30,'native_steps':3000,'command_holds':300,
 'wall_seconds_before':600,'wall_seconds_proposed':900,
 'reference_projections_seconds':{k:v*30 for k,v in rates.items()},
 'S1_FULL_observed_wall_seconds':full['wall_seconds'],'S1_FULL_observed_simulated_seconds':full['simulated_seconds'],
 'S1_FULL_scaled_30s_wall_proxy_seconds':full['wall_seconds']/full['simulated_seconds']*30,
 'primary_planning_bytes_unchanged':993906579,'with_one_complete_archival_copy_bytes':2*993906579,
 'S1_FULL_observed_artifact_bytes':full['artifact_bytes'],
 'S1_FULL_scaled_30s_artifact_proxy_bytes':full['artifact_bytes']/full['simulated_seconds']*30,
 'S1_FULL_observed_uncompressed_stream_bytes':full_receipt['uncompressed_bytes'],
 'S1_FULL_scaled_30s_uncompressed_proxy_bytes':full_receipt['uncompressed_bytes']/full['simulated_seconds']*30,
 'stream_cap_bytes_unchanged':1500000000,'combined_new_artifact_cap_bytes_unchanged':20000000000,
 'stop_request_bytes_unchanged':19000000000,'flush_reserve_bytes_unchanged':1000000000,
 'minimum_free_bytes_unchanged':20000000000,'read_only_reporting_seconds_unchanged':1800,
 'free_disk_at_preparation_bytes':shutil.disk_usage(ROOT).free,
 'limitations':['Historical A2/A3/A5 are base-throughput references, not measurements of this sensory-free case.',
 'S1-FULL is a recent apparatus proxy, not an executed sensory-free timing test. Different inputs/contact paths can change cost.',
 '900 seconds is an administrative ceiling, not a completion guarantee. Native-step and flush overshoot remain unchanged.',
 'No historical unused case/batch allowance is available for transfer; no automatic continuation or retry.'],
 'zero_new_simulated_seconds':True,'zero_new_prehistory':True}
write(DEST/'RESOURCE_ADJUSTMENT_PROJECTION.json',projection)
plan='''# Single S1-SENSORY-FREE resource proposal — NOT AUTHORIZED

Prepare exactly one unchanged S1-SENSORY-FREE case at checkpoint a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad. Its complete prepared initial snapshot, SENSORY-FREE no-input (0.30,0.30) law, 30-second ceiling, 3,000 native-step maximum, 300 existing 0.1-second holds, recording, validation, physics and existing prehistory are unchanged.

The sole numerical execution change is administrative wall_limit_seconds 600 -> 900. The outer shared_resource_limits.wall_per_case_seconds mirror is likewise 900. All other inherited resource ceilings are unchanged. For this one-case proposal the effective execution allowance is at most 900 seconds, with the existing native-step/flush overrun behavior. The historical 5,400-second aggregate and nine-case maxima do not provide a new spending pool or authorize another case.

The original shared_batch_order, original RESOURCE_AND_EXECUTION_PLAN.md and RESOURCE_PROJECTION.json are retained as historical provenance. The single_case_resource_amendment in the new object takes precedence for the current launch scope and this 900-second allowance. The nine-case batch remains stopped; the original rule permitting a next independently authorized batch case is inactive here. Stop after this one case on its normal horizon, terminal, apparatus/controller failure or administrative/resource cutoff. No retry, continuation, substitution, tuning, extra case or new prehistory.

Before any separately authorized future launch, perform the unchanged full-runtime preflight again: exact new authority, checkpoint/source/runtime, unchanged snapshot and cache identities, state matching, grant, unused output, per-case/global storage and free-disk checks. Generate no new prehistory. No execution grant or runner is supplied in this proposal. The old 600-second grant cannot authorize this changed execution object.

Retain 1,500,000,000 bytes per-case uncompressed stream cap; 20,000,000,000 bytes for combined new artifacts including existing preparation/execution records and all copies; stop requesting work at 19,000,000,000 bytes; preserve 1,000,000,000-byte flush reserve and at least 20,000,000,000 free bytes before launch. Retain the 1,800-second read-only reporting ceiling and existing full-fidelity records. At each hold a future supervisor must check shared storage; the existing runner owns the unchanged stop rules and the new 900-second wall limit. No physical replay is authorized as reporting.

Use RESOURCE_ADJUSTMENT_PROJECTION.json for updated estimates: approximately 10.09 minutes from the recent partial S1-FULL wall-rate proxy, with older A2/A3 base estimates near 5.88-5.97 minutes. These are estimates, not a sensory-free execution. The unchanged conservative storage allowance is 993,906,579 bytes primary or 1,987,813,158 bytes including one archive copy. No evidence-fidelity reduction is proposed.

Jason now accepts the preserved S1-FULL result as the productive FULL witness. Record this as Jason's later decision, without rewriting its administrative-cutoff receipt or the earlier report. The outstanding proposed comparison is only this matched sensory-free case. No new outcome exists; no B1 closure is declared by packet preparation.

S1-FULL must not be continued or retried. S1-HIDDEN, S2 and S3 must not be prepared or executed under this object. No old sealed human B1 evaluator state may be inspected. Stop for Jason's authorization of the new outer authority hash.
'''
text(DEST/'SINGLE_CASE_RESOURCE_PLAN.md',plan)
new['single_case_resource_amendment']={
 'original_authority_sha256':OLD,'original_execution_sha256':old['execution_sha256'],
 'new_authorization_required':True,'execution_order':[CASE],'maximum_attempts':1,
 'only_execution_parameter_change':expected_diff[0],
 'precedence':'This amendment and SINGLE_CASE_RESOURCE_PLAN.md govern this proposal. Original shared_batch_order, batch maxima and original resource documents are historical context, not an active schedule or transferable allowance. The sole resource value increased is this case wall allowance, mirrored in shared_resource_limits.',
 'prior_nine_case_batch_remains_stopped':True,
 'original_rule_allowing_a_next_separately_authorized_batch_case_is_inactive':True,
 'after_any_stop':'Stop. No automatic next case, retry or continuation.',
 'S1_FULL':'Preserve as accepted productive FULL witness; never continue or retry.',
 'other_cases':'No S1-HIDDEN, S2 or S3 preparation/execution authorized by this object.',
 'old_sealed_human_B1_state_access':'prohibited'}
for name in ('JASON_REQUEST.md','SINGLE_CASE_RESOURCE_PLAN.md','RESOURCE_ADJUSTMENT_PROJECTION.json'):
    new['bound_documents'][name]=sha(DEST/name)
case_dir=DEST/'cases'/CASE
write(case_dir/'MANIFEST.json',manifest)
write(case_dir/'AUTHORITY_OBJECT.json',new)
(case_dir/'AUTHORITY_OBJECT.canonical.json').write_bytes(canonical(new))
(case_dir/'EXECUTION_OBJECT.canonical.json').write_bytes(canonical(new['execution_object']))
new_hash=digest(canonical(new))
write(DEST/'AUTHORITY_INDEX.json',{'status':'ONE PROPOSAL / NOT AUTHORIZED / ZERO EXECUTION GRANTS',
 'case_order':[CASE],'authority_sha256':new_hash,'execution_sha256':new['execution_sha256'],
 'authority_file':f'cases/{CASE}/AUTHORITY_OBJECT.canonical.json','original_authority_sha256':OLD})
wrapper_diff=diff(old,new)
write(DEST/'SEMANTIC_DIFF.json',{'old_authority_sha256':OLD,'new_authority_sha256':new_hash,
 'execution_changes':expected_diff,'complete_outer_object_diff':wrapper_diff,
 'unexpected_execution_changes':[],'same_snapshot_bytes':True,'same_checkpoint':True,
 'wrapper_explanation':'Derived execution hash changes; administrative mirror 600->900; newly bound preparation/resource documents and single-case scope restriction. Original batch fields retained explicitly as history only.'})
text(DEST/'SEMANTIC_DIFF.md',f'''# Semantic diff — original S1-SENSORY-FREE to 900-second proposal

Original outer authority: `{OLD}`.
New outer authority: `{new_hash}`.

The complete recursive diff of the executable object is exactly one leaf:

| Path within execution object | Before | After |
|---|---:|---:|
| `/execution/resources/wall_limit_seconds` | 600 | 900 |

There are no other executable-field additions, deletions, value changes or type changes. The proposed manifest retains `execution_authority: null`. The 30-second physical ceiling and the existing (0.30,0.30) sensory-free law are unchanged.

The complete outer-object diff is separately retained in `SEMANTIC_DIFF.json`: the execution SHA changes as a consequence; the mirrored per-case wall allowance changes from 600 to 900; a single-case amendment explicitly prevents batch restart or any next case; and three new documentation hashes bind Jason's instruction, that scope restriction and the resource estimate. These are authority/provenance bookkeeping for the requested isolated case, not additional controller/world/start/recording/validation changes. We do not claim that the entire wrapper differs at only one JSON path.

The original nine-case order and resource documents remain unchanged historical context and are explicitly inactive as a launch schedule. No previous 600-second grant is reused. Only the new outer hash may be authorized for this proposed execution.

Initial compressed snapshot SHA-256: `{new['initial_snapshot']['sha256']}`.
Complete initial-state SHA-256: `{new['initial_snapshot']['state_sha256']}`.
Checkpoint: `{APP}`.

All initial-state and start-manifest bytes, P/world/controller/runtime/configuration bindings, simulated horizon, native/wave/field cadence, stop/validation/recording implementation and prehistory identity are preserved. No production files were changed. No new simulation or controller inference occurred.
''')
check(before==inventory(PREVIOUS),'previous execution evidence changed')
check(git('rev-parse','HEAD')==APP and git('status','--porcelain=v1','--untracked-files=all')=='','checkpoint changed during preparation')
check(sorted(p.name for p in (DEST/'cases').iterdir())==[CASE],'more than one new case')
check(sha(case_dir/'INITIAL.snapshot.json.gz')==old['initial_snapshot']['sha256'],'copied snapshot mismatch')
write(DEST/'STATIC_VERIFICATION.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'checkpoint':APP,'git_status':'clean','original_authority_verified':OLD,'new_authority_sha256':new_hash,
 'execution_diff_exactly_one_leaf':True,'only_numerical_execution_change':'wall_limit_seconds: 600 -> 900',
 'prepared_cases':[CASE],'execution_grants_created':0,'new_simulated_seconds':0,'new_native_steps':0,
 'new_controller_decisions':0,'world_or_Engine_instantiations':0,'new_prehistory_steps':0,'physical_replays':0,
 'method':'Standard-library JSON/gzip inspection, byte copying, scalar estimates, recursive JSON diff and SHA-256 verification only; no Loom runtime import.',
 'original_initial_state_matches_preserved_FULL':True,'previous_run_file_inventory_unchanged':True,
 'old_sealed_human_B1_state_accessed':False,'full_runtime_preflight_required_again_before_future_authorized_launch':True})
text(DEST/'README.md',f'''# S1-SENSORY-FREE — single resource-adjusted proposal

**NOT EXECUTED. Awaiting Jason's authorization.**

Authorize only this new canonical outer authority if approved:

`{new_hash}`

Case: `{CASE}`. Checkpoint: `{APP}`. Exact prepared S1 snapshot and no-input `(0.30,0.30)` controller; unchanged 30-second physical ceiling. Only executable change: wall allowance 600 -> **900 seconds**. No batch restart, FULL continuation/retry, HIDDEN, S2 or S3.

Read [semantic diff](SEMANTIC_DIFF.md), [single-case resource plan](SINGLE_CASE_RESOURCE_PLAN.md), [resource estimate](RESOURCE_ADJUSTMENT_PROJECTION.json) and [static verification](STATIC_VERIFICATION.json). The recent S1-FULL wall-rate proxy projects {projection['S1_FULL_scaled_30s_wall_proxy_seconds']/60:.2f} minutes; the proposed cap is 15 minutes. Retain the existing conservative 0.994 GB primary / 1.988 GB with one archival copy storage estimate and all existing recording fidelity.

Jason's acceptance of S1-FULL as the productive witness is recorded in `JASON_REQUEST.md`; previous observations and their cutoff remain unchanged. This preparation grants no execution and declares no new comparison outcome.

Only `cases/{CASE}/AUTHORITY_OBJECT.canonical.json` is the new proposal. Files under `provenance/` and the retained old resource documents are historical references. The explicit single-case amendment controls current scope. No approval envelope or runner invocation is included. Stop for Jason's authorization.
''')
write(DEST/'FILE_MANIFEST.json',{'files':inventory(DEST),'excludes':['FILE_MANIFEST.json (self)']})
archive=DEST.with_suffix('.zip')
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(DEST.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(DEST).as_posix())
with zipfile.ZipFile(archive) as z:
    check(z.testzip() is None,'archive CRC failure')
    for name,expected in read(DEST/'FILE_MANIFEST.json')['files'].items():
        data=z.read(name);check(digest(data)==expected['sha256'] and len(data)==expected['bytes'],'archive file mismatch')
write(S/'DELIVERY.json',{'authority_sha256':new_hash,'execution_sha256':new['execution_sha256'],
 'packet':str(DEST),'archive':str(archive),'archive_sha256':sha(archive),'archive_bytes':archive.stat().st_size,
 'archive_verified':True,'new_simulated_seconds':0,'new_controller_decisions':0})
print(json.dumps(read(S/'DELIVERY.json'),indent=2))
