# Codex adapter

## Tools and delegation

`Task` means the session's delegation tool, normally `spawn_agent` or the
`collaboration` namespace. Use its actual schema. A skill cannot create a tool.
For this desktop's collaboration API, inherit the model by omitting `model`;
a deliberate override requires `fork_turns: "none"`. Include the complete task
and absolute mode path in the brief. Do not pass Cursor's `subagent_type`,
`readonly`, `environment`, `resume`, or background fields. Use supported controls.

Without a registered `poteto-agent`, use a general worker whose brief requires
[../SKILL.md](../SKILL.md) and this adapter before work. Comment Sicko's full
prompt is in [../../no-comments/references/comment-sicko.md](../../no-comments/references/comment-sicko.md).
Respect session limits on delegation. If unavailable or prohibited, work
sequentially and disclose lost independence. Never spawn external CLI agents to
bypass such a limit.

Use `update_plan` for todos when available; otherwise keep a concise task list.
Use a question tool only in a supported mode. Otherwise ask in chat for required
decisions and continue independent work. `Read`, `Bash`, and `Grep` mean the actual
file tools, native shell, and `rg` in this session.

## Skills and models

Local installation exposes `$poteto-mode`, `$setup-pstack`, and other local names.
Use a plugin's actual catalog if namespaced. Read installed companion files when
implicit invocation is disabled. Supplied `agents/openai.yaml` preserves existing
explicit-only policy; it does not register an agent type or model.

The project installer strips Claude/Cursor-only frontmatter fields from the
Codex copies. Invocation policy stays in `agents/openai.yaml`. TypeScript scope
stays in its description rather than an unsupported `paths` field.

Read `~/.agents/pstack-models.md` before role selection if it exists. The aliases
`inherit-parent` and `auto` mean omit an override. Use real model names only when
the current tool confirms them. Never guess a GPT equivalent of a Claude/Grok
slug. Unsupported roles default to inheritance, with lost diversity disclosed.
Use a separate effort field when supported, not Cursor's model suffixes. Do not
change the session model, account, or provider to satisfy a skill.

For `setup-pstack`, present unavailable defaults as `inherit-parent`, with the
reason. Keep valid configured choices. Ask for the desired budget and role
choices as setup requires. Do not write invalid slugs as accepted defaults.

## History and services

Prefer Codex chat tools for a named chat. For local history, run
[../scripts/workspace_sessions.py](../scripts/workspace_sessions.py) with
`--host codex --workspace <absolute-path>`. It selects sessions by metadata cwd
before returning paths. Normalize Windows drive letters and separators. Do not
read other workspaces' bodies or sort by UUID. The current chat may not be on disk;
report that limit.

Use available real browser, terminal, or mobile controls. Missing `deslop` becomes
a focused diff cleanup; `create-skill` maps to installed skill-creator guidance.
Never claim an unavailable skill was invoked.

Cursor Automations, cloud VMs, Project stores, and Bugbot launch controls are not
provided by these files. Use local worktrees and a local tracker where suitable.
Do not create Codex automations or chats just because a Cursor recipe mentions
them. Use native services only for an authorized user request. Existing GitHub
comments remain reviewable. If event subscriptions are absent, report the missing
supervision; do not promise monitoring after the turn ends.
