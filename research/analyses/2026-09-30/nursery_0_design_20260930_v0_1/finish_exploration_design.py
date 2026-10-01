"""Summarize passive audit and revise recommendation; no Loom imports."""
from pathlib import Path
import json,math,csv
import numpy as np
OUT=Path(__file__).resolve().parent;ROOT=OUT.parent
def read(n):return json.loads((OUT/n).read_text())
def write(n,s): (OUT/n).write_text(s.strip()+'\n',encoding='utf-8')
def link(n,label=None):return f'[{label or n}](<{(OUT/n).as_posix()}>)'
A=read('EXPLORATION_AUDIT_RESULTS.json')
details=[read(f'FS-{i:03d}_EXPLORATION_DETAILS.json') for i in range(1,61)]
supp=[]
for i in range(1,61):
    p=np.load(OUT/f'FS-{i:03d}_PASSIVE_KINEMATICS.npz');t=p['time'];u=p['commands']
    q={'life_id':f'FS-{i:03d}','complete':i<60}
    # Frequencies specified by existing code before this fit. Descriptive only.
    for stage,mask in [('all',np.ones(len(t),bool)),('first60',t<=60)]:
        for channel,period in [(0,7),(1,9)]:
            tt=t[mask];yy=u[mask,channel];X=np.column_stack([np.ones(len(tt)),np.sin(2*np.pi*tt/period),np.cos(2*np.pi*tt/period)])
            residual=yy-X@np.linalg.lstsq(X,yy,rcond=None)[0]
            q[f'{stage}_command_{channel}_single_frequency_R2']=float(1-(residual@residual)/np.sum((yy-yy.mean())**2))
    q['sampled_heading_span_radians']=float(np.ptp(p['angle']))
    q['sampled_heading_final_minus_first']=float(p['angle'][-1]-p['angle'][0])
    supp.append(q)
def describe(a):return {'minimum':float(np.min(a)),'median':float(np.median(a)),'mean':float(np.mean(a)),'maximum':float(np.max(a))}
extra={'scope':'Saved 0.1-s samples only; regression is descriptive, never controller training or parameter selection','single_frequency_summary':{k:describe([x[k] for x in supp[:59]]) for k in supp[0] if k not in ('life_id','complete')},'rows':supp,
    'bout_threshold_sensitivity':{str(th):{k:describe([x['bout_sensitivity'][str(th)][k] for x in details[:59]]) for k in ('forward_median','reverse_median','reversals')} for th in (.005,.01,.02)},
    'heading_no_1e_crossing_whole_record_through_120s':sum(x['summary']['heading_acf_first_1e_s'] is None for x in details[:59])}
write('EXPLORATION_SUPPLEMENT.json',json.dumps(extra,indent=2))

audit=r'''
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

Reversal sensitivity at 0.005, 0.01 and 0.02 speed deadbands is retained in `EXPLORATION_SUPPLEMENT.json`. Coverage is also measured on one-unit bins (median 2), and with a half-bin offset on the 0.25 grid (median 6; median re-entry 92.31%). The recurrent-space result does not depend on one grid alignment. Curvature uses actual saved velocity directions rather than assuming heading equals movement direction; the latter fails during reverse movement.

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

As an additional descriptive check, the already-specified 7/9 s sine/cosine bases were regressed separately against their corresponding saved 0.1 s command channels. The retained R² values quantify resemblance to the known oscillator periods, not a causal variance attribution, a trained controller or a proposed generator. No learned coefficients are supplied to an organism. Whole-life and first-60-s fits are both recorded in `EXPLORATION_SUPPLEMENT.json`.

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
'''
write('NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md',audit)

