"""Independent workflow-guard faults, confined to manufactured apparatus fixtures."""
import copy
import json
from pathlib import Path
import sys
import tempfile
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
TARGET = Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology')
sys.path[:0] = [str(TARGET), str(TARGET/'tests_apparatus')]
import numpy as np
from test_apparatus import manufactured
from test_corrections import grant_fixture
from loom_p.records import state_hash
from loom_commissioning import authority, controllers, runner
from loom_commissioning.contract import make_manifest, validate_manifest, authorize_execution, EXTERNAL

PLAN = [{'point':[6.,5.], 'until':.1, 'press_force':0.},
        {'point':[5.,6.], 'until':.2, 'press_force':0.}]
OUT = Path(tempfile.mkdtemp(prefix='components-',dir=ROOT))
RESULT = {'components':str(OUT), 'scope':'Manufactured <=0.2 s fixtures and validation-only synthetic authority. No commissioning constructor or case execution.'}

def manifest(e,name):
    return make_manifest(e,'fixture-'+name,EXTERNAL,'waypoint',.2,plan=PLAN)

def value_error(call):
    try: call()
    except ValueError as error: return str(error)
    return None

def check_alias():
    # A real complete commissioning grant is checked only in validation calls.
    # It is not passed to Run and authorizes no commissioning trajectory.
    e_grant,m_grant,p = grant_fixture(OUT)
    validate_manifest(m_grant,e_grant); authorize_execution(m_grant)
    saved_request=p.read_bytes(); approved=authority.execution_sha256(m_grant)
    live_identity=authority.controller_identity('waypoint')
    e=manufactured(); m=manifest(e,'alias-version'); run=runner.Run(e,m,OUT/'alias-version')
    original=runner.waypoint_command
    expected,cursor=original(controllers.privileged_input(e),copy.deepcopy(PLAN),0)
    def alternate_version(data,plan,cursor):
        return np.array([-.5,.5]),cursor
    alternate_version.__name__='waypoint_command'
    alternate_version.__qualname__='waypoint_command'
    assert authority.callable_identity(alternate_version)!=authority.callable_identity(original)
    with patch.object(runner,'waypoint_command',alternate_version):
        # Current authority check and every ordinary Run guard remain enabled.
        validate_manifest(m_grant,e_grant); authorize_execution(m_grant)
        assert authority.controller_identity('waypoint')==live_identity
        run._guard(); run.begin_command(); run.advance(1)
    delivered=e.body.command.copy()
    assert np.array_equal(delivered,[-.5,.5]) and not np.array_equal(delivered,expected)
    assert p.read_bytes()==saved_request and authority.execution_sha256(m_grant)==approved
    run.close()
    # The delivered test patches this other namespace and does reject it.
    control=manufactured(); cm=manifest(control,'alias-positive-control')
    cr=runner.Run(control,cm,OUT/'alias-positive-control')
    with patch.object(controllers,'waypoint_command',alternate_version):
        error=value_error(cr.begin_command)
    assert error=='controller execution identity mismatch' and control.native_index==0
    cr.close()
    RESULT['runtime_callable_alias']={
        'same_display_name':alternate_version.__name__==original.__name__,
        'changed_callable_code_identity':True, 'authority_and_runtime_guard_accepted':True,
        'approved_controller_identity_unchanged':True, 'approved_request_unchanged':True,
        'expected_command':expected.tolist(),'delivered_command':delivered.tolist(),
        'native_steps':e.native_index,'control_controllers_namespace_rejected':error}

def check_hold_mutation():
    e=manufactured(); m=manifest(e,'held-command'); run=runner.Run(e,m,OUT/'held-command')
    run.begin_command(); recorded=copy.deepcopy(run.sensor.payload['own_commands'][-1]['command'])
    execution=authority.execution_sha256(run.manifest)
    run.session['held_command']=[-.5,.5]
    run._guard(); run.advance(1)
    assert e.body.command.tolist()==[-.5,.5] and e.body.command.tolist()!=recorded
    assert authority.execution_sha256(run.manifest)==execution
    run.close()
    RESULT['live_held_command']={'guard_accepted':True,'recorded_approved_command':recorded,
        'delivered_command':e.body.command.tolist(),'native_steps':e.native_index,
        'execution_identity_unchanged':True}

