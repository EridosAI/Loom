# Independent apparatus provenance and saved-record review

Reviewed checkpoint: `05abf60401d08f38750bca589b1c040e10513d7b` in `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405`. This is a bounded contribution to the apparatus review, not its overall disposition or permission to commission P. Runtime, authority, controller and fault-injection findings from the coordinating review must also be applied.

## VERIFIED — checkpoint, preservation and package custody

The checkpoint is the direct child of scientific P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`, on the named apparatus branch. Its diff adds 27 files; no pre-existing tracked file is modified or deleted. All 13 `loom_p` modules, configuration and the six prior test files are unchanged. `EXP1-21` has tree `f1b884a7ada4c806786d1530d76d446aac5d37b1` at d5f7efbe, f7eb6f27, 6bc9683b and 05abf604; all three earlier checkpoints are ancestors. See `GIT.json`, `ANCESTRY.json` and `IDENTITIES.json`.

The exact binary Git patch is 160,506 bytes, SHA-256 `d4fdf864080d0ee09c8a5a0fdfbd0fc1272722caf0768bc0e88e972f714f5dab`, identical to `APPARATUS.patch` in the package. The P aggregate identity is `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`; apparatus aggregate is `5dfe2c85b570d1ee84c83d812d883dd39b8bd6d1ffc3797461b7827463ba5058`; configuration semantic identity is `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`. Working configuration bytes are `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9`. Forty-three selected code/test/config/document files match the portable payload exactly and the commit either exactly or after CRLF-to-LF conversion. The conversion cases are enumerated, not silently treated as exact Git bytes.

All **792** old artifact files in the original engineering worktree match the apparatus builder's before-inventory byte length and SHA-256. The initial restricted read verified 726; a granted, narrowly scoped read-only retry verified the remaining 66 protected pytest artifacts. There were no missing or mismatching old files. See `PRESERVATION.json` and `PRESERVATION_SCOPED_RETRY.json`. This compares enumerated current bytes with the preserved receipt; it does not prove an absence of unrelated activity.

The ZIP was absent at the request's old apparatus-artifact path. Jason supplied its Workbench intake location, where the original was found:

`C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX\2026-09-24-p-commissioning-apparatus\Loom_P_Commissioning_Apparatus_Review_20260924.zip`

That original ZIP is **5,790,938 bytes**, SHA-256 **`87f4dbde39a72559caf6045c7ac68a649d9691a000d1569af5d26b090a63b053`**, exactly matching the original receipt. CRC validation succeeds. All 221 archive entries have safe, unique member paths; all 220 manifest payload entries verify. Every ZIP file is byte-identical to both the target assembled payload and the workspace portable copy supplied to the coordinating agent's suite. The suite therefore used the original ZIP's exact input files, despite the copy initially having been obtained from the assembly. No replacement ZIP was fabricated. `ZIP.json` resolves the initial absence recorded in `assembled_copy.json`.

## VERIFIED — sources and birth-cache discrimination

All ten current source files match their recorded identities and package reference copies, including the five design documents, final P review, build request and three Workbench administrative files. The design archive is 407,360 bytes, SHA-256 `018f23d8e1bdb9433d7a50c8e421f09deb70d26febc3a5f14d98fa3b467551d0`. Its 68 manifest payloads and all 55 reading copies verify. These checks establish exact selected source custody, not authorship or an additional acceptance decision. See `SOURCES.json`.

The unchanged life-0 cache passes `loom_p.prehistory.load`. It has 60,000 already-recorded world-only preparation steps, phase `3.558411277237072`, NPZ SHA-256 `f968ed0875d68e3421c5acc9f9a4a218727b9698877b1cc86225d4fec9e6ef7d`, and field-array SHA-256 `7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096`. The loader verifies original module bytes, byte-identical chemistry, relevant geometry/Streams AST dependencies, field-law parameters, phase and both field hashes (`loom_p/prehistory.py:49`).

Calling `from_verified_cache` with this cache and each proposed birth ID 1, 2, 3 and 4 rejects it as unmatched. Their derived phases are respectively 4.301831170857631, 4.7259539459117725, 0.570217752910867 and 0.5403400097866494. A life-0 1,200-second manifest can be validated without advancing its native index or changing its state hash. No cache was generated. See `PREHISTORY.json`; `loom_commissioning/initialization.py:8` and `:17`, `contract.py:70` and `:78` implement the relevant checks.

**LIMITATION / EXPECTED PROVISIONAL CHOICE:** only the old life-0 cache is delivered. Births 1–4 require their own later authorized, verified phase histories. The cache rejection is appropriate; it is not evidence that any birth was commissioned or that future authorization is otherwise sound.

## VERIFIED — existing manufactured records, alignment and observer isolation

After inspecting the utility, imported `loom_commissioning.validators.verify_segment` and applied it to the existing first, resumed-second and continuous segments for all three modes. No recorder/runner was opened and no new life was started. Each mode supplies 7 paused steps plus 13 resumed steps and a separate 20-step continuous record. There are **120 verified segment-native records**, **4 segment-wave records**, and **60 unique continuous native records / 2 unique waves**. All three continuous endpoints are `0.20000000000000004` seconds. External control correctly has zero neural handoffs and an unchanged inactive organism/RNG.

| Saved continuous mode | Native / wave / event rows | Final full-state SHA-256 | Maximum accounting residual |
|---|---:|---|---:|
| External controller | 20 / 0 / 20 | `4781752d53f7f166314afc59d266ec0981fdcd0965469b7fec47c8edc93a7689` | 1.600e-17 |
| Fixed structure | 20 / 1 / 20 | `0f9ad732f0774cf74bf250042dd0002094a0255f37fbeabea0454541cfcaff9a` | 5.424e-17 |
| Intact P | 20 / 1 / 20 | `d8a58accd4df24e96fe8ee1758950825ed883e7d70c39b49e7d0d933a9722785` | 5.424e-17 |

The verifier compares full reconstructed native and wave rows, events, final full engine state (including neural arrays, fields and random streams), field-update counts, sensor history, stop reason and source/body accounting. It checks declared stream counts and file hashes. Its implementation is at `validators.py:52`; actual results and endpoint neural/field hashes are in `RECONSTRUCTION.json`.

The independent supplemental replay also recomputed all **60 saved diagnostic rows exactly**, checked pre/post observer hashes at every row, and checked **160 cortical rows** directly against the old/new objects: step-start raw, old mean, residual, old references and applied shared/fine increments. Receptor-mean updates were recalculated from elapsed time and the configured time constant. Fixed-structure applied increments were zero. Every saved raw start differed from its endpoint, so these fixtures exercise a real distinction. Both wave records were checked for packet-minus-old-mean beta and separate old eligibility/applied-bank increments. `DIAGNOSTIC_RECONSTRUCTION.json` records these checks. The utility itself only checks diagnostic count/checksum; this supplement supplies the value reconstruction it does not perform.

For every mode, concatenated first+second native, wave, event, controller and diagnostic streams equal the continuous streams. The saved pause state equals the resumed initial state, contracts are unchanged, the final full-state hashes match, and parent manifest links match. External pause after native step 7 retains **3 remaining held steps**. See `PAUSE.json`.

Repeated copied sensor/privileged observations and mutation of their returned payloads leave each loaded initial state unchanged. Supplemental diagnostic reconstruction leaves every before/after engine state unchanged. See `OBSERVER.json`, `DIAGNOSTIC_RECONSTRUCTION.json`; `controllers.py:94`, `:107`, and `diagnostics.py:62`.

**LIMITATION / EXPECTED PROVISIONAL CHOICE:** reconstruction uses the same reviewed engine/adapter laws on detached loaded states. It strongly checks saved-evidence coherence and restart/observer isolation, but is not a second independent physics implementation. These short, zero-field manufactured fixtures do not demonstrate useful navigation, lawful birth behavior, long-run storage, beneficial learning or commissioning sufficiency. Parent review's authority and other safety findings remain independent of these successful checks.

## VERIFIED — estimate arithmetic, with its stated limits

The design workload sums to **8,960 simulated seconds**: physical 3,080, perceptual 1,080, intact 2,400 and optional fixed-structure 2,400. The three saved continuous receipts independently reproduce their reported durations, measured wall time, stored bytes and uncompressed record bytes. Largest observed wall rate is 15.16528950000065 seconds per simulated second; largest stored-byte rate is 4,801,189.999999999 bytes per simulated second. Multiplying by the proposed workload yields **37.744720533334956 machine-hours**, **43.01866239999999 decimal GB**, and **86.03732479999998 GB** with one duplicate. The previous design projection remains 11.674065179259136 hours / 17.658892757333334 GB. See `RESOURCE.json`, design `COMPUTE_ESTIMATE.json`, `P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md:13`, `:34`, and apparatus `BUILD_REPORT.md:43`.

**LIMITATION / EXPECTED PROVISIONAL CHOICE:** this is correct arithmetic from 0.2-second components with snapshot/diagnostic overhead. It is neither a measured 8,960-second workload nor a calibrated steady-state performance prediction or spending authorization. No native evidence was discarded in this review.

## Commands and write boundary

The main review command was the existing engineering venv's `python.exe -B -X utf8 <new-output>\audit.py`, from the apparatus target cwd. The supplemental command was the same interpreter/options with `diagnostic_audit.py`. Both scripts are preserved beside these receipts. They import the inspected read/replay functions; they do not call the writing CLI entrypoints of `package_apparatus.py`, `verify_apparatus.py`, prehistory preparation, or the legacy smoke runner. Git uses `GIT_OPTIONAL_LOCKS=0` and process-local `safe.directory`; commands include `rev-parse`, `diff --binary`, `ls-files`, `show`, `merge-base --is-ancestor` and `status --porcelain`.

The 66-file preservation retry read only inventory-listed old artifact paths and wrote only a new receipt in this review output. The package comparison read the user-located original ZIP in memory. All review writes were confined to the new workspace export, including its portable copy. The 422 target artifact files matched their before hashes and scoped Git status remained clean; the final repeat is in `FINAL_PRESERVATION.json`. No Workbench or target artifact, source, code, configuration or Git state was written. No new prehistory, commissioning life, scientific run or server was started by this subreview.

No additional **MUST-FIX BEFORE COMMISSIONING** finding arose in this provenance/saved-evidence subset. That statement does not override the coordinating review's defects or determine the apparatus-wide disposition.
