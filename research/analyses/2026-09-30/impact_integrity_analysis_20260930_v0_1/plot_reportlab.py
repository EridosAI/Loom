"""ReportLab vector charts of saved results; in-memory rasterization for PNG."""
import json,sys
from pathlib import Path
import numpy as np
import reportlab
from reportlab.graphics.shapes import Drawing,Line,Rect,Circle,String,PolyLine
from reportlab.graphics import renderSVG,renderPDF
from reportlab.lib.colors import HexColor,Color
import pypdfium2 as pdfium
HERE=Path(__file__).resolve().parent
BLUE=HexColor('#2864A5');ORANGE=HexColor('#BA591B');GREY=HexColor('#66717B');BLACK=HexColor('#20252A')
def load(name):return json.loads((HERE/name).read_bytes())
def text(d,x,y,s,size=11,colour=BLACK,anchor='start'):
    d.add(String(x,y,str(s),fontName='Helvetica',fontSize=size,fillColor=colour,textAnchor=anchor))
def line(d,points,colour=BLUE,width=1):d.add(PolyLine([float(v) for p in points for v in p],strokeColor=colour,strokeWidth=width,fillColor=None))
def point(d,x,y,colour=BLUE,r=3):d.add(Circle(x,y,r,fillColor=colour,strokeColor=None))
def canvas(w,h,title):
    d=Drawing(w,h);d.add(Rect(0,0,w,h,fillColor=HexColor('#FFFFFF'),strokeColor=None));text(d,30,h-30,title,18)
    text(d,30,15,'Sealed Founder Search records only. No alternative physical trajectory. Exact values are retained in companion tables.',9,GREY)
    return d
def axes(d,x,y,w,h,xlim,ylim,title,xlabel,ylabel,xticks=None):
    text(d,x,y+h+26,title,13);text(d,x,y+h+10,ylabel,10,GREY)
    line(d,[(x,y),(x,y+h)],GREY,.7);line(d,[(x,y),(x+w,y)],GREY,.7)
    X=lambda v:x+(v-xlim[0])/(xlim[1]-xlim[0])*w
    Y=lambda v:y+(v-ylim[0])/(ylim[1]-ylim[0])*h
    for v in np.linspace(*ylim,5):
        line(d,[(x,Y(v)),(x+w,Y(v))],HexColor('#E1E5E8'),.4);text(d,x-7,Y(v)-3,f'{v:.3g}',9,GREY,'end')
    for v in (np.linspace(*xlim,5) if xticks is None else xticks):text(d,X(v),y-15,f'{v:g}',9,GREY,'middle')
    text(d,x+w/2,y-33,xlabel,10,GREY,'middle')
    return X,Y
def save(d,stem):
    renderSVG.drawToFile(d,str(HERE/(stem+'.svg')))
    # This creates no PDF document artifact; the vector drawing is rasterized in memory.
    doc=pdfium.PdfDocument(renderPDF.drawToString(d));page=doc[0];page.render(scale=2).to_pil().save(HERE/(stem+'.png'))
    page.close();doc.close()
episodes=load('BEHAVIORAL_EPISODES_ENRICHED.json');probes=load('PASSIVE_LEARNED_I_OMISSIONS.json')
d=canvas(980,920,'Later contacts can soften, worsen, or remain mixed')
for r,name in enumerate(('FS-002','FS-015','FS-044')):
    ep=[z for z in episodes if z['life_id']==name]
    for col,(key,label) in enumerate((('peak_instant_closing_velocity','Peak closing speed at impact (world units/s)'),('damage','Integrity damage per episode'))):
        x=70+col*480;y=650-r*280;w=365;h=165;values=[z[key] for z in ep]
        X,Y=axes(d,x,y,w,h,(0,len(ep)+1),(0,max(values)*1.2),name+' / '+ep[0]['collider'],'Episode number; onset ages shown below',label,range(1,len(ep)+1))
        for i,z in enumerate(ep,1):
            width=min(30,w/(len(ep)+1)*.65);d.add(Rect(X(i)-width/2,y,width,Y(z[key])-y,fillColor=ORANGE if i==1 else BLUE,strokeColor=None))
            text(d,X(i),y-49,f'{i}: {z["onset"]:.1f}s',8,GREY,'middle')
save(d,'CONTACT_SEVERITY')

d=canvas(1000,690,'Clearance growth and local learned-I influence are separate observations')
for r,name in enumerate(('FS-010','FS-017')):
    blocks=load(name+'_EXPOSURE_BLOCKS.json');p=[z for z in probes if z['life_id']==name and z['kind']=='fixed_ageblock_closest']
    y=405-r*300;x=70
    X,Y=axes(d,x,y,365,170,(0,450),(0,max(z['minimum_clearance'] for z in blocks)*1.2),name+' / later clearance','Recorded age (s)','Minimum surface clearance (world units)')
    pairs=[(X(z['closest_time']),Y(z['minimum_clearance'])) for z in blocks];line(d,pairs)
    for a,b in pairs:point(d,a,b)
    values=[z['learned_I_into_force_delta_mean']*1e6 for z in p];lim=max(abs(np.array(values)).max()*1.2,1e-4)
    X,Y=axes(d,560,y,365,170,(0,450),(-lim,lim),name+' / immediate learned-I effect','Recorded age (s)','Normal minus omitted approach force (x 10^-6)')
    line(d,[(X(0),Y(0)),(X(450),Y(0))],BLACK,.8)
    for z,v in zip(p,values):point(d,X(z['last_native']*.01),Y(v),BLUE if v<0 else ORANGE)
    text(d,560,y-52,'Below zero: less into surface. Above zero: more into surface.',10,GREY)
