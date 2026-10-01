"""Administrative document packaging only. No Loom imports or trajectory decoding."""
import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import zipfile

S = Path(__file__).resolve().parent
R = S.parent
W = R / 'worktrees/loom-p-b1-coordinate-colours-20260929'
D = W / 'developmental_ecology'
E = R / 'exports/2026-09-29-B1-minimal-closure-design-v0-2'
OLD = R / 'exports/2026-09-29-B1-automated-reference-design-v0-1'
F = R / 'b1_execution_20260929_colours_01'
H = R / 'b1_hidden_execution_20260929_01'
BASE = '352f73fffa6d9781eae8aa38e708a9a05669588f'
COMPACT = '1060a17e3dd14c6361f6f15c95bb58fad3110ffc'
COLOURS = 'b684912eaf7811cd318ee94c77172aca790f3a0d'
HTML = 'developmental_ecology/loom_commissioning/sensor.html'
REQUEST = Path('C:/Users/Jason/.codex/attachments/9eaaa114-f72b-4140-a61d-78f3dafd7ca3/Pasted text.txt')
ENV = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
GIT = ['git', '-c', 'safe.directory=' + W.as_posix(), '-c',
       'core.excludesFile=' + (R / 'a5_regeneration_20260926/empty-excludes').as_posix(), '-C', str(W)]

def git(*args):
    return subprocess.check_output(GIT + list(args), env=ENV)

def hash_bytes(blob):
    return hashlib.sha256(blob).hexdigest()

def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def js(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False, allow_nan=False) + '\n', encoding='utf-8', newline='\n')

def cp(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)

def verify_inventory(directory, manifest):
    inventory = js(manifest)
    for name, record in inventory['files'].items():
        path = (directory / name).resolve()
        assert path.is_relative_to(directory.resolve())
        assert sha(path) == record['sha256'], name
        assert path.stat().st_size == record['bytes'], name
    return len(inventory['files'])

assert not E.exists(), 'Never overwrite a delivered review package'
assert git('rev-parse', 'HEAD').decode().strip() == COLOURS
assert git('status', '--porcelain') == b''
branch = git('branch', '--show-current').decode().strip()
assert branch == 'build/p-b1-coordinate-colours-20260929-01a0c405'
assert git('rev-parse', COLOURS + '^').decode().strip() == COMPACT
assert git('rev-parse', COMPACT + '^').decode().strip() == BASE
assert git('rev-list', '--count', BASE + '..' + COLOURS).decode().strip() == '2'
paths = git('diff', '--name-only', BASE, COLOURS).decode().splitlines()
assert [p for p in paths if not p.startswith('docs/')] == [HTML]
assert len(paths) == 10
html = {c: git('show', c + ':' + HTML) for c in (BASE, COMPACT, COLOURS)}
outside = {c: re.sub(rb'<style>.*?</style>', b'<style></style>', blob, flags=re.S) for c, blob in html.items()}
assert len(set(outside.values())) == 1
assert all(blob.count(b'<style>') == 1 for blob in html.values())
assert {c: hash_bytes(blob) for c, blob in html.items()} == {
    BASE: '806221de1db825a72eaf8e5533553ff97cff11d30c4a7251cf517a128bcbcf9b',
    COMPACT: '0b322ff6e4291e5cc68076002e3e37faecb178e5609eab858721abe6fbdc3a95',
    COLOURS: '3742b5989c0e3dd7d11e39d4376699dc3d3dd88918519a0bbe380073eb1c75b3'}
assert (W / HTML).read_bytes() == html[COLOURS]

