# Independent corrected-checkpoint provenance and saved-evidence review

This is a scoped contribution to the single independent post-correction review. Reviewed `f7eb6f27c661e3db193a4225b56a825d7e41739d` against `d5f7efbe67193f215e52d95ca912db131a79f31c`. No target/Workbench changes, new freely acting lives, prehistory generation, inspector server, or live inspector stepping were performed. Evidence files beside this document were newly authored in the review workspace only.

## VERIFIED — identities and preservation

- New commit is the direct single-parent child of the previous reviewed commit on `build/p-engineering-baseline-20260921-01a0c405`. The previous commit remains reachable. Both contain historical `EXP1-21` tree `f1b884a7ada4c806786d1530d76d446aac5d37b1`. Previous build documents have no Git delta.
- All 252 entries in the builder's before-correction inventory retain their recorded lengths/hashes. Independently, all 87 entries in the previous build's evidence manifest still match. During this review, all 474 target artifact files were hashed before/after and remained identical, with no added artifact files.
- Corrected ZIP: 83,421,895 bytes; SHA-256 `7e33da1b05646c5af352a4114e99082c52b51b2b5966911f30816fb2911091da`. All 152 inventory entries match and exactly account for 153 members including the inventory. There are no duplicate member names. Every attempt-003 trace/snapshot is included, including the complete birth traces.
- Packaged `CORRECTION.patch` exactly equals the scoped binary Git diff from old to new commit. Patch SHA-256: `de8fd97320af569df91d629183a61649e8ae16c082c4fcc6610fc78c472c1a21`.
- All 51 tracked package files match working/package bytes and committed content. The sole byte variation against Git is ordinary CRLF/LF normalization of `configuration.json`; its committed bytes are unchanged across the correction. Its working SHA remains `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9`.
- Runtime aggregate SHA: `af53b321220001166b73bc420b67c7526cddfe4198b8bf34ef69f7406082d868`. Only `physics.py` differs among all 13 runtime modules. Neural, engine, schema, chemistry, geometry, inspector, snapshots, reconstruction, smokes and diagnostics are byte-unchanged. Corrected physics SHA: `2a2e53bdfb3964488a446f1549682bc00cb4bc0403ef4a95f1adc245a4e58f63`.
- Semantic configuration remains `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`. All recorded dependency versions match both receipts and the running environment. All 16 selected source identity records remain identical to the previous build; their current original files and all five pinned Git blobs match.
- The nested prior review ZIP remains byte-identical with SHA `a376ad876a164e96cc0b0b1f4f9d250fc8bb70bc4b585bca24092fdee3ada57f`. The copied prior independent review equals the original review export, SHA `ffa7ffe6561ed94c2003faf1eb123637a37932c8573757b018c0dfe070dada54`.

Evidence: `PACKAGE.json`, `GIT.json`, `IDENTITIES.json`, `PRESERVATION.json`, `REVIEW_PRESERVATION.json`.

## VERIFIED — prehistory reuse

Every runtime dependency except physics is byte-identical across commits, including the prehistory entry point, field solver, geometry and stream/configuration definitions. Physics is not used by world-only preparation. The existing loader's law/source/AST/archive/array checks pass (`loom_p/prehistory.py:49–80`). Field SHA remains `7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096`; archive SHA remains `f968ed0875d68e3421c5acc9f9a4a218727b9698877b1cc86225d4fec9e6ef7d`; phase remains `3.558411277237072`. Cache reuse is valid. No generation function was invoked by this review. The builder's retained manifest and inspected preflight route support its disclosed zero regeneration. Evidence: `PREHISTORY.json`.

## VERIFIED — all corrected saved records reproduce

The unchanged `verify_engineering_records.verify(root)` at lines 14–46 was inspected and called directly. Its writing command-line entry point at lines 48–56 was not called. The new `verify_correction.verify()` also writes artifacts and was not executed.

| Existing attempt-003 case | Native / wave / events | Neural reconstruction | Final fields | Maximum accounting residual |
|---|---:|---|---|---:|
| birth_30s | 3000 / 150 / 3000 | Every saved hash identical | Bit-identical | 5.535190903717402e-17 |
| nonzero_resume_1s | 100 / 5 / 100 | Every saved hash identical | Bit-identical | 5.463362509790237e-17 |
| contact_ui_1s | 100 / 5 / 102 | Every saved hash identical | Bit-identical | 5.5162173656989055e-17 |

