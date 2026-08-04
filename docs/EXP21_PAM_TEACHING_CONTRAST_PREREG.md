# EXP21 — PAM-TEACHING CONTRAST

## Does deployed PAM teaching add or preserve externally useful visual-category differentiation in the certified-dead dwelled regime?

**Status:** TOUCH-1 RATIFIED — BUILD AUTHORIZED THROUGH G3 ONLY; HARD HOLD BEFORE G4.  
**Date:** 2026-08-04 (Asia/Singapore).  
**Code/document baseline:** `EridosAI/Loom` at `d965680cf2cfeb80cc873bdb525525273f18c01f` (`Canon: redefine §5.5 as PAM-teaching contrast`).  
**Authority carried:** Jason’s ratification of the five Touch-1 entry rulings on 2026-08-04.  
**Ratified by:** Jason Dury, 2026-08-04 (Asia/Singapore).
**Build authority:** The enumerated implementation and calibration scope through G3 only. G4 verdict execution remains unauthorized until the Touch-2 pre-flight package is separately ratified.

---

## §0 Binding inheritances — carried explicitly, never silently

The following five rulings are already fixed and are not reopened by this draft.

1. **Arm semantics.** Teaching ON is the deployed coupled learner. Teaching OFF structurally blocks both cue-side and target-side `L_PAM` gradients into the visual cortex while PAM remains present, performs the same forward operation, receives its own gradients, and continues learning.
2. **Entry.** The arm may enter under §5.3-SAT-2 without extending the fence only if an experiment-specific hook subclass passes an actual-arm B11 proof and every shared learner-chain file remains byte-untouched.
3. **Compute.** The comparison matches exposure, forward calls, parameter counts, optimiser membership, optimiser-step count, PAM learning opportunity, and evaluation schedule. Exact backward FLOP equality is neither claimed nor manufactured; no dummy backward work is permitted.
4. **Instrument.** The headline instrument is a dedicated, trajectory-inert, held-out, vision-only discrimination probe. Category is primary; coarse `A`, distractor, member identity, and broad geometry are guards.
5. **Outcome taxonomy.** Acquisition and preservation are distinct. The nine routed outcomes in §5 are exhaustive for this experiment.

Standing inheritances also bind:

- the certified `exp12_dwell` fabric and its current deployed learner are the bench;
- `W=1`; `L_JEPA` is inert in this lineage and is not an autonomous visual objective;
- held-out perceptual discrimination, never PAM’s own loss, carries the causal claim;
- nothing transports: every threshold, viability floor, repeatability envelope, and route constant is cut fresh in this regime before verdict data exists;
- every gate has an executor, a real-path falsifier, and an observed-red record before it may pass;
- report-don’t-patch; an unruled condition halts;
- one fork only; the full autonomous-objective founding test remains banked.

---

## §1 Question, estimand, and claim ceiling

### §1.1 Question

With the fabric, parameterisation, exposure sequence, mask schedule, optimiser, PAM operation, and all non-PAM visual forces held fixed, does the deployed `L_PAM → visual cortex` gradient path cause the visual cortex to:

1. **acquire** externally measurable category differentiation that the same geometry-only cortex does not acquire; or
2. **preserve** category differentiation that both arms acquire but the geometry-only cortex loses?

The intervention is subtractive. Nothing is added to Teaching ON. Teaching OFF removes only PAM’s teaching edges into vision.

### §1.2 Primary estimand

For paired seed `s`, on a fixed held-out probe bank shared by ON and OFF:

- `CAT_a,s(t)` = balanced nearest-centroid category accuracy of the visual cortex at wave `t`, for arm `a ∈ {ON, OFF}`;
- `ACQ_a,s` = certified category acquisition under the fresh G3 sustained-episode law;
- `RET_a,s` = certified final-quarter category presence under the fresh G3 retention law;
- `ΔACQ_s` = the paired ON-minus-OFF acquisition-summary difference;
- `ΔRET_s` = the paired ON-minus-OFF final-quarter-summary difference.

The cohort is a paired-seed causal contrast. Seed-level routes are assigned first. No averaging may erase a route split.

### §1.3 Strongest licensed sentence

Only `TEACHING-ADDED`, with a viable OFF control and all wrong-reason guards clear, licenses:

> **On the certified dwelled bench, deployed PAM teaching pressure causes externally measured visual-category differentiation that the same geometry-only cortex does not acquire without PAM-to-vision gradients.**

