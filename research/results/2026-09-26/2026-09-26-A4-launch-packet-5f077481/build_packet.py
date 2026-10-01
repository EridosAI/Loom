"""A4 proposal authoring only; no trajectory, controller, RNG or prehistory execution."""
import copy,hashlib,io,json,math,os,pathlib,shutil,subprocess,sys,time,zipfile
S=pathlib.Path(__file__).resolve().parent; ROOT=S.parent
OUT=ROOT/'exports/2026-09-26-A4-launch-packet-5f077481'
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405'); D=W/'developmental_ecology'
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
R1=ROOT/'exports/2026-09-25-first-commissioning-launch-packet-5f077481'
R2=ROOT/'exports/2026-09-25-A2-launch-packet-5f077481'
R3=ROOT/'exports/2026-09-25-A3-launch-packet-5f077481'
A2=ROOT/'exports/2026-09-25-A2-commissioning-result-5f077481/A2_COMMISSIONING_RESULT'
A3=ROOT/'exports/2026-09-26-A3-commissioning-result-5f077481/A3_COMMISSIONING_RESULT'
A3ZIP=A3.parent/'A3_COMMISSIONING_RESULT.zip'
CACHE=D/'artifacts/prehistory-attempt-001'
DEST=D/'artifacts/commissioning-A4-20260926-5f077481'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'; APP='5f07748102cb5eaa302569c87efbae095050e9fe'
PHASE=3.558411277237072
CASES=[('A4-CROSS',[10.,8.8],[10.,12.],16.,0.,480),('A4-WAIT',[6.,8.8],[6.,12.],28.,12.,780),('A4-DETOUR',[1.5,6.],[1.5,14.],32.,0.,840)]
COUNTS={}; BLOCKED=[]
def guard(frame,event,arg):
    if event!='call':return
    f=frame.f_code; p=f.co_filename.replace('\\','/')
    if '/loom_p/' in p or '/loom_commissioning/' in p:
        bad=f.co_name in {'step','advance','account','prepare','waypoint_command','native','handoff','draw','_coupled','coupled','begin_command','hold','resume','from_verified_cache','load_restart','free_velocity','actuator_forces'}
        bad |= f.co_name=='__init__' and p.endswith(('/engine.py','/runner.py','/neural.py','/schema.py'))
        if bad:
            BLOCKED.append(p+':'+f.co_name);raise AssertionError('A4 preparation forbids: '+BLOCKED[-1])
        if f.co_name in {'transduce','load_snapshot','save_snapshot'}:COUNTS[f.co_name]=COUNTS.get(f.co_name,0)+1
sys.setprofile(guard);sys.path.insert(0,str(D))
from loom_commissioning import authority,contract,runner
from loom_p.records import code_identity,load_snapshot,save_snapshot,state_hash,view
from loom_p.geometry import transduce
import numpy as np
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def write(n,v):
    p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(view(v),ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def cp(p,n):
    q=OUT/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(S/'empty-excludes').as_posix(),'-C',str(W),*args],env=env)
def zipcheck(raw,prefix=''):
    z=zipfile.ZipFile(io.BytesIO(raw));fm=json.loads(z.read(prefix+'FILE_MANIFEST.json'))
    assert set(z.namelist())=={prefix+n for n in fm['files']}|{prefix+'FILE_MANIFEST.json'}
    for n,v in fm['files'].items():
        b=z.read(prefix+n);assert len(b)==v['bytes'] and digest(b)==v['sha256'],n
    return z,len(fm['files'])
def gap(a,b,f,r):
    if f['kind']=='disk':
        v=[b[i]-a[i] for i in range(2)];den=sum(x*x for x in v)
        u=max(0,min(1,sum((f['centre'][i]-a[i])*v[i] for i in range(2))/den))
        return math.hypot(*(a[i]+u*v[i]-f['centre'][i] for i in range(2)))-r-f['radius']
    if f['kind']=='wall':return min(f['sign']*(a[f['axis']]-f['boundary'])-r,f['sign']*(b[f['axis']]-f['boundary'])-r)
    lo=[min(a[i],b[i]) for i in range(2)];hi=[max(a[i],b[i]) for i in range(2)]
    x0,x1,y0,y1=f['rect'];dx=max(x0-hi[0],lo[0]-x1,0);dy=max(y0-hi[1],lo[1]-y1,0)
    return math.hypot(dx,dy)-r
