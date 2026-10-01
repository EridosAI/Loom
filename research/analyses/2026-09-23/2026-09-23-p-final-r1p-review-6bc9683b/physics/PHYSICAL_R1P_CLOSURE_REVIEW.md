# Independent physical R1-P closure review

Reviewed checkpoint: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`, compared with `f7eb6f27c661e3db193a4225b56a825d7e41739d`. Semantic configuration: `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`.

**VERIFIED: the demonstrated radial/oblique R1-P class is closed in this physical subreview. No new concrete engineering defect was found in the scoped inspection.** This supports proceeding to coupling commissioning if the coordinating review's remaining delivery, regression, mutation and saved-evidence checks pass. It does not authorize or begin commissioning.

## Independently reproduced component results — VERIFIED

The exact previously failing state and the two builder variants were reproduced with an independent analytic oracle. It transcribes the specified frozen-force exponential velocity and selected displacement `p(t)=p0+t*v(t)` directly, calculates source distance with a rationalized squared-distance formula to avoid subtraction near one, and brackets the descending tolerance/zero crossings by bisection. It does not call the production release detector, free-velocity function, actuator-force function, gap geometry, or builder oracle. The original radial fixture is retained as the fourth predeclared component; this is not a geometry/parameter sweep.

| Fixed component | Oracle return to geometry tolerance | Actual free duration | Oracle zero-gap return | Actual positive contact duration |
|---|---:|---:|---:|---:|
| Exact prior oblique: normal force .01, outward speed 1e-5, positive tangent | 0.0009894214075534065 | 0.0009945075740815300 | 0.0009995291385109170 | 0.009005492425918471 |
| Normal force .02, outward speed 1e-5 | 0.0004896657399039737 | 0.0004952031080175746 | 0.0004998768431677878 | 0.009504796891982425 |
| Reflected tangent, normal force .01, outward speed 2e-5 | 0.0019932138523468474 | 0.0019947279455729630 | 0.0019982325910003850 | 0.008005272054427037 |
| Original radial: normal force .76, outward speed .001 | 0.0013148245079228596 | 0.0013149022740740090 | 0.0013149245813090734 | 0.008685097725925990 |

Each actual free duration lies within the independent spatial-resolution return interval, allowing only the declared event-time resolution. The exact fixture's reported approximately 0.000994507574-second duration is independently reproduced. Its gap at the independently chosen half-characteristic sample is 2.498143558596348e-9, approximately 25 geometry tolerances. No continuous-time position integral was substituted for the selected finite-step displacement convention.

All four cases have exactly one start release, one positive free interval, one explicit return and one positive sustained-contact interval. They terminate normally. Positive durations sum to the native 0.01 seconds within 1e-16. Free intervals have basal/effort expenditure but no source transfer, repair or contact damage. Zero-duration events have no transfer/repair. Independent per-event source renewal/debit, bodily credit/expenditure, damage and integrity balances hold within 2e-16. Requested transfer agrees with the independent duration-specific constitutive calculation within 1e-18. No duplicate release/recontact was observed.

The two additional variants are useful class checks rather than cosmetic copies. Doubling the normal force changes orientation, halves the return timescale and reduces the gap peak. The reflected variant changes the tangential direction and doubles the outward normal speed, approximately doubling the free duration and quadrupling the peak gap. Reflection alone would be a symmetry check; its simultaneous departure-speed change is a substantive timescale variation. All remain a deliberately bounded source-contact class, not arbitrary fixture coverage.

Reproduction: `independent_r1p_components.py`. Full states, events, balances, oracle roots and traces: `independent-r1p-evidence.json`. Console: `independent-r1p-console.txt`.

## Measured complete-path termination — VERIFIED

Read-only Python line tracing independently counted the actual search loops in the unchanged running functions:

| Component | Observed search/first-collision passes in call order |
|---|---|
| Exact prior oblique | search 4; prefix search 22; first_collision 15; search 74; first_collision 2 |
| Different normal force | search 5; prefix search 16; first_collision 11; search 60; first_collision 2 |
| Reflected longer flight | first_collision 31; search 74; first_collision 2 |
| Original radial | first_collision 8; search 20; first_collision 2 |

The claimed 15-pass exact-oblique sweep is reproduced independently, well inside the 500-pass limit. The whole `advance` call completes through release, free flight, return and subsequent contact. This closes the earlier subordinate failure in which a known-clear guard still exhausted the old swept search. Historical-runtime and deliberate-old-search RED controls are covered by the coordinating mutation review; they are not claimed as separately executed by this subreview.

## Search mathematics and scope — VERIFIED

All code references below are to `developmental_ecology/loom_p/physics.py` in the reviewed commit.

`motion_bounds` (`:90-95`) bounds the selected path's first and second derivatives. With gamma equal to drag/mass, velocity lies on the segment between its old and ending values. Thus `vmax + dt*amax` bounds the norm of `p'=v+s*v'`, and `(2+gamma*dt)*amax` bounds `p''=(2-gamma*s)*v'`. The bounds do not change the motion equation.

