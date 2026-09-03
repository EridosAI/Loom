# The Central Operation — Characteristics Specification

> **Revision note (this session).** The twelve characteristics below are unchanged and
> stable. What moved this session is the *open-questions and tension framing*: the
> 6+8+10 triad now has a leading resolution (the routing-layer move), and decay/growth/
> forgetting have a candidate unification (fluid pooling-state under local confidence).
> These are marked **PROPOSED — not yet pressure-tested**. They are this-session's
> leading resolutions, held provisionally per the project's sit-with-it-before-canon
> discipline. The next chat may ratify or challenge them; it should not inherit them as
> settled.

**Purpose.** This document specifies, in mechanism-neutral language, the operation
we are trying to design. It is written so that a research process can search for
candidate mechanisms by *function* rather than by *name* — and so that any candidate
that comes back can be held against these characteristics and tested for whether it
satisfies the function or merely shares vocabulary with it.

**How to read it.** The vocabulary is deliberately neutral. Where a familiar technical
term would have narrowed the search to one existing mechanism, it has been replaced
with a description of the behaviour. Terms like *wave*, *bundle*, *cortex*, and
*calling-forth* are defined below; they name functions and structures, not
implementations. A candidate mechanism is a good fit only if it satisfies the
behaviours described, not if it resembles the system superficially.

---

## What the system is (orienting description)

The system perceives and acts continuously in an environment. It is built from two
kinds of part.

The first kind is a set of **peripheral processing units**, each dedicated to one
channel of contact with the world — one for vision, one for sound, one for movement,
and others as needed. Each unit handles raw signal in its own channel at that
channel's natural rate (vision changes slowly, sound changes fast), and reduces
whatever happened in its channel into a compact **embedding (a vector summary)**.
These units are both input and output: a vision unit can summarise what was seen, and
a movement unit can take a summary and turn it into action. They are loosely analogous
to sensory and motor cortices, and we call them **cortices** for brevity. Each cortex
maintains its own internal representation space; the cortices do **not** share a common
space.

The second kind is a single **association cortex / central unit** that connects to all
the cortices — analogous to a central nervous system feeding into a brain. This central
unit does not touch the world directly. It only ever sees the cortices' summaries, and
it only ever sends summaries back to them. **The internal operation of this central unit
is what we are trying to design.** Everything below describes the constraints that
operation must satisfy. (We use "association cortex" throughout the rest of this
document; the term is provisional, not a commitment.)

The association cortex runs on a **rhythm** we call the **wave** — analogous to a
brain's sampling rhythm. On each wave, the association cortex polls every cortex and
receives whatever that cortex is emitting to summarise the interval since the previous
wave. Everything arriving on the same wave is treated as having happened "together";
the wave is the system's unit of *now*, and its only notion of simultaneity. Consecutive
waves give the system its only notion of order: what came on the wave before, and the
wave before that, within a short and fading window. There is no clock and no timestamp
finer than the wave.

So, each wave, the association cortex holds a **bundle** — the set of summaries the
cortices just emitted, with no internal order (within a wave there is no finer time).
From that bundle it must **call forth** (evoke) what it expects to accompany or follow
it, send those expectations back to the cortices, and adjust itself by the difference
between what it expected and what the next wave actually brings.

---

## Framing line

> There is one operation. It runs every wave. It takes what each cortex is currently
> emitting, calls forth what it expects to go with that, sends those expectations back,
> and adjusts itself by the difference. Everything else is this operation at varying
> reach and sophistication.

---

## The characteristics the operation must satisfy

1. **Wave-bundling.** Each wave, it receives the embedding each cortex is currently
   emitting (some cortices may emit nothing). Co-arrival within a wave is treated as
   co-occurrence; there is no finer-grained timing available to it.

2. **Cued calling-forth (within-wave).** Given part of a wave-bundle, it calls forth
   the rest — the sight of the bell calls forth the sound.

3. **Cued calling-forth (across-wave).** Given the current bundle, it calls forth a
   likely successor — cup is followed by kettle is followed by pour. Whether this is the
   same mechanism as (2) is left open (see Open Questions).

4. **Tracing.** A called-forth bundle can itself become the cue for the next
   calling-forth, producing multi-step chains without external prompting.

   *PROPOSED resolution (this session) to the compounding-error limit:* the trace is
   **variable-length, gated by confidence** — it runs forward as long as confidence stays
   above threshold and stops when confidence drops. The classic autoregressive doom
   (probability of a fully-correct n-step rollout falling as roughly (1−e)^n) is therefore
   *self-limiting* rather than fatal: the trace halts where accumulated error has eaten
   confidence. Familiarity pushes the halt-point further out — a well-practised sequence
   stays confident for many steps because its large-step predictions have been corrected
   against actual outcomes many times, shrinking per-step error in that region. Reach is
   thus an emergent property of familiarity, not a parameter. (Maps onto the
   reflex-vs-planning split: short confident traces = reflexive, long confident traces =
   goal-directed.)

