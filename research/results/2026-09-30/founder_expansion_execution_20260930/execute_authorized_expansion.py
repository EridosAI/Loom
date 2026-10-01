"""Single-use outer executor for Jason's 48 exact expansion grants. No physics changes.

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
PACKET = ROOT / 'exports/2026-09-30-Founder-Search-expansion-48'
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
COHORT = '6f0f0ddd9fd1c7605c8ce5c08f24d0db81b44a65d8f9089c1df78a900f36514a'
HASHES = ['e51da05996470950c61811b3b4a2c42c659ddffc95f52ec4cf34aaac37937e17', 'a68102400d229b1666c6e88203a436e9f6e03da4ac146f6d8d378e0dd00c9549', 'ae4a8b42dc4afa33d6e03dcd94d73b7ff6332a46ab94fa54db319fcd6f3d0647', '0d7c4f1ae0355815c3b03cef58d6e52d18104fb1600c0405c4710e6f1270720e', 'b8c9ffc0a7e3f7ac59f5fe8e8410cd46c7328085bed7ec814f7285e7f5a2f33b', '9bdb6a53f858743f6c338d12e6a1e4f985c733cfe7d6cff2efd7a1b776e6c31e', 'd0fc291d745f2bbf9cde36d8e3117a516c071eff284354ee2034c057e5513ae3', 'bbc4c4817ba620deff4a9e4aff1ef29da38c2851e99a38ba6f06b339e3a92405', 'fb22143be6c3b69fb33cc9f207a87dd346d3744f692fa33bd6a41e3df5d65ccf', 'f6ef94442bb1b6eec5c558304fbd21bab85f877974de776d4a45dca3e6f90536', '75d9db7950a54a833dc6c3ac43de2a95e50785e49d0d1ff4a078da20c73e2ac2', '5d27d0a018e840d35b62984de25dceba5a7a7683a8c5919f522ad71595e83369', 'e05efb41ae239303d60b3f11402dd72383a0c96f4ed2d4114a2ba2425dd7d263', 'f351a43da2cf754f2f38900364d2545f7e85723d030bc75606cb7dbbd7a94d61', 'af3e8719cae5f9520ea84d7f601c3f3551301557f836469f5b7b5c8ffd992b7a', 'ae17e3649c5fa27be4c2fb6839929f4605a338bc2902b59f129ad8b916c21f94', '2d160da5d75de5dad16738e245f56040615d232896d3a49aee2a1b55f73e90ae', '37180c51cec64e1aaea170bd49a166b8a85a1182e4cfc642fcd52119b6d3d0c8', 'afad2cd7b021252e80e41feca25c6fb78da1add396910cb782841798a158079e', 'ee9e51569b178a626611058cd60a4343ac839705dc344d62c22c1156c99ddea7', '8c1ebf2c529369a0a44df0ee60fd131a6cebf4b9480e2cae43f8e6dca7e7a32c', 'c5fd0986c0376fed53be8abdae8d6912f2ef2e2601721af5e25ade14b3be3bf6', 'af56e148a054a6ff937e23f6d0c5bbd9bf2544d8932dddc1d6e6f229efe0e5a3', '767f5bcb1e250314d80f4a7d64c7b855a254fd89d5eec4d4d8ed7da9342d5ff4', '06542240be2e6e170c679c3a373036f4d09481c36a8e9e7b21ba88dc1b9590e6', '34ac214bcd51ba0e05b7913d0049e00294c1970f5247dc88e7bdcacf218e4e1e', 'ce55944b1e84268be0a8c0d527968112600c8bd55df634f7948030289ce98d99', '131a817c3103d4c4d5072a6ef429d1ced42bd121a68d2289793deaaa5b99456e', 'd24db714908d34afc2b697b65467c2b2105024a5e4175b473931673ad0610a0c', '2ff5e6272e45fb8c636aed341c110c9617b87d6ad4865cc61cf564a71c74d900', 'ba37315fee4dfef7d14b5699ef403ebe317fb6e364bee90d44636c420fb46394', '5d48a3a03978e15a8781278e793ab01e9055d5def8905cb2cba80c47752ebf65', '3a959c69cd191bd2fb6bcc20f04dbffa16d52c814ec8dfa6ab110a5e1c3e932f', 'd9506e5196804299b3bc078ceb18d770f29b37a1a7a22366d904b02d870e40de', '3a028d5bfc021ee14bc3b6043ec731a001d4d99f2debbd8d017471503f4c49d9', 'fbe712866f2dec4613cc2db1bc6de1626312aeceed97435f075c5aa13631f160', '6651934168079a5a50b759ea31bcab078ea469f99f74fdb7879bf71f22d446a6', '3c20ee980c998cc9c86184859d44c89fe61d2a7e720a87fdd2e2adc62786a1dd', 'd43ed54fdba64e6880ba4773fd7a8ea25ca71637a428f9e144b5f93c1ea003b7', '180b49e7ae34a4c6ffe943d8a598504d8d287ff4377b6655adac6e45629b116b', 'ebad356fdf3e7b58068aa1626d9fc5423fe8493e4b2fa875937a4aba2c635c01', '82be4892fa5c1bfc74c7960e6cef33ae998455ec7b1f7b1d0b54eccba369bb6d', '6664cedc41b7fc78192e1b7682ece6a47ab2d9f11c6e6e7afd020aab82ac85c4', 'ad31dc1b86485b6f5d4eba148595bf7b1026c496a772d36ffb87e2d7553a9ae6', '14729605ff88cb72ebebb65ccab39aa8ec9f7d2850d829cb7957adee26cbb43f', 'f42cbf7e228ba476fceca8e0d0aed8bdb9fa889ededb59fad619ed3efccbdf84', '05f61ded7d45b8c3c1e934308e7235e003c218b5fdbaf50e10d825c85152c262', 'af27c6aebda0781bf337119ad5db7736930726172db5c188f1ff9283a7e3743d']

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
    assert data == canonical(a) and hashlib.sha256(data).hexdigest() == HASHES[i-13]
    assert a['ordinal'] == i-12 and a['birth_id'] == i and a['life_id'] == name and a['master_seed'] == 5284097
    assert a['P_commit'] == P and a['apparatus_checkpoint'] == CHECKPOINT and a['runtime_sha256'] == RUNTIME
    assert a['cohort_manifest_sha256'] == COHORT
    assert a['retry'] is a['continuation'] is a['substitution'] is a['outcome_intervention'] is False
    assert a['external_controller'] is None and a['simulation_ceiling_seconds'] == 600
    assert a['evidence_identity']['attempt_limit'] == 1 and a['evidence_identity']['parent_receipt'] is None
    s = a['runner_scope']
    assert s['kind'] == 'developmental-intact-P' and s['life_id'] == name
    assert s['initial_index'] == 0 and s['end_index'] == 60000 and s['parent_receipt_sha256'] is None
    assert (s['wall_limit_seconds'], s['storage_limit_bytes'], s['checkpoint_stride'], s['chunk_steps'], s['compression_level']) == (900,83333333,6000,100,1)
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
                 native_steps=0, waves=0, simulated_seconds=0.) for i,h in enumerate(HASHES,13)]
    active_wall = 0.; closed_bytes = 0; preflight_wall = 0.; stop = None; run = None
    resource = json.loads((PACKET / 'RESOURCE_PLAN.json').read_bytes())
    try:
        tick = time.perf_counter(); source_gate()
        assert file_hash(PACKET/'PACKAGE_MANIFEST.json') == 'e7f8ae88d546c4419b1c4bc5cc2587f5c9ba822c17b1599f9466d9069609ea6e'
        manifest=json.loads((PACKET/'PACKAGE_MANIFEST.json').read_bytes())
        for entry in manifest['files']:
            f=PACKET/entry['path']
            assert f.stat().st_size==entry['bytes'] and file_hash(f)==entry['sha256'], entry['path']
        import re
        actual=re.findall(r'\d+\. (FS-\d{3}) — ([a-f0-9]{64})',(HERE/'JASON_AUTHORIZATION.md').read_text(encoding='utf-8-sig'))
        assert actual==[(r['life_id'],r['authority_sha256']) for r in rows]
        prior=ROOT/'founder_initial_execution_20260930'
        assert file_hash(prior/'DENOMINATOR_SEALED.json')=='1d3950dc462d2e003016fdb511d21871e8d3c4f6bd7caa5f81bfed1d51ed1d5a'
        assert file_hash(prior/'DELIVERY_VERIFICATION.json')=='3e389bcf6cc6571523fb4fde4db28a292e4994d35432a16f06ff34c3c565b48c'
        cohort = json.loads((PACKET/'COHORT_MANIFEST.json').read_bytes())
        assert file_hash(PACKET/'COHORT_MANIFEST.json') == COHORT
        for file,key in [('RESOURCE_PLAN.json','resource_plan_sha256'),('ANALYSIS_PLAN.md','analysis_plan_sha256'),('EXECUTION_PROTOCOL.md','execution_protocol_sha256')]:
            assert file_hash(PACKET/file) == cohort[key]
        assert cohort['roster_order'] == [r['life_id'] for r in rows] and cohort['continuations'] == []
        current = identity(); assert hashlib.sha256(canonical(current)).hexdigest() == RUNTIME
        assert file_hash(PACKET/'shared'/(RUNTIME+'.json')) == RUNTIME
        assert shutil.disk_usage(HERE).free >= resource['total_additional_planning_bytes']
        (HERE/'approvals').mkdir(); (HERE/'grants').mkdir()
        for i,row in enumerate(rows,13):
            a = read_authority(i); e = exact_engine(a, True)
            c = cohort['lives'][i-13]
            assert (c['life_id'],c['stream_life'],c['initial_causal_sha256'],c['initial_snapshot_sha256']) == (row['life_id'],i,a['runner_scope']['initial_causal_sha256'],a['initial_snapshot']['sha256'])
            notice = f"Jason explicitly authorized {row['life_id']} once in roster order under outer SHA256 {HASHES[i-13]}. Exact preserved instruction: JASON_AUTHORIZATION.md SHA256 {file_hash(HERE/'JASON_AUTHORIZATION.md')}. No continuation, retry, replacement or extension authorized."
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
            authority_count=48,blank_states=48,correct_streams=48,full_runtime_sha256=RUNTIME,
            checkpoint=CHECKPOINT,P_commit=P,git_clean=True,simulated_steps=0,
            frozen_configuration=True,prehistory_reused_only=True,continuations_authorized=0,
            fixed_input_and_metadata_reserve_bytes=fixed_bytes,disk_free_bytes=shutil.disk_usage(HERE).free,
            memory=memory()))
        log('PREFLIGHT_PASS', cases=48, wall_seconds=preflight_wall)
        (HERE/'lives').mkdir()
        for i,row in enumerate(rows,13):
            run = None
            if active_wall >= resource['execution_allowance_seconds'] or fixed_bytes+closed_bytes+16000000 >= resource['aggregate_primary_limit_bytes']:
                stop = 'aggregate_resource_exhausted_before_launch'; break
            tick = time.perf_counter(); source_gate(); a = read_authority(i); e = exact_engine(a)
            grant = json.loads((HERE/'grants'/(row['life_id']+'.json')).read_bytes())
            assert {k:v for k,v in grant.items() if k not in ('request_path','request_sha256')} == a['runner_scope']
            validate_grant(grant,e,None)
            assert not (HERE/'lives'/row['life_id']).exists()
            assert not (HERE/(row['life_id']+'_STOP.json')).exists()
            assert shutil.disk_usage(HERE).free >= 1250000000
            preflight_wall += time.perf_counter()-tick
            assert preflight_wall < resource['full_preflight_allowance_seconds']
            row['state']='STARTING'; row['launch_utc']=utc()
            log('LAUNCH', life_id=row['life_id'], authority_sha256=HASHES[i-13], preflight_total_wall_seconds=preflight_wall)
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
                    if shutil.disk_usage(HERE).free < 1000000000:
                        stop='shared_disk_headroom'; run.close('resource_pause',stop); break
            elapsed=time.perf_counter()-started; active_wall+=elapsed
            r=run.receipt
            size=sum(p.stat().st_size for p in run.store.iterdir() if p.is_file()); closed_bytes+=size
            row.update(state=r['status'],cause=r['cause'],complete=r['complete'],native_steps=r['native_steps'],
                waves=r['wave_index'],simulated_seconds=r['final_time'],active_wall_seconds=elapsed,
                primary_bytes=size,wall_allowance_overrun_seconds=max(0.,elapsed-900),receipt_sha256=file_hash(run.store/'segment-000.json'),stop_utc=utc())
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
            preflight_wall_seconds=preflight_wall,all_forty_eight_considered=True,
            no_interpretation_during_execution=True,live_recording='Tier 1 only',
            retries=0,continuations=0,replacements=0,additional_cases=0,final_process_memory=memory()))
        log('STAGE_STOPPED',launched=sum(r['state']!='NOT_STARTED' for r in rows),
            sealed=sum(r.get('complete',False) for r in rows),batch_stop=stop,active_execution_wall_seconds=active_wall)

if __name__=='__main__':
    main()
