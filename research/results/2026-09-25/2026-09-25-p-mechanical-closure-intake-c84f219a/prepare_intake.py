"""Documentation custody and registration only. Never import or run package code."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib, io, json, zipfile

ROOT = Path(__file__).resolve().parent
WB = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ID = '2026-09-25-p-mechanical-closure-intake-c84f219a'
S = f'50_SESSIONS/{ID}'
B = '90_SOURCES/p_final_mechanical_closure_2026-09-25_c84f219a'
R = '30_REVIEWS/REVIEW-P-APPARATUS-MECHANICAL-CLOSURE-5f077481-2026-09-25-c84f219a.md'
Z = WB/'INBOX/2026-09-25-P_Final_Mechanical_Closure_Review/Loom_P_Final_Mechanical_Closure_Review_5f077481_20260925.zip'
CP = '5f07748102cb5eaa302569c87efbae095050e9fe'
PREV = '9d31e7902658b15762052a2a6a3d161d64338524'
OLD = '05abf60401d08f38750bca589b1c040e10513d7b'
P = '6bc9683b54e4fa80136fe8534d7713e2a250a95f'
DISPOSITION = 'FIT TO BEGIN AUTHORIZED COUPLING COMMISSIONING'
REPORT = 'LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md'
OLD_REVIEW = '30_REVIEWS/REVIEW-P-APPARATUS-INDEPENDENT-05abf604-2026-09-24-b92e45a7.md'
P_REVIEW = '30_REVIEWS/REVIEW-P-ENGINEERING-6bc9683b-2026-09-23-08df839e.md'
sha = lambda data: hashlib.sha256(data).hexdigest()
def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8', newline='\n')
def dump(path, obj):
    write(path, json.dumps(obj, indent=2, ensure_ascii=False)+'\n')
def verify_zip(z):
    names = z.namelist()
    assert len(names) == len(set(names))
    assert len(names) == len({n.casefold() for n in names})
    for name in names:
        p = PurePosixPath(name)
        assert not p.is_absolute() and '..' not in p.parts and ':' not in name and '\\' not in name
    manifest = json.loads(z.read('FILE_MANIFEST.json'))
    entries = manifest['files']
    if isinstance(entries, list):
        assert len(entries) == len({e['path'] for e in entries})
        entries = {e['path']:e for e in entries}
    assert set(entries) == set(names)-{'FILE_MANIFEST.json'}
    for name, info in entries.items():
        data = z.read(name)
        assert len(data) == info['bytes'] and sha(data) == info['sha256'], name
    assert z.testzip() is None
    return {'members':len(names), 'manifest_payloads_verified':len(entries), 'safe_unique_paths':True, 'crc_passed':True}

incoming = Z.read_bytes()
assert len(incoming) == 65436042 and sha(incoming) == '04b9fc32f1a855338dc0b24d09f15288031f2b0931217b00560a741eacc66672'
z = zipfile.ZipFile(io.BytesIO(incoming))
outer_check = verify_zip(z)
identities = json.loads(z.read('REVIEWED_IDENTITIES.json'))
assert (identities['checkpoint'], identities['previous_HOLD'], identities['P_checkpoint']) == (CP, PREV, P)
assert identities['disposition'] == DISPOSITION
assert identities['commissioning_authorized_by_review'] is False and identities['commissioning_executed_by_review'] is False
builder_member = 'reviewed_delivery/Loom_P_Final_Apparatus_Correction_Review_20260925.zip'
builder_bytes = z.read(builder_member)
assert len(builder_bytes) == identities['reviewed_builder_zip']['bytes']
assert sha(builder_bytes) == identities['reviewed_builder_zip']['sha256']
builder = zipfile.ZipFile(io.BytesIO(builder_bytes))
builder_check = verify_zip(builder)
checkpoint = json.loads(builder.read('CHECKPOINT.json'))
assert (checkpoint['checkpoint'], checkpoint['previous'], checkpoint['P']) == (CP, PREV, P)
patch = z.read('FINAL_CORRECTION.patch')
assert patch == builder.read('FINAL_CORRECTION.patch')
assert len(patch) == identities['patch']['bytes'] and sha(patch) == identities['patch']['sha256'] == checkpoint['diff_sha256']

previous_member = 'previous/Loom_P_Final_Independent_Apparatus_Correction_Review_9d31e790_20260925.zip'
previous_bytes = builder.read(previous_member)
assert len(previous_bytes) == 24920860 and sha(previous_bytes) == '24261f1fec4c281894729201f65f5d0e89bda564ef31bb73160925dcf1561709'
previous = zipfile.ZipFile(io.BytesIO(previous_bytes))
previous_check = verify_zip(previous)
assert z.read('references/PREVIOUS_INDEPENDENT_HOLD_REVIEW.md') == previous.read('LOOM_P_FINAL_APPARATUS_CORRECTION_REVIEW.md')
previous_builder = builder.read('previous/Loom_P_Apparatus_Correction_Review_20260924.zip')
assert sha(previous_builder) == 'e261dbb9836a916f3ff4b6daa3ae8d9c21ea12194198d1ed63dfa7ee9b798a81'
assert previous_builder == previous.read('reviewed_delivery/Loom_P_Apparatus_Correction_Review_20260924.zip')

old_builder_path = WB/'90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/Loom_P_Commissioning_Apparatus_Review_20260924.zip'
with zipfile.ZipFile(old_builder_path) as old:
    for name, expected in identities['P_runtime']['files'].items():
        member = 'developmental_ecology/loom_p/'+name
        assert sha(builder.read(member)) == expected and builder.read(member) == old.read(member)
    config_member = 'developmental_ecology/configuration.json'
    assert builder.read(config_member) == old.read(config_member)
    assert sha(builder.read(config_member)) == identities['configuration_file']['sha256']
for name, expected in identities['apparatus_runtime']['files'].items():
    assert sha(builder.read('developmental_ecology/loom_commissioning/'+name)) == expected
for member, phrase in [('worktree-suite.log','143 passed in 94.30s'),('portable-suite.log','143 passed in 95.95s')]:
    assert phrase in z.read(member).decode('utf-8-sig')

live = ['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md']
before = {}
for name in live:
    data = (WB/name).read_bytes()
    before[name] = {'bytes':len(data),'sha256':sha(data)}
    path = ROOT/'BEFORE'/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
protected = {}
for folder in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS','50_SESSIONS/2026-09-24-p-independent-apparatus-intake-b92e45a7']:
    for path in (WB/folder).rglob('*'):
        if path.is_file():
            protected[path.relative_to(WB).as_posix()] = sha(path.read_bytes())

catalog = json.loads((ROOT/'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
old_count = len(catalog['source_files'])
assert old_count == 82
selected = [
    (None,'independent-mechanical-closure-delivery-archive'),
    (REPORT,'independent-final-mechanical-closure-review'),
    ('CLOSURE_TABLE.md','independent-mechanical-closure-table'),
    ('REVIEWED_IDENTITIES.json','independent-review-identities'),
    ('FILE_MANIFEST.json','independent-review-payload-manifest'),
    ('README.md','independent-review-intake-note'),
    ('REPRODUCTION_COMMANDS.md','historical-reproduction-record-not-execution-authority'),
    ('references/PREVIOUS_INDEPENDENT_HOLD_REVIEW.md','intervening-9d31e790-independent-hold-history'),
    ('references/FINAL_MECHANICAL_REVIEW_REQUEST.txt','packaged-historical-review-request-not-current-execution-authority'),
    ('provenance/provenance.md','independent-provenance-subreview'),
    ('FAULT_AND_SUITE_AUDIT.md','independent-fault-and-suite-audit'),
]
entries = []
for number,(member, role) in enumerate(selected, old_count+1):
    name = Path(member).name if member else Z.name
    data = z.read(member) if member else incoming
    path = ROOT/'SOURCE_BATCH'/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    entry = {
        'source_id':f'SRC-{number:03d}', 'path':B+'/'+name, 'original_filename':name,
        'bytes':len(data), 'sha256':sha(data), 'role':role, 'prepared':'2026-09-25',
        'stated_author':'User review request as packaged; original chat not independently available' if member and member.endswith('REQUEST.txt') else 'Independent reviewer; exact model/backend not stated in main review or reviewed identities',
        'authority':'Registered review evidence and history only; not commissioning authority or scientific ratification',
        'acquired_from':str(Z)+('::'+member if member else ''), 'archive_member':member,
        'reviewed_checkpoint':PREV if member and 'PREVIOUS_' in member else CP,
        'p_baseline_checkpoint':P, 'review_note':R, 'record':S+'/INTAKE_RECORD.md',
        'notes':'Original bytes retained, including historical commands. Entire evidence tree is preserved in the unchanged ZIP; extracted reading copies do not rewrite source-relative references.'}
    entries.append(entry)
catalog['source_files'] += entries
catalog.setdefault('intake_events',[]).append({
    'session_id':ID, 'source_ids':[e['source_id'] for e in entries], 'review_note':R, 'record':S+'/INTAKE_RECORD.md',
    'scope':f'Exact apparatus {CP}: {DISPOSITION}; preserve earlier checkpoint holds; P unchanged; commissioning NOT STARTED; no execution authority'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)

status = f'''Exact apparatus checkpoint: `{CP}`

Commissioning apparatus: **{DISPOSITION}**  
P implementation: **unchanged / previously verified**, baseline `{P}`  
P mechanism fidelity: **INDEPENDENTLY VERIFIED within reviewed scope**  
Commissioning execution: **NOT STARTED**  
Scientific status: **UNCOMMISSIONED / UNTESTED**

Known mechanical blockers **A-R1a, A-R1b and A-R1c: CLOSED — VERIFIED** within the final independent review's scope. The original A-R2 clock-comparison defect remains closed for its reviewed boundary class.
'''
table = z.read('CLOSURE_TABLE.md').decode('utf-8-sig').replace('\r','')
table = table[table.index('| Known blocker'):table.index('\n\nNo unresolved')].strip()
review = f'''# P apparatus — final mechanical closure registration

**Registered:** 2026-09-25 under Jason's inbox-intake instruction. This note registers the supplied independent review; it is not a new execution or a fresh code review.

{status}

The [complete review](../{B}/{REPORT}) and [reviewed identities](../{B}/REVIEWED_IDENTITIES.json) supply this disposition. “Authorized” is conditional: Jason's separate execution decision is still required. This review and this intake grant no commissioning authority. No scientific efficacy, developmental success, survival capability or ecological adequacy has been established.

## Exact checkpoint history

| Apparatus checkpoint | Disposition at that checkpoint | Evidence and relationship |
|---|---|---|
| `{OLD}` | **ENGINEERING HOLD**; A1/source A-R1 and A2/source A-R2 open | [Previously registered independent review](REVIEW-P-APPARATUS-INDEPENDENT-05abf604-2026-09-24-b92e45a7.md), unchanged |
| `{PREV}` | **HOLD BEFORE COUPLING COMMISSIONING**; A-R1a/b/c open; original A-R2 verified closed | [Complete intervening independent review](../{B}/PREVIOUS_INDEPENDENT_HOLD_REVIEW.md), supplied in this package and registered here as history |
| `{CP}` | **{DISPOSITION}**; A-R1a/b/c closed | [Final independent mechanical closure](../{B}/{REPORT}); direct child of 9d31e790 according to the supplied checkpoint/provenance records |

The later dispositions apply to later exact checkpoints; they do not retrospectively clear the earlier holds. A-R1a/b/c are the three residual authority/continuation defects found after the original complete-specification correction. A-R1c's pending-command overrun was distinct from the original A-R2 numerical comparison defect. Neither set is P's historical R1–R3 or the commissioning case labels A1–A5.

The [P engineering baseline](REVIEW-P-ENGINEERING-6bc9683b-2026-09-23-08df839e.md) and its [d5f7efbe/f7eb6f27 history](P_ENGINEERING_HISTORY_2026-09-23-08df839e.md) keep their dispositions. Original P/R designs, alternative families and decisions are unchanged.

## Independent closure findings

The source's concise closure table is retained below without reclassification. Its test and execution findings belong to the independent reviewer, not this intake.

{table}

The report identifies no remaining closure action or unresolved law-bearing/scientific departure within the requested scope. The prior A-R2 numerical comparator is unchanged in this final correction and remains covered by regression. Other earlier reviewed apparatus findings retain their stated scope and classifications; this intake does not reopen or widen them.

## What the evidence establishes

The independent reviewer reports original failures on 9d31e790 and corrected controls on 5f077481, 143 tests passing in each of the worktree and portable suites, and all 54 fault/control pairs (108 logs) reaching their intended outcomes. The count comprises 59 unchanged P, 24 original apparatus, 30 previous correction and 30 final correction tests; it is supporting evidence, not the sole closure argument. See the [fault/suite audit](../{B}/FAULT_AND_SUITE_AUDIT.md) and [provenance subreview](../{B}/provenance.md).

The reported corrections reject ambiguous approvals, bind the controller actually producing commands, and validate pending decisions across advancement, save and resume. Legal seven-plus-three continuation reaches the stage boundary and then uses a fresh next-stage command. Rejected pending mutations cause no unauthorized advancement in the demonstrated checks. The review reports unchanged P/configuration and no commissioning receipts in its enumerated correction evidence; that census is not a universal claim about unrecorded activity elsewhere.

This intake independently checked package sizes, hashes, CRCs, checkpoint/patch agreement, and the identities of packaged code bytes without importing them. All 13 packaged P modules and configuration match the previously registered apparatus delivery byte-for-byte. No target repository or Git state was inspected. The reviewer-reported runtime, tests, replay and preservation claims were not rerun.

## Retained limits and authority

This is bounded mechanical fitness, not a general security, numerical convergence or scientific certification. Long-run performance, controller competence, UI polish, wider numerical cases and untested commissioning outcomes remain outside the closure question. Supported resume requires an intact complete pause and its parent evidence chain. Structured human procedure text remains inspectable approval material; software does not prove operator compliance. The earlier 18 authority fault negatives' test-callback limitation remains disclosed in the full review; the new production-guard evidence is separately described there.

P's existing limits remain: finite-step contact is not an exhaustive convergence proof; sensory capacity is provisional; the mean-plus-endpoint packet is lossy; adaptation may suppress sustained information; association is deliberately contracting; effective learned magnitudes remain unknown; and shared equal-valued E/I configuration fields remain an implementation limitation.

The [packaged closure-review request](../{B}/FINAL_MECHANICAL_REVIEW_REQUEST.txt) is historical review authority, not a new execution instruction. Synthetic grants in the ZIP are manufactured test data, never Jason authorization. This registration does not select commissioning cases, approve a route/controller, start a life, freeze a coupling, change a parameter or amend research canon.

## Custody and source gap

The unchanged [incoming archive](../{B}/{Z.name}) preserves all original evidence and nested deliveries. Selected reading copies preserve exact bytes and original archive-member identities. Source-relative references remain meaningful in their original ZIP tree; they have not been silently rewritten in these copies.

The README mentions a separate adjacent `INTAKE_RECEIPT.json`, but the supplied inbox contains only the ZIP. Its outer SHA-256 is therefore this intake's computed identity, not a comparison with that unavailable sidecar. All supplied manifest payloads and CRCs pass; this receipt gap does not invent a mechanical blocker. The pinned interpreter is deliberately not bundled and was not sought. Exact reviewer model/backend is not stated in the main review/identity record.

[Source identities and package checks](../{S}/SOURCE_IDENTITIES.json) · [Intake completion](../{S}/INTAKE_RECORD.md) · [Validation](../{S}/VALIDATION.json).
'''
write(ROOT/'NEW'/R,review)
nav = f'''## Current apparatus mechanical closure — 2026-09-25

{status}

[Registered closure and exact checkpoint history]({R}) · [Complete independent review]({B}/{REPORT}) · [Intake and custody]({S}/INTAKE_RECORD.md).

This is the supplied independent mechanical disposition, conditional on a separate Jason-authorized commissioning task. No execution is authorized by this intake. The 05abf604 and intervening 9d31e790 holds remain checkpoint history; P's earlier engineering branches and scientific limitations remain unchanged. No scientific efficacy, developmental success, survival capability or ecological adequacy has been established.

'''
for name in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    text = (ROOT/'BEFORE'/name).read_text(encoding='utf-8-sig')
    first, rest = text.split('\n',1)
    rest = rest.replace('## Current independent apparatus review — 2026-09-24','## Preserved apparatus hold — 05abf604, 2026-09-24',1)
    write(ROOT/'AFTER'/name,first+'\n\n'+nav+rest.lstrip('\n'))
text = (ROOT/'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig')
first,rest = text.split('\n',1)
rest = rest.replace('## Current apparatus review — 2026-09-24','## Preserved apparatus hold — 05abf604, 2026-09-24',1)
continuation = f'''## Current apparatus mechanical closure — 2026-09-25

The [registered final independent review]({R}) of exact apparatus checkpoint `{CP}` reports **{DISPOSITION}**. A-R1a/b/c are closed within the reviewed scope; the original A-R2 clock-comparison defect remains closed. P at `{P}` is unchanged / previously verified; scientific status is **UNCOMMISSIONED / UNTESTED** and commissioning execution is **NOT STARTED**.

This updates current navigation only. The 05abf604 and intervening 9d31e790 HOLD dispositions remain preserved checkpoint history, not failed P mechanisms. Mechanical fitness is conditional on separate Jason execution authority: this intake grants no commissioning, tests, controller runs, repair, tuning, freeze or Git operation. Synthetic approvals and archived commands remain historical data. Preserve sources, candidates, earlier decisions and all existing scientific limitations.

'''
write(ROOT/'AFTER/AGENTS.md',first+'\n\n'+continuation+rest.lstrip('\n'))
register = (ROOT/'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
register += '\n## P final mechanical closure intake — 2026-09-25\n\n| ID | Source | Identity |\n|---|---|---|\n'
for entry in entries:
    register += f"| {entry['source_id']} | [{entry['original_filename']}]({quote(entry['path'])}) | {entry['bytes']} bytes; SHA-256 `{entry['sha256']}` |\n"
register += f'\nApparatus `{CP}`: **{DISPOSITION}**, as independently reviewed. Prior `{PREV}` remains HOLD history with A-R1a/b/c open at that checkpoint. P unchanged / previously verified; commissioning **NOT STARTED**; scientific status **UNCOMMISSIONED / UNTESTED**. [Registration and history]({R}) · [Custody and completion]({S}/INTAKE_RECORD.md). Adjacent final ZIP receipt was not supplied; the outer archive hash is computed here. No new execution authority is recorded.\n'
write(ROOT/'AFTER/SOURCE_REGISTER.md',register)

verification = {
    'incoming_zip':str(Z), 'zip_bytes':len(incoming), 'zip_sha256':sha(incoming),
    'archive_members':outer_check['members'], 'manifest_payloads_verified':outer_check['manifest_payloads_verified'], 'crc_passed':True,
    'outer_archive':outer_check, 'builder_archive':builder_check, 'intervening_review_archive':previous_check,
    'apparatus_checkpoint':CP, 'previous_hold_checkpoint':PREV, 'p_baseline_checkpoint':P, 'disposition':DISPOSITION,
    'builder_zip_sha256':sha(builder_bytes), 'builder_zip_bytes':len(builder_bytes),
    'intervening_review_zip_sha256':sha(previous_bytes), 'intervening_review_zip_bytes':len(previous_bytes),
    'intervening_report_matches_nested_original':True, 'intervening_builder_archive_copies_identical':True,
    'patch_matches_both_deliveries_and_recorded_identity':True,
    'p_modules_match_prior_registered_package':13, 'configuration_matches_prior_registered_package':True,
    'apparatus_files_match_reviewed_identities':len(identities['apparatus_runtime']['files']),
    'suite_logs_match_reported_summaries':True, 'source_closure_table_preserved_verbatim':True,
    'source_gap':'Adjacent INTAKE_RECEIPT.json referenced by source README not supplied; outer ZIP hash computed here.',
    'review_rerun':False, 'commissioning_execution':False, 'scientific_execution':False, 'git_operations':False}
session = ROOT/'NEW'/S
dump(session/'SOURCE_IDENTITIES.json',{'sources':entries, 'verification':verification, 'reviewed_identities_as_supplied':identities})
record = f'''# Final mechanical closure — intake completion

**Session:** `{ID}`; 2026-09-25. Integration authority is limited to Jason's requested inbox intake, following `IMPORT_NEW_MATERIAL.txt`.

{status}

Registered the [exact-checkpoint review](../../{R}) and preserved the intervening 9d31e790 HOLD report as history. The original 05abf604 HOLD, earlier P checkpoints, source archives, candidate alternatives and decision records retain their contents and exact dispositions. No new research or execution decision was created.

## What was read and changed

Read current `AGENTS.md`, research map/status and intake instructions; the complete final mechanical review, concise closure, README, reviewed identities, packaged controlling review request, complete previous HOLD review and provenance subreview. Parsed archive manifests and checkpoint metadata and checked suite-log summaries. This is registration/custody work, not another independent code review; reported scientific/runtime/test evidence remains attributed to the original reviewers.

Added the unchanged ZIP and ten original reading/metadata files as **SRC-083–093** in a unique source batch. Added one authored review registration and this unique session record. Updated five shared files: AGENTS, research map, workspace status, source catalog and source register. Older live hold headings are explicitly historical. No shared candidate or decision file was changed. The five preceding shared files are retained byte-for-byte in the session's local recovery ZIP.

## Actual checks

All **{outer_check['manifest_payloads_verified']} outer payloads** ({outer_check['members']} total members), **{builder_check['manifest_payloads_verified']} final builder payloads** ({builder_check['members']} members), and **{previous_check['manifest_payloads_verified']} intervening independent-review payloads** ({previous_check['members']} members) pass size/SHA-256, safe unique-path and CRC validation. The nested final builder identity matches the report; its checkpoint and exact patch agree with the outer review identities. The historical report matches its nested original byte-for-byte; both preserved copies of the intervening builder ZIP are identical.

All 13 delivered P modules and the configuration match the already registered 05abf604 delivery's unchanged P bytes. All {len(identities['apparatus_runtime']['files'])} apparatus files match the supplied individual reviewed identities. The two saved suite logs contain their reported 143-test summaries; no suite, fault fixture, probe, replay, archived program or controller was run here. Target Git/source/runtime/artifact preservation findings are attributed to the review; the actual repository was not accessed.

The outer ZIP is **{len(incoming):,} bytes**, SHA-256 `{sha(incoming)}`. No adjacent `INTAKE_RECEIPT.json` was supplied, although the README references one. This computed identity and complete supplied manifest checks are retained without claiming a comparison with that missing receipt. No extra chat export or unavailable interpreter was required.

[SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json) records custody; [VALIDATION.json](VALIDATION.json) records final navigation, previous-catalog-row, protected-file and shared-file checks. Missing source-relative links in isolated reading copies are not rewritten; the original ZIP preserves their complete paths and evidence.

## Stop point

No commissioning, scientific trial, prehistory generation, new experiment number, preregistration, implementation change, parameter tuning, Git operation or freeze occurred. No actual Loom repository, unrelated vault activity, settings or Atlas database was investigated or changed. All three mechanical blockers are reported closed within scope; any first commissioning task still needs Jason's separate authority. Intake complete; stop.
'''
write(session/'INTAKE_RECORD.md',record)
dump(ROOT/'PLAN.json',{'session':S,'batch':B,'review':R,'live_before':before,'protected_before':protected,'source_entries':entries,
    'verification':verification,'zip_source':str(Z),'old_catalog_count':old_count,'status':DISPOSITION})
print(json.dumps({'ready_to_validate':True,'outer':outer_check,'builder':builder_check,'previous_review':previous_check,
    'protected':len(protected),'sources':[e['source_id'] for e in entries],'review':R}))
