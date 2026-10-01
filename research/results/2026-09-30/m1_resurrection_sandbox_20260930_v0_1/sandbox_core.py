"""NON-CANONICAL RESURRECTION SANDBOX. Narrow scheduler and explicit intervention.

Uses the corrected Engine._coupled without rebinding or modifying it. Fractional
terminal and administrative endpoints are accepted integration calls, as in the
baseline terminal search. Absolute physical time and all history counts persist.
After death a fresh 0.2-s packet window starts at the intervention time. Otherwise
wave elapsed time, including administrative partial windows, is preserved.
"""
import paths
import copy,hashlib
import numpy as np
from loom_p.engine import Engine
from loom_p.physics import TerminalCrossing
from loom_developmental.core import backup,cheap_finite
from loom_motor_commissioning import codec

LABEL='NON-CANONICAL RESURRECTION SANDBOX'

def initialize(e):
    if hasattr(e,'sandbox') or e.time!=0 or e.native_index!=0:raise ValueError('sandbox installation at blank birth only')
    if e.organism.motor.commissioning['process']!='M1':raise ValueError('M1 only')
    e.sandbox=dict(label=LABEL,resurrections=0,packet_epoch_time=0.,packet_epoch_native=0,discarded_partial_seconds=0.)
    return e

def step(e,end_age):
    if e.status in ('failure','terminal','budget_complete'):raise RuntimeError('stopped state')
    if not e.time<end_age<=4500:raise ValueError('absolute age boundary')
    if e.organism.motor.commissioning['process']!='M1':raise ValueError('M1 required')
    remaining_wave=e.c.wave_dt-e.organism.wave_elapsed
    dt=min(e.c.native_dt,end_age-e.time)
    if remaining_wave<dt-1e-12:dt=remaining_wave
    if not 0<dt<=e.c.native_dt:raise ArithmeticError('invalid fractional native interval')
    due=e.organism.wave_elapsed+dt>=e.c.wave_dt-1e-12
    old=backup(e)
    # Baseline backup detects index-aligned waves. Intervention epochs can be
    # off that index grid, so protect the same in-place writers when due here.
    if due:
        old.organism.association=copy.deepcopy(e.organism.association)
        old.organism.regulator=copy.deepcopy(e.organism.regulator)
    refresh=e.native_index>0 and e.native_index%round(e.c.noise_refresh/e.c.native_dt)==0
    terminal=None
    try:
        try:terminal=Engine._coupled(e,dt,refresh)
        except TerminalCrossing as event:
            low=0.;high=dt;dimension=event.dimension
            for _ in range(80):
                mid=(low+high)/2;candidate=copy.deepcopy(old)
                try:Engine._coupled(candidate,mid,refresh);low=mid
                except TerminalCrossing:high=mid
                if high-low<=e.c.event_time_tol:break
            else:raise ArithmeticError('terminal root did not converge')
            e.__dict__=copy.deepcopy(old.__dict__)
            terminal=Engine._coupled(e,high,refresh,True) or dimension;dt=high
        e.native_index+=1;e.last_wave=None
        if terminal:e.status='terminal';e.terminal_dimension=terminal
        elif e.organism.wave_elapsed>=e.c.wave_dt-1e-12:e.last_wave=e.organism.handoff(e.body.reserves)
        e.last_native=dict(time=e.time,elapsed=dt,native_index=e.native_index)
        cheap_finite(e,e.last_wave is not None)
        if e.time>end_age:raise ArithmeticError('age ceiling exceeded')
        if e.organism.motor.commissioning['tick']!=e.native_index:raise ArithmeticError('M1/native counter continuity')
        return dt,e.last_wave,e.last_events
    except Exception as error:
        e.__dict__=old.__dict__;e.status='failure';e.failure=f'{type(error).__name__}: {error}';raise

def protected_state(e):
    """Everything must match except the explicit boundary allowlist."""
    p=copy.deepcopy(e);p.status='paused';p.terminal_dimension=None
    p.body.energy=0.;p.body.integrity=0.
    r=p.organism.regulator;a=p.organism.association
    r.body_mean=np.zeros(2)
    for d in (4,5):a.means[d]=np.zeros_like(a.means[d]);a.traces[d]=np.zeros_like(a.traces[d])
    for c in p.organism.cortices:c.integral.fill(0)
    p.organism.motor.integral.fill(0);p.organism.wave_elapsed=0.
    p.sandbox=dict(label=LABEL)
    return codec.digest(p)

