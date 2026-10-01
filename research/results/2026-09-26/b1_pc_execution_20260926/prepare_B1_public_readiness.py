"""Public-only B1 readiness check. No sealed case, snapshot, Run or world access."""
import datetime,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
S=Path(__file__).resolve().parent;ROOT=S.parent
P=ROOT/'exports/2026-09-26-B1-regenerated-352f73ff/B1_OPERATOR_PACKET'
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926';D=W/'developmental_ecology'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
out=S/'B1_FULL_RAW.PUBLIC_READINESS.json'
assert not out.exists(), 'Readiness record already exists.'
fm=read(P/'FILE_MANIFEST.json')
for name,info in fm['files'].items():
    p=P/name
    assert p.parent.resolve()==P.resolve(), 'Public-only allow-list boundary.'
    assert sha(p)==info['sha256'] and p.stat().st_size==info['bytes']
identity=read(P/'RUNTIME_AND_APPARATUS_IDENTITIES.json')
case=read(P/'B1_SEALED_AUTHORITY_IDENTITIES.json')['cases'][0]
assert case['case']=='B1-FULL-RAW' and case['execution_grant'] is None
assert case['canonical_authority_sha256']=='2e338ae61dceaac3c3db0863f02cbccf0a9d98eb0842caf06c363207951e7c4c'
assert case['duration_seconds']==30 and case['operator_coordinates']==29
assert read(S/'SEQUENCE_STATE.json')['live_services']==0
assert read(S/'PC-LR-attempt-002/RESULT.json')['outcome']=='DEMONSTRATED'
assert read(S/'PC-MOTION.RESULT.json')['outcome']=='DEMONSTRATED WITH EXPLICIT GUIDANCE'
assert read(S/'PC-HOLD-attempt-002/RESULT.json')['physical_gentle_hold_target_met']
correction=read(S/'PC-CONTACT.ASSESSMENT_CORRECTION.json')
assert correction['corrected_assessment'].startswith('DEMONSTRATED')
assert read(S/'PC-CONTACT.JASON_ACCEPTANCE.json')['assessment_sha256']==sha(S/'PC-CONTACT.ASSESSMENT_CORRECTION.json')
integrity=read(S/'OPERATOR_INTEGRITY_RECORD.json')
assert integrity['prior_sealed_B1_access_verbatim']=='No'
env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
git=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
assert subprocess.check_output(git+['rev-parse','HEAD'],env=env).decode().strip()==identity['checkpoint']=='352f73fffa6d9781eae8aa38e708a9a05669588f'
assert subprocess.check_output(git+['status','--porcelain'],env=env)==b''
for name,digest in identity['apparatus']['files'].items():assert sha(D/'loom_commissioning'/name)==digest
sys.path.insert(0,str(D))
from loom_commissioning.authority import runtime_identity
from loom_commissioning.contract import apparatus_identity, P_CODE
from loom_p.records import code_identity
assert runtime_identity()==identity['runtime']
assert apparatus_identity()==identity['apparatus']
assert code_identity()['sha256']==P_CODE
disk_free=shutil.disk_usage(ROOT).free
assert disk_free>=12_000_000_000
result=dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    case='B1-FULL-RAW',canonical_authority_sha256=case['canonical_authority_sha256'],
    duration_seconds=30,maximum_command_holds=300,operator_coordinates=29,
    public_packet_files_verified=len(fm['files']),public_file_manifest_sha256=sha(P/'FILE_MANIFEST.json'),
    apparatus_checkpoint=identity['checkpoint'],P=identity['P'],runtime_identity_matches=True,
    P_source_identity_matches=True,apparatus_source_identity_matches=True,worktree_clean=True,
    free_disk_bytes=disk_free,publicly_declared_wall_limit_seconds=7200,
    publicly_declared_stream_limit_bytes=1500000000,
    positive_control_demonstration_component='All four documented, with prior guidance and explicitly authorized repeats retained.',
    integrity='Jason self-reported no prior sealed B1 access; no new hidden-state exposure has been reported. No independent attestation implied.',
    remaining_boundary='Separate exact B1-FULL-RAW authority approval required. Sealed manifest/snapshot checks must occur only in an authorized blinded launch workflow; public readiness is not execution admission.',
    B1_exact_grant_created=False,B1_services_started=0,B1_snapshots_loaded=0,
    B1_state_or_evaluator_files_inspected=0,B1_simulation_steps=0,controller_commands=0,
    historical_or_canonical_files_modified=False,code_changes=0,
    operator_task='Attempt an energy-source interaction from the permitted raw history using self-chosen bounded paired commands.',
    evaluator_release='No first-trial privileged evaluation before the pair ends or is explicitly abandoned.',
    second_trial_authorized=False)
with out.open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
print('Public packet, P/apparatus/runtime identities, control records and disk capacity verified. B1 remains unstarted and ungranted; no sealed B1 access.')
