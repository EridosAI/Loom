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

**Next — post-Phase-1 reframe (2026-06-25 addendum; full record in PROJECT_STATE §12).** The
post-Phase-1 read shifted the next-session framing from "pick a knob to make Readout G go clean"
to **characterise the developmental curve**. Three items:

- **(settled) gap-3 developmental shape = S-curve [hypothesis to characterise].** Toe (single
  word↔blob associations, gap-3 pressure low-ish even as words land) → rapid phase (concepts build
  on concepts; **PAM-grad share should rise above JEPA's if the paradigm bet holds — the real
  test**) → plateau (efficiency cycling). The order-1 PAM/JEPA ratio at Phase-1 is consistent with
  sitting in the *toe* (not yet evidence either way). The deliverable is the *curve*; a clean
  Readout-G window is one point on it, not the goal.
- **(settled) slow-start unpool ramp [architecture addition, §12.B].** The unpool clock should ramp
  slow→fast (reference-and-relaxation: words must stabilise against what vision already sees before
  unpooling splits the blobs). **Build-full / pin-constant for the short Stage-0 runs (no
  behavioural change now) / release when runs get long.** Principled *pacing*, NOT gating — distinct
  from the manufacture-the-effect trap. Supersedes §4's "gate pinned to 1" note *in principle only*.
- **(next session — open) characterisation sweep — NOT "make Readout G go clean."** Coarse sweep
  **both knobs together** — band (`r_fine`↓/`sigma_stim`↑) × unpool-rate — **instrumented to log
  PAM-grad/JEPA-grad share across the trajectory, not at a checkpoint**; deliverable = the
  **response surface** (as the gain ramp was handled — the surface *is* the result). Read off:
  (a) does a clean Readout-G window open anywhere; (b) does PAM-grad share rise through the rapid
  phase; (c) is the shape an S-curve. **Lightweight pre-registration** of the expected shape before
  running (so it stays a measurement, not shapes-read-into-noise). Finalise in a fresh design chat,
  then hand to CC.

**Still binding (carried):** the knob work is **re-calibration of the existing regime, never a
gate that lets vision learn B only via the word** (manufactures gap-3 = wrong-reason). Discriminator
= the no-word capacity-open **oracle must still recover B** (representable, just not acquired); no
stop-grad. The slow-start ramp passes this by construction (it paces the clock, not representability).

**Standing Readout-D debt (§12.D):** PASS-LINEAR-REGIME, `full_ols_r2 ≈ 1.0`. Re-test the entangled
corner (`full_ols_r2 < 0.9`, exp03 ~0.80) the **moment within-window content drift returns** — it
resolves for free when the deployed space genuinely moves. The band/clock sweep is a Readout-**G**
change and does **not** discharge this **D** debt.

Then (downstream): §5 throwaway projector for SPREAD_FIGHTS_POOLING; Phase 2 (Readout A ladders) +
the gain-rate sweep.

## 2026-06-25 — Characterisation-sweep knob fork CLOSED (design pass; no code)

Design session. The §12.C knob fork is **resolved**; finalised sweep design written to
`docs/STAGE0_CHARACTERISATION_SWEEP_SPEC.md` (exp03-style; CC builds from it). No code this session.

**Fork closed: which knob(s).** Resolution = **asymmetric band-dense × rate-coarse**, not a
symmetric grid. Band (`r_fine`↓ / `sigma_stim`↑) is the dense search axis (moves the
autonomous-vs-associative balance = what Readout G measures); unpool-rate is a coarse locator (two
constant rates, tempo only). A symmetric grid would entangle balance with tempo — the gain-ramp 1D
attribution-blur.

**Compute-is-free corrections folded in** (nothing rushed; runs take as long as needed):
- **Fast unpool-rate cell dropped** — its "get out of the toe" rationale was a cost substitution;
  with compute free, lengthen runs (`T_run = 1.25·T95`) so a moderate/slow clock traverses
  toe→rapid→plateau on its own clock. The toe's length is part of the S-curve hypothesis; a fast
  clock would never measure it. Also dissolves the §12.B "faster is good" tension.
- **Band axis made genuinely dense** (≥10 steps, not 3) — the transition shape (sharp vs gradual
  autonomous fall-off; oracle-loses-B cliff vs clean-G window; plateau vs knife-edge) is the
  scientific content; freed compute goes here first.
- **Seeds become an instrument** (≥20/cell) — Phase-1's G ambiguity was seed-instability;
  deliverable shifts to "in what fraction of seeds, how sustained," converting the uninterpretable
  thing into a measurement.

**Calibrate-don't-guess (the spec's central discipline).** Every scale-dependent threshold is
`[RECONCILE]` — set from the live rig on the run commit, not by feel. **Step 0 = B00 oracle
calibration**: on current HEAD, measure chance / intact-ceiling / oracle-ceiling, set
`oracle_threshold = chance + margin` below the easy-band ceiling. The oracle floor sets the band
cap, so a guess either never fires F3 (no cap) or caps inside the clean-G window (deletes the
result). Phase-1's numbers explicitly barred (ran a94863e; sweep may run on a different commit).

**Verdict operationalised** (not eyeballed): `pam_grad_share` (bounded) + `pam_jepa_grad_ratio`
across the trajectory vs `capacity_fraction` (primary cross-rate axis). S-curve signature =
pre-registered inequality over the seed distribution (`delta_rapid > 0 ∧ delta_plateau ≤ tol`).
clean-G sustainedness pinned as a rule; `autonomous_resolution_frequency` = F2/F4 discriminator;
F1–F4 pre-registered; every row carries `commit_hash` + `spec_hash`.

**Still binding (carried):** re-calibration of the existing regime only — never a gate letting
vision learn B except via the word (wrong-reason); discriminator = no-word capacity-open oracle
must still recover B; no stop-grad. Constant unpool-rate = coarse S-curve locator, orthogonal to
§12.B's ramp (**pinned off for the sweep regardless of run length**), not a pacing finding.
Readout-G change; does NOT discharge the §12.D Readout-D debt.

**Next (CC):** read the spec → confirm HEAD → run Step 0 (B00 oracle calibration on live commit) →
**surface the calibrated `[RECONCILE]` values + resulting band ladder for review** (not the knob
choice — settled) → then build. Pre-register F1–F4 + the phase-metric inequality before any run.

---

## 2026-06-26 — Characterisation sweep RUN → EMPTY-GAP (gap-3 wired but inert)  ·  runs on 2b70d74, spec_hash d1f0936c92e1

Built and ran the sweep (`experiments/04_stage0_mvp/{oracle_probe,calibrate_step0,band_ladder,run_sweep,
sweep_metrics,analyze_sweep}.py`; 480 runs = 12 bands × 2 rates × 20 seeds). Full read in
`SWEEP_RESULTS.md`; surface in `figures/response_surface.png`. Verdict folded into PROJECT_STATE §9.

