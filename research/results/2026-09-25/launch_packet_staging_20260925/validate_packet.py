"""Read-only portable-manifest validation. Never instantiate a Run or step."""
import hashlib,json,pathlib,sys
from contextlib import ExitStack
from unittest.mock import patch
R=pathlib.Path(sys.argv[1]).resolve()
sys.path[:0]=[str(R/'instrument/developmental_ecology'),str(R)]
from loom_commissioning.authority import strict_loads,canonical,execution_object,execution_sha256
from loom_commissioning.contract import authorize_execution
from loom_p.records import load_snapshot,state_hash
from loom_p.engine import Engine
from loom_p.chemistry import FieldSolver
from loom_p import physics,prehistory
from loom_commissioning import runner,adapter
import packet_checks
def forbidden(*a,**k):raise AssertionError('No execution in validation')
with ExitStack() as stack:
    for obj,name in ((Engine,'step'),(FieldSolver,'step'),(physics,'advance'),(physics,'account'),(prehistory,'prepare'),(runner.Run,'__init__'),(adapter,'step')):
        stack.enter_context(patch.object(obj,name,forbidden))
    m=strict_loads((R/'A1_MANIFEST.json').read_bytes());obj=strict_loads((R/'AUTHORITY_OBJECT.json').read_bytes())
    exact=(R/'AUTHORITY_OBJECT.canonical.json').read_bytes()
    assert exact==canonical(obj)==canonical(execution_object(m))
    h=hashlib.sha256(exact).hexdigest();assert h==execution_sha256(m)==(R/'AUTHORITY_SHA256.txt').read_text().split()[0]
    assert m['execution_authority'] is None and m['case_id']=='A1' and m['duration_seconds']==120 and m['mode']=='external_controller'
    protocol=m['execution']['procedure']['protocol']
    for name,digest in protocol['bound_files'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest,name
    snapshot=protocol['initial_snapshot_file'];assert hashlib.sha256((R/snapshot['name']).read_bytes()).hexdigest()==snapshot['sha256']
    e=load_snapshot(R/snapshot['name']);assert e.time==e.native_index==0
    before=state_hash(e);packet_checks.v1(e,m);packet_checks.v3(e)
    assert packet_checks.a0(e.c,e.phase)==strict_loads((R/'A0_GEOMETRY.json').read_bytes())
    # Empty-history read-only reader check, not a fabricated A1 observation.
    empty=packet_checks.a1_interpret(e,[],[],e.c)
    assert empty['all_fixed_windows']==[] and empty['certified_source_contact_events']==[]
    assert before==state_hash(e)
    try:authorize_execution(m)
    except ValueError as ex:assert str(ex)=='commissioning execution is not authorized'
    else:raise AssertionError('Unexpected grant')
    for name,row in strict_loads((R/'SOURCE_IDENTITIES.json').read_bytes()).items():
        assert hashlib.sha256((R/'references'/name).read_bytes()).hexdigest()==row['sha256']
    result={'portable_validation_passed':True,'canonical_sha256':h,'state_sha256':before,
            'time':e.time,'native_index':e.native_index,'grant':None,'no_trajectory_or_replay':True,
            'bound_files_and_sources_match':True,'live_V2_V3_and_A1_outcome':'not executed / pending explicit launch approval'}
    print(json.dumps(result,indent=2))
