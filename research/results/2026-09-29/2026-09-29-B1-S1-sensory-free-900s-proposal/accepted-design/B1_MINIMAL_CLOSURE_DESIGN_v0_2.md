# B1 minimal closure design v0.2

**PROPOSAL FOR JASON REVIEW — DESIGN ONLY.** No implementation, new simulation, fixture construction, prehistory generation or execution authority. Apparatus ancestry is resolved in `APPARATUS_PROVENANCE_CLARIFICATION.md`; `352f73ff` remains the last independently reviewed checkpoint. P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.

The target is one existence witness: **can a fixed external controller, using only organism-permitted sensory history, obtain a real productive energy-source interaction?** Use three new held-out starts and three arms per start, each capped at 30 seconds. No learned model, fitting, decoding benchmark, development cohort or extension. v0.1 is preserved but **NOT SELECTED**; its campaign would exceed this minimum closure question.

## Proposed controller: steer toward measured chemistry, ease into contact

The source supports a credible simple candidate without training. Two chemistry receptor sites sit 45° to either side of the body's forward direction. Comparing their readings provides a local directional cue. A stronger left reading calls for a stronger right actuator, which produces a left turn under the actual force law. When front contact appears, use a small equal push to maintain gentle contact. If that contact disappears, return to chemical steering.

This is an external assay instrument. Its constants and state are never inserted into P. It does not recognize sources: repair surfaces also emit chemistry, depleted sources still emit, multiple emissions can oppose one another, and contact does not identify material. It can therefore approach the wrong object or lose contact. Those are retained limitations, not reasons to add a planner.

The proposed constants below are fixed together from the channel/actuator scales and scalar mechanics, **not fitted to a trajectory or the old human B1 readings**. Approval would freeze them before exact held-out states are constructed or any held-out response is examined.

### Exact proposed law

Decide at the existing 0.1-second command boundaries. Use the latest ten available native rows (the previous hold); at the initial decision use the single birth row. Never request a future sample. Reset the two-state controller and its release counter for every case.

For each measured chemistry coordinate $r$, undo only its known receptor saturation:

$$g(r)=0.05r/(1-r).$$

Let $q_j$ be the mean of $g(r_j)$ over that window. The implemented order is right-front coordinates 0,1 and left-front coordinates 2,3. Define

$$R=(q_0+q_1)/2,\quad L=(q_2+q_3)/2,\quad b=(L-R)/(L+R+10^{-12}).$$

This is algebra on measured receptor values, not an analytic source gradient or access to the field grid. There is no chemical demixing, source label, fitted normalization or changing gain. Nonfinite readings or chemistry outside $[0,1)$ cause an instrument stop before another command; do not silently clip a saturated value or switch policies.

In **SEEK**, with $p_4$ the latest raw `proprioception_4`:

$$d=\frac{0.30}{1+4|b|},\qquad a=\operatorname{clip}(2b-0.20p_4,-0.40,0.40),$$
$$u_L=d-a,\qquad u_R=d+a.$$

Thus stronger imbalance turns more and reduces forward drive; angular proprioception supplies modest damping. The commands already lie within $[-1,1]$. Equal readings produce forward motion, not an inferred source direction. The controller uses no global pose or integration of a privileged heading.

Let $C$ be the maximum raw reading over contact sectors 7,0,1 and the same window. Sector 0 is front, 1 front-left and 7 front-right. If SEEK sees $C\geq0.05$, enter **HOLD immediately** and issue $(0.05,0.05)$. In HOLD, keep that pair. After three consecutive decision windows with $C<0.02$, return to SEEK on that third decision; a window at or above 0.02 resets the release counter. No material classification, target-specific hold duration, escape search or success-based stopping is added. The 0.30-second release hysteresis is controller memory, not extra simulation.

Source basis: `loom_p/geometry.py::transduce`, `loom_p/physics.py::{actuator_forces,free_velocity,advance,account}`, `loom_p/chemistry.py::FieldSolver.emission` and unchanged `developmental_ecology/configuration.json` at `b684912e`. Exact file hashes accompany the proposal.

### Why 30 seconds is a plausible bound, not a promised outcome

At baseline $E=0.7,I=1$, each actuator's force coefficient is 0.38. Equal commands of 0.30 give a straight free-motion terminal speed of 0.228 world units/s; the fixed-reserve continuous drag calculation gives about 6.61 units over 30 seconds from rest. Turning and changing reserves reduce or redirect that travel. The proposed source-surface gaps below are only 1.25–2.25 units. This establishes a reasonable local scale, not reachability under the coupled field.

For differential command $a$, the same scalar mechanics give terminal angular velocity $1.33a$ rad/s before feedback and reserve changes. The sign is correct and the maximum magnitude is about 0.532 rad/s. No manufactured world or controller trajectory was run to choose these constants.

