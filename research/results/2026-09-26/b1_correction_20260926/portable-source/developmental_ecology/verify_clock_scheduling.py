"""Isolated scheduling fault/control pairs. No A5 execution or trajectory."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path

CASES={
    'old-absolute':('test_old_absolute_rejection_corrected','physical/native clock mismatch'),
    'old-stage':('test_independent_270_transition','STAGE OWNERSHIP BREACH'),
    'clock-corruption':('test_corrupt_physical_clock_rejected','TIMING CORRUPTION BREACH'),
    'grid-rounding':('test_off_grid_declared_stage_rejected','GRID ROUNDING BREACH'),
    'extra-decision':('test_no_extra_decision','EXTRA DECISION BREACH')}

def main(output):
    root=Path(__file__).resolve().parent;out=Path(output).resolve();out.mkdir(parents=True,exist_ok=False)
    rows=[]
    for name,(test,message) in CASES.items():
        row={'fault':name,'test':test,'intended_failure':message}
        for colour in ('RED','GREEN'):
            env=os.environ.copy();env.update(PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(root))
            for key in ('APPARATUS_FAULT','CORRECTION_FAULT','FINAL_FAULT','CLOCK_FAULT'):env.pop(key,None)
            if colour=='RED':env['CLOCK_FAULT']=name
            command=[sys.executable,'-B','-X','utf8','-m','pytest',f'tests_apparatus/test_clock_scheduling.py::{test}',
                     '-q','-p','no:cacheprovider','--basetemp',str(out/f'{name}-{colour}-temp')]
            start=time.perf_counter();result=subprocess.run(command,cwd=root,env=env,capture_output=True,text=True,encoding='utf-8',timeout=90)
            log=result.stdout+result.stderr;(out/f'{name}-{colour}.log').write_text(log,encoding='utf-8')
            intended=result.returncode==1 and '1 failed' in log and message in log if colour=='RED' else result.returncode==0 and '1 passed' in log
            row[colour]={'exit':result.returncode,'intended':intended,'wall_seconds':time.perf_counter()-start,'command':command}
            print(name,colour,'verified' if intended else 'UNEXPECTED',flush=True)
            if not intended:
                (out/'INCOMPLETE.json').write_text(json.dumps(rows+[row],indent=2));raise RuntimeError(name+' '+colour)
        rows.append(row)
    (out/'FAULT_MATRIX.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');main(p.parse_args().output)
