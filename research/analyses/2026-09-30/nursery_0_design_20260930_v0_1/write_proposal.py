"""Write design documents and a static schematic. No Loom module imports."""
from pathlib import Path
import json, hashlib, csv, math

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
WT=ROOT/'worktrees/loom-p-b1-minimal-20260929'
D=WT/'developmental_ecology'
N=json.loads((OUT/'DESIGN_ARITHMETIC.json').read_text())
REQUEST=Path('C:/Users/Jason/.codex/attachments/01150d9f-0d0a-4462-bdb5-74786477f732/Pasted text.txt')
(OUT/'JASON_REQUEST.txt').write_bytes(REQUEST.read_bytes())
def link(p,label=None):
    p=Path(p);return f'[{label or p.name}](<{p.as_posix()}>)'
def here(name,label=None):return link(OUT/name,label)
def write(name,text): (OUT/name).write_text(text.strip()+'\n',encoding='utf-8')
E=ROOT/'founder_expansion_execution_20260930'
I=ROOT/'impact_integrity_analysis_20260930_v0_1'
evidence=link(E/'FOUNDER_SEARCH_60_LIFE_FINAL_REPORT.md')
fs34=link(E/'analysis/FS034_INTERPRETATION.md')
integrity=link(I/'IMPACT_INTEGRITY_DEVELOPMENT_ANALYSIS_v0_1.md')
physics=link(D/'loom_p/physics.py')
geometry=link(D/'loom_p/geometry.py')
chemistry=link(D/'loom_p/chemistry.py')
config=link(D/'configuration.json')
sources=[REQUEST,ROOT/'AGENTS.md',ROOT/'sources/00_LOOM_CURRENT_STATE(2).md',ROOT/'sources/BASE_WORLD_COMPLETION_v0_1(1).md',ROOT/'research_direction_20260929/JASON_DEVELOPMENTAL_SELECTION_CLARIFICATION.md',
    E/'FOUNDER_SEARCH_60_LIFE_FINAL_REPORT.md',E/'analysis/FS034_INTERPRETATION.md',E/'analysis/ALL_SIXTY_AB.json',E/'INTERRUPTION_NOTE.md',E/'FINAL_DELIVERY_VERIFICATION.json',
    I/'IMPACT_INTEGRITY_DEVELOPMENT_ANALYSIS_v0_1.md',I/'BEHAVIORAL_EPISODES_ENRICHED.csv',I/'DESCRIPTIVE_CLASSIFICATIONS.json',I/'FINAL_VERIFICATION.json',I/'INPUT_CUSTODY.json',
    ROOT/'founder_expansion_packet_20260930/PREPARATION_BOUNDARY_RESOLUTION.json',D/'configuration.json',D/'loom_p/schema.py',D/'loom_p/physics.py',D/'loom_p/geometry.py',D/'loom_p/chemistry.py',D/'loom_p/engine.py',D/'loom_p/prehistory.py',D/'loom_p/neural.py',D/'loom_developmental/core.py',D/'loom_developmental/evidence.py',D/'loom_developmental/runner.py',D/'loom_developmental/verify.py',D/'loom_developmental/replay.py']
for directory in ('founder_initial_execution_20260930','founder_expansion_execution_20260930'):
    sources.extend(sorted((ROOT/directory).glob('FS-*_STOP.json')))
manifest=[dict(path=p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size) for p in sources]
write('SOURCE_MANIFEST.json',json.dumps(dict(purpose='Reference custody only; not an execution authority',sources=manifest),indent=2))

write('CURRENT_WORLD_DEVELOPMENTAL_EVIDENCE.md',f'''
# Current-world developmental evidence for Nursery-0

**OBSERVED EVIDENCE.** Design input only, 2026-09-30. No Founder Search life was rerun, extended, completed retrospectively or replaced. The preserved roster is FS-001–FS-060.

## Denominator and physical opportunity

| Quantity | Verified observation | Interpretation boundary |
|---|---:|---|
| Complete lives | 59, all energy-nonviable | No complete life reached the authorized 600 s ceiling; not a test of infinite viability |
| Incomplete life | FS-060, 124 s durable native prefix; last complete checkpoint 120 s | APPARATUS_INTERRUPTED_UNCLOSED; tail and eventual biological outcome unknown |
| Complete-life age | 428.8747258878284–430.84316626881713 s; median 429.695198 s | Current configuration and these streams only |
| Path length | 12.825890–14.411948; median 13.655804 world units | Accumulated movement, not exploration radius |
| Final displacement from birth | median 0.292394; range 0.023606–1.057205 | Does not describe all intermediate excursions |
| Maximum excursion from birth | median 0.532712; range 0.296971–1.183432 | Strong evidence of local motion despite accumulated path |
| One-unit occupancy bins visited | median 2, range 1–4 | Grid-dependent coverage, not complete traversable-area measure |
| Source contact and positive intake | FS-034 only: 1/60 roster, 1/59 complete endpoints | Do not call this a zero-contact cohort; incomplete FS-060 is not a complete negative |
| Ever within sampled source-surface gap 0.05 / 0.25 / 0.5 / 1 / 2 | 2 / 3 / 8 / 13 / 34 of 59 complete lives | Endpoint near passes, not exact contacts or independent opportunities |
| Nearest sampled source gap over life | median 1.785546; maximum 4.409532 | Most complete lives never came particularly close |
| Recorded damaged lives | 9/60, all in complete subset | Meaningful integrity experience more frequent than energy contact |
| Positive restoration | FS-017 and FS-044 only, tiny quantities | Repair opportunity/dwell remains a concern |

Sources: {evidence}, {fs34}, saved `ALL_SIXTY_AB.json`. This task only summarized their existing quantities; it did not reconstruct P or a physical trajectory. The full roster's selected columns are retained in {here('CURRENT_WORLD_60_LIFE_EVIDENCE.csv')}.

## FS-034: transfer is not positive credit or acquired competence

Source 4 first contacted the body at **331.39646839636504 s**. First positive transfer ended at 331.3999999998436 s; last positive transfer ended at 367.3299999998109 s. Gross intake was exactly **0.0017489243594212861**. Aggregate source-contact duration was **0.6917392033767031 s**. The original ledger records 103 constraint/contact subdivisions and 96 positive-transfer entries; the later impact analysis groups the source contacts into **three behavioral episodes** using its explicit clearance rule. These counts describe different levels, not contradictory numbers of learned experiences.

Physical E rose in 71 of the 96 transfer entries. The eight unique subsequent E-credit handoffs nevertheless remained negative (−0.0017387501254229748 to −0.0014023513719023106), and every one of FS-034's 2,152 E-credit waves was negative. The body-trend law is unchanged: a short local rise is not necessarily a positive smoothed trend. Lifetime expenditure was 0.7017489243594637. The life ended at 430.5252801656493 s. It did not establish a repeated productive developmental sequence or useful energy learning. Source: {fs34}.

For scale only, gross intake was about 0.25% of the 0.7 birth reserve and about 1.07 s of the observed mean no-intake expenditure. This is an accounting comparison, not an extra-life counterfactual. Longer gentle source residence is physically capable of much greater transfer under existing laws; this cohort did not obtain it. No source-uptake increase is justified merely from FS-034's fleeting contact.

## Opportunity and runway inference

**UNRESOLVED INTERPRETATION.** Developmental opportunity is a serious bottleneck candidate. Geometry alone cannot be assumed to solve limited spatial exploration; extra time alone cannot be assumed to break local motion. Source-interface usability, contact duration/control, reserve trends and learned benefit are separate questions. The result does not demonstrate P failure.

Across the 58 complete no-intake lives, mean effort expenditure was **0.000128925605 energy/s**, about **7.91%** of mean total expenditure. Basal cost 0.0015 dominates current depletion. With no intake, basal cost alone imposes a 466.667 s upper bound from E=0.7; all effort makes the bound shorter. This supports considering a basal-runway change before removing the cost of action. It does not establish an optimal basal value.

**JASON-ACCEPTED PRIOR DECISIONS.** Preserve the current-world evidence and the distinction between blank starts, continuing individuals and lineage branches; no externally authored competence. The latest request opens design-only Nursery-0 after the current-world diagnosis. It supersedes the earlier temporary prohibition on preparing a nursery in `JASON_DEVELOPMENTAL_SELECTION_CLARIFICATION.md`; it does not grant execution or selection. First nursery organisms remain intact blank-start P. Prior stage ordering of 600, then potentially 900 and 1,800 s does not authorize any continuation here.

**ASSISTANT/BUILD DESIGN PROPOSALS.** The candidate geometry and biological values in the companion design are untested hypotheses, not Jason-accepted settings or an outcome-dependent rescue of these lives.

## FS-060: separate engineering question

The worker disappeared without traceback, failure receipt or normal closure. Known wall/storage amounts were below declared limits. Root cause is **unresolved**; a general runner defect has not been demonstrated or excluded. See {link(E/'INTERRUPTION_NOTE.md')}. Preserve APPARATUS_INTERRUPTED_UNCLOSED without retry. Before future batches, separately review host/process exit observability and preservation of the last durable boundary. A new nursery is not a repair for that engineering uncertainty.

Frozen evidence identities: P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; lean runner `87abae34e19d4e46234402a6b1ba776814956ec1`; recorded runtime `2fc498951552f53698d70da31f5957e1e208016320c2e27e7dfb20e5e5e7a6ab`. Initial archive SHA-256 `e3377cb965f6801b2e9a53831af6afddffe9814eea7ba78cb1ba71da9fcfbb29`; expansion archive `f184dd2ca6fd98e06a81543a8627b6a3bd7b6a67bdd7d1af410cdd08c7fc2da0`.
''')

