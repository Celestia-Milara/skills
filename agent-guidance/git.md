# Change Protection and Git Authorization

pstack owns the Git workflow. Use [Opening a PR](../pstack/skills/poteto-mode/playbooks/opening-a-pr.md)
for worktrees, staging, commits, and PRs, and [Shipping](../pstack/skills/poteto-mode/playbooks/shipping.md)
for merge delivery. Read only the parts needed for the authorized operation.
These links do not authorize a PR or merge.

Project guidance retains three boundaries:

- Preserve user and other tasks' changes, including staged, unstaged, untracked,
  and ignored files. Unclear ownership is not permission to overwrite, discard,
  move, or include the content in a commit.
- Destructive actions and shared-history rewrites need authorization that covers
  their targets and effects. Ordinary conflict resolution does not permit loss
  of others' work. Pause only the affected operation when its scope is unclear.
- Honor the current task's commit, push, PR, merge, and release limits. Permission
  for one does not imply the others. Reuse authorization for the same operation
  and scope; do not request it again. A request to implement does not authorize
  a commit, and a request to defer commits remains in force across skill handoffs.
