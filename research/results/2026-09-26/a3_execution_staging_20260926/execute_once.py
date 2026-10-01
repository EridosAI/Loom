"""Execute the genuinely approved A3 object once. No retry/resume/patch path."""
import datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,time,traceback
S=pathlib.Path(__file__).resolve().parent
ROOT=S.parent
R=ROOT/'exports/2026-09-25-A3-launch-packet-5f077481'
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology'
BASE=D/'artifacts/commissioning-A3-20260925-5f077481'
APP='5f07748102cb5eaa302569c87efbae095050e9fe'
APPROVED='43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd'
sys.path[:0]=[str(D),str(R)]
from loom_p.records import load_snapshot,state_hash,view,code_identity
from loom_commissioning import authority,contract,runner,diagnostics
from validate_packet import verify
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,value):
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(view(value),indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(R/'empty-excludes').as_posix(),'-C',str(W),*args],env=env)
def main():
    assert not BASE.exists(),'Existing attempt: no retry or overwrite permitted'
    BASE.mkdir(parents=True,exist_ok=False)
    review=BASE/'read-only-review';review.mkdir()
    for n in ('execute_once.py','AUTHORIZATION_SOURCE.txt'):shutil.copyfile(S/n,BASE/n)
    started=time.perf_counter();run=None;e=None;stage='preflight';attempts=0;before={};failure=None
    try:
        verified=verify(lambda n:(R/n).read_bytes(),[p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()])
        assert verified['authority_sha256']==APPROVED
        m=authority.strict_loads((R/'A3_MANIFEST.json').read_bytes())
        obj=authority.strict_loads((R/'AUTHORITY_OBJECT.json').read_bytes());canonical=(R/'AUTHORITY_OBJECT.canonical.json').read_bytes()
        assert authority.canonical(obj)==canonical==authority.canonical(authority.execution_object(m))
        assert authority.execution_sha256(m)==APPROVED and m['execution_authority'] is None
        p=m['execution']['procedure']['protocol']
        assert pathlib.Path(p['record_destination']).resolve()==(BASE/'trajectory-001').resolve()
        assert pathlib.Path(p['analysis_destination']).resolve()==review.resolve()
        assert git('rev-parse','HEAD').decode().strip()==APP and not git('status','--porcelain').strip()
        ids=authority.strict_loads((R/'CODE_AND_RUNTIME_IDENTITIES.json').read_bytes())
        assert code_identity()==ids['P'] and contract.apparatus_identity()==m['apparatus']==ids['apparatus']
        assert authority.runtime_identity()==m['execution']['runtime']
        assert sha(D/'configuration.json')==ids['configuration_file_sha256']
        old=authority.strict_loads((R/'HASH_BEFORE.json').read_bytes())
        for name,h in old.items():
            path=pathlib.Path(name)
            if path.is_relative_to(D/'loom_p') or path.is_relative_to(D/'loom_commissioning') or path.is_relative_to(D/'artifacts/prehistory-attempt-001') or path in (D/'configuration.json',D/'requirements-lock.txt'):
                assert sha(path)==h,name;before[name]=h
        for q in (R,ROOT/'exports/2026-09-25-first-commissioning-launch-packet-5f077481',ROOT/'exports/2026-09-25-A2-launch-packet-5f077481',ROOT/'exports/2026-09-25-A1-read-only-reanalysis-viewer-v1',D/'artifacts/first-commissioning-A1-20260925-5f077481',D/'artifacts/commissioning-A2-20260925-5f077481'):
            for path in q.rglob('*'):
                if path.is_file() and '__pycache__' not in path.parts:before[str(path)]=sha(path)
        free=shutil.disk_usage(BASE).free
        assert free>=p['disk_bytes_for_primary_analysis_and_copy'],'Insufficient approved disk reserve'
        snap=p['initial_snapshot_file'];assert sha(R/snap['name'])==snap['sha256']
        e=load_snapshot(R/snap['name'])
        assert state_hash(e)==m['initial_state'] and e.time==e.native_index==0
        notice=(BASE/'AUTHORIZATION_SOURCE.txt').read_text(encoding='utf-8').rstrip('\n')
        request={'notice':notice,'approved_execution_sha256':APPROVED,'approved_execution':obj}
        req=BASE/'APPROVAL_REQUEST.json';write(req,request)
        m['execution_authority']={'request_path':str(req),'request_sha256':sha(req),'approved_case':'A3','approved_initial_state':m['initial_state'],'approved_duration':m['duration_seconds'],'approved_execution_sha256':APPROVED}
        assert authority.canonical(authority.execution_object(m))==canonical
        contract.validate_manifest(m,e);authority.validate_execution(m,complete=True)
        authority.validate_dispatch(m,vars(runner));contract.authorize_execution(m)
        assert state_hash(e)==m['initial_state'] and e.time==e.native_index==0
        write(review/'PREFLIGHT.json',{'approved_execution_sha256':APPROVED,'packet_payloads':verified['payloads'],
             'live_state_manifest_history_runtime_dispatch_checks':True,'genuine_grant_verified':True,'initial_time':e.time,'initial_index':e.native_index,
             'initial_state_sha256':state_hash(e),'free_disk_bytes':free,'driver_sha256':sha(BASE/'execute_once.py'),
             'authorization_source_sha256':sha(BASE/'AUTHORIZATION_SOURCE.txt'),'start_utc':utc(),'preflight_wall_seconds':time.perf_counter()-started,
             'scope':'Exact approved packet and zero-time state verified; no command rehearsal, new Engine initialization, new prehistory or prior-case replay.'})
        write(BASE/'ORIGINAL_FILES_BEFORE.json',before)
        write(BASE/'LAUNCHED_MANIFEST.json',m)
        shutil.copyfile(R/'AUTHORITY_OBJECT.canonical.json',BASE/'APPROVED_OBJECT.canonical.json')
        shutil.copyfile(R/'INITIAL_A3.snapshot.json.gz',BASE/'APPROVED_INITIAL_A3.snapshot.json.gz')
        assert time.perf_counter()-started<p['component_allowance']['machine_seconds']
        print(json.dumps({'event':'preflight_complete','approved_sha256':APPROVED,'time':e.time,'native_index':e.native_index}),flush=True)
        stage='A3';attempts+=1
        run=runner.Run(e,m,p['record_destination'],observer=diagnostics.passive)
        last=time.perf_counter()
        with (BASE/'progress.jsonl').open('x',encoding='utf-8') as progress:
            while not run.closed:
                run.hold()
                if time.perf_counter()-last>=20 or run.closed:
                    row={'utc':utc(),'time':e.time,'native_index':e.native_index,'body_energy':e.body.energy,'body_integrity':e.body.integrity,
                         'status':e.status,'closed':run.closed,'wall_seconds_since_preflight':time.perf_counter()-started}
                    progress.write(json.dumps(row)+'\n');progress.flush();print(json.dumps(row),flush=True);last=time.perf_counter()
        stage='completed_attempt'
    except Exception as error:
        failure={'stage':stage,'exception':f'{type(error).__name__}: {error}','traceback':traceback.format_exc(),'utc':utc(),'time':None if e is None else e.time,'native_index':None if e is None else e.native_index}
        write(BASE/'FAILURE.json',failure)
        if run is not None and not run.closed:
            e.status='failure';e.failure=failure['exception']
            try:run.close('apparatus_failure',error=e.failure)
            except Exception as ex:write(BASE/'FAILURE_WHILE_CLOSING.json',{'exception':repr(ex),'traceback':traceback.format_exc()})
        print(json.dumps(failure),flush=True)
    after={n:sha(n) for n in before}
    write(BASE/'ORIGINAL_FILES_AFTER.json',after)
    result={'approved_execution_sha256':APPROVED,'apparatus_checkpoint':APP,'run_constructors_attempted':attempts,
            'time':None if e is None else e.time,'native_index':None if e is None else e.native_index,'engine_status':None if e is None else e.status,
            'terminal_dimension':None if e is None else e.terminal_dimension,'final_engine_sha256':None if e is None else state_hash(e),'failure':failure,
            'wall_seconds_including_preflight':time.perf_counter()-started,'finish_utc':utc(),'original_runtime_cache_prior_evidence_and_packet_unchanged':before==after,
            'changed_original_files':[n for n in before if before[n]!=after[n]],'git_status_clean':not git('status','--porcelain').strip(),'checkpoint_unchanged':git('rev-parse','HEAD').decode().strip()==APP,
            'no_retry_no_resume_no_patch':True,'physical_replays':0}
    write(BASE/'EXECUTION_RESULT.json',result);print(json.dumps(result,indent=2),flush=True)
    return 1 if failure else 0
if __name__=='__main__':sys.exit(main())
