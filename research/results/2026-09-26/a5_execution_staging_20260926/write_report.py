"""Plain-language A5 report and static SVG plots from completed saved analysis."""
import csv,datetime,html,json,math,pathlib,shutil
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
BASE=ROOT/'worktrees/loom-p-clock-correction-20260926/developmental_ecology/artifacts/commissioning-A5-20260926-68db2c58'
OUT=BASE/'read-only-review'
def js(p):return json.loads(p.read_bytes())
def write(n,x):(OUT/n).write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')
def f(v):return 'unobserved' if v is None else format(v,'.9g')
def esc(v):return html.escape(str(v),quote=True)

def check(estimated):
    deadline=datetime.datetime.fromisoformat(js(BASE/'EXECUTION_RESULT.json')['first_stop_utc'])+datetime.timedelta(seconds=3600)
    assert datetime.datetime.now(datetime.timezone.utc)<deadline,'Reporting allowance exhausted'
    paths=map(pathlib.Path,js(OUT/'PREFLIGHT.json')['disk_accounting_roots'])
    total=sum(p.stat().st_size if p.is_file() else sum(q.stat().st_size for q in p.rglob('*') if q.is_file()) if p.exists() else 0 for p in paths)
    assert total+estimated<=10_000_000_000 and shutil.disk_usage(BASE).free>=estimated+1_000_000_000

