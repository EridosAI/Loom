"""Held B1 packet authoring: zero-time snapshots, pure validation, no Run or steps.

PRIVILEGED PREPARATION SOURCE. Do not show this file to the trial operator.
No trajectory search, controller call, RNG draw, field update or UI server.
"""
import ast,collections,copy,gzip,hashlib,json,math,os,pathlib,shutil,subprocess,sys,time,zipfile

S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-clock-correction-20260926';D=W/'developmental_ecology'
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
E=ROOT/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58'
PUB=E/'B1_OPERATOR_REVIEW';PRIV=E/'B1_PRIVILEGED_EVALUATOR_HOLD'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f';APP='68db2c581f07200966d699a4f55a65f9b96df1e9'
A5=ROOT/'exports/2026-09-26-A5-launch-packet-68db2c58'
A5R=ROOT/'exports/2026-09-26-A5-commissioning-result-68db2c58/A5_COMMISSIONING_RESULT'
REQ=pathlib.Path(r'C:\Users\Jason\.codex\attachments\c449df73-7b07-4616-99d2-a69e0d47c5a9\Pasted text.txt')
DES=ROOT/'exports/2026-09-23-p-commissioning-design-2fb3ff84/PACKAGE'
CALLS=collections.Counter();FORBIDDEN=[]

def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def canonical(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def digest(v):return hashlib.sha256(canonical(v)).hexdigest()
def js(p):return json.loads(pathlib.Path(p).read_bytes())
def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def txt(p,v):
    p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('x',encoding='utf-8',newline='\n') as f:f.write(v.strip()+'\n')
def cp(p,q):q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
def git(*args,repo=W):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+repo.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(repo),*args],env=env)

def guard(frame,event,arg):
    if event!='call':return
    code=frame.f_code;path=code.co_filename.replace('\\','/')
    if '/loom_p/' not in path and '/loom_commissioning/' not in path:return
    CALLS[path.rsplit('/',1)[-1]+':'+code.co_name]+=1
    # Loading existing objects uses __new__, never their constructors. Raw
    # transduction is permitted once per predetermined zero-time fixture only.
    blocked={'step','advance','_coupled','run_bounded','prepare','draw','native','handoff',
             'waypoint_command','privileged_input','command_pair','begin_command','hold',
             'resume','load_restart','save_restart','authorize_execution','from_verified_cache','load',
             'account','actuator_forces','free_velocity','project_velocity','reconstruct','verify_segment'}
    if code.co_name in blocked or code.co_name=='__init__':
        FORBIDDEN.append(path+':'+code.co_name)
        raise AssertionError('Preparation forbids execution: '+FORBIDDEN[-1])

def seal(root):
    files={p.relative_to(root).as_posix():dict(bytes=p.stat().st_size,sha256=sha(p)) for p in sorted(root.rglob('*')) if p.is_file()}
    write(root/'FILE_MANIFEST.json',dict(files=files))
    archive=root.with_suffix('.zip')
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(root).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert set(z.namelist())==set(files)|{'FILE_MANIFEST.json'}
        for n,v in files.items():
            b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256']
    return dict(archive=archive.name,sha256=sha(archive),bytes=archive.stat().st_size,payloads=len(files),verified=True)

