"""One-shot authorized batch supervisor, outside the immutable apparatus.

No controller policy, physics, prehistory generation, replay, retry or resume.
All nine full runtime validations finish before the first Run is constructed.
"""
from pathlib import Path
import copy
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import traceback

S = Path(__file__).resolve().parent
ROOT = S.parent
W = ROOT / 'worktrees/loom-p-b1-minimal-20260929'
D = W / 'developmental_ecology'
R = ROOT / 'exports/2026-09-29-B1-minimal-apparatus-a8cdd75'
OUT = S / 'run-001'
APP = 'a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad'
AUTH = [
 ('B1-MINIMAL-S1-FULL','d829e5d9b5825c6b72b9ddb26491f508cd8030654599dc309f6bf2efb1620912'),
 ('B1-MINIMAL-S1-CHEMISTRY-HIDDEN','e46379806700a4aa638e00fbc6e36ddf97e04c8e80f420cb8fb792c2cc379b69'),
 ('B1-MINIMAL-S1-SENSORY-FREE','394dfc775fc1c6dc93820384a79f4fd63291f06ee03bb28f80e464c989861dbc'),
 ('B1-MINIMAL-S2-FULL','a60dacc6b0d536aaddf7dc71313b1adf3fe91013466f5852368dcf3bdef580b5'),
 ('B1-MINIMAL-S2-CHEMISTRY-HIDDEN','1febeb0e0cf33dbcb67478e1d8081031c45a28df348ef09cfdcee79de0c0c36b'),
 ('B1-MINIMAL-S2-SENSORY-FREE','fbf477f0220bdbf43ae80e077abe74a25e0afd78878fb9ecd710aaee78ba2092'),
 ('B1-MINIMAL-S3-FULL','a2f6d55d86d360f3cb6ca13af6a1b97b642d09ddd311321a448e481d26452ca3'),
 ('B1-MINIMAL-S3-CHEMISTRY-HIDDEN','e9cb37366aac8c0a7eba71ae5607ec61fd542bd5de58c53166508d20fe6badb4'),
 ('B1-MINIMAL-S3-SENSORY-FREE','bdb6ae7f3394ea5d763b8110ace43be8ffa0183e12eb57da9a044dc8a378901c'),
]
ORDER = [c for c,h in AUTH]
LIMITS = dict(maximum_attempts_per_case=1,total_simulated_seconds=270,total_native_steps=27000,
 total_command_holds=2700,wall_per_case_seconds=600,aggregate_execution_wall_seconds=5400,
 read_only_reporting_seconds=1800,stream_cap_per_case_bytes=1_500_000_000,
 combined_new_artifact_cap_bytes=20_000_000_000,stop_request_bytes=19_000_000_000,
 flush_reserve_bytes=1_000_000_000,minimum_free_bytes=20_000_000_000)
COUNT_ROOTS = [S,ROOT/'b1_minimal_implementation_20260929',ROOT/'b1_minimal_closure_design_20260929',
 R,R.with_suffix('.zip'),ROOT/'exports/2026-09-29-B1-minimal-closure-results-a8cdd75',
 ROOT/'exports/2026-09-29-B1-minimal-closure-results-a8cdd75.zip']

def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(raw): return hashlib.sha256(raw).hexdigest()
def file_sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
    return h.hexdigest()
def check(ok,reason):
    if not ok: raise ValueError(reason)
def save(path,value):
    with Path(path).open('x',encoding='utf-8',newline='\n') as f:
        json.dump(value,f,indent=2,allow_nan=False);f.write('\n');f.flush();os.fsync(f.fileno())
def size(path):
    if not path.exists():return 0
    if path.is_file():return path.stat().st_size
    return sum(p.stat().st_size for p in path.rglob('*') if p.is_file())
def resources():
    return {'combined_new_bytes':sum(size(p) for p in COUNT_ROOTS),
            'free_bytes':shutil.disk_usage(ROOT).free}
def git(*args):
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    return subprocess.check_output(['git','-c',f'safe.directory={W.as_posix()}',
      '-c',f'core.excludesFile={ROOT / "a5_regeneration_20260926/empty-excludes"}',
      '-C',str(W),*args],env=env,text=True).strip()
