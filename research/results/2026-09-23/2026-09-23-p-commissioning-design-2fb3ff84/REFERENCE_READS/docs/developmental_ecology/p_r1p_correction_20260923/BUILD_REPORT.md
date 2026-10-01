# Loom P — second bounded correction, R1-P

**Hold for independent fidelity review. No commissioning fitness is declared.** Sole implementation scope: R1-P from `LOOM_P_INDEPENDENT_POST_CORRECTION_FIDELITY_REVIEW.md`. R2 and R3 remain closed at the previous checkpoint; their existing test and fault-harness bytes were preserved and rerun, not redesigned.

## Checkpoints, local scope and exact diff

Previous checkpoint: `f7eb6f27c661e3db193a4225b56a825d7e41739d`. Original reviewed checkpoint: `d5f7efbe67193f215e52d95ca912db131a79f31c`. Worktree: `C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405`. Existing branch: `build/p-engineering-baseline-20260921-01a0c405`. The new commit is in the package's `CHECKPOINT_RECEIPT.json`, generated after the local evidence commit; `CORRECTION.patch` is the exact committed previous-to-new diff. The historical EXP1-21 tree remains `f1b884a7ada4c806786d1530d76d446aac5d37b1`.

Production changes are confined to `loom_p/physics.py`: added trajectory gap/derivative bounds and whole-interval release search; updated the existing swept search's progress bound. The body integrator, projection, source/repair/stress laws, all configuration values/tolerances, all P equations and native/wave/noise schedule remain unchanged. Added `tests/test_r1p_oblique.py` and new verification/package helpers; current README points here. Every earlier test file and all 12 other runtime modules are byte-identical to f7. No dependency installation, workbench/vault file edit, vault Git write, push, PR or merge occurred. Execution used the existing local Windows `.venv`, Python 3.13.5 and Git 2.50.0.windows.1, with scoped approved worktree access.

Exact user authority and complete independent review are copied into the new evidence directory. The original five-file handoff manifest, accepted P specification and physical foundation were rechecked; their source identities and preserved formatting representations are recorded separately in `SOURCE_IDENTITIES.json`. No historical proposal replaced the selected specification.

## Release and event algorithm

The old inexpensive early release certificate is retained as a fast path. Its failure now invokes `clear_excursion`, which examines the remaining frozen-force path rather than treating an inconclusive early sample as proof of continuous contact. The unchanged convention is $p(s)=p_0+s\,v(s)$, with the existing exponential frozen-force velocity.

`motion_bounds` bounds path speed and acceleration. `gap_curve` evaluates actual gap and normal path rate, including prescribed mover velocity. `gap_curvature_bound` bounds the second derivative of the gap using the relative acceleration and the distance-gradient curvature outside the convex fixture. Over an interval of width $h$, endpoint interpolation differs from the true gap by at most $Bh^2/8$. Release search discards an interval only when an upper enclosure rules out a resolvable excursion; otherwise it subdivides and evaluates the actual geometry. It retains the existing spatial-resolution criterion for a departure from the current touching state, avoiding duplicate sub-tolerance releases at a located return. Neither a failed early certificate nor a failed finite search is silently converted into sustained-contact evidence.

A clear point becomes a swept-search guard only after checking that its preceding path does not cross into the solid beyond geometric tolerance. Release remains at the beginning of the resolved departure, the clear prefix is excluded only while certified, and subsequent return is located by the same event machinery. Free flight has ordinary basal/effort expense but no source transfer, repair or contact damage. Recontact is an explicit zero-duration record, with no zero-duration transfer or repair. Remaining positive contact duration is accounted by the unchanged equations.

The swept search still has its **500-pass limit**, but can now use a local normal-rate lower bound:

$$g(s+h)\geq g(s)+g'(s)h-\tfrac12Bh^2.$$

Solving this quadratic for a safe increment prevents large tangential velocity from forcing hundreds of tiny increments while the normal gap changes slowly. The globally valid speed bound remains available when the curvature bound cannot be certified. The previous 0.8 clearance factor, native dt, geometry/event tolerances and physical-event subdivision limit are unchanged. These are search calculations, not additional integration, learning, random draws or field updates.

If a gap enclosure cannot be resolved within the existing time resolution/search bound, or a proposed free prefix crosses a solid before clearance, the implementation reports an apparatus error instead of fabricating continuous contact or skipping a collision. Those paths are explicit numerical limits, not claims of general curved-contact convergence; this pass verifies the specified radial/oblique departure class and bounded regression cases.

