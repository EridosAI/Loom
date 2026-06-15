# Session Handoff — Paradigm Chat

**What this is.** Handoff from a paradigm-level design session on the associative-memory
system (Weft/PAM lineage). This session stayed deliberately at paradigm/information-flow
level and did **not** drop into mechanism selection. Companion file:
`association_cortex_operation_spec.md` (updated this session — read it second).

**How to enter the next chat (read first).**
- Start at paradigm level. Do **not** jump to mechanism, architecture, or ML technique
  selection. The project's recurring failure mode (≈10 prior restarts) is drift from
  paradigm into familiar ML machinery — most often a transformer next-window predictor —
  which quietly substitutes a conventional system for the novel one.
- Hold the operation spec and the canon as anti-drift anchors. When any mechanism is
  proposed, test it against the spec's *functions*, not its vocabulary.
- Familiarity is a drift vector: the more productive a familiar technique looks, the more
  scrutiny before adopting it. Long elaboration that feels like progress is itself a
  drift risk.
- The current model lineage was previously dragged into transformer characterisation
  (v0/v1/v2 "Inner PAM"). That work is **not** the paradigm — it installed a forward-in-
  time autoregressive predictor where the association operation should sit. Treat the v2
  recalibration cascade as off-path unless explicitly resurrected.

---

## The paradigm as it now stands

One operation, run every wave, never frozen. No train/run distinction; development is
the only mode.

- **Cortices** — one per channel (vision, sound, movement, …). Each is a modality-specific
  processing unit with its **own** representation space (not shared). Eats raw signal at
  the channel's native rate; emits a compact embedding (vector summary) at wave-rate. Both
  input and output (a motor cortex turns a summary into action). Internally deep (many
  processing stages), mostly invisible to the rest of the system.
- **Association cortex / central unit** — connects to all cortices, touches the world only
  through them, operates only in embeddings. **This is the thing being designed.**
- **The wave** — the system's sampling rhythm and its only notion of *now*. Co-arrival in
  one wave = co-occurrence (no finer timing). Consecutive waves = the only notion of
  order, within a short fading window. The most load-bearing and most un-ML element;
  protect it from being quietly turned into a fixed batch loop. Defined as an *imposed*
  clock to start (research independently endorsed this over emergent synchrony). Variable/
  emergent wave is a more ambitious later option — but if it's ever in, it likely has to
  be in from the start (components must develop expecting variability).
- **Memory is not an archive.** Encoders eat the full stream for their own learning; only
  aggregated snapshots persist for the association cortex. Storage is per-cortex (each
  subspace holds its own material), joined by wave-co-occurrence, not by a shared
  geometry. Forgetting is a consequence of disuse against drift, not a mechanism.
- **Growth by differentiation.** Start small and dense; never empty-large. Capacity grows
  by splitting existing dense structure, paced by an intrinsic maturational clock plus
  loop pressure.
- **Second channel (the "parent").** Initially synthetic words paired with visual
  experience; any consistent, partially-aligned, lower-noise channel works. Stabilises the
  encoder so concepts are identifiable across instances; recedes as cross-cortical
  structure takes over. A parent (initially the designer) paces complexity to stay just
  ahead of competence — this external pacing keeps the internal rhythms in tune.
- **Concepts are not stored objects.** They are stable cross-cortical bindings / predictive
  structure. "Bell" is the learned tendency for sight-of-bell and sound-of-bell to evoke
  one another, not a stored unified bell. Splitting a concept (ball → red-ball/green-ball)
  is binding-refinement under more capacity + finer cues, not a special operation.
- **Evocation is one operation at growing reach.** Early: near-present prediction, used as
  surprise/correction. Middle: reaches further, biases perception before arrival (priming).
  Later: surfaces material to downstream arbitration/action-selection (anticipated, out of
  scope, but must-not-be-foreclosed). Each cortex takes its own slice of the evoked bundle
  and interprets it natively — motor slice = command, visual slice = perceptual
  expectation. Inter-cortex coherence is *learned* (incoherence is surprising), not imposed.

---

## What moved this session (four things)

