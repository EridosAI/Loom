# Resource and time proposal — no execution permission

The corrected A5 recorder measured **7,714.9715165 wall seconds for 630 simulated seconds**, or **12.245987 wall seconds per simulated second**. Its stored trajectory was 448,657,204 bytes and its uncompressed streams were 376,284,429 bytes. This is the actual corrected-apparatus long-run basis, not the original short engineering-smoke rate.

| Case | Simulated ceiling (s) | Decisions | A5 compute proxy (min) | Repeated history rows | Stream planning bound (MB) |
|---|---:|---:|---:|---:|---:|
| PC-LR | 4 | 40 | 0.82 | 7,840 | 17.1 |
| PC-MOTION | 4 | 40 | 0.82 | 7,840 | 17.1 |
| PC-CONTACT | 6 | 60 | 1.22 | 17,760 | 36.7 |
| PC-HOLD | 10 | 100 | 2.04 | 49,600 | 97.8 |
| B1-FULL-RAW | 30 | 300 | 6.12 | 448,800 | 843.3 |
| B1-CHEMISTRY-HIDDEN | 30 | 300 | 6.12 | 448,800 | 843.3 |

Total ceiling: **84 simulated seconds / 8,400 native steps / 840 human decisions**. The base A5 proxy is **17.14 minutes**, before human deliberation and human-interface overhead. Illustrative deliberation allowances: 5 s per decision → 87.1 min total; 10 s per decision → 157.1 min total; 20 s per decision → 297.1 min total. These are arithmetic illustrations, not measured interactive throughput. Existing whole-history validation, serialization, HTTP response and browser rendering add unmeasured work.

The B1 horizon is **30 s per condition**, below the reviewed 180 s ceiling. The evaluator-only static geometry places a finite-body opportunity within an ordinary short approach, while retaining time for contact and some stock change. Prior A1/A2 physical access shows that such short approaches can fit well inside this ceiling; this is not a forecast for Jason's sensor-only choices. The fixed 30 s budget poses approach/contact/transfer and possible stock-linked sensory change, without requiring exhaustive discovery, depletion, adaptation over 180 s, or negative information conclusions. This is a selected short witness horizon, not a proof of the mathematically shortest sufficient trial. A miss does not authorize extension or a second start.

The current sensor-human recorder copies the full history into every decision input. For N complete holds starting at time zero, that is `N + 5*N*(N−1)` raw rows, plus cumulative past commands and notes. A 30-second trial has **448,800 repeated raw rows**, rather than only its 3,001 displayed history entries. Storage/validation cannot be projected simply by multiplying A5's constant-sized waypoint input rate. `RESOURCE_PROJECTION.json` accounts for this and records the equations.

The conservative stream envelope uses 1,200 bytes per raw row, 128 per historical command, 6,200 per historical 1,000-character note including escaping, and 10,000 bytes per decision for surrounding metadata/current note, plus the measured A5 physical-stream proxy. It gives each B1 case a **1.5 GB uncompressed-stream cap**, each operator control **256 MB**, and separate snapshot/display allowances. No compression saving is needed for that planning calculation. The byte envelope is a conservative schema calculation, not a new measured throughput result; actual caps can still terminate a case early.

Proposed wall limits: **20 minutes per control**, **2 hours per B1 trial**, including deliberation because the existing recorder's wall timer continues while bodily time is paused. No automatic extension, continuation or retry. Proposed reporting allowance after the pair: **1 hour**, saved records only. No automatic trial advances; positive-control and integrity gates are explicit human review steps.

Proposed combined-new-artifact ceiling: **12 GB**, including primary records, operator/evaluator outputs, retained packages and delivery copies. Require **12 GB free before any future launch**, request a clean administrative stop at **11 GB**, retain **1 GB** for final flush/receipt. Count disjoint directories and all copies, including snapshots; do not count the same path twice. At most four complete equivalent retentions are budgeted (primary, review copy, portable archive, delivered archive); the conservative primary-copy estimate is **9.421 GB**. Native recording fidelity and all mask-separated evidence remain intact. No test, benchmark, prehistory, trial or background process was run to estimate these costs.

These resource numbers do not close the interface HOLD. A reviewed deprivation/lifecycle implementation must retain the same cadences and record contract, and a regenerated packet must bind its actual identities before Jason considers execution.
