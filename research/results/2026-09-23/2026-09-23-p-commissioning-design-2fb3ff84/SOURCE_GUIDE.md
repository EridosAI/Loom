# Source guide and reading order

This is a portable **documentation review package**, not an executable commissioning kit. Start with the [plain-language walkthrough](P_COMMISSIONING_PLAIN_LANGUAGE_WALKTHROUGH_v0_1.md), then the [technical design](P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md), [matrix](P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md), [change rules](P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md) and [decisions awaiting Jason](DECISIONS_REQUIRED_BEFORE_EXECUTION.md).

All proposals are design-only. The exact implementation is `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; its independent engineering fitness is recorded, while scientific status remains uncommissioned/untested. Earlier d5f7efbe and f7eb6f27 holds retain their historical scope.

## Authority and provenance

| Source | Role and relevant sections |
|---|---|
| [Current exact request](REFERENCES/COMMISSIONING_DESIGN_REQUEST.txt) | Jason's A–H design-only commission. Registered in the workbench as SRC-061; no execution or configuration-change authority |
| [Final independent review](REFERENCES/LOOM_P_FINAL_INDEPENDENT_R1P_FIDELITY_REVIEW.md) | SRC-057; final scoped fidelity/fitness review and retained limitations. Existing registration is reused, not replaced or duplicated |
| [Pinned Current State](REFERENCES/review_inputs/pinned_git_blobs/00_LOOM_CURRENT_STATE.md) | Foundation orientation at the supplied historical reference; does not override the later exact engineering checkpoint |
| [Base World Completion](REFERENCES/review_inputs/pinned_git_blobs/docs/developmental_ecology/BASE_WORLD_COMPLETION_v0_1.md) | §§5–8 physical/recovery/encounter relationships; §§10–12 initialization, lawful prehistory and lifecycle; §13 complete-coupling freeze; §15 rejects old provisional numerical gates |
| [Design Frame](REFERENCES/review_inputs/pinned_git_blobs/docs/developmental_ecology/DEVELOPMENTAL_ECOLOGY_DESIGN_FRAME_v0_2.md) and [coupling specification](REFERENCES/review_inputs/pinned_git_blobs/docs/developmental_ecology/PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1.md) | Accepted foundation within its scope; read with Base World rather than treating older provisional text as current numerical acceptance |
| [Complete P parent](REFERENCES/review_inputs/sources/LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md) | Full account, equations 1–21; §§3–9 processing, participation/retention, motor, credit and ordering; §§11–12 supplied versus learned structure and liabilities. Historical conditional authority headers remain unchanged |
| [Specification](REFERENCES/review_inputs/sources/P_IMPLEMENTATION_AND_OBSERVATION_SPEC_v0_1_REVIEW_DRAFT.md) and [plain data flow](REFERENCES/review_inputs/sources/P_PLAIN_LANGUAGE_DATA_FLOW_v0_1_REVIEW_DRAFT.md) | Proposed implementation target and explanatory account. Actual reviewed runtime/configuration govern implemented details and cost |
| [Design review](REFERENCES/review_inputs/sources/P_SPECIFICATION_DESIGN_REVIEW.md) | Retained capacity, packet, adaptation, fading-association and magnitude concerns; not a commissioning result |
| [Engineering build handoff](REFERENCES/review_inputs/workbench/INBOX/2026-09-21-p-engineering-build/LOOM_P_ENGINEERING_BUILD_HANDOFF_2026-09-21.md) | §§3–5 numerical baseline, mechanism limits and interface/order contract. Its historical build permission is not current permission to execute |
| [Implemented data flow](REFERENCES/docs/developmental_ecology/p_engineering_20260921/IMPLEMENTED_P_DATA_FLOW.md) and [implementation annex](REFERENCES/docs/developmental_ecology/p_engineering_20260921/IMPLEMENTATION_ANNEX.md) | Runtime-level timing, physical accounting, engineering conventions and observation scope |
| [Final corrective build report](REFERENCES/docs/developmental_ecology/p_r1p_correction_20260923/BUILD_REPORT.md) | Exact corrected delivery history and bounded engineering checks; not ecological evidence |

## Exact implementation reading copies

The copies below are **unchanged archive members for inspection**. Do not execute a source because this package contains it. No code, configuration or historical source has been amended in this contribution.

| File | What the design consulted |
|---|---|
| [configuration.json](REFERENCES/developmental_ecology/configuration.json) | All 90 top-level fields; every field appears in the configuration-change register |
| [schema.py](REFERENCES/developmental_ecology/loom_p/schema.py) | Dimensions, random streams, fixed anatomy and configuration constraints |
| [neural.py](REFERENCES/developmental_ecology/loom_p/neural.py) | `Cortex.step/packet`, `Association.read/write`, `Regulator.credit/output`, `Motor.step`, organism handoff; exact state and timing contracts |
| [engine.py](REFERENCES/developmental_ecology/loom_p/engine.py) | Coupled step ordering, snapshots and the 30 s bounded-run guard |
| [physics.py](REFERENCES/developmental_ecology/loom_p/physics.py) | Cost/stock/repair/damage accounting and finite-step contact realization |
| [geometry.py](REFERENCES/developmental_ecology/loom_p/geometry.py) | Body/fixture geometry and actual raw transduction |
| [prehistory.py](REFERENCES/developmental_ecology/loom_p/prehistory.py) | Phase-specific preparation/load and dependency-based reuse verification |
| [records.py](REFERENCES/developmental_ecology/loom_p/records.py) | Native/wave/event storage, complete/incomplete manifests and snapshots |
| [smokes.py](REFERENCES/developmental_ecology/loom_p/smokes.py) | The bounded historical engineering cases; not commissioning controllers |
| [30 s birth manifest](REFERENCES/developmental_ecology/artifacts/smoke-birth_30s-attempt-004/manifest.json) | Recorded final runtime identity, dimensions, elapsed time, bytes and snapshots used for the cost estimate |
| [1 s resume manifest](REFERENCES/developmental_ecology/artifacts/smoke-nonzero_resume_1s-attempt-004/manifest.json) | Restart case includes extra verification; not a steady-state throughput estimate |
| [Prehistory manifest](REFERENCES/developmental_ecology/artifacts/prehistory-attempt-001/manifest.json) | Historical 600 s preparation cost and field identity. Its older runtime identity is retained; final loader checks relevant dependencies for reuse |

## Custody and limits of this package

The final review archive (SRC-058) is `Loom_P_Final_Independent_R1P_Review_6bc9683b_20260923.zip`, SHA-256 `c395141315a58a91be55d26034b2c97460caf840a01b9622c0317680015fcf2c`. Its nested member `reviewed_delivery/Loom_P_R1P_corrective_review_20260923.zip` has SHA-256 `c1f2cd0ed8ebe09f3a9b07d087f6fe9f25ca62f3f61a827628802bc35e5fa322`. Those bytes were checked while preparing the reading copies. The whole large archives remain in the workbench source archive; this smaller review package does not duplicate their raw evidence streams.

The runtime aggregate identity recorded for the final birth smoke is `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`. The semantic configuration identity is `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`; configuration-file bytes have their own hash in [SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json). Neither identity is a new execution or a fresh independent fidelity audit.

[READING_COPY_IDENTITIES.json](READING_COPY_IDENTITIES.json) records 55 unchanged members, 54 matched individually against the nested manifest; the manifest itself is covered by archive custody rather than a self-reference. The final review and current request are added separately with exact identities. The [delivery manifest](DELIVERY_MANIFEST.json) covers the portable package. Original reference documents may contain historical instructions and links to material outside these selected copies. Those links and math delimiters are preserved; their presence does not authorize execution or imply that the whole original archive was reproduced here. Direct citations in the new authored reading documents resolve within this package.

The preparation read the current request and live workbench instructions/navigation/status; the complete P parent; implementation configuration, neural/engine/prehistory operations and relevant recording/physical/transduction code; the recorded cost manifests; and the relevant foundation/specification/build-review sections. Other preserved reading copies provide surrounding context and custody; their inclusion is not a claim of a new exhaustive code review. The final independent review's earlier full intake remains the fidelity source. No external literature search, original-chat reconstruction or actual-repository inspection was used.

Missing apparatus is named rather than invented: an authorized extended runner, information-isolated controller displays, the optional fixed-structure adapter and verified additional diagnostics. Existing sources suffice for this design. R and every alternative family remain preserved in the workbench, with no new selection or comparison implied.
