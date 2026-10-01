# Loom research map

## Current commissioning boundary — final clock correction verified, 2026-09-26

P engineering: **VERIFIED within its prior reviewed scope; unchanged**  
Commissioning apparatus: **FIT FOR A5 LAUNCH-PACKET REGENERATION**  
Native-index scheduling correction: **VERIFIED; both long-horizon failures CLOSED**  
Coupling commissioning: **IN PROGRESS; A5 NOT EXECUTED**  
Scientific/developmental efficacy: **UNTESTED**

| A5 boundary | Current status |
|---|---|
| Design | PREPARED DESIGN PRESERVED |
| Historical authority | OLD AUTHORITY HELD / NON-LAUNCHABLE |
| Clock blocker | CLOSED |
| Preparation | NEW LAUNCH PACKET REQUIRED |
| Execution | A5 NOT EXECUTED |

V1/V2/V3/A0 remain COMPLETE; A1–A4 remain OBSERVED within their bounded scopes; B1–B4 and C1/C2 remain NOT EXECUTED.

Corrected apparatus: `68db2c581f07200966d699a4f55a65f9b96df1e9`. Previous apparatus: `5f07748102cb5eaa302569c87efbae095050e9fe`. Native-index scheduling is verified; physical clock/world timing, P, configuration, world laws and A5 route/design remain unchanged. Both previously diagnosed long-horizon failures are closed. Final independent review: **176 worktree tests passed; 176 portable tests passed; 59 consequential fault/control pairs verified; 5,579 saved A1–A4 decisions checked; zero historical stage-assignment disagreements**.

Historical held A5 hash `88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6` and the HOLD packet remain unchanged and non-launchable. A new launch packet is required; none is created by this intake. A1–A4 retain original apparatus provenance and interpretations and are not relabelled as executions under 68db2c58. No A5 execution, experiment number, canon change or scientific efficacy claim follows.

[Final review registration](50_SESSIONS/2026-09-26-final-clock-review-intake-3af846d2/FINAL_CLOCK_CORRECTION_REVIEW_RECORD.md) · [Complete independent review](90_SOURCES/p_final_clock_review_2026-09-26_3af846d2/LOOM_P_NARROW_FINAL_CLOCK_REVIEW.md) · [Closure table](90_SOURCES/p_final_clock_review_2026-09-26_3af846d2/CLOSURE_TABLE.md) · [Preserved held design/authority](50_SESSIONS/2026-09-26-a5-held-intake-62c8f4b1/A5_HELD_PROPOSAL_RECORD.md) · [Accepted correction decision](40_DECISIONS/DECISION-P-APPARATUS-CLOCK-2026-09-26-91df630b.md). Earlier sections below preserve their dated dispositions.

## Preserved correction acceptance — before final verification, 2026-09-26

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

**APPARATUS DEFECT — correction required to pose approved longer horizons.** The review identifies valid-command rejection at native step 26,950 (physical time 269.4999999998999 s versus nominal 269.5 s) and a separate stage-transition rejection at 270 s. Float resolution remains adequate through 630 s; the defect concerns discrete scheduling with accumulated floating-point time.

Jason has **accepted the native-index scheduling correction as a commissioning-apparatus fix**. Physical simulation time, P, world laws, controller routes and the interpretation of A1–A4 must remain unchanged; native dt, controller hold duration, prior evidence and A5 ecological design are also preserved. The reviewed retrospective check retains the expected stage for all 5,579 saved A1–A4 decisions. Correction implementation and verification remain outstanding.

**A5 remains PREPARED / HOLD / NOT LAUNCH-READY. No A5 execution occurred.** Held proposal hash `88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6` is unchanged. No A5/ecological/P failure, inadequate renewal or inadequate source stock is recorded. Prior engineering dispositions retain their exact reviewed scopes. Acceptance of the apparatus correction does not authorize A5 execution or amend canon or numerical world settings.

