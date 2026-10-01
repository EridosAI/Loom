# Pending-command mechanical closure

**VERIFIED — the known A-R1c pending-command/save-resume blocker is closed for the exact prior failures and the delivered bounded cases reviewed here.** No remaining correction is requested in this subreview. This is a mechanical finding, not commissioning authorization or a claim of exhaustive protection against arbitrary interpreter modification.

Reviewed corrected `5f07748102cb5eaa302569c87efbae095050e9fe` against previous HOLD `9d31e7902658b15762052a2a6a3d161d64338524`. P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. The controlling request is the final mechanical closure attachment `28576fbe-9b89-4481-b331-6f0a03b6bb4f/Pasted text.txt`. Scope is the known pending-state failure and the package's manufactured boundary fixtures. Other blockers, complete suites, fault matrices and overall provenance are reported by the other reviewers.

## Exact old RED and corrected GREEN

The old runtime was imported from the preserved read-only `exports/2026-09-25-p-apparatus-correction-review-9d31e790/portable/developmental_ecology`, in a separate process. Its actual apparatus identity is `2c626ab028e895a1a63dfecdaa7bb6b4666beb26984af90dee020db01c040536`, matching the prior HOLD receipt. The new process imports the corrected target directly, actual apparatus identity `d5801b69ae38d3259f3426aed8753fef8d76132a2f4ffecdd9baffb29afeb71a`. Both report P runtime `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`. Actual imported paths and individual source hashes are saved in each results JSON.

The reproduction uses the existing `manufactured()` fixture: position `[5,5]`, angle `.3`, energy `.7`, integrity `.8`, zero initial field, explicit manufactured provenance. The unchanged two-stage plan is point `[6,5]` until `.1`, then `[5,6]` until `.2`, both with zero requested press force. It is not a commissioning start or an authorized scientific case.

On old 9d31e790, a normal decision issues `[0.717668244562803,0.237668244562803]` for ten steps. After seven steps, the script changes only the exposed pending pair to `[-.5,.5]` and remainder from three to four. Ordinary `close()` and `Run.resume()` accept it, and `hold()` reaches native index **11**, time **`0.10999999999999999`**, with the substituted pair after the `.1` stage deadline. Both old segments pass full verification: seven and four native records. No production guard was disabled and no checksum, restart or receipt file was edited. The independent load-restart → edit returned session → constructor path also reaches index 11 and passes its four-record reconstruction.

The old process exits **1** at the intended assertion, `OLD PENDING HOLD BREACH: seven plus altered four executes step 11 after the stage deadline`. This is a fresh reproduced failure, not an inherited claim or an import/setup RED. See `old.log`, `old-results.json`, and `old-components/`.

On corrected code, all four delivered public mutations reject both `hold()` and ordinary `close()` at native seven:

| Mutation | Rejection |
|---|---|
| Held pair only | `pending command differs from issued decision` |
| Remainder 3 → 4 only | `pending remainder differs from issued native progress` |
| Pair and remainder together, the exact old saved failure | `pending remainder differs from issued native progress` |
| Coherent replacement decision input/command plus held pair | `issued decision changed during segment` |

Every rejection has **zero native adapter calls and zero field calls**. Complete engine, body, field-array and inactive neural/RNG hashes are unchanged; time/index remain `.07`/7, energy `0.6998615632228802`, integrity `.8`. No bad final restart is written. Consequently the rejected attempt spends no basal energy, applies no physics/contact change and creates no native or wave advancement. Restoring only the manufactured session's original values permits its intact segment to close and pass full reconstruction.

Editing a legitimately loaded session's pair/remainder then calling the corrected constructor rejects with `loaded pending/session state changed before resume`, before any Recorder call or output directory creation. This closes the second exact old entry path. The corrected script exits **0**; see `new-002.log` and `new-002-results.json`.

## A–G closure evidence

| Requested class | Classification | Independent result |
|---|---|---|
| A. Legal mid-hold remainder | VERIFIED | Ordinary pause after seven resumes with exactly three pending steps. Those three preserve the issued pair and end at native 10, time `0.09999999999999999`. |
| B. Pending hold would cross authority | VERIFIED | The original 7+4 mutation and the delivered detached `(time=.09,index=9,remainder=2)` case reject. Neither gains a step. The remainder must equal issued length minus actual native progress. |
| C. Deadline cannot execute stale hold | VERIFIED | At native 10, setting a stale remainder of one rejects on three consecutive attempts with unchanged complete state. Exact `.1` and the delivered near-deadline detached inputs also reject the stale remainder. |
| D. Near-tolerance decision | VERIFIED within the delivered cases | `.1-5e-11` and `nextafter(.1,+inf)` at native 10 reject stale remainder one. Returning the remainder to its actual zero accepts pending validation and selects stage 1. The ordinary represented native-10 time also selects stage 1. No world time is rounded or changed. |
| E. New stage owns fresh command | VERIFIED | After the legitimate three-step remainder, the next decision is recorded at native 10 for stage 1 with pair `[-0.3577907305552408,0.6422092694447592]`. Only this fresh pair advances the next ten steps. |
| F. Altered command rejected | VERIFIED | Pair-only, combined pair/count and coherent decision/pair edits reject before evolution/save; loaded edits reject before output. |
| G. Altered count rejected | VERIFIED | Count-only and combined 3→4 edits reject before evolution/save; count cannot override the issued decision or native progress. |

The five delivered detached saved-state tuples were exactly `(.07,7,3)`, `(.09,9,2)`, `(.1,10,1)`, `(.09999999995,10,1)`, and `(.10000000000000002,10,1)`. Only the first accepts. These are preflight inputs, not claims of physically reconstructed injected clocks. At index 10 the tested zero-remainder controls accept and choose the fresh stage. The invalid remainders are rejected by the earlier progress invariant; these observations do not falsely claim the later deadline branch alone caused rejection.

