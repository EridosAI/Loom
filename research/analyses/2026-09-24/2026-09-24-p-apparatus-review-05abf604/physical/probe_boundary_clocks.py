"""Only named manufactured clock/terminal components; no long trajectory."""
import copy
import json
from pathlib import Path
import sys
from unittest.mock import patch
import numpy as np

TARGET = Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
sys.path.insert(0, str(TARGET / 'developmental_ecology'))
from loom_p.schema import Config, Streams
from loom_p.engine import Engine
from loom_p.neural import Organism
from loom_p.physics import Body
from loom_p.geometry import transduce
from loom_p.chemistry import FieldSolver
from loom_p.records import state_hash
from loom_commissioning.contract import make_manifest, INTACT, EXTERNAL
from loom_commissioning.runner import Run
from loom_commissioning.validators import verify_segment, read_stream

OUT = Path(__file__).resolve().parent

def manufactured(time, index):
    c = Config()
    e = Engine(c, np.zeros((2, c.grid_n, c.grid_n)), 0., Streams(c.master_seed), {'kind': 'manufactured'})
    e.body = Body(np.array([5., 5.]), .3, energy=.7, integrity=.8)
    e.time, e.native_index = time, index
    e.raw = transduce(c, e.body, e.fields, e.time, e.phase)
    e.organism = Organism(c, Streams(c.master_seed), e.raw, e.body.reserves)
    e.birth_provenance = {'kind': 'manufactured', 'position': [5., 5.], 'angle': .3, 'phase': 0.}
    return e

result = {}
e = manufactured(31.99, 3199)
e.organism.wave_elapsed = .19
initial_rng = e.organism.rng.counters.copy()
m = make_manifest(e, 'fixture-independent-above-old-cap', INTACT, 'none', .01)
run = Run(e, m, OUT / 'above-old-cap')
counts = {'Engine.step': 0, 'Organism.native': 0, 'Organism.handoff': 0, 'FieldSolver.step': 0}
originals = Engine.step, Organism.native, Organism.handoff, FieldSolver.step
def engine_step(self, *a, **kw):
    counts['Engine.step'] += 1
    return originals[0](self, *a, **kw)
def native(self, *a, **kw):
    counts['Organism.native'] += 1
    return originals[1](self, *a, **kw)
def handoff(self, *a, **kw):
    counts['Organism.handoff'] += 1
    return originals[2](self, *a, **kw)
def field(self, *a, **kw):
    counts['FieldSolver.step'] += 1
    return originals[3](self, *a, **kw)
with patch.object(Engine, 'step', engine_step), patch.object(Organism, 'native', native), \
     patch.object(Organism, 'handoff', handoff), patch.object(FieldSolver, 'step', field):
    run.advance(1)
assert set(counts.values()) == {1} and e.native_index == 3200 and e.organism.wave_count == 1
result['above_old_cap'] = dict(start_time=31.99, end_time=e.time, manufactured_native_steps=1,
    calls=counts, wave_count=e.organism.wave_count,
    rng_counter_delta={k: v-initial_rng.get(k, 0) for k, v in e.organism.rng.counters.items()
                       if v != initial_rng.get(k, 0)}, verification=verify_segment(OUT / 'above-old-cap'))

e = manufactured(.49, 49)
e.organism.wave_elapsed = .09
noise = e.organism.rng.counters['life/motor-noise']
m = make_manifest(e, 'fixture-independent-noise-boundary', INTACT, 'none', .02)
run = Run(e, m, OUT / 'noise-boundary')
run.advance(2)
assert e.native_index == 51 and e.organism.rng.counters['life/motor-noise'] == noise + 1
result['noise_boundary'] = dict(start_time=.49, end_time=e.time, manufactured_native_steps=2,
    motor_noise_counter_delta=e.organism.rng.counters['life/motor-noise']-noise,
    verification=verify_segment(OUT / 'noise-boundary'))

e = manufactured(.19, 19)
e.body.energy = .000005
e.raw = transduce(e.c, e.body, e.fields, e.time, e.phase)
neural = state_hash(e.organism)
m = make_manifest(e, 'fixture-independent-partial-terminal', EXTERNAL, 'sensor_human', .1)
run = Run(e, m, OUT / 'partial-terminal')
run.hold([0., 0.])
assert e.status == 'terminal' and .19 < e.time < .2 and e.native_index == 20
assert state_hash(e.organism) == neural and run.session['body_wave_samples'] == 0
assert read_stream(OUT / 'partial-terminal/wave.jsonl.gz') == []
try:
    Run.resume(OUT / 'partial-terminal', OUT / 'TERMINAL-RESUME-MUST-NOT-EXIST')
except ValueError as exc:
    rejection = str(exc)
else:
    raise AssertionError('terminal resumed')
assert not (OUT / 'TERMINAL-RESUME-MUST-NOT-EXIST').exists()
result['partial_terminal'] = dict(start_time=.19, end_time=e.time, elapsed=e.time-.19,
    manufactured_native_steps=1, terminal_dimension=e.terminal_dimension,
    body_wave_samples=run.session['body_wave_samples'], wave_records=0,
    neural_rng_unchanged=True, resume_rejection=rejection,
    verification=verify_segment(OUT / 'partial-terminal'))

e = manufactured(1199.99, 119999)
m = make_manifest(e, 'fixture-independent-1200-endpoint', EXTERNAL, 'sensor_human', .01)
run = Run(e, m, OUT / '1200-clock-endpoint')
run.hold([0., 0.])
assert e.native_index == 120000 and abs(e.time-1200.) < 1e-10 and run.closed
assert (OUT / '1200-clock-endpoint/native-120000.restart.json.gz').exists()
result['1200_endpoint_only'] = dict(start_time=1199.99, end_time=e.time, manufactured_native_steps=1,
    periodic_snapshot_written=True, verification=verify_segment(OUT / '1200-clock-endpoint'))

(OUT / 'BOUNDARY_CLOCK_RESULTS.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
