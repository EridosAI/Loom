"""Package existing verified records; no world creation or evolution."""
import hashlib,json,pathlib,shutil,subprocess,sys,zipfile
S=pathlib.Path(__file__).resolve().parent
PROJECT=pathlib.Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97')
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405');D=W/'developmental_ecology'
E=D/'artifacts/apparatus-final-correction-20260925-01a0c405'
DOC=W/'docs/developmental_ecology/p_apparatus_final_correction_20260925'
PKG=D/'artifacts/final-review-20260925';A=PKG/'assembled'
OLD='9d31e7902658b15762052a2a6a3d161d64338524'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2),encoding='utf-8')
def copy(p,q):q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q)
def tree(p,q):shutil.copytree(p,q,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
def evidence(target):
    target.mkdir(parents=True,exist_ok=True)
    for p in E.iterdir():
        if p.is_file():copy(p,target/p.name)
    for p in E.iterdir():
        if p.is_dir() and (p.name in ('references','review-evidence','attempt-001-source') or p.name.startswith('old-9d31-')):
            for f in p.rglob('*'):
                if f.is_file() and '__pycache__' not in f.parts:copy(f,target/f.relative_to(E))
        elif p.is_dir() and 'faults-' in p.name:
            for f in p.iterdir():
                if f.is_file():copy(f,target/p.name/f.name)
def prepare():
    DOC.mkdir(parents=True,exist_ok=False)
    for name in ('FINAL_CORRECTION_REPORT.md','LAW_CODE_TEST_MAP.md'):copy(S/name,DOC/name)
    for name in ('setup.py','old_red.py','audit.py','package_final.py'):copy(S/name,E/name)
    samples=E/'review-evidence';samples.mkdir()
    suite=E/'worktree-suite-001'
    prefixes=('test_resume_binding_and_stage_','test_pending_mutation_before_a','test_saved_decision_journal_rej','test_pause_resume_and_reconstr')
    for p in sorted(suite.iterdir()):
        if p.is_dir() and any(p.name.startswith(prefix) for prefix in prefixes) and not p.name.endswith('current'):
            tree(p,samples/p.name)
    A.mkdir(parents=True,exist_ok=False);code=A/'developmental_ecology';code.mkdir()
    for name in ('loom_p','loom_commissioning','tests','tests_apparatus'):tree(D/name,code/name)
    for name in ('configuration.json','requirements-lock.txt','verify_apparatus.py','verify_corrections.py','verify_final_corrections.py',
                 'Open Paused Sensor Reference.cmd','Open Privileged Apparatus Review.cmd'):copy(D/name,code/name)
    tree(D/'artifacts/prehistory-attempt-001',code/'artifacts/prehistory-attempt-001')
    tree(D/'artifacts/apparatus-20260924-01a0c405/review-evidence',code/'artifacts/apparatus-20260924-01a0c405/review-evidence')
    evidence(code/'artifacts/apparatus-final-correction-20260925-01a0c405')
    tree(DOC,A/'docs/developmental_ecology/p_apparatus_final_correction_20260925')
    previous=D/'artifacts/review-package-apparatus-correction-20260924-01a0c405/Loom_P_Apparatus_Correction_Review_20260924.zip'
    assert sha(previous)=='e261dbb9836a916f3ff4b6daa3ae8d9c21ea12194198d1ed63dfa7ee9b798a81'
    copy(previous,A/'previous'/previous.name)
    review=PROJECT/'exports/2026-09-25-p-apparatus-correction-review-9d31e790/Loom_P_Final_Independent_Apparatus_Correction_Review_9d31e790_20260925.zip'
    copy(review,A/'previous'/review.name)
    (A/'START_HERE.md').write_text('''# Loom P: final apparatus mechanical closure review

Builder verification only. STOP for independent mechanical closure review. No commissioning is authorized.

Read `docs/developmental_ecology/p_apparatus_final_correction_20260925/FINAL_CORRECTION_REPORT.md`,
`CHECKPOINT.json`, `FINAL_CORRECTION.patch` and the source/code/test map.
The evidence directory contains the exact requests/review, three original 9d31 RED reproductions,
36 unchanged previous fault pairs, 18 new pairs, complete-suite logs, identity/preservation records,
and new saved examples with their required parent segments. Historical archives remain in `previous/`.

The `old-9d31-*` records require their ORIGINAL apparatus runtime from the prior ZIP; they must not
be silently resumed or claimed valid under this corrected runtime. `old_red.py` and packaging/audit
scripts are exact host-specific provenance, not portable world-execution commands. Synthetic grants
are TEST DATA, not Jason authority. Corrupted record fixtures are clearly retained as negative inputs.

The unchanged double-click `developmental_ecology/Open Paused Sensor Reference.cmd` opens an inert
saved sensor view. Its separately named privileged view is for evaluators. Neither advances a world.

For bounded component reproduction, use Python 3.13.5 with the pinned requirements. From this package's
`developmental_ecology` directory, select fresh writable output paths:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp C:\\Temp\\loom-final-UNIQUE
python -B -X utf8 verify_apparatus.py C:\\Temp\\loom-old-pairs-UNIQUE
python -B -X utf8 verify_corrections.py C:\\Temp\\loom-prior-correction-pairs-UNIQUE
python -B -X utf8 verify_final_corrections.py C:\\Temp\\loom-final-pairs-UNIQUE
```

The life-0 cache is explicitly included, verified and reused; no new preparation is authorized.
Do not execute historical commissioning, smoke or prehistory commands under this corrective authority.
No fresh dependency installation, scientific life or cross-platform verification was performed.
''',encoding='utf-8')
    print(A)
def seal():
    git=lambda *args:subprocess.check_output(['git','-C',str(W),*args])
    head=git('rev-parse','HEAD').decode().strip();assert head!=OLD and git('rev-parse','HEAD^').decode().strip()==OLD
    assert not git('status','--porcelain').strip()
    evidence(A/'developmental_ecology/artifacts/apparatus-final-correction-20260925-01a0c405')
    for p in DOC.iterdir():copy(p,A/'docs/developmental_ecology/p_apparatus_final_correction_20260925'/p.name)
    for name in ('loom_p','loom_commissioning','tests','tests_apparatus'):
        for p in (D/name).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:assert p.read_bytes()==(A/'developmental_ecology'/p.relative_to(D)).read_bytes(),str(p)
    diff=git('diff','--binary',OLD,head);(A/'FINAL_CORRECTION.patch').write_bytes(diff)
    write(A/'CHECKPOINT.json',{'previous':OLD,'checkpoint':head,'P':'6bc9683b54e4fa80136fe8534d7713e2a250a95f',
        'branch':git('branch','--show-current').decode().strip(),'worktree':str(W),
        'diff_sha256':hashlib.sha256(diff).hexdigest(),'diff_bytes':len(diff),
        'stop':'Independent mechanical closure review required; no commissioning fitness declared.'})
    inventory={p.relative_to(A).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(A.rglob('*')) if p.is_file()}
    write(A/'FILE_MANIFEST.json',{'checkpoint':head,'files':inventory})
    output=PKG/'Loom_P_Final_Apparatus_Correction_Review_20260925.zip'
    with zipfile.ZipFile(output,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(A.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(A).as_posix())
    with zipfile.ZipFile(output) as z:
        assert z.testzip() is None
        for name,row in inventory.items():
            raw=z.read(name);assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    receipt={'zip':str(output),'bytes':output.stat().st_size,'sha256':sha(output),'checkpoint':head,
        'inventoried_files':len(inventory),'all_payload_hashes_verified':True}
    write(PKG/'RECEIPT.json',receipt);print(json.dumps(receipt,indent=2))
if __name__=='__main__':globals()[sys.argv[1]]()
