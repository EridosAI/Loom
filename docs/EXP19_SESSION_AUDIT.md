# EXP19 SESSION AUDIT — full-conversation adversarial review

**Status:** DRAFT for Jason. Design seat, 2026-07-16. Requested audit of the entire session record:
reasoning inconsistencies, falsities, missed points, missed discovery opportunities.
**Scope:** every turn from session open through the C-vs-donor-A ruling (B8 cleared). The seat's own
rulings audited at the same depth as everyone else's. My clone is at `53374d2`; findings touching
commits after that are flagged [VERIFY-AT-HEAD].

> **[Committed 2026-07-17 on Jason's ruling, VERBATIM as delivered — this document is the record of
> what the seat claimed, wrong parts included. It is read TOGETHER with its verification:
> `EXP19_SESSION_AUDIT_VERIFICATION.md` (CC, at HEAD `1a33096`), which confirms, refutes, or narrows
> every item below. Records stand and get superseded — the pair is the honest object. Ledger rows
> 46–49 arise from this pair.]**

---

## A — INTEGRITY CORRECTIONS (ledger surgery owed)

### A1. Ledger 44 is misattributed — the seat charged CC for transcribing the seat's own ruling. **[CRITICAL]**
The seat's B7 ruling stated verbatim: *"Borrow-gate survives — it's about C_shuffle's shifted floor
referent, orthogonal to α-vs-floor-audit. It rides on the full-read floor audit unchanged."*
CC transcribed this into `exp19_cal.py:6` — faithful execution of a ratified ruling, which is correct
corridor behavior. Two turns later the seat discovered the claim was false (the borrow-gate is an
α-cut null-selection construct; nothing to operate on once the α-cut dropped) and **ledgered it
against CC.**
**Fix:** reattribute 44 to the seat. Add a new row for the misattribution itself — the seat graded
its own error onto another chair, which is a distinct failure from the error.

### A2. The seat's "both rules agree at B=T" false claim was caught by CC and never ledgered. **[HIGH]**
Separation-rule gives op 550; the 8.5-rule gave 300. B=T survived the density bug because it is
powered at any width, not because the rules coincide. CC corrected this; the seat replied "Ledger 43
is not owed." Meanwhile the seat ledgered CC for a *smaller* miss (row 28, "13 fields not 12").
Inconsistent standard. **Fix:** log it. If ledger 43 is genuinely unassigned (see A3), it fits there.

### A3. Ledger 43 may be a gap. **[VERIFY-AT-HEAD]**
Numbering went 42 → 44 in the seat's rulings. Either the parallel ISOTROPY line took 43 (it took 39
once before) or the append-only ledger has a hole — the dual of the 39/39 collision CC already fixed
once. Verify; if open, A2 fills it.

