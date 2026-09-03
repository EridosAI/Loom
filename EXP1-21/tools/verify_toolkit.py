#!/usr/bin/env python3
"""
verify_toolkit.py — INDEPENDENT terminal-verification toolkit (design seat, 2026-07-12).

PURPOSE. Preserves the design seat's verification capability as code: a deliberately
SECOND implementation of every load-bearing read, written from the prereg definitions
(never from exp14_arms/exp17_score), used all session to reproduce scorer outputs
digit-exact from raw committed records. If this toolkit and the harness agree, the
result is implementation-independent; if they disagree, one of them is wrong and the
disagreement is a finding (three recipe-deltas were caught exactly this way).

RULES OF USE.
- Every function's docstring IS its method-name. Canon figures cite the recipe.
- stdlib only (json, math, statistics, itertools, random). No torch, no numpy —
  runs anywhere, including a design-chat container.
- Never edit committed records. This reads; it does not write.

Verified equivalences this session (digit-exact unless noted): 32/32 EXP14 verdict
seeds (converters, onsets, episode lengths); all four bands' fr + n_null; B floor
4.50; matched-band sweep; EXP15 final-quartile MW p=0.0286/0.0952; EXP16 k=2 bare-4,
1M tail zero, gradient pair (recipe-delta, method-named); borrow-gate shift.
"""
import json, math, statistics, itertools, random
from math import comb

EVAL_CADENCE = 300  # steps per eval window (committed record convention)

# ---------------------------------------------------------------- record loading

def load_series(path, t_min=None, t_max=500_000, field="exam_acc", post_acq=True):
    """Per-window series from a committed run record.
    RECIPE: columns with non-null <field>; t >= acquisition_onset if post_acq;
    t <= t_max (pass t_max=None for the full horizon incl. the 1M tail);
    optional t_min for tail-only reads (e.g. t_min=500_001)."""
    r = json.load(open(path)); on = r.get("acquisition_onset")
    out = []
    for c in r["columns"]:
        if c.get(field) is None: continue
        t = c["t"]
        if post_acq and on is not None and t < on: continue
        if t_min is not None and t < t_min: continue
        if t_max is not None and t > t_max: continue
        out.append((t, c[field]))
    return [t for t, _ in out], [v for _, v in out], r

# ---------------------------------------------------------------- episodes / conversion

def episodes(vals, band, N):
    """Maximal runs of consecutive windows with value >= band, length >= N.
    Returns [(start_idx, length, mean)]. This IS the registered conversion detector
    (sustained-episode, EXP14 definition)."""
    eps, i, n = [], 0, len(vals)
    while i < n:
        if vals[i] >= band:
            j = i
            while j < n and vals[j] >= band: j += 1
            if j - i >= N: eps.append((i, j - i, sum(vals[i:j]) / (j - i)))
            i = j
        else:
            i += 1
    return eps

def convert_read(path, band, N, **kw):
    """Full per-seed read: converted?, conversion_onset (t of first qualifying
    window), episode lengths, longest, per-episode means."""
    ts, vals, _ = load_series(path, **kw)
    eps = episodes(vals, band, N)
    return dict(converted=bool(eps),
                conversion_onset=(ts[eps[0][0]] if eps else None),
                lengths=[l for _, l, _ in eps],
                longest=max((l for _, l, _ in eps), default=0),
                means=[round(m, 4) for _, _, m in eps])

# ---------------------------------------------------------------- nulls / floors

def episode_mask(vals, band, N):
    """Boolean mask of windows inside qualifying episodes (for null exclusion)."""
    n = len(vals); m = [False] * n; i = 0
    while i < n:
        if vals[i] >= band:
            j = i
            while j < n and vals[j] >= band: j += 1
            if j - i >= N:
                for k in range(i, j): m[k] = True
            i = j
        else:
            i += 1
    return m

