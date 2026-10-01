"""Ingest sealed final review and update documentation; no scientific execution."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib, io, json, zipfile, shutil

ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
D=ROOT.parent/'2026-09-26-p-clock-final-review-68db2c58'
Z=D/'Loom_P_Narrow_Final_Clock_Review_68db2c58_20260926.zip'
ID='2026-09-26-final-clock-review-intake-3af846d2'
S='50_SESSIONS/'+ID
B='90_SOURCES/p_final_clock_review_2026-09-26_3af846d2'
R=S+'/FINAL_CLOCK_CORRECTION_REVIEW_RECORD.md'
HELD='90_SOURCES/p_a5_held_proposal_2026-09-26_62c8f4b1'
HR='50_SESSIONS/2026-09-26-a5-held-intake-62c8f4b1/A5_HELD_PROPOSAL_RECORD.md'
PREV='50_SESSIONS/2026-09-26-a5-clock-review-intake-91df630b/A5_CLOCK_REVIEW_AND_ACCEPTED_CORRECTION.md'
DEC='40_DECISIONS/DECISION-P-APPARATUS-CLOCK-2026-09-26-91df630b.md'
AUTH='88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6'
OLD='5f07748102cb5eaa302569c87efbae095050e9fe'
NEW='68db2c581f07200966d699a4f55a65f9b96df1e9'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
DISP='FIT FOR A5 LAUNCH-PACKET REGENERATION'
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,t):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,o):write(p,json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def safe_names(z):
    names=z.namelist()
    assert len(names)==len(set(names))==len({n.casefold() for n in names})
    for n in names:
        q=PurePosixPath(n)
        assert not q.is_absolute() and '..' not in q.parts and ':' not in n and '\\' not in n and not n.endswith('/')
    return names

raw=Z.read_bytes()
receipt=json.loads((D/'INTAKE_RECEIPT.json').read_text(encoding='utf-8-sig'))
assert sha(raw)==receipt['sha256']=='9167f3638bfca416b7f998d755a7e63f4633099699eaa398337a0fdfb359bc4a'
assert len(raw)==receipt['bytes']==6528490
assert sha(raw) in (D/(Z.name+'.sha256')).read_text()
assert receipt['disposition']==DISP and not receipt['A5_executed'] and not receipt['new_A5_authority_created'] and not receipt['launch_packet_regenerated']
z=zipfile.ZipFile(io.BytesIO(raw)); names=safe_names(z)
mf=json.loads(z.read('FILE_MANIFEST.json'))
assert len(names)==receipt['entries']==302
assert len(mf['files'])==receipt['manifest_payload_files']==301
assert {m['path'] for m in mf['files']}==set(names)-{'FILE_MANIFEST.json'}
for m in mf['files']:
    data=z.read(m['path']);assert sha(data)==m['sha256'] and len(data)==m['bytes'],m['path']
assert z.testzip() is None
incoming={}
for n in [Z.name,Z.name+'.sha256','INTAKE_RECEIPT.json']:
    incoming[str(D/n)]=sha((D/n).read_bytes())
for n in names:
    assert z.read(n)==(D/n).read_bytes(),n
expanded_verified={n:sha(z.read(n)) for n in names}
ident=json.loads(z.read('REVIEWED_IDENTITIES.json'))
assert ident['checkpoint']==NEW and ident['parent']==OLD and ident['P_checkpoint']==P and ident['held_A5']==AUTH and ident['disposition']==DISP
assert ident['final_preservation']['all_rehashed_unchanged']
assert not ident['A5_executed_by_review'] and not ident['A5_authority_created_by_review'] and not ident['launch_packet_regenerated']
builder_name='reviewed_delivery/Loom_P_Clock_Correction_Review_20260926.zip'
builder=z.read(builder_name)
assert sha(builder)==ident['builder_zip']['sha256']=='8c5e9322d06b4915ed31106770aff80e925666d961e389102c27a9ad4499e894'
inbox_builder=WB/'INBOX/2026-09-26-A5-clock-correction-68db2c58/Loom_P_Clock_Correction_Review_20260926.zip'
assert builder==inbox_builder.read_bytes();incoming[str(inbox_builder)]=sha(builder)
bz=zipfile.ZipFile(io.BytesIO(builder));bn=safe_names(bz)
bm=json.loads(bz.read('ARTIFACT_MANIFEST.json'))
assert bm['checkpoint']==NEW and not bm['execution_authority']
assert len(bn)==376 and len(bm['files'])==375
assert set(bm['files'])==set(bn)-{'ARTIFACT_MANIFEST.json'}
for n,m in bm['files'].items():
    data=bz.read(n);assert sha(data)==m['sha256'] and len(data)==m['bytes'],n
assert bz.testzip() is None
assert z.read('CLOCK_SCHEDULING_CORRECTION.patch')==bz.read('CLOCK_SCHEDULING_CORRECTION.patch')
assert sha(z.read('CLOCK_SCHEDULING_CORRECTION.patch'))==ident['patch']['sha256']
assert z.read('references/A5_CLOCK_COMPATIBILITY_REVIEW.md')==(WB/'90_SOURCES/p_a5_clock_review_2026-09-26_91df630b/A5_CLOCK_COMPATIBILITY_REVIEW/A5_CLOCK_COMPATIBILITY_REVIEW.md').read_bytes()
for n in ['CLOCK_SCHEDULING_CORRECTION_REPORT.md','NATIVE_INDEX_SCHEDULING_SPECIFICATION.md']:
    assert z.read('references/'+n)==bz.read(n),n
preserved_compare=[]
for n in bn:
    if n.startswith('developmental_ecology/loom_p/') or n in ['developmental_ecology/configuration.json','developmental_ecology/requirements-lock.txt','developmental_ecology/loom_commissioning/adapter.py']:
        assert bz.read(n)==(WB/HELD/'instrument'/n).read_bytes(),n
        preserved_compare.append(n)
assert len(preserved_compare)==16
assert sha((WB/HELD/'AUTHORITY_OBJECT.canonical.json').read_bytes())==AUTH
hm=json.loads((WB/HELD/'FILE_MANIFEST.json').read_text())
for n,m in hm['files'].items():
    data=(WB/HELD/n).read_bytes();assert sha(data)==m['sha256'] and len(data)==m['bytes'],n
audit=json.loads(z.read('FAULT_AND_SUITE_AUDIT.json'))
assert audit['pairs']==59 and audit['logs']==118 and audit['all_intended_exceptions_verified']
assert audit['collection']['total']==sum(audit['collection']['composition'].values())==176
assert len(audit['matrix_rows'])==59
for row in audit['matrix_rows']:
    for color,code in [('RED',1),('GREEN',0)]:
        assert row[color]['exit']==code
        name=f"regression/{row['matrix']}/{row['fault']}-{color}.log"
        assert sha(z.read(name))==row[color]['sha256'],name
for label in ['worktree','portable']:
    run=json.loads(z.read(f'regression/{label}-suite.json'))
    assert run['exit']==0 and b'176 passed' in z.read(f'regression/{label}-suite.log')
retro=json.loads(z.read('provenance/RETROSPECTIVE.json'))
assert retro['total']==5579 and retro['disagreements']==0
assert sum(c['saved_decisions'] for c in retro['cases'])==5579
for c in retro['cases']:
    assert not c['disagreements'] and len(c['rows'])==c['saved_decisions']==c['receipt_controller_count']
    assert all(row[2]==row[3]==row[4] for row in c['rows'])
schedule=json.loads(z.read('scheduling/new-results.json'))
assert schedule['held_A5_sha256']==AUTH
assert schedule['corrected_A']['complete_generic_manual_decision']['accepted']
assert schedule['corrected_B']['result']['accepted'] and schedule['corrected_B']['stage']==3

live=['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md','40_DECISIONS/DECISION_INDEX.md']
before={}
for n in live:
    data=(WB/n).read_bytes(); before[n]={'bytes':len(data),'sha256':sha(data)}
    q=ROOT/'BEFORE'/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
protected={}
for folder in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS','50_SESSIONS']:
    for q in (WB/folder).rglob('*'):
        if q.is_file() and q.relative_to(WB).as_posix() not in live:
            protected[q.relative_to(WB).as_posix()]=sha(q.read_bytes())
catalog=json.loads((ROOT/'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
old_count=len(catalog['source_files']);assert old_count==271
batch=ROOT/'SOURCE_BATCH';batch.mkdir(exist_ok=True)
for n in [Z.name,Z.name+'.sha256','INTAKE_RECEIPT.json']:(batch/n).write_bytes((D/n).read_bytes())
for n in names:
    q=batch/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(z.read(n))
selected=[Z.name,Z.name+'.sha256','INTAKE_RECEIPT.json','README.md','LOOM_P_NARROW_FINAL_CLOCK_REVIEW.md','CLOSURE_TABLE.md',
    'REVIEWED_IDENTITIES.json','FILE_MANIFEST.json','FAULT_AND_SUITE_AUDIT.json','FAULT_AND_SUITE_AUDIT.md','CLOCK_SCHEDULING_CORRECTION.patch',
    'scheduling/SCHEDULING_CLOSURE_REVIEW.md','scheduling/old-a-results.json','scheduling/old-b-results.json','scheduling/new-results.json',
    'scheduling/STATIC_A5_HOLDS.json','continuity/CONTINUITY_REVIEW.md','continuity/SOURCE_PRESERVATION.json',
    'regression/worktree-suite.json','regression/worktree-suite.log','regression/portable-suite.json','regression/portable-suite.log',
    'provenance/RETROSPECTIVE.json','provenance/FINAL_PRESERVATION.json','provenance/HELD_PRESERVATION.json',
    'references/NARROW_FINAL_REVIEW_REQUEST.txt','references/NATIVE_INDEX_SCHEDULING_SPECIFICATION.md',builder_name]
entries=[]
for i,n in enumerate(selected,old_count+1):
    data=(batch/n).read_bytes()
    entries.append({'source_id':f'SRC-{i:03d}','path':B+'/'+n,'original_filename':PurePosixPath(n).name,'bytes':len(data),'sha256':sha(data),
        'role':'final-narrow-apparatus-clock-correction-review','prepared':'2026-09-26','registered':'2026-09-26',
        'stated_author':'Supplied final independent narrow review; exact model/backend not stated',
        'acquired_from':str(Z)+'::'+n if n in names else str(D/n),'archive_member':n if n in names else None,
        'authority':'Current Jason instruction to ingest final review and register its bounded disposition; no packet regeneration or execution',
        'reviewed_apparatus_checkpoint':NEW,'previous_apparatus_checkpoint':OLD,'p_baseline_checkpoint':P,
        'historical_held_A5_sha256':AUTH,'review_disposition':DISP,'A5_executed':False,'review_note':R,'record':S+'/INTAKE_RECORD.md',
        'notes':'Clock correction verified within final review scope. Old held authority remains non-launchable; new packet required. A1–A4 retain original apparatus provenance. Full source bytes preserved.'})
catalog['source_files']+=entries
catalog['intake_events'].append({'session_id':ID,'source_ids':[e['source_id'] for e in entries],'review_note':R,'record':S+'/INTAKE_RECORD.md',
    'reviewed_apparatus_checkpoint':NEW,'previous_apparatus_checkpoint':OLD,'historical_held_A5_sha256':AUTH,
    'scope':DISP+'; clock blocker closed; old authority held/non-launchable; A5 design preserved, new packet required, not executed'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)
def src(n,label):return f'[{label}](../../{B}/{n})'
status='''P engineering: **VERIFIED within its prior reviewed scope; unchanged**  
Commissioning apparatus: **FIT FOR A5 LAUNCH-PACKET REGENERATION**  
Native-index scheduling correction: **VERIFIED; both long-horizon failures CLOSED**  
Coupling commissioning: **IN PROGRESS; A5 NOT EXECUTED**  
Scientific/developmental efficacy: **UNTESTED**

| A5 boundary | Current status |
|---|---|
| Design | PREPARED DESIGN PRESERVED |
| Historical authority | OLD AUTHORITY HELD / NON-LAUNCHABLE |
| Clock blocker | CLOSED |
| Preparation | NEW LAUNCH PACKET REQUIRED |
| Execution | A5 NOT EXECUTED |

V1/V2/V3/A0 remain COMPLETE; A1–A4 remain OBSERVED within their bounded scopes; B1–B4 and C1/C2 remain NOT EXECUTED.'''
record=f'''# Final narrow clock-correction review — registered disposition

**Registered:** 2026-09-26. **{DISP}.**

{status}

## Exact checkpoints and source

- Previous apparatus: `{OLD}`.
- Corrected apparatus reviewed: `{NEW}`.
- P remains `{P}`.
- Historical held A5 proposal: `{AUTH}`.

The {src('LOOM_P_NARROW_FINAL_CLOCK_REVIEW.md','complete final independent review')} and {src('CLOSURE_TABLE.md','closure table')} govern this bounded engineering disposition. They were acquired from the sealed local review export, not confused with the earlier builder submission in the inbox. The {src('REVIEWED_IDENTITIES.json','reviewed identities')} and {src(Z.name,'complete review ZIP')} preserve exact provenance. The byte-identical {src(builder_name,'nested builder package')} is retained as the reviewed delivery; its earlier “for review” wording is historical.

## Findings recorded from the final review

| Item | Final review finding |
|---|---|
| Native-index controller scheduling correction | VERIFIED |
| Physical clock/world timing | Unchanged; original accumulated physical time retained |
| First diagnosed long-horizon failure | CLOSED: valid native-26,950 decision accepted |
| Independent 270 s stage-transition failure | CLOSED: native 27,000 owns stage 3; legal hold accepted |
| Worktree suite | 176 passed |
| Portable suite | 176 passed |
| Consequential fault/control pairs | 59 verified, with 118 intended RED/GREEN logs |
| Saved A1–A4 controller decisions | 5,579 checked |
| Historical stage-assignment disagreements | Zero |
| P/configuration/world laws | Unchanged |

Evidence: {src('scheduling/SCHEDULING_CLOSURE_REVIEW.md','scheduling closure')}, {src('scheduling/new-results.json','corrected boundary results')}, {src('regression/worktree-suite.log','worktree suite log')}, {src('regression/portable-suite.log','portable suite log')}, {src('FAULT_AND_SUITE_AUDIT.json','fault/suite audit')}, {src('provenance/RETROSPECTIVE.json','historical comparisons')} and {src('continuity/SOURCE_PRESERVATION.json','physical source preservation')}.

The final review checked all 63,001 schedule indices and 6,300 prescribed holds as static/scalar scheduling evidence. Its three generic 0.3 s physical components and detached late states establish bounded timing/restart coverage, not an A5 trajectory or long ecological integration. The implemented separate binary64 consistency envelope validates physical timestamps without choosing stages or changing physical event tolerance. The earlier recommendation and current implemented specification retain their own exact wording and scope.

The review preserves its initial reviewer source-comparison setup error and corrected comparator; that failed attempt is not erased or classified as apparatus/scientific failure. The 59 pairs retain the audit's distinction between test-callback authority negatives and production-guard mutations; this record does not inflate their coverage.

## A5 boundary and unchanged historical evidence

The [prepared A5 design](../../{HR}), route, stages, initial-state prescription and 630 s horizon are preserved. The [historical HOLD packet](../../{HELD}/A5_LAUNCH_PACKET_HOLD.zip) and [canonical authority bytes](../../{HELD}/AUTHORITY_OBJECT.canonical.json) remain unchanged under hash `{AUTH}`. That object binds the old apparatus and remains ungranted/non-launchable. Closing the clock blocker does not make that old authority usable with the corrected apparatus.

**A new launch packet is required. No packet was regenerated and no new execution authority was created by this intake. A5 was not executed.** The final disposition is fitness for launch-packet regeneration, not launch authorization or an ecological result.

A1–A4 remain historical observed commissioning evidence from their original apparatus checkpoint(s), including `{OLD}`. Their 5,579-decision comparison is read-only compatibility evidence; they are **not relabelled as having run under `{NEW}`**. No replay, continuation, migration, changed interpretation or replacement trajectory follows. Earlier physical observations and limitations remain as recorded. Scientific/developmental efficacy remains UNTESTED.

## Continuation and custody

This closes the clock blocker recorded in the [prior diagnosis/acceptance continuation](../../{PREV}) and follows the unchanged [explicit Jason decision](../../{DEC}). Those dated records, earlier checkpoint dispositions, sources and all candidate alternatives remain preserved. Current navigation now points to the final closure without rewriting prior history.

Intake checked the final archive checksum/CRC, all 301 payload hashes and 302 expanded source files, the nested builder archive's 375 payload hashes, saved suite receipts/logs, all 118 fault-log identities, and the saved 5,579 comparison rows. Sixteen packaged P/configuration/requirements/adapter files match the held instrument copies. All 89 registered held payloads and the held canonical identity were checked. No supplied test, review harness, controller or simulation was run during intake; the scientific/engineering findings above are attributed to the final review, not independently rerun here.

No necessary source gap or identity conflict was found. Canon, actual repository documents, P, Base World configuration, A5 design/routes, numerical settings and scientific interpretation were not changed. No experiment number or Git operation was created/performed.

[Source identities](SOURCE_IDENTITIES.json) · [Intake completion](INTAKE_RECORD.md) · [Validation](VALIDATION.json).
'''
write(ROOT/'NEW'/R,record)
nav=f'''## Current commissioning boundary — final clock correction verified, 2026-09-26

{status}

Corrected apparatus: `{NEW}`. Previous apparatus: `{OLD}`. Native-index scheduling is verified; physical clock/world timing, P, configuration, world laws and A5 route/design remain unchanged. Both previously diagnosed long-horizon failures are closed. Final independent review: **176 worktree tests passed; 176 portable tests passed; 59 consequential fault/control pairs verified; 5,579 saved A1–A4 decisions checked; zero historical stage-assignment disagreements**.

Historical held A5 hash `{AUTH}` and the HOLD packet remain unchanged and non-launchable. A new launch packet is required; none is created by this intake. A1–A4 retain original apparatus provenance and interpretations and are not relabelled as executions under 68db2c58. No A5 execution, experiment number, canon change or scientific efficacy claim follows.

[Final review registration]({R}) · [Complete independent review]({B}/LOOM_P_NARROW_FINAL_CLOCK_REVIEW.md) · [Closure table]({B}/CLOSURE_TABLE.md) · [Preserved held design/authority]({HR}) · [Accepted correction decision]({DEC}). Earlier sections below preserve their dated dispositions.

'''
for n in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    text=(ROOT/'BEFORE'/n).read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
    old='## Current commissioning boundary — A5 clock correction accepted, 2026-09-26'
    assert old in rest
    rest=rest.replace(old,'## Preserved correction acceptance — before final verification, 2026-09-26',1)
    if n=='00_RESEARCH_MAP.md':
        old='coupling commissioning in progress; V1/V2/V3/A0 complete; A5 held before execution | A1–A4 observed external-control witnesses; A5 apparatus clock correction accepted, implementation/verification outstanding; learning/developmental efficacy untested'
        assert old in rest
        rest=rest.replace(old,'coupling commissioning in progress; V1/V2/V3/A0 complete; A5 not executed, new packet required | A1–A4 observed under original apparatus; A5 clock correction verified, old authority held/non-launchable; learning/developmental efficacy untested',1)
    write(ROOT/'AFTER'/n,first+'\n\n'+nav+rest.lstrip('\n'))
text=(ROOT/'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
old='## Current continuation — apparatus clock correction accepted, 2026-09-26';assert old in rest
rest=rest.replace(old,'## Preserved apparatus correction acceptance — before final verification, 2026-09-26',1)
continuation=f'''## Current continuation — final clock correction verified, 2026-09-26

The [final narrow review]({R}) of apparatus `{NEW}`, following `{OLD}`, is registered as **{DISP}**. Native-index scheduling correction VERIFIED; both long-horizon failures CLOSED; physical clock/world timing unchanged. Final review records 176 worktree and 176 portable tests passed, 59 verified fault/control pairs, 5,579 saved A1–A4 decisions and zero historical stage disagreements. P, configuration/world laws and A5 route/design remain unchanged.

**A5: PREPARED DESIGN PRESERVED; OLD AUTHORITY HELD / NON-LAUNCHABLE; CLOCK BLOCKER CLOSED; NEW LAUNCH PACKET REQUIRED; A5 NOT EXECUTED.** Preserve the exact historical HOLD packet and authority hash `{AUTH}`. No regenerated packet or A5 execution is authorized by this status intake. A1–A4 stay historical evidence from their original apparatus checkpoints and retain their interpretations; do not relabel them as 68db2c58 runs. V1/V2/V3/A0 COMPLETE; A1–A4 OBSERVED; B1–B4 and C1/C2 NOT EXECUTED; scientific/developmental efficacy UNTESTED.

This supersedes the live implementation/verification-outstanding wording for the narrow correction only. Earlier decisions, reviews, sources and checkpoint dispositions below retain their dated meaning. This task changes documentation/status only, with no canon/P/Base World/numerical/route/design/scientific-interpretation change, experiment number, trial or Git operation.

'''
write(ROOT/'AFTER/AGENTS.md',first+'\n\n'+continuation+rest.lstrip('\n'))
text=(ROOT/'BEFORE/40_DECISIONS/DECISION_INDEX.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
old='## Accepted apparatus clock correction — 2026-09-26';assert old in rest
rest=rest.replace(old,'## Preserved acceptance-stage decision — before final verification, 2026-09-26',1)
idx=f'''## Final verification of accepted clock correction — 2026-09-26

The [registered final narrow review](../{R}) verifies the correction at `{NEW}` and closes both clock failures: **{DISP}**. The [original accepted decision]({PurePosixPath(DEC).name}) and all prior records remain unchanged. A5 design is preserved; old authority `{AUTH}` remains held/non-launchable; new launch packet required; A5 not executed. This is an engineering-completion/status continuation, not new execution authority or a new research decision.

'''
write(ROOT/'AFTER/40_DECISIONS/DECISION_INDEX.md',first+'\n\n'+idx+rest.lstrip('\n'))
reg=(ROOT/'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
reg+='\n## Final narrow clock-correction review — 2026-09-26\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:reg+=f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
reg+=f'\n[Final review record]({R}). Exact apparatus `{NEW}`: **{DISP}**. Both clock failures closed; physical timing and P/world preserved. Historical held authority `{AUTH}` stays non-launchable; new packet required; A5 not executed. Prior A1–A4 identities/interpretations unchanged.\n'
write(ROOT/'AFTER/SOURCE_REGISTER.md',reg)
verification={'incoming_zip':str(Z),'zip_bytes':len(raw),'zip_sha256':sha(raw),'manifest_payloads_verified':301,'archive_members':302,
    'crc_passed':True,'all_expanded_source_members_match_zip':True,'expanded_copy_check_phase':'preparation; publication rechecks sealed archive and source-batch hashes','receipt_and_sidecar_match':True,
    'nested_builder_payload_hashes_verified':375,'nested_builder_matches_inbox_archive':True,'past_diagnosis_source_matches_archive':True,
    'packaged_protected_instrument_files_match_held':len(preserved_compare),'held_payloads_verified':len(hm['files']),
    'held_canonical_sha256':AUTH,'reported_worktree_tests_passed':176,'reported_portable_tests_passed':176,
    'reported_consequential_fault_control_pairs':59,'saved_fault_log_hashes_verified':118,'saved_retrospective_rows_checked':5579,
    'saved_stage_disagreements':0,'disposition':DISP,'corrected_apparatus':NEW,'previous_apparatus':OLD,
    'A5_executed':False,'packet_regenerated':False,'new_authority_created':False,'programs_or_tests_rerun_during_intake':False,
    'git_operations':False,'necessary_source_gaps':[],'source_identity_conflicts':[]}
inventory={q.relative_to(batch).as_posix():sha(q.read_bytes()) for q in batch.rglob('*') if q.is_file()}
dump(ROOT/'NEW'/S/'SOURCE_IDENTITIES.json',{'session_id':ID,'registered_sources':entries,'verification':verification,'complete_batch_sha256':inventory,'expanded_review_copies_verified_at_preparation':expanded_verified})
intake=f'''# Final narrow clock review — intake completion

Registered final independent review of `{NEW}` as **{DISP}**. [Full registration](FINAL_CLOCK_CORRECTION_REVIEW_RECORD.md).

Read current AGENTS/map/status, acceptance history/index, full final review, closure table, implementation report/specification and supporting identity/audit records. Located the sealed final review in the local review export; the inbox correction ZIP is its earlier builder input. Preserved all 302 final-review members, original ZIP, checksum and receipt, including the nested byte-identical builder ZIP and preserved reviewer setup failure.

Verified 301 review payload hashes/CRCs, 375 nested builder payloads, 118 fault-log hashes, saved suite exits/pass summaries, 5,579 saved comparison rows, 16 protected instrument copies, all 89 held payloads and the old canonical hash. These are document/evidence-custody checks; no review harness, test suite, controller or simulation was executed by intake. Registered SRC-{old_count+1:03d}–SRC-{old_count+len(entries):03d}.

Updated only AGENTS.md, 00_RESEARCH_MAP.md, 01_WORKSPACE_STATUS.md, SOURCE_CATALOG.json, SOURCE_REGISTER.md and 40_DECISIONS/DECISION_INDEX.md, plus this new session/source batch. Prior source/candidate/review/decision/session bytes and earlier catalog rows remain preserved. PRIOR_SHARED_NOTES.zip and its receipt retain all six prior live notes. [Validation](VALIDATION.json) · [Source identities](SOURCE_IDENTITIES.json).

A5 design preserved; old authority held/non-launchable; clock blocker closed; new launch packet required; A5 not executed. A1–A4 retain original apparatus provenance and scientific interpretation. No new packet/authority, experiment number, Git operation or canonical repository change. Scientific/developmental efficacy remains UNTESTED. No necessary source gap found. Stop after status confirmation.
'''
write(ROOT/'NEW'/S/'INTAKE_RECORD.md',intake)
dump(ROOT/'PLAN.json',{'session':S,'batch':B,'review':R,'live_before':before,'protected_before':protected,'source_entries':entries,
    'verification':verification,'zip_source':str(Z),'old_catalog_count':old_count,'status':DISP+'; old A5 authority held/non-launchable; A5 not executed',
    'incoming_before':incoming,'batch_inventory':inventory})
shutil.copyfile(ROOT.parent/'2026-09-26-a5-clock-review-intake-91df630b/publish_intake.py',ROOT/'publish_intake.py')
print(json.dumps({'prepared':ID,'sources':len(entries),'protected_files':len(protected),'batch_files':len(inventory)}))
