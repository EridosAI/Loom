# Static 630-second scheduler compatibility

**PASS — scalar preflight only; A5 remains unexecuted.**

All 63,001 native-index positions (including the initial endpoint) pass physical/index consistency. All 6,300 prospective ten-step holds fit their stage and case boundaries. The independent integer interval oracle agrees at every position. Stage ends are 9,000 / 12,000 / 27,000 / 30,000 / 45,000 / 48,000 / 63,000. The final index admits no fresh hold.

The scalar clock repeatedly adds 0.01 without rounding, resetting or evolving state. Calls are restricted to the corrected pure clock helpers and stage selector. No waypoint command or world-dependent input is calculated. The complete hold table is `STATIC_HOLD_SCHEDULE.csv`; all boundary samples are in the JSON companion.

| Index | Accumulated scalar time | Nominal time | Stage (zero-based) | Clock allowance | Fresh hold |
|---:|---:|---:|---:|---:|---|
| 26949 | 269.4899999998999 | 269.49 | 2 | 9.064116052721424e-10 | False |
| 26950 | 269.4999999998999 | 269.5 | 2 | 9.06471445182947e-10 | True |
| 26951 | 269.5099999998999 | 269.51 | 2 | 9.065312873141976e-10 | False |
| 26999 | 269.98999999989945 | 269.99 | 2 | 9.094063208587799e-10 | False |
| 27000 | 269.99999999989944 | 270.0 | 3 | 9.094662717918868e-10 | True |
| 27001 | 270.00999999989943 | 270.01 | 3 | 9.095262249454399e-10 | False |
| 30000 | 299.99999999987216 | 300.0 | 4 | 1.0993144090036905e-09 | True |
| 45000 | 449.99999999973573 | 450.0 | 5 | 2.3483153117148956e-09 | True |
| 48000 | 479.99999999970845 | 480.0 | 6 | 2.658067535587714e-09 | True |
| 63000 | 629.9999999995721 | 630.0 | 6 | 4.50670255844351e-09 | False |

At index 26,950 the legitimate accumulated timestamp differs from 269.5 by more than the old fixed 1e-10 threshold, but passes the corrected summation-error bound. At index 27,000 the stage selector owns stage 3 despite the slightly lower physical timestamp; the ten-step hold ends at 27,010, below the next stage end of 30,000. Neither former rejection occurs in the static scheduling predicates.

The maximum absolute scalar accumulation discrepancy is 4.2791725718416274e-10 s. At 63,000 the physical/index allowance is 4.50670255844351e-09 s. It diagnoses clock consistency and never selects a stage. Native 0.01 s, command 10-step, wave 20-step and field cadences remain defined by unchanged code/configuration. No actual field, wave, event or pause/resume operation is tested here; those component/regression results belong to the sealed prior correction review.

Scope limit: this proves declarative/native scheduling compatibility for the preserved A5 manifest. It does not prove contact success, renewal use, viability, complete-case runtime, or any physical outcome. Future live startup must still perform the normal identity/cache/state checks after separate authorization.
