"""Documentation intake only: byte custody and saved-result registration, no supplied code execution."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib, io, json, zipfile

ROOT = Path(__file__).resolve().parent
WB = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ID = '2026-09-25-a2-evidence-intake-b671e309'
S = '50_SESSIONS/' + ID
B = '90_SOURCES/p_a2_commissioning_2026-09-25_b671e309'
R = S + '/A2_COMMISSIONING_EVIDENCE_RECORD.md'
D = WB / 'INBOX/2026-09-25-A2-commissioning-result-5f077481'
LD = WB / 'INBOX/2026-09-25-A2-launch-packet-5f077481'
Z = D / 'A2_COMMISSIONING_RESULT.zip'
AUTH = '229bedc93d793892488ee0f8b1b42035777f11f70952e43179a768a30cfc3007'
P = '6bc9683b54e4fa80136fe8534d7713e2a250a95f'
CP = '5f07748102cb5eaa302569c87efbae095050e9fe'
A1S = '50_SESSIONS/2026-09-25-first-a1-evidence-intake-6ad829e4'
V3S = '50_SESSIONS/2026-09-25-v3-viewer-intake-4e7b80c2'
A1R = A1S + '/FIRST_A1_COMMISSIONING_EVIDENCE_RECORD.md'
V3R = V3S + '/A1_V3_REANALYSIS_AND_VIEWER_CONTINUATION.md'
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
assert len(raw) == receipt['bytes'] and sha(raw) == receipt['sha256']
assert receipt['authority_sha256'] == AUTH
z = zipfile.ZipFile(io.BytesIO(raw))
mf = archive_check(z)
assert mf['authority_sha256'] == AUTH
assert len(mf['files']) == receipt['verified_payloads'] == 60
incoming = {str(Z): sha(raw), str(D / 'DELIVERY_RECEIPT.json'): sha((D / 'DELIVERY_RECEIPT.json').read_bytes())}
for n in z.namelist():
    p = D / 'A2_COMMISSIONING_RESULT' / n
    assert p.read_bytes() == z.read(n), n
    incoming[str(p)] = sha(z.read(n))

launch = z.read('approved-launch/A2_LAUNCH_PACKET.zip')
lr = json.loads((LD / 'DELIVERY_RECEIPT.json').read_text(encoding='utf-8-sig'))
assert launch == (LD / 'A2_LAUNCH_PACKET.zip').read_bytes()
assert sha(launch) == lr['sha256'] and len(launch) == lr['bytes']
for p in [LD / 'DELIVERY_RECEIPT.json', LD / 'A2_LAUNCH_PACKET.zip']:
    incoming[str(p)] = sha(p.read_bytes())
lz = zipfile.ZipFile(io.BytesIO(launch))
lm = archive_check(lz, 'A2_LAUNCH_PACKET/')
assert len(lm['files']) == 75 and lm['authority_sha256'] == AUTH
canonical = z.read('evidence/APPROVED_OBJECT.canonical.json')
assert sha(canonical) == AUTH
assert canonical == lz.read('A2_LAUNCH_PACKET/AUTHORITY_OBJECT.canonical.json')
assert AUTH in z.read('evidence/AUTHORIZATION_SOURCE.txt').decode()
old_a1 = WB / '90_SOURCES/p_first_a1_commissioning_2026-09-25_6ad829e4/FIRST_A1_COMMISSIONING_RESULT.zip'
assert lz.read('A2_LAUNCH_PACKET/references/FIRST_A1_COMMISSIONING_RESULT.zip') == old_a1.read_bytes()
assert z.read('evidence/APPROVED_INITIAL_A2.snapshot.json.gz') == lz.read('A2_LAUNCH_PACKET/INITIAL_A2.snapshot.json.gz')
assert z.read('evidence/ORIGINAL_FILES_BEFORE.json') == z.read('evidence/ORIGINAL_FILES_AFTER.json')
assert z.read(RR + 'RAW_EVIDENCE_BEFORE_ANALYSIS.json') == z.read(RR + 'RAW_EVIDENCE_AFTER_ANALYSIS.json')
execution = json.loads(z.read('evidence/EXECUTION_RESULT.json'))
analysis = json.loads(z.read(RR + 'ANALYSIS_RESULT.json'))
integrity = json.loads(z.read(RR + 'RECORD_INTEGRITY.json'))
timing = json.loads(z.read(RR + 'TIMING_REPORTING_NOTE.json'))
assert execution['approved_execution_sha256'] == analysis['authority_sha256'] == integrity['authority_sha256'] == AUTH
assert execution['apparatus_checkpoint'] == CP and execution['native_index'] == 18000
assert execution['run_constructors_attempted'] == 1 and execution['no_retry_no_resume_no_patch']
assert execution['failure'] is None and execution['terminal_dimension'] is None and execution['physical_replays'] == 0
assert integrity['complete'] and integrity['valid'] and integrity['status'] == 'administrative_cutoff'
assert analysis['errors'] == {} and analysis['original_raw_files_unchanged']
assert analysis['new_simulation_steps'] == analysis['controller_command_computations'] == analysis['physical_replays'] == 0
assert not timing['analysis_or_simulator_patch'] and timing['new_world_steps'] == 0
assert [v['event_index'] for v in timing['flagged_nominal_boundary_events']] == [9001, 12002]

live = ['AGENTS.md', '00_RESEARCH_MAP.md', '01_WORKSPACE_STATUS.md', 'SOURCE_CATALOG.json', 'SOURCE_REGISTER.md']
before = {}
for n in live:
    data = (WB / n).read_bytes()
    before[n] = {'bytes': len(data), 'sha256': sha(data)}
    p = ROOT / 'BEFORE' / n
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
protected = {}
for folder in ['90_SOURCES', '20_CANDIDATES', '30_REVIEWS', '40_DECISIONS', A1S, V3S]:
    for p in (WB / folder).rglob('*'):
        if p.is_file():
            protected[p.relative_to(WB).as_posix()] = sha(p.read_bytes())
catalog = json.loads((ROOT / 'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
old_count = len(catalog['source_files'])
assert old_count == 137
batch = ROOT / 'SOURCE_BATCH'
batch.mkdir(exist_ok=True)
(batch / Z.name).write_bytes(raw)
(batch / 'DELIVERY_RECEIPT.json').write_bytes((D / 'DELIVERY_RECEIPT.json').read_bytes())
for n in z.namelist():
    p = batch / n
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(z.read(n))
# Reading copies of the original launch documents, still unmodified historical proposal bytes.
for n in ['A2_LAUNCH_PACKET.md', 'AUTHORITY_OBJECT.canonical.json', 'FILE_MANIFEST.json']:
    p = batch / 'approved-launch/A2_LAUNCH_PACKET' / n
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(lz.read('A2_LAUNCH_PACKET/' + n))
(batch / 'approved-launch/DELIVERY_RECEIPT.json').write_bytes((LD / 'DELIVERY_RECEIPT.json').read_bytes())

selected = [Z.name, 'DELIVERY_RECEIPT.json', 'README.md', 'FILE_MANIFEST.json',
    'evidence/AUTHORIZATION_SOURCE.txt', 'evidence/APPROVED_OBJECT.canonical.json', 'evidence/APPROVAL_REQUEST.json',
    'evidence/EXECUTION_RESULT.json', 'evidence/LAUNCHED_MANIFEST.json']
selected += [RR + n for n in ['A2_PLAIN_LANGUAGE_RESULT.md', 'A2_COMMISSIONING_REPORT.md', 'A2_RESULT_SUMMARY.json',
    'A2_OBSERVATIONS.json', 'TIMING_REPORTING_NOTE.json', 'RECORD_INTEGRITY.json', 'BOUNDARY_AND_DELIVERY.json',
    'ACCOUNTING.json', 'ALL_FIXED_WINDOWS.json', 'ANALYSIS_RESULT.json', 'RAW_EVIDENCE_BEFORE_ANALYSIS.json', 'RAW_EVIDENCE_AFTER_ANALYSIS.json']]
selected += ['PRESERVATION_CHECK.json', 'RESOURCE_RESULT.json', 'approved-launch/A2_LAUNCH_PACKET.zip',
    'approved-launch/A2_LAUNCH_PACKET/A2_LAUNCH_PACKET.md', 'approved-launch/DELIVERY_RECEIPT.json']
entries = []
for number, n in enumerate(selected, old_count + 1):
    data = (batch / n).read_bytes()
    is_member = n in z.namelist()
    if is_member:
        origin = str(Z) + '::' + n
    elif n.startswith('approved-launch/A2_LAUNCH_PACKET/'):
        origin = str(LD / 'A2_LAUNCH_PACKET.zip') + '::A2_LAUNCH_PACKET/' + PurePosixPath(n).name
    elif n == 'approved-launch/DELIVERY_RECEIPT.json':
        origin = str(LD / 'DELIVERY_RECEIPT.json')
    else:
        origin = str(D / n)
    entries.append({'source_id': f'SRC-{number:03d}', 'path': B + '/' + n,
        'original_filename': PurePosixPath(n).name, 'bytes': len(data), 'sha256': sha(data),
        'role': 'observed-commissioning-evidence' if n.startswith('evidence/') else 'commissioning-package-custody-and-authority-history',
        'prepared': '2026-09-25', 'stated_author': 'Supplied A2 execution/read-only result package; exact assistant model/backend not stated',
        'acquired_from': origin, 'archive_member': n if is_member else None,
        'authority': 'Jason requests intake of the single already-authorized A2 result; no additional execution or mechanism/configuration change',
        'source_execution_authority_sha256': AUTH, 'p_baseline_checkpoint': P, 'reviewed_checkpoint': CP,
        'review_note': R, 'record': S + '/INTAKE_RECORD.md', 'continues': V3R,
        'notes': 'OBSERVED COMMISSIONING EVIDENCE. Original ZIP and all 61 members preserved byte-for-byte. Historical launch proposal labels remain unchanged; the later exact grant is separately retained. No scientific/developmental efficacy established.'})
catalog['source_files'] += entries
catalog['intake_events'].append({'session_id': ID, 'source_ids': [e['source_id'] for e in entries],
    'review_note': R, 'record': S + '/INTAKE_RECORD.md', 'continues': V3R,
    'scope': 'Single authorized A2 OBSERVED COMMISSIONING EVIDENCE; 18000 native steps / 180 s cutoff; unchanged raw helper flags; efficacy UNTESTED'})
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
| A2 | OBSERVED — OBSERVED COMMISSIONING EVIDENCE |
| A3–A5 | NOT YET EXECUTED |
| B1–B4 | NOT YET EXECUTED |
| C1/C2 | NOT YET EXECUTED |'''

claim = 'One externally controlled physical witness demonstrated declining local source usefulness before stock reached zero, departure without reset, reserve-consuming travel to a different source, and renewed productive energy transfer at that second source under the unchanged world/body laws.'
record = f'''# A2 — observed coupling-commissioning evidence

**Registered:** 2026-09-25. **Disposition: OBSERVED COMMISSIONING EVIDENCE.** This registers the single already-executed, authorized A2 case. It adds no execution, experiment number or change to the commissioning sequence.

{status}

## Authority and continuity

- Exact A2 authority: `{AUTH}` — {src('evidence/APPROVED_OBJECT.canonical.json', 'approved canonical object')} and {src('evidence/AUTHORIZATION_SOURCE.txt', 'exact authorization text')}.
- P engineering baseline: `{P}`.
- Apparatus checkpoint: `{CP}`.
- Primary report: {src(RR + 'A2_PLAIN_LANGUAGE_RESULT.md', 'A2_PLAIN_LANGUAGE_RESULT.md')}.
- Complete verified delivery: {src('A2_COMMISSIONING_RESULT.zip', 'original A2 result ZIP')} and {src('FILE_MANIFEST.json', 'payload identity manifest')}.
- Supporting detail: {src(RR + 'A2_COMMISSIONING_REPORT.md', 'technical report')}, {src(RR + 'A2_RESULT_SUMMARY.json', 'full-precision summary')} and {src(RR + 'A2_OBSERVATIONS.json', 'observation records')}.

This continues the workbench's [first A1 commissioning record](../../{A1R}) and [completed V3 / passive viewer record](../../{V3R}). A2 is its own single authorized trajectory, initialized from the approved original time-zero snapshot; it is not a continuation of A1's final state. Departure inside A2 occurred without reset. The original A1 trajectory, original failed V3 post-check, corrected read-only V3 analysis and passive A1 viewer retain their distinct identities and dispositions.

The {src('approved-launch/A2_LAUNCH_PACKET/A2_LAUNCH_PACKET.md', 'original launch packet')} and its receipt retain their pre-approval “PROPOSED / NOT AUTHORIZED” history unchanged. The later exact authorization and execution record establish this A2 case's separate authority. The grant required report-don't-patch and no retry, route substitution, tuning, continuation or additional case without separate authorization. It grants no new execution through this intake.

## Recorded sequence

Values below follow the requested reporting precision; linked records retain full precision and timestamps.

| Observation | Recorded result |
|---|---|
| Extent and stop | 18,000 native steps; prescribed 180 s administrative cutoff |
| First source-0 contact | 6.31019 s |
| First negative-net source-0 window | 52.0–52.2 s, while stock remained about 0.0663 |
| Departure, without reset | 90 s; E = 0.7400694; I = 0.9930767; source-0 stock = 0.0351485 |
| Actual release-to-source-1 contact travel | 42.37643 s; energy cost = 0.07565365; intake = 0 |
| First source-1 contact | 132.37643 s; pre-contact stock = 0.2 |
| Source-1 total transfer | 0.15144825 |
| First positive-net source-1 window | 132.4–132.6 s |
| Final reserves | E = 0.7381512; I = 0.9863441 |
| Terminal crossing | None |
| Mover contact | None |
| Execution exception | None |

The negative result concerns a recorded finite 0.2 s local window, not an inferred exact instantaneous zero crossing. Source-0 stock in that window changed from 0.06652155860849777 to 0.06626443259547216; its net energy change was -1.1218724983441675e-06. The externally prescribed departure at 90 s is not evidence that P detected or acted on this change.

## Whole-case accounting and source history

| Quantity | Recorded result |
|---|---|
| Gross intake | 0.34031477 |
| Expenditure | 0.30216354 |
| Net E | +0.03815123 |
| Source-0 transfer | 0.18886653 |
| Source-0 stock at final stop, after post-departure renewal | 0.06836337 |
| Source-1 final stock | 0.05928729 |
| Other six source stocks | Each remained 0.2 |

See the preserved {src(RR + 'ACCOUNTING.json', 'accounting result')} and {src(RR + 'ALL_FIXED_WINDOWS.json', 'complete fixed-window results')}. Post-departure renewal of source 0 was recorded; no return to that source or renewal-supported cycle was demonstrated.

## Physical observations retained without interpretation

- Both source contacts briefly exceeded the 0.25 stress threshold.
- Peak contact forces were approximately 0.27075 and 0.27327 (full recorded maxima 0.27074663791428305 and 0.27326702539735814).
- Total integrity loss was 0.01365586 (full recorded value 0.013655858384640111).
- Source-1 contact contained two microscopic release/recontact gaps: 142.76000000001514–142.7600395926028 s and 164.19999999999564–164.20003960557497 s, each about 0.0000396 s.
- No repair occurred.

No further mechanism, safety, viability or ecological interpretation is attached to these observations. No mover contact is recorded; this does not establish absence of optical exposure, whose object identities are not recorded.

## Reporting limitation — retain the original helper flags

The {src(RR + 'TIMING_REPORTING_NOTE.json', 'original timing reporting note')} and every original derived artifact are preserved byte-identically. No analysis or simulator patch was made during this intake.

| Flagged event | Recorded endpoint | Nominal boundary | Offset in seconds | Within existing event-time tolerance |
|---|---|---|---|---|
| 9001 | 90.00000000000914 | 90.0 | 9.137579581874888e-12 | true |
| 12002 | 120.00000000002449 | 120.0 | 2.4485302674293052e-11 | true |

Existing `event_time_tolerance` remains `1e-10`. The raw stage helper fields remain:

| Interval | `boundary_straddling_events` | `complete_event_boundary_coverage` |
|---|---|---|
| Nominal stage 0, 0–90 s | `[9001]` | `false` |
| Nominal stage 1, 90–120 s | `[9001, 12002]` | `false` |
| Nominal stage 2, 120 s to recorded stop | `[12002]` | `false` |
| Nominal commanded-travel interval, 90.0 s to source-1 contact | `[9001]` | `false` |
| Exact recorded release-to-source-1-contact interval | `[]` | `true` |

The actual recorded release is 90.00000000000914 s, and source-1 contact is 132.3764279535912 s: duration **42.37642795358205 s**, energy cost **0.07565364813787812**, intake **0**. The nominal-boundary flags do not change this interval or its accounting.

The raw `planned_unobserved_seconds` / horizon subtraction value **1.872990651463624e-11** is also retained exactly. The supplied timing note identifies it as a representation residual, not a missing native step. It states that the helper over-flags sub-tolerance nominal-boundary endpoint offsets; the flags identify no extra or missing physical step. This is the supplied reporting qualification, not a patched result or a new tolerance.

## Strongest bounded claim and withheld claims

> {claim}

Explicitly withheld:

- P discovery, perception, learning or regulation;
- autonomous switching;
- survival capability;
- indefinite viability;
- renewal-supported cyclic sustainability;
- broad ecological sufficiency.

The external waypoint controller supplied the route, with the organism inactive for this witness. Whole-case positive net energy is not a test of P's scientific or developmental efficacy. That efficacy remains **UNTESTED**.

## Verification scope and source distinctions

The {src('evidence/EXECUTION_RESULT.json', 'execution result')} records one constructor attempt, no retry/resume/patch, no physical replay, and a completed administrative cutoff. The {src(RR + 'ANALYSIS_RESULT.json', 'subsequent read-only analysis')} reports all five saved-record sections completed without errors, 39 raw files unchanged, zero new simulation steps, zero controller-command computations and zero physical replays.

The {src(RR + 'RECORD_INTEGRITY.json', 'record-integrity result')} records 18,001 sensor envelopes, 1,800 controller rows, 18,000 native rows, 18,009 event rows and 18,000 diagnostic rows. The {src(RR + 'BOUNDARY_AND_DELIVERY.json', 'boundary/delivery result')} is a saved-record analysis, not a new execution. Production `verify_segment` was explicitly not invoked: its pending-command validator recomputes waypoint commands even with `replay=False`. The source reports separate read-only receipt, authority, sequence, boundary, accounting and delivery checks. This intake does not relabel them as a production verifier run.

Intake independently checked the outer ZIP against its receipt, all **60 payload hashes and CRCs**, and all **61 unpacked members** against the supplied folder. The embedded launch ZIP matches its separate delivery, with all **75 launch payload hashes and CRCs** verified. The approved canonical bytes match the launch object and hash to the exact A2 authority. The embedded A1 archive matches the previously registered original. Supplied before/after original-file manifests and before/after raw-analysis manifests match byte-for-byte. These checks establish source custody and registration consistency; the reported scientific/physical observations are attributed to the supplied result, not independently rerun here.

Jason's current instruction supplies intake authority and the bounded reporting scope. Observations remain distinct from that authority. No new assistant mechanism proposal, numerical choice or sequence change is adopted. No necessary source gap or conflicting package identity was found. No supplied program, checker, controller, viewer or simulation was executed in this intake; no actual Loom repository or canonical document was changed.

[Source identities](SOURCE_IDENTITIES.json) · [Intake completion](INTAKE_RECORD.md) · [Final custody/navigation validation](VALIDATION.json).
'''
write(ROOT / 'NEW' / R, record)

nav = f'''## Current coupling commissioning — A2 observed, 2026-09-25

{status}

Exact A2 authority: `{AUTH}`. P `{P}` and apparatus `{CP}` retain their reviewed dispositions. The single A2 completed **18,000 native steps** at the prescribed **180 s administrative cutoff**. There was no terminal crossing, mover contact or execution exception.

> {claim}

[A2 evidence and reporting limits]({R}) · [Primary plain-language result]({B}/{RR}A2_PLAIN_LANGUAGE_RESULT.md) · [Complete verified result package]({B}/A2_COMMISSIONING_RESULT.zip) · [Original unchanged timing flags]({B}/{RR}TIMING_REPORTING_NOTE.json) · [Prior A1 / corrected V3 / passive viewer]({V3R}).

The stage-boundary helper flags remain exactly as reported and unpatched; they do not alter the actual release-to-contact interval or its accounting. Contact-force threshold excursions, integrity loss, two microscopic source-1 release/recontact gaps and no repair remain physical observations without added interpretation. No P discovery/perception/learning/regulation, autonomous switching, survival capability, indefinite viability, renewal-supported cyclic sustainability or broad ecological sufficiency is established. No further execution, experiment number, numerical dial, canon, P, Base World or commissioning-sequence change is authorized by this intake. Earlier sections below retain their dated historical dispositions.

'''
for name in ['00_RESEARCH_MAP.md', '01_WORKSPACE_STATUS.md']:
    text = (ROOT / 'BEFORE' / name).read_text(encoding='utf-8-sig')
    first, rest = text.split('\n', 1)
    old_heading = '## Current A1 continuation — completed V3 and passive viewer, 2026-09-25'
    assert old_heading in rest
    rest = rest.replace(old_heading, '## Preserved A1 continuation — completed V3 and passive viewer, 2026-09-25', 1)
    if name == '00_RESEARCH_MAP.md':
        old = 'selected for specification; exact first external A1 package authorized | coupling commissioning in progress; V1/V2/V3/A0 complete | one bounded external A1 observed; learning/developmental efficacy untested'
        assert old in rest
        rest = rest.replace(old, 'selected for specification; exact external A1 and A2 packages authorized | coupling commissioning in progress; V1/V2/V3/A0 complete | A1 and A2 observed external-control witnesses; learning/developmental efficacy untested', 1)
    write(ROOT / 'AFTER' / name, first + '\n\n' + nav + rest.lstrip('\n'))

text = (ROOT / 'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig')
first, rest = text.split('\n', 1)
rest = rest.replace('## Current A1 continuation — completed V3 and passive viewer, 2026-09-25', '## Preserved A1 continuation — completed V3 and passive viewer, 2026-09-25', 1)
continuation = f'''## Current commissioning evidence — A2 observed, 2026-09-25

The [registered A2 result]({R}) records **OBSERVED COMMISSIONING EVIDENCE** under exact authority `{AUTH}`: one externally controlled case, 18,000 native steps, prescribed 180 s administrative cutoff. P engineering remains **VERIFIED**; apparatus **FIT / pre-run engineering CLOSED**; coupling commissioning **IN PROGRESS**; scientific/developmental efficacy **UNTESTED**. V1/V2/V3/A0 are COMPLETE; A1/A2 OBSERVED; A3–A5, B1–B4 and C1/C2 NOT YET EXECUTED.

Preserve the original stage-boundary helper flags and their reporting qualification unchanged. They do not alter exact recorded release-to-contact travel/accounting. Preserve physical force/integrity/gap observations without interpreting them as P success or failure. The A2 witness establishes no P discovery/perception/learning/regulation, autonomous switching, survival, indefinite viability, renewal-supported cyclic sustainability or broad ecological sufficiency. Earlier A1, failed V3, corrected read-only V3 and passive-viewer records remain distinct and unchanged. This intake grants no additional execution, replay, tuning, numerical-dial change, experiment number, canon/P/Base World/sequence change or Git operation. Earlier status sections are dated history.

'''
write(ROOT / 'AFTER/AGENTS.md', first + '\n\n' + continuation + rest.lstrip('\n'))
register = (ROOT / 'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
register += '\n## A2 observed coupling-commissioning evidence — 2026-09-25\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:
    register += f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
register += f'\n[A2 evidence record]({R}). Single authorized A2: OBSERVED COMMISSIONING EVIDENCE. Authority `{AUTH}`. Complete result ZIP and every member preserved; all other payload identities remain in its manifest. Timing flags remain unchanged; no efficacy claim or new execution.\n'
write(ROOT / 'AFTER/SOURCE_REGISTER.md', register)

verification = {'incoming_zip': str(Z), 'zip_bytes': len(raw), 'zip_sha256': sha(raw),
    'manifest_payloads_verified': len(mf['files']), 'archive_members': len(z.namelist()), 'crc_passed': True,
    'all_unpacked_inbox_members_match_zip': True, 'launch_payloads_verified': len(lm['files']),
    'launch_crc_passed': True, 'launch_zip_sha256': sha(launch), 'launch_matches_separate_delivery': True,
    'approved_canonical_sha256': sha(canonical), 'approved_canonical_matches_launch': True,
    'embedded_A1_matches_registered_original': True, 'supplied_before_after_original_manifests_identical': True,
    'supplied_before_after_raw_analysis_manifests_identical': True, 'timing_flags_preserved_without_patch': True,
    'source_execution_native_steps': execution['native_index'], 'source_stop': integrity['status'],
    'programs_or_tests_run_during_intake': False, 'simulation_or_controller_execution_during_intake': False,
    'git_operations': False, 'necessary_source_gaps': [], 'source_identity_conflicts': []}
inventory = {p.relative_to(batch).as_posix(): sha(p.read_bytes()) for p in batch.rglob('*') if p.is_file()}
dump(ROOT / 'NEW' / S / 'SOURCE_IDENTITIES.json', {'session_id': ID, 'authority_sha256': AUTH,
    'verification': verification, 'registered_sources': entries, 'complete_batch_sha256': inventory})
intake = f'''# A2 intake completion

**Scope:** Register one already-authorized A2 as OBSERVED COMMISSIONING EVIDENCE. Integration owner: this intake session, acting under Jason's current instruction. [Full evidence record](A2_COMMISSIONING_EVIDENCE_RECORD.md).

**Completed:** Read the live workbench instructions/navigation and supplied A2 plain-language, technical, authority, execution, timing and read-only validation records. Verified the complete result package's 60 payload hashes/CRCs, all 61 unpacked members, the embedded launch package's 75 payload hashes/CRCs, receipt identities, exact approved object and retained A1 identity. Preserved source bytes, all original derived reporting flags and earlier evidence history. Registered SRC-138–SRC-{old_count + len(entries):03d} and updated only AGENTS.md, 00_RESEARCH_MAP.md, 01_WORKSPACE_STATUS.md, SOURCE_CATALOG.json and SOURCE_REGISTER.md outside the new session/source directories.

**Status:** V1/V2/V3/A0 COMPLETE; A1/A2 OBSERVED; A3–A5, B1–B4 and C1/C2 NOT YET EXECUTED. Coupling commissioning IN PROGRESS; scientific/developmental efficacy UNTESTED. No new case, experiment number, mechanism/configuration/canon/sequence/dial change, actual repository operation, code execution, test rerun or simulation occurred in this intake. No necessary source gap was found.

**Recovery and validation:** PRIOR_SHARED_NOTES.zip preserves the five pre-intake shared files; PRIOR_SHARED_NOTES_RECEIPT.json records their exact identities. Prior source, candidate, review, decision, A1-session and V3-session files are checked unchanged before/after publication. [Validation receipt](VALIDATION.json) records final link, source, prior-row and byte-preservation checks. [Source identities](SOURCE_IDENTITIES.json).

Stop after reporting the completed intake; no next commissioning case is initiated.
'''
write(ROOT / 'NEW' / S / 'INTAKE_RECORD.md', intake)
dump(ROOT / 'PLAN.json', {'session': S, 'batch': B, 'review': R, 'live_before': before,
    'protected_before': protected, 'source_entries': entries, 'verification': verification,
    'zip_source': str(Z), 'old_catalog_count': old_count, 'status': 'A2 OBSERVED COMMISSIONING EVIDENCE; efficacy UNTESTED',
    'incoming_before': incoming, 'batch_inventory': inventory})
print(json.dumps({'prepared': ID, 'sources': len(entries), 'batch_files': len(inventory),
    'outer_payloads_verified': len(mf['files']), 'launch_payloads_verified': len(lm['files']), 'protected': len(protected)}))
