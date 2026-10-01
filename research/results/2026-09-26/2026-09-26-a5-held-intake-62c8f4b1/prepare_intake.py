"""Register an A5 held proposal; hashing/custody only, no clock audit rerun or simulation."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import hashlib, io, json, zipfile

ROOT = Path(__file__).resolve().parent
WB = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ID = '2026-09-26-a5-held-intake-62c8f4b1'
S = '50_SESSIONS/' + ID
B = '90_SOURCES/p_a5_held_proposal_2026-09-26_62c8f4b1'
R = S + '/A5_HELD_PROPOSAL_RECORD.md'
D = WB / 'INBOX/2026-09-26-A5-launch-packet-HOLD-5f077481'
Z = D / 'A5_LAUNCH_PACKET_HOLD.zip'
AUTH = '88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6'
P = '6bc9683b54e4fa80136fe8534d7713e2a250a95f'
CP = '5f07748102cb5eaa302569c87efbae095050e9fe'
A4R = '50_SESSIONS/2026-09-26-a4-evidence-intake-0e69b3c8/A4_COMMISSIONING_EVIDENCE_RECORD.md'
A4B = '90_SOURCES/p_a4_commissioning_2026-09-26_0e69b3c8'
CLASS = 'APPARATUS / CLOCK-COMPATIBILITY QUESTION PENDING REVIEW'
sha = lambda b: hashlib.sha256(b).hexdigest()

def write(p, t):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(t, encoding='utf-8', newline='\n')

def dump(p, v): write(p, json.dumps(v, indent=2, ensure_ascii=False) + '\n')

raw = Z.read_bytes()
receipt = json.loads((D / 'DELIVERY_RECEIPT.json').read_text(encoding='utf-8-sig'))
copy_receipt = json.loads((D / 'COPY_VERIFICATION.json').read_text(encoding='utf-8-sig'))
assert len(raw) == receipt['zip_bytes'] == copy_receipt['zip_bytes']
assert sha(raw) == receipt['zip_sha256'] == copy_receipt['zip_sha256']
assert receipt['authority_sha256'] == copy_receipt['verification']['authority_sha256'] == AUTH
assert not receipt['launch_ready'] and receipt['zero_simulation_execution']
z = zipfile.ZipFile(io.BytesIO(raw))
names = z.namelist()
assert len(names) == len(set(names)) == len({n.casefold() for n in names})
for n in names:
    p = PurePosixPath(n)
    assert not p.is_absolute() and '..' not in p.parts and ':' not in n and '\\' not in n
mf = json.loads(z.read('FILE_MANIFEST.json'))
assert set(mf['files']) == set(names) - {'FILE_MANIFEST.json'}
assert mf['authority_sha256'] == AUTH and mf['disposition'] == 'HOLD_CLOCK_INCOMPATIBILITY'
assert len(mf['files']) == receipt['payload_count'] == 89
for n, meta in mf['files'].items():
    data = z.read(n)
    assert len(data) == meta['bytes'] and sha(data) == meta['sha256'], n
assert z.testzip() is None
incoming = {str(Z): sha(raw)}
for n in ['DELIVERY_RECEIPT.json', 'COPY_VERIFICATION.json']:
    incoming[str(D / n)] = sha((D / n).read_bytes())
for n in names:
    p = D / 'A5_LAUNCH_PACKET_HOLD' / n
    assert p.read_bytes() == z.read(n), n
    incoming[str(p)] = sha(z.read(n))
canonical = z.read('AUTHORITY_OBJECT.canonical.json')
assert sha(canonical) == AUTH and AUTH in z.read('AUTHORITY_SHA256.txt').decode()
obj = json.loads(canonical)
manifest = json.loads(z.read('A5_MANIFEST.json'))
assert manifest['execution_authority'] is None
assert obj == {k:v for k,v in manifest.items() if k != 'execution_authority'}
assert obj == json.loads(z.read('AUTHORITY_OBJECT.json'))
assert obj['case_id'] == 'A5' and obj['duration_seconds'] == obj['hard_stop_time'] == 630
protocol = obj['execution']['procedure']['protocol']
assert protocol['source_visit_order'] == [0,1,0,1]
assert not protocol['launch_ready'] and protocol['launch_disposition'] == 'HOLD_CLOCK_INCOMPATIBILITY'
assert protocol['reviewed_checkpoints']['p_git_sha'] == P and protocol['reviewed_checkpoints']['apparatus_git_sha'] == CP
for n,h in protocol['bound_files'].items(): assert sha(z.read(n)) == h, n
assert sha(z.read('INITIAL_A5.snapshot.json.gz')) == protocol['initial_snapshot_file']['sha256']
assert z.read('INITIAL_A5.snapshot.json.gz') == z.read('references/INITIAL_A1.snapshot.json.gz')
assert z.read('references/A4_COMMISSIONING_RESULT.zip') == (WB / A4B / 'A4_COMMISSIONING_RESULT.zip').read_bytes()
assert z.read('references/A4_COMMISSIONING_EVIDENCE_RECORD.md') == (WB / A4R).read_bytes()
assert z.read('HASH_BEFORE.json') == z.read('HASH_AFTER.json')
checks = json.loads(z.read('PREPARATION_CHECKS.json'))
audit = json.loads(z.read('CLOCK_AUDIT.json'))
static = json.loads(z.read('STATIC_VALIDATION.json'))
for k in ['world_steps','field_steps','neural_steps','controller_commands','simulation_RNG_draws','new_prehistory_steps',
          'Engine_constructors','Run_constructors','sensor_evaluations','trial_routes','trial_phases','replays']:
    assert checks[k] == 0, k
assert not checks['production_runtime_failure_reproduced'] and not checks['launch_ready']
assert static['execution_grant'] is None and not static['launch_ready'] and static['authority_sha256'] == AUTH
assert audit['world_steps'] == audit['controller_calls'] == audit['rng_draws'] == 0
assert not audit['commissioning_failure_observed']
assert audit['first_decision_exceedance']['native_index'] == 26950
assert audit['first_decision_exceedance']['index_derived_time'] == 269.5
for n, meta in audit['source_excerpts'].items():
    assert sha(z.read('instrument/developmental_ecology/' + n)) == meta['sha256'], n

live = ['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md']
before = {}
for n in live:
    data = (WB / n).read_bytes()
    before[n] = {'bytes':len(data), 'sha256':sha(data)}
    p = ROOT / 'BEFORE' / n
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
protected = {}
for folder in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS','50_SESSIONS']:
    for p in (WB / folder).rglob('*'):
        if p.is_file(): protected[p.relative_to(WB).as_posix()] = sha(p.read_bytes())
catalog = json.loads((ROOT / 'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
old_count = len(catalog['source_files'])
assert old_count == 228
batch = ROOT / 'SOURCE_BATCH'
batch.mkdir(exist_ok=True)
(batch / Z.name).write_bytes(raw)
for n in ['DELIVERY_RECEIPT.json','COPY_VERIFICATION.json']:
    (batch / n).write_bytes((D / n).read_bytes())
for n in names:
    p = batch / n
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(z.read(n))
selected = [Z.name,'DELIVERY_RECEIPT.json','COPY_VERIFICATION.json','README.md','OPEN_ISSUE_A5_CLOCK.md',
    'CLOCK_AUDIT.json','AUTHORITY_OBJECT.canonical.json','AUTHORITY_OBJECT.json','AUTHORITY_SHA256.txt',
    'A5_MANIFEST.json','INITIAL_A5.snapshot.json.gz','INITIAL_STATE_SUMMARY.json','PREPARATION_CHECKS.json',
    'PREPARATION_REVIEW_NOTE.json','STATIC_VALIDATION.json','PRESERVATION.json','HASH_BEFORE.json','HASH_AFTER.json',
    'PROCEDURES.md','CIRCUIT_AND_RENEWAL_RATIONALE.json','OBSERVATION_AND_INTERPRETATION.md','REVIEW_AND_EXECUTION_BOUNDARY.md',
    'RESOURCE_PLAN.md','RESOURCE_PROJECTION.json','VIEWER_RECORD_CONTRACT.md','SOURCE_IDENTITIES.json',
    'CODE_AND_RUNTIME_IDENTITIES.json','FILE_MANIFEST.json']
entries = []
for number,n in enumerate(selected, old_count+1):
    data = (batch/n).read_bytes()
    member = n in names
    entries.append({'source_id':f'SRC-{number:03d}','path':B+'/'+n,'original_filename':PurePosixPath(n).name,
        'bytes':len(data),'sha256':sha(data),'role':'held-commissioning-proposal-and-static-preparation-evidence',
        'prepared':'2026-09-26','registered':'2026-09-26',
        'stated_author':'Supplied held A5 preparation package; exact assistant model/backend not stated',
        'acquired_from':str(Z)+'::'+n if member else str(D/n),'archive_member':n if member else None,
        'authority':'Jason requests registration of held preparation; no execution, correction or launch approval',
        'held_proposal_authority_sha256':AUTH,'execution_authorized':False,'execution_occurred':False,
        'p_baseline_checkpoint':P,'pinned_apparatus_checkpoint':CP,'review_note':R,'record':S+'/INTAKE_RECORD.md',
        'classification':CLASS,'notes':'A5 PREPARED / HOLD / NOT LAUNCH-READY. Full packet and zero-execution records preserved. Static clock finding is conditional, not an observed A5 production failure or scientific result.'})
catalog['source_files'] += entries
catalog['intake_events'].append({'session_id':ID,'source_ids':[e['source_id'] for e in entries],
    'review_note':R,'record':S+'/INTAKE_RECORD.md','held_proposal_authority_sha256':AUTH,
    'scope':'A5 PREPARED / HOLD / NOT LAUNCH-READY; apparatus / clock-compatibility question pending review; no A5 execution or failure finding'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)

def src(n,label):return f'[{label}](../../{B}/{n})'

status = '''P engineering: **VERIFIED within its prior reviewed scope**  
Commissioning apparatus: **prior scoped closure retained; A5 clock compatibility PENDING REVIEW**  
Coupling commissioning: **IN PROGRESS; A5 held before execution**  
Scientific/developmental efficacy: **UNTESTED**

| Commissioning item | Current status |
|---|---|
| V1 | COMPLETE |
| V2 | COMPLETE |
| V3 | COMPLETE |
| A0 | COMPLETE within its bounded scope |
| A1–A4 | OBSERVED within their bounded scopes |
| A5 | PREPARED / HOLD / NOT LAUNCH-READY; NOT EXECUTED |
| B1–B4 | NOT EXECUTED |
| C1/C2 | NOT EXECUTED |'''
record = f'''# A5 — held commissioning proposal

**Registered:** 2026-09-26. **A5 — PREPARED / HOLD / NOT LAUNCH-READY.**

**Classification: {CLASS}.**

**No A5 simulation occurred.** This is a preparation record, not observed A5 commissioning execution evidence. The held proposal authority identity is `{AUTH}`. It identifies the exact held object; it is not execution approval or a launch-ready approval target.

{status}

## Preserved proposal and source identities

{src('A5_LAUNCH_PACKET_HOLD.zip','Complete held packet')} · {src('README.md','packet entry')} · {src('OPEN_ISSUE_A5_CLOCK.md','OPEN_ISSUE_A5_CLOCK.md')} · {src('CLOCK_AUDIT.json','CLOCK_AUDIT.json')} · {src('AUTHORITY_OBJECT.canonical.json','exact held canonical bytes')} · {src('AUTHORITY_SHA256.txt','held canonical hash')}.

Pinned P remains `{P}`; pinned apparatus remains `{CP}`. The {src('A5_MANIFEST.json','manifest')} has a null execution grant. The bound protocol says `HOLD_CLOCK_INCOMPATIBILITY`, `launch_ready: false` and `PROPOSED / NOT AUTHORIZED / HOLD`. That source label is retained alongside Jason's requested classification above; no new approval is inferred.

The proposal preserves **630 simulated seconds**, with source order **0 → 1 → 0 → 1**, and approximately **210–222 s of unattended renewal opportunity between revisits**. The {src('PROCEDURES.md','complete procedures')} and {src('CIRCUIT_AND_RENEWAL_RATIONALE.json','circuit/renewal rationale')} retain the schedule, original healthy A1/A2 zero-time snapshot, unchanged laws and numerical settings. This is one proposed return circuit plus a second outbound leg, not two completed closed circuits. Renewal opportunities and possible contact times are planning estimates; no A5 source stock, renewed uptake, productive revisit or viability outcome has been observed.

The source-0 revisit stage is proposed for 300–450 s, followed by the final source-1 stage at 480–630 s. The 630 s horizon and all fixed stage windows are preserved; no shorter substitute or clock workaround is adopted.

## Observed preparation blocker and its limits

The supplied **static source/arithmetic audit** found that the pinned apparatus would reject a valid nonterminal controller command at approximately **269.5 simulated seconds**, before the first planned revisit. This finding is conditional on uninterrupted full native steps while the case remains nonterminal and has not stopped earlier. It does not predict survival to that time or report a production failure receipt.

The original issue locates accumulation in `loom_commissioning/adapter.py` and the absolute decision-clock check in `loom_commissioning/pending.py::validate_decision`. Saved audit values are:

| Audit quantity | Supplied value |
|---|---|
| First scalar native-step exceedance | Native index 26,941 |
| First subsequent command-decision boundary | Native index 26,950 |
| Accumulated time there | 269.4999999998999 s |
| Index-derived time | 269.5 s |
| Difference | -1.0010126061388291e-10 s |
| Existing absolute tolerance | 1e-10 s |
| Reported predicate result | `false`; `issued decision clock mismatch` |

The source also identifies an implicated stage/full-hold predicate at nominal 270 s; the earlier decision-clock predicate already blocks reaching it as a launch outcome. The audit used scalar additions/comparisons and source excerpts, with no Loom import, production-validator invocation, controller calculation or simulation. This intake preserves that evidence without rerunning the audit or declaring the question independently closed.

**Do not record A5 failure, ecological failure, inadequate source renewal, inadequate source stock or P failure.** None follows from this preparation blocker. No mechanism result, repair decision, tolerance change or physical-law conclusion is recorded.

## Zero-execution preparation evidence

The original {src('PREPARATION_CHECKS.json','preparation checks')} report zero world, field and neural steps; zero controller commands; zero simulation RNG draws; zero new prehistory; zero Engine and Run constructors; zero sensor evaluations; zero trial routes/phases and replays. They also state that the production long-clock failure was not reproduced. The original snapshot was copied and decoded as inert data.

{src('STATIC_VALIDATION.json','Static saved-byte validation')} passes packet identity/structure checks while explicitly retaining `launch_ready: false`, a null grant and the hold. A passing packet check is not launch fitness. The {src('PREPARATION_REVIEW_NOTE.json','preparation review note')}, {src('PRESERVATION.json','preservation report')} and exact {src('HASH_BEFORE.json','before')} / {src('HASH_AFTER.json','after')} inventories remain preserved. The source reports all 647 scoped original files unchanged; that is its preparation audit, not a fresh inspection of the actual repository by this intake.

## Current boundaries and unresolved review

A0–A4 remain completed/observed within their bounded scopes, as recorded in the [A4 evidence and prior history](../../{A4R}). They ended before the newly identified clock boundary. The original final mechanical closure retains its reviewed scope; it is not silently expanded to certify this 630 s proposal, nor rewritten as a failed prior review. The earlier exact-05abf604 apparatus hold and its design-not-failed clarification remain checkpoint history.

A5 is held before execution. B1–B4 and C1/C2 remain not executed. Scientific/developmental efficacy remains **UNTESTED**.

The {src('REVIEW_AND_EXECUTION_BOUNDARY.md','held review boundary')} leaves apparatus clock compatibility for a separate Jason ruling. This intake proposes no particular correction and authorizes none. Any later changed instrument would need its own reviewed identity and newly bound launch packet/authorization; the held hash alone cannot remove the hold. No numerical adjustment, timestamp rewrite, guard removal, restart workaround, route substitution, simulation or canonical amendment is performed here. The proposal and all its alternatives/limits remain reviewable as supplied.

## Intake verification and completion

The original ZIP matches both external receipts. All **89 payload hashes/CRCs** and **90 unpacked members** match the inbox copy. Canonical bytes hash to `{AUTH}` and equal the full manifest with only the null execution grant omitted. Every protocol-bound file identity and the copied initial snapshot match. Audit source-excerpt hashes match the packaged source files. The embedded A4 result ZIP and A4 workbench record match their registered originals; HASH_BEFORE and HASH_AFTER are byte-identical. Zero-execution fields and held status were checked in the saved records.

These checks establish custody and consistent registration, not runtime fitness or scientific outcomes. No archived helper, scalar audit, production validator, test, controller, simulation or viewer was executed. No necessary source gap or conflicting package identity was found. The current user instruction supplies the classification and intake authority; the 630 s circuit remains a held proposal, not an accepted execution decision.

[Source identities](SOURCE_IDENTITIES.json) · [Intake completion](INTAKE_RECORD.md) · [Final validation](VALIDATION.json).
'''
write(ROOT/'NEW'/R,record)
nav = f'''## Current commissioning boundary — A5 held proposal, 2026-09-26

{status}

**A5 — PREPARED / HOLD / NOT LAUNCH-READY.** Held proposal authority identity: `{AUTH}`. **{CLASS}.** No A5 simulation occurred; the hash identifies a held proposal, not execution approval.

Proposed bounded question: **630 simulated seconds; source 0 → source 1 → source 0 → source 1; approximately 210–222 s unattended renewal opportunity between revisits**. A static source/arithmetic audit found that the pinned apparatus would reject a valid nonterminal controller command at about **269.5 s**, before the first planned revisit, conditional on the case remaining nonterminal. No production failure or physical A5 outcome was observed.

[Held proposal record]({R}) · [Complete preserved packet]({B}/A5_LAUNCH_PACKET_HOLD.zip) · [Original open issue]({B}/OPEN_ISSUE_A5_CLOCK.md) · [Clock audit]({B}/CLOCK_AUDIT.json) · [Held canonical object]({B}/AUTHORITY_OBJECT.canonical.json) · [Zero-execution preparation checks]({B}/PREPARATION_CHECKS.json) · [Prior A4 evidence]({A4R}).

Do not classify this as A5 failure, ecological failure, inadequate source renewal, inadequate source stock or P failure. A0–A4 and prior engineering closure retain their bounded scopes; the new A5 compatibility question remains pending review. No canon, mechanism, Base World configuration, numerical setting or commissioning-sequence change, repair, launch, new run or experiment number is authorized by this intake. Earlier sections below retain their dated dispositions.

'''
for name in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    text=(ROOT/'BEFORE'/name).read_text(encoding='utf-8-sig')
    first,rest=text.split('\n',1)
    heading='## Current coupling commissioning — A4 observed, 2026-09-26'
    assert heading in rest
    rest=rest.replace(heading,'## Preserved A4 intake — before A5 clock review, 2026-09-26',1)
    if name=='00_RESEARCH_MAP.md':
        old='coupling commissioning in progress; V1/V2/V3/A0 complete | A1–A4 observed external-control witnesses; learning/developmental efficacy untested'
        assert old in rest
        rest=rest.replace(old,'coupling commissioning in progress; V1/V2/V3/A0 complete; A5 held before execution | A1–A4 observed external-control witnesses; A5 clock compatibility pending review; learning/developmental efficacy untested',1)
    write(ROOT/'AFTER'/name,first+'\n\n'+nav+rest.lstrip('\n'))
text=(ROOT/'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig')
first,rest=text.split('\n',1)
heading='## Current commissioning evidence — A4 observed, 2026-09-26'
assert heading in rest
rest=rest.replace(heading,'## Preserved A4 commissioning evidence — before A5 clock review, 2026-09-26',1)
continuation=f'''## Current commissioning boundary — A5 held proposal, 2026-09-26

The [registered A5 preparation]({R}) is **PREPARED / HOLD / NOT LAUNCH-READY**, held proposal identity `{AUTH}`. Classify its static finding as **{CLASS}**: conditional on remaining nonterminal, the pinned apparatus would reject a command near 269.5 s before the proposed first revisit. **No A5 simulation occurred.** The 630 s source 0 → 1 → 0 → 1 proposal and approximately 210–222 s renewal opportunities remain proposed, not observed.

V1/V2/V3/A0 remain COMPLETE; A1–A4 OBSERVED within their bounded scopes; A5 held before execution; B1–B4 and C1/C2 NOT EXECUTED; efficacy UNTESTED. Prior P verification and apparatus closure retain their reviewed scopes, while A5 clock compatibility is pending review. Preserve the held packet, OPEN_ISSUE_A5_CLOCK.md, CLOCK_AUDIT.json, canonical hash and zero-execution records. Do not record A5/ecological/P failure or inadequate renewal/stock. The held hash is not execution permission. This intake authorizes no correction, tolerance/numerical/world/mechanism/canon/sequence change, workaround, simulation, experiment number or Git operation. Earlier evidence and exact checkpoint histories remain unchanged.

'''
write(ROOT/'AFTER/AGENTS.md',first+'\n\n'+continuation+rest.lstrip('\n'))
register=(ROOT/'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
register+='\n## A5 held commissioning proposal — 2026-09-26\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:register+=f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
register+=f'\n[Held preparation record]({R}). Proposal hash `{AUTH}`; PREPARED / HOLD / NOT LAUNCH-READY. {CLASS}. No A5 simulation or failure finding; complete held packet and all zero-execution evidence preserved.\n'
write(ROOT/'AFTER/SOURCE_REGISTER.md',register)
verification={'incoming_zip':str(Z),'zip_bytes':len(raw),'zip_sha256':sha(raw),'manifest_payloads_verified':len(mf['files']),
    'archive_members':len(names),'crc_passed':True,'all_unpacked_inbox_members_match_zip':True,'both_delivery_receipts_match':True,
    'held_canonical_sha256':sha(canonical),'canonical_equals_manifest_without_null_grant':True,'execution_grant_is_null':True,
    'protocol_launch_ready':False,'bound_file_identities_verified':len(protocol['bound_files']),
    'audit_source_hashes_match_packaged_files':True,'copied_initial_snapshot_verified':True,
    'embedded_A4_zip_and_record_match_registered_originals':True,'supplied_before_after_manifests_identical':True,
    'zero_execution_preparation_fields_verified':True,'source_commissioning_failure_observed':False,
    'classification':CLASS,'clock_audit_rerun_during_intake':False,'programs_or_tests_run_during_intake':False,
    'simulation_or_controller_execution_during_intake':False,'git_operations':False,'necessary_source_gaps':[],'source_identity_conflicts':[]}
inventory={p.relative_to(batch).as_posix():sha(p.read_bytes()) for p in batch.rglob('*') if p.is_file()}
dump(ROOT/'NEW'/S/'SOURCE_IDENTITIES.json',{'session_id':ID,'held_proposal_authority_sha256':AUTH,
    'execution_authorized':False,'verification':verification,'registered_sources':entries,'complete_batch_sha256':inventory})
intake=f'''# A5 held-proposal intake completion

Registered **A5 — PREPARED / HOLD / NOT LAUNCH-READY** under Jason's current instruction. Integration owner: this intake session. Classification: **{CLASS}**. [Full record](A5_HELD_PROPOSAL_RECORD.md).

Read current workbench instructions/map/status and the held packet entry, open issue, saved clock audit, manifest/canonical object, procedures/renewal rationale, preparation checks and review boundary. Preserved the complete original held archive, all 90 members and both receipts; verified 89 payload hashes/CRCs, proposal identity, bound documents, null grant, zero-execution fields and prior A4 identities. Registered SRC-229–SRC-{old_count+len(entries):03d}.

Changed only the new session/source batch and AGENTS.md, 00_RESEARCH_MAP.md, 01_WORKSPACE_STATUS.md, SOURCE_CATALOG.json and SOURCE_REGISTER.md. Original source/candidate/review/decision/session files and earlier catalog rows remain unchanged. PRIOR_SHARED_NOTES.zip and its receipt preserve all five prior shared files. [Validation](VALIDATION.json) · [Source identities](SOURCE_IDENTITIES.json).

No A5 execution or production failure occurred; the apparatus clock question remains pending review. A0–A4 retain completed/observed bounded dispositions; A5 held before execution; B1–B4 and C1/C2 not executed; efficacy untested. No A5/ecological/P failure or inadequate renewal/stock is recorded. No source gap was found.

No scalar-audit rerun, scientific calculation, controller, simulation, test, patch, numerical/world/mechanism/canon/sequence change, actual repository amendment, experiment number or Git operation occurred during intake. The held hash remains review-only. Stop after confirmation.
'''
write(ROOT/'NEW'/S/'INTAKE_RECORD.md',intake)
dump(ROOT/'PLAN.json',{'session':S,'batch':B,'review':R,'live_before':before,'protected_before':protected,
    'source_entries':entries,'verification':verification,'zip_source':str(Z),'old_catalog_count':old_count,
    'status':'A5 PREPARED / HOLD / NOT LAUNCH-READY; clock compatibility pending review; no execution',
    'incoming_before':incoming,'batch_inventory':inventory})
print(json.dumps({'prepared':ID,'sources':len(entries),'batch_files':len(inventory),'payloads_verified':len(mf['files']),
    'protected':len(protected),'held_canonical_sha256':sha(canonical),'execution_grant':None}))
