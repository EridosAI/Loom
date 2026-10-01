"""Archive and document intake only; no review or organism code is executed."""
import importlib.util
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parent
helper = ROOT.parent / '2026-09-23-p-post-correction-intake-1677619b/intake_documents.py'
spec = importlib.util.spec_from_file_location('document_intake_helpers', helper)
h = importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)
h.ROOT = ROOT
h.PAYLOAD = ROOT / 'PAYLOAD'
h.ID = '2026-09-23-p-final-r1p-intake-08df839e'
h.SESSION = '50_SESSIONS/' + h.ID
h.BATCH = '90_SOURCES/p_final_r1p_review_2026-09-23_08df839e'
h.NOTE = '30_REVIEWS/REVIEW-P-ENGINEERING-6bc9683b-2026-09-23-08df839e.md'
h.INBOX = 'INBOX/2026-09-23-P_Final_Independent_R1P_Review'
h.REPORT = 'LOOM_P_FINAL_INDEPENDENT_R1P_FIDELITY_REVIEW.md'
h.ZIP = 'Loom_P_Final_Independent_R1P_Review_6bc9683b_20260923.zip'
h.COMMIT = '6bc9683b54e4fa80136fe8534d7713e2a250a95f'
h.PREVIOUS = 'f7eb6f27c661e3db193a4225b56a825d7e41739d'
ORIGINAL = 'd5f7efbe67193f215e52d95ca912db131a79f31c'
HISTORY = '30_REVIEWS/P_ENGINEERING_HISTORY_2026-09-23-08df839e.md'
OLD_D5 = '50_SESSIONS/2026-09-23-p-engineering-review-284c3913/P_ENGINEERING_CHECKPOINT_REVIEW.md'
OLD_F7 = '30_REVIEWS/REVIEW-P-ENGINEERING-f7eb6f27-2026-09-23-1677619b.md'
h.STATUS = '\n'.join([
    'P engineering baseline',
    'Exact checkpoint: ' + h.COMMIT,
    'Mechanism fidelity: INDEPENDENTLY VERIFIED within reviewed scope',
    'Engineering status: FIT TO PROCEED TO COUPLING COMMISSIONING',
    'Scientific status: UNCOMMISSIONED / UNTESTED',
    '',
    'R1: Closed for demonstrated radial/oblique release-recontact class',
    'R2: Closed',
    'R3: Closed',
])
LIMITS = [
    'finite-step contact realization is not an exhaustive convergence proof',
    'sensory capacity remains provisional',
    'mean-plus-endpoint temporal packet remains lossy by construction',
    'receptor/packet adaptation may suppress sustained information',
    'associative regime is deliberately contracting',
    'effective learned signal magnitudes remain unknown',
    'shared equal-valued E/I configuration fields remain a known implementation limitation',
]
NO_EFFICACY = 'No scientific efficacy, developmental success, survival capability or ecological adequacy has yet been established.'
LIMIT_TEXT = 'Important retained limitations:\n\n' + '\n'.join('- ' + s for s in LIMITS) + '\n\n' + NO_EFFICACY + '\n'

