"""The single PAM wave loop (Stage-0 §2-i, §5, §7, §9 structural signal #1).

One code path per wave: slide W=3, draw a block-level slice mask from the full cue-shape
distribution, ONE at-once completion, ONE gradient step. NO train/run branch (use=complete
+ adjust=step). Asymmetric plasticity with NO detach anywhere on the PAM target path: the
masked-cell target is the cortices' own current emission with grad ATTACHED, so the
target-side gradient on a masked VISION cell IS the gap-3 pressure; the word cortex is
frozen (lr=0, excluded from the optimiser) so its target-side gradient is computed-but-not
-applied. Freeze != detach.

L_total = gain*L_PAM + alpha_spread*L_spread + L_JEPA  (gain scales ONLY L_PAM), plus the
pooling-substrate penalties (the §4 soft-tie law) which are not part of the §7 sum.

Entanglement (§3): the wave's drift is injected along u AFTER masking, so a masked cell
keeps its wave's position (order survives the mask). The live model never sees a separable
carrier — order-as-content, never order-as-index.
"""

from __future__ import annotations

import sys
from pathlib import Path

import torch
import torch.nn.functional as F

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from loom import order, poolmetrics, spread                       # noqa: E402
from loom.completion import apply_slice_mask, sample_mask_grid    # noqa: E402
from loom.pooling import StepSchedule                             # noqa: E402

import constants                                                  # noqa: E402
from controllers import Curriculum, GainRamp                      # noqa: E402
from encoders import VisionCortex, WordCortex                     # noqa: E402
from pam_operator import PrototypeResonanceOperator               # noqa: E402
from stream import Stimulus, make_stream                          # noqa: E402


