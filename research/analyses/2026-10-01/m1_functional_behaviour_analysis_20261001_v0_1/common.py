"""Passive analysis only. No model import or evolution capability."""
from pathlib import Path
import sys,json,csv,math,gzip,hashlib
import numpy as np
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
PRIOR=ROOT/'m1_long_development_full_analysis_20261001_v0_1'
# Reuse the previously verified plain-data decoder and source definitions only.
import importlib.util
spec=importlib.util.spec_from_file_location('prior_plain',PRIOR/'common.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
OLD=p.OLD;EX=p.EX;BASE=p.BASE;cfg=p.cfg;SL=p.SL;SOURCE=p.SOURCE;RAD=p.RAD
rd=p.rd;attrs=p.attrs;sha=p.sha;plain=p.plain;controls=p.controls;corr=p.corr;rms=p.rms;norm=p.norm
LABEL='NON-CANONICAL RESURRECTION SANDBOX — PASSIVE FUNCTIONAL/BEHAVIOURAL ANALYSIS'
BANDS=[(0,600),(600,1500),(1500,2500),(2500,3500),(3500,4500)]
def save(name,x):
    q=OUT/name;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(plain(x),indent=2,allow_nan=False)+'\n',encoding='utf8')
def table(name,rows):
    q=OUT/name;q.parent.mkdir(parents=True,exist_ok=True)
    if not rows:q.write_text('',encoding='utf8');return
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with q.open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,keys);w.writeheader();w.writerows(plain(rows))
def readcsv(name):return list(csv.DictReader((OUT/name).open(encoding='utf8')))
def div(a,b):return float(a/b) if b else None
def mean(x):return float(np.mean(x)) if len(x) else None
def native(life):return np.load(PRIOR/'cache'/(life+'_native.npy'),mmap_mode='r')
def details(life):return json.loads((OLD/(life+'_DETAILS.json')).read_bytes())
def record(life):return json.loads((PRIOR/'cache'/(life+'.json')).read_bytes())
def rolling(t,y,width=60,squared=False):
    q=np.asarray(y);q=q*q if squared else q;lo=np.searchsorted(t,t-width,side='right');cs=np.r_[0,np.cumsum(q)];v=(cs[1:]-cs[lo])/(np.arange(len(t))+1-lo)
    return np.sqrt(np.maximum(0,v)) if squared else v
def ratio(a,b):return np.divide(a,b,out=np.full_like(np.asarray(a,dtype=float),np.nan),where=np.asarray(b)>1e-20)
def contiguous(mask):
    z=np.r_[False,mask,False];return zip(np.flatnonzero(z[1:]&~z[:-1]),np.flatnonzero(~z[1:]&z[:-1]))
