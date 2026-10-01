# Narrow clock review — reproduction commands

These commands record what was executed, not permission to execute A5. All runs used the pinned Python executable below, source `68db2c581f07200966d699a4f55a65f9b96df1e9`, and a new review export. Old failure processes explicitly import the preserved 5f source. No builder preparation, launch or checkpoint script was executed.

```powershell
$reviewPython='C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
```

Working directory:

`C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97`

Exact root invocations:

```powershell
& $reviewPython -B -X utf8 'exports\2026-09-26-p-clock-final-review-68db2c58\run_regression.py'
& $reviewPython -B -X utf8 'exports\2026-09-26-p-clock-final-review-68db2c58\audit_regression.py'
```

The regression harness uses three concurrent subprocess slots. It clears ambient PYTHONPATH, PYTEST_ADDOPTS, PYTEST_PLUGINS and all four fault variables; sets source-specific PYTHONPATH, bytecode off, plugin autoload off and optional Git locks off. It executes these exact argument forms in each indicated source root:

```text
python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp <new regression/worktree-suite-temp>
python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp <new regression/portable-suite-temp>
python -B -X utf8 verify_apparatus.py <new regression/apparatus-faults>
python -B -X utf8 verify_corrections.py <new regression/correction-faults>
python -B -X utf8 verify_final_corrections.py <new regression/final-faults>
python -B -X utf8 verify_clock_scheduling.py <new regression/clock-faults>
```

The two suite roots are `worktrees/loom-p-clock-correction-20260926/developmental_ecology` and this review's hash-verified `portable/developmental_ecology`. All matrix scripts run in the corrected worktree's `developmental_ecology`. `regression/RUNS.json` contains the complete absolute argument vectors and measured process durations. Each `FAULT_MATRIX.json` records every exact child command. RED exit 1 is expected only when its intended exception is reached; GREEN exits 0. All 59 pairs have independently verified exception frames in `FAULT_AND_SUITE_AUDIT.json`. The audit's collect-only invocation executes no additional test bodies.

Exact original RED and corrected GREEN invocations:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& $reviewPython -B -X utf8 'exports\2026-09-26-p-clock-final-review-68db2c58\scheduling\check_schedule.py' old-a
& $reviewPython -B -X utf8 'exports\2026-09-26-p-clock-final-review-68db2c58\scheduling\check_schedule.py' old-b
& $reviewPython -B -X utf8 'exports\2026-09-26-p-clock-final-review-68db2c58\scheduling\check_schedule.py' new
```

Expected exits are 1, 1, 0. Each old process writes its actual old guard result before the explicit RED oracle assertion. These are scalar/metadata checks; profile fencing prohibits world construction/steps and waypoint-command calls. `scheduling/COMMAND_RECEIPTS.json` records script identity and outputs.

Exact continuity commands and the retained reviewer source-comparison setup correction are documented in `continuity/REPRODUCTION_COMMANDS.md` and `CONTINUITY_REVIEW.md`. Only the delivered generic 0.3-second components and detached late cases are invoked. Original-record custody, extraction and final rehash commands are in `provenance/provenance.md`; source constants identify the original files. All final statuses are read-only Git calls with process-local settings.

For a future rerun, preserve the sealed output. Create a fresh sibling directory under `exports/`, copy the root and scheduling/continuity harnesses there at the same directory depth, and extract the byte-identical nested builder ZIP into that new directory's `portable/` before running. The root regression, audit and scheduling/continuity scripts derive their output location from their own path; they retain the pinned source/history inputs. Provenance helpers contain explicit output constants, so update only their new review-output constants in the copied harnesses before a rerun. No production source, original evidence or authority object needs editing. Do not run the original source-comparison attempt001 as a pass check; it is retained to disclose a corrected reviewer setup assertion.

This is portable evidence with source and commands, not a bundled interpreter or a promise of byte-identical runtime behavior on another platform. No instruction here launches A5 or creates an authority.
