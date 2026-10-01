from pathlib import Path
import hashlib,json,shutil,zipfile
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent.parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
ID=ROOT.name
S='50_SESSIONS/'+ID
B='90_SOURCES/developmental_catchup_2026-10-01_7c219ab4'
R=S+'/INTEGRATION_REPORT.md'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def write(p,t):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8',newline='\n')
def dump(p,x):write(p,json.dumps(x,indent=2,ensure_ascii=False)+'\n')
groups={
 'b1':('exports/2026-09-29-B1-S1-paired-closure-a8cdd75','B1_MINIMAL_CLOSURE_REPORT.md PAIRED_CLOSURE_RESULTS.json FULL_COMPANION.json DELIVERY_VERIFICATION.json FILE_MANIFEST.json'),
 'b1_full':('exports/2026-09-29-B1-minimal-closure-results-a8cdd75','DELIVERY_VERIFICATION.json'),
 'runner':('exports/2026-09-29-developmental-runner-optimization','DEVELOPMENTAL_RUNNER_OPTIMIZATION_REPORT.md CHECKPOINT.json EQUIVALENCE_AND_CONTINUATION.md SCIENTIFIC_EVIDENCE_INVENTORY.md DELIVERY_VERIFICATION.json PACKAGE_MANIFEST.json'),
 'founder_design':('exports/2026-09-29-Founder-Search-v0-1-design','FOUNDER_SEARCH_v0_1_DESIGN.md JASON_TIMING_RULING.md'),
 'direction':('research_direction_20260929','JASON_DEVELOPMENTAL_SELECTION_CLARIFICATION.md DISPOSITION.json'),
 'founder12':('founder_initial_execution_20260930','FOUNDER_SEARCH_INITIAL_STAGE_REPORT.md JASON_AUTHORIZATION.md ARCHIVE_VERIFICATION.json DELIVERY_VERIFICATION.json EVIDENCE_ARCHIVE_MANIFEST.json DENOMINATOR_SEALED.json REPORT_METHOD.md'),
 'founder60':('founder_expansion_execution_20260930','FOUNDER_SEARCH_60_LIFE_FINAL_REPORT.md FOUNDER_SEARCH_60_LIFE_REPORT.md JASON_AUTHORIZATION.md FINAL_DELIVERY_VERIFICATION.json ARCHIVE_VERIFICATION.json EVIDENCE_ARCHIVE_MANIFEST.json COMBINED_DENOMINATOR_SEALED.json INTERRUPTION_NOTE.md analysis/FS034_INTERPRETATION.md analysis/STREAM_B_COMPLETION.json'),
 'integrity':('impact_integrity_analysis_20260930_v0_1','IMPACT_INTEGRITY_DEVELOPMENT_ANALYSIS_v0_1.md METHODS.md FINAL_VERIFICATION.json DESCRIPTIVE_CLASSIFICATIONS.csv PASSIVE_LEARNED_I_OMISSIONS.csv CONTACT_SEVERITY.png CLEARANCE_AND_LOCAL_I.png RECORDED_CANDIDATE_PATHS.png'),
 'exploration':('nursery_0_design_20260930_v0_1','NEWBORN_EXPLORATION_DYNAMICS_AUDIT_v0_1.md EXPLORATION_AUDIT_METHODS.md EXPLORATION_PER_LIFE.csv DESIGN_ONLY_VERIFICATION.json SOURCE_MANIFEST.json NURSERY_0_DESIGN_v0_1.md NURSERY_CANDIDATE_PROPOSALS.json EXPLORATION_DYNAMICS.png NURSERY_0_LAYOUT_REVIEW.png'),
 'birth_motor_design':('nursery_birth_motor_review_20260930_v0_1','BIRTH_GEOGRAPHY_AUDIT_v0_1.md NEWBORN_SPONTANEOUS_MOTOR_DESIGN_REVIEW_v0_1.md BIRTH_AUDIT_METHODS.md REVIEW_VERIFICATION.json BIRTH_GEOGRAPHY_ALL_60.csv JASON_MOTOR_DESIGN_REQUEST.txt JASON_BIRTH_GEOGRAPHY_REQUEST.md'),
 'motor_v01':('motor_commissioning_results_20260930_v0_1','MOTOR_COMMISSIONING_RESULT_v0_1.md ARCHIVE_VERIFICATION.json DENOMINATOR_RECONCILIATION.json'),
 'contact_correction':('contact_release_correction_20260930','APPARATUS_ROOT_CAUSE_AND_CORRECTION.md CORRECTED_SOURCE_IDENTITY.json FINAL_VERIFICATION.json PACKAGE_MANIFEST.json ARCHIVE_VERIFICATION.json'),
 'motor_v02':('motor_commissioning_results_20260930_v0_2','MOTOR_COMMISSIONING_RESULT_v0_2.md ALL_NINE_DISPOSITIONS.csv AVAILABLE_CASE_METRICS.csv FINAL_VERIFICATION.json ARCHIVE_VERIFICATION.json PACKAGE_MANIFEST.json PASSIVE_VALIDATION.json NINE_CASE_PATHS.png REACH_AND_COVERAGE.png M2_RENEWAL_TIMING.png'),
 'motor_preparation':('motor_commissioning_preparation_20260930_v0_2','RUNTIME_IDENTITY.json FINAL_VERIFICATION.json PACKAGE_MANIFEST.json'),
 'sandbox':('m1_resurrection_results_20260930_v0_1','SANDBOX_REPORT.md FINDINGS.md DEVELOPMENTAL_QUESTIONS.md HOST_FAILURE_REPORT.md HOST_APPLICATION_ERROR.xml HOST_FAILURE_OBSERVATION.json HOST_STOP.json HOST_STOP_DENOMINATOR.json ALL_TWELVE_DISPOSITIONS.csv ARCHIVE_VERIFICATION.json FINAL_VERIFICATION.json PACKAGE_MANIFEST.json PASSIVE_ANALYSIS_QA.json PASSIVE_VERIFICATION.json TEMPORAL_STATE_DELTAS.json ALL_TWELVE_PATHS.png'),
 'sandbox_preparation':('m1_resurrection_sandbox_20260930_v0_1','JASON_OVERNIGHT_AUTHORIZATION.txt LAUNCH_RECORD.md BATCH_AUTHORITY.json RUNTIME_IDENTITY.json PREPARATION_MANIFEST.json')
}
live=['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','02_OPEN_QUESTIONS.md','20_CANDIDATES/CAND-P.md','40_DECISIONS/DECISION_INDEX.md','SOURCE_REGISTER.md','SOURCE_CATALOG.json']
before={}
for n in live:
 p=WB/n;data=p.read_bytes();before[n]={'sha256':sha(p),'bytes':len(data)}
 q=ROOT/'SHARED_BEFORE'/n;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
