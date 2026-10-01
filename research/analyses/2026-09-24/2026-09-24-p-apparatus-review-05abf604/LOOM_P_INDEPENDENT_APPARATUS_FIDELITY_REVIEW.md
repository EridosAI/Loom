# Loom P commissioning apparatus — independent fidelity and safety review

Date: 2026-09-24. Apparatus checkpoint: `05abf60401d08f38750bca589b1c040e10513d7b`. P scientific checkpoint: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.

**HOLD BEFORE COUPLING COMMISSIONING**

Two apparatus defects require narrow correction: the execution grant does not bind the approved arm/controller or prescribed route; and ordinary floating-point clock accumulation can make a waypoint deadline miss a complete ten-native-step command hold. Neither finding changes the prior fidelity disposition of P or says anything about P's scientific efficacy. Both are reproduced below without executing a commissioning case.

The substantial remaining checks passed: P/configuration/original tests are unchanged; the worktree and exact portable payload each pass 83 tests; all 16 delivered deliberate faults fail at their intended checks and their controls pass; independent frozen-state poison and receiver calculations pass; sensor isolation and the SO firewall are consequential; saved manufactured records reconstruct exactly; all 792 prior artifacts are preserved.

No target code, configuration, artifact, Git state or Workbench file was modified. No fix, push, PR, merge, rebase, new prehistory, A1–A5/B1–B4/C1/C2 execution, 600-second life, tuning, or scientific trial was performed. New outputs are confined to this independent review export. The synthetic authority document is a validation input explicitly marked **not Jason authorization**; it was never used to construct or advance an authorized commissioning run.

## Concise closure table

| Area | Classification | Independent result / required closure |
|---|---|---|
| A-R1: execution approval binding | **MUST-FIX BEFORE COMMISSIONING** | Same request bytes/grant accept four substituted arm/controller combinations. Different routes share one manifest but produce different commands. Bind approval to the complete immutable execution contract, including route/controller settings; reject mismatches before output. |
| A-R2: prescribed controller deadlines | **MUST-FIX BEFORE COMMISSIONING** | Native step 10 ends at `0.09999999999999999`; an `until=.1` transition is missed and the old stage commands another ten steps. Make due-time comparison robust to native-clock rounding and add the exact regression. |
| P/configuration/prior engineering tests | **VERIFIED** | No P or configuration edit; all previous 59 checks remain unchanged and green. |
| Extended runner, native/wave/noise/field timing | **VERIFIED** | Original `Engine.step` for intact P; explicit deadline; manufactured above-30-second and 1,200-second endpoint checks; no long life executed. |
| Pause/restart and command holds | **VERIFIED** | Pause at step 7 preserves three remaining hold steps; resumed and continuous final states match; terminal/cutoff/incomplete failure resume rejected. |
| Privileged controller capability boundary | **VERIFIED** | Copied closed inputs, deterministic bounded two-command output, no world mutation or P input contamination. Approval binding and deadline exceptions are A-R1/A-R2. |
| Sensor-only interface | **VERIFIED** | 10/4/8/7 raw coordinates, held actual E/I, own history; no privileged routes/payloads; inspection is inert; privileged exceptions concealed. |
| Fixed-structure adapter | **VERIFIED** | Exact frozen list and restoration order; per-field poison causes no subsequent causal/RNG difference; late bank restoration fails consequentially. |
| AV/CO/SO firewall | **VERIFIED** | SO and dishonest SO relabelling rejected; AV/CO yields a Jason review request only; deliberate removal of SO guard reaches the independent breach assertion. |
| D5 and aligned records | **VERIFIED** | Fixed index/every-handoff selection; independent nonzero receiver equations and omissions; no live state/RNG changes; input/end timestamps distinguished. |
| Saved three-mode reconstruction | **VERIFIED** | All nine saved segments reconstruct; 120 native records including pause/continuous duplicates, 60 distinct continuous-path native records; final neural/field states exact. |
| Worktree / portable suites | **VERIFIED** | `83 passed in 34.04s` / `83 passed in 33.46s`. |
| Delivered RED→GREEN matrix | **VERIFIED** | All 16 intended REDs and 16 clean controls independently reproduced. |
| Prehistory / roster | **VERIFIED** | Life-0 cache rejects births 1–4; roster preserved unstarted; no cache preparation. |
| Package, sources, historical artifacts | **VERIFIED** | Original ZIP located in user-supplied Workbench inbox; all 220 payload identities match; 792 prior artifacts preserved; exact ancestry and historical tree checked. |
| Long-run performance / finite coverage | **LIMITATION / EXPECTED PROVISIONAL CHOICE** | 37.7447 h / 43.0187 GB are short-fixture extrapolations only; no long-run calibration. |
| Navigation, positive controls, survival, learning | **SCIENTIFIC / COMMISSIONING QUESTION, NOT AN APPARATUS DEFECT** | Unexecuted and not used as acceptance criteria. |
| Later execution and freeze decisions | **UNRESOLVED / REQUIRES JASON** | No Stage-1 case selected; execution and eventual coupling freeze remain separate decisions after apparatus closure. |

