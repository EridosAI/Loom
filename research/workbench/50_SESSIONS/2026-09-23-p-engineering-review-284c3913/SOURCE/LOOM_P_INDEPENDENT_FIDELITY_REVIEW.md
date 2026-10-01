---
id: REVIEW-P-ENGINEERING-2026-09-23-D5F7EFBE
revision: v1.0
authority_status: independent-review-not-jason-decision
work_status: complete-exported-for-workbench-intake
evidence_status: source-and-code-audit-with-deterministic-component-and-record-checks
reviewed_commit: d5f7efbe67193f215e52d95ca912db131a79f31c
commissioning_disposition: hold-for-engineering-corrections-and-reverification
---

# Independent fidelity review of Loom P

**This exact checkpoint is not fit to proceed to coupling commissioning.** A reproduced contact-scheduling defect suppresses a real release/recontact interval and accounts the whole native step as sustained source contact. The delivered component suite also fails on independent execution, and several important passing tests do not reject the faults they claim to cover. These are engineering findings. They do not establish that P is scientifically unsuccessful, or justify changing its mechanism or tuning its parameters.

The retained neural equations and handoff sequence are faithful on independent inspection. Separate bodily teaching, actual/evoked separation, configurable sensory anatomy, the temporal packet path, deliberately contracting association, and the selected illumination ruling are preserved. All 3,200 saved final neural states and all three final chemical fields reproduce exactly from the recorded inputs. Reproducible execution can still reproduce an incorrect physical operation; those two conclusions are compatible.

## Identity, authority and review method

Reviewed worktree: `C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405`.

Reviewed branch: `build/p-engineering-baseline-20260921-01a0c405`.

Reviewed commit: `d5f7efbe67193f215e52d95ca912db131a79f31c`.

Configuration: `p_engineering_baseline_v0_1`, semantic SHA-256 `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`, with `illumination_boundary="open"`.

Runtime-module identity: `cf17d3248c463d9f2d00921b991ce433bb49956476fe02027c3d7ce062bf7456`.

Portable package: `developmental_ecology/artifacts/review-package-20260922-01a0c405/Loom_P_build_review_20260922.zip`, SHA-256 `a376ad876a164e96cc0b0b1f4f9d250fc8bb70bc4b585bca24092fdee3ada57f`.

This is an independent review, consolidated by the primary reviewer from direct inspection and three parallel read-only reviews of neural fidelity, physical timing, and provenance/observer isolation. The engineering:code-review skill supplied the review structure; the user's requested classifications and fidelity scope control the conclusions. Highest available reasoning was requested; the backend effort setting is not independently measurable here and is not asserted as evidence of correctness.

The current-state orientation was read first. The review then used the complete portable package inventory, its code/tests/build documentation and relevant saved evidence, the exact P parent, implementation/observation specification, plain-language walkthrough, specification handoff, design review, engineering handoff, and accepted world/body reference set. Package entries and local evidence were hash-checked; compressed records were inspected computationally rather than represented as individually human-read lines. The full historical conversation archive was not re-audited.

Source authority remains separate:

- **Jason-accepted decisions:** D1–D3 as recorded in `LOOM_P_SPECIFICATION_HANDOFF_2026-09-20.md`; bounded construction authority in `LOOM_P_ENGINEERING_BUILD_HANDOFF_2026-09-21.md`; and the transcribed 2026-09-22 illumination ruling in `JASON_RULING_2026-09-22.md`.
- **Construction target:** the exact P equations and the numerical/engineering completions selected for this first build. The source documents' historical proposal/no-build headers have not been rewritten.
- **Experimental evidence:** the preserved bounded engineering cases, deterministic checks and this review's component/reconstruction results. They supply no developmental-success finding.
- **Reviewer judgments:** the findings and commissioning hold below. They are not amendments to canon or newly accepted experimental instructions.

No code, configuration, source documentation, Git state, existing artifact, or Workbench file was modified. No fix, branch integration, commit, push, new complete-loop organism execution, prehistory execution, lifetime, commissioning run or parameter sweep was performed. Existing tests wrote only their isolated temporary fixtures outside the reviewed worktree; bytecode and pytest cache writes were disabled. Additional probes were in-memory component arithmetic, existing-test falsifiers, and detached arithmetic on already saved records. This new review export is outside the Workbench for later intake.

Code references below use `D/` for the absolute worktree path above plus `/developmental_ecology/`, and `B/` for that worktree plus `/docs/developmental_ecology/p_engineering_20260921/`. Line numbers refer to this exact checkpoint. Source references use exact basenames and section numbers so they remain identifiable after Workbench intake.

## Findings requiring correction before commissioning

### R1 — A touching but separating source contact is incorrectly retained for the whole step

