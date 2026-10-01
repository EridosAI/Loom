"""Closed-record review and criterion correction only. No simulation imports."""
import datetime, gzip, hashlib, json, math, os, subprocess
from pathlib import Path

S=Path(__file__).resolve().parent; ROOT=S.parent
A=S/'PC-HOLD-attempt-002'; R=S/'runs/PC-HOLD-attempt-002'
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926'; D=W/'developmental_ecology'
P=ROOT/'exports/2026-09-26-B1-regenerated-352f73ff/B1_OPERATOR_PACKET'

def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):
    with gzip.open(p,'rt',encoding='utf-8') as f:return [json.loads(x) for x in f if x.strip()]
def write_new(p,x):
    with p.open('x',encoding='utf-8') as f:json.dump(x,f,indent=2,ensure_ascii=False);f.write('\n')
def verify_run(path):
    m=read(path/'manifest.json'); assert m['complete']
    for name,item in m['files'].items():
        p=path/name
        assert p.parent.resolve()==path.resolve()
        assert p.stat().st_size==item['bytes'] and sha(p)==item['sha256']
    return m

at=datetime.datetime.now(datetime.timezone.utc).isoformat()
m=verify_run(R); prior=verify_run(S/'runs/PC-HOLD'); contact_manifest=verify_run(S/'runs/PC-CONTACT')
assert m['stop_cause']=='operator_withdrawal' and m['contract']['case_id']=='PC-HOLD'
assert m['contract']['initial_state']==prior['contract']['initial_state']
assert m['contract']['execution_authority']['approved_execution_sha256']=='ac1c5615c2c99ebe2524e3648b81003d7eeb42f1b54493212afd8d3cb83d719f'
assert sha(A/'approval.request.json')==m['contract']['execution_authority']['request_sha256']
assert m['contract']['execution']==prior['contract']['execution']
assert not (A/'RESULT.json').exists() and not (S/'PC-CONTACT.ASSESSMENT_CORRECTION.json').exists()

env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
git=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
assert subprocess.check_output(git+['rev-parse','HEAD'],env=env).decode().strip()=='352f73fffa6d9781eae8aa38e708a9a05669588f'
assert subprocess.check_output(git+['status','--porcelain'],env=env)==b''
for name,digest in m['code']['files'].items():assert sha(D/'loom_p'/name)==digest
for name,digest in m['contract']['apparatus']['files'].items():assert sha(D/'loom_commissioning'/name)==digest
for name,digest in m['contract']['execution']['procedure']['protocol']['bound_documents'].items():assert sha(P/name)==digest

