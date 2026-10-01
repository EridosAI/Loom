from pathlib import Path
import hashlib,json,shutil,zipfile

ROOT=Path(__file__).resolve().parent
CWD=ROOT.parent.parent
WB=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench').resolve()
SID=ROOT.name
SESSION='50_SESSIONS/'+SID
BATCH='90_SOURCES/behavioural_watchlist_2026-10-01_e74290ab'
REVIEW='30_REVIEWS/BEHAVIOURAL_DEVELOPMENT_WATCHLIST.md'
LIVE=['AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','02_OPEN_QUESTIONS.md','30_REVIEWS/DEVELOPMENTAL_EVIDENCE_INDEX_2026-10-01_7c219ab4.md','SOURCE_REGISTER.md','SOURCE_CATALOG.json']

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(8*1024*1024),b''):h.update(b)
 return h.hexdigest()
def dump(p,x):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')

assert not (WB/SESSION).exists() and not (WB/BATCH).exists() and not (WB/REVIEW).exists()
assert not (ROOT/'PLAN.json').exists(),'Do not reset original capture'
live={}
for n in LIVE:
 p=WB/n;dest=ROOT/'SHARED_BEFORE'/n;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
 live[n]={'sha256':sha(p),'bytes':p.stat().st_size}
protected={}
for folder in ['10_IDEAS','20_CANDIDATES','30_REVIEWS','40_DECISIONS','50_SESSIONS','90_SOURCES']:
 for p in (WB/folder).rglob('*'):
  if p.is_file() and p.relative_to(WB).as_posix() not in LIVE:protected[p.relative_to(WB).as_posix()]=sha(p)

curves=CWD/'m1_long_development_full_analysis_20261001_v0_1'
manifest=json.loads((curves/'CURVE_PACKAGE_MANIFEST.json').read_text(encoding='utf-8'))
mf={e['path']:e for e in manifest['files']}
inputs=[(Path(r'C:\Users\Jason\.codex\attachments\dcae795a-3a4e-4d90-b0e1-2b5cf9e68403\Pasted text.txt'),'authority/Pasted text.txt','Jason watchlist and maintenance instruction')]
for name in ['H_E_I_DEVELOPMENTAL_CURVES_v0_1.md','README_CURVES.md','CURVE_PACKAGE_MANIFEST.json','CURVE_CONSISTENCY_REVIEW.json','EXTRACTION_VERIFICATION.json','SOURCE_IDENTITY_VERIFICATION.json','INPUT_PROVENANCE.json','CURVE_ARCHIVE_RECORD.json','ANALYSIS_PROTOCOL.md']:
 inputs.append((curves/name,'curves/'+name,'Existing passive curve report / provenance; broader protocol is not a completed result'))
inputs.append((CWD/'m1_resurrection_results_20260930_v0_1/PASSIVE_METHODS.md','sandbox/PASSIVE_METHODS.md','Historical passive methods and descriptive grouping limits'))
catalog=json.loads((WB/'SOURCE_CATALOG.json').read_text(encoding='utf-8-sig'))
assert len(catalog['source_files'])==493
rows=[]
for i,(src,rel,role) in enumerate(inputs,494):
 assert src.is_file()
 h=sha(src);checked=False
 if src.parent==curves and src.name in mf:
  assert h==mf[src.name]['sha256'] and src.stat().st_size==mf[src.name]['bytes'],src.name
  checked=True
 d=ROOT/'NEW'/BATCH/rel;d.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,d)
 rows.append({'source_id':f'SRC-{i:03d}','path':BATCH+'/'+rel,'original_filename':src.name,'original_path':str(src.resolve()),'bytes':src.stat().st_size,'sha256':h,'registered':'2026-10-01','role':role,'storage':'byte-identical-small-file-copy','manifest_match':checked,'record':SESSION+'/INTEGRATION_REPORT.md','authority':'Research organisation only; not scientific or mechanism approval'})
ar=json.loads((curves/'CURVE_ARCHIVE_RECORD.json').read_text(encoding='utf-8'))
archive=Path(ar['path']);assert archive.is_file() and archive.stat().st_size==ar['bytes'] and sha(archive)==ar['sha256']
with zipfile.ZipFile(archive) as z:
 names=z.namelist()
 for name in ['CURVE_PACKAGE_MANIFEST.json','H_E_I_DEVELOPMENTAL_CURVES_v0_1.md']:
  matches=[n for n in names if n==name or n.endswith('/'+name)];assert len(matches)==1
  assert z.read(matches[0])==(curves/name).read_bytes()
rows.append({'source_id':f'SRC-{494+len(inputs):03d}','path':str(archive),'original_filename':archive.name,'bytes':ar['bytes'],'sha256':ar['sha256'],'registered':'2026-10-01','role':'Complete priority curve review package, existing passive analysis','storage':'external-reference-only-NOT-COPIED','manifest_path':BATCH+'/curves/CURVE_PACKAGE_MANIFEST.json','manifest_sha256':sha(curves/'CURVE_PACKAGE_MANIFEST.json'),'archive_sha256_recomputed_by_intake':True,'report_and_manifest_archive_bytes_matched':True,'payload_reverification_by_intake':False,'record':SESSION+'/INTEGRATION_REPORT.md'})
plan={'session':SESSION,'batch':BATCH,'review':REVIEW,'live_before':live,'protected_before':protected,'new_source_rows':rows,'old_source_count':len(catalog['source_files']),'new_source_count':len(catalog['source_files'])+len(rows),'original_inputs':{str(s.resolve()):sha(s) for s,_,_ in inputs},'external_archive':ar,'manifest_matches':sum(r.get('manifest_match',False) for r in rows),'source_copy_count':len(inputs)}
dump(ROOT/'PLAN.json',plan)
print(json.dumps({'session':SESSION,'shared_files':len(live),'protected_files':len(protected),'new_sources':len(rows),'manifest_matches':plan['manifest_matches'],'external_archive_verified':True}))
