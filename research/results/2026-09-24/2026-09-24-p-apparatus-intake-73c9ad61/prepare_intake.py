"""Read/hash/register an archive as documentation. Never executes package code."""
from pathlib import Path, PurePosixPath
from urllib.parse import quote
import json,hashlib,zipfile,re,shutil

ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ID='2026-09-24-p-apparatus-intake-73c9ad61'
S=f'50_SESSIONS/{ID}'
B='90_SOURCES/p_commissioning_apparatus_2026-09-24_73c9ad61'
R='30_REVIEWS/REVIEW-P-APPARATUS-05abf604-2026-09-24-73c9ad61.md'
D='40_DECISIONS/DECISION-P-APPARATUS-SCOPE-2026-09-24-73c9ad61.md'
Z=WB/'INBOX/2026-09-24-p-commissioning-apparatus/Loom_P_Commissioning_Apparatus_Review_20260924.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
def write(p,text):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text,encoding='utf-8',newline='\n')
def dump(p,x):write(p,json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def link(label,filename,prefix='../'):return f'[{label}]({prefix}{B}/{quote(filename)})'

z=zipfile.ZipFile(Z)
assert sha(Z.read_bytes())=='87f4dbde39a72559caf6045c7ac68a649d9691a000d1569af5d26b090a63b053'
names=z.namelist();assert len(names)==len(set(names))
for name in names:
    p=PurePosixPath(name);assert not p.is_absolute() and '..' not in p.parts and ':' not in name and '\\' not in name
manifest=json.loads(z.read('ARTIFACT_MANIFEST.json'))
assert set(manifest['files'])==set(names)-{'ARTIFACT_MANIFEST.json'}
for name,info in manifest['files'].items():
    data=z.read(name);assert len(data)==info['bytes'] and sha(data)==info['sha256'],name
assert z.testzip() is None
cp=json.loads(z.read('CHECKPOINT.json'))
assert cp['checkpoint']=='05abf60401d08f38750bca589b1c040e10513d7b'
assert cp['parent']=='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
assert sha(z.read('APPARATUS.patch'))==cp['patch_sha256']
patchpaths=re.findall(r'^diff --git a/(.*?) b/',z.read('APPARATUS.patch').decode('utf-8'),re.M)
for name,h in cp['p_code']['files'].items():assert sha(z.read('developmental_ecology/loom_p/'+name))==h
for name,h in cp['apparatus']['files'].items():assert sha(z.read('developmental_ecology/loom_commissioning/'+name))==h
old=WB/'50_SESSIONS/2026-09-23-p-commissioning-design-2fb3ff84/REFERENCES/developmental_ecology'
for name in cp['p_code']['files']:assert z.read('developmental_ecology/loom_p/'+name)==(old/'loom_p'/name).read_bytes()
assert z.read('developmental_ecology/configuration.json')==(old/'configuration.json').read_bytes()
ref='developmental_ecology/artifacts/apparatus-20260924-01a0c405/references/'
for name in ['P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md','P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md','P_COMMISSIONING_PLAIN_LANGUAGE_WALKTHROUGH_v0_1.md','P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md','DECISIONS_REQUIRED_BEFORE_EXECUTION.md']:
    assert z.read(ref+name)==(WB/'50_SESSIONS/2026-09-23-p-commissioning-design-2fb3ff84'/name).read_bytes(),name
assert sha(z.read(ref+'Loom_P_Coupling_Commissioning_Design_20260923_2fb3ff84.zip'))=='018f23d8e1bdb9433d7a50c8e421f09deb70d26febc3a5f14d98fa3b467551d0'
faults=json.loads(z.read('docs/developmental_ecology/p_apparatus_20260924/FAULT_MATRIX.json'))
assert len(faults)==16
for f in faults: assert f['RED']['exit']!=0 and f['RED']['intended'] and f['GREEN']['exit']==0 and f['GREEN']['intended']
faultlogcheck=[]
for f in faults:
    for phase in ['RED','GREEN']:
        log='developmental_ecology/artifacts/apparatus-20260924-01a0c405/faults-attempt-002/'+f['fault']+'-'+phase+'.log'
        assert log in names
        txt=z.read(log).decode('utf-8-sig')
        assert ('failed' in txt if phase=='RED' else 'passed' in txt),log
    faultlogcheck.append(f['fault'])

live=['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md','40_DECISIONS/DECISION_INDEX.md']
before={}
for name in live:
    data=(WB/name).read_bytes();before[name]={'bytes':len(data),'sha256':sha(data)}
    p=ROOT/'BEFORE'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
protected={}
for folder in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS','50_SESSIONS/2026-09-23-p-commissioning-design-2fb3ff84']:
    for p in (WB/folder).rglob('*'):
        if p.is_file() and p.relative_to(WB).as_posix() not in live:protected[p.relative_to(WB).as_posix()]=sha(p.read_bytes())

sources=ROOT/'SOURCE_BATCH';sources.mkdir(exist_ok=True)
shutil.copyfile(Z,sources/Z.name)
base='docs/developmental_ecology/p_apparatus_20260924/'
selected=[('START_HERE.md','delivery-reading-note'),('CHECKPOINT.json','apparatus-checkpoint-metadata'),('ARTIFACT_MANIFEST.json','delivery-custody-manifest'),
    (base+'BUILD_REPORT.md','builder-apparatus-construction-report'),(ref+'APPARATUS_BUILD_REQUEST.txt','packaged-user-build-authority'),
    (base+'AUTHORITY_AND_INFORMATION_FLOW.md','builder-information-flow-record'),(base+'PLAIN_LANGUAGE_WALKTHROUGH.md','builder-apparatus-walkthrough'),
    (base+'LAW_CODE_TEST_MAP.md','builder-verification-map'),(base+'EXECUTION_LEDGER.md','builder-execution-ledger'),
    (base+'SOURCE_IDENTITIES.json','builder-source-custody-record'),(base+'RUNTIME_STORAGE_ESTIMATE.json','builder-runtime-storage-estimate'),
    (base+'RUNTIME_RECORD.json','builder-runtime-record'),(base+'UI_REVIEW.json','builder-ui-review-record'),(base+'FAULT_MATRIX.json','builder-fault-verification-record')]
catalog=json.loads((ROOT/'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
assert len(catalog['source_files'])==61
entries=[]
for i,(member,role) in enumerate([(None,'apparatus-build-review-delivery-archive')]+selected,62):
    filename=PurePosixPath(member).name if member else Z.name
    data=z.read(member) if member else Z.read_bytes()
    (sources/filename).write_bytes(data)
    e={'source_id':f'SRC-{i:03d}','path':B+'/'+filename,'original_filename':filename,'bytes':len(data),'sha256':sha(data),'role':role,
       'source_date':'2026-09-24 (delivery/build-report date; individual timestamp not independently established)',
       'stated_author':'Jason, as reproduced in packaged user build request' if role=='packaged-user-build-authority' else 'Builder; exact model/backend not stated in these report headers',
       'authority':'Historical apparatus-construction and bounded engineering-fixture scope only' if role=='packaged-user-build-authority' else 'Builder-provided report/evidence, not independent apparatus approval or commissioning authority',
       'acquired_from':str(Z)+('::'+member if member else ''),'archive_member':member,
       'apparatus_checkpoint':cp['checkpoint'],'p_baseline_checkpoint':cp['parent'],'intake_record':S+'/INTAKE_RECORD.md'}
    entries.append(e)
catalog['source_files']+=entries
catalog.setdefault('intake_events',[]).append({'session_id':ID,'source_ids':[e['source_id'] for e in entries],
    'review_note':R,'decision_record':D,'record':S+'/INTAKE_RECORD.md',
    'scope':'Source intake and reported apparatus-construction status; original P baseline/history retained; no execution or independent fidelity approval'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)

review=f'''# P commissioning apparatus — build intake, awaiting independent review

**Intake date:** 2026-09-24  
**Apparatus checkpoint:** `{cp['checkpoint']}`  
**Parent / unchanged P baseline:** `{cp['parent']}`  
**Apparatus status:** BUILDER REPORTS CONSTRUCTION AND BOUNDED COMPONENT VERIFICATION COMPLETE — AWAITING INDEPENDENT REVIEW  
**Commissioning:** NOT BEGUN / NOT AUTHORIZED  
**Scientific status:** UNCOMMISSIONED / UNTESTED

This is an intake and custody record, not a new independent code/fidelity review. The supplied {link('build report','BUILD_REPORT.md')} explicitly stops at apparatus review. The archive's name contains “Review”; it is a package **for** independent review, not an independent review verdict. The exact checkpoint is declared in {link('CHECKPOINT.json','CHECKPOINT.json')}; no local or remote Git checkout was inspected in this intake.

## What arrived

A separate commissioning package around the unchanged P runtime: extended bounded runner; deterministic privileged waypoint/wait/contact controller; sensor-only human interface; **FIXED-STRUCTURE / NO-LASTING-PLASTICITY DIAGNOSTIC**; aligned passive diagnostics and receiver analysis; AV/CO/SO interpretation separation; validators and manufactured fault fixtures. The {link('walkthrough','PLAIN_LANGUAGE_WALKTHROUGH.md')}, {link('information-flow map','AUTHORITY_AND_INFORMATION_FLOW.md')} and {link('law/code/test map','LAW_CODE_TEST_MAP.md')} explain the intended boundaries.

The packaged {link('user build request','APPARATUS_BUILD_REQUEST.txt')} records seven scoped rulings. [Their attributed authority record](../{D}) preserves those rulings without rewriting the original design. In particular, D5 now uses every practical wave handoff and a predetermined native selection rule, replacing the draft's at-most-100-samples proposal for apparatus construction. Birth IDs 1–4 and 600 s ceilings remain prospective metadata, not permission to start lives.

## Builder-reported evidence, checked as records only

| Reported item | Supplied record and limit |
|---|---|
| 83 tests passed in the worktree, 34.18 s | 24 apparatus checks plus 59 unchanged P checks; final test log is inside the original ZIP |
| 83 tests passed from the assembled portable package, 58.63 s | Separate portable log; not a fresh dependency or cross-platform validation |
| 16 intended RED→GREEN fault pairs | {link('Fault matrix','FAULT_MATRIX.json')} and individual logs; all 16 matrix pairs and their fail/pass log summaries are present and internally consistent |
| Short manufactured components and restart/replay checks | {link('Execution ledger','EXECUTION_LEDGER.md')}; typically 0.2 s, controller checks 0.1 s, plus manufactured time/reserve boundaries. A step at clock 1,199.99 is not a 1,200 s life |
| Fixed-structure timing and discarded-update poisoning | Reported component evidence, including late bank restoration detection; not an innate-maintenance or learning outcome |
| Sensor display inspection | {link('UI record','UI_REVIEW.json')}; recorded 0.100/0.200 s E/I holding behavior, disabled saved-view controls. Native double-click launch not automated; direct file navigation was blocked in the build review |

This session only read/hash-checked packaged records. It did not execute tests, replay worlds, open launchers, serve a UI or run a controller. Earlier failed development/setup logs remain inside the unchanged archive; they are not substituted for intended-fault RED evidence.

## What this intake verified directly

The incoming ZIP is {Z.stat().st_size:,} bytes with SHA-256 `{sha(Z.read_bytes())}`. All **{len(manifest['files'])} payload entries** matched the delivered manifest in byte length and SHA-256; the archive contains {len(names)} members including the manifest. Its CRC check passed. There is no supplied external checksum sidecar to compare; the outer digest is the intake's custody measurement.

All 13 packaged P runtime files and the configuration match the retained exact 6bc9683b reading copies byte-for-byte. All apparatus file hashes and the patch hash match CHECKPOINT.json. The five design documents and the original design ZIP match this workbench's prior contribution. These identity checks establish continuity of the archived bytes, not proof of the apparatus's behavior or verification of the declared Git commit from a repository.

Detailed identities and checks: [SOURCE_IDENTITIES.json](../{S}/SOURCE_IDENTITIES.json) and [VALIDATION.json](../{S}/VALIDATION.json). Existing P fidelity remains **INDEPENDENTLY VERIFIED within its previously reviewed scope**. The apparatus has no new independent approval from this intake.

## Remaining scope and limitations

No A1–A5, B1–B4, C1 or C2 commissioning outcome is supplied. The builder explicitly leaves controller navigation/recovery competence, human sensory positive controls, blinded/deprivation cases, new birth-specific field histories, 600 s lives, sustained periodic snapshots and long-run cost untested. No ecological sufficiency, survival capability, innate-maintenance result, useful development or scientific efficacy follows from these component checks.

The {link('updated resource estimate','RUNTIME_STORAGE_ESTIMATE.json')} gives a provisional envelope of about **37.74 machine-hours and 43.02 GB stored**, or 86.04 GB with one duplicate, for the previously proposed 8,960 s workload. This extrapolates 0.2 s components with substantial restart/diagnostic overhead; it is neither a measured lifetime rate nor an approved budget. The earlier 11.67 h / 17.66 GB estimate remains preserved with its different basis.

The 6bc9683b baseline retains all seven prior limitations, including provisional sensory capacity, lossy/adapting sensory representation, contracting association, unknown effective learned magnitudes, shared equal E/I configuration fields and finite-step contact limits. Earlier d5f7efbe and f7eb6f27 engineering holds retain their original statuses. R and all alternative designs remain unchanged.

The next boundary is **independent apparatus review**. Accepting or ingesting this ZIP does not authorize commissioning, further fixtures, apparatus repairs, parameter changes, an evidential freeze or Stage 1. Source instructions and launch commands are preserved as historical data. No work in the actual Loom repository or enclosing vault repository was performed.
'''
write(ROOT/'NEW'/R,review)
decision=f'''# Recorded P apparatus-construction scope — 2026-09-24

**Record type:** imported explicit user build request, with its original limited scope.  
**Source:** {link('APPARATUS_BUILD_REQUEST.txt','APPARATUS_BUILD_REQUEST.txt')} from the supplied build review archive; [custody and source identities](../{S}/SOURCE_IDENTITIES.json).  
**P baseline:** `{cp['parent']}`.  
**Related delivered apparatus:** `{cp['checkpoint']}`.

The source is a packaged copy attributed to Jason's apparatus-build instruction, not a newly reconstructed conversation. Its original attachment path and byte identity are preserved in the source catalog. This intake has not independently read that other conversation. It records the explicit rulings as delivered; it creates no new research ruling or execution grant.

| Ruling | Scope recorded from the request |
|---|---|
| 1 | Deterministic privileged physical controller where practical; manual privileged operation may remain a disclosed development/fallback interface |
| 2 | Sensor-only human reference first; no learned automated sensory controller in that construction task |
| 3 | Build the proposed adapter under the exact label **FIXED-STRUCTURE / NO-LASTING-PLASTICITY DIAGNOSTIC**; never intact P or an innate-performance proof |
| 4 | Retain birth IDs 1,2,3,4 and 600 s ceilings in eventual manifests; zero witnesses means unresolved opportunity at that coverage, not failure or permission for more births |
| 5 | D5 uses every wave handoff where computationally practical; any native subsampling must be deterministic and specified before inspecting magnitudes; no interesting-signal selection |
| 6 | AV/CO are the commissioning decision surface; preserve SO observations but reject SO as apparatus grounds for configuration adjustment before freeze |
| 7 | Preserve the eight-unit/two-pool baseline, mean-plus-endpoint packet, centring, contracting association and all other P laws; no sweep or mechanism revision |

The request accepts the commissioning framework **for apparatus construction and minimum bounded manufactured engineering verification only**. It prohibits A1–A5/B1–B4/C1/C2 executions, 600 s lives, commissioning, tuning, experiment numbers, scientific preregistration and push/PR/merge. The builder reports completion of that limited construction. No standing permission is inherited by the intake session or a future execution task.

These rulings supersede the earlier draft's conflicting controller/D5 proposals only within the stated construction scope. The five original design documents and their earlier “pending” labels remain unchanged historical drafts. D1–D3 remain accepted in their prior record; no P/R synthesis or new mechanism selection is made. Exact starts/routes/phases, operator controls, cases, resource authorization and any eventual evidential freeze remain later decisions. [Apparatus status and limitations](../{R}).
'''
write(ROOT/'NEW'/D,decision)

nav=f'''## P commissioning apparatus — 2026-09-24

Apparatus checkpoint `05abf60401d08f38750bca589b1c040e10513d7b`, parent P baseline `6bc9683b54e4fa80136fe8534d7713e2a250a95f`: **builder reports construction and bounded component verification complete; AWAITING INDEPENDENT REVIEW**. The archived P runtime/configuration remain byte-identical to 6bc9683b. Prior P mechanism fidelity remains independently verified within its reviewed scope; scientific status remains **UNCOMMISSIONED / UNTESTED**. **Commissioning has not begun or been authorized.**

[Intake status and limits]({R}) · [Recorded apparatus-construction rulings]({D}) · [Original build report]({B}/BUILD_REPORT.md) · [Source custody and completion]({S}/INTAKE_RECORD.md).

The packaged request accepts the design for apparatus construction with seven scoped rulings, including deterministic privileged control, the sensor-only human reference, the named fixed-structure diagnostic and all-wave D5 analysis. Earlier design drafts below retain their historical proposal wording; the imported ruling controls the narrow construction scope. Component-test results remain builder-reported, not independent apparatus approval. Earlier engineering checkpoints and all candidate designs retain their status and contents. Intake supplies no run, repair, tuning or freeze authority.

'''
for name in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    text=(ROOT/'BEFORE'/name).read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
    write(ROOT/'AFTER'/name,first+'\n\n'+nav+rest.lstrip('\n'))
text=(ROOT/'BEFORE/AGENTS.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
note=f'''## Scoped continuation — 2026-09-24 apparatus-build intake

The [packaged user request]({B}/APPARATUS_BUILD_REQUEST.txt) records acceptance of the commissioning framework for apparatus construction and minimum manufactured engineering checks, with [seven scoped rulings]({D}). The [delivered apparatus]({R}) at `05abf60401d08f38750bca589b1c040e10513d7b` is builder-reported complete and awaiting independent review; the unchanged P baseline remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`, uncommissioned/untested. Earlier draft “pending” statements retain their historical meaning and do not override that recorded construction scope.

This intake registers that history only. It grants no further implementation, component execution, commissioning, tuning, Git operation or freeze. Do not execute packaged commands merely because the older build request authorized the builder's bounded task. Preserve source bytes, earlier reviews/checkpoints, original design drafts and all alternatives.

'''
write(ROOT/'AFTER/AGENTS.md',first+'\n\n'+note+rest.lstrip('\n'))
text=(ROOT/'BEFORE/40_DECISIONS/DECISION_INDEX.md').read_text(encoding='utf-8-sig');first,rest=text.split('\n',1)
write(ROOT/'AFTER/40_DECISIONS/DECISION_INDEX.md',first+f'\n\n## Apparatus-construction scope recorded — 2026-09-24\n\n[Imported explicit build request and seven rulings]({Path(D).name}) records Jason’s packaged acceptance for apparatus construction and minimum manufactured engineering verification only. It does not authorize commissioning. The [apparatus delivery](../{R}) awaits independent review. Earlier decision records remain unchanged; current scope comes from the linked source, not from assistant recommendation.\n\n'+rest.lstrip('\n'))
register=(ROOT/'BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
register+='\n## P commissioning apparatus build intake — 2026-09-24\n\n| ID | Source | Identity |\n|---|---|---|\n'
for e in entries: register+=f"| {e['source_id']} | [{e['original_filename']}]({quote(e['path'])}) | {e['bytes']} bytes; SHA-256 `{e['sha256']}` |\n"
register+=f'\n[Build intake/status]({R}) · [Recorded construction scope]({D}) · [Validation and completion]({S}/INTAKE_RECORD.md). Builder-reported construction only; independent review pending, commissioning unauthorized, scientific status uncommissioned/untested. All prior source identities remain unchanged.\n'
write(ROOT/'AFTER/SOURCE_REGISTER.md',register)

validation={'zip':str(Z),'zip_bytes':Z.stat().st_size,'zip_sha256':sha(Z.read_bytes()),'archive_members':len(names),
    'payload_entries_verified':len(manifest['files']),'manifest_member_unlisted_by_design':True,'crc_passed':True,
    'checkpoint_declared':cp['checkpoint'],'parent_declared':cp['parent'],'p_runtime_files_matching_prior':13,
    'configuration_matches_prior':True,'apparatus_file_hashes_matching_checkpoint':len(cp['apparatus']['files']),
    'patch_sha256_verified':cp['patch_sha256'],'patch_paths':patchpaths,'design_documents_matching_prior':5,
    'prior_design_zip_matches':True,'fault_matrix_pairs':16,'fault_log_summaries_consistent':faultlogcheck,
    'independent_apparatus_review_performed':False,'packaged_code_executed':False,'git_operations':False}
session=ROOT/'NEW'/S;session.mkdir(parents=True,exist_ok=True)
dump(session/'SOURCE_IDENTITIES.json',{'sources':entries,'archive_check':validation,'checkpoint_metadata':cp})
dump(ROOT/'PLAN.json',{'session':S,'batch':B,'review':R,'decision':D,'export':f'EXPORTS/{ID}',
    'live_before':before,'protected_before':protected,'source_entries':entries,'verification':validation,'zip_source':str(Z)})
print(json.dumps({'members':len(names),'payloads_verified':len(manifest['files']),'source_ids':[e['source_id'] for e in entries],
    'protected_files':len(protected),'p_modules_unchanged':13,'patch_paths':patchpaths,'session':S}))
