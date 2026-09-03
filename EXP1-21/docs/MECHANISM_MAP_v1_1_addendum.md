# MECHANISM MAP — v1.1 ADDENDUM (Jason's notes folded, 2026-07-11)

**Status: BANKED SYNTHESIS, reads WITH `MECHANISM_MAP_conversion_gating.md` (v1.0). Both ride to `docs/` together on ratification. Source: Jason's two design notes (orbit skepticism / reality-is-the-teacher; CWP + pretraining). Nothing in v1.0 is retracted; two of its claims are sharpened and one gap is closed.**

**[SUPERSEDED by `MECHANISM_MAP_v1_2_RECONCILED.md`, 2026-07-12 — retained as provenance, not deleted:** this is one of the two v1.1 forks v1.2 reconciles (the other is `MECHANISM_MAP_ADDENDUM_v1_1_reality_ladder.md`); where this doc and v1.2 differ, **v1.2 governs**.]**

---

## A. The gap: novelty ≠ unpredictability (v1.0 conflated them)

The orbit delivers per-frame **novelty** (never revisits) but is **maximally predictable** — a constant-ω circle is exactly where extrapolation says it is, every frame. v1.0's rung 3 ("local visual satisfiability") therefore has a variant the orbit *feeds* rather than starves:

**Rung 3′ — extrapolative satisfiability [SPECULATIVE, discriminator named].** The mid-dwell vision losses are satisfiable by short-horizon extrapolation of recent frames — no member identity required. Copying (rung 3, duplicative form) needs near-duplicate frames; extrapolation needs only *smooth* frames. The orbit kills copying and maximally enables extrapolation.

