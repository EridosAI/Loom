"""New A-R1/A-R2 consequential fault/control pairs; no commissioning entry point."""
import argparse, json, os, subprocess, sys, time
from pathlib import Path

AUTHORITY=('implementation','constants','route','stage_sequence','contact_target','manual_fallback',
    'sensor_interface','intact_arm','fixed_adapter','deprivation','initial','prehistory','duration',
    'resources','runtime','procedure','replay_arm','request_rebind')

def main(output):
    root=Path(__file__).resolve().parent; out=Path(output).resolve(); out.mkdir(parents=True,exist_ok=False)
    cases={f'authority-{n}':(f'test_approved_execution_binding[{n}]','APPROVAL BINDING BREACH: '+n) for n in AUTHORITY}
    cases.update({'clock-transition':('test_exact_review_boundary','CLOCK BREACH: expired stage issued another hold'),
                  'clock-final':('test_final_stage_and_not_due_control','CLOCK BREACH: final stage still drives')})
    receipts=[]
    for name,(test,message) in cases.items():
        pair={'fault':name,'test':test,'intended_failure':message}
        for colour in ('RED','GREEN'):
            env=os.environ.copy(); env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'; env['PYTHONDONTWRITEBYTECODE']='1'; env['PYTHONPATH']=str(root)
            env.pop('APPARATUS_FAULT',None); env.pop('CORRECTION_FAULT',None)
            if colour=='RED': env['CORRECTION_FAULT']=name
            cmd=[sys.executable,'-B','-X','utf8','-m','pytest',f'tests_apparatus/test_corrections.py::{test}',
                 '-q','-p','no:cacheprovider','--basetemp',str(out/f'{name}-{colour}-temp')]
            started=time.perf_counter(); r=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,encoding='utf-8',timeout=90)
            log=r.stdout+r.stderr; (out/f'{name}-{colour}.log').write_text(log,encoding='utf-8')
            intended=(r.returncode==1 and message in log and 'failed' in log) if colour=='RED' else r.returncode==0 and 'passed' in log
            pair[colour]={'exit':r.returncode,'intended':intended,'wall_seconds':time.perf_counter()-started,'command':cmd}
            print(name,colour,'verified' if intended else 'UNEXPECTED',flush=True)
            if not intended:
                (out/'INCOMPLETE.json').write_text(json.dumps(receipts+[pair],indent=2),encoding='utf-8')
                raise RuntimeError(f'{name} {colour} did not reach intended check')
        receipts.append(pair)
    (out/'FAULT_MATRIX.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('output'); main(p.parse_args().output)
