"""Single authorized attempt; no batch dispatch, retry, continuation or replay."""
from pathlib import Path
import copy,datetime,hashlib,json,os,shutil,subprocess,sys,time,traceback
S=Path(__file__).resolve().parent;ROOT=S.parent;OUT=S/'run-001'
W=ROOT/'worktrees/loom-p-b1-minimal-20260929';D=W/'developmental_ecology'
R=ROOT/'exports/2026-09-29-B1-S1-sensory-free-900s-proposal'
ORIGINAL=ROOT/'exports/2026-09-29-B1-minimal-apparatus-a8cdd75'
PRIOR=ROOT/'b1_minimal_execution_20260929'
CASE='B1-MINIMAL-S1-SENSORY-FREE'
APP='a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad'
AUTH='57386e964ea018050bedc18a397e4611203926626e4363c2c9b04d79c9fc5ba2'
EXE='97bf333344bc97c2bdf7bd61f2ce0c758a75a9f7201561ca297d3539c6fe565f'
COUNT=[S,PRIOR,ROOT/'b1_minimal_implementation_20260929',ROOT/'b1_minimal_closure_design_20260929',
 ORIGINAL,ORIGINAL.with_suffix('.zip'),ROOT/'exports/2026-09-29-B1-minimal-closure-results-a8cdd75',
 ROOT/'exports/2026-09-29-B1-minimal-closure-results-a8cdd75.zip',R,R.with_suffix('.zip'),
 ROOT/'b1_s1_sensory_free_resource_proposal_20260929',
 ROOT/'exports/2026-09-29-B1-S1-paired-closure-a8cdd75',ROOT/'exports/2026-09-29-B1-S1-paired-closure-a8cdd75.zip']
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def check(ok,why):
    if not ok:raise ValueError(why)
def sha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    return h.hexdigest()
def save(p,v):
    with Path(p).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(v,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def inventory(p):return {x.relative_to(p).as_posix():{'sha256':sha(x),'bytes':x.stat().st_size} for x in sorted(p.rglob('*')) if x.is_file()}
def resources():
    def size(p):return p.stat().st_size if p.is_file() else sum(x.stat().st_size for x in p.rglob('*') if x.is_file()) if p.exists() else 0
    return {'combined_new_bytes':sum(size(p) for p in COUNT),'free_bytes':shutil.disk_usage(ROOT).free}
def git(*args):return subprocess.check_output(['git','-c',f'safe.directory={W.as_posix()}',
 '-c',f'core.excludesFile={ROOT / "a5_regeneration_20260926/empty-excludes"}','-C',str(W),*args],
 env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),text=True).strip()
