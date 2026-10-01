"""NON-CANONICAL RESURRECTION SANDBOX. Post-stop plain-data observer only."""
from pathlib import Path
import ast,csv,hashlib,json,math,struct,time,zlib
from datetime import datetime,timezone
import numpy as np

OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
PREP=ROOT/'m1_resurrection_sandbox_20260930_v0_1';EX=PREP/'execution'
BASE=ROOT/'worktrees/loom-contact-release-20260930/developmental_ecology'
LABEL='NON-CANONICAL RESURRECTION SANDBOX'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def plain(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [plain(v) for v in x]
    return x
def save(name,value):
    (OUT/name).write_text(json.dumps(plain(value),indent=2,allow_nan=False)+'\n',encoding='utf8')
def csvsave(name,rows):
    if not rows:return
    rows=[dict(sandbox_status=LABEL,**r) for r in rows]
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with (OUT/name).open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,keys);w.writeheader();w.writerows(plain(rows))
def attrs(x):return x['attributes']
def norm(x):return float(np.linalg.norm(x))
def stats(x):
    a=np.asarray(x,dtype=float)
    return dict(n=a.size,min=float(a.min()),median=float(np.median(a)),mean=float(a.mean()),max=float(a.max()),rms=float(np.sqrt(np.mean(a*a)))) if a.size else None
def shape_change(now,birth):
    n=np.asarray(now).ravel();b=np.asarray(birth).ravel();bb=float(b@b);nn=norm(n)
    scale=float(n@b/bb) if bb else 0.
    return dict(best_birth_scale=scale,residual_from_scaled_birth=norm(n-scale*b),
        relative_directional_residual=norm(n-scale*b)/nn if nn else None,
        cosine_with_birth=float(n@b/(nn*math.sqrt(bb))) if nn and bb else None)

