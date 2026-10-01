"""Independent manufactured apparatus probes; no commissioning advancement.

The authority text is an inert manufactured test input, not Jason's authority.
Only validation functions see it. No authorized commissioning Run is constructed.
"""
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
from loom_p.records import state_hash, strict_bytes
from loom_p.chemistry import FieldSolver
from loom_commissioning.contract import (make_manifest, validate_manifest, authorize_execution,
                                        digest, INTACT, EXTERNAL, FIXED)
from loom_commissioning.controllers import privileged_input, validate_privileged, waypoint_command
from loom_commissioning.initialization import from_verified_cache
from loom_commissioning.runner import Run, load_restart
from loom_commissioning.validators import verify_segment, read_stream
from loom_commissioning import adapter

OUT = Path(__file__).resolve().parent
RESULT = {'scope': 'manufactured <=0.2 second apparatus components and validation-only cache reuse; no commissioning execution'}

def manufactured(time=0., index=0):
    c = Config()
    e = Engine(c, np.zeros((2, c.grid_n, c.grid_n)), 0., Streams(c.master_seed),
               {'kind': 'manufactured_zero_field_not_lawful_birth'})
    e.body = Body(np.array([5., 5.]), .3, energy=.7, integrity=.8)
    e.time = time
    e.native_index = index
    e.raw = transduce(c, e.body, e.fields, e.time, e.phase)
    e.organism = Organism(c, Streams(c.master_seed), e.raw, e.body.reserves)
    e.birth_provenance = {'kind': 'manufactured', 'position': [5., 5.], 'angle': .3, 'phase': 0.}
    return e

def rejected(fn):
    try:
        fn()
    except Exception as exc:
        return {'rejected': True, 'type': type(exc).__name__, 'message': str(exc)}
    return {'rejected': False}

def accepted(m, e):
    validate_manifest(m, e)
    authorize_execution(m)
    return True

# Read existing lawful life-0 cache without preparing fields or stepping a world.
e, init = from_verified_cache(TARGET / 'developmental_ecology/artifacts/prehistory-attempt-001', 0)
initial_hash = state_hash(e)
long_m = make_manifest(e, 'A5', EXTERNAL, 'waypoint', 1200, purpose='commissioning', initialization=init)
validate_manifest(long_m, e)
long_rejection = rejected(lambda: Run(e, long_m, OUT / 'UNAUTHORIZED-1200-MUST-NOT-EXIST'))
assert long_rejection['rejected'] and not (OUT / 'UNAUTHORIZED-1200-MUST-NOT-EXIST').exists()
assert state_hash(e) == initial_hash and e.native_index == 0
RESULT['long_manifest_without_execution'] = dict(validated_duration=1200, rejection=long_rejection,
                                                output_exists=False, native_steps=0, state_unchanged=True)

# Bind a manufactured request to a single initial controller/arm. Reuse exactly
# its bytes and five-field authority object with changed valid manifests.
base = make_manifest(e, 'authority-validation-only', EXTERNAL, 'waypoint', .01,
                     purpose='commissioning', initialization=init)
request = {
    'notice': 'MANUFACTURED AUTHORITY VALIDATION FIXTURE ONLY. NOT JASON AUTHORIZATION. NO EXECUTION.',
    'approved_manifest_without_authority': copy.deepcopy(base),
    'approved_plan': [{'point': [6., 5.], 'until': .01, 'press_force': 0.}],
}
request_path = OUT / 'MANUFACTURED-AUTHORITY-NO-EXECUTION.json'
request_path.write_bytes(strict_bytes(request))
grant = dict(request_path=str(request_path), request_sha256=digest(request_path.read_bytes()),
             approved_case=base['case_id'], approved_initial_state=base['initial_state'], approved_duration=.01)
base['execution_authority'] = grant
assert accepted(base, e)
changes = []
for mode, controller in [(EXTERNAL, 'sensor_human'), (EXTERNAL, 'manual_privileged'),
                         (INTACT, 'none'), (FIXED, 'none')]:
    variant = copy.deepcopy(base)
    variant['mode'], variant['controller'] = mode, controller
    changes.append(dict(mode=mode, controller=controller, accepted=accepted(variant, e),
                        same_authority=variant['execution_authority'] == grant))
controls = {}
for field, value in [('case_id', 'wrong-case'), ('duration_seconds', .02), ('initial_state', '0'*64),
                     ('p_code', '0'*64), ('configuration', '0'*64), ('apparatus', {})]:
    variant = copy.deepcopy(base)
    variant[field] = value
    if field == 'duration_seconds': variant['hard_stop_time'] = e.time + value
    controls[field] = rejected(lambda variant=variant: accepted(variant, e))
    assert controls[field]['rejected']
wrong_hash = copy.deepcopy(base)
wrong_hash['execution_authority']['request_sha256'] = '0'*64
controls['authority_file_hash'] = rejected(lambda: accepted(wrong_hash, e))
assert controls['authority_file_hash']['rejected'] and state_hash(e) == initial_hash
RESULT['authority_binding'] = dict(baseline_accepted=True, unchanged_request_sha256=grant['request_sha256'],
                                   mode_controller_variants=changes, rejected_controls=controls,
                                   native_steps=0, commissioning_run_constructors=0)

# A fixed manufactured route and real ten-native-step hold, paused at seven.
initial = manufactured()
m = make_manifest(initial, 'fixture-independent-waypoint-resume', EXTERNAL, 'waypoint', .2)
plan = [{'point': [6., 5.], 'until': .1, 'press_force': 0.},
        {'point': [5., 6.], 'until': .2, 'press_force': 0.}]
