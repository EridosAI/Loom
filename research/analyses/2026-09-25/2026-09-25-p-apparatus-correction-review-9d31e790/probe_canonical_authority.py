"""Independent approval-only checks. No world step or trajectory output."""
import argparse, copy, hashlib, json, sys
from pathlib import Path
from unittest.mock import patch

p=argparse.ArgumentParser();p.add_argument('--target',required=True);p.add_argument('--output',required=True)
args=p.parse_args();target=Path(args.target);out=Path(args.output);out.mkdir(parents=True,exist_ok=False)
sys.path.insert(0,str(target/'developmental_ecology'))
from loom_commissioning import authority,runner
from loom_commissioning.contract import *
from loom_commissioning.initialization import from_verified_cache
from loom_p.records import state_hash

def encode(value):
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def independent_hash(m):
    return hashlib.sha256(encode({k:v for k,v in m.items() if k!='execution_authority'})).hexdigest()
def outcome(call):
    try: call(); return {'accepted':True}
    except Exception as e: return {'accepted':False,'exception':type(e).__name__,'message':str(e)}
def grant(m,name,raw=None):
    approved={k:copy.deepcopy(v) for k,v in m.items() if k!='execution_authority'}
    obj={'notice':'MANUFACTURED REVIEW DATA. NOT JASON AUTHORITY. NO EXECUTION.',
         'approved_execution_sha256':independent_hash(m),'approved_execution':approved}
    raw=encode(obj) if raw is None else raw
    path=out/name;path.write_bytes(raw)
    g={'request_path':str(path),'request_sha256':hashlib.sha256(raw).hexdigest(),
       'approved_case':m['case_id'],'approved_initial_state':m['initial_state'],
       'approved_duration':m['duration_seconds'],'approved_execution_sha256':independent_hash(m)}
    m['execution_authority']=g
    return obj

e,init=from_verified_cache(target/'developmental_ecology/artifacts/prehistory-attempt-001',0)
before=state_hash(e)
plan=[{'point':[6.,5.],'until':.1,'press_force':0.}, {'point':[5.,6.],'until':.2,'press_force':0.}]
m=make_manifest(e,'independent-authority-validation-only',EXTERNAL,'waypoint',.2,
    purpose='commissioning',initialization=init,plan=plan)
request=grant(m,'SYNTHETIC_MATCHING_NO_EXECUTION.json')
validate_manifest(m,e);authorize_execution(m)
assert authority.execution_sha256(m)==independent_hash(m)
result={'exact_approved_specification_accepted':True,'zero_initial_native_steps':e.native_index,
        'canonical_spec_fields':list(authority.execution_object(m)),
        'approved_sha256':independent_hash(m)}

def mutate(x,name):
    v=x['execution']
    if name=='controller_implementation':v['controller']['implementation']['live_functions']['waypoint_command']='1'*64
    elif name=='controller_constants':v['controller']['configuration']['heading_gain']=.81
    elif name=='route_waypoints':v['procedure']['stages'][0]['point']=[4.,5.]
    elif name=='stage_order':v['procedure']['stages'][0]['point'],v['procedure']['stages'][1]['point']=v['procedure']['stages'][1]['point'],v['procedure']['stages'][0]['point']
    elif name=='stage_duration':v['procedure']['stages'][0]['until']=.11
    elif name=='initial_state':x['initial_state']='2'*64
    elif name=='mover_phase':x['phase']+=.1
    elif name=='prehistory':x['initialization']['cache_receipt_sha256']='3'*64
    elif name=='case_deadline':x['duration_seconds']=.3;x['hard_stop_time']=.3
    elif name=='deprivation':v['display_intervention']={'kind':'chemistry_hidden'}
    elif name=='arm_identity':x['case_id']='another-arm'
    elif name=='adapter_identity':v['adapter']['implementation_sha256']='4'*64
    elif name in ('manual_controller','sensor_controller','fixed_arm','intact_arm'):
        mode,kind={ 'manual_controller':(EXTERNAL,'manual_privileged'),'sensor_controller':(EXTERNAL,'sensor_human'),
                    'fixed_arm':(FIXED,'none'),'intact_arm':(INTACT,'none')}[name]
        x.update(mode=mode,controller=kind);x['execution']=authority.make_execution(mode,kind,protocol={'steps':[{'command_interface':'declared'}]})
    elif name=='route_prefix':v['procedure']['stages']=v['procedure']['stages'][:1]
    elif name=='route_suffix':v['procedure']['stages']=v['procedure']['stages'][1:]
    elif name=='resource_scope':v['resources']['wall_limit_seconds']+=1
    elif name=='controller_defaults_omitted':del v['controller']['configuration']['heading_gain']
    else:raise AssertionError(name)

