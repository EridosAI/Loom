"""Preserve stopped A3 evidence and read-only report in a portable review ZIP."""
import hashlib,json,pathlib,shutil,zipfile
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
B=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\commissioning-A3-20260925-5f077481')
OUT=ROOT/'exports/2026-09-26-A3-commissioning-result-5f077481'
AUTH='43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd'
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def main():
    assert (B/'EXECUTION_RESULT.json').is_file() and (B/'read-only-review/A3_COMMISSIONING_REPORT.md').is_file()
    assert not OUT.exists(),'No overwrite of existing result package'
    OUT.mkdir(parents=True);payload=OUT/'A3_COMMISSIONING_RESULT';payload.mkdir()
    before={str(p):sha(p) for p in B.rglob('*') if p.is_file()}
    shutil.copytree(B,payload/'evidence');(payload/'approved-launch').mkdir()
    launch=ROOT/'exports/2026-09-25-A3-launch-delivery-5f077481/A3_LAUNCH_PACKET.zip'
    assert sha(launch)=='4c580299d098ad26eb5c6be4dd98e4e26e1fb8e4c766fa8591d516fdb6fdcfce'
    shutil.copyfile(launch,payload/'approved-launch/A3_LAUNCH_PACKET.zip')
    shutil.copyfile(S/'package_result.py',payload/'package_result.py')
    result=json.loads((B/'EXECUTION_RESULT.json').read_bytes());receipt=json.loads((B/'trajectory-001/manifest.json').read_bytes())
    readme=f'''# Loom P — single A3 commissioning evidence

Start with [the plain-language result](evidence/read-only-review/A3_PLAIN_LANGUAGE_RESULT.md), [the contact-interruption note](evidence/read-only-review/CONTACT_INTERRUPTION_NOTE.md), then [the full technical report](evidence/read-only-review/A3_COMMISSIONING_REPORT.md). The complete ordered physical chain was observed. Source-3 support was nevertheless divided into 629 intervals with small gaps and repeated recontact damage; this is preserved separately from energy transfer and is not a full-healing or P-efficacy claim.

Executed authority: `{AUTH}`. One attempt stopped at {result['time']:.12g} simulated seconds, native index {result['native_index']}, status `{receipt['status']}`, cause `{receipt.get('stop_cause')}`, complete `{receipt['complete']}`. No retry, continuation, additional case or patch.

The exact user authorization, approved object, launched manifest, initial snapshot, raw trajectory, restart states, progress, runtime/source preservation checks and new read-only analysis are in `evidence/`. The complete untouched approved launch ZIP is in `approved-launch/`; it retains exact instrument/configuration/cache identities and historical A1/A2/V3 source evidence. The launch packet's proposed/unauthorized wording remains its original pre-approval history; the genuine A3 approval and separate launched grant are preserved in the new evidence.

`FILE_MANIFEST.json` records every payload's size and SHA-256 except itself. The delivery receipt outside the ZIP hashes the sealed archive. Verify these before relying on a moved copy. Absolute execution/approval paths are historical provenance, not portable execution instructions.

No live viewer or new passive viewer was created. Native body, all stocks, E/I, commands, forces, contacts, accounting and recorded mover data remain available for a separately requested passive viewer extension. Do not run archived scripts, resume the final restart or infer another execution grant from this package.

P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; apparatus remains `5f07748102cb5eaa302569c87efbae095050e9fe`. This physical witness does not test P learning or developmental efficacy.
'''
    (payload/'README.md').write_text(readme,encoding='utf-8')
    write(payload/'RESOURCE_RESULT.json',{'simulated_seconds_recorded':result['time'],'native_steps':result['native_index'],
        'recorder_wall_seconds':receipt['wall_seconds'],'whole_process_wall_seconds':result['wall_seconds_including_preflight'],
        'wall_ceiling_seconds':4200,'uncompressed_stream_bytes':receipt['uncompressed_bytes'],'uncompressed_stream_ceiling_bytes':1500000000,
        'stored_trajectory_bytes_including_snapshots_and_receipt':sum(p.stat().st_size for p in (B/'trajectory-001').iterdir() if p.is_file()),
        'analysis_wall_seconds':json.loads((B/'read-only-review/ANALYSIS_RESULT.json').read_bytes())['analysis_wall_seconds'],
        'read_only_reporting_ceiling_seconds':3600,'disk_reserve_bytes':3000000000})
    after={p:sha(p) for p in before};assert before==after
    write(payload/'PRESERVATION_CHECK.json',{'raw_and_analysis_source_files':len(before),'all_unchanged_during_packaging':True,'source_inventory':before,'authority_sha256':AUTH,'new_simulation_steps':0,'Git_writes':0})
    files={p.relative_to(payload).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(payload.rglob('*')) if p.is_file()}
    write(payload/'FILE_MANIFEST.json',{'authority_sha256':AUTH,'files':files})
    zpath=OUT/'A3_COMMISSIONING_RESULT.zip'
    with zipfile.ZipFile(zpath,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(payload.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(payload).as_posix())
    with zipfile.ZipFile(zpath) as z:
        assert set(z.namelist())==set(files)|{'FILE_MANIFEST.json'}
        for n,v in files.items():
            b=z.read(n);assert len(b)==v['bytes'] and hashlib.sha256(b).hexdigest()==v['sha256'],n
    total=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())+sum(p.stat().st_size for p in B.rglob('*') if p.is_file())
    delivery={'zip':str(zpath),'sha256':sha(zpath),'bytes':zpath.stat().st_size,'verified_payloads':len(files),'authority_sha256':AUTH,
              'stop_label':receipt['status'],'stop_cause':receipt.get('stop_cause'),'simulated_seconds':result['time'],'native_index':result['native_index'],
              'original_evidence_preserved':before==after,'current_primary_and_project_delivery_bytes':total,'reserved_disk_bytes':3000000000}
    assert total<3000000000
    write(OUT/'DELIVERY_RECEIPT.json',delivery);print(json.dumps(delivery,indent=2))
if __name__=='__main__':main()
