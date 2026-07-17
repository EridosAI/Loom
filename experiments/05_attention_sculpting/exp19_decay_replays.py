"""exp19_decay_replays.py — the decay micro-arm + dec_cat endpoint replays (docs/EXP19_DECAY_MICROARM.md).

Phase A (first, Jason's sequencing): 8 × exp12_dwell (A_dwell) replays — the B=1 dec_cat endpoint.
Phase C (second): 7 × exp12_shuffle s1–7 re-replays (s0 already dec_cat-bearing) — the B=T endpoint + the
decay-mechanism read. Trains NOTHING: deterministic replay of committed trajectories at each record's OWN
committed params (read from the record — provenance computed, never assumed), HEAD column instrument
(dec_cat rides as the additive field).

ANCHOR DISCIPLINE (REUSED-class): every replay must reproduce its committed record digit-exact on every
PRE-EXISTING column field + acquisition_onset. Mismatch ⇒ HALT the batch (never substitute), report → Jason.
"""
from __future__ import annotations

import hashlib
import json
import sys
import time

import torch

import exp14_arms as XA
import exp19_replay as REP

PHASE_A = [("exp12_dwell", s, "verdict") for s in range(8)]
PHASE_C = [("exp12_shuffle", s, "verdict") for s in range(1, 8)]
OUT_TAG = "dcy"
LOG = XA.OUTDIR / "exp19_decay_replays_log.json"


def _committed(arm: str, seed: int, tag: str) -> dict:
    p = XA.OUTDIR / f"exp14_{arm}_s{seed}_{tag}.json"
    if not p.exists():
        raise SystemExit(f"HALT: committed record missing: {p}")
    return json.loads(p.read_text())


def _anchor_columns(committed: dict, replay: dict) -> tuple[bool, str]:
    """Digit-exact on every PRE-EXISTING field (additive fields — dec_cat — allowed in the replay)."""
    cc, rc = committed["columns"], replay["columns"]
    if len(cc) != len(rc):
        return False, f"column count {len(rc)} != committed {len(cc)}"
    for i, (a, b) in enumerate(zip(cc, rc)):
        for k, v in a.items():
            if k not in b or b[k] != v:
                return False, f"col {i} t={a.get('t')} field {k!r}: replay {b.get(k)!r} != committed {v!r}"
    if replay.get("acquisition_onset") != committed.get("acquisition_onset"):
        return False, (f"acquisition_onset {replay.get('acquisition_onset')} != "
                       f"committed {committed.get('acquisition_onset')}")
    return True, "columns digit-exact (pre-existing fields) + acquisition_onset"


def run_batch(items) -> list:
    results = []
    for arm, seed, tag in items:
        com = _committed(arm, seed, tag)
        ra, hm = com["read_at"], com["h_max"]
        t0 = time.time()
        print(f"[{time.strftime('%H:%M:%S')}] replay {arm} s{seed} (committed {tag}: read_at={ra} h_max={hm})",
              flush=True)
        rec, per_onset = REP.capture_run(arm, seed, read_at=ra, h_max=hm, out_tag=f"{OUT_TAG}")
        ok, msg = _anchor_columns(com, rec)
        dc = [c["dec_cat"] for c in rec["columns"] if c.get("dec_cat") is not None]
        po_path = XA.OUTDIR / f"exp14_{arm}_s{seed}_{OUT_TAG}_peronset.json"
        po_path.write_text(json.dumps(dict(arm=arm, seed=seed, read_at=ra, h_max=hm, per_onset=per_onset)))
        digest = hashlib.sha256(po_path.read_bytes()).hexdigest()
        row = dict(arm=arm, seed=seed, committed_tag=tag, read_at=ra, h_max=hm,
                   anchor_ok=ok, anchor_msg=msg, wall_s=round(time.time() - t0, 1),
                   dec_cat_cols=len(dc), dec_cat_mean=(round(sum(dc) / len(dc), 4) if dc else None),
                   peronset_sha256=digest)
        results.append(row)
        _log(results)
        print(f"    anchor={'OK' if ok else 'FAIL'} ({msg}); dec_cat cols={len(dc)} "
              f"mean={row['dec_cat_mean']}; {row['wall_s']}s", flush=True)
        if not ok:
            print(f"HALT: replay of {arm} s{seed} did NOT reproduce its committed record — REUSED-class "
                  "anchor failure, never substitute. Batch stopped; -> Jason.", flush=True)
            sys.exit(1)
    return results


def _log(rows):
    LOG.write_text(json.dumps(dict(microarm="EXP19 decay + dec_cat endpoints (docs/EXP19_DECAY_MICROARM.md)",
                                   rows=rows), indent=2))


if __name__ == "__main__":
    torch.set_num_threads(1)
    phase = sys.argv[1] if len(sys.argv) > 1 else "A"
    items = PHASE_A if phase == "A" else PHASE_C
    print(f"=== decay-replay batch, phase {phase}: {len(items)} replays (sequential; anchor-gated) ===",
          flush=True)
    rows = run_batch(items)
    print(f"=== phase {phase} COMPLETE: {sum(r['anchor_ok'] for r in rows)}/{len(rows)} anchors OK ===",
          flush=True)