def plots(rows,obs):
    colours=['#175e8d','#c74e2a','#508b54','#805bb6','#9c7029','#257c7e','#b65787','#5b6b7a']
    def text(x,y,v,size=13,fill='#253344'):
        return f'<text x="{x}" y="{y}" font-size="{size}" fill="{fill}">{esc(v)}</text>'
    def panel(x,y,w,h,title,series,ymax,marks=()):
        a=[text(x,y,title,17)];l=x+45;t=y+20;pw=w-65;ph=h-55
        for k in range(5):
            yy=t+ph-k*ph/4;a.append(f'<path d="M {l} {yy} h {pw}" stroke="#dce3e8" fill="none"/>');a.append(text(x,yy+4,f'{ymax*k/4:.2f}',10))
        for sec in (0,90,270,450,630):
            xx=l+pw*sec/630;a.append(text(xx-8,t+ph+19,str(sec),10))
        for sec in (90,120,270,300,450,480):
            xx=l+pw*sec/630;a.append(f'<path d="M {xx} {t} v {ph}" stroke="#adb8c1" stroke-dasharray="3 5"/>')
        for values,c in series:
            points=' '.join(f'{l+pw*r["time"]/630:.3f},{t+ph-ph*v/ymax:.3f}' for r,v in zip(rows,values))
            a.append(f'<polyline points="{points}" fill="none" stroke="{c}" stroke-width="1.5"/>')
        for sec,label in marks:
            xx=l+pw*sec/630
            a.append(f'<path d="M {xx} {t} v {ph}" stroke="#455966" stroke-width="0.8" stroke-dasharray="1 4"/>')
            a.append(text(xx+2,t+12,label,10))
        return '\n'.join(a)
    top=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="980" viewBox="0 0 1400 980">',
         '<rect width="1400" height="980" fill="#ffffff"/>','<g font-family="Arial,sans-serif">',
         text(40,40,'A5 — recorded stocks at all eight sources',26),
         text(40,67,'Every native row retained. Dashed: prescribed boundaries. F: first contact; D: actual departure release; R: macro-return.',13)]
    for j in range(8):
        first=obs['all_source_details'][j]['first_contact']
        marks=[(first['time'],'F')] if first else []
        marks += [(r['release']['time'],'D') for r in obs['macro_departures'] if r['source']==j and r.get('release')]
        marks += [(r['revisit_contact_start'],'R') for r in obs['all_macro_returns'] if r['source']==j]
        top.append(panel(35+(j%4)*342,105+(j//4)*280,330,245,f'Source {j}',[([r[f'stock_{j}'] for r in rows],colours[j])],.2,marks))
    top.append(panel(35,675,650,245,'Energy (blue) and integrity (orange)',[([r['E'] for r in rows],colours[0]),([r['I'] for r in rows],colours[1])],1.0))
    top.extend([text(755,710,'Contact / return markers',18)])
    for k,v in enumerate(obs['visits']):
        c=v.get('first_contact');ret=v.get('one_body_diameter_macro_return')
        top.append(text(755,742+k*37,f"Visit {v['visit']}, source {v['source']}: first contact {f(c['time']) if c else 'unobserved'} s",13))
        if ret:top.append(text(770,759+k*37,f"Macro-return start {f(ret['revisit_contact_start'])} s; away {f(ret['away_seconds'])} s",11))
    top.extend([text(40,962,'Static saved-data plot. No live renderer, world replay, command computation or feedback path.',12),'</g></svg>'])
    (OUT/'A5_ALL_SOURCE_STOCKS.svg').write_text('\n'.join(top),encoding='utf-8')

def main():
    check(100_000_000)
    assert not (OUT/'A5_PLAIN_LANGUAGE_RESULT.md').exists()
    result=js(BASE/'EXECUTION_RESULT.json');analysis=js(OUT/'ANALYSIS_RESULT.json')
    if not (OUT/'A5_OBSERVATIONS.json').exists():
        (OUT/'A5_PLAIN_LANGUAGE_RESULT.md').write_text('# A5 commissioning result — reporting limitation\n\nThe single authorized attempt stopped. Saved-data observations could not be completed; preserve EXECUTION_RESULT.json, ANALYSIS_RESULT.json and every error artifact. No retry, continuation or patch was performed. No renewal-witness conclusion is issued.\n',encoding='utf-8')
        return
    obs=js(OUT/'A5_OBSERVATIONS.json');s=js(OUT/'A5_FINAL_RESULT_SUMMARY.json');accounting=js(OUT/'ACCOUNTING.json')
    actual=js(OUT/'ACTUAL_CONTACT_BOUNDARY_AUDIT.json')
    verified=not analysis['errors'] and accounting['valid'] and js(OUT/'RECORD_INTEGRITY.json')['valid'] and js(OUT/'BOUNDARY_AND_DELIVERY.json')['valid']
    claim=s['complete_bounded_productive_recurrence_witness'] and verified and actual['complete_saved_data_validation']
    headline='Bounded productive renewed revisits observed' if claim else 'The complete bounded renewal witness was not established'
    lines=['# A5 commissioning result','',f'**{headline}.**','',
           f"One authorized attempt recorded **{s['native_steps']:,} native steps**, ending at physical time **{s['observed_simulated_time']!r} s** with status **{s['stop_label']}**. The prescribed ceiling was 630 nominal seconds. Stop cause: `{s['stop_cause']}`; terminal dimension: `{s['terminal_dimension']}`. No retry, continuation, route/stage change, tuning or patch occurred.",'',
           'This was a privileged external-controller physical witness. P was inactive. The scope is the observed body, actuators, route and source-renewal law; it is not a learning, perception, autonomous-policy, indefinite-viability or scientific-efficacy test.','',
           f"Starting E/I were {s['initial_EI']}; final E/I were {s['final_EI']}. Total intake was **{f(s['all_source_intake'])}**, expenditure **{f(s['expenditure'])}**, damage **{f(s['damage'])}** and repair **{f(s['repair'])}**. The sampled native body path length was **{f(s['sampled_native_path_length'])} m**.",'',
           '| Visit | Source | First contact (s) | Transfer | Source stock at window end | Window complete |',
           '|---|---:|---:|---:|---:|---|']
    for v in obs['visits']:
        c=v.get('first_contact')
        lines.append(f"| {v['visit']} | {v['source']} | {f(c['time']) if c else 'unobserved'} | {f(v.get('transfer'))} | {f(v.get('source_stock_end'))} | {v.get('complete_stage',False)} |")
    lines += ['', 'The windows remained fixed at 0–90, 90–120, 120–270, 270–300, 300–450, 450–480 and 480–630 s. Arrival and actual contact durations were measured separately. No useful-revisit outcome shortened the case.', '',
              '| Planned revisit | Actual away time (s) | Stock at departure → return | Measured away renewal | Return-window transfer | Away-restored uptake bound |',
              '|---|---:|---|---:|---:|---|']
    for v in obs['visits'][2:]:
        r=next((r for r in actual['returns'] if r['visit']==v['visit']),None)
        if r:lines.append(f"| Source {v['source']} | {f(r['away_seconds'])} | {f(r['stock_at_departure'])} → {f(r['stock_before_revisit'])} | {f(r['away_renewal'])} | {f(r['revisit_transfer'])} | {r['away_restored_uptake_interval']} |")
        else:lines.append(f"| Source {v['source']} | unobserved | — | — | — | No qualifying macro-return observed |")
    lines += ['', 'A macro-return requires a recorded departure and at least one native sample with a full body diameter of surface clearance before renewed positive-duration contact. The report preserves the preceding sample, contact/release events, every interruption and the away debit/renewal ledger. Timing brackets and the full fixed-window tables remain available in the JSON records.', '',
              'Boundary reconciliation: the initial support-gap helper flagged source 1 because a zero-duration recontact occurred after its last positive-duration support ended at 273.06999999989665 s. The packet explicitly requires the **final actual contact**, including such touches. That final contact and release occurred at **273.07356311601956 s**; its impulse and 1.3310128316840975e-09 damage are retained. The next contact began at 492.092241357054 s. Summing the unchanged intervening events gives **219.01867824103442 s** away, no interior contact, zero source debit, and the renewal shown above. No event was removed, interpolated, or moved. The original conservative false flag remains in `A5_OBSERVATIONS.json` / `A5_RESULT_SUMMARY.json`; `ACTUAL_CONTACT_BOUNDARY_AUDIT.json` documents every predicate and `A5_FINAL_RESULT_SUMMARY.json` contains the final interpretation.', '',
              'The source-1 departure therefore took about 3.074 s after the fixed 270-second target change. All release/recontact episodes, delays and damage are preserved. No stage was extended or substituted to obtain the returns.', '',
              '| Source | Initial → final stock | Renewal | Total debit / intake | Renewed-origin interval |',
              '|---|---|---:|---:|---|']
    for detail in obs['all_source_details']:
        r=detail['origin_accounting'];lines.append(f"| {r['source']} | {f(r['initial_stock'])} → {f(r['final_stock'])} | {f(r['renewal'])} | {f(r['debit'])} | {r['renewed_origin_interval']} |")
    lines += ['',f"Across all sources, initial-origin attribution lies in **{s['origin_attribution_totals']['initial_interval']}** and renewed-origin attribution in **{s['origin_attribution_totals']['renewed_interval']}**. The compelled renewed lower bound is {f(s['renewed_lower_fraction_of_cost'])} of recorded expenditure, or {f(s['renewed_lower_basal_equivalent_seconds'])} basal-cost-equivalent seconds.",'',
              f"Using the maximum admissible initial-origin contribution alone gives a recorded-accounting end balance of **{f(s['recorded_balance_using_upper_initial_origin_only'])}**. The renewed-supply lower bound needed to cover the recorded expenditure is **{f(s['renewed_supply_lower_bound_to_cover_recorded_expenditure'])}**. This is arithmetic over the actual expenditure/debits, not a no-renewal trajectory or proof about counterfactual survival. Availability, productive transfer, compelled renewal uptake and survival necessity remain distinct.",'',
              f"Validation complete: **{verified}**. Maximum per-event ledger residual: `{accounting['maximum_residual']!r}`. Whole energy residual: `{s['whole_energy_residual']!r}`; whole integrity residual: `{s['whole_integrity_residual']!r}`. Event-chain discontinuities: {len(accounting['event_chain_discontinuities'])}; native/event endpoint mismatches: {len(accounting['native_event_endpoint_mismatches'])}. Any errors remain in `ANALYSIS_RESULT.json`; no original evidence was corrected.",'',
              f"Actual mover contacts: **{len(obs['mover']['contact_events'])} event records**. Minimum body–mover clearance at the recorded controller samples: **{f(obs['mover']['minimum_sampled_gap'])} m**. This sampling fact is not a continuous all-phase clearance guarantee.",'',
              'Record integrity checks cover hashes, the genuine grant, initial/final state, native continuity, issued/delivered commands, native stage ownership, sensor alignment, ledgers, and inactive neural/RNG state at every checkpoint. They read saved records only. No `verify_segment(replay=False)`, world replay, live command recomputation, sensor resampling or new prehistory was invoked by reporting.', '',
              f"Actual process wall time including preflight: **{result['wall_seconds_including_preflight']/60:.2f} minutes**. See `RESOURCE_RESULT.json` for recorder time, stream/storage totals, monitor checks and the unchanged caps. The clean checkpoint remains `68db2c581f07200966d699a4f55a65f9b96df1e9`; authority remains `{s['authority_sha256']}`.",'',
              'The complete trajectory is retained regardless of the renewal-witness result. Static stock/E/I plots are in `A5_ALL_SOURCE_STOCKS.svg`; lossless native plotting values are in `ALL_NATIVE_PHYSICAL_RECORDS.csv`. Full event subdivisions, all eight stocks, source ledgers, commands, actual mover samples, sensors, diagnostics and restart histories remain in the original trajectory.', '',
              'Not tested: autonomous P learning/perception, an alternative route or phase, different parameters, no-renewal counterfactuals, additional cases, cohorts, scientific lifetimes, indefinite sustainability or efficacy tuning. No experiment number, scientific commissioning campaign, Git write, push, PR or merge was performed. Stop for Jason’s review.']
    (OUT/'A5_PLAIN_LANGUAGE_RESULT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    with (OUT/'ALL_NATIVE_PHYSICAL_RECORDS.csv').open(newline='',encoding='utf-8') as f0:
        rows=[{k:float(v) for k,v in r.items()} for r in csv.DictReader(f0)]
    plots(rows,obs)
    write('REPORT_DISPOSITION.json',dict(complete_saved_data_validation=verified,
        bounded_productive_recurrence_claim=claim,headline=headline,report_only_no_patch=True,
        final_interpretation_source='A5_FINAL_RESULT_SUMMARY.json',boundary_reconciliation='ACTUAL_CONTACT_BOUNDARY_AUDIT.json',
        initial_support_gap_flag_retained=obs['summary']['complete_bounded_productive_recurrence_witness'],
        zero_new_simulation_steps=True,zero_command_recomputation=True))
    shutil.copyfile(S/'write_report.py',OUT/'write_report.py')

if __name__=='__main__':main()
