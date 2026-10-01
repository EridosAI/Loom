# Mechanical closure — reproduction commands

These commands reproduce only the three known failures, delivered deterministic fixtures, existing suites and read-only custody/reconstruction checks. They do not execute commissioning or prepare prehistory. Synthetic grant files are NOT Jason authorization.

The original executed output roots are preserved in the adjacent logs and JSON. For a repeat, use a fresh **sibling export**, preserving the directory depth required by the pending-state probe. Do not run scripts that write beside themselves from the sealed review directory.

```powershell
$python = 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
$target = 'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405'
$review = 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-25-p-final-mechanical-closure-5f077481'
$oldSource = 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-25-p-apparatus-correction-review-9d31e790\portable\developmental_ecology'
$newSource = Join-Path $target 'developmental_ecology'
$fresh = Join-Path (Split-Path -Parent $review) ('reproduction-final-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $fresh | Out-Null
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:GIT_OPTIONAL_LOCKS = '0'
Remove-Item Env:PYTHONPATH,Env:PYTEST_ADDOPTS,Env:PYTEST_PLUGINS,Env:APPARATUS_FAULT,Env:CORRECTION_FAULT,Env:FINAL_FAULT -ErrorAction SilentlyContinue
```

## Supplied package and complete suites

The independent intake includes a byte-identical supplied builder ZIP under `reviewed_delivery/`. Its SHA-256 is `c0c0a0c426ff85c5fbf848ad34bba543218ff4420ebf9c573bc66737f6a34fcf`; length 61,132,733 bytes. Before the original extraction, all 846 unique safe members, 845 payload hashes/sizes and CRCs were verified. The source package's own `CHECKPOINT.json` and `FINAL_CORRECTION.patch` match Git.

```powershell
$zip = Join-Path $review 'reviewed_delivery\Loom_P_Final_Apparatus_Correction_Review_20260925.zip'
if ((Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'c0c0a0c426ff85c5fbf848ad34bba543218ff4420ebf9c573bc66737f6a34fcf') { throw 'Wrong reviewed package' }
Expand-Archive -LiteralPath $zip -DestinationPath (Join-Path $fresh 'portable')

Push-Location $newSource
& $python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp (Join-Path $fresh 'worktree-temp-001') 2>&1 | Tee-Object -FilePath (Join-Path $fresh 'worktree-suite.log')
Pop-Location

Push-Location (Join-Path $fresh 'portable\developmental_ecology')
& $python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp (Join-Path $fresh 'portable-temp-001') 2>&1 | Tee-Object -FilePath (Join-Path $fresh 'portable-suite.log')
Pop-Location
```

Observed original results: `worktree-suite.log`, **143 passed in 94.30s**; `portable-suite.log`, **143 passed in 95.95s**. The original test roots have the same names as above below the review root. Concurrent local review work affects elapsed times; they are not commissioning performance estimates.

## All 54 delivered fault/control pairs

```powershell
Push-Location $newSource
& $python -B -X utf8 .\verify_apparatus.py (Join-Path $fresh 'previous-16-pairs-001')
& $python -B -X utf8 .\verify_corrections.py (Join-Path $fresh 'previous-20-pairs-001')
& $python -B -X utf8 .\verify_final_corrections.py (Join-Path $fresh 'new-18-pairs-001')
& $python -B -X utf8 -m pytest tests tests_apparatus --collect-only -q -p no:cacheprovider
Pop-Location
```

Each matrix orchestrator exits 0 only after each intentional RED child exits 1 at its specified assertion and each GREEN exits 0. The original `FAULT_MATRIX.json` files preserve exact child commands, expected messages and fresh temp paths. `FAULT_AND_SUITE_AUDIT.json` separately extracts actual exception lines, traceback locations, summaries and hashes for all **108 logs**. Collection confirms 59 P + 24 original apparatus + 30 previous correction + 30 final correction = 143. Collection executes no test bodies.

`audit_logs_and_collection.py` is the independent log/collection audit used here. Its checks intentionally include the original observed suite elapsed strings; it is an evidence audit of this run, not a general acceptance script for future timings. Do not rerun it in place.

## Exact old duplicate approvals and corrected rejection