write('INTEGRITY_PATHWAY_EVIDENCE_SUMMARY.md',f'''
# Integrity pathway evidence for Nursery-0

**OBSERVED EVIDENCE, with bounded analyst interpretations distinguished below.** This document summarizes {integrity}; no omission test, reconstruction, world or P execution was performed anew.

Exactly nine lives recorded damage: FS-002, FS-010, FS-015, FS-017, FS-032, FS-033, FS-034, FS-038 and FS-044. All nine began with zero I-bank state and formed nonzero I-bank state. Actual records align damage → negative I trend → nonzero eligibility → I-bank updates and reference persistence → later learned-I output → measurable immediate motor/regulatory effect. The prior analysis retained 26 behavioral episodes, 28 temporal bouts and 192 overlapping local omission windows. Solver subdivisions were not treated as independent experiences.

## Different histories must remain different

| Life | Bounded interpretation from prior analysis | Nursery implication, proposed |
|---|---|---|
| FS-002 | POSSIBLE SOFTENING: later individual wall impacts gentler, but later contact rate and aggregate damage higher; mixed I influence | Count avoidance and softening separately; gentle recurrence can still accumulate harm |
| FS-010 | POSSIBLE AVOIDANCE: single early mover injury, later separation; local learned-I directions mixed | Keep post-injury time and mover-relative exposure; do not infer avoidance from no repeated collision alone |
| FS-015 | POSSIBLE SOFTENING: lower later closing speed/damage, all three later approach probes locally less-into; second episode has more total impulse | Preserve survivable repeated mover encounters, not just first-hit success |
| FS-017 | POSSIBLE AVOIDANCE: one repair-surface injury, later near miss and separation; eight nonzero block effects locally less-into | Keep restorative surfaces reachable after deficits and record restoration separately |
| FS-032 | UNRESOLVED: later separation but mostly more-into local signs | Preserve unresolved histories, no forced benefit narrative |
| FS-033 | NO REPEATED OPPORTUNITY for impact adaptation: one mover collision and no later comparable collision | Single injury cannot support a severity-development trend |
| FS-034 | UNRESOLVED: mover impacts worsen, source impacts partly soften, energy transfer also occurs | Separate structure type and E/I consequences |
| FS-038 | REPEATED CONTACT, NO CLEAR CHANGE: second wall impact worse, third near first; later I approach effects more-into | Mixed/adverse outcomes remain in denominator |
| FS-044 | EVIDENCE AGAINST BENEFICIAL ADAPTATION in the observed softening sequence: progressively harder impacts, later I effects more-into | Do not equate active I learning with protective behavior |

These labels are descriptive interpretations from the report, not validated learned causal effects or founder selections. They do not imply that FS-044 refutes all integrity learning.

## Magnitude and recovery matter

The largest cumulative damage was FS-010's **0.01692408689137445**, about 1.69% of full I. Minimum final I across complete lives was **0.9830759131086255**; none died through integrity loss. FS-017 received **5.714258854831914e−7** restoration and FS-044 **8.09877364498001e−8**. The data show that injury reaches regulation, but neither severe crippling nor useful repeated repair was demonstrated in this current ecology.

FS-015's four mover episodes had closing speeds 0.160318 → 0.110824 → 0.011798 → 0.036617 and damage 0.00320636 → 0.00295757 → 0.000235962 → 0.000732337. FS-044's three repair-surface impacts instead rose from 0.017246 to 0.044069 to 0.055109 closing speed. Both patterns matter. FS-002's later equal-time half sustained more total harm despite gentler individual peaks.

## Causal boundary

The prior detached omissions removed learned-I at frozen local receivers while retaining actual other inputs. They established small, signed command/actuator-force effects, not alternative motion or a survival advantage. Peak one-step command differences ranged approximately 3.53e−7 to 1.49e−5 across lives. Small local effects are not proof of zero cumulative influence; they also cannot establish useful accumulated adaptation. Injury-dependent actuator asymmetry, depletion, pose, spontaneous motion and mover phase remain confounds. No beneficial learned causation is established.

## Separate design implications

**JASON-ACCEPTED DESIGN REQUIREMENT:** Nursery-0 must retain both energy and integrity consequences, and favor survivable consequences rather than stronger hazards. This is not an energy-only proposal.

**ASSISTANT PROPOSAL:** increase access to the existing three repair strips by shortening travel scales, retain the mover's speed/size/period, and retain nonzero damage and stress thresholds. Recommend no damage reduction in the first preferred candidate because present harm was small. Offer a separately identified 25% damage-scaling reduction only as the third comparison candidate for the unmeasured higher-contact ecology.

**UNRESOLVED:** whether a denser world creates more repeated *survivable* encounters, whether blank P obtains sustained low-stress repair, and whether any later improvement is caused by learned integrity regulation. More encounters may merely repeat adverse contact. Damage attenuation also attenuates the bodily teaching signal; this is a cost, not an unqualified benefit.

The current repair law needs actual low-stress, low-slip contact under deficit. Algebra gives a best stationary half-deficit recovery time of about **114.25 s** (force about 0.08708), before accounting for imperfect holding. At force 0.05 the half-deficit time is about **129.97 s**. These are favorable conditional calculations, not commands, attainable P policies or simulated results. At proposed basal cost 0.0012, the former costs at least 0.1371 energy while stationary. Repair remains a consequential tradeoff, not passive healing. Source: {physics} and {here('DESIGN_ARITHMETIC.json')}.
''')

