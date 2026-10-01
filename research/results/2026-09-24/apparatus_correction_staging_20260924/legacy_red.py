"""Exact reviewer counterexamples, checked against required behavior. No steps."""
import copy, gzip, json, pathlib, sys
WT=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
REVIEW=pathlib.Path(__file__).resolve().parents[1]/'exports/2026-09-24-p-apparatus-review-05abf604/physical'
sys.path.insert(0,str(WT/'developmental_ecology'))
from loom_commissioning.contract import *
from loom_commissioning.controllers import waypoint_command
from loom_commissioning.initialization import from_verified_cache
OUT=WT/'developmental_ecology/artifacts/apparatus-correction-20260924-01a0c405'
kind=sys.argv[1]
if kind=='authority':
    e,init=from_verified_cache(WT/'developmental_ecology/artifacts/prehistory-attempt-001',0)
    m=make_manifest(e,'authority-validation-only',EXTERNAL,'waypoint',.01,purpose='commissioning',initialization=init)
    p=REVIEW/'MANUFACTURED-AUTHORITY-NO-EXECUTION.json'
    m['execution_authority']=dict(request_path=str(p),request_sha256=digest(p.read_bytes()),approved_case=m['case_id'],approved_initial_state=m['initial_state'],approved_duration=.01)
    validate_manifest(m,e); authorize_execution(m)
    rows=[]
    for mode,controller in [(EXTERNAL,'sensor_human'),(EXTERNAL,'manual_privileged'),(INTACT,'none'),(FIXED,'none')]:
        other=copy.deepcopy(m); other.update(mode=mode,controller=controller)
        validate_manifest(other,e); authorize_execution(other)
        rows.append({'mode':mode,'controller':controller,'wrong_arm_accepted':True,'same_grant':True})
    print(json.dumps({'exact_matching_object_accepted':True,'substitutions':rows,'native_steps':e.native_index,'commissioning_constructors':0},indent=2),flush=True)
    assert not any(x['wrong_arm_accepted'] for x in rows),'A-R1 RED: original grant accepts unapproved arms'
else:
    actions=[json.loads(x) for x in gzip.decompress((REVIEW/'hold-continuous/controller.jsonl.gz').read_bytes()).splitlines()]
    data=actions[1]['inputs']; assert data['time']==0.09999999999999999
    plan=[{'point':[6.,5.],'until':.1,'press_force':0.},{'point':[5.,6.],'until':.2,'press_force':0.}]
    at=copy.deepcopy(data); at['time']=.1
    actual,cursor=waypoint_command(data,plan,0); boundary,expected=waypoint_command(at,plan,0)
    final,_=waypoint_command(data,plan[:1],0)
    print(json.dumps({'saved_time':data['time'],'nominal_time':.1,'difference':.1-data['time'],'actual_cursor':cursor,'boundary_cursor':expected,'actual_command':actual.tolist(),'boundary_command':boundary.tolist(),'final_command':final.tolist(),'extra_hold_steps':actions[1]['hold_native_steps'],'world_steps':0},indent=2),flush=True)
    assert cursor==1 and not final.any(),'A-R2 RED: original clock retains expired stage for another hold'
