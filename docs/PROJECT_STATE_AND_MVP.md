# Project State & MVP — Associative-Memory System (Weft / PAM)

**What this is.** The complete current state of the architecture: every decision, where
it stands (settled / proposed / deferred), the open gaps, and a suggested MVP. Written to
be self-contained — the base for a new chat to develop the MVP. Companion: `HANDOFF.md`
(how to work), `substrate_description.md` (substrate detail), the twelve-characteristic
spec (stable), the mechanism map (possibility space).

> **Status legend:** **[SETTLED]** decided and stable · **[PROPOSED]** this-lineage
> leading bet, not yet pressure-tested, do not inherit as settled · **[DEFERRED]** real
> but out of scope, with a named re-entry trigger.

---

## 1. The paradigm in one paragraph

One operation, run every wave, never frozen. The system perceives and acts continuously;
there is no train/run distinction — development is the only mode. It is built from
modality-specific **cortices** (each with its own representation space) feeding a central
associative operation. The central operation, each wave, takes what the cortices are
emitting, **calls forth (evokes)** what it expects to accompany or follow that, sends the
expectation back, and adjusts itself by the discrepancy. Memory is not an archive: the
associations *are* the structure. Concepts are not stored objects — they are stable
cross-cortical bindings. Everything the system does is this one operation at growing reach
and sophistication.

The twelve characteristics in `association_cortex_operation_spec.md` are **[SETTLED]** and
must not be re-litigated.

---

## 2. Architecture as it now stands

Three components. (This is the post–"router collapse" architecture — see §7 for what
changed.)

### 2.1 Cortices **[SETTLED in shape]**
- One per channel. **v1: vision + word.** Each has its **own** representation space — not
  shared across cortices.
- **JEPA-pattern** feedforward predictive embedders: eat raw signal at the channel's
  native rate, emit a compact embedding (vector summary) at wave rate. Both input and
  output (a motor cortex turns a summary into action).
- Internally run a **native-grain intrinsic prediction loop** (e.g. vision predicting its
  own next frame at ~frame rate). This is the encoder's own consistency mechanism and is
  ongoing regardless of developmental stage.
- **The word cortex is the stability anchor** ("the parent"): a pretrained, near-trivial,
  high-accuracy encoder providing clarity and certainty for the rest of the system to
  co-develop against. Recedes in influence as cross-cortical structure takes over.

### 2.2 PAM (Predictive Associative Memory) — the central operation **[SETTLED in shape]**
- The sole **associator**. Built on the pooling substrate (§4). Operates in its **own
  internal latent**.
- Three stages, which *are* what used to be called "the router":
  - **Encode** (cortex-space → PAM-latent): fuses the cortices' summaries into one input.
  - **Masked completion in latent**: the associative operation. Given a partial
    wave-bundle (or a recall cue), completes the rest — evokes the expected bundle.
  - **Decode** (PAM-latent → cortex-space): renders the evoked bundle back out; broadcast
    to all cortices, each of which takes its own slice.
- **PAM is NOT a JEPA in the sense of "an encoder you freeze."** It is the
  *masked-completion operation*, online from init, with its encode/decode as a
  co-developing matched pair.
- PAM is **modality-blind**: encode dissolves slice-identity going in; cortices
  reconstruct slice-identity at the edge going out. PAM-in-the-middle never knows which
  slice is which (characteristic 10).

### 2.3 Store — passive experience buffer **[SETTLED in shape]**
- A **separate, passive** component. Holds experience; does **no association**.
- Lives in **cortex-space** (same space the cortices emit and PAM decodes into).
- **Content-addressed**: a cue (live perception, or a PAM recall rendered to cortex-space
  via decode) pulls the nearest-content stored material. No index, no retriever, no
  order-field — *address is content*.
- Holds **ordered spans** (not isolated frames); order rides *inside* the stored embedding
  as content (position-as-content). Co-occurring items were stored in the same
  bundle/span, so "togetherness" is set at capture, not linked later.
- **PAM cannot tell store from reality** — replayed material re-enters through the same
  input pathway as live perception. This is what makes replay grounded and phase-free.
- Reached by PAM **through the decode**, exactly like a cortex. (Jason's "memory cortex"
  intuition, vindicated: the store is addressed like a cortex.)

---

