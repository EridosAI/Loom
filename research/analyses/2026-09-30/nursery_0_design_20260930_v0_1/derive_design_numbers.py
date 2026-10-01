"""Design-only arithmetic and saved-summary reads. No Loom imports or execution."""
from pathlib import Path
import json, math, statistics, hashlib, csv
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(__file__).resolve().parent
WT = ROOT/'worktrees/loom-p-b1-minimal-20260929'
cfg = json.loads((WT/'developmental_ecology/configuration.json').read_text())
rows = json.loads((ROOT/'founder_expansion_execution_20260930/analysis/ALL_SIXTY_AB.json').read_text())
complete = [r for r in rows if r['complete']]
assert len(rows)==60 and len(complete)==59
def stats(values):
    v=sorted(values)
    return dict(n=len(v),minimum=v[0],median=statistics.median(v),mean=statistics.mean(v),maximum=v[-1])
metrics={k:stats([r[k] for r in complete]) for k in ('simulated_seconds','path_length','displacement','max_excursion_from_birth','coverage_1_unit_bins','damage','repair')}
metrics['closest_source_gap']=stats([min(r['min_source_endpoint_gap']) for r in complete])
metrics['complete_lives_ever_within_source_gap']={str(g):sum(min(r['min_source_endpoint_gap'])<=g for r in complete) for g in (.05,.25,.5,1.,2.)}
metrics['damaged_lives']=[r['life_id'] for r in rows if r['damage']>0]
metrics['positive_intake_lives']=[r['life_id'] for r in rows if r['transfer_total']>0]
metrics['restored_lives']=[r['life_id'] for r in rows if r['repair']>0]
metrics['I_bank_formed']=[r['life_id'] for r in rows if r['B_initial']['theta_I_norm']==0 and r['B_final']['theta_I_norm']>0]
metrics['minimum_final_I_complete']=min(r['integrity_final'] for r in complete)
no_intake=[r for r in complete if r['transfer_total']==0]
effort_mean=statistics.mean((r['expenditure']/r['simulated_seconds']-cfg['basal_cost']) for r in no_intake)
metrics['observed_mean_effort_energy_per_second_no_intake']=effort_mean
metrics['observed_mean_effort_share_no_intake']=effort_mean/(cfg['basal_cost']+effort_mean)
metrics['mean_cost_proxy_A']=cfg['birth_energy']/(cfg['basal_cost']+effort_mean)
metrics['mean_cost_proxy_B_C']=cfg['birth_energy']/(.0012+effort_mean)
metrics['basal_only_A']=.7/.0015
metrics['basal_only_B_C']=.7/.0012

stops=[]
for directory in ('founder_initial_execution_20260930','founder_expansion_execution_20260930'):
    stops += [json.loads(p.read_text()) for p in (ROOT/directory).glob('FS-*_STOP.json')]
assert len(stops)==59 and all(r['complete'] for r in stops)
resources={
    'completed_lives':len(stops),
    'active_wall_s':stats([r['active_wall_seconds'] for r in stops]),
    'wall_s_per_simulated_s':stats([r['active_wall_seconds']/r['simulated_seconds'] for r in stops]),
    'bytes_per_simulated_s':stats([r['primary_bytes']/r['simulated_seconds'] for r in stops]),
    'primary_bytes_per_life':stats([r['primary_bytes'] for r in stops]),
    'preparation_observed_48_total_wall_s':5808.444936249638,
    'preparation_observed_mean_s':5808.444936249638/48,
    'nursery_speedup_assumed':False,
}
resources['per_600s_median_wall_s']=600*resources['wall_s_per_simulated_s']['median']
resources['per_600s_observed_rate_range_s']=[600*resources['wall_s_per_simulated_s'][k] for k in ('minimum','maximum')]
resources['per_600s_median_bytes']=600*resources['bytes_per_simulated_s']['median']
resources['per_600s_observed_rate_range_bytes']=[600*resources['bytes_per_simulated_s'][k] for k in ('minimum','maximum')]

proposed=dict(world_side=14.,source_positions=[[x,y] for y in (2.,4.5,9.5,12.) for x in (2.5,7.,11.5)],repair_rectangles=[[0.,.25,5.,9.],[13.75,14.,5.,9.],[5.,9.,13.75,14.]],mover_centre=[7.,7.],grid_n=56)
def primitive(x,r):
    return .5*(x*math.sqrt(max(0,r*r-x*x))+r*r*math.asin(x/r))
def strip_exclusion(radius):
    # Body-centre domain begins radius from arena wall. Strip protrudes .25.
    return 4*.25+2*(primitive(radius,radius)-primitive(radius-.25,radius))
def area_values(c):
    L=c['world_side']; n=len(c['source_positions']); r=.5
    stat=(L-2*r)**2-n*math.pi*(r+.5)**2-3*strip_exclusion(r)
    mover_footprint=2+6*r+math.pi*r*r
    swept_footprint=10+22*r+math.pi*r*r
    return dict(nominal_area=L*L,static_free_ground_area=L*L-n*math.pi*.25-3.,instantaneous_free_ground_area=L*L-n*math.pi*.25-3.-2.,static_body_centre_area=stat,instantaneous_body_centre_area=stat-mover_footprint,conservative_always_clear_body_centre_area=stat-swept_footprint,nominal_source_density=n/L**2,static_centre_source_density=n/stat,repair_main_frontage=12.,repair_exposed_length_including_ends=13.5,wall_perimeter=4*L,repair_main_frontage_fraction=12/(4*L),source_initial_total_stock=n*.2,maximum_instantaneous_total_renewal_rate=n*.2/400)
