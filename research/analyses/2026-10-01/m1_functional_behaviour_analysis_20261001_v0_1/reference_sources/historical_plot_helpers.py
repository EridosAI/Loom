"""Static ReportLab vector plots and matching Pillow raster previews; records only."""
from pathlib import Path
import json,math,time
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from reportlab.graphics.shapes import Drawing,Line,Rect,Circle,PolyLine,String
from reportlab.graphics import renderSVG
from reportlab.lib.colors import HexColor
OUT=Path(__file__).resolve().parent;began=time.perf_counter()
names=['CURRENT','M1','M2'];colors=['#24649c','#b36817','#784baa']
data=[np.load(OUT/f'MC-FS-001-{n}_PASSIVE_PLOT_DATA.npz') for n in names]
results=json.loads((OUT/'PASSIVE_RESULTS.json').read_bytes())[:3]

class Fig:
    def __init__(self,w,h):
        self.w=w;self.h=h;self.d=Drawing(w,h);self.im=Image.new('RGB',(w*2,h*2),'white');self.p=ImageDraw.Draw(self.im)
        self.rect(0,0,w,h,fill='#ffffff',stroke=None)
    def line(self,pts,color='#111827',width=1,dash=None):
        if len(pts)<2:return
        flat=[q for x,y in pts for q in (float(x),float(self.h-y))]
        self.d.add(PolyLine(flat,strokeColor=HexColor(color),strokeWidth=width,strokeDashArray=dash))
        if dash is None:
            self.p.line([(round(x*2),round(y*2)) for x,y in pts],fill=color,width=max(1,round(width*2)),joint='curve')
        else:
            phase=0;left=dash[0]
            for start,end in zip(pts,pts[1:]):
                s=np.array(start,dtype=float);e=np.array(end,dtype=float);length=float(np.linalg.norm(e-s))
                if length==0:continue
                direction=(e-s)/length;used=0.
                while used<length-1e-12:
                    take=min(left,length-used);a=s+used*direction;b=s+(used+take)*direction
                    if phase%2==0:self.p.line([(a[0]*2,a[1]*2),(b[0]*2,b[1]*2)],fill=color,width=max(1,round(width*2)))
                    used+=take;left-=take
                    if left<1e-10:phase=(phase+1)%len(dash);left=dash[phase]
    def rect(self,x,y,w,h,fill=None,stroke='#d1d5db',width=1):
        self.d.add(Rect(x,self.h-y-h,w,h,fillColor=HexColor(fill) if fill else None,strokeColor=HexColor(stroke) if stroke else None,strokeWidth=width))
        self.p.rectangle((round(x*2),round(y*2),round((x+w)*2),round((y+h)*2)),fill=fill,outline=stroke,width=max(1,round(width*2)))
    def circle(self,x,y,r,fill=None,stroke='#111827',width=1):
        self.d.add(Circle(x,self.h-y,r,fillColor=HexColor(fill) if fill else None,strokeColor=HexColor(stroke) if stroke else None,strokeWidth=width))
        self.p.ellipse(((x-r)*2,(y-r)*2,(x+r)*2,(y+r)*2),fill=fill,outline=stroke,width=max(1,round(width*2)))
    def text(self,x,y,text,size=13,color='#243044',bold=False):
        font='Helvetica-Bold' if bold else 'Helvetica'
        self.d.add(String(x,self.h-y-size,text,fontName=font,fontSize=size,fillColor=HexColor(color)))
        f=ImageFont.truetype('C:/Windows/Fonts/arialbd.ttf' if bold else 'C:/Windows/Fonts/arial.ttf',size*2)
        self.p.text((round(x*2),round(y*2)),text,font=f,fill=color)
    def save(self,name):
        renderSVG.drawToFile(self.d,str(OUT/(name+'.svg')))
        self.im.save(OUT/(name+'.png'))

def axis(f,x,y,w,h,xlim,ylim,xticks,yticks,xlabel,ylabel):
    X=lambda q:x+w*(q-xlim[0])/(xlim[1]-xlim[0])
    Y=lambda q:y+h-h*(q-ylim[0])/(ylim[1]-ylim[0])
    for val in yticks:
        f.line([(x,Y(val)),(x+w,Y(val))],color='#e5e7eb')
        f.text(x-43,Y(val)-7,f'{val:g}',12)
    for val in xticks:
        f.line([(X(val),y),(X(val),y+h)],color='#f0f1f3')
        f.text(X(val)-10,y+h+8,f'{val:g}',12)
    f.line([(x,y),(x,y+h),(x+w,y+h)],color='#8c96a3')
    f.text(x+w/2-40,y+h+30,xlabel,12)
    f.text(x,y-25,ylabel,12)
    return X,Y

