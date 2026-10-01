# Loom P — bounded engineering build handoff

**Prepared:** 2026-09-21  
**Version:** 0.1  
**Prepared by:** Astra, design discussion  
**Status:** Build instructions for Jason to issue to his local Codex session. This file does not claim that code, tests, repository changes or experiments have already occurred.  
**Research object:** The specified P participation-plus-retention candidate; R and the other candidate families remain preserved.  
**Purpose:** Build an inspectable first implementation and verify its engineering fidelity, without mistaking its deliberately limited configuration for the whole Loom programme.

## 0. Authority and intended result

When Jason issues the accompanying launch instruction, implement the complete P organism/world/observer described by the sources below, using their proposed numerical configuration as the **first engineering configuration only**. Complete ordinary implementation decisions and the enumerated tests without repeatedly seeking approval of already accepted D1–D3. Do not seek developmental success as the condition for finishing the build.

Previously accepted:

- D1: useful history-dependent regulation and useful lasting sensory change are separate questions; neither stands in for the other.
- D2: P's bounded, explicitly reinforcement-like, separate energy/integrity perturbation–consequence rule may change its enumerated regulatory parameters. This is not general authority for a policy optimiser, combined utility or externally supplied behavioural strategy.
- D3: specify intact P first. R is available, not rejected, and must not be merged into P by default.
- A plain-language, end-to-end account of the actual data flow is required.

Jason's subsequent concerns are controlling qualifications of the proposed first build: eight units and two pools are unvalidated starting capacities; the mean-plus-endpoint packet is a limited temporal representation; fading association is not the programme's endpoint; possible adaptive magnitude regulation is a later hypothesis, not an instruction to add it now. Preserve the distinction between a concession for an engineering branch and acceptance of a substitute for the broader research goal.

**Deliver:** working local code, one visual inspector, reproducible configuration and manifests, an equation-to-code/test map, the scoped engineering verification results, an updated implementation-level walkthrough, and the unresolved adequacy/follow-up record. Then stop for review.

**Not authorised by this handoff:** scientific lifetimes/cohorts, efficacy-driven tuning, capacity or gain sweeps, a new experiment number, preregistration, developmental claim gates, a freeze of evidential settings, publication, remote push/PR/merge, altering archived results, or replacement of P's learning/packet/association laws. The short tests in section 7 are expressly authorised engineering executions; they are not secretly evidence of development.

## 1. Sources and exact identities

The `sources/` folder in this delivery contains byte-identical copies of the five documents below. Verify them using `SOURCE_MANIFEST.json`. Read the workbench's current map and status first, then the current-state foundation, the D1–D3 record/handoff, the complete P parent, complete specification, walkthrough and design review. Use the accepted world/body files through the workbench's registered reference links when checking a particular physical requirement.

| Source | SHA-256 | Byte length |
|---|---|---:|
| `LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md` | `34bd519bb01253f783521204c9e6358b11703282ec322f4707e5ece1bb6a4da4` | 38379 |
| `P_IMPLEMENTATION_AND_OBSERVATION_SPEC_v0_1_REVIEW_DRAFT.md` | `f1af7cf234e15c0215848c5775d7f84c2d8edbeea389dce53b889b1cfa9c64ba` | 68773 |
| `P_PLAIN_LANGUAGE_DATA_FLOW_v0_1_REVIEW_DRAFT.md` | `c31218c3f65bb4e5d35d02a9030978c25504f3d93a7a95682e2255d701d8294b` | 32906 |
| `LOOM_P_SPECIFICATION_HANDOFF_2026-09-20.md` | `c133f2114a1b41254c5965f61ae202c9b198733173bdc9e9d8193164be12be33` | 21878 |
| `P_SPECIFICATION_DESIGN_REVIEW.md` | `f490e9c91ad62fc34a26c81de914dfeff6ffa22c2a11436179b888ca84fe7d62` | 19317 |

The specimen's IDs are `P-IMPLEMENTATION-OBSERVATION-SPEC-83a00674` and `P-PLAIN-LANGUAGE-DATA-FLOW-83a00674`. The specification session is `2026-09-20-p-specification-83a00674`.