def check_hold_length_mutation():
    e=manufactured(); m=manifest(e,'held-count'); run=runner.Run(e,m,OUT/'held-count')
    run.begin_command(); first=copy.deepcopy(run.session['held_command'])
    run.session['hold_remaining']=11
    run._guard(); run.hold()
    assert e.native_index==11 and e.time>.1+1e-10
    assert e.body.command.tolist()==first and run.session['cursor']==0
    run.close()
    RESULT['live_hold_count']={'guard_accepted':True,'recorded_hold_steps':10,
        'executed_native_steps':e.native_index,'time':e.time,'stage_deadline':.1,
        'recorded_command':first,'command_after_deadline':e.body.command.tolist()}

def check_resume_mutation():
    e=manufactured(); m=manifest(e,'resume-held'); first=runner.Run(e,m,OUT/'resume-first')
    first.begin_command(); recorded=copy.deepcopy(first.session['held_command']); first.advance(7)
    assert first.session['hold_remaining']==3
    first.close()
    # Legitimate saved state loads normally. Mutation happens in the ordinary mutable
    # session object consumed by Run's explicit session= restart entry point.
    resumed_e,s,resumed_m=runner.load_restart(OUT/'resume-first/final.restart.json.gz')
    original_state=state_hash(resumed_e)
    s['held_command']=[-.5,.5]; s['hold_remaining']=4
    authority.validate_session(resumed_m,s)
    resumed=runner.Run(resumed_e,resumed_m,OUT/'resume-mutated',session=s)
    resumed.hold()
    assert resumed_e.native_index==11 and resumed_e.time>.1+1e-10
    assert resumed_e.body.command.tolist()==[-.5,.5]
    resumed.close()
    RESULT['resume_pending_hold']={'loaded_original_native_index':7,'original_remaining':3,
        'mutated_remaining':4,'session_validation_accepted':True,'constructor_accepted':True,
        'recorded_command':recorded,'delivered_command':resumed_e.body.command.tolist(),
        'final_native_index':resumed_e.native_index,'final_time':resumed_e.time,
        'pre_resume_state':original_state,'saved_manifest_unchanged':resumed_m==m}

def check_persistence_of_bad_pending_hold():
    e=manufactured(); m=manifest(e,'persisted-held'); first=runner.Run(e,m,OUT/'persist-first')
    first.begin_command(); recorded=copy.deepcopy(first.session['held_command']); first.advance(7)
    first.session['held_command']=[-.5,.5]
    first.session['hold_remaining']=4
    first.close()  # Production writer creates and hashes the changed mutable state.
    resumed=runner.Run.resume(OUT/'persist-first',OUT/'persist-resumed')
    resumed.hold()
    assert resumed.engine.native_index==11 and resumed.engine.time>.1+1e-10
    assert resumed.engine.body.command.tolist()==[-.5,.5]
    resumed.close()
    RESULT['saved_bad_pending_hold']={'ordinary_save_and_resume_accepted':True,
        'recorded_command':recorded,'delivered_command':resumed.engine.body.command.tolist(),
        'final_native_index':resumed.engine.native_index,'final_time':resumed.engine.time,
        'no_disk_receipt_or_restart_hash_edit':True}

def check_supported_mutation_rejections():
    results={}
    for label in ('route','settings','resources'):
        e=manufactured(); m=manifest(e,'guard-'+label); run=runner.Run(e,m,OUT/('guard-'+label))
        before=state_hash(e)
        if label=='route':
            run.session['route'][0]['point']=[4.,5.]
            error=value_error(run.begin_command)
            run.session['route']=copy.deepcopy(PLAN)
        elif label=='resources':
            run.wall_limit+=1; error=value_error(run.begin_command); run.wall_limit-=1
        else:
            with patch.dict(controllers.WAYPOINT_SETTINGS,{'heading_gain':.81}):
                error=value_error(run.begin_command)
        assert error and state_hash(e)==before and not run.sensor.payload['own_commands']
        results[label]=error; run.close()
    RESULT['positive_rejection_controls']=results

if __name__=='__main__':
    check_alias()
    check_hold_mutation()
    check_hold_length_mutation()
    check_resume_mutation()
    check_persistence_of_bad_pending_hold()
    check_supported_mutation_rejections()
    path=ROOT/'RUNTIME_BINDING_RESULTS.json'
    path.write_text(json.dumps(RESULT,indent=2),encoding='utf-8')
    print(json.dumps(RESULT,indent=2))
