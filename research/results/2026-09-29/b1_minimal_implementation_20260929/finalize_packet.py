"""Bind the committed apparatus and static starts to nine ungranted proposals."""
import copy,datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,zipfile
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-minimal-20260929';D=W/'developmental_ecology'
OUT=S/'packet';E=ROOT/'exports/2026-09-29-B1-minimal-apparatus-a8cdd75'
BASE='b684912eaf7811cd318ee94c77172aca790f3a0d'
APP='a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad'
DESIGN=ROOT/'exports/2026-09-29-B1-minimal-closure-design-v0-2'
COUNTS={};BLOCKED=[]
def guard(frame,event,arg):
    if event!='call':return
    p=frame.f_code.co_filename.replace('\\','/');n=frame.f_code.co_name
    if '/loom_p/' not in p and '/loom_commissioning/' not in p:return
    if n in {'step','advance','prepare','draw','native','handoff','coupled','_coupled','command','waypoint_command','hold','begin_command','resume','from_verified_cache','load_restart'} or n=='__init__' and p.endswith(('/engine.py','/runner.py','/neural.py','/schema.py')):
        BLOCKED.append(p+':'+n);raise AssertionError('Finalizer cannot execute '+BLOCKED[-1])
    if n=='load_snapshot':COUNTS[n]=COUNTS.get(n,0)+1
sys.setprofile(guard);sys.path.insert(0,str(D))
from loom_p.records import code_identity,load_snapshot,state_hash
from loom_commissioning import authority,contract,runner,raw_reference

