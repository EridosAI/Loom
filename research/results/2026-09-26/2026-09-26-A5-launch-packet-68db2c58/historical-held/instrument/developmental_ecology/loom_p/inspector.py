"""One loopback-only visual inspector. Launch and replay never advance the organism."""
import argparse
import gzip
import json
from http.server import BaseHTTPRequestHandler,HTTPServer
from pathlib import Path
import threading
import webbrowser
import numpy as np
from .records import view,strict_bytes,code_identity,load_snapshot,save_snapshot,state_hash,Recorder
from .geometry import mover
from .schema import Config

ROOT=Path(__file__).resolve().parents[1]

class Inspector:
    def __init__(self):
        self.engine=None; self.replay=[]; self.waves=[]; self.record_path=None; self.replay_index=0; self.recorder=None
        self.error=None; self.start_hash=None; self.session_steps=0; self.reconstructed=None
        candidates=sorted((ROOT/'artifacts').glob('smoke-contact_ui_1s-attempt-*/manifest.json'),reverse=True)
        verified=[p for p in candidates if json.loads(p.read_text()).get('complete')]
        path=verified[0].parent/'initial.snapshot.json.gz' if verified else ROOT/'artifacts'/'unavailable.snapshot'
        if path.exists():
            try:
                self.engine=load_snapshot(path); self.start_hash=state_hash(self.engine)
                self.record_path=str(path.parent)
                self.load_replay(path.parent)
            except Exception as error: self.error=str(error)
    def load_replay(self,path):
        """Only saved observer records. No Engine.step or snapshot reconstruction here."""
        self.replay=[]; self.waves=[]
        for name,target in [('native',self.replay),('wave',self.waves)]:
            source=Path(path)/(name+'.jsonl.gz')
            if source.exists():
                with gzip.open(source,'rt',encoding='utf-8') as f: target.extend(json.loads(line) for line in f)
        self.replay_index=-1
    def observation(self):
        c=self.engine.c if self.engine else Config()
        e=self.engine
        replay=self.replay[self.replay_index] if self.replay and self.replay_index>=0 else None
        native=replay if replay else (e.last_native if e and e.last_native else None)
        at=float(native['time']) if native else (e.time if e else 0.)
        phase=e.phase if e else 0.; rect,_=mover(c,at,phase)
        selected_wave=None
        if native:
            eligible=[w for w in self.waves if w['time']<=at+1e-10]
            if eligible: selected_wave=eligible[-1]
            elif not self.replay and e and e.last_wave: selected_wave=dict(time=e.time,**e.last_wave)
        elif e and e.last_wave: selected_wave=dict(time=e.time,**e.last_wave)
        history=[]
        if selected_wave:
            end=selected_wave['time']
            history=[r for r in self.replay if end-c.wave_dt<r['time']<=end+1e-10]
        parameters=None
        if e:
            o,provenance=self.reconstructed if self.reconstructed else (e.organism,dict(provenance='Loaded paused snapshot; not reconstructed at replay cursor',time=e.time))
            parameters=dict(provenance=provenance,snapshot_time=provenance['time'],sensory=[dict(shared=x.shared,fine=x.fine,shared_reference=x.shared_ref,fine_reference=x.fine_ref,opening=x.opening,weights=x.weights) for x in o.cortices],H=o.association.H,use=o.association.use,a=o.association.a,q=o.association.q)
        diag_path=ROOT/'artifacts'/'information_loss.json'
        diagnostics=json.loads(diag_path.read_text()) if diag_path.exists() else None
        return view(dict(status='PAUSED — UNCOMMISSIONED',available=e is not None,error=self.error,code=code_identity()['sha256'],configuration=c.identifier,configuration_sha256=c.identity(),illumination_boundary=c.illumination_boundary,widths=c.widths,pools=c.pools,counts=dict(packet=sum(c.packet_widths),central=c.central_width,maps=c.map_coefficients),world=dict(side=c.world_side,sources=c.source_positions,repair=c.repair_rectangles,mover=rect,position=native['position'] if native else (e.body.position if e else None),angle=native['angle'] if native else (e.body.angle if e else 0),stocks=native['stocks'] if native else (e.stocks if e else []),reserves=native['reserves'] if native else (e.body.reserves if e else [])),time=at,native=native,wave=selected_wave,history=history,parameters=parameters,diagnostics=diagnostics,replay_count=len(self.replay),replay_index=self.replay_index,record_path=self.record_path,session_steps=self.session_steps,budget='contact_ui_1s: at most 100 native steps; launch/replay advance none'))
    def command(self,action,value=None):
        if action=='replay':
            if not self.replay: raise ValueError('No saved native records')
            self.replay_index=max(0,min(len(self.replay)-1,int(value))); self.reconstructed=None; return
        if action=='reconstruct':
            if not self.record_path or self.replay_index<0: raise ValueError('Select a saved record first')
            from .reconstruction import reconstruct
            self.reconstructed=reconstruct(self.record_path,self.replay_index); return
        if action=='pause': return
        if action not in ('native','wave'): raise ValueError('Unknown inspector action')
        if self.engine is None: raise ValueError('No verified fixture snapshot is available')
        count=1 if action=='native' else 20-self.engine.native_index%20
        if self.session_steps+count>100: raise ValueError('Named contact/UI fixture budget exhausted; no automatic new run')
        if self.recorder is None:
            from datetime import datetime,timezone
            directory=ROOT/'artifacts'/('inspector-contact-fixture-'+datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
            self.recorder=Recorder(directory,dict(case='contact_ui_1s',mode='explicit_inspector_steps',max_simulated_seconds=1,configuration_sha256=self.engine.c.identity(),initial_state_sha256=self.start_hash))
            save_snapshot(directory/'initial.snapshot.json.gz',self.engine)
        self.replay=[]; self.waves=[]; self.reconstructed=None
        try:
            for _ in range(count):
                native,wave,events=self.engine.step(); self.session_steps+=1
                self.recorder.append('native',native)
                if wave is not None: self.recorder.append('wave',dict(time=self.engine.time,**wave))
                for event in events: self.recorder.append('events',event)
                if self.engine.status in ('terminal','failure'): break
            save_snapshot(self.recorder.path/f'pause-{self.session_steps}.snapshot.json.gz',self.engine)
        except Exception as error:
            self.error=f'{type(error).__name__}: {error}'; self.engine.status='failure'
            self.recorder.close('apparatus_failure',False,self.error); self.recorder=None
            raise
    def close(self):
        if self.recorder:
            self.recorder.close('paused_inspector_closed',True); self.recorder=None

PAGE=r'''<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Loom · P engineering inspector</title>
<style>
:root{color-scheme:dark;font:15px system-ui;background:#0c141b;color:#e4edf4}*{box-sizing:border-box}body{margin:0}header{padding:22px 28px;border-bottom:1px solid #30414b;display:flex;align-items:center;justify-content:space-between}h1{font-size:24px;margin:0 0 5px}h2{font-size:18px;margin:0 0 16px}.muted{color:#96aab8;font-size:13px}.badge{color:#a4e1c7;background:#17392e;padding:8px 12px;border-radius:20px;font-size:12px;font-weight:700}.controls{padding:16px 28px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;background:#111e27}button,select{font:inherit;border:1px solid #49616f;border-radius:7px;background:#203541;color:#e4edf4;padding:9px 14px;cursor:pointer}button:disabled{opacity:.4;cursor:not-allowed}.stop{border-color:#be7575;color:#ffb3b3}nav{display:flex;gap:5px;padding:0 28px;margin-top:20px}nav button[aria-selected=true]{background:#a4e1c7;color:#082418}main{padding:22px 28px}.grid{display:grid;grid-template-columns:minmax(340px,1.1fr) minmax(340px,1fr);gap:22px}.card{background:#13212b;border:1px solid #2c414d;border-radius:12px;padding:20px;margin-bottom:18px}canvas{width:100%;height:auto;background:#0c171e;border-radius:8px}pre{white-space:pre-wrap;overflow-wrap:anywhere;max-height:450px;overflow:auto;background:#0c171e;padding:14px;font-size:12px}details{margin-top:12px}summary{cursor:pointer;color:#a4e1c7}.metric{font-size:28px;margin:8px 0}.warning{padding:14px;border-left:3px solid #e9b879;background:#3a2c1c;margin-bottom:18px}.row{display:flex;justify-content:space-between;gap:16px}.meters{display:grid;grid-template-columns:1fr 1fr;gap:18px}input[type=range]{width:260px}.hidden{display:none}.note{line-height:1.6;color:#bed0dd}label{display:block;margin-bottom:10px}.legend{font-size:12px;color:#9cb0bd;line-height:1.8}footer{padding:10px 28px 24px;font-size:12px;color:#8ea3b1}@media(max-width:900px){.grid{grid-template-columns:1fr}}
</style></head><body><header><div><h1>Loom / P</h1><div class="muted">First bounded engineering implementation · observer access only</div></div><span class="badge">PAUSED · UNCOMMISSIONED</span></header>
<div class="controls"><button id="pause">Pause</button><button id="native">Native step · 0.01 s</button><button id="wave">Step to wave boundary</button><button id="stop" class="stop">Stop & close server</button><span id="clock">0.00 s</span><span class="muted" id="budget"></span></div>
<nav><button aria-selected="true" data-tab="world">World & body</button><button data-tab="flow">Internal data flow</button><button data-tab="development">Development & limits</button></nav><main><div id="message"></div>
<section id="world" class="grid"><div class="card"><h2>Physical world</h2><canvas id="arena" width="660" height="660"></canvas><div class="legend">Gold: finite sources · green: restorative surfaces · grey: prescribed mover · white: organism. Positions, IDs and stocks are observer-only.</div></div><div><div class="card"><h2>Actual bodily reserves</h2><div class="meters"><div>Energy<div id="energy" class="metric">—</div></div><div>Integrity<div id="integrity" class="metric">—</div></div></div><p class="note">Only physical uptake and repair replenish these. Evoked reserve content cannot refill the body.</p></div><div class="card"><h2>Saved-record replay</h2><label>Native record <input id="cursor" type="range" min="0" max="0" value="0"><span id="cursor-label">No saved records</span></label><p class="note">Replay reads saved observations. It does not train, advance clocks or redraw noise.</p><button id="reconstruct">Reconstruct selected parameters</button><div id="record" class="muted"></div></div><div class="card"><h2>Build identity</h2><div id="identity" class="muted"></div><details><summary>Current physical record</summary><pre id="physical"></pre></details></div></div></section>
<section id="flow" class="hidden"><div class="grid"><div class="card"><h2>Native history → packet</h2><label>Channel <select id="channel"><option value="0">Light</option><option value="1">Chemistry</option><option value="2">Contact</option><option value="3">Proprioception</option></select></label><canvas id="history" width="640" height="230"></canvas><p class="legend">One selected native coordinate. Raw input (gold), receptor residual (blue), cortical activity (green). Fixed vertical scale −1 to 1; zero and small signals are retained.</p><details open><summary>Exact means, endpoints, centred packets and traces</summary><pre id="packet"></pre></details></div><div class="card"><h2>Effective signal at point of use</h2><p class="note">Compare return contributions, body input and bias; learned and exploratory logits; direct motor feedback and evocation. Equal amplitudes are not a target.</p><pre id="signal"></pre></div></div><details><summary>Full native record, including underlying values</summary><pre id="native-record"></pre></details><details><summary>Full handoff record and ordering</summary><pre id="wave-record"></pre></details></section>
<section id="development" class="hidden"><div class="grid"><div class="card"><h2>Capacity & pooling</h2><p class="note"><span id="capacity"></span> This capacity is provisional. Activity diversity from fixed recurrence is not proof of useful unpooling.</p><pre id="pool"></pre><details><summary>Shared/residual rows and references at paused snapshot</summary><pre id="parameters"></pre></details></div><div class="card"><h2>Stored association versus transient activity</h2><p class="note">H and its use state are stored separately from a and q. Fading activity does not establish that stored associations have vanished.</p><pre id="maps"></pre><details><summary>Complete map/update values</summary><pre id="map-values"></pre></details></div></div><div class="card"><h2>Information-loss fixtures</h2><p class="note">Fixed manufactured histories, observed through the actual cortical and packet path. Numerical distinctions can be lost. These are mechanical calculations, not evidence of ecological learning or universal temporal adequacy.</p><pre id="diagnostics"></pre></div></section></main><footer>No useful learning, source discovery or survival requirement. No automatic runs, tuning, refills or source relocation.</footer>
<script>
let state=null;const $=id=>document.getElementById(id);const pretty=v=>JSON.stringify(v,null,2);function text(id,v){$(id).textContent=typeof v==='string'?v:pretty(v)}
function world(w){const ctx=$('arena').getContext('2d'),sz=660,k=sz/w.side;ctx.clearRect(0,0,sz,sz);ctx.strokeStyle='#314955';ctx.lineWidth=1;for(let i=0;i<=w.side;i++){ctx.beginPath();ctx.moveTo(i*k,0);ctx.lineTo(i*k,sz);ctx.moveTo(0,i*k);ctx.lineTo(sz,i*k);ctx.stroke()}function rect(r,color){ctx.fillStyle=color;ctx.fillRect(r[0]*k,sz-r[3]*k,(r[1]-r[0])*k,(r[3]-r[2])*k)}w.repair.forEach(r=>rect(r,'#4fba91'));rect(w.mover,'#6e8292');w.sources.forEach((p,i)=>{ctx.beginPath();ctx.arc(p[0]*k,sz-p[1]*k,.5*k,0,Math.PI*2);ctx.fillStyle='#d5ae62';ctx.fill();ctx.fillStyle='#f4dcad';ctx.fillText('S'+i+' '+(w.stocks[i]===undefined?'—':w.stocks[i].toFixed(3)),(p[0]+.7)*k,sz-p[1]*k)});if(w.position){const [x,y]=w.position;ctx.beginPath();ctx.arc(x*k,sz-y*k,.5*k,0,Math.PI*2);ctx.fillStyle='#e6eff5';ctx.fill();ctx.strokeStyle='#e6eff5';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(x*k,sz-y*k);ctx.lineTo((x+Math.cos(w.angle))*k,sz-(y+Math.sin(w.angle))*k);ctx.stroke()}}
function plot(rows,m){const ctx=$('history').getContext('2d');ctx.clearRect(0,0,640,230);ctx.strokeStyle='#385361';ctx.beginPath();ctx.moveTo(0,115);ctx.lineTo(640,115);ctx.stroke();for(const [key,color] of [['raw','#d5ae62'],['residual','#7fbbef'],['x_new','#7fe0af']]){ctx.strokeStyle=color;ctx.lineWidth=2;ctx.beginPath();rows.forEach((r,i)=>{const d=r.sensory?.[m],v=d?.[key]?.[0]??0,x=i*640/Math.max(1,rows.length-1),y=115-v*105;i?ctx.lineTo(x,y):ctx.moveTo(x,y)});ctx.stroke()}}
function render(s){state=s;text('clock',s.time.toFixed(2)+' s');text('budget',s.budget);$('native').disabled=!s.available||s.session_steps>=100;$('wave').disabled=!s.available||s.session_steps>=100;world(s.world);text('energy',s.world.reserves[0]?.toFixed(6)??'—');text('integrity',s.world.reserves[1]?.toFixed(6)??'—');text('identity',s.configuration+'\n'+s.configuration_sha256+'\nCode '+s.code+'\n'+pretty(s.counts)+'\nLight boundary: '+s.illumination_boundary);text('record',s.record_path??'No complete-loop records yet');$('cursor').max=Math.max(0,s.replay_count-1);$('cursor').value=s.replay_index;text('cursor-label',s.replay_index>=0?`${s.replay_index+1} / ${s.replay_count}`:'Initial paused snapshot');$('message').textContent='';if(!s.available||s.error){const el=document.createElement('div');el.className='warning';el.textContent=s.error??'Baseline fixture is not yet available. No verified contact fixture is available. No organism is running.';$('message').append(el)}const n=s.native,w=s.wave,m=Number($('channel').value);text('physical',n?{time:n.time,position:n.position,commands:n.commands,forces:n.forces,velocity:n.velocity,stocks:n.stocks,reserves:n.reserves}:{});plot(s.history,m);text('packet',w?{packet:w.packets[m],old_mean:w.old_means[m],beta:w.beta[m],trace:w.traces[m]}:{});text('signal',w?{Bq_q:w.regulation.Bq_q,Bv_body:w.regulation.Bv_body,bias:w.regulation.bias,learned:w.regulation.learned,exploration:w.regulation.exploration,controls:w.new_controls,motor:n?.motor}:n?.motor??{});text('native-record',n??{});text('wave-record',w??{});text('capacity','Sensory widths '+pretty(s.widths)+'; pool memberships '+pretty(s.pools)+'.');text('pool',n?.sensory?.[m]?.groups??{});text('parameters',s.parameters?{provenance:s.parameters.provenance,snapshot_time:s.parameters.snapshot_time,sensory:s.parameters.sensory[m]}:{});text('maps',w?{read_write_count:w.association.read_write_count,a_initial:w.association.a_initial,a_final:w.association.a_final,q:w.association.q}:{});text('map-values',w?.association??s.parameters??{});text('diagnostics',s.diagnostics?{distances:s.diagnostics.distances,compression:s.diagnostics.compression,contraction:s.diagnostics.contraction,interpretation:s.diagnostics.interpretation}:{});}
async function action(action,value){try{const r=await fetch('/api/action',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action,value})});const result=await r.json();if(!r.ok)throw Error(result.error);if(action==='stop'){text('message','Inspector stopped. No simulation continues.');document.querySelectorAll('button').forEach(b=>b.disabled=true);return}render(result)}catch(e){text('message',e.message)}}
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>{document.querySelectorAll('nav button').forEach(x=>x.setAttribute('aria-selected',String(x===b)));['world','flow','development'].forEach(id=>$(id).classList.toggle('hidden',id!==b.dataset.tab));if(state)render(state)});['pause','native','wave','stop','reconstruct'].forEach(id=>$(id).onclick=()=>action(id));$('cursor').oninput=()=>action('replay',$('cursor').value);$('channel').onchange=()=>state&&render(state);fetch('/api/state').then(r=>r.json()).then(render).catch(e=>text('message',e.message));
</script></body></html>'''

def serve(port=8767,open_browser=True):
    app=Inspector()
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def send(self,status,data,content_type='application/json'):
            self.send_response(status); self.send_header('Content-Type',content_type); self.send_header('Cache-Control','no-store'); self.send_header('Content-Length',str(len(data))); self.end_headers(); self.wfile.write(data)
        def do_GET(self):
            if self.path=='/': return self.send(200,PAGE.encode(),'text/html; charset=utf-8')
            if self.path=='/api/state': return self.send(200,strict_bytes(app.observation()))
            self.send(404,b'{}')
        def do_POST(self):
            try:
                if self.headers.get('Origin') not in (None,f'http://127.0.0.1:{port}'): raise ValueError('Unexpected request origin')
                if self.path!='/api/action': raise ValueError('Unknown endpoint')
                body=json.loads(self.rfile.read(min(int(self.headers.get('Content-Length','0')),4096)))
                if body['action']=='stop':
                    app.close(); self.send(200,b'{"status":"stopped"}'); threading.Thread(target=server.shutdown,daemon=True).start(); return
                app.command(body['action'],body.get('value')); self.send(200,strict_bytes(app.observation()))
            except Exception as error: self.send(400,strict_bytes({'error':f'{type(error).__name__}: {error}'}))
    server=HTTPServer(('127.0.0.1',port),Handler)
    print(f'Paused inspector: http://127.0.0.1:{port}',flush=True)
    if open_browser: webbrowser.open(f'http://127.0.0.1:{port}')
    try: server.serve_forever()
    finally: app.close(); server.server_close()

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--port',type=int,default=8767); parser.add_argument('--no-browser',action='store_true'); args=parser.parse_args()
    serve(args.port,not args.no_browser)
