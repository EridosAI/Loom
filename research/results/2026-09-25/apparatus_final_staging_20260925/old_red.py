"""Exact three residuals at 9d31e790; bounded manufactured/validation inputs only."""
import copy,json,pathlib,sys
from unittest.mock import patch
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology';E=D/'artifacts/apparatus-final-correction-20260925-01a0c405'
sys.path[:0]=[str(D),str(D/'tests_apparatus')]
import numpy as np
from test_apparatus import manufactured
from loom_commissioning import authority,controllers,runner
from loom_commissioning.contract import *
from loom_commissioning.validators import verify_segment
PLAN=[{'point':[6.,5.],'until':.1,'press_force':0.},{'point':[5.,6.],'until':.2,'press_force':0.}]
kind=sys.argv[1];out=E/('old-9d31-'+kind);out.mkdir()
result={'checkpoint':'9d31e7902658b15762052a2a6a3d161d64338524','case':kind,'commissioning_constructors':0}
if kind=='duplicates':
    rows=[]
    for name in ('SYNTHETIC_duplicate-approved-execution_NO_EXECUTION.json','SYNTHETIC_duplicate-nested-waypoint_NO_EXECUTION.json'):
        p=E/'references'/name;raw=p.read_bytes();request=json.loads(raw);m=request['approved_execution']
        m['execution_authority']=dict(request_path=str(p),request_sha256=digest(raw),approved_case=m['case_id'],
            approved_initial_state=m['initial_state'],approved_duration=m['duration_seconds'],approved_execution_sha256=request['approved_execution_sha256'])
        authorize_execution(m);rows.append({'case':name,'ambiguous_approval_accepted':True})
    result.update(rows=rows,native_steps=0)
elif kind=='dispatch':
    e=manufactured();m=make_manifest(e,'fixture-old-alias',EXTERNAL,'waypoint',.2,plan=PLAN)
    run=runner.Run(e,m,out/'alias');expected,_=runner.waypoint_command(controllers.privileged_input(e),copy.deepcopy(PLAN),0)
    def other(data,plan,cursor):return np.array([-.5,.5]),cursor
    other.__name__=other.__qualname__='waypoint_command'
    with patch.object(runner,'waypoint_command',other):run.begin_command();run.advance(1)
    run.close();result.update(expected=expected.tolist(),delivered=e.body.command.tolist(),native_steps=e.native_index,replay=verify_segment(out/'alias'))
else:
    e=manufactured();m=make_manifest(e,'fixture-old-persisted-held',EXTERNAL,'waypoint',.2,plan=PLAN)
    first=runner.Run(e,m,out/'first');first.begin_command();issued=first.session['held_command'].copy();first.advance(7)
    first.session['held_command']=[-.5,.5];first.session['hold_remaining']=4;first.close()
    second=runner.Run.resume(out/'first',out/'second');second.hold();second.close()
    result.update(issued=issued,delivered=second.engine.body.command.tolist(),native_steps=second.engine.native_index,
        final_time=second.engine.time,stage_deadline=.1,replay=[verify_segment(out/'first'),verify_segment(out/'second')])
(out/'RESULT.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2),flush=True)
assert False,'ORIGINAL RED: '+kind+' was accepted with all original guards enabled'
