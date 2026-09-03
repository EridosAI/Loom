# Primitive Organism–World Coupling Specification — v0.1 Consolidated Draft

**Project:** Loom / PAM — Developmental Ecology line  
**Consolidation date:** 2026-09-03  
**Status:** **CONSOLIDATED DRAFT FOR JASON VERIFICATION**  
**Scope:** Integrates the Jason-accepted working branches through Fork 28, plus accepted amendments and the density-based inventory note.  
**Repository status:** **Not committed canon. No implementation authorised.**  
**Parent doctrine:** `DEVELOPMENTAL_ECOLOGY_DESIGN_FRAME_v0_2_CONSOLIDATED_DRAFT.md`

---

## 0. What this document is—and is not

This is a **functional organism–world coupling specification**.

It says what must exist for the first developmental setting to pose the intended question. It does not yet select:

- neural architectures;
- sensory-cortex learning rules;
- the central associative mechanism;
- PAM→cortex plasticity;
- action arbitration;
- numerical parameters;
- verdict laws;
- software stack;
- an experiment number.

All accepted branches remain reversible through separately named reductions, expansions, or alternate branches. Nothing here silently rewrites current Loom repository canon.

---

# 1. System overview

The first setting contains:

1. a bounded continuous two-dimensional world;
2. persistent material bodies and persistent environmental fields;
3. one persistent oriented compact organism;
4. crude body-mounted light, chemical, contact, proprioceptive, and interoceptive windows;
5. low-level paired actuation;
6. endogenous structured spontaneous activity;
7. two bodily viability dimensions—energy and integrity;
8. multiple finite renewable energy sources;
9. multiple anchored restorative surfaces;
10. one persistent autonomous block moving repeatedly on a fixed path;
11. fixed world laws and hidden external state available only to the researcher.

The world, body, senses, viability, and action form one continuous loop:

```text
world state
   ↓
light / chemical / contact consequences
   ↓
organism internal activity and association
   ↓
body-relative actuation
   ↓
body and world interaction
   ↓
changed world, proprioception, energy, integrity
   ↺
```

The same organism persists throughout the lifetime and is changed by what it experiences.

---

# 2. World substrate

## 2.1 Continuous generative causal simulation

The first habitat is a continuous generative causal simulation.

The simulator defines laws and persistent causes, not samples or lesson sequences. All sensory channels derive from one evolving world state.

Physical reality remains the standing escalation if uncertainty about the designed world becomes dominant.

## 2.2 Hybrid causal world

The world combines:

- a continuous spatial medium supporting light-like and chemical-like consequences;
- a small number of persistent localised material bodies;
- local collision, contact, exchange, depletion, repair, and motion laws.

Persistent bodies provide recurrence, obstruction, manipulability potential, and contact.

Fields provide propagation, partial availability, lingering consequence, superposition, and environmental history.

## 2.3 Practicality rider

The simulation should implement the **minimum causal structure required by the developmental hypothesis**.

Initial implementation should prefer:

- simple two-dimensional local mechanics;
- coarse geometric light sensing rather than photorealistic rendering;
- two low-resolution scalar chemical fields;
- linear diffusion and decay;
- simple source emission;
- simple rigid-body contact and stress laws;
- a small body/material inventory.

No initial need exists for:

- turbulent flow;
- particle chemistry;
- Navier–Stokes;
- realistic optics;
- meshes or deformable bodies;
- a general-purpose high-fidelity physics engine.

**Physical realism is optional. Causal fidelity at the organism’s scale is mandatory.**

---

# 3. Spatial domain

## 3.1 Bounded continuous 2D arena

The first world occupies a bounded, continuous, non-wrapping two-dimensional domain.

Two dimensions are selected because they permit:

- approach and retreat;
- turning and body-relative direction;
- alternative routes and detours;
- occlusion;
- distributed contact;
- separated sources;
- field propagation;
- an avoidable moving hazard;
- revisiting persistent places.

A third dimension remains a later expansion. One-dimensional and toroidal worlds remain later reductions or specialised controls.

## 3.2 Boundaries

Arena boundaries are persistent, perceptible physical structures.

