# Loom P — bounded corrective engineering report, 2026-09-23

**Hold for independent fidelity review.** This pass implements the authorized R1 correction and supplies new R2/R3 verification. It does not declare the build fit for coupling commissioning. The independent review's failing checkpoint and all its artifacts remain preserved; its old completion claims are historical, not the status of this correction.

## Identity and authority

Old reviewed checkpoint: `d5f7efbe67193f215e52d95ca912db131a79f31c`. Worktree: `C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405`. Existing branch: `build/p-engineering-baseline-20260921-01a0c405`. The new commit is recorded in the package's `CHECKPOINT_RECEIPT.json`, generated after the evidence commit. No amend, rebase, merge, push or PR occurred. Historical EXP1-21 tree remains `f1b884a7ada4c806786d1530d76d446aac5d37b1`.

Authority is the exact `CORRECTION_AUTHORITY.txt`; scope is R1–R3 from `LOOM_P_INDEPENDENT_FIDELITY_REVIEW.md`, copied byte-for-byte into the new evidence directory. The original complete handoff, five-file source manifest and accepted physical references remain the selected sources. Their identities were reverified in `SOURCE_IDENTITIES.json`; project history did not replace the specification. The directional open-domain ruling, P equations, eight-unit/equal-pool baseline, mean-plus-endpoint packet and fading associative regime are unchanged. R and all alternatives remain preserved.

Execution was local Windows Python 3.13.5 and Git 2.50.0.windows.1, using the existing scoped `.venv`; no dependency installation was needed. Restricted read-only inspection and approved worktree writes were distinguished. No Git writes or file edits were made in the Obsidian workbench. The original code checkout's unrelated changes were left alone.

## Exact change

Production change: `developmental_ecology/loom_p/physics.py` only. The new `release_probe` certifies a separating initial segment of the existing frozen-force trajectory. `advance` removes released contacts from the sustained constraint set and emits a zero-duration release record. `first_collision` skips that fixture only until the certified clear point, then includes it in the ordinary swept search. A returned touch is recorded even when its normal impulse is zero. A pending touch at a substep endpoint is processed. No free-motion equation, normal projection, reserve law, field solver, neural equation, constitutive parameter or tolerance was replaced.

Tests changed: `test_neural.py`, `test_physical.py`, `test_records.py`, `test_boundary_and_scheduler.py`; added `test_corrective_contracts.py`. New verification/package helpers are outside `loom_p`, so they do not change snapshot code identity. The current README points to this correction. Exact committed changes are in `CORRECTION.patch`; runtime module hashes are in `RUNTIME_RECORD.json` and every new smoke manifest.

## R1–R3 closure evidence for review

| Finding | Correction and evidence | Review status |
|---|---|---|
| R1 release/recontact | Exact review counterexample; start release, positive free flight, swept return and only the remaining duration charged as contact. Source/body balance, duration, stress/repair identity and native/noise isolation checked. Disabled release, double debit, suppressed damage and repeated native call each observed RED, then GREEN. | Implemented and locally verified; independent closure pending |
| R2 live inspector test | Empty temporary inspector root isolates both native replay and wave artifacts; unique live sentinel and exact `0.2` timestamp prove the intended branch. Missing live wave observed RED, then GREEN. Entire suite runs after all attempt-003 artifacts exist. | Implemented and locally verified; independent closure pending |
| R3 consequential falsifiers | Zero-relative-tolerance reference oracles, separate shared/fine checks, changed-theta bank oracle; terminal indices 19→20 and 59→60 plus retained index-50 noise check; fixed-time/fixed-phase body footprint; executable hidden-state and evoked-reserve injections. Each designated fault produces its expected assertion failure and then a clean test passes. | Implemented and locally verified; independent closure pending |

Final assembled component suite: **55 passed in 2.27s**. Before correction, the reproduced assembled baseline was **43 passed, 1 failed**. `mutants-attempt-001/SUMMARY.json` and 28 separate logs preserve **14 observed RED → GREEN pairs**. Every red subprocess exited 1 at its designated assertion; every corresponding unmutated subprocess exited 0. These are executed faults, not hypothetical statements that a test should fail.

