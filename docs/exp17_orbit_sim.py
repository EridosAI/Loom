# EXP17 orbital-anchor feasibility sim (design-seat verification; rides the ratification commit).
# NOT canon — the real generator at G2 decides. Constants derived exactly as exp12_fabric.py.
#
# v2 (panel fix): tremble baselines are COMPUTED in-sim, never hardcoded — v1 carried TRB=0.096
# from the design-relay sketch; the self-consistent value is ~0.0902 (both committed companion
# sims agree at v=0), a fact-check near-miss caught by the orbit panel. Floors are contrast-form
# of the MEASURED baseline; the literals below are sim expectations only.
import numpy as np

THETA = 0.25                       # = 1/TAU, exp12_fabric.py:71-72 (pinned from code)
SIG = 0.5                          # family coeff_std (exp08/exp10_calibration.json)
BOUND = 1.5                        # FAMILY_BOUND_SIG * sig
S_STEP = 0.25 * 0.5 * np.sqrt(1 - 0.75 ** 2)   # sigma_step(), derived not typed
STAT_SD = 0.125                    # stationary deviation sd = 0.25 * sig
K = 4

def reflect(x, b=BOUND):
    period = 4 * b
    y = np.mod(x + b, period)
    y = np.where(y > 2 * b, period - y, y)
    return y - b

def tremble_baselines(n=500000, k=11, seed=1):
    """A_dwell analog (static anchor at onset). Returns net/path@11, traverse@11, path@11."""
    rng = np.random.default_rng(seed)
    c = np.clip(SIG * rng.standard_normal((n, K)), -BOUND, BOUND)
    c0 = c.copy(); P = [c.copy()]; ps = []
    for p in range(2, k + 1):
        cn = reflect(c + THETA * (c0 - c) + S_STEP * rng.standard_normal((n, K)))
        ps.append(np.linalg.norm(cn - c, axis=1)); c = cn; P.append(c.copy())
    P = np.stack(P, 0)
    npb = (np.linalg.norm(P[-1] - P[0], axis=1) / np.sum(ps, axis=0)).mean()
    trb = ((P.max(0) - P.min(0)) / (2 * BOUND)).mean(1).mean()
    return npb, trb, np.mean(np.sum(ps, axis=0))

def orbit(r, omega, n, k=11, seed=1):
    """Orbital anchor per §9 R2. Returns net/path, traverse, arc, perstep_med, ANCHOR_over, clip."""
    rng = np.random.default_rng(seed)
    onset = np.clip(SIG * rng.standard_normal((n, K)), -BOUND, BOUND)
    cl = BOUND - r - 3 * STAT_SD               # centering rule: |center|inf + r + 3*stat_sd <= 1.5
    center = np.clip(onset, -cl, cl)
    e1 = rng.standard_normal((n, K)); e1 /= np.linalg.norm(e1, axis=1, keepdims=True)
    e2 = rng.standard_normal((n, K)); e2 -= np.sum(e2 * e1, axis=1, keepdims=True) * e1
    e2 /= np.linalg.norm(e2, axis=1, keepdims=True)
    ph = rng.uniform(0, 2 * np.pi, n)
    def anc(p):
        ang = ph + omega * (p - 1)
        return center + r * (np.cos(ang)[:, None] * e1 + np.sin(ang)[:, None] * e2)
    c = anc(1).copy(); P = [c.copy()]; anchor_over = 0; perstep = []
    for p in range(2, k + 1):
        a = anc(p)
        anchor_over += int((np.abs(a) > BOUND).sum())   # the R6 zero-reflection assert = ANCHOR path
        cn = reflect(c + THETA * (a - c) + S_STEP * rng.standard_normal((n, K)))
        perstep.append(np.linalg.norm(cn - c, axis=1)); c = cn; P.append(c.copy())
    P = np.stack(P, 0)
    npr = (np.linalg.norm(P[-1] - P[0], axis=1)
           / np.linalg.norm(np.diff(P, axis=0), axis=2).sum(0)).mean()
    trav = ((P.max(0) - P.min(0)) / (2 * BOUND)).mean(1).mean()
    return npr, trav, r * omega * (k - 1), np.median(np.concatenate(perstep)), anchor_over, cl

if __name__ == "__main__":
    NPB, TRB, TPATH = tremble_baselines()
    print(f"COMPUTED tremble baselines: net/path@11={NPB:.4f} traverse@11={TRB:.4f} path@11={TPATH:.4f}")
    print(f"floors: net/path >= {4*NPB:.4f} (4x) | traverse in [{2.5*TRB:.4f} (2.5x), 0.50] | arc >= {TPATH:.4f}")
    CONFUSION = 1.311   # forensic cross-boundary norm median (upper edge; per-step must stay well below)
    # RB-2 RULED grid (prereg §9 R3): r in [0.85,1.10] step 0.05; omega in [12,22] deg step 2
    print(f"{'r':>5}{'wdeg':>5}{'np':>7}{'tr':>7}{'arc':>6}{'ps':>6}{'clip':>6}  PASS(all floors, pooled+per-seed-min)")
    feas = []
    for r in [0.85, 0.90, 0.95, 1.00, 1.05, 1.10]:
        for wdeg in [12, 14, 16, 18, 20, 22]:
            w = np.deg2rad(wdeg)
            npp, trp, arc, ps, ao, cl = orbit(r, w, 200000)
            if cl <= 0:
                continue
            # per-seed-WORST (RB-2 fold, confirmation-panel m6): MIN for lower-bound floors,
            # MAX for the two ceiling forms (traverse <= 0.50; per-step <= confusion bound)
            per = [orbit(r, w, 50000, seed=s) for s in range(8)]
            npmin = min(t[0] for t in per); trmin = min(t[1] for t in per)
            trmax = max(t[1] for t in per); psmax = max(t[3] for t in per)
            ok = (npp >= 4 * NPB and npmin >= 4 * NPB
                  and 2.5 * TRB <= trp <= 0.50 and trmin >= 2.5 * TRB and trmax <= 0.50
                  and arc >= TPATH and ps <= CONFUSION and psmax <= CONFUSION and ao == 0)
            if ok:
                feas.append((r * w, r, wdeg, cl))
            print(f"{r:5.2f}{wdeg:5d}{npp:7.3f}{trp:7.3f}{arc:6.2f}{ps:6.3f}{cl:6.2f}  {'Y' if ok else '.'}")
    # RB-2 RULED selection (lexicographic): (1) feasible all floors pooled+per-seed-min;
    # (2) maximize clip half-width; (3) tie-break minimal r*omega. (r,omega) then FROZEN.
    # feasibility = pooled AND per-seed-WORST (MIN for floors, MAX for ceilings) per prereg R3.
    feas.sort(key=lambda t: (-t[3], t[0]))
    print("\nfeasible set under the RULED lexicographic objective (max clip, then min r*omega):")
    for rw, r, wd, cl in feas:
        print(f"  r={r:4.2f} w={wd:2d}deg  clip=+-{cl:.3f}  r*w={rw:.3f}")
    if feas:
        rw, r, wd, cl = feas[0]
        print(f"\nSELECTED (sim expectation; the real generator at G2 decides): "
              f"(r={r:4.2f}, omega={wd}deg)  clip=+-{cl:.3f}")
    else:
        print("\nregion EMPTY -> geometry-conflict HALT")
