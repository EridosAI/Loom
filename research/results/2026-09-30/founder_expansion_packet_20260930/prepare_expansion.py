"""Prepare streams 13..60 once; body-absent histories and ordinary time-zero birth only."""
import hashlib
import json
from pathlib import Path
import shutil
import sys
import time
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
W=ROOT/'worktrees/loom-p-b1-minimal-20260929'
D=W/'developmental_ecology'
PACKET=ROOT/'exports/2026-09-30-Founder-Search-expansion-48'
PRIOR=ROOT/'founder_initial_execution_20260930'
REQUEST=Path(r'C:\Users\Jason\.codex\attachments\64113455-37d9-41fd-bd0f-4aaf5408a289\Pasted text.txt')
sys.path.insert(0,str(D))
sys.path.insert(0,str(ROOT/'founder_initial_packet_20260930'))
sys.path.insert(0,str(PRIOR))
from loom_p.schema import Config,Streams
from loom_p.prehistory import prepare,load
from loom_p.engine import Engine
from loom_p.records import state_hash,code_identity
from loom_developmental import codec,core
from loom_developmental.runner import identity,canonical,file_hash,atomic_json
from prepare_blank_starts import verify_blank
from execute_authorized_stage import source_gate,CHECKPOINT,P,RUNTIME,git

def write(path,value):atomic_json(Path(path),value)

def log(value):
    with (HERE/'PREPARATION_LOG.jsonl').open('ab') as f:f.write(canonical(value)+b'\n');f.flush()
    print(json.dumps(value),flush=True)

