# Loom P — final mechanical closure review

**FIT TO BEGIN AUTHORIZED COUPLING COMMISSIONING**

Date: 2026-09-25. Reviewed apparatus: `5f07748102cb5eaa302569c87efbae095050e9fe`. Previous HOLD: `9d31e7902658b15762052a2a6a3d161d64338524`. P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.

All three known blockers are closed within the requested mechanical scope. Their original failures reproduce on 9d31e790, their corrected counterparts pass on 5f077481, all 18 new and 36 previous fault/control pairs reach their intended assertions, and both complete suites pass 143 tests. P and baseline configuration are unchanged. These checks exposed no directly material defect requiring HOLD.

This disposition establishes apparatus fitness for separately authorized commissioning. It does not authorize or start any case. No commissioning, new prehistory, target edit, Git mutation, Workbench write, fix or refactor was performed by this review.

## Concise closure table

| Known blocker | Original failure reproduced | Corrected evidence | Closure |
|---|---|---|---|
| A-R1a — duplicate/shadowed authority | Both exact conflicting raw approval files are accepted by old authorization; the rejection expectation fails RED. | Same bytes fail at duplicate detection; exact unambiguous approval succeeds. Delivered duplicate, canonical-key, alias, protocol-shadow and semantic-mirror checks pass before execution/output. | **CLOSED — VERIFIED** |
| A-R1b — actual controller escapes identity | Same-name runner alias emits `[-0.5,0.5]` instead of the approved pair; one native step executes and old replay accepts it. | Actual dispatch substitution is rejected with zero alternate calls, commands or advancement. Restored approved callable emits the expected pair. Wrapper/proxy, post-check replacement, settings/route and reconstructed-resume checks pass. | **CLOSED — VERIFIED** |
| A-R1c — pending command exceeds stage on resume | Ordinary seven-step pause, pair/remainder mutation 3→4, close/resume reaches step 11 past 0.1; both old segments pass replay. | Mutations fail before advance/save and before resumed output. Legal 7+3 reaches step 10 exactly within representation tolerance, then a fresh stage-1 command advances. Saved coherent corruption fails journal continuity even without physical replay. | **CLOSED — VERIFIED** |
| Complete regression | Previous suite and fault scripts retained. | 143 worktree + 143 portable; 54 pairs/108 logs; 59 P + 24 original apparatus + 30 previous correction + 30 final correction. | **VERIFIED** |
| P, scope and provenance | Prior checkpoints and inventories preserved. | Eleven-file apparatus/test/documentation patch; all required identities and inventories match; no commissioning receipt in the enumerated correction evidence. | **VERIFIED** |

No unresolved law-bearing or scientific change was identified. There is no remaining closure action from this review. The next execution decision belongs to Jason.

## Scope and controlling evidence

This review follows the user's `FINAL MECHANICAL CLOSURE REVIEW` request, preserved as `references/FINAL_MECHANICAL_REVIEW_REQUEST.txt`. It reads the prior independent 9d31e790 HOLD review, `FINAL_CORRECTION_REPORT.md`, the exact correction diff, changed source/tests and complete portable inventory/payload. The earlier three findings supply the failure definitions. The latest request's hard scope fence governs the review: no broad search for hypothetical edge cases, interpreter-level attack model, numerical campaign, controller redesign or scientific efficacy test was undertaken.

The worktree is `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405`, branch `build/p-commissioning-apparatus-20260924-01a0c405`. Execution used the existing pinned P engineering `.venv`: Python 3.13.5, NumPy 2.3.3, SciPy 1.16.2, pytest 8.4.2. All new files are confined to this new review export. Synthetic approvals are explicitly manufactured validation data, not Jason authority; accepted commissioning-purpose objects were validated only. Actual advancement occurred only in existing tests and the bounded manufactured fixtures specified by the review/package.

The evidence separates observed behavior, code inspection and limits. Exact old/new failures and delivered tests are executed evidence. Uniform duplicate-key coverage and the preserved causal call path are also inspected in source. Reconstruction uses the reviewed production arithmetic and demonstrates record consistency, not independent scientific efficacy. No untested commissioning outcome is used as a blocker or as a reason to claim success.

## 1. Exact diff and unchanged scientific scope

The exact `9d31e790 -> 5f077481` binary diff is **89,686 bytes**, SHA-256 `10b3d7f9f3f70d709f07267b0d8802ddab2943ea645fcda280681cca0f0e4585`: **11 files, 671 insertions, 31 deletions**. It matches portable `FINAL_CORRECTION.patch` and the reviewed Git objects.

