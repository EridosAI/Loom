from pathlib import Path
from urllib.parse import quote
import json
ROOT=Path(__file__).resolve().parent
plan=json.loads((ROOT/'PLAN.json').read_text(encoding='utf-8'))
S,B,R=plan['session'],plan['batch'],plan['record']
IDX='30_REVIEWS/DEVELOPMENTAL_EVIDENCE_INDEX_2026-10-01_7c219ab4.md'
DEC='40_DECISIONS/DECISION-DEVELOPMENTAL-DIRECTION-2026-10-01-7c219ab4.md'
def write(rel,text,group='NEW'):
 p=ROOT/group/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8',newline='\n')
def src(g,n,label=None):return f'[{label or n}](../../{B}/{quote(g+"/"+n)})'
def note(n,label):return f'[{label}]({n}.md)'
prior='50_SESSIONS/2026-09-26-b1-final-review-intake-f04e8c72/FINAL_B1_OPERATOR_APPARATUS_REVIEW_RECORD.md'
a5='50_SESSIONS/2026-09-26-a5-evidence-intake-82b4d9e1/A5_COMMISSIONING_EVIDENCE_RECORD.md'
classification='''**Classification:** OBSERVED EXPERIMENTAL EVIDENCE includes bounded commissioning and explicitly qualified passive analyses. JASON-ACCEPTED DECISIONS / DIRECTIONS are recorded separately. Assistant/build proposals and unresolved interpretations are not canon. This integration performs no scientific execution or reanalysis.'''