old_count = verify_inventory(OLD, OLD / 'FILE_MANIFEST.json')
old_sha = sha(OLD / 'B1_AUTOMATED_REFERENCE_DESIGN_v0_1.md')
assert old_sha == 'ac43dca13b34d1e545c9a46aebec6995454a6ce43633228dc96d842a7390be74'
assert sha(OLD.with_suffix('.zip')) == 'b7e438a187088cd59e6e829cc88d3fd4841229b4771d64ae15923a9560d78a50'
assert sha(R / 'b1_replacement_design_20260929/B1_AUTOMATED_REFERENCE_DESIGN_v0_1.md') == old_sha
full_count = verify_inventory(F / 'private', F / 'private/COMPLETED_ATTEMPT_FILE_MANIFEST.json')
hidden_count = verify_inventory(H / 'private', H / 'private/WITHDRAWN_FILE_MANIFEST.json')
full = js(F / 'FULL_RAW_OPERATOR_COMPLETION.json')
hidden = js(H / 'WITHDRAWAL_RECEIPT.json')
assert full['checkpoint'] == COLOURS and full['human_commands'] == 202 and full['native_steps'] == 2020
assert abs(full['simulated_seconds'] - 20.2) < 1e-10
assert hidden['native_steps'] == hidden['commands'] == hidden['simulated_seconds'] == 0
assert hidden['execution_authorization_withdrawn'] and hidden['prior_lifecycle'] == 'prepared'
assert js(H / 'STATE.json')['live_services'] == 0
assert js(F / 'STATE.json')['live_services'] == 0

E.mkdir(parents=True)
for name in ('README.md', 'APPARATUS_PROVENANCE_CLARIFICATION.md', 'B1_MINIMAL_CLOSURE_DESIGN_v0_2.md', 'V0_1_NOT_SELECTED.md'):
    cp(S / name, E / name)
cp(REQUEST, S / 'REQUEST.md')
cp(S / 'REQUEST.md', E / 'REQUEST.md')
cp(S / 'V0_1_NOT_SELECTED.md', OLD.parent / (OLD.name + '.NOT_SELECTED.md'))
cp(S / 'V0_1_NOT_SELECTED.md', R / 'b1_replacement_design_20260929/NOT_SELECTED.md')

changes = []
for c, parent in ((COMPACT, BASE), (COLOURS, COMPACT)):
    changes.append(dict(commit=c, parent=parent, subject=git('show', '-s', '--format=%s', c).decode().strip(),
                        changed_files=git('diff', '--name-only', parent, c).decode().splitlines(),
                        html_sha256=hash_bytes(html[c]), outside_style_byte_identical=True))
write(E / 'PROVENANCE_BYTE_PROOF.json', dict(
    checked_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    last_independently_reviewed=BASE, inspected_head=COLOURS, branch=branch, worktree=str(W),
    current_worktree_clean=True, descendants=changes, all_changed_files=paths,
    only_changed_production_file=HTML, changed_documentation_file_count=9,
    html_sha256={c: hash_bytes(b) for c, b in html.items()},
    outside_style_sha256={c: hash_bytes(b) for c, b in outside.items()},
    outside_style_byte_identical_across_all_three=True,
    current_production_bytes_match_git=True, no_new_independent_review_claim=True))
(E / 'PRODUCTION_DIFF_352f_to_b684.txt').write_bytes(git('diff', '--no-ext-diff', BASE, COLOURS, '--', HTML))

record_paths = [
    F / 'FULL_RAW_OPERATOR_COMPLETION.json', H / 'WITHDRAWAL_RECEIPT.json',
    H / 'WITHDRAWAL_PRESERVATION.json', H / 'WITHDRAWN_SERVICE_STOP_RECEIPT.json',
    R / 'b1_execution_20260927/ZERO_STEP_CLOSURE_AND_LAYOUT_AUTHORIZATION.json',
    R / 'b1_execution_20260929/EXPIRED_ZERO_STEP_RESTART_REQUEST.json',
    R / 'b1_execution_20260929_restart_01/PREFIX_CLOSURE_AND_COLOUR_LABEL_AUTHORIZATION.json']
for p in record_paths:
    cp(p, E / 'public_receipts' / p.name)

op = R / 'exports/2026-09-29-B1-colour-labels-b684912e/B1_OPERATOR_PACKET'
resource_paths = [
    R / 'exports/2026-09-26-A4-launch-packet-5f077481/references/A2_RESOURCE_RESULT.json',
    R / 'exports/2026-09-26-A4-launch-packet-5f077481/references/A3_RESOURCE_RESULT.json',
    R / 'exports/2026-09-26-A5-commissioning-result-68db2c58/A5_COMMISSIONING_RESULT/RESOURCE_RESULT.json']
resource_data = [js(p) for p in resource_paths]
ratios = {name: item['recorder_wall_seconds'] / item.get('simulated_seconds_recorded', item.get('simulated_seconds'))
          for name, item in zip(('A2', 'A3', 'A5'), resource_data)}
