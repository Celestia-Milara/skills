# Claude Code adapter

## Tools, skills, and agents

`Task` means `Agent`; `generalPurpose` means `general-purpose`. Use the live schema.
Drop Cursor's `readonly`, `environment`, `cloud_base_branch`, and
`file_attachments`. Put read-only limits and paths in the brief. Use the host's
worktree option when available. A local worktree is not a cloud VM.

Use registered `poteto-agent` and `comment-sicko` roles when present. Plugins
namespace them as `pstack:poteto-agent` and `pstack:comment-sicko`; project installs
use unprefixed names. Otherwise use `general-purpose` with the full prompt and
absolute mode path. Workers read the mode and adapter first. Do not assume a
restricted worker retains all MCP tools. Respect session delegation limits.

Use `TodoWrite`, `AskUserQuestion`, resume, and background controls only when the
live schema supports them. In print mode questions may be absent; ask in the reply
for a required decision and continue independent work.

Project/user skills expose `/poteto-mode`; a plugin exposes `/pstack:poteto-mode`.
Use the actual catalog. Most skills have `disable-model-invocation: true`, so
internal `Skill` calls can be rejected. Read installed companion files instead.
Preserve explicit-only policy and Claude Code's bundled `/code-review`.

The project installer removes Cursor's `paths` field so the TypeScript skill
remains explicitly selectable without an already-loaded matching file. Its
description retains the TypeScript scope. Other invocation policy is unchanged.

## Models

Read `~/.claude/rules/pstack-models.md` if not already loaded. The mirror's legacy
fallback is `~/.agents/pstack-models.md`. Explicit setup writes the Claude rules
file without `.mdc` frontmatter, not Cursor rules or `CLAUDE.md`.

Use only aliases the live Agent schema supports. Map a Cursor Claude slug to a
supported same-family alias, with effort in a supported separate field. Drop
`-fast`. Grok/GPT roles inherit the session when unavailable. Never silently call
that cross-family review. `auto` and `inherit-parent` mean no override.

Setup must show supported choices and inheritance, keep valid configured choices,
and never write unavailable Cursor defaults or change the account/provider.

## History, paths, and services

Use a session path supplied by the host when available. Otherwise run
[../scripts/workspace_sessions.py](../scripts/workspace_sessions.py) with
`--host claude-code --workspace <absolute-path>`. It selects the workspace project
directory, then verifies recorded cwd before returning paths. Do not mine other
projects. Remote or resumed sessions may be stored elsewhere; report the gap.

Use native shell syntax on Windows and supplied Python helpers. Preserve user
`CLAUDE.md` content. Installation does not rewrite project instruction files.

Use available browser/CLI control instead of missing `control-ui`/`control-cli`.
A focused diff cleanup replaces missing `deslop`. Use installed skill-creator
guidance for authoring, or the skill format when unavailable. State substitutions.

Skip unavailable Cursor Automations, cloud dashboards, Project stores, and Bugbot
launch steps with a concrete explanation. Existing PR comments remain reviewable.
Use available forge tools for authorized actions. Keep program state locally and
report absent event subscriptions instead of promising unsupported supervision.
