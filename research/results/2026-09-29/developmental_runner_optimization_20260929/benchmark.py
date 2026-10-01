"""One explicitly requested engineering benchmark per invocation; no science outcomes."""
import argparse
import copy
import ctypes
from ctypes import wintypes
import hashlib
import json
from pathlib import Path
import sys
import time
import zlib

ROOT=Path(__file__).resolve().parent.parent
D=ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'
sys.path.insert(0,str(D))
from loom_p.schema import Config
from loom_p.smokes import make_case
from loom_commissioning.contract import make_manifest,INTACT
from loom_commissioning.runner import Run
from loom_developmental import codec,core
from loom_developmental.runner import Life,create_engineering_grant
from loom_developmental.verify import verify_store
from loom_developmental.replay import reconstruct
from profiling import Meter

CACHE=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\developmental_ecology\artifacts\prehistory-attempt-001')
REQUEST=Path(r'C:\Users\Jason\.codex\attachments\400b7786-b3fc-4525-b4cb-f23c18150dff\Pasted text.txt')
OUT=Path(__file__).resolve().parent/'measurements'
OUT.mkdir(exist_ok=True)

class Counters(ctypes.Structure):
    _fields_=[('cb',wintypes.DWORD),('PageFaultCount',wintypes.DWORD)]+[(n,ctypes.c_size_t) for n in
        ('PeakWorkingSetSize','WorkingSetSize','QuotaPeakPagedPoolUsage','QuotaPagedPoolUsage',
         'QuotaPeakNonPagedPoolUsage','QuotaNonPagedPoolUsage','PagefileUsage','PeakPagefileUsage')]
def memory():
    k=ctypes.WinDLL('kernel32');p=ctypes.WinDLL('psapi');k.GetCurrentProcess.restype=wintypes.HANDLE
    p.GetProcessMemoryInfo.argtypes=[wintypes.HANDLE,ctypes.POINTER(Counters),wintypes.DWORD]
    c=Counters();c.cb=ctypes.sizeof(c)
    if not p.GetProcessMemoryInfo(k.GetCurrentProcess(),ctypes.byref(c),c.cb):raise ctypes.WinError()
    return {'peak_working_set_bytes':c.PeakWorkingSetSize,'working_set_bytes':c.WorkingSetSize,
            'peak_pagefile_bytes':c.PeakPagefileUsage}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('case',choices=['old-profile','old-short','lean-profile','lean-short','medium','long'])
    parser.add_argument('--label',help='Explicit unique engineering measurement label; never overwrites a prior result')
    args=parser.parse_args();case=args.case
    label=args.label or case
    if not label.replace('-','').isalnum():raise ValueError('invalid measurement label')
    destination=OUT/label
    if destination.exists() or (OUT/(label+'.json')).exists():raise FileExistsError('No implicit benchmark retry')
    c=Config(**json.loads((D/'configuration.json').read_text()))
    e=make_case(c,'nonzero_resume_1s',CACHE)
    if case in ('medium','long'):
        e.body.energy=1.;e.body.integrity=1.
        e.fixture={**e.fixture,'manufactured_EI':[1.,1.],
                   'scientific_use':False,'neural_state':'original nonzero fixture unchanged'}
    seconds={'old-profile':.2,'old-short':.6,'lean-profile':.2,'lean-short':.6,'medium':30.,'long':600.}[case]
    profile=case.endswith('profile');meter=Meter();memory_before=memory()
    if case.startswith('old-'):
        m=make_manifest(e,'fixture-context-profile',INTACT,'none',seconds,wall_limit=600,storage_limit=2_000_000_000)
        if profile:meter.start()
        start=time.perf_counter();run=Run(e,m,destination);setup=time.perf_counter()-start;blocks=[]
        for _ in range(round(seconds/.1)):
            tick=time.perf_counter();t=e.time;run.advance(10)
            blocks.append({'ending_native_index':e.native_index,'simulated_seconds':e.time-t,'wall_seconds':time.perf_counter()-tick})
        wall=time.perf_counter()-start
        prof=meter.stop() if profile else None
        result={'profile':prof,'wall_seconds':wall,'setup_wall_seconds':setup,'blocks':blocks,'simulated_seconds':e.time,
            'native_steps':e.native_index,'waves':e.organism.wave_count,'memory':memory(),
            'bytes_by_file':{p.name:p.stat().st_size for p in destination.iterdir() if p.is_file()}}
    else:
        g=create_engineering_grant(e,round(seconds/.01),REQUEST,wall_limit=7200,storage_limit=4_000_000_000)
        if profile:meter.start()
        start=time.perf_counter();run=Life(e,destination,g);setup=time.perf_counter()-start
        block=[];begin=time.perf_counter()
        while not run.closed:
            count=min(1000,g['end_index']-e.native_index);t=e.time;tick=time.perf_counter()
            run.advance(count)
            row={'ending_native_index':e.native_index,'simulated_seconds':e.time-t,
                'wall_seconds':time.perf_counter()-tick,**memory()};block.append(row)
            print(json.dumps({'case':case,**row}),flush=True)
        execute=time.perf_counter()-begin
        prof=meter.stop() if profile else None
        wall=time.perf_counter()-start
        result={'simulated_seconds':e.time,'native_steps':e.native_index,'waves':e.organism.wave_count,
            'wall_seconds':wall,'setup_wall_seconds':setup,'execution_wall_seconds':execute,
            'profile':prof,'blocks':block,'memory':memory(),'memory_before':memory_before,
            'stop_status':run.receipt['status'],'initial_fixture':e.fixture,
            'checkpoint_measurements':run.receipt['checkpoints'],'recording_timings':run.receipt['timings'],
            'shared_asset_bytes':sum(p.stat().st_size for p in run.asset_root.glob('*.json')),
            'stored_bytes':sum(p.stat().st_size for p in destination.iterdir() if p.is_file())}
        # Full passive audit is timed separately, never included in execution.
        check=verify_store(destination);result['verification']=check
        # Codec tradeoff: same completed native chunk, no world execution.
        if run.receipt['chunks']:
            first=run.receipt['chunks'][0];blob=codec.encode(codec.read(destination/first['file'],first['sha256']))
            compression=[]
            for level in (0,1,3,6):
                tick=time.perf_counter();packed=zlib.compress(blob,level) if level else blob;elapsed=time.perf_counter()-tick
                tick=time.perf_counter();unpacked=zlib.decompress(packed) if level else packed;read_time=time.perf_counter()-tick
                assert unpacked==blob
                compression.append({'level':level,'input_bytes':len(blob),'stored_bytes':len(packed),
                    'compress_seconds':elapsed,'decompress_seconds':read_time})
            result['compression_benchmark']=compression
    result['no_scientific_outcome_analysis']=True
    result['measurement_label']=label
    (OUT/(label+'.json')).write_text(json.dumps(result,indent=2),encoding='utf8')
    print(json.dumps({'case':case,'completed':True,'wall_seconds':result['wall_seconds'],
                      'simulated_seconds':result['simulated_seconds'],'memory':result['memory']}),flush=True)

if __name__=='__main__':main()
