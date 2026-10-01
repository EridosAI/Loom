# Independent R1 physical delta review

Reviewed checkpoint: `f7eb6f27c661e3db193a4225b56a825d7e41739d`, compared with `d5f7efbe67193f215e52d95ca912db131a79f31c`.

Configuration identity observed: `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`.

**Disposition from the physical review: HOLD BEFORE COUPLING COMMISSIONING.** The exact original counterexample is corrected, but the new release guard still misses a resolved oblique release/recontact under the selected finite-step motion convention. No alternative integrator or scientific parameter is needed to demonstrate the defect.

## VERIFIED — original counterexample and local accounting

The exact original state `[2,3]`, angle 0, velocity `[-0.001,0]`, E 0.7, I 1, command `[1,1]`, duration 0.01 produces these events:

| Event | Duration | Contact accounting |
|---|---:|---|
| Release | 0 | No transfer, repair, damage or expenditure |
| Free flight | 0.0013148287095122722 | Basal/effort expenditure only; no contacts, transfer, repair or damage |
| Recontact | 0 | Explicit source-0 event, zero normal impulse; no exchange or repair |
| Sustained contact | 0.008685171290487728 | Transfer 0.00009205751373294674; duration-specific damage 0.00008801521908259946 |

Durations sum to 0.01. Event-by-event source renewal/debit and body credit/expenditure balances, damage formula and integrity balance agree within 1e-15. No duplicate contact or zero-time transfer was found in this fixture. The shorter contact duration explains the changed bodily values; outcome improvement was not a criterion.

The production loop processes a pending contact even at an exact interval endpoint (`physics.py:170`, `:182-193`, `:238`). A separate detached arithmetic component supplied an exact endpoint contact time through a locator stand-in and exercised the real `advance` and `account`: one positive free interval followed by one zero-duration impact, no extra positive interval and no transfer/repair. This tests pending-event handling, not the locator's time accuracy.

Full values and events: `physics-delta-evidence.json`; reproducer: `reproduce_physics_delta.py`.

## MUST-FIX BEFORE COMMISSIONING — conservative release guard is treated as a no-release decision

`developmental_ecology/loom_p/physics.py:114` chooses only the conservative guard `u/A`; `:128-132` returns no release if clearance at that one point is at or below `geometry_tol`. Failure to resolve separation at this short point is not proof that the remaining native interval has no resolved separation. `advance` consequently keeps the source active (`:197-204`), excludes it from swept search, projects its endpoint velocity (`:224`) and accounts the entire interval (`:229`).

One deterministic oblique component, with unchanged configuration:

```python
c = Config()
b = Body(np.array([2., 3.]), math.acos(.01/.76),
         velocity=np.array([-1e-5, 0.]))
events, _, _ = advance(c, b, np.full(8, .2), 0., 0., np.ones(2), .01)
```

The fixed initial force has normal component 0.01 and a larger tangential component. The selected free-motion convention remains exactly `p(t)=p0+t*v(t)`, with the declared exponential velocity and frozen force/orientation. No exact continuous-time displacement integrator is substituted.

The guard is `6.481723120100474e-06` s, where the gap is `6.43967101865428e-11`, below the existing `1e-10` spatial tolerance. The routine therefore returns `None`. But the same free path has:

| Time | Source surface gap |
|---:|---:|
| 0.0004997501665417116 | 2.498144358042964e-09 |
| 0.0009 | 8.957368180517733e-10 |
| 0.001 | -4.708011758225439e-12 |
| 0.01 | -8.931528465705441e-07 |

The positive excursion is approximately 25 geometry tolerances. A deterministic bracket of the closed-form selected path gives return to the `1e-10` contact threshold at about **0.00098942141752729 s** and zero gap at **0.00099952910140715 s**. Thus roughly 9.9% of the native interval is resolvable free flight before return. This is not an unresolved sub-tolerance excursion.

Actual production output is one **0.01 s sustained source contact**, with no release, no free interval and no return event. Source transfer is **9.858939985959484e-06** and damage is zero. Source/body conservation still balances, but conservation cannot validate an incorrect contact duration.

This violates the same selected event-law requirement as R1: actual source exchange belongs to positive-duration contact, not preceding free flight. Authority remains the exact P implementation specification §§7.2/8.2 and the build handoff's physical-contact verification requirement. It is not a claim about the scientific adequacy of P or a demand for a different mechanics model.

