# MECHANISM MAP — WHAT GATES CONVERSION, AND WHY

**Status: BANKED SYNTHESIS (design seat, 2026-07-11). Not canon until ratified; commits to `docs/` via CC on Jason's word. Every claim is tagged [MEASURED] (verified from committed artifacts, most digit-exact by the design seat's own clone), [INFERRED] (follows from measured facts under stated assumptions), or [SPECULATIVE] (candidate mechanism, discriminating test named). Provenance: FRONTIER §10.20–§10.26, the recency and dwell-kinematics forensics, the EXP17 geometry record.**

---

## 1. The phenomenon

PAM's completer must learn P(word | scene) by masked completion. The recurring failure across the program's history: it outputs P(word) — the marginal — ignoring the scene. **Conversion** = the completer becoming genuinely scene-conditional, measured as sustained episodes of above-band exam accuracy at recency-free positions. The campaign's question: what property of experience gates conversion on and off?

## 2. The measured coordinates

1. **Ordering is the whole effect.** Dwelled and shuffled fabrics contain the *identical* multiset of training examples — same stimuli, masks, exams — under one fixed permutation. Conversion flips with order alone: shuffled converts (C 5/8, D 4/8), dwelled is dead (A 0/8; B's 5/8 is a floor-exact bare-N artifact, obs 5 ≈ exp 4.50). [MEASURED — §10.24, fabric contract code-verified]
2. **Dose is not the lever.** Exam density (means) is matched across fabrics *within dose* — A 27.48 / C 27.44 (high), B 13.72 / D 13.68 (low); within-dose gaps ≤0.3% (the A↔C computed gap is 0.15%; toolkit-corroborated); 2× density within either fabric does nothing. Word-visible fraction (`masking_mix` recipe) is likewise identical across fabrics within dose — A 0.454 = C 0.454, B 0.500 = D 0.500 — differing only ~10% along the dose axis, so crude visibility cannot explain the fabric effect. [MEASURED — `exam_n` means; `masking_mix` word-visible fraction] *(amended per fact-check 2026-07-12 A2/B2 — see SHELF_FACTCHECK_FINDINGS.md)*
3. **The dwelled completer is captured, not collapsed.** Its word completion improves monotonically with dwell depth (err 0.692→0.550 A, 0.693→0.538 B, post-acq recipe) while the shuffled arms are flat to ±0.0006 under the same position labels — the gradient is adjacency-caused. The operator is wave-local, so the improvement lives in the weights: within-dwell drift toward the current word. It sits at the marginal exactly where recency fails — the onsets, where the exams are. [MEASURED]
4. **The drift is reward-caused, not exposure-caused.** Delete the mid-dwell word-losses (word still 100% visible): the gradient collapses (Δ 0.025–0.031 vs +0.142). [MEASURED — §10.26, EXP16 coordinate 1]
5. **The shortcut is not the gate.** With the drift dead and word-participation decisively alive (~0.69, 10× bar), conversion stays at zero real across a doubled horizon — the flat 1M tail excludes "enables slowly." The block is vision-side. [MEASURED — §10.26, EXP16 coordinate 2]
6. **What "dwelled vision" actually is:** ~11 near-duplicate views trembling around one point — per-step novelty 12% of a random look, net/path 0.079 at k≥13, visiting 5.6% of the per-axis pose range; a dwell boundary is a 99% jump. [MEASURED — kinematics forensic, identity-gated]
7. **Conversion is a regime, not a state.** Converters show 2–27 recurring episodes (median 9), deep (0.88–0.92) and long (36–90 windows); non-converters show literally zero; no α-consistent locked-state "sustain" exists at 500k. [MEASURED]
8. **Acquisition survives massing.** Assignment/content-side differentiation succeeds in every regime, including dwelled — and removing the mid-dwell word-loss made acquisition dramatically *faster and tighter* (onsets 4.5–26.4k vs A's 14–300k). The block is localized to the completer's conditional readout, not to representation formation wholesale. [MEASURED]
9. **Boundary condition from 12b:** the word must sometimes be a target to bind at all — participation requires prediction load. EXP16 kept onset targets; participation was alive; the failure is not word-participation. [MEASURED, prior canon]
10. Minor, logged: shuffling shifts the operating baseline slightly (+0.0203, borrow-gate point estimate) — real, small, handled by referent machinery. Durability texture: fabric gates onset; dose *may* gate durability (banked, underpowered), with C's ~2.0× exam traffic as a candidate erosion mechanism. [MEASURED / BANKED]

## 3. The organizing principle: the cheapest-shortcut ladder

**[INFERRED — the single frame that fits all ten coordinates.]** The completer descends to the cheapest loss-reduction available in its *local* gradient stream:

- **Rung 1 — the marginal.** Always available; the floor.
- **Rung 2 — recency copy.** Available when the word repeats and repeating is *rewarded* (dwelled with mid-dwell word-loss). Measured directly as the drift (coord. 3), causally tied to reward (coord. 4).
- **Rung 3 — local visual satisfiability.** Available when consecutive vision-completion targets are near-duplicates (coord. 6): the mid-dwell vision losses can be satisfied by low-level, identity-free local structure — completing a patch of a frame nearly identical to the last ten needs no knowledge of *which member* this is.
- **Rung 4 — content association.** The expensive one: scene→word binding. Engages only when rungs 2–3 fail to absorb the gradient.

The campaign in ladder terms: **EXP13's wall** = lawful fabric maximizes rungs 2–3 (maximal temporal predictability = richest shortcut supply) — retroactively explained. **EXP14** = shuffling kills rungs 2 and 3 simultaneously → rung 4 engages. **EXP16** = killing rung 2 alone leaves conversion dead → **rung 3 alone suffices to block**. **EXP17** = degrade rung 3's precondition (near-duplicacy) while preserving identity persistence and rung 2 intact → the direct test of whether rung 3 was the gate.

Note what the ladder does *not* say: it does not say the completer is failing. Marginal-riding is *optimal* under the shortcut supply — the regime, not the learner, decides which rung pays. That is the deepest sense in which "drift is structural, not resisted" has always been true of the learner too.

## 4. Inside rung 3 — three candidate implementations

All three are compatible with coordinates 1–10 today; they diverge on named predictions. [SPECULATIVE, discriminators named]

**M1 — Local representational kneading (weak form).** Massed near-duplicate completions pull each dwell's frames toward a dwell-local attractor; the fine member-identity axes at the association interface are perpetually locally contracted and re-expanded — an unstable substrate the word channel cannot bind to. *Constraint already in hand:* acquisition-alive (coord. 8) kills the strong form (gross representational collapse would damage differentiation); only interface-local instability survives. *Prediction:* orbit converts (near-duplicacy was the poison); driven-plane representation metrics stabilize under orbit.

**M2 — Blocked-update interference at the association weights.** ~11 consecutive gradient steps per dwell carry rank-≈1 information (one scene-neighborhood); consecutive blocks partially overwrite shared weights; the stationary point of block-alternating optimization is the marginal. *Constraint in hand:* the word-target version of this died with EXP16 (onset-only word targets, consecutive dwells different members — still dead); only vision-side blocking survives, and X *retained* its ~5–6 mid-dwell vision losses per dwell, consistent. *Prediction:* orbit de-masses the vision *targets* (progressively new views) while keeping identity blocked → orbit converts iff the poison is target-duplication rather than identity-repetition. *Checkable rider:* the optimizer's state (momentum / second moments) interacts with massed blocks — **pin the optimizer from code**; if stateful, its timescale is a load-bearing constant of M2 and cheap to read.

**M3 — Effective-window starvation.** Under any finite effective memory (curvature overwriting, optimizer state, decay), the learner's *effective dataset* is its recent window. Dwelled fabric makes that window ≈ one (member, word) pair; you cannot learn a conditional from one pair at a time; the only structure stable across windows is the marginal. *Sharp fork inside M3:* if what must be diverse is the *input*, orbit converts (11 distinct views); if the *(pair)*, orbit dies (still one member per window). *Prediction beyond EXP17:* a block-length titration shows conversion turning on as blocks shrink past the learner's effective horizon — a threshold, not a cliff at exact-shuffle. This is exactly the banked dwell-length titration.

**How EXP17 splits them:** ORBIT CONVERTS → the gate was near-duplicate *targets/inputs* (M1-weak and M2-vision-as-duplication and M3-input all live; identity persistence exonerated; coherent experience can convert). ORBIT DEAD → the gate is identity-blocking per se (M3-pair; interleaving campaign; dwell-length titration is the direct knob). Either way one full branch of the tree dies.

## 5. Falsification table — for the map itself

- **Gradient-persistence control fails in the orbit arm** (drift should persist ≈ +0.142 — grading intact): the arm changed more than kinematics → attribution void, instrument audit before any reading.
- **Interior-concentration control converts** (post-CONVERTS: a *tremble* at the orbit's center distribution): the orbit's conversion was pose-distribution, not motion → the novelty reading dies; distribution-level accounts revive.
- **Dwell-length titration shows no onset-rate dependence** (post-DEAD): the interleaving account fails too → the ladder is broken below rung 3 → escalate to representation-level probes (the map's frame, not just its branch, is wrong).
- **Partial-shuffle shows conversion only at exact-shuffle** (no threshold): "effective window" is wrong and something about the permutation itself is doing unrecognized work → audit the perm.
- **Acquisition degrades in any rung-3 manipulation:** the acquisition/conversion dissociation (coord. 8) is regime-limited → M1-strong revives and the interface-local story was too weak.

## 6. Paradigm audit — evocation-as-teacher

**Established** [MEASURED]: the completer *can* leave the marginal — the founding capability is real; the enabling condition is a property of experience-*ordering*, not exposure content. The **associative pathway engages** where experience stops being locally satisfiable [MEASURED — completer-level, EXP14/16]. Whether that engagement then **teaches the encoder** — evocation-as-teacher proper — remains [PROPOSED, untested]; the bootstrap-as-control (v1.2 §5.5) is its named test. *(Amended per fact-check 2026-07-12 A1 — the session's most important catch: the paradigm's founding bet was tagged Established/[MEASURED]; the measured fact is completer-level, the encoder-teaching claim stays [PROPOSED, untested]. See SHELF_FACTCHECK_FINDINGS.md.)*

**At stake:** the paradigm bet says minds develop through temporally *coherent* experience — and to date the only converting regime destroys coherence. EXP17 is the first test of whether coherence and conversion are compatible. Three outcomes for the bet:
- **Sweet spot exists** (orbit-class regimes convert): the bet survives, sharpened — *coherent AND non-degenerate* experience teaches; lawful worlds must be built so their predictability never makes the posed losses identity-free-satisfiable. That is a design principle for every future fabric, and it makes the EXP13 re-pose designable (lawful motion IS a sweep).
- **Only interleaving converts, monotonically** (titrations show less-coherence-is-strictly-better with no interior optimum): the bet fails *in its current form* — the teaching signal is incompatible with lifelike experience under this objective. The honest moves are then developmental scheduling (interleaving-early curricula) or re-posing the completion objective — the latter is manufacturing-adjacent and is a Jason-level design decision, never an experiment-level patch.
- **Nothing coherent ever converts and titrations are flat:** the frame is wrong somewhere deeper; return to the substrate.

**What the map does not claim:** no biological fidelity; no claim the marginal is a defect (it is the regime's optimum); everything regime-scoped — nothing here transports outside the fabrics measured.

## 7. Open questions, ranked

1. EXP17's outcome (in flight) — splits the rung-3 candidates.
2. The optimizer pin (code-read, cheap) — M2/M3's timescale constant. [PINNED 2026-07-24 → optimizer_pin.json: τ₁=10, τ₂=1000]
3. Post-branch: interior-concentration control (CONVERTS) or dwell-length titration (DEAD) — both pre-named, both banked.
4. Partial-shuffle threshold — the effective-window measurement; also the natural home of Jason's correspondence-window theory (the hawk/sheep bound as the titration's upper knob).
5. Durability: does exam-traffic erosion explain decay (the ~2.0× verified traffic asymmetry), and does the recency drift *maintain* as well as block?
6. The acquisition-speedup anomaly (X 6–10× faster onsets): why does deleting the word-drift accelerate differentiation? Possibly the drift's oscillating gradients slow assignment settling — unclaimed, cheap to probe from existing checkpoints.

---

**Plain language.** The learner has a ladder of ways to be lazy, and it always takes the lowest rung that pays. Give it a world where the same word keeps being quizzed right after it was shown — it copies. Stop rewarding the copying (we did) — it drops to an even lazier trick: the world barely changes frame to frame, so it can ace the picture-completion quizzes with local pattern-matching that never needs to know *what it's looking at*. Only when the world stops being locally easy — today, only when we shuffle it — does it climb to the top rung and actually learn what goes with what. The experiment in flight asks the decisive question: if the world stays coherent but *keeps moving* — every frame a genuinely new look at the same thing — is that hard enough to force real learning? If yes, the whole bet survives in sharpened form: experience teaches when it is coherent but never boring. If no, we learn that what the learner needs is rapid alternation between different things, and we go measure exactly how rapid.
