# B1 operator correction — independent provenance and static compatibility

**No custody, causal-source-preservation or static-compatibility blocker found in this assigned narrow scope.** This subreview supports the combined independent review; it grants no execution authority. No prepared positive control or B1 case was executed, no Engine/Run was constructed, no controller command was evaluated, and no held snapshot was decompressed or deserialized.

## Package and checkpoint

| Check | Independently verified result | Receipt |
|---|---|---|
| Latest review-02 ZIP | `0166f1395e9f10fba96e05f5d53264ba2fc275db2122087810406107e3ccf318`; 27,546,035 bytes; 2,677 entries; all 2,676 payload hashes and ZIP CRC pass. Declared payload bytes: 31,245,458. Safe paths and duplicate/case-collision checks pass. | `ZIP.json` |
| Exact patch | `git diff --binary --full-index 68db2c58... 352f73ff... --` exactly matches the delivered 132,681-byte patch, SHA-256 `2191f1058eb817f84ea8fb674388bfae4eb23b470b3b8887f1f882465b1a3ed1`. Twenty-four files: 1,470 insertions, 73 deletions. | `GIT.json` |
| History | `352f73fffa6d9781eae8aa38e708a9a05669588f` directly descends from `68db2c581f07200966d699a4f55a65f9b96df1e9`. P `6bc9683b54e4fa80136fe8534d7713e2a250a95f` remains an ancestor. Both actual worktrees remain clean at their intended checkpoints. | `GIT.json`, `FINAL_PRESERVATION.json` |
| Experimental archive | `EXP1-21` tree remains `f1b884a7ada4c806786d1530d76d446aac5d37b1` at P, parent and corrected checkpoint. | `GIT.json` |
| Portable/actual source | All 72 current-source files and 69 baseline files match their actual worktrees. All corrected apparatus Python files match their committed Git blobs exactly. | `SOURCE_MATCH.json`, `GIT.json` |
| Held custody | All 124 files/archives match the pre-correction hash inventory, whose own SHA-256 is checked against the committed final-preservation receipt. Custody object hash remains `45d71cd121f823368401b11c4a1010d509af3224f49168ad528653274d0e7543`. | `HELD_PRESERVATION.json`, `STATIC_COMPATIBILITY.json` |
| Public references | All 28 listed original public source files match their recorded identities. | `PUBLIC_SOURCE_IDENTITIES.json` |
| Final rehash | After the root regression-complete signal, all 3,064 deduplicated source/evidence paths rehash unchanged. This includes the 124 held files and 115 historical A5 files discussed below. | `BEFORE_FILE_IDENTITIES.json`, `FINAL_PRESERVATION.json` |

The original latest ZIP is `exports/2026-09-26-B1-operator-correction-352f73ff-review-02/B1_OPERATOR_APPARATUS_CORRECTION_REVIEW.zip`. Its manifest SHA-256 is `e38cdb730db72fd3addd9c86b1878249631d9ce39326d6a6e0c69e97fe478c58`.

Extraction removed only the common `B1_OPERATOR_APPARATUS_CORRECTION_REVIEW/` wrapper to shorten Windows paths. The exact independent suite root is `../portable/source/developmental_ecology`. `WINDOWS_REVIEW_NOTE.md` was read; the earlier packaging path-length issue is not represented as a code regression.

## Why the two deliveries differ in size

The earlier ZIP is 457,395,677 bytes with verified file hash `4bc28da9927b29c75310a8ab56e73ccb45460b58d5e217074dac8632a1c4fc0d`. Its manifest identity also matches its receipt. The review-02 manifest has 2,676 common payload paths and no additions. All common entries retain identical identities except `task-utilities/package_review.py`.

The only 115 removed paths are generated historical A5 files accidentally included under the earlier baseline copy. The packaging-utility diff changes that baseline copy to committed source plus the existing component cache. The corrected source, baseline source, tests, reports and component evidence are unchanged. All **141 actual source/baseline payloads read from the earlier ZIP** equal the latest ZIP's extracted bytes. The omitted 115 files still match the earlier archive's inventory at their original parent-worktree locations; no historical result was deleted or rewritten.

`DELIVERY_COMPARISON.json` records the complete manifest comparison. `OMITTED_HISTORICAL_A5_PRESERVATION.json` records the 115 current-file hash checks. The earlier archive was not expanded wholesale, and this review does not claim a fresh CRC/decompression check of every earlier non-source payload. The complete latest archive was verified.

## Causal preservation and current identities

Nineteen protected files are byte-identical across parent worktree, corrected worktree and both portable trees: 13 P modules, configuration, requirements, clock, physical adapter, diagnostics and evaluation. Git confirms P/configuration/requirements/P tests are unchanged from P, and clock/adapter/diagnostics/evaluation/initialization are unchanged from 68db. None of the 176 pre-existing test cases' files changed; the correction adds the B1 test module and DOM fixture.