The result must state the bare seed count and the frozen operational definition. The sentence does not establish superiority over a functioning autonomous visual-learning objective.

### §1.4 Other licensed sentences

- `PRESERVATION-ONLY` licenses: deployed PAM teaching pressure preserves or stabilises externally measured visual-category differentiation that the geometry-only cortex also acquires but does not retain under the frozen law.
- `GENERAL-STABILISATION / WRONG-REASON` licenses only a broad stability claim.
- `CONTROL-NONVIABLE` licenses only that PAM pressure is required for broad visual viability on this bench.
- `INTERNAL-ONLY / SELF-EASING` licenses only that PAM/routing dynamics changed or became easier internally.
- `NO-EFFECT` licenses only that no contribution was detected under this bench, horizon, and instrument.
- `OFF-BETTER` licenses only that deployed PAM teaching pressure impedes the target distinction in this regime.

PAM loss, completion, routing, assignment, or conversion metrics can never independently license a perceptual teaching sentence.

---

## §2 Arms and the exact causal delta

### §2.1 Teaching ON

Teaching ON is the deployed `EXP12Loop` on `exp12_dwell`, with the current `Stage0Loop.step`, current loss composition, current optimiser, and current read order. It is semantically REUSED but must be rerun because the new external probe and paired OFF records do not exist in committed form.

### §2.2 Teaching OFF

Teaching OFF is an experiment-specific subclass of the current `EXP12Loop`. It overrides exactly two existing hooks and no other learner method:

```python
class EXP21TeachingOffLoop(EXP12Loop):
    def _pose_pam_input(self, content):
        posed = super()._pose_pam_input(content)
        out = posed.clone()
        out[..., 0, :] = posed[..., 0, :].detach()
        return out

    def _pam_target(self, content):
        target = super()._pam_target(content)
        out = target.clone()
        out[..., 0, :] = target[..., 0, :].detach()
        return out
```

This is the binding semantic specification. The implementation may differ only in syntax, never effect.

Calling `super()` first is mandatory. OFF retains the deployed cue presentation—including the current reposing transformation—and changes only autograd connectivity. The visual values entering PAM and the visual values used as targets must be numerically identical to ON before optimisation causes the arms to diverge.

### §2.3 What remains identical

For a paired seed, ON and OFF share:

- the exact pre-generated `exp12_dwell` fabric tensors;
- member order, nuisance/background streams, noise, dwell structure, masks, exam flags, and exposure count;
- initial visual, word, and PAM parameters;
- all model dimensions and parameter counts;
- optimiser type, hyperparameters, membership, and one optimiser step per wave;
- PAM forward calls, `L_PAM` calculation, gain schedule, and PAM parameter updates;
- visual spread loss, visual pooling penalty, PAM pooling penalty, and post-step re-pool operation;
- evaluation cadence, existing read order, checkpoints, and external probe bank;
- total horizon and from-scratch execution.

### §2.4 Explicitly rejected controls

The following are not Teaching OFF and must appear only as observed-red fixtures or pathway companions:

- target detachment alone;
- cue detachment alone;
- `gain=0` or deleting `L_PAM`;
- freezing the visual cortex;
- removing PAM from the optimiser;
- skipping PAM forwards or backward calls;
- changing the mask mix or deleting word-mask waves;
- replacing the deployed learner with a bare step loop;
- adding dummy gradients, dummy backward work, or dead compute to imitate FLOP equality.

### §2.5 Actual-arm B11 ruling

The experiment-specific ON and OFF classes must both resolve `step` to the committed `Stage0Loop.step`. No class below `Stage0Loop` in either actual MRO may own `step`. The runtime source must match the prereg-baseline source byte-for-byte. The repository layer must show zero additions or changes in the shared learner chain.

A planted `step` override on the OFF class must fire the fence; restoration must return it to green. The per-edit diff-scope baseline is the future commit containing this ratified preregistration and no EXP21 implementation—not an earlier experiment’s baseline and not an uncommitted working tree.

---

## §3 External held-out visual instrument

### §3.1 Instrument principle

The probe measures only the visual cortex. It does not invoke PAM, the word cortex, the association output, completion, or any learned readout head. It never contributes a gradient or changes any model, optimiser, generator, counter, or fabric field.

