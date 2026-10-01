"""Prepare only Jason's four authorized controls. Never open B1 state or start a live case."""
import collections,copy,datetime,hashlib,json,os,pathlib,shutil,subprocess,sys
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926';D=W/'developmental_ecology'
E=ROOT/'exports/2026-09-26-B1-regenerated-352f73ff';PUB=E/'B1_OPERATOR_PACKET';PRIV=E/'B1_SEALED_EVALUATOR'
PY=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe')
APP='352f73fffa6d9781eae8aa38e708a9a05669588f'
AUTHORIZED={
 'PC-LR':'a80a9098b7eed714f824eccd841d17e29e94cc607489ddf7a5390f1dc38c493a',
 'PC-MOTION':'c35d7a469da2598a0bcb0abc9b952592fc5310525fac2f3e1f5edf0461bf401c',
 'PC-CONTACT':'2e9989e37863c32ae89fd559adf51942bd8152b8d5244a8de1baf2234c52ba1d',
 'PC-HOLD':'ac1c5615c2c99ebe2524e3648b81003d7eeb42f1b54493212afd8d3cb83d719f'}
allowed_private={PRIV/folder/(case+suffix) for case in AUTHORIZED for folder,suffix in
    [('case-manifests','.json'),('authority-objects','.canonical.json'),('initial-states','.snapshot.json.gz')]}
opened_private=set();blocked=[]
def audit(event,args):
    if event=='open' and isinstance(args[0],(str,bytes,os.PathLike)):
        path=pathlib.Path(os.fsdecode(args[0])).absolute()
        if path.is_relative_to(PRIV):
            if path not in allowed_private:
                blocked.append('non-PC private file access');raise RuntimeError('Non-PC private access forbidden')
            opened_private.add(str(path))
        if path==E/'B1_SEALED_EVALUATOR.zip':
            blocked.append('sealed archive access');raise RuntimeError('Sealed archive access forbidden')
    if event in ('os.listdir','os.scandir') and args and isinstance(args[0],(str,bytes,os.PathLike)):
        if pathlib.Path(os.fsdecode(args[0])).absolute().is_relative_to(PRIV):
            blocked.append('private directory enumeration');raise RuntimeError('Private enumeration forbidden')
sys.addaudithook(audit)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_bytes())
def write(p,x):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env)
assert git('rev-parse','HEAD').decode().strip()==APP and git('status','--porcelain')==b''
free=shutil.disk_usage(ROOT).free;assert free>=12_000_000_000
assert not (S/'runs').exists() and not (S/'approvals').exists()
index=js(PUB/'PC_AUTHORITY_IDENTITIES.json');assert index['order']==list(AUTHORIZED)
assert len(index['cases'])==4
calls=collections.Counter();blocked_calls=[]
allow={
 'records.py':{'Recorder','strict_bytes','code_identity'},
 'contract.py':{'digest','require','apparatus_identity','authorize_execution'},
 'authority.py':{'canonical','unique_json','strict_loads','object_pairs','execution_object','execution_sha256','file_identity','callable_identity','portable','_runtime_identity','runtime_identity','controller_identity','adapter_identity','make_execution','validate_protocol_fields','visit','validate_execution','read_approval','verify_approval_binding'},
 'controllers.py':{'SensorHistory'},
 'operator_view.py':{'display_identity','validate_intervention'},
 'clock.py':{'grid_steps','case_end','stage_ends','expected_time','clock_allowance','decision_clock','hold_steps'}}
def profile(frame,event,arg):
    if event!='call':return
    p=pathlib.Path(frame.f_code.co_filename)
    if not p.is_relative_to(D):return
    name=frame.f_code.co_name;key=p.name+':'+name;calls[key]+=1
    if name.startswith('<'):return
    if name not in allow.get(p.name,set()):
        blocked_calls.append(key);raise RuntimeError('Live execution forbidden during preparation: '+key)
