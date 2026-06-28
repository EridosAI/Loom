# Stage-0 Characterisation Sweep — CC Implementation Spec (FINAL)

**What this is.** The build spec for the post-Phase-1 characterisation sweep. Design is closed;
this is the bridge to CC. exp03-style: thresholds calibrated from the live rig, failure
conditions and the S-curve signature pre-registered *here* as testable inequalities, before any
run.

**Status.** Closes `PROJECT_STATE_AND_MVP.md` §12.C. Built on the Phase-1 core; the loop,
operator, collapse-control, masking, and anchor are exactly Phase-1 (§10). Does not change §9,
§12.A/B/D.

**Goal.** Characterise the developmental curve — *not* "make Readout G go clean." A clean-G
window is one point on the curve. Deliverable = the **response surface**: PAM/JEPA gradient share
across the trajectory, read for (a) whether a clean-G window opens and where, (b) whether
PAM-grad share rises through the rapid phase (the paradigm test), (c) whether the shape is an
S-curve — all **computed**, not eyeballed (§6, §9).

---

## `[RECONCILE]` convention (read first)

Every value tagged **`[RECONCILE]`** is a placeholder to be set from the **live rig on the commit
the sweep runs** — via Step 0 (calibration) or the validity probe — **not pinned by feel**. This
is exp03's discipline (thresholds taken from the validity table *before* training). Round numbers
shown next to a `[RECONCILE]` tag are **illustrative, never authoritative**.

**Why this is non-negotiable for the oracle floor specifically:** the oracle threshold sets the
band ladder's upper cap (the hard-band F3 boundary). A guessed value either (a) never fires F3
(too lax → no principled cap) or (b) caps *inside* the clean-G window (too strict → silently
deletes the result you are hunting). It must be **measured on the current scale**. Do not reach
for Phase-1's logged numbers: Phase-1 ran on `a94863e`; the sweep may run on a different commit;
a stale literal re-introduces exactly this failure.

A consolidated register of every `[RECONCILE]` value is in §11.

---

## 0. Scope-lock — what varies, and what does not

The sweep varies **exactly two** things relative to Phase-1:

1. **Band** — the visual separability of B (autonomous-vs-associative balance). DENSE axis.
2. **Unpool-rate** — the maturational clock, held *constant* per run at one of a few values
   (tempo / where a run lands on the S-curve). COARSE axis.

**Everything else is Phase-1, unchanged:** same prototype-resonance operator (no softmax-attention,
no PAM latent), same no-stop-grad collapse-control (anchor + SIGReg spread), same six-family
non-causal masking, same frozen word anchor, same one code path.

**Nothing-new guard (binding).** More compute is **not** more knobs. No gain sweep, no variation of
P, no operator swap, no collapse-control change. Compute buys **band-density, run-length, and
seed-count on these two axes only**. If a change is not band-density, run-length, or seed-count, it
is out of scope — scope creep wearing a generous face is the drift vector.

---

## Step 0 — B00 oracle calibration (pre-flight; sets the cap; runs before the ladder is committed)

The oracle threshold — which sets the F3 cap **and** the clean-G oracle bar — is calibrated on the
rig it is actually capping, on the current commit, **before** the ladder is fixed.

**Procedure.** On the current commit, run the **easy band B00** (highest r/σ — B trivially
autonomously resolvable) across a calibration seed set, and measure where the three levels actually
sit *now*:

- `chance` — the begin-symbol / B floor (structurally 1/K; measure empirically too).
- `intact_easy_ceiling` — intact (word-present) arm B-recovery at B00.
- `oracle_easy_ceiling` — oracle (no-word, capacity-open) arm B-recovery at B00.

**Derive and commit, with `commit_hash`:**

- `oracle_threshold` = `chance + margin_oracle`, constrained `oracle_threshold < oracle_easy_ceiling`
  (so the threshold is comfortably cleared at the easy band, where B *is* recoverable). `margin_oracle`
  is `[RECONCILE]` — set so the threshold sits well above chance and well below the easy-band ceiling
  (a real separation, measured, not a round number).
- `noword_floor_band` (clean-G no-word bar) — `[RECONCILE]`, chance-derived (the band the no-word
  arm must sit *in* for a clean-G window).
- `intact_bar` (clean-G intact bar) — `[RECONCILE]`, derived from `intact_easy_ceiling` (the level
  the intact arm must clear).