def main():
    assert not E.exists(),'Existing packet must be preserved'
    assert git('rev-parse','HEAD').decode().strip()==APP and not git('status','--porcelain').strip()
    sources={
      'REQUEST.txt':REQ,
      'project/AGENTS.md':ROOT/'AGENTS.md',
      'project/00_LOOM_CURRENT_STATE.md':ROOT/'sources/00_LOOM_CURRENT_STATE(2).md',
      'workbench/AGENTS.md':WB/'AGENTS.md',
      'workbench/00_RESEARCH_MAP.md':WB/'00_RESEARCH_MAP.md',
      'workbench/01_WORKSPACE_STATUS.md':WB/'01_WORKSPACE_STATUS.md',
      'design/P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md':DES/'P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md',
      'design/P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md':DES/'P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md',
      'design/P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md':DES/'P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md',
      'reviews/LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md':ROOT/'exports/2026-09-24-p-independent-apparatus-intake-b92e45a7/SOURCE_BATCH/LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md',
      'reviews/FINAL_CLOCK_REVIEW.md':WB/'90_SOURCES/p_final_clock_review_2026-09-26_3af846d2/LOOM_P_NARROW_FINAL_CLOCK_REVIEW.md',
      'scope/APPARATUS_SCOPE.md':WB/'40_DECISIONS/DECISION-P-APPARATUS-SCOPE-2026-09-24-73c9ad61.md',
      'A5/RESOURCE_RESULT.json':A5R/'RESOURCE_RESULT.json',
      'A5/A5_FINAL_RESULT_SUMMARY.json':A5R/'A5_FINAL_RESULT_SUMMARY.json',
      'A5/FINAL_PRESERVATION.json':A5R/'FINAL_PRESERVATION.json',
      'A5/DELIVERY_RECEIPT.json':A5R.parent/'DELIVERY_RECEIPT.json',
      'initial-template.snapshot.json.gz':A5/'INITIAL_A5.snapshot.json.gz',
      'initial-template-manifest.json':A5/'A5_MANIFEST.json'}
    for p in (D/'loom_p').glob('*.py'):sources['instrument/loom_p/'+p.name]=p
    for p in (D/'loom_commissioning').iterdir():
        if p.suffix in ('.py','.html'):sources['instrument/loom_commissioning/'+p.name]=p
    sources['instrument/configuration.json']=D/'configuration.json'
    for sub in ('p_apparatus_20260924','p_apparatus_correction_20260924','p_apparatus_final_correction_20260925','p_clock_correction_20260926'):
        for p in (W/'docs/developmental_ecology'/sub).glob('*.md'):sources['instrument-docs/'+sub+'/'+p.name]=p
    for p in (D/'artifacts/prehistory-attempt-001').rglob('*'):
        if p.is_file():sources['verified-cache/'+p.relative_to(D/'artifacts/prehistory-attempt-001').as_posix()]=p
    original={str(p):sha(p) for p in sources.values()}
    # Preserve the previous run/package's seal itself and selected result files.
    original[str(A5R/'FILE_MANIFEST.json')]=sha(A5R/'FILE_MANIFEST.json')
    E.mkdir(parents=True);PUB.mkdir();PRIV.mkdir()
    probe=E/'temporary-access-check.txt';probe.write_text('scoped read/write check',encoding='utf-8')
    assert probe.read_text()=='scoped read/write check';probe.unlink()
    write(PRIV/'SOURCE_IDENTITIES.json',{n:dict(path=str(p),sha256=sha(p),bytes=p.stat().st_size) for n,p in sources.items()})
    for n,p in sources.items():cp(p,PRIV/'references'/n)
    write(PRIV/'ORIGINALS_BEFORE.json',original)
    sys.path.insert(0,str(D));sys.setprofile(guard)
    import numpy as np
    from loom_p.records import load_snapshot,save_snapshot,state_hash,state_bytes,view,code_identity
    from loom_p.geometry import transduce,fixtures,gap_normal
    from loom_commissioning.contract import make_manifest,EXTERNAL,apparatus_identity
    from loom_commissioning.authority import validate_execution,execution_object,execution_sha256,runtime_identity
    from loom_commissioning import clock
    template=load_snapshot(A5/'INITIAL_A5.snapshot.json.gz');base=js(A5/'A5_MANIFEST.json')
    assert code_identity()['sha256']==base['p_code'] and apparatus_identity()==base['apparatus']
    assert runtime_identity()==base['execution']['runtime']
    init=base['initialization'];cache=pathlib.Path(init['cache_directory'])
    cache_receipt=js(cache/'manifest.json')
    assert sha(cache/'manifest.json')==init['cache_receipt_sha256']
    assert hashlib.sha256(template.fields.tobytes()).hexdigest()==base['initial_fields']==init['field_sha256']==cache_receipt['field_sha256']
    assert template.phase==base['phase']==init['phase']==cache_receipt['phase']
    assert cache_receipt['status']=='complete' and cache_receipt['life']==init['birth_id']
    assert cache_receipt['steps_completed']==cache_receipt['steps_required'] and cache_receipt['end_time']==0
    rng_before=state_hash(template.organism.rng);neural_before=state_hash(template.organism)
    # Exactly one deterministic, geometry-selected test proposal; no trajectory,
    # signal, force, or outcome is evaluated to choose or replace its start.
    selector=hashlib.sha256(('first-B1-held-out-start|'+APP+'|'+sha(REQ)).encode()).digest()
    candidates=[0,1,2,5,6,7]
    source_index=candidates[int.from_bytes(selector[:4],'big')%len(candidates)]
    target=np.array(template.c.source_positions[source_index],dtype=float)
    offset=np.array([2.5 if target[0]<10 else -2.5,1. if target[1]<10 else -1.])
    position=target+offset;angle=float(math.atan2(-offset[1],-offset[0])+.55)
    configs=[
      dict(id='PC-LR',seconds=4,position=[4.2,3.8],angle=0.,description='Disclosed asymmetric raw sensory reading'),
      dict(id='PC-MOTION',seconds=4,position=[6.,5.],angle=0.,description='Disclosed free-space command and achieved-motion distinction'),
      dict(id='PC-CONTACT',seconds=6,position=[.65,6.],angle=math.pi,description='Disclosed approach to a plain boundary wall'),
      dict(id='PC-HOLD',seconds=10,position=[.52,6.],angle=math.pi,description='Disclosed near-wall gentle contact hold'),
      dict(id='B1-PAIR-INITIAL',seconds=30,position=position.tolist(),angle=angle,description='Single held-out, manufactured external-controller state; not a sampled newborn')]
    write(PRIV/'PREDECLARED_INITIAL_FIXTURES.json',dict(selection_sha256=selector.hex(),selection_policy='One hash-selected member of the declared static bottom/top-row opportunity set, with a fixed offset and heading offset; no alternatives tried. Middle-row opportunities excluded geometrically to avoid importing an A4 mover challenge.',
       source_index_evaluator_only=source_index,fixtures=configs,phase_history='Reuse the existing lawful body-absent life-0 field cache. No new field history or phase. Phase reuse is a prior-knowledge limitation; do not assert an unfamiliar phase.',
       held_out_scope='New complete body state and its raw interface have not been shown to the operator in preparation. General world knowledge and previous phase knowledge cannot be erased. Exposure declaration required before any future trial.'))
    control_gates=dict(schema=1,order=['PC-LR','PC-MOTION','PC-CONTACT','PC-HOLD','B1-FULL-RAW','B1-CHEMISTRY-HIDDEN'],
       all_statuses_now='NOT DEMONSTRATED — NOT EXECUTED',automatic_launch=False,
       B1_gate='All four operator controls explicitly documented as demonstrated, no unqualified test-state exposure, apparatus holds closed independently, new exact execution objects and Jason authorization. No automatic launch on a score.',
       evaluation_release='Positive-control evaluation may be reviewed after each disclosed control. Withhold both B1 evaluator views until both paired trials have ended or the pair is explicitly abandoned; full-raw feedback cannot guide the hidden trial.',
       no_retry=True,no_extension=True,no_substitution=True)
    write(PUB/'CONTROL_GATE.json',control_gates)
    display=dict(schema=1,reviewed_checkpoint=APP,reviewed_files={n:base['apparatus']['files'][n] for n in ['sensor.html','sensor_ui.py','controllers.py','runner.py','authority.py','pending.py']},
       permitted=dict(raw_native_coordinates=[10,4,8,7],raw_cadence_seconds=.01,EI_handoff_seconds=.2,EI_between_handoffs='held previous sample',own_commands=True,own_notes=True,ordered_history=True),
       forbidden=['global position','truth heading/pose','world image/map','fixture/source identity or position','stock','mover phase/velocity','material labels','analytic gradients','privileged notifications','evaluation','future values'],
       physical_pause='No command request: zero world, bodily, field, native/P clock or RNG advancement. Wall resource timer continues.',
       control=dict(left_right_range=[-1,1],hold_seconds=.1,native_steps_per_hold=10,auto_repeat=False,command_batching=False,command_queue=False),
       full_raw=dict(kind='none',implemented_at_checkpoint=True),
       chemistry_hidden=dict(kind='chemistry_hidden',implemented_at_checkpoint=False,raw_flat_indices=[10,11,12,13],representation='Withheld at server boundary; absent/null display entries marked hidden, never zero-valued real readings.',
           all_egress='Withhold from current values, plots, all past history, HTTP payload, downloads, notes/autofill and user-visible controller transcripts. Complete actual 29-coordinate raw stream retained evaluator-only.',
           physical_changes=False,other_channels_unchanged=True,implementation_sha256=None),
       prelaunch_gaps=['Checkpoint accepts display_intervention none only.','Page does not show running/in-flight state or disable the send button during an outstanding request.','Closed Run still exposes availability paused; lifecycle stop handling needs explicit reviewed integration.','Live launcher is not supplied by sensor_ui.main; it opens offline records only.'])
    write(PUB/'DISPLAY_CONTRACT.json',display)
    recording=dict(schema=1,operator_record=['every exact raw value delivered/shown with time/native index','display formatting/version and condition','cadence-held E/I and sample timestamp','human commands and request/response wall timestamps','own notes','shown history and display condition changes, if any','pause/running/ended state','operator exposure declarations'],
       evaluator_record=['unaltered full 29 raw coordinates including hidden chemistry','complete native body pose/velocity/forces/E/I','all eight source stocks and chemical field identities','all contacts/releases/impulses/damage/repair','source debit/body credit/renewal half-steps/expenditure','issued and delivered command ledger','initial/final complete snapshots and periodic restarts','stop reason, errors and incomplete tails','opportunity geometry and actual sampled trajectory'],
       separation='Operator endpoint serves only permitted condition-specific records. Evaluator files outside served paths and absent from operator bundle. No evaluator result released while either B1 trial remains active/pending.',
       fidelity='Native .01 s records retained; no subsampling, interpolation, synthetic hints or loss of native chronology.',
       source_state='Appearance does not directly encode stock; chemistry depends on stock, diffusion/history, position and occlusion. Depleted sources remain chemically present. No EMPTY flag.',
       display_masks_never_change_physics=True,post_trial_alignment='Exact indices/timestamps of actual raw chemistry and evaluator stock, retaining gaps, all costs and contact interruptions.',
       current_checkpoint_limit='Controller records contain the full SensorHistory at every decision, so raw display-history storage and validation grow quadratically in hold count. Masked egress/transcript contract is unimplemented and held.')
    write(PUB/'RECORDING_CONTRACT.json',recording)
    notes=dict(schema=1,operator='Jason',condition_order=['B1-FULL-RAW','B1-CHEMISTRY-HIDDEN'],
       controls='Manual bounded pair only. No AI, observer, waypoint, hint, control law, autoplay, or repeat-until-outcome driver.',
       trial_stops=['fixed native deadline','physical terminal E or I','apparatus/record/controller failure','wall/storage administrative stop','explicit operator withdrawal at paused boundary'],
       after_early_stop='Preserve prefix and reason. Do not resume, retry, replace, extend or switch to another controller automatically.',
       memory='FULL-RAW first preserves the primary naive-to-this-held-out-state witness. The second trial can benefit from human memory of the first; this fixed order is not counterbalanced and cannot establish chemistry necessity.',
       grants='None. Packet HOLD covers every case even where a full-display execution object is structurally valid.')
    write(PUB/'PROTOCOL_CONTRACT.json',notes)
    document_ids={p.name:sha(p) for p in PUB.glob('*.json')}
    states={};checks=[]
    for spec in configs:
        e=copy.deepcopy(template)
        e.body.position=np.array(spec['position'],dtype=float);e.body.angle=spec['angle']
        assert e.time==0 and e.native_index==0 and e.status=='paused'
        assert all(np.all(a==0) for a in [e.body.velocity,e.body.command,e.body.force,e.body.contact_rates]) and e.body.omega==0
        assert e.body.energy==.7 and e.body.integrity==1. and np.all(e.stocks==.2)
        scene=fixtures(e.c,0,e.phase);gaps=[float(gap_normal(e.body.position,e.c.body_radius,f)[0]) for f in scene]
        assert min(gaps)>=0,'Selected fixture is invalid; no replacement authorized'
        e.raw=transduce(e.c,e.body,e.fields,0,e.phase)
        assert state_hash(e.organism)==neural_before and state_hash(e.organism.rng)==rng_before
        e.validate_state()
        name='initial-states/'+spec['id']+'.snapshot.json.gz'
        (PRIV/'initial-states').mkdir(exist_ok=True)
        receipt=save_snapshot(PRIV/name,e)
        assert state_hash(load_snapshot(PRIV/name))==state_hash(e)
        states[spec['id']]=dict(file=name,sha256=receipt['sha256'],state_sha256=receipt['state_sha256'],bytes=receipt['bytes'])
        checks.append(dict(id=spec['id'],state_sha256=state_hash(e),time=0.,native_index=0,minimum_static_surface_gap=min(gaps),raw_widths=[len(r) for r in e.raw],raw_finite=all(np.isfinite(r).all() for r in e.raw),organism_unchanged=True,RNG_unchanged=True,fields_unchanged=np.array_equal(e.fields,template.fields)))
        if spec['id'].startswith('PC-'):
            write(PRIV/'positive-controls'/(spec['id']+'.initial-display.json'),dict(raw_labels=[f'{s}_{i}' for s,n in [('light',10),('chemistry',4),('contact',8),('proprioception',7)] for i in range(n)],raw=np.concatenate(e.raw).tolist(),actual_EI=[.7,1.],time=0,EI_sample_time=0,declared_fixture=spec,status='Prepared only; operator demonstration not performed'))
        states[spec['id']]['engine']=e
    write(PRIV/'INITIAL_STATE_CHECKS.json',checks)
    manifest_index=[]
    cases=[(s['id'],s['id'],s['seconds']) for s in configs[:-1]]+[('B1-FULL-RAW','B1-PAIR-INITIAL',30),('B1-CHEMISTRY-HIDDEN','B1-PAIR-INITIAL',30)]
    for case,initial,seconds in cases:
        protocol=dict(row='B1',operator='Jason',case_role='operator-positive-control' if case.startswith('PC-') else 'held-out-sensor-human-physical-witness',
            bound_documents=document_ids,paired_trial_order=['B1-FULL-RAW','B1-CHEMISTRY-HIDDEN'],
            human_actions='Only paired entries through the reviewed ten-step hold; all choices made by Jason from the permitted display.',
            admission='Entire packet HOLD. After a separately reviewed checkpoint and regenerated exact objects, genuine authorization plus positive-control/exposure gate required.',
            completion='Stop at first terminal/failure/resource cap/operator withdrawal or fixed native ceiling; no retry or automatic continuation.')
        m=make_manifest(states[initial]['engine'],case,EXTERNAL,'sensor_human',seconds,purpose='commissioning',initialization=copy.deepcopy(base['initialization']),protocol=protocol,
            storage_limit=256_000_000 if case.startswith('PC-') else 1_500_000_000,wall_limit=1200 if case.startswith('PC-') else 7200)
        valid=True;expected_rejection=None
        if case=='B1-CHEMISTRY-HIDDEN':
            m['execution']['display_intervention']={'kind':'chemistry_hidden','specification_sha256':sha(PUB/'DISPLAY_CONTRACT.json'),'implementation_sha256':None}
            try:validate_execution(m,complete=True)
            except ValueError as ex:
                assert str(ex)=='unsupported display intervention';valid=False;expected_rejection=str(ex)
            else:raise AssertionError('Unexpected hidden-display acceptance')
        else:validate_execution(m,complete=True)
        assert m['execution_authority'] is None and m['initial_state']==states[initial]['state_sha256']
        # Pure integer scheduling check, never calls a controller or scheduler step.
        end=clock.case_end(m)
        assert end==seconds*100
        assert all(clock.hold_steps(m,i)==10 for i in range(0,end,10))
        obj=execution_object(m);h=execution_sha256(m)
        write(PRIV/'case-manifests'/(case+'.json'),m)
        write(PRIV/'authority-objects'/(case+'.json'),obj)
        q=PRIV/'authority-objects'/(case+'.canonical.json');q.write_bytes(canonical(obj))
        assert sha(q)==h
        manifest_index.append(dict(case=case,initial_state_sha256=m['initial_state'],initial_snapshot_sha256=states[initial]['sha256'],
            duration_seconds=seconds,native_ceiling=end,command_holds=end//10,canonical_object_sha256=h,
            execution_specification_validation=valid,expected_rejection=expected_rejection,execution_grant=None,
            disposition='HELD — NOT EXECUTION AUTHORITY',hash_kind='canonical execution-object digest' if valid else 'rejected candidate digest; not a valid executable authority object'))
    assert manifest_index[-1]['initial_state_sha256']==manifest_index[-2]['initial_state_sha256']
    sys.setprofile(None)
    # Public exposure audit holds no B1 positions, phase values, stock or raw data.
    write(PUB/'CASE_AND_AUTHORITY_INDEX.json',dict(status='HOLD — no grants and no executable batch',P=P,apparatus=APP,cases=manifest_index))
    write(PRIV/'PRIVILEGED_EVALUATOR_MANIFEST.json',dict(status='HOLD / evaluator-only / no execution',P=P,apparatus=APP,
        initial_states={k:{n:v for n,v in val.items() if n!='engine'} for k,val in states.items()},
        phase=template.phase,initial_fields_sha256=base['initial_fields'],initialization=base['initialization'],
        P_inactive_neural_state_sha256=neural_before,RNG_state_sha256=rng_before,
        selected_B1_source=source_index,opportunity_geometry=template.c.source_positions,
        exact_B1_body_pose=dict(position=position.tolist(),angle=angle),case_manifests=manifest_index,
        geometry_rationale='Fixed inward offset from one source on an outer source row; positive initial clearance; no A4 mover crossing deliberately added. This is geometric opportunity, not measured dynamics or a sensor-control success forecast.',
        no_trials_or_phase_route_search=True,prior_knowledge='The existing lawful phase/cache is reused. Its prior disclosure is not erased. Obtain the operator declaration; if knowledge identifies this trial state, qualify/withhold blinded interpretation. Do not silently choose a new phase.',
        future_evaluation=['Verify operator-view versus actual permitted sensor rows and mask at every shown time; no evaluator leakage.',
            'Report signed native source surface distance, its minimum and approach change, all contact events and positive-duration contact separately.',
            'Measure exact source debit/body credit, gross transfer, total expenditure and net E; report every complete .2 s window and partial terminal interval separately.',
            'Preserve all eight stocks, chemistry/field history and exact raw stock-aligned data without adding EMPTY labels.',
            'Record trajectory, E/I, damage, repair, terminal/failure/resource/operator cutoff and full human transcript.',
            'Apply the interpretation table only after positive controls and integrity gates; a miss alone says nothing about absence of information.']))
    resource=js(A5R/'RESOURCE_RESULT.json');rate=resource['recorder_wall_seconds']/630
    projection=[]
    for c in manifest_index:
        n=c['command_holds'];repeated_rows=n+5*n*(n-1);past_commands=n*(n-1)//2
        # Conservative JSON byte envelopes. Notes may contain 1000 escaped
        # control characters (6 bytes each), not just ASCII prose.
        raw_bound=repeated_rows*1200;command_bound=past_commands*128;annotation_bound=past_commands*6200
        metadata_bound=n*10000;physical=math.ceil(resource['uncompressed_stream_bytes']/630*c['duration_seconds'])
        projection.append(dict(case=c['case'],seconds=c['duration_seconds'],holds=n,
            A5_compute_proxy_seconds=rate*c['duration_seconds'],human_overhead_measured=False,
            full_history_row_copies_in_controller_stream=repeated_rows,
            raw_history_bound_bytes=raw_bound,prior_commands_bound_bytes=command_bound,
            worst_case_prior_annotations_bound_bytes=annotation_bound,metadata_bound_bytes=metadata_bound,
            physical_stream_A5_proxy_bytes=physical,stream_planning_bound_bytes=raw_bound+command_bound+annotation_bound+metadata_bound+physical,
            snapshot_and_display_allowance_bytes=150_000_000 if n==300 else 50_000_000,
            retained_primary_planning_bytes=raw_bound+command_bound+annotation_bound+metadata_bound+physical+(150_000_000 if n==300 else 50_000_000),
            recorder_wall_limit_seconds=1200 if c['case'].startswith('PC-') else 7200,
            stream_limit_bytes=256_000_000 if c['case'].startswith('PC-') else 1_500_000_000))
    total_holds=sum(x['holds'] for x in projection);sim=sum(x['seconds'] for x in projection)
    projected=dict(status='Prospective limits only; not execution permission',measured_basis=resource,
        A5_seconds_wall_per_simulated_second=rate,cases=projection,total_simulated_ceiling=sim,total_holds=total_holds,
        A5_compute_proxy_total_seconds=rate*sim,
        deliberation_examples=[dict(seconds_per_decision=k,total_wall_minutes=(rate*sim+k*total_holds)/60) for k in [5,10,20]],
        uncertainty='A5 used a privileged waypoint input. Human command records contain growing histories, and validation/HTTP/DOM work differs. A5 is a base physics/recording proxy, not a measured human throughput forecast. No benchmark executed.',
        combined_new_artifact_cap_bytes=12_000_000_000,stop_request_bytes=11_000_000_000,flush_reserve_bytes=1_000_000_000,
        prelaunch_free_space_required_bytes=12_000_000_000,post_trial_reporting_allowance_seconds=3600,
        maximum_retentions=4,combined_primary_copy_planning_bytes=4*sum(x['retained_primary_planning_bytes'] for x in projection),
        no_native_fidelity_reduction=True,no_automatic_extension=True)
    write(PUB/'RESOURCE_PROJECTION.json',projected)
    source_lines={}
    needles={'authority.py':['unsupported display intervention','def validate_execution'],
             'sensor.html':['function render()','document.querySelector(\'#at\').oninput'],
             'sensor_ui.py':['class HumanGateway','def main'],
             'runner.py':["inputs=self.sensor.display()","'inputs':inputs","return self.sensor.display()"]}
    for name,terms in needles.items():
        lines=(D/'loom_commissioning'/name).read_text(encoding='utf-8').splitlines()
        source_lines[name]={term:[i for i,line in enumerate(lines,1) if term in line] for term in terms}
    write(PUB/'STATIC_COMPATIBILITY_FINDINGS.json',dict(source_checkpoint=APP,source_hashes=base['apparatus']['files'],locations=source_lines,
        chemistry_hidden='REJECTED by pure validate_execution: unsupported display intervention',
        live_status='STATIC SOURCE FINDING: render uses Paused between decisions for every live payload; click handler does not set in-flight state or disable submit before fetch.',
        closed_status='STATIC SOURCE FINDING: Run.close does not change SensorHistory availability; HumanGateway.display returns Run.display without closed-state translation.',
        live_launch='Existing main() constructs OfflineGateway only. HumanGateway exists but needs a separately authorized, identity-bound live integration.',
        no_static_workaround='No CSS overlay, false zero chemistry, unbound client masking, command macro, altered cadence or controller fallback was prepared.'))
    write(PUB/'PREPARATION_CHECKS.json',dict(P=P,apparatus=APP,platform=sys.platform,python=sys.version,
        local_scoped_read_write_check=True,git_head_exact=True,git_clean=True,
        worlds_constructed=0,Run_constructors=0,native_steps=0,field_steps=0,prehistory_steps=0,
        controller_command_calls=0,simulation_RNG_draws=0,human_trials=0,positive_control_demonstrations=0,
        initial_sensor_transductions=CALLS['geometry.py:transduce'],predetermined_distinct_initial_states=5,
        state_roundtrip_checks=5,pair_complete_initial_state_identical=True,pure_execution_specifications_accepted=5,
        unsupported_hidden_candidate_rejected=True,forbidden_call_attempts=FORBIDDEN,
        call_inventory=dict(sorted(CALLS.items())),clarification='Only static identities/geometry, five predetermined zero-time copies and initial raw transduction, serialization and pure contract/clock checks. No trajectory, command, human action, RNG draw, or field evolution.'))
    assert CALLS['geometry.py:transduce']==5 and not FORBIDDEN
    assert original=={p:sha(p) for p in original}
    assert not git('status','--porcelain').strip() and git('rev-parse','HEAD').decode().strip()==APP
    write(PRIV/'ORIGINALS_AFTER.json',{p:sha(p) for p in original})
    write(PUB/'PRESERVATION.json',dict(original_files_checked=len(original),all_unchanged=True,code_worktree_clean=True,P_unchanged=True,apparatus_unchanged=True,
        configuration_unchanged=True,world_body_sensor_laws_unchanged=True,existing_evidence_unchanged=True,
        git_writes=0,dependency_changes=0,workbench_canon_or_navigation_changes=0))
    cp(pathlib.Path(__file__),PRIV/'AUTHORING_SOURCE.py')
    cp(S/'write_documents.py',PRIV/'DOCUMENT_AUTHORING_SOURCE.py')
    # Documents are authored separately, without any B1 privileged scalar.
    from write_documents import documents
    documents(PUB,PRIV,manifest_index,projected,source_lines)
    held=dict(schema='B1_HELD_REVIEW_OBJECT_V1',status='HOLD_NOT_EXECUTABLE',P=P,apparatus=APP,
        cases=manifest_index,execution_grants=None,interface_version_sha256=digest(display),
        deprivation_implementation=None,case_order=control_gates['order'],required_gate_sha256=digest(control_gates),
        public_documents={p.relative_to(PUB).as_posix():sha(p) for p in sorted(PUB.rglob('*')) if p.is_file()},
        privileged_documents={p.relative_to(PRIV).as_posix():sha(p) for p in sorted(PRIV.rglob('*')) if p.is_file()},
        meaning='Review/custody object only. This is not an executable batch accepted by the current apparatus. Chemistry-hidden implementation and reviewed live lifecycle are absent. A later corrected checkpoint requires regenerated exact authorities and Jason authorization.')
    write(PRIV/'HELD_REVIEW_OBJECT.json',held)
    (PRIV/'HELD_REVIEW_OBJECT.canonical.json').write_bytes(canonical(held));h=digest(held)
    private_archive=seal(PRIV)
    write(PUB/'HELD_REVIEW_IDENTITY.json',dict(sha256=h,status='HOLD — review identity, NOT execution authority',private_archive=private_archive,
        no_grants=True,next_decision='Jason may separately authorize the narrowly specified apparatus work and independent review. Do not execute this packet.'))
    public_archive=seal(PUB)
    receipt=dict(P=P,apparatus=APP,held_review_sha256=h,public=public_archive,privileged=private_archive,
        simulation_steps=0,controller_calls=0,new_prehistory_steps=0,initial_sensor_transductions=5,all_payloads_verified=True,
        packet_status='PREPARED / HOLD / NOT LAUNCH-READY',operator_material_contains_no_B1_state=True)
    write(E/'PACKAGE_RECEIPT.json',receipt)
    txt(E/'README.md','''# B1 perceptual-ceiling preparation — HOLD

Open B1_OPERATOR_REVIEW/README.md and OPERATOR_INSTRUCTIONS.md for safe review. The operator ZIP contains no B1 test pose, phase, geometry, stocks or initial sensor readings.

B1_PRIVILEGED_EVALUATOR_HOLD.zip contains the hidden snapshots, exact manifests, source material and evaluator instructions. Jason should not inspect that archive or the expanded evaluator directory before completing both trials if he will be the sensor-only operator. Separation is a workflow/custody boundary, not protection against the machine owner.

No execution grants or launcher are supplied. Chemistry deprivation and live status/lifecycle handling are not implemented sufficiently at the pinned checkpoint. These are preparation findings, not perceptual or P failures. The packet is held for a separate narrow apparatus decision and review.
''')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
