"""At most 196 deterministically anchored, named 0.2-second saved-input P windows.

Requires complete all-roster A/B tables and a selection manifest written after
those tables. Does not evolve physics or write back to any sealed life store.
"""
import json
from pathlib import Path
import sys
import time
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
D=ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'
OUT=HERE/'analysis'
sys.path.insert(0,str(D))
from loom_developmental import codec
from loom_developmental.replay import reconstruct
from loom_developmental.runner import atomic_json,file_hash
from passive_ab import guard,plain,norm

def main():
    guard()
    assert (OUT/'AB_COMPLETION.json').exists()
    selection=json.loads((OUT/'C_WINDOW_SELECTION.json').read_bytes())
    assert selection['all_sixty_AB_sha256']==file_hash(OUT/'ALL_SIXTY_AB.json')
    assert len(selection['windows'])<=196
    if (OUT/'C_START.json').exists():raise FileExistsError('No repeated deep windows')
    atomic_json(OUT/'C_START.json',dict(selection_sha256=file_hash(OUT/'C_WINDOW_SELECTION.json'),monotonic=time.perf_counter()))
    results=[];pending=[]
    for chosen in selection['windows']:
        guard()
        elapsed=time.perf_counter()-json.loads((OUT/'ANALYSIS_CLOCK.json').read_bytes())['monotonic_started']
        if elapsed>4380 or sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())>2_400_000_000:
            pending.append(dict(chosen,reason='Analysis closure/storage reserve'));continue
        first=chosen['first_index'];last=chosen['last_index'];name=chosen['name']
        assert last-first==19 and first>0
        receipt=json.loads((HERE/'lives'/chosen['life_id']/'segment-000.json').read_bytes())
        assert last<=receipt['final_index']
        samples=[];deep_rows=[]
        def observe(index,e,diag):
            guard();deep_rows.append(diag)
            row=dict(native_index=index,time=e.time)
            if 'D5_native' in diag:
                d=diag['D5_native'];base=d['baseline']['command']
                row['motor_component_norms']={k:norm(v) for k,v in d['contributions'].items()}
                row['immediate_command_omission_delta_norm']={k:norm(v['command']-base) for k,v in d['without'].items()}
            if 'D5_wave' in diag:
                d=diag['D5_wave'];base=d['baseline']['controls']
                row['immediate_controls_omission_delta_norm']={k:norm(v['controls']-base) for k,v in d['without'].items()}
                row['sensory_context_dependency']={k:dict(q_delta=norm(v['q_difference']),controls_delta=norm(v['receiver']['controls']-base)) for k,v in d['query_support_dependencies'].items()}
                row['applied_theta_delta_norm']=norm(diag['credit_separate_E_I']['applied_theta_delta'])
            row['cortical_shared_native_delta_norms']=[norm(x['shared_applied_delta']) for x in diag['cortices']]
            row['cortical_fine_native_delta_norms']=[norm(x['fine_applied_delta']) for x in diag['cortices']]
            samples.append(row)
        started=time.perf_counter()
        replay=reconstruct(HERE/'lives'/chosen['life_id'],first_index=first,last_index=last,deep=True,fields=False,callback=observe)
        final=replay.pop('engine')
        exact=codec.write(OUT/(name+'_deep.ld'),deep_rows,level=1)
        summary=dict(**chosen,wall_seconds=time.perf_counter()-started,reconstruction=replay,
            causal_scope='Saved inputs, exact P/RNG/chunk checks where crossed; local immediate receiver omissions only. No alternative physical trajectory or benefit counterfactual.',
            native_samples=samples,deep_record=exact,endpoint_P_sha256=codec.digest(final.organism))
        atomic_json(OUT/(name+'.json'),plain(summary));results.append(summary)
        print(json.dumps(dict(window=name,life_id=chosen['life_id'],native_samples=len(samples),physics_executed=False)),flush=True)
    atomic_json(OUT/'C_WINDOWS_COMPLETE.json',plain(dict(windows=results,count=len(results),pending=pending,new_ecological_steps=0,
        analysis_wall_elapsed=time.perf_counter()-json.loads((OUT/'ANALYSIS_CLOCK.json').read_bytes())['monotonic_started'])))

if __name__=='__main__':main()
