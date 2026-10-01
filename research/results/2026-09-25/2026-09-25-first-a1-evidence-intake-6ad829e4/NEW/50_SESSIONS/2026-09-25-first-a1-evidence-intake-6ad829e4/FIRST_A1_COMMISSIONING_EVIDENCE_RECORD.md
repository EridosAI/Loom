# First Loom P coupling-commissioning evidence record

**Recorded:** 2026-09-25. **Classification:** observed commissioning evidence from one bounded external-control A1 witness, with incomplete V3 post-analysis. This registration adds no physical execution or corrected analysis.

P engineering: **VERIFIED**  
Commissioning apparatus: **FIT / CLOSED FOR PRE-RUN ENGINEERING**  
Coupling commissioning: **IN PROGRESS**  
First physical witness: **A1 OBSERVED — bounded external-control witness**  
V3: **INCOMPLETE — post-analysis checker limitation**  
Scientific/developmental efficacy: **UNTESTED**

**COUPLING COMMISSIONING HAS BEGUN.** The previous [mechanical closure](../../30_REVIEWS/REVIEW-P-APPARATUS-MECHANICAL-CLOSURE-5f077481-2026-09-25-c84f219a.md) remains the pre-run engineering disposition; its “NOT STARTED / UNCOMMISSIONED” statements describe that earlier stage. The present evidence does not retroactively change any prior checkpoint hold or engineering review.

## Exact source and execution identities

| Identity | Value |
|---|---|
| P implementation | `6bc9683b54e4fa80136fe8534d7713e2a250a95f` |
| Commissioning apparatus | `5f07748102cb5eaa302569c87efbae095050e9fe` |
| Executed canonical authority object | `a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc` |
| Case / mode / controller | `A1` / `external_controller` / `waypoint` |
| Scope | V1–V3, A0 and exactly one A1 external physical witness |
| Packaged execution finish | `2026-09-25T01:42:03.679522+00:00` |

Primary evidence: [original A1 report](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/FIRST_A1_COMMISSIONING_REPORT.md), [verified result ZIP](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/FIRST_A1_COMMISSIONING_RESULT.zip), [saved result summary](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/A1_RESULT_SUMMARY.json), [original trajectory receipt](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/trajectory-001/manifest.json) and [delivery identity receipt](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/DELIVERY_RECEIPT.json). The result ZIP preserves the complete raw `evidence/trajectory-001/` tree, including all streams, snapshots, display, receipt and original analysis files. It also preserves the complete original calculation tables `evidence/read-only-review/A1_OBSERVATIONS.json` and `V2_ACCOUNTING.json`.

## Jason-accepted authority, distinct from observations

The [untouched authorization source](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/AUTHORIZATION_SOURCE.txt) explicitly approves the exact object above for V1–V3/A0 and one A1, with “Report-don’t-patch.” Its [closed approval envelope](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/APPROVAL_REQUEST.json), [canonical approved bytes](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/APPROVED_OBJECT.canonical.json) and [actual launched manifest and six-field grant](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/LAUNCHED_MANIFEST.json) are preserved. The canonical object in the executed result is byte-identical to the original launch packet's object, and its SHA-256 matches the approved identity.

The [untouched launch packet](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip) and [original launch description](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET/FIRST_COMMISSIONING_LAUNCH_PACKET.md) retain their pre-approval “PROPOSED / NOT AUTHORIZED” labels. Those are historical preparation labels; later genuine authorization is recorded separately above. No proposal text or bound path has been rewritten. The packet's statement about an older Workbench HOLD is also its preparation-time navigation observation, not current status.

The declared manufactured external start used body centre (6,3), facing west, $E=0.7$ and $I=1$, the existing life-0 cache and phase, and one source-0 pressure stage at requested force 0.1. It was not a newborn life or intact-P actuation. The 120 s simulated ceiling and 1,200 s run wall limit belonged to that exact object. This intake records the already exercised authority; it grants no repetition, resume, extension, changed route, subsequent case or architectural decision.

## Observed commissioning evidence

