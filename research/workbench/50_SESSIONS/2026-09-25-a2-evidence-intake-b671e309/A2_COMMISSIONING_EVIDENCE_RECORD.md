# A2 — observed coupling-commissioning evidence

**Registered:** 2026-09-25. **Disposition: OBSERVED COMMISSIONING EVIDENCE.** This registers the single already-executed, authorized A2 case. It adds no execution, experiment number or change to the commissioning sequence.

P engineering: **VERIFIED**  
Commissioning apparatus: **FIT / pre-run engineering CLOSED**  
Coupling commissioning: **IN PROGRESS**  
Scientific/developmental efficacy: **UNTESTED**

| Commissioning item | Current status |
|---|---|
| V1 | COMPLETE |
| V2 | COMPLETE |
| V3 | COMPLETE |
| A0 | COMPLETE |
| A1 | OBSERVED |
| A2 | OBSERVED — OBSERVED COMMISSIONING EVIDENCE |
| A3–A5 | NOT YET EXECUTED |
| B1–B4 | NOT YET EXECUTED |
| C1/C2 | NOT YET EXECUTED |

## Authority and continuity

- Exact A2 authority: `229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007` — [approved canonical object](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/APPROVED_OBJECT.canonical.json) and [exact authorization text](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/AUTHORIZATION_SOURCE.txt).
- P engineering baseline: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.
- Apparatus checkpoint: `5f07748102cb5eaa302569c87efbae095050e9fe`.
- Primary report: [A2_PLAIN_LANGUAGE_RESULT.md](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/A2_PLAIN_LANGUAGE_RESULT.md).
- Complete verified delivery: [original A2 result ZIP](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/A2_COMMISSIONING_RESULT.zip) and [payload identity manifest](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/FILE_MANIFEST.json).
- Supporting detail: [technical report](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/A2_COMMISSIONING_REPORT.md), [full-precision summary](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/A2_RESULT_SUMMARY.json) and [observation records](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/A2_OBSERVATIONS.json).

This continues the workbench's [first A1 commissioning record](../../50_SESSIONS/2026-09-25-first-a1-evidence-intake-6ad829e4/FIRST_A1_COMMISSIONING_EVIDENCE_RECORD.md) and [completed V3 / passive viewer record](../../50_SESSIONS/2026-09-25-v3-viewer-intake-4e7b80c2/A1_V3_REANALYSIS_AND_VIEWER_CONTINUATION.md). A2 is its own single authorized trajectory, initialized from the approved original time-zero snapshot; it is not a continuation of A1's final state. Departure inside A2 occurred without reset. The original A1 trajectory, original failed V3 post-check, corrected read-only V3 analysis and passive A1 viewer retain their distinct identities and dispositions.

The [original launch packet](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/approved-launch/A2_LAUNCH_PACKET/A2_LAUNCH_PACKET.md) and its receipt retain their pre-approval “PROPOSED / NOT AUTHORIZED” history unchanged. The later exact authorization and execution record establish this A2 case's separate authority. The grant required report-don't-patch and no retry, route substitution, tuning, continuation or additional case without separate authorization. It grants no new execution through this intake.

## Recorded sequence

Values below follow the requested reporting precision; linked records retain full precision and timestamps.

| Observation | Recorded result |
|---|---|
| Extent and stop | 18,000 native steps; prescribed 180 s administrative cutoff |
| First source-0 contact | 6.31019 s |
| First negative-net source-0 window | 52.0–52.2 s, while stock remained about 0.0663 |
| Departure, without reset | 90 s; E = 0.7400694; I = 0.9930767; source-0 stock = 0.0351485 |
| Actual release-to-source-1 contact travel | 42.37643 s; energy cost = 0.07565365; intake = 0 |
| First source-1 contact | 132.37643 s; pre-contact stock = 0.2 |
| Source-1 total transfer | 0.15144825 |
| First positive-net source-1 window | 132.4–132.6 s |
| Final reserves | E = 0.7381512; I = 0.9863441 |
| Terminal crossing | None |
| Mover contact | None |
| Execution exception | None |

The negative result concerns a recorded finite 0.2 s local window, not an inferred exact instantaneous zero crossing. Source-0 stock in that window changed from 0.06652155860849777 to 0.06626443259547216; its net energy change was -1.1218724983441675e-06. The externally prescribed departure at 90 s is not evidence that P detected or acted on this change.

## Whole-case accounting and source history

| Quantity | Recorded result |
|---|---|
| Gross intake | 0.34031477 |
| Expenditure | 0.30216354 |
| Net E | +0.03815123 |
| Source-0 transfer | 0.18886653 |
| Source-0 stock at final stop, after post-departure renewal | 0.06836337 |
| Source-1 final stock | 0.05928729 |
| Other six source stocks | Each remained 0.2 |

See the preserved [accounting result](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/ACCOUNTING.json) and [complete fixed-window results](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/ALL_FIXED_WINDOWS.json). Post-departure renewal of source 0 was recorded; no return to that source or renewal-supported cycle was demonstrated.

## Physical observations retained without interpretation

