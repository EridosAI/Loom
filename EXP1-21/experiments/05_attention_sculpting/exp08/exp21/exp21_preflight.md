# EXP21 — TOUCH-2 PRE-FLIGHT PACKAGE (G3b closed; HARD HOLD before G4)

**Prereg:** `docs/EXP21_PAM_TEACHING_CONTRAST_PREREG.md` (Touch-1 ratified; commit `19a8fbf`;
SHA-256 `0889ad77950d2981c3dbd16bb762331884d50b2f01d6f75143b2a2a363e4636b`).
**HEAD at assembly:** `925f62a2a7a23736955dd8602cb818c45166e45d`.
**State: G0-G3b CLOSED, every red observed first. G4 NOT RUN; VERDICT SEEDS UNTOUCHED.**
`run_verdict` refuses until `exp08/exp21/exp21_touch2_ratified.json` (ratified=true) is
committed on Jason's word.

## (a) Operational definitions — where they bite

The ratified prereg carries the verbatim law text (§3.3-§3.6, §4, §5). The deployed
implementations, one function each (exp21_cal.py unless noted): `assert_grid_complete`
(planned grid t=0 / every 3,000 / exactly read_at — silent truncation HALTs),
`assert_record_complete` (horizon + final eval column), `eligible_index` (first read >=
cfg.t2), `episode_start` (5-consecutive-read law), `initial_state_law`, `acq_area`
(normalized area t_eligible..750k), `q4_indices`/`fq_of` ((750k, 1M], 84 reads),
`viability_fails` (chance-referenced broad-guard law), `dynamic_range_route` (§3.6),
`verify_constants` (recompute-verify, the row-56 guard), `assert_summary_integrity`
(from-raw digit-identity), exp21_probe `assert_bank_binding` (canonical-bank law),
exp21_score `seed_route`/`cohort` (§5 precedence + §4.6), exp21_verify `compare_census`/
`compare_routes`. Every law application runs on FULL-precision series; rounding is
display-only.

## (b) Constants — formula, measured inputs, value, provenance

All in `exp21_constants.json` (committed this gate; cut before any verdict data existed):

- **theta_cat = 0.5380859375** — smallest k/2048 with k/2048 >= 0.5 + delta_point_cat AND #(null streams with any 5-read episode across all 10 cal runs) <= 4/4096. Inputs: delta_point_cat =
  0.03417969, floor = 0.53417969, null exceedance
  at theta = 4/4096, null top-8 =
  [0.542969, 0.54248, 0.539062, 0.538086, 0.537598, 0.537598, 0.536621, 0.536621]. cut on the 10 calibration runs' committed primary-bank predictions before any verdict data exists; null seed 410001230000 (offline scorer-side).
- **t_eligible = 3000** (computed: first planned read >= cfg.t2 (=1200)).
- **N_ACQ = 5** (EXP21 design constant fixed by ratification).
- **Q4** = (750,000, 1,000,000], 84 planned reads.
- **FQ familywise bound = 0.14285714285714285** — smallest k/84 with #(null streams whose max-over-runs Q4 occupancy at theta_cat >= k/84) <= 4/4096.
  Null FQ top-8: [0.452381, 0.297619, 0.214286, 0.130952, 0.130952, 0.119048, 0.119048, 0.119048].
  **SURFACED:** the §4.2 familywise count (<=4/4096) applied identically to §4.3's bound — the only in-document count referent; surfaced for the Touch-2 read.
- **Envelopes:** delta_point_cat = 0.03417969; delta_acq = 0.00038477;
  delta_ret = 0.07142857; delta_guard_q4 = {'coarse_a': 0.008980845238095225, 'distractor': 0.008149642857142814, 'member': 0.011079285714285736, 'participation_ratio': 0.011936369047619078};
  delta_guard_point = {'coarse_a': 0.10791000000000003, 'distractor': 0.09033199999999997, 'member': 0.05078199999999994, 'participation_ratio': 0.23163899999999993}; delta_internal = {'exam_acc': 0.010601899159663863, 'asg_cat': 0.07520587830612246}.
  Companions: {'pointwise_cat_max': 0.08935546875, 'pointwise_cat_mean': 0.006916394589552239, 'pointwise_guard_max': {'coarse_a': 0.278808, 'distractor': 0.310547, 'member': 0.07568299999999997, 'participation_ratio': 0.7196639999999999}, 'n_pointwise': 3350}.
