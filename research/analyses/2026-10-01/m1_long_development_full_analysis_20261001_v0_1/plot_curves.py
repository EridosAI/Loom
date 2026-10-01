"""Review figures from derivative arrays; Pillow raster + ReportLab vector."""
from pathlib import Path
import ast,json,math,csv
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from reportlab.graphics.shapes import Drawing,Line,Rect,Circle,PolyLine,String
from reportlab.graphics import renderSVG
from reportlab.lib.colors import HexColor
OUT=Path(__file__).resolve().parent/'figures';OUT.mkdir(exist_ok=True)
PACKAGE=OUT.parent;ROOT=PACKAGE.parent
source=ROOT/'m1_resurrection_results_20260930_v0_1/passive_reference_sources/historical_plot_helpers.py'
nodes=[n for n in ast.parse(source.read_text()).body if isinstance(n,ast.ClassDef) and n.name=='Fig']
exec(compile(ast.Module(body=nodes,type_ignores=[]),str(source),'exec'))
COLORS=['#2166ac','#b35806','#4d9221','#762a83','#c51b7d','#008b8b','#68523b']
events=json.loads((PACKAGE/'CURVE_EVENTS.json').read_bytes())
def rolling(t,y,width=60):
    lo=np.searchsorted(t,t-width,side='right');cs=np.r_[0,np.cumsum(y)]
    return (cs[1:]-cs[lo])/(np.arange(len(t))+1-lo)
def thin(t,y,bins=1600):
    # Preserve chronological first/last/min/max per display bin, not smoothed substitutes.
    if len(t)<=bins*4:return t,y
    b=np.floor((t-t[0])/(t[-1]-t[0]+1e-15)*bins).astype(int);starts=np.r_[0,np.flatnonzero(np.diff(b))+1];ends=np.r_[starts[1:],len(t)];ids=[]
    for a,e in zip(starts,ends):ids.extend([a,a+int(np.argmin(y[a:e])),a+int(np.argmax(y[a:e])),e-1])
    ids=np.unique(ids);return t[ids],y[ids]
def ax(f,x,y,w,h,xmax,ymax,title,color='#25354a',ymin=0,xtick=True):
    scale=1
    if ymax>0 and ymax<.01:scale=10**math.floor(math.log10(ymax))
    X=lambda z:x+w*z/xmax;Y=lambda z:y+h-h*(z-ymin)/(ymax-ymin)
    f.text(x,y-35,title+(f'  [x {scale:g}]' if scale!=1 else ''),17,color,True)
    for v in np.linspace(ymin,ymax,5):
        f.line([(x,Y(v)),(x+w,Y(v))],'#e7ebef',.7);f.text(x-68,Y(v)-8,f'{v/scale:.3g}',12)
    for v in np.linspace(0,xmax,6):
        f.line([(X(v),y),(X(v),y+h)],'#edf0f3',.7)
        if xtick:f.text(X(v)-18,y+h+6,f'{v:.0f}',12)
    f.line([(x,y),(x,y+h),(x+w,y+h)],'#8c96a3',.8)
    return X,Y
def markers(f,X,y,h,life):
    for e in events:
        if e['life']!=life:continue
        t=e['age'];k=e['kind']
        if k=='external_resurrection':f.line([(X(t),y),(X(t),y+h)],'#dda0a0',.65)
        else:
            color='#16815b' if 'productive' in k else ('#b83636' if 'damage' in k else '#7654a3')
            level=y-(3 if 'productive' in k else (9 if 'damage' in k else 15));f.circle(X(t),level,2.3,fill=color,stroke=None)
