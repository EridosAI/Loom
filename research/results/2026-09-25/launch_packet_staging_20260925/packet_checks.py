"""Read-only first-packet calculations. No Run, step, account or replay calls."""
import copy
import math
import numpy as np
from loom_p.geometry import fixtures,gap_normal,mover
from loom_p.records import state_hash,view
from loom_commissioning.authority import validate_execution,validate_dispatch,execution_sha256
from loom_commissioning.contract import validate_manifest
from loom_commissioning import runner
from loom_commissioning.controllers import privileged_input,validate_privileged,SensorHistory,validate_sensor_payload,observe_without_interference
from loom_commissioning.validators import validate_ledger

def v1(engine,manifest):
    before=state_hash(engine)
    validate_manifest(manifest,engine);validate_execution(manifest,complete=True)
    validate_dispatch(manifest,vars(runner))
    assert before==state_hash(engine)
    return {'valid':True,'state_sha256':before,'execution_sha256':execution_sha256(manifest),
            'native_index':engine.native_index,'time':engine.time,'state_unchanged':True}

def v3(engine):
    before=state_hash(engine)
    privileged=observe_without_interference(engine,privileged_input);validate_privileged(privileged)
    raw=SensorHistory(engine).display();validate_sensor_payload(raw)
    assert state_hash(engine)==before
    return {'privileged_actual_input':privileged,'separate_raw_observer_payload':raw,
            'state_unchanged':True,'scope':'Initial live-object read only; no sensory trial and no command produced.'}

def _segment_gap(a,b,f,radius):
    a=np.asarray(a,float);b=np.asarray(b,float)
    if f['kind']=='disk':
        delta=b-a;u=float(np.clip((np.asarray(f['centre'])-a)@delta/(delta@delta),0,1))
        return float(np.linalg.norm(a+u*delta-f['centre'])-radius-f['radius'])
    if f['kind']=='wall':return min(gap_normal(a,radius,f)[0],gap_normal(b,radius,f)[0])
    assert a[0]==b[0] or a[1]==b[1]
    x0,x1,y0,y1=f['rect'];lo=np.minimum(a,b);hi=np.maximum(a,b)
    dx=max(x0-hi[0],lo[0]-x1,0.);dy=max(y0-hi[1],lo[1]-y1,0.)
    # Exact outside-clearance for these disjoint axis-aligned witness segments.
    assert dx>0 or dy>0
    return float(math.hypot(dx,dy)-radius)

def a0(c,phase):
    scene=fixtures(c,0.,phase)
    approach=([6.,3.],[4.,3.]);bypass=([1.5,6.],[1.5,14.])
    out={}
    for name,(a,b) in [('A1_centre_segment_to_contact_locus',approach),('A0_only_left_bypass',bypass)]:
        static={f['id']:_segment_gap(a,b,f,c.body_radius) for f in scene if f['id']!='mover'}
        swept={'kind':'rect','rect':[5.,15.,9.5,10.5]}
        out[name]={'from':a,'to':b,'static_surface_clearances':static,
                   'minimum_to_mover_union_over_all_phases':_segment_gap(a,b,swept,c.body_radius)}
    assert min(out['A1_centre_segment_to_contact_locus']['static_surface_clearances'].values())>=-c.geometry_tol
    assert out['A1_centre_segment_to_contact_locus']['static_surface_clearances']['source-0']==0
    assert min(out['A0_only_left_bypass']['static_surface_clearances'].values())>0
    out['phase_snapshots']=[{'at_time':t,'mover_rect':mover(c,t,phase)[0].tolist(),
        'mover_velocity':mover(c,t,phase)[1].tolist(),
        'probe_10_10_surface_gap':float(gap_normal(np.array([10.,10.]),c.body_radius,fixtures(c,t,phase)[-1])[0])}
        for t in (0.,7.5,15.,22.5,30.)]
    out['scope']='Finite-radius geometry only. No point-agent path, world evolution, reserve-feasibility claim or alternative A1 trajectory. Mover union used only to certify a bypass, never as a permanent exclusion of its whole swept area.'
    return out

