"""Static figures from saved analysis arrays only."""
from pathlib import Path
import ast,json,csv,math
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from reportlab.graphics.shapes import Drawing,Line,Rect,Circle,PolyLine,String
from reportlab.graphics import renderSVG
from reportlab.lib.colors import HexColor
PACKAGE=Path(__file__).resolve().parent;ROOT=PACKAGE.parent;OUT=PACKAGE/'figures';OUT.mkdir(exist_ok=True)
prior=ROOT/'m1_long_development_full_analysis_20261001_v0_1'
helper=ROOT/'m1_resurrection_results_20260930_v0_1/passive_reference_sources/historical_plot_helpers.py'
nodes=[n for n in ast.parse(helper.read_text()).body if isinstance(n,ast.ClassDef) and n.name=='Fig'];exec(compile(ast.Module(body=nodes,type_ignores=[]),str(helper),'exec'))
COLORS=['#2166ac','#b35806','#4d9221','#762a83','#c51b7d','#008b8b','#68523b']
def roll(t,y,square=False):
    lo=np.searchsorted(t,t-60,side='right');cs=np.r_[0,np.cumsum(y*y if square else y)];v=(cs[1:]-cs[lo])/(np.arange(len(t))+1-lo);return np.sqrt(np.maximum(v,0)) if square else v
def thin(t,y,bins=700):
    mask=np.isfinite(y);t=t[mask];y=y[mask]
    if len(t)<bins*3:return t,y
    ids=np.floor((t-t[0])/(t[-1]-t[0]+1e-15)*bins).astype(int);starts=np.r_[0,np.flatnonzero(np.diff(ids))+1];ends=np.r_[starts[1:],len(t)];chosen=[]
    for a,b in zip(starts,ends):chosen.extend([a,a+int(np.argmin(y[a:b])),a+int(np.argmax(y[a:b])),b-1])
    chosen=np.unique(chosen);return t[chosen],y[chosen]
def axis(f,x,y,w,h,xmax,ymin,ymax,title):
    if ymax<=ymin:ymax=ymin+1
    largest=max(abs(ymin),abs(ymax));scale=10**math.floor(math.log10(largest)) if largest and (largest<.01 or largest>1e3) else 1
    X=lambda v:x+w*v/xmax;Y=lambda v:y+h-h*(v-ymin)/(ymax-ymin)
    f.text(x,y-32,title+(f' [x {scale:g}]' if scale!=1 else ''),15,bold=True)
    for v in np.linspace(ymin,ymax,5):f.line([(x,Y(v)),(x+w,Y(v))],'#e6ebef',.7);f.text(x-67,Y(v)-8,f'{v/scale:.3g}',11)
    for v in np.linspace(0,xmax,5):f.line([(X(v),y),(X(v),y+h)],'#eef1f4',.7);f.text(X(v)-14,y+h+8,f'{v:.0f}',11)
    f.line([(x,y),(x,y+h),(x+w,y+h)],'#8e99a6',.9);return X,Y
def support(f,X,y,h,life):
    rec=json.loads((prior/'cache'/(life+'.json')).read_bytes())
    for r in rec['interventions']:f.line([(X(r['time']),y),(X(r['time']),y+h)],'#e4b5b5',.6)
