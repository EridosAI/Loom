"""One genuinely authorized A5 execution. No retry, resume or alternate route."""
import datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,time,traceback
S=pathlib.Path(__file__).resolve().parent; ROOT=S.parent
R=ROOT/'exports/2026-09-26-A5-launch-packet-68db2c58'
W=ROOT/'worktrees/loom-p-clock-correction-20260926'; D=W/'developmental_ecology'
BASE=D/'artifacts/commissioning-A5-20260926-68db2c58'
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
APP='68db2c581f07200966d699a4f55a65f9b96df1e9'
APPROVED='bdff35693db38800528d91e6d2d4d2085c640268e50713731df5ec27f8b76d1d'
NOTICE='I authorize canonical authority object `bdff35693db38800528d91e6d2d4d2085c640268e50713731df5ec27f8b76d1d` exactly as written. Execute the single 630-second A5 commissioning case using corrected apparatus checkpoint `68db2c581f07200966d699a4f55a65f9b96df1e9`. Report-don’t-patch. No retry, continuation, route/stage substitution, tuning, parameter change or additional case without separate authorization. Preserve the complete trajectory even if the bounded renewal witness is not obtained.'
DISK_ROOTS=[BASE,S,ROOT/'a5_regeneration_20260926',R,
    ROOT/'exports/A5_LAUNCH_PACKET_68db2c58_20260926.zip',
    ROOT/'exports/A5_LAUNCH_PACKET_68db2c58_20260926.receipt.json',
    ROOT/'exports/A5_LAUNCH_PACKET_68db2c58_20260926.delivery.json',
    ROOT/'exports/A5_LAUNCH_PACKET_68db2c58_20260926.zip.sha256',
    WB/'INBOX/2026-09-26-A5-launch-packet-68db2c58',
    ROOT/'exports/2026-09-26-A5-commissioning-result-68db2c58',
    WB/'INBOX/2026-09-26-A5-commissioning-result-68db2c58']

def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,v):
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env)
def size(p):
    if p.is_file():return p.stat().st_size
    return sum(q.stat().st_size for q in p.rglob('*') if q.is_file()) if p.exists() else 0
def disk_bytes():return sum(size(p) for p in DISK_ROOTS)