The existing live `dc_track()` is retained only where the faithful runner already calls it. It is not the headline instrument, because its use of the live stimulus’s counter-advancing `raw()` path means adding or moving that call changes later spread-loss samples and therefore changes training.

### §3.2 Probe bank construction

For each training seed, before wave zero:

- instantiate dedicated probe-only stimulus objects with the same member geometry, renderer, fixed background, and seed-specific world orientation as the training arm;
- use experiment-owned, collision-audited substreams, never `loop.gen`, never the live training stimulus, and never the fabric generators;
- build one **primary** bank shared byte-for-byte by paired ON/OFF;
- build one independent **shadow** bank for calibration/repeatability only; shadow-bank values never enter verdict scoring;
- balance every bank across all 16 members;
- keep support and evaluation samples disjoint by generator construction and verify no tensor identity overlap;
- store tensors, labels, generator keys, construction parameters, and SHA-256 digests before training.

Proposed fixed bank size:

- support: `32` samples per member = `512` total;
- evaluation: `128` samples per member = `2,048` total;
- total visual emissions per read: `2,560`.

This size is a preregistration choice, not a transported constant.

### §3.3 Read cadence

The external bank is read under `torch.inference_mode()` at:

- `t=0` before the first optimiser step;
- every `3,000` waves;
- `t=1,000,000` exactly, even though it is off the 3,000-wave grid.

This yields 335 planned reads per full run. The cadence is the existing block cadence and introduces no new training-time clock because the model never receives the probe or its timing.

### §3.4 Head-free scoring

At each read, emit the support and evaluation banks through `vision.emit` only. For each axis `q`:

1. compute support centroids by class;
2. assign each evaluation embedding to its nearest centroid by Euclidean distance;
3. report balanced accuracy and margin over chance.

Axes:

| Axis | Classes | Role |
|---|---:|---|
| Category | 2 | **Primary**; word-named, lower-salience target distinction |
| Distractor | 2 | Word-unnamed selectivity guard; salient visual axis |
| Coarse `A` | 4 | Broad-viability guard |
| Member identity | 16 | Information-preservation/compression guard |

Descriptive geometry companions, never standalone proof:

- covariance trace;
- covariance participation ratio/effective rank;
- within-category and between-category distances;
- within-member spread;
- pairwise centroid-distance summaries.

### §3.5 Trajectory-inertness contract

Three parity checks bind:

1. EXP21 ON with the new probe disabled reproduces the designated current ON runner’s shared fields and checkpoint state exactly on a matched short horizon.
2. EXP21 ON with the probe enabled reproduces EXP21 ON with the probe disabled exactly on every shared field, model/optimiser tensor, generator state, counter, and canonical state digest; only the additive probe artifact may differ. Raw serialization bytes are not used as the equality criterion unless the serializer is separately proven byte-deterministic.
3. A deliberately broken probe that calls the live training stimulus’s `raw()` once per read must make parity fail. A parity test blind to that mutation is dead and cannot pass G0.

### §3.6 Instrument assumption audit

G3 must verify from the real calibration path:

- every support class is non-empty;
- support/evaluation balance and disjointness hold;
- the category estimator is neither ceilinged at `t=0` nor unsupported throughout ON calibration;
- the planned acquisition and retention questions have non-empty dynamic range;
- repeated-bank variation is measured and bounded;
- no probe call changes live stimulus counters, RNG state, optimiser state, or training records.

Routes before verdict:

- category acquisition and retention both have usable range → both headline questions remain live;
- acquisition is already ceilinged but retention has usable range → `TEACHING-ADDED` is disabled before G4; the experiment proceeds as a preservation test only;
- acquisition and retention are both ceilinged, structurally unsupported, or below resolvable range → HALT; the bench cannot answer the proposed question with this instrument;
- OFF calibration broadly collapses → record the route; do not recalibrate the control into apparent viability.

---

## §4 Horizon, seeds, calibration, and frozen decision law

### §4.1 Horizon and pairing

- Primary horizon: `1,000,000` waves, from scratch.
- No checkpoint resumes.
- No post-hoc tails.
- Paired verdict seeds: `{0,1,2,3,4,5,6,7}`.
- Fresh calibration seeds: `{20,21,22,24,25}`; no verdict seed participates in calibration.
- Each seed’s ON/OFF pair shares the exact fabric and primary probe bank.

