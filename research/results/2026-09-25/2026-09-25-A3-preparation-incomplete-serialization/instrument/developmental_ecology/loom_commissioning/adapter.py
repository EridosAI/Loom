"""External interventions around unchanged P operations; no persistent patching."""
import copy
import numpy as np
from loom_p.engine import Engine
from loom_p.physics import advance, TerminalCrossing
from loom_p.geometry import transduce
from loom_p.records import state_hash
from .contract import INTACT, FIXED, EXTERNAL, require

SENSORY = ('shared', 'fine', 'shared_ref', 'fine_ref')

def structure(o):
    return {'sensory':[{k:getattr(x,k).copy() for k in SENSORY} for x in o.cortices],
            'H':copy.deepcopy(o.association.H), 'use':copy.deepcopy(o.association.use),
            'theta':o.regulator.theta.copy(), 'reference':o.regulator.reference.copy()}

def restore_sensory(o, frozen):
    for x, values in zip(o.cortices, frozen['sensory']):
        for k, v in values.items(): setattr(x, k, v.copy())

def restore_maps(o, frozen):
    o.association.H = copy.deepcopy(frozen['H'])
    o.association.use = copy.deepcopy(frozen['use'])

def restore_banks(o, frozen):
    o.regulator.theta = frozen['theta'].copy()
    o.regulator.reference = frozen['reference'].copy()

def validate_frozen(o, frozen):
    require(state_hash(structure(o)) == state_hash(frozen), 'frozen structural parameter changed')

def fixed_native(o, raw, dt, refresh, frozen):
    validate_frozen(o, frozen)
    command = o.native(raw, dt, refresh)
    hypothetical = structure(o)['sensory']
    restore_sensory(o, frozen)  # x/C/mean/opening used the ordinary old-state RHS.
    return command, {'hypothetical_sensory':hypothetical, 'applied_structural_increment':0}

def fixed_handoff(o, reserves, frozen):
    """P handoff order, with bank restore BEFORE output and maps BEFORE next read."""
    validate_frozen(o, frozen)
    c=o.c; r=o.regulator; a=o.association
    require(abs(o.wave_elapsed-c.wave_dt)<1e-10, 'No handoff on partial wave')
    old_controls=r.controls.copy()
    packets=[x.packet(c.wave_dt) for x in o.cortices]+[np.array([reserves[0]]),np.array([reserves[1]]),
             np.concatenate((o.motor.integral/c.wave_dt,o.motor.command)),old_controls]
    o.motor.integral.fill(0)
    beta,psi,old_means=a.packets_to_context(c,packets)
    r.credit(c,np.asarray(reserves))
    discarded_bank=copy.deepcopy(r.credit_diagnostic)
    restore_banks(o, frozen)
    gates,contributions=a.read(c,psi,r.h.copy())
    r.output(c,o.rng,a.q,np.asarray(reserves))
    a.write(c,psi,beta,gates,contributions)
    discarded_maps=copy.deepcopy(a.diagnostic['map_updates'])
    restore_maps(o, frozen)
    o.wave_count+=1; o.wave_elapsed=0.
    o.last_wave=dict(wave=o.wave_count,packets=packets,old_means=old_means,beta=beta,
        traces=copy.deepcopy(a.traces),psi=psi,old_controls=old_controls,new_controls=r.controls.copy(),
        association=copy.deepcopy(a.diagnostic),credit=discarded_bank,regulation=copy.deepcopy(r.output_diagnostic),
        ordering=['packet','previous_credit','restore_banks','old_map_read_4_sweeps_final_q',
                  'new_draw_controls','hypothetical_map_write_use_means','restore_maps_use'],
        diagnostic_label=FIXED,structural_updates='discarded_hypothetical',applied_structural_increment=0,
        discarded_maps=discarded_maps)
    validate_frozen(o, frozen)
    return o.last_wave

def coupled(e, dt, refresh, mode, command, frozen, allow_terminal=False):
    discarded=None
    if mode==FIXED:
        delivered, discarded=fixed_native(e.organism,e.raw,dt,refresh,frozen)
    else:
        delivered=np.array(command,dtype=float).copy()
    events,actual,terminal=advance(e.c,e.body,e.stocks,e.time,e.phase,delivered,dt,allow_terminal)
    if actual<dt-e.c.event_time_tol and not allow_terminal: raise ArithmeticError('Short physics without terminal')
    e.fields=e.solver.step(e.fields,e.stocks,e.time+dt,e.phase,dt,e.body.position)
    e.time+=dt; e.last_events=events
    e.raw=transduce(e.c,e.body,e.fields,e.time,e.phase)
    return terminal,discarded

def step(e, mode, command=None, frozen=None):
    """Intact P delegates directly. Modified arms retain the Engine.step schedule.

    Candidate terminal substeps are discarded copies, including their RNG state.
    External arms never advance the stored, inactive newborn neural object.
    """
    if mode==INTACT:
        n,w,ev=e.step(); return n,w,ev,None
    require(mode in (FIXED,EXTERNAL), 'unknown adapter mode')
    require(e.status not in ('failure','terminal','budget_complete'), 'Stopped state cannot advance')
    if mode==EXTERNAL:
        command=np.asarray(command,dtype=float)
        require(command.shape==(2,) and np.isfinite(command).all() and (abs(command)<=1).all(), 'invalid actuator command')
    old=copy.deepcopy(e); dt=e.c.native_dt
    refresh=e.native_index>0 and e.native_index%round(e.c.noise_refresh/dt)==0
    try:
        try: terminal,discarded=coupled(e,dt,refresh,mode,command,frozen)
        except TerminalCrossing as event:
            low=0.; high=dt; dimension=event.dimension
            for _ in range(80):
                mid=(low+high)/2; candidate=copy.deepcopy(old)
                try: coupled(candidate,mid,refresh,mode,command,frozen); low=mid
                except TerminalCrossing: high=mid
                if high-low<=e.c.event_time_tol: break
            else: raise ArithmeticError('Terminal location did not converge')
            e.__dict__=copy.deepcopy(old.__dict__)
            terminal,discarded=coupled(e,high,refresh,mode,command,frozen,True)
            terminal=terminal or dimension; dt=high
        e.native_index+=1; e.last_wave=None
        if terminal:
            e.status='terminal'; e.terminal_dimension=terminal
        elif e.native_index%round(e.c.wave_dt/e.c.native_dt)==0 and mode==FIXED:
            e.last_wave=fixed_handoff(e.organism,e.body.reserves,frozen)
        e.last_native=e.observe_native(dt)
        e.validate_state()
        return e.last_native,e.last_wave,e.last_events,discarded
    except Exception as error:
        e.__dict__=old.__dict__; e.status='failure'; e.failure=f'{type(error).__name__}: {error}'
        raise
