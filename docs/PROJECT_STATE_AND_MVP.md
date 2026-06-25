# Project State & MVP — Associative-Memory System (Weft / PAM)

**What this is.** The complete current state of the architecture: every decision, where
it stands (settled / proposed / deferred), the open gaps, and a suggested MVP. Written to
be self-contained — the base for a new chat to develop the MVP. Companion: `HANDOFF.md`
(how to work), `substrate_description.md` (substrate detail), the twelve-characteristic
spec (stable), the mechanism map (possibility space), `progress_log.md` (append-only
history of what happened when).

> **Validation status (see §9):** three standalone mechanism rigs are now run and green —
> the pooling substrate (real risk, validated), non-causal masked completion (lower risk,
> toy-validated), and order-as-content (exp03 — the novel claim, isolation-confirmed). They
> produced three forward design rules that refine the sections below; those rules are marked
> inline and consolidated in §9. The four §11 Stage-0 build-blockers are now resolved in design.

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
  - The anchor is also the **structural half of collapse-control** (see §11): being a *fixed*
    target, it guarantees target-diversity on word-as-target maskings and so removes
    representational collapse as a global optimum **without** any stop-gradient — the
    non-moving-target role that stop-grad usually plays, supplied by the parent being fixed.
    (Kinetic half = a SIGReg-style spread constraint on vision; §11.)

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

## 4. The substrate — pooling-state capacity **[SETTLED · empirically validated, exp01]**

(Full detail in `substrate_description.md`; essentials here so this doc stands alone. This
is the first deliberate *mechanism* commitment. **Validated in isolation — Experiment 01
(§9); the genuinely uncertain bet, and it held.**)

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
  *Design rule from exp01 (§9): when λ becomes adaptive post-v1, it must scale with local
  signal strength to hold the unpool break-through threshold constant — otherwise a strong
  differentiation gradient breaks through the tie and the clock stops being the consistent
  pacer.*
- **Differentiation of freed members — intra-group gradient disagreement.** Once unpooled,
  members receive their own gradients; if those point apart, experience differentiates them
  (red vs green). This is the *consumption* signal — what freed capacity becomes — **not**
  the unpool trigger.
- **Re-pool (capacity reclaimed) — reversible re-tightening.** Trigger: **sustained low
  pull-apart force AND sustained low recent use.** Both required (low force alone would
  re-pool successfully-learned distinctions; use distinguishes mastered-and-active from
  unused). *Trigger is force **magnitude**, not gradient cosine — exp01 (§9): cosine is
  ill-defined as gradients vanish; cosine is a useful diagnostic of whether members want
  to differentiate, but magnitude is what drives re-pool.* **Reversible tie, not
  migration** — freed resolution stays within its own branch. **Fast-out / slow-in
  hysteresis** (prevents thrash, protects dormant-but-real distinctions). **Graceful** —
  sheds detail, keeps coarse value; worst case is coarsening, never erasure.

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
   pull-apart force + low use (force magnitude, per exp01 §9). Coarsens, never erases.
2. **Drift** — representational drift of the space, on a much slower timescale; the **only
   true eraser** (carries a region to eventual inaccessibility).
3. **Downsampling / store eviction** — sheds *temporal* detail and bounds store size.
   Old memory periods compress (many frames → one span-embedding, with extent-as-content);
   rare-and-abandoned entries age out of the store entirely.

Pooling and downsampling are the *same principle* ("shed detail, keep structure") on two
axes — representation and time.

---

## 6. Order, segmentation, replay **[mixed]**

**Order — order-as-content, not order-as-operation [SETTLED; isolation-confirmed (exp03)].**
The mechanism never *steps through* time. Order lives *in* the stored/evoked structure as
content (via wave-relative position), and the whole thing completes from a partial cue at once.
The discriminator: **random access to an ordered whole = sideways (correct); sequential access
only = forward predictor (drift).** You must be able to cue from the *end* of a practised
sequence and recover its *beginning*.

