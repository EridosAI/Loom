# P coupling commissioning design v0.1 — review draft

**Date:** 2026-09-23  
**Contribution:** `2026-09-23-p-commissioning-design-2fb3ff84`  
**Author:** Codex; assistant proposal for Jason's review  
**Implementation:** `6bc9683b54e4fa80136fe8534d7713e2a250a95f`  
**Authority:** design only, under the [exact request](REFERENCES/COMMISSIONING_DESIGN_REQUEST.txt). No procedure described below has been executed in this contribution.

## 1. Status, purpose and decisions

The current P engineering baseline is **FIT TO PROCEED TO COUPLING COMMISSIONING**. Mechanism fidelity is **INDEPENDENTLY VERIFIED within reviewed scope**. Its scientific status remains **UNCOMMISSIONED / UNTESTED**. R1 is closed for the demonstrated radial/oblique release–recontact class; R2 and R3 are closed. This design neither repeats the independent review nor extends its verification claim.

The preceding `d5f7efbe67193f215e52d95ca912db131a79f31c` and `f7eb6f27c661e3db193a4225b56a825d7e41739d` checkpoints retain their historical **ENGINEERING HOLD** findings. They are preserved engineering-history branches, not failed versions of P's scientific hypothesis. The [final independent review](REFERENCES/LOOM_P_FINAL_INDEPENDENT_R1P_FIDELITY_REVIEW.md) remains the source of the present engineering disposition.

Retained limitations are: finite-step contact realization is not an exhaustive convergence proof; sensory capacity is provisional; mean-plus-endpoint packets are lossy; receptor and packet adaptation may suppress sustained information; association is deliberately contracting; effective learned signal magnitudes remain unknown; equal-valued E/I bank settings share configuration fields. No scientific efficacy, developmental success, survival capability or ecological adequacy has been established.

The proposed question is: **Does this exact body, world, sensory interface and newborn provide a physically possible, perceptually accessible and inspectable opportunity for development, without choosing its settings to obtain useful learning?** Four distinct layers answer parts of that question:

| Layer | Necessary evidence | Claim withheld |
|---|---|---|
| Physical validity | Lawful embodied witnesses and accounting, including recovery and continued access to energy | P can discover or exploit the witness |
| Perceptual ceiling | Useful distinctions are available through permitted sensory histories, where the world represents them | P's cortex or packet preserves them, or P learns a good response |
| Newborn bootstrap | Unconditional records of first consequential experience and remaining opportunity under the fixed birth process | A success rate, developmental benefit or indefinite maintenance |
| Mechanism observability | Native evidence of inputs, pressures, updates and receiver influence | Those changes are useful, semantic or adaptive |

The [matrix](P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md) defines all proposed measures and their classifications. The [change register](P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md) covers every configuration key and additional law-bearing constants. [Decisions required before execution](DECISIONS_REQUIRED_BEFORE_EXECUTION.md) are proposals awaiting Jason; D1–D3 are already accepted and are not reopened.

## 2. Exact instrument and source boundary

Use the complete runtime and configuration delivered inside the final review's nested builder archive, not the initial specification alone. The [source guide](SOURCE_GUIDE.md) distinguishes committed foundation, P parent, proposed specification, engineering implementation and review. Source identities are in [READING_COPY_IDENTITIES.json](READING_COPY_IDENTITIES.json) and [SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json).

| Surface | Current implementation to preserve |
|---|---|
| Time | Native 0.01 s; wave 0.2 s; four simultaneous associative sweeps per wave |
| Raw sensory channels | Light 10, chemistry 4, contact 8, proprioception 7: **29 raw coordinates**, plus separately actual E/I at the regulator's wave handoff |
| Learned cortex | Four eight-unit cortices; two four-row groups in each |
| Packet | Mean followed by endpoint; 82 packet coordinates, 164 context coordinates; 224 maps, 88,608 map coefficients |
| Persistent state | Sensory weights and references; associative maps/use; separate E/I regulatory banks and references; complete transient/filter/trace/random state |
| Body/world | Radius 0.5, arena side 20; eight finite sources of capacity 0.2; three wall repair strips; one moving 2-by-1 block |
| Initialization | Master seed 5284097, fixed anatomy; life-specific birth and dynamic streams; energy 0.7, integrity 1; lawful field/mover prehistory, no learned inheritance |

Sources: [configuration](REFERENCES/developmental_ecology/configuration.json), [schema](REFERENCES/developmental_ecology/loom_p/schema.py), [neural operations](REFERENCES/developmental_ecology/loom_p/neural.py), [implemented data flow](REFERENCES/docs/developmental_ecology/p_engineering_20260921/IMPLEMENTED_P_DATA_FLOW.md).

The existing `Engine.run_bounded` rejects a duration or cumulative age above 30 s. The proposed longer observations therefore need a **separately authorized, reviewed commissioning harness**, using unmodified law-bearing modules and a new bounded runner. Repeated short calls are not an authorized workaround. The harness, controller and observer adapters do not yet exist as verified commissioning apparatus. This is a real engineering dependency, not a reason to change P or to pretend that a 30-second engineering smoke establishes ecology.

