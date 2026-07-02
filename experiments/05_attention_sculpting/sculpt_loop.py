"""SculptLoop — the Stage-1 wave loop = Stage0Loop with the four new pieces wired in via the
overridable hooks (one code path; the dynamics in step()/build_cells are inherited UNCHANGED).

Overrides only:
  * ``_make_stim``   -> ConflictStimulus (distractor + category crossed fine axes).
  * ``_make_word``   -> WordCortex with vocab = n_category (the word names the CATEGORY only;
                        this is what makes the distractor associatively inert — SPEC §1).
  * ``_make_curric`` -> Curriculum over the category vocab.
  * ``_word_label``  -> member b -> category(b) (= b % n_category).
  * ``_post_step``   -> constant intrinsic Delta2 re-pool (G3: occupancy decay, envelope open).

Adds read-only diagnostics:
  * ``dc_track``     -> nearest-centroid recovery of distractor and category from vision emissions
                        (the two-arm occupancy readout; reversed lift = distractor(intact) < distractor(no-word)).
  * ``evoke_vision`` -> PAM's evoked prediction for a masked vision slot given co-present context
                        (incl. the word) — used for the Step-0 evocation-divergence check (c).

Non-causal masking, no-stop-grad PAM target, frozen anchor, six cue-shapes: all inherited.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "src"))
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))

from loom.pooling import constant_repool_delta2            # noqa: E402

from loop import Stage0Loop                                 # noqa: E402  (exp04)
from controllers import Curriculum                          # noqa: E402  (exp04)
from encoders import WordCortex                             # noqa: E402  (exp04)
from stream import make_stream                              # noqa: E402  (exp04)

from conflict_stream import ConflictStimulus                # noqa: E402  (exp05)
from revival import population_mean, repose, tie_schedule   # noqa: E402  (exp05, shared w/ exp07)


class SculptLoop(Stage0Loop):
    def __init__(self, cfg, pin):
        super().__init__(cfg, pin)
        # the revival preserve tie = the cortex StepSchedule applied to PAM (same machinery as
        # self.unpool). Onsets default to the cortex's own clock (t1/t2 = 300/1200 deployed waves)
        # — the [RECONCILE] mapping of the neutral rig's 0.075/0.30 fractions; never the 900/3600
        # neutral-budget literals.
        t1 = cfg.pam_t1 if cfg.pam_t1 is not None else cfg.t1
        t2 = cfg.pam_t2 if cfg.pam_t2 is not None else cfg.t2
        self.pam_tie_sched = tie_schedule(lam1_hi=cfg.lam1_hi, lam1_lo=cfg.lam1_lo, t1_step=t1,
                                          lam2_hi=cfg.lam2_hi, lam2_lo=cfg.lam2_lo, t2_step=t2)

    # ------------------------------------------------------------------ revival config wiring
    def _pam_penalty(self, t: int):
        """The preserve tie: two-clock hi->lo StepSchedule on PAM's pool penalty (replaces the
        constant pam_lam disease tie). 'constant' keeps the legacy path for A/B diagnostics."""
        if self.cfg.pam_tie == "constant":
            return super()._pam_penalty(t)
        return self.op.pam.pool_penalty(self.pam_tie_sched.lam1(t), self.pam_tie_sched.lam2(t))

    @torch.no_grad()
    def _vis_population_mean(self) -> torch.Tensor:
        """mu = content-blind population mean of vision emissions over the FULL member set,
        from clean centres (deterministic; independent of the window's member or mask — the
        content-blindness guard). Detached constant at presentation, like the neutral rig's mu."""
        cfg = self.cfg
        a = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
        b = torch.arange(cfg.n_B).repeat(cfg.n_A)
        return population_mean(self.vision.emit(self.stim.raw_clean(a, b)))

    def _pose_pam_input(self, content: torch.Tensor) -> torch.Tensor:
        """Content-blind global mean-centre on the VISION slot of PAM's input frame (cue side).
        Targets are never posed (gap-3 target path untouched); word slot untouched (already the
        sharp anchor); masked cells are overwritten by mask_emb downstream so posing them is inert.
        Works on (W, n_slots, D) training windows and (K, W, n_slots, D) evocation probes."""
        alpha = self.cfg.reposing_alpha
        if alpha == 0.0:
            return content
        mu = self._vis_population_mean()
        posed = content.clone()
        posed[..., 0, :] = repose(content[..., 0, :], mu, alpha)
        return posed

    @torch.no_grad()
    def pam_proto_spread(self) -> float:
        """The death-certificate watch: PAM prototype spread across groups (0 = collapsed =
        content-dead; same formula as exp07_core.measure_d's proto_spread). Logged as a live
        column from t=0 in every run."""
        Wp = self.op.pam.weights()
        return (Wp - Wp.mean(0)).norm(dim=1).mean().item()

    # ------------------------------------------------------------------ factory overrides
    def _make_stim(self):
        cfg = self.cfg
        return ConflictStimulus(
            cfg.D, cfg.n_A, cfg.n_distractor, cfg.n_category,
            R_coarse=cfg.R_coarse, r_distractor=cfg.r_distractor,
            r_category=cfg.r_category, sigma=cfg.sigma_stim, seed=cfg.seed)

    def _make_word(self):
        cfg = self.cfg
        return WordCortex(cfg.D, cfg.n_category, seed=cfg.seed + 1)   # vocab = categories

    def _make_curric(self):
        cfg = self.cfg
        return Curriculum(cfg.n_category, threshold=cfg.curric_threshold,
                          start_active=cfg.curric_start_active,
                          null_token=self.word.null_token)

    def _make_stream(self):
        # members sampled uniformly over n_B = n_distractor*n_category == uniform (distractor,category).
        cfg = self.cfg
        return make_stream(cfg.T, cfg.n_A, cfg.n_B, W=cfg.W, sigma=cfg.sigma_drift,
                           slope=cfg.slope, dwell_extra=cfg.dwell_extra, seed=cfg.seed + 3)

    def _word_label(self, b):
        return b % self.cfg.n_category                       # member -> category (the named axis)

    def _post_step(self):
        constant_repool_delta2(self.vision.pool, self.cfg.repool_rate)   # G3: Delta2-only decay

    # ------------------------------------------------------------------ diagnostics
    @torch.no_grad()
    def dc_track(self, n: int) -> dict:
        """Nearest-centroid recovery of DISTRACTOR and CATEGORY from vision emissions (no free
        head; disjoint support/eval). The occupancy readout: how well each axis is carried by
        the vision cortex's current emissions."""
        cfg = self.cfg
        g = torch.Generator().manual_seed(self._t * 7 + 1)

        def emit(K):
            a = torch.randint(0, cfg.n_A, (K,), generator=g)
            b = torch.randint(0, cfg.n_B, (K,), generator=g)
            return self.vision.emit(self.stim.raw(a, b, g)), b

        es, bs = emit(max(n, cfg.n_A * cfg.n_B * 8))
        d_sup, c_sup = bs // cfg.n_category, bs % cfg.n_category
        cen_d = torch.stack([es[d_sup == k].mean(0) for k in range(cfg.n_distractor)])
        cen_c = torch.stack([es[c_sup == k].mean(0) for k in range(cfg.n_category)])
        ee, be = emit(n)
        d_e, c_e = be // cfg.n_category, be % cfg.n_category
        d_track = (torch.cdist(ee, cen_d).argmin(1) == d_e).float().mean().item()
        c_track = (torch.cdist(ee, cen_c).argmin(1) == c_e).float().mean().item()
        return dict(distractor_track=d_track, category_track=c_track,
                    distractor_chance=1.0 / cfg.n_distractor,
                    category_chance=1.0 / cfg.n_category)

    @torch.no_grad()
    def evoke_vision(self, a_idx, b_idx, *, mask_wave: int = 1, associative: bool = True) -> torch.Tensor:
        """What PAM evokes for a member's vision slot given co-present context.

        Builds a within-dwell window of the SAME member (a, b) across all W waves and returns the
        operator's prediction for the vision slot of ``mask_wave`` (K, D). A FIXED drift carrier
        is injected (position defined; CANCELS in cross-member differences); clean centres (no stim
        noise) so the only variation across probes is the member identity. Read-only.

        ``associative=True`` (Step-0 check (c)): mask ALL vision slots, leave the WORD slots
        visible -> the read is reconstructed from the word (= category), ISOLATING the associative
        channel. Across category the word differs (productive); across distractor the word is
        identical (associatively inert BY CONSTRUCTION, since the word names category only). This is
        the spec's "PAM evokes the same across distractor / different across category".
        ``associative=False``: mask only the read slot (sibling vision visible) -> FULL-context
        evocation, dominated by the salient distractor via the vision channel (diagnostic only)."""
        cfg = self.cfg
        W = cfg.W
        a_idx = torch.as_tensor(a_idx, dtype=torch.long)
        b_idx = torch.as_tensor(b_idx, dtype=torch.long)
        K = a_idx.shape[0]
        e_vis = self.vision.emit(self.stim.raw_clean(a_idx, b_idx))    # (K, D)
        e_word = self.word.emit(b_idx % cfg.n_category)               # (K, D) category token
        content = torch.zeros(K, W, cfg.n_slots, cfg.D)
        content[:, :, 0, :] = e_vis.unsqueeze(1)
        content[:, :, 1, :] = e_word.unsqueeze(1)
        mask = torch.zeros(W, cfg.n_slots, dtype=torch.bool)
        if associative:
            mask[:, 0] = True                                        # mask ALL vision slots (word channel only)
        else:
            mask[mask_wave, 0] = True                                # mask only the read slot (full context)
        # the probe presents the SAME frame as training (revival re-pose on vision cells; inert in
        # associative mode where all vision is masked, load-bearing for the full-context diagnostic).
        masked = self._pose_pam_input(content).clone()
        masked[:, mask] = self.op.mask_emb
        drift_w = torch.arange(W, dtype=torch.float32) - (W - 1) / 2.0
        cells_in = masked + self.cb.kappa * drift_w.view(1, W, 1, 1) * self.cb.u
        C = W * cfg.n_slots
        cells = cells_in.reshape(K, C, cfg.D)
        visible = (~mask).reshape(C)
        pred = self.op(cells, self.slot_ids, visible)                 # (K, C, D)
        return pred[:, mask_wave * cfg.n_slots + 0, :]                # (K, D) evoked vision slot
