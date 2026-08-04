"""EXP21 — external held-out visual instrument (prereg §3; docs/EXP21_PAM_TEACHING_CONTRAST_PREREG.md,
Touch-1 ratified 2026-08-04, baseline commit 19a8fbf).

Dedicated primary/shadow probe banks + the head-free nearest-centroid scorer + the G3a audit.

INSTRUMENT PRINCIPLE (§3.1): the probe measures ONLY the visual cortex. It never invokes PAM, the
word cortex, the association output, or any learned head; it never contributes a gradient; it never
changes any model, optimizer, generator, counter, or fabric field. The live training stimulus is
NEVER called: `EXP12Stimulus.raw()` advances a mutable per-object counter (exp12_fabric.py:155-165),
so a read-time call would shift every later spread-loss sample and change training — the G0 red
fixture `live_stim_probe_call` proves the parity gate sees exactly that.

BANKS (§3.2): per training seed, before wave zero — dedicated probe-only EXP12Stimulus objects with
the SAME member geometry, renderer, fixed background (SEED_BG_CONST pin-to-constant) and
seed-specific world orientation (ConflictStimulus Q is seeded by cfg.seed) as the training world, on
experiment-owned collision-audited substreams (audit computed below, recorded in every manifest).
One PRIMARY bank shared byte-for-byte by the paired ON/OFF runs; one independent SHADOW bank for
calibration/repeatability only (never enters verdict scoring). 32 support + 128 eval per each of the
16 members; balanced; support/eval disjoint by generator construction and verified by tensor
identity; tensors + labels + generator keys + SHA-256 digests stored before training.

SUBSTREAM KEYS (the SEED_SWEEP/SEED_UBUF audit precedent, big-modulus family):
  primary stim probe_seed = 210000 + seed  ->  raw() substream keys (210000+seed)*1_000_003 + calls
  shadow  stim probe_seed = 310000 + seed  ->  raw() substream keys (310000+seed)*1_000_003 + calls
  stimulus-noise generators: (probe_seed)*1_000_003 + {500_000_011 support, 500_000_017 eval}
All keys are >= 2.1e11. Audited disjoint (collision_audit below) from: the assert-null lattices
61000-64199; the fabric substream keys 91000-99047 (+ conditional 100000-100025 sweep,
101000-101025 ubuf); loop-side cfg.seed+{0,1,2,3,99}; the eval-time ephemeral lattices
{7t+1, 13t+5, 17t+9 : t <= 1e6} (max < 1.71e7); and the LIVE stimulus raw() substream family
(probe_seed 99000+seed -> keys ~9.9e10 + calls, bounded < 1e11 for calls < 1e9).
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))
sys.path.insert(0, str(_HERE.parents[1] / "src"))

import exp09_arms as X9                                        # noqa: E402  (_rng_guard/_rng_check)
import exp12_fabric as F                                       # noqa: E402
from sculpt_config import SculptConfig                         # noqa: E402

OUTDIR21 = _HERE / "exp08" / "exp21"

# --- bank law (§3.2; preregistration choices, never transported) ---
N_SUPPORT = 32                     # per member
N_EVALB = 128                      # per member
N_MEMBERS = 16
SEED21_PRIMARY = 210000            # probe-only stimulus probe_seed base (primary)
SEED21_SHADOW = 310000             # probe-only stimulus probe_seed base (shadow)
NOISE_OFF_SUPPORT = 500_000_011    # stimulus-noise generator key offsets (on probe_seed*1_000_003)
NOISE_OFF_EVAL = 500_000_017

AXES = ("category", "distractor", "coarse_a", "member")        # §3.4; category is PRIMARY
AXIS_CLASSES = dict(category=2, distractor=2, coarse_a=4, member=16)


def axis_labels(member: torch.Tensor, cfg) -> dict:
    """§3.4 axis label maps, DERIVED from the member index (provenance computed, not asserted):
    member = a * n_B + b; category = b % n_category; distractor = b // n_category; coarse_a = a."""
    a, b = member // cfg.n_B, member % cfg.n_B
    return dict(category=b % cfg.n_category, distractor=b // cfg.n_category,
                coarse_a=a, member=member)


