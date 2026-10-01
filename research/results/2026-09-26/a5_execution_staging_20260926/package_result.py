"""Preserve the completed single A5 attempt and derived report in a sealed package."""
import datetime,gzip,hashlib,json,os,pathlib,shutil,subprocess,zipfile
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-clock-correction-20260926';D=W/'developmental_ecology'
BASE=D/'artifacts/commissioning-A5-20260926-68db2c58';REVIEW=BASE/'read-only-review'
EXPORT=ROOT/'exports/2026-09-26-A5-commissioning-result-68db2c58'
PACK=EXPORT/'A5_COMMISSIONING_RESULT';ZIP=EXPORT/'A5_COMMISSIONING_RESULT.zip'
APP='68db2c581f07200966d699a4f55a65f9b96df1e9';AUTH='bdff35693db38800528d91e6d2d4d2085c640268e50713731df5ec27f8b76d1d'
def js(p):return json.loads(p.read_bytes())
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def size(p):return p.stat().st_size if p.is_file() else sum(q.stat().st_size for q in p.rglob('*') if q.is_file()) if p.exists() else 0
def write(p,x):
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def guard(estimate):
    r=js(BASE/'EXECUTION_RESULT.json')
    assert datetime.datetime.now(datetime.timezone.utc)<datetime.datetime.fromisoformat(r['first_stop_utc'])+datetime.timedelta(seconds=3600),'Reporting allowance exhausted'
    roots=map(pathlib.Path,js(REVIEW/'PREFLIGHT.json')['disk_accounting_roots'])
    total=sum(size(p) for p in roots)
    assert total+estimate<=10_000_000_000,'Combined new-artifact ceiling'
    assert shutil.disk_usage(BASE).free>=estimate+1_000_000_000,'Finalization reserve'
    return total
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env)
def verify_folder(root):
    fm=js(root/'FILE_MANIFEST.json')
    assert {p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}==set(fm['files'])|{'FILE_MANIFEST.json'}
    for n,v in fm['files'].items():assert size(root/n)==v['bytes'] and sha(root/n)==v['sha256'],n
    return len(fm['files'])
def verify_zip(path):
    with zipfile.ZipFile(path) as z:
        fm=json.loads(z.read('FILE_MANIFEST.json'));assert len(z.namelist())==len(set(z.namelist()))
        assert set(z.namelist())==set(fm['files'])|{'FILE_MANIFEST.json'}
        for n,v in fm['files'].items():
            raw=z.read(n);assert len(raw)==v['bytes'] and hashlib.sha256(raw).hexdigest()==v['sha256'],n
    return len(fm['files'])

