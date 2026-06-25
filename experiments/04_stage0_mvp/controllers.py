"""The three SEPARATE rates, kept apart by ownership (Stage-0 §13).

They want to blur; the guard is that each controller takes NO input from the others'
domain. (1) unpool clock = loom.pooling.StepSchedule (activity_gate pinned 1) — the only
deployed rate, maturational. (2) gain ramp = GainRamp (fixed-and-swept, both gates OFF,
bound OFF) — attribution control; takes no capacity/confidence input. (3) curriculum =
Curriculum (external confidence-triggered parent adding a CONTRAST word, not a rename) —
the environment, not a PAM mechanism. Re-pool (loom.pooling.AdaptiveRepool) is present and
available but is NOT the run-1 deployed rate (§13: the unpool clock is).
"""

from __future__ import annotations


class GainRamp:
    """Linear ramp from 0 -> gain_max over ramp_steps. Both confidence-gating AND
    capacity-bounding are OFF for run 1 (pure fixed ramp). Scales ONLY L_PAM (§7).
    Deliberately has NO capacity/confidence argument — that coupling would be RATE_BLUR."""

    def __init__(self, gain_max: float = 1.0, ramp_steps: int = 400):
        self.gain_max = gain_max
        self.ramp_steps = max(1, ramp_steps)
        self.confidence_gate = "OFF"
        self.capacity_bound = "OFF"

    def gain(self, t: int) -> float:
        return min(1.0, t / self.ramp_steps) * self.gain_max


class Curriculum:
    """External hand-supplied parent (§13). Introduces B-label words; adds the next
    CONTRAST word when system confidence on the active set crosses ``threshold``
    (contrast-not-rename: a new word with no contrasting pair present is a rename, no
    split). For run 1 it starts with the first ``start_active`` labels so the minimal
    contrast is present immediately (gap-3 testable), and grows on confidence."""

    def __init__(self, n_B: int, *, threshold: float = 0.6, start_active: int = 2,
                 null_token: int | None = None):
        self.n_B = n_B
        self.threshold = threshold
        self.null_token = n_B if null_token is None else null_token
        self.active = set(range(min(start_active, n_B)))

    def word_token(self, true_b: int, *, no_word: bool = False) -> int:
        """The word the parent emits this wave: the true B-label if active, else null.
        ``no_word=True`` is the matched ablation arm (everything null)."""
        if no_word or int(true_b) not in self.active:
            return self.null_token
        return int(true_b)

    def update(self, confidence: float):
        if len(self.active) < self.n_B and confidence >= self.threshold:
            self.active.add(len(self.active))

    @property
    def contrast_available(self) -> bool:
        return len(self.active) >= 2

    def state(self):
        return sorted(self.active)
