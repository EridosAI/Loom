"""A3 saved-record observations. Standard library; no live controller/world calls."""
from a3_analysis_core import *

def touch(e,label):return any(c['collider']==label for c in e['contacts'])
def sign(value,allowance):return 'zero' if value==0 else 'positive_resolved' if value>allowance else 'negative_resolved' if value < -allowance else 'unresolved_at_accounting_resolution'
def allowance(ledger,i,field='integrity_residual'):
    return abs(ledger['rows'][i][field])+2e-12
def contact_intervals(d,label):
    out=[]
    for i,e in enumerate(d.events):
        if e['duration']<=0 or not touch(e,label):continue
        a=e['time']-e['duration'];b=e['time']
        if out and abs(out[-1]['end']-a)<=TOL:
            out[-1]['end']=b;out[-1]['last_event']=i;out[-1]['duration']+=e['duration']
        else:out.append({'start':a,'end':b,'duration':e['duration'],'first_event':i,'last_event':i})
    return out
def fixed_windows(d,ledger):
    out=[];events=d.events;labels=['repair-0']+[f'source-{i}' for i in range(8)]
    intervals={label:contact_intervals(d,label) for label in labels}
    for start in range(0,len(d.native),20):
        block=d.native[start:start+20];old=d.sample(start-1);new=d.sample(start+len(block)-1);a=old['time'];b=new['time']
        ix=list(range(bisect.bisect_right(d.event_times,a+TOL),bisect.bisect_right(d.event_times,b+TOL)))
        inc=[i for i in ix if events[i]['duration']>0]
        straddles=[i for i in inc if events[i]['time']-events[i]['duration']<a-TOL]
        k=bisect.bisect_right(d.event_times,b+TOL)
        if k<len(events) and events[k]['duration']>0 and events[k]['time']-events[k]['duration']<b-TOL:straddles.append(k)
        er=math.fsum(abs(ledger['rows'][i]['energy_residual']) for i in ix);ir=math.fsum(abs(ledger['rows'][i]['integrity_residual']) for i in ix)
        ea=er+(len(ix)+1)*1e-12;ia=ir+(len(ix)+1)*1e-12
        de=new['reserves'][0]-old['reserves'][0];di=new['reserves'][1]-old['reserves'][1]
        support={}
        for label in labels:
            seconds=math.fsum(max(0,min(b,c['end'])-max(a,c['start'])) for c in intervals[label])
            support[label]={'seconds':seconds,'contact_containing':any(touch(events[i],label) for i in inc),'fully_supported':abs(seconds-(b-a))<=TOL}
        out.append({'first_native':block[0]['native_index'],'last_native':block[-1]['native_index'],'start_time':a,'end_time':b,
          'complete_0_2_second_interval':len(block)==20 and abs(b-a-.2)<=TOL,'EI_before':old['reserves'],'EI_after':new['reserves'],
          'energy_delta':de,'net_energy_sign':sign(de,ea),'integrity_delta':di,'net_integrity_sign':sign(di,ia),
          'energy_allowance':ea,'integrity_allowance':ia,'source_transfers':[math.fsum(events[i]['transfer'][j] for i in inc) for j in range(8)],
          'all_source_intake':math.fsum(math.fsum(events[i]['transfer']) for i in inc),'expenditure':math.fsum(events[i]['expenditure'] for i in inc),
          'repair':math.fsum(events[i]['repair'] for i in ix),'damage':math.fsum(events[i]['damage'] for i in ix),
          'positions':[old['position'],new['position']],'stocks':[old['stocks'],new['stocks']],
          'contact_support':support,'boundary_straddling_events':straddles})
    return out
def rect_gap(p,rect,r=.5):
    x,y=p;x0,x1,y0,y1=rect;dx=max(x0-x,x-x1,0);dy=max(y0-y,y-y1,0)
    return math.hypot(dx,dy)-r if dx or dy else -min(x-x0,x1-x,y-y0,y1-y)-r
