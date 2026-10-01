"""Passive plain-data utilities. No Loom imports, constructors, RNG or evolution."""
from pathlib import Path
import ast,csv,hashlib,json,math,struct,zlib
import numpy as np
OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
OLD=ROOT/'m1_resurrection_results_20260930_v0_1'
PREP=ROOT/'m1_resurrection_sandbox_20260930_v0_1'
EX=PREP/'execution'
BASE=ROOT/'worktrees/loom-contact-release-20260930/developmental_ecology'
LABEL='NON-CANONICAL RESURRECTION SANDBOX — PASSIVE ANALYSIS ONLY'
def sha(p):
    v=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(8*1024*1024),b''):v.update(b)
    return v.hexdigest()
def plain(x):
    if isinstance(x,np.ndarray):return plain(x.tolist())
    if isinstance(x,np.generic):return plain(x.item())
    if isinstance(x,float) and not math.isfinite(x):return None
    if isinstance(x,dict):return {str(k):plain(v) for k,v in x.items()}
    if isinstance(x,(tuple,list)):return [plain(v) for v in x]
    return x
def save(name,x):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(plain(x),indent=2,allow_nan=False)+'\n',encoding='utf8')
def table(name,rows):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    if not rows:p.write_text('',encoding='utf8');return
    keys=list(dict.fromkeys(k for r in rows for k in r))
    with p.open('w',newline='',encoding='utf8') as f:
        w=csv.DictWriter(f,keys);w.writeheader();w.writerows(plain(rows))
def attrs(x):return x['attributes']
def norm(x):return float(np.linalg.norm(x))
def rms(x):return float(np.sqrt(np.mean(np.asarray(x)**2))) if np.size(x) else None
def corr(a,b):
    a=np.asarray(a);b=np.asarray(b);good=np.isfinite(a)&np.isfinite(b);a=a[good];b=b[good]
    return float(np.corrcoef(a,b)[0,1]) if len(a)>2 and np.std(a)>1e-15 and np.std(b)>1e-15 else None
def sigmoid(x):return 1/(1+np.exp(-np.asarray(x)))
SEAL=json.loads((OLD/'EXECUTION_CUSTODY_SEAL.json').read_bytes())
HASHES={v['path']:v['sha256'] for v in SEAL['files']}
decoder=OLD/'passive_reference_sources/audit_exploration.py'
node=next(n for n in ast.parse(decoder.read_text()).body if isinstance(n,ast.FunctionDef) and n.name=='read_data')
U=struct.Struct('<Q');F=struct.Struct('<d')
exec(compile(ast.Module(body=[node],type_ignores=[]),str(decoder),'exec'))
def rd(p):return read_data(p,HASHES[p.relative_to(EX).as_posix()])
schema_file=BASE/'loom_developmental/evidence.py'
schema=next(n.value for n in ast.parse(schema_file.read_text()).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='NATIVE_FIELDS' for t in n.targets))
SL={};WIDTH=0
for name,width in ast.literal_eval(schema):SL[name]=slice(WIDTH,WIDTH+width);WIDTH+=width
cfg=json.loads((BASE/'configuration.json').read_bytes())
SOURCE=np.array(cfg['source_positions']);RAD=cfg['body_radius']+cfg['source_radius']
def controls(learned,exploration,need):
    w=need[...,None]*(learned+exploration);g=8
    return np.concatenate((sigmoid(w[...,:g].sum(axis=-2)),cfg['current_max']/2*np.tanh(w[...,g:g+2]).sum(axis=-2),sigmoid(cfg['attenuation_bias']+w[...,g+2:g+4].sum(axis=-2))),axis=-1)
def checkpoint_paths(life):
    return [p for p in sorted((EX/'lives'/life).glob('*.ld')) if not p.name.startswith(('chunk-','resurrection-')) and 'failure-tail' not in p.name]
def describe(x,depth=0):
    if isinstance(x,np.ndarray):return {'shape':list(x.shape),'dtype':str(x.dtype)}
    if isinstance(x,dict):return {str(k):describe(v,depth+1) for k,v in x.items()} if depth<6 else list(map(str,x))
    if isinstance(x,(list,tuple)):return [describe(v,depth+1) for v in x[:2]]+(['...'] if len(x)>2 else [])
    return x
if __name__=='__main__':
    p=EX/'lives/RS-M1-002/overnight-000234000-periodic.ld'
    e=attrs(rd(p)['engine'])
    save('SCHEMA_PROFILE.json',describe(e))
    c=rd(EX/'lives/RS-M1-002/chunk-000234001-000234100.ld')
    save('CHUNK_PROFILE.json',describe(c))
    print('Profile written; no model imported or executed.')