## Review basis and exact identities — VERIFIED

Read the complete five-document commissioning design, matrix, plain-language walkthrough, configuration-change register and decisions-required document; final P engineering review; apparatus build report, law/code/test and authority maps; full 27-file added-only diff; actual code/tests; delivered fault logs; and portable package. The project current-state file was read for orientation and treated as an older snapshot where later committed evidence supersedes it. No scientific decision was inferred from an assistant proposal.

The construction request `APPARATUS_BUILD_REQUEST.txt` expressly accepts the framework for construction with seven rulings. Its D5 ruling supersedes the older design's at-most-100-samples proposal with every handoff where practical and deterministic native selection. That is accepted construction scope, not permission to execute commissioning. The independent review applies the engineering code-review skill and three parallel subreviews: neural/frozen/D5, physical scheduler/controller/authority, and provenance/reconstruction. The coordinating review independently exercises HTTP boundaries, the interpretation firewall and complete suites/fault matrix.

| Identity | Verified value |
|---|---|
| Apparatus commit | `05abf60401d08f38750bca589b1c040e10513d7b` |
| Direct single parent / unchanged P | `6bc9683b54e4fa80136fe8534d7713e2a250a95f` |
| Branch | `build/p-commissioning-apparatus-20260924-01a0c405` |
| Worktree | `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405` |
| P runtime aggregate SHA-256 | `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9` |
| Apparatus aggregate SHA-256 | `5dfe2c85b570d1ee84c83d812d883dd39b8bd6d1ffc3797461b7827463ba5058` |
| Semantic configuration SHA-256 | `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a` |
| Working configuration bytes SHA-256 | `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9` |
| Exact `APPARATUS.patch` SHA-256 | `d4fdf864080d0ee09c8a5a0fdfbd0fc1272722caf0768bc0e88e972f714f5dab` |
| Patch size | 160,506 bytes |
| Original builder ZIP SHA-256 | `87f4dbde39a72559caf6045c7ac68a649d9691a000d1569af5d26b090a63b053` |
| Original builder ZIP size | 5,790,938 bytes |
| Historical EXP1–21 tree | `f1b884a7ada4c806786d1530d76d446aac5d37b1` |

The ZIP was absent at its original receipt path. Jason supplied its actual location: `C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX\2026-09-24-p-commissioning-apparatus\Loom_P_Commissioning_Apparatus_Review_20260924.zip`. Its bytes match the original receipt; 221 archive members, including 220 inventoried payload files, pass hashes/size/CRC checks. Every archive member matches the assembled folder and the independent portable test copy. The location change is resolved custody information, not a missing-package finding or a rebuilt archive presented as the original.

Pinned environment actually used: Windows desktop Python 3.13.5, NumPy 2.3.3, SciPy 1.16.2, pytest 8.4.2 from the existing engineering virtual environment. No dependency installation occurred. Exact file/source/runtime identities are in `provenance/IDENTITIES.json`, `GIT.json`, `SOURCES.json`, `ZIP.json` and the nested builder checkpoint.

## A-R1 — approval does not bind the complete execution contract

**MUST-FIX BEFORE COMMISSIONING.** Primary code: `developmental_ecology/loom_commissioning/contract.py:90–95`; associated route omission: `contract.py:34–42`, `runner.py:42–59`, `runner.py:98–101`.