def pooled_null(paths, excl_band, excl_N, **kw):
    """Honest-null pool: post-acq values across cal seeds, EXCLUDING windows inside
    (excl_band x excl_N) episodes. s0-class exclusion = (0.704, 8)."""
    pool = []
    for p in paths:
        _, v, _ = load_series(p, **kw)
        m = episode_mask(v, excl_band, excl_N)
        pool += [a for a, e in zip(v, m) if not e]
    return pool

def consec_rate(pool, band, N):
    """Per-POSITION false rate: fraction of length-N positions in the pooled null
    that are all >= band. This is the harness's fr definition (re-derived exact)."""
    hits = sum(1 for i in range(len(pool) - N + 1)
               if all(pool[i + j] >= band for j in range(N)))
    return hits / (len(pool) - N + 1)

def floor_expectation(fr, window_counts, N):
    """Naive independent-position phantom expectation over seeds:
    sum_i 1-(1-fr)^(n_i - N + 1). Reproduces the 4.50 (B, EXP14) exactly."""
    return sum(1 - (1 - fr) ** (n - N + 1) for n in window_counts)

def block_bootstrap_floor(null_seqs, lengths, band, N, block=25, sims=3000, seed=7):
    """Clustered floor: circular block bootstrap from per-seed null sequences,
    synthetic seeds at the verdict window counts; returns (mean, P(>=k) fn via list).
    Autocorrelation-preserving companion to floor_expectation."""
    rng = random.Random(seed); pool = [s for s in null_seqs if len(s) > 2 * block]
    counts = []
    for _ in range(sims):
        k = 0
        for L in lengths:
            out = []
            while len(out) < L:
                s = rng.choice(pool); st = rng.randrange(len(s))
                out += [s[(st + j) % len(s)] for j in range(block)]
            if episodes(out[:L], band, N): k += 1
        counts.append(k)
    counts.sort()
    return counts

# ---------------------------------------------------------------- statistics

def fisher_one_sided(k1, n1, k2, n2):
    """Exact one-sided Fisher: P(group-1 count >= k1 | margins), hypergeometric."""
    K, Ntot = k1 + k2, n1 + n2
    return sum(comb(n1, k) * comb(n2, K - k) for k in range(k1, min(n1, K) + 1)) / comb(Ntot, K)

def matched_bar_tab(paths_a, paths_b, det_a, det_b, window=None):
    """Matched-bar cross-arm table (EXP17 F6-A; canon §10.27; catch-ledger 16).
    Reads BOTH arms through BOTH detectors so every count is like-for-like — the
    UNLIKE-BAR comparison (arm-A read at A's detector vs arm-B at B's, with different
    false rates) is exactly the error this exists to make impossible. A cross-arm count
    is evidence only at a fixed (band, N); an unlike-bar count is context-only.
    det = dict(band, N, fr, owner); `fr` is the detector's OWN between-episode false
    rate (a cal property — passed in and REPORTED, never inferred from the verdict
    series). window = kwargs forwarded to load_series (t_min/t_max/field/post_acq);
    default = the committed verdict window [0, 500k) post-acq. Group-1 of the one-sided
    Fisher is paths_a: each row reports P(a_k >= b_k | margins). The per-seed `*_longest`
    columns are true longest runs (N=1), band-gated only. Returns {both_bars, fr_ratio}."""
    kw = window or {}
    na, nb = len(paths_a), len(paths_b)
    rows = []
    for d in (det_a, det_b):
        b, N = d["band"], d["N"]
        a_conv = [i for i, p in enumerate(paths_a) if convert_read(p, b, N, **kw)["converted"]]
        b_conv = [i for i, p in enumerate(paths_b) if convert_read(p, b, N, **kw)["converted"]]
        rows.append(dict(
            detector=f"{b}x{N}", owner=d.get("owner"), fr=d.get("fr"),
            a_k=len(a_conv), a_conv=a_conv,
            a_longest=[convert_read(p, b, 1, **kw)["longest"] for p in paths_a],
            b_k=len(b_conv), b_conv=b_conv,
            b_longest=[convert_read(p, b, 1, **kw)["longest"] for p in paths_b],
            fisher_a_ge_b=fisher_one_sided(len(a_conv), na, len(b_conv), nb)))
    fr_ratio = None
    if det_a.get("fr") and det_b.get("fr"):
        fr_ratio = max(det_a["fr"], det_b["fr"]) / min(det_a["fr"], det_b["fr"])
    return dict(both_bars=rows, fr_ratio=fr_ratio)