def pose_history(d):
    out=[{'time':0.,'position':d.initial['body']['position'],'angle':d.initial['body']['angle'],'kind':'initial'}]
    out += [{'time':n['time'],'position':n['position'],'angle':n['angle'],'native_index':n['native_index'],'kind':'native'} for n in d.native]
    out += [{'time':e['time'],'position':e['body_position'],'angle':e['body_angle'],'event_index':i,'kind':'event'} for i,e in enumerate(d.events)]
    return sorted(out,key=lambda x:x['time'])
def contact_summary(d,label,gap,poses):
    ev=[(i,e) for i,e in enumerate(d.events) if touch(e,label)]
    cts=[c for _,e in ev if e['duration']>0 for c in e['contacts'] if c['collider']==label]
    impacts=[compact_event(i,e) for i,e in ev if e['impact']]
    spans=contact_intervals(d,label)
    def ran(k):
        vals=[c[k] for c in cts if k in c];return [min(vals),max(vals)] if vals else None
    arr=next((dict(v,surface_gap=gap(v['position'])) for v in poses if -1e-8<=gap(v['position'])<=2e-10),None)
    releases=[compact_event(i,e) for i,e in enumerate(d.events) if e.get('event_kind')=='release' and label in e.get('colliders',[])]
    return {'first_certified_contact':compact_event(*ev[0]) if ev else None,'geometric_arrival':arr,
      'minimum_recorded_gap':min(gap(p['position']) for p in poses),'certified_contact_events':len(ev),'positive_duration_contact_seconds':math.fsum(x['duration'] for x in spans),
      'contact_intervals':spans,'gaps_between_contact_intervals':[{'from':a['end'],'to':b['start'],'duration':b['start']-a['end']} for a,b in zip(spans,spans[1:])],
      'sustained_force_range':ran('force'),'relative_speed_range':ran('relative_speed'),'impacts':impacts,'release_events':releases,
      'force_at_or_above_stress_event_count':sum(c.get('force',0)>=.25 for c in cts)}
def departure(d,label,switch,gap):
    if switch is None:return {'observed':False,'reason':'Departure stage not reached','time':None}
    prior=[(i,e) for i,e in enumerate(d.events) if touch(e,label) and e['time']<=switch+TOL]
    if not prior:return {'observed':False,'reason':'No earlier certified contact with designated fixture','time':None}
    rel=next(((i,e) for i,e in enumerate(d.events) if e['time']>=switch-TOL and e.get('event_kind')=='release' and label in e.get('colliders',[])),None)
    supported_times=[e['time'] for e in d.events if e['duration']>0 and touch(e,label)]
    def supported(t):
        j=bisect.bisect_left(supported_times,t-TOL);return j<len(supported_times) and abs(supported_times[j]-t)<=TOL
    clear=next((n for n in d.native if n['time']>=switch-TOL and gap(n['position'])>TOL and not supported(n['time'])),None)
    substantial=next((n for n in d.native if n['time']>=switch-TOL and gap(n['position'])>=1),None)
    when=rel[1]['time'] if rel else clear['time'] if clear else None
    return {'observed':when is not None,'reason':None if when is not None else 'No release or clear native endpoint before stop','time':when,
       'release_event':compact_event(*rel) if rel else None,'first_clear_native':clear,'first_body_diameter_clearance_native':substantial,
       'event_time_precision':'recorded release event' if rel else 'first clear native endpoint; separation bracketed' if clear else None,
       'EI_bracket':d.bracket(when) if when is not None else None,
       'maximum_gap_after_instruction':max((gap(n['position']) for n in d.native if n['time']>=switch-TOL),default=None),
       'recontacts_after_departure':[compact_event(i,e) for i,e in enumerate(d.events) if when is not None and e['time']>when+TOL and touch(e,label)]}
def event_milestone(pair,reason=None):
    if pair is None:return {'observed':False,'time':None,'EI_before':None,'EI_after':None,'reason':reason or 'Not observed within recorded coverage'}
    i,e=pair
    return {'observed':True,'event_index':i,'time':e['time'],'EI_before':[e['energy_before'],e['integrity_before']],
      'EI_after':[e['energy_after'],e['integrity_after']],'position':e['body_position'],'angle':e['body_angle'],
      'stock_before':e['stock_before'],'stock_after':e['stock_after'],'damage':e['damage'],'repair':e['repair'],
      'repair_quality':e.get('repair_quality'),'contacts':e['contacts'],'time_meaning':'Recorded event endpoint; before/after ledger sides retained'}

