import hashlib, io, json, zipfile
from pathlib import Path
root=Path(__file__).resolve().parent
wb=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
outer_path=wb/'90_SOURCES/p_final_r1p_review_2026-09-23_08df839e/Loom_P_Final_Independent_R1P_Review_6bc9683b_20260923.zip'
with outer_path.open('rb') as f:
    assert hashlib.file_digest(f,'sha256').hexdigest()=='c395141315a58a91be55d26034b2c97460caf840a01b9622c0317680015fcf2c'
with zipfile.ZipFile(outer_path) as outer:
    data=outer.read('reviewed_delivery/Loom_P_R1P_corrective_review_20260923.zip')
assert hashlib.sha256(data).hexdigest()=='c1f2cd0ed8ebe09f3a9b07d087f6fe9f25ca62f3f61a827628802bc35e5fa322'
with zipfile.ZipFile(io.BytesIO(data)) as z:
    manifest=json.loads(z.read('ARTIFACT_MANIFEST.json'))
    (root/'INNER_MANIFEST_SHAPE.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    selected=[]
    for name in z.namelist():
        if name=='ARTIFACT_MANIFEST.json' or name=='developmental_ecology/configuration.json' or name.startswith('developmental_ecology/loom_p/') or (name.startswith('docs/') and name.endswith('.md')) or (name.startswith('review_inputs/') and name.endswith(('.md','.json'))) or (name.startswith('developmental_ecology/artifacts/smoke-') and name.endswith('/manifest.json')) or name.endswith('/prehistory-attempt-001/manifest.json'):
            b=z.read(name)
            p=root/'REFERENCE_READS'/name
            p.parent.mkdir(parents=True,exist_ok=True)
            p.write_bytes(b)
            selected.append({'path':name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
    (root/'READING_COPY_IDENTITIES.json').write_text(json.dumps({'outer_zip':str(outer_path),'outer_sha256':'c395141315a58a91be55d26034b2c97460caf840a01b9622c0317680015fcf2c','inner_member':'reviewed_delivery/Loom_P_R1P_corrective_review_20260923.zip','inner_sha256':hashlib.sha256(data).hexdigest(),'files':selected},indent=2),encoding='utf-8')
print(json.dumps({'reading_copies':len(selected),'manifest_type':type(manifest).__name__,'manifest_keys':list(manifest)[:6]}))