main=r'''
# NURSERY_0_DESIGN_v0_1

**DESIGN ONLY — assistant proposal for Jason review, 2026-09-30.** No nursery, P or field execution; no live parameter/configuration change; no launch authority; no canon rewrite; no Git write, push, PR or merge. The preserved Base World and all Founder Search records remain the reference condition.

## Recommendation and decision boundary

Recommend **N0-B — balanced energy runway**, subject to Jason's review and the explicit compatibility work below. Use a 14 × 14 arena, twelve unchanged sources, the three existing-size wall repair strips and the unchanged mover translated to the new centre. Reduce basal cost from 0.0015 to **0.0012**, retaining birth E=0.7, effort cost, damage, integrity-dependent actuation and repair law. The 20% basal reduction is an interpretable proposed step, not an empirically optimized constant.

N0-A provides the same ecology with current biology. N0-C adds only a 25% reduction in damage per impulse to N0-B. **N0-C is not the default:** the present cohort did not suffer integrity death or large deficits. It is a concrete alternative for the concern that denser encounters may consume developmental runway, not an accepted correction to a demonstrated injury bottleneck.

The design targets repeated meaningful **energy and integrity** experience within one continuing life. It does not target a survival percentage, a founder score or useful-learning success. All candidates can miss sources, waste energy, collide, sustain harm and die. None supplies labels, correct actions, navigation, external training or adaptive lessons.

## 1. Evidence and status of claims

**OBSERVED EVIDENCE.** The fixed 60-life roster contains 59 complete energy-terminal lives at 428.875–430.843 s and FS-060's unclosed 124 s prefix. Only FS-034 contacted an energy source: gross intake 0.0017489243594212861, 0.6917392033767031 s aggregate contact, all eight subsequent relevant E-credit handoffs still negative. No repeated productive energy-development sequence or useful energy learning was established. This is **not P failure**. See @CURRENT@ and @FINAL@.

Median total path was 13.6558, but median maximum excursion from birth only 0.5327 and median final displacement 0.2924. Thirteen of 59 complete lives passed within one body diameter of a source surface; only eight within half a diameter. Multiplying source density by three does not imply three times the encounter rate, and 100 more seconds do not imply wide exploration. Locality is a material unresolved limitation.

Nine lives formed I-bank state following actual damage and later expressed learned-I output with measurable local motor effects. FS-015 supplies a possible-softening candidate; FS-017 a possible-avoidance candidate. FS-002/010 are mixed; FS-038 is mixed/adverse; FS-044's repeated impacts worsen. Beneficial learned causation is not established. Maximum cumulative damage was only 0.0169241; all complete lives finished above I=0.983. See @INTEGRITY@ and @IREPORT@.

**JASON-ACCEPTED PRIOR DECISIONS.** Preserve this evidence; Nursery-0 is a separate revisable ecology. Blank starts remain intact P without external competence. Energy and integrity remain separate bodily consequences. Existing source/material/chemical laws remain initially; hazards must remain consequential and avoidable. Legitimately acquired continuation and lineage branching remain possible later, under separate authority. The present request authorizes proposals only. Earlier “no nursery yet” instructions in the developmental-selection clarification are superseded only to this design extent. Historical `00_LOOM_CURRENT_STATE(2).md` is dated September 4/5, not evidence of today's execution state.

**ASSISTANT/BUILD DESIGN PROPOSALS.** Every revised number and arrangement below is new, untested and reversible by choosing another *future* fixed configuration. It must never be retroactively changed within a life or applied to current-world records.

**UNRESOLVED INTERPRETATIONS.** Opportunity is a serious bottleneck candidate, not the sole established cause. Positive energy trends, informative chemical differences, repeated repair and beneficial learning in the proposed geometry remain unverified. Nothing here reinterprets the existing B1 or Founder Search evidence as a stronger result.

## 2. Shared ecology: explicit geometry and opportunity comparison

World distances are in existing world units; body diameter is 1. No body/source/mover size is rescaled. The three candidates share exactly the same geometry so A/B/C differences remain interpretable.

| Dial | Preserved current value | Proposed A/B/C value | Reason, confidence and reversibility |
|---|---|---|---|
| Square side | 20 | **14** | 30% shorter linear scale; leaves an ordinary bypass around the unchanged 10-unit swept mover length. Geometric fit high confidence, developmental gain unknown. Separate future ecology only |
| Nominal area | 400 | **196**, 0.49× | Area reduction is geometry, not altered physics |
| Source count | 8 | **12** | Modest absolute addition plus contraction; not source everywhere. Count is a proposal, not fitted to a life; reverse before a new fixed configuration |
| Nominal density | 0.020000 | **0.0612245**, 3.06122× | Report count/nominal area, never an encounter probability |
| Static body-centre accessible area | 332.406620 | **127.840250**, 0.38459× | Excludes walls, body-inflated static sources/repair; mover handled separately |
| Sources/static accessible area | 0.0240669 | **0.0938672**, 3.90026× | Accounts for finite body size; denser than nominal ratio suggests |
| Instantaneous body-centre accessible area | 326.621222 | **122.054851** | Subtract the inflated mover at its actual pose; no obstacle overlap at any phase |
| Conservative always-clear area | 310.621222 | **106.054851** | Excludes all mover-swept positions only to show bypass availability; crossing space is not permanently occupied |
| Static free ground area, before body inflation | 390.716815 | **183.575222** | Distinct from body-centre accessibility; instantaneous free ground is 181.575222 with mover |
| Repair strips | 3, each 4 long × 0.25 deep, on left/right/top walls | **Same three dimensions**, translated with arena | Retain real restoration opportunity; no new repair material or freestanding lesson object |
| Repair frontage | 12 main-face units, 15% of perimeter | **12**, 21.43% of perimeter | Full exposed length including short ends remains 13.5. Greater availability per area; not faster healing |
| Mover | centre (10,10), amplitude 4, period 30 s, size 2 × 1 | **Centre (7,7) only**; other values unchanged | Recurs between useful source rows without guarding the only route; maximum speed stays 0.837758 |
| Numerical field grid | 80 × 80, cell side 0.25 | **56 × 56, cell side 0.25** | Domain-matched numerical grid, not a diffusion/sensor change or fidelity reduction. Must be separately verified |

Current values come from @CONFIG@ and @GEOMETRY@ at runner checkpoint `87abae34e19d4e46234402a6b1ba776814956ec1`. Proposed values are selected for simple, reviewable geometry and retained bypass margins; none is claimed optimal. Exact arithmetic is in @ARITHMETIC@.

### Placement rule, independent of organism outcomes

Twelve identical radius-0.5 sources occupy the Cartesian product:

- $x\in\{2.5,7,11.5\}$;
- $y\in\{2,4.5,9.5,12\}$.

Index them row-major, increasing y then increasing x; indices are private record identities, not sensory labels. This fixed lattice is selected from geometry alone. It is not translated, rotated, shuffled or searched to match a successful trajectory or birth. No extra obstacle is introduced.

Repair rectangles use `[x_min,x_max,y_min,y_max]`:

- `[0,0.25,5,9]`;
- `[13.75,14,5,9]`;
- `[5,9,13.75,14]`.

The mover remains $x=7+4\sin(2\pi t/30+\phi)$, $y=7$. Its physical swept rectangle is `[2,12] × [6.5,7.5]`. Its initial phase is the existing independently indexed life draw, **not chosen for safety or success**. Initial phase values, seeds and life IDs are not allocated in this design.

Births retain the existing uniform rejection law over the body-centre square, requiring minimum surface clearance **0.25** from every actual fixture at the sampled birth phase. Orientation remains uniform. Birth velocities/commands are zero, I=1, E as in the candidate table; all learned state starts blank under the existing initialization. Do not condition births on source distance, bearing, future encounter, chemical strength or survival. Food is not put in front of the organism.

![Static proposed nursery geometry. No birth, phase selection or simulated path.](<@SCHEMATIC@>)

### Space for different behavior

Adjacent source-centre spacing is 2.5 vertically and 4.5 horizontally. After inflating both sources by body radius, the corresponding passage widths are **0.5 and 2.5**, respectively. These are traversable geometrical openings, not promised control accuracy. Larger open columns coexist with the narrower source-row gaps.

There are always-clear horizontal centre lines at **y=5.75 and 8.25**, x=1…13, and vertical bypass lines **x=1 and 13** linking them. Their minimum surface clearance from the whole mover sweep, all sources, wall and repair geometry is at least **0.25**. These lines demonstrate available routes; they are not supplied to P or used as controllers. For example, a body centred at (7,7) conflicts with the mover near centre phase but is clear when the mover is at an endpoint. Waiting and timed crossing therefore remain distinct possibilities from the longer always-clear detour. The swept region is not treated as a permanent obstacle in dynamics or opportunity measures.

The proposed layout retains approach, retreat, turning away, wall following, low-stress contact, source departure, travel between sources and revisits. It does not force every path through a hazard or source. Sources never overlap the mover at any phase; repair strips stay separate. Circle body orientation does not enlarge its geometric envelope. The narrowest illustrative paths still need future implementation-level geometry checks before use as evidence of apparatus access.

### Static proximity, not a promised nursery result

Deterministic midpoint quadrature over admissible birth positions and 16 equally spaced phases gives about **23.55%** within source surface gap 0.5, versus **5.90%** for the Base World; within gap 1.0, about **65.36%** versus **20.92%**. Mean-of-phase median nearest gap is about **0.800** versus **1.872**. Coarser 0.05-unit quadrature gives 23.35%/5.85% and 65.18%/20.85%; finer cell width is 0.025. These are phase-grid descriptive approximations with no random births drawn and no simulation, not confidence intervals or target percentages.

This makes local source experience more plausible given the observed 0.533 median excursion, without guaranteeing contact or recurrence. Roughly three quarters of admissible proposed births are still more than 0.5 from source contact. Repeated experience is the question for later observation, not a condition used to select births.

## 3. Three concrete configurations

All omitted baseline values remain numerically and functionally unchanged, including P widths/pools/learning/association/motor rules, source capacity/uptake/renewal, sensory transduction, native/wave/field cadence and viability boundaries. @CANDIDATES@ records explicit proposal deltas and unchanged key values; it is not a loadable launch configuration or authority.

| Runway dial | N0-A: ecology-only | N0-B: balanced runway **recommended** | N0-C: energy + integrity resilience |
|---|---|---|---|
| Shared ecology | Above | Identical | Identical |
| Birth E / I | **0.7 / 1 unchanged** | **0.7 / 1 unchanged** | **0.7 / 1 unchanged** |
| Basal cost per s | **0.0015 unchanged** | **0.0012 proposed**, −20% | **0.0012 proposed**, same as B |
| Effort cost per s | **0.001 × (abs(uL)+abs(uR))/2 unchanged** | Same | Same |
| Damage per impulse | **0.02 unchanged** | **0.02 unchanged** | **0.015 proposed**, −25% |
| Sustained-stress threshold | **0.25 unchanged** | Same | Same |
| Graded low-I capability | **Unchanged asymmetric gains** | Same | Same |
| Repair rate | **0.02 unchanged**, existing quality/deficit law | Same | Same |
| Exchange force/speed scales | **0.1 / 0.25 unchanged** | Same | Same |
| Death boundary | **E≤0 or I≤0**, existing exact crossing | Same | Same |
| No-intake basal-only upper bound | 466.667 s | 583.333 s | 583.333 s |
| Illustrative lifespan holding observed mean effort expenditure fixed | 429.731 s | 526.741 s | 526.741 s |

The last row is a scalar proxy, **not a prediction or an executed life**. In a nursery, contact, learning, E-dependent force, I-dependent asymmetry and expenditure all change. B/C buy about 97 s (22.6%) in this proxy. No candidate promises 600 s survival; an eventual 600 s administrative ceiling is not a biological target.

## 4. Resilience dials examined separately

### Birth reserve — retain 0.7 for the first comparison

Birth E is a provisional implementation number, not sacred biology. Raising it would buy reserve, but would also increase initial force through $(0.2+0.8E)$, reduce uptake headroom through $(1-E)$ and change direct need/interoceptive drive from birth. That is a broader initial-condition intervention than lowering ongoing basal drain. Retain non-maximal 0.7 to keep these initial conditions interpretable across A/B/C. No revised birth-reserve value is recommended now. Confidence: high in these code relationships, low that 0.7 is developmentally optimal. Future revision remains available with a new explicit configuration.

### Basal expenditure — propose 0.0012 in B/C

This changes passive energy loss per physical second and hence the reserve history experienced by unchanged P. The 58 no-intake complete lives spent on average 0.000128926/s on effort; basal expenditure accounts for about 92.09% of average cost. Eliminating effort altogether could only reach the 466.667 s basal bound, so it would not buy comparable time and would remove a useful action cost.

The proposed reduction is a round **one-fifth** intervention, justified as a modest first comparison rather than fitted to a required survival time. It adds about 97 s in the unchanged-average-effort proxy, enough time to make later encounters more plausible without removing need. Zero-command energy still falls at 0.0012/s. No-intake death remains inevitable before 583.333 s. Confidence: high in scalar accounting, moderate/low in developmental utility. Reversible only between separately fixed configurations.

Risk: lowering basal cost makes all sources relatively more generous, prolongs residual motion and changes later drive/force. It could make a resource circuit easier than intended. It does not merely “add a timer.” Record this as a biology/environment-coupling change while keeping the P algorithm frozen.

### Actuation-effort cost — retain the existing magnitude and relationship

The absolute paired-command cost continues even when pushing against a wall or at low achieved speed: expenditure follows attempted effort, not displacement or mechanical work. Retaining 0.001 preserves that tradeoff. Its small contribution in this cohort does not prove it will remain small in a contact-rich nursery. No retuning to make a chosen command cheap, and no automatic balancing with basal cost. Confidence: strong implementation basis; developmental sufficiency unresolved.

### Integrity damage and stress tolerance — C changes one scalar only

Instant damage remains $\Delta I=-k_J\sum J$. Sustained damage remains $-k_J\sum\max(J-F_*\Delta t,0)$ with $F_*=0.25$. In C only, $k_J$ changes from 0.02 to **0.015**. For identical recorded mechanical impulses this would yield 25% less I loss and 4/3 as much cumulative impulse tolerance in the simple impact-only calculation. It does **not** promise 4/3 lifetime because trajectories, stress, restoration and E remain coupled.

The motivation is precaution about greater contact density, not a present integrity-death observation. Current worst I loss was 1.69%; therefore C has lower evidential support than B. The proposed quarter-step is a transparent assistant choice, not an estimated biological constant. Damage, negative I trends, mechanical capability loss and integrity death remain possible. Mover speed, collision impulse mechanics and force threshold do not change.

Risk: smaller damage also weakens the bodily learning consequence, and may reward careless contact by making it too cheap. More surviving encounters need not improve learning. C must not be automatically activated after a bad life. Raising the stress threshold is deliberately not bundled: it would also expand the repair-quality window and change what counts as damaging sustained pressure. Confidence in accounting: high; need for change: low. Reversible for new configurations only.

### Graded capability loss — examined, not changed

Current paired force is $0.5(0.2+0.8E)(0.4+0.6I)u_L$ on the left and $0.5(0.2+0.8E)(0.7+0.3I)u_R$ on the right. At I=0.5 the I factors remain 0.70 and 0.85; at the worst observed final I they remain about 0.98985 and 0.99492. There is no I-driven sensor blackout in current transduction. Low-I organisms retain graded sensing and actuation until genuine nonviability, although asymmetry can impair navigation.

Slower capability loss could preserve recovery motion under severe deficits, but current lives do not establish such crippling; changing the asymmetry could also remove a relevant embodied consequence. All three candidates retain the relationship. C's smaller damage indirectly preserves capability without a second actuator-law change. Confidence: high in formulas, low in unobserved severely damaged operation. A later low-I recovery question must not be answered by assuming these mild-injury records cover it.

### Repair effectiveness — retain rate and usable-stress relationship initially

Repair remains wall-mediated, non-depleting and dependent on actual deficit and gentle low-slip residence; no automatic healing. The favorable stationary half-deficit time is approximately 114.25 s, and about 129.97 s at force 0.05. Current repair contacts were fleeting and restoration tiny; this supports access/dwell as a concern before claiming the rate itself inadequate. Existing strips become more accessible per area without increasing their count, length, emission or healing rate.

Risk of keeping the rate: blank P may never sustain contact long enough for usable recovery. Risk of increasing it: short accidental touches could erase harm and undermine the integrity pathway. B's extra runway and geometry give the unchanged rate an interpretable first comparison. This is not a finding that current repair is sufficient. Future evidence must separate reaching repair, eligible dwell, actual restoration and energy left to leave.

## 5. Sources and chemical crowding: explicit nontriviality checks

All candidates retain radius 0.5, capacity **0.2/source**, renewal time **400 s**, uptake coefficient **0.04**, exchange force scale **0.1** and relative-speed scale **0.25**. Initial sources are full. Source inventory rises from **1.6 to 2.4** total energy and maximum instantaneous summed renewal from **0.004 to 0.006/s** because there are more sources. This is a real abundance change, not merely moving the same energy closer.

For a favorable stationary single-source contact, gross uptake is $0.04(S/0.2)(1-E)q$, $q=F/(F+0.1)/(1+(v_{rel}/0.25)^2)$. At E=0.7, full stock and F=0.05 with no relative motion, gross rate is 0.004/s, above either basal rate before effort. Existing uptake can therefore produce positive physical consequences under sustained contact. This algebra does not establish a reachable P hold or positive smoothed credit. Repeated positive **and negative** E-credit opportunities must be observed, not manufactured by changing the credit rule.

A single exhausted source renews at at most 0.0005/s, below B/C's basal 0.0012 even with zero effort. Over an arbitrarily long interval its transfer cannot exceed initial stock plus 0.0005 times duration. Thus permanent parking on one source cannot support this organism indefinitely. Several sources in rotation have enough combined renewal in principle to support life; that is desirable for organized behavior and a **risk** if undirected motion obtains it too easily. Neither this algebra nor a finite pilot proves random motion cannot survive indefinitely.

Chemical emissions, mixed receptors, diffusion 0.5/0.025, decay 0.02, solid transport effects, no-flux boundary and open directional-light boundary remain unchanged. The medium diffusion-length scale $\sqrt{D/\lambda}=5$ exceeds the nearest new source spacing, so overlapping plumes are a material concern.

Using only total-emission/mass-balance arithmetic for the existing 600 s full-stock, zero-initial-field preparation, global mean concentrations change from approximately **(0.05469, 0.03156)** to **(0.16263, 0.08992)**. Applying the existing receptor law to the *uniform-field approximation* at those means gives **(0.585, 0.541)** versus **(0.806, 0.774)**. The receptor slope at mean mixed input is about 4.1–4.6 times smaller in the proposal. These are not local field solutions, average receptor measurements or predictions of directional information. Exact field mass is independent of phase under this full-stock preparation, but gradients are not.

This is the main ecological risk to resolve before interpreting nursery outcomes. After separately authorized lawful preparation, inspect raw bilateral differences and spatial ranges over fixed admissible positions/headings/phases, not just mean signal. Do not increase chemistry, sensor gain or P association strength to compensate. If geometry creates largely uninformative chemical input, return to Jason with that physical finding; do not silently substitute a fourth layout or tune outcomes.

## 6. Candidate risk comparison

Ratings below are reasoned concerns, not measured probabilities. Geometry-related risks are shared because the layouts are identical.

| Risk | N0-A | N0-B | N0-C | Observation that matters later |
|---|---|---|---|---|
| Too sparse | Still material: local motion persists | Same spatial gaps; more time | Same as B | No/late first productive contact; no recurrence; all nonencounters retained |
| Too easy | Higher source inventory/density | Greater risk from cheaper maintenance | B plus cheaper harm | Incidental sustained intake, effortless cycling, little depletion or departure pressure |
| Too damaging | Denser walls/contacts; current severity | More time also permits more accumulated harm | 25% less loss per impulse, not harmless | Injury-caused death/crippling, damage before useful energy, post-injury viable time |
| Too safe | No severity reduction; most space remains avoidable | Same severity | Greatest concern: weak I consequence | Actual I trends and restoration, not contact counts alone |
| Indefinite random survival | Cannot exclude multi-source support | Increased risk | Increased risk plus damage tolerance | Bounded energy/stock budgets and recurrence; finite survival is not proof either way |
| Chemical crowding/saturation | Shared major concern | Same physical emission/receptors, later stock history differs | Same | Fixed-position raw contrasts and admitted signal ranges; no signal tuning |
| Forced trajectories | Retained bypasses, but some 0.5-wide centre passages | Same | Same | Connected finite-body free space, source access and retreat independent of mover timing |

No combined risk score or survival/learning pass percentage is proposed. N0-B balances stronger evidence for energy runway with the weaker evidence for needing damage attenuation. N0-A remains the smallest biological intervention. N0-C addresses a plausible future hazard-density problem at the cost of weaker integrity consequence.

## 7. Separate opportunity measures for future use

These are proposed observer measures; no value feeds into P. Keep full fixed denominators, including nonencounter, injury, failure and censoring. Report per life, with distributions and event-aligned sequences, not one success number.

**Energy:** first source contact and first positive transfer times separately; total gross transfer and net reserve changes; independent productive encounter count; departure/revisit; same-source versus different-source recurrence; stocks on arrival/departure; time/energy between encounters; positive and negative actual E-credit handoffs; viable time after first useful encounter. Report source contact duration and transfer subdivisions without calling them separate experiences. Define a useful physical transfer descriptively by actual energy delivered; do not require a preselected learned result.

**Integrity:** survivable damaging episode count, damage magnitude, impulse and sustained force separately; comparable-structure re-encounters with normal/tangential speed; encounter rates relative to opportunity and path; negative/positive I-credit handoffs; post-damage viable time and actuator capability; later avoidance versus softer impacts separately; repair-surface access under deficit, eligible residence, actual restoration, and energy remaining afterwards. No impact is automatically a failure or a lesson. Single-contact lives cannot establish repeated softening.

**Exploration:** path length, displacement, maximum excursion, one-unit occupancy bins and visited accessible-area fraction; source/mover/wall/repair exposure; phase-specific mover clearance; available approach/retreat/bypass choices. Keep actual motion separate from static path availability. Longer life and more path are not sufficient developmental evidence.

For comparability, retain the prior primary behavioral episode rule: same collider, at least 0.1 s without recorded contact and intervening sampled surface clearance >0.05 before counting a new episode; retain 0.01/0.10 clearance sensitivity. Apply the same rule to source departure/revisit accounting and keep solver events underneath it. Define all observer rules before an authorized batch; do not select successful histories first.

## 8. Optional small opportunity calibration — proposed, not executed

A small pilot materially helps distinguish A's ecology-only benefit from B's extra runway and detect gross chemical/contact crowding. Propose **three independently drawn blank-start stream pairs, A and B: six lives maximum**, each to genuine nonviability or **600 s total age** or a declared apparatus/resource stop. Pair each geometry/phase/birth/anatomy/spontaneous-stream identity across A/B, with the candidate basal value explicitly different. Do not claim byte-identical complete state/configuration. No C life is included in this optional pilot; Jason may choose C for separate review instead, but there is no automatic escalation.

Use the unchanged intact newborn P initialization and spontaneous process, with ordinary within-life learning present. There is no hand-designed controller, learning freeze, new noise process or externally authored behavior. The pilot is **engineering opportunity calibration**, not an efficacy assay, founder search or test of whether P learns. Its use of intact P also means it does not isolate “random motion alone.” Assess only the separate physical opportunities above and predeclared raw-signal availability. Do not use learned weights, adaptation scores, useful behavior or survival ranking to tune the nursery. End all declared cases before reviewing differences; no retry, replacement, seed screening or outcome-dependent stop/extension.

Three pairs are too few for a target contact probability or rare-event assurance. They may expose gross starvation/contact crowding or lack of repair access, and may remain inconclusive. A life alive at 600 s is administratively censored, not proof of indefinite support. Evidence that an unorganized process supports itself indefinitely cannot be established by this finite intact-P pilot; keep that concern unresolved rather than inventing a random-motion control here.

Jason can decline this pilot and approve a later fixed nursery preparation instead. Neither option is authorized by this document. A fixed pilot roster, exact unused stream IDs/order, newborn snapshots, runtime, resources and stopping rules would need a later reviewed packet and fresh authorities. None is created now. The 900/1,800 s developmental stages remain later review questions; no continuation is prepared.

## 9. Implementation compatibility and lawful preparation — future work only

All proposed biological values are already configuration fields. The chosen source layout passes analytical nonoverlap/route checks, but the current apparatus is **not directly nursery-ready**:

1. `loom_developmental/runner.py::validate_grant` binds `e.c.identity()` to the existing `CONFIG`; any nursery change is correctly rejected. A future narrow apparatus change must bind the separately approved nursery configuration exactly, retaining the frozen P code check and explicit case/state/runtime authorization. Do not remove the guard globally or overwrite the Base World's commissioning contract.
2. `loom_developmental/evidence.py::NATIVE_FIELDS` fixes `stocks` width at **8**. Twelve stocks would shift the following raw/mover/diagnostic fields and fail the current row allocation/verification. Future schema work must bind source-count-dependent offsets in recording, `verify.py`, `replay.py` and passive readers. Four extra float64 stock entries cost 32 uncompressed bytes/native step, about **1.92 MB per 600 s**, before event/checkpoint effects. Preserve old eight-source artifacts and their original reader/schema; no reinterpretation of old columns.
3. A 14-unit domain requires 56 cells to retain 0.25 cell width. Reusing 80 would refine resolution while coupling a numerical change to ecology; using fewer than 56 would coarsen it. The proposed 56 is geometric bookkeeping, with a new field identity and necessary solver/area checks, not assumed equivalence to the old field.
4. Existing 20-unit/eight-source prehistory is **incompatible** with the new geometry and cannot be cropped, rescaled, reused or silently regenerated. Future explicit preparation would retain the reviewed **600 s body-absent full-stock history**, 60,000 native 0.01 s steps from −600 to 0, exact joint mover phase and recorded numerical diagnostics. No P exists during that preparation. A/B/C have identical field-law parameters, so reuse across a matched phase/stream pair is lawful only after exact dependency/hash checks; basal/damage do not enter the body-absent field law.
5. Future checks should cover manufactured 12-stock row round trips and offset rejection, old eight-stock compatibility, exact configuration rejection, 56-grid field mass/geometry consistency, no overlapping solids at all mover extremes/intermediate extrema, finite-body source/repair access, blank-state custody, unchanged 0.01/0.2 s scheduling, and an explicitly authorized bounded equivalence/resource check if required. No such tests that execute P/fields/world ran in this design task.

Sources: @RUNNER@, @RECORDER@, @VERIFY@, @REPLAY@ and @PREHISTORY@. This is an implementation requirement list, not permission to patch. Frozen P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; a future nursery apparatus checkpoint/runtime identity will differ and must be reviewed. The old runner checkpoint and Base World stay preserved.

FS-060 is separately **APPARATUS_INTERRUPTED_UNCLOSED**. Its worker failure cause is unresolved, despite recorded resources below limits. Review process supervision/exit observability as a separate engineering question before trusting a new unattended batch. Do not retry FS-060 or change biology in response to the missing receipt. @INTERRUPTION@

## 10. Lean-runner resource estimate

This estimate uses all 59 closed current-world receipts, not the old dense-recording commissioning runtime. Median active wall/simulated second was **0.34784**; observed range **0.31794–1.04965**. FS-025 is the slow outlier (451.07 wall s for 429.73 simulated s), retained without inventing its cause. Median primary storage was **75,636 bytes/simulated s**, range **72,782–94,613**. Forty-eight time-zero preparations took **5,808.44 s**, mean **121.01 s each**. Details are in @RESOURCE@.

| Hypothetical workload | Median-rate planning estimate | Range if current observed rates persisted | Proposed planning reserve, not permission |
|---|---|---|---|
| One life to 600 s | 209 active wall s; 45.38 MB base evidence | 191–630 s; 43.67–56.77 MB | 1,260 active wall s and 120 MB including closure margin |
| Optional six-life A/B pilot, execution only | 1,252 s (~21 min); 272 MB | 1,145–3,779 s (~19–63 min); 262–341 MB | 7,560 active wall s and 720 MB |
| Three reusable matched-phase preparations | 363 s (~6 min) from historical mean | No measured nursery range | 726 active wall s total for planning; explicit bounded preparation review required |

Add the proposed 12-stock rows (~11.52 MB uncompressed over all six 600 s lives), larger event ledgers if contact becomes common, immutable identities, snapshots, post-run validation and one separately planned archive. Reserve **about 1 GB working space plus up to 1 GB for one archive** for the six-life example. No speedup from the smaller grid or archive compression credit is assumed. More contacts can make physics slower despite fewer field cells. The historical worst-rate doubled wall reserve is a transparent provisional margin, not a measured upper bound or automatically renewable allowance.

Saved-store verification for the expansion used about 477.7 s for 47 closed lives plus the censored-store handling (~10.1 s per complete-life equivalent); linear scaling to six 600 s lives is roughly 85 s, with **10 min** proposed passive validation/report reserve. Full saved-input P reconstruction/deep omissions are neither needed nor included in this opportunity pilot budget. They would require separate scope/resource review.

Together the six-case median projection is about **28–30 min** including preparation/basic validation; current worst-throughput extrapolation plus mean preparation is roughly **70 min**, before richer contacts. The separate proposed administrative reserves total about **2.5 h** (7,560+726+600 s), plus any independently approved engineering implementation/test work. These are estimates for Jason's review, not issued limits, launch grants or a claim that the existing runner can execute twelve-source rows.

Use unchanged Tier-1 lossless native physical/raw/command/RNG evidence, actual wave outputs, all events and complete checkpoints. No live deep diagnostics, scoring, rendering or plotting. Source count/schema extension must preserve fidelity. Resource cutoff, scientific nonviability and apparatus failure remain separate; no automatic retry/continuation. If a resource envelope is inadequate, stop and report the boundary.

## 11. Exact decisions needed before any Nursery simulation

1. **Ecology:** accept or revise the single explicit 14 × 14 / twelve-source layout, three repair strips and centred unchanged mover. This also accepts the change in total stock/renewal and the identified chemical crowding risk; no hidden placement search.
2. **Biology:** select A, B or C. Recommendation B means accepting basal **0.0012 only**, with birth E, effort, damage, stress, capability and repair unchanged. C would additionally require express acceptance of **0.015 damage/impulse**. No bundled easy-mode switch.
3. **Apparatus work:** separately authorize a narrow nursery configuration/evidence-schema implementation and its bounded checks; decide how FS-060's unresolved worker termination will be investigated/contained independently. Approving this design is not authority to edit or test the runner.
4. **Preparation:** separately authorize new lawful geometry-specific body-absent prehistories and blank snapshots, with exact stream identities and bounded wall/storage allowance. Current Base World prehistory cannot supply these.
5. **First use:** accept/decline the optional three-pair A/B opportunity pilot, or specify the next fixed nursery cohort design. Agree its roster/order, intact blank-start process, separate observer measures and 600 s ceiling. No target success percentage, founder selection or 900/1,800 s extension is implicit.
6. **Execution:** after review of the new apparatus checkpoint, configuration, static/signal compatibility, matched-state records and resource plan, explicitly authorize exact fresh launch objects. No such objects exist in this delivery. Decide the planned archive and passive analysis bounds in that later packet.

Any geometry or biology revision goes into a new design version before new preparation. No existing trajectory, Base World file or lineage is rewritten. If chemistry or physical access is problematic, return to review; do not alter P, uptake, chemistry, motor rules or sensors to obtain a better outcome.

## Deliverables and custody

@CURRENT@ · @INTEGRITY@ · @CANDIDATES@ · @ARITHMETIC@ · @RESOURCE@ · @MANIFEST@ · @VERIFICATION@.

The JSON candidate records are labelled **DESIGN_PROPOSAL_NOT_EXECUTABLE**, contain no starts, seeds, grants, approval notices or launch hashes, and are not accepted by the current runner. The static drawing and geometry quadrature contain no organism, learned state or trajectory. All computations in this task are saved-summary statistics, scalar accounting or static geometry. **Zero P, world, field or prehistory execution; zero launch authorities; no parameter application, canon change, founder selection or Git writes. Stop for Jason review.**
'''
replacements={
'@CURRENT@':here('CURRENT_WORLD_DEVELOPMENTAL_EVIDENCE.md'),'@FINAL@':evidence,'@INTEGRITY@':here('INTEGRITY_PATHWAY_EVIDENCE_SUMMARY.md'),'@IREPORT@':integrity,
'@CONFIG@':config,'@GEOMETRY@':geometry,'@ARITHMETIC@':here('DESIGN_ARITHMETIC.json'),'@CANDIDATES@':here('NURSERY_CANDIDATE_PROPOSALS.json'),
'@SCHEMATIC@':(OUT/'NURSERY_0_STATIC_LAYOUT.svg').as_posix(),'@RUNNER@':link(D/'loom_developmental/runner.py'),'@RECORDER@':link(D/'loom_developmental/evidence.py'),
'@VERIFY@':link(D/'loom_developmental/verify.py'),'@REPLAY@':link(D/'loom_developmental/replay.py'),'@PREHISTORY@':link(D/'loom_p/prehistory.py'),'@INTERRUPTION@':link(E/'INTERRUPTION_NOTE.md'),
'@RESOURCE@':here('LEAN_RUNNER_RESOURCE_ESTIMATE.md'),'@MANIFEST@':here('SOURCE_MANIFEST.json'),'@VERIFICATION@':here('DESIGN_ONLY_VERIFICATION.json')}
for a,b in replacements.items():main=main.replace(a,b)
write('NURSERY_0_DESIGN_v0_1.md',main)

