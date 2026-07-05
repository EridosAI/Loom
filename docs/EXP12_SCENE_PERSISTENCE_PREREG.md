# EXP12 — Scene persistence: the minimal temporal fabric (the task-degeneracy discriminator)

**STATUS: RATIFIED FOR BUILD (2026-07-04). Checkpoint read complete; Amendments A/B +
the B1/B2 propagations applied and confirmed; §13 constants RATIFIED with Adjustments
1–2 and the margin guard. Arms do not run until the stage-two calibration constants are
recorded (§13.4–5). This prereg is an ASSEMBLY of the fork rulings, not new design;
where an item was slotted without an explicit fork ruling it is marked [SLOTTED] and
surfaces at the checkpoint read. The static line is retired (FRONTIER §10.18); gate steps
5–6 are retired with it — the teaching test re-poses here at its own gates (§9, 12b). No
arm is a fix.**

**The question, stated once: does dwell persistence break the i.i.d. task degeneracy —
does member-conditional routing survive under dwells and die under shuffled dwells?** This
is the direct test of the wrap's manufactured-root hypothesis (FRONTIER §10.18, tagged
COHERENT-DEDUCED-NOT-DEMONSTRATED): i.i.d. draws make the deck-average nearly optimal,
starving member-conditional routing by construction. Persistence is the minimal departure
from i.i.d. that the architecture was conceived for.

**v1 SCOPE, binding:** wave-local completion (no trace machinery), so v1 tests
**persistence-as-gradient-ordering ONLY** — dwelled and shuffled arms differ in nothing
but exposure order. **A v1 null is NOT fabric-refutation**; its concrete escalation is the
visibility rung (§8). Do not read past this scope.

---

## 0. The discipline traps (binding, carried from the handoff + Guiding_List)

- **Anti-forward guard.** PAM learns by non-causal masked completion over co-present
  structure. Dwell evolution is *context for completion*, **never a forecasting target**;
  the moment any component acquires a next-step objective, it is the ~10-restart drift,
  whatever it is called.
- **Time is felt, not coded** (Guiding_List, promoted entry, named for EXP12
  specifically). Order and duration enter through dynamics only — no timestamps, no dwell
  indices, no boundary flags as coded signal. Guaranteed onset masking passes this test:
  it is harness-side scheduling policy, not a signal channel.
- **World-building must not smuggle the answer.** Any persistence structure correlated
  with identity is leakage. The independence asserts extend into the time axis (§5).
- **Do not import static-line conclusions.** Carry the screens (detach-null comparator,
  stop-grad-in-costume test, wrong-reason taxonomy, calibrate-in-regime), not the
  outcomes.

## 1. The fabric (v1 world) — Fork 1 as resolved + amended

- **Continual time from t=0. All vectors, no images** (confirmed). Attention/foveation
  via evocations = salience-as-consequence, future work, out of scope.
- **Background recurrence (Fork 1 amendment):** onset poses come from a persistent
  configuration, not fresh family draws. **v1 = ONE fixed background configuration
  (pin-to-constant) + OU jitter around it**; the background library is a later rung.
  Grounds on record: familiarity must be *earnable*, not just family-robustness; a learned
  background concentrates completion gradient on the member component.
- **Within-dwell evolution = stochastic jitter (walk-law-only resolution):** member
  nuisance/pose drawn at dwell onset from the family marginal, then evolves by bounded
  OU-style random steps around the onset pose. One fixed walk law; **all hyperparameters
  global across members**; increments stochastic.
- **Struck overclaim, on the record (do not re-import):** "cheapest good completion at
  all lags is knowing the member" is FALSE — clause 2 (nuisance ⟂ identity) forbids
  member knowledge improving nuisance completion, and identity-copy from any visible
  same-dwell neighbor is free under every walk law. Routing demand therefore lives in
  **mask geometry + dwell-onset rate** (§3), not in the walk law.
- **Named control: i.i.d.-refresh = the coherence-ablation arm** (member persists,
  nuisance fresh each wave — persistence without coherence). Named, banked; isolates
  identity-persistence from nuisance-coherence if fired. RATIFIED (checkpoint read):
  trigger = post-promote — attributes which component of a working fabric did the work;
  characterization, never verdict.
