"""Preserve ended FULL-RAW metadata and opaque artifacts; no evaluation or world use."""
import datetime,hashlib,json,pathlib,shutil,urllib.request
B=pathlib.Path(__file__).resolve().parent;R=B.parent;run=B/'private/runs/B1-FULL-RAW'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write_new(p,v):
    with p.open('x',encoding='utf-8') as f:json.dump(v,f,indent=2,ensure_ascii=False,allow_nan=False);f.write('\n')
with urllib.request.urlopen('http://127.0.0.1:51048/session',timeout=15) as response:s=json.load(response)
assert s['lifecycle']=='ended' and s['display_condition']=='none'
last=s['sensors']['history'][-1];commands=len(s['sensors']['own_commands'])
assert last['native_index']==2020 and commands==202
# Only administrative completeness, counts and file identities are consulted.
# No stop-cause interpretation, final-state access, trajectory decoding or evaluator invocation.
m=js(run/'manifest.json')
assert m['complete'] is True and m['session_counters']['advanced']==2020 and m['final_time']==last['time']
for n,v in m['files'].items():
    p=run/n;assert p.parent==run and p.is_file()
    assert sha(p)==v['sha256'] and p.stat().st_size==v['bytes']
assert {p.name for p in run.iterdir() if p.is_file()}==set(m['files'])|{'manifest.json'}
inventory={p.relative_to(B/'private').as_posix():dict(sha256=sha(p),bytes=p.stat().st_size) for p in sorted((B/'private').rglob('*')) if p.is_file()}
write_new(B/'private/COMPLETED_ATTEMPT_FILE_MANIFEST.json',dict(files=inventory,excludes_self=True))
stamp=datetime.datetime.now(datetime.timezone.utc).isoformat()
write_new(B/'FULL_RAW_OPERATOR_COMPLETION.json',dict(recorded_utc=stamp,case='B1-FULL-RAW',attempt=4,
 authority_sha256='936cd43b20c84378c3d7a2e99825fb87029c873872db6e504279ee7a931ce901',
 checkpoint='b684912eaf7811cd318ee94c77172aca790f3a0d',user_report='Ok, thats finished.',
 observed_lifecycle='ended',simulated_seconds=last['time'],native_steps=2020,human_commands=commands,assistant_commands=0,
 reached_30_second_ceiling=False,complete_record=True,record_files_verified=len(m['files']),
 run_manifest_sha256=sha(run/'manifest.json'),private_inventory_sha256=sha(B/'private/COMPLETED_ATTEMPT_FILE_MANIFEST.json'),
 evaluator_results_inspected=False,private_stop_cause_interpreted=False,interaction_outcome='WITHHELD PENDING PAIRED-TRIAL DISPOSITION',
 chemistry_hidden_authorized=False,chemistry_hidden_executed=False,pair_abandoned=False,
 new_simulation_steps=0,new_controller_commands=0,retry_or_continuation=False,
 service='Existing service retained as an irreversible ended, read-only operator-history display; no active simulation.'))
write_new(B/'OPERATOR_DEBRIEF_AND_PROPOSALS.json',dict(recorded_utc=stamp,
 user_comment_verbatim="Ok, thats finished. \nI can see that without any starting position whatsoever this will be a challenge for the bug to find anything of relevance.\nI can see two options here. We could make a much smaller world with more availablity of resources so it can pick up signals quicker. \nOr we run a batch of bugs, if we go with a high enough number then one of them will likely learn. We can use that as the base bug. Then thats our 'instinct' equipped bug.",
 classification='Operator experience and Jason-proposed future directions; not authorization of a world change, cohort, state inheritance or new execution.',
 proposed_directions=['Smaller world with greater resource availability','Larger population followed by retaining an apparently learned individual as a base bug'],
 evidence_scope='Human external-controller FULL-RAW attempt; P learning was not active or tested.',
 proposals_implemented=False,configuration_changed=False,cohort_started=False,learned_state_selected_or_transferred=False,
 hidden_evaluator_information_disclosed=False))
state=js(B/'STATE.json');shutil.copyfile(B/'STATE.json',B/'STATE_AT_INITIAL_HANDOFF.preserved.json')
state.update(status='ENDED / COMPLETE RECORD PRESERVED / PAIRED EVALUATION WITHHELD',live_services=1,active_simulations=0,
 simulation_steps=2020,controller_commands=commands,simulated_seconds=last['time'],assistant_commands=0,
 evaluator_release_allowed=False,chemistry_hidden_authorized=False,completion_record='FULL_RAW_OPERATOR_COMPLETION.json',
 service_mode='ENDED / READ-ONLY OPERATOR HISTORY',status_observed_utc=stamp)
(B/'STATE.json').write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(ended=True,simulated_seconds=last['time'],native_steps=2020,human_commands=commands,
 complete_record=True,files_verified=len(m['files']),new_execution=0,evaluator_results_inspected=False)))
