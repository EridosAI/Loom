"""Fresh delivered B1 component regression and A-L fault/control invocations."""
from pathlib import Path
import concurrent.futures,json,os,re,subprocess,sys,time
R=Path(__file__).resolve().parent;W=R.parents[1]
T=W/'worktrees/loom-p-b1-apparatus-correction-20260926/developmental_ecology'
P=R/'portable/source/developmental_ecology'
OUT=R/'regression';OUT.mkdir(exist_ok=False)
NODE=Path(r'C:\Program Files\nodejs\node.exe')
CASES={
 'A':('test_A_hidden_authority','old rejection'),
 'B':('test_B_payload_canary','CHEMISTRY PAYLOAD LEAK'),
 'C':('test_C_DOM_and_UI','CSS-ONLY MASK EXPORTED CHEMISTRY'),
 'D':('test_D_raw_record_not_mutated','DISPLAY DEPRIVATION ALTERED PHYSICAL RAW RECORD'),
 'E':('test_paused_inertness[E]','PAUSED CLOCK/RNG/EXPENDITURE BREACH E'),
 'F':('test_paused_inertness[F]','PAUSED CLOCK/RNG/EXPENDITURE BREACH F'),
 'G':('test_paused_inertness[G]','PAUSED CLOCK/RNG/EXPENDITURE BREACH G'),
 'H':('test_H_duplicate_token','DUPLICATE CREATED EXTRA HOLD'),
 'I':('test_I_running_overlap','OVERLAPPING EXECUTIONS ACCEPTED'),
 'J':('test_J_ended_irreversible','ENDED ADVANCED WORLD'),
 'K':('test_K_refresh_reconnect_inert','REFRESH/RECONNECT ADVANCED WORLD'),
 'L':('test_L_full_raw_preserved','FULL RAW LOST CHEMISTRY')}
def execute(label,root,args,fault=None):
    env=os.environ.copy()
    for k in ('PYTHONPATH','PYTEST_ADDOPTS','PYTEST_PLUGINS','APPARATUS_FAULT','CORRECTION_FAULT','FINAL_FAULT','CLOCK_FAULT','B1_FAULT'):env.pop(k,None)
    env.update(PYTHONPATH=str(root),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',GIT_OPTIONAL_LOCKS='0',NODE_BIN=str(NODE))
    if fault:env['B1_FAULT']=fault
    cmd=[sys.executable,'-B','-X','utf8','-m','pytest',*args,'-q','-p','no:cacheprovider',
        '--basetemp',str(OUT/(label+'-temp')),'--junitxml',str(OUT/(label+'.xml'))]
    start=time.perf_counter()
    p=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,encoding='utf-8',timeout=600)
    log=p.stdout+p.stderr;(OUT/(label+'.log')).write_text(log,encoding='utf-8')
    result=dict(name=label,root=str(root),command=cmd,exit=p.returncode,wall_seconds=time.perf_counter()-start,
        fault=fault,node=str(NODE))
    (OUT/(label+'.json')).write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)
    return result,log
def suite(label,root):
    r,log=execute(label,root,['tests','tests_apparatus'])
    assert r['exit']==0 and re.search(r'204 passed',log),log
    return r
def faults():
    rows=[]
    for name,(test,message) in CASES.items():
        row=dict(fault=name,test=test,intended_failure=message)
        for colour in ('RED','GREEN'):
            r,log=execute(name+'-'+colour,T,['tests_apparatus/test_b1_operator.py::'+test],name if colour=='RED' else None)
            errors='\n'.join(line for line in log.splitlines() if re.match(r'^E\s+',line))
            good=(r['exit']==1 and message in errors and '1 failed' in log) if colour=='RED' else (r['exit']==0 and '1 passed' in log)
            row[colour]={**r,'intended':good}
            if not good:
                (OUT/'INCOMPLETE.json').write_text(json.dumps(rows+[row],indent=2));raise AssertionError((name,colour,log))
        rows.append(row)
    (OUT/'FAULT_MATRIX.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
    return dict(pairs=len(rows),all_intended=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    jobs=[pool.submit(suite,'worktree-suite',T),pool.submit(suite,'portable-suite',P),pool.submit(faults)]
    results=[job.result() for job in jobs]
(OUT/'RUNS.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
