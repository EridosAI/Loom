"""Authorized deterministic engineering reconstruction; never writes old records."""
from pathlib import Path
import copy,hashlib,json,sys,time
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
PREP=ROOT/'motor_commissioning_preparation_20260930_v0_1';EX=PREP/'execution'
D=ROOT/'worktrees/loom-contact-release-20260930/developmental_ecology'
sys.path[:0]=[str(D),str(PREP)]
from loom_motor_commissioning import codec,evidence
from loom_developmental import core
from loom_p.geometry import fixtures,gap_normal
from loom_p import physics

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(name,obj):
    def plain(v):
        if isinstance(v,np.ndarray):return v.tolist()
        if isinstance(v,np.generic):return v.item()
        if isinstance(v,dict):return {str(k):plain(x) for k,x in v.items()}
        if isinstance(v,(list,tuple)):return [plain(x) for x in v]
        return v
    (HERE/name).write_text(json.dumps(plain(obj),indent=2),encoding='utf8')

seal=json.loads((ROOT/'motor_commissioning_results_20260930_v0_1/EXECUTION_CUSTODY_SEAL.json').read_bytes())
hashes={x['path']:x['sha256'] for x in seal['files']}
for path,h in hashes.items():assert sha(EX/path)==h,path
def read(p):return codec.read(p,hashes[p.relative_to(EX).as_posix()])

summary=[];new_steps=0;began=time.perf_counter()
for process,limit in [('CURRENT',9000),('M1',9000),('M2',1025)]:
    case='MC-FS-001-'+process;folder=EX/'lives'/case
    e=read(next(folder.glob('*initial.ld')))['engine'];checkpoints=0
    pieces=[read(p) for p in sorted(folder.glob('chunk-*.ld'))]
    if process=='M2':
        tail=read(folder/'failure-tail-s000.ld')
        pieces.append(dict(native=tail['unclosed_native'],waves=tail['unclosed_waves'],events=tail['unclosed_events']))
    first=0;checks=0;waves=0;events_n=0;start=time.perf_counter()
    for block in pieces:
        actual_events=[];actual_waves=[]
        for row in block['native']:
            dt,w,events=core.step(e);new_steps+=1
            actual=evidence.native_row(e,dt)
            assert np.array_equal(actual,row),(case,e.native_index,'NATIVE_DIVERGENCE',np.flatnonzero(actual!=row).tolist())
            actual_events.extend(events)
            if w is not None:actual_waves.append(evidence.wave_row(e,w))
            if e.native_index==6000:
                cp=read(next(folder.glob('checkpoint-000006000-*.ld')))['engine']
                assert codec.encode(core.causal_state(e))==codec.encode(core.causal_state(cp)),(case,'CHECKPOINT_DIVERGENCE')
                e=codec.decode(codec.encode(e));checkpoints+=1
        assert codec.encode(actual_events)==codec.encode(block['events']),(case,e.native_index,'EVENT_DIVERGENCE')
        assert codec.encode(actual_waves)==codec.encode(block['waves']),(case,e.native_index,'WAVE_DIVERGENCE')
        if 'P_endpoint_sha256' in block:
            assert codec.digest(e.organism)==block['P_endpoint_sha256'],(case,e.native_index,'ORGANISM_DIVERGENCE')
            assert hashlib.sha256(e.fields.tobytes()).hexdigest()==block['field_endpoint_sha256']
            assert e.organism.rng.counters==block['rng_endpoint']
        checks+=1;waves+=len(actual_waves);events_n+=len(actual_events)
    assert e.native_index==limit
    endpoint=read(next(folder.glob('*final.ld')))['engine'] if process!='M2' else tail['engine']
    a=copy.deepcopy(core.causal_state(e));b=copy.deepcopy(core.causal_state(endpoint))
    if process=='M2':
        assert b['status']=='failure' and 'Free-path release prefix' in b['failure']
        b['status']=a['status'];b['failure']=a['failure']
    assert codec.encode(a)==codec.encode(b),(case,'FINAL_CAUSAL_DIVERGENCE')
    summary.append(dict(case=case,steps=limit,native_fields=76,all_native_rows_bit_identical=True,
        event_records=events_n,all_events_bit_identical=True,waves=waves,all_waves_bit_identical=True,
        chunk_organism_field_rng_digests_identical=True,checkpoint_roundtrips=checkpoints,
        final_causal_state_identical=True,failure_metadata_normalized_only=process=='M2',seconds=time.perf_counter()-start))
    print(case,limit,'PASS',flush=True)
    save('HISTORICAL_REGRESSION_PROGRESS.json',dict(cases=summary,engineering_committed_steps=new_steps))
    if process=='M2':
        # One corrected step twice: live reconstructed state vs saved pre-failure restart.
        first=copy.deepcopy(e);restart=codec.decode(codec.encode(tail['engine']))
        restart.status=e.status;restart.failure=e.failure
        dt,w,events=core.step(first)
        core.step(restart);new_steps+=2
        assert codec.encode(core.causal_state(first))==codec.encode(core.causal_state(restart))
        assert first.native_index==1026 and first.time==e.time+.01
        assert first.organism.rng.counters==restart.organism.rng.counters
        assert evidence.check_ledger(events,first.c.arithmetic_tol)<=first.c.arithmetic_tol
        assert min(gap_normal(first.body.position,first.c.body_radius,f)[0] for f in fixtures(first.c,first.time,first.phase))>=-first.c.overlap_tol
        codec.write(HERE/'ENGINEERING_STEP_1026_ONLY.ld',dict(purpose='engineering regression only; not a scientific continuation',engine=first))
        save('CORRECTED_STEP_1026.json',dict(before_body=vars(e.body),after_body=vars(first.body),
            events=events,engine_native_calls=1,field_advances=1,restart_bit_identical=True,
            post_step_gaps=[dict(id=f['id'],gap=gap_normal(first.body.position,first.c.body_radius,f)[0]) for f in fixtures(first.c,first.time,first.phase)],
            physics_sha256=sha(D/'loom_p/physics.py')))
for path,h in hashes.items():assert sha(EX/path)==h,path
save('HISTORICAL_REGRESSION.json',dict(status='PASS',cases=summary,engineering_committed_steps=new_steps,
    corrected_step_repetitions=2,new_screen_cases=0,old_execution_files_unchanged=len(hashes),
    seconds=time.perf_counter()-began,physics_sha256=sha(D/'loom_p/physics.py')))