write(S+'/01_COMMISSIONING_AND_RUNNER.md',f'''# Commissioning continuation and lean runner

{classification}

The [26 September integration](../../{prior}) already recorded final B1 operator-apparatus closure at `352f73fffa6d9781eae8aa38e708a9a05669588f`. [A0–A5 physical-ceiling evidence](../../{a5}) was already integrated and remains unchanged within its bounded witness set. No historical checkpoint is relabelled as having used later code.

## B1 minimal perceptual closure — observed, 29 September

The later **minimal S1 rule is satisfied** under apparatus `a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad`: a permitted-sensory external controller's preserved S1-FULL witness produced source contact and 0.05230330252357774 transfer; the paired S1-SENSORY-FREE case completed 30 s / 3,000 native steps with fixed `(0.30,0.30)` commands, no controller input and zero source transfer. Both had the same complete initial state. FULL remains at its original 29.79 s / 2,979-step wall cutoff, with its pending final hold preserved. It was not extended to make durations equal. These totals are not an equal-duration efficiency comparison.

The bounded claim is that a fixed external controller using permitted sensory history produced productive source interaction under the held-out start. **P was inactive.** This establishes no P learning, recognition, chemistry necessity, general navigation or survival competence. The minimal pair does not retroactively complete the original human FULL-RAW/CHEMISTRY-HIDDEN protocol. S1-HIDDEN, S2 and S3 remained unexecuted in this closure; no new B2–B4 or C1/C2 result was located. Human competence is not established by this external-controller result.

Sources: {src('b1','B1_MINIMAL_CLOSURE_REPORT.md','bounded paired report')}, {src('b1','PAIRED_CLOSURE_RESULTS.json','exact comparison')}, {src('b1','FULL_COMPANION.json','preserved FULL companion')}, {src('b1','USER_AUTHORIZATION.md','single-case authority')}. Its exact authority was `57386e964ea018050bedc18a397e4611203926626e4363c2c9b04d79c9fc5ba2`. The old held human evaluator material remains sealed and untouched.

## Lean developmental runner — engineering evidence

Checkpoint `87abae34e19d4e46234402a6b1ba776814956ec1`, parent `a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad`, introduced a separate lean recorder/runner. Frozen P, commissioning code and configuration were preserved. Matched short engineering execution was reported 17.41× faster and 3.87× smaller including boundary costs; the one 600-second engineering fixture completed in 204.12 wall seconds. These fixture-specific measurements do not establish scientific benefit or universal performance.

The source reports 14 release checks and exact causal-state comparisons, including split continuation and saved-input reconstruction, allowing only the redundant observer cache difference. Failure/codec history and limits remain in the source. No test is rerun by this intake. Sources: {src('runner','DEVELOPMENTAL_RUNNER_OPTIMIZATION_REPORT.md','engineering report')}, {src('runner','CHECKPOINT.json','checkpoint identity')}, {src('runner','EQUIVALENCE_AND_CONTINUATION.md','equivalence and limitations')}.

The subsequent Founder Search is actual intact-P evidence under separately recorded authority, not another engineering fixture. [Founder evidence](02_FOUNDER_SEARCH.md).
''')
write(S+'/02_FOUNDER_SEARCH.md',f'''# Founder Search — fixed 60-life evidence

**OBSERVED EXPERIMENTAL EVIDENCE.** Fixed roster **FS-001–FS-060**; **59 complete ordinary lives plus FS-060 apparatus-interrupted prefix**. Useful developmental learning was **NOT ESTABLISHED**. No founder was selected.

P baseline `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; lean runner `87abae34e19d4e46234402a6b1ba776814956ec1`; runtime `2fc498951552f53698d70da31f5957e1e208016320c2e27e7dfb20e5e5e7a6ab`. These identities come from preserved reports and verification metadata. Later contact-correction and M1 runtimes are separate branches of evidence.

The first twelve lives ran once each and all ended in genuine energy nonviability before the 600-second ceiling, without source contact or transfer. The separately authorized 48-life expansion started FS-013–FS-060 once each. Combined complete endpoints occurred at about 428.875–430.843 s. **Only FS-034 received source energy:** 0.0017489243594212861; its eight following E-credit handoffs remained negative. Its 103 contact fragments/episodes in the original account are not independent developmental discoveries. Ordinary current-world source opportunity was extremely poor under the original spontaneous motor process.

FS-060's durable prefix ends at native 12,400 / 124.00000000002653 s; its last complete causal checkpoint is native 12,000 / 120.00000000002449 s. Its unknown tail remains unknown. It has no fabricated terminal or closure receipt and is not counted as a biological failure, complete life or zero-exposure endpoint. The worker termination cause remained unresolved; it is not automatically the same cause as the later RS-M1-008 crash.

The final report supersedes the intermediate report's incomplete analysis-coverage wording: all 60 entries have A/B saved-record coverage with the prefix labelled; all 32 selected C windows completed; 59/59 complete lives passed the reported full saved-input P checks. Internal structure and later regulatory expression changed, but numerical change does not establish useful learned control. No physical counterfactual or founder selection is added by this integration.

Sources: {src('founder12','FOUNDER_SEARCH_INITIAL_STAGE_REPORT.md','initial 12-life report')}; {src('founder60','FOUNDER_SEARCH_60_LIFE_FINAL_REPORT.md','final fixed-roster report')}; {src('founder60','FOUNDER_SEARCH_60_LIFE_REPORT.md','preserved intermediate report')}; {src('founder60','INTERRUPTION_NOTE.md','FS-060 custody boundary')}; {src('founder60','analysis/FS034_INTERPRETATION.md','FS-034 interpretation')}; {src('founder60','FINAL_DELIVERY_VERIFICATION.json','final verification')}. Initial and expansion authorities retain their exact per-case hashes in the respective {src('founder12','JASON_AUTHORIZATION.md','12-life')} and {src('founder60','JASON_AUTHORIZATION.md','48-life')} authorization records. [External archive identities](EXTERNAL_EVIDENCE.md).
''')
write(S+'/03_INTEGRITY_DEVELOPMENT.md',f'''# Integrity development — observed pathway, unresolved benefit

**OBSERVED EVIDENCE / PASSIVE ANALYSIS.** Integrity consequences demonstrably entered persistent learned state in the nine damaged Founder Search lives. Damage precedes negative I-credit, eligibility-driven I-bank changes, retained parameters/references and later learned-I output. Saved-state omission at a fixed motor receiver produces measurable immediate command/regulatory differences. This is more than a changed parameter norm; it remains weaker than demonstrated beneficial physical causation.

**FS-015 is a bounded possible softening candidate.** Later contact speeds and local learned-I signs support examining that interpretation, but contact two had greater total impulse than the first, the third-to-fourth collision worsened, and E, mover phase and body orientation differed. **FS-017 is a bounded possible avoidance candidate:** a later near miss and greater clearance align with local less-into-surface influence, but there is only one realized contact history. Neither is an accepted founder or proved learned benefit.

Mixed/adverse evidence is retained. FS-002's softer individual impacts coexisted with more later contact and aggregate damage. FS-010 had separation with mixed learned-I directions. FS-044's repeated contacts grew harder. The other damaged lives remain in the denominator. Small one-receiver effects neither prove useful long-run control nor rule out cumulative effects.

The analysis covered 192 specified windows using saved-input P reconstruction and frozen-receiver algebra; it ran no alternative physical trajectory. Its 26 behavioural episodes and 28 temporal bouts are explicit groupings, with sensitivity checks, not raw solver fragments promoted to experiences. Beneficial learned causation remains **UNPROVEN**.

Sources: {src('integrity','IMPACT_INTEGRITY_DEVELOPMENT_ANALYSIS_v0_1.md','complete analysis')}, {src('integrity','METHODS.md','methods')}, {src('integrity','DESCRIPTIVE_CLASSIFICATIONS.csv','all classifications')}, {src('integrity','PASSIVE_LEARNED_I_OMISSIONS.csv','signed local omissions')}, {src('integrity','FINAL_VERIFICATION.json','verification')}. This is later analysis of the same immutable Founder Search evidence, not new lives or a retest.
''')
write(S+'/04_EXPLORATION_AND_BIRTH.md',f'''# Exploration dynamics, birth geography and proposed alternatives

**OBSERVED EVIDENCE / PASSIVE AUDITS.** Across 59 complete ordinary lives, median path length was 13.6558 world units, maximum excursion 0.5327 and final displacement 0.2924. The median sustained forward/reverse switch count was 94; typical signed bouts lasted about 3.4 s; quarter-unit-cell re-entry was 92.96%. The animals moved substantially but explored little. Repeated cancellation of translation along a persistent body heading was the leading kinematic limitation. This descriptive evidence did not alone isolate the generator from feedback, body mechanics or regulation.

Birth geography was already broadly distributed: all 16 coarse cells and 22/25 finer cells held births; the examined close-pair counts were near the conditional uniform expectation. Thus the cohort was not all born together or in a corner. Broad population coverage does not repair each individual's limited reach. The unusually low rejected-proposal count is retained as an exploratory observation, not a proved sampling defect or a reason to reroll births. FS-060 remains a separate prefix for whole-life comparisons.

Sources: {src('exploration','NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md','exploration audit')}, {src('exploration','EXPLORATION_PER_LIFE.csv','per-life exploration')}, {src('birth_motor_design','BIRTH_GEOGRAPHY_AUDIT_v0_1.md','birth audit')}, {src('birth_motor_design','REVIEW_VERIFICATION.json','audit verification')}.

**ASSISTANT / DESIGN PROPOSALS.** {src('exploration','NURSERY_0_DESIGN_v0_1.md','Nursery-0')} retains N0-A/N0-B/N0-C as provisional alternatives; the {src('birth_motor_design','NEWBORN_SPONTANEOUS_MOTOR_DESIGN_REVIEW_v0_1.md','newborn motor review')} retains CURRENT and the M1/M2 families without selecting a replacement. Prospective stratified births are also unselected. No nursery geometry, source density, birth reserve, basal cost, impact resilience or repair change is ratified here. The complete proposals are preserved, not merged into a third design or silently reduced to M1.

The motor review distinguishes blind endogenous temporal organisation from source seeking, a novelty reward or semantic actions. Altering the spontaneous process is a declared mechanism variation, not an apparatus-only optimization. [Corrected motor screen](05_MOTOR_COMMISSIONING.md) provides later bounded evidence; [current open questions](../../02_OPEN_QUESTIONS.md) keeps M1's future role and Nursery-0 sizing unresolved.
''')
write(S+'/05_MOTOR_COMMISSIONING.md',f'''# Corrected motor commissioning v0.2

**OBSERVED COMMISSIONING EVIDENCE.** Corrected apparatus checkpoint `1d7cd6fd450ea528562b2c825589ab4de18a5b38`; runtime `5df0ced8bf5602c84852bc2074fca8d422cc39cc55b9bab00a4b653bbe714c49`. All nine CURRENT/M1/M2 cases at matched FS-001/002/003 starts completed once at 90 s / 9,000 native steps, with no retry, continuation or candidate tuning.

M1 showed greater reach and lower recurrence in all three starts without greater **aggregate** effort or contact. This does not mean every individual metric or effort value was equal across arms. CURRENT maximum excursions were approximately 0.400/0.376/0.600; M1 approximately 1.059/2.159/3.382. M1's quarter-unit-cell re-entry fractions were approximately 0.143/0.143/0.032 versus CURRENT 0.833/0.826/0.800. These are bounded single-draw comparisons, not population guarantees or pass gates.

M2 was more variable and contains material impact confounds, especially FS-001 mover interaction. Food contact or raw reach is not a motor-selection score. **M1 was NOT selected as canonical Loom mechanism; CURRENT remains the reference.** Neither the screen nor its later sandbox use establishes useful developmental learning.

## Apparatus history retained

The v0.1 screen stopped after two completed cases and a 10.25 s MC-FS-001-M2 prefix; six cases were unstarted. Its guard detected an inadmissible free-path release. The later correction handles a narrowly certified flat-face-to-corner feature transition while retaining the penetration guard. v0.2 is a fresh common-apparatus comparison, not a continuation or replacement of v0.1.

The corrected body/P package digest `98bbf9053ca55ef545c6fc868e54c85342149d143319281a47f9a1fd71c28c7d` differs from the old `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9` because of the disclosed physical contact correction, not P neural-learning changes. Configuration identity remains `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a`. Do not say all implementation bytes remained identical across these checkpoints.

Sources: {src('motor_v02','MOTOR_COMMISSIONING_RESULT_v0_2.md','complete v0.2 result')}, {src('motor_v02','FINAL_VERIFICATION.json','verification and exact identities')}, {src('motor_v02','AVAILABLE_CASE_METRICS.csv','all metrics')}, {src('motor_v01','MOTOR_COMMISSIONING_RESULT_v0_1.md','historical interrupted v0.1')}, {src('contact_correction','APPARATUS_ROOT_CAUSE_AND_CORRECTION.md','contact correction')}, {src('motor_v02','JASON_AUTHORIZATION.json','exact nine-case authorization')}. No screen, regression or engineering replay was run by this integration.
''')
write(S+'/06_M1_RESURRECTION_SANDBOX.md',f'''# NON-CANONICAL RESURRECTION SANDBOX

**OBSERVED SANDBOX EVIDENCE — apparatus-interrupted, no retry.** Runtime `752b7c335347a5f55fd3e7cdf1b904137d41e5b229b8ea2252caa8e12a455f3c`, based on corrected apparatus `1d7cd6fd450ea528562b2c825589ab4de18a5b38`. It is distinct from motor-screen runtime `5df0ced8bf5602c84852bc2074fca8d422cc39cc55b9bab00a4b653bbe714c49` and from ordinary Founder Search.

Exact sandbox M1: **amplitude 0.35; zero-mean stationary Gaussian common/differential latents; SD 0.5; OU time constants 16 / 8 s; refresh every 50 accepted native calls.** M1 is not selected as canonical Loom mechanism.

| Fixed denominator | Recorded disposition |
|---|---|
| All 12 individuals | Reached 600 s |
| RS-M1-001–007 | Completed 4,500 s |
| RS-M1-008 | Durable physical/native evidence to 2,968.9548705465913 s (native 296,900); last complete causal checkpoint 2,939.9548705459583 s (native 294,000) |
| RS-M1-009–012 | Remain at 600 s; overnight stages unstarted |

The native Windows/Python memory-read failure triggered the declared stop. No retry, replacement, unknown-tail synthesis or scientific continuation occurred. The durable endpoint is **not a full restart state**; the in-flight state and exact crashing call are unavailable. The recorded Windows Application Popup identifies a memory-read error, not the responsible native module, exception code or proven root cause. Those remain an engineering question; do not label a P/world defect or a specific Python-library bug.

## Support intervention and learned-state continuity

At genuine terminal boundaries only the nonviable reserve was restored (E to 0.70 or I to 1.0). There was no relocation, source refill, clock rewind, field regeneration or replacement birth. Declared mean/trace/unfinished-packet transients quarantined the intervention from ordinary learning credit. No bank/map handoff occurred at the support jump. Long-term learned banks/references/eligibility, H/use, sensory structures, world, M1 and RNG continuity were preserved and checked. The discarded incomplete packet also lost its ordinary handoff contribution, while physical observations remained recorded; quarantine is not cost-free.

Across available exposure there were 77 energy-terminal restorations and no integrity-terminal restoration. External energy support (53.90 units) remains separate from source intake (about 2.34214). This is supported longevity, not ordinary viability or self-maintaining source exploitation.

## Bounded observations and limits

Long supported histories produced repeated energy/integrity experience and substantially more internal learned-state change. All seven long completers had productive source contact. Contact fragments are grouped explicitly (84,350 raw fragments versus 103 descriptive bouts across available exposure); neither count equals independent learned discoveries. Later contact duration/productivity and integrity outcomes are mixed, not monotonically improving.

Learned motor-current expression grew but remained small relative to M1 (late RMS roughly 0.22–1.15% of M1 input in the seven completers). Associative use/read-to-motor influence stayed very small. Fine sensory norms contracted strongly, while some matrix shapes changed; this is not evidence that the entire sensory cortex collapsed. Temporal event → internal change → later useful interaction candidates exist, but learned physical causation remains unresolved. **Useful learned navigation was NOT ESTABLISHED.**

Sources: {src('sandbox','SANDBOX_REPORT.md','complete sandbox report')}, {src('sandbox','FINDINGS.md','bounded findings')}, {src('sandbox','DEVELOPMENTAL_QUESTIONS.md','detailed developmental analysis')}, {src('sandbox','HOST_FAILURE_REPORT.md','host-failure boundary')}, {src('sandbox','HOST_STOP_DENOMINATOR.json','exact interrupted denominator')}, {src('sandbox_preparation','JASON_OVERNIGHT_AUTHORIZATION.txt','historical sandbox authorization')}, {src('sandbox_preparation','BATCH_AUTHORITY.json','exact batch authority identities')}.

The **4,653,285,580-byte archive remains outside Obsidian**. Its exact path, SHA-256 and copied manifest are in [external custody](EXTERNAL_EVIDENCE.md). No raw evidence was duplicated. This intake authorizes no restart, engineering replay, causal ablation, motor selection, world change or new experiment.
''')