The reference commit is `7ada2b300fa12a26b0daf40b1fa5682243ff6625`. It identifies the accepted Base World reference, **not current remote HEAD and not the later uncommitted P specification**. The snapshot's historical `EXP1-21/` tree is `f1b884a7ada4c806786d1530d76d446aac5d37b1`.

Read source instructions according to their historical scope. Old “no implementation” headers describe the authority when those documents were written; the issued build instruction supplies the new, restricted authority. Old experimental execution protocols do not authorise new runs or auto-push. Do not rewrite original headers or source files to make them appear contemporaneous.

Formatting variants in the live workbench may have authorised equation-delimiter changes. Record their identity separately; use the packaged exact copies for provenance. A substantive discrepancy, contradictory equation, or changed parent is a real issue to surface. A harmless formatting difference is not a reason to reconstruct or overwrite a source.

## 2. Local workspace and preservation

Research input folder:

```text
C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench
```

Previously used code repository, to verify rather than assume:

```text
C:\Users\Jason\Desktop\Eridos\Loom
```

1. Resolve the approved folders and read applicable `AGENTS.md` instructions. Inspect local repository identity, branch, status, origin and relevant existing code. Do not reuse the enclosing Obsidian Git repository as the code repository.
2. Treat the research workbench and its source archive as read-only for this build, except for the narrowly permitted contribution/export in section 8. Do not stage, commit, configure or repair the enclosing vault repository. Its previously observed index activity is not this task's investigation.
3. In the actual Loom code repository, use a new isolated worktree and unique local branch based on its actual reviewed main state. A name such as `build/p-engineering-baseline-<unique-suffix>` is acceptable. Local worktree/branch creation and scoped local commits in that repository are authorised by the launch instruction; no remote operation is authorised. Do not reset to the old reference commit or overwrite intervening work.
4. If the actual main now contains substantive competing organism work, identify it before selecting paths or a base. Do not replace that work. A missing repository, inaccessible folder, or materially conflicting instructions justify a focused question—not improvising a new repository inside the vault.
5. Preserve all unrelated tracked, untracked and ignored work. No reset, clean, stash, force operation, amendment of an existing commit, branch deletion or worktree deletion. Stage exact task-owned paths only.
6. Put new code in an isolated Developmental Ecology package, not `EXP1-21/`. Use a new build-document subdirectory under the active documentation area. Do not amend the historical archive, accepted foundation, root research canon or existing source records. Record the archive tree before and after; never “repair” a mismatch.
7. Install required dependencies only into a scoped project environment. No global installation, vault plugin, system security change, external telemetry, cloud service, model API dependency or paid service is required.
8. If permissions are needed for the isolated worktree, request them normally. Do not bypass access controls. If local Git identity is unavailable, do not change global identity or forge an author; preserve work and report the missing checkpoint rather than blocking all ordinary file work.

## 3. First configuration and scientific limits

Give the configuration an ordinary engineering identifier, for example `p_engineering_baseline_v0_1`. This is not an experiment number or evidence freeze. Preserve the exact source-derived default configuration before any test. The inspector and reports must describe it as **uncommissioned**.

Retain the specification's equations, sensor geometry, world laws, timings and numerical defaults. In particular:

- Four learned sensory cortices, eight continuous processing units each; two four-row weight pools per cortex. Light has ten raw receptors, chemistry four, contact eight and proprioception seven. A “unit” is one scalar cortical activity coordinate with a learned receptor-sensitivity row, not a pixel, object, JEPA, layer or semantic feature.
- One-level sensory pooling is a deliberately small case. It can exercise differentiation and support-dependent coarsening; it cannot establish the full nested coarse-to-fine developmental account. Fixed recurrent differences can also make tightly tied units respond differently, so activity diversity alone is not evidence of learned unpooling.
- The sensory learning family is the exact Oja-type rule with the specified recurrence and competition. It is **not a small JEPA and is not assumed equivalent to one**. Do not add pretrained encoders or a new predictive objective.
- Mean-plus-endpoint packets compress the native trajectory. They are not proven to preserve the temporal distinctions required by the moving block or the organism's own motion. Do not silently append R's temporal terms, slots, timestamps, velocities or a raw-sequence buffer to the learner.
- The central operator is associative rather than next-wave forecasting, but the proposed 0.10 map radius enforces a fading frozen-query regime. Persistent learned maps are different from persistent associative activity. This configuration does not test free-running associative chains and does not exhaust the programme's association ambition.
- Receptor-mean and packet-mean subtraction can attenuate sustained inputs. Keep these laws visible; do not install a tonic bypass, remove centring, add normalization or change their timescales to make a trace look better.
- The body's actual energy and integrity remain separately available and changed only by real accounting. D2 does not permit a shared reward, critic, privileged source success signal, sensory target or a conventional navigator.