The legal split run ends at native 20, time `0.20000000000000004`. Its complete engine hash **`a85c65c3a644c595a8a2edccc15a796e21b890b74aff8dcd310632201ac3a7a9`** exactly equals the independent continuous fixture. The resumed segment has exactly thirteen field calls, all `.01`, no wave records and unchanged inactive neural/RNG state. The split segments contain seven and thirteen native records; the continuous control contains twenty. Full reconstruction and accounting pass, with maximum residual `5.439645587267117e-17`.

Existing global-cap behavior also remains: cases with their final stage/case deadline at `.07` and `.1` execute exactly seven and ten steps, exhaust the remainder, close at administrative cutoff and reject any further hold without state change. Invalid pending state is rejected; it is not silently shortened or transferred into a later stage. The documented ordinary global-case shortening remains distinct from inventing a partial interior-stage hold.

## Saved record continuity

The delivered coherent saved-payload corruption was independently repeated on a **copy of this review's new manufactured record**. Its decision input position and resulting command/held pair were changed consistently and its ordinary payload/file checksums honestly recomputed. The original issued action journal was retained. `verify_segment(..., replay=False)` rejects with `pending decision journal continuity mismatch: decision`; `Run.resume()` rejects the same mismatch before Recorder creation or output. Physical replay is not needed to detect this inconsistency. The original intact record remains valid.

This matters because old replay faithfully reconstructed the substituted arithmetic while accepting the unbound resumed pending state. The new journal and parent continuity checks establish the missing connection to the original issued decision.

## Source assessment

Source paths below are relative to target `developmental_ecology/`; exact source hashes are in the results.

| Source | Assessed mechanism |
|---|---|
| `loom_commissioning/pending.py:10–26` | Separate loaded-session receipt binds complete session, engine and manifest; public loaded edits fail before resume. |
| `pending.py:28–62` | Issued decision records/validates controller, input, pair, native/time, issued length, execution identity, stage and case deadline against approved scope. |
| `pending.py:64–89` | Segment seal, exact native progress/remainder, pair, cursor and elapsed time checked; positive remainder must still lie within case/stage authority. |
| `pending.py:91–118` | Action/native journal derives pending continuity and compares both final snapshot decision and remainder even without physical replay. |
| `runner.py:18–54` | Normal save validates pending state; load validates pending state and returns the separate read receipt. |
| `runner.py:75–94,126–143` | Resume verifies complete pause/source journal/origin state and parent identity before Recorder creation; live guard checks pending seal and progress. |
| `runner.py:154–191` | New hold retains existing crossing rejection and global shortening; issued action is validated and sealed before command recording. |
| `runner.py:193–216,240–243` | Guard precedes advancement; the physical call consumes the serialized issued command, and remainder decreases once per native step. |
| `runner.py:252–262` | Ordinary close checks before status/cost bookkeeping and final save, blocking the original normal-writer persistence path. |
| `validators.py:54–87` | Parent/source state/session continuity and issued journal are prerequisites for segment verification. |
| `controllers.py:15–20,76–90` | Preserved absolute `event_time_tol` boundary classification; unchanged comparator/source bytes in old and new imports. |
| `tests_apparatus/test_final_corrections.py:149–234` | Delivered pending mutation, resume, saved-boundary and coherent journal cases used to bound this independent review. |

The previous vulnerable reads were `9d31 runner.py:97–106` (guard omitted pending invariants), `142–161` (trusted public pair/count), and its normal close/save path. The old restart verifier trusted resumed initial pending state. The supplied `FINAL_CORRECTION.patch` and current source show the correction concentrated on these paths. A direct Git diff command was unavailable in this worker's restricted view; this subreview does not substitute that failure for the separate complete Git/provenance audit.

## Commands, receipts and limitations

All actual runs used the existing pinned interpreter, bytecode disabled, and wrote only below this new `pending/` directory. From the shared workspace, with `PYTHONDONTWRITEBYTECODE=1` and `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`:

```powershell
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-25-p-final-mechanical-closure-5f077481\pending\check_pending.py' old
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-25-p-final-mechanical-closure-5f077481\pending\check_pending.py' new -002
```

Actual old execution used the first script version, preserved as `check_pending_attempt001.py` (SHA-256 `09e99da03ea04d299a8a776a9d201530ec256b2a68b578475bbc3d2a40c543f4`). The completed script is `check_pending.py` (SHA-256 `7203da0afbb08cb4525c41a462cafebcf7c2557e10d62598b03133320d5e002b`). A rerun must supply a **new output suffix** after `old` or `new`; the script refuses to reuse its component directory. The old branch remains the same intentional stage-overrun failure.

One harness setup error is retained transparently: the first corrected attempt accidentally gave the `.07` global case a final route deadline `.1`, and the apparatus correctly rejected `route outside duration scope`. This happened after the mutation/7+3/boundary checks. `new-attempt001.log`, its script and components remain. Only the new review harness was corrected to give that existing global-cap fixture its intended matching deadline, and the complete bounded script was rerun in fresh `-002` outputs. This was not an apparatus RED or a source fix.

No commissioning, new prehistory, scientific route search, P change, target/Workbench/Git write, broad numeric search, private-seal mutation or interpreter-hardening exercise was performed. Complete state hashes and before-call sentinels establish non-advancement for the tested rejections; replay shares production arithmetic and is not an independent physical-law proof. These are sufficient mechanical closure observations for the known pending-state blocker within the final request's fence.
