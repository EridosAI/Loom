---
id: "DECISION-P-APPARATUS-CLOCK-2026-09-26-91df630b"
authority_status: accepted-by-jason
work_status: correction-implementation-and-verification-outstanding
evidence_status: not-an-experimental-result
---

# Accepted native-index scheduling correction

**Recorded:** 2026-09-26. **Decision authority:** Jason. **Scope:** narrowly bounded commissioning-apparatus correction. **Proposer:** supplied clock-compatibility review; acceptance below is Jason's explicit current ruling.

## Jason's exact ruling

> I accept the native-index scheduling correction as a commissioning-apparatus fix. It must not change physical simulation time, P, world laws, controller routes or the interpretation of A1–A4.

Source anchor: Jason's latest user message in the current workbench intake conversation, received after the instruction to record a pending decision and before this record was written. No native message identifier or independent chat export is available. This quotation records the supplied wording; this authored note is not a complete chat export.

## Effective change and constraints

The native-index scheduling correction is **ACCEPTED**, replacing its previous pending-decision status. It may correct discrete stage ownership and command scheduling in the commissioning apparatus while retaining and validating the existing accumulated physical simulation clock.

The earlier proposed wording to which the acceptance responds was:

> Permit a narrowly scoped commissioning-apparatus correction replacing floating-clock stage ownership/command scheduling with native-index-derived scheduling. Physical simulation time, native dt, controller hold duration, world laws, P and all previous evidence remain unchanged.

The explicit ruling additionally names unchanged controller routes and unchanged interpretation of A1–A4. Keep physical time, native dt, hold duration, world laws, P, routes, A5 ecological design, numerical world settings and previous evidence unchanged. Do not retime physical dynamics or translate prior evidence onto a new clock. This decision does not accept an unbuilt implementation, certify closure, grant A5 execution, or amend canon.

## Review basis and alternatives

The [registered diagnosis](../50_SESSIONS/2026-09-26-a5-clock-review-intake-91df630b/A5_CLOCK_REVIEW_AND_ACCEPTED_CORRECTION.md) classifies the defect at exact apparatus `5f07748102cb5eaa302569c87efbae095050e9fe` as **APPARATUS DEFECT — correction required to pose approved longer horizons**. Source [§8 alternatives](../90_SOURCES/p_a5_clock_review_2026-09-26_91df630b/A5_CLOCK_COMPATIBILITY_REVIEW/A5_CLOCK_COMPATIBILITY_REVIEW.md#8-candidate-closures-compared) and [§9 closure requirements](../90_SOURCES/p_a5_clock_review_2026-09-26_91df630b/A5_CLOCK_COMPATIBILITY_REVIEW/A5_CLOCK_COMPATIBILITY_REVIEW.md#9-exact-requirements-for-the-recommended-closure) retain the technical basis. Option D is the accepted direction; detailed implementation remains subject to verification against these constraints. Raising/removing a guard alone, changing physical world time, local-stage clocks and a justified error-envelope alternative remain preserved as unselected source options.

## Supersession and chronology

This acceptance supersedes only the pending Jason decision in the [held preparation history](../50_SESSIONS/2026-09-26-a5-held-intake-62c8f4b1/A5_HELD_PROPOSAL_RECORD.md) and the source review's recommendation status. It does not overwrite either source. The source review's “STOP FOR JASON” and “proposals only” labels remain true of that document's preparation stage. Earlier decision records and exact checkpoint histories remain unchanged.

## Current disposition

**Correction direction: JASON-ACCEPTED. Implementation and engineering verification: OUTSTANDING.**

**A5: PREPARED / HOLD / NOT LAUNCH-READY; NOT EXECUTED.** Held authority identity `88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6` and its [canonical bytes](../90_SOURCES/p_a5_held_proposal_2026-09-26_62c8f4b1/AUTHORITY_OBJECT.canonical.json) remain unchanged. A later corrected instrument needs its own exact reviewed identity and separately bound execution authority; acceptance of this fix is not A5 launch approval.

A0–A4 retain completed/observed bounded scopes and interpretations. B1–B4 and C1/C2 remain not executed. Scientific/developmental efficacy remains **UNTESTED**. This recording session implements no correction, creates no experiment number and executes no commissioning or scientific trial.
