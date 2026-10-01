"""Static B1 packet regeneration. No snapshot deserialization, commands or simulation."""
import collections,copy,hashlib,json,os,pathlib,shutil,subprocess,sys,zipfile
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926';D=W/'developmental_ecology'
OLD=ROOT/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02'
OP=OLD/'B1_OPERATOR_REVIEW';OV=OLD/'B1_PRIVILEGED_EVALUATOR_HOLD'
E=ROOT/'exports/2026-09-26-B1-regenerated-352f73ff';PUB=E/'B1_OPERATOR_PACKET';PRIV=E/'B1_SEALED_EVALUATOR'
APP='352f73fffa6d9781eae8aa38e708a9a05669588f';P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
HELD='45d71cd121f823368401b11c4a1010d509af3224f49168ad528653274d0e7543'
ORDER=['PC-LR','PC-MOTION','PC-CONTACT','PC-HOLD','B1-FULL-RAW','B1-CHEMISTRY-HIDDEN']
HORIZONS=[4,4,6,10,30,30]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_bytes())
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def copyfile(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env)

assert git('rev-parse','HEAD').decode().strip()==APP and git('status','--porcelain')==b''
before={str(p):sha(p) for p in sorted(OLD.rglob('*')) if p.is_file()}
assert js(OP/'HELD_REVIEW_IDENTITY.json')['sha256']==HELD
assert sha(OV/'HELD_REVIEW_OBJECT.canonical.json')==HELD
for folder in (OP,OV):
    for name,record in js(folder/'FILE_MANIFEST.json')['files'].items():assert sha(folder/name)==record['sha256']
for archive in ('B1_OPERATOR_REVIEW.zip','B1_PRIVILEGED_EVALUATOR_HOLD.zip'):
    with zipfile.ZipFile(OLD/archive) as z:assert z.testzip() is None
assert sha(OLD/'B1_PRIVILEGED_EVALUATOR_HOLD.zip')==js(OP/'HELD_REVIEW_IDENTITY.json')['private_archive']['sha256']
if E.exists():
    # Only the empty directories from the documented import-guard stop may remain.
    assert E.resolve().is_relative_to((ROOT/'exports').resolve())
    assert set(E.iterdir())=={PUB,PRIV} and not list(PUB.iterdir()) and not list(PRIV.iterdir())
else:E.mkdir(parents=True)
PUB.mkdir(exist_ok=True);PRIV.mkdir(exist_ok=True)
write(S/'PRESERVATION_BEFORE.json',before)
probe=S/'read-write-probe.tmp';probe.write_bytes(b'B1 static preparation only');assert probe.read_bytes()==b'B1 static preparation only';probe.unlink()

# Trace every entered Loom function. Execution-bearing functions are disallowed,
# not replaced by stubs that could hide an accidental simulation attempt.
calls=collections.Counter();forbidden=[]
allowed={
 'authority.py':{'canonical','unique_json','strict_loads','object_pairs','execution_object','execution_sha256','file_identity','callable_identity','portable','_runtime_identity','runtime_identity','controller_identity','adapter_identity','make_execution','validate_protocol_fields','visit','validate_execution','read_approval'},
 'contract.py':{'digest','require','apparatus_identity','authorize_execution'},
 'records.py':{'code_identity','strict_bytes','Recorder'},
 'clock.py':{'grid_steps','case_end','stage_ends','decision_clock','hold_steps','expected_time','clock_allowance','validate_physical_time'},
 'operator_view.py':{'display_identity','validate_intervention'},
 'controllers.py':{'SensorHistory'},
}
def profile(frame,event,arg):
    if event!='call':return
    p=pathlib.Path(frame.f_code.co_filename)
    if not p.is_relative_to(D):return
    name=frame.f_code.co_name;key=p.name+':'+name;calls[key]+=1
    if name=='<module>' or name.startswith('<'):return
    if name not in allowed.get(p.name,set()):
        forbidden.append(key);raise RuntimeError('Forbidden execution-bearing Loom call: '+key)
sys.setprofile(profile);sys.path.insert(0,str(D))
from loom_commissioning.authority import canonical,execution_object,execution_sha256,make_execution,validate_execution,runtime_identity,controller_identity
from loom_commissioning.contract import apparatus_identity,authorize_execution,P_CODE,CONFIG
from loom_commissioning.operator_view import display_identity
from loom_commissioning import clock
from loom_p.records import code_identity
assert code_identity()['sha256']==P_CODE

