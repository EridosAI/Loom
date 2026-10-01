"""Package already reviewed PC evidence and explicit assessment addendum only."""
import datetime,hashlib,json,zipfile
from pathlib import Path
S=Path(__file__).resolve().parent;ROOT=S.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
receipt=read(S/'REVIEW_PACKAGE_RECEIPT.json')
old=Path(receipt['path']);assert sha(old.read_bytes())==receipt['sha256']
assert read(S/'SEQUENCE_STATE.json')['live_services']==0
assert read(S/'PC-HOLD-attempt-002/RESULT.json')['physical_gentle_hold_target_met']
data={}
with zipfile.ZipFile(old) as z:
    assert z.testzip() is None
    for name in z.namelist():data['historical-original-review/'+name]=z.read(name)
for name in ('POSITIVE_CONTROL_REVIEW_ADDENDUM.md','PC-CONTACT.ASSESSMENT_CORRECTION.json',
    'SEQUENCE_STATE.json','review_pc_hold_repeat_and_contact.py',
    'prepare_pc_hold_attempt_002.py','package_positive_control_addendum.py'):
    data[name]=(S/name).read_bytes()
for folder,prefix in ((S/'PC-HOLD-attempt-002','PC-HOLD-attempt-002/metadata'),
                      (S/'runs/PC-HOLD-attempt-002','PC-HOLD-attempt-002/records')):
    for p in sorted(folder.iterdir()):
        if p.is_file():data[prefix+'/'+p.name]=p.read_bytes()
manifest=dict(schema=1,recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    scope='Positive-control evidence only; passive review. This package does not authorize any launch; no B1 archive included.',
    prior_package_sha256=receipt['sha256'],
    current_status_document='POSITIVE_CONTROL_REVIEW_ADDENDUM.md',
    files={n:dict(bytes=len(b),sha256=sha(b)) for n,b in sorted(data.items())})
data['PACKAGE_FILE_MANIFEST.json']=(json.dumps(manifest,indent=2)+'\n').encode()
out=ROOT/'exports/2026-09-27-positive-controls-review-updated.zip'
assert not out.exists()
with zipfile.ZipFile(out,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name,b in sorted(data.items()):z.writestr(name,b)
with zipfile.ZipFile(out) as z:
    assert z.testzip() is None and set(z.namelist())==set(data)
    for n,b in data.items():assert z.read(n)==b
assert sha(old.read_bytes())==receipt['sha256']
result=dict(path=str(out),bytes=out.stat().st_size,sha256=sha(out.read_bytes()),file_count=len(data),
    all_archived_hashes_verified=True,prior_package_unchanged=True,
    B1_state_accessed=False,additional_world_steps=0,production_code_changes=0)
with (S/'REVIEW_ADDENDUM_PACKAGE_RECEIPT.json').open('x',encoding='utf-8') as f:json.dump(result,f,indent=2);f.write('\n')
print(json.dumps(result,indent=2))
