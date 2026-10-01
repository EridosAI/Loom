# A4 proposed three-case launch plan — no execution authorization

P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Apparatus: `5f07748102cb5eaa302569c87efbae095050e9fe`.

These are three independent privileged external-controller physical witnesses. They use the finite radius-0.5 body, real paired actuators, unchanged world and reserves. They do not exercise P learning or perceptual control. Each begins from its own healthy, manufactured, stationary zero-time fixture, with E=0.7, I=1, full stocks, the same verified life-0 field history and phase 3.558411277237072. None continues A1, A2, A3 or another A4 case. The stored inactive organism and RNG are retained unchanged from the original zero-time A1 fixture; these starts are not sampled newborns.

| Case | Initial centre; heading | Fixed waypoint prescription | Ceiling | Intended physical question |
|---|---|---|---:|---|
| A4-CROSS | (10, 8.8); north, pi/2 | Target (10, 12) from t=0 through t=16; press_force=0 | 16 s | Can the finite body traverse the mover's path in the available early window? |
| A4-WAIT | (6, 8.8); north, pi/2 | Target its own stationary centre (6, 8.8) through t=12; then (6, 12) through t=28; press_force=0 throughout | 28 s | Can the ordinary actuator interface implement a wait and then a crossing? Immediate progress conflicts with the moving body; the prescribed later interval is clear. |
| A4-DETOUR | (1.5, 6); north, pi/2 | Target (1.5, 14) from t=0 through t=32; press_force=0 | 32 s | Can the actual body traverse the exact always-clear left bypass declared by A0? |

All velocities, angular velocity, commands, realized forces and contact rates initially zero. No initialized damage. No mid-case resets. The detour has different endpoints from the crossings: it is the already-declared independent bypass witness, not a comparison of competing routes between identical endpoints. Its nominal length is 8 m; each crossing's nominal length is 3.2 m. Actual distances, deviations and costs must be reported.

## Selection grounds fixed before execution

The cached phase is reused because it already has a verified lawful field history. No phase search, fresh prehistory, route rehearsal, controller call, or candidate trajectory was performed. The symmetry line x=10 supplies a direct crossing during the initial leftward recession. For waiting, x=6 is the mover's leftmost centre coordinate, placing immediate northward progress in the impending occupied region while preserving a safe stationary start below it. A 12-second clock release falls after that occupancy and leaves a full crossing interval. The detour is copied from `A0_GEOMETRY.json`, not selected by a new path search.

The mover remains centre (10+4 sin(2 pi t/30+phase), 10), size 2 by 1, period 30 s. `GEOMETRY_AND_TIMING.json` records closed-form threshold times, static finite-body gaps and the immediate-proceed conflict argument. The mover's swept region is used only to certify the always-clear detour; it is not a permanent obstacle for CROSS or WAIT. Stationary WAIT has at least 0.2 m clearance from the mover throughout its waiting interval.

The unchanged waypoint controller uses heading gain 0.8, angular damping 0.2, distance gain 0.5, speed damping 0.4, force gain 0.4, turn and drive bounds 0.5, maximum target force 0.25, and heading-distance epsilon 1e-12. Its privileged input contains pose, velocity, E/I, commands, geometry, mover phase/velocity, stocks, contacts and time. These are external controller inputs, not information available to P. It issues paired commands every 0.1 s. No manual override or contact servo is selected (all target contact forces are zero).

During the stationary WAIT stage, targeting the current centre with zero velocity and angular velocity gives zero drive and turn algebraically through the same waypoint interface. No new waiting controller or force clamp is introduced. At t=12, the existing fixed-clock stage transition proceeds regardless of observed mover position or success. Fields, costs and mover time continue normally during waiting. Any deviation from the expected zero commands is retained and reported.

These short ceilings pose one crossing opportunity each and an 8 m straight bypass with ordinary approach/settling allowance. The approximate healthy straight-drive speed is 0.38 m/s initially and falls with energy. This is a scale estimate, not an integrated or tested trajectory. The 16 s movement allowance is shared by CROSS and WAIT; DETOUR receives 32 s. No claim of a mathematically minimal horizon or time/energy optimality is made.

## Execution boundary after separate approval only

Execute in order CROSS, WAIT, DETOUR, one fresh Run per exact case, at most once each. Use the unchanged passive observer, full existing recorder and the exact destination in each manifest. A completed case at its time ceiling or a bodily terminal event does not select or change the next predetermined case. An apparatus failure, failed preflight, unexpected exception, resource cutoff or operator pause stops the batch; remaining cases are explicitly unattempted. No retries, resumes, continuations, extension, route/phase replacement, controller switching, tuning or extra case are included.

Normal time ceilings are the unchanged runner's administrative_cutoff. Bodily terminal events stop that case. Apparatus faults stop as apparatus_failure; incomplete output is not bodily death. Resource limits cause a clean administrative_pause if the recorder can preserve it; no resume is authorized. Arrival, contact, damage, delay and a controller miss are observations, not new runtime stop or rescue policies. Continue to the declared time ceiling unless an existing stop applies; do not terminate early because a result looks sufficient. Preserve complete and failed records.

The prospective launch preflight must check exact live code/runtime/configuration, all packet hashes, each initial snapshot, phase-matched cache and absent output destinations, then the unchanged production manifest/history validators. No dependency installation or substitution is included. A genuinely missing or changed runtime/cache is a blocker, not permission to regenerate it. The production history validator draws into a detached verifier RNG; this is not a new prehistory or trajectory. It has not been invoked during this preparation.

`BATCH_EXECUTION_RULES.md` explains how one future explicit approval binds the three existing per-case grant envelopes. The packet contains no live grants, launch process, scheduler or renderer. Read-only reporting after an authorized run must use saved records, without controller recomputation, world replay or neural execution. Stop after preserving the three attempted/unattempted outcomes and delivering the report.
