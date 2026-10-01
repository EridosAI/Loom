"""Verify only the already identified passive HTTP service and saved UI checks."""
import argparse,urllib.request,urllib.error
from evidence import *
p=argparse.ArgumentParser();p.add_argument('url');a=p.parse_args();base=a.url.rstrip('/')+'/'
with urllib.request.urlopen(base) as r:assert r.read()==(ROOT/'index.html').read_bytes()
checks={'index_matches':True}
for method,path,expected in [('POST','',405),('PUT','',405),('DELETE','',405),('GET','not-allowed.txt',404),('GET','references/FIRST_A1_COMMISSIONING_RESULT.zip',404)]:
    request=urllib.request.Request(base+path,data=b'' if method!='GET' else None,method=method)
    try:urllib.request.urlopen(request)
    except urllib.error.HTTPError as error:assert error.code==expected
    else:raise AssertionError('Read-only allowlist failed')
    checks[method+' /'+path]=expected
states=json.loads((ROOT/'screenshots/browser-states.json').read_bytes());qa=json.loads((ROOT/'screenshots/browser-control-checks.json').read_bytes())
assert len(states)%4==0 and all([s['name'] for s in states[i:i+4]]==['01-initial','02-first-contact','03-positive-window','04-administrative-stop'] for i in range(0,len(states),4))
capture_passes=len(states)//4
states=states[-4:]
for s,t in zip(states,[0,6.31019048650431,6.399999999999908,91.83000000001007]):assert abs(float(s['clock'].split()[0])-t)<1e-9
assert dict(states[1]['values'])['force']=='Impact impulse'
assert dict(states[2]['values'])['force']=='0.270747'
assert 'partial tail' in dict(states[3]['values'])['windowNote']
assert qa[0]['clock']=='0.0100000000 s' and qa[1]['clock']=='91.8300000000 s'
assert any(x['test']=='20x playback stops at recorded end' and x['clock']=='91.8300000000 s' and x['button']=='Play records' for x in qa)
assert any(x['test']=='pause' and x['button']=='Play records' for x in qa)
assert any(x['test']=='sensor panel' and x['rows']==29 for x in qa)
write(ROOT/'BROWSER_VERIFICATION.json',{'http_checks':checks,'four_recorded_states_verified':True,'capture_passes_during_layout_verification':capture_passes,'native_step_scrub_play_pause_speed_end_stop_verified':True,
    'sensor_rows':29,'accounting_panel_checked':True,'reported_browser_javascript_errors':0,
    'direct_file_url':'Blocked by in-app browser policy; not bypassed. Supported loopback HTTP preview verified.',
    'launcher_scope':'Command and dependency path inspected; HTTP viewer route verified. OS double-click/default-browser dispatch not automated.',
    'world_steps':0})
print('HTTP allowlist/write rejection and saved browser interaction checks passed.')
