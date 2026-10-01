"""Documentation-only A3 intake. No archived programs or scientific checks are executed."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib, io, json, zipfile

ROOT = Path(__file__).resolve().parent
WB = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ID = '2026-09-26-a3-evidence-intake-7c42a9d1'
S = '50_SESSIONS/' + ID
B = '90_SOURCES/p_a3_commissioning_2026-09-26_7c42a9d1'
R = S + '/A3_COMMISSIONING_EVIDENCE_RECORD.md'
D = WB / 'INBOX/2026-09-26-A3-commissioning-result-5f077481'
LD = WB / 'INBOX/2026-09-25-A3-launch-packet-5f077481'
Z = D / 'A3_COMMISSIONING_RESULT.zip'
AUTH = '43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd'
P = '6bc9683b54e4fa80136fe8534d7713e2a250a95f'
CP = '5f07748102cb5eaa302569c87efbae095050e9fe'
A2R = '50_SESSIONS/2026-09-25-a2-evidence-intake-b671e309/A2_COMMISSIONING_EVIDENCE_RECORD.md'
A2B = '90_SOURCES/p_a2_commissioning_2026-09-25_b671e309'
RR = 'evidence/read-only-review/'
sha = lambda b: hashlib.sha256(b).hexdigest()

def write(p, text):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8', newline='\n')

def dump(p, value):
    write(p, json.dumps(value, indent=2, ensure_ascii=False) + '\n')

def archive_check(z, prefix=''):
    names = z.namelist()
    assert len(names) == len(set(names)) == len({n.casefold() for n in names})
    for n in names:
        p = PurePosixPath(n)
        assert not p.is_absolute() and '..' not in p.parts and ':' not in n and '\\' not in n
    m = json.loads(z.read(prefix + 'FILE_MANIFEST.json'))
    assert {prefix + n for n in m['files']} == set(names) - {prefix + 'FILE_MANIFEST.json'}
    for n, meta in m['files'].items():
        data = z.read(prefix + n)
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
assert mf['authority_sha256'] == AUTH
assert len(mf['files']) == receipt['verified_payloads'] == copy_receipt['verified_payloads'] == 70
incoming = {str(Z): sha(raw)}
for name in ['DELIVERY_RECEIPT.json', 'COPY_VERIFICATION.json']:
    incoming[str(D / name)] = sha((D / name).read_bytes())
for n in z.namelist():
    p = D / 'A3_COMMISSIONING_RESULT' / n
    assert p.read_bytes() == z.read(n), n
    incoming[str(p)] = sha(z.read(n))

launch = z.read('approved-launch/A3_LAUNCH_PACKET.zip')
lr = json.loads((LD / 'DELIVERY_RECEIPT.json').read_text(encoding='utf-8-sig'))
assert launch == (LD / 'A3_LAUNCH_PACKET.zip').read_bytes()
assert sha(launch) == lr['sha256'] and len(launch) == lr['bytes'] and lr['authority_sha256'] == AUTH
for p in [LD / 'DELIVERY_RECEIPT.json', LD / 'A3_LAUNCH_PACKET.zip']:
    incoming[str(p)] = sha(p.read_bytes())
lz = zipfile.ZipFile(io.BytesIO(launch))
lm = archive_check(lz, 'A3_LAUNCH_PACKET/')
assert len(lm['files']) == lr['zip_validation']['payloads'] == 86 and lm['authority_sha256'] == AUTH
canonical = z.read('evidence/APPROVED_OBJECT.canonical.json')
assert sha(canonical) == AUTH
assert canonical == lz.read('A3_LAUNCH_PACKET/AUTHORITY_OBJECT.canonical.json')
assert AUTH in z.read('evidence/AUTHORIZATION_SOURCE.txt').decode()
assert lz.read('A3_LAUNCH_PACKET/references/A2_COMMISSIONING_RESULT.zip') == (WB / A2B / 'A2_COMMISSIONING_RESULT.zip').read_bytes()
assert lz.read('A3_LAUNCH_PACKET/references/TIMING_REPORTING_NOTE.json') == (WB / A2B / RR / 'TIMING_REPORTING_NOTE.json').read_bytes()
assert z.read('evidence/APPROVED_INITIAL_A3.snapshot.json.gz') == lz.read('A3_LAUNCH_PACKET/INITIAL_A3.snapshot.json.gz')
assert z.read('evidence/ORIGINAL_FILES_BEFORE.json') == z.read('evidence/ORIGINAL_FILES_AFTER.json')
assert z.read(RR + 'RAW_EVIDENCE_BEFORE_ANALYSIS.json') == z.read(RR + 'RAW_EVIDENCE_AFTER_ANALYSIS.json')
execution = json.loads(z.read('evidence/EXECUTION_RESULT.json'))
analysis = json.loads(z.read(RR + 'ANALYSIS_RESULT.json'))
integrity = json.loads(z.read(RR + 'RECORD_INTEGRITY.json'))
contact = json.loads(z.read(RR + 'CONTACT_INTERRUPTION_OBSERVATIONS.json'))
summary = json.loads(z.read(RR + 'A3_RESULT_SUMMARY.json'))
assert execution['approved_execution_sha256'] == analysis['authority_sha256'] == integrity['authority_sha256'] == AUTH
assert execution['apparatus_checkpoint'] == CP and execution['native_index'] == 21000
assert execution['run_constructors_attempted'] == 1 and execution['no_retry_no_resume_no_patch']
assert execution['failure'] is None and execution['terminal_dimension'] is None and execution['physical_replays'] == 0
assert integrity['complete'] and integrity['valid'] and integrity['status'] == 'administrative_cutoff'
assert analysis['errors'] == {} and analysis['original_raw_files_unchanged']
assert analysis['new_simulation_steps'] == analysis['controller_command_computations'] == analysis['physical_replays'] == 0
for n, h in analysis['analysis_sources'].items():
    assert sha(z.read(RR + n)) == h, n
assert contact['source3_supported_intervals'] == contact['source3_impacts'] == 629
assert contact['source3_gaps_count'] == 628 and contact['source3_sustained_stress_damage'] == 0
assert contact['raw_and_existing_analysis_hashes_unchanged'] and contact['new_world_steps'] == contact['controller_recomputation'] == 0
# Compare the requested reporting precision to the supplied saved summary only.
milestones = summary['milestones']
for key, val in [('post_damage', '6.812'), ('first_eligible_repair', '80.710'),
                 ('first_positive_restoration', '80.710'), ('energy_arrival_after_repair_departure', '184.367')]:
    assert format(milestones[key]['time'], '.3f') == val, key
assert format(milestones['repair_departure']['time'], '.0f') == '155'
wc = summary['whole_case']
assert wc['complete_ordered_recovery_witness_observed'] and wc['damage'] > wc['repair']
assert format(wc['repair'], '.8f') == '0.00317209'
assert format(summary['source3_transfer'], '.6f') == '0.152191'
assert [format(x, '.6f') for x in wc['final_EI']] == ['0.494237', '0.989740']

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
        if p.is_file():
            protected[p.relative_to(WB).as_posix()] = sha(p.read_bytes())
catalog = json.loads((ROOT / 'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
old_count = len(catalog['source_files'])
assert old_count == 163
batch = ROOT / 'SOURCE_BATCH'
batch.mkdir(exist_ok=True)
(batch / Z.name).write_bytes(raw)
for n in ['DELIVERY_RECEIPT.json', 'COPY_VERIFICATION.json']:
    (batch / n).write_bytes((D / n).read_bytes())
for n in z.namelist():
    p = batch / n
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(z.read(n))
for n in ['A3_LAUNCH_PACKET.md', 'AUTHORITY_OBJECT.canonical.json', 'FILE_MANIFEST.json']:
    p = batch / 'approved-launch/A3_LAUNCH_PACKET' / n
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(lz.read('A3_LAUNCH_PACKET/' + n))
(batch / 'approved-launch/DELIVERY_RECEIPT.json').write_bytes((LD / 'DELIVERY_RECEIPT.json').read_bytes())
selected = [Z.name, 'DELIVERY_RECEIPT.json', 'COPY_VERIFICATION.json', 'README.md', 'FILE_MANIFEST.json',
    'evidence/AUTHORIZATION_SOURCE.txt', 'evidence/APPROVED_OBJECT.canonical.json', 'evidence/APPROVAL_REQUEST.json',
    'evidence/EXECUTION_RESULT.json', 'evidence/LAUNCHED_MANIFEST.json']
selected += [RR + n for n in ['A3_PLAIN_LANGUAGE_RESULT.md', 'CONTACT_INTERRUPTION_NOTE.md', 'A3_COMMISSIONING_REPORT.md',
    'A3_RESULT_SUMMARY.json', 'A3_OBSERVATIONS.json', 'CONTACT_INTERRUPTION_OBSERVATIONS.json', 'REPAIR_EVENT_LEDGER.json',
    'RECORD_INTEGRITY.json', 'BOUNDARY_AND_DELIVERY.json', 'ACCOUNTING.json', 'ALL_FIXED_WINDOWS.json', 'ANALYSIS_RESULT.json',
    'RAW_EVIDENCE_BEFORE_ANALYSIS.json', 'RAW_EVIDENCE_AFTER_ANALYSIS.json']]
selected += ['PRESERVATION_CHECK.json', 'RESOURCE_RESULT.json', 'approved-launch/A3_LAUNCH_PACKET.zip',
    'approved-launch/A3_LAUNCH_PACKET/A3_LAUNCH_PACKET.md', 'approved-launch/DELIVERY_RECEIPT.json']
entries = []
for number, n in enumerate(selected, old_count + 1):
    data = (batch / n).read_bytes()
    member = n in z.namelist()
    if member:
        origin = str(Z) + '::' + n
    elif n.startswith('approved-launch/A3_LAUNCH_PACKET/'):
        origin = str(LD / 'A3_LAUNCH_PACKET.zip') + '::A3_LAUNCH_PACKET/' + PurePosixPath(n).name
    elif n == 'approved-launch/DELIVERY_RECEIPT.json':
        origin = str(LD / 'DELIVERY_RECEIPT.json')
    else:
        origin = str(D / n)
    entries.append({'source_id': f'SRC-{number:03d}', 'path': B + '/' + n,
        'original_filename': PurePosixPath(n).name, 'bytes': len(data), 'sha256': sha(data),
        'role': 'observed-commissioning-evidence' if n.startswith('evidence/') else 'commissioning-package-custody-and-authority-history',
        'prepared': '2026-09-25' if n.startswith('approved-launch/') else '2026-09-26',
        'registered': '2026-09-26', 'stated_author': 'Supplied A3 execution/read-only result package; exact assistant model/backend not stated',
        'acquired_from': origin, 'archive_member': n if member else None,
        'authority': 'Jason requests intake of the single already-authorized A3 result; no further execution or mechanism/configuration change',
        'source_execution_authority_sha256': AUTH, 'p_baseline_checkpoint': P, 'reviewed_checkpoint': CP,
        'review_note': R, 'record': S + '/INTAKE_RECORD.md', 'continues': A2R,
        'notes': 'OBSERVED COMMISSIONING EVIDENCE. Original result ZIP and all 71 members preserved byte-for-byte, including contact-interruption findings. Launch proposal history remains separate from the later executed grant. Efficacy UNTESTED.'})
catalog['source_files'] += entries
catalog['intake_events'].append({'session_id': ID, 'source_ids': [e['source_id'] for e in entries],
    'review_note': R, 'record': S + '/INTAKE_RECORD.md', 'continues': A2R,
    'scope': 'Single authorized A3 OBSERVED COMMISSIONING EVIDENCE; 21000 native steps / 210 s cutoff; contact interruptions and repeated damage retained; efficacy UNTESTED'})
dump(ROOT / 'AFTER/SOURCE_CATALOG.json', catalog)

def src(n, label):
    return f'[{label}](../../{B}/{n})'

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
| A4/A5 | NOT EXECUTED |
| B1–B4 | NOT EXECUTED |
| C1/C2 | NOT EXECUTED |'''
claim = 'One externally controlled physical witness demonstrated an uninterrupted world history containing actual nonterminal damage, repair-eligible contact, positive integrity restoration, departure from repair, subsequent travel, and productive energy-source contact under the unchanged body/world laws.'
withheld = 'general recovery capability; P discovery or perception; P learning/regulation; autonomous repair-seeking; survival capability; optimal repair duration; adequacy of repair rate; adequacy of damage/contact parameters'
record = f'''# A3 — observed coupling-commissioning evidence

**Registered:** 2026-09-26. **Disposition: OBSERVED COMMISSIONING EVIDENCE.** This intake registers one already-executed, authorized A3 physical witness. It initiates no run and assigns no scientific experiment number.

{status}

## Sources, authority and continuity

- Executed A3 authority: `{AUTH}` — {src('evidence/APPROVED_OBJECT.canonical.json', 'approved canonical object')} and {src('evidence/AUTHORIZATION_SOURCE.txt', 'exact authorization')}.
- P checkpoint: `{P}`; apparatus checkpoint: `{CP}`.
- Primary evidence: {src('A3_COMMISSIONING_RESULT.zip', 'complete A3 result package')}, {src(RR + 'A3_PLAIN_LANGUAGE_RESULT.md', 'A3_PLAIN_LANGUAGE_RESULT.md')}, {src(RR + 'CONTACT_INTERRUPTION_NOTE.md', 'CONTACT_INTERRUPTION_NOTE.md')} and {src(RR + 'A3_COMMISSIONING_REPORT.md', 'A3_COMMISSIONING_REPORT.md')}.
- Full precision and underlying observations: {src(RR + 'A3_RESULT_SUMMARY.json', 'result summary')}, {src(RR + 'A3_OBSERVATIONS.json', 'A3 observations')}, {src(RR + 'CONTACT_INTERRUPTION_OBSERVATIONS.json', 'contact-interruption observations')} and {src(RR + 'REPAIR_EVENT_LEDGER.json', 'repair event ledger')}.
- Previous live record: [A2 evidence and commissioning history](../../{A2R}). All earlier A1/V3/viewer/A2 and engineering-checkpoint records remain unchanged.

The {src('approved-launch/A3_LAUNCH_PACKET/A3_LAUNCH_PACKET.md', 'original launch packet')} retains its historical proposed/unauthorized labels. The later exact grant authorized one case with report-don't-patch and no retry, extension, route substitution, tuning, continuation or additional case without separate authorization. This intake registers that completed execution; it does not renew the grant.

A3 began from its approved manufactured healthy zero-time fixture, E = 0.7 and I = 1. It is not a continuation of A2's final state or a sampled newborn. The body/world history within A3 continued through the encounters without mid-case reset. P was inactive and the existing external controller supplied fixed-deadline stages; the departure time was not a learned repair decision. The earlier launch preparation/history and previous A2 reporting limitations remain immutable source history.

## Observed ordered chain

| Milestone | Recorded observation |
|---|---|
| Actual nonterminal wall damage | 6.812 s |
| Repair-eligible contact and first positive restoration | Recorded event endpoint 80.710 s |
| Total positive restoration | 0.00317209 |
| Actual departure from repair | 155 s |
| Source-3 contact after travel | 184.367 s |
| Total source-3 transfer | 0.152191 |
| Prescribed administrative stop | 210 s / 21,000 native steps |
| Final E | 0.494237 |
| Final I | 0.989740 |
| Terminal crossing | None |
| Execution error | None |

The exact source times are 6.81222039642792 s for first damage, 80.71000000000438 s for the first eligible-restoration event endpoint, 155.000000000004 s for the actual repair-release event, and 184.36673898957898 s for source-3 arrival. Repair arrival itself occurred earlier, at 80.70607911202922 s, and caused additional impact damage before positive restoration. The before/after contact-event reserve values remain distinct in the original summary; they are not interpolated or reset.

Recorded gross restoration was 0.0031720941779426223. Source-3 transfer was 0.1521907717217202. Final reserves were E = 0.4942366785576829 and I = 0.9897395396030849. The recorded clock endpoint was 209.99999999995399 s; all 21,000 prescribed native steps and 1,050 complete fixed windows are present. The supplied result reports no unobserved tail beyond its existing event-time tolerance.

## Contact and accounting observations / limitations

**Total damage exceeded total restoration:** gross damage 0.013432554574859113 versus restoration 0.0031720941779426223. Final integrity remained below its healthy start. Positive restoration therefore does not establish full healing or general recovery.

The separate contact-interruption note is retained alongside the productive source transfer:

- Source-3 support consisted of **629 short support intervals** separated by **628 gaps**. The gaps totaled 0.22740191599123705 s; the longest was 0.00123002948387807 s. Supported contact totaled 25.405859094401176 s.
- There were no formal source-gap `release` labels. The support intervals and repeated recontact impulses establish the interruptions; original event labels are preserved. These are not 629 purposeful source revisits or autonomous switches.
- First source-3 impact damage was 0.004124216877448377. Subsequent recontact impacts caused another 0.0004699677279768306 of integrity loss. Source-3 sustained-stress damage was **0**; the repeated losses must not be attributed to above-threshold sustained stress.
- Repair-arrival impact caused 0.004811501904488715 of integrity loss before restoration. Wall contact and repair contact each formed one positive-duration interval.
- The maximum recorded surface gap after first source contact was 2.462581285556098e-07 world units. This is a saved-pose/event-endpoint maximum, not a proven continuous-time maximum.
- **No patch, tuning, retry or extension occurred**, as recorded. No replay, route substitution, continuation or additional case is added by this intake.

Repair contact had 74.29392088797518 s of resolved eligible support. The first-contact-to-departure interval cost 0.12407119508656572 energy with zero intake. Departure-to-source-3 travel lasted 29.36673898957497 s, costing 0.05084127946385125 energy with zero intake. Whole-case intake was 0.1521907717217202; expenditure was 0.3579540931640032; net E was -0.20576332144231707. Productive energy-source contact is distinct from whole-case net gain. These are supplied accounting observations, not adequacy judgments.

The contact note leaves open whether the short interruptions warrant a future numerical or control investigation. This intake neither declares an apparatus defect nor infers general physical infeasibility. It changes no engineering disposition, mechanism or numerical setting.

## Strongest bounded claim

> {claim}

“Uninterrupted world history” means the one continuous, unreset case history; it does not mean uninterrupted source contact. The 629 support intervals remain part of that same witness.

Explicitly withheld:

- general recovery capability;
- P discovery or perception;
- P learning/regulation;
- autonomous repair-seeking;
- survival capability;
- optimal repair duration;
- adequacy of repair rate;
- adequacy of damage/contact parameters.

Scientific/developmental efficacy remains **UNTESTED**. The ordered physical chain does not establish P success or failure. The manufactured low-E/I A3 arm, A4/A5, B1–B4 and C1/C2 were not executed; no additional arm or scientific experiment number is inferred from the A3 label.

## Validation and custody

The {src('evidence/EXECUTION_RESULT.json', 'execution result')} records one constructor attempt, administrative cutoff, no terminal crossing, no failure, no retry/resume/patch and zero physical replays. The {src(RR + 'ANALYSIS_RESULT.json', 'saved read-only analysis result')} reports completed checks within its stated scope, no analysis errors, 42 raw files unchanged, zero new world steps, zero controller computations and zero physical replays.

The {src(RR + 'RECORD_INTEGRITY.json', 'record-integrity result')} records 21,001 sensor envelopes, 2,100 controller rows, 21,000 native rows, 22,264 event rows and 21,000 diagnostic rows. The {src(RR + 'BOUNDARY_AND_DELIVERY.json', 'boundary/delivery result')} uses the preserved corrected V3 alignment and input checks, with inactive neural/RNG state at saved checkpoints and native RNG-counter checks. It makes no claim about arbitrary unrecorded transient state. Production `verify_segment` was not invoked because its pending-command validator recomputes commands even with `replay=False`; this remains a separately identified read-only analysis, not a production-verifier rerun.

A3's source records the prospectively approved symmetric 1e-10 boundary convention. This intake applies no new tolerance and does not amend the original A2 helper, timing flags or reports. The new contact note also records unchanged prior raw and analysis hashes. All source statements about code/cache/repository preservation remain attributed to the delivery; no actual repository inspection was performed here.

Intake verified the sealed result ZIP against both delivery receipts, all **70 payload hashes and CRCs**, and all **71 unpacked members** against the inbox copy. The embedded launch ZIP matches its separate delivery; all **86 launch payload hashes and CRCs** verify. Approved canonical bytes match the launch object and hash to the exact executed authority. The approved initial snapshot matches the launch snapshot. The embedded A2 ZIP and A2 timing note match their previously registered originals. Original-file before/after manifests and raw-analysis before/after manifests are byte-identical, and supplied analysis-source hashes match packaged files.

These are independent custody and registration checks. The physical results and post-run checks remain attributed to the supplied evidence; no simulation, scientific analysis, controller, test, viewer or archived script was executed during intake. No necessary source gap or source-identity conflict was found. Jason's current instruction supplies reporting/intake authority; this record adopts no new assistant proposal or numerical/mechanism decision.

[Source identities](SOURCE_IDENTITIES.json) · [Intake completion](INTAKE_RECORD.md) · [Final validation](VALIDATION.json).
'''
write(ROOT / 'NEW' / R, record)
nav = f'''## Current coupling commissioning — A3 observed, 2026-09-26

{status}

**A3: OBSERVED COMMISSIONING EVIDENCE.** Executed authority `{AUTH}`; P `{P}`; apparatus `{CP}`. The single case completed the prescribed **210 s / 21,000 native steps**, with no terminal crossing or execution error.

> {claim}

[A3 evidence record]({R}) · [Plain-language result]({B}/{RR}A3_PLAIN_LANGUAGE_RESULT.md) · [Contact-interruption note]({B}/{RR}CONTACT_INTERRUPTION_NOTE.md) · [Technical report]({B}/{RR}A3_COMMISSIONING_REPORT.md) · [Complete verified package]({B}/A3_COMMISSIONING_RESULT.zip) · [Previous A2 record]({A2R}).

Preserve the limitations: total damage exceeded restoration; source-3 contact comprised 629 short support intervals with repeated recontact damage; no patch/tuning/retry/extension occurred. Uninterrupted world history does not imply uninterrupted contact. Explicitly withheld: {withheld}. The intake changes no canon, P, Base World, mechanism, numerical settings or commissioning sequence; it initiates no execution and creates no scientific experiment number. Earlier sections below retain their dated historical dispositions.

'''
for name in ['00_RESEARCH_MAP.md', '01_WORKSPACE_STATUS.md']:
    text = (ROOT / 'BEFORE' / name).read_text(encoding='utf-8-sig')
    first, rest = text.split('\n', 1)
    old_heading = '## Current coupling commissioning — A2 observed, 2026-09-25'
    assert old_heading in rest
    rest = rest.replace(old_heading, '## Preserved A2 intake — 2026-09-25', 1)
    if name == '00_RESEARCH_MAP.md':
        old = 'selected for specification; exact external A1 and A2 packages authorized | coupling commissioning in progress; V1/V2/V3/A0 complete | A1 and A2 observed external-control witnesses; learning/developmental efficacy untested'
        assert old in rest
        rest = rest.replace(old, 'selected for specification; exact external A1, A2 and A3 packages authorized | coupling commissioning in progress; V1/V2/V3/A0 complete | A1/A2/A3 observed external-control witnesses; learning/developmental efficacy untested', 1)
    write(ROOT / 'AFTER' / name, first + '\n\n' + nav + rest.lstrip('\n'))
text = (ROOT / 'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig')
first, rest = text.split('\n', 1)
old_heading = '## Current commissioning evidence — A2 observed, 2026-09-25'
assert old_heading in rest
rest = rest.replace(old_heading, '## Preserved A2 commissioning evidence — 2026-09-25', 1)
continuation = f'''## Current commissioning evidence — A3 observed, 2026-09-26

The [registered A3 result]({R}) is **OBSERVED COMMISSIONING EVIDENCE** under executed authority `{AUTH}`: one external-control witness completed the prescribed 210 s / 21,000 native steps with real damage, eligible repair/restoration, repair departure, travel and productive source-3 contact. P engineering remains **VERIFIED**; apparatus **FIT / pre-run engineering CLOSED**; coupling commissioning **IN PROGRESS**; scientific/developmental efficacy **UNTESTED**. V1/V2/V3/A0 COMPLETE; A1/A2/A3 OBSERVED; A4/A5, B1–B4 and C1/C2 NOT EXECUTED.

Preserve damage exceeding restoration, 629 short source-3 support intervals and repeated recontact damage. No patch/tuning/retry/extension occurred. The continuous world history does not mean continuous contact. Withhold {withheld}. Earlier records remain distinct and unchanged. This intake grants no further execution, experiment number, canon/P/Base World/mechanism/numerical-setting/sequence change or Git operation. Earlier status sections are dated history.

'''
write(ROOT / 'AFTER/AGENTS.md', first + '\n\n' + continuation + rest.lstrip('\n'))
register = (ROOT / 'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
register += '\n## A3 observed coupling-commissioning evidence — 2026-09-26\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:
    register += f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
register += f'\n[A3 evidence record]({R}). Single executed authority `{AUTH}`; OBSERVED COMMISSIONING EVIDENCE. Complete result package and all members preserved, including separate contact-interruption findings. Other payload identities remain in the manifest. Earlier source rows/history are unchanged; efficacy UNTESTED.\n'
write(ROOT / 'AFTER/SOURCE_REGISTER.md', register)
verification = {'incoming_zip': str(Z), 'zip_bytes': len(raw), 'zip_sha256': sha(raw),
    'manifest_payloads_verified': len(mf['files']), 'archive_members': len(z.namelist()), 'crc_passed': True,
    'all_unpacked_inbox_members_match_zip': True, 'both_result_delivery_receipts_match': True,
    'launch_payloads_verified': len(lm['files']), 'launch_crc_passed': True, 'launch_zip_sha256': sha(launch),
    'launch_matches_separate_delivery': True, 'approved_canonical_sha256': sha(canonical),
    'approved_canonical_matches_launch': True, 'approved_initial_snapshot_matches_launch': True,
    'embedded_A2_zip_and_timing_note_match_registered_originals': True,
    'supplied_before_after_original_manifests_identical': True,
    'supplied_before_after_raw_analysis_manifests_identical': True,
    'analysis_source_hashes_match_packaged_files': True, 'contact_interruptions_preserved': True,
    'requested_reporting_precision_matches_saved_summary': True,
    'source_execution_native_steps': execution['native_index'], 'source_stop': integrity['status'],
    'programs_or_tests_run_during_intake': False, 'simulation_or_controller_execution_during_intake': False,
    'git_operations': False, 'necessary_source_gaps': [], 'source_identity_conflicts': []}
inventory = {p.relative_to(batch).as_posix(): sha(p.read_bytes()) for p in batch.rglob('*') if p.is_file()}
dump(ROOT / 'NEW' / S / 'SOURCE_IDENTITIES.json', {'session_id': ID, 'authority_sha256': AUTH,
    'verification': verification, 'registered_sources': entries, 'complete_batch_sha256': inventory})
intake = f'''# A3 intake completion

**Scope:** Register the single authorized A3 as OBSERVED COMMISSIONING EVIDENCE. Integration owner: this session, under Jason's current intake/status instruction. [Full record](A3_COMMISSIONING_EVIDENCE_RECORD.md).

**Read:** Current workbench instructions/map/status; A3 package entry, plain-language result, contact-interruption note, technical report, executed authority, original launch history, summary and validation/custody records.

**Changed:** New append-only source batch and unique session; source identities SRC-164–SRC-{old_count + len(entries):03d}; live AGENTS.md, 00_RESEARCH_MAP.md, 01_WORKSPACE_STATUS.md, SOURCE_CATALOG.json and SOURCE_REGISTER.md. Existing source rows and all prior sources/candidates/reviews/decisions/sessions are preserved. Local recovery copies of the five prior live files are in PRIOR_SHARED_NOTES.zip, with PRIOR_SHARED_NOTES_RECEIPT.json.

**Validation:** Result ZIP and both receipts match; 70 outer payload hashes/CRCs and 71 unpacked members verify; embedded launch matches its separate delivery with 86 verified payloads. Exact canonical authority and initial snapshot match; the embedded prior A2 ZIP/timing note match already-registered sources. Supplied preservation manifests and analysis-source identities verify. New links, published bytes, protected-file hashes and prior catalog rows are checked at publication. [Validation receipt](VALIDATION.json) · [Source identities](SOURCE_IDENTITIES.json).

**Current status:** V1/V2/V3/A0 COMPLETE; A1/A2/A3 OBSERVED; A4/A5, B1–B4 and C1/C2 NOT EXECUTED. Coupling commissioning IN PROGRESS; scientific/developmental efficacy UNTESTED. Damage exceeded restoration; 629 short source-3 support intervals and recontact damage remain observations/limitations, not general recovery, parameter-adequacy or P-efficacy conclusions.

**Open:** Later cases and efficacy remain untested; the contact note leaves any future numerical/control investigation unresolved. No necessary source gap was found. No new scientific experiment number, code execution, simulation, replay, commissioning case, tuning, canon/mechanism/configuration/sequence change, actual repository amendment or Git operation occurred. Stop after reporting this intake.
'''
write(ROOT / 'NEW' / S / 'INTAKE_RECORD.md', intake)
dump(ROOT / 'PLAN.json', {'session': S, 'batch': B, 'review': R, 'live_before': before,
    'protected_before': protected, 'source_entries': entries, 'verification': verification,
    'zip_source': str(Z), 'old_catalog_count': old_count, 'status': 'A3 OBSERVED COMMISSIONING EVIDENCE; efficacy UNTESTED',
    'incoming_before': incoming, 'batch_inventory': inventory})
print(json.dumps({'prepared': ID, 'sources': len(entries), 'batch_files': len(inventory),
    'outer_payloads_verified': len(mf['files']), 'launch_payloads_verified': len(lm['files']), 'protected': len(protected)}))
