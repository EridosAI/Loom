# NON-CANONICAL RESURRECTION SANDBOX

# Declared stop: native Python process failure

The overnight task stopped during **RS-M1-008**, after all twelve pilots had reached 600 s and the mechanical continuation gate had selected the common 4,500 s target. RS-M1-001–007 completed and verified that target. RS-M1-009–012 retain their completed 600 s pilots; their overnight stages never started.

At **2026-10-01 00:31:49.0667367 Australia/Perth**, Windows System event 26 (Application Popup), record 64403, reported:

> Application popup: python.exe - Application Error : The instruction at 0x00007FFAF9D1E20B referenced memory at 0x0000000000000002. The memory could not be read.

The executor's CPU usage remained fixed at 12,754.25 s, its main thread was in `LpcReply` wait, and no further evidence files appeared. This was a native process/application-error boundary, not a recorded Python `ArithmeticError`, biological terminal event or resource cutoff. The failed executor was terminated at approximately 00:37:32 after recording the host evidence. Its supervising execution session then exited with code 1. No simulation was relaunched.

The Windows event does **not** identify the responsible native module or establish a contact-solver, P-law or physical-state defect. The underlying cause remains unresolved. The run was stopped because the executing process was broken, as required by the declared stop rules. No fix or diagnostic world replay was attempted.

## Exact preservation boundary

- Last complete chunk: `chunk-000296801-000296900.ld`.
- Last durable native index: **296,900**.
- Last durable physical age: **2,968.9548705465913 s**.
- Last full causal checkpoint: `overnight-000294000-periodic.ld`.
- That checkpoint's native index / age: **294,000 / 2,939.9548705459583 s**.
- Full causal state at the final durable native row: **unavailable**.
- Exact crashing call and any unflushed rows: **unavailable**.

The complete chunks after the last checkpoint retain native physical observations, actual wave diagnostics, physical accounting events, endpoint P/field hashes and RNG counters. They do not contain a reconstructible full engine at every row. They must not be represented as an exact restart checkpoint. No reconstruction, rewind, retry or continuation was performed.

The native error bypassed the Python exception handler, so no executor `STOP.json`, failure tail or final denominator was written. `HOST_STOP.json` and `HOST_STOP_DENOMINATOR.json` are explicitly **external post-stop review records**, kept outside the original execution directory. No replacement receipt or missing state has been fabricated. The execution directory was sealed byte-for-byte before passive outcome analysis.

The approximate start-to-stop-action wall time was 13,452.373 s, including the error-dialog wait. Preserved primary files total 4,263,565,700 bytes. Neither the seven-hour nor eight-GB ceiling caused this stop. The seven completed continuations and all twelve pilots remain preserved; the incomplete denominator is not treated as twelve completed long histories.

## Evidence

`HOST_FAILURE_OBSERVATION.json` records process identity, timestamps, the Windows message and last file metadata. `HOST_APPLICATION_ERROR.xml` preserves the event record. `EXECUTION_CUSTODY_SEAL.json` binds all 37,909 original execution files. The final passive verification and archive verification describe available evidence only; they do not certify the missing in-flight state or close the native-crash cause.

No P/world/source/motor parameter changed. No Nursery, Founder selection, additional life or next experiment was started.
