"""Read-only component audit. Writes only this review directory; no commissioning run."""
import copy
import json
import sys
from pathlib import Path
from unittest.mock import patch

TARGET = Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology')
sys.path.insert(0, str(TARGET))
import numpy as np
from scipy.special import expit
from loom_p.schema import Config, Streams
from loom_p.engine import Engine
from loom_p.physics import Body
from loom_p.geometry import transduce
from loom_p.neural import Organism, Cortex, Regulator, Association
from loom_p.records import state_hash
from loom_commissioning import adapter, diagnostics, controllers
from loom_commissioning.contract import INTACT, FIXED, SELECTION

RESULTS = {}

def fixture(index=0):
    c = Config()
    e = Engine(c, np.zeros((2, c.grid_n, c.grid_n)), 0., Streams(c.master_seed),
               {'kind': 'manufactured_zero_field_not_lawful_birth'})
    e.body = Body(np.array([5., 5.]), .3, energy=.7, integrity=.8)
    e.time = index * c.native_dt
    e.native_index = index
    e.raw = transduce(c, e.body, e.fields, e.time, e.phase)
    e.organism = Organism(c, Streams(c.master_seed), e.raw, e.body.reserves)
    e.birth_provenance = {'kind': 'manufactured', 'position': [5., 5.], 'angle': .3, 'phase': 0.}
    e.organism.wave_elapsed = (index % 20) * c.native_dt
    return e

def causal(o):
    o = copy.deepcopy(o)
    o.last_wave = {}
    for cortex in o.cortices:
        cortex.diagnostic = {}
    o.association.diagnostic = {}
    o.regulator.credit_diagnostic = {}
    o.regulator.output_diagnostic = {}
    return o

def frozen_sequence(o, raw, frozen):
    rows = []
    for i in range(40):
        # Explicit detached synthetic receptor history, never a world trajectory.
        inputs = [x + (i + 1) * .0005 * np.arange(1, len(x) + 1) for x in raw]
        _, discarded = adapter.fixed_native(o, inputs, .01, i == 25, frozen)
        adapter.validate_frozen(o, frozen)
        if i == 5:
            assert all(np.any(x.integral) for x in o.cortices) and np.any(o.motor.integral)
        if i % 20 == 19:
            wave = adapter.fixed_handoff(o, np.array([.69 - i * .0001, .79 - i * .0002]), frozen)
            rows.append(copy.deepcopy(wave))
    return rows, discarded

