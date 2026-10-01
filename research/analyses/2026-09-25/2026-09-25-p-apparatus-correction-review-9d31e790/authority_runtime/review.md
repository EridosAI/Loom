# Independent authority/runtime and neural-regression subreview

Checkpoint: `9d31e7902658b15762052a2a6a3d161d64338524`.
Previous apparatus: `05abf60401d08f38750bca589b1c040e10513d7b`.
Unchanged P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.
Target: `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405`.

**HOLD BEFORE COUPLING COMMISSIONING** is supported by two remaining runtime-binding gaps within A-R1. The corrected manifest binds the complete proposed specification, but the checked callable is not necessarily the callable actually invoked, and mutable pending-hold state can change actuation and stage duration across a valid save/resume. These findings require no P change and do not reopen the independently correct due-time comparison.

This subreview owns runtime callable/object binding, pending controller state and regression of the earlier neural/D5/information/firewall checks. The primary reviewer owns canonical ambiguity, the complete semantic substitution matrix, complete suites, and the overall disposition. The clock and provenance reviewers own their respective independent evidence.

## Finding 1 — checked controller identity can differ from the executed callable

**MUST-FIX BEFORE COMMISSIONING.** Source: `developmental_ecology/loom_commissioning/authority.py:56–67,81–85`; `runner.py:13–14,97–101,121`.

`controller_identity()` fingerprints the functions found in the `controllers` module. `runner.py`, however, imports separate direct references to `waypoint_command`, `time_due`, `command_pair` and privileged input functions. `Run.begin_command()` invokes those runner-local references. `validate_execution()` rechecks the module attributes, not those call sites.

The independent fixture creates the manifest before a replacement, then substitutes only `runner.waypoint_command` with a function having the same display name and a different code identity. The ordinary complete authority validation and all Run guards remain enabled. The canonical approved request, execution digest, controller settings and controller identity remain unchanged and pass. The resulting one-native manufactured fixture delivers `[-0.5, 0.5]`, while the approved controller would produce `[0.717668244562803, 0.237668244562803]` from the same body/input/route. The unchanged saved-record verifier also accepts this segment as AV/replayed.

The positive rejection control substitutes the same alternate function at `controllers.waypoint_command`, which is the namespace used by the delivered test. That control correctly fails `controller execution identity mismatch` before a command or native step. Thus the test's existing version check is consequential, but covers a different binding from the one the runner executes.

The synthetic complete commissioning approval is used only in validation calls, never in a commissioning constructor. Actual command execution uses a manufactured fixture with the same implementation checks. The source files, authority checker, manifest, hashes and assertions were not modified. This is a narrow actual-call-site/version mismatch under the explicitly requested in-memory substitution audit; it does not assert general security against arbitrary owner edits or loaded-native-code tampering.

**Smallest closure:** bind and recheck the actual controller callables used by Run, or use one immutable/checked dispatch path so the checked identity and invoked function cannot diverge. Include a same-display-name replacement at the actual runner call site as a consequential negative fixture and preserve the ordinary positive version control. Review other direct controller aliases under the same rule without expanding P's mechanism or controller policy.

## Finding 2 — pending commands and hold durations escape session/restart validation

**MUST-FIX BEFORE COMMISSIONING.** Source: `developmental_ecology/loom_commissioning/authority.py:108–113`; `runner.py:70–75,97–106,135–138,142–161,185–188,197–211`; resume/load at `runner.py:27–35,86–95`. Saved-record coverage gap: `validators.py:83–90,106–108`.

`validate_session()` compares route, resource scope and execution digest. It does not check `held_command`, `hold_remaining`, or their relation to the issued controller decision, original decision index, stage end, or completed native steps. `Run.advance()` trusts those mutable fields. The stage deadline is checked only when `begin_command()` creates a fresh hold; an existing hold bypasses that stage check.

The independent checks establish three levels of consequence:

| Fixture | Observed behavior |
|---|---|
| Change `session['held_command']` after ordinary `begin_command()` | `_guard()` accepts; the next physical native step receives `[-0.5,0.5]` while the recorded decision remains `[0.717668244562803,0.237668244562803]`. |
| Change issued `hold_remaining` from 10 to 11 | `_guard()` accepts; `hold()` executes 11 steps to `0.10999999999999999`, retaining the first-stage command past its `0.1` deadline. |
| Pause after step 7, change pending command and remainder 3 to 4, then save/resume normally | Production `close()` writes the changed session with valid normal checksums. `Run.resume()` accepts it. Four more steps run, ending at index 11/time `0.10999999999999999` with the substituted command and unchanged manifest/route. No receipt, file checksum, or restart hash was edited. |

The explicit `load_restart()` → mutable session → `Run(..., session=...)` route accepts the same substitution. A changed session route, changed live waypoint setting, and changed live resource limit are correctly rejected by independent controls; the pending hold is the omitted part.

This defect also survives the record-validation boundary. Both normal saved segments in the pause case pass unchanged `verify_segment`: the first accepts seven native records; the resumed segment accepts four, including the substituted command beyond the approved stage. The verifier trusts the resumed initial pending command/count and does not establish their continuity with the preceding recorded decision. This is stronger than a fault merely detected after output: the saved and resumed bad continuation is accepted as AV/replayed.