> exp03 removed exp02's explicit-index crutch and validated order-as-content **in isolation**:
> position carried by genuine σ>0 OU drift, **entangled** with content (α=1) and **shuffled**,
> still supports random access (cue-end → recover-begin) at the faithful **high-σ ∧ high-α**
> corner. **Scope:** confirmed with *fixed generators and a single completion operator*; **not**
> validated under co-developing encoders + pooling + convergence-drift (that is the MVP). Residue:
> the operator is a within-window comparator with **residual scale-sensitivity** — the deployed
> drift has no controlled scale, so the MVP must re-examine it. (Detail: §9, `progress_log.md`.)

**Non-causal masking [SETTLED · toy-validated, exp02].** PAM learns by masking *interior*
spans and reconstructing from *both* sides. Causal masking (past→future only) would make
PAM a forward predictor. This is the single most important discipline in the recall/learning
machinery. **Validated in the toy setting — Experiment 02 (§9): non-causal recovers the
beginning from the end in one pass (1.000); the causal control cannot, by construction
(0.062 = chance). Caveat: toy setting uses explicit position indices, so this validates the
masked-LM property, NOT order-as-content (which waits for the PAM-setting test).**

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

## 8. Logged from the latest mechanism map (confirmations + four additions)

The map mostly **confirms** rather than redirects. Trust its tension map and `[CONFIRMED]`
items (the 6+8+10 triad as a real gap; the two-hub split; the major tensions). Treat its
*recommendations* and staged build with caution — they lean conservative (lead with a
shared space, defer drift = trade away the novel part first).

Four additions worth carrying:
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
4. **SIGReg / LeJEPA (Balestriero & LeCun, Nov 2025)** — distributional-spread collapse-control
   (characteristic-function matching to an isotropic Gaussian over random projections) that uses
   **no stop-gradient and no EMA**. This is the collapse-control class adopted for the vision
   encoder (§11), chosen *because* it doesn't stop-grad the target and so preserves the gap-3
   gradient path. **Corrected provenance:** it is LeJEPA's, not V-JEPA 2's; and it is distinct
   from the registers line (Darcet et al.). "Target diversity ⇒ no collapsed global optimum" is a
   2026 VJEPA-variant theorem, the formal backing for the word-anchor's structural collapse role.
   Caveat: Nov 2025–Mar 2026 sources, quantitative claims provisional; the *class* is multiply
   reproduced.

Plus a **new foundational gap** the map surfaces: **asynchronous cortex rates vs a fixed
central wave** — no surveyed mechanism sets wave duration relative to per-channel rates
(the resampling/aliasing problem). This validates designing the frame≠wave mismatch in from
the start; it raises the priority of the wave↔rate interface for a future session.

---

## 9. Empirical validation & findings to date

Three standalone mechanism rigs run — all green, all pushed to the repo. Detailed results in
`progress_log.md` and each experiment's `RESULTS.md`. These move three design bets from
"designed" to "validated in isolation," and surfaced three forward design rules (marked
inline above) plus one readout constraint.

**Experiment 01 — Pooling substrate. [VALIDATED — real risk].** Soft-tied weight pooling
genuinely opens (unpool) and reclaims (re-pool) resolution under local signals; robust across
the full `r_fine/σ` sweep, degrading only as the task itself becomes unlearnable, not as the
substrate fails. Gradual unpool pays no accuracy cost vs always-unpooled (0.96 vs 0.95);
always-pooled caps near chance for the fine distinction (0.30). All four claims passed
pre-registered conditions. The rig caught a validity bug in its own spec first (a free linear
head leaks the fine distinction through pooled weights → switched to nearest-prototype
readout). **This was the genuinely uncertain bet; it held.**

**Experiment 02 — Non-causal masked completion. [VALIDATED in toy setting — lower risk].**
Non-causal completion gives random-access fill-in (cue the end → reconstruct the beginning,
single pass = 1.000); the causal/forward control fails by construction (0.062 = chance). The
random-access sweep (causal whole-recon decaying 1.0→0.21 as the cue moves rightward,
non-causal flat-high) is the clearest anti-drift artifact to date. **Confirms "sideways, not
forward" — but only the *toy* property under explicit position indices.** The at-risk version
(order-as-content in a learned latent over bundles, under drift) is **not** validated; it
waits for the PAM-setting test.