5. **Strengthening by recurrence.** Bundles and sequences encountered often are called
   forth more confidently and more tightly than those encountered rarely. Confidence is
   a graded property of the evocation itself, not a separate stored score.

6. **Weakening by disuse.** Associations not recurred-upon fade, in coordination with a
   controllable **drift/decay** on the representation space. Fading is a consequence of
   the dynamics, not an explicit deletion step. (Drift/decay is a first-class parameter
   of the system — fixed to begin with, adaptive later.)

   *PROPOSED reframe (this session):* rather than seeking a decay knob *independent* of
   the substrate (which the research found unattested), tie decay to the substrate's own
   **pooling state**. Capacity is fluid: regions unpool under prediction error/pressure
   (plasticity, growth, finer distinctions) and re-pool under sustained confidence/quiet
   (consolidation, graceful loss of detail). Re-pooling 8 weights to 2 keeps coarse
   structure and sheds detail — the "instances dissolve, pattern remains" dynamic. This
   makes decay/growth/forgetting/plasticity *one mechanism running in both directions*,
   controlled by local confidence. Caveat: the confidence trigger likely cannot be
   instantaneous (transient early confidence could re-pool prematurely) — it needs
   sustained-confidence or confidence-plus-low-recent-use. Re-pooling handles detail-loss
   and consolidation; a region never re-touched may still need *drift* to become totally
   inaccessible, so re-pooling and drift may both be present doing different jobs.

7. **No phase separation.** Every wave both *uses* the current structure (to call forth)
   and *adjusts* it (from what arrived). There is no interval during which the operation
   only learns, and none during which it only operates. There is no train/run
   distinction.

8. **Tolerance of a moving space.** Its inputs sit in a space subject to ongoing drift,
   so its associations must remain usable as input vectors shift gradually over time, and
   must naturally favour recently-laid-down material over material the space has drifted
   away from.

9. **Refinement by splitting.** As cortices mature and emit finer distinctions, a single
   coarse association divides into finer ones without a global rebuild — one
   ball-association becoming red-ball and green-ball as capacity and cues permit.

10. **Native-slice consumption.** What it calls forth is a whole expected bundle. Each
    cortex takes its own slice of that bundle and interprets it in its own terms — as
    something to perceive, or something to enact. The operation itself stays blind to
    which is which: it evokes the expected state of everything, and the motor slice of
    that expected state *is* the command while the visual slice *is* the perceptual
    expectation. The command/prediction distinction lives in the cortex, not in the
    association cortex.

11. **Growing reach.** Early, the calling-forth reaches barely past the present and is
    used only as something to be corrected against (registered as surprise). With cortex
    sophistication, the system can look further ahead and use the called-forth material
    to *bias perception before arrival* rather than only to correct after. The operation
    is the same; what grows is how far ahead the system can usefully look and what the
    cortices do with the lead time. (Under the single-step lean below, "reach grows" does
    **not** mean the association cortex emits longer sequences — it means the cortices,
    or the tracing process, can run further forward before error accumulates.)

12. **Coherence as learned, not imposed.** When cortices run ahead at different rates,
    the resulting cross-cortex mismatch surfaces as error and is corrected. Integration
    of the cortices into one coherent agent is something the operation *learns* because
    incoherence is surprising — not a constraint wired in.

---

## Vocabulary discipline (so the called-forth thing and the arriving thing never blur)

- **Bundle** names what *arrives* on a single wave, and what is *called forth* per wave.
  It has no guaranteed internal order.
- **Trajectory** names two things, neither of which is what the association cortex emits
  per wave: (a) the path produced by *tracing* (constraint 4), built one step at a time;
  and (b) the dense, recurring shape a repeated experience forms within a single
  cortex's own subspace (e.g. the visual "smear" that becomes the cup-pattern).

---

## Open questions the search must surface, not foreclose

- **Are within-wave calling-forth (2) and across-wave calling-forth (3) the same
  mechanism or two?** LEANS UNIFIED (research-supported). Attractor accounts realise
  both in one network — symmetric weight terms give within-wave completion, asymmetric
  terms give across-wave succession — and predictive-coding realises both in one
  generative model (spatial vs temporal prediction). The evidence leans toward one
  mechanism, two regimes; not forced, but the prior is now stronger than "open."