In ideal stationary frontal contact, the 0.05 hold yields total force approximately 0.038 and exchange quality approximately 0.275. At full source stock and $E=0.7$, the corresponding initial gross transfer rate is about 0.00330 energy/s. This shows a nonzero productive hold is compatible with the laws. Actual stock, slip, impact, geometry and reserves determine the recorded transfer. Neither positive net energy nor survival is a gate.

## Exact runtime boundary and three arms

| Arm | Permitted controller input | Fixed behavior |
|---|---|---|
| FULL | Existing causal 29-coordinate raw history, held actual E/I at the existing 0.2 s handoff, causal times/indices and own previous commands | Law above; reads only chemistry, front contact and angular proprioception. Other permitted channels and E/I are unused. |
| CHEMISTRY-HIDDEN | Same projection with all four chemistry coordinates omitted from every current/past row: 25 coordinates, chemistry explicitly unavailable | Same constants, contact states and proprioceptive damping. Set the law's imbalance variable $b=0$ by the declared missing-modality branch; do not fabricate zero chemistry readings. |
| SENSORY-FREE | No raw channels, E/I, world status or scene-dependent history | Issue the same predetermined pair $(0.30,0.30)$ at every request, for all three starts. No contact response or outcome-dependent command change. |

All arms use the existing paired actuators and 0.1 s hold. Native raw recording stays at 0.01 s; E/I sampling stays at 0.2 s. Chemistry remains physically active and privately recorded in every arm. FULL and HIDDEN are the same fixed law with one declared deprivation, not separately tuned controllers. The fixed null sequence tests whether ordinary forward actuation already obtains the interaction; it is not an optimized open-loop competitor.

The controller receives only a copied, allowlisted sensory projection and its own bounded internal state. It gets **no global position/orientation, source position/identity/stock, map, field grid, analytic gradient, material identity, evaluator event, future state, fixture/seed identifier, privileged stop reason, snapshot/file path, annotation text or Engine reference**. An arm's modality availability is allowed; a case identity is not. Administrative metadata and evaluator records remain outside the controller. At termination the runner stops asking for commands rather than passing a private reason into the law.

There is no teacher, training data, runtime privileged helper, online adaptation or feedback from evaluation. Initial controller memory is empty SEEK, with zero release count. Its output is only one command pair. P neural activity/plasticity remains inactive during external control. No human UI work is required.

## Three starts, nine cases maximum

Propose these **new manufactured commissioning starts**, all noncontacting and at rest, with baseline birth $E=0.7,I=1$, zero angular velocity/command/contact history, and full source stocks under the existing lawful birth/prehistory convention:

| Start | Initial body–source surface gap | Source bearing relative to forward | Cases, each ≤30 s |
|---|---:|---:|---|
| S1 | 1.25 world units | +45° left | S1-FULL, S1-HIDDEN, S1-SENSORY-FREE |
| S2 | 1.75 world units | −45° right | S2-FULL, S2-HIDDEN, S2-SENSORY-FREE |
| S3 | 2.25 world units | +60° left | S3-FULL, S3-HIDDEN, S3-SENSORY-FREE |

Exact placements are to be frozen **after the controller law**, at three distinct existing sources in open approach regions of the unchanged Base World. Use geometry alone: initial nonoverlap; the short body-width approach corridor clear of other fixed solids and the mover's swept region; starting forward rays do not intersect a source within the nominal 30-second travel envelope. Do not move a source, clear an obstacle or select by chemical gradient, controller behavior or transfer outcome. These deliberately local opportunities ask whether access exists, not whether an arbitrary blank organism can discover a remote source. They do not pose mover competence or a new navigation objective.

The listed bearings and finite-body gaps keep a straight heading from automatically striking the intended source. Validate all-source geometry as well, so the fixed null is not accidentally guaranteed success elsewhere. If the three specified geometries cannot be placed lawfully, report that before launch; do not search alternative angle/gap settings.

Reuse one existing verified, non-human A-series world-only prehistory cache and its matched phase across starts if its law/stock/phase provenance is compatible. The source permits body-absent prehistory followed by birth insertion. Freeze the selected cache identity, exact states and construction rule in a later reviewed packet. Do not reuse or inspect the old human B1 fixture; sharing public world laws is not reuse of that fixture. If lawful reuse cannot be established, stop for a preparation-cost decision, not automatic new prehistory generation.

Within each start, all three arms receive copies of the **identical complete physical initial state**, including field, mover phase, stocks, body and random-stream state. They then evolve independently under their own commands. Do not force subsequent histories to match. Different starts vary placement and orientation, not physics. “Held out” means these exact states/responses are unavailable for adjusting the frozen controller; it is not a claim of random population sampling.