For precision, direct command/count mutations within a single segment are rejected later by replay (`native reconstruction mismatch` / `missing controller decision`). That later rejection does not prevent their world evolution. More importantly, it does not cover the normally saved pause/resume variant above. The supplied `FAULT_RECORD_VALIDATION.json` records both accepted and rejected cases.

The reproduction mutates ordinary exposed controller-session data, just as the delivered live-route mutation fixture does. It does not change engine/body state, rewrite production code, disable checks, or forge a file receipt. Pending command and remainder are the controller's continuing mutable state that §3 explicitly requires to retain the approved execution meaning.

**Smallest closure:** preserve and validate the authorized pending decision, its command, start/native index, issued length and stage/case end; derive or verify the remaining count against progress. Check this invariant before advancement and across save/load/resume, and establish that final pending state agrees with the issued decision and previous segment. Reject a changed command or an enlarged remaining hold before output/evolution. Keep the valid step-7 remainder of three and the unchanged next-stage decision as positive controls. No route tuning or P change is needed.

## Working correction and regression checks

| Classification | Independent result |
|---|---|
| VERIFIED | Exact synthetic complete-spec authorization validates without starting commissioning; the same request bytes are retained throughout the runtime callable fault. The root reviewer separately checks the full semantic substitution matrix. |
| VERIFIED | Direct session-route mutation fails `session route differs from approved procedure` before command/native output. Live named gain mutation fails `controller execution identity mismatch`. Live resource mutation fails `live resources differ from approved scope`. |
| VERIFIED | The correction diff contains no change to P/configuration, adapter, diagnostics, evaluator, sensor UI/HTML or the previous apparatus test file. The primary reviewer owns complete byte/provenance verification. |
| VERIFIED | The earlier independent neural/receiver/leakage script was copied byte-for-byte into this new review directory and rerun against 9d31e790. All four per-family/combined structural poison checks preserve causal hash/RNG. The deliberately late bank restore remains consequential with maximum control difference `0.07729363526569996`. Twenty-nine named transient fields and integral/counter behavior remain correct. |
| VERIFIED | D5 sampling, explicit nonzero receiver equations, start/end raw alignment, formation/packet/delta calculations and representative controller/sensor-copy and metadata isolation match the prior independent results exactly. q norm remains `0.00032818861375509854`; causal reference hash remains `77b57f151a82c52b0e7c49d9a542e1e00e2310545173cab9acf3895c6d4fcca5`. |
| VERIFIED | Pure AV/CO/SO regression rejects SO and falsely relabelled SO, while AV/CO produces only a Jason review request. An in-memory fault removing just the SO guard fails the intended `SO FIREWALL BREACH` assertion (exit 1); the unmodified control passes (exit 0). |
| LIMITATION / EXPECTED PROVISIONAL CHOICE | Loaded native dependencies are inventoried once per process and human compliance with structured procedure prose is not inferred. These declared workflow limits are not the basis of either finding. |
| SCIENTIFIC / COMMISSIONING QUESTION, NOT AN APPARATUS DEFECT | Route competence, deprivation/scientific outcomes, useful learning, survival, capacity and future cache preparation remain outside these manufactured checks. No outcome-driven setting change was made or requested. |

## Reproduction and evidence

All new writes are inside `exports/2026-09-25-p-apparatus-correction-review-9d31e790/authority_runtime`. Each runtime-binding run makes a fresh `components-*` directory there. Each executed physical fixture is at most 0.11 seconds; the declared fixture horizon is 0.2 seconds. No commissioning case, long life, new prehistory, or scientific trial was run. Target code/configuration/artifacts/Git/Workbench were read only.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
$python='C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
$evidence='C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-25-p-apparatus-correction-review-9d31e790\authority_runtime'
& $python -B "$evidence\probe_runtime_binding.py"
& $python -B "$evidence\verify_fault_records.py"
& $python -B "$evidence\independent_checks.py"
& $python -B "$evidence\firewall_regression.py" --fault
& $python -B "$evidence\firewall_regression.py"
```

`probe_runtime_binding.py` exits 0 when its asserted counterexamples and rejection controls reproduce. The fault record verifier reports acceptance/rejection of each saved segment. The firewall `--fault` command is intentionally RED and returns 1; the last command is GREEN and returns 0. None invokes pytest or creates a pytest cache.

Definitive evidence: `RUNTIME_BINDING_RESULTS.json`, `probe_runtime_binding.log`, `FAULT_RECORD_VALIDATION.json`, `verify_fault_records.log`, `independent_checks.json`, `neural-regression.log`, `firewall-RED.log`, `firewall-GREEN.log`, and the review-local manufactured segment files. Runtime-binding probe elapsed 8.51 seconds; record verification 2.06 seconds; neural regression 7.50 seconds.

The complete prior independent HOLD review, latest request, correction report, relevant correction diff and controller/authority/runner/test sources were read. The original design and earlier neural audit remain interpretive context, with current explicit review instructions controlling scope. No closure is inferred merely from the 113-test or 36-pair counts owned by the primary review.
