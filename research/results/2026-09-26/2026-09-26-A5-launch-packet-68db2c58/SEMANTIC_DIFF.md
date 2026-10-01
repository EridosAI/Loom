# Held versus regenerated A5 — semantic comparison

**No unexpected semantic change.** Every manifest field change is listed below; exact before/after values, supporting JSON changes and complete document replacement spans are in `SEMANTIC_DIFF.json`. The portable validator independently reproduces those diffs and asserts all other scientific/trajectory fields unchanged.

Historical HOLD object: `88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6`. New proposed object: `bdff35693db38800528d91e6d2d4d2085c640268e50713731df5ec27f8b76d1d`. Both grants are null; the former remains non-launchable.

Preserved: 630 s; source order 0→1→0→1; all seven points, press forces and physical deadlines; exact A1/A2 snapshot, phase and prehistory; all controller constants and actuator arithmetic; P, configuration, world/resource laws; full-fidelity observer/recorder contract; all observation definitions and interpretation limits; every numerical resource projection and cap.

Only clock-status phrases change in the observation table; its outcome predicates and claim limits are unchanged. The prospective output namespace follows the corrected worktree/checkpoint. Original cache identity and original path remain unchanged.

| Changed manifest field | Classification |
|---|---|
| `/apparatus/files/authority.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/apparatus/files/clock.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/apparatus/files/controllers.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/apparatus/files/pending.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/apparatus/files/runner.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/apparatus/files/validators.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/apparatus/sha256` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/controller/implementation/clock.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/controller/implementation/controllers.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/controller/implementation/live_clock_functions` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/controller/implementation/live_functions/command_pair` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/controller/implementation/live_functions/observe_without_interference` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/controller/implementation/live_functions/privileged_input` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/controller/implementation/live_functions/time_due` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/controller/implementation/live_functions/validate_plan` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/controller/implementation/live_functions/validate_privileged` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/controller/implementation/live_functions/waypoint_command` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/controller/implementation/live_functions/waypoint_stage` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/analysis_destination` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/CLOCK_AUDIT.json` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/CODE_AND_RUNTIME_IDENTITIES.json` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/OBSERVATION_AND_INTERPRETATION.md` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/OPEN_ISSUE_A5_CLOCK.md` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/PLANNING_EVIDENCE.json` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/PREPARATION_REVIEW_NOTE.json` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/PROCEDURES.md` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/RESOURCE_PLAN.md` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/RESOURCE_PROJECTION.json` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/REVIEW_AND_EXECUTION_BOUNDARY.md` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/SOURCE_IDENTITIES.json` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/STATIC_HOLD_SCHEDULE.csv` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/STATIC_SCHEDULER_COMPATIBILITY.json` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/STATIC_SCHEDULER_COMPATIBILITY.md` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/build_packet.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/clock_audit.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/deliver_packet.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/finish_packet.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/historical-held~1AUTHORITY_OBJECT.canonical.json` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/historical-held~1CLOCK_AUDIT.json` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/historical-held~1FILE_MANIFEST.json` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/historical-held~1OPEN_ISSUE_A5_CLOCK.md` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/regenerate.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/static_scheduler_check.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/bound_files/validate_packet.py` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/launch_disposition` | SCHEDULER REPRESENTATION CHANGE REQUIRED BY CLOCK FIX |
| `/execution/procedure/protocol/launch_preconditions/0` | SCHEDULER REPRESENTATION CHANGE REQUIRED BY CLOCK FIX |
| `/execution/procedure/protocol/launch_preconditions/1` | SCHEDULER REPRESENTATION CHANGE REQUIRED BY CLOCK FIX |
| `/execution/procedure/protocol/launch_preconditions/2` | SCHEDULER REPRESENTATION CHANGE REQUIRED BY CLOCK FIX |
| `/execution/procedure/protocol/launch_ready` | SCHEDULER REPRESENTATION CHANGE REQUIRED BY CLOCK FIX |
| `/execution/procedure/protocol/packet_status` | SCHEDULER REPRESENTATION CHANGE REQUIRED BY CLOCK FIX |
| `/execution/procedure/protocol/record_destination` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/reviewed_checkpoints/apparatus_git_sha` | IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS |
| `/execution/procedure/protocol/schedule_interpretation` | SCHEDULER REPRESENTATION CHANGE REQUIRED BY CLOCK FIX |

Document replacement spans and supporting JSON leaves are classified individually in the JSON. Old clock/preparation utilities and status documents are archived, not rewritten or silently treated as current. New scalar evidence replaces obsolete HOLD evidence in the new binding. Current preparation reports and checksums are derived metadata, sealed by `FILE_MANIFEST.json`; they do not authorize execution.

The exact old packet can be reconstructed from `HISTORICAL_PACKET_LAYOUT.json`; every original file is verified against its original manifest. No prior A1–A4 result is reinterpreted. The prior correction review records 5,579 saved stage decisions with no disagreement; that is prior evidence, not a new replay in this task.