- **Canon language (correction, carried):** the familiar background earns **LOW**
  prediction error — that is *why* it is ignorable; the new object is the
  **high-divergence residual**.
- **Binding:** background ⟂ member. Context–identity correlation is leakage *here*;
  real-world context correlation is deferred to a later regime, on the record.

## 2. The dwell-length law — Fork 2 as resolved + pinned

- **k = k_min + Geom(p), capped at k_max.** Constant hazard in the bulk: dwell age
  carries no information about when the dwell ends — the only clockless law. Fixed-k
  (deterministic period) and bounded-uniform (rising hazard = soft clock) are EXCLUDED on
  pin clause 1 extended to the time axis.
- **k_min = 2, pinned as default** (Jason's pin 1: the floor is itself a mini-clock —
  hazard-zero waves are a known safe window; at k_min=2 it is trivial, "no back-to-back
  exams"). Any increase requires recorded grounds.
- **Role-eligibility correction (on the record):** k_min=2 guarantees ≥1 *mid-dwell wave*
  per dwell — role-eligibility, NOT a guaranteed teaching wave; whether it teaches
  arrives at the mask-mix rate (§3). Matters only in the k=2 tail.
- **Cap-hit ceiling ASSERT (pin 2), not just a manifest line:** cap-hit rate <
  `[RECONCILE: ~1%]`. Cap-hits are the one place boundary timing becomes certain; breach
  = re-pin k_max, **surfaced, before any run consumes it**.
- **Fork-1/Fork-2 coupling, ordering pinned (pin 3):** OU decorrelation time τ and E[k]
  are not independent. τ ≪ dwell → jitter ≈ i.i.d. refresh (coherence-ablation control
  loses its contrast); τ ≫ dwell → near-frozen poses (copy-shortcut shape returns;
  familiarity trivial). **Binding relation: a few waves < τ < E[k].** Numbers at
  checkpoint (§13.1–2); the ordering is pinned here.
- **Member draw: uniform with NO immediate same-member repeat** (Fork 1.5 constraint,
  ratified — else the prior dwell contaminates the onset exam via recency). Stationary
  marginal stays uniform by symmetry.
- **New binding assert — k ⟂ member**, numerically at manifest: if any member dwells
  systematically longer, duration codes identity (clause 2 extended into time; "same coin
  for elephants and mice").

## 3. Completion geometry & the division of labor — Fork 1.5 as resolved + sharpened

- **(a) Wave-local completion.** The completer sees only the current wave [vision ;
  word-anchor slot]. **No trace machinery in v1** — the across-wave mechanism is
  mechanism-map open question #1 (unified vs split) and is not settled by rig
  construction. The dictionary is already the across-experience memory. This also keeps
  the shuffled-dwell discriminator **single-channel**: arms differ only in gradient
  ordering. **RECORDED GUARD (from build): W = 1 idles the deployed loss's
  next-wave-prediction term by construction — the anti-forward guard enforced
  structurally. Any future W > 1 rung must re-justify that term explicitly against
  trap #1 before it returns.**
- **(b) Guaranteed onset exam.** Every dwell's FIRST wave: **associate/word slot masked,
  vision visible.** No recent exposure helps; route-and-recall through the dictionary is
  the only completion path. Onset rate = the routing-gradient dial (set by Fork 2's E[k]).
  At rig-1 topology (v2) the exam pays exactly the category partition — the §10
  geometry pin.
- **Division of labor, pre-registered (sharpening 2 — two roles, two reads):**
  - **Onset waves = ROUTING EXAMS** (vision → association recall). **The verdict axis.**
  - **Mid-dwell vision-masked waves = THE TEACHING CHANNEL** (word → vision gradient) —
    where acquisition and any sculpting happen. Recency-inflated on completion; **never a
    routing pass**.
  - **Mid-dwell word-masked waves** = recency-inflated companion panel only.
  - **Onset completion is never teaching evidence; mid-dwell completion is never routing
    evidence.**
- **Mid-dwell mask mix (vision:word ratio) = checkpoint pin, default symmetric** —
  fenced against post-hoc tuning like any knob (§13.3).
- **Onset reads are acquisition-aligned (sharpening 3; standing rule applies).** Early
  dwells fail the exam trivially — nothing acquired yet. Pre-acquisition onset error IS
  the acquisition curve; **routing verdicts start post-onset** per the aligned-read
  machinery. Otherwise early-run reads manufacture a false routing-dead.
- **Mask schedule:** harness-side, deterministic-to-harness (replay contract), on its own
  seeded substream. It leaks *boundary*, never *identity* — **schedule ⟂ member assert**
  (§5). **Fallback (c) BANKED:** probabilistic-elevated onset masking, fired only if
  boundary-cue exploitation is observed (§13.10 defines the monitor).
- **Wrong-reason outcome, pre-registered:** completion-good / routing-dead =
  **shortcut-through-recency** (the wave-local analog of shortcut-through-trace) — a
  named finding, never a pass. The onset/mid-dwell split is its discriminating read: the
  exam wave has no recency channel.

## 4. The unpredictability pin — three clauses, extended into time

1. **Unpredictable as a sequence** — within-dwell via stochastic OU increments; across
   dwells via unpredictable member draws and Geom(p) endings. No cycles, no schedules.
2. **Uninformative about identity** — nuisance ⟂ member ⟂ word ⟂ category, asserted
   numerically at Step-0/manifest, **now per-lag** (§5).
3. **Learnable as a distribution** — one fixed walk law + one fixed background +
   Geom(p): predictable at the family level, never at the instance level.

## 5. Independence asserts (numeric, manifest-time) — the extended set

- Per-lag nuisance ⟂ member (walk statistics carry zero identity at every lag).
- **k ⟂ member** (§2).
- **Mask schedule ⟂ member** (§3).
- Background ⟂ member (§1).
- Substream separation: dedicated seeded streams for {nuisance/jitter, dwell-length,
  member-draw, mask-schedule} — never `loop.gen`, never probe generators; substream keys
  recorded (EXP10 §3 discipline, extended). RATIFIED (checkpoint read): mechanical.

## 6. Arms — rig-1 (the four-cell campaign)

- **A-DWELL:** the fabric as §1–3. Word-present, deployed topology.
- **A-SHUFFLE:** the IDENTICAL waves **and the IDENTICAL mask schedule, order-shuffled**
  (construction pin, ratified) — destroys dwell contiguity and nothing else. Same exams,
  different order; otherwise the table confounds exam rate with persistence.
- **Anchor coverage in rig-1: RATIFIED (checkpoint read) — deployed topology (v2).**
  Keeps the four-cell campaign single-question and static-comparable; the coverage
  question re-poses via the banked ladder, §9.
- Corollary on record: BOTH-SURVIVE attributes to variation + exam-scheduling *jointly*
  (shuffle removes only persistence); the **splitting arm (shuffled + uniform masking)**
  is banked, fires only on that cell.

## 7. The four-cell inference table (pre-registered; all cells named before the run)

| dwelled | shuffled | reading | route |
|---|---|---|---|
| survives | dies | **PROMOTE the root** — task degeneracy demonstrated as the collapse's cause | opens 12b full-seeds (teaching test) + baseline generality leg (§9) |
| survives | survives | variation + exam-scheduling jointly suffice (reads with EXP10's variation thread) | splitting arm (shuffled + uniform masking) fires to attribute |
| dies | dies | **ordering alone insufficient** — NOT root-refutation (v1 scope) | the §8 escalation ladder |
| dies | survives | **ANOMALY** — recency-cramming outcompeting routing, or instrument artifact | Fork 1.5 geometry audit + recency-channel check; **named finding only, never interpreted beyond this routing** |

"Survives" = the §10 **category-partition** survival criterion at registered constants (§13.5);
per-cell boundaries are stated numerically at checkpoint, not at read time.

## 8. The both-die escalation ladder (ordered; outranking BINDING)

**baseline → 12b → visibility rung.** World-untrainable moots word-attribution, which
moots escalation. **Parallel-fire baseline + 12b (both reduced-seed, both cheap); read on
the ladder order.**

1. **Baseline fails too** → world-broken: fix the classroom (fabric/constants), not the
   learner. Stops the ladder.
2. **Baseline trains; 12b no-word-dwelled SURVIVES** → **word re-kills on live fabric** —
   a pre-named falsifier of the §9 contrast registration; MAJOR finding, redesign input.
   Does NOT open the visibility rung (wrong culprit).
3. **Baseline trains; 12b no-word-dwelled DIES** → fabric-insufficient at the
   gradient-ordering rung → **the visibility rung opens** ((b)-style trace fabric as the
   next arm), arriving PRE-INSTRUMENTED: trace-span < dwell-span constraint + the
   trace-blinded read, banked now.

## 9. Banked arms & registered predictions (triggers pre-named)

- **12b — the no-word comparator (Fork 3, two openers).** Construction pin:
  **absent-word, NOT scrambled-word** (the static line's own comparator form). Openers:
  **(i) the promote cell** — full seeds, the teaching test at its own gates; **(ii) the
  both-die cell** — reduced seeds, as the §8 discriminator. Same arm, same construction,
  two pre-registered triggers; epistemically closed either way.
  - **REGISTERED PREDICTION (cross-scene contrast):** word-present differentiates
    word-tied axes FASTER than no-word, on identical fabric/seeds/schedule. Measure =
    acquisition-aligned differentiation **lift** on word-tied axes (lift, never share).
    **The registration's edge:** the same channel that was a ~5× *collapse* accelerant in
    the degenerate task is predicted to accelerate *differentiation* in the live one —
    same channel, opposite sign, regime-discriminating.
  - **Falsifiers, pre-named:** (a) word re-accelerates collapse on live fabric
    (fate-shared, recurring); (b) no contrast (channel inert on healthy fabric).
- **Baseline — the conventional trainability control (Fork 4, two openers).** Standard
  masked-completion learner, V-JEPA-class `[RECONCILE: family/impl]`; **identical
  manifests + identical mask schedule** (same exams, same order — the shuffled-control
  construction discipline); param scale `[RECONCILE]`. Openers: **(i) both-die** —
  trainability discriminator (§8); **(ii) the promote cell** — generality leg, reduced
  seeds, **context not gate**.
  - **Its own pre-registered bars (Jason pin 1 — the matched-bar lesson, out-of-family
    edition):** the learner has NO assignment map; its collapse read is its own. Form
    registered now, constants at checkpoint (§13.6):
    **(B1) latent CATEGORY-separability** (geometry-matched per the §10 pin —
    PROPAGATION, flagged for confirm: the baseline runs the same task, so the same
    structure is paid): windowed between-category/within-category separation ratio in
    its representation space, in-regime calibrated floor; member-separability rides as
    companion; "mean-collapse" = separability → floor while outputs → category-/deck-mean.
    **(B2) onset-exam analog lift** — associate-slot completion on onset waves vs the
    CATEGORY-PRIOR floor (symmetric completion: lift over deck-mean IS category-lift at
    v2), acquisition-aligned. "Differentiates on dwelled / mean-collapses
    on shuffled" is scored on (B1)+(B2), never on PAM's asg machinery.
  - **Generality read is ONE-DIRECTIONAL (Jason pin 2):** baseline-also-differentiates →
    the root generalizes (task property). Baseline-fails-where-PAM-passed → **context
    only, NEVER a PAM-superiority claim** — param-scale and family confounds are
    unresolved by construction. The flattering direction is fenced before any result
    exists.
  - **The fence, binding:** shares stimulus + objective family ONLY — no shared
    components, no design flowback; baseline reads are trainability context, never PAM
    bars. **Thermometer, not donor.**
- **Anchor-coverage ladder:** the banked EXP11 clean-redo design VERBATIM (uniform
  matched-min-separation or D-scaling control; fixed common post-onset window; ≥ the seed
  floor; the loose-thread disambiguation arm). Trigger RATIFIED (checkpoint read) = the
  promote cell — coverage is measurable only on living routing. Role SHARPENED by the
  §10 geometry pin: member-level routing becomes payable only as vocabulary rises —
  **16-way survival is the LADDER's question, never rig-1's.**
- **Splitting arm** (shuffled + uniform masking): trigger = both-survive (§6).
- **Coherence-ablation arm** (i.i.d.-refresh): trigger proposed post-promote (§1).
- **Curriculum arm (background-alone-first = existing Δt_offset staging):** PARKED,
  cheap later arm, not in the minimal rig. Its observable is NOT curriculum-gated — it
  rides in rig-1 (§10, Amendment A).

## 10. Readouts + criteria + instruments (the arsenal carries whole)

- **THE SURVIVAL-READ GEOMETRY PIN (Amendment B — pinned here, not deferred to §13.5):
  the verdict is geometry-matched to what the task PAYS at rig topology.** At v2,
  wave-local: vision-masked waves give the completer no member cue (word = category
  only, background ⟂ member, no trace) — category-mean is optimal by construction, so
  no gradient ever pays 16-way routing; onset exams pay exactly 2-way. **VERDICT AXIS =
  category-partition input-sensitivity** — asg_dist read between category-conditioned
  inputs (windowed; form registered here, constants §13.5). **16-member asg_dist rides
  as companion/characterization ONLY.** A 16-member survival bar would demand unpaid
  structure and manufacture a wrong-reason both-die — the matched-bar lesson, surfaced
  before the run instead of after it.
- **Primary VERDICT read: category-partition asg_dist at aligned windows** — AMENDED IN
  PLACE (Ruling 2, cross-reviewed; forced by Amendment B — the pre-amendment line named
  onset-exam completion). **Onset-exam completion LIFT = registered COMPANION**, never
  the cell-decider: a flat exam must not manufacture both-die through the completion
  side. Both acquisition-aligned, per-rung, windowed estimators with pinned forms (no
  selectable sub-windows). In-regime TWO-STAGE calibration (calibration seeds ≠ verdict
  seeds; constants from EXP12's own healthy spans — never static-line constants: §10.14
  lesson).
- **REGISTERED FINDING CLASS (pre-verdict): sensitivity-without-conversion** — asg
  alive, exam at floor. Mechanism: the exam channel is PAID but UNCONVERTED-AT-HORIZON,
  not unpaid. The dissociation is its own observable: num-floor onset vs
  exam-conversion onset (the transferred 0.01 floor demonstrably fires without
  functional conversion — the gap is data); the companion aligns to the exam's own
  onset if one appears. Named finding, never a survives-downgrade; no loss-reweighting
  to force conversion (manufacturing-class).
- **Routing-survival quantity: category-partition asg_dist** (per the pin above),
  matched post-onset windows; 16-member asg_dist / asg_argmax_k / asg_entropy as
  companions; **den = one-sided collapse-floor tripwire ONLY** (variance never certifies
  differentiation).
- **Earned-salience observable (Amendment A — a rig-1 readout; free: the divergence
  columns exist and the fixed background gives exposure from wave 0). Expectation, NOT a
  gate:** PAM divergence on background axes FALLS with exposure while member-onset
  divergence STAYS HIGH.
- **Standing panels:** dynamics panels (mean, amplitude, dominant period, trend) for
  every scalar criterion; **per-dwell-position curves** (onset vs mid-dwell — the natural
  EXP12 panel); decomposition columns (grad + evo); pin-depth; occupancy; masking-mix;
  manifests re-cut live-derived; illustrative scatter per arm.
- **Wrong-reason taxonomy carried + extended:** shortcut-through-recency (§3, named
  finding never pass) · boundary-cue exploitation (→ fallback (c)) · identity-through-
  dynamics leakage (blocked by §5 asserts) · acquisition-censored (unread, never a null).
- **Bar and read are the same function on matched geometry — including the time axis**
  (per-seed, per-arm criterion alignment).
- **Lift, never share.** Teaching-adjacent quantities are always lifts against a
  registered floor.
- **Verification pass before any verdict reaches the table** (standing; it flipped a
  surprising draft verdict in EXP08, EXP10, and EXP11).

## 11. Determinism & replay

Seed + construction order + torch threads = 1, thread count recorded in every artifact.
Dedicated seeded substreams per §5. Unpredictable to the system, deterministic to the
harness.

## 12. Scope fences (what EXP12-v1 does NOT test)

Teaching in rig-1 (gated at 12b's own gates) · the coverage ladder unless triggered ·
curriculum (parked, observable registered) · foveation / salience-as-consequence ·
real-world context–identity correlation (deferred) · the background library ·
within-bundle variable confidence (deferred regime) · external objectives (later phase).
No arm is a fix.

## 13. Checkpoint constants — RATIFIED (Jason, 2026-07-04)

1. **Walk:** the EXP10 pinned nuisance family VERBATIM [CC verifies values]; per-axis OU
   reverting to the onset pose; **STATIONARY-SPREAD PIN (Adjustment 2): OU stationary sd
   = 0.25·family-σ** — per-step σ derived by CC from τ, never pinned directly, else the
   equilibrium wander can exceed the family marginal and clause-3 quietly breaks.
   **τ = 4 waves.** Ordering verified: ~2 < 4 < 12.
2. **Dwell — AMENDED IN PLACE (Ruling 1, cross-reviewed):** k = 2 + Geom₀(p = 0.1),
   support {2..48} (E[k] = 11; cap-hit ≈ 0.7%, ceiling assert 1%); k_min = 2 realizable.
   The as-ratified arithmetic embedded a support error making k = 2 unreachable; the
   pin's grounds (floor-3 = first non-trivial hazard-zero window) outrank the constants'
   letter. Ordering re-verified: 2 < 4 < 11.
3. **Mask:** one slot masked per wave; mid-dwell coin 50:50.
4. **Onset criterion:** EXP10 num-floor onset carried (num ≥ 0.01, 2 consecutive
   windows) [CC verifies transfer]; category-prior floor; W_post ≥ 3 collapse periods in
   EXP12's own regime, per-arm at stage-two. **W_POST FALLBACK (pre-registered — the
   EXP11 estimator caveat going live on schedule): where an arm's own regime shows no
   collapse cycle, W_post = a fixed absolute-wave window recorded from that arm's
   stage-two calibration. Precedence ladder (own collapse period → fixed calibrated
   window) recorded before any verdict, never improvised at estimator fallback.** The
   common-ruler alternative (borrowing the collapsing arm's period) is rejected: it has
   no answer in the both-survive cell. **SIZING PIN: the fixed fallback window ≥ the max
   measured in-regime period, so no-cycle / present-unmeasured arms are never
   under-covered; recorded at stage-two.**
5. **Survival:** category-partition asg_dist ≥ the stage-two calibrated threshold over
   matched W_post; cell verdict = seed majority ≥ 3/5. **MARGIN GUARD: any arm at a 3–2
   seed split fires its +2 extension BEFORE the table is interpreted** (encodes the
   3/5–3/5 / 3/5–2/5 adjacent-cell rule; prevents a coin-flip table). Threshold + cell
   boundaries recorded pre-run at stage-two, never at read. **CENSORED-SEED ACCOUNTING:
   a verdict seed unacquired at horizon = UNREAD (taxonomy), never a dies; the
   margin-guard +2 extension fires on read-count shortfall BEFORE any table
   interpretation** (stage-one s20 says this will occur).
6. **Baseline:** masked-completion learner on identical vector waves + identical
   schedule; params within ~2× of PAM's plastic side [CC counts]; (B1)/(B2) constants
   from its own calibration seeds, same two-stage.
7. **Slotted items — ALL RATIFIED at the checkpoint read** (deployed topology; ladder
   on promote; coherence-ablation post-promote; substreams mechanical).
8. **Asserts:** EXP10 §7.1 numeric machinery extended — per-lag correlation bound over
   lags ≤ k_max; k ⟂ member (chi-square); schedule ⟂ member (frequency uniformity);
   background ⟂ member; ε forms inherited from EXP10's pins.
9. **Seeds/horizon:** verdict {0–4} per arm, +2 pool {5,6}, **cal {20–24} (n=5, widened
   at final read — a stage-two threshold from two seeds' spans is thin; never verdict)**;
   discriminator fires at 3 seeds; horizon = max measured acquisition onset + W_post +
   margin (EXP11 §2 form) — **onset bound from the CORRECTED-LAW re-cal,
   censoring-aware: a censored cal seed makes the bound a ≥, never a max.**
10. **Boundary-leak monitor (Adjustment 1 — position-matched, schedule-unmatched):**
    read-only off-schedule word-mask probes at POSITION 1 of dwells whose scheduled exam
    was harness-suppressed. Naive mid-dwell probes would measure anticipation PLUS
    recency, confounded; position-matching removes the recency channel, so
    scheduled-vs-probe divergence at matched acquisition isolates SCHEDULE-ANTICIPATION.
    No gradient. Probe-dwell rate small (fabric-thinning guard), constant at stage-two.
    Registered divergence fires fallback (c).

**Sequence: build → calibration pre-flight (stage-one/two; constants recorded) → rig-1
arms (A-DWELL, A-SHUFFLE) → four-cell read behind the verification pass → margin guard →
ladder-ordered fires as triggered → one review.**