**Output.** A committed calibration record: `{chance, intact_easy_ceiling, oracle_easy_ceiling,
oracle_threshold, noword_floor_band, intact_bar, commit_hash, spec_hash}`. The band ladder (§2) and
the clean-G rule (§6) are committed **only after** Step 0. This is one cell, cheap, and it anchors
the cap to the live rig.

---

## 1. The two axes

### 1.1 Why asymmetric (not a symmetric grid)

Band moves the autonomous-vs-associative balance — the quantity Readout G measures. Rate moves tempo
— where on the S-curve a finite run lands. Crossing them symmetrically entangles balance with tempo,
the attribution-blur the gain-ramp 1D sweep existed to avoid. Hence band dense, rate coarse.

### 1.2 Band — DENSE (the science is here)

Autonomous resolvability of B is governed by the visual separability ratio **r_fine / σ_stim**
(exp01's r/σ; r/σ ≈ 6.7 trivially learnable, r/σ ≈ 1.0 unlearnable-for-all). The band **hardens by
lowering r/σ** — `r_fine`↓ and/or `σ_stim`↑ (either direction admissible; both reduce the same ratio).

- **Endpoints — probe-bracketed, `[RECONCILE]`.** Top (B00) = r/σ high enough that no-word autonomous
  acquisition succeeds cleanly. Bottom = the probe estimate of where the oracle approaches
  `oracle_threshold` (Step 0). The **true** lower cap is enforced at runtime by the oracle column
  (§5): any cell breaching → F3, dropped. The probe brackets the *candidate* range; the oracle
  threshold *enforces* it.
- **Density:** ≥ 10 uniform steps in r/σ between bracketed endpoints (finer if cheap; freed compute
  goes here first). Three levels only tell you *whether* a window exists; density resolves the
  **transition shape** — sharp vs gradual fall-off of autonomous resolution, where the oracle-loses-B
  cliff sits relative to the clean-G window, whether valid-hard bands form a plateau or a knife-edge.
  The band-ladder multipliers are `[RECONCILE]`.
- **Predicted clean-G location:** the *interior* — below autonomous-success, above oracle-loss.

### 1.3 Unpool-rate — COARSE (a locator, not a finding)

- **Two constant rates: `MODERATE` and `SLOW`.** Two points are the minimum that registers the
  toe-lengthening prediction (a third only if free; the axis stays honestly coarse).
- `MODERATE` = the current §12-B-pinned Stage-0 constant clock. `SLOW` = a fixed fraction below it
  (`slow_fraction` `[RECONCILE]`).
- **The fast cell is dropped entirely.** A fast clock compresses the toe; the toe's length ("ball"
  before "green-ball") is part of what the S-curve hypothesis is *about* — speeding it up means never
  measuring it. With compute free, lengthen runs (§3) so a moderate/slow clock traverses
  toe→rapid→plateau on its own terms.

> **Rate-caveat (carry; do not drop).** The constant unpool-rate here is a coarse **S-curve locator**,
> orthogonal to §12-B's slow-start ramp (which stays **pinned off** for this run). It is **not** a
> finding about developmental pacing. Do not let a "rate matters" read become license to reintroduce
> splitting-against-an-unsettled-target — the exact failure the ramp prevents.

---

## 2. Run-length & window cadence (operationalized)

Define the **developmental clock** as `capacity_fraction` = current unpooled depth / full depth
(0→1 over a run; rate-independent).

- `T95` = first wave where `capacity_fraction ≥ 0.95`.
- `T_run = 1.25 · T95` (each run goes 25% past capacity-saturation to observe the share plateau). CC
  computes `T95` live **per (cell, rate, seed)** — it is larger for `SLOW`, which is the point: each
  clock runs to its own plateau.
- **Cadence:** ≥ **P = 40** eval-window rows uniformly across `[0, T_run]` in waves (finer if cheap).
  Trajectory rows, **never** a single checkpoint; no end-of-run summary is the primary deliverable.

**Capacity-fraction is the PRIMARY comparison axis.** Raw-wave cannot compare `MODERATE` vs `SLOW`
(different clocks). Plot/aggregate `pam_grad_share` against `capacity_fraction` to put both rates on
the same developmental axis (the phase bands in §6 are defined in capacity-fraction). Log `wave` too
— it carries the wave-domain dilation (the toe lengthening for `SLOW`) and reproducibility — but
capacity-fraction is the read for cross-rate shape comparison.

---

## 3. Seeds as instrument (not a noise-check)

