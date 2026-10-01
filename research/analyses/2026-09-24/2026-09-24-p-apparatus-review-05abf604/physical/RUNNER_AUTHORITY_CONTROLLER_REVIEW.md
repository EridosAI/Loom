# Independent runner, authority and physical-controller review

Reviewed checkpoint: `05abf60401d08f38750bca589b1c040e10513d7b`.
Verified direct parent: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.
Date: 2026-09-24. This is a bounded apparatus subreview, not commissioning.

## R1: authority/controller/plan binding — MUST-FIX BEFORE COMMISSIONING

**The same execution grant accepts a different controller/arm, and the prescribed route is outside the bound execution contract.**

`developmental_ecology/loom_commissioning/contract.py:90–95` accepts only five authority fields and compares only `approved_case`, `approved_initial_state` and `approved_duration` to the manifest. It then hashes the request file. It does not bind the approved mode/controller to the manifest, nor compare a complete approved execution-contract identity. The current code's manifest validation at lines 47–65 correctly checks current P, configuration, apparatus, initial clock, field and all-state identities; these checks do not establish that the selected arm/controller is the one approved in the request.

Independent reproduction used a **manufactured, explicitly non-authorizing request fixture**, whose preserved bytes describe one external waypoint arm. Both `validate_manifest` and `authorize_execution` accept its matching baseline. Reusing exactly the same request bytes and authority dictionary also accepts each of:

| Changed manifest mode | Changed controller | Result |
|---|---|---|
| `external_controller` | `sensor_human` | Accepted |
| `external_controller` | `manual_privileged` | Accepted |
| `intact_P` | `none` | Accepted |
| `FIXED-STRUCTURE / NO-LASTING-PLASTICITY DIAGNOSTIC` | `none` | Accepted |

No commissioning `Run` was constructed with this fixture; the reproduction calls validation only and advances zero native steps. This is a missing workflow binding, not a demand for cryptographic authentication or resistance to a malicious machine owner. An operator can accidentally reuse a valid grant with the wrong otherwise valid execution mode.

The route also enters through `Run(..., plan=...)` at `runner.py:42`, is copied into `session['route']` at line 59, and controls the commands at lines 99–103. It is absent from `make_manifest` (`contract.py:34–42`). Two zero-step manufactured constructions with the **same manifest hash** `7aee6631cda1a138d3b1e6b3383530fb47a0a7e23b8bcda947417b70e2c34bdc` but prescribed points `[6,5]` and `[4,5]` produced respectively `[0.717668244562803, 0.237668244562803]` and `[-0.5, 0.5]`. The differing plans and commands are recorded, but the grant cannot distinguish them. This matters to the design's prospective exact start/path/phase and controller authorization boundary; no route competence claim is needed to demonstrate it.

**Smallest closure:** bind the grant to a canonical complete execution contract containing the reviewed apparatus/P/configuration identities, complete initialization/phase/history identity, case, mode/controller, prescribed route or controller-plan identity, and duration/absolute deadline. Validate the supplied plan against that contract before output creation. Add consequential wrong-arm/controller/plan rejection tests using unchanged approval bytes and matched positive controls. Preserve the current P runtime/configuration. No fix was made here.

Do not overstate the failure: wrong current P code, configuration, apparatus dictionary, initial-state hash, case, duration and authority-file hash were independently rejected. This review did not demonstrate a bypass of those current identity checks. The missing complete grant identity is what prevents approval from being bound to the complete selected instrument.

Evidence: `RUNNER_AUTHORITY_RESULTS.json`, `RUNNER_AUTHORITY_CONSOLE.txt`, `probe_runner_authority.py`, and `MANUFACTURED-AUTHORITY-NO-EXECUTION.json`.

## Extended runner and stop/state boundaries — VERIFIED

The direct intact path is `runner.py:131` → `adapter.py:87–88` → the original `Engine.step`. The old bounded runner is not called. The new runner enforces the immutable manifest hash and fixed absolute deadline at `runner.py:84–92,116–120`, then closes at exhaustion at line 153. External/fixed adapters use the unchanged physical/field operations and retain the original terminal-location ordering (`adapter.py:68–119`).

Independent manufactured components reproduced:

