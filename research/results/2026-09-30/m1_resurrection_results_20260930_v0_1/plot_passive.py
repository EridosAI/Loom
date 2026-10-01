"""NON-CANONICAL RESURRECTION SANDBOX. Saved facts only; no live renderer."""
from pathlib import Path
import ast,json,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from reportlab.graphics.shapes import Drawing,Line,Rect,Circle,PolyLine,String
from reportlab.graphics import renderSVG
from reportlab.lib.colors import HexColor
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
source=OUT/'passive_reference_sources/historical_plot_helpers.py'
nodes=[n for n in ast.parse(source.read_text()).body if isinstance(n,(ast.FunctionDef,ast.ClassDef))]
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'))
cfg=json.loads((ROOT/'worktrees/loom-contact-release-20260930/developmental_ecology/configuration.json').read_bytes())
results=json.loads((OUT/'PASSIVE_RESULTS.json').read_bytes())['lives']
f=Fig(1480,2140)
f.text(30,18,'NON-CANONICAL RESURRECTION SANDBOX',25,bold=True)
f.text(30,57,'All twelve prepared organisms: available recorded paths',21)
f.text(30,90,'Blue = path; black dot = birth; red dot = final recorded position. All panels show the same arena.',13)
f.text(30,115,'Tan = source surfaces; grey = restorative surfaces. Moving obstacle is omitted from this path overview.',13)
for j,r in enumerate(results):
    name=r['life_id'];x=65+(j%3)*490;y=205+(j//3)*480;size=330
    f.text(x,y-48,name,19,bold=True)
    if 'kinematics' not in r:
        f.text(x,y,'UNSTARTED',19);continue
    d=np.load(OUT/(name+'_PLOT_DATA.npz'));X,Y=axis(f,x,y,size,size,(0,20),(0,20),(0,5,10,15,20),(0,5,10,15,20),'world x','world y')
    for px,py in cfg['source_positions']:f.circle(X(px),Y(py),size*cfg['source_radius']/20,fill='#ece3ca',stroke='#b99b63')
    for a,b,c,e in cfg['repair_rectangles']:f.rect(X(a),Y(e),X(b)-X(a),Y(c)-Y(e),fill='#dfe4e9',stroke='#919aa4')
    p=d['position'];idx=np.unique(np.r_[np.arange(0,len(p),3),len(p)-1]);f.line([(X(a),Y(b)) for a,b in p[idx]],'#24649c',1.4)
    f.circle(X(p[0,0]),Y(p[0,1]),3,fill='#111827');f.circle(X(p[-1,0]),Y(p[-1,1]),3,fill='#ae3434')
    k=r['kinematics'];f.text(x,y+371,f"Age {r['age']:.3f} s | {len(r['resurrections'])} support events",13)
    f.text(x,y+391,f"Path {k['path']:.2f} | max excursion {k['maximum_excursion']:.2f}",13)
    label='Host-crash prefix' if r['status']=='HOST_NATIVE_CRASH_DURABLE_PREFIX' else ('4,500 s complete' if r['status']=='OVERNIGHT_COMPLETE' else '600 s pilot; continuation unstarted')
    f.text(x,y+411,label,12,'#ad2831' if 'crash' in label else '#46566a')
f.text(30,2110,'Passive display only. External life support does not establish ordinary viability or learned competence.',13)
f.save('ALL_TWELVE_PATHS')
active=[r for r in results if 'kinematics' in r]
for r in active:
    d=np.load(OUT/(r['life_id']+'_PLOT_DATA.npz'));g=Fig(1420,1130);g.text(30,15,'NON-CANONICAL RESURRECTION SANDBOX',24,bold=True)
    g.text(30,54,r['life_id']+' — recorded history',21)
    g.text(30,91,'Red vertical marks indicate external resurrection. Reserve jumps are support, not source benefit or repair.',13)
    panels=[('Energy (orange) / integrity (blue)',[(d['reserves'][:,0],'#b36817'),(d['reserves'][:,1],'#24649c')],(0,1.05)),
            ('Maximum excursion (blue) / path length (orange)',[(d['excursion'],'#24649c'),(d['path'],'#b36817')],(0,max(1,float(d['path'].max())*1.05))),
            ('Occupied 0.25-unit cells',[(d['coverage'],'#24649c')],(0,max(1,float(d['coverage'].max())*1.05)))]
    for j,(title,curves,yl) in enumerate(panels):
        x=85;y=190+j*310;w=1220;hh=200;g.text(x,y-48,title,18,bold=True)
        X,Y=axis(g,x,y,w,hh,(0,max(.1,r['age'])),yl,np.linspace(0,max(.1,r['age']),6),np.linspace(*yl,5),'physical age (s)','')
        for coordinate,(v,col) in enumerate(curves):
            points=[(float(t),float(q),1) for t,q in zip(d['time'],v)]
            if j==0:
                # Include the exact terminal and restored values even when the
                # passive 0.1-second display sampling would miss that boundary.
                event_times={event['time'] for event in r['resurrections']}
                points=[p for p in points if p[0] not in event_times]
                for event in r['resurrections']:
                    points.extend([(event['time'],event['before_reserves'][coordinate],0),
                                   (event['time'],event['after_reserves'][coordinate],2)])
                points.sort(key=lambda p:(p[0],p[2]))
            g.line([(X(t),Y(q)) for t,q,_ in points],col,1.6)
        for event in r['resurrections']:g.line([(X(event['time']),y),(X(event['time']),y+hh)],'#ba4343',.8)
    g.save(r['life_id']+'_HISTORY')