def prepare():
    h.PAYLOAD.mkdir(exist_ok=False)
    before = {p: (h.WB / p).read_bytes() for p in h.SHARED}
    incoming = {h.ZIP: {'bytes': (h.WB / h.INBOX / h.ZIP).stat().st_size, 'sha256': h.file_digest(h.WB / h.INBOX / h.ZIP)}}
    assert incoming[h.ZIP]['sha256'] == 'c395141315a58a91be55d26034b2c97460caf840a01b9622c0317680015fcf2c'
    with zipfile.ZipFile(h.WB / h.INBOX / h.ZIP) as z:
        names = z.namelist()
        assert len(names) == len(set(names))
        assert all(not n.startswith(('/', '\\')) and '..' not in Path(n).parts and ':' not in n for n in names)
        retained = {name: z.read(name) for name in (h.REPORT, 'REVIEW_RECEIPT.json', 'FILE_MANIFEST.json')}
        manifest = json.loads(retained['FILE_MANIFEST.json'])
        receipt = json.loads(retained['REVIEW_RECEIPT.json'])
        assert set(names) == set(manifest) | {'FILE_MANIFEST.json'}
        checked = []
        for name, expected in manifest.items():
            with z.open(name) as stream:
                actual = h.hashlib.file_digest(stream, 'sha256').hexdigest()
            assert actual == expected['sha256'] and z.getinfo(name).file_size == expected['bytes'], name
            checked.append({'path': name, **expected})
        assert receipt['reviewed_checkpoint'] == h.COMMIT
        assert receipt['previous_checkpoint'] == h.PREVIOUS and receipt['original_checkpoint'] == ORIGINAL
        assert receipt['verdict'] == 'FIT TO PROCEED TO COUPLING COMMISSIONING'
        assert all(receipt[key] == 'VERIFIED' for key in ('R1P', 'R2', 'R3'))
        assert receipt['must_fix_findings'] == 0
        assert h.digest(retained[h.REPORT]) == receipt['report_sha256']
        delivery = manifest['reviewed_delivery/' + receipt['reviewed_delivery']['name']]
        assert delivery['sha256'] == receipt['reviewed_delivery']['sha256']
        assert delivery['bytes'] == receipt['reviewed_delivery']['bytes']
        # Check the exact preceding review identities carried by this package.
        for basename, expected in [
            ('LOOM_P_INDEPENDENT_POST_CORRECTION_FIDELITY_REVIEW.md', receipt['previous_independent_review_sha256']),
            ('LOOM_P_INDEPENDENT_FIDELITY_REVIEW.md', receipt['original_independent_review_sha256']),
        ]:
            matches = [v['sha256'] for k, v in manifest.items() if k.endswith('/' + basename)]
            assert matches == [expected], basename
    for name, data in retained.items():
        h.put(h.BATCH + '/' + name, data)
    for rel, data in before.items():
        h.put(h.SESSION + '/SHARED_BEFORE/' + rel, data)

    block = h.STATUS.replace('\n', '  \n')
    note = '# ' + block + '\n\n' + LIMIT_TEXT + '\n'
    note += f'[Full independent review](../{h.BATCH}/{h.REPORT}) · [Receipt](../{h.BATCH}/REVIEW_RECEIPT.json) · [Complete original package](../{h.BATCH}/{h.ZIP}).\n\n'
    note += 'Recorded under Jason’s 2026-09-23 intake instruction. Mechanism fidelity is attributed to the previous independent equation audit and the final review’s unchanged-identity/regression checks, within their reviewed scope. This intake performs source custody and status integration, not another code audit or test execution.\n\n'
    note += f'[Engineering-history branches](../{HISTORY}) preserve the preceding d5f7efbe and f7eb6f27 holds. This fitness disposition applies only to the exact 6bc9683b checkpoint; it does not change the historical findings. Commissioning remains a separate Jason-authorized task.\n\n'
    note += f'[Intake record and validation](../{h.SESSION}/INTAKE_RECORD.md).\n'
    h.put(h.NOTE, note)

    history = '# P engineering-history branches\n\nEach record retains the disposition established for its exact checkpoint. The earlier holds are preserved; the current fitness finding does not replace their status or turn any checkpoint into a scientific result. These are documentation records, not new Git branches.\n\n'
    history += '| Exact checkpoint | Preserved engineering status | Findings at that checkpoint | Record |\n|---|---|---|---|\n'
    history += f'| `{ORIGINAL}` | ENGINEERING HOLD | R1–R3 open; retained P mechanism independently verified within scope | [d5f7efbe review](../{OLD_D5}) |\n'
    history += f'| `{h.PREVIOUS}` | ENGINEERING HOLD | R1 original fixture closed; R1-P oblique class open; R2/R3 verified closed; mechanism fidelity unchanged / previously verified | [f7eb6f27 review](../{OLD_F7}) |\n'
    history += f'| `{h.COMMIT}` | FIT TO PROCEED TO COUPLING COMMISSIONING | R1 closed for demonstrated radial/oblique class; R2/R3 closed; mechanism fidelity independently verified within reviewed scope | [6bc9683b review](../{h.NOTE}) |\n\n'
    history += 'Scientific status for all three records: **UNCOMMISSIONED / UNTESTED**.\n\n'
    history += f'The final review records the checkpoint lineage d5f7efbe → f7eb6f27 → 6bc9683b. This intake does not recheck Git ancestry. [Retained limitations and claim boundary](../{h.NOTE}).\n'
    h.put(HISTORY, history)

    research_map = before['00_RESEARCH_MAP.md'].decode('utf-8-sig')
    old_heading = '## Current P engineering baseline — 2026-09-23'
    assert research_map.count(old_heading) == 1
    current_map = '## Current P engineering baseline — 2026-09-23\n\n'
    current_map += f'Exact checkpoint `{h.COMMIT}`: **FIT TO PROCEED TO COUPLING COMMISSIONING**. Mechanism fidelity **INDEPENDENTLY VERIFIED within reviewed scope**; scientific status **UNCOMMISSIONED / UNTESTED**. R1 closed for the demonstrated radial/oblique release-recontact class; R2 and R3 closed. [Full status and all retained limitations]({h.NOTE}) · [Engineering-history branches]({HISTORY}).\n\n'
    current_map += NO_EFFICACY + ' Commissioning remains a separate Jason-authorized task. The earlier checkpoint holds retain their exact historical status.\n\n'
    research_map = research_map.replace(old_heading, current_map + '## Preserved engineering-history branch — f7eb6f27', 1)
    assert '| engineering hold at f7eb6f27 |' in research_map
    research_map = research_map.replace('| engineering hold at f7eb6f27 |', '| fit to proceed to coupling commissioning at 6bc9683b |', 1)
    h.put('00_RESEARCH_MAP.md', research_map)

    status = before['01_WORKSPACE_STATUS.md'].decode('utf-8-sig')
    old_heading = '## Current engineering checkpoint — 2026-09-23'
    assert status.count(old_heading) == 1
    current_status = '## Current engineering checkpoint — 2026-09-23\n\n' + block + '\n\n' + LIMIT_TEXT + '\n'
    current_status += f'[Full review and exact status]({h.NOTE}) · [Preserved engineering-history branches]({HISTORY}) · [Intake record]({h.SESSION}/INTAKE_RECORD.md).\n\n'
    current_status += 'The d5f7efbe and f7eb6f27 checkpoint holds remain unchanged in their own records. This intake records engineering fitness only; no commissioning design, commissioning execution or scientific run is authorized or performed.\n\n'
    status = status.replace(old_heading, current_status + '## Preserved engineering-history branch — f7eb6f27', 1)
    h.put('01_WORKSPACE_STATUS.md', status)

    candidate = before['20_CANDIDATES/CAND-P.md'].decode('utf-8-sig')
    assert 'revision: r003' in candidate and 'engineering_checkpoint: ' + h.PREVIOUS in candidate
    candidate = candidate.replace('revision: r003', 'revision: r004', 1)
    candidate = candidate.replace('work_status: engineering-hold', 'work_status: fit-to-proceed-to-coupling-commissioning', 1)
    candidate = candidate.replace('engineering_checkpoint: ' + h.PREVIOUS, 'engineering_checkpoint: ' + h.COMMIT, 1)
    old_heading = '## Current engineering checkpoint — 2026-09-23'
    assert candidate.count(old_heading) == 1
    continuation = '## Current engineering checkpoint — 2026-09-23\n\n'
    continuation += f'`{h.COMMIT}`: **FIT TO PROCEED TO COUPLING COMMISSIONING**. Mechanism fidelity **INDEPENDENTLY VERIFIED within reviewed scope**. Scientific status **UNCOMMISSIONED / UNTESTED**. R1 closed for the demonstrated radial/oblique class; R2 and R3 closed. [Full status and retained limitations](../{h.NOTE}) · [Engineering-history branches](../{HISTORY}).\n\n'
    continuation += NO_EFFICACY + ' The complete P design remains unchanged. This status does not authorize commissioning.\n\n'
    candidate = candidate.replace(old_heading, continuation + '## Preserved engineering-history branch — f7eb6f27', 1)
    candidate += f'\n2026-09-23, {h.ID}: r004 records exact 6bc9683b engineering fitness with all limitations retained. d5f7efbe/f7eb6f27 records retain their holds. No candidate mechanism or scientific result changed.\n'
    h.put('20_CANDIDATES/CAND-P.md', candidate)

    catalog = json.loads(before['SOURCE_CATALOG.json'])
    old_rows = list(catalog['source_files'])
    start = max(int(row['source_id'].split('-')[1]) for row in old_rows) + 1
    rows = []
    for offset, name in enumerate((h.REPORT, h.ZIP, 'REVIEW_RECEIPT.json', 'FILE_MANIFEST.json')):
        identity = incoming[name] if name in incoming else {'bytes': len(retained[name]), 'sha256': h.digest(retained[name])}
        rows.append({'source_id': f'SRC-{start + offset:03}', 'path': h.BATCH + '/' + name, 'original_filename': name, **identity,
                     'role': 'independent-final-r1p-engineering-review' if name == h.REPORT else ('independent-review-delivery-archive' if name == h.ZIP else 'independent-review-custody-metadata'),
                     'authority': 'Independent scoped engineering-fitness review; scientific status uncommissioned/untested; no execution authority',
                     'prepared': '2026-09-23', 'stated_author': 'Independent reviewer; exact model/backend not stated in main report or receipt',
                     'acquired_from': h.INBOX + '/' + h.ZIP + ('' if name == h.ZIP else '::' + name),
                     'reviewed_checkpoint': h.COMMIT, 'previous_checkpoint': h.PREVIOUS, 'original_checkpoint': ORIGINAL,
                     'review_note': h.NOTE, 'history_index': HISTORY,
                     'notes': 'Byte-identical preservation. Complete nested delivery, prior reviews, scripts and logs remain in original ZIP; nothing executed.'})
    catalog['source_files'].extend(rows)
    catalog.setdefault('intake_events', []).append({'session_id': h.ID, 'source_ids': [r['source_id'] for r in rows], 'review_note': h.NOTE, 'history_index': HISTORY, 'record': h.SESSION + '/INTAKE_RECORD.md', 'scope': 'Jason-requested final review intake/status update; earlier engineering holds preserved; no scientific efficacy or execution authorization'})
    assert catalog['source_files'][:len(old_rows)] == old_rows
    h.put('SOURCE_CATALOG.json', json.dumps(catalog, ensure_ascii=False, indent=2) + '\n')
    register = before['SOURCE_REGISTER.md'].decode('utf-8-sig')
    register += '\n## P final independent R1-P review intake — 2026-09-23\n\n| ID | Source | Identity |\n|---|---|---|\n'
    for row in rows:
        register += f"| {row['source_id']} | [{row['original_filename']}]({row['path']}) | {row['bytes']} bytes; SHA-256 `{row['sha256']}` |\n"
    register += f'\nExact checkpoint `{h.COMMIT}`: **FIT TO PROCEED TO COUPLING COMMISSIONING** within the reviewed scope; scientific status **UNCOMMISSIONED / UNTESTED**. [Status and retained limitations]({h.NOTE}) · [Engineering-history branches]({HISTORY}) · [Intake validation]({h.SESSION}/INTAKE_RECORD.md). Prior source rows and checkpoint dispositions remain unchanged.\n'
    h.put('SOURCE_REGISTER.md', register)

    administrative = {Path(v['path']).name: h.digest(before[Path(v['path']).name]) == v['new_sha256'] for v in receipt['administrative_source_changes']}
    record = '# Final independent R1-P review intake — 2026-09-23\n\n'
    record += f'[Current checkpoint record](../../{h.NOTE}) · [Engineering-history branches](../../{HISTORY}) · [Live status](../../01_WORKSPACE_STATUS.md).\n\n'
    record += f'Ingested the original ZIP from `{h.INBOX}` under Jason’s current instruction. The session’s integration scope is this intake and the requested status/history navigation. The INBOX original is untouched; its byte-identical archive and extracted report/receipt/manifest are in `{h.BATCH}`.\n\n'
    record += f'Read the full main review, receipt and intake README, current Workbench instructions/map/status and P wrapper; inspected the source catalog/register and prior intake records. The review supports engineering fitness at `{h.COMMIT}`. R1 closure is limited to the demonstrated radial/oblique release-recontact class. All seven user-specified limitations and the explicit absence of established efficacy, developmental success, survival capability or ecological adequacy are retained in the live status and checkpoint record.\n\n'
    record += f'All {len(manifest)} manifest-listed members match sizes/SHA-256; {len(names)} ZIP members include the manifest itself. The report matches its receipt; the nested builder ZIP and both carried prior independent-review identities match their recorded hashes. Outer ZIP SHA-256: `{incoming[h.ZIP]["sha256"]}`. The external `ZIP_SHA256.txt` mentioned in the source was not included in this INBOX batch; this outer hash is computed custody evidence, not comparison with the absent sidecar. Supporting scripts and tests were not executed.\n\n'
    record += 'The review disclosed two administrative map/status changes from the preceding intake; both receipt hashes match this intake’s starting bytes. Those facts are preserved in the receipt. The new live navigation is another dated administrative update, not a rewrite of the source report.\n\n'
    record += f'Registered {", ".join(r["source_id"] for r in rows)}. Updated the map, live status, P navigation wrapper, source catalog and register. Previous complete shared-file bytes are in `SHARED_BEFORE/`; all {len(old_rows)} old catalog rows remain intact. New history navigation links the d5f7efbe and f7eb6f27 records with their original ENGINEERING HOLD dispositions; those review files and their existing intake/session evidence are unchanged. No Git branch was created or altered.\n\n'
    record += '[VALIDATION.json](VALIDATION.json) records archive/source checks, change guards, preserved history, local-link checks, status and limitations. No actual Loom repository, vault settings, decision history, candidate equations, scientific canon, Git operations, commissioning design, scientific runs or efficacy assessment were changed or performed. Commissioning remains a separate Jason-authorized task.\n'
    assert all(administrative.values()), administrative
    h.put(h.SESSION + '/INTAKE_RECORD.md', record)

    protected = {}
    history_roots = ['40_DECISIONS', '50_SESSIONS/2026-09-23-p-engineering-review-284c3913', '50_SESSIONS/2026-09-23-p-post-correction-intake-1677619b']
    for rel in history_roots:
        for p in (h.WB / rel).rglob('*'):
            if p.is_file():
                protected[p.relative_to(h.WB).as_posix()] = h.file_digest(p)
    for row in old_rows:
        p = h.WB / row['path']
        if p.is_file():
            protected[row['path']] = h.file_digest(p)
    for rel in ('AGENTS.md', '20_CANDIDATES/CAND-R.md', '02_OPEN_QUESTIONS.md', OLD_F7):
        protected[rel] = h.file_digest(h.WB / rel)
    validation = {'session_id': h.ID, 'created_at_utc': datetime.now(timezone.utc).isoformat(), 'reviewed_checkpoint': h.COMMIT,
                  'previous_checkpoint': h.PREVIOUS, 'original_checkpoint': ORIGINAL, 'incoming': incoming,
                  'archive_members': len(names), 'manifest_payloads_verified': len(manifest), 'report_matches_receipt': True,
                  'nested_delivery_hash_matches_receipt': True, 'carried_prior_review_identities_match': True,
                  'outer_zip_external_checksum_sidecar_supplied': False, 'old_catalog_rows_preserved': len(old_rows),
                  'administrative_receipt_matches_starting_bytes': administrative, 'source_ids': [r['source_id'] for r in rows],
                  'review_code_or_tests_executed': False, 'shared_files': h.SHARED, 'status_text': h.STATUS,
                  'retained_limitations': LIMITS, 'scientific_claim_boundary': NO_EFFICACY, 'manifest_validation': checked}
    h.put(h.SESSION + '/VALIDATION.json', json.dumps(validation, indent=2) + '\n')
    plan = {'shared_before': {p: h.digest(b) for p, b in before.items()}, 'protected': protected, 'incoming': incoming,
            'zip_destination': h.BATCH + '/' + h.ZIP,
            'staged_hashes': {p.relative_to(h.PAYLOAD).as_posix(): h.file_digest(p) for p in h.PAYLOAD.rglob('*') if p.is_file()}}
    h.write_json(ROOT / 'PLAN.json', plan)
    links = []
    for rel in h.SHARED[:-2] + ['SOURCE_REGISTER.md', h.NOTE, HISTORY, h.SESSION + '/INTAKE_RECORD.md']:
        text = (h.PAYLOAD / rel).read_text(encoding='utf-8')
        for target in re.findall(r'\]\(([^\n]+?)\)', text):
            target = unquote(target.split('#')[0].strip('<>'))
            if not target or '://' in target:
                continue
            logical = ((h.WB / rel).parent / target).resolve()
            destrel = logical.relative_to(h.WB.resolve()).as_posix()
            assert logical.exists() or (h.PAYLOAD / destrel).exists() or destrel == plan['zip_destination'], (rel, target)
            links.append({'from': rel, 'to': destrel})
    for rel in (h.NOTE, '01_WORKSPACE_STATUS.md'):
        text = (h.PAYLOAD / rel).read_text(encoding='utf-8')
        assert block in text and all(s in text for s in LIMITS) and NO_EFFICACY in text
    for rel in ('00_RESEARCH_MAP.md', '01_WORKSPACE_STATUS.md', '20_CANDIDATES/CAND-P.md'):
        text = (h.PAYLOAD / rel).read_text(encoding='utf-8')
        assert h.PREVIOUS in text and 'ENGINEERING HOLD' in text
    h.write_json(ROOT / 'LINK_CHECK.json', {'resolved_links': len(links), 'links': links})
    print(json.dumps({'prepared': h.ID, 'manifest_verified': len(manifest), 'archive_members': len(names), 'source_ids': validation['source_ids'], 'links': len(links), 'limitations': len(LIMITS), 'protected_records': len(protected)}))

def publish():
    h.publish()
    for rel in (h.NOTE, '01_WORKSPACE_STATUS.md'):
        text = (h.WB / rel).read_text(encoding='utf-8')
        assert all(s in text for s in LIMITS) and NO_EFFICACY in text
    validation_path = h.WB / h.SESSION / 'VALIDATION.json'
    validation = json.loads(validation_path.read_text(encoding='utf-8'))
    validation.update({'all_seven_limitations_read_back': True, 'no_efficacy_claim_boundary_read_back': True,
                       'preceding_checkpoint_statuses_preserved': {ORIGINAL: 'ENGINEERING HOLD', h.PREVIOUS: 'ENGINEERING HOLD'},
                       'engineering_history_index': HISTORY})
    h.write_json(validation_path, validation)
    h.write_json(ROOT / 'FINAL_VALIDATION.json', validation)

if __name__ == '__main__':
    {'prepare': prepare, 'publish': publish}[sys.argv[1]]()
