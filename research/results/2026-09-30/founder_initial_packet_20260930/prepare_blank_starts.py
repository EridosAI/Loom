"""Prepare the fixed twelve ordinary birth states; no organism steps or outcomes."""
import hashlib
import json
from pathlib import Path
import sys
import time
import numpy as np

ROOT=Path(__file__).resolve().parent.parent
HERE=Path(__file__).resolve().parent
D=ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'
PACKET=ROOT/'exports/2026-09-30-Founder-Search-initial-stage'
sys.path.insert(0,str(D))
from loom_p.schema import Config,Streams
from loom_p.prehistory import prepare,load
from loom_p.engine import Engine
from loom_p.records import state_hash,code_identity
from loom_developmental import codec,core
from loom_developmental.runner import identity,canonical,file_hash

def write(path,obj):
    path=Path(path)
    if path.exists():raise FileExistsError(path)
    path.write_bytes(canonical(obj))

def verify_blank(e):
    c=e.c;o=e.organism;a=o.association;r=o.regulator;m=o.motor
    assert not hasattr(e,'fixture')
    assert e.time==e.native_index==o.native_count==o.wave_count==o.wave_elapsed==a.write_count==0
    assert e.status=='paused' and e.failure is None and e.terminal_dimension is None
    assert e.body.energy==c.birth_energy==.7 and e.body.integrity==1
    assert np.array_equal(e.stocks,np.full(8,c.source_capacity))
    assert all(not np.any(x) for x in (*a.H.values(),*a.use.values(),a.a,a.q,*a.traces,r.theta,r.reference,r.eligibility,m.command,m.tendency,m.integral,e.body.velocity,e.body.force,e.body.command,e.body.contact_rates))
    assert e.body.omega==0 and np.array_equal(r.body_mean,e.body.reserves)
    for i,x in enumerate(o.cortices):
        assert np.array_equal(x.shared,x.shared_ref) and np.array_equal(x.fine,x.fine_ref)
        assert np.array_equal(x.mean,e.raw[i])
        assert all(not np.any(v) for v in (x.opening,x.x,x.C,x.integral))
        assert x.diagnostic=={}
    assert o.last_wave=={} and e.last_native=={} and e.last_events==[]
    anatomy={'cortices':[(x.A,x.shared,x.fine) for x in o.cortices],
        'gates':(a.gate_vectors,a.gate_bias),'regulator':(r.Bq,r.Bv,r.bias),'motor_feedback':m.feedback}
    return {'ordinary_blank_checks_passed':True,'no_authored_learned_state':True,
        'anatomy_sha256':codec.digest(anatomy),'native_index':0,'wave_index':0,'time':0.,
        'H_use_theta_reference_eligibility_zero':True,'sensory_references_match_birth_structure':True,
        'native_calls':0,'handoff_calls':0,'world_body_steps':0,'external_controller':None}

