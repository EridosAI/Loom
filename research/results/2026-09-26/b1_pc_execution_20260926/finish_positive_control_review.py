"""Verify and package only the five closed, explicitly named PC run records."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import zipfile

S=Path(__file__).resolve().parent
ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926'
D=W/'developmental_ecology'
APP='352f73fffa6d9781eae8aa38e708a9a05669588f'
PACKET=ROOT/'exports/2026-09-26-B1-regenerated-352f73ff/B1_OPERATOR_PACKET'
CASE_AUTHORITIES={
    'PC-LR':'a80a9098b7eed714f824eccd841d17e29e94cc607489ddf7a5390f1dc38c493a',
    'PC-MOTION':'c35d7a469da2598a0bcb0abc9b952592fc5310525fac2f3e1f5edf0461bf401c',
    'PC-CONTACT':'2e9989e37863c32ae89fd559adf51942bd8152b8d5244a8de1baf2234c52ba1d',
    'PC-HOLD':'ac1c5615c2c99ebe2524e3648b81003d7eeb42f1b54493212afd8d3cb83d719f'}
RUN_NAMES=['PC-LR','PC-LR-attempt-002','PC-MOTION','PC-CONTACT','PC-HOLD']

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(p,x):
    with p.open('x',encoding='utf-8') as f:
        json.dump(x,f,indent=2,ensure_ascii=False,allow_nan=False); f.write('\n')

at=datetime.datetime.now(datetime.timezone.utc).isoformat()
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
git=['git','-c','safe.directory='+W.as_posix(),'-c',
     'core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
head=subprocess.check_output(git+['rev-parse','HEAD'],env=env).decode().strip()
branch=subprocess.check_output(git+['branch','--show-current'],env=env).decode().strip()
assert head==APP and subprocess.check_output(git+['status','--porcelain'],env=env)==b''

audits=[]
for run_name in RUN_NAMES:
    r=S/'runs'/run_name; m=read(r/'manifest.json')
    case=m['contract']['case_id']
    assert case in CASE_AUTHORITIES and m['complete']
    assert m['contract']['execution_authority']['approved_execution_sha256']==CASE_AUTHORITIES[case]
    assert m['contract']['baseline']=='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
    for name,item in m['files'].items():
        p=r/name
        assert p.parent.resolve()==r.resolve()
        assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256'], str(p)
    for name,digest in m['code']['files'].items():
        assert sha(D/'loom_p'/name)==digest
    for name,digest in m['contract']['apparatus']['files'].items():
        assert sha(D/'loom_commissioning'/name)==digest
    for name,digest in m['contract']['execution']['procedure']['protocol']['bound_documents'].items():
        assert sha(PACKET/name)==digest
    assert m['records'].get('wave',0)==0 and m['records'].get('scientific_observations',0)==0
    audits.append(dict(run=run_name,case=case,authority_sha256=CASE_AUTHORITIES[case],
        receipt_sha256=sha(r/'manifest.json'),files_verified=len(m['files']),
        stop_cause=m['stop_cause'],simulated_seconds=m['final_time'],wall_seconds=m['wall_seconds'],
        native_steps=m['session_counters']['advanced'],commands=m['records'].get('controller',0),
        compressed_record_bytes=sum(x['bytes'] for x in m['files'].values())))

assert sum(x['native_steps'] for x in audits)==640
assert sum(x['commands'] for x in audits)==64
h=read(S/'PC-HOLD.RESULT.json')
state=read(S/'SEQUENCE_STATE.json')
assert state['live_services']==0 and [x['attempts'] for x in state['cases']]==[2,1,1,1]
audit=dict(recorded_utc=at,scope='Only named closed positive-control records; no B1 archive or evaluator inspection.',
    P='6bc9683b54e4fa80136fe8534d7713e2a250a95f',apparatus=head,worktree=str(W),branch=branch,
    worktree_clean=True,recorded_P_and_apparatus_file_hashes_match_current_source=True,
    bound_public_protocol_hashes_verified=True,runs=audits,
    total_native_steps=640,total_human_commands=64,total_simulated_seconds=6.4,
    live_services=0,additional_world_steps_during_review=0,production_code_changes=0,
    new_authority_objects=0,Git_writes=0,B1_execution=False,B1_evaluator_state_accessed=False,
    gate='NOT SATISFIED: PC-CONTACT remains partial; PC-HOLD one-second target not demonstrated.',
    exposure='Jason self-reported no prior sealed B1 access. Guided positive-control practice and PC-CONTACT post-case replay are explicitly preserved; not an unassisted sequence.')
write_new(S/'FINAL_RECORD_AUDIT.json',audit)

report='''# Loom positive-control execution review — 27 September 2026

All four disclosed controls have ended. Jason chose every submitted motor command. PC-HOLD established a real gentle hold for **0.8 simulated seconds**, shorter than its predeclared continuous **1.0 s** target. The four-control admission gate is **not satisfied**. Neither B1 trial was executed, and no sealed B1 evaluator or starting-state material was inspected or included here.

This is a record of guided human interface practice. It is not a test of P learning, an internal world model, navigation competence or ecological viability.

## Results and stopping conditions

| Control / attempt | Simulated time | Human commands | Stop | Disposition |
|---|---:|---:|---|---|
| PC-LR / 001 | 0 s | 0 | Administrative wall cap after connection loss | No physical execution; original attempt preserved |
| PC-LR / 002 | 0 s | 0 | Jason ended case | DEMONSTRATED with disclosed channel-pair guidance; separately authorized fresh attempt |
| PC-MOTION | 0.2 s | 2 | Administrative wall cap | DEMONSTRATED WITH EXPLICIT GUIDANCE; final interpretation after closure |
| PC-CONTACT | 2.3 s | 23 | Jason ended case | PARTIAL / not marked fully demonstrated; approximate onset detected, support interpretation initially mistaken |
| PC-HOLD | 3.9 s | 39 | Jason ended case | NOT DEMONSTRATED against the full 1.0 s criterion; shorter gentle hold verified |

The total is 640 native steps and 64 human commands across five preserved case preparations, including the separately authorized PC-LR replacement. No other retry, fixture substitution, tuning or extension occurred. The unchanged interface ended wall-limited cases at its next check; their reported wall times were 1222.682 s (PC-LR/001, approximate) and 1241.425 s (PC-MOTION). Neither advanced during the excess wall time. All local control services have been stopped after their cases closed.

## What PC-HOLD actually established

The first impact occurred at **0.233656229 s**. From **0.300 to 1.100 s**, the body had continuous positive-duration wall support. Recorded contact force ranged from **0.037666121 to 0.150862270**, strictly below the unchanged **0.25** stress threshold, with **zero sustained stress damage during that interval**. Thus Jason's interpretation of reducing effort and maintaining a lower contact signal was supported by the completed physical record.

At 1.1 s the command pair changed from `[0.05, 0.05]` to `[1, -1]` as Jason explored. The gentle interval ended. A later qualifying interval lasted **0.282791256 s**, from **2.927208744 to 3.210 s**. Separate intervals cannot be added to satisfy a continuous one-second target. The earlier screenshot showed 0.6 s at the lowest command pair; the physical review finds 0.8 s of qualifying gentle support because the preceding 0.2 and 0.1 pairs were also below the threshold. There is no contradiction between those two durations.

All impacts and later exploration remain in the record: three impact events; total impact damage **0.003453380**, sustained stress damage **0.002796736**, and total damage **0.006250117**. Expenditure was **0.009010**. E/I changed from **0.700000 / 1.000000** to **0.690990 / 0.993750**. Initial impact damage is retained separately and does not invalidate a subsequent gentle interval.

Evaluation used closed event records only: positive impulse over positive duration, actual force equal to impulse/duration, every active contact strictly below the original threshold, and no sustained stress damage. Contiguous event intervals were joined only within the existing `event_time_tol = 1e-10`; no relaxed force threshold or new efficacy criterion was introduced. The force and stress-damage arithmetic and all recorded artifact hashes/lengths were verified.

## Earlier controls and guidance

PC-LR/002: Jason reported “Chemistry 0 is bigger.” The displayed same-type pair was chemistry 0 = 0.5885631339300567 and chemistry 2 = 0.5777453792391184. The assistant identified the pair and anatomy beforehand; Jason supplied the comparison sign. No command or world step was needed. The original zero-step connection-loss attempt is preserved alongside the specifically authorized replacement.

PC-MOTION: Jason distinguished commanded input from achieved forward motion and identified the discrepancy channels as a mismatch. His initial turning-sign error was explicitly corrected. The final interpretation arrived after the wall cutoff using the retained 0.2 s observation. This supports guided understanding, not independent mastery of all signs or an unassisted result.

PC-CONTACT: the actual first impact was at 0.898417740 s; the first native contact sample was 0.900 s. Positive-duration support then persisted to 2.3 s. Jason noticed approximate onset but initially interpreted the later trace as another impact or rough ground. The post-case passive plan-view replay showed sustained wall contact. His uncertainty and later learning remain separate from the original response; this result has not been retroactively upgraded. The replay exposure occurred before PC-HOLD and is recorded as practice feedback.

Jason reported difficulty following what was happening across steps, while still making inferences from the displayed signals. His suggestion that this could support an internal world model is recorded as an operator hypothesis. The interface exposes recorded history, but access to that history did not make it easy for him to follow the motion. No interface change was made during these controls.

## Integrity, limits and next boundary

Jason's prior-B1-exposure answer was **“No”**, preserved as a self-report, not an independently established fact. Disclosed practice geometry, general sensor explanations, the PC-CONTACT post-case replay and the PC-HOLD public timing clarification are retained in the record. The assistant supplied no actuator commands and no live privileged physical-force guidance. Historical preparation records still describe their then-current statuses; this report and `FINAL_RECORD_AUDIT.json` describe the completed sequence.

The gate in the accepted `CONTROL_GATE.json` requires all four controls explicitly demonstrated and separate B1 authorization. PC-CONTACT remains partial and PC-HOLD did not obtain its full duration criterion. No B1 admission is implied by finishing these attempts. Any additional familiarization, retry, interface revision or B1 execution needs a separately scoped decision. No further run is launched.

Not tested: either blinded B1 condition, P learning or perception, formation of an internal world model, survival, commissioning efficacy, alternative routes or control policies. No production code, configuration, authority object, physical law or preserved historical source was changed. No Git write, push, PR or merge occurred.

## Exact identities and evidence

P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`

Apparatus: `352f73fffa6d9781eae8aa38e708a9a05669588f`

Worktree: `WORKTREE_PLACEHOLDER`

Branch: `BRANCH_PLACEHOLDER` (clean at review; no new commit)

| Control | Authorized execution SHA-256 |
|---|---|
AUTHORITIES_PLACEHOLDER

`FINAL_RECORD_AUDIT.json` binds the five runtime receipts and checks their source identities against the unchanged worktree. The portable review archive includes the complete closed PC run records, exact PC requests/manifests/inputs, operator observations, control results and the accepted public control/gate documents. Only these positive-control files were selected; no B1 evaluator archive is present. `REVIEW_FILE_MANIFEST.json` records every archived file hash and size. All analysis was passive; no Engine, Run, controller or world was invoked during this review.
'''
report=report.replace('WORKTREE_PLACEHOLDER',str(W)).replace('BRANCH_PLACEHOLDER',branch)
report=report.replace('AUTHORITIES_PLACEHOLDER','\n'.join('| '+k+' | `'+v+'` |' for k,v in CASE_AUTHORITIES.items()))
with (S/'POSITIVE_CONTROL_EXECUTION_REPORT.md').open('x',encoding='utf-8') as f: f.write(report)

# Explicit PC-only allow-list. Never recurse over the B1 package or private directories.
selected={}
def add(p,name):
    assert p.is_file() and name not in selected
    selected[name]=p
for name in RUN_NAMES:
    for p in sorted((S/'runs'/name).iterdir()):
        if p.is_file(): add(p,'records/'+name+'/'+p.name)
for p in sorted(S.iterdir()):
    if p.is_file() and (p.name.startswith('PC-') or p.name in (
        'OPERATOR_INTEGRITY_RECORD.json','OPERATOR_INTEGRITY_RECORD.before_readiness.json',
        'SEQUENCE_STATE.json','PRELAUNCH_CHECKS.json','FINAL_RECORD_AUDIT.json',
        'POSITIVE_CONTROL_EXECUTION_REPORT.md','review_pc_hold.py','finish_positive_control_review.py')):
        add(p,'review/'+p.name)
for sub in ('PC-LR-attempt-002','PC-CONTACT-REPLAY'):
    for p in sorted((S/sub).iterdir()):
        if p.is_file(): add(p,'review/'+sub+'/'+p.name)
for sub in ('approvals','launch-manifests','inputs'):
    for case in CASE_AUTHORITIES:
        suffix={'approvals':'.request.json','launch-manifests':'.json','inputs':'.snapshot.json.gz'}[sub]
        add(S/sub/(case+suffix),'prepared-PC-inputs/'+sub+'/'+case+suffix)
for name in ('POSITIVE_CONTROL_CARDS.md','CONTROL_GATE.json','DISPLAY_CONTRACT.json',
             'PROTOCOL_CONTRACT.json','RECORDING_CONTRACT.json','PC_AUTHORITY_IDENTITIES.json'):
    add(PACKET/name,'accepted-public-design/'+name)

file_manifest=dict(schema=1,recorded_utc=at,scope='PC-only passive review; not an executable launch authorization',
    files={name:dict(bytes=p.stat().st_size,sha256=sha(p)) for name,p in sorted(selected.items())})
write_new(S/'REVIEW_FILE_MANIFEST.json',file_manifest)
selected['REVIEW_FILE_MANIFEST.json']=S/'REVIEW_FILE_MANIFEST.json'
zip_path=ROOT/'exports/2026-09-27-positive-controls-review.zip'
assert not zip_path.exists()
with zipfile.ZipFile(zip_path,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,p in sorted(selected.items()): z.write(p,name)
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    assert set(z.namelist())==set(selected)
    for name,item in file_manifest['files'].items():
        data=z.read(name)
        assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
assert subprocess.check_output(git+['status','--porcelain'],env=env)==b''
write_new(S/'REVIEW_PACKAGE_RECEIPT.json',dict(path=str(zip_path),bytes=zip_path.stat().st_size,
    sha256=sha(zip_path),file_count=len(selected),all_archived_hashes_verified=True,
    B1_evaluator_material_included=False,additional_simulation_steps=0))
print(json.dumps(dict(report=str(S/'POSITIVE_CONTROL_EXECUTION_REPORT.md'),package=str(zip_path),
    bytes=zip_path.stat().st_size,sha256=sha(zip_path),file_count=len(selected),native_steps=640,
    commands=64,worktree_clean=True,B1_gate_satisfied=False),indent=2))
