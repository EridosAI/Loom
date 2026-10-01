"""Descriptive regressions only; never imports or runs P."""
from common import *
from scipy.stats import theilslopes
from scipy.optimize import least_squares

METRICS=['H_norm','regulator_theta_E_norm','regulator_theta_I_norm']
def bin_series(t,y,width,lo=0,hi=None):
    hi=t[-1] if hi is None else hi;tx=[];yy=[]
    for a in np.arange(lo,hi,width):
        ok=(t>a)&(t<=min(a+width,hi))
        if ok.any():tx.append(float(t[ok].mean()));yy.append(float(np.median(y[ok])))
    return np.array(tx),np.array(yy)
def slope(t,y,lo,hi):
    x,v=bin_series(t,y,5,lo,hi)
    if len(x)<3:return None
    s,intercept,_,_=theilslopes(v,x)
    p=np.polyfit(x,v,1);scale=max(float(np.median(abs(v-np.median(v)))),1e-30)
    return dict(start=lo,end=hi,n_5s_medians=len(x),theil_sen_slope=float(s),OLS_slope=float(p[0]),net_median_change=float(np.median(v[-min(12,len(v)):])-np.median(v[:min(12,len(v))])),range=float(v.max()-v.min()),median=float(np.median(v)),residual_MAD=float(np.median(abs(v-(s*x+intercept)))),predicted_change=float(s*(hi-lo)))
def models(life,key,t,y,exclude):
    x,v=bin_series(t,y,60,exclude,4500);scale=max(float(np.ptp(v)),1e-14);u=x/4500;z=v/scale
    funcs={'linear':lambda p:p[0]+p[1]*u,'saturating_exponential':lambda p:p[0]+p[1]*(1-np.exp(-u/p[2])),'power':lambda p:p[0]+p[1]*u**p[2]}
    spec={
        'linear':([[-100,-100],[100,100]],[[z[0],z[-1]-z[0]]]),
        'saturating_exponential':([[0,0,1/4500],[100,100,1e6/4500]],[[z[0],1,q/4500] for q in (150,900,4500,45000)]),
        'power':([[0,0,.05],[100,100,3]],[[z[0],1,p] for p in (.3,.7,1,1.5)])}
    rows=[];fits={}
    for model,(bounds,starts) in spec.items():
        fn=funcs[model];attempts=[least_squares(lambda p:fn(p)-z,p,bounds=bounds,loss='soft_l1',f_scale=.1,max_nfev=5000) for p in starts];fit=min(attempts,key=lambda a:a.cost);pred=fn(fit.x)*scale;res=v-pred
        p=fit.x.copy();p[:2]*=scale
        row=dict(life=life,metric=key,model=model,exclude_first_seconds=exclude,n_60s_medians=len(x),RMSE=rms(res),MAE=float(np.mean(abs(res))),R_squared=float(1-np.sum(res**2)/np.sum((v-v.mean())**2)) if np.ptp(v)>0 else None,residual_lag1=corr(res[:-1],res[1:]),residual_early_mean=float(res[:10].mean()),residual_late_mean=float(res[-10:].mean()),a_or_A=p[0],b_or_B=p[1],p_or_tau_seconds=(fit.x[2]*4500 if model=='saturating_exponential' else (fit.x[2] if model=='power' else None)),optimizer_success=bool(fit.success),asymptote_is_model_only=model=='saturating_exponential')
        if model=='linear':row['b_or_B']=p[1]/4500
        if model=='saturating_exponential':row['a_or_A']=p[0]+p[1]
        if model=='power':row['b_or_B']=p[1]/4500**fit.x[2]
        row['parameter_boundary']=bool(np.any(abs(fit.x-np.asarray(bounds[0]))<1e-6)|np.any(abs(fit.x-np.asarray(bounds[1]))<1e-6))
        row['local_median_decreases']=int(np.sum(np.diff(v)<0))
        row['diagnostic_only_not_selected_mechanism']=True
        if model=='saturating_exponential':
            grid=np.geomspace(30,1e6,101);rmses=[]
            for tau in grid:
                mat=np.column_stack((np.ones_like(x),-np.exp(-x/tau)));coef=np.linalg.lstsq(mat,v,rcond=None)[0]
                rmses.append(rms(v-mat@coef) if coef[1]>=0 and coef[0]-coef[1]>=0 else float('inf'))
            # This band is a sensitivity diagnostic, explicitly not a confidence interval.
            accepted=grid[np.array(rmses)<=min(rmses)*1.1+1e-15]
            row.update(tau_profile_10pct_RMSE_low=float(accepted.min()),tau_profile_10pct_RMSE_high=float(accepted.max()),profile_not_confidence_interval=True)
        rows.append(row);fits[model]=dict(age=x,observed=v,predicted=pred,residual=res)
    return rows,fits

