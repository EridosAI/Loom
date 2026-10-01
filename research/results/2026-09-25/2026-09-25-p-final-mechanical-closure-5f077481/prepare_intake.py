"""Prepare new mechanical-review documents/references only. No execution entry point."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;W=R.parent.parent
def read(path):return json.loads(Path(path).read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,raw):
    p=R/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
def copy(source,name,expected=None):
    raw=Path(source).read_bytes()
    if expected:assert sha(raw)==expected
    write(name,raw)
z=read(R/'provenance/ZIP.json');g=read(R/'provenance/GIT.json');ids=read(R/'provenance/IDENTITIES.json')
audit=read(R/'FAULT_AND_SUITE_AUDIT.json');pres=read(R/'provenance/PRESERVATION.json')
assert audit['pairs']==54 and audit['logs']==108 and audit['collection']['total']==143
assert g['head']=='5f07748102cb5eaa302569c87efbae095050e9fe' and not g['status']
copy(z['zip'],'reviewed_delivery/Loom_P_Final_Apparatus_Correction_Review_20260925.zip',z['sha256'])
copy(R/'portable/FINAL_CORRECTION.patch','FINAL_CORRECTION.patch',g['patch_sha256'])
copy(Path(r'C:\Users\Jason\.codex\attachments\28576fbe-9b89-4481-b331-6f0a03b6bb4f\Pasted text.txt'),'references/FINAL_MECHANICAL_REVIEW_REQUEST.txt')
prior=W/'exports/2026-09-25-p-apparatus-correction-review-9d31e790'
old_name='LOOM_P_FINAL_APPARATUS_CORRECTION_REVIEW.md'
old_id=next(x for x in read(prior/'FILE_MANIFEST.json')['files'] if x['path']==old_name)
copy(prior/old_name,'references/PREVIOUS_INDEPENDENT_HOLD_REVIEW.md',old_id['sha256'])
copy(R/'portable/docs/developmental_ecology/p_apparatus_final_correction_20260925/FINAL_CORRECTION_REPORT.md',
     'references/BUILDER_FINAL_CORRECTION_REPORT.md','2cb6deb751bd5abd40b67734cbbdb55d73a2b3edf9301b4a9f39e2b65d8bdb86')
review=(R/'LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md').read_text(encoding='utf-8')
table=review.split('## Concise closure table\n',1)[1].split('\n## Scope and controlling evidence',1)[0]
write('CLOSURE_TABLE.md',('# Final mechanical closure table\n\n**FIT TO BEGIN AUTHORIZED COUPLING COMMISSIONING**\n\n'+table.lstrip()).encode())
identity={'date':'2026-09-25','disposition':'FIT TO BEGIN AUTHORIZED COUPLING COMMISSIONING',
 'checkpoint':g['head'],'previous_HOLD':g['parent'],'P_checkpoint':'6bc9683b54e4fa80136fe8534d7713e2a250a95f',
 'branch':g['branch'],'P_runtime':ids['P'],'apparatus_runtime':ids['apparatus'],
 'configuration_file':ids['configuration_file'],'configuration_semantic':ids['configuration_semantic'],
 'patch':{'bytes':g['patch_bytes'],'sha256':g['patch_sha256']},'reviewed_builder_zip':z,
 'historical_trees':g['EXP1_21'],'preservation':pres,'final_preservation':read(R/'provenance/FINAL_PRESERVATION.json'),
 'suite_composition':audit['collection']['composition'],'suites':audit['suites'],
 'delivered_fault_control_pairs':54,'delivered_fault_control_logs':108,
 'known_blockers':{'A-R1a':'CLOSED','A-R1b':'CLOSED','A-R1c':'CLOSED'},
 'commissioning_authorized_by_review':False,'commissioning_executed_by_review':False}
write('REVIEWED_IDENTITIES.json',json.dumps(identity,indent=2).encode())
readme='''# Loom P final mechanical closure — Workbench intake

**FIT TO BEGIN AUTHORIZED COUPLING COMMISSIONING**

Reviewed apparatus `5f07748102cb5eaa302569c87efbae095050e9fe`, previous HOLD `9d31e7902658b15762052a2a6a3d161d64338524`, unchanged P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Review date 2026-09-25.

All three known blockers are closed. Both full suites pass 143 tests; all 18 new and 36 prior delivered fault/control pairs reproduce. This establishes mechanical fitness only. Jason's execution authority remains separate. No commissioning was started.

- `LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md`: full scope, conclusions and evidence.
- `CLOSURE_TABLE.md`: concise result and stop point.
- `REPRODUCTION_COMMANDS.md`: exact commands, fresh-output procedure and RED/GREEN exit semantics.
- `REVIEWED_IDENTITIES.json`: reviewed checkpoint, patch, runtime, suite and custody identities.
- `duplicates-old-RED/`, `duplicates-new-GREEN/`, `controller/`, `pending/`: exact old failures, corrected controls and bounded manufactured evidence.
- `previous-16-pairs-001/`, `previous-20-pairs-001/`, `new-18-pairs-001/`: all 108 logs and exact subprocess command matrices.
- `FAULT_AND_SUITE_AUDIT.json`: independent inspection of actual exception lines, traceback frames and log hashes; 59/24/30/30 collection.
- `provenance/`: complete preservation, package, unchanged-law and existing-record reconstruction receipts.
- `reviewed_delivery/`: byte-identical supplied builder ZIP, SHA-256 `c0c0a0c426ff85c5fbf848ad34bba543218ff4420ebf9c573bc66737f6a34fcf`. It includes matching source, cache, records and historical archives.
- `references/` and `FINAL_CORRECTION.patch`: controlling request, previous HOLD review, builder report and exact diff.
- `FILE_MANIFEST.json`: size/hash of every included payload. The separate adjacent `INTAKE_RECEIPT.json` identifies the completed ZIP after reopening and checking all entries.

Synthetic grants are manufactured data, NOT Jason authorization. All source/evidence references retain their real original paths. Use a fresh sibling export for reruns as documented; this archive does not bundle the pinned interpreter or promise portable runtime identity on another machine.

Disposable pytest trees and the redundant expanded builder tree are omitted. Full independent closure components, original failures, all fault logs and the retained reviewer fixture-setup error are included. No target, Git, existing artifact or Workbench file was modified. This archive is ready for intake; intake itself was not performed.
'''
write('README.md',readme.encode())
print(json.dumps({'prepared':True,'disposition':identity['disposition'],'reviewed_builder_zip_sha256':z['sha256']}))
