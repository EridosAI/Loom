"""Read-only correction provenance and EXISTING-record reconstruction audit."""
from pathlib import Path
import ast,copy,gzip,hashlib,importlib.metadata,json,os,subprocess,sys,time,zipfile
import numpy as np
REPO=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
P_REPO=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405')
WORK=Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97')
OUT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent
assert OUT.is_relative_to(Path(__file__).resolve().parent)
OUT.mkdir(parents=True,exist_ok=True)
OLD_REVIEW=WORK/'exports/2026-09-24-p-apparatus-review-05abf604'
D=REPO/'developmental_ecology';A=D/'artifacts/apparatus-correction-20260924-01a0c405'
OLD_A=D/'artifacts/apparatus-20260924-01a0c405'
PACKAGE=D/'artifacts/review-package-apparatus-correction-20260924-01a0c405'
PORTABLE=Path(__file__).resolve().parent.parent/'portable'
BASE='05abf60401d08f38750bca589b1c040e10513d7b';P='6bc9683b54e4fa80136fe8534d7713e2a250a95f';HEAD='9d31e7902658b15762052a2a6a3d161d64338524'
sys.path.insert(0,str(D));os.environ['GIT_OPTIONAL_LOCKS']='0'
def sha(b):return hashlib.sha256(b).hexdigest()
def identity(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def read(p):return json.loads(Path(p).read_bytes())
def emit(name,obj):
 with (OUT/(name+'.json')).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
 print(name, json.dumps({k:v for k,v in obj.items() if not isinstance(v,(dict,list))}) if isinstance(obj,dict) else len(obj),flush=True)
def inventory(root):return {p.relative_to(root).as_posix():identity(p) for p in sorted(root.rglob('*')) if p.is_file()}
def git(*args):return subprocess.check_output(['git','-c','safe.directory='+str(REPO),'-C',str(REPO),*args],cwd=REPO,env=os.environ)
def check_inventory(items,root=None):
 results=[];fails=[]
 for name,expected in items.items():
  p=Path(name) if root is None else root/name
  try:actual=identity(p)
  except Exception as e:fails.append({'path':str(p),'error':str(e)});continue
  if actual!=expected:fails.append({'path':str(p),'expected':expected,'actual':actual})
  else:results.append(str(p))
 return {'count':len(items),'verified':len(results),'failures':fails}

started=time.perf_counter();before=inventory(D/'artifacts');emit('TARGET_BEFORE',before)
commit=git('rev-list','--parents','-n','1','HEAD').decode().split();assert commit==[HEAD,BASE]
diff=git('diff','--name-status',BASE,HEAD).decode();patch=git('diff','--binary',BASE,HEAD)
assert patch==(PORTABLE/'CORRECTION.patch').read_bytes()
checkpoint=read(PORTABLE/'CHECKPOINT.json');assert sha(patch)==checkpoint['patch_sha256'] and len(patch)==checkpoint['patch_bytes']
paths=['developmental_ecology/loom_p','developmental_ecology/configuration.json','developmental_ecology/tests','EXP1-21','developmental_ecology/tests_apparatus/test_apparatus.py','developmental_ecology/verify_apparatus.py']
unchanged={path:not git('diff','--name-only',BASE,HEAD,'--',path).strip() for path in paths};assert all(unchanged.values())
refs=[P,BASE,HEAD];trees={r:git('rev-parse',r+':EXP1-21').decode().strip() for r in refs};assert set(trees.values())=={'f1b884a7ada4c806786d1530d76d446aac5d37b1'}
for r in [P,BASE]:git('merge-base','--is-ancestor',r,HEAD)
emit('GIT',{'head':HEAD,'parent':BASE,'P':P,'branch':git('branch','--show-current').decode().strip(),'status':git('status','--porcelain').decode(),'diff':diff,'unchanged':unchanged,'EXP1_21_trees':trees,'patch_sha256':sha(patch),'patch_bytes':len(patch),'prior_checkpoints_ancestors':True})

from loom_p.records import code_identity,state_hash,strict_bytes,view
from loom_p.schema import Config,Streams
from loom_p.prehistory import load
from loom_commissioning import authority,adapter,diagnostics
from loom_commissioning.contract import apparatus_identity,EXTERNAL,FIXED
from loom_commissioning.runner import load_restart
from loom_commissioning.validators import verify_segment,read_stream
from loom_commissioning.initialization import from_verified_cache
pcode=code_identity();acode=apparatus_identity();runtime_record=read(A/'RUNTIME_FILE_IDENTITIES.json');unchanged_record=read(A/'UNCHANGED_P_AND_HISTORY.json')
assert pcode==unchanged_record['p_code'];assert pcode['sha256']=='63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9'
assert acode==runtime_record['apparatus']
selected=[]
for path in git('ls-files','developmental_ecology/loom_p','developmental_ecology/loom_commissioning','developmental_ecology/tests','developmental_ecology/tests_apparatus','developmental_ecology/configuration.json','developmental_ecology/verify_apparatus.py','developmental_ecology/verify_corrections.py','docs/developmental_ecology/p_apparatus_correction_20260924').decode().splitlines():
 raw=(REPO/path).read_bytes();blob=git('show',HEAD+':'+path)
 assert raw==blob or raw.replace(b'\r\n',b'\n')==blob,path
 assert raw==(PORTABLE/path).read_bytes(),path
 if '/loom_p/' in path:assert raw==git('show',P+':'+path),path
 selected.append({'path':path,'sha256':sha(raw),'git_blob_sha256':sha(blob),'CRLF_only_difference':raw!=blob})
assert (D/'configuration.json').read_bytes()==(P_REPO/'developmental_ecology/configuration.json').read_bytes()
emit('IDENTITIES',{'P':pcode,'apparatus':acode,'configuration_semantic':Config().identity(),'configuration_file':identity(D/'configuration.json'),'selected_file_count':len(selected),'selected_files':selected})

preserved_p=check_inventory(read(OLD_A/'PRESERVATION_BEFORE.json'),P_REPO)
preserved_previous=check_inventory(read(A/'PRESERVATION_BEFORE.json'))
prior_target=check_inventory(read(OLD_REVIEW/'provenance/TARGET_BEFORE.json'),D/'artifacts')
emit('PRESERVATION',{'prior_P':preserved_p,'prior_apparatus_review_design':preserved_previous,'prior_independent_422_anchor':prior_target,'builder_before':identity(A/'PRESERVATION_BEFORE.json'),'builder_after':read(A/'PRESERVATION_AFTER.json')})

runtime=authority.runtime_identity();assert runtime==runtime_record['runtime']
packages={}
for name,expected in runtime_record['package_files'].items():
 dist=importlib.metadata.distribution(name)
 current={str(p).replace('\\','/'):sha(Path(dist.locate_file(p)).read_bytes()) for p in sorted(dist.files,key=str) if str(p).endswith(('.py','.pyd','.dll','.so','/METADATA','/RECORD'))}
 assert current==expected,name
 assert sha(authority.canonical(current))==runtime['packages'][name]['content_sha256']
 packages[name]={'files_verified':len(current),'content_sha256':sha(authority.canonical(current))}
emit('RUNTIME',{'runtime':runtime,'packages':packages,'all_file_memberships_and_bytes_verified':True,'record':identity(A/'RUNTIME_FILE_IDENTITIES.json')})

source_refs={p.name:identity(p) for p in (A/'references').iterdir() if p.is_file()}
matches=[]
for p in (A/'references').iterdir():
 if not p.is_file() or p.name=='CORRECTION_REQUEST.txt':continue
 target_name='controller.jsonl.gz' if p.name=='original-controller.jsonl.gz' else p.name
 candidates=[q for q in OLD_REVIEW.rglob(target_name) if q.is_file()]
 exact=[str(q) for q in candidates if identity(q)==identity(p)]
 assert exact,p.name
 matches.append({'copy':p.name,'source_matches':exact,'identity':identity(p)})
fixture=read(D/'tests_apparatus/fixtures/review-boundary-input.json')
actions=read_stream(A/'references/original-controller.jsonl.gz')
assert fixture==actions[1]['inputs']
old_package=PORTABLE/'previous/Loom_P_Commissioning_Apparatus_Review_20260924.zip'
assert identity(old_package)['sha256']=='87f4dbde39a72559caf6045c7ac68a649d9691a000d1569af5d26b090a63b053'
review_package=PORTABLE/'previous/Loom_P_Independent_Apparatus_Review_05abf604_20260924.zip'
old_review_candidates=list(OLD_REVIEW.rglob(review_package.name));assert len(old_review_candidates)==1 and identity(review_package)==identity(old_review_candidates[0])
emit('SOURCES',{'reference_files':source_refs,'prior_review_exact_copies':matches,'exact_boundary_fixture_matches_original_second_action_inputs':True,'boundary_time':fixture['time'],'prior_builder_zip':identity(old_package),'prior_independent_zip':identity(review_package),'prior_independent_zip_source':str(old_review_candidates[0]),'correction_request_scope':'Delivered reference identity recorded; no separate original request path is declared in the package.'})

cache=D/'artifacts/prehistory-attempt-001';fields,phase,rng,prov=load(Config(),cache,life=0);rejects=[]
for birth in (1,2,3,4):
 try:from_verified_cache(cache,birth)
 except ValueError as e:rejects.append({'birth':birth,'rejected':str(e)})
 else:raise AssertionError('wrong birth cache accepted')
emit('PREHISTORY',{'files':inventory(cache),'field_sha256':sha(fields.tobytes()),'phase':phase,'wrong_birth_rejections':rejects,'prepared':False})

executed=[]
for p in A.rglob('manifest.json'):
 receipt=read(p);contract=receipt.get('contract')
 if contract is not None:
  assert contract['purpose']=='manufactured_fixture' and contract['case_id'].startswith('fixture-') and contract['duration_seconds']<=.6
  executed.append({'path':str(p.relative_to(A)),'case':contract['case_id'],'duration':contract['duration_seconds'],'status':receipt['status'],'schema':contract['schema']})
emit('EXECUTED_RECORD_AUDIT',{'record_count':len(executed),'all_manufactured':True,'commissioning_receipts':0,'records':executed,'claim_limit':'Only enumerated receipt-bearing artifacts; no inference about unrecorded historical actions.'})

selected_segments=[]
suite=A/'worktree-suite-001'
for fixture_dir in sorted(suite.iterdir()):
 if fixture_dir.name.startswith(('test_pause_resume_and_reconstr','test_boundary_resume_counts_an','test_final_boundary_resume_can')):
  selected_segments.extend(sorted(p.parent for p in fixture_dir.glob('*/manifest.json')))
assert len(selected_segments)==17,len(selected_segments)
results=[]
for segment in selected_segments:
 result=verify_segment(segment)
 initial,s,m=load_restart(segment/'initial.restart.json.gz');final,fs,_=load_restart(segment/'final.restart.json.gz')
 result.update(path=str(segment.relative_to(A)),initial_time=initial.time,final_time=final.time,initial_index=initial.native_index,final_index=final.native_index,initial_state=state_hash(initial),final_state=state_hash(final),initial_neural=state_hash(initial.organism),final_neural=state_hash(final.organism),initial_field=sha(initial.fields.tobytes()),final_field=sha(final.fields.tobytes()),execution_sha256=authority.execution_sha256(m),purpose=m['purpose'],case=m['case_id'],initial_hold_remaining=s['hold_remaining'],final_hold_remaining=fs['hold_remaining'])
 results.append(result)
emit('RECONSTRUCTION',{'segments':results,'segment_count':len(results),'native_records':sum(r['native_records'] for r in results),'wave_records':sum(r['wave_records'] for r in results),'events':sum(r['events'] for r in results),'all_reconstructed':True})

after=inventory(D/'artifacts');assert before==after
emit('FINAL_PRESERVATION',{'target_artifacts':len(after),'all_target_artifacts_unchanged':True,'git_status':git('status','--porcelain').decode(),'elapsed_seconds':time.perf_counter()-started})
