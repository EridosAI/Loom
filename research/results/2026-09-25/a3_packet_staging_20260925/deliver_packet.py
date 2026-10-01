"""Copy only sealed A3 review files to one new authorized INBOX folder."""
import hashlib,json,pathlib,shutil
ROOT=pathlib.Path(__file__).resolve().parent.parent
PACKET=ROOT/'exports/2026-09-25-A3-launch-packet-5f077481'
DEL=ROOT/'exports/2026-09-25-A3-launch-delivery-5f077481'
DEST=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX\2026-09-25-A3-launch-packet-5f077481')
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
receipt=json.loads((DEL/'DELIVERY_RECEIPT.json').read_bytes())
assert receipt['authority_sha256']=='43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd'
assert sha(DEL/'A3_LAUNCH_PACKET.zip')==receipt['sha256']=='4c580299d098ad26eb5c6be4dd98e4e26e1fb8e4c766fa8591d516fdb6fdcfce'
assert not DEST.exists()
assert DEST.parent.is_dir() and DEST.parent.name=='INBOX'
DEST.mkdir(exist_ok=False)
for n in ('A3_LAUNCH_PACKET.zip','DELIVERY_RECEIPT.json'):
    shutil.copyfile(DEL/n,DEST/n);assert sha(DEL/n)==sha(DEST/n)
shutil.copytree(PACKET,DEST/'A3_LAUNCH_PACKET')
fm=json.loads((PACKET/'FILE_MANIFEST.json').read_bytes())
for n,v in fm['files'].items():
    p=DEST/'A3_LAUNCH_PACKET'/n;assert sha(p)==v['sha256'] and p.stat().st_size==v['bytes'],n
assert sha(PACKET/'FILE_MANIFEST.json')==sha(DEST/'A3_LAUNCH_PACKET/FILE_MANIFEST.json')
result={'destination':str(DEST),'copied_payloads_verified':len(fm['files']),'zip_sha256':receipt['sha256'],
    'authority_sha256':receipt['authority_sha256'],'authority_status':'PROPOSED / NOT AUTHORIZED','execution_occurred':False,
    'scope':'New INBOX delivery only; no shared navigation, existing sources, code or Git changes'}
(DEST/'COPY_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
