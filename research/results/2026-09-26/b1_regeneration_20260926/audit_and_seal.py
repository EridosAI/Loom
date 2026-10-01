"""Independent file/canonical/diff audit and archive custody. No research imports."""
import collections,hashlib,json,os,pathlib,shutil,subprocess,zipfile
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926';D=W/'developmental_ecology'
OLD=ROOT/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02';OP=OLD/'B1_OPERATOR_REVIEW';OV=OLD/'B1_PRIVILEGED_EVALUATOR_HOLD'
E=ROOT/'exports/2026-09-26-B1-regenerated-352f73ff';PUB=E/'B1_OPERATOR_PACKET';PRIV=E/'B1_SEALED_EVALUATOR'
APP='352f73fffa6d9781eae8aa38e708a9a05669588f';HELD='45d71cd121f823368401b11c4a1010d509af3224f49168ad528653274d0e7543'
ID='IDENTITY-ONLY / REQUIRED BY APPARATUS CORRECTION';LIFE='OPERATOR-LIFECYCLE REPRESENTATION CHANGE REQUIRED BY CORRECTION'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_bytes())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode('utf-8')
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env)
assert git('rev-parse','HEAD').decode().strip()==APP and git('status','--porcelain')==b''
before=js(S/'PRESERVATION_BEFORE.json');assert all(sha(pathlib.Path(p))==h for p,h in before.items())
index=js(PUB/'CASE_AND_AUTHORITY_INDEX.json');rows=index['cases'];assert len(rows)==6
old_hashes={r['canonical_object_sha256'] for r in js(OP/'CASE_AND_AUTHORITY_INDEX.json')['cases']}
old_hashes.add(HELD)
scope=[];all_new=set();snapshot_hashes=set();manifest_hashes=set();cache_receipts=set()
for row in rows:
    case=row['case'];m=js(PRIV/'case-manifests'/(case+'.json'));old=js(OV/'case-manifests'/(case+'.json'))
    obj={k:v for k,v in m.items() if k!='execution_authority'}
    raw=(PRIV/'authority-objects'/(case+'.canonical.json')).read_bytes();assert raw==canonical(obj)
    assert js(PRIV/'authority-objects'/(case+'.json'))==obj
    h=hashlib.sha256(raw).hexdigest();assert h==row['canonical_authority_sha256'] and h not in old_hashes and h not in all_new
    all_new.add(h);assert m['execution_authority'] is None
    assert all(m[k]==old[k] for k in old if k not in ('apparatus','execution'))
    assert m['execution']['resources']==old['execution']['resources']
    assert m['execution']['procedure']['kind']==old['execution']['procedure']['kind'] and m['execution']['procedure']['stages']==old['execution']['procedure']['stages']
    p=m['execution']['procedure']['protocol'];q=old['execution']['procedure']['protocol']
    assert set(p)==set(q) and all(p[k]==q[k] for k in q if k!='bound_documents')
    assert all(sha(PUB/name)==value for name,value in p['bound_documents'].items())
    assert m['apparatus']['files']=={n:sha(D/'loom_commissioning'/n) for n in m['apparatus']['files']}
    init=m['initialization'];cache=pathlib.Path(init['cache_directory'])/'manifest.json'
    assert cache.is_file() and sha(cache)==init['cache_receipt_sha256'];cache_receipts.add(sha(cache))
    snap='B1-PAIR-INITIAL.snapshot.json.gz' if case.startswith('B1-') else case+'.snapshot.json.gz'
    assert sha(PRIV/'initial-states'/snap)==sha(OV/'initial-states'/snap)==row['initial_snapshot_sha256']
    snapshot_hashes.add(sha(PRIV/'initial-states'/snap));manifest_hashes.add(sha(PRIV/'case-manifests'/(case+'.json')))
    scope.append(dict(case=case,canonical_binding_verified=True,all_non_identity_case_fields_preserved=True,protocol_semantics_preserved=True,
        unchanged_prehistory_receipt_present=True,null_grant=True))
