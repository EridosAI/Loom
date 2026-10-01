# Resource projection — unchanged ceilings, no execution permission

The measured basis remains the completed A5 record: 7,714.9715165 recorder wall seconds for 630 nominal simulated seconds, or 12.2459865 wall seconds per simulated second. A5 stored 448,657,204 trajectory bytes and 376,284,429 uncompressed stream bytes. Its privileged waypoint inputs differ from human histories; this is a physical-compute/recording proxy, not measured interactive throughput. No benchmark was executed.

| Case | Simulated ceiling (s) | Maximum decisions | A5 compute proxy (min) | Added lifecycle audit allowance (bytes) | Revised stream planning bound (MB) |
|---|---:|---:|---:|---:|---:|
| PC-LR | 4 | 40 | 0.82 | 84,992 | 17.218 |
| PC-MOTION | 4 | 40 | 0.82 | 84,992 | 17.218 |
| PC-CONTACT | 6 | 60 | 1.22 | 125,952 | 36.822 |
| PC-HOLD | 10 | 100 | 2.04 | 207,872 | 98.024 |
| B1-FULL-RAW | 30 | 300 | 6.12 | 617,472 | 843.907 |
| B1-CHEMISTRY-HIDDEN | 30 | 300 | 6.12 | 617,472 | 843.907 |

The **positive controls alone** total 24 simulated seconds, 2,400 native steps and at most 240 decisions. Their A5 base-compute proxy is 4.90 minutes. At 5 / 10 / 20 wall seconds of human deliberation per decision, illustrative total times are 24.9 / 44.9 / 84.9 minutes, before unmeasured interactive overhead.

The sealed pair adds 60 simulated seconds and at most 600 decisions, only if separately authorized later. All six ceilings total 84 simulated seconds / 8,400 native steps / 840 decisions. The preserved A5 base proxy is 17.14 minutes; 5 / 10 / 20 seconds of deliberation per decision give 87.1 / 157.1 / 297.1 minutes before unmeasured interactive work. These are arithmetic illustrations, not forecasts or resource extensions.

The held history bound is preserved: for N holds from time zero, controller inputs repeat `N + 5*N*(N-1)` native rows. A 30-second case repeats 448,800 rows. The original allowances remain 1,200 bytes per raw row, 128 per prior command, 6,200 per prior 1,000-character note including escaping, 10,000 per decision for metadata/current note, plus A5's physical-stream proxy. No storage saving is credited for omission of four chemistry values; private physical chemistry remains complete.

The sole necessary estimate increment is the corrected private lifecycle stream: at most `2*N + 3` normal lifecycle rows, budgeted at 1,024 uncompressed bytes each. This covers preparation/start, accepted-command and completed-pause transitions, and end. Existing snapshot/display allowances remain 50 MB per control and 150 MB per B1 case. Extraordinary failure tails remain covered by the existing flush reserve; this is a planning envelope, not a promise that failure cannot exhaust storage.

**All hard limits are unchanged:** 256 MB uncompressed streams and 1,200 wall seconds per control; 1.5 GB and 7,200 wall seconds per B1 case. Deliberation advances no simulated bodily time, but the administrative wall timer continues. No automatic extension, continuation or retry follows a resource stop. Reporting allowance remains one hour, saved evidence only.

The combined-new-artifact cap remains 12 GB, with a stop request at 11 GB and 1 GB reserved for final flush/receipt. Require 12 GB free before any future launch; count all disjoint output directories and retained copies. At most four equivalent retentions remain budgeted. The revised conservative combined primary-copy estimate is **9,428,381,812 bytes (9.428382 GB)**. No horizon or native recording fidelity was reduced.

Corrected projection, validation, history hashing, polling, HTTP serialization and browser rendering add unmeasured cost. Read-only polling creates no physical steps and no trajectory stream by itself. Actual disk or wall limits can still end a case early. No performance guarantee, human policy, useful-learning gate or B1 outcome criterion is introduced.