def panels(life):
    d=np.load(PACKAGE/'series'/(life+'_FUNCTIONAL.npz'));t=d['age'];end=json.loads((prior/'cache'/(life+'.json')).read_bytes())['curve_cutoff'];status='4500 s complete' if end==4500 else ('600 s pilot' if end==600 else f'censored, last full checkpoint {end:.6f} s')
    metrics=[('E current-only command effect','E_command_effect'),('I current-only command effect','I_command_effect'),('E command effect / M1 input RMS','E_over_M1'),('I command effect / M1 input RMS','I_over_M1'),('Associative return ||q||','q_norm'),('Mean H use','H_use_mean'),('Direct feedback RMS','direct_feedback_RMS'),('Total regulator current RMS','regulator_current_RMS'),('Actual paired command RMS','command_RMS'),('Mean attenuation (left/right average)','attenuation_mean')]
    f=Fig(1680,1860);f.text(30,16,life+' | functional development',27,bold=True);f.text(30,56,'NON-CANONICAL RESURRECTION SANDBOX | '+status,15)
    f.text(30,84,'Thin line: stored-wave operands / exact detached receiver effect. Dark: trailing 60 s RMS; use/attenuation: mean.',13)
    f.text(30,106,'Ratio panels already use trailing 60 s RMS ratios. Red lines: external support. No alternate history or world evolution.',13)
    for j,(title,key) in enumerate(metrics):
        x=108+(j%2)*825;y=192+(j//2)*326;v=d[key];top=max(float(np.nanmax(v))*1.04,1e-15);X,Y=axis(f,x,y,680,228,end,0,top,title);support(f,X,y,228,life)
        tx,vy=thin(t,v);f.line([(X(a),Y(b)) for a,b in zip(tx,vy)],'#aebcca',.65)
        sm=v if key.endswith('over_M1') else roll(t,v,square=key not in ('H_use_mean','attenuation_mean'));tx,vy=thin(t,sm);f.line([(X(a),Y(b)) for a,b in zip(tx,vy)],COLORS[j%7],1.8)
    f.text(570,1816,'Actual developmental age (seconds)',15);f.text(30,1843,'Command effects apply to one recorded native operation. Incoming current effects and complete receiver omissions are separately exported.',11);f.save(life+'_FUNCTIONAL_DEVELOPMENT')
    f=Fig(1680,1280);f.text(30,16,life+' | stored structure to expression',26,bold=True);f.text(30,57,status+' | coupling ratios are descriptive, not skill scores',15)
    keys=[('Command effect / E-bank norm','command_per_theta_E'),('Command effect / I-bank norm','command_per_theta_I'),('q norm / H norm','q_per_H'),('Mean H use / H norm','use_per_H'),('Associative motor command effect','associative_motor_command_effect'),('M1 same-receiver command effect','M1_command_effect')]
    for j,(title,key) in enumerate(keys):
        x=108+(j%2)*825;y=165+(j//2)*340;v=d[key];finite=v[np.isfinite(v)];top=max(float(finite.max())*1.04,1e-15) if len(finite) else 1;X,Y=axis(f,x,y,680,235,end,0,top,title);support(f,X,y,235,life);tx,vy=thin(t,v);f.line([(X(a),Y(b)) for a,b in zip(tx,vy)],'#aebcca',.65)
        valid=np.isfinite(v);tx=t[valid];vv=v[valid];sm=roll(tx,vv);tx,vy=thin(tx,sm);f.line([(X(a),Y(b)) for a,b in zip(tx,vy)],COLORS[j],1.8)
        if not len(finite):f.text(x+65,y+95,'Undefined: bank norm is zero throughout.',16,'#68523b')
    f.text(560,1210,'Actual developmental age (seconds)',15);f.text(30,1245,'Zero-norm ratios are undefined, not zero. Mean trend omits those undefined samples. Source equations and exact semantics in the report.',12);f.save(life+'_COUPLING')
def overlays():
    for key,title in [('E_over_M1','E command effect / M1 input RMS'),('I_over_M1','I command effect / M1 input RMS'),('q_norm','Associative return ||q||'),('H_use_mean','Mean H use')]:
        arrays=[]
        for n in range(1,9):
            d=np.load(PACKAGE/'series'/f'RS-M1-{n:03d}_FUNCTIONAL.npz');t=d['age'];y=d[key];sm=y if key.endswith('over_M1') else roll(t,y,square=key=='q_norm');arrays.append((t,y,sm))
        top=max(v[1].max() for v in arrays)*1.05;f=Fig(1480,930);f.text(30,18,title,27,bold=True);f.text(30,58,'Fixed seven complete lives. Censored 008 is separate; pilots are not pooled. Ratios use 60 s RMS windows.',14)
        for n,col in enumerate(COLORS):f.text(60+n*201,96,f'{n+1:03d}',15,col,True)
        X,Y=axis(f,110,185,1280,450,4500,0,top,'Raw trace and 60 s trend')
        for n,(t,y,sm) in enumerate(arrays[:7]):
            tx,vy=thin(t,y);f.line([(X(a),Y(b)) for a,b in zip(tx,vy)],'#dae0e5',.4);tx,vy=thin(t,sm);f.line([(X(a),Y(b)) for a,b in zip(tx,vy)],COLORS[n],1.8)
        X,Y=axis(f,110,755,1280,110,4500,0,top,'RS-M1-008 — censored; same axes');t,y,sm=arrays[7];tx,vy=thin(t,sm);f.line([(X(a),Y(b)) for a,b in zip(tx,vy)],'#222222',1.8);f.circle(X(t[-1]),Y(sm[-1]),3,fill='#ab3434');f.text(480,901,'Actual developmental age (seconds)',14);f.save('POPULATION_'+key)
def behavioral():
    rows=list(csv.DictReader((PACKAGE/'tables/FIXED_SEVEN_BAND_TOTALS.csv').open()));f=Fig(1600,1160);f.text(30,20,'Behavior across age | fixed seven complete lives',27,bold=True);f.text(30,61,'Observed rates with their opportunity denominators. No aggregate developmental score.',15)
    metrics=[('Damage / path','damage_per_path'),('Collision given hazard approach','collision_given_approach'),('Productive source bouts / path','productive_bouts_per_path'),('True source revisits / path','true_revisits_per_path'),('Mean source contact per bout (s)','mean_bout_dwell'),('Source energy / expenditure','environment_fraction_of_expense')]
    for j,(title,key) in enumerate(metrics):
        x=100+(j%2)*790;y=160+(j//2)*315;v=np.array([float(r[key]) for r in rows]);X,Y=axis(f,x,y,660,210,4500,0,max(v.max()*1.12,1e-10),title)
        for k,r in enumerate(rows):lo=float(r['start']);hi=float(r['end']);f.rect(X(lo)+3,Y(v[k]),X(hi)-X(lo)-6,Y(0)-Y(v[k]),fill='#477b9b',stroke=None)
    f.text(505,1120,'Actual developmental age bands (seconds)',15);f.save('BEHAVIOURAL_DASHBOARD')
if __name__=='__main__':
    for n in range(1,13):panels(f'RS-M1-{n:03d}');print('plotted',n,flush=True)
    overlays();behavioral()