def main():
    assert not BASE.exists(),'Existing attempt blocks retry/overwrite'
    assert (S/'AUTHORIZATION_SOURCE.txt').read_text(encoding='utf-8').rstrip('\n')==NOTICE
    BASE.mkdir(parents=True,exist_ok=False); review=BASE/'read-only-review';review.mkdir()
    for n in ('execute_once.py','AUTHORIZATION_SOURCE.txt'):shutil.copyfile(S/n,BASE/n)
    started=time.perf_counter();run=None;e=None;stage='preflight';attempts=0;failure=None;before={};monitor_checks=0;peak_disk=0
    try:
        sys.path[:0]=[str(D),str(R)]
        from loom_p.records import load_snapshot,state_hash,code_identity
        from loom_commissioning import authority,contract,runner,diagnostics
        from validate_packet import verify
        verified=verify(lambda n:(R/n).read_bytes(),[p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()])
        assert verified['authority_sha256']==APPROVED
        m=authority.strict_loads((R/'A5_MANIFEST.json').read_bytes())
        obj=authority.strict_loads((R/'AUTHORITY_OBJECT.json').read_bytes()); canonical=(R/'AUTHORITY_OBJECT.canonical.json').read_bytes()
        assert authority.canonical(obj)==canonical==authority.canonical(authority.execution_object(m))
        assert authority.execution_sha256(m)==APPROVED and m['execution_authority'] is None
        p=m['execution']['procedure']['protocol'];dest=pathlib.Path(p['record_destination'])
        assert dest.resolve()==(BASE/'trajectory-001').resolve() and not dest.exists()
        assert pathlib.Path(p['analysis_destination']).resolve()==review.resolve()
        assert m['duration_seconds']==630 and m['initial_index']==m['initial_time']==0
        assert git('rev-parse','HEAD').decode().strip()==APP and not git('status','--porcelain').strip()
        ids=authority.strict_loads((R/'CODE_AND_RUNTIME_IDENTITIES.json').read_bytes())
        assert code_identity()==ids['P'] and contract.apparatus_identity()==m['apparatus']==ids['apparatus']
        assert authority.runtime_identity()==m['execution']['runtime']
        assert sha(D/'configuration.json')==ids['configuration_file_sha256']
        # Preserve the already verified held packets and live source, then add
        # the authorized packet and the exact existing prehistory cache.
        old=authority.strict_loads((R/'HASH_BEFORE.json').read_bytes())
        for name,h in old.items():assert sha(name)==h,name;before[name]=h
        for q in (R,WB/'INBOX/2026-09-26-A5-launch-packet-68db2c58',pathlib.Path(m['initialization']['cache_directory'])):
            for path in q.rglob('*'):
                if path.is_file() and '__pycache__' not in path.parts:before[str(path)]=sha(path)
        before[str(ROOT/'exports/A5_LAUNCH_PACKET_68db2c58_20260926.zip')]=sha(ROOT/'exports/A5_LAUNCH_PACKET_68db2c58_20260926.zip')
        free=shutil.disk_usage(BASE).free; usage=disk_bytes()
        assert free>=p['free_disk_before_launch_bytes']==10_000_000_000
        assert usage<p['stop_request_disk_bytes']==9_000_000_000
        snap=p['initial_snapshot_file'];assert sha(R/snap['name'])==snap['sha256']
        e=load_snapshot(R/snap['name'])
        assert state_hash(e)==m['initial_state'] and e.time==e.native_index==0
        req=BASE/'APPROVAL_REQUEST.json'
        write(req,{'notice':NOTICE,'approved_execution_sha256':APPROVED,'approved_execution':obj})
        m['execution_authority']={'request_path':str(req),'request_sha256':sha(req),'approved_case':'A5','approved_initial_state':m['initial_state'],'approved_duration':m['duration_seconds'],'approved_execution_sha256':APPROVED}
        assert authority.canonical(authority.execution_object(m))==canonical
        contract.validate_manifest(m,e);authority.validate_execution(m,complete=True)
        authority.validate_dispatch(m,vars(runner));contract.authorize_execution(m)
        assert state_hash(e)==m['initial_state'] and e.time==e.native_index==0
        write(review/'PREFLIGHT.json',dict(approved_execution_sha256=APPROVED,apparatus_checkpoint=APP,packet_payloads=verified['payload_count'],
              live_state_manifest_history_runtime_dispatch_checks=True,genuine_grant_verified=True,initial_time=e.time,initial_index=e.native_index,
              initial_state_sha256=state_hash(e),free_disk_bytes=free,combined_new_disk_bytes=usage,disk_accounting_roots=[str(q) for q in DISK_ROOTS],
              driver_sha256=sha(BASE/'execute_once.py'),authorization_source_sha256=sha(BASE/'AUTHORIZATION_SOURCE.txt'),start_utc=utc(),
              preflight_wall_seconds=time.perf_counter()-started,scope='Exact authorized object and existing zero-time snapshot; no rehearsal, new prehistory, retry or prior-case replay.'))
        write(BASE/'ORIGINAL_FILES_BEFORE.json',before);write(BASE/'LAUNCHED_MANIFEST.json',m)
        shutil.copyfile(R/'AUTHORITY_OBJECT.canonical.json',BASE/'APPROVED_OBJECT.canonical.json')
        shutil.copyfile(R/snap['name'],BASE/'APPROVED_INITIAL_A5.snapshot.json.gz')
        write(BASE/'RUN_CONSTRUCTION_ATTEMPT.json',dict(attempt=1,utc=utc(),duration_ceiling_seconds=630,authority_sha256=APPROVED))
        print(json.dumps(dict(event='preflight_complete',approved_sha256=APPROVED,time=e.time,native_index=e.native_index,free_disk_bytes=free,combined_new_disk_bytes=usage)),flush=True)
        stage='A5';attempts+=1
        run=runner.Run(e,m,dest,observer=diagnostics.passive)
        last=time.perf_counter()
        with (BASE/'progress.jsonl').open('x',encoding='utf-8') as progress:
            while not run.closed:
                # Administrative monitoring only. No control inputs or policy.
                usage=disk_bytes();free=shutil.disk_usage(BASE).free
                monitor_checks+=1;peak_disk=max(peak_disk,usage)
                if usage>=p['stop_request_disk_bytes'] or free<p['final_flush_reserve_bytes']:
                    write(BASE/'DISK_STOP.json',dict(utc=utc(),native_index=e.native_index,combined_new_disk_bytes=usage,free_disk_bytes=free))
                    run.close('administrative_pause',cause='combined_disk_or_free_space_reserve')
                else:
                    run.hold()
                if time.perf_counter()-last>=20 or run.closed:
                    row=dict(utc=utc(),time=e.time,native_index=e.native_index,E=float(e.body.energy),I=float(e.body.integrity),
                             position=e.body.position.tolist(),status=e.status,closed=run.closed,
                             whole_process_wall_seconds=time.perf_counter()-started,combined_new_disk_bytes=usage)
                    progress.write(json.dumps(row)+'\n');progress.flush();print(json.dumps(row),flush=True);last=time.perf_counter()
        stage='completed_attempt'
    except Exception as error:
        failure=dict(stage=stage,exception=f'{type(error).__name__}: {error}',traceback=traceback.format_exc(),utc=utc(),time=None if e is None else e.time,native_index=None if e is None else e.native_index)
        write(BASE/'FAILURE.json',failure)
        if run is not None and not run.closed:
            e.status='failure';e.failure=failure['exception']
            try:run.close('apparatus_failure',error=e.failure)
            except Exception as ex:write(BASE/'FAILURE_WHILE_CLOSING.json',dict(exception=repr(ex),traceback=traceback.format_exc()))
        print(json.dumps(failure),flush=True)
    stopped_utc=utc()
    after={n:sha(n) for n in before};write(BASE/'ORIGINAL_FILES_AFTER.json',after)
    result=dict(approved_execution_sha256=APPROVED,apparatus_checkpoint=APP,run_constructors_attempted=attempts,
                time=None if e is None else e.time,native_index=None if e is None else e.native_index,
                engine_status=None if e is None else e.status,terminal_dimension=None if e is None else e.terminal_dimension,
                final_engine_sha256=None if e is None else state_hash(e),failure=failure,
                wall_seconds_including_preflight=time.perf_counter()-started,first_stop_utc=stopped_utc,finish_utc=utc(),
                originals_unchanged=before==after,changed_original_files=[n for n in before if before[n]!=after[n]],
                git_status_clean=not git('status','--porcelain').strip(),checkpoint_unchanged=git('rev-parse','HEAD').decode().strip()==APP,
                disk_monitor_checks=monitor_checks,peak_combined_new_disk_bytes=peak_disk,final_combined_new_disk_bytes=disk_bytes(),
                no_retry_no_resume_no_patch=True,physical_replays=0,new_prehistory_steps=0)
    write(BASE/'EXECUTION_RESULT.json',result);print(json.dumps(result,indent=2),flush=True)
    return 1 if failure else 0

if __name__=='__main__':sys.exit(main())