`authorize_execution` accepts a five-field authority object. It compares only approved case, initial-state hash and duration, then verifies the bytes of an arbitrary supplied request file. It does not compare the approved arm/controller with the proposed arm/controller or verify an approved full-contract digest. The route is not part of the manifest at all; `Run` receives `plan` separately and saves it in mutable session state. Manifest validation checks that the selected mode/controller combination is internally legal, which does not establish that it is the combination approved by the request.

The independent fixture constructs a validation-only request explicitly naming `external_controller` / `waypoint`, the full proposed manifest and prescribed route. It reuses exactly the same request bytes, SHA-256 and authority object. Both `validate_manifest` and `authorize_execution` accept each of:

| Substituted mode | Substituted controller | Result with unchanged request/grant |
|---|---|---|
| `external_controller` | `sensor_human` | Accepted |
| `external_controller` | `manual_privileged` | Accepted |
| `intact_P` | `none` | Accepted |
| `FIXED-STRUCTURE / NO-LASTING-PLASTICITY DIAGNOSTIC` | `none` | Accepted |

No commissioning `Run` was constructed for these variants and no native step occurred. This is a scoped workflow counterexample, not an attempt to defeat authentication or defend against an owner editing the program.

The route omission is independently causal. Two manufactured constructors receive the same manifest SHA-256 `7aee6631cda1a138d3b1e6b3383530fb47a0a7e23b8bcda947417b70e2c34bdc`, but plans pointing to `[6,5]` and `[4,5]` produce respective first command pairs `[0.717668244562803, 0.237668244562803]` and `[-0.5, 0.5]`. Only command calculation occurs: both remain at native index 0. Thus a case/initial-state/duration triple is insufficient to identify the approved intervention.

Controls reject changed case, duration, initial state, P code, configuration, current apparatus identity and authority-file hash. The verified initial-state hash covers the actual phase/fields/neural/body/RNG state, and history validation checks the cache. Those working controls do not close the arm/controller/route hole. Likewise, pinning the currently installed apparatus version does not tie that version to what a particular prior request approved.

**Smallest closure:** represent the approved execution contract in the authority mechanism, excluding only self-referential grant fields, and compare its immutable digest or equivalent complete explicit fields before output creation. Include exact apparatus/P/configuration identity, complete initial state/phase/prehistory, case, arm/controller, prescribed route and relevant controller settings, duration and absolute deadline. Preserve this binding across restart. Add consequential rejection tests for valid-but-unapproved arm/controller/route substitutions while the legitimate grant remains byte-identical, plus matching positive controls. No P law, parameter or scientific protocol expansion is needed.

Evidence: `physical/probe_runner_authority.py`, `RUNNER_AUTHORITY_RESULTS.json`, its console log and explicitly synthetic request file.

## A-R2 — a nominal route deadline misses a complete command hold

**MUST-FIX BEFORE COMMISSIONING.** Code: `developmental_ecology/loom_commissioning/controllers.py:55–56` and `:68`; ten-step consequence: `runner.py:109` and `:159–162`.

The deterministic controller advances to the next fixed route entry when `data['time'] >= plan[cursor]['until']`; after the final entry's deadline it zeros drive/turn. The actual native clock is accumulated in binary floating point. After ten 0.01-second steps, the ordinary saved decision input is `0.09999999999999999`. A prescribed `until=.1` therefore remains not due, although the native decision boundary is 0.1 seconds to all relevant simulation tolerances.

The independent check uses the **same saved manufactured controller input**, changing only the representation of that time to exact `.1` in a detached calculation. No new trajectory is needed. With a first point `[6,5]` until `.1`, followed by `[5,6]` until `.2`, actual input retains cursor 0 and commands `[0.6958934252903155, 0.23474350126270044]`; exact-boundary input advances to cursor 1 and commands `[-0.3577907305552408, 0.6422092694447592]`. The difference of `1.3877787807814457e-17` seconds causes a materially different command held for **ten further native steps**. The same issue applies to the final-entry stop: the saved input yields continued drive while exact `.1` yields `[0,0]`.

This is an executable discrepancy in the prescribed controller's command-decision timing, independent of whether an untried route can be navigated. It can extend a declared wait/contact/drive stage and defeats interpreting the prescribed schedule literally. Native/world timing itself is unchanged; the defect is the external controller's deadline comparison.

