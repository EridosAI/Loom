"""Document-only custody and scalar arithmetic. No Loom imports or execution."""
from pathlib import Path
import hashlib
import json
import math
import re
import shutil
import zipfile
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'exports/2026-09-29-Founder-Search-v0-1-design'
W = ROOT / 'worktrees/loom-p-b1-minimal-20260929'
D = W / 'developmental_ecology'
OLD = ROOT / 'exports/2026-09-23-p-commissioning-design-2fb3ff84'
SRC = OLD / 'REFERENCE_READS/review_inputs/sources'
WB = Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
ATT = Path(r'C:\Users\Jason\.codex\attachments')
REV = ROOT / 'b1_s1_sensory_free_execution_20260929/review'
A = ROOT / 'exports/2026-09-26-A5-launch-packet-68db2c58/references'
DOCS = W / 'docs/developmental_ecology'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n', encoding='utf-8')

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

sources = []
def add(group, path):
    assert path.is_file(), path
    sources.append((group, path))

add('R1', ATT/'a80991f1-e79e-4e55-b8e2-f7570485d145/Pasted text.txt')
add('R2', ATT/'012a0b89-a0e6-4c9b-869f-0fa7c8a2ed29/Pasted text.txt')
add('R3', REV/'B1_MINIMAL_CLOSURE_REPORT.md')
add('R3', REV/'PAIRED_CLOSURE_RESULTS.json')
for name in ('P_COUPLING_COMMISSIONING_DESIGN_v0_1_REVIEW_DRAFT.md', 'P_COMMISSIONING_MATRIX_v0_1_REVIEW_DRAFT.md'):
    add('R4', OLD/'PACKAGE'/name)
for name in ('BUILD_REPORT.md', 'AUTHORITY_AND_INFORMATION_FLOW.md'):
    add('R5', DOCS/'p_apparatus_20260924'/name)
add('R6', SRC/'P_IMPLEMENTATION_AND_OBSERVATION_SPEC_v0_1_REVIEW_DRAFT.md')
add('R7', SRC/'P_SPECIFICATION_DESIGN_REVIEW.md')
for name in ('schema', 'engine', 'neural', 'prehistory', 'records'):
    add('R8', D/'loom_p'/f'{name}.py')
for name in ('contract', 'runner', 'diagnostics', 'clock', 'initialization'):
    add('R8', D/'loom_commissioning'/f'{name}.py')
for case in ('A2', 'A3'):
    add('R9', A/f'{case}_RESOURCE_RESULT.json')
add('R10', DOCS/'p_apparatus_20260924/RUNTIME_STORAGE_ESTIMATE.json')
add('R11', DOCS/'p_engineering_20260921/BUILD_REPORT.md')
add('R11', DOCS/'p_r1p_correction_20260923/BUILD_REPORT.md')
add('R11', REV/'PRESERVED_S1_FULL_RESULT.json')
add('R11', REV/'B1-MINIMAL-S1-SENSORY-FREE.json')
add('R12', ROOT/'sources/00_LOOM_CURRENT_STATE(2).md')
add('R12', WB/'00_RESEARCH_MAP.md')
add('R12', WB/'01_WORKSPACE_STATUS.md')
add('R12', ROOT/'AGENTS.md')
add('R12', WB/'AGENTS.md')
add('R13', OUT/'JASON_TIMING_RULING.md')

refs = OUT/'references'
refs.mkdir(exist_ok=True)
index = []
for n, (group, original) in enumerate(sources, 1):
    copy = refs/f'{group}_{n:02d}_{original.name}'
    before = sha(original)
    shutil.copyfile(original, copy)
    assert before == sha(copy) == sha(original)
    index.append(dict(id=group, original_path=str(original), reference_path=copy.relative_to(OUT).as_posix(),
                      bytes=copy.stat().st_size, sha256=before))
dump(OUT/'SOURCE_INDEX.json', dict(status='Reference custody only; no authority or runtime import',
     inspected_checkpoint='a8cdd75c7f98ebd85d9625ce4d8ae8fa4d790dad',
     P_baseline='6bc9683b54e4fa80136fe8534d7713e2a250a95f',
     historical_orientation_not_latest_execution_status=True, files=index))

a2, a3 = (read(A/f'{n}_RESOURCE_RESULT.json') for n in ('A2','A3'))
full = read(REV/'PRESERVED_S1_FULL_RESULT.json')
null = read(REV/'B1-MINIMAL-S1-SENSORY-FREE.json')
old_rate = read(DOCS/'p_apparatus_20260924/RUNTIME_STORAGE_ESTIMATE.json')
component = next(x for x in old_rate['measured_components'] if x['mode']=='intact_P')
measurements = {}
for name, record in [('A2',a2), ('A3',a3)]:
    sim = record['simulated_seconds_recorded']
    measurements[name] = dict(simulated_seconds=sim, wall_seconds=record['recorder_wall_seconds'],
        wall_seconds_per_simulated_second=record['recorder_wall_seconds']/sim,
        stored_bytes=record['stored_trajectory_bytes_including_snapshots_and_receipt'],
        stored_bytes_per_simulated_second=record['stored_trajectory_bytes_including_snapshots_and_receipt']/sim,
        analysis_wall_seconds=record['analysis_wall_seconds'], P_active=False)
for name, record in [('B1_FULL',full),('B1_SENSORY_FREE',null)]:
    sim = record['simulated_seconds']
    measurements[name] = dict(simulated_seconds=sim, wall_seconds=record['wall_seconds'],
        wall_seconds_per_simulated_second=record['wall_seconds']/sim,
        stored_bytes=record['artifact_bytes'], stored_bytes_per_simulated_second=record['artifact_bytes']/sim,
        P_active=False)
