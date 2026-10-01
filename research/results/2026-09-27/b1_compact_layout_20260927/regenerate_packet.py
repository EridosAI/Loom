"""Static, sealed-custody regeneration. No world loading or simulation calls."""
import collections,copy,hashlib,json,os,pathlib,shutil,subprocess,sys,zipfile
S=pathlib.Path(__file__).resolve().parent;R=S.parent
W=R/'worktrees/loom-p-b1-apparatus-correction-20260926';D=W/'developmental_ecology'
OLD=R/'exports/2026-09-26-B1-regenerated-352f73ff';OP=OLD/'B1_OPERATOR_PACKET';OV=OLD/'B1_SEALED_EVALUATOR'
E=R/'exports/2026-09-27-B1-compact-1060a17e';PUB=E/'B1_OPERATOR_PACKET';PRIV=E/'B1_SEALED_EVALUATOR'
APP='1060a17e3dd14c6361f6f15c95bb58fad3110ffc';BASE='352f73fffa6d9781eae8aa38e708a9a05669588f';P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
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
assert git('rev-parse','HEAD').decode().strip()==APP and git('status','--porcelain')==b''
assert git('diff','--name-only',BASE,APP,'--','developmental_ecology').decode().splitlines()==['developmental_ecology/loom_commissioning/sensor.html']
before={str(p):sha(p) for p in sorted(OLD.rglob('*')) if p.is_file()}
run=R/'b1_execution_20260927/private/runs/B1-FULL-RAW'
run_before={p.name:sha(p) for p in run.iterdir() if p.is_file()}
for n,row in js(OP/'FILE_MANIFEST.json')['files'].items():assert sha(OP/n)==row['sha256']
assert not E.exists();PUB.mkdir(parents=True);PRIV.mkdir()
write(S/'PACKET_PRESERVATION_BEFORE.json',before)

# Only exact identity/schema and scalar-clock functions may be entered.
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
from loom_commissioning.contract import apparatus_identity,authorize_execution,P_CODE,CONFIG
from loom_commissioning import clock
from loom_p.records import code_identity
assert code_identity()['sha256']==P_CODE
identity=apparatus_identity()
old_identity=js(OP/'RUNTIME_AND_APPARATUS_IDENTITIES.json')
assert [n for n in identity['files'] if identity['files'][n]!=old_identity['apparatus']['files'][n]]==['sensor.html']
assert runtime_identity()==old_identity['runtime']
for name,h in js(S/'LAYOUT_BYTE_PROOF.json')['unchanged_files'].items():assert sha(D/name)==h

for name in ('CONTROL_GATE.json','RECORDING_CONTRACT.json','INTERPRETATION_TABLE.md','OPERATOR_INTEGRITY_FORM.md'):
    cp(OP/name,PUB/name)
cp(R/'b1_execution_20260927/ZERO_STEP_CLOSURE_AND_LAYOUT_AUTHORIZATION.json',PUB/'ZERO_STEP_CLOSURE_AND_LAYOUT_AUTHORIZATION.json')
exposure={
 'scope':'B1 pair retained. Administrative layout correction, not a perceptual outcome or automatic retry.',
 'prior_full_raw_authority':'2e338ae61dceaac3c3db0863f02cbccf0a9d98eb0842caf06c363207951e7c4c',
 'prior_attempt_closed':True,'prior_native_steps':0,'prior_commands':0,'prior_simulated_seconds':0.0,
 'prior_permitted_start_readings_seen':True,'whole_start_unseen_naivety_claim_permitted':False,
 'hidden_evaluator_access_or_feedback':False,'pair_abandoned':False,
 'operator_previous_sealed_access_self_report':'No, before the earlier preparation; not an independent access audit.',
 'positive_controls':'Completed and accepted with guidance/practice and PC-CONTACT interpretation qualifications; original records retained.',
 'approved_layout_preview_sha256':'880207be319ad796aed39fd4ab88c0d6fab00c191da9b56522548c8e1b4f5590',
 'prior_attempt_closure_record_sha256':sha(PUB/'ZERO_STEP_CLOSURE_AND_LAYOUT_AUTHORIZATION.json'),
 'next_full_raw':'One fresh separately authorized attempt using the same complete physical start and 30-second ceiling. Prior attempt remains closed.',
 'companion_hidden':'Separately prepared only. Full-raw authorization never authorizes hidden case.',
 'restrictions':'No retry, continuation, new fixture, controller substitution, tuning, live plan view or between-pair evaluator feedback.',
 'approval_scope':'Layout correction and new packet preparation only. Both execution grants remain null.'}
