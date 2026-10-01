"""Documentation packaging only. Does not import or execute research modules."""
from pathlib import Path
import json, hashlib, shutil, re
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
REQUEST=Path(r'C:\Users\Jason\.codex\attachments\36f043f0-2a46-4cfc-8549-c0980b264a45\Pasted text.txt')
ID='2026-09-23-p-commissioning-design-2fb3ff84'
SESSION=f'50_SESSIONS/{ID}'
BATCH='90_SOURCES/p_commissioning_design_authority_2026-09-23_2fb3ff84'
sha=lambda b:hashlib.sha256(b).hexdigest()
def put(path,text):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(text,encoding='utf-8',newline='\n')
def dump(path,obj): put(path,json.dumps(obj,indent=2,ensure_ascii=False)+'\n')

package=ROOT/'PACKAGE'
package.mkdir(exist_ok=True)
refs=package/'REFERENCES'
shutil.copytree(ROOT/'REFERENCE_READS',refs,dirs_exist_ok=True)
ids=json.loads((ROOT/'READING_COPY_IDENTITIES.json').read_text())
manifest=json.loads((ROOT/'INNER_MANIFEST_SHAPE.json').read_text())
matched=[]
for entry in ids['files']:
    b=(refs/entry['path']).read_bytes()
    assert sha(b)==entry['sha256'] and len(b)==entry['bytes']
    if entry['path']!='ARTIFACT_MANIFEST.json':
        assert manifest[entry['path']]=={'bytes':len(b),'sha256':sha(b)}
        matched.append(entry['path'])
assert len(matched)==54
report=WB/'90_SOURCES/p_final_r1p_review_2026-09-23_08df839e/LOOM_P_FINAL_INDEPENDENT_R1P_FIDELITY_REVIEW.md'
assert sha(report.read_bytes())=='8e9bcddfd19bcd1cc362f93186d6656ed0ee9f75b78fad4c8ef02ec1962e3a25'
shutil.copyfile(report,refs/report.name)
shutil.copyfile(REQUEST,refs/'COMMISSIONING_DESIGN_REQUEST.txt')
dump(package/'READING_COPY_IDENTITIES.json',ids)

smoke=json.loads((refs/'developmental_ecology/artifacts/smoke-birth_30s-attempt-004/manifest.json').read_text())
stored=sum(f['bytes'] for f in smoke['files'].values())
rates={'wall_seconds_per_simulated_second':smoke['wall_seconds']/30,
       'stored_bytes_per_simulated_second':stored/30,
       'uncompressed_bytes_per_simulated_second':smoke['uncompressed_bytes']/30}
rows={}
for name,seconds in [('physical',3080),('perceptual',1080),('intact_P',2400),('fixed_structure_if_approved',2400),('total',8960)]:
    rows[name]={'simulated_seconds':seconds,'estimated_machine_hours':seconds*rates['wall_seconds_per_simulated_second']/3600,
                'estimated_stored_GB':seconds*rates['stored_bytes_per_simulated_second']/1e9,
                'estimated_uncompressed_GB':seconds*rates['uncompressed_bytes_per_simulated_second']/1e9}
dump(package/'COMPUTE_ESTIMATE.json',{'status':'arithmetic estimate only; no research execution',
    'source':'REFERENCES/developmental_ecology/artifacts/smoke-birth_30s-attempt-004/manifest.json',
    'recorded_simulated_seconds':30,'recorded_wall_seconds':smoke['wall_seconds'],
    'recorded_stored_file_bytes':stored,'recorded_uncompressed_record_bytes':smoke['uncompressed_bytes'],
    'rates':rates,'proposed_workloads':rows,
    'limitations':['Short-run extrapolation, not measured commissioning performance.',
    'Full-P rate used as planning proxy for external-controller traces.',
    'Human operator time, apparatus development, preparation and extra diagnostic overhead excluded.',
    'Twofold machine/bytes allowance and second preserved copy are proposed budget margins, not observations.']})

config=json.loads((refs/'developmental_ecology/configuration.json').read_text())
rules=(ROOT/'P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md').read_text(encoding='utf-8')
missing=[key for key in config if f'`{key}`' not in rules]
assert not missing, missing

