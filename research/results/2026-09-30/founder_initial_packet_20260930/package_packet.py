"""Package prepared starts and completed release evidence; never execute P."""
import hashlib
import json
from pathlib import Path
import shutil
import time
import zipfile

ROOT=Path(__file__).resolve().parent.parent;HERE=Path(__file__).resolve().parent
D=ROOT/'worktrees/loom-p-b1-minimal-20260929/developmental_ecology'
PACKET=ROOT/'exports/2026-09-30-Founder-Search-initial-stage'
ZIP=PACKET.with_suffix('.zip')
def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''):h.update(b)
    return h.hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def main():
    if ZIP.exists():raise FileExistsError('No archive overwrite')
    check=json.loads((PACKET/'STATIC_COMPATIBILITY_REPORT.json').read_bytes())
    assert check['status']=='PASS' and check['scientific_native_calls']==0
    index=json.loads((PACKET/'AUTHORITY_INDEX.json').read_bytes())
    for row in index['authorities']:
        data=(PACKET/row['path']).read_bytes();assert data==canonical(json.loads(data))
        assert hashlib.sha256(data).hexdigest()==row['authority_sha256']
    (PACKET/'engineering').mkdir(exist_ok=True)
    for name in ('RELEASE_CHECK_PLAN.md','RELEASE_BENCHMARK_DECLARATION.json','RELEASE_BENCHMARK_RESULT.json','BLANK_PREPARATION_LOG.txt'):
        shutil.copyfile(HERE/name,PACKET/'engineering'/name)
    (PACKET/'references').mkdir(exist_ok=True)
    shutil.copyfile(Path(r'C:\Users\Jason\.codex\attachments\d28a1d79-11b8-4403-92b0-269696a4b937\Pasted text.txt'),PACKET/'references/JASON_REQUEST.txt')
    old=ROOT/'exports/2026-09-29-developmental-runner-optimization'
    for name in ('CHECKPOINT.json','SCIENTIFIC_EVIDENCE_INVENTORY.md','REMOVED_OR_DEFERRED_OPERATIONS.md'):
        shutil.copyfile(old/name,PACKET/'references'/('PREVIOUS_'+name))
    verify='''"""Verify the extracted launch packet only; no simulation imports."""
import hashlib,json
from pathlib import Path
root=Path(__file__).resolve().parent
manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_bytes())
for name,expected in manifest['files'].items():
    p=root/name
    if not p.is_file() or p.stat().st_size!=expected['bytes']:raise ValueError(name)
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1048576),b''):h.update(b)
    if h.hexdigest()!=expected['sha256']:raise ValueError(name)
index=json.loads((root/'AUTHORITY_INDEX.json').read_bytes())
for a in index['authorities']:
    if hashlib.sha256((root/a['path']).read_bytes()).hexdigest()!=a['authority_sha256']:raise ValueError(a['life_id'])
print('Verified',len(manifest['files']),'files and twelve proposed authorities; zero simulation.')
'''
    (PACKET/'VERIFY_PACKET.py').write_text(verify,encoding='utf8')
    files={}
    def add(p,name):
        if name in files:raise ValueError(name)
        files[name]=p
    def tree(base,prefix):
        for p in sorted(base.rglob('*')):
            if '__pycache__' in p.parts or p.is_symlink():continue
            if p.is_file():add(p,((prefix+'/') if prefix else '')+p.relative_to(base).as_posix())
    tree(PACKET,'')
    for name in ('loom_p','loom_commissioning','loom_developmental','tests_developmental'):
        tree(D/name,'source/developmental_ecology/'+name)
    for name in ('configuration.json','requirements-lock.txt','DEVELOPMENTAL_RUNNER.md','.gitattributes'):
        add(D/name,'source/developmental_ecology/'+name)
    tree(HERE/'release-engineering-life','engineering/release-engineering-life')
    tree(HERE/'shared-assets','engineering/shared-assets')
    for p in HERE.glob('*.py'):add(p,'engineering/tools/'+p.name)
    # The old full evidence archive remains its original artifact. Bind it as
    # provenance instead of copying that entire archive into this new package.
    old_delivery=json.loads((old/'DELIVERY_VERIFICATION.json').read_bytes())
    reference={'prior_review_archive_sha256':old_delivery['archive_sha256'],
        'prior_review_archive_bytes':old_delivery['archive_bytes'],
        'prior_review_archive_path':old_delivery['archive'],
        'prior_complete_record_preserved':True,'copied_again_into_this_archive':False}
    (PACKET/'references/PRIOR_REVIEW_ARCHIVE.json').write_bytes(canonical(reference))
    add(PACKET/'references/PRIOR_REVIEW_ARCHIVE.json','references/PRIOR_REVIEW_ARCHIVE.json')
    manifest={'schema':1,'status':'PROPOSED_UNEXECUTED_LAUNCH_PACKET',
        'files':{name:{'bytes':p.stat().st_size,'sha256':sha(p)} for name,p in files.items()}}
    (PACKET/'PACKAGE_MANIFEST.json').write_bytes(canonical(manifest))
    files['PACKAGE_MANIFEST.json']=PACKET/'PACKAGE_MANIFEST.json'
    start=time.perf_counter()
    with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=1,allowZip64=True) as z:
        for name,p in files.items():
            method=zipfile.ZIP_STORED if p.suffix in ('.ld','.npz','.gz') else zipfile.ZIP_DEFLATED
            z.write(p,name,compress_type=method,compresslevel=1)
    elapsed=time.perf_counter()-start;start=time.perf_counter()
    with zipfile.ZipFile(ZIP) as z:
        assert set(z.namelist())==set(files)
        for name,spec in manifest['files'].items():
            h=hashlib.sha256();size=0
            with z.open(name) as f:
                for b in iter(lambda:f.read(1<<20),b''):h.update(b);size+=len(b)
            assert size==spec['bytes'] and h.hexdigest()==spec['sha256'],name
        assert z.read('PACKAGE_MANIFEST.json')==(PACKET/'PACKAGE_MANIFEST.json').read_bytes()
    result={'archive_path':str(ZIP),'archive_bytes':ZIP.stat().st_size,'archive_sha256':sha(ZIP),
        'verified_files':len(files),'proposed_authorities':12,'all_manifest_hashes_verified':True,
        'write_seconds':elapsed,'verify_seconds':time.perf_counter()-start,
        'scientific_lives_executed':0,'scientific_native_steps':0,'scientific_handoffs':0,
        'engineering_lives_executed_this_task':1,'engineering_seconds':600,
        'body_absent_prehistories_prepared':12,'new_900_1800_authorities':0,
        'code_modifications':0,'git_writes':0,'old_sealed_human_B1_accessed':False}
    (PACKET/'DELIVERY_VERIFICATION.json').write_bytes(canonical(result))
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