**Smallest closure:** make due-time comparison consistent with the declared native/decision clock and existing numerical tolerance, for both entry advancement and the final-entry stop. Add the exact accumulated-clock boundary regression and a clearly-not-due control so the correction does not broadly trigger stages early. Preserve ten-step holds, pause remainder, fixed gains, P runtime and configuration; rerun the affected controller and portable suites. This requires no route search, competence criterion or outcome tuning.

Evidence: `physical/probe_route_boundary.py`, `ROUTE_BOUNDARY_RESULTS.json`, saved `hold-continuous/controller.jsonl.gz` and the physical subreview.

## Unchanged scientific implementation and complete diff — VERIFIED

The exact parent-to-apparatus diff adds 27 files and changes no existing file. New surfaces are the separate `loom_commissioning` package (adapter, contract, controllers, diagnostics, evaluator, initialization, runner, sensor UI and validators), two inert launchers, apparatus tests/fault runner/packager, and apparatus documentation/provenance. The complete patch was compared with Git and reviewed across the coordinating and specialist passes.

All 13 `loom_p` runtime modules, configuration and all prior P engineering tests are unchanged. Therefore there is no P equation, packet, centring, pooling, associative regime, E/I credit, motor law, body/world law or import-interface edit hidden in this patch. The 8-unit/two-pool baseline, mean-plus-endpoint packet, contracting association and separate bodily credit remain the reviewed scientific object. Existing component checks provide regression evidence; this does not claim a new proof of every old equation.

Intact apparatus advancement delegates directly to original `Engine.step`. External control intentionally bypasses the inactive newborn neural object and records `external_controller`, removing P-neural/action claims from its native record. Fixed structure intentionally intervenes only at the declared restoration points, records the full diagnostic label, and is never relabelled intact P. These declared wrappers are not a silent modification of P's mechanism.

## Runner, deadlines, complete state and stopping — VERIFIED

The runner advances individual native steps with a fixed absolute deadline. It never repeatedly invokes `Engine.run_bounded` to evade the old 30-second cap. The manifest supports positive native-grid durations up to 1,200 seconds. Changing the manifest during a run changes its hash and is rejected; requesting more than remaining native steps is rejected. Restart retains the original deadline.

An existing verified life-0 cache can construct and validate a 1,200-second proposal. Without authority, `Run` rejects it before creating the proposed output directory; engine time/index/state are unchanged. This test is manifest validation and unauthorized-construction rejection, not a 1,200-second life.

Independent manufactured boundary results:

| Component | Observed result |
|---|---|
| Clock 31.99→32.00, native 3199→3200 | Exactly one original `Engine.step`, one neural native call, one due handoff and one field call; one fresh E draw and one I draw. |
| Clock .49→.51 | Two native steps and exactly one due motor-noise refresh. |
| Clock .19 with small manufactured energy | Terminal at `0.1933333333581686`; elapsed `0.0033333333581685998`; no due wave or E/I release; external neural/RNG state unchanged. |
| Clock 1199.99→1200.00 | One manufactured external native step, administrative cutoff and due periodic snapshot. No preceding 1,199.99 seconds were simulated. |
| Command hold interrupted at step 7 | Three steps remain; restored held command, route/cursor, deadline, body/fields/neural/RNG state exact; finish first hold at step 10, next hold at step 20. |

The paused/resumed and continuous external paths have exactly equal final engine hashes, 20 actual field calls and unchanged inactive neural/RNG state. Saved segments reconstruct. Repeated displays before/after pause preserve engine hashes. `Run.resume` rejects terminal and cutoff receipts and `complete=false` apparatus failures before creating resume output. Failure injection produces an honest incomplete failure rather than a death or normal pause. Existing all-mode pause/resume tests add intact and fixed-structure coverage.

Periodic snapshot trigger coverage is a single manufactured endpoint; it does not establish long-series storage performance. These findings concern the native scheduler and stop/resume machinery; A-R1 remains the approval-scope exception and A-R2 remains the external controller's route-clock comparison exception.

## Privileged external controller and sensor-only human boundary — VERIFIED