**Classification: MUST-FIX BEFORE COMMISSIONING.** This changes physical energy and integrity consequences; it is not a weak-signal or learning-adequacy issue.

`D/loom_p/physics.py:124–144` marks a fixture active from its current gap alone and excludes every such fixture from the swept collision search. An active contact may already have an outward, separating velocity. If force reverses that motion within the native step, the implementation never schedules its release and recontact. Instead, `physics.py:153–170` projects the ending free velocity against the original contact and supplies that contact to `account` for the entire interval. `physics.py:63–80` then computes sustained force, exchange and stress from that full duration.

A single deterministic physical component reproduces the fault using the unchanged baseline configuration:

- Body centre `[2,3]`, touching the left side of source 0; orientation 0; energy 0.7; integrity 1; initial velocity `[-0.001,0]`; held command `[1,1]`; native duration 0.01 s.
- Under the implementation's own declared free-motion path, `p(t)=p0+t*v(t)` (`physics.py:90–102`), the body initially separates. It returns at `0.001314924581309022` s. At half that time the positive gap is `3.2862308119163686e-07` body diameters, over 3,000 times the configured geometry tolerance `1e-10`.
- Actual `advance` output is one event: duration `0.01`, `impact=False`, source-0 impulse `0.006572076516883112`, source transfer `0.00010415229960600089`, damage `0.00008144153033766224` approximately, and ending position `[2,3]`. It records neither a free interval nor a recontact impact.

The defect is the omitted release and recontact and the resulting full-interval accounting. This review does not substitute a new continuous-time integrator or claim a corrected numerical transfer value. The counterexample uses the same free-path convention as the existing solver, so it does not depend on rejecting the source's chosen finite-step mechanics.

The controlling requirements are `P_IMPLEMENTATION_AND_OBSERVATION_SPEC_v0_1_REVIEW_DRAFT.md` §§7.2 and 8.2: resolve swept impacts/subintervals, separate zero-duration impacts from positive-duration contact, and do not manufacture transfer/repair by spreading an impact across free flight. Engineering handoff §7.1 item 5 explicitly requires those distinctions. Accepted `BASE_WORLD_COMPLETION_v0_1.md` §§6–8 requires real transfer and bodily consequence, with constitutive values left to the later specification.

Existing tests miss this case. `D/tests/test_physical.py:88–96` begins detached and incoming. `D/tests/test_boundary_and_scheduler.py:88–93` begins already separated and continues away. Direct `account` tests assume that the supplied contact duration is correct. Neither setup tests touching → separation → recontact inside one step.

**Required closure:** correct active-contact event handling and add a deterministic regression that rejects full-step sustained accounting for this release/recontact case. Reverify affected mechanics/accounting and coupled timing under separately authorized corrective work. Preserve this checkpoint and its evidence. No correction was made during this review.

### R2 — The final delivered test suite is not reproducibly green

**Classification: MUST-FIX BEFORE COMMISSIONING.** This is a verification defect; no normal live-inspector timestamp defect was demonstrated.

Independent execution of the existing suite produced **43 passed, 1 failed** in 3.73 s. Failure: `D/tests/test_records.py:76–81`, `test_live_handoff_observation_has_physical_timestamp`:

```text
assert result['wave']['time']==.2 and state_hash(e)==before
E assert (0.20000000000000004 == 0.2)
1 failed, 43 passed in 3.73s
```

`Inspector()` loads the completed saved contact replay and its five waves (`D/loom_p/inspector.py:20–35`). The test replaces `engine` and clears `replay` but leaves `waves` populated. `inspector.py:46–48` selects an eligible saved wave, with timestamp `0.20000000000000004`, instead of the manufactured live wave at exactly `0.2`. Clearing `app.waves` in memory makes the intended assertion pass. Normal explicit stepping already clears both histories at `inspector.py:79`; therefore a live-path defect must not be inferred solely from this test failure.

The preserved `component-attempt-006.txt` really records 44 passes. Its file timestamp precedes the completed attempt-002 contact manifest; that supports, but does not prove, the explanation that the final saved replay did not exist when the test passed. The issue is that the test depends on ambient artifacts and the final assembled delivery was not validated in its delivered state. It is not evidence that the old log was fabricated.

**Required closure:** isolate the test from ambient saved replay, verify its intended branch, and produce a new final-checkpoint verification record after all packaged fixtures exist. Merely loosening the floating-point comparison would hide the stale-wave selection and would not address this finding.

### R3 — Important passing tests accept disabled operations or never reach their falsifier

**Classification: MUST-FIX BEFORE COMMISSIONING, for the claimed verification contract.** The current inspected neural formulas and terminal guard are correct; the defects below concern evidence strength.

