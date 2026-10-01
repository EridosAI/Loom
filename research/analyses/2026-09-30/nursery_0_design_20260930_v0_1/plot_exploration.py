"""Render saved passive results only, with existing ReportLab/PDFium libraries."""
from pathlib import Path
import json,csv,sys
import numpy as np
import reportlab,pypdfium2 as pdfium
from reportlab.graphics.shapes import Drawing,Rect,Line,Circle,String,PolyLine,Polygon
from reportlab.graphics import renderSVG,renderPDF
from reportlab.lib.colors import HexColor
OUT=Path(__file__).resolve().parent
A=json.loads((OUT/'EXPLORATION_AUDIT_RESULTS.json').read_text())
BLUE=HexColor('#2465a6');ORANGE=HexColor('#ad561d');INK=HexColor('#22313d');GRAY=HexColor('#78838c');LIGHT=HexColor('#dee7ef')
def text(d,x,y,s,size=11,color=INK,anchor='start'):d.add(String(x,y,str(s),fontName='Helvetica',fontSize=size,fillColor=color,textAnchor=anchor))
def line(d,points,color=BLUE,width=1,dash=None):
    d.add(PolyLine([float(v) for p in points for v in p],fillColor=None,strokeColor=color,strokeWidth=width,strokeDashArray=dash))
def axes(d,x,y,w,h,xlim,ylim,title,xlabel,ylabel):
    text(d,x,y+h+35,title,14);text(d,x,y+h+17,ylabel,11,GRAY)
    X=lambda v:x+(v-xlim[0])/(xlim[1]-xlim[0])*w;Y=lambda v:y+(v-ylim[0])/(ylim[1]-ylim[0])*h
    for v in np.linspace(*ylim,5):
        line(d,[(x,Y(v)),(x+w,Y(v))],LIGHT,.6);text(d,x-8,Y(v)-4,f'{v:.3g}',10,GRAY,'end')
    for v in np.linspace(*xlim,5):text(d,X(v),y-18,f'{v:g}',10,GRAY,'middle')
    line(d,[(x,y+h),(x,y),(x+w,y)],GRAY,.7);text(d,x+w/2,y-40,xlabel,11,GRAY,'middle')
    return X,Y
def save(d,name):
    renderSVG.drawToFile(d,str(OUT/(name+'.svg')))
    doc=pdfium.PdfDocument(renderPDF.drawToString(d));p=doc[0];p.render(scale=1.7).to_pil().save(OUT/(name+'.png'));p.close();doc.close()
d=Drawing(1100,1190);d.add(Rect(0,0,1100,1190,fillColor=HexColor('#ffffff'),strokeColor=None))
text(d,42,1157,'Movement accumulates while exploration remains local',22)
text(d,42,1130,'59 complete preserved lives. No new trajectories. FS-060 stays a separately reported 124 s prefix.',12,GRAY)
ages=sorted(float(x) for x in A['age_ensemble']);age=lambda t:A['age_ensemble'][str(int(t))]
X,Y=axes(d,80,840,420,215,(0,420),(0,15),'A. Distance travelled versus spatial reach','Recorded age (s)','World units; ensemble means')
line(d,[(X(t),Y(age(t)['path']['mean'])) for t in ages],BLUE,2)
line(d,[(X(t),Y(age(t)['max_excursion']['mean'])) for t in ages],ORANGE,2,dash=[4,3])
text(d,105,1007,'Path: 13.54 at 420 s',12,BLUE);text(d,105,981,'Maximum excursion: 0.591',12,ORANGE)
X,Y=axes(d,650,840,390,215,(0,420),(0,12),'B. New occupied space accumulates slowly','Recorded age (s)','Distinct 0.25-unit bins; mean and full range')
lo=[(X(t),Y(age(t)['coverage025']['minimum'])) for t in ages];hi=[(X(t),Y(age(t)['coverage025']['maximum'])) for t in ages]
d.add(Polygon([z for p in lo+hi[::-1] for z in p],fillColor=LIGHT,strokeColor=None))
line(d,[(X(t),Y(age(t)['coverage025']['mean'])) for t in ages],BLUE,2)
text(d,667,1034,'Range is across lives, not a confidence interval',10,GRAY)
X,Y=axes(d,80,470,420,235,(0,420),(0,.24),'C. Birth-relative MSD grows little late in life','Recorded age (s)','Squared world units')
for key,color,dash in [('mean',BLUE,None),('median',ORANGE,[4,3])]:line(d,[(X(t),Y(age(t)['birth_msd'][key])) for t in ages],color,2,dash)
text(d,105,687,'Mean',11,BLUE);text(d,182,687,'Median (dashed)',11,ORANGE)
curves=[json.loads((OUT/f'FS-{i:03d}_EXPLORATION_DETAILS.json').read_text())['correlations'] for i in range(1,60)]
lags=[r['lag_s'] for r in curves[0] if r['lag_s']<=12]
X,Y=axes(d,650,470,390,235,(0,12),(-1,1),'D. Heading persists; movement reverses','Lag (s)','Mean cosine / directional correlation')
for key,color,dash in [('heading_acf',ORANGE,[5,3]),('direction_acf',BLUE,None)]:
    vals=[np.mean([next(r[key] for r in cv if r['lag_s']==t) for cv in curves]) for t in lags]
    line(d,[(X(t),Y(v)) for t,v in zip(lags,vals)],color,2,dash)
