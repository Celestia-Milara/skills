# Git Commits and Collaboration

## Change Ownership and Parallel Work

Before editing, check the repository, branch, working tree, and index; follow project branch conventions. Preserve unrelated work, including staged content. Do not infer ownership from filenames, authors, or timestamps, or automatically stash, reset, or overwrite existing changes. A clean tree is not required.

Stage authorized paths or separable hunks. If mixed edits cannot be separated safely, pause only the affected staging or commit.

Prefer separate working directories for parallel tasks; a branch alone does not isolate a shared checkout, and worktree creation follows project and environment conventions. In shared checkouts, coordinate file, index, and branch writes and recheck affected results after concurrent changes.

## Commit Checks

Before committing, review the entire staged diff and file list, including pre-existing entries; coordinate before including or altering unrelated content or content whose ownership is unclear. Exclude credentials and unrelated temporary or generated files.

Run required checks without bypassing hooks; reuse applicable results. Checks must cover the indexed version: if unstaged differences could affect results, verify that version separately and disclose remaining gaps.

After committing, verify the identifier, message, and file scope, and report remaining changes.

## Commit Organization and Format

Commit one completed feature or feedback round with its related code, tests, configuration, documentation, and notes. Split independently verifiable goals when useful, not individual files or tool steps.

Use `type(scope): imperative subject`, optional scope, and English subject and body. Choose type by primary purpose and scope by feature or subsystem. Mark breaking changes with `!` and explain the break and migration. Repository conventions and validation take precedence.

## Authorization

Implementation authorization does not include committing. Show verified changes and ask before a local commit unless an existing request authorizes that operation and scope. Reuse authorization for ordinary corrections and checks; seek renewed authorization only when scope or behavior materially exceeds it.

Local commits do not authorize push, PR, merge, or release. Execute explicitly combined requests without repeated confirmation; verify each operation's branch, remote, and contents.

Create new commits by default. History rewrites or discarding changes require authorization covering their impact. Ordinary conflict resolution follows task authorization; it does not permit overwriting others' or unclear-ownership work.
