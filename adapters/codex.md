# Codex adapter

Read [common.md](common.md). Task means the live collaboration or spawn_agent tool.
If poteto-agent is not registered, use a general delegate whose brief requires
reading the installed poteto-mode SKILL.md. Pass absolute paths. Omit unsupported
Cursor subagent_type, readonly, environment and background parameters. A read-only
brief restricts behavior; it does not prove sandbox isolation.

Use the real file, terminal, search, plan and question tools. Do not launch other
CLI agents to bypass unavailable delegation. Authorized worktrees give filesystem
isolation, not cloud services.

Read `~/.agents/pstack-models.md` if present before selecting role models. auto or
inherit-parent means omit an override. Use only models and reasoning effort the
current API supports. If an override requires fork_turns, use its accepted value
and include the full task in the brief.

For setup-pstack, replace every read/write of `~/.cursor/rules/pstack-models.mdc`
in steps 2, 5 and 6 with `~/.agents/pstack-models.md`. Write plain Markdown without
Cursor frontmatter. Read it explicitly on later tasks; this is not an auto-loaded
Cursor rule. Use real model IDs and separate supported effort parameters, not
guessed model slug suffixes.

Generated agents/openai.yaml preserves explicit-only policy when the source says
disable-model-invocation. Do not enable every skill implicitly. Cursor slash
syntax maps to a supported skill mechanism or installed file reading.

For local transcripts use [workspace_sessions.py](tools/workspace_sessions.py)
with `--host codex --workspace <absolute-path>`. Read only the selected project.
Use available app controls; do not claim cursor-team-kit or cloud services ran.
