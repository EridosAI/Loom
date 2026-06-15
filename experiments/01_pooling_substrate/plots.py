"""Plotting for the pooling rig. Figures are regenerable artifacts (gitignored)."""

from __future__ import annotations

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def _vline(ax, x, label):
    if x is not None:
        ax.axvline(x, color="k", ls="--", lw=1, alpha=0.6)
        ax.text(x, ax.get_ylim()[1], label, fontsize=8, va="top", ha="left", rotation=90)


def plot_run(log, path, title, marks=None):
    """marks: dict of {label: step} vertical markers (unpool / re-pool events)."""
    marks = marks or {}
    s = log["step"]
    fig, axes = plt.subplots(2, 2, figsize=(11, 7))
    fig.suptitle(title)

    ax = axes[0, 0]
    ax.plot(s, log["coarse_acc_te"], label="coarse", color="C0")
    ax.plot(s, log["fine_acc_te"], label="fine", color="C1")
    ax.set_ylim(-0.02, 1.02)
    ax.set_title("held-out accuracy")
    ax.set_xlabel("step"); ax.legend(loc="lower right")
    for lbl, x in marks.items():
        _vline(ax, x, lbl)

    ax = axes[0, 1]
    ax.plot(s, log["d1_mean"], label="mean ||Delta1||", color="C2")
    ax.plot(s, log["d2_mean"], label="mean ||Delta2||", color="C3")
    ax.set_title("residual norms (pooling state)")
    ax.set_xlabel("step"); ax.legend()
    for lbl, x in marks.items():
        _vline(ax, x, lbl)

    ax = axes[1, 0]
    ax.plot(s, log["spread"], color="C4")
    ax.set_title("within-group weight spread")
    ax.set_xlabel("step")
    for lbl, x in marks.items():
        _vline(ax, x, lbl)

    ax = axes[1, 1]
    ax.plot(s, log["pull_apart"], label="pull-apart force", color="C5")
    ax.set_xlabel("step"); ax.set_title("re-pool signal")
    ax2 = ax.twinx()
    ax2.plot(s, log["cos_disagreement"], label="cos (disagreement)", color="C6", alpha=0.7)
    ax2.set_ylim(-1.05, 1.05)
    lines = ax.get_lines() + ax2.get_lines()
    ax.legend(lines, [ln.get_label() for ln in lines], loc="upper right", fontsize=8)
    for lbl, x in marks.items():
        _vline(ax, x, lbl)

    fig.tight_layout(rect=(0, 0, 1, 0.96))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=110)
    plt.close(fig)


def plot_overlay(logs, key, path, title, ylabel, marks=None):
    """Overlay one metric across several runs (e.g. Test B baselines)."""
    marks = marks or {}
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for label, log in logs.items():
        ax.plot(log["step"], log[key], label=label)
    ax.set_title(title); ax.set_xlabel("step"); ax.set_ylabel(ylabel)
    ax.legend()
    for lbl, x in marks.items():
        _vline(ax, x, lbl)
    fig.tight_layout()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fig.savefig(path, dpi=110)
    plt.close(fig)
