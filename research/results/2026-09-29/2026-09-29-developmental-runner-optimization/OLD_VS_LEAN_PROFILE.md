# Measured old versus lean execution

Actual Windows-local Python 3.13.5 engineering measurements, 29 September 2026. No scientific lives or outcome comparisons. P and physical laws are frozen. Decimal MB throughout; RAM means process peak working set, not total system RAM.

## Unprofiled execution

| Path / simulated duration | Total wall s | Wall s / sim s | Native steps / wall s | Waves / wall s | Stored MB / sim s | Peak RAM MB |
|---|---:|---:|---:|---:|---:|---:|
| old-0.6 | 9.8747 | 16.4578 | 6.08 | 0.30 | 6.50173 | 89.54 |
| lean-0.6-release | 0.5671 | 0.9452 | 105.80 | 5.29 | 1.67940 | 92.45 |
| lean-30-memory-fix | 10.2473 | 0.3416 | 292.76 | 14.64 | 0.10616 | 93.18 |
| lean-600-pre-memory-fix | 204.1218 | 0.3402 | 293.94 | 14.70 | 0.08711 | 463.99 |

These totals include boundary setup/checkpoint closure and exclude post-run verification, analysis and archive creation. The matched 0.6-second comparison is **17.41× faster** and **3.87× smaller**, including small-run boundary costs. Same fixture and exact complete causal endpoint. Old stored 3,901,036 bytes; release lean stored 1,007,643 bytes.

For sustained lean execution, the single 600-second benchmark took 204.1218 s including 0.3021 s setup; 203.8197 s for the native loop and closure (0.339699 wall/sim; 294.38 native steps/s). This is about 48.4× the old short-run rate, **not** a matched 600-second old/lean trial. No 600-second old run was needed or performed.

The 600-second run used the original lean codec before its memory-retention correction. It is retained unchanged. Its 463.99 MB peak is an observed engineering defect, not the release memory claim. Final memory correction: same encoded bytes, zero retained recursive codec closures; final 30-second benchmark peak 93.18 MB. Processing 180,000 saved native rows (no simulation) remained approximately 65–67 MB. The release adds Python DLL binding at boundaries and avoids deep copies during Tier-2 warm-up; neither changes the causal scheduler. The release 0.6-second and split runs/test suite exercise the exact delivered source.

## Measured subsystem attribution

Both context profiles cover setup, 0.2 simulated seconds and closure. Values are exclusive wall seconds attributed to the active subsystem, excluding measured profiler callback time. They are measured, but profiling perturbs execution. Use the unprofiled table for speed. Nested JSON/hash/copy/I/O work is assigned to those categories, not charged again to the parent diagnostic/checkpoint category.

| Subsystem | Old seconds | Lean seconds |
|---|---:|---:|
| other_harness | 0.025476 | 0.003302 |
| validation_accounting | 0.032214 | 0.004599 |
| hashing_binding | 0.170759 | 0.328091 |
| filesystem_io | 0.083081 | 0.143949 |
| serialization | 3.597045 | 0.196108 |
| state_copy | 0.256278 | 0.007532 |
| body_contact_viability | 0.018158 | 0.017327 |
| compression | 0.251292 | 0.019782 |
| snapshot_checkpoint | 0.000574 | 0.000186 |
| recorder_writes | 0.001544 | 0.004443 |
| P_neural | 0.027392 | 0.025225 |
| chemical_field | 0.032479 | 0.026528 |
| sensor_computation | 0.032123 | 0.031340 |
| observer_diagnostics | 0.016992 | 0.000000 |
| detached_D5 | 0.000612 | 0.000000 |
| tier1_extraction | 0.000000 | 0.000671 |

Old attributed execution totals 4.546020 s, of which serialization is 79.1%. Callback overhead was 5.337442 s. Lean attributed execution totals 0.809083 s, plus 1.225704 s callback overhead. Lean boundary hashing appears large at 0.2 seconds because it hashes the installed numerical runtime once; it does not repeat per step.

The first pre-optimization cProfile independently recorded JSON encoding, recursive state packing and base64 conversion as dominant functions. Its full `.pstats` and raw JSON are preserved. Context attribution was subsequently added to separate shared kernels from callers. Inclusive values below are from that first profile; they overlap and must **not** be added to the exclusive table or one another.

| Baseline operation | Calls | Inclusive s |
|---|---:|---:|
| passive | 20 | 1.596118 |
| save_restart | 2 | 0.165864 |
| observe_native | 20 | 0.193873 |
| validate_state | 20 | 0.388230 |
| motor_receiver | 1 | 0.000113 |
| wave_receiver | 1 | 0.017172 |

