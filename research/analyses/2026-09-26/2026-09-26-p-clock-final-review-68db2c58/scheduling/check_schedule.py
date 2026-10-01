"""Narrow clock review: scalar arithmetic and inert scheduling metadata only.

No Engine/Run, field, body, neuron, prehistory or waypoint-command computation.
The held A5 manifest is read unchanged; no authority object is generated.
"""
import ast
import bisect
import copy
from decimal import Decimal, localcontext
import hashlib
import json
import math
from pathlib import Path
import sys
import traceback

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MODE = sys.argv[1]
OLD = Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology')
NEW = ROOT / 'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
SOURCE = OLD if MODE.startswith('old') else NEW
HELD_DIR = ROOT / 'exports/2026-09-26-A5-launch-packet-HOLD-5f077481'
HELD_HASH = '88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6'
COUNTS = {'blocked_calls': [], 'waypoint_command_calls': 0, 'world_constructors': 0,
          'world_steps': 0, 'field_steps': 0, 'neural_steps': 0, 'random_draws': 0, 'Run_constructors': 0}

def fence(frame, event, arg):
    if event != 'call': return
    code = frame.f_code; name = code.co_name; path = code.co_filename.replace('\\', '/')
    if '/loom_p/' not in path and '/loom_commissioning/' not in path: return
    prohibited = {'step', 'advance', 'account', 'prepare', 'native', 'handoff', 'draw', 'coupled',
        '_coupled', 'begin_command', 'hold', 'resume', 'from_verified_cache', 'load_snapshot',
        'load_restart', 'transduce', 'free_velocity', 'actuator_forces', 'privileged_input', 'waypoint_command'}
    is_world_constructor = name == '__init__' and (path.endswith(('/engine.py', '/runner.py', '/neural.py', '/chemistry.py'))
        or type(frame.f_locals.get('self')).__name__ == 'Streams')
    if name in prohibited or is_world_constructor:
        COUNTS['blocked_calls'].append(path + ':' + name)
        raise AssertionError('Scalar review prohibits ' + COUNTS['blocked_calls'][-1])

sys.setprofile(fence)
sys.path.insert(0, str(SOURCE))
from loom_commissioning import authority, contract, controllers, pending
if MODE == 'new':
    from loom_commissioning import clock

def digest(raw): return hashlib.sha256(raw).hexdigest()
def read(path): return json.loads(Path(path).read_bytes())
def outcome(call):
    try: call(); return {'accepted': True}
    except ValueError as error:
        return {'accepted': False, 'message': str(error), 'frames': [
            {'file': Path(x.filename).name, 'line': x.lineno, 'function': x.name}
            for x in traceback.extract_tb(error.__traceback__)]}

m = read(HELD_DIR / 'A5_MANIFEST.json')
held_before = digest((HELD_DIR / 'AUTHORITY_OBJECT.canonical.json').read_bytes())
manifest_before = digest((HELD_DIR / 'A5_MANIFEST.json').read_bytes())
assert held_before == HELD_HASH and m['execution_authority'] is None
assert authority.execution_sha256(m) == HELD_HASH
assert Path(pending.__file__).resolve() == (SOURCE / 'loom_commissioning/pending.py').resolve()
times = [0.]
for _ in range(63000): times.append(times[-1] + .01)
time_bits_before = digest(json.dumps([t.hex() for t in times]).encode())
with localcontext() as ctx:
    ctx.prec = 80
    def ticks(value):
        offset = (Decimal(str(value)) - Decimal(str(m['initial_time']))) / Decimal('0.01')
        assert offset == offset.to_integral_value()
        return m['initial_index'] + int(offset)
    ENDS = tuple(ticks(stage['until']) for stage in m['execution']['procedure']['stages'])
    END = m['initial_index'] + int(Decimal(str(m['duration_seconds'])) / Decimal('0.01'))
assert ENDS == (9000,12000,27000,30000,45000,48000,63000) and END == 63000

RESULT = {'mode': MODE, 'source': str(SOURCE), 'python': sys.version,
    'held_A5_sha256': HELD_HASH, 'held_manifest_sha256': manifest_before,
    'scope': 'Native/scalar scheduling only. No A5 commands/world/trajectory or new authority.',
    'independent_oracle': '80-digit Decimal admission, Python integer range and bisect_right ownership; no production deadline predicate used to construct expected results.',
    'expected_stage_ends': list(ENDS), 'source_identity': {}}
for filename in ('clock.py','controllers.py','pending.py','runner.py','authority.py','validators.py','adapter.py'):
    path = SOURCE / 'loom_commissioning' / filename
    if path.exists(): RESULT['source_identity'][filename] = {'bytes':path.stat().st_size, 'sha256':digest(path.read_bytes())}