The bank oracle independently checks an interior update as well as active projection, rejecting both a frozen reference and an old-theta target. Sensory reference movements use independent exponential formulas and separately reject disabling each operation. The terminal mutant changes the actual scheduler `elif` to `if` and reaches the intended failing callback, not an unrelated missing-body error. Diffusion holds mover time and phase fixed, checks the occupied cells and exact equality elsewhere.

Hidden-state checks execute real learner native/handoff arithmetic inside the actual coupled wrapper, with physical/field stand-ins and declared transductions clamped. Pose, stocks, fields, time, phase, world configuration and world-stream counter differ while every learner component stays identical. A proxy traps forbidden configuration reads; injected pose and hidden-config mutants fail. A real transduction positive control changes chemistry input and learner arithmetic. This is executable path coverage, not a security sandbox or proof against arbitrary future code.

Evoked E/I channel content is changed with nonzero regulatory weights. Actual reserve inputs remain unchanged through regulation; subsequent body state must exactly equal a separate physical advance receiving only the delivered motor command. Opposite injections do change commands and hence permitted physical effort costs. A direct evoked refill mutant fails. Neither real fields nor a fourth full organism/world case is executed by these fixtures.

## R1 bodily consequences

Exact starting fixture: position `[2,3]`, angle `0`, velocity `[-0.001,0]`, E=`0.7`, I=`1`, stocks all `0.2`, command `[1,1]`, time/phase `0`, dt=`0.01`. The analytic return of the unchanged free path is 0.001314924581309022 s. Its halfway gap is about 3.28623e-7, over 3,000 geometry tolerances.

Observed free flight: **0.0013148287095122722 s**; sustained contact: **0.0086851712904877278 s**. Swept detection stops at spatial tolerance; the test's 2e-7 s return-time allowance is derived from the approximately 0.001 normal path speed and unchanged 1e-10 geometry tolerance. It is not a relaxed configuration tolerance. A zero-impulse return is still an explicit event. All positive durations sum to 0.01 s.

| Counterexample consequence | Preserved old implementation | Corrected |
|---|---:|---:|
| Source transfer | 0.00010415229960600089 | 9.2057513732946743e-05 |
| Damage | 8.1441530337662235e-05 | 8.8015219082599464e-05 |
| Final E | 0.70007915229960593 | 0.70006705751373288 |
| Final I | 0.99991855846966238 | 0.99991198478091736 |

Damage increases here because the impulse threshold allowance is proportional to the shorter sustained-contact duration. The existing damage equation, source debit/body credit and subinterval reserve-dependent force calculation are retained. No attempt was made to recover the prior bodily values. Full old/new events are in `R1_COUNTEREXAMPLE.json`; the old source bytes were read from the preserved commit and executed only for this component comparison.

## Exact bounded reverification

Same configuration SHA `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`, master seed **5284097 / 0x50A101**, life **0**, unchanged fixture definitions and administrative durations. New identities are attempt **003**. Attempt 002 and all earlier evidence remain unchanged.

| Case / attempt | Native / wave / physical records | Simulated seconds | Wall seconds | Stop |
|---|---:|---:|---:|---|
| birth_30s / 003 | 3000 / 150 / 3000 | 30.000000000002 | 125.216 | administrative_pause |
| nonzero_resume_1s / 003 | 100 / 5 / 100 | 1 | 15.778 | administrative_pause |
| contact_ui_1s / 003 | 100 / 5 / 102 | 1 | 4.169 | administrative_pause |

All **3,200 native neural hashes** and all three final chemical fields reconstruct exactly from initial snapshots and saved actual inputs. Checksums, records, random clocks and source/body accounting pass. `RECONSTRUCTION.json` carries every final hash and accounting residual. Nonzero pause at 0.07 s resumes bit-identically through the remaining 0.93 s, with observed versus unobserved continuations compared at every step. A separate paused-inspector replay/reconstruction at record 40 leaves the live state and counters unchanged and runs zero simulation steps.

New complete-loop execution totals **32.93 simulated seconds**: 30 + 1 + 1 + the authorized 0.93 restart comparison. There were no failed new smoke attempts and no extra UI stepping. Detached reconstruction and arithmetic component fixtures are separate from complete-loop execution. Including the preserved build's disclosed 63.47 seconds, the combined historical total is 96.40 seconds; this is repetition accounting, not a new lifetime.

Observed attempt-002 → attempt-003 differences (maximum absolute values; no efficacy target):