**Experiment 03 — Order-as-content. [VALIDATED in isolation — the novel claim].** Removed
exp02's explicit-index crutch and tested whether position carried by a **drifting, shuffled,
entangled** signal still supports random access. **PASS** on all pre-registered conditions
(F1 array-axis, F2 index-in-costume, F3 not-at-once, F4 separability-dependence) plus Control A
and a carrier-ablation gate. The **faithful corner** (high-σ ∧ high-α — the regime closest to
the deployed mechanism) was verified **directly** by a stacked-corner re-run: at σ=0.8, α=1,
operator begin-recon 0.821, an independent (weaker, fixed) MLP probe 0.848 ≈ oracle 0.847, and a
fixed OLS probe 0.681 < oracle — the OLS-below-oracle gap is the tell that the corner is
**genuinely entangled** (a pure linear read is confounded) while the operator reaches the
disentangling ceiling. 3-seed. The rig **caught its own vacuous F4 near-pass** (drift injected on
a content-free axis → R²=0.994 → re-injected on the codebook's top PC → R²=0.80), a concrete
instance of the "green for the wrong reason" risk caught by adversarial review. **Licenses**
proceeding to Stage 0 with order-as-content; **does not** validate it in the loop.

**Three forward design rules these produced (carry into the build):**
1. **Re-pool trigger = pull-apart force magnitude, NOT gradient cosine** (exp01). Cosine is
   ill-defined as gradients vanish; magnitude is well-defined and is what should drive
   re-pool. Cosine remains a diagnostic. *(Already applied to §4/§5.)*
2. **Adaptive-λ scales with local signal strength** (exp01). Fixed λ lets a strong
   differentiation gradient break through the tie, drifting the clock-vs-error balance with
   signal magnitude. Post-v1 adaptive λ must scale with signal strength to hold the break-
   through threshold constant, keeping the clock the consistent pacer. *(Applied to §4.)*
3. **PAM's completion objective must sample the full cue-shape distribution** (exp02).
   Masked completion trained only on dense, centered masking learns gap-*filling*, not random
   access. Random access requires training on the full range of cue-shapes — sparse,
   one-sided, endpoint-only — or recall lacks the property, discovered late. *(Constrains §10
   blocker 2.)*

**One readout constraint confirmed (exp01).** A free linear readout leaks fine distinctions
through shared pooled weights, breaking the capacity-tracks-pooling property. Readouts must be
distance/similarity-based (nearest-prototype) — which also matches the architecture's own
commitment (concepts = regions completed by similarity, not linear boundaries). Bears on how
PAM's readout and any cortex heads are built.

**Experiment 04 — Stage-0 MVP (Phase-1 core). [BUILT — first integration; gap-3 PRESENT
(gradient path alive), not yet cleanly isolated].** The first fusion of the three rigs in one
loop — vision pooling cortex + frozen word cortex + a non-causal **prototype-resonance**
associator (no softmax-attention) — in `experiments/04_stage0_mvp/`, built from
`STAGE0_MVP_SPEC.md`. **The headline result is the gradient-attribution split:** PAM's
convergence error reaches the masked vision slot with **no detach** — `vision_grad_from_PAM` is
**nonzero every eval window** (gap-3 is wired and active), with magnitude **order-1 (comparable
to JEPA), seed/time-variable** (cross-seed mean ratio ≈ 0.8×; rises in late windows; *not*
robustly dominant). **Build-correctness verified every eval window:** word anchor frozen
(param-delta = 0); no detach (vision-from-PAM and -JEPA both nonzero); block-level whole-slice
masking over all **six** cue-shape families; **no softmax-attention**; order-as-content not
order-as-index (live carrier max single-coordinate R² < 0.9 every window); one code path
(char-7). **Phase-1 readouts (3-seed `--quick`):** **Readout D = PASS-LINEAR-REGIME (a qualified
pass, NOT a clean PASS)** — order *is* recovered in-loop and carrier-zero collapses it (real),
**but `full_ols_r2 ≈ 1.0 ≥ 0.9`**: a full linear read recovers the drift, so this validates
order-**in-loop**, not the *entangled* order-as-content corner (exp03 hit 0.80 at α=1). Cause:
the dwell-stable fix froze A/B within a dwell, leaving drift as the only within-window variation
→ linearly separable; the **entangled corner is DEFERRED** (carrier-zero collapse is
necessary-but-not-sufficient; `full_ols_r2` is the tell). Both **structural signals PASS**
(capacity opens ~8–14× from pooled; char-7 holds). **Readout G is seed-unstable / WRONG_REASON**
— B rises but the matched **no-word arm also rises** (genuine *autonomous* B-resolution from the
visual input + JEPA; **leak ruled out** — null token is B-agnostic, schedules independent, stream
matched), so the Stage-3 discipline flags it rather than declaring a false PASS. Phase 2 (Readout
A ladders), the gain-rate sweep, and Readout O are deferred per the spec's Phase 1 → Phase 2 staging.

**What this leaves:** all three *standalone-testable* mechanism bets are tested
(order-as-content **isolation-confirmed**, exp03) and the **first integration is now built**
(exp04) — **gap-3 is present (the gradient path is alive)** and the build-correctness invariants
all hold. What is *not* yet clean: **(a)** cleanly **isolating** gap-3 from autonomous resolution
(Readout G — suppress autonomous B-resolution so the no-word arm stays in the floor-band); **(b)**
the **entangled** order-as-content corner in-loop (Readout D is currently the linearly-separable
regime). Order is recovered in-loop; the entangled corner and the clean gap-3 isolation are the
next frontier, then Phase 2 (collapse-control asymmetry) and the gain sweep.

---

## 10. Open questions / gaps (prioritised)

**Block even a minimal build:** *All three former Stage-0 build-blockers are now resolved in
design — see §11. Briefly:*
- **Initialisation [RESOLVED].** Vision starts **near-fully-pooled but converged at that depth**
  (a working coarse encoder) → a stable coarse target for PAM with no cold-start, no stationarity
  crutch. Word encoder pretrained; drift carrier starts at σ>0; gain ramps from 0.
- **PAM's per-wave loss [RESOLVED in shape].** Non-causal masked completion over a **W≥3** window
  of concatenated bundles; distance-based loss on masked cells only; **full cue-shape distribution**
  sampled across time (the exp02 constraint); gradient into **both** encoders (no stop-grad). §11.
- **Component count [RESOLVED: latent OUT].** PAM runs directly on **concatenated cortex output**
  for Stage 0; distinct latent deferred to Stage 1+ (it buys only char-10 blindness + a codec, a
  second co-dev pair with no store to serve). §11.

**Build on the foundation (deferred, with triggers):**
- **Cross-cortex completion from impoverished cues [DEFERRED].** Completion must be able to fill a
  gap spanning multiple/all cortices from accumulated structure (weights + store), not from a
  co-present cue slot — the same capability **char 11 (priming)** requires. Stage 0's clean-cue
  environment brackets it, and **must not design it out**: the loss's full cue-shape sampling
  (sparse / one-sided / near-all) keeps it structurally available. Two halves on different clocks —
  **fill-from-weights** is incidentally live at Stage 0 (an all-masked two-cortex bundle has no
  co-present slot, so it completes from weights or not at all); **fill-from-store** is Stage 1+.
  Re-entry: when the store enters, or when the environment first produces impoverished bundles
  (occlusion, missing channel).
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

## 11. Suggested MVP (Stage 0)

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

### Stage-0 build decisions — RESOLVED

All four former build-blockers are now **resolved in design** — the Stage-0 MVP is fully
specifiable. Their **validation is the MVP run itself** (loop-level claims, not isolation-
testable per §9); subsections below marked **[SETTLED in design; MVP-validated]** are fixed in
design but only the loop can confirm them.

> **1. Initialisation / t=0 [RESOLVED].** Vision encoder starts **near-fully-pooled but converged
> at that depth** — a functioning coarse vision system (colours/blobs) that reliably emits the
> same embedding for the same input. This is the *stable coarse target* PAM associates against:
> stable because **converged**, not frozen (the space still drifts as it unpools — no char-8
> crutch), and there is **no cold-start wobble** because the coarse system finishes settling
> before PAM begins. Word encoder pretrained-stable; drift carrier starts its OU at σ>0; gain
> ramps from 0; PAM cold-starts off structured inputs (needs only sane scale).
>
> **2. PAM's per-wave loss [RESOLVED in shape].** (wave, slot) cells over a **W≥3** window of
> concatenated bundles. Each wave: slide one, draw a mask from the **full cue-shape distribution**
> {single-slot, whole-wave, interior-both-sides, one-sided-edge, sparse, near-all}, one completion
> pass, one gradient step — sampled **across time** (this is what makes it online / phase-free).
> Target = the **actual emitted content** of masked cells (self-supervised) = convergence error.
> Loss = **distance on masked cells only** (no free linear head). "Non-causal" is vacuous within a
> wave (char 1) and therefore **forces W≥3** across waves; within-wave completion (char 2) is the
> single-wave sub-case, across-wave (char 3) is the point — **Stage 0 is the PAM-setting test exp02
> deferred**. Operator internal form stays **open** (not a masked transformer); evaluate a
> **single** completion act (exp02 at-once).
>
> **3. Component count [RESOLVED: latent OUT].** PAM runs masked completion **directly on
> concatenated cortex-space**; the distinct PAM latent is **deferred to Stage 1+**. gap-3 does not
> need a latent (masking a slot and evoking from the sibling, backprop through concat into the
> encoders, carries the joint-association pressure either way); concatenation already preserves
> **own-space** and defers only blindness, which Stage 0 doesn't test; the codec would be a second
> co-dev pair whose decode serves a store that doesn't exist yet. Honest deferral, not a violation.

### Collapse-control [SETTLED in design; MVP-validated]

**No stop-gradient.** Standard collapse-control stop-grads the target, but gap-3's differentiation
pressure **is** the target-side gradient on the masked vision slot — stop-grad would sever the
path Stage 0 observes. Decompose by reference-and-relaxation: **anchor (structural)** — the fixed
word encoder guarantees target-diversity on word-as-target maskings, removing collapse as a global
optimum without cutting gradient; **SIGReg-style spread on vision (kinetic)** — keeps the vision
marginal diverse on vision-as-target maskings and repels early collapse, without stop-grad. Net:
**drop stop-grad, keep an active spread term.** **Attribution watch:** spread (→ isotropic) and
pooling differentiation (→ tight clusters) act on the same vision outputs — if differentiation
underperforms, interpose a **projector** (spread on a throwaway head, pooling on the backbone
summary). (SIGReg/LeJEPA: §8.)

### Gain ramp [SETTLED in design; swept in run 1]

Build gain **confidence-gatable AND capacity-boundable** in structure; **pin both OFF for run 1**
(pure fixed ramp) and **sweep the rate** — the deliverable is the **response curve**, not a tuned
value. Rationale: unresolved contrast is **not inert** — its gradient lands on the coarse weights
= corruption pressure on the seeded coarse target — so the binding constraint is on **gain** (press
vs current capacity), not the curriculum. **Capacity-gating** (not confidence-gating) is the safer
**release** gate (confidence rises exactly when capacity is absent and the push is dangerous). Bound
out of run 1 because it is moot by construction (slow ramp + first-order unpool), adds attribution-
breaking coupling, and is caught by the readout anyway.

### Stimulation curriculum — external loop [Stage-0 component]

Stage 0's impoverished environment needs a hand-supplied **parent**: read system confidence, add
the next **contrast** word when a vision/word pairing goes confident. **External, not a PAM
mechanism** (preserves no-external-objective). **Contrast-not-rename:** a new word with no
contrasting pair present = a consistent gradient = a rename, no split; differentiation needs the
contrast present in experience (cricket-ball vs not-cricket-ball, both labeled). This is the
external face of the cue-shape / gap-3 mechanism already in the loss.

### Three rates — keep separate

**(1) unpool clock** (capacity; the only deployed rate; maturational) · **(2) gain ramp** (how
hard evocation presses; pinned-swept run 1, capacity-bound release; attribution-control) ·
**(3) curriculum rate** (when the parent adds contrast; confidence-triggered; environment). They
are different clocks with different owners; do not let them blur.

### What "working" looks like at Stage 0 (success signals)
- **Char 7 holds in code** — the loop runs every wave with no train/run phase.
- **gap-3 fusion observable**, read via the **split signal**: vision differentiating a
  **word-relevant** axis = gap-3 working; vision differentiating a **visually-salient** axis with
  the **word present and contrast available** = **gap-3 FAIL** (wrong teacher); the same salience
  while the **word is still pending** = **normal**, and the **curriculum's cue to advance the word
  side** (not a fault). The naive "salience = broken" reading throws false failures.
- **Pooling visibly does something** — a coarse association differentiating as capacity opens
  under the fixed maturation rate.
- **Anchor stabilises co-development**, tested as the **asymmetric falsification**: degrading the
  anchor must collapse the **word-as-target half specifically** — collapses-everything or
  collapses-nothing both falsify the collapse-control decomposition. (This *is* the
  collapse-control test; one experiment serves both.)

### What Stage 0 deliberately does NOT test
Tracing, multi-step reach, the store and one-shot/rare-experience recall, segmentation,
replay, vividness/creativity, within-bundle association, async cortex rates, motor, reward.
Each has a re-entry trigger in §10. Resist building toward them — the point of Stage 0 is the
foundation they require.

### The discipline to hold during the build (from HANDOFF)
- **Non-causal masking** (or PAM becomes a forward predictor).
- **No store-as-overseer** (the store is Stage 1 and passive anyway).
- **Efficiency emergent, never an objective.**
- **Pinned constants are pins, not stand-ins** — build the real mechanism, pin the variable
  part, release later.
- **Test against the twelve functions, not vocabulary**, as the mechanism hardens.

---

## 12. Addendum (2026-06-25) — Post-Phase-1: gap-3 developmental shape, slow-start unpool, characterisation sweep

**Context.** Phase-1 core is built, green, committed (a94863e). gap-3 is present (`vision_grad_from_PAM` > 0 every window, order-1 / comparable to JEPA — *not* robustly dominant). Readout G is seed-unstable/WRONG_REASON (clean isolation is the open part); Readout D is PASS-LINEAR-REGIME (entangled corner deferred). This addendum records what the post-Phase-1 read changed. Two items are **settled design**; the third is **next-session design, open** — kept separate so the doc does not pre-commit the knob choice.

---

### A. The gap-3 developmental shape is an S-curve [HYPOTHESIS — to be characterised, not assumed]

The working model for how PAM's pressure shapes vision over development:

- **Toe (single-association).** Vision starts as a viable coarse encoder with good confidence in what it perceives. Unpooling begins; words start matching distinctive properties, but each is a *single* word↔blob association with little cross-concept benefit. "ball" must be learned before "green ball" / "red ball" can split from it. gap-3 pressure is expected **low-ish here even as words land** — there is no associative scaffolding to build on yet. *(The order-1 PAM/JEPA gradient ratio observed at Phase-1 is consistent with sitting in the toe — not yet evidence either way.)*
- **Rapid phase (concepts build on concepts).** Once base associations are down, new concepts form quickly because they build on prior ones; unpooling proceeds at a reasonable rate. **If the paradigm bet (evocation-as-teacher) is right, PAM's gradient share should rise above JEPA's here.** This rise — or its absence — is the real test of whether gap-3 is strong enough to be the teacher the paradigm needs.
- **Plateau (fully unpooled).** Fine distinctions take many exposures; growth-rate falls. The driver shifts from raw unpooling to re-pool/unpool *efficiency* cycling. Stage-0 short runs will not reach here, but the metric should be able to see the rate roll over if a run is long enough.

**Status.** This is a hypothesis about the *shape*, to be drawn by instrumentation (§C), not a target to land. The deliverable is the curve; a clean Readout-G window is one point on it, not the goal.

---

### B. Slow-start unpool ramp [SETTLED in design — architecture addition]

**The unpool clock should ramp slow→fast, not run at constant rate.** Constant-rate is acceptable *only* for the short Stage-0 tests (and stays pinned constant for them). In principle it is wrong: **words must stabilise against what the vision encoder already sees before unpooling splits the blobs** — otherwise the split happens against an unsettled target.

This is **reference-and-relaxation** again, applied to the unpool clock: the word-anchor is the slow reference; unpooling (the fast learner) must not outrun it early. Same *shape* as the gain ramp (already pinned-from-zero): stiff/slow at first, releasing as word↔blob associations settle.

- **Implementation face — build-full / pin-to-constant / release.** Build the ramp in full; **pin it constant for the short Stage-0 runs** (no behavioural change now); release it when runs get long enough to need it. No debt — the constant case is a special case of the ramp.
- **Discipline note — this is principled pacing, NOT gating.** Slowing the clock so the reference can settle is legitimate; it does **not** gate vision from learning B. It is distinct from (and must not become) the manufacturing-the-effect failure the next session's knob choice guards against. Pacing the clock against its reference ≠ constraining vision into the answer.

This supersedes the §4 "unpool clock — clock-led, v1 gate pinned to 1" note *only in principle* (the ramp is now the designed form); the **pinned-constant behaviour for Stage-0 runs is unchanged**.

---

### C. Characterisation sweep [NEXT SESSION — design open; do NOT pre-commit here]

The next step is **not** "make Readout G go clean." It is **characterise the curve** and let the run draw the shape. Reasoning has reached the point where it predicts less than measurement does — both open knobs are now "try it and see," instrumented.

**Shape of the next-session work (to be finalised in a fresh design chat, then handed to CC):**

1. **Coarse sweep, both knobs together** — band (`r_fine`↓ / `sigma_stim`↑) × unpool-rate — **instrumented to log the PAM-grad / JEPA-grad share across the trajectory, not at a checkpoint.** Deliverable is the **response surface / curve**, not a PASS (exactly how the gain ramp was handled — the surface *is* the result).
2. **Read three things off it:** (a) does a clean Readout-G window open anywhere on the surface; (b) does PAM-grad share rise through the rapid phase (the paradigm test); (c) does the curve show the S-shape at all, or something else.
3. **Lightweight pre-registration before running** — name the expected shape loosely ("PAM-grad share rises in the rapid phase"; "clean window opens at deeper bands") so the characterisation stays a *measurement* and does not slide into reading shapes into noise after the fact. exp03's rigour was the pre-registered failure condition; a sweep deserves the same lightweight version. Not a heavy gate — just name the expected shape so the run can surprise you.

**Knob-choice guardrail (carried from the prior session, still binding).** The band/clock work must be **re-calibration of the existing regime** — never a mechanism that gates vision from learning B except via the word (that manufactures gap-3 = wrong-reason). **Discriminator, written in:** the no-word capacity-open oracle must still recover B (representable, just not *acquired*) — no gate, no stop-grad. The slow-start ramp (B) passes this discriminator by construction (it paces the clock; it does not touch representability).

---

### D. Standing debt (carried forward, unchanged)

**Readout-D linearly-separable regime.** `full_ols_r2 ≈ 0.9999` — order recovered in-loop but in the linear-index regime, not exp03's entangled corner (~0.80). Caused by the dwell-stable fix removing exp03's along-`u` content variation. **Re-test the entangled corner (`full_ols_r2 < 0.9`) the moment within-window content drift returns** — it resolves for free when the deployed space genuinely moves. The band/clock sweep is a Readout-G change and **does not discharge this**.
