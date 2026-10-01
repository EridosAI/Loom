# First Loom P coupling commissioning — one A1 result

The single A1 attempt stopped at 91.83 simulated seconds / native record 9183 as **administrative_pause** (cause: `wall_time_limit`). The approved resource/administrative boundary stopped the attempt before the 120-second simulated ceiling. No automatic resume or replacement attempt was made.

**Validation limitation:** V1, V2 and A0 completed; the V3 initial checks completed, but the V3 post-check remains incomplete. My read-only checker incorrectly expected equal native/sensor counts. The reviewed recorder writes one initial display envelope followed by the per-step rows: 9,184 sensor entries versus 9,183 native entries. The subsequent V3 comparisons were not reached. `V3_POST_CHECK_LIMITATION.md`, `V3_COUNT_FINDING.json` and the original error preserve this finding. No corrected checker rerun or apparatus patch was made. These observations therefore are not an all-checks-clear commissioning conclusion.

Authority: `a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc`. Jason's exact approval is retained in `../AUTHORIZATION_SOURCE.txt`; the mechanism's closed envelope is `../APPROVAL_REQUEST.json`; the actual six-field grant is in `../LAUNCHED_MANIFEST.json`. Its canonical execution object remains byte-identical to the approved object. There was exactly **1** Run constructor attempt and no retry, resume, route substitution, parameter change, patch or physical replay.

P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Apparatus: `5f07748102cb5eaa302569c87efbae095050e9fe`. Worktree: `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405`, branch `build/p-commissioning-apparatus-20260924-01a0c405`. No new commit or vault Git write was made.

## Physical observations

| Predeclared distinction | Actual observation |
|---|---|
| Geometric approach | Contact locus reached: yes; minimum recorded source surface gap 3.36406458246e-11. |
| Certified physical contact | yes; first source-0 event at 6.3101904865 s. |
| Sustained support | 85.5198095135 s of positive-duration source contact, 1 contiguous interval(s); measured force range 0.0999765084528–0.270746637914. Raw impact/release/support events retained. |
| Source debit / body credit | Source-0 transfer 0.190521120591; debit reconstructed from stocks and renewal 0.190521120591; all-source transfer 0.190521120591; body credit reconstructed from E and cost 0.190521120591. |
| Transfer sign | positive_resolved; accumulated allowance 9.18600097145e-09. Exact zero and unresolved numerical signs retain their separate meanings. |
| Complete positive-net contact intervals | 229 of 459 complete fixed 0.2-second windows; 199 contact windows had resolved negative net E. 1 partial tail window(s) are separate. |
| Whole-attempt energy | 0.7 → 0.738745982019, change 0.0387459820194; expenditure 0.151775138571. This aggregate is distinct from individual contact intervals. |
| Integrity | 1 → 0.993076741064; actual impact/stress/restoration operands are preserved. |
| Source stock | Source-0 final stock 0.0342501327969; cumulative renewal 0.0247712533875. No refill/reset was supplied. |
| Physical nonviability | no; terminal dimension `None`. |
| Controller/apparatus exception | `None`. This field is separate from contact or energy outcome. |
| Stop / record completeness | `administrative_pause` / complete=True; stop cause `wall_time_limit`. |

First fixed complete positive-net contact interval: 6.2–6.4 s, E change 0.000443454535485, propagated arithmetic allowance 2.20004803346e-11. Every fixed interval is retained; this first interval is identified chronologically, not used to select a route or tune settings.

These observations concern one externally controlled physical witness. Positive transfer or net gain does not establish P's discovery, learning, survival strategy, global ecology or indefinite viability. A transfer-only interval is informative. Controller failure would not establish physical impossibility. No observation has been converted into PASS/FAIL for P or used to change the apparatus.

## V1–V3 and A0

