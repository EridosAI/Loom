"""Read preserved FS births as plain data; static geometry/statistics only. No Loom imports."""
from pathlib import Path
import ast,csv,hashlib,json,math,struct,zlib,time
import numpy as np
OUT=Path(__file__).resolve().parent; ROOT=OUT.parent
OLD=ROOT/'nursery_0_design_20260930_v0_1'
D=ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'
INPUTS={}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def track(p,expected=None):
    p=Path(p);h=sha(p)
    if expected:assert h==expected,str(p)
    INPUTS[p.as_posix()]=h;return p
def read(p):return json.loads(track(p).read_text())
def plain(x):
    if isinstance(x,np.ndarray):return x.tolist()
    if isinstance(x,np.generic):return x.item()
    if isinstance(x,dict):return {k:plain(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [plain(v) for v in x]
    return x
def save(name,x):(OUT/name).write_text(json.dumps(plain(x),indent=2,allow_nan=False)+'\n',encoding='utf-8')
def table(name,rows):
    with (OUT/name).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def stats(x):
    a=np.asarray(x);return dict(n=len(a),minimum=float(a.min()),q25=float(np.quantile(a,.25)),median=float(np.median(a)),q75=float(np.quantile(a,.75)),maximum=float(a.max()),mean=float(a.mean()))

# Reuse only the audited data decoder function, without running its source module.
decoder=track(OLD/'audit_exploration.py')
tree=ast.parse(decoder.read_text());node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='read_data')
ns={'np':np,'math':math,'hashlib':hashlib,'zlib':zlib,'U':struct.Struct('<Q'),'F':struct.Struct('<d')}
exec(compile(ast.Module(body=[node],type_ignores=[]),'passive_decoder','exec'),ns)
read_data=ns['read_data']
c=read(D/'configuration.json'); sources=np.array(c['source_positions']);repairs=np.array(c['repair_rectangles'])
for name in ('engine.py','geometry.py','schema.py','prehistory.py','neural.py','physics.py'):
    track(D/'loom_p'/name)
for p in (ROOT/'AGENTS.md',ROOT/'sources/00_LOOM_CURRENT_STATE(2).md',OLD/'NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md',OLD/'NURSERY_0_DESIGN_v0_1.md',OLD/'NURSERY_CANDIDATE_PROPOSALS.json',OLD/'EXPLORATION_AUDIT_RESULTS.json',OLD/'EXPLORATION_SUPPLEMENT.json'):
    track(p)
roster=read(ROOT/'founder_expansion_execution_20260930/analysis/ALL_SIXTY_AB.json')
assert [r['life_id'] for r in roster]==[f'FS-{i:03d}' for i in range(1,61)]

METHODS='''# Birth-geography methods fixed before metric extraction

All 60 original time-zero checkpoints are decoded as data, never instantiated as a world or organism. Verify file and payload hashes, index/time zero, configuration, and birth provenance. Use only stored birth fields/raw receptors for initial chemistry. Existing ALL_SIXTY_AB.json supplies previously derived later outcomes; no trajectory is re-executed. FS-060 belongs to all-60 birth statistics but is excluded from pooled complete-life outcome associations; its known 124 s prefix is separate.

Distances: body-surface gaps subtract body radius 0.5; also report centre-to-source-surface distance. Nearest source tie breaks by original source index. Bearing is wrapped atan2(source-centre minus body-centre) minus birth heading in [-180,180), positive counterclockwise. Mover distance is reported separately for actual birth body and full swept physical rectangle [5,15] x [9.5,10.5], with signed swept clearance and centre-to-centre-track distance. Swept clearance is descriptive, not a safety rejection rule.

Chemistry: raw channels are stored receptor values at heading offsets -45 and +45 degrees, two mixed chemical channels per site. Report site means, plus-minus contrast and contrast divided by the 0.501*sqrt(2) chord. This directional finite difference is not a supplied world gradient. For observer-only comparison compute exact bilinear field derivatives at the body centre from the saved field, without invoking transduction or a field solver. Verify static resampling reproduces the stored four receptors. No chemistry, bearing, distances, phase or outcomes are fed to P.

Safe support is evaluated by fixed midpoint spatial quadrature (0.05 units, sensitivity 0.1), using each of the 60 actual birth phases. Minimum body-surface gap must be >=0.25. The support-weighted reference is the mixture of conditional uniform distributions at those phases, not a uniform distribution over nominal arena area or the mover sweep. This conditions on observed phases; phase distribution is described separately.

Fixed spatial comparisons: 2x2, 4x4, 5x5 and 20x20 arena-aligned grids; observed counts, expected counts, expected occupied cells and coverage-weighted occupied-cell mass under independent conditional uniform draws. Four-quadrant marginal two-sided count probabilities use exact Poisson-binomial arithmetic, not Monte Carlo or an asymptotic sparse chi-square test; show Bonferroni over four quadrants. Fine-grid Pearson dispersion is descriptive only. All birth pairs at <=1/2/4 units, nearest-neighbour distances and support fraction within 1/2 units of any preserved birth are descriptive (no invented universal clustering threshold). Deterministic FFT quadrature computes expected close-pair count at distance 2 and expected support mass covered by radius-1 birth neighbourhoods, without creating synthetic births or random draws. There is no omnibus calibrated spatial point-process test and no proof of uniformity from non-rejection.

Outcome associations use 59 complete lives only: Spearman rank correlations against lifetime closest source gap and maximum excursion; group medians for damage >0, near-source <=1 and <=0.5, and actual source contact. Single source-contact life is a case description, not an estimable predictive model. Geography predictors fixed here: birth nearest source gap, cos(relative source bearing), mean chemical receptor level, max absolute receptor difference, minimum wall/repair gap, signed mover-sweep gap, actual mover gap. Report all, no outcome-dependent predictor selection, inference of cause, birth selection, or tuning. Phase/orientation are circular (sine/cosine, eight-bin counts/resultant), not ordinary raw-angle correlations. No p-values for exploratory outcome associations and no independent-sample claim for repeated time points.
'''
(OUT/'BIRTH_AUDIT_METHODS.md').write_text(METHODS,encoding='utf-8')

def rect_sdf(p,rect):
    p=np.asarray(p);lo=np.array([rect[0],rect[2]]);hi=np.array([rect[1],rect[3]])
    q=np.maximum(np.maximum(lo-p,p-hi),0);dist=np.linalg.norm(q,axis=-1)
    inside=np.all((p>=lo)&(p<=hi),axis=-1)
    depth=np.minimum(p-lo,hi-p).min(axis=-1)
    return np.where(inside,-depth,dist)
def mover_rect(phase):
    x=10+4*math.sin(phase);return np.array([x-1,x+1,9.5,10.5])
def gaps(p,phase):
    p=np.asarray(p);wall=np.minimum(p,20-p).min(axis=-1)-.5
    src=np.linalg.norm(p[...,None,:]-sources,axis=-1)-1
    rep=np.stack([rect_sdf(p,r)-.5 for r in repairs],axis=-1)
    mov=rect_sdf(p,mover_rect(phase))-.5
    return wall,src,rep,mov
def bilinear_gradient(field,p):
    u=np.array(p)/.25-.5;x,y=np.floor(u).astype(int);a,b=u-[x,y]
    v00=field[:,y,x];v10=field[:,y,x+1];v01=field[:,y+1,x];v11=field[:,y+1,x+1]
    v=(1-b)*((1-a)*v00+a*v10)+b*((1-a)*v01+a*v11)
    dx=((1-b)*(v10-v00)+b*(v11-v01))/.25
    dy=((1-a)*(v01-v00)+a*(v11-v10))/.25
    return v,np.column_stack([dx,dy])

rows=[];details=[];births=[];phases=[];source_raw_maxerr=0.;all_rejected=[];started=time.perf_counter()
for r in roster:
    name=r['life_id'];i=int(name[3:]);base=ROOT/('founder_initial_execution_20260930' if i<=12 else 'founder_expansion_execution_20260930')
    store=base/'lives'/name;cp=r['B_initial'];path=track(store/cp['checkpoint_file'],cp['checkpoint_sha256'])
    state=read_data(path,cp['checkpoint_sha256']);e=state['engine']['attributes'];b=e['body']['attributes']
    assert e['time']==e['native_index']==0
    assert e['c']['attributes']==c
    p=np.array(b['position']);theta=b['angle'];phase=e['phase'];birth=e['birth_provenance']
    assert np.array_equal(p,birth['position']) and theta==birth['angle'] and phase==birth['phase']
    wall,src,rep,mov=gaps(p,phase);min_gap=min(wall,src.min(),rep.min(),mov);assert min_gap>=.25-1e-12
    rejected=birth['rejected'];rejected_check=[]
    counters=e['organism']['attributes']['rng']['attributes']['counters']
    assert counters['life/world-position']==len(rejected)+1
    assert counters['life/world-orientation']==counters['life/world-phase']==1
    for proposal in rejected:
        gg=gaps(proposal['position'],phase);actual=min(gg[0],gg[1].min(),gg[2].min(),gg[3]);assert actual<.25 and abs(actual-proposal['minimum_gap'])<1e-12
        rejected_check.append(plain(proposal))
    raw=np.asarray(e['raw'][1]);assert raw.shape==(4,) and np.isfinite(raw).all()
    sites=[]
    for off in (-math.pi/4,math.pi/4):
        at=p+.501*np.array([math.cos(theta+off),math.sin(theta+off)]);v,grad=bilinear_gradient(e['fields'],at)
        mix=np.array([[1,.5],[.5,1]])@v;sites.extend(mix/(.05+mix))
    err=float(np.max(abs(raw-sites)));source_raw_maxerr=max(err,source_raw_maxerr);assert err<1e-12
    v,grad=bilinear_gradient(e['fields'],p);mixed=np.array([[1,.5],[.5,1]])@v;mg=np.array([[1,.5],[.5,1]])@grad;receptor_grad=.05/(.05+mixed[:,None])**2*mg
    sid=int(src.argmin());delta=sources[sid]-p;bearing=(math.atan2(delta[1],delta[0])-theta+math.pi)%(2*math.pi)-math.pi
    contrast=raw[2:]-raw[:2];means=(raw[2:]+raw[:2])/2
    sweep=rect_sdf(p,[5,15,9.5,10.5])-.5
    trackdist=np.linalg.norm(p-np.array([np.clip(p[0],6,14),10]))
    row=dict(life_id=name,complete=r['complete'],x=p[0],y=p[1],heading_rad=theta,heading_deg=math.degrees(theta),mover_phase_rad=phase,mover_phase_deg=math.degrees(phase),mover_centre_x=10+4*math.sin(phase),mover_velocity_x=4*2*math.pi/30*math.cos(phase),birth_minimum_surface_gap=min_gap,rejected_proposals=len(rejected),nearest_source_id=sid,nearest_source_body_gap=src[sid],nearest_source_centre_to_surface=src[sid]+.5,nearest_source_bearing_deg=math.degrees(bearing),source_ahead_cos=math.cos(bearing),nearest_wall_body_gap=wall,nearest_repair_body_gap=rep.min(),mover_actual_body_gap=mov,mover_swept_body_gap=sweep,mover_centre_track_distance=trackdist,chem_minus45_A=raw[0],chem_minus45_B=raw[1],chem_plus45_A=raw[2],chem_plus45_B=raw[3],chem_mean_A=means[0],chem_mean_B=means[1],chem_overall_mean=raw.mean(),chem_plus_minus_A=contrast[0],chem_plus_minus_B=contrast[1],chem_chord_gradient_A=contrast[0]/(.501*math.sqrt(2)),chem_chord_gradient_B=contrast[1]/(.501*math.sqrt(2)),chem_max_abs_contrast=abs(contrast).max(),chem_abs_normalized_imbalance_A=abs(contrast[0])/(raw[0]+raw[2]),chem_abs_normalized_imbalance_B=abs(contrast[1])/(raw[1]+raw[3]),field_centre_A=v[0],field_centre_B=v[1],field_gradient_A_norm=np.linalg.norm(grad[0]),field_gradient_B_norm=np.linalg.norm(grad[1]),receptor_field_gradient_A_norm=np.linalg.norm(receptor_grad[0]),receptor_field_gradient_B_norm=np.linalg.norm(receptor_grad[1]),observed_duration=r['simulated_seconds'],later_source_contact=r['source_contact_duration']>0,later_gross_energy=r['transfer_total'],later_damage=r['damage'],later_source_min_gap=min(r['min_source_endpoint_gap']),later_near_source_1=min(r['min_source_endpoint_gap'])<=1,later_near_source_05=min(r['min_source_endpoint_gap'])<=.5,later_max_excursion=r['max_excursion_from_birth'])
    rows.append(row);births.append(p);phases.append(phase)
    details.append(dict(**row,source_gaps=src,repair_gaps=rep,wall_gaps=np.r_[p-.5,19.5-p],field_centre_gradient=grad,receptor_centre_gradient=receptor_grad,rejected_proposals_records=rejected_check,initial_file=path.as_posix(),initial_file_sha256=cp['checkpoint_sha256'],raw_reconstruction_maxerror=err))
births=np.array(births);phases=np.array(phases);table('BIRTH_GEOGRAPHY_ALL_60.csv',rows);save('BIRTH_INITIAL_DETAILS.json',details)

def support_grid(dx):
    axis=np.arange(dx/2,20,dx);xx,yy=np.meshgrid(axis,axis);p=np.stack([xx,yy],axis=-1)
    wall,src,rep,_=gaps(p,0);static=(wall>=.25)&(src.min(axis=-1)>=.25)&(rep.min(axis=-1)>=.25)
    masks=np.stack([static&(rect_sdf(p,mover_rect(phi))-.5>=.25) for phi in phases]);mass=masks/masks.sum(axis=(1,2))[:,None,None]
    return axis,p,static,masks,mass
def pb_tail(probs,k):
    distribution=np.array([1.])
    for pr in probs:distribution=np.convolve(distribution,[1-pr,pr])
    return min(1.,2*min(distribution[:k+1].sum(),distribution[k:].sum()))

quad=[];grid_results={};sensitivity={}
for dx in (.1,.05):
    axis,grid,static,masks,mass=support_grid(dx);mix=mass.mean(axis=0);result={}
    dist=np.full(grid.shape[:2],np.inf)
    for birth in births:dist=np.minimum(dist,np.linalg.norm(grid-birth,axis=-1))
    for n in (2,4,5,20):
        cell=np.minimum((grid/(20/n)).astype(int),n-1);code=cell[:,:,1]*n+cell[:,:,0]
        actual_cell=np.minimum((births/(20/n)).astype(int),n-1);actual_code=actual_cell[:,1]*n+actual_cell[:,0]
        counts=np.bincount(actual_code,minlength=n*n)
        pi=np.stack([np.bincount(code.ravel(),weights=m.ravel(),minlength=n*n) for m in mass])
        expected=pi.sum(axis=0);expected_occupied=float((1-np.prod(1-pi,axis=0)).sum())
        v=(pi*(1-pi)).sum(axis=0)
        result[str(n)]=dict(observed_occupied=int((counts>0).sum()),cells=n*n,expected_occupied=expected_occupied,occupied_support_mass=float((pi.mean(axis=0)*(counts>0)).sum()),counts=counts,expected=expected,descriptive_pearson=float(((counts-expected)**2/np.maximum(expected,1e-300)).sum()))
        if dx==.05:
            for k in range(n*n):
                quad.append(dict(grid_n=n,ix=k%n,iy=k//n,observed=counts[k],expected=expected[k],count_sd=math.sqrt(v[k]),support_probability=pi[:,k].mean(),two_sided_marginal_p=pb_tail(pi[:,k],counts[k]) if n==2 else None))
    result.update(safe_area_mean=float(masks.sum(axis=(1,2)).mean()*dx*dx),safe_area_range=[float(masks.sum(axis=(1,2)).min()*dx*dx),float(masks.sum(axis=(1,2)).max()*dx*dx)],support_mass_within_1=float(mix[dist<=1].sum()),support_mass_within_2=float(mix[dist<=2].sum()),maximum_sampled_distance_from_births=float(dist[mix>0].max()))
    sensitivity[str(dx)]=result
    if dx==.05:
        np.savez_compressed(OUT/'BIRTH_SAFE_SUPPORT_GRID.npz',axis=axis,admissible_phase_fraction=masks.mean(axis=0),mixture_density=mix/(dx*dx),static_safe=static,births=births)
        # Deterministic convolution for expected coverage and close pairs.
        shape=grid.shape[:2];pad=tuple(2*n for n in shape)
        def kernel(radius):
            yy=np.fft.fftfreq(pad[0])*pad[0]*dx;xx=np.fft.fftfreq(pad[1])*pad[1]*dx
            return np.fft.rfftn((yy[:,None]**2+xx[None,:]**2<=radius**2+1e-12).astype(float))
        k1,k2=kernel(1),kernel(2);uncovered=np.ones(shape);sum_conv2=np.zeros(shape);own_pair=0.
        for mi in mass:
            freq=np.fft.rfftn(mi,s=pad,axes=(0,1))
            conv1=np.fft.irfftn(freq*k1,s=pad,axes=(0,1))[:shape[0],:shape[1]]
            uncovered*=1-np.clip(conv1,0,1)
            conv2=np.fft.irfftn(freq*k2,s=pad,axes=(0,1))[:shape[0],:shape[1]]
            sum_conv2+=conv2;own_pair+=float(np.sum(mi*conv2))
        result['expected_support_mass_within_1']=float(np.sum(mix*(1-uncovered)))
        result['expected_unordered_pairs_within_2']=float(.5*(np.sum(mass.sum(axis=0)*sum_conv2)-own_pair))
save('SAFE_SUPPORT_QUADRATURE.json',sensitivity);table('BIRTH_QUADRAT_COUNTS.csv',quad)
pairdist=np.linalg.norm(births[:,None,:]-births[None,:,:],axis=-1);np.fill_diagonal(pairdist,np.inf)
pairvals=pairdist[np.triu_indices(60,1)]

def ranks(x):
    x=np.asarray(x);order=np.argsort(x,kind='stable');out=np.empty(len(x));i=0
    while i<len(x):
        j=i+1
        while j<len(x) and x[order[j]]==x[order[i]]:j+=1
        out[order[i:j]]=(i+j-1)/2;i=j
    return out
complete=[r for r in rows if r['complete']];assoc=[]
predictors=['nearest_source_body_gap','source_ahead_cos','chem_overall_mean','chem_max_abs_contrast','nearest_wall_body_gap','nearest_repair_body_gap','mover_swept_body_gap','mover_actual_body_gap']
for row in rows:
    for kind,key in [('phase','mover_phase_rad'),('heading','heading_rad')]:
        row[kind+'_sin']=math.sin(row[key]);row[kind+'_cos']=math.cos(row[key])
for x in predictors+['phase_sin','phase_cos','heading_sin','heading_cos']:
    for y in ('later_source_min_gap','later_max_excursion'):
        rx=ranks([r[x] for r in complete]);ry=ranks([r[y] for r in complete]);assoc.append(dict(predictor=x,outcome=y,n=59,spearman=float(np.corrcoef(rx,ry)[0,1])))
table('EXPLORATORY_ASSOCIATIONS.csv',assoc)
groups={}
for key in ('later_source_contact','later_near_source_1','later_near_source_05','later_damage'):
    groups[key]={}
    for flag in (False,True):
        rr=[r for r in complete if bool(r[key])==flag]
        groups[key][str(flag)]=dict(n=len(rr),life_ids=[r['life_id'] for r in rr],predictors={x:stats([r[x] for r in rr]) for x in predictors})
save('OUTCOME_ASSOCIATION_GROUPS.json',groups)
summaries={k:stats([r[k] for r in rows]) for k in rows[0] if isinstance(rows[0][k],(int,float,np.number)) and not isinstance(rows[0][k],bool)}
circular={}
for key in ('heading_rad','mover_phase_rad'):
    z=np.array([r[key] for r in rows]);circular[key]=dict(eight_equal_angle_counts=np.histogram(z,bins=np.linspace(0,2*np.pi,9))[0],mean_resultant=abs(np.mean(np.exp(1j*z))),mean_direction_deg=math.degrees(np.angle(np.mean(np.exp(1j*z))))%360)
closest=np.unravel_index(pairdist.argmin(),pairdist.shape)
result=dict(all_births=60,complete_outcome_lives=59,FS060='APPARATUS_INTERRUPTED_UNCLOSED; birth included, prefix excluded from pooled complete-life outcome correlations',summary=summaries,circular=circular,rejected_total=sum(r['rejected_proposals'] for r in rows),births_with_rejections=sum(r['rejected_proposals']>0 for r in rows),nearest_neighbour=stats(pairdist.min(axis=1)),closest_pair=[rows[i]['life_id'] for i in closest],pair_counts={str(radius):int((pairvals<=radius).sum()) for radius in (1,2,4)},quadrature=sensitivity['0.05'],raw_receptor_reconstruction_error=source_raw_maxerr,source_contact_case=next(r for r in rows if r['later_source_contact']),FS060_birth=rows[-1],execution=dict(world_steps=0,P_steps=0,field_steps=0,new_births=0,RNG_draws=0,controller_calls=0),wall_seconds=time.perf_counter()-started)
save('BIRTH_AUDIT_RESULTS.json',result)
save('INPUT_CUSTODY.json',dict(purpose='read-only evidence hashes, not an authority',files=[dict(path=p,sha256=h,bytes=Path(p).stat().st_size) for p,h in INPUTS.items()]))
print(json.dumps(plain({k:result[k] for k in ('all_births','complete_outcome_lives','rejected_total','births_with_rejections','nearest_neighbour','closest_pair','pair_counts','circular','quadrature','raw_receptor_reconstruction_error','execution','wall_seconds')}),indent=2))