## RED-before-GREEN and independent fixture oracles

Before any physics edit, the exact unmodified f7 runtime was tested with the new regressions: **4 failed**. The exact review fixture and changed-normal-force variant failed at the explicit missing-free-flight assertion; the reflected longer-flight variant reproduced swept-search exhaustion. The cadence fixture also rejected the missing event path. `F7_OBLIQUE_RED.txt` preserves that execution.

The final new test uses an independent analytic transcription of the declared free trajectory and a source-centre distance calculation. It does not call production `release_probe`, `free_velocity`, `actuator_forces` or `gap_normal` for its oracle. Independent bracketing locates descending geometry-tolerance and zero-gap crossings. The scheduled free duration must lie between those crossings (apart from the existing event-time resolution). The exact fixture independently reproduces the 2.4981434698645444e-9 gap at 0.0005 s. Its source, E=0.7, I=1, command [1,1], initial velocity [-1e-5,0], orientation arccos(.01/.76), baseline Config and 0.01-second duration are unchanged.

Two fixed state variants vary orientation/normal force and departure speed/reflection. They are deterministic component falsifiers, not a parameter sweep or new complete-loop case. All fixtures require one release, nonzero free duration, one return, no free-flight contact effects, duration-specific transfer/stress, duration conservation, source/body balance and normal completion. The original radial test remains unchanged. A separate wrapper fixture asserts exactly one native/noise call and one field update despite multiple physical events.

Four new isolated faults were each observed RED then GREEN: **unmodified f7 physics**, **disabled class-level release search**, **f7 swept search with corrected release**, and **duplicated field update**. The old-search fault demonstrates why forcing release alone is insufficient. The original **14-pair fault matrix** was rerun unchanged against the final runtime; every designated fault again failed and its unmutated control passed. Total: **18 RED→GREEN pairs**, with commands, source hashes and separate logs. No runtime file was mutated by these fault subprocesses.

A development check found only an exact decimal-equality assertion on summed time failing at 0.010000000000000002. The new test now checks duration conservation to 1e-16 seconds, in addition to the independent crossing oracle. No runtime tolerance or parameter was changed. Its original 33-pass/1-fail log is retained. Final tests and the old-f7 RED control were then rerun.

## Measured component completion

Each row terminates normally. Loop counts below are observed by read-only Python tracing of the bounded release/swept loops. `search` counts include release and free-prefix validation. They are not measured by changing runtime code.

| Fixture | Positive free duration (s) | Positive contact duration (s) | Actual loop passes |
|---|---:|---:|---|
| review-exact | 0.00099450757408153009 | 0.009005492425918471 | search:4, search:22, first_collision:15, search:74, first_collision:2 |
| different-normal-force | 0.00049520310801757464 | 0.0095047968919824248 | search:5, search:16, first_collision:11, search:60, first_collision:2 |
| reflected-longer-flight | 0.0019947279455729632 | 0.0080052720544270366 | first_collision:31, search:74, first_collision:2 |
| radial-original | 0.0013149022740740091 | 0.0086850977259259905 | first_collision:8, search:20, first_collision:2 |

`PHYSICAL_COMPONENT_EVIDENCE.json` records full old/new events, bodily consequences and counters. Values are retained even when different from earlier checkpoints. The radial fixture remains GREEN; the exact oblique fixture and both variants are GREEN. Source/body equality alone is not the acceptance gate: the independent free-gap and event-duration assertions must also pass.

## Final assembled suite and smoke evidence

Final worktree suite after all new smoke/reconstruction artifacts exist: **59 passed in 2.52s**. All previously verified R2/R3 checks pass unchanged. The portable package is assembled with all fixtures and runs the same complete component suite before ZIP finalization; its result is `PORTABLE_COMPONENT_SUITE.txt` and `PORTABLE_VERIFICATION.json` inside the ZIP.

Same semantic configuration `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`, working configuration bytes `985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9`, master seed **5284097 / 0x50A101**, life **0**, same fixture definitions and administrative caps. New smoke identity: **attempt-004**.

| Case / attempt | Native / wave / event records | Simulated seconds | Wall seconds | Max source/body residual |
|---|---:|---:|---:|---:|---:|
| birth_30s / 004 | 3000 / 150 / 3000 | 30.000000000002 | 140.714 | 5.54e-17 |
| nonzero_resume_1s / 004 | 100 / 5 / 100 | 1 | 16.957 | 5.46e-17 |
| contact_ui_1s / 004 | 100 / 5 / 102 | 1 | 4.354 | 5.52e-17 |

