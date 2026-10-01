"""Measure the existing intact-P apparatus, without changing its implementation."""
import cProfile
import ctypes
import json
from pathlib import Path
import pstats
import sys
import time
import hashlib

ROOT=Path(__file__).resolve().parent.parent
W=ROOT/'worktrees/loom-p-b1-minimal-20260929'
D=W/'developmental_ecology'
sys.path.insert(0,str(D))
import numpy as np
from loom_p.schema import Config
from loom_p.smokes import make_case
from loom_p.records import state_hash,save_snapshot,code_identity
from loom_commissioning.contract import make_manifest,INTACT
from loom_commissioning.runner import Run

CACHE=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\developmental_ecology\artifacts\prehistory-attempt-001')
OUT=Path(__file__).resolve().parent/'baseline'
OUT.mkdir(exist_ok=False)
CONFIG=Config(**json.loads((D/'configuration.json').read_text()))

def category(file,name):
    f=file.replace('\\','/').lower(); n=name.lower()
    if 'receiver' in n:return 'detached_D5'
    if 'save_restart' in n or 'load_restart' in n or 'save_snapshot' in n:return 'snapshot_generation'
    if 'deepcopy' in n or f.endswith('/copy.py'):return 'state_copy'
    if 'hashlib' in f or 'openssl' in n or 'digest' in n or n in ('state_hash','code_identity','apparatus_identity','file_identity'):return 'hashing'
    if 'gzip' in f or 'zlib' in n or 'compress' in n:return 'compression'
    if 'fsync' in n or 'replace' in n or 'stat'==n or '_io.' in n:return 'filesystem'
    if 'json/' in f or n in ('pack','unpack','view','strict_bytes','canonical','state_bytes','scalar_count'):return 'serialization'
    if 'validat' in n or 'require'==n or 'authority.py' in f or 'contract.py' in f or 'pending.py' in f or n=='_guard':return 'validation'
    if '/loom_p/neural.py' in f:return 'P_neural'
    if '/loom_p/physics.py' in f:return 'physics'
    if '/loom_p/chemistry.py' in f:return 'fields'
    if '/loom_p/geometry.py' in f:return 'geometry_sensing_shared'
    if 'diagnostics.py' in f:return 'observer_diagnostics'
    if n in ('append','_manifest','close') and 'records.py' in f:return 'recorder_writes'
    return 'other_shared_kernels_python'

def stats_report(prof,path):
    prof.dump_stats(str(path.with_suffix('.pstats')))
    stats=pstats.Stats(prof)
    rows=[];bins={}
    for (file,line,name),(primitive,calls,own,cumulative,callers) in stats.stats.items():
        kind=category(file,name);bins[kind]=bins.get(kind,0)+own
        rows.append(dict(file=file,line=line,function=name,calls=calls,exclusive_seconds=own,
                         inclusive_seconds=cumulative,category=kind))
    value=dict(exclusive_seconds_by_category=bins,top_functions=sorted(rows,key=lambda x:-x['exclusive_seconds'])[:80],
        inclusive_core_functions=[x for x in rows if (x['file'].replace('\\','/').endswith('/loom_p/neural.py') and x['function'] in ('native','handoff'))
            or (x['file'].replace('\\','/').endswith('/loom_p/physics.py') and x['function']=='advance')
            or (x['file'].replace('\\','/').endswith('/loom_p/chemistry.py') and x['function']=='step')
            or (x['file'].replace('\\','/').endswith('/loom_p/geometry.py') and x['function']=='transduce')],
        warning='Exclusive bins sum without double counting. Shared kernels remain separate. Inclusive core values overlap exclusive bins; do not add them. Profiler changes wall throughput.')
    path.write_text(json.dumps(value,indent=2))
    return bins

initial=make_case(CONFIG,'nonzero_resume_1s',CACHE)
save_snapshot(OUT/'fixture.snapshot.json.gz',initial)
identities=dict(P=code_identity(),config=CONFIG.identity(),initial_state=state_hash(initial),cache=str(CACHE))
(OUT/'IDENTITIES.json').write_text(json.dumps(identities,indent=2))
results=[]
for label,seconds,profile in [('profiled',.2,True),('unprofiled',.6,False)]:
    e=make_case(CONFIG,'nonzero_resume_1s',CACHE)
    m=make_manifest(e,'fixture-developmental-profile-'+label,INTACT,'none',seconds,wall_limit=600,storage_limit=2_000_000_000)
    prof=cProfile.Profile();start=time.perf_counter()
    if profile:prof.enable()
    init_start=time.perf_counter();run=Run(e,m,OUT/label);init_wall=time.perf_counter()-init_start
    blocks=[]
    for _ in range(round(seconds/.1)):
        start_block=time.perf_counter();run.advance(10)
        blocks.append(dict(native_index=e.native_index,seconds=.1,wall_seconds=time.perf_counter()-start_block))
    total=time.perf_counter()-start
    if profile:prof.disable()
    result=dict(label=label,seconds=seconds,total_wall_seconds=total,initialization_wall_seconds=init_wall,
        wall_seconds_per_simulated_second=total/seconds,blocks=blocks,final_state=state_hash(e),
        bytes_by_file={p.name:p.stat().st_size for p in (OUT/label).iterdir() if p.is_file()},
        final_native_index=e.native_index,final_wave_index=e.organism.wave_count)
    if profile:result['profile_exclusive']=stats_report(prof,OUT/'OLD_PROFILE.json')
    results.append(result);print(json.dumps(result),flush=True)
(OUT/'OLD_RESULTS.json').write_text(json.dumps(results,indent=2))
