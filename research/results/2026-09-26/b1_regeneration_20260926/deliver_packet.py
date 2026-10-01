"""Copy operator-safe material ONLY; sealed evaluator archive remains in existing custody."""
import hashlib,json,pathlib,shutil
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
E=ROOT/'exports/2026-09-26-B1-regenerated-352f73ff'
inbox=pathlib.Path(r'C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench\INBOX').resolve()
target=(inbox/E.name).resolve();assert target.parent==inbox and target.is_relative_to(inbox) and not target.exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((E/'PACKAGE_RECEIPT.json').read_bytes())
before=json.loads((S/'PRESERVATION_BEFORE.json').read_bytes())
assert all(sha(pathlib.Path(p))==h for p,h in before.items())
assert sha(E/receipt['public']['archive'])==receipt['public']['sha256']
target.mkdir()
shutil.copytree(E/'B1_OPERATOR_PACKET',target/'B1_OPERATOR_PACKET')
for name in ('B1_OPERATOR_PACKET.zip','README.md','PACKAGE_RECEIPT.json'):shutil.copyfile(E/name,target/name)
assert not (target/'B1_SEALED_EVALUATOR').exists()
assert not (target/'B1_SEALED_EVALUATOR.zip').exists()
copied={}
for p in target.rglob('*'):
    if p.is_file():
        rel=p.relative_to(target);assert sha(p)==sha(E/rel);copied[rel.as_posix()]=sha(p)
assert all(sha(pathlib.Path(p))==h for p,h in before.items())
result=dict(delivery=str(target),apparatus=receipt['apparatus'],packet_custody_sha256=receipt['packet_custody_sha256'],
    files_copied=len(copied),every_copy_sha256_verified=True,operator_archive=receipt['public'],
    sealed_archive_delivered=False,sealed_material_retained_in_existing_private_custody=True,expanded_evaluator_directory_delivered=False,hidden_B1_state_undisclosed=True,
    automatic_approval_review='Rejected the initial proposal to copy the evaluator archive to the Jason-facing INBOX. No part of that rejected command ran. Resolved by delivering operator-safe material only; sealed content stays in its existing custody location.',
    historical_files_unchanged=len(before),no_git_operations=True,zero_simulation_or_controller_execution=True,
    all_execution_grants_null=True,next_decision='Jason authorization of the four positive controls only; B1 remains separately unauthorized',copied_file_sha256=copied)
(target/'DELIVERY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
(S/'DELIVERY_RECEIPT.json').write_bytes((target/'DELIVERY_RECEIPT.json').read_bytes())
print(json.dumps({k:v for k,v in result.items() if k!='copied_file_sha256'},indent=2))
