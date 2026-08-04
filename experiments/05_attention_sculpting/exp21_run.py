"""EXP21 — corridor-safe run orchestration (prereg §9.1 item 6; gates G3b-launch and G4).

Calibration (authorized through G3b): 2 arms x cal seeds {20,21,22,24,25} x 1M waves, from
scratch, primary+shadow banks scored at every planned read, one process per run
(torch threads = 1; the existing-style scheduling, justified by G0's repeat-run determinism).

Verdict (G4 — NOT AUTHORIZED by the build order): `run_verdict` exists because the gate-executor
audit requires every executor before Touch 2, but it REFUSES to run unless the committed
ratification artifact `exp08/exp21/exp21_touch2_ratified.json` exists with ratified=true —
written only on Jason's word after the Touch-2 pre-flight read. No resume, no tail, no seed
substitution, no artifact overwrite (append-only asserts in the runner). The G4 fixtures below
are fixture-only synthetic route tests (allowed under the hard hold); none touches a
verdict-seed training process.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch

import sys
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))

import exp21_probe as P21                                      # noqa: E402
import exp21_teaching as T21                                   # noqa: E402

OUTDIR21 = T21.OUTDIR21
RATIFY_ARTIFACT = OUTDIR21 / "exp21_touch2_ratified.json"
CAL_TAG, VERDICT_TAG = "cal", "verdict"


def run_cal_one(arm: str, seed: int) -> dict:
    """One calibration run (G3b block). Both banks scored per read; wall time recorded."""
    assert arm in ("on", "off") and seed in T21.CAL_SEEDS21, f"not a cal cell: {arm} s{seed}"
    t0 = time.perf_counter()
    T21.run_exp21_arm(arm, seed, read_at=T21.H21, out_tag=CAL_TAG,
                      probe=("primary", "shadow"))
    dur = time.perf_counter() - t0
    d = dict(arm=arm, seed=seed, tag=CAL_TAG, wall_seconds=round(dur, 1))
    (OUTDIR21 / f"exp21_{arm}_s{seed}_{CAL_TAG}.duration.json").write_text(json.dumps(d))
    return d


def run_verdict(arm: str, seed: int) -> dict:
    """G4 executor — refuses without the committed Touch-2 ratification artifact."""
    assert RATIFY_ARTIFACT.exists() and json.loads(RATIFY_ARTIFACT.read_text()).get(
        "ratified") is True, \
        ("G4 REFUSED: Touch-2 pre-flight package not ratified (missing/false "
         f"{RATIFY_ARTIFACT.name}). The corridor hard-holds before G4.")
    assert arm in ("on", "off") and seed in T21.VERDICT_SEEDS21
    # paired-bank contract: the primary bank must exist and hash-verify BEFORE the run
    bank = P21.load_bank(seed, "primary")                      # hash-asserted on load
    assert not (OUTDIR21 / f"exp21_{arm}_s{seed}_{VERDICT_TAG}.json").exists(), \
        "verdict record exists — append-only; no re-run, no resume"
    t0 = time.perf_counter()
    rec = T21.run_exp21_arm(arm, seed, read_at=T21.H21, out_tag=VERDICT_TAG,
                            probe=("primary",))
    d = dict(arm=arm, seed=seed, tag=VERDICT_TAG,
             wall_seconds=round(time.perf_counter() - t0, 1),
             bank_sha256=P21.bank_digest(bank))
    (OUTDIR21 / f"exp21_{arm}_s{seed}_{VERDICT_TAG}.duration.json").write_text(json.dumps(d))
    return rec


# ------------------------------------------------------------------ G4 fixtures (fixture-only)
def g4_fixtures() -> dict:
    """§7 row G4 observed-red fixtures — every red fires a DEPLOYED law (the build-review
    panel's dead-fixture findings bind here); no verdict-seed training process is
    instantiated (the ratification-refusal red itself proves that)."""
    import exp21_cal as CAL
    import exp21_score as SC
    torch.set_num_threads(1)
    reds = {}

    # unratified launch: run_verdict must REFUSE outright (deployed refusal, verdict seed 0
    # untouched — the refusal fires before any loop is constructed)
    assert not RATIFY_ARTIFACT.exists(), \
        "ratification artifact already exists — it may only be written on Jason's word"
    try:
        run_verdict("on", 0)
        raise SystemExit("G4 fixture: run_verdict LAUNCHED without ratification — HALT")
    except AssertionError as e:
        reds["unratified_launch"] = dict(red=True, message=str(e)[:160],
                                         note="no loop constructed, no verdict-seed process "
                                              "instantiated")

    # resume_attempt: a stale checkpoint at the cell must make the RUNNER's deployed
    # fresh-cell law refuse (from-scratch only; cal seed 20 — never a verdict seed)
    stale_ckpt = OUTDIR21 / "exp21_on_s20_g4res.ckpt_read.pt"
    stale_ckpt.write_bytes(b"stale")
    try:
        T21.run_exp21_arm("on", 20, read_at=300, checkpoint=False, probe=(),
                          out_tag="g4res")
        raise SystemExit("G4 fixture: runner RESUMED over a stale checkpoint — HALT")
    except AssertionError as e:
        reds["resume_attempt"] = dict(red=True, message=str(e)[:160])
    finally:
        stale_ckpt.unlink()

    # paired_bank_mismatch: the DEPLOYED pair-share law (exp21_score.assert_pair_share)
    p = P21.build_bank(20, "primary")
    s = P21.build_bank(20, "shadow")
    try:
        SC.assert_pair_share(dict(seed=20, bank_sha256=P21.bank_digest(p)),
                             dict(seed=20, bank_sha256=P21.bank_digest(s)))
        raise SystemExit("G4 fixture: pair-share law blind to a bank mismatch — HALT")
    except AssertionError as e:
        reds["paired_bank_mismatch"] = dict(red=True, message=str(e)[:160])

    # step_count_mismatch: the DEPLOYED completeness laws must fire on a truncated record
    # and on a truncated read grid (the silent-truncation finding)
    fake = dict(read_at=500_000, columns=[dict(t=499_800)])
    try:
        CAL.assert_record_complete(fake, T21.H21)
        raise SystemExit("G4 fixture: record-completeness law blind to a 500k record — HALT")
    except AssertionError as e:
        msg1 = str(e)[:120]
    try:
        CAL.assert_grid_complete([0, 3000, 6000], T21.H21)
        raise SystemExit("G4 fixture: grid-completeness law blind to truncation — HALT")
    except AssertionError as e:
        reds["step_count_mismatch"] = dict(red=True, record_message=msg1,
                                           grid_message=str(e)[:120])

    # record_overwrite: the runner's deployed append-only law must fire on an existing record
    probe_target = OUTDIR21 / "exp21_on_s20_g4ow.json"
    probe_target.write_text("{}")
    try:
        T21.run_exp21_arm("on", 20, read_at=300, checkpoint=False, probe=(),
                          out_tag="g4ow")
        raise SystemExit("G4 fixture: runner OVERWROTE an existing record — HALT")
    except AssertionError as e:
        reds["record_overwrite"] = dict(red=True, message=str(e)[:120])
    finally:
        probe_target.unlink()

    T21.gatelog_append(dict(gate="G4-fixtures", outcome="OBSERVED-RED (fixture-only)",
                            executor="exp21_run.g4_fixtures", reds=sorted(reds),
                            note="G4 NOT RUN; VERDICT SEEDS UNTOUCHED"))
    print("G4 fixtures (fixture-only) reds:", sorted(reds))
    return reds


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--cal", nargs=2, metavar=("ARM", "SEED"))
    ap.add_argument("--g4-fixtures", action="store_true")
    args = ap.parse_args()
    torch.set_num_threads(1)                                   # the determinism contract
    if args.cal:
        run_cal_one(args.cal[0], int(args.cal[1]))
    elif args.g4_fixtures:
        g4_fixtures()
