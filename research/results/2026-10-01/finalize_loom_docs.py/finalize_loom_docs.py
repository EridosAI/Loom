from pathlib import Path
import json

stage=Path('p_build_staging')
docs=stage/'docs/developmental_ecology/p_engineering_20260921'
actual=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405')
def read(p): return p.read_text(encoding='utf-8')
def write(p,s): p.write_text(s,encoding='utf-8')
old=read(actual/'docs/developmental_ecology/p_engineering_20260921/BUILD_REPORT.md')
write(docs/'PRIOR_CHECKPOINT_REPORT.md',old)
checks=json.loads(read(actual/'developmental_ecology/artifacts/verification/record-reconstruction.json'))['cases']
report='''# P engineering build — bounded verification complete

**Ready for the originally specified build review; uncommissioned.** Continued from `bf5df05ad2aafb8590e8765a947df111956b9528`, applied Jason's 2026-09-22 directional-illumination ruling, and completed the three predeclared engineering cases. No scientific conclusion or additional execution is authorized by this result.

'''+old[old.index('## Actual environment'):old.index('## What exists')]+'''## Implemented revision and selected law

The complete local body/world/P organism, configurable sensory widths and equal-size one-level pools, native-history/pooling/effective-signal diagnostics, lossless records and one paused visual inspector are implemented. All 21 P operations remain intact. RUNTIME_RECORD.json and each smoke manifest record code/runtime/configuration identities. The review package CHECKPOINT_RECEIPT.json records the exact final commit/branch and archive tree. Package-scoped Git attributes preserve exact runtime source bytes because snapshot identity is byte-exact.

Configuration: `p_engineering_baseline_v0_1`, SHA-256 `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`, `illumination_boundary="open"`. External directional light crosses the boundary; finite interior bodies shadow it; ambient remains. Walls retain M1 material, visual response and contact. The specified restorative rectangles protrude into the interior and can shadow. The closed-wall alternative is preserved as rejected in OPEN_ISSUE_LIGHT_BOUNDARY.md. No other constitutive parameter or mechanism changed.

## Executed engineering evidence

Final component suite: **44 passed**, `artifacts/verification/component-attempt-006.txt`. Coverage includes the 21 operations with independent arithmetic oracles and consequential wrong-order/no-op comparisons; configurable anatomy; conservation/contact accounting; chemistry/sensors; strict snapshots/failure paths; the selected optical law; and terminal scheduler rollback. The equation/test map names exact checks and limits. Earlier logs remain intact.

Final fixed cases: master seed **5284097 / 0x50A101**, life **0**, attempt **002**, unchanged initial-state definitions.

| Case | Simulated duration | Native / wave / physical records | Wall seconds | Uncompressed record bytes | Stored evidence bytes |
|---|---:|---:|---:|---:|---:|
'''
for r in checks:
    report+=f"| {r['case']} | {r['time']:.2f} s | {r['native']} / {r['wave']} / {r['events']} | {r['execution_wall_seconds']:.3f} | {r['uncompressed_bytes']:,} | {r['stored_bytes']:,} |\n"
