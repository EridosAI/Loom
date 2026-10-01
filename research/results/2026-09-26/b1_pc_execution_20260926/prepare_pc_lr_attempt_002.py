"""Record Jason's one fresh-attempt grant; validate without loading a world."""
import copy
import datetime
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

S = Path(__file__).resolve().parent
ROOT = S.parent
W = ROOT / 'worktrees/loom-p-b1-apparatus-correction-20260926'
D = W / 'developmental_ecology'
APP = '352f73fffa6d9781eae8aa38e708a9a05669588f'
A = S / 'PC-LR-attempt-002'

def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_new(path, value):
    with path.open('x', encoding='utf-8') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False)
        f.write('\n')

assert not A.exists(), 'Attempt preparation already exists: do not repeat'
state = read(S / 'SEQUENCE_STATE.json')
assert state['cases'][0]['attempts'] == 1
assert all(c['attempts'] == 0 for c in state['cases'][1:])
prior = read(S / 'runs/PC-LR/manifest.json')
assert prior['complete'] and prior['stop_cause'] == 'wall_time_limit'
assert prior['session_counters']['advanced'] == 0 and prior['final_time'] == 0
for name, item in prior['files'].items():
    path = S / 'runs/PC-LR' / name
    assert sha(path) == item['sha256'] and path.stat().st_size == item['bytes']

env = dict(os.environ, GIT_OPTIONAL_LOCKS='0')
git = ['git', '-c', 'safe.directory=' + W.as_posix(), '-c',
       'core.excludesFile=' + (ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(), '-C', str(W)]
assert subprocess.check_output(git + ['rev-parse', 'HEAD'], env=env).decode().strip() == APP
assert subprocess.check_output(git + ['status', '--porcelain'], env=env) == b''
assert shutil.disk_usage(ROOT).free >= 12_000_000_000

original = read(S / 'LAUNCH_PLAN.json')['cases'][0]
manifest_path = S / 'launch-manifests/PC-LR.json'
snapshot = S / 'inputs/PC-LR.snapshot.json.gz'
assert sha(manifest_path) == original['granted_manifest_sha256']
assert sha(snapshot) == original['snapshot_sha256']
assert sha(S/'approvals/PC-LR.request.json') == original['approval_request_sha256']
sys.path.insert(0, str(D))
from loom_commissioning.authority import execution_object, execution_sha256, validate_execution
from loom_commissioning.contract import authorize_execution
m = read(manifest_path)
assert execution_sha256(m) == original['authority_sha256']
validate_execution(m, complete=True)
authorize_execution(m)
for name, expected in m['execution']['procedure']['protocol']['bound_documents'].items():
    assert sha(ROOT/'exports/2026-09-26-B1-regenerated-352f73ff/B1_OPERATOR_PACKET'/name) == expected

question = ('Do you authorize one fresh PC-LR attempt, with the same fixture, interface and original limits? '
            'B1 will remain untouched.')
notice = ('Jason replied "Yes." to the explicit question: ' + question + '\n'
          'This authorizes exactly one fresh PC-LR attempt (attempt 002), after attempt 001 ended '
          'at its wall limit with zero commands and zero simulated steps. This is a separate '
          'attempt grant for the identical canonical execution object, not a continuation or '
          'fixture change. Retain the original 4 simulated-second ceiling, 1200 wall-second '
          'limit, 256000000-byte stream limit and all source/configuration/interface identities. '
          'Preserve attempt 001. Jason alone chooses all commands and observations. '
          'No further retry, tuning, substitution, code change, B1 execution or sealed B1 inspection is authorized.')
A.mkdir()
request_path = A / 'approval.request.json'
write_new(request_path, {'notice': notice, 'approved_execution_sha256': execution_sha256(m),
                         'approved_execution': execution_object(m)})
fresh = copy.deepcopy(m)
fresh['execution_authority']['request_path'] = str(request_path)
fresh['execution_authority']['request_sha256'] = sha(request_path)
assert execution_object(fresh) == execution_object(m)
authorize_execution(fresh)
write_new(A/'launch-manifest.json', fresh)
new_command = copy.deepcopy(original['command'])
new_command[new_command.index('--manifest')+1] = str(A/'launch-manifest.json')
new_command[new_command.index('--output')+1] = str(S/'runs/PC-LR-attempt-002')
assert not (S/'runs/PC-LR-attempt-002').exists()
write_new(A/'LAUNCH_PLAN.json', {'case': 'PC-LR', 'attempt': 2, 'command': new_command,
    'cwd': str(D), 'environment': original['environment'], 'automatic_commands': False,
    'maximum_invocations': 1, 'authority_sha256': execution_sha256(fresh)})
write_new(A/'LAUNCH_INTENT.json', {'case': 'PC-LR', 'attempt': 2, 'apparatus': APP,
    'recorded_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'question': question, 'user_answer_verbatim': 'Yes.', 'grant_scope': notice,
    'authority_sha256': execution_sha256(fresh), 'same_execution_object': True,
    'snapshot_sha256': sha(snapshot), 'granted_manifest_sha256': sha(A/'launch-manifest.json'),
    'request_sha256': sha(request_path), 'source_clean': True,
    'prior_attempt_receipt_sha256': sha(S/'runs/PC-LR/manifest.json'),
    'prior_artifact_hashes_verified': True, 'free_disk_bytes': shutil.disk_usage(ROOT).free,
    'prior_PC_exposure': 'Jason saw disclosed PC-LR raw readings and anatomy/control instructions; no command choices or comparison answer supplied by assistant.',
    'invocation_reserved': 1, 'service_started_by_this_script': False,
    'snapshot_deserialized_by_this_script': False, 'simulation_steps': 0,
    'B1_state_accessed': False})
print('Fresh PC-LR attempt 002 grant recorded and verified. Exact execution identity unchanged. No world loaded or service started. Prior run preserved.')
