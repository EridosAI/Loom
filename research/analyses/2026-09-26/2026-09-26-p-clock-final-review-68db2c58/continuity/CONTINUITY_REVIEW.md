# Physical clock, cadence and pause/resume — narrow review

**VERIFIED within the delivered fixtures: physical time is preserved, meaningful clock corruption rejects, and the reviewed pause/resume paths retain exact native progress. No directly material scheduling defect was exposed.** This contribution supports the root review's disposition; it does not grant A5 execution or prepare authority.

Reviewed correction `68db2c581f07200966d699a4f55a65f9b96df1e9` against `5f07748102cb5eaa302569c87efbae095050e9fe`, preserving P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Source references below are under `worktrees/loom-p-clock-correction-20260926/developmental_ecology/` in the shared workspace. The exact request, `A5_CLOCK_COMPATIBILITY_REVIEW.md`, `CLOCK_SCHEDULING_CORRECTION_REPORT.md`, `NATIVE_INDEX_SCHEDULING_SPECIFICATION.md`, runtime hunks and delivered clock/pause tests were read. Static held-A5 scheduling and A1–A4 history are separate reviewers' evidence.

## Direct continuity evidence

`check_continuity.py` independently reproduces the delivered generic 0.3-second manufactured component from `test_clock_scheduling.py:138–172`: initial time 269.9/index 26990, two generic points, stage boundary 270.0 and cap 270.2. It does not use A5 initialization, route or authority. Passive wrappers count unchanged adapter/field calls and compare every physical timestamp to an independent repeated-addition recurrence; no scheduling function is replaced.

| Pause in the delivered component | Stored physical time | Native index | Remaining hold | Last issued stage |
|---|---:|---:|---:|---:|
| One step before boundary (local 9) | 269.9899999999999 | 26999 | 1 | 0 |
| At boundary (local 10) | 269.9999999999999 | 27000 | 0 | 0 |
| After boundary / within next valid hold (local 11) | 270.0099999999999 | 27001 | 9 | 1 |

All three preserve the time's exact binary64 hexadecimal representation, native index and remainder through production save, load and `Run.resume`. The last-issued cursor at the completed boundary is correctly still 0 with no remainder; the next decision reconstructs stage 1 from index 27000. Each split path and its continuous control contains exactly native indices 26991–27020, **30 field calls of 0.01**, command indices **26990/27000/27010**, hold lengths **10/10/10**, two body-wave samples, no neural-wave records and unchanged inactive neural/RNG state. Each field endpoint equals the actual post-step physical timestamp. All nine first/resumed/continuous segment reconstructions pass.

Every final engine hash is `7d741d1131108cc3f88c1b0bbd22f32363726f098b634c2122649745b4d31441`. Actual final time remains **270.1999999999997**, hexadecimal `0x1.0e3333333332ep+8`, while the index reference is **270.2**. This directly falsifies an implementation that silently projects world time onto the scheduling grid. Split/continuous timestamp sequences and full engine endpoints are exactly equal.

The eleven delivered detached checkpoints (26999, 27000, 27001, 29999, 30000, 44999, 45000, 47999, 48000, 62999, 63000) separately preserve session/index/time through unchanged P pack → strict JSON → unpack. Valid issued-stage/remainder states pass; an extra remaining step, stale cursor, or time displaced by 0.01 rejects. Near 630, this is **detached serialization/preflight evidence**, not a physical world continuation or reconstructed injected history.

## Clock integrity and allowance

At the existing scalar recurrence values, index 26950 retains time `269.4999999998999`, index 27000 retains `269.99999999989944`, and index 63000 retains `629.9999999995721`. All are accepted without rewriting. Corresponding allowances are approximately `9.06471445e-10`, `9.09466272e-10`, and `4.50670256e-9` seconds. Displacing each by one native interval rejects with `physical/native clock mismatch`.

For the delivered detached decision cases at 26950 and 27000, a read-only Python call observer confirms that a 0.01-corrupted timestamp is rejected by `pending.validate_decision` **before either waypoint_stage or waypoint_command is invoked**. The decision input dictionary remains unchanged. The mismatch therefore cannot silently select another stage.

