# Loom P — final independent apparatus correction review

**HOLD BEFORE COUPLING COMMISSIONING**

Reviewed 2026-09-25. Corrected apparatus: `9d31e7902658b15762052a2a6a3d161d64338524`. Previous apparatus HOLD: `05abf60401d08f38750bca589b1c040e10513d7b`. P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.

The original clock-comparison defect is closed for the reproduced failure and the independently tested boundary class. The complete manifest now binds substantially more of the proposed execution, and ordinary substitutions fail before recording. Nevertheless, A-R1 is not fully closed: three concrete gaps remain in approval parsing, the identity of the callable actually executed, and pending-command continuity across save/resume. The last gap permits a first-stage command to continue to native step 11 past its step-10 deadline, and both saved segments pass the existing replay verifier.

Both fresh full suites passed **113 tests**. All **20 new** and **16 previous** delivered fault/control pairs reproduced their intended RED then GREEN outcomes. These results do not cover the three counterexamples below. P, configuration and the reported prior artifacts retained their identities. No commissioning was performed by this review, and no fix, target edit, Git mutation, Workbench edit or new prehistory was made.

## Concise closure table

Each material finding uses exactly one requested classification. An entry marked VERIFIED is limited to the proposition stated in that row.

| Item | Classification | Independent result / smallest remaining closure |
|---|---|---|
| A-R1: ordinary complete-specification binding | VERIFIED | The readable canonical object includes the required proposed arm, implementation, settings, procedure, initialization, interventions and resource scope. Twenty independent semantic substitutions are rejected before Recorder creation; the exact unambiguous synthetic approval is accepted in validation only. |
| A-R1a: ambiguous approval records | MUST-FIX BEFORE COMMISSIONING | Conflicting duplicate `approved_execution` and nested `point` fields are silently accepted. Reject duplicate object keys and ambiguous non-string-key coercion at the approval/canonical boundary. |
| A-R1b: actual runtime callable | MUST-FIX BEFORE COMMISSIONING | A same-name replacement of `runner.waypoint_command` executes while the checked `controllers.waypoint_command` remains approved. Bind/recheck the actual invoked dispatch path. |
| A-R1c: pending hold and restart continuity | MUST-FIX BEFORE COMMISSIONING | Changed pending command/count survive ordinary close/resume and accepted replay; step 7 + an enlarged four-step remainder ends at step 11. Bind/derive pending decision, command, issued length, elapsed native steps and stage/case end, including continuity between segments. |
| A-R2: original numerical comparison | VERIFIED | Exact old saved input is RED on old code and GREEN on corrected code; independent Decimal oracle, 13 boundary values, zero-evolution crossing rejection and due-stage transition agree. |
| Ordinary unchanged-command pause/resume and global cap | VERIFIED | Pauses at native 7/9/10 reproduce the continuous complete final state; final expired resumes cannot regain a hold. Global 0.1/0.07 cases perform ten/seven steps. This does not supersede A-R1c. |
| P / prior guarantees / test composition | VERIFIED | Unchanged 59 P + 24 prior apparatus + 30 correction tests; both 113-test suites pass. Previous 16 pairs and independent neural/D5/information/firewall controls pass. |
| Provenance and supplied correction scope | VERIFIED | Nine changed files only; all 792 prior P and 1,908 prior apparatus/review/design files match; EXP1-21 and prior checkpoints/packages preserved. |
| Interior crossing holds are rejected; runtime inventory is process-local | LIMITATION / EXPECTED PROVISIONAL CHOICE | Explicitly declared, consistent with the preserved contract in the tested cases. Neither choice independently causes HOLD. |
| Route competence, human controls, A1–A5/B1–B4/C1/C2, future caches, 600-second lives, performance and scientific outcomes | SCIENTIFIC / COMMISSIONING QUESTION, NOT AN APPARATUS DEFECT | Not tested here and not used as blockers. |

No unexpected scientific or world-law change, or reject-versus-shorten conflict, was found that requires an `UNRESOLVED / REQUIRES JASON` classification. Future execution authority remains Jason's separate decision; this review supplies none.

