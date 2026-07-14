# ISOTROPY-BALANCE (α-sweep) — PREREGISTRATION  [RATIFIED — Jason touch-1, 2026-07-14]

**Status:** RATIFIED (Jason, 2026-07-14; "prereg good to go"). Authored by CC on Jason's ruling; the SPREAD-IS-ERASER
hypothesis is the SEAT's. Separate arm, separate corridor — **does not touch EXP19** (`l_spread` is identical at every
B; G5b proceeds unaffected). Compute queues **behind the EXP19 run** (Jason).

**Author:** Jason Dury. No co-author.

---

## §0 — Provenance & the object under test
- **Manipulation point:** `alpha_spread` (`experiments/04_stage0_mvp/constants.py:35`, committed `= 0.1`). Constants-only.
- **The term:** `α·l_spread`, `l_spread = spread.spread_loss(vision.emit(...), P=64)` (`loop.py:205`, `src/loom/spread.py:19`),
  an **isotropy penalty** `mean² + (var−1)²` over P random projections, acting on the **vision cortex**
  (`loop.py:204`, "grad flows to vision"). Fixed point = isotropic emission covariance.
- **Established this session (R8–R11, committed data + code):**
  - Capacity is NOT the block — the 608-param cortex reaches sep_cat max 0.86–0.96 / asg_cat max 0.66–0.95 in the
    shuffle converters (R8).
  - The vision salience **flickers** cyclically in lockstep with the exam episodes (R10; REPRESENTATIONAL-FLICKER 5/5).
  - After t2=1200 the ONLY two standing forces on the vision cortex are `gain·l_pam` (completion) and `α·l_spread`
    (isotropy); tie penalty and re-pool are zero (R9: `lam1_lo=lam2_lo=0`, `repool_rate=0`).
  - `l_spread`'s fixed point IS the observed dead-arm floor (Stage 0 below). SPREAD-IS-ERASER is form-confirmed;
    its **magnitude gate is unmeasured** (Stage 1 closes it).

## §1 — Hypothesis (SPREAD-IS-ERASER)
The isotropy regularizer `α·l_spread` is the standing force that pins the certified-dead cortex at the isotropy
floor and erases the salience the completion gradient transiently builds. If so, **reducing α should release the
brake** and let the certified-dead `exp12_dwell` arm sustain differentiation (convert) — WITHOUT re-ordering the
fabric. Falsifier: α-invariance (INERT) ⇒ the ordering framing survives intact.

## §2 — STAGE 0 struck as evidence + the discriminating read  [AMENDED, touch-1]
**FINGERPRINT is STRUCK as evidence (AMENDMENT 1).** sep_cat ≈ 0.5 is what ANY category-blind representation
returns — isotropic or not — so "0/38 dead-arm terminals at the floor" merely **restates the null result**; it
does not fingerprint the penalty. The 38 terminals (C_dwell 0.476 · EXP16 X 0.474 · EXP17 orbit 0.473 · SCATTER
0.474; range [0.467, 0.500], 0/38 > 0.50) are retained as **DESCRIPTIVE CONTEXT ONLY**, not evidence.
**Do not write 0.50 as "the cap":** 0.50 is `E[sep_cat | random isotropy]` (sim 0.5000 ± 0.006) — the expectation
under random isotropy, a *different quantity* from the penalty's fixed-point signature. (Seat's earlier 0.539 is
withdrawn — it rested on an `iso_pen < 0.25` threshold with no outcome-independent grounds.)

**The discriminating read (replaces the fingerprint):** the penalty's signature is a **spherical emission
covariance — flat eigenspectrum, effective rank ≈ D = 16 — NOT sep_cat = 0.5.**
**Availability (checked this turn):** the 16-probe emissions / their covariance / `effective_rank` are **NOT
stored** in the committed dead-arm records (no rank/spectrum/eig/cov column; `spread.effective_rank` /
`covariance_spectrum` (spread.py:37,46) exist but are eval-only and **uncalled** in `_eval_column`). The stored
scalars (`div_*` = residual sub-block norms, exp12_arms.py:318–320; `pairwise_emit`, `sep_*`) do not yield the
eigenspectrum. **⇒ cannot compute from committed data → FOLDS INTO STAGE 1's instrumentation** (do not re-run).
**Cells:** flat spectrum, eff-rank ≈ 16 ⇒ the penalty is shaping the cortex (**FOR**) · uneven, eff-rank < 16 ⇒
vision has structure, just not category (**AGAINST**).

