# Independent suite and 36-pair log audit

No test bodies were rerun. This audit read all 72 saved RED/GREEN logs and performed one collect-only invocation in the pinned environment.

| Group | Pairs | Reached RED result | Clean GREEN result |
|---|---:|---|---|
| Previous apparatus | 16 | 16 intended exception failures | 16 passed |
| New authority | 18 | 18 intended APPROVAL BINDING BREACH assertions | 18 passed |
| Clock transition | 1 | 2 failed, 3 passed parameter cases | 5 passed |
| Clock final stop | 1 | 1 intended CLOCK BREACH failure | 1 passed |

The 18 authority RED cases replace only the test callback with `lambda: None` at `test_corrections.py:82`, then fail its assertion at line 83. They do not patch production `verify_approval_binding`. Their GREEN cases call the actual verifier and constructor rejection checks. The two clock cases do replace the production module comparison in memory. These qualifications prevent treating all 20 new pairs as equivalent production mutations.

Clock-transition RED failures are the two parametrized occurrences of the same below-boundary floating value `0.09999999999999999`; exact/above cases pass under the old comparator. The corrected GREEN runs all five parameter cases successfully.

| Collected group | Cases |
|---|---:|
| Unchanged P engineering | 59 |
| Previous apparatus | 24 |
| New correction | 30 |
| Total | 113 |

Saved complete-suite logs independently contain `113 passed in 77.05s (0:01:17)` for the worktree and `113 passed in 60.96s (0:01:00)` for the portable package. Collection does not itself establish passing execution.

Every JSON pair entry includes the actual reached `E ...` exception line, traceback file/line, RED/GREEN summaries, recorded exits and both log hashes. An intended string appearing only in quoted source was insufficient.

| Fault | Actual RED exception | GREEN count |
|---|---|---:|
| identity | ValueError: manifest/code identity mismatch | 1 |
| missing_native | ValueError: missing native record | 1 |
| phase | ValueError: wrong field/mover phase | 1 |
| ledger | ValueError: source debit/body credit mismatch | 1 |
| input | ValueError: forbidden controller input | 1 |
| observer | ValueError: observer RNG/state interference | 1 |
| stop | ValueError: mislabelled stop reason | 1 |
| sensor_leak | ValueError: privileged data leakage into sensor-only interface | 1 |
| label | ValueError: external controller incorrectly labelled intact P | 1 |
| frozen | ValueError: frozen structural parameter changed | 1 |
| discarded | AssertionError: discarded structural update affected later output/state | 1 |
| duration | ValueError: manifest changed during run | 1 |
| extra_updates | AssertionError: extra native/wave/random/field updates introduced by controller hold | 1 |
| extra_native | AssertionError: extra native/wave/random state change from external hold | 1 |
| extra_wave | AssertionError: extra native/wave/random state change from external hold | 1 |
| extra_random | AssertionError: extra native/wave/random state change from external hold | 1 |
| authority-implementation | AssertionError: APPROVAL BINDING BREACH: implementation | 1 |
| authority-constants | AssertionError: APPROVAL BINDING BREACH: constants | 1 |
| authority-route | AssertionError: APPROVAL BINDING BREACH: route | 1 |
| authority-stage_sequence | AssertionError: APPROVAL BINDING BREACH: stage_sequence | 1 |
| authority-contact_target | AssertionError: APPROVAL BINDING BREACH: contact_target | 1 |
| authority-manual_fallback | AssertionError: APPROVAL BINDING BREACH: manual_fallback | 1 |
| authority-sensor_interface | AssertionError: APPROVAL BINDING BREACH: sensor_interface | 1 |
| authority-intact_arm | AssertionError: APPROVAL BINDING BREACH: intact_arm | 1 |
| authority-fixed_adapter | AssertionError: APPROVAL BINDING BREACH: fixed_adapter | 1 |
| authority-deprivation | AssertionError: APPROVAL BINDING BREACH: deprivation | 1 |
| authority-initial | AssertionError: APPROVAL BINDING BREACH: initial | 1 |
| authority-prehistory | AssertionError: APPROVAL BINDING BREACH: prehistory | 1 |
| authority-duration | AssertionError: APPROVAL BINDING BREACH: duration | 1 |
| authority-resources | AssertionError: APPROVAL BINDING BREACH: resources | 1 |
| authority-runtime | AssertionError: APPROVAL BINDING BREACH: runtime | 1 |
| authority-procedure | AssertionError: APPROVAL BINDING BREACH: procedure | 1 |
| authority-replay_arm | AssertionError: APPROVAL BINDING BREACH: replay_arm | 1 |
| authority-request_rebind | AssertionError: APPROVAL BINDING BREACH: request_rebind | 1 |
| clock-transition | AssertionError: CLOCK BREACH: expired stage issued another hold | 5 |
| clock-final | AssertionError: CLOCK BREACH: final stage still drives | 1 |