write(PUB/'OPERATOR_EXPOSURE_AND_ATTEMPT_HISTORY.json',exposure)
display=js(OP/'DISPLAY_CONTRACT.json');display['reviewed_checkpoint']=APP
display['reviewed_files']['sensor.html']=identity['files']['sensor.html']
display['independent_disposition']='Historical disposition at '+BASE+' only; this CSS-only checkpoint is verified by the attached byte, DOM and browser checks and Jason-approved preview. No new independent disposition claimed.'
display['compact_layout']={'approved_preview_sha256':exposure['approved_layout_preview_sha256'],'style_only':True,'outside_style_byte_identical':True,
 'tested_viewports':[[777,722],[1280,720]],'no_page_overflow_at_tested_sizes':True,'history_retained':True,'small_mobile_may_scroll':True}
write(PUB/'DISPLAY_CONTRACT.json',display)
protocol_contract=js(OP/'PROTOCOL_CONTRACT.json')
protocol_contract['memory']='FULL-RAW remains first in the pair. Jason already saw its permitted initial readings during a zero-step attempt closed for layout correction; no wholly unseen starting-state claim remains. No privileged feedback was released. The second condition can benefit from memory of FULL-RAW; the fixed order is not counterbalanced and cannot establish chemistry necessity.'
protocol_contract['grants']='None in this regenerated packet. Authorize each exact new object separately. Historical grants do not authorize these objects.'
write(PUB/'PROTOCOL_CONTRACT.json',protocol_contract)
rows=[];changes=[];current={}
for oldrow in js(OP/'CASE_AND_AUTHORITY_INDEX.json')['cases']:
    name=oldrow['case']
    if not name.startswith('B1-'):continue
    old=js(OV/'case-manifests'/(name+'.json'));m=copy.deepcopy(old)
    assert m['execution_authority'] is None and m['duration_seconds']==30 and m['baseline']==P
    assert execution_sha256(old)==oldrow['canonical_authority_sha256']
    assert sha(OV/'authority-objects'/(name+'.canonical.json'))==oldrow['canonical_authority_sha256']
    protocol=copy.deepcopy(old['execution']['procedure']['protocol'])
    for document,h in protocol['bound_documents'].items():
        assert sha(OP/document)==h;protocol['bound_documents'][document]=sha(PUB/document)
    protocol['bound_documents']['OPERATOR_EXPOSURE_AND_ATTEMPT_HISTORY.json']=sha(PUB/'OPERATOR_EXPOSURE_AND_ATTEMPT_HISTORY.json')
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
    assert {k:v for k,v in protocol.items() if k!='bound_documents'}=={k:v for k,v in old['execution']['procedure']['protocol'].items() if k!='bound_documents'}
    assert clock.case_end(m)-m['initial_index']==3000
    assert all(clock.hold_steps(m,i)==10 for i in range(m['initial_index'],clock.case_end(m),10))
    for path in differences(old,m):
        if path.startswith(('/apparatus/','/execution/controller/implementation/sensor.html')):category='IDENTITY-ONLY / REQUIRED BY APPROVED COMPACT LAYOUT'
        elif path.startswith('/execution/procedure/protocol/bound_documents/'):category='APPROVED LAYOUT AND ADMINISTRATIVE HISTORY DOCUMENT BINDING'
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
cp(snap,PRIV/'initial-states'/snap.name) # Opaque bytes only; never decompressed.
runtime=runtime_identity();human=controller_identity('sensor_human')
sys.setprofile(None)
assert not forbidden
write(PUB/'B1_SEALED_AUTHORITY_IDENTITIES.json',dict(checkpoint=APP,cases=rows,execution_grants=None,complete_pair_initial_state_identical=True,
 next_decision='FULL-RAW only. CHEMISTRY-HIDDEN requires its own later authorization.',evaluation_release='Only after both paired trials end or explicit pair abandonment.'))
write(PUB/'RUNTIME_AND_APPARATUS_IDENTITIES.json',dict(checkpoint=APP,parent=BASE,P=P,apparatus=identity,runtime=runtime,sensor_human=human,
 branch=git('branch','--show-current').decode().strip(),worktree=str(W),worktree_clean=True))
write(PUB/'SEMANTIC_DIFF.json',dict(parent_checkpoint=BASE,checkpoint=APP,manifest_changes=changes,
 changed_public_contract_fields={n:differences(js(OP/n),js(PUB/n)) for n in ('DISPLAY_CONTRACT.json','PROTOCOL_CONTRACT.json')},
 expected_changes=['CSS layout and required source/document identity bindings','Explicitly bind zero-step closure and prior permitted-reading exposure; no naivety claim'],
 unchanged=['all physical initial fields and snapshot bytes','P, world, body, sensors, controller and runtime','paired order and display deprivation','duration, holds, cadence, resource limits and fidelity','completion and interpretation criteria'],unexpected_semantic_changes=[]))