```powershell
$fixtures = Join-Path $fresh 'portable\developmental_ecology\tests_apparatus\fixtures\final_review'
$duplicateProbe = Join-Path $review 'reproduce_duplicate_closure.py'
& $python -B -X utf8 $duplicateProbe --source $oldSource --fixtures $fixtures --output (Join-Path $fresh 'duplicates-old-RED') --expect-rejection
# Expected exit 1: ORIGINAL DUPLICATE APPROVAL BREACH.
& $python -B -X utf8 $duplicateProbe --source $newSource --fixtures $fixtures --output (Join-Path $fresh 'duplicates-new-GREEN')
# Expected exit 0: both exact files rejected at duplicate detection;
# the exact unambiguous current specification is accepted in validation only.
```

Original evidence: `duplicates-old-RED.log`, `duplicates-new-GREEN.log`, their `RESULT.json` and byte-identical copied raw requests. No runner is constructed and native/time remain zero.

## Exact old controller escape and corrected actual dispatch

```powershell
$controllerProbe = Join-Path $review 'controller\reproduce_controller_closure.py'
& $python -B -X utf8 $controllerProbe --source $oldSource --checkpoint 9d31e7902658b15762052a2a6a3d161d64338524 --output (Join-Path $fresh 'controller-old-RED') --expect old-RED
& $python -B -X utf8 $controllerProbe --source $newSource --checkpoint 5f07748102cb5eaa302569c87efbae095050e9fe --output (Join-Path $fresh 'controller-new-GREEN') --expect new-GREEN
```

The probe's `--expect` selects which observed behavior is asserted, so both observation processes exit 0 when the selected old failure/new success reproduces. The separate rejection oracle below applies the same rejection-before-advancement expectation to those recorded outcomes: old RED exit 1, corrected GREEN exit 0, without another physical run. Original outputs are `controller/old-RED-001`, `controller/new-GREEN-001` and their logs. Actual imported files are checked against the selected checkpoint. Old code emits the substituted pair; corrected code rejects with zero alternate calls and no advancement, then the restored approved implementation emits the expected pair. Only the exact prior fixture and eight selected delivered controller checks are used.

```powershell
& $python -B -X utf8 (Join-Path $review 'controller\assert_rejection_oracle.py') (Join-Path $fresh 'controller-old-RED\RESULT.json')
# Expected exit 1: ORIGINAL CONTROLLER DISPATCH BREACH.
& $python -B -X utf8 (Join-Path $review 'controller\assert_rejection_oracle.py') (Join-Path $fresh 'controller-new-GREEN\RESULT.json')
# Expected exit 0.
```

## Exact pending overrun and corrected continuation

Copy `pending/check_pending.py` into `$fresh\pending\check_pending.py` before running. Its `old` and `new` modes use the preserved original runtime and the current target respectively; it deliberately refuses an existing component-output directory. Exact executed commands, the retained reviewer setup error and the final passing run (`new -002`) are documented in `pending/PENDING_MECHANICAL_CLOSURE.md` and `COMMAND_RECEIPTS.json`.

```powershell
$pendingFresh = Join-Path $fresh 'pending'
New-Item -ItemType Directory -Path $pendingFresh | Out-Null
Copy-Item -LiteralPath (Join-Path $review 'pending\check_pending.py') -Destination $pendingFresh
& $python -B -X utf8 (Join-Path $pendingFresh 'check_pending.py') old
# Expected exit 1: OLD PENDING HOLD BREACH after reproducing ordinary 7+4 overrun.
& $python -B -X utf8 (Join-Path $pendingFresh 'check_pending.py') new
# Expected exit 0 for rejection, exact legal continuation and delivered boundaries.
```

## Read-only preservation and reconstruction

```powershell
$provenanceFresh = Join-Path $fresh 'provenance'
New-Item -ItemType Directory -Path $provenanceFresh | Out-Null
Copy-Item -LiteralPath (Join-Path $review 'provenance\audit_closure.py') -Destination $provenanceFresh
Push-Location $target
& $python -B -X utf8 (Join-Path $provenanceFresh 'audit_closure.py')
Pop-Location
```

This expects the freshly extracted sibling `portable/` and read access to the named prior inventories and protected existing test records. It uses Git inspection, hashing and replay of existing manufactured records only. Existing receipts are never overwritten; an already-present receipt must match exactly. Historical source paths remain explicit to prevent corrected code standing in for old failures. On another host, review and adapt those paths in a new copy; this portable intake includes source/evidence archives, not the pinned Python installation or a claim of cross-platform identity equivalence.

The seal script creates only the independent intake and reopens it to verify every included payload hash, size and CRC. The intake excludes redundant extracted source and disposable pytest trees, while retaining all 108 matrix logs and all independent closure component evidence. It performs no commissioning or target writes.
