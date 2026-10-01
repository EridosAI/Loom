"""Detached final-route deadline check, using the existing ten-step fixture."""
import copy
import json
from pathlib import Path
import sys

TARGET = Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
sys.path.insert(0, str(TARGET / 'developmental_ecology'))
from loom_commissioning.controllers import waypoint_command
from loom_commissioning.validators import read_stream

OUT = Path(__file__).resolve().parent
action = read_stream(OUT / 'hold-continuous/controller.jsonl.gz')[1]
actual = action['inputs']
rounded = copy.deepcopy(actual)
rounded['time'] = .1
plan = [{'point': [6., 5.], 'until': .1, 'press_force': 0.}]
a, _ = waypoint_command(actual, plan, 0)
b, _ = waypoint_command(rounded, plan, 0)
assert a.any() and not b.any()
result = {'scope': 'detached final-until check; zero additional world steps',
    'actual_time': actual['time'], 'nominal_native_boundary': .1,
    'actual_command': a.tolist(), 'exact_boundary_command': b.tolist(),
    'next_hold_native_steps': action['hold_native_steps'], 'single_entry_plan': plan}
(OUT / 'FINAL_UNTIL_RESULTS.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result, indent=2))
