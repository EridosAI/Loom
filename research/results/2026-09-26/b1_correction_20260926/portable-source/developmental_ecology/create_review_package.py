"""Create an honest local checkpoint manifest/review ZIP; never executes a simulation."""
import argparse
from dataclasses import asdict
from datetime import datetime,timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
import zipfile
from loom_p.schema import Config
from loom_p.records import strict_bytes,code_identity

ROOT=Path(__file__).resolve().parent
REPO=ROOT.parent
DOCS=REPO/'docs'/'developmental_ecology'/'p_engineering_20260921'
WORKBENCH=Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
DELIVERY=WORKBENCH/'INBOX'/'2026-09-21-p-engineering-build'
BASE='98a8307e56f6884f2cc5dfb29ef924294f629c22'
ARCHIVE='f1b884a7ada4c806786d1530d76d446aac5d37b1'

def digest(data): return hashlib.sha256(data).hexdigest()
def git(*args): return subprocess.check_output(['git','-C',str(REPO),*args],text=True).strip()
def source_identities():
    manifest=json.loads((DELIVERY/'SOURCE_MANIFEST.json').read_text())
    rows=[]
    for row in manifest['sources']:
        path=DELIVERY/row['path']; data=path.read_bytes()
        if len(data)!=row['bytes'] or digest(data)!=row['sha256']: raise ValueError(f'Packaged source changed: {path}')
        rows.append(dict(path=str(path),package_path=row['path'],bytes=len(data),sha256=digest(data),manifest_match=True))
    additional=[WORKBENCH/'AGENTS.md',WORKBENCH/'00_RESEARCH_MAP.md',WORKBENCH/'01_WORKSPACE_STATUS.md',DELIVERY/'LOOM_P_ENGINEERING_BUILD_HANDOFF_2026-09-21.md',DELIVERY/'SOURCE_MANIFEST.json',WORKBENCH/'40_DECISIONS'/'DECISION-P-SPECIFICATION-2026-09-20-83a00674.md']
    foundation=WORKBENCH/'90_SOURCES'/'reference_7ada2b300fa1'
    additional.append(foundation/'00_LOOM_CURRENT_STATE.md')
    for name in ('DEVELOPMENTAL_ECOLOGY_DESIGN_FRAME_v0_2.md','PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1.md','BASE_WORLD_COMPLETION_v0_1.md','DEVELOPMENTAL_ECOLOGY_DECISION_LEDGER_v0_2.md'):
        additional.append(foundation/'docs'/'developmental_ecology'/name)
    for path in additional:
        data=path.read_bytes(); row=dict(path=str(path),bytes=len(data),sha256=digest(data),manifest_match='not_in_five_file_manifest')
        if path.is_relative_to(foundation):
            relative=path.relative_to(foundation).as_posix()
            row['pinned_commit']='7ada2b300fa12a26b0daf40b1fa5682243ff6625'
            row['pinned_git_blob']=git('rev-parse',row['pinned_commit']+':'+relative)
            original=subprocess.check_output(['git','-C',str(REPO),'show',row['pinned_commit']+':'+relative])
            row['pinned_blob_sha256']=digest(original)
            row['current_workbench_bytes_equal_git_blob']=data==original
            row['note']='Current reading copy identity and pinned Git blob identity are separate; authorized workbench formatting is not assumed byte-identical.'
        rows.append(row)
    return dict(schema_version=1,verified_at=datetime.now(timezone.utc).isoformat(),reference_commit_not_remote_head='7ada2b300fa12a26b0daf40b1fa5682243ff6625',sources=rows)

def artifact_inventory():
    rows={}
    for path in sorted((ROOT/'artifacts').rglob('*')):
        if not path.is_file() or any(x.startswith('review-package-') for x in path.parts) or '__pycache__' in path.parts: continue
        data=path.read_bytes(); relative=path.relative_to(REPO).as_posix()
        included=not ('smoke-birth_30s-' in relative and path.name in ('native.jsonl.gz','wave.jsonl.gz','events.jsonl.gz'))
        rows[relative]=dict(bytes=len(data),sha256=digest(data),included_in_portable_review=included,local_path=str(path))
    return rows

