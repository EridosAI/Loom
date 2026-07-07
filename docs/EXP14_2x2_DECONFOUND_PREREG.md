# EXP14 — 2×2 CONVERSION DECONFOUND — PRE-REGISTRATION

**Status: FINALIZED — design RATIFIED (Jason, 2026-07-07) + 2 pins + adversarial panel folded (§8: 7/19 confirmed). Committed as the prereg gate / handoff seam. Build (after GO) in the next context. Nothing builds or runs before GO.**

Lineage: the EXP14 screen (fork (i)) closed with **conversion IS reachable** — 5 coin seeds (verdict {0,1,3,6} + cal s20), scheduled 0/8 (canon §10.22, commit `f039ccd`). The screen is **fabric-confounded** (coin = shuffled, scheduled = dwelled), so "coin converts, scheduled doesn't" is SCREEN-GRADE. Pin 2 fired the 2×2. **This experiment is the clean deconfound: is conversion driven by DOSE (coin exams), FABRIC (shuffled order), or their INTERACTION?**

---

## 0. Discipline traps (carried)

- **No new loss, no new force, one code path.** Reuses `EXP12Loop`/`run_exp14_arm` verbatim (proven digit-identical to `run_exp12_arm`). The 2 new cells are existing EXP12 arms. Only additions are observation/scoring.
- **Manufacturing-class FENCED:** no loss/schedule/signal engineered to produce conversion. Loss-engineering stays fenced until we know the regime (this experiment is that measurement).
- **Determinism:** seed + construction order + threads=1; faithful runner (read-order coupling). Fabric pre-built at `H_MAX=1M` (faithful extension). `.pt` checkpoints (contract).
- **Fabric-assert:** the T-independent re-pin (§10.22 / `_dwell_perm_labels`) is in force; verdict seeds pre-checked outcome-blind (swap defectives per the ruled rule).
- **Verdict-seeds {0–7} ≠ cal-seeds {20,21,22,24,25}.** Cells named before the run; behind the adversarial pass; surface-recommend-stop.

---

## 1. The question

**Attribute conversion (the operator leaving the marginal) to DOSE, FABRIC, or INTERACTION.** The screen established conversion happens on coin/shuffled; every conversion the program has ever seen is coin/shuffled. The 2×2 fills the two missing cells to say *why*.

---

## 2. The 2×2 arms (existing EXP12 arms — no new mechanism)

| | **scheduled** (guaranteed onset word-mask) | **coin** (50:50 uniform mask at pos-1) |
|---|---|---|
| **dwelled** (scene-persistence) | `exp12_dwell` — screen **0/8** | `exp12_12bc_dwp` — **NEW** |
| **shuffled** (order destroyed) | `exp12_shuffle` — **NEW** | `exp12_split` — screen **4/8 (+cal s20)** |

