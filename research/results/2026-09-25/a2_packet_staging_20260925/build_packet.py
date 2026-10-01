"""Prepare a proposed A2 packet from immutable data. No simulation or commands."""
import base64,copy,gzip,hashlib,io,json,math,os,pathlib,shutil,subprocess,sys,time,zipfile
S=pathlib.Path(__file__).resolve().parent
ROOT=S.parent
R=ROOT/'exports/2026-09-25-first-commissioning-launch-packet-5f077481'
DV=ROOT/'exports/2026-09-25-A1-read-only-reanalysis-viewer-v1'
OUT=ROOT/'exports/2026-09-25-A2-launch-packet-5f077481'
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology'
A=D/'artifacts/first-commissioning-A1-20260925-5f077481'
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
CACHE=D/'artifacts/prehistory-attempt-001'
DEST=D/'artifacts/commissioning-A2-20260925-5f077481/trajectory-001'
APP='5f07748102cb5eaa302569c87efbae095050e9fe'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
sys.path.insert(0,str(DV))
from evidence import Evidence,plain,packed_attr
sys.path.insert(0,str(D))
from loom_commissioning import authority,contract,runner
from loom_p.records import code_identity
import numpy as np

def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def write(n,v):
    p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,ensure_ascii=False,allow_nan=False,indent=2)+'\n',encoding='utf-8')
