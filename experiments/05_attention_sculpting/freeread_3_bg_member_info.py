"""FREE-READ (iii) — RUNG-3.5 CHECKABLE: does the background carry member information at all?

Memo: docs/FREE_READS_MEMO.md §(iii).  Recipe: MECHANISM_MAP_v1_2_RECONCILED.md §1 — "does the
current background (OU toward bg_const) carry member information at all? If not — likely — rung 3.5
is latent, and the context rung (L3) is a generalization-pressure arm, not a shortcut-removal arm."

Two committed-provenance measures on the built fabric's background `bg` (T, BG=4) vs member:
  - the committed independence statistic (exp12_fabric.py fabric_asserts (4)): max-abs lag-0
    correlation of bg vs the a/distractor/category label triple, against the exchangeability null
    (dwell->member permutation), reported obs vs null99 — reusing F12._max_abs_corr / _dwell_perm_labels
    / _labels_of verbatim;
  - a direct decodability: nearest-centroid classification of member (16 classes) from bg[t], vs
    chance 1/16 — the "at all" limb the corr can miss.

The background is arm-independent (per-seed OU jitter around a FIXED member-independent bg_const); the
built arm is the base A_dwell. Read-only, deterministic build (torch threads=1). One JSON. The
latent/not judgment routes to the seat.
"""
import json, statistics
from pathlib import Path

import torch
torch.set_num_threads(1)

import exp12_arms as X12
import exp12_fabric as F12                          # committed independence helpers

HERE = Path(__file__).resolve().parent
OUT = HERE / "exp08"
ARM = "exp12_dwell"                                 # bg is arm-independent; A_dwell = the base
SEEDS = list(range(8))
WINDOW = 100_000
S_CORR = 12_000                                     # committed n_sample for assert (4)
N_NULL = 200                                        # committed n_null
CHANCE = 1.0 / 16.0


def per_seed(seed):
    loop, _spec, cfg = X12.build_exp12(ARM, seed, WINDOW)
    fab = loop.stream
    S = min(fab.T, S_CORR)
    labels = F12._labels_of(fab.a[:S], fab.b[:S], cfg.n_category)
    obs = F12._max_abs_corr(fab.bg[:S], labels)
    null = []
    for i in range(N_NULL):                          # committed keys 64000+i (assert (4))
        gp = torch.Generator().manual_seed(64000 + i)
        null.append(F12._max_abs_corr(fab.bg[:S], F12._dwell_perm_labels(fab, gp, cfg.n_category, S)))
    null99 = sorted(null)[int(0.99 * N_NULL)]

    # nearest-centroid member decodability over the full window
    bg = fab.bg
    mem = fab.member.tolist()
    n = bg.shape[0]
    cent = torch.zeros(16, bg.shape[1])
    cnt = torch.zeros(16)
    for t in range(n):
        cent[mem[t]] += bg[t]; cnt[mem[t]] += 1
    cent = cent / cnt.clamp(min=1).unsqueeze(1)
    # classify: argmin over members of ||bg - cent_m|| ; block for memory
    correct = 0
    B = 20000
    for i in range(0, n, B):
        chunk = bg[i:i + B]                            # (b, D)
        d = torch.cdist(chunk, cent)                   # (b, 16)
        pred = d.argmin(dim=1).tolist()
        correct += sum(1 for j, p in enumerate(pred) if p == mem[i + j])
    acc = correct / n

    return dict(seed=seed, n=n, S_corr=S,
                bg_corr_obs=round(obs, 6), bg_corr_null99=round(null99, 6),
                bg_corr_independent=bool(obs <= null99),
                member_decode_acc=round(acc, 6), chance=CHANCE,
                decode_over_chance=round(acc - CHANCE, 6))


def main():
    per = [per_seed(s) for s in SEEDS]
    pooled = dict(
        bg_corr_obs_mean=round(statistics.mean(p["bg_corr_obs"] for p in per), 6),
        bg_corr_null99_mean=round(statistics.mean(p["bg_corr_null99"] for p in per), 6),
        all_independent=all(p["bg_corr_independent"] for p in per),
        member_decode_acc_mean=round(statistics.mean(p["member_decode_acc"] for p in per), 6),
        member_decode_acc_max=round(max(p["member_decode_acc"] for p in per), 6),
        chance=CHANCE)
    out = dict(
        read="(iii) rung-3.5 — background member-information",
        memo_section="docs/FREE_READS_MEMO.md §(iii)",
        recipe="MECHANISM_MAP_v1_2_RECONCILED.md §1",
        method=("bg (T,BG=4) vs member. (a) committed assert-(4) statistic: F12._max_abs_corr(bg[:S], "
                "label-triple) vs exchangeability null99 (F12._dwell_perm_labels, keys 64000+i, "
                "N_NULL=200, S=12000). (b) nearest-centroid member(16)-from-bg accuracy over the full "
                "window vs chance 1/16."),
        inputs=dict(arm=ARM, seeds=SEEDS, window=WINDOW,
                    note="bg is arm-independent (per-seed OU around member-independent bg_const)",
                    code_modules=["exp12_arms.py", "exp12_fabric.py"]),
        consequence=dict(
            memo_condition="background does NOT carry member information -> rung 3.5 latent -> L3 is a "
                           "generalization-pressure arm, not a shortcut-removal arm",
            measured=dict(all_seeds_bg_independent=pooled["all_independent"],
                          member_decode_acc_mean=pooled["member_decode_acc_mean"],
                          member_decode_acc_max=pooled["member_decode_acc_max"], chance=CHANCE),
            triggered="ROUTES (judgment): numbers reported; the seat rules whether decodability at/near "
                      "chance + corr within null == 'no member information' (latent)."),
        pooled=pooled,
        per_seed=per)
    OUT.mkdir(exist_ok=True)
    (OUT / "freeread_3_bg_member_info.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    print("bg-member: corr_obs_mean=%.6f null99_mean=%.6f all_indep=%s  decode_acc_mean=%.6f (chance %.4f)"
          % (pooled["bg_corr_obs_mean"], pooled["bg_corr_null99_mean"], pooled["all_independent"],
             pooled["member_decode_acc_mean"], CHANCE))
    print("-> exp08/freeread_3_bg_member_info.json")


if __name__ == "__main__":
    main()
