# BANKED-SHELF STEP-0 FACT-CHECK — CONSOLIDATED FINDINGS + RESOLUTION (audit trail)

**Status: OPS/AUDIT record (CC seat, 2026-07-12 · brief v2 §5). Rides WITH the shelf it audits. Two LLM faithfulness passes (all 9 shelf docs, ~148 claims re-derived vs committed canon) + the independent `verify_toolkit.py` gate (self-test + 3 live record-anchors, all green) + manual checks. Every item was FLAGGED first (report-don't-patch); Jason then ruled; the load-bearing items were applied as MARKED amendments in the shelf commit this record rides in.**

## RESOLUTION (Jason ruled 2026-07-12; applied as marked amendments)
- **A1** (the session's most important catch — founding bet tagged Established/[MEASURED]): down-tagged; completer-level engagement stays [MEASURED], encoder-teaching stays [PROPOSED, untested], bootstrap-as-control named. **Applied** (conversion_gating §6).
- **A2 / B2** reworded to fabric-axis form with recipe named (word-visible A0.454=C0.454, B0.500=D0.500; exam-density means A27.48/C27.44, B13.72/D13.68). **Applied** (conversion_gating coord 2).
- **B1** HANDOFF traverse: "-measured" removed, reframed to tremble-baseline contrast (sim ≈0.090; measured at freeze). **Applied.**
- **B3** +0.012 dropped; +0.0203 point estimate stands. **Applied.** · **B4** depth 0.88–0.92. **Applied.** · **B5** universal narrowed to "EXP14–17 fabric family" with exceptions cited. **Applied** (v1.2 §5.4).
- **C** count: F4/F7 declared folds-not-catches; red-team catches renumber 10–14; HANDOFF tally keeps "five" + gains a pointer to this file. **Applied** (RED_TEAM header, HANDOFF).
- **Six ruled folds** F3, F4, F7 (extended scope; "confirms not supersedes"), CWP-family, Replay-cross-ref (→ ops §3), HANDOFF-tally — **all applied.** F2-pending one-liners added at EXP_L2:20 and v1.2 §3. Both v1.1 forks' status lines gained superseded-by-v1.2/retained-as-provenance markers.
- **Toolkit gate GREEN** post-edit: self-test PASS; A Δ`pos_gradient` 0.1416, `exam_density` 27.4756, EXP16 X s6/s7 converted/[4]/[4].
- **Not folded (low; Jason not asked to rule; documented here, ride as-flagged):** coord-8 "6–10×" multiplier & the report-don't-attribute hedge; "~5–6 vision losses"; EXP_L2:30 "L1-orbit committed" tag; FUTURES "ten restarts"; EXP18 "~60 runs"/"acquisition degrades" tag; v1.1 "background pinned" framing; HANDOFF "THIN"/stale-HEAD (self-disclosed); ops tag-name example. See §E/§F below.

---
## (Original flagged findings — preserved as the pre-ruling record)

**Nothing was edited before Jason ruled; every item below was FLAGGED. The shelf did NOT read clean as-is.**

## Toolkit gate (brief §2) — GREEN ✓
- `python3 tools/verify_toolkit.py` self-test: **PASS** (4 analytic anchors).
- No forbidden imports (pin a): the only `exp14_arms/exp17_score` string is the docstring describing the pin. ✓
- 3 live anchors vs committed records: A-arm `pos_gradient` Δ=**0.1416** ✓ (`exp14_exp12_dwell_s0-7_verdict`); A-arm `exam_density`=**27.4756**≈27.48 ✓; EXP16 X (`exp12_dwell_expomid`) s6/s7 = **converted, lengths [4]/[4]** ✓.
- Independently corroborates +0.1416 and 27.48 from raw records. (Relocated docs/→tools/.)

---
## A — BLOCKERS (flagship v1.0 `MECHANISM_MAP_conversion_gating.md`; cannot ride under [MEASURED])

**A1. §6 "evocation teaches where experience stops being locally satisfiable" — Established/[MEASURED].** Canon: FRONTIER §10.10 "channel carries information; has NOT been shown to teach"; "[PROPOSED] and untested"; PROJECT_STATE "evocation-as-teacher wholly untested." The verb *teaches* is the exact untested bet. → **Recommend: down-tag to [INFERRED]/[SPECULATIVE] or excise the teaching slogan.** The two sub-facts that trace (completer-can-leave-marginal §10.22; ordering-is-the-effect §10.24) may stay [MEASURED].

**A2. coord 2 "Word-visibility is matched (~0.45–0.50) across all cells [MEASURED]."** Traces to no committed artifact; canon word visibility is 100%; the nearest number 0.456→0.500 is a vision-mask *raise* on one arm, not a match. EXP14 word-mask policies differ by construction. → **Recommend: strip/demote [MEASURED]; name the actually-matched quantity (identical mask multiset per coord 1) or drop the clause.**

---
## B — MUST-FIX numerics (hardened / fabricated / stale under [MEASURED]; need ruling)

**B1. HANDOFF:22 "traverse ≥2.5× ≈0.096-measured" — STALE + mislabeled.** Canon (EXP17 prereg :275-279, orbit-panel MUST-FIX 2, CC error owned) corrected 0.096→**0.0902** (sim expectation; floor ≈0.2255); 0.096 was never measured. Same sentence even acknowledges the correction. → **Recommend: reframe to "≈0.0902 (sim expectation; floor ≈0.2255), contrast-form to the measured tremble traverse baseline @k=11" OR drop the literal (no-literal-is-load-bearing). NO silent 0.096→0.0902 swap that leaves "-measured" standing.** Sibling "0.145-measured" (net/path) is canon-legit, stays.

**B2. coord 2 "matched across fabrics to 0.15% (27.5 vs 13.7) [MEASURED]."** 13.7 ✓. 27.5 = the MEAN (toolkit confirms **27.4756**) but canon TEXT commits median 27; "0.15%" is unsourced; "matched across fabrics" reframes exam-rate calibration (A 27.48 vs C 27.44 differ ~0.15%; the 27.5/13.7 pair is the *dose* axis, not a match). → **Recommend: label "mean 27.5 / median 27", source-or-drop 0.15%, reword "matched across fabrics" to the exam-rate-calibration fact.**

**B3. coord 10 "baseline shift (+0.012–0.020) [MEASURED]."** Canon point estimate **+0.0203** (~5σ); +0.020 is a fair round but **+0.012 lower bound traces to nothing** and low-balls the effect. → **Recommend: state as point estimate +0.0203 (≈+0.020); drop invented +0.012.**

**B4. coord 7 "deep (0.87–0.91)."** Downward truncation of committed within-episode mean **0.876–0.916** (honest round 0.88–0.92). → **Recommend: 0.88–0.92 (or exact 0.876–0.916); note "deep"=above-floor depth +0.36–0.40, a distinct statistic.**

**B5. v1.2 §5.4 "acquisition succeeds in every regime and content demonstrably present upstream [MEASURED]."** Universals canon contradicts: 0/10 at the pure-W=3 acquisition wall; sep_cat ≈0.47–0.50 undifferentiated on the lawful arm throughout. Only "the completer rides the marginal" is [MEASURED] program-wide. → **Recommend: narrow the universals or down-tag "every regime"/"demonstrably present upstream" to [INFERRED].**

---
## C — Count reconciliation (blocks the HANDOFF-tally fold; need ruling)
HANDOFF:40 "Seven design-seat catches" (7 enumerated, its own set). RED_TEAM labels F1–F7 (**seven**) but its header says "catches 9–13" (**five**). Canon (EXP17 prereg:3) "Design-seat catch count: **NINE**." Brief's fold text: "eight by the running count + scripts-are-deliverables process gap [=9, reconciles with NINE] + the terminal red-team's **five** findings." The **"five"** collides with the seven labeled F-items (reconciles only if F4 supersession-mark + F7 hygiene are declared non-catches). → **Recommend: (a) add a one-line "(F4/F7 are folds, not counted as catches)" to RED_TEAM's header; (b) confirm the fold text's "five findings" wording; (c) start the red-team catch numbering at 10, not 9 (canon already at NINE).** Do NOT silent-swap 7→5.

---
## D — Ruled folds: scope corrections from the fact-check
- **F7 under-scopes.** The un-ridered sim figure "~1.4×" sits in **reality_ladder:9 and v1.2:11 body**, not just v1.2's status block. Frame the rider as "freeze CONFIRMS (deployed median 0.2261 = 1.42× floor), does not supersede" (the freeze has landed; EXP17_PREFLIGHT_PACKAGE is now committed). Also v1.1 addendum:26 billiard net/path (0.628→0.525) is untagged sim-lineage. → fold rider into BOTH v1.2 and reality_ladder.
- **F2 (deferred per §4) will still enter canon in EXP_L2:20 AND v1.2:29** ("APU ≈ 0 exactly" overclaim under a global predictor). Ruling: accept it rides with RED_TEAM as the standing record, or add a one-line "[F2-pending: exact under per-dwell best-fit rotation]" caveat now?
- **F4** fold as ruled (L2 trigger → scatter-CONVERTS supersession mark).
- **Brief §1 gap:** neither `MECHANISM_MAP_v1_1_addendum.md` nor `..._reality_ladder.md` status line declares itself *superseded by v1.2, retained as provenance* (only v1.2 claims it). Brief §1 says to verify they do. → add the supersession marker to both fork status lines (fold) or rule.

---
## E — Auto-resolves when the shelf commits as ONE bundle (low)
- Coordinate index (coord 1–10) and design labels (M2, two-wall, rung-3.5, hawk/sheep, scatter, APU) dangle in a canon-only view but resolve once v1.0 map + v1.2 commit together — which this commit does. Numbers all trace; only the index/labels were shelf-internal.
- RED_TEAM "one committed glimpse of pos_err_vis" overstates scarcity (it's a heavily-logged record field, absent from canon *docs*). Reword "one glimpse"→"a heavily-logged record quantity absent from canon."

---
## F — Notes / soft (low; speculative-tier or self-disclosed)
- conversion_gating coord 8 onset-speedup strips canon's "report-don't-attribute / did not free conversion" hedge → carry the caveat (TAG).
- FUTURES "ten restarts" hardens canon's "≈10" (speculative-tier lore).
- EXP18 "~60 runs" arithmetic not shown; "acquisition degrades" specialization on the confusion bound is [INFERRED] not measured.
- HANDOFF "(r≈0.9,16°) THIN" in mild tension with canon's BROAD feasible region + (0.85,18°) freeze; "HEAD 0f18e10" is a self-disclosed point-in-time pointer (now e32f005).
- v1.1 "background pinned UNTOUCHED for L1" is design framing, not a quoted EXP17 fence.
- ops §1.3 tag example "v0.17-orbit-prereg" vs brief §6.2 "v0.17-shelf" (both e.g.; tag is a follow-on task, not this commit).
- conversion_gating "~5–6 mid-dwell vision losses" is [INFERRED-from-canon] (~11×50:50≈5.0–5.5), upper "6" slightly high.

---
## Q2 (cross-doc value drift): CLEAN. No number appears with a different value across docs (99% jump ×3, ~1.4× ×3, +0.142 gradient, 4.5–26.4k onsets — all consistent; only tag/rider scope varies).
