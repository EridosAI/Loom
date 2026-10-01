"""Only three HOLD findings: subprocess RED/control evidence, no commissioning."""
import argparse,json,os,subprocess,sys,time
from pathlib import Path

CASES={}
for n in ('approved_execution','point','controller','until','identical'):
    CASES['duplicate-'+n]=(f'test_duplicate_approval_rejection[{n}]','DUPLICATE APPROVAL BREACH: '+n)
CASES['canonical-keys']=('test_non_string_canonical_key','CANONICAL KEY BREACH')
CASES['approval-alias']=('test_alias_and_semantic_mirror_rejection','APPROVAL ALIAS BREACH')
CASES['protocol-shadow']=('test_protocol_cannot_shadow_bound_fields','PROTOCOL SHADOW BREACH')
for n in ('waypoint_command','command_pair','privileged_input','time_due','observe_without_interference'):
    CASES['dispatch-'+n]=(f'test_actual_dispatch_is_checked[{n}]','EXECUTED DISPATCH BREACH: '+n)
for n in ('command','remainder','both','decision'):
    CASES['pending-'+n]=(f'test_pending_mutation_before_advance_and_save[{n}]','PENDING COMMAND BREACH: '+n)
CASES['decision-journal']=('test_saved_decision_journal_rejection','DECISION JOURNAL BREACH')

def main(output):
    root=Path(__file__).resolve().parent;out=Path(output).resolve();out.mkdir(parents=True,exist_ok=False);rows=[]
    for name,(test,message) in CASES.items():
        pair={'fault':name,'test':test,'intended_failure':message}
        for colour in ('RED','GREEN'):
            env=os.environ.copy();env.update(PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(root))
            for k in ('APPARATUS_FAULT','CORRECTION_FAULT','FINAL_FAULT'):env.pop(k,None)
            if colour=='RED':env['FINAL_FAULT']=name
            cmd=[sys.executable,'-B','-X','utf8','-m','pytest',f'tests_apparatus/test_final_corrections.py::{test}',
                 '-q','-p','no:cacheprovider','--basetemp',str(out/f'{name}-{colour}-temp')]
            start=time.perf_counter();r=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,encoding='utf-8',timeout=120)
            log=r.stdout+r.stderr;(out/f'{name}-{colour}.log').write_text(log,encoding='utf-8')
            valid=(r.returncode==1 and message in log and '1 failed' in log) if colour=='RED' else r.returncode==0 and '1 passed' in log
            pair[colour]={'exit':r.returncode,'intended':valid,'wall_seconds':time.perf_counter()-start,'command':cmd}
            print(name,colour,'verified' if valid else 'UNEXPECTED',flush=True)
            if not valid:
                (out/'INCOMPLETE.json').write_text(json.dumps(rows+[pair],indent=2),encoding='utf-8')
                raise RuntimeError(name+' did not reach intended '+colour)
        rows.append(pair)
    (out/'FAULT_MATRIX.json').write_text(json.dumps(rows,indent=2),encoding='utf-8')
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('output');main(p.parse_args().output)
