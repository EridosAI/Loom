"""Offline layout proposal from CLOSED PC-HOLD data; never connects to B1."""
import hashlib,json
from pathlib import Path
S=Path(__file__).resolve().parent;ROOT=S.parent
OUT=ROOT/'b1_compact_layout_preview'
source=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926/developmental_ecology/loom_commissioning/sensor.html'
record=S/'runs/PC-HOLD-attempt-002/sensor-display.json'
data=json.loads(record.read_bytes())
assert set(data)=={'schema','raw_labels','history','own_commands','annotations','availability'}
assert len(data['raw_labels'])==29 and len(data['own_commands'])==15
data['availability']='offline_record'
envelope=dict(schema=1,lifecycle='ended',display_condition='none',decision_token=None,sensors=data,offline=True)
css='''
*{box-sizing:border-box}
body{font:12px system-ui;background:#f5f4ef;color:#183a3c;margin:0;padding:10px;max-width:none}
h1{font-size:19px;margin:0 0 3px}h2{font-size:15px;margin:0 0 5px}h3{font-size:12px;margin:0}
p{line-height:1.3;margin:4px 0}.muted{color:#536764;font-size:11px}
.bar,.panel{background:white;border:1px solid #d3ddda;border-radius:8px;padding:8px;margin:7px 0}
.bar{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px 10px;align-items:center}
#state{font-size:16px;grid-column:1}#mode{grid-column:2}#current{grid-column:3}
#body{grid-column:1 / 4;font-size:14px;font-weight:650;margin:3px 0}
.bar>p:last-child{grid-column:1 / 4;margin:2px 0}
.grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:8px}
.grid .panel{margin:0;min-width:0}table{width:100%;border-collapse:collapse;font-variant-numeric:tabular-nums;font-size:11px}
td,th{padding:3px 1px;text-align:right;white-space:nowrap}td:first-child,th:first-child{text-align:left}
canvas{width:100%;height:78px}input{width:72px;padding:5px;font:inherit}
button{padding:6px 10px;background:#245c58;color:white;border:0;border-radius:5px;margin:0;font:inherit}
button:disabled{opacity:.55}label{display:inline-flex;align-items:center;gap:6px;margin-right:8px}
#note{width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere;margin:0;font-size:11px}
#channels+.panel{display:grid;grid-template-columns:170px 170px 130px 1fr;gap:5px 10px;align-items:center}
#channels+.panel>h2{grid-column:1 / 5;margin:0}
#channels+.panel>p:first-of-type{grid-column:1 / 5;margin:0}
#channels+.panel>label{margin:0}#send{align-self:stretch}
#channels+.panel>p:nth-of-type(2){margin:0;min-width:0}#channels+.panel>p:nth-of-type(2)>label{display:flex;margin:0}
#message{grid-column:1 / 5;margin:0}#message:empty{display:none}
#channels+.panel>h3:first-of-type{grid-column:1 / 3}#channels+.panel>h3:last-of-type{grid-column:3 / 5;grid-row:4}
#commands{grid-column:1 / 3;grid-row:5;max-height:35px;overflow:auto}
#notes{grid-column:3 / 5;grid-row:5;max-height:35px;overflow:auto}
#download{grid-column:4;justify-self:end}
body>.muted{margin:2px 0}
@media(max-width:1050px){.grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:650px){.grid{grid-template-columns:1fr}.bar{display:block}#channels+.panel{display:block}#commands,#notes{max-height:60px}}
'''
html=source.read_text(encoding='utf-8')
a=html.index('<style>');b=html.index('</style>',a)+len('</style>')
html=html[:a]+'<style>'+css+'</style>'+html[b:]
html=html.replace('<title>Loom · Sensor-only reference</title>','<title>Loom · Compact layout preview · Closed practice data</title>')
html=html.replace('<h1>Sensor-only reference</h1>','<h1>Compact layout preview — completed practice data</h1>')
html=html.replace('Inspect the raw history and choose one paired command. Deliberation while paused consumes no bodily time.',
    'Layout proposal only · saved PC-HOLD practice · no connection to B1 · motor controls disabled.')
html=html.replace("q('#refresh').onclick=read;","q('#refresh').onclick=()=>{};")
tail="setInterval(()=>{if(session&&!session.offline&&!locked&&!inFlight)read();},1000);\nread();"
assert html.count(tail)==1
html=html.replace(tail,'accept('+json.dumps(envelope,separators=(',',':')).replace('</','<\\/')+",true);\nq('#refresh').disabled=true;")
assert 'http://127.0.0.1:60615' not in html and 'setInterval(' not in html
OUT.mkdir(exist_ok=False)
(OUT/'index.html').write_text(html,encoding='utf-8')
provenance=dict(kind='OFFLINE LAYOUT PROPOSAL ONLY',source_case='PC-HOLD attempt 002',
    source_html_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    source_display_sha256=hashlib.sha256(record.read_bytes()).hexdigest(),
    preview_sha256=hashlib.sha256((OUT/'index.html').read_bytes()).hexdigest(),
    source_html_unchanged=True,B1_display_or_evaluator_data_used=False,
    no_live_service_connection=True,simulation_steps=0,controller_commands=0,
    changes='Compact CSS layout plus explicit offline initialization with saved disclosed PC data. Original rendering logic, values, history and coordinate order retained. No live use authorized.')
(OUT/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
print('Offline compact-layout preview created from closed PC data. Live B1 and production source unchanged.')