protected=js(W/'docs/developmental_ecology/p_b1_operator_correction_20260926/FINAL_PRESERVATION.json')
assert all(sha(D/n)==h for n,h in protected['byte_identical_files'].items())
for name in protected['byte_identical_files']:
    if name.startswith('loom_p') or name=='configuration.json':
        relative='developmental_ecology/'+name.replace('\\','/')
        assert git('hash-object','--path='+relative,str(D/name)).strip()==git('rev-parse',P+':'+relative).strip()

# Preserve these controlling designs byte for byte, including the disclosed PC cards.
# Jason clarified that existing positive-control disclosure is retained only for PCs.
unchanged=['POSITIVE_CONTROL_CARDS.md','OPERATOR_INTEGRITY_FORM.md','INTERPRETATION_TABLE.md','CONTROL_GATE.json','PROTOCOL_CONTRACT.json']
for name in unchanged:copyfile(OP/name,PUB/name)
display=js(OP/'DISPLAY_CONTRACT.json')
display['reviewed_checkpoint']=APP
identity=apparatus_identity()
display['reviewed_files']={n:identity['files'][n] for n in [*display['reviewed_files'],'operator_view.py']}
display['chemistry_hidden'].update(implemented_at_checkpoint=True,representation='Four chemistry coordinates omitted entirely from current and historical operator rows; 25 actual remaining values, schema 2. No numeric surrogate.',implementation_sha256=display_identity('chemistry_hidden')['implementation_sha256'])
display['prelaunch_gaps']=[]
display['operator_lifecycle']={
 'states':['prepared','paused','running','ended'],
 'prepared':'Explicit Start changes to PAUSED without a native step.',
 'paused':'Inspect permitted history and prepare one command; no simulated time, energy, field, neural/native or simulation RNG advancement.',
 'running':'One accepted current-token command executes the unchanged bounded hold. No overlapping or queued second command.',
 'after_hold':'PAUSED unless a terminal, deadline, resource, failure or withdrawal stop ends the case.',
 'ended':'Irreversible for this case. No resume, continuation, retry, replacement or extension.',
 'delayed_or_duplicate_request':'Consumed decision tokens are rejected. Browser never retries uncertain commands automatically.',
 'wall_resources':'Real deliberation consumes no bodily time but counts toward the unchanged administrative wall limit.'}
display['coordinate_counts']={'FULL-RAW':29,'CHEMISTRY-HIDDEN':25}
display['chemistry_unavailable_label']='CHEMISTRY UNAVAILABLE IN THIS CONDITION'
display['independent_disposition']='FIT FOR B1 LAUNCH-PACKET REGENERATION — supplied by Jason in this regeneration request'
write(PUB/'DISPLAY_CONTRACT.json',display)
recording=js(OP/'RECORDING_CONTRACT.json')
recording['current_checkpoint_limit']='Decision records contain complete permitted history, so history recording/validation still grows quadratically. Hidden operator input has 25 values per row; private raw sensor history retains all 29. Lifecycle audit adds bounded records; no fidelity reduction.'
write(PUB/'RECORDING_CONTRACT.json',recording)

