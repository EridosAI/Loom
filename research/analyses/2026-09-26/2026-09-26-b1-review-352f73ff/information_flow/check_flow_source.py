"""Read-only source identity and causal preservation for operator projection."""
import ast,hashlib,json,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent;W=HERE.parents[2]
R=W/'worktrees/loom-p-b1-apparatus-correction-20260926';D=R/'developmental_ecology'
HEAD='352f73fffa6d9781eae8aa38e708a9a05669588f';BASE='68db2c581f07200966d699a4f55a65f9b96df1e9'
G=['git','-c','safe.directory='+R.as_posix(),'-C',str(R)]
def git(*args):return subprocess.check_output(G+list(args))
assert git('rev-parse','HEAD').decode().strip()==HEAD
unchanged=['developmental_ecology/loom_p','developmental_ecology/configuration.json',
    'developmental_ecology/loom_commissioning/adapter.py','developmental_ecology/loom_commissioning/clock.py',
    'developmental_ecology/loom_commissioning/evaluation.py','developmental_ecology/loom_commissioning/diagnostics.py']
assert not git('diff','--name-only',BASE,HEAD,'--',*unchanged)
files=['loom_commissioning/'+n for n in ('authority.py','contract.py','controllers.py','operator_view.py',
    'pending.py','runner.py','sensor.html','sensor_ui.py','validators.py')]+['tests_apparatus/test_b1_operator.py','tests_apparatus/b1_dom_fixture.cjs']
result={'head':HEAD,'base':BASE,'unchanged_paths':unchanged,'source_files':[]}
for rel in files:
    raw=(D/rel).read_bytes();blob=git('show',HEAD+':developmental_ecology/'+rel)
    assert raw==blob
    result['source_files'].append({'path':rel,'sha256':hashlib.sha256(raw).hexdigest(),'exact_committed_bytes':True})
old=ast.parse(git('show',BASE+':developmental_ecology/loom_commissioning/controllers.py').decode())
new=ast.parse((D/'loom_commissioning/controllers.py').read_text())
for name in ('SensorHistory','command_pair','waypoint_command','waypoint_stage','time_due','privileged_input'):
    def node(tree):return next(n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name==name)
    assert ast.dump(node(old),include_attributes=False)==ast.dump(node(new),include_attributes=False)
result['unchanged_controller_surfaces']=['SensorHistory','command_pair','waypoint_command','waypoint_stage','time_due','privileged_input']
result['all_checks_passed']=True
(HERE/'SOURCE_FLOW.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
