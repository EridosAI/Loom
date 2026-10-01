"""Optional loopback-only static viewer. No upload, control or simulation API."""
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
from urllib.parse import urlsplit
import argparse,mimetypes,os,time,webbrowser
ROOT=Path(__file__).resolve().parent
ALLOWED={'index.html','viewer.js','viewer_data.js','styles.css','V3_READ_ONLY_REANALYSIS_REPORT.md','VIEWER_DATA_FLOW.md'}
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        name=urlsplit(self.path).path.lstrip('/') or 'index.html'
        if name not in ALLOWED or not (ROOT/name).is_file():self.send_error(404);return
        data=(ROOT/name).read_bytes();self.send_response(200)
        self.send_header('Content-Type',(mimetypes.guess_type(name)[0] or 'application/octet-stream')+'; charset=utf-8')
        self.send_header('Content-Length',str(len(data)));self.send_header('Cache-Control','no-store');self.end_headers();self.wfile.write(data)
    def do_POST(self):self.send_error(405,'Read-only viewer')
    def do_PUT(self):self.send_error(405,'Read-only viewer')
    def do_DELETE(self):self.send_error(405,'Read-only viewer')
    def log_message(self,*args):pass
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=0);p.add_argument('--open',action='store_true');p.add_argument('--minutes',type=float,default=30);a=p.parse_args()
    server=HTTPServer(('127.0.0.1',a.port),Handler)
    url=f'http://127.0.0.1:{server.server_port}/'
    if a.open:
        print('Opening the saved A1 viewer. Close this window when finished. The local preview also stops after 30 minutes.',flush=True)
        webbrowser.open(url)
    else:print(f'PASSIVE_VIEWER_PID={os.getpid()} URL={url}',flush=True)
    server.timeout=1;deadline=time.monotonic()+a.minutes*60
    try:
        while time.monotonic()<deadline:server.handle_request()
    except KeyboardInterrupt:pass
    finally:server.server_close()
