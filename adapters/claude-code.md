# Claude Code user-skill adapter

Read [common.md](common.md) and the [official Claude Code adapter](../pstack/docs/harness/claude-code.md).
Apply these installation-specific overrides after the official tool mappings.

This is a user-skill or project-skill install, not a marketplace plugin. Invoke
`/poteto-mode` and `/setup-pstack`, without a `pstack:` namespace. Named agents are
`poteto-agent` and `comment-sicko`, without a plugin prefix. Their definitions are
in the local agents directory. Read another skill's SKILL.md if the Skill tool
refuses programmatic invocation.

Model rules remain at `~/.claude/rules/pstack-models.md`. Setup must use model and
effort values offered by this session's Agent schema. The official table does not
prove that this runtime exposes a model, field or feature. Omit unknown fields.
Do not pass Cursor is_background or readonly parameters to unsupported tools.