`CAUSAL_AST.json` independently compares `command_pair`, `waypoint_command`, `waypoint_stage`, `time_due`, `validate_plan`, `privileged_input`, and `observe_without_interference`: all AST-identical. The complete controller gain dictionary is unchanged. Thus actuator bounds, command arithmetic, native scheduling, P sensory computation, physical chemistry, event/world integration and their cadence source are preserved. The new presentation and interactive lifecycle plumbing are separately examined by the root and interface/lifecycle reviewers. No new ecological behavior or long-horizon performance claim is inferred from source equality.

`CURRENT_IDENTITIES.json` independently computes:

- Apparatus aggregate: `1ef4264e937d7501a32cd06ab76393304916c763a99d834915b8c5d06e6ac703`.
- P aggregate: `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`.
- Semantic configuration: `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`.
- Configuration checkout bytes: `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9`.
- Python 3.13.5, NumPy 2.3.3, SciPy 1.16.2 and their full recorded runtime content identities match the builder's runtime receipt. Node v22.16.0 has executable hash `c5ff4c736112dd483c750fd4149d30c8a116db1a49b8b3ec88be4b65e6c86c19`. All six recorded test-package versions match. No dependency was installed.

## Held cases: static compatibility only

The public case/authority index and display/recording contracts were read. The six private **case manifests** were compared programmatically in memory solely for structural equality and safe contract checks; no private values were emitted and no manifests were copied into this review. All snapshots remained opaque compressed bytes. No geometry, body state, field values or evaluator content was opened for model inspection.

| Held case | Horizon | Native steps | Ten-step holds | Static result |
|---|---:|---:|---:|---|
| PC-LR | 4 s | 400 | 40 | Representable; original snapshot hash matches |
| PC-MOTION | 4 s | 400 | 40 | Representable; original snapshot hash matches |
| PC-CONTACT | 6 s | 600 | 60 | Representable; original snapshot hash matches |
| PC-HOLD | 10 s | 1,000 | 100 | Representable; original snapshot hash matches |
| B1-FULL-RAW | 30 s | 3,000 | 300 | Representable; original snapshot hash matches |
| B1-CHEMISTRY-HIDDEN | 30 s | 3,000 | 300 | Representable; same original snapshot hash |

The pair has exactly these differing top-level keys: `case_id` and `execution`. Within `execution`, only `display_intervention` differs. Complete initial-state identity, world-law/configuration identities, duration, physical initialization and all other manifest fields are identical. Every held case still has a null execution grant. No candidate execution object or grant was constructed in this review.

The unchanged pure native-clock helpers accept each existing horizon and every declared ten-step hold. The corrected display validator accepts the corresponding display identity. The four controls' information requirements remain expressible: light/chemistry for left/right distinction; seven proprioception coordinates and own-command history for command versus movement; all eight contact coordinates for onset and gentle holding. The hidden view omits only indices 10–13, retaining the original order of the other 25 coordinates; full view retains all 29. Source review preserves complete private/raw recording. The root's separate manufactured-pair test supplies dynamic equality evidence; none of these static checks is a positive-control demonstration or B1 trial.

`STATIC_COMPATIBILITY.json` contains only public IDs/horizons, opaque identities and comparison booleans. It does not contain sealed manifest/state values. The held packet remains an old, non-launchable custody object and would require separately authorized regeneration against the new apparatus identity.

## Secrecy and execution limits

`SEALED_PAYLOAD_EXCLUSION_GUARD.json` provides 39 exact forbidden payload/archive hashes from held private content, excluding public reference source. The complete latest review package contains none of those bytes. The final intake packager should apply the same hash guard and exclude private-state directory components. No sealed manifest, snapshot, authoring geometry or privileged held archive is copied by this subreview.

A bounded census found 153 delivered component-record manifests, all labeled manufactured fixtures; zero commissioning manifests in that census. Combined with preserved null-grant held metadata, this supports the declared component-only evidence. It is not a universal assertion about unrecorded external files or processes. No new authority, positive control, B1 execution or evaluator disclosure occurred in this subreview.

The root independently ran the worktree and portable 204-case suites and all twelve A–L RED/GREEN pairs. Their actual logs and assertion-level results belong to the combined report; they were not rerun here. No general adversarial, scientific, efficacy, competence, throughput or unrelated security audit was performed.

## Reproduction

From the project workspace in PowerShell, the exact subreview commands were:

```powershell
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-26-b1-review-352f73ff\provenance\extract_package.py'
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-26-b1-review-352f73ff\provenance\audit_provenance.py'
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-26-b1-review-352f73ff\provenance\static_compatibility.py'
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-26-b1-review-352f73ff\provenance\final_rehash.py'
```

The extraction script deliberately refuses an existing destination; reproduce into a fresh review directory. All write destinations are this new review export. Git commands use absolute roots, process-scoped `safe.directory` and empty excludes, plus `GIT_OPTIONAL_LOCKS=0`; no Git configuration is persisted. Builder preparation, static-regeneration, packaging and commit utilities were read as source only and not executed. Target worktrees, old exports, held evidence, Workbench and canon remain read-only.
