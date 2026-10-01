"""Packet authoring only. Exact copies, identities and pure scalar scheduling."""
import ast
import collections
import copy
import hashlib
import importlib.util
import json
import os
import pathlib
import shutil
import subprocess
import sys
import zipfile
from static_scheduler_check import audit
from validate_packet import canonical, strict, diffs, verify

S = pathlib.Path(__file__).resolve().parent
ROOT = S.parent
H = ROOT/'exports/2026-09-26-A5-launch-packet-HOLD-5f077481'
OUT = ROOT/'exports/2026-09-26-A5-launch-packet-68db2c58'
W = ROOT/'worktrees/loom-p-clock-correction-20260926'
D = W/'developmental_ecology'
WB = pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench')
WBH = WB/'INBOX/2026-09-26-A5-launch-packet-HOLD-5f077481/A5_LAUNCH_PACKET_HOLD'
COR = ROOT/'exports/2026-09-26-A5-clock-correction'
CP = COR/'portable/Loom_P_Clock_Correction_Review_20260926'
P = '6bc9683b54e4fa80136fe8534d7713e2a250a95f'
APP = '68db2c581f07200966d699a4f55a65f9b96df1e9'
OLDHASH = '88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6'
DEST = D/'artifacts/commissioning-A5-20260926-68db2c58'
IDENTITY = 'IDENTITY-ONLY CHANGE REQUIRED BY NEW APPARATUS'
SCHEDULER = 'SCHEDULER REPRESENTATION CHANGE REQUIRED BY CLOCK FIX'
FORBIDDEN = []
CALLS = collections.Counter()


def guard(frame, event, arg):
    if event != 'call':
        return
    f = frame.f_code; path = f.co_filename.replace('\\', '/')
    if '/loom_p/' not in path and '/loom_commissioning/' not in path:
        return
    CALLS[path.rsplit('/', 1)[-1] + ':' + f.co_name] += 1
    allowed = {'require','digest','strict_bytes','code_identity','apparatus_identity',
               'runtime_identity','_runtime_identity','canonical','unique_json','file_identity',
               'callable_identity','portable','controller_identity','adapter_identity','make_execution',
               'validate_execution','validate_protocol_fields','visit','validate_plan','validate_dispatch',
               'authorize_execution','execution_object','execution_sha256','grid_steps','case_end',
               'stage_ends','decision_clock','hold_steps','expected_time','clock_allowance',
               'validate_physical_time','waypoint_stage','time_due'}
    class_definition = f.co_flags == 0 and f.co_name in {'Recorder','Config','Streams','Body','TerminalCrossing','FieldSolver','Cortex','Association','Regulator','Motor','Organism','Engine','SensorHistory','RestoredSession','Run'}
    if f.co_name not in allowed and not f.co_name.startswith('<') and not class_definition:
        FORBIDDEN.append(path + ':' + f.co_name)
        raise AssertionError('No simulation or command call permitted: ' + FORBIDDEN[-1])


def sha(p):
    with pathlib.Path(p).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def write(n, v):
    q = OUT/n; q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes((json.dumps(v, indent=2, ensure_ascii=False, allow_nan=False)+'\n').encode())


def txt(n, v):
    q = OUT/n; q.parent.mkdir(parents=True, exist_ok=True); q.write_bytes(v.encode())


def cp(p, n):
    q = OUT/n; q.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, q)


def git(*args):
    env = os.environ.copy(); env['GIT_OPTIONAL_LOCKS'] = '0'
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(S/'empty-excludes').as_posix(),'-C',str(W),*args], env=env)


def check_seal(folder, manifest_name='FILE_MANIFEST.json'):
    fm = strict((folder/manifest_name).read_bytes())
    names = {p.relative_to(folder).as_posix() for p in folder.rglob('*') if p.is_file()}
    assert names == set(fm['files']) | {manifest_name}
    for n,v in fm['files'].items():
        assert (folder/n).stat().st_size == v['bytes'] and sha(folder/n) == v['sha256'], str(folder/n)
    return fm


def classify(rows, allowed, reason):
    result = []
    for r in rows:
        matched = [value for prefix, value in allowed.items() if r['path'] == prefix or r['path'].startswith(prefix + '/')]
        assert matched, ('UNEXPECTED SEMANTIC CHANGE', r)
        assert len(set(matched)) == 1, r
        result.append(dict(r, classification=matched[0], reason=reason))
    return result


