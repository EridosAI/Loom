# Independent corrected clock and ordinary restart review

Date: 2026-09-25. Reviewed apparatus `9d31e7902658b15762052a2a6a3d161d64338524` versus `05abf60401d08f38750bca589b1c040e10513d7b`. P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.

**VERIFIED:** the previous nominal-clock comparator failure is corrected, including transition and final stop. The tested adjacent boundary class, rejection of new crossing holds, normal partial-hold restart and absolute cutoff behave as declared. These results concern an unmodified valid pending-hold state. They do not certify integrity against mutation of the held command/count; that separate executable state issue is reviewed by the coordinating/runtime-state reviewers and can prevent overall apparatus fitness despite this comparator closure.

## Exact former failure — VERIFIED

The exact old `controllers.py` Git blob was read from `05abf604` and executed only in an isolated in-memory module namespace. Its SHA-256 is `064f27b73903dff7d7793d609e65c574aa21a59bdf1cc32bea039b7591ec34dd`. The preserved input has time `0.09999999999999999`; the declared first deadline is 0.1. An independent Decimal/native-tick calculation assigns that representation to native decision tick 10.

| Calculation on the same saved input | Cursor | Command |
|---|---:|---|
| Exact old code, two-stage route | 0 | `[0.6958934252903155, 0.23474350126270044]` |
| Corrected code, two-stage route | 1 | `[-0.3577907305552408, 0.6422092694447592]` |
| Exact old code, final stage | 0 | `[0.6958934252903155, 0.23474350126270044]` |
| Corrected code, final stage | 0 | `[0,0]` |

The corrected transition command exactly equals the old controller's output on the same input at the exact nominal boundary. This confirms unchanged command arithmetic while changing only due-time classification. Replacing the corrected comparison in memory with `now >= deadline` restores both old wrong outcomes; restoring it returns the correct results. The coordinating review independently reruns the delivered consequential RED/GREEN processes.

`controllers.py:15–20` uses the existing absolute `Config().event_time_tol=1e-10`, with `rel_tol=0`. It neither rounds nor resets world time. The predicate controls both route progression at lines 76–77 and final stopping at line 89. The extracted settings preserve the old gain, bound and target-force literals; the scoped diff contains no controller goal or route tuning.

## Boundary class and independent oracle — VERIFIED

The independent oracle uses 80-digit Decimal values of the actual represented floats. It determines interval ownership through the exact lower boundary `deadline - tolerance`, independently of `math.isclose` and the production helper. Native decisions also have a separate Decimal/integer-tick check. This avoids declaring every value that rounds to tick 10 due: a value more than the declared tolerance below the deadline must remain not due.

Thirteen fixed cases were checked, rather than an open-ended search: zero with a full hold available; 0.09; two tolerances and 1.1 tolerances before; the represented tolerance threshold and its neighboring machine numbers; half a tolerance before; immediately below, exactly at and immediately above 0.1; half and two tolerances above. Both selected cursor and final-stage stop agree with the independent oracle in all cases.

The distinction at the actual tolerance edge is consequential:

| Represented time | Exact represented gap to deadline | Due / final stopped |
|---|---:|---|
| `0.0999999999` | `1.000000082740370999…e-10` | No |
| `0.09999999990000001` | `9.999999439624929209…e-11` | Yes |
| `0.09999999995` | `5.000000413701854995…e-11` | Yes |
| `0.09999999999999999` | `1.387778780781445675…e-17` | Yes |

The source does not assert an exact decimal interpretation of binary floats. The independent calculations and these expectations use the actual represented values, the existing absolute tolerance and the stated native cadence.

## New-hold rejection versus global cutoff — VERIFIED

`runner.py:120–122` derives the route stage from approved times starting from cursor zero, rather than trusting a saved cursor. Lines 123–129 reject an expired final stage or a new hold whose end lies beyond the selected stage's deadline/tolerance. The cursor assignment, held-command/count update and command record occur only after those checks. Existing global remaining steps still cap the hold.

Six **preflight-only manufactured continuation clocks** exercised the actual `Run.begin_command` path. The probes explicitly injected the clock into an otherwise copied manufactured continuation; they are not represented as lawful physical histories and are not included in replay-equality claims.

| Clock | New command result |
|---|---|
| 0.0, first stage ending 0.1 | Accept ten-step hold, stage 0 |
| 0.09 | Reject crossing new hold |
| `0.1 - 2e-10` | Reject crossing new hold; still genuinely not due |
| `0.1 - 5e-11` | Transition to stage 1, accept ten-step hold |
| 0.1 | Transition to stage 1, accept ten-step hold |
| `0.1 + 5e-11` | Transition to stage 1, accept ten-step hold within existing tolerance |

Rejected cases retain the complete engine **and session** hashes, zero pending hold steps and zero new command records. Their two repeated retry attempts also retain those identities. Engine identity includes body reserves/expenditure state, fields, raw values, neural state, native/wave counters and RNG. An in-memory apparatus-step sentinel further ensures preflight does not call physical advancement. Thus a rejection does not merely shorten the action, spend basal energy, update fields or secretly issue a zero/full command.

A not-yet-due stage with less than a full hold left remains an explicitly rejected incompatible prescription. It does not automatically advance time until it becomes due. A genuinely due intermediate boundary transitions on the next command decision. An expired final boundary rejects every new hold; normal and near-tolerance restart each rejected three retries without state or command changes. No loop inside the runner silently retries, advances or compensates.