[Exact accepted decision](40_DECISIONS/DECISION-P-APPARATUS-CLOCK-2026-09-26-91df630b.md) · [Review registration](50_SESSIONS/2026-09-26-a5-clock-review-intake-91df630b/A5_CLOCK_REVIEW_AND_ACCEPTED_CORRECTION.md) · [Complete source review](90_SOURCES/p_a5_clock_review_2026-09-26_91df630b/A5_CLOCK_COMPATIBILITY_REVIEW/A5_CLOCK_COMPATIBILITY_REVIEW.md) · [Held preparation history](50_SESSIONS/2026-09-26-a5-held-intake-62c8f4b1/A5_HELD_PROPOSAL_RECORD.md). Earlier sections below preserve their dated states, including the former pending-decision wording.

## Preserved A5 preparation — before clock review and acceptance, 2026-09-26

P engineering: **VERIFIED within its prior reviewed scope**  
Commissioning apparatus: **prior scoped closure retained; A5 clock compatibility PENDING REVIEW**  
Coupling commissioning: **IN PROGRESS; A5 held before execution**  
Scientific/developmental efficacy: **UNTESTED**

| Commissioning item | Current status |
|---|---|
| V1 | COMPLETE |
| V2 | COMPLETE |
| V3 | COMPLETE |
| A0 | COMPLETE within its bounded scope |
| A1–A4 | OBSERVED within their bounded scopes |
| A5 | PREPARED / HOLD / NOT LAUNCH-READY; NOT EXECUTED |
| B1–B4 | NOT EXECUTED |
| C1/C2 | NOT EXECUTED |

**A5 — PREPARED / HOLD / NOT LAUNCH-READY.** Held proposal authority identity: `88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6`. **APPARATUS / CLOCK-COMPATIBILITY QUESTION PENDING REVIEW.** No A5 simulation occurred; the hash identifies a held proposal, not execution approval.

Proposed bounded question: **630 simulated seconds; source 0 → source 1 → source 0 → source 1; approximately 210–222 s unattended renewal opportunity between revisits**. A static source/arithmetic audit found that the pinned apparatus would reject a valid nonterminal controller command at about **269.5 s**, before the first planned revisit, conditional on the case remaining nonterminal. No production failure or physical A5 outcome was observed.

[Held proposal record](50_SESSIONS/2026-09-26-a5-held-intake-62c8f4b1/A5_HELD_PROPOSAL_RECORD.md) · [Complete preserved packet](90_SOURCES/p_a5_held_proposal_2026-09-26_62c8f4b1/A5_LAUNCH_PACKET_HOLD.zip) · [Original open issue](90_SOURCES/p_a5_held_proposal_2026-09-26_62c8f4b1/OPEN_ISSUE_A5_CLOCK.md) · [Clock audit](90_SOURCES/p_a5_held_proposal_2026-09-26_62c8f4b1/CLOCK_AUDIT.json) · [Held canonical object](90_SOURCES/p_a5_held_proposal_2026-09-26_62c8f4b1/AUTHORITY_OBJECT.canonical.json) · [Zero-execution preparation checks](90_SOURCES/p_a5_held_proposal_2026-09-26_62c8f4b1/PREPARATION_CHECKS.json) · [Prior A4 evidence](50_SESSIONS/2026-09-26-a4-evidence-intake-0e69b3c8/A4_COMMISSIONING_EVIDENCE_RECORD.md).

Do not classify this as A5 failure, ecological failure, inadequate source renewal, inadequate source stock or P failure. A0–A4 and prior engineering closure retain their bounded scopes; the new A5 compatibility question remains pending review. No canon, mechanism, Base World configuration, numerical setting or commissioning-sequence change, repair, launch, new run or experiment number is authorized by this intake. Earlier sections below retain their dated dispositions.

## Preserved A4 intake — before A5 clock review, 2026-09-26

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
| A2 | OBSERVED |
| A3 | OBSERVED |
| A4 | OBSERVED |
| A5 | NOT EXECUTED |
| B1–B4 | NOT EXECUTED |
| C1/C2 | NOT EXECUTED |

