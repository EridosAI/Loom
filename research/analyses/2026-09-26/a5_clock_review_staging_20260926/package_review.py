"""Copy/hash diagnosis references and package new review documents only.

No Loom imports, launchers, code modifications, Git writes or simulation calls.
"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'exports/2026-09-26-A5-clock-compatibility-review-5f077481'
WT = Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
D = WT / 'developmental_ecology'
HELD = ROOT / 'exports/2026-09-26-A5-launch-packet-HOLD-5f077481'
WB = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
DELIVERED_HELD = WB / 'INBOX/2026-09-26-A5-launch-packet-HOLD-5f077481/A5_LAUNCH_PACKET_HOLD'
APP = '5f07748102cb5eaa302569c87efbae095050e9fe'
AUTH = '88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6'

def identity(p):
    with p.open('rb') as f:
        h = hashlib.file_digest(f, 'sha256').hexdigest()
    return {'sha256': h, 'bytes': p.stat().st_size}

def write(name, data):
    p = OUT / name
    assert not p.exists(), p
    p.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')

def git(*args):
    env = os.environ.copy()
    env['GIT_OPTIONAL_LOCKS'] = '0'
    return subprocess.check_output([
        'git', '-c', 'safe.directory=' + WT.as_posix(), '-c',
        'core.excludesFile=' + (ROOT/'a5_packet_staging_20260926/empty-excludes').as_posix(),
        '-C', str(WT), *args], env=env).decode().strip()

before = json.loads((OUT / 'SOURCE_IDENTITIES_BEFORE.json').read_bytes())
after = json.loads((OUT / 'SOURCE_IDENTITIES_AFTER.json').read_bytes())
assert before == after
assert all(identity(Path(p)) == v for p, v in before.items())
assert git('rev-parse', 'HEAD') == APP
assert not git('status', '--porcelain')
assert not (D / 'artifacts/commissioning-A5-20260926-5f077481').exists()
assert identity(HELD/'AUTHORITY_OBJECT.canonical.json')['sha256'] == AUTH
assert identity(DELIVERED_HELD/'AUTHORITY_OBJECT.canonical.json')['sha256'] == AUTH
held_files = json.loads((HELD/'FILE_MANIFEST.json').read_bytes())['files']
assert all(identity(DELIVERED_HELD/n) == v for n, v in held_files.items())

references = {}
def ref(source, relative):
    source = Path(source)
    dest = OUT/'references'/relative
    expected = before[str(source)]
    assert identity(source) == expected
    dest.parent.mkdir(parents=True, exist_ok=True)
    if not dest.exists():
        shutil.copyfile(source, dest)
    assert identity(dest) == expected
    references[dest.relative_to(OUT).as_posix()] = {'original_path':str(source), **expected}

for module in ('loom_commissioning', 'loom_p'):
    for src in sorted((D/module).glob('*.py')):
        ref(src, Path('instrument')/module/src.name)
for name in ('configuration.json', 'requirements-lock.txt'):
    ref(D/name, Path('instrument')/name)
for name in ('test_apparatus.py', 'test_corrections.py', 'test_final_corrections.py'):
    ref(D/'tests_apparatus'/name, Path('tests')/name)
ref(D/'tests_apparatus/fixtures/review-boundary-input.json', 'tests/fixtures/review-boundary-input.json')
for name in ('README.md', 'OPEN_ISSUE_A5_CLOCK.md', 'CLOCK_AUDIT.json', 'A5_MANIFEST.json', 'CODE_AND_RUNTIME_IDENTITIES.json'):
    ref(HELD/name, Path('held_A5_reference')/name)
prior_review_sources = [
    WT/'docs/developmental_ecology/p_apparatus_correction_20260924/CORRECTION_REPORT.md',
    WT/'docs/developmental_ecology/p_apparatus_final_correction_20260925/FINAL_CORRECTION_REPORT.md',
    ROOT/'exports/2026-09-24-p-apparatus-review-05abf604/physical/RUNNER_AUTHORITY_CONTROLLER_REVIEW.md',
    ROOT/'exports/2026-09-25-p-apparatus-correction-review-9d31e790/physical/INDEPENDENT_CLOCK_REVIEW.md',
    ROOT/'exports/2026-09-25-p-apparatus-correction-review-9d31e790/LOOM_P_FINAL_APPARATUS_CORRECTION_REVIEW.md',
    ROOT/'exports/2026-09-25-p-final-mechanical-closure-5f077481/LOOM_P_FINAL_MECHANICAL_CLOSURE_REVIEW.md']
for src in prior_review_sources:
    ref(src, Path('prior_reviews')/src.name)
write('REFERENCE_MANIFEST.json', {'purpose':'Byte-identical diagnosis references; not a new instrument or launch packet.', 'files':references})

assert all(identity(Path(p)) == v for p, v in before.items())
write('FINAL_VERIFICATION.json', {
    'scope':'Read-only source/evidence verification plus new diagnosis documents only.',
    'preserved_original_files':len(before), 'original_files_unchanged':True,
    'reference_copies_verified':len(references), 'worktree':str(WT),
    'HEAD':git('rev-parse','HEAD'), 'branch':git('branch','--show-current'),
    'git_porcelain':git('status','--porcelain'), 'Git_writes':0,
    'held_A5_sha256':AUTH, 'held_project_packet_unchanged':True,
    'held_workbench_payloads_verified':len(held_files),
    'held_workbench_manifest_sha256':identity(DELIVERED_HELD/'FILE_MANIFEST.json')['sha256'],
    'A5_output_directory_exists':False, 'world_evolution_calls':0,
    'production_code_modifications':0, 'new_authority_objects':0,
    'checkpoint_created':False, 'decision':'STOP FOR JASON; correction remains a recommendation.'})

readme = '''# A5 clock diagnosis — review only

Read [A5_CLOCK_COMPATIBILITY_REVIEW.md](A5_CLOCK_COMPATIBILITY_REVIEW.md).

Finding: **APPARATUS DEFECT — correction required to pose approved longer horizons.**
The pinned apparatus falsely rejects the nominal 269.5-second command when
accumulated addition error exceeds its fixed clock allowance. The separate
270-second stage comparator also needs a coherent correction.

This package records diagnosis and alternatives, not an implemented correction.
A5 is still held. No world was evolved, no production code or existing test was
edited, and no authority object or Git checkpoint was created.

## Contents and custody

- The review explains the exact branch, arithmetic, timing domains, prior tests,
  proposed closures, required future tests and bounded effect on A1–A4 evidence.
- DIAGNOSTIC_RESULTS.json is the original detached-check result; ARITHMETIC_DETAIL.json
  preserves a scalar supplement including the explicit-addition/built-in-sum distinction.
- diagnose_clock.py is the new, already-executed detached diagnostic source. It
  depends on the original local paths and pinned runtime; it is not a launcher.
  Do not execute reference scripts merely because they are included here.
- references/ contains byte-identical copies of the pinned source, clock tests,
  prior reviews and selected held-proposal documents. The held manifest is an
  unchanged reference with no grant, not a replacement launch proposal.
- REFERENCE_MANIFEST.json binds those copies to original paths and hashes.
- SOURCE_IDENTITIES_BEFORE/AFTER.json and PRESERVATION.json record the diagnostic
  preservation checks. FINAL_VERIFICATION.json repeats preservation after packaging.
- FILE_MANIFEST.json binds each payload by path, byte count and SHA-256. The archive
  checksum is provided beside the ZIP; neither is an execution authority.

Only six pre-existing detached clock test cases, inert pending predicates, scalar
calculations and saved-record metadata reads were executed. Physical pause/resume,
world component tests, replay, A5 commands against a world, fields, RNG, prehistory
and ecological trajectories were not executed. The 5,579 saved A1–A4 decisions
checked here all retained their expected stage; earlier claim limits remain.

## Unchanged identities and open decision

P: 6bc9683b54e4fa80136fe8534d7713e2a250a95f

Apparatus: 5f07748102cb5eaa302569c87efbae095050e9fe

Held A5: 88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6

The recommendation is an apparatus-only correction using native indices for
scheduling and the unchanged physical recurrence for timestamp provenance.
Jason's decision and separate correction scope remain pending. Shared workbench
navigation, canon, old reviews and commissioning records were not edited.
'''
assert not (OUT/'README.md').exists()
(OUT/'README.md').write_text(readme, encoding='utf-8')
payloads = {p.relative_to(OUT).as_posix():identity(p) for p in sorted(OUT.rglob('*')) if p.is_file()}
write('FILE_MANIFEST.json', {'schema':'diagnosis-review-file-manifest-v1', 'execution_authority':False, 'files':payloads})
zip_path = ROOT/'exports/2026-09-26-A5-clock-compatibility-review-5f077481.zip'
assert not zip_path.exists()
with zipfile.ZipFile(zip_path, 'x', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file(): z.write(p, 'A5_CLOCK_COMPATIBILITY_REVIEW/' + p.relative_to(OUT).as_posix())
with zipfile.ZipFile(zip_path) as z:
    assert z.testzip() is None
    for name, v in payloads.items():
        data = z.read('A5_CLOCK_COMPATIBILITY_REVIEW/'+name)
        assert hashlib.sha256(data).hexdigest() == v['sha256'] and len(data) == v['bytes']
zip_id = identity(zip_path)
checksum_path = zip_path.with_suffix('.zip.sha256')
assert not checksum_path.exists()
checksum_path.write_text(zip_id['sha256']+'  '+zip_path.name+'\n', encoding='ascii')
print(json.dumps({'report':str(OUT/'A5_CLOCK_COMPATIBILITY_REVIEW.md'), 'payloads':len(payloads), 'references':len(references), 'zip':str(zip_path), **zip_id}, indent=2))