The review-only `test_oblique_release_review.py` was executed against the current checkpoint and **failed its intended assertion**: `Resolved oblique separation was kept as sustained contact`. See `oblique-release-current-RED-attempt-002.txt`.

An additional direct diagnostic supplies the known-clear half-return point to the existing `first_collision` function without running a modified physical trajectory. That search hits `ArithmeticError: Swept contact search iteration limit` (`physics.py:145-158`). Therefore simply forcing this state to release is not a complete closure; its swept return must also be located within the declared event law. This secondary result is a direct search-component observation, not an assertion that the untouched `advance` currently raises: untouched `advance` instead silently retains contact as described above.

**Smallest closure:** recognize and locate this resolved oblique separation/return under the same finite-step law and existing tolerances; account only the resulting contact durations; add a consequential regression for it while retaining the original R1 and conservation/stress/native-cadence falsifiers. No P redesign, parameter tuning or tolerance relaxation is indicated.

## VERIFIED — four independently executed physical mutation pairs

The delivered mutant helper was inspected, then each named fault was run in a fresh subprocess against its actual designated test, followed by a fresh unmutated subprocess:

| Fault | Observed RED | Observed GREEN |
|---|---|---|
| `release_disabled` | Exit 1, release assertion failed | Exit 0, 1 passed |
| `double_source_debit` | Exit 1, stock-balance assertion failed | Exit 0, 1 passed |
| `damage_suppressed` | Exit 1, integrity/damage-balance assertion failed | Exit 0, 1 passed |
| `native_repeated` | Exit 1, exact native/field call list failed | Exit 0, 1 passed |

Eight independent logs are present next to this report. These falsifiers are consequential for their fixtures. They do not test the conservative-bound false-negative exposed above. Existing release fixtures in `test_corrective_contracts.py:19-63` use the axial original counterexample and outward/rest/tangent cases, without a mostly tangential force plus small outward normal velocity.

## VERIFIED — inspected delta scope

The production physics diff adds `release_probe`, guarded release-aware swept search, release records and pending recontact records/endpoint processing. Those changes belong to R1. The changed physical test compares diffusion at identical mover time/phase and belongs to R3; changed terminal scheduler test indices belong to R3. No changed line in the inspected physics diff alters `account`, actuator strength, free velocity, mass/drag, source renewal, damage/repair parameters, body geometry, optics or neural arithmetic. Whole-repository scope/provenance and the other R3 mutants are covered by the coordinating review.

## LIMITATION / EXPECTED PROVISIONAL CHOICE

These are detached deterministic physical components, not organism lifetimes, capacity sweeps or commissioning evidence. Pending-endpoint handling used an explicit locator stand-in. Finite-force/orientation/contact-normal integration remains the selected uncommissioned model; this review does not require a different model or establish general convergence. The scoped failure above is an internal event-law inconsistency within that model.

No target repository, configuration, source evidence or Workbench file was modified. Only this new review-evidence directory was written. A first external-test invocation failed during pytest root discovery with an inaccessible Windows junction; it did not execute the component. Its log is preserved as `oblique-release-current-RED.txt`. Explicit root/collection boundaries yielded the subsequent intended assertion failure.

## Reproduction commands

From the target `developmental_ecology` directory, using the existing `.venv` and bytecode/cache writes disabled:

```powershell
& '..\.venv\Scripts\python.exe' -B -X utf8 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-23-p-post-correction-review-f7eb6f27\physics\reproduce_physics_delta.py'
```

The review script writes only its sibling evidence JSON. For the current-checkpoint RED regression, let `$reviewPhysics` denote that same new review `physics` directory:

```powershell
& '..\.venv\Scripts\python.exe' -B -X utf8 -m pytest "$reviewPhysics\test_oblique_release_review.py" --rootdir "$reviewPhysics" --confcutdir "$reviewPhysics" -q -p no:cacheprovider --tb=short
```

Each delivered physical RED pair can be repeated with `verify_correction_mutants.py --child <name>`; the unmutated test is `tests/test_corrective_contracts.py::test_touch_release_return_duration_and_accounting` for the first three, and `tests/test_corrective_contracts.py::test_release_subdivision_does_not_repeat_native_or_noise` for `native_repeated`. Use `-B -X utf8`, and `-p no:cacheprovider` on the unmutated pytest invocation.
