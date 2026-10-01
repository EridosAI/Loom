"""Revalidate the one authorized PC-LR launch; no simulation or interface changes."""
import datetime,hashlib,json,os,pathlib,shutil,subprocess,sys
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926';D=W/'developmental_ecology'
APP='352f73fffa6d9781eae8aa38e708a9a05669588f'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
cmd=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
assert subprocess.check_output(cmd+['rev-parse','HEAD'],env=env).decode().strip()==APP
assert subprocess.check_output(cmd+['status','--porcelain'],env=env)==b''
state=read(S/'SEQUENCE_STATE.json');assert state['next_case']=='PC-LR' and all(c['attempts']==0 for c in state['cases'])
assert not (S/'runs/PC-LR').exists() and not (S/'PC-LR.LAUNCH_INTENT.json').exists()
plan=read(S/'LAUNCH_PLAN.json')['cases'][0];assert plan['case']=='PC-LR'
m_path=S/'launch-manifests/PC-LR.json';snapshot=S/'inputs/PC-LR.snapshot.json.gz';approval=S/'approvals/PC-LR.request.json'
assert sha(m_path)==plan['granted_manifest_sha256'] and sha(snapshot)==plan['snapshot_sha256'] and sha(approval)==plan['approval_request_sha256']
assert shutil.disk_usage(ROOT).free>=12_000_000_000
sys.path.insert(0,str(D))
from loom_commissioning.authority import execution_sha256,validate_execution
from loom_commissioning.contract import authorize_execution
m=read(m_path);assert execution_sha256(m)==plan['authority_sha256']
validate_execution(m,complete=True);authorize_execution(m)
for name,value in m['execution']['procedure']['protocol']['bound_documents'].items():
    assert sha(ROOT/'exports/2026-09-26-B1-regenerated-352f73ff/B1_OPERATOR_PACKET'/name)==value
at=datetime.datetime.now(datetime.timezone.utc).isoformat()
integrity_path=S/'OPERATOR_INTEGRITY_RECORD.json';integrity_before=integrity_path.read_bytes();integrity=json.loads(integrity_before)
(S/'OPERATOR_INTEGRITY_RECORD.before_readiness.json').write_bytes(integrity_before)
integrity.update(prior_sealed_B1_access='No — Jason self-report; no hidden contents requested',prior_sealed_B1_access_verbatim='No',
    readiness_verbatim='ok, lets do it.',ready=True,readiness_recorded_utc=at,
    interface_familiarity='Jason is familiar with the project but unfamiliar with the interface; introductory control guidance only, no response/command coaching.',
    next_interaction='Open PC-LR prepared interface. Jason identifies paired-channel indices/sign before any actuator action, and makes all commands.')
assert integrity_path.read_bytes()==integrity_before;write(integrity_path,integrity)
intent=dict(case='PC-LR',authority_sha256=plan['authority_sha256'],apparatus=APP,readiness='Explicit user readiness received',
    preflight_utc=at,free_disk_bytes=shutil.disk_usage(ROOT).free,source_clean=True,identity_and_approval_verified=True,
    initial_snapshot_hash_verified=True,snapshot_not_deserialized_by_preflight=True,
    invocation_reserved=1,service_started=False,simulation_steps=0,B1_state_accessed=False,
    rule='Launch exactly once using the unchanged prepared command; do not auto-retry on failure.')
with (S/'PC-LR.LAUNCH_INTENT.json').open('x',encoding='utf-8') as f:json.dump(intent,f,indent=2)
print('PC-LR preflight passed; exact approved identity and source verified. Readiness and no-prior-B1-exposure self-report recorded. No service or simulation started by preflight.')
