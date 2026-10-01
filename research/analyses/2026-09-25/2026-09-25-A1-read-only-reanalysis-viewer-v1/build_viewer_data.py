"""Passive extraction and ledger arithmetic; no world/geometry/control evolution."""
import bisect,math
from evidence import *
e=Evidence();v3=json.loads((ROOT/'V3_RESULT_v1_1.json').read_bytes())
assert v3['status'].startswith('V3 COMPLETED —')
n=e.stream('native');events=e.stream('events');actions=e.stream('controller');sensors=e.stream('sensor')
initial=snapshot_data(e.snapshot('initial'))['engine'];body=initial['body'];c=initial['c']
obs=e.json('evidence/read-only-review/A1_OBSERVATIONS.json');summary=e.json('evidence/read-only-review/A1_RESULT_SUMMARY.json')
frames=[{'time':0,'index':0,'position':body['position'],'angle':body['angle'],'velocity':body['velocity'],'omega':body['omega'],
    'E':body['energy'],'I':body['integrity'],'stock':initial['stocks'][0],'commands':body['command'],'forces':body['force'],
    'raw':sensors[0]['history'][0]['raw'],'heldEI':[body['energy'],body['integrity']],'eiTime':0,
    'eventStart':0,'eventEnd':0,'transfer':0,'expense':0,'deltaE':0,'cumTransfer':0,'cumExpense':0,'force':None,'contact':False,
    'damage':0,'repair':0,'debit':0,'credit':0,'renewal':0,'residual':0,'mover':0,'issued':None}]
compact_events=[];force_events=[];markers=[];impact_damage=0.;stress_damage=0.;event_offset=0;cumT=0.;cumC=0.
for j,x in enumerate(events):
    force=sum(y.get('force',0) for y in x['contacts']) if x['duration']>0 and x['contacts'] else None
    source=any(y.get('source')==0 and y.get('collider')=='source-0' for y in x['contacts'])
    debit=x['stock_before'][0]+x['renewal_first'][0]+x['renewal_second'][0]-x['stock_after'][0]
    credit=x['energy_after']-x['energy_before']+x['expenditure']
    compact_events.append({'id':j,'time':x['time'],'duration':x['duration'],'kind':x.get('event_kind','support' if x['contacts'] else 'free'),
        'impact':x['impact'],'contacts':x['contacts'],'contact':source,'position':x['body_position'],'angle':x['body_angle'],
        'Ebefore':x['energy_before'],'E':x['energy_after'],'Ibefore':x['integrity_before'],'I':x['integrity_after'],
        'stock':x['stock_after'][0],'transfer':sum(x['transfer']),'sourceTransfer':x['transfer'][0],
        'expense':x['expenditure'],'debit':debit,'credit':credit,'renewal':x['renewal_first'][0]+x['renewal_second'][0],
        'residual':credit-sum(x['transfer']),'damage':x['damage'],'repair':x['repair'],'force':force})
    if force is not None:force_events.append([x['time'],force,j])
    if x['impact']:impact_damage+=x['damage']
    else:stress_damage+=x['damage']
    if x['impact'] or x['damage']>0 or x['repair']>0 or x.get('event_kind'):
        markers.append({'event':j,'time':x['time'],'label':'impact' if x['impact'] else 'integrity debit' if x['damage']>0 else x.get('event_kind','restoration')})
