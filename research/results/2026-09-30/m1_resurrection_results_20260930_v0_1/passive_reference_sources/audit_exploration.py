"""Passive native-record exploration audit. Never imports Loom or evolves state."""
from pathlib import Path
import hashlib,json,math,struct,zlib,time,csv,ast,shutil
import numpy as np

OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
D=ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'
PREV=ROOT/'founder_expansion_execution_20260930'
cfg=json.loads((D/'configuration.json').read_text())
roster=json.loads((PREV/'analysis/ALL_SIXTY_AB.json').read_text())

# Preserve the already drafted design, without treating it as approved.
draft=OUT/'provisional_pre_exploration';draft.mkdir(exist_ok=True)
for name in ('NURSERY_0_DESIGN_v0_1.md','NURSERY_CANDIDATE_PROPOSALS.json','NURSERY_0_STATIC_LAYOUT.svg','CURRENT_WORLD_DEVELOPMENTAL_EVIDENCE.md','INTEGRITY_PATHWAY_EVIDENCE_SUMMARY.md','LEAN_RUNNER_RESOURCE_ESTIMATE.md'):
    if not (draft/name).exists():shutil.copyfile(OUT/name,draft/name)

METHODS='''# Exploration audit methods — fixed before reading native movement results

Passive extraction only. Use all 60 existing trajectories, with FS-060 prefix separate and a fixed 59-complete-life denominator for pooled biological histories. Read native physical records at original 0.01 s fidelity and initial checkpoint as data; no P import, object reinstantiation, RNG, motor generator or dynamics execution. Verify each input file/payload checksum. Heading/direction correlations and time-lag MSD use deterministic 0.1 s sampling to reduce observer work, not recording fidelity.

Report displacement/max excursion, native polyline distance, actual saved endpoint translational/angular velocity, forward/lateral velocity in the saved heading frame, commands and contacts. Age panels: 0–60, 60–120, 120–180, 180–240, 240–300, 300–360, 360–420 and final partial block. Compare early and late panels; do not label a whole-life statistic purely newborn.

MSD: (a) birth-relative squared displacement at 1/2/5/10/20/30/60/120/180/240/300/360/420 s; (b) each life's time-averaged squared displacement at fixed lags. No extrapolation of diffusion coefficient or infinite behavior. Averages across lives are not independent within-life samples.

Persistence: heading cos-difference and normalized velocity-direction dot product at fixed lags 0…20 s by 0.1 s then 21…120 s by 1 s. Velocity directions require both speeds >0.01. First correlation crossing below 1/e is an oscillatory first-crossing descriptor, not an exponential-fit persistence constant. No crossing means right-censored at 120 s. All-life and first-60-s curves retained.

Forward/reverse bouts: contiguous saved body-forward velocity >0.01 / <−0.01. Report all lengths plus count lasting ≥0.1 s. Reversals: alternate forward/reverse bouts each lasting ≥0.1 s, ignoring intervening deadband. Fixed sensitivity thresholds 0.005/0.02. No direction inferred from the sign of angular speed alone. Command correlation is ordinary Pearson left/right, separately common/differential RMS and same/opposite signs.

Activity: active if speed or body-edge rotational speed r|omega| exceeds 0.005. Predominantly rotation if r|omega|>2*speed; predominantly translation if speed>2*r|omega|; otherwise mixed. Fractions are time weighted. This is a kinematic ratio, not an intention or an energy-cost decomposition. Report thresholds, do not treat the fractions as universal categories.

Path curvature: change in saved velocity direction / native path length, excluding endpoints with speed≤0.01; retain median and 90th percentile and total absolute direction change per accepted distance. Also report body-heading change separately; reversals are not assumed to be turning in place. Near-zero denominators excluded and counted.

Coverage/recurrence: world-aligned square bins at side 0.25 and 1; count visited bins versus age, distinct-bin re-entry after leaving, and fraction of cell transitions entering an already visited bin. A within-bin step is not a new entry. Report 0.25-grid half-bin-offset sensitivity. Spatial occupancy is not swept body coverage. No visited-space information feeds P.

Trapping: saved positive contact impulse/rate, wall gap, mover gap and nearest static fixture gap; report time within 0.25/0.5 of a surface. Compare all complete lives with no-positive-contact complete lives. Local motion without contact weakens hard-collision trapping as a necessary explanation; it does not eliminate visual/chemical feedback or other environmental influence. No causal motor omission/alternative trajectory is authorized or performed.

The old source-density layout is preserved as provisional. Only findings material to mechanism-versus-opportunity interpretation may alter the design recommendation; no numerical motor option is tested or fitted here.
'''
(OUT/'EXPLORATION_AUDIT_METHODS.md').write_text(METHODS,encoding='utf-8')