**A4: OBSERVED COMMISSIONING EVIDENCE.** Executed batch authority `47a71e78ad4bbb920f2b29f7d9b0e3c5f520eb4905880916c85f0cc8bbb9f1e0`; P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; apparatus `5f07748102cb5eaa302569c87efbae095050e9fe`. A4-CROSS, A4-WAIT and A4-DETOUR each executed exactly once, retaining the prescribed 16/28/32 s ceilings. No mover collision, collision impulse, damage or bodily nonviability was observed; no retry/substitution/tuning/continuation occurred.

> Three predetermined externally controlled witnesses demonstrated physically realizable timed crossing, wait-then-cross and always-clear detour opportunities for the actual finite body under the unchanged mover and body/world laws.

[A4 evidence and case results](50_SESSIONS/2026-09-26-a4-evidence-intake-0e69b3c8/A4_COMMISSIONING_EVIDENCE_RECORD.md) · [Plain-language result](90_SOURCES/p_a4_commissioning_2026-09-26_0e69b3c8/evidence/read-only-review/A4_PLAIN_LANGUAGE_RESULT.md) · [Technical report](90_SOURCES/p_a4_commissioning_2026-09-26_0e69b3c8/evidence/read-only-review/A4_COMMISSIONING_REPORT.md) · [Complete verified package](90_SOURCES/p_a4_commissioning_2026-09-26_0e69b3c8/A4_COMMISSIONING_RESULT.zip) · [Previous A3 evidence](50_SESSIONS/2026-09-26-a3-evidence-intake-7c42a9d1/A3_COMMISSIONING_EVIDENCE_RECORD.md).

WAIT's immediate-proceed conflict remains a predeclared analytic argument, not an executed counterfactual. DETOUR uses independent endpoints and is not an equal-endpoint efficiency comparison. No all-phase safety or P perception/prediction/discovery/learning claim is made. This intake changes no canon, mechanism, Base World configuration, numerical setting or commissioning sequence, initiates no execution and creates no scientific experiment number. Earlier sections retain their dated historical dispositions.

## Preserved A3 intake — 2026-09-26

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
| A2 | OBSERVED |
| A3 | OBSERVED |
| A4/A5 | NOT EXECUTED |
| B1–B4 | NOT EXECUTED |
| C1/C2 | NOT EXECUTED |

**A3: OBSERVED COMMISSIONING EVIDENCE.** Executed authority `43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd`; P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; apparatus `5f07748102cb5eaa302569c87efbae095050e9fe`. The single case completed the prescribed **210 s / 21,000 native steps**, with no terminal crossing or execution error.

> One externally controlled physical witness demonstrated an uninterrupted world history containing actual nonterminal damage, repair-eligible contact, positive integrity restoration, departure from repair, subsequent travel, and productive energy-source contact under the unchanged body/world laws.

[A3 evidence record](50_SESSIONS/2026-09-26-a3-evidence-intake-7c42a9d1/A3_COMMISSIONING_EVIDENCE_RECORD.md) · [Plain-language result](90_SOURCES/p_a3_commissioning_2026-09-26_7c42a9d1/evidence/read-only-review/A3_PLAIN_LANGUAGE_RESULT.md) · [Contact-interruption note](90_SOURCES/p_a3_commissioning_2026-09-26_7c42a9d1/evidence/read-only-review/CONTACT_INTERRUPTION_NOTE.md) · [Technical report](90_SOURCES/p_a3_commissioning_2026-09-26_7c42a9d1/evidence/read-only-review/A3_COMMISSIONING_REPORT.md) · [Complete verified package](90_SOURCES/p_a3_commissioning_2026-09-26_7c42a9d1/A3_COMMISSIONING_RESULT.zip) · [Previous A2 record](50_SESSIONS/2026-09-25-a2-evidence-intake-b671e309/A2_COMMISSIONING_EVIDENCE_RECORD.md).

Preserve the limitations: total damage exceeded restoration; source-3 contact comprised 629 short support intervals with repeated recontact damage; no patch/tuning/retry/extension occurred. Uninterrupted world history does not imply uninterrupted contact. Explicitly withheld: general recovery capability; P discovery or perception; P learning/regulation; autonomous repair-seeking; survival capability; optimal repair duration; adequacy of repair rate; adequacy of damage/contact parameters. The intake changes no canon, P, Base World, mechanism, numerical settings or commissioning sequence; it initiates no execution and creates no scientific experiment number. Earlier sections below retain their dated historical dispositions.

