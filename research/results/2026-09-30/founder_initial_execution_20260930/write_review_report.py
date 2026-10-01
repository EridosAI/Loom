"""Assemble the review from completed, bounded passive results only."""
import csv
import hashlib
import json
from pathlib import Path
import sys
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
OUT=HERE/'analysis'
sys.path.insert(0,str(ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'))
from loom_developmental.runner import canonical,file_hash,atomic_json

def main():
    rows=json.loads((OUT/'ALL_TWELVE_AB.json').read_bytes())
    seal=json.loads((HERE/'DENOMINATOR_SEALED.json').read_bytes())
    ver=json.loads((HERE/'POSTRUN_VERIFICATION.json').read_bytes())
    archive=json.loads((HERE/'ARCHIVE_VERIFICATION.json').read_bytes())
    deep=json.loads((OUT/'C_WINDOWS_COMPLETE.json').read_bytes())
    def link(label,path):return f'[{label}](<{Path(path).resolve().as_posix()}>)'
    a_lines=[];b_lines=[];s_lines=[]
    for r in rows:
        name=r['life_id'];b=r['B_final'];gap=min(r['min_source_endpoint_gap'])
        contact='wall-2' if name=='FS-002' else 'mover' if name=='FS-010' else 'none'
        a_lines.append(f"| {name} | {r['simulated_seconds']:.6f} | {r['native_steps']:,} | {r['waves']:,} | energy | {r['integrity_final']:.9f} | {contact} | {r['damage']:.9f} | {r['path_length']:.4f} | {r['displacement']:.4f} | {gap:.6f} |")
        b_lines.append(f"| {name} | {b['H_norm']:.6g} | {b['H_use_mean']:.6g} | {b['q_norm']:.6g} | {b['theta_E_norm']:.6g} | {b['theta_I_norm']:.6g} | {b['reference_E_norm']:.6g} | {b['reference_I_norm']:.6g} |")
        s_lines.append(f"| {name} | `{r['authority_sha256']}` | `{r['receipt_sha256']}` |")
    windows=[]
    for w in deep['windows']:
        q=[x for x in w['native_samples'] if 'immediate_controls_omission_delta_norm' in x][-1]
        z=q['immediate_controls_omission_delta_norm'];m=q['immediate_command_omission_delta_norm']
        windows.append(f"| {w['name']} | {w['first_index']}–{w['last_index']} | {q['time']:.2f} | {z['learned_0']:.6g} | {z['learned_1']:.6g} | {z['evoked']:.6g} | {m['motor_evocation']:.6g} | {m['oscillator']:.6g} |")
    cortical=[]
    for m,name in enumerate(('light','chemistry','contact','proprioception')):
        def extent(k):
            xs=[r['B_final'][f'c{m}_{k}'] for r in rows]
            return f'{min(xs):.6g}–{max(xs):.6g}'
        cortical.append(f"| {name} | {extent('shared_birth_delta')} | {extent('fine_norm')} | {extent('shared_ref_birth_delta')} | {extent('fine_ref_birth_delta')} |")
    report=f'''# Founder Search initial-stage report — 30 September 2026

All twelve authorized lives ran exactly once, in FS-001→FS-012 order. All ended through genuine energy nonviability between **429.219307 and 429.948288 simulated seconds**, before the 600-second ceiling. **No life contacted a source or received energy transfer.** There were no administrative cutoffs, unstarted lives, replacements, retries, continuations or shared apparatus failures. The full denominator is 12/12, and all twelve stores passed passive verification.

Internal structure changed and changed regulator banks were expressed later. **Useful developmental regulation was not established in this stage.** This is a bounded result for these twelve blank starts, frozen P and this world; it does not show that P is universally incapable, that sensory access is absent, or that a different population would necessarily fail. No founder ranking or selection was performed.

**Authority, identity and preservation.** Frozen P `{seal['P_commit']}`; lean checkpoint `{seal['checkpoint']}`; worktree `{ROOT/'worktrees/loom-p-b1-minimal-20260929'}`; branch `build/p-developmental-runner-20260929`. No production-code/configuration change or Git write was made. The initial snapshots, their stream IDs 1–12, ordinary blank state, P/configuration/runtime, exact 600-second native deadlines and no-retry/no-continuation scopes passed preflight. Execution-side receipts materialized Jason's authorization without altering the proposed outer objects. The launch packet's historical `PROPOSED_NOT_AUTHORIZED` labels remain preserved; actual authorization is the separate {link('Jason instruction',HERE/'JASON_AUTHORIZATION.md')} and its exact per-case approval receipts.

Full runtime identity: `2fc498951552f53698d70da31f5957e1e208016320c2e27e7dfb20e5e5e7a6ab`. Configuration semantic identity: `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`. Cohort identity: `d1453af1d36fd1fd968f345dec5bfa7ece57e87c84f563d948b1238c7e44e199`. No new prehistory was generated, no old sealed human B1 evaluator state was accessed, and no earlier evidence was modified.

**A — complete physical denominator.** Every row below is complete and verified, with biological terminal status and no administrative censoring. Each began with E=0.70 and I=1.0. In every row source contact episodes, productive episodes, source transfer and repair are exactly zero. Each spent its initial 0.70 energy to numerical accounting precision. Path and displacement are in world units; nearest source gap is body-surface to source-surface distance sampled at native endpoints.

| Life | Observed age (s) | Native steps | Waves | Terminal cause | Final I | Other contact | Damage | Path length | Net displacement | Minimum source gap |
|---|---:|---:|---:|---|---:|---|---:|---:|---:|---:|
{chr(10).join(a_lines)}

The stage contains **{sum(r['native_steps'] for r in rows):,} native steps, {sum(r['waves'] for r in rows):,} completed waves, {sum(r['all_events'] for r in rows):,} physical event records and {sum(r['simulated_seconds'] for r in rows):.9f} simulated seconds**. The final partial native steps and incomplete terminal waves remain recorded. Final E values range from approximately −3.3×10⁻¹⁵ to −1.11×10⁻¹³ under the existing terminal-location arithmetic. They were neither clipped nor continued. These terminal roundoff values are not resource censoring.

Total traveled distance per life was 13.3339–13.9678, while start-to-end displacement was only 0.0236–1.0572. Thus these trajectories accumulated movement with limited net displacement. This statement alone does not establish the maximum excursion or explored area; full native paths remain available. It is not a proof of an inability to move farther.

FS-002 contacted `wall-2` in eight record-defined episodes from 160.807535 to 369.480000 s (native indices 16081–36948; global physical event indices 16082–36971). Total impulse was 0.1819314517 and damage 0.003337815168. FS-010 had mover contact records from 6.928214 to 7.580000 s (native 693–758, event 694–1342), total impulse 0.9152980120 and damage 0.016924086891. The mover interval contains repeated zero-duration touches/releases and 213 fine event-defined contact episodes, including zero-impulse records. Those are solver-level subdivisions, **not 213 independent behavioral encounters**. They are retained unchanged. Contact-flagged native counts are 192 and 61 respectively; no other life has a contact record. Ten final I values remain 1.0; the two injured lives retained positive integrity and ultimately ended through energy.

All eight source stocks stayed at their full 0.2 capacity in every life. There was no stock debit, depletion, renewal gain, restorative repair, departure/recontact with a source, accidental energy benefit or productive source interaction. FS-003, FS-006 and FS-009 entered the descriptive one-world-unit source-gap band; the remaining nine did not at recorded endpoints. FS-006 was closest: gap 0.0303067685 at native 2679, time 26.79 s, source index 0. This was a near approach without contact. Geometric proximity is not a guarantee of a usable route or a perceptual opportunity. The actual raw chemistry coordinates were present and varied; nonzero chemistry by itself does not establish that intact P used it effectively.

Full A data: {link('twelve-row physical table',OUT/'FULL_DENOMINATOR_A.csv')}, {link('complete A/B values',OUT/'ALL_TWELVE_AB.json')}. Per-life `*_contact_episodes.csv` and `*_near_source_intervals.csv` retain native/event/time boundaries. Proximity bands 0.25 and 1.0 are descriptive reporting bands only, not newly introduced viability or success criteria. Original native/event streams are authoritative for all quantities.

**B — internal change across all twelve.** H below is the combined associative-map Frobenius norm; use is the mean of its contribution-dependent use traces. q is the final actual associative return. These are numerical mechanism quantities, not usefulness scores. All H maps and banks started at zero; sensory structure started from the ordinary nonzero anatomy.

| Life | Final H norm | Mean H use | Final q norm | E-bank norm | I-bank norm | E-reference norm | I-reference norm |
|---|---:|---:|---:|---:|---:|---:|---:|
{chr(10).join(b_lines)}

Every completed wave made its declared H write; counts equal the 2,146–2,149 completed waves shown above. Writes, decay and read/use therefore occurred, but associative returns remained small. Across all retained waves the largest whole-q norm was 1.34852×10⁻⁵ and largest motor-packet q norm was 1.37567×10⁻⁶. Mean H-use traces remained on the order of 10⁻¹². Full wave summaries retain H norm/use, q, psi, credit, learned outputs, exploration, pool opening and regulatory support. Full checkpoints additionally retain H arrays, references and eligibility, with last-wave formation/decay/projection operands. Those last-wave operands are **checkpoint samples**, not reconstructed integrated totals for intervening waves.

Sensory changes are separable from transient activity. Final ranges across the full roster are:

| Modality | Shared displacement from birth | Final fine norm | Shared-reference displacement | Fine-reference displacement |
|---|---:|---:|---:|---:|
{chr(10).join(cortical)}

Initial fine norms were 0.00565685425 for light/contact/proprioception and 0.00529150262 for chemistry. They contracted substantially in every life, including contact cortex in lives with no contact. Pool opening reached 0.760866–0.761446 through the existing age-driven relaxation toward one (`loom_p/neural.py`, `Cortex.step`); opening alone is not a learned distinction. The nonzero shared/reference changes, fine contraction and transient activity must not be conflated with a useful sensory representation. Sensory residuals, support and the configured formation/coarsening/reference terms remain alternative explanations for each change.

The E-bank changed in all lives while energy decreased. The I-bank remained exactly zero in the ten uninjured lives and changed in FS-002/FS-010 following injury. This is consistent with the declared separate E/I credit law. Both banks' eligibility traces exist even when a bank receives zero credit. Late nonzero bank outputs and references are retained, but nonzero weight/eligibility norms are not evidence of improved resource interaction. Each bank's exploration-vector norm was 0.346410; the largest learned E-vector norm over the roster was 0.0161198, and the largest learned I-vector norm was 0.00217373. These are pre-need-weighting output norms, not additive shares of behavior.

Full B data: {link('all-life bank/H table',OUT/'FULL_DENOMINATOR_B.csv')}; per-life `*_waves.csv` and `*_checkpoints.csv` include exact native/wave indices, checkpoint hashes, sensory/ref displacements and eligibility. All recorded lives are represented, with no exclusion based on outcome.

**C — bounded later-expression checks.** Only after the full A/B tables were complete, four exploratory windows were declared in {link('window selection',OUT/'C_WINDOW_SELECTION.json')}. Each contains 20 native samples (0.2 s), with saved-input warm-up from the nearest earlier checkpoint. There was no body/world evolution, counterfactual ecological trajectory or feedback into a live organism. Recorded commands, wave outputs and RNG agreed during reconstruction; completed chunk endpoints encountered during warm-up were checked against their sealed P/RNG identities. Non-chunk-ending window endpoints are not claimed to have an independent stored endpoint hash.

The table gives Euclidean changes at each window's ending handoff when the named term is omitted from its immediate receiver. Control-vector deltas combine different control coordinates and have no established behavioral-benefit threshold. Command and control deltas are distinct quantities and should not be compared as interchangeable units.

| Window | Native indices | Handoff time | Controls Δ without E learned | Controls Δ without I learned | Controls Δ without associative feature input | Command Δ without motor evocation | Command Δ without oscillator |
|---|---|---:|---:|---:|---:|---:|---:|
{chr(10).join(windows)}

FS-010 supplies an ordered observation: mover injury at 6.928214 s, I-credit/bank change at the following handoff, then a still-nonzero I learned-output contribution at 429.8 s. The late immediate controls change when the I learned term is removed is 0.000108705. This establishes retained internal change and later expression at that receiver, **not useful injury avoidance or improved survival**. There was no later productive source interaction, and no alternative trajectory was executed. Current reserves, geometry/pose, exploration, direct feedback and the earlier collision remain competing explanations of behavior.

FS-006 is the explicitly included near-source/no-transfer comparison, and FS-001 is the first roster life's late no-contact comparison. In both, local motor associative influence is nonzero but very small at these sampled receivers; sensory-context omission effects on regulator controls are correspondingly tiny or numerically zero. For example, late FS-010 chemistry-context omission changes q by 1.38146×10⁻¹¹ and controls by 3.77788×10⁻¹⁶. Such near-roundoff control differences are not robust evidence of a meaningful behavioral effect. They do not prove all associative influence is always absent. In these selected windows, oscillator/noise/direct regulatory terms exert much larger immediate influence than associative motor evocation.

These probes do not isolate the value of accumulated sensory plasticity against a birth-structure counterfactual, and no such extra assay was run. Lasting sensory structural contribution to useful behavior remains unresolved. History-dependent regulatory expression is observed locally; history-dependent regulatory **benefit** is not established. No useful A→B→C developmental witness is demonstrated by this initial stage.

Exact window outputs and their lossless deep records: {link('C results',OUT/'C_WINDOWS_COMPLETE.json')}. Exactly four windows / 80 requested native samples were used. Warm-up reproduces recorded P input processing only and is not another world life. No additional windows, ranking, founder score or continuation selection were performed.

**Custody and resources.** Preflight took {seal['preflight_wall_seconds']:.6f} s total against 120 s. One worker executed the twelve lives in {seal['active_execution_wall_seconds']:.6f} active wall seconds ({seal['active_execution_wall_seconds']/60:.3f} minutes), against 3,984 s; per-life times were {min(r['active_wall_seconds'] for r in rows):.3f}–{max(r['active_wall_seconds'] for r in rows):.3f} s, each below 332 s. Closed life stores total {seal['closed_life_bytes']:,} bytes; each is below 83,333,333 bytes. Peak working set was {seal['final_process_memory']['peak_working_set_bytes']:,} bytes and peak process commit {seal['final_process_memory']['peak_commit_bytes']:,} bytes, below the plan's 500 MB / 2.5 GB figures.

Post-run validation took {ver['wall_seconds']:.6f} s against 180 s. Every store passed, and the maximum single-event energy/stock/integrity accounting residual was 5.551115123125783×10⁻¹⁷ (configured tolerance 10⁻¹²). No record tail was missing or unsealed. Archive write/member verification took {archive['archive_wall_seconds']:.6f} s; it contains {archive['verified_members']:,} hash-verified data members plus its manifest, totaling {archive['bytes']:,} bytes. Input/metadata custody and archive preparation timing are separately retained in the delivery verification.

The **single planned archive** is {link('Founder Search initial-stage results',Path(archive['path']))}. SHA-256: `{archive['sha256']}`. It contains all twelve native/wave/event stores and complete checkpoints, exact starts/prehistory, authority/approval provenance, frozen source/configuration/runtime identities, the sealed denominator, verification and outer execution/analysis scripts. `execution/VERIFY_ARCHIVE.py` is a portable standard-library, read-only byte verifier. `EVIDENCE_ARCHIVE_MANIFEST.json` governs this results archive. The nested launch packet's historical package manifest describes its separately preserved earlier package and does not replace the results manifest. Passive analyses are delivered separately and linked to this archive hash; no second full evidence archive was created.

**Remaining issues and limits.** These lives provide no source-contact, transfer, renewal/revisit or productive-development witness. The local expression checks do not establish learned competence, useful sensory restructuring or globally negligible associative influence. No learned-versus-unlearned physical comparison was run. No environmental or mechanism cause was isolated by intervention. Fine contact subdivisions, floating terminal residuals and all misses/damage remain in the evidence; none was patched or relabeled. The small population and approximately 429-second actual lifetimes bound any conclusion.

No live Tier-2/D5, plotting, scoring or outcome analysis occurred during execution. No extra birth, replayed world, retry, rewind, replacement, controller, tuning, P/world/nursery change, additional population, 900/1,800-second extension, continuation authority, C1/C2 commissioning, new perceptual assay, push, PR or merge was performed. The four C-labelled windows above are passive analysis-plan C illustrations, not the separate commissioning C1/C2 stages. The session stops for Jason's review.

**Exact per-life authority and final receipt identities.** Complete causal endpoint/checkpoint/file identities are also in the sealed records and verification file.

| Life | Authorized outer SHA-256 | Sealed segment receipt SHA-256 |
|---|---|---|
{chr(10).join(s_lines)}

Primary references: {link('sealed full denominator',HERE/'DENOMINATOR_SEALED.json')}; {link('preflight',HERE/'PREFLIGHT.json')}; {link('post-run verification',HERE/'POSTRUN_VERIFICATION.json')}; {link('archive verification',HERE/'ARCHIVE_VERIFICATION.json')}; {link('reporting method',HERE/'REPORT_METHOD.md')}; the unchanged launch packet `EXECUTION_PROTOCOL.md`, `ANALYSIS_PLAN.md` and `RESOURCE_PLAN.json`.
'''
    target=HERE/'FOUNDER_SEARCH_INITIAL_STAGE_REPORT.md'
    with target.open('x',encoding='utf8') as f:f.write(report)
    atomic_json(OUT/'PASSIVE_ANALYSIS_COMPLETION.json',dict(
        total_wall_elapsed=time.perf_counter()-json.loads((OUT/'ANALYSIS_CLOCK.json').read_bytes())['monotonic_started'],
        analysis_budget_seconds=900,derived_bytes=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file()),
        derived_budget_bytes=500000000,full_denominator=12,deep_windows=4,requested_deep_native_samples=80,
        ecological_steps_after_stage=0,new_lives=0,continuations_prepared=0,founder_scores=0,
        report_sha256=file_hash(target),archive_sha256=archive['sha256']))
    print(target)

if __name__=='__main__':main()
