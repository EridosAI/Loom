# Measured initial-stage resource plan

Fixed scope: twelve blank lives, each up to 600 seconds. No later stage is included.

The final-codec benchmark measured 234.9049 wall seconds for 600 simulated seconds, including a save/load at age 300. Conservatively multiplying this complete cost by twelve gives **46.98 minutes expected execution**. This updates the earlier approximate 41-minute estimate. The **66.4-minute (3,984-second) administrative execution allowance remains unchanged**; no observed scaling defect warrants increasing it.

One worker, fixed order. Each life has 332 wall seconds and 83,333,333 primary-store bytes; unused per-life allowance does not extend another life. The total primary ceiling is 1,000,000,000 bytes (the sum of per-life limits is four bytes lower). Native-boundary stop checks and final checkpoint closure are preserved; any atomic operation/closure overrun must be reported and may not justify another launch. The executor tracks aggregate active runner time and primary bytes and stops further launches at either common limit. Human deliberation is not simulated time.

Measured expected primary evidence: **0.627 GB**, plus **0.630 GB** for one final archive. Reserve 1 GB primary, 1 GB archive, 0.25 GB temporary headroom and 0.5 GB bounded derived outputs: **2.75 GB total planning capacity**, excluding the existing shared Python installation. No full-life decompression directory or duplicate per-chart evidence copy is planned.

Separate allowances: 120 seconds read-only launch preflight, 180 seconds passive complete-file/ledger validation, 120 seconds one archive, 900 seconds passive A/B/C analysis. Working-set planning 0.5 GB / process commit 2.5 GB for one worker. These are declared resource envelopes, not guarantees for every contact/solver workload. Check free space and unchanged runtime again immediately before any authorized execution.

All twelve lawful body-absent prehistories are already prepared in this packet; preparation took 10.14 minutes. No field preparation, birth substitution or prehistory regeneration belongs in the later execution allowance. Start only from the exact saved initial snapshots. Do not return to the superseded 57-hour/200-GB envelope.
