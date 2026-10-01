# Loom P — narrow final clock review

**FIT FOR A5 LAUNCH-PACKET REGENERATION**

Review date: 2026-09-26. Corrected apparatus: `68db2c581f07200966d699a4f55a65f9b96df1e9`. Historical apparatus: `5f07748102cb5eaa302569c87efbae095050e9fe`. P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.

The correction closes both demonstrated clock failures. Scheduling now uses native indices while physical time retains its original accumulated representation. Independent checks find no missing or extra hold in the actual held 630-second schedule, no changed historical stage assignment, and no regression in the delivered authority or pause/resume protections. This is the requested narrow mechanical disposition. No A5 execution, new A5 authority, launch-packet regeneration, production edit, Git write or Workbench/canon change occurred in this review.

## Concise closure table

| Requirement | Independently reproduced evidence | Result |
|---|---|---|
| Original failure A | Old pending validator rejects native 26,950 / `269.4999999998999`; corrected validator accepts the complete detached generic decision. Separate old rejection expectation exits 1. | Closed |
| Original failure B | Old stage loop selects stage 2 at native 27,000; the exact old runner crossing guard rejects. Corrected selector selects stage 3 and the exact new guard accepts. Independent old expectation exits 1. | Closed |
| Boundaries and static A5 | All 63,001 indices and 6,300 prescribed holds checked against an independent integer oracle; zero disagreements or crossing failures; final index 63,000 refuses another hold. | Verified |
| Physical time and laws | P/configuration/adapter bytes unchanged; actual short components retain `time += .01`, exact field endpoints and stored float bits; late terminal fraction remains fractional. | Verified |
| Cadences and restart | Three delivered 0.3-second components, pauses at local 9/10/11; exact continuous/resumed final states; 11 detached late pending states; stale counts/cursors and meaningful clock errors reject. Existing mid-hold and wave/RNG tests remain green. | Verified |
| Historical compatibility | Original hash-verified A1–A4 streams: 5,579 saved decisions, zero stage disagreements. No historical command recomputation or trajectory replay. | Verified |
| Regression | Worktree **176 passed in 134.94s**; extracted portable **176 passed in 134.94s**. All **59 RED/GREEN pairs**, 118 logs, reach their intended exception/control. | Verified |
| Scope and preservation | Exact 14-file apparatus/test/evidence diff; unchanged P, gains, routes, dt and world laws; historical and held evidence hashes preserved. | Verified |
| Execution boundary | Held proposal remains ungranted and bound to the old instrument. No A5 world or replacement authority was created. | Preserved |

## Scope, sources and exact identities

The controlling request is preserved as `references/NARROW_FINAL_REVIEW_REQUEST.txt`. The review read `A5_CLOCK_COMPATIBILITY_REVIEW.md`, `CLOCK_SCHEDULING_CORRECTION_REPORT.md`, `NATIVE_INDEX_SCHEDULING_SPECIFICATION.md`, the complete exact diff, delivered tests and fault scripts, and the directly relevant prior `LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md` pause/resume evidence. Builder assertions were treated as claims to reproduce.

The corrected worktree is `C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\worktrees\loom-p-clock-correction-20260926`, branch `build/p-clock-correction-20260926-01a0c405`. It is the direct child of the historical apparatus checkpoint, with P as an ancestor. The pinned runtime is the existing P engineering environment: CPython 3.13.5, NumPy 2.3.3, SciPy 1.16.2 and pytest 8.4.2. No dependency installation occurred.

The exact binary diff is **220,445 bytes**, SHA-256 `07b345f7ce95edc4ddf3d1edba662a416c0314c928640d1133e37edc13075714`: **14 files, 545 insertions, 61 deletions**. It matches the portable patch and Git objects. Every changed hunk was reviewed:

| Changed surface | Complete hunk assessment |
|---|---|
| `authority.py` | Binds selector and clock source/live functions; admits exact native boundaries and supported clock precision before output. |
| New `clock.py` | Pure grid admission, case/stage indices, decision cadence and separate physical-clock consistency envelope. No physical state assignment or advancement. |
| `controllers.py` | Replaces floating deadline classification with integer comparison and pure stage ownership; updates the call argument. Gain and actuator arithmetic are unchanged. |
| `pending.py` | Uses issued/current native indices for decision, hold and stage authority; adds physical-clock consistency; retains local elapsed, decision seal, cursor, progress and remainder checks. |
| `runner.py` | Integer remaining/case guards, decision context, crossing rule and metadata. Existing physical adapter calls remain unchanged. |
| `validators.py` | Integer stop/deadline and action lookup; separate physical-clock validation. Existing per-record physical elapsed accumulation and event reconstruction remain. |
| Three existing apparatus test modules | Adapt calls to native decision context. Both earlier clock faults still deliberately restore floating-time ownership. The old out-of-band timestamp is now rejected as corrupt instead of selecting a stale stage. |
| New `test_clock_scheduling.py` and `verify_clock_scheduling.py` | 33 delivered clock cases and five isolated fault/control pairs. Actual world fixtures are generic short components; scalar and detached checks are distinguished below. |
| New `clock_retrospective.json` | Derived saved-stage fixture checked against the original records, independently of its passing test. |
| Two new correction documents | Scheduling specification and builder evidence report; their consequential claims are checked here. |

