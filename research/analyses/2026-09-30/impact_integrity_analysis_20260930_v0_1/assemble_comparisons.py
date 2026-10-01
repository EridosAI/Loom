"""Descriptive saved-record comparisons. No reconstruction or physical stepping."""
import csv,json,math
import numpy as np
from impact_analysis import HERE,PREV,read,write,table,norm,initial,gap_series,path_at

def main():
    audit=read(HERE/'DAMAGED_LIFE_AUDIT.json');probes=read(HERE/'PASSIVE_LEARNED_I_OMISSIONS.json')
    roster=read(PREV/'analysis/ALL_SIXTY_AB.json');summaries=[];enriched=[];comparisons=[];halves=[];comps=[];eventsumm=[];snapshots=[]
    wavecache={}
    def wavefile(name):
        if name not in wavecache:
            with (PREV/'analysis'/(name+'_waves.csv')).open() as f:wavecache[name]={int(r['native_index']):r for r in csv.DictReader(f)}
        return wavecache[name]
    for name in audit['damaged_lives']:
        ep=read(HERE/(name+'_EPISODES.json'));raw=read(HERE/(name+'_CONTACT_RECORDS.json'))
        phys=read(HERE/(name+'_PHYSICAL_SUMMARY.json'));data=dict(np.load(HERE/(name+'_RECORDED_NATIVE.npz')));e=initial(name)
        with (HERE/(name+'_I_WAVES.csv')).open() as f:wave={int(z['native_index']):{k:(v if k=='life_id' else float(v)) for k,v in z.items()} for z in csv.DictReader(f)}
        firstcredit=next(z for z in wave.values() if z['I_trend']!=0);lastcredit=list(wave.values())[-1]
        ps=[p for p in probes if p['life_id']==name];blocks=[p for p in ps if p['kind']=='fixed_ageblock_closest']
        summary=dict(life_id=name,episodes=len(ep),bouts=phys['bouts'],grouping_sensitivity=phys['grouping_sensitivity'],
            total_damage=phys['damage'],first_damage=phys['first_damage'],first_I_trend=firstcredit['I_trend'],
            first_credit_time=firstcredit['time'],first_I_eligibility_norm=firstcredit['eligibility_norm'],
            first_I_bank_norm=firstcredit['I_bank_after_norm'],final_I_bank_norm=lastcredit['I_bank_after_norm'],
            final_I_reference_norm=lastcredit['I_reference_after_norm'],final_learned_I_output_norm=lastcredit['learned_I_norm'],
            maximum_local_command_difference=max(p['maximum_command_delta_norm'] for p in ps),
            ageblock_less_into_count=sum(p['learned_I_into_force_delta_mean']<0 for p in blocks),
            ageblock_more_into_count=sum(p['learned_I_into_force_delta_mean']>0 for p in blocks),
            ageblock_zero_count=sum(p['learned_I_into_force_delta_mean']==0 for p in blocks),
            windows=len(ps),uncertain_contact_velocities=phys['validation']['uncertain_contact_velocity_rows'])
        summaries.append(summary)
        for z in ep:
            contact=[r for r in raw if r['collider']==z['collider'] and z['first_event']<=r['event_index']<=z['last_event']]
            instant=[r for r in contact if r['instant'] and r['closing_normal_velocity'] is not None]
            z['peak_instant_closing_velocity']=max((r['closing_normal_velocity'] for r in instant),default=None)
            z['pre_0_2s_left_force_gain']=.5*(.2+.8*z['pre_0_2s_energy'])*(.4+.6*z['pre_0_2s_integrity'])
            z['pre_0_2s_right_force_gain']=.5*(.2+.8*z['pre_0_2s_energy'])*(.7+.3*z['pre_0_2s_integrity'])
            p=next(p for p in ps if p['kind']=='episode' and p['related_episode']==z['episode'])
            for k in ('command_delta_mean','learned_I_into_force_delta_mean','attenuation_delta_mean','maximum_command_delta_norm'):
                z[k]=p[k]
            damaging=next((r for r in contact if r['damage']>0),None)
            k=int(math.ceil(damaging['native_index']/20))*20 if damaging else None
            w=wave.get(k);before=wave.get(k-20) if k else None
            eventsummary=dict(life_id=name,episode=z['episode'],collider=z['collider'],onset=z['onset'],
                first_damage_event_time=damaging['end'] if damaging else None,
                integrity_before=damaging['event_integrity_before'] if damaging else None,
                integrity_after=damaging['event_integrity_after'] if damaging else None,
                next_credit_native=k)
            if w:eventsummary.update({'next_'+key:value for key,value in w.items() if key not in ('life_id','native_index')})
            if before:eventsummary.update(prior_I_trend=before['I_trend'],prior_I_bank_norm=before['I_bank_after_norm'])
            eventsumm.append(eventsummary);enriched.append(z)
        for key in sorted({z['collider'] for z in ep}):
            seq=[z for z in ep if z['collider']==key];first=seq[0]
            for later in seq[1:]:
                z=dict(life_id=name,collider=key,first_episode=first['episode'],later_episode=later['episode'],
                    first_onset=first['onset'],later_onset=later['onset'],separation_to_previous=later['onset']-seq[seq.index(later)-1]['end'])
                for k in ('onset_closing_velocity','peak_instant_closing_velocity','instant_impulse_peak','impulse','damage',
                    'sustained_force_peak','sustained_force_time_mean','contact_duration','pre_0_2s_energy','pre_0_2s_integrity',
                    'pre_0_2s_left_force_gain','pre_0_2s_right_force_gain'):
                    z['first_'+k]=first[k];z['later_'+k]=later[k]
                    z['difference_'+k]=later[k]-first[k] if first[k] is not None and later[k] is not None else None
                z['first_commands']=first['onset_commands'];z['later_commands']=later['onset_commands']
                z['later_learned_I_into_force_delta']=later['learned_I_into_force_delta_mean'];comparisons.append(z)
            start=phys['first_damage'];end=float(data['time'][-1,0]);mid=(start+end)/2
            gaps,_=gap_series(e,key,data)
            for label,lo,hi in [('early_post_injury_half',start,mid),('late_post_injury_half',mid,end)]:
                mask=(data['time'][:,0]>=lo)&(data['time'][:,0]<hi);events=[r for r in raw if r['collider']==key and lo<=r['end']<hi]
                count=sum(lo<=z['onset']<hi for z in seq);path=path_at(data,hi)-path_at(data,lo)
                halves.append(dict(life_id=name,collider=key,period=label,start=lo,end=hi,duration=hi-lo,
                    behavioral_onsets=count,onsets_per_second=count/(hi-lo),native_path=path,onsets_per_path=count/path if path else None,
                    damage=sum(r['damage'] for r in events),impulse=sum(r['impulse'] for r in events),
                    contact_seconds=sum(r['duration'] for r in events),minimum_clearance=float(gaps[mask].min()),
                    maximum_clearance=float(gaps[mask].max()),mean_clearance=float(gaps[mask].mean()),
                    time_within_0_25=float(data['elapsed'][mask,0][gaps[mask]<=.25].sum())))
        # Actual sampled positions following first injury: no extrapolation or held-body trajectory.
        for offset in (-.2,0,.2,1,5,30,60,120):
            t=max(0.,phys['first_damage']+offset);j=min(int(np.searchsorted(data['time'][:,0],t)),len(data['time'])-1)
            snapshots.append(dict(life_id=name,offset_from_first_injury=offset,requested_time=t,recorded_time=float(data['time'][j,0]),
                native_index=j+1,position=data['position'][j],orientation=float(data['angle'][j,0]),velocity=data['velocity'][j],
                omega=float(data['omega'][j,0]),commands=data['commands'][j],reserves=data['reserves'][j],mover_rectangle=data['mover_rectangle'][j]))
        for p in ps:
            k=(p['last_native']//20)*20
            candidates=[r for r in roster if r['complete'] and r['damage']==0 and r['waves']*20>=k]
            comparison=candidates[0]['life_id'] if candidates else None
            z=dict(life_id=name,window=p['name'],native_index=k,comparison_life=comparison,
                selection='earliest eligible complete no-damage roster entry at identical wave age',
                causal_isolation=False,geometry_opportunity_matched=False)
            actual=wavefile(name).get(k);control=wavefile(comparison).get(k) if comparison else None
            for key in ('credit_I','theta_I_norm','learned_I_norm','exploration_I_norm'):
                z['actual_'+key]=float(actual[key]) if actual else None;z['comparison_'+key]=float(control[key]) if control else None
            comps.append(z)
    write('PER_LIFE_SUMMARY.json',summaries);table('PER_LIFE_SUMMARY.csv',summaries)
    write('BEHAVIORAL_EPISODES_ENRICHED.json',enriched);table('BEHAVIORAL_EPISODES_ENRICHED.csv',enriched)
    table('WITHIN_LIFE_EARLY_TO_LATE.csv',comparisons);write('WITHIN_LIFE_EARLY_TO_LATE.json',comparisons)
    table('POST_INJURY_HALF_EXPOSURE.csv',halves);write('POST_INJURY_HALF_EXPOSURE.json',halves)
    table('NO_DAMAGE_AGE_MATCHED_COMPARISONS.csv',comps)
    table('EPISODE_I_CHAIN_SUMMARY.csv',eventsumm);write('EPISODE_I_CHAIN_SUMMARY.json',eventsumm)
    table('ACTUAL_POST_INJURY_SNAPSHOTS.csv',snapshots);write('ACTUAL_POST_INJURY_SNAPSHOTS.json',snapshots)
    write('COMPARISON_COMPLETION.json',dict(lives=len(summaries),episodes=len(enriched),first_to_later_pairs=len(comparisons),
        no_damage_comparisons=len(comps),new_world_steps=0,new_P_reconstructions=0,
        no_damage_I_bank_always_zero=all(z['comparison_theta_I_norm']==0 for z in comps if z['comparison_theta_I_norm'] is not None)))
    print(json.dumps(dict(episodes=len(enriched),comparison_pairs=len(comparisons),no_damage_comparisons=len(comps))))

if __name__=='__main__':main()
