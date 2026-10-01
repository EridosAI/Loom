# Jason's preparation instruction — 2026-09-29

**The S1-FULL result supplies the required productive FULL witness. Do not continue or retry S1-FULL and do not restart the nine-case batch.**

**Prepare one resource-adjusted execution object only for the existing `B1-MINIMAL-S1-SENSORY-FREE` case, using its exact already-prepared S1 initial snapshot, unchanged sensory-free controller `(0.30,0.30)`, unchanged 30-second simulated ceiling, unchanged recording/validation fidelity and unchanged checkpoint `a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad`.**

Increase only the administrative per-case wall-time allowance from 600 seconds to **900 seconds**. Bind this changed resource envelope into a new authority object.

Do not execute it yet.

Do not prepare or run S1-HIDDEN, S2 or S3.

Do not alter P, world, start, controller, horizon, validation, recording or prehistory.

Return:

- the new authority hash;
- semantic diff against the original S1-SENSORY-FREE object showing that only the administrative wall allowance changed;
- updated bounded resource estimate;
- confirmation that zero new simulation occurred.

Then stop for Jason's authorization.
