# Stage-0 MVP — Build Spec (Loom / PAM)

**What this is.** The build specification for the first integration: the smallest system that
runs the one operation end-to-end. exp03-style — success signals and their failure conditions
pre-registered here, *before* any code. CC implements from this document; it is the bridge.
**CC-ready, hardening pass folded in.**

**What Stage 0 is for.** *Observability in the loop, not capability.* Every decision is judged
by one question: does it keep **gap-3 fusion** and the **anchor decomposition** readable? — never
by "does it perform." A loop that performs by quietly violating a characteristic teaches nothing
(Stage-3 risk). The pre-registered patterns in §9 are the guard.

**Status.** All four Stage-0 build-blockers are resolved in design. This run **validates those
resolutions in the loop** — not another design pass. Do not re-litigate them.

---

## 0. Build-correctness overrides (read before building)

1. **No PAM latent.** `PROJECT_STATE_AND_MVP.md` §2.2's "own internal latent" is pre-session
   residue. **Stage-0 PAM runs masked completion directly on concatenated cortex-space. No
   distinct PAM latent. No encode/decode codec.** (Both are Stage 1+.)
2. **Asymmetric encoder plasticity, hardened freeze.** "No stop-gradient" does **not** mean every
   encoder updates (§2, §5). The **vision encoder is plastic**; the **word encoder is frozen** —
   **lr=0 AND no weight-decay, no EMA, no optimizer-state** acting on it. A nonzero word-encoder
   parameter-delta is a **build failure** (the anchor went plastic → collapse-control breaks); log
   it as a check.
3. **The operator's mechanism is not pinned in this spec** (§2-ii). CC proposes its minimal
   instance against property-level constraints and surfaces it for review. The spec canonizes no
   architecture (not energy-relaxation, not attention).

---

## 1. Scope (fixed)

- **Two cortices: vision + word.**
  - **Vision** — JEPA-pattern feedforward embedder, small, online from init, **plastic**; weights
    are the soft-tied pool (§4). Runs its own native-grain intrinsic prediction loop.
  - **Word** — pretrained, near-trivial, high-accuracy, **frozen (lr=0, no wd/EMA/optimizer-
    state)**. The parent / anchor; also the structural half of collapse-control (§5).
- **PAM** — the sole associator: non-causal masked completion over a window of **concatenated**
  vision+word bundles. No store, no latent.
- **No store, tracing, segmentation, replay, vividness, multi-entity within-bundle association,
  motor, reward.** All Stage 1+ (§11). **Single-object vision↔word completion is live and
  central** — it is char 2, the within-wave calling-forth.
- **Environment** — a **single object** (non-segmented regime) whose appearance evolves along two
  axes (§8), plus a word channel; presented as a **continuous stream** (§8).

---

## 2. The operator (contract · property constraints · screen)

Specified by **contract and falsifiable property, not architecture.**

**(i) Contract [fixed].**
- A window of **W = 3** concatenated cortex bundles (**pin W=3 for run 1**; W>3 is a sweep/release
  item). Cells are `(wave, slot)` where a **slot is a whole cortex slice** (the entire vision
  embedding, or the entire word embedding, for that wave).
- **Masking is block-level over slices** — mask **whole slices**, never individual scalar
  coordinates. (Scalar-coordinate masking is **diagnostic-only**: masking dims within one
  embedding makes it a masked-autoencoder over coordinates — the leak. Block-level forces genuine
  cross-slot / cross-wave association.)
- Each wave: slide the window by one; draw a mask from the **full cue-shape distribution**
  `{single-slot, whole-wave, interior-both-sides, one-sided-edge, sparse, near-all}` (all over
  whole slices); run **one** completion act (at-once); take **one** gradient step.
- **Target** = the actual emitted content of the masked slices (the encoders' own current outputs;
  self-supervised). Evoked-vs-actual **is** the convergence error.
- **Loss** = embedding-distance on **masked slices only**. Distance/similarity-based, **no free
  linear head** (exp01).
