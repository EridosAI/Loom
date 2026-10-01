"""Read-only full-runtime and exact nine-snapshot gate. Never advances a world."""
import paths
from paths import HERE,PACKET,WT,D
import copy,hashlib,json,subprocess,time
from loom_motor_commissioning import codec
from loom_motor_commissioning.motor import PARAMETERS,install
from loom_motor_commissioning.runner import identity,canonical,file_hash
from loom_p.records import code_identity
from loom_developmental import core

PROCESSES=('CURRENT','M1','M2')
ORDER=[f'MC-FS-{i:03d}-{p}' for i in (1,2,3) for p in PROCESSES]
P='6bc9683b54e4fa80136fe8534d7713e2a250a95f'
BASE='87abae34e19d4e46234402a6b1ba776814956ec1'

def git(*args):
    return subprocess.check_output(['git','-c','safe.directory='+WT.as_posix(),'--no-optional-locks','-C',str(WT),*args],text=True).strip()

def inspect_case(a):
    name=a['case_id'];i=int(name[6:9]);process=a['process']
    source=PACKET/a['original_snapshot']['path']
    original=codec.read(source,a['original_snapshot']['sha256'])
    assert original['index']==original['wave']==0 and original['life_id']==f'FS-{i:03d}'
    prepared=codec.read(HERE/a['prepared_snapshot']['path'],a['prepared_snapshot']['sha256'])
    assert (prepared['index'],prepared['wave'],prepared['life_id'],prepared['identity'])==(0,0,name,a['runtime_sha256'])
    e=prepared['engine'];e.validate_state()
    assert e.time==e.native_index==e.organism.native_count==e.organism.wave_count==0
    assert e.c.identity()==a['configuration_sha256']
    assert e.organism.rng.life==i and e.organism.rng.seed==5284097
    assert codec.digest(core.causal_state(e))==a['runner_scope']['initial_causal_sha256']
    candidate=copy.deepcopy(original['engine']);install(candidate,process)
    assert codec.encode(e)==codec.encode(candidate)
    proof=copy.deepcopy(e)
    if process!='CURRENT':del proof.organism.motor.commissioning
    assert codec.encode(proof)==codec.encode(original['engine'])
    assert codec.encode(e.body)==codec.encode(original['engine'].body)
    assert e.fields.tobytes()==original['engine'].fields.tobytes()
    assert codec.encode(e.organism.rng)==codec.encode(original['engine'].organism.rng)
    assert codec.encode(codec.decode(codec.encode(e)))==codec.encode(e)
    for rel,h in a['preserved_preparation_files'].items():assert file_hash(PACKET/rel)==h
    return e

def check():
    tick=time.perf_counter()
    assert git('rev-parse','HEAD')==BASE and git('status','--porcelain')==''
    manifest=json.loads((HERE/'MATRIX.json').read_bytes())
    assert [r['case_id'] for r in manifest['cases']]==ORDER
    runtime=identity();rh=hashlib.sha256(canonical(runtime)).hexdigest()
    assert file_hash(HERE/'RUNTIME_IDENTITY.json')==rh
    assert file_hash(HERE/'PARAMETERS.json')==hashlib.sha256(canonical(PARAMETERS)).hexdigest()
    checks=[]
    for ordinal,r in enumerate(manifest['cases'],1):
        f=HERE/'authorities'/(r['case_id']+'.json');blob=f.read_bytes();a=json.loads(blob)
        assert blob==canonical(a) and hashlib.sha256(blob).hexdigest()==r['authority_sha256']
        assert (a['case_id'],a['ordinal'],a['fixed_order'])==(r['case_id'],ordinal,ORDER)
        assert a['status']=='PROPOSED_UNAUTHORIZED' and a['kind']=='motor-temporal-commissioning'
        assert a['P_baseline_commit']==P and a['lean_base_checkpoint']==BASE
        assert a['runtime_sha256']==rh and a['P_baseline_code_sha256']==code_identity()['sha256']
        assert a['parameters_sha256']==file_hash(HERE/'PARAMETERS.json')
        assert a['configuration_file_sha256']==file_hash(D/'configuration.json')
        assert a['baseline_contract_sha256']==file_hash(D/'loom_commissioning/contract.py')
        assert a['simulation_seconds']==90 and a['maximum_native_steps']==9000
        assert all(a[k] is False for k in ('retry','continuation','replacement','outcome_tuning','automatic_selection'))
        for path,h in a['execution_files'].items():assert file_hash(HERE/path)==h
        e=inspect_case(a)
        checks.append(dict(case_id=a['case_id'],initial_index=e.native_index,time=e.time,
            initial_causal_sha256=codec.digest(core.causal_state(e)),matched_original_except_declared_process=True))
    return dict(status='PASS',runtime_sha256=rh,cases=checks,world_steps=0,organism_steps=0,
        no_new_prehistory=True,full_runtime_seconds=time.perf_counter()-tick)

if __name__=='__main__':print(json.dumps(check(),indent=2))
