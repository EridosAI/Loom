# Law, code and component-verification map

All paths below are relative to `developmental_ecology`. The unchanged P equations remain in `loom_p/neural.py` and its original equation map. This is an apparatus intervention map, not a new mechanism specification.

| Requirement / source | Implementation | Consequential evidence |
|---|---|---|
| Exact reviewed P and configuration; design §2 | `contract.validate_manifest`; `initialization.verify_history` | Identity/config rejection; phase mismatch; verified cache load; unmodified 59-test suite |
| Native 0.01 s, wave 0.2 s, four sweeps; design §§2,8 | `Run.advance`; intact `Engine.step`; `adapter.step` for declared modified arms | Above-old-cap single native step with due wave; noise boundary; partial terminal before due handoff; saved full replay |
| Original body/world/field laws | Original `physics.advance`, `FieldSolver.step`, `transduce` | Unchanged P regression tests; debit/credit mutant; field reconstruction; duplicate-field mutant |
| Explicit duration and original restart deadline | `contract.make_manifest`, `Run._guard`, `Run.remaining`, `load_restart`, `Run.resume` | Cap mutation rejected; no output for unauthorized A5 manifest; step-seven pause equals continuous advance |
| Ten-step command holds; design §4.1 | `begin_command`, `hold`, session held-command/remainder | Separate extra native, wave, random and field faults; full external object inactivity and field replay |
| Closed privileged allowlist; design §4.1 | `controllers.privileged_input`, `validate_privileged`, `waypoint_command` | Forbidden neural input rejected; repeat command equality; bounded two-actuator result |
| Raw-only human ceiling; design §5.1 | `SensorHistory`, `HumanGateway`, restricted HTTP handler | 29-coordinate and E/I cadence assertions; privileged key rejected; reconstructed raw/EI comparison; forbidden endpoint tests; browser check |
| Freeze sensory fields; P equations 1–3,15–16; design §6 | `fixed_native`, `restore_sensory` | Persistent-change fault; poisoned hypothetical updates leave later causal state identical |
| Freeze banks between credit and output; P equations 11–14; design §6 | `fixed_handoff`, `restore_banks` | Late-restore fault changes later output despite restored parameters; unchanged transient eligibility/body mean/RNG |
| Freeze maps/use before next read; P equations 5–10; design §6 | `fixed_handoff`, `restore_maps` | Poisoned map/use discarded without changing later causal state; stored hypothetical versus zero applied increments |
| Raw → packet → query alignment; design §§5.3,7 | `diagnostics.passive`; original wave records | Separate start/end timestamps; exact snapshot/native/wave replay; manufactured mean/endpoint alias |
| Pooling, opening, support, formation and coarsening | `diagnostics.passive` cortical records | Original P equation tests plus per-group old/new/reference and pressure operands; no diversity or growth gate |
| Receiver influence; design §7.3 and Jason's D5 ruling | `wave_receiver`, `motor_receiver`; immutable `SELECTION` | Original receiver reconstruction; nonzero manufactured q/banks; every handoff and fixed native-index selection; observer interference fault |
| Separate actual E/I credit; design §7.4 | Original `Regulator.credit/output`; `credit_separate_E_I` records | Previous perturbation/features, old/new eligibility, actual body mean/trend, learning/reference/projection and applied delta; original credit tests |
| AV/CO/SO firewall; Jason ruling 6 | `classify`, `configuration_grounds`; separate scientific stream | SO rejection with raw observation preserved; no automatic adjustment path |
| Complete records and honest stop reasons; design §8 | `Recorder`, restart wrapper, `verify_segment`, `validate_stop` | Missing native and wrong stop mutants; injected I/O failure produces incomplete apparatus failure; all-state replay |

The fixed-structure adapter duplicates only the necessary handoff and modified-arm scheduling order. It calls the unchanged operations for all equations. Its hypothetical diagnostic buffers can differ under poisoning; the test excludes only those observational buffers when comparing future causal state. It does not exclude body, random, control, filter, trace, activity or eligibility state.

The complete mandatory fault table, commands, exact intended failures and individual RED/GREEN exits are in `artifacts/apparatus-20260924-01a0c405/faults-attempt-002/FAULT_MATRIX.json`. Each clean control is a separate process. No test asserts useful learning or behavior.
