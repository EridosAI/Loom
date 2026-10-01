"""Exclusive second-correction report/package; prior reports are never rewritten."""
import argparse,hashlib,importlib.metadata,json,platform,subprocess,sys,zipfile
from datetime import datetime,timezone
from pathlib import Path
from loom_p.records import code_identity,strict_bytes
from loom_p.schema import Config
from create_review_package import source_identities,WORKBENCH
from verify_r1p import ROOT,OUT,OLD,sha
REPO=ROOT.parent
DOCS=REPO/'docs/developmental_ecology/p_r1p_correction_20260923'
PACKAGE=ROOT/'artifacts/review-package-r1p-20260923-01a0c405'
def git(*args): return subprocess.check_output(['git','-C',str(REPO),*args],text=True).strip()
def read(name): return json.loads((OUT/name).read_text(encoding='utf-8'))
def write(path,obj):
    with path.open('xb') as f: f.write(obj.encode('utf-8') if isinstance(obj,str) else strict_bytes(obj))
def prepare():
    DOCS.mkdir(parents=True,exist_ok=False)
    assert read('FINAL_SUITE_RECEIPT.json')['exit_code']==0
    write(DOCS/'SOURCE_IDENTITIES.json',source_identities())
    runtime=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),git=git('--version'),dependencies={n:importlib.metadata.version(n) for n in ('numpy','scipy','pytest','colorama','iniconfig','packaging','pluggy','pygments')},code=code_identity(),configuration_sha256=Config().identity(),configuration_file_sha256=sha(ROOT/'configuration.json'),local_execution=True,dependency_installations=0)
    write(DOCS/'RUNTIME_RECORD.json',runtime)
    summary={n:read(n+'.json') for n in ('FINAL_SUITE_RECEIPT','PREHISTORY_AND_SCOPE','RECONSTRUCTION','OBSERVER','ATTEMPT_COMPARISON','PRESERVATION','PHYSICAL_COMPONENT_EVIDENCE')}
    summary['r1p_faults']=read('r1p-fault-matrix/SUMMARY.json'); summary['unchanged_regression_faults']=read('existing-fault-matrix/SUMMARY.json')
    summary['status']='HOLD FOR INDEPENDENT REVIEW; no commissioning fitness declaration'
    write(DOCS/'VERIFICATION_SUMMARY.json',summary)
    suite=(OUT/'FINAL_SUITE.txt').read_text().strip().splitlines()[-1]
    physical=[]
    for case in summary['PHYSICAL_COMPONENT_EVIDENCE']['cases']:
        new=case['comparison']['corrected']; events=new['events']
        free=sum(e['duration'] for e in events if not e['contacts']); contact=sum(e['duration'] for e in events if e['contacts'])
        counts=', '.join(f"{r['function']}:{r['loop_passes']}" for r in new['search_frames'])
        physical.append(f"| {case['case']} | {free:.17g} | {contact:.17g} | {counts} |")
    smokes=[]
    for r in summary['RECONSTRUCTION']['cases']:
        smokes.append(f"| {r['case']} / 004 | {r['native']} / {r['wave']} / {r['events']} | {r['time']:.14g} | {r['execution_wall_seconds']:.3f} | {r['max_accounting_error']:.3g} |")
    differences='\n'.join('- '+r['case']+': '+json.dumps(r['max_absolute_difference'])+f"; changed neural hashes {r['different_neural_hashes']}, raw rows {r['different_raw_rows']}; event records {r['old_events']} → {r['new_events']}." for r in summary['ATTEMPT_COMPARISON'])
    report=fr'''# Loom P — second bounded correction, R1-P

**Hold for independent fidelity review. No commissioning fitness is declared.** Sole implementation scope: R1-P from `LOOM_P_INDEPENDENT_POST_CORRECTION_FIDELITY_REVIEW.md`. R2 and R3 remain closed at the previous checkpoint; their existing test and fault-harness bytes were preserved and rerun, not redesigned.

## Checkpoints, local scope and exact diff

Previous checkpoint: `{OLD}`. Original reviewed checkpoint: `d5f7efbe67193f215e52d95ca912db131a79f31c`. Worktree: `{REPO}`. Existing branch: `{git('branch','--show-current')}`. The new commit is in the package's `CHECKPOINT_RECEIPT.json`, generated after the local evidence commit; `CORRECTION.patch` is the exact committed previous-to-new diff. The historical EXP1-21 tree remains `f1b884a7ada4c806786d1530d76d446aac5d37b1`.

Production changes are confined to `loom_p/physics.py`: added trajectory gap/derivative bounds and whole-interval release search; updated the existing swept search's progress bound. The body integrator, projection, source/repair/stress laws, all configuration values/tolerances, all P equations and native/wave/noise schedule remain unchanged. Added `tests/test_r1p_oblique.py` and new verification/package helpers; current README points here. Every earlier test file and all 12 other runtime modules are byte-identical to f7. No dependency installation, workbench/vault file edit, vault Git write, push, PR or merge occurred. Execution used the existing local Windows `.venv`, Python 3.13.5 and Git 2.50.0.windows.1, with scoped approved worktree access.

Exact user authority and complete independent review are copied into the new evidence directory. The original five-file handoff manifest, accepted P specification and physical foundation were rechecked; their source identities and preserved formatting representations are recorded separately in `SOURCE_IDENTITIES.json`. No historical proposal replaced the selected specification.

## Release and event algorithm

The old inexpensive early release certificate is retained as a fast path. Its failure now invokes `clear_excursion`, which examines the remaining frozen-force path rather than treating an inconclusive early sample as proof of continuous contact. The unchanged convention is $p(s)=p_0+s\,v(s)$, with the existing exponential frozen-force velocity.

`motion_bounds` bounds path speed and acceleration. `gap_curve` evaluates actual gap and normal path rate, including prescribed mover velocity. `gap_curvature_bound` bounds the second derivative of the gap using the relative acceleration and the distance-gradient curvature outside the convex fixture. Over an interval of width $h$, endpoint interpolation differs from the true gap by at most $Bh^2/8$. Release search discards an interval only when an upper enclosure rules out a resolvable excursion; otherwise it subdivides and evaluates the actual geometry. It retains the existing spatial-resolution criterion for a departure from the current touching state, avoiding duplicate sub-tolerance releases at a located return. Neither a failed early certificate nor a failed finite search is silently converted into sustained-contact evidence.

A clear point becomes a swept-search guard only after checking that its preceding path does not cross into the solid beyond geometric tolerance. Release remains at the beginning of the resolved departure, the clear prefix is excluded only while certified, and subsequent return is located by the same event machinery. Free flight has ordinary basal/effort expense but no source transfer, repair or contact damage. Recontact is an explicit zero-duration record, with no zero-duration transfer or repair. Remaining positive contact duration is accounted by the unchanged equations.

The swept search still has its **500-pass limit**, but can now use a local normal-rate lower bound:

$$g(s+h)\geq g(s)+g'(s)h-\tfrac12Bh^2.$$

Solving this quadratic for a safe increment prevents large tangential velocity from forcing hundreds of tiny increments while the normal gap changes slowly. The globally valid speed bound remains available when the curvature bound cannot be certified. The previous 0.8 clearance factor, native dt, geometry/event tolerances and physical-event subdivision limit are unchanged. These are search calculations, not additional integration, learning, random draws or field updates.

If a gap enclosure cannot be resolved within the existing time resolution/search bound, or a proposed free prefix crosses a solid before clearance, the implementation reports an apparatus error instead of fabricating continuous contact or skipping a collision. Those paths are explicit numerical limits, not claims of general curved-contact convergence; this pass verifies the specified radial/oblique departure class and bounded regression cases.

## RED-before-GREEN and independent fixture oracles

Before any physics edit, the exact unmodified f7 runtime was tested with the new regressions: **4 failed**. The exact review fixture and changed-normal-force variant failed at the explicit missing-free-flight assertion; the reflected longer-flight variant reproduced swept-search exhaustion. The cadence fixture also rejected the missing event path. `F7_OBLIQUE_RED.txt` preserves that execution.

The final new test uses an independent analytic transcription of the declared free trajectory and a source-centre distance calculation. It does not call production `release_probe`, `free_velocity`, `actuator_forces` or `gap_normal` for its oracle. Independent bracketing locates descending geometry-tolerance and zero-gap crossings. The scheduled free duration must lie between those crossings (apart from the existing event-time resolution). The exact fixture independently reproduces the 2.4981434698645444e-9 gap at 0.0005 s. Its source, E=0.7, I=1, command [1,1], initial velocity [-1e-5,0], orientation arccos(.01/.76), baseline Config and 0.01-second duration are unchanged.

Two fixed state variants vary orientation/normal force and departure speed/reflection. They are deterministic component falsifiers, not a parameter sweep or new complete-loop case. All fixtures require one release, nonzero free duration, one return, no free-flight contact effects, duration-specific transfer/stress, duration conservation, source/body balance and normal completion. The original radial test remains unchanged. A separate wrapper fixture asserts exactly one native/noise call and one field update despite multiple physical events.

Four new isolated faults were each observed RED then GREEN: **unmodified f7 physics**, **disabled class-level release search**, **f7 swept search with corrected release**, and **duplicated field update**. The old-search fault demonstrates why forcing release alone is insufficient. The original **14-pair fault matrix** was rerun unchanged against the final runtime; every designated fault again failed and its unmutated control passed. Total: **18 RED→GREEN pairs**, with commands, source hashes and separate logs. No runtime file was mutated by these fault subprocesses.

A development check found only an exact decimal-equality assertion on summed time failing at 0.010000000000000002. The new test now checks duration conservation to 1e-16 seconds, in addition to the independent crossing oracle. No runtime tolerance or parameter was changed. Its original 33-pass/1-fail log is retained. Final tests and the old-f7 RED control were then rerun.

## Measured component completion

Each row terminates normally. Loop counts below are observed by read-only Python tracing of the bounded release/swept loops. `search` counts include release and free-prefix validation. They are not measured by changing runtime code.

| Fixture | Positive free duration (s) | Positive contact duration (s) | Actual loop passes |
|---|---:|---:|---|
{chr(10).join(physical)}

`PHYSICAL_COMPONENT_EVIDENCE.json` records full old/new events, bodily consequences and counters. Values are retained even when different from earlier checkpoints. The radial fixture remains GREEN; the exact oblique fixture and both variants are GREEN. Source/body equality alone is not the acceptance gate: the independent free-gap and event-duration assertions must also pass.

## Final assembled suite and smoke evidence

Final worktree suite after all new smoke/reconstruction artifacts exist: **{suite}**. All previously verified R2/R3 checks pass unchanged. The portable package is assembled with all fixtures and runs the same complete component suite before ZIP finalization; its result is `PORTABLE_COMPONENT_SUITE.txt` and `PORTABLE_VERIFICATION.json` inside the ZIP.

Same semantic configuration `{Config().identity()}`, working configuration bytes `{sha(ROOT/'configuration.json')}`, master seed **5284097 / 0x50A101**, life **0**, same fixture definitions and administrative caps. New smoke identity: **attempt-004**.

| Case / attempt | Native / wave / event records | Simulated seconds | Wall seconds | Max source/body residual |
|---|---:|---:|---:|---:|---:|
{chr(10).join(smokes)}

Every case stopped at its administrative cap. All **3,200 neural states** and all three final chemical fields reconstruct bit-identically from their saved actual inputs. Checksums, native/wave/noise counters and source/body accounting pass. The nonzero case repeats the declared 0.07-second pause and 0.93-second duplicate continuation with exact full-state comparison and repeated observer isolation. Saved replay/reconstruction of contact record 40 leaves the live inspector state/counters unchanged at time zero, with zero UI simulation steps and no server started.

New complete-loop execution: **32.93 simulated seconds**, comprising the same 30+1+1-second cases plus the authorized 0.93-second restart comparison. There were no failed attempt-004 smokes or additional complete-loop cases. Detached reconstruction and manufactured arithmetic fixtures are not scientific lifetimes. No efficacy interpretation is made.

Attempt-003 → attempt-004 measured differences:

{differences}

## Preservation, prehistory and portable inspection

All **{summary['PRESERVATION']['files']} preexisting artifact files** retain exact lengths and SHA-256 values. Both earlier checkpoints, every earlier smoke attempt, original reviews/reports and old portable packages remain preserved. Old source documents are unchanged. The new ZIP contains the byte-identical first corrective ZIP, which itself contains the original build ZIP; each checkpoint remains separately identified.

All field/prehistory dependencies and the configuration were verified unchanged before running any refreshed smoke. The existing `prehistory-attempt-001` cache was revalidated by dependency identities, law values, seed/phase, archive checksum and field-array checksum and reused. **No 600-second prehistory regeneration or prehistory step was executed.** `PREHISTORY_AND_SCOPE.json` records the exact identities.

Double-click `developmental_ecology/Open Loom Inspector.cmd`. It loads the **attempt-004 initial contact fixture at time zero, paused**; saved-record replay is available. Launch advances nothing. The existing launcher/inspector bytes are unchanged. For portable setup, the existing `Setup Loom Inspector.cmd` installs pinned dependencies into an adjacent `.venv` using Python 3.13. No fresh installation or visual browser QA was performed in this pass; paused observer arithmetic was reverified. No inspector server or background simulation was started.

The package includes full attempt-004 native/wave/event streams, snapshots, current code/tests, exact config/runtime/source records, authority/review, all RED/GREEN logs, preservation receipts, exact patch and this report. `ARTIFACT_MANIFEST.json` verifies every packaged member; the adjacent ZIP checksum and checkpoint receipt identify this new delivery. Temporary pytest snapshots are omitted; substantive logs and source fixtures are included.

## Remaining limits and what was NOT tested

Independent fidelity review remains pending. No fitness for coupling or ecological commissioning is declared. No scientific lifetimes, cohorts, commissioning, efficacy tuning, parameter/capacity sweeps, survival/useful-learning pass gates, experiment numbering, preregistration, P/R synthesis, JEPA, packet change, associative-regime change or world-law change. No fourth complete-loop case, natural terminal full-loop event, 600-second organism run or prehistory regeneration. No long-duration storage/performance study, cross-platform/dependency-version bit identity, real disk exhaustion, fresh dependency setup or renewed browser/double-click visual inspection.

The finite-step frozen-force/contact-normal realization is not a convergence proof or exhaustive treatment of arbitrary curved/grazing/simultaneous/moving contacts. Search enclosures and finite limits can reject an unresolved path explicitly. Sub-resolution departures retain the existing geometric resolution. The previously disclosed shared equal-valued E/I configuration fields and broader sensory/temporal/associative/ecological scientific questions are unchanged and outside R1-P. R2/R3's representative executable-route coverage remains as independently accepted, not an arbitrary-code security guarantee. **Stop for independent review.**
'''
    write(DOCS/'BUILD_REPORT.md',report)
    write(DOCS/'EXECUTION_LEDGER.md','''# R1-P execution ledger

All commands execute locally from developmental_ecology using the existing `.venv` Python with `-B -X utf8`, pytest cache disabled and isolated new temporary output paths. Existing code/test/configuration/artifact hashes were captured before correction. No prehistory generation, remote operation or existing evidence rewrite is part of this ledger.

1. Complete post-correction fidelity review and exact new user authority read; current f7 checkpoint/branch/clean status verified. New oblique tests run on unchanged runtime: F7_OBLIQUE_RED.txt, four failures.
2. Scoped physics edits; development component checks, including retained initial duration-roundoff failure and subsequent 59-pass suite.
3. `verify_r1p_mutants.py --output artifacts/r1p-correction-20260923-01a0c405/r1p-fault-matrix`: archived f7, disabled class search, archived swept search and duplicate field faults, each RED then GREEN.
4. Unchanged `verify_correction_mutants.py --output artifacts/r1p-correction-20260923-01a0c405/existing-fault-matrix`: original 14 pairs, RED then GREEN.
5. `verify_r1p.py preflight`: all existing tests, config and field dependencies unchanged; lawful prehistory cache validated and reused.
6. `verify_r1p.py smokes`: only birth_30s, nonzero_resume_1s and contact_ui_1s, attempt 004, same seed/life/caps; declared 0.93-second restart comparison included.
7. `verify_r1p.py evidence`: detached neural/field reconstruction and old/new recorded trajectory comparison, inert observer check, original radial and three oblique component old/new comparisons with read-only loop tracing.
8. `verify_r1p.py final`: final suite after all influencing fixtures exist, followed by all-preexisting-artifact preservation check.
9. `package_r1p.py prepare`: new report and provenance files. Scoped local commit follows final evidence; no amend, push, PR or merge.
10. `package_r1p.py package`: exact committed code/diff check, portable assembly, final portable component suite, ZIP member hashes and final checksum. No simulation server is launched.

All prior package/verification scripts remain unchanged. Their mutating stages targeting previous evidence were not invoked.
''')
    (ROOT/'README.md').write_bytes(b'''# Loom P - R1-P correction awaiting independent review

Read ../docs/developmental_ecology/p_r1p_correction_20260923/BUILD_REPORT.md. No commissioning fitness is declared. Earlier checkpoints and all their evidence remain preserved. R2/R3 tests remain unchanged.

Double-click Open Loom Inspector.cmd to load the attempt-004 initial contact_ui_1s fixture PAUSED at time zero. Launch does not advance it. Saved-record replay and detached reconstruction inspect existing records. This delivery authorizes no further runs.

For portable setup with Python 3.13 installed, Setup Loom Inspector.cmd installs the pinned local dependencies into the adjacent .venv. Verified host: Python 3.13.5. Cross-platform bit identity is not claimed. The unchanged server binds only 127.0.0.1:8767; Stop closes it.

The new ZIP includes all attempt-004 streams/snapshots, exact source/config/runtime records, RED/GREEN evidence, the exact correction patch and the unchanged first-correction ZIP. See CHECKPOINT_RECEIPT.json and ARTIFACT_MANIFEST.json. Final component command from this directory: python -B -X utf8 -m pytest tests -q -p no:cacheprovider. Do not invoke prior package preparation or regenerate prehistory when opening this review.
''')
    print('New R1-P report and provenance prepared.',flush=True)
