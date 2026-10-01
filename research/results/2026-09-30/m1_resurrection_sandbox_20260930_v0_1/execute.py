"""NON-CANONICAL RESURRECTION SANDBOX. Authorized single use; no outcome selection."""
import paths
from paths import HERE
import hashlib,json,math,shutil,time,traceback
from loom_motor_commissioning import codec
from sandbox_core import LABEL
from sandbox_runner import Budget,Life,atomic,file_hash,canonical,runtime_check,verify_segment

def main():
    ex=HERE/'execution';ex.mkdir(exist_ok=False)
    batch=json.loads((HERE/'BATCH_AUTHORITY.json').read_bytes());plan=json.loads((HERE/'RESOURCE_PLAN.json').read_bytes())
    manifest=json.loads((HERE/'PREPARATION_MANIFEST.json').read_bytes())
    for row in manifest['files']:
        if file_hash(HERE/row['path'])!=row['sha256']:raise ValueError('prepared input changed')
    assert len(batch['authorities'])==12 and batch['no_more_review_required']
    assert shutil.disk_usage(HERE).free>=30000000000
    atomic(ex/'SINGLE_USE_START.json',dict(label=LABEL,batch_authority=file_hash(HERE/'BATCH_AUTHORITY.json'),runtime=batch['runtime'],
        authorization=file_hash(HERE/'JASON_OVERNIGHT_AUTHORIZATION.txt')))
    start=time.perf_counter();budget=Budget(start,sum(p.stat().st_size for p in HERE.rglob('*') if p.is_file()))
    states=[];rows=[dict(life_id=r['life_id'],pilot='UNSTARTED',overnight='UNSTARTED') for r in batch['authorities']]
    stop=None;target=None;pilot=[];run=None;active_row=None;stage='preflight'
    try:
        runtime_check(batch['runtime'])
        for ref in batch['authorities']:
            path=HERE/'authorities'/(ref['life_id']+'.json');a=json.loads(path.read_bytes());assert file_hash(path)==ref['sha256']
            a['authority_sha256']=ref['sha256'];e=codec.read(HERE/'initial_states'/a['initial_snapshot']['file'],a['initial_snapshot']['sha256'])['engine']
            assert e.time==e.native_index==e.organism.wave_count==0 and e.organism.rng.life==a['stream_life']
            assert codec.digest(e)==a['initial_digest'] and a['runtime']==batch['runtime']
            e.validate_state();states.append((a,e))
        atomic(ex/'PREFLIGHT.json',dict(label=LABEL,status='PASS',blank_states=12,runtime=batch['runtime'],world_steps=0))
        for stage in ('pilot','overnight'):
            if stage=='pilot':target=600.
            else:
                elapsed=time.perf_counter()-start
                wall_rate=max(r['wall_seconds']/600 for r in pilot)
                byte_rate=max(r['bytes_written']/600 for r in pilot)
                allowance=min((.8*25200-elapsed-600)/(12*wall_rate),(.8*8000000000-budget.bytes-32000000)/(12*byte_rate))
                target=float(min(4500,math.floor(600+allowance)))
                if target<600:raise RuntimeError('RESOURCE_STOP pilot leaves insufficient continuation margin')
                gate=dict(label=LABEL,status='PASS',all_twelve_pilot_receipts_verified=True,continuity=True,
                    no_shared_defect=True,no_evidence_corruption=True,elapsed_wall=elapsed,primary_bytes=budget.bytes,
                    conservative_wall_per_sim_s=wall_rate,conservative_bytes_per_sim_s=byte_rate,
                    selected_common_total_age=target,projected_wall=elapsed+12*(target-600)*wall_rate+600,
                    projected_primary_bytes=budget.bytes+12*(target-600)*byte_rate+32000000,
                    criterion='Only runtime/storage and integrity of complete pilot; no developmental outcome variables inspected.')
                budget.add(atomic(ex/'CONTINUATION_GATE.json',gate)['bytes']);print(json.dumps(gate),flush=True)
                if target==600:break
            for j,(a,original) in enumerate(states):
                active_row=rows[j];active_row[stage]='PREFLIGHT'
                budget.check();runtime_check(batch['runtime'])
                store=ex/'lives'/a['life_id'];parent=None
                if stage=='pilot':e=original
                else:
                    path=store/'pilot-RECEIPT.json';r=json.loads(path.read_bytes());parent=file_hash(path)
                    e=codec.read(store/r['final_checkpoint']['file'],r['final_checkpoint']['sha256'])['engine']
                    if codec.digest(e)!=r['final_digest'] or e.time!=600:raise ValueError('pilot continuation checkpoint mismatch')
                active_row[stage]='STARTED'
                print(json.dumps(dict(label=LABEL,event='START',life=a['life_id'],stage=stage,from_age=e.time,target=target)),flush=True)
                run=Life(e,store,a,batch['runtime'],budget,stage,target,parent);receipt=run.advance()
                check=verify_segment(store,receipt);budget.add(atomic(store/(stage+'-VERIFY.json'),check)['bytes'])
                runtime_check(batch['runtime'])
                active_row[stage]='AGE_TARGET_COMPLETE';active_row['last_age']=e.time
                active_row['resurrections']=e.sandbox['resurrections'];active_row['last_receipt']=file_hash(store/(stage+'-RECEIPT.json'))
                if stage=='pilot':pilot.append(receipt)
                print(json.dumps(dict(label=LABEL,event='COMPLETE_VERIFIED',life=a['life_id'],stage=stage,age=e.time,
                    active_wall=time.perf_counter()-start,primary_bytes=budget.bytes)),flush=True)
        atomic(ex/'COMPLETED.json',dict(label=LABEL,status='COMPLETE',common_target=target,lives=12,rows=rows,
            active_wall_seconds=time.perf_counter()-start,primary_bytes=budget.bytes,no_selection=True))
    except BaseException as error:
        stop=f'{type(error).__name__}: {error}'
        if active_row is not None:active_row[stage]='DECLARED_SANDBOX_STOP'
        atomic(ex/'STOP.json',dict(label=LABEL,reason=stop,stage=stage,life=None if active_row is None else active_row['life_id'],
            native_index=None if run is None else run.e.native_index,age=None if run is None else run.e.time,
            traceback=traceback.format_exc(),no_retry=True,no_patch=True))
    finally:
        atomic(ex/'DENOMINATOR.json',dict(label=LABEL,rows=rows,stop=stop,common_target=target,
            active_wall_seconds=time.perf_counter()-start,primary_bytes=budget.bytes))
    if stop:raise SystemExit(stop)
if __name__=='__main__':main()
