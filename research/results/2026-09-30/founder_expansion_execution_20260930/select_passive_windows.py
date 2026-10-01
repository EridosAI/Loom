"""Deterministic post-batch event anchors; no outcome-based scientific changes."""
import csv,json,math
from pathlib import Path
from passive_ab import guard
from loom_developmental.runner import atomic_json,file_hash

HERE=Path(__file__).resolve().parent;OUT=HERE/'analysis'
def main():
    guard();assert (OUT/'AB_COMPLETION.json').exists()
    rows=json.loads((OUT/'ALL_SIXTY_AB.json').read_bytes())
    expansion=[r for r in rows if int(r['life_id'][3:])>=13]
    windows=[];unavailable=[];comparison_anchors={}
    for r in expansion:
        if not r.get('complete') or not (r.get('transfer_total',0)>0 or r.get('repair',0)>0 or r.get('damage',0)>0):continue
        name=r['life_id'];events=json.loads((OUT/r['consequential_events_file']).read_bytes())
        productive=[v for v in events if sum(v['event']['transfer'])>0]
        repairing=[v for v in events if v['event']['repair']>0]
        damaging=[v for v in events if v['event']['damage']>0]
        event=(productive or repairing or damaging)[0];index=event['native_index']
        episode_path=OUT/(name+'_contact_episodes.csv')
        episodes=list(csv.DictReader(episode_path.open(encoding='utf-8'))) if episode_path.exists() else []
        prior_sources={x['source'] for x in episodes if x['source']!='' and int(x['first_native'])<=index}
        later=[int(x['first_native']) for x in episodes if x['source'] in prior_sources and int(x['first_native'])>index]
        anchors=[('pre_event',((index-1)//20)*20),('event_handoff',math.ceil(index/20)*20),
            ('later_recontact' if later else 'one_second_later',math.ceil((min(later) if later else index+100)/20)*20),
            ('final_wave',r['waves']*20)]
        used=set()
        for ordinal,(kind,last) in enumerate(anchors):
            if last<=0 or last>r['waves']*20 or last in used:
                unavailable.append(dict(life_id=name,kind=kind,last_index=last,reason='unavailable_or_duplicate_complete_wave'));continue
            used.add(last)
            windows.append(dict(name=f'{name}_{kind}',life_id=name,kind=kind,first_index=last-19,last_index=last,
                anchor_event_native=index,anchor_event_index=event['event_index'],anchor_event_time=event['event']['time']))
            comparison_anchors.setdefault(ordinal,(kind,last))
    # Earliest expansion roster member with no contact/transfer at the matching age.
    for ordinal,(kind,last) in sorted(comparison_anchors.items()):
        suitable=[r for r in expansion if r.get('complete') and r.get('contact_native_count')==0 and r.get('transfer_total')==0 and r['waves']*20>=last]
        if suitable:
            name=suitable[0]['life_id']
            if any(w['life_id']==name and w['last_index']==last for w in windows):continue
            windows.append(dict(name=f'{name}_comparison_{ordinal}',life_id=name,kind='comparison_'+kind,first_index=last-19,last_index=last))
        else:unavailable.append(dict(kind='comparison_'+kind,last_index=last,reason='no_no-contact-comparison_at_this_age'))
    assert len(windows)<=196
    atomic_json(OUT/'C_WINDOW_SELECTION.json',dict(all_sixty_AB_sha256=file_hash(OUT/'ALL_SIXTY_AB.json'),
        rule='Accepted deterministic event anchors; first 12 deep records reused, not rerun.',windows=windows,unavailable=unavailable,
        maximum=196,first_twelve_new_windows=0))
if __name__=='__main__':main()