interpretation='''**CURRENT DISCUSSION-LEVEL WORKING INTERPRETATION — not canonical repository doctrine.** The original current-world shortfall was substantially an experience-acquisition / motor-organisation problem. M1 showed that blind coherent spontaneous activity can expose the same organism to much more of the existing world without simply increasing effort. Once repeated experience was available, P accumulated substantially more internal learned state, but this did not establish self-maintaining source exploitation or useful learned navigation. The question moves downstream: **does accumulated learned state materially and causally alter useful physical behaviour, and, if not, where is that influence being lost?** Jason has agreed with this broad discussion direction in the current instruction. This is not proof that M1 is correct or P is incorrect.'''

external='# External evidence archives — exact custody, not duplicated\n\nAll nine archives remain at their original locations. This intake recomputed their whole-file SHA-256 and sizes and matched the exact archived manifest bytes. It did not rerun their scientific validators or recheck every raw payload. Original verification receipts remain sources.\n\n'
for a in plan['archives']:
 external+=f"## {a['role']}\n\n- Exact path: [{a['original_filename']}](<{a['path'].replace(chr(92),'/')}>)\n- Bytes: {a['bytes']:,}\n- SHA-256: `{a['sha256']}`\n- Manifest: [preserved exact copy](../../{a['manifest_path']})\n- Manifest SHA-256: `{a['manifest_sha256']}`\n- Archive member: `{a['manifest_archive_member']}`\n- Original receipt: `{a['original_receipt']}`\n\n"
