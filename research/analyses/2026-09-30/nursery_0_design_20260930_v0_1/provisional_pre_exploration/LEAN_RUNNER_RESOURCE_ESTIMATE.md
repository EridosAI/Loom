# Lean-runner resource estimate — design only

Basis: all 59 authentic closed `FS-xxx_STOP.json` receipts listed in [SOURCE_MANIFEST.json](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_0_design_20260930_v0_1/SOURCE_MANIFEST.json>); unclosed FS-060 excluded from full-life rates, never treated as free/zero-cost execution. Preparation basis is `PREPARATION_BOUNDARY_RESOLUTION.json` (48 completed body-absent preparations, 5808.444936249638 s). No benchmark was run now.

| Rate | Minimum | Median | Maximum |
|---|---:|---:|---:|
| Active wall seconds / simulated second | 0.317938305 | 0.347838795 | 1.049651918 |
| Primary bytes / simulated second | 72781.550 | 75635.822 | 94612.587 |
| Per-600-s wall projection | 190.763 | 208.703 | 629.791 |
| Per-600-s evidence projection, decimal MB | 43.669 | 45.381 | 56.768 |

These are old-layout rates extrapolated to full 600 s. No nursery speedup assumed; no early biological death used to discount the budget. The slowest completed life is FS-025; its cause is not diagnosed here. New twelve-source rows add four float64 stocks: 32 bytes/native step, 1.92 MB/600 s before compression; contact/event growth is not bounded by this linear estimate. Smaller field arrays could help but no saving is booked.

Optional six-life paired A/B calibration only, if separately authorized: 3600 total simulated seconds maximum, three new jointly lawful 600 s body-absent field histories reusable across candidate pairs only after identity checks. Median execution 1252.22 s plus preparation 363.03 s plus roughly 85 s basic verification, about 28–30 min excluding engineering. Old worst execution rate plus mean preparation/basic verification is about 70 min. Nursery contacts may exceed that.

Proposed review reserves: **1260 active wall s / 120 MB per life**, no redistribution; **7560 active wall s / 720 MB** for six lives. **726 active preparation seconds total** and **600 passive verification/report seconds** are separate planning reserves, for a combined approximately **2.5 h**. The preparation reserve is twice the historical mean for three histories, not a measured upper bound or a bypass of the existing prehistory projected-cost check. A later packet must specify actual per-history limits and stop semantics before any preparation. Budget **1 GB working space plus 1 GB for one archive**; do not assume compression savings or repeatedly create archives.

For another later approved cohort size n, use n × 600 × measured rate plus distinct preparation, verification and archive costs. This is arithmetic, not permission to create a cohort, extend lives to 900/1800 s or enlarge the resource envelope. Full P replay/receiver diagnostics are outside this opportunity-calibration estimate. Tier-1 fidelity remains unchanged; schema changes must retain exact source stocks and field identities. Follow [NURSERY_0_DESIGN_v0_1.md](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/nursery_0_design_20260930_v0_1/NURSERY_0_DESIGN_v0_1.md>) for the required future apparatus update.

FS-060 remains APPARATUS_INTERRUPTED_UNCLOSED. Its interruption is not explained by these rates and is not evidence that the nursery will run reliably. Separate execution observability review is required before a future launch decision.
