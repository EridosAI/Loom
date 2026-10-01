# A5 clock compatibility — new static finding; report, do not patch

**Disposition: HOLD for this proposed 630-second case on apparatus `5f07748102cb5eaa302569c87efbae095050e9fe`.** P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. No A5 execution has occurred. This does not relabel prior A1–A4 results or rewrite the scoped final mechanical closure review.

## Source path and deterministic arithmetic

The external adapter's `coupled` function in `loom_commissioning/adapter.py` increments `e.time += dt`; nonterminal full native steps use dt=0.01. The runner issues a command every ten steps. `pending.py::validate_decision` requires

$$|t-(t_0+(i-i_0)0.01)|\le 10^{-10}.$$

For the exact zero-time/index initial fixture, repeated binary-float addition first exceeds that absolute tolerance at native 26,941. The first subsequent ten-step decision boundary is **26,950**:

| Quantity | Exact Python representation used in the audit |
|---|---:|
| Accumulated time | 269.4999999998999 |
| Index-derived time | 269.5 |
| Difference | -1.0010126061388291e-10 |
| Permitted absolute difference | 1e-10 |

Accordingly, **if the case remains nonterminal and has not stopped earlier**, its next decision at that point fails the unchanged `issued decision clock mismatch` predicate. The first prescribed revisit does not begin until the source-0 stage at t=300. Changing only a later stage deadline cannot avoid this absolute decision-clock predicate. Ordinary save/resume retains the same initial clock and accumulated state, so splitting the case cannot lawfully reset it away.

There is a second implicated predicate at t=270: the accumulated clock is 269.99999999989944, more than 1e-10 below the stage deadline. The existing `time_due` comparator would not treat that nominal boundary as due, and the runner's full-hold boundary check would reject the next hold. The earlier decision-clock predicate already prevents reaching this as a launch outcome.

`clock_audit.py` imports only the Python standard library and performs scalar additions/comparisons. It neither imports Loom nor constructs or advances a body, field, world, controller, RNG or replay. `CLOCK_AUDIT.json` records the arithmetic, exact source hashes and source excerpts. Static findings are distinguished from executed commissioning evidence: **no production failure receipt is claimed**. An earlier genuine physical terminal or resource stop could occur; the calculation does not predict physical survival to 269.5 seconds.

## Why this is a launch hold

The manifest's declarative schema, route-grid and identity checks can pass while this longer-horizon runtime predicate remains incompatible. Reporting a green static schema check as full launch fitness would be misleading. A1/A2/A3 and the individual A4 cases ended before this boundary; their preserved results and earlier engineering closure remain history within their checked durations.

The requested laws, controller, fixed apparatus identity and no-execution boundary leave no authorized correction in this task. No tolerance change, clock reset, timestamp rewriting, guard removal, nonzero-index fixture, restart workaround, route substitution or convenient shorter horizon is implemented. The 630-second proposal and its intended evidence remain reviewable.

**Required next decision:** a separate Jason ruling on narrowly scoped apparatus clock compatibility before producing a launch-ready authority. Any implemented correction would require its own bounded engineering scope, checks, new exact apparatus identity and newly bound launch object. This document proposes no particular patch and grants no engineering or simulation execution. Approval of this held review hash alone must not be treated as permission to ignore the hold or alter the pinned instrument.
