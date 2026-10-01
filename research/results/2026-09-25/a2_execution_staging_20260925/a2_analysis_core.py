"""A2 read-only analysis v1.0. Standard library and preserved record checker only."""
import base64,bisect,collections,gzip,hashlib,json,math,pathlib,sys
ROOT=pathlib.Path(__file__).resolve().parent.parent
PACKET=ROOT/'exports/2026-09-25-A2-launch-packet-5f077481'
sys.path.insert(0,str(PACKET/'references'))
from evidence import plain,packed_attr,canonical,digest,snapshot_data
from v3_checker_v1_1 import align,validate_inputs
AUTH='229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007'
TOL=1e-10
def shafile(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def sorted_bytes(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def js(p):return json.loads(pathlib.Path(p).read_bytes())
def stream(p):
    with gzip.open(p,'rt',encoding='utf-8') as f:return [json.loads(line) for line in f]
def snapshot(p):return json.loads(gzip.decompress(pathlib.Path(p).read_bytes()))
def source_contact(event,index):return any(c.get('source')==index and c.get('collider')==f'source-{index}' for c in event['contacts'])
def compact_event(i,e):
    return {'event_index':i,'time':e['time'],'duration':e['duration'],'event_kind':e.get('event_kind'),
       'impact':e['impact'],'position':e['body_position'],'angle':e['body_angle'],'energy_before':e['energy_before'],'energy_after':e['energy_after'],
       'integrity_before':e['integrity_before'],'integrity_after':e['integrity_after'],'stock_before':e['stock_before'],'stock_after':e['stock_after'],
       'transfer':e['transfer'],'expenditure':e['expenditure'],'renewal_first':e['renewal_first'],'renewal_second':e['renewal_second'],
       'contacts':e['contacts'],'colliders':e.get('colliders')}
class Data:
    def __init__(self,base):
        self.base=pathlib.Path(base);self.t=self.base/'trajectory-001'
        self.receipt=js(self.t/'manifest.json');self.result=js(self.base/'EXECUTION_RESULT.json')
        self.manifest=js(self.base/'LAUNCHED_MANIFEST.json')
        self.initial_wrapper=snapshot(self.t/'initial.restart.json.gz');self.initial=snapshot_data(self.initial_wrapper)['engine']
        self.final_wrapper=snapshot(self.t/'final.restart.json.gz');self.finish=snapshot_data(self.final_wrapper);self.final=self.finish['engine'];self.session=self.finish['session']
        for name in ('native','events','controller','sensor','diagnostics','wave','scientific_observations'):setattr(self,name,stream(self.t/(name+'.jsonl.gz')))
        self.times=[n['time'] for n in self.native]
        self.event_times=[e['time'] for e in self.events]
        assert all(b>=a-TOL for a,b in zip(self.event_times,self.event_times[1:]))
    def sample(self,n):
        if n<0:return {'time':0.,'native_index':0,'position':self.initial['body']['position'],'reserves':[self.initial['body']['energy'],self.initial['body']['integrity']],'stocks':self.initial['stocks']}
        v=self.native[n];return {k:v[k] for k in ('time','native_index','position','reserves','stocks')}
    def bracket(self,t):
        i=bisect.bisect_left(self.times,t)
        return {'before_or_initial':self.sample(i-1),'at_or_after':self.sample(i) if i<len(self.native) else None}
    def interval(self,a,b):
        chosen=[(i,e) for i,e in enumerate(self.events) if e['duration']>0 and e['time']>a+TOL and e['time']<=b+TOL]
        straddles=[i for i,e in enumerate(self.events) if e['duration']>0 and ((e['time']-e['duration']<a-TOL<e['time']-TOL) or (e['time']-e['duration']<b-TOL<e['time']-TOL))]
        return {'start':a,'end':b,'duration':b-a,'whole_events_included':len(chosen),
           'source_transfers':[math.fsum(e['transfer'][j] for _,e in chosen) for j in range(8)],
           'gross_intake':math.fsum(math.fsum(e['transfer']) for _,e in chosen),'expenditure':math.fsum(e['expenditure'] for _,e in chosen),
           'boundary_straddling_events':straddles,'complete_event_boundary_coverage':not straddles}

def record_integrity(d):
    r=d.receipt;m=d.manifest
    failures=[]
    for n,v in r['files'].items():
        p=d.t/n
        assert p.stat().st_size==v['bytes'] and shafile(p)==v['sha256'],n
    assert {p.name for p in d.t.iterdir() if p.is_file()}==set(r['files'])|{'manifest.json'}
    for name in ('native','events','controller','sensor','diagnostics','wave','scientific_observations'):assert len(getattr(d,name))==r['records'].get(name,0),name
    obj={k:v for k,v in m.items() if k!='execution_authority'}
    assert digest(sorted_bytes(obj))==AUTH
    assert sorted_bytes(obj)==(d.base/'APPROVED_OBJECT.canonical.json').read_bytes()==(PACKET/'AUTHORITY_OBJECT.canonical.json').read_bytes()
    req=js(d.base/'APPROVAL_REQUEST.json');grant=m['execution_authority']
    assert req['approved_execution']==obj and req['approved_execution_sha256']==AUTH
    assert shafile(d.base/'APPROVAL_REQUEST.json')==grant['request_sha256'] and grant['approved_execution_sha256']==AUTH
    assert req['notice']==(d.base/'AUTHORIZATION_SOURCE.txt').read_text(encoding='utf-8').rstrip('\n')
    assert r['contract']==m==d.initial_wrapper['manifest']==d.final_wrapper['manifest']
    initial_packed=dict(d.initial_wrapper['state']['$dict'])['engine'];final_packed=dict(d.final_wrapper['state']['$dict'])['engine']
    assert digest(canonical(initial_packed))==m['initial_state']
    assert digest(canonical(final_packed))==r['final_state']==d.result['final_engine_sha256']
    assert d.result['run_constructors_attempted']==1 and d.result['no_retry_no_resume_no_patch']
    assert d.result['physical_replays']==0
    for i,n in enumerate(d.native,1):assert n['native_index']==i and n['field_phase']==m['phase']
    assert len(d.native)==d.final['native_index'] and abs(d.final['time']-r['final_time'])<=TOL
    assert d.final['time']<=m['hard_stop_time']+1e-9
    status=r['status']
    if status=='administrative_cutoff':assert abs(d.final['time']-180)<1e-9 and d.final['terminal_dimension'] is None
    elif status=='administrative_pause':assert d.final['time']<180-1e-9 and d.final['terminal_dimension'] is None
    elif status=='terminal':assert d.final['status']=='terminal' and min(d.final['body']['energy'],d.final['body']['integrity'])<=1e-9
    elif status=='apparatus_failure':assert not r['complete'] and r['error']
    else:raise AssertionError('Unknown stop')
    return {'valid':True,'complete':r['complete'],'status':status,'stop_cause':r.get('stop_cause'),'receipt_payloads':len(r['files']),
       'record_counts':r['records'],'authority_sha256':AUTH,'physical_replay':False,'controller_recomputation':False,
       'scope':'Saved receipt, checksum, exact grant/object, native sequence and stop checks. Production verify_segment not invoked because its pending-command validator recomputes waypoint commands even with replay=False.'}

def boundary_check(d):
    envelope,rows,mapping=align(d.native,d.sensor,d.diagnostics,d.initial)
    inputs=validate_inputs(d.controller,d.native,d.initial)
    display=js(d.t/'sensor-display.json')
    assert set(display)==set(envelope) and display['schema']==envelope['schema'] and display['raw_labels']==envelope['raw_labels']
    assert display['history']==envelope['history']+rows
    assert display['own_commands']==[{'time':a['time'],'command':a['command']} for a in d.controller]
    assert display['annotations']==[] and display['availability']=='paused' and display==d.session['sensor']['payload']
    org=packed_attr(dict(d.initial_wrapper['state']['$dict'])['engine'],'organism');org_hash=digest(canonical(org));rng=d.initial['organism']['rng']
    checks=[]
    for p in sorted(d.t.glob('*.restart.json.gz')):
        w=snapshot(p);value=snapshot_data(w);engine=dict(w['state']['$dict'])['engine']
        assert packed_attr(engine,'organism')==org and value['engine']['organism']['rng']==rng
        assert w['manifest']==d.manifest
        ni=value['engine']['native_index']
        expected_field=d.manifest['initial_fields'] if ni==0 else d.native[ni-1]['field_sha256']
        assert digest(base64.b64decode(packed_attr(engine,'fields')['$array']))==expected_field
        assert value['engine']['phase']==d.manifest['phase']
        checks.append({'file':p.name,'time':value['engine']['time'],'native_index':value['engine']['native_index']})
    assert all(n['random_counters']==rng['counters'] for n in d.native)
    assert not d.wave and not d.scientific_observations
    assert d.session['advanced']==d.session['field_updates']==len(d.native)
    assert d.session['body_wave_samples']==sum(n['native_index']%20==0 and n['status']!='terminal' for n in d.native)
    assert d.session['decision']==d.controller[-1] and d.session['hold_remaining']==inputs['last_hold_pending_steps']
    stages=d.manifest['execution']['procedure']['stages'];stage_counts=collections.Counter()
    for a in d.controller:
        j=0
        while j<len(stages)-1 and (a['time']>=stages[j]['until'] or math.isclose(a['time'],stages[j]['until'],rel_tol=0,abs_tol=TOL)):j+=1
        expected={'index':j,'identity':digest(sorted_bytes(stages[j])),'start_time':0. if j==0 else stages[j-1]['until'],'deadline':stages[j]['until']}
        assert a['stage']==expected and a['execution_sha256']==AUTH and a['case_deadline']==180
        assert a['time']+a['hold_native_steps']*.01<=stages[j]['until']+TOL
        stage_counts[j]+=1
    for k,b in [('position','position'),('angle','angle'),('velocity','velocity'),('omega','omega'),('commands','command'),('forces','force')]:assert d.native[-1][k]==d.final['body'][b]
    assert d.native[-1]['reserves']==[d.final['body']['energy'],d.final['body']['integrity']]
    assert d.native[-1]['stocks']==d.final['stocks'] and d.native[-1]['raw']==list(d.final['raw'])
    return {'valid':True,'analysis_version':'A2 read-only v1.0','alignment_source':'Preserved v3_checker_v1_1.align and validate_inputs, unchanged','native_rows':len(d.native),
       'sensor_entries':len(d.sensor),'initial_envelopes':1,'controller':inputs,'stage_decision_counts':dict(stage_counts),
       'inactive_organism_sha256':org_hash,'checkpoints':checks,'native_rng_counter_comparisons':len(d.native),'neural_wave_rows':0,
       'scope':'Record-level input/delivery, stage timing and checkpoint invariance; no controller recomputation, replay or unrecorded transient-state claim','mapping':mapping}

def ledger_check(d):
    rows=[];maximum=0.;discontinuities=[]
    for i,e in enumerate(d.events):
        if i:
            previous=d.events[i-1]
            for old,new in [('energy_after','energy_before'),('integrity_after','integrity_before'),('stock_after','stock_before')]:
                if previous[old]!=e[new]:discontinuities.append({'event_index':i,'previous_field':old,'current_field':new})
        intake=math.fsum(e['transfer']);renew=[a+b for a,b in zip(e['renewal_first'],e['renewal_second'])]
        er=(e['energy_after']-e['energy_before'])-(intake-e['expenditure'])
        sr=[e['stock_after'][j]-e['stock_before'][j]-renew[j]+e['transfer'][j] for j in range(8)]
        ir=(e['integrity_after']-e['integrity_before'])-(e['repair']-e['damage'])
        maximum=max(maximum,abs(er),abs(ir),*(abs(v) for v in sr))
        if e['duration']==0:assert intake==e['expenditure']==e['repair']==0
        rows.append({'event_index':i,'time':e['time'],'duration':e['duration'],'energy_residual':er,'stock_residuals':sr,'integrity_residual':ir,
           'body_credit':e['energy_after']-e['energy_before']+e['expenditure'],'transfer':e['transfer'],'source_debit':[e['stock_before'][j]+renew[j]-e['stock_after'][j] for j in range(8)],'expenditure':e['expenditure'],'renewal':renew})
    endpoint_mismatches=[]
    for n in d.native:
        i=bisect.bisect_right(d.event_times,n['time']+TOL)-1
        if i<0 or abs(d.events[i]['time']-n['time'])>TOL:endpoint_mismatches.append({'native_index':n['native_index'],'reason':'missing matching event endpoint'});continue
        e=d.events[i]
        if [e['energy_after'],e['integrity_after']]!=n['reserves'] or e['stock_after']!=n['stocks']:endpoint_mismatches.append({'native_index':n['native_index'],'event_index':i,'reason':'native/event reserve or stock mismatch'})
    return {'valid':maximum<=1e-12 and not discontinuities and not endpoint_mismatches,'maximum_residual':maximum,'arithmetic_tolerance':1e-12,'event_chain_discontinuities':discontinuities,'native_event_endpoint_mismatches':endpoint_mismatches,'rows':rows}

def contact_intervals(d,j):
    out=[]
    for i,e in enumerate(d.events):
        if e['duration']<=0 or not source_contact(e,j):continue
        a=e['time']-e['duration'];b=e['time']
        if out and abs(out[-1]['end']-a)<=TOL:
            out[-1]['end']=b;out[-1]['last_event']=i;out[-1]['duration']+=e['duration']
        else:out.append({'start':a,'end':b,'duration':e['duration'],'first_event':i,'last_event':i})
    return out

def windows(d,ledger):
    out=[];events=d.events;contactsets={j:contact_intervals(d,j) for j in (0,1)}
    for start in range(0,len(d.native),20):
        block=d.native[start:start+20];old=d.sample(start-1);new=d.sample(start+len(block)-1);a=old['time'];b=new['time']
        indices=list(range(bisect.bisect_right(d.event_times,a+TOL),bisect.bisect_right(d.event_times,b+TOL)))
        ix=[i for i in indices if events[i]['duration']>0]
        straddles=[i for i in ix if events[i]['time']-events[i]['duration']<a-TOL]
        # Any event extending beyond the endpoint must also be disclosed.
        k=bisect.bisect_right(d.event_times,b+TOL)
        if k<len(events) and events[k]['duration']>0 and events[k]['time']-events[k]['duration']<b-TOL:straddles.append(k)
        residual=math.fsum(abs(ledger['rows'][i]['energy_residual']) for i in ix)
        allowance=residual+(len(ix)+1)*1e-12;delta=new['reserves'][0]-old['reserves'][0]
        sign='positive_resolved' if delta>allowance else 'negative_resolved' if delta < -allowance else 'unresolved_at_accounting_resolution'
        sources={}
        for j in (0,1):
            support=math.fsum(max(0,min(b,c['end'])-max(a,c['start'])) for c in contactsets[j])
            sources[str(j)]={'transfer':math.fsum(events[i]['transfer'][j] for i in ix),'positive_duration_contact':any(source_contact(events[i],j) for i in ix),
                'support_seconds':support,'fully_supported':abs(support-(b-a))<=TOL}
        out.append({'first_native':block[0]['native_index'],'last_native':block[-1]['native_index'],'start_time':a,'end_time':b,
            'complete_0_2_second_interval':len(block)==20 and abs(b-a-.2)<=TOL,'energy_before':old['reserves'][0],'energy_after':new['reserves'][0],
            'energy_delta':delta,'position_before':old['position'],'position_after':new['position'],'stocks_before':old['stocks'],'stocks_after':new['stocks'],
            'all_source_transfer':math.fsum(math.fsum(events[i]['transfer']) for i in ix),'expenditure':math.fsum(events[i]['expenditure'] for i in ix),
            'absolute_energy_residual_sum':residual,'propagated_arithmetic_allowance':allowance,'net_energy_sign':sign,'sources':sources,'boundary_straddling_events':straddles})
    return out

def physical_observations(d,ledger,ws):
    events=d.events;end=d.final['time'];last=d.native[-1];sources={}
    for j in (0,1):
        centre=d.initial['c']['source_positions'][j]
        gap=lambda p:math.dist(p,centre)-d.initial['c']['body_radius']-d.initial['c']['source_radius']
        contact=[(i,e) for i,e in enumerate(events) if source_contact(e,j)]
        transfer=[(i,e) for i,e in enumerate(events) if e['transfer'][j]>0]
        intervals=contact_intervals(d,j)
        poses=[{'time':0.,'position':d.initial['body']['position'],'kind':'initial'}]
        poses += [{'time':n['time'],'position':n['position'],'native_index':n['native_index'],'kind':'native'} for n in d.native]
        poses += [{'time':e['time'],'position':e['body_position'],'event_index':i,'kind':'event'} for i,e in enumerate(events)]
        poses.sort(key=lambda x:x['time'])
        reached=next((dict(x,surface_gap=gap(x['position'])) for x in poses if -1e-8<=gap(x['position'])<=2e-10),None)
        eligible=[w for w in ws if w['complete_0_2_second_interval'] and w['sources'][str(j)]['positive_duration_contact']]
        firstpos=next((w for w in eligible if w['net_energy_sign']=='positive_resolved'),None)
        total=math.fsum(e['transfer'][j] for e in events)
        allowance=math.fsum(abs(r['stock_residuals'][j]) for r in ledger['rows'])+(len(events)+1)*1e-12
        forces=[c['force'] for _,e in contact if e['duration']>0 for c in e['contacts'] if c.get('source')==j and 'force' in c]
        sources[str(j)]={'geometric_arrival':reached,'minimum_recorded_surface_gap':min(gap(x['position']) for x in poses),
           'first_certified_contact':compact_event(*contact[0]) if contact else None,'first_positive_transfer':compact_event(*transfer[0]) if transfer else None,
           'contact_intervals':intervals,'positive_duration_contact_seconds':math.fsum(v['duration'] for v in intervals),
           'contact_event_count':len(contact),'transfer_total':total,'transfer_arithmetic_allowance':allowance,
           'transfer_sign':'positive_resolved' if total>allowance else 'zero' if total==0 else 'unresolved_at_accounting_resolution',
           'renewal_total':math.fsum(e['renewal_first'][j]+e['renewal_second'][j] for e in events),'initial_stock':d.initial['stocks'][j],'final_stock':d.final['stocks'][j],
           'first_positive_net_window':firstpos,'complete_contact_window_count':len(eligible),'positive_net_contact_window_count':sum(w['net_energy_sign']=='positive_resolved' for w in eligible),
           'negative_net_contact_window_count':sum(w['net_energy_sign']=='negative_resolved' for w in eligible),
           'fully_supported_complete_windows':sum(w['sources'][str(j)]['fully_supported'] for w in eligible),
           'sustained_force_range':None if not forces else [min(forces),max(forces)]}
    firstpositive=sources['0']['first_positive_net_window']
    negatives=[w for w in ws if firstpositive is not None and w['start_time']>=firstpositive['end_time']-TOL and w['end_time']<=90+TOL and w['complete_0_2_second_interval'] and w['sources']['0']['positive_duration_contact'] and w['net_energy_sign']=='negative_resolved']
    firstnegative=negatives[0] if negatives else None
    fullnegative=next((w for w in negatives if w['sources']['0']['fully_supported']),None)
    instruction=next((a for a in d.controller if a['stage']['index']==1),None)
    release=next(((i,e) for i,e in enumerate(events) if e['time']>=90-TOL and e.get('event_kind')=='release' and 'source-0' in e.get('colliders',[])),None)
    centre=d.initial['c']['source_positions'][0]
    gap0=lambda p:math.dist(p,centre)-1.
    supported={}
    for i,e in enumerate(events):
        if e['duration']>0 and source_contact(e,0):supported[round(e['time'],10)]=True
    clear=next((n for n in d.native if n['time']>=90-TOL and gap0(n['position'])>1e-10 and not supported.get(round(n['time'],10),False)),None)
    substantial=next((n for n in d.native if n['time']>=90-TOL and gap0(n['position'])>=1.),None)
    contact0before=[(i,e) for i,e in enumerate(events) if source_contact(e,0) and (clear is None or e['time']<=clear['time']+TOL)]
    departure_time=release[1]['time'] if release else clear['time'] if clear else None
    arrival=sources['1']['first_certified_contact'];arrival_time=arrival['time'] if arrival else None
    travel=None
    if departure_time is not None:
        stop=arrival_time if arrival_time is not None and arrival_time>=departure_time else end
        travel=d.interval(departure_time,stop);travel.update(arrived=arrival_time is not None and arrival_time>=departure_time,departure_endpoint_precision='exact release event' if release else 'first clear native endpoint; actual separation is bracketed')
    instructed=d.interval(90.,arrival_time if arrival_time is not None and arrival_time>=90 else end) if end>=90 else None
    mover_contacts=[compact_event(i,e) for i,e in enumerate(events) if any(c['collider']=='mover' for c in e['contacts'])]
    mover_gaps=[]
    for a in d.controller:
        f=next(f for f in a['inputs']['geometry'] if f['id']=='mover');x0,x1,y0,y1=f['rect'];x,y=a['inputs']['position']
        dx=max(x0-x,x-x1,0);dy=max(y0-y,y-y1,0)
        gap=math.hypot(dx,dy)-.5 if dx or dy else -min(x-x0,x1-x,y-y0,y1-y)-.5
        mover_gaps.append({'time':a['time'],'gap':gap,'body_position':[x,y],'mover_rectangle':f['rect'],'velocity':f['velocity']})
    return {'analysis_version':'A2 read-only v1.0','sources':sources,'first_negative_residence_window':firstnegative,'first_fully_supported_negative_residence_window':fullnegative,
       'departure_instruction':instruction,'release_event':compact_event(*release) if release else None,
       'first_clear_native':clear,'one_body_diameter_clearance_first_native':substantial,
       'departure_bracket':None if clear is None else {'last_source0_contact':compact_event(*contact0before[-1]) if contact0before else None,'first_clear_endpoint':d.sample(clear['native_index']-1)},
       'departure_EI_bracketing_native':d.bracket(departure_time) if departure_time is not None else None,
       'travel':travel,'commanded_travel_interval':instructed,
       'source0_recontacts_after_departure':[compact_event(i,e) for i,e in enumerate(events) if departure_time is not None and e['time']>departure_time+TOL and source_contact(e,0)],
       'maximum_source0_clearance_after_90':max((gap0(n['position']) for n in d.native if n['time']>=90-TOL),default=None),
       'mover':{'certified_contact_events':mover_contacts,'nearest_at_recorded_decision':min(mover_gaps,key=lambda x:x['gap']) if mover_gaps else None,'geometry_cadence_seconds':.1,
          'light_ray_interception':'Not identifiable from saved external-arm records: no ray-hit object identities were recorded. Raw light values alone do not certify mover interception. No new ray tracing performed.','other_causal_exposure':'unresolved'},
       'stage_totals':[dict(stage_index=i,**d.interval(a,min(b,end))) for i,(a,b) in enumerate(((0,90),(90,120),(120,180))) if end>=a],
       'whole_case':{'time':end,'native_index':d.final['native_index'],'initial_EI':[.7,1.],'final_EI':[d.final['body']['energy'],d.final['body']['integrity']],
         'native_final_EI':last['reserves'],'all_source_intake':math.fsum(math.fsum(e['transfer']) for e in events),'expenditure':math.fsum(e['expenditure'] for e in events),
         'net_E':d.final['body']['energy']-.7,'damage':math.fsum(e['damage'] for e in events),'repair':math.fsum(e['repair'] for e in events),
         'final_stocks':d.final['stocks'],'terminal_dimension':d.final['terminal_dimension'],'stop_label':d.receipt['status'],'stop_cause':d.receipt.get('stop_cause'),'record_complete':d.receipt['complete'],
         'controller_or_apparatus_exception':d.result['failure'],'receipt_error':d.receipt.get('error'),'planned_unobserved_seconds':max(0.,180-end)},
       'complete_window_count':sum(w['complete_0_2_second_interval'] for w in ws),'partial_window_count':sum(not w['complete_0_2_second_interval'] for w in ws),
       'interpretation':'Parallel observations only. Controller/route/reserve/physical causes remain distinct; missing arrival alone does not prove ecological infeasibility. No scientific efficacy claim.'}
