"""Narrow clock continuity review: delivered generic fixtures, never an A5 world."""
import copy,json,math,sys,tempfile
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
WORKSPACE=HERE.parents[2]
SOURCE=WORKSPACE/'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
sys.path[:0]=[str(SOURCE),str(SOURCE/'tests_apparatus')]
from test_apparatus import manufactured
from test_clock_scheduling import scalar_times,prescription,decision,ENDS
from loom_p.records import state_hash,pack,unpack,strict_bytes
from loom_p.chemistry import FieldSolver
from loom_commissioning import clock,controllers,pending,runner,validators,adapter
from loom_commissioning.contract import EXTERNAL,make_manifest

OUT=Path(tempfile.mkdtemp(prefix='fixtures-',dir=HERE))
RESULT={'source':str(SOURCE),'output':str(OUT),'scope':'Only delivered scalar/serialized cases and generic 0.3 s components; no A5 commands/world or authority.',
        'physical_components':[],'detached_pending':[],'clock_corruption':[]}
def rejects(fn):
    try:fn()
    except ValueError as e:return str(e)
    raise AssertionError('expected rejection')

def component(pause):
    root=OUT/('pause-'+str(pause));root.mkdir()
    initial=manufactured(time=269.9,index=26990)
    plan=[{'point':[6.,5.],'until':270.,'press_force':0.},
          {'point':[5.,6.],'until':270.2,'press_force':0.}]
    m=make_manifest(initial,'fixture-late-resume',EXTERNAL,'waypoint',.3,plan=plan)
    before_neural=state_hash(initial.organism);before_rng=state_hash(initial.organism.rng)
    physical=[];fields=[];current=['first'];real_step=adapter.step;real_field=FieldSolver.step
    def field(self,*args,**kwargs):
        fields.append({'segment':current[0],'endpoint':args[2],'endpoint_hex':args[2].hex(),'dt':args[4]})
        return real_field(self,*args,**kwargs)
    def step(e,*args,**kwargs):
        before=e.time;index=e.native_index;start=len(fields)
        result=real_step(e,*args,**kwargs)
        n,w,events,_=result
        assert e.native_index==index+1 and n['elapsed']==.01 and e.time==before+.01
        assert n['time']==e.time and w is None and len(fields)==start+1
        assert fields[-1]['endpoint']==e.time and fields[-1]['dt']==.01
        assert state_hash(e.organism)==before_neural and state_hash(e.organism.rng)==before_rng
        physical.append({'segment':current[0],'native_index':e.native_index,'time':e.time,
            'time_hex':e.time.hex(),'index_reference':clock.expected_time(m,e.native_index),
            'field_calls':1,'wave':False,'random_counters':dict(e.organism.rng.counters)})
        return result
    with patch.object(adapter,'step',step),patch.object(FieldSolver,'step',field):
        first=runner.Run(copy.deepcopy(initial),m,root/'first')
        first.begin_command();first.advance(min(pause,10))
        if pause>10:first.begin_command();first.advance(pause-10)
        pause_info={'time':first.engine.time,'time_hex':first.engine.time.hex(),
            'native_index':first.engine.native_index,'hold_remaining':first.session['hold_remaining'],
            'last_issued_stage':first.session['cursor'],'engine_hash_before_close':state_hash(first.engine)}
        first.close();paused_hash=state_hash(first.engine)
        loaded,s,loaded_m=runner.load_restart(root/'first/final.restart.json.gz')
        assert state_hash(loaded)==paused_hash and loaded.time.hex()==pause_info['time_hex']
        assert loaded.native_index==pause_info['native_index'] and s['hold_remaining']==pause_info['hold_remaining']
        assert s['cursor']==pause_info['last_issued_stage'] and loaded_m==m
        current[0]='resumed';resumed=runner.Run.resume(root/'first',root/'resumed')
        assert resumed.engine.time.hex()==pause_info['time_hex'] and state_hash(resumed.engine)==paused_hash
        assert resumed.session['hold_remaining']==pause_info['hold_remaining']
        while not resumed.closed:resumed.hold()
        current[0]='continuous';continuous=runner.Run(copy.deepcopy(initial),m,root/'continuous')
        while not continuous.closed:continuous.hold()
    assert state_hash(continuous.engine)==state_hash(resumed.engine)
    split=[r for r in physical if r['segment']!='continuous'];whole=[r for r in physical if r['segment']=='continuous']
    assert [r['native_index'] for r in split]==[r['native_index'] for r in whole]==list(range(26991,27021))
    assert [r['time_hex'] for r in split]==[r['time_hex'] for r in whole]
    recurrence=initial.time
    for row in whole:
        recurrence+=.01
        assert row['time'].hex()==recurrence.hex()
    assert any(r['time']!=r['index_reference'] for r in whole), 'must distinguish accumulated and index clocks'
    assert len(fields)==60 and sum(r['segment']!='continuous' for r in fields)==30
    assert continuous.engine.native_index==27020 and continuous.session['body_wave_samples']==2
    assert resumed.session['field_updates']==continuous.session['field_updates']==30
    actions=validators.read_stream(root/'continuous/controller.jsonl.gz')
    assert [(r['native_index'],r['stage']['index'],r['hold_native_steps']) for r in actions]==[(26990,0,10),(27000,1,10),(27010,1,10)]
    for name in ('first','resumed','continuous'):
        assert validators.read_stream(root/name/'wave.jsonl.gz')==[]
    verification={name:validators.verify_segment(root/name) for name in ('first','resumed','continuous')}
    assert verification['first']['native_records']==pause and verification['resumed']['native_records']==30-pause
    row={'pause_local_steps':pause,'pause':pause_info,'pause_hash_after_close':paused_hash,
        'physical_time_preserved_exactly_on_load_resume':True,'time_recurrence_matches':True,
        'final_time':continuous.engine.time,'final_time_hex':continuous.engine.time.hex(),
        'final_index_product':clock.expected_time(m,27020),'final_state_hash':state_hash(continuous.engine),
        'split_field_calls':30,'continuous_field_calls':30,'split_native_records':30,'wave_records':0,
        'body_wave_samples':2,'inactive_neural_and_rng_unchanged':True,'actions':actions,
        'physical_calls':physical,'field_calls':fields,'reconstruction':verification}
    RESULT['physical_components'].append(row)
    print('physical pause',pause,'PASS',flush=True)

