"""Three fixed zero-time starts. Static geometry/transduction only; no case execution."""
import ast,copy,hashlib,json,math,pathlib,shutil,sys
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-minimal-20260929';D=W/'developmental_ecology'
OUT=S/'packet'
ORIGIN=ROOT/'exports/2026-09-25-first-commissioning-launch-packet-5f077481/INITIAL_A1.snapshot.json.gz'
A3=ROOT/'exports/2026-09-25-A3-launch-packet-5f077481/A3_MANIFEST.json'
CACHE=pathlib.Path('C:/Users/Jason/Desktop/Eridos/Loom-p-apparatus-20260924-01a0c405/developmental_ecology/artifacts/prehistory-attempt-001')
COUNTS={};BLOCKED=[]

def guard(frame,event,arg):
    if event!='call':return
    p=frame.f_code.co_filename.replace('\\','/');name=frame.f_code.co_name
    if '/loom_p/' not in p and '/loom_commissioning/' not in p:return
    bad=name in {'step','advance','account','prepare','draw','native','handoff','_coupled','coupled',
                'waypoint_command','command','begin_command','hold','resume','from_verified_cache','load_restart'}
    bad |= name=='__init__' and p.endswith(('/engine.py','/runner.py','/neural.py','/schema.py'))
    if bad:BLOCKED.append(p+':'+name);raise AssertionError('Static preparation blocked '+BLOCKED[-1])
    if name in {'load_snapshot','save_snapshot','transduce'}:COUNTS[name]=COUNTS.get(name,0)+1
sys.setprofile(guard);sys.path.insert(0,str(D))
import numpy as np
from loom_p.records import load_snapshot,save_snapshot,state_hash,view
from loom_p.geometry import transduce,fixtures,gap_normal
from loom_p.prehistory import field_law

