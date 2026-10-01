# A4 launch packet — prepared, not executed

One proposal, three independent predetermined physical witnesses. **Jason's separate authorization is required before any case runs.**

| Case | Start → destination | Prescription | Ceiling |
|---|---|---|---:|
| A4-CROSS | (10,8.8) → (10,12) | Cross during the initial clear window | 16 s |
| A4-WAIT | (6,8.8) → (6,12) | Hold own position through t=12, then cross | 28 s |
| A4-DETOUR | (1.5,6) → (1.5,14) | Exact A0 always-clear left bypass | 32 s |

All start healthy and stationary, facing north, E=0.7/I=1, with the same lawful phase-matched field history. No mover, body, reserve, sensor, controller-gain or P-law change. Starts are explicitly manufactured external fixtures, not sampled newborns. The wait is expressed through the existing paired-actuator waypoint interface. Static geometry and analytic timing make each strategy a meaningful proposed test; actual outcomes remain unobserved.

Read [the plain-language plan](PROCEDURES.md), [interpretation table](INTERPRETATION.md), [resource plan](RESOURCE_PLAN.md), [batch approval workflow](BATCH_EXECUTION_RULES.md), and [passive replay record contract](VIEWER_RECORD_CONTRACT.md). Exact manifest/snapshot/object files are in [A4-CROSS](cases/A4-CROSS/MANIFEST.json), [A4-WAIT](cases/A4-WAIT/MANIFEST.json) and [A4-DETOUR](cases/A4-DETOUR/MANIFEST.json).

The projected new trajectory total is about **15–16 wall minutes and 26.5–29.6 MB stored** (43.2–44.7 MB uncompressed), from actual A2/A3 receipts. Full native fidelity is retained. Hard administrative allowances are **35 runner minutes + 10 reporting minutes**, and **3 GB combined disk**. Prior review evidence adds about 155 MB to this portable packet; no simulation is needed to inspect it.

**Canonical batch authority SHA-256:**

`47a71e78ad4bbb920f2b29f7d9b0e3c5f520eb4905880916c85f0cc8bbb9f1e0`

[Readable authority object](AUTHORITY_OBJECT.json) · [exact canonical bytes](AUTHORITY_OBJECT.canonical.json). The outer object binds all three complete constituent objects. The unchanged apparatus is single-case; its future exact constituent approval envelopes must retain the genuine parent approval as described in the workflow. All current manifest grants are null; all three were rejected by the existing authorization gate. This is not an execution grant.

Preparation verification: **0 world/field/neural steps, 0 controller command calls, 0 simulation RNG draws, 0 new prehistory, 0 replay or candidate trials**. Three instantaneous t=0 sensor evaluations authored the three fixed snapshots; all inactive organism/RNG/field/body attributes except declared position, heading, raw sensors and provenance are unchanged. [Guarded preparation record](PREPARATION_CHECKS.json), [preservation record](PRESERVATION.json), and [review note](PREPARATION_REVIEW_NOTE.json). All **435 scoped original files** retained their hashes; the actual code worktree remains clean at the pinned apparatus commit. No Git writes or new commit.

The portable validator uses only saved bytes and the Python standard library. `python -B validate_packet.py` verifies this extracted directory; pass the ZIP path to verify the archive. It does not import Loom, compute commands or launch a world. The included authoring helper is provenance, not a launch command; it refuses an existing output directory and is tied to the original local references. No execution helper, live viewer, server or scheduler is included.

Remaining limitations: A4 performance, actual contact/timing, destination arrival and controller competence are untested; analytic nominal clearance is not a measured continuous-time clearance certificate. The detour uses its already-declared independent endpoints, so it is not an equal-endpoint efficiency comparison. P learning/perception, all-phase safety, lifetimes and every other commissioning row remain outside this packet. Full production launch preflight is deferred until genuine authorization. Stop here for Jason's review.
