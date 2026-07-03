"""EXP10 — structured variation ("reality is the teacher"): the varied loops, the
nuisance family, calibrations, the parity gate, and the guarded scorer.

Pre-registration: docs/EXP10_STRUCTURED_VARIATION_PREREG.md (checkpoint pins ruled
2026-07-04; this module implements the RESOLVE + WIRE phase — ARMS DO NOT RUN until the
final pre-run read ratifies. Gate steps 5-6 BLOCKED).

THE UNPREDICTABILITY PIN, implemented:
  1. Unpredictable as a sequence — per-wave i.i.d. coefficient draws, counter-keyed on a
     DEDICATED seeded stream (never loop.gen): stochastic to the system, deterministic to
     the harness. No cycles, no schedules.
  2. Uninformative about identity — the K structured axes are an orthonormal basis of the
     stimulus COMPLEMENT block (indices outside [a | distractor | category]) mapped
     through the same Q: exactly ⟂ every identity centre difference BY CONSTRUCTION;
     finite-sample independence asserted numerically at manifest time vs a shuffle-null.
  3. Learnable as a distribution — the axes are FIXED for the run (family recurring);
     only the coefficients are drawn per wave.
Because the nuisance stream is dedicated and counter-keyed, a varied arm shares
BIT-IDENTICAL stimulus noise + masks with its static counterpart at the same seed
(single-variable discipline). Caveat (recorded): the counter advances on every raw()
call, so inserting/removing a probe shifts subsequent nuisance keys — the same replay
caveat class as loop.gen consumption.

Word jiggle (#12 on the input distribution): i.i.d. scatter around the FROZEN token
centroids, applied only at presentation (the `_vary_word` identity-default hook in
build_cells); evocation/probe/manifest paths call word.emit directly and stay clean.
The centroid map is never touched (frozen anchor; param_delta assert stands).

Determinism contract: seed + construction order + torch threads (pinned 1, recorded).\nRESUME CAVEAT (recorded): varied arms have NO resume-grade save — save_state does not\npersist the nuisance/jiggle counters (stim._calls, _jig_calls); varied arms run\nstart-to-finish.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import constants                                              # noqa: E402
import exp08_arms as A                                        # noqa: E402
import exp09_arms as X9                                       # noqa: E402
from conflict_stream import ConflictStimulus                  # noqa: E402
from revival import dynamics_panel                            # noqa: E402
from sculpt_config import SculptConfig                        # noqa: E402

OUTDIR = A.OUTDIR
EVAL = A.EVAL

# --- resolved constants (checkpoint pins, 2026-07-04; [RECONCILE]-at-read values land at
# the final pre-run read from the calibration artifacts, never re-typed downstream) ---
K_AXES = 4                       # proposed [RECONCILE at read]; complement block has D-8 = 8 dims
NUIS_SEED_BASE = 77000           # the dedicated nuisance stream's seed base (per-arm offset by cfg.seed)
JIG_SEED_BASE = 88000
HORIZON_NODETACH = 160000        # >= 2x the 75.3k measured pin onset (pin 6)
HORIZON_REF = 192000             # EXP09 comparability (pin 6)
CAL_SEEDS = [10, 11]             # dedicated calibration seeds — never verdict seeds (pin 7)
VERDICT_SEEDS = [0, 1, 2]


# ------------------------------------------------------------------ the nuisance family
class NuisanceStimulus(ConflictStimulus):
    """ConflictStimulus + the structured (or isotropic) nuisance family on raw() draws.

    structured: coeffs ~ N(0, coeff_std^2) per axis per row, axes = complement-block
    orthonormal basis @ Q^T (clause-2 orthogonality by construction).
    isotropic:  the annealing discriminator (pin 8 extension) — direction-free noise at
    MATCHED TOTAL POWER (sigma_iso^2 * D = coeff_std^2 * K); bleeds into identity axes
    by construction (that is the point: structure-free generic regularization).
    raw_clean() stays clean — every primary read is nuisance-marginalized by construction.
    """

    def __init__(self, *args, coeff_std: float = 0.0, k_axes: int = K_AXES,
                 family: str = "structured", nuis_seed: int = 0, **kw):
        super().__init__(*args, **kw)
        self.coeff_std, self.k_axes, self.family = float(coeff_std), int(k_axes), family
        self.nuis_seed = int(nuis_seed)
        self._calls = 0
        n_id = self.n_A + self.n_distractor + self.n_category
        if n_id + self.k_axes > self.D:
            raise ValueError("complement block too small for k_axes")
        basis = torch.zeros(self.k_axes, self.D)
        for i in range(self.k_axes):
            basis[i, n_id + i] = 1.0                       # complement block, pre-rotation
        self.axes = basis @ self.Q.t()                     # (K, D), exactly ⟂ identity axes
        self.sigma_iso = (self.coeff_std * (self.k_axes / self.D) ** 0.5)

    def nuisance(self, n_rows: int) -> tuple[torch.Tensor, torch.Tensor]:
        """(noise (n_rows, D), coeffs (n_rows, K or D)) from the DEDICATED counter stream."""
        g = torch.Generator().manual_seed(self.nuis_seed * 1_000_003 + self._calls)
        self._calls += 1
        if self.family == "isotropic":
            n = self.sigma_iso * torch.randn(n_rows, self.D, generator=g)
            return n, n
        c = self.coeff_std * torch.randn(n_rows, self.k_axes, generator=g)
        return c @ self.axes, c

    def raw(self, a, b, gen):
        base = super().raw(a, b, gen)
        if self.coeff_std == 0.0:
            return base                                    # parity path: zero draws, zero adds
        n, _ = self.nuisance(base.shape[0])
        return base + n


# ------------------------------------------------------------------ the varied loops
class VariedMixin:
    """Adds the frozen-centroid word jiggle via the `_vary_word` identity-default hook.
    Nuisance rides the stimulus (NuisanceStimulus via `_make_stim`), not the loop."""

    def _make_stim(self):
        cfg = self.cfg
        v = getattr(cfg, "_exp10", dict(coeff_std=0.0, k_axes=K_AXES, family="structured",
                                        jiggle_sigma=0.0))
        return NuisanceStimulus(
            cfg.D, cfg.n_A, cfg.n_distractor, cfg.n_category,
            R_coarse=cfg.R_coarse, r_distractor=cfg.r_distractor,
            r_category=cfg.r_category, sigma=cfg.sigma_stim, seed=cfg.seed,
            coeff_std=v["coeff_std"], k_axes=v["k_axes"], family=v["family"],
            nuis_seed=NUIS_SEED_BASE + cfg.seed)

    def _vary_word(self, e_word, tokens):
        v = getattr(self.cfg, "_exp10", None)
        sig = 0.0 if v is None else v.get("jiggle_sigma", 0.0)
        if sig == 0.0:
            return e_word                                  # parity path: identity, zero draws
        if not hasattr(self, "_jig_calls"):
            self._jig_calls = 0
        g = torch.Generator().manual_seed((JIG_SEED_BASE + self.cfg.seed) * 1_000_003
                                          + self._jig_calls)
        self._jig_calls += 1
        return e_word + sig * torch.randn(e_word.shape, generator=g)


class VariedWordLoop(VariedMixin, A.EXP08Loop):
    """no-detach × varied — the direct-test arm (deployed teaching topology intact)."""


class VariedSlowRefLoop(VariedMixin, X9.SlowRefLoop):
    """slowref × varied."""


class VariedDetachLoop(VariedMixin, A.DetachLoop):
    """detachnull × varied — the comparator (diagnostic, never a fix)."""


ARMS10 = {
    # verdict arms (pins 6): DO NOT RUN until the final pre-run read ratifies
    "nodetach_varied":   dict(loop=VariedWordLoop, no_word=False, steps=HORIZON_NODETACH,
                              seeds=VERDICT_SEEDS),
    "slowref_varied":    dict(loop=VariedSlowRefLoop, no_word=False, steps=HORIZON_REF,
                              seeds=VERDICT_SEEDS),
    "detachnull_varied": dict(loop=VariedDetachLoop, no_word=False, steps=HORIZON_REF,
                              seeds=VERDICT_SEEDS),
    # the annealing discriminator (pin 8 extension): isotropic at matched power
    "nodetach_isotropic": dict(loop=VariedWordLoop, no_word=False, steps=HORIZON_NODETACH,
                               seeds=VERDICT_SEEDS, family="isotropic"),
    # dedicated calibration arm (pin 7): spans for in-regime constants; never verdicted
    "nodetach_varied_cal": dict(loop=VariedWordLoop, no_word=False, steps=HORIZON_NODETACH,
                                seeds=CAL_SEEDS),
}


def build_varied(arm_name: str, seed: int, coeff_std: float, jiggle_sigma: float):
    spec = ARMS10[arm_name]
    pin = constants.PinnedConstants()
    cfg = SculptConfig(seed=seed)
    cfg._exp10 = dict(coeff_std=coeff_std, k_axes=K_AXES,
                      family=spec.get("family", "structured"), jiggle_sigma=jiggle_sigma)
    loop = spec["loop"](cfg, pin)
    return loop, spec, cfg


# ------------------------------------------------------------------ the parity gate (pin 9a)
def parity_gate():
    """HARD GATE before any varied run: the varied code path with variation ZEROED must
    reproduce the committed word_terminal_s1 standing columns bit-identically. Exercises
    the modified loop.py (`_vary_word` identity hook), VariedMixin, NuisanceStimulus at
    coeff_std=0, and the MRO through EXP08Loop."""
    # ONE code path, no patching: A.build_loop constructs VariedWordLoop(cfg, pin) with
    # no `_exp10` flag on cfg -> both hooks default to ZERO variation (identity, zero
    # draws) — which IS the parity configuration.
    A.ARMS["parity_wt1"] = dict(loop=VariedWordLoop, no_word=False, steps=112500, seeds=[1])
    rec = A.run_arm("parity_wt1", 1)
    committed = json.loads((OUTDIR / "word_terminal_s1.json").read_text())
    assert len(rec["columns"]) == len(committed["columns"]), "parity: window count differs"
    mism = []
    for c_new, c_old in zip(rec["columns"], committed["columns"]):
        for k in A._STANDING_COLS:
            if c_new.get(k) != c_old.get(k):
                mism.append((c_new["t"], k, c_old.get(k), c_new.get(k)))
    assert rec["grad_split"] == committed["grad_split"], "parity: grad_split diverged"
    assert rec["occupancy"] == committed["occupancy"], "parity: occupancy diverged"
    assert not mism, f"PARITY FAIL: {mism[:5]} (+{max(0, len(mism) - 5)})"
    for f in OUTDIR.glob("parity_wt1_s1.*"):
        f.unlink()                                         # gate artifact, not a record
    print("PARITY GATE PASS: varied code path (variation zeroed) BIT-IDENTICAL to committed "
          f"word_terminal_s1 ({len(rec['columns'])} windows; hooks + MRO + NuisanceStimulus "
          "exercised)")
    return True


# ------------------------------------------------------------------ calibrations (resolve)
def calibrate_jiggle():
    """Pin 2: sigma from the pairwise centroid matrix — empirical 100%-NC threshold
    ACROSS ALL RUN SEEDS (verdict {0,1,2} + calibration {10,11}; WordCortex seed =
    cfg.seed+1), then sigma* = min-threshold/2 (comfortably inside EVERY basin,
    parent-voice). Calibration uses a synthetic balanced token sample (no manifest
    exists pre-run); re-affirmed on each arm's manifest sample at Step-0."""
    from encoders import WordCortex
    per_seed = []
    for seed in VERDICT_SEEDS + CAL_SEEDS:
        cfg = SculptConfig(seed=seed)
        wc = WordCortex(cfg.D, cfg.n_category, seed=cfg.seed + 1)
        emb = wc.embed.weight.detach()
        pair = torch.cdist(emb, emb)
        off = ~torch.eye(emb.shape[0], dtype=torch.bool)
        d_min = float(pair[off].min())
        g = torch.Generator().manual_seed(4242 + seed)
        n_total = 200_000
        sig_100 = None
        for sig in [round(0.02 * i, 2) for i in range(1, 40)]:
            toks = torch.arange(emb.shape[0]).repeat_interleave(n_total // emb.shape[0])
            e = emb[toks] + sig * torch.randn(len(toks), cfg.D, generator=g)
            if float((torch.cdist(e, emb).argmin(1) == toks).float().mean()) < 1.0:
                break
            sig_100 = sig
        per_seed.append(dict(seed=seed, word_seed=seed + 1, d_min=round(d_min, 4),
                             sigma_100pct=sig_100))
    sig_min = min(p["sigma_100pct"] for p in per_seed)
    sigma_star = round(sig_min / 2, 3)
    out = dict(per_seed=per_seed, sigma_100pct_min=sig_min, sigma_star=sigma_star,
               d_min_min=min(p["d_min"] for p in per_seed),
               fraction_of_dmin_min=round(sigma_star / min(p["d_min"] for p in per_seed), 4),
               n_samples_total_per_seed=200_000,
               note="sigma* = half the MINIMUM cross-seed 100%-NC threshold (all run "
                    "seeds, 3 tokens incl. null, ~66.7k samples/token per seed); "
                    "synthetic balanced sample — re-affirmed per-arm at Step-0/manifest")
    print("JIGGLE:", json.dumps({k: v for k, v in out.items() if k != "per_seed"}))
    print("  per-seed:", json.dumps(per_seed))
    return out


def calibrate_nuisance_rungs():
    """Pin 1: magnitude rungs + the (b)-ceiling rule — category_oracle_rec re-run under
    nuisance at each rung (the environment includes the nuisance; the oracle must still
    recover the category). Rungs set relative to the load-bearing cue r_category=0.5:
    total nuisance RMS in {0.5x, 1x, 2x} r_category -> per-axis coeff_std = RMS/sqrt(K)."""
    import category_oracle as CO
    import conflict_validity as CV
    cfg = SculptConfig(seed=0)
    pin = constants.PinnedConstants()
    P = CV.CONFLICT_PARAMS
    rungs = []
    orig_stim = CO.ConflictStimulus
    for mult in [0.0, 0.5, 1.0, 2.0]:
        total = mult * cfg.r_category
        coeff = total / (K_AXES ** 0.5)

        def make(D, n_A, n_d, n_c, **kw):
            return NuisanceStimulus(D, n_A, n_d, n_c, coeff_std=coeff, k_axes=K_AXES,
                                    family="structured", nuis_seed=NUIS_SEED_BASE, **kw)
        CO.ConflictStimulus = make
        try:
            recs, abls, easies = [], [], []
            for s in range(3):
                c = SculptConfig(seed=s)
                orc = CO.category_oracle_rec(c, pin, steps=P["oracle_steps"])
                recs.append(orc["oracle_category_rec"])
                abls.append(orc["ablation_collapsed"])
                easy = SculptConfig(seed=s)
                easy.r_category = easy.r_distractor
                easies.append(CO.category_oracle_rec(easy, pin, steps=P["oracle_steps"])
                              ["oracle_category_rec"])
        finally:
            CO.ConflictStimulus = orig_stim
        chance = 1.0 / cfg.n_category
        easy_ceiling = statistics.mean(easies)
        bar = chance + P["margin_oracle_frac"] * (easy_ceiling - chance)
        rungs.append(dict(mult=mult, total_rms=round(total, 4), coeff_std=round(coeff, 4),
                          oracle_rec=[round(r, 4) for r in recs],
                          oracle_mean=round(statistics.mean(recs), 4),
                          ablation_collapsed=abls, easy_ceiling=round(easy_ceiling, 4),
                          bar=round(bar, 4),
                          clears=bool(statistics.mean(recs) >= bar and all(abls))))
        print(f"RUNG x{mult}: oracle {rungs[-1]['oracle_mean']} vs bar {rungs[-1]['bar']} "
              f"-> {'CLEARS' if rungs[-1]['clears'] else 'BELOW FLOOR'}")
    return rungs


def independence_asserts(coeff_std: float, jiggle_sigma: float, n=2000, n_null=1000):
    """Pin 3: max |corr(nuisance coeffs, identity labels)| and jiggle-residual ⟂
    non-token labels, thresholds from a shuffle-null at manifest time. Numeric."""
    cfg = SculptConfig(seed=0)
    stim = NuisanceStimulus(cfg.D, cfg.n_A, cfg.n_distractor, cfg.n_category,
                            R_coarse=cfg.R_coarse, r_distractor=cfg.r_distractor,
                            r_category=cfg.r_category, sigma=cfg.sigma_stim, seed=cfg.seed,
                            coeff_std=coeff_std, k_axes=K_AXES, nuis_seed=NUIS_SEED_BASE)
    g = torch.Generator().manual_seed(999)
    a = torch.randint(0, cfg.n_A, (n,), generator=g)
    b = torch.randint(0, cfg.n_B, (n,), generator=g)
    _, coeffs = stim.nuisance(n)
    labels = torch.stack([a.float(), (b // cfg.n_category).float(),
                          (b % cfg.n_category).float()], dim=1)   # a / distractor / category

    def max_abs_corr(x, y):
        xc = (x - x.mean(0)) / (x.std(0) + 1e-12)
        yc = (y - y.mean(0)) / (y.std(0) + 1e-12)
        return float((xc.t() @ yc / len(x)).abs().max())

    obs = max_abs_corr(coeffs, labels)
    null = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(5000 + i)
        null.append(max_abs_corr(coeffs, labels[torch.randperm(n, generator=gp)]))
    thr = sorted(null)[int(0.99 * n_null)]
    # jiggle residual vs non-token labels (residual is iid by construction; asserted anyway)
    from encoders import WordCortex
    wc = WordCortex(cfg.D, cfg.n_category, seed=cfg.seed + 1)
    toks = (b % cfg.n_category)
    gj = torch.Generator().manual_seed(31337)
    resid = jiggle_sigma * torch.randn(n, cfg.D, generator=gj)
    obs_j = max_abs_corr(resid, labels)
    null_j = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(7000 + i)
        null_j.append(max_abs_corr(resid, labels[torch.randperm(n, generator=gp)]))
    thr_j = sorted(null_j)[int(0.99 * n_null)]
    out = dict(n=n, nuis_obs=round(obs, 4), nuis_null99=round(thr, 4),
               nuis_ok=bool(obs <= thr),
               jig_obs=round(obs_j, 4), jig_null99=round(thr_j, 4),
               jig_ok=bool(obs_j <= thr_j),
               axes_identity_dot=round(float(
                   (stim.axes @ (stim.centre.reshape(-1, cfg.D)
                                 - stim.centre.reshape(-1, cfg.D).mean(0)).t()).abs().max()), 8))
    print("INDEPENDENCE:", json.dumps(out))
    return out


# ------------------------------------------------------------------ guarded scorer (pin 9b)
def function_test_read_v2(cols, *, control: bool, pinned_period: int | None = None) -> dict:
    """The SS10.14 scorer guards applied: (a) period substitution requires an actual
    collapse cycle (>=1 qualifying window) — else the pinned constant; (b) the PASS
    window scales with the used period (count threshold rescaled; the run-length limit
    stays absolute at the calibrated 2); (c) COPY-COLLAPSE goes mechanical when
    ref_pairwise is present (any post-crossing window < 3e-4)."""
    pinned = pinned_period or (X9.PERIOD_NOWORD if control else X9.PERIOD_WORD)
    any_qualifying = any(c["asg_argmax_k"] == 1 and c["den"] < X9.FLOOR for c in cols)
    per = X9._healthy_segment_period(cols, pinned)
    if per["substituted"] and not any_qualifying:
        per = dict(per, used=pinned, substituted=False,
                   note="substitution GATED: no collapse cycle in run (guard a)")
    period = per["used"]
    K = X9.K_C if control else X9.K_W
    eps = X9._epochs(cols, period)
    episodes = [e for e in eps if not e["at_horizon"]]
    verdict_pin = None
    for e in eps:
        if e["at_horizon"]:
            kind = ("PIN" if e["span"] >= K * period else "PIN_CENSORED")
            verdict_pin = dict(kind=kind, epoch=e)
    out = dict(period_resolution=per, period=period, K=K, scorer="v2-guarded",
               metastable_episodes=episodes, horizon_epoch=verdict_pin)
    if "ref_pairwise" in cols[0]:
        crossed = [c["t"] for c in cols if c["ref_pairwise"] >= 3e-4]
        sub_after = ([c["t"] for c in cols
                      if c["t"] > crossed[0] and c["ref_pairwise"] < 3e-4] if crossed else
                     [c["t"] for c in cols])
        out["copy_collapse"] = dict(first_crossing=(crossed[0] if crossed else None),
                                    post_crossing_subfloor=len(sub_after),
                                    fired=bool(not crossed or sub_after))
        if out["copy_collapse"]["fired"]:
            out["verdict"] = "COPY_COLLAPSE"
            return out
    if control:
        out["verdict"] = verdict_pin["kind"] if verdict_pin else "NO_PIN"
        return out
    n_win = max(1, (2 * period) // EVAL)
    k_min = -(-X9.PASS_K_MIN * n_win // X9.PASS_WINDOWS)      # ceil(27/32 * n_win)
    fin = cols[-n_win:]
    k_ok = sum(1 for c in fin if c["asg_argmax_k"] > 1)
    run = best = 0
    for c in fin:
        run = run + 1 if c["asg_argmax_k"] == 1 else 0
        best = max(best, run)
    den_ok = sum(1 for c in fin if c["den"] >= X9.FLOOR)
    out["pass_criteria"] = dict(n_windows=n_win, k_gt1_count=k_ok, k_gt1_min=k_min,
                                k1_run_max=best, k1_run_limit=X9.PASS_RUN_MAX,
                                den_ok_count=den_ok, den_ok_min=n_win)
    pinned_fail = verdict_pin is not None and verdict_pin["kind"] == "PIN"
    passed = (not pinned_fail and k_ok >= k_min and best <= X9.PASS_RUN_MAX
              and den_ok == n_win)
    out["verdict"] = ("FAIL_PIN" if pinned_fail else
                      "PASS_PENDING_SCREEN" if passed else
                      verdict_pin["kind"] if verdict_pin else "NEITHER")
    return out


def rescore_static():
    """Pin 9b: re-score the static cells under the guarded scorer; report changes."""
    cells = [("slowref_word_s0", False), ("slowref_word_s1", False),
             ("slowref_noword_s0", True), ("detachnull_s1", False),
             ("word_terminal_s1_decomp", False), ("marathon_ext_s0_decomp", True)]
    table = []
    for name, control in cells:
        rec = json.loads((OUTDIR / f"{name}.json").read_text())
        old = rec.get("function_test_read", {}).get("verdict", "(none scored)")
        v2 = function_test_read_v2(rec["columns"], control=control)
        table.append(dict(cell=name, v1=old, v2=v2["verdict"],
                          period_used=v2["period"],
                          period_note=v2["period_resolution"].get("note", ""),
                          changed=bool(old != "(none scored)" and old != v2["verdict"])))
        print(f"{name}: v1={old} -> v2={v2['verdict']} (period {v2['period']}"
              f"{'; ' + v2['period_resolution'].get('note', '') if v2['period_resolution'].get('note') else ''})")
    return table


def smoke():
    """Wiring asserts on the varied loops (variation ON, short)."""
    loop, _, cfg = build_varied("nodetach_varied", 0, coeff_std=0.25, jiggle_sigma=0.06)
    assert isinstance(loop.stim, NuisanceStimulus) and loop.stim.coeff_std == 0.25
    # clause-2 exact orthogonality: axes ⟂ every identity centre difference
    C = loop.stim.centre.reshape(-1, cfg.D)
    dots = (loop.stim.axes @ (C - C.mean(0)).t()).abs().max()
    assert float(dots) < 1e-5, f"axes not orthogonal to identity structure: {dots}"
    # clean probes stay clean
    ma = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
    mb = torch.arange(cfg.n_B).repeat(cfg.n_A)
    assert torch.equal(loop.stim.raw_clean(ma, mb), loop.stim.centre[ma, mb])
    for t in range(1, 301):
        loop.step(no_word=False)
    assert loop.word.param_delta() == 0.0, "anchor went plastic under jiggle"
    # slowref + detach varied MROs construct and step
    l2, _, _ = build_varied("slowref_varied", 0, coeff_std=0.25, jiggle_sigma=0.06)
    l3, _, _ = build_varied("detachnull_varied", 1, coeff_std=0.25, jiggle_sigma=0.06)
    for lp in (l2, l3):
        for t in range(1, 31):
            lp.step(no_word=False)
    assert hasattr(l2, "vision_slow")
    # isotropic power match
    li, _, ci = build_varied("nodetach_isotropic", 0, coeff_std=0.25, jiggle_sigma=0.06)
    ns, _ = li.stim.nuisance(4096)
    ss, _ = loop.stim.nuisance(4096)
    pi, ps = float(ns.pow(2).sum(1).mean()), float(ss.pow(2).sum(1).mean())
    assert abs(pi - ps) / ps < 0.1, f"isotropic power mismatch {pi} vs {ps}"
    print(f"SMOKE OK: orthogonality {float(dots):.2e}; anchor frozen; MROs step; "
          f"power matched (iso {pi:.4f} vs structured {ps:.4f})")


# ==================================================================== the campaign harness
# (built post-GO, 2026-07-04: runner + manifest-time asserts + shuffle screen +
#  acquisition-aligned machinery + stage-two calibrator + Step-0 re-validation)

def _operating_point() -> dict:
    """The ratified operating point, read from the calibration artifact — never a
    copied literal. Rung fallback (pinned): cal at x2.0 first; no acquisition onset in
    either cal seed => drop to x1.0 and re-cal before any verdict arm."""
    art = json.loads((OUTDIR / "exp10_calibration.json").read_text())
    p = art["proposed"]
    return dict(coeff_std=p["coeff_std"], k_axes=p["k_axes"],
                jiggle_sigma=p["jiggle_sigma"])


def _trace_realized(arm_name: str, seed: int, op: dict, n_steps: int = 200):
    """The REALIZED pairing: run a scratch loop (discarded) for n_steps and trace which
    nuisance coefficients / jiggle residuals actually meet which identity labels."""
    spec = ARMS10[arm_name]
    pin = constants.PinnedConstants()
    cfg = SculptConfig(seed=seed)
    cfg._exp10 = dict(coeff_std=op["coeff_std"], k_axes=op["k_axes"],
                      family=spec.get("family", "structured"),
                      jiggle_sigma=op["jiggle_sigma"])
    loop = spec["loop"](cfg, pin)
    trace = dict(labels=[], coeffs=[], jig_resid=[], jig_tokens=[])
    orig_nuis = loop.stim.nuisance
    def traced_nuis(n_rows):
        n, c = orig_nuis(n_rows)
        trace["coeffs"].append(c.clone())
        return n, c
    loop.stim.nuisance = traced_nuis
    orig_vary = loop._vary_word
    def traced_vary(e_word, tokens):
        out = orig_vary(e_word, tokens)
        trace["jig_resid"].append((out - e_word).clone())
        trace["jig_tokens"].append(tokens.clone())
        return out
    loop._vary_word = traced_vary
    orig_bc = loop.build_cells
    def traced_bc(t, **kw):
        bc = orig_bc(t, **kw)
        win = loop.stream.window(t % (loop.stream.T - cfg.W), cfg.W)
        trace["labels"].append(torch.stack(
            [win["a"].float(), (win["b"] // cfg.n_category).float(),
             (win["b"] % cfg.n_category).float()], dim=1))
        return bc
    loop.build_cells = traced_bc
    for _ in range(n_steps):
        loop.step(no_word=spec.get("no_word", False))
    return trace, loop, cfg


def _max_abs_corr(x, y):
    xc = (x - x.mean(0)) / (x.std(0) + 1e-12)
    yc = (y - y.mean(0)) / (y.std(0) + 1e-12)
    return float((xc.t() @ yc / len(x)).abs().max())


def _shuffle_null_thr(x, y, n_null=500, q=0.99):
    null = []
    for i in range(n_null):
        gp = torch.Generator().manual_seed(12000 + i)
        null.append(_max_abs_corr(x, y[torch.randperm(len(y), generator=gp)]))
    return sorted(null)[int(q * n_null)]


def exp10_manifest_asserts(arm_name: str, seed: int, op: dict) -> dict:
    """The BINDING per-arm manifest-time asserts (prereg SS11 pin 3): (a) realized
    pairing; (b) deployed jiggle residual ⟂ non-token labels; (c) token-centroid-only
    regression check (per-token residual mean ~ 0; residual ⟂ token); (d) per-arm
    sigma* NC re-check on THIS arm's word cortex. HARD-FAILS on breach."""
    trace, loop, cfg = _trace_realized(arm_name, seed, op)
    labels = torch.cat(trace["labels"])                    # (n_rows, 3) a/distractor/category
    out = dict(arm=arm_name, seed=seed, n_rows=int(labels.shape[0]), op=op)
    if trace["coeffs"]:
        coeffs = torch.cat(trace["coeffs"])[: labels.shape[0]]
        obs = _max_abs_corr(coeffs, labels)
        thr = _shuffle_null_thr(coeffs, labels)
        out["realized_pairing"] = dict(obs=round(obs, 4), null99=round(thr, 4),
                                       ok=bool(obs <= thr))
        assert obs <= thr, f"REALIZED-PAIRING LEAK: {obs} > {thr}"
    if trace["jig_resid"]:
        resid = torch.cat(trace["jig_resid"])
        toks = torch.cat(trace["jig_tokens"]).float().unsqueeze(1)
        obs_j = _max_abs_corr(resid, labels[: resid.shape[0]])
        thr_j = _shuffle_null_thr(resid, labels[: resid.shape[0]])
        obs_t = _max_abs_corr(resid, toks)
        thr_t = _shuffle_null_thr(resid, toks)
        per_tok_mean = max(float(resid[(toks.squeeze(1) == v)].mean(0).norm())
                           for v in toks.squeeze(1).unique())
        sig = op["jiggle_sigma"]
        out["jiggle_deployed"] = dict(
            resid_vs_labels=dict(obs=round(obs_j, 4), null99=round(thr_j, 4),
                                 ok=bool(obs_j <= thr_j)),
            resid_vs_token=dict(obs=round(obs_t, 4), null99=round(thr_t, 4),
                                ok=bool(obs_t <= thr_t)),
            centroid_only=dict(max_per_token_mean_norm=round(per_tok_mean, 5),
                               bound=round(3 * sig, 5),
                               ok=bool(per_tok_mean <= 3 * sig)))
        assert obs_j <= thr_j and obs_t <= thr_t, "JIGGLE RESIDUAL LEAK"
        assert per_tok_mean <= 3 * sig, "CENTROID-ONLY BREACH (systematic offset)"
    # (d) per-arm sigma* re-check on THIS arm's word cortex
    emb = loop.word.embed.weight.detach()
    g = torch.Generator().manual_seed(4242 + 100 + seed)
    toks_all = torch.arange(emb.shape[0]).repeat_interleave(66000)
    e = emb[toks_all] + op["jiggle_sigma"] * torch.randn(len(toks_all), cfg.D, generator=g)
    acc = float((torch.cdist(e, emb).argmin(1) == toks_all).float().mean())
    out["sigma_nc_recheck"] = dict(sigma=op["jiggle_sigma"], acc=acc, ok=bool(acc == 1.0))
    assert acc == 1.0, f"SIGMA* NC RE-CHECK FAIL on arm cortex: acc={acc}"
    (OUTDIR / f"{arm_name}_s{seed}.exp10asserts.json").write_text(json.dumps(out, indent=2))
    print(f"MANIFEST ASSERTS PASS [{arm_name} s{seed}]: pairing "
          f"{out.get('realized_pairing', {}).get('obs')} <= "
          f"{out.get('realized_pairing', {}).get('null99')}; NC acc {acc}")
    return out


@torch.no_grad()
def shuffle_read(lp) -> dict:
    """The read-time leakage screen on a NUISANCE-RIDING read (pin 4, sharpened):
    occupancy-style tracks computed on nuisance-carrying raws, true vs row-permuted
    nuisance. RNG-isolated (probe-local keys; the real counter untouched)."""
    if not isinstance(lp.stim, NuisanceStimulus) or lp.stim.coeff_std == 0.0:
        return {}
    st = X9._rng_guard(lp)
    cfg = lp.cfg
    g = torch.Generator().manual_seed(lp._t * 13 + 5)
    K = 256
    a = torch.randint(0, cfg.n_A, (K,), generator=g)
    b = torch.randint(0, cfg.n_B, (K,), generator=g)
    base = lp.stim.centre[a, b] + cfg.sigma_stim * torch.randn(K, cfg.D, generator=g)
    gg = torch.Generator().manual_seed(lp._t * 17 + 7)
    if lp.stim.family == "isotropic":
        nuis = lp.stim.sigma_iso * torch.randn(K, cfg.D, generator=gg)
    else:
        nuis = (lp.stim.coeff_std * torch.randn(K, lp.stim.k_axes, generator=gg)) @ lp.stim.axes
    perm = torch.randperm(K, generator=gg)

    def cat_track(raws):
        e = lp.vision.emit(raws)
        c_sup = b % cfg.n_category
        cen = torch.stack([e[c_sup == k2].mean(0) for k2 in range(cfg.n_category)])
        return float((torch.cdist(e, cen).argmin(1) == c_sup).float().mean())

    true_t = cat_track(base + nuis)
    shuf_t = cat_track(base + nuis[perm])
    X9._rng_check(lp, st, "shuffle_read")
    return dict(shufscreen_true=round(true_t, 4), shufscreen_perm=round(shuf_t, 4),
                shufscreen_delta=round(true_t - shuf_t, 4))


def probes10(no_word: bool):
    base = X9.probes_for(no_word)
    def fn(lp):
        out = base(lp)
        if lp._t % A.BLOCK == 0:
            out.update(shuffle_read(lp))
        return out
    return fn


def acquisition_onset(cols, floor=0.01, consec=2):
    """Pin 5 fire rule (pinned form): first t with num >= floor in >= consec
    consecutive eval windows; None = never crossed."""
    run = 0
    for c in cols:
        run = run + 1 if c["num"] >= floor else 0
        if run >= consec:
            return c["t"] - (consec - 1) * EVAL
    return None


def acquisition_aligned_read(cols, onset, k=7):
    """The matched-bar idiom: k-window means starting at the arm's OWN onset."""
    if onset is None:
        return None
    win = [c for c in cols if c["t"] >= onset][:k]
    if len(win) < k:
        return dict(k=len(win), censored=True)
    return dict(k=k, censored=False,
                num_mean=round(statistics.mean(c["num"] for c in win), 4),
                den_mean=round(statistics.mean(c["den"] for c in win), 4),
                asg_mean=round(statistics.mean(c["asg_dist"] for c in win), 4))


def run_exp10_arm(arm_name: str, seed: int, steps_override: int | None = None,
                  coeff_override: float | None = None):
    """The runner: manifest asserts (hard gate) -> the shared A.run_arm code path with
    exp10 spec injection + the EXP09 probe set + the shuffle screen. Verdict arms are
    NOT scored at run time (stage-two constants; one review)."""
    op = _operating_point()
    if coeff_override is not None:
        op = dict(op, coeff_std=coeff_override)
    spec10 = ARMS10[arm_name]
    exp10_manifest_asserts(arm_name, seed, op)
    A.ARMS[arm_name] = dict(loop=spec10["loop"], no_word=spec10.get("no_word", False),
                            steps=steps_override or spec10["steps"], seeds=spec10["seeds"],
                            exp10=dict(coeff_std=op["coeff_std"], k_axes=op["k_axes"],
                                       family=spec10.get("family", "structured"),
                                       jiggle_sigma=op["jiggle_sigma"]))
    rec = A.run_arm(arm_name, seed, steps_override=steps_override,
                    probes=probes10(spec10.get("no_word", False)))
    onset = acquisition_onset(rec["columns"])
    rec["acquisition_onset"] = onset
    rec["acquisition_aligned"] = acquisition_aligned_read(rec["columns"], onset)
    rec["exp10_op"] = op
    (OUTDIR / f"{arm_name}_s{seed}.json").write_text(json.dumps(rec, indent=2))
    print(f"{arm_name} s{seed}: onset={onset} aligned={rec['acquisition_aligned']}")
    return rec


def stage_two():
    """In-regime verdict constants from the CAL arm's own healthy spans (never verdict
    seeds; the SS5 calibration RULE re-applied in-regime) + the RUNG-FALLBACK CHECK."""
    recs = [json.loads((OUTDIR / f"nodetach_varied_cal_s{s}.json").read_text())
            for s in CAL_SEEDS]
    onsets = [r.get("acquisition_onset") for r in recs]
    fallback = all(o is None for o in onsets)
    out = dict(cal_seeds=CAL_SEEDS, acquisition_onsets=onsets,
               rung_fallback_fired=bool(fallback))
    if fallback:
        out["action"] = "DROP TO x1.0 AND RE-CAL before any verdict arm (pinned guard)"
        (OUTDIR / "exp10_stage2_constants.json").write_text(json.dumps(out, indent=2))
        print("RUNG FALLBACK FIRED:", json.dumps(out))
        return out
    # in-regime constants from the cal columns (healthy span = post-ramp, whole run if
    # no collapse): period (healthy-segment estimator, substitution gated), flicker
    # envelope -> k_min / run_max; den floor behavior -> den criterion form
    per_seed = []
    for r in recs:
        cols = r["columns"]
        v2p = X9._healthy_segment_period(cols, X9.PERIOD_WORD)
        any_q = any(c["asg_argmax_k"] == 1 and c["den"] < X9.FLOOR for c in cols)
        period = v2p["used"] if (v2p["substituted"] and any_q) else (
            v2p["measured"] if False else X9.PERIOD_WORD if not any_q else v2p["used"])
        H = [c for c in cols if c["t"] >= 20100]
        n_win = max(1, (2 * period) // EVAL)
        worst_k, worst_run, worst_den = 1.0, 0, 1.0
        for s0 in range(0, len(H) - n_win + 1):
            seg = H[s0:s0 + n_win]
            kf = sum(1 for c in seg if c["asg_argmax_k"] > 1) / n_win
            df = sum(1 for c in seg if c["den"] >= X9.FLOOR) / n_win
            run = best = 0
            for c in seg:
                run = run + 1 if c["asg_argmax_k"] == 1 else 0
                best = max(best, run)
            worst_k, worst_den, worst_run = min(worst_k, kf), min(worst_den, df), max(worst_run, best)
        per_seed.append(dict(seed=r["seed"], period_res=v2p, period_used_for_cal=period,
                             n_win=n_win, worst_k_frac=round(worst_k, 4),
                             worst_den_frac=round(worst_den, 4), max_k1_run=worst_run))
    k_min_frac = min(p["worst_k_frac"] for p in per_seed)
    den_frac = min(p["worst_den_frac"] for p in per_seed)
    run_max = max(p["max_k1_run"] for p in per_seed)
    out["per_seed"] = per_seed
    out["constants"] = dict(
        period=X9.PERIOD_WORD if all(not p["period_res"]["substituted"] for p in per_seed)
        else max(p["period_used_for_cal"] for p in per_seed),
        pass_k_frac=k_min_frac, pass_den_frac=den_frac, pass_run_max=max(run_max, 1),
        note="calibration RULE: every cal healthy placement passes; terminal signature "
             "(k>1 frac 0, den frac 0, run=n_win) excluded by construction")
    (OUTDIR / "exp10_stage2_constants.json").write_text(json.dumps(out, indent=2))
    print("STAGE TWO:", json.dumps(out["constants"]))
    return out


def step0_revalidate():
    """Step-0 (a)/(c) under variation at the operating point (30k, 3 seeds, intact +
    no-word varied loops; the committed WINDOWED read forms verbatim: (a) = mean
    post-onset block reads, distractor floor 0.60; (c) = associative evocation
    divergence with the channel-alive precondition -> DEFERRED, never a false pass)."""
    op = _operating_point()
    res = dict(op=op, a=[], c=[])
    for seed in range(3):
        pin = constants.PinnedConstants()
        cfg = SculptConfig(seed=seed)
        cfg._exp10 = dict(coeff_std=op["coeff_std"], k_axes=op["k_axes"],
                          family="structured", jiggle_sigma=op["jiggle_sigma"])
        intact = VariedWordLoop(cfg, pin)
        cfg2 = SculptConfig(seed=seed)
        cfg2._exp10 = dict(cfg._exp10)
        noword = VariedWordLoop(cfg2, pin)
        blocks_i, blocks_n = [], []
        for t in range(1, 30001):
            intact.step(no_word=False)
            noword.step(no_word=True)
            if t % A.BLOCK == 0 and t > cfg.t2:
                blocks_i.append(intact.dc_track(cfg.n_eval))
                blocks_n.append(noword.dc_track(cfg.n_eval))
        a_i = statistics.mean(b["distractor_track"] for b in blocks_i)
        a_n = statistics.mean(b["distractor_track"] for b in blocks_n)
        res["a"].append(dict(seed=seed, intact_dist=round(a_i, 4),
                             noword_dist=round(a_n, 4), floor=0.60,
                             ok=bool(a_i >= 0.60)))
        ma, mb = X9._member_set(cfg)
        e = intact.evoke_vision(ma, mb, associative=True)
        cat = mb % cfg.n_category
        cen = torch.stack([e[cat == k2].mean(0) for k2 in range(cfg.n_category)])
        cat_div = float(torch.cdist(cen, cen)[0, 1])
        d_sup = mb // cfg.n_category
        cend = torch.stack([e[d_sup == k2].mean(0) for k2 in range(cfg.n_distractor)])
        dist_div = float(torch.cdist(cend, cend)[0, 1])
        alive = (cat_div + dist_div) > 1e-3
        res["c"].append(dict(seed=seed, cat_div=round(cat_div, 4),
                             dist_div=round(dist_div, 4),
                             status=("share %.3f" % (cat_div / max(cat_div + dist_div, 1e-9))
                                     if alive else "DEFERRED_DEAD_CHANNEL")))
    res["a_pass"] = all(x["ok"] for x in res["a"])
    (OUTDIR / "exp10_step0_revalidation.json").write_text(json.dumps(res, indent=2))
    print("STEP0 (a):", res["a"], "\nSTEP0 (c):", res["c"])
    return res


def _main10():
    ap = argparse.ArgumentParser()
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--parity", action="store_true")
    ap.add_argument("--calibrate", action="store_true")
    ap.add_argument("--rescore", action="store_true")
    ap.add_argument("--run", nargs=2, metavar=("ARM", "SEED"))
    ap.add_argument("--coeff", type=float, default=None)
    ap.add_argument("--steps", type=int, default=None)
    ap.add_argument("--stage2", action="store_true")
    ap.add_argument("--step0", action="store_true")
    args = ap.parse_args()
    torch.set_num_threads(1)                               # the determinism contract
    if args.smoke:
        smoke()
    if args.parity:
        parity_gate()
    if args.calibrate:
        out = dict(jiggle=calibrate_jiggle(), rungs=calibrate_nuisance_rungs())
        rung = next((r for r in reversed(out["rungs"]) if r["clears"]), out["rungs"][0])
        out["independence"] = independence_asserts(rung["coeff_std"],
                                                   out["jiggle"]["sigma_star"])
        out["proposed"] = dict(k_axes=K_AXES, coeff_std=rung["coeff_std"],
                               rung_mult=rung["mult"],
                               jiggle_sigma=out["jiggle"]["sigma_star"],
                               cal_seeds=CAL_SEEDS, verdict_seeds=VERDICT_SEEDS,
                               horizons=dict(nodetach=HORIZON_NODETACH, ref=HORIZON_REF))
        out["stage_one_provenance"] = dict(
            jiggle_seeds=VERDICT_SEEDS + CAL_SEEDS, oracle_seeds=[0, 1, 2],
            nuis_seed_base=NUIS_SEED_BASE,
            note="stage-one calibrations run on synthetic/oracle draws (jiggle now "
                 "cross-seed incl. cal seeds); the {10,11} dedication is for STAGE-TWO "
                 "in-regime verdict constants")
        (OUTDIR / "exp10_calibration.json").write_text(json.dumps(out, indent=2))
        print("PROPOSED:", json.dumps(out["proposed"]))
    if args.rescore:
        table = rescore_static()
        (OUTDIR / "exp10_static_rescore.json").write_text(json.dumps(table, indent=2))
    if args.run:
        run_exp10_arm(args.run[0], int(args.run[1]), steps_override=args.steps,
                      coeff_override=args.coeff)
    elif args.stage2:
        stage_two()
    elif args.step0:
        step0_revalidate()


if __name__ == "__main__":
    _main10()
