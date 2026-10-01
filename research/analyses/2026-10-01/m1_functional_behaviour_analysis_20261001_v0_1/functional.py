from common import *
from scipy.stats import theilslopes

KEYS=['E_current_effect','I_current_effect','E_command_effect','I_command_effect','E_full_receiver_effect','I_full_receiver_effect','E_over_M1','I_over_M1','q_norm','H_use_mean','direct_feedback_RMS','regulator_current_RMS','command_RMS','attenuation_mean','M1_RMS','H_norm','theta_E_norm','theta_I_norm','command_per_theta_E','command_per_theta_I','q_per_H','use_per_H','associative_motor_command_effect','M1_command_effect']
def main():
    checks=[];bands=[];slopes=[];structure=[]
    for n in range(1,13):
        life=f'RS-M1-{n:03d}';w=np.load(PRIOR/'cache'/(life+'_waves.npz'));rec=record(life);cut=rec['curve_cutoff'];keep=w['time']<=cut;t=w['time'][keep];count=len(t);a=native(life)
        initial=attrs(rd(next((EX/'lives'/life).glob('pilot-*-pilot-initial.ld')))['engine']);r=attrs(attrs(initial['organism'])['regulator']);birth=r['output_diagnostic']
        previous=lambda key,first:np.concatenate((np.asarray(first)[None],w[key][:count-1]),axis=0)
        L=previous('learned',birth['learned']);X=previous('exploration',birth['exploration']);N=previous('need',birth['need']);C=controls(L,X,N)
        cur=w['current'][:count];atten=w['attenuation_used'][:count];target=w['target'][:count];tend=w['tendency'][:count];command=w['command'][:count]
        errors=[np.max(abs(C[:,8:10]-cur)),np.max(abs(C[:,10:12]-atten)),np.max(abs((1-atten)*tend-command))]
        z=w['oscillator'][:count]+w['direct_feedback'][:count]+w['evoked'][:count]+cur
        errors.append(np.max(abs(np.tanh(z)-target)))
        qprev=previous('q',np.zeros(164));errors.append(np.max(abs(qprev[:,134:136]-w['evoked'][:count])))
        assert max(errors)<1e-14,errors
        dt=a[w['index'][:count].astype(int)-1,SL['elapsed']][:,0];alpha=-np.expm1(-dt/cfg['tau_motor']);alpha=alpha[:,None]
        pair={};data={'age':t};rmsrow=lambda x:np.sqrt(np.mean(x*x,axis=1))
        for bank,label in ((0,'E'),(1,'I')):
            omitted=L.copy();omitted[:,bank]=0;no=controls(omitted,X,N);dc=C[:,8:10]-no[:,8:10]
            target_without=np.tanh(z-dc);current_only=(1-atten)*alpha*(target-target_without)
            without_tendency=tend+alpha*(target_without-target)
            full=command-(1-no[:,10:12])*without_tendency
            data[label+'_current_effect']=rmsrow(dc);data[label+'_command_effect']=rmsrow(current_only);data[label+'_full_receiver_effect']=rmsrow(full)
            pair[label+'_current_delta']=dc;pair[label+'_command_delta']=current_only;pair[label+'_full_delta']=full
        sp=w['oscillator'][:count];qmotor=w['evoked'][:count]
        motorq=(1-atten)*alpha*(target-np.tanh(z-qmotor));motorM1=(1-atten)*alpha*(target-np.tanh(z-sp))
        norms=previous('regulator_bank_norm',np.zeros(2));data.update(H_norm=w['H_norm'][:count],theta_E_norm=norms[:,0],theta_I_norm=norms[:,1],q_norm=np.linalg.norm(w['q'][:count],axis=1),H_use_mean=w['H_use_mean'][:count],direct_feedback_RMS=rmsrow(w['direct_feedback'][:count]),regulator_current_RMS=rmsrow(cur),command_RMS=rmsrow(command),attenuation_mean=atten.mean(axis=1),M1_RMS=rmsrow(sp),associative_motor_command_effect=rmsrow(motorq),M1_command_effect=rmsrow(motorM1),native_elapsed=dt,attenuation_left=atten[:,0],attenuation_right=atten[:,1],local_gain_min=np.min((1-atten)*(1-target**2),axis=1))
        for bank in ('E','I'):
            data[bank+'_over_M1']=ratio(rolling(t,data[bank+'_command_effect'],squared=True),rolling(t,data['M1_RMS'],squared=True))
            data['command_per_theta_'+bank]=ratio(data[bank+'_command_effect'],data['theta_'+bank+'_norm'])
            data[bank+'_current_over_M1']=ratio(rolling(t,data[bank+'_current_effect'],squared=True),rolling(t,data['M1_RMS'],squared=True))
            data[bank+'_over_M1_same_receiver']=ratio(rolling(t,data[bank+'_command_effect'],squared=True),rolling(t,data['M1_command_effect'],squared=True))
        data['q_per_H']=ratio(data['q_norm'],data['H_norm']);data['use_per_H']=ratio(data['H_use_mean'],data['H_norm'])
        (OUT/'series').mkdir(exist_ok=True);np.savez_compressed(OUT/'series'/(life+'_FUNCTIONAL.npz'),**data,**pair)
        with gzip.open(OUT/'series'/(life+'_FUNCTIONAL.csv.gz'),'wt',newline='',encoding='utf8') as f:
            wr=csv.writer(f);names=list(data)+[k+'_'+side for k in pair for side in ('left','right')];wr.writerow(names);matrix=np.column_stack(list(data.values())+list(pair.values()));wr.writerows(matrix)
        ranges=[('early',0,min(1000,cut/3)),('middle',cut/2-min(500,cut/6),cut/2+min(500,cut/6)),('late',cut-min(1000,cut/3),cut)]
        if cut>=1000:ranges.append(('final1000',cut-1000,cut))
        ranges.extend((f'fixed{width}',lo,min(lo+width,cut)) for width in (300,600) for lo in np.arange(0,cut,width))
        for label,lo,hi in ranges:
            mask=(t>lo)&(t<=hi);row=dict(life=life,band=label,start=lo,end=hi,waves=int(mask.sum()))
            for key in KEYS:
                y=data[key];valid=mask&np.isfinite(y);row[key+'_RMS']=rms(y[valid]);row[key+'_mean']=mean(y[valid])
                xx=[];yy=[]
                for a0 in np.arange(lo,hi,5):
                    ok=(t>a0)&(t<=min(a0+5,hi))&np.isfinite(y)
                    if ok.any():xx.append(t[ok].mean());yy.append(np.median(y[ok]))
                if len(xx)>=3:
                    s,inter,_,_=theilslopes(yy,xx);slopes.append(dict(life=life,metric=key,band=label,start=lo,end=hi,slope=float(s),predicted_change=float(s*(hi-lo)),median=float(np.median(yy)),residual_MAD=float(np.median(abs(np.array(yy)-(s*np.array(xx)+inter)))),OLS_slope=float(np.polyfit(xx,yy,1)[0])))
            row['E_current_to_M1_window_ratio']=div(row['E_current_effect_RMS'],row['M1_RMS_RMS']);row['I_current_to_M1_window_ratio']=div(row['I_current_effect_RMS'],row['M1_RMS_RMS'])
            row['E_command_to_M1_window_ratio']=div(row['E_command_effect_RMS'],row['M1_RMS_RMS']);row['I_command_to_M1_window_ratio']=div(row['I_command_effect_RMS'],row['M1_RMS_RMS'])
            bands.append(row)
        fixed=[r for r in bands if r['life']==life and r['band']=='fixed300']
        for store,expr in [('theta_E_norm','E_command_effect'),('theta_I_norm','I_command_effect'),('H_norm','q_norm'),('H_norm','associative_motor_command_effect'),('H_norm','H_use_mean')]:
            x=np.array([r[store+'_mean'] for r in fixed]);y=np.array([r[expr+'_mean'] for r in fixed]);age=np.array([r['start'] for r in fixed]);rx=x-np.polyval(np.polyfit(age,x,1),age);ry=y-np.polyval(np.polyfit(age,y,1),age)
            structure.append(dict(life=life,structure=store,expression=expr,windows=len(x),level_correlation=corr(x,y),first_difference_correlation=corr(np.diff(x),np.diff(y)),linear_age_detrended_correlation=corr(rx,ry)))
        checks.append(dict(life=life,rows=count,cutoff=cut,max_control_alignment_error=float(max(errors)),native_dt_min=float(dt.min()),native_dt_max=float(dt.max()),minimum_local_gain=float(data['local_gain_min'].min())))
        print(life+' functional receivers aligned and reduced',flush=True)
    table('tables/FUNCTIONAL_AGE_BANDS.csv',bands);table('tables/FUNCTIONAL_LOCAL_SLOPES.csv',slopes);table('tables/STRUCTURE_EXPRESSION_ASSOCIATIONS.csv',structure)
    save('FUNCTIONAL_VERIFICATION.json',dict(status='PASS',checks=checks,world_steps=0,RNG_draws=0,alternate_trajectories=0,receiver='detached algebra at stored native operation; no accumulated counterfactual command'))
if __name__=='__main__':main()
