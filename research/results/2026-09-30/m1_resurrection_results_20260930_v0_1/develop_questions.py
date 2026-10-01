"""NON-CANONICAL RESURRECTION SANDBOX. Post-stop descriptive synthesis only."""
from pathlib import Path
import json,math
OUT=Path(__file__).resolve().parent
LABEL='NON-CANONICAL RESURRECTION SANDBOX'
def f(x):return '—' if x is None else f'{x:.5g}'
def metric(r,key,lo,hi):
    a=[w['metrics'][key] for w in r['wave_windows'] if lo<=w['start']<hi]
    n=sum(v['n'] for v in a)
    if not n:return None
    return dict(mean=sum(v['mean']*v['n'] for v in a)/n,
        rms=math.sqrt(sum(v['rms']**2*v['n'] for v in a)/n),max=max(v['max'] for v in a))
def value(r,key,lo,hi,which='rms'):
    v=metric(r,key,lo,hi);return v[which] if v else None
def late_start(r):return max(0,60*math.ceil((r['age']-900)/60))
def contact_bouts(episodes):
    """Same collider, new bout only after >=1 s with no contact; retain actual contact time."""
    last={};out=[]
    for e in episodes:
        old=last.get(e['collider'])
        if old is None or e['start']-old['end']>=1.:
            old=dict(collider=e['collider'],start=e['start'],end=e['end'],duration=0.,transfer=0.,damage=0.,repair=0.,impulse=0.,
                first_relative_speed=e['first_relative_speed'],peak_relative_speed=0.,peak_impulse=0.,fragments=0)
            out.append(old);last[e['collider']]=old
        old['end']=e['end'];old['fragments']+=1
        for k in ('duration','transfer','damage','repair','impulse'):old[k]+=e[k]
        for k in ('peak_relative_speed','peak_impulse'):old[k]=max(old[k],e[k])
    return sorted(out,key=lambda e:e['start'])
