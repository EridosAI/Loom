# Resource reprojection — design arithmetic only

Fixed schedule: **12 × 600 seconds**, up to **4 × additional 300 seconds** (900 total age), up to **2 × additional 900 seconds** (1,800 total age). Same continuing lives. This report changes neither those ages/population sizes nor the developmental-selection direction. It creates no execution authority.

Basis: one disclosed 600-second intact-P engineering fixture, 0.339699 execution wall seconds per simulated second, 87,106.8 stored bytes per simulated second. Boundary setup from the release split measurement, extra continuation checkpoints included conservatively. Single worker; no assumption of free parallel scaling. The long fixture is not a Founder birth and its outcomes are not assessed.

| Stage | Simulated s | Expected execution | Proposed execution allowance | Expected primary | Expected one archive |
|---|---:|---:|---:|---:|---:|
| initial | 7,200 | 40.87 min | 66.40 min | 0.627 GB | 0.630 GB |
| continuation_1 | 1,200 | 6.83 min | 11.13 min | 0.108 GB | 0.109 GB |
| continuation_2 | 1,800 | 10.21 min | 16.57 min | 0.159 GB | 0.159 GB |
| maximum_total | 10,200 | 57.90 min | 94.10 min | 0.894 GB | 0.898 GB |

The allowance uses 0.55 wall/sim plus 2 seconds per segment: about 62% above the observed sustained rate, with boundary overhead. It is a proposed administrative envelope, not a guarantee under all collision/solver workloads. A future launch packet must bind actual limits and stop/report rather than change laws if exceeded. Existing phase caches may be reused only lawfully; no new phase was prepared here.

Storage reserves: initial primary **1.0 GB** plus one archive **1.0 GB**; full staged primary **1.5 GB** plus one archive **1.5 GB**. Additional temporary workspace **0.25 GB**, selected Tier-2 outputs **0.5 GB**: total proposed capacities **2.75 GB initial / 3.75 GB full**, without an extra unpacked copy. These are reasonable planning reserves, not measured exact maxima. Runtime/dependency installation is shared and excluded from per-population scientific storage. One worker's observed release peak was about 93 MB working set; allow 0.5 GB working set and 2.5 GB process commit because NumPy/BLAS reserves more committed/virtual memory than resident RAM.

Keep costs separate:

- **Prehistory, if all 12 phases are missing:** historical unchanged field-only preparation measured 65.1784 seconds per phase; 13.04 minutes projected, 20-minute separate planning reserve. This task did not prepare any phase. That work requires the later approved preparation scope.
- **Full record verification:** 1.73 minutes initial; 2.45 minutes full at the measured rate. Reserve 3 / 5 minutes, separately from execution.
- **Archive creation:** compressed chunks/checkpoints are copied into one verified archive after the stage, with no recompression and no full unpacked duplicate. Reserve 2 minutes for this modest local volume; the actual review-package write/hash cost is recorded in `DELIVERY_VERIFICATION.json`.
- **Tier 2:** whole-600-second P-only reconstruction measured 47.71 seconds. A final 20-step deep interval with a preceding 60-second neural/field warm-up measured 12.36 seconds. Propose up to four selected 60-second deep windows for an initial review, with 15 minutes of analysis CPU and 0.5 GB derived outputs reserved. This is a bounded analysis proposal, not authorization or a claim about unlimited future dossiers. Human reading time is separate.

Thus the initial execution itself is roughly **41 minutes**, with a **66.4-minute allowance**. With optional missing-prehistory reserve, verification, one archive and the proposed selected analysis, initial machine time planning is about **106 minutes**; the full staged envelope about **136 minutes**. No old 57 h / 200 GB or 82 h / 280 GB allowance is carried forward. Historical design documents remain preserved, with this measured reprojection supplied as a new document.

Uncertainty: the single long fixture does not sample all future contact loads, field-solver demands or machine contention. The reserve is explicit; it does not justify scientific execution, automatic retry, more bugs or altered horizons. No 900/1,800-second lived trajectory was benchmarked. Final-code 1,800-equivalent record-count checks use saved rows only.
