# EXP19 SESSION AUDIT — CC verification at HEAD `1a33096` (2026-07-17)

**Status:** COMMITTED with its input on Jason's ruling (2026-07-17) — read as a PAIR with
`EXP19_SESSION_AUDIT.md` (the seat's audit, verbatim as delivered, wrong parts included: records stand and
get superseded; the pair is the honest object). Ledger rows 46–49 arise from this pair.
**Input:** `docs/EXP19_SESSION_AUDIT.md` (the seat's full-session adversarial audit, clone at `53374d2`).
Three commits landed after that clone — `bd92d8b` (borrow-gate deletion, ledger 43), `1a33096` (B8 + ledger
44) — so every finding was re-verified against the committed record at HEAD, not the audit's snapshot.
Verdicts below; every claim carries its evidence. One NEW defect surfaced during this verification (N1),
CC's own, disclosed at the end.

**Ledger-numbering map (needed to read §A):** the seat's spoken numbering ran +2 ahead of the committed log
(his "45" → committed **43**; the log's next rows landed as **43** borrow-scope and **44** band-mismatch).
The audit's "ledger 44" (its A1) refers to the borrow-gate event = committed **row 43**.

---

## A — Ledger surgery items

**A1 (misattribution) — REFUTED against the committed log; a smaller kernel survives.**
Committed row 43 headline: "**Seat** — the borrow-gate-deletion ruling over-generalized…", attribution
column "**CC → Jason**" (caught by CC, ruled by Jason). Row 44: "**CC** — …", "CC's review → CC". **No
committed row charges CC for the borrow-gate transcription** — the audit's premise describes the seat's
spoken numbering, not the log. *Surviving kernel:* row 43 does not explicitly state the ORIGIN of the
"borrow-gate survives" claim (the seat's ratified B7 re-spec ruling, which CC transcribed faithfully into
`exp19_cal.py:6`). If the seat wants the origin on the record, that is a one-sentence annotation to row 43 —
his ruling.

**A2 ("both rules agree at B=T" never ledgered) — PARTIALLY CONFIRMED.**
The catch IS committed, but folded into row 42's tail ("…NOT because the rules agree (separation gives 550
there, not the 8.5-rule's 300)"), inside a row charged "Jason, correcting CC". No seat-charged row exists
for the false premise itself. Whether it warrants its own row (it can no longer "fill 43" — see A3) is the
seat's ruling; next free number is **46**.

**A3 (gap at 43) — RESOLVED, no gap.** 43 = borrow-scope catch (`bd92d8b`); 44 = band mismatch
(`1a33096`). Row 43 carries the +2-offset provenance note ("numbered 43, not the ruled '45'").

**A4 (decay contradiction) — CONFIRMED chat-side only; committed doc is CORRECT.**
`EXP19_G5A_DECAY_COMPANION.md` explicitly distinguishes s6 ("least decayed — episode most recent, tail
0.616; the other 4 at ~0.48–0.52 = chance"), and its "~chance for all seeds" sentence describes the FROZEN
500k CHECKPOINT eval — which was genuinely at chance for all seeds (the reverted model; the very HALT that
forced the replay). **No committed doc carries the false universal**; it lived in chat prose (CC's report
sentence and the seat's echo). No doc correction owed. A both-chairs ledger row for the chat-side error and
the one-gate-late catch of flag 3 = the seat's ruling.

---

## B — Canon / instrument reconciliation

**B1 (stale prereg) — CONFIRMED, narrowed to four spots.** The prereg self-annotates in place through
ledger 38 (§4.3 amendment blocks; wp-strat G5a/G5b rows amended; §10 has DECCAT-REGIME-BOUND). Genuinely
stale at HEAD:
  1. §8:350 — "stratified read and wp-strat cost **zero additional runs** — re-score committed records":
     falsified by ledger 37 (13 deterministic replays: 8 verdict + 5 cal).
  2. §8:360 — "per-B band, full read | calibrate-in-regime; **borrow-gate applies** (C's floor was
     SHIFTED)": falsified by ledger 43 (gate deleted; floor audit subsumes; finding scoped C-vs-donor-A,
     preserved as B9's floor columns).
  3. §8:360–361 — the per-B **band**-cut framing generally: the per-B constant is now the WIDTH (argmax
     separation on each B's own null) at the family band 0.64 (ledgers 38/41/42/44).
  4. §7:317 — G5b row still states the ledger-41 rule ("native ~8.5/win, width 550") without the ledger-42
     correction (argmax separation, NO density target; op at B=T still 550 — the rule changed, not the
     number).
Plus the two additive v5 items: the single-instrument-ladder statement (B2) and the B* estimator (B3).
**Prereg v5 = a ratification act — the seat's.** Concur with the audit: before any G8 assembly.

**B2 (mixed-instrument endpoints) — CONFIRMED; feasibility verified, cheaper than priced.**
B=T is already re-expressed under the floor audit: B8's committed validation (full 5/8 @op300, stratified
5/8 @op550, both = the committed set {0,2,4,5,6}) — formalize as the endpoint read. B=1: the committed
A_dwell verdict records (8 seeds) carry `exam_acc` **and `exam_n`** per column to 499,800 — everything the
sim floor needs — so the B=1 floor-audit endpoint is computable from committed columns at widths that are
multiples of EVAL=300. **Zero replays either end.**

**B3 (B* estimator unregistered) — CONFIRMED.** No extraction rule (bracket/logistic/isotonic/threshold)
anywhere in the prereg. Pre-register at G8, blind — the seat's.

**B4 (G5b margin at the final rule) — CONFIRMED; the number now computed, with a flag the restatement
must carry.** From the committed `exp19_g5b_rebin_sweep.json`, width 550 (the argmax-separation op at B=T):
matched-N (7,915) s6 margin = **q10 12 vs floor q99 8 = 1.5×** (`sep_ratio` 1.5; 5/5 converters clear) —
**and `s6_clears_robust: false`** (s6 run min 6 < floor q99 8 in the subsample-draw tail). The full-N B8
frame at 550: s6 obs 32 vs own sim null max 16 (2.0×, p<1/5000). Whether criterion 3 stays green wearing
the non-robust flag at the anchor's matched N is the seat's G8 read; the number is no longer unstated.

**B5 (recomputability) — CONFIRMED structurally; priced.** Per-onset captures + wave caches are gitignored
(`git check-ignore` confirms). Committing the two B=T caches (`exp19_g5a_strat_cache.json` 2.4 MB +
`_wave.json` 1.6 MB) restores stratified recomputability from a clone; all 13 per-onset files ≈ 26 MB
restores the full-read derivations too. Commit = the seat's word.

**B6 (content digests) — PARTIALLY LANDED.** `exp19_g0b_genregress_{baseline,edited}.json` + the 13-capture
`exp19_g5a_capture_digests.json` are committed. Whether the g0b digests enumerate all five certified arms'
fabric content is confirmed at pre-flight G0b (which re-runs regardless).

---

## C — Design gaps

**C1 (dec_cat endpoint holes) — CONFIRMED, and STRONGER than written.** Verified per seed: **only s0's
replay record carries dec_cat** (1666/1666 columns — it was the dec_cat anchor-verification re-replay,
`9f5aa7c`); **s1–s7 have zero dec_cat columns**; all A_dwell committed records lack the field. So B=T
coverage is 1/8, B=1 is 0/8. Price: 7 C_shuffle re-replays + 8 A_dwell replays (~500k-horizon runs each).
The B=T seven are **the same replays D1 needs** — shared compute, as the audit says. See also N1 below.

**C2 (U-BUF rider) — noted as a pre-flag** for the U-BUF prereg; no HEAD action.

**C3 (STRATUM-POWER-SHAPE) — CONFIRMED gap;** taxonomy addition → prereg v5, blind, the seat's.

**C4 (gradient Δ binning mismatch) — REFUTED at HEAD.** B8's `_companions` computes Δ via
`X16._recency_gradient` over the record's EVAL-300 columns — the SAME binning as the +0.1416 referent. The
per-B argmax width never enters the gradient path (it exists only in the certification detector).

**C5 (LATE-RESCUE-IN-TAIL) — CONFIRMED gap** → v5, blind, the seat's. Note: the g5a replay records stop at
t=499,800 (no 1M columns) — the descriptive tail remains unrun, so the cell costs the §3 tail seeds when
fired.

---

## D — Discovery

**D1 (decay micro-arm) — CONFIRMED sound; repriced.** Not free-from-disk: only s0 carries dec_cat (C1),
so the discriminator costs the same 7 B=T re-replays as C1's endpoint. Columns to 500k suffice (latest
episode ends 456,300). Design as stated: dec_cat persisting through exam_acc decay ⇒ readout drift;
lockstep fall ⇒ interference/rotation. Banked micro-arm, priced-at-open — the seat's call.

**D2 (necessary-nor-sufficient canon sentence)** — drafts at EXP19 close. **D3/D4** — noted to the bank.

---

## E — Standing numbers

All audit re-derivations concur. The p-value discrepancy: **committed docs are uniform at p<1/5000**
(N_SIMS=5000; G5A_RESULT table + ledger 38/44). "p<1/2000" appeared chat-side only; 2000 = `K_DRAWS`, the
G5b subsample-draw constant — a different instrument's constant, not a drift. One clarifying sentence in v5
if desired. "Borrow-gate deletion + ledger landed?" — **yes**: `bd92d8b` + `1a33096`, as rows 43/44.

---

## N — NEW defect surfaced by this verification (CC's own, disclosed)

**N1. B8's companions summary mislabels 1-seed dec_cat coverage as a cross-seed median.** `_companions`
medians over non-None per-seed values; with s1–s7 lacking dec_cat, the committed B8 validation line
"dec_cat median=0.6637" is **s0's single value wearing the label "median"**, and the validate tripwire
`|median − 0.662| < 0.02` guards one seed. The per-seed truth is present (`dec_cat_n: 0` for s1–7) but the
summary hides the coverage hole — the same convenient-summary species as F2. **Proposed fix (B8 is
committed — report-don't-patch, so disclosed here first):** `_companions` gains
`dec_cat_seeds_covered/total`; the median reports alongside coverage and the validate print states "s0
only" until C1's replays land. Rides whichever commit the seat assigns (B9's or its own).

---

## Action state after verification

| # | item | state |
|---|---|---|
| 1 | Ledger surgery (A1 kernel, A2 row, A4 row) | **the seat's ruling** — next free row 46 |
| 2 | Prereg v5 (B1's four spots + B2 statement + B3 estimator + C3/C5 cells + E note) | **the seat's ratification**, before G8 assembly |
| 3 | B2 endpoint re-expression | verified feasible, zero replays; build on word |
| 4 | B4 margin restatement | **computed** (1.5× q10, robust-flag false at matched N) — for the seat's G8 read |
| 5 | B5 recomputability commit | priced (4 MB caches / 26 MB full) — the seat's word |
| 6 | C1+D1 shared replays | priced: 7 × C_shuffle + 8 × A_dwell (~500k runs) — the seat's call |
| 7 | N1 fix | proposed, one small edit — assign to a commit |
| 8 | This audit + verification → docs/ commit | on the seat's ruling (F3) |