| Component | Observed result |
|---|---|
| Two waypoint command holds, 20 native steps | Exactly 20 field calls at 0.01 s; external inactive neural/RNG state unchanged |
| Pause after native step 7 | Original command, route, cursor and 3 remaining held steps survive restart |
| Resume first interrupted hold | Ends at native index 10; subsequent hold ends at index 20 |
| Pause/resume versus continuous execution | Complete engine state hashes equal at `0.20000000000000004` s; original deadline remains 0.2 s |
| Display during pause | Three display reads leave the complete engine state unchanged |
| Manufactured 31.99 → 32.00 boundary | One original `Engine.step`, one native neural update, one field update, one due wave; one E and one I exploratory draw |
| Manufactured 0.49 → 0.51 noise boundary | Two native steps; exactly one motor-noise refresh draw |
| Manufactured partial terminal at index 19 | Energy terminal at `0.1933333333581686` s; elapsed `0.0033333333581685998` s, one native record, no wave or body-wave sample, inactive neural/RNG unchanged |
| Manufactured 1199.99 → 1200.00 boundary | One native step, administrative cutoff, expected native-120000 restart snapshot |
| Complete cutoff or terminal resume | Rejected before a new output directory |
| Injected apparatus failure before physics | `apparatus_failure`, `complete=false`, native index 0; resume rejected |

All seven substantive saved segments from these probes independently pass the delivered exact replay/ledger verifier; the split hold contributes three segments and the four boundary checks contribute four. The verifier is production arithmetic, so this establishes preservation/reconstruction and scheduler agreement rather than a second independent physical-law proof. The largest accounting residual in these components is `5.439645587267117e-17`.

The restart wrapper serializes both complete engine and session (`runner.py:15–32`), including held command/count, route/cursor, sensor state, frozen structure where present, resource-use counters and the original manifest/deadline. `Run.resume` requires a complete administrative pause, verifies prior file hashes and the final restart contract (`runner.py:74–82`). Failure and terminal records are not treated as pauses.

A genuine 1200-second commissioning manifest was validated against the existing lawful life-0 prehistory through read-only cache loading. Its absent authority was rejected before output creation; the engine state hash and native index 0 were unchanged. **No 1200-second life, new cache or commissioning trajectory was run.**

Evidence: `RUNNER_AUTHORITY_RESULTS.json`, `BOUNDARY_CLOCK_RESULTS.json`, scripts/consoles and their export-local manufactured record directories.

## Privileged controller capability boundary — VERIFIED

`controllers.py:9–35` implements the reviewed privileged allowlist and copies/converts arrays and nested fixture/contact values into detached data. Material/source tags are removed; geometry identity is permitted for this privileged controller. Its callable receives data, a fixed plan and a cursor, not an engine/world object. Its only actuator output is a finite two-element pair bounded to [-1,1] (`controllers.py:38–41,43–69`). It cannot directly set body, field, stocks, contact, repair or damage through that interface.

Independent mutations of returned position, velocity, reserves, commands, stocks and nested disk/rectangle coordinates left the original complete engine hash unchanged. A forbidden `neural_q` key is rejected. The live call additionally copies the controller input (`runner.py:101–102`); intact P never invokes this privileged controller. External trajectories are explicitly labelled and have the inactive newborn neural state removed from causal command production (`runner.py:134–139`, `adapter.py:70–74,85–93`).

The controller's heading gain 0.8, angular damping 0.2, distance gain 0.5, speed damping 0.4, force correction 0.4 and drive/turn bounds 0.5 are fixed literals (`controllers.py:61–67`). No result/evaluation/tuning input or configuration writer exists in that controller function. Its clock selects prescribed external route stages; it is not supplied as an extra P input. Historical absence of tuning is supported by the inspected construction record rather than provable from source alone.

## R2: nominal controller deadline — MUST-FIX BEFORE COMMISSIONING

The disclosed simple route controller compares floating world time to `until` with exact `>=` (`controllers.py:55,68`). In the same two-hold fixture, ten native increments produce time `0.09999999999999999`, while the first route entry has `until=0.1`. Thus the second ten-step decision remains at cursor 0 and produces `[0.6958934252903155, 0.23474350126270044]`. A detached calculation with the same copied input but time exactly 0.1 selects cursor 1 and produces `[-0.3577907305552408, 0.6422092694447592]`.