external+='The resurrection package is prominently NON-CANONICAL RESURRECTION SANDBOX. Its archive has not entered the vault, source batch, backup or export. If external files move, these paths will require explicit relocation/custody reconciliation; no copied manifest substitutes for the complete evidence.\n'
write(S+'/EXTERNAL_EVIDENCE.md',external)

write(DEC,f'''# Recorded developmental directions and bounded historical authorities

**Registered 1 October 2026. Real Jason directions only; no new execution authority.** This record distinguishes historical authorization from current interpretation and proposal.

| Jason ruling / authority | Source and bounded scope |
|---|---|
| Legitimately acquired developmental state may be continued, checkpointed or branched; research selection is not a reward/input to the organism | [29 September clarification](../{B}/direction/JASON_DEVELOPMENTAL_SELECTION_CLARIFICATION.md). External pretraining/authored competence remains excluded. Exact lineage-derived retain/reset choices remain undecided. |
| Founder Search design timing 600 → 900 → 1,800 seconds total age | [Timing ruling](../{B}/founder_design/JASON_TIMING_RULING.md). Timing selection was not execution permission; subsequent ordinary lives did not automatically reach or continue to later stages. |
| Single sensory-free B1 closure case | [Exact authorization](../{B}/b1/USER_AUTHORIZATION.md), preserving the earlier FULL witness. No chemistry-necessity or P-learning acceptance. |
| Initial twelve and forty-eight expansion lives | [Initial authorization](../{B}/founder12/JASON_AUTHORIZATION.md), [expansion authorization](../{B}/founder60/JASON_AUTHORIZATION.md). Exact per-case identities and one-attempt limits remain in those sources; fixed denominator 60. |
| Corrected nine-case motor screen | [Exact authorization](../{B}/motor_v02/JASON_AUTHORIZATION.json). No automatic motor selection, tuning or continuation. |
| Isolated M1 resurrection sandbox | [Historical authorization](../{B}/sandbox_preparation/JASON_OVERNIGHT_AUTHORIZATION.txt), [batch identities](../{B}/sandbox_preparation/BATCH_AUTHORITY.json). Explicitly non-canonical; bounded pilot/continuation and declared failure stop, not a canonical mechanism decision. |
| Broad current research direction | [Current user instruction](../{B}/authority/Pasted%20text.txt), section CURRENT WORKING INTERPRETATION. Record as discussion-level direction with Jason's agreement, not canon or proof. |

{interpretation}

No new numerical dial, Nursery-0 geometry, motor replacement, curiosity mechanism, founder selection, causal-ablation design or scientific continuation is accepted by this record. M1/M2 and N0-A/B/C remain proposals/variants under their own scope. The pasted request's separate native-failure investigation brief remains a build-task handoff; it is preserved but not executed or sent to another task by this integration.
''')