def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def js(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def write(name,value):
    p=OUT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(view(value),indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')

def segment_gap(a,b,f,r):
    if f['kind']=='disk':
        delta=b-a;fraction=np.clip(float((f['centre']-a)@delta)/float(delta@delta),0,1)
        return float(np.linalg.norm(a+fraction*delta-f['centre'])-r-f['radius'])
    if f['kind']=='wall':return float(min(f['sign']*(a[f['axis']]-f['boundary'])-r,f['sign']*(b[f['axis']]-f['boundary'])-r))
    # These approach segments are vertical, so this box distance is exact.
    lo=np.minimum(a,b);hi=np.maximum(a,b);x0,x1,y0,y1=f['rect']
    return math.hypot(max(x0-hi[0],lo[0]-x1,0),max(y0-hi[1],lo[1]-y1,0))-r

def main():
    assert not OUT.exists();OUT.mkdir()
    frozen={str(p.relative_to(D)):sha(p) for folder in ('loom_p','loom_commissioning')
            for p in (D/folder).iterdir() if p.suffix in ('.py','.html')}
    write('CONTROLLER_FROZEN_BEFORE_STARTS.json',dict(files=frozen,decision='Accepted constants fixed; no outcomes, readings or controller calls used to choose placements.'))
    init=copy.deepcopy(js(A3)['initialization']);receipt=js(CACHE/'manifest.json')
    assert sha(CACHE/'manifest.json')==init['cache_receipt_sha256']
    assert receipt['status']=='complete' and receipt['steps_completed']==60000
    assert sha(CACHE/'fields.npz')==receipt['file_sha256']
    original_hash=sha(ORIGIN)
    original=load_snapshot(ORIGIN)
    assert state_hash(original)=='37adf68654e324141c678316f0f1f4b777853948e548cdd0d133e810c8722a6b'
    assert receipt['law']==field_law(original.c) and receipt['phase']==original.phase==init['phase']
    with np.load(CACHE/'fields.npz',allow_pickle=False) as data:
        assert data['fields'].tobytes()==original.fields.tobytes()
    assert digest(original.fields.tobytes())==init['field_sha256']==receipt['field_sha256']
    # The existing loader's lawful-reuse dependency check, without drawing a phase.
    dependency={}
    for name in ('chemistry.py','geometry.py','schema.py'):
        present=(D/'loom_p'/name).read_bytes()
        if digest(present)==receipt['code']['files'][name]:dependency[name]='byte identical';continue
        old=(CACHE/'law-source-at-preparation'/name).read_bytes()
        assert digest(old)==receipt['code']['files'][name]
        if name=='chemistry.py':assert old==present
        else:
            relevant={'geometry.py':('circle_rect_area','disk_areas','rectangle_areas','mover'),'schema.py':('Streams',)}[name]
            def required_nodes(raw):
                tree=ast.parse(raw)
                return ast.dump(ast.Module(body=[x for x in tree.body if isinstance(x,(ast.Import,ast.ImportFrom)) or getattr(x,'name',None) in relevant],type_ignores=[]),include_attributes=False)
            assert required_nodes(old)==required_nodes(present)
        dependency[name]='original hash verified; loader dependency AST/imports identical'
    write('PREHISTORY_REUSE.json',dict(initialization=init,cache_archive_sha256=sha(CACHE/'fields.npz'),
        source_receipt_sha256=sha(CACHE/'manifest.json'),dependency_verification=dependency,
        field_bytes_match_public_A1_zero_time_state=True,law_and_stock_and_phase_match=True,
        new_prehistory_steps=0,phase_RNG_draws=0,original_snapshot_sha256=original_hash))
    for p in CACHE.rglob('*'):
        if p.is_file():q=OUT/'verified-cache'/p.relative_to(CACHE);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
    rows=[];matches=[]
    # Fixed construction chosen on public geometry: first three canonical sources,
    # body due north, declared gap/bearing. No candidate search or response sampling.
    for k,(gap,bearing) in enumerate(((1.25,45.),(1.75,-45.),(2.25,60.))):
        label='S'+str(k+1);e=copy.deepcopy(original);cfg=e.c
        target=np.array(cfg.source_positions[k],dtype=float)
        position=target+np.array([0.,cfg.body_radius+cfg.source_radius+gap])
        angle=-math.pi/2-math.radians(bearing)
        endpoint=target+np.array([0.,cfg.body_radius+cfg.source_radius])
        scene=fixtures(cfg,0,e.phase)
        initial_gaps={f['id']:gap_normal(position,cfg.body_radius,f)[0] for f in scene}
        target_id='source-'+str(k)
        assert min(initial_gaps.values())>0 and abs(initial_gaps[target_id]-gap)<1e-12
        corridors={f['id']:segment_gap(position,endpoint,f,cfg.body_radius) for f in scene if f['id'] not in (target_id,'mover')}
        mx,my=cfg.mover_centre;mw,mh=cfg.mover_size
        swept=dict(kind='rect',rect=[mx-cfg.mover_amplitude-mw/2,mx+cfg.mover_amplitude+mw/2,my-mh/2,my+mh/2])
        corridors['mover-swept-region']=segment_gap(position,endpoint,swept,cfg.body_radius)
        assert min(corridors.values())>0
        travel=.228*(30-1+math.exp(-30));forward=np.array([math.cos(angle),math.sin(angle)])
        rays={f['id']:segment_gap(position,position+travel*forward,f,cfg.body_radius) for f in scene if f['kind']=='disk'}
        assert min(rays.values())>0
        actual_bearing=math.atan2(math.sin(-math.pi/2-angle),math.cos(-math.pi/2-angle))
        assert abs(math.degrees(actual_bearing)-bearing)<1e-12
        before={name:state_hash(value) for name,value in vars(e).items()};old_body=copy.deepcopy(vars(e.body))
        e.body.position=position;e.body.angle=angle
        e.raw=transduce(cfg,e.body,e.fields,0,e.phase)
        e.birth_provenance=dict(kind='B1_v0_2_manufactured_external_start',lawful_newborn_sample=False,
            start_id=label,position=position.tolist(),angle=angle,phase=e.phase,
            construction='First three canonical energy sources; body due north; exact accepted gaps and relative bearings.',
            parent_snapshot_sha256=original_hash,retained_origin=copy.deepcopy(original.birth_provenance))
        assert e.time==e.native_index==0 and e.body.energy==.7 and e.body.integrity==1
        assert all(state_hash(getattr(e.body,n))==state_hash(v) for n,v in old_body.items() if n not in ('position','angle'))
        assert sorted(n for n,v in vars(e).items() if state_hash(v)!=before[n])==['birth_provenance','body','raw']
        e.validate_state()
        path=OUT/'starts'/label/'INITIAL.snapshot.json.gz';path.parent.mkdir(parents=True)
        snap=save_snapshot(path,e)
        assert state_hash(load_snapshot(path))==state_hash(e)
        summary=dict(start=label,body=view(vars(e.body)),target_source_index=k,target_source_position=target,
            surface_gap=gap,relative_bearing_degrees=bearing,actual_bearing_degrees=math.degrees(actual_bearing),
            native_index=0,time=0.,phase=e.phase,stocks=e.stocks,initialization=init,
            field_sha256=digest(e.fields.tobytes()),state_sha256=state_hash(e),snapshot_sha256=snap['sha256'],
            inactive_organism_sha256=state_hash(e.organism),rng_counters=e.organism.rng.counters,
            initial_gaps=initial_gaps,approach_segment=[position,endpoint],approach_clearance=corridors,
            nominal_forward_envelope=travel,forward_source_clearances=rays,
            label='Manufactured external assay start; not a P life or continuation',controller_calls=0,world_steps=0)
        write('starts/'+label+'/START_MANIFEST.json',summary);rows.append(summary)
        copies=[]
        for arm in ('FULL','CHEMISTRY-HIDDEN','SENSORY-FREE'):
            cid='B1-MINIMAL-'+label+'-'+arm;dest=OUT/'cases'/cid/'INITIAL.snapshot.json.gz';dest.parent.mkdir(parents=True)
            shutil.copyfile(path,dest);assert dest.read_bytes()==path.read_bytes()
            copies.append(dict(case=cid,file=dest.relative_to(OUT).as_posix(),snapshot_sha256=sha(dest),state_sha256=state_hash(e)))
        matches.append(dict(start=label,complete_snapshot_bytes_identical=True,copies=copies))
    assert COUNTS=={'load_snapshot':4,'transduce':3,'save_snapshot':3} and not BLOCKED
    assert frozen=={str(p.relative_to(D)):sha(p) for folder in ('loom_p','loom_commissioning') for p in (D/folder).iterdir() if p.suffix in ('.py','.html')}
    assert sha(ORIGIN)==original_hash
    write('MATCHED_INITIAL_STATE_PROOF.json',dict(triplets=matches,includes='Complete Engine snapshot: physical/body/field/phase/stocks/clock/RNG and retained inactive neural state.',arm_specific_controller_state='Separate fresh SEEK / release_count=0 for every case; not part of physical snapshot.'))
    write('STATIC_PREPARATION_CHECKS.json',dict(allowed_calls=COUNTS,blocked_calls=BLOCKED,world_steps=0,
        field_steps=0,prehistory_steps=0,controller_calls_on_starts=0,simulation_RNG_draws=0,
        Engine_or_Run_constructors=0,candidate_outcome_trials=0,geometry_replacements=0,
        production_bytes_frozen_before_and_after=True,old_human_B1_fixture_inspected=False,
        exact_geometries_admissible=True,matched_complete_initial_states=True,execution_grants_created=0))
    print(json.dumps(dict(status='prepared static starts only',starts=[dict(start=x['start'],position=x['body']['position'],angle=x['body']['angle'],min_forward_source_clearance=min(x['forward_source_clearances'].values())) for x in rows],world_steps=0,controller_calls=0)))
if __name__=='__main__':main()