- **Guard bars (chance-referenced, common to both arms):** {'coarse_a': 0.258981, 'distractor': 0.50815, 'member': 0.073579, 'participation_ratio': 1.011936}.
- **Guard law (verbatim):** viability — guard q FAILS iff Q4-mean <= chance_q + delta_guard_q4(q); PR FAILS iff Q4-mean PR <= 1 + delta_guard_q4(PR); OFF NONVIABLE iff >= 2 broad guards fail among {coarse_a, distractor, member, PR}; category excluded. Selectivity —
  category advantage selective iff adv_cat > adv_q + delta_guard_q4(q) for BOTH q in {coarse_a, distractor}; adv = paired ON-OFF Q4-mean margin difference on the axis. Collapse — the improving arm's category gain is wrong-reason iff that arm's paired Q4-mean on distractor OR member falls beyond delta_guard_q4(q), or its Q4-mean PR <= floor (applied in BOTH directions by the scorer). General —
  if the improving arm's benefit on any word-unnamed bacc axis {coarse_a, distractor, member} >= its category advantage while that advantage clears repeatability -> GENERAL-STABILISATION (rank rides as a reported companion; scale-mismatched with bacc, surfaced at Touch 2).
- **Internal-metric law:** ['exam_acc', 'asg_cat'] direction ON > OFF,
  Q4-mean; fires iff ON-OFF > delta_internal(m).
- Null: 4096 streams, seed 410001230000 (offline scorer-side), grid k/2048 (balanced 1024/class).

## (c) Pre-check outcomes

No substitutions anywhere. G0 constructor/fabric/init parity + faithful-runner
digit-identity (record fields AND checkpoint state vs `run_exp14_arm`) + probe inertness
(single-bank, dual-bank, off-grid horizon) + repeat determinism (the process-scheduling
justification): all PASS at seed 0. Fabric asserts passed inside every one of the 10
calibration runs (per-run manifests committed).

## (d) Gate table + observed-red census

Every gate row names its executor and its observed-red set (each red fired a DEPLOYED law,
recorded in the gate artifact, then restored green):

- **G0** — `exp21_teaching.g0_parity` — outcome: PASS; reds: ['fabric_bit_flip', 'live_stim_probe_call', 'probe_gen_consumption', 'read_order_swap']
- **G1** — `exp21_diffscope.main` — outcome: PASS; reds: ['off_planted_step_override', 'on_planted_step_override', 'shared_exp12_edit', 'shared_loop_edit']
- **G2** — `exp21_teaching.g2_gradient_census` — outcome: PASS; reds: ['baseline_no_detach', 'cue_only', 'noop_hooks', 'pam_dead', 'single_mask_path_only', 'target_only', 'vision_frozen']
- **G3a** — `exp21_probe.g3_probe_audit` — outcome: PASS; reds: ['bank_hash_mismatch', 'empty_class', 'label_imbalance', 'live_counter_changed', 'pam_called_by_probe', 'restore_green', 'support_overlap']
- **G3b** — `exp21_cal.main` — outcome: PASS; reds: ['ceilinged_on', 'chance_converter', 'empty_q4', 'nonbiting_guard', 'null_threshold_injection', 't0_acquisition']
- **G4** — `exp21_run.run_verdict` — outcome: NOT RUN — refuses without exp21_touch2_ratified.json; reds: fixture-only census committed (unratified_launch, resume_attempt, paired_bank_mismatch, step_count_mismatch, record_overwrite)
- **G5** — `exp21_score.main` — outcome: fixture census only; frozen scorer committed pre-G4; reds: ['guard_bypass_plant', 'seed_pooling_plant', 'unrouted_pattern']
- **G6** — `exp21_verify.main` — outcome: fixture census only; executor + deployed comparators built; reds: ['bank_swap', 'gradient_record_tamper', 'missing_bare_n', 'raw_column_mutation', 'route_flip']

