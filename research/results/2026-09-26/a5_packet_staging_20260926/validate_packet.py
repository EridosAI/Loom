"""Portable saved-byte A5 HOLD validator. No Loom import or simulation."""
import argparse,base64,gzip,hashlib,json,math,pathlib,struct,zipfile

def digest(b):return hashlib.sha256(b).hexdigest()
def strict(raw):
    def pairs(xs):
        result={}
        for k,v in xs:
            assert k not in result,'duplicate key';result[k]=v
        return result
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def attr(x,k):return dict(x['attrs']['$dict'])[k]
def vector(x):return list(struct.unpack('<'+'d'*math.prod(x['shape']),base64.b64decode(x['$array'])))
def state_digest(x):return digest(json.dumps(x,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode())

def verify(read,names,sealed=True):
    assert len(names)==len(set(names)),'duplicate package member'
    if sealed:
        fm=strict(read('FILE_MANIFEST.json'))
        assert set(names)==set(fm['files'])|{'FILE_MANIFEST.json'}
        for n,v in fm['files'].items():
            b=read(n);assert len(b)==v['bytes'] and digest(b)==v['sha256'],n
    m=strict(read('A5_MANIFEST.json'));obj=strict(read('AUTHORITY_OBJECT.json'));raw=read('AUTHORITY_OBJECT.canonical.json')
    assert obj=={k:v for k,v in m.items() if k!='execution_authority'} and raw==canonical(obj)
    h=digest(raw);assert read('AUTHORITY_SHA256.txt').decode().split()[0]==h
    if sealed:assert fm['authority_sha256']==h
    assert m['execution_authority'] is None and m['case_id']=='A5' and m['mode']=='external_controller' and m['controller']=='waypoint'
    assert m['purpose']=='commissioning' and m['initial_time']==m['initial_index']==0
    assert m['baseline']=='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
    assert m['apparatus']['sha256']=='d5801b69ae38d3259f3426aed8753fef8d76132a2f4ffecdd9baffb29afeb71a'
    assert m['duration_seconds']==m['hard_stop_time']==630 and m['command_hold_seconds']==.1
    assert m['roster']['execution_authorized'] is False
    assert m['execution']['resources']=={'storage_limit_bytes':1500000000,'wall_limit_seconds':14400}
    p=m['execution']['procedure']['protocol'];assert p['launch_disposition']=='HOLD_CLOCK_INCOMPATIBILITY'
    assert p['launch_ready'] is False and p['packet_status']=='PROPOSED / NOT AUTHORIZED / HOLD'
    stages=[{'point':a,'until':t,'press_force':f} for a,t,f in [([3.,3.],90.,.1),([6.,3.],120.,0.),([10.,3.],270.,.1),([6.,3.],300.,0.),([3.,3.],450.,.1),([6.,3.],480.,0.),([10.,3.],630.,.1)]]
    assert m['execution']['procedure']['stages']==stages
    for n,v in p['bound_files'].items():assert digest(read(n))==v,n
    for n,v in strict(read('SOURCE_IDENTITIES.json')).items():
        assert digest(read('references/'+n))==v['sha256'] and len(read('references/'+n))==v['bytes'],n
    s=p['initial_snapshot_file']
    assert digest(read(s['name']))==s['sha256']
    assert read(s['name'])==read('references/INITIAL_A1.snapshot.json.gz')
    wrapper=strict(gzip.decompress(read(s['name'])));e=wrapper['state'];body=attr(e,'body')
    assert wrapper['state_sha256']==state_digest(e)==m['initial_state']=='37adf68654e324141c678316f0f1f4b777853948e548cdd0d133e810c8722a6b'
    assert attr(e,'time')==attr(e,'native_index')==0 and attr(e,'status')=='paused'
    assert vector(attr(body,'position'))==[6.,3.] and attr(body,'angle')==math.pi
    assert attr(body,'energy')==.7 and attr(body,'integrity')==1. and vector(attr(e,'stocks'))==[.2]*8
    for key in ('velocity','command','force','contact_rates'):assert all(v==0 for v in vector(attr(body,key)))
    assert attr(body,'omega')==0
    assert attr(e,'phase')==m['phase']==3.558411277237072
    assert digest(base64.b64decode(attr(e,'fields')['$array']))==m['initial_fields']=='7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096'
    assert digest(read('verified-cache/manifest.json'))==m['initialization']['cache_receipt_sha256']
    cache=strict(read('verified-cache/manifest.json'));assert cache['status']=='complete' and cache['steps_completed']==60000
    assert digest(read('verified-cache/fields.npz'))==cache['file_sha256']
    for module,v in m['apparatus']['files'].items():assert digest(read('instrument/developmental_ecology/loom_commissioning/'+module))==v,module
    ids=strict(read('CODE_AND_RUNTIME_IDENTITIES.json'))
    for module,v in ids['P']['files'].items():assert digest(read('instrument/developmental_ecology/loom_p/'+module))==v,module
    assert ids['runtime']==m['execution']['runtime'] and ids['apparatus_commit']=='5f07748102cb5eaa302569c87efbae095050e9fe'
    clock=strict(read('CLOCK_AUDIT.json'));assert clock['first_decision_exceedance']['native_index']==26950
    now=0.
    for i in range(26950):now+=.01
    assert now==clock['first_decision_exceedance']['accumulated_time'] and abs(now-269.5)>1e-10
    assert clock['commissioning_failure_observed'] is False and clock['world_steps']==clock['controller_calls']==0
    prep=strict(read('PREPARATION_CHECKS.json'))
    for key in ('world_steps','field_steps','neural_steps','controller_commands','simulation_RNG_draws','new_prehistory_steps','Engine_constructors','Run_constructors','sensor_evaluations','trial_routes','trial_phases','replays'):assert prep[key]==0,key
    assert prep['forbidden_calls']==[] and prep['null_grant_denial']=='commissioning execution is not authorized'
    assert prep['production_history_validation_executed'] is False and prep['prospective_output_absent'] is True
    assert strict(read('HASH_BEFORE.json'))==strict(read('HASH_AFTER.json'))
    return {'saved_byte_checks_pass':True,'launch_ready':False,'disposition':'HOLD_CLOCK_INCOMPATIBILITY',
            'authority_sha256':h,'payload_count':len(fm['files']) if sealed else None,'execution_grant':None,
            'world_steps':0,'controller_commands':0,'scope':'Packet identity/structure and scalar clock arithmetic only; not runtime fitness or physical outcome verification.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('path',nargs='?',default=str(pathlib.Path(__file__).resolve().parent));p.add_argument('--unsealed',action='store_true');a=p.parse_args();root=pathlib.Path(a.path)
    if root.is_file():
        with zipfile.ZipFile(root) as z:result=verify(z.read,z.namelist(),not a.unsealed)
    else:result=verify(lambda n:(root/n).read_bytes(),[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()],not a.unsealed)
    print(json.dumps(result,indent=2))