text(d,650,408,'Solid: movement direction / dashed: body heading',11,GRAY)
X,Y=axes(d,80,103,420,235,(0,40),(-.14,.14),'E. First roster member: forward and backward','Recorded age (s), FS-001','Saved body-forward velocity (world units/s)')
p=np.load(OUT/'FS-001_PASSIVE_KINEMATICS.npz');sel=p['time']<=40
line(d,[(X(t),Y(v)) for t,v in zip(p['time'][sel],p['forward'][sel])],BLUE,1.5)
line(d,[(X(0),Y(0)),(X(40),Y(0))],GRAY,.9)
X,Y=axes(d,707.5,103,235,235,(-1.3,1.3),(-1.3,1.3),'F. Recorded centres relative to birth','x offset (world units)','y offset (world units); all 59 complete lives')
damaged={'FS-002','FS-010','FS-015','FS-017','FS-032','FS-033','FS-034','FS-038','FS-044'}
for i in range(1,60):
    name=f'FS-{i:03d}';q=np.load(OUT/(name+'_PASSIVE_KINEMATICS.npz'));pos=q['position']-q['birth'];pos=pos[::3]
    line(d,[(X(x),Y(y)) for x,y in pos],ORANGE if name in damaged else HexColor('#aebbc5'),.45)
d.add(Circle(X(0),Y(0),2.5,fillColor=INK,strokeColor=None))
text(d,650,40,'Orange: damaged / grey: no positive contact',10,GRAY)
text(d,42,22,'Sources: EXPLORATION_* tables. Point occupancy and sampled display paths are not swept-body areas. No causal motor intervention.',10,GRAY)
save(d,'EXPLORATION_DYNAMICS')

# Re-render the exact provisional layout in a portable raster, without changing coordinates.
c=json.loads((OUT/'DESIGN_ARITHMETIC.json').read_text())['proposal_geometry']
d=Drawing(920,730);d.add(Rect(0,0,920,730,fillColor=HexColor('#ffffff'),strokeColor=None))
text(d,35,695,'Provisional Nursery-0 geometry retained for review',20)
text(d,35,670,'Geometry is not locked. No birth, motor change or simulation. A/B/C share this layout.',12,GRAY)
X=lambda x:65+38*x;Y=lambda y:70+38*y
d.add(Rect(X(0),Y(0),14*38,14*38,fillColor=None,strokeColor=INK,strokeWidth=2))
d.add(Rect(X(2),Y(6.5),10*38,38,fillColor=HexColor('#ffe4d6'),strokeColor=ORANGE,strokeDashArray=[5,3]))
d.add(Rect(X(6),Y(6.5),2*38,38,fillColor=HexColor('#e9b399'),strokeColor=ORANGE))
for x0,x1,y0,y1 in c['repair_rectangles']:d.add(Rect(X(x0),Y(y0),(x1-x0)*38,(y1-y0)*38,fillColor=HexColor('#7255a2'),strokeColor=None))
for k,(x,y) in enumerate(c['source_positions']):
    d.add(Circle(X(x),Y(y),.5*38,fillColor=HexColor('#e6bd47'),strokeColor=HexColor('#725b20')));text(d,X(x),Y(y)-4,k,11,INK,'middle')
for y in (5.75,8.25):line(d,[(X(1),Y(y)),(X(13),Y(y))],BLUE,1.5,[4,3])
for x in (1,13):line(d,[(X(x),Y(5.75)),(X(x),Y(8.25))],BLUE,1.5,[4,3])
for t in range(0,15,2):text(d,X(t),Y(0)-20,t,11,GRAY,'middle');text(d,X(0)-15,Y(t)-4,t,11,GRAY,'end')
for i,s in enumerate(['14 x 14 world; body diameter 1','12 sources, radius 0.5','3 wall repair strips, 4 x 0.25','Mover: 2 x 1, amplitude 4','Period: 30 s (unchanged)','Shaded band: mover sweep','Block: illustrative midpoint','Blue: available bypass examples','No route is supplied to P','Numbering is observer-only']):text(d,625,596-i*35,s,12)
d.add(Circle(653,183,19,strokeColor=INK,fillColor=None));text(d,685,179,'Body size only',12)
text(d,65,25,'Static geometry drawing. Swept space is not permanently occupied; actual phase governs crossing availability.',11,GRAY)
save(d,'NURSERY_0_LAYOUT_REVIEW')
(OUT/'PLOT_RUNTIME.json').write_text(json.dumps({'python':sys.version,'reportlab':reportlab.Version,'pypdfium2':str(pdfium.PYPDFIUM_INFO),'numpy':np.__version__,'matplotlib_available':False,'new_installs':False,'inputs':'derived saved summaries and static geometry only','world_steps':0,'P_steps':0},indent=2)+'\n')
print('Two SVG/PNG figures rendered from saved data.')
