# A5 conditional resource plan — full fidelity, no benchmark

**Awaiting authorization:** the clock correction is reviewed and the proposed full 630-second schedule passes scalar preflight. These remain the unchanged A2/A3-based estimates, not a new benchmark or runtime guarantee. The scheduler correction requires no change to the retained numerical projection.

| Measured evidence | Recorded simulated time | Wall s / simulated s | 630 s recorder projection | 630 s uncompressed streams |
|---|---:|---:|---:|---:|
| A2 | 180.00 s | 11.755737 | 123.44 min | 369.80 MB |
| A3 | 210.00 s | 11.934442 | 125.31 min | 358.03 MB |
| A4 | 76.00 s | 11.418702 | 119.90 min | 321.46 MB |

A2 and A3 are the controlling long-run measurements; A4 supplies a recent shorter three-case comparison. Whole-process projections and all exact receipts are in `RESOURCE_PROJECTION.json`. Plan for **roughly 2.0–2.1 hours of execution**, plus reporting. Accumulating sensor history, snapshots, host load and contact complexity may make 630 seconds slower than this extrapolation. No new throughput test was run. The predetermined runner ceiling is **4 hours (14,400 s)**, followed by at most **1 hour (3,600 s) saved-data reporting/checks/packaging**. The allowance is 5 hours total, not a guarantee or permission to continue the trajectory.

Storage must include accumulated restart histories. A naive linear stored-bytes extrapolation undercounts them. The model takes each measured initial/final compressed snapshot slope and sums predicted sizes at t=0, every 10 seconds through 630, and the additional final snapshot. That is **65 snapshots**, including the separate t=630 checkpoint and final receipt state. Gzip streams and final sensor-display bytes are scaled separately, plus 1 MB miscellaneous allowance. This assumes approximately linear history-size growth, not a fitted physical trajectory.

| Long-run basis | Snapshot total | Compressed streams | Final display | Total including miscellaneous |
|---|---:|---:|---:|---:|
| A2 | 335.82 MB | 68.04 MB | 39.66 MB | 444.52 MB |
| A3 | 368.16 MB | 65.90 MB | 39.18 MB | 474.24 MB |

Allow **1 GB for the new trajectory** for planning; no record thinning. The uncompressed stream cap is **1.5 GB**, distinct from compressed files and checkpoints. The launch review adds about 167 MB of historical evidence, roughly 170 MB packaged. Allow up to 1.2 GB per result bundle with launch evidence. A planning example with 1 GB raw + 0.4 GB derived material + two extracted 1.57 GB result trees + two 1.2 GB ZIPs + existing new launch copies totals under 8 GB; it is an allowance, not a measured future size. All new artifacts and copies share a **10 GB** ceiling. Existing historical originals are excluded from this new-work total; any new copies count.

Before a future authorized launch, require 10 GB free. An administrative monitor of the specifically bound new output directories must check combined usage before each held command and stop at 9 GB or free space below 1 GB, reserving 1 GB for finalization. It may call the existing clean resource-stop interface only; it does not change physical laws or commands. Before each later analysis/copy/archive operation, include its bounded size estimate and stop if the 10 GB ceiling would be exceeded. Preserve originals; never reclaim space by deleting historical evidence. No such launcher/monitor is implemented or invoked in this preparation packet. A future separately authorized execution must implement this same administrative accounting before its first world step.

The unchanged runner checks wall time and uncompressed-stream reserve at native boundaries. These and the combined-disk rule are hard administrative stop instructions, not exact OS quotas: a current native operation, final snapshot or flush may overrun a threshold. Record actual values and any I/O failure; do not restart or continue. If the cap prevents full delivery, preserve completed originals and report the missing derivative/copy rather than drop evidence.

Full 100 Hz native, all event subdivisions, 10 Hz commands, sensor endpoints, diagnostics and restart histories are retained. The legacy selection stride is not native decimation. No plot/live viewer enters the loop. No physical terminal, controller miss or resource stop permits tuning or a second attempt.
