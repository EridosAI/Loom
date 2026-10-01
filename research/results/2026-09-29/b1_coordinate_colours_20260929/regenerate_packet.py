"""Static authority regeneration. Never deserialize snapshots or instantiate a world."""
import collections,copy,datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,zipfile
S=pathlib.Path(__file__).resolve().parent;R=S.parent
W=R/'worktrees/loom-p-b1-coordinate-colours-20260929';D=W/'developmental_ecology'
OLD=R/'exports/2026-09-27-B1-compact-1060a17e';OP=OLD/'B1_OPERATOR_PACKET';OV=OLD/'B1_SEALED_EVALUATOR'
E=R/'exports/2026-09-29-B1-colour-labels-b684912e';PUB=E/'B1_OPERATOR_PACKET';PRIV=E/'B1_SEALED_EVALUATOR'
B=R/'b1_execution_20260929_restart_01';run=B/'private/runs/B1-FULL-RAW'
APP='b684912eaf7811cd318ee94c77172aca790f3a0d';BASE='1060a17e3dd14c6361f6f15c95bb58fad3110ffc';P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8',newline='\n')
def cp(a,b):b.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(a,b)
def textfile(p,s):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s,encoding='utf-8',newline='\n')
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(R/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env)
def differences(a,b,path=''):
    if isinstance(a,dict) and isinstance(b,dict):
        return [p for k in sorted(set(a)|set(b)) for p in ([path+'/'+k] if k not in a or k not in b else differences(a[k],b[k],path+'/'+k))]
    return [] if a==b else [path]
def inventory(folder):return {str(p):dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(folder.rglob('*')) if p.is_file()}
assert git('rev-parse','HEAD').decode().strip()==APP and git('status','--porcelain')==b''
assert git('diff','--name-only',BASE,APP,'--','developmental_ecology').decode().splitlines()==['developmental_ecology/loom_commissioning/sensor.html']
closure=js(B/'PREFIX_CLOSURE_AND_COLOUR_LABEL_AUTHORIZATION.json')
assert closure['native_steps']==120 and closure['human_commands']==12 and closure['observed_lifecycle']=='ended'
assert js(B/'ENDED_SERVICE_STOP_RECEIPT.json')['ended_service_stopped'] is True
for n,v in js(B/'private/CLOSED_PREFIX_FILE_MANIFEST.json')['files'].items():
    assert sha(B/'private'/n)==v['sha256'] and (B/'private'/n).stat().st_size==v['bytes']