base=json.loads((D/'configuration.json').read_text())
shared=N['proposal_geometry']
records=[]
for name,changes,reason in [('N0-A',{},'Ecology-only comparison; current biology retained'),('N0-B',{'basal_cost':.0012},'Proposed 20% lower maintenance cost; preferred interpretable runway intervention'),('N0-C',{'basal_cost':.0012,'damage_per_impulse':.015},'Same energy runway plus proposed 25% lower I loss per impulse; lower evidence support')]:
    vals=shared|changes
    records.append(dict(candidate=name,status='DESIGN_PROPOSAL_NOT_EXECUTABLE',reason=reason,ecology_shared=True,proposed_differences=[dict(field=k,current=base[k],proposed=v,provenance='Assistant design choice in NURSERY_0_DESIGN_v0_1; not applied',confidence='Geometry/accounting explicit; developmental effect untested',reversibility='Only between separately fixed future configurations') for k,v in vals.items()],
        unchanged_key_values={k:base[k] for k in ('body_radius','body_mass','body_inertia','lever','linear_drag','angular_drag','source_radius','source_capacity','source_tau','uptake_rate','birth_energy','effort_cost','stress_threshold','repair_rate','exchange_force_scale','exchange_speed_scale','mover_amplitude','mover_period','mover_size','medium_diffusion','solid_diffusion','chemical_decay','prehistory_seconds','native_dt','wave_dt','illumination_boundary')},
        basal_cost=changes.get('basal_cost',base['basal_cost']),damage_per_impulse=changes.get('damage_per_impulse',base['damage_per_impulse']),birth_integrity=1.,actuator_integrity_factors=['0.4+0.6*I','0.7+0.3*I'],all_other_baseline_values='Unchanged',launch_permission=False))