## §2b — STAGE 0b/0c — the structure guard  [0b HALT WITHDRAWN; 0c folds into Stage 1]
**STAGE 0b (sep_a/sep_dist during vs between episodes) — WITHDRAWN as a finding (AMENDMENT 5).** The measured
anticorrelation (during-ep sep_a→0.512, corr(sep_a, sep_cat) = −0.45…−0.62, 5/5) is a **`_sep_ratio` ARTIFACT**, not
member-information loss: `_sep_ratio` is **non-additive across crossed factors**, so scaling only the category axis
mechanically drives sep_cat↑ and sep_a↓ even with a/distractor fully intact (reference: at sep_cat≈0.73 an
information-preserving embedding gives sep_a≈0.47; **observed 0.512 is ABOVE that ⇒ no member-info loss**). The earlier
"certified conversions are already collapsing" observation is **STRUCK — unsupported.** *(Lesson: verify a metric's
additivity before drawing an inference from it — as with the l_spread-direction error, an untraced instrument
assumption was backwards.)*
**STAGE 0c — content NOT stored per window** (checked: no per-window content/emission tensor in the committed records;
only derived `sep_*` scalars). So the decodability guard **cannot be cut from committed data → it FOLDS INTO STAGE 1.**
The RESCUE-BY-COLLAPSE threshold is cut from **Stage 1's α=0.1 dec baseline** — still blind, in-regime, before any
α≠0.1 data exists.

## §3 — STAGE 1 — instrumented cal run  [AMENDED: instrumentation, NOT a decision point]
**Purpose:** characterize the two-force balance descriptively. **No halt gate on any magnitude ratio; Stage 2 runs
regardless** (BLOCKER B — the seat's "≥2 orders" threshold is struck: ungrounded, and raw norm is the wrong measure —
a large gradient *orthogonal* to the category axis is inert regardless of magnitude. A kill on an ungrounded constant
is worse than no kill; Jason is not compute-limited).

**Executor (BLOCKER A — stated before ratification).** A single `L.backward()` yields only the resultant `∇_vis L`;
separating the two terms needs `autograd.grad` per term. Mechanism = the committed precedents, composed:
`torch.autograd.grad(term, vis_params, allow_unused=True)` on each of `gain·l_pam` and `α·l_spread`
(pattern: `grad_geometry_split`, exp12_arms.py:343–358), the whole diagnostic wrapped in the `X9._rng_guard`
save/restore (pattern: `grad_decomp_local`, exp12_arms.py:361–365, "RNG-free (asserted)"), and run **after** `opt.step()`.
- **Bit-exactness — preserved BY CONSTRUCTION:** the pass runs after the optimizer step; `autograd.grad` returns grads
  **without populating `.grad`** (which is all `opt.step()` reads); and the `_rng_guard` saves the RNG state before and
  restores it after, so the diagnostic's draws are rolled back and the next training step is bit-identical. The training
  trajectory is untouched. (Consequence of the guard: the diagnostic re-draws `l_spread`'s P projections, so
  `‖∇_vis(α·l_spread)‖` is a **re-sampled estimate**, not the bit-identical in-`L` gradient — acceptable because §3 is
  descriptive, not a gate.)
- **REUSED-class pre-check — the ONLY hard fence in Stage 1:** the instrumented build must reproduce committed
  `exp12_dwell`/`exp12_shuffle` **bit-exactly** at α=0.1 (provenance computed, never asserted). Divergence = instrument
  regression = **HALT → Jason**, and the build is re-spec'd as a **parallel diagnostic, explicitly NOT REUSED-certified**
  — not forced.
- **Positive-delta smoke IDs (CORRIDOR_PROTOCOL — an executor without a smoke-tested positive-delta assert is a
  pre-flight blocker):**
  - `SMOKE-GRADSPLIT-POS` — the two separated norms are finite, non-negative, and **not identical** (the split actually
    separates the terms: nonzero delta); and at α=0, `‖∇_vis(α·l_spread)‖ == 0`.
  - `SMOKE-REUSED` — instrumented α=0.1 reproduces committed `exp12_dwell`/`exp12_shuffle` bit-exactly.

**Logged per eval window (all read-only, RNG-neutral; all from the SAME content tensor `_sep_ratio` already consumes,
exp12_arms.py:659–661 — a pure scorer add, no new forward pass, no RNG draw):**
- `l_pam`, `l_spread`, `gain`; the two gradient norms;
- the emission covariance spectrum + `effective_rank` of the 16 clean probes (`spread.covariance_spectrum`/`effective_rank`,
  `@torch.no_grad()`) — **DESCRIPTIVE ONLY, not a gate** (AMENDMENT 5: a "rank → 1–2" criterion fires on an *intact*
  representation — the disentangled reference gives eff_rank 1.79 at matched sep_cat vs 1.02 collapsed; rank cannot carry
  the discriminator);
