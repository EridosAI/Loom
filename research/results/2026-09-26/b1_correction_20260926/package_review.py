"""Assemble and hash review evidence. No simulation, authority creation or Git mutation."""
import hashlib,json,os,pathlib,shutil,subprocess,zipfile
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926';D=W/'developmental_ecology'
DOC=W/'docs/developmental_ecology/p_b1_operator_correction_20260926'
H=ROOT/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02'
BASE='68db2c581f07200966d699a4f55a65f9b96df1e9'
receipt=json.loads((S/'COMMIT_RECEIPT.json').read_bytes());HEAD=receipt['commit']
BATCH=ROOT/('exports/2026-09-26-B1-operator-correction-'+HEAD[:8]+'-review-02')
PKG=BATCH/'B1_OPERATOR_APPARATUS_CORRECTION_REVIEW'
assert not BATCH.exists();PKG.mkdir(parents=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,value):p.write_text(json.dumps(value,indent=2)+'\n',encoding='utf-8')
def copy(source,dest):dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dest)
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env)
assert git('rev-parse','HEAD').decode().strip()==HEAD and git('status','--porcelain')==b''
copy(S/'COMMIT_RECEIPT.json',PKG/'CHECKPOINT.json')
(PKG/'EXACT_DIFF_68db2c58_to_352f73ff.patch').write_bytes(git('diff','--binary','--full-index',BASE,HEAD,'--'))
(PKG/'COMMIT_RECORD.txt').write_bytes(git('show','--no-patch','--format=fuller',HEAD))
(PKG/'DIFF_STAT.txt').write_bytes(git('diff','--stat',BASE,HEAD))
shutil.copytree(S/'portable-source',PKG/'source')
shutil.copytree(DOC,PKG/'docs')
old=ROOT/'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
# Include committed baseline source, not unrelated historical generated artifacts.
for name in git('ls-tree','-r','--name-only',BASE,'--','developmental_ecology').decode().splitlines():
    relative=pathlib.PurePosixPath(name).relative_to('developmental_ecology')
    source=old/relative
    assert git('hash-object','--path='+name,str(source)).strip()==git('rev-parse',BASE+':'+name).strip()
    copy(source,PKG/'baseline-68db'/name)
shutil.copytree(old/'artifacts/prehistory-attempt-001',PKG/'baseline-68db/developmental_ecology/artifacts/prehistory-attempt-001')
copy(D/'.gitattributes',PKG/'source/developmental_ecology/.gitattributes')

