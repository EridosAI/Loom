"""A5 read-only analysis v1.0. Standard library and preserved record checker only."""
import base64,bisect,collections,gzip,hashlib,json,math,pathlib,sys
from fractions import Fraction
ROOT=pathlib.Path(__file__).resolve().parent.parent
PACKET=ROOT/'exports/2026-09-26-A5-launch-packet-68db2c58'
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from evidence import plain,packed_attr,canonical,digest,snapshot_data
from v3_checker_v1_1 import align,validate_inputs
AUTH='bdff35693db38800528d91e6d2d4d2085c640268e50713731df5ec27f8b76d1d'
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
       'contacts':e['contacts'],'colliders':e.get('colliders'),'damage':e['damage'],'repair':e['repair'],'repair_quality':e.get('repair_quality')}
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
        if b<a-TOL:raise ValueError('Reversed event interval')
        chosen=[(i,e) for i,e in enumerate(self.events) if e['duration']>0 and e['time']>a+TOL and e['time']<=b+TOL]
        straddles=[i for i,e in enumerate(self.events) if e['duration']>0 and any(e['time']-e['duration']<cut-TOL and e['time']>cut+TOL for cut in (a,b))]
        impacts=[(i,e) for i,e in enumerate(self.events) if e['duration']==0 and e['time']>a+TOL and e['time']<=b+TOL]
        return {'start':a,'end':b,'duration':max(0.,b-a),'whole_duration_events_included':len(chosen),
           'source_transfers':[math.fsum(e['transfer'][j] for _,e in chosen) for j in range(8)],
           'gross_intake':math.fsum(math.fsum(e['transfer']) for _,e in chosen),'expenditure':math.fsum(e['expenditure'] for _,e in chosen),
           'repair':math.fsum(e['repair'] for _,e in chosen),'duration_damage':math.fsum(e['damage'] for _,e in chosen),
           'impact_damage_excluding_start_including_end':math.fsum(e['damage'] for _,e in impacts),
           'boundary_straddling_events':straddles,'complete_event_boundary_coverage':not straddles,
           'timing_rule':'Symmetric 1e-10 boundary membership; costs/transfer are whole event sums, never proportional interpolation; impacts at the start excluded, endpoint included.'}

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
    if status=='administrative_cutoff':assert abs(d.final['time']-m['hard_stop_time'])<1e-9 and d.final['terminal_dimension'] is None
    elif status=='administrative_pause':assert d.final['time']<m['hard_stop_time']-1e-9 and d.final['terminal_dimension'] is None
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
    ends=[int(Fraction(str(p['until']))*100) for p in stages]
    for a in d.controller:
        j=0
        while j<len(stages)-1 and a['native_index']>=ends[j]:j+=1
        expected={'index':j,'identity':digest(sorted_bytes(stages[j])),'start_time':0. if j==0 else stages[j-1]['until'],'deadline':stages[j]['until']}
        assert a['stage']==expected and a['execution_sha256']==AUTH and a['case_deadline']==d.manifest['hard_stop_time']
        assert a['native_index']+a['hold_native_steps']<=ends[j]
        allowance=1e-10+(a['native_index']*2.**-53/(1-a['native_index']*2.**-53))*(a['native_index']*.01)+2*math.ulp(a['native_index']*.01)
        assert abs(a['time']-a['native_index']*.01)<=allowance
        stage_counts[j]+=1
    for k,b in [('position','position'),('angle','angle'),('velocity','velocity'),('omega','omega'),('commands','command'),('forces','force')]:assert d.native[-1][k]==d.final['body'][b]
    assert d.native[-1]['reserves']==[d.final['body']['energy'],d.final['body']['integrity']]
    assert d.native[-1]['stocks']==d.final['stocks'] and d.native[-1]['raw']==list(d.final['raw'])
    return {'valid':True,'analysis_version':'A5 read-only v1.0','alignment_source':'Preserved v3_checker_v1_1.align and validate_inputs, unchanged','native_rows':len(d.native),
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
