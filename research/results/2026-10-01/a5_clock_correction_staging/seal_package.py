"""Seal already-tested code and review evidence. No simulation or Git writes."""
import hashlib,json,os,pathlib,shutil,subprocess,xml.etree.ElementTree as ET,zipfile
R=pathlib.Path(__file__).resolve().parents[1]
W=R/'worktrees/loom-p-clock-correction-20260926';D=W/'developmental_ecology'
O=R/'exports/2026-09-26-A5-clock-correction';P=O/'portable/Loom_P_Clock_Correction_Review_20260926'
OLD=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
DIAG=R/'exports/2026-09-26-A5-clock-compatibility-review-5f077481'
WB=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
def ident(p):
    with p.open('rb') as f:return {'sha256':hashlib.file_digest(f,'sha256').hexdigest(),'bytes':p.stat().st_size}
def write(p,value):
    assert not p.exists(),p
    p.write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def git(root,*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+root.as_posix(),'-c',
        'core.excludesFile='+(R/'a5_packet_staging_20260926/empty-excludes').as_posix(),'-C',str(root),*args],env=env).decode().strip()
cp=json.loads((O/'CHECKPOINT.json').read_bytes())
assert git(W,'rev-parse','HEAD')==cp['checkpoint'] and not git(W,'status','--porcelain')
assert git(OLD,'rev-parse','HEAD')==cp['parent'] and not git(OLD,'status','--porcelain')
protected=json.loads((O/'PROTECTED_BEFORE.json').read_bytes())
assert all(ident(D/n)['sha256']==h and ident(P/'developmental_ecology'/n)['sha256']==h for n,h in protected.items())
historical=json.loads((DIAG/'SOURCE_IDENTITIES_BEFORE.json').read_bytes())
assert all(ident(pathlib.Path(n))==v for n,v in historical.items())
prior=json.loads((O/'RETROSPECTIVE_SOURCES.json').read_bytes())
assert all(ident(pathlib.Path(n))==v for n,v in prior.items())
assert not (OLD/'developmental_ecology/artifacts/commissioning-A5-20260926-5f077481').exists()
assert not (D/'artifacts/commissioning-A5-20260926-5f077481').exists()
held=R/'exports/2026-09-26-A5-launch-packet-HOLD-5f077481'
delivered=WB/'INBOX/2026-09-26-A5-launch-packet-HOLD-5f077481/A5_LAUNCH_PACKET_HOLD'
hm=json.loads((held/'FILE_MANIFEST.json').read_bytes())['files']
assert all(ident(delivered/n)==v for n,v in hm.items())

summary={'suite_results':{},'new_tests':33,'unchanged_P_tests':59,'existing_apparatus_tests':84,
         'fault_pairs':59,'saved_decisions_compatible':5579,'saved_stage_disagreements':0,
         'A5_runs':0,'new_prehistory':0,'new_launch_authority_objects':0}
for label in ('FINAL_WORKTREE_SUITE','FINAL_PORTABLE_SUITE'):
    receipt=json.loads((O/(label+'-receipt.json')).read_bytes());assert receipt['exit']==0
    tree=ET.parse(O/(label+'.xml')).getroot()
    groups=tree.findall('testsuite') if tree.tag=='testsuites' else [tree]
    counts={k:sum(int(t.attrib.get(k,0)) for t in groups) for k in ('tests','failures','errors','skipped')}
    assert counts=={'tests':176,'failures':0,'errors':0,'skipped':0}
    for name,v in receipt['source_inventory'].items():
        assert ident(D/name)==v and ident(P/'developmental_ecology'/name)==v
    summary['suite_results'][label]={**counts,'wall_seconds':receipt['wall_seconds'],'source_inventory_verified':True}
write(O/'REGRESSION_SUMMARY.json',summary)
write(O/'PRESERVATION_FINAL.json',{
    'protected_P_config_runtime_requirements_adapter_file_count':len(protected),
    'protected_hashes':protected,'historical_source_evidence_files_unchanged':len(historical),
    'original_retrospective_stream_receipts_unchanged':len(prior),'workbench_held_payloads_unchanged':len(hm),
    'held_A5_sha256':ident(held/'AUTHORITY_OBJECT.canonical.json')['sha256'],
    'old_worktree_clean_at':cp['parent'],'new_worktree_clean_at':cp['checkpoint'],
    'new_preparation_or_commissioning_execution':False,'vault_Git_writes':False,
    'physical_world_code_modified':False,'runtime_dependencies_changed':False,
    'limitations':'Checks cover the enumerated source/evidence files. Manufactured regression worlds were explicitly executed; A5 was not.'})

evidence=P/'evidence';evidence.mkdir(exist_ok=False)
for n in ('REQUEST.txt','PROTECTED_BEFORE.json','OLD_FAILURES_RED.json','RETROSPECTIVE_SOURCES.json','CORRECTION_DETAILS.json',
          'RED_GREEN_MATRIX.json','REGRESSION_SUMMARY.json','PRESERVATION_FINAL.json','development-01.log','development-02.log'):
    shutil.copyfile(O/n,evidence/n)
for label in ('FINAL_WORKTREE_SUITE','FINAL_PORTABLE_SUITE'):
    for suffix in ('.log','.xml','-receipt.json'):shutil.copyfile(O/(label+suffix),evidence/(label+suffix))