def prepare():
    DOCS.mkdir(parents=True,exist_ok=True)
    config=json.loads((ROOT/'configuration.json').read_text(encoding='utf-8')); c=Config(**config).validate()
    if c.identity()!=Config().identity(): raise ValueError('Selected configuration differs from reviewed defaults')
    source=source_identities(); (DOCS/'SOURCE_IDENTITIES.json').write_bytes(strict_bytes(source))
    runtime=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),git=git('--version'),dependencies={name:importlib.metadata.version(name) for name in ('numpy','scipy','pytest','colorama','iniconfig','packaging','pluggy','pygments')},code=code_identity(),configuration_sha256=c.identity(),configuration_file_sha256=digest((ROOT/'configuration.json').read_bytes()),snapshot_binary='IEEE-754 binary64 arrays encoded losslessly; strict JSON metadata',cross_platform_bit_identity_claimed=False,model_and_reasoning_effort='Not independently measured; no claim of backend setting',selected_ruling='JASON_RULING_2026-09-22.md')
    (DOCS/'RUNTIME_RECORD.json').write_bytes(strict_bytes(runtime))
    reconstruction=json.loads((ROOT/'artifacts/verification/record-reconstruction.json').read_text())
    ui=json.loads((ROOT/'artifacts/verification/ui-verification.json').read_text())
    attempts=[]
    for path in sorted((ROOT/'artifacts').glob('smoke-*-attempt-*/manifest.json')):
        m=json.loads(path.read_text()); attempts.append({k:m.get(k) for k in ('case','attempt','status','complete','error','records','simulated_seconds_cap','correction_reason','code','configuration_sha256','resume_identical','observer_noninterference','comparison_trajectory_seconds')})
    for result in reconstruction['cases']:
        manifest=json.loads((Path(result['path'])/'manifest.json').read_text())
        if not manifest['complete'] or manifest['code']!=code_identity(): raise ValueError('Final smoke code mismatch')
    log=(ROOT/'artifacts/verification/component-attempt-006.txt').read_bytes().decode('utf-8-sig')
    if '44 passed' not in log or 'FAILED' in log: raise ValueError('Final component result is not verified')
    verification=dict(status='bounded_engineering_verification_complete_uncommissioned',component_suite=dict(passed=44,failed=0,log='developmental_ecology/artifacts/verification/component-attempt-006.txt'),complete_loop_cases=reconstruction['cases'],all_attempts=attempts,prehistory='developmental_ecology/artifacts/prehistory-attempt-001/manifest.json',prehistory_reexecuted=False,information_loss='developmental_ecology/artifacts/information_loss.json',ui=ui,unique_complete_loop_cases=3,total_complete_loop_simulated_seconds_including_failed_prefixes_and_comparisons=63.47,scientific_lifetimes=0,cohorts=0,sweeps=0,efficacy_tuning=False,background_simulations_remaining=0,terminal_scope='Scheduler stand-in plus real physics component crossing; no natural terminal complete-loop event',scope='Engineering fidelity only; no survival/useful learning gate')
    (DOCS/'VERIFICATION_SUMMARY.json').write_bytes(strict_bytes(verification))
    (DOCS/'EVIDENCE_MANIFEST.json').write_bytes(strict_bytes(artifact_inventory()))
    commands=['# Execution ledger', '', 'All commands below ran locally in developmental_ecology with the isolated worktree Python. Exact outputs and manifests are preserved; no remote operation was issued.', '', '```powershell', '..\\.venv\\Scripts\\python.exe -m pytest tests -q', '```', '', 'Final log: artifacts/verification/component-attempt-006.txt (44 passed). Earlier attempts remain in that directory.', '']
    for path in sorted((ROOT/'artifacts').glob('smoke-*-attempt-*/manifest.json')):
        m=json.loads(path.read_text()); cmd=f"..\\.venv\\Scripts\\python.exe -m loom_p.smokes {m['case']} --attempt {m['attempt']}"
        if m['correction_reason']: cmd+=' --correction-reason '+json.dumps(m['correction_reason'])
        commands.extend(['```powershell',cmd,'```',f"Result: {m['status']}; complete={m['complete']}; records={m.get('records')}. Manifest: {path.relative_to(ROOT).as_posix()}",''])
    commands.extend(['```powershell','..\\.venv\\Scripts\\python.exe verify_engineering_records.py',"Start-Process -FilePath '.\\Open Loom Inspector.cmd' -WorkingDirectory (Get-Location).Path -WindowStyle Hidden -PassThru",'```','','The record verifier performs detached arithmetic only. Actual browser controls selected saved record 40, reconstructed it, then advanced the fixed contact prefix by one native step and to the first wave boundary, paused and stopped. ui-verification.json compares every UI record with its existing-case prefix.','', 'Scoped copy/edit/source-hash inspection and metadata/package commands do not execute organisms. Package creation command: `..\\.venv\\Scripts\\python.exe create_review_package.py --package` after the local commit.',''])
    (DOCS/'EXECUTION_LEDGER.md').write_text('\n'.join(commands),encoding='utf-8')
    print('Prepared final source, runtime, configuration, verification and evidence records.')

