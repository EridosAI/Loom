# NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1

**PASSIVE AUDIT — design evidence, not an executed motor intervention.** All available native records from FS-001–FS-060 were read; pooled complete-life results use the fixed 59-life denominator. FS-060 remains a separate 124 s prefix. No P reconstruction, motor generator call, RNG draw, field preparation, world replay or new life occurred.

## Finding

**The current bottleneck is partly about how movement is organized in time, not arena sparsity alone.** These animals move, but repeatedly reverse along a strongly persistent body-heading axis. Short directional persistence, balanced forward/backward motion and repeated occupancy explain much of the low displacement descriptively. This is not simply immobility, continual full-circle turning, or wall trapping.

The observed pattern is strongly consistent with the current newborn spontaneous motor design: separate 7 s and 9 s zero-centred sinusoidal components plus short-correlated noise. Actual commands also include direct sensory feedback, learned/evoked terms and regulation. The passive audit cannot causally isolate the generator or demonstrate that changing it would improve development. It supplies a sound reason to review temporal structure before treating smaller geometry as the primary remedy.

## Complete-life metrics (59 lives)

Unless otherwise stated, “median” below means the median of per-life summaries, not a pooled count of native samples.

| Measure | Result | Meaning / limit |
|---|---|---|
| Native path length | median **13.6558**; range 12.8259–14.4119 | Substantial accumulated movement |
| Maximum excursion from birth | median **0.5327**; range 0.2970–1.1834 | Small spatial envelope |
| Final displacement | median **0.2924** | Return/cancellation matters; endpoint alone is not the audit |
| Translational speed | median lifetime mean **0.03179 units/s**, median RMS 0.04108 | Slow but sustained movement; not zero actuation |
| Angular speed | median mean absolute **0.06165 rad/s**, median RMS 0.08001 | Oscillating rotation does not imply many complete circles |
| Absolute accumulated heading motion | median **26.51 rad** | Sum of absolute increments, not net orientation change |
| Forward/backward time above 0.01 speed | means **38.34% / 38.27%** | Approximately balanced body-axis progress and reversal; remainder is deadband |
| Forward bout duration | median per-life median **3.395 s**; median per-life maximum 6.19 s | Bouts end when body-forward speed no longer exceeds 0.01 |
| Reverse bout duration | median per-life median **3.385 s** | Comparable opposite progress |
| Sustained forward↔reverse switches | median **94/life**, range 88–100; median **13.13/min** | Each signed bout must persist ≥0.1 s; deadband is ignored between them |
| Left/right actuator correlation | median Pearson **0.01865**, range −0.03767…0.07441 | Little common command correlation |
| Opposite-sign commands | median **49.55%** of time | Differential actuation frequent; not itself proof of a damaging turn |
| Common/differential command RMS | medians **0.10366 / 0.10182** | Forward and turning drive components comparable in command units |
| Predominantly rotating / translating / mixed / inactive | means **34.98% / 36.36% / 28.05% / 0.61%** | Time-weighted ratio of body-edge angular speed to translational speed, definition below |
| Velocity-direction correlation first ≤1/e | median **1.6 s**, range 1.5–1.6 | Oscillatory first-crossing descriptor, not exponential decay constant |
| First-60-s direction first crossing | median **1.5 s**, range 1.4–1.8 | Poor persistence is already present early |
| Body-heading correlation | median **0.9794 at 4 s**, **0.9421 at 120 s** | None crosses 1/e over tested lags through 120 s |
| Velocity-direction correlation | median **−0.8576 at 4 s** | Movement commonly points opposite to its direction four seconds earlier |
| Path curvature above speed 0.01 | median of per-life medians **0.3915 rad/unit**; median per-life p90 **5.7477** | Includes curved motion, excludes ill-conditioned near-zero speed; not a circular orbit fit |
| Absolute velocity-direction turning / accepted distance | median **1.3295 rad/unit** | About 76.5% of adjacent native pairs meet curvature filters |
| Visited 0.25-unit bins | median **6**, range 2–11 | Point-centre occupancy, not swept body area |
| Re-entry into already visited 0.25 bins | median **92.96%** of cell transitions | Consecutive within-bin samples are not counted as entries |

Rotation dominance means active $r|\omega|>2|v|$; translation dominance means active $|v|>2r|\omega|$; otherwise mixed. Active means either edge rotation or translation >0.005 units/s, with r=0.5. This descriptive classification is not an intention, energy allocation or mandated nursery target. “Inactive” is not proof of a designed rest state.