| Changed file / complete hunk grouping | Assessment |
|---|---|
| `loom_commissioning/authority.py` | Canonical string-key/JSON-native validation; recursive duplicate decoder; actual dispatch validation; observer function identity added to applicable controller identity; protocol shadow rejection; closed approval envelope and strict request parsing. All address A-R1a/b. |
| New `loom_commissioning/pending.py` | Complete 118-line addition: loaded-session receipt, decision/stage identity, issued length/native progress, pending command/time/endpoints, and journal continuity. Addresses A-R1c. |
| `loom_commissioning/runner.py` | Imports; strict restart decoding and packed-key uniqueness; loaded-session/source/parent verification; captured dispatch and decision initialization; per-step guard; approved-route command calculation, post-call validation and issued decision; sealed command supplied to adapter; normal-save guard. Addresses A-R1a/b/c. |
| `loom_commissioning/sensor_ui.py` | Imports strict reader and replaces two JSON reader calls: offline saved view and submitted actuator request. Duplicate input rejection only; no information/interface redesign. |
| `loom_commissioning/validators.py` | Strict record/receipt/view reads; source-parent ancestry and state/session continuity; issued-action journal validation before optional physical replay. Addresses A-R1a/c. |
| Two new JSON files under `tests_apparatus/fixtures/final_review/` | Exact prior duplicate-approval counterexamples, one line each, byte-identical to the independent 9d31e790 review originals. |
| New `tests_apparatus/test_final_corrections.py` | Complete 243-line addition, 30 collected targeted checks. No previous test changed. |
| New `verify_final_corrections.py` | Complete 38-line addition orchestrating 18 targeted RED/control pairs; no commissioning entry point. |
| New `FINAL_CORRECTION_REPORT.md` and `LAW_CODE_TEST_MAP.md` | Builder report and traceability, 90 and 14 lines. Their consequential claims are independently checked here. |

Code/test paths above are under `developmental_ecology/`; the last documents are under `docs/developmental_ecology/p_apparatus_final_correction_20260925/`. Every changed file and hunk belongs to the three corrections or their tests/evidence/documentation. No world law, P rule, controller objective, commissioning case definition or scientific interpretation changed.

All 13 P module bytes match the `6bc9683b` Git blobs. Configuration retains its baseline Windows checkout bytes. The controller arithmetic and already-closed numerical comparator are byte-identical to 9d31e790, as are contract, adapter, diagnostics, initialization, evaluator, all 113 previous tests and both previous fault scripts. Configuration/some historical tests have the previously disclosed CRLF checkout versus LF Git representation; both hashes are retained rather than treating representation differences as new source changes.

## 2. A-R1a — duplicate and shadowed authority

The root reproduction imports the original 9d31e790 portable runtime in a separate process and passes the two exact prior raw files through `authorize_execution()`, with their raw-byte request hashes intact. Both are accepted. An explicit rejection expectation reaches `ORIGINAL DUPLICATE APPROVAL BREACH` and exits 1. The same two byte sequences on 5f077481 fail respectively with `duplicate JSON field: approved_execution` and `duplicate JSON field: point`; the corrected process exits 0. Both processes also validate a fresh exact unambiguous synthetic specification for their own runtime. Engine state remains exact, native index/time zero; no Run is constructed.

The preserved raw SHA-256 values are `b6efa768ee86703ab604118ea8f8e72d46070146ca1ac36535dc555e9cad2f51` and `7331d8ab7036f1bec1a8a995e994e52e7a08c65b3f08df6a9b69771eac3446e0`. Evidence: `duplicates-old-RED/`, `duplicates-new-GREEN/`, adjacent logs and `reproduce_duplicate_closure.py`.

`authority.py:27–38` inspects decoded object pairs before creating each dictionary. Any repeated decoded name, including an identical duplicate, raises before first/last-value resolution. The hook applies at every nesting depth without a field-name exception. `canonical()` at lines 14–25 admits actual string dictionary keys and JSON-native values only, eliminating the old integer-key coercion. Nonfinite values remain invalid. Sorted keys and insignificant whitespace preserve the unique semantic object; raw request-byte identity remains a separate mandatory check.

`read_approval()` at lines 170–174 requires exactly `notice`, `approved_execution_sha256` and `approved_execution`. An alias plus canonical field, or an extra top-level route/controller prescription, cannot be silently ignored. Existing closed manifest/execution schemas and identity comparisons reject inconsistent required mirrors. `validate_protocol_fields()` at lines 118–133 recursively rejects typed execution overrides inside descriptive procedure data.

