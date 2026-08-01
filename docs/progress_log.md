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

## 2026-07-03 — EXP09 CHECKPOINT RESOLVED (ruling): strikes ratified; ground (3) re-worded; β by rule; taxonomy ratified; build authorized to the final pre-run read

**The ruling, in order.** (1) Row-2 strike RATIFIED (Jason's carry): geometry, not pull
— dispositive on the word-free identical ratio; row 2 stands on terminal clocks + pin
depth; the word-ablated-resume discriminator unaffected (reads outcomes, not probe
ratios); post-death pull logged as no-valid-observable, not chased. (2) Ground (3)
RE-WORDED, not re-affirmed (Jason's overclaim, his words): **teaching path RE-ROUTED,
not intact** — canonical target-side gap-3 pressure severed at every β; mismatch via
cue/completion side only; the design = a recorded BET, certified or refuted by §6 +
detach-null, never assumed. The bet has teeth, pre-registered: **(a) ≈ detach-null on
outcomes ⇒ the slow copy is STOP-GRAD IN COSTUME** — function test may PASS while the
paradigm bet FAILS → partial result back to the table, never laundered into PASS.
(3) β RULE pinned: period estimator first, then τ = 2× pinned den period; retention
stated as numbers (caveat, not bound); acquisition-derived bounds STRUCK until
acquisition is measured. The buried s1 fact canonized as a named ledger observation
(log, no claim): the word's pull is task-structural, present before measurable
association. (4) Taxonomy RATIFIED (calibrate-tolerance-from-measured-healthy, third
instance): constants from healthy placements only, fixed pre-run; PASS tolerance
constructed so the terminal signature can never sit inside it; cadence-100 series =
instrument of record (4800 stands); panel estimator recomputed, discrepancy
resolved-and-recorded before β/K_w consumed it. (5) Gradient-share discriminator strike
RATIFIED (share-vs-lift, third appearance); discrimination = detach-null comparator +
outcome-level divergence. (6) Replay upgrade RATIFIED — back-fills the decomposition
onto the measured collapse baselines BEFORE EXP09 runs. Remaining pins: scope = full
self-target emission path; birth = bit-copy at t=0 (stiff-early automatic); route =
identity-default hooks, one code path, always detached; asserts (identity at t0,
divergence >0, zero grad to copy); pairwise slow-target distinctness = standing column
with pre-registered floor, COPY-COLLAPSE = named outcome; probe geometry
equalized-or-recorded, composition logged, asserted at wiring.

**Resolutions EXECUTED (all from committed data, before consumption).** Period: the
same estimator on word_terminal_s1's full series REPRODUCES the 1500 (segment
contamination — early ramp + ~70k pinned tail); on the healthy segment (20100–42300)
it reads 6000, same order as the instrument of record; **4800 STANDS** (entry-run
cadence-100 full series, n=1125); residual 6000-vs-4800 attributed to seed +
short-segment quantization. **τ = 2×4800 = 9600** (β ≈ 1.042e-4/wave); retention
92.8% by 25.2k / 98.8% by 42.6k, mean lag 9600. PASS constants calibrated from the 44
healthy 32-window placements: **≥27/32 argmax_k>1, no k=1 run >2, den ≥1e-3 in all
32** — in the STRICT healthy span den is never sub-floor (the earlier "healthy dips"
came from including the collapse transition), so the every-window den form is
CALIBRATED, not assumed; terminal signature reads 0/32 + 0/32 + run 32 — can never sit
inside the tolerance. K_w = 3 (14400); K_c = 8 (184800) with the honest consequence
recorded: control PIN practically unreachable at 192k → control terminal epochs
surface as PIN-CENSORED → extension at its own ruling; acceleration cannot hide.
Single-seed calibration (s1 = the only committed word-arm healthy span with columns)
noted. Changed-threshold ×1.5, None → pinned constant, healthy-segment-only estimator.

**All eight checkpoint items RESOLVED (EXP09 §10). Sequence: wire → surface resolved
prereg + wiring asserts + replayed-baseline decomposition panels at ONE final pre-run
read → arms run. Steps 5–6 blocked.**

## 2026-07-03 — EXP09 WIRED: slow-ref loop + decomposition probes + asserts; THREAD CATCH; both baseline replays BIT-IDENTICAL; panels landed

**Wiring (one code path).** `exp09_arms.py`: SlowRefLoop = EXP08Loop + the slow copy
(full vision-cortex parameter copy; birth bit-copy stored; post-optimizer-step lag rule,
τ=9600) — step() inherited unchanged (asserted: no new loss term); the build_cells WRAP
rewrites only the TARGET's vision rows from the window raw under no_grad (word rows
untouched — sampled assert); detach-null arm rides the existing DetachLoop. Probes (all
RNG-isolated, asserted per call): evocation split, per-member gradient split (ONE fixed
mask geometry — never the asymmetric word/self pair), reference-distinctness ×4 incl.
pairwise (copy-collapse watch), pairwise_emit baseline analogue. `exp08_arms.py` got two
ADDITIVE defaults-preserving params (probes callback; out_tag so replays never overwrite
committed artifacts) + sig-figs formatting for probe columns (gradient energies live at
1e-9; standing columns keep the committed 6-decimal contract) + `torch_num_threads`
provenance. Smoke: all wiring asserts green (t=0 identity; divergence>0 by t=1200
— d_online 3.25 vs d_birth 0.28, the lag visibly working; zero grad to copy; RNG
untouched).

**THE THREAD CATCH (instrument finding, on the record).** First replay FAILED the
bit-faithful assert — 93 windows off by the LAST DIGIT of the ratio column only
(num/den/asg untouched). A/B isolation EXONERATED the probes (none-vs-full: 0
mismatches / 6000 steps); the cause is torch THREAD COUNT: at 16 threads
parallel-reduction order perturbs floats ~1e-9 relative (visible only in ratio's coarse
6-decimal quantization); at 1–2 threads the replay is byte-identical. **The determinism
contract is seed + construction order + THREADS** — pinned to 1 for every EXP09 run;
recorded in every artifact. (The committed artifacts came from the kick session's
thread-limited parallel phase.)

**Replays (SS7 upgrade executed): BOTH baselines BIT-IDENTICAL to committed** —
word_terminal_s1 (375 windows) and marathon_ext_s0 (1666 windows) — RNG isolation +
thread contract proven end-to-end; decomposition columns back-filled onto both measured
collapse baselines. Panels: `exp08/word_terminal_decomp_panels.png`,
`exp08/marathon_ext_decomp_panels.png`; floor read `exp08/exp09_pairwise_floor_read.json`.

**First trajectory numbers (READ-ONLY observations for the pre-run read — no claims).**
Word arm: the teaching gradient is ~1.4e4:1 COMMON-dominated through the entire healthy
phase (grad_diff ~5e-9 vs grad_common ~8e-5) — the differential force starved long
before terminal events; the ratio touches ~1 only in the collapse transition (exactly
when the word channel belatedly acquires: evo_diff 1.8e-14 → 1.68); terminal ~28 with
everything decayed. No-word arm: healthy ~294 (≈50× less common-dominated than the word
arm's healthy phase — direction consistent with the 5× clock gap; cross-arm n=1 read),
pinned 2.2e6 (grad_diff 3.4e-10), revival tail ~6.9e3 with pairwise recovering.
Pairwise floor sources (SS6.1, Jason pins at the read): healthy min 0.00177 (word) /
0.000907 (no-word) vs terminal 1.1e-5 / pinned-span 3.5e-5 — proposal: floor 3e-4
(≥3× below the weakest healthy min, ≥8× above the word terminal).

**Status: everything before the final pre-run read is DONE. Steps 5–6 blocked; no arms
run until the read.**

## 2026-07-03 — FINAL PRE-RUN READ: GO. Floor 3e-4 ratified; thread contract generalized; PASS-scope pre-registered; four arms LAUNCHED

The ruling: (1) §6.1 pairwise floor RATIFIED at 3e-4 (≥3× below weakest healthy min,
≥8× above terminal); COPY-COLLAPSE the named outcome. (2) Thread catch RATIFIED and
GENERALIZED — the determinism contract (seed + construction order + threads) added to
the standing build discipline (§"discipline to hold", PROJECT_STATE): every rig
claiming replay pins and records its thread count; future rigs inherit it. (3)
PRE-REGISTERED BEFORE WAVE 0, because the read will tempt it: the baselines showed
healthy phases ~10⁴:1 common-dominated — whatever held routing open, it was NOT
differential gradient winning a balance; **a slowref PASS certifies "the reference
sustains input-sensitivity" and nothing more — the HOW (restored differential fuel vs
changed common geometry vs something else) is a separate finding read off the
decomposition columns, never assumed. A PASS does not silently validate the balance
story the baselines just undermined.** (4) Cross-arm ratio note (word healthy ≈50×
no-word) logged as-is, n=1 each, nothing more. **GO: four arms at threads=1 —
slowref_word s{0,1}, slowref_noword s0 (control), detachnull s1 (comparator) — 192000
waves each. Verdicts to ONE review; steps 5–6 blocked.**

## 2026-07-03 — EXP09 ARMS RUN + VERDICTS VERIFIED — AT ONE REVIEW (no canon until ruling)

Four arms, 192k each, threads=1, from committed pins (93cf264). **Verdicts (independently
rescored, all reproduce, no flips under period-consistent windows):** slowref_word s0 =
PASS_PENDING_SCREEN (32/32 k>1, zero k=1 windows in the whole 192k, zero episodes);
slowref_word s1 = same, maximal margins; slowref_noword s0 control = NO_PIN (zero k=1 in
640 windows — no acceleration); detachnull s1 = **PASS_PENDING_SCREEN with IDENTICAL
margins.** Adversarial verification: 35 agents, 4 lenses, per-finding adjudication — 29
confirmed findings, all folded in below.

**THE SCREEN: STOP-GRAD-IN-COSTUME — the pre-registered partial outcome FIRED.** No
recorded column separates slowref from the null in kind (asg / den / pairwise /
grad-ratio / occupancy all ≈); two of the three ruled screen axes returned no events
(vacuous — stated, not counted as equal-behavior evidence); the draft "null's channel
dies, slowref holds" was CHERRY-PICKED endpoints of a block-oscillating num column
(null toggles dead↔strongly-alive, late alive amplitude 8–40× slowref's; horizon landed
in a dead block) — struck. **Function certified per the pinned scope: the reference
sustains input-sensitivity. Paradigm bet NOT certified: partial result routes to the
design table.** Knob CERTIFIED separately (no COPY-COLLAPSE — floor breached only in
the birth transient; lag mechanically valid; τ consistent): the costume outcome is
about the FUNCTION, not a broken reference.

**THE REGIME SHIFT (headline, not buried):** all four arms live at a spread set-point
(den ~3.3 word / ~3.5 control+null; pairwise ~4–5) that NEITHER baseline ever inhabited
(~200× the word-baseline healthy-span mean den 0.0162) — produced by cutting the
target-side pull (the null shares it), not by the reference. The PASS constants were
calibrated out-of-regime and are cleared trivially by everything including the null:
**PASS was non-discriminating by construction in this regime; the §6 screen decides,
and it decides costume.**

**THE HOW COLUMNS — DEMOTED by confound analysis (verified):** the dominance flip
(baselines common-dominated ~1.4e4/~294 healthy → all four arms differential-dominated,
medians 0.11–0.17) is real in direction BUT (a) NOT attributable to probe term-removal
— detachnull's probe RETAINS the grad-attached target term and flips identically; (b)
its arithmetic is carried by grad_diff rising 5–8 orders CO-MOVING with emission
distinctness (~150–400× pairwise) — the decomposition largely RESTATES member-
distinctness in gradient units (the circularity ladder's shadow; adds no independent
support beyond den/pairwise). Separately: the two decompositions DISSOCIATE — every
fresh arm is gradient-diff-dominated yet EVOCATION-common-dominated (evo_ratio med
12–799), with recurring near-copy episodes and horizon-end decay in s0/noword/null —
the associative evocation channel stays common-dominated everywhere. Trajectory
observations only.

**Named observations (logged, no claims):** num-channel residual divergence (slowref s1
continuous-weak post-acquisition vs null intermittent-strong; seed-inconsistent,
amplitude-reversed — dedicated seeds required for any claim). Baseline corrections:
word_terminal_s1 pin ONSET = 75300 (7.81 periods; k-collapse 42600; two regrown dead
episodes before the pin), not "~80k"; marathon_ext_s0 (500k) has NO pin under the
prereg rule — three REGROWN episodes (max 5.92 no-word periods = the K_c calibration
source), den 0.048 at horizon; the ~518k no-word self-pin remains the KICK ε=0 RESUME's
measurement (a +48k continuation), not this artifact's.

**Instrument caveats + scorer guards (before any future use):** (1) the healthy-segment
period estimator MISFIRES on non-collapsing runs (locks onto ambient jitter: control
23100→1200 = 19× down-substitution, detachnull 4800→1800; silently rescales the K_c
bar 184800→9600 — vacuous here with zero qualifying windows anywhere, a live trap
later) — guard: substitution requires an actual collapse cycle; (2) the PASS read is
hardcoded 32 windows and does not track substituted periods (conservative here); (3)
COPY-COLLAPSE is procedural, not mechanical — the scorer never consults ref_pairwise
(this dated read = the record); (4) control's evo/grad columns are OOD (operator never
trained on real tokens) — excluded from cross-arm decomposition comparisons; (5)
detachnull's grad probe retains the target term (training-faithful; logged).

**AT REVIEW. No canon writes; steps 5–6 blocked; the partial result awaits the ruling.**

## 2026-07-04 — EXP09 RULING LANDED (FRONTIER §10.14) + EXP10 PREREG DRAFTED (at checkpoint)

The one-review ruling, in canon: verdicts + screen as verified; **certified scope
NARROWED — pull-removal prevents the pin, the reference's contribution UNDETECTED**
(both beats kept: the prereg's pinned scope, then the null's identical margins);
**Fork 1(a) UNRESOLVED-NOT-REFUTED**; the regime shift + its instrument lesson
(verdict constants calibrate IN-REGIME); the HOW demotion with the evo/grad
DISSOCIATION surviving as the teaching-axis observation; baseline corrections; scorer
guards as EXP10 build items; the num-continuity named observation. **The fork record
appended:** the teaching-axis discriminator runs under STRUCTURED VARIATION, static
cells as baselines — grounds: the empty-gap lesson (a potent signal moves nothing
where nothing needs moving; §12.C) + exogenous differential fuel, the one ledger force
that isn't self-consuming. Governing line "Reality is the teacher" CITED to the
original Guiding-List entry (Guiding List.md), not duplicated.

**EXP10_STRUCTURED_VARIATION_PREREG.md drafted — AT CHECKPOINT, nothing builds.**
Carries: THE UNPREDICTABILITY PIN verbatim (binding, three clauses: unpredictable as a
sequence — no cycles/schedules, a deterministic rotation is a larger closed loop;
uninformative about identity — nuisance ⟂ member ⟂ word ⟂ category asserted
numerically at Step-0/manifest; learnable as a distribution — fixed recurring family,
family-predictable never instance-predictable). Harness reconciliation: dedicated
seeded nuisance stream — unpredictable to the system, deterministic to the harness;
replay contract (seed + construction order + threads=1) holds. Word jiggle: i.i.d.
scatter around FROZEN token centroids, token-only dependence, §10.11 reference
untouched, parent→varied-speaker staged for release — #12 applied to the input
distribution. Arms {no-detach, slowref, detachnull} × varied; static cells = existing
artifacts, NO re-runs; **no-detach-varied = the direct test: does exogenous variation
alone hold the ORIGINAL loop open.** Readouts: §L acquisition quality
ACQUISITION-ALIGNED (the parked lesson now mandatory); evocation-channel decomposition
= PRIMARY teaching axis; standing columns/panels; §10.14 scorer guards applied;
in-regime calibration mandate. Pre-registered confound: NUISANCE LEAKAGE — numeric
independence asserts + the nuisance-shuffle ablation. Step-0 re-validated under
variation; manifests re-cut (independence results as data); scatter renders per
rung/arm. §10.9 NAMED: structured backgrounds are structured-diffuseness territory —
if the cue-floor fires here it fires BY DESIGN; the banked §10.9 analysis is the
pickup. Checkpoint list = EXP10 §10 (8 items, incl. a possible two-stage checkpoint
for in-regime verdict constants). **Steps 5–6 blocked; checkpoint before anything
runs.**

**Pre-commit verification of the §10.14 unit + EXP10 draft (26 agents, 3 lenses,
per-finding adjudication): 19 confirmed findings applied.** Load-bearing: the
empty-gap CITATION corrected (§12.C records lift ≈ 0 at EVERY cell incl. hard bands;
the where-nothing-needs-moving half traces to the easy-band record only; §12.E scoped
the channel content-dead throughout — the ruled line stands as the design bet, the
citation now states what the record licenses); EXP10 §1's pre-pinned inference
corrected to the licensed form (a varied-arm hold shows CLOSURE was necessary too —
pull-necessity stays demonstrated; the draft's form would have contradicted
DETACH-CONFIRMED); the two-stage verdict-constants checkpoint made REQUIRED with a
calibration-source-distinct pin; the shuffle ablation's inference scoped
(read-time vs train-time to checkpoint); wrong-reason outcomes DRAFTED (leakage-pass /
pass-through variance / churn-in-costume, each with route) instead of an empty slot;
zero-variation replay parity + guarded-scorer re-scoring added as checkpoint item 9;
the jiggle stream brought inside the independence guards; the OOD rider and the
three-of-four qualifier carried into canon; PASS_PENDING_SCREEN tags restored in
§12.E. One finding OVERRULED with grounds the verifier lacked: the pin-block "glosses"
("gets absorbed"; "creates demand without re-closing the loop") are the ruling's own
verbatim text, not additions. One wording flagged for Jason rather than changed: "the
one ledger force that is not self-consuming" kept verbatim as ruled, with the
clarifier (supplied from outside the v1 rows; rows 5–7 fail for other reasons).

## 2026-07-04 — EXP10 CHECKPOINT PINS RULED → RESOLVED + WIRED + PARITY PASSED — at the final pre-run read

Ruling flags: empty-gap citation correction RATIFIED; closure-necessary-too inference
RATIFIED ("good catch — would have collided with DETACH-CONFIRMED"); outside-the-v1-rows
clarifier CONFIRMED; pin-clause overrule RATIFIED (chat provenance). Nine checkpoint
pins ruled and EXECUTED (full record: EXP10 prereg §11; `exp10_arms.py`;
`exp08/exp10_calibration.json`; `exp08/exp10_static_rescore.json`):

**Wired (one code path):** `_vary_word` identity-default hook added to Stage0Loop
build_cells (the ONLY loop.py change; identity everywhere except varied arms);
NuisanceStimulus = ConflictStimulus + the structured family (K=4 complement-block axes
@ Qᵀ — exactly ⟂ identity, measured 6.7e-7) or the isotropic discriminator at matched
power (1.3% verified); per-wave i.i.d. draws counter-keyed on the DEDICATED stream —
a varied arm shares BIT-IDENTICAL stim noise + masks with its static counterpart
(single-variable discipline; probe-shift caveat recorded). Three varied loops by MRO
mixin (word / slowref / detachnull). Smoke green (orthogonality, frozen anchor under
jiggle, MROs, power match).

