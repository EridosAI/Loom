"""Seal and archive the held review proposal; saved bytes only, no Loom imports."""
import hashlib,json,pathlib,zipfile
from validate_packet import verify
S=pathlib.Path(__file__).resolve().parent;ROOT=S.parent
O=ROOT/'exports/2026-09-26-A5-launch-packet-HOLD-5f077481'
DEL=ROOT/'exports/2026-09-26-A5-launch-delivery-HOLD-5f077481'

def sha(p):
    with pathlib.Path(p).open('rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
def write(n,v):(O/n).write_text(json.dumps(v,indent=2,ensure_ascii=False,allow_nan=False)+'\n',encoding='utf-8')

def main():
    assert not (O/'FILE_MANIFEST.json').exists() and not DEL.exists()
    h=sha(O/'AUTHORITY_OBJECT.canonical.json');checks=json.loads((O/'PREPARATION_CHECKS.json').read_bytes())
    (O/'README.md').write_text(f'''# A5 launch proposal — HOLD, not executed

The full A5 proposal is prepared for review, but **it is not ready for execution on the pinned apparatus**. A source-and-scalar-arithmetic check found that the absolute clock guard would reject a nonterminal command at about **269.5 simulated seconds**, before the first planned revisit. No production failure or A5 physical outcome is claimed. No fix, workaround or shorter substitute has been made.

The proposed **630-second** witness follows **source 0 → source 1 → source 0 → source 1**, starting from the exact healthy A1/A2 zero-time fixture. It uses the unchanged controller, world, stocks, renewal law, expenditure, body and P configuration. The nominal 17 m route and fixed source/departure windows give approximately 210–222 s unattended renewal opportunities. They are planning estimates; actual contact, transfer, E/I and nonterminal completion remain unobserved.

| Review item | Exact packet document |
|---|---|
| Plain-language route, dwell/revisit schedule, rationale and limits | [PROCEDURES.md](PROCEDURES.md) |
| Exact single-case manifest / initial state | [A5_MANIFEST.json](A5_MANIFEST.json) / [INITIAL_STATE_SUMMARY.json](INITIAL_STATE_SUMMARY.json) |
| Complete copied initial state | [INITIAL_A5.snapshot.json.gz](INITIAL_A5.snapshot.json.gz) |
| New static blocker and source evidence | [OPEN_ISSUE_A5_CLOCK.md](OPEN_ISSUE_A5_CLOCK.md) / [CLOCK_AUDIT.json](CLOCK_AUDIT.json) |
| All-source accounting and bounded interpretation | [OBSERVATION_AND_INTERPRETATION.md](OBSERVATION_AND_INTERPRETATION.md) |
| Measured resource basis and hard administrative instructions | [RESOURCE_PLAN.md](RESOURCE_PLAN.md) / [RESOURCE_PROJECTION.json](RESOURCE_PROJECTION.json) |
| Full passive replay/stock plotting record contract | [VIEWER_RECORD_CONTRACT.md](VIEWER_RECORD_CONTRACT.md) |
| Approval/hold boundary | [REVIEW_AND_EXECUTION_BOUNDARY.md](REVIEW_AND_EXECUTION_BOUNDARY.md) |

Conditional full-run projection: **roughly 2.0–2.1 wall hours**, with a proposed **4-hour runner ceiling + 1 hour saved-data reporting**. The growing restart-history estimate is about 0.44–0.48 GB stored; allow 1 GB for trajectory planning. Caps: 1.5 GB uncompressed streams and 10 GB combined new disk usage/copies, with 1 GB finalization reserve. Full native fidelity is preserved. The resource proposal does not override the clock hold.

**Canonical held authority-object SHA-256:**

`{h}`

[Readable object](AUTHORITY_OBJECT.json) · [canonical UTF-8 bytes](AUTHORITY_OBJECT.canonical.json). This is the normal single-case execution object with only the null grant excluded, binding every case term and the HOLD. The existing authorization gate rejects the null grant. The hash identifies the review proposal; **it is not a launch-ready approval target, and approval cannot silently remove its hold**. A separate scoped clock decision and, if the instrument changes, a new verified checkpoint/packet/authorization are required.

Pinned P: `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. Apparatus: `5f07748102cb5eaa302569c87efbae095050e9fe`. Worktree: `C:\\Users\\Jason\\Desktop\\Eridos\\Loom-p-apparatus-20260924-01a0c405`; branch `build/p-commissioning-apparatus-20260924-01a0c405`. No new commit or Git write. [Code/runtime identities](CODE_AND_RUNTIME_IDENTITIES.json) and [source identities](SOURCE_IDENTITIES.json) include the unchanged record chain through A4; the full sealed A4 result carries earlier launches/results transitively.

Preparation verification: **zero world/field/neural steps, zero computed controller commands, zero RNG draws, zero sensor evaluations, zero new prehistory, zero replay and zero candidate trials**. The original snapshot was copied and decoded as inert data, with no Engine or Run object. Guarded preparation and portable saved-byte validation passed; those do not establish launch fitness. All **{checks['original_files_checked']} scoped original files** retained their hashes. The actual code worktree remains clean. [Preparation checks](PREPARATION_CHECKS.json) · [preservation](PRESERVATION.json).

No A5 run, route outcome, productive revisit, physical viability, renewed uptake, future stock plot, full-horizon performance or P efficacy has been tested. The stock ledger can support a passive all-source plot after genuine records exist; no simulated stock trace is fabricated now. There is no executable launch wrapper or live viewer in this packet.

The portable validator reads saved bytes only: `python -B validate_packet.py` in this extracted folder, or supply the ZIP path. It verifies the held disposition rather than certifying runtime fitness. The authoring/sealing/copy utilities are preparation provenance, not launch commands; their original paths and refuse-existing-output guards are retained. Historical nested archives contain historical tools and approvals as immutable evidence, not current execution instructions.

**Stop for Jason's review.** The unresolved clock compatibility needs a separately scoped decision before a launch-ready A5 object can be produced. The bounded renewal question and proposed 630-second horizon are preserved.
''',encoding='utf-8')
    result=verify(lambda n:(O/n).read_bytes(),[p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()],False)
    write('STATIC_VALIDATION.json',result)
    before=json.loads((O/'HASH_BEFORE.json').read_bytes());assert all(sha(p)==v for p,v in before.items())
    m=json.loads((O/'A5_MANIFEST.json').read_bytes());assert not pathlib.Path(m['execution']['procedure']['protocol']['record_destination']).parent.exists()
    files={p.relative_to(O).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(O.rglob('*')) if p.is_file()}
    write('FILE_MANIFEST.json',{'schema':1,'authority_sha256':h,'disposition':'HOLD_CLOCK_INCOMPATIBILITY','files':files})
    sealed=verify(lambda n:(O/n).read_bytes(),[p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()])
    DEL.mkdir(parents=True);zp=DEL/'A5_LAUNCH_PACKET_HOLD.zip'
    with zipfile.ZipFile(zp,'x',compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
        for p in sorted(O.rglob('*')):
            if p.is_file():z.write(p,p.relative_to(O).as_posix())
    with zipfile.ZipFile(zp) as z:archived=verify(z.read,z.namelist())
    receipt={'packet_directory':str(O),'zip':str(zp),'zip_sha256':sha(zp),'zip_bytes':zp.stat().st_size,'payload_count':len(files),
      'authority_sha256':h,'launch_ready':False,'disposition':'HOLD_CLOCK_INCOMPATIBILITY','directory_verification':sealed,'archive_verification':archived,'zero_simulation_execution':True}
    (DEL/'DELIVERY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
