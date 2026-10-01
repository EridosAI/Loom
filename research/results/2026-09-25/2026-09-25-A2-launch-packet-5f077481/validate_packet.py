"""Portable static packet validator. Standard library only. Never imports Loom."""
import argparse,gzip,hashlib,json,pathlib,zipfile
def digest(b):return hashlib.sha256(b).hexdigest()
def strict(raw):
    def pairs(xs):
        d={}
        for k,v in xs:
            assert k not in d,'duplicate JSON key';d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def verify(read,names):
    fm=strict(read('FILE_MANIFEST.json'))
    assert set(names)==set(fm['files'])|{'FILE_MANIFEST.json'}
    for n,v in fm['files'].items():
        b=read(n);assert len(b)==v['bytes'] and digest(b)==v['sha256'],n
    m=strict(read('A2_MANIFEST.json'));obj={k:v for k,v in m.items() if k!='execution_authority'}
    b=read('AUTHORITY_OBJECT.canonical.json');assert canonical(obj)==b
    h=digest(b);assert strict(read('AUTHORITY_OBJECT.json'))==obj and h==fm['authority_sha256']
    assert read('AUTHORITY_SHA256.txt').decode().split()[0]==h
    assert m['case_id']=='A2' and m['execution_authority'] is None
    assert m['initial_time']==m['initial_index']==0 and m['hard_stop_time']==m['duration_seconds']==180
    assert m['execution']['procedure']['stages']==[{'point':[3.,3.],'until':90.,'press_force':.1},{'point':[6.,3.],'until':120.,'press_force':0.},{'point':[10.,3.],'until':180.,'press_force':.1}]
    assert m['execution']['resources']=={'storage_limit_bytes':1500000000,'wall_limit_seconds':3600}
    pr=m['execution']['procedure']['protocol']
    for n,v in pr['bound_files'].items():assert digest(read(n))==v,n
    snap=pr['initial_snapshot_file'];assert digest(read(snap['name']))==snap['sha256']
    s=strict(gzip.decompress(read(snap['name'])))
    packed=json.dumps(s['state'],separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
    assert digest(packed)==s['state_sha256']==m['initial_state']
    assert m['roster']['execution_authorized'] is False
    return {'valid':True,'payloads':len(fm['files']),'authority_sha256':h,'grant':None,'A2_executed':False,'scope':'byte inventory / exact closed proposed object / prescribed values / snapshot checksum only; no simulation or controller calls'}
def main():
    p=argparse.ArgumentParser();p.add_argument('path',nargs='?',default=str(pathlib.Path(__file__).resolve().parent));a=p.parse_args();root=pathlib.Path(a.path)
    if root.is_file():
        with zipfile.ZipFile(root) as z:
            prefix='A2_LAUNCH_PACKET/'
            assert all(n.startswith(prefix) for n in z.namelist())
            result=verify(lambda n:z.read(prefix+n),[n[len(prefix):] for n in z.namelist()])
    else:result=verify(lambda n:(root/n).read_bytes(),[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()])
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