def mw_exact(a, b):
    """Exact tie-aware one-sided Mann-Whitney, P(U >= U_obs) by full enumeration
    (mid-ranks via 0.5 credit for ties). Feasible to ~C(24,10). Returns (U, p)."""
    U = sum((x > y) + 0.5 * (x == y) for x in a for y in b)
    pool, na = a + b, len(a); hits = tot = 0
    for idx in itertools.combinations(range(len(pool)), na):
        aa = [pool[i] for i in idx]
        bb = [pool[i] for i in range(len(pool)) if i not in idx]
        u = sum((x > y) + 0.5 * (x == y) for x in aa for y in bb)
        tot += 1; hits += (u >= U)
    return U, hits / tot

def final_quartile_tab(path, band, lo=375_000, hi=500_000):
    """EXP15 primary statistic: fraction of windows in (lo, hi] with exam_acc >= band.
    post_acq irrelevant for late windows but kept for form."""
    _, v, _ = load_series(path, t_min=lo + 1, t_max=hi, post_acq=False)
    return sum(1 for x in v if x >= band) / len(v)

# ---------------------------------------------------------------- gradients / density

def pos_gradient(paths, field="pos_err_word", buckets=("p1", "p13-48"), **kw):
    """Recency-gradient read, POST-ACQ RECIPE (the canon method): pooled mean of the
    per-window bucket values across seeds; Delta = mean(p1) - mean(p13-48).
    (The retired late-half recipe differed; always name the recipe.)"""
    acc = {b: [] for b in buckets}
    for p in paths:
        r = json.load(open(p)); on = r["acquisition_onset"]
        for c in r["columns"]:
            if c["t"] < on: continue
            pw = c.get(field) or {}
            for b in buckets:
                if pw.get(b) is not None: acc[b].append(pw[b])
    m = {b: statistics.mean(acc[b]) for b in buckets}
    m["delta"] = m[buckets[0]] - m[buckets[-1]]
    return m

def exam_density(paths, **kw):
    """Pooled mean exam_n per window post-acq (the load-confound check:
    EXP14 measured A 27.48 / C 27.44 / B 13.72 / D 13.68)."""
    xs = []
    for p in paths:
        _, v, _ = load_series(p, field="exam_n", **kw)
        xs += v
    return statistics.mean(xs)

# ---------------------------------------------------------------- kinematics (pose traces)

def net_path_traverse(pose_seq, bound=1.5):
    """Per-dwell kinematics from a pose trajectory [[axis...]...]:
    net/path = |end-start| / sum |steps| ; traverse = mean over axes of
    (max-min)/(2*bound). Folded/delivered-pose convention (the honest statistic)."""
    def norm(v): return math.sqrt(sum(x * x for x in v))
    steps = [norm([a - b for a, b in zip(pose_seq[i + 1], pose_seq[i])])
             for i in range(len(pose_seq) - 1)]
    net = norm([a - b for a, b in zip(pose_seq[-1], pose_seq[0])])
    K = len(pose_seq[0])
    trav = statistics.mean(
        (max(p[k] for p in pose_seq) - min(p[k] for p in pose_seq)) / (2 * bound)
        for k in range(K))
    return net / sum(steps), trav, statistics.mean(steps)

# ---------------------------------------------------------------- self-test

