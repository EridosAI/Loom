# Loom P independent post-correction fidelity review

Date: 2026-09-23. Exact reviewed checkpoint: `f7eb6f27c661e3db193a4225b56a825d7e41739d`.

**HOLD BEFORE COUPLING COMMISSIONING**

The original R1 counterexample is corrected, R2 is closed, and R3's material falsifiers now fail consequentially under deliberate faults. Both independently executed final suites pass all 55 tests. All 3,200 corrected saved neural states and all three final chemical fields reconstruct exactly. Nevertheless, R1 is not fully closed: a deterministic oblique-force variant, with the baseline configuration unchanged, still converts a resolvable release/free-flight/recontact interval into full-duration sustained contact. That is the sole commissioning blocker found in this delta review.

No implementation, configuration, target documentation, target artifacts, Git state, or Workbench content was changed by this review. No new freely acting lifetime, smoke run, prehistory generation, commissioning trial, parameter sweep, or efficacy run was started. New outputs are confined to this independent review export.

## R1–R3 closure table

| Item | Classification | Closure finding |
|---|---|---|
| R1 release/free-flight/recontact | **MUST-FIX BEFORE COMMISSIONING** | Original exact case passes, including duration/accounting and a consequential disabled-release mutant. A new oblique component case still has zero recorded free duration despite separation about 25 times geometric tolerance. See finding R1-P below. |
| R2 final-suite/live-inspector isolation | **VERIFIED** | Worktree and assembled portable suites each pass 55 tests. Live test passes with ambient artifacts present, absent, and poisoned; both the delivered missing-wave mutant and actual live-branch deletion fail at the intended assertion. |
| R3 consequential falsifiers | **VERIFIED** | All nine delivered R3 faults independently observed RED then GREEN; seven additional R3 variants also rejected. All seven requested protections now have executable, consequential checks. |

## Authority, evidence order, and scope

This is a delta review from `d5f7efbe67193f215e52d95ca912db131a79f31c`, not a replacement of the first review's established neural-equation audit. Inputs were the previous `LOOM_P_INDEPENDENT_FIDELITY_REVIEW.md`, previous `docs/developmental_ecology/p_engineering_20260921/BUILD_REPORT.md`, corrected `docs/developmental_ecology/p_correction_20260923/BUILD_REPORT.md`, the corrective portable package, and the actual complete Git diff and runtime files. Builder reports were treated as claims until independently checked. The user's attached post-correction request is included under `review_inputs/`.

The prior source hierarchy and accepted P mechanism remain controlling. The selected source documents are `LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md`, `P_IMPLEMENTATION_AND_OBSERVATION_SPEC_v0_1_REVIEW_DRAFT.md`, `P_PLAIN_LANGUAGE_DATA_FLOW_v0_1_REVIEW_DRAFT.md`, `LOOM_P_SPECIFICATION_HANDOFF_2026-09-20.md`, and `P_SPECIFICATION_DESIGN_REVIEW.md`, together with the accepted pinned world/coupling documents. Their exact identities and preserved representations are recorded in the reviewed delivery and `provenance/IDENTITIES.json`. No proposal in this review is represented as a Jason-accepted scientific decision.

Independent work was divided into physics, falsifier, and provenance/saved-reconstruction subreviews. The primary reviewer independently reran both final suites, checked R2 with two faults, reproduced the remaining R1 failure separately, inspected the complete changed scope, and reconciled the evidence. Numerical observations below come from these executions, not the builder's logs.

## Exact identities — VERIFIED

