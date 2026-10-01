"""Read-only audit of existing artifacts. All outputs stay beside this script."""
import ast, copy, gzip, hashlib, io, json, os, subprocess, sys, time, zipfile
from pathlib import Path

REPO=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
OLD=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405')
OUT=Path(__file__).resolve().parent
D=REPO/'developmental_ecology'
A=D/'artifacts/apparatus-20260924-01a0c405'
PACKAGE=D/'artifacts/review-package-apparatus-20260924-01a0c405'
ASSEMBLED=PACKAGE/'assembled'
DOC=REPO/'docs/developmental_ecology/p_apparatus_20260924'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
HEAD='05abf60401d08f38750bca589b1c040e10513d7b'
sys.path.insert(0,str(D))
os.environ['GIT_OPTIONAL_LOCKS']='0'
import numpy as np
from loom_p.records import code_identity,state_hash,strict_bytes,view
from loom_p.schema import Config,Streams
from loom_p.prehistory import load,field_law
from loom_commissioning.contract import apparatus_identity,INTACT,FIXED,EXTERNAL,make_manifest,validate_manifest
from loom_commissioning.initialization import from_verified_cache
from loom_commissioning.runner import load_restart
from loom_commissioning.validators import verify_segment,read_stream
from loom_commissioning.controllers import SensorHistory,observe_without_interference,privileged_input
from loom_commissioning import diagnostics,adapter

def sha(b):return hashlib.sha256(b).hexdigest()
def identity(path):
    b=path.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def read(path):return json.loads(path.read_bytes())
def emit(name,data):
    with (OUT/(name+'.json')).open('x',encoding='utf-8') as f:json.dump(data,f,indent=2)
    print(name,json.dumps(data)[:1000],flush=True)
def git(*args):
    return subprocess.check_output(['git','-c','safe.directory='+str(REPO),'-C',str(REPO),*args],env=os.environ,cwd=REPO)
def inventory(root):return {p.relative_to(root).as_posix():identity(p) for p in sorted(root.rglob('*')) if p.is_file()}

start=time.perf_counter()
target_before=inventory(D/'artifacts')
emit('TARGET_BEFORE',target_before)
head=git('rev-parse','HEAD').decode().strip();parent=git('rev-parse','HEAD^').decode().strip()
assert head==HEAD and parent==P
diff=git('diff','--name-status',P,HEAD).decode()
unchanged={p:not git('diff','--name-only',P,HEAD,'--',p).strip() for p in ['developmental_ecology/loom_p','developmental_ecology/configuration.json','developmental_ecology/tests','EXP1-21']}
assert all(unchanged.values())
prior_paths=git('ls-tree','--name-only',P).decode().splitlines()
exp_paths=[p for p in prior_paths if p=='EXP1-21']
trees={p:{ref:git('rev-parse',ref+':'+p).decode().strip() for ref in [P,HEAD]} for p in exp_paths}
patch=git('diff','--binary',P,HEAD)
assert patch==(ASSEMBLED/'APPARATUS.patch').read_bytes()
emit('GIT',{'head':head,'parent':parent,'branch':git('branch','--show-current').decode().strip(),'status':git('status','--porcelain').decode(),'diff':diff,'unchanged_paths':unchanged,'experiment_trees':trees,'patch':identity(ASSEMBLED/'APPARATUS.patch')})

runtime=read(A/'RUNTIME_RECORD.json'); source=read(DOC/'SOURCE_IDENTITIES.json'); checkpoint=read(ASSEMBLED/'CHECKPOINT.json')
pcode=code_identity();acode=apparatus_identity();c=Config()
assert pcode==runtime['p_code']==checkpoint['p_code'] and pcode['files']==source['p_runtime']
assert acode==runtime['apparatus_code']==checkpoint['apparatus']
assert c.identity()==runtime['configuration_semantic']
assert identity(D/'configuration.json')['sha256']==runtime['configuration_file_sha256']
selected=[]
for path in git('ls-files','developmental_ecology/loom_p','developmental_ecology/loom_commissioning','developmental_ecology/tests','developmental_ecology/tests_apparatus','developmental_ecology/configuration.json','docs/developmental_ecology/p_apparatus_20260924').decode().splitlines():
    current=(REPO/path).read_bytes();committed=git('show',HEAD+':'+path)
    assert current==committed or current.replace(b'\r\n',b'\n')==committed,path
    assert current==(ASSEMBLED/path).read_bytes(),path
    selected.append({'path':path,'bytes_equal_git':current==committed,'only_CRLF_difference':current!=committed})
