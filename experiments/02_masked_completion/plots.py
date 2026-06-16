"""Plots for the masked-completion rig. Figures are regenerable (gitignored)."""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_summary(res, sweep, fam, path):
    nc, ca = res["noncausal"], res["causal"]
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    # Left: the discriminator (begin recon from end) + the forward control.
    ax = axes[0]
    labels = ["prefix-cued\n(end recon)", "suffix-cued\n(BEGIN recon)"]
    nc_v = [nc["prefix_end"], nc["suffix_begin"]]
    ca_v = [ca["prefix_end"], ca["suffix_begin"]]
    x = range(len(labels))
    ax.bar([i - 0.2 for i in x], nc_v, width=0.4, label="non-causal", color="C0")
    ax.bar([i + 0.2 for i in x], ca_v, width=0.4, label="causal", color="C3")
    ax.axhline(1.0 / fam.n_begins, color="k", ls=":", lw=1, label="chance")
    ax.set_xticks(list(x)); ax.set_xticklabels(labels)
    ax.set_ylim(0, 1.05); ax.set_ylabel("reconstruction accuracy")
    ax.set_title("forward control vs end->beginning discriminator"); ax.legend()

    # Right: random access -- single cued position -> whole-sequence recon.
    ax = axes[1]
    xs = list(range(fam.L))
    ax.plot(xs, sweep["noncausal"], "o-", label="non-causal", color="C0")
    ax.plot(xs, sweep["causal"], "s-", label="causal", color="C3")
    ax.set_xticks(xs)
    ax.set_xlabel("single cued position"); ax.set_ylabel("whole-sequence recon")
    ax.set_ylim(0, 1.05)
    ax.axvline(fam.begin_pos, color="C2", ls="--", lw=1, alpha=0.5)
    ax.axvline(fam.end_pos, color="C2", ls="--", lw=1, alpha=0.5)
    ax.set_title("random access: cue one position, recover the whole"); ax.legend()

    fig.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=110)
    plt.close(fig)
