"""Single-use outer executor for Jason's twelve exact grants. No physics changes.

Preflight only reads prepared states. The only evolution entry is the frozen
Life.advance(1). No replay, diagnostics, scoring, continuation or retry entry.
"""
import ctypes
from ctypes import wintypes
from datetime import datetime, timezone
import gc
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
import traceback
import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
W = ROOT / 'worktrees/loom-p-b1-minimal-20260929'
D = W / 'developmental_ecology'
PACKET = ROOT / 'exports/2026-09-30-Founder-Search-initial-stage'
sys.path.insert(0, str(D))
sys.path.insert(0, str(ROOT / 'founder_initial_packet_20260930'))
from loom_developmental import codec, core
from loom_developmental.runner import Life, atomic_json, canonical, file_hash, identity, validate_grant
from loom_p.records import state_hash, code_identity
from loom_p.prehistory import load
from prepare_blank_starts import verify_blank

P = '6bc9683b54e4fa80136fe8534d7713e2a250a95f'
CHECKPOINT = '87abae34e19d4e46234402a6b1ba776814956ec1'
RUNTIME = '2fc498951552f53698d70da31f5957e1e208016320c2e27e7dfb20e5e5e7a6ab'
COHORT = 'd1453af1d36fd1fd968f345dec5bfa7ece57e87c84f563d948b1238c7e44e199'
HASHES = '''d2960d88f93074c6b361697743fac4fac5a05bddfcdf2e7e644c7b3fbc5ebf0e
a016fb805d2f8467bf8f6ccb1f7358a20236e0a6116e521551736174a0e79fbc
376dcefd28ee44795cdd55e5b066e1e1029f3deb6355039b8ffc39728213e84b
4799d6e1d4ed4d4240eb29f131948004e7fab567e1895dc4632411d59b9601f2
572b3420b803ac9a799634afbabbfa027afe002e545d521d81cf7badefc90372
5e6c3730fce723704313f82b88474b6f992dbe218f4234de3d69a55e456aad84
894d39535ce7e28f351d1d0f7d619953ba3c725271b96766c585da7002c7f7e3
b868a25197bf4a703bfbe6a0651b3f58f71efde28940371734a87ea6d84a1432
b49acf6456e1afdb7a38479421d8968eb1b3443d2a5469c2055a7f823533e10c
62693c8111206835bb36755162dcdcc6914e8fe52a2838b9a5ba223e4cbad730
61fd716eb39f92d639e592eec3c4319c5f3d93399c1c546df3a086fbcd22942a
596451cdd73353af2c1dddf1994d1766a9aba1f1f255a2dc0587357bf52fd622'''.split()

class Counters(ctypes.Structure):
    _fields_ = [('cb', wintypes.DWORD), ('PageFaultCount', wintypes.DWORD)] + [(n, ctypes.c_size_t) for n in
        ('PeakWorkingSetSize', 'WorkingSetSize', 'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage',
         'QuotaPeakNonPagedPoolUsage', 'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage')]

def memory():
    k = ctypes.WinDLL('kernel32'); p = ctypes.WinDLL('psapi')
    k.GetCurrentProcess.restype = wintypes.HANDLE
    p.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.POINTER(Counters), wintypes.DWORD]
    c = Counters(); c.cb = ctypes.sizeof(c)
    if not p.GetProcessMemoryInfo(k.GetCurrentProcess(), ctypes.byref(c), c.cb):
        raise ctypes.WinError()
    return dict(working_set_bytes=c.WorkingSetSize, peak_working_set_bytes=c.PeakWorkingSetSize,
                peak_commit_bytes=c.PeakPagefileUsage)

def save(name, value):
    atomic_json(HERE / name, value)

def utc():
    return datetime.now(timezone.utc).isoformat()

def log(kind, **kw):
    value = dict(utc=utc(), kind=kind, **kw)
    with (HERE / 'EXECUTION_LEDGER.jsonl').open('ab') as f:
        f.write(canonical(value) + b'\n'); f.flush(); os.fsync(f.fileno())
    print(json.dumps(value), flush=True)

