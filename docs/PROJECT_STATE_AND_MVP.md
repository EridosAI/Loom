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

**Experiment 04 — Stage-0 characterisation sweep. [RESULT — pre-registered EMPTY-GAP; gap-3 wired
but inert for acquisition].** The post-Phase-1 sweep built from `STAGE0_CHARACTERISATION_SWEEP_SPEC.md`
(`experiments/04_stage0_mvp/{oracle_probe,calibrate_step0,band_ladder,run_sweep,sweep_metrics,analyze_sweep}.py`;
**480 runs** = 12 bands × 2 rates × 20 seeds; commit `2b70d74`, `spec_hash d1f0936c92e1`; full read in
`SWEEP_RESULTS.md`, surface in `figures/response_surface.png`).

- **Verdict — EMPTY-GAP, not F1–F4, not a rig failure.** No clean Readout-G window opens at any cell
  (`cleanG_frequency = 0.00` everywhere). The decisive, **calibration-independent** measurement is the
  gap-3 **lift** `= intact_B_res − noword_B_acq ≈ 0` across all 24 cells (range −0.004 … +0.048, mean
  ~0.01, per-cell SE ≈ 0.013, **no consistent cross-rate sign**): the word-present and no-word arms
  decline in lockstep as the band hardens and never separate. **Not F2** — autonomous resolution
  genuinely *falls* 1.00 → 0.00 (transition r/σ ≈ 4–5); there IS a regime where vision cannot resolve
  B autonomously.
- **Not F3 — B is representable (the load-bearing sentence the oracle/raw separation was built to
  license).** The substrate oracle confirms B is **representable across the whole admissible ladder**
  (oracle ≥ threshold 0.4375; the F3 cap sits just below at r/σ ≈ 1.0). The failure is therefore
  **"the word does not teach a representable B," not "B is unrepresentable"** — this is exactly what
  distinguishes the clean negative from manufactured-gap-3.
- **Methodological finding (the most reusable lesson — must not be lost).** PAM-grad **share** *does*
  rise through the rapid phase (`s_curve_signature_frequency` 0.80–1.00 at every band) — but it is
  **non-discriminating**: identical at easy bands where the word is *provably inert* (lift = 0,
  autonomous resolution does everything). The rise is a real phenomenon **and a false success signal.**
  Naive trajectory-only (share-only) instrumentation would have reported this surface as a
  paradigm-positive S-curve. **Acquisition lift is the load-bearing metric, and it is null.**
- **Mechanistic reading.** gap-3 is **wired** (Phase-1: convergence-error gradient reaches the masked
  vision slot; sweep: `pam_grad_share` ≈ 0.6, rising in rapid) but **inert for acquisition** — the
  gradient arrives at vision and does not drive B-differentiation. Sharpens Phase-1's
  "present-but-weak / WRONG_REASON" into a clean negative across the full band × rate surface.
- **Scope (both halves).** The negative is precise to the **Stage-0 operating point** — two cortices,
  no store, single scene, weights-only. It is a sharp, useful negative *there*; it is **not** a
  falsification of the mature claim (concepts-on-concepts, store-fed rare associations, multi-cortex
  coherence). Neither "Stage-0 killed it" nor "just a tuning miss" is supported.
- **Capacity-non-saturation caveat (scoped).** Δ2 grows slowly **without bound** at λ2 = 0 (depth
  0.73 MOD → 1.15 SLOW → 1.37 at 3.4× length), so `capacity_fraction` self-normalises to a
  non-stationary level and `t_run ≈ steps`. This **bounds the S-curve-shape and developmental-clock
  claims** but does **not** touch the lift headline (null at every depth tested). It is a candidate
  **substrate** issue for the next design session (the clock lacks a saturating-capacity / re-pool
  mechanism) — **not** a reason the verdict is provisional.
