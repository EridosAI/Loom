"""Continuous single-object stimulus stream (Stage-0 §8).

One object, two appearance axes on disjoint subspaces (exp01 orthogonal-subspace
principle): A = salient DECOY (coarse axes, word-irrelevant, unlabelled) and B = subtle
PROBE (disjoint fine axes, word-relevant, labelled). The word channel names B.

Temporal structure (the G<->D resolution, §8): **within a dwell, (A,B) is STABLE; only the
entangled order-drift varies wave-to-wave.** B stays word-labelable (Readout G clean); the
drift supplies Readout D's within-window variation. Dwells persist a stochastic number of
waves >= W, then an UNMARKED transition (no boundary signal, no across-window chaining).
The drift carrier is one continuous OU-with-positive-slope walk over the whole stream
(never reset per window); it is entangled into content dims at alpha=1 by the loop, with no
separable carrier (§3). Balanced over the generative distribution across the stream.

This module is pure data (raw stimulus + word tokens + drift + dwell ids). Emission,
entanglement and masking happen in loop.py.
"""

from __future__ import annotations

from dataclasses import dataclass

import torch


class Stimulus:
    """Raw vision-input geometry. A on coarse axes 0..n_A-1 (radius R_coarse, salient);
    B offset on disjoint fine axes n_A..n_A+n_B-1 (radius r_fine, subtle). Rotated to a
    generic frame so nothing reads raw coordinates. Pooled encoders cannot resolve B
    (members collapse) until Delta2 opens — floor_B vs ceiling_B is a pooling-state gap,
    not an r_fine magnitude."""

    def __init__(self, D: int, n_A: int, n_B: int, *, R_coarse: float = 10.0,
                 r_fine: float = 1.0, sigma: float = 0.3, seed: int = 0):
        if n_A + n_B > D:
            raise ValueError(f"need n_A + n_B <= D; got {n_A}+{n_B} > {D}")
        g = torch.Generator().manual_seed(seed)
        self.D, self.n_A, self.n_B, self.sigma = D, n_A, n_B, sigma
        centre = torch.zeros(n_A, n_B, D)
        for a in range(n_A):
            for b in range(n_B):
                v = torch.zeros(D)
                v[a] = R_coarse                      # A on a coarse axis (salient)
                v[n_A + b] = r_fine                  # B on a disjoint fine axis (subtle)
                centre[a, b] = v
        Q, _ = torch.linalg.qr(torch.randn(D, D, generator=g))
        self.centre = centre @ Q.t()                 # (n_A, n_B, D), rotated
        self.Q = Q

    def raw(self, a: torch.Tensor, b: torch.Tensor, gen: torch.Generator) -> torch.Tensor:
        mu = self.centre[a, b]
        return mu + self.sigma * torch.randn(mu.shape, generator=gen)

    def raw_clean(self, a: torch.Tensor, b: torch.Tensor) -> torch.Tensor:
        return self.centre[a, b]


@dataclass
class Stream:
    a: torch.Tensor          # (T,) A-level per wave
    b: torch.Tensor          # (T,) B-level per wave
    word: torch.Tensor       # (T,) word token per wave (= b in the intact arm)
    drift: torch.Tensor      # (T,) drift, rescaled to unit within-window spread (order)
    nuisance: torch.Tensor   # (T,) continuous content nuisance along u (the confound)
    dwell_id: torch.Tensor   # (T,) which dwell each wave belongs to
    n_A: int
    n_B: int

    @property
    def T(self) -> int:
        return self.a.shape[0]

    def window(self, t: int, W: int) -> dict:
        sl = slice(t, t + W)
        return dict(a=self.a[sl], b=self.b[sl], word=self.word[sl],
                    drift=self.drift[sl], nuisance=self.nuisance[sl],
                    dwell_id=self.dwell_id[sl])

    def within_dwell(self, t: int, W: int) -> bool:
        d = self.dwell_id[t:t + W]
        return bool((d == d[0]).all())


def make_stream(T: int, n_A: int, n_B: int, *, W: int = 3, sigma: float = 0.8,
                slope: float = 0.7, dwell_extra: int = 4, seed: int = 0) -> Stream:
    """Build a continuous stream of T waves.

    Dwell length ~ W + Uniform[0, dwell_extra] (>= W). (A,B) resampled uniformly each
    dwell (balanced decoy + probe). Drift is one OU-with-positive-slope walk, standardized
    over the stream (within any W-window the begin wave has the lowest drift; ``sigma``
    tunes adjacent overlap)."""
    g = torch.Generator().manual_seed(seed)
    a_list, b_list, dwell_list = [], [], []
    did = 0
    while len(a_list) < T:
        a = int(torch.randint(0, n_A, (1,), generator=g))
        b = int(torch.randint(0, n_B, (1,), generator=g))
        length = W + int(torch.randint(0, dwell_extra + 1, (1,), generator=g))
        for _ in range(length):
            a_list.append(a); b_list.append(b); dwell_list.append(did)
        did += 1
    a = torch.tensor(a_list[:T]); b = torch.tensor(b_list[:T])
    dwell_id = torch.tensor(dwell_list[:T])
    word = b.clone()                                  # word names B (intact arm)
    # continuous positive-slope drift walk
    steps = slope + sigma * torch.randn(T - 1, generator=g)
    drift = torch.cat([torch.zeros(1), steps.cumsum(0)])
    drift = drift - drift.mean()
    def unit_within_window(x):
        x = x - x.mean()
        ww = torch.stack([x[t:t + W].std(unbiased=False) for t in range(0, T - W, 7)])
        return x / (ww.mean() + 1e-8)

    # rescale to UNIT WITHIN-WINDOW spread (the order lives in within-window differences).
    drift = unit_within_window(drift)
    # the confound: an INDEPENDENT, driftless (slope=0) cumulative walk on the same scale,
    # injected along u with the drift. Driftless -> its within-window values are non-monotonic
    # -> it confounds the drift's monotonic order (entangled, no clean slot) while spanning the
    # stream at the same scale (so absolute drift still grows -> Readout D scale-watch alive).
    nz = torch.cat([torch.zeros(1), torch.randn(T - 1, generator=g).cumsum(0)])
    nuisance = unit_within_window(nz)
    return Stream(a=a, b=b, word=word, drift=drift, nuisance=nuisance,
                  dwell_id=dwell_id, n_A=n_A, n_B=n_B)
