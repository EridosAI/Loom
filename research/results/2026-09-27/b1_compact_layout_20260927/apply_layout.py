"""Apply Jason-approved CSS only; no Loom imports or world operations."""
from pathlib import Path
import hashlib,json,re,subprocess,copy
R=Path(__file__).resolve().parent.parent
S=Path(__file__).resolve().parent
W=R/'worktrees/loom-p-b1-apparatus-correction-20260926'
D=W/'developmental_ecology'
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
preview=R/'b1_compact_layout_preview/index.html'
assert sha(preview.read_bytes())=='880207be319ad796aed39fd4ab88c0d6fab00c191da9b56522548c8e1b4f5590'
p=D/'loom_commissioning/sensor.html';old=p.read_bytes()
assert sha(old)=='806221de1db825a72eaf8e5533553ff97cff11d30c4a7251cf517a128bcbcf9b'
style=re.search(rb'<style>[\s\S]*?</style>',preview.read_bytes()).group()
assert len(re.findall(rb'<style>',old))==1
new=re.sub(rb'<style>[\s\S]*?</style>',lambda m:style,old,count=1)
assert re.sub(rb'<style>[\s\S]*?</style>',b'',old)==re.sub(rb'<style>[\s\S]*?</style>',b'',new)
files=[q for pkg in ('loom_p','loom_commissioning') for q in (D/pkg).iterdir() if q.is_file() and q.suffix in ('.py','.html')]
files += [D/'configuration.json',D/'requirements-lock.txt']
before={q.relative_to(D).as_posix():sha(q.read_bytes()) for q in files}
write(S/'SOURCE_BEFORE.json',before)
p.write_bytes(new)
after={q.relative_to(D).as_posix():sha(q.read_bytes()) for q in files}
changed=[n for n in before if before[n]!=after[n]]
assert changed==['loom_commissioning/sensor.html']
write(S/'LAYOUT_BYTE_PROOF.json',dict(parent='352f73fffa6d9781eae8aa38e708a9a05669588f',changed_files=changed,
 old_html_sha256=sha(old),new_html_sha256=sha(new),approved_style_sha256=sha(style),outside_style_byte_identical=True,
 script_and_HTML_semantics_byte_identical=True,unchanged_files={n:h for n,h in after.items() if n not in changed},
 simulation_steps=0,world_loads=0,controller_commands=0))
# Offline browser checks use only the already disclosed CLOSED PC-HOLD record.
data=json.loads((R/'b1_pc_execution_20260926/runs/PC-HOLD-attempt-002/sensor-display.json').read_bytes())
for hidden in (False,True):
    v=copy.deepcopy(data);v['availability']='offline_record'
    if hidden:
        keep=[i for i,n in enumerate(v['raw_labels']) if not n.startswith('chemistry_')]
        v['raw_labels']=[v['raw_labels'][i] for i in keep];v['schema']=2
        for row in v['history']:row['raw']=[row['raw'][i] for i in keep]
    env=dict(schema=1,lifecycle='ended',display_condition='chemistry_hidden' if hidden else 'none',decision_token=None,sensors=v,offline=True)
    html=new.decode('utf-8')
    html=html.replace('<h1>Sensor-only reference</h1>','<h1>Compact layout — closed practice data</h1>')
    html=html.replace('Inspect the raw history and choose one paired command. Deliberation while paused consumes no bodily time.',
                      'Offline layout check · saved PC-HOLD data · no live connection · motor controls disabled.')
    html=html.replace("q('#refresh').onclick=read;","q('#refresh').onclick=()=>{};")
    tail="setInterval(()=>{if(session&&!session.offline&&!locked&&!inFlight)read();},1000);\nread();"
    assert html.count(tail)==1
    html=html.replace(tail,'accept('+json.dumps(env,separators=(',',':')).replace('</','<\\/')+",true);\nq('#refresh').disabled=true;")
    (R/'b1_compact_layout_preview'/('compact-hidden.html' if hidden else 'compact-full.html')).write_text(html,encoding='utf-8')
print(json.dumps(dict(changed_files=changed,outside_style_byte_identical=True,new_html_sha256=sha(new))))
