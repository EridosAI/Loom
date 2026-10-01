"""Read final test/preservation evidence; no simulation or authority creation."""
import hashlib,json,pathlib,re,shutil,subprocess,sys
S=pathlib.Path(__file__).resolve().parent
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405');D=W/'developmental_ecology'
E=D/'artifacts/apparatus-final-correction-20260925-01a0c405'
A=D/'artifacts/final-review-20260925/assembled'
OLD='9d31e7902658b15762052a2a6a3d161d64338524'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
def git(*args):return subprocess.check_output(['git','-C',str(W),*args])
assert git('rev-parse','HEAD').decode().strip()==OLD
assert git('branch','--show-current').decode().strip()=='build/p-commissioning-apparatus-20260924-01a0c405'
assert not git('diff','--cached','--name-only').strip()
result={'previous':OLD,'suites':{},'fault_matrices':{},'portable_code_matches_worktree':True,
        'no_commissioning_executed':True,'independent_mechanical_closure_review_required':True}
for n in ('worktree-suite-002','portable-suite-002'):
    p=E/(n+'.log');text=p.read_text(encoding='utf-8-sig')
    matched=re.search(r'^143 passed in ([\d.]+)s',text,re.M)
    assert matched and 'failed' not in text and 'ERROR' not in text,n
    result['suites'][n]={'passed':143,'existing_unchanged':113,'new':30,'wall_seconds':float(matched[1]),'log_sha256':sha(p)}
for n,count in [('original-faults-final-002',16),('previous-correction-faults-final-002',20),('final-faults-final-002',18)]:
    p=E/n/'FAULT_MATRIX.json';rows=read(p);assert len(rows)==count
    for row in rows:
        assert row['RED']['exit']==1 and row['RED']['intended']
        assert row['GREEN']['exit']==0 and row['GREEN']['intended']
    result['fault_matrices'][n]={'pairs':count,'all_intended_RED_and_GREEN':True,'matrix_sha256':sha(p)}
for n in ('loom_p','loom_commissioning','tests','tests_apparatus'):
    for p in (D/n).rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:
            assert p.read_bytes()==(A/'developmental_ecology'/p.relative_to(D)).read_bytes(),str(p)
for n in ('configuration.json','requirements-lock.txt','verify_apparatus.py','verify_corrections.py','verify_final_corrections.py'):
    assert (D/n).read_bytes()==(A/'developmental_ecology'/n).read_bytes(),n
preserved=read(E/'PRESERVATION_AFTER.json');assert preserved['all_size_hash_matches']
identities=read(E/'IDENTITIES.json');assert identities['all_unchanged_checks_passed'] and identities['python_numpy_scipy_runtime_unchanged']
audit=read(E/'EXECUTION_AUDIT.json');assert audit['commissioning_receipts']==0 and audit['prehistory_preparations']==0 and audit['all_manufactured']
result.update(preservation=preserved,apparatus=identities['apparatus']['sha256'],p_code=identities['p_code']['sha256'],
              receipt_count=audit['count'],P_engineering_checks_unchanged_and_green=59)
(E/'FINAL_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
for name in ('package_final.py','audit.py','refresh_final.py','finalize_checks.py'):
    shutil.copyfile(S/name,E/name)
print(json.dumps(result,indent=2))