Phase-1's G ambiguity was seed-instability — categories flipping across 3 seeds, inversions
indistinguishable from signal. Convert that into a measurement:

- **≥ 20 seeds per cell** (floor; scale up freely — highest-value place compute goes). 3 cannot
  distinguish a frequency from a coin-flip; 20 makes a single flip ≈ 5% of the denominator.
- **Deliverable shifts** from "does a window appear" to **"in what fraction of seeds, and how
  sustained."** Every verdict in §6/§9 is a **fraction over the seed distribution**, not a single trace.

---

## 4. The oracle column & the drift-trap

The oracle — **no-word, capacity-open B-recovery** — is a **logged column at every band cell, every
window**, compared against the Step-0 `oracle_threshold`.

- **Pre-registered read:** as band hardens, no-word *acquisition* falls while oracle *recoverability*
  stays ≥ `oracle_threshold` (B representable, just not acquired). The cell where oracle recoverability
  *also* drops below `oracle_threshold` is where B has become **non-representable** = manufactured
  gap-3 = the **cap on the sweep**.
- **Cell-drop rule (F3):** a cell with any seed/window breaching `oracle_threshold` is flagged **F3**
  and **dropped from clean-G counting** — never counted as a clean gap.

**Drift-trap line CC must hold (binding).** Band hardens the **environment**, never vision's **access**
to B. The oracle is the line. A cell where oracle-recoverability falls is the cap; **wanting to push
past it to force the no-word arm down is the tell** — stop and surface, do not build something to drive
the no-word arm down.

---

## 5. Phase metrics — the verdict made arithmetic

The S-curve claim is a computed inequality over the seed distribution, not a shape read off a plot.

**Phase bands (in `capacity_fraction`; cutoffs `[RECONCILE]`, illustrative):**

- toe = `[0, 0.25]`, rapid = `[0.25, 0.75]`, plateau = final 20% — `[RECONCILE]`.

**Per-seed share statistics:**

- `toe_share` = mean `pam_grad_share` over the toe band.
- `rapid_peak_share` = high-quantile (peak) `pam_grad_share` over the rapid band.
- `plateau_share` = mean `pam_grad_share` over the plateau band.
- `delta_rapid` = `rapid_peak_share − toe_share`.
- `delta_plateau` = `plateau_share − rapid_peak_share`.

**Pre-registered S-curve signature (testable inequality, evaluated per seed, reported as a fraction
over the seed distribution per cell):**

> `delta_rapid > 0`  AND  `delta_plateau ≤ tol_plateau`

where `tol_plateau` is `[RECONCILE]`. Report `s_curve_signature_frequency` (fraction of seeds
satisfying it) **and** the distributions of `delta_rapid` / `delta_plateau` — not a single trace.

**clean-G sustainedness rule (pinned form; thresholds `[RECONCILE]`):** `cleanG_flag` (§7) must hold
for **≥ `N_consec` consecutive eval windows OR ≥ `X_pct`% of `T_run`, whichever is stricter**.
`N_consec`, `X_pct` are `[RECONCILE]`.

**`autonomous_resolution_frequency`** = fraction of seeds in which the **no-word arm acquires B
sustainedly** (same sustainedness rule) at the cell. This is the direct F2/F4 discriminator
(autonomous-everywhere vs suppressed-in-the-interior).

---

## 6. Logging schema

**Per logged eval-window row**, keyed by `(band_cell, unpool_rate, seed, wave)`:

| field | definition |
|---|---|
| `commit_hash`, `spec_hash` | the exact code + spec that produced the row (reproducibility) |
| `wave` | wave index |
| `capacity_fraction` | unpooled depth / full depth — the **primary** developmental axis |
| `pam_jepa_grad_ratio` | ‖g_PAM→vision‖ / ‖g_JEPA→vision‖ — *unbounded; blows up as JEPA→0 at saturation* |
| `pam_grad_share` | ‖g_PAM→vision‖ / (‖g_PAM→vision‖ + ‖g_JEPA→vision‖) — **bounded [0,1]; the plateau-read metric** |
| `noword_B_acq` | no-word arm B-acquisition (autonomous resolution; G's no-word arm) |
| `intact_B_res` | word-present arm B-resolution (G's intact arm) |
| `oracle_B_rec` | no-word **capacity-open** arm B-recovery (§4 drift-trap column) |
| `cleanG_flag` | `(intact_B_res ≥ intact_bar) ∧ (noword_B_acq ∈ noword_floor_band) ∧ (oracle_B_rec ≥ oracle_threshold)` — bars from Step 0 |
| `build_invariants` | all Phase-1 guards pass (frozen anchor, no-detach, six cue-shapes, no-softmax, order-as-content `max_coord_r2 < 0.9`, one code path) — row **invalid** if any trips |

Log **both** grad metrics (the ratio for continuity with Phase-1's headline; the bounded share
because the plateau read needs it where JEPA→0).

**Per-cell aggregation** (across seeds and the trajectory):

| field | definition |
|---|---|
| `s_curve_signature_frequency` | fraction of seeds satisfying the §5 inequality |
| `delta_rapid_dist`, `delta_plateau_dist` | the per-seed delta distributions |
| `cleanG_frequency` | fraction of seeds with a sustained (§5 rule) clean-G window |
| `cleanG_sustain` | mean window-duration `cleanG_flag` holds, over seeds where it opens |
| `autonomous_resolution_frequency` | fraction of seeds where the no-word arm acquires B sustainedly |
| `oracle_floor_breach` | True if any seed/window had `oracle_B_rec < oracle_threshold` → cell **F3**, dropped |

---

## 7. Pre-registration (fix the verdict before the run)

### 7.1 Expected shape (as inequalities)

- `s_curve_signature_frequency` materially > 0 in the interior bands, **higher / earlier in harder
  bands** (`delta_rapid > 0`, `delta_plateau ≤ tol_plateau`).
- A clean-G window opens in the harder-band **interior** (`cleanG_frequency` material where
  `autonomous_resolution_frequency` is low), **bounded above by the oracle-loses-B band**
  (`oracle_floor_breach`).
- The toe **lengthens in the wave domain** as unpool-rate slows (`SLOW` T95 > `MODERATE` T95); on the
  capacity-fraction axis the share-vs-development shape is expected largely rate-invariant (rate is a
  locator).

### 7.2 Failure taxonomy F1–F4 (verbatim — the rigor is pre-registering the failure read)

- **F1** — flat PAM trajectory across all cells (challenges the S-curve). *Computed:* `delta_rapid ≈ 0`
  everywhere; `s_curve_signature_frequency` ~0 at all cells.
- **F2** — autonomous-everywhere (WRONG_REASON extended across the surface — gap-3 alive but not the
  teacher in this regime). *Computed:* `autonomous_resolution_frequency` high at all bands.
- **F3** — oracle loses B in a hard cell (band crossed into unrepresentability — the drift trap;
  drop/flag the cell, never count it as a clean gap). *Computed:* `oracle_floor_breach` = True → cell
  dropped.
- **F4** — clean-G only at trivial/easy band (artifact, not developmental work). *Computed:*
  `cleanG_frequency` material only at high-r/σ (easy) cells, ~0 in the interior.

### 7.3 Look-here-first prior

The informative region is likely **harder-band × moderate/slow rate** — not an endpoint of either axis.
Inspect there first.

---

## 8. Verdict logic (computed)

A **paradigm-positive** read requires, at a non-trivial **interior** band cell, all of:

1. `s_curve_signature_frequency` materially > 0 (**not F1**);
2. `autonomous_resolution_frequency` low *at that cell* while higher at easy bands (**not F2**);
3. `cleanG_frequency` material at non-trivial band (**not F4**);
4. `oracle_floor_breach` = False there (**not F3**).

Each F is a named alternative the surface can land in. The result is the surface plus which of
{paradigm-positive, F1, F2, F3, F4} it matches — not a PASS/FAIL.

---

## 9. Build-correctness carry-forward

- **Every Phase-1 build invariant gates every cell** (§6 `build_invariants`). A cell with any
  invariant tripping is invalid, not a result.
- **This is a Readout-G change.** It does **not** discharge the §12-D Readout-D entangled-corner debt
  (`full_ols_r2 ≈ 1.0`, linear regime). Readout D stays linear-separable until within-window content
  drift returns; that debt is **out of scope here** and is not touched by the band/clock sweep.

---

## 10. Concrete parameter block & `[RECONCILE]` register

### Pinned (structural — do NOT calibrate; these are choices, not rig-scale thresholds)

| parameter | value |
|---|---|
| Axes | band (dense) × unpool-rate (coarse); asymmetric, not a grid |
| Band axis | r_fine / σ_stim decreasing; **≥ 10** uniform steps between bracketed endpoints |
| Unpool-rate axis | **2** constant rates: `MODERATE`, `SLOW` (fast cell dropped) |
| `MODERATE` rate | the current §12-B-pinned Stage-0 constant clock |
| Seeds per cell | **≥ 20** (floor) |
| `T95` | first wave with `capacity_fraction ≥ 0.95` |
| `T_run` | `1.25 · T95` (per cell/rate/seed) |
| Window cadence | **≥ 40** trajectory points uniform over `[0, T_run]` |
| Oracle | logged column at every cell, every window |
| Primary comparison axis | `capacity_fraction` (not wave) |
| Every row carries | `commit_hash`, `spec_hash` |

### `[RECONCILE]` register (calibrate from the live rig on the run commit — never pin by feel)

| value | source |
|---|---|
| `oracle_threshold` | **Step 0**: `chance + margin_oracle`, `< oracle_easy_ceiling` |
| `margin_oracle` | Step 0 (separation above chance, below ceiling) |
| `noword_floor_band` (clean-G no-word bar) | Step 0, chance-derived |
| `intact_bar` (clean-G intact bar) | Step 0, from `intact_easy_ceiling` |
| band-ladder multipliers + lower-endpoint candidate | validity probe bracket (top = autonomous-success; bottom ≈ oracle-threshold approach) |
| `slow_fraction` (`SLOW` = fraction × `MODERATE`) | rig (a real slow-down, measured against toe length) |
| toe / rapid / plateau capacity-fraction cutoffs | illustrative 0–0.25 / 0.25–0.75 / final-20% |
| `tol_plateau` (S-curve signature) | rig (plateau-flatness tolerance) |
| `N_consec`, `X_pct` (clean-G sustainedness) | rig |

---

## 11. The line to hold (one sentence)

Band hardens the environment, never vision's access to B; the oracle is the line; a cell where
oracle-recoverability falls is the cap on the sweep — and wanting to push past it to force the no-word
arm down is the tell.

---

## 12. CC implementation amendments (2026-06-25/26) — pinned during the build, recorded here as canon

These resolve `[RECONCILE]`/operational gaps surfaced while building; the §0–§11 design is unchanged.

**12.1 Oracle operationalisation (R5).** `oracle_B_rec` (the F3 line and the `cleanG` oracle clause)
is a **substrate** oracle, not the raw `ceiling_B`: a **fresh-per-band** `HierarchicalPoolingModel`
at the cell's `(r_fine, σ, seed)`, **capacity forced open** (Δ2 unfrozen, no pooling penalty),
**B-supervised** (CE on member-marginal = `logsumexp`-over-groups logits, jointly with A),
**SIGReg active at deployed parity** (`pin.alpha_spread`, `pin.P`, on `emit=p@W` downstream of Δ2 —
read, not re-specified), recovery by **nearest-centroid** (no free head), **read-only** (never
backprops into the deployed encoders), with a **content-ablation guard** (ablate the B-axis →
recovery must collapse to ~chance). **F3 fires on the substrate oracle only** (raw-breach ⟹
substrate-breach in valid operation; "either" risks a too-strict cap inside clean-G). Band hardened
by **`r_fine↓` at fixed `σ_stim`** (single-variable; σ↑ would mechanically depress the raw oracle).

**12.2 Substrate oracle is the correct G1 instrument (sufficiency — do not re-open).** It tests
**representability**: B representable ⟹ a no-word-arm failure is "not acquired" (the gap-3 / clean-G
reading); B non-representable ⟹ F3. **No third case** — a deployed unsupervised dynamics-collapse
(e.g. Δ2-on-A) is an *acquisition* failure measured by the no-word arm, not the oracle's job.

**12.3 Superseded divergence gate (exp03 vacuous-F4 discipline — failure kept in canon).** Ran
first on HEAD `2b70d74` (record: `experiments/04_stage0_mvp/oracle_gate_record.json`).
- *Original pre-registration (FALSIFIED 2026-06-25):* a genuine deployed-regime (not
  coefficient-cranked) oracle-LOW/raw-HIGH divergence is producible by `r_fine↓` at `α=0.1`. **Not
  producible** — the B-supervised, capacity-open oracle OVER-performs raw; deployed SIGReg(0.1) has
  ~no effect:

  | r/σ | 12.5 | 7.5 | 5.0 | 3.5 | 2.5 | 1.7 |
  |---|---|---|---|---|---|---|
  | raw `ceiling_B` | 1.00 | 0.98 | 0.745 | 0.409 | 0.280 | 0.255 |
  | oracle (α=0.1) | 1.00 | 1.00 | 1.00 | 0.971 | 0.873 | 0.701 |
  | oracle (α=0) | 1.00 | 1.00 | 1.00 | 0.969 | 0.879 | 0.707 |

- *Re-pre-registered criterion (user-adjudicated 2026-06-26; PASSES):* non-degeneracy =
  **diverges from raw** (≥0.25 at some band) **AND content-driven** (ablation collapses at every
  band) **AND oracle-HIGH at B00** at deployed strength **AND alpha/P parity**. The empirical
  divergence is oracle-HIGH/raw-LOW (substrate is a stronger, content-driven probe than naive raw
  NC), which proves the oracle measures the substrate, not the raw input — and **vindicates "F3 on
  substrate only"** (raw is the weaker, earlier-capping probe).

**12.4 Leak rule struck.** The raw-low/substrate-high "leak" invalidation is **removed** (it is the
normal stronger-probe case here, per 12.3). The **content-ablation guard is the sole leak test**;
`ceiling_B_raw` is retained for **F3-diagnosis only** (env-saturation vs substrate-pathology when the
substrate oracle breaches). The **r/σ≈1 must-breach anchor** is kept (proves F3 can fire). The wide
interior (oracle ≥0.70 to r/σ≈1.7 while raw collapses by r/σ≈2.5) is a **favorable expectation**,
not an assumption — whether a clean-G window opens is the question the sweep answers.

**12.5 Other pinned items.** SLOW = schedule time-scaling (`t1,t2,ramp_steps,steps×1/slow_fraction`),
NOT a learning-rate change (scope-lock); per-row validity gate uses `max_coord_r2<0.9` and **excludes
`full_ols_r2`** (the §12.D Readout-D debt is not gated here); `capacity_fraction` self-normalised to
the run's own plateau as the cross-rate axis, with absolute `pooling_depth`/`capacity_fraction_abs`
logged alongside; toe/rapid/plateau cutoffs and `noword_eps` calibrated from the B00 trajectory /
measured floor spread (not flat literals); capacity-axis cross-rate grad-share is a real
*observation* (PAM trains on the unscaled clock → settling-time-before-split may surface), never
license to release the §12.B ramp.

**12.6 Verdict logic FROZEN before the surface exists (exp03 pre-registration — a 480-cell surface
needs it more, not less).** All thresholds are pinned in `sweep_config.SPEC` (hashed into `spec_hash`,
stamped on every row) and read by `analyze_sweep.classify_surface` — never tuned after the surface.
- S-curve signature (per seed): `delta_rapid > 0 ∧ delta_plateau ≤ tol_plateau` (`tol_plateau=0.05`);
  phase bands toe[0,0.25]/rapid[0.25,0.75]/plateau=final 20% in `capacity_fraction`, with a **±1-bin
  cutoff-robustness re-classification** reported per cell.
- clean-G sustainedness: `cleanG_flag` holds ≥`n_consec`=3 consecutive windows **AND** ≥`x_pct`=20%
  of `[0,T_run]` (stricter-of-two).
- Per-cell verdict thresholds (operationalizing §8's qualitative terms over the ≥20-seed
  distribution): `verdict_sig_bar=0.30` ("materially >0"), `verdict_f1_cutoff=0.10` (**F1** flat),
  `verdict_clean_bar=0.30` (cleanG "material"), `verdict_auto_high=0.70` (**F2** autonomous-everywhere).
- **F3** = substrate `oracle_floor_breach` (oracle_B_rec < `oracle_threshold`=0.4375 from Step 0);
  the Step-0 `[RECONCILE]` bars (`oracle_threshold`, `noword_floor_band`=[0.25,0.316], `intact_bar`
  =0.404) are in `calibration.json` and stamped into each run's `.meta.json`.
- **paradigm-positive** = an *interior* cell with `s_curve_signature_frequency ≥ sig_bar` ∧
  `cleanG_frequency ≥ clean_bar` ∧ `autonomous_resolution_frequency < easy-band autonomous` ∧ not F3.
- Consistency-checks-NOT-findings (reported, never license): capacity-axis rate-invariance (baked in
  by time-scaling); `SLOW T95 > MODERATE T95` (scaling sanity); plateau `capacity_fraction_abs` falls
  across the ladder; the r/σ≈1 anchor breaches. Empty-gap (autonomous-loss and F3-onset coincident,
  no clean window) is a legitimate pre-registered result, not a rig failure.