- **The live frontier — a design-table call, not a CC task.** The result cannot distinguish: **(i)**
  Stage-0 is too impoverished to exercise the mechanism (no associative scaffolding for evocation to
  teach *from*, so the rapid phase the claim is about is never created in this environment → next move
  is the deferred **Stage-1 increment**: store / third cortex / richer environment, not more Stage-0);
  vs **(ii)** the mechanism is genuinely inert at the centre → architecture rethink. **Discriminating
  test:** re-run the same **lift** metric once cross-concept scaffolding exists (first Stage-1
  increment) — lift-still-null ⇒ (ii) gains weight; lift-appears ⇒ (i), Stage-0 was pre-rapid. The
  real mechanism the empty-gap did **not** test — **attention-sculpting via evocation-driven
  unpooling** (the word shapes *which* distinctions are worth maintaining, not acquisition; re-pool
  the associatively-inert against intrinsic decay) — is the forward bet in
  `docs/FRONTIER_attention_sculpting.md` (`[PROPOSED]`), which re-scopes the negative to
  acquisition-only and specifies the non-redundant discriminating rig (the 4→8 conflict, **reversed-lift**
  readout: does the *intact* arm re-pool the associatively-inert distractor axis the no-word arm keeps).
  **[2026-06-29 — SUPERSEDED on the (i)/(ii) point; see §12.E.** Building that rig surfaced a GATING
  PRECONDITION: the evocation channel is **content-dead in the deployed regime** and was never live in
  any Stage-0 configuration. So this "discriminating test" cannot be posed yet — Stage-0 gives **zero**
  bearing on (i)/(ii) in either direction; the fork is **unasked** until a channel-live rig exists. The
  `lift ≈ 0` headline stands; its scope collapses to the channel-independent part ("vision doesn't need
  the word for a resolvable distinction"). Evocation-as-teacher is **wholly untested.**]
- **Why the negative is trustworthy (process provenance).** The oracle's divergence gate had its
  **original directional criterion falsified by data** and was **re-pre-registered** to
  divergence + content-driven, the superseded gate kept in the canon (exp03 vacuous-F4 discipline,
  `oracle_gate_record.json`); **Step 0 surfaced a ~3× run-length shortfall** — Phase-1's 4000 steps
  sat at depth ~0.156 ≈ **28 % of plateau**, the quantitative confirmation of §12.A's "sitting in the
  toe"; the **verdict logic was frozen in `spec_hash` before the surface existed**; convergence was
  checked across depth 0.73 → 1.37 (~4× range) via MODERATE-vs-SLOW and a 3.4×-length extended run at
  the prime clean-G candidates b7/b8 (lift −0.014 / −0.011).

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
- **The determinism contract is seed + construction order + TORCH THREAD COUNT**
  (measured 2026-07-03, exp09 wiring: 16 threads perturbs floats ~1e-9 via
  parallel-reduction order — visible only where column quantization is percent-scale;
  1–2 threads byte-identical). Every rig that claims replay/bit-faithfulness pins the
  thread count and records it in its artifacts (`torch_num_threads`). General lesson,
  not an EXP09 footnote — future rigs inherit it.

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

**RESULT (2026-06-26) — the curve was drawn; outcome = EMPTY-GAP (see §9 / `SWEEP_RESULTS.md`).** The rapid-phase PAM-grad-**share** rise the hypothesis named IS present (s_curve_sig 0.80–1.00) — but it is **non-discriminating and non-load-bearing**: it appears identically where the word is provably inert, and the acquisition **lift** (intact − no-word) is null everywhere. So the observed S-curve is **not** the paradigm S-curve. The hypothesis is *not* confirmed; the new live frontier is the **(i) impoverished-Stage-0 vs (ii) inert-mechanism** fork (§9) — the real untested mechanism (attention-sculpting via evocation-driven unpooling) and its discriminating rig are in `docs/FRONTIER_attention_sculpting.md` (`[PROPOSED]`).

---

### B. Slow-start unpool ramp [SETTLED in design — architecture addition]

**The unpool clock should ramp slow→fast, not run at constant rate.** Constant-rate is acceptable *only* for the short Stage-0 tests (and stays pinned constant for them). In principle it is wrong: **words must stabilise against what the vision encoder already sees before unpooling splits the blobs** — otherwise the split happens against an unsettled target.

This is **reference-and-relaxation** again, applied to the unpool clock: the word-anchor is the slow reference; unpooling (the fast learner) must not outrun it early. Same *shape* as the gain ramp (already pinned-from-zero): stiff/slow at first, releasing as word↔blob associations settle.

- **Implementation face — build-full / pin-to-constant / release.** Build the ramp in full; **pin it constant for the short Stage-0 runs** (no behavioural change now); release it when runs get long enough to need it. No debt — the constant case is a special case of the ramp.
- **Discipline note — this is principled pacing, NOT gating.** Slowing the clock so the reference can settle is legitimate; it does **not** gate vision from learning B. It is distinct from (and must not become) the manufacturing-the-effect failure the next session's knob choice guards against. Pacing the clock against its reference ≠ constraining vision into the answer.

This supersedes the §4 "unpool clock — clock-led, v1 gate pinned to 1" note *only in principle* (the ramp is now the designed form); the **pinned-constant behaviour for Stage-0 runs is unchanged**.

---

### C. Characterisation sweep [RESOLVED — design closed; spec issued]

The knob fork is closed. Finalised design lives in `docs/STAGE0_CHARACTERISATION_SWEEP_SPEC.md`
(exp03-style; CC builds from it). The next step is **not** "make Readout G go clean" — it is
**characterise the curve**, computed not eyeballed.

**Resolution (the design CC builds):**

1. **Asymmetric, not a symmetric grid.** Band (`r_fine`↓ / `sigma_stim`↑) is the **dense** axis —
   it moves the autonomous-vs-associative balance, the quantity Readout G measures. Unpool-rate is
   the **coarse** axis — two constant rates (`MODERATE` = the §12.B-pinned clock, `SLOW` = a
   fraction below it), tempo only, **fast cell dropped**. Crossing symmetrically would entangle
   balance with tempo (the gain-ramp 1D attribution-blur); hence band-dense × rate-coarse.
2. **Runs reach plateau on each clock's own terms.** `T95` = first wave at capacity-fraction ≥ 0.95;
   `T_run = 1.25·T95` per (cell, rate, seed). Compute is not a constraint — the fast cell's "get out
   of the toe" rationale was a cost substitution and is dropped; the toe's length is part of the
   S-curve hypothesis, so a moderate/slow clock measures it rather than compressing it.
3. **Seeds are the instrument** (≥20/cell). Phase-1's G ambiguity was seed-instability; the
   deliverable shifts from "does a window appear" to "in what fraction of seeds, how sustained."
4. **Oracle is a logged column at every cell** (no-word capacity-open B-recovery), compared to a
   threshold **calibrated on the live commit** (Step 0 — B00 oracle calibration: `chance + margin`,
   below the easy-band ceiling; **never** a guessed literal — the oracle floor sets the band cap, so
   a guess either never fires F3 or caps inside the clean-G window). The cell where oracle-recovery
   crosses the threshold is the cap on the sweep (F3) — the drift-trap line.
5. **The verdict is arithmetic.** `pam_grad_share` (bounded) logged across the trajectory vs
   `capacity_fraction` (the only axis that compares two clocks). S-curve signature pre-registered as
   an inequality over the seed distribution: `delta_rapid > 0 ∧ delta_plateau ≤ tol`. clean-G
   sustainedness pinned as a rule; `autonomous_resolution_frequency` is the F2/F4 discriminator;
   F1–F4 failure taxonomy pre-registered in the spec.

**Still binding (carried, unchanged):** the sweep is **re-calibration of the existing regime**,
never a gate that lets vision learn B only via the word (manufactures gap-3 = wrong-reason);
discriminator = the no-word capacity-open oracle must still recover B; no stop-grad. Constant
unpool-rate here is a coarse **S-curve locator**, orthogonal to §12.B's ramp (**pinned off for the
sweep regardless of run length**) — **not** a finding about developmental pacing. This is a
Readout-**G** change and does **not** discharge the §12.D Readout-**D** entangled-corner debt.

**RESULT (2026-06-26) — BUILT, RUN, CLOSED → EMPTY-GAP.** 480 cells + extended confirmation (§9 /
`SWEEP_RESULTS.md`). No clean-G window at any cell; gap-3 wired but **inert** (lift ≈ 0 everywhere);
B **representable** throughout (not F3). The sweep delivered exactly the falsifiable read it was built
for. The remaining open question is **not** a CC sweep task — it is the design-table **(i)/(ii)** fork
(§9): is Stage-0 pre-rapid (→ Stage-1 increment) or is the mechanism inert at the centre (→ rethink)?
Also surfaced a **substrate** issue for the next design session: capacity does not saturate (Δ2 grows
unbounded at λ2 = 0), so the developmental clock lacks a re-pool / saturating-capacity mechanism.

**Next-frontier doc (forward bet, `[PROPOSED]`):** `docs/FRONTIER_attention_sculpting.md` —
attention-sculpting via evocation-driven unpooling against intrinsic decay, the mechanism the
empty-gap did **not** test (it tested the *redundant* acquisition reading; the real one is "the word
shapes which distinctions are worth *maintaining*"). Held provisionally per sit-with-it-before-canon;
its §7 A-vs-B mechanism fork (is the unpool force the existing gap-3 gradient, or a new
evocation-divergence computation?) gates any build spec, and its §8 reversed-lift rig is the
non-redundant test the Stage-0 stimulus structurally could not provide.

---

### D. Standing debt (carried forward, unchanged)

**Readout-D linearly-separable regime.** `full_ols_r2 ≈ 0.9999` — order recovered in-loop but in the linear-index regime, not exp03's entangled corner (~0.80). Caused by the dwell-stable fix removing exp03's along-`u` content variation. **Re-test the entangled corner (`full_ols_r2 < 0.9`) the moment within-window content drift returns** — it resolves for free when the deployed space genuinely moves. The band/clock sweep is a Readout-G change and **does not discharge this**.

### E. The evocation-channel blocker — gating precondition for the whole attention-sculpting program [BLOCKER · design-table decision · 2026-06-29]

Building the Stage-1 attention-sculpting rig (`STAGE1_ATTENTION_SCULPTING_RIG_SPEC.md`; built faithfully at `experiments/05_attention_sculpting/`, with only behavior-preserving hooks added to exp04 + `src/loom/constant_repool_delta2`) surfaced a prerequisite the program rests on and does not yet have. **Full brief: `FRONTIER_attention_sculpting.md` §10.** Verified by a 4-lens adversarial panel (unanimous) and a content-agnostic neutral liveness probe.

- **What is dead.** The `PrototypeResonanceOperator`'s PAM substrate **collapses to a single point** in the deployed regime (prototype within-group spread 6.8e-3 init → ~1e-9…1e-11, all 3 seeds, from ~t=300), so `z = pa @ Wp` is **content-invariant**. The gap-3 gradient reaches the masked vision **target** (so "gap-3 alive" passes) but as a **member-invariant constant pull** carrying no word/member information; vision's above-chance B_track comes from the spread/JEPA terms, **not** PAM evocation. The operator *form* is fine (a fresh op on a clean neutral 2-member task routes at (d)≈1.27 even at init 1e-3) — the collapse is purely the **deployed regime**.
- **Why it blocks the rig.** Reading-A routes occupancy through evocation; on a dead channel a reversed-lift run is a **WRONG-REASON null** ("the word doesn't teach" ≡ "the channel was too dead to carry it"). So §8 cannot be run until the channel is live.
- **Candidate levers, causal structure UNDETERMINED (not a solved diagnosis).** The authorised contained fix (operator-side, scale-robust, minimal-DOF, no tuned dial, content-agnostically validated) was pursued **to exhaustion**: prototype-init rescale, window-centering (fails — within-dwell content is itself window-constant), carrier-DC-along-`u` removal, and **stimulus-side carrier-bounding** all gave **no revival**; only a *stack* (cosine + pam_lam=0 + init + 2× training) reached ~15% of clean capacity. Three named candidate levers — **carrier scale × PAM pool penalty × the diffuse multi-member completion signal** — were each insufficient alone and jointly movable; **the load-bearing lever is unknown.** The most under-decomposed gap is **clean-2-member (d≈1.27) vs diffuse-multi-member deployed (dead)** — the real lever may be **how PAM's completion task is posed**, not the operator or carrier.
- **exp03 residue — verified, come-due, necessary-not-sufficient.** §6 / exp03 RESULTS.md:120-126 pre-flagged the comparator's **absolute-scale sensitivity to large OOD per-sequence offsets**; Stage-0's continuous unbounded carrier (deployed `ctx`≈333 vs prototypes ≈0.03) is exactly that — but **bounding it alone does not discharge it.** Real-but-partial.
- **Empty-gap re-read — a sharpening, NOT a retraction.** The `lift ≈ 0` headline **stands** (calibration-independent of *why* evocation fails). But the channel was **content-dead throughout** and never close to live in any Stage-0 configuration, so **Stage-0 gives ZERO bearing on the (i)/(ii) fork in either direction** — (i)/(ii) asks what happens *when the channel works*; it never worked, so the question is **unasked** (this **supersedes** the §9 "(i)/(ii) discriminating test" bullet). The negative's scope **collapses to its channel-independent part — "vision does not need the word for a visually-resolvable distinction"** (Step-0 (a) reconfirms: no-word vision occupies the salient distractor 0.95, neglects the subtle category ≈chance). **Plainly: the central paradigm bet (evocation-as-teacher) is wholly untested — evocation has never carried information end-to-end in a deployed loop.**
- **The blocker is a design problem, not a bug.** A live evocation channel in the deployed regime is the **prerequisite for the entire attention-sculpting program**; producing one is an open **operator/PAM-substrate (possibly completion-task) redesign** — the design table's to scope. An exp06 channel-revival experiment should be designed *from* this brief once a direction is chosen, **not instead of it** (load-bearing lever unknown). The neutral (d)-gate is the **pre-registered liveness pass** any redesign must clear before Stage-1 is re-attempted; order recovery + no-clean-slot are guards (unchanged across every operator patch).
- **Status & provenance.** Stage-1 rig: **built, faithful, not wrong** — Step-0 (a)/(b) pass, (c) blocked on the dead channel; it **waits on the redesign**. The contained fix was exhausted before escalation, and the (d)-gate **rejected the init=1.0 `clamp` artifact** (a manufacturing-shaped false positive caught **before canon**). This is the apparatus working — **not the project failing twice** — instrumentation refusing to let an **untested** bet read as tested: two apparent "the word doesn't teach" nulls, **both dead-channel artifacts, both caught, both kept out of canon.** The central claim is exactly as alive as it was; it has simply never been tested, and we now know precisely what must exist first.
- **[2026-06-29 — RESOLVED by exp06: the lever is determined (supersedes "candidate levers UNDETERMINED" above).** The decompose-first **channel-revival factorial** (`EXP06_CHANNEL_REVIVAL_FACTORIAL_SPEC.md`; `experiments/05_attention_sculpting/exp06_factorial.py`) decomposed the clean-vs-dead gap over **member-count × cue-diffuseness × PAM pool-penalty**, carrier **bounded as the necessary-not-sufficient baseline in every cell**, measured by the now-committed neutral content-agnostic **(d)-gate** (`dgate.py`). Step-0 validity triad **PASSED** (V1 clean live + d_same 0; V2 dead collapsed proto 4e-7; V3 traverse) and was committed **standalone** as a clean provenance point (`335f36d`, carrying no direction-finding). The interior read was **adversarially verified** (5 independent lenses, unanimous SURVIVES, no overturning alternative) and the deciding cell **re-confirmed at plateau**.
  - **VERDICT — JOINT LEVER = {cue-diffuseness, PAM pool-penalty}**, super-additive: undoing **either alone** from the dead corner stays dead (d 0.000), undoing **both** revives (d≈1.1, lift 1.005 vs Σ-singles 0, margin 0.477). **Member-count is tolerated-deployed for LIVENESS — a ~22% degrader that does NOT flip whether the channel revives (NOT a killer; manyOnly plateaus d≈1.11 vs clean 1.42, above the live bar); it is a non-lever ONLY for liveness. SCOPE-NARROWED by exp07 (2026-06-30): member-count DOES modulate the reshaped (preserve) tie's capacity cost — a seed-paired, scale-growing ceiling cost (~0 @card-2 → +0.103 @card-16, paired t=2.84), a channel exp06 did not measure. The liveness non-lever stands; the unqualified "non-lever" does not.** The **3-way irreducible-conjunction alternative is rejected** at convergence.
  - **DIRECTION (exp07): re-pose PAM's COMPLETION TASK** as a **joint, symmetric** redesign over the two factors — (a) **how the cue is posed**; (b) **drop/reshape the λ2-tie on PAM's prototypes** — pursued together, with **NO penalty-first ordering**. The penalty/diffuseness **kill-texture asymmetry** (penalty = perfect point-collapse proto=0; diffuseness = near-collapse proto>0 + faint seed residual) is **characterisation only** and was kept **out of the lever arithmetic** (which used d_diff means).
  - **Why convergence was accepted on the d-mean (load-bearing, recorded so it survives compaction).** The deciding cell [1,0,0] was unconverged at 4000 steps (still climbing). Re-confirmed to plateau (16 seeds, to 12000): **d_diff plateaus flat at ~1.09–1.11 from step 6000** (mean 1.106, sem 0.033, mean−2·SEM **1.040 ≥ threshold 0.967**). The pre-registered "(d) flat **AND** proto stable" criterion's proto-clause never triggers — **prototype spread keeps growing monotonically** — **but the clean cell does exactly the same** (clean proto 1.71→2.23 while clean d is rock-flat 1.418). **Proto-flat is a DEATH certificate (dead cells: proto→0 and stay 0), not a LIFE one**; for a *live* cell the substrate keeps differentiating, which can only sustain/raise d. So the **functional metric (d) is the convergence signal**, it has plateaued, any residual creep is *upward* (safer), and the §4 decision rests on the converged d-mean. Routing held under the longer budget: both deciding-pair constituents stay hard-zero, the soft diffOnly cell stays out of the arithmetic.
  - **Empty-gap / (i)/(ii):** still **unasked** — exp06 names the lever and revives the *neutral probe*; it does NOT yet revive the *deployed loop*. The fork becomes answerable only once **exp07** builds a channel-live deployed rig from this direction. Lever determined ⇒ exp07 is **scoped from** this result.]**
- **[2026-06-30 — exp07 Phase 0 (cue-floor × penalty surface), MEASURED not built (FRONTIER §10.8; `EXP07_CUE_FLOOR_PENALTY_SURFACE_SPEC.md`; `exp07_*.py`).** Read the cue-floor-as-f(penalty) surface through the committed (d)-gate (no new operator/store); `reshaped`(preserve) = the settled cortex StepSchedule on PAM's tie. **Step-0 gate signed off before any interior read.** Two methodological traps caught+fixed first (single-clock δ1-penalty irreversible-collapse → cortex two-clock; fractional-onset budget-drift → **absolute** two-clock onset 900/3600); with the fix reshaped revives across all 10 seeds both cards (earlier bimodality was the onset artifact). Interior read **adversarially verified** (4 named-blind-spot lenses; survives directionally, no false-PASS — every confirmed error understates the reshaped cost; two as-worded framings corrected in the artifact).
  - **FINDING 1 — cue recoverability is STRUCTURALLY FORCED + construction-scoped.** Re-posing = global mean-centering; the deployed cue is ~100% common-mode (5.831·base over 0.5·Cd) → floor≈0 follows from the construction, not training (near tautology). The **build-robust half** of the two-part cue fix (structured/native diffuseness) is **UNMEASURED**; common-mode-dominance is itself a probe simplification of the deployed rig (true deployed floor may be >0).
  - **FINDING 2 — penalty legitimacy = PRESERVE on the uniformity argument, at a measured cost (NOT "validated").** Both drop(off) and preserve(reshaped) **revive** (liveness doesn't select). Robust deliverable = a **seed-paired SCALE-GROWING CEILING capacity cost**: off−reshaped **+0.103 @card-16 (paired t=2.84, both converged @36000), ~0 @card-2**. "Floor-equivalent" is **ruler-dependent** (own-sharp Δ0.027 yes; common off-sharp ruler — the one the artifact's topology uses — Δ0.103 NO) and the sharp-gap is **not significant** (t=1.48) → cost booked as ceiling, not laundered out of the floor.
  - **FINDING 3 — topology klass-invariant but trivially (deployed-dead-driven); discriminating off-vs-reshaped relationship NOT cardinality-invariant** (dead tie @card-2 vs significant @card-16) → member-count modulates the tie's capacity cost (exp06 liveness non-lever scope-narrowed in place, above).
  - **exp07 DIRECTION (scoped):** re-pose completion with content-blind cue re-organization (dominant for common-mode diffuseness) + the preserve open-and-stay-open tie (legitimate on uniformity; real scale-growing capacity cost; slower convergence). **Still unmeasured:** structured-diffuseness floor; *deployed-loop* revival; empty-gap (i)/(ii) — all remain open.]
- **[2026-06-30 — cue-floor (build-robust half) SHELVED with trigger.** The structured-diffuseness floor is a property of the **static `ConflictStimulus` construction** (block geometry + σ=0.20), **not the loop**; measuring it optimizes one static single-frame stimulus, off the loop's critical path. **Deferred, not abandoned; trigger = the loop test stalls on evocation signal capacity** → the within-frame floor becomes load-bearing and Phase-1 resumes with a measured reason. Rationale: signal/clutter separation gets easier with the architecture's intended-but-unbuilt **continual time** (earned salience) + **multiple cortices** (cross-modal recovery); "easier later" is a **prior, not a fact**. CC's read-only rig analysis banked as the pickup artifact (FRONTIER §10.9): full-16 68% structured / within-group 13.5%; category signal @PCA-1.41 vs distractor @8.49 near σ=0.20; global-mean-centre = only non-circular floor instrument (PCA/whitening/block-centre variance-matching-circular; ablation guard misses this); calibrated-synthetic + deployed-direct-validation design. Phase-1 spec scoped, not written.]
- **[2026-06-30 — LIVE FRONTIER: evocation-as-teacher remains UNTESTED.** exp06/07 established the **channel revives** — clears the neutral (d)-gate **above the live bar** (revival d≈1.0–1.1 vs clean-2 *healthy* ≈1.41) once **cue and penalty are jointly addressed** (cue re-organization dominant for common-mode diffuseness **(structured/build-robust half shelved, §10.9 / shelve entry above)**; preserve-style open-and-stay-open tie legitimate on uniformity grounds at a measured, scale-growing capacity cost). **The channel carries information; it has NOT been shown to teach** — to **sculpt cortex representation via evocation-divergence.** **Next phase: scope the minimal rig that tests whether evocation sculpts cortex representation.** The scoping fork (continual time + second cortex from the start, vs single-cortex minimal-first) is **RESOLVED → FRONTIER §10.11 / the 07-02 entry below.** (Bar note: revival cleared the *live* bar 0.867, not the full *healthy* ~1.41.)]
- **[2026-07-02 — loop-test scoping fork RESOLVED → anchored-reference minimal rig
  (FRONTIER §10.11).** Plastic vision cortex against a **FROZEN word anchor** (no
  relaxation schedule in this rig — pin-to-constant, #12's stiff limit, no debt),
  **continual time, both from t=0.** Grounds: §7 signature (occupancy-lag requires the word
  cortex to exist); #12 (the anchor IS the stable reference; single-stream doesn't start);
  **echo-chamber** (single-cortex PAM's content is wholly vision-derived — a mirror, not a
  teacher; structural, premise-free; supersedes exogeneity, demoted to supporting). Fixed
  encoding ≠ fixed association — PAM still acquires vision↔word (§7 lag intact).
  Mutual-sculpting pair deferred to release (needs a designed relaxation schedule). Metric
  = occupancy-lag **lift**, never share. The revise-vs-fresh fork **RESOLVED → REVISED in
  place (eabe08b) and executed through the §L gate sequence — see the 07-03 line below.**]**
- **[2026-07-03 — DESIGN GATE OPEN (long-horizon vision-content collapse); kick probe
  pending checkpoint read; gate steps 5–6 BLOCKED.** The §L gate sequence ran: liveness
  calibration (16-cue bar 0.8866/k=13; then MATCHED bar 0.3128/k′=7 after three pre-read
  instrument fixes: degeneracy→ruler v2, censoring→schedule, composition→per-seed
  alignment), windowed Step-0 (a)/(b)/(c) PASS on the run commit, entry run
  **NON_CONVERGENCE** (cap 112500) with a verified major finding: **total vision-content
  collapse at long horizon in the word-present arm** — assignment-side (**dead-dictionary
  DEMONSTRATED**: argmax_k=1 sustained, capacity open), engine = the gap-3 no-detach
  TARGET-side pull (NECESSARY, by the detach arm), **word = ~5× accelerant +
  pin-deepener** (asg_dist ~1e-5 locked vs no-word ~0.08 regrow-capable; word terminality
  n=2; no-word = METASTABLE INTERMITTENT COLLAPSE, NEITHER_BY_CAP at 500k). EXP08 arms +
  converters pre-registered and adversarially verified throughout (FRONTIER
  §10.12–§10.12.2; `EXP08_COLLAPSE_ARMS_PREREG.md`). Instrument rulings: den demoted to a
  one-sided collapse-floor tripwire (variance statistics cannot certify differentiation);
  windowed estimators rig-wide; dynamics panels standing. **Design-gate constraint: any
  revision must keep routing/assignment INPUT-SENSITIVE under the target-side pull.** On
  the table: routing-side counter-force (highest-risk — manufacturing class) / denser
  anchor / revised target path; #12/EMA note promoted to design-table input. Parked with
  triggers: acquisition-aligned ladder reads; coarse-first ladder (ambiguity
  discriminator); ties re-dose ε<0.05; cue-floor build-robust half (§10.9, its own
  trigger). **KICK PROBE RUN + RE-SCORED (FRONTIER §10.12.3): ESCAPABLE stands both states
  (all beats kept; expected ABSORBING falsified on the record); population = 2 PIN / 8
  EMBER / 8 FLICKER / 6 SUSTAINED-functional; the no-word ε=0 control self-pinned at ~518k
  → fate shared end-to-end, word = pure accelerant (5.4×/4.8× converging) + pin-deepener
  (§10.12.2 scope line superseded by measurement). Fork re-ruled: PREVENTION-PRIMARY,
  RECOVERY-UNRELIABLE — the flow is mostly-absorbing with stochastic re-amplification
  pockets; regulation = widening the pockets by design. Correlate hunt: conditioned by
  POSITION, stochastic within position (early ≫ late); no controllable rescue lever found.
  Next: THE DESIGN TABLE opens from canon — first deliverable = the force-ledger;
  constraint = input-sensitivity must be SELF-SUSTAINING under the deployed flow; kick-
  not-a-candidate barred; steps 5–6 blocked.**]
- **[2026-07-03 — THE DESIGN TABLE (FRONTIER §10.13): force-ledger v1 DELIVERED; Fork 1
  RESOLVED → the self-path #12 reference; EXP09 spec AT CHECKPOINT.** The ledger (7
  forces, every number traced to committed artifacts) surfaces the structural fact: the
  engine and the teaching force are ONE PATH — the gap-3 gradient's common component
  (contracts) vs differential component (separates, self-consuming at the pin) — and the
  self-path is the one plastic loop with no #12 reference. Fork 1 → (a): a slow copy of
  the vision cortex supplies the self-path reconstruction target (detached reference,
  not co-developer; build-full/pin-to-constant, single fixed lag β [RECONCILE]; no new
  force or objective; word path untouched). Function test pre-registered KICK-FREE
  (word seeds {0,1} ≥192k = 2× the 96k terminal clock; no-word rides as control; FAIL =
  pin on any arm; PASS literal-form pinned, necessary-not-sufficient). Honesty block on
  record: the design shares the detach diagnostic's gradient topology — the detach-null
  wrong-reason screen is load-bearing before any PASS is trusted. Decomposition
  observable ruled (common/differential split on evocations + gradient — the
  contraction/teaching ratio as a trajectory). Parked with triggers: (b) spread
  re-weight; (c) denser anchor. Pre-commit adversarial verification applied (23
  confirmed findings — incl. the tabled row-2 "~4× post-death word pull" REFUTED as
  probe mask geometry; the β fast bound demoted to UNMEASURED; the function-test
  literal forms re-pinned flicker-tolerant/censoring-aware; the gradient-share
  discriminator struck as circular). **CHECKPOINT RESOLVED (same day, Jason's ruling):
  strikes ratified; ground (3) RE-WORDED (teaching path re-routed, not intact; the
  design = a recorded BET; stop-grad-in-costume = pre-registered partial outcome); β by
  RULE (τ = 2× pinned den period → 9600; 4800 stands as instrument of record, the 1500
  demonstrated to be segment contamination); taxonomy ratified with constants
  calibrated from measured healthy placements (27/32, k=1 run ≤2, den all-32; K_w=3,
  K_c=8 with control-PIN-unreachable consequence recorded); all eight §10 items
  resolved. BUILD AUTHORIZED to ONE final pre-run read (wire → asserts →
  replayed-baseline decomposition panels), then arms. Steps 5–6 stay blocked.** Spec:
  `EXP09_SELF_REFERENCE_PREREG.md`.]
- **[2026-07-04 — EXP09 RUN + RULED (FRONTIER §10.14): screen fires
  STOP-GRAD-IN-COSTUME; Fork 1(a) UNRESOLVED-NOT-REFUTED; fork record → EXP10
  STRUCTURED VARIATION.** Four arms 192k: both slowref word arms PASS_PENDING_SCREEN
  with maximal margins (zero k=1 windows at 2× the baseline terminal clock), control
  clean — but detachnull scores PASS_PENDING_SCREEN with IDENTICAL margins and no
  recorded column separates them.
  Certified scope NARROWED at ruling: pull-removal prevents the pin; the reference's
  contribution UNDETECTED. Knob certified separately (no copy-collapse). Regime shift:
  all four arms at a spread set-point neither baseline inhabited → instrument lesson:
  verdict constants calibrate IN-REGIME. HOW columns demoted (the flip restates
  member-distinctness in gradient units — null's probe retains the target term and
  flips anyway); SURVIVING observation: gradient-diff-dominated yet
  EVOCATION-common-dominated everywhere — the teaching axis is where the design bet
  must be decided. Baseline corrections: word_terminal pin onset 75300;
  marathon_ext(500k) NO pin
  (three regrown episodes, max 5.92 periods); ~518k = the kick ε=0 resume. Fork
  record: teaching-axis discriminator under STRUCTURED VARIATION (unpredictability pin,
  three clauses: stochastic sequence / identity-independent / learnable-as-
  distribution), static cells = existing baselines; grounds = empty-gap lesson (§12.C)
  + exogenous differential fuel (the one non-self-consuming ledger force); governing
  line = "Reality is the teacher" (Guiding List.md, cited). **EXP10 prereg DRAFT AT
  CHECKPOINT (`EXP10_STRUCTURED_VARIATION_PREREG.md`); nothing builds or runs; steps
  5–6 stay blocked.**]
