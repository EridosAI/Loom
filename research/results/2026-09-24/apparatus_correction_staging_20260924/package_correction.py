"""Assemble/seal the correction review from existing evidence; no world calls."""
import hashlib,json,pathlib,shutil,subprocess,sys,zipfile
S=pathlib.Path(__file__).resolve().parent
PROJECT=pathlib.Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97')
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D=W/'developmental_ecology'; E=D/'artifacts/apparatus-correction-20260924-01a0c405'
DOC=W/'docs/developmental_ecology/p_apparatus_correction_20260924'
PKG=D/'artifacts/review-package-apparatus-correction-20260924-01a0c405'; A=PKG/'assembled'
OLD='05abf60401d08f38750bca589b1c040e10513d7b'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x): p.write_text(json.dumps(x,indent=2),encoding='utf-8')
def copy(source,target): target.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(source,target)
def tree(source,target): shutil.copytree(source,target,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
def evidence(target):
    target.mkdir(parents=True,exist_ok=True)
    for p in E.iterdir():
        if p.is_file(): copy(p,target/p.name)
    for name in ('references','review-evidence'):
        if (target/name).exists():
            for p in (E/name).rglob('*'):
                if p.is_file(): copy(p,target/name/p.relative_to(E/name))
        else: tree(E/name,target/name)
    for folder in E.glob('*faults-*'):
        if folder.is_dir():
            for p in folder.iterdir():
                if p.is_file(): copy(p,target/folder.name/p.name)
def prepare():
    DOC.mkdir(parents=True,exist_ok=False)
    copy(S/'CORRECTION_REPORT.md',DOC/'CORRECTION_REPORT.md')
    for name in ('audit.py','custody.py','legacy_red.py','package_correction.py'):
        copy(S/name,E/name)
    (E/'AUDIT_ATTEMPT_NOTE.json').write_text(json.dumps({'first_attempt':'Direct comparison of original P test checkout bytes with raw Git blobs stopped at test_boundary_and_scheduler.py (CRLF checkout versus LF blob).',
        'correction':'Used git cat-file --filters for exact baseline checkout byte comparison; retained literal blob comparison for all 13 P runtime modules. No file normalization or source edit.',
        'final_record':'UNCHANGED_P_AND_HISTORY.json'},indent=2),encoding='utf-8')
    samples=E/'review-evidence'; samples.mkdir()
    suite=E/'worktree-suite-001'
    for p in sorted(suite.glob('test_boundary_resume_counts_an*')):
        if p.is_dir() and not p.name.endswith('current'): tree(p,samples/p.name)
    for p in sorted(suite.glob('test_final_boundary_resume_can*')):
        if p.is_dir() and not p.name.endswith('current'): tree(p,samples/p.name)
    requests=list(suite.glob('test_approved_execution_bindin*/synthetic-NOT-AUTHORITY.json'))
    assert requests
    copy(requests[0],samples/'SYNTHETIC_APPROVAL_EXAMPLE_NOT_AUTHORITY.json')
    A.mkdir(parents=True,exist_ok=False)
    code=A/'developmental_ecology'; code.mkdir()
    for name in ('loom_p','loom_commissioning','tests','tests_apparatus'): tree(D/name,code/name)
    for name in ('configuration.json','requirements-lock.txt','verify_apparatus.py','verify_corrections.py',
                 'Open Paused Sensor Reference.cmd','Open Privileged Apparatus Review.cmd'):
        copy(D/name,code/name)
    tree(D/'artifacts/prehistory-attempt-001',code/'artifacts/prehistory-attempt-001')
    old=D/'artifacts/apparatus-20260924-01a0c405'
    tree(old/'review-evidence',code/'artifacts/apparatus-20260924-01a0c405/review-evidence')
    tree(old/'references',A/'references/previous-construction')
    evidence(code/'artifacts/apparatus-correction-20260924-01a0c405')
    tree(DOC,A/'docs/developmental_ecology/p_apparatus_correction_20260924')
    original=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX\2026-09-24-p-commissioning-apparatus\Loom_P_Commissioning_Apparatus_Review_20260924.zip')
    assert sha(original)=='87f4dbde39a72559caf6045c7ac68a649d9691a000d1569af5d26b090a63b053'
    copy(original,A/'previous'/original.name)
    review=PROJECT/'exports/2026-09-24-p-apparatus-review-05abf604/Loom_P_Independent_Apparatus_Review_05abf604_20260924.zip'
    copy(review,A/'previous'/review.name)
    (A/'START_HERE.md').write_text('''# Loom P apparatus correction review

Builder verification complete. STOP for independent review; no commissioning is authorized.

Read `docs/developmental_ecology/p_apparatus_correction_20260924/CORRECTION_REPORT.md`,
`CHECKPOINT.json` and `CORRECTION.patch`. Old builder/reviewer archives are preserved under `previous/`.
The exact new evidence, old/new fault matrices and preservation records are under
`developmental_ecology/artifacts/apparatus-correction-20260924-01a0c405/`.
Synthetic approval examples are TEST DATA ONLY, not Jason authorization.

The unchanged `developmental_ecology/Open Paused Sensor Reference.cmd` opens a static saved view.
The separately named privileged view remains for evaluators. These launchers cannot evolve a body.

To reproduce component suites, use Python 3.13.5 and the pinned requirements. From this package's
`developmental_ecology` directory, choose new writable temporary/output paths:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp C:\\Temp\\loom-correction-UNIQUE
python -B -X utf8 verify_apparatus.py C:\\Temp\\loom-old-faults-UNIQUE
python -B -X utf8 verify_corrections.py C:\\Temp\\loom-new-faults-UNIQUE
```

The packaged verified life-0 cache is an explicit test input, never an ambient fallback. These commands
perform manufactured components only. Do not execute historical smoke/prehistory/commissioning commands.
The original 05abf604 RED reproductions are preserved logs; `legacy_red.py` is host-specific provenance,
not a portable current-runtime command. No new dependency installation or cross-platform run was tested.
''',encoding='utf-8')
    print(A)
def seal():
    evidence(A/'developmental_ecology/artifacts/apparatus-correction-20260924-01a0c405')
    for p in DOC.iterdir(): copy(p,A/'docs/developmental_ecology/p_apparatus_correction_20260924'/p.name)
    git=lambda *args:subprocess.check_output(['git','-C',str(W),*args])
    head=git('rev-parse','HEAD').decode().strip(); assert head!=OLD
    assert git('rev-parse','HEAD^').decode().strip()==OLD
    assert not git('status','--porcelain').strip()
    patch=git('diff','--binary',OLD,head); (A/'CORRECTION.patch').write_bytes(patch)
    # Ensure the portable tested code/tests are exactly the final working bytes.
    for folder in ('loom_p','loom_commissioning','tests','tests_apparatus'):
        for p in (D/folder).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:
                assert p.read_bytes()==(A/'developmental_ecology'/p.relative_to(D)).read_bytes(),str(p)
    write(A/'CHECKPOINT.json',{'previous':OLD,'checkpoint':head,'P':'6bc9683b54e4fa80136fe8534d7713e2a250a95f',
        'branch':git('branch','--show-current').decode().strip(),'worktree':str(W),'patch_sha256':hashlib.sha256(patch).hexdigest(),
        'patch_bytes':len(patch),'independent_review_required':True,'commissioning_authorized':False})
    files={p.relative_to(A).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(A.rglob('*')) if p.is_file()}
    write(A/'FILE_MANIFEST.json',{'files':files,'checkpoint':head})
    archive=PKG/'Loom_P_Apparatus_Correction_Review_20260924.zip'
    with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(A.rglob('*')):
            if p.is_file(): z.write(p,p.relative_to(A).as_posix())
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
        for name,row in files.items():
            b=z.read(name); assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    receipt={'zip':str(archive),'bytes':archive.stat().st_size,'sha256':sha(archive),'checkpoint':head,
             'payload_files':len(files),'all_payload_hashes_verified':True}
    write(PKG/'RECEIPT.json',receipt); print(json.dumps(receipt,indent=2))
if __name__=='__main__': globals()[sys.argv[1]]()