## Preserved A2 intake — 2026-09-25

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

Exact A2 authority: `229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007`. P `6bc9683b54e4fa80136fe8534d7713e2a250a95f` and apparatus `5f07748102cb5eaa302569c87efbae095050e9fe` retain their reviewed dispositions. The single A2 completed **18,000 native steps** at the prescribed **180 s administrative cutoff**. There was no terminal crossing, mover contact or execution exception.

> One externally controlled physical witness demonstrated declining local source usefulness before stock reached zero, departure without reset, reserve-consuming travel to a different source, and renewed productive energy transfer at that second source under the unchanged world/body laws.

[A2 evidence and reporting limits](50_SESSIONS/2026-09-25-a2-evidence-intake-b671e309/A2_COMMISSIONING_EVIDENCE_RECORD.md) · [Primary plain-language result](90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/A2_PLAIN_LANGUAGE_RESULT.md) · [Complete verified result package](90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/A2_COMMISSIONING_RESULT.zip) · [Original unchanged timing flags](90_SOURCES/p_a2_commissioning_2026-09-25_b671e309/evidence/read-only-review/TIMING_REPORTING_NOTE.json) · [Prior A1 / corrected V3 / passive viewer](50_SESSIONS/2026-09-25-v3-viewer-intake-4e7b80c2/A1_V3_REANALYSIS_AND_VIEWER_CONTINUATION.md).

The stage-boundary helper flags remain exactly as reported and unpatched; they do not alter the actual release-to-contact interval or its accounting. Contact-force threshold excursions, integrity loss, two microscopic source-1 release/recontact gaps and no repair remain physical observations without added interpretation. No P discovery/perception/learning/regulation, autonomous switching, survival capability, indefinite viability, renewal-supported cyclic sustainability or broad ecological sufficiency is established. No further execution, experiment number, numerical dial, canon, P, Base World or commissioning-sequence change is authorized by this intake. Earlier sections below retain their dated historical dispositions.

## Preserved A1 continuation — completed V3 and passive viewer, 2026-09-25

P engineering: **VERIFIED**  
Commissioning apparatus: **FIT / pre-run engineering CLOSED**  
Coupling commissioning: **IN PROGRESS**  
Scientific/developmental efficacy: **UNTESTED**

First bounded commissioning package:

- **V1 COMPLETE**
- **V2 COMPLETE**
- **V3 COMPLETE**
- **A0 COMPLETE**
- **A1 OBSERVED — one bounded external-control physical witness**

V3 status: **COMPLETED — checks support the reviewed boundary claim.**

Source execution remains the single original A1 under authority `a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc`; P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; apparatus `5f07748102cb5eaa302569c87efbae095050e9fe`. The corrected checker aligned all **9,183 native steps** using the documented initial sensor/display envelope. This is a **NEW READ-ONLY ANALYSIS of the SAME immutable A1 evidence**, not a replay, continuation or replacement trajectory. Original failed V3 artifacts remain preserved and byte-identical.

[Continuation and four-layer evidence record](50_SESSIONS/2026-09-25-v3-viewer-intake-4e7b80c2/A1_V3_REANALYSIS_AND_VIEWER_CONTINUATION.md) · [Original A1 record](50_SESSIONS/2026-09-25-first-a1-evidence-intake-6ad829e4/FIRST_A1_COMMISSIONING_EVIDENCE_RECORD.md) · [Corrected V3 report](90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/V3_READ_ONLY_REANALYSIS_REPORT.md) · [V3 result](90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/V3_RESULT_v1_1.json) · [Passive viewer v1 — entry and opening instructions](90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/README.md) · [Viewer page](90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/index.html).