A future harness must establish byte identity, input separation, native/wave ordering, lawful phase-specific prehistory, exact stop reasons and observer non-interference before longer observations. Separate external physical controllers operate the same physical/chemical/transduction laws; their actions are not P's commands. Their recordings must say `external_controller`, never `intact_P`. Do not replace the organism object and then label the resulting life as P. Any replayed sensory cortex is a detached probe; its hypothetical motor output cannot be recorded as actually delivered action.

## 3. Measurements and inference discipline

Every measure belongs to exactly one primary class:

* **APPARATUS VALIDITY (AV):** an identity, law, accounting, information-isolation or physical/sensory possibility needed for the instrument to pose its question.
* **CONFIGURATION OBSERVABILITY (CO):** opportunity, representation, numerical influence or sampling coverage under the selected configuration, without requiring useful development.
* **SCIENTIFIC OUTCOME (SO):** useful relationships, useful differentiation, beneficial credit, survival strategy or participation/retention benefit. These are excluded from commissioning acceptance and tuning.

A CO warning can motivate a documented question; it is not automatic apparatus failure. A failed controller trial can be inadequate control, insufficient coverage, numerical failure, or physical impossibility. Only an identified defect with its discriminating evidence supports an adjustment. Positive energy gain, positive restoration and nonterminal damage have meanings in the laws; arbitrary percentages of successful lives do not.

For positive/zero numerical claims, retain operands, solver residuals and accumulated accounting residual. Require the sign to be resolved beyond the propagated numerical uncertainty of the calculation. Use the existing arithmetic and solver tolerances for their specified purpose; do not turn `1e-12` into a biological effect threshold, or call every tiny nonzero number useful. Report unresolved signs as unresolved. No new developmental pass threshold, success percentile, utility score or equal-RMS target is proposed.

Finite counts are descriptive. Publish all planned starts, attempted starts, apparatus failures, deaths, administrative cutoffs and pauses. Death is a competing event for first encounters, not ordinary right-censoring. An administrative cutoff right-censors an otherwise observable life. An apparatus failure is separately unresolved, never reclassified as death or silently replaced. For this small pilot use event timelines and exact fractions with denominators; do not estimate unsupported quantiles or fit a population survival model.

### 3.1 Event definitions and checks that can actually fail

Propose these observation conventions for review before execution. A source or repair contact is an actual certified body–fixture contact in the solver/event history, not merely a nearby centre. Transfer/restoration is a positive actual ledger increment with resolved numerical sign. Net-positive energy is an increase over a complete 0.2 s physical interval that includes source contact, with all costs retained; the underlying native ledger remains available. Report partial terminal intervals separately, never pad them to a full wave. Damage is actual integrity loss attributed to the impact/stress ledger, not simply I changing in a plot.

Retain all raw contact starts/stops, separation durations and maximum clearances. For a summarized **substantive revisit**, propose leaving the fixture by at least one body diameter of surface clearance and then recontacting it; distinguish same-source and other-source returns. This observer convention prevents contact jitter becoming a revisit count. It is not a clearance requirement for physical validity or a behavioral pass gate; Jason may choose a different explicit definition before execution. Report the continuous clearance data so that the convention stays inspectable. For mover exposure, use confirmed light-ray interception of the mover or actual mover contact, with evaluator-only identity; record other possible chemical/motion exposure as uncertain unless causally established. Proximity alone is not verified perception.

A missing event has no fabricated event time; a non-finite measurement is invalid, not zero. Denominator-zero secondary rates are undefined and accompanied by exposure counts. A first-contact observation at terminal time is retained with exact event order and cannot imply continuing runway. Show time alive and subsequent actual encounters after first transfer/repair rather than a binary developmental-success label.

Every prospective AV check must have a supported input domain and a reachable negative fixture. Propose checks on **detached fixture records/copies** with a deliberately mismatched hash, missing native sample, incorrect source debit/body credit, wrong field phase, forbidden controller input and mislabelled stop reason; each validator must reject the intended defect. Matched correct fixtures must be accepted. For physical witnesses, include known non-contact/zero-uptake, I=1/zero-repair and excessive-force/ineligible-repair conditions so a vacuous “positive” detector cannot pass. These are proposed component validations, not changes to the live baseline or instructions to launch them now. The observed-red requirement follows Base World §8.2; it does not import historical experimental gates.

## 4. Physical ceiling: actual embodied possibility

### 4.1 Controller and records

Propose a small external waypoint/contact controller, or a privileged human operator for the initial witnesses, commanding only the existing bounded left/right actuators. It may read body position/orientation/velocity, actual E/I, delivered commands, exact fixture geometry, mover phase/velocity, source stocks, contact normal/force/impulse and the world clock. That list is closed: no teleport, direct energy/integrity setting during a trajectory, altered collisions, replenishment or hidden actuator. Manufactured initial states are allowed only in explicitly labelled component witnesses and are not newborns.

The simplest first implementation is an operator with a privileged world/contact display and bounded command entry. Commands are held for 0.1 s unless a native terminal event stops the interval. World time pauses between entries; operator delay is not extra bodily time. The actual mechanics still run at 0.01 s. This controller is intended to find embodied witnesses, not optimize an innate policy. Its transcript, command holds and information display are part of the apparatus manifest. Failed manual control alone proves no impossibility.

