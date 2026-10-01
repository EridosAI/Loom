# A5 apparatus clock-scheduling correction

**Implemented for narrow correction review. No A5 execution or launch-fitness declaration.**

The apparatus now derives stage ownership, command cadence, hold boundaries and case deadlines from native indices. Physical time still follows the original world arithmetic and is checked separately for consistency. This removes both diagnosed false rejections without changing P, configuration, world laws, controller gains or the proposed A5 route.

The new local checkpoint and exact patch are recorded in the portable package's `CHECKPOINT.json` and `CLOCK_SCHEDULING_CORRECTION.patch`. Its parent is `5f07748102cb5eaa302569c87efbae095050e9fe`; P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. The branch is `build/p-clock-correction-20260926-01a0c405`, in the isolated code worktree:

`C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\worktrees\loom-p-clock-correction-20260926`

This is a worktree of the actual Loom repository at `C:\Users\Jason\Desktop\Eridos\Loom`, not an unexecuted cloud substitute. The old apparatus worktree and all preserved evidence remain unchanged. Python 3.13.5, NumPy 2.3.3, SciPy 1.16.2 and their full recorded runtime identity match the held proposal. Git 2.50.0.windows.1 and a harmless scoped read/write check were verified. No dependency installation occurred.

## Authority and source review

The exact current user instruction is included as `evidence/REQUEST.txt`. It authorizes this apparatus correction, the complete existing regression suites, new scheduling tests and a local checkpoint, while prohibiting A5 execution and replacement launch authority. This task follows that ruling rather than the earlier diagnosis-only boundary.

Read and preserved references include `A5_CLOCK_COMPATIBILITY_REVIEW.md`, `OPEN_ISSUE_A5_CLOCK.md`, `CLOCK_AUDIT.json`, the old apparatus/controller/pending implementation, its prior authority/clock/final-correction reviews, and the pause/resume and authority tests. Current workbench map/status register A5 as held. Shared workbench navigation and canon were not edited.

## Exact old failures and correction

| Finding | Old apparatus, directly reproduced before correction | Corrected behavior |
|---|---|---|
| A: first command-clock rejection | Native 26,950; physical time `269.4999999998999`; product reference `269.5`; discrepancy `-1.0010126061388291e-10`. `pending.validate_decision` raises `issued decision clock mismatch` at its fixed `1e-10` check. | The separate justified clock-consistency allowance accepts the legitimate accumulated value. Index 26,950 is an ordinary ten-step command boundary in stage 2. No additional command is inserted. |
| B: independent 270-second transition rejection | Native 27,000; physical time `269.99999999989944`. Old `time_due` retains stage 2, whose deadline is 270.0. Prospective hold end `270.09999999989947` triggers `command hold would cross prescribed stage boundary`. | Native 27,000 owns stage 3. Its fresh ten-step hold lies within that stage's native deadline. The physical clock is neither rounded nor reset. |

`evidence/OLD_FAILURES_RED.json` records the actual old predicate errors. Reproduction A used an inert decision/clock dictionary, not a launch manifest. Reproduction B extracted and evaluated the exact old runner guard with the old controller's detached generic inputs and the same deadlines, deliberately isolating it from the earlier absolute-clock rejection. No world or A5 initialization was used. The new tests exercise the corrected pending validator and independent stage ownership, and short late-clock manufactured runs exercise actual runner dispatch/resume at 270 seconds.

The new fault/control matrix also reinstates the old fixed allowance and old floating stage choice in isolated test processes. Both produce their intended RED; removal of each mutation gives GREEN. It separately proves that removing clock-corruption checks, rounding an off-grid deadline and allowing off-cadence decisions are detected.

## Implementation and scheduling contract

Read [NATIVE_INDEX_SCHEDULING_SPECIFICATION.md](NATIVE_INDEX_SCHEDULING_SPECIFICATION.md) for the exact admission, arithmetic, error bound and restart rules.

| Surface | Change |
|---|---|
| `clock.py` | New pure native-grid admission, stage/case boundaries, ten-step hold calculation and physical-clock consistency check. No state advancement or clock assignment. |
| `controllers.py` | Integer-only deadline predicate and pure stage selector. The third waypoint-call argument supplies the native decision context. Actuator arithmetic and gains remain unchanged. |
| `authority.py` | Validate derived boundaries and numerical domain before output; bind clock/selector source and live implementations into execution identity. |
| `pending.py` | Recompute issued stage from its native index; validate global clock consistency, exact progress/remainder and integer stage/case ownership. Preserve local elapsed and terminal checks. |
| `runner.py` | Integer remaining steps, command windows and deadline checks. Physical adapter invocation and native/field counters are unchanged. |
| `validators.py` | Integer administrative stop/ceiling and action lookup, plus clock cross-validation. Physical native/event reconstruction remains unchanged. |

No new manifest alias, mutable scheduling cache, gain, physical parameter or policy was introduced. Human-readable deadlines remain in the bound manifest and records. Off-grid declarations are rejected, including tiny decimal offsets; they are not rounded into a different prescription. The reviewed prohibition on shortening a hold at an interior stage remains; the existing shorter final global hold remains.

