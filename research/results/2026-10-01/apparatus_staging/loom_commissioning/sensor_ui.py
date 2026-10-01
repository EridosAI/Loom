"""Loopback sensor-only interface. The default entry point is inert saved review."""
import argparse
import copy
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from pathlib import Path
from .controllers import validate_sensor_payload
from .contract import require, strict_bytes

class OfflineGateway:
    def __init__(self,path):
        self.data=json.loads(Path(path).read_bytes())
        validate_sensor_payload(self.data); self.data['availability']='offline_record'
    def display(self): return copy.deepcopy(self.data)
    def submit(self,*args): raise ValueError('Saved review cannot advance time')

class HumanGateway:
    """No evaluation endpoint. A later authorized run can supply this gateway."""
    def __init__(self,run):
        require(run.manifest['controller']=='sensor_human','sensor-human run required')
        self._run=run
    def display(self): return self._run.display()
    def submit(self,left,right,annotation):
        self._run.hold([left,right],annotation)
        return self.display()

def handler(gateway):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def send(self,code,body,content_type):
            self.send_response(code)
            self.send_header('Content-Type',content_type)
            self.send_header('Cache-Control','no-store')
            self.send_header('X-Content-Type-Options','nosniff')
            self.end_headers(); self.wfile.write(body)
        def do_GET(self):
            if self.path=='/':
                self.send(200,Path(__file__).with_name('sensor.html').read_bytes(),'text/html; charset=utf-8')
            elif self.path=='/sensors':
                value=gateway.display(); validate_sensor_payload(value)
                self.send(200,strict_bytes(value),'application/json')
            else: self.send(404,b'Unavailable','text/plain')
        def do_POST(self):
            # No generic file serving, evaluation, snapshot or state-setting API.
            if self.path!='/command': self.send(404,b'Unavailable','text/plain'); return
            try:
                require(self.headers.get('Origin')==f'http://{self.headers.get("Host")}', 'origin mismatch')
                require(self.headers.get('Content-Type')=='application/json', 'JSON required')
                size=int(self.headers.get('Content-Length','0')); require(0<size<=4096,'request size')
                value=json.loads(self.rfile.read(size)); require(set(value)=={'left','right','annotation'},'command schema')
                require(isinstance(value['annotation'],str) and len(value['annotation'])<=1000,'annotation length')
                output=gateway.submit(value['left'],value['right'],value['annotation'])
                validate_sensor_payload(output); self.send(200,strict_bytes(output),'application/json')
            except Exception:
                # Privileged physics exceptions and event details never reach the operator.
                self.send(400,b'{"message":"Command unavailable; time has paused."}','application/json')
    return Handler

def main():
    parser=argparse.ArgumentParser(description='Paused, sensor-only saved review; no world is created')
    parser.add_argument('--record',required=True); parser.add_argument('--port',type=int,default=8768)
    args=parser.parse_args()
    server=HTTPServer(('127.0.0.1',args.port),handler(OfflineGateway(args.record)))
    print(f'Saved sensor review: http://127.0.0.1:{args.port} (no world updates)',flush=True)
    try: server.serve_forever()
    except KeyboardInterrupt: pass
    finally: server.server_close()

if __name__=='__main__': main()
