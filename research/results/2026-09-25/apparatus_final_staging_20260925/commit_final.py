"""Create the one user-authorized local checkpoint; no remote operations."""
import json,pathlib,subprocess
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
E=W/'developmental_ecology/artifacts/apparatus-final-correction-20260925-01a0c405'
OLD='9d31e7902658b15762052a2a6a3d161d64338524'
def git(*args):return subprocess.check_output(['git','-C',str(W),*args])
assert git('rev-parse','HEAD').decode().strip()==OLD
assert git('branch','--show-current').decode().strip()=='build/p-commissioning-apparatus-20260924-01a0c405'
assert not git('diff','--cached','--name-only').strip()
v=json.loads((E/'FINAL_VERIFICATION.json').read_bytes())
assert all(x['passed']==143 for x in v['suites'].values())
assert [x['pairs'] for x in v['fault_matrices'].values()]==[16,20,18]
assert v['preservation']['all_size_hash_matches'] and v['portable_code_matches_worktree'] and v['no_commissioning_executed']
paths=['developmental_ecology/loom_commissioning/'+n for n in ('authority.py','runner.py','validators.py','sensor_ui.py','pending.py')]
paths+=['developmental_ecology/tests_apparatus/test_final_corrections.py','developmental_ecology/verify_final_corrections.py']
paths+=['developmental_ecology/tests_apparatus/fixtures/final_review/'+n for n in ('SYNTHETIC_duplicate-approved-execution_NO_EXECUTION.json','SYNTHETIC_duplicate-nested-waypoint_NO_EXECUTION.json')]
paths+=['docs/developmental_ecology/p_apparatus_final_correction_20260925/'+n for n in ('FINAL_CORRECTION_REPORT.md','LAW_CODE_TEST_MAP.md')]
changed=set(git('diff','--name-only').decode().splitlines()) | set(git('ls-files','--others','--exclude-standard').decode().splitlines())
assert changed==set(paths),(changed,set(paths))
git('diff','--check')
git('add','--',*paths)
assert set(git('diff','--cached','--name-only').decode().splitlines())==set(paths)
git('diff','--cached','--check')
print(git('commit','-m','Close three Loom P apparatus authority and resume findings').decode())
new=git('rev-parse','HEAD').decode().strip()
assert git('rev-parse','HEAD^').decode().strip()==OLD and not git('status','--porcelain').strip()
receipt={'previous':OLD,'checkpoint':new,'branch':git('branch','--show-current').decode().strip(),
         'worktree':str(W),'changed_files':paths,'clean_status':True,'one_new_local_commit':True,'remote_operations':0}
(E/'LOCAL_CHECKPOINT.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(receipt,indent=2))
