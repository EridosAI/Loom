"""Synthetic browser transport fixture; no Engine, controller, RNG or world."""
import copy,json,math,pathlib,sys,time
S=pathlib.Path(__file__).resolve().parent;D=S.parent/'worktrees/loom-p-b1-apparatus-correction-20260926/developmental_ecology'
sys.path.insert(0,str(D))
from loom_commissioning.sensor_ui import OperatorHTTPServer,handler
from loom_commissioning.operator_view import display_identity,project
from loom_commissioning.controllers import LABELS
class Fixture:
 def __init__(self):
  self.intervention=display_identity('chemistry_hidden');self.state='prepared';self.number=0;self.posts=0
  raw={'schema':1,'raw_labels':LABELS,'availability':'paused','history':[], 'own_commands':[], 'annotations':[]}
  for i in range(41):raw['history'].append(dict(native_index=i,time=i*.01,raw=[.15+.02*math.sin(i*.12+k) for k in range(29)],actual_EI=[.7,1.],EI_sample_time=(i//20)*.2))
  self.data=project(raw,self.intervention)
 def display(self):return copy.deepcopy(self.data)
 def envelope(self):return dict(schema=1,lifecycle=self.state,display_condition='chemistry_hidden',decision_token='synthetic-ui:'+str(self.number) if self.state in ('prepared','paused') else None,sensors=self.display(),offline=False)
 def claim(self,token,state):
  if token!='synthetic-ui:'+str(self.number) or self.state!=state:raise ValueError('fixture request unavailable')
  self.number+=1
 def start(self,token):self.claim(token,'prepared');self.state='paused';return self.envelope()
 def submit(self,left,right,annotation,token):
  self.claim(token,'paused');self.state='running';self.posts+=1
  time.sleep(2)  # Transport delay only: no simulated clock or data evolution.
  self.data['own_commands'].append(dict(time=.4,command=[left,right]))
  if annotation:self.data['annotations'].append(dict(time=.4,text=annotation))
  self.state='paused';return self.envelope()
 def end(self,token):self.claim(token,self.state);self.state='ended';return self.envelope()
g=Fixture();server=OperatorHTTPServer(('127.0.0.1',0),handler(g))
(S/'BROWSER_FIXTURE_PORT.json').write_text(json.dumps(dict(port=server.server_port,synthetic_only=True)),encoding='utf-8')
print('Manufactured UI transport only: http://127.0.0.1:'+str(server.server_port),flush=True)
try:server.serve_forever()
except KeyboardInterrupt:pass
finally:
 server.server_close()
 (S/'BROWSER_FIXTURE_RESULT.json').write_text(json.dumps(dict(synthetic_requests=g.posts,final_display_state=g.state,worlds_constructed=0,simulation_steps=0,controller_calls=0)),encoding='utf-8')
