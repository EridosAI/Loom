"""Bounded manufactured clock tests; zero commissioning execution.

Run with the pinned Python -B. Output is beside this script. Existing saved
inputs and the exact old Git blob are read only. This is not a sweep.
"""
import copy
from decimal import Decimal, getcontext, ROUND_HALF_EVEN
import gzip
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import types
from unittest.mock import patch
import numpy as np

TARGET=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
OLD='05abf60401d08f38750bca589b1c040e10513d7b'
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(TARGET/'developmental_ecology'))
from loom_p.schema import Config,Streams
from loom_p.engine import Engine
from loom_p.neural import Organism
from loom_p.chemistry import FieldSolver
from loom_p.geometry import transduce
from loom_p.physics import Body
from loom_p.records import state_hash
from loom_commissioning import controllers as c, runner, adapter
from loom_commissioning.contract import make_manifest,EXTERNAL
from loom_commissioning.validators import verify_segment,read_stream

getcontext().prec=80
TOL=Decimal.from_float(Config().event_time_tol)
def d(value): return Decimal.from_float(float(value))
def due_oracle(now,deadline): return d(now)>=d(deadline)-TOL
def tick(value): return int((d(value)/Decimal('.01')).to_integral_value(rounding=ROUND_HALF_EVEN))
PLAN=[{'point':[6.,5.],'until':.1,'press_force':0.}, {'point':[5.,6.],'until':.2,'press_force':0.}]
RESULT={'scope':'fixed manufactured boundaries and at most 0.2-second components; no commissioning',
        'timing_oracle':'80-digit Decimal interval ownership [deadline - existing absolute tolerance, infinity); integer native ticks'}

def manufactured(now=0.,index=0):
    cfg=Config()
    e=Engine(cfg,np.zeros((2,cfg.grid_n,cfg.grid_n)),0.,Streams(cfg.master_seed),{'kind':'manufactured_zero_field'})
    e.body=Body(np.array([5.,5.]),.3,energy=.7,integrity=.8)
    e.time=now; e.native_index=index
    e.raw=transduce(cfg,e.body,e.fields,e.time,e.phase)
    e.organism=Organism(cfg,Streams(cfg.master_seed),e.raw,e.body.reserves)
    e.birth_provenance={'kind':'manufactured','position':[5.,5.],'angle':.3,'phase':0.}
    return e

def failure(fn):
    try: fn()
    except ValueError as exc: return str(exc)
    return None

# Independently load and execute exact 05ab code in a detached module namespace.
old_source=subprocess.run(['git','-c',f'safe.directory={TARGET.as_posix()}','-C',str(TARGET),
    'show',f'{OLD}:developmental_ecology/loom_commissioning/controllers.py'],check=True,capture_output=True).stdout
old=types.ModuleType('independent_old_controllers'); old.__package__='loom_commissioning'
exec(compile(old_source,'05ab-controllers.py','exec'),old.__dict__)
data=json.loads((TARGET/'developmental_ecology/tests_apparatus/fixtures/review-boundary-input.json').read_bytes())
assert data['time']==0.09999999999999999 and tick(data['time'])==10
old_command,old_cursor=old.waypoint_command(data,PLAN,0)
new_command,new_cursor=c.waypoint_command(data,PLAN,0)
old_stop,_=old.waypoint_command(data,PLAN[:1],0)
new_stop,_=c.waypoint_command(data,PLAN[:1],0)
assert old_cursor==0 and new_cursor==1 and old_stop.any() and not new_stop.any()
exact=copy.deepcopy(data); exact['time']=.1
old_exact,_=old.waypoint_command(exact,PLAN,0)
assert np.array_equal(new_command,old_exact)
with patch.object(c,'time_due',lambda now,deadline:now>=deadline):
    broken_command,broken_cursor=c.waypoint_command(data,PLAN,0)
    broken_stop,_=c.waypoint_command(data,PLAN[:1],0)
assert broken_cursor==0 and broken_stop.any()
assert c.waypoint_command(data,PLAN,0)[1]==1
RESULT['exact_old_new']={'old_blob_sha256':hashlib.sha256(old_source).hexdigest(),'saved_time':data['time'],
    'old_cursor':old_cursor,'new_cursor':new_cursor,'old_command':old_command.tolist(),
    'new_command':new_command.tolist(),'old_final':old_stop.tolist(),'new_final':new_stop.tolist(),
    'old_code_fails_independent_tick_expectation':True,'disabled_comparison_fails_same_expectation':True,
    'restored_comparison_passes':True}