old_index=js(OP/'CASE_AND_AUTHORITY_INDEX.json')['cases'];assert [r['case'] for r in old_index]==ORDER
old_manifests={n:js(OV/'case-manifests'/(n+'.json')) for n in ORDER}
current={};rows=[];manifest_diffs=[]
ID='IDENTITY-ONLY / REQUIRED BY APPARATUS CORRECTION'
LIFE='OPERATOR-LIFECYCLE REPRESENTATION CHANGE REQUIRED BY CORRECTION'
def leafdiff(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        result=[]
        for k in sorted(set(a)|set(b)):
            if k not in a or k not in b:result.append(path+'/'+k)
            else:result.extend(leafdiff(a[k],b[k],path+'/'+k))
        return result
    return [] if a==b else [path]
def category(path):
    if any(path.startswith(prefix) for prefix in ('/apparatus/','/execution/runtime/','/execution/controller/','/execution/adapter/','/execution/display_intervention/','/execution/procedure/protocol/bound_documents/')):return ID
    raise RuntimeError('UNEXPECTED SEMANTIC CHANGE at '+path)
for oldrow,seconds in zip(old_index,HORIZONS):
    name=oldrow['case'];old=old_manifests[name];m=copy.deepcopy(old)
    assert m['execution_authority'] is None and m['purpose']=='commissioning' and m['baseline']==P and m['p_code']==P_CODE and m['configuration']==CONFIG
    assert m['duration_seconds']==seconds and m['controller']=='sensor_human' and m['mode']=='external_controller'
    protocol=copy.deepcopy(old['execution']['procedure']['protocol'])
    for document,h in protocol['bound_documents'].items():
        assert sha(OP/document)==h
        protocol['bound_documents'][document]=sha(PUB/document)
    resources=old['execution']['resources']
    m['apparatus']=identity
    m['execution']=make_execution(m['mode'],m['controller'],plan=copy.deepcopy(old['execution']['procedure']['stages']),protocol=protocol,
        wall_limit=resources['wall_limit_seconds'],storage_limit=resources['storage_limit_bytes'],display='chemistry_hidden' if name=='B1-CHEMISTRY-HIDDEN' else 'none')
    validate_execution(m,complete=True)
    try:authorize_execution(m)
    except ValueError as error:assert str(error)=='commissioning execution is not authorized'
    else:raise AssertionError('Null grant unexpectedly permitted execution')
    assert clock.case_end(m)-m['initial_index']==seconds*100
    assert all(clock.hold_steps(m,i)==10 for i in range(m['initial_index'],clock.case_end(m),10))
    delta=leafdiff(old,m)
    manifest_diffs.extend(dict(case=name,path=path,classification=category(path)) for path in delta)
    # Restrictive comparison: no top-level semantic field may change, and protocol
    # changes are only opaque bound-document hashes, never actions or admission.
    assert all(m[k]==old[k] for k in old if k not in ('apparatus','execution'))
    assert m['execution']['resources']==old['execution']['resources']
    assert {k:v for k,v in protocol.items() if k!='bound_documents'}=={k:v for k,v in old['execution']['procedure']['protocol'].items() if k!='bound_documents'}
    snapshot='B1-PAIR-INITIAL.snapshot.json.gz' if name.startswith('B1-') else name+'.snapshot.json.gz'
    assert sha(OV/'initial-states'/snapshot)==oldrow['initial_snapshot_sha256']
    copyfile(OV/'initial-states'/snapshot,PRIV/'initial-states'/snapshot)
    obj=execution_object(m);h=execution_sha256(m)
    assert h!=oldrow['canonical_object_sha256'] and h!=HELD
    write(PRIV/'case-manifests'/(name+'.json'),m)
    write(PRIV/'authority-objects'/(name+'.json'),obj)
    (PRIV/'authority-objects'/(name+'.canonical.json')).write_bytes(canonical(obj))
    assert sha(PRIV/'authority-objects'/(name+'.canonical.json'))==h
    rows.append(dict(case=name,duration_seconds=seconds,native_ceiling=seconds*100,maximum_command_holds=seconds*10,
        operator_coordinates=25 if name=='B1-CHEMISTRY-HIDDEN' else 29,initial_state_sha256=m['initial_state'],initial_snapshot_sha256=oldrow['initial_snapshot_sha256'],
        canonical_authority_sha256=h,previous_held_object_sha256=oldrow['canonical_object_sha256'],execution_grant=None,
        execution_specification_validation=True,null_grant_rejected=True,
        disposition='PREPARED — SEPARATE JASON AUTHORIZATION REQUIRED',object_location='sealed evaluator custody; digest only disclosed'))
    current[name]=m
assert len({r['canonical_authority_sha256'] for r in rows})==6
full=current['B1-FULL-RAW'];hidden=current['B1-CHEMISTRY-HIDDEN']
assert {k for k in full if full[k]!=hidden[k]}=={'case_id','execution'}
assert {k for k in full['execution'] if full['execution'][k]!=hidden['execution'][k]}=={'display_intervention'}
assert full['initial_state']==hidden['initial_state'] and full['duration_seconds']==hidden['duration_seconds']==30
runtime=runtime_identity();human=controller_identity('sensor_human')
sys.setprofile(None)
assert not forbidden

# Copy exact historical evaluator material as a labeled sealed historical archive.
# No historic manifest is rewritten or represented as a new authorized manifest.
copyfile(OLD/'B1_PRIVILEGED_EVALUATOR_HOLD.zip',PRIV/'historical-held/B1_PRIVILEGED_EVALUATOR_HOLD.zip')
for name in ('PREDECLARED_INITIAL_FIXTURES.json','PRIVILEGED_EVALUATOR_MANIFEST.json','INITIAL_STATE_CHECKS.json','SOURCE_IDENTITIES.json'):
    copyfile(OV/name,PRIV/'preserved-design'/name)
for p in (OV/'positive-controls').rglob('*'):
    if p.is_file():copyfile(p,PRIV/'preserved-design/positive-controls'/p.relative_to(OV/'positive-controls'))
for package in ('loom_commissioning','loom_p'):
    for p in (D/package).iterdir():
        if p.is_file() and p.suffix in ('.py','.html'):copyfile(p,PRIV/'checkpoint-source'/package/p.name)
for name in ('configuration.json','requirements-lock.txt'):copyfile(D/name,PRIV/'checkpoint-source'/name)
copyfile(pathlib.Path(__file__),PRIV/'REGENERATION_SOURCE.py')

write(PUB/'CASE_AND_AUTHORITY_INDEX.json',dict(P=P,apparatus=APP,historical_held_review_identity=HELD,
    status='PREPARED / AWAITING POSITIVE-CONTROL AUTHORIZATION ONLY; B1 separately sealed and unexecuted',cases=rows,no_batch_authority=True))
write(PUB/'PC_AUTHORITY_IDENTITIES.json',dict(authorization_scope='Only the four individually identified positive controls, in declared order; no B1 authorization.',
    order=ORDER[:4],cases=rows[:4],all_not_executed=True,all_not_demonstrated=True,execution_grants=None))
write(PUB/'B1_SEALED_AUTHORITY_IDENTITIES.json',dict(authorization_scope='NOT covered by any positive-control authorization; separately sealed independent authorities.',
    order=ORDER[4:],cases=rows[4:],complete_pair_initial_state_identical=True,execution_grants=None,evaluation_release='After both trials have ended or the pair is explicitly abandoned; never between the pair.'))
write(PUB/'RUNTIME_AND_APPARATUS_IDENTITIES.json',dict(checkpoint=APP,P=P,apparatus=identity,runtime=runtime,sensor_human=human,
    git_branch=git('branch','--show-current').decode().strip(),worktree_clean=True))

# Bound estimates retain all prior durations, hard limits and fidelity. Only
# the newly implemented lifecycle stream is added; hidden-mode savings ignored.
projection=js(OP/'RESOURCE_PROJECTION.json')
for row in projection['cases']:
    n=row['holds'];overhead=(2*n+3)*1024
    row['prior_stream_planning_bound_bytes']=row['stream_planning_bound_bytes']
    row['operator_lifecycle_audit_rows_bound']=2*n+3
    row['operator_lifecycle_audit_bytes_per_row_allowance']=1024
    row['operator_lifecycle_audit_planning_bytes']=overhead
    row['stream_planning_bound_bytes']+=overhead;row['retained_primary_planning_bytes']+=overhead
projection['combined_primary_copy_planning_bytes']=sum(r['retained_primary_planning_bytes'] for r in projection['cases'])*projection['maximum_retentions']
projection['correction_estimate_basis']='Add (2*N+3)*1024 uncompressed bytes for the new private lifecycle audit stream. Preserve prior conservative history bounds for both modes, credit no chemistry omission saving, and keep existing snapshot/display allowances and exact hard resource limits.'
projection['corrected_interactive_overhead_measured']=False
projection['uncertainty']='A5 remains a physics/recording proxy, not measured interactive throughput. The corrected gateway copies and validates permitted histories and hashes lifecycle displays; polling, serialization and browser rendering add unmeasured work. Human deliberation is wall time only. No benchmark or controller executed for this estimate.'
projection['pc_only_totals']={'simulated_seconds':24,'native_steps':2400,'maximum_decisions':240,
    'A5_compute_proxy_seconds':sum(r['A5_compute_proxy_seconds'] for r in projection['cases'][:4]),
    'retained_primary_planning_bytes':sum(r['retained_primary_planning_bytes'] for r in projection['cases'][:4]),
    'deliberation_examples':[{'seconds_per_decision':t,'wall_minutes_excluding_unmeasured_UI_overhead':(sum(r['A5_compute_proxy_seconds'] for r in projection['cases'][:4])+240*t)/60} for t in (5,10,20)]}
assert projection['combined_primary_copy_planning_bytes']<projection['combined_new_artifact_cap_bytes']
write(PUB/'RESOURCE_PROJECTION.json',projection)

public_document_diffs=[]
for name,a,b in [('DISPLAY_CONTRACT.json',js(OP/'DISPLAY_CONTRACT.json'),display),('RECORDING_CONTRACT.json',js(OP/'RECORDING_CONTRACT.json'),recording),('RESOURCE_PROJECTION.json',js(OP/'RESOURCE_PROJECTION.json'),projection)]:
    for path in leafdiff(a,b):public_document_diffs.append(dict(document=name,path=path,classification=LIFE if name=='DISPLAY_CONTRACT.json' and path.startswith('/operator_lifecycle') else ID))
write(PUB/'SEMANTIC_DIFF.json',dict(old_held_identity=HELD,old_apparatus='68db2c581f07200966d699a4f55a65f9b96df1e9',new_apparatus=APP,
    classifications=[ID,LIFE,'UNEXPECTED SEMANTIC CHANGE'],manifest_changes=manifest_diffs,contract_and_estimate_changes=public_document_diffs,
    byte_identical_controlling_documents={name:sha(PUB/name) for name in unchanged},unexpected_semantic_changes=[],
    statement='All initial, physical, timing, resource-cap, action, admission, completion and interpretation fields preserved. Only source/runtime/UI identity bindings and implemented display/lifecycle representation updated; storage estimate adds required audit overhead.',
    positive_control_disclosure='Existing cards retained byte-identically per Jason clarification; applies only to disclosed controls, never B1 geometry.'))
write(PUB/'STATIC_COMPATIBILITY_REPORT.json',dict(checkpoint=APP,cases=[dict(case=r['case'],horizon_seconds=r['duration_seconds'],native_ceiling=r['native_ceiling'],
    maximum_command_holds=r['maximum_command_holds'],operator_coordinates=r['operator_coordinates'],pure_execution_specification_accepted=True,
    null_grant_rejected=True,unchanged_snapshot_sha256=r['initial_snapshot_sha256']) for r in rows],
    snapshot_deserializations=0,new_transductions=0,complete_pair_initial_state_identical=True,paired_semantic_difference='case identity and declared display deprivation only',
    P_configuration_world_unchanged=True,clock_correction_unchanged=True,all_case_semantic_fields_preserved=True,
    positive_control_criteria_preserved=True,hidden_state_publicly_disclosed=False,
    limit='Pure execution/clock/identity checks and unchanged snapshot-byte custody, not a repeated physical initial-state validation, operator demonstration, live UI test, simulation or execution grant.'))
write(PUB/'ZERO_EXECUTION_RECORD.json',dict(simulation_steps=0,controller_command_calls=0,Run_constructors=0,Engine_constructors=0,
    field_updates=0,prehistory_updates=0,simulation_RNG_draws=0,snapshot_deserializations=0,initial_sensor_transductions=0,
    positive_controls_executed=0,B1_trials_executed=0,replays=0,component_tests=0,live_services=0,
    execution_grants_created=0,new_independent_canonical_authority_objects=6,forbidden_call_attempts=forbidden,call_inventory=dict(sorted(calls.items())),
    enforcement='Profile allowlist on all entered Loom functions; only file/identity/runtime/schema and scalar clock arithmetic permitted. No execution-bearing module or function entered.',
    observation_scope='This regeneration task only. Prior apparatus component evidence is historical and was not rerun.'))
write(PUB/'STATIC_PREPARATION_NOTE.json',dict(prior_static_import_stop='The initial allowlist rejected the Recorder class-definition body during records module import. Inspection confirmed it only defines methods; no Recorder constructor, snapshot or world call occurred. The class-definition name was permitted and static preparation repeated.',
    production_changes=0,fixture_or_controller_retries=0,prior_world_or_controller_execution=0))
assert all(sha(pathlib.Path(p))==h for p,h in before.items())
assert git('status','--porcelain')==b''
write(PUB/'PRESERVATION.json',dict(historical_held_identity=HELD,historical_files_unchanged=len(before),historical_before_inventory_sha256=sha(S/'PRESERVATION_BEFORE.json'),
    copied_snapshots_byte_identical=5,shared_B1_snapshot_identical=True,code_worktree_clean=True,no_code_or_configuration_changes=True,no_git_writes=True,
    prior_P_config_world_clock_proof_sha256=sha(W/'docs/developmental_ecology/p_b1_operator_correction_20260926/FINAL_PRESERVATION.json')))
write(S/'STATIC_RECEIPT.json',dict(export=str(E),P=P,apparatus=APP,case_authorities=[dict(case=r['case'],sha256=r['canonical_authority_sha256']) for r in rows],
    unexpected_semantic_changes=0,zero_simulation_or_controller_execution=True))
print('Static regeneration complete: six new independent authority objects, six accepted pure specifications, six null grants rejected; zero world/controller execution. Hidden state not printed.')
