# Git Commits and Collaboration

## Repository and Change Ownership

Before editing, verify the repository, branch, working tree, and existing staged changes. Do not guess ownership by filename, author, or timestamp. Investigate only what affects this task and its commit decision; preserve unrelated changes and do not require a clean tree. Follow the project's branch conventions. Do not automatically stash, reset, or overwrite other people's work.

Use one completed feature or one round of feedback changes as the commit unit. Deliver related code, tests, configuration, documentation, and notes together. Do not commit by tool step, file, or TDD cycle, or include unrelated cleanup. For multiple independently understandable and verifiable goals, you may suggest separate commits and explain the boundary. Do not separate materials needed to understand the change. Save records promptly; do not wait for a commit.

## Staging and Parallel Work

Stage only changes authorized in this round, preferably by explicit paths or safely separable hunks. Do not stage everything by default. Before committing, inspect the entire actual index. Coordinate first if it contains pre-existing changes that are unrelated or whose ownership is unclear; do not unstage, restage, or include them unilaterally. Staging this round's paths does not exclude other content already in the index. If edits in the same file cannot be safely separated, pause only the affected staging or commit; continue independent work without clearing the shared state.

Prefer separate working directories for parallel tasks, with clear file, index, and commit ownership. A branch alone does not isolate a shared checkout. Follow environment and project conventions for isolation; do not automatically create a worktree. When sharing is necessary, coordinate writes and avoid concurrent operations on the same files, index, or branch. If relevant content changes, recheck scope, review, and whether earlier conclusions still apply. Do not automatically stash or clear the tree.

## Checks Before and After Committing

Review the complete staged diff and file list, including unexpected additions, deletions, and renames. Exclude unrelated temporary files, credentials, and generated noise. Run necessary checks required by the project and address failures; do not skip hooks to get a passing result. Reuse results that remain applicable; do not rerun the full suite mechanically for every commit.

Checks must correspond to the actual index version. If the working tree differs from the index in ways that could affect the conclusion, run the relevant checks for the indexed version. Explain important gaps before proceeding; do not clean a shared tree just to create test conditions. Passing tests on the working tree do not automatically prove the staged version passes.

After committing, verify the commit identifier, message, and actual file scope. Accurately report any remaining changes; do not claim the working tree is necessarily clean.

## Commit Message Format

Use `type(scope): imperative subject`. The scope is optional; write the subject and any body in English and describe the main change specifically. Avoid vague messages such as `update code` or `fix stuff`.

| Type | Use |
| --- | --- |
| `feat` | New capability |
| `fix` | Bug fix |
| `docs` | Documentation change |
| `refactor` | Structural change that preserves behavior |
| `test` | Add or adjust tests |
| `perf` | Performance improvement |
| `build` / `ci` | Build / continuous integration |
| `chore` | Other maintenance |
| `revert` | Revert an existing commit |

Choose a type based on the primary purpose; do not change it just because tests or docs are included. Use a stable feature or subsystem name for scope; it does not have to match a directory. Add rationale, trade-offs, and verification in the body as needed; do not repeat the full diff. Add `!` only for a breaking change, and explain what breaks and any necessary migration. Existing repository conventions and automated validation take precedence. Do not invent unnecessary hard limits on message length. For example: `fix(import): preserve checkpoints after interrupted uploads`.

## Confirmation and Authorization

By default, after making and verifying changes and showing them, ask whether this round is complete and ready for a local commit. If the user continues with feedback, keep working. If the user has explicitly requested a commit for this round or confirmed the displayed scope, perform the necessary checks and commit without asking again. General implementation authorization does not imply commit authorization.

If the scope materially expands, a key behavior changes, or independent work is added after confirmation, explain the change; do not carry the old authorization over automatically. Mechanical checks do not require additional approval. Make ordinary corrections within the original goal autonomously and explain them; decide whether renewed confirmation is needed based on whether the displayed scope materially changed.

A local commit does not authorize push, PR, merge, or release. Complete explicitly combined requests within their stated authorization without asking step by step. Before each operation, verify the branch, remote, and actual contents; do not infer authorization for other targets.

By default, create a new commit. Do not automatically amend, rebase shared history, force-push, or use a destructive reset. Handle history changes, conflict resolution, and reverts according to the explicit task and project conventions. Explain the impact and obtain the relevant decision when other people's work or unrecoverable content is involved. Saving a document or marking work completed does not authorize these operations.
