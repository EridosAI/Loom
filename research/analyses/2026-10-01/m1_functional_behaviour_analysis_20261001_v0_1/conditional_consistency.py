"""Outcome-independent sensory neighborhoods; no fit/training or policy."""
from common import *
rows=[]
for n in range(1,13):
    life=f'RS-M1-{n:03d}';c=np.load(OUT/'cache'/(life+'_PERMITTED_CONTEXTS.npz'));o=np.load(OUT/'cache'/(life+'_OBSERVER.npz'));e=json.loads((OUT/'cache'/(life+'_EVENTS.json')).read_bytes());t=c['age'];z=c['normalized'];F=c['features'];ot=o['time'];age=float(ot[-1]);width=min(600,age/3);early=t<=width;late=t>=age-width;oi=np.searchsorted(ot,t);oi=np.minimum(oi,len(ot)-1);speed=o['speed'][oi]
    def action(ix):
        i=oi[ix];j=min(len(ot)-1,np.searchsorted(ot,ot[i]+1));end=ot[i]+10;u=o['commands'][i:j+1].mean(axis=0)
        return u,float(o['omega'][i:j+1].mean()),any(ot[i]<v['start']<=end for v in e['collision_bouts']),any(ot[i]<v['start']<=end and v['productive'] for v in e['source_bouts'])
    anchors=np.searchsorted(t,np.arange(5,width,30));anchors=anchors[anchors<len(t)]
    for anchor in anchors:
        if not c['contact_free'][anchor]:continue
        diff=(F[anchor,26:28]-F[anchor,24:26]).mean();rise=F[anchor,24:28].mean()-F[anchor,20:24].mean();tags=['generic_contact_free']+(['low_E'] if F[anchor,46]<.2 else [])+(['chemical_imbalance'] if abs(diff)>.01 else [])+(['rising_chemistry'] if rise>.005 else [])
        dist=np.linalg.norm(z-z[anchor],axis=1);eligible=c['contact_free']&(abs(F[:,46]-F[anchor,46])<=.1)&(abs(F[:,47]-F[anchor,47])<=.05)&(abs(speed-speed[anchor])<=.03)&(abs(t-t[anchor])>=10)
        for k in (3,5):
            selections={}
            for period,mask in [('early',early),('late',late)]:
                choices=[]
                for ix in np.argsort(np.where(eligible&mask,dist,np.inf)):
                    if not (eligible&mask)[ix] or dist[ix]>1:break
                    if all(abs(t[ix]-t[j])>=10 for j in choices):choices.append(int(ix))
                    if len(choices)==k:break
                selections[period]=choices
            rr=dict(life=life,query_age=t[anchor],k=k,early_count=len(selections['early']),late_count=len(selections['late']),paired_dispersion_available=min(map(len,selections.values()))>=2)
            for period,choices in selections.items():
                outs=[action(ix) for ix in choices];cmd=np.array([v[0] for v in outs]);rr[period+'_action_dispersion']=float(np.var(cmd,axis=0,ddof=1).mean()) if len(cmd)>=2 else None;rr[period+'_mean_common']=mean([v[0].mean() for v in outs]);rr[period+'_mean_differential']=mean([(v[0][1]-v[0][0])/2 for v in outs]);rr[period+'_mean_omega']=mean([v[1] for v in outs]);rr[period+'_collision_fraction']=mean([v[2] for v in outs]);rr[period+'_productive_fraction']=mean([v[3] for v in outs]);rr[period+'_matched_ages']=';'.join(f'{t[ix]:.6f}' for ix in choices)
            for tag in tags:rows.append(dict(kind=tag,**rr))
    print(life+' conditional action dispersion measured',flush=True)
table('tables/CONDITIONAL_ACTION_CONSISTENCY.csv',rows)
