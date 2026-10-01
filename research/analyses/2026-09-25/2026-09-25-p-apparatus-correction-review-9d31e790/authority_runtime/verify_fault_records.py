"""Check whether unchanged saved-record validators detect the runtime binding faults."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology')
from loom_commissioning.validators import verify_segment
records=Path(json.loads((ROOT/'RUNTIME_BINDING_RESULTS.json').read_text())['components'])
result={}
for name in ('alias-version','held-command','held-count','persist-first','persist-resumed'):
    try:
        result[name]={'accepted':True,'result':verify_segment(records/name)}
    except Exception as error:
        result[name]={'accepted':False,'error':f'{type(error).__name__}: {error}'}
(ROOT/'FAULT_RECORD_VALIDATION.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
