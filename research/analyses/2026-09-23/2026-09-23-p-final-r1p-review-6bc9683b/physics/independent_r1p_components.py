"""Four predeclared one-step physical components, independent analytic oracle.
No organism constructed; no source/runtime mutation; output only beside script.
Run with reviewed Python -B from developmental_ecology.
"""
import copy
import json
import math
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd()))
import numpy as np
import loom_p.physics as p
from loom_p.schema import Config
from loom_p.records import view

CASES = [
    ('review-exact', .01, 1e-5, 1.),
    ('different-normal-force', .02, 1e-5, 1.),
    ('reflected-longer-flight', .01, 2e-5, -1.),
    ('radial-original', .76, .001, 1.),
]
source_lines = Path(p.__file__).read_text().splitlines()
loop_lines = {i+1 for i, line in enumerate(source_lines) if line.strip() == 'for _ in range(500):'}
evidence = []

for label, normal_force, outward_speed, side in CASES:
    c = Config()
    angle = side*math.acos(normal_force/.76)
    body = p.Body(np.array([2., 3.]), angle, velocity=np.array([-outward_speed, 0.]))
    stocks = np.full(8, .2)
    initial = copy.deepcopy(body)

    def oracle(t):
        # Fixed E=.7, I=1, equal commands=>total force .76; fixed m=drag=1.
        # Independent selected displacement p0+t*v(t), NOT continuous integral.
        fx, fy = .76*math.cos(angle), .76*math.sin(angle)
        decay = math.exp(-t)
        one_minus_decay = -math.expm1(-t)
        vx = -outward_speed*decay + fx*one_minus_decay
        vy = fy*one_minus_decay
        x, y = -1.+t*vx, t*vy  # centre displacement from source [3,3]
        # Rationalized squared-distance expression avoids subtracting near1.
        distance = math.hypot(x, y)
        gap = ((-2*t*vx)+(t*vx)**2+(t*vy)**2)/(distance+1.)
        ax, ay = fx-vx, fy-vy
        px, py = vx+t*ax, vy+t*ay
        pxx, pyy = (2.-t)*ax, (2.-t)*ay
        rate = (x*px+y*py)/distance
        second = (x*pxx+y*pyy+px*px+py*py-rate*rate)/distance
        return gap, rate, second

    characteristic = outward_speed/normal_force
    peak_time = characteristic/2.
    peak_gap = oracle(peak_time)[0]
    assert peak_gap > 10*c.geometry_tol

    def root(threshold):
        lo, hi = peak_time, 2*characteristic
        assert oracle(lo)[0] > threshold and oracle(hi)[0] < threshold
        for _ in range(70):
            mid = (lo+hi)/2
            if oracle(mid)[0] > threshold: lo = mid
            else: hi = mid
        return hi

    threshold_return, zero_return = root(c.geometry_tol), root(0.)
    frames, searches = {}, []
    def trace(frame, event, arg):
        if frame.f_code.co_filename != p.__file__: return trace
        if event == 'call' and frame.f_code.co_name in ('search', 'first_collision'):
            frames[id(frame)] = dict(function=frame.f_code.co_name, loop_passes=0)
        if event == 'line' and frame.f_lineno in loop_lines and id(frame) in frames:
            frames[id(frame)]['loop_passes'] += 1
        if event == 'return' and id(frame) in frames:
            searches.append(frames.pop(id(frame)))
        return trace
    try:
        sys.settrace(trace)
        events, elapsed, terminal = p.advance(c, body, stocks, 0., 0., np.ones(2), .01)
    finally:
        sys.settrace(None)
    release = [e for e in events if e.get('event_kind') == 'release']
    free = [e for e in events if e['duration'] > 0 and not e['contacts']]
    returned = [e for e in events if e.get('event_kind') == 'recontact_or_first_touch']
    sustained = [e for e in events if e['duration'] > 0 and e['contacts']]
    assert len(release) == len(free) == len(returned) == len(sustained) == 1
    assert release[0]['time'] == 0
    assert returned[0]['time'] == free[0]['time']
    assert threshold_return-5*c.event_time_tol <= free[0]['duration'] <= zero_return+5*c.event_time_tol
    assert abs(sustained[0]['duration'] + free[0]['duration'] - .01) < 1e-16
    assert abs(elapsed-.01) < 1e-16 and terminal is None
    assert all(search['loop_passes'] <= 500 for search in searches)
    residuals = []
    for e in events:
        damage = c.damage_per_impulse*sum(contact['impulse'] if e['impact'] else max(contact['impulse']-c.stress_threshold*e['duration'], 0) for contact in e['contacts'])
        residual = dict(
            source=float(np.max(np.abs(e['stock_after']-e['stock_before']-e['renewal_first']-e['renewal_second']+e['transfer']))),
            energy=float(e['energy_after']-e['energy_before']-e['transfer'].sum()+e['expenditure']),
            damage=float(e['damage']-damage),
            integrity=float(e['integrity_after']-e['integrity_before']-e['repair']+damage))
        assert all(abs(value) < 2e-16 for value in residual.values())
        if e['duration'] == 0 or not e['contacts']:
            assert e['transfer'].sum() == 0 and e['repair'] == 0
        if not e['contacts']: assert e['damage'] == 0
        if e['duration'] > 0:
            assert abs(e['expenditure']-.0025*e['duration']) < 1e-18
            quality = np.zeros(8)
            for contact in e['contacts']:
                force = contact['impulse']/e['duration']
                if 'source' in contact:
                    quality[contact['source']] = force/(force+.1)/(1+(contact['relative_speed']/.25)**2)
            requested = .04*((e['stock_before']+e['renewal_first'])/.2)*(1-e['energy_before'])*quality*e['duration']
            assert np.max(np.abs(e['requested']-requested)) < 1e-18
        residuals.append(residual)
    # Independently assess the supplied curvature enclosure on the unsplit
    # starting trajectory at just three predeclared diagnostic instants.
    speed, acceleration = p.motion_bounds(c, initial, np.array([.38, .38]), .01)
    from loom_p.geometry import fixtures
    bound, _ = p.gap_curvature_bound(c, 0., fixtures(c, 0., 0.)[4], .01, speed, acceleration)
    derivative_samples = [(t, oracle(t)[2]) for t in (0., peak_time, zero_return)]
    assert all(abs(second) <= bound for _, second in derivative_samples)
    evidence.append(dict(case=label, normal_force=normal_force, outward_speed=outward_speed,
        angle=angle, peak_sample_time=peak_time, peak_gap=peak_gap,
        independent_return_at_geometry_tol=threshold_return, independent_zero_return=zero_return,
        free_duration=free[0]['duration'], contact_duration=sustained[0]['duration'],
        loop_counts=searches, events=events, balance_residuals=residuals,
        final_body=vars(body), final_stocks=stocks,
        curvature_bound=bound, analytic_second_derivative_samples=derivative_samples))

output = Path(__file__).with_name('independent-r1p-evidence.json')
output.write_text(json.dumps(view(dict(commit='6bc9683b54e4fa80136fe8534d7713e2a250a95f',
    configuration_sha256=Config().identity(), oracle='independent exponential velocity; rationalized analytic source gap; bisection; independent event accounting',
    cases=evidence)), indent=2, allow_nan=False), encoding='utf-8')
print(json.dumps([dict(case=e['case'], free_duration=e['free_duration'], contact_duration=e['contact_duration'],
    tolerance_return=e['independent_return_at_geometry_tol'], zero_return=e['independent_zero_return'],
    peak_gap=e['peak_gap'], loops=e['loop_counts']) for e in evidence], indent=2))
print('All four component oracles and accounting checks passed. Evidence:', output)
