from pathlib import Path
from urllib.parse import unquote,quote
import hashlib,json,re,shutil,os

ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
plan=json.loads((ROOT/'PLAN.json').read_text(encoding='utf-8'))
SESSION=plan['session'];BATCH=plan['batch'];REVIEW=plan['review']
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(rel,txt,group='NEW'):
 p=ROOT/group/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(txt,encoding='utf-8',newline='\n')
def add_after_title(rel,txt):
 old=(ROOT/'SHARED_BEFORE'/rel).read_bytes();sep=b'\r\n\r\n' if b'\r\n' in old else b'\n\n'
 start,rest=old.split(sep,1);addition=(txt.strip()+'\n\n').replace('\n',sep[:len(sep)//2].decode()).encode('utf-8')
 p=ROOT/'AFTER'/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(start+sep+addition+rest)

watchlink=f'[{Path(REVIEW).stem.replace("_"," ").capitalize()}]({REVIEW})'
add_after_title('00_RESEARCH_MAP.md',f'''## Standing behavioural development watchlist

{watchlink} records ten families of observable change, opportunity denominators, confounds, current evidence and unresolved causal questions. It is a live observational framework with no overall score, pass gate or required developmental sequence. Useful learned navigation remains unestablished; M1 remains non-canonical. [Establishment and validation]({SESSION}/INTEGRATION_REPORT.md).''')
add_after_title('01_WORKSPACE_STATUS.md',f'''## Watchlist established — 1 October 2026

{watchlink} is live. All ten families distinguish observable measures and opportunity from causal interpretation. Existing evidence seeds it, including the later priority H/E/I curve analysis; internal growth is not behavioural success. The original evidence and execution boundaries below are unchanged. No behavioural criterion was promoted to canon, no mechanism selected and no experiment run. [Integration record]({SESSION}/INTEGRATION_REPORT.md) · [Validation]({SESSION}/VALIDATION_REPORT.md).

Maintenance: review the watchlist during the next bounded integration after a major result, accepted design decision or substantial analysis, recording dated evidence/interpretation/measurement changes. The standing cadence is in [AGENTS.md](AGENTS.md).''')
add_after_title('02_OPEN_QUESTIONS.md',f'''## Behavioural observation questions — 1 October 2026

Use the [behavioural development watchlist]({REVIEW}) alongside the questions below. It links possible physical changes to opportunity, internal development and unresolved attribution; it does not set success criteria.

| Question | Outstanding measurement / interpretation | Watchlist connection |
|---|---|---|
| Comparable opportunity | What exposure and body-capability accounting distinguishes less harm or more intake from changed access, immobility or weakening? Preserve raw totals as well as conditioned views. | BD-01/03/05/06 |
| Re-encounter matching | How should similar organism-available pre-hazard contexts be defined without privileged object/location features, outcome selection or matching away learned change? | BD-02/08/09; promising proposed assay, not an accepted metric |
| Individual changes | Which biographies show persistent useful change, which reverse, and what later physical causal comparison could distinguish acquired influence from M1/world/support effects? | BD-04/07/10; causal effect unresolved |

The priority H/E/I curve report supports continued or renewed E-bank change in some lives and event-driven I; it does not establish useful physical causation or completion of the broader behavioural analysis. No new execution follows from these questions.''')
add_after_title('AGENTS.md',f'''## Standing workbench maintenance and watchlist cadence — 1 October 2026

Update the workbench after each major experimental result, major design decision or substantial analysis package. Prefer one bounded, dated integration after a coherent body of work rather than continuously editing shared notes during active experimentation or allowing the workbench to drift across many sessions.

Normally review the research map, workspace status, open questions, relevant candidate/review notes, [behavioural development watchlist]({REVIEW}), decision index only for actual accepted decisions, and source register/catalog. Preserve prior shared-note bytes and before/after hashes using SHARED_BEFORE and an integration-change record; confirm current hashes before replacement under the contribution protocol.

The watchlist is an evolving observational framework, not canon, a score, success criterion, mechanism selection or execution permission. Every item retains phenomenon, developmental rationale, observable measure, opportunity denominator, confounds, record availability, current evidence and causal-testing gap. During the next integration, update it when substantive evidence reveals a phenomenon, strengthens/weakens one, exposes a confound, improves a measurement or shows an item is not useful. Retain date, exact source, what changed and whether it is evidence, interpretation or proposed measurement; preserve historical versions. Do not add watchlist items to 40_DECISIONS merely because they are listed. This cadence is a contribution rule, not a scheduled automation.''')
add_after_title('30_REVIEWS/DEVELOPMENTAL_EVIDENCE_INDEX_2026-10-01_7c219ab4.md',f'''Standing live analysis: [Behavioural development watchlist](BEHAVIOURAL_DEVELOPMENT_WATCHLIST.md) — opportunity-aware phenomena and evidence, with internal H/E/I cross-references; no score or causal-success claim. [1 October establishment](../{SESSION}/INTEGRATION_REPORT.md).''')

catalog=json.loads((ROOT/'SHARED_BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
catalog['source_files'].extend(plan['new_source_rows'])
catalog['intake_events'].append({'session_id':ROOT.name,'registered':'2026-10-01','record':SESSION+'/INTEGRATION_REPORT.md','source_ids':[r['source_id'] for r in plan['new_source_rows']],'scope':'Establish live behavioural development watchlist; register instruction, priority curve report/provenance and historical passive methods. No new analysis execution, scientific authority or decision-index entry.'})
put('SOURCE_CATALOG.json',json.dumps(catalog,indent=2,ensure_ascii=False)+'\n','AFTER')
def href(path):return '<'+Path(path).as_posix()+'>' if re.match(r'^[A-Za-z]:',path) else quote(path,safe='/')
register='\n\n## Behavioural development watchlist establishment — 1 October 2026\n\n'+f'[Integration report]({SESSION}/INTEGRATION_REPORT.md). Existing source identities remain unchanged. Eleven small source copies plus one external curve archive reference; the original 4.65 GB sandbox archive is not recopied. Source protocols remain historical analysis methods/proposals, not this task’s execution instructions.\n\n| ID | Source | Custody | SHA-256 |\n|---|---|---|---|\n'
for r in plan['new_source_rows']:register+=f"| {r['source_id']} | [{r['original_filename']}]({href(r['path'])}) | {r['storage']}; {r['bytes']:,} bytes | `{r['sha256']}` |\n"
dest=ROOT/'AFTER/SOURCE_REGISTER.md';dest.write_bytes((ROOT/'SHARED_BEFORE/SOURCE_REGISTER.md').read_bytes()+register.encode('utf-8'))

watch=ROOT/'NEW'/REVIEW
refs=[]
for h in re.findall(r'\[[^\]\n]+\]\((<[^>]+>|[^\)\n]+)\)',watch.read_text(encoding='utf-8')):
 h=unquote(h.strip('<>')).split('#')[0]
 if h.startswith('../90_SOURCES/developmental_catchup_'):
  rel=(WB/'30_REVIEWS'/h).resolve().relative_to(WB).as_posix()
  if rel not in refs:refs.append(rel)
old={r['path']:r for r in json.loads((ROOT/'SHARED_BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))['source_files']}
reused=[]
for n in refs:
 r=old[n];assert sha(WB/n)==r['sha256'],n
 reused.append({'source_id':r['source_id'],'path':n,'sha256':r['sha256'],'bytes':(WB/n).stat().st_size,'reused_existing_registration':True})
identities={'session_id':ROOT.name,'date':'2026-10-01','scope':'Documentation custody; no scientific analysis rerun','new_sources':plan['new_source_rows'],'reused_sources':reused,'new_manifest_matches':plan['manifest_matches'],'curve_archive_verified_by_intake':True,'curve_report_and_manifest_match_archived_bytes':True,'all_curve_payloads_reverified':False,'original_sandbox_archive_rehashed_this_intake':False,'source_report_validation_claim':'Curve consistency review is independently coded by the same analyst, not external scientific review','missing_evidence':'No matched behavioural assay or physical causal comparison was created; incomplete original tails remain unavailable.'}
put(SESSION+'/SOURCE_IDENTITIES.json',json.dumps(identities,indent=2,ensure_ascii=False)+'\n')
srcnote=f'''# Sources and scope for watchlist revision 1

Authority: Jason's [exact instruction](../../{BATCH}/authority/Pasted%20text.txt). This is a research-organisation instruction, not a mechanism decision. [Machine-readable source identities](SOURCE_IDENTITIES.json) retain exact paths, sizes, hashes and previous source IDs.

The prior [1 October catch-up](../2026-10-01-developmental-evidence-catchup-7c219ab4/INTEGRATION_REPORT.md) supplies the registered Founder Search, integrity, exploration, birth, motor-screen and non-canonical sandbox evidence. Their source copies and earlier interpretations are unchanged. The watchlist cites their complete reports, not only short wrappers.

The newly registered **priority H/E/I curves** are an existing passive analysis of the same sandbox. [Report copy](../../{BATCH}/curves/H_E_I_DEVELOPMENTAL_CURVES_v0_1.md), [same-analyst consistency review](../../{BATCH}/curves/CURVE_CONSISTENCY_REVIEW.json), [original manifest](../../{BATCH}/curves/CURVE_PACKAGE_MANIFEST.json), and [input provenance](../../{BATCH}/curves/INPUT_PROVENANCE.json). It supplies the dynamic H band, changing H-use/q, heterogeneous E development, event-driven I and separate E/I expression observations requested as watchlist seeds. Its broader [analysis protocol](../../{BATCH}/curves/ANALYSIS_PROTOCOL.md) is not a completed behavioural result, an accepted watchlist metric or new execution permission. The observed curve cutoff for RS-M1-008 remains earlier than the physical durable prefix.

Byte-identical report copies preserve their original relative references. Figures, full compressed series and supporting tables remain in the complete original package: [original report with assets](<C:/Users/Jason/.codex/.chatgpt-projects/g-p-6a6fb425222c8191a814fdc0f7d89f97/m1_long_development_full_analysis_20261001_v0_1/H_E_I_DEVELOPMENTAL_CURVES_v0_1.md>) and [complete curve archive](<{Path(plan['external_archive']['path']).as_posix()}>). That archive has {plan['external_archive']['bytes']:,} bytes and SHA-256 `{plan['external_archive']['sha256']}`. It was hashed and its report/manifest bytes compared at intake; other payload members were not revalidated. No complete archive was copied into Obsidian.

Historical [sandbox passive methods](../../{BATCH}/sandbox/PASSIVE_METHODS.md) preserve fragment/bout grouping and actual clock/support boundaries. They are source-specific methods, not universal criteria. The workbench does not rewrite older evidence to match a newer observer definition.

## Source inventory

| Source ID | Artifact | SHA-256 |
|---|---|---|
'''
for r in reused+plan['new_source_rows']:
 n=r['path'];link=href(n) if re.match(r'^[A-Za-z]:',n) else '../../'+quote(n,safe='/')
 srcnote+=f"| {r['source_id']} | [{Path(n).name}]({link}) | `{r['sha256']}` |\n"
put(SESSION+'/SOURCE_REFERENCES.md',srcnote)
def rebase(m):
 h=m.group(1)
 if h.startswith('<') or re.match(r'^[A-Za-z]+:',h):return m.group(0)
 dest=(WB/'30_REVIEWS'/unquote(h)).resolve()
 return ']('+quote(os.path.relpath(dest,WB/SESSION).replace('\\','/'),safe='/#')+')'
put(SESSION+'/WATCHLIST_AS_ESTABLISHED.md',re.sub(r'\]\((<[^>]+>|[^\)\n]+)\)',rebase,watch.read_text(encoding='utf-8')))
# The exact initial live bytes are also retained separately, with their original relative-link base documented.
snapshot=ROOT/'NEW'/SESSION/'WATCHLIST_INITIAL_BYTES.md';snapshot.write_bytes(watch.read_bytes())
put(SESSION+'/INTEGRATION_REPORT.md',f'''# Behavioural development watchlist establishment — 1 October 2026

Created the standing [BEHAVIOURAL_DEVELOPMENT_WATCHLIST.md](../../{REVIEW}) as an evolving observational framework. Its ten stable family IDs each distinguish phenomenon, developmental rationale, measure, opportunity denominator, confounds, current record capability, evidence and unresolved causal testing. It has no overall score, numerical pass gates, required sequence or intelligence criterion.

## What changed

- Added the watchlist and prominent links from the live map, status, open questions and developmental evidence index.
- Added a light maintenance cadence in AGENTS.md: one bounded dated integration after a coherent major result/design decision/analysis, including watchlist review and preservation of shared-note history.
- Retained sparse Founder Search source experience; possible FS-015/FS-017 integrity signals with mixed/adverse cases; innate M1 exposure gains; separate supported sandbox experience; and unestablished useful learned navigation.
- Registered the existing priority H/E/I curve report to support the requested internal-development cross-references. Its dynamic H, changing use/q, heterogeneous E and event-driven I are bounded observations/interpretations, not physical causal results. Separate E/I motor effects remain small relative to M1.
- Preserved the eight-field status model, opportunity rule, source-specific measurement limits and dated evidence/interpretation/proposed-measurement change history. Matched pre-hazard contexts remain a promising proposed measurement, not an accepted metric.

Seven shared files changed: AGENTS.md, 00_RESEARCH_MAP.md, 01_WORKSPACE_STATUS.md, 02_OPEN_QUESTIONS.md, the developmental evidence review index, SOURCE_REGISTER.md and SOURCE_CATALOG.json. **40_DECISIONS and its index were not changed.** No candidate mechanism document needed alteration.

## Provenance and recovery

Prior integration ended at SRC-493. This session adds SRC-494–SRC-505: eleven small byte-identical source copies and one externally referenced curve archive. Existing catalog rows and events are preserved. [Source references](SOURCE_REFERENCES.md) and [exact source identities](SOURCE_IDENTITIES.json) identify reused reports, new report/metadata custody and the complete external package.

SHARED_BEFORE preserves exact prior shared-note bytes. [INTEGRATION_CHANGES.json](INTEGRATION_CHANGES.json) records before/after hashes and all new paths. [WATCHLIST_AS_ESTABLISHED.md](WATCHLIST_AS_ESTABLISHED.md) is a readable session snapshot with links rebased; `WATCHLIST_INITIAL_BYTES.md` preserves the exact initial live bytes and uses the original `30_REVIEWS/` relative-link base. Both snapshots are historical once the live watchlist evolves.

[Validation report](VALIDATION_REPORT.md) and [check details](VALIDATION.json) cover document content requirements, authored navigation, source/manifest identities, previous-file preservation, catalog append integrity and hash-guarded shared edits. Validation concerns custody and documentation, not a scientific rerun. The curve report's 807-checkpoint consistency result is a source-reported same-analyst check; it was not repeated here.

## Boundaries and unresolved work

No behavioural criterion was promoted to canon. No Loom mechanism was selected. No experiment was run. The watchlist is an evolving observational framework. Canonical repository files, P, Base World settings, complete candidates, all prior source/evidence records and decision history remain unchanged. No Git operation, simulation, scientific analysis/replay, automation, trial authority or experiment number was created. The original 4.65 GB evidence archive remains external; no large archive was duplicated.

Future matched-context definitions, some opportunity-normalised measures and all learned-state physical causal tests remain unspecified or unperformed; record availability is not a completed assay. FS-060/RS-M1-008 missing tails remain missing. The priority curve report is not completion of its broader analysis protocol. Stop after documentation integration and validation.
''')
print(json.dumps({'shared_files':len(plan['live_before']),'watchlist_words':len(watch.read_text().split()),'reused_source_identities_checked':len(reused),'source_catalog_rows':len(catalog['source_files'])}))