## 3. How it works — the two loops

### 3.1 Perception loop (every wave) **[SETTLED in shape]**
Cortices emit summaries → **encode/fuse** → PAM **completes** (evokes expected bundle,
including expected slice for each cortex) → **decode** → broadcast → each cortex takes its
slice and interprets it natively (motor slice = command, sensory slice = perceptual
expectation; characteristic 10) → next wave arrives → **convergence error** (evoked vs
actual) drives adjustment.

### 3.2 Recall loop **[SETTLED in shape]**
Cue (cortex-space) → encode → PAM **associates** (completes from learned weights) →
**decode to cortex-space** → **content-addresses the store** → surfaced bundles become the
next cue. The decode is *in the recall loop*, not just perception — this is what makes
PAM-space (internal) and store-space (cortex-space) compatible.

**Two relations, alternating:**
- **Similarity** — nearness in an encoder's embedding space (green-ball near tennis-ball).
  Free from the encoders. A within-representation relation.
- **Association** — co-occurrence binding (tennis→umpire). Lives in PAM's weights and in
  the store's at-capture bundling. An across-experience relation.
- Creative/exploratory recall **alternates** between the two (similarity hop, then
  association hop). The permutation explosion across both branching factors is the source
  of creative reach. **[PROPOSED]** what selects similarity-vs-association each hop:
  highest-confidence next-step wins, alternation emergent rather than scheduled.

**Hop-looseness is governed by confidence/vividness:** vivid/grounded cue → tight,
high-probability hops (focused recall); faint cue (deep in a chain, or low attendance) →
loose, low-probability hops (daydreaming / creativity). Reality-grounded = focused;
memory-deep = divergent.

---

## 4. The substrate — pooling-state capacity **[SETTLED]**

(Full detail in `substrate_description.md`; essentials here so this doc stands alone. This
is the first deliberate *mechanism* commitment.)

**Soft-tied weight pooling.** Full parameter budget allocated at init; nothing is ever
added or removed. "Capacity" means *resolution*, not parameter count. A group of weights
softly tied toward its own mean acts as one effective weight (low resolution); loosening
the tie lets members diverge (higher resolution). Pooled↔unpooled is a continuous
constraint strength, not a surgical split. This is soft weight-sharing (Nowlan & Hinton)
**with the tie driven by local error instead of a global compression objective** — that
swap is what makes it the project's, not an import.

- **Tie is a penalty, never hard equality.** Hard tying → identical copies forever, no
  differentiation. Soft tying keeps members clustered but lets latent differences express.
- **Fixed nested tree, adaptive depth.** Which weights can split from which is fixed at
  init (e.g. 1→4→16); how far down any branch is currently unpooled is adaptive.
  Envelopes are **concept-agnostic** at init — uniform generic structure; input statistics
  populate them.
- **Heterogeneous depth is normal.** Different branches sit at different resolutions
  simultaneously. **Siblings independent; ancestors gate descendants** (a node unpools
  only if its parent is — depth along any path is monotonic; re-pooling a node collapses
  everything beneath it). Re-pool high = big reclaim; re-pool at a leaf = small. Graceful
  leaf-first detail-shedding falls out of the tree shape.

**Dynamics — two directions, one local signal:**
- **Unpool (capacity opens) — clock-led, NOT error-pulled.** Paced by a maturational
  clock: `rate = base_rate × activity_gate`. **v1: gate pinned to 1** (fixed,
  predictable). Capacity opens *first*; perception of the finer distinction *follows* —
  the system can't detect "I need a distinction I can't yet represent," so growth leads and
  error consumes. (The red-ball realisation lags the capacity, as in real development.)
- **Differentiation of freed members — intra-group gradient disagreement.** Once unpooled,
  members receive their own gradients; if those point apart, experience differentiates them
  (red vs green). This is the *consumption* signal — what freed capacity becomes — **not**
  the unpool trigger.
- **Re-pool (capacity reclaimed) — reversible re-tightening.** Trigger: **sustained low
  intra-group disagreement AND sustained low recent use.** Both required (low disagreement
  alone would re-pool successfully-learned distinctions; use distinguishes
  mastered-and-active from unused). **Reversible tie, not migration** — freed resolution
  stays within its own branch. **Fast-out / slow-in hysteresis** (prevents thrash, protects
  dormant-but-real distinctions). **Graceful** — sheds detail, keeps coarse value; worst
  case is coarsening, never erasure.

