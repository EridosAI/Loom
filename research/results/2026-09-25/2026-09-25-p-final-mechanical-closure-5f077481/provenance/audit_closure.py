"""Read only: exact final scope, preservation and existing record reconstruction."""
from pathlib import Path
import gzip,hashlib,importlib.metadata,json,os,subprocess,sys,time,zipfile
R=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
OLD_P=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405')
W=Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97')
O=Path(__file__).resolve().parent;V=O.parent/'portable';D=R/'developmental_ecology';A=D/'artifacts/apparatus-final-correction-20260925-01a0c405'
C=D/'artifacts/apparatus-correction-20260924-01a0c405';FIRST=D/'artifacts/apparatus-20260924-01a0c405'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f';BASE='9d31e7902658b15762052a2a6a3d161d64338524';HEAD='5f07748102cb5eaa302569c87efbae095050e9fe'
sys.path.insert(0,str(D));os.environ['GIT_OPTIONAL_LOCKS']='0'
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def read(p):return json.loads(Path(p).read_bytes())
def emit(name,obj):
 if (O/(name+'.json')).exists():
  assert read(O/(name+'.json'))==obj,name
  print(name+' unchanged existing receipt',flush=True);return
 with (O/(name+'.json')).open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2)
 print(name,flush=True)
def walk(root):
 def fail(e):raise e
 for directory,dirs,files in os.walk(root,onerror=fail):
  for name in sorted(files):yield Path(directory)/name
def inventory(root):return {p.relative_to(root).as_posix():ident(p) for p in walk(root)}
def check(items,root=None):
 for name,expected in items.items():assert ident(Path(name) if root is None else root/name)==expected,name
 return {'count':len(items),'all_size_hash_matches':True}
def git(*args):return subprocess.check_output(['git','-c','safe.directory='+str(R),'-C',str(R),*args],cwd=R,env=os.environ)
started=time.perf_counter();before=inventory(D/'artifacts');emit('TARGET_BEFORE',before)
assert git('rev-list','--parents','-n','1','HEAD').decode().split()==[HEAD,BASE]
patch=git('diff','--binary',BASE,HEAD);assert patch==(V/'FINAL_CORRECTION.patch').read_bytes()
cp=read(V/'CHECKPOINT.json');assert sha(patch)==cp['diff_sha256'] and len(patch)==cp['diff_bytes']
unchanged=['developmental_ecology/loom_p','developmental_ecology/configuration.json','developmental_ecology/tests','developmental_ecology/tests_apparatus/test_apparatus.py','developmental_ecology/tests_apparatus/test_corrections.py','developmental_ecology/tests_apparatus/fixtures/review-boundary-input.json','developmental_ecology/verify_apparatus.py','developmental_ecology/verify_corrections.py','developmental_ecology/loom_commissioning/controllers.py','developmental_ecology/loom_commissioning/contract.py','developmental_ecology/loom_commissioning/adapter.py','developmental_ecology/loom_commissioning/diagnostics.py','developmental_ecology/loom_commissioning/initialization.py','developmental_ecology/loom_commissioning/evaluation.py']
for p in unchanged:assert not git('diff','--name-only',BASE,HEAD,'--',p).strip(),p
refs=['d5f7efbe67193f215e52d95ca912db131a79f31c','f7eb6f27c661e3db193a4225b56a825d7e41739d',P,'05abf60401d08f38750bca589b1c040e10513d7b',BASE,HEAD]
trees={ref:git('rev-parse',ref+':EXP1-21').decode().strip() for ref in refs};assert set(trees.values())=={'f1b884a7ada4c806786d1530d76d446aac5d37b1'}
for ref in refs[:-1]:git('merge-base','--is-ancestor',ref,HEAD)
emit('GIT',{'head':HEAD,'parent':BASE,'branch':git('branch','--show-current').decode().strip(),'status':git('status','--porcelain').decode(),'diff':git('diff','--name-status',BASE,HEAD).decode(),'patch_bytes':len(patch),'patch_sha256':sha(patch),'unchanged_paths':unchanged,'EXP1_21':trees,'all_earlier_checkpoints_ancestors':True})
from loom_p.records import code_identity,state_hash
from loom_p.schema import Config
from loom_p.prehistory import load
from loom_commissioning import authority
from loom_commissioning.contract import apparatus_identity
from loom_commissioning.runner import load_restart
from loom_commissioning.validators import verify_segment
ids=read(A/'IDENTITIES.json');assert code_identity()==ids['p_code'] and apparatus_identity()==ids['apparatus'] and Config().identity()==ids['configuration_semantic']
files=[]
for path in git('ls-files','developmental_ecology/loom_p','developmental_ecology/loom_commissioning','developmental_ecology/tests','developmental_ecology/tests_apparatus','developmental_ecology/configuration.json','developmental_ecology/verify_apparatus.py','developmental_ecology/verify_corrections.py','developmental_ecology/verify_final_corrections.py','docs/developmental_ecology/p_apparatus_final_correction_20260925').decode().splitlines():
 b=(R/path).read_bytes();blob=git('show',HEAD+':'+path);assert b==blob or b.replace(b'\r\n',b'\n')==blob,path
 assert b==(V/path).read_bytes(),path
 if '/loom_p/' in path:assert b==git('show',P+':'+path),path
 files.append({'path':path,'sha256':sha(b),'git_blob_sha256':sha(blob),'CRLF_only_difference':b!=blob})
