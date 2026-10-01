# Independent R3 falsifier and neural-delta review

Reviewed correction: `f7eb6f27c661e3db193a4225b56a825d7e41739d`, compared with `d5f7efbe67193f215e52d95ca912db131a79f31c`.

Worktree: `C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405`.

**R3 is closed for the named protections.** Independent execution observed 16 consequential RED → GREEN pairs: all nine delivered R3 mutants and seven additional variants. Each RED reached the intended material assertion; no import, missing-attribute, unrelated setup or arithmetic exception substituted for the intended falsifier. The preserved neural implementation and selected configuration are unchanged. Separately, this reviewer reproduced and analytically confirmed the lead reviewer's residual R1 counterexample; the overall checkpoint therefore remains on HOLD for R1.

Code references below are relative to the worktree's `developmental_ecology/`. This is a read-only, component-level audit. It did not modify the target, Workbench, Git state, configuration or existing evidence, or start any freely acting organism lifetime, smoke, prehistory or sweep.

## Consequential R3 closure

Classification of every row in this table: **VERIFIED**.

| Protection | Independent failure and restored result | Executing test/oracle |
|---|---|---|
| Bank reference following | Restoring old reference after the genuine update fails at line 204. Following old theta instead of newly projected theta fails at line 215. Both clean controls pass. | `tests/test_neural.py:195–215` |
| Sensory shared reference | Disabling only shared following fails at line 91. An independently supplied wrong-new-target mutant also fails there. Both clean controls pass. | `tests/test_corrective_contracts.py:82–93` |
| Sensory fine reference | Disabling only fine following fails at line 91. An independent wrong-new-target mutant also fails there. Both clean controls pass. | `tests/test_corrective_contracts.py:82–93` |
| Terminal handoff exclusion | Changing the actual production `elif` to an independent `if` invokes the designated `Invented terminal handoff` callback at line 48, for both start indices 19 and 59. Clean controls pass. | `tests/test_boundary_and_scheduler.py:41–62`; production guard `loom_p/engine.py:96–99` |
| Organism diffusion footprint | Removing only the body-position argument from coefficient construction fails the occupied-cell comparison at line 31. Clean control passes. | `tests/test_physical.py:18–33` |
| Executable privileged-information boundary | Delivered hidden-pose injection fails native state equality at line 135; direct forbidden configuration access fails its proxy at line 116. Additional hidden source-stock, clock and world-draw-counter injections each fail line 135. All clean controls pass. | `tests/test_corrective_contracts.py:109–144` |
| Evoked reserve ownership | Delivered direct energy refill and additional direct integrity refill fail body equality against the physical-only command oracle at line 165. Both clean controls pass. | `tests/test_corrective_contracts.py:147–169` |

Full records: `mutants-attempt-002/SUMMARY.json` and its 32 RED/GREEN logs. `recheck_r3.py` records each exact child command and requires the expected exit status, failure message, exact test line and test count. Log inspection confirmed the final failure locations, rather than relying on a test name or finding the expected phrase somewhere in the test's displayed source.

The new reference comparisons use zero relative tolerance. The numerical margins are material: shared-reference required movement is `7.905690197970716e-09`, fine-reference movement is `1.0954440195654752e-09`, both versus absolute tolerance `1e-18`. Their old-versus-new-target differences are `2.7898169885354207e-13` and `3.425076682776057e-12`. The interior bank reference moves `1.5799364010637973e-05`; using old theta instead differs by `2.003159936814214e-07`, versus `1e-16` tolerance. These are recorded in `independent_checks.json`.

The terminal fixtures now increment 19→20 and 59→60, where ordinary scheduling would invoke a handoff. They supply a reserves object, so the mutant reaches the intended callback rather than failing first on missing body data. Index 50 remains a separate retained-noise-clock check. This is a scheduler component with physical/neural stand-ins, not evidence of a naturally encountered terminal death.

Diffusion comparison holds both time (`0.01`) and mover phase (`0.7`) constant. Independent arithmetic finds 16 occupied cells, reduced diffusion in all of them and bit-identical diffusion outside them. The maximum change is `0.475`. The old confounding mover displacement is removed.

