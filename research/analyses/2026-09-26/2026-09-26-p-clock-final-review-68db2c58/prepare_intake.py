"""Assemble new review documents and reference copies; no launch or source mutation."""
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent; W=R.parents[1]
def read(p):return json.loads(Path(p).read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def write(name,raw):
    p=R/name;p.parent.mkdir(parents=True,exist_ok=True)
    with p.open('xb') as f:f.write(raw)
def copy(source,name,expected=None):
    raw=Path(source).read_bytes()
    if expected:assert sha(raw)==expected
    write(name,raw)
z=read(R/'provenance/ZIP.json');g=read(R/'provenance/GIT.json')
ids=read(R/'provenance/CURRENT_IDENTITIES.json');audit=read(R/'FAULT_AND_SUITE_AUDIT.json')
final=read(R/'provenance/FINAL_PRESERVATION.json');retro=read(R/'provenance/RETROSPECTIVE.json')
assert audit['pairs']==59 and audit['logs']==118 and audit['collection']['total']==176
assert final['all_rehashed_unchanged'] and retro['total']==5579 and retro['disagreements']==0
copy(z['source'],'reviewed_delivery/Loom_P_Clock_Correction_Review_20260926.zip',z['sha256'])
copy(R/'portable/CLOCK_SCHEDULING_CORRECTION.patch','CLOCK_SCHEDULING_CORRECTION.patch',g['patch']['sha256'])
copy(Path(r'C:\Users\Jason\.codex\attachments\5d34d925-07a0-4228-8b75-37edc5948e8d\Pasted text.txt'),'references/NARROW_FINAL_REVIEW_REQUEST.txt')
copy(W/'exports/2026-09-26-A5-clock-compatibility-review-5f077481/A5_CLOCK_COMPATIBILITY_REVIEW.md','references/A5_CLOCK_COMPATIBILITY_REVIEW.md')
prior=W/'exports/2026-09-25-p-final-mechanical-closure-5f077481'
for source,name in [('LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md','PRIOR_FINAL_MECHANICAL_CLOSURE_REVIEW.md'),
                    ('pending/PENDING_MECHANICAL_CLOSURE.md','PRIOR_PENDING_MECHANICAL_CLOSURE.md'),
                    ('controller/CONTROLLER_CLOSURE_REVIEW.md','PRIOR_CONTROLLER_CLOSURE_REVIEW.md')]:
    copy(prior/source,'references/'+name)
for name in ('CLOCK_SCHEDULING_CORRECTION_REPORT.md','NATIVE_INDEX_SCHEDULING_SPECIFICATION.md'):
    copy(R/'portable/docs/developmental_ecology/p_clock_correction_20260926'/name,'references/'+name)
review=(R/'LOOM_P_NARROW_FINAL_CLOCK_REVIEW.md').read_text(encoding='utf-8')
table=review.split('## Concise closure table\n',1)[1].split('\n## Scope, sources and exact identities',1)[0]
write('CLOSURE_TABLE.md',('# Narrow final clock review — closure table\n\n**FIT FOR A5 LAUNCH-PACKET REGENERATION**\n\n'+table.lstrip()+'\nNo A5 execution, replacement authority or launch-packet regeneration was performed.\n').encode())
identity=dict(date='2026-09-26',disposition='FIT FOR A5 LAUNCH-PACKET REGENERATION',
    checkpoint=g['HEAD'],parent=g['parent'],P_checkpoint=g['P_ancestor'],branch=g['branch'],
    held_A5='88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6',
    identities=ids,patch=g['patch'],builder_zip=z,final_preservation=final,
    historical_compatibility=dict(decisions=5579,stage_disagreements=0,historical_instrument=g['parent']),
    regression=dict(suites=audit['suites'],composition=audit['collection']['composition'],pairs=59,logs=118),
    A5_executed_by_review=False,A5_authority_created_by_review=False,launch_packet_regenerated=False)
write('REVIEWED_IDENTITIES.json',json.dumps(identity,indent=2).encode())
readme='''# Loom P narrow final clock review — Workbench intake

**FIT FOR A5 LAUNCH-PACKET REGENERATION**

Apparatus `68db2c581f07200966d699a4f55a65f9b96df1e9`; preserved parent `5f07748102cb5eaa302569c87efbae095050e9fe`; unchanged P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Date 2026-09-26.

Both old clock failures reproduce RED and corrected cases pass. All6,300 actual held A5 holds are statically legal. Original A1–A4:5,579 decisions,0stage disagreements. Both full suites:176passed;59fault/control pairs independently verified. No A5 execution, packet regeneration or replacement authority was performed. The held proposal is not execution authority.

- `LOOM_P_NARROW_FINAL_CLOCK_REVIEW.md`: full narrow review and evidence limits.
- `CLOSURE_TABLE.md`: concise closure.
- `REVIEWED_IDENTITIES.json`: checkpoint, runtime, patch, archive, preservation and test identities.
- `REPRODUCTION_COMMANDS.md`: exact commands and safe fresh-output reproduction guidance.
- `scheduling/`: separate old-A/old-B REDs, new GREEN, integer oracle, all6,300 inert holds and call fence.
- `continuity/`: short generic physical pause/resume fixtures, detached late states, source checks and preserved reviewer setup error.
- `regression/`: fresh suite logs, all118 RED/GREEN logs and exact child command matrices.
- `FAULT_AND_SUITE_AUDIT.json` and `.md`: actual exception/traceback audit, log hashes and176case composition.
- `provenance/`: original-record5,579row comparisons, exact fixture semantics, source/package/held/history and final rehash receipts.
- `CLOCK_SCHEDULING_CORRECTION.patch` and `references/`: exact diff and controlling/relevant documents.
- `reviewed_delivery/Loom_P_Clock_Correction_Review_20260926.zip`: byte-identical builder package, SHA-2568c5e9322d06b4915ed31106770aff80e925666d961e389102c27a9ad4499e894, including matching source and saved stage references.
- `FILE_MANIFEST.json`: every included payload size/hash. Adjacent `INTAKE_RECEIPT.json` identifies this completed archive after reopening and verification.

The archive is ready for intake; Workbench/canon was not changed. New scripts are review harnesses only. Original source paths and pinned local runtime remain explicit; the interpreter is not bundled. Extract the nested builder ZIP into a fresh folder for portable suite reproduction. Do not rerun review scripts inside this sealed evidence directory. Synthetic fixture manifests/grants are not Jason execution authority. Historical A1–A4 remain old-instrument observations, not corrected-instrument executions.

Expanded duplicate builder source and disposable pytest temporary trees are omitted. Independent component records, complete logs and the failed reviewer source-comparison setup attempt are retained. No long ecological world, A5 command/world, new prehistory or broader adversarial campaign was run.
'''
readme=readme.replace('All6,300','All 6,300').replace('all6,300','all 6,300').replace('A1–A4:5,579','A1–A4: 5,579').replace('decisions,0stage','decisions, 0 stage').replace('suites:176passed;59fault','suites: 176 passed; 59 fault').replace('all118','all 118').replace('and176case','and 176-case').replace('original-record5,579row','original-record 5,579-row').replace('SHA-2568c','SHA-256 8c')
write('README.md',readme.encode())
print(json.dumps({'prepared':True,'disposition':identity['disposition'],'builder_zip_sha256':z['sha256']}))
