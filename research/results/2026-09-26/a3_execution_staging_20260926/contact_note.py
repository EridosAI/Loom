"""Describe recorded contact interruptions; saved-data arithmetic only."""
import bisect,gzip,hashlib,json,math,pathlib,shutil
S=pathlib.Path(__file__).resolve().parent
B=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\commissioning-A3-20260925-5f077481')
O=B/'read-only-review'
def sha(p):
    with p.open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def readstream(n):
    with gzip.open(B/'trajectory-001'/(n+'.jsonl.gz'),'rt',encoding='utf-8') as f:return [json.loads(x) for x in f]
before={str(p):sha(p) for p in B.rglob('*') if p.is_file()}
o=json.loads((O/'A3_OBSERVATIONS.json').read_bytes());events=readstream('events');native=readstream('native')
energy=o['energy'];first=energy['first_certified_contact']['time']
points=[{'time':e['time'],'position':e['body_position'],'event_index':i} for i,e in enumerate(events) if e['time']>=first-1e-10]
points += [{'time':n['time'],'position':n['position'],'native_index':n['native_index']} for n in native if n['time']>=first-1e-10]
for p in points:p['surface_gap']=math.dist(p['position'],[3.,10.])-1.
maximum=max(points,key=lambda p:p['surface_gap'])
source_impacts=[e for e in events if e['impact'] and any(c['collider']=='source-3' for c in e['contacts'])]
source_duration=[e for e in events if not e['impact'] and any(c['collider']=='source-3' for c in e['contacts'])]
contact={'source3_supported_intervals':len(energy['contact_intervals']),'source3_positive_support_seconds':energy['positive_duration_contact_seconds'],
 'source3_gaps_count':len(energy['gaps_between_contact_intervals']),'gap_seconds_sum':math.fsum(x['duration'] for x in energy['gaps_between_contact_intervals']),
 'maximum_gap_duration_seconds':max(x['duration'] for x in energy['gaps_between_contact_intervals']),
 'maximum_recorded_surface_gap_after_first_source_contact':maximum,
 'source3_impacts':len(source_impacts),'first_source_impact_damage':source_impacts[0]['damage'],
 'subsequent_source_impact_damage':math.fsum(e['damage'] for e in source_impacts[1:]),'source3_impact_damage_total':math.fsum(e['damage'] for e in source_impacts),
 'source3_sustained_stress_damage':math.fsum(e['damage'] for e in source_duration),
 'wall_contact_intervals':len(o['wall']['contact_intervals']),'repair_contact_intervals':len(o['repair']['contact_intervals']),
 'formal_source_release_label_count':len(energy['release_events']),
 'interpretation':'Observed support gaps and repeated recontact impulses; not 629 purposeful visits, not an established apparatus defect or general infeasibility. No patch or extra diagnostic run.',
 'time_precision':'Gap durations use recorded accounting subinterval endpoints. Maximum clearance is a recorded-pose maximum, not a continuous-time extremum.',
 'raw_and_existing_analysis_hashes_unchanged':all(sha(pathlib.Path(p))==v for p,v in before.items()),'new_world_steps':0,'controller_recomputation':0}
assert contact['raw_and_existing_analysis_hashes_unchanged']
with (O/'CONTACT_INTERRUPTION_OBSERVATIONS.json').open('x',encoding='utf-8') as f:json.dump(contact,f,indent=2);f.write('\n')
text=f'''# Recorded contact interruptions — A3 reporting note

The complete ordered physical witness was observed, but source-3 contact was intermittent at small temporal and spatial scales. Preserve this alongside transfer and net-energy observations.

Wall contact and repair contact each formed one positive-duration interval. Source-3 contact formed **{contact['source3_supported_intervals']} supported intervals** separated by **{contact['source3_gaps_count']} gaps**, totaling **{contact['gap_seconds_sum']:.12g} s** without positive-duration support. The longest gap was **{contact['maximum_gap_duration_seconds']:.12g} s**. Total supported source-3 contact was **{contact['source3_positive_support_seconds']:.12g} s**. No formal `release` event labels were recorded for those source gaps; the support intervals and repeated recontact impulses establish them. Raw event labels are preserved.

The maximum saved-pose surface gap after first source contact was **{maximum['surface_gap']:.12g} world units**, at t={maximum['time']:.12g}. This is a sampled/event-endpoint maximum, not proof of a continuous-time maximum. It is far below the one-body-diameter descriptive revisit convention. Do not describe the {contact['source3_impacts']} impacts as purposeful source revisits or autonomous switching.

The first source-3 impact debited I by **{contact['first_source_impact_damage']:.12g}**. Subsequent recontact impacts debited another **{contact['subsequent_source_impact_damage']:.12g}**. Source-3 sustained-stress damage was **{contact['source3_sustained_stress_damage']:.12g}**; the recorded sustained force range was {energy['sustained_force_range']}. Do not misattribute those later integrity losses to above-threshold sustained stress.

Actual arrival at the repair strip also caused I loss of {o['milestones']['repair_arrival']['damage']:.12g}, before its positive restoration. Gross case damage ({o['whole_case']['damage']:.12g}) exceeded gross restoration ({o['whole_case']['repair']:.12g}); final integrity remained below its healthy start. No full-healing or indefinite-maintenance claim is made.

These are observed physical/contact features of this unchanged apparatus/controller case. This report does not establish whether the short interruptions warrant a future numerical or control investigation. No mechanism change, patch, replay, retry or diagnostic execution was performed. All existing raw and analysis files were hash-checked unchanged while producing this note.
'''
with (O/'CONTACT_INTERRUPTION_NOTE.md').open('x',encoding='utf-8') as f:f.write(text)
shutil.copyfile(S/'contact_note.py',O/'contact_note.py')
print(json.dumps(contact,indent=2))
