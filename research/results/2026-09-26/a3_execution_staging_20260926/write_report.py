"""Write A3 reports from immutable result JSON only. Never imports Loom."""
import json,pathlib,shutil,time
S=pathlib.Path(__file__).resolve().parent
B=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\commissioning-A3-20260925-5f077481')
O=B/'read-only-review'
AUTH='43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd'
def js(p):return json.loads(p.read_bytes())
def fmt(v):return 'not observed / unavailable' if v is None else f'{v:.12g}' if isinstance(v,(float,int)) else str(v)
def write(name,s):
    with (O/name).open('x',encoding='utf-8') as f:f.write(s)
def milestone_row(name,m,side='EI_after'):
    if not m or not m.get('observed'):return f'| {name} | Not observed | — | — |'
    if 'release_event' in m:
        e=m['release_event']
        pair=[e['energy_after'],e['integrity_after']] if e else (m.get('sample_bracket') or {}).get('at_or_after',{}).get('reserves')
    else:pair=m.get(side) or m.get('EI')
    pair=pair or [None,None]
    return f'| {name} | {fmt(m.get("time"))} | {fmt(pair[0])} | {fmt(pair[1])} |'
def main():
    result=js(B/'EXECUTION_RESULT.json');analysis=js(O/'ANALYSIS_RESULT.json')
    receipt=js(B/'trajectory-001/manifest.json')
    obs=js(O/'A3_OBSERVATIONS.json') if (O/'A3_OBSERVATIONS.json').exists() else None
    sections={n:js(O/(n+'.json')) for n in ('RECORD_INTEGRITY','BOUNDARY_AND_DELIVERY','ACCOUNTING') if (O/(n+'.json')).exists()}
    good=not analysis['errors'] and len(sections)==3 and all(v.get('valid') is True for v in sections.values())
    lines=['# Single A3 commissioning result','',f'Executed authority: `{AUTH}`. One attempt; no retry, extension, route substitution, tuning, continuation or additional case.',
      '',f"Stopped at **{fmt(result['time'])} simulated seconds**, native index **{result['native_index']}**, `{receipt['status']}`, cause `{receipt.get('stop_cause')}`, complete `{receipt['complete']}`.",
      '',f"Saved-record validation: **{'checks passed within the stated scope' if good else 'INCOMPLETE or failed; dependent claims are qualified'}**. Analysis errors: `{analysis['errors']}`.",'']
    if obs:
        w=obs['whole_case'];ms=obs['milestones'];r=obs['repair'];en=obs['energy'];travel=obs['repair_to_energy_travel'];rcost=obs['repair_arrival_to_departure_or_stop']
        if w['complete_ordered_recovery_witness_observed']:
            story='The saved records contain the intended ordered physical chain: healthy start, real nonterminal mechanical injury, repair contact with positive restoration, departure and productive contact with source-3.'
        else:
            story='The complete ordered recovery chain was not observed in this one attempt. The component observations below remain separate; this does not establish that recovery is physically impossible.'
        lines += [story+('' if good else ' This reading remains qualified by the validation limitations above.'),'',
          f"Total actual integrity damage was **{fmt(w['damage'])}**; gross integrity restoration was **{fmt(w['repair'])}** ({w['repair_sign']}). Final **E={fmt(w['final_EI'][0])}, I={fmt(w['final_EI'][1])}**. Terminal dimension: `{w['terminal_dimension']}`.",'',
          '| Milestone | Recorded time (s) | Energy E | Integrity I |','|---|---:|---:|---:|']
        lines += [milestone_row('Healthy initial state',ms['initial_healthy']),milestone_row('Immediately before first real damage',ms['pre_damage'],'EI_before'),
          milestone_row('Immediately after first real damage',ms['post_damage']),milestone_row('Repair arrival, before contact-event accounting',ms['repair_arrival'],'EI_before'),
          milestone_row('Repair arrival, after contact-event accounting',ms['repair_arrival']),milestone_row('First eligible repair, event endpoint',ms['first_eligible_repair']),
          milestone_row('First positive restoration, event endpoint',ms['first_positive_restoration']),milestone_row('Actual repair departure',ms['repair_departure']),
          milestone_row('Energy arrival after repair departure, before contact accounting',ms['energy_arrival_after_repair_departure'],'EI_before'),
          milestone_row('Energy arrival after repair departure, after contact accounting',ms['energy_arrival_after_repair_departure']),milestone_row('Final stop',ms['final_stop'])]
        lines += ['', 'Times and reserves above use recorded events and their specified before/after sides. They are not interpolated or reset. The full JSON preserves both sides, impulses and stocks. If a departure has only sampled evidence, its bracket and limitation are retained.','',
          f"Repair-0 had **{fmt(r['positive_duration_contact_seconds'])} s** of positive-duration contact and **{fmt(r['eligible_duration'])} s** with resolved eligible quality. Actual sustained force range: `{r['sustained_force_range']}`; relative-speed range: `{r['relative_speed_range']}`; repair-quality range: `{r['quality_range']}`. The force target was 0.1; recorded force can overshoot. Exact I=1 was never required.",'',
          f"From first repair contact to actual departure (or stop if no departure), expenditure was **{fmt(rcost['expenditure'] if rcost else None)}**, intake **{fmt(rcost['gross_intake'] if rcost else None)}** and restoration **{fmt(rcost['repair'] if rcost else None)}**. Contact-supported expenditure alone was {fmt(obs['repair_supported_expenditure'])}; the full interval retains waiting/alignment costs.",'',
          f"Return travel lasted **{fmt(travel['duration'] if travel else None)} s**, with expenditure **{fmt(travel['expenditure'] if travel else None)}** and intake **{fmt(travel['gross_intake'] if travel else None)}**. Source-3 transferred **{fmt(en['source3_transfer_total'])}** in total; {en['positive_net_contact_window_count']} complete contact-containing windows had resolved positive net energy and {en['negative_net_contact_window_count']} had resolved negative net energy.",'',
          f"Whole-case intake was **{fmt(w['all_source_intake'])}**, expenditure **{fmt(w['expenditure'])}**, net E change **{fmt(w['net_E'])}**. Gross intake and net gain are distinct. No mid-case E/I, stock, field or clock reset occurred.",'',
          f"Recorded mover contact events: **{len(obs['mover']['certified_contacts'])}**. The original external records do not label mover light-ray hits; no perception inference or new ray tracing was performed.",'',
          f"Complete fixed 0.2-second windows: **{obs['complete_fixed_windows']}**; partial windows: **{obs['partial_fixed_windows']}**. Unobserved tail beyond the 1e-10 timing tolerance: **{fmt(w['unobserved_seconds_beyond_event_tolerance'])} s**.",'',
          'This is one externally controlled physical witness. P was inactive. It establishes no P learning, discovery, regulation, general recovery ability, autonomous survival or ecological sufficiency. An unsuccessful route, eligibility interval or reserve outcome is not automatically a controller defect or physical impossibility.']
    lines += ['',f"Actual recorder wall time: **{fmt(receipt['wall_seconds']/60)} minutes** against the 70-minute ceiling. Whole process including preflight: {fmt(result['wall_seconds_including_preflight'])} seconds. Uncompressed streams: {receipt['uncompressed_bytes']:,} bytes against 1,500,000,000. Read-only analysis: {fmt(analysis['analysis_wall_seconds'])} seconds. No new viewer or inspector was launched.",'',
      f"Code/cache/prior evidence/approved packet unchanged: `{result['original_runtime_cache_prior_evidence_and_packet_unchanged']}`. Git status clean: `{result['git_status_clean']}`; checkpoint unchanged: `{result['checkpoint_unchanged']}`. Raw evidence unchanged by analysis: `{analysis['original_raw_files_unchanged']}`.",'',
      'P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; apparatus remains `5f07748102cb5eaa302569c87efbae095050e9fe`. Worktree: `C:\\Users\\Jason\\Desktop\\Eridos\\Loom-p-apparatus-20260924-01a0c405`; branch `build/p-commissioning-apparatus-20260924-01a0c405`. No commit or Git write.','',
      'Not tested: any retry, alternative route or horizon; the manufactured low-E/I A3 arm; other commissioning cases; autonomous P learning or survival; new prehistory; parameter sweeps/tuning; full lifetimes; general physical infeasibility. Existing historical evidence and source files remain preserved.','',
      'The exact initial/approved/launched records, all native/contact/accounting/command/sensor evidence and checkpoints are retained. Future passive-viewer work can read them without a new run. No continuation is authorized. Stop at this review boundary.','']
    plain='\n'.join(lines)
    write('A3_PLAIN_LANGUAGE_RESULT.md',plain)
    technical=plain+'\n## Validation and audit records\n\n'
    for n in ('RECORD_INTEGRITY','BOUNDARY_AND_DELIVERY','ACCOUNTING'):
        v=sections.get(n)
        if v:
            stripped={k:x for k,x in v.items() if k not in ('rows','mapping')}
            technical+=f'### {n}\n\n```json\n'+json.dumps(stripped,indent=2)+'\n```\n\n'
        else:technical+=f'{n}: unavailable; see preserved analysis error.\n\n'
    if obs:
        technical+='## Stage accounting\n\n```json\n'+json.dumps(obs['stage_totals'],indent=2)+'\n```\n\n'
        technical+='## Repair operands and energy contact\n\n'
        technical+=f"Maximum repair-quality recomputation residual from saved operands: {obs['repair']['quality_saved_operand_max_residual']}. Maximum restoration-law residual from saved operands: {obs['repair']['repair_saved_operand_max_residual']}. No dynamic accounting function was called.\n\n"
        technical+='First positive-net source-3 window:\n\n```json\n'+json.dumps(obs['energy']['first_positive_net_window'],indent=2)+'\n```\n\n'
    technical+='Full data: `A3_OBSERVATIONS.json`, `A3_RESULT_SUMMARY.json`, `REPAIR_EVENT_LEDGER.json`, `ALL_FIXED_WINDOWS.json`, `ACCOUNTING.json`, `BOUNDARY_AND_DELIVERY.json`, `RECORD_INTEGRITY.json`, and `ANALYSIS_RESULT.json`. All observer milestones are downstream of the completed run. No controller commands were recomputed.\n\n'
    technical+='Timing follows the approved symmetric 1e-10 boundary convention; native indices define fixed windows. Historical A2 overflagged-boundary records and their note are unchanged. The packet’s original proposed/unauthorized labels describe preparation history; this new record contains the actual separate grant. Workbench navigation had registered A2 by execution time; the approved packet’s earlier navigation snapshot remains immutable.\n'
    write('A3_COMMISSIONING_REPORT.md',technical)
    shutil.copyfile(S/'write_report.py',O/'write_report.py')
    print(json.dumps({'reports_written':True,'record_checks_passed':good,'physical_chain':None if obs is None else obs['whole_case']['complete_ordered_recovery_witness_observed'],'world_steps_in_reporting':0}))
if __name__=='__main__':main()