- **Gradient — no stop-gradient, asymmetric plasticity.** No `detach` at any emitted cortex
  target: target-side gradient is preserved — this **is** the gap-3 pressure on the masked vision
  slot. `detach` (severs the path) and freezing (lr=0, parameters fixed) are **different
  operations.** The **vision encoder is plastic** (updates from both the completion path and
  target-side gap-3 pressure); the **word encoder is frozen.** The word-as-target gradient is
  *computed but not applied*; the vision-as-target gradient *is* applied. The gap-3 path lands on
  the vision slot and **survives a fixed word encoder.** (Resolves the apparent "gradient into
  both encoders": detached nowhere, but only vision updates.)
- "Non-causal" is **vacuous within a wave** (char 1: no within-wave order), so it **forces W≥3**
  across waves. Within-wave completion (char 2) = single-wave sub-case; across-wave (char 3) = the
  point. **Stage 0 is the PAM-setting test exp02 deferred.**
- Cue-shape sampling is **mandatory** (exp02 rule #3). Evaluate a **single** completion act (exp02
  at-once).

**(ii) Property constraints on the operator [the spec stops here; CC proposes the instance].**
Completion uses the pooling-substrate weights (§4) to produce the masked slices, subject to:
- **the subtractive screen** — sole exclusion: the **feedforward exact-regression denoiser**.
  **No positive checklist** of admissible mechanisms (that re-imports specification and fights
  operator-form-open);
- **at-once** — a single completion act; exp03's check rejects re-mask-and-re-pass;
- **no free linear head** — distance/prototype readout (exp01);
- **no softmax-attention** — the concrete form of "not a masked transformer."

**CC proposes the minimal instance meeting these and surfaces it for review. The spec canonizes no
form** — not energy-relaxation, not PC inference, not attention. **If** the proposed instance
relaxes internally, **K_settle is bounded-and-logged** (a property-level constraint) and the
relaxation residual is logged; but internal settling is *permitted, not required or named here*,
and the at-once check still applies to the single completion act.

**(iii) Discriminator — two timescales, kept apart.**
- **Run-1: basin-hosting geometry screen (design-time, subtractive, measures nothing).** Admissible
  iff the operator's learned content sits on the **pooling substrate** — a substrate on which
  recurrence *could* deepen structure and splitting *could* divide it. **Capable-of-hosting, not
  already-exhibiting.** This is the substrate-level screen (the sole exclusion of (ii)), not a
  claim about completion-form. Checked **once, at operator selection.** Nothing about basin
  geometry, confidence, or deepening is measured at run 1 — demanding char-5 at Stage 0 is Stage-1
  smuggling.
- **The discriminator proper (pre-registered; NOT a Stage-0 gate).** Basin-deepening +
  graceful-off-manifold-degradation vs exact regression; margin form in §9 Readout O. **Deferred to
  Stage 1** (single scene generates no recurrence/splitting pressure; the regressor is already
  excluded at design time).

---

## 3. Order representation

Order is **order-as-content**, isolation-validated (exp03, faithful corner at high-σ ∧ α=1). The
window carries **wave-relative position as content** — never an index, never a stepped traversal.
Random access to the ordered whole: cue the *end*, recover the *beginning*, in one pass.

- **Entanglement is load-bearing; physical placement is not.** The live path exposes order **only
  in exp03-faithful entangled form** — σ>0 drift injected **into content-bearing dims**, with **no
  clean separable position slot** (a separable slot = order-as-*index*). *Which* content dims carry
  it is a free implementation detail; the committed property is the entanglement. **Hold the
  live-model-never-sees-a-clean-carrier line exactly.**
- **Carrier-zero is an eval-only, experimenter-side diagnostic** in Readout D (§9), using the
  experimenter's ground-truth decomposition — never a live slot, never a global gate.
- **Residue to watch (exp03 caveat).** The validated operator is a within-window comparator with
  **residual absolute-scale sensitivity**; deployed drift has no controlled scale. **Stage 0 is the
  first test of order-as-content under co-developing encoders + pooling + convergence-drift** (exp03
  used fixed generators). **Measured** — Readout D.

---

## 4. Substrate — pooling-state capacity

Soft-tied weight pooling (validated in isolation, exp01). Full parameter budget at init; nothing
added or removed; "capacity" = resolution, not parameter count.

> **Same law, separate weight populations.** The encoder and PAM share the **pooling law and
> trigger semantics** (soft-tie penalty; re-pool on sustained-low-force-magnitude + low-use;
> unpool clock-led) — **not literal shared parameters.** They are **separate weight populations**,
> each running the same law fed by its native error. CC must not read "same object" as
> weight-sharing.

This shared law is gap-3: **convergence error reaching the encoder adds to its gradients → surfaces
as intra-group disagreement → evocation drives encoder differentiation literally.**

- **Unpool — clock-led, not error-pulled.** `rate = base_rate × activity_gate`. **v1: gate pinned
  to 1.** Capacity opens first; perception of the finer distinction follows.
- **Differentiation — intra-group gradient disagreement.** The *consumption* signal, not the unpool
  trigger.
- **Re-pool — reversible re-tightening.** Trigger = **pull-apart force magnitude**, not gradient
  cosine (exp01; cosine diagnostic only). Sustained-low-force AND sustained-low-use; fast-out/slow-
  in hysteresis; graceful. *(Not load-bearing for Stage-0 observability, but the law is present,
  not stubbed.)*
- **Caps:** total budget (trivial); per-region ceiling fixed at init (cross-branch migration
  excluded for v1).
- **Forward rule (exp01):** post-v1 adaptive λ must **scale with local signal strength** to hold the
  unpool break-through threshold constant. (Run 1 is fixed λ.)

---

## 5. Collapse-control

**No stop-gradient.** gap-3's differentiation pressure **is** the target-side gradient on the masked
vision slot; stop-grad would sever it. Decompose by reference-and-relaxation:

- **Anchor (structural).** The **frozen** word encoder guarantees target-diversity on word-as-target
  maskings → removes collapse as a global optimum, **without cutting gradient** (the non-moving-
  target role, supplied by the parent being fixed by lr=0, **not** by detach).
- **Spread on vision (kinetic).** A **distributional-spread** constraint: match the vision marginal
  toward isotropy over **P** random 1D projections, with **no stop-grad, no EMA**. Coefficient
  **α_spread** (§7 loss).

Net: **drop stop-grad, keep an active spread term. Vision plastic, word frozen.**

> **The build depends on the functional property, not the citation.** The spread term is specified
> by *what it does* (distributional spread toward isotropy; no stop-grad/EMA); a future provenance
> correction (LeJEPA / VJEPA-variant) does not destabilize the build. Treat such citations as
> non-load-bearing.

> **Attribution watch.** Spread (→ isotropic) and pooling differentiation (→ tight clusters) act on
> the **same vision outputs.** If differentiation underperforms, **interpose a projector**: spread
> on a throwaway projected head, pooling on the emitted backbone summary.

---

## 6. Initialisation (t=0)

- **Vision: near-fully-pooled but CONVERGED at that depth** — a functioning coarse vision system
  that reliably emits the same embedding for the same input; the **stable coarse target** PAM
  associates against. Stable because **converged, not frozen** (still drifts as it unpools — **no
  char-8 crutch**); **no cold-start wobble.**
- **Word:** pretrained-stable, frozen (lr=0, no wd/EMA/optimizer-state).
- **Drift carrier:** OU at σ>0, entangled per §3, continuous across the stream.
- **Gain:** ramps from 0 (§7).
- **PAM:** cold-starts off structured inputs; needs only sane scale.

---

## 7. Gain ramp

Build gain **confidence-gatable AND capacity-boundable**; **pin both OFF for run 1** (pure fixed
ramp). **Sweep the rate** — deliverable is the **response curve.**

- **Loss target.** `L_total = gain · L_PAM + α_spread · L_spread + L_JEPA`. **Gain scales only the
  PAM convergence loss.** `L_JEPA` (vision's intrinsic prediction loss) and `L_spread` are unscaled
  by gain.
- **Sweep axes.** x = ramp-rate. y (primary) = **B-acquisition-rate** and **final B-margin**;
  diagnostic = **A-capture**; safety = **collapse/diversity**. The sweep **depends on Readout G
  being operational** — sequence after G is established (§9).
- **Rationale (inert-error correction).** Unresolved contrast is **not inert** — its gradient lands
  on coarse weights = corruption pressure on the seeded coarse target. The binding constraint is on
  **gain** (press vs *current capacity*), not the curriculum.
- **Capacity-gating, not confidence-gating, is the safer release gate.**
- **Bound left out of run 1:** moot by construction (slow ramp + first-order unpool), adds
  attribution-breaking coupling, caught by the readout anyway. **Pin, not stand-in.**

---

## 8. Stimulus — factorial axes on a continuous stream

**One object, two appearance axes, one labelled.** (A second object is excluded — multi-entity
within-bundle association is Stage 1+, §11.)

- **A = decoy axis** — visually salient, **word-irrelevant** (unlabelled).
- **B = probe axis** — visually **subtle**, **word-relevant** (labelled). B must sit in a band
  (exp03's σ logic): subtle enough that the **coarse-autonomous** encoder won't find it,
  recoverable-with-capacity so a loop failure is gap-3 breaking, not a ceiling. Two-sided.

**Why both axes (gap-3 teeth).** Probe-only can't fire the FAIL arm; a salient-*probe* destroys
attribution. Subtle-probe + salient-decoy is the only design where the pass reading *and* the fail
reading can occur.

### Temporal structure — continuous stream with dwell (required for Readout D)

- **Continuous stream**, not per-wave i.i.d. draws (per-wave sampling makes Readout D vacuous — no
  order to recover).
- The generative process emits a stream in which the object's appearance (A, B) and word-state
  evolve. **Stochastic dwell**: a coherent segment persists for a stochastic number of waves **≥ W**
  before an **unmarked transition** to a new configuration.
- The **drift carrier runs continuously** (σ>0 OU, **never reset per window**), entangled into
  content-bearing dims (§3).
- **Balanced sampling is over the generative distribution** (across the stream, A×B×word-state×mask
  are balanced), **not per-wave**.
- **Guards (single-object, non-segmented regime):** transitions are **unmarked** — the system gets
  **no boundary signal** (preserves no-segmentation); there is **no across-window chaining** (no
  tracing). The within-window content varies (so order is non-trivial) while staying single-object.

### Pre-loop validity probe (stimulus-admissibility gate)

> **Run ONCE, pre-loop. A stimulus-admissibility gate — NOT a Stage-0 success signal.** It gates
> whether the stimulus is admissible (as exp03 selected σ* before training); it says nothing about
> whether the loop works. A passing validity probe must **never** read as the loop succeeding.

Four checks; **all** must hold to lock the factorial:

| # | Check | Regime / form | Pass condition |
|---|---|---|---|
| 1 | **A-salience** | coarse-autonomous encoder | vision-alone differentiates A (high) → A is a real decoy |
| 2 | **B-floor** = `floor_B` | **coarse-autonomous encoder** (init regime, low capacity) | vision-alone does **not** differentiate B (≈ chance) |
| 3 | **B-ceiling** = `ceiling_B` | **capacity-open OR raw-feature oracle** (different regime) | the oracle recovers B (high) → B is above the data floor |
| 4 | **Separability** | **A_margin / B_margin** (centroid/prototype) | distinguishable; cross-axis confusion **< τ_sep** (logged) |

- **`floor_B` and `ceiling_B` are different regimes by design** — floor at coarse-autonomous
  capacity (B unresolvable), ceiling at capacity-open / raw features (B resolvable). **The floor→
  ceiling gap is the room gap-3 drives**: vision acquiring B by word-pressure when it would not
  autonomously. (As-is single-regime, the gate is self-contradictory.)
- **`ceiling_B` is non-circular**: externally supervised on **ground-truth B labels**, **pre-loop,
  frozen**, distance/prototype, using **neither PAM nor the live word channel.** Reused as Readout
  G's ceiling baseline.
- **Check 4 uses prototype/margin, not free linear directions** (free linear probes violate exp01's
  no-free-head — diagnostic only).

---

## 9. Measurement — one logging format, pre-registered readouts

**Elected structure.** All readouts share one format — exp03's triangulation: *a logged primary vs
an independent, weaker baseline; the gap is the tell; an ablation gate defeats the confound; a named
pass-shape and named fail-shapes.* **A clean primary with the baseline-gap absent is a wrong-reason
pass — flag it, do not celebrate it** (Stage-3 discipline).

### Pre-registered run ordering (sequenced, NOT concurrent)

1. **Phase 1 — intact anchor.** Establish gap-3 (Readout G). Run Readout D and the structural
   signals here. Run the gain sweep here, **once G is operational.**
2. **Phase 2 — anchor degradation.** Run the degradation ladders (Readout A) as **separate matched
   arms.** Anchor degradation changes the vision substrate G reads → must not run concurrently with
   Phase 1.

### Pre-registered conditioning variables (Readout G)

(Constants pinned pre-run — see §10.)
- **A_track, B_track** = nearest-prototype / margin accuracy on the A- and B-axes over vision
  emissions (distance-based).
- **floor_B** (coarse-autonomous, validity check 2); **ceiling_B** (capacity-open/raw oracle,
  validity check 3).
- **B_success** ≔ `B_track ≥ floor_B + k·(ceiling_B − floor_B)` for **N** consecutive eval windows.
- **floor-band** ≔ `B_track ≤ floor_B + ε` (no-word arm).
- **capacity_open** ≔ pooling depth at the B-relevant region ≥ level **L** (logged).
- **contrast_available** ≔ curriculum log shows **both** contrasting word-states introduced.

### Readout G — gap-3 fusion [LIVE · Phase 1 · hardest operationalization]

- **Primary:** **B_track** over time, conditioned on word-state; logged **alongside A_track**.
- **Independent baseline:** **ceiling_B** (external, non-circular).
- **Ablation gate (matched no-word arm):** the word channel **emits a null token** throughout
  B-introduction; the **word encoder stays present and frozen**; **all rates, curriculum schedule,
  and optimizer state are matched** to the intact arm (only the word *content* is nulled). **B_track
  must stay in the floor-band.** *(Late **autonomous** B-discovery — vision's unpool clock eventually
  resolving B without the word — is logged **separately and time-qualified**; it does not
  retroactively count as gap-3.)* *(Acute post-learning word-removal is diagnostic-only — once gap-3
  works vision has internalized B, so post-removal persistence is success, not failure.)*
- **Pre-registered pattern (split readout):**

| Outcome | Condition | Reading |
|---|---|---|
| **PASS** | `capacity_open ∧ contrast_available ∧ word present` → **B_success** | gap-3 working (vision acquired a distinction it cannot find autonomously — only the word could teach it) |
| **FAIL — capture-instead-of-acquisition** | same conditions, yet **B_track in floor-band while capacity/differentiation is persistently (N windows) allocated to A** | freed capacity **captured by A instead of acquiring B**. *(Not "A is represented" — A is salient, vision should hold it. The failure is B's non-acquisition while capacity goes to A.)* |
| **NORMAL (not a fail)** | A differentiating **while word pending** | transient — curriculum's cue to advance the word side |
| **BOUNDARY (not a fail)** | B in floor-band while **word pending** or **capacity not yet open** | data/maturation floor, not gap-3 |
| **INVALID** | A_margin/B_margin not separable (check 4 fails) | B-rise unattributable — re-gate the stimulus |

### Readout D — order-as-content in the loop [LIVE · Phase 1 · logged-and-watched]

The in-loop test of the claim exp03 sent here — it cannot be unmeasured.

- **Primary:** **endpoint→beginning completion accuracy** (cue the end wave, recover the beginning
  wave's content) as a function of **cumulative drift**. **Logged separately** (endpoint→beginning
  loss is its own log line).
- **Window selection:** valid windows sit **within a single dwell**; **transition-spanning windows
  are logged and excluded per the oracle.**
- **Independent baseline:** the **ground-truth order oracle** (true wave positions → best achievable
  endpoint→beginning recovery given the drift).
- **Carrier-ablation diagnostic (ports exp03's gate; defeats content-memorization):** **eval-only,
  experimenter-side**, using the experimenter's **ground-truth decomposition** to remove the
  position component — zeroing it **must collapse** endpoint→beginning recovery (else the operator
  was content-memorizing via the begin↔end bijection, not reading order). The **live model never
  sees a clean/zeroable carrier**; this is **not a global gate**.
- **Pre-registered watch (not a hard gate):** operator tracks the oracle as cumulative drift grows =
  order-as-content survives in-loop; **falls below oracle as drift accumulates** = **scale-
  sensitivity biting** (the exp03 residue) → **flag**, carry forward.

### Readout A — anchor-asymmetry / collapse-control [LIVE · Phase 2 · one experiment serves both]

- **Scoring: collapse is scored on DIVERSITY / MARGIN per half** (covariance spectrum / SIGReg
  statistic / word separability) — **completion-loss alone can fall *under* collapse** (a degenerate
  representation completes trivially), so **loss is task-quality support, not the collapse verdict.**
  **Score by ladder trajectory** — which half's diversity collapses first, at which rung — **not by
  endpoint.**
- **Two ladders (different intervention classes), implemented as perturbation of the emitted word
  embeddings (or a degraded copy) — NOT training drift** (the word encoder is frozen):
  - **Ladder 1 — collapse-control:** `controlled noise → reduced separability → low-diversity`.
    Scored four-way (below). Graded, **not** destructive (random destruction = data ceiling =
    vacuous; the exp03 vacuous-F4 lesson).
  - **Ladder 2 — label-permutation:** a **separate coherence diagnostic** (a char-12 / coherence
    intervention class, distinct from diversity collapse). Logged separately; not in the four-way.
- **Pre-registered four-way pattern (Ladder 1, on diversity/margin trajectory):**

| Outcome | Trajectory | Reading |
|---|---|---|
| **PASS** | **word-as-target half's diversity collapses first**; vision half holds | anchor held the word half structurally; spread held the vision half |
| **FAIL-A** | both halves collapse | spread (kinetic) insufficient |
| **FAIL-B** | neither collapses across the ladder | anchor wasn't structural |
| **FAIL-C** | **vision-as-target half collapses first** | decomposition mis-assigned (roles wrong) |

### Readout O — operator-degradation [DEFERRED to Stage 1 · format pre-registered]

- **Primary:** parent-vs-child **margin** under ambiguous-content perturbations. **Margin-based, not
  distance-to-nearest** (a nearest-prototype completer legitimately lands near a training point).
- **Pattern:** graceful = near coarse-parent / low fine-child margin · snap-regression = high-conf
  child under an ambiguous cue · confident-wrong = far from parent · collapse = cue-invariant.
- **NOT run at Stage 0** (no recurrence/splitting pressure; regressor already excluded by the
  design-time screen). The **Stage-1 re-entry test**, sharing the format.

### Two structural live signals [Phase 1 · checked directly]

- **char-7 holds in code.** Use (complete) and adjust (gradient step) in one pass; **no train/run
  branch anywhere.** PASS = no phase split.
- **pooling visibly does something.** Under the fixed unpool clock, capacity opens and members
  differentiate — substrate **live, not inert.** Distinct from Readout G: *that* differentiation
  occurs vs *whether the word taught it.*

---

## 10. Logging, pinned constants, hygiene

### Minimum-logging block (every eval window)

- **Gradient attribution** — vision gradient split by source: **vision-from-JEPA-predictor-error vs
  vision-from-PAM-convergence-error** (both nonzero = gap-3 alive). **Word-encoder parameter-delta ≈
  0** — a nonzero delta = the anchor went plastic (build failure; verifies override 0.2).
- **Loss-by-mask-family** (per cue-shape family) · **per-half loss** (word-as-target, vision-as-
  target) · **endpoint→beginning loss** (separately, feeds Readout D) · **spread/completion loss
  ratio** · **no-word B-track** (the ablation arm).
- **Relaxation residual** — *if* the operator settles (else N/A).
- **Pooling depth** per region (feeds `capacity_open`) · **pull-apart force** magnitude · **gain** ·
  **curriculum state** (feeds `contrast_available`) · **A_margin / B_margin** + cross-axis confusion.
- **Order diagnostics** — σ, adjacent-overlap, entanglement (best-linear-read R² of drift from the
  mixture; exp03 check).

### Pre-run-pinned constants (gather, choose before the run, log all)

| Const | Meaning |
|---|---|
| **k** | B_success gap fraction (`floor_B + k·(ceiling_B−floor_B)`) |
| **ε** | floor-band tolerance (no-word arm) |
| **N** | consecutive eval windows for sustained/persistent |
| **τ_sep** | validity check-4 cross-axis confusion threshold |
| **P** | number of random 1D projections (spread term) |
| **α_spread** | spread-loss coefficient in `L_total` |
| **L** | `capacity_open` pooling-depth level at the B-relevant region |
| **K_settle** | *(conditional — only if the operator settles)* bounded settle-iteration cap |

### Instrumentation hygiene (scoring policy, not first-run gates)

- **Seed policy:** **single-seed** first, to see if it runs; **3-seed for the headline Readout G
  verdict**; flag **seed-unstable** if outcome *categories* flip (PASS/FAIL/NORMAL) across seeds.
- **Eval cadence:** evaluate on **held-out windows** (within-dwell) at a fixed interval.
- **Probe support/eval separation:** prototype probes use disjoint support and eval sets.

---

## 11. What Stage 0 deliberately does NOT test (re-entry triggers)

| Deferred | Re-entry trigger |
|---|---|
| Distinct PAM latent + encode/decode codec | Stage 1 (modality-blindness / compressible space wanted) |
| Store + one-shot/rare-experience recall | when the store enters |
| Tracing, multi-step reach | Stage 1 (across-span chaining) |
| Cross-cortex completion from impoverished cues (= char-11 priming) | when the store enters, or the environment first produces impoverished bundles. **Kept structurally available now** by the loss's sparse/one-sided/near-all cue-shapes. |
| Segmentation, replay, vividness/creativity | Stage 1+ |
| **Multi-entity** within-bundle association (multiple objects per frame) | when vision emits separable entity-structure. *(Single-object vision↔word completion is **live**, §1/§2.)* |
| Wave↔cortex-rate aliasing | adding a cortex whose rate differs sharply (audio 100–500×) |
| Motor / agency, reward / salience / affect | out of scope — must remain **extensible** toward priming and surfacing-for-arbitration, never foreclosed |
| Sleep consolidation | much later (the one legitimate phase) |

---

## 12. Discipline to hold during the build

- **Non-causal masking** — causal makes PAM a forward predictor wearing a mask (exp02: 0.062 vs
  1.000).
- **Block-level masks** — mask whole slices, never scalar coordinates (scalar = masked-autoencoder
  leak).
- **Within = whole / across = trace** — within a span, material surfaces *whole*; only across spans
  a trace. At Stage 0 there is no store / no across-span trace; the live face is **the completion act
  is at-once, not stepped.**
- **No planner-bolt** · **no store-as-overseer** · **efficiency emergent, never an objective.**
- **Operator-form open** — **no softmax-attention**, not a masked transformer; the spec canonizes no
  form; CC proposes the minimal instance and **surfaces it for review**; the basin-hosting screen is
  **design-time and subtractive** (single exclusion).
- **Pinned constants are pins, not stand-ins** — word encoder frozen, activity-gate=1, gain gates
  off, W=3.
- **Test against the twelve functions, not vocabulary.**
- **Stage-3 flag (specific):** the loop can succeed for the wrong reason. Each readout's pre-
  registered baseline-gap is the guard. **Flag any MVP result that appears to succeed while quietly
  violating a characteristic.**

---

## 13. Three rates — keep separate (they want to blur)

| Rate | What it paces | Run-1 setting | Owner |
|---|---|---|---|
| **(1) unpool clock** | capacity opening | fixed (gate pinned to 1) — **the only deployed rate** | maturational |
| **(2) gain ramp** | how hard evocation presses | fixed-and-swept, both gates off, bound off | attribution-control |
| **(3) curriculum rate** | when the parent adds contrast | confidence-triggered | environment (external) |

**Stimulation curriculum (external loop).** A hand-supplied parent reads system confidence and adds
the next **contrast** word when a vision/word pairing goes confident. **External, not a PAM
mechanism** (preserves no-external-objective). **Contrast-not-rename:** a new word with no
contrasting pair present = a consistent gradient = a rename, no split; differentiation needs the
contrast **present in experience** (cricket-ball vs not-cricket-ball, both labelled). The external
face of the cue-shape / gap-3 mechanism already in the loss.
