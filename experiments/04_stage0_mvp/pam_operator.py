"""THE OPERATOR — prototype-resonance over the pooling substrate (Stage-0 §2-ii, surfaced
for review and approved). Named pam_operator to avoid shadowing Python's stdlib ``operator``.

Carrier discipline (§3, verbatim): the drift carrier and the operator's position-read must
stay entangled, never a clean separable slot, or order-as-content silently becomes
order-as-index in the first build. ``pos_extract`` is a free linear read of the WHOLE cell;
it can only become a clean carrier tap if the stream hands it one — which §3 forbids.

Why this passes the §2-ii subtractive screen (sole exclusion: a feedforward exact-regression
denoiser):
  * content sits ON the pooling substrate (a second loom.pooling population) — a substrate
    on which recurrence COULD deepen and splitting COULD divide (basin-hosting, §2-iii);
  * AT-ONCE: a single completion act per call (K_settle=1 for run 1; if it ever iterates,
    K_settle is bounded-and-logged);
  * NO free linear head: the readout resonates content against frozen-by-construction
    prototypes (distance, not a trainable class head);
  * NO softmax-attention: cross-cell mixing AND prototype resonance use **inverse-distance
    (Shepard) kernels**, never softmax over learned QK scores — this is NOT nn.Transformer /
    nn.MultiheadAttention. Non-causal by construction (every cell mixes from all visible
    cells, bidirectional).
  * NO PAM latent (§0.1): in_dim == out_dim == D_slice; in_proj EXPANDS to d_model
    (>= D_slice), out_proj reads back — not a compressing encode/decode codec.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch
import torch.nn as nn

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from loom.pooling import HierarchicalPoolingModel  # noqa: E402

EPS = 1e-4


class PrototypeResonanceOperator(nn.Module):
    def __init__(self, D_slice: int, n_slots: int = 2, d_model: int = 64,
                 n_freq: int = 12, pam_groups: int = 8, pam_members: int = 4,
                 seed: int = 0):
        super().__init__()
        torch.manual_seed(seed)
        self.in_dim = self.out_dim = D_slice           # no-latent invariant
        self.D_slice = D_slice
        self.n_slots = n_slots
        d_model = max(d_model, D_slice)                 # never compress (no bottleneck)
        self.d_model = d_model

        self.mask_emb = nn.Parameter(0.02 * torch.randn(D_slice))
        self.pos_extract = nn.Linear(D_slice, 1)        # reads the entangled drift
        freqs = torch.tensor([0.5 * (1.6 ** k) for k in range(n_freq)])
        self.register_buffer("freqs", freqs)
        self.pos_proj = nn.Linear(2 * n_freq, d_model)
        self.in_proj = nn.Linear(D_slice, d_model)
        self.value_proj = nn.Linear(d_model, d_model)
        self.slot_type = nn.Embedding(n_slots, d_model)  # vision vs word (structural tag)
        # The PAM pooling population — content resonates against ITS prototypes (basin-hosting).
        self.pam = HierarchicalPoolingModel(D=d_model, n_groups=pam_groups,
                                            members_per_group=pam_members, seed=seed + 7)
        self.out = nn.Linear(d_model, D_slice)

    # -- the position read (order-as-content), exposed for Readout D --
    def read_position(self, cells: torch.Tensor) -> torch.Tensor:
        """cells (B, C, D_slice) -> scalar position estimate per cell (B, C)."""
        return self.pos_extract(cells).squeeze(-1)

    def _hidden(self, cells, slot_ids):
        s = self.pos_extract(cells)                      # (B, C, 1) reads entangled drift
        ang = s * self.freqs                             # (B, C, n_freq)
        ff = torch.cat([torch.sin(ang), torch.cos(ang)], dim=-1)
        pos_key = self.pos_proj(ff)                      # (B, C, d_model)
        h = self.in_proj(cells) + pos_key + self.slot_type(slot_ids).unsqueeze(0)
        return h, pos_key

    def forward(self, cells: torch.Tensor, slot_ids: torch.Tensor,
                visible: torch.Tensor) -> torch.Tensor:
        """Single at-once completion.

        cells   (B, C, D_slice) — window cells; masked cells already hold mask_emb (+ the
                 wave's entangled drift, kept so position survives the mask).
        slot_ids (C,) long — slot type per cell (0 vision, 1 word).
        visible  (C,) bool — cued cells (mix only gathers from these).
        Returns predicted clean slices (B, C, D_slice).
        """
        h, pos_key = self._hidden(cells, slot_ids)
        vis = visible.to(h.dtype)                        # (C,)

        # 1) cross-cell mixing: inverse-distance (Shepard) kernel on position keys,
        #    gathering only from VISIBLE cells. NOT softmax.
        d2 = torch.cdist(pos_key, pos_key).pow(2)        # (B, C, C)
        ker = 1.0 / (EPS + d2) * vis.view(1, 1, -1)      # mask columns to visible
        ker = ker / ker.sum(dim=-1, keepdim=True).clamp_min(EPS)
        ctx = ker @ self.value_proj(h)                   # (B, C, d_model)

        # 2) prototype resonance: inverse-distance soft assignment over the PAM substrate
        #    prototypes (no free head, no softmax).
        Wp = self.pam.weights()                          # (U, d_model)
        d2p = torch.cdist(ctx, Wp).pow(2)                # (B, C, U)
        pa = 1.0 / (EPS + d2p)
        pa = pa / pa.sum(dim=-1, keepdim=True).clamp_min(EPS)
        z = pa @ Wp                                      # (B, C, d_model)
        return self.out(z)                               # (B, C, D_slice)

    @torch.no_grad()
    def has_softmax_attention(self) -> bool:
        """Static self-report for the build guard: this operator uses inverse-distance
        kernels only and contains no nn.Transformer / nn.MultiheadAttention."""
        for m in self.modules():
            if isinstance(m, (nn.MultiheadAttention, nn.Transformer,
                              nn.TransformerEncoder, nn.TransformerEncoderLayer)):
                return True
        return False