measurements['intact_P_component'] = component
measurements['intact_P_historical_30s'] = old_rate['historical_30s_rate']
measurements['prehistory_one_phase'] = dict(world_only_seconds=600, wall_seconds=65.17840160000014,
                                         P_active=False, scope='one historical phase, no new preparation')
rates = {name: x['wall_seconds_per_simulated_second'] for name,x in measurements.items()
         if 'wall_seconds_per_simulated_second' in x}
stages = {}
for name, sim in [('common_window',12*600),('maximum_staged_total',12*600+4*300+2*900)]:
    stages[name] = dict(simulated_seconds=sim, native_steps=sim*100, waves=sim*5,
        measured_rate_extrapolated_hours={k:sim*v/3600 for k,v in rates.items()},
        execution_planning_hours=sim*25/3600,
        stored_GB_historical=sim*old_rate['historical_30s_rate']['stored_MB_per_simulated_second']/1000,
        stored_GB_component=sim*component['stored_bytes_per_simulated_second']/1e9,
        uncompressed_GB_component=sim*component['uncompressed_record_bytes']/component['duration_seconds']/1e9,
        stored_GB_planning=sim*6_000_000/1e9,
        primary_plus_one_archive_GB_planning=sim*12_000_000/1e9,
        uncompressed_workspace_GB_planning=sim*12_000_000/1e9)
options = {str(n):dict(simulated_seconds=n*600,
               A2_rate_hours=n*600*rates['A2']/3600,
               A3_rate_hours=n*600*rates['A3']/3600) for n in (8,12,16)}
calculations = dict(status='Design arithmetic only; no measurements generated; not approved limits',
    measurements=measurements, stages=stages, population_options=options,
    hypothetical_at_least_one_in_12={str(p):1-(1-p)**12 for p in (.01,.05)},
    prehistory_if_twelve_missing=dict(field_steps=12*60000, world_only_seconds=12*600,
        measured_rate_projection_minutes=12*65.17840160000014/60,
        existing_15_minute_each_guard_total_hours=12*900/3600),
    assumptions=dict(planning_wall_seconds_per_simulated_second=25, planning_stored_bytes_per_simulated_second=6_000_000,
        planning_uncompressed_bytes_per_simulated_second=12_000_000,
        initial_postrun_analysis_hours=4, later_postrun_analysis_hours=4,
        initial_capacity_GB=200, maximum_capacity_GB=280,
        initial_machine_hours_allowance=50+3+4,
        maximum_machine_hours_allowance=10200*25/3600+3+8,
        Jason_selected_total_age_checkpoints_seconds=[600,900,1800],
        slow_reference_time_constants_seconds=[5000,10000],
        pure_simulation_vs_recording_split_measured=False,
        long_run_current_intact_P_rate_measured=False,
        lossless_evidence_fidelity_unchanged=True))
assert stages['maximum_staged_total']['simulated_seconds']==10200
assert calculations['assumptions']['maximum_machine_hours_allowance'] < 82
dump(OUT/'RESOURCE_CALCULATIONS.json', calculations)

design = (OUT/'FOUNDER_SEARCH_v0_1_DESIGN.md').read_text(encoding='utf-8')
sections = re.findall(r'^## (\d+)\.', design, re.MULTILINE)
assert sections == [str(n) for n in range(1,15)], sections
assert not any(marker in design for marker in ('\\[','\\]','\\(','\\)'))
assert all(sha(Path(x['original_path']))==x['sha256'] for x in index)
verification = dict(utc=datetime.now(timezone.utc).isoformat(),
    scope='Static documentation verification only; not an apparatus or scientific test',
    required_numbered_sections=sections,
    scalar_projection_arithmetic_checked=True,
    copied_reference_bytes_match=True,
    source_bytes_rechecked_unchanged=True,
    source_files=len(index),
    runtime_imports=0, new_births=0, P_execution=0, controller_execution=0,
    new_simulated_steps=0, new_prehistories=0, new_execution_authorities=0,
    code_configuration_changes=0, git_writes=0, sealed_human_B1_access=False,
    limit='Action record for this document task; not a forensic claim about other concurrent activity')
dump(OUT/'DELIVERY_VERIFICATION.json', verification)
manifest = []
for file in sorted(OUT.rglob('*')):
    if file.is_file() and file.name != 'PACKAGE_MANIFEST.json':
        manifest.append(dict(path=file.relative_to(OUT).as_posix(), bytes=file.stat().st_size, sha256=sha(file)))
dump(OUT/'PACKAGE_MANIFEST.json', dict(kind='design_document_custody_not_execution_authority',files=manifest))
for row in manifest:
    assert sha(OUT/row['path']) == row['sha256']
archive = OUT.with_suffix('.zip')
with zipfile.ZipFile(archive, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for file in sorted(OUT.rglob('*')):
        if file.is_file(): z.write(file, arcname=OUT.name+'/'+file.relative_to(OUT).as_posix())
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for row in manifest:
        assert hashlib.sha256(z.read(OUT.name+'/'+row['path'])).hexdigest() == row['sha256']
    assert z.read(OUT.name+'/PACKAGE_MANIFEST.json') == (OUT/'PACKAGE_MANIFEST.json').read_bytes()
result = dict(archive=str(archive), bytes=archive.stat().st_size, sha256=sha(archive),
              package_files=len(manifest)+1, reference_files=len(index), verification='passed')
dump(Path(__file__).parent/'PACKAGE_RESULT.json', result)
print(json.dumps(result))
print(json.dumps({'hours':stages, 'options':options},indent=2))
