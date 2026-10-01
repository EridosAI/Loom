# Independent delivered regression audit

59 pairs / 118 logs reach the intended RED exception and GREEN control. Suite collection is 59 P + 24 original apparatus + 30 prior correction + 30 final correction + 33 clock cases = 176.

| Matrix | Fault | Actual intended failure | RED | GREEN |
|---|---|---|---|---|
| apparatus-faults | identity | manifest/code identity mismatch | 1 failed in 0.76s | 1 passed in 0.74s |
| apparatus-faults | missing_native | missing native record | 1 failed in 0.77s | 1 passed in 0.73s |
| apparatus-faults | phase | wrong field/mover phase | 1 failed in 0.76s | 1 passed in 0.71s |
| apparatus-faults | ledger | source debit/body credit mismatch | 1 failed in 0.41s | 1 passed in 0.34s |
| apparatus-faults | input | forbidden controller input | 1 failed in 0.44s | 1 passed in 0.42s |
| apparatus-faults | observer | observer RNG/state interference | 1 failed in 0.47s | 1 passed in 0.45s |
| apparatus-faults | stop | mislabelled stop reason | 1 failed in 0.74s | 1 passed in 0.68s |
| apparatus-faults | sensor_leak | privileged data leakage into sensor-only interface | 1 failed in 0.45s | 1 passed in 0.41s |
| apparatus-faults | label | external controller incorrectly labelled intact P | 1 failed in 0.74s | 1 passed in 0.73s |
| apparatus-faults | frozen | frozen structural parameter changed | 1 failed in 0.47s | 1 passed in 0.45s |
| apparatus-faults | discarded | discarded structural update affected later output/state | 1 failed in 0.99s | 1 passed in 0.94s |
| apparatus-faults | duration | manifest changed during run | 1 failed in 0.86s | 1 passed in 0.98s |
| apparatus-faults | extra_updates | extra native/wave/random/field updates introduced by controller hold | 1 failed in 2.11s | 1 passed in 2.52s |
| apparatus-faults | extra_native | extra native/wave/random state change from external hold | 1 failed in 2.15s | 1 passed in 2.43s |
| apparatus-faults | extra_wave | extra native/wave/random state change from external hold | 1 failed in 2.53s | 1 passed in 2.48s |
| apparatus-faults | extra_random | extra native/wave/random state change from external hold | 1 failed in 2.16s | 1 passed in 2.53s |
| correction-faults | authority-implementation | APPROVAL BINDING BREACH: implementation | 1 failed in 0.80s | 1 passed in 0.79s |
| correction-faults | authority-constants | APPROVAL BINDING BREACH: constants | 1 failed in 0.81s | 1 passed in 0.78s |
| correction-faults | authority-route | APPROVAL BINDING BREACH: route | 1 failed in 0.76s | 1 passed in 0.81s |
| correction-faults | authority-stage_sequence | APPROVAL BINDING BREACH: stage_sequence | 1 failed in 0.79s | 1 passed in 0.78s |
| correction-faults | authority-contact_target | APPROVAL BINDING BREACH: contact_target | 1 failed in 0.78s | 1 passed in 0.80s |
| correction-faults | authority-manual_fallback | APPROVAL BINDING BREACH: manual_fallback | 1 failed in 0.77s | 1 passed in 0.79s |
| correction-faults | authority-sensor_interface | APPROVAL BINDING BREACH: sensor_interface | 1 failed in 0.76s | 1 passed in 0.80s |
| correction-faults | authority-intact_arm | APPROVAL BINDING BREACH: intact_arm | 1 failed in 0.78s | 1 passed in 0.86s |
| correction-faults | authority-fixed_adapter | APPROVAL BINDING BREACH: fixed_adapter | 1 failed in 0.80s | 1 passed in 0.79s |
| correction-faults | authority-deprivation | APPROVAL BINDING BREACH: deprivation | 1 failed in 0.78s | 1 passed in 0.80s |
| correction-faults | authority-initial | APPROVAL BINDING BREACH: initial | 1 failed in 0.77s | 1 passed in 0.78s |
| correction-faults | authority-prehistory | APPROVAL BINDING BREACH: prehistory | 1 failed in 0.78s | 1 passed in 0.78s |
| correction-faults | authority-duration | APPROVAL BINDING BREACH: duration | 1 failed in 0.80s | 1 passed in 0.81s |
| correction-faults | authority-resources | APPROVAL BINDING BREACH: resources | 1 failed in 0.81s | 1 passed in 0.80s |
| correction-faults | authority-runtime | APPROVAL BINDING BREACH: runtime | 1 failed in 0.78s | 1 passed in 0.78s |
| correction-faults | authority-procedure | APPROVAL BINDING BREACH: procedure | 1 failed in 0.79s | 1 passed in 0.80s |
| correction-faults | authority-replay_arm | APPROVAL BINDING BREACH: replay_arm | 1 failed in 0.79s | 1 passed in 0.79s |
| correction-faults | authority-request_rebind | APPROVAL BINDING BREACH: request_rebind | 1 failed in 0.78s | 1 passed in 0.82s |
| correction-faults | clock-transition | CLOCK BREACH: expired stage issued another hold | 2 failed, 3 passed in 0.41s | 5 passed in 0.37s |
| correction-faults | clock-final | CLOCK BREACH: final stage still drives | 1 failed in 0.41s | 1 passed in 0.36s |
| final-faults | duplicate-approved_execution | DUPLICATE APPROVAL BREACH: approved_execution | 1 failed in 0.77s | 1 passed in 0.81s |
| final-faults | duplicate-point | DUPLICATE APPROVAL BREACH: point | 1 failed in 0.75s | 1 passed in 0.81s |
| final-faults | duplicate-controller | DUPLICATE APPROVAL BREACH: controller | 1 failed in 0.76s | 1 passed in 0.83s |
| final-faults | duplicate-until | DUPLICATE APPROVAL BREACH: until | 1 failed in 0.73s | 1 passed in 0.81s |
| final-faults | duplicate-identical | DUPLICATE APPROVAL BREACH: identical | 1 failed in 0.75s | 1 passed in 0.82s |
| final-faults | canonical-keys | CANONICAL KEY BREACH | 1 failed in 0.45s | 1 passed in 0.38s |
| final-faults | approval-alias | APPROVAL ALIAS BREACH | 1 failed in 0.74s | 1 passed in 0.75s |
| final-faults | protocol-shadow | PROTOCOL SHADOW BREACH | 1 failed in 0.74s | 1 passed in 0.81s |
| final-faults | dispatch-waypoint_command | EXECUTED DISPATCH BREACH: waypoint_command | 1 failed in 1.00s | 1 passed in 0.94s |
| final-faults | dispatch-command_pair | EXECUTED DISPATCH BREACH: command_pair | 1 failed in 1.00s | 1 passed in 0.98s |
| final-faults | dispatch-privileged_input | EXECUTED DISPATCH BREACH: privileged_input | 1 failed in 1.00s | 1 passed in 0.93s |
| final-faults | dispatch-time_due | EXECUTED DISPATCH BREACH: time_due | 1 failed in 0.98s | 1 passed in 1.00s |
| final-faults | dispatch-observe_without_interference | EXECUTED DISPATCH BREACH: observe_without_interference | 1 failed in 1.00s | 1 passed in 0.97s |
| final-faults | pending-command | PENDING COMMAND BREACH: command | 1 failed in 1.81s | 1 passed in 1.87s |
| final-faults | pending-remainder | PENDING COMMAND BREACH: remainder | 1 failed in 1.77s | 1 passed in 1.90s |
| final-faults | pending-both | PENDING COMMAND BREACH: both | 1 failed in 1.76s | 1 passed in 1.91s |
| final-faults | pending-decision | PENDING COMMAND BREACH: decision | 1 failed in 1.80s | 1 passed in 1.89s |
| final-faults | decision-journal | DECISION JOURNAL BREACH | 1 failed in 2.04s | 1 passed in 2.63s |
| clock-faults | old-absolute | physical/native clock mismatch | 1 failed in 0.46s | 1 passed in 0.40s |
| clock-faults | old-stage | STAGE OWNERSHIP BREACH | 1 failed in 0.43s | 1 passed in 0.38s |
| clock-faults | clock-corruption | TIMING CORRUPTION BREACH | 1 failed in 0.42s | 1 passed in 0.38s |
| clock-faults | grid-rounding | GRID ROUNDING BREACH | 1 failed in 0.42s | 1 passed in 0.73s |
| clock-faults | extra-decision | EXTRA DECISION BREACH | 1 failed in 0.40s | 1 passed in 0.37s |

The prior 18 authority faults bypass their test approval callback, preserving the delivered test scope; they are not claimed as 18 production mutants. The final authority/dispatch/pending matrix removes or replaces the named production guard. The old transition fault is parameterized: two failed and three passed RED cases, five passed GREEN cases. Both updated old clock faults genuinely restore floating-time stage ownership at the native-index interface. The five new faults reinstate the fixed clock band, restore floating stage selection, disable corruption rejection, round an off-grid declaration, or permit off-cadence decisions. Actual exception lines, traceback frames and hashes are retained in the JSON audit.