Paths in this table are under `developmental_ecology/`, except the two documents under `docs/developmental_ecology/p_clock_correction_20260926/`. No P/world/scientific setting changed. The P aggregate remains `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`; configuration semantic identity remains `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`, with checkout SHA-256 `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9`. Corrected apparatus aggregate: `aaaac00790800d220589215d4d94b079bc4a9840a4d90b2c43be4196b204d2cf`. Exact component hashes are retained in the provenance receipts.

## Exact original REDs and corrected GREENs

**A — absolute clock rejection.** A separate process imported the actual old checkout. Repeated scalar `.01` additions produce index 26,950 time `269.4999999998999`, hex `0x1.0d7fffffff91fp+8`, versus the nominal product `269.5`: difference `-1.0010126061388291e-10`. Old `pending.validate_decision` rejects with `issued decision clock mismatch`. Index 26,940 passes that guard and reaches a deliberately invalid downstream input sentinel, proving which branch rejects. A complete detached generic manual decision also rejects at 26,950. The old lawful-clock expectation then exits 1 with `OLD A RED`.

On the corrected source, the same accumulated clock passes the physical consistency guard and reaches the later sentinel; the complete detached generic decision is accepted. This avoids inventing an A5 body or command. The delivered `old-absolute` mutation separately restores the fixed `1e-10` rule and reaches its intended RED; removing the mutation passes.

**B — independent stage transition.** A second old process executes the exact stage-selection loop extracted from the old controller source and the exact crossing expression extracted from the old runner. At native 27,000 / physical `269.99999999989944`, it selects zero-based stage 2. Prospective end `270.09999999989947` exceeds that stage's deadline 270.0; the real old crossing expression raises `command hold would cross prescribed stage boundary`. The earlier pending clock guard is not invoked, so A cannot mask B. The correct-transition expectation exits 1 with `OLD B RED`.

The new pure selector assigns index 27,000 to stage 3; its ten-step hold ends at 27,010, below that stage's 30,000 endpoint, and the exact new runner guard accepts. The delivered `old-stage` mutation independently restores floating stage selection and fails `STAGE OWNERSHIP BREACH`. These branch-isolation checks do not invoke a waypoint command, construct an A5 world, or advance a trajectory. Read-only call profiling fences those operations. Exact scripts, tracebacks, source hashes and exit meanings are in `scheduling/`.

## Native boundaries and the actual held 630-second schedule

The held packet is inert input. Its exact proposal hash remains `88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6`; `execution_authority` is null. An independent 80-digit Decimal conversion and integer/bisect interval oracle derive the schedule without using the production deadline comparison.

| Nominal seconds | Native index | Expected and actual stage, zero-based | New hold permitted |
|---:|---:|---:|---|
| 269.49 | 26,949 | 2 | No; mid-hold |
| 269.50 | 26,950 | 2 | Yes; 10 steps |
| 269.51 | 26,951 | 2 | No; mid-hold |
| 269.99 | 26,999 | 2 | No; mid-hold |
| 270.00 | 27,000 | 3 | Yes; 10 steps |
| 270.01 | 27,001 | 3 | No; mid-hold |

| Stage | Native interval | Declared end, seconds | Legal holds |
|---:|---|---:|---:|
| 0 | [0, 9,000) | 90 | 900 |
| 1 | [9,000, 12,000) | 120 | 300 |
| 2 | [12,000, 27,000) | 270 | 1,500 |
| 3 | [27,000, 30,000) | 300 | 300 |
| 4 | [30,000, 45,000) | 450 | 1,500 |
| 5 | [45,000, 48,000) | 480 | 300 |
| 6 | [48,000, 63,000) | 630 | 1,500 |
| Total | 63,000 native intervals | 630 | 6,300 |

