"""Package only this independent export; audited target and input files are read-only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import subprocess
import zipfile

OUT = Path(__file__).resolve().parent
REPO = Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405')
OLD = 'd5f7efbe67193f215e52d95ca912db131a79f31c'
NEW = 'f7eb6f27c661e3db193a4225b56a825d7e41739d'
PACKAGE = REPO / 'developmental_ecology/artifacts/review-package-correction-20260923-01a0c405'
DELIVERY = PACKAGE / 'Loom_P_corrective_review_20260923.zip'
ZIPNAME = 'Loom_P_Independent_Post_Correction_Review_f7eb6f27_20260923.zip'

def sha(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()

def write_new(path, data):
    with path.open('xb') as handle:
        handle.write(data)

def write_json(path, obj):
    write_new(path, (json.dumps(obj, indent=2, ensure_ascii=False)+'\n').encode('utf-8'))

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), '-c', 'core.fsmonitor=false', *args],
        env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'), stderr=subprocess.PIPE).decode().strip()

assert git('rev-parse', 'HEAD') == NEW
assert git('rev-parse', 'HEAD^') == OLD
assert git('status', '--porcelain=v1') == ''
assert sha(DELIVERY) == '7e33da1b05646c5af352a4114e99082c52b51b2b5966911f30816fb2911091da'
inputs = OUT/'review_inputs'
inputs.mkdir(exist_ok=False)
prior = OUT.parent/'2026-09-23-p-independent-fidelity-review-d5f7efbe/LOOM_P_INDEPENDENT_FIDELITY_REVIEW.md'
for source, name in (
    (prior, prior.name),
    (Path(r'C:\Users\Jason\.codex\attachments\e32a1bb4-0bd6-4e64-80b6-fd1e2cd92869\Pasted text.txt'), 'POST_CORRECTION_REVIEW_REQUEST.txt'),
    (PACKAGE/'assembled/CORRECTION.patch', 'CORRECTION.patch'),
):
    write_new(inputs/name, source.read_bytes())

report = OUT/'LOOM_P_INDEPENDENT_POST_CORRECTION_FIDELITY_REVIEW.md'
physics_names = ['release_disabled','double_source_debit','damage_suppressed','native_repeated']
for name in physics_names:
    red = (OUT/'physics'/f'{name}-RED.txt').read_text(encoding='utf-8-sig')
    green = (OUT/'physics'/f'{name}-GREEN.txt').read_text(encoding='utf-8-sig')
    assert '1 failed' in red and '1 passed' in green
neural = json.loads((OUT/'neural/mutants-attempt-002/SUMMARY.json').read_text())
assert len(neural) == 16 and all(r['RED']['confirmed'] and r['GREEN']['confirmed'] for r in neural)
r2 = json.loads((OUT/'r2/SUMMARY.json').read_text())
assert len(r2) == 7 and all(r['consequential'] for r in r2)
recon = json.loads((OUT/'provenance/RECONSTRUCTION.json').read_text())
assert sum(r['native'] for r in recon) == 3200
assert all(r['reconstruction']['identical'] and r['field_reconstruction_bit_identical'] for r in recon)
receipt = dict(
    created_at_utc=datetime.now(timezone.utc).isoformat(),
    verdict='HOLD BEFORE COUPLING COMMISSIONING', previous_checkpoint=OLD, reviewed_checkpoint=NEW,
    branch=git('branch', '--show-current'), worktree=str(REPO), final_worktree_clean=True,
    report=report.name, report_sha256=sha(report),
    classifications=dict(R1='MUST-FIX BEFORE COMMISSIONING', R2='VERIFIED', R3='VERIFIED'),
    original_r1_counterexample_corrected=True, remaining_r1='Resolvable oblique release/free-flight/return retained as full-duration sustained contact',
    suite=dict(worktree_passed=55, portable_assembled_passed=55),
    observed_delivered_mutant_pairs=14, additional_consequential_mutant_pairs=8, total_consequential_pairs=22,
    corrected_saved_neural_states_exact=3200, corrected_final_fields_exact=3,
    midwave_saved_neural_states_exact=93, observer_reconstruction_records=40,
    semantic_configuration_sha256='a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a',
    runtime_code_sha256='af53b321220001166b73bc420b67c7526cddfe4198b8bf34ef69f7406082d868',
    reviewed_delivery=dict(name=DELIVERY.name, bytes=DELIVERY.stat().st_size, sha256=sha(DELIVERY)),
    correction_patch_sha256=sha(inputs/'CORRECTION.patch'), previous_independent_report_sha256=sha(prior),
    preserved_prior_artifact_files=252, prior_build_manifest_entries_verified=87,
    target_artifact_files_unchanged_during_audit=474,
    field_prehistory_sha256='7804edb2257a3a2cd016944776e60c265a5815db838f506ae6fa5a9f14dc4096',
    archive_tree=git('rev-parse', 'HEAD:EXP1-21'),
    review_created_lifetimes=0, review_prehistory_generations=0, review_target_writes=0,
    remote_or_workbench_operations_by_review=False,
    builder_historical_no_push_pr_vault_write_claim='Not independently provable from supplied final local artifacts; no contrary evidence found',
)
write_json(OUT/'REVIEW_RECEIPT.json', receipt)

selected = {}
for path in OUT.rglob('*'):
    if not path.is_file(): continue
    relative = path.relative_to(OUT)
    directories = relative.parts[:-1]
    if any(part.startswith(('suite-temp-', 'portable-suite-temp-', 'isolated-temp', 'tmp-')) or part in ('ambient_poisoned','__pycache__','.pytest_cache') for part in directories): continue
    if path.name in (ZIPNAME,'ZIP_SHA256.txt','FILE_MANIFEST.json','PACKAGE_VERIFICATION.json'): continue
    if path.suffix.lower() not in ('.py','.md','.json','.txt','.patch'): continue
    selected[relative.as_posix()] = path
selected['reviewed_delivery/'+DELIVERY.name] = DELIVERY
assert sum(name.startswith('neural/mutants-attempt-002/') and name.endswith('.txt') for name in selected) == 32
manifest = {name:dict(bytes=path.stat().st_size, sha256=sha(path)) for name,path in sorted(selected.items())}
write_json(OUT/'FILE_MANIFEST.json', manifest)
selected['FILE_MANIFEST.json'] = OUT/'FILE_MANIFEST.json'
target = OUT/ZIPNAME
with zipfile.ZipFile(target, 'x', zipfile.ZIP_DEFLATED) as archive:
    for name,path in sorted(selected.items()):
        archive.write(path, name, compress_type=zipfile.ZIP_STORED if name.startswith('reviewed_delivery/') else zipfile.ZIP_DEFLATED)
with zipfile.ZipFile(target) as archive:
    assert len(archive.namelist()) == len(set(archive.namelist())) == len(selected)
    assert archive.testzip() is None
    for name,identity in manifest.items():
        data = archive.read(name)
        assert len(data) == identity['bytes'] and hashlib.sha256(data).hexdigest() == identity['sha256'], name
write_new(OUT/'ZIP_SHA256.txt', (sha(target)+'  '+target.name+'\n').encode('ascii'))
result = dict(zip=str(target), bytes=target.stat().st_size, sha256=sha(target), members=len(selected), all_member_hashes_verified=True)
write_json(OUT/'PACKAGE_VERIFICATION.json', result)
print(json.dumps(result, indent=2))
