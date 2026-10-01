"""Write review tables from sealed passive results; no world execution."""
from pathlib import Path
import json,csv,math
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent;PREP=ROOT/'motor_commissioning_preparation_20260930_v0_2';EX=PREP/'execution'
read=lambda p:json.loads(Path(p).read_bytes())
rows=read(OUT/'PASSIVE_RESULTS.json');den=read(EX/'DENOMINATOR.json');valid=read(OUT/'PASSIVE_VALIDATION.json')
resource=read(OUT/'RESOURCE_ACTUALS.json');seal=read(OUT/'EXECUTION_CUSTODY_SEAL.json');matrix=read(PREP/'MATRIX.json')['cases']
assert len(rows)==9 and all(r['status']=='COMPLETE_90_SECONDS' for r in rows) and den['stop'] is None
def fmt(x,n=3):return '—' if x is None else f'{x:.{n}f}'
def short(r):return r['case_id'].replace('MC-','')
def table(head,rows):return '\n'.join(['| '+' | '.join(head)+' |','| '+' | '.join(['---']*len(head))+' |']+['| '+' | '.join(map(str,r))+' |' for r in rows])
parts=[]
def add(text):parts.append(text.strip())
add('''# MOTOR_COMMISSIONING_RESULT_v0_2

All nine fresh, independently initialized cases completed once, in the authorized order, at 90 seconds / 9000 native steps. No apparatus failure, biological terminal stop, administrative cutoff, retry or continuation occurred. The complete denominator is retained. Execution is finished.

The FS-001 M1 observation replicated exactly: similar path length and effort to CURRENT, substantially greater reach and lower recurrence. Across these three fixed starts, M1 showed longer velocity-direction persistence and fewer forward/reverse switches, without greater aggregate effort or any contact. M2 showed variable realized drive and exposure across starts; its large FS-001 reach includes strong mover interaction and damage. These are bounded descriptions of these draws and starts, not a motor-selection rule or developmental-efficacy result. CURRENT remains the reference. No candidate is selected.

This is a new common-apparatus screen. `MOTOR_COMMISSIONING_RESULT_v0_1` remains unchanged historical interrupted evidence. It is neither overwritten nor treated as a continuation of this result.''')
add('''## Identity and authority

Corrected apparatus checkpoint: `1d7cd6fd450ea528562b2c825589ab4de18a5b38`.

Runtime identity: `5df0ced8bf5602c84852bc2074fca8d422cc39cc55b9bab00a4b653bbe714c49`.

Local branch: `build/p-contact-release-20260930`.

Worktree: `C:\\Users\\Jason\\.codex\\.chatgpt-projects\\g-p-6a6fb425222c8191a814fdc0f7d89f97\\worktrees\\loom-contact-release-20260930`.

Historical P baseline: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. The corrected body/P package digest is `98bbf9053ca55ef545c6fc868e54c85342149d143319281a47f9a1fd71c28c7d`, distinct from the old `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`. This reflects the already-reviewed contact-event correction, not a change to P neural learning. The common corrected apparatus was used for all nine cases. No production code changed in this execution task.

Configuration identity: `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`. The prepared motor parameter object, stochastic laws, matched FS-001/002/003 states, ordinary birth law, source laws, viability and geometry remained fixed. No new field prehistory was generated.

The frozen preparation still says `PROPOSED_UNAUTHORIZED`: its bytes were deliberately preserved. Jason's subsequent authorization is separately recorded in `execution/JASON_AUTHORIZATION.json` and the single-use start record. This report creates no new authority.''')
add(table(['Order','Case','Authorized SHA-256','Disposition'],[[i+1,r['case_id'],f"`{r['authority_sha256']}`",'9000 / 90 s complete'] for i,r in enumerate(matrix)]))
add(f'''## Execution, evidence and resources

The full runtime/source/authority/state preflight passed before the batch and was repeated immediately before each case by the unchanged executor. `execution/PREFLIGHT.json` records the batch gate; per-case start/stop/verification records and the executor source establish the subsequent gates. The gate checked the exact runtime, authority order, all prepared snapshots, original fixtures and prehistory, matched initial state except the declared spontaneous process, fixed bounds and absence of retry/continuation permission. There was no outcome-dependent decision between cases.

All {valid['total_native_rows']:,} native rows, {sum(x['waves'] for x in valid['checks']):,} wave records and {sum(x['events'] for x in valid['checks']):,} event/ledger rows were preserved and passively checked. Every case has its initial, 6000-step periodic and 9000-step final checkpoint, 90 native chunks, a closed receipt and a read-only verification result. The complete {len(seal['files'])}-file execution tree was hashed before analysis. Native time, endpoint body/reserves, wave indices, event counts, expenditure, transfer/stock and damage/repair ledgers reconcile. Largest per-event accounting residual: {max(x['ledger_max_error'] for x in valid['checks']):.4g}; allowed arithmetic tolerance is 1e-12.

The nominal ceiling is index-derived 90 seconds. The recorded accumulated float clock is 90.00000000000914 seconds for each case (about 9.14e-12 s roundoff); no additional native step occurred.

Active execution took {den['active_wall_seconds']:.3f} s against 2700 s; preflight {den['preflight_wall_seconds']:.3f} s against 300 s; store verification {den['verification_wall_seconds']:.3f} s against 600 s. Execution evidence occupies {resource['execution_total_bytes']:,} bytes ({resource['execution_total_bytes']/1e6:.2f} decimal MB), including shared assets and batch metadata. All individual cases were below the unchanged 300 s and 32 MB bounds. The 16 MB closure reserve was retained; no fidelity or cadence was reduced. Passive decoding/metrics took {valid['observer_seconds']:.3f} s. Archive/reporting had a separate 300 s planning reserve, not a simulated-time allowance or a permission for more cases.

The host emitted a read warning about its global Git ignore file. All required source/status/runtime checks succeeded; no workaround, patch or Git write was made.''')
add(table(['Case','Active wall s','Case evidence bytes'],[[short(r),fmt(s['wall_seconds']),s['stored_bytes']] for r,s in zip(rows,resource['cases'])]))
add('''## Movement and spatial exposure

Distances are world units. Path is the complete native body-centre polyline, including externally induced motion. Excursion is the maximum distance from the original birth position; final displacement is reported separately. Coverage counts body-centre bins, not traversable area or swept body volume. Revisit fraction counts transitions into an already visited bin after leaving it; it is not a fraction of time spent stationary. No outcome-based threshold or normalization was applied.''')
add(table(['Case','Path','Max excursion','Final displacement','Displacement/path','0.25 cells','Revisit fraction'],[[short(r),fmt((k:=r['kinematics'])['path_length']),fmt(k['maximum_excursion']),fmt(k['displacement']),fmt(k['displacement_path_ratio']),k['grids']['025']['visited_cells'],fmt(k['grids']['025']['reentry_fraction'])] for r in rows]))
add('![Recorded paths for the nine matched cases](NINE_CASE_PATHS.png)')
add('''Grid sensitivity is retained rather than selecting the most favorable placement. The half-cell offset adds 0.125 to both coordinates before binning. The one-unit grid can have very few transitions, so its revisit fractions are coarse.''')
add(table(['Case','0.25 cells / returns / transitions','Half-offset cells / revisit','1-unit cells / revisit'],[[short(r),f"{(g:=r['kinematics']['grids'])['025']['visited_cells']} / {g['025']['previously_visited_reentries']} / {g['025']['cell_transitions']}",f"{g['025_offset']['visited_cells']} / {fmt(g['025_offset']['reentry_fraction'])}",f"{g['100']['visited_cells']} / {fmt(g['100']['reentry_fraction'])}"] for r in rows]))
add('''Coverage and excursion growth at the fixed ages follow. The complete companion CSV also contains path, final displacement and offset/one-unit coverage at these ages.''')
add(table(['Case','Age s','Path','Max excursion','Displacement','0.25 / 1-unit cells'],[[short(r),fmt(a['age_seconds'],0),fmt(a['path_length']),fmt(a['maximum_excursion']),fmt(a['displacement']),f"{a['coverage025']} / {a['coverage100']}"] for r in rows for a in r['kinematics']['ages']]))
add('![Maximum excursion and coverage growth](REACH_AND_COVERAGE.png)')
add('''## Bouts, direction persistence and body heading

Forward/reverse means signed velocity in the actual body frame, with thresholds +0.01 / −0.01 units/s. Qualifying bouts last at least 0.1 s. Counts and medians below include a final right-censored bout where present. Switches count changes of sign between qualifying bouts, including low-speed gaps. The full JSON retains every bout and the prescribed 0.005 / 0.02 threshold sensitivity. A heading can remain similar while velocity reverses; heading and travel-direction correlations are therefore separate.''')
add(table(['Case','Forward count / median s','Reverse count / median s','Switches','Mean speed','Mean abs angular speed rad/s','Abs / net heading degrees'],[[short(r),f"{((b:=(k:=r['kinematics'])['bouts']['0.01'])['forward_qualifying_summary'] or {}).get('count',0)} / {fmt((b['forward_qualifying_summary'] or {}).get('median'))}",f"{(b['reverse_qualifying_summary'] or {}).get('count',0)} / {fmt((b['reverse_qualifying_summary'] or {}).get('median'))}",b['switches'],fmt(k['mean_speed'],4),fmt(k['mean_abs_angular_speed'],4),f"{fmt(k['heading_total_absolute_rotation_degrees'],1)} / {fmt(k['heading_net_change_degrees'],1)}"] for r in rows]))
add(table(['Case','Direction correlation 2 / 4 / 8 s','Valid pairs 2 / 4 / 8 s','Heading correlation 2 / 4 / 8 s','Rotating / translating / inactive fraction'],[[short(r),' / '.join(fmt(p['direction_correlation']) for p in r['kinematics']['persistence'][3:6]),' / '.join(str(p['valid_direction_pairs']) for p in r['kinematics']['persistence'][3:6]),' / '.join(fmt(p['heading_correlation']) for p in r['kinematics']['persistence'][3:6]),' / '.join(fmt(r['kinematics'][s]) for s in ['predominantly_rotating_fraction','predominantly_translating_fraction','inactive_fraction'])] for r in rows]))
add('''Direction correlations use unit world-velocity vectors on the fixed 0.1 s sampling grid, with both speeds >0.01. All prescribed lags (0.1, 0.5, 1, 2, 4, 8, 16 s), pair counts and heading correlations are in each case's DETAILS JSON. No fitted persistence time or diffusion coefficient is inferred. Inactivity means both speed and radius × |angular speed| ≤0.005. Predominantly rotating means rotational edge speed >2× translation speed; predominantly translating uses the reverse inequality. These categories leave mixed activity unclassified and do not sum to one.

CURRENT's 4 s direction correlation was negative in all three starts (about −0.79 to −0.73), despite strong heading correlation: recurrent forward/backward motion is visible. M1's 4 s direction correlation was positive in all three (about 0.64 to 0.76) with four switches each; M2 had five to eight switches and positive but more variable 4 s direction correlation. This describes changed temporal organization in these realizations; it does not establish general superiority.''')
add('''## Command organization, cost and susceptibility

Common command is (left+right)/2; differential command is (right−left)/2. These are actual actuator commands. The spontaneous term is measured separately from the saved 0.2 s wave diagnostics. RMS and left/right correlation do not on their own explain spatial reach.''')
add(table(['Case','Common mean / RMS','Differential mean / RMS','L/R correlation','Opposed fraction','Spontaneous RMS'],[[short(r),f"{fmt((k:=r['kinematics'])['common_command_mean'],4)} / {fmt(k['common_command_rms'],4)}",f"{fmt(k['differential_command_mean'],4)} / {fmt(k['differential_command_rms'],4)}",fmt(k['left_right_correlation']),fmt(k['opposed_command_fraction']),fmt(r['coupling']['oscillator']['rms'],4)] for r in rows]))
add('''All cases began at E=0.7 and I=1.0. Total expenditure is the exact event-ledger sum; basal expenditure is 0.135 per case. Effort is the unchanged integral of mean absolute paired command times 0.001. Damage and transfer remain visible, rather than being folded into an efficiency score.''')
add(table(['Case','Effort','Total expenditure','Impulse','Damage','Source transfer','Repair','Final E / I'],[[short(r),fmt((p:=r['physical'])['effort_expenditure'],6),fmt(p['expenditure'],6),fmt(p['total_impulse'],6),fmt(p['damage'],6),fmt(p['source_transfer'],6),fmt(p['repair'],6),f"{fmt(p['final_reserves'][0],6)} / {fmt(p['final_reserves'][1],6)}"] for r in rows]))
add(table(['Case','Direct feedback RMS','Associative evoked RMS','Current RMS','Attenuation min–max','Minimum local gain'],[[short(r),fmt((c:=r['coupling'])['direct']['rms'],6),f"{c['evoked']['rms']:.3g}",fmt(c['current']['rms'],6),f"{fmt(c['attenuation']['distribution']['minimum'])}–{fmt(c['attenuation']['distribution']['maximum'])}",fmt(c['gain_before_relaxation']['distribution']['minimum'],6)] for r in rows]))
add('''At all 4050 recorded waves, target=tanh(spontaneous+direct feedback+associative evoked+current) was checked against its stored value, and the stored achieved command matched the native row. The local additive-input gain before motor relaxation is (1−attenuation)×sech²(total input); its minimum across all cases was 0.692434. The immediate next-native gain adds the factor 1−exp(−0.1), giving a minimum about 0.0659. No recorded wave had tanh gain below 0.1 or attenuation above 0.95. These measurements show no saturation/attenuation blockage of ordinary additive feedback or regulatory current in the sampled operating range. Attenuation remained about 0.187–0.214.

The actual associative evoked contribution was tiny (roughly 1e−7 RMS), while direct feedback and current were nonzero. Preserved susceptibility is not proof that learning supplied useful control, nor a causal attribution from a perturbation experiment. No extra world perturbations or candidate component runs were performed here.''')
add('''## Contact, impulse, damage and descriptive interactions

Only two cases had recorded contact. FS-001/M2 contacted the mover; FS-003/M2 contacted `source-6`. All seven other cases had zero recorded contact, impulse, damage, transfer and repair. There was no wall, restorative-surface or other-body contact in any case. Contact transaction counts are solver ledger entries, not independent collisions. First-to-last contact is an envelope that can contain gaps; total contact duration excludes those gaps.''')
add(table(['Case / collider','First / last time s','Contact duration s','Impact / sustained impulse','Total damage','Peak impact impulse / sustained force'],[[short(r)+' / '+kind,f"{fmt(p['first_contact_time'],6)} / {fmt(p['last_contact_time'],6)}",fmt(p['contact_duration_s'],6),f"{fmt(p['impact_impulse'],6)} / {fmt(p['sustained_impulse'],6)}",fmt(p['damage'],6),f"{fmt(p['peak_instantaneous_impulse'],6)} / {fmt(p['peak_sustained_force'],6)}"] for r in rows for kind,p in r['physical']['categories'].items() if p['contact_records']]))
add('''FS-003/M2 transferred 0.0194224208259 energy from a source and incurred 0.00147708692316 damage. This interaction is recorded descriptively only and has no role in preference, parameter choice or selection. No repair occurred.

FS-001/M2's movement is materially confounded by mover interaction: in the 21.5–28 s renewal interval alone it traversed 2.264398 units, with 1.944421 impulse and 0.030978 damage. Its velocity spike during this interval is visible in the renewal figure. Recorded path includes externally induced displacement and subsequent motion; no counterfactual decomposition of autonomous versus mover-induced reach is available. Its large 90 s reach must not be called an unqualified exploration improvement.''')
add('''## FS-001 M1 replication and the other matched starts

Every native physical field of FS-001/CURRENT and FS-001/M1 is bit-identical to the corresponding complete 9000-row v0.1 record. FS-001/M2 matches all 1025 available historical native rows exactly; the new run proceeded independently from the prepared birth snapshot and did not resume that historical checkpoint. `HISTORICAL_NATIVE_COMPARISON.json` records this read-only comparison. The prior correction review separately contains the earlier engineering checkpoint/event/trajectory regression; it was not rerun here.

For FS-001, M1 path was 4.034823 versus CURRENT 4.106441 (−1.74%); effort 0.01179509 versus 0.01181584 (−0.18%). Maximum excursion was 1.058527 versus 0.400002 (2.646×); 0.25-cell revisit fraction 0.142857 versus 0.833333. Final displacement was 1.003345 versus 0.158675. Neither case contacted anything. This is the requested replication, with the qualification that repeated deterministic starts are not new independent statistical replication. M1 also accumulated more absolute body rotation (623° versus 476°), and its first 10 s did not already show the final reach advantage.

FS-002: M1 had 15.3% more path and 0.90% less effort than CURRENT, with max excursion 2.1593 versus 0.3757 and lower recurrence. M2 had 37.8% more path and 13.0% less effort, max excursion 1.8048, with recurrence between CURRENT and M1. None contacted a fixture.

FS-003: M1 had 56.2% more path and 10.7% less effort than CURRENT, max excursion 3.3822 versus 0.5997, and much less recurrence. M2 had only 1.27% more path and 18.8% less effort, max excursion 1.0358 but final displacement 0.2998 and substantially more recurrence than M1. Its late source contact/transfer is not a reason to prefer it. The three matched comparisons are retained without pooling away this variability.''')
add('''## M2: initial draw versus renewal and temporal organization

The initial common/differential latent equals the first target. Spontaneous left/right drive is 0.35×tanh(common∓differential). Initial targets and duration draws were exactly those prepared before v0.1, not redrawn after outcomes. At tick k equal to the stored renewal index, the next target is selected for native k+1; that step still emits the previous latent's drive, then follows the new target with the fixed 1 s time constant. The first changed spontaneous signal is at native k+2. Renewal dates below are nominal absolute ages, not newly simulated quantities.''')
add(table(['Start','Initial common / differential','Initial left / right drive','Pair RMS','First renewal s','Renewals observed','Whole-run spontaneous RMS'],[[short(r).replace('-M2',''),f"{fmt((m:=r['M2_renewal_analysis'])['initial_common_latent'],6)} / {fmt(m['initial_differential_latent'],6)}",' / '.join(fmt(x,6) for x in m['initial_spontaneous_pair']),fmt(m['initial_spontaneous_pair_rms'],6),fmt(m['first_target_renewal_time_s'],1),len(m['renewals']),fmt(r['coupling']['oscillator']['rms'],6)] for r in rows if r['process']=='M2']))
add('''FS-001's initial pair RMS 0.3044 is substantially larger than FS-002's 0.1633 and FS-003's 0.1443. In the common first 10 s, FS-001/M2 expended about 1.69× CURRENT's effort. Its early reach is therefore not a pure temporal-organization contrast. Across the entire 90 s, M2 effort was only 1.15% above CURRENT for FS-001 and below CURRENT for FS-002/003, but equal overall effort cannot remove early amplitude or later impact confounding.

Before/after the first target renewal follows. These are unequal-duration windows, not comparative success tests. Segment excursion is measured from the segment starting position, not from birth. Path and effort partition exactly; excursion and switches need not add.''')
add(table(['Start','Window s','Path','Segment max excursion','Effort','Impulse','Damage','Switches'],[[short(r).replace('-M2',''),f"{fmt(z['start_s'],1)}–{fmt(z['end_s'],1)}",fmt(z['kinematics']['path_length']),fmt(z['kinematics']['maximum_excursion']),fmt(z['physical']['effort_expenditure'],6),fmt(z['physical']['total_impulse'],6),fmt(z['physical']['damage'],6),z['kinematics']['bouts']['0.01']['switches']] for r in rows if r['process']=='M2' for z in [r['M2_renewal_analysis']['before_first_target_renewal'],r['M2_renewal_analysis']['after_first_target_renewal']]]))
add('''After renewal, all three show multiple sign changes, low-drive intervals and reorientation under the same fixed renewal distribution. FS-002 has low-drive intervals and sustained travel without contact. FS-003 repeatedly revisits its region and has a late contact interval. FS-001's large second displacement burst coincides with mover impulse, despite modest effort in that interval. These observations separate realized initial amplitude, actual renewals and obvious contact confounds; they do not isolate a causal temporal effect from nine unreplicated draws.

Every target, selection step, RNG counter and before/after interval metric is retained in `M2_RENEWAL_ANALYSIS.json`. The final target interval is right-censored at 90 s. No process was regenerated to fill a gap.''')
add('![M2 drive renewal, actual motion and effort](M2_RENEWAL_TIMING.png)')
add(table(['Start','Observed target-selection ages s'],[[short(r).replace('-M2',''),', '.join(fmt(v['nominal_selection_time_s'],1) for v in r['M2_renewal_analysis']['renewals'])] for r in rows if r['process']=='M2']))
add('''## Limits and review boundary

This completes the authorized motor/world exposure screen. It does not establish learning efficacy, survival advantage, general environmental coverage, an optimal motor law or overnight reliability. Ninety seconds and three original starts cannot support those claims. No motor was ranked by food, survival or learned-state magnitude. No winner is selected automatically.

No P learning law, birth law, Nursery geometry, viability/resilience parameter, source law, motor parameter, RNG distribution, native/field/wave cadence or evidence contract was changed. There was no new prehistory, long run, resurrection sandbox, Founder Search, additional commissioning case, retry, continuation, push, PR or merge. No old sealed human B1 evaluator state was read. The previous incomplete v0.1 batch and its archive were preserved.

Only observer/report/figure files were written after the nine cases stopped. The first passive plotting attempt rejected an overly narrow display range because recorded mover-driven velocity exceeded it; the displayed range was widened consistently across M2 panels to include every value. This was a presentation correction only. The graphs were visually reviewed and spacing corrected; no trajectory or metric was changed.

The corrected apparatus completed this limited contact exposure without a stop. That increases the bounded evidence beyond the earlier failing geometry; it does not certify many hours of high-contact operation or authorize it. Jason review is the next boundary.

## Review files

- `PASSIVE_RESULTS.json` and per-case `*_DETAILS.json`: all planned metrics, bout lists, threshold/grid sensitivity, physical ledgers and coupling summaries.
- `AVAILABLE_CASE_METRICS.csv`, `COVERAGE_AND_EXCURSION_GROWTH.csv`, `ALL_NINE_DISPOSITIONS.csv`: tabular review.
- `M2_RENEWAL_ANALYSIS.json`, per-case `*_WAVE_COUPLING.json`: actual motor state/renewal and susceptibility diagnostics.
- `NINE_CASE_PATHS`, `REACH_AND_COVERAGE`, `M2_RENEWAL_TIMING`: PNG previews and matching SVGs.
- `EXECUTION_CUSTODY_SEAL.json`, `PASSIVE_VALIDATION.json`, `RESOURCE_ACTUALS.json`, `FINAL_VERIFICATION.json`: evidence, resource and preservation checks.
- `PACKAGE_MANIFEST.json` and `ARCHIVE_VERIFICATION.json`: the single new result archive's contents and SHA-256. The archive contains the exact preparation/authorities, complete nine-case evidence, frozen source and review outputs. Original absolute paths in historical bindings remain literal provenance, not a portable permission to execute.''')
(OUT/'MOTOR_COMMISSIONING_RESULT_v0_2.md').write_text('\n\n'.join(parts)+'\n',encoding='utf8')
(OUT/'README.md').write_text('''# Motor commissioning v0.2 — completed

Start with [the complete report](MOTOR_COMMISSIONING_RESULT_v0_2.md).

All nine cases completed once at 90 seconds / 9000 steps. This folder is a passive review, not an execution authority. No candidate is selected.

Figures: [paths](NINE_CASE_PATHS.png), [reach and coverage](REACH_AND_COVERAGE.png), [M2 renewals](M2_RENEWAL_TIMING.png).

The review archive contains `results/`, `execution/`, `preparation/`, `frozen_source/` and `references/`. Start with `results/MOTOR_COMMISSIONING_RESULT_v0_2.md` after extraction. The supplied analysis scripts retain local provenance paths; review data/figures are directly portable. Do not run the frozen executor or interpret packaging as permission for more simulation.
''',encoding='utf8')
print('Report and README written from sealed passive records.')