def emit(event,**kw):
    row={'utc':utc(),'event':event,**kw}
    with (OUT/'operations.jsonl').open('a',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(row,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(row),flush=True)
def main():
    # Exclusive durable claim prevents a second invocation, even after failure.
    OUT.mkdir(exist_ok=False);(OUT/'cases').mkdir()
    save(OUT/'ONE_ATTEMPT_CLAIM.json',{'utc':utc(),'pid':os.getpid(),'only_case':CASE,'checkpoint':APP,
       'outer_authority_sha256':AUTH,'supervisor_sha256':sha(__file__),'authorization_sha256':sha(S/'USER_AUTHORIZATION.md')})
    stage='preflight';attempted=False;run=None;e=None;before_prior=None;stop=None;start=None
    preflight={'started_utc':utc(),'status':'INCOMPLETE'}
    try:
        sys.path.insert(0,str(D))
        from loom_p.records import load_snapshot,state_hash,code_identity
        from loom_commissioning.authority import canonical,strict_loads,execution_object,execution_sha256,runtime_identity,validate_execution,validate_dispatch
        from loom_commissioning.contract import apparatus_identity,validate_manifest,authorize_execution
        from loom_commissioning import runner
        read=lambda p:strict_loads(Path(p).read_bytes())
        check(os.name=='nt','actual Windows runtime required')
        check(git('rev-parse','HEAD')==APP and git('status','--porcelain=v1','--untracked-files=all')=='','checkpoint wrong or dirty')
        before_prior=inventory(PRIOR);save(OUT/'PRESERVED_FULL_AND_PRIOR_INVENTORY.json',before_prior)
        past=read(PRIOR/'run-001/EXECUTION_RESULT.json')
        check(past['attempted']==['B1-MINIMAL-S1-FULL'] and CASE in past['not_attempted'],'case already attempted or prior batch altered')
        check(not (PRIOR/'run-001/cases'/CASE).exists(),'case destination already exists in prior batch')
        packet=read(R/'FILE_MANIFEST.json')['files']
        for rel,v in packet.items():check(sha(R/rel)==v['sha256'] and (R/rel).stat().st_size==v['bytes'],'packet mismatch: '+rel)
        obj=read(R/'cases'/CASE/'AUTHORITY_OBJECT.json')
        raw=(R/'cases'/CASE/'AUTHORITY_OBJECT.canonical.json').read_bytes()
        check(raw==canonical(obj) and hashlib.sha256(raw).hexdigest()==AUTH,'outer authority mismatch')
        check(obj['case_id']==CASE and obj['apparatus_checkpoint']==APP,'wrong approved case/checkpoint')
        amend=obj['single_case_resource_amendment']
        check(amend['execution_order']==[CASE] and amend['maximum_attempts']==1 and amend['prior_nine_case_batch_remains_stopped'],'single-case restriction mismatch')
        for rel,digest in obj['bound_documents'].items():check(sha(R/rel)==digest,'bound document mismatch: '+rel)
        for key in ('initial_snapshot','start_manifest'):check(sha(R/obj[key]['file'])==obj[key]['sha256'],'initial identity mismatch: '+key)
        checkpoint=read(R/'CHECKPOINT.json')
        check(code_identity()==checkpoint['p_code'] and apparatus_identity()==checkpoint['source'],'source implementation mismatch')
        for rel,v in read(R/'SOURCE_IDENTITIES.json')['files'].items():check(sha(D/rel)==v['sha256'],'runtime source/configuration mismatch: '+rel)
        check(runtime_identity()==checkpoint['runtime'],'installed runtime mismatch')
        m=read(R/'cases'/CASE/'MANIFEST.json')
        check(m['execution_authority'] is None,'prepared manifest already has a grant')
        check(execution_object(m)==obj['execution_object'] and execution_sha256(m)==obj['execution_sha256']==EXE,'execution binding mismatch')
        check(m['execution']['resources']=={'storage_limit_bytes':1500000000,'wall_limit_seconds':900},'resource mismatch')
        check(m['duration_seconds']==m['hard_stop_time']==30 and m['initial_time']==m['initial_index']==0,'physical horizon/start changed')
        check(m['execution']['procedure']['protocol']['reference_arm']=='SENSORY-FREE','wrong controller arm')
        original=read(ORIGINAL/'cases'/CASE/'MANIFEST.json'); restored=copy.deepcopy(m)
        restored['execution']['resources']['wall_limit_seconds']=600
        check(restored==original,'change other than approved wall allowance')
        probe=OUT/'scoped-access.tmp';probe.write_bytes(b'bounded single-case local check')
        check(probe.read_bytes()==b'bounded single-case local check','local write/read failure');probe.unlink()
        notice=(f'Jason explicitly authorized outer authority {AUTH} exactly as written for {CASE} only in the current user message, '
          f'recorded at {S / "USER_AUTHORIZATION.md"}, SHA256 {sha(S / "USER_AUTHORIZATION.md")}. '
          'One attempt at checkpoint '+APP+'. Unchanged prepared S1 state, no-input (0.30,0.30) controller, 30-second horizon, '
          'recording/validation; amended 900-second wall allowance and unchanged storage/reporting limits. '
          'No retry, continuation, batch restart, next case, substitution, tuning, controller change, new prehistory or altered horizon. '
          'Preserve S1-FULL unchanged. Stop after the single case; evaluate only the existing B1 minimal-closure rule against the preserved FULL. '
          'No S1-HIDDEN, S2, S3, Founder Search, C1/C2, nursery or additional perceptual work. Old sealed human B1 state remains inaccessible.')
        grant=OUT/'APPROVAL.json'
        save(grant,{'notice':notice,'approved_execution_sha256':EXE,'approved_execution':obj['execution_object']})
        m['execution_authority']={'request_path':str(grant),'request_sha256':sha(grant),'approved_case':CASE,
          'approved_initial_state':m['initial_state'],'approved_duration':30.0,'approved_execution_sha256':EXE}
        check(execution_object(m)==obj['execution_object'],'grant changed execution object')
        e=load_snapshot(R/obj['initial_snapshot']['file']);before=state_hash(e)
        full=read(PRIOR/'review/B1-MINIMAL-S1-FULL.json')
        check(before==obj['initial_snapshot']['state_sha256']==m['initial_state']==full['initial_state_sha256'],'not exact matched S1 state')
        # Includes unchanged full runtime cache loader. No new prehistory/evolution.
        validate_manifest(m,e,initial=True);validate_execution(m,complete=True)
        validate_dispatch(m,vars(runner));authorize_execution(m)
        check(state_hash(e)==before and e.time==0 and e.native_index==0,'preflight state/RNG/time interference')
        res=resources();check(res['free_bytes']>=20000000000 and res['combined_new_bytes']<19000000000,'preflight storage threshold')
        save(OUT/'LAUNCHED_MANIFEST.json',m)
        preflight.update(status='PASS',ended_utc=utc(),checkpoint=APP,git_status='clean',outer_authority_sha256=AUTH,
          execution_sha256=EXE,packet_files_verified=len(packet),runtime=runtime_identity(),initial_state_sha256=before,
          initial_snapshot_sha256=obj['initial_snapshot']['sha256'],full_runtime_cache_loader='PASS',
          grant_dispatch_manifest_validation='PASS',matched_FULL_complete_initial_state=True,state_RNG_time_unchanged=True,
          prior_evidence_preservation_inventory='PRESERVED_FULL_AND_PRIOR_INVENTORY.json',resources=res,
          counted_roots=[str(p) for p in COUNT],new_native_steps=0,new_controller_decisions=0,old_human_B1_accessed=False)
        save(OUT/'PREFLIGHT.json',preflight);emit('preflight_passed',case=CASE,**res)
        stage='execution';attempted=True;start=time.perf_counter()
        emit('attempt_started',case=CASE,attempt=1)
        run=runner.Run(e,m,OUT/'cases'/CASE);last=time.perf_counter()
        while not run.closed:
            res=resources()
            cause='combined_storage' if res['combined_new_bytes']>=19000000000 else 'disk_flush_reserve' if res['free_bytes']<1000000000 else None
            if cause:run.close('administrative_pause',cause=cause);break
            run.hold()
            now=time.perf_counter()
            if now-last>=20 or run.closed:
                emit('progress',case=CASE,native_index=e.native_index,simulated_seconds=e.time,
                     case_wall_seconds=now-run.started,**resources());last=now
        stage='finished'
    except BaseException as error:
        stop={'stage':stage,'error':f'{type(error).__name__}: {error}','category':'preflight_failure' if stage=='preflight' else 'apparatus_failure_or_interruption'}
        save(OUT/'FAILURE.json',dict(stop,traceback=traceback.format_exc(),utc=utc()))
        if stage=='preflight' and not (OUT/'PREFLIGHT.json').exists():
            preflight.update(status='FAILED',error=stop);save(OUT/'PREFLIGHT.json',preflight)
        if run is not None and not run.closed:
            try:
                if isinstance(error,(KeyboardInterrupt,SystemExit)):run.close('administrative_pause',cause='administrative_interruption')
                else:
                    e.status='failure';e.failure=stop['error'];run.close('apparatus_failure',error=stop['error'])
            except BaseException as err:save(OUT/'CLOSE_FAILURE.json',{'error':repr(err),'traceback':traceback.format_exc()})
        emit('stopped',**stop)
    finally:
        receipt_path=OUT/'cases'/CASE/'manifest.json'
        receipt=json.loads(receipt_path.read_bytes()) if receipt_path.exists() else None
        preserved=before_prior==inventory(PRIOR) if before_prior is not None else None
        result={'ended_utc':utc(),'only_case':CASE,'checkpoint':APP,'outer_authority_sha256':AUTH,
          'attempts':int(attempted),'exception':stop,'previous_FULL_and_prior_evidence_unchanged':preserved,
          'status':None if receipt is None else receipt['status'],'stop_cause':None if receipt is None else receipt.get('stop_cause'),
          'complete_records':None if receipt is None else receipt['complete'],'native_steps':0 if e is None else e.native_index,
          'simulated_seconds':0 if e is None else e.time,'controller_records':0 if receipt is None else receipt.get('records',{}).get('controller',0),
          'receipt_sha256':None if receipt is None else sha(receipt_path),
          'execution_and_close_wall_seconds':None if start is None else time.perf_counter()-start,
          'resources':resources(),'no_retry_continuation_or_next_case':True,'new_prehistory':0,'old_sealed_human_B1_accessed':False}
        save(OUT/'EXECUTION_RESULT.json',result);emit('execution_finished',**result)

if __name__=='__main__':main()
