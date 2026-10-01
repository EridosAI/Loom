"""Exactly one authorized post-fix engineering life, then saved-record checks."""
import copy
import ctypes
from ctypes import wintypes
import hashlib
import json
from pathlib import Path
import statistics
import sys
import time

ROOT=Path(__file__).resolve().parent.parent
HERE=Path(__file__).resolve().parent
D=ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'
sys.path.insert(0,str(D))
from loom_developmental import codec,core
from loom_developmental.runner import Life,create_engineering_grant,file_hash,identity,canonical
from loom_developmental.verify import verify_store
from loom_developmental.replay import reconstruct

PREVIOUS=ROOT/'developmental_runner_optimization_20260929/measurements/long'
STORE=HERE/'release-engineering-life'
REQUEST=Path(r'C:\Users\Jason\.codex\attachments\d28a1d79-11b8-4403-92b0-269696a4b937\Pasted text.txt')
class Counters(ctypes.Structure):
    _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in
      ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage',
       'QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
def memory():
    k=ctypes.WinDLL('kernel32');p=ctypes.WinDLL('psapi');k.GetCurrentProcess.restype=wintypes.HANDLE
    p.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD]
    c=Counters();c.cb=ctypes.sizeof(c)
    if not p.GetProcessMemoryInfo(k.GetCurrentProcess(),ctypes.byref(c),c.cb):raise ctypes.WinError()
    return {'peak_working_set_bytes':c.PeakWorkingSetSize,'working_set_bytes':c.WorkingSetSize,'peak_pagefile_bytes':c.PeakPagefileUsage}
def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2),encoding='utf8')

def main():
    if STORE.exists() or (HERE/'RELEASE_BENCHMARK_RESULT.json').exists():raise FileExistsError('No retry or overwrite')
    previous=json.loads((PREVIOUS/'segment-000.json').read_bytes())
    initial=previous['initial_checkpoint']
    e=codec.read(PREVIOUS/initial['file'],initial['sha256'])['engine']
    assert e.native_index==0 and e.organism.native_count==0 and e.fixture['manufactured']
    grant=create_engineering_grant(e,30000,REQUEST,wall_limit=450,storage_limit=100_000_000)
    save('RELEASE_BENCHMARK_DECLARATION.json',{'checkpoint':'87abae34e19d4e46234402a6b1ba776814956ec1',
        'prior_initial_checkpoint':initial,'initial_causal_sha256':codec.digest(core.causal_state(e)),
        'fixture':e.fixture,'total_end_index':60000,'save_reload_index':30000,
        'request_sha256':file_hash(REQUEST),'plan_sha256':file_hash(HERE/'RELEASE_CHECK_PLAN.md'),
        'engineering_only':True,'Founder_lives':0})
    blocks=[];receipts=[];started=time.perf_counter();run=Life(e,STORE,grant);setup=time.perf_counter()-started
    resume_seconds=0.
    try:
        for endpoint in (30000,60000):
            while not run.closed:
                tick=time.perf_counter();old_time=run.engine.time
                run.advance(min(1000,endpoint-run.engine.native_index))
                b={'end_index':run.engine.native_index,'simulated_seconds':run.engine.time-old_time,
                    'wall_seconds':time.perf_counter()-tick,**memory()};blocks.append(b)
                print(json.dumps(b),flush=True)
            receipts.append(run.receipt)
            if run.receipt['status']!='stage_complete':raise RuntimeError('600-second release not complete')
            if endpoint==30000:
                grant=create_engineering_grant(run.engine,60000,REQUEST,wall_limit=450,storage_limit=100_000_000)
                grant['parent_receipt_sha256']=file_hash(STORE/'segment-000.json')
                before=codec.digest(core.causal_state(run.engine));tick=time.perf_counter()
                run=Life.continue_life(STORE,grant);resume_seconds=time.perf_counter()-tick
                assert codec.digest(core.causal_state(run.engine))==before
        wall=time.perf_counter()-started;execution_memory=memory()
        size=sum(p.stat().st_size for p in STORE.iterdir() if p.is_file())
        result={'status':'recorded_pending_verification','engineering_lives':1,'Founder_lives':0,
            'native_steps':run.engine.native_index,'waves':run.engine.organism.wave_count,
            'simulated_seconds':run.engine.time,'wall_seconds':wall,'setup_seconds':setup,
            'resume_seconds':resume_seconds,'stored_bytes':size,'execution_memory':execution_memory,'blocks':blocks}
        save('RELEASE_BENCHMARK_RESULT.json',result)
        verification=verify_store(STORE)
        # Every closed chunk contains identical native rows, wave outputs,
        # physical events and field/P/RNG endpoint identities.
        chunks=[f for r in receipts for f in r['chunks']]
        assert len(chunks)==len(previous['chunks'])==600
        for old,new in zip(previous['chunks'],chunks):
            assert (old['first_index'],old['last_index'])==(new['first_index'],new['last_index'])
            assert codec.encode(codec.read(PREVIOUS/old['file'],old['sha256']))==codec.encode(codec.read(STORE/new['file'],new['sha256']))
        prior_cp={x['index']:x for x in previous['checkpoints']};checked=[]
        for cp in [f for r in receipts for f in r['checkpoints']]:
            old=prior_cp[cp['index']]
            a=codec.read(PREVIOUS/old['file'],old['sha256'])['engine'];b=codec.read(STORE/cp['file'],cp['sha256'])['engine']
            assert codec.encode(core.causal_state(a))==codec.encode(core.causal_state(b))
            checked.append(cp['index'])
        tick=time.perf_counter();replay=reconstruct(STORE,first_index=1,last_index=60000)
        assert codec.encode(replay['engine'].organism)==codec.encode(run.engine.organism)
        del replay['engine'];replay['wall_seconds']=time.perf_counter()-tick
        tick=time.perf_counter();deep=reconstruct(STORE,first_index=59981,last_index=60000,fields=True)
        assert codec.encode(core.causal_state(deep['engine']))==codec.encode(core.causal_state(run.engine))
        del deep['engine'];deep['wall_seconds']=time.perf_counter()-tick
        first=sum(b['wall_seconds'] for b in blocks[:20])/200
        last=sum(b['wall_seconds'] for b in blocks[-20:])/200
        flags=[]
        if size>85_000_000:flags.append('storage exceeds predeclared release envelope')
        if wall/600>.55:flags.append('wall/sim exceeds predeclared release envelope')
        if last/first>1.5:flags.append('material chronological throughput degradation')
        if execution_memory['peak_working_set_bytes']>150_000_000:flags.append('memory exceeds predeclared release envelope')
        result.update(status='PASS' if not flags else 'HOLD',flags=flags,verification=verification,
            exact_prior_chunks=600,exact_checkpoint_indices=checked,full_P_reconstruction=replay,
            final_causal_reconstruction=deep,first_200_wall_per_sim=first,last_200_wall_per_sim=last,
            last_over_first_rate=last/first,final_causal_sha256=codec.digest(core.causal_state(run.engine)),
            final_rng=run.engine.organism.rng.counters,final_runtime=identity(),scientific_outcomes_inspected=False)
        save('RELEASE_BENCHMARK_RESULT.json',result)
        print(json.dumps({k:v for k,v in result.items() if k not in ('blocks','verification','final_runtime','final_rng')},indent=2),flush=True)
        if flags:raise RuntimeError('Release HOLD; stop without patch/retry')
    except BaseException as error:
        save('RELEASE_CHECK_EXCEPTION.json',{'error':f'{type(error).__name__}: {error}',
            'index':run.engine.native_index,'status':'HOLD','retry_authorized':False})
        raise

if __name__=='__main__':main()