Checksums, monotonic counts, separate native-noise/wave clocks and source/body arithmetic passed. Final state hashes are respectively `a00f93dbf36f8dd8b1ceaf107ef33c72d8a002562342966105265554a6a422d2`, `ad168f9afffc34612a66e84569efbfa44dc12f97d4aaac811e5250e9c0df58b3`, and `89bcc4e608b539786beb82e60e5e7a339b1e96d9f10a31d5c166496b74de3f94`.

Full configuration, seed 5284097, life 0, fixture definitions and caps 30/1/1 seconds equal attempt-002. All 3,200 corresponding raw/physical native rows and organism hashes agree; all 160 wave records agree. Initial state hashes agree, while new wrapper hashes correctly identify changed runtime code. The contact case has exactly one extra zero-duration source-0 release at time zero, with no transfer/damage/repair/cost; every other physical event row is exactly equal to its attempt-002 counterpart. The release is explicitly `event_kind=release` and reuses the instantaneous `impact=true` accounting representation; it should not be interpreted as a collision merely by counting that Boolean. No current consumer defect was identified from this representation.

Evidence: `RECONSTRUCTION.json`, `ATTEMPT_COMPARISON.json`, `EVENT_COMPARISON.json`. These are reproducibility checks, not independent physical trajectory generation or efficacy evidence. Shared production neural/field arithmetic is reused and cannot by itself prove the equations correct.

## VERIFIED — paused evidence and observer isolation

Starting from the existing 0.07-second midwave snapshot, detached neural and field arithmetic reconstructs all remaining 93 native records, every neural hash and the exact final field. No `Engine.step()` was invoked. This independently exercises restoration of partial accumulators and saved random/held states. The builder's complete body resume comparison is additionally recorded by the unchanged `smokes.py:49–73`; its manifest reports 0.93 seconds of duplicate continuation, full-state equality and observer noninterference. This review did not rerun that complete physical loop.

An independent `Inspector()` loads attempt-003 at time zero. Observation, pause, replay at index 39, detached reconstruction, and observation again reproduce 40 records while leaving live state hash `54a10515c2e5a099a0441445cf30fd926af4ccbb040060a9f9928895ea9f22f3`, random counters and time unchanged. Session steps remain zero; no recorder/server is created. Relevant production paths: `inspector.py:16–68`, `reconstruction.py:9–29`, `records.py:86–92`. Evidence: `MIDWAVE_RECONSTRUCTION.json`, `OBSERVER.json`.

## LIMITATION / EXPECTED PROVISIONAL CHOICE — scope of process claims

The final local artifacts establish direct ancestry, unchanged selected files and internally consistent recorded evidence. They cannot independently prove the historical absence of every push, PR or Workbench/vault Git write. Those remain builder-reported process claims; this review performed none and found no contradictory evidence. The source hashes establish unchanged accepted source documents rather than a whole-vault audit. The 252-file preservation check relies on the recorded baseline inventory; the previously independently checked 87-file inventory and exact preserved ZIP provide additional prior anchors.

No scientific quality or efficacy conclusion follows. Cross-host bit identity, renewed visual/browser QA, long-run behavior and exhaustive contact convergence remain outside this subreview. No new provenance, reconstruction or observer blocker was found.

## Safe reproduction

From the exact target worktree root, the following operates on existing records and writes no target artifacts:

```powershell
@'
from pathlib import Path
import sys
sys.path.insert(0,str(Path('developmental_ecology').resolve()))
from verify_engineering_records import verify
for case in ['birth_30s','nonzero_resume_1s','contact_ui_1s']:
    r=verify(Path('developmental_ecology/artifacts')/f'smoke-{case}-attempt-003')
    print(case,r['reconstruction'],r['field_reconstruction_bit_identical'])
'@ | & '.\.venv\Scripts\python.exe' -B -X utf8 -
```

`audit_provenance.py` contains the complete independent hash/diff/record/observer checks used here and writes only beside itself. It uses exclusive evidence creation; copy it to a fresh authorized review-output directory for a new execution. Run it with the target worktree as working directory and its existing `.venv` Python, using `-B -X utf8`. One initial invocation from the project working directory failed Git discovery before reconstruction; retrying from the target working directory succeeded. This was a review-harness setup issue and changed no target file.