Every native index 0–63,000, every permitted hold, and each stage's immediately preceding/at/following index within the actual schedule agree with the oracle. Holds start exactly at `range(0,63000,10)` and end at `range(10,63001,10)`. None crosses its stage/case endpoint. At the final endpoint the diagnostic selector retains the last label, but a new hold is rejected: that label cannot confer further authority. `STATIC_A5_HOLDS.json` enumerates all 6,300 results. No A5 command was computed against a world.

## Physical time, consistency and cadences

The unchanged physical adapter still uses `e.time += dt`. Native index owns scheduling only. The helper validates JSON decimal spellings with exact fractions, rejects off-grid declarations instead of rounding them, and never converts accumulated physical timestamps into deadlines. Full holds remain ten native steps; an incompatible interior crossing rejects; the existing shorter final global hold remains supported.

The consistency envelope uses the binary64 summation bound. With $u=2^{-53}$, $n$ native increments from the immutable origin, and $\gamma_n=nu/(1-nu)$, the implemented allowance is:

$$
B=10^{-10}+\gamma_n\bigl(|t_0|+n\,\mathrm{fl}(0.01)\bigr)+2\,\mathrm{ulp}(t_{\mathrm{reference}}).
$$

This bounds rounding from repeated additions and the separately evaluated reference, with the existing consistency floor. Over the admitted progress range the multiplication error is below `1.14e-13`, covered by that floor even under cancellation; the reference ULP allowance also covers its final rounding. It is passive validation; it does not widen any physical event tolerance or choose a stage. The implementation caps relative progress at 120,000 steps and rejects unsupported origins if the allowance reaches 0.0025 seconds. The independent actual-A5 scan stays within 63,000; the delivered suite's additional admitted-domain scalar cases were run as requested, without adding a new numerical campaign.

At 26,950 the allowance is approximately `9.0647e-10`; at 63,000 it is `4.50670255844351e-9`. Maximum observed scalar drift through the actual schedule is `4.2791725718416274e-10`. All ordinary clocks pass unchanged. Deliberate `.01` clock errors at 26,950, 27,000 and 63,000 reject; the instrumented pending checks reject before any stage/command selector call. They cannot silently choose a different stage to explain a bad clock.

Three independently instrumented delivered generic components start at 269.9/index 26,990 and run only 0.3 seconds. Each split and continuous path has exactly 30 native records and 30 field calls with dt `.01`; field endpoints equal the actual accumulated clock. Command indices are 26,990, 27,000, 27,010, each with ten steps. Final time is **`270.1999999999997`**, while the index reference is 270.2. Exact final state hash for all paths is `7d741d1131108cc3f88c1b0bbd22f32363726f098b634c2122649745b4d31441`. This directly distinguishes preserving the physical clock from projecting it onto an index product.

Native dt `.01`, hold `.1`, wave `.2`/20 native steps, field update calls and RNG paths are unchanged in source. The short external components retain exact inactive organism/RNG state, no neural-wave record and two body-wave samples. Existing intact-P wave/noise, terminal and extra-native/wave/field/random fault cases all pass. There are 3,150 modulo-20 opportunities in the static A5 schedule; this is arithmetic evidence, not 3,150 executed A5 neural handoffs. No full 630-second world or field integration is claimed.

Physics, contact/event laws and terminal handling are byte-preserved. A detached late terminal at native 63,000 with physical time `times[62999] + .003` is accepted as fractional terminal progress, rejected as a full nonterminal endpoint, and remains unrounded. A time from the previous full interval is rejected. Existing physical terminal/contact component tests supply the retained physical coverage; this review adds no late A5 collision or terminal trajectory.

## Pause/resume and authority

Actual close/load/resume was exercised at local steps 9, 10 and 11 of the short component: one step before, exactly at, and one step after the 270-second native boundary. Original manifest origin, native index, physical float bits, held pair, last-issued stage and remaining count survive exactly. Continuous/resumed complete state hashes and physical timestamp sequences agree, and all saved segments reconstruct with the delivered verifier. Ordinary mid-hold persistence and previous pair/remainder/journal/dispatch negatives remain covered by the full suite and delivered fault matrices.

Eleven detached late pending states at indices 26,999 / 27,000 / 27,001 / 29,999 / 30,000 / 44,999 / 45,000 / 47,999 / 48,000 / 62,999 / 63,000 survive lossless serialization. An added remaining step, changed saved cursor, or meaningful physical-clock mismatch rejects. At a boundary, an exhausted last-issued stage label may be retained as history; the next stage is reconstructed from the current native index. A stale positive remainder cannot cross that authority. Near-630 evidence is explicitly detached serialization/validation, not an executed world restart.

