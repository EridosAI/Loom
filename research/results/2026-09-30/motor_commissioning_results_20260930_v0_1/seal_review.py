"""Hash-only custody verification and one result archive. No simulation imports."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, subprocess, sys, time, zipfile

OUT = Path(__file__).resolve().parent
ROOT = OUT.parent
PREP = ROOT / 'motor_commissioning_preparation_20260930_v0_1'
EX = PREP / 'execution'
WT = ROOT / 'worktrees/loom-p-b1-minimal-20260929'
D = WT / 'developmental_ecology'
ARCHIVE = ROOT / 'MOTOR_COMMISSIONING_RESULT_20260930_v0_1.zip'

def sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()

def read(path):
    return json.loads(Path(path).read_bytes())

def save(path, data):
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf8')

def verify(base, rows):
    for row in rows:
        p = base / row['path']
        assert sha(p) == row['sha256'], str(p)
        if 'bytes' in row:
            assert p.stat().st_size == row['bytes'], str(p)
    return len(rows)

def git(*args):
    r = subprocess.run(['git', '-c', 'safe.directory=' + WT.as_posix(),
                        '--no-optional-locks', '-C', str(WT), *args],
                       capture_output=True, text=True, check=True)
    if r.stderr:
        git_warnings.append(r.stderr.strip())
    return r.stdout.strip()

started = time.perf_counter()
assert not ARCHIVE.exists(), 'The single result archive already exists; do not overwrite it.'
seal = read(OUT / 'EXECUTION_CUSTODY_SEAL.json')
checks = {'execution_custody_files': verify(EX, seal['files'])}
assert {p.relative_to(EX).as_posix() for p in EX.rglob('*') if p.is_file()} == {r['path'] for r in seal['files']}
for row in seal['files']:
    assert (EX / row['path']).stat().st_mtime_ns == row['mtime_ns'], row['path']
prepared = read(PREP / 'PACKAGE_MANIFEST.json')
checks['unchanged_preparation_files'] = verify(PREP, prepared['files'])
for folder, manifest in [('nursery_0_design_20260930_v0_1', 'DESIGN_ONLY_VERIFICATION.json'),
                         ('nursery_birth_motor_review_20260930_v0_1', 'REVIEW_VERIFICATION.json')]:
    checks[folder] = verify(ROOT / folder, read(ROOT / folder / manifest)['files'])
checks['prior_review_inputs'] = verify(ROOT, read(ROOT / 'nursery_birth_motor_review_20260930_v0_1/INPUT_CUSTODY.json')['files'])
reference = read(PREP / 'REFERENCE_INPUT_HASHES.json')
for path, digest in reference.items():
    assert sha(path) == digest, path
checks['preserved_current_reference_inputs'] = len(reference)

matrix = read(PREP / 'MATRIX.json')['cases']
auth = read(EX / 'JASON_AUTHORIZATION.json')
assert [r['authority_sha256'] for r in matrix] == auth['authorized_authority_sha256']
assert sha(EX / 'JASON_AUTHORIZATION.json') == sha(ROOT / 'motor_commissioning_authorization_20260930.json')
for row in matrix:
    assert sha(PREP / 'authorities' / (row['case_id'] + '.json')) == row['authority_sha256']
results = read(OUT / 'PASSIVE_RESULTS.json')
validation = read(OUT / 'PASSIVE_VALIDATION.json')
assert [r['case_id'] for r in results] == [r['case_id'] for r in matrix]
assert validation['status'] == 'PASS'
assert [r['native_rows'] for r in validation['checks']] == [9000, 9000, 1025]
assert sum(r['waves'] for r in validation['checks']) == 951
assert all(r['status'] == 'NOT_STARTED_BATCH_STOP' for r in results[3:])
assert {p.name for p in (EX / 'lives').iterdir() if p.is_dir()} == {r['case_id'] for r in matrix[:3]}
assert (EX / 'APPARATUS_STOP.json').is_file()

runtime = read(PREP / 'RUNTIME_IDENTITY.json')
source_members = {}
for key, folder in [('P', D / 'loom_p'), ('apparatus', D / 'loom_developmental')]:
    files = runtime[key]['files'] if key == 'P' else runtime[key]
    for name, digest in files.items():
        p = folder / name
        assert sha(p) == digest, str(p)
        source_members['frozen_source/developmental_ecology/' + p.relative_to(D).as_posix()] = p
authority0 = read(PREP / 'authorities/MC-FS-001-CURRENT.json')
for p, digest in [(D / 'configuration.json', authority0['configuration_file_sha256']),
                  (D / 'loom_commissioning/contract.py', authority0['baseline_contract_sha256'])]:
    assert sha(p) == digest, str(p)
    source_members['frozen_source/developmental_ecology/' + p.relative_to(D).as_posix()] = p
git_warnings = []
head = git('rev-parse', 'HEAD')
branch = git('branch', '--show-current')
assert head == '87abae34e19d4e46234402a6b1ba776814956ec1'
assert git('status', '--porcelain') == ''

# Hash runtime files without importing the simulation or its numerical packages.
assert sha(sys.executable) == runtime['executable']
for name, digest in runtime['python_runtime_files'].items():
    assert sha(Path(sys.base_prefix) / name) == digest, name
for name, digest in runtime['runtime_files'].items():
    assert sha(Path(sys.prefix) / 'Lib/site-packages' / name) == digest, name
checks['bound_numerical_runtime_files'] = len(runtime['runtime_files']) + len(runtime['python_runtime_files']) + 1
checks['frozen_source_files'] = len(source_members)
for path in OUT.glob('*.md'):
    assert not any(ord(c) < 32 and c not in '\n\r\t' for c in path.read_text(encoding='utf8')), path

final = dict(
    status='PASS_CUSTODY_AND_PASSIVE_VALIDATION_BATCH_INCOMPLETE', utc=datetime.now(timezone.utc).isoformat(),
    checks=checks, authorized_cases=9, started_once=3, completed_cases=2,
    apparatus_interrupted_cases=1, unstarted_cases=6, verified_native_rows=19025,
    verified_waves=951, rejected_native_step=1026, interrupted_committed_boundary=1025,
    original_denominator_preserved=True, failure_tail_preserved=True,
    exact_authorities_and_order_unchanged=True, prepared_initial_states_unchanged=True,
    prepared_runtime_sha256=sha(PREP / 'RUNTIME_IDENTITY.json'),
    frozen_P='6bc9683b54e4fa80136fe8534d7713e2a250a95f', frozen_checkout=str(WT),
    frozen_checkout_head=head, frozen_checkout_branch=branch, frozen_checkout_clean=True,
    git_read_warnings=sorted(set(git_warnings)), no_git_writes=True,
    production_code_changes=0, parameter_changes=0, new_prehistory=0,
    world_steps_after_apparatus_stop=0, retries=0, continuations=0, replacement_cases=0,
    mechanism_selected=False, CURRENT_remains_reference=True,
    new_authority_objects=0, old_human_B1_evaluator_accessed=False,
    nursery_birth_viability_learning_source_laws_unchanged=True,
    passive_observer_seconds=validation['observer_seconds'],
    final_hash_verification_seconds=time.perf_counter()-started,
    limitations=['No 90-second M2 result', 'No M2 target renewal observed',
                 'No FS-002 or FS-003 execution', 'No full contact-solver root-cause diagnosis',
                 'No automatic motor selection or developmental-efficacy claim'])
save(OUT / 'FINAL_VERIFICATION.json', final)

members = dict(source_members)
for row in prepared['files']:
    members['preparation/' + row['path']] = PREP / row['path']
for name in ('PACKAGE_MANIFEST.json', 'ARCHIVE_VERIFICATION.json'):
    members['preparation/' + name] = PREP / name
for row in seal['files']:
    members['execution/' + row['path']] = EX / row['path']
for p in sorted(OUT.iterdir()):
    if p.is_file() and p.name not in ('PACKAGE_MANIFEST.json', 'ARCHIVE_VERIFICATION.json'):
        members['results/' + p.name] = p
decoder_source = ROOT / 'nursery_0_design_20260930_v0_1/audit_exploration.py'
assert sha(decoder_source) == validation['decoder_source_sha256']
members['references/passive_decoder_source.py'] = decoder_source
manifest = dict(kind='READ_ONLY_REVIEW_PACKAGE_NOT_EXECUTION_AUTHORITY',
                completed=2, interrupted=1, unstarted=6,
                files=[dict(path=name, bytes=p.stat().st_size, sha256=sha(p)) for name,p in sorted(members.items())])
manifest['total_uncompressed_bytes'] = sum(row['bytes'] for row in manifest['files'])
save(OUT / 'PACKAGE_MANIFEST.json', manifest)
with zipfile.ZipFile(ARCHIVE, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as z:
    for name, p in sorted(members.items()):
        z.write(p, name)
    z.write(OUT / 'PACKAGE_MANIFEST.json', 'PACKAGE_MANIFEST.json')
with zipfile.ZipFile(ARCHIVE) as z:
    assert z.testzip() is None
    assert len(z.namelist()) == len(members) + 1
    for row in manifest['files']:
        blob = z.read(row['path'])
        assert len(blob) == row['bytes']
        assert hashlib.sha256(blob).hexdigest() == row['sha256'], row['path']
    assert z.read('PACKAGE_MANIFEST.json') == (OUT / 'PACKAGE_MANIFEST.json').read_bytes()
verify(EX, seal['files'])
archive_result = dict(status='PASS', path=str(ARCHIVE), sha256=sha(ARCHIVE), bytes=ARCHIVE.stat().st_size,
                      verified_members=len(members)+1, package_manifest_sha256=sha(OUT/'PACKAGE_MANIFEST.json'),
                      execution_files_unchanged_after_packaging=True, new_execution_authorized=False,
                      checksum_and_archive_seconds=time.perf_counter()-started)
save(OUT / 'ARCHIVE_VERIFICATION.json', archive_result)
print(json.dumps(dict(final=final, archive=archive_result), indent=2))
