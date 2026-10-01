# NEWBORN_SPONTANEOUS_MOTOR_DESIGN_REVIEW_v0_1

**DESIGN ONLY — 2026-09-30. No replacement selected or implemented.** No world, P, field, motor-generator or controller execution; no parameter application, birth, launch authority, canon rewrite or Git write. This review follows Jason's `JASON_MOTOR_DESIGN_REQUEST.txt` and preserves the existing N0-A/N0-B/N0-C designs unchanged and provisional. Arena size, source density, birth reserve, basal cost, impact resilience and repair remain undecided.

## 1. What the evidence supports

**OBSERVED EVIDENCE.** The primary source is [NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_0_design_20260930_v0_1/NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md>): 59 complete lives, median path 13.6558, maximum excursion 0.5327, final displacement 0.2924, about 94 sustained forward/reverse switches, ~3.4 s bouts, approximately balanced forward/reverse residence and 92.96% re-entry into previously occupied quarter-unit cells. Movement direction is strongly reversed at a four-second lag while body heading remains strongly correlated. The early-life pattern already appears before late depletion. Fifty contact-free lives show essentially the same limitation.

The leading descriptive limitation is **repeated cancellation of translation along a relatively persistent heading**, with slow growth of visited space. There is substantial angular activity, but that is not evidence of continuous complete circles. This is not simply no motor activity, and contact trapping cannot explain most lives. The recorded 7/9 s harmonic templates account descriptively for ~0.93 R² of their corresponding command channels. This is neither a causal variance decomposition nor a successful-controller benchmark.

The accompanying [birth-geography audit](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_birth_motor_review_20260930_v0_1/BIRTH_GEOGRAPHY_AUDIT_v0_1.md>) finds broad population coverage: all 16 coarse geographical cells, 22/25 finer cells, and close-pair counts near the conditional uniform expectation. Individual poor exploration is therefore not explained by the whole cohort being born together. Strong birth-distance/later-proximity association remains descriptive and must not become a source-near birth rule. FS-060 is still APPARATUS_INTERRUPTED_UNCLOSED, not a complete biological life or a replacement opportunity.

**UNRESOLVED INTERPRETATION.** The spontaneous generator is a strong mechanism candidate, but the evidence does not isolate its causal share from direct feedback, evoked P output, regulation, body mechanics, initial geography and depletion. No counterfactual generator has been executed. No candidate below is known to increase meaningful exposure or improve learning.

## 2. Accepted constraints and scope of a possible future change

**JASON-ACCEPTED CONSTRAINTS.** Initial action must remain structured endogenous spontaneous activity. An innate body-forward bias or temporal persistence is admissible for consideration; knowing a useful destination is not. Preserve paired low-level actuation, ongoing bodily cost, contact, reversibility, stopping/low activity, and susceptibility to experience. Do not replace activity with white-noise commands, target/source seeking, curiosity/novelty reward, visited-space tests, distance-from-birth reward or a semantic EXPLORE action. No privileged world information enters the process.

**DESIGN PROPOSAL.** Review only the spontaneous contribution to the motor target. Existing sensory feedback, association readout, regulation, output nonlinearity, motor relaxation, attenuation, body actuation, P learning/credit, source laws and current Base World remain the comparison reference. Changing the spontaneous generator is a **mechanism change**, even when blind. It would require an explicit new mechanism/configuration identity; it must not be described as an apparatus-only optimization or executed under frozen P `6bc9683b54e4fa80136fe8534d7713e2a250a95f` without declaring the difference.

Only **two** candidate families are retained. Both address persistence/common versus differential drive directly. A separate excitable or multi-mode switching mechanism would add states, thresholds and interpretation without a distinct minimum requirement yet. Not adding a third family is deliberate scope control, not a selected replacement.

## 3. Exact current-generator diagnosis

Source: [loom_p/neural.py, Motor and Organism](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/worktrees/loom-p-b1-minimal-20260929/developmental_ecology/loom_p/neural.py:179>), [configuration.json](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/worktrees/loom-p-b1-minimal-20260929/developmental_ecology/configuration.json>), at runner checkpoint `87abae34e19d4e46234402a6b1ba776814956ec1`. Files were read, not imported or executed.

For side $i$, current spontaneous drive is

$$
o_i=0.25\sin\varphi_i+0.1\nu_i,\qquad
\dot\varphi_i=2\pi/T_i,\quad (T_L,T_R)=(7,9)\ \mathrm{s}.
$$

