# EXP14 — CONVERSION DYNAMICS (horizon-extension arm) — PRE-REGISTRATION

**Status: FINALIZED — fork ruled (§3.1 → (i) screen-first) + adversarial panel folded (§11, 5/16 confirmed). Awaiting Jason's read + build-GO. Nothing builds or runs before GO.**

Lineage: EXP13 stage-one CLOSED, fork (a) ratified scoped (FRONTIER §10.21.7, PROJECT_STATE §12.E, commit d85970c). The completer **rides the marginal program-wide** (MEASURED, direct run-time `exam_acc`, cross-ledger); **split s0 (+3%, 7.5 SE, 27-window sustained) is the SOLE existence proof that the operator can leave the marginal.** The forward axis ruled: **CONVERSION DYNAMICS** — what regime lets the completer leave the marginal (dose / horizon / signal). Loss-engineering is **manufacturing-class FENCED** until we know what regime conversion lives in; this arm is the cheapest *measurement* of that regime, not an intervention on it.

---

## 0. Discipline traps (binding, carried from the handoff + the EXP12/13 record)

- **No new loss, no new force, one code path.** EXP14 reuses `EXP12Loop` / `run_exp12_arm` dynamics VERBATIM (step/losses/optimizer inherited, `_l_jepa` inert at W=1). The ONLY additions are (a) a longer horizon, (b) end-state checkpointing (the new contract), (c) a read-only density-matched conversion detector. Adding an observation column or a `.pt` save is measurement; it is not a mechanism change.
- **Manufacturing-class fence (G):** nothing here builds a gradient, schedule, or signal whose purpose is to pull the completer off the marginal. Conversion, if it appears, must arise through the *existing* dynamics at longer horizon / different dose — never because EXP14 engineered a path to it. If a proposed knob would make conversion the cheaper solution, it is out of scope and surfaced, not added.
- **Determinism contract:** seed + construction order + `torch.set_num_threads(1)`. The runner's interleaved reads (`dc_track`@BLOCK, `grad_geometry_split`, `_eval_column`) **couple into the trajectory** (§10.21.4, program-wide) — so EXP14 runs the **faithful runner** (`run_exp12_arm`'s exact read order), never a bare step-loop. Checkpointing is inert w.r.t. the trajectory (no RNG draw, no param touch), so it does not perturb determinism.
- **Verdict-seeds ≠ cal-seeds.** Cal {20–24} cut the constants; verdict {0–7} are never used for calibration.
- **Cells named before the run; the printed cell is a DRAFT** behind an adversarial verification pass before it reaches the table. Surprising results (a conversion) get adversarially verified before any verdict.
- **Records stand and get superseded; surface-recommend-stop; no silent patches.**

---

## 1. The question (stated once)

**Is conversion — the operator leaving the marginal on completion — reachable in a healthy existing regime at long horizon, and if so, what orders it: horizon, dose, or seed?**

Grounds: split s0 converted **late** (post-303k-class) under the **coin** dose, while every EXP13 cal and every other EXP12 run stopped at ≤160k / ≤303k with the completer at chance. The cheapest discriminating test of "conversion is slow dynamics" is to run healthy regimes **longer** and read conversion with a **rate-honest** detector.

This is a **screen**, not a mechanism claim: **any** conversion (either rung) triggers the clean deconfounding 2×2 (§3.1 pin 2); a negative result is a named finding about the horizon (§7, cell **none**).

---

## 2. The fabric & the dose ladder (grounded in the record)

The dose ladder (FRONTIER §10.20.3, three rungs; the third STRUCK):

| rung | exam policy | exemplar healthy arm | fabric |
|---|---|---|---|
| **scheduled** (strongest routing+channel) | onset word-mask guaranteed every dwell | `exp12_dwell` | **dwelled** |
| **coin** (~2–3× weaker) | position-1 word-mask by 50:50 coin | `exp12_split` | **shuffled** |
| ~~zero word-prediction load~~ | ~~word as pure reference~~ | ~~`exp12_12b*`~~ | STRUCK §10.20.3 (never binds) |

Coin policy also exists on the **dwelled** fabric as `exp12_12bc_dwp` (dwelled + `uniform_mask` + present word), and scheduled on the **shuffled** fabric as `exp12_shuffle`. So each fabric admits a clean, single-variable dose contrast:
- **dwelled dose axis:** `exp12_dwell` (scheduled) vs `exp12_12bc_dwp` (coin).
- **shuffled dose axis:** `exp12_shuffle` (scheduled) vs `exp12_split` (coin) ← **s0 lives here (coin-shuffled).**

