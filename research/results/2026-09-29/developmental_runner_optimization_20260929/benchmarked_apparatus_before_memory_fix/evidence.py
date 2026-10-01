"""Tier-1 observations: columnar native facts and compact actual wave outputs."""
import numpy as np
from loom_p.geometry import mover

NATIVE_FIELDS=[('time',1),('elapsed',1),('position',2),('angle',1),('velocity',2),('omega',1),
    ('commands',2),('forces',2),('contact_rates',8),('reserves',2),('stocks',8),
    ('raw',29),('mover_rectangle',4),('mover_velocity',2),('rng_dynamic',3),
    ('field_iterations',1),('field_relative_residual',2),('field_mass_balance',2),
    ('field_minimum',1),('field_negative_roundoff_count',1),('event_count',1)]
SLICES={};WIDTH=0
for name,width in NATIVE_FIELDS:SLICES[name]=slice(WIDTH,WIDTH+width);WIDTH+=width
DYNAMIC=('life/motor-noise','life/regulation-E','life/regulation-I')

def native_row(e,dt):
    rect,velocity=mover(e.c,e.time,e.phase);b=e.body;s=e.solver.last
    values=(e.time,dt,*b.position,b.angle,*b.velocity,b.omega,*b.command,*b.force,
        *b.contact_rates,*b.reserves,*e.stocks,*np.concatenate(e.raw),*rect,*velocity,
        *(e.organism.rng.counters[k] for k in DYNAMIC),s['iterations'],
        *s['relative_residual'],*s['mass_balance'],s['minimum'],s['negative_roundoff_count'],len(e.last_events))
    if any(e.organism.rng.counters[k]>2**53 for k in DYNAMIC):raise ValueError('native counter exact-integer bound')
    return np.asarray(values,dtype='<f8')

def raw_tuple(row):
    x=row[SLICES['raw']];return (x[:10].copy(),x[10:14].copy(),x[14:22].copy(),x[22:].copy())

def wave_row(e,w):
    """No new neural calculations; only compact outputs already computed by P."""
    a=w['association'];r=w['regulation'];credit=w['credit']
    summaries=np.stack([np.concatenate([v[name] for name in ('new_norm','use')])
        for v in a['map_updates'].values()])
    return {'index':e.native_index,'wave':e.organism.wave_count,
        'packets':np.concatenate(w['packets']),
        'psi':w['psi'],'q':a['q'],'controls':w['new_controls'],
        'credit_trend':credit['trend'],
        'learned':r['learned'],'exploration':r['exploration'],'need':r['need'],
        'map_update_use':summaries,
        'sensory_shared_norm':np.array([np.linalg.norm(c.shared) for c in e.organism.cortices]),
        'sensory_fine_norm':np.array([np.linalg.norm(c.fine) for c in e.organism.cortices]),
        'pool_opening':np.concatenate([c.opening for c in e.organism.cortices]),
        'regulator_bank_norm':np.linalg.norm(e.organism.regulator.theta,axis=(1,2))}

def check_ledger(events,tolerance):
    maximum=0.
    for r in events:
        transfer=np.asarray(r['transfer']);renew=np.asarray(r['renewal_first'])+r['renewal_second']
        errors=((r['energy_after']-r['energy_before'])-(float(transfer.sum())-r['expenditure']),
            float(np.max(abs(np.asarray(r['stock_after'])-r['stock_before']-renew+transfer))),
            r['integrity_after']-r['integrity_before']-(r['repair']-r['damage']))
        if not np.isfinite(errors).all() or max(abs(x) for x in errors)>tolerance:
            raise ArithmeticError('source/energy/integrity ledger mismatch')
        if r['duration']==0 and (np.any(transfer) or r['expenditure']!=0 or r['repair']!=0):
            raise ArithmeticError('zero-duration exchange')
        maximum=max(maximum,*map(abs,errors))
    return maximum
