"""Run only explicitly authorized component regression/fault suites."""
import argparse,hashlib,json,os,pathlib,shutil,subprocess,sys,time
R=pathlib.Path(__file__).resolve().parents[1]
D=R/'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
OUT=R/'exports/2026-09-26-A5-clock-correction'
PORTABLE=OUT/'portable/Loom_P_Clock_Correction_Review_20260926'
def ident(p):
    with p.open('rb') as f:return {'sha256':hashlib.file_digest(f,'sha256').hexdigest(),'bytes':p.stat().st_size}
def snapshot(root):
    return {p.relative_to(root).as_posix():ident(p) for name in ('loom_p','loom_commissioning','tests','tests_apparatus')
            for p in sorted((root/name).rglob('*')) if p.is_file() and '__pycache__' not in p.parts}
def check_protected(root):
    before=json.loads((OUT/'PROTECTED_BEFORE.json').read_bytes())
    assert all(ident(root/p)['sha256']==v for p,v in before.items())
def env(root):
    e=os.environ.copy();e.update(PYTHONPATH=str(root),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
    for k in ('APPARATUS_FAULT','CORRECTION_FAULT','FINAL_FAULT','CLOCK_FAULT'):e.pop(k,None)
    return e
def suite(root,label):
    check_protected(root);before=snapshot(root)
    command=[sys.executable,'-B','-X','utf8','-m','pytest','tests','tests_apparatus','-q','-p','no:cacheprovider',
             '--basetemp',str(OUT/(label+'-temp')),'--junitxml',str(OUT/(label+'.xml'))]
    start=time.perf_counter()
    with (OUT/(label+'.log')).open('x',encoding='utf-8') as f:
        result=subprocess.run(command,cwd=root,env=env(root),stdout=f,stderr=subprocess.STDOUT,timeout=1200)
    assert before==snapshot(root);check_protected(root)
    receipt={'exit':result.returncode,'wall_seconds':time.perf_counter()-start,'command':command,
             'cwd':str(root),'code_tests_unchanged_by_execution':True,'source_inventory':before}
    (OUT/(label+'-receipt.json')).write_text(json.dumps(receipt,indent=2),encoding='utf-8')
    print((OUT/(label+'.log')).read_text()[-5000:],flush=True)
    assert result.returncode==0
def fault_suites():
    before=snapshot(D)
    for script,label in [('verify_apparatus.py','original-apparatus-faults'),('verify_corrections.py','prior-correction-faults'),
                         ('verify_final_corrections.py','prior-final-faults'),('verify_clock_scheduling.py','new-clock-faults')]:
        command=[sys.executable,'-B','-X','utf8',script,str(OUT/label)]
        start=time.perf_counter()
        with (OUT/(label+'.log')).open('x',encoding='utf-8') as f:
            result=subprocess.run(command,cwd=D,env=env(D),stdout=f,stderr=subprocess.STDOUT,timeout=1200)
        print(label,result.returncode,'wall',round(time.perf_counter()-start,2),flush=True)
        if result.returncode:print((OUT/(label+'.log')).read_text()[-5000:],flush=True)
        assert result.returncode==0
    assert snapshot(D)==before;check_protected(D)
    matrix=[]
    for label in ('original-apparatus-faults','prior-correction-faults','prior-final-faults','new-clock-faults'):
        matrix.extend(dict(suite=label,**x) for x in json.loads((OUT/label/'FAULT_MATRIX.json').read_bytes()))
    assert all(r['RED']['intended'] and r['GREEN']['intended'] for r in matrix)
    (OUT/'RED_GREEN_MATRIX.json').write_text(json.dumps(matrix,indent=2),encoding='utf-8')
    print('Verified fault/control pairs:',len(matrix),flush=True)
def prepare_portable():
    dest=PORTABLE/'developmental_ecology';dest.mkdir(parents=True,exist_ok=False)
    for name in ('loom_p','loom_commissioning','tests','tests_apparatus'):
        shutil.copytree(D/name,dest/name,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
    for name in ('configuration.json','requirements-lock.txt','verify_apparatus.py','verify_corrections.py','verify_final_corrections.py','verify_clock_scheduling.py'):
        shutil.copyfile(D/name,dest/name)
    shutil.copytree(D/'artifacts/prehistory-attempt-001',dest/'artifacts/prehistory-attempt-001')
    assert snapshot(D)==snapshot(dest);check_protected(dest)
    print('Portable source and preserved cache copied and verified.',flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=('worktree','faults','prepare-portable','portable'));a=p.parse_args().action
    if a=='worktree':suite(D,'FINAL_WORKTREE_SUITE')
    elif a=='faults':fault_suites()
    elif a=='prepare-portable':prepare_portable()
    else:suite(PORTABLE/'developmental_ecology','FINAL_PORTABLE_SUITE')