def main():
    assert not (OUT/'AUTHORITY_OBJECT.canonical.json').exists() and not (OUT/'FILE_MANIFEST.json').exists() and not DEST.exists()
    (S/'empty-excludes').touch(exist_ok=True)
    assert git('rev-parse','HEAD').decode().strip() == APP
    assert not git('status','--porcelain').strip()
    oldfm = check_seal(H); wbheldfm = check_seal(WBH); assert oldfm == wbheldfm
    assert sha(WBH.parent/'A5_LAUNCH_PACKET_HOLD.zip') == '2fa70cd6fb37a80043045678227a0b331b7df9205c7ac46e01d71df754e04460'
    spec = importlib.util.spec_from_file_location('held_validator', H/'validate_packet.py')
    oldvalidator = importlib.util.module_from_spec(spec); spec.loader.exec_module(oldvalidator)
    oldcheck = oldvalidator.verify(lambda n: (H/n).read_bytes(), list(oldfm['files'])+['FILE_MANIFEST.json'])
    assert oldcheck['authority_sha256'] == OLDHASH
    check_seal(CP, 'ARTIFACT_MANIFEST.json')
    old = strict((H/'A5_MANIFEST.json').read_bytes()); m = copy.deepcopy(old)
    preserved = {p for root in (H, WBH) for p in root.rglob('*') if p.is_file()}
    preserved.add(WBH.parent/'A5_LAUNCH_PACKET_HOLD.zip')
    preserved.update(p for name in ('loom_p','loom_commissioning') for p in (D/name).iterdir() if p.suffix in ('.py','.html'))
    preserved.update((D/'configuration.json', D/'requirements-lock.txt'))
    before = {str(p): sha(p) for p in sorted(preserved)}
    OUT.mkdir(parents=True,exist_ok=True)
    probe = OUT/'access-check.tmp'; probe.write_bytes(b'A5 packet preparation only'); assert probe.read_bytes() == b'A5 packet preparation only'; probe.unlink()
    # Small old files are archived exactly; large immutable references/cache are shared.
    for p in H.rglob('*'):
        if not p.is_file(): continue
        n = p.relative_to(H).as_posix()
        if n.startswith(('references/', 'verified-cache/')):
            cp(p,n)
        else:
            cp(p,'historical-held/'+n)
    sys.setprofile(guard); sys.path.insert(0,str(D))
    from loom_commissioning import authority, contract, clock, controllers, runner
    from loom_p.records import code_identity
    pi = code_identity(); ai = contract.apparatus_identity(); ri = authority.runtime_identity()
    assert pi['sha256'] == m['p_code'] == contract.P_CODE
    assert ri == m['execution']['runtime']
    idsold = strict((H/'CODE_AND_RUNTIME_IDENTITIES.json').read_bytes())
    assert sha(D/'configuration.json') == idsold['configuration_file_sha256']
    for p in (D/'loom_p').glob('*.py'):
        assert p.read_bytes() == git('show',P+':developmental_ecology/loom_p/'+p.name)
    assert (D/'configuration.json').read_bytes() == git('cat-file','--filters',P+':developmental_ecology/configuration.json')
    for folder in ('loom_p','loom_commissioning'):
        for p in (D/folder).iterdir():
            if p.suffix in ('.py','.html'): cp(p, 'instrument/developmental_ecology/'+folder+'/'+p.name)
    for n in ('configuration.json','requirements-lock.txt'): cp(D/n, 'instrument/developmental_ecology/'+n)
    samefiles = ['INITIAL_A5.snapshot.json.gz','INITIAL_STATE_SUMMARY.json','CIRCUIT_AND_RENEWAL_RATIONALE.json','VIEWER_RECORD_CONTRACT.md']
    for n in samefiles: cp(H/n,n)
    m['apparatus'] = ai; m['execution']['controller'] = authority.controller_identity('waypoint')
    assert m['execution']['controller']['configuration'] == old['execution']['controller']['configuration']
    assert authority.adapter_identity(m['mode']) == m['execution']['adapter']
    # Verify all actuator arithmetic AST nodes after native stage selection are unchanged,
    # apart from the final time_due arguments now being native indices.
    def command_ast(raw):
        fn = next(n for n in ast.parse(raw).body if isinstance(n,ast.FunctionDef) and n.name=='waypoint_command')
        nodes = fn.body
        start = next(i for i,n in enumerate(nodes) if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='p' for t in n.targets))
        tail = copy.deepcopy(nodes[start:])
        for n in ast.walk(ast.Module(body=tail,type_ignores=[])):
            if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='time_due':
                n.args = [ast.Constant('SCHEDULING_CONTEXT'), ast.Constant('SCHEDULING_DEADLINE')]
        return ast.dump(ast.Module(body=tail,type_ignores=[]),include_attributes=False)
    assert command_ast((H/'instrument/developmental_ecology/loom_commissioning/controllers.py').read_text()) == command_ast((D/'loom_commissioning/controllers.py').read_text())
    controller_ast_identical = True
    newids = copy.deepcopy(idsold)
    newids.update(apparatus=ai, apparatus_commit=APP, worktree=str(W), branch=git('branch','--show-current').decode().strip())
    write('CODE_AND_RUNTIME_IDENTITIES.json',newids)
    sourceids = strict((H/'SOURCE_IDENTITIES.json').read_bytes())
    additions = {
        'A5_REGENERATION_REQUEST.txt': pathlib.Path(r'C:\Users\Jason\.codex\attachments\6b973486-d30d-44ff-962c-fd71fa7cde1e\Pasted text.txt'),
        'clock-correction/CLOCK_SCHEDULING_CORRECTION_REPORT.md': CP/'CLOCK_SCHEDULING_CORRECTION_REPORT.md',
        'clock-correction/NATIVE_INDEX_SCHEDULING_SPECIFICATION.md': W/'docs/developmental_ecology/p_clock_correction_20260926/NATIVE_INDEX_SCHEDULING_SPECIFICATION.md',
        'clock-correction/CHECKPOINT.json': CP/'CHECKPOINT.json',
        'clock-correction/CORRECTION_DETAILS.json': COR/'CORRECTION_DETAILS.json',
        'clock-correction/CLOCK_SCHEDULING_CORRECTION.patch': CP/'CLOCK_SCHEDULING_CORRECTION.patch',
        'clock-correction/PRESERVATION_FINAL.json': COR/'PRESERVATION_FINAL.json',
    }
    for n,p in additions.items():
        assert n not in sourceids
        cp(p,'references/'+n); sourceids[n] = dict(source_path=str(p),sha256=sha(p),bytes=p.stat().st_size)
    write('SOURCE_IDENTITIES.json',sourceids)
    edits = {}
    def document(n, pairs):
        text = (H/n).read_bytes().decode('utf-8'); rows=[]
        for a,b in pairs:
            assert text.count(a)==1,(n,a)
            text = text.replace(a,b)
            rows.append(dict(before=a,after=b,classification=SCHEDULER,reason='Replace obsolete clock-HOLD status/representation only; preserve all prospective physical and interpretation terms.'))
        txt(n,text); edits[n]=rows
    procedures = (H/'PROCEDURES.md').read_text(encoding='utf-8')
    holdparagraph = next(p for p in procedures.split('\n\n') if p.startswith('**A static clock audit'))
    document('PROCEDURES.md',[
        ('# A5 proposed circuit — HOLD, not authorized or ready to launch','# A5 proposed circuit — launch-ready proposal, awaiting Jason authorization'),
        (holdparagraph,'**The reviewed native-index clock correction removes the scheduling blocker.** The unchanged 630-second proposal is bound to apparatus `'+APP+'`. `STATIC_SCHEDULER_COMPATIBILITY.md` records scalar-only checks through native index 63,000. The old object remains HOLD / NON-LAUNCHABLE in `historical-held/`; the new execution grant remains null. No A5 simulation or controller command has been performed.'),
        ('Grid alignment alone does not cure the discovered accumulated-clock issue.','The reviewed scheduler assigns stages and ten-step holds by exact native indices while leaving the continuous physical clock unchanged. Stage-end indices are 9000, 12000, 27000, 30000, 45000, 48000 and 63000; a decision at an interior stage end belongs to the next stage.'),
        ('Subject to a future resolved launch packet and separate genuine authorization:','Subject to separate genuine authorization of this exact regenerated packet:'),
        ('Stop for Jason\'s review of this held proposal and its clock finding.','Stop for Jason\'s authorization of this new exact object. The reviewed correction does not itself authorize A5.'),
    ])
    document('OBSERVATION_AND_INTERPRETATION.md',[
        ('**Held proposal; no A5 measurements yet.**','**Launch-ready proposal awaiting authorization; no A5 measurements yet.**'),
        ('after a separately resolved and authorized launch','after a separately authorized launch'),
        ('record failure or the present static clock incompatibility','record failure or a clock incompatibility'),
        ('The present hold is static apparatus evidence, not an executed A5 outcome.','The historical clock hold remains static apparatus evidence, not an executed A5 outcome.'),
    ])
    document('RESOURCE_PLAN.md',[
        ('**HOLD:** these are costs for the proposed full 630-second case, not a promise that the pinned apparatus can execute it. The static clock incompatibility must be resolved separately first.','**Awaiting authorization:** the clock correction is reviewed and the proposed full 630-second schedule passes scalar preflight. These remain the unchanged A2/A3-based estimates, not a new benchmark or runtime guarantee. The scheduler correction requires no change to the retained numerical projection.'),
        ('No such launcher/monitor is implemented or invoked in this held packet.','No such launcher/monitor is implemented or invoked in this preparation packet. A future separately authorized execution must implement this same administrative accounting before its first world step.'),
    ])
    boundary_old = (H/'REVIEW_AND_EXECUTION_BOUNDARY.md').read_bytes().decode()
    boundary_new = '''# Review and execution boundary

This is a launch-ready proposal awaiting Jason's separate authorization. The canonical object is the complete manifest with only `execution_authority` excluded. It binds one A5 case, original snapshot, phase/prehistory, unchanged route, controller constants and actuator arithmetic, corrected scheduling/code identity, runtime, 630-second horizon, all resource ceilings, recording, observation and interpretation contracts. The execution grant is null and the existing gate rejects it.

The protocol disposition `READY_FOR_JASON_AUTHORIZATION` means packet preparation is complete; it grants no execution. Jason's current request reports the independent disposition FIT FOR A5 LAUNCH-PACKET REGENERATION for apparatus `68db2c581f07200966d699a4f55a65f9b96df1e9`. Earlier workbench navigation and the correction report's pre-review labels are dated history; they were not rewritten. The current user request supplies the later ruling. No live inspection, controller command, world step or simulation RNG draw has occurred in regeneration.

Historical authority `88dd97546d565711a7f852795da7188f551651d0b529f4684b9e4013a5b940f6` remains HOLD / NON-LAUNCHABLE and cannot authorize the corrected instrument. Its exact canonical bytes, manifest, original issue/audit and original documents are retained under `historical-held/`, with large immutable references/cache shared at their original relative locations. `HISTORICAL_PACKET_LAYOUT.json` makes byte-exact reconstruction explicit.

The prospective case is one fresh continuous trajectory only. No retry, resume, extension, route/phase/source replacement, early-success selection, gain change, physical-law/P change, extra case, scientific lifetime, cohort, sweep or useful-learning gate is part of it. Body, source, field, mover and controller history remain continuous between contacts. Ordinary failure and terminal evidence must be preserved. After any future authorized first stop, report from saved evidence and stop.

Before any future authorized first world step, reverify the exact approved object, live checkpoint/source/runtime/dispatch identities, initial snapshot/cache, bound files, empty prospective output and the unchanged 10 GB free-space precondition. Enforce the existing 4-hour runner and 1-hour saved-data allowance, 1.5 GB stream ceiling, 10 GB combined-new-artifact ceiling, 9 GB stop request and 1 GB flush reserve. The resource monitor is an administrative execution wrapper to be supplied only within a separately authorized execution, not a new controller or permission to change its trajectory.

This regeneration uses only source/identity reads, exact copies, harmless scoped access verification, scalar clock arithmetic, pure stage/hold checks, declarative execution/dispatch checks, null-grant denial, canonical hashing and packaging. No production history validator, Engine/Run constructor, live command, replay or prehistory generation is invoked. Existing full regression results are referenced, not rerun. No launch command or grant is supplied. No code modification, Git write, commit, push, PR, merge or workbench navigation edit is part of this task. Stop for Jason's decision.
'''
    document('REVIEW_AND_EXECUTION_BOUNDARY.md',[(boundary_old,boundary_new)])
    resources = strict((H/'RESOURCE_PROJECTION.json').read_bytes())
    resources['status']='Retained A2/A3 measured-basis estimates for the unchanged 630-second proposal under the reviewed scheduler. No new benchmark or A5 run; awaiting authorization.'
    resources['enforcement']=resources['enforcement'].replace('No executable wrapper supplied under HOLD.','No executable wrapper supplied in this preparation packet.')
    write('RESOURCE_PROJECTION.json',resources)
    report,holds = audit(m,clock,controllers)
    write('STATIC_SCHEDULER_COMPATIBILITY.json',report); txt('STATIC_HOLD_SCHEDULE.csv',holds)
    rows = report['boundary_rows']
    lines=['# Static 630-second scheduler compatibility','',
           '**PASS — scalar preflight only; A5 remains unexecuted.**','',
           'All 63,001 native-index positions (including the initial endpoint) pass physical/index consistency. All 6,300 prospective ten-step holds fit their stage and case boundaries. The independent integer interval oracle agrees at every position. Stage ends are 9,000 / 12,000 / 27,000 / 30,000 / 45,000 / 48,000 / 63,000. The final index admits no fresh hold.','',
           'The scalar clock repeatedly adds 0.01 without rounding, resetting or evolving state. Calls are restricted to the corrected pure clock helpers and stage selector. No waypoint command or world-dependent input is calculated. The complete hold table is `STATIC_HOLD_SCHEDULE.csv`; all boundary samples are in the JSON companion.','',
           '| Index | Accumulated scalar time | Nominal time | Stage (zero-based) | Clock allowance | Fresh hold |','|---:|---:|---:|---:|---:|---|']
    for r in rows:
        if r['native_index'] in (26949,26950,26951,26999,27000,27001,30000,45000,48000,63000):
            lines.append(f"| {r['native_index']} | {r['accumulated_scalar_time']!r} | {r['nominal_time']} | {r['stage_zero_based']} | {r['allowance']!r} | {r['fresh_hold_permitted']} |")
    lines += ['', 'At index 26,950 the legitimate accumulated timestamp differs from 269.5 by more than the old fixed 1e-10 threshold, but passes the corrected summation-error bound. At index 27,000 the stage selector owns stage 3 despite the slightly lower physical timestamp; the ten-step hold ends at 27,010, below the next stage end of 30,000. Neither former rejection occurs in the static scheduling predicates.', '',
              'The maximum absolute scalar accumulation discrepancy is '+repr(report['maximum_absolute_accumulation_error'])+' s. At 63,000 the physical/index allowance is '+repr(rows[-1]['allowance'])+' s. It diagnoses clock consistency and never selects a stage. Native 0.01 s, command 10-step, wave 20-step and field cadences remain defined by unchanged code/configuration. No actual field, wave, event or pause/resume operation is tested here; those component/regression results belong to the sealed prior correction review.', '',
              'Scope limit: this proves declarative/native scheduling compatibility for the preserved A5 manifest. It does not prove contact success, renewal use, viability, complete-case runtime, or any physical outcome. Future live startup must still perform the normal identity/cache/state checks after separate authorization.']
    txt('STATIC_SCHEDULER_COMPATIBILITY.md','\n'.join(lines)+'\n')
    for n in ('regenerate.py','static_scheduler_check.py','validate_packet.py'): cp(S/n,n)
    p = m['execution']['procedure']['protocol']
    p['packet_status']='PROPOSED / NOT AUTHORIZED / LAUNCH-READY'
    p['launch_disposition']='READY_FOR_JASON_AUTHORIZATION'; p['launch_ready']=True
    p['reviewed_checkpoints']['apparatus_git_sha']=APP
    p['schedule_interpretation']='Fixed physical target windows owned by exact native indices, no outcome-triggered switch or actual-contact guarantee; one completed return circuit plus second outbound leg.'
    p['record_destination']=str(DEST/'trajectory-001'); p['analysis_destination']=str(DEST/'read-only-review')
    p['launch_preconditions']=[
        'Separate genuine Jason authorization of this new exact canonical object; execution grant remains null during preparation',
        'Corrected apparatus 68db2c581f07200966d699a4f55a65f9b96df1e9 and its bound native-index scheduling implementation; static schedule preflight passes through native index 63000',
        'Before execution reverify exact live identities, dispatch, cache/snapshot/bound files, empty prospective output and the unchanged disk/resource monitor requirements']
    bound = ['PROCEDURES.md','OBSERVATION_AND_INTERPRETATION.md','VIEWER_RECORD_CONTRACT.md','REVIEW_AND_EXECUTION_BOUNDARY.md',
             'SOURCE_IDENTITIES.json','INITIAL_STATE_SUMMARY.json','CODE_AND_RUNTIME_IDENTITIES.json','CIRCUIT_AND_RENEWAL_RATIONALE.json',
             'RESOURCE_PROJECTION.json','RESOURCE_PLAN.md','STATIC_SCHEDULER_COMPATIBILITY.json','STATIC_SCHEDULER_COMPATIBILITY.md',
             'STATIC_HOLD_SCHEDULE.csv','static_scheduler_check.py','regenerate.py','validate_packet.py',
             'historical-held/AUTHORITY_OBJECT.canonical.json','historical-held/FILE_MANIFEST.json',
             'historical-held/OPEN_ISSUE_A5_CLOCK.md','historical-held/CLOCK_AUDIT.json']
    p['bound_files']={n:sha(OUT/n) for n in bound}
    authority.validate_execution(m,complete=True); authority.validate_dispatch(m,vars(runner))
    try: contract.authorize_execution(m)
    except ValueError as exc: denial=str(exc)
    else: raise AssertionError('null grant accepted')
    assert denial=='commissioning execution is not authorized'
    obj=authority.execution_object(m); h=authority.execution_sha256(m)
    assert h != OLDHASH and m['execution_authority'] is None
    write('A5_MANIFEST.json',m); write('AUTHORITY_OBJECT.json',obj)
    (OUT/'AUTHORITY_OBJECT.canonical.json').write_bytes(authority.canonical(obj)); txt('AUTHORITY_SHA256.txt',h+'\n')
    semantic = dict(historical_authority_sha256=OLDHASH, new_authority_sha256=h,
                    classification_labels=[IDENTITY,SCHEDULER,'UNEXPECTED SEMANTIC CHANGE'],
                    unexpected_semantic_changes=[],document_replacements=edits,
                    byte_identical_scientific_files=samefiles,
                    note='Field-level exact comparison; JSON pointers use RFC6901 escaping. Document edits are exact before/after replacements checked against original bytes. Every unspecified manifest field is unchanged. New audit/report/hash utilities are preparation evidence, never trajectory definitions.')
    allowed = {'/apparatus':IDENTITY,'/execution/controller/implementation':IDENTITY,
               '/execution/procedure/protocol/reviewed_checkpoints/apparatus_git_sha':IDENTITY,
               '/execution/procedure/protocol/bound_files':IDENTITY,
               '/execution/procedure/protocol/record_destination':IDENTITY,
               '/execution/procedure/protocol/analysis_destination':IDENTITY}
    allowed.update({'/execution/procedure/protocol/'+n:SCHEDULER for n in ('packet_status','launch_disposition','launch_ready','schedule_interpretation','launch_preconditions')})
    semantic['manifest_fields']=classify(diffs(old,m),allowed,'Corrected apparatus identity/evidence binding or reviewed native-index scheduling preflight; no ecological term changed.')
    semantic['supporting_json_fields']={
        'CODE_AND_RUNTIME_IDENTITIES.json':classify(diffs(idsold,newids),{'/apparatus':IDENTITY,'/apparatus_commit':IDENTITY,'/worktree':IDENTITY,'/branch':IDENTITY},'Bind the actual corrected checkpoint; P/configuration/runtime unchanged.'),
        'RESOURCE_PROJECTION.json':classify(diffs(strict((H/'RESOURCE_PROJECTION.json').read_bytes()),resources),{'/status':SCHEDULER,'/enforcement':SCHEDULER},'Remove obsolete clock HOLD wording only; every measurement, estimate and cap remains exact.'),
        'SOURCE_IDENTITIES.json':classify(diffs(strict((H/'SOURCE_IDENTITIES.json').read_bytes()),sourceids),{'/'+n.replace('~','~0').replace('/','~1'):IDENTITY for n in additions},'Add exact current ruling and corrected-instrument provenance; original reference identities unchanged.'),
    }
    changed_sources=[]
    for n,v in ai['files'].items():
        oldv=old['apparatus']['files'].get(n)
        if oldv != v:
            assert n in {'clock.py','controllers.py','authority.py','pending.py','runner.py','validators.py'},n
            changed_sources.append(dict(file=n,before_sha256=oldv,after_sha256=v,classification=SCHEDULER,reason='Previously reviewed native-index correction at the exact requested checkpoint; this preparation makes no code changes.'))
    semantic['corrected_instrument_sources']=changed_sources
    semantic['unchanged_verifications']=dict(horizon_seconds=630,source_order=[0,1,0,1],stages_exact=True,
        initial_snapshot_exact=True,phase_prehistory_exact=True,P_configuration_world_exact=True,
        controller_constants_exact=True,actuator_arithmetic_AST_exact_except_scheduler_context=controller_ast_identical,
        renewal_expenditure_exact=True,observation_definitions_and_interpretation_limits_exact_except_clock_status=True,
        recording_contract_exact=True,resource_measurements_estimates_and_ceilings_exact=True,runtime_exact=True)
    write('SEMANTIC_DIFF.json',semantic)
    md=['# Held versus regenerated A5 — semantic comparison','',
        '**No unexpected semantic change.** Every manifest field change is listed below; exact before/after values, supporting JSON changes and complete document replacement spans are in `SEMANTIC_DIFF.json`. The portable validator independently reproduces those diffs and asserts all other scientific/trajectory fields unchanged.','',
        'Historical HOLD object: `'+OLDHASH+'`. New proposed object: `'+h+'`. Both grants are null; the former remains non-launchable.','',
        'Preserved: 630 s; source order 0→1→0→1; all seven points, press forces and physical deadlines; exact A1/A2 snapshot, phase and prehistory; all controller constants and actuator arithmetic; P, configuration, world/resource laws; full-fidelity observer/recorder contract; all observation definitions and interpretation limits; every numerical resource projection and cap.','',
        'Only clock-status phrases change in the observation table; its outcome predicates and claim limits are unchanged. The prospective output namespace follows the corrected worktree/checkpoint. Original cache identity and original path remain unchanged.','',
        '| Changed manifest field | Classification |','|---|---|']
    md += ['| `'+r['path']+'` | '+r['classification']+' |' for r in semantic['manifest_fields']]
    md += ['', 'Document replacement spans and supporting JSON leaves are classified individually in the JSON. Old clock/preparation utilities and status documents are archived, not rewritten or silently treated as current. New scalar evidence replaces obsolete HOLD evidence in the new binding. Current preparation reports and checksums are derived metadata, sealed by `FILE_MANIFEST.json`; they do not authorize execution.', '',
           'The exact old packet can be reconstructed from `HISTORICAL_PACKET_LAYOUT.json`; every original file is verified against its original manifest. No prior A1–A4 result is reinterpreted. The prior correction review records 5,579 saved stage decisions with no disagreement; that is prior evidence, not a new replay in this task.']
    txt('SEMANTIC_DIFF.md','\n'.join(md)+'\n')
    layout={n:('historical-held/'+n if (OUT/'historical-held'/n).exists() else n) for n in list(oldfm['files'])+['FILE_MANIFEST.json']}
    write('HISTORICAL_PACKET_LAYOUT.json',dict(authority_sha256=OLDHASH,status='HOLD / NON-LAUNCHABLE',files=layout))
    prep={k:0 for k in ('world_steps','field_steps','neural_steps','controller_commands','simulation_RNG_draws','new_prehistory_steps','Engine_constructors','Run_constructors','sensor_evaluations','trial_routes','trial_phases','replays')}
    prep.update(forbidden_calls=FORBIDDEN,profiled_loom_calls=dict(sorted(CALLS.items())),null_grant_denial=denial,
                production_history_validation_executed=False,prospective_output_absent=not DEST.exists(),
                A5_physical_outcome=None,code_modifications=0,git_writes=0,
                execution_validation_pass=True,live_dispatch_identity_check_pass=True,
                actual_context='Local Windows code worktree and pinned installed Python; no cloud runtime substitute.',
                guard_scope='All calls into loom_p and loom_commissioning profiled against a pure metadata/clock allowlist. No Engine/Run, command, world, sensor, neural, physics, chemistry, reconstruction or simulation RNG method was permitted. Scalar checks do not instantiate simulation RNG streams.')
    assert FORBIDDEN==[] and not DEST.exists()
    write('PREPARATION_CHECKS.json',prep)
    sys.setprofile(None)
    after={str(p):sha(p) for p in sorted(preserved)}; assert before==after
    assert git('rev-parse','HEAD').decode().strip()==APP and not git('status','--porcelain').strip()
    write('HASH_BEFORE.json',before); write('HASH_AFTER.json',after)
    write('PRESERVATION.json',dict(all_preserved_hashes_match=True,files_checked=len(before),worktree_clean_after=True,
          apparatus_commit=APP,branch=newids['branch'],historical_local_and_workbench_hold_unchanged=True,
          held_zip_sha256=sha(WBH.parent/'A5_LAUNCH_PACKET_HOLD.zip'),P_configuration_world_unchanged=True,
          no_simulation_execution=True,no_production_code_modification=True,no_Git_write=True))
    txt('README.md',f'''# A5 regenerated launch packet — awaiting Jason authorization

**Launch-ready proposal only. A5 has not been executed. Execution grant: null.**

New canonical authority SHA-256:

`{h}`

P: `{P}`  
Corrected apparatus: `{APP}`  
Local branch: `{newids['branch']}`  
Worktree: `{W}`

The existing 630-second physical witness is unchanged. It begins at (6,3), facing west, E=0.7/I=1, using the exact healthy A1/A2 snapshot and existing phase-specific prehistory. The privileged external controller approaches source 0, leaves at 90 s toward the midpoint, targets source 1 at 120 s, leaves at 270 s, targets source 0 at 300 s, leaves at 450 s, and targets source 1 again at 480 s until the 630 s ceiling. These are fixed target windows, not guaranteed arrival or contact times. One return circuit and a second outbound leg pose two renewed revisit opportunities. P remains inactive. There is no learning, perception, indefinite-support or scientific-efficacy claim.

- `PROCEDURES.md`: complete unchanged route and physical rationale.
- `A5_MANIFEST.json`, `AUTHORITY_OBJECT.canonical.json`, `AUTHORITY_OBJECT.json`: exact proposed scope and identities.
- `SEMANTIC_DIFF.md` / `.json`: every changed manifest field, supporting metadata and exact document replacement spans; no unexpected semantic changes.
- `STATIC_SCHEDULER_COMPATIBILITY.md` / `.json` and `STATIC_HOLD_SCHEDULE.csv`: 63,001 scalar clock points and 6,300 prospective holds pass; both former rejection points are absent.
- `RESOURCE_PLAN.md` / `RESOURCE_PROJECTION.json`: unchanged A2/A3 basis; approximately 123.44–125.31 recorder wall minutes and 444.52–474.24 MB stored trajectory, with 4 h runner + 1 h saved-data reporting, 1.5 GB uncompressed-stream and 10 GB combined-new-artifact ceilings. These are extrapolations, not a benchmark of the corrected apparatus.
- `OBSERVATION_AND_INTERPRETATION.md`, `VIEWER_RECORD_CONTRACT.md`: retained measurement/claim limits and passive-record requirements.
- `PREPARATION_CHECKS.json`, `PRESERVATION.json`: zero world, command, simulation RNG, replay and new-prehistory execution; unchanged P/configuration/world; clean corrected worktree; preserved local and Workbench held packet.
- `historical-held/`, `HISTORICAL_PACKET_LAYOUT.json`: exact historical HOLD object `{OLDHASH}` and all original metadata. Large immutable original references/cache are shared at their original relative paths and verified against the historical manifest.

The attached current user request supplies the later independent-review disposition FIT FOR A5 LAUNCH-PACKET REGENERATION. Earlier workbench navigation and correction-report pre-review labels remain untouched historical records. This package changes no canon or research status navigation.

This is a portable review packet, not a bundled Python installation. `instrument/` contains exact source/configuration bytes; `CODE_AND_RUNTIME_IDENTITIES.json` binds the installed runtime. `validate_packet.py <folder-or-zip>` performs stdlib-only saved-byte checks. `regenerate.py` is the recorded authoring utility with original local source paths, not an execution launcher. No runnable A5 launcher or grant is supplied.

Not tested here: A5 motion, contact, renewed intake, reserve trajectory, survival, controller effectiveness, full-horizon runtime, or ecological outcomes. Existing correction regressions are referenced, not rerun. A later authorized execution must reverify live identities, snapshot/cache and empty output, enforce the same resource monitor, preserve all failure evidence, report without patch/retry/resume/tuning/extension/substitution and stop.

**Stop for Jason's separate authorization of this new exact hash.**
''')
    payloads={p.relative_to(OUT).as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted(OUT.rglob('*')) if p.is_file()}
    write('FILE_MANIFEST.json',dict(authority_sha256=h,files=payloads))
    result=verify(lambda n:(OUT/n).read_bytes(),list(payloads)+['FILE_MANIFEST.json'])
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
