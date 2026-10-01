# Focused B1 component report

**35 passed. No physical world case.** See `COMPONENT_JUNIT.xml` and `COMPONENT_FINAL.txt`. Tests are `developmental_ecology/tests_apparatus/test_b1_minimal.py` at the new checkpoint. All inputs are manufactured; no held-out snapshot or human B1 record is a test input.

| Requested check | Test / result |
|---|---|
| 1–3 Left/right sign and equal straight drive | `test_turn_sign_equal_forward_and_drive_reduction`: intended signs and exact `(0.30,0.30)`. |
| 4 Stronger imbalance lowers drive | Same test compares increasing imbalance at unchanged other inputs. |
| 5 Angular damping | `test_equation_window_order_and_damping`: equation, correct coordinate, signs and latest-ten-row window. |
| 6 Front contact enters HOLD | `test_front_contact_hold_and_exact_release_hysteresis`, all sectors 7/0/1 and exact onset threshold. |
| 7 Exact hold pair | Same test and runner integration: `(0.05,0.05)`. |
| 8 Release hysteresis | Two low windows keep HOLD; a reading at 0.02 resets count; third consecutive reading below it releases immediately. |
| 9 Hidden omission / zero imbalance branch | `test_hidden_omission_and_missing_branch` and runner arm test: every row has 25 channels; FULL input rejected for HIDDEN. |
| 10 Sensory-free no feedback | `test_sensory_free_has_no_input_and_fixed_pair` rejects even an empty dict; runner spy forbids any sensory request. |
| 11 No private fields | Twelve top-level/row canaries rejected; annotations, future E/I, nonfinite values and invalid protocols rejected. |
| 12 Per-case reset | Pure-state test and two fresh real Run sessions with manufactured inert engines. |
| 13 Exactly one existing hold | Real scheduler accepts one decision, rejects an overlapping decision / 11-step advance, calls an inert adapter exactly ten times and emits one controller record. |
| 14 Inference leaves world/RNG unchanged | Packed inert-engine identity before/after each arm; pure input/state immutability; real RNG draws and physical functions guarded against calls. |
| 15 Runner-owned stops | Terminal/wall/storage conditions prevent decisions; manufactured terminal during a hold ends after three artificial ticks, retaining the seven unspent ticks. |

Additional checks cover invalid chemistry with no fallback, changed live dispatch/constants, manual overrides, memory/command/clock substitutions, exact arm authority identities, null-grant denial and unchanged 30-second commissioning ceiling.

The inert adapters increment only manufactured time/index values and emit empty physical-event lists. Across the integration suite there are ten ordinary artificial ticks plus three artificial terminal ticks. **Physical native steps = 0; field steps = 0; prehistory steps = 0; simulation RNG draws = 0.** No inference on prepared S1/S2/S3 states occurs during preparation.

The initial RED was an expected missing-feature import error. Intermediate test-harness failures and their resolutions are retained in `TEST_HISTORY.json`; the final passing run is the authoritative component result. No claim of independent review, full runtime performance or successful productive interaction is made.