write('NURSERY_CANDIDATE_PROPOSALS.json',json.dumps(dict(status='DESIGN_PROPOSAL_NOT_EXECUTABLE',base_configuration_file_sha256=hashlib.sha256((D/'configuration.json').read_bytes()).hexdigest(),recommended='N0-B',candidates=records,no_seeds_or_starts_prepared=True,no_launch_authorities_created=True),indent=2))

r=N['resources']
write('LEAN_RUNNER_RESOURCE_ESTIMATE.md',f'''
# Lean-runner resource estimate — design only

Basis: all 59 authentic closed `FS-xxx_STOP.json` receipts listed in {here('SOURCE_MANIFEST.json')}; unclosed FS-060 excluded from full-life rates, never treated as free/zero-cost execution. Preparation basis is `PREPARATION_BOUNDARY_RESOLUTION.json` (48 completed body-absent preparations, 5808.444936249638 s). No benchmark was run now.

| Rate | Minimum | Median | Maximum |
|---|---:|---:|---:|
| Active wall seconds / simulated second | {r['wall_s_per_simulated_s']['minimum']:.9f} | {r['wall_s_per_simulated_s']['median']:.9f} | {r['wall_s_per_simulated_s']['maximum']:.9f} |
| Primary bytes / simulated second | {r['bytes_per_simulated_s']['minimum']:.3f} | {r['bytes_per_simulated_s']['median']:.3f} | {r['bytes_per_simulated_s']['maximum']:.3f} |
| Per-600-s wall projection | 190.763 | 208.703 | 629.791 |
| Per-600-s evidence projection, decimal MB | 43.669 | 45.381 | 56.768 |

These are old-layout rates extrapolated to full 600 s. No nursery speedup assumed; no early biological death used to discount the budget. The slowest completed life is FS-025; its cause is not diagnosed here. New twelve-source rows add four float64 stocks: 32 bytes/native step, 1.92 MB/600 s before compression; contact/event growth is not bounded by this linear estimate. Smaller field arrays could help but no saving is booked.

Optional six-life paired A/B calibration only, if separately authorized: 3600 total simulated seconds maximum, three new jointly lawful 600 s body-absent field histories reusable across candidate pairs only after identity checks. Median execution 1252.22 s plus preparation 363.03 s plus roughly 85 s basic verification, about 28–30 min excluding engineering. Old worst execution rate plus mean preparation/basic verification is about 70 min. Nursery contacts may exceed that.

Proposed review reserves: **1260 active wall s / 120 MB per life**, no redistribution; **7560 active wall s / 720 MB** for six lives. **726 active preparation seconds total** and **600 passive verification/report seconds** are separate planning reserves, for a combined approximately **2.5 h**. The preparation reserve is twice the historical mean for three histories, not a measured upper bound or a bypass of the existing prehistory projected-cost check. A later packet must specify actual per-history limits and stop semantics before any preparation. Budget **1 GB working space plus 1 GB for one archive**; do not assume compression savings or repeatedly create archives.

For another later approved cohort size n, use n × 600 × measured rate plus distinct preparation, verification and archive costs. This is arithmetic, not permission to create a cohort, extend lives to 900/1800 s or enlarge the resource envelope. Full P replay/receiver diagnostics are outside this opportunity-calibration estimate. Tier-1 fidelity remains unchanged; schema changes must retain exact source stocks and field identities. Follow {here('NURSERY_0_DESIGN_v0_1.md')} for the required future apparatus update.

FS-060 remains APPARATUS_INTERRUPTED_UNCLOSED. Its interruption is not explained by these rates and is not evidence that the nursery will run reliably. Separate execution observability review is required before a future launch decision.
''')

