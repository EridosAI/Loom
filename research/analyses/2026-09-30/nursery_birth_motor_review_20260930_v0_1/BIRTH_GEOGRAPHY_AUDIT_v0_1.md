# BIRTH_GEOGRAPHY_AUDIT_v0_1

**PASSIVE ANALYSIS / DESIGN ONLY — 2026-09-30.** Sixty preserved original time-zero checkpoints, with no new birth, world, P, field, motor or controller execution. Frozen P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; runner: `87abae34e19d4e46234402a6b1ba776814956ec1`. No authority or replacement birth law is implemented.

## Finding

**The cohort was broadly spread across safe birth support. The measured spatial pattern does not show excess clustering on the examined scales.** All 16 coarse cells contain births; 22 of 25 finer cells are occupied versus 22.115 expected. There are 62 pairs within two units versus 61.033 expected. At a one-unit neighbourhood radius, 44.15% of the conditional safe-support mixture is near a birth versus 43.37% expected. Expectations are deterministic geometry calculations under independent uniform-rejection births at the 60 actual phases, not synthetic lives.

This does not prove ideal randomness at every scale. Small local clusters and gaps exist, and rejected-proposal count has a separate low-tail observation described below. It does **not** support explaining the developmental result by all animals starting in one corner. Population coverage and within-life exploration are distinct: distributing newborns broadly cannot itself cure each animal's recurrent local motion.

Starting source distance remains strongly associated with later closest approach (Spearman 0.973), while it has almost no monotonic association with maximum excursion (−0.024). This is consistent with the prior exploration audit, not a causal analysis or a reason to place births near food.

![Preserved birth positions and headings cover all broad arena regions.](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_birth_motor_review_20260930_v0_1/BIRTH_ARENA_MAP.png>)

## Sources, scope and custody

Initial state is read from each execution store's `checkpoint-000000000-s000-initial.ld`, bound to the hash already recorded in `ALL_SIXTY_AB.json::B_initial`. The passive decoder reads stored object tags as dictionaries and NumPy arrays; it never instantiates an Engine, Organism or random stream. All 60 checkpoint file/payload hashes, time/index zero, configuration and birth-provenance position/orientation/phase agree. All actual minimum gaps are at least 0.25. The initial indexed-stream counters agree with the complete rejection ledger: one orientation and phase draw, and one position draw per recorded proposal. All four rejected positions violate the same safety threshold.

Later outcomes are read from the existing `founder_expansion_execution_20260930/analysis/ALL_SIXTY_AB.json`; no new trajectory reconstruction or outcome analysis through P is performed. All 60 births are included in spatial summaries. **Only the 59 complete lives** enter whole-life group comparisons/correlations. FS-060 remains **APPARATUS_INTERRUPTED_UNCLOSED**, with its known 124 s prefix shown separately; no unknown tail is treated as zero.

[All 60 positions, headings, phases, receptors, distances and outcome joins](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_birth_motor_review_20260930_v0_1/BIRTH_GEOGRAPHY_ALL_60.csv>) · [Exact per-birth details and checkpoint identities](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_birth_motor_review_20260930_v0_1/BIRTH_INITIAL_DETAILS.json>) · [Definitions fixed before extraction](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_birth_motor_review_20260930_v0_1/BIRTH_AUDIT_METHODS.md>) · [Input hashes](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_birth_motor_review_20260930_v0_1/INPUT_CUSTODY.json>). Source documents and code are references, not rewritten canon. The older `00_LOOM_CURRENT_STATE(2).md` was read for orientation; the September 30 artifacts govern this audit.

## Existing birth law and safe support

`loom_p/engine.py::Engine.__init__` proposes the body centre uniformly in `[0.5,19.5]²`. It rejects until the minimum body-surface gap to every wall, source disk, repair rectangle and the **actual-phase** mover is at least 0.25. The draw cap is 10,000; a failure would stop preparation, not change geometry. Heading is then an independent uniform angle. `prehistory.py` takes an independently labelled uniform world-phase draw before the lawful body-absent field history; `schema.py::Streams` derives indexed SHA-256 values from seed, life, label, counter and element. This source description is not a new RNG run or proof of statistical independence.

For mover phase $\phi$, call the admitted body-centre set $S_\phi$ and its area $A(\phi)$. Walls restrict centres to `[0.75,19.25]²`; sources exclude centre distance below 1.25. Repair and mover exclusions are their rectangles expanded by 0.75 with rounded corners. This is **birth support**, smaller than ordinary physically accessible space because birth requires an extra 0.25 clearance. Later movement does not obey this birth margin.