The two birth phases are independently indexed uniform angles. Initial $\nu_i$ lies in (−1,1), subsequently following an independent ±1 drive with relaxation 1 s; that drive refreshes every 0.5 s. The spontaneous term has a 0.35 per-side absolute envelope. This is a bound, not its RMS or final actuator magnitude. The two sinusoidal templates recur jointly after **63 s** at any initial phase, up to floating arithmetic. Noise, direct feedback, regulation, learning and mechanics prevent exact 63 s trajectory repetition. The native 0.01 s and wave 0.2 s clocks are unchanged.

The motor path is

$$
z=o+F[\mathrm{proprioception};\mathrm{contact}]+q_{\mathrm{motor},2:4}+j,
\qquad v^*=\tanh z,
$$
$$
m_{n+1}=e^{-\Delta t/0.1}m_n+(1-e^{-\Delta t/0.1})v^*,
\qquad u=(1-\alpha)\odot m_{n+1}.
$$

Here $F$ is the existing fixed anatomical 2×15 map; chemistry and vision do not directly enter that map. They may affect later activity through existing P pathways. $q_{\mathrm{motor},2:4}$ is the evoked endpoint readout, $j$ the regulator's two motor currents, and $\alpha$ its two attenuation values. This is continuous native control, **not the old human commissioning interface's 0.1 s held decisions**. The 0.1 s here is motor relaxation. Mean-plus-endpoint motor packets, association, eligibility and credit remain as implemented.

Zero-centred independent oscillatory sides can repeatedly reverse their common component without accumulating much net heading. Independent side periods create both common and differential actuation; the observed near-zero left/right correlation, high opposed-command residence and balanced forward/backward motion fit this description. Body translational and angular drag time scales are 1 s and 0.625 s respectively. A ~3.4 s translational bout can therefore develop ordinary motion and then cancel it on the next reversal; merely raising its amplitude need not repair the temporal cancellation. These are consistency arguments, not a causal ablation.

As E falls, the unchanged force scale includes $0.2+0.8E$. Later slowing can therefore reduce exposure further. Changing energy cost before motor organization would confound these contributions. No oscillator period, feedback gain, amplitude, body parameter or energy value was changed in this review.

## 4. Candidate M1: correlated common and differential drive

**State:** two real latent drives $c,d$, plus the existing motor tendency and existing indexed random-stream counters. Common drive controls the paired tendency; differential drive supplies curvature. No position, heading estimate, memory map, source representation or usefulness estimate is stored.

One concrete mathematical family is a stationary first-order coloured process at the existing 0.5 s stochastic refresh boundaries:

$$
c_{k+1}=\mu_c+a_c(c_k-\mu_c)+\sigma_c\sqrt{1-a_c^2}\,\xi_{c,k},
\qquad
d_{k+1}=a_d d_k+\sigma_d\sqrt{1-a_d^2}\,\xi_{d,k},
$$
$$
a_c=e^{-\Delta/\tau_c},\quad a_d=e^{-\Delta/\tau_d},\quad
o_L=A\tanh(c-d),\qquad o_R=A\tanh(c+d).
$$

Innovations have a fixed zero-mean unit-variance continuous distribution, independent across channels and life streams; the exact bounded distribution is not selected. Stationary-variance scaling here is part of the mathematical family, **not runtime magnitude balancing or an outcome-adaptive rule**. Initialization must use the declared stationary distribution or a separately justified fixed transient, rather than accidentally manufacturing one unusually long opening bout. Latents are held between refreshes while the unchanged native motor relaxation, direct feedback and regulation continue to act.

**Persistence:** $\tau_c$ sets common-drive memory, $\tau_d$ sets wandering-curvature memory. Review values relative to the observed 3.4 s cancellation and bodily relaxation, rather than source distances or food hits. No numerical time constant is chosen. This family has no deterministic 7/9 s phase or exact short repeating template; the refresh clock is a numerical schedule, not a prescribed repeated trajectory.

**Innate versus learned:** a modest positive $\mu_c$ is an explicit possible body-forward predisposition. Its amount, including whether it should be positive, remains a Jason decision. Noise must still allow negative common drive, near-zero activity and turning; there is no compulsory forward floor. All these temporal/statistical properties are innate. Learning remains in existing P pathways. A different stream yields different individual histories without requiring different gains or post-birth selection.

**Reorientation:** a sustained excursion of $d$ relative to $c$ produces larger curvature or opposing actuator signs. Rare larger turns can arise from the declared distribution and correlations, without a named “turn now” action or knowledge of unexplored space. No guaranteed rate of large reorientation is promised before parameters are fixed.

