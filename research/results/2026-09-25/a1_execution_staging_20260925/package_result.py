"""Preserve the closed one-attempt evidence; no research modules are imported."""
import datetime,hashlib,json,os,pathlib,shutil,subprocess,zipfile

S=pathlib.Path(__file__).resolve().parent
P=S.parent
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
B=W/'developmental_ecology/artifacts/first-commissioning-A1-20260925-5f077481'
R=P/'exports/2026-09-25-first-commissioning-launch-packet-5f077481'
L=P/'exports/2026-09-25-first-commissioning-launch-delivery-5f077481/FIRST_COMMISSIONING_LAUNCH_PACKET.zip'
V=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
LABEL='2026-09-25-first-A1-commissioning-result-5f077481'
E=P/'exports'/LABEL
I=V/'INBOX'/LABEL
AUTH='a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc'
CHECKPOINT='5f07748102cb5eaa302569c87efbae095050e9fe'
LAUNCH_HASH='371e5ea9c7ab2972a5c1d2eee3914d9a9bb27e7bda13a76bf5a20b5331d61be5'

def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def row(p):return {'bytes':p.stat().st_size,'sha256':sha(p)}
def write(p,obj):
    with p.open('x',encoding='utf-8') as f:json.dump(obj,f,indent=2,ensure_ascii=False,allow_nan=False)
def git(*args):
    env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-C',str(W),*args],env=env).decode().strip()
def main():
    assert not E.exists() and not I.exists(),'Do not overwrite a prior delivery'
    x=json.loads((B/'read-only-review/A1_RESULT_SUMMARY.json').read_bytes())
    execution=json.loads((B/'EXECUTION_RESULT.json').read_bytes())
    assert x['authority_sha256']==AUTH and x['attempts']==1
    report=B/'read-only-review/FIRST_A1_COMMISSIONING_REPORT.md'
    assert report.is_file() and sha(L)==LAUNCH_HASH
    assert git('rev-parse','HEAD')==CHECKPOINT and not git('status','--porcelain')
    ids=json.loads((R/'CODE_AND_RUNTIME_IDENTITIES.json').read_bytes())
    original=ids['original_file_inventory']
    for name,h in original.items():assert sha(pathlib.Path(name))==h,name
    packet=json.loads((R/'FILE_MANIFEST.json').read_bytes())['files']
    for name,expected in packet.items():assert row(R/name)==expected,name
    protected={name:row(V/name) for name in ('AGENTS.md','00_RESEARCH_MAP.md','01_WORKSPACE_STATUS.md','SOURCE_CATALOG.json','SOURCE_REGISTER.md')}
    evidence={p.relative_to(B).as_posix():row(p) for p in sorted(B.rglob('*')) if p.is_file()}
    primary_bytes=sum(r['bytes'] for r in evidence.values())
    component_bytes=sum(r['bytes'] for n,r in evidence.items() if n.startswith('read-only-review/'))
    assert component_bytes<1_000_000_000
    pre=json.loads((B/'read-only-review/V1_V3_PREFLIGHT.json').read_bytes())
    assert pre['preflight_wall_seconds']+x['read_only_analysis_wall_seconds']<3600
    component_upper_bound=pre['preflight_wall_seconds']+(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(execution['finish_utc'])).total_seconds()
    assert component_upper_bound<3600
    # Existing compressed streams dominate this evidence. Reserve three full-size
    # copies conservatively before writing the two review archives.
    assert 3*(primary_bytes+L.stat().st_size+1_000_000)<3_000_000_000
    assert shutil.disk_usage(P).free>2*(primary_bytes+L.stat().st_size+1_000_000)
    E.mkdir(parents=True)
    shutil.copyfile(report,E/report.name)
    preservation={'authority_sha256':AUTH,'apparatus_checkpoint':CHECKPOINT,
        'branch':git('branch','--show-current'),'checkpoint_unchanged':True,'git_status_clean':True,
        'original_runtime_configuration_cache_file_count':len(original),'original_files':original,
        'approved_packet_payload_count':len(packet),'approved_packet_payloads_unchanged':True,
        'approved_launch_zip':row(L),'raw_and_derived_evidence_inventory':evidence,
        'workbench_navigation_before_copy':protected,'primary_evidence_bytes':primary_bytes,
        'component_records_bytes':component_bytes,
        'recorded_preflight_plus_main_analysis_wall_seconds':pre['preflight_wall_seconds']+x['read_only_analysis_wall_seconds'],
        'preflight_plus_all_elapsed_post_execution_wall_seconds_upper_bound':component_upper_bound,
        'replays':0,'research_modules_imported_by_packager':False,
        'scope':'Read-only custody and new local review delivery only; no code, configuration, source, navigation or Git mutation.'}
    write(E/'PRESERVATION_CHECK.json',preservation)
    readme=f'''# First A1 commissioning result

Read `FIRST_A1_COMMISSIONING_REPORT.md`, then `evidence/read-only-review/A1_RESULT_SUMMARY.json`. Exact authority: `{AUTH}`. One attempt at apparatus `{CHECKPOINT}`; unchanged P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.

The attempt stopped as `{x['stop_reason']}` at {x['simulated_seconds']:.12g} simulated seconds; cause `{x['stop_cause']}`. This is one externally controlled physical witness, with no P learning or survival verdict. Any unobserved remainder is untested. No retry, resume or patch was made.

V1, V2 and A0 completed. V3's post-check is incomplete: the execution's read-only checker incorrectly expected the sensor and native stream counts to match, overlooking the recorder's initial display envelope. Its original error and code are preserved, with a separate explanation in `evidence/read-only-review/V3_POST_CHECK_LIMITATION.md`. No corrected checker was run. This is not an all-checks-clear commissioning result.

## Contents

- `evidence/`: exact primary evidence tree, including approval source/envelope, launched manifest, complete trajectory streams and snapshots, progress, outcome and read-only calculations.
- `approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip`: byte-exact approved preparation packet, including canonical authority, procedure, helper, instrument sources, runtime/configuration identities and verified cache. It retains its original proposal labels; the later genuine approval is in the evidence tree.
- `FIRST_A1_COMMISSIONING_REPORT.md`: readable copy of the report also retained under `evidence/read-only-review/`.
- `PRESERVATION_CHECK.json`: exact original-file, packet and evidence inventory; component limits and pre-copy navigation checks.
- `packaging/package_result.py`: custody utility used to prepare this delivery.
- `FILE_MANIFEST.json`: SHA-256 and size of each payload file; the manifest excludes itself. The external delivery receipt records the ZIP identity and verification.

Historical absolute host paths in authority, grants, manifests and snapshots remain unchanged. This archive supplies review evidence; it is not a relocated executable grant. Included execution scripts are provenance and must not be rerun to review the records. No physical replay or portable execution is claimed.

Native records, field/state identities, all event operands, actual issued controller decisions, sensor/diagnostic records and initial/final/native-1000 snapshots are retained. External mode leaves the neural object inactive and wave stream empty. Arithmetic observations and any recorded validation errors are reported separately from P's scientific status.

The new Workbench INBOX delivery is a preserved copy only. Existing research navigation, source archives, canon and Git are unchanged by this packaging step.
'''
    with (E/'README.md').open('x',encoding='utf-8') as f:f.write(readme)
    payload={'FIRST_A1_COMMISSIONING_REPORT.md':E/report.name,'README.md':E/'README.md',
        'PRESERVATION_CHECK.json':E/'PRESERVATION_CHECK.json',
        'approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip':L,
        'packaging/package_result.py':S/'package_result.py'}
    payload.update({'evidence/'+n:B/n for n in evidence})
    files={n:row(p) for n,p in payload.items()}
    manifest={'authority_sha256':AUTH,'apparatus_checkpoint':CHECKPOINT,'files':files,
        'manifest_scope':'Every ZIP payload except FILE_MANIFEST.json itself; no trajectory evolution during packaging.'}
    write(E/'FILE_MANIFEST.json',manifest)
    payload['FILE_MANIFEST.json']=E/'FILE_MANIFEST.json'
    archive=E/'FIRST_A1_COMMISSIONING_RESULT.zip'
    with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as z:
        for name,p in payload.items():z.write(p,name)
    with zipfile.ZipFile(archive) as z:
        assert len(z.namelist())==len(payload) and set(z.namelist())==set(payload)
        assert z.testzip() is None
        for name,p in payload.items():
            with z.open(name) as f:h=hashlib.file_digest(f,'sha256').hexdigest()
            assert h==sha(p) and z.getinfo(name).file_size==p.stat().st_size,name
    finish_delivery(archive,files,evidence,original,packet,protected,primary_bytes)

