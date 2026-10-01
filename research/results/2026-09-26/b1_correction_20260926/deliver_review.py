"""Copy verified new review delivery to its authorized INBOX; no vault Git operations."""
import hashlib,json,os,pathlib,shutil,subprocess
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
r=json.loads((S/'PACKAGE_RECEIPT.json').read_bytes());source=pathlib.Path(r['batch']).resolve()
inbox=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX').resolve()
target=(inbox/source.name).resolve()
assert source.is_relative_to((ROOT/'exports').resolve())
assert target.is_relative_to(inbox) and target.parent==inbox and not target.exists()
assert source.name=='2026-09-26-B1-operator-correction-352f73ff-review-02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
archive=source/r['archive_name'];assert sha(archive)==r['archive_sha256']
original=json.loads((S/'HELD_PRESERVATION_BEFORE.json').read_bytes())
assert all(sha(pathlib.Path(p))==h for p,h in original.items())
files={p.relative_to(source):sha(p) for p in source.rglob('*') if p.is_file()}
assert not any('.git' in rel.parts for rel in files)
shutil.copytree(source,target)
assert all(sha(target/name)==value for name,value in files.items())
W=ROOT/'worktrees/loom-p-b1-apparatus-correction-20260926'
env=os.environ.copy();env['GIT_OPTIONAL_LOCKS']='0'
cmd=['git','-c','safe.directory='+W.as_posix(),'-c','core.excludesFile='+(ROOT/'a5_regeneration_20260926/empty-excludes').as_posix(),'-C',str(W)]
assert subprocess.check_output(cmd+['status','--porcelain'],env=env)==b''
assert subprocess.check_output(cmd+['rev-parse','HEAD'],env=env).decode().strip()==r['checkpoint']
receipt=dict(checkpoint=r['checkpoint'],delivery=str(target),archive_sha256=r['archive_sha256'],
    copied_files=len(files),all_copy_hashes_verified=True,held_124_files_unchanged=True,
    no_vault_git_operation=True,worktree_clean=True,independent_review_pending=True,
    no_PC_B1_or_ecological_execution=True,no_new_launch_authorities=True)
(S/'FINAL_DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
(target/'FINAL_DELIVERY_RECEIPT.json').write_bytes((S/'FINAL_DELIVERY_RECEIPT.json').read_bytes())
print(json.dumps(receipt,indent=2))
