"""New correction report/package. Never updates the preserved baseline reports."""
import argparse
from datetime import datetime,timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
import sys
import zipfile
from loom_p.records import code_identity,strict_bytes
from loom_p.schema import Config
from create_review_package import source_identities,WORKBENCH
from verify_correction import ROOT,OUT,OLD,sha

REPO=ROOT.parent
DOCS=REPO/'docs/developmental_ecology/p_correction_20260923'
PACKAGE=ROOT/'artifacts/review-package-correction-20260923-01a0c405'

def git(*args): return subprocess.check_output(['git','-C',str(REPO),*args],text=True).strip()
def read(name): return json.loads((OUT/name).read_text(encoding='utf-8'))
def write(path,value):
    with path.open('xb') as f: f.write(value.encode('utf-8') if isinstance(value,str) else strict_bytes(value))

def prepare():
    DOCS.mkdir(parents=True,exist_ok=False)
    sources=source_identities(); write(DOCS/'SOURCE_IDENTITIES.json',sources)
    runtime=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),git=git('--version'),dependencies={n:importlib.metadata.version(n) for n in ('numpy','scipy','pytest','colorama','iniconfig','packaging','pluggy','pygments')},old_checkpoint=OLD,code=code_identity(),configuration_sha256=Config().identity(),configuration_file_sha256=sha(ROOT/'configuration.json'),executed_on='Jason local Windows host through approved scoped execution; not a cloud code sandbox',prehistory_reexecuted=False)
    write(DOCS/'RUNTIME_RECORD.json',runtime)
    verification=dict(review_status='HOLD FOR INDEPENDENT FIDELITY REVIEW; no self-declaration of commissioning fitness',old_checkpoint=OLD,final_suite=read('FINAL_COMPONENT_RECEIPT.json'),mutants=read('mutants-attempt-001/SUMMARY.json'),reconstruction=read('RECONSTRUCTION.json'),observer=read('OBSERVER_ISOLATION.json'),trajectory_comparison=read('TRAJECTORY_COMPARISON.json'),preservation=read('PRESERVATION_VERIFIED.json'))
    assert verification['final_suite']['exit_code']==0
    assert all(r['observed_red'] and r['observed_green'] for r in verification['mutants']['receipts'])
    write(DOCS/'VERIFICATION_SUMMARY.json',verification)
    suite=(OUT/'FINAL_COMPONENT_SUITE.txt').read_text(encoding='utf-8').strip().splitlines()[-1]
    table=[]
    for row in verification['reconstruction']['cases']:
        table.append(f"| {row['case']} / 003 | {row['native']} / {row['wave']} / {row['events']} | {row['time']:.14g} | {row['execution_wall_seconds']:.3f} | {row['status']} |")
    delta='\n'.join('- '+r['case']+': '+json.dumps(r['max_absolute_difference'])+f"; differing organism hashes {r['different_organism_hashes']}/{r['native_compared']}; physical records {r['old_events']} → {r['new_events']}." for r in verification['trajectory_comparison'])
    r1=read('R1_COUNTEREXAMPLE.json')['comparison']; old=r1['old']; new=r1['corrected']
    flight=next(r for r in new['events'] if r['duration']>0 and not r['contacts'])
    sustained=next(r for r in new['events'] if r['duration']>0 and r['contacts'])
    report=f'''# Loom P — bounded corrective engineering report, 2026-09-23

**Hold for independent fidelity review.** This pass implements the authorized R1 correction and supplies new R2/R3 verification. It does not declare the build fit for coupling commissioning. The independent review's failing checkpoint and all its artifacts remain preserved; its old completion claims are historical, not the status of this correction.

## Identity and authority

Old reviewed checkpoint: `{OLD}`. Worktree: `{REPO}`. Existing branch: `{git('branch','--show-current')}`. The new commit is recorded in the package's `CHECKPOINT_RECEIPT.json`, generated after the evidence commit. No amend, rebase, merge, push or PR occurred. Historical EXP1-21 tree remains `f1b884a7ada4c806786d1530d76d446aac5d37b1`.

Authority is the exact `CORRECTION_AUTHORITY.txt`; scope is R1–R3 from `LOOM_P_INDEPENDENT_FIDELITY_REVIEW.md`, copied byte-for-byte into the new evidence directory. The original complete handoff, five-file source manifest and accepted physical references remain the selected sources. Their identities were reverified in `SOURCE_IDENTITIES.json`; project history did not replace the specification. The directional open-domain ruling, P equations, eight-unit/equal-pool baseline, mean-plus-endpoint packet and fading associative regime are unchanged. R and all alternatives remain preserved.

Execution was local Windows Python 3.13.5 and Git 2.50.0.windows.1, using the existing scoped `.venv`; no dependency installation was needed. Restricted read-only inspection and approved worktree writes were distinguished. No Git writes or file edits were made in the Obsidian workbench. The original code checkout's unrelated changes were left alone.

## Exact change

Production change: `developmental_ecology/loom_p/physics.py` only. The new `release_probe` certifies a separating initial segment of the existing frozen-force trajectory. `advance` removes released contacts from the sustained constraint set and emits a zero-duration release record. `first_collision` skips that fixture only until the certified clear point, then includes it in the ordinary swept search. A returned touch is recorded even when its normal impulse is zero. A pending touch at a substep endpoint is processed. No free-motion equation, normal projection, reserve law, field solver, neural equation, constitutive parameter or tolerance was replaced.

Tests changed: `test_neural.py`, `test_physical.py`, `test_records.py`, `test_boundary_and_scheduler.py`; added `test_corrective_contracts.py`. New verification/package helpers are outside `loom_p`, so they do not change snapshot code identity. The current README points to this correction. Exact committed changes are in `CORRECTION.patch`; runtime module hashes are in `RUNTIME_RECORD.json` and every new smoke manifest.

## R1–R3 closure evidence for review

| Finding | Correction and evidence | Review status |
|---|---|---|
| R1 release/recontact | Exact review counterexample; start release, positive free flight, swept return and only the remaining duration charged as contact. Source/body balance, duration, stress/repair identity and native/noise isolation checked. Disabled release, double debit, suppressed damage and repeated native call each observed RED, then GREEN. | Implemented and locally verified; independent closure pending |
| R2 live inspector test | Empty temporary inspector root isolates both native replay and wave artifacts; unique live sentinel and exact `0.2` timestamp prove the intended branch. Missing live wave observed RED, then GREEN. Entire suite runs after all attempt-003 artifacts exist. | Implemented and locally verified; independent closure pending |
| R3 consequential falsifiers | Zero-relative-tolerance reference oracles, separate shared/fine checks, changed-theta bank oracle; terminal indices 19→20 and 59→60 plus retained index-50 noise check; fixed-time/fixed-phase body footprint; executable hidden-state and evoked-reserve injections. Each designated fault produces its expected assertion failure and then a clean test passes. | Implemented and locally verified; independent closure pending |

Final assembled component suite: **{suite}**. Before correction, the reproduced assembled baseline was **43 passed, 1 failed**. `mutants-attempt-001/SUMMARY.json` and 28 separate logs preserve **14 observed RED → GREEN pairs**. Every red subprocess exited 1 at its designated assertion; every corresponding unmutated subprocess exited 0. These are executed faults, not hypothetical statements that a test should fail.

The bank oracle independently checks an interior update as well as active projection, rejecting both a frozen reference and an old-theta target. Sensory reference movements use independent exponential formulas and separately reject disabling each operation. The terminal mutant changes the actual scheduler `elif` to `if` and reaches the intended failing callback, not an unrelated missing-body error. Diffusion holds mover time and phase fixed, checks the occupied cells and exact equality elsewhere.

Hidden-state checks execute real learner native/handoff arithmetic inside the actual coupled wrapper, with physical/field stand-ins and declared transductions clamped. Pose, stocks, fields, time, phase, world configuration and world-stream counter differ while every learner component stays identical. A proxy traps forbidden configuration reads; injected pose and hidden-config mutants fail. A real transduction positive control changes chemistry input and learner arithmetic. This is executable path coverage, not a security sandbox or proof against arbitrary future code.

Evoked E/I channel content is changed with nonzero regulatory weights. Actual reserve inputs remain unchanged through regulation; subsequent body state must exactly equal a separate physical advance receiving only the delivered motor command. Opposite injections do change commands and hence permitted physical effort costs. A direct evoked refill mutant fails. Neither real fields nor a fourth full organism/world case is executed by these fixtures.

## R1 bodily consequences

Exact starting fixture: position `[2,3]`, angle `0`, velocity `[-0.001,0]`, E=`0.7`, I=`1`, stocks all `0.2`, command `[1,1]`, time/phase `0`, dt=`0.01`. The analytic return of the unchanged free path is 0.001314924581309022 s. Its halfway gap is about 3.28623e-7, over 3,000 geometry tolerances.

Observed free flight: **{flight['duration']:.17g} s**; sustained contact: **{sustained['duration']:.17g} s**. Swept detection stops at spatial tolerance; the test's 2e-7 s return-time allowance is derived from the approximately 0.001 normal path speed and unchanged 1e-10 geometry tolerance. It is not a relaxed configuration tolerance. A zero-impulse return is still an explicit event. All positive durations sum to 0.01 s.

| Counterexample consequence | Preserved old implementation | Corrected |
|---|---:|---:|
| Source transfer | {old['transfer']:.17g} | {new['transfer']:.17g} |
| Damage | {old['damage']:.17g} | {new['damage']:.17g} |
| Final E | {old['reserves'][0]:.17g} | {new['reserves'][0]:.17g} |
| Final I | {old['reserves'][1]:.17g} | {new['reserves'][1]:.17g} |

Damage increases here because the impulse threshold allowance is proportional to the shorter sustained-contact duration. The existing damage equation, source debit/body credit and subinterval reserve-dependent force calculation are retained. No attempt was made to recover the prior bodily values. Full old/new events are in `R1_COUNTEREXAMPLE.json`; the old source bytes were read from the preserved commit and executed only for this component comparison.

## Exact bounded reverification

Same configuration SHA `{Config().identity()}`, master seed **5284097 / 0x50A101**, life **0**, unchanged fixture definitions and administrative durations. New identities are attempt **003**. Attempt 002 and all earlier evidence remain unchanged.

| Case / attempt | Native / wave / physical records | Simulated seconds | Wall seconds | Stop |
|---|---:|---:|---:|---|
{chr(10).join(table)}

All **3,200 native neural hashes** and all three final chemical fields reconstruct exactly from initial snapshots and saved actual inputs. Checksums, records, random clocks and source/body accounting pass. `RECONSTRUCTION.json` carries every final hash and accounting residual. Nonzero pause at 0.07 s resumes bit-identically through the remaining 0.93 s, with observed versus unobserved continuations compared at every step. A separate paused-inspector replay/reconstruction at record 40 leaves the live state and counters unchanged and runs zero simulation steps.

New complete-loop execution totals **32.93 simulated seconds**: 30 + 1 + 1 + the authorized 0.93 restart comparison. There were no failed new smoke attempts and no extra UI stepping. Detached reconstruction and arithmetic component fixtures are separate from complete-loop execution. Including the preserved build's disclosed 63.47 seconds, the combined historical total is 96.40 seconds; this is repetition accounting, not a new lifetime.

Observed attempt-002 → attempt-003 differences (maximum absolute values; no efficacy target):

{delta}

Only `physics.py` differs among runtime modules. All field/prehistory dependencies match the baseline bytes; configuration file bytes also match the original runtime receipt. The existing lawful 600-second field cache was checked by module/AST identities, field-law values, phase, archive hash and array hash, then reused. **Zero prehistory steps were rerun.** `PREHISTORY_REUSE.json` gives the receipt. The initial preflight also exposed Git's ordinary JSON newline normalization; the check now separately verifies original working-file bytes and committed JSON content rather than confusing their representations.

## Preservation, use and review boundary

All **252 preexisting artifact files** retain their original lengths and SHA-256 values (`PRESERVATION_VERIFIED.json`). The old report, old review package, attempt-002 results and reviewed commit are preserved. An initial development assertion predicted lower damage; it failed with 54 other tests passing and was removed because that directional prediction was unsupported by the law. The retained gate is the independent duration-specific damage equation. An initial component invocation from the wrong directory failed import collection before tests; the actual recorded checks run from `developmental_ecology`. These setup failures did not run additional organisms.

Open `developmental_ecology/Open Loom Inspector.cmd` by double-clicking. It loads **attempt-003 initial contact_ui_1s at time zero, paused**, with new saved records available for replay. Nothing advances on launch. The launcher and inspector production bytes are unchanged. The browser/server was not launched or visually retested in this correction; paused observer/replay/reconstruction was exercised directly. No inspector server or background simulation was started by this pass. For a portable extraction, the existing `Setup Loom Inspector.cmd` uses Python 3.13 and installs the pinned local dependencies. Cross-host bit identity is not claimed.

The new ZIP contains full attempt-003 traces (including birth), snapshots, tests, exact configuration/runtime/source records, correction authority/review, 14 RED/GREEN pairs, preservation/reconstruction evidence and this report. It also carries the previous portable review ZIP unchanged for the failing checkpoint. `ARTIFACT_MANIFEST.json` hashes every packaged member; the adjacent receipt supplies old/new commits, exact branch, archive tree and ZIP checksum. No source archive was added to Git. All current reports sit in the new `p_correction_20260923` directory.

## What remains uncovered and what was NOT tested

No scientific lifetime, cohort, ecological commissioning, coupling commissioning, capacity/parameter sweep, efficacy tuning, developmental success, useful learning, survival gate, experiment number or preregistration. No 600-second organism run or repeated prehistory. No mechanism alternative, R run, tonic bypass, JEPA, packet replacement, magnitude balancing or stronger association. No extra complete-loop case; no natural terminal death occurred in the three smokes. Terminal scheduling is a stand-in plus separate real-physics component test. No long-duration storage/performance test, cross-platform/version identity, real disk exhaustion, fresh dependency install or renewed visual browser/double-click QA.

Finite frozen-force/contact-normal mechanics remain an uncommissioned numerical realization. The release guards and selected outward/rest/tangent source fixtures do not establish convergence or exhaustive adequacy for curved, grazing, simultaneous or moving contact geometries. Changes below the existing spatial resolution are not resolved into separate flights. Information-flow and reserve-ownership tests cover the named executable paths and mutants, not arbitrary malicious future code. The review's separate limitation that equal-valued E/I constants share configuration fields is unchanged and outside R1–R3. Broader temporal compression, sensory differentiation, associative adequacy and ecology questions remain open. Independent fidelity review must assess closure and any commissioning decision. **Stop here.**
'''
    write(DOCS/'BUILD_REPORT.md',report)
    write(DOCS/'CORRECTION_EQUATION_TEST_MAP.md', '''# Correction equation and test map

The original complete 21-operation map is preserved at `../p_engineering_20260921/EQUATION_TO_CODE_AND_TEST_MAP.md`. Its former verification-strength claims must be read with the independent review and this correction. Production `neural.py`, `engine.py`, `chemistry.py`, `geometry.py` and `schema.py` are unchanged.

| Source operation / rule | Corrective code or assertion | Executed fault |
|---|---|---|
| Physical realization, swept release/return | physics.release_probe / first_collision / advance; test_touch_release_return_duration_and_accounting | release_disabled |
| Physical source/body and duration-specific damage | test_touch_release_return_duration_and_accounting, independent balance/stress oracles | double_source_debit; damage_suppressed |
| One native/noise update per native interval | test_release_subdivision_does_not_repeat_native_or_noise | native_repeated |
| Observer physical timestamp | test_live_handoff_observation_has_physical_timestamp | live_branch_missing |
| Equation 21, new projected bank-reference target | test_bank_projection_and_reference_follow_new_value; rtol=0 | bank_reference_frozen; bank_reference_old_target |
| Equation 15, old shared/fine references | test_separate_sensory_reference_following; independent exponential, rtol=0 | shared_reference_frozen; fine_reference_frozen |
| Terminal exclusion at scheduled handoff | test_terminal_scheduler_restores_trial_state_and_draws_once, indices 19/59 | terminal_guard_removed |
| Solid footprint in field coefficient | test_field_flux_mass_and_moving_geometry_continuity, same time and phase | body_footprint_missing |
| Declared transduction boundary / equations 1–21 | test_hidden_state_cannot_bypass_declared_transductions | hidden_pose_injected; hidden_config_read |
| Evoked E/I versus actual body ownership / equations 10,14,18 | test_evoked_reserves_have_no_direct_physical_ownership | evoked_refill |

Every fault runs in a fresh subprocess with an in-memory patch; runtime files are never mutated by the harness. The 14 assertions and exact logs are named in the mutant summary. The final assembled component result is separate from these selective tests. The three new smokes preserve the exact previously authorized case definitions; detached replay checks every native learner hash and final field without adding a full-loop case.
''')
    write(DOCS/'EXECUTION_LEDGER.md','''# Corrective execution ledger

All Python executions used the existing worktree `.venv`, `-B -X utf8`, from `developmental_ecology`; pytest cache was disabled. No global dependency or Git configuration changed.

1. Read full independent review and user correction authority; inspect local identities/status; capture all 252 preexisting artifact hashes and baseline runtime module hashes. Reproduce baseline suite: 43 passed, 1 failed.
2. Apply the scoped physical correction and verification changes. Development check: 54 passed, 1 failed on an unsupported lower-damage prediction, then remove that outcome assumption while retaining the independent constitutive oracle. One wrong-directory invocation failed import collection before execution.
3. `python -B -X utf8 verify_correction_mutants.py --output artifacts/correction-20260923-01a0c405/mutants-attempt-001` — 14 deliberately broken subprocesses failed their designated assertions; 14 subsequent unmutated selective checks passed.
4. `python -B -X utf8 verify_correction.py preflight` — verify all runtime modules except physics byte-identical; original configuration working bytes and committed JSON content match; validate and reuse existing cache. No prehistory generation call.
5. `python -B -X utf8 verify_correction.py smokes` — only birth_30s, nonzero_resume_1s, contact_ui_1s, each attempt 003, seed 5284097, life 0, same durations. Nonzero comparison is the declared duplicate 0.93-second continuation.
6. `python -B -X utf8 verify_correction.py verify` — all neural/field record reconstruction, accounting, old/new trajectory comparison, paused observation/replay/reconstruction, exact R1 old/new arithmetic fixture. No fourth full loop.
7. `python -B -X utf8 verify_correction.py suite` — full suite after all three new smoke artifacts and reconstruction fixtures exist.
8. `python -B -X utf8 verify_correction.py preserve` — verify every captured preexisting artifact byte/hash.
9. `python -B -X utf8 package_correction.py prepare` — new report/source/runtime/evidence records only. Scoped local Git commit on existing branch; no amend or remote operation.
10. `python -B -X utf8 package_correction.py package` — package committed code and evidence, exact old/new patch, all full new smoke streams, preserved old ZIP and checksum manifests. ZIP verification reads every member. Independent review remains the next boundary.

The unchanged legacy `create_review_package.py` is preserved for provenance; its `prepare` action and the legacy verifier's CLI were NOT run because they target old evidence paths. The new helpers use new paths and exclusive creation.
''')
    readme='''# Loom P — correction awaiting independent review

The R1–R3 corrective pass is documented in `../docs/developmental_ecology/p_correction_20260923/BUILD_REPORT.md`. **Hold for independent fidelity review. No commissioning fitness is declared.** The reviewed d5f7efbe checkpoint, prior report and all prior artifacts remain preserved.

Double-click **Open Loom Inspector.cmd** to open the initial **attempt-003 contact_ui_1s** fixture paused at time zero. Launch advances nothing. Use saved-record replay and detached parameter reconstruction to inspect existing evidence. The existing native/wave controls are explicit, capped engineering controls; this delivery does not authorize further runs.

Portable setup: with Python 3.13 installed, **Setup Loom Inspector.cmd** creates the adjacent `.venv` and installs pinned dependencies. The verified host used Python 3.13.5; cross-platform bit identity is not claimed. The server binds only 127.0.0.1:8767. Stop closes it.

The new portable package includes every attempt-003 native, wave and event record, snapshots, exact sources/configuration/runtime records, correction review/authority, RED/GREEN evidence and the unchanged older review ZIP. Check `CHECKPOINT_RECEIPT.json` for exact commits and `ARTIFACT_MANIFEST.json` for content hashes. Original build documents are historical; the new correction report controls the delivered verification status.

The component command is `python -B -X utf8 -m pytest tests -q -p no:cacheprovider` from this directory. New verification helpers use exclusive output paths to prevent overwriting evidence. Do not rerun smokes, generate prehistory, invoke old package preparation or commission experiments as part of opening this review.
'''
    (ROOT/'README.md').write_bytes(readme.encode('utf-8'))
    print('New correction report and source/runtime records prepared.',flush=True)