**Cross-compat (this is the gap-3 fusion):** the identical pooling law runs in the
**encoder** and in **PAM**, each fed by its native error (JEPA predictor error in the
encoder; convergence error in PAM). Convergence error reaching the encoder *adds to its
gradients* → surfaces as disagreement pressure → **evocation drives encoder differentiation
literally, not metaphorically.** Weight-level is the only unit that is the same object in
both halves (why neuron-level and basin-level were rejected).

**Caps (chosen, not defaulted):**
- **Cap 1 — total parameters.** Fixed budget. Trivial.
- **Cap 2 — per-region ceiling.** The tree is fixed at init, so each region's max
  resolution is frozen *before the system has experience to inform the partition*. Freed
  capacity reuses only within its branch. **Accepted for v1**; cross-branch migration would
  dissolve Cap 2 but is known-messy and deliberately excluded.

---

## 5. Forgetting / decay — three mechanisms, three jobs **[SETTLED in shape]**

Characteristic 6 is served by **three distinct mechanisms** (not one "decay knob" — the
mechanism map confirmed a substrate-independent decay knob is unattested; we stopped
looking for it):

1. **Pooling** — sheds *representation* detail (resolution). Re-pool under sustained low
   disagreement + low use. Coarsens, never erases.
2. **Drift** — representational drift of the space, on a much slower timescale; the **only
   true eraser** (carries a region to eventual inaccessibility).
3. **Downsampling / store eviction** — sheds *temporal* detail and bounds store size.
   Old memory periods compress (many frames → one span-embedding, with extent-as-content);
   rare-and-abandoned entries age out of the store entirely.

Pooling and downsampling are the *same principle* ("shed detail, keep structure") on two
axes — representation and time.

---

## 6. Order, segmentation, replay **[mixed]**

**Order — order-as-content, not order-as-operation [SETTLED].** The mechanism never
*steps through* time. Order lives *in* the stored/evoked structure as content (via
wave-relative position), and the whole thing completes from a partial cue at once. The
discriminator: **random access to an ordered whole = sideways (correct); sequential access
only = forward predictor (drift).** You must be able to cue from the *end* of a practised
sequence and recover its *beginning*.

**Non-causal masking [SETTLED].** PAM learns by masking *interior* spans and reconstructing
from *both* sides. Causal masking (past→future only) would make PAM a forward predictor.
This is the single most important discipline in the recall/learning machinery.

**Within-span vs across-span [SETTLED — critical].** Within a stored span: whole-at-once
surfacing (sideways, no stepping). Across spans: tracing (char 4, confidence-gated,
variable-length, halts when confidence drops). The ball-kick example: the kick is *one
high-confidence span* surfaced whole; "ball flies away" is the **seam** — simultaneously the
segmentation boundary and the trace-halt point, both derived from the same
confidence-collapse.

**Plan-then-execute [SETTLED].** The whole ordered plan is surfaced at once (inspectable,
revisable mid-sequence), then enacted one wave at a time because reality is sequential.
This is *not* forward prediction (which would generate each step from the last). Test: can
you inspect step 7 before enacting step 2?

**Segmentation — confidence-driven boundaries [SETTLED that boundaries are confidence-
driven; the early-development fix is PROPOSED].** Confidence-collapse marks span boundaries
(= event segmentation by prediction error, re-derived). The **storage unit = the recall
extent** (the span is the unit, so recall surfaces the span). **[PROPOSED]:** segmentation
*is* the downsampling-compression cutting at confidence seams — recent memory stays dense
and unsegmented; aging memory compresses predictable interiors and preserves surprising
boundaries as seams. This resolves the early-development problem (when prediction is poor,
nothing is confident enough to compress, so memory stays dense — which is fine because it's
recent).

**Replay [SETTLED in shape]:**
- **Awake replay** — situation-cued associative recall (the current bundle cues the store).
  No separate scheduler; the present pulls. In scope, normal operation.
- **Sleep consolidation** — offline, broad, varied, possibly externally guided (LLM/larger
  agent). The **one legitimate phase** (sleep *is* a phase biologically). **[DEFERRED]** to
  much later.