The report's interior-stage **reject rather than shorten** rule is consistent with preserving the ten-step hold contract and declining to invent a partial-stage scheduler. The original design §4.1 prescribes 0.1-second holds with 0.01-second mechanics; the previous review required preserving that cadence and pause remainders. Neither prescribes an interior partial-stage policy. The correction report explicitly discloses this rejection rule. No conflict requiring a new Jason interpretation was identified for these tested cases.

Global truncation remains distinct and preexisting. A manufactured 0.1-second final case executes ten steps and ends at `0.09999999999999999`; a manufactured 0.07-second final case executes exactly seven steps and ends at 0.07. Both close as administrative cutoff and reject further holds. The seven-step case is the retained absolute-case cap behavior, not interior-stage shortening. No native step crosses the authorized case endpoint beyond ordinary representation error.

## Normal pause/resume and held-command ownership — VERIFIED within stated scope

The real two-stage manufactured route was run for only 0.2 seconds. One continuous path and three split paths pause at native indices 7, 9 and 10:

| Pause | Recorded time | Remaining first-hold steps | Resume result |
|---|---:|---:|---|
| Native 7 | 0.07 | 3 | Finish first hold at 10, compute new stage-1 command |
| Native 9 | 0.09 | 1 | Finish first hold at 10, compute new stage-1 command |
| Native 10 | `0.09999999999999999` | 0 | Immediately compute stage-1 command |

The existing held pair is exact through its remaining steps, while the next stage receives a newly calculated different pair. Each resumed path exactly matches the continuous final **complete engine** hash. The continuous path makes exactly twenty field calls, each at 0.01 seconds, and leaves inactive external neural/RNG state unchanged. It has two ten-step command records and no neural waves. Display reads during the ordinary pause leave the engine hash unchanged. All final native indices are 20 and the time is `0.20000000000000004`, within binary representation error of the immutable 0.2 deadline.

A separate final-stage path ends its ten-step hold at the nominal 0.1 boundary while the case has additional absolute time available. Its normal restart cannot gain another hold. A disclosed **manufactured clock variant** at `0.09999999995` is saved and reloaded through the normal restart path; it likewise cannot regain a final-stage hold. That near-tolerance probe advances zero further world steps and does not make a physical-reconstruction claim for the injected timestamp.

Nine ordinary substantive segments (continuous, three first/resumed pairs, two global cases) pass the delivered full native/wave/event/final-state reconstruction verifier, covering 97 native records including duplicated continuous/split coverage. Their maximum ledger residual is `5.439645587267117e-17`. Reconstruction shares production arithmetic and demonstrates record/state preservation; the Decimal oracle and explicit call counts supply independent timing checks. Synthetic preflight clocks and the timestamp-adjusted final pause are deliberately excluded from this reconstruction count.

These ordinary restart results must not be expanded into a guarantee against modifying pending hold state. They preserve the correct issued command/count; they do not validate an altered command/count as authorized. The coordinating review's separate mutation finding must remain visible in any overall conclusion.

## Limits and scope

**LIMITATION / EXPECTED PROVISIONAL CHOICE:** the explicit fixed boundary cases do not prove arbitrary-clock or long-run convergence. Unsupported interior prescriptions are rejected; no automatic partial-stage policy is introduced. Global shortened final holds and early physical terminal stops retain prior behavior. Short component timings are not throughput estimates.

**SCIENTIFIC / COMMISSIONING QUESTION, NOT AN APPARATUS DEFECT:** route competence, contact success, long lives, human controls, A1–A5/B1–B4/C1/C2, learning and survival were not tested or used as acceptance criteria.

Read the complete prior independent apparatus review, new correction report, corrected controllers/runner/authority source and correction tests, and the complete scoped controllers/runner diff. The commissioning design, matrix, configuration rules and decisions document were read in the preceding review and used here to interpret the preserved contract. The root review owns the full delta/package, authority, runtime mutation, provenance and complete suites/fault matrices.

No target code, Git, configuration, Workbench or preexisting artifact was modified. All outputs are in this new export. No commissioning or new prehistory occurred. Actual world advancement was limited to the disclosed manufactured components, each no longer than 0.2 seconds; record replays reproduce those same components only.

## Reproduction

Evidence is `independent_clock_review.py`, `INDEPENDENT_CLOCK_RESULTS.json`, `INDEPENDENT_CLOCK_CONSOLE.txt` and the export-local manufactured segment directories. The initial process completed with exit 0; every explicit old/new, disabled/restored, boundary, no-side-effect, record and normal restart assertion passed.

Copy the script to a fresh output directory before rerunning so existing receipts remain preserved:

```powershell
$python = 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
$review = 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-25-p-apparatus-correction-review-9d31e790\physical'
$fresh = Join-Path $review ('rerun-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $fresh | Out-Null
Copy-Item -LiteralPath "$review\independent_clock_review.py" -Destination $fresh
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:GIT_OPTIONAL_LOCKS = '0'
& $python -B -X utf8 "$fresh\independent_clock_review.py"
```

Conclusion: the specific comparator correction and normal boundary/restart behavior are supported. No additional clock-predicate defect was found. Overall apparatus disposition must also include the separate pending-hold integrity and authority/runtime findings.
