# Progress Log

Chronological record of the isolation experiments (the "bridge rungs" between paradigm and
the Stage-0 MVP). Each is a falsifiable rig with **pre-registered failure conditions** that
are not softened after seeing results. Detail lives in each experiment's `SPEC.md` /
`RESULTS.md`; this log is the one-screen status + verdict.

Convention: rigs are CPU-only, deterministic, and isolation-only (the single learned
component is the thing under test). A pass *licenses proceeding*; it does not validate the
mechanism inside the full loop (that is the MVP's job).

---

## exp01 — Pooling substrate  ·  PASS  ·  commit c58216a

`experiments/01_pooling_substrate/`. Does soft-tied weight pooling actually pool / unpool /
re-pool? Synthetic hierarchical Gaussians; the only learned part is the pooling classifier.

- **Pre-registered failures:** A — soft-tied members fail to differentiate (symmetry never
  breaks); B — gradual unpool does not beat the always-pooled cap on the fine task; C —
  re-pool destroys the coarse value instead of coarsening gracefully; D (obs) — the
  pull-apart signal does not behave as theorised.
- **Outcome:** all hold. Hard-tie control genuinely fails (chance), soft tie differentiates,
  gradual unpool reaches the unpooled ceiling while always-pooled stays capped, re-pool is
  graceful. Key design call: **nearest-prototype readout, not a free linear head** (a free
  head leaks the fine distinction through shared pooled weights — the §0 false-negative).

## exp02 — Non-causal masked completion (order-as-INDEX)  ·  PASS (flagged)  ·  commit 4efa90d

`experiments/02_masked_completion/`. Non-causal masked completion gives random-access
fill-in (cue-end → recover-begin in one pass); the causal forward control fails by
construction. Family: begin↔end bijection + interior = h(begin) non-injective +
position-varied symbols.

- **Pre-registered failures:** order-as-content fails if non-causal suffix→begin ≈ chance
  while prefix is high; discriminator invalid if the causal control also passes suffix→begin;
  at-once fails if iteration beats the single pass.
- **Outcome:** non-causal suffix→begin = 1.000, causal = 0.062 (chance), single pass
  suffices. Key lesson: **training masks must sample the full cue-shape distribution**
  (uniform number of cued positions) or the operator learns gap-filling, not random access.
- **Flag:** this rig uses an **explicit position index** — order-as-*index*, the unvalidated
  crutch. exp03 removes it.

## exp03 — Order-as-CONTENT falsification gate  ·  PASS (incl. stacked corner)  ·  commit 4a91416 (+ stacked-corner follow-up)

`experiments/03_order_as_content/`. Removes exp02's index crutch: position is carried by a
**drifting** (σ>0), **shuffled** (no array axis), **entangled** (α→1) signal. Does
random-access masked completion (cue-end → recover-begin) survive? Two orthogonal easy-outs
swept past, not pinned: σ (σ=0 = clean index) and α (α=0 = separable side-channel). Faithful
deployed corner = **high-σ ∧ high-α**.

- **Pre-registered failures:**
  - **F1** array-axis reliance — random access drops under shuffle even at low σ.
  - **F2** index-in-costume — high only in the clean-coordinate zone (σ→0), drops as σ enters
    the overlap band while aggregate order is still recoverable.
  - **F3** not at-once — iterative refinement materially beats the single pass.
  - **F4** separability-dependence — high at α=0 but collapses as α→1 while the drift signal's
    §4 validity checks still hold.
  - Boundary (NOT a failure): where aggregate order itself is unrecoverable (data ceiling).
- **Core outcome (single-seed gate):** OVERALL PASS. F1 (Primary tracks the recoverable
  oracle in-band; axis exploitable in Control B), F2 (tracks oracle through the overlap band),
  F3 (whole window in one forward pass), F4 (survives to α=1), Control A positive control, and
  a **carrier-ablation gate** (zeroing the carrier collapses begin-recon → position-reading is
  load-bearing, not the content bijection) all hold.
- **Process:** built via a design panel + two adversarial-review workflows. The review caught
  and we fixed, before commit: a **vacuous F4** (drift injected along a content-free axis,
  best-linear-read R²=0.99 → not entangled; fixed by injecting along the codebook's top-PC at
  content-matched scale → R²≈0.80) and an **OOD-confounded F3** and a content-memorization gap.
- **Stacked corner (the faithful regime, multi-seed follow-up):** the α-sweep was re-run at
  the band **edge σ=0.8 (~11% overlap)**, stacking overlap and entanglement, with independent
  2D-ceiling probes. At (σ=0.8, α=1): operator begin-recon **0.821 ± 0.012** (3 seeds), flat
  vs the α=0 edge baseline 0.809; the independent MLP probe recovers order **0.848 ≈ oracle
  0.847** (a fixed OLS probe gets 0.681 < oracle, confirming genuine entanglement). Pre-
  registered reading ⇒ **FAITHFUL CORNER VERIFIED** (order extractable AND operator uses it).
  Multi-seed headline confirms the margins; the single-seed Control B σ=1.5 dip was seed noise
  (multi-seed Control B = 1.000 ± 0.000 at every σ). See `RESULTS_stacked.md`.
- **Caveats (honest):** the operator is a within-window comparator that retains some absolute-
  scale sensitivity (not fully scale-invariant); 3 seeds; σ* in the core run sat at the
  low-overlap end (now closed by the σ=0.8 stacked corner).
- **Licenses:** proceeding to the Stage-0 MVP with **order-as-content** (carrier at α=1 /
  entangled, σ>0). Does NOT validate order-as-content under co-developing encoders + pooling +
  convergence-driven drift — the MVP integration test.

---

## [2026-06-23] Stage-0 build-blockers resolved in design; initialisation closed

Design session. All four §11 build-blockers are now **resolved in design** — the Stage-0
MVP is fully specifiable. Validation of these resolutions is the **MVP run itself** (they
are loop-level claims, not isolation-testable per §9). No code this session except exp03
(logged separately).

**Blocker — component count [RESOLVED: latent OUT for Stage 0].** PAM runs masked completion
directly on **concatenated cortex-space**; the distinct PAM latent is deferred to Stage 1+.
Resolved *against the success signals*, not by picking the simplest build: gap-3 (convergence
error shaping vision) does **not** need a distinct latent — masking a slot and evoking it from
the sibling, then backprop through concat (identity, differentiable) into the encoders, carries
joint-association pressure regardless. What the latent buys (char-10 modality-blindness, a
compressible associative space) are **not** Stage-0 signals; concatenation already preserves
**own-space** (the harder half of char 10) and defers only blindness. Second reason: the codec
is a *second* co-developing matched pair (encode↔decode round-trip) whose decode job is
store-compatibility — no store at Stage 0, and it doubles the attribution surface. Honest
deferral of modality-blindness, **not** a char-10 violation.

**Blocker — PAM per-wave loss [RESOLVED in shape].** (wave, slot) cells over a **W ≥ 3** window
of concatenated bundles. Each wave: slide the window one, draw a mask from the **full cue-shape
distribution** {single-slot, whole-wave, interior-both-sides, one-sided-edge, sparse, near-all},
run **one** completion pass, take **one** gradient step — distribution sampled across **time**
(this is what holds it online / phase-free). Target = the **actual emitted content** of the
masked cells (the encoders' own outputs; self-supervised) = evoked-vs-actual = **convergence
error**. Loss = **embedding-distance on masked cells only**, distance-based (exp01 readout
constraint), no free linear head. Reconciliations: "in latent" → "in concatenated cortex-space";
"non-causal" is **vacuous within a wave** (no internal order, char 1), so it **forces W ≥ 3**
across waves — within-wave completion (char 2) is the single-wave sub-case, across-wave
non-causal (char 3) is the point, and **Stage 0 is the PAM-setting test exp02 deferred**. The
operator's internal form stays **open** (denoising pass / attractor settling / PC inference) —
must not become a masked transformer; exp02's at-once check evaluates a **single** completion
act. Cue-shape sampling (exp02 rule #3) is mandatory or it learns gap-filling, not random access.

**Fork inside the loss — collapse-control / stop-grad [RESOLVED: no stop-grad; anchor +
SIGReg-style spread].** Standard collapse-control stop-grads the target; but gap-3's
differentiation pressure *is* the **target-side gradient on the masked vision slot** (coarse
"ball" emitted as target, convergence-vs-evoked push, contradictory across red/green instances =
§4 intra-group disagreement → unpool consumption) — so target-stop-grad severs exactly the path
Stage 0 exists to observe. Resolution decomposes collapse-control by **reference-and-relaxation
(structural / kinetic)**: the **anchor** (fixed pretrained word encoder) guarantees *target
diversity* on word-as-target maskings → removes collapse as a global optimum (**structural**;
replaces stop-grad's non-moving-target role **without cutting gradient**); a **SIGReg-style spread
constraint on vision** keeps the vision marginal diverse on vision-as-target maskings and repels
early collapse (**kinetic**) — **without** stop-grad, so the gap-3 target-side gradient survives.
Net: **drop stop-grad, keep an active spread term.** SIGReg verified this session — it is from
**LeJEPA (Balestriero & LeCun, Nov 2025)**, *not* V-JEPA 2 (prior summary mis-attributed it);
characteristic-function matching toward an isotropic Gaussian over random 1D projections; no
stop-grad / no EMA. "Target diversity ⇒ no collapsed global optimum" is a 2026 VJEPA-variant
theorem. **Caveat:** LeJEPA + follow-ons are Nov 2025–Mar 2026; treat quantitative claims as
provisional; the *class* (distributional spread, no stop-grad) is multiply reproduced.
**Pre-registered asymmetric falsification (= success-signal-4):** degrading the anchor must
collapse the **word-as-target half specifically** — collapses-everything (spread wasn't holding
the vision half) or collapses-nothing (anchor wasn't holding the word half) both **falsify the
decomposition**. **Attribution watch:** SIGReg (→ isotropic spread) and pooling differentiation
(→ tight clusters) act on the same vision outputs; if differentiation underperforms, check whether
they share a vector and **interpose a projector** (SIGReg on a throwaway projected head, pooling
on the emitted backbone summary).

**Blocker — order representation [RESOLVED: order-as-content; VALIDATED in isolation, exp03].**
Order-as-index (oracle external label) vs order-as-content (internal σ>0 OU-drift signal) are
different *suppliers* of position, **not** two strengths — index→content is a mechanism swap,
disqualified as a stand-in. Order-as-content adopted: position carried by **genuine OU drift**,
σ pinned **low-but-nonzero** (build-full/pin/release on the drift *dynamics*). Carrier
**dedicated-but-drifting** for rung 1, with an **entanglement fraction α** as a continuous knob
(`x_i(α) = [c_i + α·P(d_i) ; (1−α)·d_i]`, the *same* OU source relocated) — so **α=0 (separable)**
and **σ=0 (clean coordinate)** are both degenerate corners to **sweep past, not pin**. Two
orthogonal easy-outs (σ, α); faithful corner = **high-σ ∧ high-α**. **exp03 PASSED**, then the
stacked-corner re-run also PASSED: all F1–F4 + controls; the faithful corner (σ=0.8, α=1)
verified **directly** — operator begin-recon 0.821, independent MLP probe 0.848 ≈ oracle 0.847,
fixed OLS probe 0.681 < oracle (the tell of genuine entanglement); 3-seed. The rig caught its own
**vacuous F4 near-pass** (drift injected on a content-free axis, R²=0.994 → re-injected on the
codebook's top PC, R²=0.80). Licenses Stage 0 with order-as-content (entangled, σ>0); does **not**
validate it under co-developing encoders + pooling + convergence-drift (MVP). **Residue:** the
operator reads order as a within-window comparator with **residual scale-sensitivity** — deployed
drift has no controlled scale, so the MVP must re-examine this.

**Blocker — initialisation [RESOLVED].** The t=0 *stable-vs-smooth* fork dissolved: vision starts
**near-fully-pooled but CONVERGED at that depth** — a functioning coarse vision system that
reliably emits the same embedding for the same blob. This gives PAM a **stable coarse target**
(stable because *converged*, not frozen — no char-8 crutch; the space still drifts as it unpools)
with **no cold-start wobble** (the coarse system is done settling before PAM begins associating).
Already-fixed pieces: word encoder pretrained-stable (the anchor); drift carrier starts its OU at
σ>0 (not plastic, no cold-start); gain ramps from 0; PAM cold-starts off structured inputs (needs
only sane scale — its reference is the cortex spaces, not its own seed).

*Gain ramp [RESOLVED]:* build gain **confidence-gatable AND capacity-boundable** in structure;
**pin both OFF for run 1** (pure fixed ramp) and **sweep the rate** (deliverable = the response
curve, not a tuned value); the capacity bound enters at **release**. The **inert-error correction**
(this session): unresolved contrast is **not** inert — its gradient flows and lands on the
**coarse** weights it can reach = **corruption pressure on the seeded coarse target**. So the safe
condition is a property of **gain** (how hard error presses vs *current capacity*), not of the
curriculum. Confidence-gating *raises* gain exactly when it's dangerous (PAM confident while
vision has no capacity); **capacity-gating** holds it down → the **safer release gate**. The bound
is left out of run 1 because (a) it is **moot by construction** (slow ramp + first-order unpooling
⇒ gain is small early), (b) it adds coupling that breaks clean attribution, (c) the readout
catches the mode anyway.

*New Stage-0 component — stimulation curriculum (external loop).* Stage 0's impoverished
environment (single scene, fixed vocab) needs a hand-supplied **parent**: it reads system
confidence and adds the next **contrast** word when a vision/word pairing goes confident.
**External, not a PAM mechanism** (preserves no-external-objective). **Contrast-not-rename rule:**
a new word with no contrasting pair present supplies a *consistent* gradient = a **rename**, no
split; differentiation needs the **contrast present in experience** (cricket-ball *vs*
not-cricket-ball, both labeled, gradients point apart). This contrast requirement is the **external
face** of the cue-shape / gap-3 mechanism already in the loss. The deployed system doesn't build
this — its rich environment + parent does it naturally.

*Three rates, held separate* (they want to blur): **(1) unpool clock** — capacity opening, the
only *deployed* rate (maturational); **(2) gain ramp** — how hard evocation presses (pinned-swept
run 1, capacity-bound at release; attribution-control); **(3) curriculum rate** — when the parent
adds contrast (confidence-triggered; environment).

*Success-signal-2 split readout.* Same observable (vision differentiating a visually-salient vs a
word-relevant axis), two readings split by **whether the word is present yet**: **persistent**
salience with the word present and contrast available = **gap-3 FAIL** (evocation shaped by the
wrong teacher); **transient** salience while the word is still pending = **NORMAL**, and the
**curriculum's signal to advance the word side** (a child asking about something it has no word for
is not a fault). The naive reading (salience = gap-3 broken) would throw false failures across
run 1.

**Next:** write the Stage-0 MVP build spec (in a fresh chat, opening from the updated state doc),
with the §11 success signals — including the split readout above and the asymmetric anchor
falsification — pre-registered before the run, exp03-style.

---

## 2026-06-25 — Stage-0 MVP built (Phase-1 core)

**Built the first integration** from `STAGE0_MVP_SPEC.md`: vision pooling cortex + frozen
word cortex + a non-causal **prototype-resonance** associator, fused in one wave loop.
Shared, validated primitives promoted into `src/loom/` (pooling, poolmetrics, order,
completion, spread); the Stage-0-specific rig in `experiments/04_stage0_mvp/`. Scope this
pass = **Phase-1 core** (validity probe, Readout G, Readout D, two structural signals);
Phase 2 (Readout A ladders), the gain sweep, and Readout O deferred per the spec's staging.

**Operator (surfaced & approved, §2-ii):** a single at-once **distance-kernel resonance** over
a second pooling-substrate population (the PAM weights), keyed by an order-as-content position
read (Fourier on a learned `pos_extract`). It replaces exp03's `nn.TransformerEncoder` — **no
softmax-attention, no free head, no PAM latent** (in_dim == out_dim), basin-hosting (content
sits on the pooling substrate).

**Build-correctness — all guards pass** (static + every eval window): word anchor frozen
(param-delta = 0); **no detach** on the PAM target (gap-3 target-side gradient reaches the
masked vision slot — vision-from-PAM and vision-from-JEPA both nonzero); block-level whole-slice
masking covering **all six** cue-shape families; order-as-content never order-as-index (live
carrier max single-coord R² < 0.9 every window — gated on the within-window no-clean-slot test,
with a cumulative content nuisance confound on `u`); one code path (char-7). Pre-registration
self-tests pass (every named verdict outcome incl. WRONG_REASON; cue-shape coverage).

**Headline — gap-3 is present.** The deliverable is the gradient-attribution split:
`vision_grad_from_PAM` is **nonzero every eval window** (PAM's convergence error reaches the
masked vision slot, no detach — gap-3 wired and active), magnitude **order-1 vs JEPA**
(cross-seed mean ratio ≈ 0.8×; rises in late windows; *not* robustly dominant — "present and
comparable," not "PAM does N× the work"). Everything below is *isolating* it, not whether it's there.

**Results (3-seed `--quick`, honest):**
- **Readout D: PASS-LINEAR-REGIME (a QUALIFIED pass, not a clean PASS)** all seeds — order *is*
  recovered in-loop (order-recovery ≈ 0.77 ≫ chance 0.33) and **carrier-zero collapses** it,
  **but `full_ols_r2 ≈ 1.0 ≥ 0.9`**: a full linear read recovers the drift → the **linearly-
  separable** regime, not exp03's *entangled* corner (0.80 at α=1). Cause: the dwell-stable fix
  froze A/B within a dwell, leaving drift as the only within-window variation. The single-coord
  no-clean-slot gate (`max_coord_r2 < 0.9`) still holds; carrier-zero collapse is
  necessary-but-not-sufficient (`full_ols_r2` is the tell). **Entangled corner DEFERRED.**
- **Structural #1 (char-7) PASS; Structural #2 (pooling does something) PASS** — capacity
  opens ~8–14× from pooled. **OBSERVATION: SPREAD_FIGHTS_POOLING** (intermittent; §5 watch).
- **Readout G (gap-3 fusion): seed-unstable / WRONG_REASON** — B rises (intact > no-word) but
  the matched no-word arm **also** rises. Cause = genuine **autonomous** B-resolution (B is in
  the visual input; JEPA + the unpool clock open capacity); **leak ruled out** (null token
  B-agnostic, schedules independent, stream matched). Read the gap **paired & sustained** (a
  single-window inversion, e.g. seed 1, is no-word eval noise). **build-failure invariants: NONE.**

**The build is correct and gap-3 is present (path alive); what's open is (a) cleanly isolating
gap-3 from autonomous resolution and (b) the entangled (vs linearly-separable) order corner.**

**Next — open on the DESIGN FORK, not a build.** Cleanly isolating gap-3 requires making
`floor_B` genuinely **autonomous-unreachable** so the matched no-word arm stays in the floor-band.
This must be **re-calibration of the existing regime — NEVER a new mechanism that gates vision
from learning B except via the word.** A gate would *manufacture* gap-3 (measuring an effect you
built in) — the wrong-reason failure. Legitimate suppression keeps B autonomously *representable*
(the capacity-open oracle, no word, still recovers B) but not autonomously *acquired* in-run.

Two knobs, both **pinned constants** — *surface for review before changing anything*:
- **(band) — recommended, first.** Deepen B's subtle band (`r_fine`↓ / `sigma_stim`↑) so the
  coarse-autonomous encoder + JEPA genuinely cannot find B (`floor_B`≈chance *even with capacity
  open*), while the word-taught `ceiling_B` stays high. exp03's σ-band logic applied to B, selected
  **pre-loop via the validity probe**. Cleanest single-variable change; directly targets
  "autonomous-unreachable." Risk: too subtle → even the word can't teach it (ceiling drops, gap
  closes); the validity gate (`floor_B`≈chance ∧ `ceiling_B` high) is the guardrail.
- **(clock) — secondary lever.** Slow the unpool clock (`t2` / unpool rate) so capacity opens
  late enough that autonomous resolution cannot complete in-run while the word's contrast-aligned
  gradient still drives differentiation. Risk: too slow → B never resolves at all (BOUNDARY).

**Discriminator (legitimate re-calibration vs the manufacture-gap-3 trap):** after re-calibration
the **no-word capacity-open oracle must still recover B** (B remains representable — merely not
acquired by vision-without-word), and there is **no gate/stop-grad** forbidding vision from
learning B without the word. The same vision encoder *plus* the word CAN learn it.

**Standing Readout-D debt (carry forward):** Readout D is **PASS-LINEAR-REGIME**, not clean —
`full_ols_r2 ≈ 1.0` (linearly-separable). Re-test the **entangled corner** (`full_ols_r2 < 0.9`,
exp03 hit ~0.80 at α=1) the **moment within-window content drift returns** (a 3rd within-dwell
content axis along `u`, or the deployed moving-content regime). The band/clock work is a
Readout-**G** change and does not discharge this **D** debt.

Then (downstream of the fork): §5 throwaway projector for SPREAD_FIGHTS_POOLING; Phase 2 (Readout
A ladders) + the gain-rate sweep.
