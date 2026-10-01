"""Seal new independent review; reopen and validate every included payload."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
NAME='Loom_P_Narrow_Final_Clock_Review_68db2c58_20260926.zip'
DEST=R/NAME
EXTERNAL={NAME,NAME+'.sha256','FILE_MANIFEST.json','INTAKE_RECEIPT.json'}
for name in EXTERNAL:assert not (R/name).exists(),name
def sha(raw):return hashlib.sha256(raw).hexdigest()
def include(p):
    parts=p.relative_to(R).parts
    if parts[0]=='portable':return False
    if any(x in ('worktree-suite-temp','portable-suite-temp','__pycache__') or x.endswith(('-RED-temp','-GREEN-temp')) for x in parts[:-1]):return False
    return p.is_file() and p.name not in EXTERNAL
files=[]
for p in sorted(p for p in R.rglob('*') if include(p)):
    data=p.read_bytes();files.append(dict(path=p.relative_to(R).as_posix(),bytes=len(data),sha256=sha(data)))
names={x['path'] for x in files}
for folder,n in [('apparatus-faults',16),('correction-faults',20),('final-faults',18),('clock-faults',5)]:
    for colour in ('RED','GREEN'):
        assert sum(name.startswith('regression/'+folder+'/') and name.endswith('-'+colour+'.log') and name.count('/')==2 for name in names)==n
for name in ('LOOM_P_NARROW_FINAL_CLOCK_REVIEW.md','CLOSURE_TABLE.md','REVIEWED_IDENTITIES.json','REPRODUCTION_COMMANDS.md',
             'scheduling/old-a.log','scheduling/old-b.log','scheduling/new.log','scheduling/STATIC_A5_HOLDS.json',
             'provenance/FINAL_PRESERVATION.json','provenance/FIXTURE_SEMANTICS.json',
             'continuity/check_source_preservation_attempt001.py','continuity/SOURCE_PRESERVATION.log'):
    assert name in names,name
assert len([n for n in names if n.startswith('continuity/fixtures-') and n.endswith('/RESULT.json')])==1
builder=next(x for x in files if x['path']=='reviewed_delivery/Loom_P_Clock_Correction_Review_20260926.zip')
assert builder['bytes']==3916030 and builder['sha256']=='8c5e9322d06b4915ed31106770aff80e925666d961e389102c27a9ad4499e894'
manifest={'schema':1,'scope':'Narrow final clock correction review; no A5 execution, new authority or packet regeneration','files':files}
with (R/'FILE_MANIFEST.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(manifest,f,indent=2)
with zipfile.ZipFile(DEST,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for entry in files:
        archive.write(R/entry['path'],entry['path'],compress_type=zipfile.ZIP_STORED if entry['path'].endswith('.zip') else zipfile.ZIP_DEFLATED)
    archive.write(R/'FILE_MANIFEST.json','FILE_MANIFEST.json')
with zipfile.ZipFile(DEST) as archive:
    members=archive.namelist()
    assert len(members)==len(set(members))==len(files)+1
    assert len(members)==len({n.casefold() for n in members})
    assert set(members)==names|{'FILE_MANIFEST.json'} and archive.testzip() is None
    for name in members:
        path=PurePosixPath(name);assert not path.is_absolute() and '..' not in path.parts and '\\' not in name and ':' not in name
    assert json.loads(archive.read('FILE_MANIFEST.json'))==manifest
    for entry in files:
        raw=archive.read(entry['path'])
        assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],entry['path']
receipt=dict(file=NAME,bytes=DEST.stat().st_size,sha256=sha(DEST.read_bytes()),entries=len(files)+1,
    manifest_payload_files=len(files),safe_unique_paths=True,CRC_verified=True,all_payload_sizes_sha256_verified=True,
    all_118_fault_logs_included=True,both_original_RED_logs_included=True,builder_zip_byte_identical=True,
    preserved_reviewer_setup_failure_included=True,disposition='FIT FOR A5 LAUNCH-PACKET REGENERATION',
    A5_executed=False,new_A5_authority_created=False,launch_packet_regenerated=False)
with (R/'INTAKE_RECEIPT.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(receipt,f,indent=2)
with (R/(NAME+'.sha256')).open('x',encoding='ascii',newline='\n') as f:f.write(receipt['sha256']+'  '+NAME+'\n')
print(json.dumps(receipt,indent=2))
