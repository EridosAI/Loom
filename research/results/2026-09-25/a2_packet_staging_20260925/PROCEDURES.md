# Proposed A2 execution procedure — awaiting Jason

This is one proposed physical-ceiling case, `A2`, using P `6bc9683b54e4fa80136fe8534d7713e2a250a95f` and apparatus `5f07748102cb5eaa302569c87efbae095050e9fe`. Preparation is authorized; execution is not. The approval-bearing object is `AUTHORITY_OBJECT.canonical.json`; its SHA-256 is in `AUTHORITY_SHA256.txt`. `A2_MANIFEST.json` has `execution_authority: null`. Historical A1 approval inside reference archives grants nothing to this case.

## Initial fixture

Load the exact proposed `INITIAL_A2.snapshot.json.gz` only after separate approval. It is a byte-identical copy of the **zero-time initial A1 fixture**, newly labelled A2 in this packet and manifest. It is not A1's final restart, a continuation, or a reset within a trajectory. The reviewed restart machinery binds continuation to the original manifest and hard ceiling; no new-authority continuation is proposed.

The body starts at (6,3), angle pi (west), velocity (0,0), angular velocity 0, E=0.7, I=1, zero commands, realized forces and contact rates. Native index/time are zero, status paused, event/native history empty. All eight stocks are 0.2. Complete raw input, inactive neural object, RNG state, solver state, constructor provenance and field history are preserved in the snapshot. The manufactured body placement is not a sampled newborn. The inactive neural object retains its original construction history exactly; it is not reinitialized for A2.

First source: `source-0`, centre (3,3), radius 0.5. Second: `source-1`, centre (10,3), radius 0.5. Body radius 0.5. Expected geometric contact loci along the prescribed centre line are (4,3) and (9,3). These are geometry, not predicted observed positions. Other sources, three restorative strips, walls, mover, fields and all physical laws are unchanged.

Phase is 3.558411277237072, using the existing verified life-0 cache from master seed 5284097. Field SHA-256 is `7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096`; original cache receipt SHA-256 is `847b07eae82aeb9eeabefad7f5b9f84254e2e9324a1e93d0ff89909958019ac3`. The historical body-absent 600-second prehistory is reused; none is regenerated. It is not a claim of stationary chemistry.

## Exact fixed stages

| Absolute simulated time | Waypoint | Existing contact-force target | Intended observation |
|---|---|---|---|
| 0 <= t < 90 | (3,3) | 0.1 | Approach source 0 and remain while local opportunity declines |
| 90 <= t < 120 | (6,3) | 0 | Turn away, separate and travel to the original starting point |
| 120 <= t < 180 | (10,3) | 0.1 | Approach the different source 1 and remain in productive contact if available |

The manifest's typed stage values are authoritative. Every boundary is on the unchanged 0.1-second hold grid. Commands remain bounded left/right actuator commands, computed by the reviewed deterministic waypoint controller. There are no event-triggered stage changes. Departure is commanded at 90 seconds whether or not first contact/transfer occurred. Transition at 120 and cutoff at 180 are not extended for delayed arrival, empty stocks, controller difficulty or a promising result.

The existing gains/constants are heading_gain 0.8, angular_damping 0.2, distance_gain 0.5, speed_damping 0.4, force_gain 0.4, turn_bound 0.5, drive_bound 0.5, maximum_target_force 0.25 and heading_distance_epsilon 1e-12. Native dt remains 0.01 seconds; each command owns ten native steps unless a reviewed stop ends it earlier. No controller command was computed during packet preparation.

The existing positive-target contact servo responds to **any recorded contact**, not a filtered source identity. Stage 2's zero press target selects the controller's existing free-space steering branch so residual source-0 contact cannot keep the positive-target press servo engaged. This is a stage prescription, not a gain or controller change. Rotation, separation and acquisition of source 1 remain untested outcomes. An unexpected contact when stage 3 begins could still affect its servo; report it without repair or a new route.

## Selection rationale and horizon

Reuse the actual A1 start, phase, source-0 approach and target force. A1's first negative complete contact window was 52.0–52.2 seconds, with positive transfer and expenditure greater than that transfer. A fixed 90-second first stage retains roughly 38 seconds beyond that historical transition. The A2 transition remains an observation, not an assumed repeat or an outcome-triggered switch. No exactly-zero stock target exists.

Source 1 is the nearest different source from the first source's right contact locus: centres of the body would travel five units from (4,3) to (9,3). Source 3, equally distant from source 0's centre, is farther from that contact locus and requires leaving the bottom row. Source 1 needs no mover crossing, repair visit or additional intermediate fixture. The intermediate point (6,3) reuses the initial point, separating departure from the second contact stage. The nominal line has 2.5 units of wall clearance and at least 6 units of body-surface clearance from the mover's entire swept rectangle; other geometry clearances are in `GEOMETRY.json`. This clearance applies to the declared line, not an enforced rail or a prediction of the controller's actual track. All movers and fields keep evolving.

