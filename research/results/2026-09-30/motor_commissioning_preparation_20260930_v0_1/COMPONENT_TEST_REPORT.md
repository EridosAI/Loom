# Component-test report

Final result: **26 passed** on local Windows Python 3.13.5 / NumPy 2.3.3. Exact results and elapsed time are in COMPONENT_TESTS.xml. Production source files were not changed. Tests used the prepared overlay plus original motor, regulator, codec and scheduler helpers; no complete organism or world loop was permitted.

| Requirement | Evidence |
|---|---|
| CURRENT preserves motor semantics | Bit-for-bit original-versus-overlay state comparison over 151 manufactured-input component steps. |
| Original downstream law remains | Exact command, tendency, integral and phase equations checked for M1 and M2. |
| Existing direct/associative/current input remains effective | Manufactured spontaneous values spanning ±0.349, original anatomical contact/proprioception feedback, q/current perturbations and large background-current grid. |
| Learned/regulatory coupling remains | Legal ±0.5 constant-feature regulator-bank perturbations change currents and attenuation, with corresponding command changes; no credit/learning update. |
| Attenuation remains effective | 0, 0.2, 0.8 and 1 attenuation; exact original multiplicative law. |
| Blindness and RNG separation | Identical next process states under changed sensory/regulatory inputs; reproducible namespaced draws; original engine/RNG unchanged. |
| Clock and renewal | Native tick 50 M1 boundary, M2 exact predetermined renewal boundary, duration endpoints 8 and 24, fractional component update. |
| Memory/reset/serialization | Case reset, separate life streams, exact typed round trip and next standalone transition equality at a refresh boundary. |
| Rollback | Original lean backup remains unchanged when the copied candidate state advances. |
| Authority/deadline/resource ownership | Explicit new kind required; mismatched process, parameters, state, wall cap and deadline rejected; no continuation; manufactured pre-step stops and terminal branch. |

During tests, Engine.step, Engine._coupled, Organism.native/handoff, FieldSolver.step and physical advance were replaced by fail-on-call sentinels. The terminal-branch test used only a manufactured index object. Snapshot preparation separately installed fail-on-evolution guards and recorded zero calls. Test-only temporary approval records say COMPONENT FIXTURE ONLY and cannot launch a prepared case; none was copied into the review archive.

The first run passed 20 tests but three approval-fixture tests could not create the framework's default temporary directory because Windows denied access. This was an environment error, not a failing motor result. The tests were rerun with a new scoped workspace temporary directory; later added coupling/terminal checks bring the final result to 26 passed. No test retuned a motor constant. No RED-before-GREEN claim is made.

Not tested: candidate-world trajectories, candidate ecological outcomes, full-world bit equivalence, live performance, 90-second motor/world behavior, impact outcomes, learning usefulness, survival benefit, long-run numerical behavior beyond the scope, or a solution to the historical FS-060 interruption. A future authorized launch must repeat the full runtime/source/state gate. Component readiness does not establish environmental efficacy.