| Claimed protection | Actual falsifier weakness | Consequence |
|---|---|---|
| New-value bank reference following | `D/tests/test_neural.py:194–202` passes when `Regulator.credit` performs its real calculation and then restores the old reference. Default `np.allclose` relative tolerance accepts the roughly `8e-6` movement from a value near 0.8. | Passing this test does not establish equation 21's reference update. |
| Old-value sensory reference following | `D/tests/test_neural.py:33–49` passes when `Cortex.step` restores both old references after the calculation. The shared-reference movement is about `1e-9`, below its relative tolerance; fine-reference following is not asserted. | Passing this test does not establish these slow but retained operations. |
| No handoff on a terminal partial step | `D/tests/test_boundary_and_scheduler.py:41–60` begins at native index 50 and ends at 51. Its failing handoff callback cannot run even if the terminal exclusion is removed, because 51 is not divisible by 20. An in-memory mutant changing the production `elif` at `engine.py:98` to an independent `if` still passes this exact existing test. | The branch intended to reject an invented terminal handoff is unreachable. Rollback and one retained draw are tested; handoff suppression at a scheduled wave boundary is not. |
| Organism footprint changes field diffusion | `D/tests/test_physical.py:18–30` compares coefficients at different times while also inserting a body. Mover displacement alone can make the asserted difference nonzero. | This assertion cannot isolate the body's diffusion footprint. Source inspection confirms the present implementation adds it at `chemistry.py:18`. |
| Information allowlist / evoked reserve ownership | `test_neural.py:120` checks a string declaration, and `test_physical.py:74–78` supplies no evoked content at all. | These are not adversarial data-flow or evoked-reserve injection tests. The positive boundary finding in this review instead rests on tracing the actual call and write paths. |

The first three weaknesses were exercised with in-memory mutants against existing tests, without changing source files. The last two follow directly from the tested operands and assertions. The actual reference operations remain at `neural.py:62–63,162`, and the terminal exclusion remains at `engine.py:96–99`.

**Required closure:** make the reference oracles reject no-ops, exercise the terminal case where the native counter would otherwise trigger a handoff, and make isolated component/boundary checks match the claims made for them. This does not require a new scientific lifetime, efficacy gate or mechanism redesign. A 44-pass count alone does not close R1–R3.

## Independent equation-to-code trace

**Classification for every row below: VERIFIED for the selected equal-valued baseline.** This table was derived from the executing code and source equations, rather than accepted from the builder's map. Verification weaknesses remain separately identified above.

| P operation | Executing code | Independent fidelity result |
|---|---|---|
| 1 — sensory activity | `D/loom_p/neural.py:42–68` | Residual uses old receptor mean; activity uses old reconstructed W, old x and fixed A; exponential Euler is the specified discretization. |
| 2 — packet | `neural.py:68–73,196,222–223` | Sensory trapezoidal mean plus endpoint; motor piecewise-constant delivered-command mean plus endpoint; only integrals turn over. Actual reserve endpoints and held applied regulation occupy their declared blocks. |
| 3 — local formation | `neural.py:46–48,67` | Old x/r/W/C; diagonal competition excluded; no q or bodily score in F. |
| 4 — centring/context | `neural.py:90–95,138` | Old means subtracted once; trace follows beta; psi is beta then trace; means update after read/write processing. |
| 5 — context gates | `neural.py:96–102` | Target block excluded; other-channel ungated actual psi enters fixed signed anatomy; positive branch coefficients normalize to one. |
| 6 — association write | `neural.py:126–133,228` | Actual psi outer product, target gate, physical wave-duration scaling, old-map decay, per-map Frobenius projection, once per real wave. |
| 7 — map use/preservation | `neural.py:123,129–137` | Final old-map contribution supplies use drive; old use sets current decay; new use influences later decay. No positive extra occurrence write. |
| 8 — sensory participation | `neural.py:110–117` | Group gain `0.1+0.9*h` repeats across mean, endpoint and both trace blocks; other channels retain unit gain. |
| 9 — associative relaxation | `neural.py:118–124` | Persistent a, four simultaneous sweeps, linked alpha/Delta/S/tau, fixed old maps and gates, final q without fifth activity update. |
| 10 — regulator features | `neural.py:164–166` | Full q plus actual separate reserves plus fixed bias, tanh and constant. No additional direct scene input. |
| 11 — trial responses | `neural.py:167–169` | Distinct bank sign streams drawn once after credit; learned and exploratory terms are explicit. |
| 12 — need gains | `neural.py:170–171` | Each actual reserve supplies its own need gain, with the specified positive floor. |
| 13 — support | `neural.py:172` | Separate need-weighted bank logits add before logistic support. |
| 14 — current/attenuation | `neural.py:173–174` | Per-bank tanh current contributions and summed attenuation logits follow the specified anatomy. |
| 15 — shared/fine formation and references | `neural.py:48–63`; `10–21` | Group-mean local pressure, centred differential pressure, distinct reference attraction; tangent and finite-step projections; sensory references follow old parameters. |
| 16 — opening/support spring | `neural.py:53,57,64` | Same group support reduces the reclaim spring; private opening follows its exponential law. No content-writing target is introduced. |
| 17 — spontaneous motor source | `neural.py:179–195` | Old phase/noise generates tendency; phase advances analytically; held noise follows its filter with scheduled refresh. |
| 18 — motor enactment | `neural.py:187–197` | Raw proprioception/contact, centered endpoint motor q coordinates 2:4, current and oscillator enter leaky tanh tendency; attenuation then creates delivered command. |
| 19 — bodily trend/filter | `neural.py:152–155` | Actual current reserve versus its own old low-pass reading; no event labels or evoked reserve substitution. |
| 20 — eligibility | `neural.py:153–156,225–227` | Previous applied xi and phi enter the trace before new perturbations exist. |
| 21 — separate bank change | `neural.py:157–163` | Each trend multiplies only its own eligibility bank; separate parameter/reference arrays; row bound; bank reference follows newly projected value. |

