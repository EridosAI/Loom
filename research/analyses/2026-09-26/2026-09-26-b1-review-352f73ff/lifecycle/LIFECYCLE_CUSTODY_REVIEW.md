# Independent B1 apparatus lifecycle and custody review

**VERIFIED within the requested lifecycle scope.** The corrected gateway permits one accepted bounded command, rejects overlapping/stale/cross-session requests, keeps paused simulation state inert, and makes an ended interactive case non-resumable. No directly material lifecycle defect was found. Overall B1 disposition also depends on the separate information-flow, held-fixture, regression and provenance reviews.

Corrected apparatus: `352f73fffa6d9781eae8aa38e708a9a05669588f`; parent: `68db2c581f07200966d699a4f55a65f9b96df1e9`. Read the complete final-review request, `LIVE_OPERATOR_STATE_MACHINE.md`, builder correction report, A–L matrix, complete old/new `sensor_ui.py`, actual HTML lifecycle code, relevant runner/authority/pending patch hunks and delivered component tests. No held positive-control or B1 snapshot/geometry/evaluator file was read or loaded by this subreview. No launch authority was generated.

## Fresh old baseline failures

The old process imported the preserved actual 68db worktree source, not an injected replacement. A validation-only check copied its generic sensor-human manifest and supplied the **complete exact hidden-display declaration** from this review's corrected generic record: kind, four indices, omitted representation and implementation identity. Actual old `authority.validate_execution(..., complete=True)` rejected it with **`unsupported display intervention`**, while accepting the original FULL-RAW manifest. No Engine, Run or snapshot was constructed in this supplementary call. It exits 1 at the intended `OLD HIDDEN RED` assertion. See `old-hidden-exact.log` and `old-hidden-exact-results.json`. The combined duplicate baseline had first used a shorter kind/hash declaration, also rejected by the same old none-only guard; its original results are retained. This complements correction fault A's deliberately reinstated old guard and is not a held-case launch or fabricated commissioning grant.

On the old generic 0.2-second fixture, two identical `HumanGateway.submit(.1,.1,'same submitted body')` calls produced **20 native steps and two controller records**, rather than one ten-step hold. The first returned at index 10; the duplicate returned at index 20, time `0.20000000000000004`. Full reconstruction accepted the resulting manufactured segment. The process then exited **1** at the intended assertion `OLD DUPLICATE RED: identical duplicate accepted a second ten-step hold`. No guard or old source was patched. See `old.log` and `old-results.json`.

This shows the old gateway lacked a consumed-request distinction. It does not claim that sequential duplicate calls themselves produced simultaneous physical integration.

## Corrected lifecycle and actual HTTP checks

The independent corrected process used only the delivered style of generic manufactured state, uniform invented field values and horizons at most 0.2 seconds. It ran the real loopback `OperatorHTTPServer`/handler against the real gateway. A synchronization wrapper delayed the first already accepted call before the real `Run.hold`, so requests could be tested during RUNNING without racing uncontrolled world operations. Once released, the original physical hold ran normally. Cleanup releases the gate, joins the server/request threads and closes all cases.

| Required property | Independent result |
|---|---|
| PREPARED is not started | Command submission rejects. Direct attached `Run.begin_command` and `Run.advance(0)` reject `operator case is not running`. Complete engine and session hashes remain equal. |
| Explicit start | PREPARED becomes PAUSED, with a new revision token and no physical state change. The old PREPARED token cannot issue a command afterward. |
| Paused deliberation | Three reads at each manufactured wall-clock offset of five seconds and 300 seconds preserve the entire engine and session hashes and exact UI envelope. These are substituted wall clocks, not literal five-minute sleeps. |
| Paused refresh/reconnect | Fresh HTTP connections to `/`, `/session`, `/sensors`, `/session` preserve exact engine/session, current decision token, condition, history and last-command payload. |
| RUNNING publication | While the accepted command is blocked before its first native call, GET exposes RUNNING, no actionable token and exactly the previous completed permitted sensor payload. Read requests add zero native/field calls. |
| Duplicate/concurrent requests | Two additional identical `/command` requests and `/start` and `/end` requests during RUNNING all return the generic HTTP 400 response. There is one entered hold, not a queue of accepted holds. |
| Client closes during RUNNING | The accepted POST's socket is closed before the gate is released. The already authorized bounded hold completes once. No connection closure or server response failure creates another command. |
| One command, one hold | Exactly **one hold entry**, maximum active entries **one**, **ten native calls**, **ten field calls each `.01`**, and **one controller record**. It returns to PAUSED at native 10, physical time `0.09999999999999999`. |
| Delayed delivery after completion | Reusing the consumed command token after the gateway returns to PAUSED still returns HTTP 400; no eleventh step or second command record appears. Three further GET reconnections preserve exact state and custody. |
| Explicit end | PAUSED becomes ENDED. Submit, start and direct `Run.hold` all reject. Refresh/reconnect remains ENDED and does not change engine/session hashes. |
| Interactive restart | `Run.resume()` on the normally closed interactive pause receipt rejects **`interactive cases cannot resume`** before Recorder creation; no resumed output directory is created. |
| Genuine case cutoff | A separate generic `.1`-second case ends after exactly ten steps. It publishes ENDED and rejects a further command without advancement. |

