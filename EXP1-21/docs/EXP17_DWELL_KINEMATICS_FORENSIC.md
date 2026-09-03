# EXP17 pre-work forensic — dwell kinematics: "how boring is a dwell?"

**Read-only, learning-free measurement from the rebuilt A_dwell fabric (ground truth).**
Date: 2026-07-11 · Authority: Jason (design chat) · Rides with the EXP17 prereg; enters **no canon** in this task.

Machine-readable companion: `docs/EXP17_DWELL_KINEMATICS_FORENSIC.json` (pair relocated from repo
`scratchpad/` at ratification — prereg §8 F1, the BD-9 precedent). Every number below is
recomputable from that JSON plus the recipe stated in its `recipe` block. This document reports
measurements and their honest uncertainties only — no fork design, no recommendations.

---

## 0. What this measures and why

EXP16 placed the conversion block on the **vision side**; §10.24 established the gate is the **fabric**
(dwelled), main effect on onset. The live EXP17 hypothesis: a dwell is **jitter around a point, not a
sweep** — the pose does bounded OU drift that **mean-reverts to the onset pose**, so consecutive frames
tremble around one viewpoint rather than progressively revealing new views. Near-identical consecutive
views ⇒ degenerate completion among them ⇒ massed near-duplicate updates. This forensic quantifies, from
the ground-truth fabric, **how small the visited neighborhood actually is** — so the EXP17 fork
(reverting-OU vs progressive-sweep — jitter held fixed, anchor speed *added*; per-step displacement
is *not* matched) arrives with the current dwell's novelty measured, not assumed. [Ratification mark
(prereg §8 F14): the earlier "at matched per-step displacement" phrasing is struck — matching
per-step displacement would require shrinking the OU jitter, the σ>0-fenced move §0/§1 forbid; the
fork design is in the prereg §1/F4, not here.]

**Pose.** `c_t := fab.nuis[t]`, the K=4 OU nuisance-coefficient vector (`exp12_fabric.py::build_fabric`,
lines 266–271). Onset pose `c0 := nuis at pos==1`. Reflection bound `= 3·coeff_std = 1.5` per axis; the
family marginal support is `[-1.5, 1.5]` per axis (width 3.0). Designed walk: onset drawn from the family
marginal `N(0, 0.5)` clamped to ±1.5, then per-axis OU `c ← c + θ(c0−c) + s_step·ξ` reflected at ±1.5,
with `θ = 1/τ = 0.25` (τ=4), `s_step = 0.0826797`.

## 1. Provenance and the identity cross-check (the rebuild IS the committed fabric)

Rebuilt `exp12_dwell` deterministically for verdict seeds **{0…7}** via the committed build path
(`build_fabric`, arm flags shuffled=False / uniform_mask=False / word_ref=False / probe_rate=0.0),
`cfg.T = 1,000,008` (h_max=1M), `torch.set_num_threads(1)`. Kinematics measured over frames
**[0, 500,000)** (= `read_at`, the committed run/read window). `coeff_std=0.5` READ from
`exp08/exp10_calibration.json` (`proposed.coeff_std`), not typed.

**Identity gate (hard-stop on mismatch).** For every seed, the full committed fabric manifest
(`exp08/exp14_exp12_dwell_s{seed}_verdict.manifest.json`: T, n_dwells, cap_hits, realized_mean_k,
k_min_realized_frac, truncated_last_dwell, mask_mix, member_hist[16], background_const[4]) matched the
rebuild **byte-for-byte**, and `sum(is_exam[0:499800])` matched the committed `Σ exam_n` (the union of the
1666 emitted eval columns × 300).

| seed | manifest match | exam_n[0:499800] = committed | contained dwells |
|---|---|---|---|
| 0 | ✅ exact | 45680 = 45680 | 45701 |
| 1 | ✅ exact | 45615 = 45615 | 45625 |
| 2 | ✅ exact | 45752 = 45752 | 45775 |
| 3 | ✅ exact | 46045 = 46045 | 46060 |
| 4 | ✅ exact | 45674 = 45674 | 45690 |
| 5 | ✅ exact | 45624 = 45624 | 45641 |
| 6 | ✅ exact | 45769 = 45769 | 45790 |
| 7 | ✅ exact | 45777 = 45777 | 45790 |

Reference: s0 manifest gives n_dwells=91401, cap_hits=649, mask_mix={exam:91401, probe_exam:0,
mid_vis:454283, mid_word:454324}, background_const=[−0.187339, −0.431914, 0.761901, −0.924558] — all
reproduced exactly. **The measured fabric is provably the committed A_dwell fabric.** (Independently,
every headline statistic was re-derived for seed 0 with a from-scratch numpy pass that does not reuse the
measurement code; it matched to 6 decimals.)

> Provenance note (surfaced, non-blocking): HEAD advanced `efc819b → 175e01ee` during the run — the EXP16
> instance committed its `expo_midword` arm. The build path (`exp12_fabric.py`, `sculpt_config.py`,
> `constants.py`, `conflict_stream.py`, `exp10_calibration.json`) and the eight A_dwell verdict reference
> records are **unchanged** across that range; the measurement is unaffected. This forensic touched no
> tracked file and wrote only to `scratchpad/`.

