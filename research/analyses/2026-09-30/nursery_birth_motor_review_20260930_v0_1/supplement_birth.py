"""Detached additional summaries and arithmetic checks, no simulation."""
from pathlib import Path
import json,math,csv,ast
import numpy as np
O=Path(__file__).resolve().parent
R=json.loads((O/'BIRTH_AUDIT_RESULTS.json').read_text());rows=json.loads((O/'BIRTH_INITIAL_DETAILS.json').read_text())
q=json.loads((O/'SAFE_SUPPORT_QUADRATURE.json').read_text())
complete=[r for r in rows if r['complete']]
out={}
out['birth_near_source_counts']={str(g):sum(r['nearest_source_body_gap']<=g for r in rows) for g in (.5,1,2)}
out['source_bearing_front_hemisphere']=sum(abs(r['nearest_source_bearing_deg'])<90 for r in rows)
out['source_bearing_eight_bins']=np.histogram([r['nearest_source_bearing_deg'] for r in rows],bins=np.linspace(-180,180,9))[0].tolist()
out['nearest_source_counts']=np.bincount([r['nearest_source_id'] for r in rows],minlength=8).tolist()
out['swept_overlap_births']=[r['life_id'] for r in rows if r['mover_swept_body_gap']<0]
out['near_source_improvement']=dict(median=float(np.median([r['nearest_source_body_gap']-r['later_source_min_gap'] for r in complete])),maximum=float(max(r['nearest_source_body_gap']-r['later_source_min_gap'] for r in complete)))
out['damaged_birth_table']=[{k:r[k] for k in ('life_id','nearest_wall_body_gap','nearest_source_body_gap','mover_swept_body_gap','mover_actual_body_gap','later_damage','later_max_excursion')} for r in complete if r['later_damage']>0]
out['rejected_lives']=[r['life_id'] for r in rows if r['rejected_proposals']>0]
# The stopping scheme is geometric rejections before each success, not fixed 64 Bernoulli trials.
accept=q['0.05']['safe_area_mean']/19**2
total=np.array([1.,0,0,0,0])
for _ in range(60):total=np.convolve(total,[accept*(1-accept)**k for k in range(5)])[:5]
out['rejection_count_descriptive_check']=dict(expected_rejections_approx=60*(1-accept)/accept,observed=4,approx_probability_total_at_most_four=float(total.sum()),meaning='Exploratory check under ideal independent proposals; area variation across phases is below 0.02%. Not an accepted-position clustering test, no PRNG defect proved, no reroll.')
# FFT convolution indexing checked against direct sums on a manufactured mask, no bodies/RNG.
m=np.zeros((8,8));m[2:6,1:7]=1;m/=m.sum();pad=(16,16);yy=np.fft.fftfreq(16)*16;xx=yy
k=(yy[:,None]**2+xx[None,:]**2<=4).astype(float)
v=np.fft.irfftn(np.fft.rfftn(m,s=pad,axes=(0,1))*np.fft.rfftn(k),s=pad,axes=(0,1))[:8,:8]
for y in range(8):
    for x in range(8):
        iy,ix=np.indices(m.shape);direct=m[(iy-y)**2+(ix-x)**2<=4].sum();assert abs(v[y,x]-direct)<1e-12
out['detached_convolution_check']='PASS: finite non-wrapping mask convolution equals direct sums at all manufactured grid points'
# Finer deterministic area/coverage check; only geometry from stored configuration and phases.
c=json.loads((O.parent/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology/configuration.json').read_text())
tree=ast.parse((O/'audit_birth.py').read_text());nodes=[v for v in tree.body if isinstance(v,ast.FunctionDef) and v.name in ('rect_sdf','mover_rect','gaps')]
ns=dict(np=np,math=math,sources=np.array(c['source_positions']),repairs=np.array(c['repair_rectangles']))
exec(compile(ast.Module(body=nodes,type_ignores=[]),'detached_geometry','exec'),ns)
dx=.025;axis=np.arange(dx/2,20,dx);xx,yy=np.meshgrid(axis,axis);p=np.stack([xx,yy],axis=-1)
wall,src,rep,_=ns['gaps'](p,0);static=(wall>=.25)&(src.min(axis=-1)>=.25)&(rep.min(axis=-1)>=.25)
distance=np.full(xx.shape,np.inf)
for row in rows:distance=np.minimum(distance,np.linalg.norm(p-[row['x'],row['y']],axis=-1))
areas=[];cover1=[];cover2=[];near05=[];near1=[]
for row in rows:
    mask=static&(ns['rect_sdf'](p,ns['mover_rect'](row['mover_phase_rad']))-.5>=.25);n=mask.sum()
    areas.append(float(n*dx*dx));cover1.append(float((mask&(distance<=1)).sum()/n));cover2.append(float((mask&(distance<=2)).sum()/n))
    near05.append(float((mask&(src.min(axis=-1)<=.5)).sum()/n));near1.append(float((mask&(src.min(axis=-1)<=1)).sum()/n))
out['finer_static_quadrature']=dict(dx=dx,mean_safe_area=float(np.mean(areas)),area_range=[min(areas),max(areas)],coverage_within_1=float(np.mean(cover1)),coverage_within_2=float(np.mean(cover2)),expected_births_source_gap_le05=float(np.sum(near05)),expected_births_source_gap_le1=float(np.sum(near1)),no_births_drawn=True)
(O/'BIRTH_SUPPLEMENT.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))
