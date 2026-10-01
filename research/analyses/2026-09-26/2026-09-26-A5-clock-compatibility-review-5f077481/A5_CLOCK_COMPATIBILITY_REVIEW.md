# A5 clock compatibility review

**Classification: APPARATUS DEFECT — correction required to pose approved longer horizons.**

The intended safety invariant is valid: an issued command's time, native index, hold, stage and case authority must agree. Its implementation incorrectly assumes that an absolute clock formed by thousands of floating additions stays within `1e-10` seconds of a separately multiplied index clock. On the pinned runtime it does not. The first rejected command boundary is native **26,950**, nominal **269.5 seconds**. A second, independently affected stage comparator would prevent the transition at **270 seconds** if only the first guard were loosened.

This is not a physical failure of A5, a deliberate 269.5-second limit, or exhaustion of double-precision time resolution. The manifest admits durations through 1,200 seconds; A5's 630-second case and its full-hold-aligned stages fit that declared domain. **A5 remains held and unexecuted.**

**Smallest recommended coherent closure:** correct scheduling and clock provenance within the apparatus only. Use the already authoritative native indices for command/stage/case ownership, and validate the unchanged physical timestamp against the clock recurrence that actually produced it. Preserve continuous physical time, P, world arithmetic, controller gains, event tolerances, full holds, terminal substeps and original deadlines. Do not simply remove a guard, globally increase the physical event tolerance, reset the clock, or shorten A5. This is a recommendation for Jason's decision, not an implemented correction.

## 1. Exact scope and evidence

| Identity | Reviewed value |
|---|---|
| P | `6bc9683b54e4fa80136fe8534d7713e2a250a95f` |
| Apparatus | `5f07748102cb5eaa302569c87efbae095050e9fe` |
| Held A5 object, unchanged | `88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6` |
| Worktree | `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405` |
| Branch, unchanged | `build/p-commissioning-apparatus-20260924-01a0c405` |
| Runtime | Pinned desktop-local CPython 3.13.5, NumPy 2.3.3, SciPy 1.16.2 |
| Configuration identity | `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a` |

The held packet's manifest, payload hashes, runtime and apparatus identity were checked. Current workbench orientation registers A1–A4 as observed and A5 as not executed. Historical draft and review dispositions remain dated history. This diagnosis does not edit their canon or grant new execution.

Evidence classes used here are kept distinct:

- **Direct component evidence:** calls to unchanged clock/pending predicates on inert dictionaries and manufactured clock objects; six existing detached clock-test cases; no world or Run construction.
- **Arithmetic evidence:** repeated scalar additions, exact float values, ULP spacing, local elapsed differences and independent integer/Decimal deadline calculations, through 630 seconds and the declared 1,200-second maximum. These are not trajectories, cohorts or a parameter search.
- **Source inference:** the conditional path a valid nonterminal execution would take, and which guard stops it. The actual A5 body state and commands at 269.5 seconds are not known or generated.
- **Historical observed evidence:** saved A1–A4 action metadata read without replay or controller recomputation.

Results: [DIAGNOSTIC_RESULTS.json](DIAGNOSTIC_RESULTS.json), [ARITHMETIC_DETAIL.json](ARITHMETIC_DETAIL.json), [CLOCK_HISTORY.json](CLOCK_HISTORY.json), and [PRESERVATION.json](PRESERVATION.json). The reproducible new detached harness is `diagnose_clock.py`; it is diagnostic code, not a production patch or launcher. Exact reference sources are under `references/`. All **250 enumerated source/evidence files** remained unchanged, including the held packet and the reviewed raw records. Git stayed clean at the pinned commit.

## 2. Causal path from the held manifest to rejection

A5 starts at `initial_time=0.0`, `initial_index=0`, has native dt 0.01, command hold 0.1 and hard stop 630.0. Its existing stage deadlines are **90, 120, 270, 300, 450, 480, 630** seconds. Their exact native indices are **9000, 12000, 27000, 30000, 45000, 48000, 63000**. No deadline or route was changed.

All source line references below are for the exact pinned checkout, also copied under `references/instrument/`.