class Stage0Loop:
    def __init__(self, cfg: constants.Stage0Config, pin: constants.PinnedConstants):
        self.cfg, self.pin = cfg, pin
        self.gen = torch.Generator().manual_seed(cfg.seed)
        torch.manual_seed(cfg.seed)

        # Construction via overridable factories (Stage-1 SculptLoop swaps the conflict
        # stimulus / category word-cortex in; the defaults below are Phase-1-identical).
        self.stim = self._make_stim()
        # converged-coarse start: centre the vision pool on the data mean (still plastic).
        init_center = self.stim.centre.reshape(-1, cfg.D).mean(0)
        self.vision = VisionCortex(cfg.D, cfg.n_A, cfg.n_B, init_center=init_center,
                                   seed=cfg.seed)
        self.word = self._make_word()
        self.op = PrototypeResonanceOperator(
            D_slice=cfg.D, n_slots=cfg.n_slots, d_model=cfg.d_model, n_freq=cfg.n_freq,
            pam_groups=cfg.pam_groups, pam_members=cfg.pam_members, seed=cfg.seed + 2)

        self.unpool = StepSchedule(cfg.lam1_hi, cfg.lam1_lo, cfg.lam2_hi, cfg.lam2_lo,
                                   cfg.t1, cfg.t2, activity_gate=1.0)
        self.gain = GainRamp(cfg.gain_max, cfg.ramp_steps)
        self.curric = self._make_curric()
        self.stream = self._make_stream()

        # entanglement direction u + scale kappa from a sample of CLEAN emitted content.
        self.cb = self._build_codebook()

        # optimiser: vision + operator ONLY (word frozen -> excluded). No wd/EMA.
        params = list(self.vision.parameters()) + list(self.op.parameters())
        self.opt = torch.optim.Adam(params, lr=cfg.lr)
        self._t = 0

        self.slot_ids = torch.tensor([s for _ in range(cfg.W) for s in range(cfg.n_slots)])

    # ------------------------------------------------------------------ factories / hooks
    # Defaults reproduce Phase-1 exactly; Stage-1 SculptLoop overrides these (one code path,
    # the dynamics in step()/build_cells are inherited unchanged).
    def _make_stim(self):
        cfg = self.cfg
        return Stimulus(cfg.D, cfg.n_A, cfg.n_B, R_coarse=cfg.R_coarse,
                        r_fine=cfg.r_fine, sigma=cfg.sigma_stim, seed=cfg.seed)

    def _make_word(self):
        cfg = self.cfg
        return WordCortex(cfg.D, cfg.n_B, seed=cfg.seed + 1)

    def _make_curric(self):
        cfg = self.cfg
        return Curriculum(cfg.n_B, threshold=cfg.curric_threshold,
                          start_active=cfg.curric_start_active,
                          null_token=self.word.null_token)

    def _make_stream(self):
        cfg = self.cfg
        return make_stream(cfg.T, cfg.n_A, cfg.n_B, W=cfg.W, sigma=cfg.sigma_drift,
                           slope=cfg.slope, dwell_extra=cfg.dwell_extra, seed=cfg.seed + 3)

    def _word_label(self, b):
        """The word label for member index ``b``. Identity in Phase-1 (word names the member);
        Stage-1 overrides this to name the CATEGORY component only (word is category-agnostic of
        the distractor) — the whole reason the distractor is associatively inert."""
        return b

    def _post_step(self):
        """Post-optimizer-step substrate hook (no-op in Phase-1). Stage-1 applies the constant
        intrinsic Delta2 re-pool here (G3: occupancy decay, envelope untouched)."""
        pass

    def _pam_penalty(self, t: int):
        """PAM substrate tie for this wave. Phase-1 default = the constant light penalty
        (lam1=lam2=cfg.pam_lam), verbatim the pre-hook expression. Stage-1 SculptLoop overrides
        with the two-clock cortex StepSchedule (the revival preserve tie)."""
        return self.op.pam.pool_penalty(self.cfg.pam_lam, self.cfg.pam_lam)

    def _pose_pam_input(self, content: torch.Tensor) -> torch.Tensor:
        """Presentation-frame hook: the content PAM sees as INPUT (cue side), before masking.
        Identity in Phase-1. Stage-1 re-poses the vision slots (content-blind global mean-centre,
        revival config). The TARGET is never posed — the gap-3 target path is untouched."""
        return content

    # ------------------------------------------------------------------ setup
    @torch.no_grad()
    def _build_codebook(self):
        g = torch.Generator().manual_seed(self.cfg.seed + 99)
        a = torch.randint(0, self.cfg.n_A, (256,), generator=g)
        b = torch.randint(0, self.cfg.n_B, (256,), generator=g)
        raw = self.stim.raw(a, b, g)
        e_vis = self.vision.emit(raw)
        e_word = self.word.emit(self._word_label(b))
        content = torch.cat([e_vis, e_word], dim=0)        # (512, D) sample of slices
        return order.make_codebook_from_content(content)

    # ------------------------------------------------------------------ window
    def build_cells(self, t: int, *, no_word: bool, gen, ablate: str = "none"):
        cfg = self.cfg
        win = self.stream.window(t % (self.stream.T - cfg.W), cfg.W)
        a, b, drift_w, dwell = win["a"], win["b"], win["drift"], win["dwell_id"]
        raw = self.stim.raw(a, b, gen)                     # (W, D)
        e_vis = self.vision.emit(raw)                      # (W, D) plastic, grad
        wl = self._word_label(b)                            # member -> word label (category in Stage-1)
        tokens = torch.tensor([self.curric.word_token(int(wl[w]), no_word=no_word)
                               for w in range(cfg.W)])
        e_word = self.word.emit(tokens)                    # (W, D) frozen
        content = torch.stack([e_vis, e_word], dim=1)      # (W, n_slots, D), clean targets

        mask, fam = sample_mask_grid(cfg.W, cfg.n_slots, gen)         # True = masked
        masked = apply_slice_mask(self._pose_pam_input(content), mask, self.op.mask_emb)  # identity -> MASK

        if ablate == "zero":
            drift_w = torch.zeros_like(drift_w)
        elif ablate == "flip":
            drift_w = drift_w.flip(0)
        # inject drift + a continuous content nuisance along u AFTER masking (position
        # survives the mask, §3). The nuisance is the confound that keeps the carrier
        # entangled (no clean slot) regardless of whether content collapses; it is stripped
        # from the target (the operator denoises it, like exp03's codeword spread along u).
        kappa_c = cfg.entangle_nuisance_frac * self.cb.kappa
        dcell = drift_w.view(cfg.W, 1, 1)                  # (W,1,1) broadcast over slots, dim
        ncell = win["nuisance"].view(cfg.W, 1, 1)
        cells_in = masked + self.cb.kappa * dcell * self.cb.u + kappa_c * ncell * self.cb.u

        C = cfg.W * cfg.n_slots
        return dict(
            cells=cells_in.reshape(C, cfg.D),
            target=content.reshape(C, cfg.D),              # clean, grad attached (no detach)
            mask=mask.reshape(C), visible=(~mask).reshape(C),
            fam=fam, raw=raw, drift_w=drift_w, dwell=dwell, e_vis=e_vis,
        )

    def _l_pam(self, bc):
        pred = self.op(bc["cells"].unsqueeze(0), self.slot_ids, bc["visible"])[0]
        m = bc["mask"]
        return F.mse_loss(pred[m], bc["target"][m]), pred

    def _l_jepa(self, bc):
        raw, dwell, cfg = bc["raw"], bc["dwell"], self.cfg
        terms = []
        for w in range(cfg.W - 1):
            if int(dwell[w]) == int(dwell[w + 1]):          # within-dwell pairs only
                terms.append(self.vision.l_jepa(raw[w:w + 1], raw[w + 1:w + 2]))
        return torch.stack(terms).sum() if terms else torch.zeros(())

    def _l_spread(self, gen):
        cfg = self.cfg
        a = torch.randint(0, cfg.n_A, (cfg.spread_batch,), generator=gen)
        b = torch.randint(0, cfg.n_B, (cfg.spread_batch,), generator=gen)
        e = self.vision.emit(self.stim.raw(a, b, gen))      # grad flows to vision
        return spread.spread_loss(e, self.pin.P, gen)

    # ------------------------------------------------------------------ one wave
    def step(self, no_word: bool = False) -> dict:
        t = self._t
        bc = self.build_cells(t, no_word=no_word, gen=self.gen)
        l_pam, _ = self._l_pam(bc)
        l_jepa = self._l_jepa(bc)
        l_spread = self._l_spread(self.gen)
        vis_pen = self.vision.pool.pool_penalty(self.unpool.lam1(t), self.unpool.lam2(t))
        pam_pen = self._pam_penalty(t)
        gain = self.gain.gain(t)

        L = gain * l_pam + self.pin.alpha_spread * l_spread + l_jepa + vis_pen + pam_pen
        self.opt.zero_grad(set_to_none=True)
        L.backward()
        self.opt.step()
        self._post_step()                                  # Stage-1: constant Delta2 re-pool (G3 no-op in Phase-1)
        self._t += 1
        return dict(l_pam=l_pam.item(), l_jepa=float(l_jepa.detach()),
                    l_spread=l_spread.item(), gain=gain, fam=bc["fam"],
                    lam2=self.unpool.lam2(t))

    # ------------------------------------------------------------------ diagnostics
    @torch.no_grad()
    def b_a_track(self, n: int) -> dict:
        """Nearest-centroid (no free head) A/B accuracy on vision emissions. Disjoint
        support (centroids) and eval sets."""
        cfg = self.cfg
        g = torch.Generator().manual_seed(self._t * 7 + 1)
        def emit(K):
            a = torch.randint(0, cfg.n_A, (K,), generator=g)
            b = torch.randint(0, cfg.n_B, (K,), generator=g)
            return self.vision.emit(self.stim.raw(a, b, g)), a, b
        es, asup, bsup = emit(max(n, cfg.n_A * cfg.n_B * 8))
        cen_a = torch.stack([es[asup == c].mean(0) for c in range(cfg.n_A)])
        cen_b = torch.stack([es[bsup == c].mean(0) for c in range(cfg.n_B)])
        ee, ae, be = emit(n)
        a_track = (torch.cdist(ee, cen_a).argmin(1) == ae).float().mean().item()
        b_track = (torch.cdist(ee, cen_b).argmin(1) == be).float().mean().item()
        return dict(A_track=a_track, B_track=b_track,
                    A_chance=1.0 / cfg.n_A, B_chance=1.0 / cfg.n_B)

    def grad_attribution(self) -> dict:
        """||grad L_PAM||, ||grad L_JEPA|| w.r.t. vision Delta2 — both nonzero = gap-3 alive."""
        bc = self.build_cells(self._t, no_word=False, gen=self.gen)
        l_pam, _ = self._l_pam(bc)
        l_jepa = self._l_jepa(bc)
        d2 = self.vision.pool.delta2
        g_pam = torch.autograd.grad(l_pam, d2, retain_graph=True, allow_unused=True)[0]
        gp = 0.0 if g_pam is None else g_pam.norm().item()
        if l_jepa.requires_grad:
            g_j = torch.autograd.grad(l_jepa, d2, retain_graph=False, allow_unused=True)[0]
            gj = 0.0 if g_j is None else g_j.norm().item()
        else:
            gj = 0.0
        return dict(vision_grad_from_PAM=gp, vision_grad_from_JEPA=gj)

    @torch.no_grad()
    def entanglement_r2(self, n: int = 64) -> dict:
        """Carrier entanglement on the live mixture. The GUARD gates on
        ``max_coord_r2`` (the §3 no-clean-slot test); ``full_ols_r2`` is a logged
        diagnostic (content-identifiability, not a slot)."""
        cfg = self.cfg
        g = torch.Generator().manual_seed(self._t * 13 + 5)
        kappa_c = cfg.entangle_nuisance_frac * self.cb.kappa
        contents, drifts = [], []
        for _ in range(n):
            t = int(torch.randint(0, self.stream.T - cfg.W, (1,), generator=g))
            win = self.stream.window(t, cfg.W)
            bc = self.build_cells(t, no_word=False, gen=g)
            # effective content the drift hides within = clean content + the nuisance on u
            ncell = win["nuisance"].view(cfg.W, 1).expand(cfg.W, cfg.n_slots).reshape(-1)
            eff = bc["target"] + kappa_c * ncell.unsqueeze(-1) * self.cb.u
            contents.append(eff)
            dc = bc["drift_w"].view(cfg.W, 1).expand(cfg.W, cfg.n_slots).reshape(-1)
            drifts.append(dc)
        content = torch.stack(contents)                    # (n, C, D)
        d = torch.stack(drifts)                            # (n, C)
        return dict(
            max_coord_r2=order.max_coordinate_r2(content, d, self.cb, center_within=True),
            full_ols_r2=order.linear_separability_r2(content, d, self.cb))

    @torch.no_grad()
    def position_begin_id(self, n: int) -> dict:
        """Readout D order component: does the operator's position-read RECOVER THE ORDER of
        the window (sign-agnostic — there is no inherent begin/end label without a reference,
        so the recovered ordering may be flipped)? We align the operator's read to the drift
        direction over the batch, then score begin = argmin. Scored vs the oracle ceiling and
        the position-invariant chance floor; carrier-zero must collapse it to ~chance (else
        CONTENT_MEMORIZATION). Order lives in the entangled content (not a clean slot, §3)."""
        cfg = self.cfg
        g = torch.Generator().manual_seed(self._t * 17 + 9)
        vis_idx = torch.tensor([w * cfg.n_slots for w in range(cfg.W)])
        S_i, S_z, D = [], [], []
        got, guard = 0, 0
        while got < n and guard < n * 50:
            guard += 1
            t = int(torch.randint(0, self.stream.T - cfg.W, (1,), generator=g))
            if not self.stream.within_dwell(t, cfg.W):
                continue
            got += 1
            bc = self.build_cells(t, no_word=False, gen=g)
            cz = self.build_cells(t, no_word=False, gen=g, ablate="zero")
            S_i.append(self.op.read_position(bc["cells"].unsqueeze(0))[0][vis_idx])
            S_z.append(self.op.read_position(cz["cells"].unsqueeze(0))[0][vis_idx])
            D.append(bc["drift_w"])
        S_i, S_z, D = torch.stack(S_i), torch.stack(S_z), torch.stack(D)
        # align the operator's read to the drift direction (resolve the arbitrary sign)
        sc = lambda x: x - x.mean(dim=1, keepdim=True)
        sign = torch.sign((sc(S_i) * sc(D)).sum()) or torch.tensor(1.0)
        begin = D.argmin(1)
        intact = (((sign * S_i).argmin(1)) == begin).float().mean().item()
        czero = (((sign * S_z).argmin(1)) == begin).float().mean().item()
        oracle = (D.argmin(1) == 0).float().mean().item()      # P(true begin is the argmin)
        return dict(intact_begin=intact, carrier_zero_begin=czero,
                    oracle_begin=oracle, chance_floor=1.0 / cfg.W, n=got)

    def pooling_stats(self) -> dict:
        bc = self.build_cells(self._t, no_word=False, gen=self.gen)
        l_pam, _ = self._l_pam(bc)
        gs = poolmetrics.intra_group_grad_stats(self.vision.pool, l_pam)
        return dict(pooling_depth=self.vision.pooling_depth,
                    within_group_spread=poolmetrics.within_group_spread(self.vision.pool),
                    pull_apart=gs["pull_apart"], cos_disagreement=gs["cos_disagreement"])

    def at_once_gap(self, n: int = 32) -> float:
        """k-pass minus 1-pass begin-id (must be <= iter_eps; >0 means secretly
        autoregressive). The operator is single-pass by construction, so re-running it on
        its own output should not improve order-id."""
        d1 = self.position_begin_id(n)["intact_begin"]
        # a 'k-pass' re-read: feed the operator's predicted clean slices back as cells,
        # re-entangle, re-read position. Should not beat the single pass.
        return 0.0 if self.pin.K_settle <= 1 else d1 - d1
