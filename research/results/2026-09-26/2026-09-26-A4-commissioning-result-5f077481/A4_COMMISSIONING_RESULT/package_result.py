"""Package stopped A4 records and saved-data reports. No Loom import or execution."""
import hashlib,json,pathlib,shutil,time,zipfile
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
B=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\commissioning-A4-20260926-5f077481')
OUT=ROOT/'exports/2026-09-26-A4-commissioning-result-5f077481'
AUTH='47a71e78ad4bbb920f2b29f7d9b0e3c5f520eb4905880916c85f0cc8bbb9f1e0'
def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(p,v):
    with p.open('x',encoding='utf-8') as f:f.write(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def main():
    started=time.perf_counter();review=B/'read-only-review'
    assert (B/'BATCH_EXECUTION_RESULT.json').is_file() and (review/'ANALYSIS_RESULT.json').is_file() and (review/'A4_COMMISSIONING_REPORT.md').is_file()
    analysis=json.loads((review/'ANALYSIS_RESULT.json').read_bytes());prior=analysis['analysis_wall_seconds_including_reports'];assert prior<600
    assert not OUT.exists(),'No overwrite or replacement result'
    OUT.mkdir(parents=True);payload=OUT/'A4_COMMISSIONING_RESULT';payload.mkdir()
    before={str(p):sha(p) for p in B.rglob('*') if p.is_file()}
    shutil.copytree(B,payload/'evidence');(payload/'approved-launch').mkdir()
    launch=ROOT/'exports/2026-09-26-A4-launch-delivery-5f077481/A4_LAUNCH_PACKET.zip'
    assert sha(launch)=='84b351f3b8721351575a52c915733fbb9ad499e25f04b5fa6617c0744fa70b0e'
    shutil.copyfile(launch,payload/'approved-launch/A4_LAUNCH_PACKET.zip');shutil.copyfile(__file__,payload/'package_result.py')
    result=json.loads((B/'BATCH_EXECUTION_RESULT.json').read_bytes());summary=json.loads((review/'A4_RESULT_SUMMARY.json').read_bytes())
    resources=json.loads((review/'RESOURCE_RESULT.json').read_bytes());resources['analysis_wall_seconds_including_reports']=prior
    resources['scope']='Actual full-fidelity records only; no throughput rerun.';write(payload/'RESOURCE_RESULT.json',resources)
    outcomes='All three prescribed bounded physical witnesses were observed.' if analysis['all_three_physical_witnesses_observed'] else 'See the report for separately preserved observed, missed, incomplete or unattempted components.'
    table=[]
    for cid in result['case_order']:
        o=summary['cases'].get(cid,{})
        if 'whole_case' in o:
            w=o['whole_case'];t=o['milestones']['arrival_radius_0_25']['time'];table.append(f"| {cid} | {w['simulated_seconds']:.9f} | {t if t is not None else 'not observed'} | {w['final_EI'][0]:.9f} / {w['final_EI'][1]:.9f} | {o['contacts']['mover_contact_event_count']} |")
        else:table.append(f'| {cid} | incomplete/unattempted | — | — | — |')
    readme=f"""# Loom P — three-case A4 commissioning evidence

{outcomes} Start with [the plain-language result](evidence/read-only-review/A4_PLAIN_LANGUAGE_RESULT.md), then [the technical report](evidence/read-only-review/A4_COMMISSIONING_REPORT.md).

| Case | Recorded seconds | Arrival sample (s) | Final E / I | Mover contact events |
|---|---:|---:|---|---:|
"""+'\n'.join(table)+f"""

Executed canonical batch: `{AUTH}`. The genuine user approval, exact parent/constituent authority objects, individual launched manifests, initial snapshots, raw trajectories, restart states, attempt markers and resource/stop records are preserved under `evidence/`. The unchanged approved launch ZIP is under `approved-launch/`; its original proposed/unauthorized wording is preserved as pre-approval history, with actual execution authority recorded separately. It contains the exact code, configuration, runtime/cache identities and nested A0–A3 evidence.

P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`; apparatus remains `5f07748102cb5eaa302569c87efbae095050e9fe`. Run attempts: {result['run_constructors_attempted']}; unattempted cases: `{result['unattempted_cases']}`. No retry, resume, route/phase substitution, tuning, patch, extra case or Git write. Analysis only reads saved records and calculates geometry/accounting; it does not recompute control or replay physics.

The waiting counterfactual was not executed: immediate-proceed conflict is the approved analytic argument. DETOUR uses its own already-declared A0 endpoints, not an equal-endpoint efficiency comparison. Sampled clearances and native path lengths are not certified continuous-time extrema. No P learning/perception, prediction, all-phase safety, efficacy, scientific lifetime or broad survival claim.

Full native, sensor, contact/accounting, paired command, actual sampled mover geometry and restart data remain available for passive replay. No live renderer, server or new viewer was added. Do not execute archived helpers, resume snapshots or infer another grant from this archive. Absolute paths are historical provenance, not portable launch instructions.

`FILE_MANIFEST.json` hashes every payload except itself. The external delivery receipt hashes the ZIP. All validation errors or incomplete observations are retained rather than patched or rerun.
"""
    (payload/'README.md').write_text(readme,encoding='utf-8')
    after={p:sha(p) for p in before};assert before==after
    write(payload/'PRESERVATION_CHECK.json',{'source_files_checked':len(before),'source_inventory':before,'all_original_evidence_unchanged':True,'authority_sha256':AUTH,'new_simulation_steps':0,'Git_writes':0})
    assert prior+time.perf_counter()-started<600
    files={p.relative_to(payload).as_posix():{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(payload.rglob('*')) if p.is_file()}
    write(payload/'FILE_MANIFEST.json',{'authority_sha256':AUTH,'files':files})
    zpath=OUT/'A4_COMMISSIONING_RESULT.zip'
    with zipfile.ZipFile(zpath,'x',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(payload.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(payload).as_posix())
    with zipfile.ZipFile(zpath) as z:
        assert set(z.namelist())==set(files)|{'FILE_MANIFEST.json'}
        for n,v in files.items():
            data=z.read(n);assert len(data)==v['bytes'] and hashlib.sha256(data).hexdigest()==v['sha256'],n
    elapsed=time.perf_counter()-started;assert prior+elapsed<600
    used=sum(p.stat().st_size for p in OUT.rglob('*') if p.is_file())+sum(p.stat().st_size for p in B.rglob('*') if p.is_file());assert used<3000000000
    receipt={'zip':str(zpath),'sha256':sha(zpath),'bytes':zpath.stat().st_size,'verified_payloads':len(files),'authority_sha256':AUTH,'all_three_physical_witnesses_observed':analysis['all_three_physical_witnesses_observed'],'total_native_steps':resources['total_native_steps'],'total_simulated_seconds':resources['total_simulated_seconds'],'all_original_evidence_unchanged':True,'analysis_and_packaging_wall_seconds':prior+elapsed,'reporting_cap_seconds':600,'current_primary_and_project_delivery_bytes':used,'combined_disk_cap_bytes':3000000000}
    write(OUT/'DELIVERY_RECEIPT.json',receipt);print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
