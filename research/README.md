# Loom research workspace

`research/` is the active research/Workbench/result/analysis layer. It does not override canonical files. Canonical Developmental Ecology material stays in its established repository paths, including `docs/developmental_ecology/`. `EXP1-21/` remains historical preserved evidence. Each result/report keeps its own status; Workbench synthesis is useful orientation and is not independent scientific authority.

Prefer current committed canonical documents and verified artifacts, then `00_LOOM_CURRENT_STATE`, later verified experimental/analysis artifacts, Workbench synthesis, and dated retrospectives/history. Distinguish OBSERVED EVIDENCE, JASON-ACCEPTED DECISIONS, PROPOSALS and UNRESOLVED INTERPRETATIONS. Preserve unresolved contradictions; no conclusion changed through this migration.

| Durable output | Location |
|---|---|
| Live research synthesis | `research/workbench/` |
| Result reports | `research/results/<date>/<package>/` |
| Passive analysis | `research/analyses/<date>/<package>/` |
| Session records | `research/sessions/` |
| Major raw/private/archive custody | `research_artifacts_local/` |
| Canonical design doctrine | Existing canonical paths, only with explicit authority |

The prepared worktree is `C:\Users\Jason\Desktop\Eridos\Loom-research-workspace-20261001`, branch `restructure/research-workspace-in-repo-20261001`, based on fetched `origin/main` `7ada2b300fa12a26b0daf40b1fa5682243ff6625`. Existing Build worktrees/branches remain separate. The dirty primary checkout was not used for migration. This is a repository worktree; future chats should open a worktree containing this research layer and follow its local guidance rather than authoring durable outputs in the old `.codex` project mirror.

Start with [the package index](PACKAGE_INDEX.md), [Workbench map](workbench/00_RESEARCH_MAP.md), [workspace status](workbench/01_WORKSPACE_STATUS.md), [open questions](workbench/02_OPEN_QUESTIONS.md), and [Behavioural Watchlist](workbench/30_REVIEWS/BEHAVIOURAL_DEVELOPMENT_WATCHLIST.md). Update the Workbench after major experimental, design or analysis milestones through a bounded integration.

Heavy evidence is stored locally under `research_artifacts_local/`; the tracked root `.gitignore` and retained common Git `info/exclude` exclude that root; never force-add custody. Small tracked package-local manifests retain physical path, archive member, original relative/absolute source, size, SHA-256, runtime/config references and original scientific status. Original native M1/Founder trees are represented by verified complete archives. Separate saved derived-analysis records are supplemental custody, not a second expanded native tree. Archive members were streamed and hashed without extraction or execution. `!/` separates nested ZIP member chains.

Active Workbench notes and small source files necessary for navigation are under `research/workbench/`. Heavy/private/archive custody is under `research_artifacts_local/workbench_custody/` or reused through another verified local archive, with original relative paths indexed in the [custody map](workbench/WORKBENCH_CUSTODY_INDEX_20261001.csv.gz). The previous source was `C:\Users\Jason\Documents\Obsidian\All Projects\Projects\Eridos\Experiments\Loom\Loom Research Workbench`. Historical absolute paths and source catalog identity rows remain provenance; the migration map provides current access. Workbench private-source ignore rules remain in force.

The complete [path map](MIGRATION_PATH_MAP_20261001.csv.gz) is compressed to keep the tracked manifest small. An identical uncompressed convenience CSV is present locally and excluded by the tracked root guard as well as the local guard. Both are organizational manifests, not regenerated scientific evidence. See [the migration report](REPO_WORKSPACE_MIGRATION_REPORT_20261001.md) for validation and limitations.

ChatGPT/Codex may keep metadata, temporary worktrees and caches under `.codex`; durable Loom outputs now belong in the repository. No original was deleted. Two local migration commits are authorized for review after verification. No simulation, continuation, scientific regeneration, push, merge or PR is authorized or performed. See [the final custody gate and reduction record](sessions/2026-10-01-tracked-payload-review/README.md).
