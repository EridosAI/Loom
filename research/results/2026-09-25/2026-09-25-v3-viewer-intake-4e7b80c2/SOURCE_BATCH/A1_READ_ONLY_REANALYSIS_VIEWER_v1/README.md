# First A1 — derived V3 analysis and passive viewer

V3 COMPLETED — checks support the reviewed boundary claim. This reanalyses the original 91.83-second A1; it does not replace its canonical evidence package or run another trajectory.

1. Extract this derived package into a folder.
2. Double-click **OPEN_A1_VIEWER.cmd**. A local browser viewer opens. Close the small launch window when finished; the preview also stops after 30 minutes.
3. Read **V3_READ_ONLY_REANALYSIS_REPORT.md**, **V3_RESULT_v1_1.json**, **VIEWER_DATA_FLOW.md**, and **VIEWER_VERIFICATION.md**.
4. **STATIC_VIEWER_VALIDATION.html** and **screenshots/** show the four requested recorded states and force/integrity detail.

Python 3 is used only for the read-only server and analysis; the existing pinned interpreter is selected on Jason's machine, with `py -3` as the portable fallback. No package installation is needed. No simulation/Engine module is imported. The viewer has no live control interface.

The exact historical **FIRST_A1_COMMISSIONING_RESULT.zip** is preserved under **references/**. The original failed V3 checker and all its error/limitation artifacts remain inside that archive, byte-identical. New versioned analysis files live only in this derived folder. **HASH_BEFORE.json**, **HASH_AFTER.json** and **CUSTODY_PROOF.json** document custody; **FILE_MANIFEST.json** identifies the derived payloads.

Mover pose is shown from actual 0.1-second controller-geometry samples, with sample age. Exact sub-step events retain their own pose/reserves; other channels keep labelled native sample times. There is no display interpolation, physical replay, continuation, new controller calculation, RNG consumption, tuning, efficacy claim or new commissioning result.