full=js(PRIV/'case-manifests/B1-FULL-RAW.json');hidden=js(PRIV/'case-manifests/B1-CHEMISTRY-HIDDEN.json')
assert {k for k in full if full[k]!=hidden[k]}=={'case_id','execution'}
assert {k for k in full['execution'] if full['execution'][k]!=hidden['execution'][k]}=={'display_intervention'}
assert full['execution']['display_intervention']=={'kind':'none'}
assert hidden['execution']['display_intervention']=={'kind':'chemistry_hidden','raw_flat_indices':[10,11,12,13],
    'representation':'omitted','implementation_sha256':sha(D/'loom_commissioning/operator_view.py')}
assert [r['case'] for r in js(PUB/'PC_AUTHORITY_IDENTITIES.json')['cases']]==['PC-LR','PC-MOTION','PC-CONTACT','PC-HOLD']
assert [r['case'] for r in js(PUB/'B1_SEALED_AUTHORITY_IDENTITIES.json')['cases']]==['B1-FULL-RAW','B1-CHEMISTRY-HIDDEN']

projection=js(PUB/'RESOURCE_PROJECTION.json');prior=js(OP/'RESOURCE_PROJECTION.json')
allowed_row_changes={'stream_planning_bound_bytes','retained_primary_planning_bytes'}
for r,o in zip(projection['cases'],prior['cases']):
    assert all(r[k]==o[k] for k in o if k not in allowed_row_changes)
    delta=(2*o['holds']+3)*1024
    assert r['stream_planning_bound_bytes']-o['stream_planning_bound_bytes']==delta
    assert r['retained_primary_planning_bytes']-o['retained_primary_planning_bytes']==delta
for key in prior:
    if key not in ('cases','combined_primary_copy_planning_bytes','uncertainty'):assert projection[key]==prior[key]
assert projection['combined_primary_copy_planning_bytes']==sum(r['retained_primary_planning_bytes'] for r in projection['cases'])*4
assert not js(PUB/'SEMANTIC_DIFF.json')['unexpected_semantic_changes']
zero=js(PUB/'ZERO_EXECUTION_RECORD.json')
assert not zero['forbidden_call_attempts']
for k in ('simulation_steps','controller_command_calls','Run_constructors','Engine_constructors','field_updates','prehistory_updates','simulation_RNG_draws','snapshot_deserializations','initial_sensor_transductions','positive_controls_executed','B1_trials_executed','replays','component_tests','live_services','execution_grants_created'):assert zero[k]==0
assert not any(name.startswith(('engine.py:','physics.py:','chemistry.py:','neural.py:','prehistory.py:','runner.py:','sensor_ui.py:','adapter.py:')) for name in zero['call_inventory'])

# Public data may contain opaque hashes and unchanged explicitly disclosed PC cards.
# No scalar B1 state, current manifest, snapshot or private evaluator payload is copied.
forbidden_keys={'position','orientation','angle','phase','initial_time','initial_index','initial_fields','initialization','stock','stocks','velocity','body','fields','sources','mover','pose'}
def public_keys(x):
    if isinstance(x,dict):
        assert not forbidden_keys.intersection(x),'Private physical key in public JSON'
        for v in x.values():public_keys(v)
    elif isinstance(x,list):
        for v in x:public_keys(v)
for p in PUB.glob('*.json'):public_keys(js(p))
public_names={p.name for p in PUB.iterdir() if p.is_file()}
assert not any(p.suffix=='.gz' for p in PUB.rglob('*'))
assert not {sha(p) for p in PUB.rglob('*') if p.is_file()}.intersection(snapshot_hashes|manifest_hashes|all_new)
assert sha(PUB/'POSITIVE_CONTROL_CARDS.md')==sha(OP/'POSITIVE_CONTROL_CARDS.md')
for p in PUB.glob('*.md'):
    text=p.read_text(encoding='utf-8')
    assert '](B1_SEALED_EVALUATOR' not in text and '](../B1_SEALED_EVALUATOR' not in text
    if p.name!='POSITIVE_CONTROL_CARDS.md':
        assert '(4.2, 3.8)' not in text and '(3, 3)' not in text

