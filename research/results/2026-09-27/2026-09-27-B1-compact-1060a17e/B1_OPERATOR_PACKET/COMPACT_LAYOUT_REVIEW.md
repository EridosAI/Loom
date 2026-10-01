# Compact B1 operator layout — 2026-09-27

Jason requested that readings and commands fit in one screen, reviewed an offline proposal made from closed PC-HOLD attempt 002, then authorized closing the zero-step B1 attempt and preparing a layout-only revision for new exact authorization: “Yes, this works. Lets do it.” This change follows apparatus checkpoint `352f73fffa6d9781eae8aa38e708a9a05669588f`. P remains `6bc9683b54e4fa80136fe8534d7713e2a250a95f`.

Only the `<style>` block of `developmental_ecology/loom_commissioning/sensor.html` changed. It is the exact CSS of the approved preview, SHA-256 `880207be319ad796aed39fd4ab88c0d6fab00c191da9b56522548c8e1b4f5590`. Panels use four columns on wide displays and two in the tested narrow pane, smaller charts and spacing, and internally scrollable command/note histories. Narrow mobile displays retain the one-column fallback and can require scrolling. No data, precision, chart algorithm, text, DOM structure, JavaScript, command behavior, lifecycle or protocol was changed. The entire file outside the style block is byte-identical to the parent.

## Verification

- Detached existing `tests_apparatus/b1_dom_fixture.cjs`: PASS. Manufactured JavaScript envelopes only; chemistry canary rejection, 25-coordinate hidden download, 29-coordinate full download, explicit unavailable label, prepared/paused/running/ended controls, delayed response, double-click/key-repeat protection and read-only refresh. No Python Engine or Run, world or controller execution.
- Browser checks used only the closed disclosed PC-HOLD record. Both full and hidden displays fit at 777 × 722 and 1280 × 720 with no page overflow. At 777 × 722 the command button bottom was 625.792 px, with E/I at 91.198 px in the full display. All 29/25 rows and Current/Selected columns remained. Motors were disabled throughout offline checks. No B1 readings or evaluator records were used in these previews.
- `LAYOUT_BYTE_PROOF.json` inventories unchanged source, configuration and dependencies. Every P and apparatus Python source, world law, controller, clock, runtime requirement and configuration remains unchanged.

## Existing attempt and interpretation

The prior B1-FULL-RAW authority `2e338ae61dceaac3c3db0863f02cbccf0a9d98eb0842caf06c363207951e7c4c` was closed through its existing End control at exactly 0.000 simulated seconds, zero native steps and zero commands. Its complete record is preserved separately and its service stopped before editing source. This is an administrative UI correction, not a perceptual failure. The prior grant is consumed; it cannot authorize a replacement.

Jason saw permitted initial raw readings and E/I before closure. A future attempt cannot be described as a wholly unseen first exposure. Hidden state remains sealed, and the pair has not been abandoned. No evaluator feedback is released. Completed positive controls and earlier physical evidence retain their original code/interface identities and qualifications.

New case objects must bind the new HTML/apparatus identity and explicitly record this exposure and zero-step administrative history. Both cases retain their original complete physical start, laws, 30-second ceilings and recording fidelity. Preparation is not authorization to launch either case. This document claims only the layout/component checks above; it does not claim a new independent review disposition.

No B1 simulation, fresh positive control, prehistory, P learning, physical trajectory, throughput benchmark or live renderer was run for this correction. No efficacy, survival or human performance gate was applied. No push, PR, merge, Obsidian Git write or canonical research change occurred. Stop for Jason's exact launch authorization after the revised packet is prepared.
