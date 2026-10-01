"""Read-only final correction preservation/identity audit. No engine advancement."""
import hashlib,json,pathlib,subprocess,sys
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405');D=W/'developmental_ecology'
E=D/'artifacts/apparatus-final-correction-20260925-01a0c405'
OLD='9d31e7902658b15762052a2a6a3d161d64338524';BASE='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
P=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(*args):return subprocess.check_output(['git','-C',str(W),*args])
def write(name,obj):(E/name).write_text(json.dumps(obj,indent=2),encoding='utf-8')
before=json.loads((E/'PRESERVATION_BEFORE.json').read_bytes())
for name,row in before.items():
    p=pathlib.Path(name);assert p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],name
old_p=json.loads((D/'artifacts/apparatus-20260924-01a0c405/PRESERVATION_BEFORE.json').read_bytes())
for name,row in old_p.items():
    p=P/name;assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],name
prior=json.loads((D/'artifacts/apparatus-correction-20260924-01a0c405/PRESERVATION_BEFORE.json').read_bytes())
for name,row in prior.items():
    p=pathlib.Path(name);assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],name
write('PRESERVATION_AFTER.json',{'this_pass_inventory':len(before),'prior_P_inventory':len(old_p),
    'prior_correction_inventory':len(prior),'all_size_hash_matches':True})
names=git('ls-tree','-r','--name-only',BASE,'developmental_ecology/loom_p','developmental_ecology/tests').decode().splitlines()
rows={}
for name in names:
    current=(W/name).read_bytes();blob=git('show',BASE+':'+name);projected=git('cat-file','--filters',BASE+':'+name)
    assert current==projected,name
    if '/loom_p/' in name:assert current==blob,name
    rows[name]={'working_sha256':sha(W/name),'git_blob_sha256':hashlib.sha256(blob).hexdigest(),'baseline_checkout_identical':True}
config='developmental_ecology/configuration.json';actual=(W/config).read_bytes()
assert actual==git('cat-file','--filters',BASE+':'+config)==(P/config).read_bytes()
rows[config]={'working_sha256':sha(W/config),'git_blob_sha256':hashlib.sha256(git('show',BASE+':'+config)).hexdigest(),
    'baseline_checkout_identical':True,'note':'Existing CRLF checkout versus LF Git blob; no normalization performed.'}
unchanged=['tests_apparatus/test_apparatus.py','tests_apparatus/test_corrections.py','tests_apparatus/fixtures/review-boundary-input.json',
    'verify_apparatus.py','verify_corrections.py','loom_commissioning/controllers.py','loom_commissioning/adapter.py',
    'loom_commissioning/contract.py','loom_commissioning/diagnostics.py','loom_commissioning/initialization.py','loom_commissioning/evaluation.py']
for name in unchanged:
    data=(D/name).read_bytes();blob=git('show',OLD+':developmental_ecology/'+name)
    assert data==blob or data==git('cat-file','--filters',OLD+':developmental_ecology/'+name),name
    rows['developmental_ecology/'+name]={'working_sha256':sha(D/name),'unchanged_from_9d31':True}
tree=git('rev-parse','HEAD:EXP1-21').decode().strip();assert tree=='f1b884a7ada4c806786d1530d76d446aac5d37b1'
assert not git('diff',OLD,'--','EXP1-21','developmental_ecology/loom_p','developmental_ecology/configuration.json','developmental_ecology/tests')
sys.path.insert(0,str(D))
from loom_p.records import code_identity
from loom_commissioning.contract import apparatus_identity,CONFIG
from loom_commissioning.authority import runtime_identity
old_runtime=json.loads((D/'artifacts/apparatus-correction-20260924-01a0c405/RUNTIME_FILE_IDENTITIES.json').read_bytes())
assert runtime_identity()==old_runtime['runtime']
write('RUNTIME_DEPENDENCY_FILES.json',old_runtime['package_files'])
write('IDENTITIES.json',{'P':BASE,'previous_apparatus':OLD,'p_code':code_identity(),'configuration_semantic':CONFIG,
    'apparatus':apparatus_identity(),'runtime':runtime_identity(),'python_numpy_scipy_runtime_unchanged':True,
    'files':rows,'historical_EXP1_21_tree':tree,'all_unchanged_checks_passed':True})
receipts=[]
for p in E.rglob('manifest.json'):
    data=json.loads(p.read_bytes());m=data.get('contract')
    if m:
        assert m['purpose']=='manufactured_fixture' and m['case_id'].startswith('fixture-') and m['duration_seconds']<=.6
        receipts.append({'path':str(p.relative_to(E)),'case':m['case_id'],'duration':m['duration_seconds'],'status':data['status']})
write('EXECUTION_AUDIT.json',{'scope':'Receipt-bearing outputs under this pass, including explicitly labelled original RED reproductions.',
    'receipts':receipts,'count':len(receipts),'commissioning_receipts':0,'prehistory_preparations':0,'all_manufactured':True})
print('Verified',len(before),'current-preservation files,',len(old_p),'prior P files,',len(prior),'prior correction files and',len(receipts),'manufactured receipts.')