class OutputBarrier(Exception):pass
names=['controller_implementation','controller_constants','route_waypoints','stage_order','stage_duration',
       'initial_state','mover_phase','prehistory','case_deadline','deprivation','arm_identity','adapter_identity',
       'manual_controller','sensor_controller','fixed_arm','intact_arm','route_prefix','route_suffix','resource_scope','controller_defaults_omitted']
rows=[]
for name in names:
    changed=copy.deepcopy(m);mutate(changed,name)
    assert authority.execution_sha256(changed)==independent_hash(changed)!=independent_hash(m)
    binding=outcome(lambda:authority.verify_approval_binding(changed,changed['execution_authority']))
    assert not binding['accepted'] and binding['message']=='approved execution identity mismatch'
    dest=out/('MUST-NOT-EXIST-'+name)
    with patch.object(runner,'Recorder',side_effect=OutputBarrier('recorder reached')):
        entry=outcome(lambda:runner.Run(e,changed,dest))
    assert not entry['accepted'] and entry['exception']!='OutputBarrier' and not dest.exists()
    rows.append({'field':name,'new_hash':independent_hash(changed),'binding':binding,'full_pre_output_entry':entry})
result['independent_substitutions']=rows

# Reordered keys and whitespace retain a single unambiguous parsed specification.
def reverse_keys(x):
    if isinstance(x,dict):return {k:reverse_keys(v) for k,v in reversed(list(x.items()))}
    if isinstance(x,list):return [reverse_keys(v) for v in x]
    return x
reordered=reverse_keys(m)
assert authority.execution_sha256(reordered)==independent_hash(m)
pretty=copy.deepcopy(m)
grant(pretty,'SYNTHETIC_PRETTY_NO_EXECUTION.json',json.dumps(reverse_keys(request),indent=3).encode())
authorize_execution(pretty)
result['key_order_whitespace_unambiguous']=True

# Strict independent JSON reader is an oracle for duplicate field ambiguity.
def no_duplicates(pairs):
    output={}
    for k,v in pairs:
        if k in output:raise ValueError('duplicate JSON key: '+k)
        output[k]=v
    return output

dups=[]
approved=authority.execution_object(m)
bad=copy.deepcopy(approved);bad['execution']['procedure']['stages'][0]['point']=[4.,5.]
raw=(b'{"notice":"SYNTHETIC NO EXECUTION","approved_execution_sha256":'+encode(independent_hash(m))+
     b',"approved_execution":'+encode(bad)+b',"approved_execution":'+encode(approved)+b'}')
nested=encode(request)
needle=b'"point":[6.0,5.0]'
assert nested.count(needle)==1
nested=nested.replace(needle,b'"point":[4.0,5.0],"point":[6.0,5.0]')
for name,raw in [('duplicate-approved-execution',raw),('duplicate-nested-waypoint',nested)]:
    alternate=copy.deepcopy(m);grant(alternate,'SYNTHETIC_'+name+'_NO_EXECUTION.json',raw)
    strict=outcome(lambda:json.loads(raw,object_pairs_hook=no_duplicates))
    actual=outcome(lambda:authorize_execution(alternate))
    assert not strict['accepted'] and actual['accepted']
    dups.append({'case':name,'strict_independent_parser':strict,'production_authorization':actual,
                 'request_sha256':alternate['execution_authority']['request_sha256'],'resolved_spec_hash':authority.execution_sha256(alternate)})
result['AMBIGUOUS_APPROVAL_FINDING']=dups

# Protocol dictionaries need string-only keys to avoid coercive identities.
numeric=copy.deepcopy(m);numeric['execution']['procedure']['protocol']={1:'first declared procedure step'}
stringy=copy.deepcopy(numeric);stringy['execution']['procedure']['protocol']={'1':'first declared procedure step'}
assert numeric['execution']['procedure']['protocol']!=stringy['execution']['procedure']['protocol']
assert authority.execution_sha256(numeric)==authority.execution_sha256(stringy)
result['non_string_protocol_key_coercion']={'different_python_objects_same_hash':True,
    'validation':outcome(lambda:authority.validate_execution(numeric,complete=True))}

# Nonfinite input is correctly rejected; no undefined/default law-bearing fields.
nan=copy.deepcopy(m);nan['execution']['procedure']['protocol']={'value':float('nan')}
assert not outcome(lambda:authority.execution_sha256(nan))['accepted']
result['nonfinite_rejected']=True
assert state_hash(e)==before and e.native_index==0
result.update(native_steps=0,trajectory_output_created=False,
    scope='Validation-only existing-cache load; synthetic requests; rejected constructor probes protected by recorder sentinel.')
(out/'CANONICAL_AUTHORITY_RESULTS.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print(json.dumps({'substitutions_rejected':len(rows),'ambiguous_files_accepted':len(dups),'native_steps':0,'output_created':False},indent=2))