protected={}
for folder in ['90_SOURCES','20_CANDIDATES','30_REVIEWS','40_DECISIONS','50_SESSIONS']:
 for p in (WB/folder).rglob('*'):
  rel=p.relative_to(WB).as_posix()
  if p.is_file() and rel not in live:protected[rel]=sha(p)
catalog=json.loads((WB/'SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
assert len(catalog['source_files'])==378
assert catalog['intake_events'][-1]['session_id']=='2026-09-26-b1-final-review-intake-f04e8c72'
batch=ROOT/'SOURCE_BATCH';batch.mkdir(exist_ok=True)
entries=[];incoming={};manifest_checks=[]
def entry(p,rel,group,extra=None):
 p=Path(p).resolve();dest=batch/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
 h=sha(p);assert sha(dest)==h;incoming[str(p)]=h
 e={'source_id':f'SRC-{379+len(entries):03d}','path':B+'/'+rel,'original_filename':p.name,'original_path':str(p),'bytes':p.stat().st_size,'sha256':h,
 'registered':'2026-10-01','role':group,'storage':'byte-identical-small-file-copy','authority':'Workbench integration only; source decisions/results retain original scopes',
 'record':R,'stated_author':'As stated in original source; no model/backend inference'}
 if extra:e.update(extra)
 entries.append(e)
for group,(folder,listing) in groups.items():
 p=BASE/folder
 for n in listing.split():entry(p/n,group+'/'+n,group)
 # Corroborate selected report/metadata identities against this package's original manifest.
 ms=[]
 for n in ['PACKAGE_MANIFEST.json','FILE_MANIFEST.json','FINAL_VERIFICATION.json','REVIEW_VERIFICATION.json','DESIGN_ONLY_VERIFICATION.json','FINAL_DELIVERY_VERIFICATION.json','DELIVERY_VERIFICATION.json','EVIDENCE_ARCHIVE_MANIFEST.json']:
  if not (p/n).is_file():continue
  d=json.loads((p/n).read_text(encoding='utf-8-sig'))
  for key in ['files','analysis_files']:
   values=d.get(key,[])
   if isinstance(values,dict):values=[dict(v,path=k) for k,v in values.items() if isinstance(v,dict)]
   if isinstance(values,list):ms += [(n,x) for x in values if isinstance(x,dict) and 'path' in x and 'sha256' in x]
  for key,report in [('final_report_sha256','FOUNDER_SEARCH_60_LIFE_FINAL_REPORT.md'),('report_sha256','IMPACT_INTEGRITY_DEVELOPMENT_ANALYSIS_v0_1.md')]:
   if key in d and (p/report).is_file():assert sha(p/report)==d[key];manifest_checks.append({'source':str(p/report),'manifest':str(p/n),'verified':True})
 for n in listing.split():
  matches=[(mn,x) for mn,x in ms if Path(x['path']).name==Path(n).name]
  correct=[(mn,x) for mn,x in matches if x['sha256']==sha(p/n)]
  if correct:manifest_checks.append({'source':str(p/n),'manifest':str(p/correct[0][0]),'member':correct[0][1]['path'],'verified':True})

request=Path(r'C:\Users\Jason\.codex\attachments\3cfe4cbe-d12c-4100-9d1d-5ff48bcbb4eb\Pasted text.txt')
entry(request,'authority/Pasted text.txt','current-Jason-integration-request',{'source_date':'2026-10-01'})
entry(BASE/'sources/00_LOOM_CURRENT_STATE(2).md','orientation/00_LOOM_CURRENT_STATE(2).md','historical-orientation-not-latest-evidence')
entry(BASE/'worktrees/loom-contact-release-20260930/00_LOOM_CURRENT_STATE.md','orientation/contact_worktree_00_LOOM_CURRENT_STATE.md','repository-orientation-read-only-not-new-head-audit')

archive_receipts=[('b1','exports/2026-09-29-B1-S1-paired-closure-a8cdd75/DELIVERY_VERIFICATION.json'),('b1_full','exports/2026-09-29-B1-minimal-closure-results-a8cdd75/DELIVERY_VERIFICATION.json'),('runner','exports/2026-09-29-developmental-runner-optimization/DELIVERY_VERIFICATION.json'),('founder12','founder_initial_execution_20260930/ARCHIVE_VERIFICATION.json'),('founder60','founder_expansion_execution_20260930/ARCHIVE_VERIFICATION.json'),('motor_v01','motor_commissioning_results_20260930_v0_1/ARCHIVE_VERIFICATION.json'),('contact_correction','contact_release_correction_20260930/ARCHIVE_VERIFICATION.json'),('motor_v02','motor_commissioning_results_20260930_v0_2/ARCHIVE_VERIFICATION.json'),('sandbox','m1_resurrection_results_20260930_v0_1/ARCHIVE_VERIFICATION.json')]
archives=[]
for group,r in archive_receipts:
 d=json.loads((BASE/r).read_text(encoding='utf-8-sig'))
 p=Path(d.get('archive',d.get('path'))).resolve();h=d.get('archive_sha256',d.get('sha256'));size=d.get('archive_bytes',d.get('bytes'))
 assert p.stat().st_size==size and sha(p)==h,str(p)
 incoming[str(p)]=h
 manifest_name={'b1':'FILE_MANIFEST.json','b1_full':'FILE_MANIFEST.json','runner':'PACKAGE_MANIFEST.json','founder12':'EVIDENCE_ARCHIVE_MANIFEST.json','founder60':'EVIDENCE_ARCHIVE_MANIFEST.json','motor_v01':'PACKAGE_MANIFEST.json','contact_correction':'PACKAGE_MANIFEST.json','motor_v02':'PACKAGE_MANIFEST.json','sandbox':'PACKAGE_MANIFEST.json'}[group]
 source_manifest=BASE/groups[group][0]/manifest_name
 mh=sha(source_manifest)
 if 'manifest_sha256' in d:assert d['manifest_sha256']==mh
 if not (batch/group/manifest_name).exists():entry(source_manifest,group+'/'+manifest_name,group)
 a={'source_id':f'SRC-{379+len(entries):03d}','path':str(p),'original_filename':p.name,'bytes':size,'sha256':h,'registered':'2026-10-01',
 'role':group+'-complete-evidence-archive','storage':'external-reference-only-NOT-COPIED','original_receipt':str((BASE/r).resolve()),
 'manifest_path':B+'/'+group+'/'+manifest_name,'manifest_original_path':str(source_manifest.resolve()),'manifest_sha256':mh,
 'archive_sha256_recomputed_by_intake':True,'payload_reverification_by_intake':False,'record':R}
 entries.append(a);archives.append(a)
 print('Verified external archive:',group,size,flush=True)
 # Byte-only retrieval of the exact sealed manifest, not a simulation or analysis rerun.
 with zipfile.ZipFile(p) as z:
  candidates=[n for n in z.namelist() if n.endswith('/'+manifest_name) or n==manifest_name]
  matching=[n for n in candidates if hashlib.sha256(z.read(n)).hexdigest()==mh]
  assert matching,('manifest not in archive',group)
  a['manifest_archive_member']=matching[0]
  if group=='b1':
   n='execution/USER_AUTHORIZATION.md';q=ROOT/'TEMP_B1_AUTHORITY.md';q.write_bytes(z.read(n));entry(q,'b1/USER_AUTHORIZATION.md','b1-accepted-single-case-authority',{'original_path':str(p)+'::'+n})
  if group=='motor_v02':
   n='execution/JASON_AUTHORIZATION.json';q=ROOT/'TEMP_MOTOR_AUTHORITY.json';q.write_bytes(z.read(n));entry(q,'motor_v02/JASON_AUTHORIZATION.json','motor-screen-accepted-authority',{'original_path':str(p)+'::'+n})

# Validate the exact terminal/custody claims from their source metadata.
f=json.loads((BASE/'founder_expansion_execution_20260930/FINAL_DELIVERY_VERIFICATION.json').read_text())
assert f['total_roster']==60 and f['complete_biological_endpoints']==59 and f['complete_exact_P_checks']==59
m=json.loads((BASE/'motor_commissioning_results_20260930_v0_2/FINAL_VERIFICATION.json').read_text())
assert m['checkpoint']=='1d7cd6fd450ea528562b2c825589ab4de18a5b38' and m['runtime_sha256']=='5df0ced8bf5602c84852bc2074fca8d422cc39cc55b9bab00a4b653bbe714c49'
assert m['completed_90s']==9 and m['mechanism_selected'] is False
r=json.loads((BASE/'m1_resurrection_results_20260930_v0_1/FINAL_VERIFICATION.json').read_text())
assert r['runtime']=='752b7c335347a5f55fd3e7cdf1b904137d41e5b229b8ea2252caa8e12a455f3c' and r['no_retry_or_replacement']
catalog['source_files']+=entries
catalog['intake_events'].append({'session_id':ID,'registered':'2026-10-01','record':R,'source_ids':[e['source_id'] for e in entries],
 'scope':'Gap-aware continuation after B1 apparatus closure through Founder Search, passive audits, corrected motor screen and non-canonical resurrection sandbox; no scientific execution or canon change'})
dump(ROOT/'AFTER/SOURCE_CATALOG.json',catalog)
inventory={p.relative_to(batch).as_posix():sha(p) for p in batch.rglob('*') if p.is_file()}
plan={'session':S,'batch':B,'record':R,'live_before':before,'protected_before':protected,'incoming_before':incoming,'source_entries':entries,
 'archives':archives,'manifest_checks':manifest_checks,'old_catalog_count':378,'batch_inventory':inventory,'groups':groups}
dump(ROOT/'PLAN.json',plan)
dump(ROOT/'NEW'/S/'SOURCE_IDENTITIES.json',{'sources':entries,'external_archives':archives,'original_manifest_crosschecks':manifest_checks,'batch_sha256':inventory,
 'scope':'Small source copies plus external full-archive path/hash/manifest custody. No raw-evidence duplication or scientific reanalysis.'})
print(json.dumps({'sources':len(entries),'small_files':len(inventory),'small_bytes':sum(p.stat().st_size for p in batch.rglob('*') if p.is_file()),'external_archives':len(archives),'source_manifest_crosschecks':len(manifest_checks),'protected':len(protected)}))
