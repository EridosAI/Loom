"""Passive package-byte verification only. No P/world/controller imports."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_bytes())
for name,identity in manifest['files'].items():
    path=root/name
    if not path.is_file() or path.stat().st_size!=identity['bytes']:raise ValueError(name)
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    if h.hexdigest()!=identity['sha256']:raise ValueError(name)
print('Verified',len(manifest['files']),'files; zero simulation or controller execution.')