def sha(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()
def digest(b):return hashlib.sha256(b).hexdigest()
def js(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def write(n,v):
    p=OUT/n;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
def cp(p,n):
    q=OUT/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
def git(*args):
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c',
        'core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
def inventory_ok(root,name):
    inv=js(root/name)
    for n,v in inv['files'].items():
        p=(root/n).resolve();assert p.is_relative_to(root.resolve())
        assert sha(p)==v['sha256'] and p.stat().st_size==v['bytes']
    return len(inv['files'])

def main():
    assert not E.exists() and not (OUT/'AUTHORITY_INDEX.json').exists()
    assert git('rev-parse','HEAD').decode().strip()==APP and git('status','--porcelain')==b''
    assert git('rev-parse','HEAD^').decode().strip()==BASE
    frozen=js(OUT/'CONTROLLER_FROZEN_BEFORE_STARTS.json')['files']
    assert all(sha(D/n)==h for n,h in frozen.items())
    assert code_identity()['sha256']==contract.P_CODE
    preserved=['developmental_ecology/loom_p','developmental_ecology/configuration.json','developmental_ecology/requirements-lock.txt',
               'developmental_ecology/loom_commissioning/adapter.py','developmental_ecology/loom_commissioning/clock.py',
               'developmental_ecology/loom_commissioning/controllers.py','developmental_ecology/loom_commissioning/operator_view.py',
               'developmental_ecology/loom_commissioning/sensor.html','developmental_ecology/loom_commissioning/sensor_ui.py']
    assert git('diff','--name-only',BASE,APP,'--',*preserved)==b''
    for p in (D/'loom_p').glob('*.py'):
        assert p.read_bytes()==git('show',contract.BASELINE+':developmental_ecology/loom_p/'+p.name)
    for name in ('README.md','IMPLEMENTATION_REPORT.md','COMPONENT_TEST_REPORT.md','RESOURCE_AND_EXECUTION_PLAN.md','COMPONENT_JUNIT.xml'):
        cp(S/name,name)
    cp(DESIGN/'APPARATUS_PROVENANCE_CLARIFICATION.md','APPARATUS_PROVENANCE_CLARIFICATION.md')
    cp(DESIGN/'B1_MINIMAL_CLOSURE_DESIGN_v0_2.md','accepted-design/B1_MINIMAL_CLOSURE_DESIGN_v0_2.md')
    cp(DESIGN/'PRODUCTION_DIFF_352f_to_b684.txt','historical-provenance/PRODUCTION_DIFF_352f_to_b684.txt')
    cp(DESIGN/'PROVENANCE_BYTE_PROOF.json','historical-provenance/PROVENANCE_BYTE_PROOF.json')
    for name in ('prepare_starts.py','finalize_packet.py'):cp(S/name,'preparation/'+name)
    cp(D/'tests_apparatus/test_b1_minimal.py','tests/test_b1_minimal.py')
    for folder in ('loom_p','loom_commissioning'):
        for p in sorted((D/folder).iterdir()):
            if p.suffix in ('.py','.html'):cp(p,'instrument/developmental_ecology/'+p.relative_to(D).as_posix())
    for name in ('configuration.json','requirements-lock.txt'):cp(D/name,'instrument/developmental_ecology/'+name)
    (OUT/'IMPLEMENTATION.diff').write_bytes(git('diff','--binary',BASE,APP))
    (OUT/'COMPONENT_FINAL.txt').write_text('Observed tool output for the final focused suite, also retained as machine-written JUnit XML:\n35 passed in 1.17s\nCommand: Python 3.13.5 -B -X utf8 -m pytest -p no:cacheprovider developmental_ecology/tests_apparatus/test_b1_minimal.py --basetemp <workspace>/b1_minimal_implementation_20260929/component-03 -q --tb=short --junitxml=<workspace>/b1_minimal_implementation_20260929/COMPONENT_JUNIT.xml\nNo physical execution; inert scheduler stubs only.\n',encoding='utf-8')
    write('TEST_HISTORY.json',dict(initial_RED='Expected ImportError: raw_reference did not exist. No production implementation at that point.',
        intermediate=[dict(result='22 passed',scope='Pure controller tests'),
                      dict(result='22 passed / 10 setup errors',reason='Default pytest temp directory inaccessible; fixed by workspace basetemp.'),
                      dict(result='31 passed / 1 failed',reason='Test spy added bound method to sensor snapshot dictionary; removed spy attribute before close.'),
                      dict(result='32 passed',scope='Controller and runner components')],
        final=dict(result='35 passed',seconds=1.17,junit='COMPONENT_JUNIT.xml'),
        world_steps=0,field_steps=0,prehistory_steps=0,simulation_RNG_draws=0,
        manufactured_scheduler_ticks=13,held_out_controller_calls=0))
    checkpoint=dict(P=contract.BASELINE,apparatus_commit=APP,parent=BASE,
        last_independently_reviewed_operator='352f73fffa6d9781eae8aa38e708a9a05669588f',
        branch=git('branch','--show-current').decode().strip(),worktree=str(W),source=contract.apparatus_identity(),
        p_code=code_identity(),configuration=contract.CONFIG,runtime=authority.runtime_identity(),
        implementation_diff_sha256=sha(OUT/'IMPLEMENTATION.diff'),new_independent_review_claim=False)
    write('CHECKPOINT.json',checkpoint)
    source_paths=[D/n for n in frozen]+[D/'configuration.json',D/'requirements-lock.txt']
    write('SOURCE_IDENTITIES.json',dict(files={str(p.relative_to(D)):dict(sha256=sha(p),bytes=p.stat().st_size) for p in source_paths},
        unchanged_from_b684=preserved,all_P_source_bytes_identical_to_baseline=True,controller_frozen_before_starts=True))
    rp=js(DESIGN/'RESOURCE_ARITHMETIC.json')
    caps=dict(maximum_attempts_per_case=1,total_simulated_seconds=270,total_native_steps=27000,total_command_holds=2700,
        wall_per_case_seconds=600,aggregate_execution_wall_seconds=5400,read_only_reporting_seconds=1800,
        stream_cap_per_case_bytes=1500000000,combined_new_artifact_cap_bytes=20000000000,
        stop_request_bytes=19000000000,flush_reserve_bytes=1000000000,minimum_free_bytes=20000000000)
    write('RESOURCE_PROJECTION.json',dict(caps=caps,base_simulation_minutes=rp['base_simulation_minutes'],
        primary_case_projection_bytes=rp['primary_bytes'],with_second_full_copy_bytes=rp['primary_plus_second_full_copy_bytes'],
        rate_source=rp['recorded_wall_per_simulated_second'],overhead_measured=False,
        free_disk_bytes_at_preparation=shutil.disk_usage(ROOT).free,
        new_prehistory=0,models_or_training=0,old_grants_reused=False,
        limitations=['Projection is not throughput verification.','Existing runner caps count uncompressed streams; all-file aggregate guard required at execution.','Native-step/flush wall overshoot possible.']))
    order=['B1-MINIMAL-'+s+'-'+arm for s in ('S1','S2','S3') for arm in raw_reference.ARMS]
    common=['RESOURCE_AND_EXECUTION_PLAN.md','RESOURCE_PROJECTION.json','CHECKPOINT.json','SOURCE_IDENTITIES.json',
            'MATCHED_INITIAL_STATE_PROOF.json','PREHISTORY_REUSE.json','STATIC_PREPARATION_CHECKS.json',
            'accepted-design/B1_MINIMAL_CLOSURE_DESIGN_v0_2.md']
    members=[];denials=[]
    for start in ('S1','S2','S3'):
        summary=js(OUT/'starts'/start/'START_MANIFEST.json')
        for arm in raw_reference.ARMS:
            cid='B1-MINIMAL-'+start+'-'+arm;sub='cases/'+cid
            path=OUT/sub/'INITIAL.snapshot.json.gz';e=load_snapshot(path)
            assert state_hash(e)==summary['state_sha256'] and sha(path)==summary['snapshot_sha256']
            init=copy.deepcopy(summary['initialization']);init['prepared_apparatus_checkpoint']=APP
            m=contract.make_manifest(e,cid,contract.EXTERNAL,raw_reference.KIND,30.,purpose='commissioning',
                initialization=init,protocol=dict(reference_arm=arm,design_sha256=raw_reference.DESIGN),
                storage_limit=1500000000,wall_limit=600)
            authority.validate_execution(m,complete=True);authority.validate_dispatch(m,vars(runner))
            try:contract.authorize_execution(m)
            except ValueError as ex:
                assert str(ex)=='commissioning execution is not authorized';denials.append(cid)
            else:raise AssertionError('Proposal accidentally grants execution')
            write(sub+'/MANIFEST.json',m)
            execution=authority.execution_object(m);raw=authority.canonical(execution)
            (OUT/sub/'EXECUTION_OBJECT.canonical.json').write_bytes(raw)
            proposal=dict(schema='loom-B1-minimal-single-case-authority-v1',status='PROPOSED / NOT AUTHORIZED',
                case_id=cid,reference_arm=arm,P=contract.BASELINE,apparatus_checkpoint=APP,
                initial_snapshot=dict(file=sub+'/INITIAL.snapshot.json.gz',sha256=sha(path),state_sha256=state_hash(e)),
                start_manifest=dict(file='starts/'+start+'/START_MANIFEST.json',sha256=sha(OUT/'starts'/start/'START_MANIFEST.json')),
                execution_sha256=digest(raw),execution_object=execution,shared_batch_order=order,shared_resource_limits=caps,
                rules=dict(no_retry=True,no_continuation=True,no_substitution=True,no_tuning=True,no_extra_cases=True,
                    no_new_prehistory=True,case_authorization_does_not_authorize_others=True,
                    stop_batch_on=['preflight_failure','apparatus_failure','controller_exception','administrative_interruption','resource_cutoff'],
                    normal_ceiling_or_physical_terminal_may_proceed_only_to_next_separately_authorized_case=True),
                bound_documents={n:sha(OUT/n) for n in common},
                approval_workflow='Jason must separately authorize this canonical object hash. Only then may its exact execution object be placed in a genuine approval envelope. No grant is supplied here.')
            canonical=authority.canonical(proposal);h=digest(canonical)
            write(sub+'/AUTHORITY_OBJECT.json',proposal);(OUT/sub/'AUTHORITY_OBJECT.canonical.json').write_bytes(canonical)
            members.append(dict(case_id=cid,arm=arm,start=start,authority_sha256=h,execution_sha256=digest(raw),
                object_file=sub+'/AUTHORITY_OBJECT.canonical.json',manifest_file=sub+'/MANIFEST.json'))
    assert len({x['authority_sha256'] for x in members})==9 and len(denials)==9
    assert COUNTS=={'load_snapshot':9} and not BLOCKED
    write('AUTHORITY_INDEX.json',dict(status='NINE SEPARATE PROPOSALS / ZERO GRANTS',case_order=order,cases=members))
    full=ROOT/'b1_execution_20260929_colours_01/private';hidden=ROOT/'b1_hidden_execution_20260929_01/private'
    full_count=inventory_ok(full,'COMPLETED_ATTEMPT_FILE_MANIFEST.json');hidden_count=inventory_ok(hidden,'WITHDRAWN_FILE_MANIFEST.json')
    write('VERIFICATION.json',dict(checkpoint=APP,worktree_clean=git('status','--porcelain')==b'',
        component_checks_passed=35,world_cases_executed=0,physical_native_steps=0,field_steps=0,neural_steps=0,
        new_prehistory_steps=0,controller_calls_on_prepared_starts=0,simulation_RNG_draws_during_preparation=0,
        preparation_transductions_at_time_zero=3,finalization_allowed_calls=COUNTS,blocked_dynamic_calls=BLOCKED,
        fresh_three_starts_admissible=True,complete_triplet_snapshot_bytes_identical=True,
        null_grant_rejected_cases=denials,proposed_authorities=9,execution_grants=0,
        full_raw_human_files_verified_opaque=full_count,hidden_human_files_verified_opaque=hidden_count,
        old_human_B1_fixture_or_evaluator_decoded=False,full_human_record_preserved=True,hidden_human_withdrawal_preserved=True,
        P_world_sensor_actuator_viability_cadence_and_UI_preserved=True,
        production_history_loader_preflight='Deferred until authorization; static exact cache law/bytes/dependencies already verified.',
        no_new_independent_review_claim=True,no_push_PR_merge=True,no_vault_Git_writes=True,
        current_scope_complete='Implementation, components, static starts and proposals only; stop for Jason review.'))
    files={p.relative_to(OUT).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(OUT.rglob('*')) if p.is_file()}
    write('FILE_MANIFEST.json',dict(files=files,excludes_self=True,not_an_execution_authority=True))
    shutil.copytree(OUT,E)
    archive=E.with_suffix('.zip');assert not archive.exists()
    with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(E.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(E))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None and set(z.namelist())==set(files)|{'FILE_MANIFEST.json'}
        for name in z.namelist():assert digest(z.read(name))==sha(E/name)
    receipt=dict(checkpoint=APP,branch=checkpoint['branch'],worktree=str(W),package=str(E),archive=str(archive),archive_sha256=sha(archive),
                 files=len(files)+1,component_tests=35,world_cases_executed=0,authority_hashes={m['case_id']:m['authority_sha256'] for m in members})
    (S/'DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
