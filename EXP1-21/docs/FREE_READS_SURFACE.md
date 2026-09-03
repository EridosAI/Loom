# FREE-READS SURFACE — batch cycle (single consolidated surface; seat verifies ONCE at the end)

**Status: BATCH RESULT (CC, 2026-07-13). Executes `docs/FREE_READS_MEMO.md` verbatim — recipes as
committed, zero improvisation. Parent HEAD at generation: `23fb8c7`. The design fence HOLDS: no read
result has been consumed by any design; every judgment call routes to the design seat, which verifies
this surface once, in full.** All four reads ran read-only; each is a standalone committed script
writing one JSON; each JSON was regenerated and BYTE-COMPARED (determinism double-run, all identical).
No mid-stream halt condition fired (no recipe-cannot-execute, no determinism mismatch, no
record-integrity failure).

> **SEAT VERIFICATION: PASS (single pass, 2026-07-13).** Scope/authorship/fence verified; all four
> sha256 recomputed and matched; read (ii) reproduced independently (22 profile numbers exact); read
> (i) confirmed a structural isometry (nuis_axes ← `basis @ Q.t()`, Q QR-orthogonal, `conflict_stream.py:59`
> — the 1.0000004 is f32 noise on a theorem); reads (iii)/(iv) confirmed to reuse committed machinery
> verbatim. **Rulings:** (i) no gain floor; (ii) premise-consistent, kill not fired; (iii) latent; (iv)
> kinematic-indicated, bridge holds. Two method notes logged below as riders (verdicts unchanged).

---

## ✔ Entry-15 correction — RESOLVED 2026-07-13 (seat supplied the text; applied in place)

> **RESOLVED (2026-07-13):** the seat confirmed the miss was theirs (text existed only in chat) and
> relayed the corrected row; `progress_log.md` ledger row 15 is now updated in place, correction marked.
> The batch-time note below is retained as provenance.

**[Batch-time state, superseded:]**

The relay directed: *"apply the corrected row text from the seat's last report in place."* **No seat
report is present in any accessible artifact** — no commit since `23fb8c7`, nothing in `docs/`,
`scratchpad/`, or the session store carries a corrected entry-15 / lens-1 row, and the corrected text
is not in the relay itself. Per report-don't-patch I did **not** fabricate a canon row. The catch-ledger
entry 15 in `progress_log.md` stands unchanged pending the seat's actual text. **Routed to Jason: relay
the corrected row text (or point to the report file) and it applies in place, correction marked,
provenance line kept — a one-line follow-up, outside this batch.**

---

## Headline table

| Read | Key numbers (pooled, 8 seeds) | Memo consequence | Fired? |
|------|-------------------------------|------------------|--------|
| **(i) render-gain** (memo §i; v1.2 §4) | anisotropy_ratio **1.0000004** (max); per-axis gain ∈ **[0.99999979, 1.00000013]**; cross-axis leakage ≤ **2.0e-7**; realized ratio **0.99999999**; random-pair ratio **0.99999999** | severe anisotropy → gain floor in scatter F5 + qualifies "as tested" | **NO** — isotropic to f32 precision; no floor indicated; "as tested" not qualified perceptually. ("severe" threshold unpinned → routes) |
| **(ii) CWP step-0** (memo §ii; v1.2 §5.2/§6) | word boundary-drop (p1−p13-48) **+0.116** orbit / **+0.138** A; vis within-slope (p13-48−p2) **−0.066** orbit / **−0.077** A | within-dwell NOT low-surprise massed → CWP closes before it opens | **ROUTES** — profile is *consistent* with low-surprise-massed (boundary spikes, within-dwell falls, both channels); kill not indicated. Seat rules. |
| **(iii) rung-3.5 bg** (memo §iii; v1.2 §1) | bg⟂member corr **0.033** ≤ null99 **0.071** (8/8 independent); member-decode **0.0685** mean / **0.0697** max vs chance **0.0625** (+0.006) | bg carries no member info → rung 3.5 latent → L3 = generalization arm | **ROUTES** — near-chance decode + corr within null ⇒ latent indicated. Seat rules. |
| **(iv) EXP13 kinematics** (memo §iv; OPS §1.6) | lawful np11 **0.624** / tr11 **0.220** / path11 **2.07**; lawscram np11 **0.087** / tr11 **0.750** / path11 **19.5**; Δnp11 **+0.537** | kinematic wall bridges lawful line to ladder; non-kinematic keeps EXP13 separate | **ROUTES** — lawful wall strongly *directed* (np11 0.62 vs scramble 0.087) ⇒ kinematic indicated. Seat rules. |