**How experience can shape it:** existing direct/evoked/current terms add before the final motor tanh; attenuation and tendency still act every native step. A weak persistent background can be biased or suppressed for several bodily time constants. It cannot require P to initiate locomotion. However, the latent process itself is blind and not updated by learned current in this minimal family: influence persists through the existing motor/body/P state, not by rewriting $c,d$. Injecting learned control into latent drift would be a separate design change, not an implicit feature.

**Likely failures:** too-large positive mean becomes permanent pushing; long $d$ correlation gives tight circles or wall following without intention; too-short memory recreates dithering; too-long common memory resists reversal; excessive variance saturates the tanh and hides small learned inputs; very small variance removes individual variation. Near-zero spontaneous drive need not last long enough to qualify as useful rest. Persistent movement may raise impacts and effort. None is solved by coverage reward or amplitude escalation.

## 5. Candidate M2: irregular renewal of smoothly followed motor tendencies

**State:** current common/differential drives $c,d$, target drives $C,D$, and an integer remaining interval count $n$, plus the unchanged motor tendency and random counters. This is five extra process variables, not a catalogue of semantic actions.

When the internal count expires, draw $(C,D)$ from one fixed continuous joint distribution and a new positive integer duration $N$ from a fixed nondegenerate distribution; assign $n=N$. Durations could belong to a geometric or bounded renewal family, but neither its law nor parameters is selected. Between renewals:

$$
\dot c=(C-c)/\tau_c^{\mathrm{follow}},\qquad
\dot d=(D-d)/\tau_d^{\mathrm{follow}},\qquad
o_L=A\tanh(c-d),\quad o_R=A\tanh(c+d).
$$

The countdown is in existing 0.5 s refresh intervals, with exact indexed timing. It changes the **latent spontaneous target**, not a frozen actuator command. Paired output, sensory feedback, evoked output, current, attenuation and native physics continue between renewals. Birth initialization needs an explicitly reviewed residual-duration law; a fresh-duration versus equilibrium-renewal start changes the first bout and cannot be hidden.

**Persistence:** random target-hold durations provide a more direct bout structure than M1; the following constants smooth changes. There is no fixed cycle or prescribed action order. Even if intervals use a discrete grid, irregular draws do not constitute a repeated finite motor template. A fixed interval distribution is innate, not a response to useful consequences.

**Innate versus learned:** a possibly positive mean of $C$ biases body-forward activity; $D$ should be sign-symmetric absent another accepted physical asymmetry. The continuous target distribution must include near-zero common drive, negative common drive and a tail allowing larger differential tendencies. No finite labels such as FORWARD, REST, SEEK or EXPLORE are needed. Specifying probabilities of semantic actions would be a different, less minimal construction.

**Reorientation and rest:** occasional draws with large $|D|$ relative to $|C|$ produce turning bouts; low-magnitude targets can produce quiet intervals and negative $C$ reversals. Their occurrence is entirely endogenous. The design does not sense contact in order to trigger a convenient escape or wait for energy before resting. Existing raw-sensory feedback remains free to affect actual motion through its normal path.

**How experience can shape it:** the same unswitched downstream summation allows P to bias a current bout at any native step; targets must not override, clamp or reset that influence. Relative to M1, persistence is easier to interpret as a held background tendency. It can also become harder to influence if targets are large or durations long. Existing learned influence does not extend or shorten the latent duration in this minimal family; permitting that would need a separate interface/semantics review.

**Likely failures:** long unlucky bouts pin the body against a wall; renewal transitions abruptly reverse direction despite smoothing; large differential targets form circles; a target distribution becomes a hand-authored motor repertoire in disguise; durations tuned to arena dimensions become hidden route engineering; integer boundary/restart mistakes corrupt timing. A minimum duration can prevent rapid noise but also remove ordinary responsiveness if implemented as an actuator lock. No such lock is allowed.

## 6. Loom-principle and hidden-competence comparison