def one(life):
    d=np.load(PACKAGE/'cache'/(life+'_curves.npz'));a=d['wave'];cols=list(d['wave_columns']);t=a[:,0];rec=json.loads((PACKAGE/'cache'/(life+'.json')).read_bytes());age=rec['curve_cutoff']
    f=Fig(1440,1625);f.text(32,18,life+' | measured developmental curves',27,bold=True)
    status='complete 4500 s' if age==4500 else ('600 s pilot; overnight unstarted' if age==600 else f'censored at last complete causal checkpoint: {age:.6f} s')
    f.text(32,58,'NON-CANONICAL RESURRECTION SANDBOX | '+status,16)
    f.text(32,90,'Thin pale line: measured raw samples. Dark line: trailing 60 s arithmetic mean (shorter at birth).',14)
    f.text(32,116,'Red vertical: external support. Top dots: source benefit (green), damage (red), repair (purple).',14)
    panels=[('A  association.H | combined Frobenius norm','H_norm','#24649c'),('B  regulator.theta[0] | E-bank Frobenius norm','regulator_theta_E_norm','#b36817'),('C  regulator.theta[1] | I-bank Frobenius norm','regulator_theta_I_norm','#6d4093')]
    for j,(title,key,col) in enumerate(panels):
        y=a[:,cols.index(key)];tt=np.r_[0,t];yy=np.r_[0,y];X,Y=ax(f,115,205+j*278,1240,190,age,max(float(y.max())*1.08,1e-10),title,col)
        markers(f,X,205+j*278,190,life);tr,yr=thin(tt,yy);f.line([(X(x),Y(v)) for x,v in zip(tr,yr)],'#c6d0da',.65)
        sm=rolling(tt,yy);f.line([(X(x),Y(v)) for x,v in zip(tt,sm)],col,1.9)
    bt=d['body_time'];body=d['body'];st=d['support_time'];sb=d['support_body']
    for q,title,col in [(0,'D  body.energy | actual E','#b36817'),(1,'E  body.integrity | actual I','#24649c')]:
        j=3+q;y=body[:,q];X,Y=ax(f,115,205+j*278,1240,190,age,1.02,title,col)
        markers(f,X,205+j*278,190,life)
        tr,yr=thin(bt,y);points=[(float(x),float(v),1) for x,v in zip(tr,yr)]
        points=[p for p in points if p[0] not in set(st)]
        points.extend((float(x),float(v),0 if i%2==0 else 2) for i,(x,v) in enumerate(zip(st,sb[:,q])))
        points.sort(key=lambda x:(x[0],x[2]));f.line([(X(x),Y(v)) for x,v,_ in points],'#c6d0da',.65)
        sm=rolling(bt,y);tx,sy=thin(bt,sm);f.line([(X(x),Y(v)) for x,v in zip(tx,sy)],col,1.8)
    f.text(520,1580,'Actual developmental age (seconds)',15)
    f.text(32,1604,'Raw exports retain every stored wave/native sample. Display-bin extrema retained for dense body curves; no extrapolation.',12)
    f.save(life+'_H_E_I_BODY')
    g=Fig(1440,1640);g.text(32,18,life+' | functional expression',27,bold=True)
    g.text(32,58,status+' | 0.2 s completed waves; thin raw + trailing 60 s mean',16)
    metrics=[('H use: mean of 224 branch-use statistics','H_use_mean'),('Associative return: ||association.q||','q_norm'),('Learned E omission effect: paired current RMS','learned_E_current_delta_rms'),('Learned I omission effect: paired current RMS','learned_I_current_delta_rms'),('M1 spontaneous pair RMS','M1_spontaneous_rms')]
    for j,(title,key) in enumerate(metrics):
        yy=a[:,cols.index(key)];X,Y=ax(g,115,155+j*283,1240,195,age,max(1e-20,float(yy.max())*1.08),title,COLORS[j]);markers(g,X,155+j*283,195,life)
        tr,yr=thin(t,yy);g.line([(X(x),Y(v)) for x,v in zip(tr,yr)],'#c6d0da',.65);g.line([(X(x),Y(v)) for x,v in zip(t,rolling(t,yy))],COLORS[j],1.9)
    g.text(450,1585,'Actual developmental age (seconds)',15);g.text(32,1610,'Omission current = intact minus learned-bank-omitted, same recorded need and exploration. No alternate world.',12);g.save(life+'_FUNCTIONAL')
def overlays():
    for key,title in [('H_norm','association.H'),('regulator_theta_E_norm','regulator.theta[0] (E bank)'),('regulator_theta_I_norm','regulator.theta[1] (I bank)')]:
        f=Fig(1480,930);f.text(32,18,title+' | seven complete lives',26,bold=True);f.text(32,58,'Thin pale raw trajectories; colored trailing 60 s arithmetic means. Identical 4500 s exposure.',15)
        arrays=[]
        for n in range(1,9):
            d=np.load(PACKAGE/'cache'/f'RS-M1-{n:03d}_curves.npz');a=d['wave'];arrays.append((a[:,0],a[:,list(d['wave_columns']).index(key)]))
        maximum=max(y.max() for _,y in arrays)*1.05
        X,Y=ax(f,115,180,1270,450,4500,maximum,'Combined Frobenius norm')
        for n,(t,y) in enumerate(arrays[:7]):
            f.line([(X(x),Y(v)) for x,v in zip(t,y)],'#d4d8df',.45);f.line([(X(x),Y(v)) for x,v in zip(t,rolling(t,y))],COLORS[n],1.9)
            f.line([(50+n*201,106),(72+n*201,106)],COLORS[n],3);f.text(78+n*201,96,f'{n+1:03d}',15,COLORS[n],True)
        f.text(520,673,'Actual developmental age (seconds)',15)
        X,Y=ax(f,115,754,1270,105,4500,maximum,'RS-M1-008 shown separately: censored; same axes','#555555')
        t,y=arrays[7];f.line([(X(x),Y(v)) for x,v in zip(t,y)],'#c6c6c6',.65);f.line([(X(x),Y(v)) for x,v in zip(t,rolling(t,y))],'#222222',1.7);f.circle(X(t[-1]),Y(rolling(t,y)[-1]),3,fill='#ab3434')
        f.text(32,908,'Pilots 009–012 are excluded from this long-exposure comparison. No asymptote or unobserved segment is drawn.',12);f.save('POPULATION_'+key)
