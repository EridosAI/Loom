# EXP09 — The self-path #12 reference: design pins + pre-registered function test

**STATUS: CHECKPOINT RESOLVED (2026-07-03) — build authorized per the ruled sequence:
resolve → wire → surface resolved prereg + wiring asserts + replayed-baseline
decomposition panels at ONE FINAL PRE-RUN READ → arms run. Gate steps 5–6 stay
BLOCKED.**

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

*Process record: pre-commit adversarial verification (32-agent / 4-lens / per-finding
verify) applied 23 confirmed findings; the checkpoint ruling (Jason, 2026-07-03)
ratified the strikes, RE-WORDED ground (3) (teaching path re-routed, not intact — his
carry), pinned the β RULE, ratified the outcome taxonomy, and resolved the eight open
items per the pins recorded in place below.*

---

## 1. Design pins (ruled; scope/birth/route RESOLVED at checkpoint)

- **The slow copy supplies the self-path reconstruction target ONLY.** Scope RESOLVED:
  **the full self-target emission path** — a complete parameter copy of the vision
  cortex (everything `vision.emit` touches). Birth RESOLVED: **bit-copy of online at
  t=0** (stiff-early automatic; the birth snapshot is STORED — §6.1 reads against it).
  Update: post-optimizer-step fixed-lag rule `θ_slow ← θ_slow + β (θ_online − θ_slow)`.
  **Detached — a reference, not a co-developer:** never receives gradient
  (forward-only).
