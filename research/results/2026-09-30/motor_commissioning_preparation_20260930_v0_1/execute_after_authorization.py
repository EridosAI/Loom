"""Future single-use executor. Preparation does not call this entry point.

Requires a separately preserved explicit Jason authorization containing all nine
exact hashes. The directory's present status is PROPOSED_UNAUTHORIZED.
"""
import paths
from paths import HERE
import argparse,hashlib,json,os,shutil,time,traceback
from preflight import check,inspect_case,ORDER
from loom_motor_commissioning.runner import Life,canonical,file_hash,atomic_json
from loom_motor_commissioning.verify import verify_store

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--authorization',required=True,type=str)
    args=parser.parse_args()
    from pathlib import Path
    auth_path=Path(args.authorization).resolve();auth=json.loads(auth_path.read_bytes())
    matrix=json.loads((HERE/'MATRIX.json').read_bytes());hashes=[r['authority_sha256'] for r in matrix['cases']]
    if set(auth)!={'jason_instruction','authorized_authority_sha256'} or not auth['jason_instruction'] or auth['authorized_authority_sha256']!=hashes:
        raise ValueError('separate exact ordered authorization required; no implicit preparation approval')
    out=HERE/'execution';out.mkdir(exist_ok=False)
    atomic_json(out/'SINGLE_USE_START.json',dict(authorization_sha256=file_hash(auth_path),authority_sha256=hashes,pid=os.getpid()))
    shutil.copyfile(auth_path,out/'JASON_AUTHORIZATION.json')
    rows=[dict(case_id=n,status='NOT_STARTED',native_steps=0) for n in ORDER]
    stop=None;active=0.;run=None;preflight_wall=0.;verification_wall=0.
    try:
        assert shutil.disk_usage(HERE).free>=2000000000
        result=check();atomic_json(out/'PREFLIGHT.json',result)
        preflight_wall+=result['full_runtime_seconds']
        if preflight_wall>300:raise RuntimeError('preflight wall allowance')
        for index,row in enumerate(rows):
            a=json.loads((HERE/'authorities'/(row['case_id']+'.json')).read_bytes())
            # Repeat complete source/runtime/state gate immediately before each case.
            tick=time.perf_counter();check()
            preflight_wall+=time.perf_counter()-tick
            if preflight_wall>300:raise RuntimeError('preflight wall allowance')
            if shutil.disk_usage(HERE).free<1000000000:raise RuntimeError('working disk reserve')
            engine=inspect_case(a)
            approval=out/(row['case_id']+'-approval.json')
            atomic_json(approval,dict(notice=auth['jason_instruction'],approved_scope=a['runner_scope']))
            grant=dict(a['runner_scope'],request_path=str(approval),request_sha256=file_hash(approval))
            row['status']='STARTED';atomic_json(out/(row['case_id']+'-START.json'),row)
            print(json.dumps(row),flush=True)
            run=Life(engine,out/'lives'/row['case_id'],grant,asset_root=out/'shared-assets')
            run.advance()
            assert run.closed
            r=run.receipt;active+=r['wall_seconds']
            row.update(status=r['status'],cause=r['cause'],native_steps=r['native_steps'],time=r['final_time'])
            tick=time.perf_counter();verification=verify_store(run.store)
            atomic_json(out/(row['case_id']+'-VERIFY.json'),verification)
            atomic_json(out/(row['case_id']+'-STOP.json'),row)
            print(json.dumps(row),flush=True)
            verification_wall+=time.perf_counter()-tick
            if verification_wall>600:raise RuntimeError('verification wall allowance')
            if r['status']=='resource_pause':
                stop='resource boundary; no redistribution/continuation';break
            if active>=2700:
                stop='batch active wall allowance';break
    except Exception as error:
        stop=f'{type(error).__name__}: {error}'
        atomic_json(out/'APPARATUS_STOP.json',dict(reason=stop,traceback=traceback.format_exc()))
    finally:
        atomic_json(out/'DENOMINATOR.json',dict(cases=rows,stop=stop,active_wall_seconds=active,preflight_wall_seconds=preflight_wall,verification_wall_seconds=verification_wall,
            no_retry=True,no_continuation=True,no_automatic_selection=True))
    if stop:raise SystemExit(stop)

if __name__=='__main__':main()