# All component records are disposable invented/manufactured evidence, not held fixtures.
for name in ('SEALED_REGRESSION-temp','PORTABLE_REGRESSION-temp','before-temp'):
    shutil.copytree(S/name,PKG/'evidence/component-records'/name,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
for name in ('fault-matrix','fault-matrix-final','fault-matrix-sealed'):
    shutil.copytree(S/name,PKG/'evidence'/name,ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
for p in sorted(S.glob('*')):
    if p.is_file() and (p.suffix in ('.log','.xml') or p.name in (
        'PORTABLE_SOURCE_IDENTITIES.json','PREFLIGHT.json','REGRESSION_RESULTS.json','FINAL_PRESERVATION.json','STATIC_HELD_COMPATIBILITY.json',
        'UI_REVIEW.json','SOURCE_IDENTITIES.json','RUNTIME_RECORD.json','EXECUTION_SCOPE_RECORD.json','P_CONFIG_WORLD_UNCHANGED.json')):
        copy(p,PKG/'evidence'/p.name)
for name in ('test_before_correction.py','browser_fixture.py','BROWSER_OBSERVED_SENSOR.html','static_compatibility.py','run_faults.py',
             'preservation_and_portable.py','prepare_review_records.py','commit_correction.py','package_review.py'):
    copy(S/name,PKG/'task-utilities'/name)
request=pathlib.Path(r'C:\Users\Jason\.codex\attachments\832f5af3-01d7-417d-83b2-4e889158997a\Pasted text.txt')
copy(request,PKG/'sources/JASON_AUTHORIZED_CORRECTION.txt')
for name in ('OPEN_ISSUE_B1_INTERFACE.md','PROTOCOL_CONTRACT.json','DISPLAY_CONTRACT.json','RECORDING_CONTRACT.json','PREPARATION_CHECKS.json','STATIC_COMPATIBILITY_FINDINGS.json','HELD_REVIEW_IDENTITY.json'):
    copy(H/'B1_OPERATOR_REVIEW'/name,PKG/'sources/held-operator-safe'/name)

readme=f'''# B1 apparatus correction: independent review package

**Checkpoint:** `{HEAD}`  
**Parent:** `{BASE}`  
**P:** `6bc9683b54e4fa80136fe8534d7713e2a250a95f`  
**Status:** apparatus correction implemented and component-tested; independent narrow review pending. No B1 launch-fitness declaration or execution authority.

Read [the report](docs/B1_OPERATOR_APPARATUS_CORRECTION_REPORT.md), [information flow](docs/CHEMISTRY_DEPRIVATION_INFORMATION_FLOW.md), [lifecycle](docs/LIVE_OPERATOR_STATE_MACHINE.md), and [RED→GREEN matrix](docs/RED_GREEN_MATRIX.md). Exact branch/worktree are in `CHECKPOINT.json`; exact code/tests/docs diff and commit record are at this level.

## Evidence

- Final worktree: 204 passed in 143.82 seconds. Final byte-identical portable source: 204 passed in 143.73 seconds.
- Final A–L matrix: 12 deliberate, consequential assertion failures and 12 passing controls. Earlier runs remain labeled separately.
- Two baseline failures against unmodified 68db are preserved. Their expected nonzero result is evidence, not an unresolved regression.
- `source/developmental_ecology` is the tested portable tree. `baseline-68db/developmental_ecology` is a read-only baseline copy for review. Each includes the existing lawful component cache; neither includes held B1 state.
- Full raw logs/JUnit and final component records are under `evidence`. Actual-physics tests use invented/manufactured fixtures; fault I and the browser transport use nonphysical synchronization/transport stubs.
- `docs/FINAL_PRESERVATION.json` checks byte identities and committed blobs, including original P/config and parent clock. Existing Git newline filters are respected; the unchanged configuration checkout is CRLF while Git stores LF.
- `docs/STATIC_HELD_COMPATIBILITY.json` is a static result only. It exposes public case identifiers/horizons and opaque snapshot hashes, not evaluator truth. Held custody `{json.loads((S/'PREFLIGHT.json').read_bytes())['held_review_hash']}` stays unchanged and non-launchable.

## Component-only reproduction

Do not run a commissioning launcher, create a new authority, load held fixtures, invoke a legacy inspector against a world, or replay an ecological record during this correction review. Legacy source entry points are included for exact source preservation, not as new authorization. `task-utilities` records this task's local preparation and packaging; those utilities have local paths and are not general launch/reproduction tools.

Use Python 3.13.5 and the pinned `requirements-lock.txt`, with Node v22.16.0 on PATH (or `NODE_BIN` set to its executable). The delivered runtime JSON records actual package/executable content identities. No runtime installation is bundled. From `source/developmental_ecology`, run the explicitly authorized component suite:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:PYTHONPATH = (Get-Location).Path
python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --junitxml=review-component-results.xml
```

The existing cached prehistory is required by legacy component tests. Preserve it; do not generate a new cache. Node is a test tool, not a live feedback path.

For a single fault/control check, select its exact node from the saved matrix. Set `B1_FAULT` to the letter only for the RED invocation, expect the named single assertion failure, then remove the environment value and repeat for GREEN. Example H, both manufactured:

```powershell
$env:B1_FAULT = 'H'
python -B -X utf8 -m pytest tests_apparatus/test_b1_operator.py::test_H_duplicate_token -q -p no:cacheprovider
Remove-Item Env:B1_FAULT
python -B -X utf8 -m pytest tests_apparatus/test_b1_operator.py::test_H_duplicate_token -q -p no:cacheprovider
```

These instructions reproduce component evidence, not PC/B1 trials. No new tests were executed merely to package this delivery.

## Integrity and boundaries

`PAYLOAD_MANIFEST.json` hashes every other package file. `ARCHIVE_RECEIPT.json` alongside the ZIP records its hash/size and successful archive verification. Opaque hashes are custody evidence, not grants. The package has no sealed evaluator snapshot/manifest/archive or B1 execution authority.

No prepared positive control, B1, ecological trajectory or ecological replay occurred. Existing and new manufactured reconstruction checks are disclosed. No new prehistory, tuning, P/config/world change, push, PR, merge or vault Git write occurred. Historical A1–A5 evidence is unchanged. Interactive history-growth cost and actual human competence remain untested. Stop for narrow independent correction review; later packet regeneration/authorization is a separate decision.
'''
(PKG/'README.md').write_text(readme,encoding='utf-8')

# Verify byte-identical portable source and no copied held initial states/manifests.
source_ids=json.loads((S/'PORTABLE_SOURCE_IDENTITIES.json').read_bytes())
assert all(sha(PKG/'source/developmental_ecology'/n)==h for n,h in source_ids.items())
original=json.loads((S/'HELD_PRESERVATION_BEFORE.json').read_bytes())
assert all(sha(pathlib.Path(p))==h for p,h in original.items())
sealed_hashes={h for p,h in original.items() if 'B1_PRIVILEGED_EVALUATOR_HOLD' in p and ('initial-states' in p or 'case-manifests' in p)}
payload={p.relative_to(PKG).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(PKG.rglob('*')) if p.is_file()}
assert not sealed_hashes.intersection(v['sha256'] for v in payload.values())
assert not any('B1_PRIVILEGED_EVALUATOR_HOLD' in name for name in payload)
write(PKG/'PAYLOAD_MANIFEST.json',dict(schema=1,checkpoint=HEAD,excludes_self=True,files=payload))
archive=BATCH/'B1_OPERATOR_APPARATUS_CORRECTION_REVIEW.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(PKG.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(BATCH).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for name,record in payload.items():assert hashlib.sha256(z.read(PKG.name+'/'+name)).hexdigest()==record['sha256']
    assert z.read(PKG.name+'/PAYLOAD_MANIFEST.json')==(PKG/'PAYLOAD_MANIFEST.json').read_bytes()
result=dict(checkpoint=HEAD,archive_name=archive.name,archive_sha256=sha(archive),archive_bytes=archive.stat().st_size,
    payload_files=len(payload),payload_bytes=sum(v['bytes'] for v in payload.values()),manifest_sha256=sha(PKG/'PAYLOAD_MANIFEST.json'),
    every_payload_hash_verified=True,zip_crc_verified=True,sealed_initial_snapshot_or_manifest_copied=False,
    held_preservation_rechecked=len(original),worktree_clean=git('status','--porcelain')==b'',
    no_new_execution_for_packaging=True,status='STOP FOR INDEPENDENT NARROW CORRECTION REVIEW')
write(BATCH/'ARCHIVE_RECEIPT.json',result)
write(S/'PACKAGE_RECEIPT.json',dict(batch=str(BATCH),package=str(PKG),**result))
print(json.dumps(result,indent=2))