Validation recorded: **20 V3 checker tests passed; 14 viewer-data checks passed**. The viewer is downstream of saved evidence only: no simulation construction/advancement, commands, simulation RNG, P tuning or raw-evidence modification. The original 91.83 s witness and unobserved 28.17 s remainder are unchanged. No new run, experiment number, scientific efficacy finding, canon/Base World/mechanism or commissioning-sequence change is created. The earlier incomplete post-check below remains a historical record.

## Preserved first A1 intake — before corrected V3 analysis, 2026-09-25

P engineering: **VERIFIED**  
Commissioning apparatus: **FIT / CLOSED FOR PRE-RUN ENGINEERING**  
Coupling commissioning: **IN PROGRESS**  
First physical witness: **A1 OBSERVED — bounded external-control witness**  
V3: **INCOMPLETE — post-analysis checker limitation**  
Scientific/developmental efficacy: **UNTESTED**

**COUPLING COMMISSIONING HAS BEGUN.** P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; apparatus `5f07748102cb5eaa302569c87efbae095050e9fe`. Executed authority: `a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc`.

V1, V2 and A0 completed; exactly one A1 external physical witness executed. It stopped administratively at **91.83 simulated seconds** / **9,183 native rows**, cause `wall_time_limit`, record `complete=True`. No retry, resume or replacement trajectory occurred; the remaining **28.17 s** of the 120 s ceiling is unobserved. V3 post-check is incomplete at the preserved sensor/native-count assertion; it has not been corrected or rerun.