**Amended EXP17 outcome table (supersedes v1.0 §4's split):**
- **ORBIT CONVERTS** — stronger than v1.0 claimed: exonerates *both* duplication AND predictability as gates (the most predictable coherent motion converts). Best possible news for the EXP13 bridge — lawful motion is predictable by definition. Identity persistence exonerated. Rung 3′ dead.
- **ORBIT DEAD — now ambiguous between two campaigns**, and the ambiguity is resolvable by one cheap arm before any interleaving conclusion:
  - Rung 3′ (predictability is the gate) → **the hand-held arm** (Ladder L2 below) discriminates;
  - identity-blocking per se (M3-pair) → the dwell-length titration.
  **Sequencing ruling: L2 runs first.** It is one generator knob from the orbit build (randomize ω_t, occasional plane wobble), and it stays on the reality-is-the-teacher trajectory rather than retreating to order destruction. The titration is the fallback if unpredictable-coherent also fails.

## B. The Reality Ladder (banked escalation — nothing discarded at any rung)

Principle (Jason's): *reality is the teacher* — the campaign's product is the **minimal reality-subset that converts**. Each rung adds ONE reality property, keeps all prior properties, and is a minimal generator delta with the standing corridor machinery. Each rung's conversion read is against the rung below it.

- **L0 — tremble** (current dwell): novel-free, predictable, duplicative. Dead. [MEASURED]
- **L1 — orbit** (EXP17, in flight): + per-frame novelty; still predictable. Cheap (built).
- **L2 — hand-held**: + increment unpredictability — ω_t stochastic (e.g., positive random around ω̄), occasional plane wobble; "a slightly different angle each time." Novel AND unpredictable AND identity-persistent AND correspondence-window-coherent. One knob from L1. *Geometry note carried from the billiard lesson: raw random-walk anchors fail net/path by construction (statistical revisiting); L2 keeps monotone phase — persistent trajectory, unpredictable increments.*
- **L3 — contexts**: + background varies per dwell (constant within, different across — "the mug in two kitchens"). Forces identity to bind to the object rather than the scene: the current fabric holds background near-constant per run (OU toward `bg_const`), so object and context are confounded today. Moderate delta (background draw per dwell). *Fence rider inherited from EXP17: the background path was pinned UNTOUCHED for L1 — L3 is where that pin is deliberately, explicitly lifted, one moving thing at a time.*
- **L4 — appearance**: + lighting / render-axis variation within dwell. Renderer work; costliest; last.

Each rung also sharpens the paradigm claim if it converts: the minimal sufficient rung IS the finding. If nothing on the ladder converts and only interleaving does, §6's middle outcome fires — with section C now supplying its candidate resolution.

## C. CWP and pretraining (Jason's paper, folded)

**C1. The connection [INFERRED — strong, testable].** CWP's documented failure mode — cannot distinguish "my representations are wrong" from "downstream is pushing me around" — is *our measured phenomenon*: the recency drift is precisely "being pushed around" (within-dwell word gradients shoving completer weights; reward-caused, coord. 4). We cured it environmentally. But CWP run forward in THIS fabric does something the map needs: confidence rises mid-dwell (recency predicts well) → plasticity closes → massed redundant updates are damped; surprise spikes at dwell onsets → plasticity opens at exactly the informative transitions. **Surprise-gated plasticity is an automatic interleaving filter: it makes massed experience effectively interleaved at the gradient level.** This is the standing candidate resolution to v1.0 §6's middle outcome (if only interleaving converts): reality does not shuffle — *brains gate*. It converts a paradigm-breaking result into a mechanism requirement.

**C2. Why Loom is a better CWP host than its original testbed.** CWP's three architectural requirements — independent grounded prediction streams, modular gradient paths, continuous sensory grounding — are largely native here: vision-slot completion, word-slot completion, and assignment are separable, logged, externally-grounded streams. And the program owns fabric-side ground truth: regimes can be *constructed* where "wrong representations" vs "being pushed around" is known by design — making CWP's irreducible-at-signal-level ambiguity empirically probeable for the first time.

**C3. Sequencing fence [RULING-CLASS, for ratification].** CWP enters only AFTER the reality ladder locates the minimal converting regime. Added earlier, it confounds every regime finding (conversion attributable to fabric or to gating — undecidable). Regime map first; gating mechanism second, with the regime map as its baseline and the ladder's dead rungs as its test suite (CWP's prediction: it should rescue conversion on rungs the plain learner fails).

**C4. Pretraining verdicts [INFERRED from coords. 5, 6, 8].**
- **Wholesale pretraining does not fix this and may deepen it.** The block is not representation quality: acquisition succeeds in dwelled fabric (coord. 8) and the failure is stationary, not slow (flat 1M tail, coord. 5). A better encoder makes local completion *cheaper* — rung 3/3′ easier — plausibly worsening the trap. And it deletes the paradigm's testable content: a pretrained encoder leaves evocation-as-teacher nothing to teach.
- **A frozen-pretrained-encoder arm is a legitimate diagnostic — the M1-eliminator.** With representations that cannot knead, M1 is impossible by construction: dead-under-massing kills M1 outright; converting confirms representation instability was the gate. Banked with trigger: fires if the EXP17 line leaves M1 vs M2/M3 ambiguous. Clearly labeled a **non-paradigm scaffold** — it answers a mechanism question, then is removed. (V-JEPA-bootstrap-then-PAM as a *product* architecture is a separate, later conversation that must not contaminate the mechanism campaign.)

## D. Open-questions list, re-ranked (supersedes v1.0 §7 ordering)

1. EXP17 / L1 outcome (in flight).
2. Optimizer pin from code (unchanged — now doubly relevant: it is also CWP's interaction surface).
3. Post-L1: L2 hand-held (if DEAD) or interior-concentration control (if CONVERTS) — both pre-named.
4. Ladder rungs L3/L4 (banked, in order).
5. Dwell-length titration — demoted one rung by the L2-first sequencing ruling, still the interleaving campaign's opener if the ladder exhausts.
6. CWP program (behind the ladder, per C3) — with the ladder's dead rungs as its test suite.
7. Frozen-encoder M1-eliminator (trigger-banked).
8. Durability/erosion and the acquisition-speedup anomaly (unchanged from v1.0).

---

**Plain language.** Two upgrades from Jason's notes. First: our moving-camera experiment tests whether *newness* is enough — but its motion is perfectly smooth, so a learner could still coast by predicting the next frame instead of understanding the object. If it converts anyway, wonderful — even predictable motion teaches. If not, the next move isn't giving up on realistic worlds; it's making the motion slightly jerky, the way a hand-held object actually moves — then different rooms, then different lighting — adding one drop of reality at a time until learning switches on. The recipe of drops that finally works is the discovery. Second: Jason's old plasticity paper may be the endgame's missing piece — a brain-like rule where components learn fastest exactly when they're surprised. In our world, that rule would automatically ignore the boring repeated frames and learn hardest at the moments something changes — which is what shuffling fakes by brute force. Reality doesn't shuffle; attention does. We'll test that properly — but only after we know exactly what the world alone can and can't teach.