report+='''
All three stopped at administrative limits. Binary64 accumulation gives the birth endpoint 30.00000000000189 s, within numerical comparison tolerance; exactly 3,000 or 100 native steps were executed. Reserves are descriptive records, never survival or useful-learning criteria. The contact fixture contains one zero-duration source impact and subsequent separation; it does not establish useful uptake or repair behaviour.

Every one of **3,200 final native neural states** reconstructed bit-for-bit from initial full snapshots plus saved actual receptor/reserve inputs and the original schedule. All reconstructed final fields also matched bit-for-bit using saved ending stocks and geometry. Checksums, counts and separate native-noise/wave perturbation clocks matched. Maximum tested source/body accounting discrepancy was **5.54e-17** reserve units. `artifacts/verification/record-reconstruction.json` gives exact values and hashes. These detached arithmetic reconstructions are not additional freely acting complete-loop runs.

The nonzero case saved at 0.07 s inside its first wave, then compared every full state against uninterrupted continuation for 0.93 s. Learned values, references, traces, packet integrals, held controls, fields and random counters stayed identical. One continuation was repeatedly observed through the inspector and one was not; states remained identical. Initial snapshot roundtrips also matched. The UI's first 20 native records exactly match the saved contact case's prefix.

Measured scalar widths are **2,513/native**, **13,685/wave**, and **62–67/physical record**. Detailed native formation/projection arrays make storage larger than the specification's rough planning allowance. Birth saved **165,615,915 uncompressed record bytes**, **59,125,747 stored bytes including snapshots**, in **124.821 wall seconds**: about 24 native steps/second. No native downsampling occurred. These short-fixture costs are not a long-run performance guarantee; this implementation is slower than real time on this host.

## Original preparation and information-loss diagnostics

Original prehistory: **60,000 world-only steps** at 0.01 s, from −600 to 0, full sources, no organism, phase **3.558411277237072**. Wall time **65.17840160000014 s**, maximum relative residual **9.999593754095302e-11**, maximum per-step mass-balance residual **6.063928742819358e-10**. Field SHA-256 **7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096**. It was **not rerun**. Reuse verifies original module bytes, unchanged field-relevant solver/geometry/random-stream code, parameters, sources and phase. Original manifest and field archive remain unchanged; constructed fixtures carry the reuse verification.

The earlier fixed calculations in `artifacts/information_loss.json` are unchanged. Their recorded configuration predates the optical ruling, but they use manufactured contact histories and unchanged neural arithmetic, not light. Pulse-order examples retain smaller packet/context distinctions; the direct mean-plus-endpoint counterexample has zero packet distance for different paths. The 90-second algebraic receptor-filter calculation and frozen-map contraction calculation are components, not organism lifetimes. No diagnostic was tuned for separability or learning success.

## Failures, corrections and repetition accounting

PRIOR_CHECKPOINT_REPORT.md and the original logs preserve the earlier work. The earlier 35-pass/1-fail component run wrongly expected zero old packet means; only its oracle changed. Component attempts 004 and 005 passed 41 checks; attempt 006 passed 44 with new regressions.

First complete-loop attempt: birth completed 30 s; nonzero resume stopped at **0.20 s** because a live inspector wave lacked a timestamp; contact stopped at **0.01 s** because conservative collision search assigned a distant mover's speed to a nearly touching stationary source. Both failures recorded `apparatus_failure`, `complete=false` and failure snapshots. Corrections added the observer timestamp and a correct per-fixture conservative bound for the same frozen-force trajectory. Tolerances, physical parameters, seed and initial states stayed fixed. Regressions reject both faults. All three cases were executed as attempt 002 so final evidence uses one corrected code identity. `artifacts/smoke-attempt-001-code/` preserves every original module byte, verified against the first-attempt hashes.

Total complete-loop simulated execution, including failures and deterministic comparisons: **30 + 0.20 + 0.13 + 0.01 + 30 + 1 + 0.93 + 1 + 0.20 = 63.47 seconds**. No single case exceeded its predeclared limit. The 0.13 and 0.93 are duplicate restart continuations; the final 0.20 is explicit UI stepping of the same contact-case prefix. No fourth integration case was introduced. Detached reconstruction is separately identified above.

## Inspector verification and use

Double-click `developmental_ecology/Open Loom Inspector.cmd`. It loads the verified **initial contact fixture at time zero**, paused and uncommissioned. This is a named manufactured engineering fixture, not an ecological life or automatic continuation of the previous manual UI session. Native/wave controls permit at most one second per session. Complete pause states are saved; the snapshot loader's all-state restoration is verified.

The launcher was invoked through Windows Start-Process and opened the application. Actual browser checks inspected all three views, replay at 0.40 s, exact reconstruction of 40 native records, one native step, a step to 0.20 s, Pause and Stop. A literal desktop mouse double-click was not performed because native desktop input is unavailable. The same launch file succeeded through Windows execution; no launcher/host permission remained blocking. After Stop the loopback port was confirmed closed.

Complete within-wave history plots use saved replay. Live stepping exposes endpoint and wave values, without a separate live history plot buffer. Parameter panels distinguish the paused snapshot from a detached reconstruction requested at a saved cursor. Replay/reconstruction do not mutate the live state. Evidence: `artifacts/verification/ui-verification.json`.

## Review boundary and remaining limits

No unresolved law-changing ambiguity remains for this branch. Capacity/ecology fit, temporal compression, tonic information, associative continuation, effective signal scale and useful differentiation remain research questions in LIMITATIONS_AND_FOLLOWUP.md. No useful learning, sensory development or survival claim follows.

Not tested: scientific lifetimes, proposed 600-second organism observation, cohorts, sweeps, efficacy tuning, commissioning campaigns, ecological damaged-state recovery, long-term storage/performance, cross-platform bit identity or other dependency versions. No natural terminal event occurred in the three smokes: terminal handling was checked with a scheduler stand-in plus separate real-physics crossing components. Contact fixtures are bounded examples, not exhaustive certification of all geometries. Storage failure was injected; actual OS full-disk exhaustion was not induced. No independent reviewer was spawned; the main writer checked source/code ordering and boundaries directly. Actual model/reasoning effort was not independently measurable and is not asserted as a correctness guarantee.

No vault Git writes, historical/source/header edits, push, PR, merge, experiment number or preregistration occurred. The inspector is closed and no background simulation continues. The portable ZIP contains exact code, sources, configuration and relevant evidence. Routine birth traces remain at their full local artifact paths; their hashes and results are included in the portable inventory. Stop for Jason's review.
'''
write(docs/'BUILD_REPORT.md',report)
p=docs/'IMPLEMENTED_P_DATA_FLOW.md'; s=read(p)
first=s.index('\n## What this configuration')
s='''# Implemented P data flow — bounded engineering build

This describes implemented P and its engineering checks, not a developmental result. Jason's selected open optical boundary is recorded in OPEN_ISSUE_LIGHT_BOUNDARY.md. The configuration remains uncommissioned. The 30-second birth and two one-second manufactured cases executed; no scientific lifetime or efficacy test did.
'''+s[first:]
s=s.replace('Geometry and material laws calculate light intensities; the optical boundary is the unresolved item.', 'Geometry and material laws calculate light intensities. External directional light enters across the arena boundary; finite interior solids can shadow it, while ambient remains. Walls retain ordinary visual material and contact response; the optical-domain boundary does not make them transparent material.')
s=s.replace('The coupled scheduler includes tentative-step rollback and terminal shortening; that complete-loop machinery still needs its declared smoke and terminal-coupling coverage. Saving and reopening a manufactured nonzero state reproduces standalone neural continuation exactly. This is narrower than verified complete-loop pause/resume.', 'The scheduler restores tentative steps before terminal shortening. Arithmetic stand-ins verify rollback, one retained noise draw and partial-wave stopping; real physical reserve crossing is separately tested. The nonzero complete-loop case resumes at 0.07 s and reproduces every full state through 1.00 s exactly. None of the three smokes encountered a terminal event; component coverage is not presented as a natural complete-loop terminal test.')
s=s.replace('At this checkpoint no complete-loop fixture exists, so its execution controls remain disabled; the inspected UI shows this clearly.', 'The inspector loads the verified initial contact fixture without advancing it. Native/wave stepping is bounded to one second; replay selects saved records. Complete history plots use saved replay; live stepping shows endpoint/wave values. Detailed parameter reconstruction is detached from the live organism and checks every complete neural-state hash. All three final trajectories and final fields reconstructed exactly.')
write(p,s)
p=docs/'LIMITATIONS_AND_FOLLOWUP.md'; s=read(p)
s=s.replace('This is an incomplete engineering checkpoint, not a completed or commissioned build. The unresolved optical boundary and unexecuted complete-loop checks are separate from the research limitations below.', 'The bounded engineering build is complete for review and remains uncommissioned. Jason resolved the optical boundary; all three named smokes passed after disclosed implementation corrections. The research questions below remain open.')
s=s[:s.index('Other open work:')]+'''Remaining coverage limits: no natural complete-loop terminal event occurred; shortening was checked with a scheduler stand-in plus real physical crossing components. Contact examples do not exhaust simultaneous moving-body geometries. Cross-platform/dependency bit identity, long-run storage/performance and OS full-disk exhaustion were not tested. Snapshot compatibility is strict same-code/schema, not forward migration. A literal mouse double-click was unavailable; invoking the delivered file through Windows succeeded, and its paused browser application was checked. Full history plots use saved replay; live stepping exposes endpoint/wave values. Independent numerical/physical review remains useful before commissioning.

Not tested or authorized: proposed 600-second organism observation, scientific lifetimes, cohorts, capacity/gain sweeps, efficacy tuning, commissioning ceilings, useful learning, ecological damaged-state repair followed by return to energy, survival capability, or causal contribution of lasting sensory change. Short smokes are engineering data only.

No experiment number, preregistration, evidential freeze, push, PR or merge was created. R, nested pooling, different packets, alternative sensory learning, less restrictive P regimes and other associative families remain available as separately reviewed designs. A scientific null cannot be inferred from these checks.
'''
write(p,s)
write(docs/'PROPOSED_WORKBENCH_STATUS_UPDATE.md','''# Proposed status contribution — for the workbench integrator

Do not overwrite live workbench indexes from this contribution. Jason authorized the bounded P build on 2026-09-21 and resolved its optical boundary on 2026-09-22. D1–D3 remain accepted. Work continued in the same isolated code worktree/branch from bf5df05ad2aafb8590e8765a947df111956b9528; the review package CHECKPOINT_RECEIPT.json records the final commit.

Status: bounded engineering build complete for review, uncommissioned. 44 component checks pass. birth_30s, nonzero_resume_1s and contact_ui_1s completed on attempt 002 after disclosed inspector/collision-search corrections; first attempts remain preserved. All 3,200 final neural states and final fields reconstructed exactly. Nonzero restart and observer non-interference matched. The original world-only preparation was reused after provenance/dependency checks. The paused inspector and its launcher were verified; its server is stopped.

External directional light enters across the arena boundary; interior bodies cast shadows, ambient remains, and walls retain ordinary material/contact behaviour. The closed-wall interpretation is preserved as rejected for this branch. No other law or mechanism changed. No scientific lifetime, cohort, efficacy claim, sweep or commissioning campaign occurred. Capacity, packet limits, tonic centring, fading association, signal scale and fine differentiation remain open. Sources, R, alternatives and historical results are preserved. No vault Git writes or live-index edits occurred.
''')
write(stage/'developmental_ecology/README.md','''# Loom P engineering build

**Bounded engineering verification complete; uncommissioned.** The intact P body/world/organism, records and local inspector are ready for review. Reports are under `../docs/developmental_ecology/p_engineering_20260921/`. No scientific lifetime or developmental claim is implied.

Double-click **Open Loom Inspector.cmd**. It opens paused at time zero with the saved initial **contact_ui_1s** fixture. This is a manufactured engineering contact state, not continuation of your previous UI session. Nothing advances at launch. Native step, Step to wave boundary, Pause and Stop are available. At most one simulated second can be stepped per session; this is not permission for scientific runs.

Use the saved-record slider for the existing one-second case. **Reconstruct selected parameters** rebuilds a detached neural state from saved actual inputs and checks every hash without altering the paused organism. Internal data flow shows the selected saved wave's raw/residual/activity history, exact packet and effective signals. Development shows pooling, association and fixed information-loss calculations. Full history plots use saved replay; live stepping shows endpoint/handoff values. Parameter panels identify snapshot versus reconstructed values.

After extracting the portable package, if the environment is absent, double-click **Setup Loom Inspector.cmd** with Python 3.13 installed. It installs pinned dependencies only in the adjacent `.venv`. The verified host used Python 3.13.5; cross-version/platform bit identity is not claimed. Preserve runtime source bytes: same-code snapshots reject changed code hashes. Only `http://127.0.0.1:8767` is served; no cloud service, model API or remote assets are required.

Full local evidence remains in `artifacts/`. The portable review contains both short-case traces/snapshots, birth snapshots/manifests, source documents and verification results, with failed attempts disclosed. Large routine birth streams remain local and are listed by size/hash in the portable inventory. See BUILD_REPORT.md for 44 component checks, three named smokes, repeats, measured costs and coverage limits.

For maintenance: `python -m pytest tests -q` runs components. `python verify_engineering_records.py` performs detached reconstruction against the full local evidence. The smoke runner permits only the three named cases and refuses to overwrite attempts. This delivery stops at review; no longer life, new case, sweep or tuning is authorized.
''')
print('Final human-readable reports prepared in task staging.')
