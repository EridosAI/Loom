# Base World Completion — v0.1

**Project:** Loom / PAM — Developmental Ecology  
**Consolidation date:** 2026-09-05 (Australia/Perth)  
**Prepared by:** Astra, design seat, from the accepted decisions in this conversation  
**Decision status:** JASON-ACCEPTED WORKING BASELINE, with accepted review amendments and explicit open details  
**Document status:** Repository continuation recording Jason-accepted Base World decisions; commit identity is available from Git history. This wording has not received a separate verbatim verification by Jason.  
**Repository status at preparation (2026-09-05):** Not committed by this task; no repository write performed.  
**Foundation reference:** `EridosAI/Loom`, `restructure/developmental-ecology` at `103973f6646a4c12ac817cb085e0456f19f77cb9`  
**Authority:** Records accepted functional decisions; does not freeze numerical configuration.  
**Implementation / experiment / run authority:** None. No neural mechanism is selected.

---

## 0. Reading and authority

### 0.1 What has closed

The Base World Completion **functional review** is complete. Jason accepted the review amendments, selected wall-only restoration as the starting placement, selected solid-body influence on chemical transport, and accepted the consolidated baseline as a revisable starting point. Exact acceptance excerpts and source identities are retained in §16.

This document consolidates those decisions. It is not another proposal to accept Sol's original packet wholesale. The original packet's provisional numbers and the provisions corrected in review do not become accepted requirements merely because the baseline was accepted.

The version number identifies this first consolidated file. It is not an experiment number and does not identify Sol's earlier conversational document, which was titled **“Base World Completion — Review Packet v0.1.”** The `BWC-1` through `BWC-12` labels below preserve that packet's topic identifiers, not new experiment or fork numbers.

### 0.2 Revisability condition

