# Characterisation Sweep — response surface

commit `2b70d743885ce75d2d3c4435c39844bbfe70dc6a`  spec_hash `d1f0936c92e1`  runs `runs`

**Overall:** no-paradigm-positive-cell (see F-tags / surface)

bars (Step 0): intact_bar=0.404  noword_floor_band=[0.25, 0.31619797301171215]  oracle_threshold=0.438

| band | rate | r/σ | oracle | s_curve_freq | robust | cleanG_freq | autonomous_freq | F3 | invalid |
|---|---|---|---|---|---|---|---|---|---|
| 0 | MODERATE | 7.50 | 1.00 | 0.80 | True | 0.00 | 1.00 | False | 0.00 |
| 0 | SLOW | 7.50 | 1.00 | 0.95 | True | 0.00 | 1.00 | False | 0.00 |
| 1 | MODERATE | 6.94 | 1.00 | 0.95 | True | 0.00 | 1.00 | False | 0.00 |
| 1 | SLOW | 6.94 | 1.00 | 1.00 | True | 0.00 | 1.00 | False | 0.00 |
| 2 | MODERATE | 6.37 | 1.00 | 0.90 | True | 0.00 | 1.00 | False | 0.00 |
| 2 | SLOW | 6.37 | 1.00 | 1.00 | True | 0.00 | 1.00 | False | 0.00 |
| 3 | MODERATE | 5.81 | 1.00 | 1.00 | True | 0.00 | 0.95 | False | 0.00 |
| 3 | SLOW | 5.81 | 1.00 | 1.00 | True | 0.00 | 0.95 | False | 0.00 |
| 4 | MODERATE | 5.25 | 1.00 | 0.80 | True | 0.00 | 1.00 | False | 0.00 |
| 4 | SLOW | 5.25 | 1.00 | 1.00 | True | 0.00 | 0.90 | False | 0.00 |
| 5 | MODERATE | 4.68 | 0.99 | 0.90 | True | 0.00 | 0.60 | False | 0.00 |
| 5 | SLOW | 4.68 | 0.99 | 1.00 | True | 0.00 | 0.60 | False | 0.00 |
| 6 | MODERATE | 4.12 | 0.99 | 0.85 | True | 0.00 | 0.40 | False | 0.00 |
| 6 | SLOW | 4.12 | 0.99 | 1.00 | True | 0.00 | 0.55 | False | 0.00 |
| 7 | MODERATE | 3.56 | 0.97 | 0.80 | True | 0.00 | 0.15 | False | 0.00 |
| 7 | SLOW | 3.56 | 0.97 | 1.00 | True | 0.00 | 0.00 | False | 0.00 |
| 8 | MODERATE | 2.99 | 0.93 | 0.85 | True | 0.00 | 0.00 | False | 0.00 |
| 8 | SLOW | 2.99 | 0.93 | 0.95 | True | 0.00 | 0.00 | False | 0.00 |
| 9 | MODERATE | 2.43 | 0.88 | 0.95 | True | 0.00 | 0.00 | False | 0.00 |
| 9 | SLOW | 2.43 | 0.88 | 1.00 | True | 0.00 | 0.00 | False | 0.00 |
| 10 | MODERATE | 1.86 | 0.77 | 0.90 | True | 0.00 | 0.00 | False | 0.00 |
| 10 | SLOW | 1.86 | 0.77 | 1.00 | True | 0.00 | 0.00 | False | 0.00 |
| 11 | MODERATE | 1.30 | 0.58 | 0.95 | True | 0.00 | 0.00 | False | 0.00 |
| 11 | SLOW | 1.30 | 0.58 | 1.00 | True | 0.00 | 0.00 | False | 0.00 |

## Per-rate F-pattern (F2/F4 relational across the band axis)

- **MODERATE**: F2_autonomous_everywhere=False  F4_cleanG_only_easy=False
- **SLOW**: F2_autonomous_everywhere=False  F4_cleanG_only_easy=False

---

## Interpretation & Verdict — EMPTY-GAP (pre-registered legitimate outcome)

The three pre-registered reads (computed, not eyeballed; 12 bands × 2 rates × 20 seeds, frozen
verdict thresholds in spec_hash `d1f0936c92e1`):

- **(a) Does a clean Readout-G window open in the interior? — NO.** `cleanG_frequency = 0.00` at
  every one of the 24 cells.
- **(b) Does PAM-grad share rise through the rapid phase? — Technically yes, but non-discriminating
  and non-load-bearing.** `s_curve_signature_frequency` = 0.80–1.00 at *all* bands (per-seed
  toe≈0.58 → rapid-peak≈0.78 → plateau≈0.58); it reads identically at easy bands where the word is
  provably inert as in the interior. So the rising PAM share is **not** evidence for
  evocation-as-teacher.
