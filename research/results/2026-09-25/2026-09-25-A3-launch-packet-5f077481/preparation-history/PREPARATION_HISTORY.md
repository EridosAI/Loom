# Preparation history — no execution

Three invocations of the packet authoring helper occurred. None instantiated Run, calculated a controller command, stepped a body/field/neural system, drew simulation randomness, regenerated prehistory or replayed a trajectory.

1. The first stopped before creating an output folder: `KeyError: There is no item named 'FILE_MANIFEST.json' in the archive`. The nested A1 launch archive has the prefix `FIRST_COMMISSIONING_LAUNCH_PACKET/`; the archive reader was corrected to use its actual existing prefix. No input archive was changed.
2. The second wrote the proposed healthy zero-time snapshot and then stopped while serializing its provenance summary: `TypeError: Object of type ndarray is not JSON serializable`. A general JSON observation conversion was added to the preparation writer. The incomplete folder remains at `C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-25-A3-preparation-incomplete-serialization`. Its helper and snapshot are preserved here for portable audit.
3. The third completed the same selected fixture and route, with successful identity, hash, geometry and null-grant checks. Its snapshot is byte-identical to the second invocation: `c46547d56a64ed06252c6795e93cbbd3c489602a47bb04e90401f7b14757f49d`.

`PREPARATION_CHECKS.json` counts the final successful builder invocation: two snapshot loads, one deterministic instantaneous time-zero transduction and one snapshot save. Across the entire preparation task there were two such time-zero transductions (one in the incomplete authoring attempt, one in the completed attempt), four snapshot loads and two saves. These are duplicate static fixture authoring/roundtrip operations, not trial routes, impacts, lifetimes or trajectory replays. The healthy pose, E/I, plan, controller constants and horizon were not changed in response to either helper error.

The first helper revision differs from the preserved incomplete helper by only the nested archive prefix. Errors above are preparatory tooling errors, not A3 case failures. They do not authorize any execution or additional case.