def main():
    slopes=[];fits=[];summary=[];plotfit={};events=[]
    encounters=json.loads((OLD/'DEVELOPMENTAL_SUMMARY.json').read_bytes())['encounters']
    for number in range(1,13):
        life=f'RS-M1-{number:03d}';d=np.load(OUT/'cache'/(life+'_curves.npz'));a=d['wave'];columns=list(d['wave_columns']);t=a[:,0];record=json.loads((OUT/'cache'/(life+'.json')).read_bytes());cut=record['curve_cutoff']
        detail=json.loads((OLD/(life+'_DETAILS.json')).read_bytes())
        for e in detail['resurrections']:
            if e['time']<=cut:events.append(dict(life=life,age=e['time'],kind='external_resurrection',amount=e['external_support'][0]))
        productive=[b for b in encounters[life] if b['transfer']>0 and b['start']<=cut]
        for j,b in enumerate(productive):
            # Fixed absolute display threshold, not an outcome selection criterion.
            if j==0 or b['transfer']>=.02:events.append(dict(life=life,age=b['start'],end=min(cut,b['end']),kind='first_productive' if j==0 else 'major_productive_0.02_E',amount=b['transfer']))
        for e in detail['physical']['episodes']:
            if e['start']<=cut and e['damage']>=.002:events.append(dict(life=life,age=e['start'],end=min(cut,e['end']),kind='damage_ge_0.002',amount=e['damage']))
            if e['start']<=cut and e['repair']>=.0001:events.append(dict(life=life,age=e['start'],end=min(cut,e['end']),kind='repair_ge_0.0001',amount=e['repair']))
        for key in METRICS:
            y=a[:,columns.index(key)]
            for width in (300,600):
                for lo in np.arange(0,cut,width):
                    r=slope(t,y,float(lo),min(float(lo+width),cut))
                    if r:slopes.append(dict(life=life,metric=key,window_type=f'fixed_{width}',**r))
            ranges=[('early',0,min(1000,cut/3)),('middle',max(0,cut/2-min(500,cut/6)),min(cut,cut/2+min(500,cut/6))),('late',max(0,cut-min(1000,cut/3)),cut)]
            if cut>=1000:ranges.append(('final_1000',cut-1000,cut))
            selected={}
            for label,lo,hi in ranges:
                r=slope(t,y,lo,hi)
                if r:slopes.append(dict(life=life,metric=key,window_type=label,**r));selected[label]=r
            summary.append(dict(life=life,metric=key,age=cut,first=float(y[0]),last=float(y[-1]),peak=float(y.max()),peak_age=float(t[y.argmax()]),early=selected.get('early'),middle=selected.get('middle'),late=selected.get('final_1000',selected.get('late'))))
            if number<=7:
                for exclude in (0,600):
                    rows,curves=models(life,key,t,y,exclude);fits+=rows;plotfit[f'{life}:{key}:exclude{exclude}']=curves
    table('tables/LOCAL_AND_LATE_SLOPES.csv',slopes);table('tables/SHAPE_MODEL_COMPARISON.csv',fits);table('tables/CURVE_EVENT_MARKERS.csv',events)
    save('CURVE_SHAPE_SUMMARY.json',summary);save('CURVE_MODEL_FITS.json',plotfit);save('CURVE_EVENTS.json',events)
    print('Computed robust local slopes and descriptive models for all requested curves; zero simulation.')
if __name__=='__main__':main()
