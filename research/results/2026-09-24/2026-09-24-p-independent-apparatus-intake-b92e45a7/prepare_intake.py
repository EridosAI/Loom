"""Documentation-only intake of an independent review; no package execution."""
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,io,shutil
from urllib.parse import quote
ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ID='2026-09-24-p-independent-apparatus-intake-b92e45a7'
S=f'50_SESSIONS/{ID}'
B='90_SOURCES/p_independent_apparatus_review_2026-09-24_b92e45a7'
R='30_REVIEWS/REVIEW-P-APPARATUS-INDEPENDENT-05abf604-2026-09-24-b92e45a7.md'
Z=WB/'INBOX/2026-09-24_P_Independent_Apparatus_Review/Loom_P_Independent_Apparatus_Review_05abf604_20260924.zip'
CP='05abf60401d08f38750bca589b1c040e10513d7b'
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,x):write(p,json.dumps(x,indent=2,ensure_ascii=False)+'\n')
z=zipfile.ZipFile(Z);names=z.namelist();assert len(names)==len(set(names))
for name in names:
    p=PurePosixPath(name);assert not p.is_absolute() and '..' not in p.parts and ':' not in name and '\\' not in name
mf=json.loads(z.read('FILE_MANIFEST.json'))
assert set(mf['files'])==set(names)-{'FILE_MANIFEST.json'}
for name,info in mf['files'].items():
    b=z.read(name);assert len(b)==info['bytes'] and sha(b)==info['sha256'],name
assert z.testzip() is None
receipt=json.loads(z.read('REVIEW_RECEIPT.json'))
assert receipt['apparatus_checkpoint']==CP and receipt['scientific_P_checkpoint']==P
reportname='LOOM_P_INDEPENDENT_APPARATUS_FIDELITY_REVIEW.md'
assert sha(z.read(reportname))==receipt['report']['sha256'] and len(z.read(reportname))==receipt['report']['bytes']
builder=z.read('reviewed-inputs/Loom_P_Commissioning_Apparatus_Review_20260924.zip')
assert sha(builder)==receipt['builder_zip']['sha256'] and len(builder)==receipt['builder_zip']['bytes']
assert builder==(WB/'90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61/Loom_P_Commissioning_Apparatus_Review_20260924.zip').read_bytes()
nested=zipfile.ZipFile(io.BytesIO(builder));nm=json.loads(nested.read('ARTIFACT_MANIFEST.json'))
for n,info in nm['files'].items():
    data=nested.read(n);assert len(data)==info['bytes'] and sha(data)==info['sha256']
assert json.loads(nested.read('CHECKPOINT.json'))['checkpoint']==CP
report=z.read(reportname).decode('utf-8-sig').replace('\r','')
table=report.split('## Concise closure table\n',1)[1].split('\n## Review basis',1)[0].strip()
assert table.count('MUST-FIX BEFORE COMMISSIONING')==2

live=['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md']
before={}
for name in live:
    b=(WB/name).read_bytes();before[name]={'bytes':len(b),'sha256':sha(b)}
    out=ROOT/'BEFORE'/name;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(b)
protected={}
for folder in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS','50_SESSIONS/2026-09-24-p-apparatus-intake-73c9ad61']:
    for p in (WB/folder).rglob('*'):
        if p.is_file():protected[p.relative_to(WB).as_posix()]=sha(p.read_bytes())
catalog=json.loads((ROOT/'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'));assert len(catalog['source_files'])==76
selected=[(None,'independent-apparatus-review-delivery-archive'),(reportname,'independent-apparatus-fidelity-review'),
    ('REVIEW_RECEIPT.json','independent-review-custody-metadata'),('FILE_MANIFEST.json','independent-review-custody-manifest'),
    ('README_INTAKE.md','independent-review-intake-note'),('REPRODUCTION_COMMANDS.md','independent-review-reproduction-record')]
sources=ROOT/'SOURCE_BATCH';sources.mkdir(exist_ok=True);entries=[]
for num,(member,role) in enumerate(selected,77):
    filename=member or Z.name;data=z.read(member) if member else Z.read_bytes();(sources/filename).write_bytes(data)
    entries.append({'source_id':f'SRC-{num:03d}','path':B+'/'+filename,'original_filename':filename,'bytes':len(data),'sha256':sha(data),
        'role':role,'prepared':'2026-09-24','stated_author':'Independent reviewer; exact model/backend not stated in main review/receipt',
        'authority':'Independent apparatus engineering review, registered under Jason\u2019s explicit status instruction; not commissioning or repair authority',
        'acquired_from':str(Z)+('::'+member if member else ''),'reviewed_checkpoint':CP,'p_baseline_checkpoint':P,
        'review_note':R,'record':S+'/INTAKE_RECORD.md','notes':'Original bytes preserved. User blocker A1 maps to source A-R1; user blocker A2 maps to source A-R2. Other reviewed dispositions unchanged.'})
