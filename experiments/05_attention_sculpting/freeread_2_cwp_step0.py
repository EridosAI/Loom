"""FREE-READ (ii) — CWP STEP-0: per-dwell-position update pressure.

Memo: docs/FREE_READS_MEMO.md §(ii).  Recipe: MECHANISM_MAP_v1_2_RECONCILED.md §5.2 — estimate
per-dwell-position update pressure (loss/surprise by within-dwell position) from the committed
records' pos_err_* buckets, to test CWP's premise that within-dwell updates are LOW-SURPRISE MASSED.
Kill (v1.2 §6): within-dwell updates NOT low-surprise massed -> CWP's premise fails in-substrate ->
the CWP program closes before it opens.

The premise has two limbs: (a) mid-dwell (pos>1) update pressure is LOW and non-rising within the
dwell; (b) the boundary (a ~99% pose jump at pos 1) SPIKES. This read reports the pooled post-acq
pressure profile by within-dwell position for both channels (vision-completion = pos_err_vis, the
channel CWP gates; onset word = pos_err_word) on the L1 (orbit) arm and the A_dwell (tremble) arm,
per seed and pooled. It does NOT rule the kill — that judgment routes to the seat.

Read-only: committed JSON records only, no build.
"""
import json, statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "exp08"

WORD_POS = ["p1", "p2", "p3", "p4-6", "p7-12", "p13-48"]   # within-dwell position order (word)
VIS_POS = ["p2", "p3", "p4-6", "p7-12", "p13-48"]          # vision masked mid-dwell only (no p1)
ARMS = {
    "orbit_L1": "exp14_exp12_dwell_orbit_s{s}_exp17verdict.json",
    "A_dwell_tremble": "exp14_exp12_dwell_s{s}_verdict.json",
}
SEEDS = list(range(8))


def _profile(path):
    """Per-record pooled-by-position mean of pos_err_word / pos_err_vis over POST-ACQ columns
    (equal weight per column — the committed _recency_gradient pooling, exp17_score.py:483)."""
    r = json.load(open(path))
    on = r.get("acquisition_onset")
    accw = {b: [] for b in WORD_POS}
    accv = {b: [] for b in VIS_POS}
    ncol = 0
    for c in r["columns"]:
        if on is not None and c["t"] < on:
            continue
        pw = c.get("pos_err_word") or {}
        pv = c.get("pos_err_vis") or {}
        if not pw and not pv:
            continue
        ncol += 1
        for b in WORD_POS:
            if pw.get(b) is not None:
                accw[b].append(pw[b])
        for b in VIS_POS:
            if pv.get(b) is not None:
                accv[b].append(pv[b])
    word = {b: (statistics.mean(accw[b]) if accw[b] else None) for b in WORD_POS}
    vis = {b: (statistics.mean(accv[b]) if accv[b] else None) for b in VIS_POS}
    return dict(onset=on, n_postacq_cols=ncol, word=word, vis=vis)


def _limb_summary(word, vis):
    """Operationalize the two premise limbs as reported numbers (NOT a verdict):
    word_boundary_drop = p1 - p13-48 (boundary spike relative to deep-dwell, expect > 0);
    vis_within_slope   = p13-48 - p2  (mid-dwell trend; > 0 means surprise RISES within dwell =
                                        the opposite of 'low-surprise massed')."""
    wbd = (word["p1"] - word["p13-48"]) if (word["p1"] is not None and word["p13-48"] is not None) else None
    vws = (vis["p13-48"] - vis["p2"]) if (vis["p13-48"] is not None and vis["p2"] is not None) else None
    return dict(word_boundary_drop_p1_minus_p13_48=wbd, vis_within_slope_p13_48_minus_p2=vws)


def _pool(profiles, keys):
    return {b: (statistics.mean([p[b] for p in profiles if p[b] is not None])
               if any(p[b] is not None for p in profiles) else None) for b in keys}


def main():
    arms_out = {}
    for arm, tmpl in ARMS.items():
        per = []
        for s in SEEDS:
            path = OUT / tmpl.format(s=s)
            pr = _profile(path)
            pr["seed"] = s
            pr["summary"] = _limb_summary(pr["word"], pr["vis"])
            per.append(pr)
        pooled_word = _pool([p["word"] for p in per], WORD_POS)
        pooled_vis = _pool([p["vis"] for p in per], VIS_POS)
        arms_out[arm] = dict(
            record_template=tmpl,
            pooled=dict(word=pooled_word, vis=pooled_vis,
                        summary=_limb_summary(pooled_word, pooled_vis)),
            per_seed=per)
    out = dict(
        read="(ii) CWP step-0 — per-dwell-position update pressure",
        memo_section="docs/FREE_READS_MEMO.md §(ii)",
        recipe="MECHANISM_MAP_v1_2_RECONCILED.md §5.2 (kill = §6)",
        method=("per-within-dwell-position pooled mean of pos_err_word/pos_err_vis over post-acq "
                "columns (equal weight per column; the committed _recency_gradient pooling). "
                "word_boundary_drop = p1 - p13-48; vis_within_slope = p13-48 - p2."),
        inputs=dict(arms=ARMS, seeds=SEEDS,
                    code_modules=[], note="pure committed-record read; no fabric build"),
        consequence=dict(
            memo_condition="within-dwell updates NOT low-surprise massed -> CWP program closes before "
                           "it opens (v1.2 §6)",
            premise_limbs=("(a) mid-dwell pos>1 pressure LOW and non-rising; "
                           "(b) boundary pos-1 spikes"),
            triggered="ROUTES (judgment): the profile numbers below are reported; whether they meet "
                      "'low-surprise massed' is the seat's ruling. Key figures per arm in "
                      "pooled.summary (word_boundary_drop, vis_within_slope)."),
        arms=arms_out)
    OUT.mkdir(exist_ok=True)
    (OUT / "freeread_2_cwp_step0.json").write_text(json.dumps(out, indent=1, sort_keys=True))
    for arm, a in arms_out.items():
        sm = a["pooled"]["summary"]
        print("%-16s word_boundary_drop=%.4f  vis_within_slope=%.4f"
              % (arm, sm["word_boundary_drop_p1_minus_p13_48"], sm["vis_within_slope_p13_48_minus_p2"]))
    print("-> exp08/freeread_2_cwp_step0.json")


if __name__ == "__main__":
    main()
