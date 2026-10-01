"""Body-only mechanics and separate physical reserve accounting (spec §8.2)."""
from dataclasses import dataclass,field
import itertools
import math
import numpy as np
from .geometry import fixtures,gap_normal,mover

@dataclass
class Body:
    position: np.ndarray
    angle: float
    energy: float=.7
    integrity: float=1.
    velocity: np.ndarray=field(default_factory=lambda:np.zeros(2))
    omega: float=0.
    command: np.ndarray=field(default_factory=lambda:np.zeros(2))
    force: np.ndarray=field(default_factory=lambda:np.zeros(2))
    contact_rates: np.ndarray=field(default_factory=lambda:np.zeros(8))
    @property
    def reserves(self): return np.array([self.energy,self.integrity])

class TerminalCrossing(Exception):
    def __init__(self,elapsed,dimension,events):
        self.elapsed=elapsed; self.dimension=dimension; self.events=events

def project_velocity(free,normals,bounds,mass,tol=1e-10):
    """Exact small 2D convex QP by active sets of rank <=2, ordered deterministically."""
    normals=np.asarray(normals,dtype=float).reshape(-1,2); bounds=np.asarray(bounds,dtype=float)
    if not len(normals): return free.copy(),np.zeros(0)
    candidates=[]
    if np.all(normals@free>=bounds-tol): candidates.append((0.,free.copy(),np.zeros(len(normals))))
    for count in (1,2):
        for ids in itertools.combinations(range(len(normals)),count):
            n=normals[list(ids)]; gram=n@n.T
            if np.linalg.matrix_rank(gram,tol=1e-12)<count: continue
            multiplier=np.linalg.solve(gram,bounds[list(ids)]-n@free)
            if multiplier.min()<-tol: continue
            corrected=free+n.T@multiplier
            if np.min(normals@corrected-bounds)<-tol: continue
            impulses=np.zeros(len(normals)); impulses[list(ids)]=mass*np.maximum(multiplier,0)
            candidates.append((float(np.sum((corrected-free)**2)),corrected,impulses))
    if not candidates: raise ArithmeticError('Unsolved simultaneous rigid contact constraints')
    _,velocity,impulses=min(candidates,key=lambda item:item[0])
    return velocity,impulses

def actuator_forces(c,body,command):
    return .5*(.2+.8*body.energy)*np.array([.4+.6*body.integrity,.7+.3*body.integrity])*command

def free_velocity(c,body,forces,dt):
    forward=np.array([np.cos(body.angle),np.sin(body.angle)])
    v=body.velocity*np.exp(-c.linear_drag*dt/c.body_mass)+(forces.sum()/c.linear_drag)*forward*(-np.expm1(-c.linear_drag*dt/c.body_mass))
    omega=body.omega*np.exp(-c.angular_drag*dt/c.body_inertia)+(c.lever*(forces[1]-forces[0])/c.angular_drag)*(-np.expm1(-c.angular_drag*dt/c.body_inertia))
    return v,float(omega)