- Both source contacts briefly exceeded the 0.25 stress threshold.
- Peak contact forces were approximately 0.27075 and 0.27327 (full recorded maxima 0.27074663791428305 and 0.27326702539735814).
- Total integrity loss was 0.01365586 (full recorded value 0.013655858384640111).
- Source-1 contact contained two microscopic release/recontact gaps: 142.76000000001514–142.7600395926028 s and 164.19999999999564–164.20003960557497 s, each about 0.0000396 s.
- No repair occurred.

No further mechanism, safety, viability or ecological interpretation is attached to these observations. No mover contact is recorded; this does not establish absence of optical exposure, whose object identities are not recorded.

## Reporting limitation — retain the original helper flags

The [original timing reporting note](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/TIMING_REPORTING_NOTE.json) and every original derived artifact are preserved byte-identically. No analysis or simulator patch was made during this intake.

| Flagged event | Recorded endpoint | Nominal boundary | Offset in seconds | Within existing event-time tolerance |
|---|---|---|---|---|
| 9001 | 90.00000000000914 | 90.0 | 9.137579581874888e-12 | true |
| 12002 | 120.00000000002449 | 120.0 | 2.4485302674293052e-11 | true |

Existing `event_time_tolerance` remains `1e-10`. The raw stage helper fields remain:

| Interval | `boundary_straddling_events` | `complete_event_boundary_coverage` |
|---|---|---|
| Nominal stage 0, 0–90 s | `[9001]` | `false` |
| Nominal stage 1, 90–120 s | `[9001, 12002]` | `false` |
| Nominal stage 2, 120 s to recorded stop | `[12002]` | `false` |
| Nominal commanded-travel interval, 90.0 s to source-1 contact | `[9001]` | `false` |
| Exact recorded release-to-source-1-contact interval | `[]` | `true` |

The actual recorded release is 90.00000000000914 s, and source-1 contact is 132.3764279535912 s: duration **42.37642795358205 s**, energy cost **0.07565364813787812**, intake **0**. The nominal-boundary flags do not change this interval or its accounting.

The raw `planned_unobserved_seconds` / horizon subtraction value **1.872990651463624e-11** is also retained exactly. The supplied timing note identifies it as a representation residual, not a missing native step. It states that the helper over-flags sub-tolerance nominal-boundary endpoint offsets; the flags identify no extra or missing physical step. This is the supplied reporting qualification, not a patched result or a new tolerance.

## Strongest bounded claim and withheld claims

> One externally controlled physical witness demonstrated declining local source usefulness before stock reached zero, departure without reset, reserve-consuming travel to a different source, and renewed productive energy transfer at that second source under the unchanged world/body laws.

Explicitly withheld:

- P discovery, perception, learning or regulation;
- autonomous switching;
- survival capability;
- indefinite viability;
- renewal-supported cyclic sustainability;
- broad ecological sufficiency.

The external waypoint controller supplied the route, with the organism inactive for this witness. Whole-case positive net energy is not a test of P's scientific or developmental efficacy. That efficacy remains **UNTESTED**.

## Verification scope and source distinctions

The [execution result](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/EXECUTION_RESULT.json) records one constructor attempt, no retry/resume/patch, no physical replay, and a completed administrative cutoff. The [subsequent read-only analysis](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/ANALYSIS_RESULT.json) reports all five saved-record sections completed without errors, 39 raw files unchanged, zero new simulation steps, zero controller-command computations and zero physical replays.

The [record-integrity result](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/RECORD_INTEGRITY.json) records 18,001 sensor envelopes, 1,800 controller rows, 18,000 native rows, 18,009 event rows and 18,000 diagnostic rows. The [boundary/delivery result](../../90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/BOUNDARY_AND_DELIVERY.json) is a saved-record analysis, not a new execution. Production `verify_segment` was explicitly not invoked: its pending-command validator recomputes waypoint commands even with `replay=False`. The source reports separate read-only receipt, authority, sequence, boundary, accounting and delivery checks. This intake does not relabel them as a production verifier run.

Intake independently checked the outer ZIP against its receipt, all **60 payload hashes and CRCs**, and all **61 unpacked members** against the supplied folder. The embedded launch ZIP matches its separate delivery, with all **75 launch payload hashes and CRCs** verified. The approved canonical bytes match the launch object and hash to the exact A2 authority. The embedded A1 archive matches the previously registered original. Supplied before/after original-file manifests and before/after raw-analysis manifests match byte-for-byte. These checks establish source custody and registration consistency; the reported scientific/physical observations are attributed to the supplied result, not independently rerun here.

Jason's current instruction supplies intake authority and the bounded reporting scope. Observations remain distinct from that authority. No new assistant mechanism proposal, numerical choice or sequence change is adopted. No necessary source gap or conflicting package identity was found. No supplied program, checker, controller, viewer or simulation was executed in this intake; no actual Loom repository or canonical document was changed.

[Source identities](SOURCE_IDENTITIES.json) · [Intake completion](INTAKE_RECORD.md) · [Final custody/navigation validation](VALIDATION.json).
