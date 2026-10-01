# Authority and information-flow map

The current user request authorizes apparatus construction and minimum manufactured engineering fixtures only. The five commissioning design documents are accepted for that scope with the seven user rulings. In particular, the D5 ruling replaces the earlier at-most-100-wave-samples proposal with every handoff where practical. No other design proposal is promoted to a permission to run.

| Actor / component | Reads | Writes / capability | Forbidden crossing |
|---|---|---|---|
| Intact P | Existing raw tuple and actual E/I through original engine | Existing P state and two motor commands | World geometry, labels, stock, phase or observer conclusions |
| Privileged external controller | Copied body pose/velocity/E/I/commands; geometry; mover phase/velocity; stocks; normal/force/impulse; world clock | Two actuator commands and route cursor | Engine reference, direct physical-state mutation, neural state or random generator |
| Sensor-only human gateway | 29 raw coordinates, raw history, cadence-held E/I, own commands/annotations | Two commands for one hold | World/evaluation/snapshot/manifest/phase/stock/fixture payload or privileged exception |
| Fixed-structure adapter | Ordinary P inputs and explicitly listed frozen newborn fields | Restore only listed structure at declared boundaries; retain hypothetical updates as diagnostics | A substitute policy, disabled transient dynamics, changed P settings or an intact-P label |
| Passive diagnostics | Detached pre/post snapshots and recorded contributions | New diagnostic records | Live RNG or state mutation, alternate world evolution, outcome-based sampling |
| Privileged evaluator | Completed native/wave/event records and restart snapshots | Separate offline AV/CO display and preserved SO stream | Live human-controller information |
| Configuration-ground builder | Evidence rows with fixed registered classes | Review request requiring Jason | SO as a pre-freeze adjustment ground; automatic configuration edits |
| Bounded runner | Exact explicit contract and complete state | Native steps within deadline; append-only records; honest stop | New births, silent resets, longer durations on restart, invisible incomplete tails |

Default launchers open inert saved HTML. They do not start Python, create a world, run a timer or install anything. The optional loopback sensor server defaults to an offline saved-record gateway. A live human gateway must be explicitly supplied by a later authorized task. Privileged evaluation is a separate module/output and has no route on that server.

The execution-authority record for a future commissioning manifest must identify a separately supplied request file and its SHA-256, the approved case, exact initial-state hash and duration. This release supplies no such grant. Hash checks establish custody and scope, not the identity of a human author; Jason's actual instruction remains the authority. The four birth IDs and 600-second ceiling are prospective roster metadata with `execution_authorized=false`.

A future operator must not inspect the test's privileged starting state/phase or evaluation before a blinded sensory witness. Human positive controls and held-out scenario/deprivation protocols remain an execution-task requirement, untested here. An automated learned sensory controller was not built.

No shared workbench map, canonical research source or vault Git state was written. The main Loom checkout's preexisting modifications remain outside this worktree. Prior engineering artifacts and failed-development evidence are preserved. The new commit is local only and is an engineering checkpoint, not commissioning approval or an evidential freeze.