state=js(B/'STATE.json');assert (B/'STATE_AT_INITIAL_PREPARATION.preserved.json').exists()
assert sha(B/'STATE.json')==sha(B/'STATE_AT_INITIAL_PREPARATION.preserved.json')
state.update(status='ENDED AT 1.2 SECONDS / COMPLETE PREFIX PRESERVED FOR COLOUR-LABEL CORRECTION',live_services=0,
 simulation_steps=120,controller_commands=12,simulated_seconds=closure['simulated_seconds'],assistant_commands=0,
 next_launch_authorized=False,evaluator_release_allowed=False,closure_record='PREFIX_CLOSURE_AND_COLOUR_LABEL_AUTHORIZATION.json',
 updated_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
write(B/'STATE.json',state)
before=inventory(OLD)
prior_attempts=[R/'b1_execution_20260927',R/'b1_execution_20260929',B]
prior_runs={str(folder):inventory(folder/'private/runs/B1-FULL-RAW') for folder in prior_attempts}
for folder in (OP,OV):
    listed=js(folder/'FILE_MANIFEST.json')['files']
    assert {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}==set(listed)|{'FILE_MANIFEST.json'}
    for n,row in listed.items():assert sha(folder/n)==row['sha256'] and (folder/n).stat().st_size==row['bytes']
assert not E.exists();PUB.mkdir(parents=True);PRIV.mkdir()
write(S/'PACKET_PRESERVATION_BEFORE.json',before)
write(S/'PRIOR_RUN_PRESERVATION_BEFORE.json',prior_runs)

# Whitelist only schema, identity, null-grant rejection and scalar clock calls.
allowed={
 'authority.py':{'canonical','unique_json','strict_loads','object_pairs','execution_object','execution_sha256','file_identity','callable_identity','portable','_runtime_identity','runtime_identity','controller_identity','adapter_identity','make_execution','validate_protocol_fields','visit','validate_execution'},
 'contract.py':{'digest','require','apparatus_identity','authorize_execution'},
 'records.py':{'code_identity','strict_bytes','Recorder'},
 'clock.py':{'grid_steps','case_end','stage_ends','decision_clock','hold_steps','expected_time','clock_allowance','validate_physical_time'},
 'operator_view.py':{'display_identity','validate_intervention'},'controllers.py':{'SensorHistory'}}
calls=collections.Counter();forbidden=[]
def profile(frame,event,arg):
    if event!='call':return
    p=pathlib.Path(frame.f_code.co_filename)
    if not p.is_relative_to(D):return
    name=frame.f_code.co_name;calls[p.name+':'+name]+=1
    if name=='<module>' or name.startswith('<'):return
    if name not in allowed.get(p.name,set()):
        forbidden.append(p.name+':'+name);raise RuntimeError('Non-static Loom call rejected')
sys.setprofile(profile);sys.path.insert(0,str(D))
from loom_commissioning.authority import canonical,execution_object,execution_sha256,make_execution,validate_execution,runtime_identity,controller_identity
from loom_commissioning.contract import apparatus_identity,authorize_execution,P_CODE
from loom_commissioning import clock
from loom_p.records import code_identity
assert code_identity()['sha256']==P_CODE
identity=apparatus_identity();old_identity=js(OP/'RUNTIME_AND_APPARATUS_IDENTITIES.json')
assert set(identity['files'])==set(old_identity['apparatus']['files'])
assert [n for n in identity['files'] if identity['files'][n]!=old_identity['apparatus']['files'][n]]==['sensor.html']
assert runtime_identity()==old_identity['runtime']
for name,h in js(S/'VERIFICATION.json')['unchanged_files'].items():assert sha(D/name)==h
proof=js(S/'BYTE_PROOF.json');assert identity['files']['sensor.html']==proof['new_html_sha256']
assert proof['outside_style_identical'] and proof['new_legend'] is False

for name in ('CONTROL_GATE.json','RECORDING_CONTRACT.json','INTERPRETATION_TABLE.md','OPERATOR_INTEGRITY_FORM.md'):
    cp(OP/name,PUB/name)
for name in ('COMPACT_LAYOUT_REVIEW.md','ZERO_STEP_CLOSURE_AND_LAYOUT_AUTHORIZATION.json'):
    cp(OP/name,PUB/'historical-layout'/name)
cp(B/'PREFIX_CLOSURE_AND_COLOUR_LABEL_AUTHORIZATION.json',PUB/'PREFIX_CLOSURE_AND_COLOUR_LABEL_AUTHORIZATION.json')
cp(B/'OPERATOR_COLOUR_KEY_ASSISTANCE_CORRECTION.json',PUB/'prior-attempts/OPERATOR_COLOUR_KEY_ASSISTANCE_CORRECTION.json')
cp(R/'b1_execution_20260929/EXPIRED_ZERO_STEP_RESTART_REQUEST.json',PUB/'prior-attempts/EXPIRED_ZERO_STEP_RESTART_REQUEST.json')
cp(OP/'OPERATOR_EXPOSURE_AND_ATTEMPT_HISTORY.json',PUB/'prior-attempts/HISTORICAL_EXPOSURE_RECORD.json')
exposure={
 'scope':'Same B1 pair. Coordinate-label presentation correction. Closure and new packet preparation approved; replacement execution not yet granted.',
 'previous_full_raw_authority':'45f2349183579ed478e4c5582cdb70ba6619e06769ccfaad05f2dd36d26b173d',
 'prior_attempts':[
  dict(attempt=1,authority='2e338ae61dceaac3c3db0863f02cbccf0a9d98eb0842caf06c363207951e7c4c',native_steps=0,commands=0,simulated_seconds=0,closure='Operator-requested compact layout; complete zero-step record retained.'),
  dict(attempt=2,authority='45f2349183579ed478e4c5582cdb70ba6619e06769ccfaad05f2dd36d26b173d',native_steps=0,commands=0,simulated_seconds=0,closure='Administrative wall allowance expired; complete zero-step record retained.'),
  dict(attempt=3,authority='45f2349183579ed478e4c5582cdb70ba6619e06769ccfaad05f2dd36d26b173d',native_steps=120,commands=12,simulated_seconds=closure['simulated_seconds'],closure='Explicit withdrawal for coordinate-label colours; complete prefix retained.')],
 'all_prior_attempts_ended':True,'prior_permitted_start_readings_seen':True,'prior_permitted_1_2_second_movement_history_seen':True,
 'whole_start_unseen_or_first_naive_trial_claim_permitted':False,
 'prior_sealed_access_self_report':'No, before the earlier preparation; retained self-report, not a new attestation or independent access audit.',
 'hidden_evaluator_feedback_released':False,'pair_abandoned':False,
 'positive_controls':'Completed and accepted with documented guidance/practice, PC-CONTACT qualification and separately approved PC-HOLD repeat; historical evidence retained.',
 'separate_colour_key':'Draft created but never delivered; user requested coloured coordinate labels and explicitly rejected a separate key.',
 'colour_label_change':'Each existing coordinate label has the exact existing graph colour; no separate key, numeric change or new channel.',
 'closure_record_sha256':sha(PUB/'PREFIX_CLOSURE_AND_COLOUR_LABEL_AUTHORIZATION.json'),
 'next_full_raw':'One fresh, separately authorized attempt at the same complete physical start and unchanged 30-second ceiling; never continuation of the preserved prefix.',
 'companion_hidden':'Prepared separately, ungranted. FULL-RAW permission never authorizes CHEMISTRY-HIDDEN.',
 'restrictions':'No automatic retry, continuation, fixture replacement, tuning, live plan view or between-pair evaluator feedback.',
 'approval_scope':'Close/preserve existing prefix and prepare revised authority objects only. Both grants remain null.'}
write(PUB/'OPERATOR_EXPOSURE_AND_ATTEMPT_HISTORY.json',exposure)
display=js(OP/'DISPLAY_CONTRACT.json');display['reviewed_checkpoint']=APP
display['reviewed_files']['sensor.html']=identity['files']['sensor.html']
display['independent_disposition']='Historical independent disposition remains at 352f73fffa6d9781eae8aa38e708a9a05669588f. Compact layout was previously approved. The coordinate-colour CSS correction is verified by attached byte, detached DOM and offline browser checks; no new independent disposition claimed.'
display['coordinate_label_colours']=dict(exact_existing_trace_colours=True,all_29_full_and_25_hidden_coordinates_verified=True,
 no_separate_legend=True,numeric_colours_unchanged=True,graph_algorithm_and_colours_unchanged=True,
 outside_style_byte_identical=True,byte_proof_sha256=sha(S/'BYTE_PROOF.json'),browser_verification_sha256=sha(S/'VERIFICATION.json'))
write(PUB/'DISPLAY_CONTRACT.json',display)
protocol_contract=js(OP/'PROTOCOL_CONTRACT.json')
protocol_contract['memory']='FULL-RAW remains first in the pair. Two earlier zero-step attempts and one 1.2-second / 120-step / 12-command prefix are preserved as ended. Jason has seen permitted starting readings and that prefix history; no first-naive or wholly unseen-start claim remains. No evaluator feedback was released. Any later separately authorized fresh attempt reuses the same complete physical start. The second condition can benefit from FULL-RAW memory; fixed order is not counterbalanced and cannot establish chemistry necessity.'
write(PUB/'PROTOCOL_CONTRACT.json',protocol_contract)
rows=[];changes=[];current={}
for oldrow in js(OP/'B1_SEALED_AUTHORITY_IDENTITIES.json')['cases']:
    name=oldrow['case'];old=js(OV/'case-manifests'/(name+'.json'));m=copy.deepcopy(old)
    assert m['execution_authority'] is None and m['duration_seconds']==30 and m['baseline']==P
    assert execution_sha256(old)==oldrow['canonical_authority_sha256']
    assert sha(OV/'authority-objects'/(name+'.canonical.json'))==oldrow['canonical_authority_sha256']
    protocol=copy.deepcopy(old['execution']['procedure']['protocol'])
    for document,h in protocol['bound_documents'].items():
        assert sha(OP/document)==h;protocol['bound_documents'][document]=sha(PUB/document)
    r=old['execution']['resources'];m['apparatus']=identity
    m['execution']=make_execution(m['mode'],m['controller'],plan=old['execution']['procedure']['stages'],protocol=protocol,
      wall_limit=r['wall_limit_seconds'],storage_limit=r['storage_limit_bytes'],display='chemistry_hidden' if name=='B1-CHEMISTRY-HIDDEN' else 'none')
    validate_execution(m,complete=True)
    try:authorize_execution(m)
    except ValueError as error:assert str(error)=='commissioning execution is not authorized'
    else:raise AssertionError('Null grant permitted execution')
    assert all(m[k]==old[k] for k in old if k not in ('apparatus','execution'))
    assert m['execution']['runtime']==old['execution']['runtime'] and m['execution']['adapter']==old['execution']['adapter']
    assert m['execution']['display_intervention']==old['execution']['display_intervention']
    assert m['execution']['resources']==old['execution']['resources']
    assert m['execution']['procedure']['stages']==old['execution']['procedure']['stages']
    assert {k:v for k,v in protocol.items() if k!='bound_documents'}=={k:v for k,v in old['execution']['procedure']['protocol'].items() if k!='bound_documents'}
    assert clock.case_end(m)-m['initial_index']==3000
    assert all(clock.hold_steps(m,i)==10 for i in range(m['initial_index'],clock.case_end(m),10))
    for path in differences(old,m):
        if path.startswith(('/apparatus/','/execution/controller/implementation/sensor.html')):category='IDENTITY-ONLY / REQUIRED BY APPROVED COORDINATE-COLOUR CORRECTION'
        elif path in ('/execution/procedure/protocol/bound_documents/DISPLAY_CONTRACT.json',):category='PRESENTATION DOCUMENT BINDING REQUIRED BY CORRECTION'
        elif path in ('/execution/procedure/protocol/bound_documents/PROTOCOL_CONTRACT.json','/execution/procedure/protocol/bound_documents/OPERATOR_EXPOSURE_AND_ATTEMPT_HISTORY.json'):category='ACCEPTED CLOSURE AND PRIOR EXPOSURE HISTORY BINDING'
        else:raise RuntimeError('Unexpected semantic change; stop')
        changes.append(dict(case=name,path=path,classification=category))
    h=execution_sha256(m);assert h!=oldrow['canonical_authority_sha256']
    write(PRIV/'case-manifests'/(name+'.json'),m)
    obj=execution_object(m);write(PRIV/'authority-objects'/(name+'.json'),obj)
    (PRIV/'authority-objects'/(name+'.canonical.json')).write_bytes(canonical(obj))
    assert sha(PRIV/'authority-objects'/(name+'.canonical.json'))==h
    rows.append(dict(case=name,canonical_authority_sha256=h,previous_authority_sha256=oldrow['canonical_authority_sha256'],
      duration_seconds=30,native_ceiling=3000,maximum_command_holds=300,operator_coordinates=oldrow['operator_coordinates'],
      initial_state_sha256=m['initial_state'],initial_snapshot_sha256=oldrow['initial_snapshot_sha256'],
      execution_grant=None,static_validation=True,null_grant_rejected=True))
    current[name]=m
assert {k for k in current['B1-FULL-RAW'] if current['B1-FULL-RAW'][k]!=current['B1-CHEMISTRY-HIDDEN'][k]}=={'case_id','execution'}
assert {k for k in current['B1-FULL-RAW']['execution'] if current['B1-FULL-RAW']['execution'][k]!=current['B1-CHEMISTRY-HIDDEN']['execution'][k]}=={'display_intervention'}
snap=OV/'initial-states/B1-PAIR-INITIAL.snapshot.json.gz'
assert sha(snap)==rows[0]['initial_snapshot_sha256']==rows[1]['initial_snapshot_sha256']
cp(snap,PRIV/'initial-states'/snap.name) # Opaque copy only; never decompress.
runtime=runtime_identity();human=controller_identity('sensor_human')
sys.setprofile(None);assert not forbidden
ids={r['case']:r['canonical_authority_sha256'] for r in rows}
write(PUB/'B1_SEALED_AUTHORITY_IDENTITIES.json',dict(checkpoint=APP,cases=rows,execution_grants=None,complete_pair_initial_state_identical=True,
 next_decision='Authorize B1-FULL-RAW only. CHEMISTRY-HIDDEN remains separately ungranted.',evaluation_release='Only after both paired trials end or explicit pair abandonment.'))
write(PUB/'RUNTIME_AND_APPARATUS_IDENTITIES.json',dict(checkpoint=APP,parent=BASE,P=P,apparatus=identity,runtime=runtime,sensor_human=human,
 branch=git('branch','--show-current').decode().strip(),worktree=str(W),worktree_clean=True))
write(PUB/'SEMANTIC_DIFF.json',dict(parent_checkpoint=BASE,checkpoint=APP,manifest_changes=changes,
 changed_public_contract_fields={n:differences(js(OP/n),js(PUB/n)) for n in ('DISPLAY_CONTRACT.json','PROTOCOL_CONTRACT.json','OPERATOR_EXPOSURE_AND_ATTEMPT_HISTORY.json')},
 expected_changes=['Existing coordinate-label colours match existing graph traces; no separate key','Required HTML, apparatus and bound-display identities','Explicitly bind two zero-step closures and one 1.2-second prefix closure/exposure; no naive-start claim'],
 unchanged=['all physical initial fields and opaque snapshot bytes','P, configuration, body/world/sensor laws, controller and runtime','paired order and chemistry-only display omission','duration, holds, cadence, resource limits and recording fidelity','completion and interpretation criteria'],
 operator_lifecycle_representation_changes=[],unexpected_semantic_changes=[]))
write(PUB/'STATIC_COMPATIBILITY_REPORT.json',dict(checkpoint=APP,cases=rows,complete_pair_initial_state_identical=True,shared_snapshot_not_deserialized=True,
 prior_run_prefixes_preserved=True,production_change='29 CSS rules colour existing coordinate labels only',unchanged_controller_semantics=True,
 unexpected_semantic_changes=[],no_new_independent_disposition_claimed=True,
 scope='Identity/schema, null-grant rejection and integer clock checks only; no new world, controller invocation, prehistory, physical rerun or B1 launch.'))
write(PUB/'ZERO_EXECUTION_RECORD.json',dict(scope='Coordinate-label correction and packet regeneration only. The earlier 120-step human prefix is preserved separately.',
 simulation_steps=0,world_loads=0,Engine_constructors=0,Run_constructors=0,controller_commands=0,snapshot_deserializations=0,prehistory_updates=0,
 live_B1_services_started=0,old_B1_services_closed=1,execution_grants_created=0,static_authority_objects_created=2,
 detached_JS_fixture='Existing mocked DOM/transport check',browser_fixture='Closed disclosed PC-HOLD data only, never B1',
 guarded_Loom_call_inventory=dict(sorted(calls.items())),forbidden_calls=forbidden))
for name in ('BYTE_PROOF.json','VERIFICATION.json','DOM_RESULT.txt','BROWSER_COLOUR_QA.json','colour-labels-preview.png'):
    cp(S/name,PUB/'verification'/name)
cp(W/'docs/developmental_ecology/p_b1_coordinate_colours_20260929/REVIEW.md',PUB/'COORDINATE_COLOURS_REVIEW.md')
cp(D/'loom_commissioning/sensor.html',PUB/'apparatus-source/sensor.html')
for p in (OP/'prior-controls').iterdir():
    if p.is_file():cp(p,PUB/'prior-controls'/p.name)
for p in (OP/'historical-resource-basis').iterdir():
    if p.is_file():cp(p,PUB/'historical-resource-basis'/p.name)
projection=js(OP/'RESOURCE_PROJECTION.json')
projection['basis']='Unchanged measured A5 proxy and interactive recording planning basis. Coordinate-label CSS requires no new runtime/storage benchmark.'
write(PUB/'RESOURCE_PROJECTION.json',projection)
resource=(OP/'RESOURCE_PLAN.md').read_text(encoding='utf-8')
resource=resource.replace('compact CSS','coordinate-label CSS').replace('including the preserved zero-step attempt','including both zero-step attempts and the preserved 1.2-second prefix')
textfile(PUB/'RESOURCE_PLAN.md',resource)
instructions=(OP/'OPERATOR_INSTRUCTIONS.md').read_text(encoding='utf-8')
old_sentence='This packet binds the approved compact layout. Completed positive controls retain their recorded qualifications. The next decision is new exact authorization of B1-FULL-RAW only; the companion hidden trial remains separately ungranted. The prior FULL-RAW attempt ended at zero steps for this layout correction, after its permitted starting readings were seen.'
assert old_sentence in instructions
instructions=instructions.replace(old_sentence,'This packet adds the requested coordinate-label colours to the approved compact layout. Completed positive controls retain their recorded qualifications. The next decision is exact authorization of B1-FULL-RAW only; CHEMISTRY-HIDDEN remains separately ungranted. Two earlier zero-step attempts and a 1.2-second / 12-command attempt are preserved as ended. You have seen the permitted starting readings and that movement history, so a fresh attempt cannot be described as first-naive or wholly unseen.')
instructions+='\n## Coordinate colours\n\nEach coordinate label now has the exact colour of its existing graph trace. There is no separate key. The numbers, graph scales, history controls, commands, timing and permitted information are unchanged.\n'
textfile(PUB/'OPERATOR_INSTRUCTIONS.md',instructions)
textfile(PUB/'APPARATUS_DISPOSITION.md',f'''# Apparatus disposition

Checkpoint `{APP}` adds only the requested coordinate-label colours to `{BASE}`. Byte proof, the existing detached DOM fixture and offline browser verification passed: 29 FULL-RAW and 25 CHEMISTRY-HIDDEN labels match their existing traces. No separate key was added. Jason authorized closing/preserving the old prefix and preparing revised launch identities. No new independent review disposition is claimed.

Both execution grants are null. No fresh B1 attempt or timer has started. The historical control-gate file is retained unchanged; its status at preparation is qualified by the completed control records in `prior-controls/`. The bound exposure record preserves both zero-step attempts and the closed 1.2-second prefix. No evaluator feedback is released.
''')
textfile(PUB/'README.md',f'''# B1 coordinate-colour operator packet — awaiting authorization

Each coordinate label now matches its existing graph trace. There is no separate key. The compact layout, numeric readings, controls, history, permitted information, P and physical laws remain unchanged.

Apparatus: `{APP}`. Parent: `{BASE}`. P: `{P}`.

## Separate authorities

| Case | Canonical authority SHA-256 | Ceiling | State |
|---|---|---:|---|
| B1-FULL-RAW | `{ids['B1-FULL-RAW']}` | 30 s | New authorization required |
| B1-CHEMISTRY-HIDDEN | `{ids['B1-CHEMISTRY-HIDDEN']}` | 30 s | Separately sealed, ungranted |

The next decision is **B1-FULL-RAW only**. Authorization of one object does not authorize the other. No automatic retry, continuation, fixture substitution, tuning or parameter change is permitted.

The old attempt ended at 1.2 simulated seconds, 120 native steps and 12 human commands. Its complete prefix is preserved with verified record hashes. The two earlier zero-step attempts remain preserved. Jason has seen permitted starting readings and the 1.2-second movement history: no first-naive or wholly unseen-start claim is available. This closure is an interface-related administrative event, not a scientific B1 failure. A separately authorized fresh attempt would use the same complete physical start and unchanged 30-second ceiling.

Both paired physical starts remain identical. FULL-RAW retains 29 coordinates; CHEMISTRY-HIDDEN retains 25, with an explicit unavailable label and full private chemistry retained. The fixed order and ordinary-memory carryover limitation remain. No evaluator feedback was released and no new execution occurred during this correction/regeneration.

`OPERATOR_INSTRUCTIONS.md` describes the unchanged task. `COORDINATE_COLOURS_REVIEW.md`, `verification/`, `SEMANTIC_DIFF.json` and `STATIC_COMPATIBILITY_REPORT.json` document the bounded change. `RESOURCE_PLAN.md` preserves the resource projections and limits. `OPERATOR_EXPOSURE_AND_ATTEMPT_HISTORY.json` binds the actual history. `CONTROL_GATE.json` remains historical; `prior-controls/` supplies the accepted control qualifications.

Exact case manifests, canonical authority bytes and the opaque shared initial snapshot remain in sealed local custody. This public package contains identities only. No privileged evaluator record is included. Do not release evaluator material until both trials end or the pair is explicitly abandoned.

No new trial, command, timer or world has been prepared. A new exact FULL-RAW grant is required to launch.
''')
for pkg in ('loom_commissioning','loom_p'):
    for p in (D/pkg).iterdir():
        if p.is_file() and p.suffix in ('.py','.html'):cp(p,PRIV/'checkpoint-source'/pkg/p.name)
for name in ('configuration.json','requirements-lock.txt'):cp(D/name,PRIV/'checkpoint-source'/name)
cp(pathlib.Path(__file__),PRIV/'STATIC_REGENERATION_SOURCE.py')
write(PRIV/'PRIOR_CUSTODY_REFERENCE.json',dict(previous_packet=str(OLD),historical_held_identity='45d71cd121f823368401b11c4a1010d509af3224f49168ad528653274d0e7543',no_sealed_archive_opened=True))
assert inventory(OLD)==before
for folder in prior_attempts:assert inventory(folder/'private/runs/B1-FULL-RAW')==prior_runs[str(folder)]
assert git('status','--porcelain')==b''
write(PUB/'PRESERVATION.json',dict(historical_packet_files_unchanged=len(before),prior_attempt_record_files_unchanged={str(i+1):len(prior_runs[str(f)]) for i,f in enumerate(prior_attempts)},
 old_packet_inventory_sha256=sha(S/'PACKET_PRESERVATION_BEFORE.json'),prior_runs_inventory_sha256=sha(S/'PRIOR_RUN_PRESERVATION_BEFORE.json'),
 shared_snapshot_byte_identical=True,source_checkpoint_clean=True,vault_git_writes=0,pushes=0,PRs=0,merges=0,hidden_evaluator_state_disclosed=False))
for folder in (PUB,PRIV):
    files={p.relative_to(folder).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(folder.rglob('*')) if p.is_file()}
    write(folder/'FILE_MANIFEST.json',dict(files=files,excludes_self=True))
    with zipfile.ZipFile(E/(folder.name+'.zip'),'w',zipfile.ZIP_DEFLATED) as archive:
        for p in sorted(folder.rglob('*')):
            if p.is_file():archive.write(p,p.relative_to(folder))
write(S/'DELIVERY_RECEIPT.json',dict(checkpoint=APP,branch=git('branch','--show-current').decode().strip(),worktree=str(W),
 authority_identities=ids,public_packet=str(PUB),public_zip=str(E/'B1_OPERATOR_PACKET.zip'),public_zip_sha256=sha(E/'B1_OPERATOR_PACKET.zip'),
 sealed_archive_sha256=sha(E/'B1_SEALED_EVALUATOR.zip'),zero_new_execution=True))
print(json.dumps(dict(checkpoint=APP,authority_identities=ids,unexpected_semantic_changes=0,new_execution=0,public_zip_sha256=sha(E/'B1_OPERATOR_PACKET.zip'))))