def main():
    assert not EXPORT.exists(),'Preserve existing result delivery; no overwrite'
    r=js(BASE/'EXECUTION_RESULT.json');receipt=js(BASE/'trajectory-001/manifest.json')
    assert r['approved_execution_sha256']==AUTH and r['run_constructors_attempted']==1
    assert r['no_retry_no_resume_no_patch'] and r['physical_replays']==0
    before=js(BASE/'ORIGINAL_FILES_BEFORE.json');after={p:sha(p) for p in before}
    assert before==after,'An original changed'
    assert git('rev-parse','HEAD').decode().strip()==APP and not git('status','--porcelain').strip()
    for name,v in receipt['files'].items():assert sha(BASE/'trajectory-001'/name)==v['sha256'],name
    analysis=js(REVIEW/'ANALYSIS_RESULT.json')
    rawbefore=js(REVIEW/'RAW_EVIDENCE_BEFORE_ANALYSIS.json');assert all(sha(p)==h for p,h in rawbefore.items())
    guard(2_000_000)
    resource=dict(case='A5',authority_sha256=AUTH,simulated_seconds=r['time'],native_steps=r['native_index'],
                  recorder_wall_seconds=receipt.get('wall_seconds'),whole_process_wall_seconds=r['wall_seconds_including_preflight'],
                  uncompressed_stream_bytes=receipt.get('bytes_uncompressed'),stored_trajectory_bytes=size(BASE/'trajectory-001'),
                  recorded_files=len(receipt['files']),record_counts=receipt['records'],
                  runner_wall_cap_seconds=14400,reporting_allowance_seconds=3600,uncompressed_stream_cap_bytes=1500000000,
                  combined_new_artifact_cap_bytes=10000000000,stop_request_bytes=9000000000,flush_reserve_bytes=1000000000,
                  disk_monitor_checks=r['disk_monitor_checks'],peak_combined_disk_during_run=r['peak_combined_new_disk_bytes'],
                  analysis_wall_seconds=analysis['analysis_wall_seconds'],
                  elapsed_since_first_stop_before_packaging_seconds=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(r['first_stop_utc'])).total_seconds(),
                  projected_basis='Unchanged A2/A3 projection: 123.44–125.31 recorder wall minutes; 444.52–474.24 MB stored trajectory.',
                  no_benchmark_rerun=True,no_fidelity_reduction=True)
    # Recorder's schema uses these exact fields; retain the full receipt too.
    if resource['recorder_wall_seconds'] is None:resource['recorder_wall_seconds']=receipt.get('wall_seconds_elapsed')
    if resource['uncompressed_stream_bytes'] is None:resource['uncompressed_stream_bytes']=receipt.get('uncompressed_bytes')
    write(REVIEW/'RESOURCE_RESULT.json',resource)
    preservation=dict(original_files_checked=len(before),all_originals_unchanged=True,raw_evidence_files_checked=len(rawbefore),raw_unchanged_after_reporting=True,
                      clean_apparatus_worktree=True,apparatus_checkpoint=APP,authority_sha256=AUTH,
                      production_code_changed=False,configuration_changed=False,new_prehistory=False,physical_replay=False,
                      Git_writes=False,workbench_canon_or_navigation_changed=False)
    write(REVIEW/'FINAL_PRESERVATION.json',preservation)
    shutil.copyfile(S/'package_result.py',REVIEW/'package_result.py')
    shutil.copyfile(S/'deliver_result.py',REVIEW/'deliver_result.py')
    launch=ROOT/'exports/A5_LAUNCH_PACKET_68db2c58_20260926.zip'
    estimate=size(BASE)+size(launch)+2_000_000
    guard(estimate)
    PACK.mkdir(parents=True,exist_ok=False)
    shutil.copytree(BASE,PACK/'evidence')
    (PACK/'approved-launch').mkdir();shutil.copyfile(launch,PACK/'approved-launch/A5_LAUNCH_PACKET.zip')
    for n in ('A5_PLAIN_LANGUAGE_RESULT.md','A5_FINAL_RESULT_SUMMARY.json','ACTUAL_CONTACT_BOUNDARY_AUDIT.json','A5_RESULT_SUMMARY.json','RESOURCE_RESULT.json','FINAL_PRESERVATION.json','ANALYSIS_RESULT.json','REPORT_DISPOSITION.json','A5_ALL_SOURCE_STOCKS.svg'):
        if (REVIEW/n).exists():shutil.copyfile(REVIEW/n,PACK/n)
    text=f'''# A5 commissioning result — one executed case

Authority: `{AUTH}`  
Apparatus: `{APP}`  
P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`

Read `A5_PLAIN_LANGUAGE_RESULT.md`, `A5_FINAL_RESULT_SUMMARY.json`, `ACTUAL_CONTACT_BOUNDARY_AUDIT.json`, `RESOURCE_RESULT.json` and the full saved-data checks in `evidence/read-only-review/`. The initial support-gap flag in `A5_RESULT_SUMMARY.json` is preserved, but the final interpretation uses the packet's final-actual-contact rule, including a zero-duration departure recontact. The audit documents that reconciliation without changing any original event or production code. The entire original trajectory, restart history, issued commands, sensors, events, diagnostics and receipt are in `evidence/trajectory-001/`, unchanged. Static charts read saved rows only. The authorized launch ZIP and its exact object remain under `approved-launch/`.

This records the one authorized attempt, including any terminal event, missed witness, controller limitation, damage, reserve cost, resource stop or analysis error. No retry, continuation, route/stage substitution, tuning, parameter change, additional case, P/world patch, scientific lifetime, counterfactual run or Git write occurred. This evidence package grants no further execution.

This is a portable evidence package, not a relocated launch environment. Included execution/reporting utilities preserve their original local paths and exact source; no second execution is authorized by their presence.

Every payload is sealed by `FILE_MANIFEST.json`. `evidence/EXECUTION_RESULT.json` records the actual stop and runtime, `evidence/APPROVAL_REQUEST.json` preserves the genuine authorization, and `evidence/LAUNCHED_MANIFEST.json` differs from the proposed object only by its execution grant. Prior A1–A4 and both A5 proposal packets are preserved. Stop for Jason's review.
'''
    (PACK/'README.md').write_text(text,encoding='utf-8')
    files={p.relative_to(PACK).as_posix():dict(bytes=size(p),sha256=sha(p)) for p in sorted(PACK.rglob('*')) if p.is_file()}
    write(PACK/'FILE_MANIFEST.json',dict(authority_sha256=AUTH,apparatus_checkpoint=APP,files=files))
    count=verify_folder(PACK)
    guard(int(size(PACK)*1.02)+2_000_000)
    with zipfile.ZipFile(ZIP,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(PACK.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(PACK).as_posix())
    assert verify_zip(ZIP)==count
    rec=dict(packet=str(PACK),zip=str(ZIP),zip_sha256=sha(ZIP),zip_bytes=size(ZIP),payload_count=count,
             all_payloads_verified=True,authority_sha256=AUTH,apparatus_checkpoint=APP,
             combined_new_bytes_after_packaging=guard(20000),reporting_elapsed_seconds=(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(r['first_stop_utc'])).total_seconds())
    write(EXPORT/'PACKAGE_RECEIPT.json',rec)
    (EXPORT/'A5_COMMISSIONING_RESULT.zip.sha256').write_text(rec['zip_sha256']+'  A5_COMMISSIONING_RESULT.zip\n')
    print(json.dumps(rec,indent=2))

if __name__=='__main__':main()
