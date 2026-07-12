# EXP17 — PRE-FLIGHT ANNEX: touch-2 advisory kinematics sweep

**Advisory, scope-fenced (Jason-requested, 2026-07-12). Rides the pre-flight commit.** Fabric
kinematics + onset marginals ONLY — no learner, no loss, no outcome statistic touched; the corridor
stays shut. Committed-measurer recipes verbatim (`exp17_score.measure_kinematics`;
`onset_marginal_delta`'s per-axis quantile-coupled W1 estimator, replicated byte-faithful because
the committed function hard-codes the verdict-seed set). Generator:
`experiments/05_attention_sculpting/exp17_annex_sweep.py` (rides the commit). **No new constant is
pinned.** If any finding motivated a pin change it would route as **ratification-class
re-selection** with the fence-adjacent flag — never an in-place nudge.

**Bottom line: neither halt-class condition trips.** Deployed walls are *wider* than the 100k read
(not tighter); W1(r) is smooth and monotone with the pin at its low-confound end (no knee). The
(0.85, 18°) freeze is corroborated at the deployed window.

---

## Step 0 — prefix-identity lever (verified)

Byte-compare of the orbit canonical arm (`exp12_dwell_orbit`, seed 0), fabric rows [0, 500k), a
T=500k build vs the T=1M build: **`nuis`, `pos`, `orbit_planes`, `orbit_centers` all byte-identical
across the 45,701 contained dwells.** The build is forward and prefix-stable. **Consequence:** every
sweep cell runs at T=500k with the [0,500k) window and is **deployed-window-exact at half cost**.

*Seed-class check:* kinematics measures are fabric-only, X-blind; the pre-registered seed roles
(cal / verdict / EXT / subst) bind LEARNER runs and scoring, not fabric kinematics — `select_orbit`
itself measured kinematics over the verdict seeds with no seed-class restriction. Seeds {0,1,2,3}
(a subset of verdict) are admissible for a kinematics-only measure. No rule binds.

---

## Sweep A — deployed ω-slope at r = 0.85 (seeds {0,1,2,3}, [0,500k))

`np11` / `tr11` = `measure_kinematics` pooled mean of per-seed means over k==11 contained dwells
(committed recipe). Deployed bars = **4× / 2.5× `baselines_1M`** (freeze artifact): np ≥ **0.57956**,
tr ≥ **0.22548** (and tr ≤ 0.50 ceiling, far above).

| ω | np11 (±sd) | tr11 (±sd) | np clears 0.57956 | tr clears 0.22548 |
|---:|---|---|:--:|:--:|
| 17 | 0.5898 ± 0.0016 | 0.2320 ± 0.0003 | ✓ (+0.0102) | ✓ (+0.0065) |
| **18 (pin)** | **0.5869 ± 0.0016** | **0.2379 ± 0.0003** | ✓ (+0.0073) | ✓ (+0.0124) |
| 19 | 0.5813 ± 0.0016 | 0.2430 ± 0.0002 | ✓ (+0.0017) | ✓ (+0.0175) |

*Curve 1 (np11 ↓, tr11 ↑ vs ω):* `np11: 0.5898 → 0.5869 → 0.5813` (monotone down);
`tr11: 0.2320 → 0.2379 → 0.2430` (monotone up).

**Slopes, deployed vs the 100k selection grid (side by side):**

| slope (per °) | deployed [0,500k), seeds {0–3} | 100k grid, seeds {0–7} |
|---|---:|---:|
| np11 | −0.00426 | −0.00415 |
| tr11 | +0.00547 | +0.00542 |

The deployed slopes match the 100k grid to ~3% — the kinematic surface is **scale-stable**.

**Interpolated feasibility walls (ω where each statistic crosses its bar):** np wall **ω = 19.40**,
tr wall **ω = 15.81** → deployed feasible window ≈ **[15.81, 19.40]** (width 3.6°). The 100k grid
window (np falls through by ω=20, tr by ω=16) ≈ **[16.0, 18.9]** (width 2.9°). The pin ω=18 sits
inside with **2.2° / 1.4°** margin to the tr / np walls. *(100k grid r=0.85: ω16 np 0.5885 / tr
0.2255[fails floor2]; ω18 np 0.5858 / tr 0.2379; ω20 np 0.5719[fails floor1] / tr 0.2472.)*