Clock/selector source and live functions are bound into the new controller identity. The delivered clock-function substitution test rejects before Recorder creation; the original authority, actual dispatch, pending seal, loaded-session and journal protections remain green. Historical objects stay bound to the historical instrument. Neither this correction nor this review grants cross-version continuation or lets the held old proposal authorize the new instrument.

## A1–A4: original-record compatibility only

Original compressed command streams were read directly from the historical 5f apparatus artifact directories and checked against their original receipts. All 114 enumerated trajectory payloads retain receipt hashes. Only saved indices/times/stage labels and bound stage deadlines enter the new pure selector and a separately written Fraction/integer oracle. No old command is recomputed, no trajectory replayed and no record rewritten for this check.

| Original saved case | Decisions | Stage disagreements |
|---|---:|---:|
| A1 | 919 | 0 |
| A2 | 1,800 | 0 |
| A3 | 2,100 | 0 |
| A4-CROSS | 160 | 0 |
| A4-WAIT | 280 | 0 |
| A4-DETOUR | 320 | 0 |
| Total | **5,579** | **0** |

`provenance/RETROSPECTIVE.json` retains every comparison and its source identity. These cases were executed under **5f077481**, not 68db2c58. Their prior observed outcomes and interpretation limits remain unchanged; the three A4 clocks are separate origins. Passing compatibility does not retrospectively replace their apparatus identity or establish ecological efficacy.

## Complete regression, preservation and intake

Both independent full runs pass 176 tests in 134.94 seconds each. Collection confirms **59 unchanged P + 24 original apparatus + 30 prior correction + 30 final correction + 33 new clock cases**. The 84 existing apparatus cases remain present, with the disclosed interface adaptations in three files. No skipped/error result is used as a pass. The two identical reported times are the separate fresh pytest results, not copied builder timing.

All **16 + 20 + 18 + 5 = 59** delivered fault/control pairs reproduce. The audit reads actual exception lines and traceback frames in all 118 logs, rather than searching only echoed source text. Every RED child exits 1 and every GREEN child exits 0. The older transition fault is parameterized: two RED failures/three passes and five GREEN passes. The prior 18 authority negatives bypass their delivered test callback; they are not described as 18 production mutants. The later dispatch/pending/parser and new clock cases disable or replace their named checks. `FAULT_AND_SUITE_AUDIT.json` and `.md` retain exact commands, hashes, exception evidence and scope.

One independent source-comparison helper initially included the intentionally replaced stage loop in its actuator-arithmetic slice and failed its own comparison. Only that reviewer comparator was corrected; the old attempt and log remain under `continuity/`. The final source checks pass. This setup error is neither an apparatus failure nor an omitted failed test.

The original correction ZIP is **3,916,030 bytes**, SHA-256 `8c5e9322d06b4915ed31106770aff80e925666d961e389102c27a9ad4499e894`: 376 unique safe entries, all 375 manifest payload sizes/hashes and CRCs verified before extraction. The portable suite runs from that extracted source. Fifty-five target source/document files match the ZIP; the protected P/configuration/tests/requirements/adapter inventory matches old, new and portable representations. Historical EXP1–21 remains tree `f1b884a7ada4c806786d1530d76d446aac5d37b1`.

Preservation receipts compare the 250-file prior diagnosis inventory, original A1–A4 payloads, original saved-stage source anchors, and the held packet's 89 local and 89 delivered Workbench payloads. These overlapping inventories are not summed. The old and corrected checkouts remain at their exact commits with clean status. Final rehash results and the scoped authority/execution census are retained under `provenance/`. This review itself performs no A5 execution or authority creation; the enumerated delivered A5 evidence remains held. No assertion about hypothetical unrecorded activity elsewhere is needed.

The independent intake contains this report, the concise closure table, reproduction commands, reviewed identities, both original REDs, corrected boundary evidence, bounded continuity evidence, all 118 fault logs, preservation receipts, the exact patch and byte-identical builder ZIP. Its own manifest lists every included payload; the adjacent `INTAKE_RECEIPT.json` identifies the final archive after reopen, CRC and per-file hash verification. Expanded duplicate source and disposable pytest directories are excluded. The archive is prepared for Workbench intake; intake was not performed.

No directly material scheduling defect remains demonstrated within the requested contract. A5's ecological outcome, controller competence and long-run performance are outside this review. Work stops at **FIT FOR A5 LAUNCH-PACKET REGENERATION**. No packet regeneration or execution follows from this task.
