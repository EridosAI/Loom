# Independent R1-P provenance and saved-evidence contribution

Reviewed `6bc9683b54e4fa80136fe8534d7713e2a250a95f` against `f7eb6f27c661e3db193a4225b56a825d7e41739d`. The original `d5f7efbe67193f215e52d95ca912db131a79f31c` remains an additional preservation anchor. This is the provenance/reconstruction subreview, not a separate overall commissioning disposition. No provenance, saved-record or observer blocker was found.

No target, Workbench, source, existing artifact or Git state was modified. No freely acting lifetime, smoke, prehistory generation, server or live inspector step was started. New evidence is confined to this review directory. The exact previous independent post-correction report and new report/helpers were read before execution; writing verifier/package entry points were inspected but not executed.

## VERIFIED — exact identities and preservation

| Identity | Independent result |
|---|---|
| HEAD | `6bc9683b54e4fa80136fe8534d7713e2a250a95f` |
| Direct single parent | `f7eb6f27c661e3db193a4225b56a825d7e41739d` |
| Original checkpoint | `d5f7efbe67193f215e52d95ca912db131a79f31c`, preserved and reachable |
| Branch | `build/p-engineering-baseline-20260921-01a0c405` |
| EXP1-21 tree at all three checkpoints | `f1b884a7ada4c806786d1530d76d446aac5d37b1` |
| Semantic configuration | `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a` |
| Working configuration SHA | `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9` |
| Runtime aggregate SHA | `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9` |
| New physics SHA | `72a7768a82d23cbb9aed806a67a3e466a2a1d053d3488d3e10f91d5376413783` |
| R1-P delivery ZIP SHA | `c1f2cd0ed8ebe09f3a9b07d087f6fe9f25ca62f3f61a827628802bc35e5fa322` |
| R1-P delivery ZIP bytes | 150,085,054 |
| Exact complete correction patch SHA | `a6b58eff994e5900013dda2265805c397c4071424fd3fe3af7e95c9de375c1a7` |

All **171** manifest entries match bytes/hash and account for exactly **172** unique ZIP members including the manifest. All **60** tracked packaged files match working delivery and committed content; `configuration.json` has only the already-disclosed CRLF checkout/LF Git representation difference. The committed configuration is byte-unchanged across checkpoints. The packaged patch and supplied assembled patch both equal the full unscoped binary Git diff. All attempt-004 streams and snapshots are included, including birth.

The preserved f7 delivery ZIP exactly matches its prior independent SHA `7e33da1b05646c5af352a4114e99082c52b51b2b5966911f30816fb2911091da`; the original d5 delivery ZIP remains `a376ad876a164e96cc0b0b1f4f9d250fc8bb70bc4b585bca24092fdee3ada57f`. Both earlier build-document directories have no Git changes. The copied previous independent review equals the original export: 35,475 bytes, SHA `897610b06492554fd8299518dbc993117211ad133dda2129ee463299a1162f06`.

All **489** entries in the new before-correction preservation inventory match. The earlier **252**-file inventory and independently anchored original **87**-file evidence inventory also match. During this review all **792** current target artifact files were hashed before/after, with no changed or added artifact files. An initial read encountered Windows access denial for a preserved old pytest snapshot; approved scoped read escalation allowed the full inventory to be checked. No inaccessible entries are omitted from the claim.

Evidence: `PACKAGE.json`, `GIT.json`, `IDENTITIES.json`, `PRESERVATION.json`, `PRIOR_REVIEW_IDENTITY.json`, `REVIEW_PRESERVATION.json`.

## VERIFIED — mechanism, dependencies and source representations

Only physics differs among all 13 runtime modules. All 12 others, including neural, engine/scheduling, schema/configuration, geometry/illumination, chemistry, streams, snapshots, inspector and reconstruction, are byte-identical to f7. All five previous test files are byte-identical; the new oblique test is additional. The pinned dependencies match both receipts and the running environment (Python 3.13.5, NumPy 2.3.3, SciPy 1.16.2, pytest 8.4.2, with other versions listed in `IDENTITIES.json`). This supports unchanged selected P equations, packet/centering/pooling laws, handoff and random-stream cadence; it does not independently establish that the changed physical event path is correct.

**Source qualification:** 14 of the 16 source identity records are unchanged. The two differences are administrative Workbench files, not selected P/scientific equations or accepted world/coupling source documents:

| File | Previous bytes / SHA | Current bytes / SHA |
|---|---|---|
| `00_RESEARCH_MAP.md` | 4919 / `94568977c104a3511f20b36784fe0613134764eab6c883dee35d4a8042df2150` | 5685 / `3c41c9fbad74fd5efbf59eb405a18f9bb1ff49df5076dbeef9f4323bc5e7491d` |
| `01_WORKSPACE_STATUS.md` | 6573 / `e38231bc1c9b0df9240e30e95c49fdefdb53b590c4e55b42d02e6707926686a4` | 7462 / `87dd151c48bfbb73b1cee0d1751434ea959d2760cfcc3dba1eed14184d9cf410` |

The exact diffs add the f7 checkpoint's ENGINEERING HOLD status, original R1 closed / R1-P open / R2 and R3 verified closed, and preserve the former specification-stage text as historical. They link intake `1677619b` and agree with the prior independent review. The new package accurately identifies and contains the current bytes. No author or acceptance attribution is inferred from these changes. All selected mechanism/foundation source identities remain unchanged, and all current source files and five pinned Git blobs match their respective recorded hashes. Do not describe the entire 16-entry inventory as unchanged. Evidence: `ADMINISTRATIVE_SOURCE_DIFFS.json`, `IDENTITIES.json`.

