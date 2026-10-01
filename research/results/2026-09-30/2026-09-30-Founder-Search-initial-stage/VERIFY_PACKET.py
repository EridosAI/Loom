"""Verify the extracted launch packet only; no simulation imports."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_bytes())
for name,expected in manifest['files'].items():
    p=root/name
    if not p.is_file() or p.stat().st_size!=expected['bytes']:raise ValueError(name)
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    if h.hexdigest()!=expected['sha256']:raise ValueError(name)
index=json.loads((root/'AUTHORITY_INDEX.json').read_bytes())
for a in index['authorities']:
    if hashlib.sha256((root/a['path']).read_bytes()).hexdigest()!=a['authority_sha256']:raise ValueError(a['life_id'])
print('Verified',len(manifest['files']),'files and twelve proposed authorities; zero simulation.')
