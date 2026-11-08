# Pi adapter

Read [common.md](common.md). User skills live in `~/.pi/agent/skills/`, with this
bundle in `~/.pi/agent/pstack/`. Read companions by absolute installed path. Read
`~/.agents/pstack-models.md` if present; Pi does not automatically inject that file.
For setup-pstack steps 2, 5 and 6, read and write that path instead of Cursor's
`~/.cursor/rules/pstack-models.mdc`. Write plain Markdown without Cursor frontmatter
and read it explicitly on later tasks. Configure only real supported overrides;
otherwise use inherit-parent and report the capability limit.

Pi core does not promise subagents. Use a registered delegation extension only
when its live schema exists. Otherwise execute sequentially and report the lost
independence. Do not launch CLI agents to replace a missing tool. Models, effort
and question controls must come from the live schema, not Cursor Task fields.

Invoke an explicit skill with `/skill:poteto-mode` or `/skill:<name>` in Pi.
The source disable-model-invocation field is retained for Pi's native discovery.
Use the real read, edit, write and bash tools. MCP requires configured extensions;
reading a file does not connect a server. Respect explicit-only skills through
deliberate user requests or a supported explicit workflow route.
