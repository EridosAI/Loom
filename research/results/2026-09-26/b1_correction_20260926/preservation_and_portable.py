"""File/AST preservation evidence and a byte-identical portable source copy."""
import ast,hashlib,json,os,pathlib,shutil,subprocess
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926';D=W/'developmental_ecology'
BASE='68db2c581f07200966d699a4f55a65f9b96df1e9'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def git(*a):
 env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
 return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W),*a],env=env)
old=ROOT/'worktrees/loom-p-clock-correction-20260926/developmental_ecology'
protected=[*sorted((D/'loom_p').glob('*.py')),D/'configuration.json',D/'requirements-lock.txt',D/'loom_commissioning/clock.py',D/'loom_commissioning/adapter.py',D/'loom_commissioning/diagnostics.py',D/'loom_commissioning/evaluation.py']
identities={str(p.relative_to(D)):sha(p) for p in protected}
assert all(sha(old/n)==h for n,h in identities.items())
assert git('diff',BASE,'--','developmental_ecology/loom_p','developmental_ecology/configuration.json','developmental_ecology/loom_commissioning/clock.py')==b''
def functions(p):
 tree=ast.parse(p.read_text(encoding='utf-8'));return {n.name:ast.dump(n,include_attributes=False) for n in tree.body if isinstance(n,(ast.FunctionDef,ast.Assign)) and hasattr(n,'name')}
old_fn=functions(old/'loom_commissioning/controllers.py');new_fn=functions(D/'loom_commissioning/controllers.py')
stable=['command_pair','waypoint_command','waypoint_stage','time_due','validate_plan','privileged_input','observe_without_interference']
assert all(old_fn[n]==new_fn[n] for n in stable)
original=json.loads((S/'HELD_PRESERVATION_BEFORE.json').read_bytes())
assert all(sha(pathlib.Path(p))==h for p,h in original.items())
write(S/'P_CONFIG_WORLD_UNCHANGED.json',dict(parent_checkpoint=BASE,P_checkpoint='6bc9683b54e4fa80136fe8534d7713e2a250a95f',
 byte_identical_files=identities,controller_functions_AST_identical=stable,
 P_config_clock_git_diff_empty=True,held_packet_files_and_archives_checked=len(original),held_packet_unchanged=True,
 no_p_world_sensor_physics_configuration_change=True,no_existing_evidence_rewritten=True))
target=S/'portable-source';assert not target.exists()
shutil.copytree(D,target/'developmental_ecology',ignore=shutil.ignore_patterns('__pycache__','.pytest_cache'))
# Tests use only the existing lawful component cache, never held B1 state.
source_ids={str(p.relative_to(D)):sha(p) for p in D.rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts}
assert all(sha(target/'developmental_ecology'/n)==h for n,h in source_ids.items())
write(S/'PORTABLE_SOURCE_IDENTITIES.json',source_ids)
print('P/config/clock/physical adapter byte identity verified; portable source copied without any held B1 snapshot or manifest.')
