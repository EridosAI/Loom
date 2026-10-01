"""Post-archive saved-input P reconstruction. Never evolves fields or physics."""
import copy
import json
import time
from pathlib import Path
import sys
import numpy as np

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=HERE/'analysis'
sys.path.insert(0,str(ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'))
from loom_developmental import codec
from loom_developmental.replay import reconstruct
from loom_developmental.runner import atomic_json,file_hash
from passive_ab import guard,plain,norm,csv_out

def main():
    guard()
    assert (OUT/'AB_COMPLETION.json').exists()
    rows=json.loads((OUT/'ALL_SIXTY_AB.json').read_bytes())
    mode=sys.argv[1] if len(sys.argv)>1 else 'all'
    assert mode in ('all','consequential','remaining')
    def consequential(r):return int(r['life_id'][3:])>=13 and any(r.get(k,0)>0 for k in ('transfer_total','repair','damage'))
    if mode=='consequential':rows=[r for r in rows if consequential(r)]
    if mode=='remaining':rows=[r for r in rows if not consequential(r)]
    atomic_json(OUT/('B_RECONSTRUCTION_'+mode+'_STARTED.json'),dict(monotonic=time.perf_counter(),
        scope='Realized saved inputs only; fields=False, deep=False; deterministic roster within declared analysis priority',mode=mode,
        AB_sha256=file_hash(OUT/'ALL_SIXTY_AB.json')))
    directory=OUT/'wave_operands';directory.mkdir(exist_ok=True)
    initial_bytes=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())
    written=0; results=[];stop=None
    for row in rows:
        if not row.get('complete'):
            results.append(dict(life_id=row['life_id'],status='NO_COMPLETE_STORE'));continue
        if stop:
            results.append(dict(life_id=row['life_id'],status='PENDING',reason=stop));continue
        name=row['life_id'];base=HERE if int(name[3:])>=13 else ROOT/'founder_initial_execution_20260930'
        buffers=[];summaries=[];files=[];first=None;last=None;native_count=0
        def flush():
            nonlocal written
            if not buffers:return
            f=directory/f'{name}-waves-{buffers[0]["wave"]:05d}-{buffers[-1]["wave"]:05d}.ld'
            record=codec.write(f,buffers,level=1);files.append(record);written+=record['bytes'];buffers.clear()
        def observe(index,e,diag):
            nonlocal first,last,native_count
            native_count+=1
            if index%100==0:
                guard()
                elapsed=time.perf_counter()-json.loads((OUT/'ANALYSIS_CLOCK.json').read_bytes())['monotonic_started']
                reserve_deadline=3300 if mode=='consequential' else 4300
                if elapsed>=reserve_deadline:raise RuntimeError('Shared analysis time reserved for remaining C/report closure')
                if initial_bytes+written+100_000_000>=2_500_000_000:raise RuntimeError('Derived evidence storage reserve reached')
            if e.last_wave is None:return
            o=e.organism;a=o.association;r=o.regulator
            credit=r.credit_diagnostic
            # No duplicate complete H matrices: their exact realized inputs and
            # original checkpoints remain sealed. Preserve all map write/decay/
            # projection/use operands and exact per-wave structural/bank arrays.
            sample=dict(native_index=index,time=e.time,wave=o.wave_count,
                cortices=[{k:getattr(c,k).copy() for k in ('shared','fine','shared_ref','fine_ref','opening','mean','x','C')} for c in o.cortices],
                credit=copy.deepcopy(credit),regulation=copy.deepcopy(r.output_diagnostic),
                maps=copy.deepcopy(a.diagnostic['map_updates']),gates=a.diagnostic['gates'].copy(),
                q=a.q.copy(),use=copy.deepcopy(a.use),write_count=a.write_count,
                motor=copy.deepcopy(o.motor.diagnostic))
            buffers.append(sample)
            z=dict(native_index=index,time=e.time,wave=o.wave_count,
                credit_E=float(credit['trend'][0]),credit_I=float(credit['trend'][1]),
                theta_E_norm=norm(r.theta[0]),theta_I_norm=norm(r.theta[1]),
                reference_E_norm=norm(r.reference[0]),reference_I_norm=norm(r.reference[1]),
                eligibility_E_norm=norm(r.eligibility[0]),eligibility_I_norm=norm(r.eligibility[1]),
                learning_E_norm=norm(credit['learning'][0]),learning_I_norm=norm(credit['learning'][1]),
                reference_force_E_norm=norm(credit['reference_force'][0]),reference_force_I_norm=norm(credit['reference_force'][1]),
                H_write_norm=float(sum(np.sum(v['write_norm']) for v in a.diagnostic['map_updates'].values())),
                H_decay_norm=float(sum(np.sum(v['decay_norm']) for v in a.diagnostic['map_updates'].values())),
                H_projection_norm=float(sum(np.sum(v['projection_norm']) for v in a.diagnostic['map_updates'].values())),
                q_norm=norm(a.q),H_use_mean=float(np.concatenate(list(a.use.values())).mean()),
                learned_E_norm=norm(r.output_diagnostic['learned'][0]),learned_I_norm=norm(r.output_diagnostic['learned'][1]),
                exploration_norm=norm(r.output_diagnostic['exploration']))
            for m,c in enumerate(o.cortices):
                for k in ('shared','fine','shared_ref','fine_ref','x','C'):
                    z[f'c{m}_{k}_norm']=norm(getattr(c,k))
                z[f'c{m}_reference_separation']=norm(c.fine-c.fine_ref)
            summaries.append(z)
            if first is None:first=index
            last=index
            if len(buffers)>=100:flush()
        started=time.perf_counter();result=None
        try:
            result=reconstruct(base/'lives'/name,deep=False,fields=False,callback=observe)
            endpoint=result.pop('engine')
            result['endpoint_P_sha256']=codec.digest(endpoint.organism)
            status='PASS'
        except Exception as error:
            stop=f'{type(error).__name__}: {error}';status='INCOMPLETE'
        finally:
            flush();csv_out(name+'_exact_wave_summary.csv',summaries)
            summary_path=OUT/(name+'_exact_wave_summary.csv')
            if summary_path.exists():written+=summary_path.stat().st_size
            item=dict(life_id=name,status=status,reason=stop,requested_native=row['native_steps'],
                native_observed=native_count,first_wave_native=first,last_wave_native=last,waves=len(summaries),
                files=files,reconstruction=result,wall_seconds=time.perf_counter()-started,
                warmup_native_steps=0,physical_steps=0,fields_reconstructed=False,
                incomplete_claim='Only returned completed reconstruction reports certify all requested chunk endpoints; interrupted records retain explicit incomplete status.')
            atomic_json(OUT/(name+'_B_RECONSTRUCTION.json'),plain(item));results.append(item)
            written+=(OUT/(name+'_B_RECONSTRUCTION.json')).stat().st_size
            print(json.dumps(dict(life_id=name,status=status,native=native_count,waves=len(summaries),wall_seconds=item['wall_seconds'])),flush=True)
    atomic_json(OUT/('B_RECONSTRUCTION_'+mode+'_COMPLETION.json'),plain(dict(results=results,stop=stop,
        complete=sum(x['status']=='PASS' for x in results),new_world_steps=0,
        derived_operand_bytes=written,records_are_detached=True)))

if __name__=='__main__':main()
