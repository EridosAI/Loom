"""Documentation-only intake of an existing narrow review; never execute its code."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib, io, json, shutil, zipfile, xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
D=ROOT.parent/'2026-09-26-b1-review-352f73ff'
Z=D/'Loom_P_B1_Narrow_Independent_Review_352f73ff_20260926.zip'
ID='2026-09-26-b1-final-review-intake-f04e8c72'
S='50_SESSIONS/'+ID
B='90_SOURCES/p_b1_final_review_2026-09-26_f04e8c72'
R=S+'/FINAL_B1_OPERATOR_APPARATUS_REVIEW_RECORD.md'
HR='50_SESSIONS/2026-09-26-b1-held-intake-6e3ac812/B1_HELD_PREPARATION_RECORD.md'
HB='90_SOURCES/p_b1_held_preparation_2026-09-26_6e3ac812'
A5R='50_SESSIONS/2026-09-26-a5-evidence-intake-82b4d9e1/A5_COMMISSIONING_EVIDENCE_RECORD.md'
AUTH='45d71cd121f823368401b11c4a1010d509af3224f49168ad528653274d0e7543'
OLD='68db2c581f07200966d699a4f55a65f9b96df1e9'
CP='352f73fffa6d9781eae8aa38e708a9a05669588f'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
STATUS='FIT FOR B1 LAUNCH-PACKET REGENERATION'
sha=lambda b:hashlib.sha256(b).hexdigest()
def fsha(p):
    h=hashlib.sha256()
    with Path(p).open('rb') as f:
        for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
    return h.hexdigest()
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

receipt=json.loads((D/'INTAKE_RECEIPT.json').read_text(encoding='utf-8-sig'))
assert fsha(Z)==receipt['sha256']=='4163bd5560b2fbdbad88954f96e7ebed4bdabb445062b5b293ef1609e5ae5ebc'
assert Z.stat().st_size==receipt['bytes']==28685146
assert receipt['sha256'] in (D/(Z.name+'.sha256')).read_text()
assert receipt['disposition']==STATUS
for k in ['prepared_controls_executed','B1_executed','new_launch_authority','launch_packet_regenerated','hidden_snapshot_decoded','hidden_state_disclosed']:assert receipt[k] is False
z=zipfile.ZipFile(Z);names=safe_names(z)
assert len(names)==receipt['entries']==254
mf=json.loads(z.read('FILE_MANIFEST.json'))
assert len(mf['files'])==receipt['manifest_payload_files']==253
assert {m['path'] for m in mf['files']}==set(names)-{'FILE_MANIFEST.json'}
for m in mf['files']:
    data=z.read(m['path']);assert len(data)==m['bytes'] and sha(data)==m['sha256'],m['path']
assert z.testzip() is None
assert not any('B1_PRIVILEGED_EVALUATOR_HOLD/' in n or 'B1-PAIR-INITIAL.snapshot' in n for n in names)
for n in names:assert fsha(D/n)==sha(z.read(n)),n
ident=json.loads(z.read('REVIEWED_IDENTITIES.json'))
assert ident['checkpoint']==CP and ident['parent']==OLD and ident['P_checkpoint']==P
assert ident['held_review_hash']==AUTH and ident['disposition']==STATUS
assert ident['final_preservation']['all_unchanged']
for k in ['prepared_controls_executed','B1_executed','new_launch_authority','launch_packet_regenerated','hidden_snapshots_decoded','hidden_state_disclosed']:assert ident[k] is False
assert ident['static_compatibility']['pair_identical_complete_initial_state']
assert ident['static_compatibility']['pair_only_case_id_and_declared_display_differ']

# The review's builder ZIP is a public correction package, not the sealed evaluator ZIP.
builder_name='reviewed_delivery/B1_OPERATOR_APPARATUS_CORRECTION_REVIEW.zip'
builder=z.read(builder_name)
assert sha(builder)==ident['builder_zip']['sha256']=='0166f1395e9f10fba96e05f5d53264ba2fc275db2122087810406107e3ccf318'
inbox=WB/'INBOX/2026-09-26-B1-operator-correction-352f73ff-review-02'
assert fsha(inbox/'B1_OPERATOR_APPARATUS_CORRECTION_REVIEW.zip')==sha(builder)
bz=zipfile.ZipFile(io.BytesIO(builder));bn=safe_names(bz)
prefix='B1_OPERATOR_APPARATUS_CORRECTION_REVIEW/'
assert all(n.startswith(prefix) for n in bn)
bm=json.loads(bz.read(prefix+'PAYLOAD_MANIFEST.json'))
assert bm['checkpoint']==CP
assert len(bn)==2677 and len(bm['files'])==2676
assert {prefix+n for n in bm['files']}==set(bn)-{prefix+'PAYLOAD_MANIFEST.json'}
for n,m in bm['files'].items():
    data=bz.read(prefix+n);assert sha(data)==m['sha256'] and len(data)==m['bytes'],n
assert bz.testzip() is None
assert z.read('EXACT_DIFF_68db2c58_to_352f73ff.patch')==bz.read(prefix+'EXACT_DIFF_68db2c58_to_352f73ff.patch')
assert sha(z.read('EXACT_DIFF_68db2c58_to_352f73ff.patch'))==ident['patch']['sha256']

# Read saved component evidence; do not rerun tests, validators, controllers or UI.
audit=json.loads(z.read('FAULT_AND_SUITE_AUDIT.json'))
assert audit['pairs']==12 and audit['logs']==24 and audit['all_actual_failure_frames_verified']
assert len(audit['rows'])==12 and {row['fault'] for row in audit['rows']}==set('ABCDEFGHIJKL')
for row in audit['rows']:
    for color,exit_code in [('RED',1),('GREEN',0)]:
        info=row[color];base='regression/'+row['fault']+'-'+color
        assert info['exit']==exit_code
        assert sha(z.read(base+'.log'))==info['log_sha256']
        assert sha(z.read(base+'.xml'))==info['junit_sha256']
        assert json.loads(z.read(base+'.json'))['exit']==exit_code
        root=ET.fromstring(z.read(base+'.xml'))
        cases=list(root.iter('testcase'));assert len(cases)==1
        failures=list(root.iter('failure'));assert len(failures)==(1 if color=='RED' else 0)
        assert not list(root.iter('error')) and not list(root.iter('skipped'))
test_ids=[]
for label in ['worktree-suite','portable-suite']:
    summary=audit['suites'][label]
    assert summary['all_cases_passed'] and sum(summary['composition'].values())==204
    assert '204 passed' in summary['summary']
    assert json.loads(z.read('regression/'+label+'.json'))['exit']==0
    assert b'204 passed' in z.read('regression/'+label+'.log')
    root=ET.fromstring(z.read('regression/'+label+'.xml'))
    cases=list(root.iter('testcase'));assert len(cases)==204
    assert not list(root.iter('failure')) and not list(root.iter('error')) and not list(root.iter('skipped'))
    test_ids.append(sorted((t.attrib.get('classname'),t.attrib['name']) for t in cases))
assert test_ids[0]==test_ids[1]

live=['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md','40_DECISIONS/DECISION_INDEX.md']
before={}
for n in live:
    data=(WB/n).read_bytes();before[n]={'bytes':len(data),'sha256':sha(data)}
    q=ROOT/'BEFORE'/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
protected={}
for folder in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS','50_SESSIONS']:
    for q in (WB/folder).rglob('*'):
        if q.is_file() and q.relative_to(WB).as_posix() not in live:protected[q.relative_to(WB).as_posix()]=fsha(q)
incoming={str(D/n):fsha(D/n) for n in [Z.name,Z.name+'.sha256','INTAKE_RECEIPT.json']}
incoming[str(inbox/'B1_OPERATOR_APPARATUS_CORRECTION_REVIEW.zip')]=sha(builder)
# Preserve the previous held INBOX as opaque file custody, never parse evaluator content.
held_inbox=WB/'INBOX/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02'
for q in held_inbox.iterdir():
    if q.is_file():incoming[str(q)]=fsha(q)
for q in (held_inbox/'B1_OPERATOR_REVIEW').rglob('*'):
    if q.is_file():incoming[str(q)]=fsha(q)
old_held_receipt=json.loads((WB/HB/'custody/PACKAGE_RECEIPT.json').read_text(encoding='utf-8-sig'))
assert old_held_receipt['held_review_sha256']==AUTH
sealed=WB/HB/'SEALED_EVALUATOR_DO_NOT_OPEN/B1_PRIVILEGED_EVALUATOR_HOLD.zip'
assert fsha(sealed)==old_held_receipt['privileged']['sha256']
assert sealed.stat().st_size==old_held_receipt['privileged']['bytes']
assert fsha(held_inbox/'B1_PRIVILEGED_EVALUATOR_HOLD.zip')==fsha(sealed)

batch=ROOT/'SOURCE_BATCH';batch.mkdir(exist_ok=True)
for n in [Z.name,Z.name+'.sha256','INTAKE_RECEIPT.json']:shutil.copyfile(D/n,batch/n)
for n in names:
    q=batch/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(z.read(n))
catalog=json.loads((ROOT/'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
old_count=len(catalog['source_files']);assert old_count==352
selected=[Z.name,Z.name+'.sha256','INTAKE_RECEIPT.json','README.md','LOOM_P_B1_NARROW_INDEPENDENT_REVIEW.md','CLOSURE_TABLE.md',
 'REVIEWED_IDENTITIES.json','FILE_MANIFEST.json','FAULT_AND_SUITE_AUDIT.json','FAULT_AND_SUITE_AUDIT.md','REPRODUCTION_COMMANDS.md',
 'EXACT_DIFF_68db2c58_to_352f73ff.patch','information_flow/INFORMATION_FLOW_REVIEW.md','lifecycle/LIFECYCLE_CUSTODY_REVIEW.md',
 'lifecycle/new-results.json','regression/worktree-suite.json','regression/worktree-suite.log','regression/worktree-suite.xml',
 'regression/portable-suite.json','regression/portable-suite.log','regression/portable-suite.xml',
 'provenance/STATIC_COMPATIBILITY.json','provenance/FINAL_PRESERVATION.json','provenance/SEALED_PAYLOAD_EXCLUSION_GUARD.json',
 'references/NARROW_B1_REVIEW_REQUEST.txt',builder_name]
entries=[]
for i,n in enumerate(selected,old_count+1):
    data=(batch/n).read_bytes()
    entries.append({'source_id':f'SRC-{i:03d}','path':B+'/'+n,'original_filename':PurePosixPath(n).name,'bytes':len(data),'sha256':sha(data),
      'role':'final-narrow-B1-operator-apparatus-review','prepared':'2026-09-26','registered':'2026-09-26',
      'stated_author':'Supplied independent narrow B1 review; exact model/backend not stated',
      'acquired_from':str(Z)+'::'+n if n in names else str(D/n),'archive_member':n if n in names else None,
      'authority':'Current Jason instruction to ingest final narrow review; no packet regeneration or execution',
      'reviewed_apparatus_checkpoint':CP,'previous_apparatus_checkpoint':OLD,'p_baseline_checkpoint':P,
      'held_B1_review_identity':AUTH,'review_disposition':STATUS,'prepared_cases_executed':False,
      'review_note':R,'record':S+'/INTAKE_RECORD.md',
      'notes':'Apparatus blockers closed within reviewed scope; historical held packet remains unchanged/non-launchable. No new launch authority. No sealed B1 state copied or opened by intake.'})
catalog['source_files']+=entries
catalog['intake_events'].append({'session_id':ID,'source_ids':[e['source_id'] for e in entries],'review_note':R,'record':S+'/INTAKE_RECORD.md',
 'reviewed_apparatus_checkpoint':CP,'previous_apparatus_checkpoint':OLD,'held_B1_review_identity':AUTH,
 'scope':STATUS+'; apparatus blocker closed; all six prepared cases unexecuted; no launch authority'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)
def src(n,label):return f'[{label}](../../{B}/{n})'
status='''P engineering: **previously VERIFIED; unchanged**  
B1 operator apparatus: **FIT FOR B1 LAUNCH-PACKET REGENERATION**  
B1 apparatus blocker: **CLOSED within the narrow independent review scope**  
Coupling commissioning: **IN PROGRESS**  
Physical ceiling A0–A5: **EXERCISED within its scoped bounded witness set**  
B1 preparation: **DESIGN PRESERVED; OLD PACKET HELD / NON-LAUNCHABLE; REGENERATION NEXT**  
B1 execution: **NOT STARTED; NO LAUNCH AUTHORITY**  
Human competence / perceptual outcomes: **UNTESTED**  
Scientific/developmental efficacy: **UNTESTED**'''
claims='''| Reviewed property | Registered finding |
|---|---|
| Chemistry-hidden condition | VERIFIED as display-side only; full physical/raw chemistry remains in privileged records. |
| Operator information isolation | No chemistry leakage through reviewed HTTP, DOM, export or error surfaces. |
| Lifecycle | PREPARED / PAUSED / RUNNING / ENDED VERIFIED. PAUSED produces zero simulated evolution. |
| Single-command hold | One accepted ordinary operator command produces exactly one 0.1 s / 10-native-step hold, with no automatic continuation. |
| Command exclusion | Duplicate, concurrent and stale commands rejected. |
| End state | ENDED is irreversible. |
| Authority | Binds exact display/deprivation identity. |
| Prior protections | Clock/index scheduling and apparatus protections remain intact. |'''
cases='''| Prepared case | Execution status |
|---|---|
| PC-LR | UNEXECUTED |
| PC-MOTION | UNEXECUTED |
| PC-CONTACT | UNEXECUTED |
| PC-HOLD | UNEXECUTED |
| B1-FULL-RAW | UNEXECUTED |
| B1-CHEMISTRY-HIDDEN | UNEXECUTED |'''
record=f'''# Final narrow B1 operator-apparatus review — registration

**Registered:** 2026-09-26. **Independent review disposition: {STATUS}.**

| Identity | Exact value |
|---|---|
| Corrected B1 operator apparatus | `{CP}` |
| Previous apparatus | `{OLD}` |
| P baseline, unchanged | `{P}` |
| Historical held B1 review/custody identity | `{AUTH}` |

{status}

## Final review findings

{claims}

Source: {src('LOOM_P_B1_NARROW_INDEPENDENT_REVIEW.md','complete independent review')} and {src('CLOSURE_TABLE.md','closure table')}. The two earlier commissioning-apparatus defects—chemistry deprivation and live operator lifecycle—are closed at the corrected checkpoint within this review's scope. Their original findings at `{OLD}` remain preserved history; neither was a perceptual, chemistry, sensor, P or Base World failure.

The {src('information_flow/INFORMATION_FLOW_REVIEW.md','information-flow review')} supports display-only omission from the operator projection while full physical/raw chemistry stays in privileged evidence. The {src('lifecycle/LIFECYCLE_CUSTODY_REVIEW.md','lifecycle/custody review')} supports zero simulated evolution while paused, one-command execution, command exclusion, irreversible end and authority binding. The single ordinary hold is 10 native steps of 0.01 s; the recorded floating physical time is `0.09999999999999999`. Existing genuine terminal or case/resource cutoff rules may interrupt a hold. Administrative wall expiry can end a paused case by bookkeeping without simulated bodily evolution. These qualifications retain the source's timing semantics.

## Verification evidence and scope

- **204 worktree tests passed.**
- **204 portable tests passed.**
- **All 12 A–L RED→GREEN pairs verified**, with 24 corresponding logs.

The {src('FAULT_AND_SUITE_AUDIT.md','independent audit')} and {src('FAULT_AND_SUITE_AUDIT.json','saved detailed audit')} distinguish actual expected failures and passing controls. Pair A raises the reinstated restriction's ValueError; pair I checks overlapping entry with a synchronization stub. These are not twelve equivalent ecological interventions. The saved suite composition is 59 P tests plus 117 previous apparatus tests plus 28 B1 operator tests. Earlier clock/index scheduling, authority/dispatch binding, stage bounds, pending-command persistence, observer RNG isolation and fixed-structure protections remain covered.

This intake checked archived logs, exit receipts, JUnit counts/IDs, hashes and pair outcomes. **It did not rerun tests, reconstruct a trajectory, start the UI or execute any controller/simulation.** The review's manufactured engineering fixtures are distinct from the prepared human positive controls and B1 trials. Apparatus verification does not establish human competence or a perceptual outcome.

## Prepared cases and launch boundary

{cases}

Four sensor-only positive controls and the paired 30-second FULL-RAW / CHEMISTRY-HIDDEN design remain preserved. The review reports that the B1 pair shares the same complete initial physical state and world laws; only case label and declared display differ. This intake uses the safe compatibility finding, not sealed evaluator manifests or hidden state. No hidden B1 state was disclosed by the review or this intake.

**No launch authority exists yet. B1 launch-packet regeneration is next; no regeneration occurs here.** The [historical held record](../../{HR}), its exact custody identity `{AUTH}`, held packet and separately sealed evaluator material remain unchanged and non-launchable. Closing the apparatus blocker does not convert the old custody identity into execution authority.

## Broader commissioning status and limitations

V1/V2/V3/A0 COMPLETE; A1–A5 OBSERVED within their bounded scopes. The [finite A0–A5 physical-ceiling evidence](../../{A5R}) remains historical evidence from its original apparatus checkpoints, not relabelled as runs under `{CP}`. B1's six prepared cases remain UNEXECUTED; B2–B4 and C1/C2 remain NOT EXECUTED. Human competence, perceptual outcomes and scientific/developmental efficacy remain UNTESTED.

Retain the review's limits: no claim of human usability or UI appearance validation, perceptual sufficiency, successful B1 outcomes, long interactive duration or history-growth performance. The reviewed operator/evaluator separation is not an operating-system access guarantee. No canon, P, Base World configuration, numerical settings, perceptual-commissioning design, sequence, scientific interpretation or actual repository change follows. No experiment number or Git operation is created.

## Custody and completion

The final independent review was located in the local review export `exports/2026-09-26-b1-review-352f73ff`; the Workbench inbox correction archive is the earlier builder package and retains its original independent-review-pending wording. Both source layers are preserved without rewriting either status. The final review supersedes that pending wording for current navigation only.

Preserved the complete independent review ZIP, its checksum/receipt, and all 254 members in a unique append-only source batch. Verified 253 payload hashes, sizes and CRCs, plus exact expanded copies. The nested public builder ZIP matches the inbox ZIP and has 2,676 verified payloads. Sealed evaluator material was not opened, extracted, decoded or linked; its existing outer bytes were checked for preservation only. No necessary source gap was found.

The old catalog rows and earlier sources/candidates/reviews/decisions/sessions remain unchanged. Prior shared notes have a local recovery copy. {src('README.md','Source entry')} · [Intake completion](INTAKE_RECORD.md) · [Custody validation](VALIDATION.json).
'''
write(ROOT/'NEW'/R,record)
nav=f'''## Current commissioning boundary — B1 apparatus closure, 2026-09-26

{status}

Corrected B1 operator apparatus: `{CP}`; previous apparatus: `{OLD}`. **{STATUS}.** The held review/custody identity `{AUTH}` and packet remain unchanged and non-launchable. No launch authority exists yet. No packet is regenerated by this intake.

{claims}

Independent verification: **204 worktree tests passed; 204 portable tests passed; all 12 A–L RED→GREEN pairs verified.** These are engineering component results, not human positive-control or perceptual results.

**All prepared cases remain UNEXECUTED:** PC-LR, PC-MOTION, PC-CONTACT, PC-HOLD, B1-FULL-RAW and B1-CHEMISTRY-HIDDEN. B2–B4 and C1/C2 remain NOT EXECUTED. No hidden B1 state was disclosed; sealed evaluator material remains unchanged and unlinked. Preserve the design; do not infer launch authority, human competence or perceptual success from apparatus closure.

[Final B1 apparatus review registration]({R}) · [Complete independent review]({B}/LOOM_P_B1_NARROW_INDEPENDENT_REVIEW.md) · [Closure table]({B}/CLOSURE_TABLE.md) · [Historical held preparation]({HR}). Earlier sections below retain their dated meaning; the old apparatus defects are closed at the corrected checkpoint, without rewriting the held source packet.

'''
for n in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    text=(ROOT/'BEFORE'/n).read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
    old='## Current commissioning boundary — B1 held before execution, 2026-09-26';assert old in rest
    rest=rest.replace(old,'## Preserved B1 preparation hold — before final apparatus closure, 2026-09-26',1)
    if n=='00_RESEARCH_MAP.md':
        old='coupling commissioning in progress; finite A0–A5 physical ceiling exercised; B1 prepared/held, two apparatus defects | A1–A5 observed external physical witnesses; B1 not executed; P learning/developmental efficacy untested'
        assert old in rest
        rest=rest.replace(old,'coupling commissioning in progress; finite A0–A5 physical ceiling exercised; B1 apparatus closed, launch-packet regeneration next | A1–A5 observed external physical witnesses; B1/controls unexecuted, no launch authority; P learning/developmental efficacy untested',1)
    write(ROOT/'AFTER'/n,first+'\n\n'+nav+rest.lstrip('\n'))
text=(ROOT/'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
old='## Current commissioning boundary — B1 held before execution, 2026-09-26';assert old in rest
rest=rest.replace(old,'## Preserved B1 preparation hold — before final apparatus closure, 2026-09-26',1)
continuation=f'''## Current commissioning boundary — B1 apparatus closure, 2026-09-26

The [final independent B1 operator-apparatus review]({R}) of `{CP}`, following `{OLD}`, is **{STATUS}**. **B1 apparatus blocker CLOSED within reviewed scope.** Chemistry-hidden is display-side only; full raw/physical chemistry remains in privileged records, with no leakage through reviewed operator HTTP/DOM/export/error surfaces. PREPARED/PAUSED/RUNNING/ENDED lifecycle is verified: paused has zero simulated evolution; one ordinary accepted command yields one 0.1 s / 10-native-step hold; duplicate/concurrent/stale commands reject; ENDED is irreversible. Existing terminal/resource cutoff rules remain. Authority binds display/deprivation identity; prior clock/index scheduling and protections remain intact. Independent review: 204 worktree + 204 portable tests passed; all 12 A–L pairs verified.

**B1 launch-packet regeneration is next; no launch authority exists yet.** PC-LR, PC-MOTION, PC-CONTACT, PC-HOLD, B1-FULL-RAW and B1-CHEMISTRY-HIDDEN remain UNEXECUTED. The exact held review/custody identity `{AUTH}` and historical HOLD packet remain unchanged and non-launchable. Preserve sealed evaluator material; do not open or surface sealed manifests, hidden geometry or privileged fixture information in live navigation. No hidden B1 state was disclosed by this review/intake.

A0–A5 physical ceiling remains exercised within bounded scope and retains original apparatus provenance. B2–B4/C1–C2 remain NOT EXECUTED. Human competence, perceptual outcomes and scientific/developmental efficacy remain UNTESTED. P, canon, Base World configuration, settings and perceptual-commissioning design are unchanged. This intake registers closure only; no packet regeneration, grant, execution, experiment number or Git operation. Earlier hold/blocker wording below is dated history, not the current corrected-apparatus status. Stop after status/navigation confirmation.

'''
write(ROOT/'AFTER/AGENTS.md',first+'\n\n'+continuation+rest.lstrip('\n'))
text=(ROOT/'BEFORE/40_DECISIONS/DECISION_INDEX.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
idx=f'''## Final B1 apparatus review — no launch authority, 2026-09-26

[Final review registration](../{R}): **{STATUS}** at `{CP}`, following `{OLD}`. Chemistry-deprivation and lifecycle blockers CLOSED within reviewed scope; all six prepared cases remain UNEXECUTED. The historical held identity `{AUTH}` and packet stay unchanged/non-launchable. Launch-packet regeneration is next, not performed or authorized by this intake; no launch grant exists. Human competence/perceptual outcomes and efficacy UNTESTED. This registers engineering review closure, not a new research decision or execution approval. Earlier decisions and hold records remain unchanged.

'''
write(ROOT/'AFTER/40_DECISIONS/DECISION_INDEX.md',first+'\n\n'+idx+rest.lstrip('\n'))
reg=(ROOT/'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
reg+='\n## Final narrow B1 operator-apparatus review — 2026-09-26\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:reg+=f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
reg+=f'\n[Registration]({R}). Corrected apparatus `{CP}`; **{STATUS}**. Historical held packet remains non-launchable; six prepared cases unexecuted; no new authority. Source review excludes sealed B1 state.\n'
write(ROOT/'AFTER/SOURCE_REGISTER.md',reg)
verification={'incoming_zip':str(Z),'zip_bytes':Z.stat().st_size,'zip_sha256':fsha(Z),'manifest_payloads_verified':253,'archive_members':254,
 'CRC_verified':True,'expanded_copies_match':254,'nested_public_builder_payloads_verified':2676,'nested_builder_zip_matches_inbox':True,
 'reviewed_apparatus_checkpoint':CP,'previous_apparatus_checkpoint':OLD,'held_review_identity':AUTH,
 'saved_suite_tests_each':204,'saved_suites_junit_failures_errors_skips':0,'saved_suite_test_ids_match':True,'saved_fault_control_pairs_checked':12,
 'held_evaluator_outer_bytes_unchanged':True,'evaluator_archive_opened':False,'sealed_manifests_opened':False,'hidden_state_disclosed_by_intake':False,
 'prepared_controls_executed':False,'B1_executed':False,'new_launch_authority':False,'launch_packet_regenerated':False,
 'tests_or_validators_run_by_intake':False,'simulation_or_controller_execution_by_intake':False,'git_operations':False,'necessary_source_gaps':[]}
inventory={q.relative_to(batch).as_posix():fsha(q) for q in batch.rglob('*') if q.is_file()}
dump(ROOT/'NEW'/S/'SOURCE_IDENTITIES.json',{'session_id':ID,'registered_sources':entries,'verification':verification,'complete_batch_sha256':inventory})
intake=f'''# Final narrow B1 review intake — completion

Registered **{STATUS}** for apparatus `{CP}`. [Full registration](FINAL_B1_OPERATOR_APPARATUS_REVIEW_RECORD.md). Both commissioning-apparatus blockers CLOSED; historical held identity `{AUTH}` remains unchanged and non-launchable. All six prepared cases unexecuted; no launch authority. Regeneration is next. Human competence/perceptual outcomes and scientific/developmental efficacy remain UNTESTED.

Read current instructions/map/status, complete final independent review, closure table, saved audit/identities and intake receipt. Preserved the complete final review archive and 254 members, checksum/receipt and nested public builder archive; checked 253 outer and 2,676 nested payload hashes/CRCs, exact expanded matches, saved 204/204 suites and all 12 A–L pair receipts/logs/JUnit. No archived utility, test, validator, UI or simulation was executed. Source identities: SRC-{old_count+1:03d}–SRC-{old_count+len(entries):03d}.

Updated AGENTS.md, 00_RESEARCH_MAP.md, 01_WORKSPACE_STATUS.md, SOURCE_CATALOG.json, SOURCE_REGISTER.md and 40_DECISIONS/DECISION_INDEX.md. Added this unique session and append-only source batch. Earlier sources/candidates/reviews/decisions/sessions and catalog rows preserved; PRIOR_SHARED_NOTES.zip/receipt contain the six pre-update shared notes. [Validation](VALIDATION.json) records actual custody/link/preservation checks.

Held operator packet and sealed evaluator archive remain byte-identical. No sealed evaluator archive/member manifest/state was opened or decoded; no hidden initial geometry or privileged fixture information was added to navigation. Review-held compatibility claims remain attributed to the independent source. No canon/P/Base World/settings/design/sequence, actual repository, experiment number or Git change. No necessary source gap. Stop after concise status/navigation confirmation.
'''
write(ROOT/'NEW'/S/'INTAKE_RECORD.md',intake)
for group in ['NEW','AFTER']:
    for q in (ROOT/group).rglob('*.md'):
        t=q.read_text(encoding='utf-8');assert 'B1_PRIVILEGED_EVALUATOR_HOLD.zip' not in t and 'SEALED_EVALUATOR_DO_NOT_OPEN' not in t
dump(ROOT/'PLAN.json',{'session':S,'batch':B,'review':R,'live_before':before,'protected_before':protected,'source_entries':entries,
 'verification':verification,'zip_source':str(Z),'old_catalog_count':old_count,'status':STATUS,'incoming_before':incoming,'batch_inventory':inventory})
shutil.copyfile(ROOT.parent/'2026-09-26-b1-held-intake-6e3ac812/publish_intake.py',ROOT/'publish_intake.py')
print(json.dumps({'prepared':ID,'registered_sources':len(entries),'protected_files':len(protected),'batch_files':len(inventory),'private_state_opened':False}),flush=True)