## Scope, sources and evidence boundary

The controlling request is the user's final post-correction review attachment, copied in this intake as `references/FINAL_REVIEW_REQUEST.txt`. Read and compared: the complete previous independent HOLD review, the new `CORRECTION_REPORT.md`, exact `05abf604 -> 9d31e790` patch, complete portable payload/inventory, changed runtime/test files and saved former-failure input. The commissioning design §4.1, matrix, configuration-change rules and `DECISIONS_REQUIRED_BEFORE_EXECUTION.md` remain interpretive sources; the latest explicit user instructions govern this review. Historical proposals are not treated as execution approval.

Target: `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405`, branch `build/p-commissioning-apparatus-20260924-01a0c405`. Existing pinned environment: Python 3.13.5, NumPy 2.3.3, SciPy 1.16.2, pytest 8.4.2, from the P engineering worktree's `.venv`. No installation or environment replacement was performed.

All new outputs are confined to this new export. Synthetic grants are explicitly labelled manufactured / not Jason authority / no execution. Accepted commissioning-purpose objects were exercised only by validation calls. Bad constructor probes are stopped before Recorder creation. Actual advancement is limited to deterministic tests and disclosed manufactured components, plus read-only reconstruction of existing components. Neither a synthetic validation success nor AV/replayed status is commissioning authorization.

The review separates code/data observations from builder process claims. Available correction receipts contain only manufactured fixtures, at most 0.6 seconds; no commissioning receipt was found. This supports the delivered scope. It cannot establish a universal negative about unrecorded activity elsewhere. No remote or vault operation was performed to expand that claim.

## 1. Complete diff and preservation of P

The exact binary diff is **58,401 bytes**, SHA-256 `20e5bc0f285a5bac6e7c46443e117b4bfc54c06695c5d6b2e4a98ce38fd19ba1`. It matches the portable `CORRECTION.patch`, with nine files, 771 added lines and 18 removed lines. Below, every changed hunk is assigned to its actual purpose; added files are single whole-file hunks.

| Changed file / hunks | Classification and content assessment |
|---|---|
| `loom_commissioning/authority.py`, new lines 1–123 | Authority correction. Canonical object/digest; runtime inventory; function/source/settings and adapter identities; complete procedure/resources validation; session and request checks. Within authorized apparatus scope. Omissions A-R1a/b/c below prevent complete closure. |
| `contract.py`, manifest signature/schema/execution hunks at 32–45; validation at 50 and 84–85; authority at 96 and 100–102 | Authority correction. Adds explicit plan/protocol/resources and schema 2, integrates complete execution validation, adds approved execution digest and readable request comparison. Old case/state/duration checks remain. No P state arithmetic changes. |
| `controllers.py`, import at 7; settings/helper/plan validation at 10–31 | Authority and clock corrections. Extracts unchanged nine literals into explicit settings, adds the existing absolute-tolerance comparison, and requires ordered finite prescribed stages. No gain, bound, force target or epsilon tuning. |
| `controllers.py`, waypoint hunks at 74–89 | Uses validated ordered plan, shared deadline predicate and the same arithmetic with named old literals. Changes due-time stage progression/final stop; otherwise preserves controller equations. |
| `runner.py`, imports/load at 14–15/33; constructor at 46–56; session at 71–72; guards at 100–103 | Authority correction. Validates readable scope before output, rejects separate route/resources/observer mismatch, saves execution identity, checks session route/resources and live implementation. Actual callable and pending-hold gaps remain. |
| `runner.py`, decision hunk at 119–129 | Clock correction. Derives stage from approved times rather than mutable cursor, rejects expired final stage and newly crossing hold before command/state recording. Preserves global remaining-step cap. Does not validate the invariant of a hold already in progress. |
| `tests_apparatus/fixtures/review-boundary-input.json`, new 243-line file | Evidence fixture only. Entire JSON parses and exactly equals the preserved second-action input, including time `0.09999999999999999`; no commissioning route optimization. |
| `tests_apparatus/test_corrections.py`, new 203-line file | Thirty collected correction cases: complete binding variants, supplied/live program/resource rejection, old exact and adjacent clock cases, crossing preflight and normal boundary restarts. Test coverage assessed below; count is not closure. |
| `verify_corrections.py`, new 35-line file | Test orchestration only: 18 authority and two clock subprocess fault/control pairs, isolated environment/output and assertion-specific receipts. No commissioning entry point. |
| `CORRECTION_REPORT.md`, new 79-line file | Builder documentation: scope, identity, clock policy, evidence and limits. Its claims were reproduced or qualified here. |
| `LAW_CODE_TEST_MAP.md`, new 16-line file | Traceability documentation for the two corrections and preserved constraints. Mapping does not itself prove completeness. |