summary='''| Evidence line | Current bounded disposition |
|---|---|
| P engineering / physical A0–A5 | Previously verified / bounded physical ceiling exercised; retained history |
| B1 minimal S1 perceptual closure | Satisfied by productive permitted-sensory FULL and completed unproductive sensory-free pair; P inactive |
| Ordinary Founder Search | Fixed FS-001–FS-060: 59 complete lives plus FS-060 interrupted prefix; only FS-034 received source energy |
| Integrity pathway | Persistent learned-I state and later local output influence observed; useful physical causation unproven |
| Exploration / births | Substantial movement with little reach; reversal cancellation led; births already broadly distributed |
| Motor screen v0.2 | Nine 90 s cases complete on corrected common apparatus; bounded M1 reach/recurrence improvement; M2 impact confounds |
| M1 resurrection sandbox | NON-CANONICAL; twelve 600 s pilots, seven 4,500 s completers, RS-M1-008 interrupted, four remain at 600 s |
| Useful developmental learning / learned navigation | NOT ESTABLISHED; internal change and experience are not proof of useful learned causation |'''
gap=[
('1. Completed P engineering / commissioning continuation','Already integrated through B1 operator-apparatus closure; later minimal B1 and lean runner added','01_COMMISSIONING_AND_RUNNER'),
('2. Physical commissioning through A5','Already integrated; linked without duplicating or relabelling evidence','01_COMMISSIONING_AND_RUNNER'),
('3. B1 minimal perceptual closure','New later bounded S1 pair; distinct from old human chemistry-hidden protocol','01_COMMISSIONING_AND_RUNNER'),
('4. Lean developmental runner','New engineering optimization / identity / limits','01_COMMISSIONING_AND_RUNNER'),
('5. Initial 12-life Founder Search','New ordinary evidence; twelve complete energy-terminal lives','02_FOUNDER_SEARCH'),
('6. 48-life expansion / fixed 60','New fixed-denominator final analysis; interrupted FS-060 retained','02_FOUNDER_SEARCH'),
('7. Impact/integrity analysis','New passive pathway evidence with unresolved beneficial causation','03_INTEGRITY_DEVELOPMENT'),
('8. Exploration audit','New passive kinematic evidence','04_EXPLORATION_AND_BIRTH'),
('9. Birth-geography audit','New passive broad-coverage finding; stratification unselected','04_EXPLORATION_AND_BIRTH'),
('10. Newborn motor design review','New design proposals; full M1/M2 and nursery alternatives preserved','04_EXPLORATION_AND_BIRTH'),
('11. Corrected motor commissioning v0.2','New common-apparatus screen; v0.1 interruption and correction retained','05_MOTOR_COMMISSIONING'),
('12. M1 resurrection sandbox','New NON-CANONICAL interrupted supported-history evidence; archive external','06_M1_RESURRECTION_SANDBOX')]
rows='\n'.join(f'| {a} | {b} | [{c}]({c}.md) |' for a,b,c in gap)
write(R,f'''# Developmental Ecology evidence catch-up — 1 October 2026

**Integration complete through the supplied 1 October evidence.** Continue from the workbench's last integration, not from a new setup. The last registered event was `2026-09-26-b1-final-review-intake-f04e8c72`, ending at SRC-378. A0–A5 and the earlier engineering reviews were already present. The source register now adds SRC-379–SRC-{378+len(plan['source_entries']):03d} in this one dated session.

{summary}

## Gap-aware continuation

| Requested line | Integration action | Review note |
|---|---|---|
{rows}

## Authority, interpretation and source hierarchy

{classification}

Use exact committed/checkpoint-identified source and verified artifact provenance first; Current State orientation next; later verified artifacts over older retrospectives. The local `00_LOOM_CURRENT_STATE(2).md` and contact-correction worktree's orientation are dated foundation documents, not a complete present-day result register. No current remote/repository HEAD claim or Git audit was made. The source archives identify their exact runtime/checkpoint boundaries; the corrected contact code is not misrepresented as byte-identical historical P.

{interpretation}

[Recorded Jason decisions/directions](../../{DEC}) cites the current pasted instruction and historical authorization files. **ASSISTANT / BUILD PROPOSALS:** M1/M2 motor designs, N0-A/B/C nursery designs, prospective birth stratification, and any later physical learned-state ablation remain unselected or undesigned beyond their explicit source scope. **UNRESOLVED INTERPRETATIONS:** useful learned physical causation, source-specific E regulation, associative/sensory usefulness, adequate control magnitude and native-crash cause remain open. [Live questions](../../02_OPEN_QUESTIONS.md).

## Exact custody and validation

Preserved **{len(plan['batch_inventory'])} small source/report/metadata files** ({sum(e['bytes'] for e in plan['source_entries'] if e['storage']=='byte-identical-small-file-copy'):,} bytes); registered **nine complete archives externally**. Whole-archive hashes/sizes were recomputed and exact manifest copies matched to archive members. **The 4,653,285,580-byte resurrection archive was not copied into Obsidian.** [Exact external paths and hashes](EXTERNAL_EVIDENCE.md) · [All source identities and original manifest matches](SOURCE_IDENTITIES.json).

Selected reports/metadata were checked against their original manifest/verification declarations where present ({len(plan['manifest_checks'])} matches). Self-describing receipts and the current user instruction additionally have fresh custody hashes; the intake does not pretend each receipt self-hashes. The final 60-life report is a later derived report, distinct from its preserved intermediate report and unchanged scientific archive. Analysis scripts and reproduction instructions were treated as data and never run.

Read all required live entry/index notes, current source catalog/register and last integration report before changes. Updated eight live shared files: AGENTS.md, 00_RESEARCH_MAP.md, 01_WORKSPACE_STATUS.md, 02_OPEN_QUESTIONS.md, CAND-P.md, DECISION_INDEX.md and source register/catalog. Added six concise evidence reviews, a review index, one direction/authority record and this session's custody/report files. [Before/after shared hashes](INTEGRATION_CHANGES.json), [validation](VALIDATION.json) and SHARED_BEFORE preserve the exact prior shared notes. Previous sources/reviews/decisions/sessions and all complete candidate originals remain unchanged.

## Gaps and work deliberately not performed

No necessary report or manifest for the twelve requested evidence lines was missing. The FS-060 and RS-M1-008 unknown in-flight tails remain genuine evidence gaps; neither was synthesized. No new B2–B4/C1/C2 outcome was found in this catch-up, and the old human B1 evaluator remains sealed. No whole raw-payload or scientific-validator rerun is claimed; archive identity plus supplied verification records bounds this intake.

The separate appended native-failure brief was preserved with the user request as a **build-task handoff only**. No Windows forensic collection, engineering replay, stress run, debugger setup, root-cause diagnosis or fix was undertaken here. The existing OS observation was registered; it does not identify a faulting module or prove a specific exception code.

No canonical repository document, P/world/motor law, numerical dial, scientific evidence, held packet, sealed evaluator state, other vault folder, Atlas database or vault setting was changed. No scientific simulation, new experiment number, Git operation, external publication or message to another task occurred. Useful learning remains unestablished; M1 remains non-canonical. Stop after integration and validation.
''')

