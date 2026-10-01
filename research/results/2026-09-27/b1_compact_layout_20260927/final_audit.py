"""Final read-only artifact audit plus task status records. No Loom imports."""
from pathlib import Path
import hashlib,json,zipfile,shutil,datetime,subprocess,os
R=Path(__file__).resolve().parent.parent;S=Path(__file__).resolve().parent
E=R/'exports/2026-09-27-B1-compact-1060a17e';PUB=E/'B1_OPERATOR_PACKET';PRIV=E/'B1_SEALED_EVALUATOR'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
for folder in (PUB,PRIV):
    listed=js(folder/'FILE_MANIFEST.json')['files']
    assert {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}==set(listed)|{'FILE_MANIFEST.json'}
    for n,v in listed.items():assert sha(folder/n)==v['sha256'] and (folder/n).stat().st_size==v['bytes']
with zipfile.ZipFile(E/'B1_OPERATOR_PACKET.zip') as z:
    assert z.testzip() is None
    assert set(z.namelist())=={p.relative_to(PUB).as_posix() for p in PUB.rglob('*') if p.is_file()}
    assert not any(x in n.lower() for n in z.namelist() for x in ('snapshot','restart','case-manifests','authority-objects','sealed_evaluator','native.jsonl','evaluator-manifest'))
    for n in z.namelist():assert hashlib.sha256(z.read(n)).hexdigest()==sha(PUB/n)
qa=js(PUB/'verification/BROWSER_LAYOUT_QA.json')
for n in ('fullWide','hiddenWide','fullNarrow','hiddenNarrow'):
    v=qa[n];assert v['pageHeight']==v['height'] and v['controlBottom']<v['height']
assert qa['fullNarrow']['width']==777 and qa['hiddenNarrow']['width']==777
assert qa['fullNarrow']['rows']==29 and qa['hiddenNarrow']['rows']==25
receipt=js(S/'DELIVERY_RECEIPT.json')
assert sha(E/'B1_OPERATOR_PACKET.zip')==receipt['public_zip_sha256']
assert sha(E/'B1_SEALED_EVALUATOR.zip')==receipt['sealed_archive_sha256']
W=Path(receipt['worktree']);env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
git=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(R/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
assert subprocess.check_output(git+['status','--porcelain'],env=env)==b''
assert subprocess.check_output(git+['rev-parse','HEAD'],env=env).decode().strip()==receipt['checkpoint']
committed=subprocess.check_output(git+['show','HEAD:developmental_ecology/loom_commissioning/sensor.html'],env=env)
assert hashlib.sha256(committed).hexdigest()==sha(W/'developmental_ecology/loom_commissioning/sensor.html')
for folder in (PUB,PRIV):
    for n,v in js(folder/'FILE_MANIFEST.json')['files'].items():assert sha(folder/n)==v['sha256']
B=R/'b1_execution_20260927'
state=js(B/'STATE.json');assert state['simulation_steps']==state['controller_commands']==0
shutil.copyfile(B/'STATE.json',B/'STATE_AT_INITIAL_PREPARATION.preserved.json')
state.update(status='ENDED AT ZERO STEPS / PRESERVED FOR LAYOUT CORRECTION',live_services=0,
 next_launch_authorized=False,evaluator_release_allowed=False,closure_record='ZERO_STEP_CLOSURE_AND_LAYOUT_AUTHORIZATION.json',
 revised_packet=str(PUB),updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
write(B/'STATE.json',state)
write(S/'FINAL_AUDIT.json',dict(public_file_hashes_verified=True,sealed_file_hashes_verified_without_disclosing_contents=True,
 public_zip_exact=True,public_zip_contains_no_B1_state_or_evaluator_artifacts=True,sealed_zip_not_opened=True,
 paired_opaque_identities_verified=True,working_tree_clean=True,committed_HTML_equals_verified_HTML=True,
 no_new_execution=True,authority_objects_ungranted=True,checkpoint=receipt['checkpoint'],public_zip_sha256=receipt['public_zip_sha256']))
print('Final audit passed: exact public archive, sealed custody hashes, clean checkpoint, correct 29/25-row compact views, no new launch.')
