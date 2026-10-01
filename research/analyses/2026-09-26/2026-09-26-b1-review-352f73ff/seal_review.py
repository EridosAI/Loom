"""Seal the public review, exclude exact private payloads, reopen and verify."""
from pathlib import Path,PurePosixPath
import hashlib,json,zipfile
R=Path(__file__).resolve().parent
NAME='Loom_P_B1_Narrow_Independent_Review_352f73ff_20260926.zip'
DEST=R/NAME
EXTERNAL={NAME,NAME+'.sha256','FILE_MANIFEST.json','INTAKE_RECEIPT.json'}
for name in EXTERNAL:assert not (R/name).exists(),name
def sha(raw):return hashlib.sha256(raw).hexdigest()
guard=json.loads((R/'provenance/SEALED_PAYLOAD_EXCLUSION_GUARD.json').read_bytes())
forbidden=set(guard['forbidden_file_hashes']);assert len(forbidden)==39
def include(p):
    parts=p.relative_to(R).parts
    if parts[0]=='portable' or '__pycache__' in parts:return False
    if parts[0]=='regression' and len(parts)>2 and parts[1].endswith('-temp'):return False
    return p.is_file() and p.name not in EXTERNAL
files=[]
for p in sorted(p for p in R.rglob('*') if include(p)):
    raw=p.read_bytes();digest=sha(raw)
    assert digest not in forbidden,'Private payload exclusion violation'
    files.append(dict(path=p.relative_to(R).as_posix(),bytes=len(raw),sha256=digest))
names={x['path'] for x in files}
for colour in ('RED','GREEN'):
    assert sum(n.startswith('regression/') and n.endswith('-'+colour+'.log') and n.count('/')==1 for n in names)==12
for name in ('LOOM_P_B1_NARROW_INDEPENDENT_REVIEW.md','CLOSURE_TABLE.md','REPRODUCTION_COMMANDS.md','REVIEWED_IDENTITIES.json',
             'lifecycle/old.log','lifecycle/new.log','lifecycle/old-hidden-exact.log','lifecycle/old-hidden-exact-results.json',
             'lifecycle/LIFECYCLE_CUSTODY_REVIEW.md','information_flow/INFORMATION_FLOW_REVIEW.md',
             'information_flow/OBSERVED-DOM-C-RED.log','information_flow/OBSERVED-DOM-C-GREEN.log',
             'provenance/provenance.md','provenance/FINAL_PRESERVATION.json'):
    assert name in names,name
builder=next(x for x in files if x['path']=='reviewed_delivery/B1_OPERATOR_APPARATUS_CORRECTION_REVIEW.zip')
assert builder['bytes']==27546035 and builder['sha256']=='0166f1395e9f10fba96e05f5d53264ba2fc275db2122087810406107e3ccf318'
# Recheck every nested supplied member against the private-byte exclusion list.
with zipfile.ZipFile(R/builder['path']) as nested:
    assert nested.testzip() is None
    for info in nested.infolist():
        if not info.is_dir():assert sha(nested.read(info)) not in forbidden,'Nested private payload exclusion violation'
manifest=dict(schema=1,scope='Narrow B1 interface review; no prepared controls/B1 execution, new authority or hidden-state disclosure',files=files)
with (R/'FILE_MANIFEST.json').open('x',encoding='utf8',newline='\n') as f:json.dump(manifest,f,indent=2)
with zipfile.ZipFile(DEST,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as archive:
    for entry in files:
        archive.write(R/entry['path'],entry['path'],compress_type=zipfile.ZIP_STORED if entry['path'].endswith('.zip') else zipfile.ZIP_DEFLATED)
    archive.write(R/'FILE_MANIFEST.json','FILE_MANIFEST.json')
with zipfile.ZipFile(DEST) as archive:
    members=archive.namelist()
    assert len(members)==len(set(members))==len({x.casefold() for x in members})==len(files)+1
    assert set(members)==names|{'FILE_MANIFEST.json'} and archive.testzip() is None
    for name in members:
        path=PurePosixPath(name);assert not path.is_absolute() and '..' not in path.parts and '\\' not in name and ':' not in name
    assert json.loads(archive.read('FILE_MANIFEST.json'))==manifest
    for entry in files:
        raw=archive.read(entry['path']);digest=sha(raw)
        assert len(raw)==entry['bytes'] and digest==entry['sha256'] and digest not in forbidden
receipt=dict(file=NAME,bytes=DEST.stat().st_size,sha256=sha(DEST.read_bytes()),entries=len(files)+1,
    manifest_payload_files=len(files),safe_unique_paths=True,CRC_verified=True,all_payload_sizes_sha256_verified=True,
    all_24_A_L_fault_logs_included=True,exact_old_hidden_and_duplicate_RED_included=True,
    builder_zip_byte_identical=True,forbidden_private_payload_hashes_checked=39,private_payload_collisions=0,
    nested_builder_private_payload_collisions=0,disposition='FIT FOR B1 LAUNCH-PACKET REGENERATION',
    prepared_controls_executed=False,B1_executed=False,new_launch_authority=False,launch_packet_regenerated=False,
    hidden_snapshot_decoded=False,hidden_state_disclosed=False)
with (R/'INTAKE_RECEIPT.json').open('x',encoding='utf8',newline='\n') as f:json.dump(receipt,f,indent=2)
with (R/(NAME+'.sha256')).open('x',encoding='ascii',newline='\n') as f:f.write(receipt['sha256']+'  '+NAME+'\n')
print(json.dumps(receipt,indent=2))