- **Route RESOLVED: the existing identity-default hooks, one code path, always
  detached.** Wiring plumbing note: `_pam_target(content)` does not see the window
  stimuli, so the build wraps `build_cells` in the EXP09 loop subclass (calls super,
  re-poses the TARGET's vision rows from the returned window `raw` under `no_grad`) —
  no signature change to the base hooks, no change to any existing arm.
- **Wiring ASSERTS (ruled):** identity at t=0 (`‖θ_slow − θ_online‖ = 0`); divergence
  > 0 after warm-up; ZERO grad to the copy (no parameter of the slow copy carries
  grad_fn / requires_grad); word-slot target byte-identical to the baseline path;
  loss-term count unchanged (no new force, no new objective).
- **#12 form: build-full / pin-to-constant.** Lag machinery built schedulable (β(t));
  v1 pinned by RULE (§4). Relaxation schedule deferred to the release gate — designed
  there, never defaulted here.

## 2. What the reference is supposed to do (the function, stated once)

Under the no-detach baseline the target follows the online encoder instantly: when
routing starts contracting, the target contracts with it — nothing in the loop stores
yesterday's distinctions. Under (a) the operator is held to a LAGGED map: if the online
encoder starts collapsing, PAM is still trained toward pre-collapse targets, its
predictions retain the earlier distinctions, and the mismatch reaching the online
weights (cue side) pulls back toward them — **distinctions generating the pressure that
keeps distinctions.** That is the design-gate constraint implemented as a reference,
not as a new force.

**Ground (3), as RE-WORDED at checkpoint (supersedes "gap-3 intact"):** teaching path
RE-ROUTED, not intact. The canonical target-side gap-3 pressure is severed at every β
(detached target); the mismatch reaches online vision via the cue/completion side only;
word path untouched. The design is a recorded BET — lagged-content targets re-supply
the teaching function — certified or refuted by the §6 screen + detach-null comparator,
never assumed.

## 3. Mechanical consequences — stated plainly (the honesty block)

Facts of the construction, verified in source:

1. **At EVERY β, the direct target-side gradient into online vision at masked cells is
   zero** (the slow target is `no_grad`) — the gradient topology w.r.t. online vision
   is identical to the exp08 DETACH diagnostic. What differs is the target's CONTENT
   (lagged map vs current map), hence what PAM converges to, hence what the cue-side
   path and the evocation channel teach.
2. **The design family interpolates detach ↔ freeze and never contains the baseline:**
   β=1 degenerates EXACTLY to the detach arm; β=0 to a frozen-at-birth target (nothing
   acquired, nothing to restore). The lag window is two-sided.
3. **PAM-loss gradient reaches online vision only through VISIBLE vision cells** — the
   all-vision-masked family contributes operator-only gradient. Watched, not fixed
   (masking-mix census, §8).
4. **The detach arm did not pin either** — a bare no-pin PASS cannot distinguish "the
   reference is doing work" from "the target-side pull is absent." §6 is load-bearing.
   **The pre-registered partial outcome (checkpoint, "the bet gets teeth"):
   (a) ≈ detach-null on outcomes ⇒ the slow copy is STOP-GRAD IN COSTUME — the function
   test may PASS while the paradigm bet FAILS; that routes back to the design table as
   a PARTIAL RESULT, never laundered into PASS.**
5. **The word-channel wrinkle:** in word_terminal_s1, num = 0.0 through t=45000 — the
   word→category association POST-DATES routing collapse in that seed. What the
   reference can absorb pre-collapse is the VISION-side differentiated map. (Canonized
   as a named ledger observation, §10.13: the word's pull is task-structural, present
   before measurable association — log, no claim.)

## 4. The lag constant β — RESOLVED BY RULE (checkpoint)

**The rule (pinned): period estimator first, then τ = 1/β = 2 × the pinned den
period.** Acquisition-derived bounds are STRUCK until acquisition is measured (the
first draft's "~30k plateau" traced to nothing — verification catch on the record).

**Period resolution (executed 2026-07-03, before β/K_w consumed it — the §5 instrument
ruling):** the cadence-100 entry-run series is the INSTRUMENT OF RECORD →
**den period = 4800 stands** (panel output on the full n=1125 series). The
word_terminal_s1 panel's 1500 is demonstrated to be SEGMENT CONTAMINATION: the same
estimator on its full series reproduces 1500 (early ramp + ~70k pinned tail dominate
the autocorrelation), while on the healthy segment (20100–42300) it reads 6000 — the
same order as 4800; the residual 6000-vs-4800 gap is attributed to seed + short-segment
quantization (75 windows ≈ 4.7 nominal periods at cadence 300). EXP09's own estimator
therefore runs on the HEALTHY SEGMENT ONLY (per-run, recorded).

**Resolved values:** τ = 2 × 4800 = **9600 waves**; β = 1/9600 ≈ 1.042e-4 per wave,
applied post-optimizer-step.

**Retention caveat — numbers stated, not bounds (checkpoint ruling):** EMA absorbed
fraction 1 − e^(−t/τ) at the measured collapse clocks: **92.8% by t=25200** (s1 first
argmax transient), **98.8% by t=42600** (s1 sustained onset); mean content lag = τ =
9600 waves (at the s1 sustained-collapse onset the reference ≈ the online map of
~t=33k). Stated for the record; the fast side of the window remains UNMEASURED on the
acquisition axis.

## 5. The pre-registered FUNCTION TEST (RESOLVED constants; kick-free)

**Arms and horizons:**
- **Word arms, seeds {0, 1}** — horizon **192000 waves** (= 2× the 96k s0 terminal
  clock; ≈4.5× the s1 sustained onset).
- **No-word arm, seed 0, same horizon — RIDES AS CONTROL** (pre-terminal by its own
  ~518k clock; differential comparator, not a terminality read).
- **Detach-null comparator arm alongside (§6, ratified):** target = online-detached,
  same horizon, same columns, word seeds {0, 1} share its record `[one seed proposed:
  s1 — the faster measured clock; second seed only if the read demands it]`.
- No kicks, no perturbations, deployed flow only. Eval cadence 300 (the exp08 idiom);
  4800-wave period = 16 windows; final-2-period read = 32 windows.

**Outcome taxonomy (RATIFIED — total; calibrate-tolerance-from-measured-healthy, third
instance of the lesson):**

- **METASTABLE EPISODE:** `asg_argmax_k = 1` AND den < 1e-3 in every window for ≥ 1
  full den period, then regrows before horizon end. Logged, never scored as PIN.
- **PIN (word arms):** such an epoch persisting THROUGH horizon end, duration ≥ K_w =
  **3 word periods (14400 waves / 48 windows)**.
- **PIN vs PIN-CENSORED (control):** K_c = **8 no-word periods (184800 waves)** — must
  exceed the measured 5.9-period regrown maximum. **Honest consequence, on the record:
  at the 192k horizon a control PIN requires epoch onset ≤ ~7.2k and is practically
  unreachable; a control terminal epoch will surface as PIN-CENSORED → extension at its
  own ruling, not auto-FAIL.** Acceleration therefore cannot hide: it lands as
  PIN-CENSORED + extension, never silently inside PASS.
- **FAIL = PIN on any arm.**
- **PASS (WORD ARMS, both seeds) — constants CALIBRATED from the 44 healthy 32-window
  placements of word_terminal_s1 (20100–42300; the only committed word-arm healthy span
  carrying columns — single-seed calibration, noted), fixed pre-run:**
  1. No PIN on any arm over the full horizon;
  2. `asg_argmax_k > 1` in **≥ 27 of the final 32 windows** (observed healthy worst =
     27/32 = 84.4%) AND **no argmax_k=1 run > 2 windows** (observed healthy max run =
     2);
  3. **den ≥ 1e-3 in ALL 32 final windows** (observed healthy: ZERO sub-floor windows —
     the earlier "healthy den dips" came from including the collapse transition; in
     the strict healthy span the every-window den form is CALIBRATED, not assumed).
  **Terminal-exclusion check (constructed, verified): the measured terminal signature
  reads 0/32 on criterion 2 and 0/32 on criterion 3 with a k=1 run of 32 — it can never
  sit inside this tolerance.** (num-freeze, the third terminal marker, is logged
  alongside; not a PASS criterion.)
- **NEITHER (pre-registered third outcome):** no PIN, PASS unmet. Restoration NOT
  certified; interpretation and next action at its own ruling — never rescued into
  PASS.

**Period-estimator pin (resolved):** instrument = `revival.dynamics_panel` on the den
series, HEALTHY SEGMENT ONLY; instrument of record for the pinned constants =
cadence-100 (4800 stands); per-run recomputation at the run's own cadence recorded;
**changed-threshold: the run's own measured healthy-segment period replaces 4800 for
that run's window counts only if it differs by > 1.5× (either direction), and the
substitution is LOGGED**; estimator returns None → pinned constant.

**PASS is NECESSARY, NOT SUFFICIENT** (confidence-first): a PASS that has not cleared
§6 decides nothing — and the §3.4 partial outcome (stop-grad in costume) is live even
on PASS.

**WHAT A PASS CERTIFIES — pinned at the final pre-run read (Jason, 2026-07-03), before
wave 0, because the decomposition read will tempt more:** the replayed baselines showed
healthy phases running ~10⁴:1 common-dominated — whatever held routing open in the
healthy regime, it was NOT differential gradient winning a balance. Therefore: **if the
slowref arms PASS, the certified claim is "the reference sustains input-sensitivity" —
nothing more. HOW it sustains it (restored differential fuel vs changed common geometry
vs something else) is read off the decomposition columns as a SEPARATE finding, never
assumed.** A PASS does not silently validate the balance story the baselines just
undermined.

## 6. THE WRONG-REASON SCREEN — the detach-null comparator (load-bearing)

Null model = the exp08 detach arm run at the function-test horizon with the same
columns (§5). Discrimination RESOLVED at checkpoint (share-vs-lift, third appearance —
the gradient-share candidate is STRUCK as circular: member-distinct slow targets
mechanically produce member-dependent probe gradients):

1. **Reference-distinctness (mechanical validity, standing columns):**
   `‖θ_slow − θ_online‖` (detach-equivalence watch: bounded away from 0 after
   warm-up), `‖θ_slow − θ_slow(0)‖` (freeze-equivalence watch, against the stored
   birth snapshot), `‖slow_target − online_target‖` (target space, per probe window),
   and **slow-copy target PAIRWISE distinctness across the 16 members = a standing
   column with the floor RESOLVED at the final pre-run read (Jason, 2026-07-03):
   floor = 3e-4** — geometric placement ≥3× below the weakest replayed-baseline
   healthy minimum (0.000907, no-word) and ≥8× above the word terminal (1.1e-5).
   **COPY-COLLAPSE (pairwise distinctness below floor) = a NAMED OUTCOME — the
   reference failing at its own level — never silently absorbed.** These certify the
   KNOB, not the function.
2. **The teaching discriminator (RESOLVED): the detach-null comparator arm +
   OUTCOME-LEVEL divergence** — input-sensitivity trajectories (asg_dist / argmax_k),
   regrow-after-episode behavior, occupancy; differences in what the SYSTEM does, not
   in what the probe gradient mechanically inherits. §L entry-gate acquisition reads
   logged alongside (machinery as-is). **Partial-case routing per the re-worded ground
   (3): (a) ≈ null on outcomes ⇒ STOP-GRAD IN COSTUME ⇒ partial result to the design
   table.**

## 7. THE DECOMPOSITION OBSERVABLE (read-only; "the common part becomes a number")

Standing columns (eval cadence; dynamics panels standing; parts logged separately,
never only ratios). **Explicitly NOT a §6 certifier** — a trajectory instrument.

- **Evocation split.** Over the 16-member associative evocation set {e_i}
  (`evoke_vision(associative=True)`, clean centres): μ = population mean; `evo_common =
  ‖μ‖²`; `evo_diff = mean_i ‖e_i − μ‖²`; ratio as third column. Complements num/den.
- **Gradient split, same decomposition.** Per-member probes: g_i = the PAM-loss
  gradient w.r.t. member i's vision emissions in a probe window; ḡ = mean; `grad_common
  = ‖ḡ‖²`; `grad_diff = mean_i ‖g_i − ḡ‖²`; ratio. **Probe hygiene (RULED — asserted
  at wiring):** (1) **RNG isolation** — probes use an isolated generator / clean
  centres, NEVER `loop.gen`; assert: the training RNG stream is untouched by probes
  (demonstrated end-to-end by the baseline replays reproducing the committed standing
  columns bit-identically). (2) **Geometry equalized-or-recorded per probe class** —
  the per-member probes use ONE fixed mask geometry across all members (equalized);
  the standing word/self grad-split keeps its asymmetric pair with the ≈4.0 mechanical
  geometry factor RECORDED as an instrument caveat; probe-class composition logged.
  (3) **THREADS (wiring catch, measured 2026-07-03): the determinism contract is seed +
  construction order + torch THREAD COUNT.** At 16 threads, parallel-reduction order
  perturbs floats ~1e-9 relative — visible ONLY in the ratio column's coarse 6-decimal
  quantization (93 windows off by the last digit; num/den/asg untouched); at 1–2
  threads the replay is byte-identical to the committed artifacts (which came from the
  kick session's thread-limited parallel phase). The new probes were EXONERATED by A/B
  isolation (none-vs-full: 0 mismatches over 6000 steps). **Pinned: every EXP09 run and
  replay executes at torch threads = 1; the thread count is recorded in every artifact
  (`torch_num_threads`).**
- **The deliverable:** the contraction/teaching ratio as a TRAJECTORY — where it sits,
  when it tips, what (a) does to it.
- **Baseline comparator (RATIFIED, upgraded):** replay BOTH baselines
  (word_terminal_s1 AND marathon_ext_s0) carrying the new columns (~4 min + ~19 min
  measured; replay bit-faithful at HEAD). **This back-fills the common/differential
  decomposition onto the measured collapse baselines — the "common part" trajectory
  lands BEFORE EXP09 runs, at the final pre-run read.**

## 8. Readouts

The standing column set verbatim (den/num + NOT_ASSESSABLE floor 1e-3; asg_dist /
asg_argmax_k / asg_entropy; occupancy dc_track; proto_spread; word/self grad_split with
its geometry caveat; masking-mix census) + dynamics panels + the new columns: §6.1
reference-distinctness (four, incl. pairwise), §7 decomposition pair. Entry-gate
machinery reused as-is. Windowed estimators rig-wide.

## 9. Guards (verbatim; standing)

- **Kick-not-a-candidate** — barred; no noise term in this design.
- **Counter-force = manufacturing class** — door bolted: no new force, no new
  objective (wiring assert); the reference re-times an existing path.
- **Confidence-first** — §6 must be cleared before the first PASS is trusted; the
  stop-grad-in-costume partial outcome is pre-registered and cannot be laundered into
  PASS.
- **Detach stays DIAGNOSTIC** — the detach arm is the §6 null comparator, never the
  fix.
- **Steps 5–6 BLOCKED.** A §5 PASS re-opens that question at its own ruling; nothing
  auto-proceeds.

## 10. Checkpoint list — ALL EIGHT RESOLVED (2026-07-03 ruling; values above)

1. β: RULE = 2× pinned den period → **τ = 9600** (period resolution executed; 4800
   stands). Retention numbers stated as caveat; acquisition bounds struck.
2. Scope = full self-target emission path; birth = bit-copy at t=0, stored; route =
   identity-default hooks via the build_cells wrap; asserts as §1.
3. Function-test constants: K_w = 3; K_c = 8 (control-PIN unreachability consequence
   recorded); PASS = 27/32 + max-run 2 + den all-32 (calibrated from the 44 healthy
   placements; terminal-exclusion verified); period estimator pinned (healthy-segment;
   ×1.5 changed-threshold; None → constant; cadence recorded).
4. Teaching discriminator = detach-null comparator arm + outcome-level divergence;
   gradient-share candidate struck; partial-case routing pre-registered.
5. Distinctness = four standing columns; pairwise floor set at the final pre-run read
   from the replayed-baseline healthy-span value; copy-collapse = named outcome.
6. Baseline replays: BOTH, with new columns (minutes, not hours).
7. Detach-null arm alongside: YES (s1 first).
8. Probe hygiene: RNG isolation + geometry equalized-or-recorded + composition logged,
   asserted at wiring.

**Remaining before arms run: wire → ONE final pre-run read (resolved prereg + wiring
asserts + replayed-baseline decomposition panels). Nothing else.**
