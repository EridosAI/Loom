from pathlib import Path, PurePosixPath
import json, hashlib, zipfile, stat
W=Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97')
O=W/'exports/2026-09-26-b1-review-352f73ff';DEST=O/'portable'
SRC=W/'exports/2026-09-26-B1-operator-correction-352f73ff-review-02/B1_OPERATOR_APPARATUS_CORRECTION_REVIEW.zip'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
assert SRC.stat().st_size==27546035
assert sha(SRC)=='0166f1395e9f10fba96e05f5d53264ba2fc275db2122087810406107e3ccf318'
with zipfile.ZipFile(SRC) as z:
    infos=z.infolist();names=[i.filename for i in infos];prefix='B1_OPERATOR_APPARATUS_CORRECTION_REVIEW/'
    assert len(names)==len(set(names))==len({n.casefold() for n in names})
    for i in infos:
        p=PurePosixPath(i.filename)
        assert i.filename.startswith(prefix) and not p.is_absolute() and '..' not in p.parts
        assert ':' not in i.filename and '\\' not in i.filename and not stat.S_ISLNK(i.external_attr>>16)
    manifest_raw=z.read(prefix+'PAYLOAD_MANIFEST.json');manifest=json.loads(manifest_raw);files=manifest['files']
    assert set(names)=={prefix+n for n in files}|{prefix+'PAYLOAD_MANIFEST.json'}
    for n,v in files.items():
        raw=z.read(prefix+n)
        assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['sha256'],n
    assert z.testzip() is None
    assert not DEST.exists();DEST.mkdir()
    for i in infos:
        p=DEST.joinpath(*PurePosixPath(i.filename[len(prefix):]).parts)
        assert p.resolve().is_relative_to(DEST.resolve())
        p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f:f.write(z.read(i))
receipt={'archive':str(SRC),'sha256':sha(SRC),'bytes':SRC.stat().st_size,'entries':len(names),'payloads_verified':len(files),'payload_bytes':sum(v['bytes'] for v in files.values()),'manifest_sha256':hashlib.sha256(manifest_raw).hexdigest(),'CRC_verified':True,'safe_paths_and_duplicate_checks':True,'extraction_prefix_removed':prefix,'destination':str(DEST),'suite_root':str(DEST/'source/developmental_ecology')}
(O/'provenance/ZIP.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
