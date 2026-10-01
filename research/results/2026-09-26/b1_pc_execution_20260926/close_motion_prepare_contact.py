"""Verify preserved PC-MOTION evidence and reserve the authorized PC-CONTACT launch."""
import datetime, gzip, hashlib, json, math, os
from pathlib import Path
import shutil, subprocess, sys
S=Path(__file__).resolve().parent; ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926'; D=W/'developmental_ecology'
APP='352f73fffa6d9781eae8aa38e708a9a05669588f'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with gzip.open(p,'rt',encoding='utf-8') as f: return [json.loads(x) for x in f if x.strip()]
def write_new(p,x):
    with p.open('x',encoding='utf-8') as f: json.dump(x,f,indent=2,ensure_ascii=False); f.write('\n')
at=datetime.datetime.now(datetime.timezone.utc).isoformat()
run=S/'runs/PC-MOTION'; r=read(run/'manifest.json')
assert r['complete'] and r['stop_cause']=='wall_time_limit'
for name,item in r['files'].items():
    assert sha(run/name)==item['sha256'] and (run/name).stat().st_size==item['bytes']
n=rows(run/'native.jsonl.gz'); events=rows(run/'events.jsonl.gz'); commands=rows(run/'controller.jsonl.gz')
assert len(n)==20 and len(commands)==2 and r['session_counters']['advanced']==20
assert [c['command'] for c in commands]==[[.7,0],[.4,.8]]
assert [x['native_index'] for x in n]==list(range(1,21))
last=n[-1]; first_pos=[6.,5.]
angle=last['angle']; vx,vy=last['velocity']
vf=vx*math.cos(angle)+vy*math.sin(angle)
vl=-vx*math.sin(angle)+vy*math.cos(angle)
raw=last['raw'][3]; u=last['commands']; omega=last['omega']
expected=[u[0],u[1],math.tanh(vf),math.tanh(vl),math.tanh(omega/1.75),
          math.tanh(u[0]-(vf-.35*omega)),math.tanh(u[1]-(vf+.35*omega))]
assert max(abs(a-b) for a,b in zip(raw,expected))<1e-12
result=dict(case='PC-MOTION',attempt=1,outcome='DEMONSTRATED WITH EXPLICIT GUIDANCE',recorded_utc=at,
    user_final_statement_verbatim='I think 5 and 6 represent a mismatch. So something like slipping wheels. Or dragging on one side.',
    assessment='Jason correctly identified command channels 0/1, forward sign, turning modality and the discrepancy/mismatch concept. Turning direction initially inverted and corrected by assistant. Examples of slipping/drag are hypotheses, not established causes.',
    assistance='Assistant supplied the anatomy map, explained bounded motion and discrepancy transformations, corrected negative turning sign to right/clockwise, and explained that discrepancy does not uniquely identify a cause. Do not label the result unassisted.',
    timing_qualification='Final conceptual explanation was received after the administrative wall cutoff, using the preserved 0.2 s observation. No further world advancement occurred.',
    interpretation='Disclosed guided operator/interface familiarization only; independent turning-sign mastery, navigation and P learning not demonstrated.',
    actual_stop_cause=r['stop_cause'],actual_runtime_status=r['status'],wall_seconds=r['wall_seconds'],
    simulation_seconds=r['final_time'],native_steps=len(n),commands=[dict(time=c['time'],pair=c['command']) for c in commands],
    initial_position=first_pos,final_position=last['position'],final_orientation=angle,
    final_velocity_world=last['velocity'],final_forward_speed=vf,final_lateral_speed=vl,final_turning_rate=omega,
    final_proprioception=raw,transduction_matches_existing_source=True,
    starting_EI=[.7,1.],final_EI=last['reserves'],expenditure=sum(e['expenditure'] for e in events),
    damage=sum(e['damage'] for e in events),contact_records=sum(len(e['contacts']) for e in events),
    record_counts=r['records'],all_artifact_hashes_and_lengths_verified=True,
    runtime_receipt_sha256=sha(run/'manifest.json'),apparatus=APP,
    assistant_actuator_commands=0,retry_or_continuation=False,B1_state_accessed=False)
assert result['damage']==0 and result['contact_records']==0

state_path=S/'SEQUENCE_STATE.json'; state=read(state_path)
assert state['cases'][0]['attempts']==2 and state['cases'][1]['attempts']==1
assert all(c['attempts']==0 for c in state['cases'][2:])
assert not (S/'runs/PC-CONTACT').exists() and not (S/'PC-CONTACT.LAUNCH_INTENT.json').exists()
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
git=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
assert subprocess.check_output(git+['rev-parse','HEAD'],env=env).decode().strip()==APP
assert subprocess.check_output(git+['status','--porcelain'],env=env)==b''
assert shutil.disk_usage(ROOT).free>=12_000_000_000
plan=read(S/'LAUNCH_PLAN.json')['cases'][2]; assert plan['case']=='PC-CONTACT'
assert sha(S/'launch-manifests/PC-CONTACT.json')==plan['granted_manifest_sha256']
assert sha(S/'inputs/PC-CONTACT.snapshot.json.gz')==plan['snapshot_sha256']
assert sha(S/'approvals/PC-CONTACT.request.json')==plan['approval_request_sha256']
sys.path.insert(0,str(D))
from loom_commissioning.authority import execution_sha256,validate_execution
from loom_commissioning.contract import authorize_execution
m=read(S/'launch-manifests/PC-CONTACT.json')
assert execution_sha256(m)==plan['authority_sha256']
validate_execution(m,complete=True); authorize_execution(m)
for name,value in m['execution']['procedure']['protocol']['bound_documents'].items():
    assert sha(ROOT/'exports/2026-09-26-B1-regenerated-352f73ff/B1_OPERATOR_PACKET'/name)==value
write_new(S/'PC-MOTION.RESULT.json',result)
write_new(S/'SEQUENCE_STATE.before_PC-CONTACT.json',state)
state.update(status='PC-MOTION CLOSED; PC-CONTACT VERIFIED FOR LAUNCH',next_case='PC-CONTACT',status_observed_utc=at)
state['cases'][1]['status']='CLOSED AT WALL CAP; DEMONSTRATED WITH GUIDANCE AND POST-CLOSURE EXPLANATION'
state_path.write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8')
write_new(S/'PC-CONTACT.LAUNCH_INTENT.json',dict(case='PC-CONTACT',attempt=1,apparatus=APP,
    authority_sha256=plan['authority_sha256'],preflight_utc=at,free_disk_bytes=shutil.disk_usage(ROOT).free,
    source_clean=True,identity_and_approval_verified=True,initial_snapshot_hash_verified=True,
    invocation_reserved=1,service_started=False,simulation_steps=0,snapshot_not_deserialized_by_preflight=True,
    B1_state_accessed=False,scope='Existing exact PC-CONTACT grant in prepared order; one attempt, no retry, no changes.'))
print('PC-MOTION result and guidance preserved; native records verified. PC-CONTACT exact grant/source verified and one launch reserved. No world loaded by this script.')
