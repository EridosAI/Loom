from pathlib import Path
from urllib.parse import unquote
import hashlib,json,re,shutil,sys

ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
plan=json.loads((ROOT/'PLAN.json').read_text(encoding='utf-8'))
SESSION=plan['session'];BATCH=plan['batch'];REVIEW=plan['review']
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def dump(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def dest(n):
 p=(WB/n).resolve();assert p.is_relative_to(WB) and p!=WB;return p

new={p.relative_to(ROOT/'NEW').as_posix():sha(p) for p in (ROOT/'NEW').rglob('*') if p.is_file()}
after={p.relative_to(ROOT/'AFTER').as_posix():sha(p) for p in (ROOT/'AFTER').rglob('*') if p.is_file()}
assert set(after)==set(plan['live_before'])
assert all(n.startswith((BATCH+'/',SESSION+'/')) or n==REVIEW for n in new)
assert all(not dest(n).exists() for n in new)
assert not dest(SESSION).exists() and not dest(BATCH).exists()
before_catalog=json.loads((ROOT/'SHARED_BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
after_catalog=json.loads((ROOT/'AFTER/SOURCE_CATALOG.json').read_text(encoding='utf-8'))
assert after_catalog['source_files'][:493]==before_catalog['source_files']
assert after_catalog['intake_events'][:-1]==before_catalog['intake_events']
assert {k:v for k,v in after_catalog.items() if k not in ('source_files','intake_events')}=={k:v for k,v in before_catalog.items() if k not in ('source_files','intake_events')}
assert len(after_catalog['source_files'])==505 and len({r['source_id'] for r in after_catalog['source_files']})==505
for n,b in plan['live_before'].items():
 assert sha(WB/n)==b['sha256'],'Concurrent shared edit: '+n
 assert sha(ROOT/'SHARED_BEFORE'/n)==b['sha256'],n
for n,h in plan['protected_before'].items():assert sha(WB/n)==h,'Concurrent protected edit: '+n
for n,h in plan['original_inputs'].items():assert sha(n)==h,'Concurrent input edit: '+n
for r in plan['new_source_rows']:
 if r['storage']=='byte-identical-small-file-copy':assert sha(ROOT/'NEW'/r['path'])==r['sha256']

# Shared prose is additive: no old body text is removed or rewritten.
for n in after:
 if n=='SOURCE_CATALOG.json':continue
 old=(ROOT/'SHARED_BEFORE'/n).read_bytes();changed=(ROOT/'AFTER'/n).read_bytes()
 if n=='SOURCE_REGISTER.md':assert changed.startswith(old)
 else:
  sep=b'\r\n\r\n' if b'\r\n' in old else b'\n\n';head,tail=old.split(sep,1)
  assert changed.startswith(head+sep) and changed.endswith(tail),n

watch=(ROOT/'NEW'/REVIEW).read_text(encoding='utf-8')
parts=re.split(r'^## BD-\d{2} — ',watch,flags=re.M)[1:]
assert len(parts)==10
for i,s in enumerate(parts,1):
 for num,label in enumerate(['Phenomenon to watch.','Why it could indicate development.','Observable measure.','Opportunity denominator.','Major confounds.','Can current records measure it?','Current evidence.','What would require causal testing.'],1):
  assert f'**{num}. {label}**' in s,(i,label)
for phrase in ['A behavioural improvement is not interpretable','NO OPPORTUNITY','NOT YET EXAMINED','CAUSAL EFFECT UNRESOLVED','no overall score','FS-015','FS-017','FS-044','H-use','E-bank','I-bank','Cortical structural change','Temporal ordering','No behavioural criterion was promoted to canon','No Loom mechanism was selected','No experiment was run']:
 assert phrase in watch,phrase
assert not re.search(r'\\[\[\]\(\)]',watch)
assert sha(ROOT/'NEW'/SESSION/'WATCHLIST_INITIAL_BYTES.md')==sha(ROOT/'NEW'/REVIEW)
for n in ['00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','02_OPEN_QUESTIONS.md']:
 assert REVIEW in (ROOT/'AFTER'/n).read_text(encoding='utf-8')

generated={SESSION+'/INTEGRATION_CHANGES.json',SESSION+'/VALIDATION.json',SESSION+'/VALIDATION_REPORT.md'}
def links(virtual):
 errors=[];count=0
 for n in list(new)+list(after):
  if not n.endswith('.md') or n.startswith(BATCH+'/') or n.endswith('/WATCHLIST_INITIAL_BYTES.md'):continue
  p=(ROOT/('NEW' if n in new else 'AFTER')/n) if virtual else WB/n
  for href in re.findall(r'(?<!!)\[[^\]\n]+\]\((<[^>]+>|[^\)\n]+)\)',p.read_text(encoding='utf-8-sig')):
   h=unquote(href.strip('<>')).split('#')[0]
   if not h or re.match(r'^https?://',h):continue
   target=Path(h) if re.match(r'^[A-Za-z]:[/\\]',h) else (WB/n).parent/h
   target=target.resolve();exists=target.exists()
   if virtual and target.is_relative_to(WB):
    rel=target.relative_to(WB).as_posix();exists=exists or rel in new or rel in generated
   if not exists:errors.append({'source':n,'target':h})
   count+=1
 assert not errors,json.dumps(errors,indent=2)
 return count
count=links(True)
ready={'ready':True,'watchlist_families':10,'required_fields_per_family':8,'shared_files':len(after),'new_files_before_validation':len(new),'small_source_copies':plan['source_copy_count'],'new_source_rows':12,'catalog_rows':505,'preserved_prior_catalog_rows':493,'protected_files':len(plan['protected_before']),'authored_links':count,'existing_cited_source_hashes_verified':len(json.loads((ROOT/'NEW'/SESSION/'SOURCE_IDENTITIES.json').read_text())['reused_sources']),'new_source_manifest_matches':plan['manifest_matches'],'archive_copies':0}
dump(ROOT/'PREPUBLICATION_VALIDATION.json',ready)
if '--publish' not in sys.argv:print(json.dumps(ready));sys.exit(0)

# No destination is scientific code or evidence. Recheck exact source and shared identities before writes.
ar=plan['external_archive'];assert Path(ar['path']).stat().st_size==ar['bytes'] and sha(ar['path'])==ar['sha256']
for n,h in plan['original_inputs'].items():assert sha(n)==h,n
for n,b in plan['live_before'].items():assert sha(WB/n)==b['sha256'],'Concurrent shared edit: '+n
for n in new:
 p=dest(n);p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'NEW'/n,p)
session=dest(SESSION)
shutil.copytree(ROOT/'SHARED_BEFORE',session/'SHARED_BEFORE')
for n,h in after.items():
 assert sha(WB/n)==plan['live_before'][n]['sha256'],'Concurrent shared edit: '+n
 dest(n).write_bytes((ROOT/'AFTER'/n).read_bytes())
changes={'session_id':ROOT.name,'shared_files':{n:{'before':plan['live_before'][n],'after':{'sha256':after[n],'bytes':(WB/n).stat().st_size}} for n in after},'new_files':{n:{'sha256':h,'bytes':(WB/n).stat().st_size} for n,h in new.items()},'validation_artifacts':[Path(n).name for n in sorted(generated)],'protected_prior_files':plan['protected_before'],'original_source_inputs':plan['original_inputs'],'decision_index_changed':False,'initial_watchlist_sha256':new[REVIEW]}
dump(session/'INTEGRATION_CHANGES.json',changes)
for n,h in new.items():assert sha(WB/n)==h,n
for n,h in after.items():assert sha(WB/n)==h,n
for n,h in plan['protected_before'].items():assert sha(WB/n)==h,n
for n,b in plan['live_before'].items():assert sha(session/'SHARED_BEFORE'/n)==b['sha256'],n
for n,h in plan['original_inputs'].items():assert sha(n)==h,n
validation=dict(ready,integration_complete=True,decision_records_unchanged=True,candidate_documents_unchanged=True,existing_sources_unchanged=True,old_shared_body_text_preserved=True,shared_before_bytes_verified=True,new_scientific_analysis=False,simulation=False,experiment_execution=False,mechanism_selected=False,canon_changed=False,git_operations=False,automation_created=False,raw_scientific_payloads_revalidated=False,curve_archive_sha256_verified=True,curve_report_manifest_archive_bytes_verified=True,scope='Documentation structure, source custody, file-link existence, additive edits and preservation; source-reported scientific checks not rerun')
dump(session/'VALIDATION.json',validation)
report=f'''# Watchlist integration validation — 1 October 2026

**PASS.** Ten watchlist families each have all eight required fields. Opportunity denominators, confounds, modest evidence labels, causal limits, internal-development cross-references and dated maintenance history are present. No overall score, numerical success gate, mechanism selection or canon promotion was introduced.

- {len(after)} shared files updated additively; their exact earlier bytes are preserved in SHARED_BEFORE with before/after SHA-256 records.
- {len(plan['protected_before'])} prior source/candidate/review/decision/session files remain byte-identical. The decision index is unchanged.
- {count} authored file links resolve, including all changed shared notes and the readable establishment snapshot. Exact source copies retain their original relative asset references; the complete original package is linked separately. WATCHLIST_INITIAL_BYTES.md deliberately retains the original live document's relative-link base.
- Source catalog rows SRC-001–493 and earlier events are preserved. SRC-494–505 add eleven source copies and one external curve-archive reference. Ten reused source identities match the catalog; seven new files match their original curve manifest.
- The complete curve archive's SHA-256/size and archived report/manifest bytes match. Its other payloads and the original 4.65 GB sandbox archive were not revalidated by this task. No complete archive was copied into the vault.

No scientific calculation pipeline, simulator, experiment, replay, Git operation, automation or canonical repository edit was performed. The watchlist is an evolving observational framework; useful learned navigation remains unestablished and M1 non-canonical. Source-reported consistency results are attributed to their authors, not claimed as newly executed validation.

[Check details](VALIDATION.json) · [Before/after hashes](INTEGRATION_CHANGES.json) · [Source identities](SOURCE_IDENTITIES.json) · [Integration report](INTEGRATION_REPORT.md).
'''
(session/'VALIDATION_REPORT.md').write_text(report,encoding='utf-8',newline='\n')
assert links(False)==count
result={'status':'COMPLETE','watchlist':str(WB/REVIEW),'report':str(session/'INTEGRATION_REPORT.md'),'validation':str(session/'VALIDATION_REPORT.md'),'authored_links':count,'protected_files_unchanged':len(plan['protected_before'])}
dump(ROOT/'PUBLISHED_RESULT.json',result);print(json.dumps(result))
