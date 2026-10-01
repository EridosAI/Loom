"""Scoped custody and source copies; no world evolution."""
import hashlib,json,pathlib,shutil,subprocess
P=pathlib.Path(__file__).resolve().parents[1]
W=pathlib.Path(r'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405')
E=W/'developmental_ecology/artifacts/apparatus-final-correction-20260925-01a0c405'
R=P/'exports/2026-09-25-p-apparatus-correction-review-9d31e790'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert subprocess.check_output(['git','-C',str(W),'rev-parse','HEAD'],text=True).strip()=='9d31e7902658b15762052a2a6a3d161d64338524'
assert not subprocess.check_output(['git','-C',str(W),'status','--porcelain'],text=True).strip()
inventory={}
for root in (W/'developmental_ecology/artifacts',R):
    for p in sorted(root.rglob('*')):
        if p.is_file():inventory[str(p)]={'bytes':p.stat().st_size,'sha256':sha(p)}
E.mkdir(exist_ok=False)
check=E/'temporary-access-check';check.write_text('Windows-local scoped access');assert check.read_text()=='Windows-local scoped access';check.unlink()
(E/'PRESERVATION_BEFORE.json').write_text(json.dumps(inventory,indent=2),encoding='utf-8')
refs=E/'references';refs.mkdir()
for name in ('LOOM_P_FINAL_APPARATUS_CORRECTION_REVIEW.md','probe_canonical_authority.py'):
    shutil.copyfile(R/name,refs/name)
for name in ('probe_runtime_binding.py','RUNTIME_BINDING_RESULTS.json','FAULT_RECORD_VALIDATION.json','review.md'):
    shutil.copyfile(R/'authority_runtime'/name,refs/name)
for name in ('SYNTHETIC_duplicate-approved-execution_NO_EXECUTION.json','SYNTHETIC_duplicate-nested-waypoint_NO_EXECUTION.json'):
    shutil.copyfile(R/'canonical-001'/name,refs/name)
shutil.copyfile(pathlib.Path(r'C:\Users\Jason\.codex\attachments\82a12456-aa2d-4d2e-a8f1-986029f832f8\Pasted text.txt'),refs/'FINAL_CORRECTION_REQUEST.txt')
print('Verified Windows-local scoped access; inventoried',len(inventory),'prior files.')