Halt list: prereg §8 verbatim, all standing. Envelopes: (b) above.

## (e) Protocol instance

CORRIDOR_PROTOCOL.md at HEAD governs; three-touch cadence; this package is touch 2.
Executor/positive-delta/reachable-falsifier census: every G0-G6 gate has its executing
function committed and its named fixtures OBSERVED RED through the deployed law it
certifies (gate artifacts carry the red messages).

## Dynamic-range ruling (§3.6, mechanical)

**Route: BOTH-QUESTIONS-LIVE** — ON max bacc 0.679688 vs floor 0.53418;
acq-immediate flags [False, False, False, False, False]; retention ceilinged: False.
OFF broad collapse in calibration: NONE.

## Calibration census (bare N = 10 runs; per-run summaries in exp21_calibration.json)

Wall time per run (s): {'off_s20': 3022.6, 'off_s21': 2894.1, 'off_s22': 2951.8, 'off_s24': 2913.8, 'off_s25': 2915.8, 'on_s20': 2926.7, 'on_s21': 2931.9, 'on_s22': 3073.0, 'on_s24': 2917.6, 'on_s25': 2957.6}; total 8.2 h.
Storage (committed + on-disk): {'records': {'n': 10, 'mb': 44.4}, 'probe_pt': {'n': 20, 'mb': 14.1}, 'probe_json': {'n': 20, 'mb': 5.4}, 'banks': {'n': 19, 'mb': 3.6}, 'checkpoints': {'n': 20, 'mb': 3.3}}.
Probe cost, measured (§10.2): {'seconds_per_read_per_bank': 0.0422, 'emissions_per_read': 2560, 'reads_per_full_run': 335, 'projected_seconds_per_run_per_bank': 14.1} — per read per bank; shadow rode all 10
cal runs; verdict runs will read primary only.
Checkpoints: saved on disk per the standing contract, gitignored by repo convention
(`*.pt`); SHA-256 digests committed in `exp21_preflight.json` (the EXP19 digests-committed
precedent). Banks: 13 primary + 5 cal shadows committed at G3a (+1 s0 shadow from G0's
dual-bank parity check — never read at verdict).

## Surfaced readings (mechanical implementations of ratified text — flagged for the read)

1. **FQ familywise count:** §4.3 names "the fresh 4,096-stream familywise null bound"
   without a count; the §4.2 count (<=4/4096) is applied identically — the only
   in-document referent.
2. **Arm-neutral collapse cell:** §5's CATEGORY-COLLAPSE-IN-COSTUME text names no arm; the
   scorer tests the IMPROVING arm's compression in both directions, and OFF-BETTER
   requires the OFF-side guards clear.
3. **GENERAL-STABILISATION breadth axes:** the §5 cell names coarse A, distractor, member
   information, or rank; the mechanical max runs over the three bacc-scale axes
   (coarse_a, distractor, member); rank (participation ratio) is scale-mismatched with
   bacc and rides as a reported companion (adv_pr in every seed detail).
4. **Cohort "materially different causal routes":** mechanical form = a second
   causal-claim cell (TEACHING-ADDED / PRESERVATION-ONLY / OFF-BETTER) beside the top
   route forces SEED-SPLIT (fixture-proven).
5. **§3.6 restriction wiring:** when calibration routes PRESERVATION-ONLY-RESTRICTION, the
   scorer disables acquisition-based cells in BOTH directions (fixture-proven).

## What ratification opens

G4: 2 arms x 8 paired seeds x 1M from scratch (16 runs), primary bank only, then G5 frozen
scoring and G6 independent verification. **Nothing runs until
`exp21_touch2_ratified.json` is committed on Jason's word.**
