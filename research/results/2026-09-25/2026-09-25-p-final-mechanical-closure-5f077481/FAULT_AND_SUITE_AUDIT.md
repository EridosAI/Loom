# Delivered fault/control and suite audit

All 54 pairs / 108 logs reach their intended RED exception and GREEN control. Collection: 59 + 24 + 30 + 30 = 143; no test bodies executed by collection.

| Matrix | Fault | Reached assertion | RED | GREEN |
|---|---|---|---|---|
| previous-16-pairs-001 | identity | manifest/code identity mismatch | 1 failed in 0.81s | 1 passed in 0.78s |
| previous-16-pairs-001 | missing_native | missing native record | 1 failed in 0.82s | 1 passed in 0.75s |
| previous-16-pairs-001 | phase | wrong field/mover phase | 1 failed in 0.81s | 1 passed in 0.78s |
| previous-16-pairs-001 | ledger | source debit/body credit mismatch | 1 failed in 0.44s | 1 passed in 0.38s |
| previous-16-pairs-001 | input | forbidden controller input | 1 failed in 0.49s | 1 passed in 0.46s |
| previous-16-pairs-001 | observer | observer RNG/state interference | 1 failed in 0.51s | 1 passed in 0.46s |
| previous-16-pairs-001 | stop | mislabelled stop reason | 1 failed in 0.80s | 1 passed in 0.76s |
| previous-16-pairs-001 | sensor_leak | privileged data leakage into sensor-only interface | 1 failed in 0.48s | 1 passed in 0.43s |
| previous-16-pairs-001 | label | external controller incorrectly labelled intact P | 1 failed in 0.79s | 1 passed in 0.77s |
| previous-16-pairs-001 | frozen | frozen structural parameter changed | 1 failed in 0.55s | 1 passed in 0.48s |
| previous-16-pairs-001 | discarded | discarded structural update affected later output/state | 1 failed in 1.07s | 1 passed in 1.00s |
| previous-16-pairs-001 | duration | manifest changed during run | 1 failed in 0.86s | 1 passed in 1.05s |
| previous-16-pairs-001 | extra_updates | extra native/wave/random/field updates introduced by controller hold | 1 failed in 2.20s | 1 passed in 2.60s |
| previous-16-pairs-001 | extra_native | extra native/wave/random state change from external hold | 1 failed in 2.33s | 1 passed in 2.79s |
| previous-16-pairs-001 | extra_wave | extra native/wave/random state change from external hold | 1 failed in 2.78s | 1 passed in 2.70s |
| previous-16-pairs-001 | extra_random | extra native/wave/random state change from external hold | 1 failed in 2.25s | 1 passed in 2.65s |
| previous-20-pairs-001 | authority-implementation | APPROVAL BINDING BREACH: implementation | 1 failed in 0.85s | 1 passed in 0.85s |
| previous-20-pairs-001 | authority-constants | APPROVAL BINDING BREACH: constants | 1 failed in 0.85s | 1 passed in 0.87s |
| previous-20-pairs-001 | authority-route | APPROVAL BINDING BREACH: route | 1 failed in 0.90s | 1 passed in 0.87s |
| previous-20-pairs-001 | authority-stage_sequence | APPROVAL BINDING BREACH: stage_sequence | 1 failed in 0.83s | 1 passed in 0.81s |
| previous-20-pairs-001 | authority-contact_target | APPROVAL BINDING BREACH: contact_target | 1 failed in 0.81s | 1 passed in 0.81s |
| previous-20-pairs-001 | authority-manual_fallback | APPROVAL BINDING BREACH: manual_fallback | 1 failed in 0.81s | 1 passed in 0.82s |
| previous-20-pairs-001 | authority-sensor_interface | APPROVAL BINDING BREACH: sensor_interface | 1 failed in 0.80s | 1 passed in 0.83s |
| previous-20-pairs-001 | authority-intact_arm | APPROVAL BINDING BREACH: intact_arm | 1 failed in 0.82s | 1 passed in 0.82s |
| previous-20-pairs-001 | authority-fixed_adapter | APPROVAL BINDING BREACH: fixed_adapter | 1 failed in 0.81s | 1 passed in 0.85s |
| previous-20-pairs-001 | authority-deprivation | APPROVAL BINDING BREACH: deprivation | 1 failed in 0.80s | 1 passed in 0.81s |
| previous-20-pairs-001 | authority-initial | APPROVAL BINDING BREACH: initial | 1 failed in 0.82s | 1 passed in 0.81s |
| previous-20-pairs-001 | authority-prehistory | APPROVAL BINDING BREACH: prehistory | 1 failed in 0.80s | 1 passed in 0.82s |
| previous-20-pairs-001 | authority-duration | APPROVAL BINDING BREACH: duration | 1 failed in 0.83s | 1 passed in 0.81s |
| previous-20-pairs-001 | authority-resources | APPROVAL BINDING BREACH: resources | 1 failed in 0.81s | 1 passed in 0.82s |
| previous-20-pairs-001 | authority-runtime | APPROVAL BINDING BREACH: runtime | 1 failed in 0.80s | 1 passed in 0.81s |
| previous-20-pairs-001 | authority-procedure | APPROVAL BINDING BREACH: procedure | 1 failed in 0.80s | 1 passed in 0.87s |
| previous-20-pairs-001 | authority-replay_arm | APPROVAL BINDING BREACH: replay_arm | 1 failed in 0.80s | 1 passed in 0.85s |
| previous-20-pairs-001 | authority-request_rebind | APPROVAL BINDING BREACH: request_rebind | 1 failed in 0.82s | 1 passed in 0.84s |
| previous-20-pairs-001 | clock-transition | CLOCK BREACH: expired stage issued another hold | 2 failed, 3 passed in 0.42s | 5 passed in 0.37s |
| previous-20-pairs-001 | clock-final | CLOCK BREACH: final stage still drives | 1 failed in 0.42s | 1 passed in 0.37s |
| new-18-pairs-001 | duplicate-approved_execution | DUPLICATE APPROVAL BREACH: approved_execution | 1 failed in 0.83s | 1 passed in 0.88s |
| new-18-pairs-001 | duplicate-point | DUPLICATE APPROVAL BREACH: point | 1 failed in 0.83s | 1 passed in 0.87s |
| new-18-pairs-001 | duplicate-controller | DUPLICATE APPROVAL BREACH: controller | 1 failed in 0.84s | 1 passed in 0.87s |
| new-18-pairs-001 | duplicate-until | DUPLICATE APPROVAL BREACH: until | 1 failed in 0.84s | 1 passed in 0.85s |
| new-18-pairs-001 | duplicate-identical | DUPLICATE APPROVAL BREACH: identical | 1 failed in 0.82s | 1 passed in 0.87s |
| new-18-pairs-001 | canonical-keys | CANONICAL KEY BREACH | 1 failed in 0.46s | 1 passed in 0.42s |
| new-18-pairs-001 | approval-alias | APPROVAL ALIAS BREACH | 1 failed in 0.82s | 1 passed in 0.84s |
| new-18-pairs-001 | protocol-shadow | PROTOCOL SHADOW BREACH | 1 failed in 0.80s | 1 passed in 0.90s |
| new-18-pairs-001 | dispatch-waypoint_command | EXECUTED DISPATCH BREACH: waypoint_command | 1 failed in 1.10s | 1 passed in 1.02s |
| new-18-pairs-001 | dispatch-command_pair | EXECUTED DISPATCH BREACH: command_pair | 1 failed in 1.05s | 1 passed in 1.00s |
| new-18-pairs-001 | dispatch-privileged_input | EXECUTED DISPATCH BREACH: privileged_input | 1 failed in 1.02s | 1 passed in 0.97s |
| new-18-pairs-001 | dispatch-time_due | EXECUTED DISPATCH BREACH: time_due | 1 failed in 1.03s | 1 passed in 0.98s |
| new-18-pairs-001 | dispatch-observe_without_interference | EXECUTED DISPATCH BREACH: observe_without_interference | 1 failed in 1.06s | 1 passed in 0.99s |
| new-18-pairs-001 | pending-command | PENDING COMMAND BREACH: command | 1 failed in 2.05s | 1 passed in 2.01s |
| new-18-pairs-001 | pending-remainder | PENDING COMMAND BREACH: remainder | 1 failed in 1.98s | 1 passed in 2.05s |
| new-18-pairs-001 | pending-both | PENDING COMMAND BREACH: both | 1 failed in 1.97s | 1 passed in 2.03s |
| new-18-pairs-001 | pending-decision | PENDING COMMAND BREACH: decision | 1 failed in 1.93s | 1 passed in 1.94s |
| new-18-pairs-001 | decision-journal | DECISION JOURNAL BREACH | 1 failed in 2.16s | 1 passed in 2.81s |

The prior authority matrix contains 18 test-callback bypass faults, unchanged from the previous review. The final matrix instead restores the old parser or removes the named production check, as documented in the full review. The old clock-transition pair contains two failed and three passed RED instances; GREEN has five passed instances. Counts do not replace inspection of the actual exception and causal fault.
