# Three-finding mechanical closure map

| Review requirement | Code path | Consequential checks |
|---|---|---|
| A-R1a: reject ambiguous serialized approval | `authority.strict_loads`, `read_approval`, `verify_approval_binding` | Exact two reviewer files; five duplicate RED→GREEN pairs; extra alias envelope rejected; exact unambiguous approved controls |
| Unique canonical semantic values | `authority.canonical`, `validate_protocol_fields`; existing closed manifest/execution schemas | Integer-key coercion RED→GREEN; canonical-name/alias and top/nested mirror conflicts; nested protocol controller/route/intervention shadows RED→GREEN; finite/string-key controls |
| Other supported serialized input | Strict reader in runner/validators/sensor gateway; packed-key uniqueness before P unpacking | Duplicate saved pending pair key; duplicate actuator JSON rejected before submission |
| A-R1b: actual invoked controller | `authority.validate_dispatch`; captured dispatch in `Run.begin_command`; post-call guard | Five actual runner aliases RED→GREEN; same-name proxy; change immediately after check; post-approval constants/route; wrong reconstructed dispatch on resume |
| Actual pair used by physics | Immutable issued decision bytes in `Run.advance` | Original old alias physical counterexample; approved fresh/resumed commands; altered held pair/decision rejected before advance |
| A-R1c: issued state and native progress | `pending.validate_decision`, `validate_pending`; guards before advance/normal close/save/load | Exact old seven-plus-four persistence RED; four mutation pairs; legal seven-plus-three remainder; exact/tolerance/after-deadline preflight |
| Cross-segment continuity | `RestoredSession`, `validate_restored`, source snapshot comparison, parent link and `validate_journal` | Modified loaded state rejected before Recorder; coherent modified saved payload rejected despite updated checksums; journal RED→GREEN; valid parent chain reconstruction |
| Scientific/runtime preservation | No P/config/controller-clock edits | Unchanged 59 P + 24 original apparatus + 30 prior correction checks, 36 previous pairs, byte/hash/tree inventories |

Native progress is the actual index difference from issuance; legal remainder is issued steps minus that difference. Pending time must match the original clock plus native progress within the existing tolerance (or the existing partial terminal interval). Both remaining stage/case endpoints are checked before further advancement. The controller's existing numerical due-time function is unchanged. No physical equation, tolerance, dt, hold duration or controller gain was changed.
