# First A1 continuation — V3 reanalysis and passive viewer

**Registered:** 2026-09-25 under Jason's explicit continuation instruction. Continues the [existing first-commissioning record](../../50_SESSIONS/2026-09-25-first-a1-evidence-intake-6ad829e4/FIRST_A1_COMMISSIONING_EVIDENCE_RECORD.md); no new commissioning run or experiment number is created.

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

Source execution authority remains `a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc`. P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; apparatus remains `5f07748102cb5eaa302569c87efbae095050e9fe`. The original A1 ZIP remains SHA-256 `f37dfec92288fbe8a650b00eed611d086a3ece3b280292e95b891e371cc0d37f`.

## Four distinct records

| Layer | Preserved identity and relationship |
|---|---|
| Original A1 trajectory evidence | [Original result ZIP](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/FIRST_A1_COMMISSIONING_RESULT.zip), one 91.83 s external-control witness, 9,183 native rows, administrative wall-limit stop; no retry/resume/replacement. The 28.17 s remainder remains unobserved. |
| Original failed V3 post-check | [Original checker](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/read_results.py), [AssertionError](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/V3_BOUNDARY_ERROR.json), [count finding](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/V3_COUNT_FINDING.json), [limitation](../../90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/evidence/read-only-review/V3_POST_CHECK_LIMITATION.md). These remain byte-identical, including their historical incomplete disposition. |
| Corrected read-only V3 reanalysis | [New report](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/V3_READ_ONLY_REANALYSIS_REPORT.md), [version 1.1.0 result](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/V3_RESULT_v1_1.json), [versioned checker source](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/v3_checker_v1_1.py). A NEW READ-ONLY ANALYSIS of the SAME immutable A1 evidence; supersedes the live incomplete V3 conclusion only. |
| Derived passive viewer | **A1 passive read-only plan-view viewer v1**: [viewer entry and opening instructions](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/README.md), [viewer page](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/index.html), [saved visual verification](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/STATIC_VIEWER_VALIDATION.html). A downstream display of recorded evidence, not a simulation or additional result. |

## Completed V3 claim and validation

The corrected checker validates the contents of the documented initial sensor/display envelope and aligns all **9,183 native steps** with their sensor and diagnostic endpoint records. There are **9,184 sensor entries = one validated initial envelope + 9,183 endpoint rows**. The source report distinguishes start/endpoint raw values, held E/I timestamps, controller decision ownership and final record continuity; it does not simply discard an unexplained first row.

The supplied result reports 919 closed-schema controller inputs, 9,183 issued/delivered command comparisons, 459 body handoff samples, complete inactive-organism/RNG agreement at all 11 saved checkpoints and native RNG-counter agreement at all 9,183 endpoints. Neural wave rows remain zero. The final issued hold supplied three recorded steps and retained seven unexecuted steps; no continuation is implied.

Recorded validation:

- **20 V3 checker tests passed** — [original test result record](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/V3_TEST_RESULTS.json).
- **14 viewer-data checks passed** — [original viewer-data check record](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/VIEWER_DATA_TEST_RESULTS.json).

These are supplied analysis/display validation results, not new commissioning cases or tests rerun during intake. The reviewed boundary claim is evidence-level and remains limited by available records: full neural/RNG state is available at 11 saved checkpoints, while counters are available at every native endpoint. It does not claim observation of arbitrary unlogged transient memory states.

## Passive viewer scope

The [data-flow document](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/VIEWER_DATA_FLOW.md) specifies extraction from the existing archive into display data, then browser rendering. The viewer does not instantiate or advance the simulation, issue commands, consume simulation RNG, tune P or modify raw evidence. Playback changes the selected saved record only. This is not a replay, continuation or replacement trajectory.

The [viewer verification report](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/VIEWER_VERIFICATION.md) retains the display's limits: mover pose holds the latest recorded 0.1 s controller-geometry sample and shows sample age; exact event pose/reserves and native sensor/velocity/actuator values retain their separate timestamps. It does not interpolate physical samples or invent unrecorded mover motion. All original windows and the partial tail remain available; no learning/developmental animation is implied.

The supplied [local viewer launcher](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/OPEN_A1_VIEWER.cmd) and all dependencies are preserved together. The packaged instructions describe its loopback read-only preview. No launcher, server, viewer, checker, test, extractor or reproduction command was executed during this intake. Prior reported browser verification is attributed to the supplied verification report.

## Authority, continuity and scientific boundary

Jason's current instruction authorizes registration and live status/navigation updates. The archived A1 approval belongs to the single original trajectory; neither this continuation nor the passive viewer grants new execution authority. This task proposes no mechanism, configuration, Base World, accepted architecture, canon or sequence change.

V1/V2/A0 and the bounded A1 observation retain their prior dispositions. The original failure remains a historical analysis result; the corrected analysis closes only the intended V3 record comparisons. The original force/integrity observations, positive/negative energetic windows, 91.83 s stop and source-accounting evidence are unchanged. The earlier window wording qualification remains: 459 complete fixed bins in total, 428 containing contact (229 positive-net, 199 negative-net), 31 without contact and one separate partial tail.

No A2–A5, B1–B4, C1/C2, newborn life, fixed-structure diagnostic, perceptual commissioning, developmental/scientific trial, efficacy testing, tuning/sweep or evidential freeze is added. One external physical witness and completed record-boundary checks establish no P discovery, perception, learning, regulation, survival or ecological adequacy. Scientific/developmental efficacy remains **UNTESTED**. Original candidate alternatives and all earlier checkpoint histories remain unchanged.

## Intake verification

The derived ZIP matches its external delivery receipt. All **53 payload files** and CRCs verify; all 54 extracted members match the supplied unpacked directory. The embedded original A1 ZIP is byte-identical to the already registered original. All five historical V3/summary reference copies match both that ZIP and the previously registered source files. HASH_BEFORE and HASH_AFTER match exactly; the versioned checker, tests and viewer-data identities match their supplied result records. The 20/14 counts are present in those preserved records.

This verifies custody and registration consistency, not an independent rerun of V3 or a fresh viewer audit. No source-identity/status conflict was found. [Supplied custody proof](../../90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2/A1_READ_ONLY_REANALYSIS_VIEWER_v1/CUSTODY_PROOF.json) · [Intake completion](INTAKE_RECORD.md) · [Source identities](SOURCE_IDENTITIES.json) · [Final validation](VALIDATION.json).
