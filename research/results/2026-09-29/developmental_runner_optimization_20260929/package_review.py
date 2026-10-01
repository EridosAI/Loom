"""One final archive from existing evidence; no simulation/import of the runner."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import time
import zipfile

ROOT=Path(__file__).resolve().parent.parent
OPT=Path(__file__).resolve().parent
REVIEW=ROOT/'exports/2026-09-29-developmental-runner-optimization'
W=ROOT/'worktrees/loom-p-b1-minimal-20260929'
D=W/'developmental_ecology'
BASE='a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad'
ZIP=REVIEW.with_suffix('.zip')
GIT=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+str(ROOT/'a5_regeneration_20260926/empty-excludes'),'-C',str(W)]
def git(*args):return subprocess.check_output([*GIT,*args])
def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''):h.update(block)
    return h.hexdigest()
def write(name,v):(REVIEW/name).write_text(json.dumps(v,indent=2)+'\n',encoding='utf8')

def main():
    if ZIP.exists():raise FileExistsError('Do not overwrite an existing archive')
    commit=git('rev-parse','HEAD').decode().strip();parent=git('rev-parse','HEAD^').decode().strip()
    assert parent==BASE
    assert not git('status','--porcelain').strip(),'worktree must be clean'
    changed=git('diff','--name-status',BASE,commit).decode().splitlines()
    assert changed and all(x.startswith('A\tdevelopmental_ecology/') for x in changed)
    write('CHECKPOINT.json',{'commit':commit,'parent':parent,'branch':git('branch','--show-current').decode().strip(),
        'worktree':str(W),'frozen_P':'6bc9683b54e4fa80136fe8534d7713e2a250a95f','git_status':'clean',
        'changed_paths':changed,'push_PR_merge':False,'scientific_execution_authorities_created':False,
        'Founder_Search_lives_executed':0,'new_prehistory':False})
    (REVIEW/'IMPLEMENTATION.patch').write_bytes(git('diff','--binary','--full-index',BASE,commit))
    (REVIEW/'IMPLEMENTATION_STAT.txt').write_bytes(git('diff','--stat',BASE,commit))
    verify_code='''"""Passive package-byte verification only. No P/world/controller imports."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_bytes())
for name,identity in manifest['files'].items():
    path=root/name
    if not path.is_file() or path.stat().st_size!=identity['bytes']:raise ValueError(name)
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''):h.update(block)
    if h.hexdigest()!=identity['sha256']:raise ValueError(name)
print('Verified',len(manifest['files']),'files; zero simulation or controller execution.')
'''
    (REVIEW/'VERIFY_REVIEW.py').write_text(verify_code,encoding='utf8')
    notes='''# Engineering evidence custody and development notes

The archive includes all baseline/performance benchmark measurements and stores, the sole 600-second store, shared identity assets, raw profiling results, final component-test stores, the first failed store-test evidence and every saved text test log. Earlier passing component temporary stores remain preserved locally but are not copied repeatedly into this package. No old sealed human B1 state is included or read.

`engineering/benchmarked_apparatus_before_memory_fix` is the exact source identity used for the longer benchmark, checked against its receipt. `source/` contains the release checkpoint. Intermediate benchmark identities are preserved in their own shared-assets manifests; release changes after the long benchmark were the codec recursive-closure fix, storage minimum-envelope guard, explicitly separate analysis compatibility, final analysis warm-up copy reduction and Python native-runtime boundary binding. No causal operation or recording cadence changed after the long benchmark.

Historical benchmark drivers preserve original host paths for audit. They are not launchers for scientific work. Tests use explicit environment overrides described in the technical documentation. Source/runtime checksums are immutable records, not claims that an arbitrary host can replay bit-exactly.

An initial delivery identity audit compared the existing CRLF configuration checkout directly to the Git LF blob and rejected that byte comparison. The corrected audit separately proves the pre-existing runtime-file SHA and Git-normalized blob, recording both. This was a provenance-format check failure; no configuration was changed. The audit then passed for all 29 frozen files. All development-test and codec failures described in the equivalence report remain disclosed.

