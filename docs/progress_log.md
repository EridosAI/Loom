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