def package():
    source=source_identities(); commit=git('rev-parse','HEAD'); branch=git('branch','--show-current'); tree=git('rev-parse','HEAD:EXP1-21')
    if tree!=ARCHIVE: raise ValueError('Historical archive tree mismatch; not repaired')
    if commit in (BASE,'bf5df05ad2aafb8590e8765a947df111956b9528'): raise ValueError('Final continuation commit is missing')
    for name,row in code_identity()['files'].items():
        committed=subprocess.check_output(['git','-C',str(REPO),'show',commit+':developmental_ecology/loom_p/'+name])
        if digest(committed)!=row: raise ValueError('Committed runtime bytes do not match verified code: '+name)
    if git('status','--porcelain','--','developmental_ecology','docs/developmental_ecology/p_engineering_20260921'): raise ValueError('Task-owned files are not fully committed')
    directory=ROOT/'artifacts'/'review-package-20260922-01a0c405'; directory.mkdir(exist_ok=False)
    receipt=dict(schema_version=1,status='bounded_engineering_build_complete_uncommissioned',worktree=str(REPO),branch=branch,commit=commit,continued_from='bf5df05ad2aafb8590e8765a947df111956b9528',base=BASE,archive_tree_before=ARCHIVE,archive_tree_after=tree,archive_unchanged=True,code=code_identity(),configuration_sha256=Config().identity(),prepared_at=datetime.now(timezone.utc).isoformat(),source_recheck=source,smokes_run=True,unique_cases=3,no_remote_operation=True,review_boundary='Stop; no scientific run authorized',evidence_inventory='docs/developmental_ecology/p_engineering_20260921/EVIDENCE_MANIFEST.json')
    (directory/'CHECKPOINT_RECEIPT.json').write_bytes(strict_bytes(receipt))
    chosen={}
    for folder in (ROOT/'loom_p',ROOT/'tests',DOCS):
        for path in folder.rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts and path.suffix!='.pyc': chosen[path.relative_to(REPO).as_posix()]=path.read_bytes()
    for name in ('configuration.json','requirements-lock.txt','README.md','Open Loom Inspector.cmd','Setup Loom Inspector.cmd','create_review_package.py','verify_engineering_records.py','.gitignore','.gitattributes'):
        path=ROOT/name; chosen[path.relative_to(REPO).as_posix()]=path.read_bytes()
    inventory=json.loads((DOCS/'EVIDENCE_MANIFEST.json').read_text())
    for relative,row in inventory.items():
        path=REPO/relative; data=path.read_bytes()
        if digest(data)!=row['sha256'] or len(data)!=row['bytes']: raise ValueError('Evidence changed after final manifest: '+relative)
        if row['included_in_portable_review']: chosen[relative]=data
    for row in source['sources']:
        path=Path(row['path'])
        key='review_inputs/'+(row['package_path'] if row.get('package_path') else 'workbench/'+path.relative_to(WORKBENCH).as_posix())
        chosen[key]=path.read_bytes()
        if row.get('pinned_commit'):
            relative=path.relative_to(WORKBENCH/'90_SOURCES/reference_7ada2b300fa1').as_posix()
            chosen['review_inputs/pinned_git_blobs/'+relative]=subprocess.check_output(['git','-C',str(REPO),'show',row['pinned_commit']+':'+relative])
    chosen['CHECKPOINT_RECEIPT.json']=strict_bytes(receipt)
    chosen['task.patch']=subprocess.check_output(['git','-C',str(REPO),'diff','--binary',BASE,commit,'--','developmental_ecology','docs/developmental_ecology/p_engineering_20260921'])
    manifest={name:{'bytes':len(data),'sha256':digest(data)} for name,data in sorted(chosen.items())}
    chosen['ARTIFACT_MANIFEST.json']=strict_bytes(manifest)
    target=directory/'Loom_P_build_review_20260922.zip'
    with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED) as z:
        for name,data in sorted(chosen.items()): z.writestr(name,data)
    with zipfile.ZipFile(target) as z:
        for name,row in manifest.items():
            data=z.read(name)
            if digest(data)!=row['sha256'] or len(data)!=row['bytes']: raise ValueError('Review ZIP verification failed')
    (directory/'ARTIFACT_MANIFEST.json').write_bytes(strict_bytes(manifest))
    (directory/'ZIP_SHA256.txt').write_text(digest(target.read_bytes())+'  '+target.name+'\n',encoding='utf-8')
    print(json.dumps(dict(package=str(target),bytes=target.stat().st_size,sha256=digest(target.read_bytes()),commit=commit,branch=branch,archive_tree=tree,files=len(manifest))))

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--package',action='store_true'); args=parser.parse_args()
    package() if args.package else prepare()
