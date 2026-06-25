## Addendum (2026-06-25) — Post-Phase-1: gap-3 developmental shape, slow-start unpool, characterisation sweep

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
