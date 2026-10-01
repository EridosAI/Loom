"""Predetermined A4 measurements from immutable saved records; standard library only."""
from a4_window_helpers import *

def mover_at(c,t,phase):
    theta=2*math.pi*t/c['mover_period']+phase
    x=c['mover_centre'][0]+c['mover_amplitude']*math.sin(theta);y=c['mover_centre'][1];w,h=c['mover_size']
    return {'rectangle':[x-w/2,x+w/2,y-h/2,y+h/2],'centre':[x,y],
            'velocity':[c['mover_amplitude']*2*math.pi/c['mover_period']*math.cos(theta),0.],
            'phase_parameter':phase,'wrapped_phase_at_time':theta%(2*math.pi),'pose_provenance':'Derived from the bound law at saved time; no dynamics'}

def physical_observations(d,ledger,windows):
    c=d.initial['c'];m=d.manifest;cid=m['case_id'];wait=m['execution']['procedure']['protocol']['prescribed_wait_seconds']
    start=d.initial['body'];goal=m['execution']['procedure']['stages'][-1]['point'];end=d.final['time'];r=c['body_radius']
    poses=[{'native_index':0,'time':0.,'position':start['position'],'angle':start['angle'],'velocity':start['velocity'],'omega':start['omega'],'reserves':[start['energy'],start['integrity']],'commands':start['command'],'elapsed':0.}]
    poses += [{k:n[k] for k in ('native_index','time','position','angle','velocity','omega','reserves','commands','elapsed')} for n in d.native]
    length=[0.]
    for a,b in zip(poses,poses[1:]):length.append(length[-1]+math.dist(a['position'],b['position']))
    def mark(i):
        if i is None:return {'observed':False,'time':None,'reason':'Not recorded within this case'}
        p=poses[i];prev=poses[max(0,i-1)]
        return {'observed':True,'time':p['time'],'native_index':p['native_index'],'position':p['position'],'angle':p['angle'],'speed':math.hypot(*p['velocity']),'E_I':p['reserves'],'commands':p['commands'],'mover':mover_at(c,p['time'],m['phase']),
          'preceding_native_or_initial':{k:prev[k] for k in ('native_index','time','position','reserves')},'time_meaning':'First saved native endpoint satisfying definition (or initial state); actual crossing is bracketed, not interpolated','sampled_path_length_from_start':length[i]}
    def first(pred,start_index=0):return next((i for i in range(start_index,len(poses)) if pred(poses[i])),None)
    approach=first(lambda p:8<=p['position'][1]<9)
    entry=first(lambda p:p['position'][1]>=9)
    centre=first(lambda p:p['position'][1]>=10,entry or 0)
    exit_=first(lambda p:p['position'][1]>11,entry or 0)
    arrival=first(lambda p:math.dist(p['position'],goal)<=.25)
    release_index=next((i for i,p in enumerate(poses) if abs(p['time']-wait)<=TOL),None) if wait else 0
    reentries=[mark(i) for i in range((exit_ or len(poses))+1,len(poses)) if poses[i-1]['position'][1]>11 and poses[i]['position'][1]<=11]
    departures=[mark(i) for i in range((arrival or len(poses))+1,len(poses)) if math.dist(poses[i-1]['position'],goal)<=.25 and math.dist(poses[i]['position'],goal)>.25]
    samples=[]
    for p in poses:
        mover=mover_at(c,p['time'],m['phase']);g=rect_gap(p['position'],mover['rectangle'],r)
        samples.append({'native_index':p['native_index'],'time':p['time'],'body_position':p['position'],'body_angle':p['angle'],'signed_gap':g,'mover':mover})
    def min_sample(rows):return min(rows,key=lambda x:x['signed_gap']) if rows else None
    controller_samples=[]
    for a in d.controller:
        f=next(f for f in a['inputs']['geometry'] if f['id']=='mover')
        controller_samples.append({'time':a['time'],'native_index':a['native_index'],'body_position':a['inputs']['position'],'body_angle':a['inputs']['angle'],'signed_gap':rect_gap(a['inputs']['position'],f['rect'],r),'recorded_mover_rectangle':f['rect'],'recorded_mover_velocity':f['velocity'],'phase_parameter':a['inputs']['mover_phase'],'pose_provenance':'Actual privileged controller input sample'})
    waiting_samples=[s for s in samples if s['time']<=wait+TOL] if wait else []
    crossing_samples=[s for s in samples if entry is not None and s['time']>=poses[entry]['time']-TOL and s['time']<=(poses[exit_]['time'] if exit_ is not None else end)+TOL]
    contact_events=[];labels=collections.Counter();impacts=[];sustained=[];boundaries=[]
    for i,e in enumerate(d.events):
        if e.get('event_kind') in ('release','contact','impact') or e.get('colliders'):boundaries.append(compact_event(i,e))
        if e['contacts']:
            row=compact_event(i,e);contact_events.append(row)
            for contact in e['contacts']:labels[contact['collider']]+=1
            if e['impact']:impacts.append(row)
            elif e['duration']>0:sustained.append(row)
    mover_events=[row for row in contact_events if any(x['collider']=='mover' for x in row['contacts'])]
    mover_impacts=[row for row in mover_events if row['impact']]
    mover_spans=contact_intervals(d,'mover')
    waiting_decisions=[a for a in d.controller if wait and a['stage']['index']==0]
    proceeding_decisions=[a for a in d.controller if not wait or a['stage']['index']==1]
    wait_native=[n for n in d.native if wait and n['time']<=wait+TOL]
    zero_seconds=math.fsum(n['elapsed'] for n in wait_native if max(abs(x) for x in n['commands'])<=1e-12)
    wait_cost=0.;move_cost=0.;splits=[]
    for i,e in enumerate(d.events):
        if e['duration']<=0:continue
        a=e['time']-e['duration'];b=e['time']
        if not wait or a>=wait-TOL:f=0.
        elif b<=wait+TOL:f=1.
        else:
            f=(wait-a)/(b-a);splits.append({'event_index':i,'original_start':a,'original_end':b,'split_at':wait,'waiting_fraction':f,'allocation':'Expenditure only, proportional to event duration under its constant held-command rate; no E/I interpolation'})
        wait_cost+=f*e['expenditure'];move_cost+=(1-f)*e['expenditure']
    first_motion=first(lambda p:p['position'][1]>start['position'][1]+.01)
    x=start['position'][0];max_lateral=max(abs(p['position'][0]-x) for p in poses)
    corridor=.25 if cid=='A4-DETOUR' else .5
    lateral_violations=[p['native_index'] for p in poses if abs(p['position'][0]-x)>corridor]
    detour_corridor_violations=[p['native_index'] for p in poses if abs(p['position'][0]-1.5)>.25 or not 6<=p['position'][1]<=14] if cid=='A4-DETOUR' else []
    cost=math.fsum(e['expenditure'] for e in d.events);damage=math.fsum(e['damage'] for e in d.events);repair=math.fsum(e['repair'] for e in d.events)
    intake=math.fsum(math.fsum(e['transfer']) for e in d.events)
    actual_wait=bool(wait and release_index is not None and waiting_decisions and zero_seconds>=wait-TOL and max((math.dist(p['position'],start['position']) for p in poses if p['time']<=wait+TOL),default=0)<=1e-10)
    crossing=entry is not None and exit_ is not None and not lateral_violations
    bypass=cid=='A4-DETOUR' and arrival is not None and crossing and not detour_corridor_violations
    witnessed=bypass if cid=='A4-DETOUR' else crossing and arrival is not None and (actual_wait if wait else True)
    physical_terminal=d.final['status']=='terminal';control_limits=[]
    if arrival is None:control_limits.append('Destination radius not reached within recorded coverage; no physical-impossibility inference')
    if entry is None or exit_ is None:control_limits.append('Complete band traversal not recorded')
    if lateral_violations:control_limits.append('Observed lateral route deviation beyond predeclared reporting corridor')
    if wait and not actual_wait:control_limits.append('Prescribed stationary wait not fully evidenced')
    if detour_corridor_violations:control_limits.append('Actual route left declared detour corridor')
    whole={'simulated_seconds':end,'native_steps':len(d.native),'start_EI':[start['energy'],start['integrity']],'final_EI':[d.final['body']['energy'],d.final['body']['integrity']],
      'expenditure':cost,'source_transfer':intake,'source_transfers':[math.fsum(e['transfer'][j] for e in d.events) for j in range(8)],'damage':damage,'repair':repair,'impact_damage':math.fsum(e['damage'] for e in d.events if e['impact']),'sustained_stress_damage':math.fsum(e['damage'] for e in d.events if not e['impact']),
      'sampled_path_length_through_final':length[-1],'sampled_path_length_through_arrival':None if arrival is None else length[arrival],'nominal_route_length':math.dist(start['position'],goal),
      'travel_time_to_arrival':None if arrival is None else poses[arrival]['time'],'travel_time_after_prescribed_release':None if arrival is None else poses[arrival]['time']-wait,
      'final_position':d.final['body']['position'],'final_angle':d.final['body']['angle'],'destination':goal,'final_destination_distance':math.dist(d.final['body']['position'],goal),'max_lateral_deviation':max_lateral,
      'sampled_stationary_seconds_endpoint_speed_le_1e_6':math.fsum(n['elapsed'] for n in d.native if math.hypot(*n['velocity'])<=1e-6)}
    obs={'case_id':cid,'parent_matrix_row':'A4','mode':'privileged external physical witness; P inactive','whole_case':whole,
      'milestones':{'approach':mark(approach),'entry_y_ge_9':mark(entry),'centre_y_ge_10':mark(centre),'exit_y_gt_11':mark(exit_),'arrival_radius_0_25':mark(arrival),'release_clock_boundary':mark(release_index) if wait else {'applicable':False},'first_northward_displacement_gt_0_01':mark(first_motion)},
      'waiting':{'prescribed_seconds':wait,'actual_clock_boundary_reached':bool(release_index is not None),'stationary_wait_observed':actual_wait if wait else None,'last_wait_decision':waiting_decisions[-1] if waiting_decisions else None,'first_proceed_decision':proceeding_decisions[0] if proceeding_decisions else None,'waiting_decisions':len(waiting_decisions),'zero_command_supported_seconds':zero_seconds,'max_wait_position_displacement':max((math.dist(p['position'],start['position']) for p in poses if wait and p['time']<=wait+TOL),default=0.),'waiting_expenditure':wait_cost,'post_wait_or_moving_expenditure':move_cost,'boundary_cost_allocations':splits,'waiting_command_records':[{'time':a['time'],'native_index':a['native_index'],'command':a['command']} for a in waiting_decisions]},
      'clearance':{'native_derived_minimum_whole':min_sample(samples),'native_derived_minimum_wait':min_sample(waiting_samples),'native_derived_minimum_crossing_band':min_sample(crossing_samples),'controller_actual_sample_minimum':min_sample(controller_samples),'continuous_time_minimum_certified':False,'scope':'Native samples plus analytic mover pose at original times; controller samples preserve actual sampled geometry. Contacts are established only from original events.'},
      'contacts':{'certified_contact_event_count':len(contact_events),'counts_by_collider':dict(labels),'mover_contact_event_count':len(mover_events),'mover_impact_event_count':len(mover_impacts),'mover_positive_contact_duration':math.fsum(s['duration'] for s in mover_spans),'mover_contact_intervals':mover_spans,'mover_impact_impulse_sum':math.fsum(ct['impulse'] for row in mover_impacts for ct in row['contacts'] if ct['collider']=='mover'),'mover_sustained_impulse_sum':math.fsum(ct['impulse'] for row in mover_events if row['duration']>0 for ct in row['contacts'] if ct['collider']=='mover'),'all_impact_event_count':len(impacts),'all_sustained_contact_event_count':len(sustained),'damage_at_mover_contact_events':math.fsum(row['damage'] for row in mover_events),'damage_attribution_note':'Original full-event damage; if multiple colliders share an event it is not solely mover-attributed.'},
      'route':{'lateral_corridor_half_width':corridor,'lateral_violating_native_indices':lateral_violations,'detour_corridor_violating_native_indices':detour_corridor_violations,'reentries_after_full_exit':reentries,'destination_departures_after_arrival':departures,'detour_nominal_static_certificate':'Unchanged A0 corridor, 8 m centre path; 3 m mover-union clearance' if cid=='A4-DETOUR' else None},
      'outcome':{'prescribed_physical_witness_observed':witnessed,'full_band_traversal_in_lateral_corridor':crossing,'destination_arrival':arrival is not None,'declared_detour_corridor_traversal':bypass if cid=='A4-DETOUR' else None,'controller_limitations_observed':control_limits,'physical_nonviability':physical_terminal,'terminal_dimension':d.final['terminal_dimension'],'administrative_cutoff':d.receipt['status']=='administrative_cutoff','administrative_resource_or_operator_pause':d.receipt['status']=='administrative_pause','stop_status':d.receipt['status'],'stop_cause':d.receipt.get('stop_cause'),'complete':d.receipt['complete'],'no_physical_impossibility_inference':True},
      'fixed_window_summary':{'complete_0_2_windows':sum(w['complete_0_2_second_interval'] for w in windows),'partial_windows':sum(not w['complete_0_2_second_interval'] for w in windows),'net_E_sign_counts':dict(collections.Counter(w['net_energy_sign'] for w in windows))},
      'interpretation_limits':['No all-phase or all-reserve claim.','No P perception, learning, prediction, regulation or efficacy claim.','Immediate-proceed WAIT conflict remains the approved analytic counterfactual; no counterfactual trajectory was run.','No optimality or equal-endpoint comparison between detour and crossing.','Sampled clearance/path length are not continuous-time extrema/arclength.']}
    evidence={'native_mover_clearance_samples':samples,'actual_controller_mover_samples':controller_samples,'contact_events':contact_events,'explicit_contact_boundaries':boundaries}
    return obs,evidence