The privileged input schema contains only position, angle, velocity, angular velocity, actual reserves, delivered commands, exact geometry, mover phase/velocity, stocks, contact normal/force/impulse and clock. Geometry strips material/source annotations. Controller input values and nested arrays/geometry are copied; independent destructive edits to these copies leave the engine hash unchanged. The deterministic route function returns only a finite bounded two-vector plus its cursor, has no engine capability and invokes no hidden physical operation or random stream. Its disclosed gains are fixed code constants, not values selected from survival/learning results.

The actual body receives those commands through unchanged physical, field and transduction operations. No route sets position/velocity/reserves/stock/mover/fields/contact/repair/damage directly. External neural state remains inactive and labelled accordingly. Injected privileged metadata and opposite proposed external commands into intact-adapter calls do not affect intact P's neural/body/field result; intact ignores the external-command argument. Information clock/metadata stays in apparatus paths.

`SensorHistory` supplies only 29 raw coordinates with fixed receptor labels, time/indexed history, held actual E/I, previous commands and operator notes. The sensor HTTP module does not import the privileged evaluator. Its routes are `/`, `/sensors` and the bounded command endpoint; it does not expose files, manifest, restart state or evaluator data. Static saved review uses an offline payload and disabled actuation. The evaluator lives in a separate offline module/output.

The independent live-gateway fixture exercises five repeated HTTP reads before and between decisions, both ten-step holds, invalid command rejection, eight forbidden/file-like routes, copied-data mutation and privileged metadata canaries. Engine hashes establish that deliberation reads add no world time, bodily cost, field update, P clock or random draw. At native 10 and 19, E/I remains the time-0 sample `[.7,.8]`; at native 20 the sample time is .2 and values equal actual body reserves. A deliberately thrown field exception containing a privileged canary yields only the generic paused-command error over HTTP, while the local recorder marks an incomplete apparatus failure. The server is stopped after the probe.

SO notes are preserved in their own stream, absent from the sensor response, and do not change the engine. The same manufactured two-command sequence with/without privileged bookkeeping produces identical causal state after excluding only that deliberately injected bookkeeping field. This is representative executable isolation, not a general operating-system security proof or a guarantee that a human who separately reads privileged files remains blinded. Fresh browser appearance/double-click operation was not independently re-tested; the source/payload and live HTTP isolation are the material evidence here.

## Fixed-structure / no-lasting-plasticity diagnostic — VERIFIED

The complete frozen list matches the design: every sensory cortex's `shared`, `fine`, `shared_ref`, `fine_ref`; association `H` and `use`; regulator `theta` and `reference`. Restoration uses new copies, with no alias to the frozen store. Newborn structural requirements are checked at arm construction. All trajectories carry `FIXED-STRUCTURE / NO-LASTING-PLASTICITY DIAGNOSTIC` rather than `intact_P`.

Native operations use the ordinary old-state right-hand side, then sensory structure is restored before the next native read. Handoff retains packet/context formation, then credit runs with its prior features/perturbation; bank structure is restored **between credit and output**. Association reads old maps/support, output draws fresh controls, hypothetical map/use writes run, and maps/use are restored before their next read. Means, traces, activities, eligibility, body and motor process remain live. Hypothetical operand/update diagnostics are preserved; the applied persistent structural increment is explicitly zero.

Independent poison checks separately alter discarded sensory updates, bank updates, map/use updates, and all of them together. Each correct-restoration result has exactly equal subsequent causal state and RNG, frozen structural identity and no alias. Equality excludes only explicitly observational diagnostic buffers; it retains body, controls, filters, traces, activities, eligibility and random state. Twenty-nine named transient fields change under the disclosed fixture; sensory/motor integrals accumulate and reset at handoff, and native/wave/write counts follow their specified operations.

Deliberately moving bank restoration until after output leaves the structural invariant apparently satisfied but changes later controls by a maximum `0.07729363526569996` and changes subsequent causal state. This is the relevant consequential RED: simply checking final weights would miss the contamination. The delivered discarded-update mutant and independent per-field checks both detect it. No survival or useful behavior enters any assertion.

Evidence: `neural/independent_checks.py`, `independent_checks.json`, `independent_checks-final-002.log`, the detailed neural subreview and the delivered frozen/discarded fault logs.

## Interpretation firewall — VERIFIED

