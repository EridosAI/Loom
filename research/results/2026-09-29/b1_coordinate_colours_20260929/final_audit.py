"""Final static delivery audit. No Loom imports, snapshot loading or evaluator analysis."""
import hashlib,json,os,pathlib,socket,subprocess,zipfile
S=pathlib.Path(__file__).resolve().parent;R=S.parent
E=R/'exports/2026-09-29-B1-colour-labels-b684912e';PUB=E/'B1_OPERATOR_PACKET';PRIV=E/'B1_SEALED_EVALUATOR'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,indent=2,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
counts={}
for folder in (PUB,PRIV):
    listed=js(folder/'FILE_MANIFEST.json')['files']
    assert {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}==set(listed)|{'FILE_MANIFEST.json'}
    for n,v in listed.items():assert sha(folder/n)==v['sha256'] and (folder/n).stat().st_size==v['bytes']
    counts[folder.name]=len(listed)
receipt=js(S/'DELIVERY_RECEIPT.json')
assert sha(E/'B1_OPERATOR_PACKET.zip')==receipt['public_zip_sha256']
assert sha(E/'B1_SEALED_EVALUATOR.zip')==receipt['sealed_archive_sha256']
with zipfile.ZipFile(E/'B1_OPERATOR_PACKET.zip') as z:
    assert z.testzip() is None
    assert set(z.namelist())=={p.relative_to(PUB).as_posix() for p in PUB.rglob('*') if p.is_file()}
    assert not any(x in n.lower() for n in z.namelist() for x in ('snapshot','restart.json','case-manifests','authority-objects','sealed_evaluator','native.jsonl','evaluator-manifest'))
    for n in z.namelist():assert hashlib.sha256(z.read(n)).hexdigest()==sha(PUB/n)
# Both authorities remain ungranted; bind exact public contracts and opaque snapshot identity.
for row in js(PUB/'B1_SEALED_AUTHORITY_IDENTITIES.json')['cases']:
    m=js(PRIV/'case-manifests'/(row['case']+'.json'))
    assert m['execution_authority'] is None and row['execution_grant'] is None
    assert sha(PRIV/'authority-objects'/(row['case']+'.canonical.json'))==row['canonical_authority_sha256']
    assert sha(PRIV/'initial-states/B1-PAIR-INITIAL.snapshot.json.gz')==row['initial_snapshot_sha256']
    for n,h in m['execution']['procedure']['protocol']['bound_documents'].items():assert sha(PUB/n)==h
    assert m['duration_seconds']==30
assert js(PUB/'SEMANTIC_DIFF.json')['unexpected_semantic_changes']==[]
zero=js(PUB/'ZERO_EXECUTION_RECORD.json')
for n in ('simulation_steps','world_loads','Engine_constructors','Run_constructors','controller_commands','snapshot_deserializations','execution_grants_created','live_B1_services_started'):assert zero[n]==0
assert zero['forbidden_calls']==[]
verification=js(PUB/'verification/VERIFICATION.json')
assert verification['all_label_RGBs_match_renderer_within_8bit_rounding'] and verification['no_separate_legend']
assert verification['full_coordinates']==29 and verification['hidden_coordinates']==25
env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
for path,head in ((pathlib.Path(receipt['worktree']),receipt['checkpoint']),(R/'worktrees/loom-p-b1-apparatus-correction-20260926','1060a17e3dd14c6361f6f15c95bb58fad3110ffc')):
    cmd=['git','-c','safe.directory='+path.as_posix(),'-c','core.excludesFile='+(R/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(path)]
    assert subprocess.check_output(cmd+['status','--porcelain'],env=env)==b''
    assert subprocess.check_output(cmd+['rev-parse','HEAD'],env=env).decode().strip()==head
    source=subprocess.check_output(cmd+['show','HEAD:developmental_ecology/loom_commissioning/sensor.html'],env=env)
    assert hashlib.sha256(source).hexdigest()==sha(path/'developmental_ecology/loom_commissioning/sensor.html')
for n,v in js(S/'PACKET_PRESERVATION_BEFORE.json').items():assert sha(pathlib.Path(n))==v['sha256']
for inventory in js(S/'PRIOR_RUN_PRESERVATION_BEFORE.json').values():
    for n,v in inventory.items():assert sha(pathlib.Path(n))==v['sha256']
B=R/'b1_execution_20260929_restart_01';state=js(B/'STATE.json')
assert state['simulation_steps']==120 and state['controller_commands']==12 and state['live_services']==0
with socket.socket() as connection:
    connection.settimeout(2);assert connection.connect_ex(('127.0.0.1',56824))!=0
write(S/'FINAL_AUDIT.json',dict(public_file_hashes_verified=True,sealed_file_hashes_verified_without_disclosing_contents=True,
 public_zip_exact=True,public_zip_contains_no_B1_state_or_evaluator_artifacts=True,sealed_zip_not_opened=True,
 file_counts=counts,paired_opaque_identities_verified=True,both_worktrees_clean=True,committed_HTML_equals_verified_HTML=True,
 old_attempt_ended=True,old_service_stopped=True,all_prior_prefixes_unchanged=True,
 no_new_execution=True,authority_objects_ungranted=True,checkpoint=receipt['checkpoint'],public_zip_sha256=receipt['public_zip_sha256']))
print(json.dumps(dict(final_audit='passed',file_counts=counts,new_execution=0,old_prefix_steps=120,old_service_stopped=True,ungranted_authorities=receipt['authority_identities'])))
