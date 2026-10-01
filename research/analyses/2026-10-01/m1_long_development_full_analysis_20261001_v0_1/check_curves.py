"""Independent recomputation from full checkpoints, not extraction reducers.
This is an independently coded consistency review by the same analyst.
"""
from common import *
import gzip
rows=[];worst=0.;checked=0
for number in range(1,13):
    life=f'RS-M1-{number:03d}';w=np.load(OUT/'cache'/(life+'_waves.npz'));rec=json.loads((OUT/'cache'/(life+'.json')).read_bytes());cut=rec['curve_cutoff'];errors=[]
    for p in checkpoint_paths(life):
        e=attrs(rd(p)['engine'])
        if e['time']>cut:continue
        o=attrs(e['organism']);a=attrs(o['association']);r=attrs(o['regulator']);j=np.searchsorted(w['wave'],o['wave_count'])
        norms=np.array([math.sqrt(sum(float((v*v).sum()) for v in a['H'].values())),math.sqrt(float((r['theta'][0]*r['theta'][0]).sum())),math.sqrt(float((r['theta'][1]*r['theta'][1]).sum()))])
        expected=np.r_[w['H_norm'][j],w['regulator_bank_norm'][j]] if o['wave_count'] else np.zeros(3)
        err=float(np.max(abs(norms-expected)));errors.append(err);assert err<1e-14
        checked+=1
    # Compare against independently preserved prior extraction.
    old=list(csv.DictReader((OLD/(life+'_WAVE_HISTORY.csv')).open(encoding='utf8')))
    assert len(old)==len(w['time'])
    err=max(abs(float(z['H_norm'])-x) for z,x in zip(old,w['H_norm']));assert err<1e-14
    assert max(abs(float(z['bank_E'])-x) for z,x in zip(old,w['regulator_bank_norm'][:,0]))<1e-14
    with gzip.open(OUT/'raw'/(life+'_H_E_I_WAVES.csv.gz'),'rt',encoding='utf8') as f:
        raw=list(csv.DictReader(f));assert len(raw)==rec['curve_waves'];assert float(raw[-1]['age'])<=cut
    native=np.load(OUT/'cache'/(life+'_native.npy'),mmap_mode='r')
    with gzip.open(OUT/'raw'/(life+'_BODY_NATIVE.csv.gz'),'rt',encoding='utf8') as f:
        reader=csv.DictReader(f);birth=next(reader);assert float(birth['age'])==0
        i=0
        for row in reader:
            assert int(float(row['native_index']))==i+1
            assert float(row['age'])==native[i,0]
            assert float(row['E'])==native[i,SL['reserves']][0] and float(row['I'])==native[i,SL['reserves']][1]
            i+=1
        assert i==int((native[:,0]<=cut).sum())
    rows.append(dict(life=life,checkpoints_checked=len(errors),max_checkpoint_norm_error=max(errors),prior_wave_comparison_error=err,raw_waves=len(raw),raw_native=i,cutoff=cut))
    print(life+' independently checked',flush=True)
save('CURVE_CONSISTENCY_REVIEW.json',dict(status='PASS',review_kind='Independent calculation paths by same analyst; not a second-person or external scientific review',full_checkpoints_checked=checked,checks=rows,new_simulation_steps=0,no_simulator_imports=True))