| Identity | Independently checked value |
|---|---|
| Corrected commit | `f7eb6f27c661e3db193a4225b56a825d7e41739d` |
| Direct single parent / previous reviewed commit | `d5f7efbe67193f215e52d95ca912db131a79f31c` |
| Branch | `build/p-engineering-baseline-20260921-01a0c405` |
| Worktree | `C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405` |
| Semantic configuration SHA-256 | `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a` |
| Working configuration bytes SHA-256 | `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9` |
| Runtime code aggregate SHA-256 | `af53b321220001166b73bc420b67c7526cddfe4198b8bf34ef69f7406082d868` |
| Corrected `physics.py` SHA-256 | `2a2e53bdfb3964488a446f1549682bc00cb4bc0403ef4a95f1adc245a4e58f63` |
| Corrective delivery ZIP SHA-256 | `7e33da1b05646c5af352a4114e99082c52b51b2b5966911f30816fb2911091da` |
| Corrective delivery ZIP size | 83,421,895 bytes |
| Exact `CORRECTION.patch` SHA-256 | `de8fd97320af569df91d629183a61649e8ae16c082c4fcc6610fc78c472c1a21` |
| Historical EXP1-21 tree | `f1b884a7ada4c806786d1530d76d446aac5d37b1` |
| Preserved prior build ZIP SHA-256 | `a376ad876a164e96cc0b0b1f4f9d250fc8bb70bc4b585bca24092fdee3ada57f` |

The corrective ZIP is `developmental_ecology/artifacts/review-package-correction-20260923-01a0c405/Loom_P_corrective_review_20260923.zip`. Every member was read: 153 members, 152 inventory entries, all sizes/hashes matching. All 51 packaged tracked files match the working delivery and the commit, with the disclosed CRLF-only representation difference for `configuration.json`. The committed configuration bytes are unchanged between checkpoints; its working bytes match the prior runtime receipt. The packaged patch equals the independently obtained exact Git diff. This report's own ZIP has a separate checksum in the adjacent `ZIP_SHA256.txt`.

Runtime used for independent execution: Python 3.13.5; NumPy 2.3.3; SciPy 1.16.2; pytest 8.4.2. Complete dependency identities are in `provenance/IDENTITIES.json`.

## Complete diff classification — VERIFIED

The whole diff contains 16 changed files, 875 added lines and 29 removed lines. Every hunk is assigned below. No changed line/file is classified OUT OF SCOPE. Necessary imports, helpers, comments, and whitespace belong to the same purpose as the hunk they support. The defect in the R1 implementation does not make its intended scope unauthorized.

| Changed file (repository-relative) | Added / removed | Classification of all changed content |
|---|---:|---|
| `developmental_ecology/README.md` | 6 / 8 | Necessary evidence/provenance/reporting: correction status, attempt-003 inspection, package/setup instructions and run boundary. |
| `developmental_ecology/loom_p/physics.py` | 71 / 10 | R1: new release guard; guarded collision candidates; explicit release and return records; pending endpoint handling. All runtime changes are here. |
| `developmental_ecology/package_correction.py` | 239 / 0 | Necessary evidence/provenance/reporting: exclusive new report/package creation, source/runtime receipts, exact diff, preserved old ZIP, assembled-suite check, member hashes. Embedded report/map/ledger/README text has the same classification. |
| `developmental_ecology/tests/test_boundary_and_scheduler.py` | 6 / 4 | R3: actual handoff-boundary terminal cases 19/59, retaining index-50 noise case. |
| `developmental_ecology/tests/test_corrective_contracts.py` | 169 / 0 | R1 functions through line 79: counterexample, release variants, subdivision/native-clock check. R3 from line 82: independent shared/fine oracles, manufactured learner fixtures, executable hidden-state routes and evoked-reserve ownership. Shared imports/fixtures/spacing support these purposes. |
| `developmental_ecology/tests/test_neural.py` | 15 / 2 | R3: strict sensory-reference comparisons; projected/new-target and interior bank-reference oracles. |
| `developmental_ecology/tests/test_physical.py` | 5 / 2 | R3: body footprint comparison at identical time/phase and spatially localized coefficient assertions. |
| `developmental_ecology/tests/test_records.py` | 9 / 3 | R2: empty temporary inspector root, empty replay/waves assertions, live-only sentinel and exact timestamp. |
| `developmental_ecology/verify_correction.py` | 114 / 0 | Necessary evidence/provenance/reporting: dependency/cache checks; three unchanged named-smoke definitions invoked for new attempts; saved reconstructions/comparison; observer check; old/new R1 arithmetic evidence; suite and preservation receipts. Its mutating stage entry points were inspected, not invoked by this review. |
| `developmental_ecology/verify_correction_mutants.py` | 120 / 0 | R1 fault definitions: release, double debit, suppressed damage, repeated native. R2: missing live wave. R3: nine neural/boundary faults. Necessary subprocess/log/receipt scaffolding supports those classifications. |
| `docs/developmental_ecology/p_correction_20260923/BUILD_REPORT.md` | 84 / 0 | Necessary evidence/provenance/reporting. Claims independently assessed below. |
| `docs/developmental_ecology/p_correction_20260923/CORRECTION_EQUATION_TEST_MAP.md` | 18 / 0 | Necessary evidence/provenance/reporting. |
| `docs/developmental_ecology/p_correction_20260923/EXECUTION_LEDGER.md` | 16 / 0 | Necessary evidence/provenance/reporting; historical process claims retain observability limits. |
| `docs/developmental_ecology/p_correction_20260923/RUNTIME_RECORD.json` | 1 / 0 | Necessary runtime provenance. |
| `docs/developmental_ecology/p_correction_20260923/SOURCE_IDENTITIES.json` | 1 / 0 | Necessary source provenance. |
| `docs/developmental_ecology/p_correction_20260923/VERIFICATION_SUMMARY.json` | 1 / 0 | Necessary verification receipts; independently reproduced rather than inherited. |

