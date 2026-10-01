# Loom P — proposed A2 launch packet

**PROPOSED / NOT AUTHORIZED — no A2 execution occurred.** Prepared 2026-09-25 by Codex for Jason's review. This packet proposes exactly one fresh A2 physical-ceiling witness. It creates no experiment number, scientific preregistration or evidential freeze.

Canonical authority-object SHA-256:

`229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007`

The [canonical object](AUTHORITY_OBJECT.canonical.json), [readable object](AUTHORITY_OBJECT.json) and [manifest](A2_MANIFEST.json) agree. The manifest's `execution_authority` is **null**. The reviewed authorization function rejected it as unauthorized. Jason's old A1 authorization does not apply to this object.

## What the proposed trajectory would do

Start from the same manufactured zero-time body/world state used for A1. The body is at (6,3), facing west, with E=0.7 and I=1; all eight sources start with stock 0.2. The first instruction takes it toward source 0 at (3,3), then maintains the existing gentle contact target until the clock reaches 90 seconds. The actual A1 record showed energy gain becoming negative in the 52.0–52.2-second contact window even though the source was still transferring energy. This proposal gives that decline time to be observed again; it does not demand an empty source or assume an A2 result.

At 90 seconds the same controller is instructed to turn toward (6,3), its original starting point, with the contact-press target disabled using the existing zero-target stage setting. At 120 seconds its target becomes source 1 at (10,3), with the same 0.1 contact-force target used at source 0. The case ends at 180 seconds or the first earlier stop. The intended path follows the clear bottom corridor: source residence, departure, five units of free centre travel between contact loci, then another source encounter.

Nothing is replenished or reset during the trajectory. Energy, integrity, source stocks, chemicals, mover motion, commands and history continue normally. The destinations are instructions to the unchanged controller, not teleports or an enforced path. If it fails to turn, separate, arrive or obtain productive contact, those observations stand. They do not automatically establish an impossible ecology.

## Exact proposal

| Item | Proposed value |
|---|---|
| P implementation | `6bc9683b54e4fa80136fe8534d7713e2a250a95f` |
| Apparatus / current HEAD | `5f07748102cb5eaa302569c87efbae095050e9fe` |
| Worktree | `C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405` |
| Branch | `build/p-commissioning-apparatus-20260924-01a0c405` |
| New commit / code changes | None / none |
| Arm | `external_controller`, reviewed deterministic `waypoint`; neural object inactive |
| Initial fixture | Fresh A2 label, exact saved **initial** A1 state copied; no historical A1 continuation |
| Initial physical state | Time/index 0; position (6,3); angle 3.141592653589793; velocity/omega/commands/forces/contact rates zero; E 0.7; I 1 |
| Source 0 / source 1 | Centres (3,3) / (10,3); source radii 0.5; body radius 0.5 |
| Phase / seed identity | 3.558411277237072; existing verified life-0 prehistory, master seed 5284097 |
| 0–90 seconds | Target (3,3), press target 0.1 |
| 90–120 seconds | Target (6,3), press target 0 |
| 120–180 seconds | Target (10,3), press target 0.1 |
| Native time / command hold | 0.01 s / 0.1 s, unchanged |
| Simulated ceiling | 180 s; at most 18,000 native steps and 1,800 decisions |
| Execution wall ceiling | 3,600 s (60 minutes), then preserve the stop |
| Stream ceiling / disk reserve | 1.5 GB uncompressed streams / 3 GB local free space for all evidence and copies |
| Read-only reporting allowance | Separate maximum one machine-hour; zero evolution/replay |

Exact controller gains, formulas' source identities, phase/prehistory files, complete snapshot and inactive RNG/neural state are bound through [the procedure](PROCEDURES.md), [initial state summary](INITIAL_STATE_SUMMARY.json) and [code/runtime identities](CODE_AND_RUNTIME_IDENTITIES.json). No capacity, renewal, uptake, expenditure, reserve, geometry, controller gain, P mechanism or configuration is changed.

Initial snapshot SHA-256: `348079e967a34a98cd395a5b117f484c3ea8ba58edc6b0f4cb3f4975e6bbd557`.

Full initial state SHA-256: `37adf68654e324141c678316f0f1f4b777853948e548cdd0d133e810c8722a6b`.

## Why this case and budget

