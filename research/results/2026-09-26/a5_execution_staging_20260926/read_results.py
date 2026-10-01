"""One post-stop, saved-data A5 review. No simulation or command recomputation."""
import datetime,json,pathlib,shutil,sys,time,traceback
from a5_observations import *
S=pathlib.Path(__file__).resolve().parent
BASE=ROOT/'worktrees/loom-p-clock-correction-20260926/developmental_ecology/artifacts/commissioning-A5-20260926-68db2c58'
OUT=BASE/'read-only-review'
DEADLINE=None

def resource_preflight(estimated_write_bytes):
    roots=json.loads((OUT/'PREFLIGHT.json').read_bytes())['disk_accounting_roots']
    used=sum(p.stat().st_size if p.is_file() else sum(q.stat().st_size for q in p.rglob('*') if q.is_file()) if p.exists() else 0 for p in map(pathlib.Path,roots))
    assert used+estimated_write_bytes<=10_000_000_000,'Combined new-artifact cap before analysis write'
    assert shutil.disk_usage(BASE).free>=estimated_write_bytes+1_000_000_000,'Finalization free-space reserve'
    assert datetime.datetime.now(datetime.timezone.utc)<DEADLINE,'Saved-data reporting allowance exhausted'

def write(name,obj):
    with (OUT/name).open('x',encoding='utf-8') as f:f.write(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')

def main():
    global DEADLINE
    started=time.perf_counter();assert (BASE/'EXECUTION_RESULT.json').exists(),'Single attempt has not stopped'
    stop=json.loads((BASE/'EXECUTION_RESULT.json').read_bytes())['first_stop_utc']
    DEADLINE=datetime.datetime.fromisoformat(stop)+datetime.timedelta(seconds=3600)
    resource_preflight(400_000_000)
    assert not (OUT/'ANALYSIS_STARTED.json').exists(),'Do not overwrite or silently retry analysis'
    write('ANALYSIS_STARTED.json',dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),allowance_seconds=3600))
    before={str(p):shafile(p) for p in BASE.rglob('*') if p.is_file() and not p.is_relative_to(OUT)}
    write('RAW_EVIDENCE_BEFORE_ANALYSIS.json',before)
    filenames=('read_results.py','a5_analysis_core.py','a5_observations.py','evidence.py','v3_checker_v1_1.py','prepare_reader.py')
    for n in filenames:shutil.copyfile(S/n,OUT/n)
    results={};errors={}
    def attempt(n,fn):
        try:
            assert time.perf_counter()-started<3600
            v=fn();write(n+'.json',v);results[n]=v;return v
        except Exception as ex:
            err=dict(exception=repr(ex),traceback=traceback.format_exc());errors[n]=err;write(n+'_ERROR.json',err);return None
    try:d=Data(BASE)
    except Exception as ex:
        d=None;errors['DATA_LOADING']=dict(exception=repr(ex),traceback=traceback.format_exc());write('DATA_LOADING_ERROR.json',errors['DATA_LOADING'])
    if d is not None:
        attempt('RECORD_INTEGRITY',lambda:record_integrity(d))
        attempt('BOUNDARY_AND_DELIVERY',lambda:boundary_check(d))
        led=attempt('ACCOUNTING',lambda:ledger_check(d))
        if led is not None:
            def measure():
                o,w=observations(d,led);write('ALL_FIXED_WINDOWS.json',w);save_plot_data(d,OUT);write('A5_RESULT_SUMMARY.json',o['summary'])
                actions={a['native_index']:a for a in d.controller}
                rows=[]
                for i in (26949,26950,26951,26999,27000,27001,30000,45000,48000,63000):
                    rows.append(dict(native_index=i,observed=i<=len(d.native),
                                     native_record=d.native[i-1] if i<=len(d.native) else None,
                                     issued_decision=actions.get(i)))
                write('CLOCK_BOUNDARY_OBSERVATIONS.json',dict(method='Saved records only; no clock mutation or command recomputation.',rows=rows))
                return o
            attempt('A5_OBSERVATIONS',measure)
    after={p:shafile(p) for p in before};write('RAW_EVIDENCE_AFTER_ANALYSIS.json',after)
    result=dict(authority_sha256=AUTH,completed_sections=list(results),errors=errors,raw_files_checked=len(before),
                original_raw_files_unchanged=before==after,analysis_wall_seconds=time.perf_counter()-started,
                new_simulation_steps=0,controller_command_computations=0,physical_replays=0,
                research_module_imports=[n for n in sys.modules if n.startswith(('loom_p','loom_commissioning'))],
                sources={n:shafile(OUT/n) for n in filenames},
                scheduler_check='Independent integer stage ownership and binary64 clock consistency arithmetic; no production command function called.',
                scope='Saved data only; original evidence and production code unchanged. No world replay, sensor resampling, policy or parameter change.')
    assert not result['research_module_imports'];write('ANALYSIS_RESULT.json',result)
    print(json.dumps(result,indent=2))
    if 'A5_OBSERVATIONS' in results:print(json.dumps(results['A5_OBSERVATIONS']['summary'],indent=2))

if __name__=='__main__':main()
