# Independent actual-controller reproduction

PowerShell; run from the shared workspace below. Use fresh, nonexistent output directories for each rerun. These commands run only the exact prior manufactured alias fixture and selected delivered bounded controller checks. Synthetic grants are validation inputs only and are never passed into a commissioning Run.

```powershell
Set-Location -LiteralPath 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97'
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
Remove-Item Env:PYTEST_ADDOPTS, Env:PYTHONPATH, Env:APPARATUS_FAULT, Env:CORRECTION_FAULT, Env:FINAL_FAULT -ErrorAction SilentlyContinue
$reviewPython='C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
$reviewScript='exports\2026-09-25-p-final-mechanical-closure-5f077481\controller\reproduce_controller_closure.py'

& $reviewPython -B -X utf8 $reviewScript --source 'exports\2026-09-25-p-apparatus-correction-review-9d31e790\portable\developmental_ecology' --checkpoint 9d31e7902658b15762052a2a6a3d161d64338524 --output 'exports\2026-09-25-p-final-mechanical-closure-5f077481\controller\old-RED-002' --expect old-RED
& $reviewPython -B -X utf8 $reviewScript --source 'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology' --checkpoint 5f07748102cb5eaa302569c87efbae095050e9fe --output 'exports\2026-09-25-p-final-mechanical-closure-5f077481\controller\new-GREEN-002' --expect new-GREEN
```

Recorded runs used `old-RED-001` / `new-GREEN-001` with stdout/stderr redirected to `old-RED.log` / `new-GREEN.log`; both exited 0 after confirming their expected outcome. The scripts print imported source paths, raw/Git SHA-256 identities, the actual delivered pair/rejection, and each selected delivered assertion result. No pytest cache is involved because these selected test functions are invoked directly, without pytest's runner. The complete pytest suites and mutation logs are separately recorded by the root review.

The read-only source audit was run as follows. It writes its JSON/log evidence only inside this new review directory. To retain the sealed audit on a future rerun, first copy the script into a new review output directory and adjust its declared workspace/output anchors rather than overwrite this evidence.

```powershell
& $reviewPython -B -X utf8 'exports\2026-09-25-p-final-mechanical-closure-5f077481\controller\audit_source_scope.py'
```

`audit_source_scope.py` records the exact Git comparison arguments, requires the expected HEAD, and compares the current P/configuration/controller/adapter checkout bytes to the preserved 9d portable source. Configuration's CRLF checkout bytes differ from its LF Git blob; the unchanged committed blob and unchanged checkout bytes are reported separately.