The expensive observer path includes repeated hashes of before/after complete engines, duplicate neural operands and detached receivers. D5 arithmetic itself is small on this fixture; the surrounding copying/encoding/interference proofs are expensive. The unchanged P computations themselves are retained, including their internal diagnostic construction. No mathematical simplification was made to improve these timings.

Filesystem writes/fsync and compression are measured separately above. Packaging during a life is zero in both measured benchmark drivers; the final review archive is made only after all execution stops. No live charts or browser were launched.

## Checkpoints, pause/resume and verification

| Cost | Old | Lean |
|---|---:|---:|
| Standalone/final short checkpoint bytes | 937,942 | 834,797 |
| Short checkpoint seconds | 0.112811 | 0.031680 |
| Pause at native index 7, including checkpoint | 0.106394 | 0.034135 |
| Exact reload/resume, including custody checks | 0.501506 | 0.639756 |
| Post-run verification | 0.829789 s, one 0.6 s segment | 0.100586 s, one 0.6 s segment |

The lean two-segment split verification took 0.135748 s. Strong lean reload binding can cost more than the old short reload; this is a boundary cost and is intentionally retained. The long run stored 11 checkpoints totaling 9,325,795 bytes, took 0.345343 s in checkpoint writes, and 6.723229 s in chunk closure. Mean noninitial checkpoint: 919,721 bytes / 0.033476 s. Full 600-second post-run verification took 8.652640 s; no physical replay or P execution in that check.

Whole-600-second neural reconstruction from saved sensory input took 47.7099 s (600 exact chunk-end P/RNG checks). Selected final 20-step deep analysis including a 60-second checkpoint warm-up and exact realized-field reconstruction took 12.3626 s in the release. These are post-run analysis costs, excluded from execution throughput.

## Bytes by record family

Old actual on-disk files, 0.6 seconds:

| Family | Stored bytes |
|---|---:|
| controller.jsonl.gz | 37 |
| diagnostics.jsonl.gz | 1,492,938 |
| events.jsonl.gz | 5,404 |
| final.restart.json.gz | 937,942 |
| initial.restart.json.gz | 128,570 |
| manifest.json | 7,881 |
| native.jsonl.gz | 1,095,921 |
| scientific_observations.jsonl.gz | 50 |
| sensor-display.json | 35,437 |
| sensor.jsonl.gz | 14,438 |
| wave.jsonl.gz | 182,418 |

Old native plus diagnostics streams alone used 2,588,859 bytes (66.4% of all short-run storage). They contain overlapping sensory/neural structures and detailed operands. Full restarts are the next major short-run cost.

Lean 600-second family accounting:

| Family | Bytes |
|---|---:|
| native | 36,511,800 |
| waves | 25,182,741 |
| events | 71,225,400 |
| checkpoint | 9,325,795 |
| chunks_stored | 42,539,633 |
| metadata | 398,638 |

`native`, `waves` and `events` are exact encoded **uncompressed family payload** sizes. They are compressed together per chunk: `chunks_stored` is their actual combined stored size, not an additional raw family. `checkpoint` and `metadata` are stored sizes. Do not add raw and compressed columns. Total actual primary store = 52,264,066 bytes, or 0.087107 MB/simulated second. One shared identity asset is around 0.3 MB per apparatus/runtime and is reused, not added per life.

Lossless representative chunk comparison (raw 223,464 bytes): level 1 about 67.6 kB, level 3 about 66.9 kB, level 6 about 66.7 kB. Level 6 saved only about 1.4% against level 1 while taking roughly 50% more compression CPU. Level 1 is retained. Actual measurements for every tested level and exact byte round-trip checks are in `measurements/long.json`. A final archive stores already-compressed `.ld` members without recompressing them.

## Throughput versus age

Single longer engineering trajectory, grouped into 100 simulated-second blocks:

| Nominal age interval s | Wall s | Wall / sim |
|---|---:|---:|
| 0–100 | 33.4880 | 0.334880 |
| 100–200 | 34.1200 | 0.341200 |
| 200–300 | 34.4253 | 0.344253 |
| 300–400 | 34.0540 | 0.340540 |
| 400–500 | 33.7235 | 0.337235 |
| 500–600 | 34.0017 | 0.340017 |

All individual 10-second blocks, and old/medium blocks, are in `THROUGHPUT_BY_AGE.csv`. No increasing time-per-step trend large enough to indicate whole-history copying appeared over this fixture's 600 seconds. This is not a claim covering every possible contact load or 1,800-second developmental history. The small receipt list is O(chunks); full native history is neither recopied nor re-encoded each step. The separate 180,000-row codec test is a storage scaling check, explicitly not a life.
