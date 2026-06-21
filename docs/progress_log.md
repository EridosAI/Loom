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

### Next

Initialisation (the bootstrap-from-newborn / minimum pre-existing dense structure) is
downstream of this result — not started.
