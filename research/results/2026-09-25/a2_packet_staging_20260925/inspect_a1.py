import sys,json,pathlib
ROOT=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'exports/2026-09-25-A1-read-only-reanalysis-viewer-v1'))
from evidence import Evidence
e=Evidence()
p=[json.loads(x) for x in e.z.read('evidence/progress.jsonl').splitlines()]
r=e.json('evidence/trajectory-001/manifest.json')
o=e.json('evidence/read-only-review/A1_OBSERVATIONS.json')
print(json.dumps({'progress':[(x['time'],x['wall_seconds_since_preflight']) for x in p[::8]],'windows_first':o['all_fixed_windows'][:1]},indent=2))
print(json.dumps(o['all_fixed_windows'][250:263],indent=2))
t=e.json('evidence/EXECUTION_RESULT.json')['time']
tail_start=next(x for x in p if x['time']>=70)
tail=(p[-1]['wall_seconds_since_preflight']-tail_start['wall_seconds_since_preflight'])/(t-tail_start['time'])
stored=sum(v['bytes'] for v in r['files'].values())+len(e.z.read('evidence/trajectory-001/manifest.json'))
print(json.dumps({'simulated':t,'wall':r['wall_seconds'],'uncompressed':r['uncompressed_bytes'],'stored':stored,'tail_since':tail_start['time'],'tail_rate':tail,'at180_average_wall':180*r['wall_seconds']/t,'at180_tail_wall':180*tail,'at180_uncompressed':180*r['uncompressed_bytes']/t,'at180_stored':180*stored/t},indent=2))
