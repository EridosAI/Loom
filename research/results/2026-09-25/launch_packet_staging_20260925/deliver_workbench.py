"""Append a new reviewed-byte delivery only; no Git or source edits."""
import hashlib,json,pathlib,shutil
PROJECT=pathlib.Path(__file__).resolve().parent.parent
R=PROJECT/'exports/2026-09-25-first-commissioning-launch-packet-5f077481'
DELIVERY=PROJECT/'exports/2026-09-25-first-commissioning-launch-delivery-5f077481'
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
INBOX=(WB/'INBOX').resolve();assert INBOX.is_relative_to(WB)
DEST=(INBOX/'2026-09-25-first-commissioning-launch-packet-5f077481').resolve()
assert DEST.parent==INBOX and not DEST.exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
protected={p:sha(p) for p in (WB/'AGENTS.md',WB/'00_RESEARCH_MAP.md',WB/'01_WORKSPACE_STATUS.md',WB/'SOURCE_CATALOG.json',WB/'SOURCE_REGISTER.md')}
receipt=json.loads((DELIVERY/'PACKAGE_RECEIPT.json').read_bytes())
assert sha(DELIVERY/receipt['archive_name'])==receipt['sha256']
DEST.mkdir()
shutil.copytree(R,DEST/'FIRST_COMMISSIONING_LAUNCH_PACKET')
for p in DELIVERY.iterdir():
    if p.is_file():shutil.copyfile(p,DEST/p.name)
inventory=json.loads((R/'FILE_MANIFEST.json').read_bytes())
for name,row in inventory['files'].items():
    p=DEST/'FIRST_COMMISSIONING_LAUNCH_PACKET'/name
    assert p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],name
assert sha(DEST/'FIRST_COMMISSIONING_LAUNCH_PACKET/FILE_MANIFEST.json')==receipt['manifest_sha256']
assert sha(DEST/receipt['archive_name'])==receipt['sha256']
assert all(sha(p)==h for p,h in protected.items())
(DEST/'READ_ME_FIRST.md').write_text('''# First commissioning launch packet — proposed only

Read [the compact launch packet](FIRST_COMMISSIONING_LAUNCH_PACKET/FIRST_COMMISSIONING_LAUNCH_PACKET.md).
The [portable ZIP](FIRST_COMMISSIONING_LAUNCH_PACKET.zip) and [receipt](PACKAGE_RECEIPT.json) contain the same verified payload.

Canonical authority SHA-256: `a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc`.

No commissioning execution occurred. The manifest has no execution grant. Jason's explicit approval of the complete exact object is required before launch. One A1 only; maximum 120 simulated seconds. No source/status/canonical document was changed by this delivery.
''',encoding='utf-8')
copied={'destination':str(DEST),'zip_sha256':receipt['sha256'],'canonical_authority_sha256':receipt['canonical_authority_sha256'],
        'all_payloads_verified':True,'shared_navigation_and_source_indexes_unchanged':True,'git_writes':0,
        'commissioning_execution_occurred':False,'authority_status':'PROPOSED / NOT AUTHORIZED'}
(DEST/'WORKBENCH_DELIVERY_RECEIPT.json').write_text(json.dumps(copied,indent=2),encoding='utf-8')
(DELIVERY/'WORKBENCH_DELIVERY_RECEIPT.json').write_text(json.dumps(copied,indent=2),encoding='utf-8')
print(json.dumps(copied,indent=2))