o_hash = state_hash(initial.organism)
first = Run(copy.deepcopy(initial), m, OUT / 'hold-first', plan=plan)
first.begin_command()
held = first.session['held_command'].copy()
first.advance(7)
assert first.session['hold_remaining'] == 3
before_display = state_hash(first.engine)
for _ in range(3): first.display()
assert state_hash(first.engine) == before_display
first.close()
restored_e, restored_s, restored_m = load_restart(OUT / 'hold-first/final.restart.json.gz')
assert restored_s['hold_remaining'] == 3 and restored_s['held_command'] == held
assert restored_s['route'] == plan and restored_m['hard_stop_time'] == .2
assert state_hash(restored_e) == state_hash(first.engine)
resumed = Run.resume(OUT / 'hold-first', OUT / 'hold-resumed')
resumed.hold()
assert resumed.engine.native_index == 10 and resumed.session['hold_remaining'] == 0
resumed.hold()
continuous = Run(copy.deepcopy(initial), m, OUT / 'hold-continuous', plan=plan)
field_calls = []
actual_field_step = FieldSolver.step
def count_fields(self, *args, **kwargs):
    field_calls.append(args[4])
    return actual_field_step(self, *args, **kwargs)
with patch.object(FieldSolver, 'step', count_fields):
    continuous.hold()
    continuous.hold()
assert len(field_calls) == 20 and all(x == .01 for x in field_calls)
assert state_hash(continuous.engine) == state_hash(resumed.engine)
assert state_hash(continuous.engine.organism) == o_hash
assert continuous.engine.native_index == 20 and continuous.closed and resumed.closed
receipts = {name: verify_segment(OUT / name) for name in ('hold-first', 'hold-resumed', 'hold-continuous')}
cutoff_reject = rejected(lambda: Run.resume(OUT / 'hold-resumed', OUT / 'CUT-OFF-RESUME-MUST-NOT-EXIST'))
assert cutoff_reject['rejected'] and not (OUT / 'CUT-OFF-RESUME-MUST-NOT-EXIST').exists()
RESULT['hold_resume'] = dict(paused_index=7, remaining_at_pause=3, held_command=held,
    first_hold_end_index=10, final_index=20, final_time=resumed.engine.time,
    original_deadline=resumed.manifest['hard_stop_time'], continuous_state_equal=True,
    external_neural_rng_state_unchanged=True, field_calls=len(field_calls),
    display_state_unchanged=True, complete_segment_verification=receipts, cutoff_resume_rejection=cutoff_reject)

# The route is causally important yet absent from the manifest/authority binding.
route_results = []
route_m = make_manifest(initial, 'fixture-independent-route-binding', EXTERNAL, 'waypoint', .1)
for number, destination in enumerate(([6., 5.], [4., 5.])):
    run = Run(copy.deepcopy(initial), route_m, OUT / f'route-{number}',
              plan=[{'point': destination, 'until': .1, 'press_force': 0.}])
    run.begin_command()
    route_results.append({'manifest_sha256': digest(strict_bytes(run.manifest)),
                          'plan': copy.deepcopy(run.session['route']),
                          'command': run.session['held_command'].copy(), 'native_steps': run.engine.native_index})
    run.close()
assert route_results[0]['manifest_sha256'] == route_results[1]['manifest_sha256']
assert route_results[0]['command'] != route_results[1]['command']
RESULT['route_binding'] = route_results

# Detached copies cannot mutate actual world state, including nested geometry.
probe = manufactured()
world_hash = state_hash(probe)
values = privileged_input(probe)
baseline_command, _ = waypoint_command(values, plan, 0)
values['position'][0] = 999
values['velocity'][1] = -999
values['reserves'][0] = 999
values['commands'][0] = -999
values['stocks'][0] = 999
for fixture in values['geometry']:
    if 'centre' in fixture: fixture['centre'][0] = 999
    if 'rect' in fixture: fixture['rect'][0] = 999
assert state_hash(probe) == world_hash
forbidden = privileged_input(probe)
forbidden['neural_q'] = [0]
forbidden_reject = rejected(lambda: validate_privileged(forbidden))
assert forbidden_reject['rejected']
RESULT['privileged_controller_boundary'] = dict(deep_copy_mutations_leave_engine_unchanged=True,
    baseline_command=baseline_command.tolist(), bounded=True, forbidden_input_rejection=forbidden_reject)

# Manufacture an apparatus exception before any body step; complete=false must
# block resume. A forged/noncomplete receipt is not treated as a pause.
fail_e = manufactured()
fail_m = make_manifest(fail_e, 'fixture-independent-failure', INTACT, 'none', .01)
failed = Run(fail_e, fail_m, OUT / 'failure')
with patch.object(adapter, 'step', side_effect=ArithmeticError('independent manufactured apparatus failure')):
    failure_result = rejected(lambda: failed.advance(1))
failure_receipt = json.loads((OUT / 'failure/manifest.json').read_bytes())
failure_resume = rejected(lambda: Run.resume(OUT / 'failure', OUT / 'FAILURE-RESUME-MUST-NOT-EXIST'))
assert failure_receipt['status'] == 'apparatus_failure' and not failure_receipt['complete']
assert failure_resume['rejected'] and fail_e.native_index == 0
RESULT['failure_stop'] = dict(trigger=failure_result, complete=failure_receipt['complete'],
    status=failure_receipt['status'], resume_rejection=failure_resume, native_steps=0)

(OUT / 'RUNNER_AUTHORITY_RESULTS.json').write_text(json.dumps(RESULT, indent=2), encoding='utf-8')
print(json.dumps(RESULT, indent=2))