def physical_observations(d,ledger,ws):
    ev=d.events;end=d.final['time'];poses=pose_history(d)
    wallgap=lambda p:p[0]-.5
    repairgap=lambda p:rect_gap(p,d.initial['c']['repair_rectangles'][0])
    sourcegap=lambda p:math.dist(p,d.initial['c']['source_positions'][3])-1.
    wall=contact_summary(d,'wall-0',wallgap,poses)
    repair=contact_summary(d,'repair-0',repairgap,poses)
    energy=contact_summary(d,'source-3',sourcegap,poses)
    damage=next(((i,e) for i,e in enumerate(ev) if e['damage']>allowance(ledger,i)),None)
    damagewall=next(((i,e) for i,e in enumerate(ev) if touch(e,'wall-0') and e['damage']>allowance(ledger,i)),None)
    eligibility=next(((i,e) for i,e in enumerate(ev) if touch(e,'repair-0') and e['duration']>0 and e.get('repair_quality',0)>1e-12),None)
    restored=next(((i,e) for i,e in enumerate(ev) if touch(e,'repair-0') and e['repair']>allowance(ledger,i) and damage is not None and i>damage[0]),None)
    repairarrival=next(((i,e) for i,e in enumerate(ev) if touch(e,'repair-0')),None)
    switches={j:next((a for a in d.controller if a['stage']['index']==j),None) for j in range(6)}
    wd=departure(d,'wall-0',switches[1]['time'] if switches[1] else None,wallgap)
    rd=departure(d,'repair-0',switches[4]['time'] if switches[4] else None,repairgap)
    energyany=next(((i,e) for i,e in enumerate(ev) if touch(e,'source-3')),None)
    energyafter=next(((i,e) for i,e in enumerate(ev) if rd['time'] is not None and e['time']>=rd['time']-TOL and touch(e,'source-3')),None)
    def xallow(i):return abs(ledger['rows'][i]['energy_residual'])+abs(ledger['rows'][i]['stock_residuals'][3])+2e-12
    transferany=next(((i,e) for i,e in enumerate(ev) if e['transfer'][3]>xallow(i)),None)
    transferafter=next(((i,e) for i,e in enumerate(ev) if rd['time'] is not None and e['time']>=rd['time']-TOL and e['transfer'][3]>xallow(i)),None)
    ir=math.fsum(abs(x['integrity_residual']) for x in ledger['rows']);er=math.fsum(abs(x['energy_residual']) for x in ledger['rows'])
    ia=ir+(len(ev)+1)*1e-12;ea=er+(len(ev)+1)*1e-12
    repair_total=math.fsum(e['repair'] for e in ev);damage_total=math.fsum(e['damage'] for e in ev);transfer_total=math.fsum(e['transfer'][3] for e in ev)
    quality_rows=[];quality_residual_max=0.;repair_residual_max=0.
    for i,e in enumerate(ev):
        if e['duration']<=0:continue
        terms=[c['force']/(c['force']+.1)/(1+(c['relative_speed']/.25)**2)*max(1-c['force']/.25,0) for c in e['contacts'] if c['material']==3]
        q=max(terms,default=0.);quality_residual_max=max(quality_residual_max,abs(q-e.get('repair_quality',0)))
        current=e['integrity_before']-e['damage']
        expected=(1-current)*(-math.expm1(-.02*q*e['duration'])) if current>0 else 0.
        repair_residual_max=max(repair_residual_max,abs(expected-e['repair']))
        if touch(e,'repair-0'):
            quality_rows.append({'event_index':i,'time':e['time'],'duration':e['duration'],'force_and_speed':[{'force':c.get('force'),'relative_speed':c['relative_speed'],'impulse':c['impulse']} for c in e['contacts'] if c['collider']=='repair-0'],
              'repair_quality':e.get('repair_quality',0),'quality_from_saved_operands':q,'damage':e['damage'],'repair':e['repair'],'repair_sign':sign(e['repair'],allowance(ledger,i)),
              'EI_before':[e['energy_before'],e['integrity_before']],'EI_after':[e['energy_after'],e['integrity_after']],
              'expenditure':e['expenditure'],'all_source_transfer':math.fsum(e['transfer'])})
    # No scientific or outcome-tuned threshold: report the recorded quality and its rounding allowance.
    repair['eligibility_quality_resolution_allowance']=1e-12
    repair['quality_range']=[min(x['repair_quality'] for x in quality_rows),max(x['repair_quality'] for x in quality_rows)] if quality_rows else None
    repair['eligible_duration']=math.fsum(x['duration'] for x in quality_rows if x['repair_quality']>1e-12)
    repair['positive_restoration_duration']=math.fsum(x['duration'] for x in quality_rows if x['repair_sign']=='positive_resolved')
    repair['quality_saved_operand_max_residual']=quality_residual_max;repair['repair_saved_operand_max_residual']=repair_residual_max
    contactend=rd['time'] if rd['time'] is not None else end
    repair_interval=d.interval(repairarrival[1]['time'],contactend) if repairarrival and contactend>=repairarrival[1]['time'] else None
    travel=d.interval(rd['time'],energyafter[1]['time'] if energyafter else end) if rd['time'] is not None else None
    damagedtravel=d.interval(wd['time'],repairarrival[1]['time'] if repairarrival else end) if wd['time'] is not None else None
    supported=[x for x in quality_rows if repairarrival and x['time']<=contactend+TOL]
    positivews=[w for w in ws if w['complete_0_2_second_interval'] and w['contact_support']['source-3']['contact_containing'] and w['net_energy_sign']=='positive_resolved']
    energy['first_positive_transfer_any']=event_milestone(transferany)
    energy['first_positive_transfer_after_repair_departure']=event_milestone(transferafter)
    energy['source3_transfer_total']=transfer_total;energy['source3_transfer_sign']=sign(transfer_total,ea+math.fsum(abs(x['stock_residuals'][3]) for x in ledger['rows']))
    energy['first_positive_net_window']=positivews[0] if positivews else None
    energy['positive_net_contact_window_count']=len(positivews)
    energy['negative_net_contact_window_count']=sum(w['complete_0_2_second_interval'] and w['contact_support']['source-3']['contact_containing'] and w['net_energy_sign']=='negative_resolved' for w in ws)
    milestones={'initial_healthy':{'observed':True,'time':0.,'EI':[.7,1.],'position':d.initial['body']['position'],'angle':d.initial['body']['angle']},
      'pre_damage':event_milestone(damage),'post_damage':event_milestone(damage),'repair_arrival':event_milestone(repairarrival),
      'first_eligible_repair':event_milestone(eligibility),'first_positive_restoration':event_milestone(restored),
      'repair_departure':{'observed':rd['observed'],'time':rd['time'],'release_event':rd.get('release_event'),'sample_bracket':rd.get('EI_bracket'),'reason':rd.get('reason')},
      'energy_arrival_after_repair_departure':event_milestone(energyafter),'energy_arrival_any':event_milestone(energyany),
      'final_stop':{'observed':True,'time':end,'EI':[d.final['body']['energy'],d.final['body']['integrity']],'position':d.final['body']['position'],'angle':d.final['body']['angle']}}
    milestones['pre_damage']['selected_side']='EI_before';milestones['post_damage']['selected_side']='EI_after'
    stage_totals=[];start=0.
    for j,p in enumerate(d.manifest['execution']['procedure']['stages']):
        if end>=start-TOL:stage_totals.append(dict(stage_index=j,nominal_until=p['until'],**d.interval(start,min(end,p['until']))))
        start=p['until']
    stagerows=[]
    for j in range(6):
        acts=[a for a in d.controller if a['stage']['index']==j]
        if acts:
            target=d.manifest['execution']['procedure']['stages'][j]['point']
            stagerows.append({'stage_index':j,'first_decision':acts[0],'last_decision':acts[-1],
              'decision_count':len(acts),'max_absolute_command':max(abs(v) for a in acts for v in a['command']),
              'minimum_sampled_target_centre_distance':min(math.dist(a['inputs']['position'],target) for a in acts),
              'last_sampled_target_centre_distance':math.dist(acts[-1]['inputs']['position'],target)})
    mover=[]
    for a in d.controller:
        f=next(f for f in a['inputs']['geometry'] if f['id']=='mover')
        mover.append({'time':a['time'],'gap':rect_gap(a['inputs']['position'],f['rect']),
          'position':a['inputs']['position'],'mover_rectangle':f['rect'],'velocity':f['velocity']})
    chain=bool(damage and damage[1]['integrity_after']>0 and repairarrival and eligibility and restored and eligibility[1]['time']<=restored[1]['time']+TOL and rd['time'] is not None and restored[1]['time']<rd['time']+TOL and energyafter and transferafter and transferafter[1]['energy_after']>0 and transferafter[1]['integrity_after']>0)
    end_delta=max(0.,d.manifest['hard_stop_time']-end)
    whole={'time':end,'native_index':d.final['native_index'],'initial_EI':[.7,1.],'final_EI':[d.final['body']['energy'],d.final['body']['integrity']],
      'all_source_intake':math.fsum(math.fsum(e['transfer']) for e in ev),'source_intake_totals':[math.fsum(e['transfer'][j] for e in ev) for j in range(8)],
      'expenditure':math.fsum(e['expenditure'] for e in ev),'net_E':d.final['body']['energy']-.7,'damage':damage_total,'repair':repair_total,
      'net_I':d.final['body']['integrity']-1.,'repair_sign':sign(repair_total,ia),'damage_sign':sign(damage_total,ia),
      'energy_allowance':ea,'integrity_allowance':ia,'final_stocks':d.final['stocks'],'terminal_dimension':d.final['terminal_dimension'],
      'stop_label':d.receipt['status'],'stop_cause':d.receipt.get('stop_cause'),'complete':d.receipt['complete'],'failure':d.result['failure'],'receipt_error':d.receipt.get('error'),
      'planned_minus_actual_raw_seconds':end_delta,'unobserved_seconds_beyond_event_tolerance':end_delta if end_delta>TOL else 0.,
      'complete_ordered_recovery_witness_observed':chain}
    return {'analysis_version':'A3 read-only v1.0','milestones':milestones,'whole_case':whole,'wall':wall,'repair':repair,'energy':energy,
      'first_intended_wall_damage':event_milestone(damagewall),'all_positive_damage_events':[compact_event(i,e) for i,e in enumerate(ev) if e['damage']>allowance(ledger,i)],
      'wall_departure':wd,'repair_departure':rd,'damaged_travel':damagedtravel,'repair_arrival_to_departure_or_stop':repair_interval,
      'repair_supported_expenditure':math.fsum(x['expenditure'] for x in supported),'repair_supported_intake':math.fsum(x['all_source_transfer'] for x in supported),
      'repair_to_energy_travel':travel,'stage_totals':stage_totals,'stage_decision_summaries':stagerows,
      'mover':{'certified_contacts':[compact_event(i,e) for i,e in enumerate(ev) if touch(e,'mover')],'nearest_recorded_decision':min(mover,key=lambda x:x['gap']) if mover else None,'sample_cadence':.1,
        'ray_hit_identity':'Unavailable in original external-arm record; no new ray tracing or perception claim.'},
      'complete_fixed_windows':sum(w['complete_0_2_second_interval'] for w in ws),'partial_fixed_windows':sum(not w['complete_0_2_second_interval'] for w in ws),
      'controller_failure_interpretation':'Explicit exceptions separately retained. Route misses, force overshoot or absent witness alone do not establish physical infeasibility or P failure.',
      'physical_infeasibility_claim':'No universal recovery/impossibility claim from this single prescribed case.',
      'scope':'Parallel observed commissioning facts; no P learning or efficacy gate.'},quality_rows
