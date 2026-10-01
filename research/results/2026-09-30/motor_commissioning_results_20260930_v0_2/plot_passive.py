"""Passive figures; no simulation modules or live renderer."""
from pathlib import Path
import ast,json,math,time
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from reportlab.graphics.shapes import Drawing,Line,Rect,Circle,PolyLine,String
from reportlab.graphics import renderSVG
from reportlab.lib.colors import HexColor
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent;began=time.perf_counter()
source=ROOT/'motor_commissioning_results_20260930_v0_1/plot_passive.py'
tree=ast.parse(source.read_text())
exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,(ast.FunctionDef,ast.ClassDef))],type_ignores=[]),str(source),'exec'))
cfg=json.loads((ROOT/'worktrees/loom-contact-release-20260930/developmental_ecology/configuration.json').read_bytes())
results=json.loads((OUT/'PASSIVE_RESULTS.json').read_bytes());by={r['case_id']:r for r in results}
data={r['case_id']:np.load(OUT/(r['case_id']+'_PASSIVE_PLOT_DATA.npz')) for r in results if r.get('kinematics')}
names=['CURRENT','M1','M2'];colors=['#24649c','#b36817','#784baa'];dashes=[None,[6,4],[2,3]]
ids=lambda i:[f'MC-FS-{i:03d}-{n}' for n in names]
def ticks(lo,hi):return np.linspace(lo,hi,5)
def trace(f,X,Y,t,v,col,width=1.5,dash=None,step=10):
    idx=np.unique(np.r_[np.arange(0,len(t),step),len(t)-1])
    f.line([(X(t[k]),Y(v[k])) for k in idx],col,width,dash=dash)

f=Fig(1440,1750)
f.text(30,20,'Corrected motor screen: all nine recorded paths',27,bold=True)
f.text(30,62,'Each row shares a square world-coordinate zoom across CURRENT / M1 / M2. Different rows may use different zooms.',14)
f.text(30,88,'Black dot = birth; circle + heading = final body. Grey rectangle = final mover pose; grey line = sampled mover centres.',13)
f.text(30,110,'Tan circle = energy-source surface. Dark line = arena wall. These are passive recorded paths, not a live view.',13)
for i in range(1,4):
    caseids=ids(i);available=[data[n]['position'] for n in caseids if n in data]
    if not available:continue
    allp=np.concatenate(available);lo=allp.min(axis=0);hi=allp.max(axis=0);span=max(4,math.ceil(max(hi-lo)+1.6));mid=np.round((lo+hi)*1)/2
    xl=(float(mid[0]-span/2),float(mid[0]+span/2));yl=(float(mid[1]-span/2),float(mid[1]+span/2))
    for j,n in enumerate(caseids):
        x=65+j*470;y=190+(i-1)*520;w=365
        f.text(x,y-57,f'FS-{i:03d} | {names[j]}',20,colors[j],True)
        if n not in data:f.text(x,y,'UNSTARTED',17);continue
        d=data[n];r=by[n];X,Y=axis(f,x,y,w,w,xl,yl,ticks(*xl),ticks(*yl),'world x (units)','world y (units)')
        # Clip rectangles to visible axes; only surfaces actually in this zoom.
        rects=list(cfg['repair_rectangles'])+[d['mover_rectangle'][-1].tolist()]
        for rr in rects:
            a,b,c,e=rr;a=max(a,xl[0]);b=min(b,xl[1]);c=max(c,yl[0]);e=min(e,yl[1])
            if b>a and e>c:f.rect(X(a),Y(e),X(b)-X(a),Y(c)-Y(e),fill='#e1e5ea',stroke='#9fa8b5')
        for px,py in cfg['source_positions']:
            radius=cfg['source_radius']
            if xl[0]+radius<=px<=xl[1]-radius and yl[0]+radius<=py<=yl[1]-radius:
                f.circle(X(px),Y(py),w*radius/span,fill='#e9e4cf',stroke='#aba181')
        if yl[0]<=10<=yl[1]:
            centres=(d['mover_rectangle'][:,0]+d['mover_rectangle'][:,1])/2
            a=max(xl[0],float(centres.min()));b=min(xl[1],float(centres.max()))
            if b>a:f.line([(X(a),Y(10)),(X(b),Y(10))],'#bbc3cd',1)
        for wall in (0,20):
            if xl[0]<=wall<=xl[1]:f.line([(X(wall),Y(yl[0])),(X(wall),Y(yl[1]))],'#687384',2)
            if yl[0]<=wall<=yl[1]:f.line([(X(xl[0]),Y(wall)),(X(xl[1]),Y(wall))],'#687384',2)
        p=d['position'];idx=np.unique(np.r_[np.arange(0,len(p),5),len(p)-1]);col=colors[j]
        f.line([(X(a),Y(b)) for a,b in p[idx]],col,2)
        f.circle(X(p[0,0]),Y(p[0,1]),3.5,fill='#111827')
        end=p[-1];tip=end+.4*np.array([math.cos(d['angle'][-1]),math.sin(d['angle'][-1])])
        f.circle(X(end[0]),Y(end[1]),w*.5/span,stroke=col)
        f.line([(X(end[0]),Y(end[1])),(X(tip[0]),Y(tip[1]))],col,2)
        f.circle(X(end[0]),Y(end[1]),3,fill=col,stroke=col)
        k=r['kinematics'];f.text(x,y+408,f"Path {k['path_length']:.3f} | max excursion {k['maximum_excursion']:.3f}",13)
        f.text(x,y+430,f"{k['duration_s']:.2f} s | effort {r['physical']['effort_expenditure']:.6f}",13)
