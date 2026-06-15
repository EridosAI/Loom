"""Training harness: lambda controllers + instrumented training loop (SPEC sec. 2-3).

Two lambda controllers, both exposing ``lam1(t)`` / ``lam2(t)`` and an ``update``
hook called at each log step:

* ``StepSchedule``  -- clock-led, pinned-constant unpool (SPEC sec. 2). Start both
  lambdas high (pooled); drop lambda1 at ``t1`` (unpool to G groups); drop lambda2
  at ``t2`` (unpool to full resolution). Capacity opens on a *schedule*, not pulled
  by error. ``t2 = None`` keeps lambda2 high forever (the "always-pooled" baseline).

* ``AdaptiveRepool`` -- the reverse direction (Test C). Holds lambda2 low, watches
  the pull-apart force, and once it is *sustained low* (members no longer pulled
  apart) ramps lambda2 back up to re-tighten. The threshold self-calibrates against
  the largest pull-apart force seen so far, so it needs no hand-tuned absolute value.
"""

from __future__ import annotations

from collections import defaultdict

import torch
import torch.nn.functional as F

import metrics


class StepSchedule:
    def __init__(self, lam1_hi, lam1_lo, lam2_hi, lam2_lo, t1, t2):
        self.lam1_hi, self.lam1_lo = lam1_hi, lam1_lo
        self.lam2_hi, self.lam2_lo = lam2_hi, lam2_lo
        self.t1, self.t2 = t1, t2  # t2=None -> never unpool to full resolution

    def lam1(self, t):
        return self.lam1_lo if (self.t1 is not None and t >= self.t1) else self.lam1_hi

    def lam2(self, t):
        return self.lam2_lo if (self.t2 is not None and t >= self.t2) else self.lam2_hi

    def update(self, t, stats):
        pass


class AdaptiveRepool:
    """Re-pool when the pull-apart force is sustained below ``frac`` of its peak."""

    def __init__(self, lam1, lam2_lo, lam2_hi, frac=0.1, patience=5, ramp_steps=300):
        self._lam1 = lam1
        self.lam2_lo, self.lam2_hi = lam2_lo, lam2_hi
        self.frac, self.patience, self.ramp_steps = frac, patience, ramp_steps
        self.peak = 0.0
        self.count = 0
        self.trigger_t = None

    def lam1(self, t):
        return self._lam1

    def lam2(self, t):
        if self.trigger_t is None:
            return self.lam2_lo
        frac = min(1.0, (t - self.trigger_t) / max(1, self.ramp_steps))
        return self.lam2_lo + frac * (self.lam2_hi - self.lam2_lo)

    def update(self, t, stats):
        if self.trigger_t is not None:
            return
        pull = stats.get("pull_apart", 0.0)
        self.peak = max(self.peak, pull)
        if self.peak > 0 and pull < self.frac * self.peak:
            self.count += 1
        else:
            self.count = 0
        if self.count >= self.patience:
            self.trigger_t = t


@torch.no_grad()
def _eval(model, d):
    cl, fl = model(d.X)
    return metrics.accuracy(cl, d.y_coarse), metrics.accuracy(fl, d.y_fine)


def train(
    model,
    data,
    controller,
    steps,
    *,
    lr=0.05,
    batch=256,
    train_fine=True,
    hard_tie=False,
    eval_data=None,
    log_every=20,
    seed=0,
):
    """Train under a lambda controller, logging the SPEC sec.3 instrumentation.

    ``hard_tie=True`` pins Delta2 == 0 (excluded from the optimiser and zeroed) --
    the control that must *fail* to differentiate in Test A.
    """
    g = torch.Generator().manual_seed(seed)
    if hard_tie:
        with torch.no_grad():
            model.delta2.zero_()
        params = [p for n, p in model.named_parameters() if n != "delta2"]
    else:
        params = list(model.parameters())
    opt = torch.optim.Adam(params, lr=lr)

    eval_data = eval_data or data
    N = len(data)
    log = defaultdict(list)

    for t in range(steps):
        idx = torch.randint(0, N, (batch,), generator=g)
        X, yc, yf = data.X[idx], data.y_coarse[idx], data.y_fine[idx]
        cl, fl = model(X)
        loss = F.cross_entropy(cl, yc)
        if train_fine:
            loss = loss + F.cross_entropy(fl, yf)
        loss = loss + model.pool_penalty(controller.lam1(t), controller.lam2(t))
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()

        if t % log_every == 0 or t == steps - 1:
            stats = _record(log, t, model, data, eval_data, controller, train_fine)
            controller.update(t, stats)

    return log


def _record(log, t, model, data, eval_data, controller, train_fine):
    ca_tr, fa_tr = _eval(model, data)
    ca_te, fa_te = _eval(model, eval_data)
    d1, d2 = model.residual_norms()
    # Gradient signal on a fresh batch (kept modest for speed).
    n = min(512, len(data))
    gstats = metrics.intra_group_grad_stats(
        model, data.X[:n], data.y_coarse[:n], data.y_fine[:n], train_fine
    )
    spread = metrics.within_group_spread(model)

    log["step"].append(t)
    log["lam1"].append(controller.lam1(t))
    log["lam2"].append(controller.lam2(t))
    log["coarse_acc_tr"].append(ca_tr)
    log["fine_acc_tr"].append(fa_tr)
    log["coarse_acc_te"].append(ca_te)
    log["fine_acc_te"].append(fa_te)
    log["d1_mean"].append(d1.mean().item())
    log["d2_mean"].append(d2.mean().item())
    log["spread"].append(spread)
    log["cos_disagreement"].append(gstats["cos_disagreement"])
    log["pull_apart"].append(gstats["pull_apart"])
    return dict(gstats, spread=spread, coarse_acc_te=ca_te, fine_acc_te=fa_te)
