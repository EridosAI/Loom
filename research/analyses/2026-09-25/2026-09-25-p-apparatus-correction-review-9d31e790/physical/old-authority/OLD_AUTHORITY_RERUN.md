# Fresh independent 05ab authority counterexample

Date: 2026-09-25. This is a new execution against the preserved old portable source, not an inherited prior result.

**VERIFIED:** the exact old matching grant passes, but the unchanged request bytes and five-field grant also authorize all four internally valid substitutions: external sensor-human, external manual-privileged, intact P, and fixed-structure intervention. The explicit rejection expectation reaches its intended assertion and exits **1**. The exact-grant/observation control exits **0**. Corrected-runtime positive and rejection controls are supplied separately by the coordinating review; the old-source control is not a claim that the old weakness is closed.

| Identity | Value |
|---|---|
| Old checkpoint | `05abf60401d08f38750bca589b1c040e10513d7b` |
| Source root | `exports/2026-09-24-p-apparatus-review-05abf604/portable/developmental_ecology` |
| Old apparatus aggregate | `5dfe2c85b570d1ee84c83d812d883dd39b8bd6d1ffc3797461b7827463ba5058` |
| P aggregate | `63a0241e57756aa5d0fb69c661b59dd9ddb08d53947ffc16005e483caec65ad9` |
| Configuration | `a97335ec22445cacf66831290444f933986774f6a63c9f11626988e6781a7d3a` |
| Actual RED assertion | `OLD 05ab AUTHORITY BREACH: unchanged grant accepts four different arm/controller interventions` |
| RED / control exit | 1 / 0 |

The script asserts that all four loaded apparatus modules come from the old portable path and that the complete apparatus/P aggregate identities match the old reviewed values. Individual source identities and loaded absolute paths are retained in both result JSON files. The old `authorize_execution` checks the request's bytes plus approved case, initial state and duration; it never compares mode/controller or route. Wrong case/duration controls still reject at `execution grant scope mismatch`.

Route omission is also independently causal without constructing a runner. The request names one prescribed route. The same manifest contains no route, while the old `Run` signature accepts a separately supplied `plan`. Detached old `waypoint_command` calls on the unchanged privileged input return `[0.5,0.5]` for the approved point and `[0.5,-0.5]` for the substituted point. Both points, commands and the shared manifest identity are recorded. This is a controller calculation, not world execution.

The existing life-0 cache is read only. The script constructs only its inert initial engine, then verifies its complete state hash remains unchanged at native index/time zero. There are **zero Run constructions, zero native advances and zero new prehistory steps**. The synthetic request says **NOT JASON APPROVAL / NO EXECUTION**. Neither old source nor prior export/artifacts was edited; all new files are in this `old-authority` directory.

Reproduction uses the pinned existing interpreter. Copy the script to a fresh folder before running if the receipts must remain immutable; it writes only beside itself and reads the fixed old portable source path.

```powershell
$python = 'C:\Users\Jason\Desktop\Eridos\Loom-p-engineering-20260921-01a0c405\.venv\Scripts\python.exe'
$probe = 'C:\Users\Jason\.codex\.chatgpt-projects\g-p-6a6fb425222c8191a814fdc0f7d89f97\exports\2026-09-25-p-apparatus-correction-review-9d31e790\physical\old-authority\reproduce_old_authority.py'
$env:PYTHONDONTWRITEBYTECODE = '1'
& $python -B -X utf8 $probe --expect-rejection
# Expected exit 1 at OLD 05ab AUTHORITY BREACH, after writing the results.
& $python -B -X utf8 $probe
# Expected exit 0: exact old grant accepts, observed substitutions preserved.
```

Evidence: `OLD_AUTHORITY_RED.log`, `OLD_AUTHORITY_CONTROL.log`, `OLD_AUTHORITY_RED_RESULTS.json`, `OLD_AUTHORITY_CONTROL_RESULTS.json`, the two clearly labelled synthetic request files, and `reproduce_old_authority.py`.