live=['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md']
before={}
for name in live:
    b=(WB/name).read_bytes()
    before[name]={'sha256':sha(b),'bytes':len(b)}
    dst=ROOT/'LIVE_BEFORE'/name
    dst.parent.mkdir(parents=True,exist_ok=True)
    dst.write_bytes(b)
catalog=json.loads((ROOT/'LIVE_BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
assert len(catalog['source_files'])==60
assert sum(e['source_id']=='SRC-057' for e in catalog['source_files'])==1
assert sum(e['source_id']=='SRC-058' for e in catalog['source_files'])==1
req=REQUEST.read_bytes()
entry={'source_id':'SRC-061','path':BATCH+'/Pasted text.txt','original_filename':'Pasted text.txt',
       'bytes':len(req),'sha256':sha(req),'role':'user-commissioning-design-authority',
       'authority':'Jason: commissioning design and scoped registration/status only; no execution or mechanism/configuration/canon changes',
       'received_on':'2026-09-23','source_date':'not separately stated','stated_author':'Jason (user-provided request)',
       'acquired_from':str(REQUEST),'reviewed_checkpoint':'6bc9683b54e4fa80136fe8534d7713e2a250a95f',
       'record':SESSION+'/COMPLETION_REPORT.md','notes':'Byte-identical request; proposals in the resulting design remain awaiting review.'}
catalog['source_files'].append(entry)
catalog.setdefault('intake_events',[]).append({'session_id':ID,'source_ids':['SRC-061'],
    'existing_review_source_ids':['SRC-057','SRC-058','SRC-059','SRC-060'],
    'record':SESSION+'/COMPLETION_REPORT.md','scope':'Design-only commissioning contribution; final review already registered; no duplicate review or execution'})
assert catalog['source_files'][:-1]==json.loads((ROOT/'LIVE_BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))['source_files']
dump(ROOT/'LIVE_AFTER/SOURCE_CATALOG.json',catalog)

nav=f'''## Current commissioning design — 2026-09-23 (review draft)

Jason has authorized **design only** for coupling commissioning of exact P checkpoint `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. The [request](90_SOURCES/p_commissioning_design_authority_2026-09-23_2fb3ff84/Pasted%20text.txt) is registered as SRC-061. The engineering disposition remains **FIT TO PROCEED TO COUPLING COMMISSIONING**; scientific status remains **UNCOMMISSIONED / UNTESTED**.

[Technical design]({SESSION}/P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md) · [Plain-language walkthrough]({SESSION}/P_COMMISSIONING_PLAIN_LANGUAGE_WALKTHROUGH_v0_1.md) · [Proposed matrix]({SESSION}/P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md) · [Decisions before execution]({SESSION}/DECISIONS_REQUIRED_BEFORE_EXECUTION.md) · [Change rules]({SESSION}/P_COMMISSIONING_CONFIGURATION_CHANGE_RULES_v0_1.md) · [Completion and source identities]({SESSION}/COMPLETION_REPORT.md).

All commissioning procedures, sample counts, controller choices and budgets are assistant proposals awaiting Jason's review. No commissioning was performed; no apparatus coding, run, configuration change or freeze is authorized by this design request. The proposed extended runner and optional fixed-structure diagnostic require separate authority. The final independent review was already registered; the earlier d5f7efbe/f7eb6f27 engineering holds, source files and decision history remain unchanged.

'''
for name in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md']:
    old=(ROOT/'LIVE_BEFORE'/name).read_text(encoding='utf-8-sig')
    first,rest=old.split('\n',1)
    put(ROOT/'LIVE_AFTER'/name,first+'\n\n'+nav+rest.lstrip('\n'))
old=(ROOT/'LIVE_BEFORE/AGENTS.md').read_text(encoding='utf-8-sig')
first,rest=old.split('\n',1)
note=f'''## Scoped continuation — 2026-09-23 coupling commissioning design

Jason's [registered request](90_SOURCES/p_commissioning_design_authority_2026-09-23_2fb3ff84/Pasted%20text.txt) authorizes a **design-only** commissioning contribution and the necessary review/status navigation for exact checkpoint `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Its independently verified engineering status is fit to proceed to coupling commissioning; scientific status remains uncommissioned/untested. See [the contribution]({SESSION}/P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md) and [pending execution decisions]({SESSION}/DECISIONS_REQUIRED_BEFORE_EXECUTION.md).

This narrow continuation permits the design documents; it does not authorize controllers, lifetimes, simulations, code, configuration/world/mechanism changes, Git operations, canon changes or an evidential freeze. Earlier scope statements below retain their dated meaning. Preserve prior checkpoint dispositions, all sources and all candidate alternatives. Proposed commissioning settings remain proposals until Jason decides.

'''
put(ROOT/'LIVE_AFTER/AGENTS.md',first+'\n\n'+note+rest.lstrip('\n'))
register=(ROOT/'LIVE_BEFORE/SOURCE_REGISTER.md').read_text(encoding='utf-8-sig')
register+=f'''\n## P coupling commissioning design authority — 2026-09-23

| ID | Source | Identity and scope |
|---|---|---|
| SRC-061 | [Pasted text.txt]({BATCH}/Pasted%20text.txt) | {len(req)} bytes; SHA-256 `{sha(req)}`. Jason's design-only request for the exact 6bc9683b checkpoint; no commissioning execution, changed configuration or scientific claim authorized. |

The final independent review remains registered once as SRC-057–060. [New design contribution]({SESSION}/P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md) · [Completion report]({SESSION}/COMPLETION_REPORT.md). Existing source identity rows, review checkpoints and accepted decision records remain unchanged.
'''
put(ROOT/'LIVE_AFTER/SOURCE_REGISTER.md',register)

protected={}
for dirname in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS']:
    for p in (WB/dirname).rglob('*'):
        if p.is_file(): protected[p.relative_to(WB).as_posix()]=sha(p.read_bytes())
for dirname in ['2026-09-23-p-engineering-review-284c3913','2026-09-23-p-post-correction-intake-1677619b','2026-09-23-p-final-r1p-intake-08df839e']:
    for p in (WB/'50_SESSIONS'/dirname).rglob('*'):
        if p.is_file(): protected[p.relative_to(WB).as_posix()]=sha(p.read_bytes())
dump(ROOT/'PUBLISH_PLAN.json',{'workbench':str(WB),'session':SESSION,'export':f'EXPORTS/{ID}','batch':BATCH,
    'live_before':before,'protected_before':protected,'request_entry':entry})
dump(package/'SOURCE_IDENTITIES.json',{'checkpoint':'6bc9683b54e4fa80136fe8534d7713e2a250a95f',
    'authority_request':entry,'final_review':{'catalog_id':'SRC-057','path':str(report),'bytes':report.stat().st_size,'sha256':sha(report.read_bytes())},
    'outer_archive':{'catalog_id':'SRC-058','path':ids['outer_zip'],'sha256':ids['outer_sha256']},
    'nested_archive':{'member':ids['inner_member'],'sha256':ids['inner_sha256']},
    'runtime_sha256':smoke['code']['sha256'],'config_semantic_sha256':smoke.get('configuration_sha256',smoke.get('config_sha256')),
    'configuration_file_sha256':sha((refs/'developmental_ecology/configuration.json').read_bytes()),
    'reading_copy_count':len(ids['files']),'reading_copy_manifest_matches':len(matched),
    'note':'ARTIFACT_MANIFEST.json itself is covered by nested archive custody, not by a self-referential manifest row. Original reference files are copied unchanged; none was executed.'})
for p in ROOT.glob('*.md'): shutil.copyfile(p,package/p.name)
dump(ROOT/'PREPARATION_VALIDATION.json',{'status':'prepared; workbench not yet written','source_reading_copy_count':len(ids['files']),
    'nested_manifest_payloads_verified':len(matched),'all_configuration_fields_covered':len(config),'missing_configuration_fields':missing,
    'protected_existing_files':len(protected),'live_files_prepared':live,'estimate':rows['total']})
print(json.dumps({'source_copies_verified':len(ids['files']),'configuration_keys_covered':len(config),'protected_files':len(protected),'stored_30s_bytes':stored,'total':rows['total']}))