The boundary fixture clamps declared transduction while varying physical pose, angle, stocks, fields, time, mover phase, world configuration and a world draw counter. It executes the real native and handoff neural methods in the coupled wrapper with physical/field stand-ins, and includes a real-transduction positive control. The evoked-reserve fixture uses nonzero regulatory weights, confirms opposite evocations actually change commands, and compares each resulting body against a separate physical advance supplied only that delivered command. Thus allowed effort-cost changes are distinguished from forbidden refill.

**LIMITATION / EXPECTED PROVISIONAL CHOICE:** these are executable coverage checks for named routes, not a security sandbox or proof against arbitrary future modifications. Their limited scope is explicitly described in the correction report and does not defeat R3 closure. The reserve oracle intentionally shares physical arithmetic, because it tests ownership/routing; independent correctness of that arithmetic remains R1's separate responsibility.

## Preserved selected P mechanism

**VERIFIED:** Git blob comparisons and working-file hashes in `independent_checks.json` establish unchanged `neural.py`, `schema.py`, `engine.py`, `chemistry.py`, `geometry.py`, `inspector.py`, `records.py` and configuration across the two commits. Only `physics.py` changed among runtime modules. Configuration retains semantic SHA-256 `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`; working JSON's preexisting newline representation is recorded separately from Git bytes.

The unchanged paths therefore preserve the previously independently verified equations 1–21, old-H read/later write, previous-perturbation credit, one-wave support-query latency, separate bodily banks, actual packet ownership, sensory and packet centring, one-level pools, configuration-derived widths, contraction, illumination selection and random schedule. Spot inspection confirms physical subdivision still sits inside `Engine._coupled` after its single native call (`engine.py:65–71`); the scheduler and neural handoff were not rewritten.

**LIMITATION / EXPECTED PROVISIONAL CHOICE:** the previously reported common scalar configuration fields for equal E/I rates are unchanged. They do not create a common bodily teaching signal and are outside R1–R3.

## Residual R1 cross-check

**MUST-FIX BEFORE COMMISSIONING:** the lead reviewer's new fixed counterexample remains a false full-duration contact under the implementation's own free path. This reviewer executed `../reproduce_remaining_r1.py`; full output is `remaining-r1-crosscheck.txt`.

Using unchanged Config, source-0 touch at `[2,3]`, velocity `[-1e-5,0]`, angle `acos(.01/.76)`, E `0.7`, I `1`, command `[1,1]`, duration `0.01`, the free path reaches gap `2.4981434698645444e-09` at `0.0005` seconds. That exceeds the `1e-10` spatial tolerance by about 25 times. Return to that tolerance is approximately `0.0009894214175273546` seconds. Nevertheless `release_probe` returns `None`, and `advance` returns one full `0.01` sustained-contact event, no release/free interval/recontact, and transfer `9.858939985959484e-06`.

The reason is visible at `physics.py:104–114,127–132`: a bound based on full force magnitude restricts the initial proof interval to a tiny duration when normal separation speed is small and force mostly tangential. Failure to exceed spatial tolerance within that conservative guard does not imply there is no resolvable excursion later. Yet `advance` retains the contact (`physics.py:197–204`) and charges sustained accounting for the full interval (`physics.py:215–229`). This is not a request for a different integrator or resolution; it contradicts the current model's resolvable free path. It is the same class of R1 failure outside the corrected original fixture.

## Reproduction and execution record

From PowerShell, set `PYTHONDONTWRITEBYTECODE=1` and invoke the exported harness with a fresh attempt name:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe' -B -X utf8 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-23-p-post-correction-review-f7eb6f27\neural\recheck_r3.py' --attempt reproduce-001
```

The harness disables pytest cache and third-party plugin autoload, uses a fresh export-local temporary directory per RED/GREEN child, imports production code read-only, and writes only its own new evidence directory. No delivered package writer or smoke runner is invoked.

A first local receipt attempt correctly produced the expected bank-reference RED but the review harness rejected its Windows-backslash filename while matching a forward-slash expected path. That initial log and receipt are preserved under `mutants/`; only the export-local receipt parser was corrected. The complete attempt-002 then passed all 16 pairs. A read-only nested Git query initially encountered Git ownership checking; subsequent queries used a process-local `-c safe.directory=<explicit target>` option. No global or repository Git configuration was changed.

R3 closure and neural preservation are established. They do not close the independently reproduced residual R1 defect. No commissioning design or execution is authorized or performed by this review.
