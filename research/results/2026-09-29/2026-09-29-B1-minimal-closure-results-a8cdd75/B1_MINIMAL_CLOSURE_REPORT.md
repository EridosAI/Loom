# B1 minimal closure — authorized execution report, 2026-09-29

**Disposition: B1 UNRESOLVED BY THIS EXECUTION. The batch stopped at its predeclared per-case wall-time limit.**

S1-FULL obtained real source contact and resolved positive transfer while its fixed sensory controller was active. It stopped administratively at **29.79 of 30 simulated seconds**. The matched controls and remaining starts were not executed. The accepted closure rule therefore has no completed sensory-free comparison and is not satisfied. This is an administrative cutoff, not evidence that sensory access is absent or that P scientifically failed.

## Authority and execution boundary

Jason authorized the nine separate objects in the order below, exactly as prepared, at apparatus checkpoint `a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad`. The original proposals, execution objects, starts and documents remain unchanged. Separate local approval envelopes record this actual user authorization and bind each unchanged execution object; they do not replace or amend the authorized objects.

The full-runtime preflight passed for **all nine** before any world case began. It verified the clean checkpoint, P and apparatus source bytes, configuration, installed Python/NumPy/SciPy content identities, all packet hashes, all nine authority bindings, all nine complete snapshots, byte-identical initial states within each triplet, the unchanged full-runtime prehistory-cache loader, actual local Windows access, fresh destinations and free storage. Preflight left each prepared engine's complete state, RNG, time and native index unchanged. It generated no prehistory and issued no controller decision.

| Order | Case | Authorized SHA-256 | Final disposition |
|---|---|---|---|
| 1 | B1-MINIMAL-S1-FULL | `d829e5d9b5825c6b72b9ddb26491f508cd8030654599dc309f6bf2efb1620912` | One attempt; administrative wall cutoff at 29.79 s |
| 2 | B1-MINIMAL-S1-CHEMISTRY-HIDDEN | `e46379806700a4aa638e00fbc6e36ddf97e04c8e80f420cb8fb792c2cc379b69` | Authorized, not executed; declared batch stop |
| 3 | B1-MINIMAL-S1-SENSORY-FREE | `394dfc775fc1c6dc93820384a79f4fd63291f06ee03bb28f80e464c989861dbc` | Authorized, not executed; declared batch stop |
| 4 | B1-MINIMAL-S2-FULL | `a60dacc6b0d536aaddf7dc71313b1adf3fe91013466f5852368dcf3bdef580b5` | Authorized, not executed; declared batch stop |
| 5 | B1-MINIMAL-S2-CHEMISTRY-HIDDEN | `1febeb0e0cf33dbcb67478e1d8081031c45a28df348ef09cfdcee79de0c0c36b` | Authorized, not executed; declared batch stop |
| 6 | B1-MINIMAL-S2-SENSORY-FREE | `fbf477f0220bdbf43ae80e077abe74a25e0afd78878fb9ecd710aaee78ba2092` | Authorized, not executed; declared batch stop |
| 7 | B1-MINIMAL-S3-FULL | `a2f6d55d86d360f3cb6ca13af6a1b97b642d09ddd311321a448e481d26452ca3` | Authorized, not executed; declared batch stop |
| 8 | B1-MINIMAL-S3-CHEMISTRY-HIDDEN | `e9cb37366aac8c0a7eba71ae5607ec61fd542bd5de58c53166508d20fe6badb4` | Authorized, not executed; declared batch stop |
| 9 | B1-MINIMAL-S3-SENSORY-FREE | `bdb6ae7f3394ea5d763b8110ace43be8ffa0183e12eb57da9a044dc8a378901c` | Authorized, not executed; declared batch stop |

The selected resource plan explicitly makes an administrative/resource cutoff a batch-stopping condition. Unused allowances were not transferred. No case was retried, continued, substituted or extended. A productive observation was not used to stop early; the runner's original wall guard stopped this case.

## Why execution stopped

S1-FULL began at 2026-09-29 10:52:57 UTC. Its original **600-second** wall allowance was enforced by `loom_commissioning/runner.py::Run.advance`, lines 239–240: when elapsed wall time meets the case limit, close with `administrative_pause`, cause `wall_time_limit`, before another native step.

