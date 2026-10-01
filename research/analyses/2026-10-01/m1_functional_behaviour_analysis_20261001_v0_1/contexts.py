"""Fixed observer nearest-neighbor analysis. Features never contain geometry/outcomes."""
from common import *
from behaviour import COLLIDERS

GROUPS=[('light',slice(0,20)),('chemistry',slice(20,28)),('proprioception',slice(28,42)),('recent_command',slice(42,46)),('body_EI',slice(46,48))]
def main():
    allpairs=[];queries=[];sensitivity=[];normalization=[];summaries=[];consistency=[];featurehash=[]
    for number in range(1,13):
        life=f'RS-M1-{number:03d}';d=np.load(OUT/'cache'/(life+'_OBSERVER.npz'));t=d['time'];age=float(t[-1]);a=native(life);events=json.loads((OUT/'cache'/(life+'_EVENTS.json')).read_bytes());raw=d['raw'];u=d['commands'];EI=d['reserves'];speed=d['speed'];g=d['gaps'];pos=d['position'];angle=d['angle'];omega=d['omega'];contact=d['contact'];path=d['path']
        with gzip.open(PRIOR/'raw'/(life+'_physical_events.csv.gz'),'rt') as f:physical=np.loadtxt(f,delimiter=',',skiprows=1)
        def features(i):
            lo=np.searchsorted(t,t[i]-2,side='right');hist=raw[lo:i+1];cmd=u[lo:i+1]
            return np.r_[hist[:,:10].mean(axis=0),raw[i,:10],hist[:,10:14].mean(axis=0),raw[i,10:14],hist[:,22:29].mean(axis=0),raw[i,22:29],cmd.mean(axis=0),u[i],EI[i]],bool(not contact[lo:i+1].any())
        ids=np.searchsorted(t,np.arange(2,age-10,1));ids=ids[ids<len(t)];F=[];free=[]
        for i in ids:x,b=features(i);F.append(x);free.append(b)
        F=np.array(F);free=np.array(free);scale=np.maximum(np.subtract(*np.percentile(F,[75,25],axis=0)),.01);center=np.median(F,axis=0);weights=np.ones(48)
        for _,sl in GROUPS:weights[sl]=1/math.sqrt((sl.stop-sl.start)*len(GROUPS))
        Z=(F-center)/scale*weights
        normalization.append(dict(life=life,family_slices=[dict(name=k,start=s.start,end=s.stop) for k,s in GROUPS],median=center,IQR_floor_scale=scale,distance_weights=weights,candidates=len(ids)))
        np.savez_compressed(OUT/'cache'/(life+'_PERMITTED_CONTEXTS.npz'),age=t[ids],features=F,contact_free=free,normalized=Z)
        def normal(i,k):
            if k<4:return np.array([[1,0],[-1,0],[0,1],[0,-1]])[k]
            if k<12:delta=pos[i]-SOURCE[k-4]
            else:
                rect=cfg['repair_rectangles'][k-12] if k<15 else a[int(d['native_index'][i]),SL['mover_rectangle']]
                delta=pos[i]-np.array([np.clip(pos[i,0],rect[0],rect[1]),np.clip(pos[i,1],rect[2],rect[3])])
            return delta/max(norm(delta),1e-30)
        def outcome(i):
            lo=t[i];j=min(len(t)-1,np.searchsorted(t,lo+10));j1=min(len(t)-1,np.searchsorted(t,lo+1));k=int(g[i].argmin());s=int(g[i,4:12].argmin());n=normal(i,k);heading=np.array([np.cos(angle[i]),np.sin(angle[i])]);vrel=d['velocity'][i]-(d['mover_velocity'][i] if k==15 else 0);closing=max(0,-float(vrel@n));ending=np.flatnonzero(g[i:j+1,k]>1);em=(physical[:,0]>lo)&(physical[:,0]<=lo+10)
            collisions=[c for c in events['collision_bouts'] if lo<c['start']<=lo+10];anysource=physical[em,9:17].sum();src=physical[em,9+s].sum();bouts=[b for b in events['source_bouts'] if lo<b['start']<=lo+10]
            return dict(age=float(lo),E=float(EI[i,0]),I=float(EI[i,1]),speed=float(speed[i]),hazard_gap=float(g[i,k]),source_gap=float(g[i,4+s]),hazard_opportunity=bool(g[i,k]<=1 and closing>.01),hazard_id_observer=COLLIDERS[k],source_id_observer=s,collision=bool(collisions),collision_count=len(collisions),minimum_clearance=float(g[i:j+1].min()),minimum_target_clearance=float(g[i:j+1,k].min()),closing_speed_proxy=closing,peak_impulse=max([c['peak_impulse'] for c in collisions],default=0),damage=float(physical[em,3].sum()),repair=float(physical[em,4].sum()),turn_toward_outward_normal=float(np.mean(omega[i:j1+1])*np.cross(np.r_[heading,0],np.r_[n,0])[2]),forward_drive_before=float(u[i].mean()),forward_drive_change=float(u[i:j1+1].mean()-u[i].mean()),forward_speed_before=float(d['forward'][i]),mean_speed_next10=float(speed[i:j+1].mean()),time_to_separation=float(t[i+ending[0]]-lo) if len(ending) else None,separation_censored=not len(ending),source_energy=float(anysource),nearest_source_energy=float(src),source_distance_reduction=float(g[i,4+s]-g[j,4+s]),minimum_source_gap=float(g[i:j+1,4+s].min()),near_source_at10=bool(g[j,4+s]<=1),productive_source_bouts=sum(b['productive'] for b in bouts),mean_command_left=float(u[i:j1+1,0].mean()),mean_command_right=float(u[i:j1+1,1].mean()),mean_omega_next1=float(omega[i:j1+1].mean()),command_variance_next10=float(np.var(u[i:j+1],axis=0).mean()),heading_persistence_10=float(np.cos(angle[j]-angle[i])),path_next10=float(path[j]-path[i]),support_within_outcome=any(lo<r['time']<=lo+10 for r in events['resurrections']))
        outcome_cache={}
        def getout(i):
            if i not in outcome_cache:outcome_cache[i]=outcome(i)
            return outcome_cache[i]
        specs=[]
        specs += [('collision',j+1,c['start']-1,True) for j,c in enumerate(events['collision_bouts'])]
        specs += [('productive_source',j+1,b['start']-1,True) for j,b in enumerate(events['source_bouts']) if b['productive']]
        specs += [('unselected_early_context',j+1,float(q),True) for j,q in enumerate(np.arange(5,min(600,age-70),30))]
        # Fixed generic context queries; select by experienced feature state only.
        for j,q in enumerate(np.arange(5,min(600,age-70),30)):
            i=min(len(t)-1,np.searchsorted(t,q));chem=raw[i,10:14];diff=(chem[2:]-chem[:2]).mean()
            if abs(diff)>.01:specs.append(('chemical_imbalance',j+1,float(q),True))
            k=max(0,np.searchsorted(t,q-2));rise=raw[i,10:14].mean()-raw[k,10:14].mean()
            if rise>.005:specs.append(('rising_chemistry',j+1,float(q),True))
            if EI[i,0]<.2:specs.append(('low_E',j+1,float(q),True))
        specs += [('post_impact',j+1,c['start']+1,False) for j,c in enumerate(events['collision_bouts']) if c['start']<min(600,age-70)]
        for kind,ordinal,qtime,require_free in specs:
            qi=min(len(t)-1,np.searchsorted(t,qtime));qid=f'{life}:{kind}:{ordinal}';reason=None
            if qtime<2 or qtime+70>age:reason='insufficient_pre_or_later_followup'
            feat,isfree=features(qi)
            if require_free and not isfree:reason='prehistory_not_contact_free'
            if reason:queries.append(dict(life=life,kind=kind,query=qid,age=qtime,eligible=False,reason=reason));continue
            eligible=(t[ids]>=t[qi]+60)&(abs(EI[ids,0]-EI[qi,0])<=.1)&(abs(EI[ids,1]-EI[qi,1])<=.05)&(abs(speed[ids]-speed[qi])<=.03)
            if require_free:eligible&=free
            z=(feat-center)/scale*weights;dist=np.linalg.norm(Z-z,axis=1);ordering=np.argsort(np.where(eligible,dist,np.inf));selected=[]
            for ix in ordering:
                if not eligible[ix] or not np.isfinite(dist[ix]):break
                if all(abs(t[ids[ix]]-t[ids[j]])>=10 for j in selected):selected.append(int(ix))
                if len(selected)==5:break
            base=getout(qi);queries.append(dict(life=life,kind=kind,query=qid,age=float(t[qi]),eligible=True,candidates=int(eligible.sum()),nearest_distance=float(dist[selected[0]]) if selected else None,main_matches=sum(dist[ix]<=1 for ix in selected[:3]),**{'query_'+k:v for k,v in base.items()}))
            for k in (1,3,5):
                for cap in (.5,1.,2.):
                    chosen=[ix for ix in selected[:k] if dist[ix]<=cap];outs=[getout(int(ids[ix])) for ix in chosen]
                    sensitivity.append(dict(life=life,kind=kind,query=qid,k=k,cap=cap,matches=len(chosen),query_collision=int(base['collision']),later_collision=mean([v['collision'] for v in outs]),query_clearance=base['minimum_clearance'],later_clearance=mean([v['minimum_clearance'] for v in outs]),query_damage=base['damage'],later_damage=mean([v['damage'] for v in outs]),query_source_energy=base['source_energy'],later_source_energy=mean([v['source_energy'] for v in outs]),query_source_reduction=base['source_distance_reduction'],later_source_reduction=mean([v['source_distance_reduction'] for v in outs]),query_hazard_opportunity=base['hazard_opportunity'],later_hazard_opportunity=mean([v['hazard_opportunity'] for v in outs])))
            for rank,ix in enumerate(selected[:3]):
                if dist[ix]>1:continue
                other=getout(int(ids[ix]));row=dict(life=life,kind=kind,query=qid,rank=rank+1,normalized_distance=float(dist[ix]),query_contact_free=isfree,later_contact_free=bool(free[ix]),**{'early_'+k:v for k,v in base.items()},**{'later_'+k:v for k,v in other.items()})
                for key in ('minimum_clearance','minimum_target_clearance','closing_speed_proxy','peak_impulse','damage','turn_toward_outward_normal','forward_drive_change','source_energy','source_distance_reduction','mean_command_left','mean_command_right','command_variance_next10','heading_persistence_10'):
                    row['delta_'+key]=other[key]-base[key]
                allpairs.append(row)
        my=[r for r in allpairs if r['life']==life]
        for kind in sorted(set(r['kind'] for r in queries if r['life']==life)):
            qq=[r for r in queries if r['life']==life and r['kind']==kind];rr=[r for r in my if r['kind']==kind];both=[r for r in rr if r['early_hazard_opportunity'] and r['later_hazard_opportunity']]
            def summarize(pairs,subset):
                summaries.append(dict(life=life,kind=kind,subset=subset,declared_queries=len(qq),eligible_queries=sum(r['eligible'] for r in qq),matched_queries=len(set(r['query'] for r in pairs)),pairs=len(pairs),early_collision=mean([r['early_collision'] for r in pairs]),later_collision=mean([r['later_collision'] for r in pairs]),early_hazard_opportunity=mean([r['early_hazard_opportunity'] for r in pairs]),later_hazard_opportunity=mean([r['later_hazard_opportunity'] for r in pairs]),delta_clearance=mean([r['delta_minimum_clearance'] for r in pairs]),delta_closing=mean([r['delta_closing_speed_proxy'] for r in pairs]),delta_damage=mean([r['delta_damage'] for r in pairs]),delta_source_energy=mean([r['delta_source_energy'] for r in pairs]),delta_source_distance_reduction=mean([r['delta_source_distance_reduction'] for r in pairs]),delta_forward_drive=mean([r['delta_forward_drive_change'] for r in pairs]),delta_action_variance=mean([r['delta_command_variance_next10'] for r in pairs])))
            summarize(rr,'all_main_matches');summarize(both,'both_hazard_opportunity')
        print(life+' sensory-only context matches complete',flush=True)
    table('tables/CONTEXT_QUERIES',[]) if False else None
    for name,rows in [('CONTEXT_QUERIES',queries),('CONTEXT_PAIRS',allpairs),('CONTEXT_SENSITIVITY',sensitivity),('CONTEXT_SUMMARY',summaries)]:table('tables/'+name+'.csv',rows)
    save('CONTEXT_FEATURE_AUDIT.json',dict(allowed_features=['mean/endpoint raw light[10]','mean/endpoint raw chemistry[4]','mean/endpoint raw proprioception[7]','mean/endpoint paired actual command','actual E','actual I'],forbidden_features_present=[],feature_count=48,normalization=normalization,selection_uses_future_outcome=False,world_steps=0,trained_models=0))
if __name__=='__main__':main()
