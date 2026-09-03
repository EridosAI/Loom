"""Verdict primitives (Stage-0 §9): the pre-registered tables are DATA, so the named
pass/fail shape literally IS the source of truth, and the Stage-3 wrong-reason guard is
structural — a clean primary whose required baseline-gap/ablation predicate is unmet is
forced to WRONG_REASON, never PASS.
"""

from __future__ import annotations

from dataclasses import dataclass, field


class Outcome:
    PASS = "PASS"
    NORMAL = "NORMAL"
    BOUNDARY = "BOUNDARY"
    INVALID = "INVALID"
    WRONG_REASON = "WRONG_REASON"
    # named fails are free-form strings, e.g. "FAIL-capture-instead-of-acquisition"


@dataclass
class Verdict:
    outcome: str
    evidence: dict = field(default_factory=dict)
    wrong_reason: bool = False
    notes: str = ""

    def __str__(self):
        wr = "  [WRONG_REASON]" if self.wrong_reason else ""
        return f"{self.outcome}{wr} :: {self.notes}"


def score_against_table(rows, conditioning: dict, *, wrong_reason_predicate=None) -> Verdict:
    """``rows`` = ordered list of (outcome_name, predicate(conditioning)->bool, reading).
    Walk in registered order; return the first match. If ``wrong_reason_predicate`` is given
    and fires, force a WRONG_REASON verdict regardless of which row matched (the Stage-3
    guard: primary cleared its bar but the baseline-gap/ablation did not hold)."""
    matched = None
    for name, pred, reading in rows:
        if pred(conditioning):
            matched = (name, reading)
            break
    if matched is None:
        return Verdict(Outcome.INVALID, dict(conditioning), notes="no pre-registered row matched")
    name, reading = matched
    if wrong_reason_predicate is not None and wrong_reason_predicate(conditioning):
        return Verdict(Outcome.WRONG_REASON, dict(conditioning), wrong_reason=True,
                       notes=f"{name} matched but baseline-gap absent: {reading}")
    return Verdict(name, dict(conditioning), notes=reading)
