"""Independent bounded generic lifecycle probes. Never loads held PC/B1 state."""
import copy
from contextlib import contextmanager
import hashlib
import json
from pathlib import Path
import socket
import sys
import threading
import time
import urllib.error
import urllib.request
from unittest.mock import patch

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]; MODE=sys.argv[1]
OLD=ROOT/'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
NEW=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926/developmental_ecology'
SOURCE=OLD if MODE=='old' else NEW
OUT=HERE/(MODE+'-components'); OUT.mkdir(exist_ok=False)
sys.path[:0]=[str(SOURCE),str(SOURCE/'tests_apparatus')]
from test_apparatus import manufactured
from loom_p.records import state_hash,strict_bytes
from loom_p.geometry import transduce
from loom_p.chemistry import FieldSolver
from loom_commissioning import authority,runner,sensor_ui,adapter,validators
from loom_commissioning.contract import make_manifest,EXTERNAL

def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
assert Path(sensor_ui.__file__).resolve()==(SOURCE/'loom_commissioning/sensor_ui.py').resolve()
RESULT={'mode':MODE,'source':str(SOURCE),'scope':'Only delivered generic manufactured <=0.2-second fixtures. No held PC/B1 reads, snapshots, runs, replay, grants or authority generation.',
        'source_identity':{name:sha(SOURCE/'loom_commissioning'/name) for name in ('sensor_ui.py','runner.py','authority.py','pending.py','clock.py','adapter.py')},'checks':{}}
def save():
    raw=json.dumps(RESULT,indent=2,allow_nan=False);(HERE/(MODE+'-results.json')).write_text(raw,encoding='utf-8');print(raw,flush=True)
def reject(call,needle=None):
    try:call()
    except ValueError as error:
        text=str(error)
        if needle is not None:assert needle in text,(needle,text)
        return text
    raise AssertionError('Required rejection did not occur')
def physical(e):
    # Excludes only explicit failure/administrative status, not physical/RNG data.
    return state_hash({key:value for key,value in vars(e).items() if key not in ('status','failure')})
def snap(e,r):
    return {'engine':state_hash(e),'physical':physical(e),'session':state_hash(r.session),
        'native_index':e.native_index,'time':e.time,'body':state_hash(e.body),'fields':sha_bytes(e.fields.tobytes()),
        'neural_rng_wave':state_hash(e.organism),'energy':e.body.energy,'integrity':e.body.integrity,
        'execution_identity':authority.execution_sha256(r.manifest),'case_id':r.manifest['case_id']}
def sha_bytes(value):return hashlib.sha256(value).hexdigest()
def fresh(name,seconds=.2,display='chemistry_hidden'):
    e=manufactured();e.fields.fill(.17);e.raw=transduce(e.c,e.body,e.fields,e.time,e.phase)
    options={} if MODE=='old' else {'display':display}
    m=make_manifest(e,'fixture-independent-'+name,EXTERNAL,'sensor_human',seconds,**options)
    r=runner.Run(e,m,OUT/name);g=sensor_ui.HumanGateway(r)
    return e,r,g
def finish(r,g):
    if r.closed:return
    if MODE=='old':r.close();return
    try:g.end(g.envelope()['decision_token'])
    except Exception:
        r.engine.status='failure';r.engine.failure='bounded review cleanup';r.close('apparatus_failure',error='bounded review cleanup')
@contextmanager
def service(g):
    server=sensor_ui.OperatorHTTPServer(('127.0.0.1',0),sensor_ui.handler(g))
    thread=threading.Thread(target=server.serve_forever);thread.start()
    try:yield f'http://127.0.0.1:{server.server_port}'
    finally:server.shutdown();server.server_close();thread.join(5);assert not thread.is_alive()
def get(base,path='/session'):
    with urllib.request.urlopen(base+path,timeout=5) as response:return response.read()
