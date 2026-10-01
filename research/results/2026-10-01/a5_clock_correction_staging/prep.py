import ast,copy,hashlib,json,pathlib,shutil,sys
R=pathlib.Path(__file__).resolve().parents[1]
OLD=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')/'developmental_ecology'
NEW=R/'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
OUT=R/'exports/2026-09-26-A5-clock-correction';OUT.mkdir(exist_ok=False)
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
protected={}
for directory in ('loom_p','tests'):
    for p in (OLD/directory).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:
            name=p.relative_to(OLD).as_posix();protected[name]=sha(p);assert sha(NEW/name)==protected[name]
for name in ('configuration.json','requirements-lock.txt','loom_commissioning/adapter.py'):
    protected[name]=sha(OLD/name);assert sha(NEW/name)==protected[name]
(OUT/'PROTECTED_BEFORE.json').write_text(json.dumps(protected,indent=2))
shutil.copytree(OLD/'artifacts/prehistory-attempt-001',NEW/'artifacts/prehistory-attempt-001')
(OUT/'REQUEST.txt').write_bytes(pathlib.Path(r'C:\Users\Jason\.codex\attachments\386e6945-0576-467b-b04f-caeefc7cb51c\Pasted text.txt').read_bytes())
check=NEW/'artifacts/.clock-access-check';check.write_text('scoped read write');assert check.read_text()=='scoped read write';check.unlink()
sys.path.insert(0,str(OLD))
from loom_commissioning import pending,controllers,authority,contract
from loom_p.records import code_identity
assert code_identity()['sha256']==contract.P_CODE
times=[0.]
for _ in range(27000):times.append(times[-1]+.01)
data=json.loads((OLD/'tests_apparatus/fixtures/review-boundary-input.json').read_bytes())
m={'mode':contract.EXTERNAL,'controller':'manual_privileged','initial_time':0.,'initial_index':0,'hard_stop_time':630.}
d={'time':times[26950],'native_index':26950,'actor':contract.EXTERNAL,'controller':'manual_privileged','inputs':copy.deepcopy(data),'command':[0.,0.],
   'hold_native_steps':10,'annotation':'DETACHED CLOCK REPRODUCTION; NOT A LAUNCH MANIFEST','execution_sha256':authority.execution_sha256(m),'stage':None,'case_deadline':630.}
d['inputs']['time']=d['time']
errors=[]
try:pending.validate_decision(m,d)
except ValueError as e:errors.append(str(e))
assert errors==['issued decision clock mismatch']
# Extract and execute the exact independent runner guard expression, so the
# first rejection cannot mask it. No Run, observer, physical state or world call.
src=(OLD/'loom_commissioning/runner.py').read_text()
node=next(n for n in ast.walk(ast.parse(src)) if isinstance(n,ast.Call) and len(n.args)>1 and isinstance(n.args[1],ast.Constant) and n.args[1].value=='command hold would cross prescribed stage boundary')
plan=[{'point':[6.,5.],'until':t,'press_force':0.} for t in (90.,120.,270.,300.,450.,480.,630.)]
data['time']=times[27000];_,stage=controllers.waypoint_command(data,plan,0)
until=plan[stage]['until'];end=data['time']+.1
ok=eval(compile(ast.Expression(node.args[0]),str(OLD/'loom_commissioning/runner.py'),'eval'),{'end':end,'until':until,'dispatch':{'time_due':controllers.time_due}})
try:contract.require(ok,node.args[1].value)
except ValueError as e:errors.append(str(e))
assert errors[-1]=='command hold would cross prescribed stage boundary'
result={'old_apparatus':'5f07748102cb5eaa302569c87efbae095050e9fe','world_steps':0,'A5_controller_world_calls':0,
 'A':{'status':'RED','index':26950,'physical_time':times[26950],'error':errors[0],'source':'pending.validate_decision'},
 'B':{'status':'RED','index':27000,'physical_time':data['time'],'stage':stage,'deadline':until,'end':end,'error':errors[1],
      'method':'Exact runner condition extracted by AST; first guard excluded, detached generic controller input and same deadlines.'}}
(OUT/'OLD_FAILURES_RED.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