emit('IDENTITIES',{'p':pcode,'apparatus':acode,'config_file':identity(D/'configuration.json'),'config_semantic':c.identity(),'selected_files_count':len(selected),'selected_files':selected})

preserved=read(A/'PRESERVATION_BEFORE.json');failures=[];ok=0
for path,expected in preserved.items():
    try:actual=identity(OLD/path)
    except Exception as e:failures.append({'path':path,'error':str(e)});continue
    if actual!=expected:failures.append({'path':path,'expected':expected,'actual':actual})
    else:ok+=1
emit('PRESERVATION',{'receipt_count':len(preserved),'verified':ok,'failures':failures,'before_receipt':identity(A/'PRESERVATION_BEFORE.json'),'after_receipt':read(A/'PRESERVATION_AFTER.json'),'scope':'Prior files reside in original engineering worktree; apparatus worktree contains copied cache and new evidence.'})

source_checks=[]
for row in source['sources']:
    expected={k:row[k] for k in ('bytes','sha256')}
    actual=identity(Path(row['source']));copied=identity(A/'references'/row['name'])
    assert actual==copied==expected,row['name']
    source_checks.append({'name':row['name'],'source':row['source'],**actual})
design=A/'references/Loom_P_Coupling_Commissioning_Design_20260923_2fb3ff84.zip'
assert identity(design)['sha256']==source['design_archive_sha256']
with zipfile.ZipFile(design) as z:
    names=z.namelist(); manifest=read(A/'DESIGN_ARCHIVE_MANIFEST.json')
    checked=[]
    for name,expected in manifest['files'].items():
        b=z.read(name);assert {'bytes':len(b),'sha256':sha(b)}==expected,name
        checked.append(name)
    reading=json.loads(z.read('READING_COPY_IDENTITIES.json'))
    for row in reading['files']:
        b=z.read('REFERENCES/'+row['path']);assert len(b)==row['bytes'] and sha(b)==row['sha256'],row['path']
    estimate=json.loads(z.read('COMPUTE_ESTIMATE.json'))
emit('SOURCES',{'current_and_packaged_sources':source_checks,'source_count':len(source_checks),'design_archive':identity(design),'design_payload_entries_verified':len(checked),'design_archive_entries':len(names),'reading_copies_verified':len(reading['files']),'reading_archive_anchors':{k:v for k,v in reading.items() if k!='files'}})

cache=D/'artifacts/prehistory-attempt-001';cache_manifest=read(cache/'manifest.json')
fields,phase,rng,prov=load(c,cache,life=0)
wrong_birth=[]
for birth in (1,2,3,4):
    expected_phase=float(Streams(c.master_seed,birth).draw('world-phase',(1,))[0]*2*np.pi)
    try:from_verified_cache(cache,birth)
    except ValueError as e:wrong_birth.append({'birth_id':birth,'expected_phase':expected_phase,'rejected':str(e)})
    else:raise AssertionError('Wrong birth cache accepted')
valid_engine,init=from_verified_cache(cache,0)
before=state_hash(valid_engine)
m=make_manifest(valid_engine,'A5',EXTERNAL,'waypoint',1200,purpose='commissioning',initialization=init)
validate_manifest(m,valid_engine)
assert before==state_hash(valid_engine) and valid_engine.native_index==0
emit('PREHISTORY',{'cache_files':inventory(cache),'field_array_sha256':sha(fields.tobytes()),'phase':phase,'steps':cache_manifest['steps_completed'],'reuse_verification':prov.get('reuse_verification'),'law_equal':field_law(c)==cache_manifest['law'],'wrong_birth_rejections':wrong_birth,'valid_life0_1200_manifest_validation_inert':True,'life0_state':before,'no_prepare_or_evolution_executed':True})

