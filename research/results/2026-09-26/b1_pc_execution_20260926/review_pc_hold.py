"""Post-closure PC-HOLD accounting only; no apparatus or simulation imports."""
import datetime
import gzip
import hashlib
import json
import math
from pathlib import Path

S = Path(__file__).resolve().parent
R = S / 'runs/PC-HOLD'
AUTH = 'ac1c5615c2c99ebe2524e3648b81003d7eeb42f1b54493212afd8d3cb83d719f'

def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def rows(name):
    with gzip.open(R / name, 'rt', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]

def write_new(p, obj):
    with p.open('x', encoding='utf-8') as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, allow_nan=False)
        f.write('\n')

at = datetime.datetime.now(datetime.timezone.utc).isoformat()
m = read(R / 'manifest.json')
assert m['complete'] and m['stop_cause'] == 'operator_withdrawal'
assert m['contract']['case_id'] == 'PC-HOLD'
assert m['contract']['execution_authority']['approved_execution_sha256'] == AUTH
assert not (S / 'PC-HOLD.RESULT.json').exists()
for name, item in m['files'].items():
    p = R / name
    assert p.parent.resolve() == R.resolve()
    assert p.stat().st_size == item['bytes'] and sha(p) == item['sha256'], name

n = rows('native.jsonl.gz')
events = rows('events.jsonl.gz')
commands = rows('controller.jsonl.gz')
assert len(n) == m['session_counters']['advanced'] == 390
assert len(commands) == m['records']['controller'] == 39
assert [row['native_index'] for row in n] == list(range(1, len(n)+1))
assert all(math.isfinite(e['time']) and e['duration'] >= 0 for e in events)

# Parse JSON scalars only. Never restore an Engine, Run, class, or field cache.
with gzip.open(R / 'initial.restart.json.gz', 'rt', encoding='utf-8') as f:
    restart = json.load(f)
assert hashlib.sha256(json.dumps(restart['state'], separators=(',', ':'), ensure_ascii=False,
    allow_nan=False).encode()).hexdigest() == restart['sha256']
engine_attrs = dict(dict(restart['state']['$dict'])['engine']['attrs']['$dict'])
config = dict(engine_attrs['c']['attrs']['$dict'])
body = dict(engine_attrs['body']['attrs']['$dict'])
threshold = config['stress_threshold']
tol = config['event_time_tol']
assert threshold == 0.25

supports = []
gentle = []
impacts = []
for e in events:
    positive = [c for c in e['contacts'] if c['impulse'] > 0]
    if e['impact'] and positive:
        impacts.append(e)
    if e['duration'] <= 0:
        continue
    for c in e['contacts']:
        assert math.isclose(c['force'], c['impulse']/e['duration'], rel_tol=0,
                            abs_tol=config['arithmetic_tol'])
    damage = config['damage_per_impulse'] * sum(
        max(c['impulse']-threshold*e['duration'], 0) for c in e['contacts'])
    assert math.isclose(damage, e['damage'], rel_tol=0, abs_tol=config['arithmetic_tol'])
    if positive:
        supports.append(e)
        # Strictly below the original threshold; no new pass tolerance on force.
        if all(c['force'] < threshold for c in positive) and e['damage'] == 0:
            gentle.append(e)

def intervals(eligible):
    out = []
    for e in eligible:
        a, b = e['time']-e['duration'], e['time']
        force = [c['force'] for c in e['contacts'] if c['impulse'] > 0]
        if out and a <= out[-1]['end'] + tol:
            v = out[-1]
            v['end'] = max(v['end'], b)
            v['force_min'] = min(v['force_min'], min(force))
            v['force_max'] = max(v['force_max'], max(force))
            v['event_count'] += 1
            v['stress_damage'] += e['damage']
        else:
            out.append(dict(start=a, end=b, force_min=min(force), force_max=max(force),
                            event_count=1, stress_damage=e['damage']))
    for v in out:
        v['duration'] = v['end']-v['start']
    return out