def resurrect(e):
    if e.status!='terminal' or e.failure is not None:raise ValueError('genuine terminal boundary required')
    reserves=e.body.reserves.copy();dead=reserves<=0
    if not dead.any():raise ValueError('terminal flag without nonviable reserve')
    if e.terminal_dimension not in ('energy','integrity'):raise ValueError('unknown terminal cause')
    if not dead[0 if e.terminal_dimension=='energy' else 1]:raise ValueError('terminal cause disagrees with reserve')
    before=codec.digest(e);protected=protected_state(e);o=e.organism;r=o.regulator;a=o.association
    counters=(e.native_index,o.native_count,o.wave_count,a.write_count)
    unchanged=codec.digest((r.theta,r.reference,r.eligibility,o.motor.commissioning,o.rng,a.H,a.use))
    old=dict(reserves=reserves.copy(),body_mean=r.body_mean.copy(),EI_means=[x.copy() for x in a.means[4:6]],
        EI_traces=[x.copy() for x in a.traces[4:6]],wave_elapsed=o.wave_elapsed,
        sensory_integrals=[x.integral.copy() for x in o.cortices],motor_integral=o.motor.integral.copy())
    if dead[0]:e.body.energy=e.c.birth_energy
    if dead[1]:e.body.integrity=1.
    for d in np.flatnonzero(dead):
        r.body_mean[d]=e.body.reserves[d]
        a.means[4+d]=np.array([e.body.reserves[d]])
        a.traces[4+d]=np.zeros_like(a.traces[4+d])
    # Discard unfinished packet integrals without a handoff, bank update, map
    # write or RNG draw. No sensory weights/means, H/use, bank/eligibility or
    # expressed motor/control state is reset.
    for c in o.cortices:c.integral.fill(0)
    o.motor.integral.fill(0);o.wave_elapsed=0.
    e.sandbox=dict(e.sandbox,resurrections=e.sandbox['resurrections']+1,packet_epoch_time=e.time,
        packet_epoch_native=e.native_index,discarded_partial_seconds=e.sandbox['discarded_partial_seconds']+old['wave_elapsed'])
    e.status='paused';e.terminal_dimension=None
    assert protected_state(e)==protected
    assert unchanged==codec.digest((r.theta,r.reference,r.eligibility,o.motor.commissioning,o.rng,a.H,a.use))
    assert counters==(e.native_index,o.native_count,o.wave_count,a.write_count)
    assert np.array_equal(e.body.reserves[~dead],reserves[~dead])
    assert np.array_equal(r.body_mean[~dead],old['body_mean'][~dead])
    for d in np.flatnonzero(~dead):
        assert np.array_equal(a.means[4+d],old['EI_means'][d]) and np.array_equal(a.traces[4+d],old['EI_traces'][d])
    # Manufactured credit probe on a COPY with reserves held fixed. The jump
    # contributes zero trend/learning; normal reference drift is not suppressed.
    test=copy.deepcopy(r);test.credit(e.c,e.body.reserves)
    assert np.all(test.credit_diagnostic['trend'][dead]==0)
    assert np.all(test.credit_diagnostic['learning'][dead]==0)
    e.validate_state()
    return dict(label=LABEL,kind='EXTERNAL_RESURRECTION_INTERVENTION',time=e.time,index=e.native_index,
        ordinal=e.sandbox['resurrections'],restored_dimensions=[('energy','integrity')[i] for i in np.flatnonzero(dead)],
        before_sha256=before,after_sha256=codec.digest(e),protected_sha256=protected,old_transients=old,
        restored_reserves=e.body.reserves.copy(),external_support=e.body.reserves-reserves,
        zero_immediate_credit=True,zero_learning_from_jump=True,long_term_and_RNG_identical=True,
        affected_body_mean=r.body_mean.copy(),packet_epoch=e.sandbox.copy())
