"""NON-CANONICAL RESURRECTION SANDBOX: twelve predetermined blank states once."""
import paths
from paths import HERE,ROOT,D,MOTOR
import ast,hashlib,json,shutil,time
import numpy as np
from loom_p.schema import Config,Streams
from loom_p.engine import Engine
from loom_p.prehistory import prepare,load
from loom_motor_commissioning import codec
from loom_motor_commissioning.motor import install,PARAMETERS
from sandbox_core import LABEL,initialize
from sandbox_runner import source_gate,atomic,canonical,file_hash

REQUEST=__import__('pathlib').Path(r'C:\Users\Jason\.codex\attachments\dc0d921d-6ccc-4baf-97d1-3cfecee174a8\Pasted text.txt')
def main():
    assert json.loads((HERE/'COMPONENT_TEST_REPORT.json').read_bytes())['status']=='PASS'
    assert json.loads((HERE/'RECORDER_COMPONENT_REPORT.json').read_bytes())['status']=='PASS'
    if (HERE/'PREPARATION_STARTED.json').exists():raise FileExistsError('No preparation restart or replacement birth')
    assert shutil.disk_usage(HERE).free>=30000000000
    runtime=source_gate();rh=hashlib.sha256(canonical(runtime)).hexdigest()
    atomic(HERE/'RUNTIME_IDENTITY.json',runtime)
    for name in ('prehistory','initial_states','birth_manifests','authorities','references'):(HERE/name).mkdir(exist_ok=False)
    shutil.copyfile(REQUEST,HERE/'references/JASON_SANDBOX_SPECIFICATION.txt')
    c=Config(**json.loads((D/'configuration.json').read_bytes()))
    roster=[dict(life_id=f'RS-M1-{i:03d}',stream_life=1000000+i,master_seed=c.master_seed,
        phase=float(Streams(c.master_seed,1000000+i).draw('world-phase',(1,))[0]*2*np.pi)) for i in range(1,13)]
    resource=dict(label=LABEL,worker_count=1,pilot_age=600.,maximum_common_age=4500.,
        allowed_common_ages=list(range(600,4501)),active_wall_ceiling_seconds=25200,primary_evidence_ceiling_bytes=8000000000,
        continuation_projection_fraction=.8,projection_fixed_verification_reserve_seconds=600,
        closure_reserve_bytes=32000000,required_free_before_execution_bytes=30000000000,minimum_free_during_execution_bytes=10000000000,
        archive_headroom_bytes=8000000000,temporary_headroom_bytes=8000000000,passive_analysis_headroom_bytes=2000000000,
        preparation_wall_guard_seconds=1200,recording=dict(native_dt=.01,wave_dt=.2,chunk_steps=100,checkpoint_stride=6000,compression_level=1),
        selection='After all twelve pilot receipts verify: use maximum observed per-life wall/age and bytes/age rates; include elapsed batch wall and stored bytes; reserve 600 s verification and 32 MB closure; choose greatest integer common total age <=4500 fitting 80% of both caps. No outcome variables enter.')
    prior=json.loads((ROOT/'motor_commissioning_results_20260930_v0_2/RESOURCE_ACTUALS.json').read_bytes())
    m1=[r for r in prior['cases'] if r['case_id'].endswith('-M1')]
    resource['prepilot_measured_M1_reference']=dict(max_wall_per_sim_s=max(r['wall_seconds']/90 for r in m1),
        max_bytes_per_sim_s=max(r['stored_bytes']/90 for r in m1),
        pilot_wall_projection_s=7200*max(r['wall_seconds']/90 for r in m1),
        full_4500_wall_projection_s=54000*max(r['wall_seconds']/90 for r in m1),
        caveat='New sandbox wave evidence and resurrection checkpoints add cost; only measured full pilot rates determine continuation target.')
    atomic(HERE/'RESOURCE_PLAN.json',resource)
    atomic(HERE/'PREPARATION_STARTED.json',dict(label=LABEL,roster=roster,runtime=rh,request_sha256=file_hash(REQUEST),
        fixed_before_birth_generation=True,ordinary_uniform_rejection=True,no_outcome_selection=True,
        stream_rule='Dedicated 1000001..1000012 range, disjoint from preserved FS-001..060 and MC-FS-001..003 streams; no prior sealed B1 material inspected.',
        new_prehistory='Exactly one ordinary body-absent 600 s field prehistory per declared new life; none regenerated during a life.'))
    source=ROOT/'founder_initial_packet_20260930/prepare_blank_starts.py'
    fn=next(n for n in ast.parse(source.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='verify_blank')
    exec(compile(ast.Module(body=[fn],type_ignores=[]),str(source),'exec'),globals())
    start=time.perf_counter();rows=[];anatomy=None
    try:
        for spec in roster:
            if time.perf_counter()-start>=1200:raise RuntimeError('preparation resource guard')
            name=spec['life_id'];stream=spec['stream_life'];cache=HERE/'prehistory'/name
            print(json.dumps(dict(label=LABEL,event='PREPARING_BLANK',life=name)),flush=True)
            m=prepare(c,cache,life=stream)
            tagged=json.loads((cache/'manifest.json').read_bytes());tagged['sandbox_label']=LABEL
            (cache/'manifest.json').write_bytes(canonical(tagged))
            fields,phase,rng,provenance=load(c,cache,life=stream)
            e=Engine(c,fields,phase,rng,provenance);blank=verify_blank(e)
            if anatomy is None:anatomy=blank['anatomy_sha256']
            assert anatomy==blank['anatomy_sha256'] and phase==spec['phase']
            install(e,'M1');initialize(e);e.validate_state()
            snapshot=codec.write(HERE/'initial_states'/(name+'.ld'),dict(label=LABEL,engine=e,identity=rh,life_id=name),1)
            restored=codec.read(HERE/'initial_states'/snapshot['file'],snapshot['sha256'])['engine']
            assert codec.encode(restored)==codec.encode(e)
            manifest=dict(label=LABEL,**spec,blank=blank,initial_snapshot=snapshot,initial_digest=codec.digest(e),
                position=e.body.position.tolist(),angle=e.body.angle,motor_state_sha256=codec.digest(e.organism.motor.commissioning),
                prehistory_manifest_sha256=file_hash(cache/'manifest.json'),prehistory_fields_sha256=file_hash(cache/'fields.npz'),
                prehistory_wall=m['wall_seconds'],organism_steps=0,runtime=rh)
            atomic(HERE/'birth_manifests'/(name+'.json'),manifest);rows.append(manifest)
        assert len({r['initial_digest'] for r in rows})==12
        authorities=[]
        for r in rows:
            a=dict(label=LABEL,kind='noncanonical-M1-resurrection-continuing-individual',life_id=r['life_id'],
                stream_life=r['stream_life'],initial_snapshot=r['initial_snapshot'],initial_digest=r['initial_digest'],
                runtime=rh,corrected_checkpoint='1d7cd6fd450ea528562b2c825589ab4de18a5b38',
                parameters_sha256=hashlib.sha256(canonical(PARAMETERS)).hexdigest(),configuration=c.identity(),
                pilot_age=600.,maximum_age=4500.,automatic_continuation='Only full pilot mechanical gates; exact same 12 states; common integer resource-derived target.',
                resource_plan_sha256=file_hash(HERE/'RESOURCE_PLAN.json'),specification_sha256=file_hash(REQUEST),
                intervention_code_sha256=file_hash(HERE/'sandbox_core.py'),retry=False,replacement=False,selection=False,
                authorization='Jason explicitly authorized implementation, preparation, pilot and conditional continuation in this task; no further review required.')
            ref=atomic(HERE/'authorities'/(r['life_id']+'.json'),a);authorities.append(dict(life_id=r['life_id'],sha256=ref['sha256']))
        atomic(HERE/'BLANK_START_VERIFICATION.json',dict(label=LABEL,status='PASS',rows=rows,common_anatomy_sha256=anatomy,
            new_independent_life_streams=[r['stream_life'] for r in rows],pilot_lives_executed=0,body_absent_preparation_steps=720000,
            verification_source_sha256=file_hash(source),wall_seconds=time.perf_counter()-start))
        atomic(HERE/'BATCH_AUTHORITY.json',dict(label=LABEL,authorities=authorities,runtime=rh,resource_plan_sha256=file_hash(HERE/'RESOURCE_PLAN.json'),
            user_authorization_sha256=file_hash(HERE/'JASON_OVERNIGHT_AUTHORIZATION.txt'),all_12_prepared_before_execution=True,
            stage_order=['12 pilots in declared order','mechanical gates and single common age decision','same 12 continuations in declared order'],
            one_worker=True,no_more_review_required=True))
        launch=f'''# NON-CANONICAL RESURRECTION SANDBOX — launch record

Twelve independently streamed blank M1 organisms are prepared. This is externally life-supported exploration, not Founder Search, ordinary viability, Nursery validation or canonical M1 acceptance.

Corrected checkpoint: 1d7cd6fd450ea528562b2c825589ab4de18a5b38. Base motor-screen runtime: 5df0ced8bf5602c84852bc2074fca8d422cc39cc55b9bab00a4b653bbe714c49. Sandbox runtime: {rh}.

M1 parameter hash: {hashlib.sha256(canonical(PARAMETERS)).hexdigest()}. Amplitude .35; latent SD .5; zero mean common; refresh 50 accepted native calls; common/differential OU times 16/8 s. The commissioned function, Gaussian law, stream labels and downstream motor equations are imported unchanged. Life streams 1000001–1000012 were fixed before birth/phase generation. Ordinary uniform-rejection positions, headings, full stocks, E=.7, I=1 and untouched blank P initialization. Each has one new lawful body-absent 600 s prehistory; never regenerate it during resurrection.

At a genuine terminal boundary, full before/after checkpoints and an explicit EXTERNAL_RESURRECTION_INTERVENTION preserve the event. Restore only nonviable dimensions; leave the other reserve unchanged. Align that dimension's regulator body_mean and association E/I packet mean to the restored reserve; clear that E/I packet trace. Discard all unfinished sensory/motor packet integrals and set wave_elapsed to zero. No handoff, credit, H write, bank/reference/eligibility update or RNG draw occurs at intervention. All other complete causal state is bitwise preserved, including sensory weights/references/means/coactivity, H/use, central a/q, regulator theta/reference/eligibility/phi/xi/controls, body velocity and motor tendencies/process state. Diagnostics remain historical caches. Assertions compare the entire protected state and probe credit only on a copy.

Clock semantics are explicit: absolute physical time and native/wave/history counts never reset. A fresh .2 s packet window begins at resurrection; the discarded partial window is recorded and never credited. Administrative age limits can close a fractional native call and retain its unfinished wave for continuation. Native counters count accepted integration calls, including fractions, and the commissioned M1/noise index rules remain unchanged. Fractional wave-closing intervals are bounded by .01 s. This scheduling adaptation is sandbox-only and bound into its runtime; no canonical function is patched. The ordinary unbroken path is exactly baseline-equivalent in component checks.

All twelve pilots run to exact age 600 before interpretation. Continuation requires all receipts and interventions to verify, exact checkpoint/RNG state round trips, no shared fault/corruption, and sufficient resources. Select the greatest integer common age in [600,4500] fitting 80% of 25200 s and 8 GB using the slowest/largest measured pilot rates, elapsed costs and declared closure/verification reserves. Never use contact, source benefit, survival or learned-state outcomes to select a target. One worker. Free-space gate 30 GB; 8 GB archive + 8 GB temporary + 2 GB passive outputs planned, with 10 GB minimum free during execution.

Stop immediately for any shared apparatus fault, nonfinite state, evidence/checkpoint/RNG mismatch, failed jump isolation, resource boundary or required scientific judgment. Preserve exact failed prefix and leave later cases unstarted. No retry, replacement, tuning, canon amendment, merge, push, PR or next experiment. Read COMPONENT_TEST_REPORT.json, RECORDER_COMPONENT_REPORT.json, RESOURCE_PLAN.json, BLANK_START_VERIFICATION.json and authorities/ for exact bindings.
'''
        (HERE/'LAUNCH_RECORD.md').write_text(launch,encoding='utf8')
        runtime_check=source_gate();assert hashlib.sha256(canonical(runtime_check)).hexdigest()==rh
        files=[dict(path=p.relative_to(HERE).as_posix(),sha256=file_hash(p),bytes=p.stat().st_size) for p in sorted(HERE.rglob('*')) if p.is_file() and not p.relative_to(HERE).parts[0].startswith('component_records')]
        atomic(HERE/'PREPARATION_MANIFEST.json',dict(label=LABEL,files=files))
        print(json.dumps(dict(label=LABEL,event='ALL_TWELVE_PREPARED',runtime=rh,batch_authority=file_hash(HERE/'BATCH_AUTHORITY.json'))),flush=True)
    except BaseException as error:
        atomic(HERE/'PREPARATION_STOP.json',dict(label=LABEL,reason=f'{type(error).__name__}: {error}',prepared=[r['life_id'] for r in rows]));raise
if __name__=='__main__':main()
