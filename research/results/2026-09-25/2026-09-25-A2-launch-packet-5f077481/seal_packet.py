"""Seal/verify review artifacts only. No Loom imports or execution."""
import hashlib,json,pathlib,shutil,sys,zipfile
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
P=ROOT/'exports/2026-09-25-A2-launch-packet-5f077481'
OUT=ROOT/'exports/2026-09-25-A2-launch-delivery-5f077481'
sys.path.insert(0,str(P))
from validate_packet import verify
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,allow_nan=False,indent=2)+'\n',encoding='utf-8')
before=json.loads((P/'HASH_BEFORE.json').read_bytes())
assert all(sha(p)==h for p,h in before.items()),'Reference changed during packet preparation; inspect before seal'
shutil.copyfile(S/'empty-excludes',P/'empty-excludes')
shutil.copyfile(S/'seal_packet.py',P/'seal_packet.py')
h=(P/'AUTHORITY_SHA256.txt').read_text().split()[0]
disk=shutil.disk_usage(ROOT)
write(P/'LOCAL_CAPABILITY_RECORD.json',{'platform':'Actual desktop-local Windows paths, not a cloud/session simulation','Python':'3.13.5','Git':'2.50.0.windows.1','runtime_inventory':'CODE_AND_RUNTIME_IDENTITIES.json','scoped_temporary_write_read_delete':'passed in new packet folder only','disk_free_bytes_at_seal':disk.free,'proposed_free_disk_precondition_bytes':3000000000,'disk_precondition_currently_met':disk.free>=3000000000,'execution_authority':'missing by design; Jason has authorized preparation only','dependencies':'existing pinned local runtime verified; none installed','code_worktree_access':'read only; no write needed or attempted','future_execution_output_write_access':'requires normal sandbox approval for exact new artifact destination outside project writable root, after genuine Jason execution approval','background_processes_started':0})
files={p.relative_to(P).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(P.rglob('*')) if p.is_file() and p.name!='FILE_MANIFEST.json'}
write(P/'FILE_MANIFEST.json',{'authority_status':'PROPOSED / NOT AUTHORIZED','authority_sha256':h,'files':files})
result=verify(lambda n:(P/n).read_bytes(),[p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file()])
OUT.mkdir(exist_ok=False)
zpath=OUT/'A2_LAUNCH_PACKET.zip'
with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(P.rglob('*')):
        if p.is_file():z.write(p,'A2_LAUNCH_PACKET/'+p.relative_to(P).as_posix())
with zipfile.ZipFile(zpath) as z:
    prefix='A2_LAUNCH_PACKET/'
    zr=verify(lambda n:z.read(prefix+n),[n[len(prefix):] for n in z.namelist()])
assert result==zr
receipt={'packet':'A2_LAUNCH_PACKET.zip','bytes':zpath.stat().st_size,'sha256':sha(zpath),'authority_sha256':h,'authority_status':'PROPOSED / NOT AUTHORIZED','folder_validation':result,'zip_validation':zr,'original_files_rechecked':len(before),'original_files_unchanged':all(sha(p)==v for p,v in before.items()),'execution_occurred':False}
write(OUT/'DELIVERY_RECEIPT.json',receipt)
print(json.dumps(receipt,indent=2))
