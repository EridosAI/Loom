"""Refresh only this pass's unsealed package; preserve intermediate evidence."""
import json,pathlib,shutil,sys
S=pathlib.Path(__file__).resolve().parent
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology';E=D/'artifacts/apparatus-final-correction-20260925-01a0c405'
A=D/'artifacts/final-review-20260925/assembled'
DOC=W/'docs/developmental_ecology/p_apparatus_final_correction_20260925'
def copy(p,q):q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
def tree(p,q):shutil.copytree(p,q,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
def refresh():
    archive=E/'attempt-001-source';archive.mkdir(exist_ok=False)
    tree(A/'developmental_ecology/loom_commissioning',archive/'loom_commissioning')
    for n in ('tests_apparatus/test_final_corrections.py','verify_final_corrections.py'):
        copy(A/'developmental_ecology'/n,archive/n)
    (archive/'README.md').write_text('Intermediate 142-check / 17-pair sources, retained exactly before the nested protocol shadow correction. Combine these with the unchanged P/configuration/dependency runtime from the final package only to inspect the intermediate records. These are historical evidence, not the final checkpoint. Final 143-check records are in review-evidence/final-suite-002. No commissioning is authorized.\n',encoding='utf-8')
    for n in ('loom_commissioning/authority.py','tests_apparatus/test_final_corrections.py','verify_final_corrections.py'):
        copy(D/n,A/'developmental_ecology'/n)
    for n in ('FINAL_CORRECTION_REPORT.md','LAW_CODE_TEST_MAP.md'):
        copy(S/n,DOC/n);copy(S/n,A/'docs/developmental_ecology/p_apparatus_final_correction_20260925'/n)
    for n in ('setup.py','old_red.py','audit.py','package_final.py','refresh_final.py'):copy(S/n,E/n)
    start=A/'START_HERE.md';text=start.read_text(encoding='utf-8')
    assert '17 new pairs' in text
    start.write_text(text.replace('17 new pairs','18 new pairs')+'\nFinal verification: 143 tests from the worktree and assembled package. Use the final `*-002` logs and `*-final-002` matrices. Final saved examples are in `review-evidence/final-suite-002`; intermediate examples use the separately retained `attempt-001-source` runtime.\n',encoding='utf-8')
    print('Preserved intermediate sources and refreshed final package code and review text.')
def records():
    assert '143 passed' in (E/'worktree-suite-002.log').read_text(encoding='utf-8-sig')
    dest=E/'review-evidence/final-suite-002';dest.mkdir(exist_ok=False)
    prefixes=('test_resume_binding_and_stage_','test_pending_mutation_before_a','test_saved_decision_journal_rej','test_pause_resume_and_reconstr')
    for p in sorted((E/'worktree-suite-002').iterdir()):
        if p.is_dir() and any(p.name.startswith(prefix) for prefix in prefixes) and not p.name.endswith('current'):
            tree(p,dest/p.name)
    print('Retained final saved examples and their full parent segment chains.')
if __name__=='__main__':globals()[sys.argv[1]]()
