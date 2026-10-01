"""Package this completed independent review; all target inputs remain read-only.
Run from the reviewed repository with its pinned Python and -B.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import zipfile

OUT=Path(__file__).resolve().parent
REPO=Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405')
OLD='f7eb6f27c661e3db193a4225b56a825d7e41739d'
NEW='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
PACKAGE=REPO/'developmental_ecology/artifacts/review-package-r1p-20260923-01a0c405'
DELIVERY=PACKAGE/'Loom_P_R1P_corrective_review_20260923.zip'
ZIPNAME='Loom_P_Final_Independent_R1P_Review_6bc9683b_20260923.zip'

def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def write_new(p,b):
    with p.open('xb') as f: f.write(b)
def write_json(p,obj): write_new(p,(json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode('utf-8'))
def git(*args):
    return subprocess.check_output(['git','-c','safe.directory='+REPO.as_posix(),'-C',str(REPO),'-c','core.fsmonitor=false',*args],
        env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),stderr=subprocess.PIPE).decode().strip()

assert git('rev-parse','HEAD')==NEW
assert git('rev-parse','HEAD^')==OLD
assert git('status','--porcelain=v1')==''
assert sha(DELIVERY)=='c1f2cd0ed8ebe09f3a9b07d087f6fe9f25ca62f3f61a827628802bc35e5fa322'
inputs=OUT/'review_inputs'; inputs.mkdir(exist_ok=False)
previous=OUT.parent/'2026-09-23-p-post-correction-review-f7eb6f27/LOOM_P_INDEPENDENT_POST_CORRECTION_FIDELITY_REVIEW.md'
original=OUT.parent/'2026-09-23-p-independent-fidelity-review-d5f7efbe/LOOM_P_INDEPENDENT_FIDELITY_REVIEW.md'
request=Path(r'C:\Users\Jason\.codex\attachments\8cdf6ccf-605d-4042-a61d-3c9ee06e3aee\Pasted text.txt')
for source,name in ((previous,previous.name),(original,original.name),(request,'FINAL_REVIEW_REQUEST.txt'),(PACKAGE/'assembled/CORRECTION.patch','CORRECTION.patch')):
    write_new(inputs/name,source.read_bytes())

ids=read(OUT/'provenance/IDENTITIES.json')
provenance=read(OUT/'provenance/PACKAGE.json')
recon=read(OUT/'provenance/RECONSTRUCTION.json')
mutants=read(OUT/'falsifiers/pairs-attempt-002/SUMMARY.json')
assert len(mutants)==18 and all(r['RED']['confirmed'] and r['GREEN']['confirmed'] for r in mutants)
assert sum(r['native'] for r in recon)==3200 and all(r['reconstruction']['identical'] and r['field_reconstruction_bit_identical'] for r in recon)
physics=read(OUT/'physics/independent-r1p-evidence.json')
assert len(physics['cases'])==4
report=OUT/'LOOM_P_FINAL_INDEPENDENT_R1P_FIDELITY_REVIEW.md'
receipt=dict(created_at_utc=datetime.now(timezone.utc).isoformat(),verdict='FIT TO PROCEED TO COUPLING COMMISSIONING',
    reviewed_checkpoint=NEW,previous_checkpoint=OLD,original_checkpoint='d5f7efbe67193f215e52d95ca912db131a79f31c',
    branch=git('branch','--show-current'),worktree=str(REPO),final_worktree_clean=True,
    report=report.name,report_sha256=sha(report),R1P='VERIFIED',R2='VERIFIED',R3='VERIFIED',
    must_fix_findings=0,unexpected_law_bearing_changes=0,
    component_cases=4,exact_oblique_free_duration=.00099450757408153,exact_oblique_first_collision_passes=15,
    new_fault_pairs=4,retained_fault_pairs=14,independently_observed_pairs=18,
    final_suite=dict(worktree_passed=59,portable_passed=59),neural_states_exact=3200,final_fields_exact=3,
    detached_midwave_records_exact=93,observer_reconstructed_records=40,
    preserved_prior_artifacts=489,target_artifacts_unchanged_during_audit=792,
    semantic_configuration_sha256=ids['semantic_configuration'],runtime_code_sha256=ids['runtime_code']['sha256'],
    reviewed_delivery=dict(name=DELIVERY.name,bytes=DELIVERY.stat().st_size,sha256=sha(DELIVERY)),
    correction_patch_sha256=sha(inputs/'CORRECTION.patch'),archive_tree=git('rev-parse','HEAD:EXP1-21'),
    source_inventory_unchanged=14,source_inventory_total=16,administrative_source_changes=ids['administrative_source_changes'],
    selected_scientific_sources_unchanged=True,
    previous_independent_review_sha256=sha(previous),original_independent_review_sha256=sha(original),
    prehistory_reused=True,review_prehistory_generations=0,review_lifetimes=0,review_target_writes=0,
    commissioning_designed_or_started=False,workbench_intake_performed=False,
    disposition_boundary='Separate Jason-authorized commissioning-design task; no scientific efficacy claim or arbitrary-contact-space proof')
write_json(OUT/'REVIEW_RECEIPT.json',receipt)

selected={}
for p in OUT.rglob('*'):
    if not p.is_file(): continue
    relative=p.relative_to(OUT)
    if any(part.startswith(('worktree-temp-','portable-temp-','isolated-temp','tmp-')) or part in ('__pycache__','.pytest_cache') for part in relative.parts[:-1]): continue
    if p.name in (ZIPNAME,'ZIP_SHA256.txt','FILE_MANIFEST.json','PACKAGE_VERIFICATION.json'): continue
    if p.suffix.lower() not in ('.md','.py','.json','.txt','.patch'): continue
    selected[relative.as_posix()]=p
selected['reviewed_delivery/'+DELIVERY.name]=DELIVERY
assert sum(n.startswith('falsifiers/pairs-attempt-002/') and n.endswith('.txt') for n in selected)==36
assert 'physics/failure-semantics.json' in selected and 'EVENT_CLOCK_SEPARATION.json' in selected
manifest={n:dict(bytes=p.stat().st_size,sha256=sha(p)) for n,p in sorted(selected.items())}
write_json(OUT/'FILE_MANIFEST.json',manifest)
selected['FILE_MANIFEST.json']=OUT/'FILE_MANIFEST.json'
target=OUT/ZIPNAME
with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED) as z:
    for n,p in sorted(selected.items()):
        z.write(p,n,compress_type=zipfile.ZIP_STORED if n.startswith('reviewed_delivery/') else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(target) as z:
    assert len(z.namelist())==len(set(z.namelist()))==len(selected)
    assert z.testzip() is None
    for n,r in manifest.items():
        b=z.read(n); assert len(b)==r['bytes'] and hashlib.sha256(b).hexdigest()==r['sha256'],n
write_new(OUT/'ZIP_SHA256.txt',(sha(target)+'  '+target.name+'\n').encode('ascii'))
result=dict(zip=str(target),bytes=target.stat().st_size,sha256=sha(target),members=len(selected),all_hashes_verified=True,completed_fault_logs_included=36)
write_json(OUT/'PACKAGE_VERIFICATION.json',result)
print(json.dumps(result,indent=2))