def model_figures():
    fits=json.loads((PACKAGE/'CURVE_MODEL_FITS.json').read_bytes())
    for metric,title in [('H_norm','H norm'),('regulator_theta_E_norm','E-bank norm'),('regulator_theta_I_norm','I-bank norm')]:
        f=Fig(1560,2230);f.text(32,18,title+' | descriptive fits and residuals',26,bold=True)
        f.text(32,60,'Black: 60 s medians. Blue: linear. Orange: saturating exponential. Purple: power. Fit interval 0–4500 s.',14)
        f.text(32,86,'These curves are shape diagnostics, not mechanisms. Structured residuals and non-monotonicity count against a model.',14)
        for n in range(1,8):
            life=f'RS-M1-{n:03d}';v=fits[f'{life}:{metric}:exclude0'];t=np.array(v['linear']['age']);obs=np.array(v['linear']['observed']);y=180+(n-1)*286
            high=max(max(obs),*(max(x['predicted']) for x in v.values()))*1.08;low=min(0,*(min(x['predicted']) for x in v.values()))
            X,Y=ax(f,105,y,630,185,4500,high,life+'  | norms',ymin=low)
            for model,col in [('linear','#24649c'),('saturating_exponential','#b36817'),('power','#784baa')]:f.line([(X(a),Y(b)) for a,b in zip(t,v[model]['predicted'])],col,1.4)
            for a,b in zip(t,obs):f.circle(X(a),Y(b),1.7,fill='#111111',stroke=None)
            limit=max(abs(np.array(x['residual'])).max() for x in v.values())*1.08;X,Y=ax(f,895,y,590,185,4500,max(limit,1e-12),'Observed minus fitted',ymin=-max(limit,1e-12))
            f.line([(X(0),Y(0)),(X(4500),Y(0))],'#555555',.8)
            for model,col in [('linear','#24649c'),('saturating_exponential','#b36817'),('power','#784baa')]:f.line([(X(a),Y(b)) for a,b in zip(t,v[model]['residual'])],col,1.2)
        f.text(500,2200,'Actual developmental age (seconds)',14);f.save('MODEL_RESIDUALS_'+metric)
def slope_figure():
    rows=list(csv.DictReader((PACKAGE/'tables/LOCAL_AND_LATE_SLOPES.csv').open(encoding='utf8')));f=Fig(1480,1110);f.text(32,18,'Local developmental slopes | fixed 600 s windows',26,bold=True)
    f.text(32,60,'Theil–Sen slope on non-overlapping 5 s medians, multiplied by 1000. Last window is 4200–4500 s.',14)
    for n,col in enumerate(COLORS):f.text(70+n*190,93,f'RS-M1-{n+1:03d}',13,col,True)
    for j,metric in enumerate(['H_norm','regulator_theta_E_norm','regulator_theta_I_norm']):
        selected=[r for r in rows if r['metric']==metric and r['window_type']=='fixed_600' and int(r['life'][-3:])<=7];val=np.array([float(r['theil_sen_slope'])*1000 for r in selected]);y=190+j*298
        X,Y=ax(f,120,y,1260,190,4500,max(1e-12,float(val.max())*1.1),metric+' | norm change per 1000 s',ymin=min(0,float(val.min())*1.1));f.line([(X(0),Y(0)),(X(4500),Y(0))],'#666666',.8)
        for n,col in enumerate(COLORS):
            r=[v for v in selected if v['life']==f'RS-M1-{n+1:03d}'];pts=[(X((float(v['start'])+float(v['end']))/2),Y(float(v['theil_sen_slope'])*1000)) for v in r];f.line(pts,col,1.8)
            for a,b in pts:f.circle(a,b,2.3,fill=col,stroke=None)
    f.text(530,1075,'Actual developmental age (seconds)',14);f.save('LOCAL_SLOPES')
if __name__=='__main__':
    for n in range(1,13):one(f'RS-M1-{n:03d}');print(f'plotted {n}',flush=True)
    overlays()
    model_figures();slope_figure()
