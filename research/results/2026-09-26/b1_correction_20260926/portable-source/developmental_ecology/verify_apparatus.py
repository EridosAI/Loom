"""Bounded apparatus verification. No prehistory or commissioning trajectory entry point."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path

FAULTS={
 'identity':('test_manifest_identity','manifest/code identity mismatch'),
 'missing_native':('test_native_completeness','missing native record'),
 'phase':('test_field_phase','wrong field/mover phase'),
 'ledger':('test_accounting','source debit/body credit mismatch'),
 'input':('test_controller_allowlist','forbidden controller input'),
 'observer':('test_observer_noninterference','observer RNG/state interference'),
 'stop':('test_stop_reason','mislabelled stop reason'),
 'sensor_leak':('test_sensor_boundary','privileged data leakage into sensor-only interface'),
 'label':('test_external_label','external controller incorrectly labelled intact P'),
 'frozen':('test_frozen_persistence','frozen structural parameter changed'),
 'discarded':('test_discarded_update_has_no_later_effect','discarded structural update affected later output/state'),
 'duration':('test_duration_guard','manifest changed during run'),
 'extra_updates':('test_controller_hold_schedule','extra native/wave/random/field updates introduced by controller hold')}
for _name in ('extra_native','extra_wave','extra_random'):
    FAULTS[_name]=('test_controller_hold_schedule','extra native/wave/random state change from external hold')

def faults(output):
    output=Path(output); output.mkdir(parents=True,exist_ok=False); root=Path(__file__).parent
    receipts=[]
    for name,(test,expected) in FAULTS.items():
        pair={'fault':name,'test':test,'intended_failure':expected}
        for colour in ('RED','GREEN'):
            env=os.environ.copy(); env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1'; env['PYTHONDONTWRITEBYTECODE']='1'
            env['PYTHONPATH']=str(root); env.pop('APPARATUS_FAULT',None)
            if colour=='RED': env['APPARATUS_FAULT']=name
            cmd=[sys.executable,'-B','-X','utf8','-m','pytest',f'tests_apparatus/test_apparatus.py::{test}',
                 '-q','-p','no:cacheprovider','--basetemp',str(output/f'{name}-{colour}-temp')]
            start=time.perf_counter(); result=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,encoding='utf-8',timeout=90)
            text=result.stdout+result.stderr; (output/f'{name}-{colour}.log').write_text(text,encoding='utf-8')
            valid=(result.returncode==1 and expected in text and '1 failed' in text) if colour=='RED' else (result.returncode==0 and '1 passed' in text)
            pair[colour]={'exit':result.returncode,'intended':valid,'wall_seconds':time.perf_counter()-start,'command':cmd}
            print(name,colour,'verified' if valid else 'UNEXPECTED',flush=True)
            if not valid:
                (output/'INCOMPLETE.json').write_text(json.dumps(receipts+[pair],indent=2),encoding='utf-8')
                raise RuntimeError(f'{name} {colour} did not reach intended result')
        receipts.append(pair)
    (output/'FAULT_MATRIX.json').write_text(json.dumps(receipts,indent=2),encoding='utf-8')
    return receipts

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('output'); args=parser.parse_args()
    faults(args.output)