catalog['source_files']+=entries
catalog.setdefault('intake_events',[]).append({'session_id':ID,'source_ids':[e['source_id'] for e in entries],'review_note':R,'record':S+'/INTAKE_RECORD.md',
    'scope':'Exact-commit apparatus ENGINEERING HOLD for A1/A-R1 and A2/A-R2; P unchanged/previously verified; commissioning NOT STARTED; no execution'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)

status=f'''Exact apparatus commit: `{CP}`

Commissioning apparatus: **ENGINEERING HOLD**  
P implementation: **unchanged / previously verified**  
Commissioning execution: **NOT STARTED**

Blockers:

- **A1** — approval binding does not yet bind complete arm/controller/route.
- **A2** — stage clock comparison may permit one extra 0.1 s command hold.

All other reviewed apparatus findings retain their reviewed status.
'''
review=f'''# Independent apparatus review — exact 05abf604 checkpoint

**Registered:** 2026-09-24, at Jason's explicit instruction. This note records the supplied independent review; it does not rerun it.

{status}

The unchanged P baseline is `{P}`. Scientific status remains **UNCOMMISSIONED / UNTESTED**. The apparatus hold is not a P mechanism failure or a scientific result.

## Source and blocker identities

The [complete independent review](../{B}/{reportname}) and [receipt](../{B}/REVIEW_RECEIPT.json) give the source disposition **HOLD BEFORE COUPLING COMMISSIONING**. Jason's requested live label is **ENGINEERING HOLD** for the commissioning apparatus. A1 corresponds to the review's **A-R1**; A2 corresponds to **A-R2**. Original source IDs and text are preserved. These blocker aliases are distinct from the physical-ceiling A1–A5 case labels and P's historical R1–R3 findings.

| Blocker | Scope of independently reported defect | Reviewed closure requirement; not authority to repair |
|---|---|---|
| A1 / A-R1 | A valid but unapproved arm/controller can pass the same grant; prescribed route is outside the bound manifest and can change commands without changing that manifest | Bind the complete immutable execution contract, including arm/controller/route/settings and relevant identities, before output; preserve across restart; add rejection controls |
| A2 / A-R2 | At the nominal 0.1 s decision boundary, accumulated time can be `0.09999999999999999`; the route deadline then misses stage advancement or final stop and permits another ten native steps | Use a numerically faithful due-time comparison; test the exact accumulated boundary, final-entry stop and a clearly-not-due control |

The report locates these in the apparatus approval/controller paths. It keeps the reviewed native scheduler, command-hold/restart mechanisms and other controls verified within their tested scope, with these explicit exceptions. Passing component suites does not close the two uncovered defects.

## All source dispositions retained

The following is the independent report's concise closure table, reproduced without changing classifications. Source finding IDs are intentionally retained.

{table}

## Evidence attribution and preservation

The independent reviewer reports both 83-test suites passing, all 16 delivered fault/control pairs reproduced, an additional consequential SO-firewall pair, fixed-state/receiver checks and exact saved-record reconstruction. It reports 792 prior artifacts preserved and no target modification or commissioning execution. Those are **the reviewer's findings**, not new results from this intake. This intake read the complete main review and verified archive custody; it executed none of the included commands, probes, tests, launchers or replays.

The [original builder intake](REVIEW-P-APPARATUS-05abf604-2026-09-24-73c9ad61.md) remains unchanged as the earlier awaiting-review record. The current independent disposition supersedes that pending review state for this exact apparatus checkpoint. The independently verified P baseline and the d5f7efbe/f7eb6f27 engineering-history branches retain their own dispositions. Candidate documents, all alternative families, earlier decisions and original sources are unchanged.

The review's proposed corrections and reruns are future work requiring their own authority. This registration does not begin commissioning, select Stage 1, authorize fixes, revise P, change configuration or freeze an evidential coupling. The synthetic authority file inside the ZIP is manufactured probe data and is explicitly **not Jason authorization**.

[Source identities](../{S}/SOURCE_IDENTITIES.json) · [Intake completion and validation](../{S}/INTAKE_RECORD.md) · [Original review ZIP](../{B}/{Z.name}).
'''
write(ROOT/'NEW'/R,review)
nav=f'''## Current independent apparatus review — 2026-09-24

{status}

[Independent review and retained finding table]({R}) · [Original full report]({B}/{reportname}) · [Intake and custody]({S}/INTAKE_RECORD.md).

The review calls the blockers A-R1 and A-R2; A1/A2 above are Jason's requested aliases. P remains at `6bc9683b54e4fa80136fe8534d7713e2a250a95f`, scientifically **UNCOMMISSIONED / UNTESTED**. The earlier apparatus-build “awaiting review” entry below is preserved history. No repair, commissioning execution, tuning or freeze is authorized by this registration.

'''
for name in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    t=(ROOT/'BEFORE'/name).read_text(encoding='utf-8-sig');first,rest=t.split('\n',1)
    rest=rest.replace('## P commissioning apparatus — 2026-09-24','## Preserved apparatus-build intake — before independent review',1)
    write(ROOT/'AFTER'/name,first+'\n\n'+nav+rest.lstrip('\n'))
t=(ROOT/'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig');first,rest=t.split('\n',1)
note=f'''## Current apparatus review — 2026-09-24

Jason has registered the [independent review]({R}) of exact apparatus commit `05abf60401d08f38750bca589b1c040e10513d7b` as **ENGINEERING HOLD**. A1 (source A-R1) concerns incomplete arm/controller/route approval binding; A2 (source A-R2) concerns a stage clock comparison that may permit one extra 0.1 s command hold. P implementation remains unchanged / previously verified at `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; commissioning execution is **NOT STARTED**. All other reviewed findings retain their source classifications.

This current disposition supersedes the earlier awaiting-independent-review navigation below, whose dated history remains preserved. Registration authorizes no repair, further component execution, commissioning, tuning, Git operation or freeze. Original sources, candidates and earlier decisions remain unchanged.

'''
write(ROOT/'AFTER/AGENTS.md',first+'\n\n'+note+rest.lstrip('\n'))
register=(ROOT/'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
register+='\n## Independent P apparatus review intake — 2026-09-24\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries:register+=f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
register+=f'\nApparatus `{CP}`: **ENGINEERING HOLD**, blockers A1/A-R1 and A2/A-R2. P unchanged / previously verified; commissioning **NOT STARTED**. [Recorded review and complete finding table]({R}) · [Intake validation]({S}/INTAKE_RECORD.md). Prior identities, source dispositions and checkpoint history remain preserved.\n'
write(ROOT/'AFTER/SOURCE_REGISTER.md',register)

verification={'incoming_zip':str(Z),'zip_bytes':Z.stat().st_size,'zip_sha256':sha(Z.read_bytes()),'archive_members':len(names),
    'manifest_payloads_verified':len(mf['files']),'crc_passed':True,'report_matches_review_receipt':True,
    'apparatus_checkpoint':CP,'p_baseline_checkpoint':P,'nested_builder_zip_matches_prior':True,'nested_builder_payloads_verified':len(nm['files']),
    'review_findings':[{'user_id':'A1','source_id':'A-R1'},{'user_id':'A2','source_id':'A-R2'}],
    'other_finding_table_preserved_verbatim':True,'review_rerun':False,'scientific_execution':False,'git_operations':False}
session=ROOT/'NEW'/S
dump(session/'SOURCE_IDENTITIES.json',{'sources':entries,'verification':verification,'review_receipt':receipt})
record=f'''# Independent apparatus review — intake completion

**Session:** `{ID}`; 2026-09-24. **Scope:** Jason's explicit registration/status instruction for `{CP}`.

{status}

Registered the [independent apparatus review](../../{R}), with A1 → source A-R1 and A2 → source A-R2. The complete source closure table is retained verbatim in the authored wrapper; no other reviewed status is downgraded, closed, reopened or silently reclassified. The source report and entire delivery remain unchanged.

Preserved the incoming ZIP and five reading/metadata files as SRC-077–082 in a unique source batch. Updated live AGENTS, research map, workspace status and source indexes. The preceding builder-intake review remains unchanged; its “awaiting review” navigation is marked historical. Prior P engineering checkpoints, candidate documents, all alternatives and decision records remain unchanged. No new mechanism or execution decision was created.

Read the current workbench instructions/navigation/status and the complete independent main report, intake README and review receipt. Parsed and hash-checked the complete file manifest and nested original builder payload. This was source intake, not a fresh independent code review. The source reports independently reproduced suites and faults; those executions were not repeated here.

The archive has {len(names)} members, including {len(mf['files'])} inventoried payloads; all lengths/SHA-256 match, and CRC validation passed. The report matches its receipt. The nested builder ZIP matches the already registered 5,790,938-byte original, and all {len(nm['files'])} nested payload identities match. No external ZIP checksum/verification sidecar was present in the supplied inbox folder; the outer SHA-256 is this intake's computed custody identity, not a comparison with an unavailable sidecar.

[SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json) records exact custody and [VALIDATION.json](VALIDATION.json) records final link/shared-file/preservation checks. A local recovery ZIP retains the preceding five shared notes/indexes. Portable copies preserve the intake's relative links and include the unchanged review delivery.

No target repository, vault settings, Atlas database or unrelated activity was inspected or changed. No source/program, probe, test, replay, controller or scientific run was executed; no fix, tuning, experiment number, preregistration, Git operation or freeze occurred. Synthetic authority material remains historical test data, not authorization. Intake complete; stop.
'''
write(session/'INTAKE_RECORD.md',record)
dump(ROOT/'PLAN.json',{'session':S,'batch':B,'review':R,'export':f'EXPORTS/{ID}','live_before':before,'protected_before':protected,'source_entries':entries,'verification':verification,'zip_source':str(Z)})
print(json.dumps({'members':len(names),'verified_payloads':len(mf['files']),'nested_verified':len(nm['files']),'protected':len(protected),'new_sources':[e['source_id'] for e in entries]}))
