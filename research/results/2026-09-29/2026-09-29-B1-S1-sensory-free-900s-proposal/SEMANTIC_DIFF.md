# Semantic diff — original S1-SENSORY-FREE to 900-second proposal

Original outer authority: `394dfc775fc1c6dc93820384a79f4fd63291f06ee03bb28f80e464c989861dbc`.
New outer authority: `57386e964ea018050bedc18a397e4611203926626e4363c2c9b04d79c9fc5ba2`.

The complete recursive diff of the executable object is exactly one leaf:

| Path within execution object | Before | After |
|---|---:|---:|
| `/execution/resources/wall_limit_seconds` | 600 | 900 |

There are no other executable-field additions, deletions, value changes or type changes. The proposed manifest retains `execution_authority: null`. The 30-second physical ceiling and the existing (0.30,0.30) sensory-free law are unchanged.

The complete outer-object diff is separately retained in `SEMANTIC_DIFF.json`: the execution SHA changes as a consequence; the mirrored per-case wall allowance changes from 600 to 900; a single-case amendment explicitly prevents batch restart or any next case; and three new documentation hashes bind Jason's instruction, that scope restriction and the resource estimate. These are authority/provenance bookkeeping for the requested isolated case, not additional controller/world/start/recording/validation changes. We do not claim that the entire wrapper differs at only one JSON path.

The original nine-case order and resource documents remain unchanged historical context and are explicitly inactive as a launch schedule. No previous 600-second grant is reused. Only the new outer hash may be authorized for this proposed execution.

Initial compressed snapshot SHA-256: `d8a2657916dc62a9a80d58d26f25f374e597526da69d409128ecf61c074aba2b`.
Complete initial-state SHA-256: `5cc5eda4aa4b1ac94fccda97ea42b485a2508fe33e2bb659f82cb61725d72671`.
Checkpoint: `a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad`.

All initial-state and start-manifest bytes, P/world/controller/runtime/configuration bindings, simulated horizon, native/wave/field cadence, stop/validation/recording implementation and prehistory identity are preserved. No production files were changed. No new simulation or controller inference occurred.
