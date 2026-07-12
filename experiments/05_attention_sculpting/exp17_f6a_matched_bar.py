"""EXP17 F6-A — matched-bar reproduction (CC-side, independent, 2026-07-12).

FRESH code: a from-scratch reader + run-length detector that imports NOTHING from exp17_score /
exp14_arms / verify_toolkit (and does not port the design seat's script). It reproduces the
matched-bar correction that superseded the G8 DRAFT's unlike-bar Fisher row: at a COMMON detector
the orbit shows no excess over tremble, and A_dwell self-converts at its own detector exactly as the
orbit does. Detector = (band, N); a seed "crosses" iff its longest consecutive >=band run reaches N.
Window: verdict {0-7}, post-acquisition, [0,500k). Writes exp08/exp17_f6a_matched_bar.json.
"""
import json
from math import comb
from pathlib import Path

OUT = Path(__file__).parent / "exp08"


def series(path, field="exam_acc", t_max=500_000):
    r = json.load(open(path))
    on = r.get("acquisition_onset")
    vals = []
    for c in r["columns"]:
        v = c.get(field)
        if v is None:
            continue
        t = c["t"]
        if on is not None and t < on:      # post-acquisition
            continue
        if t >= t_max:                       # [0, 500k)
            continue
        vals.append(v)
    return vals


def longest_run(vals, band):
    best = cur = 0
    for v in vals:
        cur = cur + 1 if v >= band else 0
        best = max(best, cur)
    return best


def fisher_one_sided(k1, n1, k2, n2):
    K, Ntot = k1 + k2, n1 + n2
    return sum(comb(n1, k) * comb(n2, K - k)
              for k in range(k1, min(n1, K) + 1)) / comb(Ntot, K)


def arm(prefix, seeds, band, N):
    runs = [longest_run(series(str(OUT / prefix.format(s=s))), band) for s in seeds]
    conv = [s for s, lr in zip(seeds, runs) if lr >= N]
    return runs, conv


def main():
    V = list(range(8))
    ORBIT = "exp14_exp12_dwell_orbit_s{s}_exp17verdict.json"
    ADWELL = "exp14_exp12_dwell_s{s}_verdict.json"
    detectors = [dict(band=0.6111, N=4, fr=0.000439, owner="A_dwell"),
                 dict(band=0.6129, N=3, fr=0.000964, owner="orbit")]
    table = []
    for d in detectors:
        o_runs, o_conv = arm(ORBIT, V, d["band"], d["N"])
        a_runs, a_conv = arm(ADWELL, V, d["band"], d["N"])
        row = dict(detector=f"{d['band']}x{d['N']}", owner=d["owner"], fr=d["fr"],
                   orbit_k=len(o_conv), orbit_conv=o_conv, orbit_longest=o_runs,
                   a_k=len(a_conv), a_conv=a_conv, a_longest=a_runs,
                   fisher_orbit_ge_a=round(fisher_one_sided(len(o_conv), 8, len(a_conv), 8), 4))
        table.append(row)
        print(f"det {row['detector']} (fr {d['fr']}): orbit {row['orbit_k']}/8 {o_conv} | "
              f"A {row['a_k']}/8 {a_conv} | Fisher p={row['fisher_orbit_ge_a']}")
    # A-cal self-conversion at A's own detector
    _, acal = arm("exp14_exp12_dwell_s{s}_cal.json", [20, 21, 22, 24, 25], 0.6111, 4)
    committed = json.load(open(OUT / "exp14_band_2x2_cal.json"))["cells"]["A_dwell"][
        "per_cal_seed_converters"]
    out = dict(
        finding="F6-A matched-bar correction (EXP17 close): no matched-bar excess; DIRECTION-ONLY is "
                "a property of low-N band geometry + the symmetric cal-converts rule, not the orbit",
        window="verdict {0-7}, post-acquisition, [0,500k)",
        fr_ratio=round(0.000964 / 0.000439, 3),
        both_bars=table,
        a_cal_self_converts=dict(band=0.6111, N=4, converters=acal, k=len(acal),
                                 committed_per_cal_seed_converters=committed),
        note="fresh-code reproduction; imports nothing from the harness or the seat toolkit")
    (OUT / "exp17_f6a_matched_bar.json").write_text(json.dumps(out, indent=1))
    print(f"A-cal @0.6111x4: {acal} ({len(acal)}/5); fr ratio {out['fr_ratio']}x")
    print("-> exp08/exp17_f6a_matched_bar.json")


if __name__ == "__main__":
    main()