Paths in this table are below `developmental_ecology/`, except the two documents below `docs/developmental_ecology/p_apparatus_correction_20260924/`. The table subdivides whole-file additions for explanation; it does not imply additional changed files.

**VERIFIED:** all thirteen `loom_p` modules exactly match their `6bc9683b` Git blobs, aggregate `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`. Configuration retains its previous Windows checkout bytes and semantic identity. LF Git versus CRLF checkout differences in configuration/some tests/fixture are disclosed individually in `provenance/scoped-complete/IDENTITIES.json`; they are not silently normalized changes. P tests, original apparatus tests and original fault runner have no committed change. Adapter, diagnostics, evaluator, initialization, validators and UI are unchanged. No world, neural mechanism or scientific parameter changed.

Schema-1 records remain associated with their original runtime/package. The correction does not claim they can be silently resumed under schema 2. Retaining historical records and their environment is an expected compatibility boundary, not a defect introduced by this review.

## 2. Complete proposed specification: verified coverage and parsing defect

`execution_object()` deep-copies every manifest field except the self-referential `execution_authority`; its digest is SHA-256 of UTF-8 sorted-key compact finite JSON. The readable request must contain both that digest and the complete approved object, and its raw bytes must match the grant's request hash. Ordinary changed content cannot be authorized merely by altering the grant digest.

The independent canonical receipt lists all 21 top-level fields: schema, baseline, P code, configuration, apparatus, case ID, purpose, mode, controller, initial state/time/index/fields, phase, initialization, duration, hard stop, command-hold seconds, selection, roster and execution. Nested execution includes Python/platform/executable/DLL and NumPy/SciPy identities; controller source/live function code/settings; adapter; ordered procedure/stages/protocol; explicit display intervention; storage and wall limits. The full human-readable object, including the nine controller constants, is saved in the synthetic positive request. Hash coverage is inspectable without guessing what a digest represents.

**VERIFIED:** an independent encoder/digest over that actual semantic object matches production. Reordering keys and changing whitespace preserves unambiguous meaning when the raw request identity is updated accordingly. Changing raw bytes without updating their approved request hash is a different check and remains rejected. Non-finite numbers are rejected.

Twenty independently written substitutions each change the corresponding actual field, produce the independently computed changed digest, fail binding, and fail the full pre-output entry path. A Recorder sentinel establishes that none reached output creation. They cover controller implementation; constants; waypoint; stage order; stage duration; initial state; mover phase; prehistory; case deadline; deprivation; case/arm identity; adapter; manual controller; sensor controller; fixed arm; intact arm; route prefix; route suffix; resources; and omission of a law-bearing default (`heading_gain`). Some also fail an earlier specific validation, such as phase/initial-state identity; the separate direct complete-binding checks demonstrate participation in the canonical object even in those cases. The exact unmodified object passes validation, with zero native steps.

### A-R1a — conflicting fields are silently resolved

**MUST-FIX BEFORE COMMISSIONING.** `authority.py:120` uses plain `json.loads(raw)`. A request containing conflicting duplicate `approved_execution` fields is accepted when the later value matches the manifest. A second request with a conflicting duplicated `point` inside the approved route is also accepted. An independent duplicate-aware decoder rejects both. Request-byte hashes and normal production authorization checks remain active; these are synthetic requests, not forged Jason authority.