Every case stopped at its administrative cap. All **3,200 neural states** and all three final chemical fields reconstruct bit-identically from their saved actual inputs. Checksums, native/wave/noise counters and source/body accounting pass. The nonzero case repeats the declared 0.07-second pause and 0.93-second duplicate continuation with exact full-state comparison and repeated observer isolation. Saved replay/reconstruction of contact record 40 leaves the live inspector state/counters unchanged at time zero, with zero UI simulation steps and no server started.

New complete-loop execution: **32.93 simulated seconds**, comprising the same 30+1+1-second cases plus the authorized 0.93-second restart comparison. There were no failed attempt-004 smokes or additional complete-loop cases. Detached reconstruction and manufactured arithmetic fixtures are not scientific lifetimes. No efficacy interpretation is made.

Attempt-003 → attempt-004 measured differences:

- birth_30s: {"reserves": 0.0, "position": 0.0, "angle": 0.0, "velocity": 0.0, "omega": 0.0, "commands": 0.0, "stocks": 0.0, "contact_rates": 0.0}; changed neural hashes 0, raw rows 0; event records 3000 → 3000.
- nonzero_resume_1s: {"reserves": 0.0, "position": 0.0, "angle": 0.0, "velocity": 0.0, "omega": 0.0, "commands": 0.0, "stocks": 0.0, "contact_rates": 0.0}; changed neural hashes 0, raw rows 0; event records 100 → 100.
- contact_ui_1s: {"reserves": 0.0, "position": 0.0, "angle": 0.0, "velocity": 0.0, "omega": 0.0, "commands": 0.0, "stocks": 0.0, "contact_rates": 0.0}; changed neural hashes 0, raw rows 0; event records 102 → 102.

## Preservation, prehistory and portable inspection

All **489 preexisting artifact files** retain exact lengths and SHA-256 values. Both earlier checkpoints, every earlier smoke attempt, original reviews/reports and old portable packages remain preserved. Old source documents are unchanged. The new ZIP contains the byte-identical first corrective ZIP, which itself contains the original build ZIP; each checkpoint remains separately identified.

All field/prehistory dependencies and the configuration were verified unchanged before running any refreshed smoke. The existing `prehistory-attempt-001` cache was revalidated by dependency identities, law values, seed/phase, archive checksum and field-array checksum and reused. **No 600-second prehistory regeneration or prehistory step was executed.** `PREHISTORY_AND_SCOPE.json` records the exact identities.

Double-click `developmental_ecology/Open Loom Inspector.cmd`. It loads the **attempt-004 initial contact fixture at time zero, paused**; saved-record replay is available. Launch advances nothing. The existing launcher/inspector bytes are unchanged. For portable setup, the existing `Setup Loom Inspector.cmd` installs pinned dependencies into an adjacent `.venv` using Python 3.13. No fresh installation or visual browser QA was performed in this pass; paused observer arithmetic was reverified. No inspector server or background simulation was started.

The package includes full attempt-004 native/wave/event streams, snapshots, current code/tests, exact config/runtime/source records, authority/review, all RED/GREEN logs, preservation receipts, exact patch and this report. `ARTIFACT_MANIFEST.json` verifies every packaged member; the adjacent ZIP checksum and checkpoint receipt identify this new delivery. Temporary pytest snapshots are omitted; substantive logs and source fixtures are included.

## Remaining limits and what was NOT tested

Independent fidelity review remains pending. No fitness for coupling or ecological commissioning is declared. No scientific lifetimes, cohorts, commissioning, efficacy tuning, parameter/capacity sweeps, survival/useful-learning pass gates, experiment numbering, preregistration, P/R synthesis, JEPA, packet change, associative-regime change or world-law change. No fourth complete-loop case, natural terminal full-loop event, 600-second organism run or prehistory regeneration. No long-duration storage/performance study, cross-platform/dependency-version bit identity, real disk exhaustion, fresh dependency setup or renewed browser/double-click visual inspection.

The finite-step frozen-force/contact-normal realization is not a convergence proof or exhaustive treatment of arbitrary curved/grazing/simultaneous/moving contacts. Search enclosures and finite limits can reject an unresolved path explicitly. Sub-resolution departures retain the existing geometric resolution. The previously disclosed shared equal-valued E/I configuration fields and broader sensory/temporal/associative/ecological scientific questions are unchanged and outside R1-P. R2/R3's representative executable-route coverage remains as independently accepted, not an arbitrary-code security guarantee. **Stop for independent review.**