### §4.2 Acquisition score

For arm `a`, seed `s`, read `t`:

- `cat_margin_a,s(t) = CAT_a,s(t) - 0.5`.

The sustained-acquisition form is fixed before calibration:

- `N_acq = 5` consecutive planned reads, equal to 15,000 waves on the 3,000-wave grid. This is a new EXP21 design constant fixed by ratification, not transported as a valid value from another regime;
- `θ_cat`: category score threshold cut fresh at G3;
- `t_eligible`: the first planned read at or after `cfg.t2` (computed and asserted from the run config; under the current 3,000-wave grid this is `t=3,000`, not a calibrated value);
- `ACQ_a,s`: first five-read qualifying episode, or none by 1M.

Null construction:

- 4,096 fixed, class-balance-preserving permutations of evaluation category labels;
- one permutation is held fixed across the full time series within a null stream, preserving temporal correlation in model predictions;
- the null is evaluated over both calibration arms and the complete planned read grid;
- `θ_cat` is the smallest attainable score threshold satisfying both `θ_cat ≥ 0.5 + δ_point_cat` and the condition that at most 4/4,096 null streams produce any five-read qualifying episode;
- the selected `θ_cat` must leave every calibration initial state below the five-read acquisition law; failure is a HALT, never a threshold adjustment;
- ON-calibration dynamic range is a proceed/restrict/halt gate only and never selects a more favourable threshold.

The formula, all measured inputs, the resulting value, the null exceedance count, and provenance are committed before G4.

### §4.3 Retention score

The terminal interval is the final quarter:

- `Q4 = (750,000, 1,000,000]`.

For each arm/seed:

- `FQ_a,s` = fraction of planned Q4 reads at or above `θ_cat`;
- `RET_a,s` = `FQ_a,s` exceeds the fresh 4,096-stream familywise null bound and the arm has a pre-Q4 certified acquisition.

`FQ` is primary for preservation because it measures occupancy of an episodic distinction across a terminal interval rather than requiring an unsupported locked terminal state. Final-quarter mean category margin rides beside it.

### §4.4 Instrument repeatability envelope

On calibration checkpoints only, score the same model state with primary and shadow banks.

- `δ_point_cat` = the 99th-percentile absolute primary-vs-shadow difference in pointwise category accuracy across calibration checkpoints;
- `δ_acq` = the 99th-percentile absolute primary-vs-shadow difference in the normalized acquisition-area summary;
- `δ_ret` = the 99th-percentile absolute primary-vs-shadow difference in final-quarter `FQ`;
- `δ_guard(q)` is cut analogously for each guard-axis summary;
- pointwise primary-vs-shadow differences and maxima are reported as companions;
- a paired ON/OFF difference smaller than the matching envelope is instrument-indistinguishable and cannot carry a route.

The shadow bank is never used to choose a favourable verdict value and never enters a verdict record.

Any internal metric used by `INTERNAL-ONLY / SELF-EASING` must also have a pre-named direction and a frozen G3 envelope or existing in-regime certification law. An uncalibrated favourable-looking internal curve is descriptive only and cannot fire that route.

### §4.5 Paired causal summaries

For each seed:

- acquisition summary = normalized area above `θ_cat` from `t_eligible` through 750k;
- retention summary = `FQ` in Q4;
- paired advantages are ON minus OFF.

A seed has an acquisition advantage only if:

- ON has certified acquisition;
- OFF does not;
- `ΔACQ_s > δ_acq`;
- OFF is viable;
- selectivity and compression guards clear.

A seed has a preservation advantage only if:

- both arms have certified pre-Q4 acquisition;
- ON retains and OFF does not under the frozen Q4 law;
- `ΔRET_s > δ_ret`;
- OFF is viable;
- selectivity and compression guards clear.

### §4.6 Cohort count law

With eight paired seeds, seven same-direction pairs are the minimum one-sided exact sign count below 0.05 (`9/256 = 0.03515625`). Therefore:

- a cohort route requires at least `7/8` paired seeds in that route;
- no opposite-signed route may occur;
- `TEACHING-ADDED` additionally requires all `8/8` OFF controls to satisfy the frozen viability law and `0/8` OFF seeds to show certified category acquisition;
- if no single route reaches 7/8, or materially different causal routes occur, the cohort is `SEED-SPLIT`;
- every result reports the full 8-row seed table; the count never replaces composition.

