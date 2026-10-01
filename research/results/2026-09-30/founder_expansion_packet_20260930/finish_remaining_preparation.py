"""Finish only unprepared declared streams after the first preparation wall guard.

This is not a life continuation or field-history retry. Frozen production code is
unchanged. The first segment and its exact completed assets remain immutable.
"""
import hashlib
import json
import time
from pathlib import Path
import prepare_expansion as q

HERE=q.HERE; PACKET=q.PACKET
TOTAL_ACTIVE_GUARD=8000

def log(value):
    with (HERE/'REMAINING_PREPARATION_LOG.jsonl').open('ab') as f:
        f.write(q.canonical(value)+b'\n');f.flush()
    print(json.dumps(value),flush=True)

def main():
    started=time.perf_counter()
    if (HERE/'REMAINING_PREPARATION_STARTED.json').exists():
        raise FileExistsError('No second invocation; preserve this preparation boundary')
    hold=json.loads((HERE/'PREPARATION_HOLD.json').read_bytes())
    assert hold['error']=='RuntimeError: Preparation aggregate wall guard'
    assert hold['scientific_lives_executed']==0
    assert not (PACKET/'BLANK_START_VERIFICATION.json').exists()
    assert not (PACKET/'AUTHORITY_INDEX.json').exists()
    q.source_gate();assert hashlib.sha256(q.canonical(q.identity())).hexdigest()==q.RUNTIME
    c=q.Config(**json.loads((q.D/'configuration.json').read_bytes()))
    declaration=json.loads((PACKET/'ROSTER_DECLARATION.json').read_bytes())
    specs=declaration['roster']
    assert specs==[dict(life_id=f'FS-{i:03d}',stream_life=i,master_seed=c.master_seed,
        phase=float(q.Streams(c.master_seed,i).draw('world-phase',(1,))[0]*2*q.np.pi)) for i in range(13,61)]
    done=hold['completed'];assert done==[r['life_id'] for r in specs[:len(done)]] and 0<len(done)<48
    assert sorted(p.stem for p in (PACKET/'birth_manifests').glob('*.json'))==done
    assert sorted(p.stem for p in (PACKET/'initial_states').glob('*.ld'))==done
    assert sorted(p.name for p in (PACKET/'prehistory').iterdir())==done
    old_files=[dict(path=p.relative_to(PACKET).as_posix(),sha256=q.file_hash(p))
        for p in sorted(PACKET.rglob('*')) if p.is_file()]
    rows=[json.loads((PACKET/'birth_manifests'/(name+'.json')).read_bytes()) for name in done]
    prior=json.loads((q.ROOT/'exports/2026-09-30-Founder-Search-initial-stage/BLANK_START_VERIFICATION.json').read_bytes())
    common=prior['common_anatomy_sha256']
    for row in rows:
        e=q.codec.read(PACKET/'initial_states'/row['initial_snapshot']['file'],row['initial_snapshot']['sha256'])['engine']
        assert q.verify_blank(e)==row['blank'] and row['blank']['anatomy_sha256']==common
        assert q.codec.digest(q.core.causal_state(e))==row['initial_causal_sha256']
        assert q.state_hash(e)==row['initial_engine_sha256']
    old_log=[json.loads(s) for s in (HERE/'PREPARATION_LOG.jsonl').read_bytes().splitlines()]
    first_elapsed=max(max(r.get('preparation_elapsed_seconds',0) for r in old_log),
        (HERE/'PREPARATION_HOLD.json').stat().st_mtime-(HERE/'PREPARATION_STARTED.json').stat().st_mtime)
    assert first_elapsed>=4800
    notice=dict(status='PREPARATION_ONLY',reason='Measured body-absent field preparation became materially slower than the prior twelve. Finish the still-unprepared portion of Jason\'s requested 48; retain the original 80-minute guard stop.',
        original_guard_seconds=4800,total_active_preparation_guard_seconds=TOTAL_ACTIVE_GUARD,
        preparation_storage_guard_bytes=256000000,original_hold_sha256=q.file_hash(HERE/'PREPARATION_HOLD.json'),
        original_log_sha256=q.file_hash(HERE/'PREPARATION_LOG.jsonl'),first_segment_observed_seconds=first_elapsed,
        completed_preserved=done,only_newly_prepared=[r['life_id'] for r in specs[len(done):]],
        original_packet_file_bindings=old_files,driver_sha256=q.file_hash(__file__),
        scientific_native_calls=0,P_handoffs=0,scientific_lives_executed=0,
        frozen_checkpoint=q.CHECKPOINT,runtime_sha256=q.RUNTIME,
        life_execution_permission=False,request_sha256=q.file_hash(q.REQUEST))
    q.write(HERE/'REMAINING_PREPARATION_STARTED.json',notice)
    new_names=[]
    try:
        for spec in specs[len(done):]:
            if first_elapsed+time.perf_counter()-started>=TOTAL_ACTIVE_GUARD:
                raise RuntimeError('Revised aggregate preparation wall guard')
            name=spec['life_id'];life=spec['stream_life'];cache=PACKET/'prehistory'/name
            assert not cache.exists() and not (PACKET/'initial_states'/(name+'.ld')).exists()
            log(dict(preparing=name,body_absent=True,organism_time=0,earlier_histories_repeated=0))
            result=q.prepare(c,cache,life=life)
            fields,phase,rng,provenance=q.load(c,cache,life=life)
            assert phase==spec['phase'] and result['life']==life and not result['organism_created']
            e=q.Engine(c,fields,phase,rng,provenance);e.validate_state();blank=q.verify_blank(e)
            assert blank['anatomy_sha256']==common
            snapshot=q.codec.write(PACKET/'initial_states'/(name+'.ld'),dict(engine=e,identity=q.RUNTIME,index=0,wave=0,life_id=name),level=1)
            restored=q.codec.read(PACKET/'initial_states'/snapshot['file'],snapshot['sha256'])['engine']
            assert q.codec.encode(q.core.causal_state(e))==q.codec.encode(q.core.causal_state(restored))
            assert restored.organism.rng.life==life and q.verify_blank(restored)==blank
            manifest=dict(**spec,status='PREPARED_UNEXECUTED',blank=blank,
                initial_causal_sha256=q.codec.digest(q.core.causal_state(e)),initial_engine_sha256=q.state_hash(e),
                initial_snapshot=snapshot,runtime_sha256=q.RUNTIME,configuration_sha256=c.identity(),
                birth_provenance=dict(position=e.body.position.tolist(),angle=e.body.angle,phase=phase,
                    rejected=[dict(position=x['position'].tolist(),minimum_gap=x['minimum_gap']) for x in e.birth_provenance['rejected']]),
                initial_rng_counters=e.organism.rng.counters,
                prehistory=dict(path='prehistory/'+name,manifest_sha256=q.file_hash(cache/'manifest.json'),
                    field_array_sha256=result['field_sha256'],field_file_sha256=result['file_sha256'],
                    steps=result['steps_completed'],world_interval=[-600,0],wall_seconds=result['wall_seconds'],
                    body='absent',source_stocks='full_constant',initial_fields='zero',new_preparation=True),
                organism_time_advanced=0,no_outcome_selection=True)
            q.write(PACKET/'birth_manifests'/(name+'.json'),manifest);rows.append(manifest);new_names.append(name)
            log(dict(prepared=name,prepared_count=len(rows),native_steps=0,waves=0,
                snapshot_sha256=snapshot['sha256'],initial_causal_sha256=manifest['initial_causal_sha256'],
                aggregate_active_preparation_seconds=first_elapsed+time.perf_counter()-started))
            if sum(p.stat().st_size for p in PACKET.rglob('*') if p.is_file())>=256000000:
                raise RuntimeError('Preparation storage guard')
        assert len(rows)==48 and len({r['initial_causal_sha256'] for r in rows})==48
        assert not {r['initial_causal_sha256'] for r in prior['rows']}.intersection(r['initial_causal_sha256'] for r in rows)
        assert all(q.file_hash(PACKET/r['path'])==r['sha256'] for r in old_files)
        q.source_gate();assert hashlib.sha256(q.canonical(q.identity())).hexdigest()==q.RUNTIME
        active=first_elapsed+time.perf_counter()-started;assert active<TOTAL_ACTIVE_GUARD
        proof=dict(status='PASS',lives=48,rows=rows,common_anatomy_sha256=common,
            ordinary_blank_initialization=True,new_independent_streams=list(range(13,61)),
            all_initial_snapshots_distinct_from_first_twelve=True,scientific_native_steps=0,scientific_wave_handoffs=0,
            scientific_lives_executed=0,body_absent_prehistories=48,prehistory_world_steps=2880000,
            wall_seconds=active,clock_basis='Sum of measured preparation segments; intervening review gap excluded',
            elapsed_since_initial_preparation_marker_seconds=time.time()-(HERE/'PREPARATION_STARTED.json').stat().st_mtime,
            preparation_aggregate_wall_guard_seconds=TOTAL_ACTIVE_GUARD,
            first_segment_observed_seconds=first_elapsed,remaining_segment_seconds=time.perf_counter()-started,
            original_guard_stop_preserved=True,earlier_preparation_assets_unchanged=True,field_histories_repeated=0,
            runtime_sha256=q.RUNTIME,code_configuration_unchanged=True)
        q.write(PACKET/'BLANK_START_VERIFICATION.json',proof)
        resolution=dict(status='PASS',original_hold_sha256=notice['original_hold_sha256'],
            original_log_sha256=notice['original_log_sha256'],completed_preserved=done,newly_prepared=new_names,
            revised_preparation_notice_sha256=q.file_hash(HERE/'REMAINING_PREPARATION_STARTED.json'),
            blank_verification_sha256=q.file_hash(PACKET/'BLANK_START_VERIFICATION.json'),
            original_packet_files_unchanged=len(old_files),field_histories_repeated=0,
            all_48_time_zero=True,scientific_lives_executed=0,active_preparation_seconds=active,
            interpretation='Administrative preparation boundary only. No life started, restarted or continued. Only previously unprepared declared streams were prepared.')
        q.write(HERE/'PREPARATION_BOUNDARY_RESOLUTION.json',resolution)
        log(dict(status='PREPARATION_COMPLETE',prepared=48,scientific_lives_executed=0,all_organism_times=0))
    except BaseException as error:
        q.write(HERE/'REMAINING_PREPARATION_HOLD.json',dict(error=f'{type(error).__name__}: {error}',
            completed=[r['life_id'] for r in rows],scientific_lives_executed=0,no_retry_or_substitution=True))
        raise

if __name__=='__main__':main()