| Path | Relevant source and operation | At native 26,950, assuming no earlier terminal/failure/resource stop |
|---|---|---|
| Physical timestamp generation | `loom_commissioning/adapter.py::coupled`, lines 68–79: one full nonterminal native call uses dt=0.01, then `e.time += dt`. `step`, lines 94–109, increments the native index. | Index 26,950; accumulated time `269.4999999998999`. |
| Command request | `runner.py::hold`, lines 240–243 → `begin_command`, lines 154–157. `_guard` checks the previous issued command; its index was 26,940. | The completed previous ten-step hold still has valid provenance and zero remainder. A new decision is requested. |
| Stage selection | `controllers.py::waypoint_command`, lines 76–89, uses `time_due` from lines 15–20. | Zero-based stage **2**, target **(10,3)**, target force **0.1**, deadline **270.0**. The stage is not due yet, correctly. |
| Case remaining arithmetic | `runner.py::remaining`, lines 151–152. | `(630.0 - time)/0.01 = 36050.00000001001`; rounding gives **36,050** steps. The prospective hold is **10** steps. |
| New hold within stage | `runner.py::begin_command`, lines 168–174. | `end = time + 10*0.01 = 269.5999999998999`, less than 270.0. This check passes. |
| Case time guard | `runner.py::_guard`, line 148. | `time <= 630.0 + 1e-9` passes. There is no 269.5-second case cap. |
| Action assembly / validation | `runner.py::begin_command`, lines 179–185. The approved stage identity is recomputed; the action carries time, index, original hold length, stage/case deadlines and execution identity. | The execution identity still binds the exact held object; no route substitution is involved. |
| **Actual rejecting branch** | **`loom_commissioning/pending.py::validate_decision`, lines 44–46**; called at **`runner.py:185`**. | The absolute time/index comparison exceeds `1e-10`. `contract.py::require`, line 29, raises **`ValueError: issued decision clock mismatch`**. |
| What does not happen afterward | `runner.py:186–190` would install/seal the new decision and append its command record; `hold` would then call `advance`. | Those operations are not reached for the rejected new action. No extra native hold is authorized by this failure. |

The precise condition is:

```python
type(d['native_index']) is int and d['native_index'] >= m['initial_index']
and abs(d['time'] - (m['initial_time']
    + (d['native_index'] - m['initial_index']) * .01)) <= 1e-10
```

This literal `1e-10` is an apparatus provenance condition, although it equals the configuration's event-time tolerance numerically. It is not a duration setting. `contract.py::validate_manifest`, lines 57–61, separately accepts `0 < duration <= 1200` on the native grid. The old P engineering helper's 30-second smoke cap is not in this causal path: commissioning calls the native adapter directly, not `Engine.run_bounded`.

The exception occurs in `begin_command`, outside `advance`'s exception/failure-finalization block at lines 198–238. Therefore the diagnosis does not invent a completed A5 failure receipt or claim that this branch alone automatically finalizes one. An authorized caller would have to preserve/report a rejected attempt. **No such attempt was made here.**

## 3. Exact arithmetic and why it first crosses near 269.5 seconds

Let $t_0=0$ and $t_{n+1}=\mathrm{fl}(t_n+\mathrm{fl}(0.01))$. The guard compares this recurrence with the separately rounded product $\mathrm{fl}(n\times0.01)$.

| Native index | Repeated-addition time | Index product | Difference | Clock predicate |
|---:|---:|---:|---:|---|
| 12,800 | 128.00000000002856 | 128.0 | +2.8563817977556027e-11 | Pass |
| 26,940 | 269.3999999999 | 269.4 | −9.99875737761613e-11 | Pass; last valid ten-step decision before failure |
| 26,941 | 269.4099999999 | 269.41 | −1.000444171950221e-10 | First scalar exceedance; not a fresh decision boundary |
| **26,950** | **269.4999999998999** | **269.5** | **−1.0010126061388291e-10** | **First fresh decision rejection** |
| 27,000 | 269.99999999989944 | 270.0 | −1.0055600796476938e-10 | Fail |
| 63,000 | 629.9999999995721 | 630.0 | −4.2791725718416274e-10 | Fail |
| 120,000 | 1199.9999999990537 | 1200.0 | −9.463292371947318e-10 | Fail |

At the first rejected decision, the accumulated binary64 value is exactly:

```text
hex:                0x1.0d7fffffff91fp+8
exact decimal:      269.49999999989989873938611708581447601318359375
index-product hex:  0x1.0d80000000000p+8
exact difference:  -1.0010126061388291418552398681640625E-10
```