def check_poison():
    e = fixture(); initial = copy.deepcopy(e.organism); frozen = adapter.structure(initial)
    reference = copy.deepcopy(initial)
    waves, _ = frozen_sequence(reference, e.raw, frozen)
    originals = Cortex.step, Regulator.credit, Association.write
    def poison_cortex(self, *args, **kwargs):
        originals[0](self, *args, **kwargs)
        self.shared += .123; self.fine -= .09
        self.shared_ref += .03; self.fine_ref += .07
    def poison_bank(self, *args, **kwargs):
        originals[1](self, *args, **kwargs)
        self.theta += .2; self.reference -= .3
    def poison_map(self, *args, **kwargs):
        originals[2](self, *args, **kwargs)
        for key in self.H:
            self.H[key] += .01; self.use[key] += .1
    cases = [([patch.object(Cortex, 'step', poison_cortex)], 'sensory'),
             ([patch.object(Regulator, 'credit', poison_bank)], 'banks'),
             ([patch.object(Association, 'write', poison_map)], 'maps_use'),
             ([patch.object(Cortex, 'step', poison_cortex), patch.object(Regulator, 'credit', poison_bank),
               patch.object(Association, 'write', poison_map)], 'all')]
    from contextlib import ExitStack
    outcomes = {}
    for patches, label in cases:
        other = copy.deepcopy(initial)
        with ExitStack() as stack:
            for p in patches: stack.enter_context(p)
            poisoned_waves, discarded = frozen_sequence(other, e.raw, frozen)
        assert state_hash(causal(reference)) == state_hash(causal(other)), label
        assert reference.rng.counters == other.rng.counters
        adapter.validate_frozen(other, frozen)
        # Restored arrays are copies; neither live structure nor discarded diagnostics alias frozen data.
        for x, values in zip(other.cortices, frozen['sensory']):
            for k, v in values.items(): assert not np.shares_memory(getattr(x, k), v)
        for key in frozen['H']:
            assert not np.shares_memory(other.association.H[key], frozen['H'][key])
            assert not np.shares_memory(other.association.use[key], frozen['use'][key])
        assert not np.shares_memory(other.regulator.theta, frozen['theta'])
        assert not np.shares_memory(other.regulator.reference, frozen['reference'])
        assert poisoned_waves[-1]['applied_structural_increment'] == 0
        assert poisoned_waves[-1]['diagnostic_label'] == FIXED
        outcomes[label] = {'causal_state_identical': True, 'rng_identical': True,
                           'frozen_identical': True, 'frozen_alias_absent': True}

    # Consequential negative control: restoration after output leaves banks frozen but changes controls/state.
    late = copy.deepcopy(initial)
    real_output = Regulator.output
    def output_then_restore(self, *args, **kwargs):
        real_output(self, *args, **kwargs)
        self.theta = frozen['theta'].copy(); self.reference = frozen['reference'].copy()
    with patch.object(Regulator, 'credit', poison_bank), patch.object(adapter, 'restore_banks', lambda *a: None), \
         patch.object(Regulator, 'output', output_then_restore):
        frozen_sequence(late, e.raw, frozen)
    adapter.validate_frozen(late, frozen)
    assert state_hash(causal(reference)) != state_hash(causal(late))
    control_difference = float(np.max(abs(reference.regulator.controls - late.regulator.controls)))
    assert control_difference > .01
    # Ordinary transient evolution remains active despite the structural freeze.
    changes = {}
    for i, (a, b) in enumerate(zip(initial.cortices, reference.cortices)):
        for name in ('mean', 'x', 'C', 'opening'):
            changes[f'cortex_{i}.{name}'] = bool(np.any(getattr(a, name) != getattr(b, name)))
    for name in ('a', 'means', 'traces'):
        changes['association.' + name] = state_hash(getattr(initial.association, name)) != state_hash(getattr(reference.association, name))
    for name in ('body_mean', 'eligibility', 'phi', 'xi', 'controls'):
        changes['regulator.' + name] = bool(np.any(getattr(initial.regulator, name) != getattr(reference.regulator, name)))
    for name in ('phase', 'nu', 'drive', 'tendency', 'command'):
        changes['motor.' + name] = bool(np.any(getattr(initial.motor, name) != getattr(reference.motor, name)))
    assert all(changes.values()), changes
    assert reference.native_count == 40 and reference.wave_count == 2
    assert reference.association.write_count == 2
    assert all(not np.any(x.integral) for x in reference.cortices) and not np.any(reference.motor.integral)
    assert all(not np.any(x) for x in reference.association.H.values())
    assert not np.any(reference.regulator.theta)
    RESULTS['fixed_poison'] = {'cases': outcomes, 'late_restore_frozen_but_causal_RED': True,
        'late_restore_max_control_difference': control_difference, 'fast_state_changes': changes,
        'sensory_motor_integrals_accumulate_then_reset_at_handoff': True,
        'reference_rng': reference.rng.counters, 'reference_causal_hash': state_hash(causal(reference))}