For every physical witness retain native body pose/velocity/E/I, actuator commands and realized force, expenditure, source debit/body credit, stocks/renewal, impulses and positive-duration forces, contact eligibility, repair increments, terminal status, mover and chemical state identities. Distances and object labels in these **observer** records never feed the organism. A map showing body-centre configuration space uses the actual radius and collision boundaries, not a point-agent path.

### 4.2 Proposed bounded checks

All counts and horizons below are workload proposals, not established sufficiency. Start definitions, paths and phase choices must be fixed in the execution manifest before observing P. Use deterministic geometry-based fixtures plus the declared birth distribution; do not select starts because P did well there.

| Check | Exact privileged information used | Horizon and trajectory intervention | What a lawful witness proves / does not prove | If it fails |
|---|---|---|---|---|
| A0: body accessibility | Radius, wall/source/repair/mover geometry and motion law; no neural state | Static configuration-space calculation, no world evolution. Include mover phase snapshots and an always-clear bypass; do not exclude its whole swept area permanently | Geometric clearance for body centres / not dynamic, reserve or perceptual feasibility | Contradictory clearance can establish a geometric defect; an incomplete path search cannot |
| A1: source approach and productive hold | Pose/velocity, geometry, E/I, source stock, contact forces, clock, mover phase | Two 120 s externally driven trajectories; approach from an open region and a wall-adjacent region, then hold contact | Reachable contact; separately actual transfer and a positive **net** energy interval / not newborn discovery, source recognition or sustained lifetime | Check controller error, collision access, actuator capability, eligibility, ledger and excessive cost separately |
| A2: depletion, leave, later opportunity | A1 information plus all stocks/renewal and destination geometry | Two 400 s trajectories. Up to 180 s source residence, then up to 220 s travel and contact elsewhere; all state continues | Actual stock drawdown, declining local opportunity, expenditure during travel and another productive source / not exact zero stock, indefinite sufficiency or learned switching | Saturated E can prevent depletion; renewal prevents an exact-zero target. Distinguish poor loading/control from wrong stock accounting or reserve-infeasible route |
| A3: damage → repair → energy | Pose/velocity, E/I, geometry, impulse/force, repair eligibility, stocks, clock/mover | Two 240 s trajectories. One starts healthy and receives controlled actual nonterminal damage; one manufactured state starts at E=0.5, I=0.5 and is labelled non-newborn. Reserve up to 90 s for repair, then leave for energy | A damaged body reaches repair, sustains eligible force, has actual positive I restoration, and reaches productive energy again before nonviability / not recovery from every damage/reserve level or full restoration to I=1 | Separate terminal injury, insufficient actuator capability, inaccessible strip, force overshoot, too-long repair, cost and accounting defects. A failed route requires further diagnosis, not automatic reserve inflation |
| A4: mover crossing/wait/detour | Body state, complete mover geometry/phase/velocity, static geometry, E/I and clock | Three 120 s trajectories, one per strategy; real actuator commands alter body/world history | At least specified time-dependent crossing, waiting and bypass opportunities for the finite body / not sensor prediction or safety for every phase and reserve | Distinguish controller timing, swept-geometry error, collision impulse, unavailable bypass and reserve cost |
| A5: repeated renewal-supported circuit | A1/A2 data plus all renewal/source ledgers | One 1,200 s external-control trajectory; revisit sources and include repair only when physically required; no resets | Bounded evidence of replenishment, revisitation and energy balance under actual travel and stock histories / never indefinite viability | If stocks merely drain, report transient support. Failure may be controller limitation; analytically inadequate accessible replenishment is a different defect |

Total physical horizon ceiling: **3,080 simulated seconds** across ten controlled trajectories; no such trajectory is authorized now. A3's healthy-start damage command stops when a nonterminal injury is recorded, with I=0.8 as a proposed operator stopping target, not a required measured value or a post-impact reset. If an impact overshoots or kills the body, preserve that outcome. Its manufacture at I=0.5 is a separate initial-condition probe, never substituted for the actual-damage trajectory.

### 4.3 Law-based checks that prevent misleading success

In the implemented law, expenditure is $0.0015+0.001(|u_L|+|u_R|)/2$ per second. Without intake, birth E=0.7 permits at most about 466.7 s under basal expenditure, or 280 s at maximum effort throughout. Damage and terminal events can shorten that interval. These are arithmetic bounds, not measured lifetimes.

A source's maximum renewal is $0.2/400=0.0005$ per second, below basal expenditure. Thus a body plus one finite source cannot maintain total energy indefinitely: even perfect transfer cannot overcome the combined stock/reserve deficit. Eight sources have aggregate maximum renewal 0.004 per second, but that inequality alone does **not** establish global sufficiency: actual deficits, travel, contact and repair govern realizable supply. A5 examines those costs and stock drift; it cannot turn finite observations into an indefinite claim.

