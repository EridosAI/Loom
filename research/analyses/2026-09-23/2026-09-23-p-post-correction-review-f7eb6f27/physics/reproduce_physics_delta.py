"""Read-only, deterministic component evidence. Does not construct an organism.

Run from the reviewed developmental_ecology directory with its Python -B.
Only this script's sibling JSON output is written.
"""
import copy
import json
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd()))
import numpy as np
import loom_p.physics as physics
from loom_p.geometry import fixtures, gap_normal
from loom_p.schema import Config
from loom_p.records import view


def execute(body):
    c = Config()
    stocks = np.full(8, .2)
    initial = copy.deepcopy(body)
    events, elapsed, terminal = physics.advance(c, body, stocks, 0., 0., np.ones(2), .01)
    balances = []
    for event in events:
        damage = c.damage_per_impulse * sum(
            item['impulse'] if event['impact'] else max(item['impulse'] - c.stress_threshold*event['duration'], 0.)
            for item in event['contacts'])
        balances.append(dict(
            energy=float(event['energy_after'] - event['energy_before'] - event['transfer'].sum() + event['expenditure']),
            stock=float(np.max(np.abs(event['stock_after'] - event['stock_before'] - event['renewal_first'] - event['renewal_second'] + event['transfer']))),
            damage=float(event['damage'] - damage),
            integrity=float(event['integrity_after'] - event['integrity_before'] - event['repair'] + damage)))
        assert max(abs(x) for x in balances[-1].values()) < 1e-15
        if event['duration'] == 0 or not event['contacts']:
            assert event['transfer'].sum() == 0 and event['repair'] == 0 and event['damage'] == 0
    assert abs(sum(event['duration'] for event in events) - .01) < 1e-16
    assert elapsed == .01 and terminal is None
    return dict(initial=vars(initial), final=vars(body), events=events, balances=balances,
                elapsed=elapsed, terminal=terminal,
                transfer=sum(float(event['transfer'].sum()) for event in events),
                damage=sum(event['damage'] for event in events))


c = Config()
original = execute(physics.Body(np.array([2., 3.]), 0., velocity=np.array([-.001, 0.])))
assert [event.get('event_kind', 'interval') for event in original['events']] == [
    'release', 'interval', 'recontact_or_first_touch', 'interval']
assert original['events'][1]['contacts'] == []
assert original['events'][2]['contacts'][0]['impulse'] == 0
assert abs(original['events'][1]['duration'] - .0013148287095122722) < 1e-16

# Targeted oblique release/recontact. A large tangential force makes the
# global acceleration bound conservative; it does not remove radial separation.
body = physics.Body(np.array([2., 3.]), math.acos(.01/.76), velocity=np.array([-1e-5, 0.]))
force = physics.actuator_forces(c, body, np.ones(2))
source = fixtures(c, 0., 0.)[4]
tm = math.log(1.001) / 2


def free_gap(t):
    # Independent closed form of the selected p(t)=p0+t*v(t) convention,
    # using the fixed initial force, orientation and drag. No new integrator.
    steady = force.sum() * np.array([math.cos(body.angle), math.sin(body.angle)]) / c.linear_drag
    velocity = steady + (body.velocity - steady) * math.exp(-c.linear_drag*t/c.body_mass)
    return float(gap_normal(body.position + t*velocity, c.body_radius, source)[0])


def return_root(threshold):
    lo, hi = tm, .01
    assert free_gap(lo) > threshold and free_gap(hi) < threshold
    for _ in range(60):
        mid = (lo+hi)/2
        if free_gap(mid) > threshold:
            lo = mid
        else:
            hi = mid
    return dict(low=lo, high=hi, gap=free_gap(hi), threshold=threshold)


guard = physics.release_probe(c, body, force, 0., 0., .01, 4)
samples = [(t, free_gap(t)) for t in [0., tm, .0009, .001, .01]]
assert free_gap(tm) > 20*c.geometry_tol
assert free_gap(.0009) > c.geometry_tol
assert guard is None
roots = [return_root(0.), return_root(c.geometry_tol)]
oblique = execute(copy.deepcopy(body))
assert len(oblique['events']) == 1 and oblique['events'][0]['duration'] == .01
assert oblique['events'][0]['contacts'] and oblique['transfer'] > 0

# A clear-point diagnostic, not a patched physical run: demonstrate what the
# existing swept search does if supplied the known clear half-return point.
try:
    search = dict(result=physics.first_collision(c, body, force, 0., 0., .01, set(), {4: tm}))
except ArithmeticError as error:
    search = dict(error=type(error).__name__ + ': ' + str(error))

# Exercise pending-at-exact-endpoint without relying on sub-tolerance behavior
# of the normal locator. Only the contact-time locator is an arithmetic stand-in.
old_locator = physics.first_collision
calls = []
def endpoint_locator(config, current_body, forces, t, phase, dt, excluded, released=None):
    calls.append(dict(t=t, dt=dt))
    return dt, 4
physics.first_collision = endpoint_locator
try:
    endpoint_body = physics.Body(np.array([2.-.01*math.exp(-.01), 3.]), 0., velocity=np.array([1., 0.]))
    endpoint_events, endpoint_elapsed, endpoint_terminal = physics.advance(
        c, endpoint_body, np.full(8, .2), 0., 0., np.zeros(2), .01)
finally:
    physics.first_collision = old_locator
assert len(calls) == 1 and len(endpoint_events) == 2
assert endpoint_events[0]['duration'] == .01 and endpoint_events[0]['contacts'] == []
assert endpoint_events[1]['duration'] == 0 and endpoint_events[1]['event_kind'] == 'recontact_or_first_touch'
assert endpoint_events[1]['time'] == .01 and endpoint_events[1]['contacts'][0]['impulse'] > 0
assert all(event['transfer'].sum() == 0 and event['repair'] == 0 for event in endpoint_events)

result = dict(
    reviewed_commit='f7eb6f27c661e3db193a4225b56a825d7e41739d',
    configuration_sha256=c.identity(),
    scope='detached one-step physics only; no organism/native or lifetime execution',
    original_counterexample=original,
    remaining_oblique_counterexample=dict(
        guard=guard, gap_samples=samples, roots=roots, actual=oblique,
        swept_search_with_known_clear_guard=search,
        conclusion='Resolvable separation/recontact is still accounted as full-duration sustained contact'),
    pending_endpoint_component=dict(locator='stand-in reporting exact endpoint source touch', calls=calls,
        elapsed=endpoint_elapsed, terminal=endpoint_terminal, events=endpoint_events))
output = Path(__file__).with_name('physics-delta-evidence.json')
output.write_text(json.dumps(view(result), indent=2, allow_nan=False), encoding='utf-8')
print(json.dumps(dict(
    original_event_kinds=[event.get('event_kind', 'interval') for event in original['events']],
    original_durations=[event['duration'] for event in original['events']],
    original_transfer=original['transfer'],
    oblique_gap_samples=samples,
    oblique_guard=guard,
    oblique_return_roots=roots,
    oblique_actual_durations=[event['duration'] for event in oblique['events']],
    oblique_transfer=oblique['transfer'],
    known_clear_swept_search=search,
    pending_exact_endpoint='verified',
    evidence=str(output)), indent=2))