def finish_delivery(archive,files,evidence,original,packet,protected,primary_bytes):
    # Verify source custody once the archive is closed, before copying it.
    for name,expected in evidence.items():assert row(B/name)==expected,name
    for name,h in original.items():assert sha(pathlib.Path(name))==h,name
    for name,expected in packet.items():assert row(R/name)==expected,name
    assert sha(L)==LAUNCH_HASH
    assert git('rev-parse','HEAD')==CHECKPOINT and not git('status','--porcelain')
    assert {n:row(V/n) for n in protected}==protected,'Concurrent navigation change; do not overwrite'
    I.mkdir(parents=True)
    for name in (archive.name,'FIRST_A1_COMMISSIONING_REPORT.md','README.md','PRESERVATION_CHECK.json','FILE_MANIFEST.json'):
        shutil.copyfile(E/name,I/name)
        assert row(E/name)==row(I/name),name
    protected_after={n:row(V/n) for n in protected}
    assert protected_after==protected
    total_retained=primary_bytes+sum(p.stat().st_size for p in E.iterdir() if p.is_file())+sum(p.stat().st_size for p in I.iterdir() if p.is_file())
    assert total_retained+20000<3_000_000_000
    receipt={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'authority_sha256':AUTH,'apparatus_checkpoint':CHECKPOINT,
        'result_zip':str(archive),'workbench_copy':str(I/archive.name),
        'zip':row(archive),'payload_count_excluding_manifest':len(files),
        'zip_crc_and_every_payload_sha256_verified':True,'workbench_copy_byte_identical':True,
        'source_evidence_unchanged_after_packaging':True,'approved_packet_unchanged':True,
        'original_runtime_configuration_cache_unchanged':True,'checkpoint_unchanged':True,'git_status_clean':True,
        'workbench_navigation_before':protected,'workbench_navigation_after':protected_after,
        'workbench_navigation_unchanged_by_copy':True,'vault_git_writes':0,
        'retained_bytes_before_receipts':total_retained,'primary_and_copies_allowance_bytes':3_000_000_000,
        'extra_world_steps_replays_retries_resumes_patches':0,
        'portable_scope':'Payload integrity verified; no relocated execution or trajectory replay.'}
    write(E/'DELIVERY_RECEIPT.json',receipt)
    shutil.copyfile(E/'DELIVERY_RECEIPT.json',I/'DELIVERY_RECEIPT.json')
    assert row(E/'DELIVERY_RECEIPT.json')==row(I/'DELIVERY_RECEIPT.json')
    print(json.dumps(receipt,indent=2),flush=True)

if __name__=='__main__':main()
