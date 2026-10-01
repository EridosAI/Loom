# Equation-to-code and test coverage — bounded engineering build

Paths below are relative to developmental_ecology/. Tests are deterministic component checks and three bounded named smokes, not scientific results. The final component suite passes 44 checks. Coverage limits are explicit; examples are not exhaustive numerical certification.

| P equation | Executing function | Current verification |
|---|---|---|
| 1 | neural.Cortex.step | test_sensory_old_rhs_and_pool_terms checks independent old-state activity formula and rejects new-state formation |
| 2 | Cortex.step/packet; Motor.step; Organism.handoff | trapezoid accumulator assertion, baseline/alternate shape and first-write tests; independent delivered-command mean/endpoint ordering oracle |
| 3 | Cortex.step | independent Oja/competition formula; negative wrong-state fixture |
| 4 | Association.packets_to_context/write | independent old-mean centring and exact trace/mean filter oracles |
| 5 | Association.gates | positive normalized gates, exact target exclusion, other-channel influence and support independence |
| 6 | Association.write | independent map increment and one-write assertion; detects no-op and reread-new-map deviations |
| 7 | Association.read/write | independent sampled-use and old-use decay oracle from final old-map contributions |
| 8 | Association.read | exact low/high support gains and repeated coordinate routing |
| 9 | Association.read | independent four simultaneous sweeps, final old-map q, rejection of fifth sweep; frozen-map observer calculation |
| 10 | Regulator.output | exact fixed feature mixing and actual-reserve interface check |
| 11 | Regulator.output | signed streams and previous/new perturbation distinction; output contribution diagnostics |
| 12 | Regulator.output | independent need-floor/extreme reserve checks |
| 13 | Regulator.output | independent learned/exploratory weighted-logit superposition oracle |
| 14 | Regulator.output | independent tanh current and logistic attenuation superposition oracle |
| 15 | Cortex.step; tangent_step | local terms, centring, old references, tangent and radial projection fixtures |
| 16 | Cortex.step | support-dependent spring, exact opening exponential and independent group update |
| 17 | Motor.__init__/step | old-phase/noise exponential and analytic phase oracle; saved-record reconstruction checks native-noise/wave draw counters in all three smokes |
| 18 | Motor.step | feedback route, exact endpoint block selection and command/tendency distinction |
| 19 | Regulator.credit | trend from old mean, corresponding bank assertion |
| 20 | Regulator.credit | independent previous-xi/phi eligibility formula; fresh-draw mutant differs |
| 21 | Regulator.credit | independent bank update, untouched other bank, active row projection and new-value reference oracle |

| Other source rule | Code | Evidence or limitation |
|---|---|---|
| 82/164/88,608 and configurable pools | schema.Config | default inventory, legal six-unit interleaved pools, malformed membership rejection |
| Exact random encoding | schema.Streams | anatomical independence from life, distinct life streams, endpoint safety, counter continuation |
| Source/body conservation and renewal | physics.account | conservation/headroom, renewed-stock, attempt-cost and no impact transfer assertions |
| Damage/repair/contact duration | physics.account | every collider material, gentle repair, zero-duration no-repair, terminal physical notification |
| Simultaneous constraints and swept mover | physics.project_velocity/first_collision/advance | corner and sustained moving/static projection, impossible constraints fail, source sweep, analytic mover impact and near-source separation regression |
| Coupled terminal shortening | engine.Engine.step | test_terminal_scheduler_restores_trial_state_and_draws_once forces a shortened step with arithmetic stand-ins; real physical crossing separately tested; no natural terminal event in named smokes |
| Solid-aware field and finite preparation | chemistry.FieldSolver; prehistory.prepare/load | exact circle/cell emission areas, flux/mass, coefficients, zero RHS, forced failure; full 60,000-step prehistory record |
| Rear blindness/proprioception | geometry.light_readings/transduce | manufactured rear-source and command/movement tests; selected open-domain visibility/ambient/finite-body/flush-versus-protruding fixtures in test_boundary_and_scheduler.py |
| Learner allowlist | Organism interface | explicit raw widths/actual-reserve inputs; world truth absent from neural module interface; manual source/interface audit: only the raw tuple and actual reserves enter neural methods; diagnostics, pose, IDs, stocks, time and fields have no neural argument route |
| Snapshot/restart | records.pack/unpack/save_snapshot/load_snapshot | birth and manufactured nonzero exact snapshot roundtrips; 0.07-second mid-wave restart with every state compared through 1.00 seconds; missing arrays, wrong shapes, checksum/nonfinite/unknown-class rejection |
| Storage failure | records.Recorder | injected storage failure and coupled solver-exception rollback produce complete=false/apparatus_failure; real full-disk condition not induced |
| Observer/replay noninterference | inspector.Inspector | state hash unchanged by observations/replay; nonzero same-case continuation observed versus unobserved stays identical; actual browser replay/reconstruction and 20-step contact prefix match |
| Native/wave/events/reconstruction | records.Recorder; engine.run_bounded | verify_engineering_records.py: 3,200 neural states and all three final fields reconstruct bit-identically; checksums, counts, clocks, conservation and measured widths/bytes/throughput recorded |
| Single paused visual inspector | inspector.serve | actual launcher invoked through Windows; paused initial fixture, all three browser views, replay/reconstruction, native/wave/Pause/Stop checked; literal mouse double-click not available |
| Exact complete-loop budget | smokes.CASES/execute | only birth_30s (30 s), nonzero_resume_1s (1 s), contact_ui_1s (1 s); attempt 002 complete after disclosed fixes; previous attempts preserved |

Remaining limits: terminal integration is component-tested, not encountered naturally in a fourth complete-loop case; complex contact geometries are not exhaustively certified; no long-run/cross-platform/OS full-disk or scientific adequacy checks were performed. Full history plots use saved replay, while live stepping exposes endpoint/wave values. Test count is not scientific evidence.
