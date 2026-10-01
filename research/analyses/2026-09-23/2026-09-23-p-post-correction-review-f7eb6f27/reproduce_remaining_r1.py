"""Read-only deterministic component reproduction; expected to fail at f7eb6f27.
Run from developmental_ecology with that directory in PYTHONPATH.
Does not construct or advance Engine, write target files, or tune Config.
"""
import json
import numpy as np
from loom_p.schema import Config
from loom_p.physics import Body, actuator_forces, free_velocity, release_probe, advance
from loom_p.geometry import fixtures, gap_normal

c = Config()
b = Body(np.array([2., 3.]), float(np.arccos(.01/.76)), velocity=np.array([-1e-5, 0.]))
force = actuator_forces(c, b, np.ones(2))
index = next(i for i, f in enumerate(fixtures(c, 0., 0.)) if f.get('source') == 0)
def gap_at(t):
    velocity, _ = free_velocity(c, b, force, t)
    return float(gap_normal(b.position+t*velocity, c.body_radius, fixtures(c,t,0.)[index])[0])
def descending_root(target):
    lo, hi = .0005, .002
    assert gap_at(lo) > target > gap_at(hi)
    for _ in range(70):
        mid = (lo+hi)/2
        if gap_at(mid) > target: lo = mid
        else: hi = mid
    return (lo+hi)/2

clearance = gap_at(.0005)
assert clearance > 20*c.geometry_tol, 'Fixture must have resolvable separation'
observed = dict(checkpoint='f7eb6f27c661e3db193a4225b56a825d7e41739d',
    angle=b.angle, initial_velocity=b.velocity.tolist(), force=force.tolist(),
    geometry_tol=c.geometry_tol, gap_at_half_millisecond=clearance,
    return_to_geometry_tol=descending_root(c.geometry_tol), zero_gap_return=descending_root(0.),
    release_probe=release_probe(c,b,force,0.,0.,.01,index))
events, elapsed, terminal = advance(c,b,np.full(8,.2),0.,0.,np.ones(2),.01)
observed.update(event_count=len(events), elapsed=elapsed, terminal=terminal,
    free_duration=sum(r['duration'] for r in events if not r['contacts']),
    contact_duration=sum(r['duration'] for r in events if r['contacts']),
    transfer=sum(float(r['transfer'].sum()) for r in events),
    release_events=sum(r.get('event_kind')=='release' for r in events),
    recontact_events=sum(r.get('event_kind')=='recontact_or_first_touch' for r in events),
    final_position=b.position.tolist(), final_reserves=b.reserves.tolist())
print(json.dumps(observed, indent=2), flush=True)
assert observed['free_duration'] > .0009, 'R1 remains: resolvable release/return was charged as full-duration contact'