sys.setprofile(profile);sys.path.insert(0,str(D))
from loom_commissioning.authority import canonical,execution_object,execution_sha256,validate_execution
from loom_commissioning.contract import authorize_execution
notice='''Jason explicitly authorized these four exact positive-control authority objects and no others:
PC-LR: a80a9098b7eed714f824eccd841d17e29e94cc607489ddf7a5390f1dc38c493a
PC-MOTION: c35d7a469da2598a0bcb0abc9b952592fc5310525fac2f3e1f5edf0461bf401c
PC-CONTACT: 2e9989e37863c32ae89fd559adf51942bd8152b8d5244a8de1baf2234c52ba1d
PC-HOLD: ac1c5615c2c99ebe2524e3648b81003d7eeb42f1b54493212afd8d3cb83d719f
Prepared order PC-LR -> PC-MOTION -> PC-CONTACT -> PC-HOLD. Report-don't-patch. No B1 trial or sealed B1 evaluator-state inspection. No retry, fixture substitution, tuning or interface change.
Subsequent steering: Jason is going to bed and requests preparation only. DO NOT LAUNCH until Jason returns and says he is ready. The scope authorization persists, but readiness has not been given. Human commands and observations must be Jason's, never an assistant policy.'''
prepared=[];before={}
for row in index['cases']:
    case=row['case'];expected=AUTHORIZED[case]
    assert row['canonical_authority_sha256']==expected
    source=PRIV/'case-manifests'/(case+'.json');original=js(source)
    raw=(PRIV/'authority-objects'/(case+'.canonical.json')).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==expected and canonical(execution_object(original))==raw
    assert original['execution_authority'] is None and original['case_id']==case
    validate_execution(original,complete=True)
    snapshot=PRIV/'initial-states'/(case+'.snapshot.json.gz')
    assert sha(snapshot)==row['initial_snapshot_sha256']
    for p in (source,PRIV/'authority-objects'/(case+'.canonical.json'),snapshot):before[str(p)]=sha(p)
    snapshot_copy=S/'inputs'/(case+'.snapshot.json.gz');snapshot_copy.parent.mkdir(exist_ok=True)
    shutil.copyfile(snapshot,snapshot_copy);assert sha(snapshot_copy)==sha(snapshot)
    approval={'notice':notice,'approved_execution_sha256':expected,'approved_execution':execution_object(original)}
    request=S/'approvals'/(case+'.request.json');request.parent.mkdir(exist_ok=True)
    request.write_bytes(canonical(approval))
    granted=copy.deepcopy(original)
    granted['execution_authority']={'request_path':str(request),'request_sha256':sha(request),'approved_case':case,
        'approved_initial_state':original['initial_state'],'approved_duration':original['duration_seconds'],'approved_execution_sha256':expected}
    assert execution_sha256(granted)==expected and execution_object(granted)==execution_object(original)
    authorize_execution(granted)  # Pure request/identity verification; no Run or state load.
    manifest=S/'launch-manifests'/(case+'.json');write(manifest,granted)
    for name,value in original['execution']['procedure']['protocol']['bound_documents'].items():assert sha(PUB/name)==value
    prepared.append(dict(case=case,authority_sha256=expected,duration_seconds=original['duration_seconds'],
        wall_limit_seconds=original['execution']['resources']['wall_limit_seconds'],stream_limit_bytes=original['execution']['resources']['storage_limit_bytes'],
        command=[str(PY),'-B','-X','utf8','-m','loom_commissioning.sensor_ui','--manifest',str(manifest),'--initial',str(snapshot_copy),
                 '--output',str(S/'runs'/case),'--port','0'],cwd=str(D),environment={'PYTHONPATH':str(D),'PYTHONDONTWRITEBYTECODE':'1'},
        status='AUTHORIZED / NOT STARTED — WAIT FOR JASON READINESS',native_steps=0,simulation_seconds=0,
        attempt_count=0,approval_request_sha256=sha(request),granted_manifest_sha256=sha(manifest),snapshot_sha256=sha(snapshot_copy)))
sys.setprofile(None)
assert not blocked_calls and not blocked
assert all(sha(pathlib.Path(p))==h for p,h in before.items())
assert not (S/'runs').exists() and git('status','--porcelain')==b''
write(S/'PC_SOURCE_PRESERVATION.json',dict(files=before,all_unchanged=True,B1_state_files_accessed=0,sealed_archives_opened=0))
write(S/'LAUNCH_PLAN.json',dict(app=APP,order=list(AUTHORIZED),cases=prepared,automatic_launch=False,automatic_progression=False,
    current_permission='Preparation only until Jason returns and says ready; authorization of exact four scopes is retained.',
    B1_authorized=False,simulation_or_control_policy_added=False))
write(S/'SEQUENCE_STATE.json',dict(status='WAITING FOR JASON READINESS',next_case='PC-LR',order=list(AUTHORIZED),cases=[dict(case=p['case'],attempts=0,status='NOT STARTED') for p in prepared],
    live_services=0,timers_started=0,worlds_loaded=0,simulation_steps=0,controller_commands=0,all_commands_must_be_Jason_choices=True))
