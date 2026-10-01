"""Post-regression identity rehash and sealed-payload exclusion guard; hash-only custody."""
from pathlib import Path
import json,hashlib,os,subprocess,zipfile
W=Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97');O=W/'exports/2026-09-26-b1-review-352f73ff/provenance';Z=O.parent/'portable';T=W/'worktrees/loom-p-b1-apparatus-correction-20260926';OLD=W/'worktrees/loom-p-clock-correction-20260926';H=W/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02';private=H/'B1_PRIVILEGED_EVALUATOR_HOLD'
def read(p):return json.loads(p.read_bytes())
def ident(p):
    with p.open('rb') as f:return {'sha256':hashlib.file_digest(f,'sha256').hexdigest(),'bytes':p.stat().st_size}
def save(n,d):(O/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
before=read(O/'BEFORE_FILE_IDENTITIES.json'); changed={}
for p,v in before.items():
    actual=ident(Path(p))
    if actual!=v:changed[p]={'before':v,'after':actual}
assert not changed
held=read(O/'HELD_PRESERVATION.json')['files'];forbidden={}
for p,v in held.items():
    path=Path(p)
    if (path.is_relative_to(private) and path.relative_to(private).parts[0]!='references') or path==H/'B1_PRIVILEGED_EVALUATOR_HOLD.zip':
        forbidden[v['sha256']]={'basename':path.name,'bytes':v['bytes']}
# Exclude all private authoring/fixture/manifest/snapshot/custody-object payloads,
# not only .gz files. Public original-reference source remains permissible.
manifest=read(Z/'PAYLOAD_MANIFEST.json')['files']
collisions={n:v for n,v in manifest.items() if v['sha256'] in forbidden}
assert not collisions
save('SEALED_PAYLOAD_EXCLUSION_GUARD.json',{'scope':'Exact-byte hashes of original held private payloads except public reference source, plus private archive. Hashes only: no private contents included. Apply these to every candidate final archive entry; no matching payload may be included.','forbidden_file_hashes':forbidden,'forbidden_hash_count':len(forbidden),'portable_payloads_checked':len(manifest),'portable_collisions':collisions,'forbidden_archive_path_components':['B1_PRIVILEGED_EVALUATOR_HOLD','case-manifests','initial-states','authority-objects'],'review_approach':'Case-manifest structural comparison emitted only safe contract fields/booleans; none copied. Snapshots and geometry never deserialized.'})
# Bounded census of delivered manufactured evidence; do not infer global negatives.
records=[]
for n in manifest:
    if n.startswith('evidence/component-records/') and n.endswith('/manifest.json'):
        r=read(Z/n)
        if 'contract' in r:
            c=r['contract'];records.append({'path':n,'purpose':c['purpose'],'case_id':c['case_id'],'duration_seconds':c['duration_seconds']})
assert all(x['purpose']=='manufactured_fixture' for x in records)
save('DELIVERED_RECORD_CENSUS.json',{'manufactured_record_manifests':len(records),'records':records,'commissioning_count':0,'scope':'Only delivered component-record manifests, plus preserved held null-grant metadata. This is not a universal negative about unrecorded external activity.'})
env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0';git={}
for root in [T,OLD]:
    command=['git','-c','safe.directory='+root.as_posix(),'-c','core.excludesFile='+(O/'empty-excludes').as_posix(),'-C',str(root)]
    git[str(root)]={'HEAD':subprocess.check_output(command+['rev-parse','HEAD'],cwd=root,env=env).decode().strip(),'status':subprocess.check_output(command+['status','--porcelain'],cwd=root,env=env).decode()}
assert all(not x['status'] for x in git.values())
archives={}
for folder in ['2026-09-26-B1-operator-correction-352f73ff','2026-09-26-B1-operator-correction-352f73ff-review-02']:
    path=W/'exports'/folder/'B1_OPERATOR_APPARATUS_CORRECTION_REVIEW.zip';r=read(path.parent/'ARCHIVE_RECEIPT.json');value=ident(path)
    assert value['sha256']==r['archive_sha256'] and value['bytes']==r['archive_bytes'];archives[folder]=value
save('FINAL_PRESERVATION.json',{'source_and_evidence_files_rehashed':len(before),'changed':changed,'all_unchanged':True,'held_files':len(held),'original_omitted_A5_files':115,'current_and_parent_git':git,'original_archives':archives,'forbidden_held_payload_hashes':len(forbidden),'portable_sealed_payload_collisions':0,'no_held_snapshots_decoded':True,'no_authority_objects_generated':True,'no_simulation_or_controller_calls_by_subreview':True})
print(json.dumps({'files_rehashed':len(before),'changed':len(changed),'held_preserved':len(held),'sealed_payload_hashes_excluded':len(forbidden),'manufactured_record_manifests':len(records),'git_clean':True},indent=2))
