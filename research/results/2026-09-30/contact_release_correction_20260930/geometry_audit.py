"""Scalar reconstruction of the saved frozen-force contact geometry only."""
from pathlib import Path
import json,sys
import numpy as np
from scipy.optimize import brentq,minimize_scalar
HERE=Path(__file__).resolve().parent;ROOT=HERE.parent
sys.path.insert(0,str(ROOT/'worktrees/loom-contact-release-20260930/developmental_ecology'))
from loom_p.schema import Config
from loom_p.physics import Body,actuator_forces,flat_face_exit,motion_bounds
from loom_p.geometry import fixtures,gap_normal
d=json.loads((HERE/'EXACT_PHYSICAL_INPUT.json').read_bytes());c=Config(**d['c'])
b=Body(**{k:np.array(v) if isinstance(v,list) else v for k,v in d['body'].items()})
t=d['t'];p=d['phase'];u=np.array(d['command']);dt=d['dt']
F=actuator_forces(c,b,u);forward=np.array([np.cos(b.angle),np.sin(b.angle)])
def curve(s):
    v=b.velocity*np.exp(-c.linear_drag*s/c.body_mass)+F.sum()*forward/c.linear_drag*(-np.expm1(-c.linear_drag*s/c.body_mass))
    pos=b.position+s*v
    edge=c.mover_centre[0]+c.mover_amplitude*np.sin(2*np.pi*(t+s)/c.mover_period+p)-c.mover_size[0]/2
    gap=np.hypot(max(edge-pos[0],0.),c.mover_centre[1]-c.mover_size[1]/2-pos[1])-c.body_radius
    return dict(s=s,body_position=pos.tolist(),mover_left=edge,tangent_margin=pos[0]-edge,gap=float(gap))
face=brentq(lambda s:curve(s)['tangent_margin'],0,dt,xtol=1e-14)
inside=brentq(lambda s:curve(s)['gap']+c.geometry_tol,0,.005,xtol=1e-14)
exit0=brentq(lambda s:curve(s)['gap'],.005,dt,xtol=1e-14)
minimum=minimize_scalar(lambda s:curve(s)['gap'],bounds=(0,dt),method='bounded',options={'xatol':1e-14})
certificate=flat_face_exit(c,b,F,t,p,dt,15)
f=fixtures(c,t,p)[15];gap,n=gap_normal(b.position,c.body_radius,f)
speed,A=motion_bounds(c,b,F,dt);A+=c.mover_amplitude*(2*np.pi/c.mover_period)**2
result=dict(classification='RELEASE_PATH_DEFECT_UNSUPPORTED_LEGITIMATE_FACE_TO_CORNER_CONTACT',
    time=t,phase=p,body_position=b.position.tolist(),radius=c.body_radius,body_angle=b.angle,
    body_velocity=b.velocity.tolist(),command=u.tolist(),forces=F.tolist(),
    mover_rectangle=f['rect'].tolist(),mover_velocity=f['velocity'].tolist(),
    initial_gap=gap,initial_normal=n.tolist(),relative_velocity=(b.velocity-f['velocity']).tolist(),
    geometry_tolerance=c.geometry_tol,overlap_tolerance=c.overlap_tol,event_time_tolerance=c.event_time_tol,
    face_exit_oracle=face,face_exit_solver=certificate,root_time_error=certificate-face,
    face_exit_bracket=[certificate-c.event_time_tol,certificate],
    free_gap_below_negative_geometry_tolerance_at=inside,free_zero_return_at=exit0,
    free_minimum=dict(s=float(minimum.x),gap=float(minimum.fun)),
    original_clear_probe=dt,original_inward_probe=.005,
    tangential_relative_rate=float(b.velocity[0]-f['velocity'][0]),
    relative_second_derivative_bound=A,
    certified_max_tangent_rate=float(b.velocity[0]-f['velocity'][0]+A*dt),
    samples=[curve(s) for s in (0,inside,face,.005,float(minimum.x),exit0,dt)])
(HERE/'GEOMETRY_AUDIT.json').write_text(json.dumps(result,indent=2),encoding='utf8')
print(json.dumps(result,indent=2))