idx=f'''# Developmental evidence review index — 1 October 2026

Navigation wrappers for exact existing evidence; no mechanism selection or canon update. [Integration report](../{R}) · [P candidate](../20_CANDIDATES/CAND-P.md) · [Source register](../SOURCE_REGISTER.md).

'''
for n,title in [('01_COMMISSIONING_AND_RUNNER','Commissioning and lean runner'),('02_FOUNDER_SEARCH','Fixed 60-life Founder Search'),('03_INTEGRITY_DEVELOPMENT','Integrity pathway and benefit limits'),('04_EXPLORATION_AND_BIRTH','Exploration, birth geography and full proposals'),('05_MOTOR_COMMISSIONING','Corrected motor screen v0.2'),('06_M1_RESURRECTION_SANDBOX','NON-CANONICAL resurrection sandbox')]:idx+=f'- [{title}](../{S}/{n}.md)\n'
idx+='\nEarlier exact-checkpoint engineering reviews and all original candidate/report families remain unchanged.\n'
write(IDX,idx)

nav=f'''## Current developmental evidence — 1 October 2026

{summary}

**M1 is NOT canonical Loom mechanism.** The resurrection sandbox remains explicitly NON-CANONICAL, with external support separated from ordinary source energy and learning credit. No complete state exists at RS-M1-008's final durable row; no retry occurred. Motor apparatus `1d7cd6fd450ea528562b2c825589ab4de18a5b38`; screen runtime `5df0ced8bf5602c84852bc2074fca8d422cc39cc55b9bab00a4b653bbe714c49`; sandbox runtime `752b7c335347a5f55fd3e7cdf1b904137d41e5b229b8ea2252caa8e12a455f3c`.

{interpretation}

[Integration report]({R}) · [Evidence review index]({IDX}) · [Current open questions](02_OPEN_QUESTIONS.md) · [Exact external archive custody]({S}/EXTERNAL_EVIDENCE.md) · [Jason's scoped directions]({DEC}). Earlier sections below retain their dated status; “untested/unexecuted” there does not override the later bounded evidence above. The original human B1 held protocol remains separate from the later minimal S1 closure. No B2–B4/C1/C2 closure is inferred.

'''
for n in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
 t=(ROOT/'SHARED_BEFORE'/n).read_text(encoding='utf-8-sig');first,rest=t.split('\n',1)
 rest=rest.replace('## Current commissioning boundary — B1 apparatus closure, 2026-09-26','## Preserved 26 September boundary — before developmental evidence catch-up',1)
 if n=='00_RESEARCH_MAP.md':
  old='coupling commissioning in progress; finite A0–A5 physical ceiling exercised; B1 apparatus closed, launch-packet regeneration next | A1–A5 observed external physical witnesses; B1/controls unexecuted, no launch authority; P learning/developmental efficacy untested'
  assert old in rest
  rest=rest.replace(old,'A0–A5 exercised; minimal B1 closed; ordinary Founder Search and separate motor/sandbox evidence registered | Learned-state change observed; useful developmental learning/navigation not established; M1 non-canonical',1)
 write(n,first+'\n\n'+nav+rest.lstrip('\n'),'AFTER')