The literal 0.01 itself is `0.01000000000000000020816681711721685132943093776702880859375`. That initial representation error is tiny. The main effect here is **rounding each subsequent addition at the magnitude of the absolute clock**. In the relevant ranges, the represented increment becomes `0.009999999999990905`, a deficit of about **9.094947017729283e-15 seconds per addition** relative to exact 0.01. The earlier positive error near 128 seconds is progressively consumed and becomes negative. It crosses the chosen tolerance at index 26,941; the next ten-step command opportunity is index 26,950.

There is no special floating-point exponent transition, recorder threshold, source-renewal event or controller deadline at 269.5. The threshold is the accidental intersection of this summation error with a fixed acceptance band. Different accumulation origins or algorithms could cross it elsewhere; it is not a general maximum representable simulation time.

The unmodified production predicate was called directly on the exact A5 manifest with a schema/identity-correct clock prefix and deliberately invalid downstream input sentinel. At 26,940 it passed the clock check and reached the expected later `forbidden controller input` rejection. At 26,950 and 27,000 it instead rejected at `pending.py:44` with `issued decision clock mismatch`, before reaching the sentinel. No A5 controller call occurred. These are branch-isolation probes, **not fabricated valid A5 world states or issued commands**.

Complete detached manual pending-input checks independently accepted the accumulated 26,940 decision at progress 0/7/9/10 and rejected a stale positive remainder at completion. They rejected decisions issued at 26,950 and later at the absolute clock condition. These inert test dictionaries are not executable commissioning manifests, have no grants, and were not used to create a Run.

## 4. The next incompatibility is independent

At nominal 270 seconds:

```text
time                    = 269.99999999989944
deadline                = 270.0
time_due(time, deadline) = False
selected stage          = 2, rather than 3
prospective hold end    = 270.09999999989947
new full hold fits      = False
```

`controllers.py::time_due` tests `now >= deadline` or `math.isclose(..., rel_tol=0, abs_tol=Config().event_time_tol)`. The accumulated clock is now slightly more than `1e-10` below the declared deadline, so the old stage remains selected. `runner.py:174` then rejects a new ten-step hold with **`command hold would cross prescribed stage boundary`**. The same pattern appears at the selected 300, 450 and 480-second transitions in detached arithmetic.

Thus changing only `pending.py:45` cannot close A5 compatibility. Removing it would expose the stage error rather than solve scheduling. The final 630-second case cap is different: its remaining-step expression rounds to zero and its separate `1e-9` cutoff check passes for the scalar history. Nevertheless the final stage's `time_due` still says false, illustrating inconsistent clock conventions. The unchanged apparatus never reaches this complete hypothetical prefix because earlier guards stop it.

## 5. Classification and historical origin

| Possible explanation | Finding |
|---|---|
| Deliberate safety invariant | **Yes, the invariant is deliberate:** bind issued decision to native progress and prevent stale/enlarged holds. Keep it. **No evidence of an intended 269.5-second ceiling.** |
| Numerical precision safeguard | The tolerance is a numerical consistency check, but it bounds the wrong error model: global repeated addition versus index multiplication. It does not prove insufficient float resolution. |
| Configuration/schema limit | No. A5 is inside the declared 1,200-second ceiling. Its native/wave/hold ratios and stage grid are valid. |
| Controller assumption | The stage comparator independently assumes the same fixed absolute band remains sufficient over long accumulated clocks. This affects prescribed timing, not navigation competence or gains. |
| Recorder/restart assumption | Pending validation is reused before saves, restart and journal verification, so it carries the incompatibility into those paths. Gzip/JSON storage is not its cause. |
| Historical short-check coverage | Supported. Existing short boundary/hold tests and a one-step large-clock fixture did not exercise accumulation from zero to a late deadline. |
| Actual defect | **Yes: apparatus clock/scheduling consistency defect over an admitted horizon.** No A5 design change or physical-law change is needed to explain it. |

The history is specific:

1. **05abf604:** `RUNNER_AUTHORITY_CONTROLLER_REVIEW.md` found the original exact-`>=` comparator failed at `0.09999999999999999`, allowing the old stage an extra hold. It also disclosed a manufactured **1199.99 → 1200.00 one-step** check, not a 1,200-second accumulated history.
2. **9d31e790:** `CORRECTION_REPORT.md` and `INDEPENDENT_CLOCK_REVIEW.md` document `time_due` using the existing `1e-10` event tolerance without changing world time. Near-0.1 boundaries, crossing-hold rejection and ordinary pauses at 7/9/10 steps were reviewed. The independent review explicitly limited its arbitrary-clock/long-run claim.
3. **5f077481:** `FINAL_CORRECTION_REPORT.md` and `LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md` closed pending-command mutation and restart provenance findings. Git blame places **all of `pending.validate_decision`, including the absolute clock check, in this commit**. The numerical comparator remained unchanged. Its new safety checks were verified over short components, not the full declared accumulated-time range.

The large-clock test `test_long_ceiling_endpoint_without_long_trajectory` initializes both time and the manifest origin to **1199.99**, then executes one native step. Its clock validation spans one relative increment; it cannot reveal 120,000 additions from zero. `test_native_wave_noise_schedules_above_old_cap` likewise uses manufactured boundary clocks. The pause/resume tests invoke real short physical steps, so they were **read, not rerun**, under the present no-world instruction.

Six existing tests that only compute detached controller-boundary arithmetic were executed: five parameter cases of `test_exact_review_boundary` and `test_final_stage_and_not_due_control`. All passed. There were 13 controller-function calls on the old manufactured saved boundary inputs, **zero against an A5 world**. This shows the old short comparison guarantee still holds; it does not cure the new long-clock incompatibility.

## 6. Numerical soundness through 630 seconds

**Float resolution and integer cadence are adequate; the complete current apparatus is not clock-compatible over that horizon.** These are separate conclusions.

| Timing concern | Source/arithmetic evidence | Conclusion and limit |
|---|---|---|
| Native 0.01 s | 63,000 scalar increments remain strictly increasing; minimum represented increment `0.009999999999990905`. Maximum absolute accumulated/index discrepancy `4.2791725718416274e-10`. | No lost native increment. The provenance guard nevertheless falsely rejects legitimate accumulated timestamps. |
| Command 0.1 s | Ten native indices per hold. Maximum error between ten local additions and `issued_time + progress*0.01`, over all tested positions/progress through 630 s, is **1.1368683772161603e-13**. | Local hold progress is well within `1e-10`; global issued-time validation and late stage ownership are not. |
| Wave/body sample 0.2 s | Engine/adapter wave boundaries use native-index modulo 20; SensorHistory samples E/I at modulo 20. `Organism.wave_elapsed` resets each handoff. Twenty explicit additions give `0.20000000000000004`. | 3,150 scalar wave boundaries; no accumulating 630-second wave-phase error. A5 has an inactive neural object and no neural handoffs; body/EI sampling still follows the native count. No neural evolution was tested. |
| Field cadence | `adapter.coupled` calls `FieldSolver.step` once per native call, with dt=0.01 and endpoint `e.time+dt`, then assigns the same addition to world time. | Scheduling has no separate floating field timer. Source supports 63,000 calls for a full nonterminal case; no field solver was executed and no convergence claim is made. |
| Event/terminal time | Physics uses local `elapsed`, `remaining=dt-elapsed`, and local bisection widths. Absolute event stamps are `t+elapsed`. At 630 s, ULP is **1.1368683772161603e-13**. | About 880 ULPs fit inside event tolerance `1e-10`; executed positive intervals at the `1e-12` threshold remain resolvable. Sub-ULP absolute timestamps can coincide, as can legitimate zero-duration impacts. Local duration/event ordering must be preserved. No actual collision or terminal solver was run. |
| Case remaining / cutoff | At every scalar index through 630 and 1,200 s, `round((deadline-time)/0.01)` matches the intended remaining native count. At 630, difference is below the current final `1e-9` allowance. | Existing case arithmetic itself passes these zero-origin scalar checks. This does not bypass failed decision/stage validation or prove all arbitrary origins. |
| Pause/resume | JSON round-trips preserve the tested float values exactly; local ten-step arithmetic is sound. `load_restart`, `save_restart`, `_guard` and `validate_journal` reuse pending validation and preserve original origin/index. | A proper restart does not erase accumulated error. Splitting the case cannot cure it. Full physical save/resume equivalence was not rerun. |
| Native record continuity | `validators.validate_native_sequence` adds saved elapsed values to the segment's saved start, matching the actual repeated-addition convention. | It is not the index-product mismatch source. Replay uses matching saved times; it must not be silently switched to a different physical clock. No replay was performed. |