The physical-clock bound depends on binary64 summation error, elapsed native count and origin, rather than a fitted tolerance at the observed failure. It diagnoses corrupted timing and does not participate in stage selection. It leaves the physical event tolerance and continuous world clock untouched. Unsupported origins whose clock allowance reaches one quarter native interval are explicitly rejected.

## Verification

The sealed package includes complete suite logs, JUnit results, per-run source inventories and a 59-row RED/GREEN matrix. All 59 existing P tests remain byte-identical. The 84 existing apparatus test cases remain present; three test modules were adapted to the explicit native-clock controller argument. Their original authority, pending/restart and boundary fault purposes remain exercised. The old near-0.1 out-of-tolerance timestamp is now rejected as corrupted timing rather than selecting a stale stage. The two old clock fault injections explicitly restore physical-time ownership at the new interface; they are not silently counted as effective mutations when they no longer alter behavior.

There are 33 new test cases. They cover:

- All requested indices 26,949 / 26,950 / 26,951 / 26,999 / 27,000 / 27,001, with an independent integer interval oracle.
- Every native scheduling index through 63,000 and every one of the 6,300 prescribed full command holds; all stage boundaries 9,000 / 12,000 / 27,000 / 30,000 / 45,000 / 48,000 / 63,000. These are scalar/detached checks, not a 630-second world.
- Physical-clock accumulation through the 1,200-second admitted duration from zero and several nonzero manufactured origins; corrupt clocks, one-step mismatches, off-grid prescriptions, final refusal and the seven-step global case cap.
- Detached serialized pending states immediately before/at/after late boundaries and stale remainders/cursors; full snapshot/journal pause/resume in generic **0.3-second** manufactured components around 270 seconds, paused after 9/10/11 local steps.
- For those short physical components: exact continuous/resumed state equality, 30 field calls of 0.01 seconds, no duplicate native indices, exact three command indices, unchanged inactive neural/RNG state, correct body-wave sample count and zero external neural-wave records. Existing intact-P wave/noise/partial-terminal tests and update-fault pairs remain in the complete suite.
- Pure saved-record stage compatibility and live clock-implementation identity rejection before a recorder can be created.

The final complete suite passed both in the worktree (**176 passed in 124.27 seconds**) and from the byte-verified portable source copy (**176 passed in 121.02 seconds**). Exact results are in `evidence/REGRESSION_SUMMARY.json`; each run records unchanged code/test inventories. No successful behavior, survival, learning, energy economy or A5 source renewal is a pass gate.

Fault/control totals: 16 original apparatus pairs, 20 prior authority/clock correction pairs, 18 prior final authority/save-resume pairs and 5 new clock pairs: **59 pairs, all intended RED and GREEN**. Isolated mutations are test-only; no mutant is written into production modules. The original diagnosis, initial 84-case apparatus check and 33-case new-test check are retained separately from the final complete runs.

## Retrospective compatibility and preserved identities

| Original saved case | Decisions checked | Stage disagreements |
|---|---:|---:|
| A1 | 919 | 0 |
| A2 | 1,800 | 0 |
| A3 | 2,100 | 0 |
| A4-CROSS | 160 | 0 |
| A4-WAIT | 280 | 0 |
| A4-DETOUR | 320 | 0 |
| **Total** | **5,579** | **0** |

The compressed original command streams were verified against their receipts. Only stored clocks, indices, stage labels and bound prescription fields were supplied to the new pure stage selector. No old commands were recomputed, no trajectories replayed, and no evidence was rewritten. The portable package includes those original streams/receipts and the derived test rows for independent checking. This is compatibility evidence, not retroactive execution under the new apparatus.

P source identity remains `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`; configuration identity remains `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`. Hash comparisons preserve all P modules/tests, configuration, pinned requirements, runtime, controller gains and the complete external physical adapter. Consequently dt, body/world laws, field/physics updates, wave cadence and original physical-clock arithmetic were not edited. The final preservation receipt also checks the historical source/evidence inventory and unchanged held A5 hash.

## Held A5 and review boundary

Held proposal `88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6` remains byte-identical, has no grant, and binds the old apparatus. Static derivation of its 630-second stage indices succeeds under the corrected scheduler. This is **not a new launch object, execution permission, commissioning result or declaration of A5 fitness**. Its route, stages, initial state, horizon and laws were not changed.

Not tested: A5 world execution, its controller trajectory, source revisits/renewal/efficacy, long physical integration, new prehistory, other operating systems or runtimes, cross-version continuation of old records, resource projections for a future A5 run, or new UI behavior. Terminal fractional clock semantics were checked with detached late-clock inputs; existing physical terminal component tests remain unchanged. No scientific lifetime, cohort, tuning, sweep, extra commissioning case, push, PR, merge or vault Git write occurred.

**Stop for a narrow correction review.** Future A5 preparation must bind the reviewed new apparatus checkpoint and obtain a separate canonical authority hash and authorization. Neither the historical held hash nor this correction package authorizes a launch.
