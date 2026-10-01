import hashlib,json,subprocess,sys
from pathlib import Path

repo=Path(sys.argv[1]); old=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405')
evidence=repo/'developmental_ecology/artifacts/apparatus-20260924-01a0c405'
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
before=json.loads((evidence/'PRESERVATION_BEFORE.json').read_bytes())
for name,row in before.items():
    path=old/name
    assert path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],name
source=json.loads((evidence/'SOURCE_IDENTITIES.json').read_bytes())
for item in source['sources']: assert sha(Path(item['source']))==item['sha256'],item['source']
for name,value in source['p_runtime'].items(): assert sha(repo/'developmental_ecology/loom_p'/name)==value,name
unchanged=subprocess.check_output(['git','-C',str(repo),'diff','--name-only','6bc9683b54e4fa80136fe8534d7713e2a250a95f','--','developmental_ecology/loom_p','developmental_ecology/configuration.json','developmental_ecology/tests','EXP1-21'],text=True)
assert not unchanged,unchanged
result={'prior_artifact_files_checked':len(before),'prior_artifact_bytes_unchanged':True,
        'source_files_checked':len(source['sources']),'source_bytes_unchanged':True,
        'all_13_P_runtime_modules_unchanged':True,'configuration_and_prior_tests_git_unchanged':True,
        'EXP1_21_tree_unchanged':True,'audit_scope':'exact enumerated files and scoped Git comparison, not a claim about unrelated activity'}
(evidence/'PRESERVATION_AFTER.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