def main():
    if PACKET.exists() or (HERE/'PREPARATION_STARTED.json').exists():
        raise FileExistsError('Preserve an existing preparation; no overwrite, rephase or replacement')
    source_gate()
    runtime=identity();runtime_sha=hashlib.sha256(canonical(runtime)).hexdigest()
    assert runtime_sha==RUNTIME
    c=Config(**json.loads((D/'configuration.json').read_bytes()))
    assert c.master_seed==5284097
    first=json.loads((PRIOR/'DENOMINATOR_SEALED.json').read_bytes())
    delivery=json.loads((PRIOR/'DELIVERY_VERIFICATION.json').read_bytes())
    assert delivery['status']=='PASS' and first['batch_stop'] is None
    assert [r['life_id'] for r in first['roster']]==[f'FS-{i:03d}' for i in range(1,13)]
    for r in first['roster']:
        assert r['state']=='terminal' and r['complete']
        assert file_hash(PRIOR/'lives'/r['life_id']/'segment-000.json')==r['receipt_sha256']
    assert shutil.disk_usage(HERE).free>=11500000000
    # Harmless scoped access check, removed before generation.
    check=HERE/'SCOPED_ACCESS_CHECK.tmp'
    with check.open('xb') as f:f.write(b'Loom expansion preparation access check')
    assert check.read_bytes()==b'Loom expansion preparation access check';check.unlink()
    PACKET.mkdir()
    for name in ('prehistory','initial_states','birth_manifests','shared','references','authorities'):(PACKET/name).mkdir()
    shutil.copyfile(REQUEST,PACKET/'references/JASON_EXPANSION_REQUEST.txt')
    write(PACKET/'shared'/(runtime_sha+'.json'),runtime)
    measured=first['roster'];seconds=sum(r['simulated_seconds'] for r in measured)
    wall=first['active_execution_wall_seconds'];stored=first['closed_life_bytes']
    oldprep=json.loads((ROOT/'exports/2026-09-30-Founder-Search-initial-stage/BLANK_START_VERIFICATION.json').read_bytes())
    projection=dict(status='PREPARATION_ONLY_NOT_EXECUTION_PERMISSION',basis='Measured FS-001 through FS-012; no new trajectory run for projections',
        measured_lives=12,measured_simulated_seconds=seconds,measured_wall_seconds=wall,measured_primary_bytes=stored,
        weighted_wall_per_sim=wall/seconds,worst_observed_life_wall_per_sim=max(r['active_wall_seconds']/r['simulated_seconds'] for r in measured),
        weighted_bytes_per_sim=stored/seconds,worst_observed_life_bytes_per_sim=max(r['primary_bytes']/r['simulated_seconds'] for r in measured),
        full_600_all_48_wall_seconds=wall/seconds*600*48,
        full_600_all_48_slowest_observed_rate_wall_seconds=max(r['active_wall_seconds']/r['simulated_seconds'] for r in measured)*600*48,
        full_600_all_48_primary_bytes=round(stored/seconds*600*48),
        full_600_all_48_largest_observed_rate_primary_bytes=round(max(r['primary_bytes']/r['simulated_seconds'] for r in measured)*600*48),
        historical_duration_scenario_only_wall_seconds=wall*4,historical_duration_scenario_only_primary_bytes=stored*4,
        horizons_not_shortened=True,each_end_index=60000,per_life_wall_limit_seconds=332,per_life_storage_limit_bytes=83333333,
        execution_allowance_seconds=48*332,aggregate_primary_limit_bytes=4000000000,archive_limit_bytes=4000000000,
        temporary_headroom_bytes=1000000000,derived_analysis_limit_bytes=2500000000,total_additional_planning_bytes=11500000000,
        full_preflight_allowance_seconds=480,postrun_validation_allowance_seconds=720,archive_allowance_seconds=480,
        passive_analysis_wall_limit_seconds=4500,concurrent_lives=1,worker_working_set_planning_bytes=500000000,
        worker_commit_planning_bytes=2500000000,recording_chunk_steps=100,checkpoint_stride=6000,compression_level=1,
        expected_body_absent_preparation_seconds=oldprep['wall_seconds']*4,preparation_aggregate_wall_guard_seconds=4800,
        preparation_storage_guard_bytes=256000000,prior_denominator_sha256=file_hash(PRIOR/'DENOMINATOR_SEALED.json'),
        prior_delivery_sha256=file_hash(PRIOR/'DELIVERY_VERIFICATION.json'),
        caution='Linear projections from the first twelve are not guarantees for contact-rich or energy-extended lives. Exact per-life and aggregate guards govern. No tuning or replacement if a bound is reached.')
    write(PACKET/'RESOURCE_PROJECTION_BEFORE_AUTHORITY.json',projection)
    prospective=[dict(life_id=f'FS-{i:03d}',stream_life=i,master_seed=c.master_seed,
        phase=float(Streams(c.master_seed,i).draw('world-phase',(1,))[0]*2*np.pi)) for i in range(13,61)]
    write(PACKET/'ROSTER_DECLARATION.json',dict(status='PREPARATION_ONLY',roster=prospective,
        selection='The next consecutive life streams 13..60; fixed before generating fields or positions; no proximity/outcome selection.',
        same_anatomy=True,ordinary_birth_rejection_only='Unchanged Engine constructor overlap/clearance rejection. No additional source-distance filtering.',
        each_seconds_ceiling=600,each_native_ceiling=60000,initial_states_reused=0,continuations=0,replacements=0,
        request_sha256=file_hash(REQUEST),checkpoint=CHECKPOINT,P_commit=P,runtime_sha256=runtime_sha,
        known_founder_stream_inventory={'preserved_executed':list(range(1,13)),'new_fixed':list(range(13,61)),
        'scope':'Existing Founder roster/manifests checked; old sealed human B1 evaluator material not accessed.'}))
    write(HERE/'PREPARATION_STARTED.json',dict(checkpoint=CHECKPOINT,P_commit=P,runtime_sha256=runtime_sha,
        branch=git('branch','--show-current'),git_clean=True,request_sha256=file_hash(REQUEST),
        scoped_access_check='PASS',scientific_native_calls=0,scientific_Life_objects=0,preparation_driver_sha256=file_hash(__file__)))
    started=time.perf_counter();rows=[];common=oldprep['common_anatomy_sha256']
    try:
        for spec in prospective:
            if time.perf_counter()-started>=4800:raise RuntimeError('Preparation aggregate wall guard')
            name=spec['life_id'];life=spec['stream_life'];cache=PACKET/'prehistory'/name
            log(dict(preparing=name,body_absent=True,organism_time=0))
            result=prepare(c,cache,life=life)
            fields,phase,rng,provenance=load(c,cache,life=life)
            assert phase==spec['phase'] and result['life']==life and not result['organism_created']
            e=Engine(c,fields,phase,rng,provenance);e.validate_state();blank=verify_blank(e)
            assert blank['anatomy_sha256']==common
            snapshot=codec.write(PACKET/'initial_states'/(name+'.ld'),dict(engine=e,identity=runtime_sha,index=0,wave=0,life_id=name),level=1)
            restored=codec.read(PACKET/'initial_states'/snapshot['file'],snapshot['sha256'])['engine']
            assert codec.encode(core.causal_state(e))==codec.encode(core.causal_state(restored))
            assert restored.organism.rng.life==life and verify_blank(restored)==blank
            manifest=dict(**spec,status='PREPARED_UNEXECUTED',blank=blank,
                initial_causal_sha256=codec.digest(core.causal_state(e)),initial_engine_sha256=state_hash(e),
                initial_snapshot=snapshot,runtime_sha256=runtime_sha,configuration_sha256=c.identity(),
                birth_provenance=dict(position=e.body.position.tolist(),angle=e.body.angle,phase=phase,
                    rejected=[dict(position=x['position'].tolist(),minimum_gap=x['minimum_gap']) for x in e.birth_provenance['rejected']]),
                initial_rng_counters=e.organism.rng.counters,
                prehistory=dict(path='prehistory/'+name,manifest_sha256=file_hash(cache/'manifest.json'),
                    field_array_sha256=result['field_sha256'],field_file_sha256=result['file_sha256'],
                    steps=result['steps_completed'],world_interval=[-600,0],wall_seconds=result['wall_seconds'],
                    body='absent',source_stocks='full_constant',initial_fields='zero',new_preparation=True),
                organism_time_advanced=0,no_outcome_selection=True)
            write(PACKET/'birth_manifests'/(name+'.json'),manifest);rows.append(manifest)
            log(dict(prepared=name,prepared_count=len(rows),native_steps=0,waves=0,
                snapshot_sha256=snapshot['sha256'],initial_causal_sha256=manifest['initial_causal_sha256'],
                preparation_elapsed_seconds=time.perf_counter()-started))
            if sum(p.stat().st_size for p in PACKET.rglob('*') if p.is_file())>=256000000:
                raise RuntimeError('Preparation storage guard')
        assert len(rows)==48 and len({r['initial_causal_sha256'] for r in rows})==48
        oldhashes={r['initial_causal_sha256'] for r in oldprep['rows']}
        assert not oldhashes.intersection(r['initial_causal_sha256'] for r in rows)
        source_gate();assert hashlib.sha256(canonical(identity())).hexdigest()==runtime_sha
        assert time.perf_counter()-started<4800
        write(PACKET/'BLANK_START_VERIFICATION.json',dict(status='PASS',lives=48,rows=rows,
            common_anatomy_sha256=common,ordinary_blank_initialization=True,new_independent_streams=list(range(13,61)),
            all_initial_snapshots_distinct_from_first_twelve=True,scientific_native_steps=0,scientific_wave_handoffs=0,
            scientific_lives_executed=0,body_absent_prehistories=48,prehistory_world_steps=2880000,
            wall_seconds=time.perf_counter()-started,runtime_sha256=runtime_sha,code_configuration_unchanged=True))
        log(dict(status='PREPARATION_COMPLETE',prepared=48,scientific_lives_executed=0,all_organism_times=0))
    except BaseException as error:
        write(HERE/'PREPARATION_HOLD.json',dict(error=f'{type(error).__name__}: {error}',completed=[r['life_id'] for r in rows],
            no_retry_or_substitution=True,scientific_lives_executed=0))
        raise

if __name__=='__main__':main()
