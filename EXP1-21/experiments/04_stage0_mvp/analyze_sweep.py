"""analyze_sweep.py — read the JSONL trajectories, compute the response surface, classify.

Per (band cell × rate): post-hoc capacity_fraction (self-normalized), T95/T_run, per-seed S-curve
share stats + clean-G/autonomous sustainedness, then per-cell frequencies over the seed
distribution. Verdict = the surface + which of {paradigm-positive, F1, F2, F3, F4} (computed, not a
PASS). Writes `sweep_cells.csv`, `SWEEP_RESULTS.md`, and (if matplotlib) `figures/response_surface.png`.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import sweep_config as sc
import sweep_metrics as sm

HERE = Path(__file__).resolve().parent
SPEC = sc.SPEC


def load_runs(runs_dir):
    groups = defaultdict(list)   # (band_index, rate, seed) -> rows
    for fp in sorted(Path(runs_dir).glob("*.jsonl")):
        rows = [json.loads(ln) for ln in fp.read_text().splitlines() if ln.strip()]
        if not rows:
            continue
        k = (rows[0]["band_index"], rows[0]["unpool_rate"], rows[0]["seed"])
        groups[k] = rows
    return groups


def analyze_seed(rows, calib, *, toe=None, rapid=None):
    rows = sorted(rows, key=lambda r: r["wave"])
    waves = [r["wave"] for r in rows]
    depths = [r["pooling_depth"] for r in rows]
    cap, full_depth, _ = sm.capacity_fraction_series(depths, plateau_frac=SPEC["plateau_frac"])
    t95, t_run = sm.t95_trun(waves, cap, level=SPEC["t95_level"], factor=SPEC["t_run_factor"])
    shares = [r["pam_grad_share"] if r["build_invariants_ok"] else None for r in rows]
    ss = sm.per_seed_share_stats(waves, shares, cap, t_run, SPEC, toe=toe, rapid=rapid)
    cg = [bool(r["cleanG_flag"] and r["build_invariants_ok"]) for r in rows]
    cg_sus, _, _ = sm.sustained(cg, waves, t_run, n_consec=SPEC["n_consec"], x_pct=SPEC["x_pct"])
    au = [bool(r["noword_B_acq"] >= calib["intact_bar"] and r["build_invariants_ok"]) for r in rows]
    au_sus, _, _ = sm.sustained(au, waves, t_run, n_consec=SPEC["n_consec"], x_pct=SPEC["x_pct"])
    inrun = [r for r in rows if r["wave"] <= t_run]
    invalid_frac = sum(1 for r in inrun if not r["build_invariants_ok"]) / max(1, len(inrun))
    return dict(t95=t95, t_run=t_run, full_depth=full_depth,
                oracle_B_rec=rows[0]["oracle_B_rec"], r_over_sigma=rows[0]["r_over_sigma"],
                cleanG_sustained=cg_sus, autonomous_sustained=au_sus, invalid_frac=invalid_frac, **ss)


def signature_freq(seed_rows_by_seed, calib, *, toe, rapid):
    sigs = [analyze_seed(rows, calib, toe=toe, rapid=rapid)["s_curve_signature"]
            for rows in seed_rows_by_seed]
    return sm.frac_true(sigs)


def analyze_cell(seed_rows_by_seed, calib):
    ms = [analyze_seed(rows, calib) for rows in seed_rows_by_seed]
    base_sig = sm.frac_true([m["s_curve_signature"] for m in ms])
    # robustness: re-classify the S-curve signature under ±1-bin cutoff perturbation
    perturbed = [signature_freq(seed_rows_by_seed, calib, toe=t, rapid=r) for t, r in
                 [([0.0, 0.20], [0.20, 0.70]), ([0.0, 0.30], [0.30, 0.80])]]
    sig_robust = all(abs(p - base_sig) <= 0.25 for p in perturbed)
    return dict(
        r_over_sigma=ms[0]["r_over_sigma"], oracle_B_rec=ms[0]["oracle_B_rec"],
        n_seeds=len(ms),
        s_curve_signature_frequency=base_sig, s_curve_signature_freq_perturbed=perturbed,
        s_curve_robust=sig_robust,
        delta_rapid_dist=sm.agg([m["delta_rapid"] for m in ms]),
        delta_plateau_dist=sm.agg([m["delta_plateau"] for m in ms]),
        cleanG_frequency=sm.frac_true([m["cleanG_sustained"] for m in ms]),
        autonomous_resolution_frequency=sm.frac_true([m["autonomous_sustained"] for m in ms]),
        oracle_floor_breach=any(m["oracle_B_rec"] < calib["oracle_threshold"] for m in ms),
        mean_invalid_frac=sm.agg([m["invalid_frac"] for m in ms]),
        t95=sm.agg([m["t95"] for m in ms]), t_run=sm.agg([m["t_run"] for m in ms]),
        full_depth=sm.agg([m["full_depth"] for m in ms]),
        toe_share=sm.agg([m["toe_share"] for m in ms]),
        rapid_peak_share=sm.agg([m["rapid_peak_share"] for m in ms]),
        plateau_share=sm.agg([m["plateau_share"] for m in ms]))


def classify_surface(table):
    """table: list of dicts with keys (band_index, rate, metrics...). Returns the verdict + per-cell
    F-tags. Thresholds are the FROZEN, pre-registered SPEC values (hashed into spec_hash) — NOT tuned
    after the surface exists. F2/F4 are relational across the band axis (per rate)."""
    sig_bar = SPEC["verdict_sig_bar"]; clean_bar = SPEC["verdict_clean_bar"]
    auto_high = SPEC["verdict_auto_high"]; f1_cutoff = SPEC["verdict_f1_cutoff"]
    by_rate = defaultdict(list)
    for row in table:
        by_rate[row["rate"]].append(row)
    verdict = {"paradigm_positive_cells": [], "per_rate": {},
               "thresholds": dict(sig_bar=sig_bar, clean_bar=clean_bar, auto_high=auto_high,
                                  f1_cutoff=f1_cutoff)}
    for rate, cells in by_rate.items():
        cells = sorted(cells, key=lambda c: c["band_index"])          # top(easy)→bottom(hard)
        autos = [c["autonomous_resolution_frequency"] for c in cells]
        easy_auto = autos[0] if autos else 0.0
        tags = {}
        for c in cells:
            t = []
            if c["oracle_floor_breach"]:
                t.append("F3")
            if c["s_curve_signature_frequency"] <= f1_cutoff:
                t.append("F1")
            tags[c["band_index"]] = t
        # F2: autonomous high at ALL bands (premise dead)
        f2 = all(a >= auto_high for a in autos) if autos else False
        # F4: cleanG material only at easy bands, ~0 in interior
        clean = [c["cleanG_frequency"] for c in cells]
        f4 = (clean and clean[0] >= clean_bar
              and all(x < clean_bar for x in clean[1:]))
        for c in cells:
            interior = 0 < c["band_index"] < (cells[-1]["band_index"])
            pos = (interior and not c["oracle_floor_breach"]
                   and c["s_curve_signature_frequency"] >= sig_bar
                   and c["cleanG_frequency"] >= clean_bar
                   and c["autonomous_resolution_frequency"] < easy_auto)
            if pos:
                verdict["paradigm_positive_cells"].append((rate, c["band_index"]))
        verdict["per_rate"][rate] = dict(F2_autonomous_everywhere=bool(f2),
                                         F4_cleanG_only_easy=bool(f4), per_cell_tags=tags)
    verdict["overall"] = ("paradigm-positive" if verdict["paradigm_positive_cells"]
                          else "no-paradigm-positive-cell (see F-tags / surface)")
    return verdict


def write_csv(table, path):
    cols = ["band_index", "rate", "r_over_sigma", "oracle_B_rec", "n_seeds",
            "s_curve_signature_frequency", "s_curve_robust", "cleanG_frequency",
            "autonomous_resolution_frequency", "oracle_floor_breach", "mean_invalid_frac"]
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols + ["delta_rapid_mean", "delta_plateau_mean", "t_run_mean", "full_depth_mean"])
        for c in sorted(table, key=lambda r: (r["band_index"], r["rate"])):
            w.writerow([c["band_index"], c["rate"], round(c["r_over_sigma"], 3),
                        round(c["oracle_B_rec"], 3), c["n_seeds"],
                        round(c["s_curve_signature_frequency"], 3), c["s_curve_robust"],
                        round(c["cleanG_frequency"], 3), round(c["autonomous_resolution_frequency"], 3),
                        c["oracle_floor_breach"], round(c["mean_invalid_frac"]["mean"] or 0, 3),
                        c["delta_rapid_dist"]["mean"], c["delta_plateau_dist"]["mean"],
                        c["t_run_mean"]["mean"] if "t_run_mean" in c else c["t_run"]["mean"],
                        c["full_depth"]["mean"]])


def write_md(table, verdict, calib, runs_dir, path):
    L = []
    P = L.append
    P("# Characterisation Sweep — response surface\n")
    P(f"commit `{sc.commit_hash()}`  spec_hash `{sc.spec_hash()}`  runs `{runs_dir}`\n")
    P(f"**Overall:** {verdict['overall']}\n")
    P(f"bars (Step 0): intact_bar={calib['intact_bar']:.3f}  "
      f"noword_floor_band={calib['noword_floor_band']}  oracle_threshold={calib['oracle_threshold']:.3f}\n")
    P("| band | rate | r/σ | oracle | s_curve_freq | robust | cleanG_freq | autonomous_freq | F3 | invalid |")
    P("|---|---|---|---|---|---|---|---|---|---|")
    for c in sorted(table, key=lambda r: (r["band_index"], r["rate"])):
        P(f"| {c['band_index']} | {c['rate']} | {c['r_over_sigma']:.2f} | {c['oracle_B_rec']:.2f} | "
          f"{c['s_curve_signature_frequency']:.2f} | {c['s_curve_robust']} | "
          f"{c['cleanG_frequency']:.2f} | {c['autonomous_resolution_frequency']:.2f} | "
          f"{c['oracle_floor_breach']} | {(c['mean_invalid_frac']['mean'] or 0):.2f} |")
    P("\n## Per-rate F-pattern (F2/F4 relational across the band axis)\n")
    for rate, d in verdict["per_rate"].items():
        P(f"- **{rate}**: F2_autonomous_everywhere={d['F2_autonomous_everywhere']}  "
          f"F4_cleanG_only_easy={d['F4_cleanG_only_easy']}")
    if verdict["paradigm_positive_cells"]:
        P(f"\n**paradigm-positive cells:** {verdict['paradigm_positive_cells']}")
    Path(path).write_text("\n".join(L) + "\n")


def write_figure(table, path):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"  (matplotlib unavailable: {e}; skipping figure)")
        return False
    rates = sorted({c["rate"] for c in table})
    metrics = [("s_curve_signature_frequency", "S-curve sig freq"),
               ("cleanG_frequency", "clean-G freq"),
               ("autonomous_resolution_frequency", "autonomous freq")]
    fig, axes = plt.subplots(1, len(metrics), figsize=(5 * len(metrics), 4))
    if len(metrics) == 1:
        axes = [axes]
    for ax, (key, title) in zip(axes, metrics):
        for rate in rates:
            cs = sorted([c for c in table if c["rate"] == rate], key=lambda c: c["r_over_sigma"])
            ax.plot([c["r_over_sigma"] for c in cs], [c[key] for c in cs], "o-", label=rate)
        ax.set_xlabel("r/σ (band, hard→easy →)"); ax.set_ylabel(title); ax.set_title(title)
        ax.set_ylim(-0.05, 1.05); ax.legend()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout(); fig.savefig(path, dpi=110); plt.close(fig)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", default="runs")
    ap.add_argument("--calib", default="calibration.json")
    ap.add_argument("--out-prefix", default=None)
    args = ap.parse_args()
    runs_dir = HERE / args.runs
    calib = json.loads((HERE / args.calib).read_text())
    groups = load_runs(runs_dir)
    if not groups:
        raise SystemExit(f"no runs in {runs_dir}")

    by_cell = defaultdict(dict)   # (band_index, rate) -> {seed: rows}
    for (bi, rate, seed), rows in groups.items():
        by_cell[(bi, rate)][seed] = rows

    table = []
    for (bi, rate), seedmap in sorted(by_cell.items()):
        cell = analyze_cell(list(seedmap.values()), calib)
        cell.update(band_index=bi, rate=rate,
                    t_run_mean=cell["t_run"], )   # alias for csv
        table.append(cell)
    verdict = classify_surface(table)

    pref = args.out_prefix or ("smoke_" if "smoke" in args.runs else "")
    write_csv(table, HERE / f"{pref}sweep_cells.csv")
    write_md(table, verdict, calib, args.runs, HERE / f"{pref}SWEEP_RESULTS.md")
    fig_ok = write_figure(table, HERE / "figures" / f"{pref}response_surface.png")
    print(f"analyzed {len(table)} (band×rate) cells from {len(groups)} runs")
    print(f"overall: {verdict['overall']}")
    for c in sorted(table, key=lambda r: (r["band_index"], r["rate"])):
        print(f"  b{c['band_index']} {c['rate']:<8} r/σ={c['r_over_sigma']:.2f} "
              f"s_curve={c['s_curve_signature_frequency']:.2f} cleanG={c['cleanG_frequency']:.2f} "
              f"auto={c['autonomous_resolution_frequency']:.2f} F3={c['oracle_floor_breach']}")
    print(f"wrote {pref}sweep_cells.csv, {pref}SWEEP_RESULTS.md" + (", figure" if fig_ok else ""))


if __name__ == "__main__":
    main()