def main():
    started=time.perf_counter();assert not OUT.exists() and not DEST.exists()
    assert git('rev-parse','HEAD').decode().strip()==APP and not git('status','--porcelain').strip()
    assert code_identity()['sha256']==contract.P_CODE
    assert contract.apparatus_identity()['sha256']=='d5801b69ae38d3259f3426aed8753fef8d76132a2f4ffecdd9baffb29afeb71a'
    for p in (D/'loom_p').glob('*.py'):assert p.read_bytes()==git('show',P+':developmental_ecology/loom_p/'+p.name)
    assert (D/'configuration.json').read_bytes()==git('cat-file','--filters',P+':developmental_ecology/configuration.json')
    assert sha(A3ZIP)=='083ec15d6fc702d75d26e5b3783ab4a4f0292a8dbf83de21bf26f8df0f9db474'
    z3,n3=zipcheck(A3ZIP.read_bytes());zr3,nr3=zipcheck(z3.read('approved-launch/A3_LAUNCH_PACKET.zip'),'A3_LAUNCH_PACKET/')
    z2,n2=zipcheck(zr3.read('A3_LAUNCH_PACKET/references/A2_COMMISSIONING_RESULT.zip'))
    zr2,nr2=zipcheck(z2.read('approved-launch/A2_LAUNCH_PACKET.zip'),'A2_LAUNCH_PACKET/')
    z1,n1=zipcheck(zr2.read('A2_LAUNCH_PACKET/references/FIRST_A1_COMMISSIONING_RESULT.zip'))
    zr1,nr1=zipcheck(z1.read('approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip'),'FIRST_COMMISSIONING_LAUNCH_PACKET/')
    for folder in (R1,R2,R3):
        fm=json.loads((folder/'FILE_MANIFEST.json').read_bytes())
        for n,v in fm['files'].items():assert sha(folder/n)==v['sha256'] and (folder/n).stat().st_size==v['bytes']
    runtime_files=[p for f in ('loom_p','loom_commissioning') for p in (D/f).iterdir() if p.suffix in ('.py','.html')]+[D/'configuration.json',D/'requirements-lock.txt']
    source_names=['00_LOOM_CURRENT_STATE.md','P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md','P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md','P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md','DECISION-P-APPARATUS-SCOPE-2026-09-24-73c9ad61.md','LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md','V3_RESULT_v1_1.json','V3_READ_ONLY_REANALYSIS_REPORT.md','VIEWER_DATA_FLOW.md']
    sources={n:R3/'references'/n for n in source_names}
    sources.update({'A0_GEOMETRY.json':R1/'A0_GEOMETRY.json','A3_COMMISSIONING_RESULT.zip':A3ZIP,'A2_RESOURCE_RESULT.json':A2/'RESOURCE_RESULT.json','A3_RESOURCE_RESULT.json':A3/'RESOURCE_RESULT.json','A3_PLAIN_LANGUAGE_RESULT.md':A3/'evidence/read-only-review/A3_PLAIN_LANGUAGE_RESULT.md','CONTACT_INTERRUPTION_NOTE.md':A3/'evidence/read-only-review/CONTACT_INTERRUPTION_NOTE.md','WORKBENCH_AGENTS.md':WB/'AGENTS.md','WORKBENCH_MAP.md':WB/'00_RESEARCH_MAP.md','WORKBENCH_STATUS.md':WB/'01_WORKSPACE_STATUS.md','PROJECT_AGENTS.md':ROOT/'AGENTS.md','INITIAL_A1.snapshot.json.gz':R1/'INITIAL_A1.snapshot.json.gz'})
    assert (A2/'RESOURCE_RESULT.json').read_bytes()==z2.read('RESOURCE_RESULT.json')
    assert (A3/'RESOURCE_RESULT.json').read_bytes()==z3.read('RESOURCE_RESULT.json')
    assert sources['A0_GEOMETRY.json'].read_bytes()==zr1.read('FIRST_COMMISSIONING_LAUNCH_PACKET/A0_GEOMETRY.json')
    preserved=set(runtime_files)|set(sources.values())|{p for folder in (CACHE,R1,R2,R3,D/'artifacts/first-commissioning-A1-20260925-5f077481',D/'artifacts/commissioning-A2-20260925-5f077481',D/'artifacts/commissioning-A3-20260925-5f077481') for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    before={str(p):sha(p) for p in sorted(preserved)}
    OUT.mkdir(parents=True);probe=OUT/'access-check.tmp';probe.write_bytes(b'A4 preparation only');assert probe.read_bytes()==b'A4 preparation only';probe.unlink()
    write('HASH_BEFORE.json',before)
    ids={}
    for n,p in sources.items():cp(p,'references/'+n);ids[n]={'source_path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    write('SOURCE_IDENTITIES.json',ids)
    docs=['PROCEDURES.md','INTERPRETATION.md','BATCH_EXECUTION_RULES.md','VIEWER_RECORD_CONTRACT.md','A4_PREPARATION_REQUEST.txt','build_packet.py','validate_packet.py']
    for n in docs:cp(S/n,n)
    for p in runtime_files:cp(p,'instrument/developmental_ecology/'+p.relative_to(D).as_posix())
    for p in CACHE.rglob('*'):
        if p.is_file():cp(p,'verified-cache/'+p.relative_to(CACHE).as_posix())
    cfg=json.loads((D/'configuration.json').read_bytes());init=copy.deepcopy(json.loads((R3/'A3_MANIFEST.json').read_bytes())['initialization'])
    cr=json.loads((CACHE/'manifest.json').read_bytes())
    assert sha(CACHE/'manifest.json')==init['cache_receipt_sha256'] and cr['phase']==PHASE and cr['status']=='complete' and cr['steps_completed']==60000
    assert sha(CACHE/'fields.npz')==cr['file_sha256'] and all(cfg[k]==v for k,v in cr['law'].items())
    # These exact cache bytes were already dependency-verified and used by A1/A2/A3.
    assert init==json.loads((R2/'A2_MANIFEST.json').read_bytes())['initialization']
    scene=[]
    for i,(axis,sign,boundary) in enumerate(((0,1,0),(0,-1,20),(1,1,0),(1,-1,20))):scene.append({'id':f'wall-{i}','kind':'wall','axis':axis,'sign':sign,'boundary':boundary})
    for i,p in enumerate(cfg['source_positions']):scene.append({'id':f'source-{i}','kind':'disk','centre':p,'radius':cfg['source_radius']})
    for i,p in enumerate(cfg['repair_rectangles']):scene.append({'id':f'repair-{i}','kind':'rect','rect':p})
    assert cfg['mover_centre']==[10.,10.] and cfg['mover_size']==[2.,1.] and cfg['mover_amplitude']==4 and cfg['mover_period']==30 and cfg['body_radius']==.5
    swept={'kind':'rect','rect':[5.,15.,9.5,10.5]};omega=2*math.pi/30
    left_conflict_start=(math.pi+math.asin(.625)-PHASE)/omega
    left_conflict_end=(2*math.pi-math.asin(.625)-PHASE)/omega
    cross_clear_end=(2*math.pi-math.asin(.375)-PHASE)/omega
    mover=lambda t:10+4*math.sin(omega*t+PHASE)
    geo={'scope':'Static axis-aligned body-centre segments and analytic sine/time inequalities only; no dynamics or control calls, no sampled candidate runs.',
      'body_radius':.5,'phase':PHASE,'mover_law':{'centre':[10,10],'amplitude':4,'period':30,'size':[2,1]},'static_fixtures':scene,'mover_swept_rectangle':swept['rect'],'segments':{},
      'CROSS':{'nominal_x':10,'clear_for_all_y_start':0,'clear_for_all_y_end_exclusive':cross_clear_end,'reason':'mover right edge < 9.5 until its return; radius-0.5 body at x=10 is horizontally clear',
        'analytic_conditional_exit_bound_s':10,'minimum_drive_before_exit':.348,'energy_lower_bound_through_t10':.675,'forward_force_lower_bound':.25752,'distance_lower_bound_at_t10_if_not_exited':.25752*(10-1+math.exp(-10))},
      'WAIT':{'nominal_x':6,'horizontal_conflict_interval':[left_conflict_start,left_conflict_end],'release_at':12,'next_horizontal_conflict_at':left_conflict_start+30,'stationary_minimum_mover_gap':.2,
        'immediate_proceed_argument':{'counterfactual_executed':False,'time_used_for_contradiction':3,'mover_rect_at_t3':[mover(3)-1,mover(3)+1,9.5,10.5],
          'no_contact_speed_upper_bound':.38,'no_contact_displacement_upper_bound':1.14,'minimum_distance_to_destination_through_t3':2.06,
          'drive_lower_unclipped':.5*2.06-.4*.38,'therefore_saturated_drive':.5,'conservative_forward_force_lower_bound':.376,
          'speed_lower_bound_after_t1':.376*(1-math.exp(-1)),'displacement_lower_bound_over_t1_to_t3':2*.376*(1-math.exp(-1)),
          'body_centre_y_interval_at_t3_under_no_contact_assumption':[8.8+2*.376*(1-math.exp(-1)),8.8+1.14],
          'conclusion':'At t=3 mover rectangle contains x=6; the no-contact y bounds force disk overlap. Thus immediate northward progress must conflict before/by 3 s. This is an analytic contradiction using unchanged saturated actuator/drag laws, not an executed comparison.'},
        'analytic_conditional_exit_bound_absolute_s':22,'minimum_drive_before_exit':.348,'energy_lower_bound_through_t22':.645,'forward_force_lower_bound':.249168,'distance_lower_bound_over_10s_if_not_exited':.249168*(10-1+math.exp(-10))},
      'bound_derivation':'Until northward centre y=11, destination distance >=1 and speed <=0.38, so drive >=0.5-0.4*0.38=0.348. No-contact healthy symmetric forces have zero torque. Reserve bound E>=0.7-0.0025*t gives the stated force floors. Unit-mass/unit-drag v>=Fmin*(1-exp(-elapsed)); the existing positive-acceleration endpoint-position update has a right-sum displacement no smaller than the integral. Both ten-second lower distances exceed the required 2.2 m and fall inside their clear intervals. These ideal symmetric analytic opportunity bounds are not executed controller-competence or floating-contact certification.',
      'detour_reference':'A0_GEOMETRY.json / A0_only_left_bypass, exact endpoints retained','detour_corridor_half_width':.25,
      'detour_corridor_static_margin_lower_bound':.25,'detour_corridor_mover_union_margin_lower_bound':2.75,
      'selected_without_trials':True,'candidate_trajectory_count':0,'limitations':['Nominal paths do not assert actual realized paths.','Full fixed-ceiling outcomes, damage, timing misses and controller limits remain unobserved.','Rounded decimal bounds are conservative; actual floating contact behavior is left to the authorized record.']}
    assert cross_clear_end>10 and left_conflict_end<12 and left_conflict_start+30>22
    assert geo['CROSS']['distance_lower_bound_at_t10_if_not_exited']>2.2 and geo['WAIT']['distance_lower_bound_over_10s_if_not_exited']>2.2
    for cid,a,b,dur,wait,wall in CASES:
        gaps={f['id']:gap(a,b,f,.5) for f in scene};assert min(gaps.values())>0
        geo['segments'][cid]={'from':a,'to':b,'nominal_length':math.dist(a,b),'static_surface_clearances':gaps,'crosses_mover_swept_region':cid!='A4-DETOUR'}
    bypass=json.loads((R1/'A0_GEOMETRY.json').read_bytes())['A0_only_left_bypass'];det=geo['segments']['A4-DETOUR']
    assert det['from']==bypass['from'] and det['to']==bypass['to']
    assert all(abs(v-bypass['static_surface_clearances'][k])<1e-12 for k,v in det['static_surface_clearances'].items())
    det['mover_union_clearance']=gap(det['from'],det['to'],swept,.5);assert det['mover_union_clearance']==bypass['minimum_to_mover_union_over_all_phases']==3
    write('GEOMETRY_AND_TIMING.json',geo)
    measured={'A2':json.loads(z2.read('RESOURCE_RESULT.json')),'A3':json.loads(z3.read('RESOURCE_RESULT.json'))};rates={}
    for label,r in measured.items():
        t=r['simulated_seconds_recorded'];rates[label]={'recorder_wall_seconds_per_sim_second':r['recorder_wall_seconds']/t,'whole_process_wall_seconds_per_sim_second':r['whole_process_wall_seconds']/t,'uncompressed_bytes_per_sim_second':r['uncompressed_stream_bytes']/t,'stored_bytes_per_sim_second':r['stored_trajectory_bytes_including_snapshots_and_receipt']/t}
    def projection(rr,seconds):
        return {'recorder_wall_seconds':seconds*rr['recorder_wall_seconds_per_sim_second'],
                'whole_process_wall_seconds':seconds*rr['whole_process_wall_seconds_per_sim_second'],
                'uncompressed_stream_bytes':seconds*rr['uncompressed_bytes_per_sim_second'],
                'stored_trajectory_bytes':seconds*rr['stored_bytes_per_sim_second']}
    projections={}
    for cid,a,b,dur,wait,wall in CASES:
        projections[cid]={'simulated_seconds':dur,'native_steps':round(100*dur),'command_decisions':round(10*dur),'wall_cap_seconds':wall,'uncompressed_stream_cap_bytes':100000000,
          'by_measured_case':{label:projection(rr,dur) for label,rr in rates.items()},'reserve_lower_bound_no_intake':.7-.0025*dur}
    write('RESOURCE_PROJECTION.json',{'basis':'Actual sealed A2 and A3 long-run results; no new benchmark. Decimal bytes/MB. Linear projections are estimates, not physical outcomes or completion guarantees.',
      'measurements':measured,'rates':rates,'per_case':projections,'total_simulated_seconds':76,'total_native_steps':7600,'total_command_decisions':760,
      'total_by_measured_case':{label:projection(rr,76) for label,rr in rates.items()},
      'total_runner_wall_cap_seconds':2100,'total_read_only_reporting_cap_seconds':600,'total_combined_wall_allowance_seconds':2700,
      'combined_disk_cap_bytes':3000000000,'free_disk_precondition_bytes':3000000000,'sum_uncompressed_stream_caps_bytes':300000000,
      'historical_review_archive_bytes':A3ZIP.stat().st_size,'estimated_launch_packet_bytes':160000000,'estimated_result_bundle_including_launch_bytes':200000000,
      'storage_plan':'At worst measured trajectory rate about 29.6 MB for the new three records, about 44.7 MB uncompressed. Launch review carries about 155 MB of immutable nested prior evidence; allow about 160 MB launch and 200 MB result per copy, plus raw/analysis. All copies share the declared 3 GB cap. Three fresh starts add overhead that linear per-second extrapolation does not resolve.',
      'limitations':['Mover contact complexity and host load may differ from A2/A3.','Short fresh runs have startup/snapshot overhead; do not claim the measured rates are guaranteed.','Full native/sensor/contact/snapshot fidelity remains unchanged.','Recorder storage guard counts uncompressed streams plus a reserve, not all files.','Native-step wall guards and flushes may slightly exceed nominal caps; no continuation afterward.']})
    identities={'P':code_identity(),'apparatus':contract.apparatus_identity(),'runtime':authority.runtime_identity(),'configuration_semantic_sha256':contract.CONFIG,'configuration_file_sha256':sha(D/'configuration.json'),'p_commit':P,'apparatus_commit':APP,'branch':git('branch','--show-current').decode().strip(),'git_version':subprocess.check_output(['git','--version']).decode().strip(),'executable':sys.executable,'worktree':str(W)}
    assert identities['runtime']==json.loads((R3/'A3_MANIFEST.json').read_bytes())['execution']['runtime']
    write('CODE_AND_RUNTIME_IDENTITIES.json',identities)
    write('PLANNING_EVIDENCE.json',{'completed_physical_rows':['A0','A1','A2','A3'],'prior_archive_sha256':sha(A3ZIP),'verified_nested_payload_counts':{'A3_result':n3,'A3_launch':nr3,'A2_result':n2,'A2_launch':nr2,'A1_result':n1,'A1_launch':nr1},'navigation_status':'Workbench navigation was last updated through A2 and still described A3 as unexecuted. The later sealed A3 result and explicit current user request establish completion. No navigation file is altered.','scope':'Past measurements set resource projections. A0 supplies the exact bypass. No prior P efficacy or new simulated trajectory selects starts/phases/routes. Historical acceptance documents remain attributed, not relabelled as execution authority.'})
    common=docs+['SOURCE_IDENTITIES.json','GEOMETRY_AND_TIMING.json','RESOURCE_PROJECTION.json','CODE_AND_RUNTIME_IDENTITIES.json','PLANNING_EVIDENCE.json']
    members=[];denials=[]
    for cid,a,b,dur,wait,wall in CASES:
        e=load_snapshot(R1/'INITIAL_A1.snapshot.json.gz');assert state_hash(e)=='37adf68654e324141c678316f0f1f4b777853948e548cdd0d133e810c8722a6b'
        old={k:state_hash(v) for k,v in vars(e).items()};oldbody=copy.deepcopy(vars(e.body));prov=copy.deepcopy(e.birth_provenance);inactive=state_hash(e.organism);rng=copy.deepcopy(e.organism.rng.counters)
        assert e.time==e.native_index==0 and e.status=='paused' and e.body.energy==.7 and e.body.integrity==1 and e.phase==PHASE
        e.body.position=np.array(a);e.body.angle=math.pi/2;e.raw=transduce(e.c,e.body,e.fields,e.time,e.phase)
        e.birth_provenance={'kind':'manufactured_external_geometry_start','lawful_newborn_sample':False,'case_label':cid,'position':a,'angle':math.pi/2,'phase':e.phase,'constructor_origin_retained':prov['constructor_origin_retained'],'fixture_parent_snapshot_sha256':sha(R1/'INITIAL_A1.snapshot.json.gz'),'description':'Independent healthy zero-time A4 external physical witness. Only initial position, heading, instantaneous sensors and provenance change; cached fields and inactive organism/RNG retained. No previous trajectory state or outcome used.'}
        e.validate_state();changed=sorted(k for k,v in vars(e).items() if state_hash(v)!=old[k]);assert changed==['birth_provenance','body','raw']
        for k,v in vars(e.body).items():
            if k not in ('position','angle'):assert state_hash(v)==state_hash(oldbody[k])
        assert state_hash(e.organism)==inactive and e.organism.rng.counters==rng and digest(e.fields.tobytes())==init['field_sha256']
        with np.load(CACHE/'fields.npz',allow_pickle=False) as f:assert f['fields'].tobytes()==e.fields.tobytes()
        snapname=f'cases/{cid}/INITIAL.snapshot.json.gz';(OUT/snapname).parent.mkdir(parents=True);snap=save_snapshot(OUT/snapname,e)
        assert state_hash(load_snapshot(OUT/snapname))==state_hash(e)
        summary=f'cases/{cid}/INITIAL_STATE_SUMMARY.json'
        write(summary,{'label':cid+' proposed independent manufactured external start, not newborn or continuation','body':vars(e.body),'time':e.time,'native_index':e.native_index,'status':e.status,'stocks':e.stocks,'mover_phase':e.phase,'initialization':init,'field_sha256':digest(e.fields.tobytes()),'state_sha256':state_hash(e),'snapshot_sha256':snap['sha256'],'inactive_organism_sha256':inactive,'rng_counters':rng,'birth_provenance':e.birth_provenance,'changed_engine_attributes':changed,'changed_body_attributes':['position','angle'],'all_other_body_engine_attributes_identical':True,'fresh_session':{'cursor':0,'hold_remaining':0,'decision':None,'own_commands':[]},'world_steps':0,'time_zero_sensor_recomputations':1})
        stages=([{'point':a,'until':wait,'press_force':0.}] if wait else [])+[{'point':b,'until':dur,'press_force':0.}]
        m=copy.deepcopy(json.loads((R3/'A3_MANIFEST.json').read_bytes()));m.update(case_id=cid,initial_state=state_hash(e),duration_seconds=dur,hard_stop_time=dur,execution_authority=None)
        m['execution']['procedure']['stages']=stages;m['execution']['resources']={'storage_limit_bytes':100000000,'wall_limit_seconds':wall}
        rec=copy.deepcopy(m['execution']['procedure']['protocol']['recording_contract']);rec['post_read']='Saved-data-only observations and byte/ledger/delivery checks per INTERPRETATION.md; no replay, command recomputation or new dynamics.'
        m['execution']['procedure']['protocol']={'packet_label':cid+' — PROPOSED / NOT AUTHORIZED','matrix_parent_row':'A4','batch_order':['A4-CROSS','A4-WAIT','A4-DETOUR'],'member_count':3,'reviewed_checkpoints':{'p_git_sha':P,'apparatus_git_sha':APP},'bound_files':{n:sha(OUT/n) for n in common+[summary]},'initial_snapshot_file':{'name':snapname,'sha256':snap['sha256']},'fixture_label':'Healthy independent manufactured external fixture; inactive retained organism; not a sampled newborn, P test or prior-case continuation','recording_contract':rec,'record_destination':str(DEST/cid/'trajectory-001'),'analysis_destination':str(DEST/'read-only-review'/cid),'physical_question':{'A4-CROSS':'Finite-body timed crossing of mover path','A4-WAIT':'Fixed 12-second actuator-interface wait followed by finite-body crossing','A4-DETOUR':'A0 declared always-clear left bypass'}[cid],'prescribed_wait_seconds':wait,'arrival_observation_radius_metres':.25,'stop_names':['terminal','apparatus_failure','administrative_pause','administrative_cutoff'],'failure_rule':'No retry, extension, resume, route/phase/controller substitution or patch. Whole batch stops on apparatus/preflight/resource/operator failure; a normal ceiling or bodily terminal may be followed only by the next untouched bound case.','continuity_rule':'All body/EI/stocks/fields/clock/controller history continues within this case. The next case is a separate prebound zero-time fixture, never a reset or rescue of this case.','viewer_rule':'Retain original native, event, sensor, controller sampled mover poses and restart records; no live renderer or feedback.','legacy_roster_note':'execution_authorized=false; no births, A5, B, C, D or other run proposed.'}
        authority.validate_execution(m,complete=True);authority.validate_dispatch(m,vars(runner))
        try:contract.authorize_execution(m)
        except ValueError as ex:assert str(ex)=='commissioning execution is not authorized';denials.append({'case':cid,'reason':str(ex)})
        else:raise AssertionError('Null grant accepted')
        name=f'cases/{cid}/MANIFEST.json';write(name,m);obj=authority.execution_object(m);canonical=authority.canonical(obj);h=digest(canonical)
        objectname=f'cases/{cid}/EXECUTION_OBJECT.canonical.json';(OUT/objectname).write_bytes(canonical)
        members.append({'case_id':cid,'manifest_file':name,'manifest_file_sha256':sha(OUT/name),'execution_object_file':objectname,'execution_sha256':h,'execution_object':obj})
    batch={'schema':'loom-A4-batch-authority-v1','status':'PROPOSED / NOT AUTHORIZED','purpose':'Three predetermined independent privileged external-controller physical opportunity witnesses; no P perception or learning test','p_commit':P,'apparatus_commit':APP,'case_order':[x[0] for x in CASES],'cases':members,
      'batch_limits':{'maximum_attempts_per_case':1,'maximum_Run_construction_attempts':3,'total_simulated_seconds':76,'total_native_steps':7600,'total_runner_wall_seconds':2100,'read_only_reporting_seconds':600,'combined_disk_bytes':3000000000,'free_disk_precondition_bytes':3000000000,'budget_transfer_between_cases':False},
      'execution_rules':{'order_fixed':True,'parallel_execution':False,'retry':False,'resume':False,'extension':False,'substitution':False,'tuning':False,'patching':False,'new_prehistory':False,'neural_execution':False,'live_renderer':False,'stop_remaining_on':['preflight_failure','apparatus_failure','unexpected_exception','resource_cutoff','operator_pause'],'continue_to_next_unchanged_case_after':['normal_declared_time_ceiling','physical_terminal_event']},
      'bound_documents':{n:sha(OUT/n) for n in common},'approval_workflow':'BATCH_EXECUTION_RULES.md; future genuine Jason batch approval may be represented by exact constituent approval envelopes for the unchanged single-case apparatus. This object itself creates no grant.'}
    write('AUTHORITY_OBJECT.json',batch);raw=authority.canonical(batch);(OUT/'AUTHORITY_OBJECT.canonical.json').write_bytes(raw);h=digest(raw)
    (OUT/'AUTHORITY_SHA256.txt').write_text(h+'  AUTHORITY_OBJECT.canonical.json\n',encoding='utf-8')
    assert COUNTS=={'load_snapshot':6,'transduce':3,'save_snapshot':3} and not BLOCKED and not DEST.exists()
    write('PREPARATION_CHECKS.json',{'scope':'Saved-state loading, three predetermined zero-time body/heading changes with instantaneous transduction, static geometry/closed-form timing, source/runtime/dispatch identities and null-grant rejection only.',
      'Engine_constructor_calls':0,'Run_constructor_calls':0,'computed_controller_commands':0,'world_steps':0,'field_steps':0,'neural_steps':0,'simulation_RNG_draws':0,'new_prehistory_steps':0,'replays':0,'trial_routes':0,'trial_phases':0,
      'allowed_static_calls':COUNTS,'blocked_dynamic_calls':BLOCKED,'null_grant_denials':denials,'full_production_history_validation_executed':False,'snapshot_roundtrips':3,'phase_fields_receipt_law_matching':True,'inactive_neural_RNG_unchanged':True,'actual_runtime_and_dispatch_identical':True,'native_fidelity_unchanged':True,'all_stages_on_native_hold_wave_grids':True,'prospective_output_directory_absent':True,'preparation_wall_seconds':time.perf_counter()-started,'preparation_status':'No A4 outcome observed. Full prospective production preflight deferred until genuine separate approval.'})
    after={p:sha(p) for p in before};assert before==after and not git('status','--porcelain').strip() and git('rev-parse','HEAD').decode().strip()==APP
    write('HASH_AFTER.json',after);write('PRESERVATION.json',{'original_files_checked':len(before),'all_original_hashes_unchanged':True,'worktree_clean':True,'code_changes':0,'configuration_changes':0,'Git_writes':0,'vault_Git_writes':0,'new_commit':None,'A4_execution_occurred':False,'source_manifest_verified':True})
    print(json.dumps({'packet':str(OUT),'batch_authority_sha256':h,'cases':[{'id':m['case_id'],'execution_sha256':m['execution_sha256']} for m in members],'world_steps':0,'controller_calls':0,'static_transductions':3,'preserved_files':len(before)},indent=2))
if __name__=='__main__':main()