def main():
    gate=json.loads((HERE/'RELEASE_BENCHMARK_RESULT.json').read_bytes())
    if gate['status']!='PASS' or (HERE/'RELEASE_CHECK_EXCEPTION.json').exists():raise RuntimeError('Release gate not passed')
    if (PACKET/'ROSTER_DECLARATION.json').exists():raise FileExistsError('No preparation retry or replacement')
    PACKET.mkdir(exist_ok=True)
    for name in ('prehistory','initial_states','birth_manifests','shared'):(PACKET/name).mkdir(exist_ok=True)
    c=Config(**json.loads((D/'configuration.json').read_bytes()));assert c.master_seed==5284097
    runtime=identity();runtime_sha=hashlib.sha256(canonical(runtime)).hexdigest()
    write(PACKET/'shared'/f'{runtime_sha}.json',runtime)
    prospective=[{'life_id':f'FS-{i:03d}','stream_life':i,'master_seed':c.master_seed,
        'phase':float(Streams(c.master_seed,i).draw('world-phase',(1,))[0]*2*np.pi)} for i in range(1,13)]
    write(PACKET/'ROSTER_DECLARATION.json',{'status':'PREPARATION_ONLY_NOT_AUTHORIZED_TO_EXECUTE',
        'roster':prospective,'order':'ascending FS-001 through FS-012','selected_before_birth_or_outcome_inspection':True,
        'native_ceiling':60000,'seconds_ceiling':600,'continuations_prepared':False,
        'preparation_scope':'At most one ordinary 600-second body-absent field preparation per declared life; Engine initialization only, zero organism-time.',
        'preparation_aggregate_wall_guard_seconds':1200,
        'cache_inventory':{'known_compatible_lives_1_to_12':[],
            'existing_cache':'Desktop/Eridos/Loom-p-engineering-20260921-01a0c405/developmental_ecology/artifacts/prehistory-attempt-001',
            'existing_cache_life':0,'existing_cache_phase':3.558411277237072,
            'scope':'Known primary cache/preparation locations searched; historical protected test-temp directories not traversed; no old sealed human B1 archive accessed.'},
        'request_sha256':file_hash(Path(r'C:\Users\Jason\.codex\attachments\d28a1d79-11b8-4403-92b0-269696a4b937\Pasted text.txt')),
        'runtime_sha256':runtime_sha,'configuration_sha256':c.identity(),'P_code_sha256':code_identity()['sha256']})
    started=time.perf_counter();rows=[];common_anatomy=None
    try:
        for row in prospective:
            if time.perf_counter()-started>=1200:raise RuntimeError('Preparation aggregate wall guard; no further history')
            name=row['life_id'];life=row['stream_life'];cache=PACKET/'prehistory'/name
            print(json.dumps({'preparing':name,'organism_time':0,'body_absent':True}),flush=True)
            result=prepare(c,cache,life=life)
            fields,phase,rng,provenance=load(c,cache,life=life)
            assert phase==row['phase'] and result['life']==life and result['organism_created'] is False
            e=Engine(c,fields,phase,rng,provenance)
            e.validate_state();blank=verify_blank(e)
            if common_anatomy is None:common_anatomy=blank['anatomy_sha256']
            assert common_anatomy==blank['anatomy_sha256']
            snapshot=codec.write(PACKET/'initial_states'/(name+'.ld'),{
                'engine':e,'identity':runtime_sha,'index':0,'wave':0,'life_id':name},level=1)
            restored=codec.read(PACKET/'initial_states'/snapshot['file'],snapshot['sha256'])['engine']
            assert codec.encode(core.causal_state(e))==codec.encode(core.causal_state(restored))
            manifest={**row,'status':'PREPARED_UNEXECUTED','blank':blank,
                'initial_causal_sha256':codec.digest(core.causal_state(e)),'initial_engine_sha256':state_hash(e),
                'initial_snapshot':snapshot,'runtime_sha256':runtime_sha,'configuration_sha256':c.identity(),
                'birth_provenance':{'position':e.body.position.tolist(),'angle':e.body.angle,'phase':phase,
                    'rejected':[{'position':x['position'].tolist(),'minimum_gap':x['minimum_gap']} for x in e.birth_provenance['rejected']]},
                'initial_rng_counters':e.organism.rng.counters,
                'prehistory':{'path':'prehistory/'+name,'manifest_sha256':file_hash(cache/'manifest.json'),
                    'field_array_sha256':result['field_sha256'],'field_file_sha256':result['file_sha256'],
                    'steps':result['steps_completed'],'world_interval':[-600,0],'wall_seconds':result['wall_seconds'],
                    'body':'absent','source_stocks':'full_constant','initial_fields':'zero','new_preparation':True},
                'organism_time_advanced':0,'no_outcome_selection':True}
            write(PACKET/'birth_manifests'/(name+'.json'),manifest);rows.append(manifest)
            print(json.dumps({'prepared':name,'snapshot_sha256':snapshot['sha256'],
                'initial_causal_sha256':manifest['initial_causal_sha256'],'native_steps':0,
                'aggregate_preparation_wall_seconds':time.perf_counter()-started}),flush=True)
        assert len(rows)==12 and len({x['initial_causal_sha256'] for x in rows})==12
        if time.perf_counter()-started>=1200:raise RuntimeError('Preparation aggregate wall guard reached')
        write(PACKET/'BLANK_START_VERIFICATION.json',{'status':'PASS','lives':12,'rows':rows,
            'common_anatomy_sha256':common_anatomy,'ordinary_blank_initialization':True,'scientific_native_steps':0,
            'scientific_wave_handoffs':0,'scientific_lives_executed':0,'prehistory_world_steps':720000,
            'body_absent_prehistories':12,'wall_seconds':time.perf_counter()-started,'runtime_sha256':runtime_sha})
    except BaseException as error:
        write(HERE/'PREPARATION_HOLD.json',{'error':f'{type(error).__name__}: {error}',
            'completed_life_ids':[x['life_id'] for x in rows],'no_retry_or_substitution':True})
        raise

if __name__=='__main__':main()