def collision_audit(keys: list[int]) -> dict:
    """Assert the probe substream keys are disjoint from every live generator-key family
    (module docstring). Computed, never asserted-by-comment; recorded in each bank manifest."""
    lo, hi = min(keys), max(keys)
    fams = dict(
        assert_null=(61000, 64199),
        fabric=(91000, 99047),
        sweep=(100000, 100025),
        ubuf=(101000, 101025),
        loop_side=(0, 200),                                   # cfg.seed+{0..3,99} for seeds < 100
        eval_ephemeral=(1, 17 * 1_000_000 + 9),               # {7t+1,13t+5,17t+9 : t <= 1e6}
        live_raw_substream=(99000 * 1_000_003,                # probe_seed 99000+seed, seed <= 47
                            99047 * 1_000_003 + 1_000_000_000),
    )
    out = {}
    for name, (flo, fhi) in fams.items():
        clash = not (hi < flo or lo > fhi)
        out[name] = dict(range=[flo, fhi], clash=bool(clash))
        assert not clash, f"probe substream keys [{lo},{hi}] collide with {name} [{flo},{fhi}]"
    return dict(key_range=[lo, hi], families=out, ok=True)


def _bank_stim(seed: int, kind: str) -> F.EXP12Stimulus:
    """Probe-only stimulus: SAME world (geometry/orientation/background) as the training arm at
    this seed — identical constructor args incl. cfg.seed — but its OWN probe_seed substream.
    A separate object: the live training stimulus and its counter are never touched."""
    assert kind in ("primary", "shadow")
    cfg = SculptConfig(seed=seed)
    fam = F.family()
    base = (SEED21_PRIMARY if kind == "primary" else SEED21_SHADOW) + seed
    stim = F.EXP12Stimulus(
        cfg.D, cfg.n_A, cfg.n_distractor, cfg.n_category,
        R_coarse=cfg.R_coarse, r_distractor=cfg.r_distractor,
        r_category=cfg.r_category, sigma=cfg.sigma_stim, seed=cfg.seed,
        coeff_std=fam["coeff_std"], probe_seed=base)
    return stim


def _bank_members(n_per: int, cfg) -> tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
    m = torch.arange(N_MEMBERS).repeat_interleave(n_per)       # member-major, balanced
    return m // cfg.n_B, m % cfg.n_B, m


def bank_digest(bank: dict) -> str:
    """Canonical SHA-256 over the tensor bytes in fixed order + the meta json."""
    h = hashlib.sha256()
    for k in ("support", "eval", "sup_member", "ev_member"):
        h.update(bank[k].numpy().tobytes())
    h.update(json.dumps(bank["meta"], sort_keys=True).encode())
    return h.hexdigest()


def build_bank(seed: int, kind: str) -> dict:
    """§3.2 bank construction — deterministic, before wave zero, live state untouched."""
    cfg = SculptConfig(seed=seed)
    stim = _bank_stim(seed, kind)
    base = stim.probe_seed
    keys = dict(
        raw_substream_support=base * 1_000_003 + 0,            # stim._calls == 0 at 1st raw()
        raw_substream_eval=base * 1_000_003 + 1,               # _calls == 1 at 2nd raw()
        noise_support=base * 1_000_003 + NOISE_OFF_SUPPORT,
        noise_eval=base * 1_000_003 + NOISE_OFF_EVAL)
    audit = collision_audit(list(keys.values()))
    a_s, b_s, m_s = _bank_members(N_SUPPORT, cfg)
    a_e, b_e, m_e = _bank_members(N_EVALB, cfg)
    assert stim._calls == 0, "probe stimulus counter must start at 0 (fresh object)"
    g_s = torch.Generator().manual_seed(keys["noise_support"])
    support = stim.raw(a_s, b_s, g_s)                          # _calls 0 -> 1
    g_e = torch.Generator().manual_seed(keys["noise_eval"])
    ev = stim.raw(a_e, b_e, g_e)                               # _calls 1 -> 2
    assert stim._calls == 2
    # disjointness by construction (distinct counter keys + distinct noise gens), verified:
    dmin = float(torch.cdist(support, ev).min())
    assert dmin > 0.0, "support/eval tensor identity overlap"
    meta = dict(exp="exp21", kind=kind, seed=seed, probe_seed=base,
                n_support=N_SUPPORT, n_eval=N_EVALB, n_members=N_MEMBERS,
                D=cfg.D, generator_keys=keys, collision_audit=audit,
                min_support_eval_dist=round(dmin, 6),
                construction="EXP12Stimulus.raw() on a probe-only object; member-major balanced; "
                             "support then eval (counter keys 0,1); world = training seed's")
    return dict(support=support, eval=ev, sup_member=m_s, ev_member=m_e, meta=meta)


