"""run_sweep.py — the characterisation-sweep orchestrator (the only trainer).

Per (band cell × unpool-rate × seed): construct matched intact + no-word `Stage0Loop`s in Phase-1
order, run fixed-long, and emit one JSONL trajectory row per eval window (+ a `.meta.json`). The
loop dynamics are EXACTLY Phase-1 (`Stage0Loop.step`); the per-window read is a lighter READ-ONLY
diagnostic (grad_attribution + b_a_track×2 + entanglement_r2 for the max_coord_r2 invariant +
pooling_depth) — Readout-D's `position_begin_id` is skipped (out of scope here, G3; it uses its own
RNG so omitting it does not change the training trajectory). One code path is preserved: the eval is
read-only, the loop never branches train/run.

`oracle_B_rec` / `ceiling_B_raw` / ablation are per-cell constants from `band_ladder.json` (the
substrate oracle is the F3 line). `capacity_fraction` is POST-HOC (analyze_sweep, from the depth
series). `--smoke` runs a tiny pipeline check; `--cell-index k` runs one band's rate×seed (parallel).
"""

from __future__ import annotations

import argparse
import itertools
import json
import sys
from dataclasses import replace
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import constants                                          # noqa: E402
import sweep_config as sc                                 # noqa: E402
from loop import Stage0Loop                               # noqa: E402

HERE = Path(__file__).resolve().parent


def run_one(cell, cell_idx, rate, seed, *, calib, pin, base, verbose=False):
    cfg = sc.rate_cfg(sc.band_cfg(base, cell), rate)
    cfg = replace(cfg, seed=seed)
    intact = Stage0Loop(cfg, pin)            # Phase-1 construction order: intact then no-word
    noword = Stage0Loop(cfg, pin)

    oracle_B_rec = cell["oracle_substrate"]          # per-cell static (the F3 line)
    ceiling_B_raw = cell["ceiling_B_raw"]            # F3-diagnosis only
    ablation_ok = cell["ablation_ok"]
    ib = calib["intact_bar"]; nlo, nhi = calib["noword_floor_band"]; othr = calib["oracle_threshold"]
    commit, sh = sc.commit_hash(), sc.spec_hash()
    ent_n = sc.SPEC["ent_n"]

    rows = []
    for i in range(cfg.steps):
        r = intact.step()                    # no_word=False
        noword.step(no_word=True)
        if i % cfg.eval_every == 0 or i == cfg.steps - 1:
            ga = intact.grad_attribution()                 # advances intact.gen (deterministic)
            gp, gj = ga["vision_grad_from_PAM"], ga["vision_grad_from_JEPA"]
            ent = intact.entanglement_r2(n=ent_n)
            depth = intact.vision.pooling_depth
            intact_B = intact.b_a_track(cfg.n_eval)["B_track"]
            noword_B = noword.b_a_track(cfg.n_eval)["B_track"]
            wpd = intact.word.param_delta()
            share = (gp / (gp + gj)) if (gp + gj) > 0 else None
            ratio = (gp / gj) if gj > 0 else None
            gap3_alive = bool(gp > 0 and gj > 0)
            biok = bool(wpd == 0.0 and gap3_alive and ent["max_coord_r2"] < pin.tau_entangle)
            cleanG = bool(intact_B >= ib and nlo <= noword_B <= nhi and oracle_B_rec >= othr)
            rows.append(dict(
                commit_hash=commit, spec_hash=sh, band_index=cell_idx,
                r_over_sigma=cell["r_over_sigma"], r_fine=cell["r_fine"], sigma_stim=cell["sigma_stim"],
                unpool_rate=rate, seed=seed, wave=i,
                pooling_depth=depth,
                vision_grad_from_PAM=gp, vision_grad_from_JEPA=gj,
                pam_jepa_grad_ratio=ratio, pam_grad_share=share,
                intact_B_res=intact_B, noword_B_acq=noword_B,
                oracle_B_rec=oracle_B_rec, ceiling_B_raw=ceiling_B_raw, oracle_ablation_ok=ablation_ok,
                cleanG_flag=cleanG, word_param_delta=wpd,
                max_coord_r2=ent["max_coord_r2"], full_ols_r2=ent["full_ols_r2"],
                gap3_alive=gap3_alive, build_invariants_ok=biok,
                lam2=r["lam2"], gain=r["gain"]))
            if verbose and (i % (cfg.eval_every * 8) == 0 or i == cfg.steps - 1):
                print(f"    [{rate} b{cell_idx} s{seed}] w={i:>6} depth={depth:.3f} "
                      f"B={intact_B:.2f} noW={noword_B:.2f} share={share if share is None else round(share,2)} "
                      f"cleanG={cleanG} biok={biok}")
    return cfg, rows


