"""Keep rare steps visible beside robust background slopes."""
from common import *
rows=[]
for n in range(1,13):
    life=f'RS-M1-{n:03d}';w=np.load(OUT/'cache'/(life+'_waves.npz'));cut=json.loads((OUT/'cache'/(life+'.json')).read_bytes())['curve_cutoff'];mask=w['time']<=cut;t=w['time'][mask]
    d=json.loads((OLD/(life+'_DETAILS.json')).read_bytes());episodes=d['physical']['episodes'];support=np.array([s['time'] for s in d['resurrections']])
    for metric,y in [('H_norm',w['H_norm'][mask]),('regulator_theta_E_norm',w['regulator_bank_norm'][mask,0]),('regulator_theta_I_norm',w['regulator_bank_norm'][mask,1])]:
        delta=np.diff(np.r_[0,y]);ranked=np.argsort(-delta);chosen=[]
        for idx in ranked:
            if delta[idx]<=0:break
            if all(abs(t[idx]-t[j])>=5 for j in chosen):chosen.append(idx)
            if len(chosen)==5:break
        for rank,idx in enumerate(chosen):
            near=[e for e in episodes if e['end']>=t[idx]-2 and e['start']<=t[idx]]
            # Episode totals can exceed the two-second overlap; label as context, not local sums.
            rows.append(dict(life=life,metric=metric,rank_positive_wave_increment=rank+1,age=t[idx],wave=int(w['wave'][mask][idx]),increment=delta[idx],value=y[idx],source_context=any(e['collider'].startswith('source') for e in near),damage_context=any(e['damage']>0 for e in near),repair_context=any(e['repair']>0 for e in near),collider_context=';'.join(sorted(set(e['collider'] for e in near))),seconds_to_nearest_resurrection=float(abs(support-t[idx]).min()) if len(support) else None))
table('tables/EVENT_STEP_CATALOG.csv',rows)
print('Largest positive increments retained separately from robust slopes; passive only.')
