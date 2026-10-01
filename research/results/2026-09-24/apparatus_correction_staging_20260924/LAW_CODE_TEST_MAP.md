# Correction source → code → check map

This supplements the original apparatus map without reopening its verified areas.

| Controlling requirement | Implementation | Consequential evidence |
|---|---|---|
| A-R1: exact approved object | `authority.execution_object`, `canonical`, `execution_sha256`, `verify_approval_binding`; schema-2 `contract.make_manifest` / `authorize_execution` | Original 05ab authority RED; `test_approved_execution_binding` (18 variants), `verify_corrections.py` and all 18 fault/control pairs |
| Controller program and constants | `authority.controller_identity` and unchanged-valued `controllers.WAYPOINT_SETTINGS` | Implementation/constants pairs; live function/configuration mutation checks in `test_canonical_identity_and_live_program_guard` |
| Complete arm/procedure/resources before output | `authority.validate_execution`; `Run.__init__` before `Recorder` | Manual/sensor/intact/fixed/deprivation/procedure/replay/resource pairs; `test_route_and_resources_rejected_before_output` |
| Approval survives restart | `authority.validate_session`; `load_restart`, `Run.__init__`, `Run._guard`; clock-derived route cursor | Altered restored-session route rejection; waypoint resume at native 7 and 10; all original three-mode reconstruction cases |
| A-R2: nominal native deadline | `controllers.time_due`, both route progression and final-stop uses | Original saved input RED; `test_exact_review_boundary` (five represented times), `test_final_stage_and_not_due_control`; transition/final comparator RED→GREEN pairs |
| Design §4.1 ten-step holds; no unauthorized stage extension | `Run.begin_command` checks route completion and proposed hold endpoint before recording | `test_full_hold_cannot_cross_stage`; final-boundary resume cannot gain a hold |
| Native cadence, independent duration accounting, absolute ceiling | Unchanged native advancement; new boundary guards only | Independent Decimal native-tick oracle, twenty .01 field calls, no neural/RNG/wave change; exact continuous/resumed equality; `verify_segment` reconstruction; original cap/terminal/noise tests |
| P and historical preservation | No P/config/test edits | `UNCHANGED_P_AND_HISTORY.json`, `PRESERVATION_BEFORE.json`, `PRESERVATION_AFTER.json`; 113-case worktree and portable suites |

Canonical identity is SHA-256 over UTF-8 sorted-key compact JSON, rejecting non-finite numbers and excluding only the grant field. Route times remain physical absolute deadlines. No equation, time step, physical tolerance or controller gain was tuned. The duration oracle is test-side Decimal/integer arithmetic; it does not invoke the production `time_due` function.