def account(c,body,stocks,contacts,dt,instant=False):
    """One physical subinterval; exact same source debit/body credit, no neural input."""
    energy_before=body.energy; integrity_before=body.integrity; stock_before=stocks.copy()
    if instant:
        damage=c.damage_per_impulse*sum(x['impulse'] for x in contacts)
        body.integrity-=damage
        return dict(duration=0.,impact=True,contacts=contacts,energy_before=energy_before,energy_after=body.energy,integrity_before=integrity_before,integrity_after=body.integrity,damage=damage,repair=0.,requested=np.zeros_like(stocks),transfer=np.zeros_like(stocks),renewal_first=np.zeros_like(stocks),renewal_second=np.zeros_like(stocks),expenditure=0.,stock_before=stock_before,stock_after=stocks.copy())
    if dt<=0: raise ValueError('Sustained accounting requires positive duration')
    expense=(c.basal_cost+c.effort_cost*np.abs(body.command).sum()/2)*dt
    renewal_first=(c.source_capacity-stocks)*(-np.expm1(-dt/(2*c.source_tau))); stocks+=renewal_first
    quality=np.zeros_like(stocks); repair_quality=0.
    for contact in contacts:
        force=contact['impulse']/dt; speed=contact['relative_speed']
        q=force/(force+c.exchange_force_scale)/(1+(speed/c.exchange_speed_scale)**2)
        contact['force']=force
        if 'source' in contact: quality[contact['source']]=max(quality[contact['source']],q)
        if contact['material']==3: repair_quality=max(repair_quality,q*max(1-force/c.stress_threshold,0))
    requested=c.uptake_rate*(stocks/c.source_capacity)*(1-body.energy)*quality*dt
    debit=np.minimum(requested,stocks)
    if debit.sum()>1-body.energy+expense: debit*=max(0,1-body.energy+expense)/debit.sum()
    stocks-=debit; body.energy+=float(debit.sum())-expense
    renewal_second=(c.source_capacity-stocks)*(-np.expm1(-dt/(2*c.source_tau))); stocks+=renewal_second
    damage=c.damage_per_impulse*sum(max(x['impulse']-c.stress_threshold*dt,0) for x in contacts)
    body.integrity-=damage; repair=0.
    if body.integrity>0:
        repair=(1-body.integrity)*(-np.expm1(-c.repair_rate*repair_quality*dt)); body.integrity+=repair
    return dict(duration=dt,impact=False,contacts=contacts,energy_before=energy_before,energy_after=body.energy,integrity_before=integrity_before,integrity_after=body.integrity,damage=damage,repair=repair,repair_quality=repair_quality,requested=requested,transfer=debit,renewal_first=renewal_first,renewal_second=renewal_second,expenditure=expense,stock_before=stock_before,stock_after=stocks.copy())

def contact_record(c,body,fixture,normal,impulse):
    arm=-c.body_radius*normal
    surface=body.velocity+body.omega*np.array([-arm[1],arm[0]])
    record=dict(collider=fixture['id'],material=fixture['material'],normal=normal.copy(),impulse=float(impulse),relative_speed=float(np.linalg.norm(surface-fixture['velocity'])))
    if 'source' in fixture: record['source']=fixture['source']
    return record

def first_collision(c,body,forces,t,phase,dt,excluded):
    """Conservative advancement using a global relative-speed bound; analytic mover."""
    # v(t) is a convex interpolation along one line under frozen force. Its norm
    # is bounded by the endpoint norms. For p(t)=p0+t*v(t), bound |p'| by
    # vmax+dt*amax. Only the mover adds its own speed; assigning that speed to
    # almost-touching stationary sources made separating contact searches stall.
    ending_velocity,_=free_velocity(c,body,forces,dt)
    vmax=max(float(np.linalg.norm(body.velocity)),float(np.linalg.norm(ending_velocity)))
    speed_bound=vmax+dt*(abs(float(forces.sum()))+c.linear_drag*vmax)/c.body_mass+1e-12
    elapsed=0.
    for _ in range(500):
        velocity,_=free_velocity(c,body,forces,elapsed); position=body.position+elapsed*velocity
        candidates=[(gap_normal(position,c.body_radius,f)[0],i,speed_bound+(c.mover_amplitude*2*np.pi/c.mover_period if f['id']=='mover' else 0.)) for i,f in enumerate(fixtures(c,t+elapsed,phase)) if i not in excluded]
        if not candidates: return None
        gap,index,_=min(candidates)
        if gap<=c.geometry_tol: return elapsed,index
        if elapsed>=dt: return None
        increment=max(c.event_time_tol*.1,min(.8*g/speed for g,_,speed in candidates))
        elapsed=min(dt,elapsed+increment)
    raise ArithmeticError('Swept contact search iteration limit')

