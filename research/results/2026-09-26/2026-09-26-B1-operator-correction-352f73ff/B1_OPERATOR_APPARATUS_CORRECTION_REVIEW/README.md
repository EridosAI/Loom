# B1 apparatus correction: independent review package

**Checkpoint:** `352f73fffa6d9781eae8aa38e708a9a05669588f`  
**Parent:** `68db2c581f07200966d699a4f55a65f9b96df1e9`  
**P:** `6bc9683b54e4fa80136fe8534d7713e2a250a95f`  
**Status:** apparatus correction implemented and component-tested; independent narrow review pending. No B1 launch-fitness declaration or execution authority.

Read [the report](docs/B1_OPERATOR_APPARATUS_CORRECTION_REPORT.md), [information flow](docs/CHEMISTRY_DEPRIVATION_INFORMATION_FLOW.md), [lifecycle](docs/LIVE_OPERATOR_STATE_MACHINE.md), and [RED→GREEN matrix](docs/RED_GREEN_MATRIX.md). Exact branch/worktree are in `CHECKPOINT.json`; exact code/tests/docs diff and commit record are at this level.

## Evidence

- Final worktree: 204 passed in 143.82 seconds. Final byte-identical portable source: 204 passed in 143.73 seconds.
- Final A–L matrix: 12 deliberate, consequential assertion failures and 12 passing controls. Earlier runs remain labeled separately.
- Two baseline failures against unmodified 68db are preserved. Their expected nonzero result is evidence, not an unresolved regression.
- `source/developmental_ecology` is the tested portable tree. `baseline-68db/developmental_ecology` is a read-only baseline copy for review. Each includes the existing lawful component cache; neither includes held B1 state.
- Full raw logs/JUnit and final component records are under `evidence`. Actual-physics tests use invented/manufactured fixtures; fault I and the browser transport use nonphysical synchronization/transport stubs.
- `docs/FINAL_PRESERVATION.json` checks byte identities and committed blobs, including original P/config and parent clock. Existing Git newline filters are respected; the unchanged configuration checkout is CRLF while Git stores LF.
- `docs/STATIC_HELD_COMPATIBILITY.json` is a static result only. It exposes public case identifiers/horizons and opaque snapshot hashes, not evaluator truth. Held custody `45d71cd121f823368401b11c4a1010d509af3224f49168ad528653274d0e7543` stays unchanged and non-launchable.

## Component-only reproduction

Do not run a commissioning launcher, create a new authority, load held fixtures, invoke a legacy inspector against a world, or replay an ecological record during this correction review. Legacy source entry points are included for exact source preservation, not as new authorization. `task-utilities` records this task's local preparation and packaging; those utilities have local paths and are not general launch/reproduction tools.

Use Python 3.13.5 and the pinned `requirements-lock.txt`, with Node v22.16.0 on PATH (or `NODE_BIN` set to its executable). The delivered runtime JSON records actual package/executable content identities. No runtime installation is bundled. From `source/developmental_ecology`, run the explicitly authorized component suite:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
$env:PYTHONPATH = (Get-Location).Path
python -B -X utf8 -m pytest tests tests_apparatus -q -p no:cacheprovider --junitxml=review-component-results.xml
```

The existing cached prehistory is required by legacy component tests. Preserve it; do not generate a new cache. Node is a test tool, not a live feedback path.

For a single fault/control check, select its exact node from the saved matrix. Set `B1_FAULT` to the letter only for the RED invocation, expect the named single assertion failure, then remove the environment value and repeat for GREEN. Example H, both manufactured:

```powershell
$env:B1_FAULT = 'H'
python -B -X utf8 -m pytest tests_apparatus/test_b1_operator.py::test_H_duplicate_token -q -p no:cacheprovider
Remove-Item Env:B1_FAULT
python -B -X utf8 -m pytest tests_apparatus/test_b1_operator.py::test_H_duplicate_token -q -p no:cacheprovider
```

These instructions reproduce component evidence, not PC/B1 trials. No new tests were executed merely to package this delivery.

## Integrity and boundaries

`PAYLOAD_MANIFEST.json` hashes every other package file. `ARCHIVE_RECEIPT.json` alongside the ZIP records its hash/size and successful archive verification. Opaque hashes are custody evidence, not grants. The package has no sealed evaluator snapshot/manifest/archive or B1 execution authority.

No prepared positive control, B1, ecological trajectory or ecological replay occurred. Existing and new manufactured reconstruction checks are disclosed. No new prehistory, tuning, P/config/world change, push, PR, merge or vault Git write occurred. Historical A1–A5 evidence is unchanged. Interactive history-growth cost and actual human competence remain untested. Stop for narrow independent correction review; later packet regeneration/authorization is a separate decision.