The 1,200-second scalar extension gives maximum drift **9.463292371947318e-10** and ULP **2.2737367544323206e-13**. It is useful coverage of the schema limit, not execution of that horizon. The supported diagnosis remains narrower than a proof of long-run physical integration accuracy.

`ARITHMETIC_DETAIL.json` distinguishes explicit `+=` accumulation from Python 3.13's more accurate built-in `sum`: the initial diagnostic JSON's `scalar_wave_elapsed_after20` field used the latter and reports 0.2. The actual production-style explicit value is 0.20000000000000004; both satisfy the wave check. Original diagnostic bytes are preserved rather than rewritten.

## 7. What simply increasing a limit would do

Changing the **1,200-second duration cap** would do nothing: 630 already fits it. Increasing only the **absolute decision-clock tolerance** would let the 269.5-second predicate pass but leave the **270-second stage rejection** intact.

A uniform apparatus tolerance of `1e-9` covers the measured zero-origin accumulated drift through 1,200 seconds. That fact alone is insufficient for a safe closure:

- Reusing it for every deadline comparison changes the existing negative control **`.1 - 2e-10` from not due to due**. It broadens authority-boundary interpretation, not merely a passive log check.
- Removing clock provenance entirely loses the check that a timestamp belongs to its native index; index-based remainder checks do not independently detect all incoherent timestamps.
- Relaxing one site but leaving others at `1e-10`/`1e-9` creates inconsistent new-command, pending-hold, stop and restart decisions.
- The scalar observed maximum is not a justified bound for every nonzero origin, partial terminal or altered cadence. Any allowance must state its domain and reject cases outside it.
- Increasing **`Config.event_time_tol`** changes physical event searches/terminal location as well as the controller comparator and changes configuration identity. That is outside an apparatus-only correction and is not recommended.

No physical precision is lost merely by accepting a known representation discrepancy; the risk is accepting inconsistent clock provenance or silently reinterpreting when authority starts/ends. Correct integer ownership can preserve the ten-step/no-overrun invariant without pretending the two floating clocks are identical.

## 8. Candidate closures compared

All entries below are proposals only. Every implemented apparatus change would require a new exact checkpoint, appropriate review and a newly bound execution authority later. **No replacement authority is prepared here.**

| Candidate | Exact code surface and physical effect | Authority / restart / historical effects | Required tests and risks |
|---|---|---|---|
| **A. Raise/remove the guard** | One-line change at `pending.py:45` alone is insufficient. A coherent variant also affects `controllers.time_due`, runner stage/global checks, pending stage/case checks and possibly stop validation. Never raise P's configuration event tolerance. Apparatus-only allowance need not change physical integration. | A larger universal comparison band changes the reviewed boundary acceptance interval. Removal weakens provenance. Saved clock fields can remain unchanged, but historical records still require their matching instrument. A1–A4 evidence need not be rewritten. | Reproduce all late boundaries; retain short negative controls, one-step/count corruption and no extra hold. Uniform `1e-9` fails the existing short not-due control; a justified origin/length-aware error budget could work but must be used consistently. Not recommended as a blind tolerance change. |
| **B. Make physical world time index-derived** | `loom_p/engine.py::_coupled/step` and `loom_commissioning/adapter.py::coupled/step` would derive time from native index; terminal fractional times need explicit treatment. All recorder/native/restart checks must agree. Mathematical laws may be unchanged, but **P code and the exact numerical world evolution change**. | Stage/hold indices are natural, but replacing physical times changes recorded timestamps and time-dependent geometry/fields. Old snapshots/replays cannot be silently translated. New state/clock versioning and authority identity needed. | Late integer-grid and terminal/substep tests; byte-level old/new characterization, wave/field counts, snapshot compatibility. At 630 s, the clock change can shift the mover position by up to about **3.59e-10 m** from timing alone, exceeding the `1e-10` geometry tolerance. Small does not mean bit-identical or consequence-free. Excessive scope for this defect. |
| **C. Local-stage clock with continuous absolute world time** | Apparatus runner/controller/pending stage timing and serialized session gain a local clock/anchor; absolute provenance still needs correction. No P or world-law change if the physical timestamp is untouched. | Stage clocks must resume exactly without being reset by pause. Multiple clock states must stay bound to the same original stage/case deadlines. Existing records lack that new stage state. | Subtracting stored absolute timestamps is insufficient: `t450 - t300 = 149.99999999986358`, already more than `1e-10` short of 150. A separately accumulated 150-second local clock is within tolerance, but can fail for longer stages and adds reset/provenance complexity. Test every boundary, pause/restart and stale-anchor fault. |
| **D. Apparatus index ownership plus faithful physical-clock validation — recommended** | One small shared apparatus clock/deadline helper; its callers in `runner.py`, `pending.py`, controller stage selection/recomputation and `validators.py`. Keep `loom_p/*`, configuration, adapter world-time addition, physical dt/fields/events and gain/force arithmetic unchanged. | Compile the existing declared seconds into validated native-boundary indices; use indices for stage ownership, hold end, remainder and case stop. Separately check physical timestamps against the same float recurrence from the immutable initial origin. No clock rewriting or widened universal event tolerance. Serialized physical time/index can remain; any new derived cache must be reconstructible and non-authoritative. Legacy records stay bound to old apparatus. | Requires shared semantics at all call sites, exact old short controls, late ordinary/malformed decisions, terminal exception, save/load/journal continuity and unsupported-stage rejection. A recurrence reference can be cached using scalar arithmetic only; do not recompute it quadratically on every guard or silently persist an unverified anchor. No prototype production change was made here. |