The corrected accepted ten-step physical state exactly equals the old first ten-step state: full engine SHA-256 **`dfd6a0cd62ff2fcaf23426d28985cfeb954799eb6953456a07f53c98cccab254`** in both processes. This is a bounded cross-version preservation control, not a B1 outcome. The corrected generic withdrawal and cutoff records each reconstruct ten native records, zero neural-wave records and ten events, with maximum accounting residual `1.5998758307739225e-17`.

Paused equality covers the physical clock/index, body pose/velocity/reserves, fields, organism/neural/RNG/wave state and all remaining engine fields through the complete engine hash. The complete session hash additionally covers pending decision/remainder, progression/counters, history, commands, lifecycle and execution identity. The old and new records and all checks remain in this new `lifecycle/` directory.

## Custody and post-validation changes

A token from a separate fresh generic case, using a different case identity and display mode, is rejected by the first case without changing any state. The consumed PREPARED token and consumed command token are rejected independently. Reads do not regenerate a token, select a case or reconstruct a world. The opaque nonce/revision belongs to the existing gateway's bound Run, rather than accepting a caller-supplied case selector.

Three delivered-scope mutations were made only to separate new manufactured cases **after** construction/validation and start:

| Mutation | Before-world rejection and result |
|---|---|
| Change `run.manifest['case_id']` | Private cause `manifest changed during run`; operator receives only `request unavailable`; zero native calls, native/time remain 0/0. |
| Change `session['execution_sha256']` | Private cause `session execution identity mismatch`; same generic operator rejection; zero native calls. |
| Change chemistry-hidden manifest declaration to FULL-RAW | Private cause `manifest changed during run`; same generic operator rejection; zero native calls. |

All three leave complete physical/RNG data unchanged and fail closed as ENDED. Apparatus failure bookkeeping intentionally changes `status`/`failure`; the physical comparison excludes only those two fields and does not incorrectly claim identical bookkeeping after rejection. No forged approval, implementation bypass or source edit was used. This confirms the live correction does not permit a post-validation case/session/deprivation substitution to actuate.

Authority's existing complete execution object includes the exact display intervention. New declaration validation and implementation identity are added rather than bypassing approval binding. The full suite's unchanged prior authority cases and distinct FULL-RAW/CHEMISTRY-HIDDEN declaration checks are handled by the root review; this subreview does not generate a new commissioning approval to test them. The root ran the twelve B1 fault/control pairs, not a new replay of all previous fault matrices.

## H/I fault meaning and coverage limits

Delivered H at `tests_apparatus/test_b1_operator.py:113–124` bypasses the token claim only after the first hold returns to PAUSED. Its RED executes a second real ten-step generic hold, making the fault consequential; the unmodified control rejects the same consumed token. Our genuine old-source duplicate reproduction and corrected delayed-token HTTP test independently cover that causal distinction.

Delivered I at lines 126–147 bypasses the RUNNING claim and uses a blocked `hold` synchronization stub. Its RED detects **two accepted execution entries**, not two physically integrated concurrent worlds. This is an appropriate narrow concurrency sentinel but must not be described as an observed overlapping physical trajectory. Our corrected HTTP probe uses the same bounded gating principle followed by one real hold, records maximum active hold entries one, and verifies ten actual native/field calls. The root review separately reproduced all twelve A–L fault/control pairs and inspected their intended assertion failures.