main=(OUT/'NURSERY_0_DESIGN_v0_1.md').read_text()
start=main.index('## Recommendation and decision boundary');end=main.index('## 1. Evidence and status of claims')
replacement=f'''## Recommendation after the exploration addendum

**Do not lock the nursery geometry yet. Make a narrow review of endogenous spontaneous-motor temporal structure the next design decision.** The passive audit found substantial movement but approximately 94 forward/reverse switches per life, roughly 3.4 s forward bouts and strong recurrence. Fifty of 59 complete lives never had positive contact impulses and show the same pattern. This materially weakens arena/source sparsity as the sole or primary assumed remedy. See {link('NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md')}.

Preserve **N0-A, N0-B and N0-C exactly as provisional environment/biology candidates**. No fourth configuration, revised motor constant or larger-arena number is selected. **N0-B remains the preferred conditional configuration if Jason elects to hold the current motor process fixed:** shared 14 × 14 / twelve-source ecology, birth E=0.7, basal 0.0012, all other biology unchanged. It is no longer an unconditional recommendation to freeze that geometry now. N0-C remains lower-priority because current injuries did not cause crippling or integrity death.

If Jason instead opens a temporal-structure revision, defer choosing arena scale and source count until that blind endogenous process has a separately reviewed design and bounded physical-exposure basis. Better persistent movement may permit a larger nursery with less wall pressure and chemical crowding; that is a plausible advantage, not a measured result or permission to expand the candidate set silently.

The already-developed candidate files and earlier recommendation are preserved unchanged in {link('provisional_pre_exploration/NURSERY_0_DESIGN_v0_1.md','the pre-addendum provisional draft')}. Their numerical values remain proposals, never applied to P or the world. The sections below retain their analytical comparisons, explicitly conditional on the unchanged current motor process unless stated otherwise.

'''
main=main[:start]+replacement+main[end:]
marker='## 6. Candidate risk comparison'
motor=r'''
## 5A. New explicit dial: blind spontaneous-motor temporal structure

**OBSERVED BASIS:** median path 13.6558 versus median maximum excursion 0.5327; mean time fractions forward/reverse 38.34%/38.27%; velocity-direction correlation near −0.858 at 4 s while heading correlation is about 0.979; 92.96% median re-entry into already visited quarter-unit bins. The first 60 s already show balanced motion and short directional persistence. The effect is present in 50 contact-free lives, including 45 never within 0.25 of a fixture. These are passive facts, not a claim that the spontaneous generator alone caused them.

**CURRENT UNCHANGED TEMPORAL VALUES:** separate oscillator periods 7/9 s; sinusoidal amplitude 0.25 per side; filtered-noise amplitude 0.1; noise relaxation 1 s and sign refresh 0.5 s; motor tendency relaxation 0.1 s. Current direct feedback, learned/evoked motor material, regulatory current and attenuation remain part of the final command. None is executed, edited or bypassed here.

**ASSISTANT DESIGN DIRECTION, NOT A FOURTH NUMERICAL CONFIGURATION:** consider a shared persistent common-mode spontaneous drive with a more slowly varying, bounded left/right imbalance. In descriptive coordinates $o_L(t)=c(t)-d(t)$ and $o_R(t)=c(t)+d(t)$, c and d would be endogenous time/random-history processes only. These symbols describe a potential replacement for the **spontaneous component**, not the full command; they do not remove or change the sensory/learned/regulatory inputs or the existing actuator interface. No law, distribution, time constant, amplitude allocation, stochastic seed or implementation is selected now.

| Temporal feature to consider | Why it fits the audit | What must not be assumed or bundled |
|---|---|---|
| Longer correlated locomotor bouts | Current 3.4 s bouts commonly undo each other | Merely lengthening a symmetric oscillation can still retrace; no distance target or forward reward |
| Slow bounded left/right imbalance | Current near-zero command correlation spends similar drive on translation/differential action | Permanent imbalance makes circles; no turn chosen from source or wall truth |
| Broad wandering / occasional spontaneous reorientation | Persistent heading plus repeated reversal retraces local space | Reorientation must arise endogenously, not detect novelty, unvisited cells or a useful bearing |
| Natural low-activity intervals | Current inactive fraction is only ~0.61% under the disclosed kinematic threshold | Rest still consumes basal energy; do not introduce a need-triggered helpful policy or disable consequence |
| Preserve amplitude as an independent dial | The defect candidate is temporal organization, not absent motor activity | Do not increase command magnitude or auto-balance it based on outcomes; matched effort is a future assessment, not a normalization feedback loop |

This would be a **motor-generator mechanism/configuration change requiring separate Jason approval**, even though it supplies no task knowledge. Do not call it apparatus-only or slip it into a nursery configuration hash. P remains fully unchanged in this task and in all three recorded provisional candidates. A later design should choose the fewest temporal changes that address reversals and retracing; the table is a menu of relationships to consider, not instructions to add all features at once.

No source seeking, novelty reward, distance-from-birth reward, unvisited-space detection, target coordinates, semantic EXPLORE action or privileged state is admissible. No opportunity/coverage metric becomes an organism input. Sampling a blind endogenous time process is distinct from steering towards desirable outcomes. Proposed parameters must be justified by bodily time scales and blind movement properties, not selected on learning/survival or cherry-picked source contacts.

**Evidence supports opening the dial, not choosing its value.** No counterfactual motor trajectory, free-world motor ablation, new generator or trained model exists. Lengthening bouts may increase travel, energy cost and collision severity; reorientation could worsen loops; rest may reduce exposure. None of these outcomes is known. Do not remove existing spontaneous structure simply because the present assay has not shown useful development.

### Joint implications for nursery dials

- **Geometry:** greater directional persistence might support wider source spacing and a larger arena, mitigating the 14-unit option's chemical/wall crowding. No larger arena is locked without evidence; the current three layouts remain fixed provisional references.
- **Energy:** persistence does not add energy. B's basal reduction remains a distinct, interpretable proposal, but its 527 s cost proxy cannot be carried over unchanged if command duty/effort changes.
- **Integrity:** more effective translation can increase impact speed/opportunity even in a larger arena. Keep damage and repair measurements; do not preemptively switch to C or increase hazards.
- **Repair:** better travel may improve access but not sustained low-stress holding. The existing 114–130 s favorable half-recovery calculations remain conditional physical facts, not a motor program.
- **Resources:** changed contact frequency makes the old throughput projection uncertain; no hidden allowance extension. Native recording and fidelity remain fixed.

The optional A/B pilot below is **deferred and conditional on Jason choosing to retain the current motor process**. It cannot test a new temporal process or justify reducing arena size if that separate decision remains open. If motor design is selected first, rewrite the later small calibration proposal explicitly; do not run a factorial sweep across world, biology and motor dials.

'''
main=main.replace(marker,motor+marker)
main=main.replace('## 11. Exact decisions needed before any Nursery simulation','## 11. Exact decisions needed before any Nursery simulation\n\n**First, temporal structure:** choose whether to retain the existing motor generator for the first nursery, or authorize a separate narrow design of blind correlated locomotor activity before geometry is frozen. The audit supports the latter design review; it does not choose replacement values or authorize implementation. All decisions below remain pending and conditional on that choice.')
main=main.replace('No nursery, P or field execution;', 'Exploration addendum incorporated. No nursery, P or field execution;')
main=main.replace('## Deliverables and custody',f'## Exploration audit additions\n\n{link("NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md")} · {link("EXPLORATION_PER_LIFE.csv")} · {link("EXPLORATION_AUDIT_METHODS.md")} · {link("EXPLORATION_AUDIT_RESULTS.json")} · {link("EXPLORATION_SUPPLEMENT.json")}\n\n## Deliverables and custody')
write('NURSERY_0_DESIGN_v0_1.md',main)
proposal=read('NURSERY_CANDIDATE_PROPOSALS.json');proposal['recommended']='N0-B only if Jason freezes current spontaneous motor process; geometry decision deferred pending temporal-structure review';proposal['exploration_addendum']='All three candidate values preserved unchanged; no new motor value or fourth configuration';write('NURSERY_CANDIDATE_PROPOSALS.json',json.dumps(proposal,indent=2))
with (OUT/'CURRENT_WORLD_DEVELOPMENTAL_EVIDENCE.md').open('a',encoding='utf-8') as f:f.write('\n## Exploration addendum\n\nThe new passive native audit materially strengthens temporal-organization as a bottleneck candidate: balanced forward/reverse motion, ~94 reversals per life, 1.6 s velocity-direction correlation first crossing, 92.96% repeated-bin re-entry and the same pattern in 50 contact-free complete lives. Do not infer that arena/source sparsity alone explains the result. '+link('NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md')+'. No P/world/motor change was made.\n')
with (OUT/'LEAN_RUNNER_RESOURCE_ESTIMATE.md').open('a',encoding='utf-8') as f:f.write('\n## Exploration addendum qualification\n\nThese projections and the six-life example assume the unchanged current motor generator and remain conditional, not a proposed immediate launch. If temporal structure is redesigned, motion/contact/effort may change and these rates are only prior planning evidence. The passive exploration audit read 2,547,923 native rows in about 24.23 s on this host; it ran no P or world step. This reading cost does not estimate a replacement generator or a nursery life.\n')
print(json.dumps({'status':'DESIGN_RECOMMENDATION_REVISED','supplement':extra['single_frequency_summary'],'threshold_sensitivity':extra['bout_threshold_sensitivity']},indent=2))