They must not be:

- invisible coordinate clamps;
- wraparound seams;
- reset triggers;
- semantic penalties.

Walls obstruct through ordinary contact mechanics and have stable visual/material consequences. Wall following, corner use, and boundary landmarks are legitimate adaptations.

## 3.3 Exact geometry is not yet fixed

Open numerical design variables include:

- arena shape and area;
- body-to-arena scale;
- source and restorative-surface density;
- placement distributions;
- moving-block track placement;
- detour length;
- sensor ranges;
- chemical boundary conditions.

These are commissioning parameters until frozen before evidential lifetimes.

---

# 4. The organism’s body

## 4.1 Compact oriented physical body

The organism is one persistent, physically extended, oriented compact body—not a point agent and not an articulated creature.

It has:

- a body boundary;
- a functional front/rear and left/right through morphology;
- finite extent and collision geometry;
- body-mounted receptors;
- low-level paired actuation;
- bodily viability state.

The body’s axis exists physically. The organism receives no symbolic `FRONT`, `LEFT`, heading, or global compass.

## 4.2 Geometry

The exact organism shape remains open within a simple convex family, likely disk/capsule/rounded-body class.

The first body has no limbs, gripper, articulated joints, or semantic action set.

## 4.3 Body as a recurring causal nexus

Giving the organism a body is not giving it a self-concept.

A self/world distinction may eventually become learnable because one physical locus repeatedly links:

- outgoing motor activity;
- actual movement;
- contact;
- sensory change;
- energy and integrity consequences.

No explicit self token is supplied.

---

# 5. Action and initial activity

## 5.1 Low-level paired actuation

The body acts through two body-relative continuous actuators—functionally equivalent to paired drive or local thrust.

This permits:

- forward motion;
- turning;
- curved trajectories;
- stalled movement under obstruction;
- different outcomes from the same motor activity under different contact conditions.

The organism does not issue:

- destination coordinates;
- global-axis velocity commands;
- `EAT`, `REPAIR`, `PUSH`, `AVOID`, or other semantic actions;
- object-targeted commands.

## 5.2 Endogenous structured spontaneous activity

The first organism begins with self-sustaining, bounded, temporally correlated motor activity.

This supplies continued movement before the organism understands movement.

It must not be mere independent white-noise control, and it must not contain a goal-specific policy such as following a resource gradient.

The exact generator remains open. Candidate implementations may later include coupled oscillatory dynamics, correlated stochastic processes, or a tiny endogenous motor circuit.

## 5.3 Claim boundary

Spontaneous action is innate.

Potentially emergent phenomena include:

- selective/decisive action;
- state-sensitive action;
- curiosity-like information-seeking;
- longer-horizon action;
- inspired or recombinative action.

The base system does not pre-install a curiosity reward, novelty objective, or belief that continued attempts will improve outcomes.

---

# 6. Sensory windows

The organism has separate raw windows into one world. No common external coordinate system or object identity is supplied across channels.

## 6.1 Light-like distal sense

The light sense is:

- body-relative;
- directionally limited;
- coarse and forward-facing;
- spatially distributed across a small angular fan;
- genuinely rear-blind;
- minimally spectral.

Each angular sector produces **two raw broad-band photoreceptor activities**.

The organism receives no engineered hue, saturation, brightness-normalised colour, bearing, depth map, segmentation, or object mask.

Persistent material properties generate stable two-band character. Received activity changes lawfully with:

- geometry;
- distance;
- surface orientation;
- occlusion;
- directional illumination;
- organism motion;
- autonomous-body motion.

## 6.2 Illumination

The first world uses:

- one fixed distant directional light source;
- stable two-band spectral composition;
- a weak spectrally matched ambient floor.

The directional component provides a lawful global asymmetry and shading. The ambient floor prevents important causes from becoming completely invisible in shadow.

No initial:

- flicker;
- day/night cycle;
- moving light;
- changing spectral composition;
- multiple coloured lights;
- realistic global illumination.

The organism receives no light-source direction or compass.

## 6.3 Chemical-like distal sense

The chemical world contains two persistent diffusing field components.