`classify` uses the fixed row/class register. AV and CO can enter `configuration_grounds`; SO cannot. A second check rejects an S-row fraudulently relabelled AV. The result is a request requiring `Jason defect-specific ruling`, with `automatic_adjustment=false`; there is no configuration-writing API. Scientific observations are retained separately, rather than deleted or converted into a pass score. No route in the reviewed implementation uses useful survival, learning, association, sensory differentiation or beneficial credit as a commissioning acceptance test.

The independent test submits synthetic beneficial-survival/credit evidence as S2 and confirms rejection; a valid V1 identity defect and D5 CO observation produce only a review request. It then removes only the SO rejection in memory while retaining class matching. That corrupted path fails the independent assertion `SO FIREWALL BREACH: scientific outcome accepted as configuration grounds` (exit 1); the unmodified control rejects both SO routes and exits 0. This additional firewall pair is separate from the builder's delivered 16 pairs. Evidence: `firewall-RED.log`, `firewall-GREEN.log`, `FIREWALL_PAIR.json`, `reviewer_boundary_probes.py`.

Class registration cannot mechanically infer scientific meaning from arbitrary prose deliberately filed under a false unrelated AV row. Correct human classification remains part of the declared workflow. No semantic authentication claim is made or needed for the tested SO path.

## D5 selection, detached calculations and record alignment — VERIFIED

The manifest fixes every wave handoff and the native rule `native_index % 100 == 0`; motor reconstruction also occurs at every handoff. Selection uses index/handoff existence, never q, regulatory magnitude, error, survival or a result. Independent fixed-index probes select 100/200 and omit 1/99/101, while every handed-off wave is selected. The broader wave coverage follows Jason's explicit construction ruling.

Detached association reconstruction uses the pre-step maps/activity with the recorded new context and old support, reconstructs original q first, then changes one declared sensory-query/support contribution and recomputes its immediate read dependencies. Regulator reconstruction uses post-credit bank state, actual body terms, recorded fresh exploration and need weighting. Motor reconstruction uses prior motor/filter/regulator state and step-start feedback; it reconstructs original command before each omission. Live state and RNG hashes are checked around observer reads. No alternate world is advanced, gain is normalized or P setting is adjusted.

The independent fixture uses nonzero maps and banks, moving-body raw feedback, nonzero motor terms and separate explicit equations. Original q norm is `0.00032818861375509854`. Each body/bias/evoked/learned-bank/exploration omission changes controls; even the small evoked effect is resolved as a numerical influence (`3.0416409509126385e-08` maximum), without being called useful. All six motor omissions change command; direct feedback changes it by `0.00020753983050081012`. Query/support dependencies match independent calculations. Corrupting original receiver output is rejected before influence is accepted. These tests are consequential at nonzero values rather than checking zero newborn maps alone.

Native records independently align step-start raw, old/new receptor mean, residual, x, formation/coarsening/reference pressures, support/opening, weights and applied deltas. Post-physics raw has its own endpoint timestamp and is not substituted for the neural input. Wave records align packets, prior packet means, beta, trace, psi/query, association contributions and separate actual E/I credit. Prior perturbation/features, eligibility, bank learning/reference terms and new controls remain distinguishable. Fixed-arm hypothetical updates and actual zero applied structure remain separately labelled.

An earlier strengthening attempt of the reviewer's motor-omission fixture failed because a stationary manufactured body had exactly zero direct feedback. It is retained in `neural/independent_checks-final.log`, not counted as a production defect or intended RED. The reviewer changed only the manufactured fixture's velocity/omega to make that contribution nonzero; the final independent check passed. Initial/final reviewer logs are preserved.

## Saved reconstruction and observer non-interference — VERIFIED

The independent provenance pass reads the three delivered manufactured modes and each mode's first, resumed and continuous segments. It reconstructs from saved initial state and saved controller inputs, compares complete native/wave/event sequences and final engine/neural/field identities, verifies held E/I against reconstructed transduction, and checks frozen structure. Nine segments contain 120 native records in total because the 7+13-step pause path duplicates each 20-step continuous path; the three distinct continuous paths contain 60 native records. There are four wave records across the duplicated intact/fixed paths, and no external-neural wave.

