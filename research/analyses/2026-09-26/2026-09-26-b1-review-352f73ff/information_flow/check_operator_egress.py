"""Display-only omission using delivered generic fixtures; no held B1 data."""
import contextlib,copy,hashlib,io,json,sys,tempfile,urllib.error,urllib.request
from pathlib import Path
from unittest.mock import patch
HERE=Path(__file__).resolve().parent;W=HERE.parents[2]
D=W/'worktrees/loom-p-b1-apparatus-correction-20260926/developmental_ecology'
sys.path[:0]=[str(D),str(D/'tests_apparatus')]
from test_apparatus import manufactured
from test_b1_operator import raw_fixture,service,CANARY
from loom_p.geometry import transduce
from loom_p.records import state_hash,strict_bytes
from loom_commissioning import sensor_ui,operator_view
from loom_commissioning.contract import make_manifest,EXTERNAL
from loom_commissioning.runner import Run
from loom_commissioning.validators import read_stream,verify_segment

OUT=Path(tempfile.mkdtemp(prefix='generic-fixtures-',dir=HERE))
RESULT={'source':str(D),'output':str(OUT),'scope':'Only delivered generic manufactured 0.2s pair and invented canary payload; no held B1 or prepared positive-control state.', 'paired':[]}
def request(base,path,value=None):
    req=urllib.request.Request(base+path,data=None if value is None else strict_bytes(value),
        headers={} if value is None else {'Origin':base,'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=15) as response:
            return response.status,response.read(),dict(response.headers)
    except urllib.error.HTTPError as error:return error.code,error.read(),dict(error.headers)
def decode(base,path,value=None):
    status,body,headers=request(base,path,value);assert status==200,(path,status,body)
    assert headers['Cache-Control']=='no-store'
    return json.loads(body)

initial=manufactured();initial.fields.fill(.17)
initial.raw=transduce(initial.c,initial.body,initial.fields,0.,initial.phase)
final=[];raw_records=[]
for mode in ('none','chemistry_hidden'):
    e=copy.deepcopy(initial)
    m=make_manifest(e,'fixture-identical-physics',EXTERNAL,'sensor_human',.2,display=mode)
    root=OUT/mode;r=Run(e,m,root);g=sensor_ui.HumanGateway(r);public=[]
    with service(g) as base:
        prepared=decode(base,'/session');public.append(prepared)
        assert prepared['lifecycle']=='prepared'
        paused=decode(base,'/start',{'token':prepared['decision_token']});public.append(paused)
        for left,right in ((.13,.07),(-.1,.04)):
            previous=public[-1]
            response=decode(base,'/command',{'left':left,'right':right,'annotation':'manufactured','token':previous['decision_token']})
            public.append(response)
            sensors=decode(base,'/sensors');assert sensors==response['sensors']
        assert public[-1]['lifecycle']=='ended' and e.native_index==20
        assert decode(base,'/session')==public[-1]
    (OUT/(mode+'-HTTP.json')).write_text(json.dumps(public,indent=2),encoding='utf-8')
    raw={name:read_stream(root/(name+'.jsonl.gz')) for name in ('native','wave','events','sensor')}
    complete=[*raw['sensor'][0]['history'],*raw['sensor'][1:]]
    assert len(complete)==21 and all(len(row['raw'])==29 for row in complete)
    assert all(any(v!=0 for v in row['raw'][10:14]) for row in complete)
    for envelope in public:
        payload=envelope['sensors'];width=29 if mode=='none' else 25
        assert payload['schema']==(1 if mode=='none' else 2)
        assert len(payload['raw_labels'])==width and all(len(row['raw'])==width for row in payload['history'])
        for shown,truth in zip(payload['history'],complete):
            assert shown==dict(truth,raw=truth['raw'] if mode=='none' else [truth['raw'][i] for i in operator_view.KEPT])
    actions=read_stream(root/'controller.jsonl.gz')
    assert actions[0]['inputs']==public[1]['sensors'] and actions[1]['inputs']==public[2]['sensors']
    saved=json.loads((root/'sensor-display.json').read_bytes())
    assert saved==public[-1]['sensors']
    assert sensor_ui.OfflineGateway(root/'sensor-display.json').display()['history']==saved['history']
    verification=verify_segment(root)
    final.append(state_hash(e));raw_records.append(raw)
    RESULT['paired'].append({'condition':mode,'native_steps':e.native_index,'raw_rows':len(complete),
        'raw_width':29,'operator_width':width,'operator_history_lengths':[len(x['sensors']['history']) for x in public],
        'all_operator_values_exact_selected_raw_coordinates':True,'real_chemistry_retained_nonzero_all_rows':True,
        'action_inputs_equal_actual_previous_operator_surface':True,'saved_operator_file_equals_HTTP':True,
        'final_physical_hash':final[-1],'raw_stream_hashes':{k:hashlib.sha256(strict_bytes(v)).hexdigest() for k,v in raw.items()},
        'verification':verification})
assert final[0]==final[1] and raw_records[0]==raw_records[1]
RESULT['physical_and_raw_evidence_identical_across_display_conditions']=True

# Invented canary only; this gateway owns no Engine and cannot advance one.
truth=raw_fixture();unchanged=copy.deepcopy(truth)
class CanaryGateway:
    intervention=operator_view.display_identity('chemistry_hidden')
    def display(self):return operator_view.project(truth,self.intervention)
    def envelope(self):return {'schema':1,'lifecycle':'paused','display_condition':'chemistry_hidden',
        'decision_token':'invented-token','sensors':self.display(),'offline':False}
    def submit(self,*args):raise ValueError('INVENTED PRIVATE CHEMISTRY '+str(CANARY))
g=CanaryGateway();egress=[];stdout=io.StringIO();stderr=io.StringIO()
with contextlib.redirect_stdout(stdout),contextlib.redirect_stderr(stderr),service(g) as base:
    for endpoint in ('/','/sensors','/session'):
        status,body,headers=request(base,endpoint)
        assert status==200 and str(CANARY).encode() not in body
        egress.append({'endpoint':endpoint,'status':status,'canary_present':False,'bytes':len(body)})
    for endpoint in ('/evaluation','/state','/manifest.json','/sensor-display.json','/../configuration.json','/socket','/debug','/download','/snapshot'):
        status,body,_=request(base,endpoint)
        assert status==404 and body==b'Unavailable'
        egress.append({'endpoint':endpoint,'status':status,'generic_body':True})
    status,body,_=request(base,'/command',dict(left=0,right=0,annotation='',token='invented-token'))
    assert status==400 and body==sensor_ui.ERROR and str(CANARY).encode() not in body
    egress.append({'endpoint':'/command','private_exception_status':status,'generic_error_exact':True})
    for kind in ('payload','aggregate'):
        bad=g.envelope()
        if kind=='payload':bad['sensors']['history'][0]['raw'].insert(10,CANARY)
        else:bad['chemistry_mean']=CANARY
        with patch.object(g,'envelope',return_value=bad):
            status,body,_=request(base,'/session')
        assert status==400 and body==sensor_ui.ERROR
        egress.append({'injected_leak':kind,'status':status,'generic_error_exact':True})
assert truth==unchanged and stdout.getvalue()==stderr.getvalue()==''
RESULT['invented_canary_HTTP']=egress
RESULT['server_stdout_stderr_empty']=True
RESULT['projection_source_object_unchanged']=True
RESULT['all_expected_assertions_passed']=True
(OUT/'RESULT.json').write_text(json.dumps(RESULT,indent=2),encoding='utf-8')
print(json.dumps({'output':str(OUT),'paired_physical_hash':final[0],'operator_widths':[29,25],
    'raw_width':29,'raw_rows_per_condition':21,'canary_route_checks':len(egress),'all_checks_passed':True},indent=2))
