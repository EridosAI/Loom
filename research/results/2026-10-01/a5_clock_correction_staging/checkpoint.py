"""Create the explicitly authorized local checkpoint; no remote operations."""
import hashlib,json,os,pathlib,subprocess
R=pathlib.Path(__file__).resolve().parents[1]
W=R/'worktrees/loom-p-clock-correction-20260926';D=W/'developmental_ecology'
O=R/'exports/2026-09-26-A5-clock-correction'
OLD='5f07748102cb5eaa302569c87efbae095050e9fe'
BRANCH='build/p-clock-correction-20260926-01a0c405'
env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
def git(*args):
    return subprocess.check_output(['git','-c','safe.directory='+W.as_posix(),'-c',
        'core.excludesFile='+(R/'a5_packet_staging_20260926/empty-excludes').as_posix(),'-C',str(W),*args],env=env)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for label in ('FINAL_WORKTREE_SUITE','FINAL_PORTABLE_SUITE'):
    r=json.loads((O/(label+'-receipt.json')).read_bytes());assert r['exit']==0
    assert '176 passed' in (O/(label+'.log')).read_text()
    for name,ident in r['source_inventory'].items():assert sha(D/name)==ident['sha256']
assert git('rev-parse','HEAD').decode().strip()==OLD
assert git('branch','--show-current').decode().strip()==BRANCH
assert not git('diff','--cached','--name-only').strip()
paths=[f'developmental_ecology/loom_commissioning/{n}.py' for n in ('clock','authority','controllers','pending','runner','validators')]
paths += [f'developmental_ecology/tests_apparatus/{n}.py' for n in ('test_apparatus','test_corrections','test_final_corrections','test_clock_scheduling')]
paths += ['developmental_ecology/tests_apparatus/fixtures/clock_retrospective.json','developmental_ecology/verify_clock_scheduling.py']
paths += ['docs/developmental_ecology/p_clock_correction_20260926/'+n for n in ('CLOCK_SCHEDULING_CORRECTION_REPORT.md','NATIVE_INDEX_SCHEDULING_SPECIFICATION.md')]
git('add','--',*paths)
staged=git('diff','--cached','--name-only').decode().splitlines();assert set(staged)==set(paths)
assert not git('diff','--cached','--name-only','--','developmental_ecology/loom_p','developmental_ecology/tests',
               'developmental_ecology/configuration.json','developmental_ecology/requirements-lock.txt','developmental_ecology/loom_commissioning/adapter.py').strip()
print(git('commit','-m','Correct apparatus scheduling with native indices and bounded clock validation').decode())
head=git('rev-parse','HEAD').decode().strip();assert not git('status','--porcelain').strip()
patch=git('diff','--binary',OLD,head);(O/'CLOCK_SCHEDULING_CORRECTION.patch').write_bytes(patch)
# The apparatus uses -text attributes. Verify committed production blobs have
# the exact tested bytes, not a checkout-normalized implementation identity.
for p in (D/'loom_commissioning').glob('*.py'):
    assert git('show',head+':developmental_ecology/loom_commissioning/'+p.name)==p.read_bytes()
checkpoint={'checkpoint':head,'parent':OLD,'branch':BRANCH,'worktree':str(W),
            'P':'6bc9683b54e4fa80136fe8534d7713e2a250a95f','changed_files':staged,
            'patch_sha256':hashlib.sha256(patch).hexdigest(),'git_clean':True,
            'tested_apparatus_bytes_match_committed_blobs':True,'push_PR_merge':False,
            'scope':'Local apparatus correction; stop for narrow review; not A5 authority.'}
(O/'CHECKPOINT.json').write_text(json.dumps(checkpoint,indent=2),encoding='utf-8')
print(json.dumps(checkpoint,indent=2))
