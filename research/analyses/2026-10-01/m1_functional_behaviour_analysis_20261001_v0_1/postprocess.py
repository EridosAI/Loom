from common import *
from scipy.stats import theilslopes
def num(r,k):return float(r[k]) if r.get(k,'')!='' else None
def main():
    b=readcsv('tables/BEHAVIOURAL_AGE_BANDS.csv');ap=readcsv('tables/HAZARD_APPROACHES.csv');sb=readcsv('tables/SOURCE_BOUTS.csv');ints=readcsv('tables/RESURRECTION_INTERVALS.csv');cp=readcsv('tables/CONTEXT_PAIRS.csv');queries=readcsv('tables/CONTEXT_QUERIES.csv');sens=readcsv('tables/CONTEXT_SENSITIVITY.csv');ws=readcsv('tables/BEHAVIOURAL_60S.csv')
    aggregate=[]
    for lo,hi in BANDS:
        rr=[r for r in b if int(r['life'][-3:])<=7 and num(r,'start')==lo];total=lambda k:sum(num(r,k) or 0 for r in rr);path=total('path');sec=total('seconds');ss=[r for r in sb if int(r['life'][-3:])<=7 and lo<num(r,'start')<=hi];op=[r for r in ap if int(r['life'][-3:])<=7 and lo<num(r,'start')<=hi and r['censored']=='False'];sourceop=[r for r in op if r['family']=='source']
        donors=sum(len([v for v in details(f'RS-M1-{n:03d}')['resurrections'] if lo<v['time']<=hi]) for n in range(1,8));source=total('source_energy');damage=total('damage')
        aggregate.append(dict(start=lo,end=hi,lives=7,seconds=sec,path=path,expenditure=total('expenditure'),external_E=.7*donors,resurrections=donors,source_E=source,environment_fraction_of_inputs=div(source,source+.7*donors),environment_fraction_of_expense=div(source,total('expenditure')),damage=damage,damage_per_path=div(damage,path),repair=total('repair'),collision_bouts=total('collision_bouts'),collisions_per_path=div(total('collision_bouts'),path),hazard_approaches=len(op),collision_given_approach=div(sum(r['collision']=='True' for r in op),len(op)),contact_given_approach=div(sum(r['contact']=='True' for r in op),len(op)),source_approaches=len(sourceop),productive_given_source_approach=div(sum(num(r,'transfer')>0 for r in sourceop),len(sourceop)),source_bouts=len(ss),productive_bouts=sum(r['productive']=='True' for r in ss),productive_bouts_per_path=div(sum(r['productive']=='True' for r in ss),path),true_source_revisits=sum(r['true_departure_revisit']=='True' for r in ss),true_revisits_per_path=div(sum(r['true_departure_revisit']=='True' for r in ss),path),mean_bout_dwell=mean([num(r,'duration') for r in ss]),mean_E_per_bout=mean([num(r,'transfer') for r in ss]),source_contact_seconds=total('source_contact_seconds'),energy_per_contact_second=div(source,total('source_contact_seconds')),hazard_exposure=total('hazard_exposure_seconds'),source_exposure=total('source_exposure_seconds'),mean_speed=sum(num(r,'mean_speed')*num(r,'seconds') for r in rr)/sec,pinned_seconds=total('pinned_seconds')))
    table('tables/FIXED_SEVEN_BAND_TOTALS.csv',aggregate)
    # Capability/family standardization within individuals, retaining common support only.
    standardized=[];strata=[]
    for life in [f'RS-M1-{n:03d}' for n in range(1,8)]+['FIXED_SEVEN']:
        rows=[r for r in ap if r['censored']=='False' and (r['life']==life if life!='FIXED_SEVEN' else int(r['life'][-3:])<=7)];early=[r for r in rows if num(r,'start')<=600];late=[r for r in rows if 3500<num(r,'start')<=4500]
        key=lambda r:(r['life'],r['family'],r['E_band'],r['I_band'],r['speed_band'])
        shared=set(map(key,early))&set(map(key,late));pairs=[]
        for k in sorted(shared):
            e=[r for r in early if key(r)==k];l=[r for r in late if key(r)==k];weight=len(e)+len(l);r=dict(comparison=life,stratum='|'.join(k),early_n=len(e),late_n=len(l),weight=weight)
            for metric in ('collision','contact','damage','peak_impulse','entry_closing','min_clearance'):
                get=lambda x:int(x[metric]=='True') if metric in ('collision','contact') else num(x,metric)
                r['early_'+metric]=mean([get(x) for x in e]);r['late_'+metric]=mean([get(x) for x in l])
            strata.append(r);pairs.append(r)
        den=sum(r['weight'] for r in pairs);r=dict(life=life,early_approaches=len(early),late_approaches=len(late),shared_strata=len(shared),early_retained=sum(r['early_n'] for r in pairs),late_retained=sum(r['late_n'] for r in pairs))
        for metric in ('collision','contact','damage','peak_impulse','entry_closing','min_clearance'):
            for label in ('early','late'):r[label+'_'+metric]=div(sum(v['weight']*v[label+'_'+metric] for v in pairs),den)
        standardized.append(r)
    table('tables/CAPABILITY_STANDARDIZED_HAZARD_COMPARISON.csv',standardized);table('tables/CAPABILITY_SHARED_STRATA.csv',strata)
    intervaltrend=[]
    for n in range(1,13):
        life=f'RS-M1-{n:03d}';rr=[r for r in ints if r['life']==life and r['end_cause']=='energy_resurrection'];x=np.array([(num(r,'start')+num(r,'end'))/2 for r in rr]);r=dict(life=life,completed_energy_epochs=len(rr),admin_censored_intervals=sum(v['life']==life and v['end_cause']!='energy_resurrection' for v in ints))
        for k in ('duration','environment_fraction','source_energy_per_path','source_energy_per_time','source_energy'):
            yy=np.array([num(v,k) for v in rr]);r[k+'_first']=float(yy[0]) if len(yy) else None;r[k+'_last']=float(yy[-1]) if len(yy) else None;r[k+'_slope']=float(theilslopes(yy,x)[0]) if len(yy)>2 else None;r[k+'_mean']=mean(yy)
        intervaltrend.append(r)
    table('tables/ENERGY_EPOCH_TRENDS.csv',intervaltrend)
    # Equal-query context summaries, separate from pair weighting.
    context=[];sensitivity=[]
    for kind in sorted(set(r['kind'] for r in queries)):
        qq=[r for r in queries if r['kind']==kind and int(r['life'][-3:])<=7]
        for subset in ('all_main_matches','both_hazard_opportunity','both_source_near'):
            rr=[r for r in cp if r['kind']==kind and int(r['life'][-3:])<=7]
            if subset=='both_hazard_opportunity':rr=[r for r in rr if r['early_hazard_opportunity']=='True' and r['later_hazard_opportunity']=='True']
            if subset=='both_source_near':rr=[r for r in rr if num(r,'early_source_gap')<=1 and num(r,'later_source_gap')<=1]
            ids=sorted(set(r['query'] for r in rr));out=dict(kind=kind,subset=subset,declared_queries=len(qq),eligible_queries=sum(r['eligible']=='True' for r in qq),matched_queries=len(ids),pairs=len(rr))
            for key in ('collision','hazard_opportunity','minimum_clearance','closing_speed_proxy','peak_impulse','damage','source_energy','source_distance_reduction','near_source_at10','forward_drive_change','command_variance_next10','heading_persistence_10'):
                for age in ('early','later'):
                    def value(r):return int(r[age+'_'+key]=='True') if key in ('collision','hazard_opportunity','near_source_at10') else num(r,age+'_'+key)
                    out[age+'_'+key]=mean([mean([value(r) for r in rr if r['query']==qid]) for qid in ids])
            out['different_nearest_source_pairs']=sum(r['early_source_id_observer']!=r['later_source_id_observer'] for r in rr);context.append(out)
        for k in (1,3,5):
            for cap in (.5,1.,2.):
                rr=[r for r in sens if r['kind']==kind and int(r['life'][-3:])<=7 and int(r['k'])==k and num(r,'cap')==cap and int(r['matches'])>0]
                out=dict(kind=kind,k=k,cap=cap,matched_queries=len(rr),pairs=sum(int(r['matches']) for r in rr))
                for field in ('query_collision','later_collision','query_clearance','later_clearance','query_damage','later_damage','query_source_energy','later_source_energy','query_hazard_opportunity','later_hazard_opportunity'):
                    def v(r):return int(r[field]=='True') if r[field] in ('True','False') else num(r,field)
                    out[field]=mean([v(r) for r in rr])
                sensitivity.append(out)
    table('tables/FIXED_SEVEN_CONTEXT_COMPARISON.csv',context);table('tables/FIXED_SEVEN_CONTEXT_SENSITIVITY.csv',sensitivity)
    # Exploratory change points: every declared metric, no significance selection.
    phases=[];links=[]
    metrics=['damage_per_path','collisions_per_path','productive_bouts_per_path','source_energy_per_path','mean_source_contact_duration','revisit_fraction','pinned_seconds','rotation_per_path','command_variance','mean_speed']
    for n in range(1,9):
        life=f'RS-M1-{n:03d}';rows=[r for r in ws if r['life']==life and num(r,'end')-num(r,'start')>=59.999];f=np.load(OUT/'series'/(life+'_FUNCTIONAL.npz'));t=f['age'];series={k:[num(r,k) for r in rows] for k in metrics}
        for k in ('E_command_effect','I_command_effect','q_norm','H_use_mean','theta_E_norm','theta_I_norm','H_norm'):
            series[k]=[mean(f[k][(t>num(r,'start'))&(t<=num(r,'end'))]) for r in rows]
        for k,values in series.items():
            valid=[i for i,v in enumerate(values) if v is not None];y=np.array([values[i] for i in valid]);x=np.array([num(rows[i],'end') for i in valid])
            if len(y)<10:continue
            total=float(np.sum((y-y.mean())**2));cost=[]
            for j in range(5,len(y)-4):cost.append((float(np.sum((y[:j]-y[:j].mean())**2)+np.sum((y[j:]-y[j:].mean())**2)),j))
            score,j=min(cost);phases.append(dict(life=life,metric=k,split_age=float(x[j-1]),valid_windows=len(y),before_mean=float(y[:j].mean()),after_mean=float(y[j:].mean()),SSE_reduction_fraction=div(total-score,total),exploratory_only=True,missing_opportunity_windows=len(rows)-len(y)))
        for neural in ('E_command_effect','I_command_effect','q_norm','H_use_mean'):
            for physical in ('source_energy_per_path','productive_bouts_per_path','damage_per_path','revisit_fraction'):
                x=np.array([np.nan if v is None else v for v in series[neural]]);y=np.array([np.nan if v is None else v for v in series[physical]]);links.append(dict(life=life,internal=neural,behavior=physical,windows=len(x),contemporaneous_correlation=corr(x,y),internal_leading_next_window_correlation=corr(x[:-1],y[1:])))
    table('tables/EXPLORATORY_PHASE_CANDIDATES.csv',phases);table('tables/INTERNAL_BEHAVIOURAL_COVARIATION.csv',links)
    # Intervention margins: observed natural states only, not unsupported counterfactuals.
    confounds=[]
    for n in range(1,8):
        life=f'RS-M1-{n:03d}';o=np.load(OUT/'cache'/(life+'_OBSERVER.npz'));times=o['time'];e=details(life)['resurrections'];rt=np.array([r['time'] for r in e]);distance=np.min(abs(times[:,None]-rt),axis=1);f=np.load(OUT/'series'/(life+'_FUNCTIONAL.npz'));fdistance=np.min(abs(f['age'][:,None]-rt),axis=1)
        for margin in (0,5,30,60):
            for label,lo,hi in [('early',0,600),('late',3500,4500)]:
                m=(times>lo)&(times<=hi)&(distance>margin);fm=(f['age']>lo)&(f['age']<=hi)&(fdistance>margin);row=dict(life=life,margin_seconds=margin,band=label,native_display_samples=int(m.sum()),wave_samples=int(fm.sum()),mean_E=mean(o['reserves'][m,0]),mean_I=mean(o['reserves'][m,1]),mean_speed=mean(o['speed'][m]),command_RMS=rms(o['commands'][m]),E_command_effect_RMS=rms(f['E_command_effect'][fm]),I_command_effect_RMS=rms(f['I_command_effect'][fm]),q_RMS=rms(f['q_norm'][fm]),H_use_mean=mean(f['H_use_mean'][fm]));confounds.append(row)
    table('tables/SUPPORT_MARGIN_SENSITIVITY.csv',confounds)
    # First-class per-life rows retain all additive totals and denominators.
    save('PASSIVE_SUMMARY.json',dict(fixed_seven_bands=aggregate,capability_standardized=standardized,energy_epochs=intervaltrend,contexts=context,scope='Descriptive; no causal inference or mechanism selection',new_simulation_steps=0))
    print('Pooled denominators, matched-support comparisons, support epochs and exploratory phase tables complete.')
if __name__=='__main__':main()