times=scalar_times();m=prescription()
# Existing corruption cases, with a read-only call observer proving rejection
# happens before any stage/command selection in pending decision validation.
for index in (26950,27000):
    d=decision(m,index,times[index]);d['time']+=.01;d['inputs']['time']=d['time']
    saved=copy.deepcopy(d);calls=[]
    watched={controllers.waypoint_stage.__code__,controllers.waypoint_command.__code__}
    def profile(frame,event,arg):
        if event=='call' and frame.f_code in watched:calls.append(frame.f_code.co_name)
    sys.setprofile(profile)
    try:error=rejects(lambda:pending.validate_decision(m,d))
    finally:sys.setprofile(None)
    assert error=='physical/native clock mismatch' and not calls and d==saved
    RESULT['clock_corruption'].append({'index':index,'one_step_clock_error':error,'selector_calls':calls,'input_unchanged':True})
for index in (26950,27000,63000):
    saved=times[index];clock.validate_physical_time(m,index,saved)
    assert times[index]==saved
    error=rejects(lambda:clock.validate_physical_time(m,index,saved+.01))
    RESULT['clock_corruption'].append({'index':index,'legitimate':saved,'reference':clock.expected_time(m,index),
        'allowance':clock.clock_allowance(m,index),'legitimate_drift_accepted_without_rewrite':True,'one_step_clock_error':error})

# Exactly the delivered detached late-boundary fixtures. Store the physical
# clock/index alongside session through unchanged P pack/JSON/unpack primitives.
for index in (26999,27000,27001,29999,30000,44999,45000,47999,48000,62999,63000):
    issued=index//10*10
    if index%10==0:issued-=10
    d=decision(m,issued,times[issued]);progress=index-issued
    s={'decision':d,'held_command':d['command'],'hold_remaining':10-progress,'cursor':d['stage']['index']}
    payload={'session':s,'native_index':index,'time':times[index]}
    restored=unpack(json.loads(strict_bytes(pack(payload))))
    assert restored==payload and restored['time'].hex()==times[index].hex()
    e=SimpleNamespace(native_index=restored['native_index'],time=restored['time'],status='paused',c=SimpleNamespace(native_dt=.01,event_time_tol=1e-10))
    pending.validate_pending(m,restored['session'],e)
    stale=copy.deepcopy(restored['session']);stale['hold_remaining']+=1
    stale_error=rejects(lambda:pending.validate_pending(m,stale,e))
    cursor=copy.deepcopy(restored['session']);cursor['cursor']=(s['cursor']+1)%7
    cursor_error=rejects(lambda:pending.validate_pending(m,cursor,e))
    corrupt=copy.deepcopy(e);corrupt.time+=.01
    corruption_error=rejects(lambda:pending.validate_pending(m,restored['session'],corrupt))
    RESULT['detached_pending'].append({'native_index':index,'time':e.time,'time_hex':e.time.hex(),
        'issued_index':issued,'last_issued_stage':s['cursor'],'remaining':s['hold_remaining'],
        'next_stage_by_index':controllers.waypoint_stage(clock.decision_clock(m,index),7),
        'serialization_exact':True,'stale_remainder_error':stale_error,'cursor_error':cursor_error,
        'mismatch_error':corruption_error})

partial=times[62999]+.003
clock.validate_physical_time(m,63000,partial,terminal=True)
full_error=rejects(lambda:clock.validate_physical_time(m,63000,partial))
old_error=rejects(lambda:clock.validate_physical_time(m,63000,times[62998],terminal=True))
assert partial==times[62999]+.003 and partial!=times[63000]
RESULT['terminal_partial']={'index':63000,'time':partial,'time_hex':partial.hex(),
    'full_endpoint':times[63000],'terminal_accepted_without_projection':True,
    'same_nonterminal_error':full_error,'previous_full_interval_error':old_error}
for pause in (9,10,11):component(pause)
RESULT['all_expected_assertions_passed']=True
(OUT/'RESULT.json').write_text(json.dumps(RESULT,indent=2),encoding='utf-8')
print(json.dumps({'output':str(OUT),'physical_fixtures':3,'detached_pending':11,
    'all_expected_assertions_passed':True},indent=2))
