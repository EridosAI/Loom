"""Apply the rejection expectation to the already executed exact alias fixture.

Reads evidence only; does not repeat the physical fixture or edit its result.
"""
import json,sys
from pathlib import Path
row=json.loads(Path(sys.argv[1]).read_bytes())['exact_alias']
assert row['rejection'] is not None and row['alternate_calls']==0 and row['native_index']==0 and row['time']==0 and row['engine_unchanged'], 'ORIGINAL CONTROLLER DISPATCH BREACH: substituted controller executed instead of rejection before advancement'
print('GREEN: exact alias substitution rejected before invocation, recording and advancement')