# Classify old-document disposition and every new authored document role. Historical
# evidence not current at the new checkpoint stays under the untouched old seal.
unchanged=js(PUB/'SEMANTIC_DIFF.json')['byte_identical_controlling_documents']
mapping={'STATIC_COMPATIBILITY_FINDINGS.json':'STATIC_COMPATIBILITY_REPORT.json','PREPARATION_CHECKS.json':'ZERO_EXECUTION_RECORD.json',
    'OPEN_ISSUE_B1_INTERFACE.md':'APPARATUS_DISPOSITION.md','HELD_REVIEW_IDENTITY.json':'PACKET_CUSTODY_IDENTITY.json',
    'DOCUMENTATION_REVISION.json':'SESSION_RECORD.md'}
changes=[]
for p in sorted(OP.iterdir()):
    if not p.is_file():continue
    if p.name in unchanged:
        assert sha(p)==sha(PUB/p.name)
        changes.append(dict(previous=p.name,current=p.name,changed=False,disposition='Byte-identical controlling design; no change.'))
    else:
        target=mapping.get(p.name,p.name)
        classes=[ID,LIFE] if p.name in ('OPERATOR_INSTRUCTIONS.md','DISPLAY_CONTRACT.json','README.md') else [ID]
        changes.append(dict(previous=p.name,current=target,changed=True,classifications=classes,
            disposition='Historical file preserved under old seal; current counterpart updates apparatus identity, implemented representation, static evidence or custody/status only.'))
new_names=public_names-{p.name for p in OP.iterdir() if p.is_file()}
new_names.update({'DOCUMENT_CHANGE_CLASSIFICATION.json','STATIC_FILE_AUDIT.json','PACKET_CUSTODY_IDENTITY.json','FILE_MANIFEST.json'})
for name in sorted(new_names):changes.append(dict(previous=None,current=name,changed=True,classifications=[ID,LIFE] if name=='SEMANTIC_DIFF.md' else [ID],
    disposition='New identity/custody/static-review wrapper or documentation of required apparatus correction; no additional case or physical semantics.'))
write(PUB/'DOCUMENT_CHANGE_CLASSIFICATION.json',dict(classifications=[ID,LIFE,'UNEXPECTED SEMANTIC CHANGE'],files=changes,
    current_private_files='Current private manifests/authority objects have the exact path-level delta in SEMANTIC_DIFF.json; current snapshots are byte-identical copies. Preserved evaluator design and historical archive are byte-identical; checkpoint-source bytes are identity-required source records. No hidden contents are disclosed here.',
    unexpected_semantic_changes=[]))
audit=dict(independent_file_only_audit=True,case_checks=scope,all_authorities_new_and_separate=True,same_complete_pair_state=True,
    unchanged_snapshot_files=len(snapshot_hashes),unchanged_prehistory_receipts=len(cache_receipts),all_resource_hard_limits_unchanged=True,
    resource_change_only_new_lifecycle_audit_allowance=True,unexpected_semantic_changes=0,public_bundle_contains_no_B1_scalar_state=True,
    public_bundle_contains_no_current_manifest_snapshot_or_canonical_execution_object=True,
    existing_disclosed_PC_cards_preserved_under_Jason_clarification=True,hidden_B1_evaluator_not_opened_to_operator=True,
    native_fidelity_unchanged=True,code_worktree_clean=True,historical_files_unchanged=len(before),
    launch_state='All grants null; no simulations/controllers/tests/live services executed; awaiting positive-control authorization only.',
    available_disk_bytes_at_static_audit=shutil.disk_usage(ROOT).free,repeat_disk_check_required_before_future_launch=True)
write(PUB/'STATIC_FILE_AUDIT.json',audit)
shutil.copyfile(pathlib.Path(__file__),PRIV/'STATIC_AUDIT_SOURCE.py')

