import hashlib,json,sys
from pathlib import Path
root=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\developmental_ecology')
out=root/'artifacts/r1p-correction-20260923-01a0c405'
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
existing={p.relative_to(root/'artifacts').as_posix():dict(bytes=p.stat().st_size,sha256=sha(p)) for p in (root/'artifacts').rglob('*') if p.is_file()}
out.mkdir(exist_ok=False)
(out/'PRESERVED_ARTIFACTS_BEFORE.json').write_text(json.dumps(existing,indent=2),encoding='utf-8')
paths=list((root/'loom_p').glob('*.py'))+list((root/'tests').glob('*.py'))+[root/'configuration.json']
(out/'BASELINE_FILE_HASHES.json').write_text(json.dumps({p.relative_to(root).as_posix():sha(p) for p in paths},indent=2),encoding='utf-8')
inputs={
 'CORRECTION_AUTHORITY.txt':Path(r'C:\Users\Jason\.codex\attachments\ea68d13a-ba3d-4951-95b6-1c626e91db8e\Pasted text.txt'),
 'LOOM_P_INDEPENDENT_POST_CORRECTION_FIDELITY_REVIEW.md':Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-23-p-post-correction-review-f7eb6f27\LOOM_P_INDEPENDENT_POST_CORRECTION_FIDELITY_REVIEW.md')}
for name,p in inputs.items(): (out/name).write_bytes(p.read_bytes())
print('Preserved inventory:',len(existing),'files; local Python',sys.version)
