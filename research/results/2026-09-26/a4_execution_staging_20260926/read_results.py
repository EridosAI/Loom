"""One A4 post-run saved-data analysis and report. No Loom import/replay/control calls."""
import datetime,json,pathlib,shutil,sys,time,traceback
from a4_observations import *
BASE=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\commissioning-A4-20260926-5f077481')
OUT=BASE/'read-only-review';S=pathlib.Path(__file__).resolve().parent
def write(p,v):
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def put(p,text):
    with p.open('x',encoding='utf-8') as f:f.write(text)
def main():
    assert (BASE/'BATCH_EXECUTION_RESULT.json').exists(),'Batch must have stopped'
    assert not (OUT/'ANALYSIS_ATTEMPT.json').exists(),'One analysis attempt; never overwrite outcomes'
    start=time.perf_counter();write(OUT/'ANALYSIS_ATTEMPT.json',{'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'reporting_cap_seconds':600,'batch_authority_sha256':BATCH_AUTH})
    before={str(p):shafile(p) for p in BASE.rglob('*') if p.is_file() and not p.is_relative_to(OUT)};write(OUT/'RAW_EVIDENCE_BEFORE_ANALYSIS.json',before)
    files=['read_results.py','a4_observations.py','a4_analysis_core.py','a4_window_helpers.py','evidence.py','v3_checker_v1_1.py','prepare_analysis.py']
    for n in files:shutil.copyfile(S/n,OUT/n)
    batch=js(BASE/'BATCH_EXECUTION_RESULT.json');reports={};errors={};checks={};resources={}
    for cid in batch['case_order']:
        case=BASE/cid;target=OUT/cid;target.mkdir(exist_ok=False);sections={}
        if not (case/'EXECUTION_RESULT.json').exists():
            reports[cid]={'case_id':cid,'status':'unattempted' if cid in batch['unattempted_cases'] else 'attempted_without_complete_dispatch_result','batch_failure':batch['failure']}
            write(target/'CASE_LIMITATION.json',reports[cid]);continue
        if time.perf_counter()-start>=600:
            errors[cid]={'reason':'read_only_reporting_cap'};break
        def attempt(name,fn):
            try:
                v=fn();write(target/(name+'.json'),v);sections[name]=v;return v
            except Exception as ex:
                err={'exception':repr(ex),'traceback':traceback.format_exc()};errors[cid+'/'+name]=err;write(target/(name+'_ERROR.json'),err);return None
        try:d=Data(case)
        except Exception as ex:
            err={'exception':repr(ex),'traceback':traceback.format_exc()};errors[cid+'/DATA_LOADING']=err;write(target/'DATA_LOADING_ERROR.json',err);continue
        attempt('RECORD_INTEGRITY',lambda:record_integrity(d));attempt('BOUNDARY_AND_DELIVERY',lambda:boundary_check(d))
        ledger=attempt('ACCOUNTING',lambda:ledger_check(d))
        if ledger is not None:
            windows=attempt('ALL_FIXED_WINDOWS',lambda:fixed_windows(d,ledger))
            if windows is not None:
                def observe():
                    o,ev=physical_observations(d,ledger,windows)
                    for n,v in ev.items():write(target/(n.upper()+'.json'),v)
                    return o
                o=attempt('OBSERVATIONS',observe)
                if o is not None:reports[cid]=o
        checks[cid]={name:{k:v for k,v in value.items() if k not in ('rows','mapping','checkpoints')} for name,value in sections.items() if name in ('RECORD_INTEGRITY','BOUNDARY_AND_DELIVERY','ACCOUNTING')}
        resources[cid]={'simulated_seconds':d.final['time'],'native_steps':len(d.native),'recorder_wall_seconds':d.receipt['wall_seconds'],'whole_process_wall_seconds':d.result['whole_process_wall_seconds'],'uncompressed_stream_bytes':d.receipt['uncompressed_bytes'],'stored_trajectory_bytes':sum(p.stat().st_size for p in d.t.iterdir() if p.is_file()),'record_counts':d.receipt['records'],'wall_cap_seconds':d.manifest['execution']['resources']['wall_limit_seconds'],'uncompressed_stream_cap_bytes':d.manifest['execution']['resources']['storage_limit_bytes'],'status':d.receipt['status'],'stop_cause':d.receipt.get('stop_cause'),'complete':d.receipt['complete']}
        print(json.dumps({'case':cid,'sections':list(sections),'errors':[k for k in errors if k.startswith(cid+'/')],'outcome':reports.get(cid,{}).get('outcome')}),flush=True)
    after={p:shafile(p) for p in before};write(OUT/'RAW_EVIDENCE_AFTER_ANALYSIS.json',after)
    validation={'version':'A4 saved-data v1.0','batch_authority_sha256':BATCH_AUTH,'case_checks':checks,'errors':errors,'raw_files_checked':len(before),'original_raw_files_unchanged':before==after,'analysis_sources':{n:shafile(OUT/n) for n in files},'new_simulation_steps':0,'controller_command_computations':0,'physical_replays':0,'research_module_imports':[n for n in sys.modules if n.startswith(('loom_p','loom_commissioning'))],'scope':'Original receipt/byte/parent-constituent identity, input/delivery, native alignment, saved-state RNG invariance and ledger checks; no production validator command recomputation.'}
    assert not validation['research_module_imports'];write(OUT/'ANALYSIS_CHECKS.json',validation)
    summary={'batch_authority_sha256':BATCH_AUTH,'execution':batch,'cases':reports,'resources':resources,'analysis_errors':errors};write(OUT/'A4_RESULT_SUMMARY.json',summary)
    write(OUT/'RESOURCE_RESULT.json',{'cases':resources,'total_simulated_seconds':math.fsum(v['simulated_seconds'] for v in resources.values()),'total_native_steps':sum(v['native_steps'] for v in resources.values()),'total_recorder_wall_seconds':math.fsum(v['recorder_wall_seconds'] for v in resources.values()),'total_uncompressed_stream_bytes':sum(v['uncompressed_stream_bytes'] for v in resources.values()),'total_stored_trajectory_bytes':sum(v['stored_trajectory_bytes'] for v in resources.values()),'total_runner_wall_cap_seconds':2100,'read_only_reporting_cap_seconds':600,'combined_disk_cap_bytes':3000000000})
    def fmt(x):return 'not observed' if x is None else f'{x:.6f}'
    lines=[];detail=[]
    for cid in batch['case_order']:
        o=reports.get(cid)
        if not o or 'whole_case' not in o:
            lines.append(f'| {cid} | incomplete/unattempted | — | — | — | — | — |');detail.append(f'## {cid}\n\nNo complete observation report. Preserve the batch/analysis limitation: `{errors}`.\n');continue
        w=o['whole_case'];m=o['milestones'];ct=o['contacts'];out=o['outcome'];wait=o['waiting'];g=o['clearance']['native_derived_minimum_whole']
        lines.append(f"| {cid} | {fmt(m['entry_y_ge_9']['time'])} | {fmt(m['exit_y_gt_11']['time'])} | {fmt(m['arrival_radius_0_25']['time'])} | {w['expenditure']:.9f} | {w['final_EI'][0]:.9f} / {w['final_EI'][1]:.9f} | {ct['mover_contact_event_count']} |")
        stamps=[]
        for name,milestone in m.items():
            if milestone.get('observed'):
                move=milestone['mover'];stamps.append(f"| {name} | {milestone['time']:.9f} | {milestone['position']} | {move['centre'][0]:.9f} | {move['wrapped_phase_at_time']:.9f} | {milestone['E_I']} |")
        detail.append(f"""## {cid}

One independent external-control case stopped at {w['simulated_seconds']:.12g} s, {w['native_steps']} native steps, `{out['stop_status']}`, cause `{out['stop_cause']}`, complete `{out['complete']}`. Full prescribed physical witness observed: **{out['prescribed_physical_witness_observed']}**. Destination arrival: {out['destination_arrival']}; physical nonviability: {out['physical_nonviability']}; controller limitations: `{out['controller_limitations_observed']}`. The planned administrative cutoff remains separate from these physical observations.

| Milestone | Saved time (s) | Body centre | Mover centre x | Wrapped phase | E / I |
|---|---:|---|---:|---:|---|
"""+'\n'.join(stamps)+f"""

Milestones use the first matching native sample, with the preceding sample preserved in [{cid}/OBSERVATIONS.json]({cid}/OBSERVATIONS.json). They are not interpolated event times. Mover coordinates in this table are derived analytically at those saved times; original actual controller-sampled rectangles/velocities are preserved separately.

Minimum native-sampled body–mover clearance: **{g['signed_gap']:.9f} m at {g['time']:.9f} s**, body {g['body_position']}, mover {g['mover']['centre']}. The separate minimum using actual controller geometry samples is {o['clearance']['controller_actual_sample_minimum']['signed_gap']:.9f} m. The waiting and crossing-band minima, with their poses, are in the same observation record. These are sampled extrema, not a certified continuous-time minimum.

Actual mover contact events: **{ct['mover_contact_event_count']}**, impact events {ct['mover_impact_event_count']}, impact impulse sum {ct['mover_impact_impulse_sum']:.12g}, supported contact duration {ct['mover_positive_contact_duration']:.12g} s. All colliders: `{ct['counts_by_collider']}`. Total actual damage {w['damage']:.12g}; impact damage {w['impact_damage']:.12g}; sustained stress damage {w['sustained_stress_damage']:.12g}; repair {w['repair']:.12g}. Complete contact/boundary records remain available; no contact is inferred from proximity alone.

Waiting prescription {wait['prescribed_seconds']:g} s; recorded zero-command waiting support {wait['zero_command_supported_seconds']:.12g} s; maximum waiting displacement {wait['max_wait_position_displacement']:.12g} m. Waiting cost {wait['waiting_expenditure']:.12g}; post-wait/moving cost {wait['post_wait_or_moving_expenditure']:.12g}. Actual waiting/proceeding decisions and every waiting command are preserved. Any straddling cost allocation is explicitly listed ({len(wait['boundary_cost_allocations'])} here). No intermediate reserve values are invented.

Sampled path length through arrival {fmt(w['sampled_path_length_through_arrival'])} m; through final record {w['sampled_path_length_through_final']:.9f} m; nominal route {w['nominal_route_length']:g} m. Travel time to arrival {fmt(w['travel_time_to_arrival'])} s; time after prescribed release {fmt(w['travel_time_after_prescribed_release'])} s. Maximum lateral deviation {w['max_lateral_deviation']:.12g} m. Final destination distance {w['final_destination_distance']:.9f} m. Later band reentries: {len(o['route']['reentries_after_full_exit'])}; departures from arrival radius: {len(o['route']['destination_departures_after_arrival'])}. DETOUR corridor violations: {len(o['route']['detour_corridor_violating_native_indices'])}.

Starting E/I {w['start_EI']}; final E/I {w['final_EI']}; expenditure {w['expenditure']:.12g}; source transfer {w['source_transfer']:.12g}. All fixed 0.2 s windows are retained ({o['fixed_window_summary']['complete_0_2_windows']} complete, {o['fixed_window_summary']['partial_windows']} partial); net-E signs `{o['fixed_window_summary']['net_E_sign_counts']}`. Energy gain and useful learning are not pass gates.
""")
    all_witnessed=(len(reports)==3 and not errors and len(checks)==3
                   and all(len(v)==3 and all(section.get('valid') is True for section in v.values()) for v in checks.values())
                   and all(x.get('outcome',{}).get('prescribed_physical_witness_observed',False) for x in reports.values()))
    lead='All three predetermined bounded physical witnesses were observed.' if all_witnessed else 'The preserved case results below distinguish observed physical opportunities from incomplete or missed components.'
    table='| Case | Band entry (s) | Full exit (s) | Destination (s) | Expenditure | Final E / I | Mover contact events |\n|---|---:|---:|---:|---:|---|---:|\n'+'\n'.join(lines)
    plain=f"""# A4 commissioning result

{lead} The cases were executed once each under canonical batch `{BATCH_AUTH}`, in the declared order and with their original 16/28/32-second ceilings. The result describes the finite body and paired actuators under privileged external control. P was inactive; this is not a learning or perceptual test.

{table}

Entry and exit refer to the y=9 and y>11 body-centre markers. For DETOUR these are side-passage markers outside the mover region. Arrival is the predeclared 0.25 m radius. Times are native samples with bracketed precision, not exact interpolated crossing times.

WAIT uses the original fixed 12-second wait. Its immediate-proceed conflict remains the predeclared analytic argument; no counterfactual run was added. DETOUR uses the A0 left corridor with its independent endpoints, so this is not an equal-endpoint route-efficiency comparison. Read [the detailed report](A4_COMMISSIONING_REPORT.md) for waiting costs, path lengths, clearances, impulses, reserves, cutoffs and validation limits.

No retry, continuation, phase/route substitution, gain change, tuning, patch, new prehistory, additional case, live viewer or scientific run occurred. All native, sensor, contact/accounting, command, sampled mover and restart records are retained for passive replay. Actual outcome and analysis limitations are preserved separately in the detailed report. No inference of all-phase safety, P prediction/learning, efficacy, lifetime survival or global physical impossibility is made.
"""
    put(OUT/'A4_PLAIN_LANGUAGE_RESULT.md',plain)
    checktext=[]
    for cid,v in checks.items():
        ac=v.get('ACCOUNTING',{});bc=v.get('BOUNDARY_AND_DELIVERY',{});ri=v.get('RECORD_INTEGRITY',{})
        checktext.append(f"- {cid}: record/authority integrity {ri.get('valid')}; boundary/delivery {bc.get('valid')}; accounting {ac.get('valid')}, max residual {ac.get('maximum_residual')}; {bc.get('native_rows')} native rows, stage counts {bc.get('stage_decision_counts')}, neural wave rows {bc.get('neural_wave_rows')}.")
    technical=f"""# A4 technical commissioning report

{lead}

Authority `{BATCH_AUTH}`. P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; apparatus `5f07748102cb5eaa302569c87efbae095050e9fe`. Source request and derived constituent grants retain the genuine batch approval. Historical proposal labels in bound objects remain unchanged; the executed grant is separately recorded.

{table}

## Saved-data validation

"""+'\n'.join(checktext)+f"""

Analysis errors: `{errors}`. {len(before)} original raw/evidence files compared before and after analysis; byte-identical: **{before==after}**. No research modules imported, controller commands recomputed, world/field/neural steps or physical replays performed by analysis. This checks saved evidence, not unrecorded transient state or continuous-time convergence. Full original checks and per-window ledgers are retained under each case directory.

## Execution and limits

Run construction attempts: {batch['run_constructors_attempted']}. Unattempted cases: `{batch['unattempted_cases']}`. Attempted without completed result: `{batch['attempted_without_completed_result']}`. Batch failure: `{batch['failure']}`. Stop limitation: `{batch['batch_stop']}`. No opportunity to transfer unused duration/budget between cases was used.

The original runtime/cache/packet/prior evidence preservation check reports {batch['original_files_unchanged']}, clean Git state {batch['git_status_clean']}, exact checkpoint unchanged {batch['checkpoint_unchanged']}. No Git writes. Exact resource receipts are in `RESOURCE_RESULT.json`; recorder and reporting times are measurements, not new performance trials. Record fidelity was not reduced.

"""+'\n'.join(detail)+"""
## What was not tested

No alternate phase, route, initial state, reserve level, controller gain, retry, extension or additional A case. No live renderer, sensor-only controller, P neural processing, learning/perceptual test, efficacy tuning, scientific lifetime, cohort or all-phase safety test. No executed immediate-proceed comparator for WAIT and no shortest-path or optimal-energy test. Sampling does not certify a continuous-time minimum clearance or exact path arclength. A physical opportunity is bounded to the recorded conditions.
"""
    put(OUT/'A4_COMMISSIONING_REPORT.md',technical)
    elapsed=time.perf_counter()-start
    result={'batch_authority_sha256':BATCH_AUTH,'analysis_wall_seconds_including_reports':elapsed,'within_reporting_cap_before_packaging':elapsed<600,'completed_case_reports':list(reports),'errors':errors,'new_simulation_steps':0,'controller_command_computations':0,'physical_replays':0,'raw_files_unchanged':before==after,'all_three_physical_witnesses_observed':all_witnessed}
    write(OUT/'ANALYSIS_RESULT.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
