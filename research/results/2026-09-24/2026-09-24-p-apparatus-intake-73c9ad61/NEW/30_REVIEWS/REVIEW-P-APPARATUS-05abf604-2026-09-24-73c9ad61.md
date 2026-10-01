# P commissioning apparatus — build intake, awaiting independent review

**Intake date:** 2026-09-24  
**Apparatus checkpoint:** `05abf60401d08f38750bca589b1c040e10513d7b`  
**Parent / unchanged P baseline:** `6bc9683b54e4fa80136fe8534d7713e2a250a95f`  
**Apparatus status:** BUILDER REPORTS CONSTRUCTION AND BOUNDED COMPONENT VERIFICATION COMPLETE — AWAITING INDEPENDENT REVIEW  
**Commissioning:** NOT BEGUN / NOT AUTHORIZED  
**Scientific status:** UNCOMMISSIONED / UNTESTED

This is an intake and custody record, not a new independent code/fidelity review. The supplied [build report](../90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/BUILD_REPORT.md) explicitly stops at apparatus review. The archive's name contains “Review”; it is a package **for** independent review, not an independent review verdict. The exact checkpoint is declared in [CHECKPOINT.json](../90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/CHECKPOINT.json); no local or remote Git checkout was inspected in this intake.

## What arrived

A separate commissioning package around the unchanged P runtime: extended bounded runner; deterministic privileged waypoint/wait/contact controller; sensor-only human interface; **FIXED-STRUCTURE / NO-LASTING-PLASTICITY DIAGNOSTIC**; aligned passive diagnostics and receiver analysis; AV/CO/SO interpretation separation; validators and manufactured fault fixtures. The [walkthrough](../90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/PLAIN_LANGUAGE_WALKTHROUGH.md), [information-flow map](../90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/AUTHORITY_AND_INFORMATION_FLOW.md) and [law/code/test map](../90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/LAW_CODE_TEST_MAP.md) explain the intended boundaries.

The packaged [user build request](../90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/APPARATUS_BUILD_REQUEST.txt) records seven scoped rulings. [Their attributed authority record](../40_DECISIONS/DECISION-P-APPARATUS-SCOPE-2026-09-24-73c9ad61.md) preserves those rulings without rewriting the original design. In particular, D5 now uses every practical wave handoff and a predetermined native selection rule, replacing the draft's at-most-100-samples proposal for apparatus construction. Birth IDs 1–4 and 600 s ceilings remain prospective metadata, not permission to start lives.

## Builder-reported evidence, checked as records only

| Reported item | Supplied record and limit |
|---|---|
| 83 tests passed in the worktree, 34.18 s | 24 apparatus checks plus 59 unchanged P checks; final test log is inside the original ZIP |
| 83 tests passed from the assembled portable package, 58.63 s | Separate portable log; not a fresh dependency or cross-platform validation |
| 16 intended RED→GREEN fault pairs | [Fault matrix](../90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/FAULT_MATRIX.json) and individual logs; all 16 matrix pairs and their fail/pass log summaries are present and internally consistent |
| Short manufactured components and restart/replay checks | [Execution ledger](../90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/EXECUTION_LEDGER.md); typically 0.2 s, controller checks 0.1 s, plus manufactured time/reserve boundaries. A step at clock 1,199.99 is not a 1,200 s life |
| Fixed-structure timing and discarded-update poisoning | Reported component evidence, including late bank restoration detection; not an innate-maintenance or learning outcome |
| Sensor display inspection | [UI record](../90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/UI_REVIEW.json); recorded 0.100/0.200 s E/I holding behavior, disabled saved-view controls. Native double-click launch not automated; direct file navigation was blocked in the build review |

This session only read/hash-checked packaged records. It did not execute tests, replay worlds, open launchers, serve a UI or run a controller. Earlier failed development/setup logs remain inside the unchanged archive; they are not substituted for intended-fault RED evidence.

## What this intake verified directly

The incoming ZIP is 5,790,938 bytes with SHA-256 `87f4dbde39a72559caf6045c7ac68a649d9691a000d1569af5d26b090a63b053`. All **220 payload entries** matched the delivered manifest in byte length and SHA-256; the archive contains 221 members including the manifest. Its CRC check passed. There is no supplied external checksum sidecar to compare; the outer digest is the intake's custody measurement.

All 13 packaged P runtime files and the configuration match the retained exact 6bc9683b reading copies byte-for-byte. All apparatus file hashes and the patch hash match CHECKPOINT.json. The five design documents and the original design ZIP match this workbench's prior contribution. These identity checks establish continuity of the archived bytes, not proof of the apparatus's behavior or verification of the declared Git commit from a repository.

Detailed identities and checks: [SOURCE_IDENTITIES.json](../50_SESSIONS/2026-09-24-p-apparatus-intake-73c9ad61/SOURCE_IDENTITIES.json) and [VALIDATION.json](../50_SESSIONS/2026-09-24-p-apparatus-intake-73c9ad61/VALIDATION.json). Existing P fidelity remains **INDEPENDENTLY VERIFIED within its previously reviewed scope**. The apparatus has no new independent approval from this intake.

## Remaining scope and limitations

No A1–A5, B1–B4, C1 or C2 commissioning outcome is supplied. The builder explicitly leaves controller navigation/recovery competence, human sensory positive controls, blinded/deprivation cases, new birth-specific field histories, 600 s lives, sustained periodic snapshots and long-run cost untested. No ecological sufficiency, survival capability, innate-maintenance result, useful development or scientific efficacy follows from these component checks.

The [updated resource estimate](../90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/RUNTIME_STORAGE_ESTIMATE.json) gives a provisional envelope of about **37.74 machine-hours and 43.02 GB stored**, or 86.04 GB with one duplicate, for the previously proposed 8,960 s workload. This extrapolates 0.2 s components with substantial restart/diagnostic overhead; it is neither a measured lifetime rate nor an approved budget. The earlier 11.67 h / 17.66 GB estimate remains preserved with its different basis.

The 6bc9683b baseline retains all seven prior limitations, including provisional sensory capacity, lossy/adapting sensory representation, contracting association, unknown effective learned magnitudes, shared equal E/I configuration fields and finite-step contact limits. Earlier d5f7efbe and f7eb6f27 engineering holds retain their original statuses. R and all alternative designs remain unchanged.

The next boundary is **independent apparatus review**. Accepting or ingesting this ZIP does not authorize commissioning, further fixtures, apparatus repairs, parameter changes, an evidential freeze or Stage 1. Source instructions and launch commands are preserved as historical data. No work in the actual Loom repository or enclosing vault repository was performed.
