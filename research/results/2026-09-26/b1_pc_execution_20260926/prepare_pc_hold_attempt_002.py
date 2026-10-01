"""Record one newly authorized, unchanged PC-HOLD attempt; no world loading."""
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

S=Path(__file__).resolve().parent
ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926'
D=W/'developmental_ecology'
APP='352f73fffa6d9781eae8aa38e708a9a05669588f'
A=S/'PC-HOLD-attempt-002'
RUN=S/'runs/PC-HOLD-attempt-002'

def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(p,obj):
    with p.open('x',encoding='utf-8') as f:
        json.dump(obj,f,indent=2,ensure_ascii=False,allow_nan=False); f.write('\n')

assert not A.exists() and not RUN.exists(), 'Attempt already reserved; do not repeat.'
state=read(S/'SEQUENCE_STATE.json')
assert [c['attempts'] for c in state['cases']]==[2,1,1,1]
assert state['live_services']==0
prior=read(S/'runs/PC-HOLD/manifest.json')
assert prior['complete'] and prior['stop_cause']=='operator_withdrawal'
assert prior['session_counters']['advanced']==390
for name,item in prior['files'].items():
    p=S/'runs/PC-HOLD'/name
    assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes']
review_receipt=read(S/'REVIEW_PACKAGE_RECEIPT.json')
assert sha(Path(review_receipt['path']))==review_receipt['sha256']

env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
git=['git','-c','safe.directory='+W.as_posix(),'-c',
     'core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
assert subprocess.check_output(git+['rev-parse','HEAD'],env=env).decode().strip()==APP
assert subprocess.check_output(git+['status','--porcelain'],env=env)==b''
assert shutil.disk_usage(ROOT).free>=12_000_000_000

original=read(S/'LAUNCH_PLAN.json')['cases'][3]
assert original['case']=='PC-HOLD'
manifest_path=S/'launch-manifests/PC-HOLD.json'
snapshot=S/'inputs/PC-HOLD.snapshot.json.gz'
assert sha(manifest_path)==original['granted_manifest_sha256']
assert sha(snapshot)==original['snapshot_sha256']
assert sha(S/'approvals/PC-HOLD.request.json')==original['approval_request_sha256']
sys.path.insert(0,str(D))
from loom_commissioning.authority import execution_object, execution_sha256, validate_execution
from loom_commissioning.contract import authorize_execution
m=read(manifest_path)
assert execution_sha256(m)==original['authority_sha256']
validate_execution(m,complete=True)
authorize_execution(m)
for name,digest in m['execution']['procedure']['protocol']['bound_documents'].items():
    assert sha(ROOT/'exports/2026-09-26-B1-regenerated-352f73ff/B1_OPERATOR_PACKET'/name)==digest

verbatim='Wait is it unmet because I only went to 0.8s?\nRerun it if you like.'
notice=('Jason wrote: '+verbatim+'\n'
    'In context this separately authorizes one fresh PC-HOLD attempt (002), with the same '
    'fixture, complete initial state, interface and original limits, after reviewing attempt 001. '
    'The assistant elects to prepare this one human-operated attempt. This is not permission '
    'for assistant-selected motor commands. Retain the identical canonical execution object, '
    '10 simulated-second ceiling, 1200 wall-second limit, 256000000-byte stream limit and '
    'original one-second continuous gentle-support criterion. Preserve all previous attempts '
    'and the completed review package. Do not claim an unassisted or naive attempt: Jason has '
    'seen practice feedback and the closed first PC-HOLD physical review. No further retry, '
    'PC-CONTACT rerun, tuning, substitution, code/interface change, B1 execution or sealed '
    'B1 inspection is authorized by this grant.')
A.mkdir()
request=A/'approval.request.json'
write_new(request,dict(notice=notice,approved_execution_sha256=execution_sha256(m),
    approved_execution=execution_object(m)))
fresh=copy.deepcopy(m)
fresh['execution_authority']['request_path']=str(request)
fresh['execution_authority']['request_sha256']=sha(request)
assert execution_object(fresh)==execution_object(m)
authorize_execution(fresh)
write_new(A/'launch-manifest.json',fresh)
command=copy.deepcopy(original['command'])
command[command.index('--manifest')+1]=str(A/'launch-manifest.json')
command[command.index('--output')+1]=str(RUN)
write_new(A/'LAUNCH_PLAN.json',dict(case='PC-HOLD',attempt=2,command=command,
    cwd=str(D),environment=original['environment'],automatic_commands=False,
    maximum_invocations=1,authority_sha256=execution_sha256(fresh)))
write_new(A/'SEQUENCE_STATE.before_launch.json',state)
write_new(A/'LAUNCH_INTENT.json',dict(case='PC-HOLD',attempt=2,apparatus=APP,
    recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    user_authorization_verbatim=verbatim,grant_scope=notice,
    authority_sha256=execution_sha256(fresh),same_execution_object=True,
    snapshot_sha256=sha(snapshot),granted_manifest_sha256=sha(A/'launch-manifest.json'),
    request_sha256=sha(request),source_clean=True,
    prior_attempt_receipt_sha256=sha(S/'runs/PC-HOLD/manifest.json'),
    prior_artifact_hashes_verified=True,prior_review_package_sha256=review_receipt['sha256'],
    free_disk_bytes=shutil.disk_usage(ROOT).free,invocation_reserved=1,
    service_started_by_this_script=False,snapshot_deserialized_by_this_script=False,
    simulation_steps=0,B1_state_accessed=False,
    gate_status='PC-CONTACT remains partial; a PC-HOLD repeat does not by itself clear the B1 gate.'))
print('One fresh PC-HOLD attempt 002 authorized and reserved. Exact execution identity and prior evidence verified. No world loaded or evolved.')
