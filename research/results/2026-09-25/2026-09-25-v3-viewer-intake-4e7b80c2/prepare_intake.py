"""Documentation-only continuation intake; never run supplied analysis or viewer code."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import json, hashlib, io, zipfile
ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ID='2026-09-25-v3-viewer-intake-4e7b80c2'
S=f'50_SESSIONS/{ID}'
B='90_SOURCES/p_a1_v3_reanalysis_viewer_2026-09-25_4e7b80c2'
R=S+'/A1_V3_REANALYSIS_AND_VIEWER_CONTINUATION.md'
D=WB/'INBOX/2026-09-25-A1-read-only-reanalysis-viewer-v1'
Z=D/'A1_READ_ONLY_REANALYSIS_VIEWER_v1.zip'
PRE='A1_READ_ONLY_REANALYSIS_VIEWER_v1/'
ORIG='90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4'
ORIG_SESSION='50_SESSIONS/2026-09-25-first-a1-evidence-intake-6ad829e4'
ORIG_RECORD=ORIG_SESSION+'/FIRST_A1_COMMISSIONING_EVIDENCE_RECORD.md'
AUTH='a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
CP='5f07748102cb5eaa302569c87efbae095050e9fe'
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,v):write(p,json.dumps(v,indent=2,ensure_ascii=False)+'\n')
raw=Z.read_bytes();receipt=json.loads((D/'DELIVERY_RECEIPT.json').read_text(encoding='utf-8-sig'))
assert len(raw)==receipt['zip']['bytes'] and sha(raw)==receipt['zip']['sha256']
z=zipfile.ZipFile(io.BytesIO(raw));names=z.namelist()
assert len(names)==len(set(names))==len({n.casefold() for n in names})
for n in names:
    p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and ':' not in n and '\\' not in n
mf=json.loads(z.read(PRE+'FILE_MANIFEST.json'))
assert {PRE+n for n in mf['files']}==set(names)-{PRE+'FILE_MANIFEST.json'}
for n,meta in mf['files'].items():
    b=z.read(PRE+n);assert len(b)==meta['bytes'] and sha(b)==meta['sha256'],n
assert z.testzip() is None
incoming_before={str(Z):sha(raw),str(D/'DELIVERY_RECEIPT.json'):sha((D/'DELIVERY_RECEIPT.json').read_bytes())}
for n in names:
    assert (D/n).read_bytes()==z.read(n),n
    incoming_before[str(D/n)]=sha(z.read(n))

original=z.read(PRE+'references/FIRST_A1_COMMISSIONING_RESULT.zip')
assert original==(WB/ORIG/'FIRST_A1_COMMISSIONING_RESULT.zip').read_bytes()
assert sha(original)==mf['original_A1_sha256']=='f37dfec92288fbe8a650b00eed611d086a3ece3b280292e95b891e371cc0d37f'
old=zipfile.ZipFile(io.BytesIO(original))
assert sha(old.read('evidence/APPROVED_OBJECT.canonical.json'))==AUTH
historical=['read_results.py','V3_BOUNDARY_ERROR.json','V3_POST_CHECK_LIMITATION.md','V3_COUNT_FINDING.json','A1_RESULT_SUMMARY.json']
history_matches={}
for n in historical:
    data=z.read(PRE+'references/historical-v3/'+n)
    assert data==old.read('evidence/read-only-review/'+n)==(WB/ORIG/'evidence/read-only-review'/n).read_bytes()
    history_matches[n]=sha(data)
assert z.read(PRE+'references/FIRST_A1_COMMISSIONING_REPORT.md')==(WB/ORIG/'FIRST_A1_COMMISSIONING_REPORT.md').read_bytes()
assert z.read(PRE+'HASH_BEFORE.json')==z.read(PRE+'HASH_AFTER.json')
custody=json.loads(z.read(PRE+'CUSTODY_PROOF.json'))
assert custody['P_checkpoint']==P and custody['apparatus_checkpoint']==CP and custody['input_before_equals_after'] is True
result=json.loads(z.read(PRE+'V3_RESULT_v1_1.json'))
vtests=json.loads(z.read(PRE+'V3_TEST_RESULTS.json'))
dtests=json.loads(z.read(PRE+'VIEWER_DATA_TEST_RESULTS.json'))
assert result['status']=='V3 COMPLETED — checks support the reviewed boundary claim'
assert result['evidence_sha256']==sha(original)
assert result['mapped_endpoint_rows']==result['native_records']==len(result['mapping'])==9183
assert result['sensor_entries']==9184 and result['initial_envelopes']==1
assert vtests['passed']==len(vtests['tests'])==20 and all(t['result']=='PASS' for t in vtests['tests'])
assert dtests['passed']==len(dtests['checks'])==14
assert vtests['checker_sha256']==result['checker_sha256']==sha(z.read(PRE+'v3_checker_v1_1.py'))
assert vtests['test_sha256']==sha(z.read(PRE+'test_v3_v1_1.py'))
assert dtests['test_sha256']==sha(z.read(PRE+'test_viewer_data.py'))
assert dtests['viewer_js_sha256']==sha(z.read(PRE+'viewer.js'))
assert dtests['viewer_data_sha256']==sha(z.read(PRE+'viewer_data.js'))
for k in ['simulation_steps','engine_instances','research_module_imports','physical_replays']:assert result[k]==0

live=['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md']
before={}
for n in live:
    b=(WB/n).read_bytes();before[n]={'bytes':len(b),'sha256':sha(b)}
    p=ROOT/'BEFORE'/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
protected={}
for folder in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS',ORIG_SESSION]:
    for p in (WB/folder).rglob('*'):
        if p.is_file():protected[p.relative_to(WB).as_posix()]=sha(p.read_bytes())
catalog=json.loads((ROOT/'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'));old_count=len(catalog['source_files']);assert old_count==117
batch=ROOT/'SOURCE_BATCH';batch.mkdir(exist_ok=True)
(batch/Z.name).write_bytes(raw);(batch/'DELIVERY_RECEIPT.json').write_bytes((D/'DELIVERY_RECEIPT.json').read_bytes())
# Preserve the entire package tree so all viewer assets and source-relative links remain available.
for n in names:
    p=batch/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
selected=[Z.name,'DELIVERY_RECEIPT.json']+[PRE+n for n in [
    'README.md','V3_READ_ONLY_REANALYSIS_REPORT.md','V3_RESULT_v1_1.json','V3_TEST_RESULTS.json','VIEWER_DATA_TEST_RESULTS.json',
    'VIEWER_DATA_FLOW.md','VIEWER_VERIFICATION.md','CUSTODY_PROOF.json','HASH_BEFORE.json','HASH_AFTER.json','FILE_MANIFEST.json',
    'v3_checker_v1_1.py','index.html','OPEN_A1_VIEWER.cmd','viewer.js','viewer_data.js','styles.css','STATIC_VIEWER_VALIDATION.html']]
entries=[]
for number,n in enumerate(selected,old_count+1):
    data=(batch/n).read_bytes()
    entries.append({'source_id':f'SRC-{number:03d}','path':B+'/'+n,'original_filename':PurePosixPath(n).name,'bytes':len(data),'sha256':sha(data),
        'role':'derived-read-only-analysis-and-viewer-source' if n.startswith(PRE) else 'derived-delivery-custody',
        'prepared':'2026-09-25','stated_author':'Supplied derived analysis/viewer; exact assistant model/backend not stated in report',
        'acquired_from':str(Z)+'::'+n if n.startswith(PRE) else str(D/n),'archive_member':n if n.startswith(PRE) else None,
        'authority':'Jason requests registration of completed reanalysis/viewer only; no new run, replay or scientific conclusion',
        'source_execution_authority_sha256':AUTH,'p_baseline_checkpoint':P,'reviewed_checkpoint':CP,
        'review_note':R,'record':S+'/INTAKE_RECORD.md','continues':ORIG_RECORD,
        'notes':'Complete original package tree preserved byte-for-byte; all remaining payload identities are in FILE_MANIFEST.json. Original A1 and failed V3 remain unchanged.'})
catalog['source_files']+=entries
catalog.setdefault('intake_events',[]).append({'session_id':ID,'source_ids':[e['source_id'] for e in entries],'review_note':R,'record':S+'/INTAKE_RECORD.md',
    'continues':ORIG_RECORD,'scope':'New read-only V3 analysis COMPLETE and derived passive viewer v1; same immutable A1, no new execution; efficacy UNTESTED'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)
status='''P engineering: **VERIFIED**  
Commissioning apparatus: **FIT / pre-run engineering CLOSED**  
Coupling commissioning: **IN PROGRESS**  
Scientific/developmental efficacy: **UNTESTED**

First bounded commissioning package:

- **V1 COMPLETE**
- **V2 COMPLETE**
- **V3 COMPLETE**
- **A0 COMPLETE**
- **A1 OBSERVED — one bounded external-control physical witness**

V3 status: **COMPLETED — checks support the reviewed boundary claim.**'''
def src(n,label):return f'[{label}](../../{B}/{PRE}{n})'
record=f'''# First A1 continuation — V3 reanalysis and passive viewer

**Registered:** 2026-09-25 under Jason's explicit continuation instruction. Continues the [existing first-commissioning record](../../{ORIG_RECORD}); no new commissioning run or experiment number is created.

{status}

Source execution authority remains `{AUTH}`. P remains `{P}`; apparatus remains `{CP}`. The original A1 ZIP remains SHA-256 `f37dfec92288fbe8a650b00eed611d086a3ece3b280292e95b891e371cc0d37f`.

## Four distinct records

| Layer | Preserved identity and relationship |
|---|---|
| Original A1 trajectory evidence | [Original result ZIP](../../{ORIG}/FIRST_A1_COMMISSIONING_RESULT.zip), one 91.83 s external-control witness, 9,183 native rows, administrative wall-limit stop; no retry/resume/replacement. The 28.17 s remainder remains unobserved. |
| Original failed V3 post-check | [Original checker](../../{ORIG}/evidence/read-only-review/read_results.py), [AssertionError](../../{ORIG}/evidence/read-only-review/V3_BOUNDARY_ERROR.json), [count finding](../../{ORIG}/evidence/read-only-review/V3_COUNT_FINDING.json), [limitation](../../{ORIG}/evidence/read-only-review/V3_POST_CHECK_LIMITATION.md). These remain byte-identical, including their historical incomplete disposition. |
| Corrected read-only V3 reanalysis | {src('V3_READ_ONLY_REANALYSIS_REPORT.md','New report')}, {src('V3_RESULT_v1_1.json','version 1.1.0 result')}, {src('v3_checker_v1_1.py','versioned checker source')}. A NEW READ-ONLY ANALYSIS of the SAME immutable A1 evidence; supersedes the live incomplete V3 conclusion only. |
| Derived passive viewer | **A1 passive read-only plan-view viewer v1**: {src('README.md','viewer entry and opening instructions')}, {src('index.html','viewer page')}, {src('STATIC_VIEWER_VALIDATION.html','saved visual verification')}. A downstream display of recorded evidence, not a simulation or additional result. |

## Completed V3 claim and validation

The corrected checker validates the contents of the documented initial sensor/display envelope and aligns all **9,183 native steps** with their sensor and diagnostic endpoint records. There are **9,184 sensor entries = one validated initial envelope + 9,183 endpoint rows**. The source report distinguishes start/endpoint raw values, held E/I timestamps, controller decision ownership and final record continuity; it does not simply discard an unexplained first row.

The supplied result reports 919 closed-schema controller inputs, 9,183 issued/delivered command comparisons, 459 body handoff samples, complete inactive-organism/RNG agreement at all 11 saved checkpoints and native RNG-counter agreement at all 9,183 endpoints. Neural wave rows remain zero. The final issued hold supplied three recorded steps and retained seven unexecuted steps; no continuation is implied.

Recorded validation:

- **20 V3 checker tests passed** — {src('V3_TEST_RESULTS.json','original test result record')}.
- **14 viewer-data checks passed** — {src('VIEWER_DATA_TEST_RESULTS.json','original viewer-data check record')}.

These are supplied analysis/display validation results, not new commissioning cases or tests rerun during intake. The reviewed boundary claim is evidence-level and remains limited by available records: full neural/RNG state is available at 11 saved checkpoints, while counters are available at every native endpoint. It does not claim observation of arbitrary unlogged transient memory states.

## Passive viewer scope

The {src('VIEWER_DATA_FLOW.md','data-flow document')} specifies extraction from the existing archive into display data, then browser rendering. The viewer does not instantiate or advance the simulation, issue commands, consume simulation RNG, tune P or modify raw evidence. Playback changes the selected saved record only. This is not a replay, continuation or replacement trajectory.

The {src('VIEWER_VERIFICATION.md','viewer verification report')} retains the display's limits: mover pose holds the latest recorded 0.1 s controller-geometry sample and shows sample age; exact event pose/reserves and native sensor/velocity/actuator values retain their separate timestamps. It does not interpolate physical samples or invent unrecorded mover motion. All original windows and the partial tail remain available; no learning/developmental animation is implied.

The supplied {src('OPEN_A1_VIEWER.cmd','local viewer launcher')} and all dependencies are preserved together. The packaged instructions describe its loopback read-only preview. No launcher, server, viewer, checker, test, extractor or reproduction command was executed during this intake. Prior reported browser verification is attributed to the supplied verification report.

## Authority, continuity and scientific boundary

Jason's current instruction authorizes registration and live status/navigation updates. The archived A1 approval belongs to the single original trajectory; neither this continuation nor the passive viewer grants new execution authority. This task proposes no mechanism, configuration, Base World, accepted architecture, canon or sequence change.

V1/V2/A0 and the bounded A1 observation retain their prior dispositions. The original failure remains a historical analysis result; the corrected analysis closes only the intended V3 record comparisons. The original force/integrity observations, positive/negative energetic windows, 91.83 s stop and source-accounting evidence are unchanged. The earlier window wording qualification remains: 459 complete fixed bins in total, 428 containing contact (229 positive-net, 199 negative-net), 31 without contact and one separate partial tail.

No A2–A5, B1–B4, C1/C2, newborn life, fixed-structure diagnostic, perceptual commissioning, developmental/scientific trial, efficacy testing, tuning/sweep or evidential freeze is added. One external physical witness and completed record-boundary checks establish no P discovery, perception, learning, regulation, survival or ecological adequacy. Scientific/developmental efficacy remains **UNTESTED**. Original candidate alternatives and all earlier checkpoint histories remain unchanged.

## Intake verification

The derived ZIP matches its external delivery receipt. All **53 payload files** and CRCs verify; all 54 extracted members match the supplied unpacked directory. The embedded original A1 ZIP is byte-identical to the already registered original. All five historical V3/summary reference copies match both that ZIP and the previously registered source files. HASH_BEFORE and HASH_AFTER match exactly; the versioned checker, tests and viewer-data identities match their supplied result records. The 20/14 counts are present in those preserved records.

This verifies custody and registration consistency, not an independent rerun of V3 or a fresh viewer audit. No source-identity/status conflict was found. {src('CUSTODY_PROOF.json','Supplied custody proof')} · [Intake completion](INTAKE_RECORD.md) · [Source identities](SOURCE_IDENTITIES.json) · [Final validation](VALIDATION.json).
'''
write(ROOT/'NEW'/R,record)
nav=f'''## Current A1 continuation — completed V3 and passive viewer, 2026-09-25

{status}

Source execution remains the single original A1 under authority `{AUTH}`; P `{P}`; apparatus `{CP}`. The corrected checker aligned all **9,183 native steps** using the documented initial sensor/display envelope. This is a **NEW READ-ONLY ANALYSIS of the SAME immutable A1 evidence**, not a replay, continuation or replacement trajectory. Original failed V3 artifacts remain preserved and byte-identical.

[Continuation and four-layer evidence record]({R}) · [Original A1 record]({ORIG_RECORD}) · [Corrected V3 report]({B}/{PRE}V3_READ_ONLY_REANALYSIS_REPORT.md) · [V3 result]({B}/{PRE}V3_RESULT_v1_1.json) · [Passive viewer v1 — entry and opening instructions]({B}/{PRE}README.md) · [Viewer page]({B}/{PRE}index.html).

Validation recorded: **20 V3 checker tests passed; 14 viewer-data checks passed**. The viewer is downstream of saved evidence only: no simulation construction/advancement, commands, simulation RNG, P tuning or raw-evidence modification. The original 91.83 s witness and unobserved 28.17 s remainder are unchanged. No new run, experiment number, scientific efficacy finding, canon/Base World/mechanism or commissioning-sequence change is created. The earlier incomplete post-check below remains a historical record.

'''
for name in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    text=(ROOT/'BEFORE'/name).read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
    rest=rest.replace('## Current coupling commissioning — first A1, 2026-09-25','## Preserved first A1 intake — before corrected V3 analysis, 2026-09-25',1)
    if name=='00_RESEARCH_MAP.md':
        oldrow='coupling commissioning in progress; V3 incomplete | bounded external A1 observed; learning/developmental efficacy untested'
        assert oldrow in rest;rest=rest.replace(oldrow,'coupling commissioning in progress; V1/V2/V3/A0 complete | one bounded external A1 observed; learning/developmental efficacy untested',1)
    write(ROOT/'AFTER'/name,first+'\n\n'+nav+rest.lstrip('\n'))
text=(ROOT/'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
rest=rest.replace('## Current commissioning evidence — 2026-09-25','## Preserved first A1 intake — before corrected V3 analysis, 2026-09-25',1)
current=f'''## Current A1 continuation — completed V3 and passive viewer, 2026-09-25

The [registered continuation]({R}) records **V3 COMPLETED — checks support the reviewed boundary claim** as a new read-only analysis of the same original A1 evidence under authority `{AUTH}`. V1/V2/V3/A0 are complete; A1 remains one observed bounded external-control witness. Coupling commissioning is **IN PROGRESS**; P engineering VERIFIED; apparatus FIT / pre-run engineering CLOSED; scientific/developmental efficacy **UNTESTED**.

Preserve four distinct layers: original A1 trajectory, original failed V3 post-check, corrected versioned V3 analysis and derived passive viewer v1. The original failed checker, AssertionError and limitation artifacts remain byte-identical; their earlier incomplete labels below are history. The recorded 20 V3 tests and 14 viewer-data checks belong to analysis/display validation, not new commissioning cases. The viewer reads saved evidence without simulation construction/advancement, commands, simulation RNG, tuning or raw-record changes. This intake authorizes no new run, replay, continuation, experiment number, canon/Base World/P mechanism/sequence change or Git operation.

'''
write(ROOT/'AFTER/AGENTS.md',first+'\n\n'+current+rest.lstrip('\n'))
register=(ROOT/'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
register+='\n## First A1 continuation — completed V3 / passive viewer v1, 2026-09-25\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:register+=f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
register+=f'\n[Continuation]({R}) of [the original A1 record]({ORIG_RECORD}). V3 complete by new read-only analysis; 20 checker tests and 14 viewer-data checks passed as recorded. Full derived package tree and original ZIP preserved, with all other payload identities in its manifest. Source execution authority `{AUTH}` is unchanged; no new run or efficacy result.\n'
write(ROOT/'AFTER/SOURCE_REGISTER.md',register)
verification={'incoming_zip':str(Z),'zip_bytes':len(raw),'zip_sha256':sha(raw),'manifest_payloads_verified':len(mf['files']),
    'archive_members':len(names),'crc_passed':True,'all_unpacked_inbox_members_match_zip':True,'original_A1_zip_matches_registered_source':True,
    'original_A1_zip_sha256':sha(original),'historical_V3_copies_verified':history_matches,'hash_before_after_byte_identical':True,
    'source_execution_authority_sha256':AUTH,'v3_checker_sha256':result['checker_sha256'],'recorded_v3_tests_passed':20,'recorded_viewer_data_checks_passed':14,
    'tests_or_analysis_rerun':False,'viewer_launched':False,'scientific_execution':False,'git_operations':False,'source_conflicts':[]}
session=ROOT/'NEW'/S
dump(session/'SOURCE_IDENTITIES.json',{'sources':entries,'verification':verification,'all_preserved_batch_files':{p.relative_to(batch).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in batch.rglob('*') if p.is_file()}})
record_short=f'''# V3 reanalysis / passive viewer — continuation intake complete

**Session:** `{ID}`; 2026-09-25. Jason authorized registration/status only. Continues [the first A1 record](../../{ORIG_RECORD}); no new commissioning run or experiment number.

{status}

[Continuation record](A1_V3_REANALYSIS_AND_VIEWER_CONTINUATION.md) distinguishes the original trajectory, original failed post-check, corrected V3 version 1.1.0 and derived passive viewer v1. The original record and all its source/failure artifacts remain unchanged. Updated only five shared files: AGENTS, research map, workspace status, source catalog and source register. Previous live incomplete status is labelled history; the map's P row points to current completed V3 status. No decision/candidate/canon/configuration/mechanism/sequence amendment was made.

Preserved the original ZIP, delivery receipt and complete 54-member unpacked tree in a unique append-only source batch. Registered {len(entries)} selected source/entry identities, **{entries[0]['source_id']}–{entries[-1]['source_id']}**; every remaining file retains its manifest identity. Viewer assets and source-relative links stay together. Source model/backend is not stated in the supplied main report.

Read current instructions/map/status and supplied README, full V3 report, viewer data-flow/verification, test/check result records, result metadata, manifests, custody and before/after inventories. Verified all 53 payload lengths/hashes and CRC, loose-tree agreement, exact original A1 ZIP identity, five original historical V3/summary copies and checker/test/viewer identities. Stored result contains 9,183 aligned rows, one initial envelope and recorded 20/14 passing checks. These are reported completed validation results; this intake reran none of the supplied code or checks.

No source conflict found. Full neural/RNG comparisons remain scoped to 11 saved checkpoints; every native endpoint has counter comparisons. Viewer sampling/timestamp limits remain in the continuation. No physical replay, simulation/command/RNG advancement, repeat/resume/replacement, efficacy result, tuning or Git operation occurred. The actual Loom repository and unrelated vault activity were not accessed.

[SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json) records exact custody; [VALIDATION.json](VALIDATION.json) records final links, protected-file/source-row preservation and shared changes. A local recovery ZIP retains the five prior shared files. Stop after registration.
'''
write(session/'INTAKE_RECORD.md',record_short)
batch_inventory={p.relative_to(batch).as_posix():sha(p.read_bytes()) for p in batch.rglob('*') if p.is_file()}
dump(ROOT/'PLAN.json',{'session':S,'batch':B,'review':R,'live_before':before,'protected_before':protected,'source_entries':entries,
    'verification':verification,'zip_source':str(Z),'old_catalog_count':old_count,'status':'V3 COMPLETED; COUPLING COMMISSIONING IN PROGRESS; EFFICACY UNTESTED',
    'incoming_before':incoming_before,'batch_inventory':batch_inventory})
print(json.dumps({'payloads_verified':len(mf['files']),'all_batch_files':len(batch_inventory),'source_ids':[entries[0]['source_id'],entries[-1]['source_id']],
    'historical_files_byte_identical':len(history_matches),'protected_existing':len(protected),'v3_status':result['status']}))
