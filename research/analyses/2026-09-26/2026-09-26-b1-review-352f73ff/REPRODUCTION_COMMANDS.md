# B1 narrow review — reproduction commands

Commands below document component review only. They do not execute prepared controls/B1 or prepare authority. Working directory:

`C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97`

```powershell
$reviewPython='C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
& $reviewPython -B -X utf8 'exports\2026-09-26-b1-review-352f73ff\run_regression.py'
& $reviewPython -B -X utf8 'exports\2026-09-26-b1-review-352f73ff\audit_regression.py'
```

The root harness starts both complete suites and the A–L matrix in three subprocess slots. It clears PYTHONPATH, PYTEST_ADDOPTS, PYTEST_PLUGINS and all prior/B1 fault variables, then sets source-specific PYTHONPATH, bytecode/plugin autoload off and optional Git locks off. Node is explicitly `C:\Program Files\nodejs\node.exe`. Each pytest invocation uses `-q -p no:cacheprovider`, its own fresh `--basetemp` and `--junitxml`.

Worktree suite root: `worktrees/loom-p-b1-apparatus-correction-20260926/developmental_ecology`. Portable suite root: `exports/2026-09-26-b1-review-352f73ff/portable/source/developmental_ecology`. The portable source was extracted from the verified review-02 ZIP; only its common archive wrapper was removed to shorten paths. Both suites run `tests tests_apparatus` and pass 204 cases.

Each A–L pair invokes the exact delivered `tests_apparatus/test_b1_operator.py::<test-id>` twice: RED with its one B1_FAULT letter, GREEN with all fault variables absent. `regression/FAULT_MATRIX.json` and per-run JSON files contain complete absolute command vectors. RED exit 1 is accepted only with the intended actual failure; GREEN exits 0. `FAULT_AND_SUITE_AUDIT.json` verifies actual exception frames and JUnit failure bodies. A raises the deliberately restored old guard's ValueError. C runs the final inline JavaScript through the delivered detached Node DOM fixture. I is a synchronization stub; H/J/K have bounded physical effects. No count-only inference is used.

Independent lifecycle old/new calls:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& $reviewPython -B -X utf8 'exports\2026-09-26-b1-review-352f73ff\lifecycle\check_lifecycle.py' old
& $reviewPython -B -X utf8 'exports\2026-09-26-b1-review-352f73ff\lifecycle\check_lifecycle.py' new
```

Old exit 1 is the explicit one-hold rejection oracle after observing two actual generic holds on unmodified 68db. New exit 0 verifies actual HTTP single execution, paused custody, end and identity guards. The report in `lifecycle/` documents the supplementary exact-declaration old hidden-mode rejection separately. Only generic manufactured components are used, never prepared B1/control snapshots.

Information-flow evidence comes from `information_flow/check_operator_egress.py`, delivered DOM C RED/GREEN and `observe_delivered_dom.cjs`. The latter adds observation immediately before the retained RED assertion without changing production source. It distinguishes an actually observed DOM leak from the delivered fixture's first export failure. Detailed commands and source identities accompany that report.

Provenance reproduction is documented in `provenance/provenance.md`: safe archive extraction, read-only Git/source hashing, safe manifest comparison and final rehash. These scripts never load sealed snapshots or instantiate held cases. Their hashes/public results are provided; sealed manifests are not bundled. No builder packaging/checkpoint/launch script was run.

For future reproduction, preserve this archive. Create a fresh sibling review export, copy harnesses at the same directory depth and extract the nested builder ZIP into that new export's `portable/` (remove its single common wrapper as documented in ZIP.json). Root/lifecycle/information-flow scripts derive output location from their own path; the fixed target worktrees remain read-only inputs. Provenance helpers have explicit output constants: update only those constants in copied review harnesses. Do not rerun scripts against sealed output or overwrite original evidence. Exact runtime identities and local source paths are prerequisites, not a claim of platform-independent byte equality.