The 30-second departure/transit allowance is intended for a half-turn and two units of travel to the intermediate point. A further 60 seconds permits the three-unit approach from that point to source-1 contact and a residence interval. A1 crossed its initial two-unit free approach in approximately 6.31 seconds; that is a scale reference, not a tested bound on departure or the new approach. This allocation is a fixed practical proposal; controller sufficiency has not been demonstrated. It is substantially below the old 400-second per-case design ceiling and does not inherit that draft's two-case count.

## Unchanged recording and observation

Use the exact reviewed `Run` and `diagnostics.passive`, with the existing native, wave, events, controller, diagnostics, sensor and scientific_observations streams. Retain every native record, all eight stocks, physical E/I, intake/expenditure, stock renewal/debit/transfer, body trajectory, issued/delivered commands, realized forces, contact impulses and positive-duration forces, accounting residuals, field identities and actual mover data. Keep initial/final and every-1000-native-step restart snapshots. Preserve the initial sensor envelope plus endpoint rows. External neural state stays inactive; zero neural waves is expected for this arm, not missing intact-P evidence.

Mover rectangles/velocity in privileged controller inputs have the existing decision cadence (0.1 seconds); physical events and saved phase/time supplement them. A future passive viewer must label that cadence instead of presenting interpolated mover positions as recorded 100 Hz geometry. No live visualization, extra observer, downsampling or stream removal is proposed. `INTERPRETATION.md` predeclares parallel outcomes and time/accounting conventions. Reading saved evidence is separate from simulation; physical replay and sensory replay are excluded.

## Resource ceilings and stops

Proposed case ceiling: **180 simulated seconds**, at most 18,000 native steps and 1,800 command decisions. Reviewed runner wall ceiling: **3,600 seconds**. Stream storage ceiling: **1,500,000,000 uncompressed bytes**, unchanged from A1. Reserve **3,000,000,000 free local disk bytes** for trajectory, growing restart histories, derived review and portable copy. The stream ceiling does not itself cap snapshot/archive disk usage; this free-space reserve is a launch precondition, not a new live disk monitor. `BUDGET.json` distinguishes all measures and records actual A1 operands.

Actual A1 average throughput projects 39.24 minutes for 180 seconds; its recorded tail since 71.8 seconds projects 40.43 minutes. The 60-minute runner ceiling provides about 53% headroom over the average, not a completion guarantee. History validation and snapshots may grow in cost, and host load may differ. Stream/trajectory linear projections are about 106.5 MB/49.0 MB; snapshot growth and route-dependent event volume make these planning estimates. The old 400-second horizon would project about 87.2 minutes even at the A1 average. No speed, fidelity, law or recording change is used to fit this shorter proposal.

After the first stop, preserve and report. Reviewed categories remain `terminal`, `apparatus_failure`, `administrative_pause` and `administrative_cutoff`, with exact cause and completeness. Wall/storage checks occur before further advancement; finishing a native operation and record closure may add wall time beyond the nominal budget. Clean resource stops do not authorize continuation. An I/O error is an apparatus failure, not a clean administrative pause. An operator interruption must retain its actual cause. No retry, resume, second fixture, manual override, alternate controller, new phase, tuning, patch or automatic background continuation is included.

## Later launch steps — conditional on explicit approval of this exact object

1. Preserve Jason's genuine approval text and bind the apparatus's normal approval envelope to this exact canonical object. Do not synthesize consent from the historical A1 envelope. Confirm typed manifest, all bound file hashes, live source/runtime/configuration identities and cache match. If anything differs, stop and report.
2. Confirm the exact proposed destination is absent, the local disk reserve is available and the pinned runtime works. Read the exact zero-time snapshot. Run production manifest/state/history and execution/dispatch validation before constructing the one `Run`. Keep original snapshot, proposed null-grant manifest, canonical object and later launched grant separately.
3. Construct one `Run` at the bound new `trajectory-001` destination using `diagnostics.passive` and the unchanged typed route/resources. Fresh session cursor=0, no pending decision, no command history; the runner establishes these normally. Call its ordinary holds without manual commands until the first stop. Do not initialize a new Engine, generate prehistory, or load A1's final restart.
4. Preserve all raw evidence and perform read-only receipt/accounting/input-boundary analysis only. Use the corrected V3 initial-envelope alignment as the documented rule, never the historical failed equal-count assumption. Any new A2-specific analysis must be labelled/versioned; the A1 checker is archive-bound and is not claimed to be an already implemented A2 analyzer. No suite execution, physical replay, dynamic probe or newly computed controller comparison is included.
5. Report all predeclared A2 observations and failures without patching. Post-run read-only reporting/package work is proposed within a separate maximum 1 machine-hour and the same disk reserve; it grants zero world/field/neural steps. Stop for review. No new viewer build, other commissioning case, newborn life, scientific test, experiment number, preregistration or freeze is included.

No Git write, code/configuration change, push, PR, merge or preserved-source modification is proposed. R and all alternatives retain their prior status.