def explicit_association(before, psi, support):
    c = before.c; a = before.organism.association
    gates = []
    for m, sl in enumerate(c.slices):
        others = np.concatenate((psi[:sl.start], psi[sl.stop:]))
        v = c.gate_epsilon + expit(a.gate_vectors[m] @ others + a.gate_bias[m])
        gates.append(v / v.sum())
    gates = np.array(gates); gain = np.ones_like(psi); offset = 0
    for m in range(4):
        unit = np.zeros(c.widths[m])
        for group in c.pools[m]:
            unit[group] = c.query_floor + (1 - c.query_floor) * support[offset]; offset += 1
        gain[c.slices[m]] = np.tile(unit, 4)
    def recall(activity):
        q = np.zeros_like(activity)
        for (m, n), maps in a.H.items():
            part = np.einsum('jmn,n->jm', maps, activity[c.slices[n]], optimize=False) * gates[m, :, None]
            q[c.slices[m]] += part.sum(axis=0)
        return q
    activity = a.a.copy(); leak = -np.expm1(-c.wave_dt / (c.sweeps * c.tau_a))
    for _ in range(c.sweeps): activity = (1-leak)*activity + leak*np.tanh(gain*psi + recall(activity))
    return recall(activity)

def explicit_regulator(after, wave, q, omit=None):
    c = after.c; r = after.organism.regulator; d = wave['regulation']
    terms = {'evoked': r.Bq @ q, 'body': r.Bv @ after.body.reserves, 'bias': r.bias.copy()}
    if omit in terms: terms[omit] = np.zeros_like(terms[omit])
    phi = np.r_[1., np.tanh(sum(terms.values()))]
    learned = np.einsum('dof,f->do', r.theta, phi, optimize=False)
    explore = d['exploration'].copy()
    for bank in (0, 1):
        if omit == f'learned_{bank}': learned[bank] = 0
        if omit == f'exploration_{bank}': explore[bank] = 0
    logits = d['need'][:, None] * (learned + explore); g = c.group_count
    controls = np.r_[expit(logits[:, :g].sum(axis=0)),
        c.current_max/2*np.tanh(logits[:, g:g+2]).sum(axis=0),
        expit(c.attenuation_bias + logits[:, g+2:g+4].sum(axis=0))]
    return {'features': phi, 'weighted_logits': logits, 'controls': controls}

