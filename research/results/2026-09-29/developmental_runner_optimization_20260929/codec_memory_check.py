"""Saved-record-only memory/byte-equivalence check; no simulation or P calls."""
import gc
import hashlib
import json
from pathlib import Path
import shutil
import sys
import types
from benchmark import memory,D,OUT
from loom_developmental import codec

phase=sys.argv[1]
if phase not in ('before','after'):raise ValueError(phase)
result_path=OUT/('codec-memory-'+phase+'.json')
if result_path.exists():raise FileExistsError(result_path)
if phase=='before':
    target=OUT.parent/'benchmarked_apparatus_before_memory_fix'
    shutil.copytree(D/'loom_developmental',target,ignore=shutil.ignore_patterns('__pycache__'))
first=sorted((OUT/'long').glob('chunk-*.ld'))[0]
value=codec.read(first);expected=hashlib.sha256(codec.encode(value)).hexdigest()
def retained():
    counts={'put':0,'get':0};parts_bytes=0
    for obj in gc.get_objects():
        if isinstance(obj,types.FunctionType) and obj.__name__ in counts and obj.__code__.co_filename.endswith('codec.py'):
            counts[obj.__name__]+=1
            cells=dict(zip(obj.__code__.co_freevars,obj.__closure__ or ()))
            if 'parts' in cells:
                try:parts_bytes+=sum(len(p) for p in cells['parts'].cell_contents)
                except ValueError:pass
    return {'closures':counts,'retained_encoding_parts_bytes':parts_bytes,**memory()}
gc.collect();baseline=retained();gc.disable()
try:
    for _ in range(100):
        blob=codec.encode(value);restored=codec.decode(blob)
        assert hashlib.sha256(blob).hexdigest()==expected
    before_collection=retained()
finally:gc.enable()
collected=gc.collect();after_collection=retained()
result={'phase':phase,'world_steps':0,'P_calls':0,'iterations':100,
    'encoded_sha256':expected,'encoded_bytes':len(blob),'baseline':baseline,
    'before_collection':before_collection,'after_collection':after_collection,'collected':collected}
result_path.write_text(json.dumps(result,indent=2));print(json.dumps(result))