questions=[
('E regulation and context','Does learned E regulation become source/sensory-context specific or remain mainly body-state regulation? Source contact and bank growth do not establish context-specific control.','06_M1_RESURRECTION_SANDBOX'),
('Control magnitude','Is the learned control contribution too small relative to M1 spontaneous activity? Preserve direct learned current, exploratory regulation, attenuation and indirect pathways separately.','06_M1_RESURRECTION_SANDBOX'),
('Associative H/read/use','Are write, retention, read and actual receiver use functionally too weak or fading? Nonzero H and growing q are not evidence of useful motor influence.','06_M1_RESURRECTION_SANDBOX'),
('Sensory cortical development','Are useful source distinctions preserved, or do observed changes mainly track generic contraction? Do not infer complete cortical collapse from fine-norm shrinkage.','06_M1_RESURRECTION_SANDBOX'),
('Cumulative integrity benefit','Does repeated integrity experience produce beneficial behaviour at longer ages? FS-015/FS-017 are bounded possible candidates, not causal success.','03_INTEGRITY_DEVELOPMENT'),
('Source effectiveness with age','Do contacts become more effective with developmental age once exposure, renewal, geometry and external support are accounted for? Current temporal trends are mixed.','06_M1_RESURRECTION_SANDBOX'),
('M1 status','Is M1 a useful commissioning/sandbox motor prior or a candidate newborn Loom mechanism? Canonical selection remains undecided despite the bounded screen and sandbox use.','05_MOTOR_COMMISSIONING'),
('Nursery-0 geometry','Does geometry still need shrinking after M1 increases reach? Preserve N0-A/B/C; no geometry or source-density change is accepted automatically.','04_EXPLORATION_AND_BIRTH'),
('Inherited competence','How much inherited sensorimotor structure is legitimate? Distinguish supplied anatomy, lawful lineage-acquired state and prohibited externally authored competence; retain/reset details need review.','04_EXPLORATION_AND_BIRTH'),
('Curiosity / intrinsic motivation','Would an intrinsic-motivation mechanism be needed later? It is an open mechanism question, not an accepted addition or present explanation.','04_EXPLORATION_AND_BIRTH'),
('Native long-run crash','What caused RS-M1-008’s native process failure? The faulting module/root cause and in-flight state are unknown; investigate separately from science. FS-060’s earlier interruption remains a distinct unresolved event.','06_M1_RESURRECTION_SANDBOX'),
('Learned-state physical causal ablation','What later matched physical intervention could test whether learned state changes useful behaviour while preserving exact state/RNG and support boundaries? No design, parameters, permission or result is implied.','06_M1_RESURRECTION_SANDBOX')]
qtext=f'''# Open questions

## Current questions — 1 October 2026

P now has ordinary-life and separate sandbox observations. Useful developmental learning/navigation remains **NOT ESTABLISHED**, rather than wholly untested. R and all alternative families remain preserved and unselected. These are questions, not instructions to build or run. [Evidence integration]({R}) · [Jason's directions]({DEC}).

| Question | Unresolved issue | Evidence context |
|---|---|---|
'''
for label,body,n in questions:qtext+=f'| {label} | {body} | [Review]({S}/{n}.md) |\n'
qtext+='\nM1 canonical status, Nursery-0 settings, inherited competence and any curiosity mechanism require Jason’s separate review. Control magnitude, associative usefulness, sensory differentiation, age trends and cumulative benefit are empirical/interpretive questions. Engineering crash diagnosis is separate; no scientific continuation follows.\n\n## Preserved specification-era question register — 20 September 2026\n\nThe original entries below retain their dated wording and hypotheses. Their “both untested”, numerical-pending and specification-stage labels describe that earlier record, not current execution history. Participation/retention, sustained cues and attribution questions remain available; none was erased by catch-up.\n\n'
old=(ROOT/'SHARED_BEFORE/02_OPEN_QUESTIONS.md').read_text(encoding='utf-8-sig').split('\n',1)[1]
write('02_OPEN_QUESTIONS.md',qtext+old.lstrip('\n'),'AFTER')
t=(ROOT/'SHARED_BEFORE/20_CANDIDATES/CAND-P.md').read_text(encoding='utf-8-sig')
t=t.replace('revision: r004','revision: r005',1).replace('work_status: fit-to-proceed-to-coupling-commissioning','work_status: developmental-evidence-integrated-through-2026-10-01',1).replace('evidence_status: untested','evidence_status: observed-internal-change-useful-developmental-learning-unestablished',1)
heading='# P — Contextual Association with Learned Participation'
assert heading in t
current=f'''## Current evidence — 1 October 2026

**Ordinary Founder Search evidence and separate non-canonical motor/sandbox evidence are now registered. Useful developmental learning and learned navigation are NOT ESTABLISHED.** Fixed roster FS-001–FS-060 contains 59 complete lives and one apparatus-interrupted prefix. Integrity consequences enter persistent learned state and later local output, while beneficial learned physical causation remains unresolved.

M1 is an explicitly declared motor variation, **not selected as canonical P**. Its corrected three-start screen and externally supported resurrection sandbox retain distinct runtimes, interventions and incomplete denominators. P’s neural learning mechanism is not revised by this wrapper. R, every original report family and the complete P draft remain unchanged.

[Current evidence index](../{IDX}) · [Integration report](../{R}) · [Open questions](../02_OPEN_QUESTIONS.md) · [Discussion-level direction](../{DEC}). Older engineering/specification statements below retain their historical scope; do not read “uncommissioned/untested” there as the present evidence state.

'''
t=t.replace(heading,heading+'\n\n'+current,1).replace('## Current engineering checkpoint — 2026-09-23','## Preserved engineering checkpoint — 2026-09-23',1)
t+='\n2026-10-01, '+ROOT.name+': r005 live evidence/navigation update; original complete candidate, mechanism equations and all alternatives preserved. Useful learned causation not established; M1 non-canonical.\n'
write('20_CANDIDATES/CAND-P.md',t,'AFTER')

