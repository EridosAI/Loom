# EXP17 — sim-divergence exhibit (net/path-vs-v; the reconciliation record)

**[HISTORICAL — the straight-line (v-grid) arc. The falling-curve outcome this exhibit describes
FIRED as the geometry-conflict HALT and was accepted as finding R1 (billiard pinned); superseded by
prereg §9 R2/R3 (orbital re-pose; lexicographic (r,ω) selection). Retained as the
divergence-and-resolution record; nothing here is a live adjudication path.]**

**Rides the EXP17 ratification commit. Enters no canon.** This documents why the prereg's
selection rule is a **contrast form (≥ 4× the measured tremble baseline), not a fixed absolute**
(prereg §8 F4), and hands the adjudication to the real fabric at G2.

## What happened

The prereg's original net/path target (≥ 0.8) came from an implicit **tight-tracking assumption**
(pose ≈ anchor). It was never computed. The actual OU refutes it: at reversion rate **θ = 0.25**
(`TAU = 4.0`; pinned from code, `exp12_fabric.py:71-72`, not from any sim), the pose confined to
±1.5 lags a moving anchor by `v/θ` and cannot follow it once the anchor unrolls past the walls.

Three independent computations from the identical constants
(θ=0.25, `s_step`=0.0826797, bound ±1.5, K=4 axes, onset N(0,0.5) clamped, k==11):

| source | v=0 (tremble) | sweep regime behavior |
|---|---|---|
| all three | **0.145** (exact agreement) | — |
| CC (`exp17_reconcile_sim.py`) | 0.145 | **rises to a ~0.75 cap** (0.712→0.750 over v 0.30→0.50) |
| Jason | 0.145 | **falls** (0.611→0.515) |
| traverse@11 (both) | ~0.09 | agree to ~0.02 throughout |

Same OU core, **opposite sweep behavior** — the locus is the anchor-reflection detail (how the
moving anchor folds at the ±1.5 walls and drags the pose), NOT θ (identical) and NOT the jitter
(identical). CC's `v/θ ≈ 2.3` remark during reconciliation was a **mislabel**: 2.3 was the distance
to the *unrolled* anchor (which diverges by construction); the true tracking lag is `v/θ` = 1.6 at
v=0.4.

## Why this forces the contrast form

- No **absolute** net/path target is defensible when two validated sims disagree on the absolute
  level. Fitting 0.70 to CC's 0.75 cap would fit to a sim that may not match the generator (Jason's
  sim says the ceiling is 0.61 and falling).
- What **both** sims agree on: v=0 tremble ≈ 0.145, and a large separation once v>0. The
  **contrast** (sweep net/path ≥ 4× the *measured* tremble baseline ≈ 0.58) is reachable under both
  curves and is the discriminator that actually matters (reverting vs directed). Selection binds
  per-seed (margin-by-robustness) and jointly with traverse ∈ [0.30,0.50] and the correspondence
  window (§8 F4/F11).

## Adjudication — the real fabric decides

The measurer **reports the full net/path-vs-v curve shape** at G2 (rising-to-cap vs falling), free
at selection time. That single curve says which sim was faithful:

- Curve **rises** past 4×baseline while traverse enters [0.30,0.50] → a v clears both → proceed.
- Curve **falls** short (Jason's regime) → **no v clears both → the pre-named geometry-conflict
  HALT fires** (routes to design). Feasibility is generator-dependent and this outcome is on the
  record, not papered over.

Neither sim is canon. `exp17_reconcile_sim.py` (CC) rides for reproducibility; Jason's curve is
recorded from the design chat (source not ported — only the reported values). The generator, at G2
on the deployed fabric, gets the last word.