- **DOSE axis:** scheduled {dwell, shuffle} vs coin {12bc_dwp, split}.
- **FABRIC axis:** dwelled {dwell, 12bc_dwp} vs shuffled {shuffle, split}.
- Each arm × seeds **{0–7}** × horizon **500k** (h_max 1M) × checkpointed = **32 runs** (16 new: the 2 new arms × 8; dwell & split verdict runs reuse the screen's committed runs — same seeds, same read).

**Liveness prerequisite (from EXP14 §7 pre-gate A):** the 2 NEW arms must ACQUIRE at 500k for their READ-floor to be meaningful. `exp12_shuffle` acquires fast (shuffled ~3k, like split). `exp12_12bc_dwp` (dwelled+coin) is the open one — established at stage-one cal (below) before any verdict interpretation.

---

## 3. Conversion definition (Jason's pin) + stability companion

- **Conversion = sustained-EPISODE presence, NOT endpoint.** A seed converts if a density-band episode (≥ `conv_consec` consecutive windows ≥ `conv_band`, per-cell) fires **anywhere** post-acquisition-onset. Endpoint-only would miss the real transient conversions (the screen's s1/s3/s6 converted mid-run then decayed).
- **STABILITY logged separately (registered companion):** per converting seed, does the episode **sustain to the horizon** (endpoint above band) or **decay**? Report per cell: n_convert, n_sustain-to-horizon, longest-episode length, within-episode mean. The screen's stability finding (only s0 sustained; s1/s3/s6 decayed) rides in as the baseline.

---

## 4. Per-cell honest band (density-matched, cut at stage-two)

> **STAGE-ONE ADDENDUM (Rulings A + B, Jason 2026-07-08; canon §10.23 — this supersedes the two-pass and the per-cell-own-marginal premise below where they conflict).**
> **Ruling A — the F1 two-pass fixpoint null is DROPPED.** As-built literal, it re-cut on the *self-thinned* null and **violated α on the true marginal** (honest fr, un-thinned: A 0.00132 / C 0.00684 / D 0.00379 vs α=0.001; the printed `false_rate@cut`=0.0 was circular, measured on the null the episodes were removed from). Its guard scenario (a hidden dampened sub-s0 conversion inflating a band → under-detection) did **not** bite B, the dose-only cell (clean at provisional). Band method = the **provisional (§10.22 honest-null) cut** for A/B/D. `_twopass_cut` retained SUPERSEDED (mechanism record + the per-cal / between-episode helpers). Lesson: a false-rate must be measured against the marginal that includes its own chance runs.
> **Ruling B — "each cell on its OWN marginal null" fails for a converting cell; only C_shuffle is broken.** A (0/5 s0-class @cal), B (0/5), D (1/5 = the known s20) self-calibrate on provisional (D keeps committed **0.6875×5** → **F7 preserved**). **C_shuffle's cal seeds convert (4/5 s0-class)** → no marginal; it borrows the **density-matched A_dwell** marginal (both scheduled) **iff the borrow-validity gate passes** (A's band controls the false-rate on C's between-episode windows ≤ 2α). **Gate = SHIFTED** (mean +0.0203; A-band fr 0.00467 on C's floor) → **C uses its OWN between-episode null → 0.64×5.**
> **Referent asymmetry (SAME α, DIFFERENT null):** C's fr is honest against C's own *elevated* floor, so a C conversion means "leaves C's shifted baseline," while A/B/D conversions mean "leaves the dwelled marginal." Recorded per-cell (`false_rate_referent`) in `exp14_band_2x2_cal.json`. **Do not read the four fr's as one equal-guarantee column.**
> Final honest bands (fr ≤ α): **A 0.6111×4, B 0.6667×3, C 0.64×5, D 0.6875×5.**

Each cell gets its OWN band on its OWN marginal null, joint (band, N) cut controlling the pre-conversion false-rate ≤ α, anchored at s0's 0.704×16. *(Superseded for C by the addendum above — C has no own marginal.)*

**TWO-PASS iterative null (panel F1 — the sharpened s20 lesson) — SUPERSEDED by Ruling A (kept for the record):** the §10.22 honest-null excluded only s0-class episodes (`EPISODE_MIN=8` ≥0.704), but the verdict detector cuts bands as low as 0.61×4 — so a *moderate verdict-grade* conversion in a cal seed (e.g. 0.68×5, below the s0-class cut) would survive in that cell's null, inflate its high tail, and push its band UP → **the cell under-detects at verdict.** This bites the decision-relevant `12bc_dwp` cell hardest: on the conversion-suppressing dwelled fabric a *dampened* s20-like episode (below 0.704×8) is the likely regime, so 12bc_dwp's band inflates while split's carried band stays clean → **a true DOSE result would masquerade as INTERACTION** (a confirmation trap on the screen's prior). Fix: cut to a **fixpoint** — (1) provisional (band,N) on the s0-class-excluded null; (2) additionally exclude any cal episode that WOULD fire the *provisional* detector (≥ provisional band for ≥ provisional N); (3) re-cut; iterate. The exclusion now tracks the actual detection band, not a fixed anchor — and does NOT reintroduce the over-stripping that the blanket ≥0.6 exclusion caused (it removes only what the detector itself would call a conversion).
- **Per-cal-seed conversion diagnostic (surfaced):** `cut_conv_band` runs the provisional detector on EACH cal seed and reports which converted, so cal-seed contamination (esp. s20 on 12bc_dwp) is an explicit ruling at the surfacing gate, not something a reviewer must infer from `null_p99`.
- **dwell 0.6111×4, split 0.6875×5** carried from the screen (`exp14_band_cal.json`) — RE-VERIFIED unchanged under the two-pass cut before reuse.
- **shuffle, 12bc_dwp:** cut fresh at stage-one on cal {20,21,22,24,25} @ 500k. **Surfaced (per-cell band, N, n_null, s0-admission, per-cal-seed converters, acquisition-liveness) before any verdict read.**
- Per-cell bands equalize the false-alarm rate across cells — but note that equal false-rate does NOT equalize detection POWER if a cell's null is contaminated (F1) or its post-onset budget differs (§5 F6); both are guarded.