per = js(op / 'RESOURCE_PROJECTION.json')['cases'][0]['retained_primary_planning_bytes']
total = 3 * 3 * 30
force_coefficient = .5 * (.2 + .8 * .7)
hold_force = 2 * force_coefficient * .05
q = hold_force / (hold_force + .1)
write(E / 'RESOURCE_ARITHMETIC.json', dict(
    status='PROPOSAL / NO EXECUTION AUTHORITY', starts=3, arms_per_start=3, maximum_trajectories=9,
    per_case_simulated_ceiling_seconds=30, total_simulated_ceiling_seconds=total,
    native_step_ceiling=27000, command_hold_ceiling=2700, model_fitting_runs=0,
    recorded_wall_per_simulated_second=ratios,
    base_simulation_minutes={name: total * rate / 60 for name, rate in ratios.items()},
    proposed_per_case_wall_ceiling_seconds=600, proposed_aggregate_execution_wall_ceiling_seconds=5400,
    proposed_separate_reporting_wall_ceiling_seconds=1800,
    overhead_measured=False, overheads=['sensory-history serialization', 'static verification and packaging'],
    no_new_prehistory_in_projection=True,
    prehistory_dependency='Reuse verified non-human A-series world-only cache if compatible; otherwise stop for Jason decision.',
    conservative_existing_B1_allowance_per_case_bytes=per, primary_bytes=9 * per,
    primary_plus_second_full_copy_bytes=18 * per,
    exact_storage_cap_requires_later_packet=True, old_grants_or_caps_not_reused=True,
    storage_redesign=False, native_fidelity_reduction=False, benchmark_runs=0))
write(E / 'SCALAR_PLAUSIBILITY.json', dict(
    status='ALGEBRA ONLY / NOT A TRAJECTORY OR CONTROLLER EXECUTION',
    conditioning='Undamaged body at E=0.7, I=1; ideal frozen reserves and stationary frontal contact where stated.',
    actuator_force_coefficient=force_coefficient,
    seek_pair_when_balanced=[.3, .3], free_terminal_speed=2 * force_coefficient * .3,
    continuous_drag_30s_straight_displacement=2 * force_coefficient * .3 * (30 - (1 - math.exp(-30))),
    angular_terminal_rate_per_differential_command=.35 * 2 * force_coefficient / .2,
    maximum_scalar_angular_terminal_rate=.35 * 2 * force_coefficient / .2 * .4,
    hold_pair=[.05, .05], ideal_hold_force=hold_force, ideal_exchange_quality=q,
    initial_gross_transfer_rate_if_full_source_and_stationary=.04 * (1 - .7) * q,
    static_contact_onset_rate_equivalent=-.25 * math.log(1 - .05),
    coupling_dynamics_evaluated=False, new_model_or_controller_implemented=False))

sources = [R / 'AGENTS.md', W / '00_LOOM_CURRENT_STATE.md', REQUEST,
           S / 'REQUEST.md', OLD / 'B1_AUTOMATED_REFERENCE_DESIGN_v0_1.md', OLD / 'FILE_MANIFEST.json',
           R / 'research_direction_20260929/JASON_DEVELOPMENTAL_SELECTION_CLARIFICATION.md',
           R / 'exports/2026-09-23-p-commissioning-design-2fb3ff84/P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md',
           *record_paths, *resource_paths, op / 'RESOURCE_PROJECTION.json', op / 'PROTOCOL_CONTRACT.json',
           op / 'DISPLAY_CONTRACT.json',
           *[D / 'loom_p' / n for n in ('geometry.py', 'physics.py', 'chemistry.py', 'prehistory.py')],
           *[D / 'loom_commissioning' / n for n in ('controllers.py', 'operator_view.py', 'initialization.py', 'authority.py', 'runner.py', 'evaluation.py')],
           D / 'configuration.json', D / 'requirements-lock.txt', W / HTML,
           W / 'docs/developmental_ecology/p_b1_compact_layout_20260927/COMPACT_LAYOUT_REVIEW.md',
           W / 'docs/developmental_ecology/p_b1_compact_layout_20260927/LAYOUT_BYTE_PROOF.json',
           W / 'docs/developmental_ecology/p_b1_coordinate_colours_20260929/REVIEW.md',
           W / 'docs/developmental_ecology/p_b1_coordinate_colours_20260929/VERIFICATION.json']