def write():
    assert held_before == digest((HELD_DIR / 'AUTHORITY_OBJECT.canonical.json').read_bytes())
    assert manifest_before == digest((HELD_DIR / 'A5_MANIFEST.json').read_bytes())
    assert time_bits_before == digest(json.dumps([t.hex() for t in times]).encode())
    assert not COUNTS['blocked_calls']
    RESULT['physical_scalar_timestamps_unchanged'] = True
    RESULT['held_files_unchanged'] = True
    RESULT['fence'] = COUNTS
    result = HERE / (MODE + '-results.json')
    with result.open('x', encoding='utf-8') as f: json.dump(RESULT, f, indent=2, allow_nan=False)
    print(json.dumps(RESULT, indent=2, allow_nan=False), flush=True)

def prefix(index):
    return {'time': times[index], 'native_index': index, 'actor': contract.EXTERNAL,
        'controller': m['controller'], 'inputs': {}, 'command': [0.,0.], 'hold_native_steps':10,
        'annotation':'INERT CLOCK PREFIX; INVALID INPUT SENTINEL; NOT A COMMAND',
        'execution_sha256': HELD_HASH, 'stage':None, 'case_deadline':m['hard_stop_time']}

def manual_decision(index):
    # Incomplete manufactured manual-input dictionary. Not launchable, no grant.
    toy = {'initial_time':0., 'initial_index':0, 'duration_seconds':630., 'hard_stop_time':630.,
           'mode':contract.EXTERNAL, 'controller':'manual_privileged',
           'execution':{'procedure':{'stages':[]}}}
    inputs = read(SOURCE / 'tests_apparatus/fixtures/review-boundary-input.json')
    inputs['time'] = times[index]
    d = {'time':times[index], 'native_index':index, 'actor':contract.EXTERNAL, 'controller':'manual_privileged',
         'inputs':inputs, 'command':[0.,0.], 'hold_native_steps':10, 'annotation':'INERT GENERIC MANUAL CLOCK FIXTURE',
         'execution_sha256':authority.execution_sha256(toy), 'stage':None, 'case_deadline':630.}
    return outcome(lambda: pending.validate_decision(toy, d))

def crossing_call():
    path = SOURCE / 'loom_commissioning/runner.py'
    tree = ast.parse(path.read_text(encoding='utf-8'))
    calls = [x for x in ast.walk(tree) if isinstance(x,ast.Call) and len(x.args)==2
             and isinstance(x.args[1],ast.Constant) and x.args[1].value=='command hold would cross prescribed stage boundary']
    assert len(calls)==1
    node = calls[0]
    RESULT['exact_crossing_expression'] = {'file':str(path), 'line':node.lineno, 'code':ast.unparse(node)}
    return compile(ast.Expression(node), str(path), 'eval')

if MODE == 'old-a':
    controls = [ {'native_index':i, 'physical_time':times[i], **outcome(lambda i=i:pending.validate_decision(m,prefix(i)))}
                 for i in (26940,26950,27000)]
    assert controls[0]['message'] == 'forbidden controller input'
    assert controls[1]['message'] == controls[2]['message'] == 'issued decision clock mismatch'
    RESULT['old_A'] = {'controls':controls, 'nominal_26950':269.5, 'delta':times[26950]-269.5,
                       'physical_hex':times[26950].hex(), 'complete_generic_manual_decision':manual_decision(26950)}
    assert RESULT['old_A']['complete_generic_manual_decision']['message']=='issued decision clock mismatch'
    write()
    assert controls[1]['accepted'], 'OLD A RED: legitimate accumulated clock rejected at native 26950'
elif MODE == 'old-b':
    # Execute the original source's stage-only loop and exact runner crossing call.
    # This deliberately bypasses blocker A without loosening/patching any guard.
    tree = ast.parse((SOURCE/'loom_commissioning/controllers.py').read_text(encoding='utf-8'))
    function = next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='waypoint_command')
    loop = next(x for x in function.body if isinstance(x,ast.While))
    env = {'cursor':0, 'data':{'time':times[27000]}, 'plan':m['execution']['procedure']['stages'], 'time_due':controllers.time_due}
    exec(compile(ast.Module(body=[loop],type_ignores=[]), str(SOURCE/'loom_commissioning/controllers.py'), 'exec'),env)
    stage = env['cursor']; until=m['execution']['procedure']['stages'][stage]['until']; end=times[27000]+.1
    expr = crossing_call()
    got = outcome(lambda:eval(expr, {'require':contract.require,'end':end,'until':until,'dispatch':{'time_due':controllers.time_due}}))
    assert stage==2 and got['message']=='command hold would cross prescribed stage boundary'
    RESULT['old_B'] = {'native_index':27000, 'physical_time':times[27000], 'nominal':270., 'selected_stage':stage,
        'expected_stage':bisect.bisect_right(ENDS,27000), 'until':until,'prospective_hold_end':end,
        'stage_loop_line':loop.lineno, 'result':got, 'earlier_clock_guard_invoked':False}
    write()
    assert stage==3 and got['accepted'], 'OLD B RED: accumulated clock retains stage2 and independently rejects the 270s transition'