def cp(p,n):
    q=OUT/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    # Disable only the unreadable optional global excludes for this read-only query.
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(S/'empty-excludes').as_posix(),'-C',str(W),*args],env=env)
def json_bytes(v):return json.dumps(v,allow_nan=False,separators=(',',':'),ensure_ascii=False).encode()
def no_execution(frame,event,arg):
    if event!='call':return
    f=frame.f_code;path=f.co_filename.replace('\\','/')
    if '/loom_p/' in path or '/loom_commissioning/' in path:
        forbidden=f.co_name in {'step','advance','account','prepare','waypoint_command','native','handoff','draw','_coupled','begin_command','hold','resume','transduce','from_verified_cache'}
        forbidden |= f.co_name=='__init__' and path.endswith(('/engine.py','/runner.py'))
        if forbidden:raise AssertionError('Preparation forbids execution: '+path+':'+f.co_name)

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
    started=time.perf_counter();sys.setprofile(no_execution)
    assert git('rev-parse','HEAD').decode().strip()==APP
    assert not git('status','--porcelain').strip()
    assert not DEST.parent.exists()
    assert code_identity()['sha256']=='63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9'
    assert contract.apparatus_identity()['sha256']=='d5801b69ae38d3259f3426aed8753fef8d76132a2f4ffecdd9baffb29afeb71a'
    for p in (D/'loom_p').glob('*.py'):assert p.read_bytes()==git('show',P+':developmental_ecology/loom_p/'+p.name)
    assert (D/'configuration.json').read_bytes()==git('cat-file','--filters',P+':developmental_ecology/configuration.json')
    e=Evidence() # verify original A1 ZIP and its nested launch manifest, read only
    lm=json.loads((R/'FILE_MANIFEST.json').read_bytes())
    for n,v in lm['files'].items():assert sha(R/n)==v['sha256'] and (R/n).stat().st_size==v['bytes'],n
    dvzip=ROOT/'exports/2026-09-25-A1-read-only-reanalysis-viewer-v1-delivery/A1_READ_ONLY_REANALYSIS_VIEWER_v1.zip'
    assert sha(dvzip)=='f8abb9adad900e80ee0b56c07a3068a4b5bc34a343dba580e360302b46c27d05'
    with zipfile.ZipFile(dvzip) as z:
        prefix='A1_READ_ONLY_REANALYSIS_VIEWER_v1/'
        vm=json.loads(z.read(prefix+'FILE_MANIFEST.json'))
        for n,v in vm['files'].items():
            b=z.read(prefix+n);assert digest(b)==v['sha256'] and len(b)==v['bytes'],n
    sources={
      'A2_PREPARATION_REQUEST.txt':pathlib.Path(r'C:\Users\Jason\.codex\attachments\8ebdd17a-b7d6-45d3-b411-6b1d587eef40\Pasted text.txt'),
      'WORKBENCH_AGENTS.md':WB/'AGENTS.md','WORKBENCH_MAP.md':WB/'00_RESEARCH_MAP.md','WORKBENCH_STATUS.md':WB/'01_WORKSPACE_STATUS.md',
      'REGISTERED_A1.md':WB/'50_SESSIONS/2026-09-25-first-a1-evidence-intake-6ad829e4/FIRST_A1_COMMISSIONING_EVIDENCE_RECORD.md',
      'REGISTERED_V3.md':WB/'50_SESSIONS/2026-09-25-v3-viewer-intake-4e7b80c2/A1_V3_REANALYSIS_AND_VIEWER_CONTINUATION.md',
      '00_LOOM_CURRENT_STATE.md':ROOT/'sources/00_LOOM_CURRENT_STATE(2).md',
      'V3_READ_ONLY_REANALYSIS_REPORT.md':DV/'V3_READ_ONLY_REANALYSIS_REPORT.md',
      'v3_checker_v1_1.py':DV/'v3_checker_v1_1.py','evidence.py':DV/'evidence.py',
      'V3_RESULT_v1_1.json':DV/'V3_RESULT_v1_1.json','VIEWER_DATA_FLOW.md':DV/'VIEWER_DATA_FLOW.md',
      'FIRST_A1_COMMISSIONING_RESULT.zip':e.path}
    for n in ('P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md','P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md','P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md','DECISION-P-APPARATUS-SCOPE-2026-09-24-73c9ad61.md','LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md'):
        sources[n]=R/'references'/n
    runtime_files=[p for folder in ('loom_p','loom_commissioning') for p in (D/folder).iterdir() if p.suffix in ('.py','.html')]+[D/'configuration.json',D/'requirements-lock.txt']
    preserved=set(runtime_files)|set(sources.values())|{p for q in (CACHE,A,R,DV) for p in q.rglob('*') if p.is_file() and '__pycache__' not in p.parts}|{dvzip}
    before={str(p):sha(p) for p in sorted(preserved)}
    OUT.mkdir(parents=True,exist_ok=False)
    probe=OUT/'access-check.tmp';probe.write_bytes(b'A2 packet preparation access');assert probe.read_bytes()==b'A2 packet preparation access';probe.unlink()
    write('HASH_BEFORE.json',before)
    records={}
    for n,p in sources.items():
        cp(p,'references/'+n);records[n]={'source_path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    write('SOURCE_IDENTITIES.json',records)
    for n in ('PROCEDURES.md','INTERPRETATION.md','build_packet.py','validate_packet.py'):cp(S/n,n)
    for p in runtime_files:cp(p,'instrument/developmental_ecology/'+p.relative_to(D).as_posix())
    for p in CACHE.rglob('*'):
        if p.is_file():cp(p,'verified-cache/'+p.relative_to(CACHE).as_posix())
    cp(R/'INITIAL_A1.snapshot.json.gz','INITIAL_A2.snapshot.json.gz')
    snap=json.loads(gzip.decompress((OUT/'INITIAL_A2.snapshot.json.gz').read_bytes()))
    assert digest(json_bytes(snap['state']))==snap['state_sha256']=='37adf68654e324141c678316f0f1f4b777853948e548cdd0d133e810c8722a6b'
    data=plain(snap['state']) # built-ins only, never production Engine unpack/construction
    assert data['time']==data['native_index']==0 and data['status']=='paused'
    assert data['last_events']==[] and data['last_native']=={} and data['last_wave'] is None
    assert data['body']['position']==[6.,3.] and data['body']['angle']==math.pi
    assert data['body']['energy']==.7 and data['body']['integrity']==1.
    assert data['stocks']==[.2]*8
    assert data['body']['velocity']==data['body']['command']==data['body']['force']==[0.,0.]
    assert data['body']['omega']==0 and data['body']['contact_rates']==[0.]*8
    summary=json.loads((R/'INITIAL_STATE_SUMMARY.json').read_bytes())
    summary.update(label='PROPOSED A2 fresh manufactured fixture; exact zero-time A1 initial snapshot reused; NOT historical A1 continuation',
                   snapshot_name='INITIAL_A2.snapshot.json.gz',fresh_session={'cursor':0,'hold_remaining':0,'decision':None,'own_commands':[]},
                   origin='A1 initial fixture bytes only; no state reset after time zero; no regenerated fields, neural state or RNG')
    write('INITIAL_STATE_SUMMARY.json',summary)
    cfg=json.loads((D/'configuration.json').read_bytes())
    field=packed_attr(snap['state'],'fields')
    assert digest(base64.b64decode(field['$array']))==summary['field_sha256']
    cache_receipt=json.loads((CACHE/'manifest.json').read_bytes())
    assert sha(CACHE/'manifest.json')==summary['initialization']['cache_receipt_sha256']
    assert cache_receipt['phase']==data['phase']==summary['mover_phase']
    assert cache_receipt['status']=='complete' and cache_receipt['steps_completed']==60000
    assert sha(CACHE/'fields.npz')==cache_receipt['file_sha256']
    assert all(cfg[k]==v for k,v in cache_receipt['law'].items())
    with np.load(CACHE/'fields.npz',allow_pickle=False) as f:assert f['fields'].tobytes()==base64.b64decode(field['$array'])
    scene=[]
    for i,(axis,sign,boundary) in enumerate(((0,1,0),(0,-1,20),(1,1,0),(1,-1,20))):scene.append({'id':f'wall-{i}','kind':'wall','axis':axis,'sign':sign,'boundary':boundary})
    for i,p in enumerate(cfg['source_positions']):scene.append({'id':f'source-{i}','kind':'disk','centre':p,'radius':cfg['source_radius']})
    for i,p in enumerate(cfg['repair_rectangles']):scene.append({'id':f'repair-{i}','kind':'rect','rect':p})
    cx,cy=cfg['mover_centre'];mw,mh=cfg['mover_size'];amp=cfg['mover_amplitude']
    swept={'kind':'rect','rect':[cx-amp-mw/2,cx+amp+mw/2,cy-mh/2,cy+mh/2]}
    geo={'body_radius':cfg['body_radius'],'source_0':cfg['source_positions'][0],'source_1':cfg['source_positions'][1],
         'mover_swept_rectangle':swept['rect'],'segments':{},'scope':'Exact straight-segment finite-body clearance only; no dynamic/controller path prediction; no A2 execution.'}
    for n,a,b in [('first_approach',[6.,3.],[4.,3.]),('depart_to_original_start',[4.,3.],[6.,3.]),('second_approach',[6.,3.],[9.,3.])]:
        gaps={f['id']:segment_gap(a,b,f,cfg['body_radius']) for f in scene}
        assert min(gaps.values())>=-cfg['geometry_tol']
        geo['segments'][n]={'from':a,'to':b,'length':math.dist(a,b),'surface_clearances':gaps,'mover_union_clearance':segment_gap(a,b,swept,cfg['body_radius'])}
    assert geo['segments']['second_approach']['surface_clearances']['source-1']==0
    write('GEOMETRY.json',geo)
    receipt=e.json('evidence/trajectory-001/manifest.json');result=e.json('evidence/EXECUTION_RESULT.json')
    observations=e.json('evidence/read-only-review/A1_OBSERVATIONS.json')
    first_negative=next(x for x in observations['all_fixed_windows'] if x['complete_0_2_second_interval'] and x['source_0_positive_duration_contact'] and x['net_energy_sign']=='negative_resolved')
    progress=[json.loads(x) for x in e.z.read('evidence/progress.jsonl').splitlines()]
    tail=next(x for x in progress if x['time']>=70)
    elapsed=result['time'];stored=sum(v['bytes'] for v in receipt['files'].values())+len(e.z.read('evidence/trajectory-001/manifest.json'))
    rate=receipt['wall_seconds']/elapsed;tailrate=(progress[-1]['wall_seconds_since_preflight']-tail['wall_seconds_since_preflight'])/(elapsed-tail['time'])
    budget={'planning_source':'Actual one A1 attempt and immutable progress/receipt records, not engineering-smoke rates',
       'a1_zip_sha256':e.zip_sha256,'a1_measured':{'simulated_seconds':elapsed,'native_steps':result['native_index'],'recorder_wall_seconds':receipt['wall_seconds'],'whole_process_wall_seconds':result['wall_seconds_including_preflight'],'uncompressed_stream_bytes':receipt['uncompressed_bytes'],'stored_trajectory_bytes_including_snapshots_and_receipt':stored},
       'rates':{'wall_seconds_per_simulated_second':rate,'uncompressed_bytes_per_simulated_second':receipt['uncompressed_bytes']/elapsed,'stored_trajectory_bytes_per_simulated_second':stored/elapsed,'tail_start_simulated_time':tail['time'],'tail_wall_seconds_per_simulated_second':tailrate},
       'projection_180_seconds':{'average_wall_seconds':180*rate,'tail_wall_seconds':180*tailrate,'uncompressed_bytes':180*receipt['uncompressed_bytes']/elapsed,'stored_trajectory_bytes':180*stored/elapsed},
       'old_400_seconds_average_wall_seconds':400*rate,'proposed_case_simulated_ceiling':180,'native_steps_ceiling':18000,'command_decisions_ceiling':1800,
       'runner_wall_seconds_ceiling':3600,'uncompressed_stream_bytes_ceiling':1500000000,'local_free_disk_reserve_bytes':3000000000,
       'separate_read_only_reporting_wall_seconds_ceiling':3600,'separate_reporting_world_steps':0,
       'wall_headroom_fraction':3600/(180*rate)-1,
       'limitations':['Linear projection is not an assured completion time or storage bound.','Restart sensor history grows; snapshot costs and total stored size need not scale linearly.','Second-stage travel/contact and host load may differ from A1.','Storage guard counts uncompressed streams, not total snapshots/archives.','No new performance benchmark was executed.']}
    write('BUDGET.json',budget)
    write('A1_PLANNING_EVIDENCE.json',{'first_negative_contact_window':first_negative,'source_report':'references/FIRST_A1_COMMISSIONING_RESULT.zip: evidence/read-only-review/A1_OBSERVATIONS.json','status':'Historical evidence, not an A2 outcome','a1_final_time':elapsed,'a1_ended_by':'administrative_pause / wall_time_limit','a1_source0_final_stock':observations['certified_source_contact_events'][-1]['stock_after'][0]})
    ids={'P_commit':P,'apparatus_commit':APP,'worktree':str(W),'branch':git('branch','--show-current').decode().strip(),'P':code_identity(),'apparatus':contract.apparatus_identity(),'runtime':authority.runtime_identity(),'controller':authority.controller_identity('waypoint'),'configuration_file_sha256':sha(D/'configuration.json'),'configuration_semantic':snap['configuration'],'git_status_clean':True,'read_only_git_note':'Empty local excludes file scoped to query because optional global ignore is inaccessible; tracked and untracked worktree status empty. No Git configuration written.'}
    write('CODE_AND_RUNTIME_IDENTITIES.json',ids)
    m=json.loads((R/'A1_MANIFEST.json').read_bytes())
    m.update(case_id='A2',duration_seconds=180.,hard_stop_time=180.,execution_authority=None)
    m['execution']['procedure']['stages']=[{'point':[3.,3.],'until':90.,'press_force':.1},{'point':[6.,3.],'until':120.,'press_force':0.},{'point':[10.,3.],'until':180.,'press_force':.1}]
    m['execution']['resources']={'storage_limit_bytes':1500000000,'wall_limit_seconds':3600}
    record=copy.deepcopy(m['execution']['procedure']['protocol']['recording_contract'])
    record['post_read']='Read-only hashes/ledger/controller-input and issued-versus-delivered command checks; corrected initial-envelope V3 alignment per INTERPRETATION.md and reference report. No replay; no new live viewer.'
    bound_names=['PROCEDURES.md','INTERPRETATION.md','build_packet.py','validate_packet.py','SOURCE_IDENTITIES.json','INITIAL_STATE_SUMMARY.json','GEOMETRY.json','BUDGET.json','A1_PLANNING_EVIDENCE.json','CODE_AND_RUNTIME_IDENTITIES.json']
    protocol={'packet_label':'A2 physical-ceiling witness / PROPOSED / NOT AUTHORIZED',
       'reviewed_checkpoints':{'p_git_sha':P,'apparatus_git_sha':APP},'case_count':1,
       'prior_evidence_status':{'V1':'COMPLETE','V2':'COMPLETE','V3':'COMPLETE by read-only reanalysis','A0':'COMPLETE','A1':'one external physical witness OBSERVED'},
       'bound_files':{n:sha(OUT/n) for n in bound_names},
       'initial_snapshot_file':{'name':'INITIAL_A2.snapshot.json.gz','sha256':sha(OUT/'INITIAL_A2.snapshot.json.gz')},
       'fixture_label':'Fresh A2 manufactured external initial fixture, exact zero-time A1 initial state reused; not a continuation and not a newborn',
       'first_source_label':'source-0 at (3,3)','second_source_label':'source-1 at (10,3)',
       'recording_contract':record,'record_destination':str(DEST),'analysis_destination':str(DEST.parent/'read-only-review'),
       'launch_operations':['Only after genuine Jason approval of exact object','verify every bound file and live identity','load exact zero-time snapshot; production manifest/state/history and dispatch checks','one fresh Run using unchanged passive observer and typed prescription','ordinary holds without manual commands until first stop','preserve all evidence and read-only report; no retry/resume/patch'],
       'stop_names':['terminal','apparatus_failure','administrative_pause','administrative_cutoff'],
       'failure_rule':'Report all outcomes without patch; no route substitution, deadline extension, new start or automatic continuation.',
       'continuity_rule':'All E/I, stocks, fields, mover clock, controller history and physical state continue throughout the single case; no midtrajectory resets.',
       'component_allowance':{'machine_seconds':3600,'world_steps':0,'scope':'Identity and read-only record/report/package work only; no component suite, replay or dynamic probes'},
       'disk_bytes_for_primary_analysis_and_copy':3000000000,
       'excluded_cases':['A1 repetition as a separate case','A3','A4','A5','B1','B2','B3','B4','C1','C2','newborn lives','fixed-structure diagnostic','scientific tests','new prehistory','parameter sweeps'],
       'legacy_roster_note':'Mandatory roster remains execution_authorized=false; no births or C cases proposed.'}
    m['execution']['procedure']['protocol']=protocol
    assert m['initial_state']==snap['state_sha256'] and m['execution_authority'] is None
    assert m['execution']['runtime']==ids['runtime']
    authority.validate_execution(m,complete=True)
    authority.validate_dispatch(m,vars(runner))
    try:contract.authorize_execution(m)
    except ValueError as ex:assert str(ex)=='commissioning execution is not authorized';denial=str(ex)
    else:raise AssertionError('Null grant accepted')
    write('A2_MANIFEST.json',m)
    obj=authority.execution_object(m);canonical=authority.canonical(obj);h=authority.execution_sha256(m)
    write('AUTHORITY_OBJECT.json',obj);(OUT/'AUTHORITY_OBJECT.canonical.json').write_bytes(canonical)
    (OUT/'AUTHORITY_SHA256.txt').write_text(h+'  AUTHORITY_OBJECT.canonical.json\n',encoding='utf-8')
    write('PREPARATION_CHECKS.json',{'scope':'Static saved-data/geometry/hash/manifest checks only, NOT an A2 physical witness or new completion of V1-V3/A0',
       'original_A1_manifest_payloads_verified':len(e.manifest['files']),'original_launch_payloads_verified':len(lm['files']),'V3_viewer_package_payloads_verified':len(vm['files']),
       'initial_snapshot_exact_A1_zero_time_copy':True,'snapshot_state_payload_checksum_valid':True,'cache_fields_exact_snapshot_match':True,'cache_identity_phase_law_valid':True,
       'live_runtime_controller_and_dispatch_valid':True,'complete_execution_structure_valid':True,'null_grant_rejected':denial,
       'typed_deadlines_on_0_1_grid':all(abs(x['until']/.1-round(x['until']/.1))<1e-8 for x in m['execution']['procedure']['stages']),
       'all_geometric_segments_nonpenetrating':True,'new_output_destination_absent':not DEST.parent.exists(),
       'Engine_constructors':0,'Run_constructors':0,'computed_controller_commands':0,'world_steps':0,'field_steps':0,'neural_steps':0,'simulation_RNG_draws':0,'new_prehistory_steps':0,'replays':0,
       'future_launch_preflight':'Production validate_manifest checks on the loaded exact state, including history-loader verification, remain required after separate authorization. No Engine was unpacked/constructed in preparation.',
       'preparation_wall_seconds':time.perf_counter()-started})
    after={p:sha(p) for p in before};assert before==after
    assert not git('status','--porcelain').strip() and git('rev-parse','HEAD').decode().strip()==APP
    write('HASH_AFTER.json',after)
    write('PRESERVATION.json',{'files_checked':len(before),'all_original_hashes_unchanged':True,'code_changes':0,'configuration_changes':0,'Git_writes':0,'vault_Git_writes':0,'new_commit':None,'authority_status':'PROPOSED / NOT AUTHORIZED','A2_execution_occurred':False})
    print(json.dumps({'output':str(OUT),'authority_sha256':h,'average_projected_minutes':180*rate/60,'tail_projected_minutes':180*tailrate/60,'null_grant_rejected':True,'executed':False},indent=2))

if __name__=='__main__':main()