fields=next(n.value for n in ast.parse((D/'loom_developmental/evidence.py').read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NATIVE_FIELDS' for t in n.targets))
fields=ast.literal_eval(fields);SL={};width=0
for name,n in fields:SL[name]=slice(width,width+n);width+=n
assert width==76
U=struct.Struct('<Q');F=struct.Struct('<d')
def read_data(path,expected=None,native_only=False):
    b=path.read_bytes()
    if expected:assert hashlib.sha256(b).hexdigest()==expected,str(path)
    assert b[:8]==b'LOOMDEV1' and b[8]<=9
    size=U.unpack(b[9:17])[0];assert size<=512000000
    if b[8]:
        dec=zlib.decompressobj();raw=dec.decompress(b[49:],size+1)
        assert dec.eof and not dec.unused_data and not dec.unconsumed_tail
    else:raw=b[49:]
    assert len(raw)==size and hashlib.sha256(raw).digest()==b[17:49]
    view=memoryview(raw);offset=0
    def take(n):
        nonlocal offset
        assert 0<=n<=len(view)-offset
        x=view[offset:offset+n];offset+=n;return x
    def count():return U.unpack(take(8))[0]
    def get(depth=0):
        assert depth<=100
        tag=bytes(take(1))
        if tag==b'n':return None
        if tag==b't':return True
        if tag==b'f':return False
        if tag==b'r':return F.unpack(take(8))[0]
        if tag in (b's',b'b',b'i'):
            x=bytes(take(count()));return x if tag==b'b' else int(x) if tag==b'i' else x.decode('utf-8')
        if tag in (b'l',b'u'):
            x=[get(depth+1) for _ in range(count())];return x if tag==b'l' else tuple(x)
        if tag==b'd':
            x={}
            for _ in range(count()):
                k=get(depth+1);assert k not in x;x[k]=get(depth+1)
                if native_only and depth==0 and k=='native':return x
            return x
        if tag==b'/':return {'stored_slice':get(depth+1)}
        if tag==b'a':
            dt=np.dtype(get(depth+1));shape=get(depth+1);n=count()
            assert dt.kind in 'fiu' and n==math.prod(shape)*dt.itemsize
            return np.frombuffer(take(n),dt).reshape(shape).copy()
        if tag==b'o':
            return {'stored_class':get(depth+1),'attributes':get(depth+1)}
        raise ValueError(tag)
    val=get()
    if not native_only:assert offset==len(view)
    return val

def plain(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    if isinstance(x,dict):return {k:plain(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [plain(v) for v in x]
    return x
def save(name,x): (OUT/name).write_text(json.dumps(plain(x),indent=2,allow_nan=False)+'\n',encoding='utf-8')
def table(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def stat(a):
    a=np.asarray(a);return dict(mean=float(np.mean(a)),median=float(np.median(a)),minimum=float(np.min(a)),maximum=float(np.max(a))) if len(a) else None
def runs(mask,dt):
    p=np.r_[False,mask,False];starts=np.flatnonzero(p[1:]&~p[:-1]);ends=np.flatnonzero(~p[1:]&p[:-1]);cs=np.r_[0,np.cumsum(dt)]
    return starts,ends,cs[ends]-cs[starts]
def bouts(vf,dt,threshold):
    a,b,d=runs(vf>threshold,dt);c,e,f=runs(vf< -threshold,dt)
    sign=[(int(s),1) for s,du in zip(a,d) if du>=.1-1e-9]+[(int(s),-1) for s,du in zip(c,f) if du>=.1-1e-9]
    sign.sort();seq=[v for _,v in sign]
    reversals=sum(x!=y for x,y in zip(seq[:-1],seq[1:]))
    return dict(forward_count=len(d),forward_count_ge01=int(np.sum(d>=.1-1e-9)),forward_median=float(np.median(d)) if len(d) else 0.,forward_max=float(np.max(d)) if len(d) else 0.,reverse_count=len(f),reverse_median=float(np.median(f)) if len(f) else 0.,reverse_max=float(np.max(f)) if len(f) else 0.,reversals=reversals,reversals_per_minute=reversals/(dt.sum()/60))
def grid_metrics(p,size,offset=0.):
    codes=np.floor((p+offset)/size).astype(int);seen=set();entries=returns=0;prior=None;growth=[]
    for x,y in codes:
        cell=(int(x),int(y))
        if cell!=prior:
            if prior is not None:
                entries+=1;returns+=cell in seen
            seen.add(cell);prior=cell
        growth.append(len(seen))
    return dict(visited=len(seen),transitions=entries,return_transitions=returns,return_fraction=returns/entries if entries else None),np.array(growth)
def correlation_curves(p,angle,v,time_mask=None):
    q=p[::10];a=angle[::10];vv=v[::10]
    if time_mask is not None:q=q[time_mask];a=a[time_mask];vv=vv[time_mask]
    sp=np.linalg.norm(vv,axis=1);unit=vv/np.maximum(sp[:,None],1e-300)
    lags=list(range(0,201))+list(range(210,1201,10));out=[]
    for lag in lags:
        if lag>=len(q):continue
        if lag==0:head=direction=1.;msd=0.;count=int(np.sum(sp>.01))
        else:
            head=float(np.cos(a[lag:]-a[:-lag]).mean())
            ok=(sp[lag:]>.01)&(sp[:-lag]>.01);count=int(ok.sum())
            direction=float(np.einsum('ij,ij->i',unit[lag:][ok],unit[:-lag][ok]).mean()) if count else None
            msd=float(np.sum((q[lag:]-q[:-lag])**2,axis=1).mean())
        out.append(dict(lag_s=lag/10,heading_acf=head,direction_acf=direction,direction_pairs=count,time_averaged_msd=msd))
    return out
def firstcross(curve,key):
    for r in curve:
        if r[key] is not None and r[key]<=1/math.e:return r['lag_s']
    return None

all_rows=[];all_blocks=[];all_ages=[];all_correlations=[];nfiles=0;totalsteps=0;began=time.perf_counter()
for r in roster:
    name=r['life_id'];base=ROOT/('founder_initial_execution_20260930' if int(name[3:])<13 else 'founder_expansion_execution_20260930');store=base/'lives'/name
    if r['complete']:receipt=json.loads((store/'segment-000.json').read_text());refs=receipt['chunks'];cp=receipt['initial_checkpoint']
    else:
        refs0=json.loads((base/'INTERRUPTION_CUSTODY_SEAL.json').read_text())['files'];refs=sorted((z for z in refs0 if z['file'].startswith('chunk-')),key=lambda z:z['file']);cp=next(z for z in refs0 if z['file'].endswith('-initial.ld'))
    initial=read_data(store/cp['file'],cp['sha256'])['engine']['attributes'];body=initial['body']['attributes'];p0=np.array(body['position']);angle0=body['angle']
    native=[];index=0
    for ref in refs:
        q=read_data(store/ref['file'],ref['sha256'],True);assert q['first_index']==index+1
        a=q['native'];assert a.ndim==2 and a.shape[1]==width and np.isfinite(a).all()
        index=q['last_index'];assert index==q['first_index']+len(a)-1
        native.append(a);nfiles+=1
    a=np.concatenate(native);totalsteps+=len(a)
    t=a[:,SL['time']].ravel();dt=a[:,SL['elapsed']].ravel();p=a[:,SL['position']];v=a[:,SL['velocity']];angle=a[:,SL['angle']].ravel();omega=a[:,SL['omega']].ravel();u=a[:,SL['commands']]
    dp=np.diff(np.vstack((p0,p)),axis=0);ds=np.linalg.norm(dp,axis=1);path=float(ds.sum());assert abs(path-r['path_length'])<1e-8
    speed=np.linalg.norm(v,axis=1);vf=v[:,0]*np.cos(angle)+v[:,1]*np.sin(angle);vl=-v[:,0]*np.sin(angle)+v[:,1]*np.cos(angle)
    rot=.5*abs(omega);active=(speed>.005)|(rot>.005);predrot=active&(rot>2*speed);predtrans=active&(speed>2*rot)
    impulse=np.any(a[:,SL['contact_rates']]>1e-12,axis=1)
    wall=np.minimum.reduce((p[:,0]-.5,19.5-p[:,0],p[:,1]-.5,19.5-p[:,1]))
    near=wall.copy()
    for x,y in cfg['source_positions']:near=np.minimum(near,np.hypot(p[:,0]-x,p[:,1]-y)-1.)
    for x0,x1,y0,y1 in cfg['repair_rectangles']:
        near=np.minimum(near,np.hypot(np.maximum(np.maximum(x0-p[:,0],p[:,0]-x1),0),np.maximum(np.maximum(y0-p[:,1],p[:,1]-y1),0))-.5)
    rect=a[:,SL['mover_rectangle']]
    mg=np.hypot(np.maximum(np.maximum(rect[:,0]-p[:,0],p[:,0]-rect[:,1]),0),np.maximum(np.maximum(rect[:,2]-p[:,1],p[:,1]-rect[:,3]),0))-.5
    near=np.minimum(near,mg)
    gr,growth=grid_metrics(np.vstack((p0,p)),.25);gr1,growth1=grid_metrics(np.vstack((p0,p)),1.);gro,_=grid_metrics(np.vstack((p0,p)),.25,.125)
    cv=correlation_curves(p,angle,v);early=correlation_curves(p,angle,v,t[::10]<=60)
    direction=np.arctan2(v[:,1],v[:,0]);turn=np.abs(np.angle(np.exp(1j*np.diff(direction))))
    ok=(speed[1:]>.01)&(speed[:-1]>.01)&(ds[1:]>1e-12)
    curv=turn[ok]/ds[1:][ok]
    dur=float(dt.sum());weight=lambda x:float(np.dot(np.asarray(x,float),dt)/dur)
    raw=dict(life_id=name,complete=r['complete'],duration_s=dur,path_length=path,max_excursion=float(np.linalg.norm(p-p0,axis=1).max()),final_displacement=float(np.linalg.norm(p[-1]-p0)),mean_speed=weight(speed),rms_speed=math.sqrt(weight(speed**2)),mean_abs_omega=weight(abs(omega)),rms_omega=math.sqrt(weight(omega**2)),heading_total_abs_rotation=float(np.abs(np.diff(np.r_[angle0,angle])).sum()),mean_forward_velocity=weight(vf),mean_abs_forward_velocity=weight(abs(vf)),mean_abs_lateral_velocity=weight(abs(vl)),forward_time_fraction=weight(vf>.01),reverse_time_fraction=weight(vf<-.01),rotation_dominant_time_fraction=weight(predrot),translation_dominant_time_fraction=weight(predtrans),mixed_active_time_fraction=weight(active&~predrot&~predtrans),inactive_time_fraction=weight(~active),left_right_command_correlation=float(np.corrcoef(u.T)[0,1]),common_command_rms=math.sqrt(weight(((u[:,0]+u[:,1])/2)**2)),differential_command_rms=math.sqrt(weight(((u[:,1]-u[:,0])/2)**2)),opposed_commands_time_fraction=weight(u[:,0]*u[:,1]<0),positive_contact_time_fraction=weight(impulse),positive_contact_native_count=int(impulse.sum()),near_wall_025_time_fraction=weight(wall<=.25),near_wall_05_time_fraction=weight(wall<=.5),near_any_fixture_025_time_fraction=weight(near<=.25),near_any_fixture_05_time_fraction=weight(near<=.5),minimum_fixture_gap=float(near.min()),heading_acf_first_1e_s=firstcross(cv,'heading_acf'),direction_acf_first_1e_s=firstcross(cv,'direction_acf'),early_heading_acf_first_1e_s=firstcross(early,'heading_acf'),early_direction_acf_first_1e_s=firstcross(early,'direction_acf'),curvature_median=float(np.median(curv)),curvature_p90=float(np.quantile(curv,.9)),absolute_path_direction_turn_per_length=float(turn[ok].sum()/ds[1:][ok].sum()),curvature_valid_native_fraction=float(ok.mean()),coverage025=gr['visited'],coverage1=gr1['visited'],coverage025_offset=gro['visited'],reentry025_fraction=gr['return_fraction'],reentry025_transitions=gr['transitions'],reentry1_fraction=gr1['return_fraction'],reentry025_offset_fraction=gro['return_fraction'])
    bout=bouts(vf,dt,.01);raw.update(bout)
    save(name+'_EXPLORATION_DETAILS.json',dict(summary=raw,bout_sensitivity={str(th):bouts(vf,dt,th) for th in (.005,.01,.02)},correlations=cv,early_correlations=early,coverage025=gr,coverage1=gr1,coverage_offset=gro))
    all_rows.append(raw)
    for c in cv:all_correlations.append(dict(life_id=name,complete=r['complete'],**c))
    for end in [1,2,5,10,20,30,60,120,180,240,300,360,420,dur]:
        if end>dur+1e-8:continue
        idx=min(len(t)-1,max(0,int(round(end/.01))-1))
        all_ages.append(dict(life_id=name,complete=r['complete'],requested_age_s=end,recorded_age_s=float(t[idx]),birth_msd=float(np.sum((p[idx]-p0)**2)),max_excursion=float(np.linalg.norm(p[:idx+1]-p0,axis=1).max()),path=float(ds[:idx+1].sum()),coverage025=int(growth[idx+1]),coverage1=int(growth1[idx+1])))
    for start in range(0,int(math.ceil(dur/60))*60,60):
        mask=(t>start+1e-9)&(t<=start+60+1e-8);d=dt[mask];period=float(d.sum())
        if not period:continue
        w=lambda x:float(np.dot(np.asarray(x)[mask],d)/period)
        all_blocks.append(dict(life_id=name,complete=r['complete'],start_s=start,end_s=min(start+60,dur),sample_duration=period,mean_speed=w(speed),mean_abs_omega=w(abs(omega)),mean_forward_velocity=w(vf),mean_abs_forward_velocity=w(abs(vf)),mean_abs_lateral_velocity=w(abs(vl)),forward_fraction=w(vf>.01),reverse_fraction=w(vf<-.01),rotation_dominant_fraction=w(predrot),translation_dominant_fraction=w(predtrans),contact_fraction=w(impulse),near_wall025_fraction=w(wall<=.25),left_right_command_correlation=float(np.corrcoef(u[mask].T)[0,1]),path=float(ds[mask].sum()),coverage025_end=int(growth[np.flatnonzero(mask)[-1]+1]),coverage1_end=int(growth1[np.flatnonzero(mask)[-1]+1]),reversals=bouts(vf[mask],d,.01)['reversals']))
    # Observer-only display samples, original records remain native fidelity.
    ids=np.unique(np.r_[np.arange(0,len(t),10),len(t)-1])
    np.savez_compressed(OUT/(name+'_PASSIVE_KINEMATICS.npz'),time=t[ids],position=p[ids],angle=angle[ids],velocity=v[ids],omega=omega[ids],commands=u[ids],forward=vf[ids],birth=p0,wall_gap=wall[ids],any_gap=near[ids])
    print(json.dumps(dict(audited=name,steps=len(t),wall_s=round(time.perf_counter()-began,2))),flush=True)

table('EXPLORATION_PER_LIFE.csv',all_rows);table('EXPLORATION_AGE_BLOCKS.csv',all_blocks);table('EXPLORATION_COVERAGE_MSD_BY_AGE.csv',all_ages);table('EXPLORATION_CORRELATIONS_MSD_BY_LAG.csv',all_correlations)
complete=[r for r in all_rows if r['complete']]
no_contact=[r for r in complete if r['positive_contact_native_count']==0]
numeric=[k for k,v in complete[0].items() if isinstance(v,(int,float)) and k not in ('complete',)]
summary={group:{k:stat([r[k] for r in members if r[k] is not None]) for k in numeric} for group,members in [('complete_59',complete),('no_contact',no_contact)]}
summary['n_no_contact']=len(no_contact)
summary['no_contact_never_within_025']=sum(r['minimum_fixture_gap']>.25 for r in no_contact)
summary['FS060_prefix']=all_rows[-1]
summary['age_ensemble']={str(age):{k:stat([r[k] for r in all_ages if r['complete'] and r['requested_age_s']==age]) for k in ('birth_msd','max_excursion','path','coverage025','coverage1')} for age in (1,2,5,10,20,30,60,120,180,240,300,360,420)}
summary['lag_ensemble']={str(lag):{k:stat([r[k] for r in all_correlations if r['complete'] and r['lag_s']==lag and r[k] is not None]) for k in ('heading_acf','direction_acf','time_averaged_msd')} for lag in (0,1,2,3,4,5,7,9,10,15,20,30,60,120)}
summary['age_block_ensemble']={str(start):{k:stat([r[k] for r in all_blocks if r['complete'] and r['start_s']==start]) for k in ('mean_speed','mean_abs_omega','forward_fraction','reverse_fraction','rotation_dominant_fraction','translation_dominant_fraction','contact_fraction','coverage025_end','reversals')} for start in range(0,420,60)}
summary['checks']=dict(native_files_verified=nfiles,native_steps_read=totalsteps,all_native_paths_match_prior=True,world_steps=0,P_steps=0,prehistory_steps=0,world_replay_steps=0,new_random_draws=0,wall_seconds=time.perf_counter()-began)
save('EXPLORATION_AUDIT_RESULTS.json',summary)
print(json.dumps(dict(status='COMPLETE',n_no_contact=len(no_contact),**summary['checks'])),flush=True)
