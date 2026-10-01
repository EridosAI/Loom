# A3 proposed procedure — one actual-damage → repair → energy case

PROPOSED / NOT AUTHORIZED. Preparation only. No case has been executed. The exact A3 manifest and its canonical authority hash are the prospective review object. Prior A1/A2 grants do not authorize it.

Use unchanged P `6bc9683b54e4fa80136fe8534d7713e2a250a95f` and apparatus `5f07748102cb5eaa302569c87efbae095050e9fe`. One external privileged waypoint case; inactive P; no births, learning test or alternative low-E/I arm. No component suite, replay, dynamic probe or performance benchmark is proposed. Source laws, repair/damage laws, parameters, controller gains, body/world geometry and configuration stay byte-identical.

## Exact initial fixture

Load `INITIAL_A3.snapshot.json.gz`, not a regenerated body or world. At t=0/native index 0, body centre (2.5,6), angle pi radians (west), radius 0.5, E=0.7, I=1, velocity (0,0), angular velocity 0, both commands/forces zero and all contact rates zero. All eight stocks are 0.2. No contact or damage has occurred. The complete snapshot fixes every remaining state component.

This is a manufactured external geometry start, not a sampled newborn and not a continuation of A1 or A2. It derives from the preserved A1 zero-time snapshot by changing only body position, recomputing its deterministic instantaneous raw sensors at time zero, and labelling that provenance. Angle, E/I, other body fields, inactive organism, RNG state, solver, fields and clock are unchanged. No Engine constructor, new random draw, prehistory regeneration or world step is used. The inactive organism retains its original constructor history, as in the reviewed A1 fixture; it does not control or learn in this arm.

Use the same life-0 verified 600-second body-absent field history, master seed 5284097 and phase 3.558411277237072. Field hash `7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096`; cache receipt `847b07eae82aeb9eeabefad7f5b9f84254e2e9324a1e93d0ff89909958019ac3`. This old history is reused, never rerun. Complete fixture/provenance hashes are in `INITIAL_STATE_SUMMARY.json`.

## One geometrically selected interaction and route

Damage target: plain left arena wall `wall-0`, x=0, around y=6. This is below the restorative strip, whose y-range is 8–12. The healthy body approaches west over 2 units of body-centre travel to nominal contact centre (0.5,6). The ordinary solver's normal collision must supply any injury. No damage amount is stipulated, no I≈0.8 target is pursued, and no direct integrity write or ledger injection is permitted after launch. All initial-impact loss, later stress loss, overshoot and terminal outcomes stand.

Repair target: existing `repair-0`, rectangle [0,0.25] × [8,12], approached at its interior face x=0.25, y=10 (nominal body centre x=0.75). Its geometry/material is unchanged. The centre corridor x=1.5 is clear of this strip and source-3; it is left of the mover's complete swept rectangle. Energy destination: existing `source-3`, centre (3,10), radius 0.5, approached from its left (nominal body centre (2,10)). No source is moved, replenished or enlarged for the case.

The six fixed stages below are the complete typed prescription. Times are absolute from the one initial state. Each command is held 0.1 s under the unchanged 0.01 s physical cadence. Target points inside solids instruct approach/press; the solver determines actual body position and contact. Geometric segments in `GEOMETRY.json` stop at finite-body contact loci, not inside solids.

| Time interval (s) | Target point | Press-force target | Intended action |
|---|---|---|---|
| 0–15 | (0,6) | 0.1 | Approach the ordinary wall once; actual impact, then gentle commanded contact |
| 15–40 | (1.5,6) | 0 | Turn away and release the damage wall |
| 40–75 | (1.5,10) | 0 | Travel north through the left corridor with actual damaged state |
| 75–155 | (0,10) | 0.1 | Approach the existing repair strip and seek eligible contact/restoration |
| 155–180 | (1.5,10) | 0 | Turn away and release the repair surface |
| 180–210 | (3,10) | 0.1 | Approach source-3, seek actual transfer, stop at the horizon |

Controller constants are unchanged: heading_gain 0.8; angular_damping 0.2; distance_gain 0.5; speed_damping 0.4; force_gain 0.4; turn_bound 0.5; drive_bound 0.5; maximum_target_force 0.25; heading_distance_epsilon 1e-12. The full function and live-dispatch identities are bound in the manifest. It receives only its existing closed privileged physical inputs. The force servo responds to any measured contact; it does not recognize the requested surface. Both departure stages therefore have zero press target. Unexpected contacts, persistent contact, force overshoot or route deviations remain reportable limitations.

### Explicit timing interpretation for Jason's review

