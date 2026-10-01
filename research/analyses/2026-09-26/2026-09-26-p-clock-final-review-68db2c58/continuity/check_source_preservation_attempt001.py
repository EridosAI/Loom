"""Read-only causal source/cadence audit; writes this new review directory only."""
import ast,hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;W=HERE.parents[2]
R=W/'worktrees/loom-p-clock-correction-20260926';D=R/'developmental_ecology'
BASE='5f07748102cb5eaa302569c87efbae095050e9fe';HEAD='68db2c581f07200966d699a4f55a65f9b96df1e9';P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
G=['git','-c','safe.directory='+R.as_posix(),'-C',str(R)]
def git(*args):return subprocess.check_output(G+list(args))
def blob(commit,rel):return git('show',commit+':developmental_ecology/'+rel)
def sha(b):return hashlib.sha256(b).hexdigest()
assert git('rev-parse','HEAD').decode().strip()==HEAD
result={'head':HEAD,'base':BASE,'P':P,'unchanged_committed_paths':[],'P_files':[],
        'physical_time_assignment_changes':[], 'preserved_function_bodies':[]}
for commit,paths in [(P,['developmental_ecology/loom_p','developmental_ecology/configuration.json']),
    (BASE,['developmental_ecology/loom_commissioning/adapter.py','developmental_ecology/loom_p',
           'developmental_ecology/configuration.json','developmental_ecology/tests','developmental_ecology/requirements-lock.txt'])]:
    assert not git('diff','--name-only',commit,HEAD,'--',*paths)
    result['unchanged_committed_paths'].append({'from':commit,'paths':paths,'diff_empty':True})
for p in sorted((D/'loom_p').glob('*.py')):
    raw=p.read_bytes();old=blob(P,p.relative_to(D).as_posix());assert raw==old
    result['P_files'].append({'path':p.relative_to(D).as_posix(),'sha256':sha(raw),'equals_P_blob':True})
for rel in ('loom_commissioning/adapter.py','loom_commissioning/clock.py','loom_commissioning/controllers.py',
            'loom_commissioning/pending.py','loom_commissioning/runner.py','loom_commissioning/authority.py','loom_commissioning/validators.py'):
    assert (D/rel).read_bytes()==blob(HEAD,rel)
def function(source,name):
    return next(n for n in ast.walk(ast.parse(source)) if isinstance(n,ast.FunctionDef) and n.name==name)
def dump(n):return ast.dump(n,include_attributes=False)
for rel,names in [('loom_commissioning/runner.py',['advance','hold','close']),
                 ('loom_commissioning/controllers.py',['privileged_input','command_pair','validate_sensor_payload','observe_without_interference'])]:
    old=blob(BASE,rel).decode();new=(D/rel).read_text()
    for name in names:
        assert dump(function(old,name))==dump(function(new,name))
        result['preserved_function_bodies'].append(rel+'::'+name)
old=ast.parse(blob(BASE,'loom_commissioning/controllers.py').decode())
new=ast.parse((D/'loom_commissioning/controllers.py').read_text())
def settings(tree):return next(n for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='WAYPOINT_SETTINGS' for t in n.targets))
assert dump(settings(old))==dump(settings(new));result['controller_settings_unchanged']=True
def force_math(tree):
    n=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='waypoint_command')
    start=next(i for i,x in enumerate(n.body) if isinstance(x,ast.Assign) and isinstance(x.value,ast.Name) and x.value.id=='WAYPOINT_SETTINGS')
    stop=next(i for i,x in enumerate(n.body) if isinstance(x,ast.If) and isinstance(x.test,ast.Call) and isinstance(x.test.func,ast.Name) and x.test.func.id=='time_due')
    return [dump(x) for x in n.body[start:stop]]
assert force_math(old)==force_math(new);result['waypoint_actuator_math_unchanged']=True
for rel in ('clock.py','authority.py','controllers.py','pending.py','runner.py','validators.py'):
    tree=ast.parse((D/'loom_commissioning'/rel).read_text())
    assignments=[]
    for n in ast.walk(tree):
        targets=n.targets if isinstance(n,ast.Assign) else [n.target] if isinstance(n,(ast.AnnAssign,ast.AugAssign)) else []
        if any(isinstance(t,ast.Attribute) and t.attr=='time' for t in targets):assignments.append(n.lineno)
    assert not assignments,(rel,assignments)
    result['physical_time_assignment_changes'].append({'file':rel,'assignments_to_object_time':assignments})
sys.path.insert(0,str(D))
from loom_p.schema import Config
c=Config();result['unchanged_cadences']={'native_dt':c.native_dt,'wave_dt':c.wave_dt,
    'wave_native_steps':round(c.wave_dt/c.native_dt),'motor_noise_refresh':c.noise_refresh,
    'noise_native_steps':round(c.noise_refresh/c.native_dt),'event_time_tol':c.event_time_tol,
    'command_steps':10}
assert c.native_dt==.01 and c.wave_dt==.2 and c.noise_refresh==.5 and c.event_time_tol==1e-10
result['all_checks_passed']=True
(HERE/'SOURCE_PRESERVATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
