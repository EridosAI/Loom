"""Exact prior alias fixture and delivered bounded controller checks only."""
import argparse
import copy
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

p=argparse.ArgumentParser()
p.add_argument('--source',type=Path,required=True)
p.add_argument('--checkpoint',required=True)
p.add_argument('--output',type=Path,required=True)
p.add_argument('--expect',choices=['old-RED','new-GREEN'],required=True)
a=p.parse_args()
source=a.source.resolve(); output=a.output.resolve(); output.mkdir(parents=True,exist_ok=False)
target=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
sys.path[:0]=[str(source),str(source/'tests_apparatus')]
import numpy as np
from test_apparatus import manufactured
from test_corrections import grant_fixture, PLAN
from loom_p.records import state_hash
from loom_commissioning import authority,controllers,runner
from loom_commissioning.contract import make_manifest,validate_manifest,authorize_execution,EXTERNAL
from loom_commissioning.validators import verify_segment

result={'checkpoint':a.checkpoint,'source':str(source),'expectation':a.expect,
        'scope':'Exact prior manufactured alias fixture; synthetic grant validation only; no commissioning execution.',
        'command':sys.argv,'source_identity':[]}
files=[*source.joinpath('loom_p').glob('*.py'),source/'configuration.json',
       *[source/'loom_commissioning'/f for f in ('authority.py','controllers.py','runner.py','adapter.py')],
       *[source/'tests_apparatus'/f for f in ('test_apparatus.py','test_corrections.py')]]
for file in sorted(files):
    rel=file.relative_to(source).as_posix()
    blob=subprocess.run(['git','-c','safe.directory='+target.as_posix(),'-C',str(target),
        'show',a.checkpoint+':developmental_ecology/'+rel],capture_output=True,check=True).stdout
    raw=file.read_bytes()
    exact=raw==blob; normalized=raw.replace(b'\r\n',b'\n')==blob.replace(b'\r\n',b'\n')
    assert normalized, ('SOURCE DOES NOT MATCH PINNED CHECKPOINT',rel)
    result['source_identity'].append({'path':rel,'raw_sha256':hashlib.sha256(raw).hexdigest(),
        'git_blob_sha256':hashlib.sha256(blob).hexdigest(),'raw_equal':exact,'newline_normalized_equal':normalized})
for module in (authority,controllers,runner):
    assert Path(module.__file__).resolve().is_relative_to(source)
result['imported_modules']={m.__name__:str(Path(m.__file__).resolve()) for m in (authority,controllers,runner)}

# The same complete synthetic approval check from the original reproduction.
# It is never passed into a Run; the executed fixture retains manufactured purpose.
grant_dir=output/'validation-only'; grant_dir.mkdir()
ge,gm,gp=grant_fixture(grant_dir)
validate_manifest(gm,ge);authorize_execution(gm)
approved_bytes=gp.read_bytes(); approved_digest=authority.execution_sha256(gm)
controller_identity=authority.controller_identity('waypoint')
e=manufactured();m=make_manifest(e,'fixture-alias-version',EXTERNAL,'waypoint',.2,plan=PLAN)
run=runner.Run(e,m,output/'alias-version')
original=runner.waypoint_command
expected,cursor=original(controllers.privileged_input(e),copy.deepcopy(PLAN),0)
before=state_hash(e); alternate_calls=[]; error=None
def alternate_version(data,plan,cursor):
    alternate_calls.append(True)
    return np.array([-.5,.5]),cursor
alternate_version.__name__=alternate_version.__qualname__='waypoint_command'
assert authority.callable_identity(alternate_version)!=authority.callable_identity(original)
with patch.object(runner,'waypoint_command',alternate_version):
    validate_manifest(gm,ge);authorize_execution(gm)
    assert authority.controller_identity('waypoint')==controller_identity
    try:
        run._guard();run.begin_command();run.advance(1)
    except ValueError as exc:
        error=str(exc)
assert gp.read_bytes()==approved_bytes and authority.execution_sha256(gm)==approved_digest
result['exact_alias']={'expected_command':expected.tolist(),'body_command':e.body.command.tolist(),
    'native_index':e.native_index,'time':e.time,'rejection':error,'alternate_calls':len(alternate_calls),
    'engine_unchanged':state_hash(e)==before,'own_commands':copy.deepcopy(run.sensor.payload['own_commands']),
    'approved_identity_and_request_unchanged':True}
if a.expect=='old-RED':
    assert error is None and alternate_calls and e.native_index==1
    assert e.body.command.tolist()==[-.5,.5] and e.body.command.tolist()!=expected.tolist()
    run.close()
    verified=verify_segment(output/'alias-version')
    assert verified['native_records']==1
    result['exact_alias']['replay_accepted']=verified
else:
    assert error=='executed controller dispatch mismatch: waypoint_command'
    assert not alternate_calls and state_hash(e)==before and not run.sensor.payload['own_commands']
    assert e.native_index==0 and e.time==0.
    # Restore the approved actual emitter and confirm its pair reaches physics.
    run.begin_command(); assert run.session['held_command']==expected.tolist()
    run.advance(1); assert e.body.command.tolist()==expected.tolist()
    result['approved_physical_control']={'delivered':e.body.command.tolist(),'native_index':e.native_index,'time':e.time}
    run.close()
    assert verify_segment(output/'alias-version')['native_records']==1
    # Exact delivered fixtures; no alternate routes, controller objectives or sweeps.
    import test_final_corrections as tests
    checks=[]
    for name in ('waypoint_command','command_pair','privileged_input','time_due','observe_without_interference'):
        d=output/('delivered-dispatch-'+name);d.mkdir()
        tests.test_actual_dispatch_is_checked(d,name)
        checks.append({'test':'test_actual_dispatch_is_checked['+name+']','passed':True})
    for name in ('test_dispatch_changed_between_check_and_use','test_post_approval_constants_and_route',
                 'test_resume_binding_and_stage_transition'):
        d=output/name;d.mkdir();getattr(tests,name)(d)
        checks.append({'test':name,'passed':True})
    result['delivered_controller_checks']=checks
result['all_expected_assertions_passed']=True
(output/'RESULT.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
