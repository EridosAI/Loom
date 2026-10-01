"""Write the outcome report from retained closed records only."""
import json,pathlib,shutil
S=pathlib.Path(__file__).resolve().parent
B=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\first-commissioning-A1-20260925-5f077481')
O=B/'read-only-review'
x=json.loads((O/'A1_RESULT_SUMMARY.json').read_bytes())
execution=json.loads((B/'EXECUTION_RESULT.json').read_bytes())
shutil.copyfile(S/'write_report.py',O/'write_report.py')
def num(v):return 'not available' if v is None else f'{v:.12g}'
def yes(v):return 'yes' if v is True else 'no' if v is False else 'unresolved'
first=x['first_positive_net_contact_window']
record_check='completed without a reported validation error' if x['V1_record_validation'] is not None else 'reported a validation error; see V1_POST_RECORD_VALIDATION_ERROR.json'
boundary_check='completed without a reported validation error' if x['V3'] is not None else 'reported a validation error; see V3_BOUNDARY_ERROR.json'
first_text='None recorded.' if first is None else f"First fixed complete positive-net contact interval: {num(first['start_time'])}–{num(first['end_time'])} s, E change {num(first['energy_delta'])}, propagated arithmetic allowance {num(first['propagated_arithmetic_allowance'])}. Every fixed interval is retained; this first interval is identified chronologically, not used to select a route or tune settings."
stop=f"The single A1 attempt stopped at {num(x['simulated_seconds'])} simulated seconds / native record {x['native_records']} as **{x['stop_reason']}** (cause: `{x['stop_cause']}`)."
if x['stop_reason']=='administrative_pause':stop+=' The approved resource/administrative boundary stopped the attempt before the 120-second simulated ceiling. No automatic resume or replacement attempt was made.'
text=f'''# First Loom P coupling commissioning — one A1 result

{stop}

**Validation limitation:** V1, V2 and A0 completed; the V3 initial checks completed, but the V3 post-check remains incomplete. My read-only checker incorrectly expected equal native/sensor counts. The reviewed recorder writes one initial display envelope followed by the per-step rows: 9,184 sensor entries versus 9,183 native entries. The subsequent V3 comparisons were not reached. `V3_POST_CHECK_LIMITATION.md`, `V3_COUNT_FINDING.json` and the original error preserve this finding. No corrected checker rerun or apparatus patch was made. These observations therefore are not an all-checks-clear commissioning conclusion.

Authority: `a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc`. Jason's exact approval is retained in `../AUTHORIZATION_SOURCE.txt`; the mechanism's closed envelope is `../APPROVAL_REQUEST.json`; the actual six-field grant is in `../LAUNCHED_MANIFEST.json`. Its canonical execution object remains byte-identical to the approved object. There was exactly **{x['attempts']}** Run constructor attempt and no retry, resume, route substitution, parameter change, patch or physical replay.

P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Apparatus: `5f07748102cb5eaa302569c87efbae095050e9fe`. Worktree: `C:\\Users\\Jason\\Desktop\\Eridos\\Loom-p-apparatus-20260924-01a0c405`, branch `build/p-commissioning-apparatus-20260924-01a0c405`. No new commit or vault Git write was made.

## Physical observations

| Predeclared distinction | Actual observation |
|---|---|
| Geometric approach | Contact locus reached: {yes(x['geometric_approach_achieved'])}; minimum recorded source surface gap {num(x['minimum_source_surface_gap'])}. |
| Certified physical contact | {yes(x['certified_source_contact'])}; first source-0 event at {num(x['first_contact_time'])} s. |
| Sustained support | {num(x['positive_duration_contact_seconds'])} s of positive-duration source contact, {x['contact_interval_count']} contiguous interval(s); measured force range {num(x['sustained_force_min'])}–{num(x['sustained_force_max'])}. Raw impact/release/support events retained. |
| Source debit / body credit | Source-0 transfer {num(x['source_0_transfer'])}; debit reconstructed from stocks and renewal {num(x['source_0_debit_from_stock_and_renewal'])}; all-source transfer {num(x['all_source_transfer'])}; body credit reconstructed from E and cost {num(x['body_credit_from_energy_and_cost'])}. |
| Transfer sign | {x['transfer_interpretation']}; accumulated allowance {num(x['transfer_sign_allowance'])}. Exact zero and unresolved numerical signs retain their separate meanings. |
| Complete positive-net contact intervals | {x['positive_net_contact_window_count']} of {x['complete_fixed_windows']} complete fixed 0.2-second windows; {x['negative_net_contact_window_count']} contact windows had resolved negative net E. {x['partial_windows']} partial tail window(s) are separate. |
| Whole-attempt energy | {num(x['initial_energy'])} → {num(x['final_energy'])}, change {num(x['whole_attempt_energy_delta'])}; expenditure {num(x['total_expenditure'])}. This aggregate is distinct from individual contact intervals. |
| Integrity | {num(x['initial_integrity'])} → {num(x['final_integrity'])}; actual impact/stress/restoration operands are preserved. |
| Source stock | Source-0 final stock {num(x['source_0_final_stock'])}; cumulative renewal {num(x['source_0_renewal'])}. No refill/reset was supplied. |
| Physical nonviability | {yes(x['physical_nonviability'])}; terminal dimension `{x['terminal_dimension']}`. |
| Controller/apparatus exception | `{x['trajectory_failure']}`. This field is separate from contact or energy outcome. |
| Stop / record completeness | `{x['stop_reason']}` / complete={x['record_complete']}; stop cause `{x['stop_cause']}`. |

{first_text}

These observations concern one externally controlled physical witness. Positive transfer or net gain does not establish P's discovery, learning, survival strategy, global ecology or indefinite viability. A transfer-only interval is informative. Controller failure would not establish physical impossibility. No observation has been converted into PASS/FAIL for P or used to change the apparatus.

## V1–V3 and A0

V1 checked exact Git/source/runtime/configuration/cache/snapshot/authority identities before launch. The initial state and phase matched. Post-record validation {record_check}. `V1_POST_RECORD_VALIDATION.json`, or its explicit error record, contains the existing segment validator's result with **replay=false**, covering exact receipt/file hashes, native sequence, issued-decision journal and ledger. Observed maximum accounting residual: {num(x['maximum_accounting_residual'])}; the unchanged arithmetic tolerance is 1e-12. Errors, if any, are retained separately and are not patched.

V2 first read the retained historical R1-P event operands without replay, clearly labelled historical. The live result uses only this A1's actual event records. `V2_ACCOUNTING.json` retains every source debit/body-credit/cost/renewal operand; `A1_OBSERVATIONS.json` contains all fixed-window calculations and certified contact events. `SOURCE_0_CONTACT_INTERVALS.json` retains the contact intervals with the existing event-time tolerance and no minimum duration gate.

V3 {boundary_check}. Its checks cover the actual privileged controller inputs, every issued versus delivered command, raw sensor/native equality and held E/I cadence. They compare complete initial/final inactive neural state and RNG counters. Result details: `V3_BOUNDARY.json` (or its explicit error record); only completed checks support a claim of invariance. The external neural object did not become an intact-P or perceptual trial.

A0 recomputed the approved finite-body geometry with no world evolution: the (6,3)→(4,3) centre approach reaches source-0 with no intervening solid and 6 units of separation from the mover's swept geometry. The separately declared analytical left bypass retains at least 0.5 static clearance and 3 mover-union clearance. The phase snapshots remain geometric calculations; no bypass/crossing trajectory was executed. `A0_GEOMETRY.json` preserves all operands and phase values.

## Timing, records and preservation

Recorded counts: {x['native_records']} native rows; {x['event_records']} physical event rows; {x['command_decisions']} controller decisions; {x['wave_records']} neural wave rows. The receipt contains actual session counters; the V3 finding distinguishes completed inactive-organism/RNG comparisons from the subsequent comparisons that were not reached. No other case, new birth or prehistory was executed. No physical replay was performed during verification.

Recorder wall time: {num(x['recorder_wall_seconds'])} seconds. Whole process including preflight: {num(x['whole_process_wall_seconds'])} seconds. Read-only analysis: {num(x['read_only_analysis_wall_seconds'])} seconds. Uncompressed recorded streams: {x['recorded_uncompressed_bytes']} bytes. Trajectory files including snapshots/receipt: {x['trajectory_file_bytes']} bytes. The approved limits remained 120 simulated seconds, 1,200 run wall seconds and 1,500,000,000 uncompressed record bytes. Record closure and read-only reporting may finish after evolution stops at a resource boundary; they add no body time.

Original runtime/configuration/cache files unchanged: {execution['original_runtime_config_cache_unchanged']}. Git checkpoint unchanged: {execution['checkpoint_unchanged']}; status clean: {execution['git_status_clean']}. Raw evidence unchanged during analysis: {x['raw_evidence_unchanged_during_analysis']}. The exact untouched launch packet is included in the portable result archive. Its absolute host paths remain preserved; they are not silently rewritten for a relocated reviewer.

Read-only analysis errors: `{x['analysis_errors']}`. No helper or reviewed code was patched in response to the case.

## Boundary

Only V1–V3/A0 and this one A1 were attempted, with the V3 post-check limitation stated above. A2–A5, B1–B4, C1/C2, newborn lives, fixed-structure diagnostics, perceptual/scientific trials, sweeps, tuning, new prehistory and mechanism/world changes were not performed. No push, PR, merge or evidential freeze occurred. The 28.17 simulated seconds remaining to A1's 120-second ceiling were not observed. Work stops at the approved boundary.
'''
with (O/'FIRST_A1_COMMISSIONING_REPORT.md').open('x',encoding='utf-8') as f:f.write(text)
print(O/'FIRST_A1_COMMISSIONING_REPORT.md')
