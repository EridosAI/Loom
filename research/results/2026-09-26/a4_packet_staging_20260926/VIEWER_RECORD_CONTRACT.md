# Passive replay evidence retained for A4

This packet adds no renderer, server, live observer feedback path or live controller display. It preserves the unchanged records needed for a later file-only viewer. Viewer construction itself is not part of the three executions.

| Visible item | Original evidence | Display restriction |
|---|---|---|
| Arena, sources, repair structures | Exact configuration, initial snapshot and privileged geometry samples | Preserve actual body radius and finite mover size; do not turn the swept union into a solid obstacle |
| Body path, position, orientation and speed | Initial snapshot and every 100 Hz native endpoint | Mark sample time; interpolated display is visual interpolation, not physics |
| Mover path and actual sampled pose | Bound sine law/phase plus each 10 Hz controller input's mover rectangle and velocity | Distinguish recorded samples from analytic path/native-time geometric evaluation |
| Issued and delivered paired commands | Controller records and native commands/realized forces | Show held 0.1 s commands, decision timestamps and actual stage index; never recompute a command |
| E/I, costs, transfer, damage and repair | Native reserves and complete contact/accounting event operands | Separate instantaneous impact and sustained accounting; retain actual terminal and partial-tail records |
| Contact and impulse | Event collider, contact normals, force, impulse, impact and boundary labels | Contact is an event fact, not a proximity coloring rule |
| Timing and waiting | Exact fixed stages, controller stage/time, native clock and wait observations | Label prescribed versus observed waiting; no event-driven launch or viewer input |
| Entry, exit, arrival and detour distance | Saved-data definitions in INTERPRETATION.md | Sampled milestones with bracketing times; no fictional exact event time |

Retain all streams and restart snapshots. P is inactive during these external trajectories; absence of neural wave execution must remain visible. No downsampling of stored evidence is authorized. Any eventual display may visually select a frame without dropping the native source record. Offline playback never calls Engine, Run, a controller, a physics integrator or a neural operation.