Repair eligibility uses force below 0.25 and a speed penalty. For zero slip and force 0.1, the configured eligibility factor is $0.1/(0.1+0.1)\,(1-0.1/0.25)=0.3$. This is a proposed contact target because it lies inside the eligible range; it is not a changed actuator law. For a fixed eligibility $Q_R$, restoration approaches I=1 asymptotically, with rate 0.02: demanding exactly I=1 within a finite horizon would be an invalid gate. Inspect native positive restoration and net integrity separately from simultaneous damage. Show actual energy and capability at departure and arrival; do not invent a minimum departure-reserve percentile.

Sources: [physics accounting and step](REFERENCES/developmental_ecology/loom_p/physics.py), [geometry and transduction](REFERENCES/developmental_ecology/loom_p/geometry.py), [Base World §§5–8, 10–13](REFERENCES/review_inputs/pinned_git_blobs/docs/developmental_ecology/BASE_WORLD_COMPLETION_v0_1.md).

## 5. Perceptual ceiling: information actually available

### 5.1 A deliberately external, capable reference

Recommend a **sensor-only human reference controller** as the first small apparatus, avoiding a second learned organism or a policy-training project. It receives labelled receptor coordinates, their native history and its own past commands: ten light, four chemistry, eight contact and seven proprioceptive coordinates at 100 Hz. Actual E/I are released only at the same 5 Hz handoff as P's bodily regulator, held between handoffs. It may inspect past history and use memory; this is an information ceiling, not P's architecture. It commands the same two actuators through the 0.1 s hold interface described above.

The display has no world image, position, object IDs, source stocks, analytic gradients, material names, privileged event notifications or future values. Sensor coordinate/anatomy labels are allowed; inferred relationships must come from observed histories. Pause the world while the operator studies the trace; native traces are neither resampled nor turned into privileged summaries. Privileged evaluation is performed afterward in a separate view. Record screen fields, commands and annotations. Operator familiarity can be established on disclosed manufactured fixtures, never by secretly showing the test trajectory's world view.

Keep test initial states and phases hidden from this operator. A person who has already inspected a privileged trajectory cannot supply a blinded sensory-only witness by replaying its answers. Use undisclosed held-out starts and separate privileged evaluation; record any accidental disclosure as an apparatus limitation. General knowledge of the declared sensor/body laws is allowed, but the current trial's hidden state is not.

Before interpreting a failure, require recorded positive controls showing the operator can read left/right sensory differences, command/achieved-motion differences, contact onset and a gentle hold using this interface. A successful held-out physical interaction witnesses accessible information. A failure remains inconclusive unless an independent observability argument identifies absence. An automated raw-history controller is the strongest repeatable alternative; it needs its own reviewed architecture, training separation and cost estimate, not an unspecified “smart controller.” Jason's choice is outstanding.

### 5.2 Comparisons and source-state limits

Propose three paired 180 s scenario families (six trajectories; **1,080 simulated seconds**): source approach/contact/state change, repair/body-wall interaction, and mover/self-motion. A pair restores the same complete initial physical state and then compares full raw input with one predeclared deprivation. Restore only **between** separate trials; there is no mid-life rescue. Deprivations are display-side only and logged; other channels retain their real values. Choose chemistry hidden for the source pair, contact sectors hidden for repair, and temporal ordering hidden in the mover display while leaving current values visible. This last control tests the external reference's use of history, not a change to P's packet. The controllers' choices will change future trajectories; do not pretend these are matched sensory streams after action divergence.

Use the already recorded full histories additionally for paired offline inspection with specific light, chemistry, contact or proprioceptive coordinates hidden and with full versus ordered-history views. Such offline comparisons do not evolve the world. They can show dependence or ambiguity, not closed-loop performance. No full factorial deprivation battery is proposed.

| Target | Actual observable channel and discriminating record | Forbidden inference |
|---|---|---|
| Source approach/contact | Retinotopic light, two-site chemistry, contact and delivered/achieved movement; observer aligns opportunity and arrival | Object identity or reliable navigation is not supplied |
| Source state change | Emission magnitude depends on stock, but chemistry also depends on transport, history, position and occlusion. Compare held position and matched motion histories with observed stock only in evaluator records | Appearance is stock-independent; a depleted source still emits. Instantaneous stock or an unambiguous “empty” flag is not available |
| Restorative interaction | Light/chemical differences where present; contact and proprioception for gentle hold; actual I trend after real repair | No repair-material label, integrity gain prediction or unique classification of every material is required |
| Mover approach/motion | Light-sector changes, chemistry disturbed by solids, contact and self-motion/proprioceptive histories | Walls and mover share material; movement must not be inferred from a privileged velocity field |
| Body-wall relation | Contact sectors, achieved forward/lateral/angular motion and discrepancy with command | No wall distance or pose is given directly |
| Command–achieved discrepancy | Seven proprioceptive coordinates include delivered commands, motion and fixed discrepancy transforms | A body-centred signal does not imply global localization |
| E and I | Real bodily values at the wave handoff and their separate trend records | Evoked bodily packet coordinates are not actual reserve, repair or gain |

### 5.3 Locate loss before proposing a repair