The primary 0.05-unit midpoint quadrature gives mean support area **290.858 units²** (phase range 290.840–290.875, mostly raster-boundary variation). It is not the nominal 400-unit arena. A finer 0.025-grid check gives **291.100 units²**, an 0.083% difference; the coarser 0.1 grid gives 291.905. Area is therefore reported approximately as **291 units²**, not exact to three decimals. One/two-unit neighbourhood coverage is 44.162%/84.909% on the finer grid versus 44.149%/84.918% on the primary grid. [SAFE_SUPPORT_QUADRATURE.json](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_birth_motor_review_20260930_v0_1/SAFE_SUPPORT_QUADRATURE.json>) and [BIRTH_SUPPLEMENT.json](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_birth_motor_review_20260930_v0_1/BIRTH_SUPPLEMENT.json>) retain the numerical sensitivity. All coverage fractions below use the equally weighted mixture of the **60 phase-conditional uniform distributions**, not a permanent ban on the swept region.

There were **4 rejected proposals**, one each in FS-024, FS-035, FS-037 and FS-057. Under ideal independent proposals and the computed ~0.806 acceptance probability, the expected rejection total is ~14.47; the approximate chance of at most four before 60 acceptances is **0.00283**. This exploratory low-tail fact is retained. It is a rejection-count check, not evidence of accepted-position clustering; a fixed finite draw stream can produce a rare count. The stored ledgers/counters are consistent, and no sampling defect is established. No reroll, extra seed or expanded RNG audit was performed. It would be incorrect to claim this task has certified all statistical properties of the birth generator.

## Spatial coverage and clustering checks

| Grid / neighbourhood | Observed | Uniform-rejection conditional expectation |
|---|---:|---:|
| Four quadrants, lower-left / lower-right / upper-left / upper-right | 17 / 13 / 18 / 12 | 15.03 / 15.10 / 14.90 / 14.97 |
| Occupied 5 × 5-unit cells (16 total) | 16 | 15.558 |
| Occupied 4 × 4-unit cells (25 total) | 22 | 22.115 |
| Occupied 1 × 1-unit cells | 55 | 54.774 |
| Unordered birth pairs separated by ≤2 units | 62 | 61.033 |
| Support-mixture mass within 1 unit of any birth | 44.15% | 43.37% |
| Support-mixture mass within 2 units of any birth | 84.92% | Not calculated |

Occupied one-unit cells contain 17.26% of the safe-support probability mass; occupied four-unit cells contain 93.26%. These depend on bin scale: 60 points have zero continuous area, and an occupied large cell is not wholly traversed or sensed. Nearest-birth separation has median **1.1105**, range **0.1873–3.2159**; the closest pair is FS-018/FS-030. Pair counts within 1/2/4 units are 13/62/245. The largest sampled safe-support point distance to any birth is 4.1704 units. All these remain coverage descriptions, not competence scores.

Exact marginal quadrant count-tail calculations under the quadrature probabilities give two-sided values 0.646, 0.649, 0.432 and 0.468 (all four Bonferroni-adjusted values 1). Sparse 16/25/400-cell dispersion is supplied descriptively, without an invalid asymptotic significance claim. No omnibus point-process test was calibrated; “no excess clustering detected here” must not become “uniformity proved.”

## Initial distance, bearing and phase

Distances below are in world units; body diameter is 1. Body-surface gap subtracts both body radius and fixture radius where applicable. Centre-to-source-surface distance is also supplied to remove ambiguity.

| Quantity | Median | Interquartile range | Full range |
|---|---:|---:|---:|
| Nearest energy source: body-surface gap | 2.07459 | 1.36037–2.71437 | 0.257556–4.49127 |
| Nearest source: body centre to source surface | 2.57459 | 1.86037–3.21437 | 0.757556–4.99127 |
| Nearest wall: body-surface gap | 3.85275 | 2.31666–5.57519 | 0.253078–7.79522 |
| Nearest repair: body-surface gap | 4.72614 | 3.79995–6.6692 | 0.432628–9.66389 |
| Actual mover at birth: body-surface gap | 5.5589 | 3.9033–7.59052 | 1.06206–12.9798 |
| Mover swept physical region: signed body gap | 3.34712 | 2.05988–5.36 | -0.32921–8.2659 |
| Body centre to mover centre-line segment | 4.70936 | 3.32012–6.47663 | 0.758727–9.40179 |

