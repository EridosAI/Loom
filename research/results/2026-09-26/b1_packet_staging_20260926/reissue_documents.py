"""File-only correction of preparation documentation; no research imports."""
import json,pathlib,shutil,hashlib
from prepare_packet import canonical,digest,sha,write,seal
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
OLD=ROOT/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58'
E=ROOT/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02'
PUB=E/'B1_OPERATOR_REVIEW';PRIV=E/'B1_PRIVILEGED_EVALUATOR_HOLD'
assert not E.exists()
def js(p):return json.loads(p.read_bytes())
receipt=js(OLD/'PACKAGE_RECEIPT.json')
exclude={'FILE_MANIFEST.json','HELD_REVIEW_IDENTITY.json','HELD_REVIEW_OBJECT.json','HELD_REVIEW_OBJECT.canonical.json'}
for name in ['B1_OPERATOR_REVIEW','B1_PRIVILEGED_EVALUATOR_HOLD']:
    for p in (OLD/name).rglob('*'):
        if p.is_file() and p.name not in exclude:
            q=E/name/p.relative_to(OLD/name);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
old="The Workbench's latest navigation still says A5 NOT EXECUTED. That is a dated pre-execution status. The newer sealed A5 result and Jason's present instruction control this task; the older files were preserved rather than silently reconciled or edited. A0–A5 remain bounded physical commissioning evidence, not P learning/perception or scientific efficacy."
new="The Workbench's current instructions/map/status and registered A5_COMMISSIONING_EVIDENCE_RECORD.md record A5 as OBSERVED and the bounded physical ceiling as exercised. The older A5 NOT EXECUTED sections are explicitly preserved preparation history. This matches the newer sealed A5 result and Jason's present request. A0–A5 remain bounded physical commissioning evidence, not P learning/perception or scientific efficacy. No navigation or source file was changed."
note=PUB/'SESSION_RECORD.md';text=note.read_text(encoding='utf-8');assert text.count(old)==1
note.write_text(text.replace(old,new),encoding='utf-8',newline='\n')
shutil.copyfile(S/'write_documents.py',PRIV/'DOCUMENT_AUTHORING_SOURCE.py')
shutil.copyfile(S/'reissue_documents.py',PRIV/'DOCUMENT_CORRECTION_SOURCE.py')
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
source=WB/'50_SESSIONS/2026-09-26-a5-evidence-intake-82b4d9e1/A5_COMMISSIONING_EVIDENCE_RECORD.md'
source_key='workbench/A5_COMMISSIONING_EVIDENCE_RECORD.md'
shutil.copyfile(source,PRIV/'references'/source_key)
ids=js(PRIV/'SOURCE_IDENTITIES.json');ids[source_key]=dict(path=str(source),sha256=sha(source),bytes=source.stat().st_size)
(PRIV/'SOURCE_IDENTITIES.json').write_text(json.dumps(ids,indent=2)+'\n',encoding='utf-8')
before=js(PRIV/'ORIGINALS_BEFORE.json');before[str(source)]=sha(source)
assert all(sha(pathlib.Path(p))==h for p,h in before.items())
for name in ['ORIGINALS_BEFORE.json','ORIGINALS_AFTER.json']:
    (PRIV/name).write_text(json.dumps(before,indent=2)+'\n',encoding='utf-8')
pres=js(PUB/'PRESERVATION.json');pres['original_files_checked']=len(before)
(PUB/'PRESERVATION.json').write_text(json.dumps(pres,indent=2)+'\n',encoding='utf-8')
write(PUB/'DOCUMENTATION_REVISION.json',dict(previous_seal_sha256=receipt['held_review_sha256'],revision=2,
    reason='Correct session note: current Workbench navigation already records A5 OBSERVED; older NOT EXECUTED sections are explicitly historical. Add the registered evidence source.',
    original_preparation_retained=True,case_manifests_unchanged=True,case_authority_digests_unchanged=True,
    snapshots_byte_identical=True,new_initial_sensor_calculations=0,new_simulation_steps=0,new_controller_calls=0))
for folder in ['initial-states','case-manifests','authority-objects']:
    for p in (PRIV/folder).rglob('*'):
        if p.is_file():assert sha(p)==sha(OLD/'B1_PRIVILEGED_EVALUATOR_HOLD'/p.relative_to(PRIV))
held=js(OLD/'B1_PRIVILEGED_EVALUATOR_HOLD/HELD_REVIEW_OBJECT.json')
held['public_documents']={p.relative_to(PUB).as_posix():sha(p) for p in sorted(PUB.rglob('*')) if p.is_file()}
held['privileged_documents']={p.relative_to(PRIV).as_posix():sha(p) for p in sorted(PRIV.rglob('*')) if p.is_file()}
write(PRIV/'HELD_REVIEW_OBJECT.json',held)
(PRIV/'HELD_REVIEW_OBJECT.canonical.json').write_bytes(canonical(held));h=digest(held)
private_archive=seal(PRIV)
write(PUB/'HELD_REVIEW_IDENTITY.json',dict(sha256=h,status='HOLD — review identity, NOT execution authority',private_archive=private_archive,
    no_grants=True,next_decision='Jason may separately authorize the narrowly specified apparatus work and independent review. Do not execute this packet.'))
public_archive=seal(PUB)
receipt.update(held_review_sha256=h,public=public_archive,privileged=private_archive,documentation_revision=2)
write(E/'PACKAGE_RECEIPT.json',receipt)
shutil.copyfile(OLD/'README.md',E/'README.md')
print(json.dumps(receipt,indent=2))
