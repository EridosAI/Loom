"""Substrate oracle (Characterisation-Sweep R5-PIN): the G1 line for the sweep.

`oracle_B_rec` answers: can a FRESH substrate, capacity forced open, B-supervised, **with the
deployed SIGReg/spread regime active at deployed strength**, recover B from its OWN emissions
(`vision.emit = p @ W`)? This is the "B representable in the *substrate*, just not acquired"
ceiling — the line gap-3 must not cross by manufacture.

Why a substrate oracle (not the raw `validity_probe.ceiling_B`): the no-word arm reads the live
substrate emissions, not the raw input. A regime can keep B in the raw input while killing it in
emissions (SIGReg drives emissions isotropic, or Δ2 opens on the A-axis). Raw `ceiling_B` would
then give false reassurance the guardrail holds. So F3 fires on THIS oracle; raw `ceiling_B`
(`validity_probe.run_validity_probe`) is logged alongside for F3-diagnosis (env-saturation vs
substrate-pathology) and as a leak-check (substrate-high + raw-low ⟹ leak).

Pinned surface (see plan R5-PIN; design sign-off recorded):
  - FRESH per band: a separate `HierarchicalPoolingModel` at the cell's (r_fine, sigma, seed).
    The ladder is built probe-only (before any deployed encoder exists) and `oracle_B_rec` is a
    per-cell constant — so it inherits the deployed REGIME, never a deployed transient state.
  - READ-ONLY: a separate instance; never backprops into the deployed vision/word encoders.
  - SIGReg-active at DEPLOYED PARITY: `spread.spread_loss(emit, pin.P, gen)` scaled by
    `pin.alpha_spread`, on `emit` (downstream of Δ2 — the deciding pipeline point). SIGReg acting
    on Δ2's output under B-supervision is what makes a spread-collapse NOT undoable by the oracle's
    own supervision. Weaker → under-inherits, drifts to raw; stronger → false F3s. Parity asserted.
  - capacity FORCED OPEN: Δ2 unfrozen, NO pooling penalty (lam1=lam2=0).
  - B-supervision: CE on the member-marginal logits (logsumexp over GROUPS) — the dual of
    `validity_probe._train_coarse_encoder`'s CE on coarse (group) logits for A; trained jointly
    with A so the group/member structure forms. Recovery read by NEAREST-CENTROID (no free head).
  - content-ablation guarded (exp03 carrier-zero idiom): ablate the B input axis → recovery MUST
    collapse to ~chance, else it reads the supervision not the content (invalidate the cell).

`--selftest` is the HARD GATE (must pass before Step 0). SUPERSEDED-GATE RECORD (kept in the canon,
not painted over — exp03 vacuous-F4 discipline):

  * ORIGINAL pre-registration (FALSIFIED by data, 2026-06-25): a deployed-strength oracle-LOW while
    raw-HIGH divergence is producible by moving the band. Result on HEAD 2b70d74: NOT producible —
    the B-supervised capacity-open oracle OVER-performs raw (recovers B where raw nearest-centroid
    can't), and deployed SIGReg(0.1) has ~no effect. The hypothesised substrate-pathology direction
    does not occur at deployed strength. (Full table in the gate record.)
  * RE-PRE-REGISTERED criterion (user-adjudicated 2026-06-26): non-degeneracy = the oracle DIVERGES
    from raw by >= DIVERGENCE_MARGIN at some band AND is CONTENT-DRIVEN (ablation collapses at every
    band) AND reads HIGH at B00 at deployed strength AND alpha/P parity. The empirical divergence is
    oracle-HIGH/raw-LOW (the substrate is a stronger, content-driven probe than naive raw NC) — this
    PASSES and proves the oracle measures the substrate, not a re-expression of the raw input.

Sufficiency argument (why a B-supervised oracle is the correct G1 instrument — recorded so it is not
re-opened): the oracle tests REPRESENTABILITY. B representable ⟹ a no-word-arm failure is "not
acquired" = the gap-3 / clean-G reading; B non-representable ⟹ F3. There is no third case: a
deployed unsupervised dynamics-collapse (e.g. Δ2-on-A) is an ACQUISITION failure, which the no-word
arm measures directly — it is not the oracle's job. F3 fires on this oracle; raw ceiling_B is logged
for F3-DIAGNOSIS ONLY (env-saturation vs substrate-pathology when the substrate oracle breaches).
The raw-low/substrate-high "leak" rule is STRUCK — that is the normal stronger-probe case here; the
content-ablation guard is the sole leak test.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from loom import spread                                   # noqa: E402

import constants                                          # noqa: E402
from encoders import VisionCortex                         # noqa: E402
from stream import Stimulus                               # noqa: E402
from validity_probe import run_validity_probe             # noqa: E402

ABLATION_MARGIN = 0.10          # ablated recovery must be <= chance + this (collapse)
HIGH_BAR = 0.70                 # "recovers B" bar for the selftest
RAW_HIGH = 0.80                 # "raw still separable" bar (original pathology-direction probe)
DIVERGENCE_MARGIN = 0.25        # |oracle - raw| must exceed this at some band (non-degeneracy)


def _member_marginal_logits(pool, X: torch.Tensor) -> torch.Tensor:
    """B-logits = logsumexp over GROUPS of the fine logits (dual of coarse = logsumexp over
    members). Returns (N, M=n_B)."""
    _, fine = pool(X)                        # (N, U)
    fl = fine.view(X.shape[0], pool.G, pool.M)
    return torch.logsumexp(fl, dim=1)        # (N, M)


def train_substrate_oracle(cfg, pin, *, alpha_spread, steps=600, lr=0.05, seed_offset=7000):
    """Fresh, capacity-open, A+B-supervised encoder with SIGReg at the given strength. READ-ONLY
    w.r.t. the deployed encoders (a separate instance). Returns (enc, stim, gen, alpha, P)."""
    g = torch.Generator().manual_seed(cfg.seed + seed_offset)
    stim = Stimulus(cfg.D, cfg.n_A, cfg.n_B, R_coarse=cfg.R_coarse, r_fine=cfg.r_fine,
                    sigma=cfg.sigma_stim, seed=cfg.seed)
    init_center = stim.centre.reshape(-1, cfg.D).mean(0)
    enc = VisionCortex(cfg.D, cfg.n_A, cfg.n_B, init_center=init_center,
                       seed=cfg.seed + seed_offset)
    # capacity forced open: optimise the pool with NO pooling penalty (lam1=lam2=0).
    opt = torch.optim.Adam(enc.pool.parameters(), lr=lr)
    for _ in range(steps):
        a = torch.randint(0, cfg.n_A, (256,), generator=g)
        b = torch.randint(0, cfg.n_B, (256,), generator=g)
        raw = stim.raw(a, b, g)
        coarse, _ = enc.pool(raw)
        b_logits = _member_marginal_logits(enc.pool, raw)
        e = enc.emit(raw)                                  # p @ W (downstream of Δ2)
        loss = (F.cross_entropy(coarse, a) + F.cross_entropy(b_logits, b)
                + alpha_spread * spread.spread_loss(e, pin.P, g))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    return enc, stim, g, alpha_spread, pin.P


@torch.no_grad()
def _b_recovery(enc, cfg, g, *, ablate_B: bool) -> float:
    """Nearest-centroid B-recovery on the oracle's emissions (no free head). With ablate_B the
    B-axis offset is zeroed (r_fine=0) so b carries no signal → recovery must be ~chance."""
    stim = Stimulus(cfg.D, cfg.n_A, cfg.n_B, R_coarse=cfg.R_coarse,
                    r_fine=(0.0 if ablate_B else cfg.r_fine), sigma=cfg.sigma_stim, seed=cfg.seed)

    def emit(K):
        a = torch.randint(0, cfg.n_A, (K,), generator=g)
        b = torch.randint(0, cfg.n_B, (K,), generator=g)
        return enc.emit(stim.raw(a, b, g)), b

    es, bs = emit(max(512, cfg.n_A * cfg.n_B * 16))
    cen = torch.stack([es[bs == c].mean(0) for c in range(cfg.n_B)])
    ee, be = emit(512)
    return (torch.cdist(ee, cen).argmin(1) == be).float().mean().item()


def oracle_b_rec(cfg, pin, *, alpha_spread=None, steps=600) -> dict:
    """Substrate-oracle B-recovery + its content-ablation guard at the given (default = deployed)
    SIGReg strength. Returns the per-cell oracle reading.

    alpha_spread defaults to the DEPLOYED value (pin.alpha_spread) — parity, read not re-specified.
    """
    a_s = pin.alpha_spread if alpha_spread is None else alpha_spread
    enc, _stim, g, alpha, P = train_substrate_oracle(cfg, pin, alpha_spread=a_s, steps=steps)
    rec = _b_recovery(enc, cfg, g, ablate_B=False)
    abl = _b_recovery(enc, cfg, g, ablate_B=True)
    chance = 1.0 / cfg.n_B
    return dict(oracle_B_rec=rec, ablation_rec=abl,
                ablation_collapsed=bool(abl <= chance + ABLATION_MARGIN),
                alpha_spread=alpha, P=P, chance=chance,
                r_fine=cfg.r_fine, sigma_stim=cfg.sigma_stim)


def _commit_hash() -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=str(Path(__file__).resolve().parent), text=True).strip()
    except Exception:
        return "unknown"


def divergence_selftest(steps=600, verbose=True, record_path="oracle_gate_record.json") -> dict:
    """HARD GATE (R5-PIN), re-pre-registered 2026-06-26 — see module docstring for the superseded
    original. Records BOTH criteria to the canon (`oracle_gate_record.json`):

      RE-PRE-REGISTERED (verdict): non-degeneracy = (a) oracle diverges from raw by
        >= DIVERGENCE_MARGIN at some band AND (b) content-driven (ablation collapses at EVERY band)
        AND (c) oracle HIGH at B00 at deployed strength AND (d) alpha/P parity.
      ORIGINAL (falsified, logged): oracle-LOW while raw-HIGH at deployed strength (band-moved).
    """
    pin = constants.PinnedConstants()
    base = constants.Stage0Config()
    chance = 1.0 / base.n_B
    out = {"commit_hash": _commit_hash(), "deployed_alpha_spread": pin.alpha_spread,
           "P": pin.P, "chance": chance, "divergence_margin": DIVERGENCE_MARGIN}

    # --- B00 (the current easy config) at deployed strength -------------------------------------
    raw_b00 = run_validity_probe(base, pin)["ceiling_B"]
    o_b00 = oracle_b_rec(base, pin, steps=steps)            # deployed alpha_spread (parity)
    parity_ok = (abs(o_b00["alpha_spread"] - pin.alpha_spread) < 1e-12 and o_b00["P"] == pin.P)
    out["B00"] = dict(ceiling_B_raw=raw_b00, **o_b00)
    out["parity_ok"] = bool(parity_ok)
    b00_ok = (o_b00["oracle_B_rec"] >= HIGH_BAR and o_b00["ablation_collapsed"])

    # --- band sweep at DEPLOYED strength --------------------------------------------------------
    grid, divergence_at, original_pathology_at = [], None, None
    for r_fine in (2.5, 1.5, 1.0, 0.7, 0.5, 0.35):
        cfg = replace(base, r_fine=r_fine)
        raw = run_validity_probe(cfg, pin)["ceiling_B"]
        on = oracle_b_rec(cfg, pin, steps=steps)            # deployed alpha_spread, band-moved
        off = oracle_b_rec(cfg, pin, alpha_spread=0.0, steps=steps)  # control: regime OFF
        row = dict(r_fine=r_fine, r_over_sigma=r_fine / base.sigma_stim, ceiling_B_raw=raw,
                   oracle_on=on["oracle_B_rec"], oracle_off=off["oracle_B_rec"],
                   ablation_collapsed=on["ablation_collapsed"])
        grid.append(row)
        if verbose:
            print(f"  r_fine={r_fine:>4}  r/σ={row['r_over_sigma']:>5.1f}  raw={raw:.3f}  "
                  f"oracle_on(α={pin.alpha_spread})={on['oracle_B_rec']:.3f}  "
                  f"oracle_off={off['oracle_B_rec']:.3f}  abl_collapse={on['ablation_collapsed']}")
        if divergence_at is None and abs(on["oracle_B_rec"] - raw) >= DIVERGENCE_MARGIN \
                and on["ablation_collapsed"]:
            divergence_at = dict(row, abs_divergence=abs(on["oracle_B_rec"] - raw))
        if original_pathology_at is None and raw >= RAW_HIGH and on["oracle_B_rec"] <= chance + 0.15:
            original_pathology_at = dict(row)
    out["band_sweep"] = grid

    ablation_ok_all = all(r["ablation_collapsed"] for r in grid) and o_b00["ablation_collapsed"]
    out["re_preregistered"] = dict(
        criterion="non-degeneracy: |oracle-raw|>=margin at some band AND ablation collapses at all "
                  "bands AND oracle HIGH at B00 AND alpha/P parity",
        divergence_from_raw=divergence_at, content_driven_all_bands=bool(ablation_ok_all),
        b00_high=bool(b00_ok), parity_ok=bool(parity_ok))
    out["original_criterion"] = dict(
        criterion="oracle-LOW while raw-HIGH at deployed strength (band-moved)",
        status="FALSIFIED" if original_pathology_at is None else "FOUND",
        found_at=original_pathology_at,
        note="substrate oracle OVER-performs raw; deployed SIGReg(0.1) ~no effect")

    out["GATE_PASS"] = bool(parity_ok and b00_ok and ablation_ok_all and divergence_at is not None)
    out["verdict_against"] = "re_preregistered"

    Path(record_path).write_text(json.dumps(out, indent=2))
    if verbose:
        print(f"\n[B00] raw={raw_b00:.3f} oracle={o_b00['oracle_B_rec']:.3f} "
              f"(deployed α={pin.alpha_spread}) ablation_collapsed={o_b00['ablation_collapsed']}")
        print("[parity] alpha/P match deployment:", parity_ok)
        print("[original criterion: oracle-LOW/raw-HIGH] ->", out["original_criterion"]["status"],
              "(falsified by data; logged in canon)")
        if divergence_at:
            print("[re-pre-registered: divergence-from-raw + content-driven] -> PASS "
                  "(divergence {abs_divergence:.3f} at r/σ={r_over_sigma:.1f}; "
                  "oracle={oracle_on:.3f} vs raw={ceiling_B_raw:.3f})".format(**divergence_at))
        print("[content-driven at all bands]:", ablation_ok_all)
        print("GATE_PASS =", out["GATE_PASS"], f"(record -> {record_path})")
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--steps", type=int, default=600)
    args = ap.parse_args()
    if args.selftest:
        res = divergence_selftest(steps=args.steps)
        sys.exit(0 if res["GATE_PASS"] else 1)
    else:
        print("oracle_probe: use --selftest to run the divergence hard-gate.")
