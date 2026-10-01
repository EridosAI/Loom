"""Document custody and navigation only. Does not import or execute review code."""
import hashlib
import json
import re
import shutil
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

WB = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ROOT = Path(__file__).resolve().parent
PAYLOAD = ROOT / 'PAYLOAD'
ID = '2026-09-23-p-post-correction-intake-1677619b'
SESSION = '50_SESSIONS/' + ID
BATCH = '90_SOURCES/p_post_correction_review_2026-09-23_1677619b'
NOTE = '30_REVIEWS/REVIEW-P-ENGINEERING-f7eb6f27-2026-09-23-1677619b.md'
INBOX = 'INBOX/2026-09-23-P_Independent_Post_Correction'
REPORT = 'LOOM_P_INDEPENDENT_POST_CORRECTION_FIDELITY_REVIEW.md'
ZIP = 'Loom_P_Independent_Post_Correction_Review_f7eb6f27_20260923.zip'
COMMIT = 'f7eb6f27c661e3db193a4225b56a825d7e41739d'
PREVIOUS = 'd5f7efbe67193f215e52d95ca912db131a79f31c'
SHARED = ['00_RESEARCH_MAP.md', '01_WORKSPACE_STATUS.md', '20_CANDIDATES/CAND-P.md', 'SOURCE_CATALOG.json', 'SOURCE_REGISTER.md']
STATUS = '\n'.join([
    'P engineering baseline',
    'Checkpoint: ' + COMMIT,
    'Status: ENGINEERING HOLD',
    '',
    'R1 original fixture: closed',
    'R1-P oblique release/recontact class: open',
    'R2: verified closed',
    'R3: verified closed',
    'P mechanism fidelity: unchanged / previously verified',
    'Scientific status: uncommissioned / untested',
])

def digest(data):
    return hashlib.sha256(data).hexdigest()

def file_digest(path):
    with path.open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()

def put(relative, data):
    target = PAYLOAD / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data.encode('utf-8') if isinstance(data, str) else data)