There is no changed scientific/world-law parameter, packet definition, JEPA addition, R import, adaptive balancing, associative regime, or efficacy-oriented modification. No unexpected law-bearing configuration change required Jason's adjudication. The old branch-base issue has not changed in relevance and was not reopened.

## R1 original exact counterexample — VERIFIED within that fixture

The requested initial state was reproduced exactly: source 0, centre `[2,3]`, angle 0, energy 0.7, integrity 1, velocity `[-0.001,0]`, command `[1,1]`, duration 0.01 s, unmodified `Config()`.

The corrected event sequence is:

| Event | Duration (s) | Accounting observation |
|---|---:|---|
| Release at t=0 | 0 | No contacts, transfer, damage, repair, or expenditure. |
| Free interval | 0.0013148287095122722 | No source transfer, repair, or contact damage; ordinary basal/effort expenditure applies. |
| Explicit return | 0 | `recontact_or_first_touch`, source-0 present, zero impulse in this fixture; no instantaneous transfer or repair. |
| Sustained source contact | 0.008685171290487728 | Contact-specific transfer and damage use only this duration. |

Total elapsed time is 0.01 s. The existing free-motion convention gives zero-gap return about 0.001314924581309022 s; the located return is within the existing geometric resolution. The regression's 2e-7-second allowance follows the local gap rate and spatial tolerance, rather than relaxing accounting to accept the old full-duration behavior.

Observed corrected source transfer is `9.205751373294674e-05`; damage is `8.801521908259946e-05`; final reserves are `[0.7000670575137329, 0.9999119847809174]`. Per-event energy, stock-renewal/debit, integrity, and constitutive damage balances hold to floating-point roundoff (largest displayed residual below 4e-17). Damage need not decrease when contact duration decreases: the sustained-stress allowance also shortens. The builder's removal of a preferred lower-damage assertion is appropriate because the remaining oracle checks the actual law.

Independent in-memory `release_disabled` is RED at the intended release assertion; its unmodified control is GREEN. Independently repeated `double_source_debit`, `damage_suppressed`, and `native_repeated` are also RED then GREEN at their intended accounting/clock assertions. A separate component fixture with an exact-endpoint locator stand-in verifies the real `advance`/accounting path processes one endpoint return without extra positive time or transfer. No duplicate event or zero-time resource exchange was found in these fixtures. This is bounded verification, not a proof of every possible contact configuration.

Evidence: `physics/physics-delta-evidence.json`, `physics/reproduce_physics_delta.py`, and the eight R1 mutant/control logs.

## R1-P: resolvable oblique release is still retained — MUST-FIX BEFORE COMMISSIONING

