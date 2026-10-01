# Obsidian MathJax source-formatting session

**Role:** documentation contributor. **Date:** 2026-09-20T12:56:41.063593+08:00.

Jason explicitly extended the delimiter-only formatting task to source documents. This overrides the source archive no-reformatting rule for this narrow pass. It does not change any research decision, candidate, mathematical content or authority.

Reviewed 75 Markdown files in the workbench, including source documents and authored/exported notes. Converted 82 display equations and 100 inline equations in 11 source files. Inspected all targeted mathematical spans and excluded fenced/indented code, inline code, comments and escaped delimiters. No non-mathematical escape was treated as an equation. New mathematical notation uses double-dollar display delimiters and single-dollar inline delimiters.

## Preservation and verification

Only delimiter bytes changed in the existing Markdown files. Mathematical bodies, whitespace, line endings, 40 equation tags, code, and all other content were preserved exactly. Reconstructing the originals from the replacement map reproduced the original bytes. All other existing Markdown files remained unchanged. No convertible legacy delimiters remain in the checked scope. No Obsidian renderer, scientific run or Git operation was invoked.

The verified [original-byte backup](../../90_BACKUPS/2026-09-20-mathjax-sources-694d49c2-originals.zip) contains every affected pre-conversion source and the prior catalog. [FORMATTING_RECEIPT.json](FORMATTING_RECEIPT.json) maps each live file to its prior and new SHA-256, conversion counts and backup member. The source catalog retains its existing source identity rows and appends a formatting-event pointer; prior byte fingerprints remain historical and should not be compared directly to the newly formatted files without this transformation record.

## Pre-existing difference

P already differed from its catalogued original before this pass. The backup preserves the current P bytes that were actually read; this task neither reverted nor attributed that earlier difference. The exact before/after and catalog hashes are in the receipt. All current P and R mathematical content was retained unchanged.

## Files formatted

- [LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md](../../90_SOURCES/candidate_comparison_2026-09-20/sources/participation_retention/LOOM_ASSOCIATIVE_REGULATORY_CANDIDATE_v0_1_DISCUSSION_DRAFT.md) — 33 display, 0 inline.
- [LOOM_ASSOCIATIVE_REGULATION_WORKED_CANDIDATE_v0_1.md](../../90_SOURCES/candidate_comparison_2026-09-20/sources/retention_only/LOOM_ASSOCIATIVE_REGULATION_WORKED_CANDIDATE_v0_1.md) — 19 display, 0 inline.
- [Pasted markdown(2).md](../../90_SOURCES/discussions/four_jobs_review/Pasted%20markdown%282%29.md) — 0 display, 12 inline.
- [PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1(2).md](../../90_SOURCES/input_variants/stale_landing_status/PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1%282%29.md) — 1 display, 0 inline.
- [LOOM_DEVELOPMENTAL_MECHANISM_RESEARCH_BRIEF_v0_1_DRAFT.md](../../90_SOURCES/original_research_assignment/LOOM_DEVELOPMENTAL_MECHANISM_RESEARCH_BRIEF_v0_1_DRAFT.md) — 1 display, 0 inline.
- [LOOM_MULTI_MODEL_RESEARCH_PACKET_v0_1_DRAFT.md](../../90_SOURCES/original_research_assignment/LOOM_MULTI_MODEL_RESEARCH_PACKET_v0_1_DRAFT.md) — 1 display, 0 inline.
- [BASE_WORLD_COMPLETION_v0_1.md](../../90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/BASE_WORLD_COMPLETION_v0_1.md) — 3 display, 0 inline.
- [PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1.md](../../90_SOURCES/reference_7ada2b300fa1/docs/developmental_ecology/PRIMITIVE_ORGANISM_WORLD_COUPLING_SPEC_v0_1.md) — 1 display, 0 inline.
- [Astra deep-research-report(1).md](../../90_SOURCES/research_reports/Astra%20deep-research-report%281%29.md) — 9 display, 19 inline.
- [Grok LOOM_DEVELOPMENTAL_MECHANISM_RESEARCH_REPORT_v0_1(1).md](../../90_SOURCES/research_reports/Grok%20LOOM_DEVELOPMENTAL_MECHANISM_RESEARCH_REPORT_v0_1%281%29.md) — 3 display, 69 inline.
- [LOOM_INDEPENDENT_MECHANISM_INVESTIGATION(1).md](../../90_SOURCES/research_reports/LOOM_INDEPENDENT_MECHANISM_INVESTIGATION%281%29.md) — 11 display, 0 inline.