decoder=OUT/'passive_reference_sources/audit_exploration.py'
node=next(n for n in ast.parse(decoder.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='read_data')
U=struct.Struct('<Q');F=struct.Struct('<d')
exec(compile(ast.Module(body=[node],type_ignores=[]),str(decoder),'exec'))
schema_file=BASE/'loom_developmental/evidence.py'
schema=next(n.value for n in ast.parse(schema_file.read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NATIVE_FIELDS' for t in n.targets))
SL={};WIDTH=0
for name,width in ast.literal_eval(schema):SL[name]=slice(WIDTH,WIDTH+width);WIDTH+=width
cfg=json.loads((BASE/'configuration.json').read_bytes())

def checkpoint_summary(e,initial):
    o=attrs(e['organism']);oi=attrs(initial['organism']);a=attrs(o['association']);r=attrs(o['regulator'])
    cort=[]
    for obj,old in zip(o['cortices'],oi['cortices']):
        c=attrs(obj);b=attrs(old)
        cort.append(dict(shared=norm(c['shared']),fine=norm(c['fine']),shared_reference=norm(c['shared_ref']),fine_reference=norm(c['fine_ref']),
            shared_change_from_birth=norm(c['shared']-b['shared']),fine_change_from_birth=norm(c['fine']-b['fine']),
            shared_reference_gap=norm(c['shared']-c['shared_ref']),fine_reference_gap=norm(c['fine']-c['fine_ref']),
            fine_row_dispersion=norm(c['fine']-np.mean(c['fine'],axis=0)),activity=norm(c['x']),
            shared_shape=shape_change(c['shared'],b['shared']),fine_shape=shape_change(c['fine'],b['fine'])))
    hv=list(a['H'].values());uv=np.concatenate(list(a['use'].values()))
    return dict(age=e['time'],index=e['native_index'],status=e['status'],resurrections=e['sandbox']['resurrections'],
        E=attrs(e['body'])['energy'],I=attrs(e['body'])['integrity'],cortices=cort,
        H_norm=float(np.sqrt(sum(np.sum(v*v) for v in hv))),use=stats(uv),q_norm=norm(a['q']),a_norm=norm(a['a']),writes=a['write_count'],
        bank_norm=np.linalg.norm(r['theta'],axis=(1,2)),reference_norm=np.linalg.norm(r['reference'],axis=(1,2)),
        bank_reference_gap=np.linalg.norm(r['theta']-r['reference'],axis=(1,2)),eligibility_norm=np.linalg.norm(r['eligibility'],axis=(1,2)),
        current=r['current'],attenuation=r['attenuation'],M1_latent=attrs(o['motor'])['commissioning']['latent'])

def wave_compact(w):
    d=w['motor_coupling'];z=sum(d[k] for k in ('oscillator','direct_feedback','evoked','current'))
    gain=(1-d['attenuation_used'])*(1-np.tanh(z)**2)
    assert np.allclose(np.tanh(z),d['target'],rtol=0,atol=1e-14)
    m=w['map_update_use'];wd=w['map_write_decay'];learn=w['learned'];explore=w['exploration']
    g=len(w['controls'])-4;weighted=w['need'][:,None]*(learn+explore);blind=w['need'][:,None]*explore
    outgoing=cfg['current_max']/2*np.tanh(weighted[:,g:g+2]).sum(axis=0)
    without=cfg['current_max']/2*np.tanh(blind[:,g:g+2]).sum(axis=0)
    assert np.allclose(outgoing,w['controls'][g:g+2],rtol=0,atol=1e-14)
    sigmoid=lambda v:1/(1+np.exp(-v))
    attenuation=sigmoid(cfg['attenuation_bias']+weighted[:,g+2:g+4].sum(axis=0))
    attenuation_without=sigmoid(cfg['attenuation_bias']+blind[:,g+2:g+4].sum(axis=0))
    assert np.allclose(attenuation,w['controls'][-2:],rtol=0,atol=1e-14)
    return dict(age=w['time'],index=w['index'],wave=w['wave'],oscillator_rms=float(np.sqrt(np.mean(d['oscillator']**2))),
        direct_rms=float(np.sqrt(np.mean(d['direct_feedback']**2))),evoked_rms=float(np.sqrt(np.mean(d['evoked']**2))),
        current_rms=float(np.sqrt(np.mean(d['current']**2))),min_gain=float(gain.min()),mean_gain=float(gain.mean()),
        learned_logit_norm=norm(learn),exploration_logit_norm=norm(explore),q_norm=norm(w['q']),
        outgoing_current_rms=float(np.sqrt(np.mean(outgoing**2))),
        learned_current_algebraic_delta_rms=float(np.sqrt(np.mean((outgoing-without)**2))),
        learned_attenuation_algebraic_delta_rms=float(np.sqrt(np.mean((attenuation-attenuation_without)**2))),
        H_norm=norm(m[:,:4]),use_mean=float(m[:,4:].mean()),use_max=float(m[:,4:].max()),
        write_norm=norm(wd[:,:4]),decay_norm=norm(wd[:,4:]),bank_E=float(w['regulator_bank_norm'][0]),bank_I=float(w['regulator_bank_norm'][1]),
        reference_E=float(w['regulator_reference_norm'][0]),reference_I=float(w['regulator_reference_norm'][1]),
        eligibility_E=float(w['regulator_eligibility_norm'][0]),eligibility_I=float(w['regulator_eligibility_norm'][1]),
        trend_E=float(w['credit_trend'][0]),trend_I=float(w['credit_trend'][1]),
        learning_E=float(w['regulator_learning_norm'][0]),learning_I=float(w['regulator_learning_norm'][1]),
        sensory_shared_norm=w['sensory_shared_norm'],sensory_fine_norm=w['sensory_fine_norm'],
        sensory_reference_norm=w['sensory_reference_norm'],sensory_activity_norm=w['sensory_activity_norm'])

def kinematics(native,body):
    t=native[:,0];dt=native[:,1];p=np.vstack((body['position'],native[:,SL['position']]))
    length=np.cumsum(np.r_[0,np.linalg.norm(np.diff(p,axis=0),axis=1)])
    excursion=np.maximum.accumulate(np.linalg.norm(p-p[0],axis=1));displacement=float(np.linalg.norm(p[-1]-p[0]))
    grids={};growth={}
    for size in (.25,1.):
        cells=np.floor(p/size).astype(int);seen=set();old=None;entries=returns=0;hist=[];eh=[];rh=[]
        for cell in map(tuple,cells):
            if cell!=old:
                if old is not None:entries+=1;returns+=cell in seen
                seen.add(cell);old=cell
            hist.append(len(seen))
            eh.append(entries);rh.append(returns)
        grids[str(size)]=dict(visited=len(seen),entries=entries,reentries=returns,reentry_fraction=returns/entries if entries else None)
        growth[str(size)]=np.array(hist)
        growth[str(size)+'_entries']=np.array(eh);growth[str(size)+'_reentries']=np.array(rh)
    vel=native[:,SL['velocity']];ang=native[:,SL['angle']][:,0];omega=native[:,SL['omega']][:,0]
    speed=np.linalg.norm(vel,axis=1);vf=np.sum(vel*np.column_stack((np.cos(ang),np.sin(ang))),axis=1)
    commands=native[:,SL['commands']];duration=float(dt.sum());avg=lambda x:float(np.dot(dt,x)/duration)
    bt=[]
    for sign in (1,-1):
        z=np.r_[False,sign*vf>.01,False];s=np.flatnonzero(z[1:]&~z[:-1]);en=np.flatnonzero(~z[1:]&z[:-1]);tt=np.r_[0,t]
        bt.extend(dict(start=float(tt[i]),end=float(tt[j]),duration=float(tt[j]-tt[i]),sign=sign,end_censored=bool(j==len(t))) for i,j in zip(s,en))
    bt.sort(key=lambda x:x['start']);q=[r for r in bt if r['duration']>=.1-1e-9]
    windows=[]
    for hi in list(np.arange(60,t[-1],60))+[float(t[-1])]:
        lo=max(0,60*math.floor((hi-1e-8)/60));i=np.searchsorted(t,lo,side='right');j=np.searchsorted(t,hi,side='right')
        if j<=i:continue
        sl=slice(i,j);dd=dt[sl];wt=lambda x:float(np.dot(dd,x[sl])/dd.sum())
        windows.append(dict(start=lo,end=hi,path=float(length[j]-length[i]),maximum_birth_excursion=float(excursion[j]),
            displacement_from_window_start=float(np.linalg.norm(p[j]-p[i])),new_cells025=int(growth['0.25'][j]-growth['0.25'][i]),
            total_cells025=int(growth['0.25'][j]),mean_speed=wt(speed),mean_abs_omega=wt(abs(omega)),
            entries025=int(growth['0.25_entries'][j]-growth['0.25_entries'][i]),
            reentries025=int(growth['0.25_reentries'][j]-growth['0.25_reentries'][i]),
            effort=cfg['effort_cost']*float(np.dot(dd,abs(commands[sl]).mean(axis=1)))))
    sample=np.unique(np.r_[np.searchsorted(t,np.arange(.1,t[-1],.1)),len(t)-1]);sample=sample[sample<len(t)]
    direction=[]
    vv=vel[sample];ss=speed[sample];aa=ang[sample]
    for lag in (.1,1.,4.,8.,16.):
        k=round(lag/.1)
        if len(sample)<=k:continue
        ok=(ss[k:]>.01)&(ss[:-k]>.01)
        direction.append(dict(lag=lag,heading=float(np.cos(aa[k:]-aa[:-k]).mean()),
            velocity_direction=float(np.mean(np.sum(vv[k:][ok]*vv[:-k][ok],axis=1)/(ss[k:][ok]*ss[:-k][ok]))) if ok.any() else None))
    summary=dict(age=float(t[-1]),native_steps=len(t),path=float(length[-1]),maximum_excursion=float(excursion[-1]),displacement=displacement,
        displacement_path_ratio=displacement/length[-1] if length[-1] else None,grids=grids,mean_speed=avg(speed),mean_abs_omega=avg(abs(omega)),
        common_rms=math.sqrt(avg(commands.mean(axis=1)**2)),differential_rms=math.sqrt(avg(((commands[:,1]-commands[:,0])/2)**2)),
        forward_bouts=stats([b['duration'] for b in q if b['sign']==1]),reverse_bouts=stats([b['duration'] for b in q if b['sign']==-1]),
        switches=sum(a['sign']!=b['sign'] for a,b in zip(q,q[1:])),persistence=direction,windows=windows)
    idx=np.unique(np.r_[0,1+sample]);plot=dict(time=np.r_[0,t][idx],position=p[idx],angle=np.r_[body['angle'],ang][idx],
        reserves=np.vstack(([body['energy'],body['integrity']],native[:,SL['reserves']]))[idx],stocks=np.vstack((native[0,SL['stocks']],native[:,SL['stocks']]))[idx],
        excursion=excursion[idx],path=length[idx],coverage=growth['0.25'][idx])
    return summary,plot

class Physical:
    def __init__(self):
        self.expense=0.;self.damage=0.;self.repair=0.;self.transfer=np.zeros(8);self.impulse=0.;self.ledger_max=0.
        self.episodes=[];self.last={};self.bins={};self.count=0
    def consume(self,r):
        self.count+=1;tr=np.asarray(r['transfer']);renew=np.asarray(r['renewal_first'])+r['renewal_second']
        errs=[(r['energy_after']-r['energy_before'])-(tr.sum()-r['expenditure']),
            np.max(abs(np.asarray(r['stock_after'])-r['stock_before']-renew+tr)),r['integrity_after']-r['integrity_before']-(r['repair']-r['damage'])]
        self.ledger_max=max(self.ledger_max,*map(abs,errs));assert self.ledger_max<=cfg['arithmetic_tol']
        self.expense+=r['expenditure'];self.damage+=r['damage'];self.repair+=r['repair'];self.transfer+=tr
        binno=int(max(0,r['time']-1e-10)//60)
        b=self.bins.setdefault(binno,dict(start=60*binno,end=60*(binno+1),expenditure=0.,damage=0.,repair=0.,transfer=0.,impulse=0.))
        for k,key in [('expenditure','expenditure'),('damage','damage'),('repair','repair')]:b[k]+=r[key]
        b['transfer']+=float(tr.sum())
        for c in r['contacts']:
            cid=c['collider'];dt=r['duration'];start=r['time']-dt;imp=c['impulse'];self.impulse+=imp;b['impulse']+=imp
            old=self.last.get(cid)
            if old is None or start>old['end']+1e-8:
                old=dict(collider=cid,start=start,end=r['time'],duration=0.,impulse=0.,damage=0.,transfer=0.,repair=0.,rows=0,
                    start_position=r['body_position'],last_position=r['body_position'],first_relative_speed=c['relative_speed'],
                    peak_relative_speed=0.,peak_impulse=0.,peak_sustained_force=0.,impact_rows=0);self.episodes.append(old);self.last[cid]=old
            old['end']=r['time'];old['duration']+=dt;old['rows']+=1;old['impulse']+=imp;old['last_position']=r['body_position']
            old['peak_relative_speed']=max(old['peak_relative_speed'],c['relative_speed']);old['peak_impulse']=max(old['peak_impulse'],imp)
            old['impact_rows']+=int(r['impact'])
            if not r['impact'] and dt>0:old['peak_sustained_force']=max(old['peak_sustained_force'],imp/dt)
            old['damage']+=cfg['damage_per_impulse']*(imp if r['impact'] else max(0,imp-cfg['stress_threshold']*dt))
            if cid.startswith('source-'):
                old['transfer']+=float(tr[int(cid.split('-')[-1])])
            if cid.startswith('repair'):old['repair']+=r['repair']
    def result(self):
        return dict(expenditure=self.expense,damage=self.damage,repair=self.repair,transfer_by_source=self.transfer,source_transfer=float(self.transfer.sum()),
            impulse=self.impulse,ledger_max=self.ledger_max,event_rows=self.count,episodes=self.episodes,windows=list(self.bins.values()))

def main():
    began=time.perf_counter();denpath=EX/'DENOMINATOR.json'
    if not denpath.exists():denpath=OUT/'HOST_STOP_DENOMINATOR.json'
    assert denpath.exists(),'Observer requires stopped executor or documented terminated host failure'
    den=json.loads(denpath.read_bytes());assert (EX/'STOP.json').exists() or (EX/'COMPLETED.json').exists() or (OUT/'HOST_STOP.json').exists()
    files=[dict(path=p.relative_to(EX).as_posix(),bytes=p.stat().st_size,sha256=h(p)) for p in sorted(EX.rglob('*')) if p.is_file()]
    seal=dict(label=LABEL,utc=datetime.now(timezone.utc).isoformat(),files=files,bytes=sum(x['bytes'] for x in files),denominator_sha256=h(denpath))
    sealpath=OUT/'EXECUTION_CUSTODY_SEAL.json'
    if sealpath.exists():
        old=json.loads(sealpath.read_bytes());assert old['files']==files
    else:save(sealpath.name,seal)
    hashes={x['path']:x['sha256'] for x in files}
    def rd(p):return read_data(p,hashes[p.relative_to(EX).as_posix()])
    results=[];table=[];checks=[]
    for row in den['rows']:
        name=row['life_id'];store=EX/'lives'/name
        if not store.exists():results.append(dict(label=LABEL,life_id=name,status='UNSTARTED'));table.append(dict(life_id=name,status='UNSTARTED',age=0.));continue
        initial=attrs(rd(next(store.glob('pilot-*-pilot-initial.ld')))['engine']);body=attrs(initial['body'])
        chunks=[];waves=[];physical=Physical();t=0.;index=0;interventions=[]
        for p in sorted(store.glob('resurrection-*.ld')):
            x=rd(p)['intervention'];interventions.append(x)
        for p in sorted(store.glob('chunk-*.ld')):
            v=rd(p);assert v['start_time']==t and v['first_index']==index+1
            a=v['native'];chunks.append(a)
            for r in a:t+=float(r[1]);index+=1;assert t==r[0]
            for w in v['waves']:waves.append(wave_compact(w))
            for event in v['events']:physical.consume(event)
            assert index==v['last_index']
        tails=sorted(store.glob('*-failure-tail.ld'));full_endpoint=True
        if tails:
            assert len(tails)==1;tail=rd(tails[0]);final=attrs(tail['engine']);a=tail['unclosed_native']
            if len(a):
                chunks.append(a)
                for r in a:t+=float(r[1]);index+=1;assert t==r[0]
            for w in tail['unclosed_waves']:waves.append(wave_compact(w))
            for event in tail['unclosed_events']:physical.consume(event)
            status='DECLARED_SANDBOX_STOP'
        elif row['overnight']=='HOST_NATIVE_CRASH_DURABLE_PREFIX':
            final=attrs(rd(store/row['last_full_checkpoint'])['engine']);status='HOST_NATIVE_CRASH_DURABLE_PREFIX';full_endpoint=False
        else:
            stage='overnight' if (store/'overnight-RECEIPT.json').exists() else 'pilot'
            rec=json.loads((store/(stage+'-RECEIPT.json')).read_bytes());final=attrs(rd(store/rec['final_checkpoint']['file'])['engine']);status=stage.upper()+'_COMPLETE'
        if not index:
            results.append(dict(label=LABEL,life_id=name,status=status,age=0.));table.append(dict(life_id=name,status=status,age=0.));continue
        native=np.concatenate(chunks);assert native.shape==(index,WIDTH) and np.isfinite(native).all()
        if full_endpoint:assert index==final['native_index'] and t==final['time'] and len(waves)==attrs(final['organism'])['wave_count']
        else:
            assert index==row['last_durable_native_index'] and t==row['last_age']
            assert final['native_index']<index and final['time']<t
            assert sum(w['index']<=final['native_index'] for w in waves)==attrs(final['organism'])['wave_count']
        assert [w['wave'] for w in waves]==list(range(1,len(waves)+1))
        assert all(w['index']<=index for w in waves)
        assert int(native[:,SL['event_count']].sum())==physical.count
        support=sum((x['external_support'] for x in interventions),np.zeros(2));fb=attrs(final['body']) if full_endpoint else dict(
            energy=float(native[-1,SL['reserves']][0]),integrity=float(native[-1,SL['reserves']][1]),position=native[-1,SL['position']])
        balance=np.array([fb['energy']-body['energy']-support[0]-physical.transfer.sum()+physical.expense,
            fb['integrity']-body['integrity']-support[1]+physical.damage-physical.repair]);assert abs(balance).max()<1e-9
        assert np.array_equal(native[-1,SL['position']],fb['position'])
        k,plot=kinematics(native,body);np.savez_compressed(OUT/(name+'_PLOT_DATA.npz'),sandbox_status=np.array(LABEL),**plot)
        histories=[]
        for p in sorted(store.glob('*.ld')):
            if p.name.startswith('chunk-') or p.name.startswith('resurrection-') or 'failure-tail' in p.name:continue
            v=rd(p)
            if 'engine' in v:histories.append(dict(file=p.name,**checkpoint_summary(attrs(v['engine']),initial)))
        histories.append(dict(file='authoritative-final' if full_endpoint else 'last-full-checkpoint-not-endpoint',**checkpoint_summary(final,initial)));histories.sort(key=lambda x:(x['age'],x['file']))
        iw=[dict(time=x['time'],index=x['index'],ordinal=x['ordinal'],restored_dimensions=x['restored_dimensions'],external_support=x['external_support'],
            before_reserves=x['old_transients']['reserves'],after_reserves=x['restored_reserves'],
            discarded_partial_seconds=x['old_transients']['wave_elapsed'],zero_learning_from_jump=x['zero_learning_from_jump'],protected_sha256=x['protected_sha256']) for x in interventions]
        ww=[]
        for lo in range(0,int(math.ceil(t/60))*60,60):
            w=[x for x in waves if lo<x['age']<=lo+60]
            if not w:continue
            metrics={key:stats([x[key] for x in w]) for key in w[0] if key not in ('age','index','wave') and np.isscalar(w[0][key])}
            ww.append(dict(start=lo,end=min(lo+60,t),waves=len(w),metrics=metrics))
        result=dict(label=LABEL,life_id=name,status=status,age=t,kinematics=k,physical=physical.result(),resurrections=iw,support=support,
            complete_causal_state_at_endpoint=full_endpoint,last_complete_checkpoint_age=final['time'],last_complete_checkpoint_index=final['native_index'],
            accounting_residual=balance,wave_windows=ww,checkpoint_history=histories,first_wave=waves[0] if waves else None,last_wave=waves[-1] if waves else None)
        save(name+'_DETAILS.json',result);csvsave(name+'_WAVE_HISTORY.csv',[{k:v for k,v in w.items() if np.isscalar(v)} for w in waves])
        results.append(result);table.append(dict(life_id=name,status=status,age=t,native_steps=index,waves=len(waves),resurrections=len(iw),
            external_E=float(support[0]),external_I=float(support[1]),path=k['path'],maximum_excursion=k['maximum_excursion'],coverage025=k['grids']['0.25']['visited'],
            recurrence025=k['grids']['0.25']['reentry_fraction'],expenditure=physical.expense,source_transfer=float(physical.transfer.sum()),damage=physical.damage,repair=physical.repair,final_E=fb['energy'],final_I=fb['integrity']))
        checks.append(dict(life_id=name,rows=index,waves=len(waves),events=physical.count,accounting_residual=balance,ledger_max=physical.ledger_max,
            complete_causal_state_at_endpoint=full_endpoint,last_complete_checkpoint_age=final['time']))
        print(json.dumps(dict(label=LABEL,event='PASSIVE_LIFE_COMPLETE',life=name,age=t)),flush=True)
    save('PASSIVE_RESULTS.json',dict(label=LABEL,denominator=den,lives=results));csvsave('ALL_TWELVE_DISPOSITIONS.csv',table)
    assert all(h(EX/x['path'])==x['sha256'] for x in files)
    save('PASSIVE_VERIFICATION.json',dict(label=LABEL,status='PASS',checks=checks,execution_bytes_unchanged=True,new_simulation_steps=0,
        decoder_source_sha256=h(decoder),schema_source_sha256=h(schema_file),observer_wall_seconds=time.perf_counter()-began))
if __name__=='__main__':main()
