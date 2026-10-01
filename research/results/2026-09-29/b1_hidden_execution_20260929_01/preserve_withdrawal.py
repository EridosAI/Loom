"""Close-custody verification only; no simulation, trajectory decoding or evaluation."""
import datetime,hashlib,json,pathlib,shutil
B=pathlib.Path(__file__).resolve().parent;R=B.parent
FULL=R/'b1_execution_20260929_colours_01';RUN=B/'private/runs/B1-CHEMISTRY-HIDDEN'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write_new(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2,allow_nan=False);f.write('\n')
withdrawal=read(B/'WITHDRAWAL_RECEIPT.json')
assert withdrawal['prior_lifecycle']=='prepared' and withdrawal['final_lifecycle']=='ended'
assert withdrawal['native_steps']==withdrawal['commands']==withdrawal['simulated_seconds']==0
receipt=read(RUN/'manifest.json')
assert receipt['complete'] is True and receipt['final_time']==0 and receipt['session_counters']['advanced']==0
for n,v in receipt['files'].items():
    p=RUN/n;assert p.parent==RUN and sha(p)==v['sha256'] and p.stat().st_size==v['bytes']
full_inventory=read(FULL/'private/COMPLETED_ATTEMPT_FILE_MANIFEST.json')['files']
for n,v in full_inventory.items():assert sha(FULL/'private'/n)==v['sha256'] and (FULL/'private'/n).stat().st_size==v['bytes']
files={p.relative_to(B/'private').as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted((B/'private').rglob('*')) if p.is_file()}
write_new(B/'private/WITHDRAWN_FILE_MANIFEST.json',dict(files=files,excludes_self=True))
write_new(B/'WITHDRAWAL_PRESERVATION.json',dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
 complete_zero_step_record=True,run_manifest_sha256=sha(RUN/'manifest.json'),private_inventory_sha256=sha(B/'private/WITHDRAWN_FILE_MANIFEST.json'),
 hidden_record_files_verified=len(receipt['files']),full_raw_record_files_verified=len(full_inventory),
 full_raw_records_byte_unchanged=True,full_raw_reinterpreted=False,
 evaluator_state_inspected=False,trajectory_streams_decoded=False,stop_cause_interpreted=False,
 source_or_configuration_changed=False,new_simulation_steps=0,new_controller_commands=0,
 grant='Historical authorization preserved, then withdrawn by Jason; no further invocation permitted.',
 human_pair='Closed administratively with CHEMISTRY-HIDDEN withdrawn before start; no paired perceptual conclusion assigned.'))
shutil.copyfile(B/'STATE.json',B/'STATE_BEFORE_WITHDRAWAL.preserved.json')
state=read(B/'STATE.json')
state.update(status='AUTHORIZED-BUT-NOT-EXECUTED / WITHDRAWN AT JASON DIRECTION',active_simulations=0,
 simulation_steps=0,controller_commands=0,simulated_seconds=0,chemistry_hidden_authorized=False,
 historical_grant_preserved=True,execution_authorization_withdrawn=True,evaluator_release_allowed=False,
 withdrawal_record='WITHDRAWAL_RECEIPT.json',preservation_record='WITHDRAWAL_PRESERVATION.json',
 service_mode='ENDED / AWAITING SERVICE RETIREMENT',status_observed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(B/'STATE.json').write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(withdrawn=True,complete_zero_step_record=True,full_raw_byte_unchanged=True,
 evaluator_state_inspected=False,record_files_verified=len(receipt['files']))))