for n,new in [('AGENTS.md',f'''## Current integration boundary — 1 October 2026

[Developmental evidence catch-up]({R}) supersedes the live September “no B1 execution / all science untested” summary only within its exact evidence scopes. A0–A5 bounded physical ceiling and later minimal B1 external-controller closure are registered. Ordinary FS-001–FS-060 has 59 complete lives and FS-060 interrupted prefix; useful learning unestablished. Passive I-pathway evidence, exploration/birth audits and a corrected nine-case motor screen are registered. **M1 is not canonical. NON-CANONICAL RESURRECTION SANDBOX:** all twelve reached 600 s, seven 4,500 s, RS-M1-008 has durable evidence through ~2968.955 s and a last full checkpoint ~2939.955 s, four remain at 600 s; no retry. Its 4.65 GB archive stays external.

Distinguish observed evidence, explicit Jason directions, assistant/build proposals and unresolved interpretations. [Jason’s current broad direction]({DEC}) is discussion-level, not canonical doctrine: examine whether accumulated learned state causally alters useful physical behaviour and where influence is lost. Do not infer M1 selection, P failure, new execution or Nursery-0 adoption. Original sealed human B1 evaluator material remains opaque; later minimal S1 evidence is a separate lineage. The appended crash-investigation brief is preserved for a separate build task; no replay or forensics was conducted by this integration. Canon/world/P/settings/evidence and previous complete candidates remain unchanged. Earlier sections are dated history.\n\n'''),('40_DECISIONS/DECISION_INDEX.md',f'''## Developmental directions and recorded bounded authorities — 1 October 2026

[Scoped decision/direction record]({Path(DEC).name}) registers actual Jason clarification, timing, historical B1/Founder/motor/sandbox authorizations and current broad discussion agreement, with original source links. No new launch permission, M1 canonical selection, nursery setting or causal-ablation decision is created. [Current integration](../{R}) keeps observations separate from those rulings. Earlier records remain unchanged.\n\n''')]:
 t=(ROOT/'SHARED_BEFORE'/n).read_text(encoding='utf-8-sig');first,rest=t.split('\n',1)
 if n=='AGENTS.md':rest=rest.replace('## Current commissioning boundary — B1 apparatus closure, 2026-09-26','## Preserved B1 apparatus boundary — 26 September 2026',1)
 write(n,first+'\n\n'+new+rest.lstrip('\n'),'AFTER')

reg=(ROOT/'SHARED_BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
reg+=f'\n## Developmental Ecology evidence catch-up — 1 October 2026\n\n[Integration]({R}) · [External archive custody]({S}/EXTERNAL_EVIDENCE.md). Small reports/metadata are byte-identical copies; nine full archives remain external. The resurrection archive is not copied.\n\n| ID | Source | Custody | SHA-256 |\n|---|---|---|---|\n'
for e in plan['source_entries']:
 path=e['path'].replace('\\','/');link='<'+path+'>' if e['storage'].startswith('external') else quote(path)
 reg+=f"| {e['source_id']} | [{e['original_filename']}]({link}) | {e['storage']}; {e['bytes']:,} bytes | `{e['sha256']}` |\n"
write('SOURCE_REGISTER.md',reg,'AFTER')
