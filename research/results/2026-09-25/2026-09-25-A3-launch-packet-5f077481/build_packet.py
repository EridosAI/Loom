"""A3 proposal authoring only. Guard all dynamic operations; no launch grant."""
import base64,copy,gzip,hashlib,io,json,math,os,pathlib,shutil,subprocess,sys,time,zipfile
S=pathlib.Path(__file__).resolve().parent
ROOT=S.parent
R1=ROOT/'exports/2026-09-25-first-commissioning-launch-packet-5f077481'
R2=ROOT/'exports/2026-09-25-A2-launch-packet-5f077481'
A2DEL=ROOT/'exports/2026-09-25-A2-commissioning-result-5f077481'
A2ZIP=A2DEL/'A2_COMMISSIONING_RESULT.zip'
OUT=ROOT/'exports/2026-09-25-A3-launch-packet-5f077481'
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology'
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
CACHE=D/'artifacts/prehistory-attempt-001'
DEST=D/'artifacts/commissioning-A3-20260925-5f077481/trajectory-001'
APP='5f07748102cb5eaa302569c87efbae095050e9fe'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
PLAN=[{'point':[0.,6.],'until':15.,'press_force':.1},
      {'point':[1.5,6.],'until':40.,'press_force':0.},
      {'point':[1.5,10.],'until':75.,'press_force':0.},
      {'point':[0.,10.],'until':155.,'press_force':.1},
      {'point':[1.5,10.],'until':180.,'press_force':0.},
      {'point':[3.,10.],'until':210.,'press_force':.1}]
COUNTS={}
BLOCKED=[]
def guard(frame,event,arg):
    if event!='call':return
    f=frame.f_code;path=f.co_filename.replace('\\','/')
    if '/loom_p/' in path or '/loom_commissioning/' in path:
        forbidden=f.co_name in {'step','advance','account','prepare','waypoint_command','native','handoff','draw','_coupled','coupled','begin_command','hold','resume','from_verified_cache'}
        forbidden |= f.co_name=='__init__' and path.endswith(('/engine.py','/runner.py','/neural.py','/schema.py'))
        if forbidden:
            BLOCKED.append(path+':'+f.co_name)
            raise AssertionError('Preparation forbids dynamic operation: '+BLOCKED[-1])
        if f.co_name in {'transduce','load_snapshot','save_snapshot'}:COUNTS[f.co_name]=COUNTS.get(f.co_name,0)+1
sys.setprofile(guard)
sys.path.insert(0,str(D))
from loom_commissioning import authority,contract,runner
from loom_p.records import code_identity,load_snapshot,save_snapshot,state_hash,view
from loom_p.geometry import transduce
import numpy as np

def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def write(n,v):
    p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(view(v),ensure_ascii=False,allow_nan=False,indent=2)+'\n',encoding='utf-8')
def cp(p,n):
    q=OUT/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(S/'empty-excludes').as_posix(),'-C',str(W),*args],env=env)
def verify_zip(raw,prefix=''):
    z=zipfile.ZipFile(io.BytesIO(raw));fm=json.loads(z.read(prefix+'FILE_MANIFEST.json'))
    assert set(z.namelist())=={prefix+n for n in fm['files']}|{prefix+'FILE_MANIFEST.json'}
    for n,v in fm['files'].items():
        b=z.read(prefix+n);assert len(b)==v['bytes'] and digest(b)==v['sha256'],n
    return z,len(fm['files'])
def segment_gap(a,b,f,r):
    if f['kind']=='disk':
        v=[b[i]-a[i] for i in range(2)];den=sum(x*x for x in v)
        u=max(0,min(1,sum((f['centre'][i]-a[i])*v[i] for i in range(2))/den))
        return math.hypot(*(a[i]+u*v[i]-f['centre'][i] for i in range(2)))-r-f['radius']
    if f['kind']=='wall':return min(f['sign']*(a[f['axis']]-f['boundary'])-r,f['sign']*(b[f['axis']]-f['boundary'])-r)
    lo=[min(a[i],b[i]) for i in range(2)];hi=[max(a[i],b[i]) for i in range(2)]
    x0,x1,y0,y1=f['rect'];dx=max(x0-hi[0],lo[0]-x1,0);dy=max(y0-hi[1],lo[1]-y1,0)
    assert dx>0 or dy>0
    return math.hypot(dx,dy)-r

