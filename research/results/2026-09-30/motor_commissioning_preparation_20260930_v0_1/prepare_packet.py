"""Snapshot copies, content identities and proposed scopes only; no launch."""
import paths
from paths import HERE,ROOT,PACKET,D,WT
import copy,hashlib,json,shutil
from loom_p.engine import Engine
from loom_p.neural import Organism
from loom_p.chemistry import FieldSolver
from loom_p import physics
from loom_developmental import core
from loom_motor_commissioning import codec
from loom_motor_commissioning.motor import install,PARAMETERS
from loom_motor_commissioning.runner import identity,canonical,file_hash
from preflight import ORDER,P,BASE,git

counts={'forbidden_evolution_calls':0}
def forbidden(*args,**kwargs):
    counts['forbidden_evolution_calls']+=1
    raise RuntimeError('Preparation is not authorized to evolve a world or organism')
Engine.step=Engine._coupled=Organism.native=Organism.handoff=FieldSolver.step=physics.advance=forbidden

def save(name,value):
    path=HERE/name
    if path.exists():raise FileExistsError(path)
    path.parent.mkdir(exist_ok=True,parents=True)
    path.write_bytes(canonical(value))
    return file_hash(path)

assert git('rev-parse','HEAD')==BASE and git('status','--porcelain')==''
runtime=identity();runtime_hash=save('RUNTIME_IDENTITY.json',runtime)
parameter_hash=save('PARAMETERS.json',PARAMETERS)
ref=json.loads((HERE/'AMPLITUDE_EFFORT_REFERENCE.json').read_bytes())
resource=dict(schema=1,simulated_seconds_per_case=90,total_simulated_seconds=810,
    active_wall_seconds_per_case=300,active_wall_seconds_batch=2700,stored_bytes_per_case=32000000,
    stored_bytes_batch=288000000,closure_reserve_bytes_per_case=16000000,
    preflight_wall_seconds_total=300,verification_wall_seconds_total=600,archive_report_planning_seconds=300,
    required_free_bytes_before_batch=2000000000,required_free_bytes_before_each_case=1000000000,
    reference_rates=ref['resource'],extra_wave_diagnostic_planning_bytes_per_case=2000000,
    record_fidelity='unchanged native Tier-1 plus compact per-wave already-computed motor/process values',
    resource_stop='stop batch, preserve prefix, no continuation/redistribution',
    qualifications=['Rates are historical, not a benchmark of candidates.','Different contacts may cost more.',
        'Checks occur before a native step; one in-flight operation/closure can overrun wall limit.',
        'FS-060 interruption remains unexplained. No blanket reliability claim.'])