def check_receivers():
    e = fixture(19); o = e.organism; deterministic = np.random.default_rng(71003)
    e.body.velocity = np.array([.1, .03]); e.body.omega = .1
    e.raw = transduce(e.c, e.body, e.fields, e.time, e.phase)
    for key in o.association.H: o.association.H[key][:] = deterministic.uniform(-.0004, .0004, o.association.H[key].shape)
    o.association.a[:] = deterministic.uniform(-.1, .1, len(o.association.a))
    o.association.q[:] = deterministic.uniform(-.01, .01, len(o.association.q))
    o.regulator.theta[:] = deterministic.uniform(-.005, .005, o.regulator.theta.shape)
    for cortex in o.cortices:
        cortex.mean += .01; cortex.x[:] = deterministic.uniform(-.03, .03, len(cortex.x))
        cortex.integral[:] = deterministic.uniform(-.002, .002, len(cortex.integral))
    before = copy.deepcopy(e); native, wave, _, _ = adapter.step(e, INTACT)
    before_hash = state_hash(before); after_hash = state_hash(e)
    row = diagnostics.passive(before, e, wave, INTACT, None)
    assert before_hash == state_hash(before) and after_hash == state_hash(e)
    q = explicit_association(before, wave['psi'], before.organism.regulator.h)
    assert np.array_equal(q, wave['association']['q']) and np.linalg.norm(q) > 0
    influence = row['D5_wave']; differences = {}
    for omit in [None, *influence['without']]:
        expected = explicit_regulator(e, wave, q, omit)
        observed = influence['baseline'] if omit is None else influence['without'][omit]
        for name in expected: assert np.array_equal(expected[name], observed[name]), (omit, name)
        if omit:
            differences[omit] = float(np.max(abs(expected['controls'] - influence['baseline']['controls'])))
            assert differences[omit] > 0, omit
    for m in range(4):
        psi = wave['psi'].copy(); psi[e.c.slices[m]] = 0
        expected = explicit_association(before, psi, before.organism.regulator.h)
        observed = influence['query_support_dependencies'][f'sensory_context_{m}']
        assert np.array_equal(expected, observed['q']) and np.linalg.norm(expected - q) > 0
        assert np.array_equal(explicit_regulator(e, wave, expected)['controls'], observed['receiver']['controls'])
    expected = explicit_association(before, wave['psi'], np.zeros_like(before.organism.regulator.h))
    observed = influence['query_support_dependencies']['support_to_zero_with_query_floor']
    assert np.array_equal(expected, observed['q']) and np.linalg.norm(expected - q) > 0

    m = before.organism.motor; c = e.c; r = before.organism.regulator
    motor_terms = {'oscillator': c.motor_amplitude*np.sin(m.phase), 'noise': c.motor_noise_amplitude*m.nu,
        'direct_feedback': m.feedback @ np.r_[before.raw[3], before.raw[2]],
        'motor_evocation': before.organism.association.q[c.slices[6]][2:4], 'regulatory_current': r.current}
    total = sum(motor_terms.values()); motor = row['D5_native']; motor_differences = {}
    for omit in [None, *motor['without']]:
        drive = total if omit is None or omit == 'attenuation' else total - motor_terms[omit]
        target = np.tanh(drive); tendency = m.tendency + (-np.expm1(-.01/c.tau_motor))*(target-m.tendency)
        command = tendency if omit == 'attenuation' else (1-r.attenuation)*tendency
        observed = motor['baseline'] if omit is None else motor['without'][omit]
        for key, value in [('target', target), ('tendency', tendency), ('command', command)]:
            assert np.array_equal(value, observed[key]), ('motor', omit, key)
        if omit:
            motor_differences[omit] = float(np.max(abs(command - motor['baseline']['command'])))
            assert motor_differences[omit] > 0, ('motor', omit)
    assert np.array_equal(motor['baseline']['command'], e.body.command)
    # First-stage reconstruction really rejects a corrupted baseline, not only returns a probe.
    corrupt = copy.deepcopy(wave); corrupt['association']['q'][0] += 1e-3
    try: diagnostics.wave_receiver(before, e, corrupt)
    except ValueError as error: assert str(error) == 'associative receiver reconstruction mismatch'
    else: raise AssertionError('bad association baseline accepted')
    corrupt = copy.deepcopy(wave); corrupt['regulation']['controls'][0] += 1e-3
    try: diagnostics.wave_receiver(before, e, corrupt)
    except ValueError as error: assert str(error) == 'regulator receiver reconstruction mismatch'
    else: raise AssertionError('bad regulation baseline accepted')
    # Native/wave timing: formation uses the step-start raw and old mean/weights/activity.
    assert row['input_time'] == before.time and row['endpoint_time'] == e.time
    for i, (old, new, record) in enumerate(zip(before.organism.cortices, e.organism.cortices, row['cortices'])):
        assert np.array_equal(row['raw_step_start'][i], before.raw[i])
        assert np.array_equal(row['raw_endpoint'][i], e.raw[i])
        assert np.array_equal(record['residual_used'], before.raw[i]-old.mean)
        assert np.array_equal(native['sensory'][i]['raw'], before.raw[i])
        assert np.array_equal(record['shared_applied_delta'], new.shared-old.shared)
        assert np.array_equal(record['fine_applied_delta'], new.fine-old.fine)
        offdiag = old.C.copy(); np.fill_diagonal(offdiag, 0)
        formation = old.x[:,None]*(before.raw[i]-old.mean)[None,:] - old.x[:,None]**2*old.weights - c.competition*(offdiag@old.weights)
        assert np.array_equal(formation, native['sensory'][i]['formation'])
        packet = np.r_[(old.integral + .01*(old.x+new.x)/2)/.2, new.x]
        assert np.array_equal(packet, wave['packets'][i])
    assert not np.array_equal(np.concatenate(before.raw), np.concatenate(e.raw))
    RESULTS['receivers_alignment'] = {'nonzero_q_norm': float(np.linalg.norm(q)),
        'omission_control_max_differences': differences, 'all_explicit_equations_match': True,
        'motor_omission_command_max_differences': motor_differences,
        'dependency_probes_nonzero_and_correct': True, 'baseline_corruption_rejected': True,
        'native_step_start_endpoint_distinct_and_aligned': True, 'observer_state_rng_unchanged': True}
    return before, e, wave

