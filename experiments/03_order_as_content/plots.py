"""Plots for the order-as-content rig. Figures are regenerable (gitignored)."""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def plot_summary(sigma_grid, alpha_grid, band, sigma_star, vtab, prim_sigma, prim_alpha,
                 ctrlB, ctrlA, chance, probe, path):
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # --- Panel 1: F1/F2 -- begin-recon vs sigma ---
    ax = axes[0]
    prim = [prim_sigma[s] for s in sigma_grid]
    cb_ = [ctrlB[s] for s in sigma_grid]
    oracle = [vtab[s]["begin_is_argmin"] for s in sigma_grid]
    ax.plot(sigma_grid, prim, "o-", color="C0", label="Primary (drift, shuffled)")
    ax.plot(sigma_grid, cb_, "s--", color="C3", label="Control B (drift, unshuffled)")
    ax.plot(sigma_grid, oracle, "^:", color="C2", label="oracle (begin=argmin)")
    if band:
        ax.axvspan(min(band), max(band), color="C0", alpha=0.08, label="testable band")
    ax.axhline(chance, color="k", ls=":", lw=1, label=f"chance ({chance:.3f})")
    ax.axvline(sigma_star, color="C4", ls="-.", lw=1, alpha=0.6)
    ax.text(sigma_star, 0.02, " sigma*", color="C4", fontsize=8)
    ax.set_xlabel("sigma (drift noise -> adjacent overlap)")
    ax.set_ylabel("cue-end -> begin recon")
    ax.set_ylim(-0.02, 1.05)
    ax.set_title("F1 / F2: begin-recon vs sigma")
    ax.legend(fontsize=8, loc="center right")

    # --- Panel 2: F4 -- begin-recon vs alpha at sigma* ---
    ax = axes[1]
    pa = [prim_alpha[a] for a in alpha_grid]
    ax.plot(alpha_grid, pa, "o-", color="C0", label=f"Primary @ sigma*={sigma_star}")
    ax.axhline(chance, color="k", ls=":", lw=1, label=f"chance ({chance:.3f})")
    ax.axhline(ctrlA, color="C1", ls="--", lw=1, alpha=0.6, label=f"Control A clean ({ctrlA:.2f})")
    ax.set_xlabel("alpha (0 = dedicated channel  ->  1 = entangled into content)")
    ax.set_ylabel("cue-end -> begin recon")
    ax.set_ylim(-0.02, 1.05)
    ax.set_title("F4: begin-recon vs entanglement alpha")
    ax.annotate(f"alpha=1 probe\nbegin=argmin={probe['probe_begin_is_argmin']:.2f}",
                xy=(1.0, pa[-1]), xytext=(0.45, 0.25), fontsize=8,
                arrowprops=dict(arrowstyle="->", color="gray"))
    ax.legend(fontsize=8, loc="lower left")

    fig.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=110)
    plt.close(fig)