The final state is at native index **2,979**, physical time `29.790000000001857`, with **298** decisions issued. The last decision was issued at index 2,970; nine of its ten authorized native steps occurred, and **one remains unexecuted** in the preserved snapshot. That pending step does not authorize continuation. No command exceeded its existing 0.1-second hold.

The session recorded 600.2436659000814 wall seconds at stop. Closing and flushing produced a recorder wall total of 600.9738899000222 seconds; the external supervisor recorded 601.1839588000439 seconds for execution and closure. The small wall overrun is the already-declared in-progress-step/flush behavior. No physical step after the stop was requested. `complete: true` in the recorder receipt means the **partial trajectory's records were closed completely**, not that its 30-second case completed.

The observed automated case used about 20.17 wall seconds per simulated second, exceeding the historical A2/A3 base-throughput projection. Full-history validation and recording are present in this apparatus; no profiling experiment was performed, so this report does not assign an exact causal breakdown of the overhead. The 10-minute resource envelope was insufficient on this actual run. No limit, validation path, recording fidelity or implementation was changed.

## Observed S1-FULL result

| Measure | Recorded result |
|---|---:|
| Physical duration | 29.790000000001857 s |
| Native records / field updates | 2,979 / 2,979 |
| Sensor rows, including birth | 2,980 |
| Issued command pairs | 298 |
| First source contact | 10.247049110709092 s |
| First resolved transfer event endpoint | 10.249999999999826 s |
| Summed source-contact interval duration | 18.602343168635553 s |
| Contacted collider | `source-0` only |
| Gross source debit / body credit recorded as transfer | 0.05230330252357774 |
| Reconstructed gross source debit, renewal removed | 0.05230330252358972 |
| Reconstructed gross body credit, expenditure added back | 0.05230330252357588 |
| Expenditure | 0.048195130356779727 |
| Starting E / I | 0.7 / 1.0 |
| Final E / I | 0.7041081721667961 / 0.9966723205606128 |
| Integrity damage / repair | 0.003327679439389176 / 0 |
| Total recorded contact impulse | 0.8448644997237181 |
| Controller transition to HOLD | 10.299999999999825 s |
| HOLD decisions | 195, including the final interrupted hold |
| Physical terminal / controller exception | Neither |
| Administrative outcome | `administrative_pause` / `wall_time_limit` |

The controller started with empty SEEK memory. Its first pair was `(0.24652535916747192, 0.3150149652277429)`, based on the permitted chemistry imbalance. Subsequent pairs changed with the recorded permitted readings. At 10.3 seconds it entered the specified HOLD state and used exactly `(0.05, 0.05)`. The complete command trace, including imbalance, angular proprioception, front contact and state transitions, accompanies this report. No command or policy was chosen from the observed result.

All 6,889 physical accounting events passed the existing `1e-12` per-event ledger tolerance. The maximum energy/stock/integrity residual was `5.55107277147842e-17`. Gross transfer is well above the conservative accumulated bound of `6.889e-9` (one existing tolerance allowance per recorded event). Every resolved source transfer has a matching actual source contact in the ledger. Renewal and expenditure were accounted separately. The energy increase is descriptive; net energy and survival were not pass gates.

## Closure interpretation

| Accepted requirement | Evidence in this execution |
|---|---|
| FULL has real source contact and resolved positive debit/credit | Observed in the preserved partial S1-FULL record |
| Permitted sensory feedback actually changes the FULL commands | Verified from recorded inputs, command algebra and state transitions |
| Matched, completed SENSORY-FREE case is unproductive | **Not available: case never started** |
| Chemistry-deprivation comparison | **Not available: HIDDEN never started** |
| Complete declared set, unless a batch-stop condition occurs | One attempt; the declared resource-stop condition halted the other eight |

Thus the partial run demonstrates an observed productive interaction by the fixed sensory controller, but **does not close B1 under the accepted comparison rule**. There is no observed FULL/HIDDEN difference, no completed null contrast and no nine-case outcome distribution. No claim about chemistry necessity, general navigation, source recognition, P learning, developmental efficacy or survival competence follows.

