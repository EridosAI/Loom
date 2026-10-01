"""Create only the user-authorized local correction checkpoint."""
import json,pathlib,subprocess
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
E=W/'developmental_ecology/artifacts/apparatus-correction-20260924-01a0c405'
def git(*args): return subprocess.check_output(['git','-C',str(W),*args],text=True)
assert git('rev-parse','HEAD').strip()=='05abf60401d08f38750bca589b1c040e10513d7b'
assert git('branch','--show-current').strip()=='build/p-commissioning-apparatus-20260924-01a0c405'
assert not git('diff','--cached','--name-only').strip()
for name in ('worktree-suite-001.log','portable-suite-001.log'): assert '113 passed' in (E/name).read_text(encoding='utf-8')
for name,count in [('existing-faults-final-002',16),('new-faults-final-002',20)]:
    rows=json.loads((E/name/'FAULT_MATRIX.json').read_bytes())
    assert len(rows)==count and all(x[c]['intended'] for x in rows for c in ('RED','GREEN'))
assert json.loads((E/'PRESERVATION_AFTER.json').read_bytes())['all_unchanged']
assert json.loads((E/'UNCHANGED_P_AND_HISTORY.json').read_bytes())['all_unchanged']
paths=['developmental_ecology/loom_commissioning/'+n for n in ('authority.py','contract.py','controllers.py','runner.py')]
paths+=['developmental_ecology/tests_apparatus/test_corrections.py','developmental_ecology/tests_apparatus/fixtures/review-boundary-input.json',
    'developmental_ecology/verify_corrections.py','docs/developmental_ecology/p_apparatus_correction_20260924/CORRECTION_REPORT.md',
    'docs/developmental_ecology/p_apparatus_correction_20260924/LAW_CODE_TEST_MAP.md']
git('add','--',*paths)
assert set(git('diff','--cached','--name-only').splitlines())==set(paths)
assert not git('diff','--cached','--check').strip()
print(git('diff','--cached','--stat'))
print(git('commit','-m','Bind apparatus approval to full execution and enforce stage deadlines'))
assert not git('status','--porcelain').strip()
print('NEW CHECKPOINT',git('rev-parse','HEAD').strip())
