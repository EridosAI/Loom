# RED-TEAM PASS — THE BANKED SHELF (design seat auditing itself, 2026-07-12)

**Scope: MECHANISM_MAP v1.0 + v1.2, EXP18, EXP-L2. Findings ride WITH the shelf to `docs/`; each folds as a marked amendment at commit or at the named trigger. None require re-drafting now; two are design bugs that would have bitten at build time. Session catch-count (corrected, fact-check 2026-07-12 C): F1/F2/F3/F5/F6 are catches **10–14** (the in-line eight + the scripts-are-deliverables process gap = nine precede them); **F4 (supersession mark) and F7 (hygiene) are folds, not counted as catches** — the pass paying for itself.**

---

## F1 — EXP18 §A.2 assert (i) is unsatisfiable as written [DESIGN BUG — fix at trigger, MUST]

Resampling ictrl's *anchors* from the orbit's realized **pose** pool, then trembling around them, yields ictrl pose marginal = pool ⊛ OU — strictly wider than the orbit's marginal (the pool already contains the orbit's jitter; the OU adds it again). The match-assert as written fails by construction. **Fix:** assert (i) re-specified as *anchor distribution == orbit pose marginal* (exact by resampling), with the pose-marginal residual (the predicted, computable OU widening) **reported**, not asserted away. The confound being controlled — interior concentration — is fully covered either way; the bug was in the assert's object, not the design's logic. Secondary note: the orbit's own pose-deviation-from-anchor differs from tremble's (tracking lag inflates it), so "exact marginal match" was never achievable — the honest target is location/concentration match plus a characterized residual.

## F2 — L2's APU estimator is underspecified and "L1 APU ≈ 0 exactly" overclaims [DESIGN BUG — fix at trigger, MUST]

"Rotation is linear" holds *within a plane with a per-dwell-fitted map*; a single **global** linear predictor across dwells with random planes has APU > 0 on L1 too, and even a constant-velocity baseline has curvature error ≈ r·ω²/2 per step (≈0.14 of the step at candidate constants — not 0). **Fix at L2's prereg:** pin the estimator as *per-dwell best-fit rotation in the fitted plane* (deterministic; L1 → ~0 by construction, L2 → >0, falsifier exact), or explicitly re-derive the floor bracket against whichever estimator is pinned. The metric's *purpose* survives; its arithmetic identity did not.

## F3 — v1.2 §5.1 states the boundary-surprise spike as established [OVERCLAIM — tense fix, one line]

"A dwell boundary is a 99% jump → surprise spikes" — the 99% is the *pose* jump [MEASURED]; the *loss* spike is CWP's **premise**, and the one committed glimpse of `pos_err_vis` is flat-ish and non-monotone. The step-0 diagnostic exists precisely to test this. Fix: condition the sentence ("IF losses spike at boundaries — step-0 checks this"). The diagnostic's priority ranking already reflects the doubt; the prose didn't.

## F4 — Cross-doc conflict: L2's trigger line vs v1.2's sequencing [SUPERSESSION MARK — mechanical]

EXP-L2 §status says "primary trigger: EXP17 SWEEP DEAD" and its §3 routes L2-dead → L3. v1.2 (written later) supersedes: **scatter first; L2 = the conditional interpolator, trigger = scatter-CONVERTS (post-orbit-DEAD)**; scatter-dead skips L2 entirely. Fold as a marked supersession on the L2 doc at commit — do not silently rewrite.

## F5 — Scatter has a floor vacuum [SPEC GAP — fill at scatter's prereg]

Net/path is an anti-revisit statistic for *paths*; scatter has no path and fails it by construction — correctly, and the ladder never imposed it on scatter, but nothing was pinned in its place. A fast reader could fill the vacuum wrongly. **Fill:** scatter's selection/verification statistics are per-step displacement contrast (≥ κ× tremble per-step) + distinct-pose coverage per dwell + the confusion-bound ceiling; explicitly NOT net/path. Also make the window's arm-class dependence explicit where the two-wall law is stated: path-arms take the dwell-scale lower wall; scatter-class takes per-step.

## F6 — The pretrained-encoder arm family's decision table is glib [JUDGMENT FLAG — work out at its prereg]

v1.2 §5.4 assigns "frozen reads M1, trainable-mature reads race" — but frozen+dead kills *both* stories (mature features, no instability, still dead), frozen+converts is M1-or-race ambiguous, and the trainable variant separates them only via a specific argument (instability-restored, early-trap-absent) that needs proper working-out. The banked triggers are fine; the one-line assignments must not be inherited as settled.

## F7 — Sim-derived numbers in v1.2 lack the supersession rider [HYGIENE]

"~1.4× the noise floor," the (r≈0.9, 16°) region, and kin are sim estimates; EXP18 carries the "freeze artifact supersedes" rider, v1.2 does not. Fold the same rider into v1.2's status block. Corollary carried from the session: no sim-derived absolute is load-bearing anywhere on the shelf — verified true after this pass, with F7 closing the labeling gap.

## Clean under attack (worth recording)

The order-only foundation, the ladder's one-property-per-rung discipline, scatter-first bracketing logic, the CWP sequencing fence, bootstrap-as-control's held-out-probe form, EXP18's certification rule and Part-D blind claim language, and the render-gain audit's no-amendment-needed retroactivity — each was pushed and held.