[Evidence record, exact values and claim boundary](50_SESSIONS/2026-09-25-first-a1-evidence-intake-6ad829e4/FIRST_A1_COMMISSIONING_EVIDENCE_RECORD.md) · [A1 report](90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/FIRST_A1_COMMISSIONING_REPORT.md) · [Result package](90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/FIRST_A1_COMMISSIONING_RESULT.zip) · [Untouched launch packet](90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip) · [Exact authority object](90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/APPROVED_OBJECT.canonical.json) · [Jason's authorization source](90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/AUTHORIZATION_SOURCE.txt) · [Preserved V3 limitation](90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/V3_POST_CHECK_LIMITATION.md) · [Pre-run mechanical closure](30_REVIEWS/REVIEW-P-APPARATUS-MECHANICAL-CLOSURE-5f077481-2026-09-25-c84f219a.md).

One external witness reached source-0, established certified contact and received real energy transfer, with both positive-net and negative-net contact-containing windows. This establishes no P discovery, perception, learning, regulation, survival capability or ecological adequacy. Saved labels show 459 complete fixed bins in total, **428 containing contact**; the request's “459 complete contact windows” wording is explicitly qualified in the evidence record.

A2–A5, B1–B4, C1/C2, newborn lives, fixed-structure diagnostic, perceptual commissioning, developmental/scientific trials, efficacy testing, tuning/sweeps and evidential freeze remain unperformed. This is evidence registration only; no continuation, corrected V3 analysis or new execution is authorized. Earlier pre-run and HOLD dispositions below remain historical snapshots.

## Preserved pre-run mechanical closure — 2026-09-25

Exact apparatus checkpoint: `5f07748102cb5eaa302569c87efbae095050e9fe`

Commissioning apparatus: **FIT TO BEGIN AUTHORIZED COUPLING COMMISSIONING**  
P implementation: **unchanged / previously verified**, baseline `6bc9683b54e4fa80136fe8534d7713e2a250a95f`  
P mechanism fidelity: **INDEPENDENTLY VERIFIED within reviewed scope**  
Commissioning execution: **NOT STARTED**  
Scientific status: **UNCOMMISSIONED / UNTESTED**

Known mechanical blockers **A-R1a, A-R1b and A-R1c: CLOSED — VERIFIED** within the final independent review's scope. The original A-R2 clock-comparison defect remains closed for its reviewed boundary class.


[Registered closure and exact checkpoint history](30_REVIEWS/REVIEW-P-APPARATUS-MECHANICAL-CLOSURE-5f077481-2026-09-25-c84f219a.md) · [Complete independent review](90_SOURCES/p_final_mechanical_closure_2026-09-25_c84f219a/LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md) · [Intake and custody](50_SESSIONS/2026-09-25-p-mechanical-closure-intake-c84f219a/INTAKE_RECORD.md).

This is the supplied independent mechanical disposition, conditional on a separate Jason-authorized commissioning task. No execution is authorized by this intake. The 05abf604 and intervening 9d31e790 holds remain checkpoint history; P's earlier engineering branches and scientific limitations remain unchanged. No scientific efficacy, developmental success, survival capability or ecological adequacy has been established.

## Preserved apparatus hold — 05abf604, 2026-09-24

Exact apparatus commit: `05abf60401d08f38750bca589b1c040e10513d7b`

Commissioning apparatus: **ENGINEERING HOLD**  
P implementation: **unchanged / previously verified**  
Commissioning execution: **NOT STARTED**

Blockers:

- **A1** — approval binding does not yet bind complete arm/controller/route.
- **A2** — stage clock comparison may permit one extra 0.1 s command hold.

All other reviewed apparatus findings retain their reviewed status.

Checkpoint scope reaffirmed 2026-09-26: **the commissioning design itself is not marked failed**. This is an apparatus hold for exact 05abf604; later checkpoint closure and execution records retain their own statuses. [Scope confirmation](50_SESSIONS/2026-09-26-05abf604-scope-confirmation-c1857b2a/APPARATUS_REVIEW_SCOPE_CONFIRMATION.md).


[Independent review and retained finding table](30_REVIEWS/REVIEW-P-APPARATUS-INDEPENDENT-05abf604-2026-09-24-b92e45a7.md) · [Original full report](90_SOURCES/p_independent_apparatus_review_2026-09-24_b92e45a7/LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md) · [Intake and custody](50_SESSIONS/2026-09-24-p-independent-apparatus-intake-b92e45a7/INTAKE_RECORD.md).

The review calls the blockers A-R1 and A-R2; A1/A2 above are Jason's requested aliases. P remains at `6bc9683b54e4fa80136fe8534d7713e2a250a95f`, scientifically **UNCOMMISSIONED / UNTESTED**. The earlier apparatus-build “awaiting review” entry below is preserved history. No repair, commissioning execution, tuning or freeze is authorized by this registration.

## Preserved apparatus-build intake — before independent review

Apparatus checkpoint `05abf60401d08f38750bca589b1c040e10513d7b`, parent P baseline `6bc9683b54e4fa80136fe8534d7713e2a250a95f`: **builder reports construction and bounded component verification complete; AWAITING INDEPENDENT REVIEW**. The archived P runtime/configuration remain byte-identical to 6bc9683b. Prior P mechanism fidelity remains independently verified within its reviewed scope; scientific status remains **UNCOMMISSIONED / UNTESTED**. **Commissioning has not begun or been authorized.**

[Intake status and limits](30_REVIEWS/REVIEW-P-APPARATUS-05abf604-2026-09-24-73c9ad61.md) · [Recorded apparatus-construction rulings](40_DECISIONS/DECISION-P-APPARATUS-SCOPE-2026-09-24-73c9ad61.md) · [Original build report](90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/BUILD_REPORT.md) · [Source custody and completion](50_SESSIONS/2026-09-24-p-apparatus-intake-73c9ad61/INTAKE_RECORD.md).

The packaged request accepts the design for apparatus construction with seven scoped rulings, including deterministic privileged control, the sensor-only human reference, the named fixed-structure diagnostic and all-wave D5 analysis. Earlier design drafts below retain their historical proposal wording; the imported ruling controls the narrow construction scope. Component-test results remain builder-reported, not independent apparatus approval. Earlier engineering checkpoints and all candidate designs retain their status and contents. Intake supplies no run, repair, tuning or freeze authority.

## Preserved commissioning design — 2026-09-23 (review draft)

Jason has authorized **design only** for coupling commissioning of exact P checkpoint `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. The [request](90_SOURCES/p_commissioning_design_authority_2026-09-23_2fb3ff84/Pasted%20text.txt) is registered as SRC-061. The engineering disposition remains **FIT TO PROCEED TO COUPLING COMMISSIONING**; scientific status remains **UNCOMMISSIONED / UNTESTED**.

[Technical design](50_SESSIONS/2026-09-23-p-commissioning-design-2fb3ff84/P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md) · [Plain-language walkthrough](50_SESSIONS/2026-09-23-p-commissioning-design-2fb3ff84/P_COMMISSIONING_PLAIN_LANGUAGE_WALKTHROUGH_v0_1.md) · [Proposed matrix](50_SESSIONS/2026-09-23-p-commissioning-design-2fb3ff84/P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md) · [Decisions before execution](50_SESSIONS/2026-09-23-p-commissioning-design-2fb3ff84/DECISIONS_REQUIRED_BEFORE_EXECUTION.md) · [Change rules](50_SESSIONS/2026-09-23-p-commissioning-design-2fb3ff84/P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md) · [Completion and source identities](50_SESSIONS/2026-09-23-p-commissioning-design-2fb3ff84/COMPLETION_REPORT.md).

All commissioning procedures, sample counts, controller choices and budgets are assistant proposals awaiting Jason's review. No commissioning was performed; no apparatus coding, run, configuration change or freeze is authorized by this design request. The proposed extended runner and optional fixed-structure diagnostic require separate authority. The final independent review was already registered; the earlier d5f7efbe/f7eb6f27 engineering holds, source files and decision history remain unchanged.

This is Jason's research authoring workbench. The [direction draft §1](90_SOURCES/direction_2026-09-18/LOOM_DEVELOPMENTAL_DIRECTION_v0_1_REVIEW_DRAFT.md#1-the-intended-organism) describes the first organism's aim as practical accumulated experience: history changes how it meets the present. Rich episodic recall, mature planning and precision robotics are later ambitions. That attribution preserves the draft's status; this map ratifies no mechanism.

## Preserved P engineering clearance — 2026-09-23

Exact checkpoint `6bc9683b54e4fa80136fe8534d7713e2a250a95f`: **FIT TO PROCEED TO COUPLING COMMISSIONING**. Mechanism fidelity **INDEPENDENTLY VERIFIED within reviewed scope**; scientific status **UNCOMMISSIONED / UNTESTED**. R1 closed for the demonstrated radial/oblique release-recontact class; R2 and R3 closed. [Full status and all retained limitations](30_REVIEWS/REVIEW-P-ENGINEERING-6bc9683b-2026-09-23-08df839e.md) · [Engineering-history branches](30_REVIEWS/P_ENGINEERING_HISTORY_2026-09-23-08df839e.md).

No scientific efficacy, developmental success, survival capability or ecological adequacy has yet been established. Commissioning remains a separate Jason-authorized task. The earlier checkpoint holds retain their exact historical status.

## Preserved engineering-history branch — f7eb6f27

Checkpoint `f7eb6f27c661e3db193a4225b56a825d7e41739d`: **ENGINEERING HOLD**. R1 original fixture closed; R1-P oblique release/recontact class open; R2 and R3 verified closed. P mechanism fidelity unchanged / previously verified. Scientific status uncommissioned / untested. [Exact status and review](30_REVIEWS/REVIEW-P-ENGINEERING-f7eb6f27-2026-09-23-1677619b.md) · [Intake record](50_SESSIONS/2026-09-23-p-post-correction-intake-1677619b/INTAKE_RECORD.md).

This later engineering record supersedes the specification-stage work-status wording below for this checkpoint only. Earlier decisions, source documents and reviews remain preserved. This intake authorizes no repair or execution.

## Foundation and direction

Start with [00_LOOM_CURRENT_STATE.md](90_SOURCES/reference_7ada2b300fa1/00_LOOM_CURRENT_STATE.md), then [Design Frame v0.2](90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/DEVELOPMENTAL_ECOLOGY_DESIGN_FRAME_v0_2.md), [coupling specification with its Base World reading note](90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1.md), [Base World Completion](90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/BASE_WORLD_COMPLETION_v0_1.md), and [decision ledger v0.2](90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/DEVELOPMENTAL_ECOLOGY_DECISION_LEDGER_v0_2.md). Their original identities are associated with `7ada2b300fa12a26b0daf40b1fa5682243ff6625`, not a check of current remote main. The source catalog records later authorised MathJax formatting; [current and original identities](50_SESSIONS/2026-09-20-p-specification-83a00674/SOURCE_IDENTITIES.json) are distinguished. Accepted world/body choices retain their scope. P is selected for specification under the scoped decision below; numerical completions await review.

The later [direction draft](90_SOURCES/direction_2026-09-18/LOOM_DEVELOPMENTAL_DIRECTION_v0_1_REVIEW_DRAFT.md) and [source/continuation audit](90_SOURCES/direction_2026-09-18/LOOM_SOURCE_AND_CONTINUATION_AUDIT_v0_1_DRAFT.md) preserve discussion with mixed, individually attributed statuses. They do not override accepted doctrine by being newer. [Decisions and authority](40_DECISIONS/DECISION_INDEX.md) locates the accepted reference and pending rulings.

## Available complete candidates

| Candidate | Proposed interaction | Authority | Work | Evidence |
|---|---|---|---|---|
| [P](20_CANDIDATES/CAND-P.md) | Fast sensory query participation plus slow retention | selected for specification; exact external A1–A4 packages authorized | coupling commissioning in progress; V1/V2/V3/A0 complete; A5 not executed, new packet required | A1–A4 observed under original apparatus; A5 clock correction verified, old authority held/non-launchable; learning/developmental efficacy untested |
| [R](20_CANDIDATES/CAND-R.md) | Direct sensory return through retention; fast motor/regulatory effects remain | preserved alternative; unselected for this specification | available | untested |

Both complete designs remain preserved. Jason has [selected intact P first for specification and permitted its bounded bodily-learning scaffold](40_DECISIONS/DECISION-P-SPECIFICATION-2026-09-20-83a00674.md). R remains available and unselected for this specification; no merged design or compulsory comparison is created. The earlier [comparison](30_REVIEWS/REVIEW-P-R.md) remains assistant analysis; selection comes from Jason's later explicit ruling.

Read the new [P implementation and observation specification](50_SESSIONS/2026-09-20-p-specification-83a00674/P_IMPLEMENTATION_AND_OBSERVATION_SPEC_v0_1_REVIEW_DRAFT.md) and [plain-language data flow](50_SESSIONS/2026-09-20-p-specification-83a00674/P_PLAIN_LANGUAGE_DATA_FLOW_v0_1_REVIEW_DRAFT.md). Both are assistant review drafts with proposed numerical/engineering completions, not authorisation to build. The [completion report](50_SESSIONS/2026-09-20-p-specification-83a00674/COMPLETION_REPORT.md) records source identities, checks and remaining review choices.

[Open questions](02_OPEN_QUESTIONS.md) covers participation versus retention, common activity versus fine differentiation, sustained-input availability, packet/gain compatibility, reciprocal maps, bodily interaction, and useful sensory/associative learning. Its order is navigation, not an experimental sequence.

Two small idea notes retain [participation–retention](10_IDEAS/IDEA-PARTICIPATION-RETENTION.md) and [conditional restraint without erasure](10_IDEAS/IDEA-RESTRAINT-WITHOUT-ERASURE.md). The [independent-report index](20_CANDIDATES/RESEARCH_REPORT_INDEX.md) keeps other candidate families available; newer P/R proposals do not reject them.

## Sources and continuation

- [Source register](SOURCE_REGISTER.md), [exact catalog](SOURCE_CATALOG.json), and [coverage/provenance](SETUP_PROVENANCE.md).
- [Workspace status and recovery](01_WORKSPACE_STATUS.md).
- [Session and contribution workflow](50_SESSIONS/README.md), [setup report](50_SESSIONS/2026-09-20-setup-3ea17017/SETUP_REPORT.md), and [templates](80_TEMPLATES/SESSION.md).

The full primary-chat export audit is pending. The earlier user-notes `Pasted text.txt` is missing; the packaged namesake is P's assistant response. Missing material does not block design navigation. No mechanism build, experiment number, preregistration, commissioning or scientific run is authorized.