- **Online-interleaved, never offline batch** during awake operation (preserves char 7).

**Pollution = priming [SETTLED reframe].** Replayed memory re-entering perception was
feared as contamination; it is *also* the mechanism characteristic 11 (priming) requires.
Resolved by **vividness-attenuation** (replay enters the same port as perception but
fainter, so it biases rather than asserts) **+ learned attendance** (PAM learns how much to
weight the replay channel by whether attending paid off). The vividness gradient does
double duty: it is the reality signal (faded = remembered, vivid = real — matches the
introspective "memory is less vivid unless meditative") *and* the creativity knob.

---

## 7. What changed this lineage (so it isn't re-opened)

- **The "routing layer" dissolved.** It was never *dispatch* (characteristic 10 forbids
  anything that knows which slice goes where). Its fusion/translation work **is PAM's
  encoder/decoder.** Three paths remain: passive write (to store), encode (in), decode
  (out). There is no separate router component.
- **Consequence — stability reference relocated.** There is no "frozen router" scaffold to
  develop against. The stabilising reference for PAM's development is the **externally-
  stabilised cortex spaces** (anchored by the word/parent cortex). Don't carry a phantom
  frozen-router.
- **Encode/decode are a co-developing matched pair** (autoencoder-shaped: decode must
  invert encode well enough to round-trip). Each is the other's reference — reference-and-
  relaxation operating *inside* PAM, not just around it.
- **The store is separate but format-identical-via-decode**, not a sequence PAM "sees
  over." Framing-1 (store + overseer = forward predictor in disguise) is rejected;
  framing-2 (associations are the structure) is the thesis. The store is the bridge from
  one-shot/rare experience to slow weight-consolidation: frequent → lives in weights (store
  entry redundant); rare-but-recurring → store feeds it until weights take over;
  rare-and-abandoned → ages out of both.
- **JEPA commitment scoped:** yes for the *cortices* (the conservative choice — de-risk the
  periphery, concentrate novelty at the centre); **architecture not protocol** (online from
  init, no pretraining phase); **small-and-growing, not big-and-pretrained** (the ViT
  weights are the soft-tied pool). The **association cortex (PAM) is not a frozen JEPA**.
  Motor cortices: action-as-prediction is plausible (active inference) but not proven —
  flagged.

---

## 8. Logged from the latest mechanism map (confirmations + three additions)

The map mostly **confirms** rather than redirects. Trust its tension map and `[CONFIRMED]`
items (the 6+8+10 triad as a real gap; the two-hub split; the major tensions). Treat its
*recommendations* and staged build with caution — they lean conservative (lead with a
shared space, defer drift = trade away the novel part first).

Three additions worth carrying:
1. **Resonator networks (Frady, Kent & Olshausen 2020)** — the named mechanism for
   recovering each cortex's slice from one superposed bundle. Fills the previously-blank
   "how does a cortex extract its slice from the broadcast" step (char-10 consumption).
2. **VSA bundling/binding (Plate, Kanerva, Gayler)** — the *principled* version of the
   fusion we did cheaply with pooled concatenation: order-agnostic and own-space by
   construction. Fallback if fixed-slot concatenation ever chafes (esp. if the cortex count
   needs to be genuinely open). **Coupling to watch:** how you fuse *in* determines whether
   you can cleanly factor *out* — pooled concatenation fuses simply but may not factor
   cleanly under drift; VSA role-binding does both by construction. Could revise the fusion
   choice once there are >2 cortices under drift.
3. **Silent-swap / Dreamer warning** — the canonical drift for tracing: bolting a
   value/planner model on to extend horizon. Named tripwire (see HANDOFF live-vector 3).

Plus a **new foundational gap** the map surfaces: **asynchronous cortex rates vs a fixed
central wave** — no surveyed mechanism sets wave duration relative to per-channel rates
(the resampling/aliasing problem). This validates designing the frame≠wave mismatch in from
the start; it raises the priority of the wave↔rate interface for a future session.

---

## 9. Open questions / gaps (prioritised)

**Block even a minimal build:**
- **Initialisation (Fork A, never closed).** The *minimum dense structure* PAM and the
  visual encoder start with so the loop's error is meaningful from wave 1. Word-encoder is
  pretrained-stable; visual seed is "temporally-smooth summaries"; convergence gain ramps
  from 0 — but the concrete t=0 state isn't pinned.
