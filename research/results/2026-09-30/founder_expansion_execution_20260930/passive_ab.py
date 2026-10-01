"""Saved-record A/B summaries, only after the batch seal and verified archive.

No ecological evolution, controller, birth, selection score or P reconstruction.
"""
import csv
import io
from types import SimpleNamespace
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
from loom_developmental import codec,evidence
from loom_developmental.runner import canonical,file_hash,atomic_json

def plain(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [plain(v) for v in x]
    return x

def analysis_storage_guard(additional):
    used=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())
    if used+additional>2_480_000_000:raise RuntimeError('Derived analysis storage reserve reached')

def save(name,value):
    value=plain(value);analysis_storage_guard(len(canonical(value)))
    atomic_json(OUT/name,value)

def csv_out(name,rows):
    if not rows:return
    buffer=io.StringIO(newline='')
    w=csv.DictWriter(buffer,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    data=buffer.getvalue().encode('utf8');analysis_storage_guard(len(data))
    with (OUT/name).open('xb') as f:f.write(data)

def norm(x):return float(np.linalg.norm(x))

def checkpoint_row(e,initial,cp):
    o=e.organism;a=o.association;r=o.regulator
    row=dict(index=e.native_index,time=e.time,wave=o.wave_count,checkpoint_file=cp['file'],checkpoint_sha256=cp['sha256'])
    for m,(x,b) in enumerate(zip(o.cortices,initial.organism.cortices)):
        for k in ('shared','fine','shared_ref','fine_ref'):
            row[f'c{m}_{k}_norm']=norm(getattr(x,k));row[f'c{m}_{k}_birth_delta']=norm(getattr(x,k)-getattr(b,k))
        row[f'c{m}_shared_reference_separation']=norm(x.shared-x.shared_ref)
        row[f'c{m}_fine_reference_separation']=norm(x.fine-x.fine_ref)
        row[f'c{m}_activity_norm']=norm(x.x);row[f'c{m}_coactivity_norm']=norm(x.C)
        row[f'c{m}_opening_mean']=float(x.opening.mean())
    row.update(H_norm=float(np.sqrt(sum(norm(h)**2 for h in a.H.values()))),
        H_use_mean=float(np.concatenate(list(a.use.values())).mean()),H_write_count=a.write_count,q_norm=norm(a.q),
        theta_E_norm=norm(r.theta[0]),theta_I_norm=norm(r.theta[1]),
        reference_E_norm=norm(r.reference[0]),reference_I_norm=norm(r.reference[1]),
        eligibility_E_norm=norm(r.eligibility[0]),eligibility_I_norm=norm(r.eligibility[1]))
    updates=a.diagnostic.get('map_updates',{})
    for k in ('write_norm','decay_norm','projection_norm'):
        row['last_wave_H_'+k]=float(sum(np.sum(x[k]) for x in updates.values())) if updates else 0.
    row['last_wave_learning_norm']=norm(r.credit_diagnostic['learning']) if r.credit_diagnostic else 0.
    row['last_wave_reference_force_norm']=norm(r.credit_diagnostic['reference_force']) if r.credit_diagnostic else 0.
    return row

def intervals(mask,times,indices):
    padded=np.r_[False,mask,False];start=np.flatnonzero(padded[1:] & ~padded[:-1]);end=np.flatnonzero(~padded[1:] & padded[:-1])-1
    return [dict(first_native=int(indices[a]),last_native=int(indices[b]),first_endpoint=float(times[a]),last_endpoint=float(times[b])) for a,b in zip(start,end)]

def analyse_life(row):
    name=row['life_id'];base=HERE if int(name[3:])>=13 else ROOT/'founder_initial_execution_20260930';store=base/'lives'/name
    incomplete=not row.get('complete')
    if incomplete:
        custody=json.loads((HERE/'INTERRUPTION_CUSTODY_SEAL.json').read_bytes())
        assert name=='FS-060'
        refs=custody['files'];cps0=sorted((f for f in refs if f['file'].startswith('checkpoint-')),key=lambda f:f['file'])
        r={'initial_checkpoint':next(f for f in cps0 if f['file'].endswith('-initial.ld')),
           'final_checkpoint':cps0[-1],'checkpoints':cps0,
           'chunks':sorted((f for f in refs if f['file'].startswith('chunk-')),key=lambda f:f['file'])}
    else:r=json.loads((store/'segment-000.json').read_bytes())
    initial=codec.read(store/r['initial_checkpoint']['file'],r['initial_checkpoint']['sha256'])['engine']
    final=codec.read(store/r['final_checkpoint']['file'],r['final_checkpoint']['sha256'])['engine']
    if incomplete:
        last=codec.read(store/r['chunks'][-1]['file'],r['chunks'][-1]['sha256'])['native'][-1];sl=evidence.SLICES
        # A recorded physical endpoint view only: no Engine, P state, new
        # receipt, biological-endpoint claim or resumption capability is made.
        final=SimpleNamespace(body=SimpleNamespace(position=last[sl['position']],energy=float(last[sl['reserves']][0]),integrity=float(last[sl['reserves']][1])),
            stocks=last[sl['stocks']],time=float(last[0]),terminal_dimension=None)
    native=[];waves=[];episodes=[];open_episodes={};total_events=0
    transfer=np.zeros(8);renewal=np.zeros(8);damage=repair=expense=impulses=0.;impact_count=release_count=0
    mover_impulse=0.;source_contact_duration=0.;contact_native=set();productive_native=set();mover_native=set()
    event_first_transfer=None;event_last_transfer=None;consequences=[]
    def close_episode(key):
        if key in open_episodes:episodes.append(open_episodes.pop(key))
    for chunk in r['chunks']:
        guard()
        data=codec.read(store/chunk['file'],chunk['sha256']);native.append(data['native']);waves.extend(data['waves']);offset=0
        for index,n in enumerate(data['native'],data['first_index']):
            count=int(n[evidence.SLICES['event_count']][0])
            for ev in data['events'][offset:offset+count]:
                total_events+=1;dt=float(ev['duration']);t=float(ev['time']);cs=ev['contacts']
                active={c['collider'] for c in cs}
                if dt>0:
                    for key in list(open_episodes):
                        if key not in active:close_episode(key)
                if ev.get('event_kind')=='release':
                    release_count+=1
                    for key in ev['colliders']:close_episode(key)
                for c in cs:
                    key=c['collider'];imp=float(c['impulse']);impulses+=imp;contact_native.add(index)
                    if key=='mover':mover_impulse+=imp;mover_native.add(index)
                    if key not in open_episodes:
                        open_episodes[key]=dict(life_id=name,collider=key,source=c.get('source'),
                            first_native=index,last_native=index,first_event=total_events,last_event=total_events,
                            start_time=t-dt,end_time=t,contact_duration=0.,impulse=0.,transfer=0.,event_count=0)
                    ep=open_episodes[key];ep.update(last_native=index,last_event=total_events,end_time=t)
                    ep['contact_duration']+=dt;ep['impulse']+=imp;ep['event_count']+=1
                    if 'source' in c:ep['transfer']+=float(ev['transfer'][c['source']])
                if any('source' in c for c in cs):source_contact_duration+=dt
                v=np.asarray(ev['transfer']);transfer+=v
                renewal+=np.asarray(ev['renewal_first'])+ev['renewal_second']
                damage+=ev['damage'];repair+=ev['repair'];expense+=ev['expenditure']
                if np.any(v>0) or ev['repair']>0 or ev['damage']>0:
                    consequences.append(dict(native_index=index,event_index=total_events,event=plain(ev)))
                if ev['impact'] and cs:impact_count+=1
                if np.any(v>0):
                    productive_native.add(index)
                    loc=dict(native_index=index,event_index=total_events,time=t,source_indices=np.flatnonzero(v>0).tolist())
                    if event_first_transfer is None:event_first_transfer=loc
                    event_last_transfer=loc
            offset+=count
        assert offset==len(data['events'])
    for key in list(open_episodes):close_episode(key)
    rows=np.vstack(native);s=evidence.SLICES;t=rows[:,s['time']].ravel();indices=np.arange(1,len(rows)+1)
    pos=rows[:,s['position']];res=rows[:,s['reserves']];raw=rows[:,s['raw']]
    gaps=np.linalg.norm(pos[:,None,:]-np.asarray(initial.c.source_positions)[None,:,:],axis=2)-initial.c.body_radius-initial.c.source_radius
    rect=rows[:,s['mover_rectangle']];closest=np.column_stack((np.clip(pos[:,0],rect[:,0],rect[:,1]),np.clip(pos[:,1],rect[:,2],rect[:,3])))
    mover_clearance=np.linalg.norm(pos-closest,axis=1)-initial.c.body_radius
    near=[]
    for source in range(8):
        for threshold in (.25,1.):
            for x in intervals(gaps[:,source]<=threshold,t,indices):near.append(dict(life_id=name,source=source,surface_gap_threshold=threshold,**x))
    min_at=np.argmin(gaps,axis=0);min_mover=int(np.argmin(mover_clearance))
    result=dict(**row,terminal_dimension=final.terminal_dimension,all_events=total_events,
        energy_start=initial.body.energy,energy_final=final.body.energy,integrity_start=initial.body.integrity,integrity_final=final.body.integrity,
        expenditure=expense,transfer_total=float(transfer.sum()),transfer_by_source=transfer.tolist(),
        renewal_total=float(renewal.sum()),renewal_by_source=renewal.tolist(),final_stocks=final.stocks.tolist(),
        minimum_recorded_stock_by_source=rows[:,s['stocks']].min(axis=0).tolist(),
        damage=damage,repair=repair,impulse_total=impulses,impact_event_count=impact_count,release_event_count=release_count,
        contact_native_count=len(contact_native),productive_native_count=len(productive_native),
        source_contact_duration=source_contact_duration,source_contact_episodes=sum(e['source'] is not None for e in episodes),
        productive_source_episodes=sum(e['source'] is not None and e['transfer']>0 for e in episodes),
        source_ids_contacted=sorted({e['source'] for e in episodes if e['source'] is not None}),
        first_transfer=event_first_transfer,last_transfer=event_last_transfer,
        mover_contact_native_count=len(mover_native),mover_impulse=mover_impulse,
        minimum_mover_endpoint_clearance=float(mover_clearance[min_mover]),minimum_mover_clearance_native=min_mover+1,
        path_length=float(np.linalg.norm(np.diff(np.vstack((initial.body.position,pos)),axis=0),axis=1).sum()),
        displacement=float(np.linalg.norm(final.body.position-initial.body.position)),
        min_source_endpoint_gap=gaps.min(axis=0).tolist(),min_source_gap_native=(min_at+1).tolist(),
        raw_min=raw.min(axis=0).tolist(),raw_max=raw.max(axis=0).tolist(),
        ledger_residual_energy=float(final.body.energy-initial.body.energy-(transfer.sum()-expense)),
        ledger_residual_integrity=float(final.body.integrity-initial.body.integrity-(repair-damage)),
        ledger_residual_stock_max=float(np.max(np.abs(final.stocks-initial.stocks-renewal+transfer))))
    wave_rows=[]
    for w in waves:
        z=w['map_update_use'];wr=dict(life_id=name,native_index=w['index'],wave=w['wave'],time=w['index']*.01,
            H_norm=norm(z[:,:4]),H_use_mean=float(z[:,4:].mean()),q_norm=norm(w['q']),
            q_motor_norm=norm(w['q'][initial.c.slices[6]]),psi_norm=norm(w['psi']),
            learned_E_norm=norm(w['learned'][0]),learned_I_norm=norm(w['learned'][1]),
            exploration_E_norm=norm(w['exploration'][0]),exploration_I_norm=norm(w['exploration'][1]),
            credit_E=float(w['credit_trend'][0]),credit_I=float(w['credit_trend'][1]),
            theta_E_norm=float(w['regulator_bank_norm'][0]),theta_I_norm=float(w['regulator_bank_norm'][1]),
            opening_mean=float(w['pool_opening'].mean()),support_mean=float(w['controls'][:initial.c.group_count].mean()))
        for m in range(4):wr[f'c{m}_shared_norm']=float(w['sensory_shared_norm'][m]);wr[f'c{m}_fine_norm']=float(w['sensory_fine_norm'][m])
        wave_rows.append(wr)
    cps=[checkpoint_row(codec.read(store/cp['file'],cp['sha256'])['engine'],initial,cp) for cp in r['checkpoints']]
    result['B_initial']=cps[0];result['B_final']=cps[-1]
    result['incomplete_prefix_only']=incomplete
    result['physical_endpoint_meaning']='last durable native endpoint; actual stopped state unknown' if incomplete else 'runner closed endpoint'
    result['B_final_meaning']='last available complete checkpoint; see its index/time, not the prefix endpoint' if incomplete else 'runner final checkpoint'
    result['max_excursion_from_birth']=float(np.linalg.norm(pos-initial.body.position,axis=1).max())
    result['spatial_extent_min']=pos.min(axis=0).tolist();result['spatial_extent_max']=pos.max(axis=0).tolist()
    result['coverage_1_unit_bins']=len(np.unique(np.floor(pos).astype(int),axis=0))
    result['coverage_bin_size_world_units']=1.
    result['first_source_contact']=next((x for x in sorted(episodes,key=lambda x:x['first_event']) if x['source'] is not None),None)
    result['beyond_initial_min_death_age']=final.time>429.2193066502889
    result['beyond_initial_max_death_age']=final.time>429.94828824435905
    result['energy_at_markers']={str(v):(float(res[np.searchsorted(t,v),0]) if t[-1]>=v else None) for v in (429.2193066502889,429.94828824435905)}
    wave_indices=np.array([x['native_index'] for x in wave_rows])
    for ev in consequences:
        k=int(np.searchsorted(wave_indices,ev['native_index'],side='left'))
        ev['prior_handoff']=wave_rows[k-1] if k>0 else None
        ev['next_handoff']=wave_rows[k] if k<len(wave_rows) else None
        ev['alignment']='Prior handoff strictly before event native; next handoff at or after event native. Events precede that native boundary handoff.'
    save(name+'_consequential_events.json',consequences)
    result['consequential_event_count']=len(consequences)
    result['consequential_events_file']=name+'_consequential_events.json'
    result['first_consequential_native']=consequences[0]['native_index'] if consequences else None
    csv_out(name+'_raw_activity.csv',[dict(coordinate=j,minimum=float(raw[:,j].min()),maximum=float(raw[:,j].max()),standard_deviation=float(raw[:,j].std())) for j in range(raw.shape[1])])
    result['wave_summary']={k:dict(min=min(x[k] for x in wave_rows),max=max(x[k] for x in wave_rows),mean=float(np.mean([x[k] for x in wave_rows]))) for k in wave_rows[0] if k not in ('life_id','native_index','wave','time')} if wave_rows else {}
    csv_out(name+'_contact_episodes.csv',episodes);csv_out(name+'_near_source_intervals.csv',near)
    csv_out(name+'_waves.csv',wave_rows);csv_out(name+'_checkpoints.csv',cps)
    # Only saved physical paths/reserves; decimated for passive report display.
    display_indices=np.unique(np.r_[0,np.arange(0,len(rows),100),len(rows)-1]).astype(int)
    save(name+'_display.json',dict(life_id=name,initial_position=initial.body.position,initial_angle=initial.body.angle,
        body_radius=initial.c.body_radius,source_radius=initial.c.source_radius,source_positions=initial.c.source_positions,
        repair_rectangles=initial.c.repair_rectangles,world_side=initial.c.world_side,
        indices=display_indices+1,time=t[display_indices],position=pos[display_indices],angle=rows[display_indices,s['angle']].ravel(),
        reserves=res[display_indices],mover_rectangle=rect[display_indices],
        recording_stride_native=100,display_only_no_new_trajectory=True))
    save(name+'_AB.json',result)
    return result

def guard():
    start=json.loads((OUT/'ANALYSIS_CLOCK.json').read_bytes())['monotonic_started']
    if time.perf_counter()-start>=4500:raise RuntimeError('Passive analysis allowance exhausted')

def main():
    archive=json.loads((HERE/'ARCHIVE_VERIFICATION.json').read_bytes())
    verification=json.loads((HERE/'POSTRUN_VERIFICATION.json').read_bytes())
    assert verification['all_available_complete_stores_verified']
    seal=json.loads((HERE/'COMBINED_DENOMINATOR_SEALED.json').read_bytes())
    OUT.mkdir(exist_ok=False)
    save('ANALYSIS_CLOCK.json',dict(monotonic_started=time.perf_counter(),budget_seconds=4500,budget_bytes=2500000000,
        archive_sha256=archive['sha256'],definition='Active analysis script wall time plus any subsequent analysis work; pause accounting recorded separately if review separates invocations.'))
    summaries=[]
    for row in seal['roster']:
        guard()
        if row.get('complete') or row.get('native_steps',0)>0:r=analyse_life(row)
        else:r=dict(row,analysis='No complete verified trajectory; retained in denominator')
        summaries.append(r);print(json.dumps(dict(life_id=row['life_id'],AB_complete=True)),flush=True)
    save('ALL_SIXTY_AB.json',summaries)
    fields=['life_id','state','simulated_seconds','native_steps','waves','terminal_dimension','energy_start','energy_final','integrity_final',
        'transfer_total','expenditure','damage','repair','path_length','source_contact_episodes','productive_source_episodes','mover_contact_native_count','max_excursion_from_birth','coverage_1_unit_bins','beyond_initial_min_death_age','beyond_initial_max_death_age','primary_bytes']
    csv_out('FULL_DENOMINATOR_A.csv',[{k:r.get(k) for k in fields} for r in summaries])
    bfields=['H_norm','H_use_mean','H_write_count','q_norm','theta_E_norm','theta_I_norm','reference_E_norm','reference_I_norm','eligibility_E_norm','eligibility_I_norm']
    csv_out('FULL_DENOMINATOR_B.csv',[dict(life_id=r['life_id'],**{k:r.get('B_final',{}).get(k) for k in bfields}) for r in summaries])
    clock=json.loads((OUT/'ANALYSIS_CLOCK.json').read_bytes())
    save('AB_COMPLETION.json',dict(complete_roster=60,wall_seconds=time.perf_counter()-clock['monotonic_started'],
        bytes=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()),
        ecological_steps=0,P_reconstructions=0,D5_windows=0,selection_scores=0,
        limitations=['Proximity is geometric endpoint exposure, not proof of a navigable opportunity.',
            'Contact episodes count nonzero constraint/contact records, separated by positive-time no-contact or explicit release.',
            'H formation/decay/projection and cortical/reference operands at saved checkpoints are last-wave samples, not integrated totals.',
            'Norm changes and read/use are not evidence of beneficial learning.']))

if __name__=='__main__':main()