The native receptor-mean and coactivity filters, initialization and parameter projections are also retained, although they do not each have their own parent equation number. `schema.py:146–171` implements deterministic indexed sign/anatomy draws and endpoint-safe uniform conversion. `neural.py:202–207` creates zero H/a/Theta/Z, actual initial means and first applied variation without a fictional completed wave.

## Timing, information boundaries and actual versus evoked state

**VERIFIED — neural handoff ordering.** `D/loom_p/neural.py:218–230` executes completed actual packets/context → previous bodily credit → old-map/old-support read → new features/draws/controls → one map write/use/mean update. New h begins affecting fine retention in the ensuing native interval; its query effect waits until the next handoff. Query-mediated bodily consequences then first enter the subsequent endpoint credit. No iteration adds a learning encounter, resets a, or advances an imagined world.

**VERIFIED — ordinary physical-time scheduling, subject to R1.** `engine.py:65–71,73–102` advances native sensory/motor state once, applies its delivered command to physics, advances fields at ending geometry/stock, obtains next transducers, then performs a complete-wave handoff if appropriate. Noise refresh uses the native scheduler, not contact subdivisions. The separation between native steps, waves and noise cadence is also checked against saved counters. R1 concerns the physical subinterval schedule inside this otherwise correctly ordered pipeline.

**VERIFIED with limited exercised scope — pause/resume and terminal handling.** Saved nonzero state includes references, eligibility, partial integrals, held controls, fields and counters. Exact nonzero snapshot restoration and the preserved 0.07 s mid-wave comparison are consistent with full-state serialization. `engine.py:75–93` restores the pre-step state for terminal-location trials and recomputes the shortened coupled step; `96–99` prevents terminal handoffs. No natural terminal complete-loop case exists in the evidence. The stand-in tests are not equivalent to one, and R3 narrows their claimed coverage. Physical terminal acceptance can differ from the requested shortened duration within the declared event tolerance; it is not evidence of unrestricted later evolution.

**VERIFIED — complete audited learner data path.** The live entry points are `Engine.__init__` at `engine.py:25–26`, `Engine._coupled` at `65–71`, and handoff at `99`. They supply actual receptor tuples, actual separate reserves, elapsed duration and scheduled noise refresh. `geometry.py:147–161` produces exactly 10 light, 4 chemical, 8 contact and 7 proprioceptive values. Association consumes packets/context; regulation consumes q and actual reserves; direct motor feedback consumes current raw proprioception/contact. No route from source identity, stock, pose, field grid, hidden class, observer replay or future state to neural arithmetic was found outside those transductions.

This is a code-level data-flow finding, not a security sandbox claim. Organism objects share a Config object containing world parameters and a Streams object containing labelled counters. The audit checked their actual reads: neural code does not read source positions/stocks/fixture identifiers or world draw counters. Per-label random hashing prevents a count of rejected birth positions from shifting motor/regulatory streams. Physiological opening, motor phase and noise clocks are the expressly supplied private dynamics; they are not appended time tokens. Geometry uses world time to generate the physical mover; the learner sees only its lawful consequences.

**VERIFIED — actual/evoked separation and separate bodily learning.** Physical reserve writes reside in `physics.py:55–81` and physical initialization; no physical API accepts q, psi, Theta or an internal energy/integrity estimate. Evoked reserve content can affect action through the declared regulator but cannot refill a reserve or replace the credit argument. Internal motor return must traverse `neural.py:190–193` and then `physics.py:46–53`. Applied controls and actual commands, rather than returned proposals, enter future packets. Internal evocations are not repeatedly written as external experience. The energy/integrity product in actuator capability is a supplied physical law, not a common teaching score. Output superposition likewise does not sum the two trend signals into a utility.

