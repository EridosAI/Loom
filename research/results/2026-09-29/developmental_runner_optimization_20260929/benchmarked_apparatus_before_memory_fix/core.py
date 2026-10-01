"""Transaction scheduler around the unchanged P causal operations.

Native rollback copies only fields mutated in-place before commit. Static field
geometry, configuration, matrices and non-writing wave state are shared. Rare
terminal root-finding remains the exact baseline algorithm, using complete copies.
"""
import copy
import numpy as np
from loom_p.engine import Engine
from loom_p.physics import TerminalCrossing

def backup(e):
    old=copy.copy(e)
    old.body=copy.deepcopy(e.body);old.stocks=e.stocks.copy()
    old.solver=copy.copy(e.solver)
    o=e.organism;old.organism=copy.copy(o);b=old.organism
    b.rng=copy.copy(o.rng);b.rng.counters=o.rng.counters.copy()
    b.cortices=[]
    for c in o.cortices:
        saved=copy.copy(c)
        for name in ('shared','fine','integral'):setattr(saved,name,getattr(c,name).copy())
        b.cortices.append(saved)
    b.motor=copy.copy(o.motor)
    b.motor.phase=o.motor.phase.copy();b.motor.integral=o.motor.integral.copy()
    if (e.native_index+1)%round(e.c.wave_dt/e.c.native_dt)==0:
        b.association=copy.deepcopy(o.association)
        b.regulator=copy.deepcopy(o.regulator)
    return old

def cheap_finite(e,wave):
    arrays=[e.body.position,e.body.velocity,e.body.command,e.body.force,e.body.reserves,*e.raw,
            e.organism.motor.command,e.organism.motor.phase,e.organism.motor.nu]
    for c in e.organism.cortices:
        arrays.extend((c.x,c.shared,c.fine,c.mean,c.C,c.integral,c.shared_ref,c.fine_ref,c.opening))
    if wave:
        a=e.organism.association;r=e.organism.regulator
        arrays.extend((a.a,a.q,r.theta,r.reference,r.eligibility,r.controls,*a.H.values(),*a.use.values()))
    if any(not np.isfinite(x).all() for x in arrays):raise ValueError('Nonfinite committed causal state')

def step(e):
    """Same operation order/terminal search as Engine.step; no live observer work."""
    if e.status in ('failure','terminal','budget_complete'):raise RuntimeError('Stopped state cannot advance')
    old=backup(e);dt=e.c.native_dt
    refresh=e.native_index>0 and e.native_index%round(e.c.noise_refresh/dt)==0
    terminal=None
    try:
        try:terminal=Engine._coupled(e,dt,refresh)
        except TerminalCrossing as event:
            low=0.;high=dt;dimension=event.dimension
            for _ in range(80):
                mid=(low+high)/2;candidate=copy.deepcopy(old)
                try:
                    Engine._coupled(candidate,mid,refresh);low=mid
                except TerminalCrossing:high=mid
                if high-low<=e.c.event_time_tol:break
            else:raise ArithmeticError('Terminal location did not converge')
            e.__dict__=copy.deepcopy(old.__dict__)
            terminal=Engine._coupled(e,high,refresh,True) or dimension;dt=high
        e.native_index+=1;e.last_wave=None
        if terminal:e.status='terminal';e.terminal_dimension=terminal
        elif e.native_index%round(e.c.wave_dt/e.c.native_dt)==0:
            e.last_wave=e.organism.handoff(e.body.reserves)
        # This cache is observer-only; complete native observation is recreated
        # from Tier 1 and neural replay instead of copying/hashing it every step.
        e.last_native={'time':e.time,'elapsed':dt,'native_index':e.native_index}
        cheap_finite(e,e.last_wave is not None)
        return dt,e.last_wave,e.last_events
    except Exception as error:
        e.__dict__=old.__dict__;e.status='failure';e.failure=f'{type(error).__name__}: {error}'
        raise

def causal_state(e):
    """Only the observer native cache differs; every other Engine field compares."""
    return {k:v for k,v in vars(e).items() if k!='last_native'}