elif MODE == 'new':
    assert clock.stage_ends(m)==ENDS and clock.case_end(m)==END
    p=outcome(lambda:pending.validate_decision(m,prefix(26950)))
    assert p['message']=='forbidden controller input'
    whole=manual_decision(26950); assert whole['accepted']
    RESULT['corrected_A']={'native_index':26950,'physical_time':times[26950],'clock_prefix_reaches_later_input_sentinel':p,
                          'complete_generic_manual_decision':whole,'allowance':clock.clock_allowance(m,26950)}
    expr=crossing_call()
    i=27000; stage=controllers.waypoint_stage(clock.decision_clock(m,i),len(ENDS))
    end=i+clock.hold_steps(m,i); until=clock.stage_ends(m)[stage]
    got=outcome(lambda:eval(expr,{'require':contract.require,'end':end,'until':until}))
    assert stage==3 and got['accepted']
    RESULT['corrected_B']={'native_index':i,'physical_time':times[i],'stage':stage,'hold_end':end,'stage_end':until,'result':got}
    def row(i):
        expected=min(bisect.bisect_right(ENDS,i),len(ENDS)-1)
        stage=controllers.waypoint_stage(clock.decision_clock(m,i),len(ENDS))
        assert stage==expected
        clock.validate_physical_time(m,i,times[i])
        hold=outcome(lambda:clock.hold_steps(m,i))
        should_issue=(i%10==0 and i<END)
        assert hold['accepted']==should_issue
        return {'native_index':i,'nominal_time':i/100,'physical_time':times[i],'physical_hex':times[i].hex(),
                'drift':times[i]-i*.01,'allowance':clock.clock_allowance(m,i),'stage':stage,
                'expected_stage':expected,'new_hold':10 if should_issue else 0,'hold_validation':hold,
                'route_complete':i==END}
    RESULT['representative_boundaries']=[row(i) for i in (26949,26950,26951,26999,27000,27001)]
    RESULT['all_A5_stage_boundaries']=[{'deadline_index':boundary,'rows':[row(i) for i in (boundary-1,boundary,boundary+1) if i<=END]} for boundary in ENDS]
    holds=[]; stage_counts=[0]*len(ENDS); max_drift=0.; max_ratio=0.; residual_local=0.
    for i,t in enumerate(times):
        clock.validate_physical_time(m,i,t)
        expected=min(bisect.bisect_right(ENDS,i),len(ENDS)-1)
        stage=controllers.waypoint_stage(clock.decision_clock(m,i),len(ENDS))
        assert stage==expected
        max_drift=max(max_drift,abs(t-i*.01));max_ratio=max(max_ratio,abs(t-i*.01)/clock.clock_allowance(m,i))
        if i<END and i%10==0:
            count=clock.hold_steps(m,i);assert count==10
            assert i+count<=ENDS[stage] and i+count<=END
            eval(expr,{'require':contract.require,'end':i+count,'until':ENDS[stage]})
            holds.append({'start_index':i,'end_index':i+count,'stage':stage,'physical_time':t})
            stage_counts[stage]+=1
            for progress in range(11):residual_local=max(residual_local,abs(times[i+progress]-(t+progress*.01)))
    assert [h['start_index'] for h in holds]==list(range(0,END,10))
    assert [h['end_index'] for h in holds]==list(range(10,END+1,10))
    assert stage_counts==[900,300,1500,300,1500,300,1500]
    assert not outcome(lambda:clock.hold_steps(m,END))['accepted']
    with (HERE/'STATIC_A5_HOLDS.json').open('x',encoding='utf-8') as f:json.dump(holds,f,separators=(',',':'))
    RESULT['static_schedule']={'checked_native_indices':len(times),'holds':len(holds),'steps':END,
        'per_stage_hold_counts':stage_counts,'all_holds_exact_and_contiguous':True,'stage_disagreements':0,
        'crossing_failures':0,'final_new_hold_rejected':True,'final_physical_time':times[-1],
        'max_abs_drift':max_drift,'max_drift_fraction_of_allowance':max_ratio,
        'max_local_ten_step_elapsed_residual':residual_local,'final_allowance':clock.clock_allowance(m,END),
        'native_mod20_opportunities':sum(i%20==0 for i in range(1,END+1)),
        'physical_cadence_claim':'No world cadence executed here; arithmetic index opportunities only.'}
    bad=[]
    for i in (26950,27000,63000):
        got=outcome(lambda i=i:clock.validate_physical_time(m,i,times[i]+.01))
        assert got['message']=='physical/native clock mismatch'
        bad.append({'native_index':i,'physical_time':times[i]+.01,'result':got,
                    'stage_still_index_owned':controllers.waypoint_stage(clock.decision_clock(m,i),len(ENDS))})
    RESULT['delivered_meaningful_clock_mismatches']=bad
    write();print('GREEN: both old clock failure sites closed; actual held A5 schedule representable without execution',flush=True)
else:raise ValueError(MODE)