V1, V2 and A0 completed; exactly one A1 external physical witness executed. It stopped administratively at **91.83 simulated seconds** / **9,183 native rows**, cause `wall_time_limit`, record `complete=True`. No retry, resume or replacement trajectory occurred; the remaining **28.17 s** of the 120 s ceiling is unobserved. V3 post-check is incomplete at the preserved sensor/native-count assertion; it has not been corrected or rerun.

The saved execution time is `91.83000000001007` s; 91.83 s is the report's readable value. `complete=True` records closure of the stopped attempt's records, not completion of the 120 s ceiling or all commissioning checks. Original evidence reports no physical nonviability and no controller/apparatus exception. The V3 checker failure is a separate analysis result.

The tables reproduce the saved summary's numeric values at its recorded precision. The report rounds them for reading; no tolerance, gate or physical quantity has been changed.

### Physical approach and contact

| Observation | Packaged value |
|---|---|
| Contact locus reached / certified source-0 contact | yes / yes |
| Minimum recorded source surface gap | 3.3640645824561943e-11 |
| First certified source-0 contact, s | 6.31019048650431 |
| Positive-duration source contact, s | 85.5198095134956 |
| Contiguous contact intervals | 1 |
| Measured contact-force range | 0.099976508452766 to 0.27074663791428305 |
| Requested contact-force target | 0.1 |

### Energy and accounting

| Observation | Packaged value |
|---|---|
| Source-0 transfer | 0.190521120590528 |
| Reconstructed source debit | 0.19052112059052898 |
| Reconstructed body credit | 0.19052112059052115 |
| Whole-attempt expenditure | 0.15177513857116529 |
| Energy, initial → final | 0.7 → 0.7387459820193558 |
| Whole-attempt energy change | +0.03874598201935586 |
| Source-0 final stock | 0.03425013279694742 |
| Cumulative source-0 renewal | 0.024771253387476377 |
| Maximum accounting residual | 5.550945716536332e-17 |
| Existing arithmetic tolerance | 1e-12 |

### Windows, integrity and records

| Observation | Packaged value |
|---|---|
| Complete fixed 0.2 s windows, total | 459; 428 contain contact, 31 do not |
| Complete contact-containing bins with resolved positive / negative net energy | 229 / 199 |
| Partial tail | 1; retained separately |
| First complete positive-net contact-containing bin | 6.2–6.4 s |
| Energy change in that bin | +0.0004434545354845554 |
| Integrity, initial → final | 1.0 → 0.9930767410641572 |
| Physical nonviability / terminal dimension | none / `None` |
| Controller/apparatus exception | none; separate V3 analysis AssertionError retained |
| Native / physical event / controller decision / neural wave rows | 9,183 / 9,185 / 919 / 0 |
| Sensor entries / diagnostic rows | 9,184 / 9,183 |


The transfer, reconstructed debit and reconstructed credit round to the same reported `0.190521120591`; their machine-precision values are separately retained above, rather than asserted to be bit-identical. Source-0 debit minus transfer is `9.71445146547012e-16` and body credit minus transfer is `-6.855627177060342e-15`. The existing arithmetic tolerance and maximum residual are recorded as evidence, not new acceptance gates.

The first positive bin's saved endpoints are `6.199999999999912` and `6.399999999999908` s. First contact occurs inside that bin. “Complete” denotes the full fixed time bin; it does not mean contact throughout all 0.2 s. Whole-attempt energy gain is distinct from the positive and negative contact-containing windows. One partial terminal bin remains separate.

## Completed checks and the preserved V3 limitation

| Item | Recorded disposition |
|---|---|
| V1 | Completed; preflight identities and the existing post-record validator with `replay=false` are preserved |
| V2 | Completed; historical precheck remains labelled historical, and the actual A1 contact/accounting operands remain distinct |
| A0 | Completed without world evolution; geometry only, no bypass/crossing trajectory |
| A1 | One external physical witness observed, administratively truncated |
| V3 | Initial checks completed; post-check **INCOMPLETE** at the original assertion; subsequent comparisons not reached |