def emit(kind,**data):
    row={'utc':utc(),'event':kind,**data}
    with (OUT/'operations.jsonl').open('a',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(row,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
    print(json.dumps(row,allow_nan=False),flush=True)

def main():
    # A permanent exclusive claim makes a second invocation fail before preflight.
    OUT.mkdir(exist_ok=False)
    (OUT/'grants').mkdir()
    (OUT/'launched-manifests').mkdir()
    (OUT/'cases').mkdir()
    save(OUT/'ONE_ATTEMPT_CLAIM.json',{'utc':utc(),'pid':os.getpid(),'cases':ORDER,
         'checkpoint':APP,'supervisor_sha256':file_sha(__file__),
         'authorization_sha256':file_sha(S/'USER_AUTHORIZATION.md')})
    stage='preflight'; current=None; run=None; batch_start=None
    prepared=[]; outcomes=[]; attempted=[]; stop=None
    preflight={'started_utc':utc(),'checks':[],'cases':[],'status':'INCOMPLETE'}
    try:
        check(os.name=='nt','expected actual Windows runtime')
        head=git('rev-parse','HEAD'); status=git('status','--porcelain=v1','--untracked-files=all')
        check(head==APP and status=='','wrong or dirty apparatus checkpoint')
        preflight['git']={'head':head,'status':status,'branch':git('branch','--show-current'),
             'common_directory':git('rev-parse','--git-common-dir'),'version':git('--version')}
        probe=OUT/'scoped-access.tmp'
        with probe.open('xb') as f:f.write(b'bounded B1 local read/write check\n')
        check(probe.read_bytes()==b'bounded B1 local read/write check\n','write/read mismatch')
        probe.unlink()
        sys.path.insert(0,str(D))
        from loom_p.records import load_snapshot,state_hash,code_identity
        from loom_commissioning.authority import (canonical,strict_loads,execution_object,
             execution_sha256,runtime_identity,validate_execution,validate_dispatch)
        from loom_commissioning.contract import validate_manifest,authorize_execution,apparatus_identity
        from loom_commissioning import runner
        read=lambda p:strict_loads(Path(p).read_bytes())
        files=read(R/'FILE_MANIFEST.json')['files']
        for rel,v in files.items():
            p=R/rel
            check(p.stat().st_size==v['bytes'] and file_sha(p)==v['sha256'],'packet file mismatch: '+rel)
        preflight['checks'].append({'packet_files_verified':len(files),'manifest_sha256':file_sha(R/'FILE_MANIFEST.json')})
        checkpoint=read(R/'CHECKPOINT.json')
        check(checkpoint['apparatus_commit']==APP,'checkpoint document mismatch')
        check(apparatus_identity()==checkpoint['source'],'apparatus source mismatch')
        check(code_identity()==checkpoint['p_code'],'P source mismatch')
        identities=read(R/'SOURCE_IDENTITIES.json')['files']
        for rel,v in identities.items():
            p=D/rel
            check(p.stat().st_size==v['bytes'] and file_sha(p)==v['sha256'],'runtime file mismatch: '+rel)
        runtime=runtime_identity()
        check(runtime==checkpoint['runtime'],'full runtime identity mismatch')
        preflight['runtime']=runtime
        preflight['checks'].append({'runtime_source_files_verified':len(identities),'runtime_identity_exact':True})
        index=read(R/'AUTHORITY_INDEX.json')
        check(index['case_order']==ORDER,'authority index order mismatch')
        check([(x['case_id'],x['authority_sha256']) for x in index['cases']]==AUTH,'index differs from user authorization')
        for i,(case,authorized) in enumerate(AUTH):
            current=case; cdir=R/'cases'/case
            raw=(cdir/'AUTHORITY_OBJECT.canonical.json').read_bytes(); obj=read(cdir/'AUTHORITY_OBJECT.json')
            check(raw==canonical(obj) and sha(raw)==authorized,'authorized outer object mismatch: '+case)
            check(obj['case_id']==case and obj['apparatus_checkpoint']==APP,'object identity mismatch')
            check(obj['shared_batch_order']==ORDER and obj['shared_resource_limits']==LIMITS,'shared bounds mismatch')
            for rel,expected in obj['bound_documents'].items():check(file_sha(R/rel)==expected,'bound document mismatch: '+rel)
            for key in ('initial_snapshot','start_manifest'):
                check(file_sha(R/obj[key]['file'])==obj[key]['sha256'],key+' file mismatch')
            m=read(cdir/'MANIFEST.json')
            check(m['execution_authority'] is None,'prepared manifest has an unexpected grant')
            check(execution_object(m)==obj['execution_object'] and execution_sha256(m)==obj['execution_sha256'],'execution binding mismatch')
            check((cdir/'EXECUTION_OBJECT.canonical.json').read_bytes()==canonical(execution_object(m)),'execution canonical bytes mismatch')
            check(m['duration_seconds']==30 and m['initial_index']==0 and m['initial_time']==0,'prepared case clock mismatch')
            notice=(f'Jason explicitly authorized outer proposal {authorized} for {case}, in position {i+1} of the exact nine-case order, '
              f'on 2026-09-29. User message recorded at {S / "USER_AUTHORIZATION.md"}; SHA256 {file_sha(S / "USER_AUTHORIZATION.md")}. '
              'This grant records that actual authorization, not a new proposal. All shared rules and limits in the authorized object apply: '
              'one attempt, no retry/continuation/substitution/tuning/new prehistory/extra case; full runtime preflight; '
              '30-second ceiling; report-dont-patch; stop remaining batch on preflight/apparatus/controller/admin/resource failure; '
              'normal ceiling or physical terminal permits only next separately authorized case; do not stop for an early positive witness; '
              'do not inspect old sealed human B1 evaluator state. '
              'Exact shared order: '+json.dumps(ORDER)+'; shared resource limits: '+json.dumps(LIMITS,sort_keys=True)+'.')
            envelope={'notice':notice,'approved_execution_sha256':obj['execution_sha256'],'approved_execution':obj['execution_object']}
            grant=OUT/'grants'/(case+'.json'); save(grant,envelope)
            m=copy.deepcopy(m)
            m['execution_authority']={'request_path':str(grant),'request_sha256':file_sha(grant),'approved_case':case,
                'approved_initial_state':m['initial_state'],'approved_duration':m['duration_seconds'],
                'approved_execution_sha256':obj['execution_sha256']}
            check(execution_object(m)==obj['execution_object'],'grant changed execution semantics')
            e=load_snapshot(R/obj['initial_snapshot']['file'])
            before=state_hash(e)
            check(before==m['initial_state']==obj['initial_snapshot']['state_sha256'],'snapshot state mismatch')
            # Includes the unchanged full runtime lawful cache loader, without evolving a world.
            validate_manifest(m,e,initial=True)
            validate_execution(m,complete=True);validate_dispatch(m,vars(runner));authorize_execution(m)
            check(state_hash(e)==before and e.time==0 and e.native_index==0,'preflight mutated physical/RNG state')
            save(OUT/'launched-manifests'/(case+'.json'),m)
            record={'case_id':case,'authority_sha256':authorized,'execution_sha256':obj['execution_sha256'],
                'initial_snapshot_sha256':obj['initial_snapshot']['sha256'],'initial_state_sha256':before,
                'full_runtime_cache_loader':'PASS','manifest_runtime_dispatch_grant':'PASS','state_RNG_clock_unchanged':True}
            preflight['cases'].append(record);prepared.append((case,m,e))
            emit('case_preflight_passed',case=case)
        for k in range(0,9,3):
            triplet=preflight['cases'][k:k+3]
            check(len({x['initial_snapshot_sha256'] for x in triplet})==1 and len({x['initial_state_sha256'] for x in triplet})==1,
                  'matched triplet identity mismatch')
        resource=resources()
        check(resource['free_bytes']>=LIMITS['minimum_free_bytes'],'insufficient initial free storage')
        check(resource['combined_new_bytes']<LIMITS['stop_request_bytes'],'combined artifact stop threshold')
        preflight.update(status='PASS',ended_utc=utc(),resources=resource,
             counted_roots=[str(p) for p in COUNT_ROOTS],zero_native_steps=True,zero_controller_decisions=True,
             old_human_B1_material_accessed=False,matched_triplets_exact=True)
        save(OUT/'PREFLIGHT.json',preflight)
        emit('all_nine_preflight_passed',**resource)
        stage='execution'; current=None;batch_start=time.perf_counter()
        for case,m,e in prepared:
            current=case;run=None;resource=resources()
            cause=('aggregate_wall_time' if time.perf_counter()-batch_start>=LIMITS['aggregate_execution_wall_seconds']
                else 'combined_storage' if resource['combined_new_bytes']>=LIMITS['stop_request_bytes']
                else 'disk_flush_reserve' if resource['free_bytes']<LIMITS['flush_reserve_bytes'] else None)
            if cause:stop={'category':'resource_cutoff','cause':cause,'before_case':case};break
            check(state_hash(e)==m['initial_state'],'untouched prepared state changed')
            check(case not in attempted and not (OUT/'cases'/case).exists(),'case already attempted')
            attempted.append(case)
            emit('attempt_started',case=case,attempt=1,order=len(attempted),batch_wall_seconds=time.perf_counter()-batch_start)
            # Only this single constructor/trajectory is authorized for this case.
            run=runner.Run(e,m,OUT/'cases'/case)
            last=time.perf_counter()
            while not run.closed:
                resource=resources()
                cause=('aggregate_wall_time' if time.perf_counter()-batch_start>=LIMITS['aggregate_execution_wall_seconds']
                  else 'combined_storage' if resource['combined_new_bytes']>=LIMITS['stop_request_bytes']
                  else 'disk_flush_reserve' if resource['free_bytes']<LIMITS['flush_reserve_bytes'] else None)
                if cause:
                    run.close('administrative_pause',cause=cause)
                    break
                run.hold()
                now=time.perf_counter()
                if now-last>=20 or run.closed:
                    emit('progress',case=case,native_index=e.native_index,simulated_seconds=e.time,
                         case_wall_seconds=now-run.started,batch_wall_seconds=now-batch_start,**resources())
                    last=now
            receipt=read(OUT/'cases'/case/'manifest.json')
            outcome={'case_id':case,'status':receipt['status'],'complete':receipt['complete'],
              'stop_cause':receipt['stop_cause'],'native_steps':run.session['advanced'],'final_time':e.time,
              'wall_seconds':receipt['wall_seconds'],'controller_records':receipt['records'].get('controller',0),
              'receipt_sha256':file_sha(OUT/'cases'/case/'manifest.json')}
            outcomes.append(outcome);emit('case_ended',**outcome)
            normal=(receipt['complete'] and receipt['status'] in ('administrative_cutoff','terminal') and receipt['stop_cause'] is None)
            if not normal:
                stop={'category':'declared_batch_stop','case':case,'status':receipt['status'],'cause':receipt['stop_cause']}
                break
        stage='finished'
    except BaseException as error:
        stop={'category':'preflight_failure' if stage=='preflight' else 'apparatus_failure_or_interruption',
              'stage':stage,'case':current,'error':f'{type(error).__name__}: {error}'}
        save(OUT/'FAILURE.json',dict(stop,traceback=traceback.format_exc(),utc=utc()))
        if stage=='preflight':
            preflight.update(status='FAILED',failure=stop,ended_utc=utc(),zero_native_steps=True,zero_controller_decisions=True)
            if not (OUT/'PREFLIGHT.json').exists():save(OUT/'PREFLIGHT.json',preflight)
        if run is not None and not run.closed:
            try:
                # Never repair/retry the failing command or state.
                if isinstance(error,(KeyboardInterrupt,SystemExit)):
                    run.close('administrative_pause',cause='administrative_interruption')
                else:
                    run.engine.status='failure';run.engine.failure=stop['error']
                    run.close('apparatus_failure',error=stop['error'])
            except BaseException as close_error:
                save(OUT/'CLOSE_FAILURE.json',{'error':repr(close_error),'traceback':traceback.format_exc()})
        emit('batch_stopped',**stop)
    finally:
        result={'ended_utc':utc(),'checkpoint':APP,'authorized_order':ORDER,'attempted':attempted,'outcomes':outcomes,
          'not_attempted':[c for c in ORDER if c not in attempted],'batch_stop':stop,
          'aggregate_execution_wall_seconds':None if batch_start is None else time.perf_counter()-batch_start,
          'resources':resources(),'no_retry_or_continuation':True,'no_new_prehistory':True,
          'old_sealed_human_B1_material_accessed':False,'production_code_modified':False}
        save(OUT/'EXECUTION_RESULT.json',result)
        emit('execution_finished',attempted=len(attempted),normal_outcomes=len(outcomes),batch_stop=stop)

if __name__=='__main__':main()
