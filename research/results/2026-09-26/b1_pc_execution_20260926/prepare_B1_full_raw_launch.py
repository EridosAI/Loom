"""Prepare the authorized blinded launch; report only public checks and hashes.

The exact manifest/authority are processed mechanically in private custody.
No snapshot deserialization, scene inspection, Run, Engine or controller call.
"""
import copy,datetime,hashlib,json,os,shutil,subprocess,sys,traceback
from pathlib import Path
PC=Path(__file__).resolve().parent; ROOT=PC.parent
PACK=ROOT/'exports/2026-09-26-B1-regenerated-352f73ff'
PUBLIC=PACK/'B1_OPERATOR_PACKET'; SEALED=PACK/'B1_SEALED_EVALUATOR'
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926'; D=W/'developmental_ecology'
OUT=ROOT/'b1_execution_20260927'; PRIVATE=OUT/'private'
CASE='B1-FULL-RAW'; AUTH='2e338ae61dceaac3c3db0863f02cbccf0a9d98eb0842caf06c363207951e7c4c'
APP='352f73fffa6d9781eae8aa38e708a9a05669588f'
stage='initial checks'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(p,obj):
    with p.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')

def main():
    global stage
    assert not OUT.exists(), 'B1 launch preparation already reserved; do not repeat.'
    assert read(PC/'SEQUENCE_STATE.json')['live_services']==0
    assert read(PC/'PC-LR-attempt-002/RESULT.json')['outcome']=='DEMONSTRATED'
    assert read(PC/'PC-MOTION.RESULT.json')['outcome']=='DEMONSTRATED WITH EXPLICIT GUIDANCE'
    assert read(PC/'PC-HOLD-attempt-002/RESULT.json')['physical_gentle_hold_target_met']
    assert read(PC/'PC-CONTACT.ASSESSMENT_CORRECTION.json')['corrected_assessment'].startswith('DEMONSTRATED')
    assert read(PC/'PC-CONTACT.JASON_ACCEPTANCE.json')['assessment_sha256']==sha(PC/'PC-CONTACT.ASSESSMENT_CORRECTION.json')
    assert read(PC/'OPERATOR_INTEGRITY_RECORD.json')['prior_sealed_B1_access_verbatim']=='No'
    for name,info in read(PUBLIC/'FILE_MANIFEST.json')['files'].items():
        p=PUBLIC/name;assert p.parent.resolve()==PUBLIC.resolve()
        assert sha(p)==info['sha256'] and p.stat().st_size==info['bytes']
    public=read(PUBLIC/'B1_SEALED_AUTHORITY_IDENTITIES.json')['cases'][0]
    assert public['case']==CASE and public['canonical_authority_sha256']==AUTH
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    git=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
    assert subprocess.check_output(git+['rev-parse','HEAD'],env=env).decode().strip()==APP
    assert subprocess.check_output(git+['status','--porcelain'],env=env)==b''
    free=shutil.disk_usage(ROOT).free;assert free>=12_000_000_000

    stage='pure identity and private binding checks'
    sys.path.insert(0,str(D))
    from loom_commissioning.authority import (canonical,execution_object,execution_sha256,
        strict_loads,validate_execution,runtime_identity)
    from loom_commissioning.contract import authorize_execution,apparatus_identity,P_CODE
    from loom_p.records import code_identity
    identities=read(PUBLIC/'RUNTIME_AND_APPARATUS_IDENTITIES.json')
    assert runtime_identity()==identities['runtime']
    assert apparatus_identity()==identities['apparatus']
    assert code_identity()['sha256']==P_CODE
    manifest_path=SEALED/'case-manifests/B1-FULL-RAW.json'
    object_path=SEALED/'authority-objects/B1-FULL-RAW.canonical.json'
    snapshot_path=SEALED/'initial-states/B1-PAIR-INITIAL.snapshot.json.gz'
    # These are the only three sealed input files read. Snapshot bytes are hashed,
    # never decompressed or deserialized here. No values from m are printed.
    assert sha(object_path)==AUTH
    assert sha(snapshot_path)==public['initial_snapshot_sha256']
    m=strict_loads(manifest_path.read_bytes())
    assert m['execution_authority'] is None
    assert execution_sha256(m)==AUTH
    assert canonical(execution_object(m))==object_path.read_bytes()
    assert m['case_id']==CASE and m['duration_seconds']==30
    assert m['initial_state']==public['initial_state_sha256']
    assert m['controller']=='sensor_human' and m['mode']=='external_controller'
    assert m['execution']['display_intervention']=={'kind':'none'}
    assert m['execution']['resources']=={'storage_limit_bytes':1500000000,'wall_limit_seconds':7200}
    validate_execution(m,complete=True)
    source_hashes={str(p.relative_to(SEALED)):sha(p) for p in (manifest_path,object_path,snapshot_path)}
    resource_roots=[PACK,PC,ROOT/'b1_regeneration_20260926',
        ROOT/'exports/2026-09-27-positive-controls-review.zip',
        ROOT/'exports/2026-09-27-positive-controls-review-updated.zip']
    retained=sum(p.stat().st_size for root in resource_roots if root.exists()
        for p in ([root] if root.is_file() else root.rglob('*')) if p.is_file())
    assert retained<11_000_000_000

    stage='recording exact human grant'
    PRIVATE.mkdir(parents=True)
    verbatim=("Yeah but the issue is that I don't expect the bug to be able to navigate this on its first try. "
        "It will take lots and lots of tries and failures to get enough information to be able to associate various signals enough to navigate confidently towards an energy source. "
        "I'm not going to sit here for hours and hours being the bug. \n"
        "If we're using me to test whether the signals are useful enough for the bug to navigate with... why?\n\n"
        "But in the interests of the experiment launch it anyway in its current blinded form. I'm kind of keen to see if I can do it.")
    notice=('Jason previously assented to the exact B1-FULL-RAW authority '+AUTH+
        ' subject to a visual requirement. He now explicitly directs launch in its current blinded form: '+verbatim+
        '\nThis resolves the visual condition in favor of the unchanged prepared object and supersedes the pending visual-practice/replacement question. '
        'Exactly one B1-FULL-RAW case is authorized. Jason chooses every paired command through the existing interface. '
        'No assistant driving, plan view, live privileged hint, retry, continuation, extension, tuning, substitution, '
        'code change or second-case launch is authorized. Preserve all records and the fixed limits. '
        'No evaluator feedback until both B1 cases have ended or the pair is explicitly abandoned. '
        'B1-CHEMISTRY-HIDDEN still requires separate authorization.')
    request=PRIVATE/'B1-FULL-RAW.approval.request.json'
    write_new(request,dict(notice=notice,approved_execution_sha256=AUTH,approved_execution=execution_object(m)))
    granted=copy.deepcopy(m)
    granted['execution_authority']=dict(request_path=str(request),request_sha256=sha(request),
        approved_case=CASE,approved_initial_state=m['initial_state'],approved_duration=30,
        approved_execution_sha256=AUTH)
    assert execution_object(granted)==execution_object(m)
    authorize_execution(granted)
    granted_path=PRIVATE/'B1-FULL-RAW.launch-manifest.json'
    write_new(granted_path,granted)
    output=PRIVATE/'runs/B1-FULL-RAW'
    assert not output.exists()
    cmd=[sys.executable,'-B','-X','utf8','-m','loom_commissioning.sensor_ui',
        '--manifest',str(granted_path),'--initial',str(snapshot_path),'--output',str(output),'--port','0']
    write_new(PRIVATE/'LAUNCH_PLAN.json',dict(case=CASE,command=cmd,cwd=str(D),
        environment=dict(PYTHONPATH=str(D),PYTHONDONTWRITEBYTECODE='1'),maximum_invocations=1,
        automatic_commands=False,authority_sha256=AUTH))
    assert all(sha(SEALED/name)==digest for name,digest in source_hashes.items())
    write_new(OUT/'AUTHORIZATION_AND_LAUNCH_INTENT.json',dict(case=CASE,attempt=1,
        recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
        user_authorization_verbatim=verbatim,authority_sha256=AUTH,apparatus=APP,
        current_blinded_form_explicitly_authorized=True,visual_condition_resolved=True,
        pending_visual_scope_question_superseded=True,
        exact_execution_object_unchanged=True,private_grant_created=True,
        duration_seconds=30,maximum_command_holds=300,operator_coordinates=29,
        wall_limit_seconds=7200,stream_limit_bytes=1500000000,
        initial_snapshot_sha256=public['initial_snapshot_sha256'],
        initial_state_sha256=public['initial_state_sha256'],
        granted_manifest_sha256=sha(granted_path),request_sha256=sha(request),
        free_disk_bytes=free,retained_scoped_artifact_bytes=retained,
        combined_new_artifact_cap_bytes=12000000000,stop_request_threshold_bytes=11000000000,
        source_clean=True,runtime_identity_verified=True,public_packet_hashes_verified=True,
        preserved_sealed_source_file_hashes=source_hashes,
        positive_control_record='../b1_pc_execution_20260926/POSITIVE_CONTROL_REVIEW_ADDENDUM.md',
        positive_control_guidance_and_repeats_retained=True,
        prior_sealed_B1_access='No — existing Jason self-report; no new exposure reported or revealed.',
        setup_private_access='Mechanical exact-manifest/authority binding and compressed snapshot-byte hashing only; no hidden values emitted or evaluator interpretation performed.',
        snapshot_deserializations=0,Run_constructors=0,Engine_constructors=0,
        simulation_steps=0,controller_commands=0,service_launches=0,wall_timers_started=0,
        invocation_reserved=1,chemistry_hidden_authorized=False,
        evaluator_release='After both cases end or explicit abandonment of the pair; no between-case evaluation.'))
    write_new(OUT/'STATE.json',dict(status='AUTHORIZED / VERIFIED / ONE INVOCATION RESERVED',case=CASE,
        attempts=0,live_services=0,worlds_loaded=0,timers_started=0,simulation_steps=0,controller_commands=0,
        chemistry_hidden_authorized=False,evaluator_release_allowed=False))
    print('B1-FULL-RAW exact grant, unchanged bindings, runtime, control/exposure record and resource checks passed. One launch reserved. No snapshot loaded or world advanced; no hidden state emitted.')

if __name__=='__main__':
    try:main()
    except Exception as exc:
        if PRIVATE.exists():
            with (PRIVATE/'PREPARATION_ERROR.txt').open('x',encoding='utf-8') as f:traceback.print_exc(file=f)
        print('B1 preparation stopped at '+stage+' ('+type(exc).__name__+'). No automatic launch or retry. Private values withheld.')
        raise SystemExit(1)
