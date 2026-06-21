"""Position-aware completion operator (SPEC sec. 5-6).

A tiny transformer encoder over the window-as-set. Three deliberate pieces:

* **Context-derived position key.** The operator extracts a scalar position cue from each
  bundle (``pos_extract``, a learned linear read of the bundle: the dedicated context dim
  at alpha=0, or the drift component along the injection direction at alpha=1) and turns it
  into a comparable positional code via random Fourier features. This is how position is
  read from the **content/context channel** -- a continuous drift value -- rather than from
  the array axis. (A raw scalar is hard for attention to rank; Fourier features make
  closeness-in-value computable, recreating an exp02-style position code from the carrier.)

* **Slot positional encoding `A[slot]`** over the array axis. This makes the operator
  *capable* of using array position, so shuffle is a real test (a permutation-invariant
  operator would make shuffle vacuous and F1 untestable -- disallowed by SPEC sec.5). Under
  shuffle, `A[slot]` is attached to a random true position and is useless, so position must
  come from the context-derived key; unshuffled (Control B), it aligns with true position
  and an axis-exploiting operator can win even at high sigma (the F1 adjudicator).

* **Nearest-prototype readout, no free linear head** (exp01 lesson): the head emits a
  predicted content vector; decoding is by cosine to the *frozen* codebook.
"""

from __future__ import annotations

import math

import torch
import torch.nn as nn


class Completer(nn.Module):
    def __init__(self, in_dim: int, dc: int, L: int, d_model: int = 96,
                 n_layers: int = 3, n_heads: int = 4, n_freq: int = 12, seed: int = 0):
        super().__init__()
        torch.manual_seed(seed)
        self.L = L
        self.in_proj = nn.Linear(in_dim, d_model)
        self.pos_extract = nn.Linear(in_dim, 1)             # read the position scalar from the bundle
        # geometric Fourier frequencies spanning the (standardized) carrier range.
        freqs = torch.tensor([0.5 * (1.6 ** k) for k in range(n_freq)])
        self.register_buffer("freqs", freqs)
        self.pos_proj = nn.Linear(2 * n_freq, d_model)
        self.slot_pe = nn.Embedding(L, d_model)             # array-axis PE (scrambled by shuffle)
        layer = nn.TransformerEncoderLayer(
            d_model=d_model, nhead=n_heads, dim_feedforward=4 * d_model,
            dropout=0.0, batch_first=True, activation="gelu", norm_first=True,
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=n_layers)
        self.out = nn.Linear(d_model, dc)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """x: (B, L, in_dim) -> predicted content vectors (B, L, dc)."""
        s = self.pos_extract(x)                              # (B, L, 1) position scalar
        ang = s * self.freqs                                 # (B, L, n_freq)
        ff = torch.cat([torch.sin(ang), torch.cos(ang)], dim=-1)
        pos_key = self.pos_proj(ff)                          # (B, L, d_model)
        slots = torch.arange(self.L, device=x.device)
        h = self.in_proj(x) + pos_key + self.slot_pe(slots).unsqueeze(0)
        h = self.encoder(h)
        return self.out(h)
