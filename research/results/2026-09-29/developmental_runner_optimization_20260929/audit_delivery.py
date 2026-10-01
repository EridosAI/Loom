"""Read-only identity/release audit; no native/P evolution."""
import hashlib
import json
import subprocess
from pathlib import Path
from benchmark import ROOT,D,OUT
from loom_p.records import code_identity
from loom_commissioning.runner import load_restart
from loom_developmental import codec,core
from loom_developmental.runner import identity

W=D.parent;BASE='a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad'
DEST=ROOT/'exports/2026-09-29-developmental-runner-optimization'
cmd=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+str(ROOT/'a5_regeneration_20260926/empty-excludes'),'-C',str(W)]
def git(*args):return subprocess.check_output([*cmd,*args])
def sha(b):return hashlib.sha256(b).hexdigest()
files={}
for package in ('loom_p','loom_commissioning'):
    for p in sorted((D/package).rglob('*.py')):
        rel=p.relative_to(W).as_posix();before=git('show',BASE+':'+rel)
        assert before==p.read_bytes(),rel
        files[rel]={'sha256':sha(before),'unchanged':True}
p=D/'configuration.json';blob=git('show',BASE+':developmental_ecology/configuration.json')
assert p.read_bytes().replace(b'\r\n',b'\n')==blob
assert sha(p.read_bytes())=='985d2de66f9f378765bd3a2ceba75bfe210a5bf7fe30be6716dd1051bb2315a9'
files['developmental_ecology/configuration.json']={'sha256':sha(p.read_bytes()),'unchanged':True,
    'git_blob_sha256':sha(blob),'checkout_note':'Existing Git CRLF checkout versus LF blob; original runtime-file hash also verified exactly'}
old,_,_=load_restart(OUT/'old-short/final.restart.json.gz')
receipt=json.loads((OUT/'lean-short-release/segment-000.json').read_bytes())
lean=codec.read(OUT/'lean-short-release'/receipt['final_checkpoint']['file'])['engine']
assert codec.encode(core.causal_state(old))==codec.encode(core.causal_state(lean))
long_receipt=json.loads((OUT/'long/segment-000.json').read_bytes())
long_binding=json.loads((OUT/'shared-assets'/(long_receipt['identity_sha256']+'.json')).read_bytes())
saved=ROOT/'developmental_runner_optimization_20260929/benchmarked_apparatus_before_memory_fix'
assert {p.name:sha(p.read_bytes()) for p in saved.glob('*.py')}==long_binding['apparatus']
value={'parent':BASE,'branch':git('branch','--show-current').decode().strip(),'frozen_P_commit':'6bc9683b54e4fa80136fe8534d7713e2a250a95f',
       'P_file_set':code_identity(),'files':files,'release_short_exact_old_endpoint':True,
       'release_causal_endpoint_sha256':codec.digest(core.causal_state(lean)),
       'long_benchmark_source_preserved_and_exact':True,'long_recording_identity':long_receipt['identity_sha256'],
       'release_runtime_identity':identity(),'new_world_steps':0,'P_steps':0}
(DEST/'FROZEN_IDENTITY_VERIFICATION.json').write_text(json.dumps(value,indent=2))
print(json.dumps({'verified_unchanged_files':len(files),'release_short_exact_old_endpoint':True,'long_source_exact':True},indent=2))
