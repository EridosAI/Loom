"""Independent bounded operator/firewall probes. Writes only the review export."""
import argparse, copy, hashlib, json, sys, threading, urllib.request, urllib.error
from http.server import HTTPServer
from pathlib import Path
from unittest.mock import patch

parser = argparse.ArgumentParser()
parser.add_argument('--target', required=True)
parser.add_argument('--output', required=True)
parser.add_argument('--firewall-mutant', action='store_true')
parser.add_argument('--firewall-only', action='store_true')
args = parser.parse_args()
target = Path(args.target)
sys.path.insert(0, str(target / 'developmental_ecology'))
sys.path.insert(0, str(target / 'developmental_ecology' / 'tests_apparatus'))
from test_apparatus import manufactured
from loom_commissioning import contract
from loom_commissioning.controllers import privileged_input, validate_sensor_payload
from loom_commissioning.runner import Run
from loom_commissioning.sensor_ui import HumanGateway, handler
from loom_commissioning.validators import verify_segment, read_stream
from loom_p.records import state_hash, strict_bytes, view
from loom_p.chemistry import FieldSolver

def firewall_check():
    av = contract.classify('V1', {'identity_mismatch': True})
    co = contract.classify('D5', {'influence_unresolved': True})
    so = contract.classify('S2', {'survival_improved': True, 'credit_beneficial': True})
    before = contract.CONFIG
    result = contract.configuration_grounds([av, co])
    assert result['requires'] == 'Jason defect-specific ruling'
    assert result['automatic_adjustment'] is False and contract.CONFIG == before
    accepted = False
    try:
        contract.configuration_grounds([av, so])
        accepted = True
    except ValueError as e:
        assert 'SO cannot' in str(e)
    assert not accepted, 'SO FIREWALL BREACH: scientific outcome accepted as configuration grounds'
    dishonest = copy.deepcopy(so); dishonest['class'] = 'AV'
    try:
        contract.configuration_grounds([dishonest])
        raise AssertionError('relabelled scientific row accepted')
    except ValueError as e:
        assert 'class mismatch' in str(e)
    return result

if args.firewall_mutant:
    real_require = contract.require
    def omit_only_so_guard(condition, message):
        if not message.startswith('SO cannot'): real_require(condition, message)
    with patch.object(contract, 'require', omit_only_so_guard):
        firewall_check()
    raise AssertionError('fault unexpectedly passed')

if args.firewall_only:
    firewall_check()
    print('GREEN: SO rejected, relabelled SO rejected, AV/CO produces request only')
    raise SystemExit(0)

out = Path(args.output); out.mkdir(parents=True, exist_ok=False)
result = {'firewall': firewall_check()}
e = manufactured()
e.birth_provenance['privileged_review_canary'] = 'PRIVILEGED_FIXTURE_STOCK_PHASE_CANARY'
initial = copy.deepcopy(e)
before = state_hash(e)
p = privileged_input(e)
for key in ('position', 'velocity', 'reserves', 'stocks', 'commands'):
    p[key][0] = 12345.
p['geometry'][0]['id'] = 'MUTATED_COPY_ONLY'
assert state_hash(e) == before
result['controller_deep_copy_noninterference'] = True
m = contract.make_manifest(e, 'fixture-independent-operator-boundary', contract.EXTERNAL, 'sensor_human', .2)
run = Run(e, m, out / 'operator')
gateway = HumanGateway(run)
server = HTTPServer(('127.0.0.1', 0), handler(gateway))
thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
base = f'http://127.0.0.1:{server.server_port}'
def get(path):
    with urllib.request.urlopen(base + path) as response:
        return response.read(), dict(response.headers)
def post(value):
    req = urllib.request.Request(base + '/command', data=json.dumps(value).encode(),
        headers={'Content-Type':'application/json', 'Origin':base}, method='POST')
    with urllib.request.urlopen(req) as response: return json.load(response)