Proposed fixed order: S1 FULL/HIDDEN/SENSORY-FREE, then S2 in that order, then S3. Freeze every case before any execution. Complete the declared set even if a witness occurs early, unless a terminal, apparatus or administrative stop prevents it. Retain misses, contacts, damage and cutoffs. No retries, substitutions, continuations or extra cases.

## What is enough to close B1

Recommend closing this minimum access question when at least one held-out FULL case has **real source contact plus resolved positive source-debit/body-credit transfer**, and its matched SENSORY-FREE case completes a fair comparison without a productive interaction. The recorded FULL command trace must show the stipulated permitted-sensor feedback actually changing the commands. An incomplete null or a feedback-boundary violation cannot supply this contrast. Report every other case, including failures; one witness is not a success-rate claim.

Resolve transfer using the existing external event ledger: actual source contact, debit and equal gross body credit, with renewal and expenditure accounted separately at the existing numerical tolerances. A barely positive number inside accounting uncertainty is unresolved. The controller never sees this evaluation. Net E can fall despite productive transfer.

The allowed positive claim is:

> A fixed external controller restricted at runtime to the organism's permitted sensory history produced a bounded productive source interaction under held-out starting conditions.

CHEMISTRY-HIDDEN need not fail for closure. Report only its paired bounded difference in interaction and transfer. No chemistry necessity, optimal sensing, general navigation, source recognition, P learning, developmental efficacy or survival competence is established.

| Pattern | Disposition |
|---|---|
| FULL productive; matched completed null unproductive; boundary intact and feedback active | Sufficient bounded feedback witness under the proposed closure rule. |
| FULL and null both productive, with no other distinguishing start | Productive interaction observed, but insufficient attribution to feedback under this rule. Return to Jason. |
| FULL misses; HIDDEN/null succeeds or also misses | Preserve the limitation. No inference that sensory information is absent. Return to Jason. |
| All FULL cases miss, or ambiguity/contact-only/unresolved transfer remains | B1 unresolved by this simple instrument. Stop; no learned-controller escalation or tuning. |
| Leak, incompatible law/cache, material apparatus defect or administrative cutoff | Preserve records and stop the affected execution; halt the batch for a shared defect/resource breach. Do not substitute a case. |

The per-case report needs only contact, resolved transfer, first interaction time, expenditure, initial/final E/I, damage, feedback command trace and terminal/controller/administrative status. Keep native evidence at existing fidelity. No passive decodability score or extra objective is added.

## Cost and review boundary

Maximum new bodily evolution: **9 × 30 = 270 simulated seconds; 27,000 native steps; 2,700 holds**. Measured A2/A3 throughput projects **52.90–53.70 minutes** of base simulation; A5 gives **55.11 minutes**. Additional sensory-history serialization, verification and packaging are unmeasured. There is no model fitting or human deliberation allowance. For a later packet, propose a 10-minute per-case / 90-minute aggregate execution ceiling and a separate 30-minute reporting allowance; exceeding a bound stops work rather than buying more simulated time.

Using the existing conservative B1 recording allowance unchanged, primary case artifacts project **8.95 GB** for nine cases, or **17.89 GB** if a second complete copy is made. This includes unnecessary human annotation/display allowances, so it is conservative, not a measured automated-controller size. Do not redesign storage or reduce fidelity to lower the estimate. A later launch packet must count all retained copies and reserve, bind a finite storage cap and verify free space; the old human cap/grants do not authorize this batch. New prehistory is excluded and would require a separate decision if cache reuse fails. Exact arithmetic and source records accompany this document.

The existing apparatus has no automated raw-sensory authority kind. A future narrow build would add that explicit kind, the pure fixed law, allowlist/projection validation and bindings in the existing runner/authority path. Use manufactured component checks for sign/order, identical decisions, HOLD transitions, missing chemistry, no forbidden inputs/carryover, cadence and stop enforcement. No world-running shakedown or development cohort is part of this proposal. If this cannot be done credibly without substantial search/training, stop before building or launching and report the blocker.

Human FULL-RAW remains unchanged at **20.2 s / 202 human commands**, as a bounded qualitative observation only. Jason reports live/coherent channels, changes consistent with movement/interaction, conceivable navigation after familiarization, and prohibitively inefficient manual 0.1 s entry. These are operator reports, not a quantitative B1 PASS. Human CHEMISTRY-HIDDEN remains **authorized-but-not-executed / withdrawn**, at **0 s / 0 steps / 0 commands**. Its prior prepared world/timer remain in the audit history. Both sealed evaluator holdings remain undisclosed.

This is the proposed last bounded perceptual closure before P developmental testing unless a material defect emerges. The accepted current-world-first developmental-selection direction is unchanged; no population, founder criterion or nursery is designed here. **Stop for Jason's review.** No controller has been implemented, no new trajectory or prehistory has been run, and no authority has been created.