def check_selection_and_leakage(before, after, wave):
    # Synthetic observer-only index stamps isolate selection from signal size/outcomes.
    selected = {}
    for index in (1, 99, 100, 101, 200):
        other = copy.deepcopy(after); other.native_index = index
        row = diagnostics.passive(before, other, None, INTACT, None)
        selected[str(index)] = 'D5_native' in row
        assert selected[str(index)] == (index % 100 == 0)
    changed_wave = diagnostics.passive(before, after, wave, INTACT, None)
    assert 'D5_wave' in changed_wave and 'D5_native' in changed_wave
    engine = fixture(); digest = state_hash(engine)
    controller_view = controllers.privileged_input(engine)
    def overwrite(value):
        if isinstance(value, list):
            for i, v in enumerate(value):
                if isinstance(v, (dict, list)): overwrite(v)
                elif isinstance(v, (int, float)): value[i] = 991337
        elif isinstance(value, dict):
            for key, v in list(value.items()):
                if isinstance(v, (dict, list)): overwrite(v)
                elif isinstance(v, (int, float)): value[key] = 991337
    overwrite(controller_view)
    assert state_hash(engine) == digest
    history = controllers.SensorHistory(engine); sensor = history.display(); overwrite(sensor)
    assert state_hash(engine) == digest and history.display() != sensor
    # Privileged records and evaluator labels differ, while allowed neural inputs are held exact.
    plain = fixture(); poisoned = copy.deepcopy(plain)
    poisoned.birth_provenance = {'AV': 'unsafe', 'SO': 'success', 'private': 'PRIVILEGED_SENTINEL'}
    poisoned.last_events = [{'private': 'PRIVILEGED_SENTINEL', 'stock': 991337, 'material': 'secret'}]
    assert controllers.SensorHistory(plain).display() == controllers.SensorHistory(poisoned).display()
    adapter.step(plain, INTACT, command=np.array([1., -1.]))
    adapter.step(poisoned, INTACT, command=np.array([-1., 1.]))
    assert state_hash(plain.organism) == state_hash(poisoned.organism)
    assert state_hash(plain.body) == state_hash(poisoned.body)
    assert np.array_equal(plain.fields, poisoned.fields)
    assert controllers.SensorHistory(plain).display() == controllers.SensorHistory(poisoned).display()
    assert 'PRIVILEGED_SENTINEL' not in json.dumps(controllers.SensorHistory(poisoned).display())
    RESULTS['selection_leakage'] = {'contract': SELECTION, 'selected_indices': selected,
        'every_handoff_observed': True, 'deep_controller_copy_mutation_has_no_world_effect': True,
        'sensor_display_is_a_copy': True, 'privileged_metadata_absent_from_sensor': True,
        'intact_ignores_external_command_and_privileged_metadata': True}

if __name__ == '__main__':
    check_poison()
    before, after, wave = check_receivers()
    check_selection_and_leakage(before, after, wave)
    RESULTS['scope'] = 'Manufactured components only; two one-native intact fixtures and one manufactured handoff; detached frozen-input neural arithmetic. No commissioning rows or freely acting lives.'
    output = Path(__file__).with_name('independent_checks.json')
    output.write_text(json.dumps(RESULTS, indent=2), encoding='utf-8')
    print(json.dumps(RESULTS, indent=2))
