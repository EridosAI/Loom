"""Detached calculation from existing manufactured records; zero world steps."""
import copy
import json
from pathlib import Path
import sys

TARGET = Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
sys.path.insert(0, str(TARGET / 'developmental_ecology'))
from loom_commissioning.controllers import waypoint_command
from loom_commissioning.runner import load_restart
from loom_commissioning.validators import read_stream

OUT = Path(__file__).resolve().parent
actions = read_stream(OUT / 'hold-continuous/controller.jsonl.gz')
_, session, _ = load_restart(OUT / 'hold-continuous/initial.restart.json.gz')
plan = session['route']
actual = actions[1]['inputs']
rounded = copy.deepcopy(actual)
rounded['time'] = .1
a, cursor_a = waypoint_command(actual, plan, 0)
b, cursor_b = waypoint_command(rounded, plan, 0)
assert actual['time'] == 0.09999999999999999 and cursor_a == 0 and cursor_b == 1
assert (a != b).any() and a.tolist() == actions[1]['command']
result = {'scope': 'detached one-call calculation; no new trajectory', 'plan': plan,
          'actual_saved_time': actual['time'], 'mathematical_native_boundary': .1,
          'difference_seconds': .1-actual['time'], 'actual_cursor': cursor_a,
          'exact_boundary_cursor': cursor_b, 'actual_command': a.tolist(),
          'exact_boundary_command': b.tolist(), 'hold_native_steps': actions[1]['hold_native_steps']}
(OUT / 'ROUTE_BOUNDARY_RESULTS.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
