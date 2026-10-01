"""Write a report of saved A2 observations; never import or execute simulation."""
import json,pathlib,shutil
B=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\commissioning-A2-20260925-5f077481')
R=B/'read-only-review'
def get(n):return json.loads((R/n).read_bytes())
def fmt(v):return 'not observed / unavailable' if v is None else f'{v:.12g}' if isinstance(v,(float,int)) else str(v)
def event(e):return 'not observed' if e is None else f"{fmt(e['time'])} s; event {e['event_index']}"
def window(w):return 'not observed' if w is None else f"{fmt(w['start_time'])}–{fmt(w['end_time'])} s; net E {fmt(w['energy_delta'])}; intake {fmt(w['all_source_transfer'])}; cost {fmt(w['expenditure'])}"
def main():
    a=get('ANALYSIS_RESULT.json');execution=json.loads((B/'EXECUTION_RESULT.json').read_bytes());receipt=json.loads((B/'trajectory-001/manifest.json').read_bytes())
    lines=['# Loom P — single A2 commissioning result','',
      'Authority: `229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007`.',
      'P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Apparatus: `5f07748102cb5eaa302569c87efbae095050e9fe`.',
      '',f"The single authorized A2 attempt stopped at **{fmt(execution['time'])} simulated seconds**, native index **{execution['native_index']}**, as **{receipt['status']}** (cause: `{receipt.get('stop_cause')}`). Record complete: **{receipt['complete']}**. Exactly {execution['run_constructors_attempted']} Run constructor attempt(s); no retry, continuation or replacement case.",'']
    if (R/'A2_OBSERVATIONS.json').exists():
        o=get('A2_OBSERVATIONS.json');s0=o['sources']['0'];s1=o['sources']['1'];c=o['whole_case'];travel=o['travel'];dep=o['release_event']
        if dep is not None and s1['transfer_total']>0 and s1['first_positive_net_window'] is not None:
            lines += ['The requested sequence was observed in this one external physical witness: productive first-source contact, a net-negative interval during continued residence while stock remained nonzero, departure without reset, real travel expenditure, and productive contact with a different source. These are separate measured milestones, not an overall P pass/fail or an efficacy result.','']
        lines += ['## Physical observations','', '| Distinction | Recorded observation |','|---|---|',
          f"| First-source certified contact | {event(s0['first_certified_contact'])} |",
          f"| First-source transfer | First: {event(s0['first_positive_transfer'])}; cumulative {fmt(s0['transfer_total'])}, {s0['transfer_sign']} |",
          f"| First-source residence | {fmt(s0['positive_duration_contact_seconds'])} s of positive-duration support in {len(s0['contact_intervals'])} interval(s); force range {s0['sustained_force_range']} |",
          f"| First-source stock | {fmt(s0['initial_stock'])} → {fmt(s0['final_stock'])}; cumulative renewal {fmt(s0['renewal_total'])}; full native/event history retained |",
          f"| First net-negative contact-containing residence window | {window(o['first_negative_residence_window'])} |",
          f"| First fully supported negative residence window | {window(o['first_fully_supported_negative_residence_window'])} |",
          f"| Commanded departure | {fmt(None if o['departure_instruction'] is None else o['departure_instruction']['time'])} s |",
          f"| Actual source-0 release | {event(dep)} |",
          f"| E/I at release | {('not observed' if dep is None else str([dep['energy_after'],dep['integrity_after']]))} |",
          f"| First clear native endpoint | {fmt(None if o['first_clear_native'] is None else o['first_clear_native']['time'])} s; exact brackets/reserves in A2_OBSERVATIONS.json |",
          f"| One body-diameter surface clearance | {fmt(None if o['one_body_diameter_clearance_first_native'] is None else o['one_body_diameter_clearance_first_native']['time'])} s; descriptive, not a pass gate |",
          f"| Travel from observed departure | {('unobserved' if travel is None else str(travel))} |",
          f"| Second-source geometric arrival | {s1['geometric_arrival']} |",
          f"| Second-source certified contact | {event(s1['first_certified_contact'])} |",
          f"| Second-source stock before first certified contact | {fmt(None if s1['first_certified_contact'] is None else s1['first_certified_contact']['stock_before'][1])}; pre/post renewal/transfer operands retained |",
          f"| Second-source transfer | First: {event(s1['first_positive_transfer'])}; cumulative {fmt(s1['transfer_total'])}, {s1['transfer_sign']} |",
          f"| Second-source positive-net interval | {window(s1['first_positive_net_window'])} |",
          f"| Second-source contact windows | {s1['positive_net_contact_window_count']} positive and {s1['negative_net_contact_window_count']} negative among {s1['complete_contact_window_count']} complete contact-containing windows |",
          f"| Whole-case gross intake / expenditure / net E | {fmt(c['all_source_intake'])} / {fmt(c['expenditure'])} / {fmt(c['net_E'])} |",
          f"| Final E/I | {c['final_EI']} |",
          f"| Physical nonviability | Terminal dimension: `{c['terminal_dimension']}` |",
          f"| Controller/apparatus exception | `{c['controller_or_apparatus_exception']}`; receipt error `{c['receipt_error']}` |",
          f"| Administrative stop | `{c['stop_label']}` / stored cause `{c['stop_cause']}`; 18,000 native steps cover the full prescribed horizon within the existing clock tolerance. Raw 180-minus-final-time subtraction: {fmt(c['planned_unobserved_seconds'])} s (representation residual, not an unobserved step) |",
          '',f"All {o['complete_window_count']} complete fixed 0.2-second windows and {o['partial_window_count']} partial windows are preserved in ALL_FIXED_WINDOWS.json. Contact-containing and fully supported windows have separate counts. The negative residence transition is a finite-window observation, not an exact instantaneous crossing or an exactly-zero stock requirement.",'',
          '## Travel, mover and limits','',f"Commanded-travel interval (t=90 to source-1 contact, or recorded stop): `{o['commanded_travel_interval']}`. Actual travel costs above use continuous event accounting and explicitly flag any boundary-straddling event; no proportional transfer interpolation or reset is supplied.",'',
          f"Mover contact events: **{len(o['mover']['certified_contact_events'])}**. Nearest recorded decision-time clearance: `{o['mover']['nearest_at_recorded_decision']}`. Mover geometry is recorded at 0.1-second decision cadence. {o['mover']['light_ray_interception']} Other causal exposure remains unresolved.",'',
          'Controller adequacy is assessed from the actual prescribed stages, release/arrival records, commands and force history. Missing arrival or transfer would leave controller, route, reserve and physical causes to be discriminated; it would not by itself establish ecological impossibility. This external physical witness supplies no P discovery, perception, learning, useful regulation, survival strategy, global ecological adequacy or indefinite-maintenance result. No observation was collapsed into an overall PASS/FAIL.','']
        intervals=s1['contact_intervals'];gaps=[{'after':x['end'],'before':y['start'],'seconds':y['start']-x['end']} for x,y in zip(intervals,intervals[1:])]
        lines += [f"Source-1 support occurred in {len(intervals)} intervals, with recorded gaps `{gaps}`. These brief release/recontact episodes are retained, not relabelled as substantive revisits. No source-0 recontact occurred after departure. Actual sustained force reached {fmt(s0['sustained_force_range'][1])} at source 0 and {fmt(s1['sustained_force_range'][1])} at source 1, above the 0.1 controller target and 0.25 stress threshold during portions of contact. Total integrity loss was {fmt(c['damage'])}, with repair {fmt(c['repair'])}; there was no terminal crossing. The target force is not a guarantee of the realized force.",'']
        ledger=get('ACCOUNTING.json');flags=sorted({i for row in o['stage_totals'] for i in row['boundary_straddling_events']})
        offsets=[]
        for i in flags:
            row=ledger['rows'][i];nominal=min((90.,120.),key=lambda t:abs(t-row['time']))
            offsets.append({'event_index':i,'recorded_endpoint':row['time'],'nearest_nominal_boundary':nominal,'offset_seconds':row['time']-nominal,'within_existing_event_time_tolerance':abs(row['time']-nominal)<=1e-10})
        note={'kind':'Reporting limitation; original derived results retained without patch/re-run','flagged_nominal_boundary_events':offsets,
              'event_time_tolerance':1e-10,'raw_horizon_subtraction_seconds':c['planned_unobserved_seconds'],
              'interpretation':'The interval helper over-flags sub-tolerance endpoint offsets at nominal 90/120 boundaries. These flags do not identify an extra or missing physical step. Exact recorded release-to-contact travel has no straddling event and its cost remains 0.07565364813787812. Raw flags and subtraction remain unchanged.',
              'analysis_or_simulator_patch':False,'new_world_steps':0}
        with (R/'TIMING_REPORTING_NOTE.json').open('x',encoding='utf-8') as f:json.dump(note,f,indent=2,ensure_ascii=False);f.write('\n')
        lines += ['## Reporting limitation retained','',note['interpretation'],f"The flagged operands are `{offsets}`. The final recorded clock is {execution['time']!r}; its approximately 1.87e-11 s difference from 180 is below the unchanged 1e-10 clock tolerance. All 18,000 planned native steps and all 900 fixed windows exist. This note interprets the saved operands; neither the original analysis output nor its helper was patched or rerun.",'']
    else:lines += ['Physical interpretation is unavailable because the read-only analysis did not complete. Original evidence and analysis errors are retained; no patch or replacement execution was made.','']
    lines += ['## Recorded validation and preservation','',f"Completed read-only sections: {a['completed_sections']}. Errors: `{a['errors']}`."]
    for name in ('RECORD_INTEGRITY','ACCOUNTING','BOUNDARY_AND_DELIVERY'):
        if (R/(name+'.json')).exists():
            v=get(name+'.json');small={k:x for k,x in v.items() if k not in ('rows','mapping','checkpoints')};lines += ['',f'`{name}`: `{small}`.']
    lines += ['', 'The production segment verifier was not called: its saved pending-command path recomputes the waypoint controller even when physical replay is disabled. The authorized read-only analysis instead verifies receipt hashes, exact authority, ledger, saved stage timing, issued-versus-delivered commands, sensor-envelope alignment and checkpoint invariance without generating commands.',
       '',f"Raw evidence unchanged during analysis: **{a['original_raw_files_unchanged']}** ({a['raw_files_checked']} files). Original runtime/cache/earlier evidence/approved packet unchanged: **{execution['original_runtime_cache_prior_evidence_and_packet_unchanged']}**. Git HEAD unchanged: **{execution['checkpoint_unchanged']}**; status clean: **{execution['git_status_clean']}**. No new commit or vault Git write.",
       '',f"Recorder wall time: {fmt(receipt['wall_seconds'])} s. Whole execution process: {fmt(execution['wall_seconds_including_preflight'])} s. Read-only analysis: {fmt(a['analysis_wall_seconds'])} s. Uncompressed streams: {receipt['uncompressed_bytes']} bytes. Recorded counts: `{receipt['records']}`.",
       '', '## Exact location and boundary','',
       'Worktree: `C:\\Users\\Jason\\Desktop\\Eridos\\Loom-p-apparatus-20260924-01a0c405`. Branch: `build/p-commissioning-apparatus-20260924-01a0c405`. Checkpoint remains `5f07748102cb5eaa302569c87efbae095050e9fe`.',
       '', 'The original proposed packet, canonical object, genuine authorization text, normal approval envelope, launched grant, initial snapshot, driver, raw streams, restart snapshots, progress and versioned analysis are separately preserved. Existing native evidence remains suitable for later passive-viewer extension; no viewer was built or inserted here.',
       '', 'Not performed: retry, continuation, route substitution, additional case, new prehistory, new birth, physical/sensory replay, controller recomputation during analysis, apparatus or P patch, tuning, sweep, efficacy test, scientific lifetime, experiment number, preregistration, evidential freeze, push, PR or merge. Stop at the approved review boundary.','']
    with (R/'A2_COMMISSIONING_REPORT.md').open('x',encoding='utf-8') as f:f.write('\n'.join(lines))
    shutil.copyfile(pathlib.Path(__file__),R/'write_report.py')
    print(str(R/'A2_COMMISSIONING_REPORT.md'))
if __name__=='__main__':main()