**Affected code:** `developmental_ecology/loom_p/physics.py:110–132`, especially the decision at line 132 and its use at lines 197–204. Consequent full-interval projection/accounting occurs at lines 224–229.

Keep the same baseline configuration, source, reserves, command, and 0.01-second duration. Change only the manufactured component's velocity and orientation:

```python
b = Body(np.array([2., 3.]), float(np.arccos(.01/.76)),
         velocity=np.array([-1e-5, 0.]))
```

The orientation is `1.557638052356994` radians. The two actuator forces remain `[0.38,0.38]`; their total force has x component 0.01. This is a state fixture, not a parameter change or a freely acting life.

Using the implementation's own frozen-force trajectory, $p(s)=p_0+s\,v(s)$:

| Quantity | Independently observed value |
|---|---:|
| Geometric tolerance | 1e-10 |
| Free-path gap at 0.0005 s | 2.4981434698645444e-9 (about 25 times tolerance) |
| Descending return to geometric tolerance | approximately 0.0009894214175273546 s |
| Descending zero-gap return | approximately 0.000999529101407247 s |
| Free-path gap at 0.01 s | approximately -8.9315284657e-7 (return really occurs) |
| Production `release_probe` | `None` |
| Production events | One sustained source contact, duration 0.01 s |
| Recorded release / return count | 0 / 0 |
| Recorded positive free duration | 0 |
| Recorded source transfer | 9.858939985959484e-6 |

The release guard uses a norm bound containing the large tangential force. With the small outward normal speed, its first certified time is very short and its clearance is below tolerance. Line 132 then returns `None`. Failure of that conservative early certificate does **not** establish that the whole trajectory has no later resolvable separation. The source therefore remains in `active`, is excluded from swept recontact search, and receives full-step contact accounting despite the demonstrated free interval, about one tenth of the native duration.

This is the same class of event-law violation as R1, now exposed by oblique force. It does not depend on a different integrator, exact continuous-world physics, useful learning, or a sub-tolerance excursion. The correction addresses the original numerical example but incompletely addresses the release class.

The primary reviewer's standalone `reproduce_remaining_r1.py` independently fails on the current unmutated checkpoint with `R1 remains: resolvable release/return was charged as full-duration contact`. The physics subreview's separate pytest fixture also fails at its intended free-interval assertion. Conservation can remain correct while the chosen contact duration is wrong; matching source debit/body credit does not close this defect.

A diagnostic call supplying a known-clear guard to the unchanged collision-search component reaches `ArithmeticError: Swept contact search iteration limit` in this same oblique case. This is a subordinate closure consideration, not a separate observed crash of the production `advance` path: currently that path never releases the source. Merely forcing the guard to return true is therefore not an adequate demonstrated fix.

**Smallest closure:** correctly resolve this oblique separating-and-returning component case under the existing motion/accounting convention and tolerances; retain an independently calculated free-gap/return/duration oracle that is RED on `f7eb6f27` and GREEN after correction. Verify no source transfer/repair/contact damage during free motion, no duplicate or zero-time resource exchange, correct return and conserved duration-specific accounting, and no swept-search exhaustion. Preserve the now-closed R2/R3 checks and run the final assembled suite after the scoped correction. Any refreshed bounded evidence must retain distinct identities and old bytes. No neural redesign, parameter tuning, longer life, or commissioning design is required to close this finding.

## R2 isolation and final assembled suites — VERIFIED

The independent worktree run produced `55 passed in 4.37s`; the independently executed packaged assembled code produced `55 passed in 2.32s`. Each used a new workspace temporary directory, `-B`, `PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`, and `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`. The pinned existing Python environment was used; there was no dependency installation. Declared immutable prehistory is an explicit fixture, not hidden replay state.

`tests/test_records.py:76–87` now patches `inspector.ROOT` to its own empty temporary root before construction, asserts empty replay and waves plus no record path, supplies a live-only sentinel, requires the live wave, and retains exact `.2` timestamp equality and state-hash preservation. It does not loosen floating-point equality.