def write_json(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def prepare():
    PAYLOAD.mkdir(exist_ok=False)
    before = {p: (WB / p).read_bytes() for p in SHARED}
    incoming = {name: {'bytes': (WB / INBOX / name).stat().st_size, 'sha256': file_digest(WB / INBOX / name)} for name in (REPORT, ZIP)}
    assert incoming[ZIP]['sha256'] == '076eebb7c7e43428194cea26307e0f7433257ae55ea275d238e35d3d74877158'
    with zipfile.ZipFile(WB / INBOX / ZIP) as z:
        names = z.namelist()
        assert len(names) == len(set(names))
        assert all(not n.startswith(('/', '\\')) and '..' not in Path(n).parts and ':' not in n for n in names)
        manifest_bytes = z.read('FILE_MANIFEST.json')
        manifest = json.loads(manifest_bytes)
        assert set(names) == set(manifest) | {'FILE_MANIFEST.json'}
        checked = []
        for name, expected in manifest.items():
            with z.open(name) as f:
                actual = hashlib.file_digest(f, 'sha256').hexdigest()
            assert actual == expected['sha256'], name
            assert z.getinfo(name).file_size == expected['bytes'], name
            checked.append({'path': name, **expected})
        receipt_bytes = z.read('REVIEW_RECEIPT.json')
        receipt = json.loads(receipt_bytes)
        report_bytes = z.read(REPORT)
        assert report_bytes == (WB / INBOX / REPORT).read_bytes()
        assert digest(report_bytes) == receipt['report_sha256']
        assert receipt['reviewed_checkpoint'] == COMMIT and receipt['previous_checkpoint'] == PREVIOUS
        assert receipt['original_r1_counterexample_corrected'] is True
        assert receipt['classifications'] == {'R1': 'MUST-FIX BEFORE COMMISSIONING', 'R2': 'VERIFIED', 'R3': 'VERIFIED'}
        assert manifest['reviewed_delivery/' + receipt['reviewed_delivery']['name']]['sha256'] == receipt['reviewed_delivery']['sha256']
        retained = {REPORT: report_bytes, 'REVIEW_RECEIPT.json': receipt_bytes, 'FILE_MANIFEST.json': manifest_bytes}
    for name, data in retained.items():
        put(BATCH + '/' + name, data)
    for name, data in before.items():
        put(SESSION + '/SHARED_BEFORE/' + name, data)

    paragraph_status = STATUS.replace('\n', '  \n')
    note = '# ' + paragraph_status + '\n\n'
    note += f'[Independent post-correction review](../{BATCH}/{REPORT}) · [Review receipt](../{BATCH}/REVIEW_RECEIPT.json) · [Complete evidence package](../{BATCH}/{ZIP}).\n\n'
    note += 'Recorded as requested by Jason in the 2026-09-23 intake instruction. This is an exact-checkpoint engineering status, not a finding that P has failed scientifically. Verification and closure findings are attributed to the independent review; this intake did not rerun its tests.\n\n'
    note += f'The [earlier checkpoint review](../50_SESSIONS/2026-09-23-p-engineering-review-284c3913/P_ENGINEERING_CHECKPOINT_REVIEW.md) remains unchanged and applies to `{PREVIOUS}`. The original R1 fixture closure does not close the broader R1-P class.\n\n'
    note += f'[Intake record and validation](../{SESSION}/INTAKE_RECORD.md).\n'
    put(NOTE, note)

    research_map = before['00_RESEARCH_MAP.md'].decode('utf-8-sig')
    marker = '## Foundation and direction'
    assert research_map.count(marker) == 1
    new_section = f'## Current P engineering baseline — 2026-09-23\n\nCheckpoint `{COMMIT}`: **ENGINEERING HOLD**. R1 original fixture closed; R1-P oblique release/recontact class open; R2 and R3 verified closed. P mechanism fidelity unchanged / previously verified. Scientific status uncommissioned / untested. [Exact status and review]({NOTE}) · [Intake record]({SESSION}/INTAKE_RECORD.md).\n\nThis later engineering record supersedes the specification-stage work-status wording below for this checkpoint only. Earlier decisions, source documents and reviews remain preserved. This intake authorizes no repair or execution.\n\n'
    research_map = research_map.replace(marker, new_section + marker, 1)
    research_map = research_map.replace('| selected for specification | review draft prepared | untested |', '| selected for specification | engineering hold at f7eb6f27 | uncommissioned / untested |')
    put('00_RESEARCH_MAP.md', research_map)

    status = before['01_WORKSPACE_STATUS.md'].decode('utf-8-sig')
    assert '## Current continuation — 2026-09-20' in status
    current = '## Current engineering checkpoint — 2026-09-23\n\n' + paragraph_status + '\n\n'
    current += f'[Recorded status and source review]({NOTE}) · [Intake record]({SESSION}/INTAKE_RECORD.md).\n\n'
    current += 'This records Jason’s current intake instruction and the independent delta review. The specification-stage status below is a dated snapshot. No repair, commissioning or scientific execution is authorized by this intake. Integration scope is this intake only; no standing ownership is claimed.\n\n'
    status = status.replace('## Current continuation — 2026-09-20', current + '## Preserved specification continuation — 2026-09-20', 1)
    put('01_WORKSPACE_STATUS.md', status)

    candidate = before['20_CANDIDATES/CAND-P.md'].decode('utf-8-sig')
    assert 'revision: r002' in candidate and 'work_status: specification-review-draft-prepared' in candidate
    candidate = candidate.replace('revision: r002', 'revision: r003', 1).replace('work_status: specification-review-draft-prepared', 'work_status: engineering-hold\nengineering_checkpoint: ' + COMMIT, 1)
    candidate = candidate.replace('## Source identity', f'## Current engineering checkpoint — 2026-09-23\n\n`{COMMIT}`: **ENGINEERING HOLD**. [Exact status and independent post-correction review](../{NOTE}). R1 original fixture closed; R1-P open; R2 and R3 verified closed. P mechanism fidelity unchanged / previously verified; scientific status uncommissioned / untested.\n\nThe specification-stage statements below are preserved as the 2026-09-20 record. This update changes navigation and engineering status only; the complete candidate and specification originals are unchanged.\n\n## Source identity', 1)
    candidate = candidate.replace('## Current specification commission', '## Specification commission — 2026-09-20 record', 1).replace('## Evidence and disposition', '## Specification-stage evidence and disposition — 2026-09-20 record', 1)
    candidate += f'\n2026-09-23, {ID}: r003 records the exact f7eb6f27 engineering hold and verified closures, with source-linked navigation. Mechanism and earlier source history preserved.\n'
    put('20_CANDIDATES/CAND-P.md', candidate)

    catalog = json.loads(before['SOURCE_CATALOG.json'])
    old_rows = list(catalog['source_files'])
    start_id = max(int(row['source_id'].split('-')[1]) for row in old_rows) + 1
    rows = []
    for offset, name in enumerate((REPORT, ZIP, 'REVIEW_RECEIPT.json', 'FILE_MANIFEST.json')):
        identity = incoming[name] if name in incoming else {'bytes': len(retained[name]), 'sha256': digest(retained[name])}
        row = {'source_id': f'SRC-{start_id + offset:03}', 'path': BATCH + '/' + name, 'original_filename': name, **identity,
               'role': 'independent-post-correction-engineering-review' if name == REPORT else ('independent-review-delivery-archive' if name == ZIP else 'independent-review-custody-metadata'),
               'authority': 'Independent engineering delta review of exact checkpoint; not a scientific mechanism result or new execution authority',
               'prepared': '2026-09-23', 'stated_author': 'Independent reviewer; exact model/backend not stated in the main report or receipt',
               'acquired_from': INBOX + '/' + name if name in incoming else INBOX + '/' + ZIP + '::' + name,
               'reviewed_checkpoint': COMMIT, 'previous_checkpoint': PREVIOUS,
               'review_note': NOTE, 'notes': 'Preserved byte-for-byte. Supporting scripts and nested corrective delivery retained inside the original ZIP; nothing executed.'}
        rows.append(row)
    catalog['source_files'].extend(rows)
    catalog.setdefault('intake_events', []).append({'session_id': ID, 'source_ids': [r['source_id'] for r in rows], 'review_note': NOTE, 'record': SESSION + '/INTAKE_RECORD.md', 'scope': 'Jason-requested source intake and exact engineering-status navigation only'})
    assert catalog['source_files'][:len(old_rows)] == old_rows
    put('SOURCE_CATALOG.json', json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')

    register = before['SOURCE_REGISTER.md'].decode('utf-8-sig')
    register += '\n## P independent post-correction review intake — 2026-09-23\n\n'
    register += '| ID | Source | Identity |\n|---|---|---|\n'
    for row in rows:
        register += f"| {row['source_id']} | [{row['original_filename']}]({row['path']}) | {row['bytes']} bytes; SHA-256 `{row['sha256']}` |\n"
    register += f'\nCheckpoint `{COMMIT}`: **ENGINEERING HOLD**. R1 original fixture closed; R1-P open; R2 and R3 verified closed. Mechanism fidelity unchanged / previously verified; scientific status uncommissioned / untested. [Recorded status]({NOTE}) · [Intake validation]({SESSION}/INTAKE_RECORD.md). Prior source rows and reviews are preserved.\n'
    put('SOURCE_REGISTER.md', register)

    record = '# P post-correction review intake — 2026-09-23\n\n'
    record += f'[Recorded status](../../{NOTE}) · [Research map](../../00_RESEARCH_MAP.md) · [Live status](../../01_WORKSPACE_STATUS.md).\n\n'
    record += f'Ingested the two incoming files from `{INBOX}` under Jason’s current instruction. This session owns only this source intake and requested navigation/status update. The report and ZIP remain untouched in INBOX and are preserved byte-for-byte in `{BATCH}`; receipt and manifest were copied from the ZIP without rewriting them.\n\n'
    record += f'Read the full main review, receipt and intake README, current Workbench instructions/map/status, source catalog/register and P wrapper. The review describes a delta from `{PREVIOUS}` to `{COMMIT}`. Its exact R1/R1-P distinction and verified R2/R3 closures match Jason’s requested status. No fresh scientific or implementation review was performed.\n\n'
    record += f'Archive checks: all {len(manifest)} manifest-listed payload members match their declared lengths/SHA-256; the {len(names)}th member is the manifest itself. The loose report equals its ZIP member and receipt hash. The nested corrective delivery hash matches the receipt. ZIP SHA-256: `{incoming[ZIP]["sha256"]}`. The external `ZIP_SHA256.txt` mentioned by the source was not supplied in this INBOX batch; the outer hash is computed custody evidence, not comparison with that absent sidecar.\n\n'
    record += f'Registered {", ".join(r["source_id"] for r in rows)}. Updated map, live status, P navigation wrapper, catalog and register. Their previous complete bytes are in `SHARED_BEFORE/`; all {len(old_rows)} earlier catalog records retain their identities. The earlier d5f7efbe review and decision history are unchanged.\n\n'
    record += 'Validation is recorded in [VALIDATION.json](VALIDATION.json). It checks source/archive hashes, new links, exact status text, shared-file change guards and preserved records. Supporting source scripts, tests and reproduction commands were not executed. No actual Loom repository, Git state, vault settings, candidate equations, scientific canon, commissioning or experiments were changed.\n'
    put(SESSION + '/INTAKE_RECORD.md', record)
    protected = {}
    for p in sorted((WB / '40_DECISIONS').rglob('*')):
        if p.is_file():
            protected[p.relative_to(WB).as_posix()] = file_digest(p)
    for p in (WB / '50_SESSIONS/2026-09-23-p-engineering-review-284c3913').rglob('*'):
        if p.is_file():
            protected[p.relative_to(WB).as_posix()] = file_digest(p)
    for row in old_rows:
        p = WB / row['path']
        if p.is_file():
            protected[row['path']] = file_digest(p)
    for rel in ('AGENTS.md', '20_CANDIDATES/CAND-R.md', '02_OPEN_QUESTIONS.md'):
        protected[rel] = file_digest(WB / rel)
    validation = {'session_id': ID, 'created_at_utc': datetime.now(timezone.utc).isoformat(), 'reviewed_checkpoint': COMMIT,
                  'incoming': incoming, 'archive_members': len(names), 'manifest_payloads_verified': len(manifest),
                  'loose_report_matches_archive_and_receipt': True, 'nested_delivery_hash_matches_receipt': True,
                  'outer_zip_external_checksum_sidecar_supplied': False, 'old_catalog_rows_preserved': len(old_rows),
                  'source_ids': [r['source_id'] for r in rows], 'review_code_or_tests_executed': False, 'shared_files': SHARED,
                  'status_text': STATUS, 'manifest_validation': checked}
    put(SESSION + '/VALIDATION.json', json.dumps(validation, indent=2) + '\n')
    plan = {'shared_before': {p: digest(b) for p, b in before.items()}, 'protected': protected,
            'incoming': incoming, 'zip_destination': BATCH + '/' + ZIP,
            'staged_hashes': {p.relative_to(PAYLOAD).as_posix(): file_digest(p) for p in PAYLOAD.rglob('*') if p.is_file()}}
    write_json(ROOT / 'PLAN.json', plan)
    # Resolve only links in newly authored/updated navigation, not historical links inside raw source documents.
    links = []
    for rel in SHARED[:-2] + ['SOURCE_REGISTER.md', NOTE, SESSION + '/INTAKE_RECORD.md']:
        text = (PAYLOAD / rel).read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^\n]+?)\)', text):
            target = unquote(target.split('#')[0].strip('<>'))
            if not target or '://' in target:
                continue
            logical = (WB / rel).parent / target
            logical = logical.resolve()
            logical.relative_to(WB.resolve())
            destrel = logical.relative_to(WB).as_posix()
            assert logical.exists() or (PAYLOAD / destrel).exists() or destrel == plan['zip_destination'], (rel, target)
            links.append({'from': rel, 'to': destrel})
    write_json(ROOT / 'LINK_CHECK.json', {'resolved_links': len(links), 'links': links})
    print(json.dumps({'prepared': ID, 'manifest_verified': len(manifest), 'archive_members': len(names), 'source_ids': validation['source_ids'], 'links': len(links), 'shared_updates': SHARED}))