| Required semantic conflict | Evidence establishing rejection |
|---|---|
| Repeated top-level/nested fields; controller or route/stage duplicates | Exact original files plus five delivered duplicate cases, including identical duplicate and stage deadline; strict reader has no field-specific bypass. |
| Alias plus canonical name / top-versus-nested shadow | Delivered approval-envelope aliases, controller/mode mirrors and nested protocol controller/route/intervention tests; closed envelope/schema and recursive reserved-field inspection. |
| Controller identity/constants | Repeated serialized names use the same unconditional recursive rejection. Unique but inconsistent controller/configuration objects fail exact implementation/settings identity and complete approval binding; previous regression cases retained. |
| Route/stage, intervention/deprivation | Duplicate point/until cases; ordered bound procedure and nested-shadow rejection; unsupported intervention remains rejected rather than selected or merged. |
| Initial state, phase, deadline | Repeated names are rejected before semantic decoding; unique inconsistent values remain subject to exact approved object/hash and existing initial-state/phase/duration checks, all retained and green. |

This table distinguishes representative executed duplicate fixtures from source coverage of the identical parser path across the named fields. It does not claim a new open-ended alias/fuzzing campaign. There is no first-value-wins, last-value-wins, silent merge, or supported second typed prescription. The readable unique approval object is the object used by the existing digest comparison. Duplicate packed restart keys and duplicate actuator JSON are also rejected by the delivered checks before unpack/submission. **A-R1a is closed.**

## 3. A-R1b — actual command-producing controller

The exact prior alias fixture was independently rerun against checkpoint-matched old and new imports. Old 9d31e790, with unchanged approved identity/request, executes a same-display-name replacement of `runner.waypoint_command`: actual `[-0.5,0.5]` versus approved `[0.717668244562803,0.237668244562803]`, native index 1/time 0.01. Old `verify_segment()` accepts that record. This is the original identity escape, not merely a different hash on an unused function.

Corrected 5f077481 rejects `executed controller dispatch mismatch: waypoint_command` with **zero alternate calls**, native/time zero, no own-command record and exact unchanged engine hash. Restoring the approved callable produces the expected pair in the bounded positive physical control. The observation harness exits 0 when it has reproduced the specified old failure/new success; the separate rejection oracle applies the same required rejection expectation to both saved outcomes, producing explicit old RED exit 1 and corrected GREEN exit 0 without repeating any world step.

`validate_dispatch()` at `authority.py:40–53` checks the references actually present in the runner's invocation namespace against the approved controller implementation/settings and returns a read-only captured mapping. `Run.begin_command()` at `runner.py:154` invokes those captured references, using a detached copy of the approved route, and rechecks dispatch/specification before recording the result. The tests replace each actual alias with a same-name proxy and also swap a reference immediately after validation: the alternate callable is never invoked, and the changed dispatch is rejected before accepting a command.

`Run.advance()` at lines 208–214 takes the actuator pair from separately retained serialized issued-decision bytes, rather than rereading the exposed mutable pair after validation. Pending decision validation ties that pair to the approved controller/route. The object that calculates the accepted pair and the pair passed to the unchanged physical adapter therefore share the verified decision path for the supported controller.

Five delivered alias cases plus post-check substitution, changed settings/route and reconstructed-controller resume checks passed directly as bounded closure checks. The same tests also appear in the full suite; they are not added to its count. A changed controller on resume fails before Recorder creation; the exact approved controller resumes successfully. Public `begin_command()` return behavior is unchanged; internal `_guard()` now returns the checked dispatch. `load_restart()` still returns its three values, with a verified dict-subclass session.

Evidence: `controller/CONTROLLER_CLOSURE_REVIEW.md`, exact old/new `RESULT.json`, source identities and both rejection-oracle logs. No private-interpreter manipulation or generalized machine-owner security claim is needed for this closure. **A-R1b is closed.**

## 4. A-R1c — pending authority, stage boundaries and save/resume

Old 9d31e790 independently reproduces the exact ordinary persistence failure: issue the ten-step first-stage command, advance seven, change the pending pair and remainder three to four, call normal close/resume. It reaches native index **11**, time **0.10999999999999999**, beyond the first stage's **0.1** deadline. Both saved segments pass the old full verifier (seven and four records). The direct loaded-session constructor variant reproduces the same consequence. No checks, receipt or checksum were bypassed/forged. The old process reaches `OLD PENDING HOLD BREACH` and exits 1.

