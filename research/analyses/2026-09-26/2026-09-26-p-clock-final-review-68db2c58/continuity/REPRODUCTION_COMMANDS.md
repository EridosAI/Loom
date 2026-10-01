# Continuity reproduction

Exact executed commands, from `C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97`:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
Remove-Item Env:PYTEST_ADDOPTS,Env:PYTHONPATH,Env:APPARATUS_FAULT,Env:CORRECTION_FAULT,Env:FINAL_FAULT,Env:CLOCK_FAULT -ErrorAction SilentlyContinue
$reviewPython='C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
& $reviewPython -B -X utf8 'exports\2026-09-26-p-clock-final-review-68db2c58\continuity\check_continuity.py'
& $reviewPython -B -X utf8 'exports\2026-09-26-p-clock-final-review-68db2c58\continuity\check_source_preservation.py'
```

Both completed successfully. The physical harness uses a fresh `fixtures-*` directory; its recorded output was `fixtures-thz3cgf5`, with stdout/stderr in `CONTINUITY.log`. Source audit's final stdout/stderr is `SOURCE_PRESERVATION_003.log`; JSON is `SOURCE_PRESERVATION.json`. These checks call inspected delivered fixture helpers directly and create no pytest cache. Root separately runs full suites and mutation matrices.

For future reproduction, preserve this sealed directory: copy the two scripts into a fresh sibling export's `continuity/` directory at the same directory depth. Their workspace and target anchors will then remain correct, while all new script output stays beside the copied scripts. The target and historical directories are read-only inputs. The source audit requires exact HEAD `68db2c581f07200966d699a4f55a65f9b96df1e9` and uses only process-local Git safe-directory settings with read-only Git commands.

The continuity script does only the three delivered generic 0.3-second world fixtures and the delivered scalar/detached clock cases. The scalar prescription is an incomplete clock-only dictionary, never an executable A5 manifest. The world fixture uses the generic two-point plan from `test_late_short_world_pause_resume`, not A5's route or initialization. It creates no approval request or launch authority.
