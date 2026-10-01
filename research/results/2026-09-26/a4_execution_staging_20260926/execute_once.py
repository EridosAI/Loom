"""One explicitly authorized A4 batch. No retry, resume, substitution or patch path."""
import datetime,hashlib,json,os,pathlib,shutil,subprocess,sys,time,traceback
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
R=ROOT/'exports/2026-09-26-A4-launch-packet-5f077481'
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405');D=W/'developmental_ecology'
BASE=D/'artifacts/commissioning-A4-20260926-5f077481'
APP='5f07748102cb5eaa302569c87efbae095050e9fe'
APPROVED='47a71e78ad4bbb920f2b29f7d9b0e3c5f520eb4905880916c85f0cc8bbb9f1e0'
ORDER=['A4-CROSS','A4-WAIT','A4-DETOUR']
NOTICE='I authorize canonical batch authority object `47a71e78ad4bbb920f2b29f7d9b0e3c5f520eb4905880916c85f0cc8bbb9f1e0` exactly as written. Execute the three predetermined A4 cases: A4-CROSS, A4-WAIT and A4-DETOUR. Report-don’t-patch. No retry, route/phase substitution, tuning, continuation or additional case without separate authorization.'
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,v):
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a4_packet_staging_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env)
def disk_bytes(folder):return sum(p.stat().st_size for p in folder.rglob('*') if p.is_file())
def main():
    assert not BASE.exists(),'Existing batch destination blocks retry or overwrite'
    BASE.mkdir(parents=True,exist_ok=False);review=BASE/'read-only-review';review.mkdir()
    for n in ('AUTHORIZATION_SOURCE.txt','execute_once.py'):shutil.copyfile(S/n,BASE/n)
    start=time.perf_counter();run=None;e=None;where='batch_preflight';failure=None;attempts=0;before={};results=[];active=None;stop=None
    try:
        assert (BASE/'AUTHORIZATION_SOURCE.txt').read_text(encoding='utf-8').rstrip('\n')==NOTICE
        sys.path[:0]=[str(D),str(R)]
        from loom_p.records import load_snapshot,state_hash,code_identity
        from loom_commissioning import authority,contract,runner,diagnostics
        from validate_packet import verify
        batch=authority.strict_loads((R/'AUTHORITY_OBJECT.json').read_bytes());canonical=(R/'AUTHORITY_OBJECT.canonical.json').read_bytes()
        assert authority.canonical(batch)==canonical and sha(R/'AUTHORITY_OBJECT.canonical.json')==APPROVED
        assert batch['case_order']==ORDER and [m['case_id'] for m in batch['cases']]==ORDER
        write(BASE/'BATCH_ATTEMPT.json',{'batch_sha256':APPROVED,'start_utc':utc(),'authorization_source_sha256':sha(BASE/'AUTHORIZATION_SOURCE.txt'),'scope':'One foreground sequential attempt of each predetermined case. No retry/resume.','driver_sha256':sha(BASE/'execute_once.py')})
        shutil.copyfile(R/'AUTHORITY_OBJECT.canonical.json',BASE/'APPROVED_BATCH.canonical.json')
        old=authority.strict_loads((R/'HASH_BEFORE.json').read_bytes())
        for name,h in old.items():
            q=pathlib.Path(name)
            # Current originals are preserved; bound source copies are checked by
            # the packet validator. Exact live code/cache bytes remain mandatory.
            now=sha(q);before[name]=now
            if q.is_relative_to(D/'loom_p') or q.is_relative_to(D/'loom_commissioning') or q.is_relative_to(D/'artifacts/prehistory-attempt-001') or q in (D/'configuration.json',D/'requirements-lock.txt'):assert now==h,name
        for q in R.rglob('*'):
            if q.is_file():before[str(q)]=sha(q)
        write(BASE/'ORIGINAL_FILES_BEFORE.json',before)
        ids=authority.strict_loads((R/'CODE_AND_RUNTIME_IDENTITIES.json').read_bytes())
        # Recheck the complete batch, including untouched later members, before
        # every case. The approved exact member remains the single-case contract.
        for index,member in enumerate(batch['cases']):
            cid=member['case_id'];active=BASE/cid;active.mkdir(exist_ok=False)
            where=cid+'_preflight';run=None;e=None;case_start=time.perf_counter();constructed=False
            write(active/'ATTEMPT.json',{'batch_sha256':APPROVED,'case_id':cid,'ordinal':index+1,'attempt':1,'utc':utc(),'execution_sha256':member['execution_sha256']})
            checked=verify(lambda n:(R/n).read_bytes(),[p.relative_to(R).as_posix() for p in R.rglob('*') if p.is_file()])
            assert checked['authority_sha256']==APPROVED and authority.canonical(batch)==(R/'AUTHORITY_OBJECT.canonical.json').read_bytes()
            assert (BASE/'AUTHORIZATION_SOURCE.txt').read_text(encoding='utf-8').rstrip('\n')==NOTICE
            assert git('rev-parse','HEAD').decode().strip()==APP and not git('status','--porcelain').strip()
            assert code_identity()==ids['P'] and contract.apparatus_identity()==ids['apparatus']
            assert sha(D/'configuration.json')==ids['configuration_file_sha256']
            assert authority.runtime_identity()==ids['runtime']
            assert all(sha(p)==v for p,v in before.items()),'Original source or packet changed during batch'
            free=shutil.disk_usage(BASE).free;assert free>=batch['batch_limits']['free_disk_precondition_bytes'],'free_disk_precondition'
            assert disk_bytes(BASE)<batch['batch_limits']['combined_disk_bytes'],'combined_disk_cap'
            assert len(results)==index and all(x['permits_next_predetermined_case'] for x in results)
            m=authority.strict_loads((R/member['manifest_file']).read_bytes());obj=member['execution_object']
            assert m['execution_authority'] is None and authority.execution_object(m)==obj
            h=authority.execution_sha256(m);assert h==member['execution_sha256']
            p=m['execution']['procedure']['protocol'];dest=pathlib.Path(p['record_destination'])
            assert dest.resolve()==(active/'trajectory-001').resolve() and not dest.exists()
            assert pathlib.Path(p['analysis_destination']).resolve()==(review/cid).resolve()
            snap=p['initial_snapshot_file'];assert sha(R/snap['name'])==snap['sha256']
            e=load_snapshot(R/snap['name']);assert state_hash(e)==m['initial_state'] and e.time==e.native_index==0
            approval_notice=NOTICE+'\n\nConstituent scope derived from Jason\'s explicit approval of canonical batch '+APPROVED+'.\nExact constituent: '+cid+'; execution SHA-256 '+h+'. No independent or substituted case is approved.'
            req=active/'APPROVAL_REQUEST.json';write(req,{'notice':approval_notice,'approved_execution_sha256':h,'approved_execution':obj})
            m['execution_authority']={'request_path':str(req),'request_sha256':sha(req),'approved_case':cid,'approved_initial_state':m['initial_state'],'approved_duration':m['duration_seconds'],'approved_execution_sha256':h}
            assert authority.execution_object(m)==obj
            contract.validate_manifest(m,e);authority.validate_execution(m,complete=True);authority.validate_dispatch(m,vars(runner));contract.authorize_execution(m)
            assert state_hash(e)==m['initial_state'] and e.time==e.native_index==0
            write(active/'PREFLIGHT.json',{'batch_sha256':APPROVED,'case_execution_sha256':h,'full_batch_members_verified':ORDER,'packet_payloads':checked['payload_count'],'live_history_state_runtime_dispatch_valid':True,'free_disk_bytes':free,'initial_time':e.time,'initial_index':e.native_index,'initial_state_sha256':state_hash(e),'genuine_parent_and_constituent_grant_bound':True,'preflight_seconds':time.perf_counter()-case_start,'utc':utc()})
            write(active/'LAUNCHED_MANIFEST.json',m);shutil.copyfile(R/snap['name'],active/'APPROVED_INITIAL.snapshot.json.gz')
            shutil.copyfile(R/member['execution_object_file'],active/'APPROVED_EXECUTION.canonical.json')
            write(active/'RUN_CONSTRUCTION_ATTEMPT.json',{'attempt':1,'utc':utc()});attempts+=1;constructed=True;where=cid+'_run'
            print(json.dumps({'event':'case_preflight_complete','case':cid,'batch_sha256':APPROVED,'duration_seconds':m['duration_seconds']}),flush=True)
            run=runner.Run(e,m,dest,observer=diagnostics.passive)
            last=time.perf_counter()
            with (active/'progress.jsonl').open('x',encoding='utf-8') as progress:
                while not run.closed:
                    run.hold()
                    if time.perf_counter()-last>=20 or run.closed:
                        row={'case':cid,'utc':utc(),'time':e.time,'native_index':e.native_index,'E':float(e.body.energy),'I':float(e.body.integrity),'position':e.body.position.tolist(),'status':e.status,'closed':run.closed,'case_process_wall_seconds':time.perf_counter()-case_start}
                        progress.write(json.dumps(row)+'\n');progress.flush();print(json.dumps(row),flush=True);last=time.perf_counter()
            receipt=authority.strict_loads((dest/'manifest.json').read_bytes())
            permit=bool(receipt['complete'] and receipt['status'] in ('administrative_cutoff','terminal'))
            result={'case_id':cid,'execution_sha256':h,'run_constructors_attempted':1,'time':e.time,'native_index':e.native_index,'engine_status':e.status,'terminal_dimension':e.terminal_dimension,'final_engine_sha256':state_hash(e),'receipt_status':receipt['status'],'receipt_complete':receipt['complete'],'receipt_cause':receipt.get('cause'),'permits_next_predetermined_case':permit,'whole_process_wall_seconds':time.perf_counter()-case_start,'finish_utc':utc(),'no_retry_no_resume':True}
            write(active/'EXECUTION_RESULT.json',result);results.append(result);print(json.dumps({'event':'case_stopped',**result}),flush=True)
            assert sum(x['native_index'] for x in results)<=7600 and attempts<=3
            if not permit:stop={'case_id':cid,'reason':receipt['status'],'cause':receipt.get('cause')};break
            where=cid+'_complete'
    except Exception as ex:
        failure={'stage':where,'exception':f'{type(ex).__name__}: {ex}','traceback':traceback.format_exc(),'utc':utc(),'time':None if e is None else e.time,'native_index':None if e is None else e.native_index}
        write(BASE/'FAILURE.json',failure)
        if run is not None and not run.closed:
            e.status='failure';e.failure=failure['exception']
            try:run.close('apparatus_failure',error=e.failure)
            except Exception as close_error:write(BASE/'FAILURE_WHILE_CLOSING.json',{'exception':repr(close_error),'traceback':traceback.format_exc()})
        stop={'reason':'preflight_or_apparatus_failure','detail':failure};print(json.dumps(failure),flush=True)
    after={p:sha(p) for p in before};write(BASE/'ORIGINAL_FILES_AFTER.json',after)
    result={'approved_batch_sha256':APPROVED,'apparatus_checkpoint':APP,'run_constructors_attempted':attempts,'case_order':ORDER,'completed_attempts':results,
      'unattempted_cases':[cid for cid in ORDER if not (BASE/cid/'ATTEMPT.json').exists()],
      'attempted_without_completed_result':[cid for cid in ORDER if (BASE/cid/'ATTEMPT.json').exists() and not (BASE/cid/'EXECUTION_RESULT.json').exists()],
      'failure':failure,'batch_stop':stop,'wall_seconds_including_preflight':time.perf_counter()-start,'finish_utc':utc(),'original_files_unchanged':before==after,'changed_original_files':[p for p in before if before[p]!=after[p]],'git_status_clean':not git('status','--porcelain').strip(),'checkpoint_unchanged':git('rev-parse','HEAD').decode().strip()==APP,'primary_bytes':disk_bytes(BASE),'no_retry_no_resume_no_patch':True,'physical_replays':0}
    write(BASE/'BATCH_EXECUTION_RESULT.json',result);print(json.dumps(result,indent=2),flush=True)
    if failure:sys.exit(1)
if __name__=='__main__':main()