### A4. CC's decay report contradicted its own table; the seat repeated the false half. **[HIGH]**
Prose: *"end-of-run accuracy is at chance for every seed, including the converters."* Same message's
table: **s6 tail-50 = 0.616** — the highest of all eight seeds, well above chance. The seat repeated
"converters are at chance by 500k" with a disclaimer instead of reading the table against the prose.
The contradiction resurfaced one full gate later as flag 3 (s6's late plateau still rising at 500k) —
the horizon-truncation risk was visible in the data a gate earlier than it was caught.
**Fix:** one row, both chairs. Correct any doc carrying the "every seed at chance" sentence.

---

## B — CANON / INSTRUMENT RECONCILIATION DEBTS (before G8 assembly)

### B1. The committed prereg is stale against ~8 rulings — a built-in HALT. **[CRITICAL]**
The committed `EXP19_ORDERING_WINDOW_PREREG.md` (A6) still specifies: per-B **α-cut** band cuts;
**borrow-gate applies**; wp-strat as *"re-scores committed records, zero additional runs"*; α-era
detector framing in §4/§8; the pre-`dec_cat`, pre-floor-audit constants table. Superseded since by:
ledger 37 (wp-strat costs 8+5 replays — pricing false), 38 (α does not transport; floor audit is the
law), 41/42 (operating point = argmax separation on each B's own null), 44-corrected (borrow-gate
deleted, finding preserved as B9 report), plus the `dec_cat` rider and DECCAT-REGIME-BOUND.
The corridor's own rules make this urgent twice over: amending committed docs routes to ratification
(we have amended the *instrument* without the *document*), and **brief-vs-prereg divergence is a
HALT** — a G8 package assembled against the stale prereg halts by construction.
**Fix:** one reconciliation amendment — **prereg v5**, annotate-in-place, every change citing its
ledger row — ratified before G8 assembly begins. Same species as the v1.2 §5.3 lossy-compression
catch: canon drifting out from under practice.

### B2. The B* curve mixes certification instruments at its endpoints. **[CRITICAL, cheap fix]**
Endpoints "0/8" and "5/8" are α-cut-era certifications; the paid Bs will be floor-audit
certifications. One curve, two instruments — the CEILING-BORROW species in the flagship result.
**Fix, near-zero cost:** re-express both endpoints under the floor audit. B=1: stratum = 100% ⇒
stratified ≡ full read ⇒ **committed columns suffice, no replays**. B=T: G5a captures (stratified)
and B7's full-read validation (nearest run 36 vs floor 3) already exist — formalize as the endpoint
reads. State in the prereg v5 that the ladder is single-instrument end to end.

### B3. The B* estimator was never pre-registered. **[CRITICAL]**
The arm's entire output is one number and no extraction rule exists: bracket rule, logistic fit,
"smallest tested B within X of B=T's certified rate," monotone-isotonic — nothing is fixed. With 3
interior points + 2 endpoints, the choice of estimator can move B* materially.
**Fix:** pre-register the estimator (and its UNDERPOWERED/no-knee behavior) at G8, blind, with
outcome-independent grounds.

### B4. G5b's margin was never restated under the final operating rule. **[MEDIUM]**
The PASS was certified at the 27-target (3.6×), re-quoted at native density (~1.6×), and the rule
then changed to argmax-separation (B=T op 550). The binary PASS is target-invariant; the **margin at
the final rule** — the number that matters at the B=512 anchor — is unstated.
**Fix:** restate s6's margin at the argmax-separation operating point before G8 criterion 3
("wp-strat passed") is called green.

### B5. Recomputability gap: terminal verification cannot re-derive stratified numbers from git. **[HIGH]**
Per-onset captures live only on Equinox (by the seat's own ruling: captures out of git, digests in).
Digests verify integrity, not derivations. The G12 terminal verification pass — "re-derived from
pushed artifacts" — literally cannot recompute any stratified-read number. The seat's own
verification depth declined for the same reason from G5a onward: reports were read, not recomputed.
**Fix:** specify that every G8/terminal number must be recomputable from committed artifacts; commit
the minimal derived series (per-window stratified accuracy per seed, per B) that the census and floor
numbers depend on. Small files; restores both the terminal pass and the seat's power.

### B6. Committed content digests for the five certified arms — proposed, never confirmed landed. **[MEDIUM, VERIFY-AT-HEAD]**
Proposed when the generator was provably pristine ("the last moment it's free"). If dropped: still
worth doing — G0b v2's inertness proof chains digest-of-edited ≡ digest-of-original, so digests
computed now still anchor the original content, one link weaker.

---

## C — DESIGN GAPS TO CLOSE BEFORE OR AT G8

### C1. `dec_cat` endpoint holes are unpriced. **[HIGH]**
Committed endpoint runs predate `dec_cat`; the G5a captures hold per-onset `exam_acc`, not the
16-probe content tensor. So the dec_cat-by-B curve currently arrives blind at **both anchors**:
B=T needs ~8 re-replays with dec_cat capture; B=1 (A_dwell) needs ~8 fresh replays. ~30-min-wall
class each, but it is compute and it is unpriced — §12.1's own rule. Importing the ISOTROPY line's
dwelled-arm dec_cat is forbidden until shown same-instrument (nothing transports).
**Fix:** price the ~16 replays now; decide whether the endpoints ride in G8 or the curve ships
interior-only with the holes stated.

### C2. The §5.3 rider's letter blocks U-BUF at tier 2. **[HIGH, pre-flag]**
Rider: replay *"does not enter the default learner while any regime arm remains unrun."* U-BUF —
tier 2, the realizability arm — **is** a buffer in the learner, and L3 remains banked-not-dead. Read
literally, the rider blocks the very arm the three-tier structure requires next. The rider's C3
*purpose* (fabric-vs-gating attribution must stay decidable) is satisfied by U-BUF holding the fabric.
**Fix:** rule it at U-BUF's prereg, not during — either declare the regime map closed-enough, or
refine the rider to its C3 purpose. Pre-flag now so it doesn't ambush that prereg.

### C3. Stratified-read power is non-monotone in B; pre-name the wrong-reason. **[MEDIUM]**
Stratum fraction: 22.7% (B=32) → 17.7% (B=512) → 30.75% (B=T). Sensitivity is therefore lowest at
the anchor and higher at both ends. A stratified-read non-monotone could be stratum-power shape, not
mechanism — a *different* confound with the same signature as RECENCY-AT-EXAM's interior peak.
**Fix:** pre-name **STRATUM-POWER-SHAPE** in the taxonomy; the per-B floor audit covers certification
but not graded sensitivity, so the cell routes a stratified non-monotone through the per-B power
numbers before any mechanism read.

### C4. EXP16 gradient Δ referent binning mismatch. **[MINOR]**
The +0.1416 referent was measured at width-300 α-era windows; W-PERM reports Δ at per-B
argmax-separation widths. REPORTED-not-gated, but cross-width comparison is loose.
**Fix:** report Δ at matched binning alongside, or annotate the width difference wherever quoted.

### C5. Flag 3 (horizon truncation) still lacks a concrete cell. **[MEDIUM]**
If interleaving slows onset (plausible: weaker per-dwell massing), converters shift right; the latest
committed onset is already 427.5k of a 500k read. The §3 descriptive tail (4 blind seeds to 1M)
exists but is barred from cross-arm comparison.
**Fix:** pre-name a descriptive **LATE-RESCUE-IN-TAIL** cell for this arm — tail-only, never in the
B* estimator, but named before data so a late rescue is reportable rather than invisible.

---

## D — MISSED DISCOVERY OPPORTUNITIES

### D1. The decay-mechanism micro-arm — nearly free, mechanistically the biggest open question. **[PROPOSE]**
The G5a replays revealed conversion is **transient**: converters un-convert under continued shuffled
training. Nobody asked why. Three candidate mechanisms with different implications:
(i) representational interference — later waves overwrite the category axis (bears directly on CWP
and replay design); (ii) axis rotation — the ISOTROPY line's axis-selection view, dynamically
unstable at these constants; (iii) readout drift — the representation persists, the detector's
operating point moves.
**`dec_cat` through the decay discriminates them:** dec_cat persisting while exam_acc decays ⇒ (iii);
falling in lockstep ⇒ (i)/(ii). Cost: 8 C_shuffle replays with dec_cat capture (~30 min wall) —
the same replays C1 needs for the B=T endpoint, so the two share compute.
**Propose as a banked micro-arm, priced-at-open, behind nothing** — it trains nothing and touches no
gate. Possibly the most informative cheap measurement available to the campaign right now.

### D2. A canon sentence nobody wrote: recency is neither necessary nor sufficient. **[PROPOSE]**
G5a: conversion survives on the zero-preceding stratum (recency **not necessary**). EXP16: removing
the recency shortcut does not free content learning (recency **not sufficient**). Two certified
results, one two-sided closure of the recency channel in the shuffled regime — currently living in
two documents that don't cite each other. One FRONTIER sentence, citable, when EXP19 closes.

### D3. The titration's post-W-PERM role. **[NOTE]**
Re-priced, it is no longer a dead branch: if W-PERM establishes the ordering effect at fixed exam
density, the titration becomes a **fabric-side confirmatory dose-response** — its exam-density
confound gets a free control from W-PERM's result. Note in the bank; changes its trigger framing.

### D4. Phantom-floor scaling law. **[NICE-TO-HAVE]**
Floor-vs-N (G5b) and floor-vs-width (B7) are two slices of one null process. A small analytic model
(longest exceedance run under autocorrelation) would predict floors instead of simulating per B, and
deviations would flag detector pathologies. Not load-bearing; one paragraph if anyone is idle.

---

## E — FALSITY CHECK ON STANDING NUMBERS (re-verified this session)

Re-derived and confirmed: E[k]=10.9293, E[k²]=202.87, length-biased mean 18.56, ρ(B)≈17.56/B
(straddle pushes measured ρ slightly below at small B — inside the 2× envelope), recency
P(immediate)=(E[k]−1)/(B−1) → 0.320 at B=32, stratum arithmetic (30.75%×~45,750 ≈ 14,156;
17.7% ≈ 8,097 ✓), Poisson never-updated e⁻¹=36.8%, exam-density ratio 5.5×, cost 39 = 3×(5+8) =
24 verdict + 15 cal. All reproduce.
Two loose ends: G5a's p-value is quoted as p<1/2000 in one report and p<1/5000 in the next
(K presumably grew between runs — pin one K in the doc) [VERIFY-AT-HEAD]; and the borrow-gate
deletion + ledger-45 instructions were "not committed" at last report — confirm landed.

---

## F — STRUCTURAL OBSERVATIONS

**F1. The seat's verification depth declined after G5a** — structurally (captures off-git make
recomputation impossible from the clone: fix B5) and behaviorally (reports were read, not recomputed).
The early-session pattern — every number re-derived from artifacts — is the seat's entire power and
it eroded exactly when the numbers got most consequential.

**F2. The dominant error species, all chairs, unchanged all session:** convenient claims about
comfortable cases. "Both rules agree at B=T" (seat), "all seeds at chance" (CC), "elevated vs A/B/D"
(seat), "universal 8.5" (CC), "zero additional runs" (seat). B=T and favorable framings are where
scrutiny relaxes — the largest stratum is the *worst* validator precisely because it is forgiving.
The machinery caught every instance; none self-caught. That is the design working, and also the
measure of how much any chair should be trusted unverified.

**F3. Housekeeping:** PAT rotation at session close, as agreed — handoff carries it as move zero.
This audit should be committed (docs/) once Jason rules on the ledger surgery in §A, so the
corrections and the pre-G8 debts survive the session boundary.

---

## PRIORITIZED ACTION LIST

1. **Ledger surgery** (A1 reattribute 44 + misattribution row; A2/A3 fill 43; A4 both-chairs row).
2. **Prereg v5 reconciliation** (B1) — before any G8 assembly.
3. **Single-instrument endpoints** (B2) — with v5.
4. **Pre-register the B* estimator** (B3) + **STRATUM-POWER-SHAPE** and **LATE-RESCUE-IN-TAIL**
   cells (C3, C5) — at G8, blind.
5. **Commit derived series for recomputability** (B5).
6. **Price the dec_cat endpoint replays** (C1) and **rule the decay micro-arm** (D1) — shared compute.
7. **Restate G5b margin at the final rule** (B4).
8. **Pre-flag the U-BUF rider ruling** (C2); write the D2 canon sentence when EXP19 closes;
   verify B6/E loose ends at HEAD.