Create `LIMITATIONS_AND_FOLLOWUP.md` with these named unresolved topics: capacity/ecology matching; within-wave temporal information; tonic information under centring; associative continuation beyond the contracting regime; ineffective versus dominating signal scales; and group-level support versus useful fine differentiation. These are research questions, not mandatory failures, preselected fixes or reasons to delay faithful construction.

## 4. Parameterisation without building a platform

The default remains the eight-unit, two-pool case. Implement array dimensions from a validated schema rather than hardcoding 8, 16, 82 or 164 throughout the code. Derive map shapes, feature projections, regulatory output counts, anatomical slices, records and UI labels consistently.

Support configurable widths and equal-size one-level pool memberships wherever the stated P laws already define the operation. Validate legal membership, complete coordinate coverage and dimension consistency. A second-dimensional construction/arithmetic fixture may use a different legal width or grouping solely to catch hardcoding; it is not a capacity sweep or developmental comparison.

Changing width can change parameter count, random scaling, accumulated coactivity, map strength and regulation dimension. Record the exact initialization and norm conventions; do not automatically retune them or claim that width alone was changed causally. Nested hierarchy, new packet families and different associative models require a reviewed specification, not invented generality here.

Keep clean code boundaries for:

- transduction and body/world accounting;
- sensory activity/learning and packet emission;
- central context, map writing, use and recall;
- regulatory response and its two bodily-learning banks;
- motor generation and enactment;
- read-only observations, storage and inspection.

These boundaries permit future replacement and comparison. They do not justify a plugin ecosystem, unimplemented alternative engines, a job scheduler, a database platform or a broad experimental-search harness.

## 5. Implementation and information-flow contract

Build one local CPU reference implementation using the binary64 arithmetic, deterministic ordering and solver requirements in the specification. A Python implementation with pinned scientific-array, solver, test and desktop-display dependencies is a permissible engineering choice; record actual versions. Prefer clear, directly auditable functions over a generic training framework. A constrained physical contact solver is permitted; it is not an organism policy optimiser.

Before coding law-bearing functions, write a short `IMPLEMENTATION_ANNEX.md` naming module responsibilities, outstanding numerical conventions, the configuration schema, stopping/failure conventions and the intended verification fixtures. Complete and continue in the same task unless a genuine law-changing ambiguity appears. This is not another readiness review.

Pin the remaining engineering details explicitly: random seed serialization and endpoint-safe binary64 conversion, contact ordering and simultaneous constraints, event-location tolerances, zero-duration impact handling, positive-duration contact accounting, field residual norm and zero-RHS handling, terminal partial-step recomputation, projections and schema versions. Tolerances are numerical validity conditions—not behavioural success gates. Do not weaken them because an undesired biological-looking outcome occurs.

Preserve all 21 numbered P equations and the exact specification's read/write ordering. In particular:

- Actual raw sensory input, residuals, cortical activity, packet, trace, query and evocation remain distinct.
- Write association from actual packets and traces, never from each internal recurrent sweep. Use-preservation is not a new occurrence.
- Read old maps; use four simultaneous sweeps with the specified joint `S / alpha / Delta` relationship; recompute final q without another state sweep; write once afterward.
- New h affects the next query, not the query that generated it. It affects the subsequent native sensory spring as specified.
- Attribute current bodily consequence to previous applied perturbation/feature traces before drawing new perturbations.
- Actual energy/integrity are not substituted by returned content, including when q has large bodily coordinates.
- No direct full-scene input to the regulator; preserve the separately specified fast contact/proprioception motor route and ungated context-gate route.
- The delivered-command motor packet stays as defined; observer access to pre-attenuation tendency must not become an additional learner input.
- Ordinary neural updates are counted in physical time. Contact-solver subdivisions, display frames and internal association sweeps do not produce extra learning encounters or noise draws.
- Preserve every transient and structural state, held control, cache, partial accumulator, phase and random counter needed for faithful pause/resume. Replaying records in the inspector does not train the organism.