---

## 2. The six pre-named statistics

Statistics were pre-named in the measurement script **before** any number was computed (no forking-path
selection). Pooled = mean over the 8 seeds; per-seed ranges given where they matter. Seed-to-seed
variation is negligible throughout (the fabric is highly self-averaging at ~45k dwells/seed).

### Stat 1 — per-step displacement, three populations (L2 norm over the K=4 pose)

| population | median | (seed-0 IQR) | mean | vs shuffled (median) |
|---|---|---|---|---|
| **within-dwell** \|c_t − c_{t−1}\| | **0.1596** | [0.121, 0.202] | 0.164 | **0.120** |
| **cross-boundary** (last frame → next onset) | **1.3112** | [0.987, 1.659] | 1.341 | **0.989** |
| **shuffled-adjacent** (random neighbor pairs) | **1.3262** | [1.006, 1.677] | 1.358 | 1.000 |

- **within : shuffled = 0.120** (per-seed 0.1200–0.1206) — a within-dwell step travels **~12% of a random
  reshuffle jump**. Per-axis it is the same story: within-dwell |Δ| median ≈ 0.0586/axis vs shuffled
  ≈ 0.489/axis.
- **cross : shuffled = 0.989** (per-seed 0.985–0.993) — **crossing a dwell boundary is essentially a
  random jump.** A new onset is a fresh marginal draw, statistically independent of the previous dwell's
  last pose (both ≈ independent marginal poses).
- **within : cross ≈ 0.122** — a step inside a dwell is ~1/8 of the step taken at a boundary.

The three populations separate cleanly into two regimes: **inside a dwell = small tremble; at a boundary =
full jump.**

### Stat 2 — net-vs-path ratio per dwell (the tremble-vs-sweep discriminator)

`ratio = ||c_end − c_onset|| / Σ||c_t − c_{t−1}||`. Reverting-OU ⇒ net ≈ 0 while path > 0 (ratio → 0); a
progressive sweep ⇒ net ≈ path (ratio ≈ 1).

| dwell-length bucket | pooled ratio (mean) | seed-0 n | seed-0 net_mean | seed-0 path_mean |
|---|---|---|---|---|
| p2 (k=2) | **1.000** | 4438 | 0.156 | 0.156 |
| p3 (k=3) | **0.630** | 4108 | 0.194 | 0.316 |
| p4–6 | **0.372** | 10089 | 0.220 | 0.630 |
| p7–12 | **0.185** | 12753 | 0.233 | 1.334 |
| p13–48 | **0.079** | 14313 | 0.234 | 3.422 |
| all dwells (pooled) | **0.314** | — | — | — |

The signature is unambiguous. **As dwells get longer, path length grows without bound (0.16 → 3.42) while
net displacement plateaus at ≈ 0.23** — the ratio collapses toward zero. p2 is exactly 1.0 by construction
(a single step). A progressive sweep would hold ratio ≈ 1 at every length; instead it decays as ~1/path.
**Long dwells wander in place, they do not travel.**

### Stat 3 — visited-neighborhood radius

Max excursion from onset within a dwell.

- **radius (L2 norm), median = 0.301** (pooled). As a fraction of the box half-diagonal (bound·√4 = 3.0) =
  **0.100**; of the full diagonal (6.0) = **0.050**.
- **per-axis radius / per-axis support (width 3.0) = 0.0556 (pooled)** → **a dwell's max per-axis
  excursion from onset is ~5.6% of the full ±3σ axis range.**
- Context — the pose SPACE dwells sit in: `onset_pose_sd ≈ 0.499/axis` (= coeff_std 0.5, filling the
  marginal). So dwells scatter across a space of per-axis sd 0.5, but each individual dwell explores a
  neighborhood of radius ~0.30 (norm) around its own onset.

**A dwell visits ~5–10% of the pose range it could occupy.**

### Stat 4 — within-dwell pose autocorrelation by lag (deviation series)

Pooled Pearson autocorrelation of `dev_t = c_t − c_onset`:

| lag | 1 | 2 | 3 | 4 | 6 | 8 | 12 |
|---|---|---|---|---|---|---|---|
| empirical | 0.711 | 0.519 | 0.383 | 0.286 | 0.160 | 0.090 | 0.029 |
| theory 0.75^L | 0.750 | 0.563 | 0.422 | 0.316 | 0.178 | 0.100 | 0.032 |

Consecutive within-dwell poses are **~0.71 correlated**, decaying geometrically at the OU rate. The
empirical values sit **consistently ~5% below** the stationary-OU prediction `0.75^L` — because the
deviation is anchored at 0 at each onset (transient-from-onset, not a fully stationary process; dwells are
short relative to τ=4). Reported, not corrected.

### Stat 5 — dwell-length realization over [0, 500k) (context for 1–4)

