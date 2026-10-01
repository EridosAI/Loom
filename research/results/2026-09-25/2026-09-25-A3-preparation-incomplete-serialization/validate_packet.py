"""Portable saved-byte validator. Standard library only; never imports Loom."""
import argparse,base64,gzip,hashlib,json,pathlib,struct,zipfile
def digest(b):return hashlib.sha256(b).hexdigest()
def strict(raw):
    def pairs(xs):
        d={}
        for k,v in xs:
            assert k not in d,'duplicate JSON key';d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def attr(x,key):return dict(x['attrs']['$dict'])[key]
def verify(read,names):
    fm=strict(read('FILE_MANIFEST.json'))
    assert set(names)==set(fm['files'])|{'FILE_MANIFEST.json'}
    for n,v in fm['files'].items():
        b=read(n);assert len(b)==v['bytes'] and digest(b)==v['sha256'],n
    m=strict(read('A3_MANIFEST.json'));obj={k:v for k,v in m.items() if k!='execution_authority'}
    b=read('AUTHORITY_OBJECT.canonical.json');assert canonical(obj)==b
    h=digest(b);assert strict(read('AUTHORITY_OBJECT.json'))==obj and h==fm['authority_sha256']
    assert read('AUTHORITY_SHA256.txt').decode().split()[0]==h
    assert m['case_id']=='A3' and m['execution_authority'] is None
    assert m['initial_time']==m['initial_index']==0 and m['hard_stop_time']==m['duration_seconds']==210
    expected=[{'point':[0.,6.],'until':15.,'press_force':.1},{'point':[1.5,6.],'until':40.,'press_force':0.},{'point':[1.5,10.],'until':75.,'press_force':0.},{'point':[0.,10.],'until':155.,'press_force':.1},{'point':[1.5,10.],'until':180.,'press_force':0.},{'point':[3.,10.],'until':210.,'press_force':.1}]
    assert m['execution']['procedure']['stages']==expected
    assert m['execution']['resources']=={'storage_limit_bytes':1500000000,'wall_limit_seconds':4200}
    pr=m['execution']['procedure']['protocol']
    for n,v in pr['bound_files'].items():assert digest(read(n))==v,n
    for n,v in strict(read('SOURCE_IDENTITIES.json')).items():assert digest(read('references/'+n))==v['sha256']
    snap=pr['initial_snapshot_file'];assert digest(read(snap['name']))==snap['sha256']
    s=strict(gzip.decompress(read(snap['name'])))
    packed=json.dumps(s['state'],separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
    assert digest(packed)==s['state_sha256']==m['initial_state']
    e=s['state'];body=attr(e,'body')
    assert attr(body,'energy')==.7 and attr(body,'integrity')==1
    pos=attr(body,'position');assert pos['dtype']=='<f8' and pos['shape']==[2]
    assert struct.unpack('<dd',base64.b64decode(pos['$array']))==(2.5,6.)
    assert attr(e,'time')==attr(e,'native_index')==0 and attr(e,'status')=='paused'
    assert digest(base64.b64decode(attr(e,'fields')['$array']))==m['initial_fields']
    assert m['roster']['execution_authorized'] is False
    assert pr['case_count']==1
    checks=strict(read('PREPARATION_CHECKS.json'))
    assert all(checks[k]==0 for k in ['Engine_constructor_calls','Run_constructor_calls','computed_controller_commands','world_steps','field_steps','neural_steps','simulation_RNG_draws','new_prehistory_steps','replays'])
    assert checks['allowed_snapshot_and_static_transduction_calls']['transduce']==1
    assert strict(read('HASH_BEFORE.json'))==strict(read('HASH_AFTER.json'))
    return {'valid':True,'payloads':len(fm['files']),'authority_sha256':h,'grant':None,'A3_executed':False,'scope':'Byte inventory, closed proposed object, healthy zero-time snapshot and preparation record checks; no dynamics or controller calls'}
def main():
    p=argparse.ArgumentParser();p.add_argument('path',nargs='?',default=str(pathlib.Path(__file__).resolve().parent));root=pathlib.Path(p.parse_args().path)
    if root.is_file():
        with zipfile.ZipFile(root) as z:
            prefix='A3_LAUNCH_PACKET/';assert all(n.startswith(prefix) for n in z.namelist())
            result=verify(lambda n:z.read(prefix+n),[n[len(prefix):] for n in z.namelist()])
    else:result=verify(lambda n:(root/n).read_bytes(),[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()])
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