Source 1 is the nearest different source from source 0's right-hand contact locus. Reusing the original starting point as the departure waypoint separates the existing press servo from free-space departure. The prescribed straight segments have no intervening solid: their minimum wall clearance is 2.5 units and clearance from the mover's swept rectangle is 6 units, accounting for body radius. [The exact geometry calculation](GEOMETRY.json) does not claim that the controller will follow those segments.

The first 90 seconds build directly on the observed A1 approach/residence. The next 30 seconds allow turning and the two-unit move to (6,3); the final 60 seconds allow the remaining three-unit approach to contact and a period at source 1. No alternate route, start or duration was tried. The allocation is not a dynamically verified sufficiency bound.

The [resource calculation](BUDGET.json) uses actual A1: 91.83000000001007 simulated seconds, 1,201.2759735999862 recorder wall seconds, 54,337,980 uncompressed stream bytes and 24,977,060 stored trajectory bytes including snapshots/receipt. This projects **39.24 minutes**, **106.51 MB uncompressed** and **48.96 MB stored** at 180 seconds. The recorded late-A1 rate gives **40.43 minutes**. The proposed hour leaves roughly 53% headroom over the average. Growth of saved history, event volume and host load remain uncertainties; reaching 180 seconds is not guaranteed. At the same average, 400 seconds would require about 87.2 minutes, before margin. No short engineering-smoke throughput is used.

The storage guard counts streams, not all snapshot/archive bytes. The separate disk reserve covers those other files; preparation observed ample local free space, but the launch preflight must check again. Record closure may finish after the wall-time stop without adding physical time. There is no automatic extension or resume.

## What would be reported

The [predeclared interpretation table](INTERPRETATION.md) keeps contact, transfer, stock, gross intake, expenditure, net E, the first net-negative residence window, departure, departure E/I, actual travel time/cost, mover interaction, second-source arrival/stock/contact/transfer, positive-net second-source windows, final E/I and all failure/stop categories separate. There is no overall physical-outcome PASS/FAIL and no useful-learning or survival pass gate.

All existing native physical evidence is retained. A future passive viewer can distinguish residence, departure, travel and the second encounter. Mover geometry retains its existing controller-decision cadence; no invented higher-rate recording is claimed. No live viewer is inserted. The original failed A1 V3 check, corrected V3 analysis and derived passive viewer remain distinct historical records. Their current registered status is V1/V2/V3/A0 complete and one A1 witness observed; no check is relabelled as an A2 result.

## Preparation verification and remaining issues

Preparation verified 49 original A1 payloads, 65 nested launch payloads and 53 V3/viewer package payloads. It checked the exact P/configuration against Git, live apparatus/runtime/controller identities, unchanged controller dispatch, the complete proposed execution structure, null-grant rejection, snapshot checksum/zero-time physical state, exact cached fields/phase/law identities and finite-body segment geometry. Original source/runtime/cache/A1/analysis files remained unchanged across 210 recorded file hashes. The code worktree remained clean at the same HEAD. [Preparation checks](PREPARATION_CHECKS.json) and [preservation proof](PRESERVATION.json) record the scope.

No missing runtime or read capability blocked preparation. The optional global Git ignore file was unreadable, so repository-status queries used a separate empty excludes file for that command only. An initial attempt to name Windows NUL as the excludes file was rejected by Git before packet construction; using a regular empty file resolved this read-only tooling issue. No Git settings or repository content were changed. Workbench delivery uses a new INBOX folder only.

Remaining uncertainties are the controller's actual half-turn/release behavior, possible continued first-source contact when the next press stage begins, arrival timing, actual second-source productivity and runtime growth. The positive-target servo reacts to any contact; it has not been changed to prefer a source. These are disclosed observations for the single proposed case, with no rescue policy. Production validation on the loaded exact state/cache remains a required later launch preflight. The existing A1 checker is archive-bound; its corrected alignment is the documented basis for later read-only A2 analysis, not a claim that an A2 analyzer has already run.

**Not executed or tested here:** any A2 trajectory or command; Engine or Run construction; physics, fields or neural advancement; simulation RNG draw; new prehistory; A1 continuation/replay; departure dynamics; second-source arrival/transfer; performance benchmark; apparatus regression suite; other commissioning cases; newborn/scientific lifetimes; tuning or efficacy. No background run, Git write, push, PR, merge or canonical Workbench update occurred.

Stop at this review boundary. Execution requires Jason's separate approval of the exact authority hash above.