On corrected code, four delivered mutation classes—pair, remainder, both, or a coherent changed decision plus pair—fail before `hold()` advances and before ordinary `close()` saves. The independent probe counts **zero adapter calls and zero field calls** at rejection. Complete engine, body, fields, organism/RNG identities and energy/integrity remain unchanged at native 7. There is no bad final snapshot. Editing the loaded session is rejected before a new Recorder or output directory exists.

The mechanism is explicit: `pending.validate_decision()` binds issued controller/inputs/command, native index/time, original hold length, stage identity/start/deadline and case deadline. `validate_pending()` checks the separate issued-decision seal, derives progress from actual native index, requires remainder = issued length − progress, checks exact pair/cursor and validates elapsed time and both remaining endpoints. It does not invent a shortened rescue hold. These guards run before advancement, normal save and supported resume.

| Required continuation | Corrected observed result |
|---|---|
| A. Legal mid-hold pause | Seven valid steps retain exactly three; resume finishes that command at index 10/time `0.09999999999999999`. |
| B. Remaining hold crosses stage | Manufactured index-9/remainder-2 state rejects; a changed three-to-four remainder at index 7 rejects before any causal step/save. |
| C. Exactly at stage deadline | A stale positive remainder at native 10 rejects; the intact zero remainder permits a new stage decision only. |
| D. Near tolerance | Delivered `.1-5e-11` and immediately-above-.1 saved-state preflights reject stale positive remainder; zero remainder follows the unchanged due-time rule. No injected timestamp is claimed as a reconstructed physical history. |
| E. Next stage | Fresh stage-1 pair `[-0.3577907305552408,0.6422092694447592]`, not the previous pair. Three stale-boundary retries cause no evolution. |
| F/G. Altered pair/count | Rejected before advance, before normal save, and before output from a changed loaded-session constructor. |

The valid resumed segment makes exactly **13 field calls of 0.01 seconds**: the remaining three plus ten fresh second-stage steps. It ends at native 20/time `0.20000000000000004`, exactly matching the continuous complete final-state hash. External inactive neural/RNG state remains exact and no neural wave occurs. This establishes no unauthorized world time, basal/body cost, neural update, handoff, field update or random draw for the rejected states, alongside exact legal continuation. The existing absolute tolerance explains represented endpoint differences; it is not enlarged or applied as an extra native-step allowance.

Stage/global interactions retain the declared rule. A valid final 0.07-second case performs seven steps; a 0.1-second case performs ten, followed by refusal of further advancement. New interior crossing holds remain rejected; the preexisting final global-cap shortening remains permitted. Controller dt, hold length, comparator and native terminal policy are unchanged.

Save/resume is now anchored beyond self-consistent snapshot bytes. A loaded session carries a separate lossless read receipt; the constructor compares the verified source snapshot and complete administrative-pause origin before output. Relative parent links retain source segment identity. `validate_journal()` plus `verify_segment()` checks issued actions, derived remainder and final pending state, and parent-to-child state/session continuity even when physical replay is disabled. The delivered coherent saved-decision corruption with honest new checksums fails `pending decision journal continuity mismatch: decision`; resume creates no output. The portable copy independently fails at the same check. Valid parent chains reconstruct successfully.

The independent pending probe's first new attempt correctly rejected a reviewer-created invalid global fixture: route deadline 0.1 exceeded case duration 0.07. The attempted script/log/components are preserved. Only that manufactured route deadline was corrected to 0.07, and the bounded final `new-002` run passed. No apparatus source was changed and this setup error is not counted as an apparatus failure. The final pending report documents exact commands and outputs. **A-R1c is closed.**

## 5. Consequential faults and complete regression

Fresh worktree suite: **143 passed in 94.30s**. Fresh extracted portable suite: **143 passed in 95.95s**. Both use the pinned environment, separate fresh temporary roots, bytecode disabled, pytest cache disabled and plugin autoload disabled; ambient `PYTHONPATH`/fault settings are removed. Portable execution uses its own assembled source and explicitly packaged existing life-0 cache. No new prehistory was generated.

Independent collection confirms **59 unchanged P + 24 unchanged original apparatus + 30 unchanged previous correction + 30 final correction = 143**. All 113 old tests retain their source identity. Collection executes no test bodies. Both full-suite logs are included.

The 18 final pairs cover five duplicate cases, non-string keys, alias envelope, nested protocol shadows, five actual dispatch aliases, four pending mutations and saved decision-journal disagreement. RED restores the old parser or removes the specific production check while leaving the rest active. Each fails at its named `DUPLICATE APPROVAL`, `CANONICAL KEY`, `APPROVAL ALIAS`, `PROTOCOL SHADOW`, `EXECUTED DISPATCH`, `PENDING COMMAND` or `DECISION JOURNAL` breach assertion, then passes unmodified. They are consequential to the three known blockers.

