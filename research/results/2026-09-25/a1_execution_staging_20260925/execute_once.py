"""Execute exactly the approved packet sequence once. No retry or patch path."""
import copy,datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,time,traceback
S=pathlib.Path(__file__).resolve().parent
R=S.parent/'exports/2026-09-25-first-commissioning-launch-packet-5f077481'
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology'
BASE=D/'artifacts/first-commissioning-A1-20260925-5f077481'
APP='5f07748102cb5eaa302569c87efbae095050e9fe'
APPROVED='a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc'
sys.path[:0]=[str(D),str(R)]
from loom_p.records import load_snapshot,state_hash,view,code_identity
from loom_commissioning import authority,contract,runner,diagnostics
import packet_checks

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,value):
    data=json.dumps(view(value),indent=2,ensure_ascii=False,allow_nan=False)+'\n'
    with p.open('x',encoding='utf-8') as f:f.write(data)
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-C',str(W),*args],env=env)

def main():
    assert not BASE.exists(),'Existing attempt: no retry or overwrite permitted'
    BASE.mkdir(parents=True,exist_ok=False)
    review=BASE/'read-only-review';review.mkdir()
    for name in ('execute_once.py','AUTHORIZATION_SOURCE.txt'):shutil.copyfile(S/name,BASE/name)
    started=time.perf_counter();run=None;e=None;stage='preflight';attempts=0
    before={};failure=None
    try:
        manifest=authority.strict_loads((R/'A1_MANIFEST.json').read_bytes())
        original=authority.strict_loads((R/'AUTHORITY_OBJECT.json').read_bytes())
        canonical=(R/'AUTHORITY_OBJECT.canonical.json').read_bytes()
        assert authority.canonical(original)==canonical==authority.canonical(authority.execution_object(manifest))
        assert hashlib.sha256(canonical).hexdigest()==APPROVED==authority.execution_sha256(manifest)
        assert manifest['execution_authority'] is None
        inventory=authority.strict_loads((R/'FILE_MANIFEST.json').read_bytes())['files']
        for name,row in inventory.items():
            p=R/name;assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],name
        protocol=manifest['execution']['procedure']['protocol']
        for name,h in protocol['bound_files'].items():assert sha(R/name)==h,name
        for name,h in protocol['read_only_callable_identities'].items():
            assert authority.callable_identity(getattr(packet_checks,name))==h,name
        assert pathlib.Path(protocol['record_destination']).resolve()==(BASE/'trajectory-001').resolve()
        assert pathlib.Path(protocol['analysis_destination']).resolve()==review.resolve()
        assert not (BASE/'trajectory-001').exists()
        assert git('rev-parse','HEAD').decode().strip()==APP and not git('status','--porcelain').strip()
        ids=authority.strict_loads((R/'CODE_AND_RUNTIME_IDENTITIES.json').read_bytes())
        before=ids['original_file_inventory']
        for name,h in before.items():assert sha(pathlib.Path(name))==h,name
        assert code_identity()==ids['P'] and contract.apparatus_identity()==manifest['apparatus']
        assert authority.runtime_identity()==manifest['execution']['runtime']
        assert sha(D/'configuration.json')==ids['configuration_file_sha256']
        free=shutil.disk_usage(BASE).free
        assert free>=protocol['disk_bytes_for_primary_and_copy'],'Insufficient approved disk allowance'
        snapshot=protocol['initial_snapshot_file']
        assert sha(R/snapshot['name'])==snapshot['sha256']
        e=load_snapshot(R/snapshot['name'])
        assert state_hash(e)==manifest['initial_state'] and e.time==e.native_index==0
        # Preserve a readable, exact approved envelope. The proposal itself stays intact.
        text=(BASE/'AUTHORIZATION_SOURCE.txt').read_text(encoding='utf-8').rstrip('\n')
        request={'notice':text,'approved_execution_sha256':APPROVED,'approved_execution':original}
        request_path=BASE/'APPROVAL_REQUEST.json';write(request_path,request)
        manifest['execution_authority']={'request_path':str(request_path),'request_sha256':sha(request_path),
            'approved_case':manifest['case_id'],'approved_initial_state':manifest['initial_state'],
            'approved_duration':manifest['duration_seconds'],'approved_execution_sha256':APPROVED}
        assert authority.canonical(authority.execution_object(manifest))==canonical
        checks={'V1':packet_checks.v1(e,manifest),'V3':packet_checks.v3(e)}
        geometry=packet_checks.a0(e.c,e.phase)
        assert geometry==authority.strict_loads((R/'A0_GEOMETRY.json').read_bytes())
        write(review/'A0_GEOMETRY.json',geometry)
        old=authority.strict_loads((R/'references/independent-r1p-evidence.json').read_bytes())
        write(review/'V2_ARCHIVED_ACCOUNTING_CHECK.json',{'scope':'Historical events read without replay; not this A1 result',
            'cases':{c['case']:packet_checks.v2(c['events'],e.c) for c in old['cases']}})
        contract.authorize_execution(manifest)
        assert state_hash(e)==manifest['initial_state'] and e.time==e.native_index==0
        checks.update(approved_execution_sha256=APPROVED,grant_verified=True,free_disk_bytes=free,
            source_message_sha256=sha(BASE/'AUTHORIZATION_SOURCE.txt'),start_utc=utc(),
            driver_sha256=sha(BASE/'execute_once.py'),preflight_wall_seconds=time.perf_counter()-started,
            scope='Zero evolution in V1/V3/A0 and historical V2 calculation; no command rehearsal.')
        write(review/'V1_V3_PREFLIGHT.json',checks)
        write(BASE/'LAUNCHED_MANIFEST.json',manifest)
        shutil.copyfile(R/'AUTHORITY_OBJECT.canonical.json',BASE/'APPROVED_OBJECT.canonical.json')
        shutil.copyfile(R/'INITIAL_A1.snapshot.json.gz',BASE/'APPROVED_INITIAL_A1.snapshot.json.gz')
        assert time.perf_counter()-started<protocol['component_allowance']['machine_seconds']
        print(json.dumps({'event':'preflight_complete','approved_sha256':APPROVED,'time':e.time,'native_index':e.native_index}),flush=True)
        # Exactly one constructor and its declared hold loop. Decisions stay inside Run.
        stage='A1';attempts+=1
        run=runner.Run(e,manifest,protocol['record_destination'],observer=diagnostics.passive)
        last=time.perf_counter()
        with (BASE/'progress.jsonl').open('x',encoding='utf-8') as progress:
            while not run.closed:
                run.hold()
                if time.perf_counter()-last>=20 or run.closed:
                    row={'utc':utc(),'time':e.time,'native_index':e.native_index,'body_energy':e.body.energy,
                         'body_integrity':e.body.integrity,'status':e.status,'closed':run.closed,
                         'wall_seconds_since_preflight':time.perf_counter()-started}
                    progress.write(json.dumps(row)+'\n');progress.flush();print(json.dumps(row),flush=True)
                    last=time.perf_counter()
        stage='completed_attempt'
    except Exception as error:
        failure={'stage':stage,'exception':f'{type(error).__name__}: {error}','traceback':traceback.format_exc(),
                 'utc':utc(),'time':None if e is None else e.time,'native_index':None if e is None else e.native_index}
        write(BASE/'FAILURE.json',failure)
        if run is not None and not run.closed:
            e.status='failure';e.failure=failure['exception']
            try:run.close('apparatus_failure',error=e.failure)
            except Exception as close_error:
                write(BASE/'FAILURE_WHILE_CLOSING.json',{'exception':repr(close_error),'traceback':traceback.format_exc()})
        print(json.dumps(failure),flush=True)
    after={name:sha(pathlib.Path(name)) for name in before}
    result={'approved_execution_sha256':APPROVED,'apparatus_checkpoint':APP,'run_constructors_attempted':attempts,
            'time':None if e is None else e.time,'native_index':None if e is None else e.native_index,
            'engine_status':None if e is None else e.status,'terminal_dimension':None if e is None else e.terminal_dimension,
            'final_engine_sha256':None if e is None else state_hash(e),'failure':failure,
            'wall_seconds_including_preflight':time.perf_counter()-started,'finish_utc':utc(),
            'original_runtime_config_cache_unchanged':before==after,'git_status_clean':not git('status','--porcelain').strip(),
            'checkpoint_unchanged':git('rev-parse','HEAD').decode().strip()==APP,
            'no_retry_no_resume_no_patch':True,'physical_replays':0}
    write(BASE/'EXECUTION_RESULT.json',result)
    print(json.dumps(result,indent=2),flush=True)
    return 1 if failure else 0

if __name__=='__main__':sys.exit(main())