def git(*args):
    env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
    return subprocess.check_output(['git', '-c', 'safe.directory=' + W.as_posix(),
        '-c', 'core.excludesFile=' + (ROOT / 'a5_regeneration_20260926/empty-excludes').as_posix(),
        '-C', str(W), *args], env=env, text=True).strip()

def source_gate():
    assert git('rev-parse', 'HEAD') == CHECKPOINT
    assert git('status', '--porcelain') == '', 'worktree not clean'

def read_authority(i):
    name = f'FS-{i:03d}'; path = PACKET / 'authorities' / (name + '.json')
    data = path.read_bytes(); a = json.loads(data)
    assert data == canonical(a) and hashlib.sha256(data).hexdigest() == HASHES[i-1]
    assert a['ordinal'] == a['birth_id'] == i and a['life_id'] == name and a['master_seed'] == 5284097
    assert a['P_commit'] == P and a['apparatus_checkpoint'] == CHECKPOINT and a['runtime_sha256'] == RUNTIME
    assert a['cohort_manifest_sha256'] == COHORT
    assert a['retry'] is a['continuation'] is a['substitution'] is a['outcome_intervention'] is False
    assert a['external_controller'] is None and a['simulation_ceiling_seconds'] == 600
    assert a['evidence_identity']['attempt_limit'] == 1 and a['evidence_identity']['parent_receipt'] is None
    s = a['runner_scope']
    assert s['kind'] == 'developmental-intact-P' and s['life_id'] == name
    assert s['initial_index'] == 0 and s['end_index'] == 60000 and s['parent_receipt_sha256'] is None
    assert (s['wall_limit_seconds'], s['storage_limit_bytes'], s['checkpoint_stride'], s['chunk_steps'], s['compression_level']) == (332,83333333,6000,100,1)
    return a

def exact_engine(a, full_prehistory=False):
    assert file_hash(D / 'configuration.json') == a['configuration_file_sha256']
    assert code_identity()['sha256'] == a['P_code_sha256']
    snapshot = a['initial_snapshot']; state = codec.read(PACKET / snapshot['path'], snapshot['sha256'])
    assert (state['identity'], state['index'], state['wave'], state['life_id']) == (RUNTIME,0,0,a['life_id'])
    assert hashlib.sha256(codec.encode(state)).hexdigest() == snapshot['raw_sha256']
    e = state['engine']; e.validate_state()
    assert state_hash(e) == a['initial_engine_sha256']
    assert codec.digest(core.causal_state(e)) == a['runner_scope']['initial_causal_sha256']
    assert e.c.identity() == a['configuration_sha256'] and e.c.native_dt == .01 and e.c.wave_dt == .2
    assert e.phase == a['mover_phase']
    assert e.organism.rng.life == a['birth_id'] and e.organism.rng.seed == a['master_seed']
    bpath = PACKET / a['birth_manifest']['path']
    assert file_hash(bpath) == a['birth_manifest']['sha256']
    b = json.loads(bpath.read_bytes())
    assert verify_blank(e) == b['blank']
    assert e.organism.rng.counters == b['initial_rng_counters']
    assert b['initial_causal_sha256'] == a['runner_scope']['initial_causal_sha256']
    assert b['stream_life'] == a['birth_id'] and b['phase'] == a['mover_phase']
    pre = a['prehistory']; cache = PACKET / pre['path']
    assert file_hash(cache / 'manifest.json') == pre['manifest_sha256']
    assert file_hash(cache / 'fields.npz') == pre['field_file_sha256']
    assert hashlib.sha256(e.fields.tobytes()).hexdigest() == pre['field_array_sha256']
    if full_prehistory:
        fields, phase, rng, pm = load(e.c, cache, life=a['birth_id'])
        assert phase == e.phase and np.array_equal(fields, e.fields)
        assert pm['life'] == a['birth_id'] and pm['body'] == 'absent' and pm['organism_created'] is False
    return e