- **(c) Is the shape an S-curve? — A rise-then-settle bump in share, decoupled from acquisition**
  and riding on a non-saturating capacity curve (caveat below). Not the paradigm S-curve.

**The decisive measurement — gap-3 lift ≈ 0 at every band.** With `lift = intact_B_res −
noword_B_acq` (post-T_run tail mean):

| band r/σ | autonomous freq | intact_B | noword_B | lift |
|---|---|---|---|---|
| 7.50 (easy) | 1.00 | 0.48 | 0.48 | ~0.00 |
| ~4 (transition) | 0.40–0.60 | 0.37 | 0.37 | ~0.01 |
| 1.30 (interior) | 0.00 | 0.27 | 0.27 | ~0.00 |

`lift` over all 24 cells ranges −0.004 … +0.048 (mean ~0.01; per-cell SE≈0.013; no consistent
cross-rate sign) — **the word-present arm resolves B no better than the no-word arm at any band.**
The two arms decline in lockstep as the band hardens; they never separate, so no band has the word
lifting B above the autonomous floor → cleanG=0 everywhere.

**Why this is the empty-gap result, not F1–F4 and not a rig failure:**
- **Not F2** — autonomous resolution genuinely *falls* 1.00 → 0.00 (transition r/σ≈4–5). There IS a
  regime where vision cannot resolve B autonomously.
- **Not F3** — the substrate oracle (the G1 line) confirms B is representable across the whole
  admissible ladder (oracle ≥ threshold 0.4375; no breach); the F3 cap sits just below at r/σ≈1.0.
- **Not F1/F4 helpfully** — the S-curve signature is high but non-discriminating; cleanG is not even
  material at the easy end.
- The **autonomous-loss and the gap-3-teaching-failure coincide**: where vision fails autonomously
  (interior), the word *also* fails to teach it. No clean window exists between them — the
  pre-registered "empty gap" (spec §12.6 / failure taxonomy), a real read about the regime.

**Mechanistic reading.** gap-3 is **wired** (Phase-1: convergence-error gradient reaches the masked
vision slot; sweep: `pam_grad_share`≈0.6, PAM gradient present and rising in the rapid phase) but
**inert for acquisition** — the gradient arrives at vision yet does not drive B-differentiation.
Evocation, in this Stage-0 regime, is not a teacher. This sharpens Phase-1's "present but weak /
WRONG_REASON" into a clean negative across the full band×rate surface.

**Extended-length confirmation (convergence ruled out as the cause).** The MODERATE-vs-SLOW contrast
is itself a 2× length / +50% depth check (null lift at both). An extra run at the prime clean-G
candidates b7 (r/σ=3.56) and b8 (r/σ=2.99) at **3.4× the sweep length** (`LONG_STEPS=48000`, 4 seeds)
reached depth ≈ 1.37 / 1.29 — nearly 2× the sweep's MODERATE depth (~0.73) — and the lift remained
null: **b7 lift = −0.014 (sd 0.045), b8 lift = −0.011 (sd 0.033)**, neither intact arm clearing the
bar (0.404). So across a ~4× range of realized capacity (depth 0.73 → 1.37) the gap-3 lift does not
appear. (Transient cleanG "hits" at b7/b8 are scattered noise flickers rejected by the sustainedness
rule — consistent with the sweep's cleanG_frequency=0.)

**Caveats (honest).**
- **Capacity does not cleanly plateau** — Δ2 grows slowly without bound at λ2=0 (SLOW reaches ~50%
  higher depth than MODERATE; the extended run kept rising to 1.37). So `capacity_fraction`
  self-normalizes to a non-stationary level and `t_run ≈ steps` across the sweep. This weakens the
  S-curve *plateau* interpretation (the plateau is not a true asymptote) but does **not** touch the
  lift headline (measured at run-end; null at MODERATE, SLOW, and the extended length). A clean
  developmental clock would need a saturating capacity mechanism (out of scope for this sweep).
- The claim is "**no detectable lift within noise**," not "provably exactly zero."
- Scope: this is a negative for the paradigm bet **in this Stage-0 regime** (this operator, this
  no-stop-grad collapse-control, this stimulus structure, this run-length) — it does not prove
  gap-3 can never teach; other regimes are out of the scope-locked two-axis sweep.

**Bottom line.** The clean Readout-G window the project set out to characterise **does not exist at
this operating point**: gap-3 is present (gradient wired) but provides no associative-acquisition
lift over autonomous resolution at any band, rate, or capacity level tested. An honest, falsifiable
negative — exactly the outcome the pre-registration was built to be able to deliver.
