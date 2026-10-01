# Independent native scheduling closure

**VERIFIED: both original clock blockers are closed, and the actual held A5 schedule is representable through its final native index.** No directly material scheduling defect was found within this narrow scalar review. The overall final disposition also depends on the separately reviewed physical/pause, historical, regression and provenance evidence.

Reviewed corrected `68db2c581f07200966d699a4f55a65f9b96df1e9` against original `5f07748102cb5eaa302569c87efbae095050e9fe`. P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Held A5 hash `88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6` was treated only as inert data, read unchanged, and is not execution authority.

## Scope and sources

Read the complete final-review request, prior `A5_CLOCK_COMPATIBILITY_REVIEW.md`, `CLOCK_SCHEDULING_CORRECTION_REPORT.md`, `NATIVE_INDEX_SCHEDULING_SPECIFICATION.md`, the exact portable patch's six production-file sections, current clock/controller/pending/runner paths and the delivered clock tests. The patch changes native scheduling/clock validation and its callers; it does not edit the physical adapter or actuator equations/gains. Root review covers every non-production changed hunk, complete package provenance, suites and fault matrix.

`check_schedule.py` imports the actual old or new modules in separate pinned Python processes. The old module path is the original Desktop apparatus worktree; the new path is `worktrees/loom-p-clock-correction-20260926/developmental_ecology`. Imported paths and SHA-256s are in the results. A call-profile fence rejects Engine/Run construction, native/field/neural/random operations, prehistory, physical-state observation and all `waypoint_command` calls. No blocked call occurred. No command was computed against an A5 world, and no world or Run was constructed. Scalar `time += .01` values have no associated body/field/neural state.

The independent scheduling oracle uses 80-digit Decimal arithmetic to derive native endpoints from the held JSON deadline values, then Python integer ranges and `bisect_right` for half-open stage ownership. It does not call the production deadline predicate to construct expected stages or hold indices.

## Two genuine old failures

| Failure | Fresh old result | Corrected result |
|---|---|---|
| A: native 26,950 | Physical time `269.4999999998999`, nominal `269.5`, discrepancy `-1.0010126061388291e-10`. Unmodified old `pending.validate_decision` raises `issued decision clock mismatch` at `pending.py:44`. | `clock.validate_physical_time` accepts the unchanged physical value. The held-manifest prefix reaches its deliberately invalid downstream-input sentinel instead; the complete generic detached manual decision passes. |
| B: 270-second stage transition | At native 27,000, physical time `269.99999999989944`, the original stage loop retains zero-based stage 2. Its prospective end `270.09999999989947` fails the exact old runner crossing guard at `runner.py:174`. | Native 27,000 selects stage 3. The exact new runner crossing guard accepts hold end 27,010 against stage end 30,000. |

Failure A uses the unchanged held manifest and a schema/identity/clock-correct prefix with intentionally invalid `inputs={}`. At old native 26,940 this reaches `forbidden controller input`; at 26,950 it fails earlier at the clock check. This is a branch-isolation control, not a fabricated valid A5 state or a launch decision. A separate complete, unlaunchable manufactured manual-input dictionary confirms old rejection/new acceptance of the same clock without any waypoint command calculation or authority creation.

Failure B is independent: the harness parses and executes only the original controller's exact stage-selection `while` node and the original runner's exact crossing `require` expression. It does not invoke the earlier pending clock guard, execute actuator arithmetic or replace any production predicate. Source line and exact expression are recorded. Consequently A cannot mask B.

The two old processes each exit **1 at their intended assertion**, respectively `OLD A RED` and `OLD B RED`. Their actual predicate exceptions precede those assertions in the saved results. The corrected process exits **0**. These are fresh reproductions rather than inherited builder receipts, disabled assertions or setup failures.

Evidence: `old-a.log`, `old-a-results.json`, `old-b.log`, `old-b-results.json`, `new.log`, `new-results.json`.

## Required nearby boundaries

Stages are zero-based. A zero in the new-hold column means a new decision is refused there; an already issued valid hold may be partway through its steps.

| Native index | Nominal seconds | Unchanged scalar physical time | Stage | New hold steps |
|---:|---:|---:|---:|---:|
| 26,949 | 269.49 | 269.4899999998999 | 2 | 0 |
| 26,950 | 269.50 | 269.4999999998999 | 2 | 10 |
| 26,951 | 269.51 | 269.5099999998999 | 2 | 0 |
| 26,999 | 269.99 | 269.98999999989945 | 2 | 0 |
| 27,000 | 270.00 | 269.99999999989944 | 3 | 10 |
| 27,001 | 270.01 | 270.00999999989943 | 3 | 0 |

No representative off-cadence index acquires a new hold, and both legal ten-step decision indices retain theirs. At 27,000 stage ownership changes despite the unchanged physical timestamp being slightly below 270.

## Every actual A5 boundary and hold

The actual held deadlines are 90, 120, 270, 300, 450, 480 and 630 seconds. Independent exact conversion gives native boundaries 9,000, 12,000, 27,000, 30,000, 45,000, 48,000 and 63,000. Each boundary was checked immediately before and at it, and immediately after where that remains inside A5. No out-of-scope index 63,001 was tested.

| Boundary index | Physical time at boundary | Stage at boundary | New hold steps |
|---:|---:|---:|---:|
| 9,000 | 90.00000000000914 | 1 | 10 |
| 12,000 | 120.00000000002449 | 2 | 10 |
| 27,000 | 269.99999999989944 | 3 | 10 |
| 30,000 | 299.99999999987216 | 4 | 10 |
| 45,000 | 449.99999999973573 | 5 | 10 |
| 48,000 | 479.99999999970845 | 6 | 10 |
| 63,000 | 629.9999999995721 | 6, final label only | 0; case complete |