## Configuration, temporal retention and effective influence

**VERIFIED — width and pool parameterization.** `D/loom_p/schema.py:104–116,126–142` validates complete, nonduplicated, equal-size one-level memberships and derives group/output/packet/central/map dimensions. `neural.py:25–35,79–88,112–116,143–150,204–207` uses those shapes and memberships. The six-unit, three-interleaved-pool fixture at `tests/test_neural.py:11–20` meaningfully changes both width and support count. No structural dependency on eight sensory units or two pools was found. Fixed four sensory families, eight total channel families, two actuators and four specified sweeps/branches are different, explicitly specified restrictions.

**LIMITATION / EXPECTED PROVISIONAL CHOICE — bank parameter configurability has a source-contract gap.** Specification §10 says differently named constants remain separate configuration fields even when equal. `schema.py:52–59` instead exposes common scalars for bodily filtering, bank rate/reference, exploration and need floor, broadcast across E/I by `neural.py:154–174`. This reproduces the exact equal-valued baseline, and it does not combine teaching signals. It cannot express independently chosen bank values without a schema/code revision. Record this limitation explicitly; do not claim full independent bank-parameter configuration or silently vary such values during commissioning. It is not the reason for the present hold.

**VERIFIED — temporal path and retained native evidence.** The actual path is raw native readings → receptor means/residuals → x → trapezoidal mean plus endpoint → old-mean centring → five-second context → gates/query/write. No temporal signature, timestamp, inferred velocity or raw-sequence learner buffer is added. Body-relative velocity remains only the specified proprioceptive transduction.

All 3,200 final native rows retain the four raw vectors and old/new cortical activity. Each sensory diagnostic input matches the preceding boundary's raw input, starting from the initial snapshot. Independently summing `elapsed*(x_old+x_new)/2` across each interval, dividing by 0.2 and appending endpoint x reproduces every sensory packet in all **160** saved waves with **maximum error 0.0**. `engine.py:106–110` and `neural.py:49–69` retain these histories; `reconstruction.py:9–29` consumes their actual ordering. The endpoint `raw` field and the step-start sensory diagnostic `raw` are deliberately different moments, not a one-step loss.

**LIMITATION / EXPECTED PROVISIONAL CHOICE — representation losses.** Eight units/two groups, one-level pooling, the mean-plus-endpoint packet, fixed context anatomy, receptor/packet centring and finite traces are explicitly provisional in the engineering handoff §§3–4 and 9. The direct equal-mean/endpoint counterexample in `diagnostics.py:37–41` demonstrates compression loss, without claiming physical reachability. Frozen contact-history diagnostics preserve raw/activity/packet distinctions but are not an ecological learning result. Positive query gain cannot restore information erased upstream. None of this licenses importing R, a tonic bypass, a richer packet or a different learner.

**VERIFIED — fading association.** Each map has Frobenius radius 0.10; positive normalized gates mix four maps per directed pair; seven source channels give a frozen-read block-norm Lipschitz bound 0.70. With the actual alpha, the sweep contraction bound is `0.9336402349214215`; four sweeps give `0.7598331497328624`. `neural.py:117–124` retains prior a rather than resetting it. H can persist while activity fades; positive actual-coactivity writing and nonzero decay remain distinct. No next-state target or hidden predictive/reset mechanism was found.

**VERIFIED — no obligatorily dead or permanently saturated receiver under the declared baseline bounds.** Direct inspection and independent conservative bounds give the following. These are analytical ceilings, not observations that learning reaches them:

| Receiver/path | Bound or structural check | Interpretation |
|---|---|---|
| Sensory query | `G=0.1+0.9*h`; repeated over four unit-coordinate copies | h can affect a nonzero query; it does not gate the other-channel context input. Zero psi legitimately removes its immediate effect. |
| Fine retention | h changes the reclaim rate by up to 0.005/s | It affects existing residuals, without creating desired content. A zero residual legitimately has no spring displacement. |
| Association | Baseline q block norms ≤ `[2.75264,2.75264,2.75264,2.75264,3.17690,3.17690,3.03548,2.82843]`; total norm ≤8.22847 | Zero H blocks return at birth by design; the positive write path is present. |
| Regulatory features | `abs(Bq*q+Bv*v+b) ≤ 2.86423`; tanh magnitude ≤0.993517 | No forced binary64 tanh saturation. Every baseline Bq column is nonzero. |
| Regulatory outputs | Support-logit magnitude ≤11.68913; h approximately between 0.0000083844 and 0.999991616; maximum attenuation approximately 0.999966463 | Exact permanent suppression is not forced by legal baseline bounds, although small derivatives and cancellation are possible. |
| Motor dynamics | Oscillator ≤0.35; feedback norm bound `0.1*sqrt(15)`; motor-return block ≤3.03548; current ≤0.5; preactivation ≤4.27278 | No receiver is structurally bypassed or forced into exact saturation. Every direct-feedback column is nonzero. |