write(PUB/'STATIC_COMPATIBILITY_REPORT.json',dict(checkpoint=APP,cases=rows,complete_pair_initial_state_identical=True,shared_snapshot_not_deserialized=True,
 current_run_prefix_preserved=True,production_change='sensor.html style only',unchanged_controller_semantics=True,unexpected_semantic_changes=[],
 scope='Pure identity, schema, null-grant rejection and integer clock checks. No physical-state rerun, controller invocation or B1 launch.'))
write(PUB/'ZERO_EXECUTION_RECORD.json',dict(scope='This correction and regeneration task; prior zero-step Run closure recorded separately.',
 simulation_steps=0,world_loads=0,Engine_constructors=0,Run_constructors=0,controller_commands=0,snapshot_deserializations=0,prehistory_updates=0,
 live_B1_services_started=0,old_B1_services_closed=1,execution_grants_created=0,static_authority_objects_created=2,
 detached_JS_fixture='Existing mocked DOM/transport test only',browser_fixture='Closed disclosed PC-HOLD data, never B1',
 guarded_Loom_call_inventory=dict(sorted(calls.items())),forbidden_calls=forbidden))
for name in ('LAYOUT_BYTE_PROOF.json','BROWSER_LAYOUT_QA.json','DOM_COMPONENT_RESULT.txt','compact-full-narrow.png'):
    cp(S/name,PUB/'verification'/name)
cp(W/'docs/developmental_ecology/p_b1_compact_layout_20260927/COMPACT_LAYOUT_REVIEW.md',PUB/'COMPACT_LAYOUT_REVIEW.md')
cp(D/'loom_commissioning/sensor.html',PUB/'apparatus-source/sensor.html')
for name in ('POSITIVE_CONTROL_REVIEW_ADDENDUM.md','PC-CONTACT.JASON_ACCEPTANCE.json'):
    cp(R/'b1_pc_execution_20260926'/name,PUB/'prior-controls'/name)
cp(OP/'RESOURCE_PROJECTION.json',PUB/'historical-resource-basis/RESOURCE_PROJECTION.json')
cp(OP/'RESOURCE_PLAN.md',PUB/'historical-resource-basis/RESOURCE_PLAN.md')
projection=js(OP/'RESOURCE_PROJECTION.json')
write(PUB/'RESOURCE_PROJECTION.json',dict(basis='Unchanged measured A5 and prior interactive-history planning basis; compact CSS requires no new simulation or recorder estimate.',
 cases=[r for r in projection['cases'] if r.get('case','').startswith('B1-')],
 wall_limit_per_case_seconds=7200,stream_limit_per_case_bytes=1500000000,minimum_prelaunch_free_bytes=12000000000,
 combined_artifact_cap_bytes=12000000000,stop_request_bytes=11000000000,flush_reserve_bytes=1000000000,
 no_benchmark_run=True,human_deliberation_is_wall_only=True,old_attempt_and_all_retained_copies_count_toward_caps=True))