times=[a['time'] for a in actions]
movers=[{'time':a['time'],'native_index':a['native_index'],**next(f for f in a['inputs']['geometry'] if f['id']=='mover')} for a in actions]
for row,sensor in zip(n,sensors[1:]):
    start=event_offset
    while event_offset<len(events) and events[event_offset]['time']<=row['time']+c['event_time_tol']:event_offset+=1
    group=compact_events[start:event_offset];t=math.fsum(x['transfer'] for x in group);cost=math.fsum(x['expense'] for x in group)
    cumT+=t;cumC+=cost
    last=group[-1] if group else None
    native=row['native_index'];owner=(native-1)//10
    frames.append({'time':row['time'],'index':native,'position':row['position'],'angle':row['angle'],'velocity':row['velocity'],'omega':row['omega'],
        'E':row['reserves'][0],'I':row['reserves'][1],'stock':row['stocks'][0],'commands':row['commands'],'forces':row['forces'],
        'raw':sensor['raw'],'heldEI':sensor['actual_EI'],'eiTime':sensor['EI_sample_time'],
        'eventStart':start,'eventEnd':event_offset,'transfer':t,'expense':cost,'deltaE':row['reserves'][0]-frames[-1]['E'],
        'cumTransfer':cumT,'cumExpense':cumC,'force':None if last is None else last['force'],'contact':False if last is None else last['contact'],
        'damage':math.fsum(x['damage'] for x in group),'repair':math.fsum(x['repair'] for x in group),
        'debit':math.fsum(x['debit'] for x in group),'credit':math.fsum(x['credit'] for x in group),
        'renewal':math.fsum(x['renewal'] for x in group),'residual':math.fsum(x['residual'] for x in group),
        'mover':bisect.bisect_right(times,row['time'])-1,'issued':owner})
    assert abs(frames[-1]['deltaE']-(t-cost))<1e-12
assert event_offset==len(events)
first=next(x for x in compact_events if x['contact']);peak=max(force_events,key=lambda x:x[1])
data={'schema':1,'title':'Loom · first A1 / recorded evidence','provenance':{'P':'6bc9683b54e4fa80136fe8534d7713e2a250a95f','apparatus':'5f07748102cb5eaa302569c87efbae095050e9fe','authority':'a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc','evidence_sha256':e.zip_sha256,'V3':v3['status']},
    'world':{'side':c['world_side'],'bodyRadius':c['body_radius'],'sources':c['source_positions'],'sourceRadius':c['source_radius'],'repairs':c['repair_rectangles']},
    'frames':frames,'events':compact_events,'movers':movers,'actions':[{'time':a['time'],'index':a['native_index'],'command':a['command']} for a in actions],
    'labels':sensors[0]['raw_labels'],'windows':obs['all_fixed_windows'],'forceEvents':force_events,'markers':markers,
    'firstContact':first['id'],'firstPositive':summary['first_positive_net_contact_window'],'peakForce':peak,
    'targetForce':.1,'stressThreshold':c['stress_threshold'],'impactDamage':impact_damage,'sustainedDamage':stress_damage,
    'summary':{k:v for k,v in summary.items() if k not in ('analysis_errors','V3')},
    'limitations':['Recorded states only; no interpolation or simulation. Path/trace lines connect recorded points for display.',
        'Mover rectangles are the latest recorded controller-input geometry (0.1 s cadence); their own timestamp and age are shown. No mover-law evaluation.',
        'Exact event selection uses recorded event pose, E/I and stock. Velocity, raw sensors, command and realized actuators remain explicitly labelled at their own latest native sample.',
        'The last partial fixed window ends at an administrative pause, not a bodily terminal event. Negative-net windows are observations, not failures.']}
(ROOT/'viewer_data.js').write_text('"use strict";\nconst A1_DATA = '+json.dumps(data,separators=(',',':'),allow_nan=False)+';\n',encoding='utf-8')
write(ROOT/'VIEWER_EXTRACTION.json',{'input_sha256':e.zip_sha256,'frames':len(frames),'events':len(events),'mover_samples':len(movers),
    'exact_first_contact_event':first,'peak_force':[peak[0],peak[1],peak[2]],'impact_damage_sum':impact_damage,'sustained_damage_sum':stress_damage,
    'ledger_partition_all_events':True,'simulation_steps':0,'mover_law_evaluations':0,'interpolated_physical_samples':0,
    'builder_sha256':filehash(__file__),'viewer_data_sha256':filehash(ROOT/'viewer_data.js')})
print(json.dumps({'frames':len(frames),'events':len(events),'first_contact':first['time'],'peak_force':peak,'viewer_bytes':(ROOT/'viewer_data.js').stat().st_size}))