# Fixed representable cases straddling the absolute tolerance, including its
# immediately adjacent machine numbers. These are an explicit boundary class.
threshold=.1-1e-10
cases=[('full_hold_before',0.),('one_native_before',.09),('two_tolerances_before',.1-2e-10),
 ('one_point_one_tolerances_before',.1-1.1e-10),('below_tolerance_edge',math.nextafter(threshold,-math.inf)),
 ('represented_tolerance_edge',threshold),('above_tolerance_edge',math.nextafter(threshold,math.inf)),
 ('half_tolerance_before',.1-5e-11),('immediately_below',math.nextafter(.1,-math.inf)),
 ('exact',.1),('immediately_above',math.nextafter(.1,math.inf)),
 ('half_tolerance_above',.1+5e-11),('two_tolerances_above',.1+2e-10)]
boundary=[]
for name,now in cases:
    probe=copy.deepcopy(data); probe['time']=now
    _,cursor=c.waypoint_command(probe,PLAN,0)
    stop,_=c.waypoint_command(probe,PLAN[:1],0)
    expected=due_oracle(now,.1)
    assert cursor==int(expected) and (not stop.any())==expected
    boundary.append({'name':name,'now':now,'deadline_minus_now_decimal':str(d(.1)-d(now)),
                     'oracle_due':expected,'cursor':cursor,'final_stopped':not bool(stop.any())})
RESULT['boundary_class']=boundary

# Real recorded initial-to-final manufactured hold for direct comparison.
start=manufactured(); manifest=make_manifest(start,'fixture-independent-corrected-clock',EXTERNAL,'waypoint',.2,plan=PLAN)
continuous=runner.Run(copy.deepcopy(start),manifest,HERE/'continuous')
fields=[]; original=FieldSolver.step
def count(self,*a,**kw): fields.append(a[4]); return original(self,*a,**kw)
with patch.object(FieldSolver,'step',count): continuous.hold(); continuous.hold()
assert fields==[.01]*20 and tick(continuous.engine.time)==20 and state_hash(start.organism)==state_hash(continuous.engine.organism)
assert [x['hold_native_steps'] for x in read_stream(HERE/'continuous/controller.jsonl.gz')]==[10,10]
assert continuous.session['cursor']==1
RESULT['continuous']={'final_time':continuous.engine.time,'final_tick':continuous.engine.native_index,
 'field_calls':len(fields),'neural_rng_unchanged':True,'verification':verify_segment(HERE/'continuous')}

resumes=[]
for index in (7,9,10):
    first=runner.Run(copy.deepcopy(start),manifest,HERE/f'pause-{index}')
    first.begin_command(); first.advance(index); held=first.session['held_command'].copy(); first.close()
    resumed=runner.Run.resume(HERE/f'pause-{index}',HERE/f'resume-{index}')
    assert resumed.session['hold_remaining']==10-index and resumed.session['held_command']==held
    snapshot_hash=state_hash(resumed.engine)
    resumed.display(); assert state_hash(resumed.engine)==snapshot_hash
    if index<10: resumed.hold()
    assert tick(resumed.engine.time)==10 and resumed.session['hold_remaining']==0
    resumed.begin_command()
    assert resumed.session['cursor']==1 and resumed.session['held_command']!=held and resumed.session['hold_remaining']==10
    resumed.advance(10)
    assert state_hash(resumed.engine)==state_hash(continuous.engine)
    resumes.append({'pause_index':index,'pause_time':first.engine.time,'remaining':10-index,
        'held_command_preserved':True,'next_stage_cursor':1,'next_stage_new_command':True,
        'state_equal_continuous':True,'first_verification':verify_segment(HERE/f'pause-{index}'),
        'resumed_verification':verify_segment(HERE/f'resume-{index}')})
RESULT['pause_resume']=resumes

# Preflight-only clock states. We reuse a complete manufactured session and
# deliberately set its engine clock; no world advance or replay claim is made
# for these synthetic continuation probes. Real Run guards/command path apply.
base_e,base_s,base_m=runner.load_restart(HERE/'pause-10/final.restart.json.gz')
preflight=[]
selected=[('clearly_before',0.),('crossing_less_than_hold',.09),('outside_tolerance',.1-2e-10),
          ('effectively_due',.1-5e-11),('exactly_due',.1),('above_due',.1+5e-11)]