def _f6a_anchor_and_smoke():
    """Record anchor: matched_bar_tab reproduces exp17_f6a_matched_bar.json digit-exact.
    Positive-delta smoke: a PERTURBED detector must change the tab — the reachable
    falsifier the F6-A catch earned (a tab insensitive to its own (band, N) would be a
    silent unlike-bar hazard). Skips cleanly if the committed records are not present."""
    from pathlib import Path
    exp08 = Path(__file__).resolve().parent.parent / "experiments" / "05_attention_sculpting" / "exp08"
    ref = exp08 / "exp17_f6a_matched_bar.json"
    orbit = [exp08 / f"exp14_exp12_dwell_orbit_s{s}_exp17verdict.json" for s in range(8)]
    adwell = [exp08 / f"exp14_exp12_dwell_s{s}_verdict.json" for s in range(8)]
    if not (ref.exists() and all(p.exists() for p in orbit + adwell)):
        print("verify_toolkit F6-A anchor: SKIP (records not present)")
        return
    j = json.load(open(ref))
    det_a = dict(band=0.6111, N=4, fr=0.000439, owner="A_dwell")   # A_dwell's own detector
    det_b = dict(band=0.6129, N=3, fr=0.000964, owner="orbit")     # the orbit's own detector
    op = [str(p) for p in orbit]; ap = [str(p) for p in adwell]
    tab = matched_bar_tab(op, ap, det_a, det_b)                    # group-1 = orbit (= json 'orbit_*')
    for row, jr in zip(tab["both_bars"], j["both_bars"]):
        assert row["a_k"] == jr["orbit_k"] and row["a_conv"] == jr["orbit_conv"]
        assert row["a_longest"] == jr["orbit_longest"]
        assert row["b_k"] == jr["a_k"] and row["b_conv"] == jr["a_conv"]
        assert row["b_longest"] == jr["a_longest"]
        assert round(row["fisher_a_ge_b"], 4) == jr["fisher_orbit_ge_a"]
    assert round(tab["fr_ratio"], 3) == j["fr_ratio"]
    # reachable falsifier: perturb the orbit detector (band AND N); the tab MUST move.
    pert = matched_bar_tab(op, ap, det_a, dict(det_b, band=0.62, N=8))
    base_row, pert_row = tab["both_bars"][1], pert["both_bars"][1]
    assert (base_row["a_k"], base_row["a_longest"]) != (pert_row["a_k"], pert_row["a_longest"]), \
        "perturbed detector did not change the tab — the falsifier is unreachable"
    print("verify_toolkit F6-A anchor: PASS (matched-bar digit-exact; perturbation moves the tab)")

if __name__ == "__main__":
    # Anchors that must hold forever (analytic, record-free):
    assert abs(fisher_one_sided(4, 8, 0, 8) - 0.0385) < 5e-4      # EXP14 clean leg
    assert abs(fisher_one_sided(2, 10, 0, 8) - 0.2941) < 5e-4     # EXP16 raw k
    assert abs(fisher_one_sided(1, 8, 0, 8) - 0.5) < 1e-9         # F6-A A-bar row (0.6111x4)
    assert abs(fisher_one_sided(5, 8, 3, 8) - 0.3096) < 5e-4      # F6-A orbit-bar row (0.6129x3)
    _, p = mw_exact([0.812, 0.072, 0.115, 0.409], [0.070, 0.050, 0.082, 0.024])
    assert abs(p - 0.0286) < 1e-3                                  # EXP15 committed-context
    fr, n = 0.000613, [1041, 752, 1592, 1450, 1585, 1543, 1591, 1472]
    assert abs(floor_expectation(fr, n, 3) - 4.50) < 0.06          # B floor
    print("verify_toolkit self-test: PASS (6 analytic anchors)")
    # Record-backed matched-bar anchor + reachable-falsifier smoke (skips if records absent):
    _f6a_anchor_and_smoke()
