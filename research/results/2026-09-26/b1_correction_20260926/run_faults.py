"""Twelve independent manufactured RED/control checks. Never loads held B1 state."""
import json,os,pathlib,subprocess,sys,time,xml.etree.ElementTree as ET
S=pathlib.Path(__file__).resolve().parent;D=S.parent/'worktrees/loom-p-b1-apparatus-correction-20260926/developmental_ecology'
targets={'A':'test_A_hidden_authority','B':'test_B_payload_canary','C':'test_C_DOM_and_UI','D':'test_D_raw_record_not_mutated',
 'E':'test_paused_inertness[E]','F':'test_paused_inertness[F]','G':'test_paused_inertness[G]',
 'H':'test_H_duplicate_token','I':'test_I_running_overlap','J':'test_J_ended_irreversible',
 'K':'test_K_refresh_reconnect_inert','L':'test_L_full_raw_preserved'}
phrases={'A':'old rejection','B':'CHEMISTRY PAYLOAD LEAK','C':'CSS-ONLY MASK EXPORTED CHEMISTRY','D':'DISPLAY DEPRIVATION ALTERED PHYSICAL RAW RECORD',
 'E':'PAUSED CLOCK/RNG/EXPENDITURE BREACH E','F':'PAUSED CLOCK/RNG/EXPENDITURE BREACH F','G':'PAUSED CLOCK/RNG/EXPENDITURE BREACH G',
 'H':'DUPLICATE CREATED EXTRA HOLD','I':'OVERLAPPING EXECUTIONS ACCEPTED','J':'ENDED ADVANCED WORLD','K':'REFRESH/RECONNECT ADVANCED WORLD','L':'FULL RAW LOST CHEMISTRY'}
out=S/('fault-matrix-sealed' if '--sealed' in sys.argv else 'fault-matrix-final' if '--final' in sys.argv else 'fault-matrix');out.mkdir(exist_ok=False);rows=[]
source_files={str(p.relative_to(D)):__import__('hashlib').sha256(p.read_bytes()).hexdigest()
              for sub in ['loom_commissioning','loom_p','tests_apparatus','tests'] for p in (D/sub).rglob('*')
              if p.is_file() and p.suffix in ('.py','.html','.cjs')}
(out/'TESTED_SOURCE_IDENTITIES.json').write_text(json.dumps(source_files,indent=2),encoding='utf-8')
for name,test in targets.items():
 row=dict(fault=name,test=test,expected_assertion=phrases[name],runs=[])
 for condition in ['RED','GREEN']:
  stem=out/(name+'-'+condition);env=os.environ.copy();env['PYTEST_DISABLE_PLUGIN_AUTOLOAD']='1';env['PYTHONPATH']=str(D)
  env.pop('B1_FAULT',None)
  if condition=='RED':env['B1_FAULT']=name
  cmd=[sys.executable,'-B','-X','utf8','-m','pytest','tests_apparatus/test_b1_operator.py::'+test,'-q','-p','no:cacheprovider','--basetemp='+str(stem)+'-tmp','--junitxml='+str(stem)+'.xml']
  started=time.perf_counter()
  with pathlib.Path(str(stem)+'.log').open('xb') as log:r=subprocess.run(cmd,cwd=D,env=env,stdout=log,stderr=subprocess.STDOUT)
  raw=pathlib.Path(str(stem)+'.log').read_text(encoding='utf-8')
  suite=ET.parse(str(stem)+'.xml').getroot().find('testsuite')
  valid=r.returncode==(1 if condition=='RED' else 0) and suite.attrib['tests']=='1' and suite.attrib['errors']=='0'
  if condition=='RED':valid=valid and phrases[name] in raw and suite.attrib['failures']=='1'
  else:valid=valid and suite.attrib['failures']=='0'
  row['runs'].append(dict(condition=condition,returncode=r.returncode,seconds=time.perf_counter()-started,verified=valid))
  assert valid,'Unexpected fault/check result: '+name+' '+condition
 rows.append(row);print(name+' RED -> GREEN verified',flush=True)
(out/'RED_GREEN_MATRIX.json').write_text(json.dumps(dict(manufactured_only=True,commissioning_cases_executed=0,rows=rows),indent=2),encoding='utf-8')
