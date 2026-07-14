# EXP19 W-PERM — G5b MATCHED-N POWER: **PASS** — the phantom floor was a binning artifact (2026-07-14)

**Gate (re-specified, ledger 38→39):** not "does a converter certify at N=7,915?" but **"what is the phantom
floor at 7,915, and does the converter signal still clear it?"** **Result: PASS.** The stratum's recency-free
detector powers the treatment cell at B=512 — including the marginal converter s6 — **once the WINDOW is
audited.** The apparent underpower (G5b v1) was the **third un-transported constant**: the 300-step bin.

## The artifact and its cause (ledger 39, both chairs)
G5b v1 (`exp19_g5b.py`, band 0.704, EVAL=300 bin) found s6 swallowed at N=7,915 (its run overlapped the
floor). But the detector bins at **300 steps** — a full-read constant. Full read: ~27 onsets/window. Thinned
zero-preceding stratum: **~5**. Accuracy over ~5 samples is coarse and lumpy; lumpy produces long chance runs;
long chance runs **are** the phantom floor. v1 measured a detector binned for a regime **5.6× denser** than the
one it runs in. We had audited α (ledger 38) and the forced band; **neither chair audited the window.**

## The re-cut — preserve the granularity the detector was cut for, re-derive the bins (outcome-blind)
The full-read C_shuffle detector (X15_REPRO: band **0.64**, N=5) is calibrated for ~27-onset-window
granularity. Re-bin the stratum to restore that density (sweep of window widths), **operating point chosen on
the null** (the width restoring ~27 onsets/window = 1706 steps), never on s6. **The gate is the FLOOR AUDIT**
— a within-width separation `s6_q10 > floor_q99` (m_w cancels ⇒ the separation ratio is unit-invariant). No
training; among-kept thinning to the treatment's density, K=2000 draws, pinned `SUBSAMPLE_SEED=719150`.

| width | onsets/win | floor q99 | s6 q10 | sep | s6 clears? | #conv clear |
|---|---|---|---|---|---|---|
| **300** (inherited) | 4.7 | **10** | **9** | **0.9** | **NO — swallowed** | 4/5 |
| 450 | 7.0 | 9 | 11 | 1.22 | yes | 5/5 |
| 600 (~stratum-native) | 9.3 | 8 | 13 | 1.62 | yes | 5/5 |
| 900 | 14.0 | 7 | 14 | 2.0 | yes | 5/5 |
| 1200 | 18.7 | 6 | 15 | 2.5 | yes | 5/5 |
| 1500 | 23.3 | 5 | 18 | 3.6 | yes | 5/5 |
| **1706** (restores 27) | 26.5 | **5** | **18** | **3.6** | **YES** | 5/5 |
| 2100 | 32.6 | 4 | 16 | 4.0 | yes | 5/5 |
| 3000 | 46.6 | 4 | 12 | 3.0 | yes | 5/5 |

- **s6 is swallowed ONLY at the inherited 300-step window.** At **every** width ≥ 450, s6 clears and all 5
  converters clear — a 6.7× range; the operating-point choice is non-pivotal.
- At the operating point (1706), s6 clears **3.6×** (q10 18 vs floor q99 5); **even s6's minimum draw (8–11)
  exceeds the floor's max (7–8)**. Robust across 4 subsample seeds (719150/1/42/2026).
- **The divergence is real signal, not a re-binning trick:** as windows widen the floor *shrinks* (q99 10→4
  in window units) while s6 *grows* (q10 9→18). s6 carries a genuine contiguous late episode (windows
  248–270, per-window means 0.69–1.00); the floor seeds {1,3,7} have **no** episode (longest full-data run =
  2 windows). Wide binning averages chance toward the sub-band truth while bridging s6's real super-band
  stretch — the signature of a finite-extent episode.
- **The pre-named falsifier did NOT trigger** (floor doesn't collapse AND s6 fails ⇒ genuine underpower). s6
  clears; the underpower was the binning.

## Adversarial verification (6-lens refute panel + synthesis) — FLAG-ONLY, 0 MUST-FIX
Independent recomputes confirmed: operating-point blindness (min |onsets/win − 27|, s6 absent from
selection); band-invariance (**re-ran the entire sweep at 0.704 → s6 still clears, sep 5.0**; the 0.64
recompute bit-matched all 9 rows); cache faithfulness (n_full s0 = 14,156 exactly); the divergence mechanism.
Three flags ride alongside, **all non-blocking**, carried honestly:

1. **The "135-onset evidence" is decorative.** `N_w` is reported but does not gate — the gate is the
   floor-separation. (This is *correct*: an absolute 135/N_w threshold would misfire, since at the restored
   density N_w≈5 ≤ the floor's own max.) The framing, not the computation.
2. **The 3.6× magnitude is target-dependent.** 27 onsets/window is the *all-onset* full-read density; the
   audited stratum is zero-preceding (native full-N density ~8.5/win → width ~600), where s6 clears **~1.6×**,
   not 3.6×. **The binary PASS is target-invariant (s6 clears at every width ≥450); only the margin is not.**
3. **Wide-window run-length measures block-contiguity, not conversion strength** (it reorders the converters),
   and s6's clearance rides a **late plateau still rising at the 500k read boundary** (s6 is a late converter,
   not a decayed transient — this also refutes the "widening merges a decayed episode" worry). A caveat for
   eventual **B\*** estimation: the temporal resolution at the restored density is ~293 windows.

## What it means
The recency-free stratified detector, once the window is audited in-regime, powers all 5 converters at the
treatment's density (B=512, N=7,915) — the marginal s6 clears the phantom floor. **The recency defence stands
at the ρ≤0.05 anchor.** The rejected alternatives were traps: re-anchoring to B=32 (ρ=0.549) re-enters the
FALSE-DEAD zone the ρ≤0.05 floor forbids; accepting 4/5 blinds the detector at the knee where conversion is
weak by definition, which could manufacture RESCUE-AT-CEILING-ONLY.

## Provenance / reproduction
- Artifact (the mis-specified v1): `exp19_g5b.py --run` → `exp08/exp19_g5b_phantom_floor.json` (band 0.704,
  300-bin; s6 swallowed).
- Cause + fix: `exp19_g5b_rebin.py --cache-wave` (wave-indexed stratum onsets, gitignored, regenerable) then
  `--sweep` → `exp08/exp19_g5b_rebin_sweep.json`. Panel record: `exp08/exp19_g5b_panel.json`.
- Pinned `SUBSAMPLE_SEED=719150`, `SIM`-free (subsampling only); deterministic `torch.set_num_threads(1)`;
  band 0.64 = committed X15_REPRO C_shuffle detector; committed code untouched.
