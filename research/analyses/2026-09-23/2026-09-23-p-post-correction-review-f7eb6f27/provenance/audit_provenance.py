"""Independent read-only review; writes evidence only beside this script."""
from pathlib import Path
import copy, gzip, hashlib, importlib.metadata, json, os, subprocess, sys, zipfile
import numpy as np

REPO=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405')
OUT=Path(__file__).resolve().parent
D=REPO/'developmental_ecology'
A=D/'artifacts'
COR=A/'correction-20260923-01a0c405'
PKG=A/'review-package-correction-20260923-01a0c405'
OLD='d5f7efbe67193f215e52d95ca912db131a79f31c'
NEW='f7eb6f27c661e3db193a4225b56a825d7e41739d'
sys.path.insert(0,str(D))
from loom_p.records import code_identity, load_snapshot, state_hash, state_bytes
from loom_p.schema import Config
from loom_p.prehistory import load as load_prehistory
from loom_p.inspector import Inspector
from verify_engineering_records import verify

def digest(b): return hashlib.sha256(b).hexdigest()
def file_identity(path):
    with path.open('rb') as f: h=hashlib.file_digest(f,'sha256').hexdigest()
    return dict(bytes=path.stat().st_size,sha256=h)
def read(path): return json.loads(path.read_text(encoding='utf-8-sig'))
def git(*args): return subprocess.check_output(['git','-C',str(REPO),*args],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def rows(root,kind):
    with gzip.open(root/(kind+'.jsonl.gz'),'rt',encoding='utf-8') as f:
        for line in f: yield json.loads(line)
def save(name,obj):
    if (OUT/name).exists():
        assert read(OUT/name)==json.loads(json.dumps(obj)),name
        return
    with (OUT/name).open('x',encoding='utf-8') as f: json.dump(obj,f,indent=2,ensure_ascii=False)

# Inventory before arithmetic so a later comparison proves our review preservation.
artifact_before={str(p.relative_to(A)):file_identity(p) for p in A.rglob('*') if p.is_file()}
preserved=read(COR/'PRESERVED_ARTIFACTS_BEFORE.json')
preservation_mismatches=[n for n,r in preserved.items() if file_identity(A/n)!=r]
assert not preservation_mismatches
old_evidence=read(REPO/'docs/developmental_ecology/p_engineering_20260921/EVIDENCE_MANIFEST.json')
assert all(file_identity(REPO/n)=={'bytes':r['bytes'],'sha256':r['sha256']} for n,r in old_evidence.items())
save('PRESERVATION.json',dict(preexisting_files=len(preserved),all_match=True,old_independent_inventory_files=len(old_evidence),old_inventory_all_match=True))

zip_path=PKG/'Loom_P_corrective_review_20260923.zip'
zip_identity=file_identity(zip_path)
assert zip_identity['sha256']==(PKG/'ZIP_SHA256.txt').read_text().split()[0]
with zipfile.ZipFile(zip_path) as z:
    inventory=json.loads(z.read('ARTIFACT_MANIFEST.json'))
    assert set(z.namelist())==set(inventory)|{'ARTIFACT_MANIFEST.json'}
    assert len(z.namelist())==len(set(z.namelist()))
    for n,r in inventory.items():
        b=z.read(n); assert len(b)==r['bytes'] and digest(b)==r['sha256'],n
    receipt=json.loads(z.read('CHECKPOINT_RECEIPT.json'))
    assert receipt==read(PKG/'CHECKPOINT_RECEIPT.json')
    patch=git('diff','--binary',OLD,NEW,'--','developmental_ecology','docs/developmental_ecology/p_correction_20260923')
    assert patch==z.read('CORRECTION.patch')
    oldzip=A/'review-package-20260922-01a0c405/Loom_P_build_review_20260922.zip'
    assert z.read('preserved_checkpoint/Loom_P_build_review_20260922.zip')==oldzip.read_bytes()
    tracked=git('ls-files','developmental_ecology','docs/developmental_ecology/p_engineering_20260921','docs/developmental_ecology/p_correction_20260923').decode().splitlines()
    byte_variants=[]
    for n in tracked:
        committed=git('show',NEW+':'+n); working=(REPO/n).read_bytes(); packaged=z.read(n)
        assert working==packaged,n
        if working!=committed:
            assert working.replace(b'\r\n',b'\n')==committed.replace(b'\r\n',b'\n'),n
            byte_variants.append(n)
    for case in ('birth_30s','nonzero_resume_1s','contact_ui_1s'):
        for p in (A/f'smoke-{case}-attempt-003').iterdir():
            assert z.read(p.relative_to(REPO).as_posix())==p.read_bytes()
save('PACKAGE.json',dict(**zip_identity,inventory_entries=len(inventory),members=len(inventory)+1,all_hashes_match=True,tracked_files=len(tracked),working_package_match=True,committed_crlf_only_variants=byte_variants,patch_sha256=digest(patch),patch_equals_git_diff=True,old_zip_identity=file_identity(oldzip),full_attempt003_evidence_included=True,receipt=receipt))

assert git('rev-parse','HEAD').decode().strip()==NEW
assert git('rev-parse',NEW+'^').decode().strip()==OLD
assert git('merge-base',OLD,NEW).decode().strip()==OLD
assert git('rev-parse',OLD+':EXP1-21')==git('rev-parse',NEW+':EXP1-21')
assert git('diff','--name-only',OLD,NEW,'--','docs/developmental_ecology/p_engineering_20260921')==b''
save('GIT.json',dict(head=NEW,parent=OLD,branch=git('branch','--show-current').decode().strip(),direct_single_parent=True,old_commit_reachable=True,archive_tree=git('rev-parse',NEW+':EXP1-21').decode().strip(),old_build_docs_unchanged=True,changed_files=git('diff','--name-status',OLD,NEW).decode().splitlines()))

runtime=read(REPO/'docs/developmental_ecology/p_correction_20260923/RUNTIME_RECORD.json')
oldruntime=read(REPO/'docs/developmental_ecology/p_engineering_20260921/RUNTIME_RECORD.json')
assert runtime['code']==code_identity()==receipt['code']
changed=[]
for name,h in runtime['code']['files'].items():
    new=git('show',NEW+':developmental_ecology/loom_p/'+name)
    old=git('show',OLD+':developmental_ecology/loom_p/'+name)
    assert digest(new)==h
    assert digest(old)==oldruntime['code']['files'][name]
    if new!=old: changed.append(name)
assert changed==['physics.py']
assert git('show',OLD+':developmental_ecology/configuration.json')==git('show',NEW+':developmental_ecology/configuration.json')
assert file_identity(D/'configuration.json')['sha256']==runtime['configuration_file_sha256']==oldruntime['configuration_file_sha256']
assert Config().identity()==runtime['configuration_sha256']==oldruntime['configuration_sha256']
deps={n:importlib.metadata.version(n) for n in runtime['dependencies']}
assert deps==runtime['dependencies']==oldruntime['dependencies']
sources=read(REPO/'docs/developmental_ecology/p_correction_20260923/SOURCE_IDENTITIES.json')
oldsources=read(REPO/'docs/developmental_ecology/p_engineering_20260921/SOURCE_IDENTITIES.json')
assert sources['sources']==oldsources['sources']
for r in sources['sources']:
    assert file_identity(Path(r['path']))=={'bytes':r['bytes'],'sha256':r['sha256']}
    if 'pinned_git_blob' in r: assert digest(git('cat-file','blob',r['pinned_git_blob']))==r['pinned_blob_sha256']
save('IDENTITIES.json',dict(runtime_code=code_identity(),changed_runtime_modules=changed,semantic_configuration=Config().identity(),configuration_working_sha256=file_identity(D/'configuration.json')['sha256'],configuration_committed_bytes_unchanged=True,dependencies=deps,source_count=len(sources['sources']),source_identities_unchanged=True,current_sources_and_pinned_blobs_match=True))

fields,phase,rng,prehistory=load_prehistory(Config(),A/'prehistory-attempt-001')
expected=read(COR/'PREHISTORY_REUSE.json')
assert digest(fields.tobytes())==expected['field_sha256']=='7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096'
assert phase==expected['phase']
save('PREHISTORY.json',dict(all_runtime_dependencies_except_physics_byte_unchanged=True,field_sha256=digest(fields.tobytes()),archive=file_identity(A/'prehistory-attempt-001/fields.npz'),phase=phase,loader_checks_passed=True,prehistory_generation_called=False))

results=[];comparison=[]
for case in ('birth_30s','nonzero_resume_1s','contact_ui_1s'):
    old=A/f'smoke-{case}-attempt-002';new=A/f'smoke-{case}-attempt-003'
    result=verify(new); results.append(result)
    om=read(old/'manifest.json');nm=read(new/'manifest.json')
    keys=('configuration','configuration_sha256','seed','life','simulated_seconds_cap','fixture')
    assert all(om[k]==nm[k] for k in keys)
    assert om['attempt']==2 and nm['attempt']==3
    delta={k:0. for k in ('reserves','position','angle','velocity','omega','commands','stocks','contact_rates')}
    changed_hashes=0;count=0;raw_changed=0
    for a,b in zip(rows(old,'native'),rows(new,'native'),strict=True):
        count+=1;changed_hashes+=a['organism_sha256']!=b['organism_sha256'];raw_changed+=a['raw']!=b['raw']
        for k in delta:delta[k]=max(delta[k],float(np.max(np.abs(np.asarray(a[k])-np.asarray(b[k])))))
    ow=list(rows(old,'wave'));nw=list(rows(new,'wave'))
    comparison.append(dict(case=case,native=count,different_neural_hashes=changed_hashes,different_raw_rows=raw_changed,max_absolute_differences=delta,wave_rows_equal=ow==nw,old_records=om['records'],new_records=nm['records'],matched_identity_fields=keys,initial_state_sha256_equal=om['initial_state_sha256']==nm['initial_state_sha256'],old_initial_wrapper_sha256=file_identity(old/'initial.snapshot.json.gz')['sha256'],new_initial_wrapper_sha256=file_identity(new/'initial.snapshot.json.gz')['sha256'],resume_identical=nm.get('resume_identical'),observer_noninterference=nm.get('observer_noninterference'),comparison_trajectory_seconds=nm.get('comparison_trajectory_seconds')))
    print('RECONSTRUCTED',case,result['native'],result['wave'],result['events'],flush=True)
save('RECONSTRUCTION.json',results);save('ATTEMPT_COMPARISON.json',comparison)

# Detached continuation of existing partial-wave snapshot, never Engine.step().
root=A/'smoke-nonzero_resume_1s-attempt-003'
mid=load_snapshot(root/'midwave.snapshot.json.gz');final=load_snapshot(root/'final.snapshot.json.gz')
assert mid.native_index==7 and abs(mid.time-.07)<1e-12
o=mid.organism;raw=mid.raw;ff=mid.fields.copy();count=0
for row in rows(root,'native'):
    if row['native_index']<=7:continue
    idx=row['native_index']-1
    command=o.native(raw,row['elapsed'],idx>0 and idx%round(mid.c.noise_refresh/mid.c.native_dt)==0)
    assert np.array_equal(command,row['commands'])
    if row['status']!='terminal' and row['native_index']%round(mid.c.wave_dt/mid.c.native_dt)==0:o.handoff(np.asarray(row['reserves']))
    assert digest(state_bytes(o))==row['organism_sha256']
    ff=mid.solver.step(ff,np.asarray(row['stocks']),row['time'],mid.phase,row['elapsed'],np.asarray(row['position']))
    raw=tuple(np.asarray(x) for x in row['raw']);count+=1
assert state_hash(o)==state_hash(final.organism) and np.array_equal(ff,final.fields)
save('MIDWAVE_RECONSTRUCTION.json',dict(saved_time=mid.time,saved_native_index=7,native_records_reconstructed=count,all_neural_hashes_match=True,final_fields_bit_identical=True,no_engine_steps=True))

app=Inspector();assert app.engine is not None and app.error is None
assert app.record_path.endswith('smoke-contact_ui_1s-attempt-003')
before=state_hash(app.engine);counts=copy.deepcopy(app.engine.organism.rng.counters)
app.observation();app.command('pause');app.command('replay',39);app.command('reconstruct');obs=app.observation()
assert state_hash(app.engine)==before and app.engine.organism.rng.counters==counts
assert app.session_steps==0 and app.engine.time==0. and app.recorder is None
save('OBSERVER.json',dict(live_before=before,live_after=state_hash(app.engine),random_counters_unchanged=True,time=app.engine.time,session_steps=0,record_path=app.record_path,reconstruction=obs['parameters']['provenance'],server_started=False))

artifact_after={str(p.relative_to(A)):file_identity(p) for p in A.rglob('*') if p.is_file()}
assert artifact_after==artifact_before
save('REVIEW_PRESERVATION.json',dict(files_checked=len(artifact_before),all_target_artifact_bytes_unchanged_during_review=True,added_artifact_files=0))
print('PROVENANCE AUDIT COMPLETE',len(artifact_before),'target artifact files unchanged',flush=True)