The raw examples and results are in `canonical-001/`. They show an ambiguity at the inspectable approval boundary: a file can visibly contain two different prescriptions while production silently chooses one. This directly fails the user's requirement to reject duplicate/ambiguous fields, irrespective of whether ordinary hash substitution is otherwise sound.

A related input check accepts a protocol dictionary with integer key `1` and gives it the same canonical bytes/hash as a different dictionary with string key `"1"`. Python's encoder coerces the key, despite the canonical helper's string-key docstring. This does not establish a separate actuation failure for arbitrary protocol prose, but confirms that the admitted input domain does not enforce the stated unambiguous JSON representation.

**Smallest exact closure:** reject duplicate names at every nested level while parsing approval-bearing JSON, require string dictionary keys in values admitted to the canonical specification, and reject ambiguous inputs before authorization/output. Add conflicting top-level/nested duplicate and key-coercion negatives, retaining sorted-key/whitespace and exact-object positive controls. No cryptographic signer, human-language interpreter, new controller policy or P change is requested.

## 3. Runtime and restart: two consequential residuals

The new constructor correctly rejects a separately supplied changed route/resources before Recorder creation. Live session-route, controller-module setting/function and resource mutations have consequential rejection controls. Manifest changes remain guarded; saved execution identity is checked on load/resume. Those are real improvements. They do not cover all state actually used for future commands.

### A-R1b — the checked function is not necessarily the invoked function

**MUST-FIX BEFORE COMMISSIONING.** `authority.py:56–67,81–85` fingerprints functions in `controllers`; `runner.py:13–14,121` invokes separately imported references. Replacing only `runner.waypoint_command` with a different implementation having the same display name leaves the checked identity and complete synthetic approval unchanged. All normal guards pass. The actual one-native manufactured fixture delivers `[-0.5,0.5]` instead of the approved `[0.717668244562803,0.237668244562803]`. Saved-record replay accepts that segment.

The corresponding replacement at `controllers.waypoint_command`, the namespace used by the delivered test, fails before any native step with `controller execution identity mismatch`. This positive rejection control locates the gap precisely. No production file, checker or assertion was edited. Commissioning-purpose validation and manufactured physical execution are kept separate; both use the same implementation checks.

**Smallest exact closure:** ensure the identity checked before the causal call is the identity of the callable actually invoked, using one checked dispatch path or equivalent binding. Cover same-display-name replacement at the actual runner call site and examine the other direct controller aliases under the same rule. This is the explicit runtime-version/mutable-object requirement, not a demand to secure the computer against arbitrary owner tampering.

### A-R1c — pending command/count can change and survive accepted save/resume

**MUST-FIX BEFORE COMMISSIONING.** `validate_session()` at `authority.py:108–113` compares route, resources and execution digest, but not the pending decision/command/remainder. `Run.advance()` trusts those mutable fields; the stage-end check occurs only when creating a new hold. A pending hold bypasses that new-hold check.

| Independent fault | Consequence with checks enabled |
|---|---|
| Change the held command after a normal `begin_command()` | Guard accepts; next native step uses the substituted pair while the issued decision remains the original pair. |
| Enlarge `hold_remaining` from 10 to 11 | Eleven native steps execute to `0.10999999999999999`, still under the first stage whose deadline is 0.1. |
| After seven valid steps, change the pair and remaining count 3 to 4; call ordinary `close()` and `Run.resume()` | Normal save creates valid ordinary checksums; resume accepts; four more steps execute to index 11 with the substituted command. No receipt or file hash is edited. |

The explicit load-restart → session → constructor path accepts the same changed pending state. Both saved segments of the ordinary close/resume counterexample pass `verify_segment`: seven native records in the first and four in the second. The verifier trusts the resumed initial pending state without tying it to the previously issued decision. By contrast, direct within-segment mutations are detected later by replay. That later detection neither prevents evolution nor closes the normally saved/restarted variant.

This is mutation of exposed apparatus session data within the user's stated review scope, analogous to the supplied live-route mutation test. It does not modify body/engine law, disable guards, forge approval files, or require changing the approved route. It demonstrates an unauthorized stage overrun after the numerical comparator itself has been fixed.

