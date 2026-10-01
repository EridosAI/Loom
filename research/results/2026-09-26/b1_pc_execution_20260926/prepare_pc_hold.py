"""Validate the single authorized PC-HOLD launch, without loading/evolving a world."""
import datetime, hashlib, json, os
from pathlib import Path
import shutil, subprocess, sys
S=Path(__file__).resolve().parent; ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926'; D=W/'developmental_ecology'
APP='352f73fffa6d9781eae8aa38e708a9a05669588f'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
state=read(S/'SEQUENCE_STATE.json')
assert state['next_case']=='PC-HOLD'
assert [c['attempts'] for c in state['cases']]==[2,1,1,0]
assert state['live_services']==0
assert not (S/'runs/PC-HOLD').exists() and not (S/'PC-HOLD.LAUNCH_INTENT.json').exists()
previous=read(S/'runs/PC-CONTACT/manifest.json')
assert previous['complete'] and previous['stop_cause']=='operator_withdrawal'
for name,item in previous['files'].items():
    p=S/'runs/PC-CONTACT'/name
    assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes']
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
git=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
assert subprocess.check_output(git+['rev-parse','HEAD'],env=env).decode().strip()==APP
assert subprocess.check_output(git+['status','--porcelain'],env=env)==b''
assert shutil.disk_usage(ROOT).free>=12_000_000_000
plan=read(S/'LAUNCH_PLAN.json')['cases'][3]; assert plan['case']=='PC-HOLD'
assert sha(S/'launch-manifests/PC-HOLD.json')==plan['granted_manifest_sha256']
assert sha(S/'inputs/PC-HOLD.snapshot.json.gz')==plan['snapshot_sha256']
assert sha(S/'approvals/PC-HOLD.request.json')==plan['approval_request_sha256']
sys.path.insert(0,str(D))
from loom_commissioning.authority import execution_sha256,validate_execution
from loom_commissioning.contract import authorize_execution
m=read(S/'launch-manifests/PC-HOLD.json')
assert execution_sha256(m)==plan['authority_sha256']
validate_execution(m,complete=True);authorize_execution(m)
for name,value in m['execution']['procedure']['protocol']['bound_documents'].items():
    assert sha(ROOT/'exports/2026-09-26-B1-regenerated-352f73ff/B1_OPERATOR_PACKET'/name)==value
intent=dict(case='PC-HOLD',attempt=1,authority_sha256=plan['authority_sha256'],apparatus=APP,
    preflight_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),readiness_verbatim='Ok go.',
    free_disk_bytes=shutil.disk_usage(ROOT).free,source_clean=True,identity_and_approval_verified=True,
    initial_snapshot_hash_verified=True,invocation_reserved=1,service_started=False,
    simulation_steps=0,snapshot_not_deserialized_by_preflight=True,B1_state_accessed=False,
    prior_practice_feedback='Jason has seen the disclosed PC-CONTACT passive physical replay and explanations. Preserve this training exposure; do not claim an unassisted sequence.',
    preceding_control_limit='PC-CONTACT remains documented as partial/not fully demonstrated. This does not block the already authorized fourth practice control, but the B1 demonstration gate is not satisfied.',
    scope='One unchanged predetermined PC-HOLD; original 10 s and 1200 wall-second limits. No retry, controller choice, tuning, interface change or B1 execution.')
with (S/'PC-HOLD.LAUNCH_INTENT.json').open('x',encoding='utf-8') as f:json.dump(intent,f,indent=2,ensure_ascii=False);f.write('\n')
print('PC-HOLD identity, original grant, source and resources verified. Exactly one launch reserved. No world loaded or evolved.')