All three continuous final neural/field states match exactly; joining first and second segment streams matches the continuous path. The independent supplement also reconstructs all 60 saved continuous diagnostic rows byte-exact and directly checks 160 cortical operand rows, including old means, references, residuals and applied increments. Every saved step-start raw differs from its endpoint, so timestamp alignment is exercised rather than vacuous. Both continuous wave records receive separate beta/eligibility/bank-delta checks. Full paused/continuous state equality and controller remainder are independently exercised by the suite and physical probe. Passive diagnostics with/without reads preserve the relevant engine/RNG hashes. Ledger checks preserve source debit/body credit, renewal/expenditure and damage/restoration operands.

The production replay verifier shares original physical/neural arithmetic, so its role is saved-state/record/schedule fidelity. Its diagnostic checks cover counts/checksums; the independent supplement supplies full diagnostic-value reconstruction. It is also supplemented by independent receiver equations, per-field poison, explicit boundary counts and the unchanged P engineering suite. It is not represented as an independent proof of every original physical law. Evidence: `provenance/RECONSTRUCTION.json`, `DIAGNOSTIC_RECONSTRUCTION.json`, `PAUSE.json`, `OBSERVER.json` and their audit scripts.

## All 16 delivered deliberate faults and final suites — VERIFIED

Each RED and GREEN ran in a separate process using the existing pinned environment, no bytecode writes, disabled plugin autoload, no pytest cache and fresh review-local temporary directories. The fault runner's code and the actual traceback/assertion were inspected; a nonzero exit from setup is not accepted as an intended RED.

| Fault | Reached consequential check | Clean control |
|---|---|---|
| `identity` | Manifest/code identity mismatch; independent wrong configuration also rejected | GREEN |
| `missing_native` | Actual missing native record rejected | GREEN |
| `phase` | Wrong field/mover phase rejected | GREEN |
| `ledger` | Positive-transfer debit/credit mismatch rejected | GREEN |
| `input` | Forbidden neural controller input rejected | GREEN |
| `observer` | Actual extra observer random draw changes state and is rejected | GREEN |
| `stop` | Nonterminal state mislabelled terminal rejected | GREEN |
| `sensor_leak` | Actual position key added to sensor row rejected | GREEN |
| `label` | External controller relabelled intact P rejected | GREEN |
| `frozen` | Omitting sensory restoration leaves changed structure and fails | GREEN |
| `discarded` | Late bank restoration leaves later causal/output difference and fails | GREEN |
| `duration` | Changed hard deadline rejected by manifest hash guard | GREEN |
| `extra_updates` | Additional actual field evolution fails field call count | GREEN |
| `extra_native` | Extra neural native update changes inactive external state and fails | GREEN |
| `extra_wave` | Extra neural handoff changes inactive external state and fails | GREEN |
| `extra_random` | Extra actual random draw changes state/counters and fails | GREEN |

All 16 pairs were reproduced as intended. These checks do not cover A-R1's valid-but-unapproved mode substitution or A-R2's route deadline; passing them is therefore compatible with the HOLD findings. Exact child commands, expected messages, exits and timings are in `faults-attempt-001/FAULT_MATRIX.json` and all 32 individual logs.

| Complete suite | Independent observation |
|---|---|
| Exact worktree `tests tests_apparatus` | **83 passed in 34.04 seconds** |
| Verified assembled portable payload `tests tests_apparatus` | **83 passed in 33.46 seconds** |

Both include all unchanged 59 P checks and 24 apparatus test cases. The portable suite ran from a separate workspace copy with `PYTHONPATH` removed; all its source/cache/evidence bytes were subsequently matched to the original ZIP. It does not rely on an ambient old replay directory. The packaged life-0 cache is an explicit verified fixture. The first worktree command used the wrong working directory and failed test collection on a protected Windows profile junction; that log is retained, excluded from counts, and corrected by changing the review command's working directory. No target fix was made.

## Birth roster, prehistory, cost and provenance — VERIFIED

The prospective roster remains births 1, 2, 3, 4 with 600-second ceilings, `execution_authorized=false` and zero-witness interpretation of unresolved opportunity at that coverage. None is executed. The existing life-0 cache is validated by law/dependency/phase/field identity and remains byte-identical. Its phase is `3.558411277237072`, field-array SHA-256 `7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096`, and field archive SHA-256 `f968ed0875d68e3421c5acc9f9a4a218727b9698877b1cc86225d4fec9e6ef7d`. The 60,000-step preparation is historical; this review only loads it.

