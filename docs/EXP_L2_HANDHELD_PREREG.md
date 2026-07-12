# EXP-L2 — HAND-HELD (UNPREDICTABLE-INCREMENT ORBIT) — PRE-REGISTRATION (BANKED-CONDITIONAL)

**Status: BANKED-CONDITIONAL DRAFT (design seat, 2026-07-11). Primary trigger: EXP17 terminal = SWEEP DEAD (certified). [F4 SUPERSESSION, 2026-07-12: superseded by `MECHANISM_MAP_v1_2_RECONCILED.md` §3 (written later) — SWEEP-DEAD is now a *necessary-but-not-sufficient precursor*; the live trigger is **scatter-CONVERTS (post-orbit-DEAD)**, and **scatter-DEAD skips L2 entirely**. Body retained unchanged per supersede-don't-overwrite; read the trigger through this mark.] Secondary status if EXP17 CONVERTS: banked as a characterization arm ("does unpredictability add anything once predictable motion suffices?") — not dead material either way. Inherits the full standing machinery (corridor, census, floor audits, [0,500k] referent, deployed-horizon pre-check, contrast-form targets, one-code-path).**

**What this rung tests.** L1 (orbit) delivers per-frame novelty but is **maximally predictable** — a constant-ω circle is a *linear recurrence*: the next anchor is exactly a fixed rotation of the current one, so a linear one-step predictor achieves near-zero error on it. If EXP17 dies, rung 3′ (extrapolative satisfiability) is the prime suspect, and L2 is its direct test: **keep novelty, identity-persistence, and coherence; break exact extrapolability.** "A slightly different angle each time."

---

## §1 The arm — `exp12_dwell_hand`

L1's orbit with two stochastic ingredients, both from the dedicated substream, **monotone phase preserved** (the billiard lesson: raw random-walk anchors revisit and fail net/path by construction; the hand keeps *going around* — jerkily):

- **Stochastic angular increments:** ω_t drawn per step from a pinned positive family around the L1-frozen ω* (form: RATIFY slot; candidate lognormal with CV as the knob). Phase strictly increasing → no revisiting → net/path survives.
- **Plane wobble:** small random rotation of the orbit plane per step (bounded angular rate; second knob), so the trajectory is a wandering arc, not a perfect circle.

Held fixed to L1: r*, ω̄ = ω*, centering rule, dwell law, member-per-dwell, mask policy incl. mid-dwell grading (rung 2 intact — internal control unchanged), exam density, background path UNTOUCHED (the EXP17 pin carries; see §5 for where Jason's background idea lands).

## §2 The unpredictability metric — pinned, deterministic, with its falsifier

**Anchor-path unpredictability ratio (APU):** fit the optimal linear m-lag one-step predictor to the *noise-free anchor path* (deterministic least squares on the realized fabric; m pinned, candidate 4); APU = RMSE / mean anchor step. Facts that make this clean: **L1's APU ≈ 0 exactly** (rotation is linear) [F2-pending, 2026-07-12: "exactly" holds only under the *per-dwell best-fit-rotation* estimator; under a single global m-lag predictor across the per-dwell random planes L1's APU > 0 (curvature ≈0.14/step) — pin the estimator (per-dwell fit) here at ratification, or re-derive the §2 floor bracket against whichever estimator is pinned; see RED_TEAM F2]; L2's APU > 0 with variance set by the knobs; the falsifier is exact (CV→0, wobble→0 ⇒ APU→0 ⇒ the assert fails — the required no-op falsifier).

**Selection (house pattern — the gentlest jerk that breaks extrapolation):** grid over (CV, wobble-rate); select **minimal per-step perturbation** satisfying: (i) APU ≥ floor (RATIFY slot; suggested bracket 0.25–0.40 — a quarter-to-third of each step genuinely unforecastable; grounds computed at build from the grid), (ii) the L1 kinematic floors still hold on realized L2 fabric (net/path ≥4× tremble, traverse ≥2.5×, ≤0.50 — monotone phase should preserve them; verified, not assumed), (iii) the correspondence window holds (dwell-scale lower edge; per-step ≤ confusion bound). Frozen (CV*, wobble*) with drift-assert; per-seed floors; region-empty → HALT to design.

**Scope honesty:** APU is a *fabric-side pose-space proxy* for what the learner faces in render space through its own encoder. A render-space companion rides (§4/§5); the assert stays pose-space and deterministic.

## §3 Reads, comparators, outcome cells

Own cal {20,21,22,24,25}, own provisional band, full standing pre-gates; verdict {0–7} @1M, mid-ckpt 500k, primary at 500k; EXT {8,9}, sub {10–19}.

**Three comparators, two contrasts:** A_dwell 0/8 (the conversion primary, Fisher one-sided) and **L1-orbit committed** (the decisive adjacent read — L2 converting where L1 died is the rung-3′ confirmation). C_shuffle context row rides.

- **L2 CONVERTS** (≥5 certified, floor-clean, n≥8, census-decisive): **UNPREDICTABILITY WAS THE GATE** — rung 3′ confirmed; the reality ladder validates at rung 2; and the EXP13 bridge inherits a load-bearing requirement: *lawful fabrics must carry hand-held-class increment noise or they will re-wall.* (That single sentence redesigns EXP13.)
- **L2 DEAD** (certified-0): novelty + unpredictability + coherence still insufficient within a persistent identity. Route: **L3 (contexts) is the ladder's next rung**; the interleaving titration remains the ladder-exhausted fallback, not the next move. Pre-named as a route, decided by Jason at the terminal.
- Lottery → EXT per D1; cal-converts → Ruling-B machinery; gradient-persistence internal control expected ≈ A's (+0.1416 class) — its collapse = instrument alarm; liveness/participation standing.

## §4 Companions (reported, never gated)

APU realized per seed · render-space per-step increment distribution (§5's audit) · plane-wobble realized rate · folded/unfolded delta + reflections (still zero by construction — assert) · onset-marginal delta vs A and vs L1 · 1M tail · cortex echo (div_nuis / d2_spread vs the A↔C referents) · acquisition-onset distribution (the window's breakdown signature watchpoint).

## §5 Jason's room/asymmetry idea — translated, split, and one audit it triggers NOW

The substrate has no 3D room or renderer-level viewpoint, so literal parallax and object asymmetry aren't directly available — but the idea decomposes into three functional pieces, none ignored:

1. **Render gain (the "asymmetry" content) → an audit this prereg requires, and L1 gets retroactively.** The kinematic floors live in pose space; the learner lives in render space. If pose axes have anisotropic appearance gain, a random orbit plane can be kinematically compliant yet perceptually weak. **Audit (fabric-only, deterministic, computable from the frozen fabric + committed renderer at any time — no EXP17 amendment needed):** per-dwell mean render-step / pose-step ratio along the realized trajectory, vs the same ratio over random pose pairs (isotropy reference). Rides as an L2 pre-flight read AND a retroactive L1 characterization. Conditional pin: if L1's audit shows severe anisotropy, an L2 amendment MAY add a render-gain floor to plane sampling — ratification-class, not silent.
2. **Within-dwell background-motion coupling (the "parallax" content):** lawful co-variation of background with phase is *predictable* — it amplifies render gain, it does not add unpredictability. It therefore belongs with contexts, not here.
3. **Per-dwell rooms ("the mug in two kitchens") + the parallax coupling → L3, enriched.** Jason's framing upgrades L3 from bare background-per-dwell to: background fixed per dwell, *slaved to orbital phase within the dwell* (reality-like), different across dwells (context decorrelation, forcing identity to bind to the object — today object and context are confounded by the near-constant `bg_const`). Banked verbatim into the ladder; the EXP17 background pin lifts exactly there, one moving thing at a time.

## §6 Discipline traps

Manufacturing fence: L2 is a regime probe — the APU floor is selected for *minimal* sufficiency, never searched against conversion outcomes (selection is fabric-only, X-blind, frozen before any training run). Anti-forward audit unchanged and doubly loaded: an unpredictable world makes forward prediction *both* more tempting to add and more obviously fenced. One rung, one property: background untouched, dwell law untouched, grading intact.

---

**Plain language.** The moving-camera world might fail for a sneaky reason: its motion is *perfectly smooth*, so a lazy learner can ace the quizzes by guessing where things will be instead of knowing what they are. This experiment keeps the camera moving around the object but makes the motion jerky — like a hand holding a mug up to show you: always progressing, never exactly forecastable. One number certifies the jerkiness (how much of each step a forecaster can't see coming), one dial sets the gentlest jerk that defeats forecasting, and everything else stays identical. If learning switches on here, we've found that the world must be *not just new but surprising* — and any realistic world we build afterward has to carry that surprise. If it still fails, the next drop of reality is Jason's two kitchens. And his room-and-asymmetry idea isn't discarded — it split into an audit we now run on the current experiment (does motion actually *look* like motion to the learner?) and a richer design for the rung after this one.