def main():
    if (HERE / 'SINGLE_USE_START.json').exists() or (HERE / 'lives').exists():
        raise FileExistsError('Existing batch attempt: no restart or retry permitted')
    save('SINGLE_USE_START.json', dict(utc=utc(), pid=os.getpid(),
         authorization_sha256=file_hash(HERE/'JASON_AUTHORIZATION.md'),
         executor_sha256=file_hash(__file__), checkpoint=CHECKPOINT, authorities=HASHES))
    rows = [dict(life_id=f'FS-{i:03d}', authority_sha256=h, state='NOT_STARTED',
                 native_steps=0, waves=0, simulated_seconds=0.) for i,h in enumerate(HASHES,1)]
    active_wall = 0.; closed_bytes = 0; preflight_wall = 0.; stop = None; run = None
    resource = json.loads((PACKET / 'RESOURCE_PLAN.json').read_bytes())
    try:
        tick = time.perf_counter(); source_gate()
        cohort = json.loads((PACKET/'COHORT_MANIFEST.json').read_bytes())
        assert file_hash(PACKET/'COHORT_MANIFEST.json') == COHORT
        for file,key in [('RESOURCE_PLAN.json','resource_plan_sha256'),('ANALYSIS_PLAN.md','analysis_plan_sha256'),('EXECUTION_PROTOCOL.md','execution_protocol_sha256')]:
            assert file_hash(PACKET/file) == cohort[key]
        assert cohort['roster_order'] == [r['life_id'] for r in rows] and cohort['continuations'] == []
        current = identity(); assert hashlib.sha256(canonical(current)).hexdigest() == RUNTIME
        assert file_hash(PACKET/'shared'/(RUNTIME+'.json')) == RUNTIME
        assert shutil.disk_usage(HERE).free >= 2750000000
        (HERE/'approvals').mkdir(); (HERE/'grants').mkdir()
        for i,row in enumerate(rows,1):
            a = read_authority(i); e = exact_engine(a, True)
            c = cohort['lives'][i-1]
            assert (c['life_id'],c['stream_life'],c['initial_causal_sha256'],c['initial_snapshot_sha256']) == (row['life_id'],i,a['runner_scope']['initial_causal_sha256'],a['initial_snapshot']['sha256'])
            notice = f"Jason explicitly authorized {row['life_id']} once in roster order under outer SHA256 {HASHES[i-1]}. Exact preserved instruction: JASON_AUTHORIZATION.md SHA256 {file_hash(HERE/'JASON_AUTHORIZATION.md')}. No continuation, retry, replacement or extension authorized."
            approval = HERE/'approvals'/(row['life_id']+'.json')
            atomic_json(approval, dict(notice=notice, approved_scope=a['runner_scope']))
            grant = dict(a['runner_scope'], request_path=str(approval), request_sha256=file_hash(approval))
            validate_grant(grant,e,None); save('grants/'+row['life_id']+'.json',grant)
        del e; gc.collect()
        preflight_wall += time.perf_counter()-tick
        assert preflight_wall < resource['full_preflight_allowance_seconds']
        # Count all required immutable prepared inputs once, including fields.
        input_paths = set()
        for folder in ('authorities','birth_manifests','initial_states','prehistory','shared'):
            input_paths.update(p for p in (PACKET/folder).rglob('*') if p.is_file())
        input_paths.update(PACKET/n for n in ('COHORT_MANIFEST.json','RESOURCE_PLAN.json','EXECUTION_PROTOCOL.md','ANALYSIS_PLAN.md'))
        fixed_bytes = sum(p.stat().st_size for p in input_paths) + sum(p.stat().st_size for p in HERE.rglob('*') if p.is_file()) + 2000000
        save('PREFLIGHT.json',dict(status='PASS',utc=utc(),wall_seconds=preflight_wall,
            authority_count=12,blank_states=12,correct_streams=12,full_runtime_sha256=RUNTIME,
            checkpoint=CHECKPOINT,P_commit=P,git_clean=True,simulated_steps=0,
            frozen_configuration=True,prehistory_reused_only=True,continuations_authorized=0,
            fixed_input_and_metadata_reserve_bytes=fixed_bytes,disk_free_bytes=shutil.disk_usage(HERE).free,
            memory=memory()))
        log('PREFLIGHT_PASS', cases=12, wall_seconds=preflight_wall)
        (HERE/'lives').mkdir()
        for i,row in enumerate(rows,1):
            run = None
            if active_wall >= resource['execution_allowance_seconds'] or fixed_bytes+closed_bytes+16000000 >= resource['aggregate_primary_limit_bytes']:
                stop = 'aggregate_resource_exhausted_before_launch'; break
            tick = time.perf_counter(); source_gate(); a = read_authority(i); e = exact_engine(a)
            grant = json.loads((HERE/'grants'/(row['life_id']+'.json')).read_bytes())
            assert {k:v for k,v in grant.items() if k not in ('request_path','request_sha256')} == a['runner_scope']
            validate_grant(grant,e,None)
            assert not (HERE/'lives'/row['life_id']).exists()
            assert shutil.disk_usage(HERE).free >= 1250000000
            preflight_wall += time.perf_counter()-tick
            assert preflight_wall < resource['full_preflight_allowance_seconds']
            row['state']='STARTING'; row['launch_utc']=utc()
            log('LAUNCH', life_id=row['life_id'], authority_sha256=HASHES[i-1], preflight_total_wall_seconds=preflight_wall)
            started = time.perf_counter()
            run = Life(e,HERE/'lives'/row['life_id'],grant,asset_root=HERE/'shared-assets')
            if run.identity_sha256 != RUNTIME:
                run.close('administrative_pause','runtime_identity_mismatch'); raise RuntimeError('runtime mismatch before advance')
            row['state']='RUNNING'; next_progress=time.perf_counter()+30
            while not run.closed:
                if active_wall+time.perf_counter()-started >= resource['execution_allowance_seconds']:
                    stop='aggregate_wall_time'; run.close('resource_pause',stop); break
                if fixed_bytes+closed_bytes+run.bytes_written+16000000 >= resource['aggregate_primary_limit_bytes']:
                    stop='aggregate_storage'; run.close('resource_pause',stop); break
                run.advance(1)
                if time.perf_counter()>=next_progress:
                    log('PROGRESS',life_id=row['life_id'],native_index=e.native_index,simulated_seconds=e.time,
                        active_wall_seconds=time.perf_counter()-started,closed_chunk_bytes=run.bytes_written,memory=memory())
                    next_progress=time.perf_counter()+30
            elapsed=time.perf_counter()-started; active_wall+=elapsed
            r=run.receipt
            size=sum(p.stat().st_size for p in run.store.iterdir() if p.is_file()); closed_bytes+=size
            row.update(state=r['status'],cause=r['cause'],complete=r['complete'],native_steps=r['native_steps'],
                waves=r['wave_index'],simulated_seconds=r['final_time'],active_wall_seconds=elapsed,
                primary_bytes=size,receipt_sha256=file_hash(run.store/'segment-000.json'),stop_utc=utc())
            save(row['life_id']+'_STOP.json',dict(row))
            log('STOP',**row)
            if active_wall>=resource['execution_allowance_seconds']:stop='aggregate_wall_exhausted_at_close'
            if fixed_bytes+closed_bytes>=resource['aggregate_primary_limit_bytes']:stop='aggregate_storage_exhausted_at_close'
            del run,e; run=None;gc.collect()
            if stop:break
        source_gate()
    except BaseException as error:
        stop=f'{type(error).__name__}: {error}'
        if run is not None:
            row.update(state='APPARATUS_FAILURE',native_steps=run.engine.native_index,
                       waves=run.engine.organism.wave_count,simulated_seconds=run.engine.time,complete=False)
        save('BATCH_FAULT.json',dict(error=stop,traceback=traceback.format_exc(),utc=utc()))
        log('BATCH_STOP',error=stop)
    finally:
        save('DENOMINATOR_SEALED.json',dict(schema=1,utc=utc(),checkpoint=CHECKPOINT,P_commit=P,
            authorization_sha256=file_hash(HERE/'JASON_AUTHORIZATION.md'),roster=rows,batch_stop=stop,
            active_execution_wall_seconds=active_wall,closed_life_bytes=closed_bytes,
            preflight_wall_seconds=preflight_wall,all_twelve_considered=True,
            no_interpretation_during_execution=True,live_recording='Tier 1 only',
            retries=0,continuations=0,replacements=0,additional_cases=0,final_process_memory=memory()))
        log('STAGE_STOPPED',launched=sum(r['state']!='NOT_STARTED' for r in rows),
            sealed=sum(r.get('complete',False) for r in rows),batch_stop=stop,active_execution_wall_seconds=active_wall)

if __name__=='__main__':
    main()
