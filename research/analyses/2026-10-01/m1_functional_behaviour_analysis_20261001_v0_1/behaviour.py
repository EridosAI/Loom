"""Full-native geometry, event and opportunity accounting; no world evolution."""
from common import *

COLLIDERS=[f'wall-{i}' for i in range(4)]+[f'source-{i}' for i in range(8)]+[f'repair-{i}' for i in range(3)]+['mover']
def rectgap(p,r):
    if np.ndim(r)==1:r=np.tile(r,(len(p),1))
    close=np.column_stack((np.clip(p[:,0],r[:,0],r[:,1]),np.clip(p[:,1],r[:,2],r[:,3])));delta=p-close;dist=np.linalg.norm(delta,axis=1)
    inside=dist==0
    g=dist-cfg['body_radius'];g[inside]=-np.min(np.column_stack((p[:,0]-r[:,0],r[:,1]-p[:,0],p[:,1]-r[:,2],r[:,3]-p[:,1]))[inside],axis=1)-cfg['body_radius']
    return g
def geometry(a):
    p=a[:,SL['position']];src=np.linalg.norm(p[:,None,:]-SOURCE[None,:,:],axis=2)-RAD
    g=np.column_stack((p[:,0]-.5,19.5-p[:,0],p[:,1]-.5,19.5-p[:,1],src,*[rectgap(p,r) for r in cfg['repair_rectangles']],rectgap(p,a[:,SL['mover_rectangle']])))
    return g
def paths(a,birth):
    p=np.vstack((birth,a[:,SL['position']]));cum=np.r_[0,np.cumsum(np.linalg.norm(np.diff(p,axis=0),axis=1))];t=np.r_[0,a[:,0]]
    return t,p,cum
def group_episodes(episodes,t,gaps,gapmax=1.,clearmax=.25):
    out=[];last={}
    for e in episodes:
        old=last.get(e['collider']);k=COLLIDERS.index(e['collider']);merge=False
        if old and e['start']-old['end']<=gapmax+1e-8:
            i=np.searchsorted(t,old['end'],side='right');j=np.searchsorted(t,e['start'],side='right')
            clear=float(gaps[i:j,k].max()) if j>i else 0.;merge=clear<=clearmax
        if not merge:
            old={k:e[k] for k in ('collider','start','end','duration','impulse','damage','transfer','repair','first_relative_speed','peak_relative_speed','peak_impulse','peak_sustained_force','start_position','last_position')};old['fragments']=1;out.append(old);last[e['collider']]=old
        else:
            old['end']=e['end'];old['last_position']=e['last_position'];old['fragments']+=1
            for key in ('duration','impulse','damage','transfer','repair'):old[key]+=e[key]
            for key in ('peak_relative_speed','peak_impulse','peak_sustained_force'):old[key]=max(old[key],e[key])
    return sorted(out,key=lambda x:(x['start'],x['collider']))
def approaches(t,g,episodes,impacts,entry=.5,exitgap=1.):
    out=[]
    for k,cid in enumerate(COLLIDERS):
        active=None;starts=[]
        for i in np.flatnonzero((g[:,k]<=entry)&np.r_[True,g[:-1,k]>entry]):
            if active is not None and i<active:continue
            ends=np.flatnonzero(g[i:,k]>exitgap);j=i+ends[0] if len(ends) else len(t)-1;active=j
            born=i==0;prior=max(0,i-10);closing=div(g[prior,k]-g[i,k],t[i]-t[prior]) if i>prior else 0
            genuine=(not born) and closing is not None and closing>.01
            if not genuine:continue
            lo=float(t[i]);hi=float(t[j]);es=[e for e in episodes if e['collider']==cid and e['end']>=lo and e['start']<=hi];im=[x for x in impacts if x['collider']==cid and lo<=x['time']<=hi]
            out.append(dict(collider=cid,start=lo,end=hi,duration=hi-lo,start_index=int(i),end_index=int(j),censored=not len(ends),entry_gap=float(g[i,k]),entry_closing=closing,min_clearance=float(g[i:j+1,k].min()),contact=bool(es),collision=bool(im),damage=sum(e['damage'] for e in es),transfer=sum(e['transfer'] for e in es),repair=sum(e['repair'] for e in es),peak_impulse=max([x['impulse'] for x in im],default=0),contact_duration=sum(max(0,min(hi,e['end'])-max(lo,e['start']))*e['duration']/max(e['end']-e['start'],1e-30) for e in es)))
    return sorted(out,key=lambda x:x['start'])
