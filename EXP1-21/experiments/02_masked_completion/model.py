"""Tiny masked-completion transformer with a causal/non-causal switch (SPEC, "Model").

The smallest masked-LM backbone that trains. Using a transformer encoder is *not*
architectural drift: it is not being built into the system, only used to isolate the
single variable this rig is about -- **attention direction**:

* ``causal=False`` -- masked positions attend both left and right (the property recall
  needs: random-access fill-in).
* ``causal=True`` -- masked positions attend left only. This literally instantiates the
  forbidden forward / next-window predictor and is the control.

Everything else is identical between the two.

Flagged simplification (the deferred part): positions are given by **explicit position
embeddings**, i.e. order-as-index. The real architecture's claim is
order/position-*as-content* (riding in the embedding), which this rig does NOT test.
A pass here is the masked-LM property, not the real claim.
"""

from __future__ import annotations

import torch
import torch.nn as nn


class TinyMaskedTransformer(nn.Module):
    def __init__(self, V: int, L: int, d: int = 64, n_layers: int = 2,
                 n_heads: int = 4, causal: bool = False, seed: int = 0):
        super().__init__()
        torch.manual_seed(seed)
        self.V = V
        self.L = L
        self.causal = causal
        self.mask_id = V  # the [MASK] token id (separate from the vocab 0..V-1)

        self.tok = nn.Embedding(V + 1, d)
        self.pos = nn.Embedding(L, d)
        layer = nn.TransformerEncoderLayer(
            d_model=d, nhead=n_heads, dim_feedforward=4 * d,
            dropout=0.0, batch_first=True, activation="gelu",
        )
        self.encoder = nn.TransformerEncoder(layer, num_layers=n_layers)
        self.head = nn.Linear(d, V)

        # Causal mask: position i may attend to j <= i; True entries are blocked.
        causal_mask = torch.triu(torch.ones(L, L, dtype=torch.bool), diagonal=1)
        self.register_buffer("causal_mask", causal_mask)

    def forward(self, tokens: torch.Tensor) -> torch.Tensor:
        """tokens: (B, L) with ``mask_id`` at masked positions. Returns (B, L, V) logits."""
        pos_ids = torch.arange(self.L, device=tokens.device)
        h = self.tok(tokens) + self.pos(pos_ids).unsqueeze(0)
        attn_mask = self.causal_mask if self.causal else None
        h = self.encoder(h, mask=attn_mask)
        return self.head(h)