| Question | Current process | M1: continuous correlation | M2: irregular renewal |
|---|---|---|---|
| Spontaneous state | Two phases, two noise values/drives | Two correlated latent drives | Two drives, two targets, one countdown |
| Innate temporal structure | Fixed 7/9 s template plus filtered noise | Correlation times and stationary distribution | Random-duration persistence plus smooth target following |
| Body-forward predisposition | Zero-centred spontaneous terms | Possible common-drive mean; explicit, unselected | Possible common-target mean; explicit, unselected |
| Different histories across individuals | Indexed birth phase/noise | Indexed latent initialization/innovations | Indexed targets/durations/initial residual |
| Reversal / low activity | Frequent through zero crossing | Remain possible through continuous variation | Remain possible through continuous target support |
| Occasional reorientation | Interference and noise | Differential-drive excursion | Larger differential target interval |
| Existing learned influence | Already measurable locally; spontaneous template prominent | Same output path, potentially more persistent room for bias | Same output path, with no locked command interval |
| White-noise commands? | No | No: temporally correlated, bounded output, motor relaxation | No: filtered persistent targets |
| Knowledge of useful places? | None | None | None |
| Guaranteed coverage? | No | No | No |
| Main imposed-structure risk | Recurrent cancellation | Forward bias or saturation dominates learning | Innate action repertoire / long uninterruptible-looking bouts |

For both candidates, a common/differential basis is a physical decomposition of paired actuators, not a world model. Fixed stochastic parameters may encode bodily persistence and an asymmetry between forward and backward, but cannot use source bearing, body position, mover phase, chemical magnitude, novelty, coverage, distance travelled, elapsed time since food or predicted survival to choose the spontaneous contribution. Countdown time in M2 is intrinsic motor history, not age-triggered curriculum scheduling. Observer metrics are never feedback inputs.

The proposed amplitude $A$ and latent variance must be declared independently of temporal structure. **Do not increase the current spontaneous envelope merely to obtain displacement.** The existing 0.35 absolute bound is a reference ceiling, not a selected new amplitude. Equal envelopes do not guarantee equal RMS commands, effort or impact energy. The eventual component review should state analytical magnitude/variance consequences before physical cases; no per-run normalization, outcome-based adjustment or magnitude balancing is proposed. Neither excellent random coverage nor a larger excursion is alone a Loom acceptance result.

## 7. Interaction with P and regulation: activity that remains shapeable

Keep the current motor interface in Section 3 for both families. Current, evoked readout and direct feedback enter **after** the blind spontaneous calculation and before the existing output tanh. Existing regulation can increase or decrease paired current and attenuation; it does not need a semantic permission signal from the generator. Group opening and learning/association can continue influencing the existing P representation paths. The two reserve banks and their actual eligibility/credit remain unchanged.

For a fixed instantaneous pre-tanh input $z$, the local gain to an additive input is $\operatorname{sech}^2 z$. Over a steady interval the gain to command also includes $(1-\alpha)$; at one step, the motor relaxation contributes $(1-e^{-\Delta t/0.1})$. Thus saturation, near-total attenuation or a huge persistent background can make formally present input paths practically weak. Conversely, a low-amplitude background is not useful if it leaves the body nearly inert. The problem is not solved by declaring that the input wires still exist.

At the current spontaneous envelope alone, tanh is not necessarily saturated; high command-template R² therefore does not prove a saturation defect. Small actual learned/evoked contributions, relative scale, their time structure and body dynamics remain possible reasons for weak influence. Regulator current can in principle reach ±0.5 per actuator under the configured two-bank formula, but attainable bounds are not evidence that newborn learned current reaches them. The existing integrity audit already demonstrates some measurable learned-I motor effects and must not be rewritten as “learning has no influence.”

**Proposed component checks before any world case:** on manufactured fixed sensory/current/attenuation inputs, verify a sustained positive/negative current changes the paired target/command in the expected direction, asymmetric current can bias turn tendency, attenuation remains effective, and no branch freezes the existing pathway until a bout ends. Examine gain over the declared latent envelope, plus realistic input scales taken from preserved diagnostics; do not introduce new gains to force a desired ratio. Separate finite arithmetic response from materially meaningful bodily change. A review threshold for “materially shapeable” still needs an explicit bodily/relative-scale rationale; it is not invented as a pass percentage here.

Verify draw isolation, complete process-state reset, exact restart state, native/wave schedule and no privileged inputs with manufactured inputs. M2 especially requires renewal-boundary pause/resume checks. These are **proposals only**; no candidate step, P step or new motor time series was produced in this task.

Do not inject regulation into new hidden latent gates, automatically amplify learned terms, weaken the existing spontaneous component when a learned norm grows, or bypass tanh/attenuation. Those would be additional mechanism hypotheses. No candidate is selected until both its exposure properties and its room for existing learned influence can be assessed.

## 8. Minimal commissioning comparison — proposed, not authorized

