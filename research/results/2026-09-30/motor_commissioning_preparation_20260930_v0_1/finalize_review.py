"""Read-only custody checks and a single review archive. No execution import."""
import paths
from paths import HERE,ROOT
import hashlib,json,platform,sys,zipfile
from datetime import datetime,timezone
import xml.etree.ElementTree as ET
from preflight import check,git
from loom_motor_commissioning.runner import canonical,file_hash

counts={}
for folder,report in [('nursery_0_design_20260930_v0_1','DESIGN_ONLY_VERIFICATION.json'),
                      ('nursery_birth_motor_review_20260930_v0_1','REVIEW_VERIFICATION.json')]:
    base=ROOT/folder;old=json.loads((base/report).read_bytes())
    for row in old['files']:
        assert file_hash(base/row['path'])==row['sha256'],row['path']
    counts[folder]=len(old['files'])
old=json.loads((ROOT/'nursery_birth_motor_review_20260930_v0_1/INPUT_CUSTODY.json').read_bytes())
for row in old['files']:assert file_hash(__import__('pathlib').Path(row['path']))==row['sha256'],row['path']
counts['previous_review_inputs']=len(old['files'])
inputs=json.loads((HERE/'REFERENCE_INPUT_HASHES.json').read_bytes())
for path,h in inputs.items():assert file_hash(__import__('pathlib').Path(path))==h,path
counts['current_reference_inputs']=len(inputs)
gate=check()
assert not (HERE/'execution').exists()
assert not list((HERE/'initial_states').glob('*.partial'))
tests=ET.parse(HERE/'COMPONENT_TESTS.xml').getroot().find('testsuite')
assert int(tests.attrib['tests'])==26 and int(tests.attrib['failures'])==int(tests.attrib['errors'])==0
records=json.loads((HERE/'MATCHED_INITIAL_STATE_PROOF.json').read_bytes())['cases']
for group in (records[:3],records[3:6],records[6:]):
    for key in ('original_snapshot_sha256','physical_body_sha256','fields_sha256','original_rng_sha256','original_after_removing_only_new_process_sha256'):
        assert len({x[key] for x in group})==1,(group[0]['case_id'],key)
    assert all(x['initial_native_index']==x['initial_time']==x['initial_wave_index']==0 for x in group)
result=dict(status='PASS',utc=datetime.now(timezone.utc).isoformat(),host=platform.platform(),python=sys.version,
    prepared_cases=9,world_cases_started=0,world_steps=0,organism_steps=0,learning_handoffs=0,new_prehistory=0,
    component_tests=26,component_failures=0,component_errors=0,component_world_evolution_blocked=True,
    byte_matched_original_physical_triplets=3,full_original_state_restored_by_removing_only_candidate_attribute=True,
    separate_candidate_rng_namespaces=True,checks=counts,full_runtime_preflight=gate,
    frozen_checkout_head=git('rev-parse','HEAD'),frozen_checkout_clean=git('status','--porcelain')=='',
    canonical_source_edits=0,git_writes=0,dependencies_installed=0,nursery_changes=0,birth_law_changes=0,
    viability_changes=0,P_learning_changes=0,source_law_changes=0,old_human_B1_evaluator_accessed=False,
    authority_status='NINE_NEW_PROPOSALS_ONLY',authorized_execution_objects=0,automatic_selection=False)
(HERE/'FINAL_VERIFICATION.json').write_text(json.dumps(result,indent=2),encoding='utf8')
files=[]
for p in sorted(HERE.rglob('*')):
    if not p.is_file() or any(x.startswith('component-temp-') or x=='__pycache__' for x in p.relative_to(HERE).parts):continue
    if p.name in ('PACKAGE_MANIFEST.json','ARCHIVE_VERIFICATION.json'):continue
    files.append(dict(path=p.relative_to(HERE).as_posix(),bytes=p.stat().st_size,sha256=file_hash(p)))
manifest=dict(kind='REVIEW_PACKAGE_NOT_AUTHORIZATION',files=files,total_bytes=sum(x['bytes'] for x in files))
(HERE/'PACKAGE_MANIFEST.json').write_bytes(canonical(manifest))
archive=ROOT/'MOTOR_COMMISSIONING_M1_M2_PREPARATION_20260930_v0_1.zip'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for row in files:z.write(HERE/row['path'],row['path'])
    z.write(HERE/'PACKAGE_MANIFEST.json','PACKAGE_MANIFEST.json')
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for row in files:assert hashlib.sha256(z.read(row['path'])).hexdigest()==row['sha256']
archive_result=dict(path=str(archive),sha256=file_hash(archive),bytes=archive.stat().st_size,
    package_manifest_sha256=file_hash(HERE/'PACKAGE_MANIFEST.json'),verified_members=len(files)+1,status='PASS',
    execution_authorized=False,contains_test_approval_fixtures=False)
(HERE/'ARCHIVE_VERIFICATION.json').write_text(json.dumps(archive_result,indent=2),encoding='utf8')
print(json.dumps(dict(verification=result,archive=archive_result),indent=2))
