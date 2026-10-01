"""Narrow independent reproduction of the delivered pending-hold closure.

Both runtimes are read only; every generated manufactured record is here.
Old mode deliberately exits at the demonstrated stage-overrun assertion.
"""
import copy
import gzip
import hashlib
import json
import math
import shutil
import sys
from pathlib import Path
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[2]
MODE = sys.argv[1]
SUFFIX = sys.argv[2] if len(sys.argv) > 2 else ''
SOURCE = (WORKSPACE / 'exports/2026-09-25-p-apparatus-correction-review-9d31e790/portable/developmental_ecology'
          if MODE == 'old' else Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology'))
OUT = HERE / (MODE + '-components' + SUFFIX)
OUT.mkdir(exist_ok=False)
sys.path[:0] = [str(SOURCE), str(SOURCE / 'tests_apparatus')]
import numpy as np
from test_apparatus import manufactured
from loom_p.records import state_hash, pack, unpack, strict_bytes
from loom_p.chemistry import FieldSolver
from loom_commissioning import runner, authority, controllers, validators, adapter
from loom_commissioning.contract import EXTERNAL, make_manifest, digest

PLAN = [{'point': [6., 5.], 'until': .1, 'press_force': 0.},
        {'point': [5., 6.], 'until': .2, 'press_force': 0.}]
RESULT = {'mode': MODE, 'source': str(SOURCE), 'scope': 'Existing bounded manufactured apparatus fixtures only; no commissioning, prehistory, source mutation or new geometry cases.',
          'source_files': {}, 'checks': {}}
for name in ('runner.py', 'pending.py', 'validators.py', 'authority.py', 'controllers.py'):
    path = SOURCE / 'loom_commissioning' / name
    if path.exists():
        RESULT['source_files'][name] = {'bytes': path.stat().st_size, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
assert Path(runner.__file__).resolve() == (SOURCE / 'loom_commissioning/runner.py').resolve()

def save():
    raw = json.dumps(RESULT, indent=2)
    (HERE / (MODE + SUFFIX + '-results.json')).write_text(raw, encoding='utf-8')
    print(raw, flush=True)

def create(name, duration=.2, plan=None):
    e = manufactured()
    m = make_manifest(e, 'fixture-' + name, EXTERNAL, 'waypoint', duration, plan=copy.deepcopy(PLAN if plan is None else plan))
    return runner.Run(e, m, OUT / name)

def snapshot(e):
    return {'engine_hash': state_hash(e), 'body_hash': state_hash(e.body),
            'fields_hash': hashlib.sha256(e.fields.tobytes()).hexdigest(),
            'neural_rng_hash': state_hash(e.organism), 'native_index': e.native_index,
            'time': e.time, 'energy': e.body.energy, 'integrity': e.body.integrity}

def reject(call, expected=None):
    try:
        call()
    except ValueError as error:
        message = str(error)
        if expected is not None:
            assert expected in message, (expected, message)
        return message
    raise AssertionError('Required rejection did not occur')

def old_reproduction():
    # Exact ordinary close/resume counterexample from the previous HOLD probe.
    first = create('persist-first')
    first.begin_command()
    issued = copy.deepcopy(first.session['held_command'])
    first.advance(7)
    assert first.session['hold_remaining'] == 3
    first.session['held_command'] = [-.5, .5]
    first.session['hold_remaining'] = 4
    first.close()
    resumed = runner.Run.resume(OUT / 'persist-first', OUT / 'persist-resumed')
    resumed.hold()
    assert resumed.engine.body.command.tolist() == [-.5, .5]
    assert resumed.engine.native_index == 11
    resumed.close()
    verifications = [validators.verify_segment(OUT / name) for name in ('persist-first', 'persist-resumed')]
    RESULT['checks']['ordinary_save_resume'] = {
        'issued_pair': issued, 'substituted_pair': [-.5, .5], 'initial_native_index': 7,
        'original_remaining': 3, 'substituted_remaining': 4,
        'final': snapshot(resumed.engine), 'stage_deadline': .1,
        'full_verifications': verifications, 'hash_files_edited': False,
        'old_guards_disabled': False}
    # The other previously reported public load_restart -> session -> Run path.
    first2 = create('loaded-first')
    first2.begin_command(); first2.advance(7); first2.close()
    e, s, m = runner.load_restart(OUT / 'loaded-first/final.restart.json.gz')
    before = snapshot(e)
    s['held_command'] = [-.5, .5]; s['hold_remaining'] = 4
    authority.validate_session(m, s)
    resumed2 = runner.Run(e, m, OUT / 'loaded-resumed', session=s)
    resumed2.hold(); resumed2.close()
    assert e.native_index == 11 and e.body.command.tolist() == [-.5, .5]
    RESULT['checks']['loaded_session_constructor'] = {'before': before, 'after': snapshot(e),
        'accepted_mutated_pending': True, 'full_verification': validators.verify_segment(OUT / 'loaded-resumed')}
    save()
    assert resumed.engine.native_index <= 10, 'OLD PENDING HOLD BREACH: seven plus altered four executes step 11 after the stage deadline'

def new_mutations():
    from loom_commissioning import pending
    outcomes = {}
    for name in ('command', 'remainder', 'both', 'decision'):
        run = create('mutated-' + name); run.begin_command(); run.advance(7)
        saved = copy.deepcopy(run.session); before = snapshot(run.engine)
        if name in ('command', 'both'):
            run.session['held_command'] = [-.5, .5]
        if name in ('remainder', 'both'):
            run.session['hold_remaining'] = 4
        if name == 'decision':
            run.session['decision']['inputs']['position'] = [7., 5.]
            pair, _ = controllers.waypoint_command(run.session['decision']['inputs'], copy.deepcopy(PLAN), 0)
            run.session['decision']['command'] = pair.tolist(); run.session['held_command'] = pair.tolist()
        with patch.object(adapter, 'step', side_effect=AssertionError('Native evolution reached')) as native_call, \
             patch.object(FieldSolver, 'step', side_effect=AssertionError('Field update reached')) as field_call:
            hold_error = reject(run.hold)
            close_error = reject(run.close)
        assert native_call.call_count == field_call.call_count == 0
        assert snapshot(run.engine) == before
        assert not (run.recorder.path / 'final.restart.json.gz').exists()
        outcomes[name] = {'hold_error': hold_error, 'close_error': close_error,
                          'native_calls': native_call.call_count, 'field_calls': field_call.call_count,
                          'complete_state_and_reserves_unchanged': True,
                          'no_bad_final_restart': True, 'before': before}
        # Restore only this manufactured public session so its valid segment can close.
        run.session.clear(); run.session.update(saved); run.sensor.__dict__ = run.session['sensor']; run.close()
        outcomes[name]['intact_segment_verification'] = validators.verify_segment(run.recorder.path)
        e, s, m = runner.load_restart(run.recorder.path / 'final.restart.json.gz')
        loaded_before = snapshot(e)
        s['held_command'] = [-.5, .5]; s['hold_remaining'] = 4
        bad = OUT / ('loaded-bad-' + name)
        with patch.object(runner, 'Recorder', side_effect=AssertionError('Resume output reached')) as recorder:
            outcomes[name]['loaded_mutation_error'] = reject(lambda: runner.Run(e, m, bad, session=s), 'loaded pending/session state changed')
        assert recorder.call_count == 0 and not bad.exists() and snapshot(e) == loaded_before
    RESULT['checks']['pending_mutations'] = outcomes

def legal_continuation_and_boundaries():
    from loom_commissioning import pending
    first = create('legal-first'); first.begin_command()
    issued = first.session['held_command'].copy(); first.advance(7); first.close()
    resumed = runner.Run.resume(OUT / 'legal-first', OUT / 'legal-resumed')
    assert resumed.session['hold_remaining'] == 3
    inactive = state_hash(resumed.engine.organism)
    fields = []; real = FieldSolver.step
    def counted(self, *args, **kwargs):
        fields.append(args[4]); return real(self, *args, **kwargs)
    with patch.object(FieldSolver, 'step', counted):
        resumed.hold()
        assert resumed.engine.native_index == 10 and resumed.session['hold_remaining'] == 0
        assert resumed.engine.body.command.tolist() == issued and len(fields) == 3
        boundary = snapshot(resumed.engine)
        resumed.session['hold_remaining'] = 1
        stale_errors = [reject(resumed.hold) for _ in range(3)]
        assert snapshot(resumed.engine) == boundary and len(fields) == 3
        resumed.session['hold_remaining'] = 0
        expected, next_stage = controllers.waypoint_command(controllers.privileged_input(resumed.engine), copy.deepcopy(PLAN), 0)
        assert next_stage == 1
        resumed.hold()
    assert resumed.closed and resumed.engine.native_index == 20 and fields == [.01] * 13
    assert resumed.engine.body.command.tolist() == expected.tolist() != issued
    assert state_hash(resumed.engine.organism) == inactive
    assert validators.read_stream(OUT / 'legal-resumed/wave.jsonl.gz') == []
    actions = validators.read_stream(OUT / 'legal-resumed/controller.jsonl.gz')
    assert len(actions) == 1 and actions[0]['native_index'] == 10 and actions[0]['stage']['index'] == 1
    continuous = create('legal-continuous'); continuous.hold(); continuous.hold()
    assert state_hash(continuous.engine) == state_hash(resumed.engine)
    RESULT['checks']['legal_seven_plus_three'] = {'issued_pair': issued, 'fresh_stage_pair': expected.tolist(),
        'at_native_ten': boundary, 'final': snapshot(resumed.engine), 'resumed_field_updates': fields,
        'stale_pending_retry_errors': stale_errors, 'fresh_stage_action': actions[0],
        'inactive_neural_rng_unchanged': True, 'wave_records': 0,
        'continuous_complete_final_state_equal': True,
        'full_verifications': [validators.verify_segment(OUT / n) for n in ('legal-first', 'legal-resumed', 'legal-continuous')]}
    # Exactly the five delivered saved-boundary cases; detached clock checks, not lives.
    boundary_results = []
    for now, index, remaining, valid in ((.07, 7, 3, True), (.09, 9, 2, False),
        (.1, 10, 1, False), (.1 - 5e-11, 10, 1, False), (math.nextafter(.1, math.inf), 10, 1, False)):
        e, s, m = runner.load_restart(OUT / 'legal-first/final.restart.json.gz')
        e.time = now; e.native_index = index; s['hold_remaining'] = remaining
        before = snapshot(e)
        error = None
        if valid: pending.validate_pending(m, s, e)
        else: error = reject(lambda: pending.validate_pending(m, s, e))
        assert snapshot(e) == before
        result = {'time': now, 'native_index': index, 'remaining': remaining, 'accepted': valid,
                  'error': error, 'complete_state_unchanged': True}
        if index == 10:
            s['hold_remaining'] = 0; pending.validate_pending(m, s, e)
            _, stage = controllers.waypoint_command(controllers.privileged_input(e), copy.deepcopy(PLAN), 0)
            assert stage == 1; result['zero_remainder_selects_fresh_stage'] = stage
        boundary_results.append(result)
    RESULT['checks']['delivered_saved_boundary_cases'] = boundary_results

def global_cap():
    results = []
    for duration in (.07, .1):
        plan = copy.deepcopy(PLAN[:1]); plan[0]['until'] = duration
        run = create('global-' + str(duration), duration=duration, plan=plan)
        run.hold()
        assert run.closed and run.engine.native_index == round(duration / .01)
        assert run.session['hold_remaining'] == 0
        before = snapshot(run.engine); message = reject(run.hold)
        assert snapshot(run.engine) == before
        results.append({'duration': duration, 'final': before, 'further_hold_error': message,
                        'full_verification': validators.verify_segment(run.recorder.path)})
    RESULT['checks']['unchanged_global_cap'] = results

def journal_continuity():
    # The delivered coherent-payload test, copied into this new evidence directory.
    good = OUT / 'legal-first'; bad = OUT / 'changed-journal'
    shutil.copytree(good, bad)
    path = bad / 'final.restart.json.gz'
    wrapper = json.loads(gzip.decompress(path.read_bytes())); values = unpack(wrapper['state'])
    d = values['session']['decision']; d['inputs']['position'] = [7., 5.]
    pair, _ = controllers.waypoint_command(d['inputs'], copy.deepcopy(PLAN), 0)
    d['command'] = pair.tolist(); values['session']['held_command'] = pair.tolist()
    wrapper['state'] = pack(values); wrapper['sha256'] = digest(strict_bytes(wrapper['state']))
    raw = gzip.compress(strict_bytes(wrapper), mtime=0); path.write_bytes(raw)
    receipt_path = bad / 'manifest.json'; receipt = json.loads(receipt_path.read_bytes())
    receipt['files'][path.name] = {'bytes': len(raw), 'sha256': digest(raw)}
    receipt_path.write_bytes(strict_bytes(receipt))
    error = reject(lambda: validators.verify_segment(bad, replay=False), 'pending decision journal continuity mismatch')
    with patch.object(runner, 'Recorder', side_effect=AssertionError('Unverified resume output reached')) as recorder:
        resume_error = reject(lambda: runner.Run.resume(bad, OUT / 'changed-journal-resume'), 'pending decision journal continuity mismatch')
    assert recorder.call_count == 0 and not (OUT / 'changed-journal-resume').exists()
    RESULT['checks']['coherent_changed_journal'] = {'unmodified_issued_journal_rejects_changed_pending': error,
        'resume_error': resume_error, 'recorder_calls': recorder.call_count, 'physical_replay_required': False,
        'scope': 'Only copied new manufactured records changed; checksums honestly recomputed, matching delivered fixture.'}

if MODE == 'old': old_reproduction()
elif MODE == 'new':
    new_mutations(); legal_continuation_and_boundaries(); global_cap(); journal_continuity(); save()
    print('GREEN: known pending-hold failure rejected and delivered lawful continuations preserved', flush=True)
else: raise ValueError(MODE)
