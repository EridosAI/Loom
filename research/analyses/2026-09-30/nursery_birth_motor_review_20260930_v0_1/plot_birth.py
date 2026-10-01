"""Render preserved-birth/static-analysis figures only; no Loom imports."""
from pathlib import Path
import json,math,csv
import numpy as np
from reportlab.graphics.shapes import Drawing,Rect,Circle,String,PolyLine,Polygon
from reportlab.graphics import renderSVG,renderPDF
from reportlab.lib.colors import HexColor,Color
import pypdfium2 as pdfium
O=Path(__file__).resolve().parent
rows=json.loads((O/'BIRTH_INITIAL_DETAILS.json').read_text());r=json.loads((O/'BIRTH_AUDIT_RESULTS.json').read_text())
c=json.loads((O.parent/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology/configuration.json').read_text())
INK=HexColor('#21313d');GRAY=HexColor('#677984');BLUE=HexColor('#196c9e');ORANGE=HexColor('#b65324');PURPLE=HexColor('#7961a8');PALE=HexColor('#e6edf2')
def text(d,x,y,s,size=11,color=INK,anchor='start'):d.add(String(x,y,str(s),fontName='Helvetica',fontSize=size,fillColor=color,textAnchor=anchor))
def line(d,pts,color=GRAY,width=1,dash=None):d.add(PolyLine([v for p in pts for v in p],strokeColor=color,strokeWidth=width,strokeDashArray=dash,fillColor=None))
def axes(d,x,y,w,h,xlim,ylim,title,xlabel,ylabel):
    text(d,x,y+h+38,title,15);text(d,x,y+h+20,ylabel,11,GRAY)
    X=lambda v:x+(v-xlim[0])/(xlim[1]-xlim[0])*w;Y=lambda v:y+(v-ylim[0])/(ylim[1]-ylim[0])*h
    for v in np.linspace(*ylim,5):line(d,[(x,Y(v)),(x+w,Y(v))],PALE,.7);text(d,x-7,Y(v)-4,f'{v:.3g}',10,GRAY,'end')
    for v in np.linspace(*xlim,5):text(d,X(v),y-18,f'{v:g}',10,GRAY,'middle')
    line(d,[(x,y+h),(x,y),(x+w,y)],GRAY,.8);text(d,x+w/2,y-40,xlabel,11,GRAY,'middle');return X,Y
def mark(d,x,y,row,size=3):
    color=ORANGE if row['later_damage'] else BLUE
    if not row['complete']:d.add(Polygon([x,y+5,x+5,y,x,y-5,x-5,y],strokeColor=INK,fillColor=None,strokeWidth=1.5))
    else:d.add(Circle(x,y,size,fillColor=color,strokeColor=None))
    if row['later_source_contact']:d.add(Circle(x,y,size+4,strokeColor=INK,fillColor=None,strokeWidth=1.5))
def save(d,name):
    renderSVG.drawToFile(d,str(O/(name+'.svg')))
    doc=pdfium.PdfDocument(renderPDF.drawToString(d));page=doc[0];page.render(scale=1.65).to_pil().save(O/(name+'.png'));page.close();doc.close()

d=Drawing(1180,860);d.add(Rect(0,0,1180,860,fillColor=HexColor('#ffffff'),strokeColor=None))
text(d,38,822,'Births cover the arena broadly; individual motion stayed local',23)
text(d,38,796,'FS-001–FS-060 original time-zero states. Arrows show birth heading. No new births or trajectories.',12,GRAY)
X=lambda v:70+28*v;Y=lambda v:120+28*v
d.add(Rect(X(0),Y(0),560,560,fillColor=HexColor('#edf1f4'),strokeColor=INK,strokeWidth=1.5))
# Fixed static admissible centre support; phase-dependent mover subtraction is not shown as a permanent exclusion.
d.add(Rect(X(.75),Y(.75),18.5*28,18.5*28,fillColor=HexColor('#ffffff'),strokeColor=None))
for x,y in c['source_positions']:
    d.add(Circle(X(x),Y(y),1.25*28,fillColor=HexColor('#edf1f4'),strokeColor=None))
    d.add(Circle(X(x),Y(y),.5*28,fillColor=HexColor('#e8c56a'),strokeColor=HexColor('#8b7029')))
for x0,x1,y0,y1 in c['repair_rectangles']:
    d.add(Rect(X(x0),Y(y0),(x1-x0)*28,(y1-y0)*28,fillColor=PURPLE,strokeColor=None))
# Draw exact safe mask restrictions from static geometry around restorative surfaces as grid rectangles.
g=np.load(O/'BIRTH_SAFE_SUPPORT_GRID.npz');a=g['axis'];static=g['static_safe'];step=.05
for iy,y in enumerate(a):
    bad=(~static[iy]) & (a>=.75)&(a<=19.25)
    if not .75<=y<=19.25:continue
    start=None
    for ix,val in enumerate(np.r_[bad,False]):
        if val and start is None:start=ix
        if not val and start is not None:
            d.add(Rect(X(a[start]-.025),Y(y-.025),(ix-start)*step*28,step*28,fillColor=HexColor('#edf1f4'),strokeColor=None));start=None
# Restore physical fixture outlines above exclusion tint.
for x,y in c['source_positions']:d.add(Circle(X(x),Y(y),.5*28,fillColor=HexColor('#e8c56a'),strokeColor=HexColor('#8b7029')))
d.add(Rect(X(5),Y(9.5),10*28,28,fillColor=None,strokeColor=ORANGE,strokeDashArray=[5,4],strokeWidth=1.3))
line(d,[(X(6),Y(10)),(X(14),Y(10))],ORANGE,1,[2,4])
for v in (0,5,10,15,20):
    text(d,X(v),Y(0)-19,v,11,GRAY,'middle');text(d,X(0)-12,Y(v)-4,v,11,GRAY,'end')
for row in rows:
    x,y=row['x'],row['y'];th=row['heading_rad'];tip=(X(x+.65*math.cos(th)),Y(y+.65*math.sin(th)))
    line(d,[(X(x),Y(y)),tip],GRAY,.65);mark(d,X(x),Y(y),row)
    if row['life_id'] in ('FS-034','FS-060'):text(d,X(x)+7,Y(y)+7,row['life_id'],10)
text(d,350,74,'x / y in world units; full arena 20 x 20',12,GRAY,'middle')
text(d,70,709,'Birth positions and headings',16)
for j,s in enumerate(['Blue dots: complete, no recorded damage','Orange dots: complete, recorded damage','Black ring: FS-034 source contact','Open diamond: FS-060 censored prefix','Gold: physical energy sources','Purple: physical repair surfaces','Grey: static birth-clearance exclusion','Dashed band: mover physical sweep','Sweep is NOT permanently excluded']):text(d,700,704-j*24,s,12,ORANGE if j==7 else INK)
text(d,700,466,'Coverage checks',17)
for j,s in enumerate(['16 / 16 coarse cells occupied','22 / 25 finer cells; expectation 22.11','55 one-unit cells; expectation 54.77','62 pairs within 2 units; expectation 61.03','44.15% of safe-support mass within 1 unit','of a birth; expectation 43.37%']):text(d,700,437-j*25,s,12)
text(d,700,254,'Interpretation',17)
for j,s in enumerate(['Broad coverage, with ordinary finite-sample gaps.','These checks do not show excess clustering.','They do not prove the generator is ideal uniform.','Each birth is valid at its OWN mover phase.','Exact phases and positions are in the CSV.']):text(d,700,226-j*23,s,12)
text(d,38,35,'Expected quantities: static safe-support quadrature conditioned on the 60 preserved phases. No synthetic population.',11,GRAY)
save(d,'BIRTH_ARENA_MAP')

d=Drawing(1100,950);d.add(Rect(0,0,1100,950,fillColor=HexColor('#ffffff'),strokeColor=None))
text(d,40,912,'Birth geography and later proximity: associations, not causes',22)
text(d,40,885,'Filled dots: 59 complete lives; open diamond: FS-060 prefix, excluded from reported correlations.',12,GRAY)
X,Y=axes(d,75,570,400,230,(0,5),(0,5),'Starting proximity largely persists','Birth nearest-source body gap','Lifetime minimum source body gap')
line(d,[(X(0),Y(0)),(X(5),Y(5))],GRAY,.8,[3,3])
for row in rows:mark(d,X(row['nearest_source_body_gap']),Y(row['later_source_min_gap']),row)
text(d,92,777,'Spearman rho = 0.973 (59 lives)',11)
X,Y=axes(d,655,570,380,230,(0,5),(.44,.64),'Chemical level varies with geography','Birth nearest-source body gap','Mean of four stored chemical receptors')
for row in rows:mark(d,X(row['nearest_source_body_gap']),Y(row['chem_overall_mean']),row)
X,Y=axes(d,75,145,400,230,(0,360),(0,14),'Orientation and phase span the circle','Degrees, eight bins of width 45','Birth count')
for k,key in enumerate(('heading_rad','mover_phase_rad')):
    for i,n in enumerate(r['circular'][key]['eight_equal_angle_counts']):
        x=X(i*45+4+k*19);d.add(Rect(x,Y(0),17/360*400,Y(n)-Y(0),fillColor=BLUE if k==0 else ORANGE,strokeColor=None))
text(d,90,360,'Blue: body heading; orange: mover phase',11)
X,Y=axes(d,655,145,380,230,(0,5),(0,1.3),'Excursion is weakly related to source gap','Birth nearest-source body gap','Lifetime maximum excursion from birth')
for row in rows:mark(d,X(row['nearest_source_body_gap']),Y(row['later_max_excursion']),row)
text(d,670,351,'Spearman rho = -0.024 (59 lives)',11)
text(d,40,55,'Colour in scatter plots: orange = damage, blue = no damage. Ring = FS-034, the sole source-contact case.',11,GRAY)
text(d,40,32,'Stored chemistry is not a source label. No association was used to choose births, motor parameters or nursery geometry.',11,GRAY)
save(d,'BIRTH_GEOGRAPHY_ASSOCIATIONS')
print('Rendered two static birth-review figures (SVG + PNG).')
