# Loom positive-control execution review — 27 September 2026

All four disclosed controls have ended. Jason chose every submitted motor command. PC-HOLD established a real gentle hold for **0.8 simulated seconds**, shorter than its predeclared continuous **1.0 s** target. The four-control admission gate is **not satisfied**. Neither B1 trial was executed, and no sealed B1 evaluator or starting-state material was inspected or included here.

This is a record of guided human interface practice. It is not a test of P learning, an internal world model, navigation competence or ecological viability.

## Results and stopping conditions

| Control / attempt | Simulated time | Human commands | Stop | Disposition |
|---|---:|---:|---|---|
| PC-LR / 001 | 0 s | 0 | Administrative wall cap after connection loss | No physical execution; original attempt preserved |
| PC-LR / 002 | 0 s | 0 | Jason ended case | DEMONSTRATED with disclosed channel-pair guidance; separately authorized fresh attempt |
| PC-MOTION | 0.2 s | 2 | Administrative wall cap | DEMONSTRATED WITH EXPLICIT GUIDANCE; final interpretation after closure |
| PC-CONTACT | 2.3 s | 23 | Jason ended case | PARTIAL / not marked fully demonstrated; approximate onset detected, support interpretation initially mistaken |
| PC-HOLD | 3.9 s | 39 | Jason ended case | NOT DEMONSTRATED against the full 1.0 s criterion; shorter gentle hold verified |

The total is 640 native steps and 64 human commands across five preserved case preparations, including the separately authorized PC-LR replacement. No other retry, fixture substitution, tuning or extension occurred. The unchanged interface ended wall-limited cases at its next check; their reported wall times were 1222.682 s (PC-LR/001, approximate) and 1241.425 s (PC-MOTION). Neither advanced during the excess wall time. All local control services have been stopped after their cases closed.

## What PC-HOLD actually established

The first impact occurred at **0.233656229 s**. From **0.300 to 1.100 s**, the body had continuous positive-duration wall support. Recorded contact force ranged from **0.037666121 to 0.150862270**, strictly below the unchanged **0.25** stress threshold, with **zero sustained stress damage during that interval**. Thus Jason's interpretation of reducing effort and maintaining a lower contact signal was supported by the completed physical record.

At 1.1 s the command pair changed from `[0.05, 0.05]` to `[1, -1]` as Jason explored. The gentle interval ended. A later qualifying interval lasted **0.282791256 s**, from **2.927208744 to 3.210 s**. Separate intervals cannot be added to satisfy a continuous one-second target. The earlier screenshot showed 0.6 s at the lowest command pair; the physical review finds 0.8 s of qualifying gentle support because the preceding 0.2 and 0.1 pairs were also below the threshold. There is no contradiction between those two durations.

All impacts and later exploration remain in the record: three impact events; total impact damage **0.003453380**, sustained stress damage **0.002796736**, and total damage **0.006250117**. Expenditure was **0.009010**. E/I changed from **0.700000 / 1.000000** to **0.690990 / 0.993750**. Initial impact damage is retained separately and does not invalidate a subsequent gentle interval.

Evaluation used closed event records only: positive impulse over positive duration, actual force equal to impulse/duration, every active contact strictly below the original threshold, and no sustained stress damage. Contiguous event intervals were joined only within the existing `event_time_tol = 1e-10`; no relaxed force threshold or new efficacy criterion was introduced. The force and stress-damage arithmetic and all recorded artifact hashes/lengths were verified.

## Earlier controls and guidance

PC-LR/002: Jason reported “Chemistry 0 is bigger.” The displayed same-type pair was chemistry 0 = 0.5885631339300567 and chemistry 2 = 0.5777453792391184. The assistant identified the pair and anatomy beforehand; Jason supplied the comparison sign. No command or world step was needed. The original zero-step connection-loss attempt is preserved alongside the specifically authorized replacement.

PC-MOTION: Jason distinguished commanded input from achieved forward motion and identified the discrepancy channels as a mismatch. His initial turning-sign error was explicitly corrected. The final interpretation arrived after the wall cutoff using the retained 0.2 s observation. This supports guided understanding, not independent mastery of all signs or an unassisted result.

PC-CONTACT: the actual first impact was at 0.898417740 s; the first native contact sample was 0.900 s. Positive-duration support then persisted to 2.3 s. Jason noticed approximate onset but initially interpreted the later trace as another impact or rough ground. The post-case passive plan-view replay showed sustained wall contact. His uncertainty and later learning remain separate from the original response; this result has not been retroactively upgraded. The replay exposure occurred before PC-HOLD and is recorded as practice feedback.

Jason reported difficulty following what was happening across steps, while still making inferences from the displayed signals. His suggestion that this could support an internal world model is recorded as an operator hypothesis. The interface exposes recorded history, but access to that history did not make it easy for him to follow the motion. No interface change was made during these controls.

## Integrity, limits and next boundary

Jason's prior-B1-exposure answer was **“No”**, preserved as a self-report, not an independently established fact. Disclosed practice geometry, general sensor explanations, the PC-CONTACT post-case replay and the PC-HOLD public timing clarification are retained in the record. The assistant supplied no actuator commands and no live privileged physical-force guidance. Historical preparation records still describe their then-current statuses; this report and `FINAL_RECORD_AUDIT.json` describe the completed sequence.

The gate in the accepted `CONTROL_GATE.json` requires all four controls explicitly demonstrated and separate B1 authorization. PC-CONTACT remains partial and PC-HOLD did not obtain its full duration criterion. No B1 admission is implied by finishing these attempts. Any additional familiarization, retry, interface revision or B1 execution needs a separately scoped decision. No further run is launched.

Not tested: either blinded B1 condition, P learning or perception, formation of an internal world model, survival, commissioning efficacy, alternative routes or control policies. No production code, configuration, authority object, physical law or preserved historical source was changed. No Git write, push, PR or merge occurred.

## Exact identities and evidence

P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`

Apparatus: `352f73fffa6d9781eae8aa38e708a9a05669588f`

Worktree: `C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\worktrees\loom-p-b1-apparatus-correction-20260926`

Branch: `build/p-b1-operator-correction-20260926-01a0c405` (clean at review; no new commit)

| Control | Authorized execution SHA-256 |
|---|---|
| PC-LR | `a80a9098b7eed714f824eccd841d17e29e94cc607489ddf7a5390f1dc38c493a` |
| PC-MOTION | `c35d7a469da2598a0bcb0abc9b952592fc5310525fac2f3e1f5edf0461bf401c` |
| PC-CONTACT | `2e9989e37863c32ae89fd559adf51942bd8152b8d5244a8de1baf2234c52ba1d` |
| PC-HOLD | `ac1c5615c2c99ebe2524e3648b81003d7eeb42f1b54493212afd8d3cb83d719f` |

`FINAL_RECORD_AUDIT.json` binds the five runtime receipts and checks their source identities against the unchanged worktree. The portable review archive includes the complete closed PC run records, exact PC requests/manifests/inputs, operator observations, control results and the accepted public control/gate documents. Only these positive-control files were selected; no B1 evaluator archive is present. `REVIEW_FILE_MANIFEST.json` records every archived file hash and size. All analysis was passive; no Engine, Run, controller or world was invoked during this review.
