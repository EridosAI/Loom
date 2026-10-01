"""Create and independently reopen the first intake ZIP. Writes only beside this script."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent
NAME='Loom_P_Final_Independent_Apparatus_Correction_Review_9d31e790_20260925.zip'
DEST=ROOT/NAME
assert not DEST.exists()
assert not (ROOT/'INTAKE_RECEIPT.json').exists()
assert not (ROOT/'FILE_MANIFEST.json').exists()
def sha(data):return hashlib.sha256(data).hexdigest()
def included(path):
    parts=path.relative_to(ROOT).parts
    if parts[0] in ('portable','worktree-temp-001','portable-temp-001'):return False
    if any(p.endswith('-RED-temp') or p.endswith('-GREEN-temp') or p=='__pycache__' for p in parts[:-1]):return False
    return path.is_file() and path.name not in (NAME,'INTAKE_RECEIPT.json','FILE_MANIFEST.json')
files=sorted(p for p in ROOT.rglob('*') if included(p))
entries=[]
for p in files:
    data=p.read_bytes();entries.append({'path':p.relative_to(ROOT).as_posix(),'bytes':len(data),'sha256':sha(data)})
names={e['path'] for e in entries}
for folder,count in [('old-pairs-001',16),('new-pairs-001',20)]:
    for colour in ['RED','GREEN']:
        assert sum(n.startswith(folder+'/') and n.endswith('-'+colour+'.log') and n.count('/')==1 for n in names)==count
builder=next(e for e in entries if e['path']=='reviewed_delivery/Loom_P_Apparatus_Correction_Review_20260924.zip')
assert builder['sha256']=='e261dbb9836a916f3ff4b6daa3ae8d9c21ea12194198d1ed63dfa7ee9b798a81' and builder['bytes']==20202546
manifest={'schema':1,'scope':'Independent apparatus review intake only; no commissioning authority','files':entries}
with (ROOT/'FILE_MANIFEST.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(manifest,f,indent=2)
with zipfile.ZipFile(DEST,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for e in entries:
        compression=zipfile.ZIP_STORED if e['path'].endswith('.zip') else zipfile.ZIP_DEFLATED
        z.write(ROOT/e['path'],e['path'],compress_type=compression)
    z.write(ROOT/'FILE_MANIFEST.json','FILE_MANIFEST.json')
with zipfile.ZipFile(DEST) as z:
    member_names=z.namelist();assert len(member_names)==len(set(member_names))==len(entries)+1
    assert set(member_names)==names|{'FILE_MANIFEST.json'}
    assert z.testzip() is None
    for name in member_names:
        pp=PurePosixPath(name);assert not pp.is_absolute() and '..' not in pp.parts and '\\' not in name and ':' not in name
    recorded=json.loads(z.read('FILE_MANIFEST.json'));assert recorded==manifest
    for e in recorded['files']:
        data=z.read(e['path']);assert len(data)==e['bytes'] and sha(data)==e['sha256'],e['path']
receipt={'file':NAME,'bytes':DEST.stat().st_size,'sha256':sha(DEST.read_bytes()),'entries':len(entries)+1,'manifest_payload_files':len(entries),
 'safe_unique_paths':True,'CRC_verified':True,'all_payload_sizes_and_sha256_verified':True,'all_72_delivered_fault_logs_included':True,
 'corrected_builder_zip_byte_identical':True,'disposition':'HOLD BEFORE COUPLING COMMISSIONING','commissioning_authorized':False}
with (ROOT/'INTAKE_RECEIPT.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,indent=2)
print(json.dumps(receipt,indent=2))
