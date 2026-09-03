# EXP19 PREREG v5 — reconciliation amendments (RATIFIED, Jason 2026-07-17)

**Status:** RATIFIED (Jason 2026-07-17, conditional folds A8–A10 included; applied to the prereg proper same commit). Formerly: DRAFT / PENDING RATIFICATION — committed to the record on the seat's instruction (2026-07-17:
"untracked-on-Equinox means the seat cannot clone-verify; after audit row 46 nothing goes to Jason on my
read of a report"). The seat verifies from the push; Jason ratifies; only then are the amendments applied to
`EXP19_ORDERING_WINDOW_PREREG.md` proper. Scope per Jason's 2026-07-17 ruling: the four narrowed stale spots
+ B2 single-instrument endpoints + the B5 recomputability spec + the B4 flag + the G7 separation-curve
reporting pre-flag (canonical text received 2026-07-17, Amendment 7).
**Method:** annotate-in-place in `EXP19_ORDERING_WINDOW_PREREG.md`, every change citing its ledger row —
the prereg's existing amendment-block style (ledgers 33/34/35/37–38 are already in-place). Nothing below
changes an instrument; every instrument change already happened under a ratified ruling — this closes the
document over the practice (the audit's "canon drifting out from under practice").

---

## Amendment 1 — §8:350 (wp-strat pricing). Cites ledger 37.
STALE: "The stratified read and `wp-strat` cost **zero additional runs** — they re-score committed records…"
AMEND (append block): *[v5, ledger 37 — the committed record's per-window means could not answer the
stratified question (the 500k read-checkpoint is a REVERTED model); wp-strat cost **13 deterministic
replays** (8 verdict + 5 cal, ~500k horizon each, all 13 anchors bit-exact incl. cross-commit). "Zero
additional runs" was false as pricing; the replays train nothing (replay-of-committed-trajectory, not new
arms). Scorer code + stratified cut remain the only NEW instruments.]*

## Amendment 2 — §8:360 (borrow-gate row). Cites ledgers 38, 43.
STALE: "per-B band, full read | calibrate-in-regime; **borrow-gate applies** (C's floor was SHIFTED)"
AMEND (append block): *[v5, ledgers 38+43 — the α-cut is retired (38): certification everywhere is the
FLOOR AUDIT. The borrow-gate was an α-cut null-selection rule; with no α-cut there is nothing for it to
operate on, and the floor audit SUBSUMES it (every arm judged on its OWN measured phantom null; the
committed `borrow_gate.borrow_ok:false` pre-recorded exactly that behaviour). DELETED (43). The finding it
carried is preserved as a MEASURED quantity scoped **C-vs-donor-A only** (+0.0203; B and D sit ABOVE C —
never in the borrow) and surfaces in B9's matched-bar floor columns. CEILING-BORROW in §10 stands as the
wrong-reason it always named — the shifted-floor RISK, now guarded by the tab, not by a gate.]*

## Amendment 3 — §8:360–361 (per-B constant framing). Cites ledgers 38, 41, 42, 44.
STALE: both rows frame the per-B constant as a per-B **band** cut ("its own cut", α-era).
AMEND (append block): *[v5, ledgers 38/41/42/44 — ONE detector family arm-wide: band fixed at 0.64 (the
committed X15_REPRO C_shuffle detector band; 44 fenced it into the deployed scorer with a module-load
assert). The per-B constant is the **WIDTH**: each B's operating width is cut on that B's OWN phantom null
by argmax converter/floor SEPARATION across the swept widths (42 — no density target), in the stratum's own
regime (41), outcome-blind; the per-B **≥ width floor** is the computed pre-flight constant beside ρ(B).
The per-B UNDERPOWER GATE (STRATUM-UNDERPOWER, per-B) is the generalized wp-strat; it emits the robustness
field (see Amendment 4). Executors: `exp19_cal.py` (cut) → `exp19_scorer.py` (certify at the inherited
width) → `exp19_tabs.py` (cross-B, matched bars only).]*

## Amendment 4 — §7:317 (G5b row: the ledger-42 correction + the B4 flag). Cites ledgers 42, 44 + B4 ruling.
STALE: the row's rule-statement stops at ledger 41 ("operating point cut in the STRATUM regime (native
~8.5/win, width 550)").
AMEND (append block): *[v5, ledger 42 — the "native density" rule was itself the FOURTH un-transported
constant; the final rule is **argmax separation on each B's own null, no density target** (op at B=T is
unchanged at 550 — the rule changed, not the number). **B4 flag, rides verbatim into the G8 package and any
criterion-3 statement (Jason 2026-07-17, never summarized away): s6 matched-N at the final op 550: q10 12
vs floor q99 8 (1.5×), `s6_clears_robust: false` (min 6 dips under the floor q99 in the subsample-draw
tail).** Not a HALT (the primary clears at 1.5×; the dip is draw-tail behaviour) — but every criterion-3
statement carries it. The corridor's per-B gate emits the same field (`all_clear_robust` /
`separation_vs_floor_max`, committed `da7bbb6`).]*