try:
    state = state_hash(e)
    for _ in range(5):
        body, headers = get('/sensors'); validate_sensor_payload(json.loads(body))
        assert b'PRIVILEGED_FIXTURE_STOCK_PHASE_CANARY' not in body
        assert 'stock' not in json.dumps(headers).lower()
    assert state_hash(e) == state
    result['repeated_http_get_no_world_cost_field_clock_rng_change'] = True
    html, _ = get('/')
    assert b'PRIVILEGED_FIXTURE_STOCK_PHASE_CANARY' not in html
    denied = []
    for route in ('/evaluation','/manifest.json','/state','/configuration.json','/../configuration.json','/sensor-display.json','/sensors?include=world','/initial.restart.json.gz'):
        try: get(route); raise AssertionError('privileged route served: ' + route)
        except urllib.error.HTTPError as error:
            assert error.code == 404; denied.append(route)
    result['denied_routes'] = denied
    try: post({'left':2.,'right':0.,'annotation':''}); raise AssertionError('bad command accepted')
    except urllib.error.HTTPError as error:
        assert error.code == 400
        assert error.read() == b'{"message":"Command unavailable; time has paused."}'
    assert state_hash(e) == state
    one = post({'left':.1,'right':-.1,'annotation':'operator supplied note'})
    assert len(one['history']) == 11 and one['history'][-1]['native_index'] == 10
    assert one['history'][-1]['EI_sample_time'] == 0.
    assert one['history'][-1]['actual_EI'] == [.7,.8]
    observed = state_hash(e)
    for _ in range(5): get('/sensors')
    assert state_hash(e) == observed
    run.preserve_scientific_observation({'beneficial_learning':False,'scope':'synthetic SO route probe'})
    assert state_hash(e) == observed
    two = post({'left':.1,'right':-.1,'annotation':'second own note'})
    assert len(two['history']) == 21 and two['history'][-1]['native_index'] == 20
    assert abs(two['history'][-1]['EI_sample_time']-.2)<1e-12
    assert two['history'][-1]['actual_EI'] == e.body.reserves.tolist()
    assert b'PRIVILEGED_FIXTURE_STOCK_PHASE_CANARY' not in strict_bytes(two)
    result['cadence'] = {str(i):two['history'][i] for i in (0,10,19,20)}
finally:
    server.shutdown(); server.server_close(); thread.join()
    if not run.closed: run.close()
result['record_reconstruction'] = verify_segment(out / 'operator')
scientific = read_stream(out / 'operator' / 'scientific_observations.jsonl.gz')
assert len(scientific)==1 and scientific[0]['class']=='SO'
assert 'beneficial_learning' not in strict_bytes(two).decode()
result['SO_preserved_separately_neural_inert'] = scientific

# The same declared 0.2 s manufactured component, now without observer metadata.
initial.birth_provenance.pop('privileged_review_canary')
control_m = contract.make_manifest(initial,'fixture-independent-clean-control',contract.EXTERNAL,'sensor_human',.2)
control = Run(initial,control_m,out/'clean-control')
control.hold([.1,-.1]); control.hold([.1,-.1])
e.birth_provenance.pop('privileged_review_canary')
assert state_hash(e)==state_hash(initial)
result['privileged_metadata_and_SO_do_not_enter_neural_or_world_state'] = True

# Privileged exception text stays in offline records, not the operator response.
broken = manufactured()
bm = contract.make_manifest(broken,'fixture-independent-error-isolation',contract.EXTERNAL,'sensor_human',.1)
br = Run(broken,bm,out/'expected-failure')
bs = HTTPServer(('127.0.0.1',0),handler(HumanGateway(br)))
bt = threading.Thread(target=bs.serve_forever,daemon=True); bt.start()
old_base=base; base=f'http://127.0.0.1:{bs.server_port}'
try:
    def secret_error(*a,**k): raise RuntimeError('PRIVILEGED_FIXTURE_STOCK_PHASE_CANARY')
    with patch.object(FieldSolver,'step',secret_error):
        try: post({'left':0.,'right':0.,'annotation':''}); raise AssertionError('fault accepted')
        except urllib.error.HTTPError as error:
            assert error.code==400
            response=error.read()
            assert b'PRIVILEGED_FIXTURE_STOCK_PHASE_CANARY' not in response
    receipt=json.loads((out/'expected-failure'/'manifest.json').read_bytes())
    assert receipt['status']=='apparatus_failure' and not receipt['complete']
    result['privileged_exception_http_isolation'] = response.decode()
finally:
    bs.shutdown(); bs.server_close(); bt.join(); base=old_base
(out/'BOUNDARY_RESULTS.json').write_bytes(strict_bytes(view(result)))
print(json.dumps({'result':'PASS','checks':list(result),'operator_native_steps':20,'control_native_steps':20,'fault_scope':'one manufactured field failure'},indent=2))