**Smallest exact closure:** preserve and verify the issued decision and its command, start/native index, issued hold length, selected stage and applicable endpoints; derive or validate remainder from actual progress. Enforce continuity before advance and across close/load/resume and record validation. Reject changed pairs or enlarged remainders before evolution/output. Preserve valid pause-at-seven remainder three, pause-at-nine remainder one, and the new stage's freshly computed command. No new timing policy or P mechanism change is needed.

Detailed scripts, full outcomes, saved manufactured segments and positive controls are in `authority_runtime/review.md`, `RUNTIME_BINDING_RESULTS.json` and `FAULT_RECORD_VALIDATION.json`.

## 4. Clock comparison and boundary class

**VERIFIED:** the exact old controllers Git blob, SHA-256 `064f27b73903dff7d7793d609e65c574aa21a59bdf1cc32bea039b7591ec34dd`, was executed in an isolated in-memory namespace on the original saved input. At `0.09999999999999999` versus deadline `0.1`, it returns old cursor 0 and `[0.6958934252903155,0.23474350126270044]`, eligible under the old runner for another hold. Corrected code selects cursor 1 and `[-0.3577907305552408,0.6422092694447592]`. For a final single stage, old code still drives and corrected code returns `[0,0]`. Disabling the new comparison restores both failures; restoring it returns GREEN.

The corrected command exactly equals the old command at the exact nominal boundary. This supports a classification change with unchanged controller arithmetic. No world time is rounded or reset. The helper uses the existing `event_time_tol=1e-10`, absolute only.

An independent 80-digit Decimal oracle compares actual represented numbers to the deadline minus the represented tolerance. A separate native-tick calculation identifies the nominal decision boundary. Thirteen fixed cases cover: a complete hold available; 0.09; two and 1.1 tolerances before; the represented tolerance edge and both adjacent machine numbers; half a tolerance before; immediately below/exactly at/immediately above 0.1; half and two tolerances above. All expected stage/final-stop results agree. In particular, `0.0999999999` has represented gap slightly greater than `1e-10` and is not due; `0.09999999990000001` is due. The oracle does not reuse `math.isclose` or the production helper.

Six preflight-only manufactured continuation clocks also exercise `Run.begin_command()`. Zero accepts the full hold; 0.09 and `0.1-2e-10` reject a newly crossing hold; half-tolerance-before/exact/half-tolerance-after select stage 1. Rejection retains complete engine and session hashes, zero pending steps and zero command records. A causal-step sentinel confirms no physical advancement. This covers reserves/basal expenditure, physics/field, neural/native/wave state and RNG. Repeated rejected attempts make no progress. A due intermediate stage transitions; an expired final stage rejects three retries on ordinary and near-tolerance restart. There is no automatic retry loop that spends time or grants an extra hold.

**LIMITATION / EXPECTED PROVISIONAL CHOICE:** a genuinely not-due stage with less than a complete hold remaining remains an incompatible prescription; retrying does not make it due. Rejecting it is consistent with design §4.1's ten-step hold and the corrective instruction to avoid inventing interior partial-stage semantics. Existing global-cap shortening remains separate: a final 0.1-second case performs ten steps; a 0.07-second case performs seven, each followed by refusal of further holds. A native physical terminal event retains its prior stopping behavior. No source conflict requiring Jason to choose a new rule was found.

## 5. Ordinary pause/resume and global deadline

**VERIFIED within unmodified pending-state scope:** one 0.2-second continuous manufactured two-stage path and separate pause/resume paths at native indices 7, 9 and 10 end with exactly equal complete engine hashes. The respective remainders are three, one and zero. The old pair remains exact only through its valid remainder; the next stage gets a new different pair. Twenty field calls each use 0.01 seconds; external inactive neural/RNG state remains unchanged and no neural wave occurs. Final native index is 20; `0.20000000000000004` is ordinary binary representation error of the 0.2 endpoint.

