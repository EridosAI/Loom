"""Portable A4 saved-byte validator; standard library only, no Loom import or execution."""
import argparse,base64,gzip,hashlib,json,math,pathlib,struct,zipfile
def digest(b):return hashlib.sha256(b).hexdigest()
def strict(raw):
    def pairs(xs):
        d={}
        for k,v in xs:
            assert k not in d,'duplicate key';d[k]=v
        return d
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def attr(x,k):return dict(x['attrs']['$dict'])[k]
def vector(x):return list(struct.unpack('<'+'d'*math.prod(x['shape']),base64.b64decode(x['$array'])))
def state_digest(x):return digest(json.dumps(x,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode())
def verify(read,names,sealed=True):
    if sealed:
        fm=strict(read('FILE_MANIFEST.json'));assert set(names)==set(fm['files'])|{'FILE_MANIFEST.json'}
        for n,v in fm['files'].items():
            b=read(n);assert len(b)==v['bytes'] and digest(b)==v['sha256'],n
    batch=strict(read('AUTHORITY_OBJECT.json'));raw=read('AUTHORITY_OBJECT.canonical.json')
    assert canonical(batch)==raw;h=digest(raw);assert read('AUTHORITY_SHA256.txt').decode().split()[0]==h
    if sealed:assert fm['authority_sha256']==h
    assert batch['status']=='PROPOSED / NOT AUTHORIZED' and batch['schema']=='loom-A4-batch-authority-v1'
    assert batch['p_commit']=='6bc9683b54e4fa80136fe8534d7713e2a250a95f' and batch['apparatus_commit']=='5f07748102cb5eaa302569c87efbae095050e9fe'
    expected=[('A4-CROSS',[10.,8.8],[10.,12.],16.,0.,480),('A4-WAIT',[6.,8.8],[6.,12.],28.,12.,780),('A4-DETOUR',[1.5,6.],[1.5,14.],32.,0.,840)]
    assert batch['case_order']==[x[0] for x in expected] and len(batch['cases'])==3
    for n,v in batch['bound_documents'].items():assert digest(read(n))==v,n
    originals=strict(read('SOURCE_IDENTITIES.json'))
    for n,v in originals.items():assert digest(read('references/'+n))==v['sha256'] and len(read('references/'+n))==v['bytes']
    parent=strict(gzip.decompress(read('references/INITIAL_A1.snapshot.json.gz')))['state']
    parent_body=attr(parent,'body');initials=[]
    for member,(cid,a,b,dur,wait,wall) in zip(batch['cases'],expected):
        assert member['case_id']==cid
        assert digest(read(member['manifest_file']))==member['manifest_file_sha256']
        m=strict(read(member['manifest_file']));obj={k:v for k,v in m.items() if k!='execution_authority'}
        assert member['execution_object']==obj and canonical(obj)==read(member['execution_object_file'])
        assert digest(canonical(obj))==member['execution_sha256']
        assert m['case_id']==cid and m['execution_authority'] is None and m['mode']=='external_controller' and m['controller']=='waypoint'
        assert m['purpose']=='commissioning' and m['initial_time']==m['initial_index']==0 and m['duration_seconds']==m['hard_stop_time']==dur
        assert m['phase']==3.558411277237072 and m['initial_fields']=='7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096'
        assert m['roster']['execution_authorized'] is False and m['command_hold_seconds']==.1
        assert m['execution']['resources']=={'storage_limit_bytes':100000000,'wall_limit_seconds':wall}
        stages=([{'point':a,'until':wait,'press_force':0.}] if wait else [])+[{'point':b,'until':dur,'press_force':0.}]
        assert m['execution']['procedure']['stages']==stages
        assert all(abs(p['until']/.2-round(p['until']/.2))<1e-9 for p in stages)
        p=m['execution']['procedure']['protocol'];assert p['matrix_parent_row']=='A4' and p['member_count']==3
        for n,v in p['bound_files'].items():assert digest(read(n))==v,n
        snap=p['initial_snapshot_file'];assert digest(read(snap['name']))==snap['sha256']
        wrapper=strict(gzip.decompress(read(snap['name'])));e=wrapper['state'];body=attr(e,'body')
        assert state_digest(e)==wrapper['state_sha256']==m['initial_state']
        assert vector(attr(body,'position'))==a and attr(body,'angle')==math.pi/2
        assert attr(body,'energy')==.7 and attr(body,'integrity')==1
        for k,v in body['attrs']['$dict']:
            if k not in ('position','angle'):assert v==attr(parent_body,k)
        changed=[]
        for k,v in e['attrs']['$dict']:
            if v!=attr(parent,k):changed.append(k)
        assert sorted(changed)==['birth_provenance','body','raw']
        assert attr(e,'time')==attr(e,'native_index')==0 and attr(e,'status')=='paused'
        assert digest(base64.b64decode(attr(e,'fields')['$array']))==m['initial_fields']
        assert m['initialization']['phase']==m['phase'] and digest(read('verified-cache/manifest.json'))==m['initialization']['cache_receipt_sha256']
        initials.append(m['initial_state'])
    assert len(set(initials))==3
    limits=batch['batch_limits'];assert limits['total_simulated_seconds']==76 and limits['total_native_steps']==7600 and limits['total_runner_wall_seconds']==2100
    checks=strict(read('PREPARATION_CHECKS.json'))
    for k in ['Engine_constructor_calls','Run_constructor_calls','computed_controller_commands','world_steps','field_steps','neural_steps','simulation_RNG_draws','new_prehistory_steps','replays','trial_routes','trial_phases']:assert checks[k]==0
    assert checks['allowed_static_calls']=={'load_snapshot':6,'transduce':3,'save_snapshot':3} and checks['blocked_dynamic_calls']==[]
    assert len(checks['null_grant_denials'])==3 and checks['prospective_output_directory_absent'] is True
    assert strict(read('HASH_BEFORE.json'))==strict(read('HASH_AFTER.json'))
    geo=strict(read('GEOMETRY_AND_TIMING.json'))
    assert geo['CROSS']['clear_for_all_y_end_exclusive']>10 and geo['WAIT']['horizontal_conflict_interval'][1]<12
    assert geo['WAIT']['next_horizontal_conflict_at']>22 and geo['segments']['A4-DETOUR']['mover_union_clearance']==3
    return {'valid':True,'sealed':sealed,'payload_count':len(fm['files']) if sealed else None,'authority_sha256':h,'cases':batch['case_order'],'execution_grants':[None,None,None],'world_steps':0,'computed_controller_commands':0,'scope':'Source bytes, exact batch/member bindings, original healthy zero-time snapshots and preparation record; no simulation or command recomputation'}
def main():
    p=argparse.ArgumentParser();p.add_argument('path',nargs='?',default=str(pathlib.Path(__file__).resolve().parent));p.add_argument('--unsealed',action='store_true');a=p.parse_args();root=pathlib.Path(a.path)
    if root.is_file():
        with zipfile.ZipFile(root) as z:result=verify(z.read,z.namelist(),not a.unsealed)
    else:result=verify(lambda n:(root/n).read_bytes(),[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()],not a.unsealed)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
