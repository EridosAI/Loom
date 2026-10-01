"""CSS-only coordinate colours and offline practice preview. No Loom imports."""
from pathlib import Path
import hashlib,json,copy,re,datetime
R=Path(__file__).resolve().parent.parent;S=Path(__file__).resolve().parent
W=R/'worktrees/loom-p-b1-coordinate-colours-20260929';D=W/'developmental_ecology'
active=R/'worktrees/loom-p-b1-apparatus-correction-20260926/developmental_ecology/loom_commissioning/sensor.html'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
p=D/'loom_commissioning/sensor.html';old=p.read_bytes()
expected='0b322ff6e4291e5cc68076002e3e37faecb178e5609eab858721abe6fbdc3a95'
assert sha(p)==sha(active)==expected
assert b'ctx.strokeStyle=`hsl(${k*360/indices.length},55%,40%)`' in old
rules=[];colours={}
for group,(name,count) in enumerate([('light',10),('chemistry',4),('contact',8),('proprioception',7)],1):
    for k in range(count):
        colour=f'hsl({k*360/count},55%,40%)';colours[f'{name}_{k}']=colour
        rules.append(f'#channels .panel:nth-child({group}) tr:nth-child({k+2}) td:first-child{{color:{colour}}}')
css='\n/* Coordinate names match their existing trace colours. */\n'+'\n'.join(rules)+'\n'
new=old.replace(b'</style>',css.encode()+b'</style>',1)
assert len(re.findall(b'</style>',old))==1
assert re.sub(rb'<style>[\s\S]*?</style>',b'',new)==re.sub(rb'<style>[\s\S]*?</style>',b'',old)
p.write_bytes(new)
write(S/'BYTE_PROOF.json',dict(parent='1060a17e3dd14c6361f6f15c95bb58fad3110ffc',old_html_sha256=expected,new_html_sha256=sha(p),
 outside_style_identical=True,only_addition=css,coordinate_colours=colours,active_html_unchanged=sha(active)==expected,
 new_legend=False,simulation_steps=0,controller_commands=0))
record=R/'b1_pc_execution_20260926/runs/PC-HOLD-attempt-002/sensor-display.json'
data=json.loads(record.read_bytes())
for hidden in (False,True):
    v=copy.deepcopy(data);v['availability']='offline_record'
    if hidden:
        keep=[i for i,n in enumerate(v['raw_labels']) if not n.startswith('chemistry_')]
        v['raw_labels']=[v['raw_labels'][i] for i in keep];v['schema']=2
        for row in v['history']:row['raw']=[row['raw'][i] for i in keep]
    env=dict(schema=1,lifecycle='ended',display_condition='chemistry_hidden' if hidden else 'none',decision_token=None,sensors=v,offline=True)
    html=new.decode().replace('<h1>Sensor-only reference</h1>','<h1>Coordinate colours — completed practice data</h1>')
    html=html.replace('Inspect the raw history and choose one paired command. Deliberation while paused consumes no bodily time.',
        'Offline preview · completed PC-HOLD · no connection to the active trial.')
    html=html.replace("q('#refresh').onclick=read;","q('#refresh').onclick=()=>{};")
    tail="setInterval(()=>{if(session&&!session.offline&&!locked&&!inFlight)read();},1000);\nread();"
    assert html.count(tail)==1
    html=html.replace(tail,'accept('+json.dumps(env,separators=(',',':')).replace('</','<\\/')+",true);\nq('#refresh').disabled=true;")
    (R/'b1_compact_layout_preview'/('colours-hidden.html' if hidden else 'colours-full.html')).write_text(html,encoding='utf-8')
write(R/'b1_execution_20260929_restart_01/OPERATOR_COLOUR_KEY_ASSISTANCE_CORRECTION.json',dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 corrects='OPERATOR_COLOUR_KEY_ASSISTANCE.json',correction='The separate colour-key draft was created but not delivered. Jason explicitly requested coloured coordinate labels and no separate key before delivery.',
 user_request='Write the coordinate label in the same colour as the graph. Don\'t add a separate key.',
 active_interface_unchanged=True,active_case_not_ended=True,observed_native_index_before_edit=120,assistant_commands=0))
print('Only coordinate-label CSS added in isolated checkout. Active trial unchanged. Offline practice previews prepared.')
