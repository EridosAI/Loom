# Correction equation and test map

The original complete 21-operation map is preserved at `../p_engineering_20260921/EQUATION_TO_CODE_AND_TEST_MAP.md`. Its former verification-strength claims must be read with the independent review and this correction. Production `neural.py`, `engine.py`, `chemistry.py`, `geometry.py` and `schema.py` are unchanged.

| Source operation / rule | Corrective code or assertion | Executed fault |
|---|---|---|
| Physical realization, swept release/return | physics.release_probe / first_collision / advance; test_touch_release_return_duration_and_accounting | release_disabled |
| Physical source/body and duration-specific damage | test_touch_release_return_duration_and_accounting, independent balance/stress oracles | double_source_debit; damage_suppressed |
| One native/noise update per native interval | test_release_subdivision_does_not_repeat_native_or_noise | native_repeated |
| Observer physical timestamp | test_live_handoff_observation_has_physical_timestamp | live_branch_missing |
| Equation 21, new projected bank-reference target | test_bank_projection_and_reference_follow_new_value; rtol=0 | bank_reference_frozen; bank_reference_old_target |
| Equation 15, old shared/fine references | test_separate_sensory_reference_following; independent exponential, rtol=0 | shared_reference_frozen; fine_reference_frozen |
| Terminal exclusion at scheduled handoff | test_terminal_scheduler_restores_trial_state_and_draws_once, indices 19/59 | terminal_guard_removed |
| Solid footprint in field coefficient | test_field_flux_mass_and_moving_geometry_continuity, same time and phase | body_footprint_missing |
| Declared transduction boundary / equations 1–21 | test_hidden_state_cannot_bypass_declared_transductions | hidden_pose_injected; hidden_config_read |
| Evoked E/I versus actual body ownership / equations 10,14,18 | test_evoked_reserves_have_no_direct_physical_ownership | evoked_refill |

Every fault runs in a fresh subprocess with an in-memory patch; runtime files are never mutated by the harness. The 14 assertions and exact logs are named in the mutant summary. The final assembled component result is separate from these selective tests. The three new smokes preserve the exact previously authorized case definitions; detached replay checks every native learner hash and final field without adding a full-loop case.
