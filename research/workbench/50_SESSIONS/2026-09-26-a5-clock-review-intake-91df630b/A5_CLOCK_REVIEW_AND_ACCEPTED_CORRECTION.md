# A5 clock review and accepted apparatus correction

**Registered:** 2026-09-26. **Classification: APPARATUS DEFECT — correction required to pose approved longer horizons.**

Jason has explicitly accepted the native-index scheduling correction as a commissioning-apparatus fix, subject to the [exact ruling and constraints](../../40_DECISIONS/DECISION-P-APPARATUS-CLOCK-2026-09-26-91df630b.md#jasons-exact-ruling). The review was written before that acceptance; its original pending-decision statements remain preserved. **Acceptance is recorded; implementation and engineering verification remain outstanding. No A5 execution occurred.**

P engineering: **VERIFIED within its prior reviewed scope**  
Commissioning apparatus: **A5 clock defect OPEN; scoped correction JASON-ACCEPTED; implementation/verification outstanding**  
Coupling commissioning: **IN PROGRESS; A5 held before execution**  
Scientific/developmental efficacy: **UNTESTED**

| Commissioning item | Current status |
|---|---|
| V1 / V2 / V3 | COMPLETE |
| A0 | COMPLETE within its bounded scope |
| A1–A4 | OBSERVED within their bounded scopes |
| A5 | PREPARED / HOLD / NOT LAUNCH-READY; NOT EXECUTED |
| B1–B4 | NOT EXECUTED |
| C1/C2 | NOT EXECUTED |

## Exact scope and identities

Reviewed apparatus: `5f07748102cb5eaa302569c87efbae095050e9fe`. Unchanged P baseline: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Held A5 proposal: `88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6`. The [held packet and preparation](../../50_SESSIONS/2026-09-26-a5-held-intake-62c8f4b1/A5_HELD_PROPOSAL_RECORD.md), its [canonical bytes](../../90_SOURCES/p_a5_held_proposal_2026-09-26_62c8f4b1/AUTHORITY_OBJECT.canonical.json), OPEN_ISSUE_A5_CLOCK.md and CLOCK_AUDIT.json remain unchanged. The proposed 630 s source 0 → 1 → 0 → 1 circuit and approximately 210–222 s unattended renewal opportunities are unchanged and unexecuted. The held hash identifies that proposal; it is not a new launch authority.

Primary source: [complete clock-compatibility review](../../90_SOURCES/p_a5_clock_review_2026-09-26_91df630b/A5_CLOCK_COMPATIBILITY_REVIEW/A5_CLOCK_COMPATIBILITY_REVIEW.md) (§§2–9 for diagnosis/options/closure requirements, §11 for prior evidence). Supporting records: [diagnostic results](../../90_SOURCES/p_a5_clock_review_2026-09-26_91df630b/A5_CLOCK_COMPATIBILITY_REVIEW/DIAGNOSTIC_RESULTS.json), [arithmetic detail](../../90_SOURCES/p_a5_clock_review_2026-09-26_91df630b/A5_CLOCK_COMPATIBILITY_REVIEW/ARITHMETIC_DETAIL.json), [clock history](../../90_SOURCES/p_a5_clock_review_2026-09-26_91df630b/A5_CLOCK_COMPATIBILITY_REVIEW/CLOCK_HISTORY.json), [preservation](../../90_SOURCES/p_a5_clock_review_2026-09-26_91df630b/A5_CLOCK_COMPATIBILITY_REVIEW/PRESERVATION.json), [source verification](../../90_SOURCES/p_a5_clock_review_2026-09-26_91df630b/A5_CLOCK_COMPATIBILITY_REVIEW/FINAL_VERIFICATION.json). [Original ZIP](../../90_SOURCES/p_a5_clock_review_2026-09-26_91df630b/A5_CLOCK_COMPATIBILITY_REVIEW.zip) and all source members are preserved byte-for-byte.

## Recorded defect and diagnosis

| Quantity | Reviewed finding |
|---|---|
| First affected scheduled command | Native step 26,950 |
| Accumulated physical clock | 269.4999999998999 s |
| Intended nominal boundary | 269.5 s |
| Discrepancy | -1.0010126061388291e-10 s; exceeds fixed 1e-10 allowance |
| Rejecting predicate | `pending.py::validate_decision`: `issued decision clock mismatch` |
| Separate later failure | Nominal 270 s stage transition remains not due under accumulated time; proposed hold crosses prescribed stage boundary |

These are static/scalar and detached-predicate diagnosis findings, conditional on full nonterminal native steps reaching those boundaries. They are **not an observed A5 trajectory failure**. Loosening only the absolute clock comparison would leave the 270 s stage rejection unresolved.

Float resolution itself remains adequate through the proposed 630 s horizon. The defect is inconsistent use of accumulated floating-point clock values for discrete controller scheduling. The recommended correction gives native indices ownership of stage selection, command holds and stopping while retaining and validating the existing physical clock. It must not replace physical time with index-derived timestamps, change physical event tolerance, retime the mover/fields, or weaken authority binding. The accepted direction is source option D, not wholesale approval of every engineering detail or alternative in the source.

Source §9 describes the closure requirements still to be implemented and verified: consistent index ownership at runner/controller/pending/validator call sites; physical-clock validation against the original recurrence; strict admission of native-boundary deadlines; preservation of partial-terminal handling, hold limits and restart/journal continuity; versioned instrument/authority identities. A scalar oracle showing 6,300 prescribed holds fit does not verify a future implementation.

## Prior A1–A4 evidence remains unchanged

The source's read-only retrospective metadata check reports **all 5,579 saved A1–A4 controller decisions retain their expected stage under the reviewed index interpretation**, with zero stage mismatches. Counts are A1: 919; A2: 1,800; A3: 2,100; A4-CROSS: 160; A4-WAIT: 280; A4-DETOUR: 320. Each A4 case retains its own original clock origin. This is a reported metadata check, not replay, recomputation of trajectories, or a new scientific result.

The [prior A4 evidence and earlier chain](../../50_SESSIONS/2026-09-26-a4-evidence-intake-0e69b3c8/A4_COMMISSIONING_EVIDENCE_RECORD.md) retain their observations, limits and interpretations, including A1's original post-check history, A2's retained helper flags, A3's contact/damage limitations and A4's analytic/comparison limits. Previous apparatus checkpoint dispositions retain their reviewed scopes. The new longer-horizon defect does not rewrite prior closure or mark P, A5 ecology, source renewal or stock as failed.

## Accepted decision, alternatives and remaining boundary

Jason's current acceptance is recorded in the [new decision record](../../40_DECISIONS/DECISION-P-APPARATUS-CLOCK-2026-09-26-91df630b.md); it is distinct from the source recommendation and from the earlier held-proposal record. Physical simulation time, native dt, controller hold duration, P, world laws, controller routes, A5 ecological design and A1–A4 interpretation must remain unchanged. No numerical world setting or canon amendment is accepted by this ruling.

Source §8 preserves the alternatives: raising/removing the guard, changing physical world time, local-stage clocks, and a carefully justified apparatus-only error envelope. They remain source alternatives, not selected changes. Acceptance chooses the bounded native-index correction direction, without claiming the correction has been built or closed.

**A5 remains PREPARED / HOLD / NOT LAUNCH-READY.** Correction implementation and engineering verification are outstanding. Any later changed instrument requires its own exact identity, review and separately bound execution authority. The held packet/hash is not edited or reused as permission to launch. This session stops at recording and navigation; no implementation, simulation, replay, continuation or new authority object was produced.

## Source preservation and verification limits

The source reports six detached legacy tests passed, 13 detached legacy controller calls, and zero A5 controller calls, world/field/neural steps, RNG draws or world/Run construction. Those are supplied diagnostic results; this intake did not run those tests or the packaged helper. Its before/after inventories contain the same 250 identities. The original DIAGNOSTIC_RESULTS scalar wave entry and the later ARITHMETIC_DETAIL supplement are both retained: built-in summation reported 0.2, whereas explicit repeated addition gives 0.20000000000000004. The supplement documents the production-style arithmetic distinction; neither file was rewritten.

Intake verified the archive SHA-256 against its receipt/sidecar, all 53 payload hashes and CRCs, all 54 expanded inbox members, all 42 packaged reference identities, the five held-reference copies against registered originals, and the held canonical hash. It checked saved retrospective counts, no-mismatch flags and zero-execution fields. These are custody/registration checks, not an independent rerun of the diagnosis or certification of a correction. No necessary source gap or identity conflict was found.

[Source identities](SOURCE_IDENTITIES.json) · [Completion record](INTAKE_RECORD.md) · [Intake validation](VALIDATION.json).