**[ACCEPTED WORKING — Jason's acceptance condition, consolidated wording]**

> This baseline is accepted as a coherent starting configuration. Its settings and functional choices remain research hypotheses and may be revised as the organism–world coupling is understood. Acceptance does not establish optimality or developmental sufficiency. Changes retain their reasons and provenance; a frozen evidential configuration is preserved rather than retrospectively altered.

Freezing protects the interpretation of a particular set of observations. It does not freeze the research programme. Wall-only restoration is the starting branch, not a claim that restoration belongs on walls in every useful ecology.

### 0.3 Status vocabulary

| Label | Meaning here |
|---|---|
| **ACCEPTED WORKING** | Jason accepted this starting functional choice. It remains revisable through an explicit decision. |
| **ACCEPTED AMENDMENT** | A reviewed correction or qualification accepted by Jason; it controls the corresponding original proposal. |
| **OPEN** | No exact realization, value, criterion or mechanism has been selected. |
| **PROVISIONAL EXAMPLE** | A retained numerical or implementation candidate, not a validity gate, instruction to build, or frozen constant. |
| **ANALYTICAL CONSEQUENCE** | Reasoning conditional on the stated model assumptions; not experimental evidence. |
| **DEFERRED DIAL** | An explicitly available later variation, not part of the current starting configuration. |
| **SUPERSEDED PROPOSAL** | Original wording not to be inherited as an active requirement. |

### 0.4 Relationship to the foundation

Read `00_LOOM_CURRENT_STATE.md` first, then `DEVELOPMENTAL_ECOLOGY_DESIGN_FRAME_v0_2.md`, `PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1.md`, this file, and `DEVELOPMENTAL_ECOLOGY_DECISION_LEDGER_v0_2.md`.

The four foundation files at the pinned commit retain authority for their original content. This file records the later conversation-accepted completion of their expressly open Base World layer. It does not silently amend their other accepted forks or promote their labelled hypotheses and proposals.

The original specification's statements that arena shape and placement are open, and its instruction to prepare this packet, describe the earlier stage. Their disposition is explicit here: square is the starting arena; restoration starts on walls; solids affect chemistry; the packet is functionally accepted. Numerical and mechanism dependencies remain open.

EXP1–21 remains historical evidence under `EXP1-21/`. No historical result, experiment sequence, artifact or module is modified. Historical method is used only for the measurement and provenance protections expressly retained in the accepted review. No historical threshold or neural implementation is imported.

**Sources:** [S1–S4], conversation records [P0], [R1], [J1], [C1], [J2], [J3] in §16.

---

## 1. Accepted starting world at a glance

The organism lives continuously in a bounded square, non-wrapping 2D arena with perceptible physical walls. It has the accepted compact oriented body, paired low-level actuation, directional two-band light and two-component chemical sensing, contact, proprioception, and separate energy/integrity interoception. Structured spontaneous activity is present from birth; its mechanism remains open.

The environment contains several anchored, compact, finite renewable energy sources; several separate homogeneous restorative surfaces placed against walls; and one persistent non-agentive block moving continuously back and forth on a fixed path. The mover is consequential but avoidable. General pushable furniture remains absent.

Energy sources start full. Birth integrity starts full; birth energy starts at a fixed non-maximal reserve whose value remains open. Source and restoration functions remain causally separate. World state persists throughout each life. The small material palette produces lawful optical, chemical and mechanical consequences, and solids affect chemical transport.

| Design layer | Accepted disposition |
|---|---|
| Spatial convention | Body-relative length; distinguish nominal count area, static accessibility and time-dependent mover accessibility. |
| Inventory | Counts derived from area-related availability; exact coefficients, integer floors, counts and fixture sizes remain open. |
| Energy | Identical finite source laws initially; continuous exponential renewal as the starting model; shared transfer accounting; no single-source sustainable camping. |
| Integrity | Wall-only, anchored, initially non-depleting restoration; usable damaged-state recovery and return to energy must be commissioned. |
| Materials | Background medium, neutral structural, energy-bearing, restorative and organism roles; labels stay inside the simulator. |
| Birth | Explicit safe birth-position law; uniform orientation and mover time-phase; other state initialized lawfully; required physical dependencies retained. |
| Chemistry | Persistent pre-evolved field with solid-body interaction; jointly lawful field/body/mover history, not an arbitrary snapshot-phase pairing. |
| Replication | Independent new lives; no inherited learned state or prior life's depleted world state in this baseline. |
| Evidence | Commission the complete coupling, then freeze the laws and measurement configuration; no commissioning trial is silently promoted into evidential data. |

**Sources:** [S2] §§8–14, 19–20; [S3] §§1–16; [R1], [C1], [J2].

---

## 2. BWC-1 — Arena shape and area convention

**Accepted ruling.** Start with a square arena bounded by ordinary perceptible walls. Use the organism's healthy-birth collision-envelope diameter, `D_b`, as the reference length. The final body geometry is not chosen by this unit convention. Where an orientation-independent enclosing envelope is used, identify it as a conservative geometry convention rather than claiming it is the exact configuration space of every possible body shape.

Retain `A_U` as **nominal body-accessible area before fixtures**: the area available to the body centre inside the wall boundary after accounting for its collision envelope, before inserting sources, restorative fixtures and the mover. This is the count-law denominator and avoids making source count recursively depend on the area occupied by those same sources.

Correct the original `A_N` wording. Static-fixture-accessible area excludes fixed fixtures, not the mover's entire swept region as though it were permanently occupied. Mover collision occupancy and accessibility vary with time. An **always-clear bypass map** is a separate useful safety measure. It must not replace the map used to assess entering and crossing the mover's route at appropriate times.

**Reason.** The square is a coherent simple starting geometry with corners, persistent landmarks and alternative routes. Distinct area measures prevent nominal density, usable space and permanently safe space from being confused.

**Main risk.** Body-envelope approximations may overstate obstruction, and nominal density may poorly describe experienced availability once fixtures are installed. Geometry-specific behaviour limits generality but is not automatically invalid.

**Commissioning requirement.** Report the nominal area, actual static accessibility, collision-clear routes, mover-dependent access and safe bypasses. Verify access to both viability pathways with the actual body and actuation, including turning and contact. Do not infer access solely from point-agent distances.

**Reversibility / later dial.** Arena dimensions and body-to-arena scale remain numerical dials. Other arena shapes remain deliberate later variations. Square is not asserted superior to them.

**Jason review.** Starting choice accepted. Exact geometry and numerical settings return in the configuration process; a functional change requires Jason's decision.

**Sources:** [S3] §§3–4, 10.3; [P0] BWC-1; [R1] amendment 4; [C1], [J2].

---

## 3. BWC-2 — Energy-source density and count law

**Accepted ruling.** Specify source availability relative to `A_U`, with a deterministic, explicitly defined conversion from area and density to an integer source count for a selected manifest. The starting ecology has several persistent, anchored, compact energy sources. Do not independently randomize source count between lives of that same manifest.

Exact density, minimum count, rounding implementation, source footprint and final count remain open. The original `1/(300 D_b²)` density, six-source floor and eight-source example are retained only in the non-operative proposal record in §15. They are not numerical working doctrine.

Report realised density against static-accessible area as well as the nominal count density. Source contact size is part of accessibility; equal counts need not imply equal encounter opportunity.

**Reason.** Area-based availability preserves the accepted ecological framing while actual encounter/revisit measurements determine whether the body can use it.

**Main risk.** An ecology can be too sparse for a first useful interaction, or so abundant that the intended need for organised interaction largely disappears. Either conclusion requires coupling evidence, not nominal density alone.

**Commissioning requirement.** Measure first productive encounters, subsequent different-source travel, same-source revisits, stock on arrival, spatial coverage, and encounter support across sources and births. Retain non-encounters and terminal failures. Check chemistry is informative without being effectively flat or saturated throughout the arena. Evaluate spontaneous-only operation over a declared horizon; do not claim a finite trace proves an infinite-horizon property.

**Reversibility / later dial.** Density, count, source size and later capacity heterogeneity remain available variations. Selection and adjustment must have recorded grounds independent of hoped-for developmental success.

**Jason review.** The area-based inventory relationship is accepted. Numerical choices and their permitted adjustment routes are not yet ratified.

**Sources:** [S3] §§8.2–8.4, 15; [S4] A9.1; [P0] BWC-2; [R1] amendments 1 and 6; [J1–J2].

---

## 4. BWC-3 — Restorative-surface density, count and placement

**Accepted ruling.** Begin with **wall-only placement** of multiple anchored, extended, homogeneous restorative surfaces. Each restorative surface is its own body adjacent to a wall; this does not introduce composite material bodies. Start with non-depleting restorative surfaces, while energy continues to fall during residence.

Availability is considered relative to world area, but record both the number of opportunities and their **exposed contact length**. Also record how much suitable perimeter is occupied. Exact count, density, length, spacing and geometry remain open. The original three-surface floor and six-body-diameter strip length are examples, not accepted minima.

Wall-only placement is a starting ecology. Freestanding and mixed placement are explicit later variations. Jason's reason is that different placements can give rise to different behaviour, which the programme wants to investigate; no behavioural difference has yet been demonstrated.

**Reason.** Wall-adjacent surfaces provide an intelligible initial opportunity for sustained gentle contact without adding freestanding barriers. Treating placement as an ecological variable preserves its scientific interest.

**Main risk.** Repair availability may become excessively coupled to wall-following, or strip geometry may require precise contact the newborn cannot approximate. An area-scaled count law may also outgrow the available perimeter.

**Commissioning requirement.** Check strip packing and separation jointly. Fixed strip length with area-scaled counts cannot be assumed to fit at arbitrary arena scales because area and perimeter scale differently. Measure strip encounter support, repair-eligible dwell, actual integrity restoration under deficit, and energy remaining to leave repair and return to an energy opportunity. A full-integrity contact alone does not verify restoration.

**Reversibility / later dial.** Wall-only ↔ freestanding ↔ mixed placement; count, exposed length, depletion and material diversity remain explicit dials. No variant is authorised to run here.

**Jason review.** Wall-only start and later placement variation explicitly accepted in [J2]. No further acceptance of that same choice is owed.

**Sources:** [S3] §§9, 11.4; [P0] BWC-3; [R1] amendments 2 and 4; [C1]; [J2].

---

## 5. BWC-4 — Placement and separation constraints

**Accepted ruling.** Choose placements by recorded, outcome-blind geometric and coupling-validity rules, not by developmental learner performance. Retain the relational intent of the original placement proposal: dispersed opportunities, usable contact access, separation of the two restoration pathways, and an avoidable but consequential mover.

The mover's path must intersect a recurrently useful route or region without becoming the sole gate to energy or integrity restoration. Waiting, crossing, retreat and detour remain legitimate possibilities. Source and repair placement must not collapse both needs into one indefinitely sufficient attachment point. Safe alternatives must be feasible in reserve and bodily capability, not merely present on a geometric map.

The original numerical clearances and detour ratio are not binding. There is no general ban on grids, symmetry, useful corners or regular spatial structure. A seeded irregular sampler is an available placement implementation, not a doctrine requirement. Fixed world laws must not become an adaptive sequence of lessons designed around learner progress.

**Reason.** Placement should pose the accepted situation while allowing the organism's own history to organise behaviour. Learnability does not require adversarial decorrelation.

**Main risk.** Too many individually plausible placement restrictions can amount to an authored training route. Too few checks can leave traps, inaccessible repair, or a nominally avoidable mover that reserve makes unavoidable in practice.

**Commissioning requirement.** Retain layout manifests, rejection reasons, physical/geodesic route information, actual-body clearance, source/restorative exposure and mover bypass support. Distinguish always-clear paths from time-dependent crossings. Do not require a particular behavioural repertoire or every source to receive equal traffic.

**Reversibility / later dial.** Fixture layout, separation and placement distribution remain dials with explicit versioning and outcome-independent selection grounds. The final manifest freezes with the complete coupling.

**Jason review.** Relational placement requirements accepted; exact rule set, numerical envelopes and autonomous adjustment routes remain to be specified.

**Sources:** [S2] §10; [S3] §§3.2, 10.3, 15; [P0] BWC-4; [R1] amendments 1 and 4; [J1–J2].

---

## 6. BWC-5 — Capacity, renewal and recovery relationships

### 6.1 Energy stock and exchange

**Accepted ruling.** Start with identical finite energy sources under continuous exponential renewal. Sources persist through depletion; there are no scheduled refills, disappearance or random respawn. Contact-mediated exchange is graded and bodily uptake saturates near capacity.

In source-stock units that represent transferable bodily energy, the retained starting model is:

\[
\dot S_i=\frac{C_S-S_i}{\tau_S}-U_i,\qquad
\dot E=\sum_i U_i-P_E.
\]

Here `S_i` is available stock, `C_S` is its capacity, `τ_S` is the renewal timescale, `U_i` is **actual** successful transfer, and `P_E` is bodily expenditure. This is a starting physical-accounting model, not a selected numerical integrator or exact contact law. The same actual transfer is debited from the source and credited to the body. Source stock and bodily capacity constrain transfer; clipping source stock must not leave unmatched energy credited to the organism.

The local-insufficiency relationship must hold against the lowest continuing expenditure compatible with viable attachment. Under a genuine lower bound `P_E ≥ P_b` and the one-source accounting above:

\[
\frac{d(E+S)}{dt}
=\frac{C_S-S}{\tau_S}-P_E
\le \frac{C_S}{\tau_S}-P_b.
\]

**[ANALYTICAL CONSEQUENCE]** If `C_S/τ_S < P_b` across the relevant viable states, the combined finite reserve declines under single-source attachment. This gives an analytical anti-camping condition for that model. It is not an experimental result. `C_S/τ_S` is the maximum replenishment rate, not the demonstrated rate harvested by an organism moving around the realised ecology.

Gross transfer during a long contact can exceed initial stock because renewal continues. Net bodily gain must instead be interpreted with expenditure and stock accounting. A claim that one source cannot refill a “deeply depleted” organism needs a defined starting deficit and the stated assumptions; the adjective alone is not a criterion.

Retain stable source chemical character with stock-dependent magnitude as the starting sensory relation. The reviewed packet's nonzero depleted-emission floor and affine stock-to-magnitude form remain provisional realizations, not frozen coefficients. Depleted sources remain persistent material causes; the availability of their identity is assessed through actual sensory consequences rather than a supplied ID.

### 6.2 Integrity recovery and return to energy

Integrity restoration remains a separate world-mediated pathway. Energy sources do not repair integrity; restorative surfaces do not supply energy; there is no direct energy-funded repair conversion in this baseline.

**[ACCEPTED AMENDMENT]** Commission the whole relationship **damage → recoverable deficit → meaningful restoration → return to energy**, not merely the existence of a repair surface. Ordinary non-terminal stress must sometimes leave recoverable states; graded capability loss must not eliminate recovery too early. Repair must be approachable through imperfect contact, not only by a highly competent controller.

For a repair interval followed by travel without energy intake, the relevant conditional energy check includes:

\[
E_{\mathrm{arrival}}-
\int_{\mathrm{repair\ and\ subsequent\ travel}}P_E(t)\,dt
>E_{\mathrm{terminal}}.
\]

This records the accepted recovery-budget relationship. The terminal threshold, damage law, restoration law and quantitative recovery requirement remain open. It does not require recovery from every damaged state.

**Reason.** Local depletion makes action change both organism and world; recurrence makes stock history relevant. Usable integrity recovery prevents the second viability dimension becoming an effectively irreversible counter.

**Main risk.** Apparent global viability may consume initially full stocks without becoming renewal-supported. A controller that avoids all damage may appear to certify the integrity pathway without ever using it. Conversely, repair can be physically reachable but energetically unusable.

**Commissioning requirement.** Track source stocks, actual transfers, renewal and separate bodily reserves. Establish physical and perceptual viability under actual travel/contact costs; do not infer it from a sum of maximum renewal rates. Distinguish transient stock consumption from recurring renewal-supported operation. Assess restoration in damaged-but-viable states and separate arrival, repair-eligible contact, positive restoration, and departure viability.

**Reversibility / later dial.** Capacities, renewal and uptake rates, emission coupling, restoration rate and depletion status remain dials. Heterogeneous sources and stronger direct viability coupling remain later variations.

**Jason review.** Relationships and accounting amendment accepted. Detailed laws, values and criteria remain configuration decisions; no verification has yet occurred.

**Sources:** [S2] §14; [S3] §§7–9, 15; [P0] BWC-5; [R1] amendments 2–3; [C1]; [J1–J2].

---

## 7. BWC-6 — Birth reserve and expenditure

**Accepted ruling.** Start each independent baseline life at full integrity and a fixed non-maximal energy reserve. The actual birth-energy fraction is open. `E_max = 1` and `I_max = 1` may be used as separate unit conventions; they are not a combined viability score.

Retain positive continuing basal expenditure plus an actuation-effort contribution. The original linear effort formula is a provisional realization. Expenditure is bodily accounting, not a reward for a good action, a penalty for a bad action, a learned utility, a loss-dependent fee, or a charge linked to model size. The exact effort units and relation to impaired actuation remain to be specified.

Begin without passive integrity decay: integrity loss arises through the accepted physical stress pathway. Full birth integrity avoids assigning an unexplained initial injury. Low energy and low integrity still have their separate embodied valence and capability consequences; encoding, magnitude and motor interaction are mechanism/configuration dependencies, not resolved by this packet.

**Reason.** Non-maximal energy permits early need while reserve and robustness allow experience to accumulate. A continuing basal cost prevents quiescence from trivially eliminating bodily need.

**Main risk.** Reserve or expenditure can make exploration terminal before learning is possible, or remove meaningful need for organised interaction. Initial full stocks can disguise an unsustainable long-run relationship.

**Commissioning requirement.** Measure no-intake trajectories, expenditure during movement and repair, unconditional first useful interaction probability, remaining reserve after that interaction, further encounter opportunities, and damaged-state recoverability. Do not calculate first-contact success only among survivors. The original 90th-percentile first-contact bar is not accepted. A first contact immediately followed by unavoidable terminal failure does not alone establish adequate developmental runway.

**Reversibility / later dial.** Reserve fraction, cost form and coefficients, sampled birth conditions, passive decay and stronger bodily coupling remain revisable through explicit decisions.

**Jason review.** Starting birth conditions and expenditure decomposition accepted; exact values and capability functions remain open.

**Sources:** [S2] §§9, 14; [S3] §§7, 15; [P0] BWC-6; [R1] amendments 1–3; [C1], [J2].

---

## 8. BWC-7 — Encounter/revisit commissioning measures

**Accepted ruling.** Retain the foundation's physical ceiling, perceptual ceiling and bootstrap floor. They pose different apparatus questions and do not become organism components.

| Apparatus perspective | What it is intended to establish | What it does not establish |
|---|---|---|
| Privileged physical controller | Useful viability interaction is physically possible with the actual body and world. | Newborn discoverability, sensory accessibility or developmental learning. |
| Raw-sensory controller and relevant sensory-deprived comparison | Useful structure reaches the organism's actual sensory windows. | That the developmental organism can yet exploit it, or that every modality/material must be independently classifiable. |
| Fixed newborn spontaneous process without learning | Sometimes reaches a first useful partial or complete interaction, with potential for further experience. | A required success percentile, a mechanism for learning, or infinite-horizon viability from finite observation. |

These controllers act in **separate commissioning trials** and necessarily affect the trajectories they control. Measurements attached to an evidential organism must instead be trajectory-inert: observing cannot feed information, change random draws or modify its development.

### 8.1 Measurement set

The following specifies the information to retain, not numerical pass bars or a preregistered outcome table.

| Measurement family | Required distinctions |
|---|---|
| First energy opportunity | First contact versus first positive actual energy transfer; non-encounters and death before transfer remain in the record. |
| Energy revisit | Same-source versus different-source encounter; real departure/re-entry versus numerical contact jitter; interval, travel cost and stock on arrival. |
| Energy use | Productive-contact duration, stock debit, bodily credit, continuing expenditure and source recovery. |
| Restoration opportunity | Arrival at a surface, repair-eligible low-stress contact, actual positive restoration when a deficit exists. |
| Integrity recovery | Damage state and residual capability, achievable repair, energy spent during repair, and feasible return to energy. |
| Spatial support | Birth support, nearest-opportunity route information, per-fixture encounters and inaccessible or dominant regions. Equal encounter shares are not required. |
| Mover | Exposure, visibility, collision/stress, waiting/crossing/bypass opportunities, and reserve-feasible alternatives. |
| Chemistry | Actual receptor activity, spatial/temporal variation, persistence after emission changes, and interaction with solid geometry. |
| Whole-life accounting | Separate energy and integrity trajectories, source stocks, useful repeated interactions, and reason observation ended. |

### 8.2 Interpretation protections

**[ACCEPTED AMENDMENT]** Finite survival traces are finite-horizon evidence. They do not prove that spontaneous motion never survives indefinitely or that a controller survives forever. Use analytical bounds where justified and otherwise declare observation horizons, support and uncertainty. The accepted ecological intention remains local insufficiency with accessible global sufficiency and room for organisation to matter.

Terminal failure before contact is an outcome, not a successful-finder omission. Administrative cutoff is distinct from death and is censored observation where appropriate. Unsupported quantiles, empty estimator domains and non-finite readings do not become valid numbers by default.

Event and estimator definitions must be completed before they serve as gates. Specify denominator/support, quantile convention, contact/departure/revisit definitions, observation limits and handling of missing events. A contact oscillating at the numerical boundary is not automatically a sequence of revisits.

Do not enforce a desired distribution of routes, material categories or source revisits merely to make the world appear developmental. Legitimate wall-following, stable signatures and rhythmic adaptation remain allowed; their scientific interpretation is a later question.

**Reason.** Experienced encounter and recovery relationships, not fixture counts alone, determine whether the coupling poses the question.

**Main risk.** Survivor-only statistics, vacuous checks and success-shaped gates can certify an invalid apparatus or quietly turn commissioning into learner optimisation.

**Commissioning requirement.** Preserve complete trajectories and rejected configurations with reasons. Each eventual gate needs supported input domains and a reachable, observed failing case. Carry forward explicit non-finite and estimator conventions from the verified method sources; do not transport historical constants. Full associative-timescale adequacy cannot be certified before the relevant organism operation exists.

**Reversibility / later dial.** Numerical acceptance envelopes and horizons remain open. New measurements after a freeze are descriptive unless their changed evidential role is separately defined.

**Jason review.** Measurement distinctions and validity protections accepted. Operational gates, controller definitions, thresholds and adjustment routes still require their appropriate later review.

**Sources:** [S2] §§9, 19–20; [S3] §§13, 15; [S5] estimator-support, observed-red, non-finite and quantile provisions; [P0] BWC-7; [R1] amendments 1–3 and 6; [J1–J2].

---

## 9. BWC-8 — Initial material inventory

**Accepted ruling.** Use the reviewed small reusable starting palette. These role names and IDs are simulator-side bookkeeping, never organism inputs.

| Role | Starting assignment | Sensory / interaction disposition |
|---|---|---|
| `M0` — background medium | Floor/spatial background and chemical medium | Baseline optical and contact/transport properties; no source emission in the starting palette. |
| `M1` — neutral structural | Walls and moving block | Shared material parameters; obstruction, contact and stress. No source emission. Motion and interaction, not a semantic hazard class, make the mover consequential. |
| `M2` — energy-bearing | All energy sources | Shared optical/chemical character, finite stock and contact energy exchange. Stock can change emission magnitude without changing material character. |
| `M3` — restorative | All restorative surfaces | Shared optical character and an overlapping, distinguishable chemical mixture candidate; low-stress integrity restoration, no energy provision. |
| `M4` — organism body | Organism | Physical body properties and mounting of the already accepted sensing and actuation. Exact material parameters remain open. |

Retain the original starting assignment of a stable non-one-hot chemical mixture for energy material and a weaker, overlapping mixture for restorative material, subject to numerical commissioning. Two-component chemistry and broad overlapping receptor sensitivities remain the foundation. Exact spectra, mixture values, intensities, absorption and permeability are not specified here.

**Chemically non-emitting does not mean chemically transparent.** The later solid-transport ruling applies to the world interaction law, including the non-emitting mover. No absorption mechanism is selected merely by naming a material role.

**[ACCEPTED AMENDMENT]** Do not require every simulator material to be independently distinguishable in all or even some nominated test solely because it has a name. Relevant differences must reach the senses where needed to pose the coupling; materials may lawfully share signatures. Do not install matching modality codes, but do not destroy lawful easy associations to avoid them either.

**Reason.** Reuse separates material, body instance and changing state. The wall/mover shared material makes relative motion causally important without a hazard label.

**Main risk.** Role and material are closely aligned in the starting palette, limiting claims about later generalisation. Conversely, compulsory distinguishability would add an imposed classification task.

**Commissioning requirement.** Verify shared-law consequences, relevant receptor support, absence of IDs and analytic source directions in organism inputs, stock-dependent magnitude, and solid–field interaction. Check homogeneity of individual environmental bodies without silently changing accepted sensor morphology.

**Reversibility / later dial.** Richer material variation, chemically silent restorative surfaces, cross-role materials and composite bodies remain later variations; the base palette is not a claim of necessity.

**Jason review.** Retained palette and role assignments accepted as the starting point. Exact parameters and transport realization remain open.

**Sources:** [S2] §§4, 10–11; [S3] §§6, 11–12, 14; [P0] BWC-8; [R1] amendment 5 and BWC-8 disposition; [C1], [J2].

---

## 10. BWC-9 — Body/source/mover initial-state sampling

**Accepted ruling.** Separate fixed manifest properties from permitted per-life variation, while preserving physical dependencies among state variables.

For a selected world manifest, fix arena/fixture geometry, source/restorative positions, material assignments, mover track and motion law, illumination law, and the eventual numerical world/body configuration. Start each source at full stock and restorative surfaces in their non-depleted baseline state. Start the body with the accepted fixed reserve/full-integrity condition.

Use an explicit safe birth-position distribution, uniform body orientation on `[0, 2π)`, and uniform **time-phase** over the mover's complete round trip. Safe birth support retains the reviewed intent of no initial collision/transfer, no topological trap and a commissioned first foothold. The exact distance conditioning, clearances, spatial stratification and seed schedule are open and must be disclosed; they are not to be hidden as “just sampling.”

The initial-state record must also cover body translational/angular velocity, mover velocity consistent with phase, intrinsic motor-generator state, and any sensory/contact history state that later changes dynamics. This records an obligation to define those states, not a selection of their values.

**[ACCEPTED AMENDMENT]** Independent random streams prevent accidental information coupling; they do not require physical state independence. Because solids affect chemical transport, the field and mover history must be compatible. There is no mandatory stationary motor-generator distribution before such a generator and distribution have been established.

**Reason.** Varying pose and mover phase avoids one start determining all lives. Full stocks provide a simple initial source condition; subsequent depletion belongs to that organism's history.

**Main risk.** A source-conditioned birth sampler may become undisclosed scaffolding, while blindly uniform sampling may include inaccessible starts. Independently sampled field and mover states can create impossible prehistory.

**Commissioning requirement.** Report birth support, rejected starts and their rules, distances/routes to opportunities, heading relative to fixtures, initial receptor activity, all dynamically relevant initial state and required dependencies. Do not point the body toward a source or couple its pose to resource/mover knowledge through a hidden policy.

**Reversibility / later dial.** Birth distributions, initially depleted sources, variable reserve, fixed starts and inherited environmental history remain explicit later variations.

**Jason review.** Initial-state structure accepted. Exact support and initialization method remain open; lawful dependency is required, not an unresolved alternative.

**Sources:** [S2] §§11–13; [S3] §§4–7, 10, 13–15; [P0] BWC-9; [R1] amendment 5; [C1], [J2].

---

## 11. BWC-10 — Chemical transport and pre-evolution

**Accepted ruling.** **Solid bodies affect chemical transport.** Environmental geometry must contribute to the persistent chemical patterns available to the organism's senses. This includes accounting for the moving block's influence; chemically silent is not equivalent to non-interacting.

Jason's stated reason is to provide environmentally responsive gradients relevant to navigation. That is a design rationale, not evidence that navigation or development has improved.

The accepted ruling does not choose complete impermeability, partial permeability, absorption, moving-boundary handling, field discretisation or a particular numerical method. No new wind, turbulence or general advection model is silently introduced. The foundation's minimal diffusion/decay approach remains in force while the detailed solid-interaction law is specified.

Begin from a **lawful pre-evolved chemical state**, not an all-zero organism-age-coded startup. Source state, field state, solid configuration and mover phase/history must be jointly consistent under the eventual runtime laws. During life, fields evolve persistently with delayed spatial consequences rather than being recomputed as instantaneous source-distance queries.

**[ACCEPTED AMENDMENT]** Sol's reusable static full-source equilibrium snapshot, paired independently with any mover phase, is not an accepted default. With solid–transport coupling, such independence requires an actual justification. Pre-evolution must account for the selected interaction law and the phase/history relationship. It may not simply assume a static equilibrium exists for a moving transport domain.

The original no-flux outer boundary is retained as a **provisional example** pending the precise transport specification. This packet does not silently decide that all interior solids use that same condition. Birth introduction of the organism and any effect it has on field state also need lawful handling; no insertion algorithm is selected here.

**Reason.** The chemical sense should encounter a world shaped by its surroundings, not merely distance from resource centres. Coherent prehistory prevents arbitrary initialization transients from impersonating environmental structure.

**Main risk.** Transport may become effectively instantaneous, flat, saturated or too slow; numerical treatment of moving solids may produce spurious patterns. Assuming convergence from tiny per-step changes can certify a field only because the timestep is small.

**Commissioning requirement.** Check pre-evolution under the actual world law with a meaningful residual/history criterion; record the initialized state and method. Verify useful spatial/temporal receptor variation, source-state response, lingering history and solid-dependent field consequences. Evaluate compatibility of field timescales with the eventual organism without claiming that compatibility has already been established.

**Reversibility / later dial.** Boundary conditions, transport coefficients, prehistory duration and exact solid interaction remain open numerical/physical dials. A chemically transparent-solid comparison would be a separately identified later variation, not the starting world.

**Jason review.** Solid-body influence explicitly accepted in [J2]. The exact law and initialization realization remain to be specified and reviewed where substantive.

**Sources:** [S2] §§4, 8, 12; [S3] §§6.3–6.4, 11.1, 13, 15; [P0] BWC-10; [R1] amendment 5; [J2].

---

## 12. BWC-11 — Lifetime reset and termination semantics

**Accepted ruling.** Preserve one continuing world and one continuing organism inside each life. Internal persistent/plastic state, source depletion and renewal, chemical fields, mover phase and bodily consequences continue. Contact, collision, reaching a wall or visiting a resource does not trigger an episode reset. There is no teleport, source respawn, mid-life restoration of the birth world, or researcher rescue.

Between independent baseline lives, initialize a new organism under the same selected birth law with no transfer of the prior life's learned state. Restore full source stocks and a **jointly lawful** pre-evolved world state, including the correct field/mover relationship. Resample permitted variables according to the declared law. Do not interpret “reset” as blindly restoring one field while choosing an incompatible mover state. Full trajectories remain outside the organism for research.

**[ACCEPTED AMENDMENT]** Distinguish bodily nonviability, administrative observation cutoff, simulator failure and paused execution. A healthy organism reaching a time limit has not died; a software failure is not an ecological result. Faithful continuation from a pause requires preservation and verification of all relevant state; resume fidelity is not asserted by this document. Exact nonviability rules and observation horizons remain open.

**Reason.** Persistence within a life is the developmental object. Independent initialization between lives is replication, not a recurring event the organism experiences.

**Main risk.** Hidden subepisode resets can destroy accumulated experience, while inherited learning or environmental depletion can undermine the intended independence. Mislabelled cutoffs can turn censored survival into apparent death.

**Commissioning requirement.** Verify uninterrupted within-life persistence, absence of hidden resets, complete initial/reset state, random-state discipline and explicit termination reasons. Retain failures and final states without editing the trace to improve its interpretation.

**Reversibility / later dial.** Persistent worlds across organisms, lineage inheritance, learned birth structure and variable environmental prehistory remain separately identified later programmes.

**Jason review.** Baseline lifetime/reset semantics accepted. Operational termination, cutoff and verified continuation rules remain open dependencies.

**Sources:** [S2] §§12, 19–20; [S3] §§1, 8, 13–15; [P0] BWC-11; [R1] amendment 7; [C1], [J2].

---

## 13. BWC-12 — Commissioning-to-evidential freeze boundary

### 13.1 Functional acceptance — completed

The world relationships, starting branch choices and the accepted review corrections have been accepted in this conversation. This is functional completion, not experimental validation. The current request authorises preparation of their documentation. It does not authorise implementation, a preregistration, an experiment number or a run.

### 13.2 Configuration and commissioning — not completed

Detailed body/world laws and numerical settings must be specified, and later authorised commissioning must establish whether the complete coupling poses the intended question. Recorded apparatus-invalidity grounds can justify a revision. A reason such as “encounters are too rare” is not itself a mechanical instruction to change density, reserve, speed or sensor range.

**[ACCEPTED AMENDMENT]** Automatic numerical adjustment requires an already accepted range **and adjustment route**. Otherwise judgment returns to Jason in a batched decision. No such numerical adjustment corridor is defined by this document.

Coupling-commissioning lifetimes remain allowed in principle by the design frame. Inspecting needed validity information from the eventual organism is not categorically forbidden. What is forbidden is selecting the world to obtain hoped-for developmental success, changing validity definitions opportunistically, or silently promoting exploratory commissioning lives into evidential data. Final associative-reach checks depend on the eventual organism and cannot be discharged by this world packet alone.

### 13.3 Complete-coupling freeze — later Jason ruling

The eventual freeze must cover **all laws that can change the experienced coupling**, not just a source-layout file. It freezes the rules under which development occurs, not the learned state that is supposed to change.

| Freeze surface | Required coverage, once specified |
|---|---|
| Geometry and materials | Arena, body geometry, fixture counts/placements, restorative exposure, material assignments and parameters. |
| Mechanics and action | Mass/contact/friction, actuators and effort, mover motion, spontaneous dynamics and their initialization. |
| Sensing | Receptor placement, ranges, transfer functions, noise, history/filter state, proprioception and interoception. |
| Viability | Birth conditions, expenditure, transfer/renewal/emission, damage, restoration, low-viability capability effects and nonviability rules. |
| Chemistry | Transport and solid interaction, boundaries, update law, pre-evolution, field initialization and phase/history consistency. |
| Organism mechanisms | Later-selected cortical, associative, plasticity and motor/drive laws, their parameters and birth-state rules. No selections are made here. |
| Time and lifecycle | Mechanical/field/sensory/organism cadences, observation horizons, initial-state distribution, seed schedules, resets, failure and pause/resume handling. |
| Measurement | Controller/probe definitions, supported estimators, denominators, non-finite/censoring handling, gate definitions and appropriate non-interference checks. |
| Provenance and validation | All law-bearing modules and executable checks, actual configuration/state artifacts, code/environment identifiers, commissioning records, rejected candidates and reasons, observed-red checks and leak audits. |

Exact future artifact schemas and executors are not authored here. An immutable configuration identifier is necessary provenance but is insufficient if it omits law-bearing dependencies.

### 13.4 After freeze

Once an evidential configuration opens, inconvenient outcomes stand. Changing geometry, transport, sensing, viability, initialization, organism laws or other trajectory-affecting settings defines a separately identified configuration/branch. The original data is preserved, not retrospectively repaired. Deliberate comparison of wall versus freestanding restoration remains legitimate research, not prohibited change.

**Reason.** Early calibration must not lock in an invalid instrument; late adjustment must not allow the result to select its own test.

**Main risk.** “Commissioning” becomes indefinite tuning permission, or a partial manifest hides unrecorded changes to the actual organism–world relationship.

**Commissioning requirement.** Before evidential opening, provide the complete configuration, validity evidence, supported/falsifiable checks, information-leak protection, retained candidate history and explicit Jason freeze ruling. No PASS is claimed here.

**Reversibility / later dial.** The programme stays revisable. Pre-freeze judgment is recorded; post-freeze changes preserve the original evidence and receive their own identity.

**Jason review.** Boundary law accepted. Final configuration freeze, implementation authority and run authority remain separate later decisions.

**Sources:** [S2] §§19–20, 25; [S3] §§13–18; [S4] M7 and §G; [S5] gate/adjustment discipline and freeze-completeness rider; [P0] BWC-12; [R1] amendments 6–7; [J1–J3].

---

## 14. Remaining dependencies and mechanism handoff

### 14.1 Functional choices settled; realizations still open

| Dependency | What remains open | Why this does not reopen the completed functional review |
|---|---|---|
| Geometry and inventory | Body shape/size; arena scale; density coefficients and integer rules; source/strip dimensions; placement/birth support. | Square, area-related availability and wall-only starting restoration are accepted. |
| Solid–chemical law | Permeability/exclusion/absorption, boundary treatment, moving geometry, organism introduction and pre-evolution method. | Solids affecting transport and lawful joint history are accepted; no exact mechanism was selected. |
| Viability mechanics | Cost/transfer/damage/repair functions and values; capability changes; nonviability thresholds. | Separate currencies, working renewal model and usable recovery relationship are accepted. |
| Sensory/action coupling | Receptor detail, noise, actuator realization, spontaneous process, timing. | Their accepted functional existence does not specify their mechanism or scale. |
| Commissioning | Controllers, supported estimators, horizons, criteria, adjustment routes and numerical freeze. | No commissioned configuration or gate PASS is claimed. |
| Repository record | Accepted decisions are recorded here; commit identity is available from Git history. | Conversation acceptance is real; a commit is not claimed merely by preparing files. |

These are real dependencies to resolve before implementation or evidential operation, but they are not a requirement to finish every numeric choice before discussing mechanisms.

### 14.2 Next permitted design work

Jason's instruction after documentation is to enter the deferred mechanism discussion. Retain the foundation's high-attention questions individually: primitive cortical operation; central associative operation; permitted association-to-cortex plasticity after EXP21; motor organisation; interaction of distinct interoceptive drives, perception, spontaneous dynamics and called-forth motor material; and the developmental phenomenon criterion.

This document does not choose their answers, prescribe an unaccepted detailed order, select a conventional optimiser/policy, or import the failed unrestricted teaching pathway. Historical mechanism records may inform those discussions within their actual scope. The world/body constraints and open timing dependencies travel with the discussion.

**Sources:** [S2] §25; [S3] §18; [S4] §F; [J3].

---

## 15. Disposition of the original packet's numbers and overstatements

This is a **non-operative provenance record**, not a configuration file. All entries below originate in [P0] unless stated otherwise. They are preserved so later sessions do not recover an old conversational number and assume it was ratified. No new numerical starting recommendation is made in this section.

| Original proposal | Disposition after accepted review |
|---|---|
| `L = 50 D_b`; circular-envelope example `A_U = 2401 D_b²` | Unvalidated example. Neither arena scale nor final body geometry is frozen. |
| `N_E = max(6, floor(A_U/(300 D_b²) + 0.5))`; eight-source example | Provisional count-law example, including its half-up rounding and six-source floor. Area-based inventory is accepted; these literals are not. |
| `N_R = max(3, floor(A_U/(800 D_b²) + 0.5))`; three strips of `6 D_b` | Provisional example, not a compulsory minimum. Wall-only packing/perimeter must be checked jointly. |
| Source gaps `6 D_b`, wall clearance `3 D_b`, source-to-restoration `8 D_b`, source-to-mover `4 D_b` | Provisional spacing candidates, not validity gates. |
| Strip corner gap `4 D_b`, boundary-centre spacing `12 D_b`, placement on at least two walls | Original placement preferences, not frozen restrictions. Exact placement returns with the configuration. |
| Mover bypass `3 D_b`; detour ratio approximately `1.75` | Provisional candidates. Reserve-feasible safe alternatives remain required; these values do not. |
| `C_S = 0.25–0.40 E_max`; `C_S/τ_S = 0.20–0.35 P_ref`; aggregate maximum renewal at least `1.75 P_ref`; `U_max ≥ 5 C_S/τ_S` | Unvalidated numerical relationships. Shared transfer accounting, finite stock, slow renewal and local insufficiency/global sufficiency remain the functional requirements. |
| `E_0 = 0.75 E_max`; `P_b/P_ref = 0.35–0.50` | Provisional values. Fixed non-maximal birth energy is accepted; its fraction is not. |
| `P_E = P_b + P_m (\|u_L\| + \|u_R\|)/2` | Provisional cost realization; exact effort definition, state dependence and coefficients are open. |
| `m(S) = m_min + (m_max−m_min) S/C_S`, with positive depleted emission | Provisional source-emission realization; stable character with state-dependent magnitude is the retained starting relationship. |
| `Q_0.9(T_first productive energy contact) < T_birth reserve` | **Not accepted as a gate.** Replaced by supported unconditional bootstrap/remaining-runway assessment; no substitute percentile chosen. |
| Static full-source equilibrium field independently paired with random mover phase | **Not an accepted default.** Replaced by lawful solid-aware joint prehistory; exact method open. |
| Mandatory stationary birth distribution for the motor generator | **Not accepted unconditionally.** Lawful initialization is required; generator and appropriate distribution remain open. |
| All materials must be individually distinguishable; blanket bans on grids/symmetry/corners | **Not active requirements.** Relevant sensory accessibility and lawful learnability govern. |
| Swept mover region subtracted as permanently non-navigable | **Corrected.** Distinguish static accessibility, time-dependent crossing and always-clear bypass. |
| Finite trajectories establish “indefinite” success/failure | **Corrected.** Analytical conditions and finite-horizon observations must be separated. |
| All external commissioning controllers are trajectory-inert | **Corrected.** Controllers act in their own trials; observational probes on evidential lives must not interfere. |
| Any numerical adjustment permitted for a named commissioning reason | **Corrected.** Mechanical adjustment needs a prior accepted range and route; otherwise Jason judges. |
| World-only freeze before any developmental-organism outcome can be inspected | **Corrected.** Complete-coupling freeze; needed validity observations in separate commissioning lives are allowed in principle, without outcome rescue or data promotion. |

`D_b`, separate energy/integrity normalizations and notation are measurement conventions, not sensor inputs. This table contains no measured ecological results.

---

## 16. Sources, acceptance provenance and change record

### 16.1 Verified foundation sources

Pinned repository reference for [S1–S5]: `EridosAI/Loom@103973f6646a4c12ac817cb085e0456f19f77cb9`. This is the requested foundation reference, **not a claim about current remote HEAD**.

The full local copies of [S1–S4] were read and their Git blob hashes computed during preparation. They match the blob hashes returned by the GitHub connector at the pinned reference.

| ID | Source path at the pinned commit | Verified Git blob SHA |
|---|---|---|
| S1 | `00_LOOM_CURRENT_STATE.md` | `73983cd938c6bc551c570b9dbd88d6ec0606804d` |
| S2 | `docs/developmental_ecology/DEVELOPMENTAL_ECOLOGY_DESIGN_FRAME_v0_2.md` | `a9d3d0cf5bb3dfcc0bd04e7c05fc654f18e613a4` |
| S3 | `docs/developmental_ecology/PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1.md` | `1e3441d97eb224a0dbbe9b1c50b47ac75513d59e` |
| S4 | `docs/developmental_ecology/DEVELOPMENTAL_ECOLOGY_DECISION_LEDGER_v0_1.md` | `4e1c88f2137b69e288b6332f11ce56772005cce3` |
| S5 | `EXP1-21/docs/CORRIDOR_PROTOCOL.md` | `4fad682b9de58cb1153514603519275f985247b9` |

[S5] is used for the specific method protections discussed and accepted in review: pre-named decisions versus judgment, estimator support, reachable observed-red tests, explicit non-finite/quantile treatment and complete law-bearing freeze coverage. Its EXP21-derived riders were checked against the pinned repository file. The older uploaded `CORRIDOR_PROTOCOL.md` snapshot does not contain all those riders and is not substituted for the pinned source. This document does not instantiate an experimental corridor or import its entire historical workflow by implication.

Foundation reading links for a repository landing: [design frame](DEVELOPMENTAL_ECOLOGY_DESIGN_FRAME_v0_2.md), [coupling specification](PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1.md), [original ledger](DEVELOPMENTAL_ECOLOGY_DECISION_LEDGER_v0_1.md), [updated ledger](DEVELOPMENTAL_ECOLOGY_DECISION_LEDGER_v0_2.md), [current state](../../00_LOOM_CURRENT_STATE.md).

### 16.2 Conversation source landmarks

These are document-local provenance labels, not native message IDs or experimental IDs. Exact turn timestamps and a native chat identifier were not exported with this package. The consolidation date above must not be used to invent finer-grained decision timestamps.

| ID | Conversation material | Authority |
|---|---|---|
| P0 | Sol's assistant answer titled “Base World Completion — Review Packet v0.1,” containing BWC-1–BWC-12 | Original proposal only; controlled by the accepted amendments and later acceptance scope. |
| R1 | Astra's review beginning “Sol's packet is a good first design draft, but I would not recommend accepting all twelve rulings as written,” with seven amendment groups and twelve-item disposition | Assistant review whose amendments were subsequently accepted in J1. |
| J1 | Jason's acceptance of those amendments, reproduced below | Explicit user decision. |
| C1 | Follow-up consolidation explaining the two outstanding world-law choices and the retained candidate baseline | Scope of the consolidated baseline that J2 accepts; numerical settings explicitly remained provisional. |
| J2 | Jason's wall-only choice, solid-transport choice, consolidated-baseline acceptance and revisability caveat, reproduced below | Explicit user decisions and condition of acceptance. |
| J3 | Jason's request to prepare documentation and then enter mechanisms, reproduced below | Documentation instruction and next design direction; not authority to build or run. |

### 16.3 Exact acceptance excerpts

**J1 — amendment acceptance**

> Ok, I like your amendments and I'm happy to retain them. What does that leave outstanding for me to address?

**J2 — placement, solid transport and baseline acceptance**

> Ok, for the restorative surface placement - I think wall only is a valid starting point. However freestanding is also interesting. Both versions will give rise to different behaviour and that is what we want to see. So start with walls but note that we will play with placement.
>
> Solid bodies affecting chemical transport. I think they should. Learning to navigate in the environment is a key aspect of why we're doing this. The chemical variability due to interaction with solids is a good way to offer environmentally responsive gradients to the senses.
>
> For the consolidated baseline. I accept what you've written. The only caveat being that a lot of these can and likely will be changed once we see how the coupling works. What you've got there is a valid starting point.

**J3 — documentation instruction**

> Ok, can you prepare the documentation for the base world completion?
> Then we can get into teh mechanisms.

These excerpts record acceptance, not experimental evidence. The document's prose is a consolidation of that acceptance and the identified source material, not a verbatim transcript of the full discussion.

### 16.4 Consolidation record

2026-09-05 — Astra prepared this first durable Base World Completion file, the v0.2 decision-ledger continuation, an updated current-state copy and a dated coupling-specification reading note. The original Fork 1–28 record is preserved. No new scientific result, neural mechanism, experiment number, preregistration, Developmental Ecology source code or run is created or authorised. Repository landing remains unperformed by this preparation task.
