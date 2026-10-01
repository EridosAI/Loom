# Proposed A2 packet — read this first

Start with [A2_LAUNCH_PACKET.md](A2_LAUNCH_PACKET.md). It describes one proposed 180-second external physical witness and the outstanding uncertainties in plain language. **No A2 execution occurred. The manifest remains unauthorized.**

- [Exact conditional procedure](PROCEDURES.md), including fixed stages, unchanged controller constants, state continuity, recording and stop rules.
- [Parallel interpretation table](INTERPRETATION.md), with no overall outcome pass gate.
- [Exact manifest](A2_MANIFEST.json), [canonical authority object](AUTHORITY_OBJECT.canonical.json) and [SHA-256](AUTHORITY_SHA256.txt).
- [Resource calculation](BUDGET.json), [initial state](INITIAL_STATE_SUMMARY.json), [geometry](GEOMETRY.json), [live code/runtime identities](CODE_AND_RUNTIME_IDENTITIES.json), [source identities](SOURCE_IDENTITIES.json).
- [Preparation checks](PREPARATION_CHECKS.json), [preservation](PRESERVATION.json), and before/after hash inventories.

The packet includes the exact reviewed runtime/configuration, cache and zero-time snapshot. `references/FIRST_A1_COMMISSIONING_RESULT.zip` is the complete unchanged historical A1 evidence, including its historical grant and failed V3 checker. It is reference material only. Separate V3 reanalysis report/result/source references preserve the later corrected conclusion. Do not execute historical scripts or treat an embedded A1 approval as A2 authority.

For portable **static validation only**, run Python 3.13 with `-B -X utf8 validate_packet.py` from the extracted packet. The same validator accepts the path to `A2_LAUNCH_PACKET.zip`. It reads hashes and JSON only and never imports Loom. `FILE_MANIFEST.json` covers every payload except itself; the separate delivery receipt hashes the sealed ZIP. No execution launcher or synthetic approval is delivered.

`build_packet.py` is the host-specific preparation audit source, not an execution command or a portable rebuild entry point. It retains the original absolute input paths and preparation staging layout. The canonical manifest also binds the original local cache and proposed output paths. A reviewer may inspect/validate this archive elsewhere; relocating execution paths requires a newly reviewed object rather than silently rewriting this one.

The exact proposed execution destination is:

`C:\Users\Jason\Desktop\Eridos\Loom-p-apparatus-20260924-01a0c405\developmental_ecology\artifacts\commissioning-A2-20260925-5f077481\trajectory-001`

That destination was absent during preparation and has not been created. Separate approval of the canonical authority object is required before the one proposed case can start.
