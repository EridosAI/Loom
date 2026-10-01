"""Custody and documentation intake of completed A5 evidence; no research imports."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib,json,zipfile,shutil

ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
D=WB/'INBOX/2026-09-26-A5-commissioning-result-68db2c58'
Z=D/'A5_COMMISSIONING_RESULT.zip'
ID='2026-09-26-a5-evidence-intake-82b4d9e1'
S='50_SESSIONS/'+ID
B='90_SOURCES/p_a5_commissioning_2026-09-26_82b4d9e1'
R=S+'/A5_COMMISSIONING_EVIDENCE_RECORD.md'
AUTH='bdff35693db38800528d91e6d2d4d2085c640268e50713731df5ec27f8b76d1d'
OLD_AUTH='88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
CP='68db2c581f07200966d699a4f55a65f9b96df1e9'
HELD='90_SOURCES/p_a5_held_proposal_2026-09-26_62c8f4b1'
PREV='50_SESSIONS/2026-09-26-final-clock-review-intake-3af846d2/FINAL_CLOCK_CORRECTION_REVIEW_RECORD.md'
A4R='50_SESSIONS/2026-09-26-a4-evidence-intake-0e69b3c8/A4_COMMISSIONING_EVIDENCE_RECORD.md'
CLAIM='One continuous externally controlled physical witness demonstrated two productive revisits to previously depleted finite energy sources after approximately 217–219 seconds away. Each source measurably renewed while unattended, and later contact transferred energy from the renewed state.'
sha=lambda b:hashlib.sha256(b).hexdigest()
def stream_hash(f):
    h=hashlib.sha256()
    for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)
    return h.hexdigest()
def fsha(p):
    with Path(p).open('rb') as f:return stream_hash(f)
def write(p,t):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,o):write(p,json.dumps(o,indent=2,ensure_ascii=False)+'\n')
def safe(z):
    names=z.namelist();assert len(names)==len(set(names))==len({n.casefold() for n in names})
    for n in names:
        q=PurePosixPath(n);assert not q.is_absolute() and '..' not in q.parts and ':' not in n and '\\' not in n and not n.endswith('/')
    return names

receipt=json.loads((D/'DELIVERY_RECEIPT.json').read_text(encoding='utf-8-sig'))
ziphash=fsha(Z)
assert ziphash==receipt['zip_sha256']=='2e4d536bfedf446e30064b0d7bd735e4aa767cef7b928bb89a611367ab129207'
assert Z.stat().st_size==receipt['zip_bytes']==599493115
assert receipt['authority_sha256']==AUTH and receipt['apparatus_checkpoint']==CP
assert ziphash in (D/(Z.name+'.sha256')).read_text()
z=zipfile.ZipFile(Z);names=safe(z);mf=json.loads(z.read('FILE_MANIFEST.json'))
assert len(names)==127 and len(mf['files'])==receipt['payload_count']==126
assert mf['authority_sha256']==AUTH and mf['apparatus_checkpoint']==CP
assert set(mf['files'])==set(names)-{'FILE_MANIFEST.json'}
batch=ROOT/'SOURCE_BATCH';batch.mkdir(exist_ok=True)
incoming={}
for n in [Z.name,Z.name+'.sha256','DELIVERY_RECEIPT.json']:
    incoming[str(D/n)]=fsha(D/n);shutil.copyfile(D/n,batch/n)
expanded={}
for n in names:
    q=batch/n;q.parent.mkdir(parents=True,exist_ok=True)
    with z.open(n) as src,q.open('wb') as dst:shutil.copyfileobj(src,dst,4*1024*1024)
    h=fsha(q)
    if n in mf['files']:
        m=mf['files'][n];assert h==m['sha256'] and q.stat().st_size==m['bytes'],n
    assert h==fsha(D/'A5_COMMISSIONING_RESULT'/n),n
    expanded[n]=h
print('Verified all 126 result payloads, CRC reads and 127 expanded copies.',flush=True)
summary=json.loads(z.read('A5_FINAL_RESULT_SUMMARY.json'))
assert summary['authority_sha256']==AUTH and summary['native_steps']==63000 and summary['planned_simulated_ceiling']==630
expected={'initial_EI':[0.7,1.0],'final_EI':[0.3667496379859223,0.9747806260916136],
    'expenditure':1.0578235904590032,'all_source_intake':0.7245732284449362,'damage':0.02521937390838666,'repair':0.0,
    'stop_label':'administrative_cutoff','complete_receipt':True,'terminal_dimension':None,'failure':None,
    'complete_bounded_productive_recurrence_witness':True,'observed_macro_returns':2,'planned_revisits_obtained':2}
for k,v in expected.items():assert summary[k]==v,k
assert summary['origin_attribution_totals']['renewed_interval']==[0.32457322844493625,0.41171713166753504]
assert summary['final_stocks'][2:]==[0.2]*6
assert not summary['initial_support_gap_witness_flag']
canonical=z.read('evidence/APPROVED_OBJECT.canonical.json');assert sha(canonical)==AUTH
obj=json.loads(canonical);launched=json.loads(z.read('evidence/LAUNCHED_MANIFEST.json'))
assert obj=={k:v for k,v in launched.items() if k!='execution_authority'}
grant=launched['execution_authority'];assert grant['approved_execution_sha256']==AUTH
request=json.loads(z.read('evidence/APPROVAL_REQUEST.json'))
assert request['approved_execution_sha256']==AUTH and request['approved_execution']==obj
assert sha(z.read('evidence/APPROVAL_REQUEST.json'))==grant['request_sha256']
assert z.read('evidence/AUTHORIZATION_SOURCE.txt').decode().strip()==request['notice']
assert launched['baseline']==P and launched['case_id']=='A5' and launched['mode']=='external_controller'
protocol=launched['execution']['procedure']['protocol']
assert protocol['case_count']==1 and protocol['source_visit_order']==[0,1,0,1]
assert protocol['reviewed_checkpoints']['apparatus_git_sha']==CP
run=json.loads(z.read('evidence/EXECUTION_RESULT.json'))
assert run['approved_execution_sha256']==AUTH and run['apparatus_checkpoint']==CP
assert run['run_constructors_attempted']==1 and run['native_index']==63000 and run['no_retry_no_resume_no_patch']
assert run['terminal_dimension'] is None and run['failure'] is None
tr=json.loads(z.read('evidence/trajectory-001/manifest.json'))
assert tr['contract']==launched and tr['complete'] and tr['status']=='administrative_cutoff'
assert tr['parent'] is None and tr['error'] is None and tr['terminal_dimension'] is None
assert tr['final_state']==run['final_engine_sha256'] and tr['final_time']==summary['observed_simulated_time']==run['time']
assert tr['records']['native']==63000 and tr['records']['controller']==6300
for n,m in tr['files'].items():
    q=batch/'evidence/trajectory-001'/n;assert q.stat().st_size==m['bytes'] and fsha(q)==m['sha256'],n
analysis=json.loads(z.read('ANALYSIS_RESULT.json'));assert not analysis['errors'] and analysis['original_raw_files_unchanged']
assert analysis['new_simulation_steps']==analysis['controller_command_computations']==analysis['physical_replays']==0
integrity=json.loads(z.read('evidence/read-only-review/RECORD_INTEGRITY.json'));assert integrity['valid'] and integrity['complete']
delivery=json.loads(z.read('evidence/read-only-review/BOUNDARY_AND_DELIVERY.json'));assert delivery['valid'] and delivery['native_rows']==63000
assert delivery['controller']['last_hold_pending_steps']==0 and delivery['controller']['controller_command_function_calls']==0
audit=json.loads(z.read('ACTUAL_CONTACT_BOUNDARY_AUDIT.json'))
assert audit['complete_saved_data_validation'] and audit['complete_bounded_productive_recurrence_witness']
for ret in summary['actual_contact_returns']:
    assert all(ret['predicates'].values()) and ret['away_source_debit']==0.0
assert summary['actual_contact_returns'][0]['actual_departure_time']==90.00000000000914
assert summary['actual_contact_returns'][1]['actual_departure_time']==273.07356311601956
obs=json.loads(z.read('evidence/read-only-review/A5_OBSERVATIONS.json'))
initial=json.loads(z.read('A5_RESULT_SUMMARY.json'))
assert not initial['complete_bounded_productive_recurrence_witness'] and not obs['summary']['complete_bounded_productive_recurrence_witness']
for n in ['A5_FINAL_RESULT_SUMMARY.json','A5_PLAIN_LANGUAGE_RESULT.md','A5_RESULT_SUMMARY.json','ACTUAL_CONTACT_BOUNDARY_AUDIT.json','ANALYSIS_RESULT.json']:
    assert z.read(n)==z.read('evidence/read-only-review/'+n),n
assert z.read('evidence/ORIGINAL_FILES_BEFORE.json')==z.read('evidence/ORIGINAL_FILES_AFTER.json')
assert z.read('evidence/read-only-review/RAW_EVIDENCE_BEFORE_ANALYSIS.json')==z.read('evidence/read-only-review/RAW_EVIDENCE_AFTER_ANALYSIS.json')
pres=json.loads(z.read('FINAL_PRESERVATION.json'));assert pres['all_originals_unchanged'] and pres['raw_unchanged_after_reporting']
launch_path=batch/'approved-launch/A5_LAUNCH_PACKET.zip'
inbox_launch=WB/'INBOX/2026-09-26-A5-launch-packet-68db2c58/A5_LAUNCH_PACKET.zip'
assert fsha(launch_path)==fsha(inbox_launch);incoming[str(inbox_launch)]=fsha(inbox_launch)
lz=zipfile.ZipFile(launch_path);ln=safe(lz);lm=json.loads(lz.read('FILE_MANIFEST.json'))
assert lm['authority_sha256']==AUTH and set(lm['files'])==set(ln)-{'FILE_MANIFEST.json'}
for n,m in lm['files'].items():
    with lz.open(n) as f:h=stream_hash(f)
    assert h==m['sha256'] and lz.getinfo(n).file_size==m['bytes'],n
assert lz.read('AUTHORITY_OBJECT.canonical.json')==canonical
assert json.loads(lz.read('A5_MANIFEST.json'))['execution_authority'] is None
for n,h in protocol['bound_files'].items():assert sha(lz.read(n))==h,n
assert 'final actual' in lz.read('OBSERVATION_AND_INTERPRETATION.md').decode().lower()
assert fsha(WB/HELD/'AUTHORITY_OBJECT.canonical.json')==OLD_AUTH
print('Verified executed authority, trajectory receipt, saved summaries, preserved flags and nested approved launch package.',flush=True)

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
old_count=len(catalog['source_files']);assert old_count==299
selected=[Z.name,Z.name+'.sha256','DELIVERY_RECEIPT.json','README.md','A5_PLAIN_LANGUAGE_RESULT.md','A5_FINAL_RESULT_SUMMARY.json',
    'ACTUAL_CONTACT_BOUNDARY_AUDIT.json','A5_RESULT_SUMMARY.json','ANALYSIS_RESULT.json','REPORT_DISPOSITION.json','RESOURCE_RESULT.json',
    'FINAL_PRESERVATION.json','FILE_MANIFEST.json','approved-launch/A5_LAUNCH_PACKET.zip','evidence/AUTHORIZATION_SOURCE.txt',
    'evidence/APPROVAL_REQUEST.json','evidence/APPROVED_OBJECT.canonical.json','evidence/LAUNCHED_MANIFEST.json','evidence/EXECUTION_RESULT.json',
    'evidence/RUN_CONSTRUCTION_ATTEMPT.json','evidence/trajectory-001/manifest.json','evidence/read-only-review/A5_OBSERVATIONS.json',
    'evidence/read-only-review/RECORD_INTEGRITY.json','evidence/read-only-review/BOUNDARY_AND_DELIVERY.json','evidence/read-only-review/ACCOUNTING.json',
    'evidence/read-only-review/ALL_FIXED_WINDOWS.json','evidence/read-only-review/CLOCK_BOUNDARY_OBSERVATIONS.json',
    'evidence/read-only-review/RAW_EVIDENCE_BEFORE_ANALYSIS.json','evidence/read-only-review/RAW_EVIDENCE_AFTER_ANALYSIS.json',
    'evidence/ORIGINAL_FILES_BEFORE.json','evidence/ORIGINAL_FILES_AFTER.json']
entries=[]
for i,n in enumerate(selected,old_count+1):
    q=batch/n
    entries.append({'source_id':f'SRC-{i:03d}','path':B+'/'+n,'original_filename':PurePosixPath(n).name,'bytes':q.stat().st_size,'sha256':fsha(q),
        'role':'observed-A5-commissioning-evidence','prepared':'2026-09-26','registered':'2026-09-26',
        'stated_author':'Supplied A5 execution and saved-data reporting package; exact model/backend not stated',
        'acquired_from':str(Z)+'::'+n if n in names else str(D/n),'archive_member':n if n in names else None,
        'authority':'Jason requests registration of the single completed authorized A5 result; no new execution',
        'executed_authority_sha256':AUTH,'p_baseline_checkpoint':P,'apparatus_checkpoint':CP,'review_note':R,'record':S+'/INTAKE_RECORD.md',
        'status':'OBSERVED COMMISSIONING EVIDENCE','notes':'One 630 s / 63000 native-step external physical witness. Two productive renewed revisits observed. Initial support-gap false flag and final actual-contact audit preserved separately. No survival-necessity or P-efficacy claim.'})
catalog['source_files']+=entries
catalog['intake_events'].append({'session_id':ID,'source_ids':[e['source_id'] for e in entries],'review_note':R,'record':S+'/INTAKE_RECORD.md',
    'executed_authority_sha256':AUTH,'apparatus_checkpoint':CP,
    'scope':'A5 OBSERVED; finite A0–A5 physical ceiling exercised within bounded witness set; next perceptual ceiling; B1–B4/C1–C2 unexecuted; scientific/developmental efficacy untested'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)
def src(n,label):return f'[{label}](../../{B}/{n})'
status='''P engineering: **VERIFIED; unchanged**  
Commissioning apparatus: **VERIFIED within its reviewed scope; clock correction closed**  
Coupling commissioning: **IN PROGRESS**  
Finite A0–A5 physical ceiling: **EXERCISED within its scoped bounded witness set**  
Next commissioning layer: **PERCEPTUAL CEILING**  
Scientific/developmental efficacy: **UNTESTED**

| Commissioning item | Status |
|---|---|
| V1 / V2 / V3 | COMPLETE |
| A0 | COMPLETE |
| A1 | OBSERVED |
| A2 | OBSERVED |
| A3 | OBSERVED |
| A4 | OBSERVED |
| A5 | OBSERVED COMMISSIONING EVIDENCE |
| B1–B4 | NOT EXECUTED |
| C1/C2 | NOT EXECUTED |'''
record=f'''# A5 — observed coupling-commissioning evidence

**Registered:** 2026-09-26. **A5: OBSERVED COMMISSIONING EVIDENCE.**

One authorized external-control physical witness executed under authority `{AUTH}`, with P `{P}` and commissioning apparatus `{CP}`. P was inactive. This record registers the existing result and authorizes no new run.

{status}

## Primary evidence and exact execution

{src('A5_PLAIN_LANGUAGE_RESULT.md','A5_PLAIN_LANGUAGE_RESULT.md')} · {src('A5_FINAL_RESULT_SUMMARY.json','A5_FINAL_RESULT_SUMMARY.json')} · {src(Z.name,'complete verified result package')} · {src('FILE_MANIFEST.json','payload manifest')}.

The case completed **630 nominal simulated seconds / 63,000 native steps**, with recorded physical time **629.9999999995721 s** and complete **administrative_cutoff**. Exactly one case was authorized and one Run construction attempted. No retry, continuation, tuning, patch, substitution, terminal crossing or execution failure occurred. See the {src('evidence/EXECUTION_RESULT.json','execution result')} and {src('evidence/trajectory-001/manifest.json','original trajectory receipt')}.

The {src('evidence/AUTHORIZATION_SOURCE.txt','exact execution authorization')}, {src('evidence/APPROVAL_REQUEST.json','approval request')}, {src('evidence/APPROVED_OBJECT.canonical.json','approved canonical object')}, {src('evidence/LAUNCHED_MANIFEST.json','granted launch manifest')} and {src('approved-launch/A5_LAUNCH_PACKET.zip','complete authorized launch packet')} preserve the actual authority chain. The canonical bytes hash to `{AUTH}`. The earlier held proposal `{OLD_AUTH}` remains unchanged as [historical preparation](../../{HELD}/AUTHORITY_OBJECT.canonical.json); it was not the executed authority.

## Body and visit observations

| Body/accounting item | Recorded value |
|---|---|
| Initial E / I | 0.7 / 1.0 |
| Final E / I | 0.3667496379859223 / 0.9747806260916136 |
| Expenditure | 1.0578235904590032 |
| Total intake | 0.7245732284449362 |
| Damage | 0.02521937390838666 |
| Repair | 0 |

| Visit | Source | First contact (s) | Transfer |
|---|---|---:|---:|
| 1 | Source 0 | 6.31019049 | 0.188866528 |
| 2 | Source 1 | 132.376428 | 0.230909963 |
| 3 | Source 0 revisit | 306.928349 | 0.155117741 |
| 4 | Source 1 revisit | 492.092241 | 0.149667947 |

The contact/transfer table follows the supplied rounded reporting precision; the full saved values remain in the source records. Fixed stage windows were retained. Source 1 actually departed after its 270 s target change; no stage was extended to obtain the revisit.

| Macro-return measure | Source 0 | Source 1 |
|---|---:|---:|
| Actual departure (s) | 90.00000000000914 | 273.07356311601956 |
| Revisit (s) | 306.9283486087647 | 492.092241357054 |
| Away time (s) | 216.92834860875553 | 219.01867824103442 |
| Stock at departure | 0.035148459595822044 | 0.019167314788177535 |
| Stock before revisit | 0.10415575344039082 | 0.0954123456880177 |
| Measured away renewal | 0.06900729384456919 | 0.07624503089983946 |
| Away debit | 0 | 0 |
| Productive revisit | Observed | Observed |

## Renewal attribution and bounded claim

**Renewal availability and renewed productive uptake WERE demonstrated.** The renewed-origin intake lower bound is **0.32457322844493625** and upper bound **0.41171713166753504**. The lower bound equals approximately **30.683% of recorded expenditure**, or **216.382 basal-cost-equivalent seconds**. These retain the source's origin-attribution bounds and arithmetic meaning; they are not extra measured survival time.

**Necessity of renewal for survival was NOT demonstrated.** Do not convert recorded expenditure/debit arithmetic into a no-renewal counterfactual. The source's initial-origin-only balance and zero lower bound needed to cover recorded expenditure remain arithmetic over this recorded case, not a simulated alternative trajectory or a survival conclusion.

Strongest supported A5 statement, as requested by Jason:

> {CLAIM}

Explicitly withhold renewal being necessary for survival; indefinite sustainability; global ecological sufficiency; optimal source schedule; autonomous source switching; P perception, learning or regulation; and lifetime competence.

## Contact-boundary reconciliation and other observations

Preserve the complete {src('ACTUAL_CONTACT_BOUNDARY_AUDIT.json','actual contact-boundary audit')}. The initial support-gap analysis used source 1's last positive-duration support endpoint at **273.06999999989665 s** and conservatively flagged the interval because a subsequent zero-duration contact/release occurred. The predeclared rule uses the **final actual contact**, including that touch, at **273.07356311601956 s**. Its impulse and **1.3310128316840975e-09** damage remain in the evidence. The final away interval then contains no interior contact, no boundary-straddling event and zero debit before the revisit at **492.092241357054 s**.

The original false witness flag in {src('A5_RESULT_SUMMARY.json','A5_RESULT_SUMMARY.json')} and {src('evidence/read-only-review/A5_OBSERVATIONS.json','A5_OBSERVATIONS.json')} remains byte-identical. The supplemental boundary audit and final summary record the reconciled interpretation of the same unchanged events. No event was deleted, moved or interpolated, and no new criterion, patch, retry or extension was introduced. Initial flag, audit and final interpretation remain separate records.

No mover contact events occurred. Six unused sources remained at stock **0.2**. No repair was used. All damage, contact interruptions, event subdivisions and raw restart/command/sensor records remain preserved. The complete {src('evidence/read-only-review/ACCOUNTING.json','accounting')}, {src('evidence/read-only-review/ALL_FIXED_WINDOWS.json','fixed windows')} and {src('ANALYSIS_RESULT.json','saved-data validation')} retain detailed observations and residuals without altering the raw evidence.

## Physical-ceiling status and next layer

With A0 COMPLETE and A1–A5 OBSERVED, **the planned finite A0–A5 PHYSICAL CEILING has been exercised within its scoped bounded witness set**. This is commissioning status/evidence, not proof of optimal ecology or indefinite viability, not a frozen scientific configuration and not a canon change. The [earlier A4 and preceding evidence chain](../../{A4R}) retains each witness's limits and original apparatus provenance. A1–A4 are not relabelled as corrected-apparatus executions; A5 uses `{CP}`.

**No current A0–A5 evidence requires a Base World parameter change.** Possible future dials, including source capacity, renewal, damage and repair, remain available but **UNCHANGED**. Canon, P, Base World configuration, mechanism and numerical settings remain unchanged.

Next commissioning layer: **PERCEPTUAL CEILING**. B1–B4 and C1/C2 remain unexecuted. Scientific/developmental efficacy remains **UNTESTED**. Recording the next layer grants no execution authority, new case, experiment number or scientific configuration freeze.

## Intake custody and scope

The complete original result archive, receipt, checksum and all 127 members are preserved in a unique append-only source batch. Intake verified 126 payload hashes and CRC reads, matching expanded copies, canonical executed authority and grant/object correspondence, the trajectory receipt's payload identities, nested launch-package payloads and bound documents, exact saved summary values, and preservation inventories. Original raw-before/after and prior-file inventories remain byte-identical. The source's read-only analysis reports complete validation; this intake did not rerun that analysis, production validators, controllers, simulations or trials.

The [final clock review](../../{PREV}), all earlier sources/decisions/candidates and historical held packet remain unchanged. No necessary source gap or conflicting package identity was found. No canonical repository document, numerical setting, experiment number or Git operation was changed/created. [Source identities](SOURCE_IDENTITIES.json) · [Completion](INTAKE_RECORD.md) · [Validation](VALIDATION.json).
'''
write(ROOT/'NEW'/R,record)
nav=f'''## Current coupling commissioning — A5 observed, physical ceiling exercised, 2026-09-26

{status}

A5 executed once under authority `{AUTH}` with unchanged P `{P}` and apparatus `{CP}`: **630 nominal seconds / 63,000 native steps**, complete administrative cutoff, no retry/continuation/tuning/patch/substitution, terminal crossing or execution failure. Final E/I: **0.3667496379859223 / 0.9747806260916136**.

**Renewal availability and renewed productive uptake WERE demonstrated:** two productive revisits after approximately 217–219 seconds away, with measured unattended renewal and zero away debit. **Necessity of renewal for survival was NOT demonstrated**; recorded arithmetic is not a no-renewal counterfactual. The source-1 zero-duration contact/release reconciliation, complete contact-boundary audit and original conservative false flag remain preserved separately.

> {CLAIM}

The finite A0–A5 physical ceiling has been exercised within its scoped bounded witness set. This is commissioning evidence, not optimal ecology, indefinite viability, a frozen configuration or canon change. **No current A0–A5 evidence requires a Base World parameter change.** Future source-capacity/renewal/damage/repair dials remain available but UNCHANGED. Withhold global ecological sufficiency, optimal schedule, autonomous switching, P perception/learning/regulation and lifetime competence. B1–B4/C1–C2 remain unexecuted; naming the next layer grants no new execution.

[A5 evidence record]({R}) · [Plain-language result]({B}/A5_PLAIN_LANGUAGE_RESULT.md) · [Final result summary]({B}/A5_FINAL_RESULT_SUMMARY.json) · [Contact-boundary audit]({B}/ACTUAL_CONTACT_BOUNDARY_AUDIT.json) · [Complete preserved package]({B}/{Z.name}). A1–A4 retain their original apparatus identities; A5 uses the corrected apparatus. Earlier held/non-launchable and new-packet-required sections below are dated preparation history; the historical held hash `{OLD_AUTH}` remains unchanged.

'''
for n in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    text=(ROOT/'BEFORE'/n).read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
    old='## Current commissioning boundary — final clock correction verified, 2026-09-26';assert old in rest
    rest=rest.replace(old,'## Preserved final clock closure — before A5 execution intake, 2026-09-26',1)
    if n=='00_RESEARCH_MAP.md':
        old='selected for specification; exact external A1–A4 packages authorized | coupling commissioning in progress; V1/V2/V3/A0 complete; A5 not executed, new packet required | A1–A4 observed under original apparatus; A5 clock correction verified, old authority held/non-launchable; learning/developmental efficacy untested'
        assert old in rest
        rest=rest.replace(old,'selected for specification; exact external A1–A5 packages authorized and executed | coupling commissioning in progress; finite A0–A5 physical ceiling exercised within scoped witness set; perceptual ceiling next | A1–A5 observed external physical witnesses; P learning/developmental efficacy untested',1)
    write(ROOT/'AFTER'/n,first+'\n\n'+nav+rest.lstrip('\n'))
text=(ROOT/'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
old='## Current continuation — final clock correction verified, 2026-09-26';assert old in rest
rest=rest.replace(old,'## Preserved final clock closure — before A5 execution intake, 2026-09-26',1)
continuation=f'''## Current commissioning evidence — A5 observed; physical ceiling exercised, 2026-09-26

The [registered A5 result]({R}) is **OBSERVED COMMISSIONING EVIDENCE** under executed authority `{AUTH}`, P `{P}`, apparatus `{CP}`. One prescribed 630 nominal-second / 63,000-step external physical witness completed administrative cutoff without retry, continuation, tuning/patch/substitution, terminal crossing or execution failure. P was inactive. Two productive renewed revisits after approximately 217–219 s away were observed.

**Renewal availability and renewed productive uptake WERE demonstrated; necessity of renewal for survival was NOT demonstrated.** Preserve recorded arithmetic as attribution/accounting, never a no-renewal survival counterfactual. Preserve original source-1 conservative false flag, zero-duration contact/release evidence, complete boundary audit and final interpretation separately. No P perception/learning/regulation, autonomous switching, lifetime competence, indefinite sustainability, optimal source schedule or global ecological sufficiency claim follows.

V1/V2/V3/A0 COMPLETE; A1–A5 OBSERVED. **The planned finite A0–A5 PHYSICAL CEILING has been exercised within its scoped bounded witness set. Next layer: PERCEPTUAL CEILING.** B1–B4 and C1/C2 NOT EXECUTED; scientific/developmental efficacy UNTESTED. This is commissioning status/evidence, not optimal ecology, indefinite viability, a scientific configuration freeze or canon change. No current A0–A5 evidence requires a Base World parameter change. Source capacity, renewal, damage and repair remain available future dials but UNCHANGED.

Earlier “A5 not executed / new packet required” sections retain their dated preparation meaning. Historical held packet/hash `{OLD_AUTH}` remains unchanged; it is not the executed authority. A1–A4 retain original apparatus provenance and interpretations. No canon/P/Base World/mechanism/numerical/sequence change, new execution, experiment number or Git operation is authorized by this intake. Stop after registration/status confirmation.

'''
write(ROOT/'AFTER/AGENTS.md',first+'\n\n'+continuation+rest.lstrip('\n'))
text=(ROOT/'BEFORE/40_DECISIONS/DECISION_INDEX.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
old='## Final verification of accepted clock correction — 2026-09-26';assert old in rest
rest=rest.replace(old,'## Preserved final clock verification — before A5 execution intake, 2026-09-26',1)
idx=f'''## Executed A5 authority and physical-ceiling evidence — 2026-09-26

The [A5 evidence record](../{R}) registers the single completed case under exact executed authority `{AUTH}`, with apparatus `{CP}`. The [preserved authorization wording](../{B}/evidence/AUTHORIZATION_SOURCE.txt) and [canonical approved object](../{B}/evidence/APPROVED_OBJECT.canonical.json) govern that completed execution only. A0 COMPLETE and A1–A5 OBSERVED exercise the finite physical ceiling within its scoped bounded witness set. Perceptual ceiling next; B1–B4/C1–C2 unexecuted; efficacy UNTESTED. No current A0–A5 evidence requires a Base World parameter change; future dials remain unchanged. This is evidence/status registration, not a new execution grant, canon amendment or scientific freeze. Prior decisions and held proposal `{OLD_AUTH}` remain unchanged.

'''
write(ROOT/'AFTER/40_DECISIONS/DECISION_INDEX.md',first+'\n\n'+idx+rest.lstrip('\n'))
reg=(ROOT/'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
reg+='\n## A5 observed coupling-commissioning evidence — 2026-09-26\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:reg+=f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
reg+=f'\n[A5 evidence record]({R}). Executed authority `{AUTH}`; A5 OBSERVED. Two renewed productive revisits demonstrated; survival necessity unestablished. Initial false flag/contact audit/final summary preserved separately. Finite physical ceiling exercised within bounded witness set; perceptual ceiling next, unexecuted.\n'
write(ROOT/'AFTER/SOURCE_REGISTER.md',reg)
verification={'incoming_zip':str(Z),'zip_bytes':Z.stat().st_size,'zip_sha256':ziphash,'manifest_payloads_verified':126,'archive_members':127,
    'crc_reads_passed':True,'expanded_source_copies_match':127,'expanded_copy_check_phase':'preparation; publication rechecks sealed archive and source-batch hashes',
    'executed_canonical_sha256':AUTH,'grant_matches_approved_object':True,'trajectory_receipt_payloads_verified':len(tr['files']),
    'nested_launch_payloads_verified':len(lm['files']),'nested_launch_matches_inbox':True,'bound_file_identities_verified':len(protocol['bound_files']),
    'saved_summary_values_match_user_instruction':True,'initial_false_flag_and_final_boundary_interpretation_preserved':True,
    'raw_before_after_inventories_byte_identical':True,'original_before_after_inventories_byte_identical':True,
    'historical_held_canonical_sha256':OLD_AUTH,'A5_status':'OBSERVED COMMISSIONING EVIDENCE','native_steps':63000,
    'physical_ceiling':'finite A0–A5 exercised within scoped bounded witness set','next_layer':'PERCEPTUAL CEILING',
    'new_execution_by_intake':False,'analysis_or_tests_rerun_by_intake':False,'git_operations':False,'necessary_source_gaps':[],'identity_conflicts':[]}
inventory={q.relative_to(batch).as_posix():fsha(q) for q in batch.rglob('*') if q.is_file()}
dump(ROOT/'NEW'/S/'SOURCE_IDENTITIES.json',{'session_id':ID,'registered_sources':entries,'verification':verification,'complete_batch_sha256':inventory,'expanded_copies_verified_at_preparation':expanded})
intake=f'''# A5 evidence intake — completion

Registered **A5 OBSERVED COMMISSIONING EVIDENCE** under `{AUTH}`. [Full record](A5_COMMISSIONING_EVIDENCE_RECORD.md). The finite A0–A5 physical ceiling has been exercised within its scoped bounded witness set; next layer PERCEPTUAL CEILING, with B1–B4/C1–C2 unexecuted and scientific/developmental efficacy UNTESTED.

Read AGENTS/map/status, authority index, primary A5 plain-language/final summary, boundary audit, original support-gap summary, execution/approval/trajectory receipts and saved-data validation/preservation records. Preserved original ZIP, checksum, receipt and all 127 members, including complete trajectory and approved launch ZIP. Verified 126 payload hashes/CRC reads, matching expanded copies, canonical authority/grant, {len(tr['files'])} trajectory receipt payload identities, {len(lm['files'])} nested launch payloads, bound documents and exact saved values. Original false flag, supplemental contact audit and final interpretation remain distinct. Registered SRC-{old_count+1:03d}–SRC-{old_count+len(entries):03d}.

Updated AGENTS.md, 00_RESEARCH_MAP.md, 01_WORKSPACE_STATUS.md, SOURCE_CATALOG.json, SOURCE_REGISTER.md and 40_DECISIONS/DECISION_INDEX.md plus this new session/source batch. PRIOR_SHARED_NOTES.zip/receipt preserve all six prior shared notes. Earlier sources, candidate/review/decision/session bytes, old catalog rows and historical held A5 hash remain unchanged. [Source identities](SOURCE_IDENTITIES.json) · [Validation](VALIDATION.json).

Renewal availability and renewed productive uptake demonstrated; survival necessity not demonstrated. No counterfactual claim, parameter change, scientific freeze, canon change, new experiment number, new simulation, replay, controller recomputation, analysis rerun, actual repository modification or Git operation. No necessary source gap found. Stop after status confirmation.
'''
write(ROOT/'NEW'/S/'INTAKE_RECORD.md',intake)
dump(ROOT/'PLAN.json',{'session':S,'batch':B,'review':R,'live_before':before,'protected_before':protected,'source_entries':entries,
    'verification':verification,'zip_source':str(Z),'old_catalog_count':old_count,'status':'A5 OBSERVED; finite physical ceiling exercised within bounded witness set; perceptual ceiling next, unexecuted',
    'incoming_before':incoming,'batch_inventory':inventory})
publisher=(ROOT.parent/'2026-09-26-final-clock-review-intake-3af846d2/publish_intake.py').read_text()
publisher=publisher.replace("sha=lambda b:hashlib.sha256(b).hexdigest()", "sha=lambda b:hashlib.sha256(b).hexdigest()\ndef fsha(p):\n    h=hashlib.sha256()\n    with Path(p).open('rb') as f:\n        for block in iter(lambda:f.read(4*1024*1024),b''):h.update(block)\n    return h.hexdigest()")
for old,new in [
    ("sha((WB/name).read_bytes())","fsha(WB/name)"),
    ("sha(Path(plan['zip_source']).read_bytes())","fsha(Path(plan['zip_source']))"),
    ("sha(Path(incoming_path).read_bytes())","fsha(Path(incoming_path))"),
    ("sha((ROOT/'SOURCE_BATCH'/name).read_bytes())","fsha(ROOT/'SOURCE_BATCH'/name)"),
    ("sha((batch/name).read_bytes())","fsha(batch/name)"),
    ("data=(ROOT/'SOURCE_BATCH'/Path(e['path']).relative_to(plan['batch'])).read_bytes()\n    assert len(data)==e['bytes'] and sha(data)==e['sha256']", "q=ROOT/'SOURCE_BATCH'/Path(e['path']).relative_to(plan['batch'])\n    assert q.stat().st_size==e['bytes'] and fsha(q)==e['sha256']"),
    ("data=(WB/e['path']).read_bytes();assert sha(data)==e['sha256'] and len(data)==e['bytes']", "q=WB/e['path'];assert fsha(q)==e['sha256'] and q.stat().st_size==e['bytes']")]:
    assert old in publisher,old;publisher=publisher.replace(old,new)
write(ROOT/'publish_intake.py',publisher)
print(json.dumps({'prepared':ID,'sources':len(entries),'protected_files':len(protected),'batch_files':len(inventory),'nested_launch_payloads':len(lm['files'])}),flush=True)