Median reversal counts at 0.005, 0.01 and 0.02 speed deadbands are **99, 94 and 82**; median forward-bout durations are **3.640, 3.395 and 2.925 s**. Full reversal sensitivity is retained in `EXPLORATION_SUPPLEMENT.json`. Coverage is also measured on one-unit bins (median 2), and with a half-bin offset on the 0.25 grid (median 6; median re-entry 92.31%). The recurrent-space result does not depend on one grid alignment. Curvature uses actual saved velocity directions rather than assuming heading equals movement direction; the latter fails during reverse movement.

## Coverage growth and mean-square displacement

All 59 complete lives are observed at every age below. MSD is ensemble mean squared distance from birth; it is not squared mean displacement. Path and coverage columns are ensemble means, hence they need not match medians above.

| Age (s) | Mean path | Birth-relative MSD (units²) | Mean 0.25 bins visited | Median maximum excursion |
|---:|---:|---:|---:|---:|
| 30 | 1.4552 | 0.06155 | 3.542 | 0.3164 |
| 60 | 2.8487 | 0.11295 | 4.068 | 0.3842 |
| 120 | 5.3965 | 0.14266 | 5.136 | 0.4481 |
| 180 | 7.6436 | 0.15994 | 5.610 | 0.4759 |
| 240 | 9.5744 | 0.19181 | 5.864 | 0.5034 |
| 300 | 11.2203 | 0.20564 | 6.136 | 0.5120 |
| 360 | 12.5385 | 0.18798 | 6.203 | 0.5327 |
| 420 | 13.5420 | 0.19150 | 6.339 | 0.5327 |

Motion continues after coverage growth has slowed substantially. Later MSD is not monotonically increasing: the paths revisit local regions. There is no claimed asymptotic plateau or fitted diffusion law from these short, depleting, nonstationary histories.

The separate mean time-averaged lag-MSD is 0.001615 at 1 s, 0.011612 at 4 s, **0.006124 at 7 s**, 0.019055 at 30 s, 0.031199 at 60 s and 0.045343 at 120 s. Its short-lag rise and fall is consistent with outward-and-back movement, not ordinary monotonic diffusive displacement. Birth-relative and time-averaged MSD are not interchangeable; they sample different ages and include different transient/depletion effects. Correlations/lag-MSD use fixed 0.1 s observer subsampling; native speed, bouts, paths and coverage use the complete saved 0.01 s records.

## Early versus late movement

Ensemble mean speed falls from **0.04748** in 0–60 s to **0.01673** in 360–420 s. Mean absolute angular speed falls from **0.09319 to 0.03220 rad/s**. Early forward/reverse time fractions are **42.57% / 42.03%**; late they are **32.05% / 31.31%** at the same 0.01 threshold. The temporal cancellation is already present before late-life slowing.

Current actuator force scales with $0.2+0.8E$, so depletion is a plausible direct contributor to declining movement magnitude. That algebra does not isolate all neural/mechanical causes. Extra energy runway could preserve movement capacity longer, but need not convert repeated reversing into wider exposure.

## Geometry trapping: important in some lives, not a population explanation

**50 of 59 complete lives have no native positive contact rate above 1e−12.** Their median path is 13.6533, maximum excursion 0.5212, final displacement 0.2717, reversals 94 and directional first crossing 1.6 s. They show essentially the same local reversal pattern. **45 of these 50 never enter sampled surface gap ≤0.25 from any fixture**, including the moving block.

Median near-wall time within either 0.25 or 0.5 is zero. Across-life mean wall-near fractions are 2.11% and 7.00%, respectively, with individual high-exposure exceptions. At most 0.447% of any complete life's duration is in native bins with positive contact impulse/rate; actual event contact duration is a different quantity and remains in the prior impact report. This is inconsistent with hard contact pinning most animals for most of their lives. FS-002's repeated wall contact and individual near-wall histories still matter.

No-contact motion does not exclude environmental influence through vision, chemistry, proprioceptive feedback or regulation. No world-free or motor-omitted counterpart was run. Thus environmental trapping is not a necessary general explanation, but this is not a causal proof that all geometry effects are absent.

## Implementation consistency and attribution boundary

Frozen `loom_p/neural.py::Motor.step` computes two components `0.25*sin(phase) + 0.1*nu`, with periods **7 and 9 s**, filtered independent sign drives at **0.5 s refresh**, noise time constant **1 s**, and motor-tendency time constant **0.1 s**. Each final command also includes actual direct feedback, evoked material and regulatory current, passes through tanh and is attenuated. The waves, learning and body coupling were not disabled in these lives.