def publish():
    plan = json.loads((ROOT / 'PLAN.json').read_text(encoding='utf-8'))
    for rel, expected in plan['shared_before'].items():
        assert file_digest(WB / rel) == expected, 'Shared file changed: ' + rel
    for rel, expected in plan['protected'].items():
        assert file_digest(WB / rel) == expected, 'Protected file changed: ' + rel
    for name, expected in plan['incoming'].items():
        assert file_digest(WB / INBOX / name) == expected['sha256'], 'Incoming file changed: ' + name
    for rel, expected in plan['staged_hashes'].items():
        assert file_digest(PAYLOAD / rel) == expected, 'Staged file changed: ' + rel
        target = WB / rel
        target.resolve().relative_to(WB.resolve())
        assert rel in SHARED or not target.exists(), 'New destination exists: ' + rel
    assert not (WB / plan['zip_destination']).exists()
    # Preserve new sources and backups before touching shared navigation.
    for rel in plan['staged_hashes']:
        if rel not in SHARED:
            target = WB / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(PAYLOAD / rel, target)
            assert file_digest(target) == plan['staged_hashes'][rel]
    shutil.copyfile(WB / INBOX / ZIP, WB / plan['zip_destination'])
    assert file_digest(WB / plan['zip_destination']) == plan['incoming'][ZIP]['sha256']
    for rel, expected in plan['shared_before'].items():
        assert file_digest(WB / rel) == expected, 'Shared conflict after source preservation: ' + rel
    for rel in SHARED:
        assert file_digest(WB / rel) == plan['shared_before'][rel]
        shutil.copyfile(PAYLOAD / rel, WB / rel)
        assert file_digest(WB / rel) == plan['staged_hashes'][rel]
    for rel, expected in plan['protected'].items():
        assert file_digest(WB / rel) == expected, 'Protected file changed after intake: ' + rel
    for name, expected in plan['incoming'].items():
        assert file_digest(WB / INBOX / name) == expected['sha256']
    oldcat = json.loads((PAYLOAD / SESSION / 'SHARED_BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
    newcat = json.loads((WB / 'SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
    assert newcat['source_files'][:len(oldcat['source_files'])] == oldcat['source_files']
    assert STATUS.replace('\n', '  \n') in (WB / NOTE).read_text(encoding='utf-8')
    assert STATUS.replace('\n', '  \n') in (WB / '01_WORKSPACE_STATUS.md').read_text(encoding='utf-8')
    links = json.loads((ROOT / 'LINK_CHECK.json').read_text(encoding='utf-8'))
    assert all((WB / link['to']).exists() for link in links['links'])
    validation_path = WB / SESSION / 'VALIDATION.json'
    validation = json.loads(validation_path.read_text(encoding='utf-8'))
    validation.update({'published_and_read_back': True, 'resolved_local_links': links['resolved_links'],
                       'protected_files_unchanged': len(plan['protected']), 'incoming_files_unchanged': True,
                       'shared_before_hash_guards_passed': True, 'exact_requested_status_recorded': True,
                       'archive_copy_byte_identical': True, 'completed_at_utc': datetime.now(timezone.utc).isoformat()})
    write_json(validation_path, validation)
    write_json(ROOT / 'FINAL_VALIDATION.json', validation)
    print(json.dumps({'record': str(WB / NOTE), 'status': str(WB / '01_WORKSPACE_STATUS.md'), 'archive': str(WB / plan['zip_destination']), 'links_verified': links['resolved_links'], 'protected_unchanged': len(plan['protected']), 'status_exact': True}))

if __name__ == '__main__':
    {'prepare': prepare, 'publish': publish}[sys.argv[1]]()
