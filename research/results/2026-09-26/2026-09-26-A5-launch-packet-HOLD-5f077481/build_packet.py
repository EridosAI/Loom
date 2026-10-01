"""Guarded A5 proposal authoring. No simulation, command, sensor or RNG call."""
import ast,base64,copy,gzip,hashlib,io,json,math,os,pathlib,shutil,subprocess,sys,time,zipfile
from clock_audit import audit
from validate_packet import canonical,strict,attr,vector,state_digest
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
OUT=ROOT/'exports/2026-09-26-A5-launch-packet-HOLD-5f077481'
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405');D=W/'developmental_ecology'
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
R1=ROOT/'exports/2026-09-25-first-commissioning-launch-packet-5f077481'
R2=ROOT/'exports/2026-09-25-A2-launch-packet-5f077481'
R3=ROOT/'exports/2026-09-25-A3-launch-packet-5f077481'
R4=ROOT/'exports/2026-09-26-A4-launch-packet-5f077481'
E2=ROOT/'exports/2026-09-25-A2-commissioning-result-5f077481/A2_COMMISSIONING_RESULT'
E3=ROOT/'exports/2026-09-26-A3-commissioning-result-5f077481/A3_COMMISSIONING_RESULT'
E4=ROOT/'exports/2026-09-26-A4-commissioning-result-5f077481/A4_COMMISSIONING_RESULT'
CACHE=D/'artifacts/prehistory-attempt-001';DEST=D/'artifacts/commissioning-A5-20260926-5f077481'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f';APP='5f07748102cb5eaa302569c87efbae095050e9fe'
PHASE=3.558411277237072
STAGES=[{'point':a,'until':t,'press_force':f} for a,t,f in [([3.,3.],90.,.1),([6.,3.],120.,0.),([10.,3.],270.,.1),([6.,3.],300.,0.),([3.,3.],450.,.1),([6.,3.],480.,0.),([10.,3.],630.,.1)]]
FORBIDDEN=[]

def guard(frame,event,arg):
    if event!='call':return
    f=frame.f_code;p=f.co_filename.replace('\\','/')
    if '/loom_p/' in p or '/loom_commissioning/' in p:
        bad=f.co_name in {'step','advance','account','prepare','waypoint_command','native','handoff','draw','_coupled','coupled','begin_command','hold','resume','from_verified_cache','load_restart','load_snapshot','save_snapshot','transduce','free_velocity','actuator_forces','verify_history','load'}
        bad|=f.co_name=='__init__' and (p.endswith(('/engine.py','/runner.py','/neural.py','/chemistry.py')) or type(frame.f_locals.get('self')).__name__=='Streams')
        if bad:
            FORBIDDEN.append(p+':'+f.co_name);raise AssertionError('A5 preparation forbids '+FORBIDDEN[-1])
sys.setprofile(guard);sys.path.insert(0,str(D))
from loom_commissioning import authority,contract,runner
from loom_p.records import code_identity
import numpy as np

def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def write(n,v):
    q=OUT/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
def txt(n,v):(OUT/n).write_text(v,encoding='utf-8')
def cp(p,n):
    q=OUT/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(S/'empty-excludes').as_posix(),'-C',str(W),*args],env=env)
def zipcheck(raw,prefix=''):
    z=zipfile.ZipFile(io.BytesIO(raw));fm=strict(z.read(prefix+'FILE_MANIFEST.json'));assert len(z.namelist())==len(set(z.namelist()))
    assert set(z.namelist())=={prefix+n for n in fm['files']}|{prefix+'FILE_MANIFEST.json'}
    for n,v in fm['files'].items():
        b=z.read(prefix+n);assert len(b)==v['bytes'] and digest(b)==v['sha256'],n
    return z,len(fm['files'])

