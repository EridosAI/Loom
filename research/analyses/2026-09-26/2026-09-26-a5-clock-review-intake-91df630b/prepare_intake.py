"""Register supplied diagnosis and explicit acceptance; documentation/custody only."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib, io, json, zipfile, shutil

ROOT = Path(__file__).resolve().parent
WB = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ID = '2026-09-26-a5-clock-review-intake-91df630b'
S = '50_SESSIONS/' + ID
B = '90_SOURCES/p_a5_clock_review_2026-09-26_91df630b'
PREFIX = 'A5_CLOCK_COMPATIBILITY_REVIEW/'
R = S + '/A5_CLOCK_REVIEW_AND_ACCEPTED_CORRECTION.md'
DEC = '40_DECISIONS/DECISION-P-APPARATUS-CLOCK-2026-09-26-91df630b.md'
D = WB / 'INBOX/2026-09-26-A5-clock-compatibility-review-5f077481'
Z = D / 'A5_CLOCK_COMPATIBILITY_REVIEW.zip'
HELD = '90_SOURCES/p_a5_held_proposal_2026-09-26_62c8f4b1'
HR = '50_SESSIONS/2026-09-26-a5-held-intake-62c8f4b1/A5_HELD_PROPOSAL_RECORD.md'
A4R = '50_SESSIONS/2026-09-26-a4-evidence-intake-0e69b3c8/A4_COMMISSIONING_EVIDENCE_RECORD.md'
AUTH = '88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6'
P = '6bc9683b54e4fa80136fe8534d7713e2a250a95f'
CP = '5f07748102cb5eaa302569c87efbae095050e9fe'
CLASS = 'APPARATUS DEFECT — correction required to pose approved longer horizons'
ACCEPTANCE = 'I accept the native-index scheduling correction as a commissioning-apparatus fix. It must not change physical simulation time, P, world laws, controller routes or the interpretation of A1–A4.'
sha = lambda b: hashlib.sha256(b).hexdigest()

def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')

def dump(p, obj): write(p, json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

raw = Z.read_bytes()
receipt = json.loads((D/'DELIVERY_RECEIPT.json').read_text(encoding='utf-8-sig'))
assert sha(raw) == receipt['archive_identity']['sha256'] == '4419dede7014c86b9063c045ce62195494621aae9892604383f86d4cb5ffad44'
assert len(raw) == receipt['archive_identity']['bytes'] == 225072
assert sha(raw) in (D/(Z.name+'.sha256')).read_text()
z = zipfile.ZipFile(io.BytesIO(raw))
names = z.namelist()
assert len(names) == len(set(names)) == len({n.casefold() for n in names}) == 54
for n in names:
    q = PurePosixPath(n)
    assert n.startswith(PREFIX) and not q.is_absolute() and '..' not in q.parts and ':' not in n and '\\' not in n
mf = json.loads(z.read(PREFIX+'FILE_MANIFEST.json'))
assert not mf['execution_authority']
assert len(mf['files']) == receipt['payload_files_verified'] == 53
assert set(PREFIX+n for n in mf['files']) == set(names)-{PREFIX+'FILE_MANIFEST.json'}
assert sha(z.read(PREFIX+'FILE_MANIFEST.json')) == receipt['file_manifest_sha256']
for n, m in mf['files'].items():
    b = z.read(PREFIX+n)
    assert len(b) == m['bytes'] and sha(b) == m['sha256'], n
assert z.testzip() is None
incoming = {}
for n in [Z.name,Z.name+'.sha256','DELIVERY_RECEIPT.json']:
    incoming[str(D/n)] = sha((D/n).read_bytes())
for n in names:
    assert (D/n).read_bytes() == z.read(n), n
    incoming[str(D/n)] = sha(z.read(n))
refs = json.loads(z.read(PREFIX+'REFERENCE_MANIFEST.json'))
assert len(refs['files']) == 42
for n, m in refs['files'].items():
    b = z.read(PREFIX+n)
    assert len(b) == m['bytes'] and sha(b) == m['sha256'], n
    if n.startswith('references/held_A5_reference/'):
        assert b == (WB/HELD/PurePosixPath(n).name).read_bytes(), n
assert sha((WB/HELD/'AUTHORITY_OBJECT.canonical.json').read_bytes()) == AUTH
assert z.read(PREFIX+'SOURCE_IDENTITIES_BEFORE.json') == z.read(PREFIX+'SOURCE_IDENTITIES_AFTER.json')
identities = json.loads(z.read(PREFIX+'SOURCE_IDENTITIES_BEFORE.json'))
assert len(identities) == 250
diag = json.loads(z.read(PREFIX+'DIAGNOSTIC_RESULTS.json'))
assert diag['p_commit'] == P and diag['apparatus_commit'] == CP and diag['held_A5_sha256'] == AUTH
prior = diag['prior_saved_action_metadata']
assert sum(x['action_count'] for x in prior) == 5579
assert all(not x['integer_stage_mismatches'] and not x['replayed'] for x in prior)
assert len(diag['existing_detached_test_results']) == 6 and all(x['passed'] for x in diag['existing_detached_test_results'])
for k in ['world_steps','field_steps','neural_steps','RNG_draws','world_constructors','Run_constructors','A5_controller_calls']:
    assert diag['counts'][k] == 0, k
assert diag['counts']['detached_legacy_controller_calls'] == 13
pres = json.loads(z.read(PREFIX+'PRESERVATION.json'))
assert pres['all_hashes_unchanged'] and pres['held_A5_hash_unchanged'] == AUTH
final = json.loads(z.read(PREFIX+'FINAL_VERIFICATION.json'))
assert final['original_files_unchanged'] and not final['A5_output_directory_exists']

live = ['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md','40_DECISIONS/DECISION_INDEX.md']
before = {}
for n in live:
    data = (WB/n).read_bytes()
    before[n] = {'bytes':len(data),'sha256':sha(data)}
    q = ROOT/'BEFORE'/n
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes(data)
protected = {}
for folder in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS','50_SESSIONS']:
    for q in (WB/folder).rglob('*'):
        if q.is_file() and q.relative_to(WB).as_posix() not in live:
            protected[q.relative_to(WB).as_posix()] = sha(q.read_bytes())
catalog = json.loads((ROOT/'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
old_count = len(catalog['source_files'])
assert old_count == 256
batch = ROOT/'SOURCE_BATCH'
batch.mkdir(exist_ok=True)
for n in [Z.name,Z.name+'.sha256','DELIVERY_RECEIPT.json']:
    (batch/n).write_bytes((D/n).read_bytes())
for n in names:
    q=batch/n
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes(z.read(n))
selected = [Z.name,Z.name+'.sha256','DELIVERY_RECEIPT.json'] + [n for n in names if len(PurePosixPath(n).parts)==2]
entries = []
for number,n in enumerate(selected,old_count+1):
    data=(batch/n).read_bytes()
    entries.append({'source_id':f'SRC-{number:03d}','path':B+'/'+n,'original_filename':PurePosixPath(n).name,
        'bytes':len(data),'sha256':sha(data),'role':'apparatus-clock-compatibility-review',
        'prepared':'2026-09-26','registered':'2026-09-26',
        'stated_author':'Supplied diagnosis review; exact assistant model/backend not stated',
        'acquired_from':str(Z)+'::'+n if n in names else str(D/n),'archive_member':n if n in names else None,
        'authority':'Jason requests review registration and subsequently explicitly accepts the bounded apparatus correction; acceptance recorded separately',
        'held_proposal_authority_sha256':AUTH,'execution_authorized':False,'A5_execution_occurred':False,
        'p_baseline_checkpoint':P,'reviewed_apparatus_checkpoint':CP,'review_note':R,'decision_record':DEC,
        'record':S+'/INTAKE_RECORD.md','classification':CLASS,
        'notes':'Diagnosis source preserved as issued, including its pending-decision wording. Later Jason acceptance does not certify an implementation, authorize A5 execution, or change A1–A4 interpretation.'})
catalog['source_files'] += entries
catalog['intake_events'].append({'session_id':ID,'source_ids':[e['source_id'] for e in entries],
    'review_note':R,'decision_record':DEC,'record':S+'/INTAKE_RECORD.md','held_proposal_authority_sha256':AUTH,
    'scope':'A5 clock apparatus defect registered; native-index correction Jason-accepted within explicit constraints; implementation/verification outstanding; A5 remains held and not executed'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)

def src(n,label): return f'[{label}](../../{B}/{PREFIX}{n})'

status = '''P engineering: **VERIFIED within its prior reviewed scope**  
Commissioning apparatus: **A5 clock defect OPEN; scoped correction JASON-ACCEPTED; implementation/verification outstanding**  
Coupling commissioning: **IN PROGRESS; A5 held before execution**  
Scientific/developmental efficacy: **UNTESTED**

| Commissioning item | Current status |
|---|---|
| V1 / V2 / V3 | COMPLETE |
| A0 | COMPLETE within its bounded scope |
| A1–A4 | OBSERVED within their bounded scopes |
| A5 | PREPARED / HOLD / NOT LAUNCH-READY; NOT EXECUTED |
| B1–B4 | NOT EXECUTED |
| C1/C2 | NOT EXECUTED |'''
record=f'''# A5 clock review and accepted apparatus correction

**Registered:** 2026-09-26. **Classification: {CLASS}.**

Jason has explicitly accepted the native-index scheduling correction as a commissioning-apparatus fix, subject to the [exact ruling and constraints](../../{DEC}#jasons-exact-ruling). The review was written before that acceptance; its original pending-decision statements remain preserved. **Acceptance is recorded; implementation and engineering verification remain outstanding. No A5 execution occurred.**

{status}

## Exact scope and identities

Reviewed apparatus: `{CP}`. Unchanged P baseline: `{P}`. Held A5 proposal: `{AUTH}`. The [held packet and preparation](../../{HR}), its [canonical bytes](../../{HELD}/AUTHORITY_OBJECT.canonical.json), OPEN_ISSUE_A5_CLOCK.md and CLOCK_AUDIT.json remain unchanged. The proposed 630 s source 0 → 1 → 0 → 1 circuit and approximately 210–222 s unattended renewal opportunities are unchanged and unexecuted. The held hash identifies that proposal; it is not a new launch authority.

Primary source: {src('A5_CLOCK_COMPATIBILITY_REVIEW.md','complete clock-compatibility review')} (§§2–9 for diagnosis/options/closure requirements, §11 for prior evidence). Supporting records: {src('DIAGNOSTIC_RESULTS.json','diagnostic results')}, {src('ARITHMETIC_DETAIL.json','arithmetic detail')}, {src('CLOCK_HISTORY.json','clock history')}, {src('PRESERVATION.json','preservation')}, {src('FINAL_VERIFICATION.json','source verification')}. [Original ZIP](../../{B}/{Z.name}) and all source members are preserved byte-for-byte.

## Recorded defect and diagnosis

| Quantity | Reviewed finding |
|---|---|
| First affected scheduled command | Native step 26,950 |
| Accumulated physical clock | 269.4999999998999 s |
| Intended nominal boundary | 269.5 s |
| Discrepancy | -1.0010126061388291e-10 s; exceeds fixed 1e-10 allowance |
| Rejecting predicate | `pending.py::validate_decision`: `issued decision clock mismatch` |
| Separate later failure | Nominal 270 s stage transition remains not due under accumulated time; proposed hold crosses prescribed stage boundary |

These are static/scalar and detached-predicate diagnosis findings, conditional on full nonterminal native steps reaching those boundaries. They are **not an observed A5 trajectory failure**. Loosening only the absolute clock comparison would leave the 270 s stage rejection unresolved.

Float resolution itself remains adequate through the proposed 630 s horizon. The defect is inconsistent use of accumulated floating-point clock values for discrete controller scheduling. The recommended correction gives native indices ownership of stage selection, command holds and stopping while retaining and validating the existing physical clock. It must not replace physical time with index-derived timestamps, change physical event tolerance, retime the mover/fields, or weaken authority binding. The accepted direction is source option D, not wholesale approval of every engineering detail or alternative in the source.

Source §9 describes the closure requirements still to be implemented and verified: consistent index ownership at runner/controller/pending/validator call sites; physical-clock validation against the original recurrence; strict admission of native-boundary deadlines; preservation of partial-terminal handling, hold limits and restart/journal continuity; versioned instrument/authority identities. A scalar oracle showing 6,300 prescribed holds fit does not verify a future implementation.

## Prior A1–A4 evidence remains unchanged

The source's read-only retrospective metadata check reports **all 5,579 saved A1–A4 controller decisions retain their expected stage under the reviewed index interpretation**, with zero stage mismatches. Counts are A1: 919; A2: 1,800; A3: 2,100; A4-CROSS: 160; A4-WAIT: 280; A4-DETOUR: 320. Each A4 case retains its own original clock origin. This is a reported metadata check, not replay, recomputation of trajectories, or a new scientific result.

The [prior A4 evidence and earlier chain](../../{A4R}) retain their observations, limits and interpretations, including A1's original post-check history, A2's retained helper flags, A3's contact/damage limitations and A4's analytic/comparison limits. Previous apparatus checkpoint dispositions retain their reviewed scopes. The new longer-horizon defect does not rewrite prior closure or mark P, A5 ecology, source renewal or stock as failed.

## Accepted decision, alternatives and remaining boundary

Jason's current acceptance is recorded in the [new decision record](../../{DEC}); it is distinct from the source recommendation and from the earlier held-proposal record. Physical simulation time, native dt, controller hold duration, P, world laws, controller routes, A5 ecological design and A1–A4 interpretation must remain unchanged. No numerical world setting or canon amendment is accepted by this ruling.

Source §8 preserves the alternatives: raising/removing the guard, changing physical world time, local-stage clocks, and a carefully justified apparatus-only error envelope. They remain source alternatives, not selected changes. Acceptance chooses the bounded native-index correction direction, without claiming the correction has been built or closed.

**A5 remains PREPARED / HOLD / NOT LAUNCH-READY.** Correction implementation and engineering verification are outstanding. Any later changed instrument requires its own exact identity, review and separately bound execution authority. The held packet/hash is not edited or reused as permission to launch. This session stops at recording and navigation; no implementation, simulation, replay, continuation or new authority object was produced.

## Source preservation and verification limits

The source reports six detached legacy tests passed, 13 detached legacy controller calls, and zero A5 controller calls, world/field/neural steps, RNG draws or world/Run construction. Those are supplied diagnostic results; this intake did not run those tests or the packaged helper. Its before/after inventories contain the same 250 identities. The original DIAGNOSTIC_RESULTS scalar wave entry and the later ARITHMETIC_DETAIL supplement are both retained: built-in summation reported 0.2, whereas explicit repeated addition gives 0.20000000000000004. The supplement documents the production-style arithmetic distinction; neither file was rewritten.

Intake verified the archive SHA-256 against its receipt/sidecar, all 53 payload hashes and CRCs, all 54 expanded inbox members, all 42 packaged reference identities, the five held-reference copies against registered originals, and the held canonical hash. It checked saved retrospective counts, no-mismatch flags and zero-execution fields. These are custody/registration checks, not an independent rerun of the diagnosis or certification of a correction. No necessary source gap or identity conflict was found.

[Source identities](SOURCE_IDENTITIES.json) · [Completion record](INTAKE_RECORD.md) · [Intake validation](VALIDATION.json).
'''
write(ROOT/'NEW'/R,record)
decision=f'''---
id: "DECISION-P-APPARATUS-CLOCK-2026-09-26-91df630b"
authority_status: accepted-by-jason
work_status: correction-implementation-and-verification-outstanding
evidence_status: not-an-experimental-result
---

# Accepted native-index scheduling correction

**Recorded:** 2026-09-26. **Decision authority:** Jason. **Scope:** narrowly bounded commissioning-apparatus correction. **Proposer:** supplied clock-compatibility review; acceptance below is Jason's explicit current ruling.

## Jason's exact ruling

> {ACCEPTANCE}

Source anchor: Jason's latest user message in the current workbench intake conversation, received after the instruction to record a pending decision and before this record was written. No native message identifier or independent chat export is available. This quotation records the supplied wording; this authored note is not a complete chat export.

## Effective change and constraints

The native-index scheduling correction is **ACCEPTED**, replacing its previous pending-decision status. It may correct discrete stage ownership and command scheduling in the commissioning apparatus while retaining and validating the existing accumulated physical simulation clock.

The earlier proposed wording to which the acceptance responds was:

> Permit a narrowly scoped commissioning-apparatus correction replacing floating-clock stage ownership/command scheduling with native-index-derived scheduling. Physical simulation time, native dt, controller hold duration, world laws, P and all previous evidence remain unchanged.

The explicit ruling additionally names unchanged controller routes and unchanged interpretation of A1–A4. Keep physical time, native dt, hold duration, world laws, P, routes, A5 ecological design, numerical world settings and previous evidence unchanged. Do not retime physical dynamics or translate prior evidence onto a new clock. This decision does not accept an unbuilt implementation, certify closure, grant A5 execution, or amend canon.

## Review basis and alternatives

The [registered diagnosis](../{R}) classifies the defect at exact apparatus `{CP}` as **{CLASS}**. Source [§8 alternatives](../{B}/{PREFIX}A5_CLOCK_COMPATIBILITY_REVIEW.md#8-candidate-closures-compared) and [§9 closure requirements](../{B}/{PREFIX}A5_CLOCK_COMPATIBILITY_REVIEW.md#9-exact-requirements-for-the-recommended-closure) retain the technical basis. Option D is the accepted direction; detailed implementation remains subject to verification against these constraints. Raising/removing a guard alone, changing physical world time, local-stage clocks and a justified error-envelope alternative remain preserved as unselected source options.

## Supersession and chronology

This acceptance supersedes only the pending Jason decision in the [held preparation history](../{HR}) and the source review's recommendation status. It does not overwrite either source. The source review's “STOP FOR JASON” and “proposals only” labels remain true of that document's preparation stage. Earlier decision records and exact checkpoint histories remain unchanged.

## Current disposition

**Correction direction: JASON-ACCEPTED. Implementation and engineering verification: OUTSTANDING.**

**A5: PREPARED / HOLD / NOT LAUNCH-READY; NOT EXECUTED.** Held authority identity `{AUTH}` and its [canonical bytes](../{HELD}/AUTHORITY_OBJECT.canonical.json) remain unchanged. A later corrected instrument needs its own exact reviewed identity and separately bound execution authority; acceptance of this fix is not A5 launch approval.

A0–A4 retain completed/observed bounded scopes and interpretations. B1–B4 and C1/C2 remain not executed. Scientific/developmental efficacy remains **UNTESTED**. This recording session implements no correction, creates no experiment number and executes no commissioning or scientific trial.
'''
write(ROOT/'NEW'/DEC,decision)

nav=f'''## Current commissioning boundary — A5 clock correction accepted, 2026-09-26

{status}

**{CLASS}.** The review identifies valid-command rejection at native step 26,950 (physical time 269.4999999998999 s versus nominal 269.5 s) and a separate stage-transition rejection at 270 s. Float resolution remains adequate through 630 s; the defect concerns discrete scheduling with accumulated floating-point time.

Jason has **accepted the native-index scheduling correction as a commissioning-apparatus fix**. Physical simulation time, P, world laws, controller routes and the interpretation of A1–A4 must remain unchanged; native dt, controller hold duration, prior evidence and A5 ecological design are also preserved. The reviewed retrospective check retains the expected stage for all 5,579 saved A1–A4 decisions. Correction implementation and verification remain outstanding.

**A5 remains PREPARED / HOLD / NOT LAUNCH-READY. No A5 execution occurred.** Held proposal hash `{AUTH}` is unchanged. No A5/ecological/P failure, inadequate renewal or inadequate source stock is recorded. Prior engineering dispositions retain their exact reviewed scopes. Acceptance of the apparatus correction does not authorize A5 execution or amend canon or numerical world settings.

[Exact accepted decision]({DEC}) · [Review registration]({R}) · [Complete source review]({B}/{PREFIX}A5_CLOCK_COMPATIBILITY_REVIEW.md) · [Held preparation history]({HR}). Earlier sections below preserve their dated states, including the former pending-decision wording.

'''
oldheading='## Current commissioning boundary — A5 held proposal, 2026-09-26'
historical='## Preserved A5 preparation — before clock review and acceptance, 2026-09-26'
for n in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    text=(ROOT/'BEFORE'/n).read_text(encoding='utf-8-sig')
    first,rest=text.split('\n',1)
    assert oldheading in rest
    rest=rest.replace(oldheading,historical,1)
    if n=='00_RESEARCH_MAP.md':
        old='A1–A4 observed external-control witnesses; A5 clock compatibility pending review; learning/developmental efficacy untested'
        assert old in rest
        rest=rest.replace(old,'A1–A4 observed external-control witnesses; A5 apparatus clock correction accepted, implementation/verification outstanding; learning/developmental efficacy untested',1)
    write(ROOT/'AFTER'/n,first+'\n\n'+nav+rest.lstrip('\n'))
text=(ROOT/'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig')
first,rest=text.split('\n',1)
assert oldheading in rest
rest=rest.replace(oldheading,historical,1)
continuation=f'''## Current continuation — apparatus clock correction accepted, 2026-09-26

Jason explicitly [accepted the native-index scheduling correction]({DEC}#jasons-exact-ruling) as a commissioning-apparatus fix. The [registered review]({R}) classifies the pinned apparatus's long-horizon scheduling issue as **{CLASS}**. The acceptance supersedes the pending-decision wording in earlier sections and preserved sources for this correction only.

The correction must not change physical simulation time, P, world laws, controller routes or the interpretation of A1–A4. Retain and validate the physical clock; preserve native dt, hold duration, numerical world settings, A5 ecological design and all previous evidence. Detailed implementation/verification remain outstanding; no closure is certified by this decision record.

**A5 remains PREPARED / HOLD / NOT LAUNCH-READY; no A5 execution occurred.** Preserve the held packet, OPEN_ISSUE_A5_CLOCK.md, CLOCK_AUDIT.json, zero-execution evidence and hash `{AUTH}`. No new A5 execution authority is granted. V1/V2/V3/A0 COMPLETE; A1–A4 OBSERVED within their bounded scopes and unchanged interpretations; B1–B4 and C1/C2 NOT EXECUTED; efficacy UNTESTED. Prior engineering checkpoints retain their reviewed scope. Do not record ecological/P/A5 failure or inadequate renewal/stock. This session records acceptance and stops; it does not implement the fix, alter canon, execute trials or perform Git operations.

'''
write(ROOT/'AFTER/AGENTS.md',first+'\n\n'+continuation+rest.lstrip('\n'))
text=(ROOT/'BEFORE/40_DECISIONS/DECISION_INDEX.md').read_text(encoding='utf-8-sig')
first,rest=text.split('\n',1)
idx=f'''## Accepted apparatus clock correction — 2026-09-26

[Jason's exact ruling and constraints]({PurePosixPath(DEC).name}) accept the native-index scheduling correction as an apparatus fix. Physical simulation time, P, world laws, controller routes and A1–A4 interpretation must remain unchanged. Implementation/verification remain outstanding. **A5 remains PREPARED / HOLD / NOT LAUNCH-READY, with no execution and an unchanged held hash.** The [review registration](../{R}) preserves diagnosis, source identities and the preceding pending-decision history. Earlier rulings below remain unchanged.

'''
write(ROOT/'AFTER/40_DECISIONS/DECISION_INDEX.md',first+'\n\n'+idx+rest.lstrip('\n'))
register=(ROOT/'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
register+='\n## A5 clock-compatibility review and subsequent acceptance — 2026-09-26\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:
    register+=f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
register+=f'\n[Review registration]({R}) · [Subsequent explicit Jason acceptance]({DEC}). {CLASS}. Original review recommendations/pending labels preserved; correction direction now accepted, implementation/verification outstanding. A5 held hash `{AUTH}` unchanged; no A5 execution.\n'
write(ROOT/'AFTER/SOURCE_REGISTER.md',register)
verification={'incoming_zip':str(Z),'zip_bytes':len(raw),'zip_sha256':sha(raw),
    'manifest_payloads_verified':53,'archive_members':54,'crc_passed':True,
    'all_unpacked_inbox_members_match_zip':True,'delivery_receipt_and_sidecar_match':True,
    'packaged_reference_identities_verified':42,'held_reference_copies_match_registered_originals':5,
    'held_canonical_sha256':AUTH,'supplied_before_after_manifests_byte_identical':True,
    'supplied_preservation_identities':250,'reported_prior_decisions':5579,'reported_stage_mismatches':0,
    'reported_detached_legacy_tests_passed':6,'reported_detached_legacy_controller_calls':13,
    'reported_A5_controller_and_world_execution':0,'classification':CLASS,
    'correction_decision':'accepted-by-jason','correction_implemented_by_intake':False,
    'correction_verification':'outstanding','A5_executed':False,'A5_launch_authorized':False,
    'review_or_tests_rerun_during_intake':False,'git_operations':False,'necessary_source_gaps':[],
    'source_identity_conflicts':[]}
inventory={q.relative_to(batch).as_posix():sha(q.read_bytes()) for q in batch.rglob('*') if q.is_file()}
dump(ROOT/'NEW'/S/'SOURCE_IDENTITIES.json',{'session_id':ID,'held_proposal_authority_sha256':AUTH,
    'verification':verification,'registered_sources':entries,'complete_batch_sha256':inventory,
    'acceptance_source':'Current user message; exact quotation and provenance in '+DEC})
intake=f'''# A5 clock review intake — completion

Registered the complete supplied diagnosis and Jason's later explicit acceptance of the native-index scheduling apparatus correction. **{CLASS}.** [Review record](A5_CLOCK_REVIEW_AND_ACCEPTED_CORRECTION.md) · [Accepted decision](../../{DEC}).

Read current AGENTS/map/status, decision index/template, the complete primary clock review and its structured diagnosis/arithmetic/history/preservation records, and the held proposal identity. Source pending-decision labels are preserved as preparation history; the exact current ruling is recorded separately.

Preserved original ZIP, sidecar, receipt and all 54 members in a unique source batch. Verified 53 payload hashes/CRCs, 42 internal reference identities, five held-reference copies, archive/receipt identities, held canonical hash and reported retrospective counts. Registered SRC-{old_count+1:03d}–SRC-{old_count+len(entries):03d}. No diagnostic helper, test, controller, simulation or replay was run by intake. The source's 6 detached tests and 5,579-decision check are attributed results, not new executions here.

Added this session and one explicit decision record; updated AGENTS.md, 00_RESEARCH_MAP.md, 01_WORKSPACE_STATUS.md, SOURCE_CATALOG.json, SOURCE_REGISTER.md and 40_DECISIONS/DECISION_INDEX.md. Earlier sources/candidates/reviews/decisions/sessions and existing catalog rows remain unchanged. PRIOR_SHARED_NOTES.zip plus its receipt preserve all six prior shared notes. [Source identities](SOURCE_IDENTITIES.json) · [Validation](VALIDATION.json).

Correction direction accepted; implementation and engineering verification outstanding. A5 remains PREPARED / HOLD / NOT LAUNCH-READY and not executed. Held packet/hash, canon, mechanism, physical clock, world configuration/settings, routes, sequence and A1–A4 evidence/interpretation remain unchanged. No new authority object, experiment number, Git operation or actual repository change. Scientific/developmental efficacy remains UNTESTED. No necessary source gap found. Stop after confirmation.
'''
write(ROOT/'NEW'/S/'INTAKE_RECORD.md',intake)
dump(ROOT/'PLAN.json',{'session':S,'batch':B,'review':R,'live_before':before,'protected_before':protected,
    'source_entries':entries,'verification':verification,'zip_source':str(Z),'old_catalog_count':old_count,
    'status':'A5 PREPARED / HOLD / NOT LAUNCH-READY; native-index correction JASON-ACCEPTED; implementation/verification outstanding',
    'incoming_before':incoming,'batch_inventory':inventory})
shutil.copyfile(ROOT.parent/'2026-09-26-a5-held-intake-62c8f4b1/publish_intake.py',ROOT/'publish_intake.py')
print(json.dumps({'prepared':ID,'sources':len(entries),'protected':len(protected),'batch_files':len(inventory),'decision':DEC}))