If the exact law has a concrete unresolvable contradiction, preserve an issue with source sections, competing readings and the smallest proposed resolution. Do not manufacture an alternative silently. Continue independent implementation work that does not rely on that decision.

## 6. Inspector and records: expose the suspected bottlenecks

Implement the specification's native, wave, physical-event and full-snapshot records. No silent downsampling of saved native data. Lossless compression is allowed. Record actual schema widths, storage and throughput; prior estimates are not measurements.

Provide a single local visual application with world/body, internal data flow and development views. Include double-click launch and setup instructions so Jason need not operate a CLI. Open paused; nothing should auto-run on application launch. Provide bounded engineering-fixture controls, pause, native/wave step where permitted, saved-record replay and an obvious stop control. Larger/general execution capability may exist, but do not launch it in this task.

The current configuration, code identity and uncommissioned status must be visible. No live refill, hidden parameter tuning, resource relocation or reset masquerading as continuation. Renderer speed and plotting must not alter arithmetic, learning, clocks or random draws.

In addition to the normal inspector, expose these read-only diagnostics using already available states:

**Capacity and pooling.** Unit responses; shared and residual parameters; opening state and actual spring coefficient; formation/coarsening/reference contributions; bounds/projections; common versus differential group activity. A high residual norm is not evidence of useful differentiation.

**Within-wave history.** Display the native input/activity sequence for a selected wave beside the exact mean, endpoint, centred packet and trace sent onward. Report the phase of an event within a wave only to the observer. Never feed diagnostic timing or sequence labels to the organism.

**Adaptation.** Show raw continuing input, its running mean and residual, the resulting cortical activity, then packet mean/beta/z. Preserve zero/near-zero cases and identify where a distinction disappears rather than normalising it away for display.

**Signal scale at the actual point of use.** Show per-channel return contributions, total q, `B_q q` versus actual-body and bias contributions, learned versus exploratory regulatory logits, direct motor feedback versus evoked contribution, saturation, and map write/decay/bound effects. Norm, RMS or distribution summaries may be observer statistics; retain the underlying values. Equal numerical RMS across unlike channels is not a target.

**Retained associations versus transient activity.** Display learned H and its use state separately from a and q. Silent input and contracting central dynamics must not be misreported as loss of all stored association.

Measurements must be trajectory-inert. Verify that disabling plotting or observing fewer panels leaves state and random streams unchanged.

## 7. Authorised engineering verification

This section supplies a bounded engineering execution scope. It does not approve the later 600-second organism observation, an entire developmental life, a cohort, parameter search or commissioning efficacy study.

### 7.1 Arithmetic and contract fixtures

Implement and execute small deterministic tests for:

1. Baseline dimensions and source-to-array routing, plus one legal alternate-size schema/arithmetic fixture. Confirm the default reproduces the declared 82/164/88,608 dimension inventory.
2. All 21 parent operations, exact native/handoff ordering, one-write semantics, final old-map q calculation, and previous-versus-new perturbation eligibility. Include deliberately wrong-order/no-op implementations as negative fixtures for the most consequential checks.
3. Pool centring and reconstruction, fixed parameter count, bounded projections, independent group treatment, private opening and the exact effect of h on query gain and the fine spring. Manufactured local pressures may exercise differentiation and relaxation; they are not an ecological learning result. Do not use diversity caused by fixed A as proof of unpooling.
4. Separate bodily learning and reserve ownership. Perturb one bodily input with the other held fixed at the learning interface; check the correct bank receives its direct learning signal. Shared behavioural consequences remain possible. Injected evoked reserve content must not replenish the actual body.
5. Physical conservation, renewed stock accounting, basal/actuation expenditure, actual-source headroom, nonzero-duration exchange/repair, zero-duration impacts, stress for every collider, swept mover collision and terminal crossings. No repair/uptake may be manufactured by averaging impacts across free flight.
6. Chemical flux/boundary/emission conservation, lawful solid-dependent coefficients, moving-geometry continuity and the exact finite prehistory. No deletion or clipping of inconvenient field values.
7. Sensor geometry and rear blindness, stable sampling conventions, delivered command versus actual movement, and an explicit learner input allowlist. Observer IDs/pose/stock/time/probes must remain outside the learner.
8. All-state pause/resume, deterministic record reconstruction and observer non-interference. Test restart from a deliberately nonzero manufactured state as well as birth; otherwise missing memory state can hide behind zeros.
9. Non-finite, storage failure, malformed snapshot and solver-failure handling. Exceptions must create an honest incomplete/failure record, not an apparently healthy state. JSON must not emit bare NaN/Infinity. Numerical tolerances and expected results are specified before execution.

