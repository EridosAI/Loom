"""EXP09 pre-run read: decomposition panels from the replayed baselines.

Renders the common/differential trajectories ("the common part becomes a number") for
both measured collapse baselines, plus the pairwise-emission column the SS6.1 floor is
derived from. Diagnostic figures — one y-axis per panel, log scale where the data spans
orders, measured clock lines annotated. Also prints the healthy-span pairwise stats
(the SS6.1 floor candidate) for the read.
"""

from __future__ import annotations

import json
import statistics
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_HERE = Path(__file__).resolve().parent
OUTDIR = _HERE / "exp08"

BLUE, GREEN, AMBER, RED = "#2a78d6", "#1baf7a", "#eda100", "#e34948"

CLOCKS = {
    "word_terminal": dict(seed=1, marks=[(25200, "first k=1"), (42600, "sustained k=1"),
                                         (80000, "den sub-floor")], healthy=(20100, 42300)),
    "marathon_ext": dict(seed=0, marks=[(162000, "k=1 sustained"), (230000, "floor episodes"),
                                        (470000, "revival")], healthy=(20100, 160000)),
}


def render(arm: str) -> dict:
    meta = CLOCKS[arm]
    rec = json.loads((OUTDIR / f"{arm}_s{meta['seed']}_decomp.json").read_text())
    cols = rec["columns"]
    ts = [c["t"] for c in cols]

    fig, axes = plt.subplots(3, 1, figsize=(12, 9.5), sharex=True)
    eps = 1e-30

    ax = axes[0]
    ax.plot(ts, [max(c["evo_common"], eps) for c in cols], color=BLUE, lw=1.2, label="evo_common")
    ax.plot(ts, [max(c["evo_diff"], eps) for c in cols], color=GREEN, lw=1.2, label="evo_diff")
    ax.set_yscale("log")
    ax.set_ylabel("evocation energy")
    ax.legend(loc="upper right", frameon=False, fontsize=9)

    ax = axes[1]
    ax.plot(ts, [max(c["grad_common"], eps) for c in cols], color=BLUE, lw=1.2, label="grad_common")
    ax.plot(ts, [max(c["grad_diff"], eps) for c in cols], color=GREEN, lw=1.2, label="grad_diff")
    ax.set_yscale("log")
    ax.set_ylabel("teaching-gradient energy")
    ax.legend(loc="upper right", frameon=False, fontsize=9)

    ax = axes[2]
    ratio = [(c["grad_common"] / c["grad_diff"]) if c["grad_diff"] > eps else None for c in cols]
    ax.plot([t for t, r in zip(ts, ratio) if r is not None],
            [r for r in ratio if r is not None], color=AMBER, lw=1.2,
            label="contraction/teaching ratio (grad_common/grad_diff)")
    ax.plot(ts, [c["pairwise_emit"] for c in cols], color=RED, lw=1.0, alpha=0.8,
            label="pairwise_emit (SS6.1 floor source)")
    ax.set_yscale("log")
    ax.set_ylabel("ratio / pairwise")
    ax.set_xlabel("wave t")
    ax.legend(loc="upper right", frameon=False, fontsize=9)

    for ax in axes:
        for x, lbl in meta["marks"]:
            ax.axvline(x, color="#999999", lw=0.7, ls="--")
        for s in ax.spines.values():
            s.set_color("#dddddd")
        ax.grid(True, color="#eeeeee", lw=0.5)
    for x, lbl in meta["marks"]:
        axes[0].annotate(lbl, (x, axes[0].get_ylim()[1]), fontsize=7.5, color="#666666",
                         rotation=90, va="top", ha="right")

    fig.suptitle(f"{arm} s{meta['seed']} — the common/differential decomposition back-filled "
                 f"onto the measured collapse baseline (read-only replay)", fontsize=11)
    fig.tight_layout()
    out = OUTDIR / f"{arm}_decomp_panels.png"
    fig.savefig(out, dpi=110)
    plt.close(fig)

    h0, h1 = meta["healthy"]
    hp = [c["pairwise_emit"] for c in cols if h0 <= c["t"] <= h1]
    stats = dict(arm=arm, healthy_span=[h0, h1],
                 pairwise_healthy_min=round(min(hp), 6),
                 pairwise_healthy_mean=round(statistics.mean(hp), 6),
                 pairwise_terminal_last=round(cols[-1]["pairwise_emit"], 8),
                 png=str(out.name))
    print(json.dumps(stats))
    return stats


if __name__ == "__main__":
    out = [render(a) for a in CLOCKS]
    (OUTDIR / "exp09_pairwise_floor_read.json").write_text(json.dumps(out, indent=2))