## Amendment 5 — NEW §8 subsection: single-instrument ladder (audit B2). Cites ledgers 38/44 + B2 ruling.
ADD: *[v5 — **the B\* ladder is single-instrument end to end**: every point on the curve, endpoints
included, is a floor-audit certification at band 0.64. The α-cut-era endpoint labels ("0/8", "5/8") are
context-only. Endpoint reads, zero replays: **B=T** = B8's committed validation (full 5/8 @op300,
stratified 5/8 @op550, both = the committed converter set {0,2,4,5,6}; `exp19_scorer.py --validate`).
**B=1** (A_dwell; stratum structurally 100% ⇒ stratified ≡ full read) = a column-based floor audit from the
committed A_dwell verdict records — `exam_acc` (per-window means) + `exam_n` (per-window onset counts) are
committed for all 8 seeds, which is everything `_sim_null_runs` consumes; widths restricted to multiples of
EVAL=300. The B=1 read is a small pre-flight build (pre-registered here, blind — expected 0/8 under the
committed record, but the read is run, not assumed).]*

## Amendment 6 — NEW §12 item (e): recomputability standard (audit B5). Cites the B5 ruling.
ADD: *[v5 — **every G8/terminal number must be recomputable from committed artifacts.** Standard output per
arm: the derived per-window stratified series per seed (the B=T pair `exp19_g5a_strat_cache{,_wave}.json`
is committed at `a72ea3c` as the pattern). Raw per-onset captures stay off-git with committed digests; the
full raw set is not taken by default — revisit at G8 if the derived series proves insufficient for terminal
recomputation.]*

## Amendment 7 — NEW §7 pre-flight surface: the G7 separation-curve reporting pre-flag (canonical text,
## the seat 2026-07-17). Cites ledger 45 (B9 catch #2's corrected provenance).
ADD: *[v5 — **Motivation:** the argmax-separation operating point showed real draw-variance on the thinned
proxy — op 600 on the committed draw vs 900 on the range(8) draw (B9 catch #2's corrected provenance). A
selection rule with that sensitivity must expose its landscape before it gates anything. **Rule:** G7's cal
output reports, per B and per read (full + stratified), the **full separation-vs-width curve** —
nearest-converter-run − floor-q99 at every swept width — not only the argmax. (The committed sweep output
already carries this; the rule makes it a required pre-flight surface.) REPORTED, never gating.
**Tie-break, pre-registered blind:** separation is an integer (run − q99), so a flat-top is an exact integer
tie at the max — no ε constant needed. If any B's curve has a **non-unique argmax**, that is a **HALT →
Jason rules the tie-break before the corridor proceeds.** Pre-named condition, judgment routes to the human,
no constant invented.]*

## Amendment 8 — the B* estimator (audit B3; Jason's ratification fold, text supplied). BRACKET RULE, primary:
c(B) = certified count at B under the floor audit. B*_lo = largest tested B with c = 0; B*_hi = smallest with
c ≥ 1; report B* ∈ (B*_lo, B*_hi] with the full c(B) curve always. No point estimate; a descriptive
isotonic/logistic fit may be REPORTED, never gates. Degenerate routes: all paid B ≥ 1 → "B* ≤ 32, below
ladder floor"; all paid B = 0 → NO-KNEE-IN-LADDER as pre-named; non-monotone → existing NON-MONOTONE routing.
Grounds: certified counts only (L18); a bracket refuses false precision from 3 interior points; endpoints pin
the extremes; committed before any G9 data exists.

## Amendment 9 — STRATUM-POWER-SHAPE (audit C3), wrong-reason cell (§10): the stratum fraction is
non-monotone in B (22.7% → 17.7% → 30.75%), so stratified sensitivity is lowest at the anchor and higher at
both ends; any stratified-read non-monotone routes through the per-B power numbers before any mechanism read.

## Amendment 10 — LATE-RESCUE-IN-TAIL (audit C5), descriptive cell (§7): the latest committed onset is 427.5k
of a 500k read; if interleaving slows onset, converters shift right. Tail-only (§3's 4 blind seeds), never
enters the B* estimator, named before data so a late rescue is reportable rather than invisible.

*(A8–A10 fold note, Jason: the earlier deferral followed the audit's action list — the conflict between the
two documents was the seat's; v5-now governs because chat-side content has been this session's loss surface.)*

---

**Superseded by A8–A10 above (v5-now governs):** the B\* estimator and C3/C5 cells are no longer deferred. Still at close: (blind, per the audit action list — NOT in this draft):** the B\* estimator (B3);
STRATUM-POWER-SHAPE and LATE-RESCUE-IN-TAIL taxonomy cells (C3, C5); the D2 canon sentence at close.