assert (D/'configuration.json').read_bytes()==(OLD_P/'developmental_ecology/configuration.json').read_bytes()
emit('IDENTITIES',{'P':code_identity(),'apparatus':apparatus_identity(),'configuration_file':ident(D/'configuration.json'),'configuration_semantic':Config().identity(),'selected_file_count':len(files),'files':files})
pres={'prior_P':check(read(FIRST/'PRESERVATION_BEFORE.json'),OLD_P),'prior_1908':check(read(C/'PRESERVATION_BEFORE.json')),'new_3902':check(read(A/'PRESERVATION_BEFORE.json')),'previous_independent_3106':check(read(W/'exports/2026-09-25-p-apparatus-correction-review-9d31e790/provenance/scoped-complete/TARGET_BEFORE.json'),D/'artifacts')}
emit('PRESERVATION',pres)
runtime=authority.runtime_identity();assert runtime==ids['runtime'];deps=read(A/'RUNTIME_DEPENDENCY_FILES.json');counts={}
for name,expected in deps.items():
 dist=importlib.metadata.distribution(name);actual={str(p).replace('\\','/'):sha(Path(dist.locate_file(p)).read_bytes()) for p in sorted(dist.files,key=str) if str(p).endswith(('.py','.pyd','.dll','.so','/METADATA','/RECORD'))}
 assert actual==expected;assert sha(authority.canonical(actual))==runtime['packages'][name]['content_sha256'];counts[name]=len(actual)
emit('RUNTIME',{'runtime':runtime,'dependency_counts':counts,'all_bytes_memberships_match':True})
copied=[]
for p in walk(V):
 relative=p.relative_to(V);source=R/relative
 if relative.parts[0] in ('developmental_ecology','docs') and source.is_file():
  assert p.read_bytes()==source.read_bytes(),str(relative);copied.append(str(relative))
previous_zip={p.name:ident(p) for p in walk(V) if p.suffix=='.zip'}
assert any(row['sha256']=='e261dbb9836a916f3ff4b6daa3ae8d9c21ea12194198d1ed63dfa7ee9b798a81' for row in previous_zip.values())
source_pairs=[]
old_review=W/'exports/2026-09-25-p-apparatus-correction-review-9d31e790'
for p in (D/'tests_apparatus/fixtures/final_review').iterdir():
 q=old_review/'canonical-001'/p.name
 matches=[str(q)] if ident(q)==ident(p) else [];assert matches,p.name
 source_pairs.append({'fixture':p.name,'identity':ident(p),'prior_review_sources':matches})
emit('PACKAGE_SOURCE_MATCH',{'target_files_matched':len(copied),'files':copied,'historical_archives':previous_zip,'old_exact_duplicate_inputs':source_pairs})
census=[]
for p in walk(A):
 if p.name=='manifest.json':
  m=read(p);c=m.get('contract')
  if c:
   assert c['purpose']=='manufactured_fixture' and c['case_id'].startswith('fixture-') and c['duration_seconds']<=.6
   census.append({'path':str(p.relative_to(A)),'case':c['case_id'],'duration':c['duration_seconds'],'status':m['status']})
