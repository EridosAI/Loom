# B1 minimal closure implementation — review only

Jason accepted `B1_MINIMAL_CLOSURE_DESIGN_v0_2` in substance and authorized this narrow implementation and static packet preparation. **The nine world cases remain unexecuted and ungranted.** This is not a B1 result or an independent review disposition.

The build starts from `b684912eaf7811cd318ee94c77172aca790f3a0d`, whose parent is `1060a17e3dd14c6361f6f15c95bb58fad3110ffc`, whose parent is the last independently reviewed operator checkpoint `352f73fffa6d9781eae8aa38e708a9a05669588f`. Only CSS in `sensor.html` and nine review files changed in that interval. The supplied provenance clarification resolves those identities before the new implementation. There is no material P/world/sensor-law change in that interval.

The new explicit kind is `automated_raw_reference`. Its bound procedure chooses exactly one of FULL, CHEMISTRY-HIDDEN or SENSORY-FREE. The controller law and all constants match the accepted document (SHA-256 `8f0437aaa53bb192dad36f5337340a2cc8a4b7060660445d573f9c5ca473cbe6`). A fresh session starts in SEEK with release count zero. FULL uses the last ten native receptor rows (one at birth), the specified saturation inverse, left/right contrast, drive reduction and angular damping. Front contact immediately enters the exact `(0.05,0.05)` HOLD; three consecutive windows strictly below 0.02 release it on the third decision. HIDDEN omits chemistry throughout its copied input and sets imbalance to zero. SENSORY-FREE receives `None` and always issues `(0.30,0.30)`.

Production changes are confined to `loom_commissioning`:

| File | Change |
|---|---|
| `raw_reference.py` (new) | Fixed law, closed input projection, state validation/reset and typed arm selection. No world object, I/O or RNG. |
| `authority.py` | New kind/procedure identity, live function/constants/schema binding, exact arm and 30-second commissioning validation. |
| `contract.py` | Recognize the explicit external controller kind. |
| `runner.py` | Copy inputs into the pure controller, retain state and decisions, apply existing resource rules before inference, prohibit manual override and continuation. |
| `pending.py` | Validate recorded commands/state transitions against the law and maintain memory continuity in the journal. |
| `validators.py` | Check recorded controller inputs against the actual physical sensory prefix, with chemistry omission where declared. |

The actual native stepping, physical adapter and recorder are unchanged. `clock.py`, `controllers.py` (historical controllers), `operator_view.py`, human UI, all `loom_p` sources, configuration and dependencies are byte-preserved. No P mechanism, world geometry, chemistry, viability, sensor transduction, force law, native/wave/field cadence or historical controller constants changed. No training, tuning, learned model or additional controller was added.

The automated controller receives no pose, source/material/stock labels, field grid, fixture/seed identity, evaluator event, stop reason, annotation or artifact path. Internal SEEK/HOLD memory is recorded separately from the sensory payload. SENSORY-FREE does not even request a sensory display for inference; the trusted recorder independently retains the complete physical/raw evidence. A controller error ends the instrument without issuing a fallback command. Runner-owned terminal/resource boundaries remain in force. A new reference trajectory cannot resume under the old grant; no continuation is commissioned.

## Verification and limits

The focused manufactured suite passes 35 checks. It blocks real physical stepping, field stepping, new prehistory and simulation RNG draws. The scheduler integration exercises the real Run/Recorder with an inert clock adapter, including a ten-tick hold and a manufactured terminal interruption. These are component checks, not ecological smokes. The report explicitly distinguishes those artificial ticks from physical evolution.

RED-before-GREEN evidence began with the new tests failing to import the absent feature. Later negative checks reject forbidden inputs, overrides, changed constants/dispatch, state/command/time substitutions, invalid receptor values and absent execution grants. Two test-harness issues were corrected: the default temporary directory was inaccessible (moved to the permitted project workspace), and an instance-level test spy polluted snapshot attributes (removed before final recording). Neither required a production-law change or any physical run.

Static preparation uses the public A1 zero-time snapshot and its existing verified A-series world-only prehistory. Only body position, heading, time-zero raw transduction and manufactured-start provenance are changed for the three distinct starts. No trajectory outcome or controller response is queried. The complete snapshot for each start is copied byte-for-byte to its three arms. Original inactive organism/RNG state, fields, phase, stocks and other body state remain unchanged. Exact identities, geometry proofs and construction counters accompany the packet.

No full historical audit, replay, world-running smoke, performance benchmark, paired B1 outcome evaluation or P developmental test was run. Actual controller efficacy and automated-run throughput remain unmeasured. Future execution needs Jason's exact authority for each case and the declared preflight/resource checks. A geometry/cache incompatibility, apparatus defect or resource breach must stop work; it does not permit substituted starts, tuning or extra cases.

Historical human FULL-RAW is preserved at 20.2 simulated seconds / 202 human commands as a qualitative observation only. Human CHEMISTRY-HIDDEN remains withdrawn before start at zero seconds/steps/commands. No old sealed human B1 fixture or evaluator contents were opened. v0.1 remains NOT SELECTED. P developmental-selection direction and the accepted B1 closure rule remain unchanged.
