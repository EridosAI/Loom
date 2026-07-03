# EXP09 — The self-path #12 reference: design pins + pre-registered function test

**STATUS: SPEC AT CHECKPOINT (2026-07-03). Nothing is built; nothing runs until Jason
ratifies the [RECONCILE] items below. Gate steps 5–6 stay BLOCKED.**

Fork 1 of the design table (FRONTIER §10.13) resolved → **(a) give the self-path its
missing #12 reference.** The diagnosed violation: the self-path is the one plastic loop
through the associative operator (the PAM target path) with no slower reference — vision
predicting vision, both sides the same weights. (JEPA's within-member stop-grad loop
sits outside #12's scope — exonerated as engine, not reference-bearing.) The word path
had its reference (the frozen anchor) and its channel survived to full horizon. The
design supplies the self-path's reference: **a slow copy of the vision cortex supplies
the self-path reconstruction target.**

Drift guard, verbatim from the ruling: this is the most-ML-familiar move on the table —
**it passes on FUNCTION (input-sensitivity self-sustaining under the deployed flow,
kick-free), never on the EMA vocabulary.**

*Pre-commit adversarial verification (2026-07-03, 32-agent / 4-lens / per-finding
independent verify): 23 confirmed findings applied to this spec and its companion canon
before first commit. The load-bearing ones are marked in place below.*

---

## 1. Design pins (ruled 2026-07-03)

- **The slow copy supplies the self-path reconstruction target ONLY.** A full parameter
  copy of the vision cortex (`θ_slow`; everything `vision.emit` touches — scope
  `[RECONCILE]`, full-cortex proposed), initialized `θ_slow = θ_online` at t=0 (the
  birth snapshot is STORED — §6.1 needs it), updated post-optimizer-step by the
  fixed-lag rule `θ_slow ← θ_slow + β (θ_online − θ_slow)`. **Detached — a reference,
  not a co-developer:** the slow copy never receives gradient (forward-only; build
  assert).
- **Wiring: the `_pam_target` hook point** (`loop.py:121`, identity default; the same
  hook the exp08 detach diagnostic used), config-gated (`pam_target_ref = "online" |
  "slow"`): the vision-slot targets of the window become the slow copy's emissions of
  the SAME window stimuli, computed under `no_grad`. NB the existing signature
  `_pam_target(content)` does not see the window's raw stimuli — the hook signature is
  extended (or a SlowRefLoop overrides `build_cells`) `[RECONCILE at build]`. **Word
  path and targets untouched** (build assert: word-slot target byte-identical to the
  baseline path). **One code path** — no new loop dynamics, no new loss term (build
  assert: loss-term count unchanged).
- **#12 form: build-full / pin-to-constant.** The lag machinery is built schedulable
  (β(t)); **v1 pins a single fixed constant β `[RECONCILE]`** (§4). The relaxation
  schedule is deferred to the release gate — designed there, never defaulted here.

## 2. What the reference is supposed to do (the function, stated once)

Under the no-detach baseline the target follows the online encoder instantly: when
routing starts contracting, the target contracts with it — nothing in the loop stores
yesterday's distinctions. Under (a) the operator is held to a LAGGED map: if the online
encoder starts collapsing, PAM is still trained toward pre-collapse targets, its
predictions retain the earlier distinctions, and the mismatch reaching the online
weights (cue side) pulls back toward them — **distinctions generating the pressure that
keeps distinctions.** That is the design-gate constraint ("input-sensitivity
self-sustaining under the deployed flow") implemented as a reference, not as a new
force.

## 3. Mechanical consequences — stated plainly (the honesty block)

These are facts of the construction, verified in source before this spec was written:

1. **At EVERY β, the direct target-side gradient into online vision at masked cells is
   zero** (the slow target is `no_grad`). The gradient topology w.r.t. online vision is
   therefore **identical to the exp08 DETACH diagnostic** — the canonical gap-3
   target-side pressure is SEVERED at every β; the mismatch reaches the online weights
   via the completion/cue-side path only. What differs from detach is the target's
   CONTENT (lagged map vs current map), hence what PAM converges to, hence what the
   cue-side path and the evocation channel teach. **The design is a bet that
   lagged-content targets re-supply the teaching function through that path — the bet
   §6 must certify.**
2. **The design family interpolates detach ↔ freeze and never contains the baseline:**
   at β=1 it degenerates EXACTLY to the detach arm (target = current values, no grad);
   at β=0 to a frozen-at-birth target (a reference that never acquired anything — the
   pre-acquisition map has no distinctions to restore). The lag window is therefore
   two-sided (§4).
3. **PAM-loss gradient reaches online vision only through VISIBLE vision cells.** In
   the all-vision-masked family, vision receives no PAM gradient that wave
   (operator-only). Named consequence, watched not fixed: the per-family gradient
   census column (§8).
4. **The detach arm did not pin either** (exp08: detach prevented collapse;
   word-channel structure 3/3 at 30k). Therefore **a bare no-pin PASS cannot
   distinguish "the reference is doing work" from "the target-side pull is absent."**
   The wrong-reason screen (§6) is load-bearing, not pro-forma.
5. **The word-channel wrinkle (verification catch):** in the only committed word-arm
   seed carrying the full column set (word_terminal_s1), word-channel structure is
   num = 0.0 in every window through t=45000 — the word→category association
   POST-DATES routing collapse in that seed. What the reference can absorb pre-collapse
   is the VISION-side differentiated map, not the word association. §2's "yesterday's
   distinctions" means the vision map.

Consequence 1+4 is the guard interaction, faced directly: **detach stays DIAGNOSTIC and
is never the fix** — and this design shares detach's gradient topology. The design's
claim to be different is entirely in the reference content and must be EARNED at §6, at
the checkpoint's satisfaction, before any PASS is trusted.

## 4. The lag constant β — `[RECONCILE]` with derivation (checkpoint decides)

The window is two-sided. **Verification correction on the record:** the first draft's
fast bound ("acquisition plateaus by ~30k") traced to NOTHING and is contradicted by
canon — §10.12.1's generalized caution (any word-dependent 30k read is
acquisition-suspect; vocab2 word-axis structure absent 2/3 seeds at 30k) and by the
artifact itself (§3.5: s1 num = 0.0 through 45k). The corrected derivation uses only
committed clocks:

- **Slow bound (#12: the reference changes slower than what it regulates):** 1/β ≫ the
  healthy collapse-regrow den period (working constant 4800 waves, word regime; but see
  §5's period-instrument discrepancy) — the reference must not follow a trough down.
- **Fast bound — against the DIFFERENTIATION-holding window, and UNMEASURED on the
  acquisition side.** The reference is useful only if it carries a differentiated
  vision map when contraction starts. Measured collapse clocks: word s1 — first
  argmax_k=1 transient at t=25200, SUSTAINED from t=42600 (the "~50k" canon shorthand
  is not used quantitatively here); word s0 — healthy through ~72k, occupancy chance
  from ~96k. No committed artifact pins when the vision map itself is "acquired" —
  there is NO measured acquisition-plateau clock; the fast bound is therefore a
  judgment the checkpoint makes with that uncertainty on the record.
- **Absorption arithmetic for the candidates** (EMA absorbed fraction 1 − e^(−t/τ), τ =
  1/β): τ=9600 → 93% by t=25200, 99% by 42600; τ=12000 → 88% / 97%; τ=23100 → 66% /
  84%.

**Candidates** (1/β in deployed waves): 9600 / **12000 (proposed v1 pin)** / 23100
(flagged: at the worst-case measured onset its absorption is ~66% — likely outside the
window; kept on the list for the checkpoint to strike). Single value ratified at
checkpoint; logged in the run config; never a copied literal downstream (`[RECONCILE]`
at build from this section).

## 5. The pre-registered FUNCTION TEST (pinned before any run; kick-free)

**Arms and horizons** (from the measured clocks, per the ruling):
- **Word arms, seeds {0, 1}** (the terminal-replication pair) — horizon **≥ 192000
  waves = 2× the 96k seed-0 terminal clock** (≈4.5× the seed-1 sustained-collapse
  onset at 42.6k).
- **No-word arm, seed 0, same horizon — RIDES AS CONTROL.** Explicitly pre-terminal by
  its own ~518k clock at this horizon: a differential comparator, NOT a terminality
  read.
- No kicks, no perturbations, deployed flow only.

**Measured baseline facts the literal forms are calibrated against (verification
catches):** the healthy pre-collapse word span (word_terminal_s1, 20.1k–42.3k, 74
windows) already flickers to argmax_k=1 in 8/74 windows (~11%) and dips den below 1e-3
in troughs — only 41% of healthy-span 2-period placements satisfy an every-window form;
and the committed no-word run contains THREE epochs ≥ 1 den period with argmax_k=1 AND
den sub-floor in every window that later REGROW (longest regrown epoch 5.9 periods). An
every-window PASS bar is stricter than any measured healthy state, and a
duration-only PIN bar over-fires on the control regime. Both forms below are pinned
accordingly.

**Outcome taxonomy (total — every run lands in exactly one):**

- **METASTABLE EPISODE (not a verdict):** any epoch with `asg_argmax_k = 1` AND den
  below the 1e-3 tripwire in EVERY window, lasting ≥ 1 full den period, that regrows
  before horizon end. Logged, never scored as PIN (the 500k no-word adjudication
  idiom).
- **PIN (word arms):** such an epoch persisting THROUGH horizon end with duration ≥ K_w
  den periods. `K_w [RECONCILE]`, proposed 3 (no committed word-regime pin ever
  regrew).
- **PIN vs PIN-CENSORED (control arm):** the committed no-word regime regrows from
  epochs up to 5.9 periods — duration alone cannot separate pin from episode there. A
  horizon-end epoch of duration < K_c periods = **PIN-CENSORED** (named outcome;
  resolution = extension at its own ruling, NOT an automatic FAIL); ≥ K_c = **PIN**.
  `K_c [RECONCILE]`, must exceed the measured 5.9; proposed 8.
- **FAIL = PIN on ANY arm** (a control PIN at this horizon = acceleration).
- **PASS (WORD ARMS, both seeds; literal form, flicker-tolerant, constants calibrated —
  the CALIBRATION RULE is what is pinned):** over the final 2 den periods of each word
  arm: `asg_argmax_k > 1` in ≥ X% of windows AND no argmax_k=1 run longer than L
  consecutive windows AND den above the 1e-3 tripwire in ≥ X% of windows with no
  sub-floor run longer than L. **Calibration rule (pinned):** X and L are set at
  checkpoint from the committed word_terminal_s1 spans such that EVERY measured healthy
  2-period placement passes and EVERY measured terminal placement fails; the healthy
  flicker rate (~11%) implies X ≈ 80; L computed from the longest healthy argmax_k=1
  run in the artifact. `X, L [RECONCILE]` — constants land at checkpoint, before any
  run.
- **NEITHER (pre-registered third outcome):** no PIN, PASS criteria unmet. Restoration
  NOT certified; interpretation and next action at its own ruling — never rescued into
  a PASS.

The control contributes the FAIL/PIN-CENSORED criteria and comparator columns only —
it is NOT held to the PASS criteria (the committed baseline no-word run
argmax-collapses at ~162k, inside this horizon, without pinning; an (a)-arm control
doing the same is comparator data, not a verdict).

**Period constants — instrument discrepancy on the record (verification catch):** the
entry run measured den period ≈4800 at eval cadence 100; the committed word-arm
dynamics panel (word_terminal_s1, cadence 300 — the cadence these arms inherit) reads
dominant_period_steps = 1500 on the same regime. Window sizes for PIN/PASS depend on
this 3.2× discrepancy. **Checkpoint pins:** (1) the period estimator (instrument + the
trajectory segment it runs on — healthy pre-collapse segment only, proposed); (2) a
numeric threshold for "changed dominant period" before a run's own measured period
replaces the pinned constant; (3) the fallback when the panel returns None (= the
pinned constant); (4) the eval cadence. Working constants until then: 4800 word /
23100 no-word, discrepancy logged.

**PASS is NECESSARY, NOT SUFFICIENT.** A PASS that has not cleared §6 decides nothing
(confidence-first guard).

## 6. THE WRONG-REASON SCREEN — the detach-null comparator (load-bearing)

The null model is the exp08 detach arm: reference-free amputation, which also does not
pin. Before any PASS is trusted, the design must show the reference DOING WORK — an
observable the null lacks. Pinned screens:

1. **Reference-distinctness (mechanical validity, three columns):**
   `‖θ_slow − θ_online‖` (detach-equivalence watch: bounded away from 0 after lag
   warm-up), `‖θ_slow − θ_slow(0)‖` (freeze-equivalence watch: the slow copy must move
   away from the stored birth snapshot — verification catch: the first two columns
   cannot detect β-too-slow), and `‖slow_target − online_target‖` (target space, per
   probe window). Bounds `[RECONCILE]`. These certify the KNOB, not the function.
2. **The teaching discriminator `[RECONCILE at checkpoint — pick and pin]`.**
   **Verification catch, applied: the first draft's candidate (ii) — "differential
   gradient share above the detach-null's" — is STRUCK as a certifier: member-distinct
   slow targets mechanically guarantee member-dependent probe gradients whenever §6.1
   distinctness holds, so it certifies that the reference EXISTS, not that it
   teaches.** Surviving candidates:
   - **(i) A detach-null comparator ARM at the same horizon with the same columns**
     (target = online-detached; the detach arm used AS a diagnostic — never as a
     candidate). The null trajectory everything else is judged against. Cost: one more
     arm.
   - **(ii′) Outcome-level divergence from that null:** input-sensitivity trajectories
     (asg_dist / argmax_k), regrow-after-episode behavior, occupancy — differences in
     what the SYSTEM does, not in what the probe gradient mechanically inherits.
   - **(iii) §L entry-gate acquisition criteria** firing on the (a) arms (entry
     machinery reused as-is) where the null's acquisition record is thinner (detach has
     only a 30k read: num 0.26/0.59/1.35, 3/3).
   Proposal: (i) + (ii′), with (iii) logged alongside. Checkpoint decides.

## 7. THE DECOMPOSITION OBSERVABLE (ruled 2026-07-03; read-only; "the common part becomes a number")

Wired as standing columns (eval cadence; dynamics panels standing — an average never
ships alone; parts logged separately, never only ratios — the den lesson). **Explicitly
NOT a §6 certifier** (see the struck candidate above): a trajectory instrument.

- **Evocation split.** Over the 16-member associative evocation set {e_i} (the standing
  `evoke_vision(associative=True)` probe): μ = population mean; `evo_common = ‖μ‖²`;
  `evo_diff = mean_i ‖e_i − μ‖²`; ratio as the third column. Complements num/den (num =
  cross-class separation, den = centred CONTENT norm; this is the EVOCATION set's own
  energy decomposition).
- **Gradient split, same decomposition.** Per-member forced-mask probes (the grad_split
  idiom — read-only w.r.t. weights, no optimizer step): g_i = the PAM-loss gradient
  w.r.t. member i's vision emissions in the probe window; ḡ = mean_i g_i; `grad_common
  = ‖ḡ‖²`; `grad_diff = mean_i ‖g_i − ḡ‖²`; ratio. **Probe-design pins (verification
  catches):** (1) **RNG isolation** — the existing grad_split idiom draws stimulus
  noise from the TRAINING generator (`loop.gen`); the new probes MUST use an isolated
  probe generator or clean centres (the `evoke_vision` idiom), with a build assert that
  the training RNG stream is untouched — else bit-faithful replay comparability is
  void. (2) **Mask-geometry control** — the standing word/self grad-split ratio carries
  a mask-geometry factor (the word-path probe masks all W=3 vision cells, the self-path
  probe one; measured ≈4.0 mechanical at pinned states in word AND no-word arms — the
  §10.13 row-2 refutation). The per-member probes use ONE fixed mask geometry across
  all members so cross-member comparisons cannot inherit it. Exact tensor plumbing
  `[RECONCILE at build]`.
- **The deliverable:** the contraction/teaching ratio as a TRAJECTORY — where it sits,
  when it tips, what (a) does to it.
- **Baseline comparator `[RECONCILE at checkpoint]` — cost corrected by verification:**
  the committed runs predate these columns, and replay is proven bit-faithful at HEAD
  (7a0db83). The first draft priced the replay at "~3.5h" — WRONG: the artifact
  timestamps show the word_terminal_s1 replay ran in ~4 minutes (05:29→05:33,
  2026-07-03) and the 500k marathon extension in ~19 minutes. Proposal accordingly
  upgraded: replay BOTH baselines (word_terminal_s1 AND marathon_ext_s0) carrying the
  new columns, so "what (a) does to it" has measured baseline trajectories on both
  regimes.

## 8. Readouts

The standing column set verbatim (den/num + NOT_ASSESSABLE floor 1e-3; asg_dist /
asg_argmax_k / asg_entropy; occupancy dc_track; proto_spread; word-path/self-path
grad_split; masking-mix census) + dynamics panels + the new columns: §6.1
reference-distinctness (three), §7 decomposition pair, per-family gradient census
(§3.3). Entry-gate machinery reused as-is. Windowed estimators rig-wide (standing
mandate).

## 9. Guards (verbatim; standing)

- **Kick-not-a-candidate** — barred; this design contains no noise term.
- **Counter-force = manufacturing class** — the door stays bolted: no new force, no new
  objective (build assert §1); the reference re-times an existing path.
- **Confidence-first** — §6 must be cleared before the first PASS is trusted.
- **Detach stays DIAGNOSTIC** — the exp08 arm is the §6 null comparator, never the fix;
  §3's honesty block records that this design shares its gradient topology and earns
  its difference at §6.
- **Steps 5–6 BLOCKED.** No arm here is a gate step; a §5 PASS re-opens that question
  at its own ruling, nothing auto-proceeds.

## 10. Checkpoint list (what ratification pins before any build)

1. β v1 value (§4 candidates; 12000 proposed; 23100 flagged likely-outside; fast bound
   ratified WITH its unmeasured-acquisition caveat on the record).
2. Slow-copy scope (full vision cortex proposed) + birth-snapshot storage + the
   hook-signature extension route (§1).
3. Function-test constants: K_w (proposed 3), K_c (proposed 8), the PASS calibration
   rule's X and L (computed from word_terminal_s1 at checkpoint), the period-estimator
   pin (§5: instrument, segment, changed-threshold, None-fallback, cadence).
4. The teaching discriminator (§6.2: proposal (i) + (ii′), (iii) logged; (ii) struck).
5. Reference-distinctness bounds (§6.1, three columns).
6. The baseline-replay knob (§7: BOTH baselines, minutes not hours — proposed yes).
7. The detach-null comparator arm alongside (§6.2(i) — proposed yes).
8. Probe hygiene asserts (§7: RNG isolation; fixed mask geometry).