Attempted loads for birth IDs 1–4 reject this cache as unmatched/incomplete. Their distinct expected phases are retained in `provenance/PREHISTORY.json`. Wrong manifest phase/field/receipt identity is rejected. No future birth-specific cache is inferred from life 0 and none was prepared. Lack of those future caches is an execution prerequisite, not an apparatus-fitness failure.

The three saved 0.2-second component costs/record sizes independently support the arithmetic of the reported projection. The maximum measured fixture rate is 15.16528950000065 wall seconds per simulated second; the maximum stored rate is 4,801,189.999999999 bytes per simulated second. Thus 8960 seconds projects to 37.744720533334956 machine-hours and 43.01866239999999 decimal GB, or 86.03732479999998 GB with one duplicate. The maxima come from different short fixtures. Snapshot/diagnostic startup overhead is included; this is not a steady-state lifetime rate, commissioning result or approved budget. The earlier 11.67 h / 17.66 GB basis remains separately disclosed. Evidence: `provenance/RESOURCE.json`.

Exact commit ancestry, all 13 P module identities, semantic/byte configuration, original tests, full added-only patch and historical EXP1–21 tree are preserved. The 792-entry prior-artifact inventory refers to the completed engineering delivery. All 792 sizes/hashes were checked: 726 accessible directly and 66 protected historical pytest artifacts through scoped read-only access; all match, none is silently omitted. Current apparatus artifact inventory also remains unchanged within the enumerated before/after audit. No remote operation was used to infer local preservation.

All 10 selected source documents match their recorded current identities; all 55 reading copies and 68 design delivery entries were independently verified, anchored to the prior review/builder archives. The current administrative maps reflect subsequent review/design history; their current hashes match this builder's source record. No selected source or canonical decision is silently rewritten by the apparatus diff. Local bytes cannot prove every historical negative process assertion such as no prior push or vault write; that remains a process-observability limit, not an inferred breach.

## Limits and non-blocking questions

**LIMITATION / EXPECTED PROVISIONAL CHOICE:** component and saved-record coverage is finite. Long-run storage/performance, repeated ten-second snapshots over a life, fresh dependency installation, cross-platform bit identity, exhaustive geometry/contact convergence and new browser appearance are not established. Information isolation is verified on representative executable routes, not as an operating-system security boundary against the owner.

**SCIENTIFIC / COMMISSIONING QUESTION, NOT AN APPARATUS DEFECT:** A1–A5 route/contact competence, B1–B4 perceptual outcomes, human positive controls, C1/C2 opportunity, natural terminal lives, 600-second operation, survival, useful learning, capacity adequacy, temporal packet adequacy, association magnitude/usefulness, beneficial credit and innate maintenance remain untested. None is used to justify this HOLD. A-R2 concerns the implemented deadline comparison at an existing manufactured boundary, not the success of a route.

**UNRESOLVED / REQUIRES JASON:** after the two apparatus defects are corrected and independently closed, Jason still selects and authorizes exact commissioning cases, starts/routes/phases, operator controls and resource limits. No approval for Stage 1 or eventual evidential freeze is inferred from this review. No unexpected P mechanism or world-law change was found that needs a scientific redesign ruling.

## Exact closure and portable intake

Close A-R1 with a complete immutable approved-contract binding and valid-but-wrong-arm/controller/route rejection before output. Close A-R2 with numerically faithful due-time comparison and the exact nominal native-boundary regression, including final-entry stop. Keep all P runtime/configuration bytes and previous artifacts unchanged; rerun affected guards/controller/restart checks, all 16 fault pairs and both complete suites on the corrected checkpoint/package. Do not attempt commissioning or efficacy testing to close these engineering findings.

`REPRODUCTION_COMMANDS.md` supplies exact commands. The portable independent intake contains this review/table, the commands, independent probe scripts/results, full 32 delivered fault logs plus the independent firewall pair, specialist reports, relevant manufactured receipts, exact reviewed patch/identities, the review request, and the byte-identical original builder ZIP. Temporary pytest directories are omitted; substantive successful and failed reviewer logs are retained. `FILE_MANIFEST.json`, `REVIEW_RECEIPT.json` and the external ZIP checksum identify this independent package separately.

Prepared for later Workbench intake only. The Workbench itself remains unchanged. Review complete; commissioning remains stopped.
