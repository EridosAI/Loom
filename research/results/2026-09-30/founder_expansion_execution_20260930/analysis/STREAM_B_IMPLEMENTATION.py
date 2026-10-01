"""Remaining approved saved-input B checks, without duplicating large arrays.

Runs only after the first passive pipeline has stopped. Full vectors are
computed exactly, hashed at every wave, and summarized chronologically. The
immutable native inputs and checkpoints remain the lossless reconstruction
source. No world stepping, fields, controller, deep window or life continuation.
"""
import copy,hashlib,json,sys,time
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent;OUT=HERE/'analysis'
sys.path.insert(0,str(ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'))
from loom_developmental import codec
from loom_developmental.replay import reconstruct
from loom_developmental.runner import atomic_json,file_hash
from passive_ab import checkpoint_row,norm

def main():
    assert (HERE/'DELIVERY_VERIFICATION.json').exists(), 'First pipeline must have stopped'
    clock=json.loads((OUT/'ANALYSIS_CLOCK.json').read_bytes());started=clock['monotonic_started']
    rows=json.loads((OUT/'ALL_SIXTY_AB.json').read_bytes());prior=[]
    for mode in ('consequential','remaining'):
        prior.extend(json.loads((OUT/f'B_RECONSTRUCTION_{mode}_COMPLETION.json').read_bytes())['results'])
    passed={r['life_id'] for r in prior if r['status']=='PASS'}
    with (OUT/'STREAM_B_IMPLEMENTATION.py').open('xb') as f:f.write(Path(__file__).read_bytes())
    atomic_json(OUT/'STREAM_B_START.json',dict(original_analysis_clock_sha256=file_hash(OUT/'ANALYSIS_CLOCK.json'),
        implementation_sha256=file_hash(__file__),previous_fully_checked=sorted(passed),
        rationale='Complete remaining approved B verification within the same wall/storage limits; avoid duplicate full arrays.',
        representation='Chronological float64 operand summaries and exact full-wave operand SHA256; original lossless native/checkpoint evidence unchanged.',
        new_physical_steps=0,deep_windows=0))
    results=[];stop=None
    for row in rows:
        name=row['life_id']
        if name in passed:continue
        if not row.get('complete'):
            results.append(dict(life_id=name,status='UNSEALED_PREFIX_ONLY',reason='No manufactured receipt or final state'));continue
        if stop:
            results.append(dict(life_id=name,status='PENDING',reason=stop));continue
        base=HERE if int(name[3:])>=13 else ROOT/'founder_initial_execution_20260930';store=base/'lives'/name
        receipt=json.loads((store/'segment-000.json').read_bytes());cp=receipt['initial_checkpoint']
        initial=codec.read(store/cp['file'],cp['sha256'])['engine'];summaries=[];digests=[];observed=0;first_tick=time.perf_counter()
        used=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())
        def callback(index,e,diag):
            nonlocal observed
            observed+=1
            if index%100==0:
                if time.perf_counter()-started>=4320:raise RuntimeError('Original shared analysis time closure reserve')
                if used+8_000_000>=2_500_000_000:raise RuntimeError('Original shared analysis storage closure reserve')
            if e.last_wave is None:return
            o=e.organism;a=o.association;r=o.regulator
            # Same full-vector payload as the retained full-array B records.
            payload=dict(native_index=index,time=e.time,wave=o.wave_count,
                cortices=[{k:getattr(c,k).copy() for k in ('shared','fine','shared_ref','fine_ref','opening','mean','x','C')} for c in o.cortices],
                credit=copy.deepcopy(r.credit_diagnostic),regulation=copy.deepcopy(r.output_diagnostic),
                maps=copy.deepcopy(a.diagnostic['map_updates']),gates=a.diagnostic['gates'].copy(),
                q=a.q.copy(),use=copy.deepcopy(a.use),write_count=a.write_count,motor=copy.deepcopy(o.motor.diagnostic))
            digests.append(np.frombuffer(hashlib.sha256(codec.encode(payload)).digest(),dtype=np.uint8).copy())
            z=checkpoint_row(e,initial,cp);z.pop('checkpoint_file');z.pop('checkpoint_sha256')
            z.update(credit_E=float(r.credit_diagnostic['trend'][0]),credit_I=float(r.credit_diagnostic['trend'][1]),
                learning_E_norm=norm(r.credit_diagnostic['learning'][0]),learning_I_norm=norm(r.credit_diagnostic['learning'][1]),
                learned_E_norm=norm(r.output_diagnostic['learned'][0]),learned_I_norm=norm(r.output_diagnostic['learned'][1]),
                exploration_E_norm=norm(r.output_diagnostic['exploration'][0]),exploration_I_norm=norm(r.output_diagnostic['exploration'][1]),
                support_mean=float(r.h.mean()),motor_evocation_norm=norm(o.motor.diagnostic['evoked']),
                motor_oscillator_norm=norm(o.motor.diagnostic['oscillator']),motor_direct_feedback_norm=norm(o.motor.diagnostic['direct_feedback']))
            summaries.append(z)
        replay=None;status='PASS'
        try:
            replay=reconstruct(store,fields=False,deep=False,callback=callback)
            final=replay.pop('engine');replay['endpoint_P_sha256']=codec.digest(final.organism)
        except Exception as error:stop=f'{type(error).__name__}: {error}';status='INCOMPLETE'
        columns=list(summaries[0]) if summaries else []
        value=dict(columns=columns,values=np.array([[v[k] for k in columns] for v in summaries],dtype='<f8'),
            full_operand_sha256=np.array(digests,dtype=np.uint8),hash_payload='Exact payload keys documented in stream_remaining_b.py; no rounding',
            original_receipt_sha256=file_hash(store/'segment-000.json'),full_vectors_regenerable_from_original_evidence=True)
        record=codec.write(OUT/(name+'_streamed_wave_summary.ld'),value,level=1)
        old=next((x for x in prior if x['life_id']==name),{})
        item=dict(life_id=name,status=status,reason=stop,reconstruction=replay,record=record,
            requested_native=row['native_steps'],native_observed=observed,waves=len(summaries),
            earlier_partial_reconstruction_overlap_native=old.get('native_observed',0),
            wall_seconds=time.perf_counter()-first_tick,new_physical_steps=0,full_vector_duplicate_files=False)
        atomic_json(OUT/(name+'_STREAM_B.json'),item);results.append(item)
        print(json.dumps(dict(life_id=name,status=status,waves=len(summaries),wall_seconds=item['wall_seconds'])),flush=True)
    atomic_json(OUT/'STREAM_B_COMPLETION.json',dict(results=results,previous_full_array_passes=sorted(passed),stop=stop,
        complete_verified_lives=len(passed)+sum(r['status']=='PASS' for r in results),
        elapsed_from_original_analysis_start=time.perf_counter()-started,new_physical_steps=0,deep_windows=0,
        bytes=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())))
if __name__=='__main__':main()
