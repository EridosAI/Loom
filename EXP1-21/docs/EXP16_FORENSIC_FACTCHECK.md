# EXP16 RECENCY-FORENSIC FACT-CHECK (post-recovery; the provenance record behind AMD-2)

**Status: VERIFIED — four independent recomputes, all digit-exact (2026-07-10/11).** This document
is the in-repo provenance record the prereg's AMD-2 cites (it supersedes an ephemeral scratchpad
draft that predated the recipe recovery — panel BD-9; that draft's C/D rows carried full-run
values and must not be cited).

## The claim under check

Design-seat original (ratified draft, design chat 2026-07-10): *"dwelled pos_err_word gradient
0.692→0.582 / 0.694→0.579 vs shuffled flat"* — the capture-not-collapse forensic motivating EXP16.

## The two recipes, both reproducing from the committed EXP14 verdict records {0–7}

Per-eval-column `pos_err_word` position buckets (p1, p2, p3, p4-6, p7-12, p13-48), pooled across
seeds with equal column weight:

**Recipe A — ALL post-acquisition columns (t ≥ acquisition_onset; the CANON recipe, AMD-2):**

| arm | p1 | p2 | p3 | p4-6 | p7-12 | p13-48 | Δ(p1−p13-48) |
|---|---|---|---|---|---|---|---|
| A_dwell | 0.6915 | 0.6859 | 0.6774 | 0.6581 | 0.6174 | 0.5499 | **+0.1416** |
| B_12bc_dwp | 0.6930 | 0.6886 | 0.6825 | 0.6645 | 0.6236 | 0.5381 | **+0.1549** |
| C_shuffle | 0.6503 | 0.6504 | 0.6500 | 0.6499 | 0.6500 | 0.6502 | +0.0001 |
| D_split | 0.6403 | 0.6408 | 0.6403 | 0.6408 | 0.6407 | 0.6409 | −0.0006 |

Both dwelled arms **strictly monotone across all six buckets**. Shuffled controls **flat**:
spread (max − min across the six buckets) C = 0.0005, D = 0.0006. Post-acquisition column counts
(of 13,328 full-grid each; A/B start acquiring later, C/D early — their onsets 3,000–6,000 sit just
above the first eval column t=300, excluding only 96/98 pre-onset columns): A 10,478 / B 11,026 /
C 13,232 / D 13,230. Recipe pin (panel, numbers lens): the
inclusive boundary (t ≥ onset) and column-pooling (not per-seed means) are load-bearing — strict
t > onset gives p1 0.6914; per-seed-mean pooling gives 0.6996/0.5614.

**Recipe B — the recovered design-seat recipe (LATE HALF of columns, no acquisition filter):**
A 0.6924 → 0.5816; B 0.6944 → 0.5787 — reproducing the design-seat originals **0.692→0.582 /
0.694→0.579 at 3dp exactly**. Direction and magnitude agree across both recipes.

## Verification chain (all digit-exact)

1. CC artifact fact-check (2026-07-10, this session) — Recipe A + the shuffled spreads.
2. Design-seat independent recompute from committed records (2026-07-10) — recipe recovery.
3. §7.1 panel, numbers lens (`wf_7122fd66`) — both recipes + monotonicity over all six buckets +
   the spread definition (max−min is the only reading that reproduces 0.0005/0.0006; the p1−p13-48
   contrast gives C +0.0001).
4. §7.1 panel, fences lens — independent recomputation in its BD-8 analysis (including the
   "late-run ∩ post-acq" variant 0.6906/0.5832, which matches NEITHER label — the reason AMD-2b
   struck "Late-run" from the canon sentence).

## Reading (the prereg's lineage paragraph, unchanged)

The gradient is adjacency-caused: same position labels ride the permutation in the shuffled
controls (identical wave multiset — the fabric contract), and the gradient vanishes to ±0.0006
while the dwelled arms carry +0.14–0.15. Since the operator is wave-local, the within-dwell
improvement lives in the weights — online drift toward the current word during the dwell,
recency-satisfiable, cancelling across dwells. EXP16 asks which side of the wave feeds that
capture.