# Static geometry SVG. The outlined block is an illustrative middle pose only.
def xy(x,y):return (70+40*x,670-40*y)
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="750" viewBox="0 0 1000 750">','<rect width="1000" height="750" fill="#f8fafc"/>','<g font-family="Arial,sans-serif" fill="#152b3c">','<text x="45" y="38" font-size="25" font-weight="bold">Nursery-0 · proposed shared geometry</text>','<text x="45" y="65" font-size="15">Static design only — no organism, chosen birth phase or simulated trajectory</text>','<rect x="70" y="110" width="560" height="560" fill="white" stroke="#152b3c" stroke-width="3"/>']
x,y=xy(2,7.5);svg.append(f'<rect x="{x}" y="{y}" width="400" height="40" fill="#fee2e2" stroke="#b91c1c" stroke-dasharray="7 5"/>')
x,y=xy(6,7.5);svg.append(f'<rect x="{x}" y="{y}" width="80" height="40" fill="#efb3b3" stroke="#991b1b"/>')
for x0,x1,y0,y1 in shared['repair_rectangles']:
    x,y=xy(x0,y1);svg.append(f'<rect x="{x}" y="{y}" width="{40*(x1-x0)}" height="{40*(y1-y0)}" fill="#6d28d9"/>')
for i,(x0,y0) in enumerate(shared['source_positions']):
    x,y=xy(x0,y0);svg.append(f'<circle cx="{x}" cy="{y}" r="20" fill="#e3ba39" stroke="#765600" stroke-width="2"/><text x="{x}" y="{y+5}" text-anchor="middle" font-size="13">{i}</text>')
