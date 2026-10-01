# Loom P — single A2 commissioning result

Authority: `229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007`.
P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Apparatus: `5f07748102cb5eaa302569c87efbae095050e9fe`.

The single authorized A2 attempt stopped at **180 simulated seconds**, native index **18000**, as **administrative_cutoff** (cause: `None`). Record complete: **True**. Exactly 1 Run constructor attempt(s); no retry, continuation or replacement case.

The requested sequence was observed in this one external physical witness: productive first-source contact, a net-negative interval during continued residence while stock remained nonzero, departure without reset, real travel expenditure, and productive contact with a different source. These are separate measured milestones, not an overall P pass/fail or an efficacy result.

## Physical observations

| Distinction | Recorded observation |
|---|---|
| First-source certified contact | 6.3101904865 s; event 632 |
| First-source transfer | First: 6.32 s; event 633; cumulative 0.188866528375, positive_resolved |
| First-source residence | 83.6898095135 s of positive-duration support in 1 interval(s); force range [0.09997717404633852, 0.27074663791428305] |
| First-source stock | 0.2 → 0.0683633712998; cumulative renewal 0.0572298996746; full native/event history retained |
| First net-negative contact-containing residence window | 52–52.2 s; net E -1.12187249834e-06; intake 0.000323929572681; cost 0.000325051445179 |
| First fully supported negative residence window | 52–52.2 s; net E -1.12187249834e-06; intake 0.000323929572681; cost 0.000325051445179 |
| Commanded departure | 90 s |
| Actual source-0 release | 90 s; event 9002 |
| E/I at release | [0.7400694253244556, 0.9930767410641572] |
| First clear native endpoint | 90.01 s; exact brackets/reserves in A2_OBSERVATIONS.json |
| One body-diameter surface clearance | 97.63 s; descriptive, not a pass gate |
| Travel from observed departure | {'start': 90.00000000000914, 'end': 132.3764279535912, 'duration': 42.37642795358205, 'whole_events_included': 4238, 'source_transfers': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'gross_intake': 0.0, 'expenditure': 0.07565364813787812, 'boundary_straddling_events': [], 'complete_event_boundary_coverage': True, 'arrived': True, 'departure_endpoint_precision': 'exact release event'} |
| Second-source geometric arrival | {'time': 132.3764279535912, 'position': [9.004680346670531, 2.903362596320232], 'event_index': 13240, 'kind': 'event', 'surface_gap': 4.693045951853492e-11} |
| Second-source certified contact | 132.376427954 s; event 13241 |
| Second-source stock before first certified contact | 0.2; pre/post renewal/transfer operands retained |
| Second-source transfer | First: 132.38 s; event 13242; cumulative 0.151448245864, positive_resolved |
| Second-source positive-net interval | 132.4–132.6 s; net E 0.00143030160482; intake 0.00178690647698; cost 0.000356604872166 |
| Second-source contact windows | 226 positive and 13 negative among 239 complete contact-containing windows |
| Whole-case gross intake / expenditure / net E | 0.340314774239 / 0.302163541585 / 0.0381512326544 |
| Final E/I | [0.7381512326543674, 0.9863441416153598] |
| Physical nonviability | Terminal dimension: `None` |
| Controller/apparatus exception | `None`; receipt error `None` |
| Administrative stop | `administrative_cutoff` / stored cause `None`; 18,000 native steps cover the full prescribed horizon within the existing clock tolerance. Raw 180-minus-final-time subtraction: 1.87299065146e-11 s (representation residual, not an unobserved step) |

All 900 complete fixed 0.2-second windows and 0 partial windows are preserved in ALL_FIXED_WINDOWS.json. Contact-containing and fully supported windows have separate counts. The negative residence transition is a finite-window observation, not an exact instantaneous crossing or an exactly-zero stock requirement.

## Travel, mover and limits

Commanded-travel interval (t=90 to source-1 contact, or recorded stop): `{'start': 90.0, 'end': 132.3764279535912, 'duration': 42.37642795359119, 'whole_events_included': 4238, 'source_transfers': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], 'gross_intake': 0.0, 'expenditure': 0.07565364813787812, 'boundary_straddling_events': [9001], 'complete_event_boundary_coverage': False}`. Actual travel costs above use continuous event accounting and explicitly flag any boundary-straddling event; no proportional transfer interpolation or reset is supplied.

Mover contact events: **0**. Nearest recorded decision-time clearance: `{'time': 96.90000000001267, 'gap': 5.762765571214633, 'body_position': [4.726336447808764, 3.252851983849663], 'mover_rectangle': [5.168348058855637, 7.168348058855637, 9.5, 10.5], 'velocity': [0.24048575658651694, 0.0]}`. Mover geometry is recorded at 0.1-second decision cadence. Not identifiable from saved external-arm records: no ray-hit object identities were recorded. Raw light values alone do not certify mover interception. No new ray tracing performed. Other causal exposure remains unresolved.

Controller adequacy is assessed from the actual prescribed stages, release/arrival records, commands and force history. Missing arrival or transfer would leave controller, route, reserve and physical causes to be discriminated; it would not by itself establish ecological impossibility. This external physical witness supplies no P discovery, perception, learning, useful regulation, survival strategy, global ecological adequacy or indefinite-maintenance result. No observation was collapsed into an overall PASS/FAIL.

