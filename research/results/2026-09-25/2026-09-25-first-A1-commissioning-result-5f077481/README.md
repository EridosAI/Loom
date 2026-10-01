# First A1 commissioning result

Read `FIRST_A1_COMMISSIONING_REPORT.md`, then `evidence/read-only-review/A1_RESULT_SUMMARY.json`. Exact authority: `a744982d245d479a36fdc47c49f0459c24da2b0a1de109e947e543d1a06023dc`. One attempt at apparatus `5f07748102cb5eaa302569c87efbae095050e9fe`; unchanged P `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.

The attempt stopped as `administrative_pause` at 91.83 simulated seconds; cause `wall_time_limit`. This is one externally controlled physical witness, with no P learning or survival verdict. Any unobserved remainder is untested. No retry, resume or patch was made.

V1, V2 and A0 completed. V3's post-check is incomplete: the execution's read-only checker incorrectly expected the sensor and native stream counts to match, overlooking the recorder's initial display envelope. Its original error and code are preserved, with a separate explanation in `evidence/read-only-review/V3_POST_CHECK_LIMITATION.md`. No corrected checker was run. This is not an all-checks-clear commissioning result.

## Contents

- `evidence/`: exact primary evidence tree, including approval source/envelope, launched manifest, complete trajectory streams and snapshots, progress, outcome and read-only calculations.
- `approved-launch/FIRST_COMMISSIONING_LAUNCH_PACKET.zip`: byte-exact approved preparation packet, including canonical authority, procedure, helper, instrument sources, runtime/configuration identities and verified cache. It retains its original proposal labels; the later genuine approval is in the evidence tree.
- `FIRST_A1_COMMISSIONING_REPORT.md`: readable copy of the report also retained under `evidence/read-only-review/`.
- `PRESERVATION_CHECK.json`: exact original-file, packet and evidence inventory; component limits and pre-copy navigation checks.
- `packaging/package_result.py`: custody utility used to prepare this delivery.
- `FILE_MANIFEST.json`: SHA-256 and size of each payload file; the manifest excludes itself. The external delivery receipt records the ZIP identity and verification.

Historical absolute host paths in authority, grants, manifests and snapshots remain unchanged. This archive supplies review evidence; it is not a relocated executable grant. Included execution scripts are provenance and must not be rerun to review the records. No physical replay or portable execution is claimed.

Native records, field/state identities, all event operands, actual issued controller decisions, sensor/diagnostic records and initial/final/native-1000 snapshots are retained. External mode leaves the neural object inactive and wave stream empty. Arithmetic observations and any recorded validation errors are reported separately from P's scientific status.

The new Workbench INBOX delivery is a preserved copy only. Existing research navigation, source archives, canon and Git are unchanged by this packaging step.
