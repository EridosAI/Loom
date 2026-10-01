"""One saved-record A3 analysis after the single attempt has stopped."""
import datetime,json,pathlib,shutil,sys,time,traceback
from a3_observations import *
BASE=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\commissioning-A3-20260925-5f077481')
OUT=BASE/'read-only-review'
S=pathlib.Path(__file__).resolve().parent
def write(name,obj):
    with (OUT/name).open('x',encoding='utf-8') as f:f.write(json.dumps(obj,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def main():
    started=time.perf_counter();assert (BASE/'EXECUTION_RESULT.json').exists(),'Attempt has not stopped'
    assert not (OUT/'ANALYSIS_RESULT.json').exists(),'No overwrite/retry of this analysis'
    before={str(p):shafile(p) for p in BASE.rglob('*') if p.is_file() and not p.is_relative_to(OUT)}
    write('RAW_EVIDENCE_BEFORE_ANALYSIS.json',before)
    filenames=('read_results.py','a3_analysis_core.py','a3_observations.py','evidence.py','v3_checker_v1_1.py','prepare_analysis.py')
    for n in filenames:shutil.copyfile(S/n,OUT/n)
    results={};errors={}
    def attempt(n,fn):
        try:v=fn();write(n+'.json',v);results[n]=v;return v
        except Exception as ex:
            err={'exception':repr(ex),'traceback':traceback.format_exc()};errors[n]=err;write(n+'_ERROR.json',err);return None
    try:d=Data(BASE)
    except Exception as ex:
        d=None;errors['DATA_LOADING']={'exception':repr(ex),'traceback':traceback.format_exc()};write('DATA_LOADING_ERROR.json',errors['DATA_LOADING'])
    if d is not None:
        attempt('RECORD_INTEGRITY',lambda:record_integrity(d))
        attempt('BOUNDARY_AND_DELIVERY',lambda:boundary_check(d))
        led=attempt('ACCOUNTING',lambda:ledger_check(d))
        if led is not None:
            ws=attempt('ALL_FIXED_WINDOWS',lambda:fixed_windows(d,led))
            if ws is not None:
                def observe():
                    o,q=physical_observations(d,led,ws);write('REPAIR_EVENT_LEDGER.json',q);return o
                attempt('A3_OBSERVATIONS',observe)
    after={p:shafile(p) for p in before};write('RAW_EVIDENCE_AFTER_ANALYSIS.json',after)
    elapsed=time.perf_counter()-started
    result={'analysis_version':'A3 read-only v1.0','authority_sha256':AUTH,'completed_sections':list(results),'errors':errors,
      'raw_files_checked':len(before),'original_raw_files_unchanged':before==after,'analysis_wall_seconds':elapsed,
      'within_one_hour_allowance':elapsed<3600,'new_simulation_steps':0,'controller_command_computations':0,'physical_replays':0,
      'research_module_imports':[n for n in sys.modules if n.startswith(('loom_p','loom_commissioning'))],
      'analysis_sources':{n:shafile(OUT/n) for n in filenames},
      'generic_check_origin':str(ROOT/'a2_execution_staging_20260925/a2_analysis_core.py'),
      'timing_rule':'Prospectively approved symmetric 1e-10 boundary membership. Original A2 helper/results untouched.',
      'scope':'Saved data only; no original source patch, controller recomputation, replay, live observer or viewer.'}
    assert not result['research_module_imports'];write('ANALYSIS_RESULT.json',result)
    print(json.dumps(result,indent=2))
    if 'A3_OBSERVATIONS' in results:
        o=results['A3_OBSERVATIONS']
        compact={'whole_case':o['whole_case'],'milestones':o['milestones'],
          'wall_force_range':o['wall']['sustained_force_range'],'repair_force_range':o['repair']['sustained_force_range'],
          'repair_quality_range':o['repair']['quality_range'],'eligible_repair_seconds':o['repair']['eligible_duration'],
          'positive_restoration_seconds':o['repair']['positive_restoration_duration'],
          'repair_cost':o['repair_arrival_to_departure_or_stop'],'return_travel':o['repair_to_energy_travel'],
          'source3_transfer':o['energy']['source3_transfer_total'],'first_positive_net_energy_window':o['energy']['first_positive_net_window'],
          'mover_contact_count':len(o['mover']['certified_contacts'])}
        write('A3_RESULT_SUMMARY.json',compact)
        print(json.dumps({'whole_case':o['whole_case'],'milestone_times':{k:v.get('time') for k,v in o['milestones'].items()},
          'repair_contact_seconds':o['repair']['positive_duration_contact_seconds'],'eligible_seconds':o['repair']['eligible_duration'],
          'source3_transfer':o['energy']['source3_transfer_total']},indent=2))
if __name__=='__main__':main()
