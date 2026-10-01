"""Validation-only exact corrected hidden declaration on original68db authority.

Reads only this review's generic manifests; no Engine, Run, snapshot or grant.
"""
import copy,hashlib,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
SOURCE=ROOT/'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
sys.path.insert(0,str(SOURCE))
from loom_commissioning import authority
assert Path(authority.__file__).resolve()==(SOURCE/'loom_commissioning/authority.py').resolve()
old=json.loads((HERE/'old-components/old-duplicate/manifest.json').read_bytes())['contract']
new=json.loads((HERE/'new-components/lifecycle/manifest.json').read_bytes())['contract']
authority.validate_execution(old,complete=True)
hidden=copy.deepcopy(old)
hidden['execution']['display_intervention']=copy.deepcopy(new['execution']['display_intervention'])
assert set(hidden['execution']['display_intervention'])=={'kind','raw_flat_indices','representation','implementation_sha256'}
assert hidden['execution']['display_intervention']['raw_flat_indices']==[10,11,12,13]
try:authority.validate_execution(hidden,complete=True)
except ValueError as error:message=str(error)
else:raise AssertionError('Expected genuine old hidden rejection')
assert message=='unsupported display intervention'
result={'source':str(SOURCE),'authority_source_sha256':hashlib.sha256((SOURCE/'loom_commissioning/authority.py').read_bytes()).hexdigest(),
 'unchanged_full_raw_manifest_accepted':True,'exact_corrected_generic_hidden_declaration':hidden['execution']['display_intervention'],
 'actual_old_rejection':message,'Engine_or_Run_construction':False,'snapshot_loaded':False,'world_steps':0,'new_authority_generated':False}
(HERE/'old-hidden-exact-results.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(json.dumps(result,indent=2),flush=True)
assert False,'OLD HIDDEN RED: actual68db rejects exact corrected chemistry-hidden declaration'
