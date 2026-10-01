"""Seal and verify prepared review files. No Loom imports or execution."""
import hashlib,json,os,pathlib,shutil,subprocess,sys,zipfile
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
P=ROOT/'exports/2026-09-25-A3-launch-packet-5f077481'
OUT=ROOT/'exports/2026-09-25-A3-launch-delivery-5f077481'
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
sys.path.insert(0,str(P))
from validate_packet import verify
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,v):p.write_text(json.dumps(v,ensure_ascii=False,allow_nan=False,indent=2)+'\n',encoding='utf-8')
before=json.loads((P/'HASH_BEFORE.json').read_bytes())
assert all(sha(p)==h for p,h in before.items()),'Original changed during review; inspect before seal'
env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
g=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(S/'empty-excludes').as_posix(),'-C',str(W)]
assert subprocess.check_output(g+['rev-parse','HEAD'],env=env).decode().strip()=='5f07748102cb5eaa302569c87efbae095050e9fe'
assert subprocess.check_output(g+['status','--porcelain'],env=env)==b''
m=json.loads((P/'A3_MANIFEST.json').read_bytes())
dest=pathlib.Path(m['execution']['procedure']['protocol']['record_destination'])
assert not dest.parent.exists()
shutil.copyfile(S/'empty-excludes',P/'empty-excludes')
shutil.copyfile(S/'seal_packet.py',P/'seal_packet.py')
h=(P/'AUTHORITY_SHA256.txt').read_text().split()[0]
disk=shutil.disk_usage(ROOT)
write(P/'LOCAL_CAPABILITY_RECORD.json',{'platform':'Actual desktop-local Windows; resolved code/workbench/project paths, not cloud execution',
    'Python':subprocess.check_output([sys.executable,'-B','--version']).decode().strip(),
    'Git':subprocess.check_output(['git','--version']).decode().strip(),
    'runtime_inventory':'CODE_AND_RUNTIME_IDENTITIES.json','scoped_temporary_write_read_delete':'passed in new packet folder only',
    'disk_free_bytes_at_seal':disk.free,'proposed_free_disk_precondition_bytes':3000000000,'disk_precondition_currently_met':disk.free>=3000000000,
    'execution_authority':'missing by design; preparation only','dependencies':'existing pinned Python/numpy/scipy identities checked; none installed',
    'code_worktree':'read only, unchanged clean branch/HEAD; no new worktree or code write needed',
    'prospective_A3_run_directory_absent':True,'future_execution_output_permission':'Normal sandbox approval for exact artifact output outside project root, only after genuine Jason execution authority',
    'background_processes_started':0,'viewer_inspector_servers_started':0})
files={p.relative_to(P).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(P.rglob('*')) if p.is_file() and p.name!='FILE_MANIFEST.json'}
write(P/'FILE_MANIFEST.json',{'authority_status':'PROPOSED / NOT AUTHORIZED','authority_sha256':h,'files':files})
result=verify(lambda n:(P/n).read_bytes(),[p.relative_to(P).as_posix() for p in P.rglob('*') if p.is_file()])
OUT.mkdir(exist_ok=False)
zpath=OUT/'A3_LAUNCH_PACKET.zip'
with zipfile.ZipFile(zpath,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(P.rglob('*')):
        if p.is_file():z.write(p,'A3_LAUNCH_PACKET/'+p.relative_to(P).as_posix())
with zipfile.ZipFile(zpath) as z:
    prefix='A3_LAUNCH_PACKET/'
    zr=verify(lambda n:z.read(prefix+n),[n[len(prefix):] for n in z.namelist()])
assert result==zr
assert all(sha(p)==v for p,v in before.items()) and not dest.parent.exists()
receipt={'packet':'A3_LAUNCH_PACKET.zip','bytes':zpath.stat().st_size,'sha256':sha(zpath),'authority_sha256':h,
    'authority_status':'PROPOSED / NOT AUTHORIZED','folder_validation':result,'zip_validation':zr,
    'original_files_rechecked':len(before),'original_files_unchanged':True,'Git_clean_and_HEAD_unchanged':True,
    'prospective_run_directory_absent':True,'execution_occurred':False,'unexecuted_world_steps':0,
    'whole_task_instantaneous_zero_time_sensor_evaluations':2,'preparation_history':'preparation-history/PREPARATION_HISTORY.md'}
write(OUT/'DELIVERY_RECEIPT.json',receipt)
print(json.dumps(receipt,indent=2))
