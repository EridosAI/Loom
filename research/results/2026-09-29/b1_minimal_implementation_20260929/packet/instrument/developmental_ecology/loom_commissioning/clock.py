"""Apparatus scheduling only. Never assigns physical time or advances state."""
from fractions import Fraction
import math
from .contract import require


def grid_steps(value, origin=0):
    """JSON decimal spellings must specify an exact native-grid offset.

    No nearest-tick repair: even a small off-grid declared deadline is rejected.
    The accumulated physical timestamp is NOT passed through this conversion.
    """
    require(type(value) in (int, float) and math.isfinite(value)
            and type(origin) in (int, float) and math.isfinite(origin), 'nonfinite scheduling time')
    steps = (Fraction(str(value)) - Fraction(str(origin))) * 100
    require(steps.denominator == 1, 'scheduling time is not native-grid aligned')
    return int(steps)


def case_end(m):
    require(type(m['initial_index']) is int and m['initial_index'] >= 0, 'invalid initial native index')
    count = grid_steps(m['duration_seconds'])
    require(0 < count <= 120000, 'duration cap invalid')
    require(math.isfinite(m['initial_time']) and math.isfinite(m['hard_stop_time'])
            and abs(m['hard_stop_time'] - (m['initial_time'] + m['duration_seconds'])) < 1e-9,
            'duration cap identity mismatch')
    return m['initial_index'] + count


def stage_ends(m):
    end = case_end(m)
    plan = m['execution']['procedure']['stages']
    ends = tuple(m['initial_index'] + grid_steps(p['until'], m['initial_time']) for p in (plan or []))
    require(not ends or m['initial_index'] < ends[0] and ends[-1] <= end
            and all(a < b for a, b in zip(ends, ends[1:])), 'route outside duration scope')
    return ends


def decision_clock(m, index):
    require(type(index) is int and m['initial_index'] <= index <= case_end(m), 'duration cap bypass')
    return index, stage_ends(m)


def hold_steps(m, index):
    end = case_end(m)
    require(type(index) is int and m['initial_index'] <= index < end, 'duration cap reached')
    require((index - m['initial_index']) % 10 == 0, 'decision is not at a ten-step boundary')
    return min(10, end - index)


def expected_time(m, index):
    return m['initial_time'] + (index - m['initial_index']) * .01


def clock_allowance(m, index):
    """Binary64 summation bound, plus the existing 1e-10 consistency floor.

    gamma_n bounds n repeated additions of the same represented dt. Two ULPs
    cover the separately evaluated multiply/add expected time. The allowance
    is exclusively diagnostic, never a scheduling/deadline comparison band.
    Reject origins too large to distinguish a quarter native step.
    """
    n = index - m['initial_index']
    require(type(index) is int and 0 <= n <= 120000, 'invalid native clock progress')
    u = 2.**-53
    gamma = n*u/(1-n*u)
    expected = expected_time(m, index)
    allowance = 1e-10 + gamma*(abs(m['initial_time']) + n*.01) + 2*math.ulp(expected)
    require(math.isfinite(allowance) and allowance < .0025, 'physical clock precision outside supported domain')
    return allowance


def validate_physical_time(m, index, time, terminal=False):
    require(type(index) is int and m['initial_index'] <= index <= case_end(m)
            and type(time) in (int, float) and math.isfinite(time), 'physical/native clock mismatch')
    expected = expected_time(m, index)
    allowance = clock_allowance(m, index)
    if terminal:
        require(index > m['initial_index'] and expected_time(m, index-1)-allowance <= time <= expected+allowance,
                'terminal physical/native clock mismatch')
    else:
        require(abs(time-expected) <= allowance, 'physical/native clock mismatch')
