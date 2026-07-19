# EXP19 W-PERM — DRAFT (no attribution; terminal read is Jason's)

**Status:** DRAFT, 2026-07-19, corridor CLOSED at `7500f73`. The seat's independent scorer-depth
verification (all six cells, pre-DRAFT, unanchored by prose) precedes this document. Panel targets ruled;
attribution, cell-mapping sentences, and §10.29 are NOT here — touch 3.

## The primary: the bracket behaved (ratified A8)
c(B), floor-audit certified counts, single instrument end to end:

| read | B=1 | B=32 | B=128 | B=512 | B=T |
|---|---|---|---|---|---|
| full | 0 | 0 | 0 | 6/8 {0,3,4,5,6,7} | 5 |
| stratified | 0 | 0 | 0 | 4/8 {4,5,6,7} | 5 |

**B\* ∈ (128, 512], BOTH reads.** Small-B zeros are instrument-certified arm-truthful (powercert PASS at
both densities, committed ≥90% bar; s6 marginal at 99.75%/97.45%). Full curves + per-B ops in the g9
artifacts; ops cut per-B on own nulls (B512: full 450 / stratified 300 — regimes differ from B=T's 300/550,
as ledger 42 anticipated), G7 curves surfaced, no integer tie.

## The decomposition the table must not blur (the seat's recompute; verified against artifacts)
The full-read 6 at the anchor is **four emphatic** (s4: 118 v 35 · s5: 65 v 15 · s6: 60 v 41 · s7: 21 v 7)
**plus two knife-edge** (s0: **7 v 5** · s3: **6 v 5** — one and two windows over their nulls). The
knife-edge pair IS the recency-carried pair: recency-free they read 7 v 15 and 5 v 14 — nowhere close.
**The recency channel is live at the anchor and the stratified instrument fired on exactly those seeds**
(§4's predicted failure surface). Strip the channel: the anchor reads 4, and the stratified curve is
monotone 0, 0, 0, 4, 5.

## Cross-arm: EMBARGO RESOLVED BY THE TAB (no unlike-bar sentence survives)
"6 > 5" was an unlike-bar artifact. The B9 matched-bar tabs (B512↔B=T, both reads, both bars each,
`exp19_g9_tab_B512_vs_BT_*.json`):
- **full @450 (B512's bar): 6 v 6** (B=T gains s1 like-for-like) — fisher 0.715, paired-exact 0.6875;
  @300: 6 v 5, fisher 0.500, paired 0.5. **No excess at any matched bar.**
- **stratified @300: 4 v 5; @550: 3 v 5** — paired 0.875 / 0.9375. On the recency-free read B=T ≥ B512 at
  every matched bar. Seed identities differ across regimes ({0,3,4,5,6,7} vs {0,1,2,4,5,6} at 450).
Any comparative sentence at terminal speaks from this tab only (ledger 17; CEILING-BORROW).

## dec_cat — descriptive line only (DECCAT-REGIME-BOUND governing; no mechanism sentence)
Stratified-certified at B=512: s4 0.727, s5 0.607, s6 0.672 — **s7 0.468** (the seat's "0.61–0.73 on the
four" corrected here: it holds on three; s7 sits at 0.47). All B=32/128 seeds: 0.19–0.39, inside the
dead-arm band (0.238 ± 0.211). Recency-carried s0/s3: 0.400/0.469.

## Standing flags into the terminal
B4 flag verbatim (s6 matched-N @550: q10 12 v floor q99 8 = 1.5×, robust false) · s25 cal null-max 127
(terminal check outstanding) · STRATUM-POWER-SHAPE (stratum non-monotone in B; sensitivity lowest at the
anchor) · LATE-RESCUE-IN-TAIL (tail-only; latest onsets at small B run late — B32 s0/s1 acq 97.5k/111.9k)
· fence event + SPLIT ruling + OOM recovery (deterministic; anchor recheck in flight) · no-prose rule held
until this DRAFT.

## Panel targets (ruled): (1) null-draw sensitivity of s0/s3's 1–2-window margins; (2) the matched-bar tab
audit before any comparative phrasing; (3) the OOM-run anchors (recheck running).