def main():
    started=time.perf_counter();assert not OUT.exists() and not DEST.exists()
    (S/'empty-excludes').touch(exist_ok=True)
    assert git('rev-parse','HEAD').decode().strip()==APP and not git('status','--porcelain').strip()
    pi=code_identity();ai=contract.apparatus_identity();ri=authority.runtime_identity()
    assert pi['sha256']==contract.P_CODE and ai['sha256']=='d5801b69ae38d3259f3426aed8753fef8d76132a2f4ffecdd9baffb29afeb71a'
    for p in (D/'loom_p').glob('*.py'):assert p.read_bytes()==git('show',P+':developmental_ecology/loom_p/'+p.name)
    assert (D/'configuration.json').read_bytes()==git('cat-file','--filters',P+':developmental_ecology/configuration.json')
    assert ri==strict((R3/'A3_MANIFEST.json').read_bytes())['execution']['runtime']
    prior=E4.parent/'A4_COMMISSIONING_RESULT.zip'
    assert sha(prior)=='3d6eaaa52b056a344bd2b1c5312ded561c477c273a01868f075dae3424097f8a'
    z4,n4=zipcheck(prior.read_bytes());zr4,nr4=zipcheck(z4.read('approved-launch/A4_LAUNCH_PACKET.zip'))
    z3,n3=zipcheck(zr4.read('references/A3_COMMISSIONING_RESULT.zip'));zr3,nr3=zipcheck(z3.read('approved-launch/A3_LAUNCH_PACKET.zip'),'A3_LAUNCH_PACKET/')
    z2,n2=zipcheck(zr3.read('A3_LAUNCH_PACKET/references/A2_COMMISSIONING_RESULT.zip'));zr2,nr2=zipcheck(z2.read('approved-launch/A2_LAUNCH_PACKET.zip'),'A2_LAUNCH_PACKET/')
    z1,n1=zipcheck(zr2.read('A2_LAUNCH_PACKET/references/FIRST_A1_COMMISSIONING_RESULT.zip'));zr1,nr1=zipcheck(z1.read('approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip'),'FIRST_COMMISSIONING_LAUNCH_PACKET/')
    for folder in (R1,R2,R3,R4):
        fm=strict((folder/'FILE_MANIFEST.json').read_bytes())
        for n,v in fm['files'].items():assert sha(folder/n)==v['sha256'] and (folder/n).stat().st_size==v['bytes'],str(folder/n)
    assert (R1/'INITIAL_A1.snapshot.json.gz').read_bytes()==zr1.read('FIRST_COMMISSIONING_LAUNCH_PACKET/INITIAL_A1.snapshot.json.gz')
    reference_names=['00_LOOM_CURRENT_STATE.md','P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md','P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md','P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md','DECISION-P-APPARATUS-SCOPE-2026-09-24-73c9ad61.md','LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md','V3_RESULT_v1_1.json','V3_READ_ONLY_REANALYSIS_REPORT.md','VIEWER_DATA_FLOW.md']
    sources={n:R3/'references'/n for n in reference_names}
    sources.update({'A5_PREPARATION_REQUEST.txt':pathlib.Path(r'C:\Users\Jason\.codex\attachments\1a4d0fd2-43e2-40ca-b9ba-7105493b1dfd\Pasted text.txt'),
       'A4_COMMISSIONING_RESULT.zip':prior,'INITIAL_A1.snapshot.json.gz':R1/'INITIAL_A1.snapshot.json.gz','A0_GEOMETRY.json':R1/'A0_GEOMETRY.json',
       'A2_RESOURCE_RESULT.json':E2/'RESOURCE_RESULT.json','A3_RESOURCE_RESULT.json':E3/'RESOURCE_RESULT.json','A4_RESOURCE_RESULT.json':E4/'RESOURCE_RESULT.json',
       'A2_OBSERVATIONS.json':E2/'evidence/read-only-review/A2_OBSERVATIONS.json',
       'A3_PLAIN_LANGUAGE_RESULT.md':E3/'evidence/read-only-review/A3_PLAIN_LANGUAGE_RESULT.md',
       'CONTACT_INTERRUPTION_NOTE.md':E3/'evidence/read-only-review/CONTACT_INTERRUPTION_NOTE.md',
       'A4_RESULT_SUMMARY.json':E4/'evidence/read-only-review/A4_RESULT_SUMMARY.json',
       'A4_PLAIN_LANGUAGE_RESULT.md':E4/'evidence/read-only-review/A4_PLAIN_LANGUAGE_RESULT.md',
       'A4_COMMISSIONING_EVIDENCE_RECORD.md':WB/'50_SESSIONS/2026-09-26-a4-evidence-intake-0e69b3c8/A4_COMMISSIONING_EVIDENCE_RECORD.md',
       'WORKBENCH_AGENTS.md':WB/'AGENTS.md','WORKBENCH_MAP.md':WB/'00_RESEARCH_MAP.md','WORKBENCH_STATUS.md':WB/'01_WORKSPACE_STATUS.md','PROJECT_AGENTS.md':ROOT/'AGENTS.md'})
    for E,z in ((E2,z2),(E3,z3),(E4,z4)):
        assert (E/'RESOURCE_RESULT.json').read_bytes()==z.read('RESOURCE_RESULT.json')
    assert sources['A2_OBSERVATIONS.json'].read_bytes()==z2.read('evidence/read-only-review/A2_OBSERVATIONS.json')
    assert sources['A4_RESULT_SUMMARY.json'].read_bytes()==z4.read('evidence/read-only-review/A4_RESULT_SUMMARY.json')
    runtime_files=[p for f in ('loom_p','loom_commissioning') for p in (D/f).iterdir() if p.suffix in ('.py','.html')]+[D/'configuration.json',D/'requirements-lock.txt']
    raw_roots=[D/'artifacts'/n for n in ('first-commissioning-A1-20260925-5f077481','commissioning-A2-20260925-5f077481','commissioning-A3-20260925-5f077481','commissioning-A4-20260926-5f077481')]
    preserved=set(runtime_files)|set(sources.values())|{p for folder in (CACHE,R1,R2,R3,R4,*raw_roots) for p in folder.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    before={str(p):sha(p) for p in sorted(preserved)}
    OUT.mkdir(parents=True)
    probe=OUT/'access-check.tmp';probe.write_bytes(b'A5 static preparation only');assert probe.read_bytes()==b'A5 static preparation only';probe.unlink()
    write('HASH_BEFORE.json',before)
    ids={}
    for n,p in sources.items():cp(p,'references/'+n);ids[n]={'source_path':str(p),'sha256':sha(p),'bytes':p.stat().st_size}
    write('SOURCE_IDENTITIES.json',ids)
    docs=['PROCEDURES.md','OBSERVATION_AND_INTERPRETATION.md','VIEWER_RECORD_CONTRACT.md','REVIEW_AND_EXECUTION_BOUNDARY.md','OPEN_ISSUE_A5_CLOCK.md','clock_audit.py','build_packet.py','validate_packet.py','finish_packet.py','deliver_packet.py']
    for n in docs:cp(S/n,n)
    for p in runtime_files:cp(p,'instrument/developmental_ecology/'+p.relative_to(D).as_posix())
    for p in CACHE.rglob('*'):
        if p.is_file() and '__pycache__' not in p.parts:cp(p,'verified-cache/'+p.relative_to(CACHE).as_posix())
    cfg=strict((D/'configuration.json').read_bytes());cr=strict((CACHE/'manifest.json').read_bytes())
    m=copy.deepcopy(strict((R2/'A2_MANIFEST.json').read_bytes()))
    assert cr['phase']==PHASE and cr['status']=='complete' and cr['steps_completed']==60000
    assert sha(CACHE/'manifest.json')==m['initialization']['cache_receipt_sha256'] and sha(CACHE/'fields.npz')==cr['file_sha256']
    assert all(cfg[k]==v for k,v in cr['law'].items())
    with np.load(CACHE/'fields.npz',allow_pickle=False) as data:assert digest(data['fields'].tobytes())==cr['field_sha256']==m['initial_fields']
    relevant={'geometry.py':{'circle_rect_area','disk_areas','rectangle_areas','mover'},'schema.py':{'Streams'}}
    dependency_checks={}
    for name in ('chemistry.py','geometry.py','schema.py'):
        original=(CACHE/'law-source-at-preparation'/name).read_bytes();current=(D/'loom_p'/name).read_bytes()
        assert digest(original)==cr['code']['files'][name]
        if name=='chemistry.py':assert original==current
        else:
            def dependencies(raw):
                nodes=[n for n in ast.parse(raw.decode()).body if isinstance(n,(ast.Import,ast.ImportFrom)) or getattr(n,'name',None) in relevant[name]]
                return ast.dump(ast.Module(body=nodes,type_ignores=[]),include_attributes=False)
            assert dependencies(original)==dependencies(current)
        dependency_checks[name]={'original_sha256':digest(original),'current_sha256':digest(current),'required_dependencies_identical':True}
    cp(R1/'INITIAL_A1.snapshot.json.gz','INITIAL_A5.snapshot.json.gz')
    snap=strict(gzip.decompress((OUT/'INITIAL_A5.snapshot.json.gz').read_bytes()));e=snap['state'];b=attr(e,'body')
    assert state_digest(e)==snap['state_sha256']==m['initial_state']=='37adf68654e324141c678316f0f1f4b777853948e548cdd0d133e810c8722a6b'
    assert vector(attr(b,'position'))==[6.,3.] and attr(b,'angle')==math.pi
    assert attr(e,'time')==attr(e,'native_index')==0 and vector(attr(e,'stocks'))==[.2]*8
    assert state_digest(attr(e,'organism'))=='0d1de850e85a085dd7288cadbd8be0da577211a8a1e47d819a5d7e111024a5ed'
    write('INITIAL_STATE_SUMMARY.json',{'snapshot_file':'INITIAL_A5.snapshot.json.gz','snapshot_sha256':sha(OUT/'INITIAL_A5.snapshot.json.gz'),'state_sha256':m['initial_state'],
        'body':{'position':vector(attr(b,'position')),'angle':attr(b,'angle'),'energy':attr(b,'energy'),'integrity':attr(b,'integrity'),'velocity':vector(attr(b,'velocity')),'omega':attr(b,'omega'),'commands':vector(attr(b,'command')),'forces':vector(attr(b,'force')),'contact_rates':vector(attr(b,'contact_rates'))},
        'stocks':vector(attr(e,'stocks')),'time':0,'native_index':0,'status':'paused','phase':PHASE,'field_sha256':m['initial_fields'],'history':m['initialization'],
        'unchanged_inactive_organism_sha256':state_digest(attr(e,'organism')),'snapshot_is_byte_identical_A1_A2_start':True,'fixture_type':'manufactured_external_geometry_start; not newborn, not a continuation',
        'cache_dependency_verification':dependency_checks,'new_prehistory_steps':0,'sensor_evaluations':0,'fixture_mutations':0})
    write('CODE_AND_RUNTIME_IDENTITIES.json',{'P':pi,'apparatus':ai,'runtime':ri,'configuration_semantic_sha256':contract.CONFIG,'configuration_file_sha256':sha(D/'configuration.json'),
        'p_commit':P,'apparatus_commit':APP,'worktree':str(W),'branch':git('branch','--show-current').decode().strip(),'executable':sys.executable,'git_version':subprocess.check_output(['git','--version']).decode().strip(),
        'local_execution_context':'Real Windows desktop paths and installed pinned Python read directly; no cloud simulation or sandbox substitute','worktree_clean':True})
    write('CLOCK_AUDIT.json',audit(D))
    away=[210,216,222];departure_stock=.035148459595822044
    renewal={str(a):{'restored_fraction_of_deficit':-math.expm1(-a/400),'illustrative_A2_departure_stock':departure_stock,'illustrative_unattended_return_stock':.2-(.2-departure_stock)*math.exp(-a/400),'illustrative_renewal':(.2-departure_stock)*(-math.expm1(-a/400))} for a in away}
    a4s=strict(sources['A4_RESULT_SUMMARY.json'].read_bytes())
    geometry={'method':'Static geometry, saved measurements and analytic source-law evaluation only. No dynamic trajectory, controller command or candidate trial.',
       'source_centres':cfg['source_positions'],'body_radius':cfg['body_radius'],'source_radius':cfg['source_radius'],'source_order':[0,1,0,1],
       'nominal_body_contact_positions':[[4.,3.],[9.,3.]],'nominal_body_centre_legs_metres':[2.,5.,5.,5.],'nominal_total_path_metres':17.,
       'mover_swept_rectangle':[5.,15.,9.5,10.5],'nominal_bottom_route_surface_gap_to_mover_union':6.,'nominal_bottom_wall_surface_gap':2.5,
       'renewal_tau_seconds':400.,'capacity_per_source':.2,'away_time_law_examples':renewal,
       'A1_A2_initial_approach':{'nominal_metres':2.,'actual_contact_seconds':6.31019048650431,'nominal_metres_per_second':2/6.31019048650431},
       'A2_transfer_leg':{'actual_release':90.00000000000914,'actual_arrival':132.3764279535912,'actual_seconds':42.37642795358205,'actual_expenditure':.07565364813787812,'nominal_contact_to_contact_metres':5.,'nominal_distance_per_elapsed_second':5/42.37642795358205},
       'A4_detour_arrival':{'actual_sampled_metres':7.750192603431225,'actual_seconds':23.43,'sampled_metres_per_elapsed_second':7.750192603431225/23.43},
       'A2_source0_first_stage':{'departure_stock':departure_stock,'actual_gross_intake':.18886652837484535,'actual_expenditure':.14879710305038218},
       'planned_horizon_seconds':630.,'scheduled_dwell_windows_seconds':[90.,150.,150.,150.],'separate_departure_windows_seconds':[30.,30.,30.],
       'planned_contact_time_not_guaranteed':True,'trial_trajectories':0,'two_source_maximum_total_renewal_per_second':.001,'basal_expenditure_per_second':.0015,'indefinite_viability_claim':False}
    assert cfg['source_tau']==400 and cfg['source_capacity']==.2 and cfg['body_radius']==cfg['source_radius']==.5
    write('CIRCUIT_AND_RENEWAL_RATIONALE.json',geometry)
    measured={'A2':strict(sources['A2_RESOURCE_RESULT.json'].read_bytes()),'A3':strict(sources['A3_RESOURCE_RESULT.json'].read_bytes()),'A4':strict(sources['A4_RESOURCE_RESULT.json'].read_bytes())}
    rates={};storage_models={}
    for label,r in measured.items():
        t=r['total_simulated_seconds'] if label=='A4' else r['simulated_seconds_recorded']
        wall=r['total_recorder_wall_seconds'] if label=='A4' else r['recorder_wall_seconds']
        whole=sum(v['whole_process_wall_seconds'] for v in r['cases'].values()) if label=='A4' else r['whole_process_wall_seconds']
        unc=r['total_uncompressed_stream_bytes'] if label=='A4' else r['uncompressed_stream_bytes']
        stored=r['total_stored_trajectory_bytes'] if label=='A4' else r['stored_trajectory_bytes_including_snapshots_and_receipt']
        rates[label]={'simulated_seconds':t,'wall_seconds_per_sim_second':wall/t,'whole_process_wall_seconds_per_sim_second':whole/t,'uncompressed_bytes_per_sim_second':unc/t,'naive_stored_bytes_per_sim_second':stored/t,
                      'projected_recorder_wall_seconds':630*wall/t,'projected_whole_process_wall_seconds':630*whole/t,'projected_uncompressed_stream_bytes':630*unc/t,'naive_linear_stored_bytes_not_used_as_main_estimate':630*stored/t}
        if label in ('A2','A3'):
            folder=raw_roots[1 if label=='A2' else 2]/'trajectory-001';initial=(folder/'initial.restart.json.gz').stat().st_size;final=(folder/'final.restart.json.gz').stat().st_size
            snaps={p.name:p.stat().st_size for p in sorted(folder.glob('*.restart.json.gz'))}
            streams=sum(p.stat().st_size for p in folder.glob('*.jsonl.gz'));display=(folder/'sensor-display.json').stat().st_size
            slope=(final-initial)/t
            predicted_snapshots=sum(initial+slope*s for s in [0,*range(10,631,10),630])
            predicted=predicted_snapshots+streams*630/t+display*630/t+1000000
            storage_models[label]={'initial_snapshot_bytes':initial,'final_snapshot_bytes':final,'snapshot_bytes_by_name':snaps,'stream_gzip_bytes':streams,'display_json_bytes':display,
              'snapshot_bytes_per_sim_second_slope':slope,'predicted_65_snapshot_bytes':predicted_snapshots,'predicted_stream_gzip_bytes':streams*630/t,'predicted_display_json_bytes':display*630/t,'receipt_misc_allowance_bytes':1000000,'predicted_total_bytes':predicted}
    budget={'status':'Conditional proposal estimates only; current clock hold prevents meaningful full-horizon launch. No benchmark or A5 run.',
      'measurements':measured,'rates_and_linear_projections':rates,'growing_restart_history_models':storage_models,'simulated_ceiling_seconds':630,'maximum_full_native_steps':63000,'maximum_controller_decisions':6300,'expected_full_sensor_rows':63001,'snapshot_count_full_case':65,
      'runner_wall_cap_seconds':14400,'read_only_reporting_wall_cap_seconds':3600,'combined_wall_allowance_seconds':18000,'uncompressed_stream_cap_bytes':1500000000,'combined_new_disk_cap_bytes':10000000000,'free_disk_precondition_bytes':10000000000,
      'stop_request_disk_bytes':9000000000,'final_flush_reserve_bytes':1000000000,'no_continuation':True,'prior_review_archive_bytes':prior.stat().st_size,
      'predicted_trajectory_high_bytes':max(v['predicted_total_bytes'] for v in storage_models.values()),'conservative_planning_trajectory_bytes':1000000000,
      'estimated_new_launch_zip_bytes':170000000,'estimated_result_zip_with_launch_and_raw_bytes':1200000000,
      'disk_scope':'Combined new primary record, analysis files and new project/workbench packet/result copies. Existing immutable A0-A4 originals excluded; any new copies of them included.',
      'enforcement':'No executable wrapper supplied under HOLD. Future authorized wrapper must preflight free space, measure all bound new output trees before every command hold, request clean administrative_pause when >=9 GB or free<1 GB, and prohibit copying/reporting work that would cross 10 GB. Native-step wall/stream guards remain unchanged. Final native operation/flush is not an OS hard quota; expose any overrun/I/O failure.'}
    write('RESOURCE_PROJECTION.json',budget)
    rows='\n'.join(f"| {k} | {v['simulated_seconds']:.2f} s | {v['wall_seconds_per_sim_second']:.6f} | {v['projected_recorder_wall_seconds']/60:.2f} min | {v['projected_uncompressed_stream_bytes']/1e6:.2f} MB |" for k,v in rates.items())
    storage_rows='\n'.join(f"| {k} | {v['predicted_65_snapshot_bytes']/1e6:.2f} MB | {v['predicted_stream_gzip_bytes']/1e6:.2f} MB | {v['predicted_display_json_bytes']/1e6:.2f} MB | {v['predicted_total_bytes']/1e6:.2f} MB |" for k,v in storage_models.items())
    txt('RESOURCE_PLAN.md',f'''# A5 conditional resource plan — full fidelity, no benchmark

**HOLD:** these are costs for the proposed full 630-second case, not a promise that the pinned apparatus can execute it. The static clock incompatibility must be resolved separately first.

| Measured evidence | Recorded simulated time | Wall s / simulated s | 630 s recorder projection | 630 s uncompressed streams |
|---|---:|---:|---:|---:|
{rows}

A2 and A3 are the controlling long-run measurements; A4 supplies a recent shorter three-case comparison. Whole-process projections and all exact receipts are in `RESOURCE_PROJECTION.json`. Plan for **roughly 2.0–2.1 hours of execution**, plus reporting. Accumulating sensor history, snapshots, host load and contact complexity may make 630 seconds slower than this extrapolation. No new throughput test was run. The predetermined runner ceiling is **4 hours (14,400 s)**, followed by at most **1 hour (3,600 s) saved-data reporting/checks/packaging**. The allowance is 5 hours total, not a guarantee or permission to continue the trajectory.

Storage must include accumulated restart histories. A naive linear stored-bytes extrapolation undercounts them. The model takes each measured initial/final compressed snapshot slope and sums predicted sizes at t=0, every 10 seconds through 630, and the additional final snapshot. That is **65 snapshots**, including the separate t=630 checkpoint and final receipt state. Gzip streams and final sensor-display bytes are scaled separately, plus 1 MB miscellaneous allowance. This assumes approximately linear history-size growth, not a fitted physical trajectory.

| Long-run basis | Snapshot total | Compressed streams | Final display | Total including miscellaneous |
|---|---:|---:|---:|---:|
{storage_rows}

Allow **1 GB for the new trajectory** for planning; no record thinning. The uncompressed stream cap is **1.5 GB**, distinct from compressed files and checkpoints. The launch review adds about 167 MB of historical evidence, roughly 170 MB packaged. Allow up to 1.2 GB per result bundle with launch evidence. A planning example with 1 GB raw + 0.4 GB derived material + two extracted 1.57 GB result trees + two 1.2 GB ZIPs + existing new launch copies totals under 8 GB; it is an allowance, not a measured future size. All new artifacts and copies share a **10 GB** ceiling. Existing historical originals are excluded from this new-work total; any new copies count.

Before a future authorized launch, require 10 GB free. An administrative monitor of the specifically bound new output directories must check combined usage before each held command and stop at 9 GB or free space below 1 GB, reserving 1 GB for finalization. It may call the existing clean resource-stop interface only; it does not change physical laws or commands. Before each later analysis/copy/archive operation, include its bounded size estimate and stop if the 10 GB ceiling would be exceeded. Preserve originals; never reclaim space by deleting historical evidence. No such launcher/monitor is implemented or invoked in this held packet.

The unchanged runner checks wall time and uncompressed-stream reserve at native boundaries. These and the combined-disk rule are hard administrative stop instructions, not exact OS quotas: a current native operation, final snapshot or flush may overrun a threshold. Record actual values and any I/O failure; do not restart or continue. If the cap prevents full delivery, preserve completed originals and report the missing derivative/copy rather than drop evidence.

Full 100 Hz native, all event subdivisions, 10 Hz commands, sensor endpoints, diagnostics and restart histories are retained. The legacy selection stride is not native decimation. No plot/live viewer enters the loop. No physical terminal, controller miss or resource stop permits tuning or a second attempt.
''')
    write('PLANNING_EVIDENCE.json',{'completed_physical_rows':['A0','A1','A2','A3','A4'],'prior_A4_archive_sha256':sha(prior),
       'verified_nested_payload_counts':{'A4_result':n4,'A4_launch':nr4,'A3_result':n3,'A3_launch':nr3,'A2_result':n2,'A2_launch':nr2,'A1_result':n1,'A1_launch':nr1},
       'source_hierarchy':'Pinned code and exact sealed records control. Workbench AGENTS/map/status now register A4 OBSERVED. Earlier retrospective/draft statuses are preserved history.',
       'accepted_decisions':'Only scope accepted by the packaged decision/ruling records; current user authorizes A5 preparation, not execution, clock repair or changes.',
       'assistant_proposal':'One 630-second two-source itinerary selected without trials; all stage timings, resource estimates and attribution bounds are proposed review terms.',
       'unresolved':'Pinned longer-horizon absolute clock predicate rejects a decision before first revisit. No A5 physical outcome observed.'})
    common=docs+['SOURCE_IDENTITIES.json','INITIAL_STATE_SUMMARY.json','CODE_AND_RUNTIME_IDENTITIES.json','CLOCK_AUDIT.json','CIRCUIT_AND_RENEWAL_RATIONALE.json','RESOURCE_PROJECTION.json','RESOURCE_PLAN.md','PLANNING_EVIDENCE.json']
    protocol={'packet_status':'PROPOSED / NOT AUTHORIZED / HOLD','launch_disposition':'HOLD_CLOCK_INCOMPATIBILITY','launch_ready':False,'case_count':1,
       'reviewed_checkpoints':{'p_git_sha':P,'apparatus_git_sha':APP},'prior_evidence_status':{k:'OBSERVED' for k in ('A1','A2','A3','A4')},
       'bound_files':{n:sha(OUT/n) for n in common},'initial_snapshot_file':{'name':'INITIAL_A5.snapshot.json.gz','sha256':sha(OUT/'INITIAL_A5.snapshot.json.gz')},
       'fixture_label':'Byte-identical healthy A1/A2 manufactured external start; original provenance preserved; not newborn or continuation',
       'source_visit_order':[0,1,0,1],'schedule_interpretation':'Fixed absolute-clock target windows, no outcome-triggered switch or actual-contact guarantee; one completed return circuit plus second outbound leg.',
       'recording_contract':{'observer_symbol':'loom_commissioning.diagnostics.passive','observer_file_sha256':ai['files']['diagnostics.py'],'recorder_file_sha256':pi['files']['records.py'],
           'streams':['native','wave','events','controller','diagnostics','sensor','scientific_observations'],'native_hz':100,'decision_hz':10,'snapshots':'initial/final and every 1000 native steps; unchanged accumulated history',
           'post_read':'Saved data only; no world replay, command recomputation or sensor resampling. All-source plot contract in bound document.'},
       'record_destination':str(DEST/'trajectory-001'),'analysis_destination':str(DEST/'read-only-review'),
       'launch_preconditions':['HOLD must be resolved by a separate Jason ruling; do not execute this proposal as written','Any apparatus correction requires new verified identity and newly bound launch object','Future genuine approval, exact live identities, cache/snapshot/file verification, empty prospective output and adequate disk'],
       'stop_names':['terminal','apparatus_failure','administrative_pause','administrative_cutoff'],'failure_rule':'Report without patch, retry, resume, extension, route/phase substitution, reset or additional case.',
       'component_allowance':{'wall_seconds':3600,'world_steps':0,'scope':'Saved-data identity/continuity/ledger/milestone validation, reporting and packaging only'},
       'combined_new_disk_bytes':10000000000,'stop_request_disk_bytes':9000000000,'final_flush_reserve_bytes':1000000000,'free_disk_before_launch_bytes':10000000000,
       'excluded_work':['clock correction','new prehistory','P learning/perception tests','replays','counterfactual no-renewal runs','alternative circuits or phases','scientific lifetimes','cohorts','sweeps','tuning','every other commissioning case'],
       'legacy_roster_note':'Mandatory roster remains execution_authorized=false; no newborn life proposed.'}
    m.update(case_id='A5',duration_seconds=630.,hard_stop_time=630.,execution=authority.make_execution(contract.EXTERNAL,'waypoint',plan=STAGES,protocol=protocol,storage_limit=1500000000,wall_limit=14400),execution_authority=None)
    authority.validate_execution(m,complete=True);authority.validate_dispatch(m,vars(runner))
    assert all(abs(v['until']/.2-round(v['until']/.2))<1e-9 for v in STAGES)
    denial=None
    try:contract.authorize_execution(m)
    except ValueError as error:denial=str(error)
    assert denial=='commissioning execution is not authorized'
    write('A5_MANIFEST.json',m);obj=authority.execution_object(m);write('AUTHORITY_OBJECT.json',obj)
    (OUT/'AUTHORITY_OBJECT.canonical.json').write_bytes(authority.canonical(obj));h=sha(OUT/'AUTHORITY_OBJECT.canonical.json')
    txt('AUTHORITY_SHA256.txt',h+'  AUTHORITY_OBJECT.canonical.json\n')
    after={p:sha(p) for p in before};assert before==after
    assert not git('status','--porcelain').strip() and git('rev-parse','HEAD').decode().strip()==APP and not DEST.exists() and not FORBIDDEN
    write('HASH_AFTER.json',after)
    write('PREPARATION_CHECKS.json',{'world_steps':0,'field_steps':0,'neural_steps':0,'controller_commands':0,'simulation_RNG_draws':0,'new_prehistory_steps':0,'Engine_constructors':0,'Run_constructors':0,'sensor_evaluations':0,'trial_routes':0,'trial_phases':0,'replays':0,
       'forbidden_calls':FORBIDDEN,'snapshot_method':'Standard-library gzip/JSON/base64 read of exact copied bytes; no Engine object constructed or loaded','static_authority_and_dispatch_checks_pass':True,'null_grant_denial':denial,
       'production_history_validation_executed':False,'production_runtime_failure_reproduced':False,'scalar_clock_incompatibility_identified':True,'prospective_output_absent':True,'original_files_checked':len(before),'all_original_hashes_unchanged':True,
       'Git_writes':0,'vault_Git_writes':0,'code_or_config_edits':0,'worktree_clean':True,'preparation_wall_seconds':time.perf_counter()-started,'launch_ready':False})
    write('PRESERVATION.json',{'original_files_checked':len(before),'all_original_hashes_unchanged':True,'P_and_apparatus_unchanged':True,'configuration_unchanged':True,'worktree_clean':True,'Git_writes':0,'new_commit':None,'shared_workbench_navigation_edited':False,'A5_execution_occurred':False})
    print(json.dumps({'packet':str(OUT),'authority_sha256':h,'launch_ready':False,'clock_hold_at_native_index':26950,'preserved_files':len(before),'zero_world_steps':True,'rates':rates,'storage_totals':{k:v['predicted_total_bytes'] for k,v in storage_models.items()}},indent=2))
if __name__=='__main__':main()