### 7.2 Information-loss fixtures: report, do not optimise to pass

Build an observer-only deterministic diagnostic utility to inspect a small predeclared set of native signal histories through the **actual implemented** transduction/cortex/packet path. Use fixed or frozen documented internal states, never a new trained observer passed to the organism. Suitable cases include reversed local motion patterns, two short pulses in opposite orders with matched total exposure and endpoint, wave-boundary shifts, and a sustained step/slow change.

Record raw histories, cortical histories, packets, subsequent context and numerical distances at each available stage. Include a direct packet-arithmetic fixture demonstrating that identical means and endpoints need not identify the whole trajectory. Such a fixture describes the compression operator; do not claim it proves that every demonstrated trace is reachable from the physical world or that the complete organism always confuses it.

A faithfully implemented packet can lose a distinction. That is an observed property of this limited mechanism, not automatically a coding failure. Do not tune seeds, learning rates, signals or thresholds until every diagnostic becomes separable. Report a mechanical calculation as such and a limitation as such. No universal temporal-adequacy claim follows from passing a few examples.

A separate algebraic/exponential filter fixture may run long enough to show adaptation on the specified timescale; it is not a freely acting organism lifetime. A frozen-map associative fixture may check the documented contraction with a manufactured nonzero legal H; this is not a claim that learning has produced those maps. Distinguish rejection of future forecast targets from dependence on recent sensory traces.

### 7.3 Complete-loop and UI smoke budget

Before execution, name at most **three deterministic integration cases**, each capped at **30 seconds of simulated organism time**, with fixed seed/state and purpose. These are administrative engineering limits, not scientific thresholds. A birth case, a nonzero-state pause/resume case and a contact/record/UI case are sufficient examples. Do not require survival, improved behaviour, resource discovery or useful sensory learning as a pass condition.

The exact **600-second world-only chemical prehistory** is allowed when required to construct a lawful newborn fixture. No organism evolves during it. It is not deducted from the 30-second organism limit. Cache/reuse it only with identical field law, geometry, source state and mover phase, with provenance verified. Do not shorten it to save time while presenting the resulting birth as the specified baseline.

Re-execution of a fixed case after an actual implementation correction is allowed with a recorded reason, preserving attempts. Do not change a configuration or initial state in response to its behavioural outcome. No automatic progression from successful smokes to full lives, sweeps or training. If the resource cost of the prescribed check is unexpectedly large, report it before enlarging the budget or changing the laws.

## 8. Completion and checkpoint

Use one main writer. Optional independent reviewers should be narrowly scoped and read-only: numerical/data-flow fidelity, then physical/recording fidelity. Do not launch an uncontrolled set of writers or have all reviewers regenerate the design. A reviewer should inspect source and code, not only the builder's completion narrative.

A useful delivery includes:

- Working local package, pinned dependencies, exact configuration, tests and double-click inspector launcher.
- `IMPLEMENTATION_ANNEX.md`: source-resolved numerical conventions and bounded engineering decisions.
- `EQUATION_TO_CODE_AND_TEST_MAP.md`: every consequential rule, executing function and verifying fixture; omitted coverage is explicit.
- `IMPLEMENTED_P_DATA_FLOW.md`: plain-language source-to-effect walkthrough corresponding to the implemented revision; include dimensions, supplied/learned distinctions, timing and known representation losses. Do not alter archived walkthrough bytes.
- `LIMITATIONS_AND_FOLLOWUP.md`: the questions in sections 3 and 9, their observer diagnostics and the limits of present conclusions.
- `BUILD_REPORT.md` and machine-readable verification/artifact manifests: actual commands, seeds, simulated durations, configuration/source/code hashes, environment, results, failed attempts and remaining issues. State engineering verification separately from developmental adequacy.