### §4.7 Selectivity, viability, and compression guards

G3 cuts all numeric envelopes fresh.

**Target selectivity.** A category advantage is selective only if it exceeds the ON-minus-OFF advantage on both word-unnamed axes—coarse `A` and distractor—by the fresh repeatability/selectivity envelope. Member improvement is allowed; it is not a competing target axis.

**Broad viability.** OFF is nonviable only under a conjunction fixed at G3: failure of at least two broad guards among coarse `A`, distractor, member information, and effective-rank/variance, with category excluded from the viability definition.

**Category-collapse guard.** A category improvement is wrong-reason compression if distractor or member performance falls beyond its guard envelope, or broad effective rank/variance crosses its collapse floor.

**General-stability guard.** If ON’s benefit is as large or larger on the word-unnamed axes as on category, the route is broad stabilisation, not selective teaching.

No guard constant transports from another experiment. Treatment-comparison bars are common across arms, cut jointly with both-arm calibration, and then applied identically. OFF is included in calibration so an ON-only internal set-point is not silently imposed on it; neither arm receives a separately favourable target bar.

---

## §5 Exhaustive outcome cells

Routes are assigned per seed first, then by the §4.6 cohort law.

**Seed-level precedence, binding:** (1) `CONTROL-NONVIABLE`; (2) `CATEGORY-COLLAPSE-IN-COSTUME`; (3) `GENERAL-STABILISATION / WRONG-REASON`; (4) `OFF-BETTER`; (5) `TEACHING-ADDED`; (6) `PRESERVATION-ONLY`; (7) `INTERNAL-ONLY / SELF-EASING`; (8) `NO-EFFECT`. The first satisfied row is the seed route. `SEED-SPLIT` is assigned only at cohort composition. This precedence prevents a flattering target score from outranking a dead control or a compression wrong reason.

`ACQUISITION-SPEEDUP`—both arms eventually acquire, ON earlier, with no preservation difference—is a reported companion under `NO-EFFECT`, not a tenth causal cell and not evidence that PAM added a distinction.

| Cell | Mechanical condition | Licensed route |
|---|---|---|
| **TEACHING-ADDED** | ON acquires; viable OFF never acquires; paired acquisition advantage clears repeatability; target-selectivity and compression guards clear | Strong §1.3 sentence, with bare-N and regime scope |
| **PRESERVATION-ONLY** | Both acquire pre-Q4; only ON satisfies frozen retention law; paired retention advantage clears repeatability; guards clear | Preservation/stabilisation sentence only; acquisition causation forbidden |
| **GENERAL-STABILISATION / WRONG-REASON** | ON protects category only as part of an equal-or-broader benefit on coarse `A`, distractor, member information, or rank | General stability only; selective teaching forbidden |
| **INTERNAL-ONLY / SELF-EASING** | PAM loss, completion, routing, assignment, or conversion improves without a certified external category advantage | Internal task became easier/different; no perceptual teaching claim |
| **CATEGORY-COLLAPSE-IN-COSTUME** | Category improves while distractor/member information or broad rank collapses beyond the frozen guard | Wrong-reason compression; no useful differentiation claim |
| **NO-EFFECT** | OFF viable; no evidence-grade acquisition or preservation cell fires and no earlier route fires. Subcriterion external shifts, including acquisition speedup, are reported as companions | No detected added/preserved distinction under this bench/instrument/horizon |
| **OFF-BETTER** | OFF has a certified category acquisition or retention advantage over ON, with guards clear | PAM teaching impedes the target distinction in this regime |
| **CONTROL-NONVIABLE** | OFF fails the frozen broad-viability conjunction rather than merely the target category test | PAM pressure required for broad stability; selective teaching not identified |
| **SEED-SPLIT** | No route reaches 7/8, opposite routes occur, or route composition is materially heterogeneous | Report seeds separately; no pooled causal sentence |

An observed pattern that cannot be assigned mechanically to one of these cells is a HALT, never a new in-corridor interpretation.

---

## §6 Cheapest-shortcut and burden-reversal audit

### §6.1 Learner-side shortcuts