def post(base,path,data):
    request=urllib.request.Request(base+path,data=strict_bytes(data),method='POST',headers={'Origin':base,'Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=5) as response:return json.loads(response.read())
def post_denied(base,path,data):
    try:post(base,path,data)
    except urllib.error.HTTPError as error:
        body=error.read();assert error.code==400 and body==sensor_ui.ERROR
        return {'status':400,'generic_error':True}
    raise AssertionError('Unexpected HTTP acceptance')

def old_cases():
    e,r,g=fresh('old-duplicate')
    try:
        hidden=copy.deepcopy(r.manifest)
        hidden['execution']['display_intervention']={'kind':'chemistry_hidden','implementation_sha256':sha(NEW/'loom_commissioning/operator_view.py')}
        hidden_error=reject(lambda:authority.validate_execution(hidden,complete=True),'unsupported display intervention')
        g.submit(.1,.1,'same submitted body');first=snap(e,r)
        g.submit(.1,.1,'same submitted body');second=snap(e,r)
        assert first['native_index']==10 and second['native_index']==20 and r.closed
        actions=validators.read_stream(r.recorder.path/'controller.jsonl.gz');assert len(actions)==2
        RESULT['checks']['actual_old_hidden_rejection']={'error':hidden_error,'native_before_commands':0,'scope':'Validation-only modified generic manufactured manifest, no grant.'}
        RESULT['checks']['actual_old_duplicate']={'after_first':first,'after_identical_second':second,'controller_records':len(actions),'closed_at_cutoff':r.closed,
            'full_generic_record_verification':validators.verify_segment(r.recorder.path)}
        save()
        assert e.native_index==10,'OLD DUPLICATE RED: identical duplicate accepted a second ten-step hold'
    finally:finish(r,g)

def main_lifecycle():
    e,r,g=fresh('lifecycle');foreign_e,foreign_r,foreign=fresh('foreign',display='none')
    release=threading.Event();entered=threading.Event();completed=threading.Event()
    counts={'hold_entries':0,'active':0,'maximum_active':0,'native_calls':0,'field_durations':[]}
    original_hold=r.hold;native=adapter.step;field=FieldSolver.step
    def slow_hold(*args):
        counts['hold_entries']+=1;counts['active']+=1;counts['maximum_active']=max(counts['maximum_active'],counts['active']);entered.set()
        try:assert release.wait(5);return original_hold(*args)
        finally:counts['active']-=1;completed.set()
    def counted_native(*args,**kwargs):counts['native_calls']+=1;return native(*args,**kwargs)
    def counted_field(self,*args,**kwargs):counts['field_durations'].append(args[4]);return field(self,*args,**kwargs)
    try:
        prepared=g.envelope();before=snap(e,r)
        assert prepared['lifecycle']=='prepared'
        prepared_errors=[reject(lambda:g.submit(.1,.1,'',prepared['decision_token'])),reject(lambda:r.begin_command([0,0])),reject(lambda:r.advance(0))]
        assert snap(e,r)==before
        paused=g.start(prepared['decision_token']);assert paused['lifecycle']=='paused' and state_hash(e)==before['engine']
        token=paused['decision_token'];assert token!=prepared['decision_token']
        paused_before=snap(e,r);payload_before=copy.deepcopy(paused)
        for elapsed in (5.,300.):
            with patch.object(sensor_ui.time,'perf_counter',return_value=r.started+elapsed):
                for _ in range(3):assert g.envelope()==payload_before
            assert snap(e,r)==paused_before
        foreign.start(foreign.envelope()['decision_token'])
        wrong_session=reject(lambda:g.submit(.1,.1,'foreign session',foreign.envelope()['decision_token']))
        stale_start=reject(lambda:g.submit(.1,.1,'stale start',prepared['decision_token']))
        assert snap(e,r)==paused_before
        with service(g) as base,patch.object(r,'hold',slow_hold),patch.object(adapter,'step',counted_native),patch.object(FieldSolver,'step',counted_field):
            # Repeated fresh HTTP connections while paused preserve exact custody.
            for path in ('/','/session','/sensors','/session'):get(base,path)
            assert json.loads(get(base))==payload_before and snap(e,r)==paused_before
            value={'left':.1,'right':.1,'annotation':'one generic hold','token':token}
            raw=strict_bytes(value);port=int(base.rsplit(':',1)[1])
            client=socket.create_connection(('127.0.0.1',port),timeout=5)
            try:
                header=f'POST /command HTTP/1.1\r\nHost: 127.0.0.1:{port}\r\nOrigin: {base}\r\nContent-Type: application/json\r\nContent-Length: {len(raw)}\r\nConnection: close\r\n\r\n'.encode()
                client.sendall(header+raw);assert entered.wait(5)
                running=json.loads(get(base));assert running['lifecycle']=='running' and running['decision_token'] is None
                assert running['sensors']==payload_before['sensors'] and state_hash(e)==paused_before['engine']
                # Duplicate command, attempted new lifecycle operations and reads
                # while the accepted request is deliberately held in flight.
                denied=[post_denied(base,'/command',value),post_denied(base,'/command',value),
                        post_denied(base,'/start',{'token':token}),post_denied(base,'/end',{'token':token})]
                for path in ('/','/session','/sensors'):get(base,path)
                assert counts['hold_entries']==1 and counts['native_calls']==0
            finally:
                client.close()  # Browser/network disconnect cannot create/retry a command.
                release.set()
            assert completed.wait(5)
            deadline=time.monotonic()+5
            while True:
                after=json.loads(get(base))
                if after['lifecycle']=='paused':break
                assert time.monotonic()<deadline;time.sleep(.002)
            assert e.native_index==10 and after['decision_token']!=token
            stable=snap(e,r)
            delayed=post_denied(base,'/command',value)
            for _ in range(3):assert json.loads(get(base))==after
            assert snap(e,r)==stable and counts['native_calls']==10
        assert counts=={'hold_entries':1,'active':0,'maximum_active':1,'native_calls':10,'field_durations':[.01]*10}
        assert r.recorder.counts['controller']==1
        end_state=g.end(after['decision_token']);assert end_state['lifecycle']=='ended' and end_state['decision_token'] is None
        final=snap(e,r)
        ended_errors=[reject(lambda:g.submit(0,0,'',after['decision_token'])),reject(lambda:g.start(after['decision_token'])),reject(lambda:r.hold([0,0]))]
        with patch.object(runner,'Recorder',side_effect=AssertionError('Resume output reached')) as recorder:
            resume_error=reject(lambda:runner.Run.resume(r.recorder.path,OUT/'resume-forbidden'),'interactive cases cannot resume')
        assert recorder.call_count==0 and not (OUT/'resume-forbidden').exists()
        with service(g) as base:
            for path in ('/','/session','/sensors','/session'):get(base,path)
            assert json.loads(get(base))['lifecycle']=='ended'
            post_denied(base,'/command',{'left':0,'right':0,'annotation':'','token':after['decision_token']})
        assert snap(e,r)==final
        RESULT['checks']['lifecycle_http']={'prepared_errors':prepared_errors,'prepared_physical_unchanged':True,
            'paused_5_and_300_wall_seconds_complete_engine_session_equal':True,'paused_custody_equal':True,
            'wrong_session_error':wrong_session,'stale_start_error':stale_start,'running_requests_denied':denied,
            'delayed_duplicate_denied':delayed,'running_published_only_last_complete_display':True,
            'client_disconnected_while_running':True,'counts':counts,'after_one_command':stable,
            'ended_errors':ended_errors,'interactive_resume_error':resume_error,'after_end_all_reads_rejections_inert':True,
            'complete_generic_record_verification':validators.verify_segment(r.recorder.path)}
    finally:
        release.set();finish(r,g);finish(foreign_r,foreign)

def closed_cutoff():
    e,r,g=fresh('cutoff',seconds=.1)
    try:
        g.start(g.envelope()['decision_token']);token=g.envelope()['decision_token'];g.submit(.1,.1,'cutoff',token)
        assert r.closed and e.native_index==10 and g.envelope()['lifecycle']=='ended'
        before=snap(e,r);error=reject(lambda:g.submit(.1,.1,'again',token));g.envelope();g.display()
        assert snap(e,r)==before
        RESULT['checks']['cutoff']={'native_index':10,'time':e.time,'ended':True,'after_end_error':error,'inert':True,
            'verification':validators.verify_segment(r.recorder.path)}
    finally:finish(r,g)

def binding_after_validation():
    checks={}
    for kind in ('case','authority_session','deprivation'):
        e,r,g=fresh('binding-'+kind)
        try:
            g.start(g.envelope()['decision_token']);token=g.envelope()['decision_token'];before=physical(e)
            if kind=='case':r.manifest['case_id']='fixture-another-case'
            elif kind=='authority_session':r.session['execution_sha256']='0'*64
            else:r.manifest['execution']['display_intervention']={'kind':'none'}
            with patch.object(adapter,'step',side_effect=AssertionError('Unauthorized native reached')) as causal:
                error=reject(lambda:g.submit(0,0,'',token),'request unavailable')
            assert causal.call_count==0 and physical(e)==before and e.native_index==0 and r.closed and g._state=='ended'
            checks[kind]={'operator_error':error,'native_calls':0,'native_index':e.native_index,'time':e.time,
                'physical_state_unchanged':True,'ended':True,'private_failure':e.failure,
                'limit':'Apparatus failure bookkeeping changes status; it does not evolve physical/RNG state.'}
        finally:finish(r,g)
    RESULT['checks']['post_validation_binding']=checks

if MODE=='old':old_cases()
elif MODE=='new':main_lifecycle();closed_cutoff();binding_after_validation();save();print('GREEN: bounded lifecycle, custody and one-command semantics verified',flush=True)
else:raise ValueError(MODE)