**5/60** births begin within 0.5 of source contact, **12/60** within 1.0 and **28/60** within 2.0. Geometry-only conditional expectations for the first two counts are approximately **3.54 and 12.56**, respectively, on the finer grid. Nearest-source index counts 0…7 are **5,13,6,10,8,6,8,4**. Unequal nearest-source counts are not by themselves a nonuniform sampler: accessible Voronoi regions differ.

The nearest-source bearing is wrapped relative to initial body heading; positive means counterclockwise. There are **29/60** in the forward hemisphere. Counts in eight 45° bins from −180° are **8,7,7,7,5,10,7,9**. Exact angles are in the CSV; arithmetic angle averages are not treated as meaningful direction evidence.

Body-heading eight-bin counts over 0…360° are **6,7,8,10,5,9,6,9**, mean resultant length **0.0252**. Mover-phase counts are **8,11,3,6,7,11,9,5**, resultant **0.0742**. Neither shows a strong single preferred direction. The mover centre at birth spans x=6.0004…13.9970, with motion in both directions; exact phase and signed velocity are retained. This is not a tuned phase schedule.

Mover centre track is the segment `[6,14] × {10}`; physical swept region is `[5,15] × [9.5,10.5]`. The CSV reports distance to both track and actual pose. **FS-010, FS-032, FS-033 and FS-034 have negative signed clearance to the swept physical region after body inflation, while all are safe at their own initial phase.** Such births are lawful. A swept-region overlap does not imply an initial collision or inevitable later damage.

## Initial chemistry: stored signals and observer gradients

Four raw values are read directly from the original snapshots. They are the two mixed/saturating channels at the −45° site, then the same two at +45°, each 0.501 from body centre. Labels A/B here name mixed receptor channels, not source identities. Mixing is `[[1,.5],[.5,1]]`; transduction is $r=m/(0.05+m)$. Static interpolation of the stored field reproduces all four values **exactly in the used float arithmetic** (maximum discrepancy 0), without calling transduction, updating a field, or constructing a world.

| Quantity | Median | Interquartile range | Full range |
|---|---:|---:|---:|
| Receptor 0: −45° site, mixed channel A | 0.557195 | 0.537044–0.584533 | 0.495461–0.624478 |
| Receptor 1: −45° site, mixed channel B | 0.509845 | 0.489653–0.539294 | 0.448581–0.58829 |
| Receptor 2: +45° site, mixed channel A | 0.557884 | 0.534336–0.583569 | 0.494284–0.626448 |
| Receptor 3: +45° site, mixed channel B | 0.512066 | 0.490065–0.537697 | 0.447065–0.593562 |
| Larger absolute plus-minus receptor contrast | 0.0089433 | 0.00630862–0.0135858 | 0.000846886–0.0313641 |
| Channel A absolute normalized imbalance | 0.00803208 | 0.00513515–0.0118699 | 0.00076925–0.0250253 |
| Channel B absolute normalized imbalance | 0.00885122 | 0.00536851–0.0127326 | 0.000371912–0.0276265 |
| Stored field component A gradient magnitude at body centre | 0.00337593 | 0.00234615–0.00504966 | 0.000752376–0.012029 |
| Stored field component B gradient magnitude at body centre | 0.00206455 | 0.00121782–0.00326889 | 0.000354572–0.00691468 |

The larger bilateral difference is typically ~0.009 against levels ~0.5–0.6. Values are nonzero and below saturation at 1, but neither that observation nor a gradient magnitude establishes usable navigation or a missing signal. Channel A plus-minus differences span −0.03047…0.02344; B −0.03136…0.02392. The corresponding finite differences per unit of the 0.70852-unit site chord are in the CSV. They approximate a lateral directional difference at forward-offset sampling sites; they are **not** a full gradient supplied to P.

For observer interpretation only, the exact piecewise-bilinear derivative of each **saved chemical field** is also evaluated at body centre. This uses the original array and no evolution. The field-component units differ from dimensionless receptor units; the JSON supplies both raw-field and mixed/saturating receptor-field derivatives. No hidden derivative, source coordinate or identity was an organism input. The same field can contain contributions from several materials/sources, so nearest source and local gradient need not align.

## Associations with later records — descriptive, not causal

![Birth geography and stored outcome associations, with FS-060 marked separately.](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_birth_motor_review_20260930_v0_1/BIRTH_GEOGRAPHY_ASSOCIATIONS.png>)