Independent selective executions passed with ambient inspector artifacts present, with an absent ambient root, and with a deliberately invalid saved-manifest fixture in a poisoned ambient root. The latter would fail if constructor loading reached it; the test replaces the root first. The delivered missing-wave mutant fails at `Live handoff branch was not exercised`. Independently replacing the actual `elif not self.replay and e and e.last_wave` branch at `inspector.py:48` with an unreachable condition fails at the same assertion. Fresh unmutated controls pass after each fault. This establishes the intended live path is consequential, not accidentally satisfied by replay.

Evidence: `FINAL_SUITE_INDEPENDENT.txt`, `PORTABLE_SUITE_INDEPENDENT.txt`, `review_r2.py`, and `r2/SUMMARY.json` with seven execution logs.

## R3 falsifiers — VERIFIED

All 14 delivered faults were independently rerun across R1/R2/R3, with observed intended RED assertions followed by unmutated GREEN controls. The nine R3 faults and seven additional R3 probes are recorded below. The primary reviewer's actual live-branch removal is an eighth additional probe overall: **22 consequential RED→GREEN pairs total**, including the 14 delivered faults. The new unmutated oblique R1 failure is separate and remains RED.

| Requested protection | Why the corrected check is consequential | Independently observed faults |
|---|---|---|
| Bank reference following | Zero relative tolerance; explicit nontrivial expected movement. Projected case plus changing interior theta distinguish no movement and old target from the newly projected target. | `bank_reference_frozen`, `bank_reference_old_target`: RED at `test_neural.py:204/215`, then GREEN. |
| Shared sensory reference | Independent exponential oracle from old shared value, nontrivial reference gap, strict tolerance. | `shared_reference_frozen`; additional `shared_reference_new_target`: RED at corrective test line 91, then GREEN. |
| Fine sensory reference | Separately parametrized fine reference and old fine value; independent nontrivial movement. | `fine_reference_frozen`; additional `fine_reference_new_target`: RED at line 91, then GREEN. |
| Terminal handoff exclusion | Real scheduler `Engine.step` with arithmetic stand-ins now starts at 19→20 and 59→60; a handoff would actually be due. Index 50 remains a distinct noise/rollback check. | `terminal_guard_removed` at 19; additional removal at 59: RED at the intended handoff-failure callback, then GREEN. |
| Body diffusion footprint | Same time 0.01 and phase 0.7 in both coefficient calculations; every footprint cell must decrease and every exterior cell remain equal. | `body_footprint_missing`: RED at `test_physical.py:31`, then GREEN. |
| Privileged information boundary | Executed native and handoff arithmetic sees clamped allowed transductions while pose, stocks, fields, clock, phase, world configuration and a world counter differ. A proxy traps representative forbidden config reads. Real chemical transduction is a positive control that does alter neural state. | Delivered `hidden_pose_injected`, `hidden_config_read`; additional stock, clock, and world-counter injections: RED at the intended neural-digest/config trap, then GREEN. |
| Evoked reserve ownership | Opposite evoked E/I content with nonzero regulator weights alters command. Body/stocks must exactly equal independent physical advancement receiving only that command; actual reserve input must remain unchanged. Allowed effort-cost differences are required, rather than mistaking motor effects for a leak. | Delivered `evoked_refill`; additional direct integrity refill: RED at `test_corrective_contracts.py:165`, then GREEN. |

Tests target representative executable routes and their consequences. They are not a security sandbox or an exhaustive proof against arbitrary future code. That scope is a **LIMITATION / EXPECTED PROVISIONAL CHOICE**, not an unclosed R3 engineering failure.

Evidence: `neural/recheck_r3.py`, `neural/mutants-attempt-002/SUMMARY.json`, and all 32 associated logs. The first reviewer harness attempt correctly obtained RED but its receipt parser mishandled Windows path separators; only that review harness was corrected, and a complete new attempt succeeded. Earlier logs are preserved and excluded from success counts. A review-only oblique pytest invocation initially encountered root-discovery permissions; the later explicit-root run records the real assertion failure. No target code was altered to resolve these harness setup issues.

## Regression of selected P mechanism — VERIFIED