---

## 5. The inference table (named before the run)

Read per cell: pre-gate A (READ = acquired on num/den/asg_cat) → pre-gate B (post-onset budget, F6 below) → conversion (sustained-episode, per-cell band) over READ seeds {0–7}. The attribution is on **which cells convert** — the *pattern* is the verdict; **exact counts are NOT claimed robust at n=8** (power gate F5 below).

Cells: **A** = `dwell` (dwelled-scheduled, the double-negative), **B** = `12bc_dwp` (dwelled-coin = dose-only carrier), **C** = `shuffle` (shuffled-scheduled = fabric-only carrier), **D** = `split` (shuffled-coin = the corner, both ingredients). Structured on the corner D (a REUSED committed run) then B, C — **exhaustive + exclusive:**

| convert-set (post READ/budget gates) | attribution |
|---|---|
| **D does NOT convert** | **INSTRUMENT REGRESSION, not a regime finding (F7):** D is the screen's committed split run re-scored — it MUST reproduce {0,1,3,6}. If it doesn't, the generalized 4-cell scorer/band diverged from the screen → fix the pipeline, do NOT read attribution. (Reuse freezes D's regime + seeds; only the code can make D "fail.") |
| **D only** (B, C silent) | **INTERACTION** — needs BOTH coin dose AND shuffled fabric. Pin-1 null-outcome: "corner only, 3 silent" IS the interaction read (screen prior), not ambiguous. |
| **D + B** (C silent) | **DOSE main effect** — coin enables on either fabric; shuffled-scheduled (C) alone insufficient. |
| **D + C** (B silent) | **FABRIC main effect** — shuffled enables at either dose; dwelled-coin (B) alone insufficient. |
| **D + B + C** (A silent) | **BOTH MAIN EFFECTS — additive, no interaction (F3):** dose AND fabric each independently enable; the double-negative A stays silent. The canonical non-interaction 2×2, and — since each new arm carries exactly one ingredient — arguably the most likely non-interaction result. |
| **A converts** (any set incl. A) | **ANOMALY** — the double-negative should not convert (screen dwell 0/8); if it does, the baseline is contradicted → Fork-1.5-style audit, report, do NOT force an attribution. |
| **NOBODY converts** (incl. D) | routes to the D-regression row above (D not converting is a pipeline check, never a silent regime null). |

**Power gate (F5) — counts are noisy at n=8** (per-cell binomial SE ~0.18 near p=0.5; interaction SE ~0.35). **Any NEW-arm cell (B or C) landing in lottery {1,2} or ambiguous {3,4} fires the `EXT_POOL` {8,9} extension (n→10) BEFORE the attribution row is selected;** the factorial companion reports a Fisher-exact / interaction CI, not a point estimate. A B/C cell counts as "converts" for the pattern only at across-seeds (≥5) or after extension resolves it above ambiguous.

**Budget gate (F6) — match conversion OPPORTUNITY across cells.** Conversions onset late (split up to ~130k post-acquisition); the dwelled cells (A, B) acquire late/variably (dwell onsets 14k–300k), so a dwelled seed can lack the post-onset budget to develop one. Pre-register: a READ seed whose post-onset budget `(500k − acquisition_onset)` is below the **minimum conversion-onset budget on the reference converter (split, ~130k)** is **UNREAD(budget-truncated)** — a latency-censored B seed never scores as a "coin-dwelled doesn't convert" dose/fabric point (analogous to the window-truncated status).

**Factorial companion (reported, not a gate):** dose = mean(coin)−mean(scheduled); fabric = mean(shuffled)−mean(dwelled); interaction = (D−B)−(C−A), with CIs; reported PARTIAL (undefined) if any cell is UNREAD.

**Wrong-reason screens:** unacquired/censored/budget-truncated seed = UNREAD (pre-gates A/B), never a no-conversion point. A conversion failing the per-cell honest band = false alarm.

**Pin 2 — liveness = ACQUISITION, not conversion (EXP14 pre-gate-A / the UNREAD-never-none rule):** `exp12_12bc_dwp`'s cell only enters the attribution if the arm ACQUIRES (differentiated on num/den/asg_cat) on ≥ `N_MIN`=3 verdict seeds. **A non-acquiring 12bc_dwp cell is UNREAD, NOT "no conversion"** — a dead arm must never read as a dose/fabric data point (that would fabricate a "coin-dwelled doesn't convert" attribution from an arm that never came alive to test). If liveness fails at stage-one cal, the (dwelled, coin) cell is UNREAD-AT-HORIZON and the dose/fabric attribution is reported with that cell explicitly absent (surfaced to Jason — the factorial is then partial, not silently completed).

---

## 6. Scope fences

- No loss-engineering (FENCED). No new objective/schedule/signal. No change to EXP12 dynamics/fabric/constants. EXP13 PAUSED.
- Not a claim beyond dose/fabric/interaction attribution of conversion, at this power/horizon.
- Stability is a companion read, not a second verdict axis (its own regime question is downstream).

---

## 7. Build plan + sequence (after GO)

Reuses `exp14_arms.py`: extend `RUNGS` to the 4-cell `CELLS` map; `run_exp14_arm` unchanged; `cut_conv_band` gets the two-pass fixpoint null (F1) + per-cal-seed converter diagnostic; `score_exp14` generalizes to 4 cells; a `score_2x2` for the factorial + attribution.
- **spec_hash parity assert (F2):** `cut_conv_band` and `score_2x2` collect `rec['spec_hash']` across ALL four cells (reused dwell/split + fresh shuffle/12bc_dwp, cal + verdict) and **assert a single value, failing loudly on mismatch** (naming the divergent cell) — because reused-vs-fresh coincides exactly with one interaction diagonal, so a silent build skew would load straight onto the interaction contrast. Prefer `spec_hash` (commit_hash over-trips). Record the shared hash in the emitted verdict JSON.
1. **Pre-check** verdict {0–7} fabric-assert for the 2 new arms (T-independent, T=15k, fast); outcome-blind swap any defective (recorded).
2. **Stage-one cal** the 2 new arms × {20,21,22,24,25} @ 500k → cut shuffle & 12bc_dwp honest bands; establish **12bc_dwp acquisition-liveness**. **SURFACE all 4 per-cell bands + liveness for Jason's read** before verdict.
3. **Verdict:** the 2 new arms × {0–7} @ 500k (dwell & split reuse the committed screen runs) → per-cell conversion + stability.
4. **Score:** per-cell rate → 2×2 attribution DRAFT → **behind the adversarial pass** → route to Jason. STOP at the attribution.

Nothing verdict-grade before the 4 bands + liveness are surfaced. Commit at the gate. Conversion = sustained-episode; stability = companion.

---

## 8. Verification pass (recorded — the exp03 discipline)

Adversarial refute-default panel (`wf_69bccd79`, 5 lenses + verify, high effort) before build. **19 raised, 7 CONFIRMED (should-fix/minor), 12 refuted.** All 7 folded:
- **F1** (band-comparability): the honest-null exclusion (s0-class, 0.704×8) is STRICTER than the verdict detector (0.61×4) → a moderate verdict-grade conversion in a cal seed contaminates its cell's null → the cell under-detects; on the decision-relevant `12bc_dwp` a dampened conversion makes a true DOSE read as INTERACTION. → §4 **two-pass fixpoint null** (exclude what the *provisional detector* would fire, not a fixed anchor) + per-cal-seed converter diagnostic.
- **F2** (run-reuse): reused dwell/split vs fresh shuffle/12bc_dwp = one interaction diagonal; a build skew loads onto the interaction contrast. → §7 **spec_hash parity assert** across all cells.
- **F3** (attribution): the additive both-main-effects pattern {B,C,D convert, A silent} fell through. → §5 **BOTH-MAIN-EFFECTS row** added.
- **F4** (attribution): rows 2/3 overlapped row 5. → §5 table restructured on corner-D then B/C = exhaustive + exclusive.
- **F5** (power): n=8 counts not robust (interaction SE ~0.35). → §5 **power gate** (lottery/ambiguous new-arm cell fires EXT_POOL {8,9}) + CIs; "robust to counts" struck.
- **F6** (opportunity): dwelled cells acquire late → less post-onset budget → conversion opportunity unmatched. → §5 **budget gate** (budget < ~130k = UNREAD budget-truncated).
- **F7** (run-reuse): "split fails to reproduce = regime instability" is wrong (reuse freezes D). → §5 reframed as an **instrument-regression** check.

The 12 refuted stayed off. This prereg is the handoff seam; the build (two-pass null + spec_hash + 4-cell scorer + the two gates) executes in the next context after Jason's GO on the sequence.