At the same native times align raw input $s$, receptor mean $\mu$, residual $s-\mu$, cortical trajectory $x$, its wave mean/endpoint $b$, packet mean, centred packet $\beta$, trace, query and returned $q$. The implementation distinguishes step-start raw used by neural operations from end-of-step raw reported after physical advance. Compare like timestamps; do not misdiagnose that offset as sensory loss.

Classify an observed problem as one of four things: **absent raw information** (identical permitted histories under a specific physically different condition); **weak raw information** (present but small, ill-conditioned or practically ambiguous); **cortical loss** (raw distinction present, no corresponding residual/activity distinction under the examined state); **packet loss** (native cortical histories differ but mean/endpoint or subsequent centring makes the distinction unavailable). The latter two are CO findings about P, not permission to revise its mechanism during commissioning. Different endings or similar plots do not prove exact equality. Report pairwise norms, time alignment and error precision; label approximate aliases as approximate and keep their full traces.

Use controlled contrasts, not an outcome-trained decoder, to make an absence claim. No finite decoder failure proves information-theoretic absence. A successful raw-only controller does not discharge cortical or packet accessibility. A raw distinction lost by the chosen mechanism may ultimately define the scope of a scientific test or motivate a separately authorized mechanism branch; it is not silently fixed here.

## 6. Bootstrap floor and the innate-maintenance risk

Propose four outcome-independent birth stream IDs, **1, 2, 3 and 4**, under the unchanged master seed and birth law. Prepare the correct field/mover prehistory for each; do not reuse life 0's cache with another phase. Each intact P observation has a 600 s ceiling or earlier actual nonviability/apparatus termination. This exceeds the no-intake birth-energy bound, covers twenty mover periods, ten packet-adaptation time constants and two opening time constants. It does not cover slow references (5,000–10,000 s), establish population rates or prove indefinite behavior.

Intact P starts learning immediately. Therefore its later behavior cannot honestly be called a test of innate maintenance alone. Recommend a separately labelled, Jason-approved **fixed-structure diagnostic** paired to each birth: retain newborn sensory weights/references, associative maps/use and E/I bank weights/references at their exact initial values; let bodily dynamics, sensory activities, centring, fast traces, eligibility, exploratory process and other transient state evolve under their existing laws. Initial maps and banks remain zero. Held controls must be computed from the frozen bank state; resetting weights after producing controls would be too late. The diagnostic adapter needs independent review of its update timing and state list. It is an intentional external intervention, never intact P or a revision of P. If Jason does not authorize it, omit these four controls and restrict innate claims to genuinely pre-learning observations; do not quietly infer innate sufficiency from intact P.

No code for this adapter is provided or authorized now. Pairing gives a shared starting state and stream definition, not identical experiences after action divergence. Differences are not a developmental-efficacy result. The control is included to expose a potentially trivial innate solution, not to select a better learner.

The proposed exact frozen fields are each cortex's `shared`, `fine`, `shared_ref`, `fine_ref`; association `H` and `use`; regulator `theta` and `reference`. Keep cortex `mean`, `x`, `C`, `opening` and integrals, association means/traces/activity, body mean, eligibility, random counters and motor state live. Their ordinary dynamics do not introduce a replacement policy. If the adapter calls the existing update functions, restore frozen sensory fields before the next native read, map/use fields before the next associative read, and bank fields **between `credit` and `output`**. Diagnostics must distinguish the discarded hypothetical update from the applied zero structural increment. No discarded update may affect later controls, state or RNG. Verify this contract on component fixtures before interpreting the diagnostic as fixed structure.

For every assigned start record first geometric source encounter; first transfer; first net-positive source interval; first contact stress/actual damage; first repair-surface contact; first eligible contact while I<1; first positive actual restoration; first mover-associated sensory/contact event (privileged annotation only); and time, E/I and continuing encounters after each useful bodily interaction. A contact event with no gain and repair contact at I=1 remain distinct. Use exact encounter geometries, actual debits/credits and state ledgers, not guessed behavioral labels.

All event opportunity timelines are **CO**. Publish each life, including no encounters, deaths and cutoffs, over all four assigned births for each arm. Mark the unstarted/apparatus-failed subset explicitly; do not compute useful-contact rates only among survivors or only among damaged animals. Also show damaged-time and contact-time exposures as secondary denominators, alongside unconditional counts. A life that dies before damage remains in the unconditional useful-repair denominator. Four lives can reveal a gross issue; four negative lives do not establish that a possible event never occurs.

For the opposite risk, inspect fixed-structure trajectories for repeated source cycling, repair, reserve/stock drift and activity beyond initial fuel use. Single-source indefinite maintenance is excluded by the energy bound in §4.3. Finite successful circuits can suggest an overly easy innate regime but cannot establish indefinite maintenance. A formal invariant/cycle argument, or a separately authorized longer fixed-process assessment, would be needed for that stronger claim. Do not make the world harder merely because an innate trajectory lasts 600 s. Useful learning, better survival, more appropriate distinctions or beneficial participation are **SO**, outside this pilot's gates.

## 7. Mechanism and coupling observability

