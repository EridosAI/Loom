"""Package review-local evidence and read-only inputs; never execute a world."""
import hashlib, json, re, shutil, zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
SOURCE_ZIP = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX\2026-09-24-p-commissioning-apparatus\Loom_P_Commissioning_Apparatus_Review_20260924.zip')
PACKAGE = REPO / 'developmental_ecology/artifacts/review-package-apparatus-20260924-01a0c405'
EXPECTED_ZIP = '87f4dbde39a72559caf6045c7ac68a649d9691a000d1569af5d26b090a63b053'
def digest(data): return hashlib.sha256(data).hexdigest()
def identify(path):
    data=path.read_bytes(); return {'bytes':len(data),'sha256':digest(data)}
def new_json(path,data):
    with path.open('x',encoding='utf-8') as f: json.dump(data,f,indent=2)

# Minor spacing corrections only in reviewer-authored prose, before sealing.
replacements={
    'all16':'all 16','All16':'All 16','all32':'all 32','full32':'full 32',
    'in34.04':'in 34.04','in33.46':'in 33.46','and24':'and 24',
    'births1,2,3,4':'births 1, 2, 3, 4','with600':'with 600',
    'The60,000':'The 60,000','IDs1–4':'IDs 1–4','life0':'life 0',
    'saved0.2':'saved 0.2','is15.165':'is 15.165','is4,801':'is 4,801',
    'Thus8960':'Thus 8960','to37.744':'to 37.744','and43.018':'and 43.018',
    'or86.037':'or 86.037','39999999GB':'39999999 GB','79999998GB':'79999998 GB',
    'decimalGB':'decimal GB','earlier11.67h/17.66GB':'earlier 11.67 h / 17.66 GB',
    'All10':'All 10','all13':'all 13','all55':'all 55','and68':'and 68',
    'The792':'The 792','All792':'All 792',':726':': 726','and66':'and 66',
    'all16':'all 16','two authorized0.2':'two authorized 0.2',
    'stage1':'stage 1','Stage1':'Stage 1',',600':', 600',
}
for name in ('LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md','REPRODUCTION_COMMANDS.md'):
    path=ROOT/name; text=path.read_text(encoding='utf-8')
    for a,b in replacements.items():text=text.replace(a,b)
    path.write_text(text,encoding='utf-8')

inputs=ROOT/'reviewed-inputs';inputs.mkdir(exist_ok=False)
data=SOURCE_ZIP.read_bytes();assert digest(data)==EXPECTED_ZIP
(inputs/SOURCE_ZIP.name).write_bytes(data)
for name in ('APPARATUS.patch','CHECKPOINT.json','ARTIFACT_MANIFEST.json'):
    shutil.copyfile(PACKAGE/'assembled'/name,inputs/name)
shutil.copyfile(PACKAGE/'RECEIPT.json',inputs/'BUILDER_RECEIPT.json')
shutil.copyfile(Path(r'C:\Users\Jason\.codex\attachments\474bc883-58ad-42c6-8904-d59b1abeab51\Pasted text.txt'),inputs/'INDEPENDENT_REVIEW_REQUEST.txt')

with zipfile.ZipFile(SOURCE_ZIP) as z:
    assert z.testzip() is None
    expected=json.loads(z.read('ARTIFACT_MANIFEST.json'))['files']
    assert len(expected)==220 and len(z.namelist())==221
    for name, row in expected.items():
        member=z.read(name)
        assert len(member)==row['bytes'] and digest(member)==row['sha256']
        assert member==(ROOT/'portable'/name).read_bytes()

matrix=json.loads((ROOT/'faults-attempt-001/FAULT_MATRIX.json').read_bytes())
assert len(matrix)==16
for pair in matrix:
    assert pair['RED']['exit']==1 and pair['RED']['intended']
    assert pair['GREEN']['exit']==0 and pair['GREEN']['intended']
    red=(ROOT/'faults-attempt-001'/f"{pair['fault']}-RED.log").read_text(encoding='utf-8')
    assert pair['intended_failure'] in red and '1 failed' in red
