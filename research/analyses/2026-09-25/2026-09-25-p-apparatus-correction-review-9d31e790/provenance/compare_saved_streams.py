"""Preserved Python-stdin payload of the executed read-only comparison."""
from pathlib import Path
import gzip,json,hashlib
root=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology/artifacts')
out=Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-25-p-apparatus-correction-review-9d31e790\provenance')
old=root/'apparatus-20260924-01a0c405/review-evidence/records';new=root/'apparatus-correction-20260924-01a0c405/worktree-suite-001'
names={'external_controller':'external-manufactured','intact_P':'intact-manufactured','FIXED-STRUCTURE / NO-LASTING-PLASTICITY DIAGNOSTIC':'fixed-manufactured'}
results=[]
for d in sorted(new.glob('test_pause_resume_and_reconstr*')):
 p=d/'continuous';m=json.loads((p/'manifest.json').read_bytes());mode=m['contract']['mode'];rows={}
 for name in ('native','wave','events','diagnostics','controller','sensor','scientific_observations'):
  oldb=gzip.decompress((old/names[mode]/'continuous'/(name+'.jsonl.gz')).read_bytes());newb=gzip.decompress((p/(name+'.jsonl.gz')).read_bytes());assert oldb==newb,(mode,name)
  rows[name]={'uncompressed_bytes':len(newb),'sha256':hashlib.sha256(newb).hexdigest(),'rows':len(newb.splitlines()),'exact_previous_05ab_bytes':True}
 results.append({'mode':mode,'streams':rows})
assert len(results)==3
before=json.loads((out/'scoped-complete/TARGET_BEFORE.json').read_bytes());after={p.relative_to(root).as_posix():{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in root.rglob('*') if p.is_file()};assert before==after
with (out/'PREVIOUS_STREAM_COMPARISON.json').open('x',encoding='utf-8') as f:json.dump({'modes':results,'streams_verified':21,'all_uncompressed_stream_bytes_equal_previous_runtime':True,'target_files_still_unchanged':len(after)},f,indent=2)
print(json.dumps({'modes':len(results),'streams':21,'all_equal':True,'target_files_unchanged':len(after)},indent=2))