textfile(PUB/'RESOURCE_PLAN.md','''# Resource plan

The two separately granted B1 cases retain 30 simulated seconds, 3,000 native steps and 300 manual holds each. Each case retains its 7,200-second wall and 1.5 GB uncompressed-stream caps. Native fidelity is unchanged.

The prior measured A5 proxy remains 12.2459865 wall seconds per simulated second: 6.12 minutes of base compute per B1 case, before unmeasured interactive work and human deliberation. At 5 / 10 / 20 seconds of deliberation per hold, a complete case illustrates about 31.1 / 56.1 / 106.1 minutes before that extra overhead. These are illustrations, not guarantees. Deliberation consumes wall time, never bodily time.

The unchanged stream planning bound is about 843.907 MB per case, with 150 MB snapshot/display allowance. History recording remains quadratic; compact CSS does not reduce it. The retained historical resource basis gives the original detailed arithmetic. No benchmark, horizon change or fidelity reduction was performed.

The existing 12 GB combined artifact cap, 11 GB stop request and 1 GB flush reserve remain. Require at least 12 GB free before a future launch and count all retained copies, including the preserved zero-step attempt. Preparation has not started a new administrative timer. No automatic retry or extension follows a cutoff.
''')
instructions=(OP/'OPERATOR_INSTRUCTIONS.md').read_text(encoding='utf-8')
obsolete='This packet has been regenerated against the corrected operator apparatus. No case is authorized or started. The next decision is authorization of the four positive controls only; B1 needs separate later authorization.'
assert obsolete in instructions
instructions=instructions.replace(obsolete,'This packet binds the approved compact layout. Completed positive controls retain their recorded qualifications. The next decision is new exact authorization of B1-FULL-RAW only; the companion hidden trial remains separately ungranted. The prior FULL-RAW attempt ended at zero steps for this layout correction, after its permitted starting readings were seen.')
instructions+='\n## Compact layout\n\nE/I and lifecycle appear at the top, raw panels in the middle, and the actuator inputs below them. All fit at the verified 777 × 722 pane size. Current and Selected columns, full history slider and data export are unchanged. The command and note logs scroll within their own small regions. Smaller screens or larger browser text settings can still require scrolling. There is no new scene view or inferred navigation cue.\n'
textfile(PUB/'OPERATOR_INSTRUCTIONS.md',instructions)
textfile(PUB/'APPARATUS_DISPOSITION.md',f'''# Apparatus disposition

Checkpoint `{APP}` changes only approved compact CSS from `{BASE}`. Attached byte preservation, detached DOM and offline browser checks passed. Jason approved the concrete layout and preparation of new authority objects. No new independent reviewer disposition is asserted; the prior independently closed apparatus holds remain historical at their own checkpoint.

Both grants remain null. This is a reviewable launch proposal; no new attempt, timer or B1 world was prepared. The historic gate file is retained byte-for-byte and its original NOT EXECUTED status describes its preparation date; completed controls are documented separately. Prior starting-reading exposure is explicitly qualified in the new bound record.
''')
ids={r['case']:r['canonical_authority_sha256'] for r in rows}
textfile(PUB/'README.md',f'''# B1 compact operator packet — awaiting exact authorization

The approved display now fits the tested narrow pane. Only CSS changed; commands, permitted information, timing, recording, P and physical laws remain unchanged.

Apparatus: `{APP}`. Parent: `{BASE}`. P: `{P}`.

## Separate authorities

| Case | New canonical authority SHA-256 | Ceiling | State |
|---|---|---:|---|
| B1-FULL-RAW | `{ids['B1-FULL-RAW']}` | 30 s | New authorization required |
| B1-CHEMISTRY-HIDDEN | `{ids['B1-CHEMISTRY-HIDDEN']}` | 30 s | Separately sealed, not granted |

The next requested decision is FULL-RAW only. Its exact canonical object includes the approved compact interface and the administrative history qualification. Authorization of one case does not authorize the other. No automatic retry, continuation, replacement, tuning or parameter change is permitted.

The former FULL-RAW attempt is preserved as ended at 0.000 simulated seconds, zero commands and zero steps. Jason had seen its permitted initial readings; a wholly unseen starting-state claim is unavailable. This is not a B1 outcome. The same paired physical initial state is retained. No evaluator feedback has been released, and no new B1 execution has occurred.

`OPERATOR_INSTRUCTIONS.md` explains the unchanged task and the compact display. `COMPACT_LAYOUT_REVIEW.md`, `SEMANTIC_DIFF.json`, `STATIC_COMPATIBILITY_REPORT.json` and `verification/` record the checks. `RESOURCE_PLAN.md` preserves resource limits and projections. `prior-controls/` records the accepted practice qualifications. `CONTROL_GATE.json` is the unchanged historical gate; its status sentence is historical, not the current control outcome.

Exact case manifests, canonical authority bytes and the unchanged paired snapshot remain in sealed local custody. This operator package contains hashes only and must not include that custody directory. Do not release evaluator material until both trials end or the pair is explicitly abandoned.

No launch is implied by reading or approving the layout. The new FULL-RAW authority must be explicitly authorized before a fresh attempt is prepared.
''')
for pkg in ('loom_commissioning','loom_p'):
    for p in (D/pkg).iterdir():
        if p.is_file() and p.suffix in ('.py','.html'):cp(p,PRIV/'checkpoint-source'/pkg/p.name)
for name in ('configuration.json','requirements-lock.txt'):cp(D/name,PRIV/'checkpoint-source'/name)
cp(pathlib.Path(__file__),PRIV/'STATIC_REGENERATION_SOURCE.py')
write(PRIV/'PRIOR_CUSTODY_REFERENCE.json',dict(previous_packet=str(OLD),historical_held_identity='45d71cd121f823368401b11c4a1010d509af3224f49168ad528653274d0e7543',no_archive_opened=True))
assert all(sha(pathlib.Path(p))==h for p,h in before.items())
assert {p.name:sha(p) for p in run.iterdir() if p.is_file()}==run_before
assert git('status','--porcelain')==b''
write(PUB/'PRESERVATION.json',dict(historical_packet_files_unchanged=len(before),old_run_files_unchanged=len(run_before),
 old_inventory_sha256=sha(S/'PACKET_PRESERVATION_BEFORE.json'),shared_snapshot_byte_identical=True,source_checkpoint_clean=True,
 vault_git_writes=0,pushes=0,PRs=0,merges=0,hidden_evaluator_state_disclosed=False))
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