def package():
    commit=git('rev-parse','HEAD'); branch=git('branch','--show-current')
    assert commit!=OLD and git('rev-parse','HEAD^')==OLD
    assert git('rev-parse','HEAD:EXP1-21')=='f1b884a7ada4c806786d1530d76d446aac5d37b1'
    assert not git('status','--porcelain','--','developmental_ecology','docs/developmental_ecology/p_correction_20260923')
    for name,h in code_identity()['files'].items():
        blob=subprocess.check_output(['git','-C',str(REPO),'show',commit+':developmental_ecology/loom_p/'+name])
        assert hashlib.sha256(blob).hexdigest()==h
    PACKAGE.mkdir(exist_ok=False)
    receipt=dict(status='HOLD FOR INDEPENDENT FIDELITY REVIEW',old_checkpoint=OLD,new_checkpoint=commit,branch=branch,worktree=str(REPO),code=code_identity(),configuration_sha256=Config().identity(),archive_tree=git('rev-parse','HEAD:EXP1-21'),created_at=datetime.now(timezone.utc).isoformat(),prehistory_regenerated=False,no_remote_operation=True,smoke_attempt=3,scope='R1–R3 engineering only; no commissioning fitness declaration')
    selected={}
    def add(path):
        selected[path.relative_to(REPO).as_posix()]=path.read_bytes()
    for folder in (ROOT/'loom_p',ROOT/'tests',DOCS,REPO/'docs/developmental_ecology/p_engineering_20260921',OUT,ROOT/'artifacts/prehistory-attempt-001'):
        for path in folder.rglob('*'):
            if path.is_file() and '__pycache__' not in path.parts: add(path)
    for name in ('configuration.json','requirements-lock.txt','README.md','Open Loom Inspector.cmd','Setup Loom Inspector.cmd','verify_correction.py','verify_correction_mutants.py','package_correction.py','verify_engineering_records.py','create_review_package.py','.gitignore','.gitattributes'):
        add(ROOT/name)
    add(ROOT/'artifacts/information_loss.json')
    for case in ('birth_30s','nonzero_resume_1s','contact_ui_1s'):
        for path in (ROOT/'artifacts'/f'smoke-{case}-attempt-003').iterdir(): add(path)
    oldzip=ROOT/'artifacts/review-package-20260922-01a0c405/Loom_P_build_review_20260922.zip'
    selected['preserved_checkpoint/Loom_P_build_review_20260922.zip']=oldzip.read_bytes()
    selected['preserved_checkpoint/physics.py']=subprocess.check_output(['git','-C',str(REPO),'show',OLD+':developmental_ecology/loom_p/physics.py'])
    source=source_identities()
    for row in source['sources']:
        path=Path(row['path']); key='review_inputs/'+(row['package_path'] if row.get('package_path') else 'workbench/'+path.relative_to(WORKBENCH).as_posix())
        selected[key]=path.read_bytes()
        if row.get('pinned_commit'):
            relative=path.relative_to(WORKBENCH/'90_SOURCES/reference_7ada2b300fa1').as_posix()
            selected['review_inputs/pinned_git_blobs/'+relative]=subprocess.check_output(['git','-C',str(REPO),'show',row['pinned_commit']+':'+relative])
    selected['CHECKPOINT_RECEIPT.json']=strict_bytes(receipt)
    selected['CORRECTION.patch']=subprocess.check_output(['git','-C',str(REPO),'diff','--binary',OLD,commit,'--','developmental_ecology','docs/developmental_ecology/p_correction_20260923'])
    selected['READ_FIRST.md']=(DOCS/'BUILD_REPORT.md').read_bytes()
    # Exercise exactly the portable member bytes from a separate assembled root.
    # This full component run occurs after every packaged fixture is present.
    assembled=PACKAGE/'assembled'
    for name,data in selected.items():
        path=assembled/name
        assert path.resolve().is_relative_to(assembled.resolve())
        path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as f: f.write(data)
    result=subprocess.run([sys.executable,'-B','-X','utf8','-m','pytest','tests','-q','-p','no:cacheprovider','--basetemp',str(PACKAGE/'portable-test-tmp')],cwd=assembled/'developmental_ecology',capture_output=True,text=True,encoding='utf-8')
    portable_log=(result.stdout+result.stderr).encode('utf-8')
    write(PACKAGE/'PORTABLE_COMPONENT_SUITE.txt',portable_log.decode('utf-8'))
    if result.returncode or '55 passed' not in result.stdout:
        print(result.stdout+result.stderr,flush=True); raise RuntimeError('Portable assembled suite failed')
    selected['PORTABLE_COMPONENT_SUITE.txt']=portable_log
    selected['PORTABLE_VERIFICATION.json']=strict_bytes(dict(exit_code=result.returncode,component_checks=55,cwd=str(assembled/'developmental_ecology'),runtime_executable=sys.executable,after_all_portable_fixtures_present=True,new_dependency_install=False,additional_complete_loop_execution=False))
    manifest={n:dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest()) for n,b in sorted(selected.items())}
    selected['ARTIFACT_MANIFEST.json']=strict_bytes(manifest)
    target=PACKAGE/'Loom_P_corrective_review_20260923.zip'
    with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED) as z:
        for n,b in sorted(selected.items()): z.writestr(n,b)
    with zipfile.ZipFile(target) as z:
        for n,row in manifest.items():
            b=z.read(n); assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    write(PACKAGE/'CHECKPOINT_RECEIPT.json',receipt)
    write(PACKAGE/'ARTIFACT_MANIFEST.json',manifest)
    write(PACKAGE/'ZIP_SHA256.txt',sha(target)+'  '+target.name+'\n')
    print(json.dumps(dict(package=str(target),bytes=target.stat().st_size,sha256=sha(target),members=len(selected),commit=commit,branch=branch)),flush=True)

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('action',choices=['prepare','package']); args=parser.parse_args(); globals()[args.action]()
