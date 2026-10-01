"""Inert manifest/type compatibility only; no initial state deserialization."""
import copy,hashlib,json,pathlib,sys
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
D=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926/developmental_ecology'
H=ROOT/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02'
sys.path.insert(0,str(D))
from loom_commissioning.authority import make_execution,validate_execution
from loom_commissioning.contract import apparatus_identity
from loom_commissioning import clock
def read(p):return json.loads(p.read_bytes())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
index=read(H/'B1_OPERATOR_REVIEW/CASE_AND_AUTHORITY_INDEX.json')['cases']
private=H/'B1_PRIVILEGED_EVALUATOR_HOLD'
cases={x['case']:read(private/'case-manifests'/(x['case']+'.json')) for x in index}
full=cases['B1-FULL-RAW'];hidden=cases['B1-CHEMISTRY-HIDDEN']
assert {k for k in full if full[k]!=hidden[k]}=={'case_id','execution'}
assert {k for k in full['execution'] if full['execution'][k]!=hidden['execution'][k]}=={'display_intervention'}
assert full['initial_state']==hidden['initial_state'] and full['duration_seconds']==hidden['duration_seconds']==30
rows=[]
for name,m in cases.items():
    assert m['execution_authority'] is None
    # Disposable in-memory type check. No serialization/hash of a regenerated
    # execution object, no grant, no Run, and no load of any sealed snapshot.
    candidate=copy.deepcopy(m);old=m['execution'];resource=old['resources']
    candidate['apparatus']=apparatus_identity()
    candidate['execution']=make_execution(m['mode'],m['controller'],protocol=copy.deepcopy(old['procedure']['protocol']),
        storage_limit=resource['storage_limit_bytes'],wall_limit=resource['wall_limit_seconds'],
        display='chemistry_hidden' if name=='B1-CHEMISTRY-HIDDEN' else 'none')
    validate_execution(candidate,complete=True)
    assert clock.case_end(candidate)==round(m['duration_seconds']*100)
    assert all(clock.hold_steps(candidate,i)==10 for i in range(0,clock.case_end(candidate),10))
    row=next(x for x in index if x['case']==name)
    snapshot=private/'initial-states'/('B1-PAIR-INITIAL.snapshot.json.gz' if name.startswith('B1-') else name+'.snapshot.json.gz')
    assert sha(snapshot)==row['initial_snapshot_sha256']
    rows.append(dict(case=name,horizon_seconds=m['duration_seconds'],unchanged_snapshot_sha256=row['initial_snapshot_sha256'],
        controller='sensor_human',display_representable=True,grid_and_hold_representable=True,execution_grant=None))
before=read(S/'HELD_PRESERVATION_BEFORE.json')
assert all(sha(pathlib.Path(p))==h for p,h in before.items())
result=dict(held_review_hash='45d71cd121f823368401b11c4a1010d509af3224f49168ad528653274d0e7543',
    static_only=True,held_source_files_unchanged=len(before),pair_complete_initial_state_identical=True,
    paired_semantic_difference='operator display deprivation only; case identities differ',cases=rows,
    positive_controls={'left_right':'All actual light/chemistry coordinates retained in full-raw practice.',
        'command_achieved':'Seven real proprioception channels, actual paired commands and ordered native history retained.',
        'contact_onset':'All eight actual native contact channels retained.',
        'gentle_hold':'Same actuators, 0.1 s holds, native contact/proprioception and 5 Hz E/I; no servo added.'},
    physical_raw_recording='Shared full 29-coordinate SensorHistory/native physical recording; only copied operator view is projected.',
    no_snapshot_loaded=True,no_controller_or_world_invoked=True,new_launch_objects_saved=0,new_execution_authorities=0,
    interpretation='Type/identity compatibility only. No demonstration, human outcome, independent closure or B1 launch fitness claimed.')
(S/'STATIC_HELD_COMPATIBILITY.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print('Six held case specifications statically expressible; exact snapshots and horizons preserved. No new launch authority generated.')