- **Arm detectability:** ON and OFF differ only in autograd edges. Before the first update their forward tensors must be exactly equal. No arm flag enters the model input.
- **Time/schedule:** no new timestamp, position signal, boundary flag, terminal mask, curriculum, or predictable schedule enters training.
- **Identity:** no member-specific dynamics, dose, duration, or probe feedback enters training.
- **Loss deletion:** PAM remains active and trained in OFF; the intervention cannot be re-described as “no PAM.”
- **Frozen-cortex shortcut:** forbidden and detected by the autonomous-visual-gradient/update proof.
- **Dead-hook shortcut:** both hook overrides must be shown to change the real gradient graph on admissible scheduled masks.

### §6.2 Instrument-side shortcuts

- Probe labels exist only in the offline scorer.
- The learner never sees probe tensors, centroids, scores, or read times.
- The fixed repeated bank cannot be memorised because it never enters an update.
- The primary and shadow banks are generated and frozen before their respective permitted use.
- A category-only two-cluster compression is explicitly routed as `CATEGORY-COLLAPSE-IN-COSTUME`.
- Broad visual protection is explicitly routed as `GENERAL-STABILISATION` or `CONTROL-NONVIABLE`, never relabelled selective teaching.

### §6.3 Internal-metric burden reversal

Any favourable PAM-internal change must answer: what is the external category signal made of? Internal improvement without external discrimination is `INTERNAL-ONLY`, regardless of how coherent the mechanism story appears.

---

## §7 Corridor and gate table

The corridor hard-holds before G4 for Touch 2. Executor names below are part of build scope and must exist before pre-flight can pass.

| Gate | Executor | Pre-named condition | Observed-red / positive-delta smoke IDs | Pass action | Fail action |
|---|---|---|---|---|---|
| **G0 — REUSED/trajectory parity** | `exp21_teaching.g0_parity` | ON constructor/fabric/init matches current `exp12_dwell`; faithful-runner shared fields match; probe-enabled state equals probe-disabled state | `live_stim_probe_call`, `probe_gen_consumption`, `read_order_swap`, `fabric_bit_flip` | Commit parity artifact; proceed | HALT |
| **G1 — actual-arm B11 + diff-scope** | `exp21_diffscope.main` | shared learner chain unchanged; both actual MROs resolve committed `Stage0Loop.step`; new-file blast radius only | `off_planted_step_override`, `on_planted_step_override`, `shared_loop_edit`, `shared_exp12_edit` | Commit fence artifact; proceed | HALT |
| **G2 — gradient/compute census** | `exp21_teaching.g2_gradient_census` | forward equality at init; raw unscaled `L_PAM` gives nonzero all-vision-parameter gradient norm in ON and exact zero/unused norm in OFF on both real vision-mask and word-mask paths; PAM raw gradient and an actual gain-positive PAM update remain nonzero in OFF; autonomous visual gradient/update >0; params/optimiser/steps/forward counts match | `baseline_no_detach`, `target_only`, `cue_only`, `pam_dead`, `vision_frozen`, `noop_hooks`, `single_mask_path_only` | Commit census; proceed | HALT |
| **G3a — probe audit** | `exp21_probe.g3_probe_audit` | bank balance, disjointness, checksums, support, inertness, axis mappings, and repeatability machinery all valid | `support_overlap`, `empty_class`, `label_imbalance`, `bank_hash_mismatch`, `pam_called_by_probe`, `live_counter_changed` | Commit bank manifests; proceed | HALT |
| **G3b — calibration and dynamic range** | `exp21_cal.main` | 2 arms × 5 cal seeds at 1M; fresh acquisition/retention/selectivity/viability constants cut by prereg formulas; all inputs supported; question remains measurable | `null_threshold_injection`, `chance_converter`, `t0_acquisition`, `ceilinged_on`, `empty_q4`, `nonbiting_guard` | Commit constants/scorer/pre-flight; HARD HOLD for Touch 2 | HALT or pre-named preservation-only restriction |
| **G4 — verdict execution** | `exp21_run.run_verdict` | Touch-2 package ratified; 2 arms × 8 paired seeds ×1M from scratch; no artifact overwrite; all runtime contracts green | `paired_bank_mismatch`, `step_count_mismatch`, `resume_attempt`, `record_overwrite` | Append/push each closed run; proceed | HALT |
| **G5 — frozen scoring/routes** | `exp21_score.main` | scorer committed before G4; every seed and cohort maps mechanically to §5; internal metrics remain companions | one fixture per nine cells; `unrouted_pattern`; `seed_pooling_plant`; `guard_bypass_plant` | Commit draft result + complete composition table | HALT |
| **G6 — terminal verification** | `exp21_verify.main` | independent from-raw recomputation; bank/fabric rebuild; gradient proof replay; route recomputation; full gate log; zero MUST-FIX | `raw_column_mutation`, `bank_swap`, `route_flip`, `gradient_record_tamper`, `missing_bare_n` | Terminal surface → Touch 3 | HALT |