The difference `1.3877787807814457e-17` seconds therefore delays the declared route transition by one complete 0.1-second command decision. A second detached check makes the deadline consequence unambiguous: using that same saved input and a **single final entry** ending at 0.1, the actual controller still returns `[0.6958934252903155, 0.23474350126270044]`, whereas the identical input at exactly 0.1 returns `[0,0]` under `controllers.py:68`. The nonzero pair is eligible for all ten next held steps through `runner.py:109,159–162`.

This is a consequential discrepancy in the prescribed point/wait/press controller (`controllers.py:43–47`), not an untried route-navigation failure. Native time advances on the specified 0.01-second lattice. A representation difference far below the existing event-time tolerance should not change whether the controller's nominal due time has arrived and issue an entire additional command block. The defect affects planned wait/stop/route timing independently of the physical or scientific success of the route. It does **not** bypass the separate absolute manifest deadline, alter P's native/wave schedule, or misrecord the actual command.

**Smallest closure:** make the due-time comparison for route progression and final stopping consistent with the existing native/command cadence and existing numerical timing tolerance, without changing P, gains or force targets. Add a matched regression at a represented native boundary where the accumulated clock lies just below the nominal time; require the due transition/final stop, the unchanged ten-step hold schedule, and continued pause/resume equivalence. No controller competence or new commissioning trajectory is needed to close it.

Evidence: `ROUTE_BOUNDARY_RESULTS.json`, `ROUTE_BOUNDARY_CONSOLE.txt`, `probe_route_boundary.py`, `FINAL_UNTIL_RESULTS.json`, `FINAL_UNTIL_CONSOLE.txt` and `probe_final_until.py`. These follow-ups only read existing manufactured records and evaluate a controller function; they add zero world steps.

## Controller competence and long-run behavior — SCIENTIFIC / COMMISSIONING QUESTION, NOT AN APPARATUS DEFECT

No A1–A5 navigation, recovery, gentle-contact or circuit competence is required or claimed by this review. Long-duration behavior, natural terminal lives, birth-specific field caches, controller witness success and efficacy remain later execution questions. They are not additional reasons to HOLD.

## Scope, sources and reproduction

Read the complete commissioning design and matrix, plain-language walkthrough, configuration-change rules, decisions-required document, current-state orientation, apparatus build report, relevant complete runtime modules and the apparatus tests. The earlier final P engineering review remains the engineering baseline. The design's controller/path authorization and no-rescue rules are review requirements; route success, long lives and birth-specific caches are future execution questions. Root coordinates complete diff/provenance, final suites, fixed diagnostics and information-isolation subreviews.

All new outputs are under this `physical` export. No target code, configuration, artifacts, Git, Workbench or source file was edited. No A1–A5/B1–B4/C1/C2 execution, efficacy experiment, tuning, new prehistory or freely acting long trajectory occurred. Read-only cache initialization creates an inert engine only. Manufactured steps match the already authorized fixture class and last at most 0.2 seconds each. No general security proof or exhaustive timing/contact-space claim is made.

Exact reproduction on the reviewed host (copy scripts to a **fresh** workspace folder first; their output paths are relative to their own locations):

```powershell
$python = 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
$review = 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-24-p-apparatus-review-05abf604\physical'
$fresh = Join-Path $review ('rerun-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $fresh | Out-Null
Copy-Item -LiteralPath "$review\probe_runner_authority.py","$review\probe_boundary_clocks.py","$review\probe_route_boundary.py","$review\probe_final_until.py" -Destination $fresh
$env:PYTHONDONTWRITEBYTECODE = '1'
& $python -B -X utf8 "$fresh\probe_runner_authority.py"
& $python -B -X utf8 "$fresh\probe_boundary_clocks.py"
& $python -B -X utf8 "$fresh\probe_route_boundary.py"
& $python -B -X utf8 "$fresh\probe_final_until.py"
```

Both initial probe processes and both detached follow-ups completed without assertion failures. Positive authority validation is deliberately not execution authorization: the manufactured request is labelled **NO EXECUTION** and is never passed to a commissioning `Run`.

Subreview disposition: authority/controller/plan binding and the demonstrated nominal controller-deadline defect require closure before commissioning. No other material runner/physical-controller defect was found within this bounded scope.