Only `physics.py` changed among all 13 runtime modules. `neural.py`, `engine.py`, `chemistry.py`, `geometry.py`, `schema.py`, `records.py`, `reconstruction.py`, `inspector.py`, `smokes.py`, and the other runtime files are byte-identical between the two commits. Their complete hashes are in `provenance/IDENTITIES.json`.

The prior equation audit therefore remains applicable, supported by the corrected strict tests and saved-state reconstruction: P equations 1–21; handoff order; old-H read before coactivity write; previous-perturbation bodily credit; support/query latency; separate E/I banks; actual/evoked reserve ownership; mean-plus-endpoint packets; receptor/packet centring; one-level pooling; configurable sensory widths and pool membership; the deliberately contracting association; selected illumination ruling; and random-stream cadence were not changed. The executable information-boundary checks now provide stronger evidence around the unchanged arithmetic.

At the touched interface, physical event subdivision does not add organism native updates, noise draws, or field updates: the coupled component observes one native and one field operation for the native duration, and the repeated-native mutant fails. Physical and field sensory consequences remain mediated by the existing transduction path. The residual R1 duration error is a body/world realization defect, not a modification of the selected neural mechanism.

## Existing attempt-003 evidence — VERIFIED

Only the existing three authorized cases were inspected and reconstructed. Their configuration identity, master seed `5284097`, life `0`, fixtures, and administrative caps equal attempt-002. Initial underlying states match; snapshot wrapper/code identities correctly differ. Old attempts remain separate and intact.

| Existing case | Native / wave / event records | Final simulated time | Independent reconstruction |
|---|---:|---:|---|
| `birth_30s` / attempt-003 | 3000 / 150 / 3000 | 30.00000000000189 s | All 3000 neural hashes and final field exactly match. |
| `nonzero_resume_1s` / attempt-003 | 100 / 5 / 100 | 1.0000000000000007 s | All 100 neural hashes and final field exactly match. |
| `contact_ui_1s` / attempt-003 | 100 / 5 / 102 | 1.0000000000000007 s | All 100 neural hashes and final field exactly match. |

All cases end in `administrative_pause`; tiny clock excesses are the existing floating-point accumulation, within the verifier's cap tolerance. Recorded source/body balance errors are below 5.6e-17. Every archived member checksum, monotone native index/time, saved random-counter cadence, final neural state and final field was checked by importing the read-only `verify_engineering_records.verify(root)` function. Its file-writing CLI was not run.

Attempt-002 versus attempt-003 comparisons show zero difference in every recorded native reserve, position, angle, velocity, omega, command, stock and contact-rate value; no raw-input or organism-hash differences; and identical complete wave rows. Contact events increase 101→102 solely because an explicit zero-duration source-0 release at t=0 is now recorded. Removing that release record leaves every old/new event row equal. The release uses the existing instantaneous-accounting `impact=True` schema but has explicit `event_kind='release'`, empty contacts and zero exchange; consumers should use the event kind when counting collisions. No trajectory improvement was tuned into these cases. The original manufactured R1 component does change physical accounting, and those differences are independently documented above.

A separate saved midwave check started from the existing 0.07-second/nonzero snapshot at native index 7 and reconstructed the remaining 93 neural/field updates from saved inputs: every hash and final field match. This is detached arithmetic, not a new body/world/organism continuation. Full freely acting replay of the builder's reported duplicate 0.93-second continuation was deliberately not rerun under the user's restriction; its saved result is internally corroborated by this reconstruction.

The inspector loads attempt-003, remains paused at time 0, and observation, pause, saved replay to record 40, and detached parameter reconstruction preserve the live snapshot hash `54a10515c2e5a099a0441445cf30fd926af4ccbb040060a9f9928895ea9f22f3` and random counters. Session steps remain zero; no recorder or server is started.

Evidence: `provenance/RECONSTRUCTION.json`, `ATTEMPT_COMPARISON.json`, `MIDWAVE_RECONSTRUCTION.json`, `OBSERVER.json`, and the unchanged underlying delivery records. These checks establish record consistency and deterministic arithmetic; they do not certify correct contact timing in unexercised states or ecological efficacy.

