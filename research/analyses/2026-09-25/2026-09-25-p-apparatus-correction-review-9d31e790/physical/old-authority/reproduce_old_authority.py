"""Exact old portable source, synthetic authority, validation only.

No Run is constructed; no Engine.step, adapter.step, or field preparation runs.
--expect-rejection deliberately exits RED after preserving the counterexample.
"""
import argparse
import copy
import inspect
import json
import math
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
OLD=Path(r'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-24-p-apparatus-review-05abf604\portable\developmental_ecology')
sys.path.insert(0,str(OLD))
from loom_p.records import state_hash, strict_bytes, code_identity
from loom_commissioning import contract, controllers, initialization, runner

parser=argparse.ArgumentParser()
parser.add_argument('--expect-rejection',action='store_true')
args=parser.parse_args()
apparatus=contract.apparatus_identity()
assert apparatus['sha256']=='5dfe2c85b570d1ee84c83d812d883dd39b8bd6d1ffc3797461b7827463ba5058'
assert code_identity()['sha256']=='63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9'
for module in (contract,controllers,initialization,runner):
    assert Path(module.__file__).resolve().parent==OLD/'loom_commissioning'

e,init=initialization.from_verified_cache(OLD/'artifacts/prehistory-attempt-001',0)
before=state_hash(e)
m=contract.make_manifest(e,'authority-validation-only',contract.EXTERNAL,'waypoint',.01,
                        purpose='commissioning',initialization=init)
direction=[math.cos(e.body.angle),math.sin(e.body.angle)]
plan_a=[{'point':[float(e.body.position[i]+direction[i]) for i in range(2)],'until':.01,'press_force':0.}]
plan_b=[{'point':[float(e.body.position[i]-direction[i]) for i in range(2)],'until':.01,'press_force':0.}]
request={'notice':'SYNTHETIC VALIDATION ONLY. NOT JASON APPROVAL. NO EXECUTION.',
         'approved_manifest_without_authority':copy.deepcopy(m),'approved_route':plan_a}
request_path=HERE/('SYNTHETIC-NO-EXECUTION-RED.json' if args.expect_rejection else 'SYNTHETIC-NO-EXECUTION-CONTROL.json')
request_path.write_bytes(strict_bytes(request))
saved=request_path.read_bytes()
grant={'request_path':str(request_path),'request_sha256':contract.digest(saved),
       'approved_case':m['case_id'],'approved_initial_state':m['initial_state'],'approved_duration':m['duration_seconds']}
m['execution_authority']=grant
contract.validate_manifest(m,e); contract.authorize_execution(m)

rows=[]
for mode,kind in ((contract.EXTERNAL,'sensor_human'),(contract.EXTERNAL,'manual_privileged'),
                  (contract.INTACT,'none'),(contract.FIXED,'none')):
    variant=copy.deepcopy(m); variant.update(mode=mode,controller=kind)
    contract.validate_manifest(variant,e); contract.authorize_execution(variant)
    rows.append({'mode':mode,'controller':kind,'accepted':True,'same_grant':variant['execution_authority']==grant})

inputs=controllers.privileged_input(e)
a,_=controllers.waypoint_command(copy.deepcopy(inputs),plan_a,0)
b,_=controllers.waypoint_command(copy.deepcopy(inputs),plan_b,0)
assert a.tolist()!=b.tolist() and 'plan' in inspect.signature(runner.Run).parameters
assert 'plan' not in m and 'execution' not in m
controls={}
for field,value in (('case_id','wrong-case'),('duration_seconds',.02)):
    altered=copy.deepcopy(m); altered[field]=value
    if field=='duration_seconds': altered['hard_stop_time']=e.time+value
    try: contract.validate_manifest(altered,e); contract.authorize_execution(altered)
    except ValueError as exc: controls[field]=str(exc)
    else: raise AssertionError('old basic grant guard unexpectedly failed')
assert state_hash(e)==before and e.native_index==0 and e.time==0 and request_path.read_bytes()==saved
result={'old_checkpoint':'05abf60401d08f38750bca589b1c040e10513d7b','source_root':str(OLD),
        'apparatus':apparatus,'p_code':code_identity(),'configuration':e.c.identity(),
        'loaded_sources':{mod.__name__:str(Path(mod.__file__).resolve()) for mod in (contract,controllers,initialization,runner)},
        'exact_grant_accepted':True,'request_sha256':grant['request_sha256'],
        'same_grant_substitutions':rows,'working_old_rejection_controls':controls,
        'route':{'manifest_sha256':contract.digest(strict_bytes(m)),'approved':plan_a,'substituted':plan_b,
                 'approved_command':a.tolist(),'substituted_command':b.tolist(),
                 'manifest_has_no_route':True,'run_signature_accepts_independent_plan':True,
                 'calls':'detached waypoint_command only; no Run'},
        'engine_state_unchanged':True,'native_steps':0,'run_constructors':0,'new_prehistory_steps':0,
        'expect_rejection_mode':args.expect_rejection}
name='OLD_AUTHORITY_RED_RESULTS.json' if args.expect_rejection else 'OLD_AUTHORITY_CONTROL_RESULTS.json'
(HERE/name).write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps(result,indent=2))
if args.expect_rejection:
    assert not any(row['accepted'] for row in rows), 'OLD 05ab AUTHORITY BREACH: unchanged grant accepts four different arm/controller interventions'
