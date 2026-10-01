"""Copy sealed review documents into a new INBOX directory only."""
import hashlib,json,pathlib,shutil
R=pathlib.Path(__file__).resolve().parents[1]
O=R/'exports/2026-09-26-A5-clock-correction'
P=O/'portable/Loom_P_Clock_Correction_Review_20260926'
INBOX=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX').resolve()
DEST=INBOX/'2026-09-26-A5-clock-correction-68db2c58'
def ident(p):
    with p.open('rb') as f:return {'sha256':hashlib.file_digest(f,'sha256').hexdigest(),'bytes':p.stat().st_size}
receipt=json.loads((O/'PACKAGE_RECEIPT.json').read_bytes())
archive=pathlib.Path(receipt['archive'])
assert ident(archive)=={k:receipt[k] for k in ('sha256','bytes')}
manifest=json.loads((P/'ARTIFACT_MANIFEST.json').read_bytes())['files']
assert all(ident(P/n)==v for n,v in manifest.items())
assert DEST.resolve().parent==INBOX and not DEST.exists()
DEST.mkdir()
bundle=DEST/P.name;shutil.copytree(P,bundle)
for n in (archive.name,archive.name+'.sha256','PACKAGE_RECEIPT.json'):
    shutil.copyfile(O/n,DEST/n)
assert all(ident(bundle/n)==v for n,v in manifest.items())
assert ident(bundle/'ARTIFACT_MANIFEST.json')==ident(P/'ARTIFACT_MANIFEST.json')
assert ident(DEST/archive.name)==ident(archive)
delivered={'checkpoint':receipt['checkpoint'],'report':str(bundle/'CLOCK_SCHEDULING_CORRECTION_REPORT.md'),
    'package':str(DEST/archive.name),'sha256':receipt['sha256'],'verified_payloads':len(manifest),
    'new_INBOX_directory_only':True,'existing_workbench_files_changed':False,'vault_Git_writes':False,
    'A5_execution':False,'new_launch_authority':False,'status':'STOP for narrow correction review'}
(DEST/'DELIVERY_RECEIPT.json').write_text(json.dumps(delivered,indent=2),encoding='utf-8')
print(json.dumps(delivered,indent=2))
