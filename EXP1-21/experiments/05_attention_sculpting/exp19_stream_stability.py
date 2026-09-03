"""exp19_stream_stability.py — Phase-1(a) of the ratified EXP19 close-out (Jason 2026-07-20): the
QUALIFIED tag's evidence, clone-recomputable.

Recomputes the terminal panel's stream-stability sweep at the 450 bar (the B=512 full-read op): for every
verdict seed, the pinned certification (SIM_SEED+seed — the corridor's law) PLUS N_STREAMS=200 independent
simulator streams, generator recipe gseed = SIM_SEED + 1_000_003*(k+1) + seed (the panel verifier's scheme,
which reproduced the finder's numbers exactly). Emits per-stream × per-seed null_max/cert, the derived
rates, the per-draw stream-marginal tails, and asserts the RECORDED rates reproduce: s3 22/200 = 0.110,
s0 172/200 = 0.860, modal family count 5, bracket (B512 full count >= 4) in 200/200. The 4.2e-4
stream-marginal tail for s3 (vs the law's advertised 2e-4) is the ledger-52 quantity — the ratified
standing amendment reads the law's bound as stream-MARGINAL, and this artifact is its measurement.
"""
from __future__ import annotations

import json
import sys
from collections import Counter

import torch

import exp14_arms as XA
import exp19_floor as FL
import exp19_scorer as SC

WIDTH = 450                      # the B512 full-read op (g9 ops artifact)
N_STREAMS = 200
STRIDE = 1_000_003               # the panel's stream-seed stride (recorded in the confirmed finding)
SEEDS = list(range(8))
ARM = "exp19_wperm_B512"
RECORDED = dict(s3_rate=0.110, s0_rate=0.860, modal_count=5, bracket_all=200)


def _series(seed: int):
    d = json.loads((XA.OUTDIR / f"exp19_g9_{ARM}_s{seed}_series.json").read_text())
    return d["acq"], d["full_onsets"]


def main():
    torch.set_num_threads(1)
    out = {"recipe": dict(width=WIDTH, n_streams=N_STREAMS, sim_seed_base=FL.SIM_SEED, stride=STRIDE,
                          scheme="pinned gen = SIM_SEED + seed; stream k gen = SIM_SEED + STRIDE*(k+1) + seed",
                          n_sims_per_stream=FL.N_SIMS, band=SC.BAND, arm=ARM, read="full"),
           "per_seed": {}}
    counts_per_stream = [0] * N_STREAMS
    for s in SEEDS:
        acq, ons = _series(s)
        pinned = SC._certify_seed(ons, acq, WIDTH, torch.Generator().manual_seed(FL.SIM_SEED + s))
        grid, win = SC._bin(ons, acq, WIDTH)
        series = FL._series_from_win({str(t): v for t, v in win.items()}, grid)
        obs = FL._longest_run(series, band=SC.BAND)
        cnts = [len(win.get(t, [])) for t in grid]
        vals = [a for a in series if a is not None]
        p_hat = sum(vals) / len(vals)
        null_maxes, certs, tail_hits = [], [], 0
        for k in range(N_STREAMS):
            gen = torch.Generator().manual_seed(FL.SIM_SEED + STRIDE * (k + 1) + s)
            null = FL._sim_null_runs(cnts, p_hat, FL.N_SIMS, gen, band=SC.BAND)
            nm = int(null.max())
            null_maxes.append(nm)
            c = bool(obs > nm)
            certs.append(c)
            counts_per_stream[k] += int(c)
            tail_hits += int((null >= obs).sum())
        out["per_seed"][s] = dict(
            observed_run=obs, p_hat=round(p_hat, 6),
            pinned=dict(null_max=pinned["null_max"], certified=pinned["certified"]),
            stream_null_max=null_maxes, stream_cert=[int(c) for c in certs],
            cert_rate=round(sum(certs) / N_STREAMS, 4),
            null_max_hist=dict(Counter(null_maxes)),
            stream_marginal_tail=dict(hits=tail_hits, draws=N_STREAMS * FL.N_SIMS,
                                      p=round(tail_hits / (N_STREAMS * FL.N_SIMS), 8)))
        print(f"  s{s}: obs {obs} | pinned null_max {pinned['null_max']} cert {pinned['certified']} | "
              f"stream cert rate {out['per_seed'][s]['cert_rate']} | marginal tail "
              f"{out['per_seed'][s]['stream_marginal_tail']['p']:.2e}", flush=True)
    cdist = dict(Counter(counts_per_stream))
    modal = max(cdist, key=lambda k: cdist[k])
    bracket_ok = sum(1 for c in counts_per_stream if c >= 4)
    out["derived"] = dict(full_count_per_stream_hist=cdist, modal_full_count=int(modal),
                          bracket_count_ge4_streams=bracket_ok,
                          note="bracket = B512 full count >= 4 (the B* lower edge is untouched iff 200/200)")
    # ASSERTS vs the recorded panel numbers (the artifact must REPRODUCE the record, not restate it)
    assert out["per_seed"][3]["cert_rate"] == RECORDED["s3_rate"], \
        f"s3 rate {out['per_seed'][3]['cert_rate']} != recorded {RECORDED['s3_rate']}"
    assert out["per_seed"][0]["cert_rate"] == RECORDED["s0_rate"], \
        f"s0 rate {out['per_seed'][0]['cert_rate']} != recorded {RECORDED['s0_rate']}"
    assert int(modal) == RECORDED["modal_count"], f"modal count {modal} != {RECORDED['modal_count']}"
    assert bracket_ok == RECORDED["bracket_all"], f"bracket streams {bracket_ok} != {RECORDED['bracket_all']}"
    assert all(out["per_seed"][s]["pinned"]["certified"] == (s in [0, 3, 4, 5, 6, 7]) for s in SEEDS), \
        "pinned certs do not reproduce the corridor verdict"
    (XA.OUTDIR / "exp19_stream_stability.json").write_text(json.dumps(out, indent=2))
    print(f"WROTE exp19_stream_stability.json — all recorded rates reproduced "
          f"(s3 {out['per_seed'][3]['cert_rate']}, s0 {out['per_seed'][0]['cert_rate']}, modal {modal}, "
          f"bracket {bracket_ok}/200; s3 marginal tail {out['per_seed'][3]['stream_marginal_tail']['p']:.2e})",
          flush=True)


if __name__ == "__main__":
    main()