No gate may pass merely because its invariance check also passes a dead/no-op implementation. Every named observed-red fixture must run first and its failure message must be recorded.

---

## §8 Standing halt conditions for EXP21

HALT on any of the following:

- residual `L_PAM → vision` gradient in OFF on either scheduled mask path;
- absent PAM gradient/update in OFF;
- absent non-PAM visual gradient/update in OFF;
- target-only or cue-only partial detachment masquerading as OFF;
- ON/OFF forward-value mismatch at initial state;
- parameter-count, optimiser-membership, step-count, exposure, fabric, mask, or probe-bank mismatch;
- any shared learner-chain edit or actual-arm `step` override;
- probe-induced change to a live RNG, counter, training field, checkpoint, or trajectory;
- probe support overlap, empty class, hash drift, or label imbalance;
- category estimator ceilinged/unsupported for every licensed question;
- a calibration constant whose formula, inputs, value, or provenance is missing;
- an unobserved-red gate;
- a scorer or route changed after verdict data exists;
- a seed omitted, substituted, replayed, resumed, or pooled outside the written rule;
- an outcome not covered by §5;
- a verification panel MUST-FIX or judgment-class finding;
- any need to say “I recommend” inside the corridor.

---

## §9 Enumerated build scope — anything else requires ratification

### §9.1 New documents/code permitted

1. `docs/EXP21_PAM_TEACHING_CONTRAST_PREREG.md`  
   Ratified text, carried verbatim.
2. `experiments/05_attention_sculpting/exp21_teaching.py`  
   Experiment-scoped ON/OFF constructors; `EXP21TeachingOffLoop`; faithful runner; G0 parity; G2 gradient/compute census; short fixtures.
3. `experiments/05_attention_sculpting/exp21_probe.py`  
   Dedicated primary/shadow bank construction, manifests/checksums, head-free scorer, G3a audit.
4. `experiments/05_attention_sculpting/exp21_diffscope.py`  
   Per-edit baseline, symbol blast radius, actual-arm B11, planted override and shared-file red teams.
5. `experiments/05_attention_sculpting/exp21_cal.py`  
   Calibration executor, 4,096 null streams, repeatability envelopes, dynamic-range routes, constant artifact and pre-flight surface.
6. `experiments/05_attention_sculpting/exp21_run.py`  
   Corridor-safe cal/verdict orchestration, append-only records, paired manifests, checkpoint contract.
7. `experiments/05_attention_sculpting/exp21_score.py`  
   Frozen seed/cohort route logic and all-cell fixtures.
8. `experiments/05_attention_sculpting/exp21_verify.py`  
   Terminal from-raw recomputation/refute panel and G6 package.

Files may be combined only if every named gate executor and smoke remains independently callable and the total semantic scope does not expand.

### §9.2 Shared files forbidden to change

The build whitelist is an empty changed/addition set for at least:

- `experiments/04_stage0_mvp/loop.py`;
- `experiments/05_attention_sculpting/sculpt_loop.py`;
- `experiments/05_attention_sculpting/exp08_arms.py`;
- `experiments/05_attention_sculpting/exp12_arms.py`;
- `experiments/05_attention_sculpting/exp12_fabric.py`;
- `experiments/05_attention_sculpting/exp14_arms.py`.

If the implementation cannot be completed without touching a shared file, the build halts and returns for a fence ruling. Convenience is not an amend path.

### §9.3 Required artifacts

- `exp21_gatelog.json`;
- one primary probe-bank tensor file and manifest per unique calibration/verdict seed, plus one shadow bank per calibration seed;
- `exp21_g0_parity.json`;
- `exp21_g1_diffscope.json`;
- `exp21_g2_gradient_census.json`;
- `exp21_probe_audit.json`;
- `exp21_calibration.json`;
- `exp21_constants.json`;
- `exp21_preflight.md` and machine-readable companion;
- per-arm/per-seed run record, manifest, and terminal checkpoint;
- `exp21_verdict.json`;
- `exp21_terminal.md` and machine-readable companion;
- independent panel record with all raw recomputations and flags.

