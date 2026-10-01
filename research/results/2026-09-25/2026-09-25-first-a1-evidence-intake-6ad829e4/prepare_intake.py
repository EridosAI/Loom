"""Register immutable supplied evidence. No research imports, execution or V3 rerun."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib, io, json, zipfile, collections

ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ID='2026-09-25-first-a1-evidence-intake-6ad829e4'
S=f'50_SESSIONS/{ID}'
B='90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4'
R=S+'/FIRST_A1_COMMISSIONING_EVIDENCE_RECORD.md'
INBOX=WB/'INBOX/2026-09-25-first-A1-commissioning-result-5f077481'
Z=INBOX/'FIRST_A1_COMMISSIONING_RESULT.zip'
REQUEST=Path(r'C:\Users\Jason\.codex\attachments\e51c086b-ace3-442d-bfa7-8fe9e2bfb6c0\Pasted text.txt')
LAUNCH_INBOX=WB/'INBOX/2026-09-25-first-commissioning-launch-packet-5f077481'
CP='5f07748102cb5eaa302569c87efbae095050e9fe'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
AUTH='a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc'
PRED='30_REVIEWS/REVIEW-P-APPARATUS-MECHANICAL-CLOSURE-5f077481-2026-09-25-c84f219a.md'
PRED_SOURCE='90_SOURCES/p_final_mechanical_closure_2026-09-25_c84f219a/LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md'
PRE='FIRST_COMMISSIONING_LAUNCH_PACKET/'
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,t):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,x):write(p,json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def verify_zip(z,prefix=''):
    names=z.namelist()
    assert len(names)==len(set(names))==len({n.casefold() for n in names})
    for n in names:
        p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and ':' not in n and '\\' not in n
    m=json.loads(z.read(prefix+'FILE_MANIFEST.json'))
    assert {prefix+n for n in m['files']}==set(names)-{prefix+'FILE_MANIFEST.json'}
    for n,meta in m['files'].items():
        b=z.read(prefix+n);assert len(b)==meta['bytes'] and sha(b)==meta['sha256'],n
    assert z.testzip() is None
    return {'members':len(names),'payloads':len(m['files']),'length_sha256_crc_valid':True,'safe_unique_paths':True}

receipt=json.loads((INBOX/'DELIVERY_RECEIPT.json').read_text(encoding='utf-8-sig'))
raw=Z.read_bytes();assert len(raw)==receipt['zip']['bytes'] and sha(raw)==receipt['zip']['sha256']
assert receipt['authority_sha256']==AUTH and receipt['apparatus_checkpoint']==CP
z=zipfile.ZipFile(io.BytesIO(raw));outer=verify_zip(z)
for name in ['FIRST_A1_COMMISSIONING_REPORT.md','README.md','FILE_MANIFEST.json','PRESERVATION_CHECK.json']:
    assert z.read(name)==(INBOX/name).read_bytes(),name
launch_bytes=z.read('approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip')
assert launch_bytes==(LAUNCH_INBOX/'FIRST_COMMISSIONING_LAUNCH_PACKET.zip').read_bytes()
launch_receipt=json.loads((LAUNCH_INBOX/'PACKAGE_RECEIPT.json').read_text(encoding='utf-8-sig'))
assert len(launch_bytes)==launch_receipt['bytes'] and sha(launch_bytes)==launch_receipt['sha256']
launch=zipfile.ZipFile(io.BytesIO(launch_bytes));launch_check=verify_zip(launch,PRE)
assert launch.read(PRE+'references/LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md')==(WB/PRED_SOURCE).read_bytes()
canonical=z.read('evidence/APPROVED_OBJECT.canonical.json')
assert sha(canonical)==AUTH and canonical==launch.read(PRE+'AUTHORITY_OBJECT.canonical.json')
approved=json.loads(canonical)
envelope=json.loads(z.read('evidence/APPROVAL_REQUEST.json'))
manifest=json.loads(z.read('evidence/LAUNCHED_MANIFEST.json'))
assert approved==envelope['approved_execution']=={k:v for k,v in manifest.items() if k!='execution_authority'}
assert envelope['approved_execution_sha256']==manifest['execution_authority']['approved_execution_sha256']==AUTH
assert sha(z.read('evidence/APPROVAL_REQUEST.json'))==manifest['execution_authority']['request_sha256']
assert z.read('evidence/AUTHORIZATION_SOURCE.txt').decode('utf-8-sig').strip()==envelope['notice']
assert manifest['baseline']==P and manifest['case_id']=='A1' and manifest['mode']=='external_controller'
assert manifest['execution']['procedure']['protocol']['reviewed_checkpoints']['apparatus_git_sha']==CP
summary=json.loads(z.read('evidence/read-only-review/A1_RESULT_SUMMARY.json'))
execution=json.loads(z.read('evidence/EXECUTION_RESULT.json'))
trajectory=json.loads(z.read('evidence/trajectory-001/manifest.json'))
v3=json.loads(z.read('evidence/read-only-review/V3_COUNT_FINDING.json'))
assert summary['authority_sha256']==execution['approved_execution_sha256']==AUTH
assert trajectory['contract']==manifest and trajectory['complete'] is True
assert trajectory['status']==summary['stop_reason']=='administrative_pause'
assert trajectory['stop_cause']==summary['stop_cause']=='wall_time_limit'
assert summary['attempts']==execution['run_constructors_attempted']==1
assert execution['no_retry_no_resume_no_patch'] is True and execution['physical_replays']==0
assert summary['native_records']==trajectory['records']['native']==9183
assert summary['event_records']==trajectory['records']['events']==9185
assert summary['command_decisions']==trajectory['records']['controller']==919
assert summary['wave_records']==0 and summary['V3'] is None
assert trajectory['records']['sensor']==v3['receipt_record_counts']['sensor']==9184
assert sha(z.read('evidence/read-only-review/read_results.py'))==v3['checker_sha256']
assert 'AssertionError' in z.read('evidence/read-only-review/V3_BOUNDARY_ERROR.json').decode('utf-8-sig')

# Count only labels already saved in the packaged observation table. Do not run its analysis.
obs=json.loads(z.read('evidence/read-only-review/A1_OBSERVATIONS.json'))
counts=collections.Counter((w['complete_0_2_second_interval'],w['source_0_positive_duration_contact'],w['net_energy_sign']) for w in obs['all_fixed_windows'])
assert counts=={(True,False,'negative_resolved'):31,(True,True,'positive_resolved'):229,(True,True,'negative_resolved'):199,(False,True,'negative_resolved'):1}
conflict={
    'request_wording':'459 complete contact windows',
    'packaged_summary_field':'complete_fixed_windows = 459',
    'saved_window_labels':{'complete_fixed_total':459,'complete_with_contact':428,'complete_without_contact':31,'complete_contact_positive_resolved':229,'complete_contact_negative_resolved':199,'partial_tail_contact_negative_resolved':1},
    'source_member':'evidence/read-only-review/A1_OBSERVATIONS.json::all_fixed_windows',
    'resolution':'Record 459 complete fixed windows in total, of which 428 contain positive-duration source-0 contact; preserve original request and evidence. This is a census of stored labels, not corrected V3 analysis.',
    'first_positive_window_note':'The 6.2–6.4 s complete fixed bin contains first contact at 6.31019048650431 s; complete describes the bin, not contact throughout it.'}

live=['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md']
before={}
for name in live:
    b=(WB/name).read_bytes();before[name]={'bytes':len(b),'sha256':sha(b)}
    p=ROOT/'BEFORE'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
protected={}
for folder in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS','50_SESSIONS/2026-09-25-p-mechanical-closure-intake-c84f219a']:
    for p in (WB/folder).rglob('*'):
        if p.is_file():protected[p.relative_to(WB).as_posix()]=sha(p.read_bytes())
incoming_before={str(p):sha(p.read_bytes()) for p in INBOX.iterdir() if p.is_file()}
incoming_before[str(REQUEST)]=sha(REQUEST.read_bytes())
incoming_before[str(LAUNCH_INBOX/'FIRST_COMMISSIONING_LAUNCH_PACKET.zip')]=sha(launch_bytes)
catalog=json.loads((ROOT/'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'));old_count=len(catalog['source_files']);assert old_count==93
selected=[
    ('attachment','Pasted text.txt','current-Jason-evidence-registration-request'),
    ('inbox',Z.name,'immutable-first-A1-result-archive'),
    ('inbox','DELIVERY_RECEIPT.json','result-delivery-identity-receipt'),
    ('result','FIRST_A1_COMMISSIONING_REPORT.md','first-A1-execution-report'),
    ('result','FILE_MANIFEST.json','complete-result-payload-manifest'),
    ('result','PRESERVATION_CHECK.json','execution-delivery-preservation-record'),
    ('result','README.md','result-reading-and-scope-note'),
    ('result','approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip','untouched-approved-preparation-packet'),
    ('launch',PRE+'FIRST_COMMISSIONING_LAUNCH_PACKET.md','original-launch-proposal-later-authorized-exactly'),
    ('result','evidence/APPROVED_OBJECT.canonical.json','exact-executed-authority-object'),
    ('result','evidence/AUTHORIZATION_SOURCE.txt','Jason-exact-bounded-execution-approval-as-packaged'),
    ('result','evidence/APPROVAL_REQUEST.json','closed-approval-envelope'),
    ('result','evidence/LAUNCHED_MANIFEST.json','actual-launched-manifest-and-grant'),
    ('result','evidence/EXECUTION_RESULT.json','one-attempt-execution-record'),
    ('result','evidence/read-only-review/A1_RESULT_SUMMARY.json','saved-first-A1-observations-summary'),
    ('result','evidence/read-only-review/V3_POST_CHECK_LIMITATION.md','preserved-incomplete-V3-analysis-limitation'),
    ('result','evidence/read-only-review/V3_COUNT_FINDING.json','preserved-sensor-envelope-count-finding'),
    ('result','evidence/read-only-review/V3_BOUNDARY_ERROR.json','original-V3-AssertionError'),
    ('result','evidence/read-only-review/read_results.py','original-failed-analysis-source-do-not-execute'),
    ('result','evidence/read-only-review/V1_POST_RECORD_VALIDATION.json','completed-existing-validator-record-no-replay'),
    ('result','evidence/read-only-review/V1_V3_PREFLIGHT.json','completed-preflight-record'),
    ('result','evidence/read-only-review/A0_GEOMETRY.json','zero-evolution-approved-geometry-record'),
    ('result','evidence/read-only-review/SOURCE_0_CONTACT_INTERVALS.json','saved-certified-contact-intervals'),
    ('result','evidence/trajectory-001/manifest.json','original-trajectory-receipt'),
]
entries=[]
for number,(origin,member,role) in enumerate(selected,old_count+1):
    if origin=='attachment':b=REQUEST.read_bytes();source=str(REQUEST);dest=member
    elif origin=='inbox':b=(INBOX/member).read_bytes();source=str(INBOX/member);dest=member
    elif origin=='result':b=z.read(member);source=str(Z)+'::'+member;dest=member
    else:b=launch.read(member);source=str(Z)+'::approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip::'+member;dest='approved-launch/'+member
    p=ROOT/'SOURCE_BATCH'/dest;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    entries.append({'source_id':f'SRC-{number:03d}','path':B+'/'+dest,'original_filename':PurePosixPath(member).name,'bytes':len(b),'sha256':sha(b),
        'role':role,'prepared':'2026-09-25','stated_author':'Jason (current attached request)' if origin=='attachment' else ('Jason authorization as preserved in delivery' if member.endswith('AUTHORIZATION_SOURCE.txt') else 'Supplied execution/preparation record; exact assistant model/backend not stated'),
        'authority':'Evidence registration only; the archived grant authorizes only its already executed bounded package, not continuation or repetition',
        'acquired_from':source,'archive_member':member if origin in ['result','launch'] else None,'reviewed_checkpoint':CP,'p_baseline_checkpoint':P,
        'executed_authority_sha256':AUTH,'review_note':R,'record':S+'/INTAKE_RECORD.md','notes':'Original bytes preserved. Entire raw trajectory, all calculation operands and original failed analysis remain in the result ZIP. No code execution during intake.'})
catalog['source_files']+=entries
catalog.setdefault('intake_events',[]).append({'session_id':ID,'source_ids':[e['source_id'] for e in entries],'review_note':R,'record':S+'/INTAKE_RECORD.md',
    'scope':'First actual A1 external physical witness; coupling commissioning IN PROGRESS; V3 incomplete; learning/developmental efficacy untested; no new execution authority'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)

def source(member,label):return f'[{label}](../../{B}/{member})'
status='''P engineering: **VERIFIED**  
Commissioning apparatus: **FIT / CLOSED FOR PRE-RUN ENGINEERING**  
Coupling commissioning: **IN PROGRESS**  
First physical witness: **A1 OBSERVED — bounded external-control witness**  
V3: **INCOMPLETE — post-analysis checker limitation**  
Scientific/developmental efficacy: **UNTESTED**'''
short='''V1, V2 and A0 completed; exactly one A1 external physical witness executed. It stopped administratively at **91.83 simulated seconds** / **9,183 native rows**, cause `wall_time_limit`, record `complete=True`. No retry, resume or replacement trajectory occurred; the remaining **28.17 s** of the 120 s ceiling is unobserved. V3 post-check is incomplete at the preserved sensor/native-count assertion; it has not been corrected or rerun.'''
metric_groups=[
 ('Physical approach and contact',[
 ('Contact locus reached / certified source-0 contact','yes / yes'),
 ('Minimum recorded source surface gap',str(summary['minimum_source_surface_gap'])),
 ('First certified source-0 contact, s',str(summary['first_contact_time'])),
 ('Positive-duration source contact, s',str(summary['positive_duration_contact_seconds'])),
 ('Contiguous contact intervals',str(summary['contact_interval_count'])),
 ('Measured contact-force range',f"{summary['sustained_force_min']} to {summary['sustained_force_max']}"),
 ('Requested contact-force target','0.1')]),
 ('Energy and accounting',[
 ('Source-0 transfer',str(summary['source_0_transfer'])),
 ('Reconstructed source debit',str(summary['source_0_debit_from_stock_and_renewal'])),
 ('Reconstructed body credit',str(summary['body_credit_from_energy_and_cost'])),
 ('Whole-attempt expenditure',str(summary['total_expenditure'])),
 ('Energy, initial → final',f"{summary['initial_energy']} → {summary['final_energy']}"),
 ('Whole-attempt energy change','+'+str(summary['whole_attempt_energy_delta'])),
 ('Source-0 final stock',str(summary['source_0_final_stock'])),
 ('Cumulative source-0 renewal',str(summary['source_0_renewal'])),
 ('Maximum accounting residual',str(summary['maximum_accounting_residual'])),
 ('Existing arithmetic tolerance','1e-12')]),
 ('Windows, integrity and records',[
 ('Complete fixed 0.2 s windows, total','459; 428 contain contact, 31 do not'),
 ('Complete contact-containing bins with resolved positive / negative net energy','229 / 199'),
 ('Partial tail','1; retained separately'),
 ('First complete positive-net contact-containing bin','6.2–6.4 s'),
 ('Energy change in that bin','+'+str(summary['first_positive_net_contact_window']['energy_delta'])),
 ('Integrity, initial → final',f"{summary['initial_integrity']} → {summary['final_integrity']}"),
 ('Physical nonviability / terminal dimension','none / `None`'),
 ('Controller/apparatus exception','none; separate V3 analysis AssertionError retained'),
 ('Native / physical event / controller decision / neural wave rows','9,183 / 9,185 / 919 / 0'),
 ('Sensor entries / diagnostic rows','9,184 / 9,183')])]
tables=''
for title,rows in metric_groups:
    tables+='### '+title+'\n\n| Observation | Packaged value |\n|---|---|\n'
    for label,value in rows:tables+=f'| {label} | {value} |\n'
    tables+='\n'
record=f'''# First Loom P coupling-commissioning evidence record

**Recorded:** 2026-09-25. **Classification:** observed commissioning evidence from one bounded external-control A1 witness, with incomplete V3 post-analysis. This registration adds no physical execution or corrected analysis.

{status}

**COUPLING COMMISSIONING HAS BEGUN.** The previous [mechanical closure](/PLACEHOLDER) remains the pre-run engineering disposition; its “NOT STARTED / UNCOMMISSIONED” statements describe that earlier stage. The present evidence does not retroactively change any prior checkpoint hold or engineering review.

## Exact source and execution identities

| Identity | Value |
|---|---|
| P implementation | `{P}` |
| Commissioning apparatus | `{CP}` |
| Executed canonical authority object | `{AUTH}` |
| Case / mode / controller | `A1` / `external_controller` / `waypoint` |
| Scope | V1–V3, A0 and exactly one A1 external physical witness |
| Packaged execution finish | `{execution['finish_utc']}` |

Primary evidence: {source('FIRST_A1_COMMISSIONING_REPORT.md','original A1 report')}, {source('FIRST_A1_COMMISSIONING_RESULT.zip','verified result ZIP')}, {source('evidence/read-only-review/A1_RESULT_SUMMARY.json','saved result summary')}, {source('evidence/trajectory-001/manifest.json','original trajectory receipt')} and {source('DELIVERY_RECEIPT.json','delivery identity receipt')}. The result ZIP preserves the complete raw `evidence/trajectory-001/` tree, including all streams, snapshots, display, receipt and original analysis files. It also preserves the complete original calculation tables `evidence/read-only-review/A1_OBSERVATIONS.json` and `V2_ACCOUNTING.json`.

## Jason-accepted authority, distinct from observations

The {source('evidence/AUTHORIZATION_SOURCE.txt','untouched authorization source')} explicitly approves the exact object above for V1–V3/A0 and one A1, with “Report-don’t-patch.” Its {source('evidence/APPROVAL_REQUEST.json','closed approval envelope')}, {source('evidence/APPROVED_OBJECT.canonical.json','canonical approved bytes')} and {source('evidence/LAUNCHED_MANIFEST.json','actual launched manifest and six-field grant')} are preserved. The canonical object in the executed result is byte-identical to the original launch packet's object, and its SHA-256 matches the approved identity.

The {source('approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip','untouched launch packet')} and {source('approved-launch/'+PRE+'FIRST_COMMISSIONING_LAUNCH_PACKET.md','original launch description')} retain their pre-approval “PROPOSED / NOT AUTHORIZED” labels. Those are historical preparation labels; later genuine authorization is recorded separately above. No proposal text or bound path has been rewritten. The packet's statement about an older Workbench HOLD is also its preparation-time navigation observation, not current status.

The declared manufactured external start used body centre (6,3), facing west, $E=0.7$ and $I=1$, the existing life-0 cache and phase, and one source-0 pressure stage at requested force 0.1. It was not a newborn life or intact-P actuation. The 120 s simulated ceiling and 1,200 s run wall limit belonged to that exact object. This intake records the already exercised authority; it grants no repetition, resume, extension, changed route, subsequent case or architectural decision.

## Observed commissioning evidence

{short}

The saved execution time is `{summary['simulated_seconds']}` s; 91.83 s is the report's readable value. `complete=True` records closure of the stopped attempt's records, not completion of the 120 s ceiling or all commissioning checks. Original evidence reports no physical nonviability and no controller/apparatus exception. The V3 checker failure is a separate analysis result.

The tables reproduce the saved summary's numeric values at its recorded precision. The report rounds them for reading; no tolerance, gate or physical quantity has been changed.

{tables}
The transfer, reconstructed debit and reconstructed credit round to the same reported `0.190521120591`; their machine-precision values are separately retained above, rather than asserted to be bit-identical. Source-0 debit minus transfer is `{summary['source_0_debit_minus_transfer']}` and body credit minus transfer is `{summary['body_credit_minus_transfer']}`. The existing arithmetic tolerance and maximum residual are recorded as evidence, not new acceptance gates.

The first positive bin's saved endpoints are `{summary['first_positive_net_contact_window']['start_time']}` and `{summary['first_positive_net_contact_window']['end_time']}` s. First contact occurs inside that bin. “Complete” denotes the full fixed time bin; it does not mean contact throughout all 0.2 s. Whole-attempt energy gain is distinct from the positive and negative contact-containing windows. One partial terminal bin remains separate.

## Completed checks and the preserved V3 limitation

| Item | Recorded disposition |
|---|---|
| V1 | Completed; preflight identities and the existing post-record validator with `replay=false` are preserved |
| V2 | Completed; historical precheck remains labelled historical, and the actual A1 contact/accounting operands remain distinct |
| A0 | Completed without world evolution; geometry only, no bypass/crossing trajectory |
| A1 | One external physical witness observed, administratively truncated |
| V3 | Initial checks completed; post-check **INCOMPLETE** at the original assertion; subsequent comparisons not reached |

Sources: {source('evidence/read-only-review/V1_V3_PREFLIGHT.json','V1/V3 preflight')}, {source('evidence/read-only-review/V1_POST_RECORD_VALIDATION.json','V1 post-record validation')}, {source('evidence/read-only-review/A0_GEOMETRY.json','A0 geometry')}, {source('evidence/read-only-review/V3_POST_CHECK_LIMITATION.md','V3 limitation')}, {source('evidence/read-only-review/V3_COUNT_FINDING.json','V3 count finding')}, {source('evidence/read-only-review/V3_BOUNDARY_ERROR.json','original AssertionError')} and {source('evidence/read-only-review/read_results.py','original failed checker — preserved source, not a runnable instruction')}.

The checker wrongly asserted equal native/sensor/diagnostic counts. The recorder contains one initial sensor/display envelope at native index 0, followed by the per-step rows: **9,184 sensor entries versus 9,183 native and diagnostic rows**. This is the preserved reader/schema-assumption limitation, not evidence of an extra native update.

The recorded preceding comparisons of complete inactive-organism state, organism RNG counters, manifest equality and closed display schema had completed before the assertion. Subsequent display/stream, actual controller-input, issued/delivered-command, raw/native and E/I cadence comparisons and final counter/state assertions were not reached. The separately completed existing segment validator checked its issued-decision journal, sequence, receipt/file hashes, ledger and stop classification with no physical replay. It does not make V3 complete.

No corrected V3 checker, rerun or replacement analysis is supplied or performed here. Any later corrected read-only analysis must be a **new analysis of this same immutable A1 evidence**, linked to this original failure. It must not replace the failed checker, its error, these findings or the trajectory.

## Claim boundary

One externally controlled commissioning witness demonstrated that the implemented finite body can, in the tested geometry, physically reach source-0, establish solver-certified contact, receive real source-to-body energy transfer, and experience complete contact-containing intervals with resolved positive net energy under the implemented mechanics and accounting. This statement retains the incomplete V3 post-check qualification above.

This does **not** establish that P can discover, perceive, recognise, learn from or regulate toward the source; newborn bootstrap; survival capability; global ecological sufficiency; indefinite viability; or usefulness of P, R or any associative mechanism. The neural object was inactive in this external arm; zero neural waves does not constitute a perceptual/developmental trial. P remains scientifically **UNTESTED for learning/developmental efficacy**. No P PASS/FAIL, scientific efficacy result or new experiment number is assigned.

## Unresolved observations and work not performed

Retain as observations/open interpretations: integrity declined from 1 to 0.9930767410641572; measured force reached 0.27074663791428305 while the requested target was 0.1; contact contained both positive-net and negative-net windows; the wall-time boundary truncated the 120 s ceiling at 91.83 s; and V3 remains incomplete. These are not automatically apparatus defects, mechanism failures or permission to change configuration.

Not performed: A2–A5; B1–B4; C1/C2; newborn lives; fixed-structure diagnostic; perceptual commissioning; developmental/scientific trials; efficacy testing; tuning/sweeps; or evidential freeze. The remaining 28.17 s is unobserved. This task introduces **no assistant proposal** for a new route, case, parameter, architecture or sequence. All earlier candidate alternatives, accepted Base World choices and decisions remain unchanged.

## Source discrepancy and custody

The intake request says **“459 complete contact windows.”** The primary summary says `complete_fixed_windows: 459`. The saved `all_fixed_windows` labels contain **428 complete bins with contact** (229 positive, 199 negative), **31 complete bins without contact**, and **one separate partial contact tail**. This registration follows those primary records and explicitly preserves the discrepancy. [Source-conflict record](SOURCE_CONFLICTS.json) records the label census; it is not new physical analysis or a corrected V3 check. Rounded human-readable values versus machine precision are retained as representations of the same saved quantities.

The package, report copies, original authority and launch packet agree on their identities. The source ZIP passed its supplied receipt, every payload hash/size and CRC; the embedded launch packet matches the separately supplied launch ZIP and its manifest. [Source identities](SOURCE_IDENTITIES.json) and [intake completion](INTAKE_RECORD.md) record the exact checks and edits. No packaged code, validator, checker, replay or scientific trial was executed by this intake. No canonical repository document, configuration, world/mechanism law, accepted architecture or commissioning sequence was changed.
'''
record=record.replace('(/PLACEHOLDER)',f'(../../{PRED})')
write(ROOT/'NEW'/R,record)
nav=f'''## Current coupling commissioning — first A1, 2026-09-25

{status}

**COUPLING COMMISSIONING HAS BEGUN.** P `{P}`; apparatus `{CP}`. Executed authority: `{AUTH}`.

{short}

[Evidence record, exact values and claim boundary]({R}) · [A1 report]({B}/FIRST_A1_COMMISSIONING_REPORT.md) · [Result package]({B}/FIRST_A1_COMMISSIONING_RESULT.zip) · [Untouched launch packet]({B}/approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip) · [Exact authority object]({B}/evidence/APPROVED_OBJECT.canonical.json) · [Jason's authorization source]({B}/evidence/AUTHORIZATION_SOURCE.txt) · [Preserved V3 limitation]({B}/evidence/read-only-review/V3_POST_CHECK_LIMITATION.md) · [Pre-run mechanical closure]({PRED}).

One external witness reached source-0, established certified contact and received real energy transfer, with both positive-net and negative-net contact-containing windows. This establishes no P discovery, perception, learning, regulation, survival capability or ecological adequacy. Saved labels show 459 complete fixed bins in total, **428 containing contact**; the request's “459 complete contact windows” wording is explicitly qualified in the evidence record.

A2–A5, B1–B4, C1/C2, newborn lives, fixed-structure diagnostic, perceptual commissioning, developmental/scientific trials, efficacy testing, tuning/sweeps and evidential freeze remain unperformed. This is evidence registration only; no continuation, corrected V3 analysis or new execution is authorized. Earlier pre-run and HOLD dispositions below remain historical snapshots.

'''
for name in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    text=(ROOT/'BEFORE'/name).read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
    rest=rest.replace('## Current apparatus mechanical closure — 2026-09-25','## Preserved pre-run mechanical closure — 2026-09-25',1)
    rest=rest.replace('## Current commissioning design — 2026-09-23 (review draft)','## Preserved commissioning design — 2026-09-23 (review draft)',1)
    rest=rest.replace('## Current P engineering baseline — 2026-09-23','## Preserved P engineering clearance — 2026-09-23',1)
    rest=rest.replace('## Current engineering checkpoint — 2026-09-23','## Preserved P engineering clearance — 2026-09-23',1)
    if name=='00_RESEARCH_MAP.md':
        old='| [P](20_CANDIDATES/CAND-P.md) | Fast sensory query participation plus slow retention | selected for specification | fit to proceed to coupling commissioning at 6bc9683b | uncommissioned / untested |'
        new='| [P](20_CANDIDATES/CAND-P.md) | Fast sensory query participation plus slow retention | selected for specification; exact first external A1 package authorized | coupling commissioning in progress; V3 incomplete | bounded external A1 observed; learning/developmental efficacy untested |'
        assert old in rest;rest=rest.replace(old,new,1)
    write(ROOT/'AFTER'/name,first+'\n\n'+nav+rest.lstrip('\n'))
text=(ROOT/'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
rest=rest.replace('## Current apparatus mechanical closure — 2026-09-25','## Preserved pre-run mechanical closure — 2026-09-25',1)
continuation=f'''## Current commissioning evidence — 2026-09-25

The [first actual A1 evidence record]({R}) registers execution under exact authority `{AUTH}` with P `{P}` and apparatus `{CP}`. **Coupling commissioning is IN PROGRESS:** V1/V2/A0 completed and one bounded external-control A1 witness was observed. V3 post-analysis remains **INCOMPLETE** at the preserved checker error; scientific/developmental efficacy remains **UNTESTED**. Engineering remains verified and apparatus FIT / CLOSED FOR PRE-RUN ENGINEERING.

The [original authorization source]({B}/evidence/AUTHORIZATION_SOURCE.txt) belongs to that already executed package only. The 91.83 s attempt stopped at its wall-time limit without retry/resume; its remaining 28.17 s is unobserved. Prior “NOT STARTED / UNCOMMISSIONED” text below is pre-run history, not current commissioning status. Preserve the original failure, checker, V3 limitation and immutable raw records. Any later corrected analysis is a new analysis of the same evidence, never a replacement run or rewritten history. This intake authorizes no further execution, corrected checker, tuning, sequence/canon/architecture change or Git operation.

'''
write(ROOT/'AFTER/AGENTS.md',first+'\n\n'+continuation+rest.lstrip('\n'))
register=(ROOT/'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
register+='\n## First A1 coupling-commissioning evidence — 2026-09-25\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:register+=f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
register+=f'\nExecuted authority `{AUTH}`; unchanged P `{P}`; apparatus `{CP}`. Coupling commissioning **IN PROGRESS**, one A1 external witness observed, V3 **INCOMPLETE**, learning/developmental efficacy **UNTESTED**. [Evidence and explicit source discrepancy]({R}) · [Intake/custody]({S}/INTAKE_RECORD.md). Original raw trajectory and failed analysis are preserved in the unchanged ZIP; no rerun or new architectural decision.\n'
write(ROOT/'AFTER/SOURCE_REGISTER.md',register)
verification={'incoming_zip':str(Z),'zip_bytes':len(raw),'zip_sha256':sha(raw),'manifest_payloads_verified':outer['payloads'],
    'result_archive':outer,'launch_archive':launch_check,'launch_zip_sha256':sha(launch_bytes),'launch_matches_separate_inbox_copy':True,
    'outer_matches_delivery_receipt':True,'loose_report_manifest_readme_preservation_match_zip':True,'predecessor_review_matches_packaged_reference':True,
    'canonical_authority_sha256':AUTH,'approved_canonical_bytes_match_original_launch':True,'approval_envelope_and_launched_object_match':True,
    'apparatus_checkpoint':CP,'p_baseline_checkpoint':P,'original_checker_matches_recorded_hash':True,
    'source_discrepancy':conflict,'source_counts_copied_from_receipt_and_summary':True,
    'new_physical_execution':False,'new_corrected_V3_analysis':False,'packaged_program_execution':False,'git_operations':False}
session=ROOT/'NEW'/S
dump(session/'SOURCE_IDENTITIES.json',{'sources':entries,'verification':verification,'incoming_files_before':incoming_before})
dump(session/'SOURCE_CONFLICTS.json',{'material_wording_discrepancy':conflict,'identity_conflicts':[],
    'historical_labels':'Original launch proposal labels precede the preserved genuine grant. Earlier NOT STARTED navigation is pre-run history; originals not rewritten.'})
intake=f'''# First A1 evidence intake — completion

**Session:** `{ID}`; 2026-09-25. Jason's [attached instruction](../../{B}/Pasted%20text.txt) authorizes evidence registration and live status/navigation only.

{status}

Added the [commissioning evidence record](FIRST_A1_COMMISSIONING_EVIDENCE_RECORD.md), source identities and explicit [source discrepancy](SOURCE_CONFLICTS.json). Registered **SRC-094–117**: current request, original result ZIP/receipt/report, untouched launch packet, exact approval/authority, saved observations/receipts and original V3 checker/failure/limitation. Complete raw A1 records and all calculation operands remain unchanged inside the ZIP; selected reading copies preserve original bytes and member paths.

Updated AGENTS, research map, workspace status, source catalog and source register. Historical pre-run headings are labelled as history; the map's live P row now distinguishes commissioning progress from untested learning/developmental efficacy. Existing candidate files, earlier review/checkpoint dispositions, source rows and decision records are unchanged. No new scientific experiment number, architecture ruling or accepted mechanism conclusion was created. The five prior shared files are preserved in the session's local recovery ZIP.

Read the current workbench instructions/map/status, intake instructions, attached user request, complete first A1 report/README, result/launch receipts, exact grant/authority, execution and trajectory receipts, saved observation summary, V1/V3 preflight, V3 limitation/count/error and relevant original checker section, launch description and predecessor closure. Parsed manifest inventories and the existing fixed-window labels. No research utility or packaged checker was imported or run.

Actual validation: **{outer['payloads']} result payloads** in {outer['members']} members, and **{launch_check['payloads']} launch payloads** in {launch_check['members']} members pass size/SHA-256/CRC and safe unique-path checks. Result ZIP matches its delivery receipt; loose report/manifest/README/preservation files match the ZIP. The launch ZIP matches the separate supplied original and its receipt. Approved canonical bytes match the original launch and exact authority hash; approval envelope and launched manifest bind the same object. The original V3 checker matches its saved hash. The packaged predecessor review matches the registered source. These are custody/consistency checks, not a new V3 or independent scientific validation.

One wording conflict was found: the request's “459 complete contact windows” versus 459 complete **fixed** windows in the primary summary. Existing saved labels identify 428 complete contact-containing bins (229 positive, 199 negative), 31 complete bins without contact, and one partial contact tail. The evidence record preserves that distinction and the original request. No checkpoint, authority or payload-identity conflict was found. Rounded report quantities and full saved precision remain distinct representations, not silently equalized values.

The V3 error, failed checker and exact raw evidence remain historical immutable sources. No corrected check, physical replay, extra native step, retry, resume, replacement trajectory, configuration change, commissioning sequence change, canonical repository edit or Git operation occurred. P efficacy remains untested. No actual repository or unrelated vault activity was inspected. [VALIDATION.json](VALIDATION.json) records saved-file, source-row, link, recovery and preservation checks. Intake complete; stop.
'''
write(session/'INTAKE_RECORD.md',intake)
dump(ROOT/'PLAN.json',{'session':S,'batch':B,'review':R,'live_before':before,'protected_before':protected,'source_entries':entries,
    'verification':verification,'zip_source':str(Z),'old_catalog_count':old_count,'status':'COUPLING COMMISSIONING IN PROGRESS; V3 INCOMPLETE; EFFICACY UNTESTED','incoming_before':incoming_before})
print(json.dumps({'ready_to_validate':True,'result':outer,'launch':launch_check,'source_count':len(entries),'source_ids':[entries[0]['source_id'],entries[-1]['source_id']],
    'protected':len(protected),'window_label_discrepancy':conflict['saved_window_labels']}))