Use the intact P bootstrap records for passive measurements below. Reuse physical/sensory histories only in explicitly detached probes; they do not show what intact P encountered. All measurements here are **CO** unless a record fails identity, ordering or accounting (AV). None requires usefulness.

### 7.1 Capacity and differentiation

Retain all 29 raw coordinates and all 32 cortical coordinates. For each cortex show receptor residual ranges, saturation, activity covariance/singular spectrum, weight-row norms, within-group similarity, and the difference between shared and fine components. Record spectra as continuous diagnostics, with numerical-rank uncertainty; no invented rank-success cutoff. The ten-to-eight light reduction is a dimension limit, not by itself proof that necessary task information is lost. A four-to-eight chemistry expansion cannot create raw information that is absent.

Effective non-use requires distinguishing absent encounters, receptor cancellation, near-zero drive, saturation, a disconnected path and an actual low-dimensional environment. Tied weights may still yield different activities through fixed recurrence; activity diversity is not proof of learned differentiation. Evidence supporting a capacity-starvation proposal must locate a required physical distinction in raw histories, establish its loss under the current representation on independent controlled cases, rule out missing encounters, adaptation, packet compression and numerical faults, and supply a representational or controlled encoding argument for insufficient capacity. “P did not learn” and an arbitrary singular-value threshold are not such evidence. Even adequate evidence only returns a width/topology hypothesis to Jason; there is no width sweep or automatic increase.

For each four-row group retain shared and fine weights/reference states; shared and fine formation terms; coarsening/reference pressure; effective spring; opening state; support and its timing; projection/clipping; and actual signed increments. Show component norms and alignment/cancellation as well as the final increment. Ask whether fine formation can be nonzero, whether pressure is always cancelled or clipped, and whether the allowed support changes the spring. No requirement says that fine deviations must grow monotonically or encode useful features. Opening takes 300 s, so a 30 s engineering trace was not an adequate opportunity assessment; a 600 s pilot still does not settle slow retention.

### 7.2 Packet loss and sustained adaptation

For mover passage and self-turning events chosen by predeclared physical annotations, preserve the full 20 native samples and boundary state for each 0.2 s wave, cortical trajectory, trapezoidal mean and endpoint, then centred packet/trace/query. Search these retained histories for pairs with different order, curvature or brief contact patterns but similar emitted packets. Select pairs by a documented distance in packet space and then show **all** candidate distances and native differences; a handpicked pair is an illustration, not a frequency estimate. Include exact manufactured same-mean/same-endpoint signals as a component demonstration of mathematical non-injectivity, labelled non-ecological, without evolving a world or changing P.

For stable light, chemistry and contact, use at least 180 s histories from the controlled holds where available and detached constant-input replays when a natural stable interval does not occur. Record receptor mean (30 s), cortical residual/activity and packet mean (60 s) throughout. Label synthetic replay input as such and preserve initial filter state; frozen versus evolving weights must be explicit. Reuse existing receiver operations only in a later authorized probe. In a constant-input receptor example the residual decays on the 30 s scale; that does not prove every downstream activity vanishes because recurrence, actual motion and weights still matter.

Determine where the physically needed distinction remains: raw channels, transient onset/offset, continuing changes, direct contact/proprioceptive motor route, or real E/I. The raw values existing in the observer do not make them available to P's associative path. There is no tonic light/chemistry bypass. Loss under sustained conditions is reported with durations and scope; do not remove centring or add a bypass to obtain a pleasing plot.

### 7.3 Scale, receiver influence and fading association

Keep separate records for sensory packet/query/support; context gate and actual map recall $q$; regulator feature input $B_q q$, actual-body term $B_v v$ and bias; the nonlinear features; each E/I bank's learned contribution; each bank's fresh exploratory perturbation; need weighting and bounded output; motor evocation; direct contact/proprioceptive feedback; oscillator/noise; regulatory current; attenuation; pre-attenuation tendency and actual command. Native/wave units and timing must accompany norms. Bias is not learned signal, and a large bodily coordinate in $q$ is evocation, not real restoration.

Opportunity to affect a receiver means more than a nonzero upstream norm. Record saturation and cancellation and, on at most 100 preselected handoffs/native samples per intact life, evaluate the **same frozen receiver once** with one additive contribution absent. The resulting feature/logit/tendency/command difference is a detached local sensitivity diagnostic, not an alternative trajectory or an estimate of behavioral benefit. Preserve the original state, RNG and outputs; do not use the result to normalize gains. Query/support changes require recomputing their defined immediate read dependencies in a detached state, not deleting an unrelated output vector. If exact receiver reconstruction cannot be verified, report contributions only and leave influence unresolved.

The implemented map-radius bound 0.1 with seven off-diagonal channels bounds the frozen-query recurrent read by 0.7 in the specified norm. With the implemented sweep leak, the four-sweep activity comparison contracts by approximately 0.759833 under frozen maps/query/context. Verify that precise condition in detached paired-state component probes and examine map norms, sweep residuals and actual q magnitudes in encountered states. Do not demand monotonic decay from a real time series driven by changing queries, maps and context. Weak long autonomous chains are expected in this branch; they do not falsify the broader association ambition. Near-zero learned q despite material inputs is a CO observation; poor learned relationships once material signals exist are SO.

