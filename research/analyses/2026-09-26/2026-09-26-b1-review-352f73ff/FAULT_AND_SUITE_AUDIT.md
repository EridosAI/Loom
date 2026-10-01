# Independent A–L and full-suite audit

All 12 RED/GREEN pairs reach their intended failure and pass unmutated. RED failures are checked in actual exception frames and JUnit failure bodies, not merely echoed source. Each pair has one test case and no collection error or skip.

| Pair | Intended observed failure | RED | GREEN |
|---|---|---|---|
| A | old rejection | 1 failed in 0.79s | 1 passed in 0.72s |
| B | CHEMISTRY PAYLOAD LEAK | 1 failed in 0.49s | 1 passed in 0.44s |
| C | CSS-ONLY MASK EXPORTED CHEMISTRY | 1 failed in 0.47s | 1 passed in 0.42s |
| D | DISPLAY DEPRIVATION ALTERED PHYSICAL RAW RECORD | 1 failed in 0.47s | 1 passed in 0.43s |
| E | PAUSED CLOCK/RNG/EXPENDITURE BREACH E | 1 failed in 1.04s | 1 passed in 1.05s |
| F | PAUSED CLOCK/RNG/EXPENDITURE BREACH F | 1 failed in 1.05s | 1 passed in 0.98s |
| G | PAUSED CLOCK/RNG/EXPENDITURE BREACH G | 1 failed in 1.01s | 1 passed in 1.02s |
| H | DUPLICATE CREATED EXTRA HOLD | 1 failed in 3.34s | 1 passed in 2.09s |
| I | OVERLAPPING EXECUTIONS ACCEPTED | 1 failed in 1.03s | 1 passed in 0.94s |
| J | ENDED ADVANCED WORLD | 1 failed in 1.02s | 1 passed in 1.10s |
| K | REFRESH/RECONNECT ADVANCED WORLD | 1 failed in 1.59s | 1 passed in 1.48s |
| L | FULL RAW LOST CHEMISTRY | 1 failed in 0.49s | 1 passed in 0.45s |

A reinstates the old restriction in the test and raises its actual ValueError; it is not an assertion about the hidden world. B/D/L alter detached projection inputs/condition; E/F/G/J/K inject the named causal effect. H disables consumed-token rejection around real short component holds. I disables running-state rejection around a synchronization stub; it demonstrates overlapping entry, not overlapping physical trajectories. C bypasses the real client validator in detached Node DOM execution; its actual failed assertion proves exported chemistry and is supported by the independent surface review. These scope distinctions are preserved instead of calling every pair a production-code mutant.

worktree-suite: **204 passed in 149.41s**; composition {"P_engineering": 59, "original_apparatus": 24, "previous_correction": 30, "final_correction": 30, "clock_correction": 33, "B1_operator": 28}.
portable-suite: **204 passed in 150.31s**; composition {"P_engineering": 59, "original_apparatus": 24, "previous_correction": 30, "final_correction": 30, "clock_correction": 33, "B1_operator": 28}.