As an additional descriptive check, the already-specified 7/9 s sine/cosine bases were regressed separately against their corresponding saved 0.1 s command channels. The retained R² values quantify resemblance to the known oscillator periods, not a causal variance attribution, a trained controller or a proposed generator. No learned coefficients are supplied to an organism. Median command R² is **0.93294 (left, 7 s) and 0.93328 (right, 9 s)** over whole lives, and **0.94212 / 0.94229** in the first 60 s. The sampled heading span over a life is median **1.227 rad** (range 0.796–2.056), despite 26.51 rad of absolute accumulated angular motion. This supports heading oscillation rather than continuous full-circle spinning; span is from 0.1 s display samples, so it is a sampled bound. Whole-life and first-60-s fits are both recorded in `EXPLORATION_SUPPLEMENT.json`.

The observable combination—near-zero mean signed forward velocity, roughly equal forward/reverse residence, high heading correlation, strongly negative movement-direction correlation around 4 s and near-zero left/right correlation—makes **short-lived, alternating translation** the leading identifiable kinematic limitation. Differential drive produces substantial angular activity too, but “tight circles everywhere” is not supported as the sole or clearest explanation.

| Candidate cause | Passive disposition |
|---|---|
| Insufficient movement magnitude | Motion is present and extensive in aggregate. Speeds are modest and decay later, so magnitude can contribute; inactivity alone is inadequate |
| Excessive turning/reversal | Reversal strongly supported. Rotation is substantial, but largely heading oscillation/persistence rather than universal full loops |
| Insufficient directional persistence | Strongly supported for velocity direction, already early; body heading itself persists |
| Environmental trapping | Local cases possible; cannot account for the 50 contact-free histories or 45 clearly separated ones |
| Another cause | Balanced independent oscillatory actuation plus depletion-dependent capability is a plausible combination; exact causal shares and learned-regulation contribution unresolved |

## Design consequence

Add **newborn spontaneous-motor temporal structure** as a separate, explicitly unselected Nursery-0 dial. Preserve the three draft ecology/runway candidates. The audit changes the recommendation: **do not lock the 14-unit arena as the necessary remedy before resolving whether to redesign blind spontaneous temporal structure.** N0-B remains the preferred *conditional* option if Jason deliberately freezes the current motor process for the first nursery comparison.

There is enough evidence to justify a narrow temporal-structure design review, but not enough to select a numerical replacement, promise broader wandering, prove useful learning or choose a new larger arena. Source sparsity and short runway remain relevant; their optimal intervention sizes depend on exposure generated by the motor process. The main design's new motor-dial section records the permitted conceptual direction and the decisions still required.

## Files and execution boundary

Methods fixed before native metric extraction: `EXPLORATION_AUDIT_METHODS.md`. Complete tables: `EXPLORATION_PER_LIFE.csv`, `EXPLORATION_AGE_BLOCKS.csv`, `EXPLORATION_COVERAGE_MSD_BY_AGE.csv`, `EXPLORATION_CORRELATIONS_MSD_BY_LAG.csv`; per-life detail JSON includes all selected lags and threshold checks. Plots are display-only renderings of these passive results.

The audit checksum-verified **25,503 native chunk files**, read **2,547,923 native rows**, and matched every recomputed path length to the prior report within 1e−8. Stored initial objects were decoded as data dictionaries, never reinstantiated as engines. Original archives/records are untouched. FS-060 stays APPARATUS_INTERRUPTED_UNCLOSED; no tail was inferred. **Zero P/world/field/prehistory steps, no births, no draws, no authorities, no parameter changes.**


## Passive figure

![Saved-record exploration metrics show repeated reversal and slowing coverage growth.](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_0_design_20260930_v0_1/EXPLORATION_DYNAMICS.png>)

[Vector figure](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_0_design_20260930_v0_1/EXPLORATION_DYNAMICS.svg>); [all per-life numbers](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_0_design_20260930_v0_1/EXPLORATION_PER_LIFE.csv>); [coverage and MSD by age](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_0_design_20260930_v0_1/EXPLORATION_COVERAGE_MSD_BY_AGE.csv>); [correlations and lag-MSD](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_0_design_20260930_v0_1/EXPLORATION_CORRELATIONS_MSD_BY_LAG.csv>).