def main():
    started=time.perf_counter()
    assert git('rev-parse','HEAD').decode().strip()==APP and not git('status','--porcelain').strip()
    assert not DEST.parent.exists()
    assert code_identity()['sha256']=='63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9'
    assert contract.apparatus_identity()['sha256']=='d5801b69ae38d3259f3426aed8753fef8d76132a2f4ffecdd9baffb29afeb71a'
    for p in (D/'loom_p').glob('*.py'):assert p.read_bytes()==git('show',P+':developmental_ecology/loom_p/'+p.name)
    assert (D/'configuration.json').read_bytes()==git('cat-file','--filters',P+':developmental_ecology/configuration.json')
    assert sha(A2ZIP)=='212c0497531e3ccee7b2b3825045dda116ca15468fe3415a4e79634d620cb502'
    z2,n2=verify_zip(A2ZIP.read_bytes())
    zr2,nr2=verify_zip(z2.read('approved-launch/A2_LAUNCH_PACKET.zip'),'A2_LAUNCH_PACKET/')
    z1,n1=verify_zip(zr2.read('A2_LAUNCH_PACKET/references/FIRST_A1_COMMISSIONING_RESULT.zip'))
    zr1,nr1=verify_zip(z1.read('approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip'),'FIRST_COMMISSIONING_LAUNCH_PACKET/')
    for folder in (R1,R2):
        fm=json.loads((folder/'FILE_MANIFEST.json').read_bytes())
        for n,v in fm['files'].items():assert sha(folder/n)==v['sha256'] and (folder/n).stat().st_size==v['bytes']
    runtime_files=[p for folder in ('loom_p','loom_commissioning') for p in (D/folder).iterdir() if p.suffix in ('.py','.html')]+[D/'configuration.json',D/'requirements-lock.txt']
    sources={n:R2/'references'/n for n in ('00_LOOM_CURRENT_STATE.md','P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md','P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md','P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md','DECISION-P-APPARATUS-SCOPE-2026-09-24-73c9ad61.md','LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md','V3_RESULT_v1_1.json','V3_READ_ONLY_REANALYSIS_REPORT.md','VIEWER_DATA_FLOW.md')}
    sources.update({'A3_PREPARATION_REQUEST.txt':pathlib.Path(r'C:\Users\Jason\.codex\attachments\a93d9e6b-e674-4599-ac26-e549e323aa8e\Pasted text.txt'),
        'WORKBENCH_AGENTS.md':WB/'AGENTS.md','WORKBENCH_MAP.md':WB/'00_RESEARCH_MAP.md','WORKBENCH_STATUS.md':WB/'01_WORKSPACE_STATUS.md',
        'A2_COMMISSIONING_RESULT.zip':A2ZIP,'A1_BUDGET_MEASUREMENTS.json':R2/'BUDGET.json','A1_PLANNING_EVIDENCE.json':R2/'A1_PLANNING_EVIDENCE.json',
        'A2_RESOURCE_RESULT.json':A2DEL/'A2_COMMISSIONING_RESULT/RESOURCE_RESULT.json'})
    for n in ('A2_PLAIN_LANGUAGE_RESULT.md','A2_COMMISSIONING_REPORT.md','A2_OBSERVATIONS.json','TIMING_REPORTING_NOTE.json','ANALYSIS_RESULT.json','RECORD_INTEGRITY.json'):
        sources[n]=A2DEL/'A2_COMMISSIONING_RESULT/evidence/read-only-review'/n
    preserve_dirs=[CACHE,R1,R2,D/'artifacts/first-commissioning-A1-20260925-5f077481',D/'artifacts/commissioning-A2-20260925-5f077481']
    preserved=set(runtime_files)|set(sources.values())|{p for folder in preserve_dirs for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    before={str(p):sha(p) for p in sorted(preserved)}
    OUT.mkdir(parents=True,exist_ok=False)
    probe=OUT/'access-check.tmp';probe.write_bytes(b'A3 packet preparation only');assert probe.read_bytes()==b'A3 packet preparation only';probe.unlink()
    write('HASH_BEFORE.json',before)
    identities={}
    for n,p in sources.items():
        cp(p,'references/'+n);identities[n]={'source_path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    write('SOURCE_IDENTITIES.json',identities)
    for n in ('PROCEDURES.md','INTERPRETATION.md','build_packet.py','validate_packet.py'):cp(S/n,n)
    for p in runtime_files:cp(p,'instrument/developmental_ecology/'+p.relative_to(D).as_posix())
    for p in CACHE.rglob('*'):
        if p.is_file():cp(p,'verified-cache/'+p.relative_to(CACHE).as_posix())
    e=load_snapshot(R1/'INITIAL_A1.snapshot.json.gz') # __new__/unpack, no Engine constructor or RNG
    assert e.time==e.native_index==0 and e.status=='paused' and e.body.energy==.7 and e.body.integrity==1.
    assert e.body.position.tolist()==[6.,3.] and e.body.angle==math.pi
    assert state_hash(e)=='37adf68654e324141c678316f0f1f4b777853948e548cdd0d133e810c8722a6b'
    oldattrs={k:state_hash(v) for k,v in vars(e).items()}
    oldbody=copy.deepcopy(vars(e.body));oldprovenance=copy.deepcopy(e.birth_provenance)
    inactive=state_hash(e.organism);rng=copy.deepcopy(e.organism.rng.counters)
    e.body.position=np.array([2.5,6.])
    e.raw=transduce(e.c,e.body,e.fields,e.time,e.phase) # instantaneous deterministic fixture authoring only
    e.birth_provenance={'kind':'manufactured_external_geometry_start','lawful_newborn_sample':False,
        'position':[2.5,6.],'angle':math.pi,'phase':e.phase,'constructor_origin_retained':oldprovenance['constructor_origin_retained'],
        'fixture_parent_snapshot_sha256':sha(R1/'INITIAL_A1.snapshot.json.gz'),
        'description':'A3 healthy external fixture; only initial body position and instantaneous raw sensors changed from A1 zero-time state; original inactive organism/RNG retained. No prior trajectory state used.'}
    e.validate_state()
    changed=[k for k,v in vars(e).items() if state_hash(v)!=oldattrs[k]]
    assert sorted(changed)==['birth_provenance','body','raw']
    for k,v in vars(e.body).items():
        if k!='position':assert state_hash(v)==state_hash(oldbody[k]),k
    assert state_hash(e.organism)==inactive and e.organism.rng.counters==rng
    snap=save_snapshot(OUT/'INITIAL_A3.snapshot.json.gz',e)
    assert state_hash(load_snapshot(OUT/'INITIAL_A3.snapshot.json.gz'))==state_hash(e)
    init=copy.deepcopy(json.loads((R2/'A2_MANIFEST.json').read_bytes())['initialization'])
    assert digest(e.fields.tobytes())==init['field_sha256'] and e.phase==init['phase']
    cr=json.loads((CACHE/'manifest.json').read_bytes())
    assert sha(CACHE/'manifest.json')==init['cache_receipt_sha256'] and cr['phase']==e.phase and cr['status']=='complete' and cr['steps_completed']==60000
    assert sha(CACHE/'fields.npz')==cr['file_sha256']
    cfg=json.loads((D/'configuration.json').read_bytes());assert all(cfg[k]==v for k,v in cr['law'].items())
    with np.load(CACHE/'fields.npz',allow_pickle=False) as f:assert f['fields'].tobytes()==e.fields.tobytes()
    summary={'label':'A3 proposed healthy manufactured external fixture, not newborn or continuation','snapshot_name':'INITIAL_A3.snapshot.json.gz',
        'body':view(vars(e.body)),'stocks':e.stocks.tolist(),'time':e.time,'native_index':e.native_index,'status':e.status,
        'mover_phase':e.phase,'field_sha256':digest(e.fields.tobytes()),'initialization':init,
        'state_sha256':state_hash(e),'snapshot_sha256':snap['sha256'],'inactive_organism_sha256':inactive,'rng_counters':rng,
        'birth_provenance':e.birth_provenance,'parent_A1_zero_time_provenance':oldprovenance,
        'changed_engine_attributes':changed,'changed_body_attributes':['position'],'all_other_engine_body_attributes_identical':True,
        'fresh_session':{'cursor':0,'hold_remaining':0,'decision':None,'own_commands':[]},
        'time_zero_sensor_recomputations':1,'world_steps':0,'new_prehistory_steps':0,'neural_steps':0,'simulation_RNG_draws':0}
    write('INITIAL_STATE_SUMMARY.json',summary)
    scene=[]
    for i,(axis,sign,boundary) in enumerate(((0,1,0),(0,-1,20),(1,1,0),(1,-1,20))):scene.append({'id':f'wall-{i}','kind':'wall','axis':axis,'sign':sign,'boundary':boundary})
    for i,p in enumerate(cfg['source_positions']):scene.append({'id':f'source-{i}','kind':'disk','centre':p,'radius':cfg['source_radius']})
    for i,p in enumerate(cfg['repair_rectangles']):scene.append({'id':f'repair-{i}','kind':'rect','rect':p})
    cx,cy=cfg['mover_centre'];mw,mh=cfg['mover_size'];amp=cfg['mover_amplitude']
    swept={'kind':'rect','rect':[cx-amp-mw/2,cx+amp+mw/2,cy-mh/2,cy+mh/2]}
    geo={'body_radius':cfg['body_radius'],'all_static_fixtures':scene,'mover_swept_rectangle':swept['rect'],
        'segments':{},'scope':'Axis-aligned nominal finite-body paths only. No executed or predicted controller trajectory; actual deviations untested.'}
    segments=[('damage_approach',[2.5,6.],[.5,6.]),('wall_release',[.5,6.],[1.5,6.]),('corridor',[1.5,6.],[1.5,10.]),('repair_approach',[1.5,10.],[.75,10.]),('repair_release',[.75,10.],[1.5,10.]),('energy_approach',[1.5,10.],[2.,10.])]
    for n,a,b in segments:
        gaps={f['id']:segment_gap(a,b,f,cfg['body_radius']) for f in scene}
        assert min(gaps.values())>=-cfg['geometry_tol']
        geo['segments'][n]={'from':a,'to':b,'length':math.dist(a,b),'surface_clearances':gaps,'mover_union_clearance':segment_gap(a,b,swept,cfg['body_radius'])}
    write('GEOMETRY.json',geo)
    b1=json.loads((R2/'BUDGET.json').read_bytes());a1=b1['a1_measured']
    a2=json.loads(z2.read('RESOURCE_RESULT.json'))
    rates={}
    for label,sim,wall,unc,stored in [('A1',a1['simulated_seconds'],a1['recorder_wall_seconds'],a1['uncompressed_stream_bytes'],a1['stored_trajectory_bytes_including_snapshots_and_receipt']),('A2',a2['simulated_seconds_recorded'],a2['recorder_wall_seconds'],a2['uncompressed_stream_bytes'],a2['stored_trajectory_bytes_including_snapshots_and_receipt'])]:
        rates[label]={'wall_seconds_per_simulated_second':wall/sim,'uncompressed_bytes_per_simulated_second':unc/sim,'stored_bytes_per_simulated_second':stored/sim,
            'projection_210_simulated_seconds':{'wall_seconds':210*wall/sim,'uncompressed_bytes':210*unc/sim,'stored_trajectory_bytes':210*stored/sim}}
    write('BUDGET.json',{'basis':'Immutable actual A1/A2 long-run receipts, not smoke timing; no new benchmark','A1_measured':a1,'A2_measured':a2,'rates':rates,
        'A1_tail_wall_seconds_per_simulated_second':b1['rates']['tail_wall_seconds_per_simulated_second'],
        'A1_tail_projection_seconds':210*b1['rates']['tail_wall_seconds_per_simulated_second'],
        'simulated_ceiling_seconds':210,'native_step_ceiling':21000,'command_decision_ceiling':2100,'runner_wall_ceiling_seconds':4200,
        'uncompressed_stream_ceiling_bytes':1500000000,'primary_analysis_delivery_disk_ceiling_bytes':3000000000,'free_disk_precondition_bytes':3000000000,
        'separate_read_only_reporting_ceiling_seconds':3600,'separate_reporting_world_steps':0,
        'wall_headroom_over_A1_tail_fraction':4200/(210*b1['rates']['tail_wall_seconds_per_simulated_second'])-1,
        'reserve_lower_envelope_no_intake':{'equation':'E >= 0.7 - 0.0025*t while viable','at_155':.7-.0025*155,'at_180':.7-.0025*180,'at_210':.7-.0025*210},
        'ideal_repair_illustration_only':{'force':.1,'relative_speed':0.,'quality':.3,'rate_constant_per_second':.006,'fraction_of_deficit_restored_in_70_seconds':-math.expm1(-.006*70)},
        'limitations':['Linear projections are not completion guarantees or storage bounds.','Sensor histories and snapshot overhead grow; A2 stored bytes per second exceeded A1.','Actual A3 mechanics/contact and host load may differ.','Storage guard counts uncompressed streams, not snapshots or delivery copies.','Guards check between native steps; final flush and one in-flight step may overrun nominal wall threshold.','No trial, route rehearsal, dynamic benchmark or parameter tuning occurred.']})
    a2obs=json.loads(z2.read('evidence/read-only-review/A2_OBSERVATIONS.json'))
    write('PLANNING_EVIDENCE.json',{'A1_source':'references/A1_PLANNING_EVIDENCE.json','A2_source':'references/A2_OBSERVATIONS.json',
        'A2_zip_sha256':sha(A2ZIP),'A2_authority':'229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007',
        'separation':'A1/A2 observations inform allowance and ordinary-impact choice only; no A3 outcome is observed.',
        'A2_reported_final_EI':[.7381512326543674,.9863441416153598],
        'A2_first_source_contact_s':6.31019048650431,'A2_second_source_contact_s':132.3764279535912,
        'A2_total_damage':.013655858384640111,'A2_repair':0,
        'selection_rule':'One ordinary wall impact below an existing strip; orthogonal nearby corridor; nearby existing source; selected before any A3 commands, without candidate trials.',
        'workbench_navigation_status':'Current map/status stops at A1/V3; latest explicit request and verified A2 result are later evidence. Navigation not edited.',
        'A2_boundary_reporting_limitation':'Preserve TIMING_REPORTING_NOTE.json; sub-tolerance nominal-boundary flags do not establish missing integration.'})
    ids=json.loads((R2/'CODE_AND_RUNTIME_IDENTITIES.json').read_bytes())
    assert ids['P']==code_identity() and ids['apparatus']==contract.apparatus_identity()
    write('CODE_AND_RUNTIME_IDENTITIES.json',ids)
    m=copy.deepcopy(json.loads((R2/'A2_MANIFEST.json').read_bytes()))
    m.update(case_id='A3',initial_state=state_hash(e),duration_seconds=210.,hard_stop_time=210.,execution_authority=None)
    m['execution']['procedure']['stages']=PLAN
    m['execution']['resources']={'storage_limit_bytes':1500000000,'wall_limit_seconds':4200}
    rec=copy.deepcopy(m['execution']['procedure']['protocol']['recording_contract'])
    rec['post_read']='Saved-data-only identity, continuity, ledger and issued-versus-delivered validation; all milestone reserves per INTERPRETATION.md. No replay or controller recomputation.'
    bound=['PROCEDURES.md','INTERPRETATION.md','build_packet.py','validate_packet.py','SOURCE_IDENTITIES.json','INITIAL_STATE_SUMMARY.json','GEOMETRY.json','BUDGET.json','PLANNING_EVIDENCE.json','CODE_AND_RUNTIME_IDENTITIES.json']
    m['execution']['procedure']['protocol']={
        'packet_label':'A3 actual-damage / repair / energy — PROPOSED / NOT AUTHORIZED','reviewed_checkpoints':{'p_git_sha':P,'apparatus_git_sha':APP},'case_count':1,
        'prior_evidence_status':{'V1':'COMPLETE','V2':'COMPLETE','V3':'COMPLETE by read-only reanalysis','A0':'COMPLETE','A1':'one external physical witness OBSERVED','A2':'one external physical witness OBSERVED'},
        'bound_files':{n:sha(OUT/n) for n in bound},'initial_snapshot_file':{'name':'INITIAL_A3.snapshot.json.gz','sha256':snap['sha256']},
        'fixture_label':'Healthy manufactured external geometry start; not newborn, not A1/A2 continuation; no initialized damage',
        'damage_target':'wall-0 x=0 around y=6; one initial approach, no target integrity',
        'repair_target':'repair-0 rectangle [0,0.25] x [8,12], interior face around y=10',
        'energy_target':'source-3 centre (3,10), approach from left',
        'timing_interpretation':'Fixed-clock phases, no damage or repair-triggered transition. Complete chain requires positive repair before actual departure; otherwise report incomplete chain, with no extension or feedback.',
        'recording_contract':rec,'record_destination':str(DEST),'analysis_destination':str(DEST.parent/'read-only-review'),
        'launch_operations':['Separate genuine Jason approval of this exact object','verify bound files/live identities/cache/snapshot and empty destination','one fresh unchanged Run/passive observer under typed prescription','ordinary holds until first stop, no manual commands','preserve and report from saved records only; no retry, resume or patch'],
        'stop_names':['terminal','apparatus_failure','administrative_pause','administrative_cutoff'],
        'failure_rule':'Report all outcomes without repair, route replacement, horizon extension, outcome-selected continuation or extra case.',
        'continuity_rule':'Retain all actual E/I, stocks, fields, clock and mechanical/controller history throughout; no midtrajectory reset.',
        'component_allowance':{'machine_seconds':3600,'world_steps':0,'scope':'Read-only identity, record validation, reporting and packaging only; no dynamic probes, command recomputation or replay'},
        'disk_bytes_for_primary_analysis_and_copy':3000000000,
        'excluded_cases':['manufactured low-E/I A3 arm','A1 repeat','A2 repeat','A4','A5','B1','B2','B3','B4','C1','C2','newborn lives','fixed-structure diagnostic','scientific tests','new prehistory','sweeps'],
        'legacy_roster_note':'Mandatory roster remains execution_authorized=false; no births proposed.'}
    authority.validate_execution(m,complete=True);authority.validate_dispatch(m,vars(runner))
    try:contract.authorize_execution(m)
    except ValueError as ex:assert str(ex)=='commissioning execution is not authorized';denial=str(ex)
    else:raise AssertionError('Null grant accepted')
    write('A3_MANIFEST.json',m)
    obj=authority.execution_object(m);canonical=authority.canonical(obj);h=authority.execution_sha256(m)
    write('AUTHORITY_OBJECT.json',obj);(OUT/'AUTHORITY_OBJECT.canonical.json').write_bytes(canonical)
    (OUT/'AUTHORITY_SHA256.txt').write_text(h+'  AUTHORITY_OBJECT.canonical.json\n',encoding='utf-8')
    assert not BLOCKED and COUNTS=={'load_snapshot':2,'transduce':1,'save_snapshot':1}
    write('PREPARATION_CHECKS.json',{'scope':'Static identity/saved-state/geometry and one instantaneous time-zero transduction only; no A3 dynamics or commands',
        'verified_nested_payload_counts':{'A2_result':n2,'A2_launch':nr2,'A1_result':n1,'A1_launch':nr1},
        'snapshot_roundtrip_valid':True,'healthy_EI':[.7,1.],'cache_fields_exact_match':True,'cache_phase_receipt_and_law_valid':True,
        'inactive_organism_and_RNG_unchanged':True,'only_selected_fixture_attributes_changed':True,
        'live_runtime_controller_dispatch_valid':True,'complete_manifest_execution_structure_valid':True,'null_grant_rejected':denial,
        'deadlines_on_0_1_and_0_2_grids':all(abs(p['until']/.2-round(p['until']/.2))<1e-8 for p in PLAN),
        'nominal_geometric_segments_nonpenetrating':True,'prospective_execution_destination_absent':not DEST.parent.exists(),
        'Engine_constructor_calls':0,'Run_constructor_calls':0,'computed_controller_commands':0,'world_steps':0,'field_steps':0,'neural_steps':0,'simulation_RNG_draws':0,'new_prehistory_steps':0,'replays':0,
        'allowed_snapshot_and_static_transduction_calls':COUNTS,'blocked_dynamic_calls':BLOCKED,
        'preparation_limitation':'No controller competence, actual wall damage, repair, energy arrival or performance result has been tested. Production validate_manifest/history check remains a launch preflight after separate approval.',
        'preparation_wall_seconds':time.perf_counter()-started})
    after={p:sha(p) for p in before};assert before==after
    assert not git('status','--porcelain').strip() and git('rev-parse','HEAD').decode().strip()==APP
    write('HASH_AFTER.json',after)
    write('PRESERVATION.json',{'files_checked':len(before),'all_original_hashes_unchanged':True,'code_changes':0,'configuration_changes':0,'Git_writes':0,'vault_Git_writes':0,'new_commit':None,'authority_status':'PROPOSED / NOT AUTHORIZED','A3_execution_occurred':False})
    print(json.dumps({'output':str(OUT),'authority_sha256':h,'world_steps':0,'controller_commands':0,'time_zero_transduction':1,'grant':None},indent=2))

if __name__=='__main__':main()
