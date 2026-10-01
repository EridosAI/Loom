from pathlib import Path, PurePosixPath
import json, hashlib, zipfile, stat
W=Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97')
OUT=W/'exports/2026-09-26-p-clock-final-review-68db2c58'
SRC=W/'exports/2026-09-26-A5-clock-correction/Loom_P_Clock_Correction_Review_20260926.zip'
DEST=OUT/'portable'
raw=SRC.read_bytes(); sha=hashlib.sha256(raw).hexdigest()
assert sha=='8c5e9322d06b4915ed31106770aff80e925666d961e389102c27a9ad4499e894'
assert len(raw)==3916030
with zipfile.ZipFile(SRC) as z:
    assert z.testzip() is None
    infos=z.infolist(); names=[i.filename for i in infos]
    assert len(names)==len(set(names))
    assert len(names)==len({n.casefold() for n in names})
    for i in infos:
        p=PurePosixPath(i.filename)
        assert not p.is_absolute() and '..' not in p.parts and ':' not in i.filename and '\\' not in i.filename
        assert not stat.S_ISLNK(i.external_attr>>16)
    manifest=json.loads(z.read('ARTIFACT_MANIFEST.json'))
    files=manifest['files']
    assert set(names)==set(files)|{'ARTIFACT_MANIFEST.json'}
    for n,m in files.items():
        data=z.read(n)
        assert len(data)==m['bytes'] and hashlib.sha256(data).hexdigest()==m['sha256'], n
    assert not DEST.exists()
    DEST.mkdir()
    for i in infos:
        p=DEST.joinpath(*PurePosixPath(i.filename).parts)
        assert p.resolve().is_relative_to(DEST.resolve())
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as f: f.write(z.read(i))
receipt={'source':str(SRC),'sha256':sha,'bytes':len(raw),'entries':len(names),'manifest_payloads_verified':len(files),'CRC':'pass','safe_names':'pass','destination':str(DEST),'suite_root':str(DEST/'developmental_ecology')}
(OUT/'provenance/ZIP.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