for label in ('original-apparatus-faults','prior-correction-faults','prior-final-faults','new-clock-faults'):
    dest=evidence/label;dest.mkdir()
    for p in (O/label).iterdir():
        if p.is_file():shutil.copyfile(p,dest/p.name)
shutil.copytree(O/'saved_stage_references',evidence/'saved_stage_references')
for folder in sorted((O/'FINAL_WORKTREE_SUITE-temp').glob('test_late_short_world_pause_re[0-9]')):
    shutil.copytree(folder,evidence/'late_pause_resume_records'/folder.name)
assert len(list((evidence/'late_pause_resume_records').iterdir()))==3
shutil.copytree(DIAG,P/'references/A5_clock_diagnosis')
shutil.copytree(R/'a5_clock_correction_staging',P/'evidence/build_helpers',ignore=shutil.ignore_patterns('__pycache__'))
docs=W/'docs/developmental_ecology/p_clock_correction_20260926'
shutil.copytree(docs,P/'docs/developmental_ecology/p_clock_correction_20260926')
for name in ('CLOCK_SCHEDULING_CORRECTION_REPORT.md','NATIVE_INDEX_SCHEDULING_SPECIFICATION.md'):
    shutil.copyfile(docs/name,P/name)
for name in ('CHECKPOINT.json','CLOCK_SCHEDULING_CORRECTION.patch'):shutil.copyfile(O/name,P/name)
(P/'START_HERE.md').write_text('''# Loom P apparatus clock correction — narrow review

Read [CLOCK_SCHEDULING_CORRECTION_REPORT.md](CLOCK_SCHEDULING_CORRECTION_REPORT.md)
and [NATIVE_INDEX_SCHEDULING_SPECIFICATION.md](NATIVE_INDEX_SCHEDULING_SPECIFICATION.md).

Both complete suites passed 176 tests, from the worktree and this portable source
copy. All 59 fault/control pairs reached intended RED and GREEN. All 5,579 saved
A1–A4 stage decisions agree. Exact logs, JUnit output, inventories, runtime,
preservation receipts and selected complete manufactured pause/resume chains
are under evidence/. CHECKPOINT.json identifies the new local commit, branch
and worktree; CLOCK_SCHEDULING_CORRECTION.patch is its exact diff from 5f077481.

P, configuration, physical adapter, gains and runtime are unchanged. The held
A5 hash 88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6 remains
unmodified and has no grant. This package is not an execution authority or a
declaration of A5 launch fitness. No new launch object is supplied.

## Independent bounded component verification

Use Python 3.13.5 with the unchanged pinned requirements and compare its exact
identity with evidence/CORRECTION_DETAILS.json. Fresh dependency installation
and other runtimes/operating systems were not tested. From developmental_ecology:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
$env:PYTHONDONTWRITEBYTECODE='1'
python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp C:\\Temp\\loom-clock-review-UNIQUE
python -B -X utf8 verify_apparatus.py C:\\Temp\\loom-clock-original-faults-UNIQUE
python -B -X utf8 verify_corrections.py C:\\Temp\\loom-clock-prior-faults-UNIQUE
python -B -X utf8 verify_final_corrections.py C:\\Temp\\loom-clock-final-faults-UNIQUE
python -B -X utf8 verify_clock_scheduling.py C:\\Temp\\loom-clock-new-faults-UNIQUE
```

Choose unused output paths. These are the authorized component/fault checks,
not commissioning or ecological trajectories. The preserved prehistory cache
is read; no new prehistory is generated. Long-clock tests are scalar/detached.
The late physical fixture spans only 0.3 seconds and uses a generic route.

The saved A1–A4 streams/receipts are historical references bound to the old
instrument. Do not replay, migrate or continue them with the new apparatus.
References and helper scripts retain their original context and some original
local paths; do not execute historical scripts merely because they are included.

ARTIFACT_MANIFEST.json binds every payload by SHA-256 and byte count. The ZIP
checksum is supplied separately. Stop for Jason's narrow correction review.
''',encoding='utf-8')

inventory={p.relative_to(P).as_posix():ident(p) for p in sorted(P.rglob('*')) if p.is_file()}
write(P/'ARTIFACT_MANIFEST.json',{'checkpoint':cp['checkpoint'],'execution_authority':False,'files':inventory})
archive=O/'Loom_P_Clock_Correction_Review_20260926.zip'
with zipfile.ZipFile(archive,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for p in sorted(P.rglob('*')):
        if p.is_file():z.write(p,p.relative_to(P).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for name,v in inventory.items():
        raw=z.read(name);assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['sha256']
receipt={'archive':str(archive),**ident(archive),'payloads':len(inventory),'all_hashes_verified':True,
         'checkpoint':cp['checkpoint'],'report':str(P/'CLOCK_SCHEDULING_CORRECTION_REPORT.md')}
write(O/'PACKAGE_RECEIPT.json',receipt)
(O/'Loom_P_Clock_Correction_Review_20260926.zip.sha256').write_text(receipt['sha256']+'  '+archive.name+'\n',encoding='ascii')
print(json.dumps(receipt,indent=2))