## VERIFIED — chemical prehistory remains valid for reuse

Complete chemistry, geometry, schema/streams, prehistory and serialization modules and the configuration remain byte-identical across the corrective delta. Physics is not a dependency of world-only field preparation. The existing `prehistory.py:49–80` checks law values, seed-derived phase, preparation-source dependencies, archive checksum and field array checksum successfully. Field SHA remains `7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096`; 94,596-byte archive SHA remains `f968ed0875d68e3421c5acc9f9a4a218727b9698877b1cc86225d4fec9e6ef7d`; phase remains `3.558411277237072`. No prehistory generation was invoked. Evidence: `PREHISTORY.json` and unchanged dependency hashes.

## VERIFIED — attempt-004 reconstruction and comparison

The inspected `verify_engineering_records.verify(root)` at lines 14–46 was called directly. Its CLI writes the old artifact at lines 48–56, so it was not executed. The new `verify_r1p.evidence()` also writes target outputs and was not used. Existing saved inputs alone were reconstructed.

| Existing attempt-004 case | Native / wave / events | Final time | Neural hashes and final field | Maximum accounting residual |
|---|---:|---:|---|---:|
| birth_30s | 3000 / 150 / 3000 | 30.00000000000189 | All match exactly | 5.535190903717402e-17 |
| nonzero_resume_1s | 100 / 5 / 100 | 1.0000000000000007 | All match exactly | 5.463362509790237e-17 |
| contact_ui_1s | 100 / 5 / 102 | 1.0000000000000007 | All match exactly | 5.5162173656989055e-17 |

Checksums, native index/time order, separate noise/perturbation clocks, source/body accounting, all **3,200** neural hashes and all **three** final fields pass. All cases remain administrative pauses under the existing cap tolerance. Final state hashes are respectively `a00f93dbf36f8dd8b1ceaf107ef33c72d8a002562342966105265554a6a422d2`, `ad168f9afffc34612a66e84569efbfa44dc12f97d4aaac811e5250e9c0df58b3`, and `89bcc4e608b539786beb82e60e5e7a339b1e96d9f10a31d5c166496b74de3f94`.

Complete configuration, master seed 5284097, life 0, fixture definitions, 30/1/1-second caps and initial state hashes match attempt-003. New snapshot wrappers identify the new code. **All nine native/wave/event streams are byte-identical after decompression between attempts 003 and 004**, establishing the builder's no-trajectory-difference claim without selecting a subset of fields. This equality is an observation, not a success requirement and not evidence that the oblique release class was exercised by these three smokes.

Evidence: `RECONSTRUCTION.json`, `ATTEMPT_COMPARISON.json`, `EXACT_STREAM_COMPARISON.json`.

## VERIFIED — saved midwave and observer isolation

Detached continuation from the existing nonzero snapshot at 0.07 seconds/native index 7 reproduces the remaining **93** neural states and final field exactly. No `Engine.step()` was called. This exercises restoration of partial integrals, held values and random counters. The unchanged `smokes.py:49–73` implements the builder's recorded complete-state 0.93-second comparison; this review does not rerun a freely acting physical continuation.

The inspector automatically loads attempt-004 at time zero. Observation, pause, replay index 39, detached reconstruction and another observation reproduce 40 states while leaving live hash `54a10515c2e5a099a0441445cf30fd926af4ccbb040060a9f9928895ea9f22f3`, random counters, time and zero session-step count unchanged. No recorder or server is created. Relevant unchanged paths: `inspector.py:16–68`, `reconstruction.py:9–29`, `records.py:86–92`. Evidence: `MIDWAVE_RECONSTRUCTION.json`, `OBSERVER.json`.

## LIMITATION / EXPECTED PROVISIONAL CHOICE — claim scope

Reconstruction reuses production neural/field arithmetic and establishes deterministic storage/schedule fidelity, not an independent physics oracle or scientific efficacy. The full-body freely acting resume comparison was not rerun; saved partial-state reconstruction corroborates its record without exceeding authorization. No renewed browser/visual or cross-host verification is claimed. Finite component/smoke coverage is not exhaustive contact-space proof.

Current local bytes and ancestry establish the preservation claims above, but do not prove historical absence of every remote or vault operation. No remote/vault operation was attempted for such negative claims. The 489-file baseline receipt is builder-recorded; the earlier 252/87 inventories and independently established prior ZIP hashes provide additional anchors. No new source/canon or law-bearing change was found from this scope.

## Safe reproduction

From the exact target worktree root, using the existing pinned environment:

```powershell
@'
from pathlib import Path
import sys
sys.path.insert(0,str(Path('developmental_ecology').resolve()))
from verify_engineering_records import verify
for case in ['birth_30s','nonzero_resume_1s','contact_ui_1s']:
    r=verify(Path('developmental_ecology/artifacts')/f'smoke-{case}-attempt-004')
    print(case,r['reconstruction'],r['field_reconstruction_bit_identical'])
'@ | & '.\.venv\Scripts\python.exe' -B -X utf8 -
```

`audit_provenance.py` contains the full independent hash/diff/source/record/midwave/observer checks. It writes only beside itself with exclusive creation. For re-execution, copy it to a fresh authorized review-output directory and run it with the target worktree as working directory, existing `.venv` Python, `-B -X utf8`. Its Git calls use `GIT_OPTIONAL_LOCKS=0` and a process-local safe-directory setting; no persistent Git configuration is changed. Protected old pytest artifacts may require scoped read permission. The target is always read-only.
