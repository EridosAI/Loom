"""Scoped documentation publication and byte/link validation. No research execution."""
from pathlib import Path
from urllib.parse import unquote
import json,hashlib,re,shutil,zipfile,sys

ROOT=Path(__file__).resolve().parent
P=ROOT/'PACKAGE'
plan=json.loads((ROOT/'PUBLISH_PLAN.json').read_text(encoding='utf-8'))
WB=Path(plan['workbench']).resolve()
sha=lambda b:hashlib.sha256(b).hexdigest()
def putjson(path,obj): path.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def within(path):
    p=path.resolve()
    assert p.is_relative_to(WB) and p!=WB, str(p)
    return p
def links(paths,mapper=None,planned=()):
    found=[]; errors=[]
    for p in paths:
        txt=p.read_text(encoding='utf-8-sig')
        for href in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^\)\n]+)\)',txt):
            if re.match(r'^[a-zA-Z]+:',href): continue
            target,_,anchor=unquote(href.strip('<>')).partition('#')
            dest=(p.parent/target).resolve() if target else p.resolve()
            if mapper: dest=mapper(dest)
            if not dest.is_file() and str(dest) not in planned:
                errors.append({'from':str(p),'href':href,'missing':str(dest)})
            if dest.is_file() and anchor and dest.suffix=='.md':
                headings=re.findall(r'^#{1,6}\s+(.+)$',dest.read_text(encoding='utf-8-sig'),re.M)
                slugs=[re.sub(r'[^\w\- ]','',h.lower()).replace(' ','-') for h in headings]
                if anchor not in slugs: errors.append({'from':str(p),'href':href,'missing_anchor':anchor})
            found.append({'from':p.name,'href':href})
    assert not errors, json.dumps(errors,indent=2)
    return len(found)

authored=sorted(P.glob('*.md'))
assert len(authored)==7, [p.name for p in authored]
planned=[str((P/'VALIDATION.json').resolve()),str((P/'DELIVERY_MANIFEST.json').resolve())]
link_count=links(authored,planned=planned)
for p in authored:
    txt=p.read_text(encoding='utf-8')
    assert '\\[' not in txt and '\\(' not in txt, p.name
    assert '6bc9683b' in txt or p.name in ['COMPLETION_REPORT.md','SOURCE_GUIDE.md'],p.name
