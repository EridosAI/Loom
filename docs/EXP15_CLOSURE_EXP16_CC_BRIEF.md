# CC BRIEF — EXP15 CLOSURE (RELEASED) + EXP16 (STAGED)

**Date:** 2026-07-10 · **Authority:** Jason's GO on Rulings 1–3 (design chat) · **Repo:** `EridosAI/Loom` `main`, origin in sync at `5e1ff0e`. Author of all commits: Jason Dury, no co-author. Report-don't-patch. Loss-engineering FENCED; EXP13 PAUSED.

**Structure: Part 1 is released now. Part 2 is STAGED — it does not start until the Part-1 verdict surface has routed through Jason.**

---

## PART 1 — EXP15 CLOSURE (RELEASED)

Ruling 1 = menu option (i): execute the capped top-up per the letter, expecting the floor miss, on the record. Ruling 2 = pre-check moves to the deployed horizon. Ruling 3 = no relabel; UNDERPOWERED with the annotation below.

### 1.1 Pre-check {40–47} at the DEPLOYED horizon (Ruling 2, new standard)

- Fabric-assert both arms at **T = 1M** (the deployed fabric — build is 36.4 s, cost is nothing). **1M decides.**
- Run the 15 k screen too, **advisory only** — record, never rejects.
- Outcome-blind; ruled substitution: reject → lowest unused seed from {36, 38, 39} then upward, pre-checked at 1M under the same standard, recorded. (s36's known 15 k failure is now advisory; its 1M result decides if reached.)

### 1.2 Run the top-up

- **{40–47} × {exp12_shuffle, exp12_split} = 16 runs**, `read_at=1M, h_max=1M, mid_ckpt_at=500k`, threads=1, faithful runner, one fixed perm per arm (existing), `.pt` per contract.
- Full cap in one batch — ruled ("runs the 16"); the pairs choreography was incremental floor-checking, which Ruling 1 supersedes since the miss is expected and the batch is for the record + descriptive value.

### 1.3 Final score at n=28

- Primary **unchanged and frozen**: exact tie-aware MW one-sided (D>C) on final-quartile time-above-band (416 windows in (375k, 500k], ruler 0.6875), eligible converters (≥5-consec-≥ruler ∧ longest-run ≥ 8 ∧ runway ≥ 200k), **new seeds only** (now {8–19}\{10} ∪ {28–35} ∪ {37} ∪ the checked {40–47}). Committed 16 stay quarantined context.
- Floor audit + bare-N census in the surface. Sensitivities as registered. 1M tail descriptive.

### 1.4 Panel addendum

- Continuation of `wf_80ee0e95`, refute-default, **no lens assumes D>C**; reproduce the load-bearing n=28 numbers from raw records. Brief — the n=20 panel stands; the addendum covers only what n=28 changes.

### 1.5 Canon DRAFTS (write, faithfulness-check, do NOT commit)

Draft the following; run the faithfulness + directive-coverage check (the `wf_6dd5ab14` pattern: every number re-derived from artifacts; every directive landed where a successor hits it) before surfacing:

1. **FRONTIER §10.25 — EXP15 verdict.** Outcome cell **UNDERPOWERED per the letter** (floor 12/cell vs eligibles at n=28), with the ruled annotation verbatim in spirit: *"floor structurally unreachable under this design at feasible n (P≈0.10 at cap, pre-top-up); direction D>C suggestive (p at n=28, robust to eligibility-gate variants, carried by k of m observations — not characterizable); banked behind the mechanism campaign."* Fill p/k/m from the n=28 score. Include: the peek-quarantine note (committed-16 inclusion → p≈0.009, excluded by registration), C's near-zero fracs = genuine early-converter decay (real durability failure, measured), Ruling-3 machinery worked (phantom-free pool, empty 8–18 gap).
2. **Design-seat ownership + standing rule** (F1-family, instrument-side): *the 12/cell floor was ratified before Ruling 3's eligibility gate and never reconciled — when an eligibility gate changes, every downstream constant that assumed the old eligible rate is re-derived before GO.*
3. **Pre-check re-pin:** pre-checks run at the deployed horizon; 15 k demoted to advisory; the assert suite's per-seed false-alarm rate stated explicitly (you have the number — one-in-20 at expectation) so future rejections are read against expectation; the s10/s36 finding recorded (passes 15k/100k/500k, fails only at 1M by 3%; s10 ≠ s23; ruled swap applied literally, outcome-blind).
4. **Banked fork with trigger:** durability-by-dose re-poses only if the mechanism campaign makes it predictable; candidate hypothesis noted for EXP16-successors — C's 2× exam traffic as post-conversion erosion.
5. PROJECT_STATE bullet · progress_log entry.

### 1.6 HARD STOP → surface for Jason

Surface together: top-up pre-check (any swaps) · n=28 score + outcome cell · panel addendum · floor audit / bare-N census · canon drafts + clean faithfulness check. **Nothing commits.** On Jason's ratification: **one commit** (40+16 records, panel + addendum, canon set), push, origin sync confirmed. Then Part 2 opens.

---

## PART 2 — EXP16 CAPTURE-FEED DISCRIMINATION (STAGED — opens only after the Part-1 surface routes)

The prereg is ratified (design chat, 2026-07-10). One amendment before it goes to panel, then the ratified §7 sequence verbatim.

### 2.1 Amend prereg §7 (pre-panel, ruled)

Pre-check line becomes: **fabric-assert at the deployed horizon (1M; fabric pre-built at h_max=1M), 15 k advisory only** — the EXP15 Ruling-2 standard.

### 2.2 The ratified sequence (from the prereg, unchanged)

1. **Prereg behind an adversarial refute-default panel** (on the prereg itself, pre-commit).
2. **Commit:** prereg + the **recency-forensic canon entry riding with it** (capture-not-collapse: order-only fabric fact; dwelled pos_err_word gradient 0.692→0.582 / 0.694→0.579 vs shuffled flat; wave-local operator ⇒ within-dwell weight drift; cheapest-shortcut at the learning-dynamics level; EXP13-wall unification note). Fact-check every number against committed traces before it enters canon (the Step-0 rule — these figures originated in the design seat).
3. **Build:** new flag `expo_midword` — exposure-only iff `slot==1 AND NOT is_exam AND expo_midword`. A new flag; `expo_word` semantics untouched (12bc twins' pos-1 behavior must not move). Zero draw-consumption change. Smoke: digit-identity on ALL existing arms + stream bit-identity of `exp12_dwell_expomid` to `exp12_dwell` at seed.
4. **Cal:** {20,21,22,24,25} @ 500k (run to 1M, mid-ckpt 500k, EXP15 pattern) → honest band (provisional §10.22 method; C-precedent pre-named if cal converts: own between-episode null, referent recorded) + acquisition-liveness + **recency-gradient-at-cal** (Δ(p1 − p13-48) on pos_err_word, new arm vs A).
5. **HARD STOP → surface** band / liveness / recency-gradient for Jason's read. **Verdict {0–7} releases only on Jason's GO.**
6. Verdict → DRAFT halts → refute-default panel (**no lens assumes conversion**) → routes to Jason. Outcome cells per prereg §4 (converts ⇒ WORD-SIDE CAPTURE; dead ⇒ VISION-SIDE MASSING; lottery ⇒ EXT_POOL {8,9} before any row; cal-converts/liveness-fail pre-named). Mechanism companion §5 (gradient-collapse × conversion 2×2) reported, not gated.

---

**Standing at every gate:** surface-recommend-stop; verdicts, canon writes, and pushes each wait for separate explicit authorization; plain-language translation with every ruling; nothing is real until written to `docs/`.
