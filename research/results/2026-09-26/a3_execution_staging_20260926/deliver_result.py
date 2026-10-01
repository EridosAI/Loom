"""Copy sealed stopped-A3 result into one new workbench INBOX delivery."""
import hashlib,json,pathlib,shutil
ROOT=pathlib.Path(__file__).resolve().parent.parent
SRC=ROOT/'exports/2026-09-26-A3-commissioning-result-5f077481'
DEST=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX\2026-09-26-A3-commissioning-result-5f077481')
BASE=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\commissioning-A3-20260925-5f077481')
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def total(p):return sum(f.stat().st_size for f in p.rglob('*') if f.is_file())
receipt=json.loads((SRC/'DELIVERY_RECEIPT.json').read_bytes())
assert receipt['authority_sha256']=='43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd'
assert sha(SRC/'A3_COMMISSIONING_RESULT.zip')==receipt['sha256']
assert total(BASE)+2*total(SRC)<3000000000
assert not DEST.exists() and DEST.parent.is_dir()
shutil.copytree(SRC,DEST)
payload=DEST/'A3_COMMISSIONING_RESULT';fm=json.loads((payload/'FILE_MANIFEST.json').read_bytes())
for n,v in fm['files'].items():
    p=payload/n;assert sha(p)==v['sha256'] and p.stat().st_size==v['bytes'],n
assert sha(SRC/'A3_COMMISSIONING_RESULT/FILE_MANIFEST.json')==sha(payload/'FILE_MANIFEST.json')
assert sha(DEST/'A3_COMMISSIONING_RESULT.zip')==receipt['sha256']
report={'destination':str(DEST),'verified_payloads':len(fm['files']),'zip_sha256':receipt['sha256'],'authority_sha256':receipt['authority_sha256'],
        'primary_and_all_delivery_bytes':total(BASE)+total(SRC)+total(DEST),'disk_budget_bytes':3000000000,
        'new_world_steps':0,'scope':'Copy of stopped evidence and read-only report; no prior files, shared navigation or Git changed.'}
(DEST/'COPY_VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