save('RESOURCE_PLAN.json',resource)
execution_files={p:file_hash(HERE/p) for p in ('paths.py','preflight.py','execute_after_authorization.py','EXECUTION_PROTOCOL.md','ANALYSIS_PLAN.md','RESOURCE_PLAN.json')}
manifests=[];proofs=[]
for i in (1,2,3):
    old_a=json.loads((PACKET/'authorities'/f'FS-{i:03d}.json').read_bytes())
    original=codec.read(PACKET/old_a['initial_snapshot']['path'],old_a['initial_snapshot']['sha256'])
    base=original['engine'];assert base.native_index==base.time==base.organism.native_count==0
    assert codec.digest(core.causal_state(base))==old_a['runner_scope']['initial_causal_sha256']
    pre=old_a['prehistory']
    old_files={old_a['birth_manifest']['path']:old_a['birth_manifest']['sha256'],
        pre['path']+'/manifest.json':pre['manifest_sha256'],pre['path']+'/fields.npz':pre['field_file_sha256']}
    for rel,h in old_files.items():assert file_hash(PACKET/rel)==h
    shutil.copyfile(PACKET/old_a['birth_manifest']['path'],HERE/f'FS-{i:03d}_ORIGINAL_BIRTH_MANIFEST.json')
    for process in ('CURRENT','M1','M2'):
        name=f'MC-FS-{i:03d}-{process}'
        e=install(copy.deepcopy(base),process);e.validate_state()
        e2=copy.deepcopy(e)
        if process!='CURRENT':del e2.organism.motor.commissioning
        assert codec.encode(e2)==codec.encode(base)
        s=dict(engine=e,identity=runtime_hash,index=0,wave=0,life_id=name)
        path=HERE/'initial_states'/(name+'.ld');record=codec.write(path,s)
        state=dict(process=process,baseline_motor=vars(base.organism.motor),
            candidate_process=getattr(e.organism.motor,'commissioning',None))
        # Exact typed initial process bytes (included in the all-state snapshot).
        state_hash=codec.digest(state)
        scope=dict(schema=1,kind='motor-temporal-commissioning',life_id=name,
            initial_causal_sha256=codec.digest(core.causal_state(e)),initial_index=0,end_index=9000,
            parent_receipt_sha256=None,wall_limit_seconds=300,storage_limit_bytes=32000000,
            checkpoint_stride=6000,chunk_steps=100,compression_level=1,process=process,parameters_sha256=parameter_hash)
        a=dict(schema=1,status='PROPOSED_UNAUTHORIZED',kind='motor-temporal-commissioning',case_id=name,
            ordinal=len(manifests)+1,fixed_order=ORDER,process=process,
            original_life=f'FS-{i:03d}',master_seed=5284097,life_stream=i,
            P_baseline_commit=P,lean_base_checkpoint=BASE,P_baseline_code_sha256=runtime['P']['sha256'],
            identity_claim='CURRENT delegates to frozen P; M1/M2 replace only spontaneous motor summand through separately bound overlay; P learning/world remain frozen',
            runtime_sha256=runtime_hash,configuration_sha256=base.c.identity(),
            configuration_file_sha256=file_hash(D/'configuration.json'),baseline_contract_sha256=file_hash(D/'loom_commissioning/contract.py'),
            parameters_sha256=parameter_hash,original_snapshot=old_a['initial_snapshot'],
            prepared_snapshot=dict(record,path='initial_states/'+path.name),
            initial_process_state_sha256=state_hash,preserved_preparation_files=old_files,
            execution_files=execution_files,runner_scope=scope,simulation_seconds=90,maximum_native_steps=9000,
            external_controller=None,new_prehistory=False,birth_law='original ordinary uniform-rejection fixtures reused without resampling',
            retry=False,continuation=False,replacement=False,outcome_tuning=False,automatic_selection=False,
            source_contact_can_determine_preference=False)
        ah=save('authorities/'+name+'.json',a)
        manifests.append(dict(case_id=name,authority_sha256=ah))
        proofs.append(dict(case_id=name,original_snapshot_sha256=old_a['initial_snapshot']['sha256'],
            prepared_snapshot_sha256=record['sha256'],original_engine_typed_sha256=codec.digest(base),
            physical_body_sha256=codec.digest(e.body),fields_sha256=hashlib.sha256(e.fields.tobytes()).hexdigest(),
            original_rng_sha256=codec.digest(e.organism.rng),original_after_removing_only_new_process_sha256=codec.digest(e2),
            complete_original_state_unchanged_except_added_candidate_process=True,
            initial_native_index=0,initial_time=0.,initial_wave_index=0,
            original_birth_position=base.body.position.tolist(),original_birth_angle=float(base.body.angle),original_mover_phase=base.phase,
            prepared_process_state=(None if process=='CURRENT' else {
                k:(v.tolist() if hasattr(v,'tolist') else (vars(v) if k=='rng' else v))
                for k,v in e.organism.motor.commissioning.items()})))
save('MATRIX.json',dict(status='PROPOSED_UNAUTHORIZED',cases=manifests))
save('MATCHED_INITIAL_STATE_PROOF.json',dict(cases=proofs,mechanism_state_is_intentionally_different=True))
save('PREPARATION_BOUNDARY.json',dict(**counts,world_steps=0,organism_steps=0,learning_handoffs=0,
    newly_generated_prehistories=0,world_cases_started=0,candidate_selection=False,
    component_execution_separate_from_world_execution=True,runner_checkpoint=BASE,branch=git('branch','--show-current'),
    worktree=str(WT),git_clean=True,original_birth_law_retained=True,nursery_configuration_changed=False))
print(json.dumps(dict(runtime_sha256=runtime_hash,parameters_sha256=parameter_hash,cases=manifests),indent=2))
