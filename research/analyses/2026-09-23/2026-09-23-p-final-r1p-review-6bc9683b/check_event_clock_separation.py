"""Manufactured scheduler/physics component; no real neural/field lifetime.
Uses real Engine.step/_coupled and real oblique physics, with instrumented
fixed-command learner and field stand-ins. Writes only a sibling receipt.
"""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import numpy as np
import loom_p.engine as module
from loom_p.engine import Engine
from loom_p.physics import Body
from loom_p.schema import Config, Streams

old_transduce = module.transduce
results = []
try:
    for start_index in (19, 50):
        calls = []
        rng = Streams(Config().master_seed)
        def native(raw, dt, refresh_noise):
            calls.append(['native', dt, refresh_noise])
            if refresh_noise: rng.draw('review-native-noise', (1,))
            return np.ones(2)
        def handoff(reserves):
            calls.append(['handoff'])
            rng.draw('review-handoff', (1,))
            return {'component_handoff': True}
        def fields(old, stocks, t, phase, dt, position):
            calls.append(['field', dt])
            return old
        e = Engine.__new__(Engine)
        e.c=Config(); e.time=0.; e.phase=0.; e.native_index=start_index
        e.status='paused'; e.failure=None; e.terminal_dimension=None
        e.body=Body(np.array([2.,3.]),float(np.arccos(.01/.76)),velocity=np.array([-1e-5,0.]))
        e.stocks=np.full(8,.2); e.fields=np.zeros((2,1,1))
        e.raw=[np.zeros(d) for d in (10,4,8,7)]
        e.organism=SimpleNamespace(native=native,handoff=handoff,rng=rng)
        e.solver=SimpleNamespace(step=fields)
        e.last_wave=None; e.last_events=[]; e.last_native={}
        e.observe_native=lambda dt:dict(time=e.time,elapsed=dt,index=e.native_index)
        e.validate_state=lambda:True
        module.transduce=lambda *args:e.raw
        _,wave,events=e.step()
        expected=[['native',.01,start_index==50],['field',.01]]
        if start_index==19: expected.append(['handoff'])
        assert calls==expected, calls
        assert len(events)==4 and sum(r.get('event_kind')=='release' for r in events)==1
        assert sum(r.get('event_kind')=='recontact_or_first_touch' for r in events)==1
        assert e.native_index==start_index+1 and e.time==.01
        expected_draws={'life/review-handoff':1} if start_index==19 else {'life/review-native-noise':1}
        assert rng.counters==expected_draws, rng.counters
        results.append(dict(start_index=start_index,end_index=e.native_index,time=e.time,
            event_count=len(events),calls=calls,counters=copy.deepcopy(rng.counters),wave=wave))
finally:
    module.transduce=old_transduce
output=Path(__file__).with_name('EVENT_CLOCK_SEPARATION.json')
with output.open('x',encoding='utf-8') as f:
    json.dump(dict(method='Real scheduler and oblique physics; instrumented fixed-command learner/field/observer stand-ins; no free organism lifetime',cases=results),f,indent=2)
print(json.dumps(results,indent=2))
