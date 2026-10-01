"""Preserve an already-ended run; hash opaque records without replay/evaluation."""
import datetime,hashlib,json,pathlib,shutil,urllib.request
R=pathlib.Path(__file__).resolve().parent.parent
B=R/'b1_execution_20260929_restart_01';run=B/'private/runs/B1-FULL-RAW'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_text(json.dumps(v,indent=2,allow_nan=False)+'\n',encoding='utf-8')
receipt=B/'PREFIX_CLOSURE_AND_COLOUR_LABEL_AUTHORIZATION.json'
assert not receipt.exists()
with urllib.request.urlopen('http://127.0.0.1:56824/session',timeout=15) as response:
    s=json.load(response)
assert s['lifecycle']=='ended'
history=s['sensors'];last=history['history'][-1]
assert last['native_index']==120 and len(history['own_commands'])==12
m=js(run/'manifest.json')
assert m['complete'] is True and m['session_counters']['advanced']==120
assert m['final_time']==last['time']
for n,v in m['files'].items():
    p=run/n;assert p.parent==run and sha(p)==v['sha256'] and p.stat().st_size==v['bytes']
inventory={p.relative_to(B/'private').as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted((B/'private').rglob('*')) if p.is_file()}
write(B/'private/CLOSED_PREFIX_FILE_MANIFEST.json',dict(files=inventory,excludes_self=True))
shutil.copyfile(B/'STATE.json',B/'STATE_AT_INITIAL_PREPARATION.preserved.json')
write(receipt,dict(recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),case='B1-FULL-RAW',attempt=3,
 prior_authority='45f2349183579ed478e4c5582cdb70ba6619e06769ccfaad05f2dd36d26b173d',
 prior_checkpoint='1060a17e3dd14c6361f6f15c95bb58fad3110ffc',
 user_request="Write the coordinate label in the same colour as the graph. Don't add a separate key.",
 user_confirmation='yes',confirmation_scope='Close and preserve this 1.2-second attempt, then prepare the revised launch for authorization.',
 observed_lifecycle='ended',simulated_seconds=last['time'],native_steps=120,human_commands=12,assistant_commands=0,
 complete_record=True,run_manifest_sha256=sha(run/'manifest.json'),private_inventory_sha256=sha(B/'private/CLOSED_PREFIX_FILE_MANIFEST.json'),
 closure='Explicit operator withdrawal at paused boundary through existing /end lifecycle; no /command request.',
 permitted_readings_and_movement_history_seen=True,whole_start_unseen_naivety_claim_permitted=False,
 evaluator_feedback_released=False,hidden_trial_authorized=False,replacement_trial_authorized=False,
 new_simulation_steps=0,new_controller_commands=0,new_worlds_loaded=0,new_timers_started=0))
print(json.dumps(dict(ended=True,native_steps=120,human_commands=12,simulated_seconds=last['time'],complete_record=True,record_files_verified=len(m['files']),private_files_preserved=len(inventory))))
