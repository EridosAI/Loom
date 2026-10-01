Jason review of B1_AUTOMATED_REFERENCE_DESIGN_v0_1:

The proposal is careful, but it is too large for the remaining
commissioning question.

Do NOT implement v0.1 as written.

We have explicitly decided to do the minimum credible perceptual closure
and then move on to testing P.

==================================================
FIRST: IDENTITY / PROVENANCE CLARIFICATION
==================================================

The design names current apparatus:

b684912eaf7811cd318ee94c77172aca790f3a0d

Our last independently reviewed operator-apparatus checkpoint was:

352f73fffa6d9781eae8aa38e708a9a05669588f

and the regenerated B1 packet was reported as built against 352f73ff.

Before doing any new design/build work, report:

- what b684912e... is;
- its exact parent;
- why it differs from 352f73ff...;
- every production-code change between them, if any;
- whether the human FULL-RAW execution required any apparatus/source
  commit after 352f73ff.

Do not silently reconcile these identities.

==================================================
RETIRE CURRENT v0.1 SCALE
==================================================

Do not proceed with:

- 32-state GRU;
- supervised FULL/HIDDEN/null model fitting;
- 16/4/12 train-development-test split;
- passive nearest-source vector benchmark;
- 56 trajectories;
- 1,680 simulated seconds;
- multi-hour fitting campaign;
- ~56+ GB evidence campaign.

Preserve B1_AUTOMATED_REFERENCE_DESIGN_v0_1 as a thorough proposal, but
mark it NOT SELECTED.

Reason:
this would create a substantial external-controller research programme
when the present requirement is only to rule out catastrophic perceptual
inaccessibility before testing the actual organism.

==================================================
PREPARE B1 MINIMAL CLOSURE v0.2 — DESIGN ONLY
==================================================

Target question:

Can a fixed external controller, receiving only the organism-permitted
raw sensory history, use sensory feedback to produce a real useful
energy-source interaction?

This is an EXISTENCE WITNESS, not a benchmark.

Prefer a simple deterministic controller over a trained model.

The controller MAY be designed with knowledge of:
- receptor geometry;
- channel ordering;
- actuator semantics;
- general sensor/world laws.

At RUNTIME it MUST NOT receive:
- global position or orientation;
- source position/identity/stock;
- map;
- analytic source gradient;
- material identity;
- evaluator events;
- future state;
- fixture/seed identity;
- privileged stop reason.

Use actual permitted sensors/history only.

==================================================
PREFERRED CONTROLLER
==================================================

Investigate whether the existing directional sensor geometry admits a
simple fixed feedback law.

For example only, not as an imposed mechanism:

- left/right sensory imbalance -> differential turning;
- overall relevant sensory magnitude -> forward tendency;
- contact/proprioception -> simple bounded contact/collision response.

If chemistry provides the cleanest directional signal, using it is
acceptable.

This controller is commissioning apparatus.
It is NOT P and will never be copied into P.

Do not optimize extensively.

Fix all constants before held-out execution.

If no credible simple controller can be specified without substantial
training/search, STOP and report that rather than escalating automatically
to learned-controller development.

==================================================
CASES
==================================================

Design the smallest bounded set that gives variation in initial geometry.

Provisional target:
3 predeclared held-out starts.

For each start:

1. FULL permitted sensory feedback;
2. CHEMISTRY-HIDDEN relevant deprived condition;
3. SENSORY-FREE/open-loop control.

Maximum:
9 held-out trajectories.

Retain the existing 30-second ceiling unless there is a concrete reason
that makes it invalid.

Starts should vary orientation/relative geometry enough that one fixed
open-loop sequence is not trivially useful across all of them.

No replacement starts after outcomes are seen.

No train/development cohort.

No old human B1 fixture.

==================================================
INTERPRETATION
==================================================

Primary witness:

- real source contact; AND
- resolved positive source-debit/body-credit transfer.

Before attributing usefulness to sensory feedback, compare with the
sensory-free control.

Allowed claim if witnessed:

"A fixed external controller restricted at runtime to the organism's
permitted sensory history produced a bounded productive source interaction
under held-out starting conditions."

CHEMISTRY-HIDDEN provides only a bounded modality-deprivation comparison.

Do NOT claim:
- chemistry necessity;
- optimal sensing;
- general navigation;
- source recognition;
- P learning;
- developmental efficacy;
- survival competence.

A simple-controller failure does NOT establish sensory information absence.
It returns the issue for Jason review.

==================================================
EXISTING HUMAN OBSERVATION
==================================================

Preserve FULL-RAW exactly:

20.2 simulated seconds
202 human commands

Retain only as a bounded qualitative apparatus observation.

Jason reports that during use:
- the channels appeared live and coherent;
- sensor changes appeared consistent with interaction/movement;
- navigation from the interface seemed conceivable with enough
  familiarisation;
- manual 0.1-second command entry was prohibitively inefficient.

Do not convert those statements into a quantitative B1 PASS.

CHEMISTRY-HIDDEN remains withdrawn before start:
0 simulated seconds / 0 steps / 0 commands.

==================================================
RESOURCE INTENT
==================================================

The new design should be radically smaller than v0.1.

Do not redesign storage.
Do not create a new ML training pipeline.
Do not improve the human UI.
Do not add additional perceptual objectives.

This is the last bounded perceptual-ceiling closure before moving to P
developmental testing unless a material defect is found.

==================================================
DELIVERY
==================================================

Return:

1. apparatus identity/provenance clarification;
2. B1_MINIMAL_CLOSURE_DESIGN_v0_2;
3. proposed deterministic controller law in plain language;
4. exact runtime information boundary;
5. proposed 3-start / 3-arm case structure;
6. estimated simulation/wall/storage cost;
7. explicit statement of what result would be enough to close B1;
8. explicit stop condition if the simple controller cannot provide a
   credible witness.

DESIGN ONLY.

No implementation.
No new simulation.
No authority.
No P/world change.

Stop for Jason review.