write(S/'OPERATOR_INTEGRITY_RECORD.json',dict(operator='Jason',familiarity_verbatim='I am familiar.',
    prior_sealed_B1_access='NOT ANSWERED — do not infer no exposure',readiness_verbatim="I'm going to bed. Prepare everything. Then when I come in in the mornign I will tell you.",
    ready=False,controls_not_demonstrated=True,B1_evaluator_material_accessed_by_this_preparation=False,
    assistance='Assistant performed file, identity and authorization preparation only; no sensor interpretation, command choice or trial.',
    next_interaction='When Jason returns, start PC-LR once after readiness. Record the unanswered exposure item without requesting hidden contents.'))
write(S/'PRELAUNCH_CHECKS.json',dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),checkpoint=APP,git_clean=True,
    free_disk_bytes=free,minimum_free_disk_bytes=12_000_000_000,repeat_disk_runtime_identity_checks_on_return=True,
    four_exact_authority_bindings_verified=True,grants_created_only_for_authorized_PC_cases=4,case_objects_unchanged=True,
    initial_snapshots_byte_identical=True,snapshot_deserializations=0,Run_constructors=0,Engine_constructors=0,simulation_steps=0,controller_commands=0,
    service_launches=0,wall_timers_started=0,component_tests=0,replays=0,B1_state_files_accessed=0,sealed_archives_opened=0,
    private_files_opened_only_named_PC_files=len(opened_private),forbidden_access_attempts=blocked,forbidden_execution_attempts=blocked_calls,
    pure_Loom_call_inventory=dict(sorted(calls.items()))))
(S/'README.md').write_text('''# Positive controls authorized — waiting for Jason

Jason authorized exactly PC-LR -> PC-MOTION -> PC-CONTACT -> PC-HOLD, then asked to prepare everything and wait until he returns in the morning. The four exact request records and granted manifests have been prepared and verified. Existing authority objects, snapshots, source code, interface, configuration, horizons and limits are unchanged.

**DO NOT LAUNCH until Jason says ready.** No live service, simulation, controller request or 20-minute case timer has started. No Run or Engine was constructed and no snapshot deserialized. The four disclosed PC snapshots were copied and hashed only. No B1 state file or sealed archive was opened; no B1 grant was created.

Next: recheck runtime/source identities and free disk; follow the PC-LR entry in LAUNCH_PLAN.json exactly once. It invokes the existing corrected sensor_ui module, with a fresh output path and an OS-selected loopback port. Open its printed operator URL for Jason. Do not issue Start or actuator commands on his behalf. The configured wall timer starts when the actual Run is prepared, even before Start, so wait for readiness before invoking it. The actual launcher was deliberately not exercised overnight.

PC-LR's task is to identify a left/right difference from paired raw channels and state channel indices/sign before any action. Jason must make that observation and all actuator choices himself. Do not supply the answer, a suggested command policy, a queued/batched hold or an automatic demonstration. A zero pair still advances simulated time. The four fixed ceilings are 4/4/6/10 seconds; each control retains a 1,200-wall-second and 256-MB stream limit.

After each control ends, preserve its complete record and operator explanation, report the disclosed-control evaluation, and continue only in the authorized order with Jason operating. One attempt per case; no restart, retry, substitution, tuning or patch. Do not start the next control's timer while Jason is unavailable. B1 remains outside this authorization regardless of the controls' results.

The integrity record preserves “I am familiar.” The separate prior-B1-exposure question was not answered; do not turn it into a no-exposure attestation. Ask only for yes/no/unsure later, never hidden contents. No automatic reminder, background service or scheduled continuation was created.

Files: LAUNCH_PLAN.json, SEQUENCE_STATE.json, PRELAUNCH_CHECKS.json, OPERATOR_INTEGRITY_RECORD.json, PC_SOURCE_PRESERVATION.json. Approval/manifests and PC snapshots remain local administrative preparation records. Do not copy sealed evaluator material into the operator-facing workbench.
''',encoding='utf-8')
print(json.dumps(dict(status='PREPARED / WAITING FOR JASON',prepared_controls=list(AUTHORIZED),authority_bindings_verified=4,
    free_disk_bytes=free,source_clean=True,services=0,timers=0,simulation_steps=0,B1_state_accesses=0),indent=2))
