"""Read-only result verification and launch bookkeeping; no world evolution."""
import datetime, gzip, hashlib, json, os
from pathlib import Path
import shutil, subprocess, sys

S = Path(__file__).resolve().parent
ROOT = S.parent
W = ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926'
D = W/'developmental_ecology'
APP = '352f73fffa6d9781eae8aa38e708a9a05669588f'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(p, v):
    with p.open('x', encoding='utf-8') as f:
        json.dump(v, f, indent=2, ensure_ascii=False); f.write('\n')

at = datetime.datetime.now(datetime.timezone.utc).isoformat()
run = S/'runs/PC-LR-attempt-002'
r = read(run/'manifest.json')
assert r['complete'] and r['stop_cause'] == 'operator_withdrawal'
assert r['final_time'] == 0 and r['session_counters']['advanced'] == 0
assert r['contract']['initial_state'] == r['final_state']
for name, item in r['files'].items():
    assert sha(run/name) == item['sha256'] and (run/name).stat().st_size == item['bytes']
counts = {}
for name in ('controller', 'native', 'wave', 'sensor', 'operator'):
    with gzip.open(run/(name+'.jsonl.gz'), 'rt', encoding='utf-8') as f:
        counts[name] = sum(bool(line.strip()) for line in f)
assert counts == dict(controller=0, native=0, wave=0, sensor=1, operator=2)
obs = read(S/'PC-LR-attempt-002/PC-LR.OPERATOR_OBSERVATION.json')
display = read(run/'sensor-display.json')
row = display['history'][0]
assert row['raw'][display['raw_labels'].index('chemistry_0')] == obs['exact_chemistry_0']
assert row['raw'][display['raw_labels'].index('chemistry_2')] == obs['exact_chemistry_2']
assert obs['comparison_result'] == 'DEMONSTRATED' and not display['own_commands']

state_path = S/'SEQUENCE_STATE.json'
state = read(state_path)
assert state['cases'][0]['attempts'] == 2
assert all(c['attempts'] == 0 for c in state['cases'][1:])
assert not (S/'runs/PC-MOTION').exists() and not (S/'PC-MOTION.LAUNCH_INTENT.json').exists()
env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
git = ['git','-c','safe.directory='+W.as_posix(),'-c',
       'core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
assert subprocess.check_output(git+['rev-parse','HEAD'],env=env).decode().strip() == APP
assert subprocess.check_output(git+['status','--porcelain'],env=env) == b''
assert shutil.disk_usage(ROOT).free >= 12_000_000_000
plan = read(S/'LAUNCH_PLAN.json')['cases'][1]
assert plan['case'] == 'PC-MOTION'
assert sha(S/'launch-manifests/PC-MOTION.json') == plan['granted_manifest_sha256']
assert sha(S/'inputs/PC-MOTION.snapshot.json.gz') == plan['snapshot_sha256']
assert sha(S/'approvals/PC-MOTION.request.json') == plan['approval_request_sha256']
sys.path.insert(0,str(D))
from loom_commissioning.authority import execution_sha256, validate_execution
from loom_commissioning.contract import authorize_execution
m = read(S/'launch-manifests/PC-MOTION.json')
assert execution_sha256(m) == plan['authority_sha256']
validate_execution(m,complete=True); authorize_execution(m)
for name,value in m['execution']['procedure']['protocol']['bound_documents'].items():
    assert sha(ROOT/'exports/2026-09-26-B1-regenerated-352f73ff/B1_OPERATOR_PACKET'/name) == value

write_new(S/'PC-LR-attempt-002/RESULT.json', dict(case='PC-LR',attempt=2,
    outcome='DEMONSTRATED',recorded_utc=at,observation=obs,
    actual_stop_cause=r['stop_cause'],actual_runtime_status=r['status'],
    closure_context='Jason clicked End this case after the recorded reading check; user confirmed done.',
    simulation_seconds=0,commands=0,native_steps=0,field_updates=0,
    achieved_physical_response='No movement or state change; initial and final complete state identities match.',
    initial_and_final_EI=row['actual_EI'],wall_seconds=r['wall_seconds'],
    record_counts=counts,all_artifact_hashes_and_lengths_verified=True,
    runtime_receipt_sha256=sha(run/'manifest.json'),prior_attempt_retained=True,
    limitations='Disclosed, guided raw-reading comparison; no navigation, P learning, movement or ecological claim.',
    B1_state_accessed=False))
write_new(S/'SEQUENCE_STATE.before_PC-MOTION.json',state)
state.update(status='PC-LR CLOSED AND DEMONSTRATED; PC-MOTION VERIFIED FOR LAUNCH',
             next_case='PC-MOTION',live_services=0,status_observed_utc=at)
state['cases'][0]['status']='ATTEMPT 002 CLOSED / DEMONSTRATED; ATTEMPT 001 ADMINISTRATIVE CUTOFF PRESERVED'
state_path.write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8')
write_new(S/'PC-MOTION.LAUNCH_INTENT.json',dict(case='PC-MOTION',attempt=1,
    authority_sha256=plan['authority_sha256'],apparatus=APP,preflight_utc=at,
    free_disk_bytes=shutil.disk_usage(ROOT).free,source_clean=True,
    identity_and_approval_verified=True,initial_snapshot_hash_verified=True,
    snapshot_not_deserialized_by_preflight=True,invocation_reserved=1,
    service_started=False,simulation_steps=0,B1_state_accessed=False,
    scope='Existing exact PC-MOTION authorization, prepared order, one attempt, no retry or modification.'))
print('PC-LR closure and DEMONSTRATED result preserved. PC-MOTION exact identity verified and one launch reserved. No world loaded by this script.')
