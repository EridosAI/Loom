"""Commit exactly the reviewed apparatus, component tests and correction documents."""
import hashlib,json,os,pathlib,subprocess
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926';D=W/'developmental_ecology'
BASE='68db2c581f07200966d699a4f55a65f9b96df1e9'
BRANCH='build/p-b1-operator-correction-20260926-01a0c405'
env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
def git(*args):
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env)
assert git('rev-parse','HEAD').decode().strip()==BASE
assert git('branch','--show-current').decode().strip()==BRANCH
assert git('diff','--cached','--name-only')==b''
tested=json.loads((S/'fault-matrix-sealed/TESTED_SOURCE_IDENTITIES.json').read_bytes())
assert all(hashlib.sha256((D/n).read_bytes()).hexdigest()==h for n,h in tested.items())
names=['authority.py','contract.py','controllers.py','operator_view.py','pending.py','runner.py','sensor.html','sensor_ui.py','validators.py']
paths=['developmental_ecology/loom_commissioning/'+n for n in names]
paths+=['developmental_ecology/tests_apparatus/test_b1_operator.py','developmental_ecology/tests_apparatus/b1_dom_fixture.cjs']
docs='docs/developmental_ecology/p_b1_operator_correction_20260926'
paths += sorted(p.relative_to(W).as_posix() for p in (W/docs).rglob('*') if p.is_file())
git('add','--',*paths)
staged=git('diff','--cached','--name-only','-z').decode().strip('\0').split('\0')
assert set(staged)==set(paths)
git('diff','--cached','--check')
output=git('commit','-m','Correct B1 operator display deprivation and bounded interactive lifecycle')
head=git('rev-parse','HEAD').decode().strip()
assert git('rev-parse','HEAD^').decode().strip()==BASE
assert git('status','--porcelain')==b''
(S/'COMMIT_RECEIPT.json').write_text(json.dumps(dict(commit=head,parent=BASE,branch=BRANCH,worktree=str(W),files=paths,clean_worktree=True),indent=2)+'\n',encoding='utf-8')
print(output.decode(),end='')
print('CHECKPOINT '+head)
