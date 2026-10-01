"""Read-only identity/record audit; never evolves an engine."""
import copy, gzip, hashlib, importlib.metadata, json, pathlib, subprocess, sys
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology'; E=D/'artifacts/apparatus-correction-20260924-01a0c405'
P=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405')
sys.path.insert(0,str(D))
from loom_commissioning import authority, controllers
from loom_commissioning.contract import apparatus_identity
from loom_p.records import code_identity
BASE='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
OLD='05abf60401d08f38750bca589b1c040e10513d7b'
def sha(data): return hashlib.sha256(data).hexdigest()
def git(*args): return subprocess.check_output(['git','-C',str(W),*args])
def write(name,obj): (E/name).write_text(json.dumps(obj,indent=2),encoding='utf-8')
files=git('ls-tree','-r','--name-only',BASE,'developmental_ecology/loom_p','developmental_ecology/tests').decode().splitlines()
identities={}
for name in files:
    original=git('show',BASE+':'+name); current=(W/name).read_bytes()
    projected=git('cat-file','--filters',BASE+':'+name)
    assert current==projected,name
    if '/loom_p/' in name: assert current==original,name
    identities[name]={'sha256':sha(current),'git_blob_sha256':sha(original),
        'identical_to_git_blob':current==original,'identical_baseline_checkout_bytes':True}
config='developmental_ecology/configuration.json'
blob=git('show',BASE+':'+config); projected=git('cat-file','--filters',BASE+':'+config)
actual=(W/config).read_bytes()
assert actual==projected==(P/config).read_bytes()
identities[config]={'working_sha256':sha(actual),'git_blob_sha256':sha(blob),
    'baseline_checkout_projection_sha256':sha(projected),'identical_baseline_checkout_bytes':True,
    'note':'Git text checkout is CRLF; raw committed blob is LF. Neither has been modified.'}
for name in ('tests_apparatus/test_apparatus.py','verify_apparatus.py'):
    raw=(D/name).read_bytes(); assert raw==git('show',OLD+':developmental_ecology/'+name)
    identities['developmental_ecology/'+name]={'sha256':sha(raw),'identical_to_05ab_blob':True}
tree=git('rev-parse',OLD+':EXP1-21').decode().strip()
assert tree=='f1b884a7ada4c806786d1530d76d446aac5d37b1'==git('rev-parse','HEAD:EXP1-21').decode().strip()
assert not git('diff',OLD,'--','EXP1-21','developmental_ecology/loom_p','developmental_ecology/configuration.json','developmental_ecology/tests')
prior=json.loads((D/'artifacts/apparatus-20260924-01a0c405/PRESERVATION_BEFORE.json').read_bytes())
for name,row in prior.items():
    p=P/name; assert p.stat().st_size==row['bytes'] and sha(p.read_bytes())==row['sha256'],name
write('UNCHANGED_P_AND_HISTORY.json',{'P':BASE,'prior_apparatus':OLD,'p_code':code_identity(),
    'identities':identities,'historical_EXP1_21_tree':tree,'prior_P_artifacts_checked':len(prior),'all_unchanged':True})
runtime=authority.runtime_identity(); packages={}
for name in ('numpy','scipy'):
    dist=importlib.metadata.distribution(name)
    records={str(p).replace('\\','/'):sha(pathlib.Path(dist.locate_file(p)).read_bytes()) for p in sorted(dist.files,key=str)
             if str(p).endswith(('.py','.pyd','.dll','.so','/METADATA','/RECORD'))}
    assert sha(authority.canonical(records))==runtime['packages'][name]['content_sha256']
    packages[name]=records
write('RUNTIME_FILE_IDENTITIES.json',{'runtime':runtime,'package_files':packages,'apparatus':apparatus_identity(),
    'executable_path':sys.executable,'execution':'real Windows desktop host; existing pinned venv; no installs'})
data=json.loads((D/'tests_apparatus/fixtures/review-boundary-input.json').read_bytes())
plan=[{'point':[6.,5.],'until':.1,'press_force':0.},{'point':[5.,6.],'until':.2,'press_force':0.}]
actual,cursor=controllers.waypoint_command(data,plan,0)
exact=copy.deepcopy(data); exact['time']=.1
expected,expected_cursor=controllers.waypoint_command(exact,plan,0)
final,_=controllers.waypoint_command(data,plan[:1],0)
assert cursor==expected_cursor==1 and actual.tolist()==expected.tolist() and not final.any()
write('EXACT_CLOCK_GREEN.json',{'saved_time':data['time'],'nominal_time':.1,'difference':.1-data['time'],
    'cursor':cursor,'command':actual.tolist(),'exact_boundary_command':expected.tolist(),'final_command':final.tolist(),
    'world_steps':0,'original_saved_stream_sha256':sha((E/'references/original-controller.jsonl.gz').read_bytes())})
manifests=[]
for p in E.rglob('manifest.json'):
    m=json.loads(p.read_bytes()); c=m.get('contract')
    if c:
        assert c['purpose']=='manufactured_fixture' and c['case_id'].startswith('fixture-') and c['duration_seconds']<=.6
        manifests.append({'path':str(p.relative_to(E)),'purpose':c['purpose'],'case':c['case_id'],'duration':c['duration_seconds'],'status':m['status']})
write('EXECUTED_RECORD_AUDIT.json',{'record_count':len(manifests),'all_manufactured':True,'commissioning_records':0,
    'prehistory_preparations':0,'scope':'All receipt-bearing records under this correction evidence root; tests also include detached/component checks without Run records.',
    'records':manifests})
print('Verified unchanged P/config/tests,',len(prior),'historical P artifacts, runtime identity and',len(manifests),'manufactured receipts.')