Committed records are append-only and never regenerated over the same path.

---

## §10 Priced compute and storage scope

### §10.1 Full-horizon wave updates

Calibration:

- 2 arms × 5 calibration seeds × 1,000,000 waves = **10,000,000 wave updates**.

Verdict:

- 2 arms × 8 verdict seeds × 1,000,000 waves = **16,000,000 wave updates**.

Base paid total:

- **26,000,000 full training wave updates**.

This is:

- two-thirds of EXP20’s 24-run primary verdict block for the verdict stage alone (`16M / 24M`);
- 8.33% above that 24M block when EXP21’s full calibration is included (`26M / 24M = 1.0833`).

There is no conditional full-horizon escalation arm in this preregistration.

### §10.2 External probe forwards

At the proposed bank size and cadence:

- 2,560 visual samples/read;
- 335 reads/full run;
- **857,600 read-only visual emissions per bank per full run**;
- primary banks across all 26 full runs → **22,297,600 visual emissions**;
- shadow banks across the 10 calibration runs → **8,576,000 additional visual emissions**;
- total planned external-probe load → **30,873,600 read-only visual emissions**.

These are batched, inference-only, and carry no backward pass. Their runtime and memory cost must be measured and reported at G3; they are not silently folded into “free.”

### §10.3 Engineering/verification scope

Additional bounded work:

- short G0/G1/G2 smokes and planted-red fixtures;
- one primary probe bank per unique calibration/verdict seed and one shadow bank per calibration seed;
- 4,096 offline label-permutation null streams on stored predictions;
- terminal from-raw rescoring and independent route recomputation;
- one terminal checkpoint per full run.

No extra 1M arm, no adaptive top-up, no tail, and no seed substitution pool are authorized.

---

## §11 Touch sequence and ratification surface

### Touch 1 — this document

Ratifying this draft fixes:

1. EXP21’s question and claim ceiling;
2. the exact ON/OFF arm semantics and no-shared-edit entry;
3. the 1M from-scratch horizon and paired seed sets;
4. the external bank law, proposed size, axes, and 3,000-wave cadence;
5. the five-read acquisition law, retention formulas, and 4,096-stream fresh calibration procedure;
6. the 7/8 cohort law, including 0/8 OFF acquisition for `TEACHING-ADDED`;
7. the nine outcome cells and halt list;
8. the enumerated build scope and 26M-wave-update price.

### Touch 2 — pre-flight

The package must contain verbatim operational definitions, all measured constants with formula/inputs/provenance, complete gate executor/smoke census, observed-red records, probe bank manifests, dynamic-range ruling, and exact compute/storage measurements. Ratification opens G4.

### Touch 3 — verified result

Only after independent G6 verification: attribution, licensed sentence, and canon disposition.

---

## §12 Source anchors at the prereg baseline

Authoritative paths at `d965680cf2cfeb80cc873bdb525525273f18c01f`:

- `docs/MECHANISM_MAP_v1_2_RECONCILED.md` — §5.3-SAT-2 and amended §5.5;
- `docs/CORRIDOR_PROTOCOL.md` — three-touch corridor, executor/falsifier/observed-red/support requirements;
- `experiments/04_stage0_mvp/loop.py` — hooks, loss composition, optimiser, and `Stage0Loop.step`;
- `experiments/05_attention_sculpting/sculpt_loop.py` — deployed cue reposing and live `dc_track` behavior;
- `experiments/05_attention_sculpting/exp08_arms.py` — target-only `DetachLoop` and faithful-runner precedents;
- `experiments/05_attention_sculpting/exp12_arms.py` — `W=1`, mask roles, current `build_cells`, and `exp12_dwell` constructor;
- `experiments/05_attention_sculpting/exp12_fabric.py` — pure training fabric and counter-advancing probe/spread `raw()` path;
- `experiments/05_attention_sculpting/exp19_diffscope.py` — symbol-scoped B11 and planted runtime override precedent;
- `experiments/05_attention_sculpting/exp14_arms.py` — faithful long-horizon runner and current calibration/verdict seed precedent.

---

**Stop line:** This document authorizes no code and no run until ratified. After ratification, the build may proceed only through G3 and must stop at the Touch-2 hard hold.