All rank correlations below use exactly the **59 complete lives**, one independent life summary per row. “Later closest source gap” is the minimum saved native endpoint gap, a geometric proximity measure, not proof of seeking. Exact contact comes from the existing event/contact summary. The median reduction from birth gap to later minimum is only **0.1748** units; maximum 0.9626.

| Initial predictor | Spearman with later closest source gap | Spearman with maximum excursion |
|---|---:|---:|
| nearest_source_body_gap | +0.973 | -0.024 |
| source_ahead_cos | -0.125 | -0.106 |
| chem_overall_mean | -0.798 | -0.152 |
| chem_max_abs_contrast | -0.552 | +0.131 |
| nearest_wall_body_gap | +0.598 | +0.241 |
| nearest_repair_body_gap | +0.408 | +0.022 |
| mover_swept_body_gap | -0.415 | -0.235 |
| mover_actual_body_gap | -0.508 | -0.050 |

[EXPLORATORY_ASSOCIATIONS.csv](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_birth_motor_review_20260930_v0_1/EXPLORATORY_ASSOCIATIONS.csv>) retains all prelisted predictors plus phase/heading sine and cosine. The distance association partly reflects the shared geometry of birth and later endpoints when displacement is small; it is not an independent demonstration that distance causes failure. Chemistry and wall/mover placement co-vary with the same geometry. No multivariable causal model, held-out predictor or birth-selection rule is fitted.

| Later grouping, yes / no | Counts | Median birth source gap, yes / no | Median initial mean receptor, yes / no |
|---|---:|---:|---:|
| Later within 1.0 of source | 13 / 46 | 0.748 / 2.394 | 0.5723 / 0.5288 |
| Later within 0.5 of source | 8 / 51 | 0.433 / 2.196 | 0.5792 / 0.5313 |
| Any recorded damage | 9 / 50 | 1.465 / 2.112 | 0.5415 / 0.5330 |

Only **FS-034** has source contact, so no reliable population source-contact model is estimated. It started at `(15.17078997, 9.78387852)`, source-4 gap **0.841933**, relative bearing **+157.436°** (largely behind), mover phase **312.895°**, and mean chemistry **0.537234**. Its actual mover clearance was **6.601181**, but swept-region signed gap **−0.329210**. It later incurred damage and gross energy 0.0017489243594212861; the pre-existing negative subsequent E-credit interpretation is preserved. This is not evidence that a backward heading or mover exposure is beneficial.

Damage has a mixed geographical pattern: some damaged births were near walls, others near the future mover path. A single group median would obscure that structure:

| Life | Birth wall gap | Birth swept-mover gap | Actual mover gap | Total later damage |
|---|---:|---:|---:|---:|
| FS-002 | 0.356 | +8.144 | 8.144 | 0.003338 |
| FS-010 | 6.518 | -0.241 | 4.908 | 0.016924 |
| FS-015 | 4.739 | +0.029 | 5.050 | 0.007132 |
| FS-017 | 0.683 | +3.474 | 10.008 | 0.001081 |
| FS-032 | 4.170 | -0.164 | 6.269 | 0.004760 |
| FS-033 | 5.911 | -0.214 | 1.062 | 0.009193 |
| FS-034 | 4.329 | -0.329 | 6.601 | 0.009433 |
| FS-038 | 0.253 | +8.266 | 9.147 | 0.002491 |
| FS-044 | 0.750 | +7.750 | 7.750 | 0.002328 |

Maximum excursion has no strong monotonic association with the initial source gap. Initial heading alignment and individual phase sine/cosine correlations are also modest in these records. This does not identify causal invariance; limited N, correlated geometry, shared anatomy, interactions, multiple descriptive comparisons and the interrupted FS-060 all limit interpretation. No result is used to choose a better birth location, motor parameter or viable-life subset.

## Possible stratified-random nursery law — design proposal, not adopted

**Purpose:** make the *cohort* represent broad geographical regions, without teaching any *individual* where to go. The current law has adequate broad coverage in this cohort; stratification is therefore a prospective variance/coverage choice, not a rescue justified by an observed clustering defect. It cannot fix within-life local reversal or guarantee an encounter.

Preserve the existing single-birth target law. With $p$ a centre position, $\phi$ the mover phase and $\theta$ body heading, its idealized density is:

$$
f(p,\phi,\theta)=\frac{\mathbf 1[p\in S_\phi]}{(2\pi)^2 A(\phi)}.
$$