The regulatory row bound gives the conservative logit inequality `2*(sqrt(33)+0.1)`; q bounds follow from `0.1*sum(sqrt(p_n))` over other channel widths. These deductions concern the selected valid baseline, not every schema value that Config could accept.

**SCIENTIFIC QUESTION, NOT AN ENGINEERING DEFECT — effective learned influence and adequacy.** Whether actual q becomes negligible beside body/bias input, whether learned logits matter beside exploratory ones, whether common group usefulness protects useful fine differences, and whether the adapting/fading system provides useful regulation are unanswered. The saved arrays expose the relevant contributions. No equal-RMS target, tuning advice or claim of scientific success/failure follows.

## Physical realization and illumination ruling

**VERIFIED, except R1's contact timing — constitutive implementation.** `D/loom_p/physics.py:46–81` implements reserve-dependent actuator capacity, basal/attempted-effort expenditure, finite source debit/body credit with split renewal and headroom, separate integrity stress and gentle-contact repair. Instantaneous accounting has zero transfer/repair duration. The conservation checks confirm equality of recorded debit/credit; they do not prove a contact interval was physically warranted. This is why R1 survives those checks.

`chemistry.py:15–29,30–66` retains concentration while moving geometry changes harmonic solid/medium and face coefficients; it uses conservative backward Euler, residual checks, recorded small negative anomalies and no concentration clipping. The outer chemical boundary remains no-flux. The stored 60,000-step world-only prehistory and its reuse identities were checked, not rerun. `prehistory.py:49–80` verifies the cached field and relevant source dependencies.

**VERIFIED — 2026-09-22 illumination ruling.** `geometry.py:103–120` treats a boundary exit without a prior finite in-arena blocker as visible to the external directional field. It omits boundary walls only from shadow obstruction, caps shadows at the first domain exit, and includes finite interior bodies including the organism. `geometry.py:50–57,76–100,122–138` preserves ordinary wall M1 material, wall visual hits and material shading; ambient remains in the additive 0.1 term even in shadow. Protruding repair rectangles can shadow; a flush boundary surface does not suppress entry. Contact and field laws were not changed to obtain this optical behavior. The selected law matches `B/JASON_RULING_2026-09-22.md`; the rejected opaque alternative is preserved in `B/OPEN_ISSUE_LIGHT_BOUNDARY.md`.

**LIMITATION / EXPECTED PROVISIONAL CHOICE — numerical contact adequacy beyond R1 remains uncommissioned.** Finite-step frozen-force/contact-normal projection is not a convergence demonstration for curved contacts or moving constraints. Endpoint nonoverlap and several component examples do not prove continuous contact geometry is accurate in every case. This review distinguishes that disclosed numerical question from R1's concrete failure to schedule separation under the solver's own free-path convention. It does not demand scientific recovery success to accept repaired engineering.

## Records, observers and reproducibility

**VERIFIED — exact saved-record reconstruction.** The inspected `verify_engineering_records.verify(root)` function was called directly; its artifact-writing command-line entry point was not run. It reproduced:

| Existing final case | Native / wave / physical events | Neural states | Final field |
|---|---:|---|---|
| `birth_30s-attempt-002` | 3000 / 150 / 3000 | Every hash identical | Bit-identical |
| `nonzero_resume_1s-attempt-002` | 100 / 5 / 100 | Every hash identical | Bit-identical |
| `contact_ui_1s-attempt-002` | 100 / 5 / 101 | Every hash identical | Bit-identical |

Archive checksums, record counts, ordering and separate noise/perturbation clocks matched. Maximum tested source/body accounting discrepancy was `5.535190903717402e-17`. Production neural/field arithmetic is reused during reconstruction, so this is strong storage/schedule reproducibility evidence, not an independent equation oracle or proof of correct physical events.

**VERIFIED — inspector/replay isolation.** `records.py:86–92` converts arrays to detached display lists. `inspector.py:61–68` changes replay cursor or reconstructs from a newly loaded snapshot; `reconstruction.py:9–29` operates on that separate organism. An independent saved-record-40 replay/reconstruction/observation check reproduced 40 neural hashes and left the live Engine hash unchanged. Ordinary observations make no learning calls or random draws. Explicit native/wave commands at `inspector.py:70–87` are the separate, visible execution controls; this review did not invoke them or launch the server. R2 concerns the test fixture's mixed histories, not an observed mutation of live state.