**Calibrated (artifact-derived, never re-typed):** jiggle d_min 1.4019, σ_100% = 0.16
empirical (200k/token), σ* = 0.08 (5.7% of d_min, parent-voice); rung table ×0/0.5/1/2
→ (b) oracle 0.9557/0.9564/0.9557/0.9551 vs bar 0.625 — the ⟂ construction leaves the
ceiling unbound in range; PROPOSED operating rung ×2.0 (coeff_std 0.5 = total RMS 2×
r_category); independence asserts PASSING at the proposed point (nuis 0.0274 vs null99
0.0755; jiggle-residual 0.0567 vs 0.0817).

**PARITY GATE PASS (pin 9a, the hard gate):** the varied code path with variation
zeroed reproduces committed word_terminal_s1 BIT-IDENTICALLY (375 windows; standing
columns + grad_split + occupancy; the loop.py hook, the mixin MRO, and
NuisanceStimulus all exercised). **Guarded scorer v2 re-score (pin 9b): all four EXP09
verdicts UNCHANGED; guard (a) fired correctly on the two non-collapsing cells
(substitution GATED — the 19×/2.7× down-substitutions neutralized); baselines
FAIL_PIN (word_terminal) / NO_PIN (marathon_ext, legitimate 57000 substitution — the
run has collapse cycles).**

**At the read: ratify ×2.0 rung / σ*=0.08 / K=4 / seed budget → GO. Then: calibration
arm (seeds {10,11}, stage-two in-regime constants) → Step-0 (a)/(c) re-validation
under variation → verdict arms {nodetach_varied, slowref_varied, detachnull_varied,
nodetach_isotropic}. Steps 5–6 stay BLOCKED.**

**Pre-read verification of the resolution surface (22 agents, 3 lenses): 15 confirmed
findings applied — one changed a RATIFICATION NUMBER before the read could consume it:
the jiggle calibration was seed-0-only and the 100%-NC threshold is seed-dependent
(0.16 / 0.12 / 0.12 / 0.08 / 0.10 across run seeds; weakest basin d_min 0.894 at cal
seed 10) — the drafted σ*=0.08 would have sat at 1.0× the weakest seed's threshold.
RECALIBRATED CROSS-SEED: σ* = 0.04 = min-threshold/2 (4.5% of the weakest d_min), the
/2 rule preserved.** Also applied: sample-size wording corrected (200k TOTAL per seed,
~66.7k/token — not per-token); independence asserts RE-SCOPED to a calibration-time
machinery demonstration (the binding per-arm manifest-time asserts — realized pairing
of actual stream windows vs actual nuisance keys + the deployed jiggle residual + the
centroid-only regression check — land with the runner); cal/verdict seeds + stage-one
provenance now IN the artifact (the ruled "pinned in artifact" was unimplemented);
pin-4 SHARPENED (primary reads are nuisance-marginalized by construction — the
read-time shuffle cannot fire on them; it operates on nuisance-riding reads;
flag for ratification); isotropic match noted scale-exact by construction (verified
at 0.25); parity zip length assert added; varied-arm resume caveat recorded (no
resume-grade save — run start-to-finish); execution-status honestly re-scoped (pins
1,2,6,7,8,9 executed+wired; pin 3 calibrated, binding asserts with the runner; pins
4–5 ruled, constructions with the runner). Artifact regenerated
(`exp10_calibration.json` with per-seed jiggle table + seed pins + provenance).

## 2026-07-04 — EXP10 FINAL PRE-RUN READ: GO (rung fallback pinned); campaign launched