- **the DECODABILITY guard (AMENDMENT 6 — the load-bearing discriminator; STAGE 0c folded in):** `dec_a` = leave-one-out
  nearest-centroid accuracy for `ma` (4-way, chance 0.25), `dec_dist` = same for `mb // n_category` (2-way, chance 0.50),
  `dec_cat` for symmetry. **Scale-invariant** ⇒ boosting the category axis cannot move it; intact → high, collapsed → chance.

**Run (BLOCKER C re-spec):** α=0.1, **8 seeds × {dwell, shuffle}, read_at = 500k — 16 runs.** NOT cal-seeds/short-horizon:
the dec baseline requires a *real conversion*, which exists only in the SHUFFLE arm and only at full horizon (verified
converter first-episode onsets {19.2k, 72.3k, 91.8k, 106.2k, **427.5k**}, max 427.5k — a short horizon misses the late
converters. *Provenance note: the seat's "median 161k" did not reproduce — first-episode median 91.8k, `conversion_onset_
PROPOSED` median 7.8k; the max 427.5k is confirmed and is what sets read_at=500k.*)
- **shuffle** → REUSED fence (**must reproduce 5/8**, converters {0,2,4,5,6}) · the `dec_a`/`dec_dist` **converter
  baseline** · the tug-of-war signature.
- **dwell** → REUSED fence (**0/8**) · the dead-arm gradient balance · spectrum / `effective_rank`.

**Threshold recipe — fixed now, cut blind (no free constant):**
- **RESCUE-BY-COLLAPSE iff `dec_a` → chance (0.25) / `dec_dist` → 0.50** (absolute floor).
- **RESCUE requires the α↓ arm's during-episode `dec_a` to fall WITHIN the range spanned by the 5 shuffled α=0.1
  converters** (in-regime band). Both cut from this Stage-1 α=0.1 run, blind, before any α≠0.1 arm exists.

**Reported descriptively (no gate, Stage 2 proceeds regardless):**
1. the two gradient norms — **with the orthogonality caveat** (raw norm ≠ category-relevant force);
2. spectrum + `effective_rank` — interpretive only (FOR: flat/eff-rank≈16 penalty shapes the cortex · AGAINST:
   uneven/eff-rank<16 structure not category);
3. two tug-of-war signatures — `∇_vis(α·l_spread)` non-trivial between episodes? · `‖∇_vis(gain·l_pam)‖` falls when the
   exam is passing?

## §4 — STAGE 2 — the α-sweep  [proceeds once Stage 1's REUSED bit-exact fence passes; Stage 0 + Stage-1 balance are descriptive, not gates] [AMENDED]
**Manipulation:** `alpha_spread` only. No new code path, no loss term, no optimizer change. `read_at = 500_000`,
everything else inherited unchanged.
- **DWELL fabric (rescue side):** α ∈ **{0, 0.01}**, 8 seeds each = **16 runs**, fabric = certified-dead `exp12_dwell`.
  **α = 0.1 dwell is NOT re-run** — committed reference; must reduce **bit-exactly** to `exp12_dwell` (0/8). Reachable
  falsifier / **Stage-1 pre-check**, not a paid arm.
- **SHUFFLED fabric — α ∈ {0, 0.3}, 8 seeds each = 16 runs**, fabric = `exp12_shuffle`:
  - **α = 0.3 (harm side, AMENDMENT 2):** the only cell with dynamic range (5/8 CAN fall), immune to RESCUE-BY-COLLAPSE
    (higher α ⇒ less collapse), the only cell where the hypothesis predicts HARM. Named blind (§6): texture moves first.
  - **α = 0 (viability control, BLOCKER E):** without it a dwell-α=0 null is uninterpretable — "nothing converts" and
    "α=0 is broken" are indistinguishable. α=0 collapsing on shuffle but NOT dwell is itself a mechanism finding.
  - **α = 0.1 shuffle** = the **Stage-1 instrumented reference** (5/8, REUSED-fenced to the committed run); not a Stage-2 arm.
- *(The α=0.3-DWELL bank is DROPPED — Jason's ruling: on a floored 0/8 arm α↑ has no reachable falsifier on the primary,
  and its only content (representation dose-response) is already spanned by Stage 1 (α=0.1) + Stage 2 (α∈{0,0.01}).)*

**Paid total (Stage 2): dwell {0, 0.01}×8 = 16 + shuffle {0, 0.3}×8 = 16 → 32 runs @ 500k.**

**Draw-neutrality — VERIFIED property (loop.py:200–218):** `l_spread = self._l_spread(self.gen)` is called
**unconditionally** (loop.py:213); `alpha_spread` only *multiplies* it in `L` (loop.py:218). So `_l_spread`'s RNG
consumption (the a/b draws, `stim.raw`, and `spread_loss`'s P projections) is **identical at every α, including α=0**.
⇒ each α sees the **bit-identical stimulus stream and generator trajectory**; α is a pure loss-coefficient change. The
α-ladder is draw-matched by construction (no RNG confound between α cells).

## §5 — THE TRAP and the guard (mandatory; without it Stage 2 is uninterpretable)
At α=0 the completion loss has a **degenerate optimum:** vision collapses onto the frozen word vectors ⇒ PAM's
word↔vision completion is trivially perfect ⇒ exam_acc→1.0 AND sep_cat→1.0 (two tight per-category clusters). This is
the **manufactured RESCUE signature** — exactly the dimensional collapse `l_spread` exists to prevent; removing it makes
collapse the cheapest descent. **Burden-reversal fires.**
**The guard is ARCHITECTURAL, not a judgment call — DECODABILITY, not separation (AMENDMENT 5+6). Log per window
(pure scorer add on the content tensor exp12_arms.py:659–661; no new forward, no RNG, no bit-exactness risk):**
- **`dec_a`** — leave-one-out nearest-centroid accuracy for `ma` (4-way, **chance 0.25**).
- **`dec_dist`** — same for `mb // n_category` (2-way, **chance 0.50**).
- **`dec_cat`** — for symmetry.
**Scale-invariant** — boosting the category axis cannot move it (this is the defect that killed the sep-ratio prong;
STAGE 0b's "collapse" was a `_sep_ratio` non-additivity artifact, §2b). **Intact member info → dec high; collapse-onto-
label → dec at chance.**
**STRUCK:** the `sep_a`/`sep_dist`/`sep_member` separation prong (metric artifact, §2b) AND `effective_rank` as a *gate*
(it fires "rank → 1–2" on an intact rep — 1.79 intact vs 1.02 collapsed; retained descriptive only, §3).
**Threshold — calibrate-in-regime (STAGE 0c folded into Stage 1):** cut RESCUE-BY-COLLAPSE from the **α=0.1 converter
`dec_a`/`dec_dist` baseline** measured in Stage 1, blind, before any α≠0.1 arm.

## §6 — OUTCOME CELLS  [named blind, before any α≠0.1 data exists]
| cell | condition | reading |
|---|---|---|
| **RESCUE** | dwelled converts at α↓, **`dec_a` and `dec_dist` hold at the α=0.1 converter baseline** | the block is the regularizer, not ordering. Coherent experience back on the table. |
| **RESCUE-BY-COLLAPSE** (wrong-reason) | dwelled "converts" but **`dec_a` → 0.25 / `dec_dist` → 0.50** (member information destroyed, not merely de-prioritised) | manufactured — vision collapsed onto the label. NOT a conversion. Named now so it cannot be argued away later. |
| **COLLAPSE** | representation degenerates, exam does not rise | the term is load-bearing; the tension is real ⇒ design problem becomes *anti-collapse without isotropy*. |
| **INERT** (dwell) | no α-dependence on the dwell side | SPREAD-IS-ERASER refuted; the ordering framing survives intact. |

**Shuffle α=0.3 (harm side) — named blind:**
| cell | condition | reading |
|---|---|---|
| **SPREAD-HARMS** | **texture moves FIRST** — episode count & duration fall *before* converter count | the penalty actively suppresses conversion; SPREAD-IS-ERASER's harm prediction confirmed (this cell is immune to RESCUE-BY-COLLAPSE). |
| **INERT-SHUFFLE** | 5/8 AND episode structure unchanged | no α-dependence on the shuffle side ⇒ SPREAD-IS-ERASER weakened. |

**α=0 viability control (BLOCKER E):**
| cell | condition | reading |
|---|---|---|
| **VIABLE-α0** | shuffle α=0 still converts (≈5/8) | α=0 is a valid regime ⇒ a dwell-α=0 null is a REAL null, not a broken run. |
| **BROKEN-α0** | shuffle α=0 collapses (converters fall) | removing the isotropy floor breaks the shuffle arm too. **OVERRIDE (RULING-CLASS): BROKEN-α0 supersedes the dwell-α=0 cell entirely — the dwelled α=0 result is uninterpretable and MUST NOT be read at all.** "Collapse on shuffle but not dwell" is itself a mechanism finding. Route to Jason. |

**The 2×2 TERMINAL reading (BLOCKER D closed — seat's verbatim four cells. dwell α↓ RESCUES/INERT × shuffle α↑
HARMS/INERT; "dwell RESCUES" = the decodability-validated RESCUE, not RESCUE-BY-COLLAPSE):**
| | **shuffle α↑ HARMS** | **shuffle α↑ INERT** |
|---|---|---|
| **dwell α↓ RESCUES** | **SPREAD-IS-GATE** — both directions confirm; the isotropy penalty IS the block, and ordering is a proxy for the teacher's strength against it. Coherent experience is back on the table. | **ASYMMETRIC** — rescue without harm. Either dose-saturation (α=0.1 already saturates the antagonist: ↑ does nothing, ↓ does) OR a genuine fabric interaction. → conditional escalation α=1.0 shuffle to separate them. **(exactly this cell — the "α=0 breaks one fabric" reading is BROKEN-α0's, NOT here.)** |
| **dwell α↓ INERT** | **ANTAGONIST-INSUFFICIENT** — α is a real antagonist (it demonstrably costs conversion) but reducing it does NOT free the dwelled arm. **Both forces are live and roughly ADDITIVE: spread is one block, ordering is another.** Neither the flattering nor the null result. Route to Jason. | **INERT** — SPREAD-IS-ERASER refuted. The ordering framing survives intact; PART 3 proceeds unmodified. |

**ASYMMETRIC escalation — pre-priced & pre-named NOW (arms are priced when they open, not inherited from banked prose):**
α = **1.0**, **shuffle**, **8 seeds = +8 runs @ 500k**. **Trigger:** terminal outcome = ASYMMETRIC. Separates
dose-saturation (α=1.0 still no harm) from fabric-interaction (α=1.0 harms). Banked, not built.

## §7 — Standing requirements
- **Calibrate-in-regime.** Every α is a new regime. Cut every constant fresh. **Surface the band-cutting recipe BEFORE
  the verdict arms — do NOT inherit EXP14's band (0.64/0.6875).** Any cross-α claim (including prose) comes from a
  `matched_bar_tab` call.
- **Halt fences:** REUSED-class pre-check divergence · any value outside a pre-named envelope · any outcome in no named
  route · anything for which the honest next sentence is "I recommend…".
- **Compute.** **Stage 1 = 16 runs @ 500k** (α=0.1, 8 seeds × {dwell, shuffle}) + **Stage 2 = 32 runs @ 500k**
  (dwell {0, 0.01}×8 + shuffle {0, 0.3}×8) = **48 runs @ 500k** on Equinox, **+ 8 banked** (ASYMMETRIC escalation
  α=1.0 shuffle, pre-priced) = **48 committed / 56 if escalated**. **Price against EXP19's queue; surface the contention
  to Jason — do NOT self-schedule.** Stage 1 is no longer a cheap short-horizon cal (BLOCKER C: the dec baseline needs a
  full-horizon conversion); it establishes the REUSED fences + the dec baseline + the balance instrumentation before any
  α≠0.1 arm.
- **Checkpoint every run** at horizon + any pre-registered event (standing contract).

## §8 — Held / routed (not part of this arm's execution)
- **PART 3 M2/M3 — HELD.** Add **α as the third knob: α moves B\* ⇒ M1** (the representation-level candidate).
- **Baseline contrast** — deferred.
- **SCATTER acq-guard canon correction** — Jason's, still owed (mis-anchored `sep_cat=0.4733`).
- **Ledger 39 — misdirected:** the ISOTROPY-BALANCE hypothesis is the SEAT's, not CC's. Route to Jason for amendment.
- **BANKED — the t2 / unpool-rate sweep** (t2 ∈ {1200,50k,200k,500k}, repool_rate=0, AdaptiveRepool off). Trigger:
  after ISOTROPY-BALANCE terminals. The earlier "longer pooling → less flicker" prediction is **WITHDRAWN** (the tie
  acts on weights, isotropy on the emission covariance; their interaction is unanalyzed). Do not draft.
- **TEACHER-IS-ERASER** — withdrawn (R11), not routed.
