# pstack in Codex

The root library's installer exposes 58 pstack skills and five supplementary
skills in `.agents/skills/`, with the complete bundle in `.agents/pstack/`.
Use `$poteto-mode` in a new session.

The [Codex adapter](../../skills/poteto-mode/references/codex.md) owns operational
mappings. Every skill loads the [host router](../../skills/poteto-mode/references/host.md),
including direct leaf invocations. Roles use `~/.agents/pstack-models.md`;
installation does not choose models or write user configuration.

General workers use bundled prompts, so custom agent registration is unnecessary.
Missing model families and services are disclosed rather than counted as passes.

Official references checked 2026-11-03:

- [Skill discovery and policy](https://learn.chatgpt.com/docs/build-skills).
- [Plugin format](https://developers.openai.com/plugins/build/plugins).
- [Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents).