- birth_30s: {"reserves": 0.0, "position": 0.0, "angle": 0.0, "velocity": 0.0, "omega": 0.0, "commands": 0.0, "stocks": 0.0, "contact_rates": 0.0}; differing organism hashes 0/3000; physical records 3000 → 3000.
- nonzero_resume_1s: {"reserves": 0.0, "position": 0.0, "angle": 0.0, "velocity": 0.0, "omega": 0.0, "commands": 0.0, "stocks": 0.0, "contact_rates": 0.0}; differing organism hashes 0/100; physical records 100 → 100.
- contact_ui_1s: {"reserves": 0.0, "position": 0.0, "angle": 0.0, "velocity": 0.0, "omega": 0.0, "commands": 0.0, "stocks": 0.0, "contact_rates": 0.0}; differing organism hashes 0/100; physical records 101 → 102.

Only `physics.py` differs among runtime modules. All field/prehistory dependencies match the baseline bytes; configuration file bytes also match the original runtime receipt. The existing lawful 600-second field cache was checked by module/AST identities, field-law values, phase, archive hash and array hash, then reused. **Zero prehistory steps were rerun.** `PREHISTORY_REUSE.json` gives the receipt. The initial preflight also exposed Git's ordinary JSON newline normalization; the check now separately verifies original working-file bytes and committed JSON content rather than confusing their representations.

## Preservation, use and review boundary

All **252 preexisting artifact files** retain their original lengths and SHA-256 values (`PRESERVATION_VERIFIED.json`). The old report, old review package, attempt-002 results and reviewed commit are preserved. An initial development assertion predicted lower damage; it failed with 54 other tests passing and was removed because that directional prediction was unsupported by the law. The retained gate is the independent duration-specific damage equation. An initial component invocation from the wrong directory failed import collection before tests; the actual recorded checks run from `developmental_ecology`. These setup failures did not run additional organisms.

Open `developmental_ecology/Open Loom Inspector.cmd` by double-clicking. It loads **attempt-003 initial contact_ui_1s at time zero, paused**, with new saved records available for replay. Nothing advances on launch. The launcher and inspector production bytes are unchanged. The browser/server was not launched or visually retested in this correction; paused observer/replay/reconstruction was exercised directly. No inspector server or background simulation was started by this pass. For a portable extraction, the existing `Setup Loom Inspector.cmd` uses Python 3.13 and installs the pinned local dependencies. Cross-host bit identity is not claimed.

The new ZIP contains full attempt-003 traces (including birth), snapshots, tests, exact configuration/runtime/source records, correction authority/review, 14 RED/GREEN pairs, preservation/reconstruction evidence and this report. It also carries the previous portable review ZIP unchanged for the failing checkpoint. `ARTIFACT_MANIFEST.json` hashes every packaged member; the adjacent receipt supplies old/new commits, exact branch, archive tree and ZIP checksum. No source archive was added to Git. All current reports sit in the new `p_correction_20260923` directory.

## What remains uncovered and what was NOT tested

No scientific lifetime, cohort, ecological commissioning, coupling commissioning, capacity/parameter sweep, efficacy tuning, developmental success, useful learning, survival gate, experiment number or preregistration. No 600-second organism run or repeated prehistory. No mechanism alternative, R run, tonic bypass, JEPA, packet replacement, magnitude balancing or stronger association. No extra complete-loop case; no natural terminal death occurred in the three smokes. Terminal scheduling is a stand-in plus separate real-physics component test. No long-duration storage/performance test, cross-platform/version identity, real disk exhaustion, fresh dependency install or renewed visual browser/double-click QA.

Finite frozen-force/contact-normal mechanics remain an uncommissioned numerical realization. The release guards and selected outward/rest/tangent source fixtures do not establish convergence or exhaustive adequacy for curved, grazing, simultaneous or moving contact geometries. Changes below the existing spatial resolution are not resolved into separate flights. Information-flow and reserve-ownership tests cover the named executable paths and mutants, not arbitrary malicious future code. The review's separate limitation that equal-valued E/I constants share configuration fields is unchanged and outside R1–R3. Broader temporal compression, sensory differentiation, associative adequacy and ecology questions remain open. Independent fidelity review must assess closure and any commissioning decision. **Stop here.**