save(d,'CLEARANCE_AND_LOCAL_I')

d=canvas(1000,980,'Recorded body-centre paths and contact episodes')
text(d,30,929,'Paths are sampled for colour display only; native records remain complete. No trajectory was resimulated.',10,GREY)
for panel,name in enumerate(('FS-002','FS-010','FS-015','FS-017')):
    data=np.load(HERE/(name+'_RECORDED_NATIVE.npz'));pos=data['position'];times=data['time'][:,0]
    ep=[z for z in episodes if z['life_id']==name];first=ep[0];j=first['first_native']-1
    x=65+(panel%2)*495;y=525-(panel//2)*440;w=355;h=310
    xmin,xmax=pos[:,0].min()-.55,pos[:,0].max()+.55;ymin,ymax=pos[:,1].min()-.55,pos[:,1].max()+.55
    unit=max((xmax-xmin)/w,(ymax-ymin)/h);xmax=xmin+w*unit;ymax=ymin+h*unit
    X=lambda v:x+(v-xmin)/unit;Y=lambda v:y+(v-ymin)/unit
    text(d,x,y+h+25,name+' / actual path',14)
    if first['collider']=='wall-2' and ymin<=0<=ymax:line(d,[(x,Y(0)),(x+w,Y(0))],GREY,3)
    if first['collider']=='repair-0':
        xa=max(xmin,0);xb=min(xmax,.25);ya=max(ymin,8);yb=min(ymax,12)
        if xb>xa and yb>ya:d.add(Rect(X(xa),Y(ya),(xb-xa)/unit,(yb-ya)/unit,fillColor=HexColor('#DDDDDD'),strokeColor=GREY))
    if first['collider']=='mover':
        rect=data['mover_rectangle'][j];xa=max(xmin,rect[0]);xb=min(xmax,rect[1]);ya=max(ymin,rect[2]);yb=min(ymax,rect[3])
        if xb>xa and yb>ya:d.add(Rect(X(xa),Y(ya),(xb-xa)/unit,(yb-ya)/unit,fillColor=HexColor('#E4E4E4'),strokeColor=GREY))
    ids=np.unique(np.r_[np.arange(0,len(pos),10),len(pos)-1]).astype(int)
    for a,b in zip(ids[:-1],ids[1:]):
        f=times[a]/431;colour=Color(.2+.6*f,.3+.3*f,.75-.6*f)
        line(d,[(X(pos[a,0]),Y(pos[a,1])),(X(pos[b,0]),Y(pos[b,1]))],colour,.7)
    point(d,X(pos[0,0]),Y(pos[0,1]),BLUE,4);point(d,X(pos[-1,0]),Y(pos[-1,1]),BLACK,4)
    text(d,X(pos[0,0])+5,Y(pos[0,1])+5,'start',9,BLUE);text(d,X(pos[-1,0])+5,Y(pos[-1,1])-11,'end',9,BLACK)
    d.add(Circle(X(pos[j,0]),Y(pos[j,1]),.5/unit,fillColor=None,strokeColor=ORANGE,strokeWidth=.8,strokeDashArray=[3,2]))
    ordered=sorted(ep,key=lambda z:pos[z['first_native']-1,0])
    for order,z in enumerate(ordered):
        v=pos[z['first_native']-1];point(d,X(v[0]),Y(v[1]),ORANGE,3)
        if len(ep)>1:
            lx=x+25+order*(w-50)/(len(ep)-1);ly=y+35
            line(d,[(X(v[0]),Y(v[1])-3),(lx,ly+12)],ORANGE,.4);text(d,lx,ly,str(z['episode']),11,ORANGE,'middle')
        else:text(d,X(v[0])+4,Y(v[1])+5,str(z['episode']),10,ORANGE)
    text(d,x,y-20,'Orange numbers: episodes. Dashed circle: body at first contact.',9,GREY)
    text(d,x,y-35,'Blue-to-orange path: early-to-late. Grey mover: first-contact pose only.',9,GREY)
    text(d,x,y-50,f'x = {xmin:.2f} to {xmax:.2f}; y = {ymin:.2f} to {ymax:.2f} world units; equal scale.',9,GREY)
save(d,'RECORDED_CANDIDATE_PATHS')
(HERE/'PLOT_RUNTIME.json').write_text(json.dumps(dict(python=sys.version,executable=sys.executable,numpy=np.__version__,reportlab=reportlab.Version,
    scientific_code_imported=False,inputs='derived JSON and NPZ only',world_steps=0,
    note='Matplotlib unavailable in bundled runtime; existing Conda copy lacks pyparsing. No package was installed; ReportLab and bundled PDFium rasterized figures.')),encoding='utf-8')
print('Saved three SVG/PNG passive figures using installed ReportLab.')