for y0 in (5.75,8.25):
    x,y=xy(1,y0);x2,_=xy(13,y0);svg.append(f'<path d="M{x},{y} H{x2}" fill="none" stroke="#177e89" stroke-width="2" stroke-dasharray="4 5"/>')
for x0 in (1,13):
    x,y=xy(x0,5.75);_,y2=xy(x0,8.25);svg.append(f'<path d="M{x},{y} V{y2}" fill="none" stroke="#177e89" stroke-width="2" stroke-dasharray="4 5"/>')
for t in (0,2,4,6,8,10,12,14):
    x,y=xy(t,0);svg.append(f'<text x="{x}" y="694" font-size="13" text-anchor="middle">{t}</text>')
    x,y=xy(0,t);svg.append(f'<text x="57" y="{y+5}" font-size="13" text-anchor="end">{t}</text>')
notes=[('14 × 14 world; body diameter 1',130),('Gold disks: 12 finite sources',175),('Purple: 3 wall repair strips',210),('Red band: physical mover sweep',245),('Block: illustrative centre pose',275),('Teal: examples of available bypass',320),('These lines are never inputs to P.',349),('Swept space remains crossable',394),('when the actual mover pose allows.',422),('No body/source/mover size change.',467),('No birth is placed in this diagram.',496),('Source numbers are observer IDs.',541)]
for t,y in notes:svg.append(f'<text x="655" y="{y}" font-size="15">{t}</text>')
svg.extend(['<circle cx="681" cy="607" r="20" fill="none" stroke="#152b3c" stroke-width="2"/><text x="714" y="612" font-size="15">Body size reference only</text>','<text x="70" y="730" font-size="14">All three candidates share this layout. None is approved or executed.</text>','</g></svg>'])
write('NURSERY_0_STATIC_LAYOUT.svg','\n'.join(svg))
print(json.dumps(dict(documents_written=4,candidates=3,status='DESIGN_ONLY',world_steps=0,P_steps=0)))