**LIMITATION / EXPECTED PROVISIONAL CHOICE — delivery/operational scope.** Full histories are available through saved replay; live plotting has no separate native-history buffer, as disclosed. The portable package omits six large routine birth streams (native/wave/events for both attempts), while local files and their hashes remain present. The ZIP alone therefore cannot reproduce all birth reconstruction checks. This follows the handoff's compact-export instruction and is disclosed, rather than a missing local record. The implementation's recorded throughput/storage are not long-run guarantees; cross-platform identity, other dependency versions, actual full-disk exhaustion and ecological damaged-state recovery were not established.

**VERIFIED — package and source custody.** All 145 inventory entries match their hashes/sizes and account for the 146 ZIP members including the self-manifest. All 87 entries in `B/EVIDENCE_MANIFEST.json` match local files. All 16 recorded original sources and all five pinned Git blobs match. The runtime module bytes, dependency versions and semantic Config identity match `B/RUNTIME_RECORD.json`. The inspected environment is Python 3.13.5, NumPy 2.3.3, SciPy 1.16.2 and pytest 8.4.2, with the remaining packages matching `D/requirements-lock.txt`.

All 41 tracked task files were compared with committed/packaged content. `README.md` and `configuration.json` have only CRLF/LF differences between working bytes and Git; the package matches working bytes and normalized text matches Git. Runtime modules are byte-identical. Accepted Coupling and Base World Workbench copies differ from their pinned Git texts only by equation delimiter formatting. These distinctions must remain explicit rather than describing every copy as byte-identical.

**VERIFIED — the older branch base is not itself an implementation-fidelity defect.** The merge base is `98a8307e56f6884f2cc5dfb29ef924294f629c22`. The path to accepted reference `7ada2b300fa12a26b0daf40b1fa5682243ff6625` contains documentation commit `9dffecf4d7da962ac423414f37a38cdb28eaefc9` and its merge, with five changed files: root Current State, README, Coupling, and added Base World/decision-ledger-v0.2 documents. There is no implementation code in that gap. The builder explicitly sourced and packaged the later accepted physical references; the review checked those sources against their Git blobs.

The branch's root orientation remains older and must not silently substitute for the pinned accepted references. That is provenance/navigation debt, not grounds to merge branches to validate the existing implementation. Historical `EXP1-21` tree remains `f1b884a7ada4c806786d1530d76d446aac5d37b1`. No branch integration was performed or is proposed by this review.

## Reproduction commands

These commands reproduce the findings within the read-only review scope. They do not alter source, configuration or the existing evidence. The test suite creates only fresh temporary fixtures. The arithmetic snippets create no complete-loop organism lifetime. Do not invoke the smoke runner, inspector stepping, package writer or verifier's command-line entry point to reproduce these findings.

For R1, from the reviewed `developmental_ecology` directory:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
@'
import math
import numpy as np
from loom_p.schema import Config
from loom_p.physics import Body, actuator_forces, free_velocity, advance
from loom_p.geometry import fixtures, gap_normal
c=Config()
b=Body(np.array([2.,3.]),0.,velocity=np.array([-.001,0.]))
command=np.ones(2)
forces=actuator_forces(c,b,command)
v_inf=float(forces.sum()/c.linear_drag)
tr=math.log((v_inf-b.velocity[0])/v_inf)*c.body_mass/c.linear_drag
tm=tr/2
v,_=free_velocity(c,b,forces,tm)
source=next(f for f in fixtures(c,0.,0.) if f.get('source')==0)
print('return time',tr)
print('positive free gap',gap_normal(b.position+tm*v,c.body_radius,source)[0])
print('geometry tolerance',c.geometry_tol)
events,elapsed,terminal=advance(c,b,np.full(8,.2),0.,0.,command,.01)
print('elapsed/terminal/position',elapsed,terminal,b.position.tolist())
print([(e['duration'],e['impact'],float(e['transfer'].sum()),e['damage'])
       for e in events])
'@ | & '..\.venv\Scripts\python.exe' -B -
```

For R2, from the same directory, preserving any old temporary outputs by choosing a new directory:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$reviewTemp=Join-Path $env:TEMP ('loom-p-review-'+[guid]::NewGuid().ToString('N'))
& '..\.venv\Scripts\python.exe' -B -m pytest tests -q -p no:cacheprovider --basetemp $reviewTemp
```

For the R3 reference no-ops, from the same directory:

