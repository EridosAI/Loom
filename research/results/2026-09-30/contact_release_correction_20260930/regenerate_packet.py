"""Prepare fresh authorities and identity wrappers only; all evolution prohibited."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
OLD=ROOT/'motor_commissioning_preparation_20260930_v0_1'
NEW=ROOT/'motor_commissioning_preparation_20260930_v0_2'
WT=ROOT/'worktrees/loom-contact-release-20260930';D=WT/'developmental_ecology'
def git(*args):return subprocess.check_output(['git','-c','safe.directory='+WT.as_posix(),'--no-optional-locks','-C',str(WT),*args],text=True).strip()
checkpoint=git('rev-parse','HEAD');assert git('status','--porcelain')==''
NEW.mkdir(exist_ok=False);(NEW/'initial_states').mkdir();(NEW/'authorities').mkdir();(NEW/'tests').mkdir()
for name in ('loom_motor_commissioning','tests'):
    if name=='loom_motor_commissioning':shutil.copytree(OLD/name,NEW/name,ignore=shutil.ignore_patterns('__pycache__'))
    else:shutil.copyfile(OLD/name/'test_components.py',NEW/name/'test_components.py')
for name in ('paths.py','preflight.py','execute_after_authorization.py','ANALYSIS_PLAN.md','RESOURCE_PLAN.json','PARAMETERS.json','AMPLITUDE_EFFORT_REFERENCE.json'):
    shutil.copyfile(OLD/name,NEW/name)
for i in (1,2,3):shutil.copyfile(OLD/f'FS-{i:03d}_ORIGINAL_BIRTH_MANIFEST.json',NEW/f'FS-{i:03d}_ORIGINAL_BIRTH_MANIFEST.json')
def replace(name,old,new):
    p=NEW/name;s=p.read_text(encoding='utf8');assert old in s,(name,old);p.write_text(s.replace(old,new),encoding='utf8')
replace('paths.py','loom-p-b1-minimal-20260929','loom-contact-release-20260930')
replace('preflight.py',"BASE='87abae34e19d4e46234402a6b1ba776814956ec1'",f"BASE='{checkpoint}'")
replace('preflight.py',"a['lean_base_checkpoint']==BASE","a['lean_base_checkpoint']=='87abae34e19d4e46234402a6b1ba776814956ec1' and a['corrected_apparatus_checkpoint']==BASE")
replace('preflight.py',"a['P_baseline_code_sha256']==code_identity()['sha256']","a['P_baseline_code_sha256']=='63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9' and a['corrected_body_code_sha256']==code_identity()['sha256']")
replace('preflight.py',"assert a['status']=='PROPOSED_UNAUTHORIZED'", "assert a['screen_id']=='MOTOR_COMMISSIONING_v0_2_CORRECTED_APPARATUS'\n        assert a['status']=='PROPOSED_UNAUTHORIZED'")
replace('loom_motor_commissioning/runner.py','result=baseline_identity()',"result=baseline_identity(expected_p_code='98bbf9053ca55ef545c6fc868e54c85342149d143319281a47f9a1fd71c28c7d')")
replace('loom_motor_commissioning/runner.py',"result['claim']='frozen P core/world with explicitly identified experimental spontaneous motor overlay'",f"result['claim']='P neural mechanism/configuration and motor laws fixed; explicit contact-face apparatus correction; separately identified spontaneous motor overlay'\n    result['contact_correction_checkpoint']='{checkpoint}'\n    result['historical_P_baseline']='6bc9683b54e4fa80136fe8534d7713e2a250a95f'")
# Preserve execution semantics, but name this fresh dataset explicitly.
replace('execute_after_authorization.py',"dict(authorization_sha256=file_hash(auth_path)","dict(screen_id='MOTOR_COMMISSIONING_v0_2_CORRECTED_APPARATUS',authorization_sha256=file_hash(auth_path)")
protocol=(OLD/'EXECUTION_PROTOCOL.md').read_text(encoding='utf8')
protocol=protocol.replace('Only after separate explicit Jason authorization','This is a NEW screen under the corrected common apparatus, not a retry, replacement or continuation of MOTOR_COMMISSIONING_RESULT_v0_1. Original records remain immutable.\n\nOnly after separate explicit Jason authorization')
protocol=protocol.replace('unchanged lean runner/P checkout','corrected contact apparatus checkout')
protocol=protocol.replace('learning, world, physics, fields and lean transaction/terminal scheduler remain the original implementations','learning, world constitutive laws, fields and lean transaction/terminal scheduler remain unchanged; physics has the separately bound certified face-to-corner correction')
(NEW/'EXECUTION_PROTOCOL.md').write_text(protocol,encoding='utf8')
sys.path[:0]=[str(NEW),str(D)]
from loom_p.engine import Engine
from loom_p.neural import Organism
from loom_p.chemistry import FieldSolver
from loom_p import physics
from loom_developmental import core
from loom_motor_commissioning import codec
from loom_motor_commissioning.runner import identity,canonical,file_hash
from loom_motor_commissioning.motor import PARAMETERS
counts={'forbidden_evolution_calls':0}
def forbidden(*args,**kw):
    counts['forbidden_evolution_calls']+=1
    raise RuntimeError('No evolution in packet preparation')
Engine.step=Engine._coupled=Organism.native=Organism.handoff=FieldSolver.step=physics.advance=forbidden
def save(name,v):
    p=NEW/name;assert not p.exists(),p;p.write_bytes(canonical(v));return file_hash(p)
runtime=identity();rh=save('RUNTIME_IDENTITY.json',runtime)
execution={name:file_hash(NEW/name) for name in ('paths.py','preflight.py','execute_after_authorization.py','EXECUTION_PROTOCOL.md','ANALYSIS_PLAN.md','RESOURCE_PLAN.json')}
matrix=[];proof=[];diffs=[]
for row in json.loads((OLD/'MATRIX.json').read_bytes())['cases']:
    name=row['case_id'];a=json.loads((OLD/'authorities'/(name+'.json')).read_bytes())
    prior=codec.read(OLD/a['prepared_snapshot']['path'],a['prepared_snapshot']['sha256'])
    e=prior['engine'];state=codec.digest(e)
    new=dict(prior,identity=rh)
    record=codec.write(NEW/a['prepared_snapshot']['path'],new)
    assert codec.digest(codec.read(NEW/a['prepared_snapshot']['path'])['engine'])==state
    b=dict(a,screen_id='MOTOR_COMMISSIONING_v0_2_CORRECTED_APPARATUS',
        corrected_apparatus_checkpoint=checkpoint,corrected_body_code_sha256=runtime['P']['sha256'],
        historical_authority_sha256=row['authority_sha256'],
        identity_claim='P neural mechanism, world constitutive laws and parameters unchanged; corrected contact-event solver common to all nine cases; unchanged declared spontaneous processes',
        runtime_sha256=rh,prepared_snapshot=dict(record,path=a['prepared_snapshot']['path']),execution_files=execution)
    ah=save('authorities/'+name+'.json',b);assert ah!=row['authority_sha256']
    matrix.append(dict(case_id=name,authority_sha256=ah))
    proof.append(dict(case_id=name,old_engine_sha256=state,new_engine_sha256=state,complete_engine_bytes_identical=True,
        original_snapshot_sha256=a['original_snapshot']['sha256'],physical_body_sha256=codec.digest(e.body),
        fields_sha256=hashlib.sha256(e.fields.tobytes()).hexdigest(),original_rng_sha256=codec.digest(e.organism.rng),
        initial_causal_sha256=codec.digest(core.causal_state(e)),process_state_sha256=a['initial_process_state_sha256']))
    changed=[k for k in sorted(set(a)|set(b)) if a.get(k)!=b.get(k)]
    assert set(changed)=={'screen_id','corrected_apparatus_checkpoint','corrected_body_code_sha256','historical_authority_sha256','identity_claim','runtime_sha256','prepared_snapshot','execution_files'}
    diffs.append(dict(case_id=name,changed_fields=changed,classification='IDENTITY_AND_EXPLICIT_APPARATUS_CORRECTION_ONLY',unchanged_runner_scope=b['runner_scope']==a['runner_scope']))
for start in (proof[:3],proof[3:6],proof[6:]):
    for field in ('original_snapshot_sha256','physical_body_sha256','fields_sha256','original_rng_sha256'):assert len({r[field] for r in start})==1
save('MATRIX.json',dict(status='PROPOSED_UNAUTHORIZED',screen_id='MOTOR_COMMISSIONING_v0_2_CORRECTED_APPARATUS',cases=matrix))
save('MATCHED_INITIAL_STATE_PROOF.json',dict(cases=proof,old_prepared_engines_preserved_byte_for_byte=True))
save('SEMANTIC_DIFF.json',dict(cases=diffs,motor_py_identical=file_hash(NEW/'loom_motor_commissioning/motor.py')==file_hash(OLD/'loom_motor_commissioning/motor.py'),
    parameters_identical=file_hash(NEW/'PARAMETERS.json')==file_hash(OLD/'PARAMETERS.json'),
    analysis_criteria_identical=file_hash(NEW/'ANALYSIS_PLAN.md')==file_hash(OLD/'ANALYSIS_PLAN.md'),
    resource_recording_limits_identical=file_hash(NEW/'RESOURCE_PLAN.json')==file_hash(OLD/'RESOURCE_PLAN.json'),
    unexpected_semantic_changes=[]))
save('PREPARATION_BOUNDARY.json',dict(**counts,world_steps=0,organism_steps=0,new_prehistory=0,new_screen_cases_started=0,
    corrected_apparatus_checkpoint=checkpoint,git_clean=True,old_batch_preserved=True,automatic_selection=False))
from preflight import check
save('STATIC_PREFLIGHT_REPORT.json',check())
(NEW/'AUTHORITY_INDEX.md').write_text('# Fresh v0.2 proposals — NOT AUTHORIZED\n\nAll nine are independent cases under one corrected apparatus. No old authorization applies.\n\n'+ '\n'.join(f"{i}. **{r['case_id']}** — `{r['authority_sha256']}`" for i,r in enumerate(matrix,1))+'\n',encoding='utf8')
print(json.dumps(dict(checkpoint=checkpoint,runtime_sha256=rh,cases=matrix),indent=2))
