# MECHANISM MAP — ADDENDUM v1.1: THE REALITY LADDER

**Status: BANKED SYNTHESIS addendum (design seat + Jason, 2026-07-11). Folds into MECHANISM_MAP_conversion_gating.md at commit. Source: Jason's orbit-skepticism note and the mug/kitchen examples — this addendum formalizes them. Tags as in the map.**

**[SUPERSEDED by `MECHANISM_MAP_v1_2_RECONCILED.md`, 2026-07-12 — retained as provenance, not deleted:** this is one of the two v1.1 forks v1.2 reconciles; where this doc and v1.2 differ, **v1.2 governs** (notably: the SWEEP-DEAD table in A1 below is *two-way*; v1.2 §2's *three-way* table — which adds the predictability/rung-3′ branch — is the governing form). **[F7 sim rider:** the "~1.4× the noise floor" figure in A1 is a sim estimate; the landed freeze artifact **confirms** it (deployed per-step median 0.2261 = 1.42× floor).]**

---

## A1 — Orbit is a point probe on a continuum, and SWEEP-DEAD is ambiguous as currently tabled

Rung 3 (local visual satisfiability) is not binary. The orbit moves per-step novelty to ~1.4× the noise floor along a **smooth, predictable path** — rung 3 degrades gracefully, it does not die. The operator is wave-local, so path-predictability cannot be exploited through recurrence — but it can through weights, and weight-drift exploitation of *slowly varying* targets is exactly the mechanism family the map already measured (coord. 3). [INFERRED]

**Consequence for the EXP17 outcome table:** SWEEP-DEAD conflates two readings — **(a)** identity-interleaving gates conversion (M3-pair), or **(b)** the per-frame novelty dose was insufficient (rung 3 still satisfiable at orbit speeds). *[Superseded by v1.2 §2's three-way table — the predictability-protective (rung 3′) branch was the missing third reading; read this two-way form through that mark.]* The map's §4 read of DEAD as "interleaving is the gate" is therefore provisional pending the disambiguator below. SWEEP-CONVERTS is unaffected (a positive at *low* novelty dose is the strongest possible form). [The correspondence-window position at frozen (r, ω), already a pre-flight deliverable, is the quantitative anchor for how far along the continuum the orbit actually sits.]

## A2 — The disambiguator: the SCATTER-DWELL (Jason's mug, formalized)

Someone showing you a mug turns it a *slightly different, unpredicted* way each moment — per-frame novelty without a smooth path. The arm: **per-frame pose resampling within a dwell-local ball** (identity held; ball center per dwell; radius pinned under the confusion bound so identity-correspondence survives; draws from the dedicated substream). Properties: maximal per-frame novelty within identity · zero path smoothness · zero interleaving · dwell law, member, word channel, mask policy all held to A.

**Outcome table (named now):**
- **Scatter CONVERTS (orbit having died):** *smoothness itself was protective* — a predictable path keeps rung 3 satisfiable regardless of displacement. The correspondence window becomes **two-sided in function**: frame-to-frame change bounded *below* for learning (must defeat local satisfiability) and *above* for identity (must preserve correspondence) — the hawk/sheep principle sharpened into a two-wall design law. Interleaving exonerated.
- **Scatter DEAD:** identity-interleaving gates, hard (M3-pair confirmed with input novelty maximal) → the dwell-length titration measures the interleaving dose. Reading (b) is closed.
- Scatter converts *and* orbit converted: novelty suffices at low dose; scatter adds the smoothness-irrelevance datum.

**Sequencing:** orbit → (if DEAD) scatter → (if DEAD) titration. One arm, one axis, per step. [DESIGN — banked, trigger = SWEEP-DEAD]

## A3 — The reality ladder: escalation axes, one at a time

Guiding principle made operational: **when the minimal sim underdelivers, escalate toward reality along exactly one axis** — each rung buys realism at the cost of attribution cleanliness, and the ladder is the discipline that keeps "more real" from becoming "more confounded."

- **Axis N — novelty dose within identity:** tremble → orbit (smooth) → scatter (jumpy) → [compound pose+appearance motion]. Attacks rung 3's precondition directly.
- **Axis C — cue isolation across dwells:** the *kitchen test* — the same member appears against different backgrounds in different dwells, so the object becomes the only stable correlate of the word. This attacks a shortcut the map v1.0 did not list: **rung 3.5, context-as-proxy** (predicting the word from background/context statistics rather than the object). Note the current fabric's background is OU-toward-`bg_const`; whether background currently carries member information is a **code/artifact check to run before this axis is designed** — if it is uninformative today, rung 3.5 is latent, not active, and Axis C is a *generalization pressure* arm rather than a shortcut-removal arm. [CHECKABLE]
- **Axis A — appearance nuisance:** lighting/texture variation within identity; a second novelty channel orthogonal to pose.

**Fence note:** every Axis arm is fabric structure (regime probes, shuffle-class); none engineers a loss. The anti-forward audit applies at full strength on all of them.

## A4 — Falsification additions to the map

- Orbit DEAD + scatter CONVERTS → smoothness-protective; the two-wall window law enters the map as [MEASURED-conditional]; M2-as-duplication is refuted in its "displacement is what matters" form.
- Orbit DEAD + scatter DEAD + titration flat → the ladder below rung 4 is mischaracterized; escalate to representation-level probes (unchanged from map §5, now with the novelty branch properly excluded first).
- Any Axis-N arm degrading **acquisition** → the acquisition/conversion dissociation is dose-limited; the confusion bound was set too loose; re-derive the window's upper wall from the acquisition read, not the rendering distance.