---

## 3. Arms — screen-first (fork §3.1 RULED → (i))

**Primary (Jason's literal naming "scheduled=rig-1 dwell, coin=split"):** the two exemplar healthy rungs as named —
- **SCHEDULED rung:** `exp12_dwell` (dwelled fabric, scheduled onset exams).
- **COIN rung:** `exp12_split` (shuffled fabric, coin exams) — the s0 lineage.

× seeds **{0–7}** × horizon **500k** × checkpointed.

### 3.1 OPEN DECISION (fork) — the fabric confound (single-variable catch, surfaced not silently resolved)

The recommended pair differs in **BOTH** dose (scheduled vs coin) **AND** fabric (dwelled vs shuffled). So a **dose-ordered** result across these two arms is confounded with fabric — it cannot alone promote the "dose axis." Three resolutions, Jason's ruling owed at GO:

- **(i) SCREEN-FIRST (RULED — Jason, 2026-07-07):** run the literal pair as a *screen* — "does conversion appear at 500k anywhere on s0's own lineage?" The fabric covariate is a **flagged limitation**; **any conversion in EITHER rung triggers** the clean deconfounding 2×2 as the first escalation (see PINS below). Cheapest; matches the stated arm naming; keeps s0's lineage (split) in the primary; the "none" cell (§7) still lands honestly.
- **(ii) DECONFOUND-NOW, dwelled axis:** replace the coin rung with `exp12_12bc_dwp` → `exp12_dwell` vs `exp12_12bc_dwp`, both **dwelled**. Clean dose on the healthy scene-persistence fabric — but does **not** contain s0 (coin-dwelled never converted; a fresh cell), so the s0 existence-proof lineage is dropped from the primary. Would add `exp12_split` {0–7} as a named companion to keep the s0 lineage.
- **(iii) DECONFOUND-NOW, full 2×2:** {dwelled, shuffled} × {scheduled, coin} = `exp12_dwell`, `exp12_12bc_dwp`, `exp12_shuffle`, `exp12_split`, each {0–7}. Cleanest (dose clean within fabric, fabric clean within dose, contains s0), at 4 arms × 8 = 32 runs @ 500k.

**RULED: (i) screen-first (Jason, 2026-07-07).** The primary question is *does conversion happen at all beyond s0* — the screen answers that on s0's own lineage; dose-attribution only becomes worth 32 runs if something converts. Two binding PINS:

1. **Screen cells are SCREEN-GRADE.** Any dose-ordered pattern seen in the screen is **NAMED, never CLAIMED** — it is confounded with fabric by construction, so its *only* license is to **fire the 2×2**. No claim-ceiling drift: the screen never promotes a dose claim, it only decides whether the clean factorial runs.
2. **The 2×2 trigger is ANY-CONVERSION-IN-EITHER-RUNG — not dose-ordering.** Attribution needs the factorial regardless of *which* rung converts; ordering within a confounded pair does not gate the clean design. (So even a single-rung conversion, or an *un*-ordered both-rung conversion, fires the 2×2.)

*(The rest of this prereg — §4–§10 — is arm-set-agnostic; the fork changes only which rows populate the cell table.)*

---

## 4. The density-matched conversion band (the registered form, cut for real)

**Why rate-honesty matters.** `exam_acc` (per eval window) is the **mean over the exams that fell in that window**. Scheduled (~100% onset exams) and coin (~50%) rungs have different exams-per-window → different noise on the mean → a fixed threshold (the PROPOSED `exam_acc ≥ 0.6`, 2-consec) has a **different false-conversion rate per rung** (the "~4× hot at halved density" observation, progress_log 2026-07-05).

**Registered form (§13.6.iv, EXP12): own chance-band, sustained N consecutive windows — cut from the PRE-CONVERSION MARGINAL span, not the thin pre-acquisition span (panel fix F2/F3).** This matches how EXP12's stage-two band is *actually* cut (`exp12_stage2.py`: the null segment = windows with no conversion, which INCLUDES the large post-acquisition span where the operator rides the marginal program-wide). Cutting from the pre-*acquisition* span instead is unstable on the coin/shuffled rung, which acquires ~3.3k → only ~11 pre-acquisition windows/seed (~55 pooled) → a p99 that is near-max and single-window-dominated (the recorded n=89-thin problem, §10.20.3), and asymmetric vs the dwelled rung's hundreds. Per rung, cut at **stage-two on cal seeds {20–24}**:
- **Null span = post-acquisition, pre-conversion `exam_acc` windows** (the operator-at-chance segment), excluding any candidate conversion episode. `conv_band[rung]` = the high quantile (p99) of that span, **cross-checked against the parametric per-window `Binomial(exam_n, 0.5)` null** (density-matched by construction via each window's own `exam_n`, stable regardless of span length). On disagreement the wider (more conservative) band is used and the gap surfaced.
- `conv_consec[rung] = N` so the pre-conversion false-conversion rate ≤ a common small α across rungs (N ≥ 3, per §13.6.iv).
- **Stability guard (panel fix F3):** register a minimum pooled null-window floor `n_null ≥ N_NULL_MIN`; if a rung falls below it, **WIDEN the cal pool `{20–24}→{20–29}`** (adding slower-acquirer seeds, as EXP12 needed s26) BEFORE cutting — cut before the run, never on verdict seeds. Per-rung `n_null` is **reported at the surfacing gate** so the coin-vs-dwelled estimation asymmetry is visible before any verdict.
- `conversion_onset = first t` where `exam_acc ≥ conv_band[rung]` for `conv_consec[rung]` consecutive windows.
- **Cell count-cuts (panel fix F4) are pinned HERE too**, alongside the band, so §7's partition is fixed before the verdict read: `across-seeds ≥ 5/8`, `s0-class-lottery ∈ {1,2}/8`, `none = 0/8`, `ambiguous = {3,4}/8` (a registered state — §7).

**Surfaced before the verdict read.** ALL stage-two constants (per-rung band, `conv_consec`, `n_null`, count-cuts, rising-criterion) are reported to Jason before any verdict-seed conversion is interpreted. Stage-one logs raw `exam_acc` + the PROPOSED 0.6/2 band for the online checkpoint trigger only (§6).

**Content-real guard (panel-sharpened):** (a) the null band must sit **below** any genuine sustained conversion by a margin; (b) a seed's conversion must survive the *density-matched* band, not only the naive 0.6 (a 0.6-only conversion is an exam-rate false alarm, reported as such); (c) **s0-admission anchor** — because cal {20–24} may contain no converter to validate against, the cut coin band MUST admit split s0's already-measured level (sustained `exam_acc ≥ 0.704 × N`, FRONTIER §10.20.1) as a fixed anchor: a coin band that would reject s0 as a false alarm is over-cut and re-derived (widen pool / use the Binomial null).

---

## 5. Seeds, horizon, and the pre-registered extension rule

- **Seeds:** verdict **{0–7}** per rung (fresh; ≠ cal {20–24}). Note **seed 0 = the split-conversion seed index** — on the coin rung this is the regime-level read of "does s0 reproduce" (regime, not trajectory-faithfulness; that was declined).
- **Horizon & hard cap (panel fix F1):** both rungs' fabrics are **pre-built up front at `H_MAX` (pinned; default 1.0M steps)** — ONE fixed permutation over the full horizon for the shuffled/coin rung — and the run READS + checkpoints at **500k**. This is what makes extension faithful for the coin rung: the shuffled order is `randperm(T)`, therefore T-dependent, so a rebuild at larger T reshuffles the whole fabric (there is no faithful "next wave"); pre-building at `H_MAX` and stepping on the SAME perm is the only faithful extension. `H_MAX` is the hard compute cap. (500k comfortably past split s0's post-303k-class onset; `H_MAX` gives ~2× headroom.)
- **EXTENSION RULE (pre-registered NOW, binding):** past 500k, continue a run (on its already-built `H_MAX` fabric) **only if** its density-matched conversion-band curve is **still rising at the read point** (positive post-onset `exam_acc` slope above a noise floor cut from the cal-seed null slope) **AND a density-matched conversion has fired** (crossed §4's band) **but not plateaued**. At most **2 extensions/seed**, never past `H_MAX`. **Grounds recorded per extension.** Extension is **never** fired because a read disappoints: a flat/at-chance curve at 500k on an ACQUIRED seed is the **none** cell (§7), not a trigger. **The cell-deciding converter tally is FROZEN at the common 500k read** — extension only characterizes the plateau of an already-fired conversion; it can never promote a non-converter, so it cannot move a seed between §7 cells. The rising-criterion constants are cut at stage-two with the band.

---

## 6. The checkpoint contract (this arm honors it first — PROJECT_STATE §12.E)

Every EXP14 run saves its end-state:
- **`.pt` at the horizon** (500k or the extended horizon).
- **`.pt` at the conversion-onset event** — detected online via the PROPOSED band (0.6/2) as a *trigger* (cheap, liberal; the verdict uses the density-matched band post-hoc). The online trigger only decides *where to save*; it never decides the verdict.
- Saved state = `loop` params + `cfg` + `rng`/`gen` state + wave index. **Faithful-resume scope (panel fix F1):** resume/extension is faithful on the **dwelled** fabric unconditionally (its per-substream draws APPEND — a larger-T build reproduces the prefix); on the **shuffled/coin** fabric it is faithful ONLY because §5 pre-builds one fixed `H_MAX` permutation up front — a rebuild at larger T would reshuffle and is **FORBIDDEN**. Either way the checkpoint suffices to re-probe the operator read-only (the exact thing the §10.21.6 retro probe could not do). Checkpointing consumes no RNG and touches no param → trajectory-inert.

---

## 7. The four-cell inference table (named before the run; EXHAUSTIVE + EXCLUSIVE)

Read on the **density-matched** band (§4), per rung, over verdict seeds {0–7}, behind the adversarial verification pass. **Two pre-gates fire BEFORE the four-cell table:**

**Pre-gate A — READ floor (panel fix F5; ports EXP12 §13.9 pin ii).** `READ` = a seed that **ACQUIRED** (differentiated on num/den/asg_cat — NOT on exam_acc, so an unacquired flat curve is distinguishable from acquired-but-marginal). A rung with fewer than **`N_MIN` = 3** READ verdict seeds is **UNREAD-AT-HORIZON** → recorded **horizon re-pin** (or a Jason ruling that *acquisition*, not conversion, is the blocker) — it is **NOT** the `none` cell. So `none` is reachable ONLY when ≥ `N_MIN` seeds acquired and zero of them converted. *(For forks (ii)/(iii), `exp12_12bc_dwp`'s 500k acquisition must be established at stage-one cal before its read floor is meaningful.)*

**Pre-gate B — count partition (panel fix F4; cuts pinned in §4).** Over the READ seeds, per rung, the converter count maps to exactly one cell: **≥5/8 → across-seeds · {1,2}/8 → s0-class-lottery · 0/8 → none · {3,4}/8 → AMBIGUOUS** (a registered state, not a fall-through: surfaced to Jason — fire the extension pool / re-pin power, never force a cell).

| cell | signature (READ seeds, density-matched band) | reading | routing |
|---|---|---|---|
| **across-seeds** | ≥5/8 convert (a rung, or matched across both) | **slow-dynamics confirmed** → **horizon axis** real | promote horizon axis; characterize onset-time distribution over the **uniform ≤500k window across all 8 seeds** (extension tails are slope-selected → NOT pooled) |
| **s0-class-lottery** | {1,2}/8 convert | **seed lottery** at this power — named, not promoted; matches split s0's isolation | bank lottery-at-current-power; re-pose at higher power / different regime |
| **dose-ordered** | converter count/rate ordered by dose (coin vs scheduled) | **SCREEN-GRADE only (§3.1 pin 1): NAMED, never CLAIMED** — confounded with fabric by construction | its ONLY license is firing the 2×2 |
| **none** | 0/8 convert (with ≥`N_MIN` acquired) | **named finding: conversion unreachable in these regimes at this horizon** — NOT a rig failure, NOT a "dies" | **routes back to Jason** (never a silent extension) |

**The 2×2 trigger (§3.1 pin 2): ANY conversion in EITHER rung** — across-seeds, lottery, OR a dose-ordered pattern — fires the clean deconfounding 2×2. Ordering within the confounded screen pair does not gate it; a single-rung or an un-ordered both-rung conversion fires it just the same.

**Exhaustive/exclusive:** pre-gate A removes `< N_MIN` READ rungs (→ UNREAD); over READ seeds the converter count ∈ {0, {1,2}, {3,4}, ≥5} maps to exactly one of {none, lottery, ambiguous, across-seeds}. dose-ordered is an orthogonal SCREEN-GRADE tag whose sole role is the 2×2 trigger. No outcome falls through.

**Wrong-reason screens (carried):** acquisition-censored/unacquired seed = UNREAD (pre-gate A), never a "no-conversion" data point. A conversion under 0.6 but not the density-matched band = exam-rate false alarm (§4).

---

## 8. Instrumentation (the EXP12 arsenal carries whole)

All EXP12 reads verbatim (`_eval_column`, the 17-key panel incl. `exam_acc`, `asg_cat`, `num`, `den`; `dc_track`@BLOCK; `grad_geometry_split`). NEW, all read-only / non-mechanism: the density-matched conversion detector (§4), the online conversion-onset trigger + `.pt` checkpointing (§6), the extension-rule rising-criterion read (§5). No new loss, no new force.

---

## 9. Scope fences (what EXP14 does NOT do)

- No loss-engineering to pull the completer off the marginal (manufacturing-class FENCED). No new objective, schedule, or signal.
- No change to the EXP12 dynamics, fabric construction, or in-force EXP12 constants. EXP13 (lawful-drift fabric, mixed-W) holds **paused** — EXP14 runs on the EXP12 fabric only.
- Not a certification of any committed trajectory (declined). Fresh runs on current code; regime-level reads only.
- No claim beyond "conversion (does / does not) appear, and (is / isn't) ordered by {horizon, dose, seed}, at this power and horizon."

---

## 10. Build plan (after GO + fork ruling)

One new file `exp14_arms.py` that **imports** `exp12_arms` and (the DYNAMICS — step/losses/optimizer in `EXP12Loop`/`Stage0Loop` — are reused verbatim; `run_exp14_arm` is a new runner body, not a fence violation):
1. `run_exp14_arm(arm, seed, read_at=500_000, h_max=1_000_000)` = `run_exp12_arm`'s loop/reads VERBATIM, but the fabric is **pre-built at `h_max`** (one fixed perm for the shuffled/coin rung — §5/F1); reads + checkpoints (`.pt`) at `read_at`; online conversion-onset trigger (PROPOSED 0.6/2) → `.pt` at onset; the density-matched band read; extension on the SAME fabric only per §5, ≤2×, never past `h_max`.
2. `cut_conv_band(cal_seeds)` = stage-two, per rung: high-quantile of the **post-acquisition, pre-conversion** `exam_acc` span (§4/F2) + `Binomial(exam_n,0.5)` cross-check; `conv_consec`; `n_null` floor with cal-pool widening `{20–24}→{20–29}` if thin (F3); the count-cuts (F4); the rising-criterion; the s0-admission anchor check. **Surfaced before verdict** (reports per-rung `n_null`).
3. `score_exp14()` = pre-gate A (READ floor, F5) → pre-gate B (count partition, F4) → the four-cell read, DRAFT behind the verification pass.
4. `smoke()` = one-code-path assert (step is inherited), checkpoint round-trips (save→load→identical read), **extension faithfulness** (dwelled prefix-reproduces; coin steps past `read_at` on the pre-built `h_max` perm), band cut on a short run, determinism (`gen` parity), fabric asserts.

**Sequence:** GO → build `exp14_arms.py` → smoke → stage-one cal {20–24} @ `h_max` → **cut + surface the per-rung density-matched band + `n_null` + count-cuts** (widen pool if thin) → verdict {0–7} @ read 500k → pre-gates A/B → four-cell read behind the adversarial pass → **STOP at the cell (`none`, `ambiguous`, or ANY conversion → route to Jason; conversion fires the 2×2).** Nothing verdict-grade before the band is surfaced. Commit at the gate.

---

## 11. Verification pass (recorded — the exp03 discipline)

This prereg went through an adversarial refute-default panel (21 agents: 5 lenses × find → per-finding verify at high effort; run `wf_2c90fecd-f47`, 2026-07-07) BEFORE reaching the verdict table. **16 findings raised, 5 CONFIRMED (all should-fix), 11 refuted.** All 5 folded into this doc:
- **F1** (extension/resume): the shuffled/coin fabric is not post-hoc extendable (`randperm(T)` is T-dependent; `build_cells` asserts `t < fab.T`) — the s0-lineage rung. → §5 pre-builds at `H_MAX`; §6 scopes faithful resume (dwelled append-faithful, coin only via the fixed `H_MAX` perm).
- **F2** (band thin-null on coin): p99 over the ~55-window pre-*acquisition* span is unstable, could reject s0 as a false alarm. → §4 cuts from the **pre-conversion marginal span** (the actual EXP12 form) + Binomial cross-check + s0-admission anchor.
- **F3** (band no stability guard): → §4 `n_null` floor + cal-pool widening.
- **F4** (cells don't partition 0–8): → §4/§7 pinned count-cuts + registered AMBIGUOUS state.
- **F5** (`none` has no read-floor → rig-failure masquerade): → §7 pre-gate A (READ = acquired on num/den/asg_cat; `<N_MIN` READ = UNREAD-AT-HORIZON, not `none`).

The 11 refuted (kept off the doc) included: the seed-0 "privileged link" (mechanically real but not a claimed defect), the across-seeds extension-subsample bias (already fenced by §5), the online-trigger-biases-verdict claim (§6 fences it to checkpoint placement), and the "one-code-path violated" reading (§0 scopes verbatim to the dynamics).