- **Verdict — pre-registered EMPTY-GAP; not F1–F4; not a rig failure.** `cleanG_frequency = 0.00` at
  every one of the 24 cells. Decisive, **calibration-independent** measurement: gap-3 **lift** =
  `intact_B − noword_B ≈ 0` across all cells (range −0.004…+0.048, mean ~0.01, SE≈0.013, no consistent
  cross-rate sign); arms decline in lockstep, never separate.
- **Not F2** — autonomous resolution genuinely falls 1.00 → 0.00 (transition r/σ≈4–5). **Not F3 —
  B is representable** across the whole admissible ladder (substrate oracle ≥ threshold; F3 cap at
  r/σ≈1.0). The failure is **"word doesn't teach a representable B," not "B unrepresentable"** — the
  sentence the oracle/raw separation was built to license; it makes the negative *clean*, not
  manufactured-gap-3.
- **Methodological lesson (most reusable — do not lose):** PAM-grad **share** rises through the rapid
  phase (s_curve_sig 0.80–1.00) but is **non-discriminating** — identical at easy bands where the word
  is provably inert. The rise is real **and a false success signal**; **acquisition lift is the
  load-bearing metric, and it's null.** Share-only trajectory instrumentation would have called this a
  paradigm-positive S-curve.
- **Mechanistic:** gap-3 wired (gradient reaches the masked vision slot; share≈0.6, rising) but inert
  for acquisition. Sharpens Phase-1's present-but-weak / WRONG_REASON into a clean negative across the
  full surface.
- **Scope (both halves):** a sharp, useful negative at the **Stage-0 operating point** (two cortices,
  no store, single scene, weights-only); **not** a falsification of the mature claim
  (concepts-on-concepts, store-fed rare associations, multi-cortex coherence).
- **Caveat (scoped, not verdict-provisional):** Δ2 grows unbounded at λ2=0 (depth 0.73→1.15→1.37);
  bounds the S-curve-shape / developmental-clock claims, not the lift (null at every depth). Candidate
  substrate fix for the design table: a saturating-capacity / re-pool clock.
- **Live frontier (design-table call, NOT CC):** can't yet distinguish **(i)** Stage-0 too impoverished
  (no scaffolding to teach from → rapid phase never created → do the Stage-1 increment) vs **(ii)**
  mechanism inert at the centre (→ rethink). **Discriminating test:** re-run the lift metric once
  cross-concept scaffolding exists (first Stage-1 increment) — still-null ⇒ (ii); appears ⇒ (i).
- **Why trustworthy (provenance):** oracle gate's original directional criterion **falsified by data**,
  re-pre-registered to divergence+content-driven, superseded gate kept in canon (exp03 vacuous-F4
  discipline); Step 0 surfaced the **~3× run-length shortfall** (Phase-1 at ~28% of plateau —
  quantitative confirmation of §12.A "sitting in the toe"); **verdict frozen in spec_hash before the
  surface existed**; convergence checked across depth 0.73→1.37 (MODERATE-vs-SLOW + 3.4×-length
  extended run at b7/b8: lift −0.014 / −0.011).

**Next:** the (i)/(ii) fork is the design-table's, not a CC sweep — the discriminating move is the
deferred **Stage-1 increment** (store / third cortex / richer environment), then re-run the lift
metric. §12.D Readout-D entangled-corner debt remains undischarged (untouched by this Readout-G sweep).

---

## 2026-06-29 — Stage-1 attention-sculpting rig BUILT; blocked on a dead evocation channel (gating precondition)

Built the Stage-1 rig from `STAGE1_ATTENTION_SCULPTING_RIG_SPEC.md` at `experiments/05_attention_sculpting/`
(constant Δ2 re-pool / G3 = `src/loom/constant_repool_delta2`, λ2/Δ1 untouched, **not** exp01's λ2-raise;
4→8 conflict stimulus; category oracle; Step-0 (a)/(b)/(c); conflict-strength ladder), with only
behavior-preserving hooks added to the `[SETTLED]` exp04 (backward-compat verified). **Step-0 (a)/(b)
pass** (vision-alone occupies the salient distractor 0.95 / neglects the subtle category ≈chance;
category oracle-representable + ablation-guarded). **(c) is blocked**, and the root is upstream:

**BLOCKER — the operator's evocation channel is content-dead in the deployed regime** (4-lens adversarial
panel, unanimous; content-agnostic neutral (d)-gate). PAM prototypes collapse to a point (spread
6.8e-3→~1e-10, all seeds, from ~t=300) → `z=pa@Wp` content-invariant → gap-3 is a member-invariant
constant pull (the gradient reaches the target but carries no information). The contained operator-side
fix (authorised, scale-robust, minimal-DOF, no dial, content-agnostically validated) was pursued **to
exhaustion** — init-rescale / window-center / carrier-DC-removal / **stimulus-side carrier-bound** all
gave no revival; only a stack (cosine + pam_lam=0 + init + 2× training) reached ~15% capacity. Candidate
levers (carrier scale × pool penalty × diffuse multi-member signal) **each insufficient alone, causal
structure undetermined**; the clean-2-member (d≈1.27) vs diffuse-deployed (dead) gap is under-decomposed
(task structure may be the real lever). exp03's pre-flagged comparator scale-sensitivity (RESULTS.md:120-126)
has **come due** but is **necessary-not-sufficient** (bounding the carrier alone doesn't discharge it).

**Empty-gap re-read (sharpening, not retraction):** the channel was never live in any Stage-0 config →
Stage-0 gives **zero bearing on (i)/(ii) in either direction**; the fork is **unasked** until a
channel-live rig exists. `lift≈0` stands; scope collapses to "vision doesn't need the word for a
resolvable distinction." **Evocation-as-teacher is wholly untested.** Full brief: `FRONTIER` §10 /
PROJECT_STATE §12.E. The (d)-gate rejected a manufacturing-shaped init=1.0 `clamp` false-positive before
canon — the apparatus working, not the project failing.

**Next:** design-table decision on reviving the deployed evocation channel (operator/PAM-substrate, possibly
completion-task redesign), informed by the undecomposed levers; exp06 to be designed *from* the brief, not
instead of it. The neutral (d)-gate is the pre-registered liveness pass any redesign must clear. No code
beyond the built (uncommitted) rig; nothing committed.

## 2026-06-29 — exp06 channel-revival factorial → LEVER DETERMINED: JOINT {cue-diffuseness, pool-penalty}  ·  gate commit 335f36d, spec_hash c1c56cbd9cb6

`experiments/05_attention_sculpting/` (exp06_factorial.py, dgate.py, exp06_gate_validation.py,
exp06_interior_read.py, exp06_reconfirm.py). The decompose-first factorial that **named the redesign
direction** for the dead channel (the design-table fork from the 2026-06-29 blocker entry above).

- **Design.** 2×2×2 over **member-count × cue-diffuseness × PAM pool-penalty**, carrier **bounded as the
  necessary-not-sufficient baseline in every cell** (so it is NOT a factor). Measured by the now-committed
  neutral content-agnostic **(d)-gate** (`dgate.py`, promoted from the exp05 design) — train a fresh op on a
  neutral M-member associative task under each cell's factors, measure associated-different separation
  (d_diff) with d_same + ablation guards. [RECONCILE] levels read programmatically from `SculptConfig`.
- **Pre-registered failures / gating (exp03 discipline).** Step-0 validity **triad resolved first and
  fully** (execution-order pinned: gates before any interior read; V3 before super-additivity): **V1** clean
  anchor live (d 1.41, d_same 0), **V2** dead anchor collapsed (d 0.000, proto 4e-7), **V3** ≥1 toggle
  traverses. **PASS** → committed standalone (`335f36d`) as a clean provenance point carrying **no
  direction-finding**.
- **Gate-validity probes (the 0.000's are real).** Collapse cells reach d=0 **and** proto=0 by step 200 and
  stay flat (not under-training); raw un-normalised member separation ≈0 with normal output norm and
  chance-level noise-decodability (not a magnitude artifact); d_same=0 on the live cells (genuine
  differential separation). Cue radii read from `SculptConfig` (provenance, not circular).
- **Interior read (§4/§5), adversarially verified (5 lenses, unanimous SURVIVES).** From the dead corner,
  undoing **any single factor** stays dead; undoing **diffuseness AND penalty together** revives (d≈1.1) —
  **super-additive** (1.005 vs Σ-singles 0). **VERDICT: JOINT LEVER = {cue-diffuseness, PAM pool-penalty};
  member-count tolerated-deployed** (a ~22% degrader, NOT a killer); 3-way irreducible-conjunction
  **rejected**. Kill-texture asymmetry (penalty point-collapse vs diffuseness near-collapse+residual) is
  characterisation only, kept out of the lever arithmetic.
- **Deciding cell re-confirmed at plateau (the fork hung on it).** [1,0,0] was unconverged at 4000 steps;
  re-run to 12000 (16 seeds): **d_diff plateaus flat ~1.09–1.11 from step 6000** (mean 1.106, mean−2·SEM
  1.040 ≥ threshold 0.967). **Convergence accepted on the d-mean:** prototype spread keeps growing in the
  live regime (clean does the same while its d is rock-flat) — **proto-flat is a DEATH certificate, not a
  LIFE one**, so (d) is the convergence signal for a live cell. Routing held (constituents stay hard-zero,
  soft cell stays out).
- **Direction (exp07).** **Re-pose PAM's COMPLETION TASK** as a joint, symmetric redesign over both lever
  factors — (a) how the cue is posed; (b) drop/reshape the λ2-tie on PAM's prototypes — **no penalty-first
  ordering**. Must clear the (d)-gate at the healthy bar **in the deployed loop** before Stage-1 (§8). The
  empty-gap **(i)/(ii) fork stays unasked** until exp07 revives the *deployed* loop (exp06 revives the
  *neutral probe* + names the lever). Full record: `FRONTIER` §10.7 / PROJECT_STATE §12.E.

## 2026-06-30 — exp07 Phase 0: cue-floor × penalty surface (MEASURED, not built)  ·  spec_hash in artifacts

`experiments/05_attention_sculpting/exp07_{config,core,step0,surface,ceiling_reconfirm,converge_off16,interior_read}.py`.
Measures the surface exp07's redesign is scoped from — read through the committed (d)-gate (`dgate.py`),
**no new operator/store**. Cue axis (flat-diffuse → content-blind re-posings → sharp) × penalty
`{off=drop, reshaped=preserve, deployed=collapse}`, member-count 16 + a card-2 probe. All knobs
`[RECONCILE]`d from the exp06 commit. **Step-0 gate (re-posing construction + separability/sanity +
corner-gate) surfaced and signed off before any interior read** (the standing gate).

- **`reshaped` (preserve) = the settled cortex StepSchedule on PAM's tie** (preserve = cortex-uniform
  machinery). **Two methodological traps caught + fixed before any verdict** (each would have manufactured
  a wrong-reason result): (1) single-clock δ1-penalty → irreversible collapse trap (reshaped couldn't
  revive) → cortex two-clock keeps group symmetry-breakers; (2) fractional clock-onset drifted later when
  the budget was extended for plateau → **absolute** two-clock onset (900/3600, budget-independent). With
  the fix reshaped revives across **all 10 seeds** at both cards — the earlier bimodality was the onset
  artifact, not intrinsic.
- **Interior read adversarially verified** (4 named-blind-spot lenses + synthesis: construction-dependence,
  floor-equivalence framing, onset-fix/plateau, topology invariance). Survives **directionally, no
  high-severity / false-PASS** (every confirmed error understates the reshaped cost, so no spurious
  "preserve" can be manufactured); **two framings that failed *as worded* were corrected in the artifact**.
- **FINDING 1 — cue recoverability floor≈0 is STRUCTURALLY FORCED + construction-scoped.** The re-posing is
  exactly global mean-centering and the deployed cue is ~100% common-mode (5.831·base over 0.5·Cd) → floor≈0
  follows from the construction, not training (near tautology). The **build-robust half** of the two-part
  cue fix (structured/native diffuseness) is **UNMEASURED**; common-mode-dominance is itself a probe
  simplification of the deployed rig (true floor may be >0).
- **FINDING 2 — penalty legitimacy = PRESERVE on the uniformity argument, at a measured cost (NOT
  "validated").** Both drop & preserve **revive** (liveness doesn't select). Robust deliverable = a
  **seed-paired SCALE-GROWING CEILING capacity cost**: off−reshaped **+0.103 @card-16 (paired t=2.84; off
  1.126 vs reshaped 1.023, both converged @36000), ~0 @card-2**. "Floor-equivalent" is **ruler-dependent**
  (own-sharp Δ0.027 yes; common off-sharp ruler — the one the artifact's topology uses — Δ0.103 NO) and the
  sharp-gap is **not significant** (t=1.48) → cost booked as a ceiling cost, not laundered out of the floor.
- **FINDING 3 — topology klass-invariant but trivially (deployed-dead-driven); discriminating off-vs-reshaped
  relationship NOT cardinality-invariant** (dead tie @card-2 vs significant @card-16) → **member-count
  modulates the tie's capacity cost** (exp06 liveness non-lever **scope-narrowed in place**: §10.7 /
  §12.E / memory — does not flip liveness, does modulate the reshaped tie's capacity cost).
- **Direction (scoped):** re-pose completion with content-blind cue re-organization (dominant for common-mode
  diffuseness) + the preserve open-and-stay-open tie (legitimate on uniformity; real scale-growing capacity
  cost; slower convergence). **Still unmeasured/open:** structured-diffuseness floor; *deployed-loop*
  revival; empty-gap (i)/(ii). Full record: `FRONTIER` §10.8 / PROJECT_STATE §12.E; numbers in
  `exp07_interior_read.json`.

## 2026-06-30 — Cue-floor (build-robust half) SHELVED with trigger

Caught that the **structured-diffuseness floor is a property of the static `ConflictStimulus` construction,
not the loop** — a now-vs-later problem we'd stopped questioning after the exp07 SNR work. **Deferred, not
abandoned;** trigger = **the loop test stalls on evocation signal capacity** (channel-carries-information
doesn't hold in the regime the loop test runs in) → the within-frame structured floor becomes load-bearing
and Phase-1 resumes with a measured reason. Reasoning: signal/clutter separation gets structurally easier
with the two mechanisms the architecture intends but we haven't built — **continual time** (earned salience)
and **multiple cortices** (cross-modal recovery) — so forcing one static frame to do it (PCA/whitening/block-
centre variance-matching-circular; only global-mean-centre is a fair instrument) asks a frame to do the
loop's job. **"Easier later" recorded as a prior, not a fact** (same status as the temporal floor). **CC's
read-only rig analysis banked as the pickup artifact** (structured decomposition, circularity ladder,
calibrated-synthetic + deployed-direct-validation design — Phase-1 spec scoped, not written; FRONTIER §10.9).
No code; `ac7ea57` stands as the last build.

## 2026-07-02 — Loop-test scoping fork RESOLVED in design → anchored-reference minimal rig

Design session; no code; `ac7ea57` stands as HEAD. The §10.10 opening fork (continual time
+ second cortex from the start, vs single-cortex minimal-first) is resolved: **one plastic
vision cortex against a FROZEN word anchor, continual time, both from t=0.** Load-bearing
grounds: **§7 signature** (occupancy-lag behind word-association acquisition requires the
word cortex to exist); **#12** (the anchor IS the stable reference, at its frozen limit —
single-stream has no reference and the loop doesn't start); **echo-chamber** (single-cortex
PAM's associative content is wholly vision-derived — evocation mirrors the encoder back at
itself; a mirror, not a teacher; structural, premise-free). Exogeneity **demoted to
supporting** (rests on the untested premise that vision's own objective would already split
the taught distinction). **No relaxation schedule in this rig** — frozen = pin-to-constant,
#12's stiff limit, no debt; relaxation enters only at the deferred mutual-sculpting release
stage. Binding scope check: **fixed encoding ≠ fixed association** — PAM still acquires
vision↔word (§7 lag intact). Metric = occupancy-lag **lift**, never share. Full entry:
`FRONTIER` §10.11 (+ §10.10 tail pointer, + PROJECT_STATE §12.E dated line). **Next:**
loop-test rig spec, pre-registered failures first; opening question = revise
`STAGE1_ATTENTION_SCULPTING_RIG_SPEC.md` vs fresh.

## 2026-07-02 — STAGE1 spec REVISED in place under §10.11 (no code)

Bindings swapped to the exp06/07 revival config ([RECONCILE] from ac7ea57). §L
deployed-liveness phase added: calibrated entry bar — the exp06 "healthy bar" line
SUPERSEDED on reference-category grounds (healthy = clean/card-2; deployed gate pinned to
config-matched calibration) — plus continuous channel column (channel treated as an
adaptive quantity; trajectory + covariates are a deliverable) and §10.9 trigger wiring.
Δt_offset sweep stands (availability-staging; presence from t=0 per §10.11). Δt_assoc
kernel arm added (piggyback, window-bounded, non-gating). Bars-amendment convention
recorded. Step-0 (a)/(b) to be re-confirmed on the run commit.

## 2026-07-02 — §L gate step 1: liveness CALIBRATION run; REVIEW GATE 1 = PASS

Built `experiments/05_attention_sculpting/calibrate_stage1_liveness.py` (reuse-only: one
code path over `exp07_core.cell_trajectory`; no reimplementation). Ran the NEUTRAL (d)-gate
at the deployed **revived** rig cell `16 / reshaped@(900,3600) / repose@1.0` (content-blind
global mean-centre cue; preserve two-clock tie; all knobs [RECONCILE]'d from `ac7ea57`),
20 seeds, read at the CONVERGED budget 36000 (12000 is pre-plateau/bimodal for this
slow-reviving cell). **bar = 0.8866 = reference 1.0813 − 2·(per-seed std 0.0973)**;
plateaued; ablated_max 0. Correctness: seeds 0–9 reproduce the exp07 converge cell
bit-for-bit (max_abs_dev 0.0). Artifact `liveness_calibration.json`. Adversarial verify
(4-lens refute + synth): caveats-only, 0 blocking — two "blocking" flags were skeptic
errors (config-match read exp07's disease-terminology 'flat=deployed'; budget-plateau
cross-checked the wrong `off` cell).

**REVIEW GATE 1 PASS (Jason):** both config calls ratified (repose@1.0 = the revived cue,
flat@0 gates nothing; budget 36000 on the pre-plateau lesson). Amendments landed in §L:
(1) **entry-read timing corrected** — the k-window mean is taken once the deployed
acquisition curve PLATEAUS, not at run start (at onset a healthy PAM reads sub-bar for
timing reasons = wrong-reason fail in temporal costume); (2) **k pinned = 13 eval-windows**
(1300 steps) from the calibration's eval-cadence plateau (single windows crash to 0.49, so
a one-window read false-fails; binding seed-9 plateau-mean 0.907); (3) **neutral-ceiling
framing recorded as a PRIOR** (deployed read assumed ≤ neutral ceiling at config), not a
fact — §10.9 bookkeeping; (4) **entry-fail disambiguation** — dead-pattern (d≈0, collapse,
ablation-flat) → §10.9 trigger vs depressed-but-alive (structured, ablation-sensitive,
sub-bar) → reference-error under the bars convention; (5) **terminology disambiguation** —
"deployed" = disease regime in exp07 sweep labels vs the revived config in this spec.
Register rows filled (k, plateau-flatness criterion). Next: gate step 2 — Step-0 (a)/(b)
reconfirm on the run commit.

## 2026-07-02 — §L gate step 2: Step-0 (a)/(b) reconfirmed on the run commit

Ran the STAGE1 conflict-validity Step-0 (`conflict_validity.py`) on commit 34fa8c4.
**Provenance:** this is the **first end-to-end execution of the integrated Step-0 gate** —
the `category_share` KeyError proves `conflict_validity.py` had never run to completion (the
rig blocked at 1a9e8ba on the dead evocation channel before the gate was exercised). The old
(a)/(b) PASS came from the **exp05-era probe path** (the separate ladder/oracle probes), not
this integrated gate; **this reconfirm supersedes it.** Two harness bugs surfaced and were
fixed: (1) `category_share` referenced but never computed → KeyError,
crashed all execution; (2) (c) **vacuously PASSED on a dead channel** (both divergences ~1e-10
→ share 0/0 noise, yet CONFLICT_VALIDITY_OK=True) → added a **channel-alive precondition** so
(c) reports DEFERRED, never a false pass (a verdict must not rest on a flagged measurement).

Result **STEP2_AB_OK = True**: **(a) salience→distractor PASS** (distractor_track 0.717 >
category_track 0.508; sep 0.209 ≥ 0.15; floor 0.717 ≥ 0.60 — the QUICK-mode fail at 1500
steps was a budget artifact; raw_distractor 1.000 vs raw_category 0.646 confirms the geometry).
**(b) category-representable PASS** (substrate oracle 0.956 ≥ thr 0.625, ablation-guarded;
easy-ceiling 1.000). seed 2 marginal on (a) per-seed (sep 0.055) but the pre-registered MEAN
criterion passes. **(c) conflict DEFERRED_DEAD_CHANNEL** — the revival config is not yet wired
into the deployed loop, so evocation is dead; (c) is assessable only at gate step 4 (post
entry-gate, live channel). Artifact `conflict_validity.json` (full CONFLICT_VALIDITY_OK=False,
awaiting c). Next (user-directed): wire the revival config into the deployed loop (prerequisite
for step 3 entry gate).

## 2026-07-02 — Revival config WIRED into the deployed loop; knob register RATIFIED

**Build (this commit = the run commit).** The two Edit-3 bindings enter `SculptLoop` via a new
shared module `revival.py` (one code path: `exp07_core` now delegates to the same
`population_mean`/`repose`/`tie_schedule`; **anchor: the 20-seed §L calibration reproduced
`liveness_calibration.json` bit-for-bit through the refactor**). Two identity-default hooks in
`Stage0Loop` (`_pam_penalty`, `_pose_pam_input` — Phase-1 verbatim-preserved); `SculptLoop`
overrides: content-blind global mean-centre on PAM's vision-cue cells (input side; targets never
posed — gap-3 path untouched) + the two-clock preserve tie; `evoke_vision` presents the same
posed frame (probe-consistency, flagged); read-only `pam_proto_spread` column. Wiring asserts
ALL GREEN (`revival_wiring_check.py`): independent-reference step-function equivalence;
mean-centre exactness (1e-07, re-asserted along live training); ablation analogue (identical
population poses identical — μ manufactures nothing, max sep 0.0); tie transitions + penalty
exactly 0 when open; proto-spread live from t=0. Adversarial verify: caveats-only, 0 blocking.

**Register ratification (Jason).**
1. **Onsets:** PAM tie ≡ the cortex's own StepSchedule (same class, same onsets t1=300/t2=1200,
   same clock as `self.unpool`) — the uniformity binding made literal; absoluteness holds on
   each rig's own clock. **Reference-record note: the neutral calibration stays at its own
   canonical clock (900/3600@12000) — matched fractionally and matched in binding; do NOT
   re-run neutral at 300/1200 (two things at once).**
2. **μ:** binding PROPERTIES (future estimators [RECONCILE] against these, not the recipe):
   content-blind population statistic over all 16, detached, pairwise-diff invariance asserted
   per wave. Nonstationary = the correct deployed analogue. **Pre-registered expectation:**
   early-run, vision undifferentiated → μ ≈ everything → channel column weak for
   DEVELOPMENTAL reasons (the co-development story, not a wiring fault); the asserts separate
   the two.
3. **Scope:** vision-slot / input-side / targets-raw (Edit 3 verbatim); `evoke_vision` fix
   stands (one-code-path applies to reads too).
4. **Entry run length — criterion-led, capped:** run until the deployed channel column fires
   the eps-flatness criterion (calibration form, eval cadence); entry read = first k′ windows
   after; **cap = 48000 waves [RECONCILE]** (headroom above both clock readings). Flatness
   never fires by cap → stop, surface as a NON-CONVERGENCE FINDING (neither pass nor fail).
5. **Read construction:** category-partition d (d_diff across category, d_same
   within-category-across-distractor, d_ablated null-word) + mean-centred denominator —
   ratified. **This voids the 16-cue bar's transfer** (different statistic on different
   association geometry; cardinality moving converged d is the settled exp06/07 lesson;
   direction uncertain → measure, don't argue). **Pre-run addition: MATCHED-BAR calibration**
   — same 20-seed harness, same emission population, only the associate map changes (16 → 2,
   8+8), the pinned statistic computed by the SAME code path the entry read will use, same
   margin form, k′ re-derived by the pinned procedure. **General rule: bar and read must be
   the same function on matched geometry.** 0.8866 / k=13 stand as the 16-cue instrument's
   record — SCOPED, not superseded. Surface the matched-bar JSON before the entry read
   (checkpoint, not a full gate); structurally surprising → STOP (design question, not knob).

**Sequence:** commit build → matched-bar calibration (surface JSON) → (a)/(b) re-run on the
run commit → entry run → k′-mean vs matched bar → fail: stop + pre-registered disambiguation;
pass: step 4, all surfacing together at REVIEW GATE 4.

## 2026-07-02 — Matched-bar checkpoint: RULER SUPERSEDED pre-read; schedule re-converged; alignment finding OPEN

Four records (the checkpoint fired twice, correctly, before any gated read consumed a broken
instrument — instrument-validity supersessions, the bars convention's clean branch):

**1. Degeneracy + ruler supersession.** The pinned v1 statistic (category-partition d,
mean-centred-EVOCATION denominator) is DEGENERATE on 2-associate geometry: within-class
evocations are identical by construction → centred evocation set = {±d/2} → d_diff ≡ 2 at ANY
scale. Demonstrated (matched-bar v1, 20 seeds): raw cross-class separation spanning SIX ORDERS
of magnitude (8.6e-07 → 0.70) all read 1.995–2.000; the derived bar (1.9961) split dead seeds
from dead seeds on eps-noise; k′ degenerated. **Ruler v2 (ratified, binding properties not
recipe):** numerator = cross-class evoked separation (centring-invariant); denominator = mean
centred-CONTENT norm over the 16-item population (neutral: harness items; deployed: vision's
live emissions at read time), detached, one shared code path (`revival.partition_read`);
denominator floor → NOT_ASSESSABLE, never a number; numerator/denominator/ratio logged as
separate columns; the channel column switches to this ruler. Validated: dead reads 0.0 (v1:
1.64), healthy ≈ 0.5 (class-mean geometry), graded across seeds. 16-cue record 0.8866/k=13
stays consistent as the SCOPED instrument — untouched, not reusable.

**2. d_same STRUCK as a discriminator on 2-associate geometry** (≡ 0 for dead and healthy
alike — never read zero as health; reported for the record only). The ablation guard carries
content-dependence alone.

**3. Censoring + schedule re-convergence.** v1's 7/20 "dead" seeds at 36000 were
RIGHT-CENSORED, not dead (healthy seed 0: dead at 33000 → alive at 34000). Mechanistic
expectation (context, not a gate): 2 distinct cues supply weaker symmetry-breaking pull than
16 → slower prototype differentiation. Extended to cap 60000: **all 20 seeds alive**
(bimodality pre-registration does NOT fire; no reliability finding). v2 read @60000:
reference 0.5044, spread 0.0772, bar 0.3500 (mean − 2·per-seed std).

**4. Cap re-derivation — first attempt EXPOSED an alignment flaw (OPEN design item).** The
revival-onset distribution is long-right-tailed (onsets 30000→60000, right-censored at cap;
seed 13 revived in the final ~1000 steps: 52/61 fine-tail windows at 0 → k′ under any window
count underivable; the family "plateau onset" (33000) was a composition artifact — converged
seeds are stationary, the family mean climbs as late revivers arrive). A FIXED-STEP reference
read cannot be aligned against this distribution. **Proposed (awaiting ratification):
per-seed criterion-aligned reference** — each seed read k′ windows after ITS OWN eps-flatness
criterion fires (the same alignment the ratified entry procedure already uses: the
bar-and-read-same-function rule extended to the time axis); non-firing-by-cap seeds reported
as a non-convergence fraction (material fraction → the reliability stop); k′ derived from
post-fire windows; entry cap [RECONCILE] from the onset distribution's right tail (~90000-
scale, vs the superseded 48000 literal and the broken family-onset×1.5). Bar/k′/cap derived
ONCE, on the aligned reference. HOLDING at the checkpoint.

## 2026-07-02 — Matched bar DERIVED (v3, per-seed criterion-aligned): bar 0.3128, k′=7, cap 112500

**Alignment ratified + five pins** (fixed before the run; Jason): (1) read-eligibility = fire
AND full derivation tail inside budget (no partial-tail reads); (2) k′ FIRST, bar-independent
(smallest k with every read seed's k-window post-fire mean within eps of its own long-tail
plateau mean), THEN bar — anti-circularity; (3) censoring ladder 90000 → extend-once 120000;
still-unfired → STOP (reliability); >2/20 unread → STOP (material fraction); (4) entry cap =
(max onset + read tail) × 1.5 [RECONCILE from the artifact], clock caveat named (onsets in
neutral optimizer steps; step↔wave equivalence for revival dynamics unproven — conservative
unshrunk mapping, a ceiling not a target); (5) deployed flatness fires on the RATIO column
with the denominator-floor assert standing; NOT-ASSESSABLE + three-column logging keep a late
or absent deployed plateau interpretable. **Ownership line (Jason): the family-onset×1.5 rule
is superseded on demonstrated grounds — it assumed a family-level plateau that doesn't exist
for a staggered-onset family; the climbing mean was late arrivals (composition artifact,
correctly caught).** Three pre-read instrument fixes now stand in sequence: degeneracy →
ruler; censoring → schedule; composition → alignment — all caught before a gated read
consumed them.

**Outcome (ladder round 1 sufficed): 20/20 seeds READ at 90000** — no unfired, no
fired-too-late, neither pin-3 stop fires. Fire criterion: consecutive 3000-block means both
alive (>0.1) and |Δ| ≤ 0.05; fires span 27000–69000 (seed 13 at 69000, the v2 right-tail,
now cleanly read). **k′ = 7 eval-windows (700 steps)**, bar-independent. **Reference 0.4929,
spread 0.0901, bar = 0.3128** (mean − 2·per-seed std of aligned k′-reads). Entry cap derived
**112500** = (69000 + 6000) × 1.5. Fixed-step v2 numbers (0.5044/0.3500 @60000) carried as
provenance only (`liveness_matched_bar.fixedstep60k.json`). Guards (v1/v2, structurally
forced μ-side): d_ablated 0.0, d_same struck ≡ 0. Artifact `liveness_matched_bar.json`.
**Deployed entry gate is now fully specified: fire on the ratio column (same block/eps/alive
constants) → read = 7-window mean → clear 0.3128; cap 112500 waves; non-convergence =
finding; fail → the pre-registered dead-pattern vs depressed-but-alive disambiguation.**

## 2026-07-02 — (a) point-read FAIL → WINDOWED estimators ruled (rig-wide sweep) + dynamics panel

**The beats, in order (all three in the record):** (1) **FAIL(point):** (a) re-run on the run
commit read distractor 0.552 vs category 0.505 (was 0.717/0.508 PASS at fb9a27d) —
`conflict_validity.pointread_fail.json`. (2) **Ruling (Jason; bars convention,
reference-error grounds, three demonstrated legs — `diag_a_trajectory.log`):** no-word
distractor occupancy intrinsically OSCILLATES 0.49↔1.00 at ~1500-wave period in the revival
AND legacy configs (amplitude ≫ eval noise ≈0.04); the LEGACY config also fails point-reads at
other draws (dips to 0.488@7500 — the old PASS was a lucky draw; symmetry, no config favored);
thresholds untouched — estimator only. The criterion measured a point draw of an oscillating
process where it should have measured the process mean. (3) **Re-run(windowed):** pending on
the amendment commit.

**The amendment unit:** (a) read = mean over ALL post-onset 3000-wave block reads of the
no-word trajectory, run span 30000 (~20 cycles), onset = capacity clock — no selectable
sub-window exists in the code path. **Point-read sweep (pre-result):** (c) windowed the same
way in `conflict_validity`; (c)-at-entry = mean over the k′ entry-read windows
(`stage1_entry_gate.py`); reversed-lift + words-after asymptotic gap mandated windowed in the
spec before their harnesses exist. **Dynamics panel (standing deliverable):** every artifact
axis ships {mean, amplitude/envelope, dominant period, trend} beside its windowed scalar
(`revival.dynamics_panel`, one code path) — an average never ships alone. **Pre-registration
additions:** differential-stability named expectation (category should hunt LESS than
distractor in the word-run; amplitude ratio, panel-derived; NOT a gate; joins the
structured-open family) + T_run register input measured (no-word distractor cycle ≈1500
waves, amplitude 0.49↔1.00 — regime constants; §6 stable-depth-vs-hunt remains the word-run
trigger with this diagnostic as comparison evidence). Entry runner + `evoke_vision(null_word=)`
(the deployed ablation guard) land in the same unit. **This commit is the run commit.**

## 2026-07-02 — GATE 4: windowed a/b/c PASS; entry run NON_CONVERGENCE; VERIFIED collapse finding

**Windowed re-run @ad23fc6: STEP2_AB_OK=True; full CONFLICT_VALIDITY_OK=True.** (a) PASS
0.749 vs 0.524 (per-seed 0.72–0.78 — the estimator amendment stabilized the instrument as
the diagnostic predicted). (b) PASS (0.956). (c) PASS — **flagged: carried by seed 2's LIVE
deployed channel** (cat_div 1.423, dist_div 0, share 1.000 — the first live word→category
evocation observed in the deployed rig, structure exactly as designed); seeds 0/1 pre-onset
at 30000 (staggered onsets, as the reference family predicts).

**Entry run (gate step 3, seed 0, cap 112500): NON_CONVERGENCE** — the channel column never
fired the two-block stability criterion. Pre-registered lane (neither pass nor fail; no
rescue). Underneath it, a 4-lens adversarially verified finding (three of the initial
readings corrected in verification):
- **DEMONSTRATED — total vision-content collapse, word-present arm, long horizon:** all 16
  member emissions → ONE point (denominator 1.108 → 2.5e-07; final ~20k waves pinned;
  occupancy both-axes chance from ~96000; healthy through ~72000; failed revival transient
  @93000). Real, not instrument (all artifact hypotheses ruled out in source). Terminal
  failure of a standing collapse-and-regrow oscillation (denom period ≈4800; 394/1125
  windows assessable). Caveat: ratio column + occupancy both read through vision.emit — one
  collapse read twice.
- **DEMONSTRATED — evocation channel alive and DECOUPLED from dead content:** numerator
  declines through discrete plateaus 46→36→10→13→4.97 (prototype-resonance snapping);
  proto_spread at run-max (0.0317); ratio correctly NOT_ASSESSABLE at tail.
- **MECHANISM — word-driven homogenization REFUTED** (floors at 2 points ≠ 1; word cannot
  name the A/distractor axes that died; the word-LESS distractor died — the word path is a
  failed 2-point ANCHOR). **Surviving suspect, PLAUSIBLE only: the gap-3 no-detach
  TARGET-side pull via the vision-SELF reconstruction path (a contraction on emissions),
  permitted by sparse anchor (2 targets/16 members) + spread 10× under-weighted (0.1 vs
  gain 1.0) + all L2 ties → 0 after t=1200.** No-detach is deliberate design → any fix is a
  design revision at its own gate. Exonerated: JEPA, re-pool.
- **Routing (per verification):** NON_CONVERGENCE stands as the gate enum AND a **§10.9
  trigger ASSESSMENT is owed alongside** (route B textually satisfied; the parenthetical is
  interpretive — evocations separated while teaching demonstrably did not proceed).
  Signature is descriptively NEW (content death + live channel + live prototypes ≠ exp06
  prototype-collapse). Power: n=1 full-horizon; 30k corroboration 2/3 word-arm dead vs 3/3
  no-word healthy — under-powered vs the ≥20 floor.

**GATE 4 ruling (Jason):** Gate-4 unit committed as surfaced (artifacts honest,
NON_CONVERGENCE standing). Canon: new FRONTIER §10.12 (finding, status-split, stress-test
reading, potency held as reading, #12/EMA note flagged for the design gate — decides
nothing); §L route-B reworded in place (signal-side death with content assessable) + third
pattern into the entry-fail disambiguation. Diagnostic arms pre-registered BEFORE launch
(per-arm prediction table under the composed hypothesis; sharpest line = no-word marathon
collapses no slower than word-arm; arm-5 vocab ladder with monotone-easing prediction);
new columns everywhere (substrate-side Δ2; word-path vs self-path gradient split +
masking-mix fraction). Adoption line: no arm is a fix — detach amputates the teaching
channel, ties>0 is Tier-2-adjacent, re-weight is a knob; design revision happens after
verdicts at its own gate. All verdicts return to ONE review; steps 5–6 stay blocked;
word-arm seed extension staged as compute allows, split pre-registered.

## 2026-07-03 — THE ONE REVIEW: five verdicts ratified as verified; NO design revision yet

EXP08 campaign ran clean (22/22, artifacts @57ce968); verdicts adversarially verified (2
corrected, 1 instrument demoted) and ratified by Jason — including the refuted sharpest
line (Jason's own), kept with all beats: prediction (no-word collapses no slower) → result
(nowhere near terminal at matched cap; ~4.8× slower clock — den period 23100 vs 4800) →
revision (word-presence = ACCELERANT, demonstrated; distinct terminality mechanism only
suspected, n=1 vs n=1, marathon caught mid-decay). DETACH confirmed re-anchored (target-
side pull NECESSARY; num 3/3 seeds, fixed-α contrast; gW=0.00 validates amputation).
SPREAD not-confirmed-as-stated (circular readout, manufacturing class — spread_loss forces
the variance den measures; s0 counterexample); partial 2/3 independent. TIES uninformative
(ε=0.1 overshot; parked, re-dose on-call). LADDER statistically flat but UNINFORMATIVE on
anchor density at 30k (dense anchors under-acquired, num ~4× weaker at v8/16); follow-up
pre-named not launched: acquisition-aligned per-rung reads (time-axis lesson #3); any
word-dependent 30k read is acquisition-suspect until aligned. Localization: capacity-open
ASSIGNMENT-collapse (dead-dictionary) — deduced, column pending; both Δ2 metrics
non-diagnostic. **den DEMOTED to a one-sided collapse-floor tripwire; principle joins the
circularity ladder as its second instance: variance statistics cannot certify
differentiation — floor tripwires only.** Full verified table: FRONTIER §10.12.1.

**Ruling: design gate PARKED** (three claims still deduced/suspected: driver identity,
dead-dictionary, terminal lock; converters cheaper than the design they'd steer). All four
converters authorized, composed (EXP08 prereg extension, pinned pre-run): assignment
columns + gradient-to-terminality FIRST; Run A = no-word marathon extension to cap 500000
(TERMINAL / ASYMPTOTIC / neither, pre-registered); Run B = +1 word-arm full-horizon seed
carrying the gradient columns through the terminal window. Then ONE follow-up review →
the design gate. Steps 5–6 stay blocked.

## 2026-07-03 — FOLLOW-UP REVIEW: dead-dictionary DEMONSTRATED; DESIGN GATE OPENED

Converter runs A+B complete (artifacts @a0f318b). **Run A (no-word, 500k):
NEITHER_BY_CAP, earned — the no-word regime named METASTABLE INTERMITTENT COLLAPSE**
(floor episodes e-6…e-8 from ~230k with episodic partial revivals; final window still
flickering: occD 0.60, den 0.048). **Run B (word, seed 1): TERMINALITY REPLICATED n=2**,
earlier than seed 0 (pin from ~80k; zero regrow). **Dead-dictionary DEDUCED → DEMONSTRATED**
(argmax_k=1 sustained both arms; capacity open, Δ2 2.54/1.14). **Pin-depth correlate
measured: word asg_dist ≈1e-5 (locked) vs no-word ≈0.08 (regrow-capable) — 4 orders. Word
= accelerant + pin-deepener.** Scope line: engine shared, lock word-conditional on current
data; do NOT extrapolate no-word terminality; the 75k self-spike = named observable only.
Self-absorption reading coherent-deduced → the KICK PROBE is its direct test (prereg in
EXP08 doc; construction surfaced for checkpoint read BEFORE any run). **DESIGN GATE
OPENED:** constraint = keep routing input-sensitive under the target-side pull; on the
table = routing-side counter-force / denser anchor / revised target path; drift guards
verbatim (counter-force highest-risk = manufacturing class; confidence-first check;
detach stays diagnostic); #12/EMA note promoted to design-table input. Steps 5–6 blocked.
Full record: FRONTIER §10.12.2.

## 2026-07-03 — KICK PROBE: ESCAPABLE stands (re-scored); fork re-ruled PREVENTION-PRIMARY

All beats: mean-form ESCAPABLE(ε*=0.01 both) → flagged (measured a different quantity than
the prereg word "sustained") → re-score ruled, pinned literal form → **ESCAPABLE STANDS
(word ε*=0.1, no-word ε*=0.01); no third pass.** Falsified expectations kept on record:
the expected ABSORBING-in-substance; the form-robustness ground; CC's "decay-back
universal" interim read (downsample artifact, corrected). Population structure (24 kicked
resumes): 2 PIN / 8 EMBER (named: sustained 1e-4–3e-3, flat) / 8 FLICKER (2
right-censored, caveat only) / 6 SUSTAINED functional-scale (no-word ε=.01 k2: mean 0.232
≈ 4× pre-kick, positive trend; word ε=.3 k0: 10⁴× the pin). **Bonus finding (canon,
verdict-independent): the no-word ε=0 control self-pins unkicked at ~518k → fate shared
end-to-end; word = pure accelerant (5.4× terminal / 4.8× period, converging) +
pin-deepener; pin-depth gap = position on one trajectory. §10.12.2 scope line superseded
by measurement (amended in place).** Fork re-ruled: **PREVENTION-PRIMARY,
RECOVERY-UNRELIABLE** (~25% stochastic rescue = gambler's mechanism; the flow is
mostly-absorbing with stochastic re-amplification windows; design question = what
conditions put the system in the re-amplifying regime; picture = a current with eddies;
regulation = widening the pockets). Kick-not-a-candidate barred, now load-bearing.
Authorized: the CORRELATE HUNT (read-only, no new runs — SUSTAINED(6) vs PIN/EMBER(10);
candidates: t=0 magnitude, state, ε, early-window trend). **HUNT RUN: the one real
correlate is STATE = trajectory position (SUSTAINED 5 no-word / 1 word vs PIN-EMBER 3/7;
~5× pocket-width gradient — early ≫ late); t0 weak non-separating (U≈0.80,
counterexamples both ways); ε none. "Stochastic" → "conditioned by position, stochastic
within position"; no controllable rescue lever — sharpens PREVENTION-PRIMARY.** Then
design table from canon, first deliverable = the force-ledger. Full record: FRONTIER
§10.12.3 + the prereg hunt record.

## 2026-07-03 — Position-vs-live-pull confound recorded (flagged at close, landed post-compaction)

Jason's close-ratification flag, ruled after the 7a0db83 close message and landed here:
the STATE correlate (SUSTAINED 5 no-word / 1 word) is confounded at n=2 states — reading
(a) position/pocket-width (as recorded) vs reading (b) the word's ongoing pull during
resume consuming re-seeded sensitivity in real time. Both consistent with shared fate;
both say intervene early; the anchor's pull is itself a flow term. Pre-named cheap
discriminator (design-table input, NOT launched): resume the word-pinned state with word
ablated + kick — pockets widening ⇒ the pull closes them ⇒ anchor design = a direct
pocket-width lever. Recorded in the EXP08 prereg tail (Position-vs-live-pull confound
section). No other changes; design table remains open in chat; steps 5–6 blocked.

## 2026-07-03 — THE DESIGN TABLE: force-ledger v1 (FRONTIER §10.13); Fork 1 → self-path #12 reference; EXP09 spec AT CHECKPOINT

The design table opened from canon; first deliverable landed. **Force-ledger v1**
canonical in §10.13 — 7 forces (3 contraction / 4 differentiation), every number traced
to committed artifacts before writing. TWO tabled claims corrected on the record: row 3
(constant Δ2 re-pool) was tabled "slow, designed, graceful" but the deployed rate was 0
= no-op in every collapse run (exonerated as engine, and OFF); and the tabled row-2
clause "persists post-death at ~4× self magnitude" was REFUTED in pre-commit
verification — the word/self grad-split ratio reads the identical ≈4.0 in the word-FREE
marathon (probe mask geometry: word-path probe masks all W=3 vision cells, self-path
probe one), so 4.0× is an instrument signature, not word-pull evidence; post-death
word-pull persistence currently has no valid observable. Structural fact surfaced: rows
1+4 are ONE PATH (gap-3 common component contracts / differential component separates,
self-consuming at the pin — coherent-deduced); the self-path is the one plastic loop
THROUGH THE ASSOCIATIVE OPERATOR with no #12 reference (JEPA's stop-grad loop outside
#12 scope).

**Fork 1 RESOLVED → (a) the self-path #12 reference** (grounds in §10.13: repairs the
violation; no new force/objective; gap-3 mismatch still flows to online weights [as
ruled — SHARPENED by verification: via the completion/cue-side path only; canonical
target-side gap-3 pressure is severed at every β, the EXP09 §3 honesty-block fact];
spread stays row-5 complement on the surface mismatch). (b)/(c) parked with triggers.
Drift guard verbatim: passes on FUNCTION, never on EMA vocabulary.

**EXP09_SELF_REFERENCE_PREREG.md written — SPEC AT CHECKPOINT, nothing built or run.**
Pins: slow copy of the vision cortex supplies the self-path reconstruction target only
(detached; forward-only; the `_pam_target` hook point with signature extension
[RECONCILE at build]; one code path, config-gated); build-full/pin-to-constant, β
[RECONCILE] — slow bound vs den period; **fast bound UNMEASURED (verification catch: no
committed acquisition-plateau clock exists; §10.12.1's 30k caution applies; in word s1
num = 0.0 through 45k — the word association post-dates routing collapse); measured
collapse clocks used instead (s1 transient 25.2k / sustained 42.6k)**; candidates
9600/12000/23100 (23100 flagged likely-outside). Function test pre-registered kick-free
(word {0,1} ≥192k; no-word control rides, pin on it = acceleration = FAIL) with a TOTAL
outcome taxonomy re-pinned against measured spans: METASTABLE EPISODE / PIN (K_w) /
PIN-CENSORED (control; regrown epochs to 5.9 periods on the books) / FAIL / PASS
(flicker-tolerant calibration rule — healthy spans flicker argmax_k=1 in ~11% of
windows; every-window forms fail 59% of measured HEALTHY placements) / NEITHER
(pre-registered third outcome). Period-instrument discrepancy logged (entry-run 4800 @
cadence 100 vs word_terminal_s1 panel 1500 @ cadence 300) — estimator pinned at
checkpoint. **Honesty block (EXP09 §3):** at every β the target-side gradient into
online vision is zero — the same topology as the detach diagnostic (β=1 = detach arm
exactly; β=0 = frozen-at-birth; family never contains the baseline) and the detach arm
did not pin either → a bare no-pin PASS proves nothing; the detach-null wrong-reason
screen (EXP09 §6) is load-bearing — and its gradient-share candidate was STRUCK as
circular in verification (member-distinct targets mechanically produce member-dependent
probe gradients); discrimination rests on the detach-null comparator arm +
outcome-level divergence. Decomposition observable spec'd (§7, explicitly NOT a
certifier): common/differential energy split on the 16-member evocation set + the same
split on the per-member teaching gradient, with probe hygiene pinned (RNG isolation —
the grad_split idiom consumes training RNG; fixed mask geometry — the standing
word/self ratio carries a ≈4.0 mechanical geometry factor). Baseline-replay cost
corrected 3.5h → ~4 min measured (both baselines proposed). **Pre-commit adversarial
verification: 32 agents / 4 lenses / per-finding independent verify; 28 raw → 23
confirmed findings, all applied above; 5 rejected on re-derivation (incl. 3.24 traces
via the pooled estimator sum/sum = 3.235 in marathon_s0 grad_split).** Checkpoint list
= EXP09 §10 (8 items). Steps 5–6 stay blocked.
