"""exp20_ubuf.py — EXP20 U-BUF gate executors (prereg §6/§7): G0 fabric-hash + K=1 REUSED,
G2 map asserts + multiplicity companion + delivered-stratum support, and the delivered-stratum
cutter. G1 = exp20_diffscope.main() (B11 both layers + blast radius, planted-red per invocation).

Modes:
  --fixtures        the observed-red set that needs no runs: causality plant (deliver[t] = t+1
                    MUST fire), length plant, cutter hand-fixtures, empty-support red
  --g0 [--full]     fabric-field identity (ubuf vs dwell) + K=1 REUSED bit-identity vs a fresh
                    exp12_dwell run AND vs the committed pre-delta anchor — the consumed-RNG-draw
                    broken variant runs FIRST and must be observed red
  --g2 [--seeds a,b] map asserts + multiplicity + delivered-stratum support per K per seed at the
                    verdict fabric scale (T = 1M + 8), from the real data path

The delivered-stratum cutter (prereg §3): FORM re-derived from the committed EXP19 cutter
(exp19_score.py:46 `_zero_preceding = is_exam & _first_occ(dwell_id)` — "no contaminating wave
before the exam", where the contamination channel is the one the shortcut lives in). On the
delivered stream the shortcut is same-MEMBER replay within the buffer's reach, so the transported
form is: onset exam at t is delivered-zero-preceding iff NO same-member wave was DELIVERED in the
trailing window W. W is a PRE-FLIGHT constant (primary derivation W = K, the buffer's own reach;
W = 2K and W = inf ride as measured alternatives) — the package carries the derivation + measured
support per candidate; nothing reads through the cutter before touch-2 ratification.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import torch

torch.set_num_threads(1)
import exp12_arms as X12
import exp12_fabric as F
import exp14_arms as XA

HERE = Path(__file__).resolve().parent
OUTDIR = HERE / "exp08"
GATELOG = OUTDIR / "exp20_gatelog.json"
PAID_K = (32, 128, 512)
VERDICT_SEEDS = list(range(8))            # the committed verdict-seed set (exp19_corridor.py:34)
READ_AT_1M = 1_000_000
FAB_FIELDS = ("raw", "cat", "mask_slot", "is_exam", "dwell_id", "nuis", "bg", "member",
              "pos", "is_probe_exam")


def _gatelog_update(gate: str, payload: dict) -> None:
    log = json.loads(GATELOG.read_text()) if GATELOG.exists() else {}
    log[gate] = payload
    GATELOG.write_text(json.dumps(log, indent=2))


# ------------------------------------------------------------------ map asserts (G2 core)

def causality_assert(deliver: torch.Tensor, T: int) -> None:
    """Prereg §2 asserts replacing wp-multiset: causal (deliver[t] <= t, every t) + length == T."""
    assert deliver.shape[0] == T, f"deliver length {deliver.shape[0]} != T {T} — HALT"
    idx = torch.arange(T)
    bad = (deliver > idx).nonzero(as_tuple=True)[0]
    assert bad.numel() == 0, \
        f"CAUSALITY VIOLATION: deliver[{int(bad[0])}] = {int(deliver[bad[0]])} > t — HALT"
    assert int(deliver.min()) >= 0, "negative delivery index — HALT"


def multiplicity(deliver: torch.Tensor, read_at: int) -> dict:
    """The multiplicity companion (prereg §2): realized per-wave delivery-count histogram over
    waves [0, read_at) as delivered during [0, read_at) — reported, never assumed."""
    counts = torch.bincount(deliver[:read_at].clamp_max(read_at - 1), minlength=read_at)
    hist = torch.bincount(counts.clamp_max(12), minlength=13)
    return dict(p_never=round(float((counts == 0).float().mean()), 5),
                mean=round(float(counts.float().mean()), 5),
                max=int(counts.max()),
                count_hist_0_to_12=[int(h) for h in hist])


# ------------------------------------------------------------------ delivered-stratum cutter

def delivered_zero_preceding(member: torch.Tensor, deliver: torch.Tensor | None,
                             is_exam: torch.Tensor, W: int | None, read_at: int) -> torch.Tensor:
    """Cutter (prereg §3; form transported from exp19_score.py:46, see module docstring).
    Returns a bool mask over waves [0, read_at): True at onset exams with NO same-member wave
    DELIVERED in the trailing window W (W=None => infinite window, the committed first-occ form).
    deliver=None => identity (the K=1 arm)."""
    dm = member if deliver is None else member[deliver]
    last_del = {}
    out = torch.zeros(read_at, dtype=torch.bool)
    for t in range(read_at):
        if bool(is_exam[t]):
            ld = last_del.get(int(member[t]), None)
            clean = ld is None if W is None else (ld is None or (t - ld) > W)
            out[t] = clean
        last_del[int(dm[t])] = t
    return out


def support_check(member, deliver, is_exam, read_at, K: int) -> dict:
    """Estimator-support check (CORRIDOR_PROTOCOL rider, standing; wired per prereg §3): the
    delivered-stratum onset population must be non-empty, verified from the real data path.
    Reports the primary derivation (W = K) plus the measured alternatives (W = 2K, W = inf)."""
    n_onsets = int(is_exam[:read_at].sum())
    out = dict(n_onsets=n_onsets, windows={})
    for label, W in (("W=K", K), ("W=2K", 2 * K), ("W=inf", None)):
        n = int(delivered_zero_preceding(member, deliver, is_exam, W, read_at).sum())
        out["windows"][label] = dict(support=n, frac=round(n / max(1, n_onsets), 5),
                                     empty=(n == 0))
    out["support_ok_primary"] = not out["windows"]["W=K"]["empty"]
    return out


# ------------------------------------------------------------------ fixtures (observed red)

def fixtures():
    reds = {}
    # causality plant: deliver[t] = t + 1 MUST fire (the order's named falsifier)
    d = torch.arange(100)
    d[41] = 42
    try:
        causality_assert(d, 100)
        raise SystemExit("CAUSALITY FIXTURE FAILED TO FAIL — no observed red")
    except AssertionError as e:
        reds["causality_planted_t_plus_1"] = str(e)[:90]
    # length plant
    try:
        causality_assert(torch.arange(99), 100)
        raise SystemExit("LENGTH FIXTURE FAILED TO FAIL")
    except AssertionError as e:
        reds["length_plant"] = str(e)[:90]
    # cutter hand-fixture: member [0,1,0,2], identity delivery, onset at t=2 (member 0, last
    # delivered at t=0 -> gap 2): W=1 clean, W=3 contaminated, W=inf contaminated
    mem = torch.tensor([0, 1, 0, 2])
    ex = torch.tensor([False, False, True, False])
    assert bool(delivered_zero_preceding(mem, None, ex, 1, 4)[2])
    assert not bool(delivered_zero_preceding(mem, None, ex, 3, 4)[2])
    assert not bool(delivered_zero_preceding(mem, None, ex, None, 4)[2])
    reds["cutter_hand_fixture"] = "W=1 clean / W=3 contaminated / W=inf contaminated — all as computed"
    # empty-support red: every onset contaminated => support 0 must be FLAGGED empty
    mem2 = torch.tensor([0, 0, 0, 0])
    ex2 = torch.tensor([False, True, True, True])
    sc = support_check(mem2, None, ex2, 4, K=8)
    assert sc["windows"]["W=K"]["empty"] and not sc["support_ok_primary"], \
        "empty-support fixture FAILED to flag"
    reds["empty_support_flagged"] = "support 0/3 at W=K flagged empty (the rider's red)"
    _gatelog_update("fixtures_observed_red", {**reds, "result": "ALL RED OBSERVED"})
    print("FIXTURES: causality t+1 plant fires · length plant fires · cutter hand-fixture exact · "
          "empty-support flagged", flush=True)


# ------------------------------------------------------------------ G0

def _record_equal(ra: dict, rb: dict, skip=("arm", "eb_onsets", "commit_hash")) -> list:
    diffs = []
    for k in ra:
        if k in skip or k not in rb:
            continue
        if ra[k] != rb[k]:
            diffs.append(k)
    return diffs


def g0(full: bool = False):
    torch.set_num_threads(1)
    out = {}
    # (a) fabric-field identity: the U-BUF arm HOLDS the certified fabric byte-identical
    T = (READ_AT_1M if full else 20_000)
    t0 = time.time()
    ld, _s, _c = X12.build_exp12("exp12_dwell", 0, T)
    lu, _s, _c = X12.build_exp12(X12.exp20_ubuf(32), 0, T)
    for f in FAB_FIELDS:
        assert torch.equal(getattr(ld.stream, f), getattr(lu.stream, f)), \
            f"FABRIC FIELD {f} DIFFERS dwell vs ubuf_K32 — the fabric is NOT held — HALT"
    ka, kb = dict(ld.stream.substreams), dict(lu.stream.substreams)
    assert kb.pop("ubuf") == F.SEED_UBUF + 0 and ka == kb, "substream keys differ beyond 'ubuf'"
    out["fabric_hold"] = f"all {len(FAB_FIELDS)} fabric fields torch.equal at T={T} " \
                         f"({round(time.time()-t0, 1)}s); substreams differ ONLY by 'ubuf'"

    # (b) manifest-vs-committed baseline (instrument regression fence): the dwell build's
    # substream keys must match the committed verdict manifest's
    man = json.loads((OUTDIR / "exp14_exp12_dwell_s0_verdict.manifest.json").read_text())
    mkeys = man["fabric"]["substream_keys"]
    assert {k: int(v) for k, v in mkeys.items()} == {k: int(v) for k, v in ka.items()}, \
        "dwell substream keys drifted from the committed verdict manifest — HALT (regression)"
    out["manifest_anchor"] = "substream keys == committed verdict manifest s0 (fabric block)"

    # (c) K=1 REUSED bit-identity — BROKEN VARIANT FIRST (one consumed RNG draw from the live
    # training generator), observed red; then the proper short-circuit, green.
    N = 2000
    rd = XA.run_exp14_arm("exp12_dwell", 0, read_at=N, h_max=N, out_tag="g20dwell",
                          checkpoint=False)
    orig_bw = X12._buffer_wave

    def _broken_bw(loop, *a, **k):
        if not getattr(loop, "_g0red", False):
            loop._g0red = True
            _ = torch.rand(1, generator=loop.gen)             # THE consumed draw
        return orig_bw(loop, *a, **k)

    X12._buffer_wave = _broken_bw
    try:
        rk_broken = XA.run_exp14_arm(X12.exp20_ubuf(1), 0, read_at=N, h_max=N,
                                     out_tag="g20k1broken", checkpoint=False)
    finally:
        X12._buffer_wave = orig_bw
    diffs_broken = _record_equal(rd, rk_broken)
    assert diffs_broken, "BROKEN VARIANT FAILED TO GO RED — the bit-identity check cannot see a " \
                         "consumed draw; the gate is asserted, not tested — HALT"
    out["k1_broken_observed_red"] = f"one consumed draw from loop.gen -> record fields diverge: " \
                                    f"{diffs_broken[:4]}"

    rk = XA.run_exp14_arm(X12.exp20_ubuf(1), 0, read_at=N, h_max=N, out_tag="g20k1",
                          checkpoint=False)
    diffs = _record_equal(rd, rk)
    assert not diffs, f"K=1 REUSED NOT bit-identical to exp12_dwell: {diffs} — HALT, never substitute"
    assert rk.get("eb_onsets"), "E-B onset reads absent on the ubuf arm — HALT"
    out["k1_reused"] = (f"K=1 == exp12_dwell digit-exact on every shared record field at N={N} "
                        f"({len(rd['columns'])} columns); E-B additive ({len(rk['eb_onsets'])} "
                        f"onset reads, zero draws)")

    # committed pre-delta anchor, if the config matches (instrument regression fence)
    ref_p = OUTDIR / "exp12_dwell_s0_exp16_predelta_ref.json"
    ref = json.loads(ref_p.read_text())
    if ref.get("read_at") == N and ref.get("probe_rate") == 0.0:
        dref = _record_equal(ref, rd, skip=("arm", "eb_onsets", "commit_hash", "torch_num_threads",
                                            "read_at", "h_max", "mid_ckpt_at"))
        assert not dref, f"fresh dwell diverges from the COMMITTED pre-delta ref: {dref} — HALT " \
                         "(instrument regression, never substitute)"
        out["committed_anchor"] = "fresh dwell == committed exp16_predelta_ref digit-exact"
    else:
        out["committed_anchor"] = (f"pre-delta ref config differs (read_at={ref.get('read_at')}, "
                                   f"probe_rate={ref.get('probe_rate')}) — dwell-vs-dwell anchor "
                                   f"rides on the manifest key check in (b)")
    _gatelog_update("G0", {**out, "result": "PASS (red observed first)"})
    print("G0 PASS:", json.dumps(out, indent=2), flush=True)


# ------------------------------------------------------------------ G2

def g2(seeds=None):
    torch.set_num_threads(1)
    seeds = seeds if seeds is not None else VERDICT_SEEDS
    T = READ_AT_1M + 8
    out = {"T": T, "read_at": READ_AT_1M, "per_seed": {}}
    for s in seeds:
        t0 = time.time()
        loop, _sp, _c = X12.build_exp12("exp12_dwell", s, READ_AT_1M)
        fab = loop.stream
        member, is_exam = fab.member, fab.is_exam
        row = {}
        for K in PAID_K:
            deliver = F.ubuf_map(fab.T, K, torch.Generator().manual_seed(F.SEED_UBUF + s))
            causality_assert(deliver, fab.T)
            row[f"K{K}"] = dict(multiplicity=multiplicity(deliver, READ_AT_1M),
                                support=support_check(member, deliver, is_exam, READ_AT_1M, K))
        row["K1"] = dict(multiplicity=dict(p_never=0.0, mean=1.0, max=1,
                                           note="identity — every wave delivered exactly once"),
                         support=support_check(member, None, is_exam, READ_AT_1M, 1))
        out["per_seed"][s] = row
        empt = [f"K{K}" for K in PAID_K
                if row[f"K{K}"]["support"]["windows"]["W=K"]["empty"]]
        print(f"  s{s} ({round(time.time()-t0, 1)}s): " +
              " | ".join(f"K{K}: p_never {row[f'K{K}']['multiplicity']['p_never']} "
                         f"support(W=K) {row[f'K{K}']['support']['windows']['W=K']['support']}"
                         for K in PAID_K) +
              (f"  EMPTY: {empt}" if empt else ""), flush=True)
    empties = [(s, k) for s, r in out["per_seed"].items() for k, v in r.items()
               if isinstance(v, dict) and v.get("support", {}).get("windows", {})
               .get("W=K", {}).get("empty")]
    out["halt_surfaces"] = ([f"EMPTY delivered-stratum support (W=K) at {e}" for e in empties]
                            if empties else [])
    (OUTDIR / "exp20_g2_maps.json").write_text(json.dumps(out, indent=2))
    _gatelog_update("G2", {"seeds": list(seeds), "halt_surfaces": out["halt_surfaces"],
                           "result": "HALT" if empties else "PASS",
                           "artifact": "exp08/exp20_g2_maps.json"})
    if empties:
        print("G2 HALT — empty delivered-stratum support:", empties, flush=True)
        sys.exit(3)
    print("G2 PASS -> exp08/exp20_g2_maps.json", flush=True)


if __name__ == "__main__":
    if "--fixtures" in sys.argv:
        fixtures()
    elif "--g0" in sys.argv:
        g0(full="--full" in sys.argv)
    elif "--g2" in sys.argv:
        sd = None
        if "--seeds" in sys.argv:
            sd = [int(x) for x in sys.argv[sys.argv.index("--seeds") + 1].split(",")]
        g2(sd)
    else:
        raise SystemExit("modes: --fixtures | --g0 [--full] | --g2 [--seeds a,b,...]")