Construct **K fixed geographical strata**, with $1<K\le N$, $C_k$ by deterministic spatial cuts of the phase-marginal safe probability measure, giving each equal mass $w_k=1/K$. Cuts use arena and collision geometry only, with a fixed axis/order/tie rule; no field values, rays, source visibility, anticipated exposure, outcomes or preferred heading. Physical source geometry enters only because it excludes unsafe body overlap. Strata are not “food”, “repair” or “interesting” zones. Broad rectangular cuts intersected with safe support are preferable to intricate semantic partitions. K and the partition are chosen from planned cohort size and geometry before drawing any births; no exact K or nursery geometry is selected here.

Allocate `floor(N/K)` lives to each stratum; assign any remainder without replacement uniformly among strata, then randomly permute the full assignment order. Each life receives independently randomized exact position, heading and phase from the **original law conditioned on its assigned stratum**. With $A_k(\phi)=|S_\phi\cap C_k|$:

$$
p(\phi\mid C_k)=\frac{A_k(\phi)}{2\pi A(\phi)w_k},\qquad
p(p\mid\phi,C_k)=\frac{\mathbf 1[p\in S_\phi\cap C_k]}{A_k(\phi)},\qquad
p(\theta)=\frac1{2\pi}.
$$

This is a geometry-only conditional distribution. Globally, randomized equal-mass quotas recover the original one-life marginal in expectation, including uniform phase and orientation, while reducing independent within-cohort placement variance. Phase is not generally uniform **within a fixed stratum** because the actual-phase mover changes its safe area; that dependence already exists in the original joint law. It must not be replaced silently by phase-first uniform sampling inside every stratum, which would produce a different joint law. A phase with zero admitted stratum area has zero probability there because of present physical feasibility, not favourable timing. Future collisions remain possible; never exclude the entire swept track.

No joint draws, strata, seeds, snapshots or authorities are produced here. The mathematical equal-mass construction requires a separately reviewed numerical geometry sampler with bounded area error. If support cannot be partitioned or sampled as declared, stop preparation; do not pick a convenient stratum, phase or source-near point. Derive the lawful prehistory **after** the selected phase is fixed; do not alter a snapshot's phase while retaining an incompatible field history. Preserve indexed streams and all rejected proposals; cap computation without an automatic reroll or replacement.

| Property | Existing uniform rejection | Proposed stratified random |
|---|---|---|
| Single-birth support and safety margin | Entire actual-phase safe set | Same set and margin; no extra future-path exclusion |
| Population allocation | Independent geography draws; chance duplication/gaps | Balanced broad geographical quotas, random assignment order |
| Position, heading, phase | Random under existing joint law | Random under its stratum-conditional law; marginal target preserved in expectation |
| Competence / sensory privilege | None from birth placement | None; stratum/geometry/quotas never supplied to the organism |
| Independence | Ideal independently indexed birth draws | Intentional cross-life dependence from quotas; must be retained in analysis |
| Inferential effect | Ordinary fixed-roster denominator | Report strata/weights and cohort design; do not pretend IID simple random sampling |
| Guarantee | Safe initial state only | Broad population allocation only; no path, food, survival or within-life coverage guarantee |
| Cost/risk | Simple rejection | More geometry/custody work; accidental phase-law distortion or overcomplicated partition |

Choosing this law would be an explicit new cohort-initialization design decision, not an apparatus-only refactor. Preserve the existing 60 births and their law unchanged. For the motor comparison in the accompanying design review, keep the proposed matched original starts; do not confound that comparison by introducing stratified birth sampling simultaneously.

## Decisions and boundary

**OBSERVED EVIDENCE:** broad population spread, small within-life reach, the listed geography associations, and the unusual low rejected-proposal count. **JASON-ACCEPTED CONSTRAINTS:** passive analysis only; no outcome-selected births or competence. **DESIGN PROPOSAL:** optionally stratify geographical cohort coverage while retaining the original single-birth joint law. **UNRESOLVED:** whether stratification is worth its added machinery, any broader random-stream concern, and how a changed motor process alters future nursery opportunity.

Jason must decide whether to retain ordinary births or request a separate exact stratification design after nursery geometry/cohort size are settled. No change is required by the current spatial clustering checks. Keep motor temporal organization, birth population coverage and ecology/runway as separate dials. No source-guided placement or numerical nursery revision follows automatically.

**Zero new lives, P/world/field/prehistory steps, RNG draws, parameter applications, authorities or Git writes.** No old sealed human B1 evaluator state was inspected. Stop for Jason review.