f=Fig(1370,710)
f.text(32,20,'FS-001: two complete paths; one interrupted prefix',28,bold=True)
f.text(32,63,'Same original birth. Body-centre paths on identical 4 x 4 unit zooms; the arena is 20 x 20.',15)
f.text(32,88,'Circle = actual body radius 0.5; arrow = heading. Light mover trace = sampled centres, not an occupied region.',13)
for j,(name,d,r,col) in enumerate(zip(names,data,results,colors)):
    x=62+j*445;y=180;size=350
    f.text(x,y-74,name+(' | 90 s complete' if j<2 else ' | 10.25 s prefix'),20,col,True)
    X,Y=axis(f,x,y,size,size,(8.5,12.5),(6.5,10.5),(9,10,11,12),(7,8,9,10),'world x (units)','world y (units)')
    mr=d['mover_rectangle'];centres=(mr[:,0]+mr[:,1])/2
    lo=max(8.5,float(centres.min()));hi=min(12.5,float(centres.max()))
    if hi>=lo:f.line([(X(lo),Y(10)),(X(hi),Y(10))],color='#b4bcc6',width=2)
    x0,x1,y0,y1=mr[-1];x0=max(8.5,x0);x1=min(12.5,x1);y0=max(6.5,y0);y1=min(10.5,y1)
    if x1>x0 and y1>y0:f.rect(X(x0),Y(y1),X(x1)-X(x0),Y(y0)-Y(y1),fill='#e1e5ea',stroke='#9fa8b5')
    p=d['position'];idx=np.unique(np.r_[np.arange(0,len(p),5),len(p)-1])
    f.line([(X(px),Y(py)) for px,py in p[idx]],col,2.4)
    start=p[0];end=p[-1]
    f.circle(X(start[0]),Y(start[1]),3.5,fill='#111827')
    f.circle(X(end[0]),Y(end[1]),size*.5/4,stroke=col,width=1.2)
    f.circle(X(end[0]),Y(end[1]),3.5,fill=col,stroke=col)
    angle=float(d['angle'][-1]);tip=end+.4*np.array([math.cos(angle),math.sin(angle)])
    f.line([(X(end[0]),Y(end[1])),(X(tip[0]),Y(tip[1]))],col,2)
    for da in (-.5,.5):
        tail=tip-.1*np.array([math.cos(angle+da),math.sin(angle+da)])
        f.line([(X(tip[0]),Y(tip[1])),(X(tail[0]),Y(tail[1]))],col,2)
    if j==2:
        first=r['physical']['contact_event_rows'][0]['position']
        f.circle(X(first[0]),Y(first[1]),5,stroke='#ad2831',width=2)
        f.text(x,y+407,'Mover contact starts at 7.937 s.',13,'#ad2831')
    else:
        f.text(x,y+407,'No recorded contact or damage.',13)
    f.text(x,y+433,'Path %.3f | maximum excursion %.3f' % (r['kinematics']['path_length'],r['kinematics']['maximum_excursion']),13)
f.text(32,675,'Grey rectangle = last recorded mover pose (outside this zoom in CURRENT/M1). M2 ends before its first 11 s renewal.',13)
f.save('FS001_PATHS')

f=Fig(1330,1100)
f.text(32,20,'Timing and movement: only recorded intervals are drawn',26,bold=True)
for j,name in enumerate(names):
    f.line([(35+j*285,77),(70+j*285,77)],colors[j],3,dash=[None,[6,4],[2,3]][j])
    f.text(80+j*285,65,name+(' (90 s)' if j<2 else ' (10.25 s prefix)'),15,colors[j],True)
panels=[('Maximum distance from birth','units',(0,1.5),[0,.5,1,1.5],lambda d:d['excursion']),
    ('Spatial coverage growth','visited 0.25-unit cells',(0,20),[0,5,10,15,20],lambda d:d['coverage025']),
    ('Body-forward velocity','units/s',(-.22,.22),[-.2,-.1,0,.1,.2],lambda d:d['forward_velocity']),
    ('Unwrapped body-heading change','degrees',(-600,100),[-600,-400,-200,0,100],lambda d:np.degrees(d['angle']-d['angle'][0])),
    ('Common actuator command','(left + right) / 2',(-.3,.3),[-.3,-.15,0,.15,.3],lambda d:d['commands'].mean(axis=1)),
    ('Differential actuator command','(right - left) / 2',(-.3,.3),[-.3,-.15,0,.15,.3],lambda d:(d['commands'][:,1]-d['commands'][:,0])/2)]
for k,(title,label,ylim,yt,fn) in enumerate(panels):
    x=75+(k%2)*650;y=180+(k//2)*295;w=545;hh=185
    f.text(x,y-58,title,19,bold=True)
    X,Y=axis(f,x,y,w,hh,(0,90),ylim,[0,10,30,60,90],yt,'age (seconds)',label)
    for j,(d,col) in enumerate(zip(data,colors)):
        vals=fn(d);assert float(np.min(vals))>=ylim[0]-1e-9 and float(np.max(vals))<=ylim[1]+1e-9
        idx=np.unique(np.r_[np.arange(0,len(vals),10),len(vals)-1])
        if k==1:idx=np.unique(np.r_[idx,np.flatnonzero(np.diff(vals)!=0)+1])
        f.line([(X(d['time'][i]),Y(vals[i])) for i in idx],col,1.6,dash=[None,[6,4],[2,3]][j])
        f.circle(X(d['time'][-1]),Y(vals[-1]),3,fill=col,stroke=col)
f.text(32,1060,'Metrics use full native records. Display traces sampled at 0.1 s, retaining endpoints and coverage transitions. Six later cases were unstarted.',13)
f.save('FS001_TIMING')
print(json.dumps(dict(figures=['FS001_PATHS','FS001_TIMING'],render_seconds=time.perf_counter()-began,world_steps=0)))