gentle_intervals = intervals(gentle)
support_intervals = intervals(supports)
longest = max(gentle_intervals, key=lambda x:x['duration'], default=None)
demonstrated = longest is not None and longest['duration'] + tol >= 1.0
expense = sum(e['expenditure'] for e in events)
damage = sum(e['damage'] for e in events)
repair = sum(e['repair'] for e in events)
assert math.isclose(sum(e['duration'] for e in events), m['final_time'], abs_tol=tol)
assert math.isclose(body['integrity']-damage+repair, n[-1]['reserves'][1], abs_tol=1e-12)
write_new(S / 'PC-HOLD.OPERATOR_REFLECTION.json', dict(
    case='PC-HOLD', recorded_utc=at,
    user_statement_verbatim='Ok, its stopped now. I just had a poke around. Its hard to know what is happening because I can only see teh current step. But I can infer what is happening. I can see how this could build an internal world model.',
    classification='Operator feedback and hypothesis; not evidence of P learning or an internal model in P.',
    interface_experience='Operator reports difficulty following motion across steps, while making inferences from displayed signals.',
    earlier_interpretation_record='PC-HOLD.USER_CONTACT_OBSERVATION.json',
    assistant_motor_or_end_actions=0, B1_state_accessed=False))

result = dict(case='PC-HOLD', attempt=1, recorded_utc=at, authority_sha256=AUTH,
    apparatus='352f73fffa6d9781eae8aa38e708a9a05669588f',
    outcome='DEMONSTRATED' if demonstrated else 'NOT DEMONSTRATED — PREDECLARED 1.0 s TARGET NOT OBTAINED',
    physical_gentle_hold_target_met=demonstrated, target_seconds=1.0, stress_threshold=threshold,
    support_intervals=support_intervals, qualifying_gentle_intervals=gentle_intervals,
    longest_qualifying_gentle_interval=longest,
    first_positive_contact_event=min((e['time'] for e in events if any(c['impulse']>0 for c in e['contacts'])), default=None),
    first_native_contact_sample=next((x['time'] for x in n if any(z>0 for z in x['contact_rates'])), None),
    impact_event_times=[e['time'] for e in impacts],
    impact_damage=sum(e['damage'] for e in impacts),
    sustained_stress_damage=sum(e['damage'] for e in events if e['duration']>0),
    total_damage=damage, expenditure=expense, repair=repair,
    starting_EI=[body['energy'], body['integrity']], final_EI=n[-1]['reserves'],
    final_position=n[-1]['position'], final_orientation=n[-1]['angle'],
    actual_stop_cause=m['stop_cause'], actual_runtime_status=m['status'],
    simulated_seconds=m['final_time'], wall_seconds=m['wall_seconds'],
    native_steps=len(n), commands=len(commands), record_counts=m['records'],
    command_history=[dict(time=c['time'], pair=c['command']) for c in commands],
    operator_assessment='Jason detected contact, reduced both commands and identified a persistent lower signal. Later he explored other commands and ended the case. This conceptual observation is distinct from the physical duration target.',
    assistance='General sensor explanations, prior PC-CONTACT post-case replay, and public timing clarification at 1.1 s were supplied. No live privileged force feedback or assistant motor commands.',
    method='Read closed event records; positive impulse over positive duration denotes support. Every active contact force must be strictly below 0.25 and recorded sustained damage zero. Contiguous intervals joined only within existing event_time_tol. Initial impact damage retained separately.',
    event_time_tolerance=tol, force_and_stress_arithmetic_verified=True,
    all_recorded_artifact_hashes_and_lengths_verified=True, runtime_receipt_sha256=sha(R/'manifest.json'),
    additional_simulation_steps=0, controller_calls_during_review=0,
    production_code_changes=0, assistant_motor_commands=0, B1_state_accessed=False,
    interpretation='Disclosed human operator practice only. No P neural/learning test, biological failure, B1 performance inference or retry.')
write_new(S / 'PC-HOLD.RESULT.json', result)
write_new(S / 'PC-HOLD.CLOSURE.json', dict(case='PC-HOLD',recorded_utc=at,
    complete=m['complete'],stop_cause=m['stop_cause'],runtime_status=m['status'],
    final_time=m['final_time'],native_steps=len(n),commands=len(commands),
    runtime_receipt_sha256=sha(R/'manifest.json'),files_verified=m['files'],
    assistant_sent_end=False,additional_world_steps=0))

state_path=S/'SEQUENCE_STATE.json'
state=read(state_path)
state.update(status='ALL FOUR CONTROLS CLOSED; PC-HOLD REVIEWED; B1 NOT AUTHORIZED OR EXECUTED',
    next_case=None, simulation_steps=640, controller_commands=64, status_observed_utc=at)
state['cases'][3]['status']='CLOSED AT 3.9 s / '+result['outcome']
state_path.write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('outcome','longest_qualifying_gentle_interval',
    'qualifying_gentle_intervals','impact_event_times','impact_damage','sustained_stress_damage',
    'total_damage','expenditure','starting_EI','final_EI','simulated_seconds','commands')},indent=2))