The narrow matrix is **three current-world starts × three processes (current, M1, M2) × 90 s maximum age = nine short cases, 810 simulated seconds at most**. It is not Founder Search, an efficacy experiment or a nursery cohort. No authority, runnable candidate configuration or birth preparation is included here.

Use the first three original roster births, **FS-001, FS-002 and FS-003**, as a fixed ordinal rule independent of their outcomes—not selected for contact, source direction, chemistry, safety beyond the existing rule, or candidate performance. Their geography and existing outcomes are already public in this research record; these are matched, disclosed commissioning fixtures, not held-out evaluation starts. This is a proposed future reuse of initial snapshots as separate identified commissioning clones, never continuation, replacement or retry of those Founder lives. The complete physical state, exact phase/field prehistory, original non-motor blank P state, anatomy and unrelated indexed streams remain matched within each triplet. Only declared spontaneous-process state/schema/initialization differs for M1/M2; do **not** claim whole-engine byte equality across mechanisms.

| Ordinal start | Current generator | M1 family | M2 family |
|---|---:|---:|---:|
| Original FS-001 birth | 90 s | 90 s | 90 s |
| Original FS-002 birth | 90 s | 90 s | 90 s |
| Original FS-003 birth | 90 s | 90 s | 90 s |

Three starts provide minimal replication of gross regime differences without presenting a single stream as representative. Ninety seconds covers one full current 63 s joint template plus additional observation and many present ~3.4 s bouts, while remaining far shorter than the ~430 s complete lives. This is a proposal for a gross physical-exposure screen, not enough to characterize rare tails or prove learning. If a later chosen family contains time scales too long to characterize within 90 s, **return to design review**; do not silently extend the horizon or tune it after a miss.

Keep normal P learning active, with no newly invented learning freeze or privileged controller. Its presence means this is an intact newborn coupling screen, not a pure motor-only causal isolation. Selection must not use learned success or learned-state magnitude. No P learning score is computed during execution. Stored current 90 s prefixes may be used only as passive reference checks; a matched baseline launch, if later authorized, must have a separately named commissioning identity and cannot overwrite Founder evidence. No new prehistory is needed if exact configuration/phase dependency and saved initial-field custody are verified; incompatible reuse stops preparation rather than generating more history automatically.

Candidate constants, distributions and initialization must be fixed **once before any physical case**, justified from body time scales and the declared mathematical process, not fitted by trying phases, starts or food outcomes. The new motor stream labels must leave all unrelated indexed draws unchanged. Order by start, then current/M1/M2; no outcome-dependent reordering. No trial-and-retry parameter loop, alternate seeds, replacement starts, added case or continuation. Complete the declared small matrix unless a predeclared shared apparatus/resource defect stops it; keep all starts, misses, damage and cutoffs in the denominator. Genuine nonviability ends a case; survival is not a score.

### Measures, interpretation and failure criteria

Use the already disclosed exploration definitions at native resolution: path, excursion, birth/lag MSD, coverage growth at 0.25 and 1 units with grid-offset sensitivity, direction versus heading correlation, forward/reverse residence/switches/bouts, common/differential command RMS, curvature, low-activity fraction and repeated-space entry. Report paired per-start differences and all time courses. Directional first crossing of an oscillatory correlation is not automatically a decay time. Measure effort expenditure, E/I, contact count/duration, impulse, damage and wall/mover exposure separately. Report expenditure and displacement together rather than hiding increased power behind “better exploration.”

Source contact or transfer may appear in the physical ledger as an opportunity consequence. Do not rank candidates by food hits, impose a source-contact minimum, maximize energy return or infer useful learning. Source location is an observer field only. No survival score, founder score, trained-controller comparison or downstream selection is part of this screen.

| Disposition | Predeclared meaning |
|---|---|
| Apparatus invalidity | Forbidden input; nonfinite state; schedule/state-reset/restart mismatch; broken evidence/custody; undeclared draw or parameter difference. Stop and report; do not patch during the comparison |
| No gross temporal improvement observed | Repeated cancellation/locality remains in all paired records despite activity. Preserve as a kinematic miss; not P failure |
| Mere magnitude escalation | Any increased reach accompanies materially larger drive/effort without a clear change in persistence/recurrence. Do not credit temporal design without separating this confound; no automatic rescaling |
| Inflexible background | Manufactured tests show a blocked regulation path, or declared expected input scales produce negligible modulation throughout most of the envelope. Return to design review; no automatic learned-signal amplification |
| Hazard-dominated exposure | More distance comes with sustained pinning, repeated hard impacts or large damage. Report the tradeoff; do not rescue with resilience/geometry tuning inside the batch |
| Inconclusive | Mixed starts, too few renewals, administrative censoring or scale-sensitive metrics. Do not force a winner or extend the screen automatically |