assert len(census)==read(A/'EXECUTION_AUDIT.json')['count']
emit('RECORD_CENSUS',{'count':len(census),'commissioning_receipts':0,'all_manufactured_at_most_0_6_seconds':True,'records':census,'scope':'Enumerated receipt-bearing evidence only, including disclosed original REDs; no universal claim about unrecorded history.'})
segments=[];suite=A/'worktree-suite-002'
for d in suite.iterdir():
 if d.name.startswith(('test_pause_resume_and_reconstr','test_boundary_resume_counts_an','test_final_boundary_resume_can')):
  segments.extend(sorted(p.parent for p in d.glob('*/manifest.json')))
assert len(segments)==17
portable_records=V/'developmental_ecology/artifacts/apparatus-final-correction-20260925-01a0c405/review-evidence/final-suite-002'
segments.extend([portable_records/'test_resume_binding_and_stage_0/first',portable_records/'test_resume_binding_and_stage_0/resumed',portable_records/'test_saved_decision_journal_re0/good'])
results=[]
for path in segments:
 r=verify_segment(path);e,s,m=load_restart(path/'initial.restart.json.gz');f,fs,_=load_restart(path/'final.restart.json.gz')
 r.update(path=str(path),initial_time=e.time,final_time=f.time,initial_index=e.native_index,final_index=f.native_index,initial_state=state_hash(e),final_state=state_hash(f),final_neural=state_hash(f.organism),final_field=sha(f.fields.tobytes()),initial_remaining=s['hold_remaining'],final_remaining=fs['hold_remaining'])
 results.append(r)
bad=portable_records/'test_saved_decision_journal_re0/bad'
try:verify_segment(bad,replay=False)
except ValueError as ex:assert 'pending decision journal continuity mismatch' in str(ex);rejection=str(ex)
else:raise AssertionError('Delivered journal negative accepted')
emit('RECONSTRUCTION',{'segments':results,'accepted_segments':len(results),'native_records':sum(r['native_records'] for r in results),'wave_records':sum(r['wave_records'] for r in results),'events':sum(r['events'] for r in results),'packaged_negative_rejection':rejection,'negative_path':str(bad)})
comparisons=[]
for d in sorted(suite.glob('test_pause_resume_and_reconstr*')):
 old=C/'worktree-suite-001'/d.name/'continuous';new=d/'continuous';streams={}
 for name in ('native','wave','events','diagnostics','sensor','scientific_observations'):
  a=gzip.decompress((old/(name+'.jsonl.gz')).read_bytes());b=gzip.decompress((new/(name+'.jsonl.gz')).read_bytes());assert a==b,(d.name,name)
  streams[name]={'sha256':sha(b),'bytes':len(b),'rows':len(b.splitlines())}
 old_actions=[json.loads(x) for x in gzip.decompress((old/'controller.jsonl.gz').read_bytes()).splitlines()];new_actions=[json.loads(x) for x in gzip.decompress((new/'controller.jsonl.gz').read_bytes()).splitlines()]
 assert len(old_actions)==len(new_actions)
 for a,b in zip(old_actions,new_actions):assert all(b[k]==v for k,v in a.items())
 comparisons.append({'case':d.name,'streams_equal':streams,'old_controller_fields_preserved':True,'new_controller_fields':sorted(set(new_actions[0])-set(old_actions[0])) if old_actions else []})
emit('PREVIOUS_TRACES',{'modes':comparisons,'unchanged_streams':18,'all_old_controller_fields_preserved':True})
fields,phase,rng,prov=load(Config(),D/'artifacts/prehistory-attempt-001',life=0)
emit('PREHISTORY',{'field_sha256':sha(fields.tobytes()),'phase':phase,'cache':inventory(D/'artifacts/prehistory-attempt-001'),'prepared':False})
assert before==inventory(D/'artifacts')
emit('FINAL_PRESERVATION',{'target_artifact_files':len(before),'all_unchanged':True,'git_status':git('status','--porcelain').decode(),'elapsed_seconds':time.perf_counter()-started})