def bank_paths(seed: int, kind: str) -> tuple[Path, Path]:
    b = OUTDIR21 / f"exp21_bank_{kind}_s{seed}"
    return b.with_suffix(".pt"), b.with_suffix(".manifest.json")


def write_bank(seed: int, kind: str) -> dict:
    """Build + store (append-only: an existing committed bank is never regenerated over)."""
    OUTDIR21.mkdir(parents=True, exist_ok=True)
    pt, mf = bank_paths(seed, kind)
    bank = build_bank(seed, kind)
    dig = bank_digest(bank)
    if pt.exists():
        old = load_bank(seed, kind)
        assert bank_digest(old) == dig, \
            f"EXISTING bank {pt.name} differs from deterministic rebuild — append-only violation"
        return old
    torch.save(bank, pt)
    mf.write_text(json.dumps(dict(bank=bank["meta"], sha256=dig), indent=2))
    return bank


def check_bank_hash(bank: dict, expected_sha: str, name: str = "bank"):
    """The deployed hash-drift law (exercised by the bank_hash_mismatch fixture)."""
    got = bank_digest(bank)
    assert got == expected_sha, \
        f"{name} hash drift vs manifest: {got[:12]} != {expected_sha[:12]}"


def load_bank(seed: int, kind: str):
    pt, mf = bank_paths(seed, kind)
    bank = torch.load(pt, weights_only=False)
    man = json.loads(mf.read_text())
    check_bank_hash(bank, man["sha256"], pt.name)
    return bank


def assert_bank_binding(seed: int, payload_sha: str):
    """A run's probe payload must carry the seed's CANONICAL primary-bank hash (the
    deployed bank-swap law: scoring against any other bank is a HALT)."""
    _, mf = bank_paths(seed, "primary")
    man = json.loads(mf.read_text())
    assert payload_sha == man["sha256"], \
        (f"probe payload bank {payload_sha[:12]} is NOT seed {seed}'s canonical primary "
         f"bank {man['sha256'][:12]} — bank swap, HALT")