These are structured review outcomes, not newly invented numerical efficacy gates. Before a future launch, exact numeric component tolerances and any categorical physical thresholds must be frozen for apparatus correctness and gross-regime interpretation. The design intentionally does not invent an optimal percentage of coverage or food contacts. Jason reviews all outcomes; no selection function or winner is implemented.

### Bounded resource proposal

Current lean evidence receipts give median active wall/simulated second 0.34784 and observed range 0.31794–1.04965. At unchanged rates, nine 90 s cases project about **282 s (~4.7 min) active wall time**, range ~258–850 s (~4.3–14.2 min), and ~61 MB primary evidence at the historical median (~59–77 MB range). Ninety-second records have relatively larger fixed checkpoint overhead; new process-state fields and richer contact can add cost. These are rough planning projections, not measured candidate throughput or executable allowances. A simple future planning reserve is at most 300 active wall seconds and 25 MB per case plus explicit validation overhead, to be reviewed and bound later; it is not permission to run or renew a resource limit.

Retain Tier-1 native physical/raw/command/RNG records, actual wave records, full new process state in checkpoints and all contact/energy/integrity events. No live deep diagnostic pass, plotting or outcome-driven inspection. Existing observer kinematic metrics may be derived after the whole declared matrix stops. If extra generator diagnostics are required, define their schema/resource cost before launch; do not silently turn on live D5. All resource estimates remain uncertain because better travel can change contact cost.

## 9. Consequences for Nursery-0 and birth sampling

Preserve [N0-A/N0-B/N0-C](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_0_design_20260930_v0_1/NURSERY_CANDIDATE_PROPOSALS.json>) exactly. The existing 14-unit/twelve-source ecology is not locked. This follow-up also defers the proposed basal/damage changes: a new process may alter exposure, effort, impact speed and repair access, so the old runway proxy cannot establish the appropriate amount of tuning. No new larger-world number or alternative resilience value is selected.

If blind activity exposes more space at comparable ordinary motion cost and remains shapeable, a larger arena/lower density may deserve review, potentially preserving richer route choice and reducing wall or chemical crowding. It could instead increase impact speed enough to offset fewer wall encounters. Improved exploration alone does not establish adequate source opportunity, sufficient net intake, recoverable integrity deficits or repair holds. These remain separate ecology and body questions after motor characterization.

The birth audit's possible stratified-random law addresses population coverage only. It is not incorporated into the motor comparison and does not replace the original matched starts. Do not change motor, birth law, geometry and viability together; their effects would be hard to interpret and the exercise would become a larger programme.

## 10. Exact unresolved decisions for Jason

1. Whether either or both M1/M2 families warrant a concrete parameterized design. **Neither is selected here.** Retaining the current generator remains a valid review disposition.
2. Whether to permit a body-forward statistical bias, and how much spontaneous dominance is acceptable while leaving ordinary reversal, rest and learned influence. This is an innate physical prior, not source knowledge, but it must be explicit.
3. The distribution, correlation/duration constants, amplitude envelope, stationary/birth initialization and stream labels for any retained family. No numerical replacement values have been chosen or applied.
4. Whether influence through the existing additive/attenuation path is sufficient. Direct learned modification of latent persistence or duration is **outside these minimal families** and would require another explicit mechanism decision.
5. Whether the proposed three-start, three-process, 90 s matrix is the appropriate small commissioning scope. Review exact component criteria, physical interpretation rules, snapshot reuse and resource limits before any implementation or authority.
6. What new mechanism and apparatus identities are needed to record candidate process state and distinguish it from frozen P. Required implementation/component checks would be a later task; no old authority is reusable.
7. After motor evidence, whether to reconsider nursery geometry, birth stratification and the amount of energy/integrity/repair adjustment. None is decided from the present associations.

**Status separation:** measured trajectories and code are evidence; Jason's blind-endogenous/activity constraints are accepted; M1/M2 and the commissioning matrix are proposals; causal shares, useful influence and nursery benefit are unresolved. The correct present endpoint is review, not a chosen mechanism or launch.

**Zero simulation or P execution. No candidate motor series generated, no parameter applied, no new birth/prehistory/authority, no preserved record or code changed. Stop for Jason review.**
