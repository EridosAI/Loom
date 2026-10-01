"""Prepare public B1 review artifacts and reference copies, never held state."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;W=R.parents[1]
def read(p):return json.loads(Path(p).read_bytes())
def sha(raw):return hashlib.sha256(raw).hexdigest()
def write(name,raw):
    path=R/name;path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('xb') as f:f.write(raw)
def copy(source,name,expected=None):
    raw=Path(source).read_bytes()
    if expected:assert sha(raw)==expected
    assert sha(raw) not in forbidden
    write(name,raw)
forbidden=read(R/'provenance/SEALED_PAYLOAD_EXCLUSION_GUARD.json')['forbidden_file_hashes']
z=read(R/'provenance/ZIP.json');g=read(R/'provenance/GIT.json');ids=read(R/'provenance/CURRENT_IDENTITIES.json')
final=read(R/'provenance/FINAL_PRESERVATION.json');static=read(R/'provenance/STATIC_COMPATIBILITY.json')
audit=read(R/'FAULT_AND_SUITE_AUDIT.json')
assert final['all_unchanged'] and audit['pairs']==12 and audit['logs']==24
assert static['pair_only_case_id_and_declared_display_differ'] and not static['snapshot_content_decoded']
copy(z['archive'],'reviewed_delivery/B1_OPERATOR_APPARATUS_CORRECTION_REVIEW.zip',z['sha256'])
copy(R/'portable/EXACT_DIFF_68db2c58_to_352f73ff.patch','EXACT_DIFF_68db2c58_to_352f73ff.patch',g['patch']['sha256'])
copy(Path(r'C:\Users\Jason\.codex\attachments\4be44c95-00c6-481f-9eac-0e68f206f6ba\Pasted text.txt'),'references/NARROW_B1_REVIEW_REQUEST.txt')
for name in ('B1_OPERATOR_APPARATUS_CORRECTION_REPORT.md','CHEMISTRY_DEPRIVATION_INFORMATION_FLOW.md','LIVE_OPERATOR_STATE_MACHINE.md','RED_GREEN_MATRIX.md'):
    copy(R/'portable/docs'/name,'references/'+name)
copy(W/'exports/2026-09-26-p-clock-final-review-68db2c58/LOOM_P_NARROW_FINAL_CLOCK_REVIEW.md','references/PRIOR_NARROW_CLOCK_REVIEW.md')
copy(W/'exports/2026-09-26-B1-operator-correction-352f73ff-review-02/WINDOWS_REVIEW_NOTE.md','references/WINDOWS_REVIEW_NOTE.md')
review=(R/'LOOM_P_B1_NARROW_INDEPENDENT_REVIEW.md').read_text(encoding='utf8')
table=review.split('## Concise closure table\n',1)[1].split('\n## Scope and reviewed identities',1)[0]
write('CLOSURE_TABLE.md',('# B1 operator correction — closure table\n\n**FIT FOR B1 LAUNCH-PACKET REGENERATION**\n\n'+table.lstrip()+'\nNo positive control/B1 execution, new authority, packet regeneration or hidden-state disclosure occurred.\n').encode())
identity=dict(date='2026-09-26',disposition='FIT FOR B1 LAUNCH-PACKET REGENERATION',checkpoint=g['HEAD'],parent=g['parent'],
    P_checkpoint=g['P_ancestor'],branch=g['branch'],held_review_hash=static['held_review_hash'],identities=ids,
    patch=g['patch'],builder_zip=z,final_preservation=final,static_compatibility=static,
    regression=dict(suites={k:v['summary'] for k,v in audit['suites'].items()},composition=audit['suites']['worktree-suite']['composition'],pairs=12,logs=24),
    prepared_controls_executed=False,B1_executed=False,new_launch_authority=False,launch_packet_regenerated=False,
    hidden_snapshots_decoded=False,hidden_state_disclosed=False)
write('REVIEWED_IDENTITIES.json',json.dumps(identity,indent=2).encode())
readme='''# Loom P B1 narrow independent review — Workbench intake

**FIT FOR B1 LAUNCH-PACKET REGENERATION**

Date 2026-09-26. Apparatus `352f73fffa6d9781eae8aa38e708a9a05669588f`; parent `68db2c581f07200966d699a4f55a65f9b96df1e9`; P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.

Display-only chemistry deprivation and interactive lifecycle correction verified within the requested narrow scope. Both complete suites passed 204 tests; all 12 A–L fault/control pairs reproduced. Independent actual HTTP, detached DOM, physical-record equality and concurrency evidence support closure. Held controls/B1 were checked only as inert metadata and opaque snapshot bytes.

- `LOOM_P_B1_NARROW_INDEPENDENT_REVIEW.md`: full review, conclusions and limits.
- `CLOSURE_TABLE.md`: concise closure.
- `REPRODUCTION_COMMANDS.md`: exact invocation and fresh-output procedure.
- `REVIEWED_IDENTITIES.json`: checkpoint/runtime/patch/package/preservation identities.
- `information_flow/`: permitted HTTP/history/DOM/download evidence and generic paired raw/physical proof.
- `lifecycle/`: actual old rejection/duplicate evidence, new HTTP concurrency/custody/end/binding proof and manufactured component records.
- `regression/`: fresh suite logs/JUnit and all 24 A–L logs with exact command receipts.
- `FAULT_AND_SUITE_AUDIT.json` and `.md`: inspected actual exception frames/JUnit failures, hashes and 204-case composition.
- `provenance/`: package/source/held preservation, safe static compatibility, runtime identity and final rehash of 3,064 unchanged paths.
- `references/` and exact patch: controlling request, builder specifications and directly relevant previous review.
- `reviewed_delivery/B1_OPERATOR_APPARATUS_CORRECTION_REVIEW.zip`: byte-identical latest builder archive, SHA-256 `0166f1395e9f10fba96e05f5d53264ba2fc275db2122087810406107e3ccf318`.
- `FILE_MANIFEST.json`: included payload sizes/hashes. Adjacent `INTAKE_RECEIPT.json` identifies the final reopened/verified archive.

No prepared positive control, B1 case, new prehistory or ecological replay occurred. No new B1 authority or packet was created. The original held packet remains non-launchable. Sealed geometry/snapshots are not included or disclosed. This archive is ready for intake; Workbench/canon was not modified.

The supplied runtime is not bundled. Reproduction uses the recorded pinned local Python/Node and fresh output roots. New harnesses must not be rerun inside sealed evidence. Manufactured manifests/records are component evidence, not Jason execution permission. Expanded duplicate builder source and disposable pytest trees are omitted; independent records and all completed evidence are retained.
'''
write('README.md',readme.encode())
print(json.dumps({'prepared':True,'builder_zip_sha256':z['sha256'],'disposition':identity['disposition']}))