## Saved-evidence verification and preservation

The read-only reviewer verified every file hash in the case receipt, both restart internal checksums, exact initial/final state hashes, unchanged execution binding, native sequence and stop classification, physical event accounting, source/contact linkage, native field counts, all physical raw rows, held E/I cadence, every recorded controller input against its exact allowlisted causal physical prefix, prior-command prefixes, initial controller-memory reset, state continuity, the frozen command algebra and applied command holds. It also confirmed that the inactive P organism state is byte-identical before and after external control. No saved-data check failed.

This review loaded saved states and evaluated scalar arithmetic only. It did **not** replay physics, run another controller trajectory, evolve a field/world, generate prehistory or inspect any old sealed human B1 evaluator file. The historical human records remain outside this report's evidence base.

Exact execution identities:

- P baseline: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.
- Apparatus checkpoint: `a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad`.
- Parent: `b684912eaf7811cd318ee94c77172aca790f3a0d`.
- Branch: `build/p-b1-minimal-20260929-01a0c405`.
- Worktree: `C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\worktrees\loom-p-b1-minimal-20260929`.
- S1-FULL execution SHA-256: `22e754d557273781852d727a550a201cbc17ce71d623373b9c57c42581a3f955`.
- S1-FULL initial state: `5cc5eda4aa4b1ac94fccda97ea42b485a2508fe33e2bb659f82cb61725d72671`.
- S1-FULL final state: `a6580774b30cb64e3e41282114cdd7bdd046419e9c79215a88122b12abcdbf47`.
- Recorder receipt SHA-256: `84fc5325b49ccf047c5b4c8699127bee26eb7caf79b25741928fea3be06aea27`.

P, the Base World, sensor laws, controller constants, starts, clocks, horizons and production code were not modified. The checkpoint remains clean. No Git write, push, PR or merge occurred. New files are confined to execution records, the external authorization/supervision wrapper and reporting/package artifacts in the writable project workspace.

## Resources and evidence locations

Before launch, free disk was 634,313,261,056 bytes, above the 20,000,000,000-byte minimum. Counted prepared/scratch artifacts totaled 7,804,722 bytes. At execution end, combined counted files totaled 99,911,675 bytes. The case's physical files occupy 92,075,074 bytes; its uncompressed stream total is 282,200,122 bytes, below its 1,500,000,000-byte cap. Storage was not the stopping condition. Final packaging usage and archive verification are recorded in `DELIVERY_VERIFICATION.json`; all retained copies count toward the 20 GB cap. Only one additional complete trajectory copy is made, inside the portable ZIP.

Primary evidence remains under `b1_minimal_execution_20260929/run-001/`. The portable review archive includes that complete directory, the execution/review scripts and original user-authorization record, this report and machine-readable review, and the unchanged prepared packet with all nine authority objects, starts, source/configuration/runtime identities and instrument source. `FILE_MANIFEST.json` in the archive binds every included file. The archive is for review; it grants no retry, continuation or new run.

Principal evidence files: `PREFLIGHT.json`, `operations.jsonl`, `EXECUTION_RESULT.json`, `cases/B1-MINIMAL-S1-FULL/manifest.json`, native/event/controller/sensor/diagnostic streams, initial/intermediate/final restarts, `BOUNDED_RESULTS.json`, `B1-MINIMAL-S1-FULL.json`, and `B1-MINIMAL-S1-FULL-command-trace.csv`. The closure rule and stop policy are preserved in the prepared packet's `accepted-design/B1_MINIMAL_CLOSURE_DESIGN_v0_2.md` and `RESOURCE_AND_EXECUTION_PLAN.md`.

## Review boundary

The eight untouched cases, remaining 0.21 seconds of S1-FULL, matched null comparison and chemistry-deprivation comparison are **not tested**. No extra smoke, replay, retry, continuation, tuning, substituted start, new prehistory, Founder Search, C1/C2, nursery design or additional perceptual assay was performed. No replacement authority or automatic next run is prepared. **Execution is stopped for Jason's review.**
