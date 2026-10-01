"""File-only custody review; never imports the research packages or prints hidden state."""
import gzip,hashlib,json,pathlib,zipfile,sys
ROOT=pathlib.Path(__file__).resolve().parent.parent
E=ROOT/'exports'/('2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02' if '--revision-2' in sys.argv else '2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58')
PUB=E/'B1_OPERATOR_REVIEW';PRIV=E/'B1_PRIVILEGED_EVALUATOR_HOLD'
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
receipt=read(E/'PACKAGE_RECEIPT.json')
counts={}
for root,key in [(PUB,'public'),(PRIV,'privileged')]:
    fm=read(root/'FILE_MANIFEST.json')['files']
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    assert actual==set(fm)|{'FILE_MANIFEST.json'}
    for n,v in fm.items():assert sha(root/n)==v['sha256'] and (root/n).stat().st_size==v['bytes']
    archive=E/receipt[key]['archive'];assert sha(archive)==receipt[key]['sha256']
    with zipfile.ZipFile(archive) as z:
        assert set(z.namelist())==actual and z.testzip() is None
        for n in actual:assert z.read(n)==(root/n).read_bytes()
    counts[key]=len(fm)
held=read(PRIV/'HELD_REVIEW_OBJECT.json')
assert canonical(held)==(PRIV/'HELD_REVIEW_OBJECT.canonical.json').read_bytes()
assert hashlib.sha256(canonical(held)).hexdigest()==receipt['held_review_sha256']
for key,root in [('public_documents',PUB),('privileged_documents',PRIV)]:
    for n,h in held[key].items():assert sha(root/n)==h
index=read(PUB/'CASE_AND_AUTHORITY_INDEX.json')['cases']
assert len(index)==6
for row in index:
    m=read(PRIV/'case-manifests'/(row['case']+'.json'))
    obj=read(PRIV/'authority-objects'/(row['case']+'.json'))
    assert m['execution_authority'] is None
    assert obj=={k:v for k,v in m.items() if k!='execution_authority'}
    assert hashlib.sha256(canonical(obj)).hexdigest()==row['canonical_object_sha256']
    assert row['duration_seconds']==m['duration_seconds']
    assert (PRIV/'authority-objects'/(row['case']+'.canonical.json')).read_bytes()==canonical(obj)
full=read(PRIV/'case-manifests/B1-FULL-RAW.json')
hidden=read(PRIV/'case-manifests/B1-CHEMISTRY-HIDDEN.json')
assert full['initial_state']==hidden['initial_state'] and index[-1]['initial_snapshot_sha256']==index[-2]['initial_snapshot_sha256']
def attrs(obj):return {k:v for k,v in obj['attrs']['$dict']}
template=json.loads(gzip.decompress((PRIV/'references/initial-template.snapshot.json.gz').read_bytes()))
base=attrs(template['state'])
allowed={'body','raw'}
differences={}
for p in sorted((PRIV/'initial-states').glob('*.gz')):
    x=json.loads(gzip.decompress(p.read_bytes()));a=attrs(x['state'])
    changed={k for k in a if a[k]!=base[k]}
    assert changed<=allowed
    b0=attrs(base['body']);b1=attrs(a['body'])
    body_changes={k for k in b1 if b1[k]!=b0[k]}
    assert body_changes<={'position','angle'}
    differences[p.name]={'engine_fields':sorted(changed),'body_fields':sorted(body_changes)}
    assert a['time']==0 and a['native_index']==0
checks=read(PUB/'PREPARATION_CHECKS.json')
for k in ['worlds_constructed','Run_constructors','native_steps','field_steps','prehistory_steps','controller_command_calls','simulation_RNG_draws','human_trials','positive_control_demonstrations']:assert checks[k]==0
assert checks['initial_sensor_transductions']==5 and checks['forbidden_call_attempts']==[]
before=read(PRIV/'ORIGINALS_BEFORE.json');after=read(PRIV/'ORIGINALS_AFTER.json')
assert before==after and all(sha(pathlib.Path(p))==h for p,h in before.items())
priv=read(PRIV/'PRIVILEGED_EVALUATOR_MANIFEST.json')
public_text='\n'.join(p.read_text(encoding='utf-8') for p in PUB.rglob('*') if p.is_file())
for value in [priv['phase'],priv['exact_B1_body_pose']['angle']]:assert repr(value) not in public_text
assert not any(p.name.endswith('.gz') or 'snapshot' in p.name.lower() for p in PUB.rglob('*') if p.is_file())
resources=read(PUB/'RESOURCE_PROJECTION.json')
assert resources['combined_primary_copy_planning_bytes']<resources['stop_request_bytes']
result=dict(status='PASS — file-only audit',archive_payload_counts=counts,
    exact_manifests=6,null_execution_grants=6,identical_paired_initial_state=True,
    only_pose_and_initial_raw_changed=True,fixture_difference_paths=differences,
    protected_original_files_unchanged=len(before),canonical_review_hash=receipt['held_review_sha256'],
    public_exact_phase_and_heading_absent=True,public_snapshot_files_absent=True,
    simulation_steps=0,controller_calls=0,notes='No research imports; archive/JSON/hash checks only. Public prose/JSON fields were also manually reviewed. No claim of owner-resistant secrecy.')
out=E/'POST_SEAL_FILE_AUDIT.json'
with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2)
print(json.dumps({k:v for k,v in result.items() if k!='fixture_difference_paths'},indent=2))