## Chemical prehistory reuse — VERIFIED

All relevant old-versus-corrected dependencies are unchanged: complete `chemistry.py`, `geometry.py`, `schema.py`, `prehistory.py`, records/serialization dependencies, configuration bytes/semantics, seed/life stream and pinned numerical runtime. The only changed runtime module is physics, which is not in the world-only preparation path. The cache loader independently validates its full field-law values, original preparation source hashes/relevant AST dependencies where applicable, phase, archive checksum and field-array checksum. The historical optical representation distinction predates this correction; no new dependency exception is introduced.

The reused cache is `prehistory-attempt-001`, 600 seconds / 60,000 world-only steps in its preserved completed manifest. Phase is `3.558411277237072`. Field-array SHA-256 is `7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096`; the 94,596-byte `fields.npz` SHA-256 is `f968ed0875d68e3421c5acc9f9a4a218727b9698877b1cc86225d4fec9e6ef7d`. The exact old cache remains intact, the new delivery uses it, and no regeneration was needed or executed in this review. No stale dependency was found. Evidence: `provenance/PREHISTORY.json` and identity/preservation receipts.

## Provenance, preservation, and process-claim limits

**VERIFIED:** old checkpoint remains the exact reachable single parent of the new commit; no intervening merge/rewrite appears in this branch segment. EXP1-21 has the same tree. Old build documents are unchanged. All 252 files in the correction's baseline artifact inventory match size/hash; additionally all 87 entries from the earlier committed build's `EVIDENCE_MANIFEST.json` independently match. That earlier manifest and the old builder ZIP were already available at the previous checkpoint; the ZIP still matches its previous independently established SHA. The corrected delivery has all attempt-003 streams/snapshots, current code/config, source identities, and an exact patch. All 16 selected source identities match their prior records and present reading copies/pinned blobs in their respective representations. The already-disclosed two Workbench-versus-pinned formatting representations are not silently conflated.

**VERIFIED:** during this independent audit, all 474 target artifact files remained byte-identical and no target artifact was added. Review outputs are outside the target repository and Workbench. This review made no commit, push, PR, merge, rebase or vault write.

**LIMITATION / EXPECTED PROVISIONAL CHOICE:** local ancestry and final bytes do not prove the historical absence of a push, PR, or every possible Workbench/vault Git write. Those negative builder process claims cannot be independently certified from the supplied artifacts alone. No contradictory evidence was found. No remote operation or vault-Git write was performed to seek such proof, and this observability limit is not an additional HOLD reason.

## Other limits and scientific questions

**LIMITATION / EXPECTED PROVISIONAL CHOICE:** the finite-step motion convention, contact tolerances, finite solver limits, same-runtime bit reproducibility, unchanged shared bank-parameter configuration, and bounded component/three-case coverage remain as previously disclosed. No fresh browser visual review was needed for unchanged inspector code; observer arithmetic was rechecked. These limits alone are not commissioning blockers. R1-P exceeds the existing geometric tolerance and contradicts the selected event law, so it is not absorbed into this limitation.

**SCIENTIFIC QUESTION, NOT AN ENGINEERING DEFECT:** weak learned influence, survival, useful differentiation, mean/endpoint temporal compression, receptor adaptation, contracting association, and eight-unit capacity remain commissioning/research questions. This review makes no efficacy inference and proposes no change to them.

**UNRESOLVED / REQUIRES JASON:** no unexpected mechanism or law-bearing configuration change was found that requires adjudication. Commissioning remains a separate Jason-authorized task after the engineering HOLD is cleared.

## Exact reproduction commands

PowerShell commands below target the reviewed worktree. Set `$review` to this export's location if moved. All new scratch output belongs outside the target worktree. Review scripts embed the reviewed host path where needed; another host must point them to an extracted, identity-verified delivery. Do not invoke smoke/prehistory generation or the mutating verification/package stages.