def write_run(out_dir, cell, cell_idx, rate, seed, cfg, pin, calib, rows):
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f"band{cell_idx:02d}_{rate}_seed{seed:02d}"
    (out_dir / f"{stem}.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
    (out_dir / f"{stem}.meta.json").write_text(json.dumps(dict(
        cell=cell, band_index=cell_idx, rate=rate, seed=seed,
        cfg=cfg.logged(), pin=pin.logged(),
        bars=dict(intact_bar=calib["intact_bar"], noword_floor_band=calib["noword_floor_band"],
                  oracle_threshold=calib["oracle_threshold"]),
        commit_hash=sc.commit_hash(), spec_hash=sc.spec_hash(),
        n_rows=len(rows), pooled_baseline=(rows[0]["pooling_depth"] if rows else None)), indent=2))
    valid = sum(1 for r in rows if r["build_invariants_ok"])
    return dict(stem=stem, n_rows=len(rows), n_valid=valid,
                final_depth=(rows[-1]["pooling_depth"] if rows else None),
                any_cleanG=any(r["cleanG_flag"] for r in rows),
                gap3_all=all(r["gap3_alive"] for r in rows))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--cell-index", type=int, default=None, help="run only this band index (parallel)")
    ap.add_argument("--rate", default=None, help="run only this rate (MODERATE/SLOW) for parallelism")
    ap.add_argument("--seeds", type=int, default=None, help="override seed count")
    ap.add_argument("--threads", type=int, default=None, help="torch threads (set 1 for many procs)")
    ap.add_argument("--out-dir", default=None)
    ap.add_argument("--calib", default="calibration.json")
    ap.add_argument("--ladder", default="band_ladder.json")
    args = ap.parse_args()
    if args.threads:
        torch.set_num_threads(args.threads)

    calib = json.loads((HERE / args.calib).read_text())
    ladder = json.loads((HERE / args.ladder).read_text())
    if not (calib["commit_hash"] == ladder["commit_hash"] == sc.commit_hash()):
        raise SystemExit("commit mismatch between calibration/ladder/HEAD — re-run Step 0 + ladder")
    pin = constants.PinnedConstants()
    cells = ladder["admissible_cells"]
    rates = [args.rate] if args.rate else list(sc.SPEC["rates"].keys())

    if args.smoke:
        out_dir = Path(args.out_dir or (HERE / "runs_smoke"))
        cells_sel = [(0, cells[0]), (min(len(cells) - 1, 8), cells[min(len(cells) - 1, 8)])]
        seeds = [0, 1]
        base = sc.base_cfg(steps=6000, T=8000, eval_every=100)
        print(f"SMOKE: {len(cells_sel)} bands × {len(rates)} rates × {len(seeds)} seeds -> {out_dir}")
    else:
        out_dir = Path(args.out_dir or (HERE / "runs"))
        idxs = [args.cell_index] if args.cell_index is not None else list(range(len(cells)))
        cells_sel = [(k, cells[k]) for k in idxs]
        seeds = list(range(args.seeds or sc.SPEC["n_seeds"]))
        base = sc.base_cfg()
        print(f"FULL: {len(cells_sel)} bands × {len(rates)} rates × {len(seeds)} seeds -> {out_dir}")

    summaries = []
    for (cell_idx, cell), rate, seed in itertools.product(cells_sel, rates, seeds):
        cfg, rows = run_one(cell, cell_idx, rate, seed, calib=calib, pin=pin, base=base,
                            verbose=args.smoke)
        s = write_run(out_dir, cell, cell_idx, rate, seed, cfg, pin, calib, rows)
        summaries.append(s)
        print(f"  {s['stem']}: rows={s['n_rows']} valid={s['n_valid']} "
              f"final_depth={s['final_depth']:.3f} gap3_all={s['gap3_all']} anyCleanG={s['any_cleanG']}")
    print(f"\nwrote {len(summaries)} runs to {out_dir}")


if __name__ == "__main__":
    main()
