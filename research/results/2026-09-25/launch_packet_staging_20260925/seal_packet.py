"""Seal documentation/state proposal only, with complete portable hashes."""
import hashlib,json,pathlib,shutil,zipfile
S=pathlib.Path(__file__).resolve().parent
R=S.parent/'exports/2026-09-25-first-commissioning-launch-packet-5f077481'
DELIVERY=S.parent/'exports/2026-09-25-first-commissioning-launch-delivery-5f077481'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ('validate_packet.py','seal_packet.py'):shutil.copyfile(S/name,R/name)
validation=json.loads((R/'PORTABLE_VALIDATION.json').read_bytes())
assert validation['portable_validation_passed'] and validation['grant'] is None and validation['time']==validation['native_index']==0
assert validation['canonical_sha256']=='a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc'
inventory={p.relative_to(R).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(R.rglob('*')) if p.is_file()}
(R/'FILE_MANIFEST.json').write_text(json.dumps({'authority_status':'PROPOSED / NOT AUTHORIZED','canonical_sha256':validation['canonical_sha256'],'files':inventory},indent=2),encoding='utf-8')
DELIVERY.mkdir(exist_ok=False)
output=DELIVERY/'FIRST_COMMISSIONING_LAUNCH_PACKET.zip'
with zipfile.ZipFile(output,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(R.rglob('*')):
        if p.is_file():z.write(p,'FIRST_COMMISSIONING_LAUNCH_PACKET/'+p.relative_to(R).as_posix())
with zipfile.ZipFile(output) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))==len(inventory)+1
    for name,row in inventory.items():
        raw=z.read('FIRST_COMMISSIONING_LAUNCH_PACKET/'+name)
        assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256'],name
receipt={'archive_name':output.name,'bytes':output.stat().st_size,'sha256':sha(output),'payload_files':len(inventory),
    'canonical_authority_sha256':validation['canonical_sha256'],'all_payload_hashes_and_CRC_verified':True,
    'manifest_sha256':sha(R/'FILE_MANIFEST.json'),'commissioning_execution_occurred':False,'authority_status':'PROPOSED / NOT AUTHORIZED'}
(DELIVERY/'PACKAGE_RECEIPT.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(receipt,indent=2))