old=json.loads((ROOT/'LIVE_BEFORE/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
new=json.loads((ROOT/'LIVE_AFTER/SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
assert new['source_files'][:-1]==old['source_files'] and len(new['source_files'])==61
assert new['intake_events'][:-1]==old['intake_events']
for name,expected in plan['live_before'].items():
    assert sha((WB/name).read_bytes())==expected['sha256'], f'Concurrent live edit: {name}'
for name,digest in plan['protected_before'].items():
    assert sha((WB/name).read_bytes())==digest, f'Concurrent protected edit: {name}'
session=within(WB/plan['session']); export=within(WB/plan['export']); batch=within(WB/plan['batch'])
for target in [session,export,batch]: assert not target.exists(),f'Unique destination already exists: {target}'

if '--publish' not in sys.argv:
    print(json.dumps({'ready':True,'authored_links':link_count,'authored_documents':len(authored),
        'protected_files':len(plan['protected_before']),'shared_files':list(plan['live_before']),
        'destinations':[str(session),str(export),str(batch)]}))
    sys.exit(0)

session.mkdir(parents=True,exist_ok=False)
batch.mkdir(parents=True,exist_ok=False)
export.mkdir(parents=True,exist_ok=False)
for f in P.iterdir():
    if f.is_dir(): shutil.copytree(f,session/f.name)
    else: shutil.copyfile(f,session/f.name)
request=Path(plan['request_entry']['acquired_from'])
assert sha(request.read_bytes())==plan['request_entry']['sha256']
shutil.copyfile(request,batch/'Pasted text.txt')
with zipfile.ZipFile(session/'PRIOR_LIVE_NOTES.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name,identity in plan['live_before'].items():
        b=(ROOT/'LIVE_BEFORE'/name).read_bytes()
        assert sha(b)==identity['sha256']
        z.writestr(name,b)
putjson(session/'PRIOR_LIVE_NOTES_RECEIPT.json',{'zip':'PRIOR_LIVE_NOTES.zip',
    'sha256':sha((session/'PRIOR_LIVE_NOTES.zip').read_bytes()),'files':plan['live_before'],
    'note':'Original bytes of five authored/index notes before this contribution; local same-disk recovery only.'})
for name,expected in plan['live_before'].items():
    # Recheck immediately before this individual replacement.
    assert sha((WB/name).read_bytes())==expected['sha256'],f'Concurrent live edit: {name}'
    (WB/name).write_bytes((ROOT/'LIVE_AFTER'/name).read_bytes())

for name,digest in plan['protected_before'].items():
    assert sha((WB/name).read_bytes())==digest,f'Protected bytes changed: {name}'
for name in plan['live_before']:
    assert (WB/name).read_bytes()==(ROOT/'LIVE_AFTER'/name).read_bytes()
session_links=links(sorted(session.glob('*.md')),planned=[str(session/'VALIDATION.json'),str(session/'DELIVERY_MANIFEST.json')])
live_links=links([WB/'AGENTS.md',WB/'00_RESEARCH_MAP.md',WB/'01_WORKSPACE_STATUS.md',WB/'SOURCE_REGISTER.md'])
validation={'status':'documentation validation passed; no research execution',
    'date':'2026-09-23','checkpoint':'6bc9683b54e4fa80136fe8534d7713e2a250a95f',
    'source_reading_copies_verified':55,'nested_manifest_payload_matches':54,
    'configuration_fields_covered':90,'authored_local_links_validated':session_links,
    'live_navigation_links_validated':live_links,'protected_existing_files_unchanged':len(plan['protected_before']),
    'existing_catalog_rows_unchanged':60,'existing_intake_events_unchanged':True,
    'new_request_source_id':'SRC-061','no_duplicate_final_review_registration':True,
    'prior_checkpoint_and_decision_bytes_unchanged':True,
    'math_delimiters_checked':'New authored documents use dollar delimiters; archive copies remain byte-identical.',
    'shared_files':{name:{'before':plan['live_before'][name]['sha256'],'after':sha((WB/name).read_bytes())} for name in plan['live_before']},
    'research_execution':False,'git_operations':False,
    'validation_scope':'Document links, arithmetic/field coverage, custody and protected-file comparisons; not a new engineering-fidelity review or scientific validation.'}
putjson(session/'VALIDATION.json',validation)

# Export the portable reading package, not local authoring utilities or recovery snapshots.
for f in session.iterdir():
    if f.name.startswith('PRIOR_LIVE_NOTES'): continue
    if f.is_dir(): shutil.copytree(f,export/f.name)
    else: shutil.copyfile(f,export/f.name)
payload={}
for f in sorted(export.rglob('*')):
    if f.is_file(): payload[f.relative_to(export).as_posix()]={'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())}
delivery={'package':'P coupling commissioning design v0.1 review draft','session':plan['session'],
    'checkpoint':'6bc9683b54e4fa80136fe8534d7713e2a250a95f',
    'scope':'Portable reading documents and unchanged selected references; no executable commissioning apparatus.',
    'files':payload,'exclusions':'This manifest, the containing ZIP and its checksum receipt are excluded to avoid self-reference.'}
putjson(export/'DELIVERY_MANIFEST.json',delivery)
shutil.copyfile(export/'DELIVERY_MANIFEST.json',session/'DELIVERY_MANIFEST.json')
links(sorted(export.glob('*.md')))
zip_path=export/'Loom_P_Coupling_Commissioning_Design_20260923_2fb3ff84.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for name in list(payload)+['DELIVERY_MANIFEST.json']:
        z.write(export/name,name)
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    for name,identity in payload.items():
        b=z.read(name)
        assert len(b)==identity['bytes'] and sha(b)==identity['sha256']
receipt={'zip':zip_path.name,'bytes':zip_path.stat().st_size,'sha256':sha(zip_path.read_bytes()),
    'payload_files':len(payload),'manifest_sha256':sha((export/'DELIVERY_MANIFEST.json').read_bytes()),
    'all_payload_hashes_verified_from_zip':True}
putjson(export/'ZIP_RECEIPT.json',receipt)
putjson(session/'EXPORT_RECEIPT.json',dict(receipt,export_directory=str(export)))
for name,digest in plan['protected_before'].items(): assert sha((WB/name).read_bytes())==digest
result={'session':str(session),'export':str(export),'zip':str(zip_path),'receipt':receipt,'validation':validation}
putjson(ROOT/'PUBLISHED_RESULT.json',result)
print(json.dumps({'session':str(session),'export':str(export),'zip':str(zip_path),
    'authored_links':session_links,'live_links':live_links,'protected_unchanged':len(plan['protected_before']),
    'payload_files':len(payload),'zip_bytes':zip_path.stat().st_size,'zip_sha256':receipt['sha256']}))