Persistent emitting causes produce stable low-dimensional mixtures of those components. Source state may lawfully alter emission magnitude while preserving chemical character.

The body has a small number of separated anterior or anterior-lateral sampling locations. At each location, broad overlapping receptor sensitivities produce raw local activities.

The organism receives no:

- source identity;
- chemical label;
- mixture ratio;
- analytic gradient;
- source bearing;
- source stock;
- viability meaning.

Some bodies may be chemically silent.

## 6.4 Chemical dynamics

Chemical state is real persistent world state, not a distance-to-source query.

The initial model uses:

- emission;
- linear diffusion;
- linear decay;
- superposition;
- source-state-dependent magnitude where appropriate;
- simple boundary behaviour.

No initial wind, turbulence, or advection.

The field should begin from a lawful pre-evolved state rather than an organism-age-coded all-zero startup.

Chemistry evolves and lingers over longer timescales than light.

## 6.5 Contact sensing

Contact sensing is spatially distributed around a wider portion of the body boundary than the distal forward sensors.

It reports local bodily interaction—contact location, pressure/stress or another low-level physical consequence—not collision partner ID or semantic meaning.

## 6.6 Proprioception and movement sensing

The organism has access to:

- the motor activity it produced;
- the body-relative motion that actually resulted;
- rotation/translation consequences;
- actuator/contact discrepancy.

Command and outcome are not assumed identical.

No global `x,y`, absolute heading, world velocity, or simulator pose is supplied.

## 6.7 Interoception

Interoception continuously exposes dimension-specific bodily condition for:

- energy;
- structural integrity.

The exact encoding remains open, but each dimension must be:

- monotonic over the relevant range;
- separately perceivable;
- always available;
- free of a combined utility value.

---

# 7. Viability and primitive valence

## 7.1 Two separate dimensions

The first organism has two viability dimensions:

### Energy

Capacity for ongoing work, sensing, and actuation.

### Integrity

Continuing physical coherence and sensorimotor reliability of the body.

They are not aggregated into one health, fitness, reward, or action-selection scalar.

## 7.2 Preferred bodily regions

Higher energy and greater integrity are intrinsically preferable embodied conditions.

Depletion produces dimension-specific interoceptive drive and lawful capability consequences. Restoration reduces drive and improves available functioning.

This is primitive valence and need.

It does not specify strategy.

## 7.3 Candidate capability effects

Exact effects remain open and must preserve recoverability.

Working functional directions:

- low energy may reduce sustainable actuation or spontaneous-activity intensity;
- low integrity may reduce reliability, introduce actuator asymmetry, increase sensory distortion, or reduce tolerance of future stress.

Capability loss must be graded. It must not remove the very sensing and action needed for recovery before learning can occur.

## 7.4 No hidden scalar

No rule may collapse the two dimensions into:

\[
V = w_E E + w_I I
\]

for reward, policy, plasticity, or arbitration.

The dimensions remain separate in cause and restoration, while interacting indirectly through one shared body and one continuing life.

---

# 8. Energy ecology

## 8.1 Graded contact-mediated exchange

Energy is restored through physical contact with persistent resource-bearing bodies.

There is no semantic `EAT` action and no reward event.

Exchange is graded by lawful interaction such as:

- contact duration;
- contact quality;
- possibly area, relative motion, or another simple physical quantity.

An accidental brush may help slightly; sustained productive contact may transfer more; uptake saturates as bodily energy approaches its capacity.

## 8.2 Multiple persistent finite sources

The base world contains multiple spatially distributed resource bodies.

Each source:

- is persistent;
- has finite locally available stock;
- is depleted by successful exchange;
- replenishes slowly under fixed laws;
- remains present while depleted and recovering;
- has stable material and chemical character;
- may show state-dependent chemical magnitude and uptake strength.

Sources do not disappear and randomly respawn in the base branch.

## 8.3 Local insufficiency, global sufficiency

No one source sustains indefinite attachment.

The wider ecology can sustain the organism through sufficiently effective movement and interaction.

The intended operating relationship is qualitative until commissioned:

```text
single-source sustained yield
    < continuing bodily need
    < accessible ecological yield
```

Random movement should sometimes find and use sources, but should not maintain viability indefinitely with no developmental organisation.

## 8.4 Density-based inventory

The working direction is to specify source availability primarily by **density over accessible world area**, not by an absolute count detached from arena scale.

However, density alone does not establish adequacy. Commissioning must examine:

- encounter-time distribution;
- revisit-time distribution;
- body speed and turning;
- sensory range;
- depletion and renewal times;
- birth reserve;
- arena topology and obstacles.

Exact source count and density remain open until the base-world packet is reviewed.

---

# 9. Integrity ecology

## 9.1 Causally separate restoration pathway

Integrity is not repaired by spending energy in the base branch.

Energy sources do not restore integrity.

Integrity-restoring conditions do not supply energy.

Energy-dependent repair, universal intrinsic healing, and stronger cross-coupling remain later complexity levers.

## 9.2 Anchored extended restorative surfaces

Integrity is restored through graded, sustained, low-stress physical contact with one or more anchored homogeneous restorative surfaces.

The interaction differs functionally from energy exchange:

- energy: compact, finite, renewable sources; quicker exchange;
- integrity: extended, anchored surfaces; slower, sustained gentle coupling.

Brief gentle contact may provide a small effect. Stable low-relative-motion contact may restore more. Forceful impact does not count as repair and remains subject to damage law.

The surface may initially be non-depleting because energy continues to fall during prolonged residence.

## 9.3 Density-based working direction

Jason’s current direction is to include **more than one restorative opportunity**, with availability considered relative to world area rather than as an isolated fixed count.

The exact number, density, geometry, and whether all restorative surfaces share one material are not yet frozen.

## 9.4 Integrity damage

Integrity loss arises from one physical mechanical-stress law.

Stress may be:

- self-caused by poor movement or collision;
- world-caused by autonomous motion;
- interaction-dependent on both organism and world state.

The organism receives no `SELF_CAUSED` or `WORLD_CAUSED` label.

Damage is graded through relative motion, stress, duration, angle, or another simple local physical quantity—not semantic hazard identity.

---

# 10. Autonomous environmental dynamics

## 10.1 Mixed causal autonomy

The world contains:

- changes caused by organism action;
- lawful changes independent of the organism;
- outcomes that depend jointly on both.

Autonomous dynamics must be bounded, perceptible, recurrent, and legible at the newborn organism’s temporal and sensory scale.

They are not arbitrary noise or a staged curriculum.

## 10.2 Periodic moving block

The first autonomous integrity threat is one persistent non-agentive material block constrained to a fixed linear path.

It moves continuously back and forth between two endpoints under a simple lawful motion rule.

It does not:

- target the organism;
- react strategically to it;
- teleport;
- spawn randomly;
- deliver hidden arbitrary damage.

The organism receives no period, phase, age, or global clock.

Predictability is permitted. Learning the block’s rhythm is a legitimate adaptation, but later claims must distinguish current-sensory response from phase entrainment.

## 10.3 Avoidable but consequential placement

The block’s track intersects a recurrently useful route or region, while leaving physically accessible alternatives.

The block is not the sole gate to energy or integrity restoration.

Possible interactions include:

- crossing at a suitable time;
- waiting;
- retreating;
- detouring;
- surviving graded collision;
- using current perception or learned rhythm.

Exact speed, track, phase, mass, damage, and geometry are commissioning variables that must freeze before evidential lifetimes.

---

# 11. Materials and bodies

## 11.1 Reusable causal material palette

The world uses a small palette of reusable materials.

A material parameterises how physical stuff participates in:

- two-band light response;
- chemical emission/absorption;
- density and mass;
- friction and contact;
- stress/damage;
- energy exchange;
- integrity restoration.

Material identity and parameters remain hidden from the organism.

Several bodies may share a material. The same body persists through changing state.

## 11.2 Body, material, and state remain distinct

### Body

Persistent localised cause with geometry, position, motion, and individual history.

### Material

Reusable lawful interaction properties.

### State