`gap_curve` (`:98-105`) differentiates the actual selected path, using `normal dot (velocity+s*acceleration-fixture_velocity)`. It includes mover motion in the relative normal rate.

`gap_curvature_bound` (`:108-122`) adds the prescribed mover's speed/acceleration bounds. For a wall, signed distance is affine and has no surface-curvature term. For other convex fixtures, `body_radius+gap` is distance from the organism centre to the fixture surface; subtracting the relative-speed bound times the candidate interval gives a conservative lower distance. When positive, `relative_acceleration + relative_speed^2/lower` bounds the gap's second derivative. For the disk this surface distance is smaller than its centre distance, so the bound is conservative. If positivity cannot be established, the function returns an infinite curvature bound and retains the global speed route. The independent source oracle's exact second derivative was also checked at three predeclared instants per fixture against the supplied enclosure; all checks passed. This numerical check supplements the algebraic reasoning rather than replacing it.

`release_probe` now calls `clear_excursion` after the cheap certificate fails (`:201-207`). `clear_excursion` (`:125-161`) evaluates actual gap geometry across the remaining interval. Its endpoint Lipschitz and `B*h^2/8` interpolation enclosures are upper bounds; an interval is discarded only when an upper bound rules out a resolvable excursion. An actual sampled clearance is required to return a guard. The preceding path is separately checked for penetration beyond geometric tolerance. Unresolved enclosures, finite-search exhaustion and a penetrating proposed prefix raise explicit `ArithmeticError`; they are not treated as retained contact.

The swept-search local increment (`:225-234`) solves

$$0.8g + g' h - \tfrac12 B h^2 = 0.$$

Together with the lower Taylor enclosure, this leaves at least `0.2g` predicted clearance. The negative-rate expression is its stable rationalized form. Both the old speed-based step and the new curvature/rate step are independently safe under their respective bounds, so taking their maximum is conservative; taking the minimum across colliders and pending guard boundaries preserves all constraints. The infinite-curvature case falls back to the global speed increment. The 500-pass swept limit remains at `:218`, with explicit failure at `:246`; physical subdivisions remain separately bounded. No native/field/neural step or random draw is performed by these searches.

The inspected physics delta introduces only event-search calculations required by R1-P. It does not alter reserve accounting, force strength, the body integrator, normal projection, source/repair/stress parameters, timestep, tolerances, optics, chemistry, P arithmetic or neural scheduling. The coordinating review checks all other changed files and identities.

## Unresolved-enclosure failure semantics — VERIFIED

A bounded in-memory test retained the actual touching-source geometry and inward-force path, replacing only the curvature helper with a valid but deliberately uninformative bound `(infinity, 1e9)`. It reached `ArithmeticError: Active-contact gap enclosure unresolved at event time tolerance` after 28 bound evaluations, at enclosure duration 7.450580596923828e-11. It did not return `None` or manufacture a sustained-contact decision. No configuration value was changed.

A separate threshold-evaluator stand-in reached the same explicit failure. These are injected branch checks, not natural physical failures or additional integration cases. Existing unchanged engine rollback/failure handling is covered by the coordinating regression suite.

Evidence: `verify_failure_semantics.py`, `failure-semantics.json`, `failure-semantics-console.txt`.

## LIMITATION / EXPECTED PROVISIONAL CHOICE

The four named components establish the demonstrated radial/materially oblique separation-return class and the tested accounting/termination properties. They do not prove arbitrary curved, grazing, simultaneous or moving-contact correctness, global finite-step convergence, natural terminal organism behavior or scientific efficacy. Finite unresolved cases may explicitly halt; that disclosed numerical limit is not itself grounds for HOLD. No additional geometry sweep or indefinite counterexample search was performed.

This subreview changed only new review-evidence files. No target code, configuration, existing artifact, source document, Workbench content or Git state was changed. No organism was constructed, and no freely acting life, commissioning case, prehistory or efficacy run was started.

## Exact reproduction commands

From `C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\developmental_ecology`:

```powershell
& '..\.venv\Scripts\python.exe' -B -X utf8 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-23-p-final-r1p-review-6bc9683b\physics\independent_r1p_components.py'
& '..\.venv\Scripts\python.exe' -B -X utf8 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-23-p-final-r1p-review-6bc9683b\physics\verify_failure_semantics.py'
```

These commands write only their sibling review JSON receipts. They do not modify the target runtime or run an organism.