```powershell
@'
import runpy
t=runpy.run_path('tests/test_neural.py')
Regulator=t['Regulator']; Cortex=t['Cortex']
original_credit=Regulator.credit
def no_reference_credit(self,*args,**kwargs):
    before=self.reference.copy()
    original_credit(self,*args,**kwargs)
    self.reference=before
try:
    Regulator.credit=no_reference_credit
    t['test_bank_projection_and_reference_follow_new_value']()
    print('PASS despite bank reference no-op')
finally:
    Regulator.credit=original_credit
original_step=Cortex.step
def no_reference_step(self,*args,**kwargs):
    sr=self.shared_ref.copy(); fr=self.fine_ref.copy()
    original_step(self,*args,**kwargs)
    self.shared_ref=sr; self.fine_ref=fr
try:
    Cortex.step=no_reference_step
    t['test_sensory_old_rhs_and_pool_terms']()
    print('PASS despite sensory reference no-ops')
finally:
    Cortex.step=original_step
'@ | & '..\.venv\Scripts\python.exe' -B -
```

For the R3 unreachable terminal-handoff falsifier, from the same directory:

```powershell
@'
import inspect, runpy, textwrap
import pytest
import loom_p.engine as module
from loom_p.engine import Engine
t=runpy.run_path('tests/test_boundary_and_scheduler.py')
original=Engine.step
source=textwrap.dedent(inspect.getsource(original)).replace(
    'elif self.native_index%','if self.native_index%')
namespace={}
exec(compile(source,'<in-memory-terminal-guard-mutant>','exec'),
     module.__dict__,namespace)
try:
    Engine.step=namespace['step']
    with pytest.MonkeyPatch.context() as mp:
        t['test_terminal_scheduler_restores_trial_state_and_draws_once'](mp)
    print('PASS despite removal of terminal handoff exclusion')
finally:
    Engine.step=original
'@ | & '..\.venv\Scripts\python.exe' -B -
```

For saved evidence reconstruction, from the worktree root (import the function, which does not write the verification artifact):

```powershell
@'
from pathlib import Path
import sys
sys.path.insert(0,str(Path('developmental_ecology').resolve()))
from verify_engineering_records import verify
for case in ['birth_30s','nonzero_resume_1s','contact_ui_1s']:
    r=verify(Path('developmental_ecology/artifacts')/f'smoke-{case}-attempt-002')
    print(case,r['reconstruction'],r['field_reconstruction_bit_identical'])
'@ | & '.\.venv\Scripts\python.exe' -B -
```

For branch provenance, from the worktree root:

```powershell
$env:GIT_OPTIONAL_LOCKS='0'
git rev-parse HEAD
git branch --show-current
git merge-base HEAD 7ada2b300fa12a26b0daf40b1fa5682243ff6625
git diff --name-status 98a8307e56f6884f2cc5dfb29ef924294f629c22 7ada2b300fa12a26b0daf40b1fa5682243ff6625
git rev-parse HEAD:EXP1-21
```

## Coverage and final disposition

The review covers every requested audit area: equations (operation table); ordering and physical time (R1, R3 and timing trace); information boundaries; actual/evoked separation; distinct bodily learning; support/query/retention; configurable anatomy; native temporal retention; fading association; effective-signal bounds; physical/optical ruling; actual test falsifiers; observer isolation; and source/runtime/Git provenance. The five-file ancestry difference was independently checked and does not explain away R1 or require branch integration.

**UNRESOLVED / REQUIRES JASON:** no new mechanism ruling is required to identify the defects above. Jason retains authority to commission corrective work and decide whether a subsequently reviewed checkpoint proceeds. This report does not change canon, choose a new experimental sequence, or authorize commissioning. The broader scientific questions remain separate from engineering closure.

| Decision area | Classification | Fit to proceed at this exact checkpoint? |
|---|---|---|
| Retained P equations, separate bodily teaching, support latency, information boundaries | VERIFIED | Faithful baseline implementation on inspection. |
| Physical release/recontact and consequence accounting | MUST-FIX BEFORE COMMISSIONING — R1 | **No.** Full-step sustained contact can replace a separating/recontact interval. |
| Final suite reproducibility and consequential falsifiers | MUST-FIX BEFORE COMMISSIONING — R2–R3 | **No.** 43/44 pass in delivered state; key disabled operations still escape checks. |
| Native records, reconstruction, observer isolation, identities and branch-base provenance | VERIFIED | Support review; do not certify the faulty physical schedule. |
| Capacity, temporal compression, centring, contracting association and signal usefulness | LIMITATION / EXPECTED PROVISIONAL CHOICE; SCIENTIFIC QUESTION, NOT AN ENGINEERING DEFECT | No efficacy judgment or tuning recommendation. |
| **Overall: `d5f7efbe67193f215e52d95ca912db131a79f31c`** | **MUST-FIX BEFORE COMMISSIONING** | **HOLD. Correct and reverify the engineering findings under a new authorization; preserve this checkpoint.** |

Review completed and exported for Loom Research Workbench intake. No fixes or commissioning execution performed.
