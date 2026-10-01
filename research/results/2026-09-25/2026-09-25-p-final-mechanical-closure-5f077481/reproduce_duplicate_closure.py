"""Exact two previous approval failures, using their unchanged raw fixture bytes.

Validation only: no Run constructor, native step, prehistory preparation or new
fault class. Source/output roots must be explicitly selected for each process.
"""
import argparse,copy,hashlib,json,sys
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--source',required=True);p.add_argument('--fixtures',required=True)
p.add_argument('--output',required=True);p.add_argument('--expect-rejection',action='store_true')
a=p.parse_args();source=Path(a.source).resolve();out=Path(a.output).resolve()
out.mkdir(parents=True,exist_ok=False);sys.path.insert(0,str(source))
from loom_commissioning import authority,contract
from loom_commissioning.initialization import from_verified_cache
from loom_p.records import state_hash
def sha(data):return hashlib.sha256(data).hexdigest()
def result(call):
    try:call();return {'accepted':True}
    except ValueError as error:return {'accepted':False,'error':str(error)}
assert Path(authority.__file__).resolve().is_relative_to(source)
engine,init=from_verified_cache(source/'artifacts/prehistory-attempt-001',0)
before=state_hash(engine)
rows=[]
for filename in ('SYNTHETIC_duplicate-approved-execution_NO_EXECUTION.json','SYNTHETIC_duplicate-nested-waypoint_NO_EXECUTION.json'):
    raw=(Path(a.fixtures)/filename).read_bytes();path=out/filename;path.write_bytes(raw)
    doc=json.loads(raw);m=copy.deepcopy(doc['approved_execution'])
    m['execution_authority']={'request_path':str(path),'request_sha256':sha(raw),
        'approved_case':m['case_id'],'approved_initial_state':m['initial_state'],
        'approved_duration':m['duration_seconds'],'approved_execution_sha256':doc['approved_execution_sha256']}
    observed=result(lambda:contract.authorize_execution(m))
    rows.append({'fixture':filename,'sha256':sha(raw),'authorization':observed})
plan=[{'point':[6.,5.],'until':.1,'press_force':0.},{'point':[5.,6.],'until':.2,'press_force':0.}]
m=contract.make_manifest(engine,'duplicate-closure-validation-only',contract.EXTERNAL,'waypoint',.2,
    purpose='commissioning',initialization=init,plan=plan)
doc={'notice':'MANUFACTURED VALIDATION ONLY. NOT JASON AUTHORIZATION. NO EXECUTION.',
     'approved_execution_sha256':authority.execution_sha256(m),'approved_execution':authority.execution_object(m)}
clean=authority.canonical(doc);path=out/'SYNTHETIC_UNAMBIGUOUS_NO_EXECUTION.json';path.write_bytes(clean)
m['execution_authority']={'request_path':str(path),'request_sha256':sha(clean),
    'approved_case':m['case_id'],'approved_initial_state':m['initial_state'],
    'approved_duration':m['duration_seconds'],'approved_execution_sha256':doc['approved_execution_sha256']}
contract.validate_manifest(m,engine);contract.authorize_execution(m)
assert state_hash(engine)==before and engine.native_index==0 and engine.time==0
record={'source':str(source),'apparatus_identity':contract.apparatus_identity(),
 'authority_source_sha256':sha(Path(authority.__file__).read_bytes()),'rows':rows,
 'exact_unambiguous_current_spec_accepted':True,'engine_state_unchanged':True,
 'native_steps':0,'Run_constructors':0,'prehistory_prepared':False,
 'scope':'The exact two delivered prior raw files; synthetic approval-only controls.'}
(out/'RESULT.json').write_text(json.dumps(record,indent=2),encoding='utf-8')
print(json.dumps(record,indent=2))
if a.expect_rejection:
    assert all(not row['authorization']['accepted'] for row in rows), 'ORIGINAL DUPLICATE APPROVAL BREACH: both conflicting raw files were accepted'
else:
    assert all(not row['authorization']['accepted'] and row['authorization']['error'].startswith('duplicate JSON field:') for row in rows), 'Corrected parser must reject the exact original files at duplicate detection'
