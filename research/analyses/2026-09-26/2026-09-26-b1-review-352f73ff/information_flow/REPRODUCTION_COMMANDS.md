# Commands executed for the information-flow evidence

PowerShell, from workspace `C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97`. These are the recorded commands; do not overwrite a sealed evidence directory. A subsequent reproduction must use a fresh output copy at the equivalent `exports/<new-review>/information_flow` depth. The scripts derive the workspace from that depth and read the pinned worktree. No target-source writes or cache creation are required.

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD='1'
Remove-Item Env:PYTEST_ADDOPTS,Env:PYTHONPATH,Env:APPARATUS_FAULT,Env:CORRECTION_FAULT,Env:FINAL_FAULT,Env:CLOCK_FAULT,Env:B1_FAULT -ErrorAction SilentlyContinue
$python='C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
$evidence='exports\2026-09-26-b1-review-352f73ff\information_flow'
$fixture='worktrees\loom-p-b1-apparatus-correction-20260926\developmental_ecology\tests_apparatus\b1_dom_fixture.cjs'
$node='C:\Program Files\nodejs\node.exe'

& $python -B -X utf8 "$evidence\check_operator_egress.py" *> "$evidence\OPERATOR_EGRESS.log"
# Observed exit 0. Fresh generic-fixtures-evl0r32q/RESULT.json, HTTP payloads and component records.

& $python -B -X utf8 "$evidence\check_flow_source.py" *> "$evidence\SOURCE_FLOW.log"
# Observed exit 0. SOURCE_FLOW.json records exact source identities and unchanged surfaces.

$env:B1_FAULT='C'
& $node $fixture *> "$evidence\DOM-C-RED.log"
# Observed exit 1: CSS-ONLY MASK EXPORTED CHEMISTRY, 1 !== 0.
Remove-Item Env:B1_FAULT
& $node $fixture *> "$evidence\DOM-C-GREEN.log"
# Observed exit 0.

$env:B1_FAULT='C'
& $node "$evidence\observe_delivered_dom.cjs" $fixture *> "$evidence\OBSERVED-DOM-C-RED.log"
# Observed exit 1; pre-assert observation confirms exported and rendered canary.
Remove-Item Env:B1_FAULT
& $node "$evidence\observe_delivered_dom.cjs" $fixture *> "$evidence\OBSERVED-DOM-C-GREEN.log"
# Observed exit 0; invalid hidden response rejected, valid hidden/full preserve 25/29 channels.
```

No full pytest suite or complete fault matrix was rerun by this subreview. The two short physical executions reuse only the delivered generic manufactured 0.2-second component fixture; the canary HTTP gateway owns no Engine, and the DOM fixture uses invented data. The intentional RED changes are in-memory fixture behavior, not target-file edits.
