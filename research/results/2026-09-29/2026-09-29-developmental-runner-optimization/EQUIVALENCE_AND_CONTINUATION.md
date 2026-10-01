# Equivalence, reconstruction and continuation evidence

Release result: `COMPONENT_RELEASE.txt` — **14 passed in 29.81 seconds**. No scientific pass gate, learning/survival assessment, Founder start or new prehistory. The suite uses disclosed `loom_p.smokes.make_case` engineering fixtures. All comparisons are exact typed binary equality or `array_equal`, not loose numeric closeness. The only causal-state exclusion is duplicate observer cache `Engine.last_native`.

| Check | Result / scope |
|---|---|
| Old `Engine.step` versus new scheduler, nonzero neural fixture | Every Engine causal field, wave and event identical after each of 60 native steps. |
| Old versus new, contact fixture | Same every-step exact comparison, 60 native steps. |
| Energy terminal | Same exact partial terminal dt and all causal state. |
| Integrity/contact terminal | Same exact terminal result and all causal state. |
| Invalid-field rollback | Same failure and rolled-back causal state. |
| Binary state | Exact round-trip; bit corruption/truncation rejected. |
| Tier-2 full state and D5 | Every native state and original passive/D5 row exactly reconstructed for 60 saved steps, including fields. |
| Continuous versus save/load | Continuous 60 steps equals split at 7 → 20 → 60, preserving partial wave and exact final body/fields/P/RNG. |
| Total-age boundary tests | Manufactured clocks around 600 / 900 / 1,800 seconds: 14 native steps each; split at the named boundary versus continuous old scheduler. No claim these fixtures lived to those ages. |
| Stop/custody/error handling | Terminal continuation, mismatched state/parent, unauthorized science-kind grant and corrupted chunk rejected; storage pause at zero steps; injected I/O failure preserved separately from biology. |

Independent lifecycle timing check: old continuous endpoint equals old split at index 7; release lean split at 7 equals the same old continuous endpoint. No reset/rebirth/refill occurs. Exact final P hash in the matched pre-release comparison: `228602660301c4c58f8784b1a814251c5252e0fbdbd99bb274a0ec2d1a42bfe4`. `lifecycle-final.json` records release results and complete runtime identity.

The longer preserved fixture yielded 60,000 native records / 3,000 handoffs. Reconstructing P from all its saved actual inputs checked every one of 600 P/RNG chunk endpoints (47.7099 seconds, zero body/world trajectory steps). Selected last 20 steps plus nearest-checkpoint warm-up regenerated exact realized fields and complete final causal state. The 600-second original record was not re-run or replaced after the memory repair.

Continuation API uses absolute integer native deadlines. A later grant can extend 60,000 → 90,000 → 180,000 while retaining the exact prior checkpoint and receipt, same life identifier and store, full transients/learned structures/phase/RNG. World physical time continues in the unchanged accumulated-float representation; it is never rebased. These capability tests do not authorize such scientific continuations.

Development failures are preserved:

- The first pytest run could not use the global Windows temporary directory. A fresh explicit writable base directory resolved that environment issue.
- `STORE_TESTS_001.txt` exposed a reconstructed raw-container list/tuple mismatch. The baseline uses a tuple. This was corrected in the analysis codec projection and all exact tests then passed; no physical/P law changed.
- The 600-second benchmark exposed temporary encoding/decoding closure retention. With GC disabled in an isolated saved-record component, 100 old codec calls retained 100 `put`/`get` closures and 22,346,400 bytes of encoding parts. The correction retains zero closures/parts, with identical encoded SHA `05ff3d0d00f63b4affee37dd851e5922046860c942c577e0350302aadaf7989d`. A subsequent 30-second benchmark and 180,000-row saved-data scaling check validate stable memory. No longer trajectory was repeated.
- The profiler was refined to attribute neural helpers invoked by D5 to diagnostic context. Earlier raw profiles are preserved and marked superseded for attribution, not erased.

The final source additionally binds Python DLL/native runtime files at segment boundaries and avoids unnecessary deep copies during analysis warm-up. These changes are included in release tests and lifecycle/short benchmarks; the sole long benchmark is explicitly identified as the earlier lean source. Its exact source files and identities accompany the package.

Not tested: scientific founder births/populations, learning efficacy, selection, nursery, adversarial machine-owner tampering, cross-platform bit-exact replay, crash recovery after incomplete I/O, all possible pathological collider/solver states, or a full lived 1,800-second trajectory. Incomplete stores deliberately require review rather than automatic continuation.
