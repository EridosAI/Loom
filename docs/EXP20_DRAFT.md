# EXP20 U-BUF — DRAFT RESULT v2 (G6; no attribution; the corrected 1M-law read)

**v1 → v2:** DRAFT v1 (uncommitted; superseded in place — its refuted claims are QUOTED inside
the panel record's findings, not preserved verbatim; panel-v2 FLAG folded) reported the
500k-truncated read and was REFUTED in full by the G6 panel — ledger row 56, fix `e4d1007`,
corrected G3/G5 recomputed at the ratified 1M grid. Panel record: `exp08/exp20_panel_v1.json`.
This v2 is the ratified-law result and faces its own verification pass before terminal.

**Corridor state:** G0–G5 closed (all reds observed first); touch-2 `0ff5fbe`; verdict runs
`92e7d44`; row-56 fix `e4d1007`. Law: width 300 (Q2), per-K in-regime bands (0.6154/0.6190/0.6333
— band values unchanged by row 56; they were cut on true-1M windows), floor-audit certification at
the ratified read_at = 1,000,000, stream-marginal per ledger 52, cutter W=K (Q1), K512 stratified
UNDECIDABLE-IN-ARM (AMD-1). Corrected G3 detail: at the 1M grid K128 gains an in-arm cal converter
(s24) — its ops cut to full 300 / stratified 300, coinciding with the ruled verdict width.

## The result (per-seed, the committed law, no pooling beyond it)

| K | full read | delivered-stratum read |
|---|---|---|
| 32 | **0/8** (runs 2–3 vs null max 6–8) | **0/8** |
| 128 | **1/8 — s2: 39 > 7** (others 2–4 vs 7–8) | **1/8 — s2: 13 > 10** (others 3–4 vs 8–9) |
| 512 | **7/8** — s0 40>9 · s1 36>7 · s2 45>7 · **s3 140>45** · s4 49>8 · s5 71>7 · s6 58>9; s7 3<8 | UNDECIDABLE-IN-ARM (AMD-1; support ≈ 470–530/seed recorded) |

**Every certification is stream-emphatic: 200/200 independent simulator families, marginal tail
0.0 — none rides QUALIFIED.** That includes the two decisive cells: K128 s2's stratified 13 > 10
and K512 s3's 140 > 45.

## Cells (mechanical, §5 + AMD-1)

- **RESCUE-MONOTONE (powered strata): SATISFIED.** Stratified-surviving counts K32 → K128 =
  0 → 1, non-decreasing with a strict rise; s2's certification survives the delivered-stratum read
  and the stream-marginal amendment unqualified. Per the pre-registered route: **realizability
  ESTABLISHED at the smallest certifying K = 128**, and §1's rescue sentence is licensed with
  K = 128: *"a causal uniform replay buffer of capacity K = 128 rescues certified conversion in
  the certified-dead dwelled regime — ordering-in-updates is realizably sufficient."* The
  mechanism WHY stays [PROPOSED]; no K↔B equivalence claim is licensed (BAR-1). Presented
  plainly: the powered-stratum certification is **one seed of eight** (s2); the law's cell is an
  existence bar and the count is stated wherever the cell is.
- **RESCUE-FULL-ONLY-K512 = {0,1,2,3,4,5,6} (7/8)**, licensed sentence verbatim and entire:
  *"certified on the full read at K512; the recency-free confirmation is structurally unpowered at
  this K — RECENCY-CARRIED cannot be excluded in-arm."* dec_cat rides as the companion-grade
  discriminator (below).
- RECENCY-CARRIED at powered K: **empty** (s2 certifies both reads). STRATIFIED-ONLY: none.
  ALL-PAID-DEAD: no — **K=2048 stays dormant.** WARMUP-CARRIED: none (earliest episode start
  58.5k ≫ K). MULTIPLICITY-CARRIED: not fired (certified-vs-noncert p_never gap inside the
  spread). No unrouted outcome; no halts; no flags.

## Companions (descriptive; no cell, no gate)

- **Episode geometry (corrected):** K512 spans s0 271.5–283.5k · s1 418.5–429.3k · s2
  152.7–166.2k · **s3 498.6–540.6k (the episode the truncated grid chopped at its 4th window)** ·
  s4 58.5–73.2k · s5 112.8–134.1k · s6 169.8–187.2k; K128 s2 905.4–917.1k. The v1 claim "all
  episodes end by 429k — sustained, then gone" is RETRACTED (row 56): s3's episode straddles 500k
  and s2-K128's sits at 905–917k. Episodes remain bounded (10.8k–42k waves) within the 1M read;
  onset-to-episode distances vary seed-to-seed.
- **dec_cat** (companion-grade): certified K512 seeds' post-acq means 0.493–0.633; late-minus-
  early: s3 +0.508 (the late certifier), s1/s2 ≈ +0.005/+0.007, s0/s4/s5/s6 −0.023…−0.175.
  K128 s2: mean 0.396, dLE −0.001. Reported as computed by the committed companion form; the
  panel's v1 finding that the "mid-run straddle" caveat was itself wrong is folded — no caveat
  is asserted here beyond the numbers.
- **K↔B correspondence** (no equivalence claim licensed): adjacency 0.451/0.183/0.099; mean
  displacement 15.4/63.1/251.4 (≈ K/2).
- **Powercert context for the K32 zeros:** cal powercert passed (1.00/1.00 at K32's densities);
  the K32 zeros are arm-truthful under the corrected grid (panel-verified at 1M).
- **E-A continuity:** in the committed records, untouched.
