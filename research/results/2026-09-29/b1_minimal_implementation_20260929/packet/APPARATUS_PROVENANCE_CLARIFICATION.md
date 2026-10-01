# B1 apparatus provenance clarification — 2026-09-29

**Verified from local Git objects and preserved public administrative receipts. No simulation or sealed evaluator inspection.** This clarification was reported to Jason before preparing the new design.

The last independently reviewed operator checkpoint remains **`352f73fffa6d9781eae8aa38e708a9a05669588f`**. `b684912eaf7811cd318ee94c77172aca790f3a0d` is a later, locally verified presentation derivative. It is not another name for `352f73ff`, and no new independent review disposition is claimed.

| Commit | Exact parent | Purpose |
|---|---|---|
| `1060a17e3dd14c6361f6f15c95bb58fad3110ffc` | `352f73fffa6d9781eae8aa38e708a9a05669588f` | Compact the operator layout following Jason's scrolling complaint and approval of the preview. |
| `b684912eaf7811cd318ee94c77172aca790f3a0d` | `1060a17e3dd14c6361f6f15c95bb58fad3110ffc` | Colour each coordinate label to match its existing trace, as Jason requested. |

**Every production change between `352f73ff` and `b684912e`:** one file, `developmental_ecology/loom_commissioning/sensor.html`, changed only within its CSS `<style>` block. The complete production diff accompanies this report as `PRODUCTION_DIFF_352f_to_b684.txt`.

- `1060a17e`: compact font sizes, padding and margins; a four-column wide / two-column narrower / one-column mobile panel layout; smaller charts; compact status/E/I and actuator layout; internal scrolling for command/note history. The underlying DOM, text, data and JavaScript were unchanged.
- `b684912e`: 29 coordinate-label selectors assign the existing trace HSL colours, using index × 360 / modality width, 55% saturation and 40% lightness. No separate key was added. Numeric-value colours and trace rendering were unchanged.

The entire HTML outside the style block is byte-identical across all three commits. There are no changes to Python, P, configuration, body/world/sensor laws, controller behavior, command holds, lifecycle, recorder, dependency locks or JavaScript in this interval. Nine additional changed files are documentation and verification artifacts, enumerated in `PROVENANCE_BYTE_PROOF.json`: four under `p_b1_compact_layout_20260927`, five under `p_b1_coordinate_colours_20260929`.

| HTML version | SHA-256 |
|---|---|
| `352f73ff` | `806221de1db825a72eaf8e5533553ff97cff11d30c4a7251cf517a128bcbcf9b` |
| `1060a17e` | `0b322ff6e4291e5cc68076002e3e37faecb178e5609eab858721abe6fbdc3a95` |
| `b684912e` | `3742b5989c0e3dd7d11e39d4376699dc3d3dd88918519a0bbe380073eb1c75b3` |

**Did the human FULL-RAW execution use a later commit? Yes.** The retained 20.2-second / 202-command record ran at `b684912e`, with a separately regenerated and authorized identity. Post-`352f73ff` source was required to reproduce that run's exact approved presentation and runtime hashes. It was not required to supply a missing simulation or controller capability. These distinctions matter because presentation affected human operation even though the underlying dynamics did not change.

| Preserved FULL-RAW attempt | Apparatus | Recorded exposure | Public record |
|---|---|---|---|
| 1 | `352f73ff` | 0 s / 0 commands; closed for layout revision | `b1_execution_20260927/ZERO_STEP_CLOSURE_AND_LAYOUT_AUTHORIZATION.json` |
| 2 | `1060a17e` | 0 s / 0 commands; wall allowance expired | `b1_execution_20260929/EXPIRED_ZERO_STEP_RESTART_REQUEST.json` |
| 3 | `1060a17e` | 1.2 s / 12 commands; closed for label colours | `b1_execution_20260929_restart_01/PREFIX_CLOSURE_AND_COLOUR_LABEL_AUTHORIZATION.json` |
| 4 | `b684912e` | 20.2 s / 202 human commands; ended before 30 s | `b1_execution_20260929_colours_01/FULL_RAW_OPERATOR_COMPLETION.json` |

Attempt 4 binds authority `936cd43b20c84378c3d7a2e99825fb87029c873872db6e504279ee7a931ce901` and run-manifest SHA-256 `85c2bbaaebb693db170e4bf8b6d9f241cd075a00aad8de36a180428712a903d1`. This is historical provenance, not a renewed authority. Its private stop cause and interaction outcome were not inspected.

The original `2026-09-26-B1-regenerated-352f73ff` packet, subsequent `2026-09-27-B1-compact-1060a17e` packet and `2026-09-29-B1-colour-labels-b684912e` packet are separate preserved artifacts. The earlier report that the first regenerated packet used `352f73ff` does not identify the later execution. v0.1's bare “current apparatus” wording omitted this distinction; this report supplies it without rewriting those artifacts.

The existing compact-layout and colour reviews record detached component/browser checks using manufactured envelopes and disclosed, closed positive-control material. They explicitly claim local verification, not independent review. This task rechecked Git ancestry, changed paths and byte identity; it did not rerun those tests.

P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`. The current inspected worktree is `worktrees/loom-p-b1-coordinate-colours-20260929`, branch `build/p-b1-coordinate-colours-20260929-01a0c405`, HEAD `b684912eaf7811cd318ee94c77172aca790f3a0d`. It remains clean. No new source checkpoint is created by this design task.
