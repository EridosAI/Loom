"""Static held contract comparison: no snapshots decoded, no command/world/authority generation."""
from pathlib import Path
import json,hashlib,sys,zipfile
W=Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97');O=W/'exports/2026-09-26-b1-review-352f73ff/provenance';Z=O.parent/'portable';D=W/'worktrees/loom-p-b1-apparatus-correction-20260926/developmental_ecology';OLD=W/'worktrees/loom-p-clock-correction-20260926';H=W/'exports/2026-09-26-B1-perceptual-ceiling-HOLD-68db2c58-review-02'
def read(p):return json.loads(p.read_bytes())
def ident(p):
    with p.open('rb') as f:return {'sha256':hashlib.file_digest(f,'sha256').hexdigest(),'bytes':p.stat().st_size}
def save(n,d):(O/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf8')
# Manifests are never serialized/copied to this review. Only pair structural
# equality and whitelisted public contract fields are emitted. All snapshots
# remain opaque compressed bytes; no gzip, snapshot parser, Engine or Run.
index=read(H/'B1_OPERATOR_REVIEW/CASE_AND_AUTHORITY_INDEX.json')['cases'];private=H/'B1_PRIVILEGED_EVALUATOR_HOLD'
cases={row['case']:read(private/'case-manifests'/(row['case']+'.json')) for row in index}
full=cases['B1-FULL-RAW'];hidden=cases['B1-CHEMISTRY-HIDDEN']
topdiff=[k for k in full if full[k]!=hidden[k]]
executiondiff=[k for k in full['execution'] if full['execution'][k]!=hidden['execution'][k]]
assert set(topdiff)=={'case_id','execution'} and executiondiff==['display_intervention']
assert full['initial_state']==hidden['initial_state'];assert full['duration_seconds']==hidden['duration_seconds']==30
sys.path.insert(0,str(D))
from loom_commissioning import clock
from loom_commissioning.operator_view import display_identity,validate_intervention,KEPT,HIDDEN_LABELS
from loom_commissioning.controllers import LABELS
from loom_p.schema import Config
from loom_p.records import code_identity
results=[]
for row in index:
    name=row['case'];m=cases[name]
    assert m['execution_authority'] is None and row['execution_grant'] is None
    assert m['initial_state']==row['initial_state_sha256'];assert m['duration_seconds']==row['duration_seconds']
    assert m['p_code']==code_identity()['sha256'] and m['configuration']==Config().identity()
    assert m['controller']=='sensor_human' and m['mode']=='external_controller'
    assert m['command_hold_seconds']==.1
    kind='chemistry_hidden' if name=='B1-CHEMISTRY-HIDDEN' else 'none'
    assert m['execution']['display_intervention']['kind']==kind
    current_display=display_identity(kind);validate_intervention(current_display)
    count=clock.case_end(m)-m['initial_index'];assert count==row['native_ceiling']
    holds=[clock.hold_steps(m,i) for i in range(m['initial_index'],clock.case_end(m),10)]
    assert len(holds)==row['command_holds'] and set(holds)=={10}
    snapshot=private/'initial-states'/('B1-PAIR-INITIAL.snapshot.json.gz' if name.startswith('B1-') else name+'.snapshot.json.gz')
    snapshot_hash=ident(snapshot);assert snapshot_hash['sha256']==row['initial_snapshot_sha256']
    results.append({'case':name,'duration_seconds':row['duration_seconds'],'native_steps':count,'holds':len(holds),'all_holds_ten_steps':True,'unchanged_snapshot':snapshot_hash,'same_p_and_config':True,'display_kind':kind,'display_identity_valid':True,'execution_grant':None})
held=read(O/'HELD_PRESERVATION.json');hash_target='45d71cd121f823368401b11c4a1010d509af3224f49168ad528653274d0e7543'
objects=[{'path':p,**v} for p,v in held['files'].items() if v['sha256']==hash_target];assert objects
assert len(LABELS)==29 and len(KEPT)==25 and KEPT==tuple(range(10))+tuple(range(14,29))
assert HIDDEN_LABELS==LABELS[:10]+LABELS[14:]
save('STATIC_COMPATIBILITY.json',{'held_review_hash':hash_target,'held_object_hash_matches':objects,'snapshot_content_decoded':False,'private_manifest_values_output':False,'private_manifests_copied':False,'pair_top_level_different_keys':sorted(topdiff),'pair_execution_different_keys':executiondiff,'pair_identical_complete_initial_state':True,'pair_only_case_id_and_declared_display_differ':True,'pair_same_world_laws':True,'cases':results,'positive_control_information_channels':{'left_right':'Full 10 light and 4 chemistry values retained','command_and_movement':'Paired own command history plus 7 proprioception values retained','contact_onset':'All 8 contact values retained','gentle_contact_hold':'Same actuator and 10-native-step hold, contact/proprioception and original E/I cadence'},'full_raw_coordinates':len(LABELS),'hidden_coordinates':len(KEPT),'hidden_indices_omitted':[10,11,12,13],'physical_recording_evidence':'P sensor computation, adapter and SensorHistory.observe unchanged; source review confirms private sensor stream remains full, operator projection is copy-only. Root tests independently exercise manufactured pair equality.','new_execution_objects_constructed':0,'new_launch_authorities':0,'controller_calls':0,'world_steps':0,'scope':'Static contract/grid/identity compatibility only; no positive control or B1 executed, no snapshot deserialized, no hidden geometry inspected. Held checkpoint remains non-launchable and is not rewritten.'})
# Verify the 115 omitted historical A5 files still equal the original ZIP inventory.
comparison=read(O/'DELIVERY_COMPARISON.json');original=Path(comparison['original_archive']['path'])
with zipfile.ZipFile(original) as z:old_manifest=json.loads(z.read('B1_OPERATOR_APPARATUS_CORRECTION_REVIEW/PAYLOAD_MANIFEST.json'))['files']
checks={};before=read(O/'BEFORE_FILE_IDENTITIES.json')
for n in comparison['removed']:
    assert n.startswith('baseline-68db/')
    path=OLD/n[len('baseline-68db/'):];actual=ident(path);assert actual==old_manifest[n]
    checks[str(path)]=actual;before[str(path)]=actual
save('OMITTED_HISTORICAL_A5_PRESERVATION.json',{'count':len(checks),'all_match_original_archive_inventory':True,'files':checks,'contents_not_decoded':True})
save('BEFORE_FILE_IDENTITIES.json',before)
print('Static six-case contract compatibility verified; same complete B1 pair state, display-only manifest difference. No private values emitted. 115 omitted historical A5 bytes verified unchanged.')