public_payload={p.relative_to(PUB).as_posix():sha(p) for p in sorted(PUB.rglob('*')) if p.is_file()}
private_payload={p.relative_to(PRIV).as_posix():sha(p) for p in sorted(PRIV.rglob('*')) if p.is_file()}
custody=dict(kind='document-custody-only-NOT-execution-authority',historical_held_identity=HELD,P=index['P'],apparatus=APP,
    independent_disposition='FIT FOR B1 LAUNCH-PACKET REGENERATION, supplied by Jason',
    case_authorities=[dict(case=r['case'],canonical_authority_sha256=r['canonical_authority_sha256']) for r in rows],
    public_documents=public_payload,sealed_documents=private_payload,all_grants_null=True,zero_execution=True,
    next_decision='Jason authorization of positive controls only; B1 separately unauthorized')
write(PRIV/'PACKET_CUSTODY_OBJECT.json',custody)
(PRIV/'PACKET_CUSTODY_OBJECT.canonical.json').write_bytes(canonical(custody));custody_hash=sha(PRIV/'PACKET_CUSTODY_OBJECT.canonical.json')
assert custody_hash!=HELD and custody_hash not in all_new
def seal(folder):
    files={p.relative_to(folder).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(folder.rglob('*')) if p.is_file() and p.name!='FILE_MANIFEST.json'}
    write(folder/'FILE_MANIFEST.json',dict(files=files,excludes_self=True))
    archive=folder.with_suffix('.zip')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(folder.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(E).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for n,r in files.items():assert hashlib.sha256(z.read(folder.name+'/'+n)).hexdigest()==r['sha256']
        assert z.read(folder.name+'/FILE_MANIFEST.json')==(folder/'FILE_MANIFEST.json').read_bytes()
    return dict(archive=archive.name,sha256=sha(archive),bytes=archive.stat().st_size,payloads=len(files),verified=True)
private_archive=seal(PRIV)
write(PUB/'PACKET_CUSTODY_IDENTITY.json',dict(sha256=custody_hash,kind='Review/custody identity ONLY — not execution authority',
    historical_held_identity=HELD,case_authority_count=6,no_batch_authority=True,all_grants_null=True,
    sealed_archive_identity=private_archive,operator_instruction='Do not open the sealed evaluator archive; only its opaque identity is disclosed.'))
public_archive=seal(PUB)
assert all(sha(pathlib.Path(p))==h for p,h in before.items())
assert git('status','--porcelain')==b''
receipt=dict(P=index['P'],apparatus=APP,historical_held_identity=HELD,packet_custody_sha256=custody_hash,
    public=public_archive,sealed=private_archive,case_authorities=custody['case_authorities'],
    operator_blinding_preserved=True,zero_simulation_or_controller_execution=True,all_grants_null=True,
    unexpected_semantic_changes=0,next_decision='Positive controls only; no B1 authorization',no_code_or_git_writes=True)
write(E/'PACKAGE_RECEIPT.json',receipt);write(S/'PACKAGE_RECEIPT.json',receipt)
(E/'README.md').write_text('''# B1 regenerated launch-packet preparation

Open `B1_OPERATOR_PACKET/README.md` or the operator-only ZIP for safe review. It contains the four independent positive-control authority identities, unchanged disclosed practice cards, operator instructions, static checks, semantic diff and resource projection.

The separate sealed evaluator archive is custody material and must remain closed to Jason while he is the blinded operator. It is deliberately not linked here. No sealed contents belong in live navigation. The expanded sealed staging directory is not included in the workbench delivery.

No case is authorized or executed. Stop for Jason's authorization of the four positive controls only. The two B1 authorities remain separate and ungranted. The historical held packet is unchanged.
''',encoding='utf-8')
print(json.dumps(dict(public_archive=public_archive,packet_custody_sha256=custody_hash,case_authorities=custody['case_authorities'],
    unexpected_semantic_changes=0,zero_simulation_or_controller_execution=True,all_grants_null=True),indent=2))
