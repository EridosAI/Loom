# B1 apparatus compatibility — HOLD BEFORE EXECUTION

P and the pinned apparatus are unchanged. The independent review verified the existing full-raw information boundary and inert inspection within its tested scope; it did not verify a chemistry-hidden adapter or fresh browser appearance. The later correction explicitly bound `display_intervention = {"kind":"none"}` and rejected unimplemented alternatives. A5's corrected long clock does not add perceptual-display capabilities.

| Finding | Exact present surface | Consequence |
|---|---|---|
| B1-H1 — chemistry-hidden unavailable | `loom_commissioning/authority.py::validate_execution` requires `display_intervention == {'kind':'none'}` and raises `unsupported display intervention`. `controllers.py::SensorHistory`, `Run.display`, and `HumanGateway.display` supply full raw history. | The exact chemistry-hidden candidate is rejected by pure validation. It has a custody digest, not a valid launch authority. No masking implementation hash exists. |
| B1-H2 — misleading in-flight state and queued submissions | `sensor.html::render` shows `Paused between decisions` for every live payload. The click handler awaits `/command` without first changing state or disabling submission. | During an authorized future hold, the page would still look paused, and further clicks could queue commands. This does not meet the requested obvious paused/running interaction. |
| B1-H3 — live lifecycle not supplied | `sensor_ui.main` constructs `OfflineGateway` only. `HumanGateway` exists for explicit later integration. `Run.close` does not change the sensor payload's `availability`, and `HumanGateway.display` does not translate closed state. | The inert launcher is not a live launch workflow, and a finished run can retain a paused/submit-ready payload. A reviewed integration must end input cleanly without revealing privileged stop details live. |
| B1-R1 — growing record/validation work | `Run.begin_command` obtains the entire `sensor.display()` history, records it in each action, and pending-command validation revisits it. | Use the explicit history-growth estimate; A5 physics throughput alone is insufficient. No performance claim or recording-fidelity reduction is substituted. |

`STATIC_COMPATIBILITY_FINDINGS.json` gives exact checked source hashes and line anchors. The code was read, not modified. The hidden candidate was passed only to the pure execution-specification validator and produced the expected rejection. No Run, controller, live gateway or world was invoked.

## Smallest proposed closure for Jason's separate decision

Authorize a narrowly scoped **apparatus-only** implementation and independent review of:

1. A server-side chemistry-display deprivation, bound by exact implementation/specification identity. Withhold all four chemistry coordinates from every operator-visible route/history/export and record what was actually shown. Retain the original real sensor values separately for the evaluator. No physical-field, sensor-law, P, world, body or actuator change.
2. Honest client-side in-flight/paused/ended indication and rejection of concurrent/queued extra submissions. Preserve exactly one 0.1-second hold per explicit decision and the existing native/5 Hz cadence. No control macro, batching or automatic repeat.
3. Explicit authorized live gateway lifecycle, no evaluator endpoints, safe closed-state handling, and complete display/command/annotation audit. No hidden control assistance.

Exact affected surfaces likely include `authority.py`, condition-specific sensor egress/recording in `controllers.py`/`runner.py`/`pending.py` as required, and `sensor_ui.py`/`sensor.html`. The final minimal diff must be established by the separate engineering task, not inferred as authorized here.

Required review evidence: real versus shown channel equality; complete chemistry suppression including all prior rows/downloads; poison/canary leak rejection; unchanged physical state/RNG across repeated reads and display deprivation; unchanged commands/hold remainder/deadlines; one-decision handling during slow requests/double clicks; honest terminal/failure/cutoff state; separated operator/evaluator records and same full initial-state identity; null grants fail closed; canonical authority binds the actual mask implementation; pause/inspection costs no bodily time or RNG. Any manufactured execution used for that review needs separate explicit scope. No such tests were run here.

Existing full-display case objects and all prepared initial snapshots remain preserved. A new reviewed apparatus changes identities, so regenerate the exact manifests and approval hashes; do not edit the held objects, relabel the unsupported candidate as valid, mask by CSS only, substitute fake zero chemistry, or bypass validation. Do not launch FULL-RAW alone to work around the held pair. No B2/B3/B4/C1/C2 work is included.