write(E / 'SOURCE_RECORDS.json', dict(
    local=[dict(path=str(p), sha256=sha(p), bytes=p.stat().st_size) for p in sources],
    priority='Jason current review governs design and human interpretation. Verified current source governs interface facts. Earlier snapshots remain context.',
    current_orientation_is_older_than_implementation=True,
    sealed_state_access='Only opaque byte checksums against existing preservation inventories; no snapshot, trajectory or evaluator decoding.',
    external_sources=[]))

assert git('status', '--porcelain') == b''
assert verify_inventory(OLD, OLD / 'FILE_MANIFEST.json') == old_count
assert verify_inventory(F / 'private', F / 'private/COMPLETED_ATTEMPT_FILE_MANIFEST.json') == full_count
assert verify_inventory(H / 'private', H / 'private/WITHDRAWN_FILE_MANIFEST.json') == hidden_count
write(E / 'VERIFICATION.json', dict(
    recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    task='B1 minimal closure design only', provenance_reported_before_design=True,
    apparatus=COLOURS, exact_parent=COMPACT, last_independently_reviewed=BASE,
    P='6bc9683b54e4fa80136fe8534d7713e2a250a95f', worktree_clean_before_and_after=True,
    original_v0_1_status='NOT SELECTED', original_v0_1_design_unchanged=True,
    original_v0_1_package_files_verified=old_count, original_v0_1_archive_unchanged=True,
    disposition_additive_outside_frozen_package=True,
    full_raw_private_files_verified_opaque=full_count, full_raw_simulated_seconds=20.2,
    full_raw_human_commands=202, full_raw_interpretation='Jason qualitative observation only; no quantitative B1 PASS',
    hidden_private_files_verified_opaque=hidden_count,
    hidden_status='AUTHORIZED-BUT-NOT-EXECUTED / WITHDRAWN AT JASON DIRECTION',
    hidden_simulated_seconds=0, hidden_native_steps=0, hidden_commands=0,
    old_human_records_modified=False, evaluator_state_inspected=False,
    private_trajectory_or_snapshot_decoded=False, evaluator_disclosed=False,
    production_code_changes=0, controller_implementations=0, configuration_changes=0,
    new_simulation_steps=0, new_worlds_loaded=0, new_controller_executions=0,
    new_prehistory_generation=0, fitting_or_training_runs=0, execution_authorities_created=0,
    tests_run=0, checks='Read-only Git ancestry/diff and byte identity; preservation hashes; scalar arithmetic; package integrity.',
    no_new_independent_review_claim=True, population_or_nursery_design=False,
    git_writes=0, vault_git_writes=0, pushes=0, PRs=0, merges=0))

files = {p.relative_to(E).as_posix(): dict(sha256=sha(p), bytes=p.stat().st_size)
         for p in sorted(E.rglob('*')) if p.is_file()}
write(E / 'FILE_MANIFEST.json', dict(files=files, excludes_self=True, not_an_execution_authority=True))
archive = E.with_suffix('.zip')
assert not archive.exists()
with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as z:
    for p in sorted(E.rglob('*')):
        if p.is_file():
            z.write(p, p.relative_to(E))
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    assert set(z.namelist()) == set(files) | {'FILE_MANIFEST.json'}
    for name in z.namelist():
        assert hash_bytes(z.read(name)) == sha(E / name)
    assert not any(s in n.lower() for n in z.namelist() for s in ('private/', 'snapshot', 'native.jsonl', 'sensor.jsonl', 'controller.jsonl', 'authority-object'))
write(S / 'DELIVERY_RECEIPT.json', dict(package=str(E), archive=str(archive), archive_sha256=sha(archive),
    design_sha256=sha(E / 'B1_MINIMAL_CLOSURE_DESIGN_v0_2.md'), files=len(files) + 1,
    design_only=True, no_new_authority=True, no_execution=True, no_sealed_state_decoded=True))
print(json.dumps(dict(package=str(E), archive_sha256=sha(archive), files=len(files) + 1,
                     base_wall_minutes={k: round(v * total / 60, 3) for k, v in ratios.items()},
                     primary_bytes=9 * per, provenance='verified', preservation='verified', new_execution=0)))