```powershell
$repo = 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405'
$review = 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-23-p-post-correction-review-f7eb6f27'
$python = "$repo\.venv\Scripts\python.exe"
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:GIT_OPTIONAL_LOCKS = '0'
Set-Location -LiteralPath "$repo\developmental_ecology"
$env:PYTHONPATH = (Get-Location).Path
$scratch = Join-Path $review ('rerun-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $scratch | Out-Null

# Final worktree suite: expected 55 passed.
& $python -B -X utf8 -m pytest tests -q -p no:cacheprovider --basetemp "$scratch\suite"

# Current unmutated residual R1: expected exit 1 at the final free-duration assertion.
& $python -B -X utf8 "$review\reproduce_remaining_r1.py"

# Original R1 / oblique / endpoint arithmetic evidence, writing only a fresh sibling JSON.
Copy-Item -LiteralPath "$review\physics\reproduce_physics_delta.py" -Destination "$scratch\reproduce_physics_delta.py"
& $python -B -X utf8 "$scratch\reproduce_physics_delta.py"

# Independently observed delivered 14-mutant matrix: each RED exit 1 then GREEN exit 0.
# The inspected harness writes only its explicitly chosen new output directory.
$env:PYTEST_ADDOPTS = "--basetemp=$scratch\mutant-temp"
& $python -B -X utf8 verify_correction_mutants.py --output "$scratch\delivered-mutants"
Remove-Item Env:\PYTEST_ADDOPTS

# R2 artifact-presence controls and delivered/actual-branch faults, with new output root.
Copy-Item -LiteralPath "$review\review_r2.py" -Destination "$scratch\review_r2.py"
& $python -B -X utf8 "$scratch\review_r2.py"

# Sixteen R3 pairs, including the seven independent extra variants.
Copy-Item -LiteralPath "$review\neural\recheck_r3.py" -Destination "$scratch\recheck_r3.py"
& $python -B -X utf8 "$scratch\recheck_r3.py" --attempt independent-rerun

# Read-only ancestry, identities, preservation, all3200 states/fields, observer and midwave audit.
Copy-Item -LiteralPath "$review\provenance\audit_provenance.py" -Destination "$scratch\audit_provenance.py"
& $python -B -X utf8 "$scratch\audit_provenance.py"

# Exact diff/ancestry checks (read-only).
git -C $repo rev-parse HEAD
git -C $repo rev-list --parents -n 1 HEAD
git -C $repo diff --binary d5f7efbe67193f215e52d95ca912db131a79f31c f7eb6f27c661e3db193a4225b56a825d7e41739d
git -C $repo rev-parse HEAD:EXP1-21
```

The portable assembled-suite command is the same pytest invocation after changing directory to `$repo\developmental_ecology\artifacts\review-package-correction-20260923-01a0c405\assembled\developmental_ecology`, setting `PYTHONPATH` to that directory, and using a different fresh `--basetemp`. It independently produced 55 passes. Actual command arguments and designated assertions for each R3 run are saved in its `SUMMARY.json`; physics and R2 receipts/logs identify their controls. RED exits for deliberate faults and the residual R1 are expected evidence, not suite success claims. When reproducing under a different sandbox account, Git may require the process-local `-c safe.directory=<exact reviewed repository>` option in the review helper's Git calls; no global or repository Git configuration change is needed.

## Disposition and intake

**HOLD BEFORE COUPLING COMMISSIONING.** The only required engineering closure is R1-P's oblique release/recontact handling and a consequential regression for it, followed by preservation of the current verified checks and updated exact delivery evidence. R2 and R3 are closed at the reviewed commit. No scientific redesign or commissioning plan is requested or started by this review.

The portable independent-review ZIP includes this report, exact reproduction scripts, independent logs/receipts, the previous independent review report, the user request, exact correction patch, and the byte-identical audited corrective delivery ZIP. `REVIEW_RECEIPT.json`, `FILE_MANIFEST.json`, and the adjacent `ZIP_SHA256.txt` distinguish this independent review from the builder's package. Temporary pytest snapshots and artificial ambient-fixture directories are omitted from the portable package; their substantive logs are retained. The export is ready for Workbench intake; it has not been written into the Workbench.
