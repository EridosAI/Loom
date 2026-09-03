# Experiment 01 — Pooling Substrate Validation Rig

Isolated, falsifiable test of the project's growth substrate: **soft-tied weight
pooling** that opens resolution (unpool) and reclaims it (re-pool) under local
signals. Full design and the pre-registered failure conditions are in
[`SPEC.md`](SPEC.md); measured outcomes are in [`RESULTS.md`](RESULTS.md)
(auto-generated).

## Run it

```bash
pip install -r requirements.txt
python run_tests.py            # full suite + r_fine/sigma sweep, writes RESULTS.md + figures/
python run_tests.py --quick    # smaller/faster smoke test
```

CPU-only, deterministic (fixed seeds), ~40 s for the full suite. Figures land in
`figures/` (regenerable, gitignored); `RESULTS.md` is committed. The process exits
non-zero if any pre-registered failure condition trips.

## Files

| file | role |
|------|------|
| `data.py` | hierarchical Gaussian generator (`R_coarse`, `r_fine`, `sigma`) + nesting check (SPEC §1) |
| `model.py` | additive-residual prototype model: `W_i = base + Δ1_{g(i)} + Δ2_i`, per-level λ penalties (SPEC §2) |
| `metrics.py` | coarse/fine accuracy, residual norms, within-group spread, intra-group gradient signal (SPEC §3) |
| `harness.py` | `StepSchedule` (clock-led unpool) + `AdaptiveRepool` controllers, instrumented training loop |
| `run_tests.py` | Tests A–D with pre-registered pass/fail lines; writes `RESULTS.md` |
| `plots.py` | per-run and overlay figures |

## What the tests check (and how to read a failure)

- **A — symmetry break** (make-or-break): soft-tied members must *diverge* once
  sub-structure is present; the hard-tie control (`Δ2≡0`) must fail; free is the
  upper reference. Fails ⇒ the substrate cannot differentiate from a pooled state.
- **B — pool → unpool → differentiate**: coarse must reach ceiling while pooled;
  fine must lift only when resolution opens; gradual unpool must beat the
  always-pooled baseline and match always-unpooled. Includes the required
  `r_fine/σ` sweep.
- **C — re-pool**: after full differentiation, when the pull-apart force is
  sustained low, λ₂ is ramped back up; `Δ2` must collapse and **coarse value must
  survive** (graceful coarsening, not collapse). C1 = signal removed from input,
  C2 = signal present but unrewarded.
- **D — signal behaviour** (observational): the gradient signal should rise while a
  group differentiates and fall once it settles. Flags, does not gate.

## Two implementation choices worth knowing

These are deliberate and documented in the module docstrings / `RESULTS.md`:

1. **Prototype (nearest-prototype) readout, not a free linear head.** A free linear
   head can separate clusters that differ along any single shared direction, so it
   *leaks* the fine distinction through the pooled weights — making capacity *not*
   track the pooling state (the SPEC §0 false-negative trap). With a prototype
   readout, a pooled group is one prototype in one place and genuinely cannot
   resolve its fine sub-clusters until `Δ2` opens. This preserves what §7 requires:
   soft (not hard) tie, per-level relaxation, graceful re-pool.
2. **Re-pool triggers on the pull-apart force magnitude** ("members no longer pulled
   apart"), with the directional cosine logged alongside for Test D. Magnitude stays
   well-defined when gradients vanish or the fine head is untrained; a bare cosine
   does not.

## Non-goals

No cortices/PAM, no convergence loop, no real perceptual data. This rig is the
substrate **alone** (SPEC §6).