### 7.4 Two actual bodily credit streams

For each E/I bank record actual reserve, old/new body filter, trend, prior applied perturbation and features, old/new eligibility, learning term, reference term, projection, parameter update and resulting separate contribution. Respect ordering: consequence credits previously applied perturbations/features before fresh perturbations are drawn. No credit from imagined bodily content, source labels or observer success events is allowed.

Energy can vary through expenditure/transfer; integrity needs real damage and restoration. Intact lives that never suffer damage cannot establish an integrity-credit failure. A detached replay of a controlled damage/repair history may demonstrate arithmetic opportunity in the exact bank operation, but cannot establish that intact P experienced it. Record both scopes. Equal-valued bank parameters are currently shared fields; a request for independent E/I numerical settings requires a reviewed schema/configuration change, not an undocumented split. Whether a bank strengthens helpful or harmful responses is SO, never a commissioning tuning objective.

## 8. Data, inspection and cost

### 8.1 Retain what diagnoses the current concerns

Keep native 100 Hz records, wave 5 Hz records, all contact/accounting events and complete restart snapshots. The baseline records have 2,513 native scalars and 13,685 wave scalars, plus event records. Native diagnostic input and endpoint transduction must remain separately labelled. Keep initial/final and existing 10 s snapshots; full matrices omitted from individual wave records can be reconstructed only from exact state plus verified replay. Do not claim that a norm trace contains a complete matrix. Additional passive records or replay must be checked not to change trajectory or consume random draws.

The existing inspectable view should be supplemented only with aligned plots and the controller displays needed above: physical ledgers; raw → residual → cortical trajectory → packet; shared/fine pressure; separate route contributions and E/I credit. A local file-based reader is sufficient. No database, platform, scheduler or new agent architecture is needed. Raw-only controller views and privileged observer views must be separated by construction.

Store compressed original streams and hashed manifests before derived plots; do not downsample evidence to meet an attractive budget. Record every initial state, field cache, seed/stream, executable/configuration/environment identity, controller input/action transcript, termination reason and rejected/failed trial. Declare a wall-time/storage stop as administrative only when it occurs cleanly before loss; an I/O error or incomplete stream is an apparatus failure with `complete=false`. No missing tail is silently reconstructed or counted as bodily death. On pause, preserve all state and verify continuation before relying on it.

### 8.2 Measured baseline and workload proposal

The final builder's [30 s birth manifest](REFERENCES/developmental_ecology/artifacts/smoke-birth_30s-attempt-004/manifest.json) records 140.714 wall seconds, 165,615,915 uncompressed record bytes and approximately 59.126 MB of stored files. That is **4.6905 wall seconds, 5.5205 MB uncompressed and 1.9709 MB stored per simulated second**. MB/GB here are decimal. These are short recorded engineering measurements, not new benchmarks or assured long-run throughput. The 1 s resume check includes duplicate advancement/verification and must not be substituted as a steady-state rate. Existing component-suite seconds are also not lifetime rates.

| Proposed class | Workload | Baseline-rate compute estimate | Stored / uncompressed estimate |
|---|---:|---:|---:|
| Physical ceiling A1–A5 | 3,080 simulated s | 4.01 h | 6.07 / 17.00 GB |
| Perceptual ceiling | 6 × 180 = 1,080 simulated s | 1.41 h | 2.13 / 5.96 GB |
| Intact newborn observations | 4 × 600 = 2,400 simulated s | 3.13 h | 4.73 / 13.25 GB |
| Fixed-structure diagnostic, if approved | 4 × 600 = 2,400 simulated s | 3.13 h | 4.73 / 13.25 GB |
| Total ceiling, excluding fixtures/replays | **8,960 simulated s** | **11.67 h** | **17.66 / 49.46 GB** |

Use full-P measured recording cost as a conservative planning proxy for external physical controllers; their actual implementation cost is unknown and may be lower or higher. These figures exclude human deliberation. Propose a separate **two-hour operator-time ceiling per controlled trajectory**, twenty hours for physical and twelve for sensory trials, with clean administrative pauses and no automatic extensions. That is a workload allowance, not a prediction. A staged pilot can stop after A0/A1 on a genuine apparatus defect; do not launch the entire list blindly.

Propose a twofold allowance on machine time (about 23.4 h) and recorded bytes (about 35.4 GB) for diagnostic overhead/variation, plus a second preserved copy: reserve roughly **72 GB** for compressed evidence and its duplicate. Avoid full decompression; if needed, budget another 50 GB. These are planning margins, not measured overhead or permission to discard records. If they exceed the available budget, Jason should reduce explicitly identified coverage or defer a layer; do not shrink native-rate evidence unnoticed.

The recorded 600 s prehistory preparation took about 65.18 wall seconds and produced about 0.095 MB of compressed fields for one phase. Its manifest retains an earlier runtime identity; the final delivery includes explicit dependency-based reuse verification. This timing is a historical preparation estimate, not a new 6bc9683b benchmark. Four additional life-specific caches would be about 261 wall seconds at that observed rate. Every other distinct controlled initial phase needs its own lawful history or a verified compatible cache; budget up to ten more such preparations (about eleven minutes) until the fixture inventory is fixed. The code's law checks and residual/history evidence remain required; 600 s preparation is not a proof of stationary chemical equilibrium.

