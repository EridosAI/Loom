# Reproduction commands and evidence locations

Disposition: **HOLD BEFORE COUPLING COMMISSIONING**. These commands reproduce reviews/tests only. Synthetic approval files do not authorize a case. Do not run commissioning cases or prepare new prehistory. Existing target, prior review, Workbench and sealed evidence remain read-only.

The original review used the exact paths below. For a repeat, the unique `$fresh` root replaces only output locations. Copy scripts that write beside themselves into that root first. The reports/JSON preserve original executed paths, arguments and observed results. The byte-identical corrected builder ZIP is bundled under `reviewed_delivery/` and contains the full corrected source, cache, patch and historical packages. An installed pinned Python environment is still required; this intake does not bundle Python or claim cross-platform identity equivalence.

```powershell
$python = 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
$target = 'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405'
$review = 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-25-p-apparatus-correction-review-9d31e790'
$fresh = Join-Path $review ('reproduction-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $fresh | Out-Null
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:GIT_OPTIONAL_LOCKS = '0'
Remove-Item Env:PYTHONPATH,Env:APPARATUS_FAULT,Env:CORRECTION_FAULT -ErrorAction SilentlyContinue
```

## Complete suites and delivered matrices

Original worktree output: `worktree-suite.log` (113 passed in 77.05s), temp root `worktree-temp-001`. Original portable output: `portable-suite.log` (113 passed in 60.96s), temp root `portable-temp-001`. The extraction was verified against all 433 payload identities, CRCs and safe unique paths before testing; `provenance/ZIP.json` records that audit. A repeat can extract the hash-verified exact archive into a fresh directory:

```powershell
Push-Location (Join-Path $target 'developmental_ecology')
& $python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp (Join-Path $fresh 'worktree-temp') 2>&1 | Tee-Object -FilePath (Join-Path $fresh 'worktree-suite.log')
Pop-Location

$builderZip = Join-Path $review 'reviewed_delivery\Loom_P_Apparatus_Correction_Review_20260924.zip'
if ((Get-FileHash -LiteralPath $builderZip -Algorithm SHA256).Hash.ToLowerInvariant() -ne 'e261dbb9836a916f3ff4b6daa3ae8d9c21ea12194198d1ed63dfa7ee9b798a81') { throw 'Wrong reviewed package' }
Expand-Archive -LiteralPath $builderZip -DestinationPath (Join-Path $fresh 'portable')
Push-Location (Join-Path $fresh 'portable\developmental_ecology')
& $python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp (Join-Path $fresh 'portable-temp') 2>&1 | Tee-Object -FilePath (Join-Path $fresh 'portable-suite.log')
Pop-Location

Push-Location (Join-Path $target 'developmental_ecology')
& $python -B -X utf8 .\verify_apparatus.py (Join-Path $fresh 'old-pairs')
& $python -B -X utf8 .\verify_corrections.py (Join-Path $fresh 'new-pairs')
& $python -B -X utf8 -m pytest tests tests_apparatus --collect-only -q -p no:cacheprovider
Pop-Location
```

Both verifiers should exit 0 after verifying every intentional RED (child exit 1) and GREEN (child exit 0). Original outputs are `old-pairs-001/FAULT_MATRIX.json` and `new-pairs-001/FAULT_MATRIX.json`; every pair includes the full child command and distinct temp directory. Original 72 logs and the independently extracted actual exception lines/traceback locations are retained. See `authority_runtime/SUITE_AND_FAULT_AUDIT.json`: 36 pairs, 37 RED failing test instances plus three passing ones, 40 GREEN passing instances. The clock transition pair accounts for its five parameter cases. Collection is 59/24/30 and executes no test bodies.

## Canonical binding and ambiguity

```powershell
& $python -B -X utf8 (Join-Path $review 'probe_canonical_authority.py') --target $target --output (Join-Path $fresh 'canonical')
```

Expected exit 0 means the script has reproduced its assertions, including the present defects: two ambiguous requests accepted by production but rejected by the independent parser. It also asserts exact-object acceptance, 20 actual semantic substitutions rejected before Recorder and no world evolution. Original result: `canonical-001/CANONICAL_AUTHORITY_RESULTS.json`. A green probe process is not a declaration of apparatus fitness.

## Actual callable, pending state, saved-record consequence and neural regression

