"""Record completed bounded verification; no engine calls."""
import hashlib,json,pathlib,shutil,subprocess,sys
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology'; E=D/'artifacts/apparatus-correction-20260924-01a0c405'
A=D/'artifacts/review-package-apparatus-correction-20260924-01a0c405/assembled'
git=lambda *args:subprocess.check_output(['git','-C',str(W),*args],text=True).strip()
record={'previous':'05abf60401d08f38750bca589b1c040e10513d7b','checkpoint':git('rev-parse','HEAD'),
    'branch':git('branch','--show-current'),'worktree':str(W),'status':git('status','--porcelain'),
    'worktree_suite':{'count':113,'seconds':52.18,'cwd':str(D),'log':'worktree-suite-001.log'},
    'portable_suite':{'count':113,'seconds':52.68,'cwd':str(A/'developmental_ecology'),'log':'portable-suite-001.log'},
    'command_template':[sys.executable,'-B','-X','utf8','-m','pytest','tests','tests_apparatus','-q','-p','no:cacheprovider','--basetemp','<fresh evidence-local directory>'],
    'old_fault_pairs':16,'new_fault_pairs':20,'all_intended_RED_then_GREEN':True,
    'original_old_runtime_counterexamples':2,'P_tests_unchanged':59,'original_apparatus_tests_unchanged':24,'new_tests':30,
    'no_commissioning_executed':True,'prehistory_preparations':0,'dependency_installations':0,
    'stop':'Independent review required. No apparatus fitness or commissioning authorization declared.'}
assert record['status']==''
for log in ('worktree-suite-001.log','portable-suite-001.log'): assert '113 passed' in (E/log).read_text(encoding='utf-8')
(E/'FINAL_VERIFICATION.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
for name in ('audit.py','custody.py','commit_correction.py','package_correction.py','final_record.py'):
    shutil.copyfile(pathlib.Path(__file__).parent/name,E/name)
print(json.dumps(record,indent=2))