Cheap identity, geometry and accounting fixtures should be run first in a later authorized task. Reserve up to one machine-hour and 1 GB for new component/replay diagnostics, an explicit unmeasured allowance to be revised from their first timing; do not extrapolate the old ~2.5 s unit-suite duration to newly written probes. Native histories already recorded support packet/capacity/scale analysis without extra world evolution. The [machine-readable estimate](COMPUTE_ESTIMATE.json) preserves the arithmetic and assumptions.

## 9. Conservative change and freeze protocol

The [configuration-change rules](P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md) are part of this design, not optional guidance. No automatic adjustment range or route is approved. For a suspected defect, preserve the failed configuration/data, identify the measure and class, isolate a law/implementation/configuration/controller cause, state the smallest proposed change and alternatives, then return the batch to Jason. Do not “repair” the original observations. A numerical proposal is not permission to change accepted Base World choices. A contradiction with a specified law is an engineering hold on the affected implementation, not a finding that P failed scientifically.

Packet construction, cortical learning law, pooling law, bodily credit, associative operation and regulator architecture require a separately specified **mechanism revision** and Jason's authority. Capacity/topology changes require the §7.1 evidence before consideration. Neither a little q nor a dead body automatically authorizes larger gains, more neurons, easier food or gentler damage.

### 9.1 Proposed freeze boundary

There is no freeze in this design contribution. Propose the following later boundary:

1. Jason accepts a specific commissioning plan, its information interfaces, validity interpretations and finite execution budget, and separately authorizes the apparatus work and executions.
2. The reviewed harness/observers pass identity, no-leak, ordering, accounting, record-completeness and non-interference checks. Physical witnesses and sensory availability evidence establish the scoped question the instrument can pose; unproven coverage is stated. CO records establish what pathways were exercised and what remains absent, weak or unresolved. Useful learning is not required.
3. A review disposition explicitly lists every AV defect, every CO concern, all failed configurations, all excluded/inconclusive measurements and the bounded scientific question still supportable. An unresolved AV defect relevant to that question prevents its evidential opening. A CO limitation may instead narrow the question, require more coverage, or justify a separately authorized branch; it is not erased by calling it science.
4. **Jason explicitly freezes the complete identified coupling and measurement contract** and separately authorizes any later evidential work. Finishing commissioning, producing a ZIP or making a commit cannot substitute for that ruling. Commissioning observations remain labelled commissioning; they are not silently promoted to evidential trials.

The freeze manifest must identify all law-bearing code and dependencies; exact configuration and hardcoded constants; body/world/material/transport/viability laws; sensor geometry/transfers/noise; cortical/packet/association/pooling/regulatory/motor laws; initialization and source/field/mover history; seed schedules and fixed anatomy; native/wave/solver cadence; horizon and reset/nonviability/pause rules; controllers/probes/deprivations; estimator definitions and denominators; record/inspection versions; validation evidence; permitted adjustment corridors (none proposed here); and the limitations accepted with the resulting question. **Learned state evolves under those frozen rules** and is not held constant in intact P.

After that explicit freeze, any change capable of changing experienced coupling, learner state updates, selection of observations or the meaning of a result creates a new identified branch. Preserve original settings, data and negative outcomes. A discovered apparatus bug invalidates only the claims/data whose dependency chain is affected, records that scope and requires revalidation before a new freeze; it does not justify relabelling a bad scientific outcome as a bug. A display-only repair may remain a documented non-trajectory patch only after its unchanged inputs, records and interpretation are demonstrated.

Examples of **SO that must stand** under a valid frozen instrument: association learns poor relationships despite material signal; cortex develops nuisance distinctions despite adequate information/capacity; separate credit strengthens harmful responses; the organism dies despite physically and perceptually available recovery; P's participation–retention link provides no useful benefit. These are not reasons for gain balancing, larger capacity, wider repair strips, extra reserve or easier resource placement.

## 10. Completion and genuine gaps

This contribution designs bounded checks and records; it does not assert any new physical, sensory, bootstrap or developmental result. The final review was already registered, so the live status keeps that exact checkpoint and links this design-only continuation without duplicating the review or replacing earlier holds.

The necessary remaining engineering gaps are the unbuilt extended commissioning harness, information-isolated controller views, reviewed fixed-structure adapter (if chosen), additional passive diagnostics/reconstruction checks and measured overhead for those additions. The human reference's capability and the finite fixture manifest need approval before negative interpretations. These gaps can be resolved from the packaged sources and later scoped engineering work; no missing broad literature survey or original-chat export prevents review of this design.

The most consequential review choices are the raw-only human reference versus a separately specified automated controller, the proposed paired fixed-structure diagnostic, the finite coverage/time/storage budget, and the explicit no-rescue change/freeze rules. They are consolidated in [the decision list](DECISIONS_REQUIRED_BEFORE_EXECUTION.md). Stop here for Jason's review.