with gzip.open(R/'initial.restart.json.gz','rt',encoding='utf-8') as f:restart=json.load(f)
assert hashlib.sha256(json.dumps(restart['state'],separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()==restart['sha256']
attrs=dict(dict(restart['state']['$dict'])['engine']['attrs']['$dict'])
c=dict(attrs['c']['attrs']['$dict']); body=dict(attrs['body']['attrs']['$dict'])
assert c['stress_threshold']==.25
events=rows(R/'events.jsonl.gz'); native=rows(R/'native.jsonl.gz'); commands=rows(R/'controller.jsonl.gz')
assert len(native)==m['session_counters']['advanced']==150
assert len(commands)==m['records']['controller']==15
assert [x['native_index'] for x in native]==list(range(1,151))
intervals=[]; impacts=[]
for e in events:
    positive=[x for x in e['contacts'] if x['impulse']>0]
    if e['impact'] and positive:impacts.append(e)
    if e['duration']<=0:continue
    for ct in e['contacts']:
        assert math.isclose(ct['force'],ct['impulse']/e['duration'],rel_tol=0,abs_tol=c['arithmetic_tol'])
    expected=c['damage_per_impulse']*sum(max(x['impulse']-c['stress_threshold']*e['duration'],0) for x in e['contacts'])
    assert math.isclose(expected,e['damage'],rel_tol=0,abs_tol=c['arithmetic_tol'])
    if not positive or any(x['force']>=c['stress_threshold'] for x in positive) or e['damage']!=0:continue
    start,end=e['time']-e['duration'],e['time']; forces=[x['force'] for x in positive]
    if intervals and start<=intervals[-1]['end']+c['event_time_tol']:
        v=intervals[-1];v['end']=end;v['force_min']=min(v['force_min'],min(forces));v['force_max']=max(v['force_max'],max(forces));v['events']+=1
    else:intervals.append(dict(start=start,end=end,force_min=min(forces),force_max=max(forces),events=1,stress_damage=0))
for v in intervals:v['duration']=v['end']-v['start']
longest=max(intervals,key=lambda x:x['duration'],default=None)
met=longest is not None and longest['duration']+c['event_time_tol']>=1.0
damage=sum(e['damage'] for e in events); repair=sum(e['repair'] for e in events)
assert math.isclose(body['integrity']-damage+repair,native[-1]['reserves'][1],abs_tol=1e-12)
assert math.isclose(sum(e['duration'] for e in events),m['final_time'],abs_tol=c['event_time_tol'])
result=dict(case='PC-HOLD',attempt=2,recorded_utc=at,
    outcome='DEMONSTRATED WITH PRIOR PRACTICE AND TIMING GUIDANCE' if met else 'NOT DEMONSTRATED',
    physical_gentle_hold_target_met=met,target_seconds=1.0,stress_threshold=c['stress_threshold'],
    qualifying_intervals=intervals,longest_qualifying_interval=longest,
    impact_times=[e['time'] for e in impacts],impact_damage=sum(e['damage'] for e in impacts),
    sustained_stress_damage=sum(e['damage'] for e in events if e['duration']>0),total_damage=damage,
    expenditure=sum(e['expenditure'] for e in events),repair=repair,
    starting_EI=[body['energy'],body['integrity']],final_EI=native[-1]['reserves'],
    simulated_seconds=m['final_time'],wall_seconds=m['wall_seconds'],native_steps=len(native),commands=len(commands),
    command_history=[dict(time=x['time'],pair=x['command']) for x in commands],
    stop_cause=m['stop_cause'],runtime_status=m['status'],
    authority_sha256=m['contract']['execution_authority']['approved_execution_sha256'],
    repeated_execution_object_unchanged=True,complete_initial_state_identical_to_attempt_001=True,
    runtime_receipt_sha256=sha(R/'manifest.json'),initial_state_identity=m['contract']['initial_state'],
    all_run_hashes_and_lengths_verified=True,force_and_damage_arithmetic_verified=True,
    operator_end_statement='done.\nWhat was wrong with the pc contact?',
    operator_explanation='Earlier recognition of reduced contact signal and holding was recorded in PC-HOLD.USER_CONTACT_OBSERVATION.json. No new explanatory statement beyond done was supplied for the repeat.',
    qualification='Separately authorized repeat after physical feedback on attempt 001 and explicit duration clarification. Jason selected all commands. Not naive or unassisted.',
    first_attempt_preserved=True,assistant_actuator_or_end_actions=0,additional_world_steps_during_review=0,
    production_code_changes=0,source_clean=True,B1_state_accessed=False)
write_new(A/'RESULT.json',result)
write_new(A/'CLOSURE.json',dict(recorded_utc=at,case='PC-HOLD',attempt=2,
    complete=True,stop_cause=m['stop_cause'],final_time=m['final_time'],records=m['records'],
    runtime_receipt_sha256=sha(R/'manifest.json'),files_verified=m['files'],assistant_sent_end=False))

contact_review=read(S/'PC-CONTACT-REPLAY/CONTACT_REVIEW.json')
observation=read(S/'PC-CONTACT.USER_CONTACT_OBSERVATION.json')
card=(P/'POSITIVE_CONTROL_CARDS.md').read_text(encoding='utf-8-sig')
criterion='Use small paired entries to approach, and identify contact onset from raw contact/proprioceptive history.'
assert criterion in card
correction=dict(case='PC-CONTACT',attempt=1,recorded_utc=at,
    previous_assessment_file='PC-CONTACT.RESULT.json',previous_assessment_sha256=sha(S/'PC-CONTACT.RESULT.json'),
    previous_assessment='PARTIAL / NOT MARKED FULLY DEMONSTRATED',
    corrected_assessment='DEMONSTRATED FOR DECLARED CONTACT-ONSET RECOGNITION; TIMING UNCERTAINTY AND SCENE-INTERPRETATION ERRORS PRESERVED',
    criterion_source='POSITIVE_CONTROL_CARDS.md',criterion_source_sha256=sha(P/'POSITIVE_CONTROL_CARDS.md'),
    exact_criterion=criterion,
    user_original_observation=observation['user_statement_verbatim'],
    user_approximate_onset_seconds=.8,
    actual_impact_seconds=contact_review['first_recorded_positive_contact_event'],
    actual_first_native_contact_sample=contact_review['first_native_contact_sample'],
    actual_support_intervals=contact_review['positive_duration_support_intervals'],
    reason='The assistant incorrectly treated trace-colour/channel identification and a correct explanation of later continuous support as additional PC-CONTACT pass requirements. The predeclared task was onset recognition. Jason identified the first contact transition before physical replay, with approximate timing. The card sets no numerical timing-accuracy gate; none is added now.',
    retained_limitations=['Original timing was tentative, not precise event-time identification.',
        'Trace colours were not confidently associated with coordinates.',
        'Later persistence was misinterpreted as another impact or rough ground.',
        'First commands were [1,1], not a careful small approach; subsequent smaller pairs and all resulting damage remain recorded. No damage-free gate was specified.',
        'Post-case physical replay and explanations were additional feedback; not evidence of prior correct scene interpretation.'],
    correction_basis='Existing pre-feedback observation and accepted criterion, not a new run or a newly supplied operator answer.',
    original_result_and_report_preserved=True,recorded_physics_changed=False,
    acceptance_criterion_changed=False,no_new_timing_tolerance=True,
    runtime_receipt_sha256=sha(S/'runs/PC-CONTACT/manifest.json'),
    original_contact_run_hashes_and_lengths_reverified=True,
    B1_state_accessed=False,B1_execution_authorized=False)
write_new(S/'PC-CONTACT.ASSESSMENT_CORRECTION.json',correction)
state_path=S/'SEQUENCE_STATE.json';state=read(state_path)
assert [x['attempts'] for x in state['cases']]==[2,1,1,2]
state['cases'][2]['status']='CLOSED / ONSET RECOGNITION DEMONSTRATED; ASSESSMENT CORRECTION RECORDED, ORIGINAL ERRORS PRESERVED'
state['cases'][3]['status']='ATTEMPT 001 TARGET NOT MET; AUTHORIZED ATTEMPT 002 '+result['outcome']
state.update(status='ALL CONTROLS CLOSED; REVIEW ADDENDUM RECORDED; B1 NOT AUTHORIZED OR EXECUTED',
    next_case=None,simulation_steps=790,controller_commands=79,status_observed_utc=at)
state_path.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
print(json.dumps({k:result[k] for k in ('outcome','longest_qualifying_interval','impact_damage',
    'sustained_stress_damage','total_damage','expenditure','final_EI','simulated_seconds')},indent=2))
print('PC-CONTACT assessment correction appended against unchanged accepted onset criterion; original records preserved.')
