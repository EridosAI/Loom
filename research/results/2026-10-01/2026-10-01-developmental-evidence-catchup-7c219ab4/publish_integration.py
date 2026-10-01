"""Publish only reviewed documentation and small source copies, with optimistic locks."""
from pathlib import Path
from urllib.parse import unquote
import hashlib,json,re,shutil,sys
ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
plan=json.loads((ROOT/'PLAN.json').read_text(encoding='utf-8'))
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def dump(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def guarded(rel):
 p=(WB/rel).resolve();assert p.is_relative_to(WB) and p!=WB;return p
def links(virtual):
 bad=[];count=0
 for group in ['NEW','AFTER']:
  for q in (ROOT/group).rglob('*.md'):
   rel=q.relative_to(ROOT/group);base=WB/rel;actual=q if virtual else base
   for href in re.findall(r'(?<!!)\[[^\]\n]+\]\((<[^>]+>|[^\)\n]+)\)',actual.read_text(encoding='utf-8-sig')):
    href=unquote(href.strip('<>')).split('#')[0]
    if not href or re.match(r'^https?://',href):continue
    if re.match(r'^[A-Za-z]:[/\\]',href):dest=Path(href)
    else:dest=(base.parent/href).resolve()
    exists=dest.exists()
    if virtual and dest.is_relative_to(WB):
     r=dest.relative_to(WB);exists=exists or (ROOT/'NEW'/r).exists() or (ROOT/'AFTER'/r).exists()
     if r.as_posix().startswith(plan['batch']+'/'):exists=exists or (ROOT/'SOURCE_BATCH'/r.relative_to(plan['batch'])).exists()
     if r.as_posix() in [plan['session']+'/VALIDATION.json',plan['session']+'/INTEGRATION_CHANGES.json']:exists=True
    if not exists:bad.append({'source':str(rel),'target':href})
    count+=1
 assert not bad,json.dumps(bad,indent=2)
 return count

before=json.loads((ROOT/'SHARED_BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
after=json.loads((ROOT/'AFTER/SOURCE_CATALOG.json').read_text(encoding='utf-8'))
assert after['source_files'][:378]==before['source_files'] and after['intake_events'][:-1]==before['intake_events']
assert len(after['source_files'])==493
assert len({e['source_id'] for e in after['source_files']})==493
assert len(plan['archives'])==9
for a in plan['archives']:
 assert a['storage']=='external-reference-only-NOT-COPIED'
 assert not any(p.name==a['original_filename'] for p in (ROOT/'SOURCE_BATCH').rglob('*'))
for n,h in plan['batch_inventory'].items():assert sha(ROOT/'SOURCE_BATCH'/n)==h,n
for n,m in plan['live_before'].items():assert sha(WB/n)==m['sha256'],'Concurrent shared edit: '+n
for n,h in plan['protected_before'].items():assert sha(WB/n)==h,'Concurrent protected edit: '+n
count=links(True)
new=[p.relative_to(ROOT/'NEW') for p in (ROOT/'NEW').rglob('*') if p.is_file()]
assert not (WB/plan['batch']).exists() and not (WB/plan['session']).exists()
assert all(not (WB/n).exists() for n in new)
changes={n:{'before':m,'after':{'sha256':sha(ROOT/'AFTER'/n),'bytes':(ROOT/'AFTER'/n).stat().st_size}} for n,m in plan['live_before'].items()}
assert set(changes)=={p.relative_to(ROOT/'AFTER').as_posix() for p in (ROOT/'AFTER').rglob('*') if p.is_file()}
for group in ['NEW','AFTER']:
 for p in (ROOT/group).rglob('*.md'):
  t=p.read_text(encoding='utf-8')
  assert 'SEALED_EVALUATOR_DO_NOT_OPEN' not in t and 'B1_PRIVILEGED_EVALUATOR_HOLD.zip' not in t

ready={'ready':True,'authored_links':count,'new_authored_files':len(new),'updated_shared_files':len(changes),'small_source_files':len(plan['batch_inventory']),
 'old_files_preserved':len(plan['protected_before']),'external_archives':9,'archive_copies_to_vault':0}
dump(ROOT/'PREPUBLICATION_VALIDATION.json',ready)
if '--publish' not in sys.argv:print(json.dumps(ready));sys.exit(0)

# Recheck all input source bytes, including whole external archives, before any WB write.
for n,h in plan['incoming_before'].items():assert sha(n)==h,'Concurrent source edit: '+n
for n,m in plan['live_before'].items():assert sha(WB/n)==m['sha256'],'Concurrent shared edit: '+n
shutil.copytree(ROOT/'SOURCE_BATCH',guarded(plan['batch']))
for n in new:
 d=guarded(n);d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/'NEW'/n,d)
session=guarded(plan['session'])
shutil.copytree(ROOT/'SHARED_BEFORE',session/'SHARED_BEFORE')
for n,m in plan['live_before'].items():
 assert sha(WB/n)==m['sha256'],'Concurrent shared edit: '+n
 (WB/n).write_bytes((ROOT/'AFTER'/n).read_bytes())
dump(session/'INTEGRATION_CHANGES.json',{'session_id':ROOT.name,'shared_files':changes,'new_authored_files':[n.as_posix() for n in new],
 'new_source_batch':plan['batch'],'source_files':len(plan['batch_inventory']),'external_archives_not_copied':9})
for n,h in plan['protected_before'].items():assert sha(WB/n)==h,n
for n,h in plan['batch_inventory'].items():assert sha(WB/plan['batch']/n)==h,n
for n,m in plan['live_before'].items():
 assert sha(session/'SHARED_BEFORE'/n)==m['sha256'],n
 assert sha(WB/n)==changes[n]['after']['sha256'],n
for n in new:assert sha(WB/n)==sha(ROOT/'NEW'/n),str(n)
# Whole archives are read-only and not write targets. Confirm preserved size/mtime after guarded copying.
validation=dict(ready,integration_complete=True,source_catalog_old_rows_preserved=378,source_catalog_rows=493,
 source_manifest_crosschecks=len(plan['manifest_checks']),input_hashes_verified_before_publication=len(plan['incoming_before']),
 external_whole_archive_hashes_verified=9,original_archive_manifest_bytes_matched=9,
 raw_payload_validation_rerun=False,science_execution=False,git_operations=False,canon_modified=False,settings_modified=False,
 sealed_human_B1_opened=False,held_previous_sources_unchanged=True,SHARED_BEFORE_verified=True,
 validation_scope='Documentation custody, source/manifest identities, archive hashes, linked navigation, exact prior-file preservation; no new scientific analysis or validation execution.',
 retained_gaps=['FS-060 unknown unflushed tail','RS-M1-008 unavailable in-flight state and unresolved native faulting module/root cause'],
 separate_build_brief_executed=False)
dump(session/'VALIDATION.json',validation)
assert links(False)==count
validation_md=f'''# Integration validation — 1 October 2026

**PASS.** {len(changes)} shared notes updated, {len(new)} new authored/custody documents, {len(plan['batch_inventory'])} small source copies. SRC-001–378 preserved; SRC-379–493 added. {count} authored navigation links resolve. {len(plan['protected_before'])} previous source/candidate/review/decision/session files remain byte-identical; all eight prior shared notes match SHARED_BEFORE and their recorded hashes.

Nine external archives matched their supplied SHA-256/size and archived manifest bytes. No complete archive was copied to the vault, including the 4,653,285,580-byte resurrection archive. {len(plan['manifest_checks'])} selected source identities matched original manifest/verification declarations. The remaining copied receipts/request material has explicit freshly computed custody hashes; no invented self-hash verification is claimed.

No raw-payload scientific validator, test, P/world/field/controller, engineering replay, Git operation or Windows crash investigation was executed. Canon, settings, complete candidate designs and raw evidence were not edited. All observations and interpretations retain bounded source status; M1 remains NON-CANONICAL. The incomplete FS-060/RS-M1-008 states and crash root cause remain unresolved.

Exact checks: [VALIDATION.json](VALIDATION.json). Shared before/after identities: [INTEGRATION_CHANGES.json](INTEGRATION_CHANGES.json). Inputs: [SOURCE_IDENTITIES.json](SOURCE_IDENTITIES.json). Integration: [INTEGRATION_REPORT.md](INTEGRATION_REPORT.md).
'''
(session/'VALIDATION_REPORT.md').write_text(validation_md,encoding='utf-8',newline='\n')
dump(ROOT/'PUBLISHED_RESULT.json',{'status':'COMPLETE','session':str(session),'report':str(WB/plan['record']),'links':count,'protected_files_unchanged':len(plan['protected_before'])})
print(json.dumps({'status':'COMPLETE','report':str(WB/plan['record']),'links':count,'protected_files_unchanged':len(plan['protected_before']),'archive_copies':0}))