def main():
    doc=json.loads((OUT/'PASSIVE_RESULTS.json').read_bytes());allr=doc['lives'];rs=[r for r in allr if 'kinematics' in r]
    bouts={r['life_id']:contact_bouts(r['physical']['episodes']) for r in rs}
    lines=['# '+LABEL,'','# Developmental questions — descriptive post-run assessment','',
        'All twelve prepared individuals remain in the denominator. The following summaries use fixed 900-second age bands and the saved 60-second windows. Incomplete bands retain their actual exposure. No source/learning outcome changed execution or the age target.','',
        'External restoration is excluded from source energy and repair. The same bodies, histories, M1 processes and worlds continued; these are externally supported histories, not independent ordinary lifetimes.','',
        '## 1. Source contact frequency with age','',
        '| Age band (s) | Available individual-seconds | Literal contact fragments | Grouped source bouts | Source-contact seconds | Source energy |',
        '|---|---:|---:|---:|---:|---:|']
    bands=[]
    for lo in range(0,4500,900):
        hi=lo+900;exposure=sum(max(0,min(r['age'],hi)-lo) for r in rs)
        eps=[e for r in rs for e in r['physical']['episodes'] if e['collider'].startswith('source-') and lo<=e['start']<hi]
        energy=sum(w['transfer'] for r in rs for w in r['physical']['windows'] if lo<=w['start']<hi)
        contact_seconds=sum(max(0,min(hi,e['end'])-max(lo,e['start'])) for r in rs for e in r['physical']['episodes'] if e['collider'].startswith('source-'))
        nb=sum(e['collider'].startswith('source-') and lo<=e['start']<hi for es in bouts.values() for e in es)
        bands.append(dict(start=lo,end=hi,exposure=exposure,source_episodes=len(eps),productive_episodes=sum(e['transfer']>0 for e in eps),grouped_source_bouts=nb,contact_seconds=contact_seconds,energy=energy))
        lines.append(f"| {lo}–{hi} | {f(exposure)} | {len(eps)} | {nb} | {f(contact_seconds)} | {f(energy)} |")
    lines+=['','Episode starts are literal contact intervals, not independent successful searches. Energy is allocated by physical event time. Age differences alone do not establish learned source seeking.','',
        '## 2–4. Later interaction, return to productive regions, duration and transfer','',
        '| Individual | Source bouts | Productive bouts | Same-source recontacts | Recontacts after productive bout | First / last actual contact duration (s) | First / last source-bout energy |',
        '|---|---:|---:|---:|---:|---|---|']
    encounters={};candidates=[]
    for r in rs:
        eps=[e for e in bouts[r['life_id']] if e['collider'].startswith('source-')];last={};productive=set();re=rp=0;rows=[]
        for e in eps:
            old=last.get(e['collider']);gap=e['start']-old['end'] if old else None
            returned=old is not None and gap>=1.;re+=returned;rp+=returned and e['collider'] in productive
            rows.append(dict(**e,gap_since_same_source=gap,previously_productive_source=e['collider'] in productive))
            if e['transfer']>0:productive.add(e['collider'])
            last[e['collider']]=e
        encounters[r['life_id']]=rows
        duration=f"{f(eps[0]['duration'])} / {f(eps[-1]['duration'])}" if eps else '—'
        transfer=f"{f(eps[0]['transfer'])} / {f(eps[-1]['transfer'])}" if eps else '—'
        lines.append(f"| {r['life_id']} | {len(eps)} | {sum(e['transfer']>0 for e in eps)} | {re} | {rp} | {duration} | {transfer} |")
    lines+=['','A new same-source bout requires at least 1 s without contact with that source, using the separation threshold declared before outcome analysis. Consecutive smaller gaps are joined for this descriptive display only; duration sums actual contact time and excludes the gaps. The native record contains many short release/recontact fragments. Every fragment, impulse and damage remains in PASSIVE_RESULTS.json; no physical observation is suppressed. A repeated source ID documents recontact, not a heading choice or goal.','',
        'Grouped per-source encounter sequences are retained in DEVELOPMENTAL_SUMMARY.json; full fragments and positions remain in PASSIVE_RESULTS.json. First/last summaries are order-based descriptions, not selected best encounters.','',
        '## 5–6. Damage, later contact and repair','',
        '| Individual | Damage | Repair | Damaging episodes | Repair episodes | First / last damaging approach speed | First / last damaging impulse |',
        '|---|---:|---:|---:|---:|---|---|']
    for r in rs:
        p=r['physical'];dam=[e for e in bouts[r['life_id']] if e['damage']>0];rep=[e for e in bouts[r['life_id']] if e['repair']>0]
        speed=f"{f(dam[0]['first_relative_speed'])} / {f(dam[-1]['first_relative_speed'])}" if dam else '—'
        imp=f"{f(dam[0]['impulse'])} / {f(dam[-1]['impulse'])}" if dam else '—'
        lines.append(f"| {r['life_id']} | {f(p['damage'])} | {f(p['repair'])} | {len(dam)} | {len(rep)} | {speed} | {imp} |")
    lines+=['','Later contact can differ because of geometry, approach angle, speed or mover timing. These uncontrolled histories do not isolate acquired avoidance or gentle-contact learning. Absence of a later contact also does not establish avoidance. Repair after damage is a physical observation; causally learned repair seeking is not tested.','',
        '## 7. Roaming and accumulated experience','',
        '| Individual | Path, first / last block (up to 900 s) | New 0.25-unit cells, first / last | Re-entry fraction, first / last | Mean speed, first / last |',
        '|---|---|---|---|---|']
    roaming={}
    for r in rs:
        pair=[]
        for lo,hi in [(0,min(900,r['age'])),(late_start(r),r['age'])]:
            ws=[w for w in r['kinematics']['windows'] if lo<=w['start']<hi];duration=sum(w['end']-w['start'] for w in ws)
            entries=sum(w['entries025'] for w in ws);returns=sum(w['reentries025'] for w in ws)
            pair.append(dict(start=lo,end=hi,path=sum(w['path'] for w in ws),new_cells=sum(w['new_cells025'] for w in ws),
                reentry=returns/entries if entries else None,mean_speed=sum(w['mean_speed']*(w['end']-w['start']) for w in ws)/duration if duration else None))
        roaming[r['life_id']]=pair;a,b=pair
        lines.append(f"| {r['life_id']} | {f(a['path'])} / {f(b['path'])} | {a['new_cells']} / {b['new_cells']} | {f(a['reentry'])} / {f(b['reentry'])} | {f(a['mean_speed'])} / {f(b['mean_speed'])} |")
    lines+=['','Coverage is cumulative centre occupancy. Fewer new cells late in a finite arena can simply reflect previous coverage. These changes describe roaming with age; they do not demonstrate that accumulated learning biased it. Full records also retain reversal bouts, common/differential commands, heading motion, velocity-direction persistence and contact exposure.','',
        '## 8. Actual learned/regulatory expression relative to M1','',
        '| Individual | M1 RMS, early / late | Ordinary current RMS, early / late | Learned-only algebraic current increment RMS, early / late | Evoked RMS, early / late | Minimum observed local gain |',
        '|---|---|---|---|---|---:|']
    expression={}
    for r in rs:
        pairs={}
        for key in ('oscillator_rms','current_rms','learned_current_algebraic_delta_rms','learned_attenuation_algebraic_delta_rms','evoked_rms','direct_rms','q_norm','H_norm','write_norm','decay_norm','use_mean'):
            pairs[key]=[value(r,key,0,min(900,r['age'])),value(r,key,late_start(r),r['age'])]
        expression[r['life_id']]=pairs
        cells=[' / '.join(map(f,pairs[k])) for k in ('oscillator_rms','current_rms','learned_current_algebraic_delta_rms','evoked_rms')]
        gain=min(w['metrics']['min_gain']['min'] for w in r['wave_windows'])
        lines.append(f"| {r['life_id']} | "+' | '.join(cells)+f' | {f(gain)} |')
    lines+=['','Early/late means first/last available block of up to 900 s, aligned to stored 60-second window starts. For RS-M1-008 the late block is 2,100 s to its durable endpoint; for the four 600-second individuals early and late are the same block and cannot show an age effect. RMS combines the actual waves. Ordinary current includes exploratory and learned regulation. The learned-only increment holds recorded need, features and exploratory draws fixed and removes only the learned-logit summand in the unchanged output equation; it is an instantaneous algebraic difference, not a replay intervention. Attenuation effects are retained separately in the JSON.','',
        'Local gain is the derivative at the recorded pre-relaxation motor target, including attenuation. A nonzero gain means that additive input remains locally effective; it does not show that a useful feedback signal was present or large. Outgoing regulator algebra applies after the wave, whereas recorded motor coupling describes the preceding native call.','',
        '## 9. Cortical structure versus uniform contraction','',
        '| Individual | Channel | Fine norm birth → final | Residual from best scaled birth / final norm | Cosine with birth | Final reference gap |',
        '|---|---|---|---:|---:|---:|']
    for r in rs:
        birth=min(r['checkpoint_history'],key=lambda x:x['age']);end=next(x for x in r['checkpoint_history'] if x['file'] in ('authoritative-final','last-full-checkpoint-not-endpoint'))
        for name,a,b in zip(('light','chemistry','contact','proprioception'),birth['cortices'],end['cortices']):
            lines.append(f"| {r['life_id']} | {name} | {f(a['fine'])} → {f(b['fine'])} | {f(b['fine_shape']['relative_directional_residual'])} | {f(b['fine_shape']['cosine_with_birth'])} | {f(b['fine_reference_gap'])} |")
    lines+=['','For RS-M1-008, "final" neural values mean the last full checkpoint at 2,939.954870546 s, earlier than the durable physical prefix. A nonzero residual shows that a matrix did more than uniformly shrink along its birth direction. It does not show useful cortical distinctions, source representations or an internal world model. Shared matrices, reference history, row dispersion and activity are also retained in the complete checkpoint summaries.','',
        '## 10. Associative write, use and return','',
        '| Individual | H RMS early / late | Write RMS early / late | Mean-use RMS early / late | q-return RMS early / late |',
        '|---|---|---|---|---|']
    for r in rs:
        p=expression[r['life_id']];lines.append(f"| {r['life_id']} | "+' | '.join(' / '.join(map(f,p[k])) for k in ('H_norm','write_norm','use_mean','q_norm'))+' |')
    lines+=['','Use is the apparatus’s recorded associative-use quantity, not a behavioral success measure. Inspect absolute values as well as growth ratios: increasing from nearly zero can still remain negligible at the point of motor use. Decay and checkpoint H/use/q histories remain available.','',
        '## 11. Consequential experience → internal change → later useful behavior','',
        'For every individual with a productive source bout, this fixed-order screen takes the first productive bout (A), the next two saved checkpoints after that entire bout (B), and the first productive bout beginning after the second checkpoint (C). Missing later checkpoints or bouts remain missing. This enforces temporal order but does not establish dependence.','',
        '| Individual | First productive bout (s) | First productive bout after B (s) | E-bank norm before / next / following | H norm before / next / following |',
        '|---|---:|---:|---|---|']
    for r in rs:
        es=[e for e in encounters[r['life_id']] if e['transfer']>0]
        if not es:continue
        a=es[0]
        # Only periodic/final checkpoints for this descriptive persistence view;
        # exact before/after support duplicates are retained in the full record.
        hs=[v for v in r['checkpoint_history'] if v['file'] in ('authoritative-final','last-full-checkpoint-not-endpoint') or 'periodic' in v['file'] or 'pilot-initial' in v['file']]
        byage={v['age']:v for v in hs};hs=sorted(byage.values(),key=lambda x:x['age'])
        distinct=[]
        for v in hs:
            if distinct and v['age']-distinct[-1]['age']<.2:distinct[-1]=v
            else:distinct.append(v)
        hs=distinct
        before=[v for v in hs if v['age']<=a['start']];after=[v for v in hs if v['age']>a['end']]
        chosen=([before[-1]] if before else [])+after[:2]
        later=next((e for e in es[1:] if len(after)>=2 and e['start']>after[1]['age']),None)
        cand=dict(life_id=r['life_id'],first_productive=a,next_separated_productive=later,
            checkpoint_comparison=[dict(age=v['age'],file=v['file'],bank_E=v['bank_norm'][0],H_norm=v['H_norm'],q_norm=v['q_norm']) for v in chosen],causal_dependence_established=False)
        candidates.append(cand)
        lines.append(f"| {r['life_id']} | {f(a['start'])} | {f(later['start'] if later else None)} | "+' / '.join(f(v['bank_norm'][0]) for v in chosen)+' | '+' / '.join(f(v['H_norm']) for v in chosen)+' |')
    if not candidates:lines+=['| No productive source episode recorded | — | — | — | — |']
    lines+=['','The complete damage/repair/contact histories also remain available. Persistent internal change can arise from ordinary drift and ongoing exposure. A later useful contact can arise from M1 wandering or geometry. This run contains no causal ablation or matched counterfactual, so no organism can be declared to have useful behavior dependent on that internal change on this evidence alone.','',
        '## Boundary','',
        'No founder was selected. No canonical motor acceptance, Nursery change, new life, continuation, parameter adjustment or further experiment follows from this analysis. All external support, discarded partial-wave durations and intervention boundaries remain explicit in the evidence.']
    (OUT/'DEVELOPMENTAL_QUESTIONS.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
    (OUT/'DEVELOPMENTAL_SUMMARY.json').write_text(json.dumps(dict(label=LABEL,bands=bands,encounters=encounters,all_contact_bouts=bouts,roaming=roaming,expression=expression,temporal_candidates=candidates),indent=2,allow_nan=False)+'\n',encoding='utf8')
if __name__=='__main__':main()