Ratifications: σ* correction ratified ("seed-0-only calibration was the exact
'comfortably inside' failure; 0.04 against the weakest basin is the pin as intended");
**rung ×2.0 with the RUNG-FALLBACK GUARD pinned pre-run** (no Step-0 observable exists
for the acquisition-floor risk → the guard moves to runtime: cal arm at ×2.0 first; NO
acquisition onset in EITHER cal seed where static baselines acquired ⇒ drop to ×1.0 +
re-cal before any verdict arm); σ*=0.04 / K=4 / seed budget as tabled; pin-4
sharpening ratified (manifest-time realized-pairing asserts carry primary-read
leakage); execution ledger accepted. **Sequence: build → cal (fallback-guarded) →
Step-0 re-validation → verdict arms → ONE review. Steps 5–6 blocked.**

## 2026-07-04 — EXP10 campaign harness BUILT + smoked; cal arms + Step-0 launched

Post-GO build (the remaining-ledger items): the ARMS10 runner (`run_exp10_arm` —
manifest asserts as a HARD pre-run gate → the shared A.run_arm code path with an
additive `exp10` spec key in build_loop → EXP09 probe set + the shuffle screen at
block cadence → acquisition-onset + aligned-read fields in the artifact); the BINDING
manifest-time asserts (realized pairing traced from a 200-step scratch loop — actual
stream windows vs the actual nuisance keys those waves consume; the DEPLOYED
`_vary_word` residual vs non-token labels AND vs token; the centroid-only check
(per-token residual mean bound); the per-arm σ* NC re-check on THIS arm's word
cortex; all vs live shuffle-null 99th-pct thresholds; hard-fail on breach); the
read-time shuffle screen on a nuisance-riding read (true vs row-permuted nuisance,
RNG-isolated); `acquisition_onset` (pinned form: num ≥ 0.01 in ≥2 consecutive
windows) + `acquisition_aligned_read` (k-window means from the arm's OWN onset);
`stage_two` (rung-fallback check FIRST, then in-regime constants by the §5
calibration rule from cal-arm healthy placements); `step0_revalidate` ((a) windowed
distractor floor 0.60 + (c) evocation divergence with the alive-precondition,
DEFERRED never false-pass). Runner smoked end-to-end (asserts PASS: realized pairing
0.093 ≤ 0.138, NC 1.0; probe + shufscreen columns land). Cal arms (seeds 10, 11 @
160k ×2.0 — the rung-fallback guard live) + Step-0 re-validation LAUNCHED.

## 2026-07-04 — EXP10 RAN → NEGATIVE result set, verified (FRONTIER §10.15); at the one review

Sequence executed: cal seeds {10,11} @160k ×2.0 (RUNG FALLBACK NOT FIRED — both
acquired, onsets 15k/21k) → Step-0 re-validation under variation ((a) distractor
0.71/0.62/0.76 ≥0.60 3/3; (b) ceiling unbound; (c) channel LIVE 3/3 share 1.000) →
12 verdict arms (threads=1; manifest-time asserts PASS every arm: realized pairing ≤
shuffle-null, deployed jiggle residual ⟂ labels+token, centroid-only bound, per-arm
σ*=0.04 NC=1.0) → score → adversarial verification (48 agents, 4 lenses; 36 confirmed
findings, 0 fabrication — every campaign number recomputed exactly).

**THREE OF MY DRAFT VERDICTS FLIPPED IN VERIFICATION (on the record):** (1) direct
test — my "terminal lock mostly beaten / onsets earlier than every static word arm" →
NEGATIVE: the no-detach loop is NOT held open (all 3 seeds routing-die, k1-only
asg-dead tails 69.3k/33.6k/45.3k waves, dead at horizon; word channel decoupled-alive
= the static signature with extended flicker); occupancy death at/before the static
word clock; word ACCELERATES routing death (no-word-metastable-earlier alternative
refuted, entry 9–27k vs marathon ~141k); closure-necessary-too DOES NOT fire,
pull-necessity via either-way clause; varied onsets beat only the static NO-DETACH
clock (45.3k n=1), tie the static stop-grad arms. (2) annealing — my "isotropic NEITHER
×3 = holds routing open equally" was a period-substitution artifact; the pinned route
STILL fires but A FORTIORI: isotropic (matched power, corrupts identity axes by
construction) is WORSE on every routing outcome (deeper joint-dead pockets 41.1k/29.7k
vs ≤18k; one horizon-terminal FULL PIN at matched period, iso s2 3.5 periods — no
structured seed reached it) → routing-openness NOT structure-specific → structured
ROUTING claim FALLS; the earlier-onset residue (3/3, 1.3–2.9×, n=3 ns) is CONFOUNDED
by cue-corruption, named-not-claimed. (3) evocation — "moved off common-dominated in
5/6" → only 3/6 full-run; the true change = differentiation channel ALIVE-at-horizon
5/6 (vs static decay), common-domination persists (evo_ratio>1 ≥99.6% windows).

**TEACHING AXIS = STOP-GRAD-IN-COSTUME AGAIN under variation:** no slowref-vs-null
divergence on any axis (both ROUTING-OPEN, 0 k=1/640, asg 1.6–1.73); all 3 leans
(live-frac, onset, evo_diff) favor the NULL; churn does NOT fire (acquisition present
all 12) → teaching bet UNDECIDED via NO-DIVERGENCE. **Fork 1(a) UNRESOLVED-NOT-REFUTED
on a 2nd independent regime.**

**SCORER BUG CAUGHT+FIXED (verification):** the both-period disclosure read still
applied substitution — hid iso-s2's terminal PIN; added a `force_period` path
(genuine pinned-period read); iso-s2 now correctly FAIL_PIN @4800. Stage-two note
self-contradiction fixed (claimed a terminal-exclusion not implemented; regime finding
survives exclusion-honoring recompute). Read-time shuffle low-power BY DESIGN
(nuisance-riding read 0.52–0.55 vs chance 0.50 — primary-read leakage carried by the
manifest asserts, as pinned). Honest labels in exp10_verdicts.json (static-calibrated
PASS-form stripped to OUT-OF-REGIME artifact; regime_label + both-period + onsets +
trajectories). Process note: Step-0 ran concurrent with cal (gate order preserved at
verdict launch; pin future = fallback-firing triggers Step-0 re-run).

**WHAT EXP10 SETTLES:** structured variation as operationalized does NOT hold the loop
open; the routing-openness variation does produce is not structure-specific; the
self-path reference stays undetectable vs its detach-null on a 2nd regime. DOES NOT
settle: stronger/among-cue variation, longer horizon, or a different teaching-axis
instrument. "Reality is the teacher" not refuted as a principle; this operationalization
didn't deliver. AT THE ONE REVIEW; no arm a fix; steps 5–6 blocked; next design move =
Jason's ruling.

## 2026-07-04 — EXP10 verdicts RATIFIED + next-move RULED: the denser anchor (EXP11 prereg at checkpoint)

Ratified: §10.15 as stated (EXP10 NEGATIVE; routing-openness not structure-specific;
costume 2nd regime; Fork 1(a) unresolved-not-refuted; live thread + onset residue
named-not-claimed; 3 flipped drafts kept as beats; a-fortiori iso + scorer catch = the
apparatus). "Reality is the teacher" scoped to this-operationalization-undetected,
principle untouched.

**RULING (FRONTIER §10.16): next move = the DENSER ANCHOR via the parked
acquisition-aligned ladder, BEFORE any counter-force.** Grounds verified against source:
every intervention so far acts on targets/inputs, detach-null matches-or-beats all
because nothing touches ROUTING differentiation; counter-force = manufacturing-class
drift (last resort, only on measured exhaustion); anchor = stimulus-side, no new
machinery, lever UNMEASURED — EXP08 ladder fell to CURRICULUM LAG not a null (num final
verified 2.262/2.297/0.191/0.771 across v2/4/8/16 at fixed 30k — dense under-acquired),
EXP10 built the aligned-read instrument that removes it; the ns occD-step-at-v4 fragment
(verified +0.095, largest) points the same way; word channel = sole #12 reference
surviving every collapse.

**EXP11_ANCHOR_DENSITY_PREREG.md drafted — AT CHECKPOINT, nothing builds.** Nested
ladder v2/4/8/16 (fixed maps b%2 / b / (a%2)·4+b / a·4+b, geometry untouched), STATIC
env (EXP08 comparability), ≥3 seeds/rung, horizon 160k [RECONCILE] (collapse regime +
v16 acquisition headroom). PRIMARY axis = acquisition-aligned reads per rung (EXP10
harness — read at each rung's own num-onset, removes curriculum lag; never-crossed =
ACQUISITION-CENSORED, unread not null). VERDICT axis = routing outcomes, asg_dist
(input-sensitivity) as the PRIMARY quantity NOT argmax_k count. Teaching-fence intact
(v≥4 never teaching evidence). **CENTRAL CONFOUND pre-registered = anchor-geometry
degradation:** verified pairwise MIN 1.402→1.139→1.047→0.829 v2→v16 (41% drop, mean
holds ~1.4) — "denser survives less" = density OR degraded separation; reading fork
(a) survives-more-despite-degrading = density dominates / (b) survives-less-AND-degrades
= confounded → matched-separation follow-up parked / (c) survives-more-AND-holds =
cleanest. **ANCHOR-AS-CRUTCH screen** = asg_dist survival, not argmax_k count (a larger
target set could mechanically floor collapse-to-one while assignment stays
input-insensitive). In-regime two-stage calibration + guarded-v2 scorer (EXP10 fixes).
Varied-ladder + matched-separation control + coarse-first ladder all PARKED with
triggers. Checkpoint list = EXP11 §9 (7 items incl. the adoption clause: ladder measures
the lever, adoption = separate ruling). Steps 5–6 blocked; no arm a fix.

**Pre-commit verification of the §10.16 ruling + EXP11 prereg (15 agents, 3 lenses): 9
confirmed findings; TWO BLOCKERS fixed before commit (real design revision, not
wording).** BLOCKER 1 — the "dense anchors under-acquired / curriculum lag" gloss is
REFUTED by the per-seed artifacts: EXP08 acquisition is a SEED LOTTERY (acquired 1/3,
3/3, 2/3, 2/3 across v2/4/8/16 — the SPARSEST rung v2 is the WORST; means each dominated
by one spiking seed), and the 160k horizon was justified from the word_terminal PIN
onset (75.3k, deployed-v2 collapse clock) conflated with a v16 ACQUISITION onset never
measured. Fixed: reframed as a lottery (stronger support for lever-unmeasured); horizon
now set from a MEASURED per-rung acquisition-onset PRE-FLIGHT (max onset + W_post +
margin); seed budget ≥5/rung sized so decisive rungs reach ≥3 ACQUIRED. BLOCKER 2 — the
VERDICT axis was taken at fixed absolute horizon while the PRIMARY read was
acquisition-aligned; denser rungs acquire LATER, so at a fixed horizon they've had FEWER
post-acquisition collapse periods and would look "survives better" as an artifact —
re-introducing the confound the aligned read removes. Fixed: BOTH axes now
acquisition-aligned — routing survival read over a MATCHED POST-ONSET WINDOW (in
collapse-periods), comparing rungs at matched collapse-phase. Also applied: VARIABLE
renamed density→COVERAGE (cardinality/coverage collinear in the nested ladder →
coarse-first control parked); geometry MIN drop corrected 41%→~26% (41% was
seed-1-only; per-run anchor mean 1.208/1.120/1.046/0.889 v2→v16); crutch screen Form-2
residual NAMED (a mandatory-distinct 16-target reference can mechanically force asg_dist
high — matched-diversity assignment-collapsible control parked; scaffold = CONSISTENT
not DEMONSTRATED until it runs); occD +0.095 method-pinned (last-minus-first-block
mean-over-seeds; direction robust, magnitude aggregation-sensitive); num finals flagged
outlier-dominated (medians/acquisition-counts cited). Canon (§10.16), §12.E, and the
EXP11 prereg all corrected. Checkpoint list = EXP11 §9 (7 items).

## 2026-07-04 — EXP11 §9 pins ratified; harness built; PRE-FLIGHT done; verdict arms launched

§9 pins ratified verbatim (seeds ≥5/rung + ≥3-acquired + one +2 extension then
ACQUISITION-STARVED, cal seeds distinct; horizon = max onset + W_post + margin; W_post =
3 collapse periods in the rung's OWN regime + in-regime asg_dist threshold; geometry fork
tolerance from per-run distribution + matched-separation control RUNS ALONGSIDE;
Form-2/crutch control parked-until-positive; adoption clause verbatim; probes ride
read-only zero-marginal-run). Harness `exp11_arms.py`: MatchedSepVocabLoop
(closest-anchor-pair rotation to a common target min-sep, UNIT NORM preserved exactly —
smoke: v2/4/8 matched 1.402/1.139/1.047 → 0.896, v16 natural 0.829; anchor frozen);
build_loop issubclass patch; both-axes-aligned verdict read (matched post-onset window).

**PRE-FLIGHT (8 cal runs, seeds {20,21}, 130k; `exp11_preflight.json`): all 4 rungs
acquired 2/2.** Per-rung onsets v2 [15300,15000] v4 [9300,15000] v8 [9300,45000] v16
[15300,45300]; per-rung collapse periods v2 12000 / v4 5400 / v8 30000 / v16 4800 (n=2,
thin — caveat). **HORIZON = 45300 (max onset) + 3×30000 (max period) + 12000 margin =
147300.** Verdict arms launched: 20 natural (4 rungs × verdict seeds {0–4}) at 147300,
matched-separation control to follow. Each rung's verdict reads at 3 periods in ITS OWN
regime. Steps 5–6 blocked.

## 2026-07-04 — EXP11 RAN → INCONCLUSIVE (FRONTIER §10.17); both my draft verdicts refuted in verification

40 verdict arms (natural + matched-sep, 5 seeds/rung, all 5/5 acquired) + adversarial
verification (37 agents, 4 lenses, 20 confirmed findings; every artifact number + all
construction integrity reproduced clean — threads=1, spec_hash consistent, teaching
fence intact). **My draft (clean COVERAGE-NULL + a new inverse "tighter-anchor-helps"
lever) was WRONG on both counts — honest verdict INCONCLUSIVE.**

Real (estimator-free full-post-onset window): natural ladder asg_dist survival rises
~monotone with coverage (v2 0.033 → v4 0.137 → v8 0.158 → v16 0.179, 5.4×) — BUT
coverage collinear with anchor min-sep (v2 1.205 → v16 0.896) AND onset. **COVERAGE-NULL
NOT established:** the matched-sep control is CONFOUNDED — non-uniform closest-pair
rotation perturbs v2 heavily / v16 ~zero, so its flatness comes from lifting ONLY v2
(within-rung nat→ms: v2 +0.130, v4 −0.001, v8 −0.040, v16 −0.016), an artifact not
evidence coverage is inert; underpowered n=5 (matched-sep pairwise |t|<0.7).
**"Tighter min-sep lever" STRUCK:** no within-rung dose (coverage-fixed effect is
entirely v2, the most-perturbed rung); pooled corr(min_sep,asg)=−0.38 is
coverage/perturbation collinearity wearing a min-sep mask. Loose thread (named, not a
mechanism): heavily re-perturbing the v2 category-only anchor lifts survival ~4× via an
UNIDENTIFIED channel (min-sep/mean-sep/onset/generic-redraw all co-vary; persists at
matched onset — early means 0.281 vs 0.057).

**INSTRUMENT LESSON (scorer correction, canonized like EXP10 force_period):** the pinned
"W_post = 3 collapse periods in the rung's OWN regime" window is UNUSABLE — the per-rung
den-period estimator is fallback-dominated (3/5 failures → PERIOD_WORD=4800 fallback),
swings 6× (cal 30000 vs in-regime 4800), so the window is arbitrary-length and it
manufactured the draft's non-monotone "v8 peak / 5.0× endpoint" (v8 short fallback
window caught only its plateau). RETRACTED for the estimator-free full window (kept in
artifact for provenance). §4 fork's directional assumption (degrading min-sep hurts) was
wrong; reality came orthogonal; the machine geometry_fork string is stale/inverted, not
quoted.

**HONEST ANSWER: EXP11 cannot answer the ruling's question cleanly; the anchor lever
remains UNMEASURED (flawed control, not a null).** Clean redo needs: UNIFORM
matched-min-sep control (re-draw all rungs to common min-sep by one method, or D-scaling
— NOT non-uniform closest-pair rotation); fixed common post-onset window; more seeds; the
loose-thread control (perturbed-same-min-sep vs tighter). **DECISION FOR JASON: clean-redo
the anchor vs move to the routing-side counter-force (manufacturing-class last resort).**
Steps 5–6 blocked; no arm a fix. Artifacts: exp08/cov*_s*.json (40), exp11_verdicts.json
(HONEST_READ; period-normalized RETRACTED), exp11_preflight.json.

## 2026-07-04 — EXP11 INCONCLUSIVE → static-frame line RETIRED; continual time promoted to primary frontier

EXP11 (anchor-coverage ladder, acquisition-aligned): verified INCONCLUSIVE — the anchor lever is
UNMEASURED (the matched-separation control was non-uniform: closest-pair rotation perturbs v2
heavily, v16 barely; its "flatness" was construction artifact, not a null). Natural-ladder rise is
real (asg_dist 0.033→0.179, v2→v16, 5.4×) but coverage ∥ min-separation ∥ onset — unattributable.
"Tighter min-sep lever" STRUCK (no within-rung dose-response; collinearity in a mask). v2
re-perturbation loose thread (~4× survival, unidentified channel) NAMED, not claimed. Scorer catch
canonized: per-rung den-period estimator fallback-dominated → verdict window retracted for the
estimator-free full-post-onset window. Third campaign where verification flipped a surprising
draft verdict (EXP08, EXP10, EXP11).

**RULING — wrap, not redo.** Clean-redo design BANKED as pickup (uniform matched-min-sep or
D-scaling; fixed common post-onset window; ≥ seed floor; loose-thread disambiguation arm); the
coverage question re-poses inside EXP12 where the answer is load-bearing. Counter-force stays
parked (trigger = measured exhaustion; inconclusive-by-flawed-control is not that, and its static
venue is retired).

**Static-line ledger (canon: FRONTIER wrap unit).** Proved: channel carries end-to-end (first live
word→category evocation, Gate 4); dead-dictionary localization (assignment-side, capacity open,
prototypes alive); engine = no-detach target-side pull (necessity demonstrated); word = ~5×
accelerant + pin-deepener, fate shared end-to-end; prevention-primary / recovery-unreliable;
stop-grad-in-costume on two regimes (Fork 1(a) UNRESOLVED-NOT-REFUTED); the instrument arsenal +
determinism contract (seed + construction order + threads=1). Manufactured [COHERENT-DEDUCED, not
demonstrated — the motivating hypothesis EXP12 tests]: task degeneracy — i.i.d. draws make the
deck-average nearly optimal, starving member-conditional routing by construction. Gate steps 5–6
RETIRE with the line; the teaching test re-poses in the continual-time rig at its own gates.

**Next: EXP12 (scene persistence — minimal temporal fabric).** Pre-committed: shuffled-dwell
discriminator from day one; the unpredictability pin (3 clauses) carries; anchor arm carries the
banked design; acquisition-aligned reads, in-regime calibration, guarded scorer v2, panels. Opening
fork for the next session: what within-dwell evolution is, mechanically. Handoff:
`docs/HANDOFF_next_chat_continual_time.md`.

*(Hash fill, flagged at session open: the wrap unit above committed as `0f5d971`; the four-cell
pre-registration follow-up as `8abc338`.)*

## 2026-07-04 — EXP12 SCOPING SESSION (design chat): five forks resolved; prereg RATIFIED FOR BUILD; canon unit §10.19

The continual-time scoping session (Jason + design chat) resolved all five EXP12 forks and
ratified the prereg for build. **F1** walk law = stochastic OU jitter around the dwell-onset pose
(one fixed law, global hyperparameters; struck overclaim on record — routing demand lives in mask
geometry + onset rate, not the walk). **F1 amendment** background recurrence: v1 = ONE fixed
background configuration (pin-to-constant) + OU jitter; familiarity earnable; familiar background
earns LOW prediction error, the new object is the high-divergence residual. **F1.5** wave-local
completion (no trace in v1 — persistence-as-gradient-ordering ONLY; a v1 null is NOT
fabric-refutation) + guaranteed onset exam (word-masked first wave); division of labor: onset =
routing exams (verdict axis) / mid-dwell vision-masked = teaching channel; never crossed;
shortcut-through-recency pre-registered as the wrong-reason outcome. **F2** dwell law k = k_min +
Geom(p) capped (constant hazard, the only clockless law); k ⟂ member + cap-hit ceiling as binding
asserts; member draw uniform no-immediate-repeat. **F3** 12b gated with two openers (promote-cell
full-seeds teaching test | both-die reduced-seeds word-culprit discriminator); absent-word not
scrambled-word. **F4** baseline banked, two openers; escalation ladder BINDING baseline → 12b →
visibility rung; thermometer-not-donor fence; generality read one-directional.

Checkpoint ratification: §13 constants (walk = EXP10 pinned nuisance family VERBATIM, τ=4,
stationary sd = 0.25·family-σ derived not pinned; dwell p=0.1/k_min=2/k_max=48, cap ceiling 1%;
mask one-slot-per-wave, mid-dwell 50:50; EXP10 num-floor onset carried; W_post ≥ 3 own-regime
collapse periods with the PRE-REGISTERED fallback ladder (own period → fixed calibrated
absolute-wave window) — the EXP11 estimator caveat going live on schedule; survival =
category-partition asg_dist ≥ stage-two threshold, seed majority ≥ 3/5 with the MARGIN GUARD
(any 3–2 split fires +2 extension BEFORE table interpretation); baseline params within ~2× of
PAM's plastic side; cal seeds {20–24} n=5, verdict {0–4}, +2 pool {5,6}; boundary-leak monitor =
position-matched schedule-unmatched read-only probes at suppressed-exam dwell onsets).
Amendment B (survival-read geometry pin): verdict = category-partition input-sensitivity; 16-way
survival is the ladder's question, never rig-1's. Registered prediction (cross-scene contrast:
word accelerates differentiation on live fabric — same channel, opposite sign) + registered
observable (earned salience) on record with pre-named falsifiers.

Canon writes this commit: prereg `docs/EXP12_SCENE_PERSISTENCE_PREREG.md` (verbatim, ratified) +
build handoff `docs/HANDOFF_CC_exp12_build.md` + FRONTIER §10.19 (fork rulings) + Guiding List
candidate (HELD: "word = moving stability matching the object; environment = standing stability
behind it"; promotion trigger = both registered observables landing) + §12.E pointer + this
entry. Next: CC-verify list → build → stage-one calibration numbers reported to chat BEFORE any
stage-two constant is set. Banked arms built-when-fired. No arm is a fix.

## 2026-07-05 — EXP12 harness BUILT (canon b2898c8, harness a98b45a) + STAGE-ONE RUN; stage-two WAITS on the chat read

**Build (wave-local rig, one code path):** `exp12_fabric.py` (pre-generated world on 9 dedicated
substreams; k = 2+Geom(0.1) cap 48; per-axis OU τ=4 with STATIONARY-DERIVED per-step σ
(0.1654·σf), reflect ±3σf; pin-to-constant background (fixed key 94000, identical across
seeds/arms) + continuous OU jitter; guaranteed position-1 word-mask exam; mid-dwell 50:50;
BOTH per-dwell coins drawn every dwell → probe-rate changes leave downstream draws ALIGNED and
probe sets NESTED; per-lag(0–48)/k/schedule/background ⟂ member asserts vs dwell-permutation
nulls, all HARD) + `exp12_arms.py` (EXP12Loop: W=1, step() inherited unchanged, A-SHUFFLE =
identical waves + identical masks order-shuffled, loop.gen bit-parity across arms asserted;
reads: asg_cat verdict-designate = L1 between category-conditioned mean assignment vectors +
16-member companions, onset-exam lift/acc, mid-dwell companions, earned-salience divergence
split (id/nuis/bg), per-position curves split by masked slot, §13.10 probe machinery PRE-update)
+ `exp12_baseline.py` (thermometer, 11,728 params = 1.04× PAM plastic side 11,281; B1/B2; fence
asserted). Wave-local consequences SURFACED (not silent): L_JEPA inert by construction (also
idles the deployed loss's one next-wave-prediction term); no u-carrier (within-window order does
not exist at W=1); EXP10 word jiggle not carried (prereg fabric enumerates nuisance+background
only).

**Adversarial review BEFORE first run (32 agents; 15 confirmed → 5 distinct, ALL FIXED):**
(1) MAJOR probe-dwell branch consumed an extra g_mask draw → any stage-two rate change would
have reshuffled the whole downstream mask schedule (the §13.10 invariant's stated purpose
defeated) → both coins now drawn every dwell, alignment + nestedness regression-tested;
(2) MAJOR the §13.10 probe read was POST-update vs the scheduled exam's PRE-update stash —
re-introducing the recency channel position-matching exists to remove → probe now reads
pre-update in the runner; (3) MAJOR stage-one period read leaned on the static line's
4800-pin/1.5×-band/20100-cut estimator (§10.14 ban; §10.17 lesson) → replaced with the
estimator-free in-regime dynamics-panel read; cycle-present-period-unmeasured now labeled
exactly that, never folded into the no-cycle fallback; (4) pos_err pooled word-cell and
vision-cell error scales → split; (5) probe-dwell onsets contaminated the mid-dwell companions
→ excluded. 13 findings refuted in verification (incl. the asg_cat mean-cancellation concern
and the per-lag stride worry; stride tightened to 1 anyway).

**STAGE-ONE NUMBERS (cal {20–24}, 120k horizon, threads=1; artifacts exp12_*_s2*.json +
exp12_stage1.json; NO stage-two constant set):** fabric at scale verified (mean k 11.89,
cap-hit 0.70% vs 0.785% theory, all asserts green). A-DWELL onsets: {s20 NEVER (censored),
s21 41.1k, s22 3.3k, s23 31.2k, s24 50.1k} — 4/5 acquired. A-SHUFFLE onsets: {3.3k, 3.0k,
2.7k, 4.2k, 3.3k} — 5/5, ~10× earlier. Collapse cycles: dwell 3/4 acquired seeds (periods
44.1k / 28.2k measured; one present-unmeasured; s23 none), shuffle 4/5 (57.9k / 21.6k / 24.9k /
29.4k; s21 none) — periods are LONG (20–58k), so W_post = 3 own-periods implies ~60–170k
verdict windows (horizon consequence for §13.9). Onset-exam channel AT CHANCE in BOTH arms
(acc 0.48–0.51, lift ≈ 0/negative) at 120k — the deck-mean word completion, a regime fact for
stage-two threshold design. asg_cat post-onset: dwell ends mostly ≈0 (0.0006/0.0006/0.0001;
s24 0.035) with asg_dist 0.16–0.61; shuffle ends higher on 4/5 (0.051/0.017/0.101/0.050/0.002)
with asg_dist 0.12–0.25. NOT a table read (cal seeds, no thresholds, unmatched windows).
**DISCREPANCY SURFACED (not patched): the ratified §13.2 constants (E[k]=12, cap≈0.8%) entail
Geom support ≥1 → realized dwell support is k∈{3..48}; k_min=2 is unrealizable as built, so the
prereg's "k=2 tail" language and the law disagree at the margin — Jason's call.** Stage-two
(survival threshold, W_post, B1/B2, probe rate, verdict horizon) NOT set — waits on the chat
read per the handoff.

## 2026-07-05 — Prereg AMENDED IN PLACE (Rulings 1–2 + guards, cross-reviewed); corrected-law RE-CAL; the FIRST MEASURED FABRIC FACT named; stage-two PROPOSED (canon §10.19.1)

Jason's amendments landed in place (forward-pointer rule; commit 6872add): **Ruling 1** dwell
law = 2 + Geom₀(0.1), support {2..48}, k_min=2 REALIZABLE (E[k]=11, cap ≈0.7%; the as-ratified
arithmetic embedded a support error — the pin's grounds outrank the constants' letter);
**Ruling 2** primary VERDICT read = category-partition asg_dist at aligned windows (forced by
Amendment B), onset-exam completion lift = registered COMPANION never the cell-decider;
**sensitivity-without-conversion** registered as a pre-verdict finding class (num-floor onset
vs exam-conversion onset — the dissociation is data); the W=1 anti-forward RECORDED GUARD;
W_post SIZING PIN; CENSORED-SEED accounting (unread never dies; +2 fires on read-count
shortfall); censoring-aware §13.9 onset bound. Cascades executed: law re-pinned + verified
(min k=2, P(k=2)=0.100, cap 0.73% vs 0.707% theory); §13.8 asserts re-run green on the new
support; the stale-law 120k bound DISCARDED, re-cal at 160k.

**Corrected-law re-cal (cal {20–24}, 160k, both arms + baseline on identical fabrics; canon
§10.19.1).** THE FIRST MEASURED FABRIC FACT, named so nobody "fixes" it: **shuffle acquires
~10× faster than dwell on every seed** (shuffle onsets {2.4–7.8k} 5/5; dwell {6.3k, 31.8k,
103.2k} + 2 CENSORED at 160k) — and the out-of-family baseline REPRODUCES it on the identical
fabric (B2 acc: shuffle 0.93–0.96 all 5; dwell 2/5 trained, 3/5 chance) → a TASK property; the
acquisition-aligned machinery is what keeps it out of the four-cell table.
Sensitivity-without-conversion already visible: num fires while the exam channel sits at
chance in both arms; the draft conversion form (acc≥0.6 ×2) false-fired on 60% of chance
segments → rejected for the chance-band form. Periods: dwell {18.6k measured, 1
present-unmeasured, 1 no-cycle}; shuffle {43.8k, 9.3k measured, 1 present-unmeasured, 1
no-cycle} — up to 4.7× within-arm estimator spread (§10.17 instability, in-regime as
expected).

**Stage-two constants PROPOSED, not in force** (`exp12_stage2_constants.PROPOSED.json`): onset
bound ≥160k (censoring-aware); W_post ladder per arm (dwell 55.8k / shuffle 131.4k own-period;
recommendation = the fixed COMMON 131.4k window, EXP11-lesson-consistent); verdict horizon
303.4k; survival θ RECOMMENDED dead-p95 = 0.0057 (alternates p90 0.0004 / p99 0.0267 surfaced;
the choice is DECISIVE on cal spans — dwell 1/3 + shuffle 2/5 above p99 vs 3/3 + 5/5 above
p95 — which is why it is ratified, never read off); probe rate 0.02; baseline B1 floors
(dwell/shuffle from its own pre-differentiation bands) + B2 floor 0; conversion form =
chance-band p99 (acc ≥ 0.704) ×3, measured false-fire 0. **Verdict arms (seeds {0–4}, +2 pool
{5,6}) run only after ratification.**

## 2026-07-05 — EXP12 RIG-1 VERDICT: **BOTH-SURVIVE** (verified 28-agent/18-findings; canon §10.20); the splitting arm's trigger fires

Stage-two ratified in chat (Rulings A/B, pins i–iv, symmetric B2) → constants IN-FORCE
(3120f54) → verdict arms {0–4} × both arms at 303,400 waves, probe 0.02 → scorer → the
verification pass BEFORE the table. **THE CELL: A-DWELL SURVIVES (read 4: 3S/1D; s0 UNREAD
window-truncated per pin i) · A-SHUFFLE SURVIVES (5S/0D, θ-robust 4.4–25.5×). Registered
reading applied as pre-registered: variation + exam-scheduling jointly suffice; root REFINED,
not confirmed; the splitting arm (shuffled + uniform masking) is the pre-registered trigger
that now fires (built-when-fired, awaiting GO).**

Verification texture (18 confirmed, none cell-moving; 2 reading-changing): (1) the window-MEAN
form certifies W_post-mean input-sensitivity, NOT alive-at-horizon — decoupled in this
oscillatory regime (shuffle s3 passes at 0.0915 yet 98% dead-signature at run end; collapse is
not abolished on this fabric, it is delayed/reshaped); (2) θ-provenance: the dead reference is
85% shuffle windows (~32× arm-asymmetric tail) → θ is CONSERVATIVE against dwell survival and
the p99-ANOMALY alternate is defused as a shuffle-tail artifact; (3) my draft "shuffle converts
3/5" gloss STRUCK in verification (band-edge flicker; s2 misdated ~219k; s1 de-converts) —
**sensitivity-without-conversion holds ARM-WIDE** (both arms asg-alive/exam-at-floor at 303k);
(4) mode asymmetry: shuffle survival sustained (frac-above 0.80–1.00), dwell survival an
intermittent duty-cycled revival mode (0.34–0.56; s1 = late-revival, alive-at-horizon, the
suspected wrong-reason shape INVERTED); (5) arm-wide ordering inversion (min shuffle mean >
max dwell; the §10.19.1 fabric fact continuing into survival); (6) §13.10 monitor has NO
registered bar (gap on record) — dwell 4/4 positive paired deltas (max t≈+2.3), not a
registered fire, fallback (c) stays unfired; (7) two latent scorer defects fixed UNEXERCISED
(margin predicate letter-exact 3–2 only; extensions gated on guard-fire). Fourth campaign
where verification materially corrected a draft reading (EXP08/10/11/12 — this time a
companion gloss, not the cell).

## 2026-07-05 — SPLITTING ARM: **SURVIVES 3S/0D → VARIATION ALONE SUFFICES on the registered ruler**, bounded by a 2–3× scheduling dose effect + 2/3 horizon deaths (canon §10.20.1; verified 16-agent/12-findings)

Registered block (prereg §14) recorded BEFORE launch; fired on Jason's GO. Construction
verified BIT-LEVEL: A-SPLIT = A-SHUFFLE fabric verbatim per seed (tensors torch.equal;
mid-dwell masks bit-identical; all 13,426 mask diffs at position 1; draw parity free — the
always-drawn onset coin is used instead of ignored). Seeds {0,1,2} at the in-force constants
verbatim. **READ: 3S/0D (0.0348/0.0469/0.0077 = 6.2×/8.3×/1.35× θ; onsets 3.3–3.6k; no guard
fires). Pre-named mapping: variation alone suffices for REGISTERED routing survival — the
guaranteed onset exam is not necessary; EXP10's variation thread confirmed on live fabric.**

Verified bounds (all recomputed, none verdict-changing): scheduling = a 2–3× DOSE factor on
every paired seed (0.60×/0.32×/0.31× of the scheduled twin; worst margin 4.4×→1.35× θ); at
HORIZON split dies 2/3 where the twin lives 3/3 (exam scheduling looks load-bearing for
persistence-to-horizon — the natural next question, not a verdict; window-mean≠end-state cuts
both ways); s2 dying-in-window (front-loaded margin; estimator-free form reads 0.88× θ;
adjacent forms → 2S/1D backfill letter — fragility on record, read stands as registered); the
uniform coin also RAISED teaching density +9.7% (second moved channel, named — exam-loss vs
teaching-gain not separable in this arm); acquisition unchanged-or-EARLIER (10500→3600 at s1)
— acquisition rides the teaching channel, not the exams; FIRST REAL exam conversions of the
campaign in split s0 (late, 16-consec sustained, accs to 1.0, outside the verdict window) —
sensitivity-without-conversion carries a per-run exception; conversion band mis-calibrated at
halved exam density (~4× hot; density-matched band = a constants item for exam-rate-changing
arms). §14 guard letter now has a committed producer (exp12_score.py --split). Ledger:
root stays REFINED — variation sufficient, exams buy margin + horizon persistence,
dwell-ordering buys neither. Four-cell table untouched. No arm a fix.

## 2026-07-05 — POST-SPLIT RULINGS EXECUTED + 12b CAL: **REGIME FINDING — the zero-prediction-load word is INERT** (canon §10.20.2/§10.20.3); verdict twins DO NOT run pending ruling

Rulings 1–6 recorded (canon §10.20.2; prereg amended in place): 12b trigger →
routing-alive-arm-wide; registration re-cut (SELECTIVITY primary, speed companion);
regime-bound rider on §10.20/§10.20.1 (non-generative fabric; lawful-dynamics worlds = named
future rung; continual motion deferred not demoted); parallel-blocks standing principle; s2
backfill by ruling after §14 verdict-invariance; density-matched conversion band registered.

**s2 backfill: both READ SURVIVES (0.0663/0.0227 = 11.7×/4.0× θ) → A-SPLIT 5S/0D** — the
registered read strengthened, s2 stays the floor case.

**12b (prereg §15, amended trigger):** twin harness built + CC-verified (exposure loss-skip
clean; twin parity torch.equal ex-word; null-token convention; per-partition sep columns);
one build catch (shuffled-twin checksum rebuilt without word_ref — died at the assert
pre-training, fixed, relaunched). **Cal twins ({20–24} × 2 × 2, 160k): num max over ALL 20
runs = 2.6e-5 (vs 0.284 scheduled, same seed); onsets None 20/20; present ≡ absent on every
panel. The word as pure reference NEVER BINDS — participation appears to require prediction
load somewhere. Third dose rung measured: zero word-prediction load → channel never forms AND
the world collapses harder (9/20 dead-dictionary ends, 15/20 den sub-floor; dwelled twins
fully dead most seeds).** Constants NOT settable (no aligned-window support; S unread + raw
form unbounded — bounded form proposed for any re-pin; dead regime shifted 1.5×, θ not
transportable unflagged). The registered S prediction is UNTESTED, not falsified. Ruling
required; candidate re-poses surfaced in chat (re-pin twins onto the split coin-exam policy |
rule inertness the block's answer). No verdict twin runs.

## 2026-07-05 — 12b RE-POSED at the COIN POLICY (ruled; (iii) STRUCK, finding recorded); coin-policy cal RUN; stage-two SURFACED — verdict twins await ratification

Ruling executed: prereg §15 amended in place ((iii) struck with the finding as the record);
present twin = A-SPLIT coin policy verbatim; absent twin = same coin same draws, word-mask
draws → EXPOSURE-ONLY (the original option (ii) — rejected then as a dose confound, correct
now because THE DOSE IS THE MECHANISM); vision-teaching density matched by construction; dose
control = S itself (untied subtraction; selectivity = the dose-robust axis, earning its keep);
BOUNDED S form ratified (between/(between+within); sep columns bounded from 36f0d7f); nothing
transports — all constants fresh-cut.

**Coin-policy cal ({20–24} × {present, absent} × {sh, dw}, 160k): the channel is ALIVE where
(iii) was dead** — num_max present 1.38 (vs 2.6e-5 under (iii)); absent 9e-6 = never, by
construction. **sh block:** present onsets {3.6k, 3.9k, 9.0k, 5.4k, 6.3k} 5/5; null band
(pre-onset S) p99 = 0.0414 (n=89 — THIN, flagged: fast acquisition leaves little pre-onset
span); sustained-N = 2; post-onset S preview ALL FIVE POSITIVE {0.062, 0.006, 0.175, 0.023,
0.042} — preview only, never a band input; horizon 152,400 (= 9,000 + 131,400 + 12,000).
**dw block:** present onsets {27k, 18.3k, 60k} 3/5 + 2 CENSORED at 160k (the dwell lottery at
coin policy); null band p99 = 0.1251 (n=1414); sustained-N = 4; preview mixed
{−0.026, +0.004, −0.024}; horizon 303,400 + full UNREAD/truncation machinery. Fresh dead
reference (companion only): p50 4.8e-5 / p95 0.00775 (θ_companion proposed) / p99 0.0141
(n=1188). Untied-untied companions p99 0.45/0.55. Artifact
`exp12_12b_stage2.PROPOSED.json` — **NOTHING IN FORCE; constants surfaced in chat; verdict
twins {0–4} × 2 twins × 2 blocks run only after ratification.**

## 2026-07-05 — 12b VERDICT TWINS: **sh S-FIRES 5F/0N · dw S-NULL 0F/3N** — verified 14-agent; the fire's composition DECOMPOSED (canon §10.20.4); rulings owed

Ratified (widen + fences) → sh band RE-CUT 0.049689 (n 89→348; widening RAISED the bar; N=2
re-checked; s26 onset 64.8k surfaced — the sh acquisition tail exists, donated the band's
fattest null span) → constants IN-FORCE 48f0784 → 20 verdict twins (sh @152.4k, dw @303.4k)
→ scorer → verification BEFORE the table (14 agents, every number reproduced to the digit,
none verdict-changing).

**[sh] S-FIRES 5F/0N letter-valid** (runs 17–145 vs N=2; S_max 0.23–0.66) — **but the
verified composition changes what the fire is: the untied subtraction ADDED instead of
cancelling** (untied term +0.048..+0.085 in every fire event; Δsep_a NEGATIVE — the dying
absent twin collapses ONTO the coarse partition, 0.69–0.79 vs present 0.53–0.71); word-tied
Δcat positive in every fire event (0.023–0.064) but minority share (26–48%). Two regimes:
s0/s2/s3 sustained positive-S (means 0.08–0.18); s1/s4 duty-cycled net-≈0 (s1 cat signal ≈0,
artifact-compatible). "Acting selectively on what it names" NOT licensed as-is; licensed: the
word RESHAPES geometry away from the no-word collapse + is strongly HEALTH-PROTECTIVE
(falsifier (a) ANTI-fires; absent den-subfloor 0.72–0.89 vs present 0.0–0.48).
**INSTRUMENT LESSON: the untied control legs are contaminated by the comparator's own death**
— dose-cancellation assumed a healthy absent twin; a collapsing one turns the control into a
signal carrier. Any S re-cut = a ruling, not a scorer patch.

**[dw] S-NULL 0F/3N, stronger than drafted** (read-seed S_max 0.147–0.162 = the null pool's
own tail, p99.5 0.161 max 0.196; null runs reached 3, N=4 doing its job); s0/s1 UNREAD
window-truncated (187.8k/274.5k — the pre-acknowledged lottery); 3 reads = minimum, no guard.
Health effect present without selectivity (present asg_cat 0.017–0.024 vs absent
0.004–0.008). Falsifier (b) fires for the dwelled block.

Corrections on record: falsifier-(a) universal → preponderance (dw s2 den-subfloor worse in
present, 0.153 vs 0.093; 7/8 clean); s26/horizon internal-consistency note (in-force 152.4k
= thin-pool form; widened-pool form = 208.2k; ~1/10 sh truncation lottery, did not bite, max
verdict onset 5.1k; verdict-conservative); scorer t-assert added (all pairs verified
aligned). **Ledger: word on live fabric = health-protective (both fabrics) +
geometry-reshaping vs no-word collapse (sh, letter-fire) + NOT yet word-tied-selective in the
registered sense + inert without prediction load (§10.20.3). Rulings owed: sh-fire
interpretation, any S re-cut, dw follow-ups.**

## 2026-07-05 — S_w FRESH-SEED VERDICTS (canon §10.20.6; verified 18-agent): **sh S_w-FIRES 4F/0N ROBUST — word-tied selectivity DEMONSTRATED on the shuffled fabric · dw 3F/1N FRAGILE (seed-batch, not ruler)**

S_w registered (§10.20.5) → bands from existing cal (sh 0.006353 n=348 N=2; dw 0.019755
n=1414 N=5) → fresh seeds {5–9} both blocks → verification BEFORE the table (18 agents,
mechanics exact, none verdict-changing). One pre-run event: sh s9 fabric REJECTED by the
k⟂member gate (chi2 85.36 vs 83.42; verified OUTCOME-BLIND, pre-wave-0; ~1 marginal breach
in ~29 fabrics at a 1% gate; committed record exp12_12bc_sh_s9_REJECTED.json; sh reads on
{5–8}; s10 substitution = a ruling, not improvised).

**[sh] 4F/0N ROBUST:** weakest fire 25× the null rate (null: 3/348 above band, max run 1);
s5 showcase mean 0.0453/frac 0.565/run 77; duty-cycle regime present (s6 negative mean,
oscillatory, still 24 runs ≥2 vs zero in null). Dose-visibility passes on the CORRECT
normalization — no untied leg fires its own band on any sh seed. INSTRUMENT NOTE recorded:
raw-magnitude "Δcat ≫ untied" is scale-mismatched (untied nulls 40–60× wider); the check
is each-leg-vs-its-own-band only. Caveat: sh null 62% one seed (s26).
**[dw] 3F/1N letter-valid, FRAGILE:** s5 persistence-only (run 59 = 14.8× null max run,
amplitude inside the null tail); s7 mirror-oscillatory (below-band run 20 > fire run 15);
s8 band-adjacent AND its dA leg would fire its own band (the like-for-like failure); s6
clean null; s9 truncated. **CROSS-RULER DECOMPOSITION (post-hoc companions): the dw flip
is SEED-BATCH, not ruler — each batch same letter under both rulers** (dw {2,3,4} S_w
0F/3N; dw {5–9} composite-S 3F/1N); combined dw 3F/4N over 7 reads = a seed lottery at
current power. Health: sh unchanged (word-present much healthier); dw INVERTS on den
(present subfloor higher 3/4) while asg_cat favors present — fabric-dependent.

**STATUS: the registered cross-scene contrast is DEMONSTRATED on the shuffled fabric —
the ~5× collapse-accelerant channel, on live fabric, selectively differentiates the
partition it names (fresh seeds, robust null, untied legs quiet). Dwelled: letter-fire,
not demonstration-grade. Rulings owed: dw standing, s10 substitution, any Guiding-List
promotion touched by the sh demonstration.**


---

## 2026-07-06 — EXP12 §10.20.7 RULED: standing substitution rule (sh s9→s10) + earned-salience read registered; recorded BEFORE the substitute runs / before the read

Jason's order: "record §10.20.7, standing substitution rule, earned-salience read —
results here." Recorded in canon (FRONTIER §10.20.7) + prereg §15 pin + scorer touch
(`SW_SUB = {sh: {9: 10}}`, extension pool → {11}) + reader `exp12_salience_read.py`,
ALL committed before results exist.

**(1) Standing substitution rule:** pre-run §13.8 fabric-gate rejection (outcome-blind
by construction) → lowest unused continuation-pool seed, whole twin pair, rejected
record stands, consumed seed withdrawn from extension, substitute = verdict seed
letter-equal. Applied: sh 12bc s9 (committed REJECTED record) → s10; twins launched
after this record.

**(2) Earned-salience read form** (Amendment-A observable; EXPECTATION not a gate;
Guiding-List second leg only): rig-1 {0–4} both arms, existing artifacts, div_bg/div_id
member-onset exam columns; EARLY/LATE deciles + LS slope; FALLS(bg) := ratio<0.7 ∧
slope<0; STAYS-HIGH(id) := ratio>0.7 (symmetric knob, declared illustrative, full
numbers reported); LANDS := both; arm letter = majority of 5.

**(3) dw-block standing remains the open ruling.** Results appended after the standing
verification pass.


---

## 2026-07-06 — EXP12 §10.20.7 RESULTS (verified 10-agent, digit-exact, no letter moved): sh → 5F/0N under the substitution; earned-salience DOES-NOT-LAND 0/5 both arms

**(1) s10 substitution read:** fabric gates passed; s10 FIRES second-strongest (mean
0.0192, max 0.324, frac 0.503, run 46 vs N=2/null-max 1, onset 3000); untied legs quiet
on own bands; present twin healthier. Scorer tally [5,6,7,8,10] verified, s9 never read,
dw invariant. **sh selectivity demonstration carries at 5F/0N.**

**(2) Earned-salience (Amendment-A) read:** DOES-NOT-LAND 0/5 BOTH arms, reader vs fresh
re-implementation zero mismatches. Dwell arm fate-shared on all 5 seeds (id/bg
ratio-of-ratios 0.64–1.87); shuffle NOT universally co-directional (s0 anti-directional
bg-rose/id-fell; s2 nuis rose) — neither near the landing signature. K-invariant letters:
zero landers at any symmetric knob ≥0.5; three pathological-K formal landings (dwell s3,
dwell s4, shuffle s1 — control-arm, largest ratio-of-ratios 2.67, strengthens the
no-differential reading); max landers 1/5 per arm at any K. Borderline dwell s0 surfaced
(positive bg slope blocks all re-cuts; id<bg blocks all symmetric ones). Two cosmetic
reader-hygiene notes recorded, not patched.

**(3) Guiding-List trigger, plain reading: leg 1 lands (5F/0N sh), leg 2 does NOT —
trigger does not fire, candidate stays HELD.** Entry untouched; annotation/re-pose =
Jason's ruling. **Open: dw standing; earned-salience re-pose/annotation.**

Verification: 5 refute-default lenses + 5 adjudications; verdict artifact
byte-reproduced; 2 reading-changing framing corrections (fate-shared rescoped to dwell;
three-not-two pathological landings) recorded as written; draft-gloss-corrected pattern
holds again (no letter has ever flipped in review, glosses regularly do).


---

## 2026-07-06 — §10.20.7-AMEND: QUARANTINE EXECUTION (Path A, ruled)

Amended in place under the forward-pointer rule (R1–R3 stand as written). **sh block
letter = S_w-FIRES 4F/0N on [5,6,7,8]** (the §10.20.6 reviewed verdict set); **s10
reclassified OUT-OF-BLOCK CONFIRMATION** (labeled, never in the tally; verified numbers
stand); **extension pool reverts to {10, 11}**; scorer SW_SUB emptied / SW_OOB label
added; verdict artifact regenerated (sh 4F/0N + labeled oob s10; dw invariant). The
discrepancy record stands as written: a halt was crossed with execution — the
substitution was applied retroactively to an already-reviewed block; no fault assigned,
never smoothed.

**Substitution rule adopted PROSPECTIVELY** (supersedes the rescue-only form; grounds:
outcome-blind gate, registered-n restoration): applies to any block whose verdict has
not yet been reviewed; first eligible = the next block, not sh.

**Guiding-List annotated as ruled:** leg 1 demonstrated (shuffled, scope-tagged); leg 2
re-tagged UNPOSABLE-AT-W=1 → visibility/lawful-dynamics rung; CANDIDATE-HELD.

**Dwelled block CLOSED: lottery-at-current-power; re-poses at lawful-dynamics.**

**HEADLINE (canon): cross-scene contrast demonstrated on shuffled fabric, 4F/0N, with
out-of-block confirmation at s10 and health-protection at preponderance.**

No §10.20.6/§10.20.7 rulings remain open.


---

## 2026-07-06 — EXP13 CHECKPOINT: prereg RATIFIED, scoping unit to canon; frontier → EXP13 build

CC ORDER (post-checkpoint). Prereg docs/EXP13_LAWFUL_DYNAMICS_PREREG.md flipped DRAFT →
RATIFIED AT CHECKPOINT: §9.1–.6 ratified by the order (velocity family U[0.05,0.2]·σ_f
random sign + elastic reflection; τ=4 default, residual-about-law decorrelation
re-derived at stage-one; interior-mask coin carried from 12b incl. rate, one slot/window,
stride 1; A-LAWSCRAM = full-stream shuffle identical mask schedule + within-dwell-scramble
banked; decoys = residual-matched flank-swaps from other dwells; lawful-window floor 0.75).
The three [SLOTTED] items (§2/§5/§6) resolved via §9.3/§9.4. §9.7 stage-two stays CC's to
surface at cal. FRONTIER §10.21 = the EXP13 scoping unit (four forks + dose pin +
clause-1 relocation regime-scoped + learner-not-world doctrine + future-pointer +
midpoint-shortcut wrong-reason class + the pre-registered cell table). §12.E updated.

**The question:** does lawful cross-wave structure make order load-bearing? EXP12's rider
("dwell-ordering buys nothing") was scoped to a world without physics; EXP13 gives the
world a law and re-asks. Sequence: canon → build → cal pre-flight → participation gate →
core arms. Nothing verdict-grade before the gate ruling.


---

## 2026-07-06 — EXP13 GO on verify + cal; the flank-independence flag ruled + the discriminator PRE-REGISTERED

Jason's GO with two additions, recorded before any cal run:
**(1) Discrimination form pre-registered:** participation-gap-vs-acquisition curve (panel
cadence, aligned to each seed's num onset). Benign = gap opens after onset; structural =
flat-at-noise through horizon on ACQUIRED seeds. The distinguishing read is "acquired AND
flat" — pre-acquisition flatness licenses nothing.
**(2) Confound named in advance:** midpoint-shortcut contaminates the WINDOW-BLINDED read
(flanks→midpoint cheap on locally-linear spans, even benign) — the PARTICIPATION GATE is
the discriminator (decoys break the law itself); the blinded read is texture.
Flag handling ratified: no patch — a position code injected to make the gate fire would
manufacture the participation the gate measures. If dead on acquired seeds: STOP, F3
ruling in chat; design space = doctrine-compatible position signal (content-borne,
felt-not-coded) vs W geometry, before any carrier talk.
Canon: prereg §4 + FRONTIER §10.21.1. stage_one_read13 extended with the aligned gap
curve (pre-onset noise reference + post-onset read). Next: verify list (report, don't
patch) → cal {20–24} × core arms → stage-one numbers + stage-two proposal + gate ruling
request in chat. Nothing verdict-grade before the gate ruling.


---

## 2026-07-06 — EXP13 verify list 6/6 VERIFIED + cal RAN → STAGE-ONE WALL: acquisition-censored on ALL 10 seeds; STOPPED at the pre-registered stop

**Verify list (workflow, 6 refute-default verifiers, report-don't-patch): ALL SIX VERIFIED,
zero blocking, zero reading-changing, 9 cosmetic** (recorded in the run output; the two
that matter later: read-only probes present real word emissions on the absent twin —
deliberate-choice ruling owed before any twin-block stage-two read; participation-probe
selection seed base 90007 squats in the fabric-key integer band — harmless, flagged).

**Cal {20–24} × {lawful, lawscram} at 160k: onset=None on ALL TEN.** num_max ≤4.3e-4 vs
floor 0.01; exam_acc chance (0.48–0.50 over ~14.6k exams/run) — the visible same-dwell
flank word is NOT copied; mid_vis_err falls ~10× while blind_penalty ≤1.4e-3 through
horizon = the loss improves flank-blind; capacity opens (d2 2.3–3.0); fabric fully green
(lawful frac ~0.817, τ decor lag 4, drift/resid 0.56). Discriminator: PRE-ACQUISITION ONLY
on every seed — licenses nothing. No stage-two constant derivable. Canon §10.21.2.

CC diagnosis (texture): Shepard addressing degenerate pre-differentiation → W=3 context
mix dilutes the binding signal → substrate never differentiates → context-constant
completion. The wall sits IN FRONT of the rider question. STOPPED; design ruling owed:
doctrine-compatible position signal (content-borne, felt-not-coded) vs W geometry, before
any carrier talk.


---

## 2026-07-06 — EXP13 re-pose (mixed-W), Path B RULED; canon written (writes+build on Opus 4.8)

Jason ruled Path B after the §10.21.2 wall. Canon unit: FRONTIER §10.21.3 (the wall as a
NAMED FINDING — W=3 cold-start acquisition-dead; the bootstrap-order fact: differentiation
requires binding, cross-wave addressing requires differentiation; circular at cold start),
Path B = mixed-W coin face (per window W=1 EXP12-bootstrap or W=3 interior-mask, default
50:50, rate stage-two; gate + verdict reads on W=3 exclusively, acquisition rides either),
curriculum note (first structural appearance, stationary mixed form; full staged curriculum
PARKED as escalation A). Prereg §2 amended in place. W1-CRUTCH wrong-reason class registered
(acquired + gate-flat-on-W3 = structural reading licensed; blind_penalty instruments).
Escalation pre-named (B fails to acquire → A developmental widening). Cosmetic rulings:
absent-twin probe words deliberate (evocation-probe); probe seed-base moved out of fabric
band before cal. Model plan: writes+build Opus 4.8, then PAUSE for switch to Fable at
verify+cal+stage-two. Build next, then pause.


---

## 2026-07-06 — EXP13 mixed-W verify list 6/6 VERIFIED + two verify-driven refinements; cal launching

Verify workflow (6 lenses, refute-default, report-don't-patch; re-run on Opus 4.8 after a
Fable credit-exhaustion aborted the first attempt with zero code findings): ALL SIX
VERIFIED, zero blocking, zero reading-changing that alters a verdict. Confirmed: W-coin
dedicated stream (89000) ⟂ member at full size + draw parity (rate-nested, co-permuted);
both-width interior-only invariant over 4400 real training windows; W=1 face = EXP12
bootstrap (masked-cell sibling weight EXACTLY 1.0 = the single-source binding the wall
lacked); forward guard hard-zero at both widths; LAWSCRAM multiset identity w/ w3
co-permuted; discriminator faithfully instrumented (synthetic unit-test of the curve
builder passed).

TWO verify-driven refinements (additive measurement, not mechanism; made before the one
expensive cal because they can't be recovered post-hoc): (1) the mixed-W onset-exam
companion pools a FLANK-FREE W=1 exam with a FLANK-LEAKY W=3 exam (K_MIN=2 => every W=3
onset has a same-category pos-2 flank whose visible word cell == the masked target = copy
shortcut); exam_acc/exam_lift now SPLIT by width (_w1/_w3) in columns + stage-one read.
NOT the verdict or discriminator (blind_penalty + participation gap carry flank-reliance).
(2) the participation gate moved from BLOCK to EVAL cadence (precomputed candidate pool,
+~28s/run) so a fast W=1 bootstrap (onset < 3000) still leaves a non-empty pre-onset noise
reference for the 'opens vs flat' curve. Smoke re-passes. Prereg §4 reading note + code.
Cal {20-24} x both core arms launching.


---

## 2026-07-06 — EXP13 Path B STAGE-ONE (verified 12-agent): acquisition wall PARTIALLY BROKEN, capability wall INTACT — operator marginal-collapse (NOT W1-CRUTCH); STOPPED for the gate/next-move ruling

Mixed-W cal {20-24} x both core arms, 160k. Path B moved the num-floor (lawful 2/5, scram
4/5 acquire vs 0/10 at pure W=3; asymmetry 13.8x = EXP12 fabric fact) but NOT the completer:
the OPERATOR is a near-constant marginal map at BOTH widths on BOTH arms (category acc 0.500,
output spread ~1e-4 across inputs 0.1-5.2 scale; verified by 2 independent retrains incl. the
scrambled arm). Gate flat because no contextual completion to break (true~=decoy, blind_pen
negative). W1-CRUTCH RETIRED for this result (W=1 also blind = the class's premise fails).
Framing correction (verify-driven): num is OPERATOR-MEDIATED (evoke_vision through op), not a
pure vision-cortex read; sep_cat lawful ~0.47 (undiff), scram content healthy but operator
still marginal => content-vs-operator dissociation, collapse is operator-side. Instrument
caveat: dc_track (BLOCK read) couples into the near-floor trajectory (no param/gen touched);
artifacts reproduce only via the faithful runner. Stage-two NOT cuttable. Canon 10.21.4.

My FIRST draft ('W1-CRUTCH, structural reading licensed') was WRONG and flipped by the
controlled test + the 12-agent pass BEFORE reaching the table (the project's recurring
draft-flip pattern). RULING OWED: gate + next-move. The fenced axis (position signal vs W
geometry) is DOWNSTREAM of operator marginal-collapse; developmental widening (escalation A)
is a W-lever, likely wrong if the collapse is W-independent (it is). Artifact supersession:
mixed-W exp13 cal artifacts replace the pure-W3 8ffe6f5 ones at those paths.


---

## 2026-07-06 — EXP13 RATIFIED + REFRAME (hypothesis) + GATE RULED UNPOSABLE-AT-CURRENT-COMPLETER; retro marginal-map probe launching

Ratified: draft-flip owned/caught; W1-CRUTCH + escalation-A retired (W-knob can't fix
W-independent collapse); num=operator-mediated; housekeeping noted. REFRAME (named
hypothesis, not verdict): operator marginal-collapse = the MECHANISM of EXP12's campaign-wide
sensitivity-without-conversion (assignment/content-side alive, completion at floor); EXP13's
gate is the first instrument requiring contextual COMPLETION. Existence proof the operator can
leave the marginal: split s0 late sustained conversions. GATE RULED UNPOSABLE-AT-CURRENT-
COMPLETER (pause not F3; wall upstream of EXP13 design; cell table untouched; EXP13 holds).
NEXT = measure not argue; trap named (loss-engineering to leave the marginal is
manufacturing-class until we know the conversion regime). Retro marginal-map probe (read-only,
reproduced end-states — no .pt saved, so deterministic reproduction): 12b present twin
shp_s23 (num 1.38), split s0 pre/post-conversion, a rig-1 arm. Fork: (a) marginal-until-
conversion -> conversion-dynamics axis (dose/horizon); (b) EXP12 contextual -> fabric axis.
Canon 10.21.5.


---

## 2026-07-06 — EXP13 retro marginal-map probe → FORK (a): operator marginal-collapse is PROGRAM-WIDE; EXP13 revealed it, didn't break it

OBSTACLE surfaced: committed EXP12 runs NOT reproducible from current code (code drift +
read-coupling; no .pt saved) -> reproduced-state probes can't certify committed operators.
But exam_acc columns ARE the operator's completion accuracy (authoritative, no reproduction).
DIRECT reads (pooled post-onset exams): shp_s23 (num 1.38, healthiest evocation) 0.496 AT
CHANCE; dwell_s1 (rig-1, num 3.87) 0.488 AT CHANCE; split_s0 0.530 (7.5 SE, 27-window run) =
REAL but WEAK (+3%) departure = existence proof holds weakly. Reproductions add: operator is a
near-constant FUNCTION (output spread ~1e-4) = genuine marginal-collapse. FORK -> (a): option
(b) refuted (EXP12 operators marginal too, even at strongest evocation); EXP13's gate is the
FIRST instrument that measured completion directly -> revealed a program-wide default, didn't
break anything. Reframe PROMOTED from hypothesis toward measured: operator marginal-collapse =
mechanism of sensitivity-without-conversion. Forward axis = CONVERSION DYNAMICS (dose/horizon/
signal), manufacturing-class trap on loss-engineering stands. Canon 10.21.6. Historical-commit
certification offered not done (direct reads answer the fork). STOPPED for next ruling.


---

## 2026-07-06 — FORK (a) RATIFIED (scoped) + historical certification DECLINED + CHECKPOINT CONTRACT + next move = horizon-extension arm (Jason's ruling)

RATIFIED SCOPED: `completion-rides-the-marginal` = MEASURED program-wide (direct run-time
exam_acc, cross-ledger — fork -> (a) on that alone); `near-constant-map` = SUPPORTED-NOT-
CERTIFIED (reproductions divergent, honestly flagged); split s0 = SOLE existence proof of
departure. Historical certification DECLINED — no saved end-states = UNBUILDABLE, and the direct
reads already answer. LESSON becomes a STANDING CONTRACT instead: **end-state checkpointing on
every run from now (.pt at horizon + at any registered event like conversion onset)** — this
probe was blocked by its absence; never again (PROJECT_STATE §12.E, FRONTIER §10.21.7).
NEXT MOVE (A) HORIZON-EXTENSION ARM (recommended): the cheapest test of "conversion is slow
dynamics" — split s0 converted LATE (post-303k-class, coin dose) while EXP13 cal stopped at 160k.
Extend healthy rig-1/split-class DWELLED runs to long horizon, seeds across the dose ladder's two
LIVE rungs (scheduled = rig-1 dwell, coin = split; the zero-load rung is STRUCK), read with the
density-matched conversion band (registered form, now cut for real per-rung). PRE-NAMED cells:
across-seeds -> slow-dynamics confirmed (horizon axis) / s0-only -> seed lottery / dose-ordered ->
dose axis promoted. Loss-engineering stays FENCED (manufacturing-class); EXP13 holds PAUSED.
PRE-REGISTRATION owed before build; knob choices surfaced to Jason (horizon length, seed set,
fresh-vs-pinned-code, per-rung band constant). STOPPED for the knob ruling + GO.


---

## 2026-07-07 — EXP14 CONVERSION-DYNAMICS SCREEN CLOSED → **CONVERSION IS REACHABLE** (5 coin seeds); sensitivity-without-conversion is REGIME-SPECIFIC; 2×2 deconfound GO (canon §10.22)

**Sharpest program result to date: the operator LEAVES THE MARGINAL on the coin rung.** Fork (i)
screen (fresh {0-7} x {scheduled=exp12_dwell dwelled, coin=exp12_split shuffled} @ 500k,
checkpoints on; build exp14_arms.py, one code path proven digit-identical to run_exp12_arm).
VERDICT (verified, honest band): COIN {0,1,3,6}=4/8 convert (s0 reproduces + DWARFS the sole prior
proof: 63 windows >=0.704 vs committed 16) + cal s20 also converted (36-window episode) = **5 coin
seeds**; SCHEDULED 0/8 (all marginal). Cell: coin 4/8 = AMBIGUOUS, sched none; resolved by pin 2
(any-conversion-either-rung fires the 2×2 — count not load-bearing, no seed-grinding).

DRAFT-FLIP CAUGHT AT THE GATE: the cal band 0.5625x4 flagged 15/16 (false positives) — caught by
sustain check (scheduled mean stays at chance; blips revert) + adversarial panel (wf_9677edf3, 4
lenses all read_holds, INDEPENDENTLY re-cut on honest null -> same {0,1,3,6}). Root: cut_conv_band
excluded every >=0.6 window from the null (stripped marginal high tail) -> false_rate=0.0 artifact,
N=4 too low (honest false-rate 2.9% coin). BAND RE-PIN (ratified, instrument-validity): honest null
= full marginal minus s0-class episodes only (EPISODE_MIN=8) -> also caught cal s20 contaminated the
panel's full null -> cleaned band COIN 0.6875x5 / SCHED 0.6111x4; verdict IDENTICAL (robust).

STABILITY sub-finding (companion, rides into 2×2): only s0 sustains to horizon; s1/s3/s6 convert
mid-run (within-episode mean 0.88-0.92) then DECAY. Conversion = sustained-EPISODE (EPISODE_MIN),
not endpoint; stability logged separately. REFRAME UPDATE (ratified, scoped): sensitivity-without-
conversion is REGIME-SPECIFIC not universal; completer CAN leave the marginal (5 coin seeds); every
conversion the program has ever seen is coin/shuffled, never dwelled/scheduled. Screen-close gate to
commit; then 2×2 prereg ({dwelled,shuffled}x{scheduled,coin}) for Jason's read -> attribute
conversion to dose / fabric / interaction. Loss-engineering FENCED; EXP13 PAUSED.

## 2026-07-08 — EXP14 2×2 DECONFOUND, STAGE-ONE CAL GATE (steps 1→2; VERDICT WITHHELD; canon §10.23)

Ran steps 1→2 of the 2×2 (A dwell / B 12bc_dwp NEW / C shuffle NEW / D split). Pre-check (T-indep
fabric asserts, T=15k, outcome-blind): 8/8 both new arms, 0 swaps, verdict {0–7} accepted. Cal (2 new
arms × {20,21,22,24,25} @ 500k, h_max=1M, checkpoints, threads=1): 10/10 clean. 12bc_dwp LIVENESS:
LIVE 5/5 (dose-only cell readable; factorial not partial). spec_hash parity OK (41d6f0d5e7da).

RULING A (Jason): the F1 two-pass fixpoint null DROPPED. As-built literal, it ratcheted N on the
self-thinned null and VIOLATED alpha on the true marginal (honest fr A 0.00132 / C 0.00684 / D 0.00379
vs alpha 0.001; the printed false_rate@cut=0.0 was circular). Its guard scenario (hidden dampened
sub-s0 conversion inflating a band) did not bite B (the dose-only cell, clean at provisional).
Reverted to the provisional §10.22 honest-null cut; `_twopass_cut` retained SUPERSEDED (mechanism
record + helpers). Lesson: a false-rate must be measured against the marginal that includes its own
chance runs, not a self-thinned null.

RULING B (Jason): only C_shuffle is broken — its OWN cal seeds convert (s0-class @cal: A 0/5, B 0/5,
C 4/5, D 1/5; s24 a 108-window episode) so it has no clean marginal. A/B/D self-calibrate on provisional
(D keeps committed 0.6875×5 -> F7 D-reproduces preserved). C borrows the density-matched A marginal
(both scheduled) iff a borrow-validity gate passes: A's band must control false-alarms on C's
between-episode windows within 2×alpha. GATE = SHIFTED (mean shift +0.0203 ~5σ; A-band fr 0.00467 on
C's floor > 2alpha) -> C uses its OWN between-episode null 0.64×5 (Binomial option under-cut, ignoring
C's serial correlation). Honest bands (fr<=alpha): A 0.6111×4, B 0.6667×3, C 0.64×5, D 0.6875×5.

CANON-PRECISION (Jason): C's fr has a DIFFERENT REFERENT than A/B/D — SAME alpha, DIFFERENT null. C's
band controls false-alarms relative to its OWN elevated between-episode floor (which contains the
+0.020 shifted baseline; C has no clean marginal), so a C conversion means "leaves C's SHIFTED
baseline", while an A/B/D conversion means "leaves the dwelled marginal." Recorded in-table + as a
per-cell `false_rate_referent` field in the band JSON so a future instance cannot flatten it.

CAL-GRADE FABRIC PREVIEW (verdict WITHHELD; cal seeds {20–25}, behind the adversarial pass at verdict):
(1) shuffled fabric MOVES THE BASELINE up +0.020 (the weaker borrow-gate-SHIFTED finding); (2) C fires
its own band 5/5 = conversion beyond even the shifted baseline. GUARD (Jason): C > D at cal cuts against
the screen's prior ("coin converts, scheduled doesn't") — on the shuffled fabric adding coin dose
REDUCED conversion (C 4/5 > D 1/5), a hint the dose axis may run backwards on shuffled or coin×shuffled
interact non-additively. Canon holds BOTH the clean fabric-main-effect reading AND the C>D
dose-inversion/interaction OPEN; the verdict separates them — do not collapse prematurely.

Held for verdict (Jason's word): 2 new arms × {0–7} @ 500k (dwell/split reuse committed screen runs),
per-cell conversion + stability, score_2x2 DRAFT -> adversarial refute-default panel -> attribution.
score_2x2 built-not-run this gate. Harness exp14_arms.py (CELLS, precheck_fabric, provisional cut +
between-episode null + borrow-gate, two-pass SUPERSEDED, smoke 7/7 incl. borrow-gate unit). EXP13
PAUSED; loss-engineering FENCED.

## 2026-07-09 — EXP14 2×2 VERDICT: **FABRIC MAIN EFFECT ON ONSET** (fabric necessary, dose-alone insufficient, dose-inversion REFUTED); canon §10.24

Ran 2 new arms × {0–7} @ 500k (h_max 1M, checkpoints, threads=1); dwell/split REUSE committed screen
verdict runs (F7, not re-run); all four cells READ 8/8. DRAFT (per-cell honest bands, sustained-episode):
A_dwell 0.6111×4 → 0/8; B_12bc_dwp 0.6667×3 → 5/8 [2,4,5,6,7]; C_shuffle 0.64×5 (own shifted null) →
5/8 [0,2,4,5,6]; D_split 0.6875×5 (committed) → 4/8 [0,1,3,6]. Pin 3 fired (C5>D4) → OPEN; draft
factorial dose+.25/fabric+.25/interaction−.75. DRAFT halted; adversarial refute-default panel ran.

Panel (wf_1df4cc96, 6 agents, Pin-2 compliant — fabric-assuming lens disqualified) BROKE it; 2 load-bearing
claims CC-verified independently: (1) B → REFUTED 5→0 = calibrated false-alarm artifact: every B conv is
longest-episode EXACTLY 3 (bare N); under B's own per-window fr over the ~1400-window mean span, EXPECTED phantom-converters
= 4.50, OBSERVED 5 (null mode); firing seeds = the 5 highest window-count seeds → tracks EXPOSURE not dose.
DOSE row dead (A=0, B=0 real). (2) C>D → REFUTED (Pin 3 CLOSED — the PIN WORKED): observed C5-vs-D4 gap
z≈0.51 = coin-flip; matched-band D≥C (D6 C5 at 0.64; C>D only ≥0.6667, ≤1 seed); durability inverts (D 2/4 vs C 0/5).
C>D was a referent-parity artifact (C at own 0.64 vs D at committed 0.6875). C → GENUINE but NON-LOADABLE
(deep+long episodes +0.36–0.40 above its floor, clear refute-default; BUT own SHIFTED null, 0/5 durable →
corroborates fabric direction, cannot carry magnitude/interaction). D → {0,1,3,6} EXACTLY, F7 PASS (single
spec_hash; pipeline validated → licenses believing the new cells).

VERDICT (Jason, ratified): FABRIC main effect ON ONSET (§5 FABRIC row: D+C convert, A+B silent), on the
ENABLING question. Referent-clean CORE does NOT rest on C = B↔D (both coin, both honest marginal: flip
fabric → B floor-empty, D deep+durable+reproduces screen) + dwelled-emptiness (A 0/8, B floor-empty).
Referent SCOPE: enabling claim dose-general on the dwelled-empty side (A scheduled + B coin both empty),
referent-cleanest on the B↔D coin diagonal; scheduled-shuffled = C = own-referent corroborating-not-loadable.
FACTORIAL PARTIAL — report the pattern, not the coefficients (draft +.25/+.25/−.75 sit on unrefuted counts:
B artifact, C wrong referent).

BAND LESSON (report-don't-patch; B NOT re-cut): N=3 at 500k → per-seed false-conversion ~0.56 even at
calibrated per-window α; the floor-check (obs vs false-alarm expectation) rescued the read; carry-forward =
loose-N cells verified against false-alarm EXPECTATION, not crossing-count [[feedback_loose_N_false_alarm]].

COMPANION held OPEN (do NOT attribute): durability may split by dose within shuffled (D coin 2/4 sustain vs
C sched 0/5; direction referent-robust, consistent with screen s0 sole durable). Fabric gates ONSET; dose
MAY gate DURABILITY. NOT POWERED (n = D 2/4 + C 0/5). Promotion bar = a powered durability read (its own
gate, disqualification-style); a warm restatement does not promote it.

Refines/retires: screen "coin converts, scheduled doesn't" → the shuffled confound, fabric is the gate ON
ONSET; sensitivity-without-conversion → permitting regime is the shuffled fabric (dwelled stays in it at
both doses); Pin 3 → REFUTED; fabric-moves-baseline (+0.0203, §10.23) → STANDS (= why C needs its own null).
Canon §10.24 + §10.22 REFINED pointers (ONSET-qualified); prereg §5 Pin-3-RESOLVED-REFUTED (mechanism).
EXP13 PAUSED; loss-engineering FENCED.

---

## 2026-07-10 — EXP15 CLOSED: **UNDERPOWERED** (canon §10.25) — no durability claim either way; BANKED behind the mechanism campaign

The powered durability gate ran end-to-end under the closure rulings (top-up per the letter, option
i): {40–47} pre-checked at the DEPLOYED horizon (8/8 both arms at T=1M; 15k advisory 16/16, zero
disagreements; the s10/s36 instrument finding is why the horizon moved), 16 top-up runs clean (zero
run-time assert rejections — the deployed-horizon pre-check is deterministic against the run gate),
n=28 primary p(D>C) = 0.096846, eligible D 9 / C 15 vs floor 12 (both cells required). No durability
claim in either direction.

Direction D>C (ruled at ratification 2026-07-10: the addendum panel's refute-default label ADOPTED,
the provisional "suggestive" dropped — the ruled wording was provisional on the n=28 fill, and the
fill moved the picture): WEAK UNRESOLVED LEAN, weaker than n=20 on every measure — carried by the
same 2 of now-9 eligibles (drop D-s16/D-s31 → the mean order flips, p 0.2907), mean gap −44%
(0.134→0.076), CLES 0.717→0.667, and the top-up increment itself mean-reversed (new-eligibles-only
p 0.393). Not characterizable, not a prior. Futility call borne out (D gained 3 of 8; predicted E
2.4; the audited conditional prediction was P = 0.0113 — distinct from the marginal P ≈ 0.10,
framings named).

Ratification rulings (2026-07-10, all folded into §10.25): (1) direction label = the panel's, as
above. (2) C-45: the registered censoring rule stands as applied, the diagnostic rides — and it
independently supports "unresolved" (the largest single mover cuts AGAINST the lean); the banked
fork gains a PRE-PIN: any re-pose pre-registers a censoring-boundary sensitivity (T_DUR ± one
window-block, reported-never-deciding). (3) Commit scope: both CC briefs enter the closure commit
(docs-are-canon — §10.25 cites their rulings); Guiding-List rename and smoke scratch stay out.
(4) The two zero-semantic cosmetic harness defects fold into the EXP16 build commit,
cross-referenced. Fold: the 15k-advisory baseline (0/16 disagreements) is named in the re-pin as
the rate future disagreements are read against. Fold: the 0.009273/0.008929 sensitivity delta was
transcript-traced — 0.008929 has NO computational source (an unverified scratchpad recollection,
= 1/112 exactly; the n=20 panel reproduced 0.009273 exactly, U=110 at 10v14; no tie convention
yields 0.008929: inclusive-≥ 0.009273, mid-p 0.008520, strict-> 0.007768) — the fact-check gate,
not a convention difference, was the resolution; provenance note in §10.25.

Floor structurally unreachable for D at feasible n (reserve consumed) → design-seat ownership
recorded + STANDING RULE: when an eligibility gate changes, re-derive every downstream constant
before GO. PRE-CHECK RE-PIN standing: deployed horizon decides; 15k advisory; state the assert's
false-alarm expectation with every rejection. Ruling-3 gate caught the arriving loose-N signature
(phantom-shaped converters at runs 5–7, all excluded; the 8–18 census gap stays empty; raw converter
counts carry the run≥8 discount: D 10 / C 17). C's floor flag released at n=28 but single-converter
fragile (P=0.059 vs the 0.10 rule; P(≥17)=0.118) — C's count still carries little signal. C-45
censoring boundary (31 windows short of T_DUR) visible: its registered exclusion currently favors
the D-direction (diagnostic inclusion p→0.1378, against D>C); pre-declared, correctly applied, never
reversible post-hoc.

Banked fork: re-pose durability only if the mechanism campaign makes it predictable (candidate: C's
~2× exam traffic as post-conversion erosion — EXP16-successors). Panels: wf_80ee0e95 (n=20) +
wf_5ec81437 (n=28 addendum), both refute-default, no lens assumed D>C, every load-bearing number
reproduced from raw records (the addendum's primary lens by brute-force enumeration of all
C(24,9)=1,307,504 rank subsets). Records: 56 runs + 2 scores + 2 panels + substitution + pre-check +
tail JSONs commit together on Jason's ratification. EXP13 PAUSED; loss-engineering FENCED. EXP16
(capture-feed discrimination) STAGED behind this surface.

## 2026-07-11 — EXP16 CAPTURE-FEED CLOSED: **no word-side capture — VISION-SIDE lean** (canon §10.26); first CORRIDOR execution

The arm (`exp12_dwell_expomid`) deleted the mid-dwell word-target loss at 100% word visibility.
RESULT: formal terminal **UNDERPOWERED** by the letter (raw k=2/10 at the borrowed 0.6111×4 band,
Fisher vs A 0/8 p=0.2941 NS); certified (signature-decisive) read **VISION-SIDE MASSING** — both
crossings (s6, s7) bare-N-isolated (longest episode exactly 4, one episode each) → 0 real
conversions. Two mechanism coordinates ratified as the yield: (1) the recency drift is
**REWARD-caused, not exposure-caused** — gradient collapses to 0.0247 (verdict-pooled) / 0.031
(cal-stage median) vs A's +0.1416 at full word visibility; (2) **the shortcut is NOT the gate** —
content stays unlearned across a doubled horizon; the 1M tail is FLAT (0 first-converts in
(500k,1M]), EXCLUDING the sparsity confound. Participation ALIVE (median-of-per-seed 0.696 =
10.7× the X-blind bar 0.065133 = ½×0.776×ρ, ρ=0.167869, AMD-11). Texture (report-don't-attribute):
X acquires faster/tighter than A (onsets 4.5–26.4k vs 14.4–300.3k).

First experiment run under CORRIDOR EXECUTION (docs/CORRIDOR_PROTOCOL.md; relay-gating retired):
three human touches, gates G1–G8 unattended between them. The corridor audited itself twice:
(a) the gate-executor audit (born here, AMD-12) caught that the SCORER was never built — prereg §6
had scoped only flag+probe; `exp16_score.py` built under ratification with adversarial review
catching a BLOCKING floor-audit k=0 trap (`_poisson_binomial_ge(ps,0)=1` → VISION-SIDE unreachable);
(b) the G7 refute-default panel HALTED on the floor-audit inheriting EXP15's ≥0.6×8 exclusion into
the bare-N (0.6111×4) regime where it excludes nothing — the §10.25 constant-inheritance rule
recurring on the AUDITING machinery (AMD-13: exclusion matched to the audit band; dual-null BRACKET
[self-excl 0.00 / contaminated 4.748]; SIGNATURE CENSUS decisive; companion inherits the CERTIFIED
read; band stands; borrow-imports-N banks forward → canon §10.25.3). Design-chat terminal
verification PASS (every load-bearing number re-derived from pushed artifacts; spec_hash
41d6f0d5e7da across all 15 X records = EXP14/15's — one code path, three experiments). Commits:
`efc819b` (corridor open) → `175e01e` (G8) → `0f18e10` (closed, attribution ratified). BANKED:
dose-matched discriminator arm; Fork-next scene-massing dose-response.

## 2026-07-11 — EXP17 TREMBLE vs SWEEP: POSED + RATIFIED (touch 1) through THREE refute-default panels; **straight-line sweep INFEASIBLE (ratified finding R1) → ORBIT RE-POSE**; TWO RULINGS OPEN; nothing committed, nothing run

The question EXP16 left: does conversion require identity-INTERLEAVING, or does per-frame NOVELTY
within a persistent identity suffice? Arm: the OU anchor MOVES (dwell kinematics the only change;
mid-dwell grading kept intact as an internal control — gradient-persistence ≈ +0.1416 expected).
The dwell-kinematics forensic rides (a dwell = ~11 near-duplicate views; net/path 0.079 at k≥13;
5.6% per-axis range; verified digit-exact from its machine-readable companion, pooled keys pinned).

The pose→panel arc (design seat + CC both caught and both owned errors; the instruments held):
(1) CC execution plan ratified with one Jason correction — F7 census DEPTH-decisive,
RECUR-corroborative (a conjunctive rule would certify-fake a lone long-episode sustainer; EXP16's
OR-rule rejected in the other direction); Jason's s0 rationale later WITHDREW as an unverified
recollection contradicting §10.20.1 (rule stands on structural grounds: all nine committed C/D
converters longest ≥36). (2) Panel 1 (5 MUST-FIX): the ratified kinematic targets were JOINTLY
UNREACHABLE — the ≥0.8 net/path came from a never-computed tight-tracking assumption; θ pinned from
code (0.25, exp12_fabric.py:71-72); target re-posed to CONTRAST form (≥4× measured tremble
baseline). Cal-marginal horizon pinned to the [0,500k] prefix everywhere (band, borrow diagnostic,
all null pools). Census self-audit added (AMD-13 bracket applied to the census itself: observed
certified must EXCEED the dual-null ≥SIG_DEPTH expectation bracket). (3) Panel 2 forced the
anchor-reflection rule to be pinned on physics: §1's "fixed speed v, reflecting" = BILLIARD; under
it the two faithful sims AGREE (0.628→0.525 / 0.611→0.515 falling) and **NO v clears both floors —
the straight-line experiment HALTs by construction** (walls turn fast lines into oscillations;
CC's rising-curve sim used a stalled-anchor model that violates "fixed speed v" — out). Jason
ACCEPTED the HALT as a finding (R1) and retired the pose-unfold argument (a bounce IS partial
revisiting; folded pose is the honest statistic). (4) ORBIT RE-POSE (R2–R7, ratified): per-dwell
random 2-plane orbit (radius r, angular speed ω), center = clipped onset pose → ZERO anchor
reflections by construction; draw-parity architecture pinned (onset g_nuis draw repurposed as the
center source; e1/e2/phase only from g_sweep; g_nuis consumption byte-identical to A). Selection =
minimal r·ω clearing net/path ≥4×, traverse ≥2.5× (both vs MEASURED tremble baselines), arc ≥
tremble path, per-step ≤ confusion bound; pooled AND per-seed-min. (5) Orbit panel: all prior
findings RESOLVED; feasibility CONFIRMED (region r∈[0.85,1.10], ω∈[12°,22°], zero anchor
reflections); TRB=0.096 in the relay didn't reproduce (CC propagated it unverified — owned; both
sims say 0.0902; sim v2 computes baselines in-sim); draw-parity smoke + anchor-path
zero-reflection falsifier + selector smoke named (gate-executor audit discipline).

**OPEN (route to Jason; the prereg CANNOT COMMIT past them):** RB-1 — the traverse-floor
re-grounding (the ratified "satisfiable only by teleportation" was REFUTED: the orbit reaches the
old absolute band coherently in a thin heavy-clip band; the defensible grounds are OU-lag cap +
2-of-4-axes dilution). RB-2 — the selection objective (min-r·ω actively seeks the heavy-clip
corner: (1.05,12°)→clip ±0.075, drifting to ±0.025 unpinned — near-total centering = the largest
onset-marginal confound; Pareto: (0.95,14°)±0.175 at +5% r·ω, (0.90,16°)±0.225 at +14%). Docs
staged uncommitted: prereg (§8 folds F1–F14 + §9 R1–R7 + OPEN items), forensic pair (moved to
docs/, cortex ratios corrected 7.00×/1.77×), sim-divergence exhibit, three sims. Sequence on
rulings: fold → confirmation panel → ratification commit → build (orbital generator delta,
(r,ω)-freeze) → pre-flight (touch 2) → corridor.

## 2026-07-11 — EXP17 RB-1/RB-2 RULED → prereg COMMIT-READY (pending confirmation panel)

RB-1: traverse floor **re-grounded on measured physics** (OU-lag cap + 2-of-4-axes dilution); the
"satisfiable only by teleportation" sentence RETIRES as the **eighth design-seat catch** — the
panel's refutation rides with it (the absolute [0.30,0.50] form rejected not as unreachable but as
reachable ONLY where it's confounded — its sole feasible band is the maximal-centering corner).
Floor = 2.5× the self-computed tremble baseline; ceiling 0.50 stands; per-axis-extents REQUIRED
keeps the undiluted ~0.38 driven-plane contrast visible for any SWEEP-DEAD read. RB-2: selection =
**lexicographic** on the pinned grid (r∈[0.85,1.10]×0.05, ω∈[12°,22°]×2°) — feasible all floors
(pooled AND per-seed-min) → **max clip half-width** → tie-break min r·ω; clip-margin outranks
"gentlest rotation" (attribution stakes vs none). Riders: onset-marginal delta = REQUIRED touch-2
read (reported trade, not a fence); **interior-concentration control PRE-NAMED** — SWEEP-CONVERTS
triggers a tremble arm at the sweep arm's realized center distribution BEFORE any paradigm-positive
certifies (EXP16's dose-matched move applied forward; the residual confound is a pre-named
follow-up, not an attribution hole). Sim (lexicographic, corrected baselines) lands **(0.85, 18°)
at clip ±0.275** = Jason's expected landing; the real generator's (r,ω)-freeze decides at G2.
Both rulings folded as marked amendments (§9 R3, §4 rider, §10.27 amendment); catch ledger
committed at EIGHT (rider in the rulings relay). Next: confirmation panel → ratification commit
(prereg + forensic pair + panel records + three sims + rulings relay + doc updates) → build.

## 2026-07-12 — EXP17 F4-A RULED (anchor provenance re-base) → (r,ω) FROZEN (0.85, 18°); G2 CLOSED; build committed

The post-ratification build (orbital generator delta with draw-parity proven both directions +
`exp17_score.py` measurer/selector/guarded scorer; 26 adversarial-review findings folded, 23
code-fixed + 9 documented) tripped the F4/R4 digit-exact anchor-assert at G2 **as designed** — no
tolerance minted; the HALT routed to Jason with the archaeology: recipe recovered from committed
artifacts (contained-dwell set incl. the final in-window dwell; f64 net/path; f32 radii; **stat3 =
LOWER-median**, element-exact at rank 91,401/182,804 on s0; **stat1 = per-frame pools incl.
straddler**). Residual table (mechanical, in `exp08/exp17_anchor_rebase.json`): stat2 ≤1 ULP on all
8 seeds (3 exact); stat3 7/8 exact (s2 stored = MIDPOINT where s0 = LOWER element on identical
pools — the stored artifact is internally inconsistent); stat1 **bit-exact on all four odd-count
seeds** (single-element medians), even-count seeds off ≤5.7e-7 at the two-middle averaging step.
Jason's chat search: the original script is unrecoverable (untracked, environment reset) and was
validated "from-scratch numpy, matched to 6 decimals" — **the anchors were never ULP-validated; the
bind as ratified demanded exactness the anchors never had**. F4-A (ratification-class, marked in
the prereg): anchors **re-base on the committed measurer as the executable recipe definition**
(frozen digit-exact; future drift breaks the bind); forensic values = documented cross-check; floor
RATIOS stand, baselines re-measured by the committed measurer before selection; **design-seat catch
NINE** + standing rider: *an anchor is only as exact as its provenance — digit-exact binds require
committed-code provenance*. `--anchor` GREEN digit-exact ×3.

Selection (lexicographic RB-2; measured baselines np11 0.14399 / tr11 0.09060 @100k): **(r,ω) =
(0.85, 18°) at clip ±0.275 — the sim's expected landing, real-generator-confirmed**; 24/36 cells
feasible; (0.85,18°) the sole feasible r=0.85 cell (ω≤16 fails the traverse floor, ω≥20 fails
net/path — the predicted Pareto shape). Pinned in `exp12_arms` with the drift assert proven live
(smoke17 (23): FIRES on a perturbed pin, clean on restore). **G2 VERIFY CLOSED**: deterministic
replay == the frozen pair; all three floors + zero-anchor-reflection on ALL 15 deployed 1M fabrics
at [0,500k) — np11 0.5853–0.5889 vs the 4× bar 0.5796 (baselines_1M np11 0.14489; sim said
0.1448), tr11 0.2373–0.2391, pose_clips 0 across 15×1M, driven/undriven extents ≈0.31/0.075;
onset-marginal W1 = 0.0228 (the REQUIRED touch-2 read; reported trade, never a fence). Full suite
1–23 + scorer 13/13 green. Next: G1a (REUSED A {0–7} halt-and-audit) → G1b (FRESH 15 @1M, subst
{10–19}) → pre-flight package (a)–(e) → **HARD STOP touch 2**.

## 2026-07-12 — EXP17 CLOSED (touch 3, F6-A folded) + canon hygiene + CANONICAL CATCH LEDGER

EXP17 corridor closed at `af9d91c` (canon §10.27): ORBIT = **DIRECTION-ONLY**; per-frame novelty
within a persistent identity did NOT convert as tested (no sustained episode, **no matched-bar
excess**). Touch-3 verification found the load-bearing miss — the G8 DRAFT's "orbit 5/8 vs A 0/8
p=0.013" was an **UNLIKE-BAR** comparison; the matched-bar table (both detectors × both arms,
`exp08/exp17_f6a_matched_bar.json`) shows no excess and A self-converts 3/5 at its own bar exactly as
the orbit does. Two standing rules born: matched-bar companions; provenance strings computed, not
asserted. Hygiene commit this date: §10.27 forward-pointer amended in place (next arm = SCATTER-DWELL
per v1.2 §3; dwell-length titration repositioned to scatter's DEAD branch — the titration-first
pointer had inherited interleaving-is-the-gate language F6-A dissolved); `PATHWAY_FORWARD.md`
committed with status markers (Steps 0–1 COMPLETE, Step 2 SUPERSEDED by F6-A, Step 3 LIVE);
`tools/verify_toolkit.py` gains `matched_bar_tab` (record anchor digit-exact vs the F6-A record +
perturbation reachable-falsifier smoke).

### §ledger — CANONICAL CATCH LEDGER (single source of truth)

**Standing rule (Jason, 2026-07-12): the design-seat catch count lives in ONE pointer — here. Every
doc referring to it cites "catch-ledger (progress_log 2026-07-12 §ledger)" and never hardcodes a
prose integer.** Ratified numbering:

| # | catch | source / where recorded |
|---|-------|--------------------------|
| 1–8 | the in-line session catches (a snapped fraction; the s0 parenthetical; the never-computed net/path 0.97 via tight-tracking; the 8–23 census; the 56% unit-confusion; the all-axes traverse spec error; the cal-class ground vs its own §10.25 citation; **#8 = EXP17 RB-1's "satisfiable only by teleportation" traverse-floor sentence**) | HANDOFF:40 (species list); ORBIT_RULINGS_RELAY:47 + progress_log 2026-07-11 ("the eighth design-seat catch") |
| 9 | anchor-provenance / scripts-are-deliverables process gap at the F4 ruling | §10.27 F4-A; EXP17 prereg:3 ("NINE") |
| 10 | RED_TEAM **F1** — EXP18 assert-(i) unsatisfiable as written | RED_TEAM_banked_shelf.md |
| 11 | RED_TEAM **F2** — L2 APU estimator underspecified / "L1 APU ≈ 0 exactly" overclaim | RED_TEAM_banked_shelf.md |
| 12 | RED_TEAM **F3** — v1.2 §5.1 boundary-surprise spike stated as established | RED_TEAM_banked_shelf.md |
| 13 | RED_TEAM **F5** — scatter floor vacuum (net/path imposed where it doesn't apply) | RED_TEAM_banked_shelf.md |
| 14 | RED_TEAM **F6** — pretrained-encoder decision table glib | RED_TEAM_banked_shelf.md |
| 15 | **seat lens-1 pre-read withdrawal** — the design seat's pre-panel canon read ruled DIRECTION-ONLY ∧ SIGNATURE-DIVERGENT jointly; G7 Q1 showed F5 precedence makes the count-rung unreachable under non-loadable; the joint-naming half was withdrawn. Species: seat assertion corrected by the machinery before canon. _[corrected 2026-07-13 — seat-supplied text; the prior CC row (~~"lens-1 withdrawal … statistical-validity lens returned CLEAN"~~) was a reconstruction, the miss existed only in chat]_ | rulings relay / chat only, superseded here; the half that stood — strike the interleaving lean, surface the raw/certified split — arrived independently via lenses 3 and 4 |
| 16 | **unlike-bar comparison** — the G8 DRAFT's "orbit 5/8 vs A 0/8 p=0.013" compared different detectors (fr 2.2× apart); F6-A matched-bar correction | §10.27 close (its "catch TEN" annotated → **16** in place, strikethrough); origin = `PATHWAY_FORWARD.md` Step-2 texture instruction; caught by the **outside** verification pass; Jason-ruled |
| 17 | **unlike-bar PROSE gloss (scatter terminal)** — the SCATTER G8 terminal DRAFT's "deader than the orbit — fewer brief crossers (2/8) than the orbit (5/8)" compared scatter@N=4 vs orbit@N=3 (catch-16 species, in prose not a tab). Struck for the matched tab: scatter ≥ orbit ≥ A at every own-detector (0.6129×4: 2/1/0; 0.6111×4: 2/1/0; 0.6129×3: 6/5/3), all certified 0, max ep 4/4/3 vs ≥36 → novelty axis inert end to end. | scatter terminal DRAFT (uncommitted — caught BEFORE canon); **caught by the SEAT PRE-PANEL** (earlier than 16's outside-pass catch — the two-wall machinery tightening); standing rule reinforced: **audit every cross-arm SENTENCE for bar-matching, prose included, not just the tabs**; [[feedback_matched_bar_companions]]; Jason-ruled |
| 18 | **raw≥5-post-EXT restriction (scatter §4)** — reintroduced **raw-gating** on the certified-0 → DEAD route (a **catch-15 species**), contradicting §4's ratified two-axes spine (DEAD = no matched-bar excess ∧ census 0, no raw condition). A regression CC folded at the build review while fixing the *original* catch-15 (CONVERTS-on-raw). STRUCK. Grounds: F4-A code-precedence (committed `_primary_finding` + smoke sc4 decide DEAD raw-agnostically, pre-data); raw sits inside the floor-audit phantom bracket [0, 3.13] (raw≥5 = floor on noise); EXP16-UNDERPOWERED is a count-rung terminal that does not transport to a two-axis regime. | scatter prereg §4 (marked strikethrough amendment); **surfaced by the G7 refute-panel** (the DEAD-vs-UNDERPOWERED tension it created), **Jason-ruled DEAD** + restriction struck 2026-07-13; [[feedback_matched_bar_companions]] |
| 19 | **Previous seat** — post-SCATTER handoff called the titration/replay fork "unruled" against a pivot order **its own touch-3 words had ratified** (FRONTIER §10.28). Assertion from recollection, not read from canon. | fresh seat, from clone (EXP19 prereg cycle) |
| 20 | **Previous seat** — "replay fires now," written having read v1.2 §2–§3 and §5.2 but **never §5.1/§5.3**, where replay is fenced behind the reality ladder under CWP's sequencing rule. | fresh seat |
| 21 | **Canon hygiene — a RULING-CLASS fence made unrulable by lossy compression.** v1.2 §5.3 dropped **both** operative clauses of `MECHANISM_MAP_v1_1_addendum.md:40` (C3): the confound's definition and the baseline requirement. **New species: canon compressed past rulability.** Resolved from the origin text; fence ruled SATISFIED **without a supersession** (A2 folds the clauses back). | fresh seat |
| 22 | **Seat** — "titration interpolates between two certified endpoints." False: `K_MIN = 2` is a constant, not the knob (dwell=1 unreachable); the multiset is not preserved at any `P_GEOM ≠ 0.1`. | **Jason** |
| 23 | **Design authority** — "~2.7× SCATTER." The v1 ladder computes to **52 runs = 4.0×** (SCATTER = 5 cal + 8 verdict = 13, `exp_scatter_score.py:31–32`). Prose figure asserted without in-session derivation (§12.2 species). | fresh seat |
| 24 | **Seat, prereg v1** — (a) `wpT` asserted bit-identity to C_shuffle while §5 pinned a *new* substream `SEED_REPLAY`; both could not hold *(Jason)*. (b) Pursuing (a): **`fab.shuffled` gates code paths, not labels** — `wp1` would have failed on an assert unrelated to update parity *(seat)*. Resolved: `SEED_REPLAY ≡ keys["shuffle"]`; `fab.shuffled = (B > 1)`. | Jason + seat |
| 25 | **Seat, prereg v1** — **RECENCY-AT-EXAM omitted.** The arm's one real confound absent from the taxonomy; NON-MONOTONE routed straight to *"the account is wrong"* — but the predicted artifact **is** a non-monotone (32% of exams contaminated at B=32, zero at both endpoints). A pre-named wrong reason would have fired as a finding. | **Jason** |
| 26 | **Seat, prereg v3 — WRONG-FABRIC (new species).** Spec'd its shuffle construction, exam lock, and `fab.shuffled` evidence against **`exp13_fabric`** (the lawful-dynamics derivative; its shuffle arm `exp13_lawscram` is uncertified). **Both certified endpoints live in exp12** (`exp14_arms:55,59` → `exp12_dwell`/`exp12_shuffle`; `:42` → `import exp12_fabric as F`). `wpT`/`wp-strat` unsatisfiable as written. **Consequence: the claim-ceiling read-regime narrowing was FALSE and is struck** — exp12 rebuilds the unshuffled twin and checksums the multiset rather than disabling reads. §12.1's instrument audit catching the document that proposed §12.1. | **CC fact-check gate, pre-canon** |
| 27 | **Seat, CC brief v1** — G9: *"3 B × 8 seeds = 39."* 3 × 8 = **24**. 39 = 3 × (5 cal + 8 verdict). Number right, formula wrong — **§12.2 species, in the brief carrying the §12.2 rule.** | **CC** |
| 28 | **CC** — exp12's permuted field list is **12**, not 13 *(a, b, member, cat, dwell_id, pos, mask_slot, is_exam, is_probe_exam, nuis, bg, raw)*. And the `fab.shuffled` census missed a fifth site: **`exp14_arms:1969` — a *positive* `assert fc.shuffled`** in the coin-rung smoke. | seat (caught CC) |
| 29 | **Seat, CC brief Part B — REUSED obligation omitted on the shared-generator edit.** Part B permitted the `wperm_B` edit to `exp12_fabric`/`exp12_arms` (the `scatter_r`/`orbit_r` kwarg precedent) without attaching that precedent's fence: SCATTER edited the same generator and ran **G1a** (`exp_scatter_preflight.py:55`) to prove it inert. `wp1`/`wpT` cover only W-PERM's two endpoints; the other ~13 importers were unguarded, and a perturbed generator silently invalidates every certified record in the campaign. **New gate G0b — GENERATOR REGRESSION** ruled (deterministic replay of 5 representative arms — `exp12_dwell`/`exp12_shuffle`/scatter/orbit/expomid — fabric fingerprint bit-identity vs committed manifests; any divergence HALTs). Baseline + edited passes both CLEAN (5/5 byte-identical) ⇒ the edit is inert. | seat's omission (Jason: "my omission, not yours"), **Jason-ruled**; the gap's neighbourhood surfaced by CC's build-scope question |
| 30 | **Seat — ruled "bit-identity against committed records" without verifying any committed bit-level record exists.** `fabric_manifest` is summary statistics only; there was **nothing to compare to at the bit level**. The G0b ruling was unexecutable as written, and the baseline pass (an unedited-generator replay) turned out to be the only reference the digest could anchor to. | seat |
| 31 | **CC — G0b v1 built on a permutation-INVARIANT comparator against an explicit ruling; PASS reported without the ruled red-team.** v1 compared only `F.fabric_manifest` (order-blind summary stats; asserts on the unshuffled twin), blind to the shuffled arm's realized order — the exact failure it exists to catch; it "passed" only because the edit was inert (`wpT` showed that). **Fixed v2** (`2f8c25e`): content digest (12 permuted fields + `dwell_k` + `perm`) = the gate, manifest a companion; **fail-closed** on absent/incomplete reference; **`gen_source_sha` anchor-provenance** (baseline ≠ edited); eval-path/generator-behaviour integrity carried by the generator **diff-scope** (ruling 1), not the digest; red-team fires on ORDER + CONTENT perturbations, bound to the real build. An adversarial panel caught the fail-open + provenance MUST-FIXes before finalizing. | seat, from the pushed code ("a gate passed for an unverifiable reason is a HALT") |
| 32 | **Seat — B11 specified as a FILE hash on files carrying legitimate edits.** `EXP12Loop` lives at `exp12_arms.py:159`, which B3 edits — so a file digest trips on a legitimate edit while `EXP12Loop.step` is untouched. **A fence that misfires on a legitimate edit is a fence that gets waived** — and this fence is the anti-forward fence. Must be **symbol-scoped** (`inspect.getsource(EXP12Loop.step)`; sibling of the generator diff-scope, ruling 1). Build B11 per this, not the file hash. | seat |
| 33 | **Seat — §4.3 straddle-correction SIGN backwards.** §4.3 read the interior zero-preceding stratum as "~17.3% **minus** a straddle correction"; the exact index-list computation shows straddle **RAISES** it — the `pos==1` onset sits in the EARLIER block of a straddling dwell, its mates pushed to the next block cannot precede it ⇒ fewer local competitors ⇒ P(emitted-first) = 1/k₁ ≥ 1/k. The stratum approaches E[1/k]=17.3% from **ABOVE**, monotone (500k: 22.7→18.4→17.7→17.5→**17.29% at B=T**, z=+0.4σ). Magnitude right, sign wrong; §4.3 corrected in place. Favorable direction (bigger stratum = more power) — least-interrogated, and it fell on the ρ≤0.05 anchor B=512, so it was run down explicitly. | **CC**, from the exact computation |
| 34 | **CC — B=T stratum re-correction used the wrong horizon; and §4.3's "matched" claim retired.** Fixing ledger 33, I wrote B=T stratum = 17.29% from a 500k-**build** (`randperm(500k)`, no slicing) — but the deployed C_shuffle is `randperm(1M)` **read at [0,500k)** (`read_at=500000, h_max=1000000`, confirmed from the committed manifest). The single block spans [0,1M); the 500k read slices ~half, per-dwell competitors halve ⇒ stratum ≈ 2×E[1/k] = **30.75%** (14156/46034), NOT 17.3%. So B=T's stratum is LARGER than the treatment (17.7%) — §4.3's "exactly matched to the treatment stratum" is **retired**. FAVORABLE for wp-strat (positive control gets more power); §8 per-stratum calibration accommodates the size difference; the paid ladder (B≤2048 < read window) is unaffected. Flagged for Jason's G8 read (touches wp-strat). | **CC**, from the deployed pre-flight measure |
| 35 | **CC — dismissed the wp-strat power-transfer gap as "not a HALT, favorable."** Having found B=T's stratum (30.75%, 14,156 onsets) is LARGER than the treatment's (17.7%, 8,097), CC reasoned the larger control stratum was favorable and §8 per-stratum calibration accommodated it. **Wrong: certification at 14,156 is NOT evidence about 8,097** — the positive control must prove power at the TREATMENT's onset count, not its own inflated one. **Jason ruled wp-strat MATCHED-N:** subsample C_shuffle's zero-preceding stratum to the smallest paid stratum (B=512, N=8,097), require it still certifies over draws (report the distribution, not one subsample); if the subsampled control fails, the stratified detector is underpowered at the ρ≤0.05 anchor B=512 → **HALT → Jason**. B7/B8 proceed only against the matched-N control (the scorer is built against it). | **Jason**, correcting CC's dismissal |
| 36 | **Seat — wp-strat presumed a stratum baseline that does not exist and a detector whose constants transport; neither holds.** wp-strat was ruled "re-score the committed records and it must still certify," but (a) the committed 5/8 is a full-READ conv-`0.64×5` count over ALL onsets — NOT a zero-preceding-stratum census; whether C_shuffle certifies on its own recency-free stratum at full N is **unestablished** (structural shatter risk: a 36-onset episode yields ~6 in-stratum onsets); and (b) `consec=5` cannot be inherited onto the stratum (a 5-run spans ~28 original onsets; the timescale changed) — calibrate-in-regime transports the procedure, not the constant. **Jason ruled: SPLIT the gate — G5a stratum-viability (full N, re-cut (band,N) via `_provisional_cut`; NO ⇒ HALT, recency defence decorative) then G5b matched-N power (among-kept thinning to N=7,915, ≥90% per-seed retention derived from q·k<0.5, negative control {1,3,7}≤1% gates the method).** Caught by CC's adversarial panel, pre-commit (5 MUST-FIXes in the draft pre-registration). | **CC's panel** → **Jason** |
| 37 | **CC — recommended the stratum detector by its OUTCOME.** Faced with the fork (prereg names `_provisional_cut`; the committed C_shuffle cell used Ruling-B), CC recommended provisional "because it's clean and Ruling-B leaks" — selecting an instrument by its results, the exact thing the house forbids. **Jason: the fork is a computable TEST, not a choice.** Ruling-B exists because C_shuffle's CAL seeds convert on the full read (no clean marginal); the trigger is whether that fires in the stratum REGIME. It does — **4/5** cal seeds convert s0-class on the zero-preceding stratum (s21/22/24/25 runs 22/37/37/13; s20 no) = exactly the full-read 4/5, same seeds ⇒ Ruling-B regime forced, provisional's null contaminated; the leak rides as confirmation, never grounds. Per-onset signal recovered by deterministic replay (`exp19_replay.py`, read-only `_buffer_wave` monkeypatch), **all 13 anchors bit-exact incl. cross-commit** (committed @396c0a7/510f23b == replay @HEAD ⇒ B1 didn't perturb the arm); red-team fires A1 on a shifted draw, A3 on a corrupted capture. | **CC** → **Jason** |
| 38 | **Jason (self-correction) — the "negative control must not leak" bar set for G5a contradicts canon ledger-18.** Ledger-18 stands: raw counts never gate a finding; they scale with the false rate and sit inside the phantom floor. The non-converter stratum runs {1:4,3:5,7:6} are NOT a leak — **they ARE the phantom floor, measured** (they carry the regime's granularity + autocorrelation). House discipline = EXCESS over a measured floor (SCATTER-terminal "raw sits inside/outside the bracket"), never raw firing: converters {12,17,20,37,71}, nearest **12 = 2× the ceiling 6**, and every converter exceeds its in-regime simulated null (pinned 5000-sim, p<1/5000); non-converters sit within theirs (p 0.11–0.81). **The buried finding: ALPHA=1e-3 does NOT transport.** It is cut against an i.i.d. false-rate model (`_consec_rate`); the stratum is granular (5–13 onsets/window) and autocorrelated, so the i.i.d. model fails — a detector nominally at 1e-3 delivered an ACTUAL **2/3** false rate (**~667× miss**), a calibrate-in-regime violation inside a constant. **Ruling-B didn't fail; ALPHA did** — the instrument-assumption audit neither party ran, and the hardest/most valuable one. The in-regime simulated FLOOR AUDIT is the certification, not the α-cut binary. Standing (ruling 4): **nothing transports into the stratum regime unshown-red** — band, N, α, cadence all suspect. G5a = **PASS** by floor audit. G5b re-specified: measure the phantom floor at 7,915 (rises as the stratum thins), does the converter signal (s6=12, the marginal) still clear it? | **Jason** (self-correction) |
| 39 | **Seat — ISOTROPY-BALANCE's design surface carried five seat-originated defects, each caught downstream:** an ungrounded `iso_pen < 0.25` threshold (cap 0.539, withdrawn) · a circular FINGERPRINT check (sep_cat ≈ 0.5 is category-blindness, not a penalty signature) · a sep_a/sep_dist collapse guard that measured a crossed-label artifact, not information loss · a restated converter median (161k; true first-episode median 91.8k) · a banked α=0.3-dwell arm with no reachable falsifier (floored primary). **Common species: a number or premise carried rather than computed in-session. The standing rule already covers claims; it now covers premises.** *(Ledger-39 itself was a carried number — the seat cited a non-existent "ledger 39"; progress_log was at 38. This entry IS 39.)* | **seat** |
| 40 | **Both chairs — the WINDOW (EVAL=300) was the THIRD un-transported constant; G5b's phantom-floor "underpower" was a binning artifact.** *(Numbered 40, not 39: committed after `9a11555`'s ledger-39 ISOTROPY-BALANCE from a parallel line; the two 39s collided in-file, this entry conforms to 40 — the earlier-committed 39 keeps its number.)* After auditing α (ledger 38) and the forced band, neither chair applied "nothing transports" to the detector's BIN WIDTH. The full-read C_shuffle detector bins at 300 steps ≈ **27 onsets/window**; the thinned zero-preceding stratum (N=7,915) holds **~5** — 5.6× sparser. Accuracy over ~5 samples is coarse/lumpy → long chance runs → the phantom floor. G5b v1 measured a detector binned for a 5.6× denser regime, NOT an underpowered stratum. **Jason's three rejected alternatives were traps:** re-anchor to B=32 = the ρ=0.549 FALSE-DEAD zone the ρ≤0.05 floor exists to forbid (flattering path); accept-4/5 blinds the detector at the knee where conversion is weak BY DEFINITION → biases B\* upward → can manufacture RESCUE-AT-CEILING-ONLY (a paradigm-level conclusion from an instrument artifact). **Ruling (Jason): the operating point is an EVIDENCE requirement (~135 onsets sustained ≥0.64, X15_REPRO band 0.64/N5), not a bin requirement — preserve the granularity the detector was cut for, re-derive the bins.** Re-binning to restore ~27 onsets/window (width ≈1706), outcome-blind (operating point on the null, never on s6), s6 clears the phantom floor **3.6×** (q10 18 vs floor q99 5) — swallowed ONLY at the inherited 300 (q10 9 ≤ q99 10); all 5 converters clear at every width ≥450; robust across 4 subsample seeds; **the pre-named falsifier did NOT trigger.** Adversarial 6-lens panel FLAG-ONLY, 0 MUST-FIX (band-invariant — re-verified at 0.704: sep 5.0; divergence = real localized late episode win248–270 mean 0.876 while floor seeds have NO episode, longest run 2). Three flags carried: the "135-onset evidence" is decorative (gate = floor-separation, unit-invariant); the 3.6× magnitude is target-dependent (stratum-native density ~8.5/win → ~1.6×, binary PASS invariant); wide-window run = block-CONTIGUITY not strength, s6 rides a boundary-truncated late plateau (B\* caveat). **G5b PASSES; the recency-free stratified detector powers the treatment cell at B=512 once the window is audited.** | **Jason + CC** (both chairs) |
| 41 | **Jason (self-correction) — the ledger-40 re-bin fixed "binned too fine for the stratum" by binning for the POPULATION instead of the stratum.** The ruling was "restore the full-read's onsets-per-window" (27), but the full read runs on the WHOLE population while the treatment detector runs on the STRATUM only — matching 27 widens windows until the sparse stratum FAKES the dense population's granularity, an operating point in a regime the detector never runs in. **The operating point must be cut in the STRATUM's own regime.** At the stratum's native density the margin is ~1.6×, not the 3.6× headline (the 3.6× was the over-correction). The PASS is target-invariant (s6 clears at every width ≥450) — but the MARGIN is what G5b reports, and it resolves the way everything else this cycle did: **sweep window width, cut the operating point on the swept phantom floor (outcome-blind, before s6), name the ≥450 width floor — below which the granularity floor swamps the signal — as a COMPUTED pre-flight constant beside ρ(B) and the stratum counts.** The treatment detector runs at the swept optimum. *(Ledger 40 and 41 both from the seat's rulings this stretch — the corridor catches the chair at the same rate it catches drafts; the design working, not failing.)* | **Jason** (self-correction) |
| 42 | **CC — "fixed" ledger 41 by transporting a FOURTH un-transported constant: forced every B's stratified detector to B=T's stratum density (8.5), disguised as "one detector family."** After ledger 41 (don't match the population's 27-onset target), the seat re-cut the operating point at a UNIVERSAL 8.5 onsets/window (= C_shuffle's full-N 14156-onset stratum density), restoring it on each B by widening the window (B=512's 8097 ⇒ ~540). **Wrong: 8.5 is B=T's count; it has no business setting B=512's detector.** B=512's stratum and B=T's are different REGIMES; forcing B=512 to 8.5 transports B=T's density onto a 44%-thinner stratum — "consistency" as the disguise. The width-300 artifact (G5b) was a window cut for the POPULATION being too narrow for the stratum — the per-B SWEEP fixes that; it does NOT follow that all B share one density. **Jason ruled (b) PER-B NATIVE: the operating point is cut on EACH B's OWN phantom null by MAXIMIZING converter/floor separation (widest nearest-converter-run − floor-q99 gap) across the swept widths — no density target. One detector FAMILY = one RULE (sweep, select on the null, per B), NOT one density.** Re-spec'd `exp19_cal` (op = argmax separation; `STRATUM_NATIVE_DENSITY` deleted; ≥ width floor unchanged). Red-team CONFIRMS the op differs across regimes (B=T full 550 @15.6/win vs B=512-proxy 600 @9.5/win — no density leak) and the underpower gate stays a reachable falsifier. Notably the argmax lands in the STRATUM regime (550-600), agreeing with ledger 41 — NOT the population 1706 (past the stratum regime converters shrink faster than the floor, so the gap peaks in-regime). The bug was invisible at B=T because B=T is comfortable (powered at any width), NOT because the rules agree (separation gives 550 there, not the 8.5-rule's 300). | **Jason**, correcting CC |
| 43 | **Seat — the borrow-gate-deletion ruling over-generalized the committed asymmetry: "elevated vs A/B/D" / "A/B/D's lower floor" is C-vs-donor-A ONLY.** The borrow-gate is an α-cut null-selection rule ("cut C_shuffle's α against C's own elevated null, not the clean donor marginal"; every term — fr, alpha, false-alarms — an α-cut construct); B7 dropped the α-cut, so nothing remains for it to operate on, and the floor audit **subsumes it by construction** — every arm judged against its OWN phantom null, measured from its OWN data, so C's elevated floor is reproduced as a measured quantity, not carried by a gate (committed `exp14_band_2x2_cal.json borrow_gate` already recorded **borrow_ok:false / "SHIFTED — C uses OWN between-episode null"** — the audit's behaviour, pre-recorded). **But the deletion ruling's "elevated vs A/B/D" contradicts that same committed artifact:** per-arm floor heights are A 0.7083, **C 0.7667**, B 0.8182, D 0.8462 — C is elevated vs the density-matched **donor A ONLY** (+0.0203 = the borrow_gate's own `mean_shift`), the actual C←A relationship (both scheduled). **B and D sit ABOVE C** and were never in the borrow (separate cells, own higher floors); "A/B/D's lower floor" **inverts the risk direction** for them — judging a C-converter against B/D's higher floor UNDER-counts (a power loss, not a false gain). **Ruling (Jason, a): scope to C-vs-donor-A.** Corrected red-team (`exp19_cal --redteam-borrow`, C's committed captures only, no GPU): C's full-read floor audit self-calibrates on C's own {1,3,7} null (5/5 converters clear, sep 33), and C's floor-audit non-converter marginal 0.5017 sits **+0.0118 above the committed donor-A marginal 0.4899** — SAME direction as the committed whole-cell +0.0203 (magnitude differs by construction: {1,3,7}-only floor-audit marginal vs whole-cell α-cut between-episode shift; the same-instrument exact-magnitude cross-arm ordering, all arms under one floor audit, is **B9's** job — A/B/D have no per-onset captures and generating them front-runs B9's in-regime per-arm tab). Caught by CC from the committed 2×2 floors. *(Numbered 43, not the ruled "45": progress_log's ledger ends at 42 and the SCATTER parallel line is terminal at 39; "45" carried a +2 offset — the carried-number species of ledger 39/40. This entry conforms to 43.)* **Origin note (appended 2026-07-17, Jason's ruling — the surviving kernel of audit A1):** "borrow-gate survives / rides unchanged" originated as the seat's ratified B7 ruling, transcribed faithfully into exp19_cal:6 by CC. The error was the seat's from inception; CC's transcription was correct corridor behavior. | **CC** → **Jason** |
| 44 | **CC — B8's deployed scorer certified at the RETRACTED band (0.704) while inheriting a width cut at the ratified band (0.64): a FIFTH un-transported constant, this one leaking BACKWARD.** The scorer reused `exp19_floor`'s certification functions, whose default `FLOOR_BAND = EPISODE_BAND = 0.704` is the α-forced sparse-bin artifact that the G5b re-bin **retracted** (ledger 40/41); the op WIDTH it froze came from `exp19_cal`, which selects width by argmax separation at `RB.BAND = 0.64` (the committed X15_REPRO C_shuffle detector band). Two different detectors across one calibrate→score handoff — the width and the certification threshold described different instruments, the deployed threshold 0.064 stricter than the one its width was cut for. **Same species as ledgers 38/40/41/42, new direction: prior catches were constants transported FORWARD into a new regime unshown; this one leaked BACKWARD from a deprecated instrument into the corrected one, riding a reused function's default argument.** Invisible at B=T because both bands give 5/8 (0.704-clearing windows ⊆ 0.64-clearing) — comfortable, not correct; a dampened treatment-arm conversion in [0.64, 0.704) would have been silently un-certifiable at the band its width was selected for. **Fix:** `FL._sim_null_runs` gained a `band` parameter (default 0.704 — the committed G5a `--audit` re-run is **bit-identical**, proven by git diff); the scorer passes `BAND = CAL.BAND = 0.64` to every certification call; module-load `assert BAND == RB.BAND` fences one detector family. B=T re-validates 5/8 both reads at 0.64 with the null floors correctly risen (s6 stratified run 32 vs null max 16, all converters p<1/5000; non-converters inside their floors). Caught by CC's own pre-commit adversarial review (5 refute-default lenses + adversarial verify; 4 MUST-FIX confirmed, all fixed: this band mismatch, a vacuous `issubset` survival assert, an unhandled STRATIFIED-ONLY certification — now a named HALT anomaly — and smoke branches that never drove the HALT paths). The two-wall discipline working pre-commit: the corridor's own review caught the corridor's own leak. | **CC's review** → **CC** |
| 45 | **CC — B9 v1 (`exp19_tabs.py`) carried three self-inflicted species in one file, panel-caught pre-commit (7 MUST-FIX + 3 FLAG confirmed, all folded).** (a) **Its own validation print performed the UNLIKE-BAR subtraction its header declares structurally absent** — the drops line pinned full-N to its 550-row and subtracted the proxy's 600-row read (F6-A species, catch-16's exact shape); on the committed captures the two coincided by set-coincidence, masking the forbidden derivation. Fixed: drops computed per matched row, same bar both cells. (b) **`_thinned_proxy` claimed "bit-reproduced" but reproduced a DIFFERENT draw** — a SHARED pinned generator binds the k-th randperm to the k-th seed VISITED, and v1 iterated `range(8)` where the committed `exp19_cal._redteam` iterates conv+nonconv `[0,2,4,5,6,1,3,7]` — so the committed op 600 was worn by data whose own-null op is 900 (provenance asserted-not-computed, the anchor-provenance species). The "s2 drops at both bars" finding EVAPORATED on the true draw: corrected result = proxy@550 (foreign bar) k=4/8 with **s6** dropping (the G5b marginal converter — the coherent story), proxy@600 (own bar) k=5/8 {0,2,4,5,6}, NOTHING drops. Fixed: `REDTEAM_ORDER` pinned + provenance RECOMPUTED as an assert (`cal_floor_audit` on the exact constructed draw must return op 600). (c) **The ledger-43 floor surface itself nearly re-inverted**: `floor_ceiling` (max over per-seed sim nulls) is carried by the strongest converter's episode-inflated p̂ at every validated bar — on the max, an arm with MORE SIGNAL reads as ELEVATED FLOOR, the exact inversion species row 43 exists to prevent. Fixed: ceiling relabeled certification ENVELOPE with `ceiling_carrier` named; cross-cell floor ordering reads on `floor_median`/per-seed heights with p̂s visible; evidence-grade PHANTOM-floor ordering = non-converter-labeled, downstream only (validated: thinned ≥ full 3/3 at BOTH bars once episode inflation is excluded). Also folded: McNemar-exact paired companion = evidence-grade for same-seed cells (independent-groups Fisher annotated context-only there); equal-width bars collapse to ONE row + `bars_coincide`; exact-schema smoke (the old superset/substring check was vacuous BOTH directions); a cross-read mutation-killer (a width-ignoring `_bar_read` — the silent unlike-bar tab — previously PASSED the smoke, now dies in smoke and validation); `cell()` snapshots caller data. | **CC's panel** → **CC** |
| 46 | **Seat — the session audit's headline finding (A1) asserted committed-ledger misattribution from the seat's own spoken numbering without reading the log at HEAD** (clone available, three commits stale). Canon was already clean — row 43 headlined Seat, CC→Jason; the chat-side charge against CC was real but never committed. The audit committed the F2 species it named, in its most prominent item; the rows-19/20 species (canon asserted from recollection). *(Record: `docs/EXP19_SESSION_AUDIT.md` verbatim + `docs/EXP19_SESSION_AUDIT_VERIFICATION.md` at HEAD — the pair.)* | **CC's verification run** → **Seat** |
| 47 | **Seat — prereg §6's anti-forward fence named three files; the effective executor is `Stage0Loop.step` at `experiments/04_stage0_mvp/loop.py:208` via the MRO** (verified at the seat's clone and re-verified at HEAD) — a hash on the named files passes while the actual step changes. The method handoff's own words: "verify at the code/MRO level." Fixed by the two-layer fence (B11, `a8fcfb3`): learner chain frozen symbol-scoped vs baseline + runtime `learner_fence()` on the live MRO with a planted-override red-team. | **CC at B11 build** → **Seat** |
| 48 | **CC — B8's "dec_cat median 0.6637" is s0's single value wearing the label median**; per-seed `dec_cat_n=0` fields carried the truth, the summary hid the coverage hole (**1/8 at B=T, 0/8 at B=1** — only the dec_cat anchor-verification re-replay of s0 carries the field). Convenient-summary species (F2). Self-caught in the verification run, disclosed pre-fix; fix = coverage-honest companions (per-seed `dec_cat_n` surfaced; no bare "median" over n=1), rides the N1 commit. The dec_cat-by-B endpoint holes route to the decay-companion replays (C1/D1 shared compute, ruled 2026-07-17). | **CC** (self-caught) |
| 49 | **Both chairs, chat-side — "at chance for every seed, including the converters" contradicted by the same message's table (s6 tail-50 = 0.616)**; the seat repeated it with a disclaimer instead of reading the table; resurfaced one gate later as flag 3 (horizon truncation). The committed decay doc was already correct (distinguishes s6 0.616 from the four at ~0.48–0.52; its "~chance for all seeds" sentence describes the frozen 500k checkpoint, which is true) — **no doc surgery.** | **both chairs** (chat-side; audit A4 + verification) |
| 50 | **CC — the first cell-read script label for s6 used an INVENTED 0.05 constant** against the ratified "no thresholds invented" rule; self-caught pre-commit, conformed to the ratified MIXED cell, disclosed in the artifact (row-44 precedent: pre-commit self-catches are rowed). | **CC** (self-caught) |
| 51 | **Seat — the ratified MIXED cell under-specified the move statistic** ("within-band" is ambiguous across sd / dead-envelope / SE readings); surfaced by the read's knife-edge margins (s6 Δ 0.196 vs sd 0.211); remedied by the pre-named three-reading sensitivity companion (appended to the cell-read artifact + doc; primary stays Δ-vs-sd). | **Seat** (via the read) |
| 52 | **CC — the certification law's advertised tail bound fails at knife-edge margins: `certified = obs > null_max` over ONE pinned 5000-draw stream treats the pinned stream's max as the floor, but null_max is itself a DRAW — at B=512 full-read s3 (obs 6), the pinned stream's null_max=5 is a 22/200 minority draw (modal null_max = 6 = the observed run) and the true per-draw tail P(null ≥ 6) ≈ 4.2e-4 exceeds the docstring's advertised p<1/N_SIMS = 2e-4.** The cert is an 11%-stability event; the corridor headline "full 6/8" reproduces in 9.5% of independent stream families (modal 5). s0 milder (0.860, law-compliant 2.9e-5). The emphatic four unflippable (200/200); **the primary B\* bracket survives ALL 200 streams — the defect qualifies a seed, not the finding.** Species: a single pinned stream's max-statistic wearing a p-value guarantee it only delivers away from the boundary. Remedy (panel-ruled): the DRAFT carries the rates, s3 rides QUALIFIED; terminal-instrument note for any future law revision (revision itself = a ratification act, not taken here). Caught by the terminal panel on the seat's ruled target. | **panel** → **CC** |
| 53 | **CC — the committed `save_checkpoint` docstring's "sufficient to resume" claim is FALSE: a checkpoint-resume diverges from the from-scratch trajectory** (caught by the tails' own fidelity smoke BEFORE any tail ran; a three-way state-transplant matrix — `mix`, `stim._calls`, `mask_emb` — did not close the gap; forensics recorded in `exp19_tails.py`'s retained `_resume`/`smoke` evidence instrument, root cause NOT resolved — report-don't-patch). Phase-2 mechanics conformed to the committed ec8121a rule instead ("full runs from the start; no checkpoint-resume anywhere"); all 8 tails prefix-anchored digit-exact to their committed g9 records. Standing flag: any future resume-dependent design must first fix and prove the checkpoint's completeness with a fired smoke. | **CC's fidelity smoke** → **CC** (instrument flag) |
| 54 | **BOTH CHAIRS — the §2.4 non-causality paragraph reached canon §10.29 by CITATION, not verbatim paste, against the prereg's own carry rule ("carry verbatim, not by citation", prereg :432): the block was omitted through an explicit two-item fix order (CC), and the promised land-time spot-check slipped to post-close (seat).** State verified at HEAD `0d6b102`: the carry WAS present verbatim in `EXP19_TERMINAL_SURFACE.md`; canon alone cited. Patched post-close: canon block pasted byte-exact (diff-verified vs prereg §2.4), terminal surface annotated in place — no number, route, or definition touched. **Tail note:** the post-close fix order itself sat unexecuted across a session boundary — the sixth relay crossing — which is why the echo-back handshake is standing (this order was echoed back verbatim before execution). | **seat's post-close verification pass** → **CC + seat (both chairs)** |
| 55 | **Seat — the STEP-0 prereg committed a per-channel estimator whose input support was never verified per channel: the committed mask schedule guarantees position-1 word-mask (`exp12_fabric.py:27`), so §4's vis-channel onset-dominance domain was structurally EMPTY (pos_err_vis carries p1 in 0/13,328 columns across the 8-record cell) — the prereg's G0 checked fields, not buckets.** Species: estimator-support unverified at prereg. The machinery caught it: census-surfaced HALT, G2 HELD lawfully, no workaround; resolved by AMD-1 (word-channel-only cells; vis rides descriptive). Standing remedy ratified with this row: the CORRIDOR_PROTOCOL rider "Estimator-support check at pre-flight: every pre-named estimator's input domain verified non-empty from the real data path." The ledger carries this seat's rows 46 and 51 already; the record's value is that it carries everyone's. | **census HALT (CC's instrument)** → **Seat** |
| 56 | **CC — the EXP20 G5 certification (and the G3 cal split + stream nulls) ran on EXP19's 500k window grid while the ratified law reads at 1M: `SC._certify_seed`'s DEF-TIME `read_at` default (exp19_g5b_rebin.py:43 READ_AT=500_000 → exp19_cal.py:49 → exp19_scorer.py:47 → `_bin`) silently truncated every certification; `exp20_verdict.py`'s READ_AT=1_000_000 was dead code — the 6th un-transported constant, and the first through a def-time default (module-attr injection cannot reach it; the parameter must be passed).** Proven bit-exact both directions by the G6 refute panel (3 lenses refuted, 8/8 adversarial verifies CONFIRMED). Consequences at the ratified law: K512 6/8→7/8 (s3's "run 4" = the first 4 windows of a 140-window episode straddling the 500k grid edge, 140 > null_max 45); K128 s2 certifies BOTH reads (full 39>7, stratified 13>10 — the powered-stratum certification; stream-emphatic 200/200, unqualified); K32 0/8 robust; the six original K512 certs survive; the "episodes all end by 429k / transient-then-gone" geometry claim was a truncation artifact and is retracted. Fix `e4d1007`: explicit read_at param, DEFAULT UNCHANGED (every EXP19 result byte-preserved, anchored); EXP20 callers pass 1M; powercert deliberately stays on C's committed 500k grid (reported-never-bridged). The `92e7d44` artifact = the 500k-truncated read, superseded never overwritten. Species kin: ledgers 38/39/40/42/44 — this one hid in a parameter DEFAULT, invisible to module-injection audits. | **G6 refute panel** → **CC** |
| 57 | **Seat — the drafted §10.31 close block carried numbers not anchored in the record: the close date "2026-07-26" (no referent — the terminal and verdict runs committed 2026-07-28, the prereg 2026-07-25; folded to the 28th on Jason's one-line word) and the section number §10.31 drafted against an unoccupied §10.30 (§10.29 was canon's last numbered section; resolved by Jason numbering the bench re-anchor as §10.30, `4cbb344`).** Species: carried numbering — a number written from the chair's own frame rather than read from the record; kin of rows 39/40/43. Both instances were caught at the canon gate before landing (the date by the pre-landing fact-check, the gap by the §10.30 existence check); neither entered canon wrong. The ledger carries every chair's rows — that is its point. | **CC's canon-gate fact-check** → **Seat** |

RED_TEAM **F4** (supersession mark) and **F7** (hygiene) are folds, NOT counted as catches (the pass
paying for itself). **Two prior "TEN" labels reconciled** (never rewritten): the §10.27 close's "catch
TEN" → **16** (strikethrough-annotated in place); the rulings-relay's "TEN-for-lens-1" → **15**
(chat-side — nothing in-repo carried that label to annotate). This ledger absorbs every earlier prose
count (EIGHT / NINE / "10–14"); those remain correct as-of-their-commit and now point here.