Changeable quantities such as source stock, depletion, recovery, position, or velocity.

This permits the same source to remain visually/materially familiar while its chemical magnitude and current usefulness change.

## 11.3 Stable signatures

Stable distinctive multisensory signatures are allowed.

They must arise because the same material and world laws generate them—not because separate modality codes are manually assigned matching labels.

The base world is learnable before it is ambiguous.

## 11.4 Homogeneous bodies

Each initial body is made from one material.

No initial layered, composite, articulated, deformable, or part-specialised bodies.

Composite bodies remain a later complexity expansion.

## 11.5 Simple rigid convex geometry

The world uses a small reusable geometry vocabulary:

- compact round bodies;
- capsules or rounded rectangles;
- elongated simple movers;
- extended strips/surfaces for walls or restoration.

Exact primitives remain open, but bodies are initially:

- rigid;
- convex;
- stable through the lifetime;
- easy to simulate and inspect.

No shape label or object boundary is supplied to the organism.

---

# 12. Environmental manipulability

## 12.1 Baseline branch

The base world does not contain general pushable furniture.

- energy sources are anchored;
- restorative surfaces are anchored;
- arena boundaries are fixed;
- the autonomous block follows its prescribed track.

This keeps the first question focused on whether spontaneous action becomes organised through perception, viability, association, and consequence.

## 12.2 Early expansion

One or a few persistent pushable neutral bodies are an early post-baseline complexity branch.

They should be included only when displacement can alter real affordances through shared laws, such as:

- route geometry;
- occlusion;
- collision exposure;
- shielding;
- contact arrangement.

There is no semantic `PUSH` action and no object labelled as a tool or shield.

Displacement persists within the lifetime.

---

# 13. Temporal character

The qualitative timescale hierarchy is:

### Light

Fast response to current geometry, movement, and occlusion; little persistence after geometry changes.

### Contact and proprioception

Fast or event-like body–world consequences.

### Chemical field

Slower propagation, mixture, decay, and lingering environmental history.

### Interoception

Slower integration of ongoing expenditure, uptake, damage, and repair.

### Source state

Depletion and renewal slower than individual contact events.

No timestamps, ages, field phases, or global update indices are supplied to the organism.

Exact rates remain commissioning parameters. The modalities must still overlap within the usable temporal reach of the eventual associative mechanism.

---

# 14. Information prohibited from the organism

The simulator may know these. The organism may not receive them directly:

- global position;
- absolute orientation;
- body or object identity;
- object class;
- material ID;
- shape type;
- distance-to-source;
- nearest-resource direction;
- analytic chemical gradient;
- source stock;
- collision partner ID;
- hazard label;
- restorative label;
- global map;
- timestep or age;
- combined health/utility;
- reward;
- semantic action;
- cross-modal correspondence.

Different modalities must not share trivially matching channel indices that amount to a supplied common coordinate code.

---

# 15. Coupling commissioning

Before an evidential developmental cohort opens, the world–body coupling must be shown to pose the question.

## 15.1 Physical ceiling

Using privileged simulator state, verify that continued viability is physically possible with the actual body, actuators, resources, repair surfaces, and block.

## 15.2 Perceptual ceiling

Verify that a controller restricted to the organism’s actual raw sensory windows can outperform one deprived of the relevant sensory information.

This proves useful structure reaches the body. It does not become part of the organism.

## 15.3 Bootstrap floor

Verify that the innate spontaneous-action process sometimes reaches partial or complete viability-supporting interactions before terminal failure.

Random motion must not solve the ecology indefinitely, but it must sometimes reach the first learnable rung.

## 15.4 Core commissioning questions

A verdict-bearing cohort must not open if:

- sources or restorative surfaces are physically unreachable;
- sensory differences are numerically absent or inaccessible;
- chemical fields are effectively flat everywhere or detectable only at contact;
- chemistry is merely a second instantaneous distance sensor;
- the block is invisible until unavoidable impact;
- no safe alternative route exists;
- detours are physically impossible within bodily reserve;
- one source permits indefinite camping;
- total ecological renewal is below unavoidable expenditure;
- random movement sustains viability indefinitely;
- low energy/integrity removes recovery capability too early;
- repair requires competence spontaneous activity cannot approximate;
- modal timescales never overlap within associative reach;
- hidden state leaks into action or plasticity.