Sources: [V1/V3 preflight](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/V1_V3_PREFLIGHT.json), [V1 post-record validation](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/V1_POST_RECORD_VALIDATION.json), [A0 geometry](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/A0_GEOMETRY.json), [V3 limitation](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/V3_POST_CHECK_LIMITATION.md), [V3 count finding](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/V3_COUNT_FINDING.json), [original AssertionError](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/V3_BOUNDARY_ERROR.json) and [original failed checker — preserved source, not a runnable instruction](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/read_results.py).

The checker wrongly asserted equal native/sensor/diagnostic counts. The recorder contains one initial sensor/display envelope at native index 0, followed by the per-step rows: **9,184 sensor entries versus 9,183 native and diagnostic rows**. This is the preserved reader/schema-assumption limitation, not evidence of an extra native update.

The recorded preceding comparisons of complete inactive-organism state, organism RNG counters, manifest equality and closed display schema had completed before the assertion. Subsequent display/stream, actual controller-input, issued/delivered-command, raw/native and E/I cadence comparisons and final counter/state assertions were not reached. The separately completed existing segment validator checked its issued-decision journal, sequence, receipt/file hashes, ledger and stop classification with no physical replay. It does not make V3 complete.

No corrected V3 checker, rerun or replacement analysis is supplied or performed here. Any later corrected read-only analysis must be a **new analysis of this same immutable A1 evidence**, linked to this original failure. It must not replace the failed checker, its error, these findings or the trajectory.

## Claim boundary

One externally controlled commissioning witness demonstrated that the implemented finite body can, in the tested geometry, physically reach source-0, establish solver-certified contact, receive real source-to-body energy transfer, and experience complete contact-containing intervals with resolved positive net energy under the implemented mechanics and accounting. This statement retains the incomplete V3 post-check qualification above.

This does **not** establish that P can discover, perceive, recognise, learn from or regulate toward the source; newborn bootstrap; survival capability; global ecological sufficiency; indefinite viability; or usefulness of P, R or any associative mechanism. The neural object was inactive in this external arm; zero neural waves does not constitute a perceptual/developmental trial. P remains scientifically **UNTESTED for learning/developmental efficacy**. No P PASS/FAIL, scientific efficacy result or new experiment number is assigned.

## Unresolved observations and work not performed

Retain as observations/open interpretations: integrity declined from 1 to 0.9930767410641572; measured force reached 0.27074663791428305 while the requested target was 0.1; contact contained both positive-net and negative-net windows; the wall-time boundary truncated the 120 s ceiling at 91.83 s; and V3 remains incomplete. These are not automatically apparatus defects, mechanism failures or permission to change configuration.

Not performed: A2–A5; B1–B4; C1/C2; newborn lives; fixed-structure diagnostic; perceptual commissioning; developmental/scientific trials; efficacy testing; tuning/sweeps; or evidential freeze. The remaining 28.17 s is unobserved. This task introduces **no assistant proposal** for a new route, case, parameter, architecture or sequence. All earlier candidate alternatives, accepted Base World choices and decisions remain unchanged.

## Source discrepancy and custody

The intake request says **“459 complete contact windows.”** The primary summary says `complete_fixed_windows: 459`. The saved `all_fixed_windows` labels contain **428 complete bins with contact** (229 positive, 199 negative), **31 complete bins without contact**, and **one separate partial contact tail**. This registration follows those primary records and explicitly preserves the discrepancy. [Source-conflict record](SOURCE_CONFLICTS.json) records the label census; it is not new physical analysis or a corrected V3 check. Rounded human-readable values versus machine precision are retained as representations of the same saved quantities.

The package, report copies, original authority and launch packet agree on their identities. The source ZIP passed its supplied receipt, every payload hash/size and CRC; the embedded launch packet matches the separately supplied launch ZIP and its manifest. [Source identities](SOURCE_IDENTITIES.json) and [intake completion](INTAKE_RECORD.md) record the exact checks and edits. No packaged code, validator, checker, replay or scientific trial was executed by this intake. No canonical repository document, configuration, world/mechanism law, accepted architecture or commissioning sequence was changed.