for name,now in selected:
    e=copy.deepcopy(base_e); s=copy.deepcopy(base_s)
    e.time=now; e.native_index=tick(now); s['hold_remaining']=0; s['cursor']=0
    r=runner.Run(e,base_m,HERE/f'preflight-{name}',session=s)
    before=state_hash(e); before_session=state_hash(r.session); calls=[]
    # If hold rejects, any accidental adapter step is a consequential failure.
    with patch.object(adapter,'step',side_effect=AssertionError('preflight evolved world')):
        error=failure(r.begin_command)
    expected_cursor=int(due_oracle(now,.1))
    end=d(now)+Decimal('.1')
    expected_accept=end<=d(PLAN[expected_cursor]['until'])+TOL
    assert (error is None)==expected_accept and state_hash(e)==before
    if error:
        assert state_hash(r.session)==before_session and r.recorder.counts.get('controller',0)==0
        for _ in range(2): assert failure(r.hold)==error and state_hash(e)==before
        assert state_hash(r.session)==before_session
    else:
        assert r.session['cursor']==expected_cursor and r.session['hold_remaining']==10
    preflight.append({'case':name,'time':now,'oracle_accept':expected_accept,'error':error,
        'cursor':r.session['cursor'],'hold_remaining':r.session['hold_remaining'],
        'world_unchanged':True,'rejection_session_unchanged':bool(error),
        'command_records':r.recorder.counts.get('controller',0)})
    r.close()
RESULT['preflight_only_clock_states']=preflight

# Expired final stage cannot regain commands, including persisted restart at
# a represented clock within half the existing tolerance before .1.
final_plan=PLAN[:1]
e=manufactured(); fm=make_manifest(e,'fixture-independent-final-stage',EXTERNAL,'waypoint',.2,plan=final_plan)
first=runner.Run(e,fm,HERE/'final-stage-first'); first.hold(); first.close()
final_results=[]
for label,shift in [('nominal',0.),('half-tolerance-before',-5e-11)]:
    if shift:
        fe,fs,fm2=runner.load_restart(HERE/'final-stage-first/final.restart.json.gz')
        fe.time=.1+shift
        prior=runner.Run(fe,fm2,HERE/'final-stage-near-manufactured',session=fs)
        prior.close()
        directory=HERE/'final-stage-near-manufactured'
    else: directory=HERE/'final-stage-first'
    r=runner.Run.resume(directory,HERE/f'final-stage-resumed-{label}')
    before=state_hash(r.engine); before_session=state_hash(r.session); records=r.recorder.counts.get('controller',0)
    errors=[failure(r.hold) for _ in range(3)]
    assert all(x=='route complete; no command hold authorized' for x in errors)
    assert state_hash(r.engine)==before and state_hash(r.session)==before_session
    assert r.recorder.counts.get('controller',0)==records==0
    final_results.append({'label':label,'time':r.engine.time,'errors':errors,'remaining':r.session['hold_remaining'],
        'no_state_or_command_change':True,'native_index':r.engine.native_index})
    r.close()
RESULT['expired_final_retries_resume']=final_results

# Preserve established global-cutoff shortening only. Interior stage crossing
# rejects; an earlier global native-aligned ceiling can end a final short hold.
global_results=[]
for label,duration,plan in [('full',.1,PLAN[:1]),('short-global',.07,[{'point':[6.,5.],'until':.07,'press_force':0.}])]:
    e=manufactured(); m=make_manifest(e,'fixture-independent-global-'+label,EXTERNAL,'waypoint',duration,plan=plan)
    r=runner.Run(e,m,HERE/('global-'+label)); r.hold()
    assert abs(d(e.time)-Decimal(str(duration)))<Decimal('1e-15') and r.closed
    expected=int(Decimal(str(duration))/Decimal('.01'))
    assert e.native_index==expected and failure(r.hold) is not None
    global_results.append({'kind':label,'duration':duration,'final_time':e.time,'steps':e.native_index,
        'hold_steps':read_stream(HERE/('global-'+label)/'controller.jsonl.gz')[0]['hold_native_steps'],
        'verification':verify_segment(HERE/('global-'+label))})
RESULT['global_deadlines']=global_results

(HERE/'INDEPENDENT_CLOCK_RESULTS.json').write_text(json.dumps(RESULT,indent=2),encoding='utf-8')
print(json.dumps(RESULT,indent=2))
