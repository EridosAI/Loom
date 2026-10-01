from common import *
rows=[]
for number in range(1,13):
    life=f'RS-M1-{number:03d}';d=np.load(OUT/'cache'/(life+'_curves.npz'));a=d['wave'];cols=list(d['wave_columns']);end=json.loads((OUT/'cache'/(life+'.json')).read_bytes())['curve_cutoff'];w=np.load(OUT/'cache'/(life+'_waves.npz'));n=(w['time']<=end).sum()
    for band,lo,hi in [('early',0,min(1000,end/3)),('middle',end/2-min(500,end/6),end/2+min(500,end/6)),('late',max(0,end-min(1000,end/3)),end)]:
        mask=(a[:,0]>lo)&(a[:,0]<=hi);r=dict(life=life,band=band,start=lo,end=hi,waves=int(mask.sum()))
        for key in cols[3:]:
            values=a[mask,cols.index(key)];r[key+'_mean']=float(values.mean());r[key+'_RMS']=rms(values)
        sp=r['M1_spontaneous_rms_RMS'];r['E_current_effect_over_M1']=r['learned_E_current_delta_rms_RMS']/sp;r['I_current_effect_over_M1']=r['learned_I_current_delta_rms_RMS']/sp
        gain=(1-w['attenuation_used'][:n][mask])*(1-w['target'][:n][mask]**2);r['motor_target_local_gain_min']=float(gain.min());r['motor_target_local_gain_mean']=float(gain.mean())
        rows.append(r)
table('tables/FUNCTIONAL_READOUT_BY_AGE.csv',rows)
print('Functional age bands derived from stored waves only.')
