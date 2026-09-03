# Substrate — Pooling-State Capacity 

> Status: structure closed this session. One empirical knob deferred (use-window). Mechanism-level, not paradigm — this is the first deliberate mechanism commitment.

## Core choice

**Soft-tied weight pooling.** Full parameter budget allocated at init; nothing is ever added or removed. "Capacity" is _resolution_, not parameter count. A group of physical weights softly tied toward its own mean acts as one effective weight (low resolution); loosening the tie lets members diverge (higher resolution). Pooled↔unpooled is a continuous constraint strength, not a surgical split.

- The tie is a **penalty, not a hard equality**. Hard tying makes copies identical forever (no symmetry break, no differentiation). Soft tying keeps members clustered but lets latent differences express when loosened.
- This is soft weight-sharing (Nowlan & Hinton) with the cluster tightness driven by **local error**, not a global compression objective. That swap is what makes it ours.

## Structure — fixed nested tree, adaptive depth

- **Which weights can split from which is fixed at init** (a nested tree, e.g. 1→4→16). _How far down any branch is currently unpooled_ is fully adaptive.
- Envelopes are **concept-agnostic** at init — uniform generic structure; whatever the input statistics route into a region is what it becomes. Not "16 weights for ball."
- **Heterogeneous depth is the normal operating state.** Different branches sit at different resolutions simultaneously.
- **Siblings independent; ancestors gate descendants.** A branch re-pools without affecting siblings. But a node can only be unpooled if its parent is — fine distinctions live inside coarse ones, so depth along any path is monotonic. Re-pooling a node implicitly collapses everything beneath it.
- Consequence (free, useful): re-pool high in the tree = big reclaim (whole category); re-pool at a leaf = small reclaim. Graceful detail-shedding, leaf-first, falls out of the tree shape.

## Dynamics — two directions, one local signal

**Unpool (capacity opens) — clock-led, NOT error-pulled.**

- Paced by a maturational clock: `rate = base_rate × activity_gate`.
- **v1: gate pinned to 1** (fixed, predictable rate). The gated form is in the structure, dormant — released later. Harmless in v1 because vision+word are both always active; the gate only earns its keep once a channel can sit idle (audio before sound, etc.).
- Capacity opens _first_; perception of the finer distinction _follows_ once room exists. Reason: the system can't detect "I need a distinction I can't currently represent" — the distinction is unrepresentable until capacity is there. So growth leads, error consumes. (The red-ball realisation lags the capacity, as in real development.)

**Differentiation of freed members — intra-group gradient disagreement.**

- Once a group is unpooled, members still receive their own gradients. If those point apart, experience differentiates them (red vs green). This is the **consumption** signal — what freed capacity _becomes_ — NOT the unpool trigger.

**Re-pool (capacity reclaimed) — reversible re-tightening.**

- Trigger: **sustained low intra-group disagreement AND sustained low recent use.** Both required. Low disagreement alone would re-pool successfully-learned distinctions (they're also quiet); use distinguishes mastered-and-active from unused.
- **Reversible tie, not migration.** Re-pool re-tightens the prior in place; freed resolution stays _within its own branch_ (no cross-region reallocation).
- **Fast-out / slow-in hysteresis.** Unpool/differentiate responds promptly; re-pool waits for _sustained_ low-use. Prevents thrash and protects dormant-but-real distinctions (the once-a-year grandmother).
- **Graceful.** Re-pool sheds detail, keeps coarse value ("instances dissolve, pattern remains"). Worst case is coarsening, never erasure — so it's safe to set somewhat aggressively; re-encounter rebuilds the split fast against the surviving coarse frame.

## Cross-compat — same law both halves (this is the gap-3 fusion)

The identical pooling law runs in the **encoder** and the **association cortex**, each fed by its native error:

- Encoder: JEPA predictor error → gradients → per-group disagreement.
- Association cortex: convergence error (evoked vs actual) → gradients → per-group disagreement.

Convergence error reaching the encoder _adds to its gradients_, which surfaces as extra disagreement pressure — so **evocation drives encoder differentiation literally**, not metaphorically. One control law, two error sources, both halves. Weight-level is the only unit that is the same object in both halves (why neuron-level and basin-level were rejected).

## Caps (chosen, not defaulted)

- **Cap 1 — total parameters.** Fixed budget. Trivial; true of any model.
- **Cap 2 — per-region ceiling.** Because the tree is fixed at init, each region's max resolution is frozen _before the system has experience to inform the partition_. Freed capacity reuses only within its own branch. **Accepted for v1** (with a generous budget and only vision+word, no region should hit its ceiling). Migration across branches would dissolve Cap 2 but is known-messy and deliberately excluded. Revisit only if a domain proves it must exceed its init-guessed share.

## Guardrails

- **Efficiency is emergent, never an objective.** System-wide efficiency is the _consequence_ of local re-pool of low-disagreement branches, not a global "minimise weights" term. The moment it becomes a target, a global loss is back (violates the no-external-objective commitment).
- **Drift, not re-pool, is the only true eraser.** Re-pool lowers resolution; total inaccessibility comes from representational drift carrying a region away, on a much slower timescale. Characteristic 6 is served by _two_ things doing different jobs — pooling-state (resolution/consolidation) and drift (eventual inaccessibility).
- **JEPA boundary.** Cortices are JEPA-pattern encoders (online from init, small-and- growing, predictor confined to the cortex). The **association cortex is not a JEPA** — it's the associative/pooling substrate that consumes embeddings. The predictor never becomes the evocation operation.

## Open / deferred

- **Use-window length** (the dormancy tolerance in the re-pool trigger) — the one free parameter. Empirical: depends on how often real distinctions recur in the environment. Make it a tunable with a deliberately long default; find it by observation, don't derive it.
- **activity_gate** — built but pinned to 1 for v1; release when an idle channel exists.