f.text(30,1712,'Metrics use full 0.01 s records. Paths displayed at 0.05 s. Mover trace is not a permanently occupied region.',13)
f.save('NINE_CASE_PATHS')

f=Fig(1390,1170)
f.text(30,18,'Reach and coverage growth by matched start',27,bold=True)
for j,name in enumerate(names):
    f.line([(40+j*270,79),(78+j*270,79)],colors[j],3,dash=dashes[j]);f.text(90+j*270,66,name,15,colors[j],True)
maxexc=max(float(d['excursion'].max()) for d in data.values());maxcov=max(int(d['coverage025'].max()) for d in data.values())
lims=[math.ceil(maxexc*2)/2,math.ceil(maxcov/10)*10]
for i in range(1,4):
    for j,field in enumerate(('excursion','coverage025')):
        x=80+j*685;y=177+(i-1)*322;w=555;hh=212;upper=lims[j]
        f.text(x,y-52,f"FS-{i:03d} | "+('maximum birth excursion' if j==0 else '0.25-unit occupied cells'),19,bold=True)
        X,Y=axis(f,x,y,w,hh,(0,90),(0,upper),[0,10,30,60,90],ticks(0,upper),'age (seconds)','units' if j==0 else 'visited cells')
        for k,n in enumerate(ids(i)):
            if n not in data:continue
            d=data[n];t=d['time'];v=d[field]
            idx=np.unique(np.r_[np.arange(0,len(t),10),np.flatnonzero(np.diff(v)!=0)+1 if j else [],len(t)-1]).astype(int)
            f.line([(X(t[a]),Y(v[a])) for a in idx],colors[k],1.8,dash=dashes[k])
f.text(30,1130,'Same scales across starts. Centre-cell occupancy is not swept area. No source-outcome score or candidate selection.',13)
f.save('REACH_AND_COVERAGE')

f=Fig(1500,1260)
f.text(30,18,'M2: initial drive, target renewal and realised motion',27,bold=True)
f.text(30,62,'Dashed vertical lines = target selection. The old latent supplies that step; the first changed drive follows one native step later.',14)
f.text(30,90,'Spontaneous drive: left blue / right orange. Forward velocity: purple. Effort only: blue cumulative curve (basal cost excluded).',13)
f.text(30,110,'Red marks at the bottom of velocity panels = recorded contact intervals or impulses.',12,color='#a52d39')
effort_max=max(float(np.sum(np.diff(data[ids(i)[2]]['time'])*np.abs(data[ids(i)[2]]['commands'][1:]).mean(axis=1)*cfg['effort_cost'])) for i in range(1,4) if ids(i)[2] in data)
velocity_limit=math.ceil(max(float(np.max(abs(data[ids(i)[2]]['forward_velocity']))) for i in range(1,4) if ids(i)[2] in data)*10)/10
for i in range(1,4):
    n=ids(i)[2]
    if n not in data:continue
    d=data[n];r=by[n];m=r['M2_renewal_analysis'];waves=json.loads((OUT/(n+'_WAVE_COUPLING.json')).read_bytes())
    x=65+(i-1)*490;w=395
    f.text(x,132,f"FS-{i:03d}: initial drive RMS {m['initial_spontaneous_pair_rms']:.3f}",18,bold=True)
    for row in range(3):
        y=211+row*325;hh=215
        if row==0:ylim=(-.36,.36);label='spontaneous pair (pre-feedback)'
        elif row==1:ylim=(-velocity_limit,velocity_limit);label='body-forward velocity (units/s)'
        else:ylim=(0,math.ceil(effort_max*1000)/1000);label='cumulative effort expenditure'
        X,Y=axis(f,x,y,w,hh,(0,90),ylim,[0,30,60,90],ticks(*ylim),'age (seconds)',label)
        for renew in m['renewals']:
            at=renew['nominal_selection_time_s'];f.line([(X(at),y),(X(at),y+hh)],'#b8bec7',.8,dash=[3,4])
        if row==0:
            t=np.r_[0,[q['age'] for q in waves]];s=np.vstack((m['initial_spontaneous_pair'],[q['oscillator'] for q in waves]))
            for k in range(2):trace(f,X,Y,t,s[:,k],colors[k],step=1)
        elif row==1:
            assert np.max(abs(d['forward_velocity']))<=velocity_limit
            trace(f,X,Y,d['time'],d['forward_velocity'],colors[2])
            for contact in r['physical']['contact_event_rows']:
                a=contact['time']-contact['duration'];b=contact['time']
                f.line([(X(a),y+hh-3),(max(X(a)+.6,X(b)),y+hh-3)],'#a52d39',2)
        else:
            cost=np.r_[0,np.cumsum(np.diff(d['time'])*np.abs(d['commands'][1:]).mean(axis=1)*cfg['effort_cost'])]
            trace(f,X,Y,d['time'],cost,colors[0])
    f.text(x,1201,'First renewal %.1f s | %d observed renewals' % (m['first_target_renewal_time_s'],len(m['renewals'])),13)
f.save('M2_RENEWAL_TIMING')
print(json.dumps(dict(figures=['NINE_CASE_PATHS','REACH_AND_COVERAGE','M2_RENEWAL_TIMING'],render_seconds=time.perf_counter()-began,world_steps=0)))