All **63,001 native indices from 0 through 63,000** agree with the independent stage oracle and pass physical-time consistency for the scalar recurrence. All **6,300 full holds** are exactly the start/end transitions `0→10`, `10→20`, …, `62990→63000`, covering native updates 1 through 63,000 once each. Every hold passes the exact new runner crossing expression and stays within both its selected stage and the original case end. Per-stage hold counts are **900, 300, 1,500, 300, 1,500, 300, 1,500**. There are zero stage disagreements or crossing failures. The final index refuses a new hold.

`STATIC_A5_HOLDS.json` retains every checked interval, its selected stage and original scalar physical timestamp. It is an inert schedule table, not an executable route, command stream, authority object or run output. This proves that the prescribed schedule loses/gains no hold. Source inspection ties live stage selection and pending validation to the same native context; actual fresh-command/pending-state execution is covered by the separate bounded component review, not by pretending this static table contains computed A5 actuator values.

## Clock separation and integrity

The new allowance is a diagnostic bound for repeated binary64 addition, not a wider stage-transition tolerance. `clock.py:55–70` uses the nonnegative accumulated error term `gamma_n*(abs(initial_time)+n*.01)`, the existing `1e-10` consistency floor and two ULPs of the separately evaluated reference. For A5's zero origin and 63,000 additions, this is conservative relative to the actual scalar error observed. Native stage functions have no physical-time argument, so acceptance of ordinary clock drift cannot select an earlier/later stage.

At 26,950 the allowance is `9.06471445182947e-10`; at 63,000 it is `4.50670255844351e-9`. The maximum observed absolute accumulation drift through A5 is `4.2791725718416274e-10`; the maximum drift/allowance ratio over the checked indices is `0.1187446309249412`. A deliberately wrong physical timestamp displaced by `.01` at indices 26,950, 27,000 and 63,000 is rejected with `physical/native clock mismatch`. The native-selected stage remains the same in those checks; corruption is not used to choose another stage.

The full scalar timestamp sequence's hexadecimal representations have identical before/after hashes. In particular the final value remains `629.9999999995721`, not `630.0`. The held manifest and held authority-object bytes also retain their pre-check hashes. The maximum local ten-step elapsed discrepancy over all A5 holds is only `1.1368683772161603e-13`, preserving the unchanged narrow local pending-time check's applicability to this scalar schedule.

The adapter is byte-identical in both imported sources: SHA-256 `ded81ad92bba426580ae4e9609fb95211aedf92a51fe19a63d05003970972aee`. The changed hunks contain no assignment of an index-derived value to engine time. Physical fields/events/terminal behavior were not executed in this subreview; their preservation and bounded physical tests are reported separately. The arithmetic schedule has exactly 3,150 native-modulo-20 opportunities, not a claim that A5 neural waves were executed. No field/native/RNG operation was called here.

## Source mapping and limits

Paths are under the corrected worktree's `developmental_ecology/loom_commissioning/`.

| Source | Relevant closure |
|---|---|
| `clock.py:7–48` | Exact declared-grid admission, native case/stage endpoints, index decision context and ten-step/final-global hold length. |
| `clock.py:51–82` | Separate physical-time reference/allowance; finite precision guard and explicit terminal interval branch; no clock mutation. |
| `controllers.py:14–17,63–75,78–100` | Integer-only due predicate and stage selector; waypoint context uses native index while its existing actuator arithmetic remains unchanged. |
| `pending.py:29–61` | Issued-stage selection, expected-command recomputation, clock consistency and hold/stage ends all use the same native context. |
| `pending.py:64–90` | Live pending state checks physical clock separately and bounds remaining steps by native case/stage indices. Local elapsed and partial-terminal checks remain. |
| `runner.py:148–175,182–185` | Remaining count, new hold ownership, stage crossing and recorded issued context use native indices; record `time` remains `engine.time`. |
| `validators.py:13–26,42–52,103–108` | Administrative stop/native ceiling checks are index based; recorded physical elapsed reconstruction remains; replay locates actions by native index. |
| `authority.py:93–108,160–166` | Scheduling implementations enter execution identity; exact derived boundaries and clock domain are checked before output. |

The new `clock.py` SHA-256 is `2fa876c7ff2a0b1e704da009bf23300e046105512ab9d104a885ceb213e658b2`; all seven examined old/new source hashes are in the result files. Old/new runtime imports were checked against their requested directories. Checkpoint/patch/Git and full artifact preservation are independently handled by the provenance subreview.

No generalized scheduler audit, off-schedule numeric search, physical A5 command calculation, new prehistory, ecological trajectory, authority generation, code edit, target/old-export/Workbench write, Git write or remote action occurred. No conclusions about A5 ecological success, route competence, learning or source renewal are implied. Historical A1–A4 reassignment counts and actual pause/cadence tests are deliberately left to their assigned independent reviews rather than duplicated here.

## Reproduction commands

Executed from the shared workspace with `PYTHONDONTWRITEBYTECODE=1`, using the pinned existing interpreter:

```powershell
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-26-p-clock-final-review-68db2c58\scheduling\check_schedule.py' old-a
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-26-p-clock-final-review-68db2c58\scheduling\check_schedule.py' old-b
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-26-p-clock-final-review-68db2c58\scheduling\check_schedule.py' new
```

Observed Python exits are **1 / 1 / 0**, at the expected old assertions and completed new checks. `COMMAND_RECEIPTS.json` records the commands and source/script identity. The script uses exclusive output creation; repeat in a new review directory rather than overwriting these results. No earlier failed harness attempt occurred in this subreview.
