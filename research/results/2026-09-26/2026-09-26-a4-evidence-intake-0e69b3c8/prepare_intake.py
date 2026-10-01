"""A4 documentation intake: preserved bytes and supplied results only."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib, io, json, zipfile

ROOT = Path(__file__).resolve().parent
WB = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ID = '2026-09-26-a4-evidence-intake-0e69b3c8'
S = '50_SESSIONS/' + ID
B = '90_SOURCES/p_a4_commissioning_2026-09-26_0e69b3c8'
R = S + '/A4_COMMISSIONING_EVIDENCE_RECORD.md'
D = WB / 'INBOX/2026-09-26-A4-commissioning-result-5f077481'
LD = WB / 'INBOX/2026-09-26-A4-launch-packet-5f077481'
Z = D / 'A4_COMMISSIONING_RESULT.zip'
AUTH = '47a71e78ad4bbb920f2b29f7d9b0e3c5f520eb4905880916c85f0cc8bbb9f1e0'
P = '6bc9683b54e4fa80136fe8534d7713e2a250a95f'
CP = '5f07748102cb5eaa302569c87efbae095050e9fe'
A3R = '50_SESSIONS/2026-09-26-a3-evidence-intake-7c42a9d1/A3_COMMISSIONING_EVIDENCE_RECORD.md'
A3B = '90_SOURCES/p_a3_commissioning_2026-09-26_7c42a9d1'
RR = 'evidence/read-only-review/'
CASES = ['A4-CROSS', 'A4-WAIT', 'A4-DETOUR']
sha = lambda b: hashlib.sha256(b).hexdigest()

def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')

def dump(p, value):
    write(p, json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def archive_check(z):
    names = z.namelist()
    assert len(names) == len(set(names)) == len({n.casefold() for n in names})
    for n in names:
        p = PurePosixPath(n)
        assert not p.is_absolute() and '..' not in p.parts and ':' not in n and '\\' not in n
    m = json.loads(z.read('FILE_MANIFEST.json'))
    assert set(m['files']) == set(names) - {'FILE_MANIFEST.json'}
    for n, meta in m['files'].items():
        data = z.read(n)
        assert len(data) == meta['bytes'] and sha(data) == meta['sha256'], n
    assert z.testzip() is None
    return m

raw = Z.read_bytes()
receipt = json.loads((D / 'DELIVERY_RECEIPT.json').read_text(encoding='utf-8-sig'))
copy_receipt = json.loads((D / 'COPY_VERIFICATION.json').read_text(encoding='utf-8-sig'))
assert len(raw) == receipt['bytes'] and sha(raw) == receipt['sha256'] == copy_receipt['zip_sha256']
assert receipt['authority_sha256'] == copy_receipt['authority_sha256'] == AUTH
z = zipfile.ZipFile(io.BytesIO(raw))
mf = archive_check(z)
assert mf['authority_sha256'] == AUTH and len(mf['files']) == receipt['verified_payloads'] == copy_receipt['verified_payloads'] == 121
incoming = {str(Z): sha(raw)}
for n in ['DELIVERY_RECEIPT.json', 'COPY_VERIFICATION.json']:
    incoming[str(D / n)] = sha((D / n).read_bytes())
for n in z.namelist():
    p = D / 'A4_COMMISSIONING_RESULT' / n
    assert p.read_bytes() == z.read(n), n
    incoming[str(p)] = sha(z.read(n))
launch = z.read('approved-launch/A4_LAUNCH_PACKET.zip')
lr = json.loads((LD / 'DELIVERY_RECEIPT.json').read_text(encoding='utf-8-sig'))
assert launch == (LD / 'A4_LAUNCH_PACKET.zip').read_bytes()
assert sha(launch) == lr['zip_sha256'] and len(launch) == lr['zip_bytes'] and lr['authority_sha256'] == AUTH
for p in [LD / 'DELIVERY_RECEIPT.json', LD / 'COPY_VERIFICATION.json', LD / 'A4_LAUNCH_PACKET.zip']:
    incoming[str(p)] = sha(p.read_bytes())
lz = zipfile.ZipFile(io.BytesIO(launch))
lm = archive_check(lz)
assert len(lm['files']) == lr['payload_count'] == 89 and lm['authority_sha256'] == AUTH
canonical = z.read('evidence/APPROVED_BATCH.canonical.json')
assert sha(canonical) == AUTH and canonical == lz.read('AUTHORITY_OBJECT.canonical.json')
parent = json.loads(canonical)
assert parent['case_order'] == CASES and parent['p_commit'] == P and parent['apparatus_commit'] == CP
assert AUTH in z.read('evidence/AUTHORIZATION_SOURCE.txt').decode()
assert lz.read('references/A3_COMMISSIONING_RESULT.zip') == (WB / A3B / 'A3_COMMISSIONING_RESULT.zip').read_bytes()
assert lz.read('references/CONTACT_INTERRUPTION_NOTE.md') == (WB / A3B / RR / 'CONTACT_INTERRUPTION_NOTE.md').read_bytes()
assert z.read('evidence/ORIGINAL_FILES_BEFORE.json') == z.read('evidence/ORIGINAL_FILES_AFTER.json')
assert z.read(RR + 'RAW_EVIDENCE_BEFORE_ANALYSIS.json') == z.read(RR + 'RAW_EVIDENCE_AFTER_ANALYSIS.json')
execution = json.loads(z.read('evidence/BATCH_EXECUTION_RESULT.json'))
analysis = json.loads(z.read(RR + 'ANALYSIS_RESULT.json'))
checks = json.loads(z.read(RR + 'ANALYSIS_CHECKS.json'))
assert execution['approved_batch_sha256'] == analysis['batch_authority_sha256'] == checks['batch_authority_sha256'] == AUTH
assert execution['apparatus_checkpoint'] == CP and execution['run_constructors_attempted'] == 3
assert execution['case_order'] == CASES and len(execution['completed_attempts']) == 3
assert execution['unattempted_cases'] == execution['attempted_without_completed_result'] == []
assert execution['failure'] is None and execution['batch_stop'] is None
assert execution['no_retry_no_resume_no_patch'] and execution['physical_replays'] == 0
assert analysis['errors'] == checks['errors'] == {} and checks['original_raw_files_unchanged']
assert analysis['new_simulation_steps'] == analysis['controller_command_computations'] == analysis['physical_replays'] == 0
for n, h in checks['analysis_sources'].items():
    assert sha(z.read(RR + n)) == h, n
case_hashes = {}
observations = {}
for index, (case, steps, arrival, expenditure, energy) in enumerate([
        ('A4-CROSS', 1600, '10.37', '0.028233662', '0.671766338'),
        ('A4-WAIT', 2800, '22.55', '0.046314133', '0.653685867'),
        ('A4-DETOUR', 3200, '23.43', '0.058767050', '0.641232950')]):
    obj_bytes = z.read(f'evidence/{case}/APPROVED_EXECUTION.canonical.json')
    assert obj_bytes == lz.read(f'cases/{case}/EXECUTION_OBJECT.canonical.json')
    assert json.loads(obj_bytes) == parent['cases'][index]['execution_object']
    assert parent['cases'][index]['case_id'] == case
    case_hashes[case] = sha(obj_bytes)
    ex = json.loads(z.read(f'evidence/{case}/EXECUTION_RESULT.json'))
    assert ex == execution['completed_attempts'][index]
    assert ex['execution_sha256'] == case_hashes[case] and ex['run_constructors_attempted'] == 1
    assert ex['native_index'] == steps and ex['receipt_status'] == 'administrative_cutoff' and ex['receipt_complete']
    assert ex['terminal_dimension'] is None and ex['receipt_cause'] is None and ex['no_retry_no_resume']
    assert z.read(f'evidence/{case}/APPROVED_INITIAL.snapshot.json.gz') == lz.read(f'cases/{case}/INITIAL.snapshot.json.gz')
    o = json.loads(z.read(RR + case + '/OBSERVATIONS.json'))
    observations[case] = o
    wc = o['whole_case']
    assert wc['native_steps'] == steps
    assert format(wc['travel_time_to_arrival'], '.2f') == arrival
    assert format(wc['expenditure'], '.9f') == expenditure
    assert format(wc['final_EI'][0], '.9f') == energy and wc['final_EI'][1] == 1
    assert wc['damage'] == wc['impact_damage'] == wc['sustained_stress_damage'] == wc['source_transfer'] == 0
    assert o['contacts']['certified_contact_event_count'] == o['contacts']['mover_contact_event_count'] == o['contacts']['all_impact_event_count'] == 0
    assert o['contacts']['mover_impact_impulse_sum'] == 0 and not o['outcome']['physical_nonviability']
    for section in ['RECORD_INTEGRITY', 'BOUNDARY_AND_DELIVERY', 'ACCOUNTING']:
        assert checks['case_checks'][case][section]['valid']
    assert checks['case_checks'][case]['RECORD_INTEGRITY']['case_execution_sha256'] == case_hashes[case]
wait = observations['A4-WAIT']['waiting']
assert wait['prescribed_seconds'] == wait['zero_command_supported_seconds'] == 12 and wait['stationary_wait_observed']

live = ['AGENTS.md', '00_RESEARCH_MAP.md', '01_WORKSPACE_STATUS.md', 'SOURCE_CATALOG.json', 'SOURCE_REGISTER.md']
before = {}
for n in live:
    data = (WB / n).read_bytes()
    before[n] = {'bytes': len(data), 'sha256': sha(data)}
    p = ROOT / 'BEFORE' / n
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
protected = {}
for folder in ['90_SOURCES', '20_CANDIDATES', '30_REVIEWS', '40_DECISIONS', '50_SESSIONS']:
    for p in (WB / folder).rglob('*'):
        if p.is_file(): protected[p.relative_to(WB).as_posix()] = sha(p.read_bytes())
catalog = json.loads((ROOT / 'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
old_count = len(catalog['source_files'])
assert old_count == 192
batch = ROOT / 'SOURCE_BATCH'
batch.mkdir(exist_ok=True)
(batch / Z.name).write_bytes(raw)
for n in ['DELIVERY_RECEIPT.json', 'COPY_VERIFICATION.json']:
    (batch / n).write_bytes((D / n).read_bytes())
for n in z.namelist():
    p = batch / n
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(z.read(n))
for n in ['DELIVERY_RECEIPT.json', 'COPY_VERIFICATION.json']:
    (batch / 'approved-launch' / n).write_bytes((LD / n).read_bytes())
selected = [Z.name, 'DELIVERY_RECEIPT.json', 'COPY_VERIFICATION.json', 'README.md', 'FILE_MANIFEST.json',
    'evidence/AUTHORIZATION_SOURCE.txt', 'evidence/APPROVED_BATCH.canonical.json', 'evidence/BATCH_ATTEMPT.json', 'evidence/BATCH_EXECUTION_RESULT.json']
selected += [RR + n for n in ['A4_PLAIN_LANGUAGE_RESULT.md', 'A4_COMMISSIONING_REPORT.md', 'A4_RESULT_SUMMARY.json',
    'ANALYSIS_RESULT.json', 'ANALYSIS_CHECKS.json', 'RAW_EVIDENCE_BEFORE_ANALYSIS.json', 'RAW_EVIDENCE_AFTER_ANALYSIS.json']]
for case in CASES:
    selected += [f'evidence/{case}/APPROVED_EXECUTION.canonical.json', f'evidence/{case}/APPROVAL_REQUEST.json',
        f'evidence/{case}/EXECUTION_RESULT.json', RR + case + '/OBSERVATIONS.json', RR + case + '/RECORD_INTEGRITY.json']
selected += ['PRESERVATION_CHECK.json', 'RESOURCE_RESULT.json', 'approved-launch/A4_LAUNCH_PACKET.zip',
    'approved-launch/DELIVERY_RECEIPT.json', 'approved-launch/COPY_VERIFICATION.json']
entries = []
for number, n in enumerate(selected, old_count + 1):
    data = (batch / n).read_bytes()
    member = n in z.namelist()
    origin = str(Z) + '::' + n if member else str(LD / PurePosixPath(n).name) if n.startswith('approved-launch/') else str(D / n)
    entries.append({'source_id': f'SRC-{number:03d}', 'path': B + '/' + n, 'original_filename': PurePosixPath(n).name,
        'bytes': len(data), 'sha256': sha(data), 'role': 'observed-commissioning-evidence' if n.startswith('evidence/') else 'commissioning-package-custody-and-authority-history',
        'prepared': '2026-09-26', 'registered': '2026-09-26', 'stated_author': 'Supplied A4 batch execution/read-only result package; exact assistant model/backend not stated',
        'acquired_from': origin, 'archive_member': n if member else None,
        'authority': 'Jason requests intake of the already-authorized three-case A4 batch; no further execution or changes',
        'source_execution_authority_sha256': AUTH, 'p_baseline_checkpoint': P, 'reviewed_checkpoint': CP,
        'review_note': R, 'record': S + '/INTAKE_RECORD.md', 'continues': A3R,
        'notes': 'OBSERVED COMMISSIONING EVIDENCE. Complete result ZIP and all 122 members preserved. CROSS/WAIT/DETOUR remain distinct predetermined cases, one attempt each. WAIT counterfactual unexecuted; DETOUR not equal-endpoint comparison; efficacy UNTESTED.'})
catalog['source_files'] += entries
catalog['intake_events'].append({'session_id': ID, 'source_ids': [e['source_id'] for e in entries],
    'review_note': R, 'record': S + '/INTAKE_RECORD.md', 'continues': A3R,
    'scope': 'A4 OBSERVED COMMISSIONING EVIDENCE: three predetermined cases once each, original ceilings retained, bounded claims and comparison limits preserved; efficacy UNTESTED'})
dump(ROOT / 'AFTER/SOURCE_CATALOG.json', catalog)

def src(n, label): return f'[{label}](../../{B}/{n})'

status = '''P engineering: **VERIFIED**  
Commissioning apparatus: **FIT / pre-run engineering CLOSED**  
Coupling commissioning: **IN PROGRESS**  
Scientific/developmental efficacy: **UNTESTED**

| Commissioning item | Current status |
|---|---|
| V1 | COMPLETE |
| V2 | COMPLETE |
| V3 | COMPLETE |
| A0 | COMPLETE |
| A1 | OBSERVED |
| A2 | OBSERVED |
| A3 | OBSERVED |
| A4 | OBSERVED |
| A5 | NOT EXECUTED |
| B1–B4 | NOT EXECUTED |
| C1/C2 | NOT EXECUTED |'''
claim = 'Three predetermined externally controlled witnesses demonstrated physically realizable timed crossing, wait-then-cross and always-clear detour opportunities for the actual finite body under the unchanged mover and body/world laws.'
record = f'''# A4 — observed coupling-commissioning evidence

**Registered:** 2026-09-26. **Disposition: OBSERVED COMMISSIONING EVIDENCE.** This records the already-authorized A4 batch: A4-CROSS, A4-WAIT and A4-DETOUR, executed in that fixed order exactly once each. No new run or scientific experiment number is created.

{status}

## Authority, sources and continuity

Executed canonical batch authority: `{AUTH}`. The {src('evidence/APPROVED_BATCH.canonical.json', 'approved canonical batch object')} and {src('evidence/AUTHORIZATION_SOURCE.txt', 'genuine authorization source')} bind the three separate constituent cases. P remains `{P}`; apparatus remains `{CP}`.

Primary sources: {src('A4_COMMISSIONING_RESULT.zip', 'complete verified result package')} · {src(RR + 'A4_PLAIN_LANGUAGE_RESULT.md', 'A4_PLAIN_LANGUAGE_RESULT.md')} · {src(RR + 'A4_COMMISSIONING_REPORT.md', 'A4_COMMISSIONING_REPORT.md')} · {src(RR + 'A4_RESULT_SUMMARY.json', 'full result summary')}. This continues the [A3 evidence record and commissioning history](../../{A3R}).

| Case | Exact constituent execution SHA-256 | Saved evidence |
|---|---|---|
| A4-CROSS | `{case_hashes['A4-CROSS']}` | {src('evidence/A4-CROSS/APPROVED_EXECUTION.canonical.json', 'object')} · {src('evidence/A4-CROSS/EXECUTION_RESULT.json', 'execution')} · {src(RR + 'A4-CROSS/OBSERVATIONS.json', 'observations')} |
| A4-WAIT | `{case_hashes['A4-WAIT']}` | {src('evidence/A4-WAIT/APPROVED_EXECUTION.canonical.json', 'object')} · {src('evidence/A4-WAIT/EXECUTION_RESULT.json', 'execution')} · {src(RR + 'A4-WAIT/OBSERVATIONS.json', 'observations')} |
| A4-DETOUR | `{case_hashes['A4-DETOUR']}` | {src('evidence/A4-DETOUR/APPROVED_EXECUTION.canonical.json', 'object')} · {src('evidence/A4-DETOUR/EXECUTION_RESULT.json', 'execution')} · {src(RR + 'A4-DETOUR/OBSERVATIONS.json', 'observations')} |

The unchanged apparatus remains single-case; the parent approval and its exact constituent envelopes document the batch workflow. Historical proposed/unauthorized labels inside the {src('approved-launch/A4_LAUNCH_PACKET.zip', 'original launch packet')} remain unchanged and distinct from the later actual grant. Each case used its own prescribed manufactured healthy initial fixture, E = 0.7 / I = 1.0; these are independent witnesses, not one continued trajectory or sampled newborn lives. P was inactive.

## Observed cases

| Case | Prescription | Destination arrival | Whole-case expenditure | Final E / I | Mover contacts |
|---|---|---|---|---|---|
| A4-CROSS | Predetermined timed crossing | 10.37 s | 0.028233662 | 0.671766338 / 1.0 | 0 |
| A4-WAIT | Fixed zero-command wait for 12 s, then cross | 22.55 s | 0.046314133 | 0.653685867 / 1.0 | 0 |
| A4-DETOUR | Predetermined A0 left bypass | 23.43 s | 0.058767050 | 0.641232950 / 1.0 | 0 |

A4-WAIT entered the mover's vertical collision band at **13.25 s** and fully exited at **18.96 s**. The 12 s zero-command wait was recorded, with zero waiting displacement. Waiting expenditure was 0.018; post-wait/moving expenditure was 0.0283141333927. The wait/release came from the fixed prescription, not a sensor-derived or learned choice.

Arrival is the predeclared 0.25 m destination-radius milestone, using the first matching native sample and its preceding sample. Entry uses body-centre y >= 9, and full exit y > 11 for CROSS/WAIT. These are sampled milestones, not exact interpolated crossing times or collision events. DETOUR's corresponding y markers are side-passage markers outside the mover region.

The expenditure and final-reserve columns cover each complete case through its prescribed cutoff, **not only travel to first arrival**. The ceilings remained:

| Case | Prescribed cutoff | Recorded native steps | Recorded stop |
|---|---|---|---|
| A4-CROSS | 16 s | 1,600 | Complete administrative cutoff |
| A4-WAIT | 28 s | 2,800 | Complete administrative cutoff |
| A4-DETOUR | 32 s | 3,200 | Complete administrative cutoff |

The batch therefore retains all 7,600 native steps and 76 prescribed simulated seconds across separate cases. No unused duration or budget was transferred. No case was unattempted or left without a completed result; the source records no execution failure.

Across all three cases, the preserved observations are **no mover collision, no collision impulse, no damage and no bodily nonviability**. The full contact records contain no collider contacts or impact events; no source transfer or repair occurred. There was no retry, substitution, tuning, continuation, patch, phase/route change or extra case. Original raw evidence, saved command streams, contacts, sampled mover geometry and restart states remain preserved.

## Strongest bounded claim and retained limits

> {claim}

- **A4-WAIT does not experimentally establish that immediate proceeding would have collided.** That conflict remains the predeclared analytic argument. No immediate-proceed counterfactual trajectory was executed.
- **DETOUR has independent endpoints and is not an equal-endpoint efficiency comparison.** Its A0 bypass runs from (1.5,6) to (1.5,14), whereas CROSS runs from (10,8.8) to (10,12), and WAIT from (6,8.8) to (6,12). Costs and arrival times do not establish optimality or route ranking under equal endpoints.
- **No all-phase safety claim.** The always-clear corridor refers to the accepted A0 geometric opportunity; this batch witnesses its physical realization under the recorded conditions. Sampled clearance minima are not continuous-time convergence or safety proofs for every phase, start, reserve or controller.
- **No P perception, prediction, discovery or learning claim.** The privileged external controller supplied the actions while P was inactive. No P regulation, scientific/developmental efficacy or broad survival capability is established.

Derived native-time mover geometry is distinguished in the source from actual controller-sampled rectangles and velocities. Contact absence is retained from the contact/event records, not inferred merely from positive sampled gaps. No new geometry analysis, ray tracing or replay was performed during intake. Scientific/developmental efficacy remains **UNTESTED**.

## Saved checks and intake validation

The {src('evidence/BATCH_EXECUTION_RESULT.json', 'batch execution result')} records three construction attempts in the declared order, one per case, no failed/incomplete/unattempted case, no retry/resume/patch and zero physical replays. The {src(RR + 'ANALYSIS_RESULT.json', 'read-only analysis result')} and {src(RR + 'ANALYSIS_CHECKS.json', 'complete check summary')} report record/authority integrity, boundary/delivery and accounting checks passed for each case, no analysis errors and all 73 original raw/evidence files byte-identical before/after analysis. They report zero new simulation steps, controller-command recomputations or physical replays.

Saved sensor/native counts are 1,601/1,600, 2,801/2,800 and 3,201/3,200 respectively, with a separately validated initial envelope for each case. Controller counts are 160, 280 and 320. Inactive neural state and saved RNG checks retain the source's recorded-state scope; neural wave rows are zero. Production `verify_segment` was not invoked because it recomputes commands even with `replay=False`. These are the supplied saved-data checks, not a production-verifier rerun or independent scientific validation by this intake.

Intake independently verified the result ZIP against its delivery and copy receipts; all **121 payload hashes/CRCs** and **122 unpacked members** match. The embedded launch ZIP matches its separate delivery, with all **89 launch payload hashes/CRCs** verified. The canonical parent bytes hash to the exact executed authority and match the launch object. All three constituent objects and approved initial snapshots match their bound launch originals; execution hashes and reported attempts match the respective case records. The embedded prior A3 ZIP/contact note match the already-registered originals. Original-file and raw-analysis before/after manifests are byte-identical; analysis-source hashes match their packaged files. Requested rounded results match the saved observation values.

These are custody and registration checks. No supplied script, scientific checker, controller, simulation, viewer, test suite or actual Loom repository was run or modified. No necessary source gap or source-identity contradiction was found. The current user instruction authorizes this intake/status update only; no new mechanism, numerical setting, Base World configuration, canon or sequence decision is adopted.

[Source identities](SOURCE_IDENTITIES.json) · [Intake completion](INTAKE_RECORD.md) · [Final validation](VALIDATION.json).
'''
write(ROOT / 'NEW' / R, record)
nav = f'''## Current coupling commissioning — A4 observed, 2026-09-26

{status}

**A4: OBSERVED COMMISSIONING EVIDENCE.** Executed batch authority `{AUTH}`; P `{P}`; apparatus `{CP}`. A4-CROSS, A4-WAIT and A4-DETOUR each executed exactly once, retaining the prescribed 16/28/32 s ceilings. No mover collision, collision impulse, damage or bodily nonviability was observed; no retry/substitution/tuning/continuation occurred.

> {claim}

[A4 evidence and case results]({R}) · [Plain-language result]({B}/{RR}A4_PLAIN_LANGUAGE_RESULT.md) · [Technical report]({B}/{RR}A4_COMMISSIONING_REPORT.md) · [Complete verified package]({B}/A4_COMMISSIONING_RESULT.zip) · [Previous A3 evidence]({A3R}).

WAIT's immediate-proceed conflict remains a predeclared analytic argument, not an executed counterfactual. DETOUR uses independent endpoints and is not an equal-endpoint efficiency comparison. No all-phase safety or P perception/prediction/discovery/learning claim is made. This intake changes no canon, mechanism, Base World configuration, numerical setting or commissioning sequence, initiates no execution and creates no scientific experiment number. Earlier sections retain their dated historical dispositions.

'''
for name in ['00_RESEARCH_MAP.md', '01_WORKSPACE_STATUS.md']:
    text = (ROOT / 'BEFORE' / name).read_text(encoding='utf-8-sig')
    first, rest = text.split('\n', 1)
    heading = '## Current coupling commissioning — A3 observed, 2026-09-26'
    assert heading in rest
    rest = rest.replace(heading, '## Preserved A3 intake — 2026-09-26', 1)
    if name == '00_RESEARCH_MAP.md':
        old = 'selected for specification; exact external A1, A2 and A3 packages authorized | coupling commissioning in progress; V1/V2/V3/A0 complete | A1/A2/A3 observed external-control witnesses; learning/developmental efficacy untested'
        assert old in rest
        rest = rest.replace(old, 'selected for specification; exact external A1–A4 packages authorized | coupling commissioning in progress; V1/V2/V3/A0 complete | A1–A4 observed external-control witnesses; learning/developmental efficacy untested', 1)
    write(ROOT / 'AFTER' / name, first + '\n\n' + nav + rest.lstrip('\n'))
text = (ROOT / 'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig')
first, rest = text.split('\n', 1)
heading = '## Current commissioning evidence — A3 observed, 2026-09-26'
assert heading in rest
rest = rest.replace(heading, '## Preserved A3 commissioning evidence — 2026-09-26', 1)
continuation = f'''## Current commissioning evidence — A4 observed, 2026-09-26

The [registered A4 batch]({R}) is **OBSERVED COMMISSIONING EVIDENCE** under executed authority `{AUTH}`: A4-CROSS, A4-WAIT and A4-DETOUR once each, with their prescribed 16/28/32 s ceilings retained. P engineering **VERIFIED**; apparatus **FIT / pre-run engineering CLOSED**; coupling commissioning **IN PROGRESS**; scientific/developmental efficacy **UNTESTED**. V1/V2/V3/A0 COMPLETE; A1/A2/A3/A4 OBSERVED; A5, B1–B4 and C1/C2 NOT EXECUTED.

Preserve the three independent external physical witnesses, no mover collision/impulse/damage/nonviability, and no retry/substitution/tuning/continuation. WAIT has no executed immediate-proceed comparator; its conflict is the predeclared analytic argument. DETOUR retains independent A0 endpoints, not an equal-endpoint efficiency comparison. No all-phase safety or P perception/prediction/discovery/learning claim follows. This intake grants no extra execution, experiment number, canon/mechanism/Base World/numerical-setting/sequence change or Git operation. Earlier evidence and checkpoint statuses remain distinct history, including the exact 05abf604 apparatus hold; the commissioning design is not marked failed.

'''
write(ROOT / 'AFTER/AGENTS.md', first + '\n\n' + continuation + rest.lstrip('\n'))
register = (ROOT / 'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
register += '\n## A4 observed coupling-commissioning batch — 2026-09-26\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:
    register += f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
register += f'\n[A4 evidence record]({R}). Batch authority `{AUTH}`; three distinct predetermined cases executed once each. Complete original result package preserved; all other payload identities remain in the manifest. WAIT counterfactual and DETOUR comparison limits retained; efficacy UNTESTED.\n'
write(ROOT / 'AFTER/SOURCE_REGISTER.md', register)
verification = {'incoming_zip': str(Z), 'zip_bytes': len(raw), 'zip_sha256': sha(raw),
    'manifest_payloads_verified': len(mf['files']), 'archive_members': len(z.namelist()), 'crc_passed': True,
    'all_unpacked_inbox_members_match_zip': True, 'both_result_delivery_receipts_match': True,
    'launch_payloads_verified': len(lm['files']), 'launch_crc_passed': True, 'launch_zip_sha256': sha(launch),
    'launch_matches_separate_delivery': True, 'approved_canonical_sha256': sha(canonical), 'approved_canonical_matches_launch': True,
    'constituent_execution_sha256': case_hashes, 'all_constituents_and_initial_snapshots_match_bound_launch': True,
    'embedded_A3_zip_and_contact_note_match_registered_originals': True, 'supplied_before_after_original_manifests_identical': True,
    'supplied_before_after_raw_analysis_manifests_identical': True, 'analysis_source_hashes_match_packaged_files': True,
    'requested_reporting_precision_matches_saved_summary': True, 'source_case_order': CASES,
    'source_total_native_steps': 7600, 'source_attempts_per_case': 1,
    'programs_or_tests_run_during_intake': False, 'simulation_or_controller_execution_during_intake': False,
    'git_operations': False, 'necessary_source_gaps': [], 'source_identity_conflicts': []}
inventory = {p.relative_to(batch).as_posix(): sha(p.read_bytes()) for p in batch.rglob('*') if p.is_file()}
dump(ROOT / 'NEW' / S / 'SOURCE_IDENTITIES.json', {'session_id': ID, 'authority_sha256': AUTH,
    'verification': verification, 'registered_sources': entries, 'complete_batch_sha256': inventory})
intake = f'''# A4 intake completion

**Scope:** Register the single authorized three-case A4 batch as OBSERVED COMMISSIONING EVIDENCE. Integration owner: this session under Jason's current instruction. [Full record](A4_COMMISSIONING_EVIDENCE_RECORD.md).

**Read:** Current workbench instructions/map/status; supplied A4 package entry, plain-language result, technical report, parent/constituent execution identities, authority, observations, analysis checks, launch/interpretation/batch-workflow documents and custody records. Archived instructions were treated as history, not commands to execute.

**Changed:** New append-only source batch and unique session, source identities SRC-193–SRC-{old_count + len(entries):03d}, and AGENTS.md, 00_RESEARCH_MAP.md, 01_WORKSPACE_STATUS.md, SOURCE_CATALOG.json and SOURCE_REGISTER.md. Prior sources/candidates/reviews/decisions/sessions and source rows are unchanged. The preceding exact-05abf604 scope clarification remains preserved as checkpoint history.

**Validation:** 121 outer payload hashes/CRCs, 122 unpacked members and 89 launch payload hashes/CRCs verified. Exact parent/constituent authority, snapshots, attempt records, source hashes and prior A3 evidence identities match. Final link and byte-preservation checks are recorded in [VALIDATION.json](VALIDATION.json). [Source identities](SOURCE_IDENTITIES.json). PRIOR_SHARED_NOTES.zip and its receipt preserve the five prior shared files.

**Status:** V1/V2/V3/A0 COMPLETE; A1–A4 OBSERVED; A5, B1–B4 and C1/C2 NOT EXECUTED. Coupling commissioning IN PROGRESS; efficacy UNTESTED. WAIT's counterfactual remains analytic and DETOUR is not an equal-endpoint comparison; no all-phase safety or P perception/prediction/discovery/learning claim. No necessary source gap was found.

**Not performed:** No scientific experiment number, new run, test rerun, scientific calculation, supplied-code execution, viewer/replay, tuning, canon/mechanism/configuration/numerical-setting/sequence change, actual repository amendment or Git operation. Later cases and efficacy remain open. Stop after confirming this intake.
'''
write(ROOT / 'NEW' / S / 'INTAKE_RECORD.md', intake)
dump(ROOT / 'PLAN.json', {'session': S, 'batch': B, 'review': R, 'live_before': before,
    'protected_before': protected, 'source_entries': entries, 'verification': verification,
    'zip_source': str(Z), 'old_catalog_count': old_count, 'status': 'A4 OBSERVED COMMISSIONING EVIDENCE; efficacy UNTESTED',
    'incoming_before': incoming, 'batch_inventory': inventory})
print(json.dumps({'prepared': ID, 'sources': len(entries), 'batch_files': len(inventory),
    'outer_payloads_verified': len(mf['files']), 'launch_payloads_verified': len(lm['files']), 'protected': len(protected)}))