The reason to prefer D is **preservation of causal/numerical state and strict authority ownership**, not convenience. It avoids both a new physical clock and a global enlargement of the deadline acceptance band. It is more than deleting one assertion, but addresses both demonstrated failure sites and their restart consumers coherently. A carefully proved apparatus-only error-envelope solution remains a viable alternative for Jason to consider; this review does not declare it impossible.

## 9. Exact requirements for the recommended closure

1. **Maintain two meanings explicitly.** The native index owns discrete scheduling; the existing accumulated timestamp remains the continuous absolute world/record clock. A derived scheduling coordinate must not overwrite engine time, retime mover/chemistry, or become a new P input.
2. **Retain clock integrity.** For full nonterminal steps, compare recorded time with the deterministic recurrence starting at the immutable manifest origin, using the existing narrow comparison tolerance. A cached recurrence reference is scalar metadata, not another world. It must be reproducible from pinned runtime/dt/origin/count. Keep the partial-terminal interval exception explicit; never force a terminal time onto a full native endpoint.
3. **Bind deadlines once without permissive rounding.** The A5 native deadlines are exact integers already. Accept only a justified representation of an intended native boundary within the existing declared admission rule. Do not round a genuinely incompatible deadline into a legal route. Preserve rejection of a full hold crossing an interior boundary, including the 0.05/0.15 examples. Preserve the independently allowed seven-step final global hold.
4. **Use one interpretation everywhere.** New-command stage selection and final stopping; `pending.decision_stage` and expected-command recomputation; integer progress/remainder; stage/case hold bounds; runner remaining/stop logic; save/load/resume and journal checks must agree. Do not trust a mutable saved cursor. Do not supply physical-time inputs to one controller calculation and an inconsistent scheduling time to its verifier.
5. **Preserve versioned history.** Do not mutate old grants, files, timestamps or replay inputs. The exact authority identity necessarily changes with apparatus code. Reading older artifacts with their original verifier remains valid; cross-version continuation is not implicitly permitted.

No closure implementation is supplied. The arithmetic oracle only demonstrates that all **6,300 prescribed A5 full holds** fit their stage/case native indices, and that scalar recurrence checks can retain a `1e-10` consistency threshold without rejecting legitimate late timestamps. It does not establish that a not-yet-written correction satisfies every requirement above.

## 10. Tests required before a new apparatus checkpoint

These are prospective correction acceptance requirements, **not execution permission from this diagnosis**:

| Test class | Required evidence |
|---|---|
| Exact defect / consequential controls | Current code reaches the named rejection at 26,950 and the independent 270-second stage failure. Corrected code admits the lawful clock schedule. Reinstating each old faulty rule must reproduce its own failure; do not let an earlier unrelated assertion mask the intended check. |
| Entire admitted scalar domain | From immutable zero and representative supported nonzero origins, evaluate every native/command boundary through 630 and 1,200 seconds without a world. Include 128/256/512/1024 exponent regions, all A5 deadlines and exact/adjacent represented values. |
| Deadline authority | Preserve next-stage ownership, expired-final refusal, no full hold crossing an interior deadline, seven-step global shortening, no extra native step/hold, zero/negative/unsupported durations and clearly-not-due controls including `.1-2e-10`. |
| Clock/progress corruption | Wrong native index/time, one-step displacement, inconsistent origin, altered pair/count/decision/cursor, stale positive remainder and changed stage/case identity reject before output or causal advance. A long-clock representation allowance must not forgive a real extra native step. |
| Pause/resume and journal | Detached long-clock states at progress 0/7/9/10 around 270/300/450/480/630; exact remainder and stage ownership after lossless serialization; immutable parent/origin binding; coherent saved corruption rejected. A later separately authorized short physical component suite should retain full continuous-versus-resumed equality and exact field/native counts. No long ecological run is needed to exercise the clock defect. |
| Terminal and physical preservation | Explicit partial-native terminal records at late absolute times; no final wave on partial terminal; unchanged physical dt/event tolerances and world-time sequence. Verify P/config/adapter causal bytes stay unchanged for candidate D. |
| Controller/authority binding | Same scheduling interpretation in live controller dispatch, decision metadata, expected-command validation and record checks; altered controller/route/runtime/hash rejected; old grants cannot authorize the new instrument. |
| Historical compatibility and complete regression | Retain old review fixtures/failures, six detached comparator tests, all 143 existing engineering cases under separately authorized bounded component scope, and saved A1–A4 identity/stage checks. Use matching original instruments for historical replay; no rerun/reinterpretation of commissioning. |

A new checkpoint should state the supported clock domain, the exact admission semantics for off-grid/near-boundary prescriptions, and how it handles a partial terminal. It should not use successful learning, source renewal, route completion or survival as an engineering pass condition.

## 11. Effect on A1–A4 evidence

No original record, route, grant, result or interpretation changes. Saved controller streams were hash-checked against their receipts, then their stored stage indices were compared with the independent native-deadline calculation. No controller commands were recalculated for these cases.

| Saved case | Commands inspected | Maximum stored command-clock discrepancy | Stage disagreements |
|---|---:|---:|---:|
| A1, 91.83-second observed prefix | 919 | 1.0061285138363019e-11 | 0 |
| A2, 180 seconds | 1,800 | 2.8563817977556027e-11 | 0 |
| A3, 210 seconds | 2,100 | 4.5929482439532876e-11 | 0 |
| A4-CROSS, 16 seconds | 160 | 2.948752353404416e-13 | 0 |
| A4-WAIT, 28 seconds | 280 | 1.55964130499342e-12 | 0 |
| A4-DETOUR, 32 seconds | 320 | 2.184918912462308e-12 | 0 |

Total: **5,579 saved decisions**, all below the current absolute-clock threshold, all with the expected stage. The three A4 cases have separate zero-time starts; their times must not be combined into one accumulated clock. A1's wall stop, A2's preserved reporting boundary flags, A3's contact interruptions/damage and all prior claim limits remain unchanged. These checks do not independently revalidate every physical ledger or establish P efficacy.

The earlier mechanical closure remains evidence that its scoped tests passed on `5f077481`. This diagnosis adds a longer-horizon incompatibility those tests did not cover. It does not erase the earlier corrections, turn prior valid cases into failures, or call A5 scientifically failed.

## 12. Stop statement

**No A5 execution occurred. No world, field, neural or prehistory step occurred. No A5 controller was invoked against a world. No production code, existing test, P module, configuration, controller gain, world law, A5 stage or initial state was modified. No grant or replacement authority object was prepared. No Git write, commit, push, PR or merge occurred.**

The only new work is this diagnosis, inert evidence reads, scalar/manufactured checks and new review artifacts. The existing short tests that evolve a world were not run; no physical replay or long-run convergence/efficacy test was performed. The held A5 object remains byte-identical at the hash above.

**Stop for Jason's decision on a separately bounded apparatus correction.**
