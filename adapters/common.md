# Runtime contract

The pstack source is the pinned official distribution. This installed tree adds
host adapters without editing that source. Read the adapter for the actual engine.

Use the live tool schema for tools, parameters, model names and reasoning effort.
Installed folders do not establish runtime capabilities. Read companion SKILL.md
files through this installed tree if native invocation is unavailable. Resolve
dependencies relative to the file that references them.

Use the host's advertised skill entry path for execution and delegation, not the
raw SKILL.md inside the resource bundle. If reading a bundled source, return to
the corresponding `<host-root>/skills/<name>/SKILL.md` entry before running tools.
The bundle is reference material. Scripts that install dependencies or write
beside themselves run from the host entry's private scripts directory. Never use
the shared resource bundle as a mutable tool working directory.

Task instructions, project constraints and host permissions still apply. A skill
step does not grant permission to commit, publish, delete data or contact people.
Reuse authorization covering the same operation. Preserve unrelated changes.

Do not invent cloud agents, Bugbot, subscriptions or persistent supervision.
Sequential execution loses independence. Same-model delegates do not establish
cross-model evidence. Enumerate available models before setup. Unknown role
overrides inherit the current model with the limitation reported. Keep role
settings outside the shared source; do not change accounts to satisfy a workflow.

Installation does not establish Windows compatibility. Use native scripts only
when dependencies and process behavior are verified. Otherwise report the missing
capability or use a configured WSL execution path. Do not silently translate paths
or install tools.