A final-stage pause at nominal 0.1 cannot regain a hold even when global case time remains. An explicitly manufactured nearby timestamp `0.09999999995` also cannot regain one after save/load. That clock injection is a preflight test, not claimed as a physically reconstructed trajectory. Nine ordinary component segments pass full reconstruction, covering 97 native records including continuous/split duplication; maximum ledger residual is `5.439645587267117e-17`.

These positives do not establish the stronger invariant that no modified pending state can exceed a stage deadline. A-R1c disproves that invariant. The global cap in its tested paths remains effective; the fault exceeds the earlier stage while still within the larger global case scope.

## 6. Fault matrices and fresh suites

**VERIFIED:** complete worktree suite: **113 passed in 77.05 seconds**. Complete extracted portable suite: **113 passed in 60.96 seconds**. Both used the pinned environment, fresh distinct temporary roots, bytecode disabled, pytest cache disabled and plugin autoload disabled. The portable suite ran from its extracted source with its explicitly packaged verified cache. Collection confirms **59 unchanged P + 24 unchanged apparatus + 30 new correction cases**. Concurrent local checks affect elapsed timings; these are not commissioning performance estimates.

All 36 delivered pairs were rerun in subprocesses, yielding 72 logs plus exact-command receipts. Each RED exits 1 at its intended assertion; each GREEN exits 0. The 18 new authority variants reach `APPROVAL BINDING BREACH: <variant>`. Their fault mode skips the test's complete-binding callback; it does not independently patch 18 different production implementations. Their unmodified controls do mutate/check the actual proposed fields, and full constructor controls reject before recording. This establishes sensitivity to losing the binding check, not complete coverage of all parser/runtime/session paths. The root's independent semantic matrix and three new counterexamples address those omissions.

The new clock transition fault reaches two failures and three passing cases; its GREEN has five passing cases. This is expected: old comparison remains correct at exact/above or clearly earlier values, and fails the within-tolerance lower cases. The final-stop pair has one intended failure then one pass. Neither is an import/setup failure.

The previous 16 pairs retain intended failures for: identity, missing native record, phase, ledger, forbidden input, observer interference, stop label, sensor leakage, external/intact label, frozen structure, discarded update, duration, and extra field/native/wave/random updates. They remain consequentially closed for their stated cases. The complete assertion/log audit is supplied separately with all individual logs.

Old 05ab authority weakness was also independently rerun against original source with a synthetic byte-hashed grant, zero native steps and no Run construction; its old acceptance of changed controller/arm remains a reproduced counterexample. That is distinguished from the new test-only disabled-binding branch. Exact details and source identities are in `physical/old-authority/`.

## 7. Regression and scientific boundary

**VERIFIED:** unchanged cadence, absolute-duration, ordinary pause/resume, controller input restrictions, sensor-only isolation, fixed-structure restore timing, observer/RNG isolation, cache/phase rejection and birth-roster guard remain covered by the existing suite/fault pairs and independent checks. All 59 P engineering tests pass; runtime bytes remain the verified P implementation.

The earlier independent neural/receiver/leakage probe was copied byte-identically into this new export and rerun. Four structural families/combined poison controls retain exact causal state and RNG, while deliberately late restoration has consequential maximum difference `0.07729363526569996`. Twenty-nine transient fields and integral/counter behavior retain the reviewed behavior. D5 predetermined selection, detached influence probes, explicit nonzero receiver arithmetic and start/end raw alignment match the previous results: q norm `0.00032818861375509854`, causal reference hash `77b57f151a82c52b0e7c49d9a542e1e00e2310545173cab9acf3895c6d4fcca5`. Representative controller/sensor copies and metadata do not enter neural arithmetic.

An independent pure AV/CO/SO regression rejects SO and falsely relabelled SO; valid AV/CO creates only a Jason review request. Removing the SO guard in memory reaches `SO FIREWALL BREACH` (exit 1); the intact control passes (exit 0). Replay acceptance of the A-R1b/c faulty component records is explicitly reported above: faithful reconstruction of recorded arithmetic does not by itself establish authorized controller provenance.

