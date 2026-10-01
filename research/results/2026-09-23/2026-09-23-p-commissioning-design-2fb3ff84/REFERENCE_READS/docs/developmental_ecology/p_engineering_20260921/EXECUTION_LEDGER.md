# Execution ledger

All commands below ran locally in developmental_ecology with the isolated worktree Python. Exact outputs and manifests are preserved; no remote operation was issued.

```powershell
..\.venv\Scripts\python.exe -m pytest tests -q
```

Final log: artifacts/verification/component-attempt-006.txt (44 passed). Earlier attempts remain in that directory.

```powershell
..\.venv\Scripts\python.exe -m loom_p.smokes birth_30s --attempt 1
```
Result: administrative_pause; complete=True; records={'native': 3000, 'events': 3000, 'wave': 150}. Manifest: artifacts/smoke-birth_30s-attempt-001/manifest.json

```powershell
..\.venv\Scripts\python.exe -m loom_p.smokes birth_30s --attempt 2 --correction-reason "Collision-search speed-bound correction and inspector timestamp fix verified by regressions; repeat unchanged birth case so final evidence and snapshots use the corrected code identity."
```
Result: administrative_pause; complete=True; records={'native': 3000, 'events': 3000, 'wave': 150}. Manifest: artifacts/smoke-birth_30s-attempt-002/manifest.json

```powershell
..\.venv\Scripts\python.exe -m loom_p.smokes contact_ui_1s --attempt 1
```
Result: apparatus_failure; complete=False; records={'native': 1, 'events': 2}. Manifest: artifacts/smoke-contact_ui_1s-attempt-001/manifest.json

```powershell
..\.venv\Scripts\python.exe -m loom_p.smokes contact_ui_1s --attempt 2 --correction-reason "Corrected conservative collision speed bound so stationary-source separation does not inherit remote mover speed; unchanged fixture, physics laws and tolerances."
```
Result: administrative_pause; complete=True; records={'native': 100, 'events': 101, 'wave': 5}. Manifest: artifacts/smoke-contact_ui_1s-attempt-002/manifest.json

```powershell
..\.venv\Scripts\python.exe -m loom_p.smokes nonzero_resume_1s --attempt 1
```
Result: apparatus_failure; complete=False; records={'native': 20, 'events': 20, 'wave': 1}. Manifest: artifacts/smoke-nonzero_resume_1s-attempt-001/manifest.json

```powershell
..\.venv\Scripts\python.exe -m loom_p.smokes nonzero_resume_1s --attempt 2 --correction-reason "Corrected missing timestamp in live inspector wave observation; retained all-state and observer comparisons."
```
Result: administrative_pause; complete=True; records={'native': 100, 'events': 100, 'wave': 5}. Manifest: artifacts/smoke-nonzero_resume_1s-attempt-002/manifest.json

```powershell
..\.venv\Scripts\python.exe verify_engineering_records.py
Start-Process -FilePath '.\Open Loom Inspector.cmd' -WorkingDirectory (Get-Location).Path -WindowStyle Hidden -PassThru
```

The record verifier performs detached arithmetic only. Actual browser controls selected saved record 40, reconstructed it, then advanced the fixed contact prefix by one native step and to the first wave boundary, paused and stopped. ui-verification.json compares every UI record with its existing-case prefix.

Scoped copy/edit/source-hash inspection and metadata/package commands do not execute organisms. Package creation command: `..\.venv\Scripts\python.exe create_review_package.py --package` after the local commit.