---

## Sweep B — r-trajectory at ω = 18 (seeds {0,1,2,3}, [0,500k))

Same builds serve W1 and np11/tr11. `W1` = per-axis quantile-coupled Wasserstein-1 between the
arm's onset (pos==1) marginal and A_dwell's, pooled over seeds (committed estimator); per-seed W1
gives the error bar. r = 0.80 is off-grid and expected infeasible — it reads the slope, not a
candidate.

| r | clip ±hw | np11 | tr11 | W1 (pooled) | W1 (per-seed ±sd) | feasible? |
|---:|---:|---|---|---|---|:--:|
| 0.80 | 0.325 | 0.5701 | 0.2264 | 0.0173 | 0.0175 ± 0.0006 | ✗ (np < 0.57956) |
| **0.85 (pin)** | **0.275** | **0.5869** | **0.2379** | **0.0227** | **0.0228 ± 0.0005** | ✓ |
| 0.90 | 0.225 | 0.6022 | 0.2494 | 0.0304 | 0.0305 ± 0.0004 | ✓ |

*Curve 2 ({W1, np11, tr11} vs r):* `W1: 0.0173 → 0.0227 → 0.0304` (monotone up, mildly convex —
steps +0.0054 then +0.0077); `np11: 0.5701 → 0.5869 → 0.6022`; `tr11: 0.2264 → 0.2379 → 0.2494`.

W1 rises monotonically with r. The pin r=0.85 sits at the **low end** of the W1 range — the
max-clip lexicographic objective placed it at *least* centering (RB-2's design intent). The
onset-marginal confound accelerates only at *larger* r, away from the pin. r=0.80 has a larger clip
(0.325) yet is infeasible on the np floor — larger clip does not rescue a too-small arc.

---

## Reference C — W1 in contrast form (the ratio)

Baseline = **W1(A_dwell tremble onset marginal vs the tremble RAW full-frame delivered marginal)**,
same estimator and seeds {0,1,2,3}, [0,500k) — the intrinsic within-tremble scale (how far the
onset subset sits from the full delivered pose distribution). **Baseline W1 = 0.0096 ± 0.0003.**

- pin onset shift / baseline = 0.0227 / 0.0096 = **2.36×**
- freeze {0–7}@1M onset shift / baseline = 0.0228 / 0.0096 = **2.37×**

The pin's onset marginal sits ~2.4× the tremble's own onset-vs-full-marginal spread — a modest,
bounded shift. (RB-2 rider a: reported trade, never a fence.)

**Cross-checks (deployed corroborates the freeze):** pin np11 4-seed 0.5869 vs freeze 15-seed
0.5858; pin W1 4-seed {0,1,2,3} 0.0227 vs committed `onset_marginal_delta` {0–7}@1M 0.0228; Sweep A
reproduced byte-identically across two independent runs (determinism). Estimator seed-scatter is
small (W1 per-seed sd ≤ 0.0006), so the W1(r) rise is well-resolved, not noise.

**Recipe fidelity certified:** the replicated W1 estimator, run over the committed seed set {0–7},
reproduces `onset_marginal_delta`'s value **byte-exact** — 0.022779201148368088, abs diff 0.0
(and, computed from a T=500k build, it equals the committed T=1M [0,500k) value, re-confirming the
Step-0 prefix-identity lever). `np11`/`tr11` are `measure_kinematics` called unchanged.

---

## Halt-class assessment (qualitative — Jason rules)

| criterion | finding | trips? |
|---|---|:--:|
| deployed walls materially tighter than the 100k read | walls **wider** (3.6° vs 2.9°); slopes scale-stable; both 1°-inside probes clear (np@19 +0.0017, tr@17 +0.0065) | **no** |
| a W1 knee at the pin | W1(r) smooth, monotone, mildly convex; pin at the low-confound end; steepening is *past* the pin | **no** |

**Neither condition trips.** The one thin number worth naming: np11 at ω=19 clears the bar by only
+0.0017 — but that is one degree *above* the pin (the pin's own np margin is +0.0073), and the np
wall (ω=19.40) is farther from the pin than at 100k (ω≈18.9). The advisory sweep corroborates the
(0.85, 18°) freeze and surfaces no reason to re-select.