def audit_bank(bank: dict, cfg, stim=None) -> dict:
    """The deployed STRUCTURAL bank law (§3.2/§3.4), taking the bank OBJECT so the observed-
    red fixtures exercise THIS code on planted broken banks (the panel's inline-copy
    finding). Axis mappings are cross-checked against the DEPLOYED stimulus definitions
    (conflict_stream category_of/distractor_of), not a re-typed formula."""
    sup_lab = axis_labels(bank["sup_member"], cfg)
    ev_lab = axis_labels(bank["ev_member"], cfg)
    checks = {}
    for q in AXES:
        kcl = AXIS_CLASSES[q]
        s_counts = [int((sup_lab[q] == c).sum()) for c in range(kcl)]
        e_counts = [int((ev_lab[q] == c).sum()) for c in range(kcl)]
        assert min(s_counts) > 0, f"empty support class on axis {q}: {s_counts}"
        assert len(set(s_counts)) == 1 and len(set(e_counts)) == 1, \
            f"axis {q} imbalance: support {s_counts} eval {e_counts}"
        checks[q] = dict(support_per_class=s_counts[0], eval_per_class=e_counts[0])
    assert bank["support"].shape == (N_MEMBERS * N_SUPPORT, cfg.D), "support shape wrong"
    assert bank["eval"].shape == (N_MEMBERS * N_EVALB, cfg.D), "eval shape wrong"
    dmin = float(torch.cdist(bank["support"], bank["eval"]).min())
    assert dmin > 0.0, "support/eval tensor identity overlap"
    m = bank["ev_member"]
    b = m % cfg.n_B
    if stim is None:
        stim = _bank_stim(int(bank["meta"]["seed"]), bank["meta"]["kind"])
    assert torch.equal(ev_lab["category"], stim.category_of(b)), \
        "category axis map != deployed stimulus category_of"
    assert torch.equal(ev_lab["distractor"], stim.distractor_of(b)), \
        "distractor axis map != deployed stimulus distractor_of"
    assert torch.equal(ev_lab["coarse_a"], m // cfg.n_B), "coarse_a axis map wrong"
    return checks


# ------------------------------------------------------------------ head-free scorer (§3.4)
def _balanced_acc(pred: torch.Tensor, lab: torch.Tensor, n_classes: int) -> float:
    return float(sum((pred[lab == c] == c).float().mean() for c in range(n_classes)) / n_classes)


def score_state(vision, bank: dict, cfg) -> dict:
    """Score ONE model state on ONE bank through `vision.emit` only (§3.4). Returns per-axis
    balanced accuracy + margin, geometry companions, and the per-sample CATEGORY predictions
    (int8) for the offline null machinery. Caller guards inertness (probe_read)."""
    with torch.inference_mode():
        e_sup = vision.emit(bank["support"])
        e_ev = vision.emit(bank["eval"])
        sup_lab = axis_labels(bank["sup_member"], cfg)
        ev_lab = axis_labels(bank["ev_member"], cfg)
        out = dict(axes={}, geom={})
        cat_pred = None
        for q in AXES:
            k = AXIS_CLASSES[q]
            cents = torch.stack([e_sup[sup_lab[q] == c].mean(0) for c in range(k)])
            pred = torch.cdist(e_ev, cents).argmin(1)
            bacc = _balanced_acc(pred, ev_lab[q], k)
            out["axes"][q] = dict(bacc=round(bacc, 6), margin=round(bacc - 1.0 / k, 6),
                                  chance=1.0 / k)
            if q == "category":
                cat_pred = pred.to(torch.int8)
        # geometry companions (§3.4; descriptive, never standalone proof)
        ec = e_ev - e_ev.mean(0)
        cov = (ec.t() @ ec) / (ec.shape[0] - 1)
        ev_ = torch.linalg.eigvalsh(cov).clamp_min(0)
        tr = float(ev_.sum())
        pr = float(ev_.sum() ** 2 / (ev_.pow(2).sum() + 1e-30))
        dm = torch.cdist(e_ev, e_ev)
        cl = ev_lab["category"]
        same = cl.unsqueeze(0) == cl.unsqueeze(1)
        off = ~torch.eye(len(cl), dtype=torch.bool)
        cat_cents = torch.stack([e_ev[cl == c].mean(0) for c in range(2)])
        mem_spread = float(torch.stack(
            [(e_ev[ev_lab["member"] == m] - e_ev[ev_lab["member"] == m].mean(0)).norm(dim=1).mean()
             for m in range(N_MEMBERS)]).mean())
        mcents = torch.stack([e_ev[ev_lab["member"] == m].mean(0) for m in range(N_MEMBERS)])
        moff = ~torch.eye(N_MEMBERS, dtype=torch.bool)
        out["geom"] = dict(
            cov_trace=round(tr, 6), participation_ratio=round(pr, 6),
            within_cat_dist=round(float(dm[same & off].mean()), 6),
            between_cat_dist=round(float(dm[(~same) & off].mean()), 6),
            cat_centroid_dist=round(float((cat_cents[0] - cat_cents[1]).norm()), 6),
            within_member_spread=round(mem_spread, 6),
            member_centroid_dist_mean=round(float(torch.cdist(mcents, mcents)[moff].mean()), 6))
    return out, cat_pred


def probe_read(loop, bank: dict) -> tuple[dict, torch.Tensor]:
    """One trajectory-inert read (§3.5): vision only, zero RNG, zero live-state mutation,
    ZERO PAM/word invocations — every clause guarded at run time, not asserted-by-design
    (the pam_called_by_probe / live_counter_changed fixtures fire THESE guards)."""
    st = X9._rng_guard(loop)
    calls0, t0 = loop.stim._calls, loop._t
    n_calls = dict(op=0, word=0)
    orig_op, orig_we = loop.op.forward, loop.word.emit
    loop.op.forward = lambda *a, **k: (n_calls.__setitem__("op", n_calls["op"] + 1),
                                       orig_op(*a, **k))[1]
    loop.word.emit = lambda *a, **k: (n_calls.__setitem__("word", n_calls["word"] + 1),
                                      orig_we(*a, **k))[1]
    try:
        out, cat_pred = score_state(loop.vision, bank, loop.cfg)
    finally:
        del loop.op.forward
        loop.word.emit = orig_we
    assert n_calls["op"] == 0, f"probe invoked PAM {n_calls['op']}x — forbidden (§3.1)"
    assert n_calls["word"] == 0, f"probe invoked the word cortex {n_calls['word']}x (§3.1)"
    X9._rng_check(loop, st, "exp21_probe_read")
    assert loop.stim._calls == calls0, "probe advanced the LIVE stimulus counter"
    assert loop._t == t0, "probe advanced the wave counter"
    return out, cat_pred


class ProbeSession:
    """Accumulates the planned reads of one run (per bank). The runner owns the cadence
    (t=0, every 3000, exactly read_at — prereg §3.3); this object only accumulates + writes."""

    def __init__(self, banks: dict):
        self.banks = banks                                     # name -> bank dict
        self.ts: list[int] = []
        self.summ = {k: [] for k in banks}
        self.pred = {k: [] for k in banks}

    def read(self, loop, t: int):
        self.ts.append(int(t))
        for name, bank in self.banks.items():
            out, cat_pred = probe_read(loop, bank)
            self.summ[name].append(out)
            self.pred[name].append(cat_pred)

    def write(self, base: Path) -> dict:
        files = {}
        for name in self.banks:
            pt = Path(str(base) + f".probe_{name}.pt")
            js = Path(str(base) + f".probe_{name}.json")
            assert not pt.exists() and not js.exists(), f"probe artifact overwrite: {pt.name}"
            preds = torch.stack(self.pred[name])               # (n_reads, 2048) int8
            payload = dict(ts=self.ts, predictions=preds,
                           bank_sha256=bank_digest(self.banks[name]),
                           ev_member=self.banks[name]["ev_member"])
            torch.save(payload, pt)
            js.write_text(json.dumps(dict(
                ts=self.ts, bank_sha256=payload["bank_sha256"],
                reads=self.summ[name],
                predictions_sha256=hashlib.sha256(preds.numpy().tobytes()).hexdigest()),
                indent=2))
            files[name] = dict(pt=pt.name, json=js.name)
        return files


# ------------------------------------------------------------------ G3a — probe audit (§7)
def _audit_one_bank(seed: int, kind: str) -> dict:
    bank = write_bank(seed, kind)
    cfg = SculptConfig(seed=seed)
    checks = audit_bank(bank, cfg)                             # the DEPLOYED structural law
    _, mf = bank_paths(seed, kind)
    check_bank_hash(bank, json.loads(mf.read_text())["sha256"], mf.name)
    dig = bank_digest(bank)
    rebuilt = build_bank(seed, kind)
    assert bank_digest(rebuilt) == dig, "bank rebuild differs — construction not deterministic"
    return dict(seed=seed, kind=kind, sha256=dig, checks=checks,
                collision_audit=bank["meta"]["collision_audit"]["ok"])


def _broken_copy(bank: dict) -> dict:
    return {k: (v.clone() if torch.is_tensor(v) else dict(v)) for k, v in bank.items()}


def _observed_red_fixtures() -> dict:
    """Every named G3a fixture fails FIRST under its deliberately broken condition (§7 row
    G3a) — each drives the DEPLOYED law (audit_bank / check_bank_hash / probe_read's own
    guards), never an inline restatement. Broken objects are synthetic locals; nothing
    broken is stored."""
    import exp21_teaching as T21
    reds = {}

    def expect_red(name, fn):
        try:
            fn()
        except AssertionError as e:
            reds[name] = dict(red=True, message=str(e)[:300])
            return
        raise SystemExit(f"G3a fixture {name}: expected red, saw green — dead gate, HALT")

    bank = build_bank(0, "primary")
    cfg = SculptConfig(seed=0)
    stim0 = _bank_stim(0, "primary")
    audit_bank(bank, cfg, stim0)                               # the real bank passes first

    def support_overlap():
        b = _broken_copy(bank)
        b["eval"][0] = b["support"][0]                          # plant an identical row
        audit_bank(b, cfg, stim0)
    expect_red("support_overlap", support_overlap)

    def empty_class():
        b = _broken_copy(bank)
        b["sup_member"][b["sup_member"] % cfg.n_B % cfg.n_category == 1] = 0   # empty cat 1
        audit_bank(b, cfg, stim0)
    expect_red("empty_class", empty_class)

    def label_imbalance():
        b = _broken_copy(bank)
        b["ev_member"][-64:] = 0                                # tilt the balance (m15 -> m0)
        audit_bank(b, cfg, stim0)
    expect_red("label_imbalance", label_imbalance)

    def bank_hash_mismatch():
        b = _broken_copy(bank)
        b["eval"][0, 0] += 1e-3                                 # perturb a stored tensor
        check_bank_hash(b, bank_digest(bank), "planted")        # the DEPLOYED hash law
    expect_red("bank_hash_mismatch", bank_hash_mismatch)

    # live-loop fixtures: broken probes caught by probe_read's DEPLOYED guards
    loop, _, _ = T21.build_exp21("on", 0, steps=64)

    def pam_called_by_probe():
        real = globals()["score_state"]

        def broken_score_state(vision, b, c):                   # a probe that consults PAM
            loop.op(torch.zeros(1, loop.cfg.n_slots, loop.cfg.D).reshape(1, -1, loop.cfg.D),
                    loop.slot_ids, torch.ones(loop.cfg.n_slots, dtype=torch.bool))
            return real(vision, b, c)
        globals()["score_state"] = broken_score_state
        try:
            probe_read(loop, bank)                              # ITS guard must fire
        finally:
            globals()["score_state"] = real
    expect_red("pam_called_by_probe", pam_called_by_probe)

    def live_counter_changed():
        real = globals()["score_state"]

        def broken_score_state(vision, b, c):                   # a probe touching live stim
            loop.stim.raw(torch.tensor([0]), torch.tensor([0]),
                          torch.Generator().manual_seed(0))
            return real(vision, b, c)
        globals()["score_state"] = broken_score_state
        calls0 = loop.stim._calls
        try:
            probe_read(loop, bank)                              # ITS guard must fire
        finally:
            globals()["score_state"] = real
            loop.stim._calls = calls0                           # restore exactly
    expect_red("live_counter_changed", live_counter_changed)

    # restoration proof: the REAL probe on the same live loop leaves every guard green
    st = X9._rng_guard(loop)
    calls0, t0 = loop.stim._calls, loop._t
    probe_read(loop, bank)
    X9._rng_check(loop, st, "g3a_restore")
    assert loop.stim._calls == calls0 and loop._t == t0
    reds["restore_green"] = dict(real_probe_guards="all green after plant removal")
    return reds


def g3_probe_audit(cal_seeds, verdict_seeds) -> dict:
    """G3a executor (§7). Builds + audits every bank; observed-red fixtures FIRST; proves live
    inertness, PAM/word non-invocation, and repeatability machinery on the real path."""
    torch.set_num_threads(1)
    OUTDIR21.mkdir(parents=True, exist_ok=True)
    reds = _observed_red_fixtures()
    banks = []
    for s in sorted(set(cal_seeds) | set(verdict_seeds)):
        banks.append(_audit_one_bank(s, "primary"))
    for s in cal_seeds:
        banks.append(_audit_one_bank(s, "shadow"))
    # primary/shadow independence + repeatability machinery executable on a real state
    import exp21_teaching as T21
    loop, _, _ = T21.build_exp21("on", cal_seeds[0], steps=64)
    p = load_bank(cal_seeds[0], "primary")
    sh = load_bank(cal_seeds[0], "shadow")
    assert bank_digest(p) != bank_digest(sh), "primary and shadow banks identical"
    (op_, _), (os_, _) = probe_read(loop, p), probe_read(loop, sh)
    rep = dict(point_cat_diff=round(abs(op_["axes"]["category"]["bacc"]
                                        - os_["axes"]["category"]["bacc"]), 6),
               machinery="executable")
    out = dict(gate="G3a", executor="exp21_probe.g3_probe_audit",
               observed_red=reds, banks=banks, repeatability=rep,
               law=dict(n_support=N_SUPPORT, n_eval=N_EVALB, axes=list(AXES),
                        primary_base=SEED21_PRIMARY, shadow_base=SEED21_SHADOW))
    T21.write_gate_artifact(OUTDIR21 / "exp21_probe_audit.json", out)
    print(f"G3a probe audit: {len(banks)} banks OK; reds={list(reds)}")
    return out


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--audit", action="store_true")
    args = ap.parse_args()
    torch.set_num_threads(1)
    if args.audit:
        import exp21_teaching as T21
        g3_probe_audit(T21.CAL_SEEDS21, T21.VERDICT_SEEDS21)
