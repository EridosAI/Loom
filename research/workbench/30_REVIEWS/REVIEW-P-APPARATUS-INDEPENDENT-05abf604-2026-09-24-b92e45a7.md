# Independent apparatus review — exact 05abf604 checkpoint

**Registered:** 2026-09-24, at Jason's explicit instruction. This note records the supplied independent review; it does not rerun it.

Exact apparatus commit: `05abf60401d08f38750bca589b1c040e10513d7b`

Commissioning apparatus: **ENGINEERING HOLD**  
P implementation: **unchanged / previously verified**  
Commissioning execution: **NOT STARTED**

Blockers:

- **A1** — approval binding does not yet bind complete arm/controller/route.
- **A2** — stage clock comparison may permit one extra 0.1 s command hold.

All other reviewed apparatus findings retain their reviewed status.


The unchanged P baseline is `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Scientific status remains **UNCOMMISSIONED / UNTESTED**. The apparatus hold is not a P mechanism failure or a scientific result.

## Source and blocker identities

The [complete independent review](../90_SOURCES/p_independent_apparatus_review_2026-09-24_b92e45a7/LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md) and [receipt](../90_SOURCES/p_independent_apparatus_review_2026-09-24_b92e45a7/REVIEW_RECEIPT.json) give the source disposition **HOLD BEFORE COUPLING COMMISSIONING**. Jason's requested live label is **ENGINEERING HOLD** for the commissioning apparatus. A1 corresponds to the review's **A-R1**; A2 corresponds to **A-R2**. Original source IDs and text are preserved. These blocker aliases are distinct from the physical-ceiling A1–A5 case labels and P's historical R1–R3 findings.

| Blocker | Scope of independently reported defect | Reviewed closure requirement; not authority to repair |
|---|---|---|
| A1 / A-R1 | A valid but unapproved arm/controller can pass the same grant; prescribed route is outside the bound manifest and can change commands without changing that manifest | Bind the complete immutable execution contract, including arm/controller/route/settings and relevant identities, before output; preserve across restart; add rejection controls |
| A2 / A-R2 | At the nominal 0.1 s decision boundary, accumulated time can be `0.09999999999999999`; the route deadline then misses stage advancement or final stop and permits another ten native steps | Use a numerically faithful due-time comparison; test the exact accumulated boundary, final-entry stop and a clearly-not-due control |

The report locates these in the apparatus approval/controller paths. It keeps the reviewed native scheduler, command-hold/restart mechanisms and other controls verified within their tested scope, with these explicit exceptions. Passing component suites does not close the two uncovered defects.

## All source dispositions retained

The following is the independent report's concise closure table, reproduced without changing classifications. Source finding IDs are intentionally retained.

| Area | Classification | Independent result / required closure |
|---|---|---|
| A-R1: execution approval binding | **MUST-FIX BEFORE COMMISSIONING** | Same request bytes/grant accept four substituted arm/controller combinations. Different routes share one manifest but produce different commands. Bind approval to the complete immutable execution contract, including route/controller settings; reject mismatches before output. |
| A-R2: prescribed controller deadlines | **MUST-FIX BEFORE COMMISSIONING** | Native step 10 ends at `0.09999999999999999`; an `until=.1` transition is missed and the old stage commands another ten steps. Make due-time comparison robust to native-clock rounding and add the exact regression. |
| P/configuration/prior engineering tests | **VERIFIED** | No P or configuration edit; all previous 59 checks remain unchanged and green. |
| Extended runner, native/wave/noise/field timing | **VERIFIED** | Original `Engine.step` for intact P; explicit deadline; manufactured above-30-second and 1,200-second endpoint checks; no long life executed. |
| Pause/restart and command holds | **VERIFIED** | Pause at step 7 preserves three remaining hold steps; resumed and continuous final states match; terminal/cutoff/incomplete failure resume rejected. |
| Privileged controller capability boundary | **VERIFIED** | Copied closed inputs, deterministic bounded two-command output, no world mutation or P input contamination. Approval binding and deadline exceptions are A-R1/A-R2. |
| Sensor-only interface | **VERIFIED** | 10/4/8/7 raw coordinates, held actual E/I, own history; no privileged routes/payloads; inspection is inert; privileged exceptions concealed. |
| Fixed-structure adapter | **VERIFIED** | Exact frozen list and restoration order; per-field poison causes no subsequent causal/RNG difference; late bank restoration fails consequentially. |
| AV/CO/SO firewall | **VERIFIED** | SO and dishonest SO relabelling rejected; AV/CO yields a Jason review request only; deliberate removal of SO guard reaches the independent breach assertion. |
| D5 and aligned records | **VERIFIED** | Fixed index/every-handoff selection; independent nonzero receiver equations and omissions; no live state/RNG changes; input/end timestamps distinguished. |
| Saved three-mode reconstruction | **VERIFIED** | All nine saved segments reconstruct; 120 native records including pause/continuous duplicates, 60 distinct continuous-path native records; final neural/field states exact. |
| Worktree / portable suites | **VERIFIED** | `83 passed in 34.04s` / `83 passed in 33.46s`. |
| Delivered RED→GREEN matrix | **VERIFIED** | All 16 intended REDs and 16 clean controls independently reproduced. |
| Prehistory / roster | **VERIFIED** | Life-0 cache rejects births 1–4; roster preserved unstarted; no cache preparation. |
| Package, sources, historical artifacts | **VERIFIED** | Original ZIP located in user-supplied Workbench inbox; all 220 payload identities match; 792 prior artifacts preserved; exact ancestry and historical tree checked. |
| Long-run performance / finite coverage | **LIMITATION / EXPECTED PROVISIONAL CHOICE** | 37.7447 h / 43.0187 GB are short-fixture extrapolations only; no long-run calibration. |
| Navigation, positive controls, survival, learning | **SCIENTIFIC / COMMISSIONING QUESTION, NOT AN APPARATUS DEFECT** | Unexecuted and not used as acceptance criteria. |
| Later execution and freeze decisions | **UNRESOLVED / REQUIRES JASON** | No Stage-1 case selected; execution and eventual coupling freeze remain separate decisions after apparatus closure. |

## Evidence attribution and preservation

The independent reviewer reports both 83-test suites passing, all 16 delivered fault/control pairs reproduced, an additional consequential SO-firewall pair, fixed-state/receiver checks and exact saved-record reconstruction. It reports 792 prior artifacts preserved and no target modification or commissioning execution. Those are **the reviewer's findings**, not new results from this intake. This intake read the complete main review and verified archive custody; it executed none of the included commands, probes, tests, launchers or replays.

The [original builder intake](REVIEW-P-APPARATUS-05abf604-2026-09-24-73c9ad61.md) remains unchanged as the earlier awaiting-review record. The current independent disposition supersedes that pending review state for this exact apparatus checkpoint. The independently verified P baseline and the d5f7efbe/f7eb6f27 engineering-history branches retain their own dispositions. Candidate documents, all alternative families, earlier decisions and original sources are unchanged.

The review's proposed corrections and reruns are future work requiring their own authority. This registration does not begin commissioning, select Stage 1, authorize fixes, revise P, change configuration or freeze an evidential coupling. The synthetic authority file inside the ZIP is manufactured probe data and is explicitly **not Jason authorization**.

[Source identities](../50_SESSIONS/2026-09-24-p-independent-apparatus-intake-b92e45a7/SOURCE_IDENTITIES.json) · [Intake completion and validation](../50_SESSIONS/2026-09-24-p-independent-apparatus-intake-b92e45a7/INTAKE_RECORD.md) · [Original review ZIP](../90_SOURCES/p_independent_apparatus_review_2026-09-24_b92e45a7/Loom_P_Independent_Apparatus_Review_05abf604_20260924.zip).