1. **The 6+8+10 triad — broken (PROPOSED).** Research confirmed it as a real unsolved gap:
   nothing jointly does controllable decay (6) + drift-tolerant recency (8) + modality-
   agnostic evocation (10). Proposed way out: a **routing layer** at the cortex↔association
   boundary. The association cortex works in its *own single internal space*; routing
   translates each cortex-space → association-space inbound, and association-space →
   cortex-space outbound. 10 honoured (cortices keep own spaces; association cortex is
   modality-blind); 6+8 become tractable (drift-tolerant dynamics now in one space, which
   the literature can do). Matches biology (the deep cortical stack *is* the translation).
   **Cost / open sub-question:** the routing layer is load-bearing and must co-develop —
   another bootstrap loop. See spec for detail.

2. **Decay/growth/forgetting/plasticity unified as fluid pooling-state (PROPOSED).** Don't
   seek a substrate-independent decay knob (unattested). Tie it to the substrate's pooling
   state: unpool under error/pressure (growth, plasticity, finer detail); re-pool under
   sustained confidence/quiet (consolidation, graceful detail-loss — "instances dissolve,
   pattern remains"). One mechanism, both directions, local confidence as control. Caveat:
   confidence trigger can't be instantaneous (premature re-pool risk). Re-pooling and drift
   may coexist (detail-loss vs eventual total inaccessibility). DEN-style splitting can
   avoid retraining cost by splitting into *identical* copies and letting ordinary
   experience differentiate them at the normal rate (no special retrain phase → preserves
   constraint 7).

3. **Compounding-error in tracing — resolved (PROPOSED).** Traces are **variable-length,
   confidence-gated**: run forward while confident, stop when confidence drops. The
   (1−e)^n rollout doom is self-limiting, and familiarity (practice) shrinks per-step error
   so well-worn sequences stay confident further out. Reach = emergent property of
   familiarity, not a parameter. Maps to reflex (short) vs planning (long).

4. **Reference-and-relaxation principle — named (candidate canon).** No plastic component
   without a slower-changing reference to converge against; the reference is itself on a
   relaxation schedule (stiff early, loosening as config settles). Co-development loops
   without a stable reference don't converge. Instances: parent→encoder, fixed wave→
   convergence, stiff routing→translation. Stiffness = rate hierarchy, not hard fixity;
   stiff-but-wrong is its own failure, hence relaxation. **Action: add to canon** (text
   drafted in chat; consolidate with existing parent/wave entries, which are now instances
   of this single rule rather than independent commitments).

Also confirmed: 2-vs-3 (within/across-wave evocation) leans **unified** (research-backed —
symmetric vs asymmetric terms in one network / spatial vs temporal prediction in one
generative model). Single-step-iterated lean for multi-step also holds and is reinforced by
the error-accumulation evidence.

---

## Open threads parked for next time

- **Routing-layer bootstrap** — pressure-test whether its co-development is harder than the
  loops already accepted, or just another of the same kind. Likely first build: fixed/dumb
  routing as observable scaffold → slow stiff plasticity → relax. (Scaffold-removal
  discipline: decide *now* what observation shows the fixed routing is holding the system
  back, so it actually gets removed rather than becoming load-bearing.)
- **Re-pooling trigger** — needs to be sustained-confidence or confidence-plus-low-recent-
  use, not instantaneous. Design the trigger.
- **Gaps 3–7 from the gap list** (not yet worked at paradigm level):
  3. How each cortex learns *within itself*, and how its intrinsic within-modality
     prediction relates to the convergence-error feedback (two pressures on one encoder).
  4. Initialisation — what minimum pre-existing dense structure lets the loop start
     (the bootstrap-from-newborn problem).
  5. Motor side / agency — proactive vs reactive; does evocation drive action directly.
  6. Reward / salience / affect — why some experience is weighted more; where affect lives.
  7. Within-cortex trajectories vs cross-cortex bindings — same operation at different
     scales, or distinct-and-composing? (Likely falls out of resolving the core operation.)

---

## Housekeeping

- **Spec status:** `association_cortex_operation_spec.md` updated this session. The twelve
  characteristics are stable; the open-questions/tension framing now carries this session's
  PROPOSED resolutions, clearly marked as not-yet-pressure-tested.
- **Canon:** add the reference-and-relaxation principle; check whether it subsumes the
  existing parent and fixed-wave entries (consolidate rather than duplicate). A full canon
  consistency pass is worth doing next session if the current canon is to hand.
- **Research artifact:** the Deep-Research return (12-characteristic mechanism map) is the
  input that drove this session. Headline was the 6+8+10 gap. Its *recommendations* lean
  toward a staged build that defers drift (8) and leans on shared-space mechanisms —
  treat the recommendations with caution (they trade away the novel part first); the
  *tension map* is the more truthful part of that document.