No pre-named consequence auto-fires a floor or a program-close; all four route to seat verification.

---

## Per-read detail

### (i) Render-gain audit — `exp08/freeread_1_render_gain.json`
**Method** (JSON `method`): pose = K=4 nuisance coeffs; render(pose) = `pose @ nuis_axes`
(`exp12_fabric.py:139,353`). per_axis_gain = ‖axes_k‖; cross_axis_leakage = max_{i≠j}|axes_i·axes_j|;
anisotropy_ratio = max/min of ‖u@axes‖ over 20000 random unit u∈ℝ^K; realized_ratio = ‖Δrender‖/‖Δpose‖
over within-dwell consecutive frames; randompair_ratio = same over 20000 random family-marginal pose
pairs. float64. Arm `exp12_dwell_orbit`, window 100000 (X17_SELECT_T; ratio is T-invariant under the
isometry). **Finding:** the pose→render map is a linear isometry (orthonormal nuisance axes), measured
isotropic to f32 precision — a random orbit plane is NOT perceptually weak, so no ratification-class
gain floor is *indicated* for scatter's ball sampling, and §10.27's "did NOT convert as tested" is not
qualified on perceptual-weakness grounds. Per-seed anisotropy_ratio: 1.00000015, 1.00000028,
1.00000018, 1.00000034, 1.00000017, 1.00000035, 1.00000015, 1.00000021 (seeds 0–7).

### (ii) CWP step-0 — `exp08/freeread_2_cwp_step0.json`
**Method:** per-within-dwell-position pooled mean of `pos_err_word`/`pos_err_vis` over post-acq columns
(equal weight per column — the committed `_recency_gradient` pooling). Pure committed-record read.
**Post-acq pooled profile by within-dwell position:**

| arm | channel | p1 | p2 | p3 | p4-6 | p7-12 | p13-48 |
|-----|---------|----|----|----|------|-------|--------|
| orbit_L1 | word | 0.7015 | 0.6920 | 0.6862 | 0.6770 | 0.6500 | 0.5857 |
| orbit_L1 | vis  | —      | 0.2985 | 0.2940 | 0.2826 | 0.2597 | 0.2330 |
| A_dwell  | word | 0.6996 | 0.6942 | 0.6858 | 0.6669 | 0.6269 | 0.5614 |
| A_dwell  | vis  | —      | 0.3150 | 0.3101 | 0.2979 | 0.2730 | 0.2385 |

Both channels, both arms: monotone-falling within the dwell (highest right after the boundary jump,
decaying to a low plateau) — the boundary-spike + within-dwell-decay shape CWP's premise predicts. The
kill condition ("within-dwell updates NOT low-surprise massed") is therefore **not indicated** by these
numbers; the ruling on whether this *is* "low-surprise massed" routes to the seat.

> **[Seat rider, 2026-07-13 — method note, verdict UNCHANGED.]** This read pools the FULL record while
> citing the `_recency_gradient` pooling, so the arm windows are unequal (orbit ~1M vs A ~500k).
> Recomputed under a matched **[0,500k)**: word boundary-drops **0.1412** (orbit) / **0.1382** (A); vis
> within-slopes **−0.0859** / **−0.0765** — shape identical, premise-consistent read stands.

### (iii) Rung-3.5 background member-information — `exp08/freeread_3_bg_member_info.json`
**Method:** (a) committed assert-(4) statistic `F12._max_abs_corr(bg[:S], label-triple)` vs
exchangeability null99 (`F12._dwell_perm_labels`, keys 64000+i, N_NULL=200, S=12000); (b) nearest-centroid
member(16)-from-bg accuracy over the full 100000 window vs chance 1/16. Arm `exp12_dwell` (bg is
arm-independent). **Per-seed:** corr_obs 0.035/0.034/0.026/0.044/0.024/0.028/0.039/0.033, each ≤ its
null99 (0.069/0.089/0.077/0.072/0.060/0.072/0.064/0.066); member-decode 0.0697/0.0658/0.0682/0.0695/
0.0680/0.0684/0.0691/0.0694 (chance 0.0625). Background decodability sits at chance; correlation sits
within the independence null on all 8 seeds. Whether this reads as "no member information" (rung 3.5
latent → L3 a generalization arm) routes to the seat.

> **[Seat rider, 2026-07-13 — method note, verdict UNCHANGED.]** The nearest-centroid decode is
> **in-sample** (centroids fit and scored on the same window); the **+0.006** over chance is in-sample
> centroid bias, mechanically expected, **not** member information — do not read 0.0685 > 0.0625 as a
> leak. The calibrated corr-vs-null99 (**8/8 within null**) is the decisive statistic; **latent** stands.