Source-1 support occurred in 3 intervals, with recorded gaps `[{'after': 142.76000000001514, 'before': 142.7600395926028, 'seconds': 3.959258765462437e-05}, {'after': 164.19999999999564, 'before': 164.20003960557497, 'seconds': 3.960557933169184e-05}]`. These brief release/recontact episodes are retained, not relabelled as substantive revisits. No source-0 recontact occurred after departure. Actual sustained force reached 0.270746637914 at source 0 and 0.273267025397 at source 1, above the 0.1 controller target and 0.25 stress threshold during portions of contact. Total integrity loss was 0.0136558583846, with repair 0; there was no terminal crossing. The target force is not a guarantee of the realized force.

## Reporting limitation retained

The interval helper over-flags sub-tolerance endpoint offsets at nominal 90/120 boundaries. These flags do not identify an extra or missing physical step. Exact recorded release-to-contact travel has no straddling event and its cost remains 0.07565364813787812. Raw flags and subtraction remain unchanged.
The flagged operands are `[{'event_index': 9001, 'recorded_endpoint': 90.00000000000914, 'nearest_nominal_boundary': 90.0, 'offset_seconds': 9.137579581874888e-12, 'within_existing_event_time_tolerance': True}, {'event_index': 12002, 'recorded_endpoint': 120.00000000002449, 'nearest_nominal_boundary': 120.0, 'offset_seconds': 2.4485302674293052e-11, 'within_existing_event_time_tolerance': True}]`. The final recorded clock is 179.99999999998127; its approximately 1.87e-11 s difference from 180 is below the unchanged 1e-10 clock tolerance. All 18,000 planned native steps and all 900 fixed windows exist. This note interprets the saved operands; neither the original analysis output nor its helper was patched or rerun.

## Recorded validation and preservation

Completed read-only sections: ['RECORD_INTEGRITY', 'BOUNDARY_AND_DELIVERY', 'ACCOUNTING', 'ALL_FIXED_WINDOWS', 'A2_OBSERVATIONS']. Errors: `{}`.

`RECORD_INTEGRITY`: `{'valid': True, 'complete': True, 'status': 'administrative_cutoff', 'stop_cause': None, 'receipt_payloads': 28, 'record_counts': {'sensor': 18001, 'controller': 1800, 'native': 18000, 'events': 18009, 'diagnostics': 18000}, 'authority_sha256': '229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007', 'physical_replay': False, 'controller_recomputation': False, 'scope': 'Saved receipt, checksum, exact grant/object, native sequence and stop checks. Production verify_segment not invoked because its pending-command validator recomputes waypoint commands even with replay=False.'}`.

`ACCOUNTING`: `{'valid': True, 'maximum_residual': 5.551115123125783e-17, 'arithmetic_tolerance': 1e-12, 'event_chain_discontinuities': [], 'native_event_endpoint_mismatches': []}`.

`BOUNDARY_AND_DELIVERY`: `{'valid': True, 'analysis_version': 'A2 read-only v1.0', 'alignment_source': 'Preserved v3_checker_v1_1.align and validate_inputs, unchanged', 'native_rows': 18000, 'sensor_entries': 18001, 'initial_envelopes': 1, 'controller': {'closed_controller_inputs': 1800, 'delivered_command_rows': 18000, 'controller_command_function_calls': 0, 'last_hold_consumed_steps': 10, 'last_hold_pending_steps': 0}, 'stage_decision_counts': {'0': 900, '1': 300, '2': 600}, 'inactive_organism_sha256': '0d1de850e85a085dd7288cadbd8be0da577211a8a1e47d819a5d7e111024a5ed', 'native_rng_counter_comparisons': 18000, 'neural_wave_rows': 0, 'scope': 'Record-level input/delivery, stage timing and checkpoint invariance; no controller recomputation, replay or unrecorded transient-state claim'}`.

The production segment verifier was not called: its saved pending-command path recomputes the waypoint controller even when physical replay is disabled. The authorized read-only analysis instead verifies receipt hashes, exact authority, ledger, saved stage timing, issued-versus-delivered commands, sensor-envelope alignment and checkpoint invariance without generating commands.

Raw evidence unchanged during analysis: **True** (39 files). Original runtime/cache/earlier evidence/approved packet unchanged: **True**. Git HEAD unchanged: **True**; status clean: **True**. No new commit or vault Git write.

Recorder wall time: 2116.0327042 s. Whole execution process: 2116.9375998 s. Read-only analysis: 9.04399759998 s. Uncompressed streams: 105656295 bytes. Recorded counts: `{'sensor': 18001, 'controller': 1800, 'native': 18000, 'events': 18009, 'diagnostics': 18000}`.

## Exact location and boundary

Worktree: `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405`. Branch: `build/p-commissioning-apparatus-20260924-01a0c405`. Checkpoint remains `5f07748102cb5eaa302569c87efbae095050e9fe`.

The original proposed packet, canonical object, genuine authorization text, normal approval envelope, launched grant, initial snapshot, driver, raw streams, restart snapshots, progress and versioned analysis are separately preserved. Existing native evidence remains suitable for later passive-viewer extension; no viewer was built or inserted here.

Not performed: retry, continuation, route substitution, additional case, new prehistory, new birth, physical/sensory replay, controller recomputation during analysis, apparatus or P patch, tuning, sweep, efficacy test, scientific lifetime, experiment number, preregistration, evidential freeze, push, PR or merge. Stop at the approved review boundary.
