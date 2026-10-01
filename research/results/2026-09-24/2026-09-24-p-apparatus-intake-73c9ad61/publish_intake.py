"""Scoped intake publication; does not import or run archived scientific code."""
from pathlib import Path
from urllib.parse import unquote
import json,hashlib,zipfile,shutil,re,sys
ROOT=Path(__file__).resolve().parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
plan=json.loads((ROOT/'PLAN.json').read_text(encoding='utf-8'))
sha=lambda b:hashlib.sha256(b).hexdigest()
def dump(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def scoped(p):
    p=p.resolve();assert p.is_relative_to(WB) and p!=WB;return p
def verify_links(files,virtual=False):
    count=0;fail=[]
    for file,base in files:
        for href in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^\)\n]+)\)',file.read_text(encoding='utf-8-sig')):
            if re.match(r'^[A-Za-z]+:',href):continue
            target=unquote(href.strip('<>')).split('#')[0]
            if not target:continue
            dest=(base.parent/target).resolve()
            exists=dest.is_file()
            if virtual and dest.is_relative_to(WB):
                rel=dest.relative_to(WB)
                exists=exists or (ROOT/'NEW'/rel).is_file() or (ROOT/'AFTER'/rel).is_file()
                if rel.as_posix().startswith(plan['batch']+'/'):exists=exists or (ROOT/'SOURCE_BATCH'/rel.name).is_file()
                if rel.as_posix()==plan['session']+'/VALIDATION.json':exists=True
            if not exists:fail.append({'file':str(base),'target':href})
            count+=1
    assert not fail,json.dumps(fail,indent=2)
    return count

for name,h in plan['live_before'].items():assert sha((WB/name).read_bytes())==h['sha256'],f'Concurrent edit {name}'
for name,h in plan['protected_before'].items():assert sha((WB/name).read_bytes())==h,f'Concurrent protected edit {name}'
assert sha(Path(plan['zip_source']).read_bytes())==plan['verification']['zip_sha256']
old=json.loads((ROOT/'BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
new=json.loads((ROOT/'AFTER/SOURCE_CATALOG.json').read_text(encoding='utf-8'))
assert new['source_files'][:61]==old['source_files'] and new['intake_events'][:-1]==old['intake_events']
md=[]
for directory in ['NEW','AFTER']:
    for file in (ROOT/directory).rglob('*.md'):md.append((file,WB/file.relative_to(ROOT/directory)))
count=verify_links(md,True)
targets=[scoped(WB/plan[k]) for k in ['session','batch','review','decision','export']]
assert all(not p.exists() for p in targets),'Unique intake destination already exists'
if '--publish' not in sys.argv:
    print(json.dumps({'ready':True,'links':count,'protected':len(plan['protected_before']),'new_sources':len(plan['source_entries'])}));sys.exit(0)
session,batch,review,decision,export=targets
shutil.copytree(ROOT/'SOURCE_BATCH',batch)
for file in (ROOT/'NEW').rglob('*'):
    if file.is_file():
        dest=scoped(WB/file.relative_to(ROOT/'NEW'));dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(file,dest)
with zipfile.ZipFile(session/'PRIOR_SHARED_NOTES.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name,identity in plan['live_before'].items():
        data=(ROOT/'BEFORE'/name).read_bytes();assert sha(data)==identity['sha256'];z.writestr(name,data)
dump(session/'PRIOR_SHARED_NOTES_RECEIPT.json',{'sha256':sha((session/'PRIOR_SHARED_NOTES.zip').read_bytes()),'files':plan['live_before']})
for name,identity in plan['live_before'].items():
    assert sha((WB/name).read_bytes())==identity['sha256'],f'Concurrent edit {name}'
    (WB/name).write_bytes((ROOT/'AFTER'/name).read_bytes())
for name,h in plan['protected_before'].items():assert sha((WB/name).read_bytes())==h,name
for e in plan['source_entries']:assert sha((WB/e['path']).read_bytes())==e['sha256']
validation=dict(plan['verification'],existing_source_rows_preserved=61,protected_files_unchanged=len(plan['protected_before']),
    link_count=count,shared_notes={n:{'before':v['sha256'],'after':sha((WB/n).read_bytes())} for n,v in plan['live_before'].items()},
    validation_scope='Archive identities and records only; not independent apparatus approval or new commissioning.',intake_complete=True)
dump(session/'VALIDATION.json',validation)
assert verify_links([(base,base) for _,base in md])==count

# Portable copies preserve the workbench-relative paths used in the three new notes.
export.mkdir(parents=True,exist_ok=False)
for rel in [plan['review'],plan['decision']]:
    dest=export/rel;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(WB/rel,dest)
shutil.copytree(batch,export/plan['batch'])
for name in ['INTAKE_RECORD.md','SOURCE_IDENTITIES.json','VALIDATION.json']:
    dest=export/plan['session']/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(session/name,dest)
(export/'READ_FIRST.md').write_text(f"# P apparatus build intake\n\n[Status and limitations]({plan['review']}) · [Recorded construction scope]({plan['decision']}) · [Completion record]({plan['session']}/INTAKE_RECORD.md).\n\nBuilder-reported construction complete; independent review pending. Commissioning is not authorized. The original ZIP and unchanged reading copies are included for custody, not execution.\n",encoding='utf-8')
portable_count=verify_links([(p,p) for p in [export/'READ_FIRST.md',export/plan['review'],export/plan['decision'],export/plan['session']/'INTAKE_RECORD.md']])
payload={p.relative_to(export).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in export.rglob('*') if p.is_file()}
dump(export/'DELIVERY_MANIFEST.json',{'files':payload,'scope':'Portable intake documentation and unchanged sources; manifest/containing ZIP excluded from own list','links_verified':portable_count})
zip_path=export/'Loom_P_Apparatus_Intake_20260924_73c9ad61.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for name in list(payload)+['DELIVERY_MANIFEST.json']:z.write(export/name,name)
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    for name,h in payload.items():assert sha(z.read(name))==h['sha256']
receipt={'export':str(export),'zip':str(zip_path),'bytes':zip_path.stat().st_size,'sha256':sha(zip_path.read_bytes()),'payload_files_verified':len(payload),'portable_links':portable_count}
dump(export/'ZIP_RECEIPT.json',receipt);dump(session/'EXPORT_RECEIPT.json',receipt)
for name,h in plan['protected_before'].items():assert sha((WB/name).read_bytes())==h
dump(ROOT/'PUBLISHED_RESULT.json',{'session':str(session),'review':str(review),'decision':str(decision),'validation':validation,'export':receipt})
print(json.dumps({'review':str(review),'session':str(session),'zip':str(zip_path),'links':count,'protected_unchanged':len(plan['protected_before']),'payloads_verified':plan['verification']['payload_entries_verified']}))
