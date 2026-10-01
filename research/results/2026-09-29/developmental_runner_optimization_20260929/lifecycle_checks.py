"""Disclosed 0.6-second engineering split comparison; no Founder starts."""
import copy
import json
import time
from benchmark import D,OUT,CACHE,REQUEST,Config,make_case,memory
from loom_commissioning.contract import make_manifest,INTACT
from loom_commissioning.runner import Run,load_restart,save_restart
from loom_commissioning.validators import verify_segment
from loom_developmental import codec,core
from loom_developmental.runner import Life,create_engineering_grant,file_hash,identity,canonical
from loom_developmental.verify import verify_store
from loom_developmental.replay import reconstruct

def timed(operation):
    start=time.perf_counter();value=operation();return value,time.perf_counter()-start

def main():
    result_path=OUT/'lifecycle-final.json'
    if result_path.exists():raise FileExistsError(result_path)
    result={}
    c=Config(**json.loads((D/'configuration.json').read_text()))
    original=make_case(c,'nonzero_resume_1s',CACHE)
    expected,_,_=load_restart(OUT/'old-short/final.restart.json.gz')
    old=copy.deepcopy(original)
    m=make_manifest(old,'fixture-split-cost',INTACT,'none',.6,wall_limit=600,storage_limit=2_000_000_000)
    run,setup=timed(lambda:Run(old,m,OUT/'old-split-1'))
    _,first=timed(lambda:run.advance(7))
    _,pause=timed(lambda:run.close('administrative_pause'))
    run,resume=timed(lambda:Run.resume(OUT/'old-split-1',OUT/'old-split-2'))
    _,finish=timed(lambda:run.advance(53))
    assert codec.encode(core.causal_state(run.engine))==codec.encode(core.causal_state(expected))
    verification,verify=timed(lambda:verify_segment(OUT/'old-short',replay=False))
    end,session,manifest=load_restart(OUT/'old-short/final.restart.json.gz')
    _,snapshot_time=timed(lambda:save_restart(OUT/'old-checkpoint-measurement.json.gz',end,session,manifest))
    result['old']={'setup_seconds':setup,'first_7_steps_seconds':first,'pause_including_checkpoint_seconds':pause,
        'resume_seconds':resume,'remaining_53_steps_including_close_seconds':finish,
        'continuous_record_verification_seconds':verify,'standalone_final_checkpoint_seconds':snapshot_time,
        'standalone_final_checkpoint_bytes':(OUT/'old-checkpoint-measurement.json.gz').stat().st_size,
        'exact_continuous_endpoint':True,'new_world_native_steps':60,'verification_replay':False}
    e=copy.deepcopy(original);g=create_engineering_grant(e,60,REQUEST)
    run,setup=timed(lambda:Life(e,OUT/'lean-split-final',g))
    _,first=timed(lambda:run.advance(7))
    _,pause=timed(lambda:run.close('administrative_pause'))
    g=create_engineering_grant(e,60,REQUEST)
    g['parent_receipt_sha256']=file_hash(run.store/'segment-000.json')
    run,resume=timed(lambda:Life.continue_life(run.store,g))
    _,finish=timed(lambda:run.advance())
    assert codec.encode(core.causal_state(run.engine))==codec.encode(core.causal_state(expected))
    verified,verify=timed(lambda:verify_store(run.store))
    result['lean']={'setup_seconds':setup,'first_7_steps_seconds':first,'pause_including_checkpoint_seconds':pause,
        'resume_seconds':resume,'remaining_53_steps_including_close_seconds':finish,
        'split_record_verification_seconds':verify,'verification':verified,
        'exact_continuous_endpoint':True,'new_world_native_steps':60}
    # Final analysis-only optimization: no complete-state copies during the
    # nearest-checkpoint warm-up if deep rows were not requested there.
    reconstructed,analysis=timed(lambda:reconstruct(OUT/'long',first_index=59981,last_index=60000,deep=True,fields=True))
    receipt=json.loads((OUT/'long/segment-000.json').read_bytes())
    saved=codec.read(OUT/'long'/receipt['final_checkpoint']['file'])['engine']
    assert codec.encode(core.causal_state(reconstructed['engine']))==codec.encode(core.causal_state(saved))
    del reconstructed['engine']
    result['selected_deep_final']={**reconstructed,'wall_seconds':analysis,'exact_final_causal_state':True,'new_world_steps':0}
    result['final_identity']=identity();result['memory']=memory()
    result_path.write_text(json.dumps(result,indent=2));print(json.dumps({k:v for k,v in result.items() if k not in ('final_identity','lean')},indent=2),flush=True)
    print(json.dumps({'lean':{k:v for k,v in result['lean'].items() if k!='verification'}},indent=2),flush=True)

if __name__=='__main__':main()