### (iv) EXP13 kinematics — `exp08/freeread_4_exp13_kinematics.json`
**Method:** committed `exp17_score.measure_kinematics` run UNCHANGED, fabric source redirected to
`exp13_arms.build_exp13(<arm>)`; np11/tr11/path11 over realized k==11 contained dwells, net/path f64,
traverse f32 radii, per-step f64. Window 100000, matched lawful vs lawscram. **Pooled:** lawful
np11 0.6243 / tr11 0.2199 / path11 2.072 / perstep 0.2025 / cross 1.644; lawscram np11 0.0873 /
tr11 0.7495 / path11 19.526 / perstep 1.9032. Lawful per-seed np11 tightly clustered 0.617–0.630.
The lawful drift is strongly *directed* (net/path 0.62) against its scrambled control (0.087,
tremble-like); whether that certifies "the wall was kinematic" routes to the seat.

---

## Double-run determinism confirmations

Each script was run twice; the output JSON is byte-identical (sha256 of the regenerated file):

| read | sha256 | double-run |
|------|--------|-----------|
| freeread_1_render_gain.json | `add228afe1ca2be3a6667a974744188da55cbf82c97ec7b8e1ebda23ea15cd39` | BYTE-IDENTICAL |
| freeread_2_cwp_step0.json | `6666ce4c98769607d93ca8999e672f0c422d1c58e429a53b279fcf495d09334b` | BYTE-IDENTICAL |
| freeread_3_bg_member_info.json | `50fc00b09292221af59c8c14c6b6574a69af5b2e37de62568868bb97a0eabf3f` | BYTE-IDENTICAL |
| freeread_4_exp13_kinematics.json | `e99f77661a2c5756b445098e433fe85d1b28b7f53c43d1d0b4c79eec4c11a3fb` | BYTE-IDENTICAL |

All builds `torch.set_num_threads(1)`; all sampling on fixed generator seeds.

---

## What this binds for SCATTER's F5 (implications only — no design; seat rules)

Stated, not designed; every clause is [PENDING-SEAT-VERIFICATION]:

- **Render-gain floor: not indicated.** The pose→render map is measured isotropic (gains 1.0±2e-7,
  cross-leakage ≤2e-7). RED_TEAM **F5**'s selection statistics (per-step displacement contrast +
  distinct-pose coverage + confusion-bound ceiling) can be filled **without** a ratification-class
  render-gain floor on ball sampling, *if the seat concurs that f32-precision isotropy = no anisotropy*.
  Corollary: §10.27's "as tested" needs **no** perceptual-weakness qualifier.
- **"As tested" scope:** the L1 orbit delivered faithful pose-proportional appearance change; the
  DIRECTION-ONLY result is not a render-gain artifact. (States the close's robustness; changes nothing.)
- **CWP step-0 does not gate scatter** (it gates the CWP program, behind the ladder). Reported here
  because it rode the same batch; the profile is premise-consistent, so the CWP slot is **not** closed
  by this read.
- **Rung-3.5 → L3 framing** (not scatter): near-chance background decodability points L3 toward a
  generalization-pressure arm; irrelevant to scatter's F5 statistics, recorded for the ladder.
- **EXP13 kinematics** bears on the lawful-line bridge, not on scatter's F5 directly; the directedness
  contrast is logged for the seat's sequencing call.

---

## Provenance

**Scripts (committed this batch):** `experiments/05_attention_sculpting/freeread_1_render_gain.py`,
`…/freeread_2_cwp_step0.py`, `…/freeread_3_bg_member_info.py`, `…/freeread_4_exp13_kinematics.py`.
Parent HEAD at generation `23fb8c7`.

**Inputs pinned by filename → producing commit:**

| input | producing commit |
|-------|------------------|
| exp14_exp12_dwell_orbit_s{0..7}_exp17verdict.json (records; read (ii)) | `c1a3df5` |
| exp14_exp12_dwell_s{0..7}_verdict.json (records; read (ii)) | `f039ccd` |
| exp12_arms.py / exp12_fabric.py / exp17_score.py (build + measurer; reads i,iii,iv) | `0fb3e4c` |
| exp13_arms.py (build; read iv) | `110ef50` |
| exp13_fabric.py (build; read iv) | `e2ec777` |

Each JSON carries its own `method`, `memo_section`, `recipe`, `inputs.code_modules`, and `consequence`
block. Fabric builds are deterministic (threads=1); reads (i)/(iii)/(iv) rebuild the fabric from the
committed generators, read (ii) is a pure committed-record read.
