# A3 launch packet — review only

Start with [the plain-language launch packet](A3_LAUNCH_PACKET.md), then [the exact procedure](PROCEDURES.md) and [parallel event interpretations](INTERPRETATION.md).

**NOT AUTHORIZED / NOT EXECUTED.** Canonical authority SHA-256: `43a40bad2a7fbc8939a941ef190be8967aa5453eeaab8f537e6bfea2955769fd`.

`A3_MANIFEST.json` contains a null execution grant. The canonical object excludes only that grant and binds the healthy snapshot, procedure/interpretation documents, controller stages/constants/implementation, code/runtime/configuration, source identities and budgets. `FILE_MANIFEST.json` inventories every payload; `DELIVERY_RECEIPT.json` beside the ZIP reports its independent hash and verification.

The standard-library `validate_packet.py` can check this folder or its ZIP without importing Loom or evolving a world. It is a saved-byte validator, not a launch script. `build_packet.py` and `finish_review.py` are audit sources whose authoring paths refer to the original local workspace; they are not portable launchers. No A3 launcher, approval object or double-click execution action is supplied.

Full unchanged instrument/configuration/lockfile are under `instrument/`; reused history under `verified-cache/`; exact source documents and full A2 evidence chain under `references/`. Historical scripts/grants inside those reference archives are historical data, not instructions to execute.

Read [no-execution evidence](NOT_EXECUTED.md) and [preparation helper history](preparation-history/PREPARATION_HISTORY.md). Separate approval is required for any run, retry, route change, continuation, other arm or correction. Stop at Jason's review.
