from common import *
def f(r,k):return float(r[k]) if r.get(k,'')!='' else None
def main():
    b=readcsv('tables/BEHAVIOURAL_AGE_BANDS.csv');sb=readcsv('tables/SOURCE_BOUTS.csv');nr=readcsv('tables/SOURCE_NEIGHBORHOOD_RETURNS.csv');ap=readcsv('tables/HAZARD_APPROACHES.csv');cp=readcsv('tables/CONTEXT_PAIRS.csv');cc=readcsv('tables/CONDITIONAL_ACTION_CONSISTENCY.csv')
    summaries=[];biographies=[];dash=[];functional=[]
    for n in range(1,13):
        life=f'RS-M1-{n:03d}';events=json.loads((OUT/'cache'/(life+'_EVENTS.json')).read_bytes());ss=[r for r in sb if r['life']==life];neigh=[r for r in nr if r['life']==life];rep=events['repair_bouts'];sourceids=[];different_returns=0
        for r in ss:
            s=r['source']
            if sourceids and s!=sourceids[-1] and s in sourceids:different_returns+=1
            sourceids.append(s)
        repair_op=[r for r in ap if r['life']==life and r['family']=='repair' and r['censored']=='False' and f(r,'I')<1-1e-8]
        departures=[r for r in neigh if r['censored']=='False'];returned=[r for r in neigh if r['return_visit']=='True'];consequential=[r for r in returned if r['previous_consequence']=='True']
        summaries.append(dict(life=life,source_bouts=len(ss),distinct_sources=len(set(sourceids)),true_same_source_revisits=sum(r['true_departure_revisit']=='True' for r in ss),switchback_to_previously_visited_source=different_returns,source_neighborhood_departures=len(departures),subsequent_neighborhood_returns=len(returned),descriptive_return_fraction=div(len(returned),len(departures)),consequential_neighborhood_returns=len(consequential),right_censored_final_neighborhood_visits=sum(r['censored']=='True' for r in neigh),repair_contact_bouts=len(rep),repair_surface_ids=len(set(r['collider'] for r in rep)),repair_repeat_contacts=max(0,len(rep)-len(set(r['collider'] for r in rep))),damaged_state_repair_approaches=len(repair_op),repair_contact_given_approach=div(sum(r['contact']=='True' for r in repair_op),len(repair_op)),repair_gain_given_approach=div(sum(f(r,'repair')>0 for r in repair_op),len(repair_op)),physical_repair=details(life)['physical']['repair']))
        good=max(events['source_bouts'],key=lambda r:r['transfer'],default=None);bad=max(events['all_contact_bouts'],key=lambda r:r['damage'],default=None)
        row=dict(life=life,selection='largest total-transfer source bout and largest total-damage contact bout; descriptive selection, not a hypothesis test')
        for label,event in [('productive',good),('adverse',bad)]:
            for k in ('start','end','collider','duration','transfer','damage','peak_impulse','peak_sustained_force'):row[label+'_'+k]=event[k] if event else None
        biographies.append(row)
        F=np.load(OUT/'series'/(life+'_FUNCTIONAL.npz'));cut=record(life)['curve_cutoff']
        for label,lo,hi in [('early',0,min(1000,cut/3)),('late',max(0,cut-min(1000,cut/3)),cut)]:
            m=(F['age']>lo)&(F['age']<=hi);rr=dict(life=life,band=label,start=lo,end=hi)
            for bank in ('E','I'):
                rr[bank+'_current_RMS']=rms(F[bank+'_current_effect'][m]);rr[bank+'_command_RMS']=rms(F[bank+'_command_effect'][m]);rr[bank+'_full_receiver_RMS']=rms(F[bank+'_full_receiver_effect'][m]);rr[bank+'_command_over_M1_input']=div(rr[bank+'_command_RMS'],rms(F['M1_RMS'][m]));rr[bank+'_command_over_M1_same_receiver']=div(rr[bank+'_command_RMS'],rms(F['M1_command_effect'][m]))
            for k in ('q_norm','H_use_mean','theta_E_norm','theta_I_norm','H_norm','direct_feedback_RMS','regulator_current_RMS','command_RMS','attenuation_mean','associative_motor_command_effect'):rr[k+'_mean']=mean(F[k][m])
            functional.append(rr)
        my=[r for r in b if r['life']==life]
        if n<=7:
            for j,r in enumerate(my):
                p=my[j-1] if j else None
                direction=lambda key,good: 'unresolved: first-band reference' if p is None else ('no opportunity' if f(r,key) is None or f(p,key) is None else ('improving descriptively' if (f(r,key)-f(p,key))*good>0 else ('worsening descriptively' if (f(r,key)-f(p,key))*good<0 else 'unchanged')))
                dash.append(dict(life=life,start=r['start'],end=r['end'],damage_per_path=direction('damage_per_path',-1),collision_given_approach=direction('collision_given_approach',-1),productive_bouts_per_path=direction('productive_bouts_per_path',1),productive_given_source_approach=direction('source_approach_productive_fraction',1),source_dwell=direction('mean_source_contact_duration',1),repair='no opportunity' if not any(f(rp,'start')>f(r,'start') and f(rp,'start')<=f(r,'end') for rp in repair_op) else 'unresolved: opportunity present; accidental contact possible',spatial='mixed/unresolved: novelty and recurrence are descriptive; neither has a universal preferred sign',causal_development='unresolved for every cell; signs compare the previous unequal-duration band and are not skill scores'))
    table('tables/RETURN_AND_REPAIR_OPPORTUNITIES.csv',summaries);table('tables/SELECTED_BIOGRAPHICAL_EVENTS.csv',biographies);table('tables/AGE_BAND_STATUS_ANNOTATIONS.csv',dash);table('tables/FUNCTIONAL_SCALE_COMPARISON.csv',functional)
    consistency=[]
    for kind in ('generic_contact_free','chemical_imbalance','low_E','rising_chemistry'):
        for k in (3,5):
            rr=[r for r in cc if int(r['life'][-3:])<=7 and r['kind']==kind and int(r['k'])==k];paired=[r for r in rr if r['paired_dispersion_available']=='True'];row=dict(kind=kind,k=k,declared_eligible_anchors=len(rr),matched_both_early_and_late=len(paired),lives=len(set(r['life'] for r in paired)))
            for key in ('action_dispersion','mean_common','mean_differential','mean_omega','collision_fraction','productive_fraction'):
                for age in ('early','late'):row[age+'_'+key]=mean([f(r,age+'_'+key) for r in paired])
            consistency.append(row)
    table('tables/CONDITIONAL_CONSISTENCY_SUMMARY.csv',consistency)
    detailed=[]
    for kind in sorted(set(r['kind'] for r in cp)):
        for subset in ('all','both_hazard','both_source_near','outside_support_followup'):
            rr=[r for r in cp if int(r['life'][-3:])<=7 and r['kind']==kind]
            if subset=='both_hazard':rr=[r for r in rr if r['early_hazard_opportunity']==r['later_hazard_opportunity']=='True']
            if subset=='both_source_near':rr=[r for r in rr if f(r,'early_source_gap')<=1 and f(r,'later_source_gap')<=1]
            if subset=='outside_support_followup':rr=[r for r in rr if r['early_support_within_outcome']==r['later_support_within_outcome']=='False']
            qids=set(r['query'] for r in rr);row=dict(kind=kind,subset=subset,queries=len(qids),pairs=len(rr))
            for key in ('closing_speed_proxy','turn_toward_outward_normal','forward_drive_change','time_to_separation','damage','source_distance_reduction','mean_command_left','mean_command_right','mean_omega_next1','command_variance_next10','heading_persistence_10'):
                keep=[r for r in rr if r['early_'+key]!='' and r['later_'+key]!=''];ids=set(r['query'] for r in keep);row[key+'_paired_queries']=len(ids)
                for age in ('early','later'):row[age+'_'+key]=mean([mean([f(r,age+'_'+key) for r in keep if r['query']==q]) for q in ids])
            row['separation_censored_pair_fraction']=div(sum(r['early_separation_censored']=='True' or r['later_separation_censored']=='True' for r in rr),len(rr));detailed.append(row)
    table('tables/CONTEXT_EXTENDED_OUTCOMES.csv',detailed)
    print('Interpretation tables, capability opportunities and biographies complete.')
if __name__=='__main__':main()