def main():
    allbands=[];intervals=[];allbouts=[];allapproach=[];sens=[];allimpact=[];repairseq=[];windows=[];summaries=[];allneighborhood=[]
    for n in range(1,13):
        life=f'RS-M1-{n:03d}';a=native(life);d=details(life);rec=record(life);t=a[:,0];dt=a[:,1];age=float(t[-1]);pos=a[:,SL['position']];vel=a[:,SL['velocity']];speed=np.linalg.norm(vel,axis=1);ang=a[:,SL['angle']][:,0];omega=a[:,SL['omega']][:,0];u=a[:,SL['commands']];EI=a[:,SL['reserves']]
        tt,pp,path=paths(a,rec['birth_position']);plen=lambda lo,hi:float(np.interp(hi,tt,path)-np.interp(lo,tt,path));g=geometry(a);near=g[:,4:12].min(axis=1);forward=np.sum(vel*np.column_stack((np.cos(ang),np.sin(ang))),axis=1)
        contact=a[:,SL['contact_rates']].sum(axis=1)>0;immobile=contact&(speed<.005)
        episodes=d['physical']['episodes'];grouped=group_episodes(episodes,t,g);sources=[e for e in grouped if e['collider'].startswith('source')];repairs=[e for e in grouped if e['collider'].startswith('repair')]
        impact=[]
        for r in csv.DictReader((PRIOR/'tables'/(life+'_IMPACTS.csv')).open()):
            impact.append({k:(float(v) if k not in ('life','collider') and v!='' else v) for k,v in r.items()})
        # Group positive instantaneous impacts, preserving exact totals and peaks.
        collisions=[];last={}
        for r in impact:
            old=last.get(r['collider'])
            if old is None or r['time']-old['end']>1:
                old=dict(life=life,collider=r['collider'],start=r['time'],end=r['time'],impulses=0.,peak_impulse=0.,damage=0.,rows=0,first_closing=r['isolated_normal_closing_speed'],peak_closing=0.);collisions.append(old);last[r['collider']]=old
            old['end']=r['time'];old['impulses']+=r['impulse'];old['damage']+=r['damage'];old['rows']+=1;old['peak_impulse']=max(old['peak_impulse'],r['impulse'])
            if r['isolated_normal_closing_speed']!='':old['peak_closing']=max(old['peak_closing'],r['isolated_normal_closing_speed'])
        app=approaches(t,g,episodes,impact)
        for r in app:
            i=r['start_index'];r.update(life=life,E=EI[i,0],I=EI[i,1],speed=speed[i],E_band=int(np.digitize(EI[i,0],[.2,.45])),I_band=int(EI[i,1]>=.9),speed_band=int(np.digitize(speed[i],[.03,.08])),family=r['collider'].split('-')[0]);allapproach.append(r)
        # Fixed geometry sensitivity; no result-dependent threshold choice.
        for en,ex in ((.25,.5),(1.,1.5)):
            ap=approaches(t,g,episodes,impact,en,ex);sens.append(dict(life=life,kind='hazard_approach',entry=en,exit=ex,approaches=len(ap),uncensored=sum(not r['censored'] for r in ap),contact=sum(r['contact'] for r in ap if not r['censored']),collision=sum(r['collision'] for r in ap if not r['censored'])))
        for seconds in (.2,1.,5.):
            for clear in (.05,.25,.5):
                rows=[x for x in group_episodes(episodes,t,g,seconds,clear) if x['collider'].startswith('source')];sens.append(dict(life=life,kind='source_bout',merge_seconds=seconds,merge_clearance=clear,bouts=len(rows),productive=sum(r['transfer']>0 for r in rows),contact_seconds=sum(r['duration'] for r in rows),transfer=sum(r['transfer'] for r in rows)))
        source_last={}
        for j,r in enumerate(sources):
            s=int(r['collider'].split('-')[1]);i=min(len(t)-1,np.searchsorted(t,r['start']));en=min(len(t)-1,np.searchsorted(t,r['end']));old=source_last.get(s)
            r.update(life=life,bout=j+1,source=s,E_onset=EI[i,0],I_onset=EI[i,1],E_end=EI[en,0],stock_onset=a[i,SL['stocks']][s],stock_end=a[en,SL['stocks']][s],brush_like=r['duration']<1.,productive=r['transfer']>0,approach_speed=speed[max(0,i-1)],departure_speed=speed[en],path_since_previous_contact=plen(sources[j-1]['end'],r['start']) if j else None,time_since_previous_contact=r['start']-sources[j-1]['end'] if j else None)
            r['chemistry_onset']=a[i,SL['raw']][10:14].tolist();r['nearest_other_source_contact']=sources[j-1]['collider'] if j else None
            if old:
                k=np.searchsorted(t,old['end']);clearmax=float(g[k:i+1,4+s].max());r.update(same_source_prior=True,max_departure_clearance=clearmax,true_departure_revisit=clearmax>.25,time_since_same_source=r['start']-old['end'],path_since_same_source=plen(old['end'],r['start']),unrelated_1unit_cells=int(len(set(map(tuple,np.floor(pos[k:i+1]).astype(int))))))
            else:r.update(same_source_prior=False,true_departure_revisit=False)
            for horizon in (5,30):
                end=r['start']+horizon
                r[f'near_after_{horizon}s']=bool(g[min(len(t)-1,np.searchsorted(t,end)),4+s]<=1) if end<=age else None
            r['transfer_per_contact_second']=div(r['transfer'],r['duration']);source_last[s]=r;allbouts.append(r)
        # Source neighborhood recurrence can include a return without a new contact.
        neighborhood=[]
        for s in range(8):
            ends_at=-1;last_visit=None
            for i in np.flatnonzero((g[:,4+s]<=1)&np.r_[True,g[:-1,4+s]>1]):
                if i<ends_at:continue
                ends=np.flatnonzero(g[i:,4+s]>1.5);j=i+ends[0] if len(ends) else len(t)-1;ends_at=j;previous_consequence=any(b['source']==s and b['productive'] and b['end']<t[i] for b in sources)
                r=dict(life=life,source=s,start=float(t[i]),end=float(t[j]),born_near=i==0,censored=not len(ends),previous_consequence=previous_consequence,return_visit=last_visit is not None,return_latency=float(t[i]-last_visit['end']) if last_visit else None,return_path=plen(last_visit['end'],t[i]) if last_visit else None,contact=any(b['source']==s and t[i]<=b['start']<=t[j] for b in sources),productive=any(b['source']==s and b['productive'] and t[i]<=b['start']<=t[j] for b in sources));neighborhood.append(r);last_visit=r
        allneighborhood+=neighborhood
        with gzip.open(PRIOR/'raw'/(life+'_physical_events.csv.gz'),'rt') as f:ev=np.loadtxt(f,delimiter=',',skiprows=1)
        assert abs(ev[:,9:17].sum()-d['physical']['source_transfer'])<1e-9
        # Coverage / revisit census from native cells; no event or goal weighting.
        cells=np.floor(pos/.25).astype(int);codes=cells[:,0]*1000+cells[:,1];change=np.r_[True,codes[1:]!=codes[:-1]];seen=set();entryidx=np.flatnonzero(change);isreturn=[]
        for i in entryidx:isreturn.append(int(codes[i]) in seen);seen.add(int(codes[i]))
        novel=np.zeros(len(t),int);reent=novel.copy();entries=novel.copy();novel[entryidx]=~np.array(isreturn);reent[entryidx]=isreturn;entries[entryidx]=1
        # Visits begin at first native point; include birth cell if it differs.
        state=np.where(forward>.01,1,np.where(forward<-.01,-1,0));bout=[]
        for sign in (-1,1):
            for i,j in contiguous(state==sign):
                dur=float(t[j-1]-(t[i-1] if i else 0))
                if dur>=.1:bout.append(dict(start=float(t[i-1] if i else 0),end=float(t[j-1]),sign=sign,duration=dur))
        bout.sort(key=lambda r:r['start'])
        for label,ranges in [('dashboard',BANDS if n<=7 else [(0,age)]),('fixed60',[(lo,min(lo+60,age)) for lo in np.arange(0,age,60)])]:
            for lo,hi in ranges:
                hi=min(hi,age)
                if lo>=hi:continue
                m=(t>lo)&(t<=hi);em=(ev[:,0]>lo)&(ev[:,0]<=hi);pl=plen(lo,hi);bb=[b for b in sources if lo<b['start']<=hi];ap=[r for r in app if lo<r['start']<=hi and not r['censored']];col=[r for r in collisions if lo<r['start']<=hi];rp=[r for r in repairs if lo<r['start']<=hi];bo=[b for b in bout if lo<=b['start']<hi];sapp=[r for r in ap if r['family']=='source'];neigh=[r for r in neighborhood if lo<r['start']<=hi and not r['born_near'] and not r['censored']]
                displacement=float(np.linalg.norm(np.array([np.interp(hi,t,pos[:,k])-np.interp(lo,tt,pp[:,k]) for k in (0,1)])));spent=float(ev[em,2].sum());transfer=float(ev[em,9:17].sum());damage=float(ev[em,3].sum());repair=float(ev[em,4].sum());counts=np.unique(codes[m],return_counts=True)[1];prob=counts/counts.sum();entropy=-float(np.sum(prob*np.log(prob)))
                contact_time=float(sum(max(0,min(hi,e['end'])-max(lo,e['start']))*e['duration']/max(e['end']-e['start'],1e-30) for e in episodes if e['collider'].startswith('source')));productive_time=float(ev[em & (ev[:,9:17].sum(axis=1)>0),1].sum())
                exposure=float(dt[m & (g.min(axis=1)<=.5)].sum());src_exposure=float(dt[m & (near<=1)].sum());row=dict(life=life,window=label,start=lo,end=hi,seconds=hi-lo,path=pl,displacement=displacement,displacement_path_ratio=div(displacement,pl),new_cells=int(novel[m].sum()),visited_cells=int(len(counts)),entry_count=int(entries[m].sum()),revisit_fraction=div(reent[m].sum(),entries[m].sum()),occupancy_entropy=entropy,coverage_per_energy=div(novel[m].sum(),spent),expenditure=spent,effort=float(cfg['effort_cost']*np.dot(dt[m],abs(u[m]).mean(axis=1))),path_per_energy=div(pl,spent),damage=damage,repair=repair,source_energy=transfer,source_energy_over_expense=div(transfer,spent),source_energy_per_path=div(transfer,pl),source_energy_per_second=transfer/(hi-lo),source_contact_seconds=contact_time,productive_contact_seconds=productive_time,source_transfer_per_contact_second=div(transfer,contact_time),source_bouts=len(bb),productive_bouts=sum(b['productive'] for b in bb),productive_bouts_per_path=div(sum(b['productive'] for b in bb),pl),productive_bouts_per_minute=60*sum(b['productive'] for b in bb)/(hi-lo),distinct_sources=len(set(b['source'] for b in bb)),same_source_revisits=sum(b['true_departure_revisit'] for b in bb),mean_revisit_latency=mean([b['time_since_same_source'] for b in bb if b['true_departure_revisit']]),mean_revisit_path=mean([b['path_since_same_source'] for b in bb if b['true_departure_revisit']]),mean_source_contact_duration=mean([b['duration'] for b in bb]),mean_transfer_per_bout=mean([b['transfer'] for b in bb]),brush_fraction=div(sum(b['brush_like'] for b in bb),len(bb)),retention_5s=mean([b['near_after_5s'] for b in bb if b['productive'] and b['near_after_5s'] is not None]),retention_30s=mean([b['near_after_30s'] for b in bb if b['productive'] and b['near_after_30s'] is not None]),departure_speed=mean([b['departure_speed'] for b in bb if b['productive']]),source_approaches=len(sapp),source_approach_productive_fraction=div(sum(b['transfer']>0 for b in sapp),len(sapp)),source_exposure_seconds=src_exposure,productive_bouts_per_exposure_minute=div(60*sum(b['productive'] for b in bb),src_exposure),neighborhood_visits=len(neigh),consequential_neighborhood_returns=sum(v['return_visit'] and v['previous_consequence'] for v in neigh),hazard_exposure_seconds=exposure,hazard_approaches=len(ap),approaches_with_contact=sum(r['contact'] for r in ap),approaches_with_collision=sum(r['collision'] for r in ap),contact_given_approach=div(sum(r['contact'] for r in ap),len(ap)),collision_given_approach=div(sum(r['collision'] for r in ap),len(ap)),collision_bouts=len(col),collisions_per_path=div(len(col),pl),collisions_per_minute=60*len(col)/(hi-lo),damage_per_path=div(damage,pl),instant_impact_damage_per_collision=div(sum(r['damage'] for r in col),len(col)),mean_collision_peak_impulse=mean([r['peak_impulse'] for r in col]),max_collision_impulse=max([r['peak_impulse'] for r in col],default=0),mean_isolated_closing_speed=mean([r['first_closing'] for r in col if r['first_closing']!='']),max_sustained_force=max([r['peak_sustained_force'] for r in grouped if lo<r['start']<=hi],default=0),contact_seconds=float(dt[m & contact].sum()),pinned_seconds=float(dt[m & immobile].sum()),near_miss_clearance=mean([r['min_clearance'] for r in ap if not r['contact']]),repair_bouts=len(rp),repair_dwell=mean([r['duration'] for r in rp]),repair_relative_speed=mean([r['first_relative_speed'] for r in rp]),mean_E=float(np.average(EI[m,0],weights=dt[m])),mean_I=float(np.average(EI[m,1],weights=dt[m])),mean_speed=float(np.average(speed[m],weights=dt[m])),mean_abs_omega=float(np.average(abs(omega[m]),weights=dt[m])),rotation_per_path=div(np.dot(dt[m],abs(omega[m])),pl),command_variance=float(np.var(u[m],axis=0).mean()),forward_bout_mean=mean([b['duration'] for b in bo if b['sign']==1]),reverse_bout_mean=mean([b['duration'] for b in bo if b['sign']==-1]),reversal_switches=sum(x['sign']!=y['sign'] for x,y in zip(bo,bo[1:])),short_bouts=sum(b['duration']<1 for b in bo))
                (allbands if label=='dashboard' else windows).append(row)
        # Every support interval, including administratively censored first/last pieces.
        bounds=[0]+[r['time'] for r in d['resurrections']]+[age]
        for j,(lo,hi) in enumerate(zip(bounds,bounds[1:])):
            m=(ev[:,0]>lo)&(ev[:,0]<=hi);bb=[b for b in sources if lo<b['start']<=hi];tr=float(ev[m,9:17].sum());spent=float(ev[m,2].sum());pl=plen(lo,hi)
            intervals.append(dict(life=life,interval=j,start=lo,end=hi,duration=hi-lo,end_cause='energy_resurrection' if j<len(bounds)-2 else ('host_censored_prefix' if n==8 else 'administrative_age_stop'),source_energy=tr,expenditure=spent,environment_fraction=div(tr,spent),path=pl,source_energy_per_path=div(tr,pl),source_energy_per_time=div(tr,hi-lo),bouts=len(bb),productive_bouts=sum(b['productive'] for b in bb),productive_contact_seconds=float(ev[m&(ev[:,9:17].sum(axis=1)>0),1].sum()),distinct_sources=len(set(b['source'] for b in bb)),same_source_revisits=sum(b['true_departure_revisit'] for b in bb)))
        for e in [r for r in grouped if r['damage']>0]:
            nxt=next((r for r in repairs if r['start']>e['end']),None);nd=next((r for r in grouped if r['damage']>0 and r['start']>e['end']),None);limit=nd['start'] if nd else age;op=[r for r in app if r['family']=='repair' and r['start']>e['end'] and r['start']<=limit]
            repairseq.append(dict(life=life,damage_start=e['start'],damage_end=e['end'],collider=e['collider'],damage=e['damage'],next_repair_start=nxt['start'] if nxt else None,latency=nxt['start']-e['end'] if nxt else None,path_until_repair=plen(e['end'],nxt['start']) if nxt else None,repair_before_next_damage=bool(nxt and nxt['start']<limit),repair_opportunities_before_next_damage=len(op),next_damage_start=nd['start'] if nd else None,right_censored=nxt is None,repair_gain=nxt['repair'] if nxt else None,repair_dwell=nxt['duration'] if nxt else None))
        allimpact+=collisions
        # Small observer arrays for subsequent matching and plotting; raw input remains copied sensory only.
        si=np.unique(np.r_[np.searchsorted(t,np.arange(0,age,.1)),len(t)-1]);si=si[si<len(t)];(OUT/'cache').mkdir(exist_ok=True)
        np.savez_compressed(OUT/'cache'/(life+'_OBSERVER.npz'),time=t[si],native_index=si,raw=a[si,SL['raw']],commands=u[si],reserves=EI[si],velocity=vel[si],position=pos[si],angle=ang[si],omega=omega[si],path=path[si+1],gaps=g[si],contact=contact[si],speed=speed[si],forward=forward[si],mover_velocity=a[si,SL['mover_velocity']])
        save('cache/'+life+'_EVENTS.json',dict(source_bouts=sources,repair_bouts=repairs,collision_bouts=collisions,approaches=app,neighborhood=neighborhood,all_contact_bouts=grouped,resurrections=d['resurrections']))
        summaries.append(dict(life=life,age=age,source_transfer=sum(r['transfer'] for r in sources),original_source_transfer=d['physical']['source_transfer'],collision_bouts=len(collisions),hazard_approaches=len(app),source_bouts=len(sources),native_rows=len(a)))
        assert abs(sum(r['transfer'] for r in sources)-d['physical']['source_transfer'])<1e-9
        print(life+' passive opportunities, bouts and age bands complete',flush=True)
    for name,rows in [('BEHAVIOURAL_AGE_BANDS',allbands),('BEHAVIOURAL_60S',windows),('RESURRECTION_INTERVALS',intervals),('SOURCE_BOUTS',allbouts),('HAZARD_APPROACHES',allapproach),('DEFINITION_SENSITIVITY',sens),('COLLISION_BOUTS',allimpact),('REPAIR_AFTER_DAMAGE',repairseq),('SOURCE_NEIGHBORHOOD_RETURNS',allneighborhood)]:table('tables/'+name+'.csv',rows)
    save('BEHAVIOURAL_VERIFICATION.json',dict(status='PASS',new_world_steps=0,checks=summaries))
if __name__=='__main__':main()