reconstruction=[];pause=[];observer=[]
records=A/'review-evidence/records'
for directory in sorted(records.iterdir()):
    continuous=directory/'continuous';first=directory/'first';second=directory/'second'
    for segment in (first,second,continuous):
        s0=time.perf_counter(); result=verify_segment(segment)
        result.update(directory=str(segment),wall_seconds=time.perf_counter()-s0)
        initial,session,manifest=load_restart(segment/'initial.restart.json.gz')
        final,finish,_=load_restart(segment/'final.restart.json.gz')
        result.update(initial_time=initial.time,final_time=final.time,initial_state=state_hash(initial),final_state=state_hash(final),initial_organism=state_hash(initial.organism),final_organism=state_hash(final.organism),initial_field=sha(initial.fields.tobytes()),final_field=sha(final.fields.tobytes()),initial_index=initial.native_index,final_index=final.native_index,initial_rng=initial.organism.rng.counters,final_rng=final.organism.rng.counters,manifest=manifest)
        reconstruction.append(result)
    f1,s1,m1=load_restart(first/'final.restart.json.gz');i2,si2,m2=load_restart(second/'initial.restart.json.gz')
    f2,s2,_=load_restart(second/'final.restart.json.gz');fc,sc,mc=load_restart(continuous/'final.restart.json.gz')
    equal={kind:read_stream(first/(kind+'.jsonl.gz'))+read_stream(second/(kind+'.jsonl.gz'))==read_stream(continuous/(kind+'.jsonl.gz')) for kind in ('native','wave','events','controller','diagnostics')}
    assert all(equal.values()) and state_hash(f1)==state_hash(i2) and state_hash(f2)==state_hash(fc)
    assert m1==m2==mc
    if m1['mode']==EXTERNAL:assert s1['hold_remaining']==si2['hold_remaining']==3
    pause.append({'mode':m1['mode'],'identical_joined_streams':equal,'pause_time':f1.time,'pause_index':f1.native_index,'pause_state':state_hash(f1),'resumed_initial_equal':True,'final_equal':True,'final_state':state_hash(f2),'hold_remaining':s1['hold_remaining'],'parent_manifest_hash':read(second/'manifest.json')['parent'],'expected_parent_manifest_hash':sha((first/'manifest.json').read_bytes())})
    initial,session,m=load_restart(continuous/'initial.restart.json.gz')
    history=SensorHistory.__new__(SensorHistory);history.__dict__=copy.deepcopy(session['sensor'])
    old=state_hash(initial)
    for _ in range(4):
        display=history.display();display['history'][-1]['raw'][0]+=1
        privileged=observe_without_interference(initial,privileged_input);privileged['position'][0]+=1
    assert state_hash(initial)==old
    observer.append({'mode':m['mode'],'calls':8,'state_hash_before':old,'state_hash_after':state_hash(initial),'native_index':initial.native_index,'time':initial.time,'returned_payload_mutations_inert':True})
emit('RECONSTRUCTION',{'segments':reconstruction,'unique_continuous_native_records':sum(x['native_records'] for x in reconstruction if x['directory'].endswith('continuous')),'all_segment_native_records':sum(x['native_records'] for x in reconstruction),'all_segment_wave_records':sum(x['wave_records'] for x in reconstruction)})
emit('PAUSE',pause);emit('OBSERVER',observer)

est=read(A/'RUNTIME_STORAGE_ESTIMATE.json');components=[]
for rate in est['measured_components']:
    match=next(p for p in records.iterdir() if read(p/'continuous/manifest.json')['contract']['mode']==rate['mode'])
    receipt=read(match/'continuous/manifest.json');stored=sum(p.stat().st_size for p in (match/'continuous').iterdir() if p.is_file())
    duration=receipt['final_time']-receipt['contract']['initial_time']
    assert stored==rate['stored_bytes'] and duration==rate['duration_seconds'] and receipt['wall_seconds']==rate['wall_seconds']
    assert receipt['uncompressed_bytes']==rate['uncompressed_record_bytes']
    assert stored/duration==rate['stored_bytes_per_simulated_second'] and receipt['wall_seconds']/duration==rate['wall_seconds_per_simulated_second']
    components.append(rate)
workload=sum(v['simulated_seconds'] for k,v in estimate['proposed_workloads'].items() if k!='total');assert workload==8960==est['future_world_ceiling_seconds']
hours=max(x['wall_seconds_per_simulated_second'] for x in components)*workload/3600
gb=max(x['stored_bytes_per_simulated_second'] for x in components)*workload/1e9
assert hours==est['conservative_component_rate_extrapolation']['machine_hours'] and gb==est['conservative_component_rate_extrapolation']['stored_GB']
emit('RESOURCE',{'components':components,'workload':estimate['proposed_workloads'],'total_seconds':workload,'projected_hours':hours,'projected_GB':gb,'one_duplicate_GB':gb*2,'interpretation':'Arithmetic extrapolation of short fixture rates, not observed or calibrated commissioning throughput.'})
target_after=inventory(D/'artifacts');assert target_before==target_after
emit('TARGET_UNCHANGED',{'before_files':len(target_before),'after_files':len(target_after),'all_bytes_unchanged':True,'git_status':git('status','--porcelain').decode(),'elapsed_seconds':time.perf_counter()-start})
