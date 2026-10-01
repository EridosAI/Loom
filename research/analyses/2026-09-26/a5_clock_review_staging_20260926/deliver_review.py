"""Deliver only the already prepared diagnosis documents to a new INBOX folder."""
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT/'exports/2026-09-26-A5-clock-compatibility-review-5f077481'
ZIP = SOURCE.with_suffix('.zip')
INBOX = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX').resolve()
DEST = INBOX/'2026-09-26-A5-clock-compatibility-review-5f077481'
EXPECTED_ZIP = '4419dede7014c86b9063c045ce62195494621aae9892604383f86d4cb5ffad44'

def identity(p):
    with p.open('rb') as f:
        h = hashlib.file_digest(f,'sha256').hexdigest()
    return {'sha256':h,'bytes':p.stat().st_size}

assert DEST.resolve().parent == INBOX and not DEST.exists()
assert identity(ZIP)['sha256'] == EXPECTED_ZIP
files = json.loads((SOURCE/'FILE_MANIFEST.json').read_bytes())['files']
assert all(identity(SOURCE/n) == v for n,v in files.items())
assert set(p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob('*') if p.is_file()) == set(files)|{'FILE_MANIFEST.json'}
with zipfile.ZipFile(ZIP) as z:
    assert z.testzip() is None
DEST.mkdir()
BUNDLE = DEST/'A5_CLOCK_COMPATIBILITY_REVIEW'
shutil.copytree(SOURCE,BUNDLE)
archive = DEST/'A5_CLOCK_COMPATIBILITY_REVIEW.zip'
shutil.copyfile(ZIP,archive)
assert all(identity(BUNDLE/n) == v for n,v in files.items())
assert identity(BUNDLE/'FILE_MANIFEST.json') == identity(SOURCE/'FILE_MANIFEST.json')
assert identity(archive)['sha256'] == EXPECTED_ZIP
(DEST/'A5_CLOCK_COMPATIBILITY_REVIEW.zip.sha256').write_text(EXPECTED_ZIP+'  '+archive.name+'\n',encoding='ascii')
receipt = {
    'purpose':'Delivery of diagnosis only; no simulation, production patch or authority object.',
    'report':str(BUNDLE/'A5_CLOCK_COMPATIBILITY_REVIEW.md'),
    'archive':str(archive), 'archive_identity':identity(archive),
    'payload_files_verified':len(files),
    'file_manifest_sha256':identity(BUNDLE/'FILE_MANIFEST.json')['sha256'],
    'destination_was_new':True, 'existing_workbench_files_modified':False,
    'Git_operations':False, 'world_evolution':False,
    'status':'Diagnosis complete; stop for Jason decision.'}
(DEST/'DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
print(json.dumps(receipt,indent=2))