Checkpoint exact task-owned code/docs in the **new local code branch only** when allowed by the repository's normal instructions. No remote push, PR or merge. Report the actual commit, base and archive-tree check; do not infer a clean unrelated workspace.

Return a portable review package in a unique export location with the report, manifests, walkthrough and relevant evidence, not gigabytes of copied routine traces. Keep full raw outputs in the declared artifact location. Write only a new contribution/export directory in the workbench if it is within the approved write scope; do not claim integration ownership over live indexes, AGENTS.md or decision history. Include a proposed workbench status update for its integrator. If that extra folder is inaccessible, return the package in the code worktree and give its exact path.

Stop with the inspector paused/closed and no background simulation continuing. Report explicitly what is implemented, what was verified, what remains untested, and what requires a scientific design decision. A successful build is not authorisation for a cohort.

## 9. Follow-up design obligations, not extra work authorised now

The first build is not the endpoint. Preserve the following as linked research issues, without requiring baseline success before they can be investigated:

| Question | What a later design should separate |
|---|---|
| Capacity and pool topology | Raw receptor accessibility, cortical width, number/size of pools, hierarchy depth, learning timescales and changed downstream capacity. Width examples such as 8/16/32 are proposals, not an authorised sweep. A new configuration receives a new identity and fresh initialization unless transfer is explicitly designed. |
| Temporal representation | Which organism-relevant differences already exist in raw histories, survive cortical activity, survive emission and remain usable centrally. Larger width does not automatically recover information removed before it. A different packet is a reviewed revision, not a debugging patch. |
| Association-led continuation | Preserve the goal of context-sensitive internal unfolding, with earlier evocation able to shape what follows, no mandatory next-state target, and ongoing vulnerability to actual perception/body. The present frozen-query contraction deliberately narrows this. A less restrictive P regime and a different associative operation are distinct candidate revisions; larger gain alone is no promise of useful thought. |
| Sensory learning family | The tiny local learner is a first engineering hypothesis, not a demonstrated replacement for a JEPA-like developing cortex. A later alternative must specify its local objective, temporal operation, preparation, return interface and capacity law. |
| Adaptive signal regulation | Examine bounded, context-appropriate effective influence rather than forcing equal numerical amplitudes everywhere. Preserve silence and meaningful magnitude, separate actual reserves, timescale/bound state and existing stability assumptions. Do not add this rule until its site and law are reviewed. |

Before interpreting a later null, identify which plausible failure location the saved evidence supports. Do not require every question to be solved before commissioning, and do not tune around a representation loss indefinitely. Structural exclusions cannot be falsified by demanding the excluded behaviour from this configuration.

## 10. Reasoning and model use

Jason should select Astra explicitly where available rather than assume “Latest.” Recommended division: **High for the main implementation; a bounded Max/Ultra review for equation-to-code, timing, physics and evidence fidelity before broader commissioning.** Routine documentation or UI edits may use less effort. This is a task-allocation recommendation, not a measured optimal setting or a correctness guarantee.

OpenAI's official usage guide says higher reasoning can use more allowance and need not improve a result. Its rate-card documentation says Ultra uses maximum reasoning and may involve additional agents for eligible users. Do not equate Ultra to a fixed multiplier, invent a backend identity, or assume writing “use Ultra” in the prompt changes the user's selected setting. Record disclosed settings and limits honestly.

Official sources checked for this handoff (2026-09-21):

- OpenAI Help Center, “Managing usage with GPT-6 Astra in Work and Codex,” article 20001516.
- OpenAI Help Center, “ChatGPT Rate Card (Business, Enterprise/Edu credit-based pricing),” article 11481834.
- OpenAI API, GPT-6 Astra model page: https://developers.openai.com/api/docs/models/gpt-6-astra

This setting choice does not replace independent review, exact code provenance, reachable failing test cases or complete source access.