The previous 16 apparatus and 20 correction pairs also reproduce. Their existing guarantees include input/sensor isolation, identity, phase, ledger, observer, stop/trajectory labeling, frozen structure/discarded update, duration, extra native/wave/field/random update rejection, complete specification binding and the already-fixed clock comparison. The 18 authority negatives within the **previous** matrix still bypass a test callback, as previously disclosed; that limitation is not attributed to the new production-guard mutations. The old clock-transition RED has two failing and three passing parameter cases; GREEN has five passes.

All **54 pairs / 108 logs** were independently reread. Actual exception lines and traceback frames—not merely expected text appearing in source—match each intended failure. Every RED child exits 1 and each GREEN child exits 0. `FAULT_AND_SUITE_AUDIT.json` preserves per-log hashes, summaries, frames and exact commands. This evidence does not replace the exact original counterexamples and legal positive controls above; it supports them.

## 6. P immutability, timing and custody

**VERIFIED:** P aggregate remains `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`; all 13 module bytes match 6bc9683b. Configuration checkout SHA-256 remains `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9`, semantic identity `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`.

Authority, controller and resume metadata stays in apparatus validation/records. The adapter and P arithmetic are unchanged. Eighteen comparable native/wave/event/diagnostic/sensor/scientific-observation streams for the original three modes are byte-identical to their prior counterparts; all old controller-record fields are preserved, with only new issued-decision metadata added. Legal continuation field/native/RNG/wave counts remain exact. This is direct evidence that the metadata changes do not enter neural arithmetic or change timing on the legal paths checked.

The corrected checkpoint is the direct child of 9d31e790. Previous 05abf604 and earlier P checkpoints remain reachable. Historical EXP1-21 remains `f1b884a7ada4c806786d1530d76d446aac5d37b1` at all inspected checkpoints. All **792 prior P**, **1,908 prior apparatus/review/design**, **3,902 correction-baseline** and the previous independent **3,106-file anchor** inventories match their recorded sizes/hashes. These inventories overlap and are not summed. All **8,200 current target artifact files** remain unchanged across the review audit; Git status is clean.

Twenty existing good segments reconstruct exactly, including the portable new continuation and journal-positive fixture with parent chains: **237 native records, four waves, 237 events**. The packaged bad journal rejects even with replay disabled. The correction receipt census contains **333 manufactured outputs**, all at most 0.6 seconds, and **zero commissioning receipts**. This describes the enumerated delivered evidence, including old RED fixtures; it is not a claim about hypothetical unrecorded activity outside the reviewed material. No remote or vault operation was used to prove a negative process claim.

The supplied builder ZIP is **61,132,733 bytes**, SHA-256 `c0c0a0c426ff85c5fbf848ad34bba543218ff4420ebf9c573bc66737f6a34fcf`. All **846 unique safe members**, **845 manifest payloads**, sizes/hashes and CRCs pass. The checkpoint/diff match Git; 840 target-origin payload files and 45 selected source/config/test/document identities match their expected source representations. Historical nested packages retain their original bytes. Current apparatus aggregate is `d5801b69ae38d3259f3426aed8753fef8d76132a2f4ffecdd9baffb29afeb71a`.

The existing runtime membership/bytes match 432 NumPy and 1,078 SciPy entries. Life-0 cache remains unchanged, phase `3.558411277237072`, field hash `7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096`. Existing snapshots are interpreted with their matching apparatus version; historical records were not rewritten.

## Limits and stop point

This is the requested mechanical closure, not a broader security or scientific certification. General interpreter/private-internal replacement, UI polish, long-run performance, future controller competence, wider numerical cases and untested commissioning outcomes do not supply HOLD grounds here. No such campaign or refactor proposal was added. Structured human procedure text is inspectable approval material; operator compliance is not inferred by software. Supported resume requires an intact complete pause and its parent evidence chain. These are declared workflow limits, not unresolved versions of the three demonstrated blockers.

The independent intake contains this full review, concise closure table, exact reproduction commands, reviewed identities, all 108 delivered fault/control logs, exact old/new closure evidence, preserved setup-error evidence and provenance receipts. It also includes the byte-identical reviewed builder ZIP. The adjacent intake receipt identifies the final archive after a complete reopen/hash/CRC check.

All required mechanical conditions are met. Work stops here. No commissioning authority is issued or exercised by this review.
