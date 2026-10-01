"""Analyze the first stopped A2 once, without replay or controller computation."""
import datetime,json,pathlib,shutil,sys,time,traceback
from a2_analysis_core import *
BASE=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\commissioning-A2-20260925-5f077481')
OUT=BASE/'read-only-review'
def write(name,obj):
    with (OUT/name).open('x',encoding='utf-8') as f:f.write(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def main():
    started=time.perf_counter();assert (BASE/'EXECUTION_RESULT.json').exists(),'Case has not stopped'
    assert not (OUT/'ANALYSIS_RESULT.json').exists(),'No overwrite/retry of this analysis'
    before={str(p):shafile(p) for p in BASE.rglob('*') if p.is_file() and not p.is_relative_to(OUT)}
    write('RAW_EVIDENCE_BEFORE_ANALYSIS.json',before)
    for n in ('read_results.py','a2_analysis_core.py'):shutil.copyfile(pathlib.Path(__file__).resolve().parent/n,OUT/n)
    results={};errors={}
    def attempt(n,fn):
        try:v=fn();write(n+'.json',v);results[n]=v;return v
        except Exception as ex:
            err={'exception':repr(ex),'traceback':traceback.format_exc()};errors[n]=err;write(n+'_ERROR.json',err);return None
    d=None
    # Loading object itself is not JSON; preserve failures before attempting dependent reads.
    try:d=Data(BASE)
    except Exception as ex:
        errors['DATA_LOADING']={'exception':repr(ex),'traceback':traceback.format_exc()};write('DATA_LOADING_ERROR.json',errors['DATA_LOADING'])
    if d is not None:
        attempt('RECORD_INTEGRITY',lambda:record_integrity(d))
        attempt('BOUNDARY_AND_DELIVERY',lambda:boundary_check(d))
        led=attempt('ACCOUNTING',lambda:ledger_check(d))
        if led is not None:
            ws=attempt('ALL_FIXED_WINDOWS',lambda:windows(d,led))
            if ws is not None:attempt('A2_OBSERVATIONS',lambda:physical_observations(d,led,ws))
    after={p:shafile(p) for p in before};write('RAW_EVIDENCE_AFTER_ANALYSIS.json',after)
    duration=time.perf_counter()-started
    result={'analysis_version':'A2 read-only v1.0','authority_sha256':AUTH,'completed_sections':list(results),'errors':errors,
       'original_raw_files_unchanged':before==after,'raw_files_checked':len(before),'analysis_wall_seconds':duration,
       'within_one_hour_allowance':duration<3600,'new_simulation_steps':0,'controller_command_computations':0,'physical_replays':0,
       'research_module_imports':[n for n in sys.modules if n.startswith(('loom_p','loom_commissioning'))],
       'checker_sources':{n:shafile(PACKET/'references'/n) for n in ('v3_checker_v1_1.py','evidence.py')},
       'analysis_sources':{n:shafile(OUT/n) for n in ('a2_analysis_core.py','read_results.py')},
       'scope':'Read-only saved-record analysis; original A1/checker/evidence preserved. No recomputed controller decisions, new observer, simulation or live viewer.'}
    assert not result['research_module_imports'];write('ANALYSIS_RESULT.json',result)
    print(json.dumps(result,indent=2))
    if 'A2_OBSERVATIONS' in results:
        o=results['A2_OBSERVATIONS'];summary={'whole_case':o['whole_case'],'source0':{k:v for k,v in o['sources']['0'].items() if k not in ('contact_intervals','first_positive_net_window')},
          'source1':{k:v for k,v in o['sources']['1'].items() if k not in ('contact_intervals','first_positive_net_window')},
          'release_event':o['release_event'],'travel':o['travel'],'commanded_travel_interval':o['commanded_travel_interval'],
          'negative_residence_window':o['first_negative_residence_window'],'mover':o['mover']}
        write('A2_RESULT_SUMMARY.json',summary);print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