## 15.5 Commissioning versus rescue

Numerical adjustment is legitimate only while establishing physical, perceptual, and developmental reachability.

After the frozen evidential configuration opens, an inconvenient developmental result is recorded. Changing the world to obtain a hoped-for result defines a new branch.

---

# 16. What is fixed functionally versus still open numerically

## 16.1 Functionally accepted

- continuous causal simulation, physical reality behind it as escalation;
- hybrid world with persistent bodies and fields;
- bounded non-wrapping 2D arena;
- oriented compact body with paired actuation;
- light + chemical + contact + proprioception + interoception;
- directional heterogeneous sensor layouts;
- two-band light and two-component chemistry;
- fixed directional light with weak ambient floor;
- dynamic diffusive/decaying chemistry;
- two viability dimensions: energy and integrity;
- primitive valence without reward;
- finite renewable energy sources;
- external low-stress integrity restoration;
- mixed mechanical integrity threats;
- one periodic moving block on an avoidable consequential crossing;
- reusable materials, homogeneous bodies, simple convex geometries;
- no general pushables in the baseline;
- synthesis before reduction;
- coupling commissioning before scientific interpretation.

## 16.2 Still open

- arena area and shape;
- body size and mass;
- actuator range and motor generator;
- receptor counts, fan aperture, range, and noise;
- material parameter values;
- source/restorative density and placement law;
- source capacity, uptake, renewal, and emission coupling;
- energy and integrity depletion rates;
- capability effects of low viability;
- repair-contact law;
- damage law;
- block track, speed, mass, phase, and visibility;
- chemical grid, diffusion, decay, and update cadence;
- mechanical integration cadence;
- association wave and modality-rate relationships;
- neural and plasticity mechanisms;
- developmental duration and cohort design;
- observation and verdict laws.

---

# 17. Explicit complexity dials

These are preserved as later reductions or expansions, not silently rejected:

- one viability dimension ↔ two ↔ three or more;
- intensity-only light ↔ two bands ↔ richer spectra;
- one chemical component ↔ two ↔ richer mixtures;
- omnidirectional ↔ directional sensing;
- single temporal receptor ↔ spatially distributed receptors;
- ambient-only ↔ directional+ambient ↔ dynamic illumination;
- diffusion only ↔ advection/wind/turbulence;
- one shape ↔ simple palette ↔ composite/deformable bodies;
- fixed furniture ↔ pushable neutral bodies;
- one mover ↔ several/complex movers ↔ another agent;
- static source positions ↔ migrating causes;
- simulation ↔ physical embodied reality;
- weak association-to-cortex nudging ↔ stronger co-development;
- no explicit curiosity ↔ later information-seeking mechanisms;
- short-horizon self-preservation ↔ longer-horizon goals.

Each dial moves only in a separately specified branch.

---

# 18. Mechanism layer deliberately deferred

The following questions require individual high-attention forks after the base-world packet is complete:

1. What does each primitive cortex learn and by what local operation?
2. What is the central associative operation in this organism?
3. How is current PAM lineage evidence used without importing the failed unrestricted EXP21 pathway?
4. How does association influence cortical development—if at all—and at what strength/timescale?
5. How do interoceptive drive, current perception, spontaneous dynamics, and called-forth motor material combine?
6. What prevents early learned motor habits from extinguishing exploration?
7. What developmental observation distinguishes ecology-driven regime change from a simple reactive controller?

No answer is implied by the world specification.

---

# 19. Next review packet

The next batched design packet should close the **Base World Completion** layer:

- arena shape and area convention;
- energy-source and restorative-surface density;
- placement and initial-state law;
- source capacity and renewal relationships;
- encounter/revisit commissioning metrics;
- material inventory and initial role assignments;
- birth position/orientation and mover phase sampling;
- world pre-evolution and lifetime reset semantics.

Those should be proposed as a packet for Jason review rather than one conversational fork at a time.
