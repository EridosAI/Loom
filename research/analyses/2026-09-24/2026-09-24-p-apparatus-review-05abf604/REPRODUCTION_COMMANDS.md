# Independent reproduction commands

These commands reproduce apparatus components only. They do not authorize commissioning, any A/B/C case, a 600-second life, prehistory preparation, or a change to P. The authority fixture is deliberately synthetic and used only by validation functions; it is not an execution grant.

The original worktree and Workbench remain read-only. All generated results go to a new directory. The independent scripts contain the reviewed host's explicit target path; on another host, change that path in a scratch copy after verifying the supplied source identities. Do not run the builder's `package_apparatus.py` stages, old smoke helpers, or prehistory generator.

```powershell
$repo = 'C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405'
$review = 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-24-p-apparatus-review-05abf604'
$python = 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
$env:PYTHONDONTWRITEBYTECODE = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:GIT_OPTIONAL_LOCKS = '0'
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
Remove-Item Env:APPARATUS_FAULT -ErrorAction SilentlyContinue
$scratch = Join-Path $review ('rerun-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $scratch | Out-Null

# Exact worktree suite, including all unchanged 59 P tests and 24 apparatus cases.
Set-Location -LiteralPath "$repo\developmental_ecology"
& $python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp "$scratch\worktree-temp"

# All 16 delivered RED/GREEN pairs. Each RED must exit1 at its intended failure;
# each clean control exits0. FAULT_MATRIX.json records every child command.
& $python -B -X utf8 verify_apparatus.py "$scratch\fault-pairs"

# Privileged/sensor HTTP boundaries, two authorized 0.2-second manufactured
# components, separate SO preservation, one manufactured exception.
& $python -B -X utf8 "$review\reviewer_boundary_probes.py" --target $repo --output "$scratch\boundaries"

# Independent consequential firewall corruption: expected exit1 and named
# SO FIREWALL BREACH assertion; the restored check must exit0.
& $python -B -X utf8 "$review\reviewer_boundary_probes.py" --target $repo --output unused --firewall-mutant
& $python -B -X utf8 "$review\reviewer_boundary_probes.py" --target $repo --output unused --firewall-only

# Validation-only authority counterexamples, manufactured hold/resume and
# one-step clock boundaries. The copied scripts write beside themselves.
New-Item -ItemType Directory -Path "$scratch\physical" | Out-Null
Copy-Item -LiteralPath "$review\physical\probe_runner_authority.py" -Destination "$scratch\physical\probe_runner_authority.py"
Copy-Item -LiteralPath "$review\physical\probe_boundary_clocks.py" -Destination "$scratch\physical\probe_boundary_clocks.py"
Copy-Item -LiteralPath "$review\physical\probe_route_boundary.py" -Destination "$scratch\physical\probe_route_boundary.py"
Copy-Item -LiteralPath "$review\physical\probe_final_until.py" -Destination "$scratch\physical\probe_final_until.py"
& $python -B -X utf8 "$scratch\physical\probe_runner_authority.py"
& $python -B -X utf8 "$scratch\physical\probe_boundary_clocks.py"
& $python -B -X utf8 "$scratch\physical\probe_route_boundary.py"
& $python -B -X utf8 "$scratch\physical\probe_final_until.py"

# Independent per-field poison, detached explicit receiver calculations,
# deterministic selection, alignment and information-route probes.
New-Item -ItemType Directory -Path "$scratch\neural" | Out-Null
Copy-Item -LiteralPath "$review\neural\independent_checks.py" -Destination "$scratch\neural\independent_checks.py"
& $python -B -X utf8 "$scratch\neural\independent_checks.py"

# Portable suite. Extract the byte-verified nested builder ZIP to a NEW scratch
# directory first. This package was located in the Workbench inbox, rather
# than the original worktree path printed by its receipt.
Expand-Archive -LiteralPath "$review\reviewed-inputs\Loom_P_Commissioning_Apparatus_Review_20260924.zip" -DestinationPath "$scratch\portable"
Set-Location -LiteralPath "$scratch\portable\developmental_ecology"
& $python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --basetemp "$scratch\portable-temp"

# Read-only identity/diff checks; use only process-local trust if required.
git -c "safe.directory=$repo" -C $repo rev-list --parents -n 1 05abf60401d08f38750bca589b1c040e10513d7b
git -c "safe.directory=$repo" -C $repo diff --binary 6bc9683b54e4fa80136fe8534d7713e2a250a95f 05abf60401d08f38750bca589b1c040e10513d7b
git -c "safe.directory=$repo" -C $repo diff --exit-code 6bc9683b54e4fa80136fe8534d7713e2a250a95f 05abf60401d08f38750bca589b1c040e10513d7b -- developmental_ecology/loom_p developmental_ecology/configuration.json developmental_ecology/tests EXP1-21
```

The completed original runs used `worktree-temp-002`, `portable-temp-001`, and `faults-attempt-001` inside this export. The first worktree invocation used an incorrect working directory and failed collection while pytest walked a protected Windows profile junction. That setup error is retained in `worktree-suite.log`, excluded from all test and RED counts, and resolved by running from the target's `developmental_ecology` directory. No target change was needed.

The provenance subreview supplies its own saved-record and hash-audit commands. Protected historical pytest artifacts may require scoped read permission. The review obtained no permission to modify those artifacts. Exact per-process fault commands and outcomes remain in `faults-attempt-001/FAULT_MATRIX.json`.