- **mean k = 10.93** (per-seed 10.86–10.96), design E[k] = 11.
- **P(k=2) = 0.099** (per-seed 0.097–0.103), design 0.1.
- **cap-hits (k=48): 351–390 per seed** (~0.78% of dwells), design theory 0.71%.
- seed-0 histogram: p2 4438 / p3 4108 / p4–6 10089 / p7–12 12753 / p13–48 14314.
- **The realized dwell law matches the designed law with no drift.** (Surfaced per report-don't-patch:
  nothing anomalous here — realized ≈ designed.)

### Stat 6 — designed vs realized OU parameters

| quantity | designed | realized (pooled) | realized / designed |
|---|---|---|---|
| per-axis within-step sd | 0.08839 * | 0.08716 | 0.986 |
| per-axis stationary-deviation sd | 0.12500 | 0.11741 | 0.939 |
| lag-1 autocorrelation | 0.750 | 0.711 | 0.948 |

\* Theory `sqrt(θ²·Var(dev) + s_step²)`, `Var(dev)=s_step²/(1−(1−θ)²)`; `s_step = 0.0826797`.

**Realized within-step sd matches design (98.6%).** The **stationary-deviation sd lands ~6% below the
0.125 target** — the same transient-from-onset effect: with mean dwell length ~11 and τ=4, a large share
of frames have not yet reached the stationary spread from their onset. This *reinforces* the boring-dwell
reading — dwells do not even fully expand to their own designed stationary radius before they end.

---

## 3. Companion (secondary, LEARNED-SIDE, confounded by learning — context only)

From the committed EXP14 verdict records (not the ground-truth fabric): mean over the last 10 eval columns,
A_dwell (`exp12_dwell`) vs C_shuffle (`exp12_shuffle`), averaged across seeds 0–7. **This is
learned-representation-side and confounded by learning; it rides as context, never as a primary number,
and no causal reading is offered here.**

| late-run metric | A_dwell | C_shuffle | A / C |
|---|---|---|---|
| `div_nuis` (exam nuisance-residual energy) | 0.0125071 | 0.0017880 | **7.00** |
| `d2_spread` (within-group pool spread) | 4.0339 | 2.2732 | **1.77** |

*(Ratification fact-check correction, prereg §8 F1: the ratios read 6.99 / 1.78 before ratification;
full-precision from the JSON aggregates is 6.995 → 7.00 and 1.7745 → 1.77.)*

Descriptively, the dwelled arm carries **~7× the nuisance-residual energy** and **~1.8× the pool spread**
of the shuffled arm at late run. Directionally consistent with "the dwelled fabric keeps the
representation less settled on the nuisance axes," but this is a learned quantity and cannot be
disentangled from learning dynamics in this forensic — it is logged, not interpreted.

---

## 4. Honest uncertainties / surfaced observations

- **Autocorrelation and stationary-deviation sd both sit slightly below their stationary-OU targets**
  (Stat 4, Stat 6). This is the transient-from-onset anchoring, not an instrument discrepancy — the
  estimator measures deviation from onset, and short dwells never reach stationarity. It is a real
  property of the fabric (dwells are *even smaller* than the stationary neighborhood), reported as such.
- **The shuffled-adjacent baseline** is computed as adjacent diffs after a fixed random permutation of the
  in-window frames (committed A-SHUFFLE key), i.e. random neighbor pairs — distributionally identical to
  the C_shuffle arm's frame neighbors, not the literal T=1,000,008 permutation restricted to the window.
- **Per-dwell statistics (Stat 2, 3)** use dwells fully contained in [0, 500k) (`onset_idx + k ≤ W`);
  the ≤1 boundary-straddling dwell per seed is excluded from per-dwell metrics (it still contributes its
  in-window frames to the per-frame Stat 1 / Stat 4 pools).
- **No anomaly between designed and realized dwell law** — the realized law is the designed law.
- Seed-to-seed variation is negligible on every statistic; the numbers are stable.

---

## 5. How boring is a dwell, in numbers

A dwell is a tremble, not a tour. Frame to frame inside a dwell the viewpoint moves about **one-eighth**
of the distance it would move to a random other frame (within:shuffled = 0.12), and it moves that little
while **circling its own starting pose**: over a full dwell the net displacement is only **31%** of the
path walked, and for the long dwells that dominate the traffic (k ≥ 13, ~31% of dwells) it is just **8%** —
the pose accumulates 3.4 units of path but ends 0.23 from where it began. The whole excursion stays inside
a neighborhood about **5–6% of the per-axis pose range** wide, and consecutive poses are **~0.71
correlated**, decaying at 0.75 per step. Crossing into the *next* dwell, by contrast, is a full random
jump (cross:shuffled = 0.99). So the fabric the system trains on delivers, within each dwell, a run of
~11 near-duplicate views of one object — trembling in place, not sweeping to reveal new views — punctuated
by an abrupt jump to a fresh object. That is the degenerate-completion neighborhood EXP17's
reverting-OU-vs-progressive-sweep contrast is built to break: quantified here, the current dwell's
per-step novelty is ~12% of a random look and its net novelty falls toward zero the longer it lasts.