assert len(list((ROOT/'faults-attempt-001').glob('*-RED.log')))==16
assert len(list((ROOT/'faults-attempt-001').glob('*-GREEN.log')))==16
assert '83 passed in 34.04s' in (ROOT/'worktree-suite-attempt-002.log').read_text(encoding='utf-8')
assert '83 passed in 33.46s' in (ROOT/'portable-suite.log').read_text(encoding='utf-8')

receipt={
 'date':'2026-09-24','disposition':'HOLD BEFORE COUPLING COMMISSIONING',
 'apparatus_checkpoint':'05abf60401d08f38750bca589b1c040e10513d7b',
 'scientific_P_checkpoint':'6bc9683b54e4fa80136fe8534d7713e2a250a95f',
 'findings':[
  {'id':'A-R1','classification':'MUST-FIX BEFORE COMMISSIONING','finding':'Approval lacks complete arm/controller/route execution-contract binding'},
  {'id':'A-R2','classification':'MUST-FIX BEFORE COMMISSIONING','finding':'Nominal route deadline may miss a ten-native-step command hold'}],
 'worktree_suite':{'passed':83,'seconds':34.04},'portable_suite':{'passed':83,'seconds':33.46},
 'unchanged_prior_P_checks':59,'delivered_fault_pairs_verified':16,
 'additional_firewall_pair_verified':True,'prior_artifacts_preserved':792,
 'saved_segments_reconstructed':9,'saved_native_records_including_duplicates':120,
 'unique_continuous_native_records':60,'saved_diagnostics_exact':60,
 'target_modified':False,'commissioning_executed':False,'prehistory_prepared':False,
 'builder_zip':dict(original_path=str(SOURCE_ZIP),**identify(SOURCE_ZIP)),
 'report':identify(ROOT/'LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md'),
 'scope':'Component suites, authorized manufactured fixtures, deliberate in-memory faults, detached saved replay and read-only provenance only',
}
new_json(ROOT/'REVIEW_RECEIPT.json',receipt)

archive_name='Loom_P_Independent_Apparatus_Review_05abf604_20260924.zip'
excluded_names={archive_name,'FILE_MANIFEST.json','ZIP_SHA256.txt','PACKAGE_VERIFICATION.json'}
def include(path):
    rel=path.relative_to(ROOT)
    if rel.parts[0]=='portable' or path.name in excluded_names:return False
    if any(x.startswith(('worktree-temp-','portable-temp-','rerun-')) or x.endswith('-temp') or x=='__pycache__' for x in rel.parts):return False
    return path.is_file()
files=sorted(p for p in ROOT.rglob('*') if include(p))
inventory={p.relative_to(ROOT).as_posix():identify(p) for p in files}
new_json(ROOT/'FILE_MANIFEST.json',{'files':inventory,'review_checkpoint':receipt['apparatus_checkpoint'],'disposition':receipt['disposition']})
archive=ROOT/archive_name
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for path in files+[ROOT/'FILE_MANIFEST.json']:
        z.write(path,path.relative_to(ROOT).as_posix(),compress_type=zipfile.ZIP_STORED if path.suffix=='.zip' else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert len(z.namelist())==len(set(z.namelist()))==len(inventory)+1
    for name,row in inventory.items():
        data=z.read(name);assert len(data)==row['bytes'] and digest(data)==row['sha256']
    assert digest(z.read('reviewed-inputs/'+SOURCE_ZIP.name))==EXPECTED_ZIP
    count_red=len([n for n in z.namelist() if n.startswith('faults-attempt-001/') and n.endswith('-RED.log')])
    count_green=len([n for n in z.namelist() if n.startswith('faults-attempt-001/') and n.endswith('-GREEN.log')])
    assert count_red==count_green==16
archive_id=identify(archive)
(ROOT/'ZIP_SHA256.txt').write_text(archive_id['sha256']+'  '+archive_name+'\n',encoding='utf-8')
verification=dict(archive=archive_name,**archive_id,entries=len(inventory)+1,all_members_verified=True,delivered_RED_logs=count_red,delivered_GREEN_logs=count_green,original_builder_zip_exact=True)
new_json(ROOT/'PACKAGE_VERIFICATION.json',verification)
print(json.dumps(verification,indent=2))