V1 checked exact Git/source/runtime/configuration/cache/snapshot/authority identities before launch. The initial state and phase matched. Post-record validation completed without a reported validation error. `V1_POST_RECORD_VALIDATION.json`, or its explicit error record, contains the existing segment validator's result with **replay=false**, covering exact receipt/file hashes, native sequence, issued-decision journal and ledger. Observed maximum accounting residual: 5.55094571654e-17; the unchanged arithmetic tolerance is 1e-12. Errors, if any, are retained separately and are not patched.

V2 first read the retained historical R1-P event operands without replay, clearly labelled historical. The live result uses only this A1's actual event records. `V2_ACCOUNTING.json` retains every source debit/body-credit/cost/renewal operand; `A1_OBSERVATIONS.json` contains all fixed-window calculations and certified contact events. `SOURCE_0_CONTACT_INTERVALS.json` retains the contact intervals with the existing event-time tolerance and no minimum duration gate.

V3 reported a validation error; see V3_BOUNDARY_ERROR.json. Its checks cover the actual privileged controller inputs, every issued versus delivered command, raw sensor/native equality and held E/I cadence. They compare complete initial/final inactive neural state and RNG counters. Result details: `V3_BOUNDARY.json` (or its explicit error record); only completed checks support a claim of invariance. The external neural object did not become an intact-P or perceptual trial.

A0 recomputed the approved finite-body geometry with no world evolution: the (6,3)→(4,3) centre approach reaches source-0 with no intervening solid and 6 units of separation from the mover's swept geometry. The separately declared analytical left bypass retains at least 0.5 static clearance and 3 mover-union clearance. The phase snapshots remain geometric calculations; no bypass/crossing trajectory was executed. `A0_GEOMETRY.json` preserves all operands and phase values.

## Timing, records and preservation

Recorded counts: 9183 native rows; 9185 physical event rows; 919 controller decisions; 0 neural wave rows. The receipt contains actual session counters; the V3 finding distinguishes completed inactive-organism/RNG comparisons from the subsequent comparisons that were not reached. No other case, new birth or prehistory was executed. No physical replay was performed during verification.

Recorder wall time: 1201.2759736 seconds. Whole process including preflight: 1202.0992399 seconds. Read-only analysis: 16.5902145 seconds. Uncompressed recorded streams: 54337980 bytes. Trajectory files including snapshots/receipt: 24977060 bytes. The approved limits remained 120 simulated seconds, 1,200 run wall seconds and 1,500,000,000 uncompressed record bytes. Record closure and read-only reporting may finish after evolution stops at a resource boundary; they add no body time.

Original runtime/configuration/cache files unchanged: True. Git checkpoint unchanged: True; status clean: True. Raw evidence unchanged during analysis: True. The exact untouched launch packet is included in the portable result archive. Its absolute host paths remain preserved; they are not silently rewritten for a relocated reviewer.

Read-only analysis errors: `{'V3_BOUNDARY': {'exception': 'AssertionError()', 'traceback': 'Traceback (most recent call last):\n  File "C:\\Users\\Jason\\.codex\\.chatgpt-projects\\g-p-6a6fb425222c8191a814fdc0f7d89f97\\a1_execution_staging_20260925\\read_results.py", line 41, in attempt\n    value=fn();result[name]=value;write(name+\'.json\',value);return value\n  File "C:\\Users\\Jason\\.codex\\.chatgpt-projects\\g-p-6a6fb425222c8191a814fdc0f7d89f97\\a1_execution_staging_20260925\\read_results.py", line 69, in v3\n    assert len(native)==len(sensors)==len(diagnostic)\n           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\nAssertionError\n'}}`. No helper or reviewed code was patched in response to the case.

## Boundary

Only V1–V3/A0 and this one A1 were attempted, with the V3 post-check limitation stated above. A2–A5, B1–B4, C1/C2, newborn lives, fixed-structure diagnostics, perceptual/scientific trials, sweeps, tuning, new prehistory and mechanism/world changes were not performed. No push, PR, merge or evidential freeze occurred. The 28.17 simulated seconds remaining to A1's 120-second ceiling were not observed. Work stops at the approved boundary.
