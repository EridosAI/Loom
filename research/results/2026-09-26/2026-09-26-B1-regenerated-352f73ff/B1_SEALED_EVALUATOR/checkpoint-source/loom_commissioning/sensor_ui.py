"""Loopback operator service. No evaluator/file endpoint; no automatic command."""
import argparse
import copy
import gzip
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import secrets
import sys
import threading
import time
from .contract import require, strict_bytes, digest
from .authority import strict_loads
from .controllers import command_pair
from .operator_view import infer_display, validate_operator_payload

ERROR=b'{"message":"Request unavailable. Refresh the permitted display before deciding again. Do not resubmit an uncertain command."}'

def validate_envelope(value,intervention):
    require(type(value) is dict and set(value)=={'schema','lifecycle','display_condition','decision_token','sensors','offline'}
            and value['schema']==1 and value['lifecycle'] in ('prepared','paused','running','ended')
            and value['display_condition']==intervention['kind'] and type(value['offline']) is bool,
            'operator envelope mismatch')
    actionable=value['lifecycle'] in ('prepared','paused') and not value['offline']
    require(isinstance(value['decision_token'],str) if actionable else value['decision_token'] is None,
            'operator token mismatch')
    validate_operator_payload(value['sensors'],intervention)

class OperatorHTTPServer(ThreadingHTTPServer):
    daemon_threads=False
    def handle_error(self,request,client_address):pass  # No exception/log side channel.

class OfflineGateway:
    def __init__(self,path):
        self.data=strict_loads(Path(path).read_bytes())
        self.intervention=infer_display(self.data);self.data['availability']='offline_record'
    def display(self):return copy.deepcopy(self.data)
    def envelope(self):return {'schema':1,'lifecycle':'ended','display_condition':self.intervention['kind'],
                               'decision_token':None,'sensors':self.display(),'offline':True}
    def submit(self,*args):raise ValueError('Saved review cannot advance time')

class HumanGateway:
    """One interactive case, from prepared through irreversible ended.

    Readers see a copied last-complete display while a bounded hold runs.
    Tokens are consumed before actuation. Queued/retried old requests cannot
    become a second decision after network delay.
    """
    def __init__(self,run):
        run._guard()
        require(run.manifest['controller']=='sensor_human' and not run.closed
                and run.session['decision'] is None and run.session['advanced']==0
                and 'operator_lifecycle' not in run.session,'fresh sensor-human case required')
        self._run=run;self.intervention=copy.deepcopy(run.manifest['execution']['display_intervention'])
        self._lock=threading.RLock();self._nonce=secrets.token_hex(16);self._revision=0
        self._payload=run.display();self._state='prepared'
        run.session['operator_lifecycle']='prepared'
        run.recorder.streams['operator']=gzip.open(run.recorder.path/'operator.jsonl.gz','wb')
        from .runner import save_restart
        save_restart(run.recorder.path/'initial.restart.json.gz',run.engine,run.session,run.manifest)
        self._audit('prepared')

    def _token(self):
        return f'{self._nonce}:{self._revision}' if self._state in ('prepared','paused') else None

    def _audit(self,event):
        if self._run.closed:return
        self._run.recorder.append('operator',dict(event=event,lifecycle=self._state,
            wall_seconds=time.perf_counter()-self._run.started,
            display_condition=self.intervention['kind'],display_sha256=digest(strict_bytes(self._payload))))

    def _transition(self,state):
        require(self._state!='ended','ended is irreversible')
        self._state=state;self._run.session['operator_lifecycle']=state;self._revision+=1

    def _expire(self):
        if self._state in ('prepared','paused') and not self._run.closed:
            elapsed=self._run.session['wall_seconds_used']+time.perf_counter()-self._run.started
            if elapsed>=self._run.wall_limit:
                self._run.close('administrative_pause',cause='wall_time_limit')
        if self._run.closed:
            self._state='ended';self._payload=self._run.display()

    def display(self):
        with self._lock:
            self._expire();validate_operator_payload(self._payload,self.intervention)
            return copy.deepcopy(self._payload)

    def envelope(self):
        with self._lock:
            payload=self.display()
            return {'schema':1,'lifecycle':self._state,'display_condition':self.intervention['kind'],
                    'decision_token':self._token(),'sensors':payload,'offline':False}

    def _claim(self,token,state):
        self._expire()
        require(self._state==state and isinstance(token,str) and secrets.compare_digest(token,self._token()),
                'request unavailable')

    def start(self,token):
        with self._lock:
            self._claim(token,'prepared');self._transition('paused');self._audit('paused')
            return self.envelope()

    def submit(self,left,right,annotation,token):
        pair=command_pair([left,right])
        require(isinstance(annotation,str) and len(annotation)<=1000,'annotation length')
        # Claim/publication use the lock; native execution does not hold it.
        # RUNNING readers receive only the last complete permitted display.
        with self._lock:
            self._claim(token,'paused');self._transition('running')
            try:self._audit('command_accepted')
            except Exception as error:
                self._fail(error);raise ValueError('request unavailable') from None
        try:
            self._run.hold(pair,annotation)
            with self._lock:
                self._payload=self._run.display()
                if self._run.closed:self._state='ended'
                else:self._transition('paused');self._audit('paused')
                return self.envelope()
        except Exception as error:
            with self._lock:self._fail(error)
            raise ValueError('request unavailable') from None

    def _fail(self,error):
        self._state='ended';self._run.session['operator_lifecycle']='ended';self._revision+=1
        if not self._run.closed:
            self._run.engine.status='failure';self._run.engine.failure=f'{type(error).__name__}: {error}'
            try:self._run.close('apparatus_failure',error=self._run.engine.failure)
            except Exception:pass  # Preserve incomplete private receipt; never restart.
        self._payload=self._run.display()

    def end(self,token):
        with self._lock:
            self._expire();require(self._state in ('prepared','paused'),'request unavailable')
            self._claim(token,self._state)
            self._run.close('administrative_pause',cause='operator_withdrawal')
            self._state='ended';self._revision+=1;self._payload=self._run.display()
            return self.envelope()

    def shutdown(self):
        # server_close joins its bounded in-flight requests before this call.
        with self._lock:
            if self._state in ('prepared','paused'):self.end(self._token())
            require(self._state=='ended','cannot shut down during an active hold')

