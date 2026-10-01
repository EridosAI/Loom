"""Explicit unresolved-enclosure branch fixture; geometric evaluator stand-in.
No physical/organism run. No numerical configuration change.
"""
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd()))
import numpy as np
import loom_p.physics as p
from loom_p.schema import Config
from loom_p.geometry import fixtures

c = Config()
body = p.Body(np.array([2., 3.]), 0., velocity=np.array([-.001, 0.]))
original = p.gap_curve
fixture = fixtures(c, 0., 0.)[4]
calls = []
def unresolved(*args):
    # Samples lie exactly on the threshold, while the positive curvature
    # enclosure cannot rule out an excursion. This must not mean retention.
    calls.append(args[5])
    return c.geometry_tol, 0., fixture
p.gap_curve = unresolved
try:
    try:
        p.clear_excursion(c, body, np.array([.38, .38]), 0., 0., .01, 4, 0.)
    except ArithmeticError as error:
        message = str(error)
        assert message == 'Active-contact gap enclosure unresolved at event time tolerance'
    else:
        raise AssertionError('An unresolved enclosure silently returned instead of failing')
finally:
    p.gap_curve = original
result = dict(classification='VERIFIED', fixture='geometry evaluator stand-in exactly at threshold',
              error_type='ArithmeticError', message=message, gap_evaluations=len(calls),
              physical_steps=0, organism_created=False, configuration_sha256=c.identity())
original_bound = p.gap_curvature_bound
bound_calls = []
def loose_bound(*args):
    # Infinity bounds curvature, and 1e9 bounds this fixed path's actual speed.
    # The bound is deliberately uninformative; actual geometry is untouched.
    bound_calls.append(args[3])
    return np.inf, 1e9
p.gap_curvature_bound = loose_bound
try:
    try:
        p.clear_excursion(c, p.Body(np.array([2., 3.]), 0.), np.array([.38, .38]), 0., 0., .01, 4, 0.)
    except ArithmeticError as error:
        loose_message = str(error)
        assert loose_message == 'Active-contact gap enclosure unresolved at event time tolerance'
    else:
        raise AssertionError('Uninformative valid bound silently returned sustained contact')
finally:
    p.gap_curvature_bound = original_bound
result['actual_geometry_loose_bound_check'] = dict(
    fixture='touching source, stationary body, inward force; actual gap evaluator; deliberately loose valid bound only',
    error_type='ArithmeticError', message=loose_message, bound_evaluations=len(bound_calls),
    final_enclosure_duration=bound_calls[-1])
path = Path(__file__).with_name('failure-semantics.json')
path.write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
