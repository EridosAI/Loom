"""Register operator-safe B1 hold; sealed evaluator archive remains opaque."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib,json,zipfile,shutil

ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
D=WB/'INBOX/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02'
Z=D/'B1_OPERATOR_REVIEW.zip'
PRIVATE=D/'B1_PRIVILEGED_EVALUATOR_HOLD.zip'
ID='2026-09-26-b1-held-intake-6e3ac812'
S='50_SESSIONS/'+ID
B='90_SOURCES/p_b1_held_preparation_2026-09-26_6e3ac812'
R=S+'/B1_HELD_PREPARATION_RECORD.md'
AUTH='45d71cd121f823368401b11c4a1010d509af3224f49168ad528653274d0e7543'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
CP='68db2c581f07200966d699a4f55a65f9b96df1e9'
A5R='50_SESSIONS/2026-09-26-a5-evidence-intake-82b4d9e1/A5_COMMISSIONING_EVIDENCE_RECORD.md'
STATUS='B1 PERCEPTUAL CEILING — PREPARED / HOLD / NOT LAUNCH-READY'
sha=lambda b:hashlib.sha256(b).hexdigest()
def fsha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
def write(p,t):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,o):write(p,json.dumps(o,indent=2,ensure_ascii=False)+'\n')

receipt=json.loads((D/'PACKAGE_RECEIPT.json').read_text(encoding='utf-8-sig'))
assert receipt['held_review_sha256']==AUTH and receipt['P']==P and receipt['apparatus']==CP
assert receipt['simulation_steps']==receipt['controller_calls']==receipt['new_prehistory_steps']==0
assert receipt['operator_material_contains_no_B1_state'] and receipt['documentation_revision']==2
assert fsha(Z)==receipt['public']['sha256'] and Z.stat().st_size==receipt['public']['bytes']
# Opaque byte-stream hashing/copying only. Never enumerate, decompress or read evaluator members.
assert fsha(PRIVATE)==receipt['privileged']['sha256'] and PRIVATE.stat().st_size==receipt['privileged']['bytes']
z=zipfile.ZipFile(Z)
names=z.namelist();assert len(names)==21 and len(set(names))==len({n.casefold() for n in names})==21
for n in names:
    p=PurePosixPath(n)
    assert len(p.parts)==1 and not p.is_absolute() and '..' not in p.parts and ':' not in n and '\\' not in n
mf=json.loads(z.read('FILE_MANIFEST.json'))
assert len(mf['files'])==receipt['public']['payloads']==20
assert set(mf['files'])==set(names)-{'FILE_MANIFEST.json'}
batch=ROOT/'SOURCE_BATCH';batch.mkdir(exist_ok=True)
shutil.copyfile(Z,batch/Z.name)
sealed_copy=batch/'SEALED_EVALUATOR_DO_NOT_OPEN'/PRIVATE.name
sealed_copy.parent.mkdir(exist_ok=True);shutil.copyfile(PRIVATE,sealed_copy)
assert fsha(sealed_copy)==receipt['privileged']['sha256']
incoming={str(Z):fsha(Z),str(PRIVATE):fsha(PRIVATE)}
for n in ['README.md','PACKAGE_RECEIPT.json','DELIVERY_RECEIPT.json','POST_SEAL_FILE_AUDIT.json']:
    dest=batch/'custody'/n;dest.parent.mkdir(exist_ok=True);shutil.copyfile(D/n,dest)
    incoming[str(D/n)]=fsha(D/n)
for n in names:
    data=z.read(n)
    if n in mf['files']:
        m=mf['files'][n];assert len(data)==m['bytes'] and sha(data)==m['sha256'],n
    assert data==(D/'B1_OPERATOR_REVIEW'/n).read_bytes(),n
    dest=batch/'B1_OPERATOR_REVIEW'/n;dest.parent.mkdir(exist_ok=True);dest.write_bytes(data)
    incoming[str(D/'B1_OPERATOR_REVIEW'/n)]=sha(data)
assert z.testzip() is None
held=json.loads(z.read('HELD_REVIEW_IDENTITY.json'))
assert held['sha256']==AUTH and held['no_grants']
assert held['private_archive']==receipt['privileged']
index=json.loads(z.read('CASE_AND_AUTHORITY_INDEX.json'))
cases={c['case']:c for c in index['cases']};assert len(cases)==6
assert all(c['execution_grant'] is None for c in cases.values())
assert list(cases)==['PC-LR','PC-MOTION','PC-CONTACT','PC-HOLD','B1-FULL-RAW','B1-CHEMISTRY-HIDDEN']
full=cases['B1-FULL-RAW'];hidden=cases['B1-CHEMISTRY-HIDDEN']
assert full['duration_seconds']==hidden['duration_seconds']==30
assert full['initial_state_sha256']==hidden['initial_state_sha256']
assert full['initial_snapshot_sha256']==hidden['initial_snapshot_sha256']
assert full['execution_specification_validation'] and not hidden['execution_specification_validation']
assert hidden['expected_rejection']=='unsupported display intervention'
checks=json.loads(z.read('PREPARATION_CHECKS.json'))
for k in ['worlds_constructed','Run_constructors','native_steps','field_steps','prehistory_steps','controller_command_calls','simulation_RNG_draws','human_trials','positive_control_demonstrations']:
    assert checks[k]==0,k
assert checks['pair_complete_initial_state_identical'] and checks['unsupported_hidden_candidate_rejected']
assert checks['initial_sensor_transductions']==5
static=json.loads(z.read('STATIC_COMPATIBILITY_FINDINGS.json'));assert static['source_checkpoint']==CP
assert static['chemistry_hidden']=='REJECTED by pure validate_execution: unsupported display intervention'
revision=json.loads(z.read('DOCUMENTATION_REVISION.json'));assert revision['revision']==2
delivery=json.loads((D/'DELIVERY_RECEIPT.json').read_text())
assert delivery['held_review_sha256']==AUTH and not delivery['privileged_expanded_in_workbench']
post=json.loads((D/'POST_SEAL_FILE_AUDIT.json').read_text())
assert post['canonical_review_hash']==AUTH and post['identical_paired_initial_state']
# The custody hash is corroborated by operator-safe records. Its sealed canonical object is intentionally not opened.

live=['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md','40_DECISIONS/DECISION_INDEX.md']
before={}
for n in live:
    data=(WB/n).read_bytes();before[n]={'bytes':len(data),'sha256':sha(data)}
    q=ROOT/'BEFORE'/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
protected={}
for folder in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS','50_SESSIONS']:
    for q in (WB/folder).rglob('*'):
        if q.is_file() and q.relative_to(WB).as_posix() not in live:protected[q.relative_to(WB).as_posix()]=fsha(q)
catalog=json.loads((ROOT/'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
old_count=len(catalog['source_files']);assert old_count==330
# Register only operator-safe reading material. No live link to the evaluator archive or its members.
selected=[Z.name]+['B1_OPERATOR_REVIEW/'+n for n in names]
entries=[]
for i,n in enumerate(selected,old_count+1):
    q=batch/n;member=PurePosixPath(n).name if n!=Z.name else None
    entries.append({'source_id':f'SRC-{i:03d}','path':B+'/'+n,'original_filename':PurePosixPath(n).name,'bytes':q.stat().st_size,'sha256':fsha(q),
        'role':'operator-safe-held-B1-preparation','prepared':'2026-09-26','registered':'2026-09-26',
        'stated_author':'Supplied B1 preparation packet; exact model/backend not stated',
        'acquired_from':str(Z)+'::'+member if member else str(Z),'archive_member':member,
        'authority':'Current Jason instruction to register held preparation and apparatus-defect classification; no implementation or execution',
        'held_review_custody_sha256':AUTH,'p_baseline_checkpoint':P,'pinned_apparatus_checkpoint':CP,'review_note':R,'record':S+'/INTAKE_RECORD.md',
        'status':STATUS,'blinding':'Operator-safe material only; evaluator archive retained opaque, not opened or linked in live navigation',
        'notes':'Two commissioning-apparatus defects; no B1/controller/human-trial execution, no perceptual/sensor/chemistry/P/Base World failure finding. Custody identity is not launch authority.'})
catalog['source_files']+=entries
catalog['intake_events'].append({'session_id':ID,'source_ids':[e['source_id'] for e in entries],'review_note':R,'record':S+'/INTAKE_RECORD.md',
    'held_review_custody_sha256':AUTH,'scope':STATUS+'; chemistry deprivation and live operator lifecycle are commissioning-apparatus defects; operator blinding preserved; no execution'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)
def src(n,label):return f'[{label}](../../{B}/B1_OPERATOR_REVIEW/{n})'
status='''P engineering: **previously VERIFIED; unchanged**  
Commissioning apparatus: **B1 HOLD — two commissioning-apparatus defects**  
Coupling commissioning: **IN PROGRESS**  
Physical ceiling A0–A5: **EXERCISED within its scoped bounded witness set**  
Perceptual ceiling B1: **PREPARED / HOLD / NOT LAUNCH-READY; NOT EXECUTED**  
Scientific/developmental efficacy: **UNTESTED**

| Commissioning item | Current status |
|---|---|
| V1 / V2 / V3 / A0 | COMPLETE |
| A1–A5 | OBSERVED within their bounded scopes |
| B1 | HELD BEFORE EXECUTION |
| B2–B4 | NOT EXECUTED |
| C1/C2 | NOT EXECUTED |'''
record=f'''# B1 perceptual ceiling — held preparation

**Registered:** 2026-09-26. **{STATUS}.**

Held review/custody identity: `{AUTH}`. This identifies the prepared review packet; it is **not execution authority**. P remains `{P}`; pinned apparatus `{CP}`. **No B1 simulation/controller execution occurred.**

{status}

## Prepared scope, still unexecuted

- Four sensor-only human positive controls.
- One 30-second FULL-RAW B1 source trial.
- One paired 30-second CHEMISTRY-HIDDEN B1 source trial.
- The two B1 trials share the same complete initial physical state, as recorded by matching opaque state/snapshot identities in the operator-safe index.
- Evaluator fixture/state remains separately sealed for operator blinding.

The {src('README.md','operator-safe packet entry')}, {src('CASE_AND_AUTHORITY_INDEX.json','opaque case/authority index')} and {src('HELD_REVIEW_IDENTITY.json','held identity record')} preserve this scope without disclosing the B1 test state. Four controls being prepared does not mean operator competence has been demonstrated; all six case grants remain null. The FULL-RAW condition remains held with the pair; its pure specification acceptance is not launch readiness.

## Observed preparation blockers

| Blocker | Observed preparation finding | Classification |
|---|---|---|
| CHEMISTRY DEPRIVATION | The pinned apparatus rejects the reviewed display-side chemistry-hidden condition as `unsupported display intervention`. | COMMISSIONING-APPARATUS DEFECT |
| LIVE OPERATOR LIFECYCLE | The live sensor-reference path requires correction of running / paused / ended handling before interactive human commissioning can be trusted, including submission handling. | COMMISSIONING-APPARATUS DEFECT |

The {src('OPEN_ISSUE_B1_INTERFACE.md','original open issue')} labels chemistry deprivation B1-H1. The requested lifecycle blocker encompasses its B1-H2 in-flight/queued-submission finding and B1-H3 live-launch/closed-state finding. The source's separate history-growth/resource observation remains in that document; it is not silently promoted into a third user-designated blocker. {src('STATIC_COMPATIBILITY_FINDINGS.json','Static compatibility findings')} retain exact source hashes and anchors.

These findings are **not perceptual failure, sensor inadequacy, chemistry inadequacy, P failure or a Base World defect**. No B1 outcome exists. The source proposes a future narrow apparatus correction/review; registration does not accept or implement that proposal, create a replacement interface or authorize any case.

## Zero-execution preparation and blinding boundary

The {src('PREPARATION_CHECKS.json','saved preparation checks')} report zero worlds/Run constructions, native/field/prehistory steps, controller-command calls, simulation RNG draws, human trials and positive-control demonstrations. Five zero-time initial transductions are explicitly reported as fixture preparation; this is not a claim of zero preparation calculations or an executed trajectory. No supplied validator, controller, UI, test or simulation was run by this intake.

**Operator blinding preserved during intake.** Only the designated operator-safe package and outer custody receipts were inspected. The evaluator ZIP was hashed/copied as opaque bytes; its member list, manifests, snapshots, hidden initial geometry, raw test readings and privileged fixture information were not opened, extracted or surfaced. It remains separately sealed and is not linked from live Markdown navigation or the reading-source register. The original inbox archive remains unchanged.

The two conditions' shared complete initial-state identity was corroborated through the public opaque index and preparation check, not by opening their sealed state. Likewise, the held custody identity was matched across operator-safe identity/receipt records and Jason's instruction; its privileged canonical object was deliberately not opened or recomputed. This is a scoped blinding-preserving custody check, not a claim of independent evaluator-state inspection. No necessary operator-safe source gap was found.

## Broader status and retained authority

The [A5 evidence record and preceding physical-ceiling chain](../../{A5R}) remain unchanged: A0–A5 physical ceiling exercised within bounded scope. B1 is held before execution; B2–B4 and C1/C2 remain not executed. Scientific/developmental efficacy remains UNTESTED. Prior engineering reviews and observations retain their reviewed scopes; the new B1 apparatus defects do not rewrite them as scientific failures.

The {src('REVIEW_AND_AUTHORITY_BOUNDARY.md','review/authority boundary')} preserves remaining correction, review, valid-packet, explicit authorization and operator-gate requirements. None is performed or granted by this intake. Canon, world/mechanism configuration and numerical settings are unchanged; no experiment number or Git operation is created.

## Custody and completion

Preserved the full operator ZIP, all 21 operator members and outer delivery metadata in a unique append-only batch, with a separate opaque evaluator-archive copy. Verified the operator archive checksum/CRC, all 20 payload hashes and expanded matches, and the evaluator archive's outer size/hash only. The source reports 102 evaluator payloads verified during preparation; this intake deliberately did not repeat that internal check. The source's documentation revision 2 remains unchanged.

New live navigation links only operator-safe material. Earlier sources/candidates/reviews/decisions/sessions and prior catalog rows remain preserved; previous shared notes have a recovery archive. [Intake completion](INTAKE_RECORD.md) · [Custody validation](VALIDATION.json).
'''
write(ROOT/'NEW'/R,record)
nav=f'''## Current commissioning boundary — B1 held before execution, 2026-09-26

{status}

**{STATUS}.** Held review/custody identity `{AUTH}`; not launch authority. Prepared: four sensor-only human positive controls, one 30-second FULL-RAW B1 source trial and one paired 30-second CHEMISTRY-HIDDEN B1 source trial, sharing the same complete initial physical state. Evaluator fixture/state remains separately sealed for operator blinding.

| Blocker | Classification |
|---|---|
| CHEMISTRY DEPRIVATION — pinned apparatus rejects the reviewed display-side chemistry-hidden condition | COMMISSIONING-APPARATUS DEFECT |
| LIVE OPERATOR LIFECYCLE — running / paused / ended handling requires correction before trusted interactive human commissioning | COMMISSIONING-APPARATUS DEFECT |

**No B1 simulation/controller execution occurred.** These are not perceptual failure, sensor inadequacy, chemistry inadequacy, P failure or a Base World defect. Do not open/surface sealed evaluator manifests, hidden initial geometry or privileged fixture information in live navigation. This intake grants no repair or execution and changes no canon or world/mechanism settings.

[B1 held preparation record]({R}) · [Operator-safe entry]({B}/B1_OPERATOR_REVIEW/README.md) · [Original apparatus issues]({B}/B1_OPERATOR_REVIEW/OPEN_ISSUE_B1_INTERFACE.md) · [A5 and physical-ceiling evidence]({A5R}). Earlier sections below retain dated states and bounded claims.

'''
for n in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    text=(ROOT/'BEFORE'/n).read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
    old='## Current coupling commissioning — A5 observed, physical ceiling exercised, 2026-09-26';assert old in rest
    rest=rest.replace(old,'## Preserved A5 intake — before B1 preparation hold, 2026-09-26',1)
    if n=='00_RESEARCH_MAP.md':
        old='coupling commissioning in progress; finite A0–A5 physical ceiling exercised within scoped witness set; perceptual ceiling next | A1–A5 observed external physical witnesses; P learning/developmental efficacy untested'
        assert old in rest
        rest=rest.replace(old,'coupling commissioning in progress; finite A0–A5 physical ceiling exercised; B1 prepared/held, two apparatus defects | A1–A5 observed external physical witnesses; B1 not executed; P learning/developmental efficacy untested',1)
    write(ROOT/'AFTER'/n,first+'\n\n'+nav+rest.lstrip('\n'))
text=(ROOT/'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
old='## Current commissioning evidence — A5 observed; physical ceiling exercised, 2026-09-26';assert old in rest
rest=rest.replace(old,'## Preserved A5 evidence intake — before B1 preparation hold, 2026-09-26',1)
continuation=f'''## Current commissioning boundary — B1 held before execution, 2026-09-26

The [registered operator-safe B1 preparation]({R}) is **{STATUS}**, held review/custody identity `{AUTH}`, not launch authority. Prepared scope: four sensor-only human positive controls and paired 30-second FULL-RAW / CHEMISTRY-HIDDEN B1 source trials from the same complete initial physical state. Evaluator fixture/state remains separately sealed.

Record two **COMMISSIONING-APPARATUS DEFECTS**: CHEMISTRY DEPRIVATION (pinned apparatus rejects reviewed display-side chemistry-hidden condition) and LIVE OPERATOR LIFECYCLE (running/paused/ended and submission handling need correction before interactive commissioning can be trusted). Do not classify either as perceptual failure, sensor/chemistry inadequacy, P failure or Base World defect. **No B1 simulation/controller execution occurred.**

**Preserve operator blinding: do not open or surface sealed evaluator manifests, hidden initial geometry or privileged fixture information in live navigation.** Use operator-safe material only for this status intake; evaluator archive remains opaque and separately sealed, with no live reading link. Static fixture preparation and null-grant specification checks do not establish operator competence or launch readiness. No correction or execution is authorized here.

A0–A5 physical ceiling remains exercised within bounded scope; B1 held before execution; B2–B4 and C1/C2 NOT EXECUTED; scientific/developmental efficacy UNTESTED. Prior P/engineering/evidence scope remains unchanged. No canon, world/mechanism/numerical setting change, experiment number or Git operation. Earlier statuses below are dated history. Stop after registration/status confirmation.

'''
write(ROOT/'AFTER/AGENTS.md',first+'\n\n'+continuation+rest.lstrip('\n'))
text=(ROOT/'BEFORE/40_DECISIONS/DECISION_INDEX.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
idx=f'''## B1 held preparation — no execution authority, 2026-09-26

[Operator-safe B1 hold record](../{R}): **{STATUS}**. Identity `{AUTH}` is review/custody only. Chemistry deprivation and live operator lifecycle are commissioning-apparatus defects; no perceptual/scientific failure is inferred. Four controls and paired 30-second conditions are prepared, unexecuted. Evaluator material remains sealed and is not linked here. A0–A5 bounded physical ceiling remains exercised; B2–B4/C1–C2 unexecuted; efficacy UNTESTED. This registers a hold, not apparatus-correction acceptance or execution approval. Prior decisions remain unchanged.

'''
write(ROOT/'AFTER/40_DECISIONS/DECISION_INDEX.md',first+'\n\n'+idx+rest.lstrip('\n'))
reg=(ROOT/'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
reg+='\n## B1 held preparation — operator-safe sources, 2026-09-26\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:reg+=f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
reg+=f'\n[Held record]({R}). Review/custody identity `{AUTH}`; {STATUS}. Two commissioning-apparatus defects; no B1 execution. Only operator-safe reading material is indexed here; privileged evaluator material remains sealed, opaque and unlinked.\n'
write(ROOT/'AFTER/SOURCE_REGISTER.md',reg)
verification={'incoming_zip':str(Z),'zip_bytes':Z.stat().st_size,'zip_sha256':fsha(Z),'manifest_payloads_verified':20,'archive_members':21,
    'operator_crc_passed':True,'operator_expanded_copies_match':21,'held_review_custody_identity':AUTH,
    'held_identity_check':'Matched current user instruction, operator-safe held identity and outer receipt; sealed canonical object not opened/recomputed',
    'opaque_evaluator_archive_sha256':fsha(PRIVATE),'opaque_evaluator_archive_bytes':PRIVATE.stat().st_size,
    'evaluator_archive_members_enumerated':False,'evaluator_archive_extracted':False,'evaluator_manifests_or_state_opened':False,
    'evaluator_internal_payload_verification_by_intake':False,'evaluator_live_reading_links_added':False,
    'matching_paired_initial_state_opaque_identities':True,'case_grants_reported_null':6,'preparation_execution_counts_zero':True,
    'source_initial_zero_time_transductions_reported':5,'documentation_revision':2,'classification':'COMMISSIONING-APPARATUS DEFECTS',
    'B1_executed':False,'tests_or_validators_run_by_intake':False,'git_operations':False,'necessary_operator_safe_source_gaps':[]}
inventory={q.relative_to(batch).as_posix():fsha(q) for q in batch.rglob('*') if q.is_file()}
dump(ROOT/'NEW'/S/'SOURCE_IDENTITIES.json',{'session_id':ID,'registered_operator_safe_sources':entries,'verification':verification,'complete_batch_opaque_sha256':inventory})
intake=f'''# B1 held-preparation intake — completion

Registered **{STATUS}**, review/custody identity `{AUTH}`. [Operator-safe hold record](B1_HELD_PREPARATION_RECORD.md). Chemistry deprivation and live operator lifecycle classified as COMMISSIONING-APPARATUS DEFECTS; no B1/controller execution or scientific failure finding.

Read current instructions/map/status and designated operator-safe entry, identity/index, issue, authority boundary, preparation/compatibility checks and documentation/session revision. Verified 20 operator payload hashes/CRCs and all 21 expanded copies. Copied the evaluator ZIP as opaque bytes and checked its outer size/hash only; never enumerated, extracted or opened its members. Matching paired state identity comes from operator-safe opaque hashes, not privileged state inspection. No fixture values or private reading links added to live navigation. Registered SRC-{old_count+1:03d}–SRC-{old_count+len(entries):03d}.

Added this session/source batch; updated AGENTS.md, 00_RESEARCH_MAP.md, 01_WORKSPACE_STATUS.md, SOURCE_CATALOG.json, SOURCE_REGISTER.md and 40_DECISIONS/DECISION_INDEX.md. Earlier sources/candidates/reviews/decisions/sessions and old catalog rows preserved. PRIOR_SHARED_NOTES.zip/receipt preserve all six prior shared files. [Validation](VALIDATION.json).

A0–A5 physical ceiling remains exercised within bounded scope; B1 held; B2–B4/C1–C2 unexecuted; efficacy UNTESTED. No canon, world/mechanism/numerical settings, actual repository, scientific interpretation, experiment number or Git operation changed. No apparatus fix, source validator, controller, live UI, trial or simulation run. No necessary operator-safe source gap. Stop after confirmation.
'''
write(ROOT/'NEW'/S/'INTAKE_RECORD.md',intake)
# Explicit navigation audit: no archive link or privileged member information was authored.
for group in ['NEW','AFTER']:
    for q in (ROOT/group).rglob('*.md'):
        t=q.read_text(encoding='utf-8');assert 'B1_PRIVILEGED_EVALUATOR_HOLD.zip' not in t and 'SEALED_EVALUATOR_DO_NOT_OPEN' not in t
dump(ROOT/'PLAN.json',{'session':S,'batch':B,'review':R,'live_before':before,'protected_before':protected,'source_entries':entries,
    'verification':verification,'zip_source':str(Z),'old_catalog_count':old_count,'status':STATUS,'incoming_before':incoming,'batch_inventory':inventory})
shutil.copyfile(ROOT.parent/'2026-09-26-a5-evidence-intake-82b4d9e1/publish_intake.py',ROOT/'publish_intake.py')
print(json.dumps({'prepared':ID,'operator_sources':len(entries),'protected_files':len(protected),'batch_files':len(inventory),'sealed_evaluator_contents_opened':False}),flush=True)
