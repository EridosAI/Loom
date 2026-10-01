"""One authorized compact FULL-RAW preparation. No world loading in this script."""
import copy,datetime,hashlib,json,os,shutil,subprocess,sys,traceback
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
PC=ROOT/'b1_pc_execution_20260926';PREVIOUS=ROOT/'b1_execution_20260927'
PACK=ROOT/'exports/2026-09-27-B1-compact-1060a17e';PUBLIC=PACK/'B1_OPERATOR_PACKET';SEALED=PACK/'B1_SEALED_EVALUATOR'
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926';D=W/'developmental_ecology'
OUT=ROOT/'b1_execution_20260929';PRIVATE=OUT/'private'
CASE='B1-FULL-RAW';AUTH='45f2349183579ed478e4c5582cdb70ba6619e06769ccfaad05f2dd36d26b173d'
APP='1060a17e3dd14c6361f6f15c95bb58fad3110ffc'
stage='initial checks'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
def main():
    global stage
    assert not OUT.exists(),'Invocation already reserved; no repeat.'
    previous=read(PREVIOUS/'STATE.json')
    assert previous['status']=='ENDED AT ZERO STEPS / PRESERVED FOR LAYOUT CORRECTION' and previous['live_services']==0
    closure=read(PREVIOUS/'ZERO_STEP_CLOSURE_AND_LAYOUT_AUTHORIZATION.json')
    assert closure['native_steps']==closure['commands']==closure['simulated_seconds']==0
    assert sha(PREVIOUS/'private/runs/B1-FULL-RAW/manifest.json')==closure['manifest_sha256']
    assert read(PC/'SEQUENCE_STATE.json')['live_services']==0
    assert read(PC/'PC-LR-attempt-002/RESULT.json')['outcome']=='DEMONSTRATED'
    assert read(PC/'PC-MOTION.RESULT.json')['outcome']=='DEMONSTRATED WITH EXPLICIT GUIDANCE'
    assert read(PC/'PC-HOLD-attempt-002/RESULT.json')['physical_gentle_hold_target_met']
    assert read(PC/'PC-CONTACT.ASSESSMENT_CORRECTION.json')['corrected_assessment'].startswith('DEMONSTRATED')
    assert read(PC/'PC-CONTACT.JASON_ACCEPTANCE.json')['assessment_sha256']==sha(PC/'PC-CONTACT.ASSESSMENT_CORRECTION.json')
    assert read(PC/'OPERATOR_INTEGRITY_RECORD.json')['prior_sealed_B1_access_verbatim']=='No'
    for n,info in read(PUBLIC/'FILE_MANIFEST.json')['files'].items():
        p=PUBLIC/n;assert p.resolve().is_relative_to(PUBLIC.resolve())
        assert sha(p)==info['sha256'] and p.stat().st_size==info['bytes']
    pub=read(PUBLIC/'B1_SEALED_AUTHORITY_IDENTITIES.json')['cases'][0]
    assert pub['case']==CASE and pub['canonical_authority_sha256']==AUTH
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    git=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
    assert subprocess.check_output(git+['rev-parse','HEAD'],env=env).decode().strip()==APP
    assert subprocess.check_output(git+['status','--porcelain'],env=env)==b''
    free=shutil.disk_usage(ROOT).free;assert free>=12_000_000_000
    stage='private mechanical binding and current runtime verification'
    sys.path.insert(0,str(D))
    from loom_commissioning.authority import canonical,execution_object,execution_sha256,strict_loads,validate_execution,runtime_identity
    from loom_commissioning.contract import authorize_execution,apparatus_identity,P_CODE
    from loom_p.records import code_identity
    ids=read(PUBLIC/'RUNTIME_AND_APPARATUS_IDENTITIES.json')
    assert runtime_identity()==ids['runtime'] and apparatus_identity()==ids['apparatus']
    assert code_identity()['sha256']==P_CODE
    manifest=SEALED/'case-manifests/B1-FULL-RAW.json';obj=SEALED/'authority-objects/B1-FULL-RAW.canonical.json'
    snapshot=SEALED/'initial-states/B1-PAIR-INITIAL.snapshot.json.gz'
    # Only these three sealed inputs are mechanically read. No values are emitted.
    assert sha(obj)==AUTH and sha(snapshot)==pub['initial_snapshot_sha256']
    m=strict_loads(manifest.read_bytes())
    assert m['execution_authority'] is None and execution_sha256(m)==AUTH
    assert canonical(execution_object(m))==obj.read_bytes()
    assert m['case_id']==CASE and m['duration_seconds']==30 and m['initial_state']==pub['initial_state_sha256']
    assert m['controller']=='sensor_human' and m['mode']=='external_controller'
    assert m['execution']['display_intervention']=={'kind':'none'}
    assert m['execution']['resources']=={'storage_limit_bytes':1500000000,'wall_limit_seconds':7200}
    for document,h in m['execution']['procedure']['protocol']['bound_documents'].items():assert sha(PUBLIC/document)==h
    validate_execution(m,complete=True)
    source_hashes={p.relative_to(SEALED).as_posix():sha(p) for p in (manifest,obj,snapshot)}
    roots=[PACK,PC,PREVIOUS,ROOT/'b1_compact_layout_20260927',ROOT/'b1_compact_layout_preview',ROOT/'b1_regeneration_20260926',
        ROOT/'b1_packet_staging_20260926',ROOT/'exports/2026-09-26-B1-regenerated-352f73ff',
        ROOT/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02',
        ROOT/'exports/2026-09-27-positive-controls-review.zip',ROOT/'exports/2026-09-27-positive-controls-review-updated.zip']
    retained=sum(p.stat().st_size for root in roots if root.exists() for p in ([root] if root.is_file() else root.rglob('*')) if p.is_file())
    assert retained+993906579<11_000_000_000
    stage='recording Jason exact grant'
    PRIVATE.mkdir(parents=True)
    notice=('Jason replied "Yes, authorised." on 2026-09-29 to the explicit question asking authorization of B1-FULL-RAW only under authority '+AUTH+'. '
      'This authorizes one fresh case at corrected compact apparatus '+APP+', following the preserved zero-step administrative closure. '
      'The bound record qualifies prior permitted initial-reading exposure; no wholly unseen starting-state claim. '
      'Jason chooses every command. No assistant driving, plan view, privileged hint, retry, continuation, extension, tuning, substitution or code change. '
      'B1-CHEMISTRY-HIDDEN is not authorized. No evaluator feedback before both trials end or the pair is explicitly abandoned.')
    request=PRIVATE/'B1-FULL-RAW.approval.request.json'
    write_new(request,dict(notice=notice,approved_execution_sha256=AUTH,approved_execution=execution_object(m)))
    granted=copy.deepcopy(m)
    granted['execution_authority']=dict(request_path=str(request),request_sha256=sha(request),approved_case=CASE,
      approved_initial_state=m['initial_state'],approved_duration=30,approved_execution_sha256=AUTH)
    assert execution_object(granted)==execution_object(m);authorize_execution(granted)
    granted_path=PRIVATE/'B1-FULL-RAW.launch-manifest.json';write_new(granted_path,granted)
    output=PRIVATE/'runs/B1-FULL-RAW';assert not output.exists()
    command=[sys.executable,'-B','-X','utf8','-m','loom_commissioning.sensor_ui','--manifest',str(granted_path),
             '--initial',str(snapshot),'--output',str(output),'--port','0']
    write_new(PRIVATE/'LAUNCH_PLAN.json',dict(case=CASE,command=command,cwd=str(D),environment=dict(PYTHONPATH=str(D),PYTHONDONTWRITEBYTECODE='1'),
        maximum_invocations=1,automatic_commands=False,authority_sha256=AUTH))
    assert all(sha(SEALED/n)==h for n,h in source_hashes.items())
    write_new(OUT/'AUTHORIZATION_AND_LAUNCH_INTENT.json',dict(case=CASE,attempt=2,invocations_under_this_authority=1,
      recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),user_authorization_verbatim='Yes, authorised.',
      authority_sha256=AUTH,apparatus=APP,exact_execution_object_unchanged=True,private_grant_created=True,
      duration_seconds=30,maximum_command_holds=300,operator_coordinates=29,wall_limit_seconds=7200,stream_limit_bytes=1500000000,
      initial_snapshot_sha256=pub['initial_snapshot_sha256'],initial_state_sha256=pub['initial_state_sha256'],
      granted_manifest_sha256=sha(granted_path),request_sha256=sha(request),free_disk_bytes=free,retained_scoped_artifact_bytes=retained,
      retained_resource_roots=[str(p) for p in roots],combined_artifact_cap_bytes=12000000000,stop_request_threshold_bytes=11000000000,
      source_clean=True,runtime_verified=True,public_packet_hashes_verified=True,preserved_sealed_source_file_hashes=source_hashes,
      prior_attempt='Preserved zero-step closure on 2026-09-27; earlier grant not reused.',
      operator_exposure_record_sha256=sha(PUBLIC/'OPERATOR_EXPOSURE_AND_ATTEMPT_HISTORY.json'),
      positive_control_guidance_and_repeats_retained=True,prior_sealed_B1_access='No — existing self-report; no new attestation inferred.',
      preparation_access='Mechanical exact-manifest/canonical binding and compressed snapshot hashing only. No hidden values emitted.',
      snapshot_deserializations=0,worlds_loaded=0,simulation_steps=0,controller_commands=0,service_launches=0,
      chemistry_hidden_authorized=False,evaluator_release_allowed=False))
    write_new(OUT/'STATE.json',dict(status='AUTHORIZED / VERIFIED / ONE INVOCATION RESERVED',case=CASE,attempt=2,
      live_services=0,worlds_loaded=0,timers_started=0,simulation_steps=0,controller_commands=0,
      chemistry_hidden_authorized=False,evaluator_release_allowed=False))
    print('Exact authority, checkpoint, runtime, preserved controls/exposure and resource checks passed. One FULL-RAW invocation reserved; no world loaded yet.')
if __name__=='__main__':
    try:main()
    except Exception as exc:
        if PRIVATE.exists():
            with (PRIVATE/'PREPARATION_ERROR.txt').open('x',encoding='utf-8') as f:traceback.print_exc(file=f)
        print('Preparation stopped at '+stage+' ('+type(exc).__name__+'). No launch or retry. Private values withheld.')
        raise SystemExit(1)