def handler(gateway):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def send(self,code,body,content_type):
            self.send_response(code);self.send_header('Content-Type',content_type)
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers();self.wfile.write(body)
        def do_GET(self):
            try:
                if self.path=='/':
                    self.send(200,Path(__file__).with_name('sensor.html').read_bytes(),'text/html; charset=utf-8')
                elif self.path in ('/sensors','/session'):
                    value=gateway.display() if self.path=='/sensors' else gateway.envelope()
                    payload=value if self.path=='/sensors' else value['sensors']
                    validate_operator_payload(payload,gateway.intervention)
                    if self.path=='/session':validate_envelope(value,gateway.intervention)
                    self.send(200,strict_bytes(value),'application/json')
                else:self.send(404,b'Unavailable','text/plain')
            except Exception:self.send(400,ERROR,'application/json')
        def do_POST(self):
            if self.path not in ('/command','/start','/end'):
                self.send(404,b'Unavailable','text/plain');return
            try:
                require(self.headers.get('Origin')==f'http://{self.headers.get("Host")}', 'origin mismatch')
                require(self.headers.get('Content-Type')=='application/json','JSON required')
                size=int(self.headers.get('Content-Length','0'));require(0<size<=8192,'request size')
                value=strict_loads(self.rfile.read(size))
                if self.path=='/command':
                    require(set(value)=={'left','right','annotation','token'},'command schema')
                    output=gateway.submit(value['left'],value['right'],value['annotation'],value['token'])
                else:
                    require(set(value)=={'token'},'lifecycle schema')
                    output=(gateway.start if self.path=='/start' else gateway.end)(value['token'])
                validate_envelope(output,gateway.intervention)
                self.send(200,strict_bytes(output),'application/json')
            except Exception:self.send(400,ERROR,'application/json')
    return Handler

def live_gateway(manifest_path,initial_path,output):
    """Explicit future granted launch. No case selection, grant or retry here."""
    from .authority import validate_execution
    from .contract import authorize_execution
    m=strict_loads(Path(manifest_path).read_bytes())
    require(m['purpose']=='commissioning' and m['controller']=='sensor_human','sensor-human commissioning manifest required')
    validate_execution(m,complete=True);authorize_execution(m)
    from loom_p.records import load_snapshot
    from .runner import Run
    run=Run(load_snapshot(initial_path),m,output)
    try:return HumanGateway(run)
    except Exception as error:
        if not run.closed:
            run.engine.status='failure';run.engine.failure=f'{type(error).__name__}: {error}'
            run.close('apparatus_failure',error=run.engine.failure)
        raise

def main():
    parser=argparse.ArgumentParser(description='Sensor-only operator service; no automatic world advancement')
    source=parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--record');source.add_argument('--manifest')
    parser.add_argument('--initial');parser.add_argument('--output');parser.add_argument('--port',type=int,default=8768)
    args=parser.parse_args()
    require(bool(args.manifest)==bool(args.initial and args.output),'live launch requires manifest, initial snapshot and new output')
    gateway=live_gateway(args.manifest,args.initial,args.output) if args.manifest else OfflineGateway(args.record)
    server=None
    try:
        server=OperatorHTTPServer(('127.0.0.1',args.port),handler(gateway))
        print(f'Sensor-only interface: http://127.0.0.1:{server.server_port} (no automatic commands)',flush=True)
        server.serve_forever()
    except KeyboardInterrupt:pass
    finally:
        if server is not None:server.server_close()
        if isinstance(gateway,HumanGateway):gateway.shutdown()

def entrypoint():
    try:main()
    except Exception:
        print('Operator interface unavailable. No automatic continuation. Consult the private apparatus record.',file=sys.stderr)
        return 1
    return 0

if __name__=='__main__':raise SystemExit(entrypoint())
