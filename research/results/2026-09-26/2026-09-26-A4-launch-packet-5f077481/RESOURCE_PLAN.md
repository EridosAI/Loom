# A4 resource projection — no new benchmark

The source measurements are the complete A2 180 s and A3 210 s records. A2 used 2,116.03 recorder wall seconds, 105.66 MB uncompressed and 62.74 MB stored. A3 used 2,506.23 recorder wall seconds, 119.34 MB uncompressed and 81.73 MB stored. Exact receipts and calculations are in `RESOURCE_PROJECTION.json`, with unchanged originals under `references/` and inside the sealed A3 result archive.

| Case | Simulated ceiling | Projected recorder time | Projected stored trajectory | Runner wall cap |
|---|---:|---:|---:|---:|
| A4-CROSS | 16 s | 3.13–3.18 min | 5.58–6.23 MB | 8 min |
| A4-WAIT | 28 s | 5.49–5.57 min | 9.76–10.90 MB | 13 min |
| A4-DETOUR | 32 s | 6.27–6.37 min | 11.15–12.45 MB | 14 min |

Total: **76 simulated seconds, 7,600 native steps, 760 controller decisions** at full recording fidelity. The two measured rates project **14.89–15.12 minutes** of recorder time and **26.49–29.58 MB stored**, or **43.19–44.61 MB uncompressed**. Whole-process linear extrapolation is 14.90–15.22 minutes. Allow roughly **15–16 minutes plus saved-data reporting**; three fresh starts and mover-specific contacts may cost differently. No completion guarantee or throughput benchmark was run.

The fixed administrative runner caps total **35 minutes**, plus **10 minutes total for read-only validation/reporting/packaging**. Each case has a 100 MB uncompressed-stream cap; these are distinct from the combined 3 GB disk cap for primary records, analysis and delivery copies. Require 3 GB free before launch and before each subsequent case. A clean resource pause ends the batch without resume or substitution. The unchanged native-step guard and final flushing can add a small overrun; an I/O fault is an apparatus failure, not a clean cutoff.

The portable launch packet also carries about **155 MB of immutable nested A0–A3 review evidence**, which dominates its size. Budget about **160 MB for the launch packet** and **200 MB per final review bundle** including launch evidence and new records. Preserve raw originals and copied packages within the same 3 GB allowance. The delivery receipt gives actual preparation package bytes.

No thinning of native records, sensors, events, controller samples or snapshots is allowed. Snapshot/history overhead is not perfectly linear; short independent cases differ from A2/A3. Do not reclaim space by deleting historical evidence. The basal/max-command conservative energy floors at the ceilings are CROSS 0.66, WAIT 0.63 and DETOUR 0.62 in the absence of intake; this is an accounting bound, not a survival or learning gate.