The compact review folder is not another full evidence copy. One portable archive is made from existing primary stores only after all engineering execution and analysis completes. Compressed evidence members are stored without recompression; small text/source files are deflated. No ongoing background worker or live inspector is part of this delivery.
'''
    (REVIEW/'ENGINEERING_CUSTODY_NOTES.md').write_text(notes,encoding='utf8')
    files={}
    def add(p,name):
        if name in files:raise ValueError('duplicate archive name '+name)
        files[name]=Path(p)
    def tree(base,prefix):
        for p in sorted(Path(base).rglob('*')):
            rel=p.relative_to(base)
            if any(x.endswith('current') or x=='__pycache__' for x in rel.parts):continue
            if p.is_file() and not p.is_symlink():add(p,prefix+'/'+rel.as_posix())
    for p in sorted(REVIEW.iterdir()):
        if p.is_file() and p.name not in ('PACKAGE_MANIFEST.json','DELIVERY_VERIFICATION.json'):add(p,p.name)
    for name in ('loom_p','loom_commissioning','loom_developmental','tests_developmental'):
        tree(D/name,'source/developmental_ecology/'+name)
    for name in ('configuration.json','requirements-lock.txt','DEVELOPMENTAL_RUNNER.md','.gitattributes'):
        add(D/name,'source/developmental_ecology/'+name)
    for name in ('baseline','measurements','benchmarked_apparatus_before_memory_fix','component-temp-release','store-temp-001'):
        tree(OPT/name,'engineering/'+name)
    for p in sorted(OPT.iterdir()):
        if p.is_file():add(p,'engineering/'+p.name)
    cache=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\developmental_ecology\artifacts\prehistory-attempt-001')
    tree(cache,'engineering/preserved-prehistory-attempt-001')
    add(Path(r'C:\Users\Jason\.codex\attachments\400b7786-b3fc-4525-b4cb-f23c18150dff\Pasted text.txt'),'references/JASON_ENGINEERING_REQUEST.txt')
    prior=ROOT/'exports/2026-09-29-Founder-Search-v0-1-design'
    for name in ('RESOURCE_CALCULATIONS.json','JASON_TIMING_RULING.md','FOUNDER_SEARCH_v0_1_DESIGN.md'):
        add(prior/name,'references/prior-design/'+name)
    add(ROOT/'sources/00_LOOM_CURRENT_STATE(2).md','references/00_LOOM_CURRENT_STATE(2).md')
    started=time.perf_counter()
    manifest={'schema':1,'purpose':'portable engineering review; no execution authority','checkpoint':commit,
        'files':{name:{'bytes':p.stat().st_size,'sha256':digest(p)} for name,p in files.items()}}
    write('PACKAGE_MANIFEST.json',manifest);files['PACKAGE_MANIFEST.json']=REVIEW/'PACKAGE_MANIFEST.json'
    manifest_seconds=time.perf_counter()-started
    started=time.perf_counter();long_bytes=0;long_seconds=0.
    with zipfile.ZipFile(ZIP,'x',allowZip64=True,compression=zipfile.ZIP_DEFLATED,compresslevel=1) as archive:
        for name,p in files.items():
            method=zipfile.ZIP_STORED if p.suffix in ('.ld','.gz','.npz','.pstats') else zipfile.ZIP_DEFLATED
            tick=time.perf_counter();archive.write(p,name,compress_type=method,compresslevel=1)
            if name.startswith('engineering/measurements/long/'):
                long_seconds+=time.perf_counter()-tick;long_bytes+=archive.getinfo(name).compress_size
    archive_seconds=time.perf_counter()-started
    started=time.perf_counter()
    with zipfile.ZipFile(ZIP) as archive:
        assert set(archive.namelist())==set(files)
        for name,spec in manifest['files'].items():
            h=hashlib.sha256();size=0
            with archive.open(name) as f:
                for block in iter(lambda:f.read(1<<20),b''):h.update(block);size+=len(block)
            assert size==spec['bytes'] and h.hexdigest()==spec['sha256'],name
        assert archive.read('PACKAGE_MANIFEST.json')==(REVIEW/'PACKAGE_MANIFEST.json').read_bytes()
    check_seconds=time.perf_counter()-started
    result={'checkpoint':commit,'archive':str(ZIP),'archive_sha256':digest(ZIP),'archive_bytes':ZIP.stat().st_size,
        'verified_files':len(files),'manifest_seconds':manifest_seconds,'archive_write_seconds':archive_seconds,
        'archive_verify_seconds':check_seconds,'long_evidence_archive_payload_bytes':long_bytes,
        'long_evidence_archive_write_seconds':long_seconds,'raw_source_bytes_total':sum(p.stat().st_size for p in files.values()),
        'all_manifest_hashes_verified':True,'world_or_P_steps_during_packaging':0,'complete_evidence_archive_copies_created':1,
        'extra_unpacked_evidence_copy_created':False,'old_sealed_human_B1_material_accessed':False}
    write('DELIVERY_VERIFICATION.json',result)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