def v2(events,c):
    maximum=validate_ledger(events,c.arithmetic_tol)
    rows=[]
    for index,e in enumerate(events):
        transfer=math.fsum(e['transfer']);renew=np.asarray(e['renewal_first'])+e['renewal_second']
        rows.append({'event_index':index,'time':e.get('time'),'duration':e['duration'],
            'contacts':copy.deepcopy(e['contacts']),'event_kind':e.get('event_kind'),
            'body_position':e.get('body_position'),'body_angle':e.get('body_angle'),
            'source_debit':(np.asarray(e['stock_before'])+renew-np.asarray(e['stock_after'])).tolist(),
            'transfer':copy.deepcopy(e['transfer']),'body_credit':e['energy_after']-e['energy_before']+e['expenditure'],
            'energy_delta':e['energy_after']-e['energy_before'],'expenditure':e['expenditure'],
            'energy_residual':(e['energy_after']-e['energy_before'])-(transfer-e['expenditure']),
            'damage':e['damage'],'restoration':e['repair']})
    return {'maximum_ledger_residual':maximum,'existing_arithmetic_tolerance':c.arithmetic_tol,'rows':rows}

def a1_interpret(initial,native,events,c):
    """All fixed 20-native-sample windows; no useful-behavior pass gate."""
    accounting=v2(events,c)
    source=lambda e:any(x.get('source')==0 and x.get('collider')=='source-0' for x in e['contacts'])
    gaps=[float(np.linalg.norm(np.asarray(initial.body.position)-c.source_positions[0])-c.body_radius-c.source_radius)]
    gaps += [float(np.linalg.norm(np.asarray(n['position'])-c.source_positions[0])-c.body_radius-c.source_radius) for n in native]
    gaps += [float(np.linalg.norm(np.asarray(e['body_position'])-c.source_positions[0])-c.body_radius-c.source_radius) for e in events if 'body_position' in e]
    contacts=[{'event_index':i,**copy.deepcopy(e)} for i,e in enumerate(events) if source(e)]
    windows=[]
    for start in range(0,len(native),20):
        block=native[start:start+20]
        t0=initial.time if start==0 else native[start-1]['time']
        e0=initial.body.energy if start==0 else native[start-1]['reserves'][0]
        t1=block[-1]['time'];e1=block[-1]['reserves'][0]
        ix=[i for i,e in enumerate(events) if e['duration']>0 and e['time']>t0+c.event_time_tol and e['time']<=t1+c.event_time_tol]
        chosen=[events[i] for i in ix]
        complete=len(block)==20 and abs(t1-t0-c.wave_dt)<=c.event_time_tol
        residual=math.fsum(abs(accounting['rows'][i]['energy_residual']) for i in ix)
        # Propagate the existing per-event arithmetic allowance, plus one
        # endpoint subtraction allowance. This is not a biological effect size.
        allowance=residual+(len(ix)+1)*c.arithmetic_tol
        delta=e1-e0;transfer=math.fsum(math.fsum(e['transfer']) for e in chosen)
        has_contact=any(source(e) for e in chosen)
        sign='positive_resolved' if delta>allowance else 'negative_resolved' if delta < -allowance else 'unresolved_at_accounting_resolution'
        windows.append({'first_native':block[0]['native_index'],'last_native':block[-1]['native_index'],
            'start_time':t0,'end_time':t1,'complete_0_2_second_interval':complete,
            'energy_before':e0,'energy_after':e1,'energy_delta':delta,'source_0_transfer':math.fsum(e['transfer'][0] for e in chosen),
            'all_source_transfer':transfer,'expenditure':math.fsum(e['expenditure'] for e in chosen),
            'source_0_positive_duration_contact':has_contact,'absolute_energy_residual_sum':residual,
            'propagated_arithmetic_allowance':allowance,'net_energy_sign':sign,
            'positive_net_contact_interval':bool(complete and has_contact and delta>allowance)})
    return {'classification':'A1 / apparatus validity observations; no P PASS/FAIL',
        'minimum_source_surface_gap':min(gaps),
        'geometric_contact_locus_reached':min(gaps)<=2*c.geometry_tol and min(gaps)>=-c.overlap_tol,
        'certified_source_contact_events':contacts,'ledger':accounting,'all_fixed_windows':windows,
        'interpretation':'A transfer-only witness is informative; controller failure is not physical impossibility. Terminal partial windows are retained separately through complete_0_2_second_interval=false. No learning/survival/developmental selection.'}