**SCIENTIFIC / COMMISSIONING QUESTION, NOT AN APPARATUS DEFECT:** no conclusion is drawn about A1–A5 route/contact competence, human sensor-reference positive controls, B1–B4, C1/C2, useful learning, survival, parameter adequacy, later-life caches or long-run resource cost. None is a reason for HOLD. No scientific experiment number, canon change or controller tuning is proposed.

## 8. Provenance and reviewed identities

**VERIFIED:** corrected HEAD has direct parent `05abf604`; both prior apparatus and P checkpoints are reachable ancestors. Branch and clean status match the supplied identities. EXP1-21 is `f1b884a7ada4c806786d1530d76d446aac5d37b1` at all three checkpoints. All **792** prior P artifacts and **1,908** prior apparatus/review/design/package files match the recorded individual size/hash identities. All **3,106** current target artifact files are unchanged across the complete scoped audit. The earlier independently captured target inventory also matches.

The initial restricted audit encountered unreadable protected fixture trees; its partial receipts are retained for transparency. `provenance/scoped-complete/` is the authoritative replacement: a scoped read-only rerun enumerated and checked the protected trees, and completed all counts. Missing access was not treated as a match or an empty directory. No unresolved preservation mismatch remains.

Seventeen existing substantive final-suite segments were independently reconstructed: 210 native records, four neural waves and 210 events, with exact final fields, neural and engine state. They cover three apparatus modes and boundary pauses/resumes. All 21 comparable uncompressed continuous streams for the three original modes match the preserved 05ab records byte-for-byte. The complete correction-root receipt inventory contains 87 manufactured runs, all at most 0.6 seconds, zero commissioning receipts. Reconstruction shares production arithmetic and is not an independent scientific model proof; source inspection, fault controls and independent timing/neural calculations supply additional evidence.

The runtime membership and individual file bytes independently match 432 NumPy and 1,078 SciPy entries. Existing life-0 prehistory is reused read-only: phase `3.558411277237072`, field-array SHA-256 `7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096`. Wrong birth/phase combinations 1–4 are rejected. No 600-second prehistory or life was generated.

| Reviewed identity | Value |
|---|---|
| Apparatus runtime aggregate | `2c626ab028e895a1a63dfecdaa7bb6b4666beb26984af90dee020db01c040536` |
| P runtime aggregate | `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9` |
| Configuration semantic SHA-256 | `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a` |
| Configuration checkout SHA-256 | `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9` |
| Exact correction patch | 58,401 bytes; `20e5bc0f285a5bac6e7c46443e117b4bfc54c06695c5d6b2e4a98ce38fd19ba1` |
| Supplied corrected builder ZIP | 20,202,546 bytes; `e261dbb9836a916f3ff4b6daa3ae8d9c21ea12194198d1ed63dfa7ee9b798a81` |
| Original 05ab builder ZIP | 5,790,938 bytes; `87f4dbde39a72559caf6045c7ac68a649d9691a000d1569af5d26b090a63b053` |
| Previous independent HOLD ZIP | 7,227,837 bytes; `32c16dbf33ac368f4016b42b7c2b4ada355860e5541c5223ce3f163577d66006` |

The supplied corrected ZIP has 434 safe unique entries; all 433 listed payload files match `FILE_MANIFEST.json`, and all CRCs pass. Its checkpoint and exact patch agree with local Git. Its assembled runtime/test/configuration files match the target representations. The prior builder archive, previous review and original saved failure inputs match the retained originals. The corrected builder ZIP is copied byte-for-byte into this independent intake so the reviewed subject is available alongside this report; it is not repackaged as a new builder result.

## Required closure and stop point

Close A-R1a, A-R1b and A-R1c with the smallest changes stated above and consequential before-evolution negatives plus their existing positive controls. In particular, accepted replay of a normally saved altered pending command must become an explicit rejection, while a legitimate partial hold must resume exactly. Preserve P, the corrected comparator, previous artifacts and scientific sequence.

The package includes the full review, concise closure table, exact reproduction commands, machine-readable identities, source/patch reference, all 72 delivered fault/control logs, independent counterexamples, ordinary clock proofs and preservation receipts. It is prepared for Workbench intake only; no Workbench files were written. Work stops at this review. No commissioning authority is issued or exercised.