The existing waypoint controller switches by fixed clock, not by damage or restoration events. The 15-second damage phase therefore does not stop at first injury, and departure at 155 seconds does not wait for restoration. The 0.1 force target is inside the existing gentle range, but achieved force and subsequent injury are observations, not guaranteed values. This deliberately does not implement the original design draft's optional operator I≈0.8 stopping policy or add an event-driven controller.

The intended complete witness requires real nonterminal damage, positive repair, actual departure and energy transfer in that order. If positive restoration has not occurred before actual repair departure, later energy contact cannot be reported as the complete A3 recovery witness. The fixed prescription still ends as written; no observer feedback, waiting-until-success, early result-selected phase change, route substitution or extension. This timing interpretation is a visible part of the proposed authority object, not a claim that the ordering has already been achieved.

## Horizon and reserves

210 seconds = at most 21,000 native steps and 2,100 command decisions. Allocations are 15 seconds for wall approach, 25 for release/turn, 35 for 4-unit corridor travel, 80 for repair approach/contact, 25 for repair release/turn and 30 for the nearby source. These are prospective allowances, not measured A3 arrival times. The 80-second repair allocation leaves room for alignment and a finite positive increment; there is no full-repair requirement. At force 0.1 and zero relative contact speed, the unchanged repair quality is 0.3 and rate constant 0.006/s. Seventy seconds at that ideal contact would restore about 34% of the then-existing deficit, but actual force, speed, damage and contact duration determine the result. This calculation selected a finite observation opportunity, not a trajectory outcome or acceptance percentage.

With valid commands, expense is bounded above by 0.0025/s. Starting E=0.7 gives the arithmetic no-intake lower envelope E≥0.7−0.0025t while viable: 0.3125 at t=155, 0.25 at t=180 and 0.175 at t=210. This leaves reserve margin without increasing birth energy or changing the world. It does not guarantee actuator competence, nonterminal I, timely arrival, repair or transfer. The 240-second historical proposal is not inherited automatically.

Actual A1/A2 long-run projections and limits are in `BUDGET.json`: expected extrapolated wall time roughly 41–47 minutes; proposed hard runner ceiling 4,200 seconds (70 minutes), uncompressed stream limit 1,500,000,000 bytes, primary/analysis/delivery disk budget 3,000,000,000 bytes. Reserve that free space before launch. The wall/storage checks occur between native steps, so one in-flight step and final record flushing may finish after a threshold; no hard process kill or unbounded continuation is proposed. Snapshot history costs can grow nonlinearly. Allow separately at most 3,600 machine seconds of read-only validation/reporting/packaging, zero additional world steps. No performance probe is authorized by this plan.

## Prospective launch boundary and evidence

Only a later genuine Jason approval of the exact canonical object can permit launch. Recheck live code/runtime, all bound files, cache, initial snapshot and empty prospective destination. Use the existing production manifest/state/history and dispatch validation. Preserve the actual authorization source and exact approved object. Construct one fresh `Run` with the unchanged `diagnostics.passive` observer, its typed plan and resource limits. Ordinary holds only; no manual commands, live viewer, online evaluator feedback or interactive inspector. Never reuse an old grant or fabricate one. The dormant legacy birth roster remains execution_authorized=false.

Stop on the first ordinary terminal, apparatus failure, administrative resource pause or t=210 cutoff. Record the actual stop/cause, coverage and any unobserved tail. No retry, restart, resume, continuation, patch, parameter adjustment, new prehistory or extra case follows. Preserve incomplete evidence on failure. No Git operation, push, PR, merge, experiment number or evidential freeze.

Retain every native, event, controller, diagnostics and sensor record, initial/final and every 1,000-native restart, and all original manifests. The external arm has zero neural wave records. Preserve native pose/orientation/E/I/commands/realized forces/stocks; contact IDs/normals/impulses/forces/relative speeds; damage/restoration/repair-quality/expenditure/intake/renewal operands; phase and actual mover geometry/velocity at controller cadence; exact event times and ordering. Raw sensor records are available for later passive-viewer extension. No viewer is built or launched now. Existing external diagnostics do not label mover light-ray hits; that limitation remains.

After the sole attempt, validate saved data without resimulating or recomputing controller commands: hashes, continuity, ledger residuals, input schema, issued-versus-delivered commands, snapshot inactive-organism/RNG identity and phase/field coverage. Use the initial sensor envelope plus native rows correctly. Do not invoke production `verify_segment` under a no-controller-recompute report scope, because it recalculates commands. Report all observations using `INTERPRETATION.md`; failed validation restricts the affected claim and is not patched in place.