geometry={'current':area_values(cfg),'proposed':area_values(proposed)}
def grid_summary(c,dx):
    # Fixed midpoint quadrature and 16 equally-spaced phases. Not a trajectory.
    L=c['world_side']; v=np.arange(dx/2,L,dx); X,Y=np.meshgrid(v,v); X=X.ravel();Y=Y.ravel()
    wallgap=np.minimum.reduce((X-.5,L-X-.5,Y-.5,L-Y-.5))
    near=np.full(X.shape,np.inf)
    eligible=wallgap>=.25
    for x,y in c['source_positions']:
        g=np.hypot(X-x,Y-y)-1.;near=np.minimum(near,g);eligible &= g>=.25
    for x0,x1,y0,y1 in c['repair_rectangles']:
        g=np.hypot(np.maximum(np.maximum(x0-X,X-x1),0),np.maximum(np.maximum(y0-Y,Y-y1),0))-.5
        eligible &= g>=.25
    result=[]
    for k in range(16):
        mx=c['mover_centre'][0]+4*math.sin(2*math.pi*k/16);my=c['mover_centre'][1]
        gm=np.hypot(np.maximum(np.abs(X-mx)-1,0),np.maximum(np.abs(Y-my)-.5,0))-.5
        ok=eligible & (gm>=.25)
        result.append(dict(phase=2*math.pi*k/16,admissible_area=float(ok.sum()*dx**2),within_gap_05=float(np.mean(near[ok]<=.5)),within_gap_10=float(np.mean(near[ok]<=1.)),nearest_gap_median=float(np.median(near[ok]))))
    return dict(cell=dx,phase_count=16,kind='STATIC_GEOMETRIC_QUADRATURE_NOT_SIMULATION',phases=result,mean_birth_area=statistics.mean(x['admissible_area'] for x in result),mean_fraction_gap05=statistics.mean(x['within_gap_05'] for x in result),mean_fraction_gap10=statistics.mean(x['within_gap_10'] for x in result),mean_nearest_gap_median=statistics.mean(x['nearest_gap_median'] for x in result))
geometry['birth_proximity']={name:{str(dx):grid_summary(c,dx) for dx in (.05,.025)} for name,c in [('current',cfg),('proposed',proposed)]}

def chemical_budget(n,L):
    emission=[.05*n+.25*.15,.5*.05*n+.35*.15]
    finite_factor=1-(1+.01*.02)**(-60000)
    mean=[x/(.02*L*L)*finite_factor for x in emission]
    mixed=[mean[0]+.5*mean[1],.5*mean[0]+mean[1]]
    return dict(total_emission=emission,full_stock_600s_global_mean_concentration=mean,mixed_global_mean=mixed,uniform_field_receptor_proxy=[x/(.05+x) for x in mixed],receptor_slope_at_mean=[.05/(.05+x)**2 for x in mixed],not_spatial_field_or_signal_prediction=True)
chemistry={'current':chemical_budget(8,20),'proposed':chemical_budget(12,14),'medium_diffusion_length_sqrt_D_over_decay':math.sqrt(.5/.02)}
force=math.sqrt(.1**2+.1*.25)-.1
rq=force/(force+.1)*(1-force/.25)
physics=dict(optimal_motionless_repair_force=force,maximum_motionless_repair_quality=rq,best_half_deficit_repair_time=math.log(2)/(.02*rq),repair_half_deficit_at_force005=math.log(2)/(.02*(.05/(.05+.1))*(1-.05/.25)),mover_maximum_speed=4*2*math.pi/30,source_empty_renewal_rate=.2/400)

data=dict(scope='DESIGN_ONLY_NO_LOOM_IMPORT_NO_P_OR_WORLD_EXECUTION',metrics=metrics,resources=resources,geometry=geometry,chemistry=chemistry,physics=physics,proposal_geometry=proposed)
(OUT/'DESIGN_ARITHMETIC.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
with (OUT/'CURRENT_WORLD_60_LIFE_EVIDENCE.csv').open('w',newline='',encoding='utf-8') as f:
    keys=['life_id','complete','state','simulated_seconds','path_length','displacement','max_excursion_from_birth','coverage_1_unit_bins','damage','repair','transfer_total','source_contact_duration','integrity_final']
    w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows({k:r[k] for k in keys} for r in rows)
print(json.dumps({k:data[k] for k in ('metrics','resources','chemistry','physics')},indent=2))
print(json.dumps({k:geometry[k] for k in ('current','proposed')},indent=2))
print(json.dumps({name:{dx:{k:v for k,v in row.items() if k!='phases'} for dx,row in scans.items()} for name,scans in geometry['birth_proximity'].items()},indent=2))
