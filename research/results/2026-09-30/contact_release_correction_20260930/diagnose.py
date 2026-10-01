"""Exact single-step engineering reconstruction, isolated from historical records."""
from pathlib import Path
import copy, hashlib, json, sys
import numpy as np
HERE=Path(__file__).resolve().parent; ROOT=HERE.parent
PREP=ROOT/'motor_commissioning_preparation_20260930_v0_1'
D=ROOT/'worktrees/loom-contact-release-20260930/developmental_ecology'
sys.path[:0]=[str(D),str(PREP)]
from loom_motor_commissioning import codec
from loom_developmental import core
from loom_p import physics
from loom_p.geometry import fixtures, gap_normal

def plain(v):
    if isinstance(v,np.ndarray):return v.tolist()
    if isinstance(v,np.generic):return v.item()
    if isinstance(v,dict):return {str(k):plain(x) for k,x in v.items()}
    if isinstance(v,(list,tuple)):return [plain(x) for x in v]
    if isinstance(v,(str,int,float,bool)) or v is None:return v
    return plain(vars(v)) if hasattr(v,'__dict__') else str(v)

tail=PREP/'execution/lives/MC-FS-001-M2/failure-tail-s000.ld'
saved=codec.read(tail)
print('Tail keys:',list(saved))
e=copy.deepcopy(saved['engine']);e.status='paused'
before=codec.digest(core.causal_state(e)); traces=[]; inputs=[]
def trace(frame,event,arg):
    if Path(frame.f_code.co_filename)==D/'loom_p/physics.py':
        name=frame.f_code.co_name; L=frame.f_locals
        if name=='advance' and event=='call':
            inputs.append(plain({k:L[k] for k in ('c','body','stocks','t','phase','command','dt')}))
        if name=='release_probe' and event=='call':
            traces.append(dict(function=name,event=event,locals=plain({k:L[k] for k in ('body','forces','t','phase','dt','index')})))
        if name in ('clear_excursion','search') and event in ('return','exception'):
            traces.append(dict(function=name,event=event,return_value=plain(arg) if event=='return' else str(arg[1]),
                locals={k:plain(v) for k,v in L.items() if k not in ('search','c','body','forces')}))
        if name=='release_probe' and event=='return':
            traces.append(dict(function=name,event=event,return_value=arg,
                locals={k:plain(L[k]) for k in ('gap','n','u','A','J','probe','acceleration','relative') if k in L}))
    return trace
sys.settrace(trace)
try:
    core.step(e)
    result='UNEXPECTED_SUCCESS'
except Exception as error:
    result=f'{type(error).__name__}: {error}'
finally:sys.settrace(None)
out=dict(purpose='ONE_STEP_ENGINEERING_RECONSTRUCTION_NOT_COMMISSIONING_CONTINUATION',
    saved_tail_sha256=hashlib.sha256(tail.read_bytes()).hexdigest(),source_sha256=hashlib.sha256((D/'loom_p/physics.py').read_bytes()).hexdigest(),
    committed_index=saved['engine'].native_index,result=result,physical_inputs=inputs,traces=traces)
(HERE/'EXACT_FAILURE_TRACE.json').write_text(json.dumps(out,indent=2),encoding='utf8')
assert result=='ArithmeticError: Free-path release prefix crosses solid before clearance',result
assert len(inputs)==1
(HERE/'EXACT_PHYSICAL_INPUT.json').write_text(json.dumps(inputs[0],indent=2),encoding='utf8')
print(result)
for row in traces:
    if row['function']=='search':print('SEARCH',row['event'],row.get('return_value'),{k:row['locals'].get(k) for k in ('end','sign','limit','a','b','h','mid','ga','gb','gm')})
print('input',json.dumps(inputs[0]['body']), 'time',inputs[0]['t'],'phase',inputs[0]['phase'],'command',inputs[0]['command'])