The supplied stop-mode tests also cover terminal, wall, storage, failure, withdrawal and shutdown with no resume. This independent subreview directly repeats withdrawal and cutoff, post-validation failure, and a RUNNING connection loss. It does not duplicate every stop fixture or claim exhaustive operating-system/concurrency fault tolerance. A client disconnect cannot cancel a command already accepted; the reviewed contract permits that bounded command to finish and forbids a second hold. An abrupt process/OS failure is not a promised recovery workflow.

The inspected HTML uses one in-flight action, consumes the displayed token, disables action controls before sending, prevents second click/key-repeat dispatch, uses response epochs to discard stale reads, and locks rather than automatically retrying uncertain requests. Actual DOM/egress/leakage tests belong to the separate information-flow review. Reconnect is permitted observation of the same paused case; it is not resume of an ended case.

## Source mapping

All locations are in corrected `developmental_ecology/loom_commissioning/` unless stated otherwise.

| Source | Relevant mechanism |
|---|---|
| `sensor_ui.py:48–60` | Fresh unadvanced sensor-human attachment and persisted PREPARED lifecycle. |
| `sensor_ui.py:62–102` | Opaque per-gateway revision tokens, copied display, exact lifecycle/token claim and inert explicit start. |
| `sensor_ui.py:104–123` | Claim under lock before RUNNING; native hold outside lock; next token only after complete publication; no accepted request queue. |
| `sensor_ui.py:125–145` | Failure/withdrawal/shutdown end semantics; no restart transition. |
| `sensor_ui.py:147–184` | Threaded HTTP service exposes only explicit read/action routes and generic errors; no automatic command on read/disconnect. |
| `runner.py:75–77` | Reject all attached interactive restart sessions before Recorder construction. |
| `runner.py:138–150,155–158,196–200` | Original identity/pending guards plus attached-lifecycle RUNNING gate before command/advance. |
| `runner.py:259–280` | End lifecycle before final snapshot/receipt; no world advancement in closure. |
| `authority.py:104–109,145–154,176–184` | Display implementation/condition and session execution identity/lifecycle validation. |
| `pending.py:56–60` | Human issued inputs validated against their declared display projection. |

The examined native-index clock and external physical adapter remain byte-identical across these imports: clock SHA-256 `2fa876c7ff2a0b1e704da009bf23300e046105512ab9d104a885ceb213e658b2`, adapter SHA-256 `ded81ad92bba426580ae4e9609fb95211aedf92a51fe19a63d05003970972aee`. Full imported-source identities are saved in `old-results.json` and `new-results.json`. Source/diff inspection found no actuator-bound, hold-length, native-clock or physical update change in the lifecycle correction. The complete P/config/package preservation audit is separate.

## Commands and receipts

From the shared workspace, with `PYTHONDONTWRITEBYTECODE=1`:

```powershell
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-26-b1-review-352f73ff\lifecycle\check_lifecycle.py' old
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-26-b1-review-352f73ff\lifecycle\check_lifecycle.py' new
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'exports\2026-09-26-b1-review-352f73ff\lifecycle\check_old_hidden.py'
```

Observed Python exits: **old 1 at the intended duplicate assertion; new 0; exact hidden baseline 1 at its intended rejection assertion**. Main script SHA-256: `6b7e6284c563e71d509822e72a7606baccaed705b91ee5118f31a55de3748b02`; supplementary script SHA-256: `cf9a1575936db03a90d780ae46d89631787f9de5a8c3682cf6e571de2ff29521`. `COMMAND_RECEIPTS.json` records the exact invocation and results. Fresh component directories are exclusive; rerun into a new review directory rather than overwriting these receipts. No harness setup failure occurred.

Only new review files/manufactured records were written. No prepared positive control or B1 case ran; no sealed hidden geometry was opened or disclosed; no target, prior export, Workbench, canon or Git file was changed. Findings are mechanical apparatus observations, not human-competence/perceptual/ecological claims or execution authorization.
