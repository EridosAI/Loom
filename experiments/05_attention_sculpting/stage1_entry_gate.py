"""§L DEPLOYED ENTRY GATE — gate step 3 (criterion-led; matched bar), + Step-0(c) on PASS.

Runs THE deployed rig (SculptLoop, revival config = the defaults, canonical seed) and takes
the entry read exactly as the matched-bar reference was constructed (bar and read = the same
function on matched geometry, INCLUDING the time axis):

  * channel column every eval window (100 waves): revival.partition_read (ruler v2) on
    word-cued evocations (evoke_vision associative=True), labels = category (b % n_category),
    content = vision's LIVE clean-centre emissions. Three columns logged SEPARATELY
    (numerator / denominator / ratio) + proto_spread; occupancy (dc_track) as covariate at
    block cadence. Denominator-floor: NOT_ASSESSABLE windows are logged, never numbers
    (pin 5 — early co-development is interpretable, not wild).
  * FIRE (same constants as the reference): first 3000-block boundary where two consecutive
    block-means of the ratio are both alive (>0.1) and differ <= 0.05. NOT_ASSESSABLE
    windows count as not-alive.
  * ENTRY READ = mean of the k'=7 post-fire windows (from liveness_matched_bar.json), with
    the denominator-floor assert standing at every read window.
  * VERDICT: read >= bar (0.3128, from the artifact) -> PASS -> Step-0(c) on the SAME warmed
    loop (word-isolated evocation divergence across category vs distractor + the null-word
    ablation guard + full-context diagnostic). Read < bar -> the PRE-REGISTERED
    disambiguation: dead-pattern (ratio ~0, prototype collapse, ablation-flat) -> §10.9
    trigger assessment; depressed-but-alive (materially >0, structured, ablation-sensitive,
    sub-bar) -> reference-error assessment under the bars convention.
  * CAP 112500 waves [RECONCILE from liveness_matched_bar.json: (max onset 69000 + read tail
    6000) x 1.5; clock caveat recorded there]. Never fires by cap -> NON-CONVERGENCE FINDING
    (neither pass nor fail); report, do not rescue.

Output: stage1_entry_gate.json — surfaced at REVIEW GATE 4 together with (a)/(b) (re-run on
the run commit) and (c). Nothing here re-litigates the bar: it was derived once, pre-read,
on the aligned reference.
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

import torch

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[1] / "experiments" / "04_stage0_mvp"))

import constants                                             # noqa: E402  (exp04)
import exp07_config as C                                     # noqa: E402
from revival import partition_read, dynamics_panel           # noqa: E402
from sculpt_config import SculptConfig                       # noqa: E402
from sculpt_loop import SculptLoop                           # noqa: E402
from conflict_validity import _evocation_divergence, CONFLICT_PARAMS   # noqa: E402

OUT = _HERE / "stage1_entry_gate.json"

# --- everything below is [RECONCILE]'d from the matched-bar artifact; never re-typed ---
_MB = json.loads((_HERE / "liveness_matched_bar.json").read_text())
BAR = _MB["bar"]                                  # 0.3128
K_PRIME = _MB["k_prime"]                          # 7 eval-windows
CAP = _MB["entry_cap_derived"]                    # 112500 waves
AL = _MB["alignment"]
WINDOW, BLOCK = AL["window"], AL["block"]         # 100 / 3000
FLAT_EPS, ALIVE_SPLIT = AL["flat_eps"], AL["alive_split"]   # 0.05 / 0.1


class EntryGate:
    def __init__(self, seed: int = 0):
        self.cfg = SculptConfig(seed=seed)        # the deployed rig = the revival defaults
        self.pin = constants.PinnedConstants()
        self.loop = SculptLoop(self.cfg, self.pin)
        cfg = self.cfg
        self.a_idx = torch.arange(cfg.n_A).repeat_interleave(cfg.n_B)
        self.b_idx = torch.arange(cfg.n_B).repeat(cfg.n_A)
        self.labels = self.b_idx % cfg.n_category
        self.columns = []                          # (t, numerator, denominator, ratio|None, proto)

    @torch.no_grad()
    def _read_window(self) -> dict:
        e = self.loop.evoke_vision(self.a_idx, self.b_idx, associative=True)
        content = self.loop.vision.emit(self.loop.stim.raw_clean(self.a_idx, self.b_idx))
        return partition_read(e, self.labels, content)

    @torch.no_grad()
    def _ablated_ratio(self) -> float | None:
        e = self.loop.evoke_vision(self.a_idx, self.b_idx, associative=True, null_word=True)
        content = self.loop.vision.emit(self.loop.stim.raw_clean(self.a_idx, self.b_idx))
        return partition_read(e, self.labels, content)["d_diff"]

    def _fired(self) -> int | None:
        """The reference's fire rule on the live ratio column (None ratios = not alive)."""
        cols = {t: r for t, _, _, r, _ in self.columns}
        ts = sorted(cols)
        if not ts or ts[-1] - ts[0] < 2 * BLOCK:
            return None
        t = ts[-1]                                 # only the newest boundary needs checking
        if t % BLOCK != 0:
            return None
        b1 = [cols[s] for s in ts if t - 2 * BLOCK < s <= t - BLOCK]
        b2 = [cols[s] for s in ts if t - BLOCK < s <= t]
        if not b1 or not b2 or any(v is None for v in b1 + b2):
            return None
        m1, m2 = statistics.mean(b1), statistics.mean(b2)
        if m1 > ALIVE_SPLIT and m2 > ALIVE_SPLIT and abs(m2 - m1) <= FLAT_EPS:
            return t
        return None

    def run(self) -> dict:
        loop, cfg = self.loop, self.cfg
        fire, occupancy = None, {}
        t = 0
        while t < CAP:
            loop.step(no_word=False)
            t += 1
            if t % WINDOW == 0:
                r = self._read_window()
                self.columns.append((t, r["cross_dist_raw"], r["content_denom"],
                                     r["d_diff"], loop.pam_proto_spread()))
                if t % BLOCK == 0:
                    occupancy[str(t)] = loop.dc_track(cfg.n_eval)
                    fire = self._fired()
                    if fire is not None:
                        break
        rec = dict(commit_hash=C.commit_hash(), spec_hash=C.spec_hash(), seed=cfg.seed,
                   bar=BAR, k_prime=K_PRIME, cap=CAP, fire=fire,
                   reconcile_source="liveness_matched_bar.json")

        if fire is None:
            rec.update(verdict="NON_CONVERGENCE",
                       note="channel column never fired the flatness criterion by cap — a "
                            "FINDING (neither pass nor fail); report, do not rescue.")
            return self._finish(rec, occupancy)

        # entry read = k' post-fire windows; denominator-floor assert standing at each.
        # (c) divergence recorded per read window too (the windowed-estimator sweep: no point
        # reads anywhere; (c)'s scalar = mean over the SAME k' windows the entry read uses).
        reads, div_windows = [], []
        for _ in range(K_PRIME):
            for _ in range(WINDOW):
                loop.step(no_word=False)
                t += 1
            r = self._read_window()
            assert r["status"] == "assessed", f"denominator floor violated at read window t={t}"
            self.columns.append((t, r["cross_dist_raw"], r["content_denom"],
                                 r["d_diff"], loop.pam_proto_spread()))
            reads.append(r["d_diff"])
            div_windows.append(_evocation_divergence(loop, associative=True))
        entry_read = statistics.mean(reads)
        abl = self._ablated_ratio()
        proto = loop.pam_proto_spread()
        rec.update(entry_read=round(entry_read, 4), read_windows=[round(x, 4) for x in reads],
                   read_span=[fire + WINDOW, t], d_ablated=(round(abl, 4) if abl is not None else None),
                   proto_spread_at_read=round(proto, 4),
                   ablation_sensitive=bool(abl is not None and abl < 0.05 and entry_read > 0.1))

        if entry_read >= BAR:
            rec["verdict"] = "PASS"
            # ---- Step-0(c) on the SAME warmed loop, WINDOWED over the k' read windows ----
            cat = statistics.mean(d["category_divergence"] for d in div_windows)
            dist = statistics.mean(d["distractor_divergence"] for d in div_windows)
            full = _evocation_divergence(loop, associative=False)
            share = cat / (cat + dist + 1e-9)
            alive = bool((cat + dist) > CONFLICT_PARAMS["channel_alive_floor"])
            c_pass = bool(alive and share >= 0.5 + CONFLICT_PARAMS["divergence_sep"] and cat > dist)
            rec["STEP0C"] = dict(category_divergence=cat, distractor_divergence=dist,
                                 category_share=share, channel_alive=alive, PASS=c_pass,
                                 n_windows=len(div_windows),
                                 full_context_diagnostic=full,
                                 note="WINDOWED over the k' entry-read windows, on the warmed "
                                      "post-entry loop (point reads barred, 2026-07-02 sweep)")
        else:
            dead_pattern = bool(entry_read < 0.1 and proto < 0.3
                                and (abl is None or abl < 0.05))
            rec["verdict"] = "FAIL"
            rec["disambiguation"] = (
                "DEAD_PATTERN -> §10.9 trigger assessment (ratio ~0, prototype collapse, "
                "ablation-flat: the channel cannot carry signal)" if dead_pattern else
                "DEPRESSED_BUT_ALIVE -> reference-error assessment under the bars convention "
                "(materially >0, structured, ablation-sensitive, sub-bar: a RULER question, "
                "not a capacity trigger)")
        return self._finish(rec, occupancy)

    def _finish(self, rec: dict, occupancy: dict) -> dict:
        ts = [c[0] for c in self.columns]
        # the standing dynamics panel: scalar and panel always travel together
        rec["dynamics_panel"] = dict(
            ratio=dynamics_panel(ts, [c[3] for c in self.columns]),
            numerator=dynamics_panel(ts, [c[1] for c in self.columns]),
            denominator=dynamics_panel(ts, [c[2] for c in self.columns]),
            proto_spread=dynamics_panel(ts, [c[4] for c in self.columns]))
        rec["columns"] = [dict(t=t, numerator=float(f"{n:.6g}"), denominator=float(f"{d:.6g}"),
                               ratio=(round(r, 4) if r is not None else None),
                               proto=round(p, 4))
                          for t, n, d, r, p in self.columns[-200:]]   # tail; full series big
        rec["columns_note"] = "last 200 eval windows; full three-column series in dynamics_panel"
        rec["occupancy_covariate"] = occupancy
        OUT.write_text(json.dumps(rec, indent=2))
        return rec


def main():
    torch.set_num_threads(max(2, torch.get_num_threads() or 4))
    rec = EntryGate().run()
    print(f"ENTRY GATE: verdict={rec['verdict']}  fire={rec['fire']}  "
          f"read={rec.get('entry_read')}  bar={rec['bar']}  k'={rec['k_prime']}  cap={rec['cap']}")
    if "STEP0C" in rec:
        c = rec["STEP0C"]
        print(f"STEP0C: cat_div={c['category_divergence']:.4g}  dist_div={c['distractor_divergence']:.4g}  "
              f"share={c['category_share']:.3f}  alive={c['channel_alive']}  PASS={c['PASS']}")
    if "disambiguation" in rec:
        print("DISAMBIGUATION:", rec["disambiguation"])
    print(f"-> {OUT}")


if __name__ == "__main__":
    main()