```powershell
$runtimeFresh = Join-Path $fresh 'authority_runtime'
New-Item -ItemType Directory -Path $runtimeFresh | Out-Null
foreach ($name in @('probe_runtime_binding.py','verify_fault_records.py','independent_checks.py','firewall_regression.py')) {
    Copy-Item -LiteralPath (Join-Path $review ('authority_runtime\' + $name)) -Destination $runtimeFresh
}
& $python -B -X utf8 (Join-Path $runtimeFresh 'probe_runtime_binding.py')
& $python -B -X utf8 (Join-Path $runtimeFresh 'verify_fault_records.py')
& $python -B -X utf8 (Join-Path $runtimeFresh 'independent_checks.py')
& $python -B -X utf8 (Join-Path $runtimeFresh 'firewall_regression.py') --fault
# Expected exit 1 at SO FIREWALL BREACH.
& $python -B -X utf8 (Join-Path $runtimeFresh 'firewall_regression.py')
# Expected exit 0.
```

The first two commands exit 0 after reporting the reproduced residuals and acceptance/rejection by existing validators. `RUNTIME_BINDING_RESULTS.json` identifies its fresh component root. All runs are manufactured, at most 0.11s actual advance; synthetic commissioning objects are validated only. Complete explanations, source lines and old numerical regression values are in `authority_runtime/review.md`. The scripts intentionally use the verified target path; on another machine, review/adjust that path in a new copy, rather than editing sealed evidence or silently substituting runtime identities.

## Independent clock oracle and exact old approval RED

```powershell
$clockFresh = Join-Path $fresh 'physical'
New-Item -ItemType Directory -Path $clockFresh | Out-Null
Copy-Item -LiteralPath (Join-Path $review 'physical\independent_clock_review.py') -Destination $clockFresh
& $python -B -X utf8 (Join-Path $clockFresh 'independent_clock_review.py')

$oldFresh = Join-Path $clockFresh 'old-authority'
New-Item -ItemType Directory -Path $oldFresh | Out-Null
Copy-Item -LiteralPath (Join-Path $review 'physical\old-authority\reproduce_old_authority.py') -Destination $oldFresh
& $python -B -X utf8 (Join-Path $oldFresh 'reproduce_old_authority.py') --expect-rejection
# Expected exit 1 at OLD 05ab AUTHORITY BREACH.
& $python -B -X utf8 (Join-Path $oldFresh 'reproduce_old_authority.py')
# Expected exit 0 for matching old grant and the observed counterexamples.
```

The clock script uses the exact old Git blob and preserved input, an independent Decimal oracle, finite fixed cases and normal short manufactured pauses. Old authority reads the existing previous review's portable source; it asserts its old aggregate identity, advances no world state and constructs no Run. The scripts retain this old path explicitly so corrected code cannot accidentally stand in for the old RED. Historical source is also available in the nested archives for inspection.

## Read-only identity, preservation and existing-record reconstruction

The executed full audit was `audit_correction.py <review>\provenance\scoped-complete` from the apparatus target cwd. For a repeat after fresh portable extraction above:

```powershell
$provenanceFresh = Join-Path $fresh 'provenance'
New-Item -ItemType Directory -Path $provenanceFresh | Out-Null
Copy-Item -LiteralPath (Join-Path $review 'provenance\audit_correction.py') -Destination $provenanceFresh
Push-Location $target
& $python -B -X utf8 (Join-Path $provenanceFresh 'audit_correction.py') (Join-Path $provenanceFresh 'scoped-complete')
Pop-Location
```

It requires read access to the protected preexisting fixture trees. In this review, the first restricted partial audit was explicitly superseded by the complete scoped read-only audit; no missing access counted as verification. It writes receipts exclusively into the new audit root and uses only read/replay/Git-inspection operations on the target. `compare_saved_streams.py` preserves the separately executed final comparison payload with its original fixed evidence-output path; do not rerun that historical payload in place. Its exclusive write prevents overwriting the final receipt. To repeat it, redirect only its copied `out` variable to the fresh provenance root after the fresh full audit.

## Intake seal

`seal_review.py` creates the first seal only and refuses an existing destination ZIP/receipt. It includes the reviewed builder ZIP, reports, identities, full independent component evidence and all 72 fault logs. It excludes redundant extracted builder files and disposable pytest temp trees. `FILE_MANIFEST.json` lists every included payload file; `INTAKE_RECEIPT.json` records the independently reopened ZIP's size/hash/entry count and complete verification. These packaging operations perform no tests, commissioning or target writes.