- **PAM's masked-completion objective, concretely.** The *shape* is set (non-causal masked
  completion over the bundle stream, online); the *actual loss* — what's masked, what's
  predicted, the per-wave gradient — isn't written.
- **v0 component count.** Whether v0 runs with PAM's distinct latent (full encode/decode)
  or even simpler (PAM operating directly on concatenated cortex output, distinct latent
  added when it earns its place).

**Build on the foundation (deferred, with triggers):**
- **Wave↔cortex-rate aliasing** — what sets wave duration vs per-channel rates. Re-entry:
  when adding a cortex whose rate differs sharply (audio at 100–500× compression).
- **Within-bundle variable confidence** (ball vs players in one frame) — **[DEFERRED]**,
  downstream of object differentiation. Re-entry trigger: when the visual cortex begins
  emitting separable entity-structure (multiple objects per scene).
- **Span boundary specifics** — fixed-length vs surprise-segmented (leaning the latter via
  §6 PROPOSED).
- **Similarity-vs-association hop selection** — **[PROPOSED]** highest-confidence-wins.
- **Re-pool use-window length** — the one genuinely empirical knob; long default, found by
  observation, not derived.
- **Motor / agency, reward / salience / affect** — out of scope by design; must not be
  *foreclosed* (the core operation must remain extensible toward priming and surfacing-for-
  arbitration).
- **Sleep consolidation** — deferred to much later.

---

## 10. Suggested MVP (Stage 0)

**Goal:** the smallest system that runs the one operation end-to-end and lets the deferred
questions become observable. Not the full architecture — a foundation the rest builds on.

### Scope
- **Two cortices: vision + word.** Word encoder pretrained and stable (the parent/anchor).
  Vision encoder JEPA-pattern, small, online, soft-tied pooled weights.
- **PAM**: encode (fuse) → non-causal masked completion in latent → decode (broadcast).
- **No store.** Stage 0 is PAM-weights-only. (The store, tracing, segmentation, replay,
  vividness/creativity, within-bundle association are all **Stage 1+**.)
- **Pooling substrate** with `activity_gate` pinned to 1 (fixed maturation rate) — every v1
  channel is active anyway, so the gate is dormant-but-present.
- **Single visual scene + word channel** — the environment where within-bundle variable
  confidence barely fires, so whole-bundle binding is correct rather than a stopgap.

### The three decisions Stage 0 must make first (currently open — resolve in the build chat)
1. **Initialisation / t=0 state.** The minimum dense structure for vision-encoder and PAM
   such that wave-1 error is meaningful. (Fork A.)
2. **PAM's per-wave loss.** Concretely: what is masked, what is predicted, what the gradient
   is — as non-causal masked completion over the fused bundle, online, no train/run split.
3. **v0 component count.** Distinct PAM latent (full encode/decode) from the start, or PAM
   directly over concatenated cortex output with the latent added later. Decide consciously
   — it sets how much is built first.

### What "working" looks like at Stage 0 (success signals)
- The loop runs every wave with no train/run phase (char 7 holds in code, not just on
  paper).
- Convergence error meaningfully shapes the vision encoder (gap-3 fusion observable:
  evocation pressure shows up as encoder differentiation).
- Pooling visibly does *something* — a coarse association differentiating as capacity opens,
  under a fixed maturation rate.
- The word/parent anchor demonstrably stabilises co-development (removing/degrading it
  destabilises, confirming the reference role).

### What Stage 0 deliberately does NOT test
Tracing, multi-step reach, the store and one-shot/rare-experience recall, segmentation,
replay, vividness/creativity, within-bundle association, async cortex rates, motor, reward.
Each has a re-entry trigger in §9. Resist building toward them — the point of Stage 0 is the
foundation they require.

### The discipline to hold during the build (from HANDOFF)
- **Non-causal masking** (or PAM becomes a forward predictor).
- **No store-as-overseer** (the store is Stage 1 and passive anyway).
- **Efficiency emergent, never an objective.**
- **Pinned constants are pins, not stand-ins** — build the real mechanism, pin the variable
  part, release later.
- **Test against the twelve functions, not vocabulary**, as the mechanism hardens.
