"""Extract only a CLOSED PC-CONTACT record. No Engine, Run, controller or field imports."""
import base64, datetime, gzip, hashlib, json, math
from pathlib import Path
import numpy as np

S=Path(__file__).resolve().parent
RUN=S/'runs/PC-CONTACT'
OUT=S/'PC-CONTACT-REPLAY'
VIZ=Path('C:/Users/Jason/.codex/visualizations/2026/09/21/01a0c405-424f-7493-9252-7fa59a88d0d2/loom-pc-contact-replay.html')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p): return json.loads(p.read_bytes())
def rows(p):
    with gzip.open(p,'rt',encoding='utf-8') as f: return [json.loads(x) for x in f if x.strip()]
def pairs(p): return dict(p['$dict'])
def plain(p):
    if isinstance(p,list): return [plain(x) for x in p]
    if not isinstance(p,dict): return p
    if '$array' in p: return np.frombuffer(base64.b64decode(p['$array'],validate=True),dtype=p['dtype']).reshape(p['shape']).tolist()
    if '$dict' in p: return {k:plain(v) for k,v in p['$dict']}
    if '$tuple' in p: return [plain(x) for x in p['$tuple']]
    raise ValueError('No class restoration is allowed in passive replay extraction')
def write(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')

m=read(RUN/'manifest.json')
assert m['contract']['case_id']=='PC-CONTACT' and m['complete'] and m['status']!='open', 'Case must be closed before evaluator replay'
assert not OUT.exists() and not VIZ.exists(), 'Replay already exists; preserve it'
assert m['contract']['execution_authority']['approved_execution_sha256']=='2e9989e37863c32ae89fd559adf51942bd8152b8d5244a8de1baf2234c52ba1d'
for name,r in m['files'].items(): assert sha(RUN/name)==r['sha256'] and (RUN/name).stat().st_size==r['bytes']
native=rows(RUN/'native.jsonl.gz'); events=rows(RUN/'events.jsonl.gz'); sensors=rows(RUN/'sensor.jsonl.gz')
assert native and [n['native_index'] for n in native]==list(range(1,len(native)+1))
with gzip.open(RUN/'initial.restart.json.gz','rt',encoding='utf-8') as f: initial=json.load(f)
assert hashlib.sha256(json.dumps(initial['state'],separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()==initial['sha256']
engine=pairs(pairs(initial['state'])['engine']['attrs'])
c=plain(engine['c']['attrs']); body=plain(engine['body']['attrs']); phase=engine['phase']
radius=c['body_radius']
def mover(t):
    x=c['mover_centre'][0]+c['mover_amplitude']*math.sin(2*math.pi*t/c['mover_period']+phase)
    y=c['mover_centre'][1]; w,h=c['mover_size']
    return [x-w/2,x+w/2,y-h/2,y+h/2]
frames=[dict(t=0.,x=body['position'][0],y=body['position'][1],a=body['angle'],u=body['command'],
             e=body['energy'],i=body['integrity'],c=[0.]*8,contact=False,mover=mover(0))]
for n in native:
    frames.append(dict(t=n['time'],x=n['position'][0],y=n['position'][1],a=n['angle'],u=n['commands'],
        e=n['reserves'][0],i=n['reserves'][1],c=n['raw'][2],contact=any(v>0 for v in n['contact_rates']),mover=mover(n['time'])))
contacts=[(e,ct) for e in events for ct in e['contacts'] if ct['impulse']>0]
assert set(ct['collider'] for e,ct in contacts)<={'wall-0'}, 'Replay contact marker currently supports only this wall; do not mislabel another body'
impacts=[e for e in events if e['impact'] and any(ct['impulse']>0 for ct in e['contacts'])]
support=[e for e in events if e['duration']>0 and any(ct['impulse']>0 for ct in e['contacts'])]
intervals=[]
for e in support:
    start=e['time']-e['duration']; end=e['time']
    if intervals and start<=intervals[-1][1]+1e-9: intervals[-1][1]=max(intervals[-1][1],end)
    else: intervals.append([start,end])
first_raw=next((f['t'] for f in frames if f['contact']),None)
xs=[f['x'] for f in frames]; ys=[f['y'] for f in frames]
data=dict(case='PC-CONTACT',frames=frames,
    world=dict(side=c['world_side'],body_radius=radius,
               disks=[[p[0],p[1],c['source_radius']] for p in c['source_positions']],rectangles=c['repair_rectangles']),
    close_bounds=[-.15,max(xs)+radius+.55,min(ys)-radius-.45,max(ys)+radius+.45],
    first_contact_sensor_time=first_raw,impact_times=[e['time'] for e in impacts])
report=dict(case='PC-CONTACT',recorded_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    stop_cause=m['stop_cause'],runtime_status=m['status'],simulation_seconds=m['final_time'],
    native_steps=len(native),commands=len(rows(RUN/'controller.jsonl.gz')),records=m['records'],
    first_recorded_positive_contact_event=min((e['time'] for e,ct in contacts),default=None),
    first_native_contact_sample=first_raw,impact_event_times=[e['time'] for e in impacts],
    positive_duration_support_intervals=intervals,
    contact_colliders=sorted(set(ct['collider'] for e,ct in contacts)),
    minimum_wall_clearance=min(f['x']-radius for f in frames),geometry_tolerance=c['geometry_tol'],
    total_impact_impulse=sum(ct['impulse'] for e,ct in contacts if e['impact']),
    total_support_impulse=sum(ct['impulse'] for e,ct in contacts if not e['impact']),
    impact_damage=sum(e['damage'] for e in impacts),total_damage=sum(e['damage'] for e in events),
    expenditure=sum(e['expenditure'] for e in events),
    starting_EI=[body['energy'],body['integrity']],final_EI=native[-1]['reserves'],
    initial_position=body['position'],final_position=native[-1]['position'],final_orientation=native[-1]['angle'],
    user_observation_file='PC-CONTACT.USER_CONTACT_OBSERVATION.json',
    evidence_scope='All physical findings concern this completed disclosed PC-CONTACT record only.',
    replay_scope='All native recorded body poses retained; prescribed mover geometry evaluated algebraically at those sample times from recorded config/phase. Playback selects records only, no interpolation, simulation or command path.',
    source_receipt_sha256=sha(RUN/'manifest.json'),all_recorded_artifact_hashes_verified=True,
    additional_simulation_steps=0,controller_calls=0,production_code_changes=0,B1_state_accessed=False,
    exposure_note='Jason requested post-case plan-view replay before PC-HOLD. Record this additional practice/evaluator feedback in later interpretation; do not claim an unassisted sequence.')
OUT.mkdir(); write(OUT/'REPLAY_DATA.json',data); write(OUT/'CONTACT_REVIEW.json',report)
template=(S/'pc-contact-replay.template.html').read_text(encoding='utf-8')
assert template.count('__PC_CONTACT_REPLAY_DATA__')==1
fragment=template.replace('__PC_CONTACT_REPLAY_DATA__',json.dumps(data,separators=(',',':'),ensure_ascii=False,allow_nan=False).replace('</','<\\/'))
assert len(fragment.encode())<1_000_000
assert all(token not in fragment for token in ('fetch(', 'XMLHttpRequest', 'WebSocket', '/command', '/start', '/end'))
VIZ.write_text(fragment,encoding='utf-8')
write(OUT/'REPLAY_PROVENANCE.json',dict(fragment_path=str(VIZ),fragment_sha256=sha(VIZ),
    frame_count=len(frames),first_time=frames[0]['t'],last_time=frames[-1]['t'],
    source_receipt_sha256=sha(RUN/'manifest.json'),data_sha256=sha(OUT/'REPLAY_DATA.json'),
    source_files=m['files'],no_world_instantiation=True,no_simulation=True,no_B1_access=True))
print(json.dumps(report,indent=2)); print('Fragment: '+str(VIZ))
