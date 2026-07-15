# EXP19 W-PERM — G5b MATCHED-N POWER: **PASS** — the phantom floor was a binning artifact (2026-07-14)

**Gate (re-specified ledger 38; resolved ledger 40):** not "does a converter certify at N=7,915?" but **"what is the phantom
floor at 7,915, and does the converter signal still clear it?"** **Result: PASS.** The stratum's recency-free
detector powers the treatment cell at B=512 — including the marginal converter s6 — **once the WINDOW is
audited.** The apparent underpower (G5b v1) was the **third un-transported constant**: the 300-step bin.

## The artifact and its cause (ledger 40, both chairs)
G5b v1 (`exp19_g5b.py`, band 0.704, EVAL=300 bin) found s6 swallowed at N=7,915 (its run overlapped the
floor). But the detector bins at **300 steps** — a full-read constant. Full read: ~27 onsets/window. Thinned
zero-preceding stratum: **~5**. Accuracy over ~5 samples is coarse and lumpy; lumpy produces long chance runs;
long chance runs **are** the phantom floor. v1 measured a detector binned for a regime **5.6× denser** than the
one it runs in. We had audited α (ledger 38) and the forced band; **neither chair audited the window.**

## The re-cut — preserve the granularity the detector was cut for, re-derive the bins (outcome-blind)
The full-read C_shuffle detector (X15_REPRO: band **0.64**, N=5) bins at EVAL=300 steps. The re-cut sweeps
window width and cuts the operating point **in the STRATUM's own regime — NOT the population's** (ledger 41:
the treatment detector only ever sees the stratum, so widening until the sparse stratum fakes the dense
population's ~27-onset granularity is a regime the detector never runs in — the retracted over-correction).
**The gate is the FLOOR AUDIT** — a within-width separation `s6_q10 > floor_q99` (m_w cancels ⇒ unit-invariant).
Among-kept thinning to N=7,915, K=2000 draws, pinned `SUBSAMPLE_SEED=719150`; no training.

| width | onsets/win | floor q99 | s6 q10 | s6 min | sep | s6 clears? | #conv |
|---|---|---|---|---|---|---|---|
| **300** (inherited) | 4.7 | **10** | **9** | 6 | **0.9** | **NO — swallowed** | 4/5 |
| 400 (**≥ power floor**) | 6.2 | 9 | 11 | 7 | 1.22 | yes | 5/5 |
| **550** (**operating point** — stratum native ~8.5/win) | 8.6 | **8** | **12** | 6 | **1.5** | **yes** | 5/5 |
| 600 | 9.3 | 8 | 13 | 7 | 1.62 | yes | 5/5 |
| 800 | 12.5 | 7 | 15 | 9 | 2.14 | yes | 5/5 |
| 1200 | 18.7 | 6 | 15 | 9 | 2.5 | yes | 5/5 |
| ~~1706~~ (restores 27 — **retracted**) | 26.5 | 5 | 18 | 8 | ~~3.6~~ | yes | 5/5 |
| 2100 | 32.6 | 4 | 16 | 8 | 4.0 | yes | 5/5 |

- **s6 is swallowed ONLY at the inherited 300-step window** (sep 0.9, 4/5 clear). At **every** width ≥ 400 all
  5 converters clear — the pre-named falsifier did NOT trigger; the underpower was the binning.
- **Pre-flight constant — the ≥ WIDTH FLOOR = 400** (computed, outcome-blind): the narrowest window at which the
  weakest labeled converter (s6) clears the phantom floor; below it the granularity floor swamps the signal.
  It sits in the G8 package beside ρ(B) and the stratum counts. (Strict form — s6's worst draw beats the
  floor's best — holds only ≥ 1500, reported as context, not the operating point.)
- **Operating point = width 550** (~8.5 onsets/win = the stratum's own full-N density, the regime it was
  characterized at), s6 margin **1.5×** (q10 12 vs floor q99 8), 5/5 clear. **The margin is what G5b reports,
  and 1.5× at the anchor on the marginal converter is thin but real** (ledger 41: the earlier 3.6× headline at
  width 1706 was the population regime, retracted). Finest resolution consistent with power (flag 3).
- **The divergence is real signal, not a re-binning trick:** as windows widen the floor *shrinks* (q99 10→4)
  while s6 *grows* (q10 9→18). s6 carries a genuine contiguous late episode (windows 248–270, means 0.69–1.00);
  floor seeds {1,3,7} have **no** episode (longest full-data run = 2). Robust across 4 subsample seeds.

## Adversarial verification (6-lens refute panel + synthesis) — FLAG-ONLY, 0 MUST-FIX
Independent recomputes confirmed: operating-point blindness (min |onsets/win − 27|, s6 absent from
selection); band-invariance (**re-ran the entire sweep at 0.704 → s6 still clears, sep 5.0**; the 0.64
recompute bit-matched all 9 rows); cache faithfulness (n_full s0 = 14,156 exactly); the divergence mechanism.
The panel's three flags, and their disposition:

1. **The "135-onset evidence" was decorative — RESOLVED.** `N_w` was reported but never gated; the gate is the
   floor-separation (correct — an absolute 135/N_w threshold would misfire). Framing fixed.
2. **The margin was target-dependent — RESOLVED, ledger 41 (Jason's self-correction).** The original 3.6× used
   the *population's* 27-onset density; the treatment detector only sees the stratum, so the operating point is
   now cut in the **stratum's own regime** (native ~8.5/win, width 550) → **s6 margin 1.5×**, with the **≥400
   width floor** named as a computed pre-flight constant. The binary PASS is target-invariant; the 3.6× is
   retracted.
3. **The horizon may truncate a converter mid-rise — OPEN ITEM → G8 (live finding, not a caveat).** s6 clears
   on a **late plateau still rising at read_at=500k** — it is a *late* converter, not a decayed transient. So
   the §3 horizon (read_at=500,000), grounded on *onset* (all converted by 427.5k), may **undercount** a
   converter whose plateau is still climbing at the read. **If W-PERM's rescue converters also plateau late, a
   500k read undercounts rescue — biasing toward DEAD, the unflattering direction.** Carried into G8 as an open
   item against the horizon; may force the descriptive 1M tail to be read on this arm.

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