def package():
    commit=git('rev-parse','HEAD'); assert git('rev-parse','HEAD^')==OLD
    assert not git('status','--porcelain')
    tree=git('rev-parse','HEAD:EXP1-21'); assert tree=='f1b884a7ada4c806786d1530d76d446aac5d37b1'
    for name,h in code_identity()['files'].items():
        b=subprocess.check_output(['git','-C',str(REPO),'show',commit+':developmental_ecology/loom_p/'+name]); assert hashlib.sha256(b).hexdigest()==h
    PACKAGE.mkdir(exist_ok=False); selected={}
    def add(p): selected[p.relative_to(REPO).as_posix()]=p.read_bytes()
    for folder in (ROOT/'loom_p',ROOT/'tests',DOCS,REPO/'docs/developmental_ecology/p_correction_20260923',REPO/'docs/developmental_ecology/p_engineering_20260921',ROOT/'artifacts/prehistory-attempt-001'):
        for p in folder.rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts: add(p)
    for p in OUT.rglob('*'):
        if p.is_file() and not any('temp' in part for part in p.relative_to(OUT).parts): add(p)
    for case in ('birth_30s','nonzero_resume_1s','contact_ui_1s'):
        for p in (ROOT/'artifacts'/f'smoke-{case}-attempt-004').iterdir(): add(p)
    for name in ('README.md','configuration.json','requirements-lock.txt','Open Loom Inspector.cmd','Setup Loom Inspector.cmd','verify_r1p.py','verify_r1p_mutants.py','package_r1p.py','verify_correction.py','verify_correction_mutants.py','package_correction.py','verify_engineering_records.py','create_review_package.py','.gitignore','.gitattributes'): add(ROOT/name)
    add(ROOT/'artifacts/information_loss.json')
    selected['preserved_checkpoint/Loom_P_corrective_review_20260923.zip']=(ROOT/'artifacts/review-package-correction-20260923-01a0c405/Loom_P_corrective_review_20260923.zip').read_bytes()
    for row in source_identities()['sources']:
        p=Path(row['path']); selected['review_inputs/'+(row.get('package_path') or 'workbench/'+p.relative_to(WORKBENCH).as_posix())]=p.read_bytes()
        if row.get('pinned_commit'):
            rel=p.relative_to(WORKBENCH/'90_SOURCES/reference_7ada2b300fa1').as_posix()
            selected['review_inputs/pinned_git_blobs/'+rel]=subprocess.check_output(['git','-C',str(REPO),'show',row['pinned_commit']+':'+rel])
    receipt=dict(status='HOLD FOR INDEPENDENT REVIEW',previous_checkpoint=OLD,new_checkpoint=commit,original_checkpoint='d5f7efbe67193f215e52d95ca912db131a79f31c',worktree=str(REPO),branch=git('branch','--show-current'),archive_tree=tree,code=code_identity(),configuration_sha256=Config().identity(),created_at=datetime.now(timezone.utc).isoformat(),smoke_attempt=4,prehistory_regenerated=False,no_commissioning_fitness_declaration=True)
    selected['CHECKPOINT_RECEIPT.json']=strict_bytes(receipt)
    selected['CORRECTION.patch']=subprocess.check_output(['git','-C',str(REPO),'diff','--binary',OLD,commit])
    selected['READ_FIRST.md']=(DOCS/'BUILD_REPORT.md').read_bytes()
    assembled=PACKAGE/'assembled'
    for name,data in selected.items():
        p=assembled/name; assert p.resolve().is_relative_to(assembled.resolve()); p.parent.mkdir(parents=True,exist_ok=True)
        with p.open('xb') as f: f.write(data)
    r=subprocess.run([sys.executable,'-B','-X','utf8','-m','pytest','tests','-q','-p','no:cacheprovider','--basetemp',str(PACKAGE/'portable-test-temp')],cwd=assembled/'developmental_ecology',capture_output=True,text=True,encoding='utf-8')
    write(PACKAGE/'PORTABLE_COMPONENT_SUITE.txt',r.stdout+r.stderr)
    assert r.returncode==0 and '59 passed' in r.stdout,(r.stdout,r.stderr)
    selected['PORTABLE_COMPONENT_SUITE.txt']=(r.stdout+r.stderr).encode()
    selected['PORTABLE_VERIFICATION.json']=strict_bytes(dict(exit_code=0,component_checks=59,cwd=str(assembled/'developmental_ecology'),all_fixtures_present=True,complete_loop_execution=False,new_dependency_install=False))
    manifest={n:dict(bytes=len(b),sha256=hashlib.sha256(b).hexdigest()) for n,b in sorted(selected.items())}
    selected['ARTIFACT_MANIFEST.json']=strict_bytes(manifest)
    target=PACKAGE/'Loom_P_R1P_corrective_review_20260923.zip'
    with zipfile.ZipFile(target,'x',zipfile.ZIP_DEFLATED) as z:
        for n,b in sorted(selected.items()): z.writestr(n,b)
    with zipfile.ZipFile(target) as z:
        for n,row in manifest.items():
            b=z.read(n); assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256']
    write(PACKAGE/'CHECKPOINT_RECEIPT.json',receipt); write(PACKAGE/'ARTIFACT_MANIFEST.json',manifest)
    write(PACKAGE/'ZIP_SHA256.txt',sha(target)+'  '+target.name+'\n')
    print(json.dumps(dict(package=str(target),bytes=target.stat().st_size,sha256=sha(target),members=len(selected),commit=commit,branch=receipt['branch'])),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('action',choices=['prepare','package']); globals()[p.parse_args().action]()
