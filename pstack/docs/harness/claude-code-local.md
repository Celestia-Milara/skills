# Local Claude Code distribution

This library's [operational adapter](../../skills/poteto-mode/references/claude-code.md)
supersedes the original tool mapping for this adapted distribution.

Project installation exposes 63 skills in `.claude/skills/` and two agents in
`.claude/agents/`. Use `/poteto-mode`. It does not alter user settings, model roles,
`CLAUDE.md`, permissions, or installed marketplace plugins.

For plugin loading, build with the root library's `scripts/package.py`, then use
`claude --plugin-dir <bundle>`. Commands and agents have the `pstack:` namespace.
Choose one installation mode to avoid duplicates.

Setup writes `~/.claude/rules/pstack-models.md` only when explicitly invoked.
The adapters retain explicit-only skills and use file reads for internal routing.

Official references checked 2026-11-03:

- [Skills](https://code.claude.com/docs/en/skills).
- [Subagents](https://code.claude.com/docs/en/sub-agents).
- [Plugins](https://code.claude.com/docs/en/plugins).
