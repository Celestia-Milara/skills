# Host adaptation

Read the adapter for the host actually running this session:

- Codex: [codex.md](codex.md).
- Claude Code: [claude-code.md](claude-code.md).
- Cursor: use bundled Cursor names and its model configuration.
- Other hosts: use the Harness mappings in [poteto-mode](../SKILL.md).

Use the supplied host identity and live tool schema. Installed folders do not
identify the running host. Reuse an adapter already read this session. These
mappings apply to this skill, its references, and routed playbooks.

Before proposals, design, planning, implementation, review, document maintenance,
or task handoff, read [workflow composition](../../../docs/composition.md).
Reuse it within the same task. It owns supplement triggers, authorization handoffs,
artifact ownership, and plan scope for this distribution. Apply it before imported
workflow defaults. Help and model setup alone do not require those methods.

User instructions, project constraints, and tool permissions take precedence.
A workflow step does not authorize a commit, push, PR, merge, deployment, message,
data deletion, or paid job. Reuse existing task authorization without asking
again. Continue independent work when a step cannot run. Name the missing
capability and its effect on the result.

Invoke companions through a supported skill mechanism or read their installed
`SKILL.md`. Resolve siblings from this installed tree. Do not fetch a different
upstream revision to fill a local missing reference. Install complete pstack;
individual leaves can depend on the mode and principles.

When allowed, an unavailable diverse-model panel can become independent
same-model passes. Label the limitation. Same-model review is not cross-model
evidence. Leave a required independent release gate pending if its required
capability is unavailable.

Use the native shell. On Windows, use absolute native paths, quoted arguments,
and Python's `tempfile` for temporary directories. `/tmp`, Bash heredocs, `ls -t`,
`df`, and `printf` are examples, not PowerShell syntax. Prefer supplied portable
helpers. Do not mistake Windows WSL `bash.exe` for Git Bash.

The portable [worktree_audit.py](../scripts/worktree_audit.py) reports local Git
facts on Windows. It does not establish PR state, transcript activity, simulator
safety, or deletion authorization. Unknown evidence must remain unknown.
