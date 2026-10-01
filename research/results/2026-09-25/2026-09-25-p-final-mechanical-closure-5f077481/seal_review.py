"""First seal only; writes beside this file and independently reopens the ZIP."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
NAME='Loom_P_Final_Mechanical_Closure_Review_5f077481_20260925.zip'
DEST=R/NAME
for name in (NAME,'FILE_MANIFEST.json','INTAKE_RECEIPT.json'):assert not (R/name).exists(),name
def sha(data):return hashlib.sha256(data).hexdigest()
def included(p):
    parts=p.relative_to(R).parts
    if parts[0] in ('portable','worktree-temp-001','portable-temp-001'):return False
    if any(x.endswith('-RED-temp') or x.endswith('-GREEN-temp') or x=='__pycache__' for x in parts[:-1]):return False
    return p.is_file() and p.name not in (NAME,'FILE_MANIFEST.json','INTAKE_RECEIPT.json')
files=[]
for p in sorted(p for p in R.rglob('*') if included(p)):
    data=p.read_bytes();files.append({'path':p.relative_to(R).as_posix(),'bytes':len(data),'sha256':sha(data)})
names={x['path'] for x in files}
for folder,count in [('previous-16-pairs-001',16),('previous-20-pairs-001',20),('new-18-pairs-001',18)]:
    for colour in ('RED','GREEN'):
        assert sum(n.startswith(folder+'/') and n.endswith('-'+colour+'.log') and n.count('/')==1 for n in names)==count
builder=next(x for x in files if x['path']=='reviewed_delivery/Loom_P_Final_Apparatus_Correction_Review_20260925.zip')
assert builder['bytes']==61132733 and builder['sha256']=='c0c0a0c426ff85c5fbf848ad34bba543218ff4420ebf9c573bc66737f6a34fcf'
manifest={'schema':1,'scope':'Final independent mechanical closure; no commissioning authorization','files':files}
with (R/'FILE_MANIFEST.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(manifest,f,indent=2)
with zipfile.ZipFile(DEST,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for item in files:z.write(R/item['path'],item['path'],compress_type=zipfile.ZIP_STORED if item['path'].endswith('.zip') else zipfile.ZIP_DEFLATED)
    z.write(R/'FILE_MANIFEST.json','FILE_MANIFEST.json')
with zipfile.ZipFile(DEST) as z:
    members=z.namelist();assert len(members)==len(set(members))==len(files)+1
    assert set(members)==names|{'FILE_MANIFEST.json'} and z.testzip() is None
    for name in members:
        p=PurePosixPath(name);assert not p.is_absolute() and '..' not in p.parts and '\\' not in name and ':' not in name
    assert json.loads(z.read('FILE_MANIFEST.json'))==manifest
    for item in files:
        data=z.read(item['path']);assert len(data)==item['bytes'] and sha(data)==item['sha256'],item['path']
receipt={'file':NAME,'bytes':DEST.stat().st_size,'sha256':sha(DEST.read_bytes()),'entries':len(files)+1,
 'manifest_payload_files':len(files),'safe_unique_paths':True,'CRC_verified':True,'all_payload_sizes_sha256_verified':True,
 'all_108_delivered_fault_logs_included':True,'builder_zip_byte_identical':True,
 'disposition':'FIT TO BEGIN AUTHORIZED COUPLING COMMISSIONING','commissioning_authorized_by_review':False}
with (R/'INTAKE_RECEIPT.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt,indent=2))