- **Single-step vs multi-step calling-forth — the central open question.** Whether
  multi-step look-ahead is the single-step operation *iterated* (tracing a path one step
  at a time, each called-forth bundle cueing the next) or a *distinct* operation that
  emits an ordered trajectory in one act, is left open. **The paradigm leans toward the
  former** — it keeps one operation rather than two — but a candidate mechanism that
  achieves multi-step the second way is not excluded *if it can be shown to be the same
  operation maturing rather than a different architecture switched in.* A solution that
  silently swaps architectures between the single-step and multi-step regimes is the
  failure mode this question exists to catch.

- **The 6+8+10 triad — leading resolution (PROPOSED, not pressure-tested).** Research
  confirmed no published mechanism jointly delivers controllable decay (6),
  drift-tolerant recency-favouring associations (8), and modality-agnostic
  perception/action-blind evocation (10): mature decay/drift mechanisms assume a single
  *shared* space (violating 10), while clean modality-agnostic mechanisms assume a
  *stable* generative model (violating 6/8). **This session's proposed way out: a routing
  layer.** The association cortex operates in *its own single internal space* — neither
  shared across cortices nor identical to any cortex. A learned **routing layer** at the
  cortex↔association boundary translates each cortex's space *into* association-space on
  the way in, and translates called-forth material back *out* to each cortex's space on
  the way out. Consequences: (10) is honoured — cortices keep their own spaces, and the
  association cortex is modality-blind because everything reaching it is already in
  association-space and it has no idea which slice came from which cortex; (6+8) become
  tractable — drift-tolerant associative dynamics now run in *one* space, which the
  literature *can* do. This trades an unsolved problem (binding over separate spaces) for
  a tractable one plus an extra component, and it matches biology (the deep V1→V2→V4→IT→
  association stack *is* the modality→association translation; modality interpretation
  was never in the association cortex itself).
  **Open sub-question — the routing bootstrap.** The routing layer is now load-bearing
  and must *co-develop*: the right translation depends on what the association cortex has
  learned to use, which depends on what the routing delivers — another chicken-and-egg
  loop. Resolution direction (this session): governed by the general reference-and-
  relaxation principle (see below) — start with fixed/dumb routing to make the rest of
  the system observable, then introduce slow (stiff) plasticity with a wide rate gap so
  the cortices experience it as approximately stable, then relax stiffness as it
  converges. Whether the routing co-development is harder than the loops already accepted,
  or just one more of the same kind, is the thing to pressure-test next.

- **The reference-and-relaxation principle (named this session; candidate canon).** No
  plastic component without a slower-changing reference to converge against; the reference
  is itself on a relaxation schedule — stiff early when the system is chaotic, loosening
  as the rough configuration settles. Co-development loops without a stable reference do
  not converge. Instances already in the paradigm: the parent/word-stream stabilises the
  encoder; the fixed wave stabilises convergence learning; stiff routing would stabilise
  the cortex↔association translation. Each relaxes over development (parent recedes, wave
  becomes variable, routing becomes plastic). Stiffness is a *rate hierarchy* (separation
  of timescales), not hard fixity, and stiff-but-wrong is its own failure mode — hence the
  relaxation schedule.

- **What is the unit of the called-forth thing?** Left open (bundle of summaries is the
  working assumption, but the granularity is not fixed).

- **Where does persistence live?** The constraints refer to material being laid down,
  recurred-upon, and faded — but this document deliberately does **not** assert that the
  association cortex "has a memory store." Whether persistence is a separate store, or is
  folded into the operation's own structure (the associations *are* the memory), is an
  open question. *Current lean (this session):* the pooling-state reframe of constraint 6
  points toward persistence folded into the operation's own structure — the associations
  are the weights, and capacity (pooling state) under local confidence is what holds and
  sheds them. Attractor/associative substrates fold persistence into weights this way;
  a separate fast store (CLS-style) remains viable but is not the current lean.

- **Downstream action-selection / arbitration.** In mature stages, evocations may surface
  material to a downstream structure that selects or arbitrates among possibilities
  (anticipated; out of scope for the initial operation). A candidate mechanism that is a
  strong early predictor but **cannot be extended** toward priming (constraint 11) and
  toward surfacing-for-arbitration is the wrong choice even if it wins the early task.

---

## Terms to avoid in any downstream search prompt

These collapse the search onto an existing mechanism and should not appear in a research
query built from this spec: *JEPA*, *transformer*, *attention*, *predictor* (as a noun),
*retrieval* (as in key-value memory), *memory* used bare (say what role it plays —
persistence, association, calling-forth). *Encoder* is acceptable only when paired with a
functional description so it does not simply mean "the encoder half of an autoencoder."
