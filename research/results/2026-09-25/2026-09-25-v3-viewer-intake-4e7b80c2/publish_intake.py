"""Publish prepared review intake only; no research imports or execution."""
from pathlib import Path
from urllib.parse import unquote
import hashlib,json,zipfile,shutil,re,sys
ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
plan=json.loads((ROOT/'PLAN.json').read_text(encoding='utf-8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def scoped(p):
    p=p.resolve();assert p.is_relative_to(WB) and p!=WB;return p
def links(virtual):
    count=0;errors=[]
    for group in ['NEW','AFTER']:
        for p in (ROOT/group).rglob('*.md'):
            base=WB/p.relative_to(ROOT/group)
            actual=p if virtual else base
            for href in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^\)\n]+)\)',actual.read_text(encoding='utf-8-sig')):
                if re.match(r'^[A-Za-z]+:',href):continue
                path=unquote(href.strip('<>')).split('#')[0]
                if not path:continue
                dest=(base.parent/path).resolve();exists=dest.is_file()
                if virtual and dest.is_relative_to(WB):
                    rel=dest.relative_to(WB)
                    exists=exists or (ROOT/'NEW'/rel).is_file() or (ROOT/'AFTER'/rel).is_file()
                    if rel.as_posix().startswith(plan['batch']+'/'):exists=exists or (ROOT/'SOURCE_BATCH'/rel.relative_to(plan['batch'])).is_file()
                    if rel.as_posix()==plan['session']+'/VALIDATION.json':exists=True
                if not exists:errors.append({'source':str(base),'target':href})
                count+=1
    assert not errors,json.dumps(errors,indent=2)
    return count

for name,meta in plan['live_before'].items():assert sha((WB/name).read_bytes())==meta['sha256'],f'Concurrent live edit: {name}'
for name,h in plan['protected_before'].items():assert sha((WB/name).read_bytes())==h,f'Concurrent protected edit: {name}'
assert sha(Path(plan['zip_source']).read_bytes())==plan['verification']['zip_sha256']
for incoming_path,incoming_hash in plan['incoming_before'].items():assert sha(Path(incoming_path).read_bytes())==incoming_hash,incoming_path
before=json.loads((ROOT/'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
after=json.loads((ROOT/'AFTER/SOURCE_CATALOG.json').read_text(encoding='utf-8'))
assert after['source_files'][:plan['old_catalog_count']]==before['source_files']
assert after['intake_events'][:-1]==before['intake_events']
assert len(after['source_files'])==plan['old_catalog_count']+len(plan['source_entries'])
for e in plan['source_entries']:
    data=(ROOT/'SOURCE_BATCH'/Path(e['path']).relative_to(plan['batch'])).read_bytes()
    assert len(data)==e['bytes'] and sha(data)==e['sha256']
for name,h in plan['batch_inventory'].items():assert sha((ROOT/'SOURCE_BATCH'/name).read_bytes())==h,name
count=links(True)
session=scoped(WB/plan['session']);batch=scoped(WB/plan['batch']);review=scoped(WB/plan['review'])
assert all(not x.exists() for x in [session,batch,review])
if '--publish' not in sys.argv:
    print(json.dumps({'ready':True,'links':count,'protected_files':len(plan['protected_before']),'sources':len(plan['source_entries'])}));sys.exit(0)
shutil.copytree(ROOT/'SOURCE_BATCH',batch)
for p in (ROOT/'NEW').rglob('*'):
    if p.is_file():
        dest=scoped(WB/p.relative_to(ROOT/'NEW'));dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
with zipfile.ZipFile(session/'PRIOR_SHARED_NOTES.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name,meta in plan['live_before'].items():
        data=(ROOT/'BEFORE'/name).read_bytes();assert sha(data)==meta['sha256'];z.writestr(name,data)
dump(session/'PRIOR_SHARED_NOTES_RECEIPT.json',{'sha256':sha((session/'PRIOR_SHARED_NOTES.zip').read_bytes()),'files':plan['live_before']})
for name,meta in plan['live_before'].items():
    assert sha((WB/name).read_bytes())==meta['sha256'],f'Concurrent live edit: {name}'
    (WB/name).write_bytes((ROOT/'AFTER'/name).read_bytes())
for name,h in plan['protected_before'].items():assert sha((WB/name).read_bytes())==h,name
for e in plan['source_entries']:
    data=(WB/e['path']).read_bytes();assert sha(data)==e['sha256'] and len(data)==e['bytes']
for name,h in plan['batch_inventory'].items():assert sha((batch/name).read_bytes())==h,name
validation=dict(plan['verification'],existing_catalog_rows_preserved=plan['old_catalog_count'],protected_files_unchanged=len(plan['protected_before']),
    links_validated=count,source_ids=[e['source_id'] for e in plan['source_entries']],
    shared_files={n:{'before':h['sha256'],'after':sha((WB/n).read_bytes())} for n,h in plan['live_before'].items()},
    intake_complete=True,validation_scope='Source custody, exact status registration, links and byte preservation; no review rerun or scientific validation')
validation['incoming_files_preserved']=len(plan['incoming_before'])
with zipfile.ZipFile(session/'PRIOR_SHARED_NOTES.zip') as recovery:
    for name,meta in plan['live_before'].items():assert sha(recovery.read(name))==meta['sha256']
validation['recovery_archive_verified']=True
validation['full_derived_batch_files_verified']=len(plan['batch_inventory'])
dump(session/'VALIDATION.json',validation)
assert links(False)==count
assert sha(Path(plan['zip_source']).read_bytes())==plan['verification']['zip_sha256']
for incoming_path,incoming_hash in plan['incoming_before'].items():assert sha(Path(incoming_path).read_bytes())==incoming_hash,incoming_path
result={'review':str(review),'session':str(session),'status':plan['status'],'links':count,'protected_unchanged':len(plan['protected_before']),'payloads_verified':plan['verification']['manifest_payloads_verified']}
dump(ROOT/'PUBLISHED_RESULT.json',result);print(json.dumps(result))
