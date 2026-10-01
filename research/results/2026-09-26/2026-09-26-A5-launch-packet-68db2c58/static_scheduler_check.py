"""Pure scalar/native-index preflight. Does not construct or advance a world."""
import csv
import io


def audit(m, clock, controllers):
    ends = clock.stage_ends(m)
    assert ends == (9000, 12000, 27000, 30000, 45000, 48000, 63000)
    assert clock.case_end(m) == 63000
    selected = {26949, 26950, 26951, 26999, 27000, 27001, 63000}
    selected.update(i + delta for i in ends for delta in (-1, 0, 1) if 0 <= i + delta <= 63000)
    rows = []
    hold_rows = []
    t = 0.0
    max_error = 0.0
    for i in range(63001):
        clock.validate_physical_time(m, i, t)
        decision = clock.decision_clock(m, i)
        stage = controllers.waypoint_stage(decision, len(ends))
        oracle = min(sum(i >= end for end in ends), len(ends) - 1)
        assert stage == oracle
        err = t - clock.expected_time(m, i)
        max_error = max(max_error, abs(err))
        if i < 63000 and i % 10 == 0:
            count = clock.hold_steps(m, i)
            assert count == 10 and i + count <= ends[stage]
            assert i + count <= clock.case_end(m)
            hold_rows.append((i, i + count, stage, ends[stage], t, clock.expected_time(m, i)))
        if i in selected:
            rows.append(dict(native_index=i, accumulated_scalar_time=t,
                             nominal_time=clock.expected_time(m, i), error=err,
                             allowance=clock.clock_allowance(m, i), stage_zero_based=stage,
                             fresh_hold_permitted=i < 63000 and i % 10 == 0,
                             case_complete=i == 63000))
        if i < 63000:
            t += .01
    assert len(hold_rows) == 6300
    for i in (26949, 26951, 26999, 27001, 63000):
        try:
            clock.hold_steps(m, i)
        except ValueError:
            pass
        else:
            raise AssertionError(('unexpected fresh hold', i))
    by_index = {r['native_index']: r for r in rows}
    assert abs(by_index[26950]['error']) > 1e-10
    assert by_index[26950]['stage_zero_based'] == 2
    assert by_index[27000]['stage_zero_based'] == 3
    assert by_index[26950]['fresh_hold_permitted'] and by_index[27000]['fresh_hold_permitted']
    out = io.StringIO(newline='')
    writer = csv.writer(out, lineterminator='\n')
    writer.writerow(('start_native_index', 'end_native_index', 'stage_zero_based',
                     'stage_end_native_index', 'accumulated_scalar_time', 'nominal_time'))
    writer.writerows(hold_rows)
    return dict(status='PASS — scalar scheduling compatibility only', native_indices_checked=63001,
                prescribed_holds_checked=6300, stage_end_indices=list(ends), case_end_index=63000,
                all_stage_and_case_guards_pass=True, physical_clock_checks_pass=True,
                former_269_5_rejection_absent=True, independent_270_rejection_absent=True,
                holds_end_at_stage_boundary_without_shortening=True, final_time=t,
                maximum_absolute_accumulation_error=max_error, boundary_rows=rows,
                world_steps=0, controller_commands=0, simulation_RNG_draws=0,
                note='The loop adds scalar 0.01 values and calls pure scheduler functions. No Engine, Run, command, field, sensor, event, neural or RNG function is invoked. Cadence representability is not a physical trajectory or runtime benchmark.'), out.getvalue()
