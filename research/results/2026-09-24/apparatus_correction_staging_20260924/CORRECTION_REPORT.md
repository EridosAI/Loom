# Loom P apparatus: two-finding corrective pass

Date: 2026-09-24. **Builder verification complete; stop for independent review.** This report does not declare the apparatus fit for commissioning. P remains scientifically uncommissioned and untested.

Previous apparatus checkpoint: `05abf60401d08f38750bca589b1c040e10513d7b`. Unchanged P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. The new local checkpoint and exact binary diff are identified by the portable package's `CHECKPOINT.json` and `CORRECTION.patch`. Worktree: `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405`; existing branch: `build/p-commissioning-apparatus-20260924-01a0c405`.

## Scope and controlling sources

Only independent review findings A-R1 (complete execution approval binding) and A-R2 (stage deadline comparison) were corrected. The complete `LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md`, physical subreview, exact authority/route/final-deadline probes and their saved records control this pass. Exact copies and Jason's corrective request are in `developmental_ecology/artifacts/apparatus-correction-20260924-01a0c405/references`. The commissioning design §4.1 requires 0.1-second command holds with 0.01-second mechanics; A-R2 requires preserving ten-step holds and pause remainders. Current Workbench orientation records the independent HOLD; this correction does not rewrite that record or confer independent closure.

The scoped writes and tests ran on the actual Windows desktop, using local Git 2.50.0.windows.1 and the existing Python 3.13.5 environment (NumPy 2.3.3, SciPy 1.16.2, pytest 8.4.2). A harmless create/read/delete check passed inside the new correction evidence directory. Writes outside the project mirror used the approved scoped execution mechanism. No dependency installation, cloud substitute, vault Git write, remote operation or unattended simulation was used.

## A-R1: before and after

Before: the grant named a case, initial-state hash and duration, and checked request-file bytes. It did not compare the approved arm/controller or any full execution digest. The route entered `Run(..., plan=...)` separately. The exact original review reproduction was rerun against unchanged 05abf604: the same synthetic request and grant accepted sensor-human, manual-privileged, intact-P and fixed-structure substitutions. Zero native steps and zero commissioning constructors occurred. `old-05ab-authority-RED.log` preserves the reached failure.

After: manifest schema 2 includes an explicit `execution` object. SHA-256 covers canonical UTF-8 JSON with sorted keys, compact separators and finite numbers, over **every manifest field except the self-referential `execution_authority`**. The grant must name that digest. The byte-hashed request must itself contain both the same digest and the complete readable approved object. Updating only a grant's digest cannot change the request's approved contents. This preserves the old case/state/duration checks rather than replacing them.

The bound contents are:

| Part | Included contents |
|---|---|
| Apparatus and P | Schema, exact baseline commit, all P module aggregate identity, all apparatus Python/HTML file identities, configuration identity |
| Runtime | Python version/implementation, executable hash, Python DLL hashes, platform; installed NumPy/SciPy versions and deterministic content hashes of .py/.pyd/.dll/.so plus distribution METADATA/RECORD |
| Case and arm | Exact case ID, purpose, mode, controller kind, adapter source identity and intervention label |
| Controller | Source identity, live Python function-code identities, unchanged named gain/bound/force/epsilon constants; distinct privileged, manual-fallback and sensor-only interface identities; sensor UI source/HTML identity |
| Procedure | Exact ordered point/until/press-force route; procedure kind and structured protocol record where applicable. Non-waypoint commissioning requires its explicit structured protocol |
| Initialization | Complete initial-state hash, initial time/index, field-array hash, phase, complete prehistory/cache provenance |
| Scope | Duration, absolute deadline, command-hold cadence, wall-time/storage limits, fixed diagnostic selection and birth roster |
| Display intervention | Explicit implemented `none` identity. An unimplemented deprivation label is rejected; this pass builds no deprivation adapter |

`RUNTIME_FILE_IDENTITIES.json` exposes the dependency file membership and individual hashes behind the runtime aggregates. An example synthetic approved object is packaged separately and prominently marked **NOT JASON AUTHORIZATION / NO EXECUTION**. Neither this report nor that example authorizes a case.

The constructor validates the manifest, request binding, supplied route, resource limits and observer identity before opening the recorder. Route and resource identity are checked in saved sessions, on restart and before advancement. Live controller constants/functions are checked against the manifest. A changed route cannot enter via the old separate `plan` argument or mutable session route. A saved cursor cannot select another route stage: decisions derive the stage from approved times. Manual fallback, sensor-human operation and fixed structure have distinct identities and cannot inherit a waypoint grant. Only the existing passive observer is accepted at construction; observation algorithms were not changed.

This is an auditable local workflow boundary, not cryptographic authentication of Jason or protection against the owner editing the runtime. Runtime dependency bytes are inventoried once per process; hot modification of loaded native code is outside that guarantee. Human compliance with the approved structured procedure remains an operator obligation; this code does not infer the meaning of arbitrary protocol prose.

## A-R2: exact reproduction and correction

The unchanged 05abf604 run used the review's saved input and produced time `0.09999999999999999` after native step 10. A deadline of `.1` differed by `1.3877787807814457e-17` seconds. Its old stage returned `[0.6958934252903155, 0.23474350126270044]`, eligible for another ten steps. The identical input at exactly `.1` selected the next stage and returned `[-0.3577907305552408, 0.6422092694447592]`. A single final stage also kept driving instead of returning zero. `old-05ab-clock-RED.log` preserves this original failure before edits.

The sole boundary comparison now treats `now >= deadline` or an absolute difference within the **existing** P `event_time_tol=1e-10` as due (`rel_tol=0`). It applies to both stage progression and final stop. P time, dt, physical tolerances, gains and hold duration were not changed. World time is never rounded or reset. The saved input now selects cursor 1 and the exact-boundary command; its final-stage calculation returns `[0,0]`. See `EXACT_CLOCK_GREEN.json`.