def advance(c,body,stocks,t,phase,command,dt,allow_terminal=False):
    body.command=np.asarray(command).copy(); body.force=actuator_forces(c,body,command)
    events=[]; elapsed=0.; impulses_by_sector=np.zeros(8); loops=0
    def append_record(record,time):
        record['time']=time; record['body_position']=body.position.copy(); record['body_angle']=body.angle
        events.append(record)
        for contact in record['contacts']:
            normal=contact['normal']; angle=(math.atan2(-normal[1],-normal[0])-body.angle)%(2*np.pi)
            address=angle/(2*np.pi)*8; lower=int(math.floor(address))%8; f=address-math.floor(address)
            impulses_by_sector[lower]+=contact['impulse']*(1-f); impulses_by_sector[(lower+1)%8]+=contact['impulse']*f
    while elapsed<dt-1e-14:
        loops+=1
        if loops>200: raise ArithmeticError('Physical event subdivision limit')
        now=t+elapsed; remaining=dt-elapsed; scene=fixtures(c,now,phase)
        active=[]; normals=[]
        for i,f in enumerate(scene):
            gap,normal=gap_normal(body.position,c.body_radius,f)
            if gap < -c.overlap_tol: raise ArithmeticError(f"Rigid overlap {f['id']}: {gap}")
            if gap<=c.geometry_tol*2: active.append(i); normals.append(normal)
        if active:
            bounds=[float(normals[j]@scene[i]['velocity']) for j,i in enumerate(active)]
            v,impulses=project_velocity(body.velocity,normals,bounds,c.body_mass)
            if impulses.sum()>1e-12:
                body.velocity=v
                contacts=[contact_record(c,body,scene[i],normals[j],impulses[j]) for j,i in enumerate(active) if impulses[j]>0]
                append_record(account(c,body,stocks,contacts,0,True),now)
                if body.integrity<=0:
                    body.contact_rates=impulses_by_sector/max(elapsed,c.event_time_tol)
                    if allow_terminal: return events,elapsed,'integrity'
                    raise TerminalCrossing(elapsed,'integrity',events)
        # Freeze force for this physical subinterval, using its actual starting
        # reserves (including damage at an immediately preceding impact).
        body.force=actuator_forces(c,body,body.command)
        collision=first_collision(c,body,body.force,now,phase,remaining,set(active))
        interval=remaining if collision is None else collision[0]
        if interval<c.event_time_tol*.01:
            # A newly located touch joins the next exact constraint solve.
            if collision is None: raise ArithmeticError('Zero-duration physical advance')
            f=scene[collision[1]]; gap,_=gap_normal(body.position,c.body_radius,f)
            if gap>c.geometry_tol*2: raise ArithmeticError('Contact event failed to bracket')
            if collision[1] in active: raise ArithmeticError('Unresolved repeating impact')
            continue
        velocity,omega=free_velocity(c,body,body.force,interval)
        contacts=[]
        if active:
            end_scene=fixtures(c,now+interval,phase)
            bounds=[]
            for j,i in enumerate(active):
                f=scene[i]; n=normals[j]
                if f['id']=='mover':
                    displacement=(end_scene[i]['rect'][0]-f['rect'][0])/interval
                    bounds.append(float(n@np.array([displacement,0.])))
                else: bounds.append(0.)
            velocity,impulses=project_velocity(velocity,normals,bounds,c.body_mass)
            body.velocity=velocity; body.omega=omega
            contacts=[contact_record(c,body,scene[i],normals[j],impulses[j]) for j,i in enumerate(active) if impulses[j]>0]
        body.velocity=velocity; body.omega=omega
        body.position=body.position+interval*velocity; body.angle+=interval*omega
        record=account(c,body,stocks,contacts,interval); elapsed+=interval
        append_record(record,t+elapsed)
        if body.energy<=0 or body.integrity<=0:
            dimension='energy' if body.energy<=0 else 'integrity'
            if not allow_terminal: raise TerminalCrossing(elapsed,dimension,events)
            body.contact_rates=impulses_by_sector/max(elapsed,c.event_time_tol)
            return events,elapsed,dimension
        if collision is not None:
            # Next loop processes the zero-duration impact at this location.
            continue
    body.contact_rates=impulses_by_sector/dt
    for f in fixtures(c,t+dt,phase):
        gap,_=gap_normal(body.position,c.body_radius,f)
        if gap < -c.overlap_tol: raise ArithmeticError(f"Ending overlap {f['id']}: {gap}")
    return events,elapsed,None
