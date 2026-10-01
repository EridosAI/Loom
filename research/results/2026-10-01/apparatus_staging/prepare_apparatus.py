"""Read-only custody checks; writes only a fresh apparatus evidence directory."""
import hashlib,json,shutil,subprocess,sys,zipfile
from pathlib import Path

def sha(data): return hashlib.sha256(data).hexdigest()
project=Path(__file__).resolve().parent.parent
repo=Path(sys.argv[1]); out=repo/'developmental_ecology/artifacts/apparatus-20260924-01a0c405'
wb=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
design=wb/'50_SESSIONS/2026-09-23-p-commissioning-design-2fb3ff84'
export=project/'exports/2026-09-23-p-commissioning-design-2fb3ff84'
names=['P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md','P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md',
       'P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md','DECISIONS_REQUIRED_BEFORE_EXECUTION.md',
       'P_COMMISSIONING_PLAIN_LANGUAGE_WALKTHROUGH_v0_1.md']
references=out/'references'; references.mkdir(exist_ok=True)
identities=[]
for name in names:
    source=design/name; data=source.read_bytes()
    assert data==(export/name).read_bytes(),name
    (references/name).write_bytes(data)
    identities.append({'source':str(source),'name':name,'sha256':sha(data),'bytes':len(data)})
for source in [wb/'AGENTS.md',wb/'00_RESEARCH_MAP.md',wb/'01_WORKSPACE_STATUS.md',
               wb/'90_SOURCES/p_final_r1p_review_2026-09-23_08df839e/LOOM_P_FINAL_INDEPENDENT_R1P_FIDELITY_REVIEW.md',
               Path(r'C:\Users\Jason\.codex\attachments\57dba765-655a-445a-adc3-29618b3d0307\Pasted text.txt')]:
    data=source.read_bytes(); name='APPARATUS_BUILD_REQUEST.txt' if source.name=='Pasted text.txt' else source.name
    (references/name).write_bytes(data); identities.append({'source':str(source),'name':name,'sha256':sha(data),'bytes':len(data)})
# Verify the full read-copy manifest, not just the five design headings.
reading=json.loads((export/'READING_COPY_IDENTITIES.json').read_bytes())
for row in reading['files']:
    data=(export/'REFERENCE_READS'/row['path']).read_bytes()
    assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
archive=wb/'EXPORTS/2026-09-23-p-commissioning-design-2fb3ff84/Loom_P_Coupling_Commissioning_Design_20260923_2fb3ff84.zip'
assert sha(archive.read_bytes())=='018f23d8e1bdb9433d7a50c8e421f09deb70d26febc3a5f14d98fa3b467551d0'
with zipfile.ZipFile(archive) as z:
    bad=z.testzip(); assert bad is None
    inventory_name='DELIVERY_MANIFEST.json'
    inventory=json.loads(z.read(inventory_name))
    for name, row in inventory['files'].items():
        data=z.read(name)
        assert len(data)==row['bytes'] and sha(data)==row['sha256'],name
    (out/'DESIGN_ARCHIVE_MANIFEST.json').write_bytes(z.read(inventory_name))
    print('design manifest schema',type(inventory).__name__, list(inventory)[:5])
shutil.copyfile(archive,references/archive.name)
old=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405')
preserved={str(p.relative_to(old)).replace('\\','/'):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
           for p in sorted((old/'developmental_ecology/artifacts').rglob('*')) if p.is_file()}
(out/'PRESERVATION_BEFORE.json').write_text(json.dumps(preserved,indent=2),encoding='utf-8')
runtime={p.name:sha(p.read_bytes()) for p in sorted((repo/'developmental_ecology/loom_p').glob('*.py'))}
assert all(sha((old/'developmental_ecology/loom_p'/name).read_bytes())==value for name,value in runtime.items())
(out/'SOURCE_IDENTITIES.json').write_text(json.dumps({'sources':identities,'reading_copies_verified':len(reading['files']),
    'design_archive_sha256':sha(archive.read_bytes()),'protected_artifact_count':len(preserved),'p_runtime':runtime},indent=2),encoding='utf-8')
print('Verified sources, read copies, archive custody and',len(preserved),'preserved prior artifact files')