**Remaining-duration rule:** a completed stage cannot start another hold. At a due intermediate boundary, transition before calculating the next hold. At the final boundary, `Run` refuses another hold without advancing or recording a command. A full prescribed hold that would cross an interior stage deadline is rejected before command recording; it is not shortened, allowed to overshoot or compensated later. This fail-closed unsupported-prescription check preserves the design's ten-step hold requirement rather than inventing a partial-stage scheduling policy. The pre-existing global deadline may still truncate a final case hold, and a native terminal event still stops physics normally. Routes requiring a new partial-stage policy need a separate ruling; no planned route was changed or commissioned here.

An immediately preceding representable value such as `nextafter(.1, -infinity)` is the same nominal native decision boundary within the declared tolerance, so it transitions/stops. `.09` and `.1 - 2e-10` remain not due. Test expectations use an independent Decimal/integer-native-tick oracle and explicit interval ownership `[0,10)` / `[10,20)`, not the production comparison.

## Verification and consequential evidence

| Verification | Result |
|---|---|
| Original 05abf604 counterexamples | Two reached RED failures, before runtime edits; validation/detached calculations only |
| Existing fault matrix, unchanged script/tests | All 16 intended REDs followed by 16 GREEN controls |
| New complete-approval faults | 18 intended REDs followed by 18 exact-object GREEN controls |
| New clock faults | Transition and final-stop comparison restored to old behavior: two intended REDs followed by two GREEN controls |
| Final complete worktree suite | **113 passed**: 59 unchanged P + 24 unchanged apparatus + 30 new correction cases |
| Final complete portable suite | **113 passed**; see packaged `portable-suite-001.log` |

The new authority pairs cover implementation, constants, route, ordered stages, contact target, manual fallback, sensor interface, intact arm, fixed adapter, deprivation, initial state, prehistory, duration, resources, runtime, procedure, another compatible arm, and attempted grant-digest rebinding without changing request bytes. Their RED mode isolates the complete-binding guard so an older case/duration guard cannot make the check pass vacuously. Full constructor controls also reject before recorder creation; accepted synthetic authority objects are only validated, never used to construct a commissioning run.

The clock pairs restore the old comparator in detached calls. Additional GREEN tests verify exact/adjacent/effectively-at boundaries, clearly-not-due controls, rejection of a crossing hold, live program/resource mutation rejection, and pause/resume at indices 7 and 10. The step-7 route retains three steps, then transitions at native step 10. Both resumed paths equal their continuous counterpart through native step 20. Each measured continuous path has exactly twenty .01 field calls, unchanged inactive neural/RNG state, no neural wave, and two ten-step command records. Global cutoff prevents further steps. A final-stage boundary resume cannot gain any hold.

All subprocesses disable plugin autoload and pytest cache, use `-B`, explicit source roots and fresh temporary roots. The portable run uses only the assembled code and its explicitly packaged verified life-0 cache. No new prehistory was prepared. Existing failed-development and earlier successful evidence is retained; final matrices are in `existing-faults-final-002` and `new-faults-final-002`. The initial identity-audit assertion incorrectly compared CRLF test checkout bytes directly with LF Git blobs; the corrected audit compares Git's unchanged checkout projection, with both hashes disclosed. No source was normalized to make the audit pass.

## Preservation and exact change boundary

All 13 P modules are byte-identical to their 6bc9683b Git blobs; aggregate SHA-256 is `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9`. Configuration remains byte-identical to the baseline Windows checkout: `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9`; its unchanged semantic identity is `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`. Raw Git configuration is LF and the checkout is CRLF; both identities are retained. All original P tests and the original apparatus test/fault-runner files retain their baseline representations.

The historical `EXP1-21` tree remains `f1b884a7ada4c806786d1530d76d446aac5d37b1`. All 792 previously inventoried P artifacts match their hashes. The new before/after inventory also checks 1,908 pre-existing apparatus/review/design/package files. Original checkpoint/package, prior fault evidence, design and reviews are preserved. The original builder ZIP remains at Jason's supplied Workbench INBOX location and is included byte-identically as a historical archive in this package; SHA-256 `87f4dbde39a72559caf6045c7ac68a649d9691a000d1569af5d26b090a63b053`.

Runtime changes are limited to `loom_commissioning/contract.py`, `controllers.py`, `runner.py`, and new `authority.py`. New tests, one extracted exact input fixture, a fault runner and this correction documentation accompany them. Adapter, diagnostics, evaluator, initialization, validators, UI, P and configuration are unchanged. Schema-1 records intentionally remain associated with their original runtime/package; they are not silently upgraded or rewritten.

## Remaining limits and what was not tested

Independent closure is still required. No commissioning grant has been issued, no case selected, and no commissioning trajectory launched. The execution receipt audit contains only manufactured fixture records. Short test timings are not a new commissioning throughput/storage estimate; hashing/guard overhead at lifetime scale is unmeasured.

Not tested: A1–A5, B1–B4, C1/C2; 600-second lives; long lifetimes/cohorts; navigation/contact competence; efficacy, learning, survival, useful association/credit; tuning/sweeps; new prehistory or births 1–4; new display deprivations; new controller policies; fresh dependency installation; other operating systems; long-run storage/performance; new GUI appearance/double-click operation. No experiment number, preregistration, scientific reinterpretation, push, PR, merge, canonical Workbench edit or P/world-law change occurred.

The unchanged double-click sensor launcher opens an inert saved view: `developmental_ecology/Open Paused Sensor Reference.cmd`. The separately named privileged review remains for evaluators. Neither is an execution interface for this corrective pass. Stop here for independent review.