The new bound is justified by the operation being checked, rather than fitted to the old failure. For $n$ additions of represented interval $d=\operatorname{fl}(0.01)$, binary64 unit roundoff $u=2^{-53}$ gives the conservative summation bound $\gamma_n(|t_0|+nd)$, where $\gamma_n=nu/(1-nu)$. The separately computed reference adds a multiplication/addition rounding error. Over the admitted $n\le120000$, the product magnitude is at most 1200, so its rounding error is below $1.14\times10^{-13}$ seconds. The retained $10^{-10}$ floor dominates that part even with cancellation; the additional two reference ULPs cover reference evaluation. The finite allowance must remain below a quarter native interval. For the actual zero-origin 630-second contract it is millions of times smaller than a 0.01 step.

`clock.py:52–82` implements this diagnostic reference/bound and the separate terminal interval. `controllers.py:14–17,63–75` chooses stage ownership exclusively from integer indices. `pending.py:45–61` validates physical consistency before computing a stage or accepted command. The bound neither feeds integer stage choice nor changes physical event tolerance.

## Terminal and causal preservation

The exact supplied late terminal fixture accepts time **629.9929999995721** at index 63000 only with terminal semantics. It remains fractional and distinct from the full endpoint `629.9999999995721`; nonterminal interpretation and a preceding full interval reject. This is a detached terminal consistency check, not a new terminal world run.

`SOURCE_PRESERVATION.json` verifies all 13 P source bytes against 6bc9683b; P/configuration and complete external adapter have empty committed diffs. P tests and pinned requirements are unchanged. Controller settings and retained actuator arithmetic are unchanged. AST comparison also confirms unchanged `Run.advance`, `hold` and `close`, and unchanged privileged input, actuator-pair validation and sensor payload functions. None of the six changed apparatus modules assigns an object's physical `time`.

The unchanged causal path is `adapter.py:68–79` → physics with the actual time, field integration at actual `e.time+dt`, then `e.time += dt`. `adapter.py:94–115` and `loom_p/engine.py:76–100` retain native increment, terminal bisection/rollback and no handoff on a terminal step. `validators.py:43–53` still reconstructs timestamps by adding recorded physical elapsed durations. It adds an index/clock cross-check, without replacing those times. The unchanged configuration retains native dt **0.01**, wave dt **0.2 / 20 native steps**, motor-noise refresh **0.5 / 50 native steps**, and event tolerance **1e-10**. Commands retain ten native steps except the previously permitted shorter final global hold. Full intact/fixed/terminal regressions are root-owned; the independently executed late physical cases here are external-controller fixtures with inactive neural state.

## Relevant prior coverage and limits

The directly relevant prior evidence read was `exports/2026-09-25-p-final-mechanical-closure-5f077481/pending/PENDING_MECHANICAL_CLOSURE.md`, supported by that review's `LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md` and `controller/CONTROLLER_CLOSURE_REVIEW.md`. It documents ordinary seven-plus-three continuation, exact zero-remainder transition, physical endpoint equality and rejection of the original seven-plus-four overrun. The later `exports/2026-09-26-A5-clock-compatibility-review-5f077481/A5_CLOCK_COMPATIBILITY_REVIEW.md` explicitly limits those old short-clock observations and diagnoses the two longer-clock failures.

Source comparison confirms that `test_boundary_resume_counts_and_absolute_cap` (pauses 7 and 10), `test_resume_binding_and_stage_transition` (7+3), `test_final_boundary_resume_cannot_gain_hold`, the three-mode pause/reconstruction test, native/wave/noise schedule test and partial-terminal/no-handoff test retain their function bodies. Their modules have the disclosed interface adaptations elsewhere; this report does not call every old apparatus file byte-identical. Root's complete current regression covers these ordinary cases alongside the new late fixtures.

One reviewer source-audit setup assertion initially included the intentionally replaced stage-selection loop in its actuator-arithmetic slice. `check_source_preservation_attempt001.py` and `SOURCE_PRESERVATION.log` preserve that failure. The comparator was corrected to exclude that explicitly reviewed scheduling loop; the actuator math comparison and all subsequent preservation checks pass in `SOURCE_PRESERVATION_002.log`/`_003.log`. No production code was changed.

Evidence is `CONTINUITY.log`, `fixtures-thz3cgf5/RESULT.json` and its new component records, `SOURCE_PRESERVATION.json`, and the reproduction scripts. All writes are confined to this new review directory. No A5 world/command, new authority, new prehistory, long physical trajectory, target/old-export/Workbench/Git mutation or broad adversarial search occurred.
