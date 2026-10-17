# Agent Guidance Integration

[AGENT.example.md](../AGENT.example.md) is a template for the project entry point; this directory contains its companion operating rules and is not a standalone skill. `design/` stores discussion materials for this skill library only; it does not need to be copied into projects where the guidance is installed.

## Integration steps

1. Place the entry point under a name recognized by the target tool, such as `AGENTS.md` or `CLAUDE.md`. Keep the template name `AGENT.example.md` in this library; do not assume that singular `AGENT.md` is loaded automatically.
2. Copy [collaboration.md](collaboration.md), [verification.md](verification.md), and [git.md](git.md) from this directory into the target project. By default, keep them in the root-level `agent-guidance/`; using another existing project location is also fine, but update the entry point and relative links between files accordingly.
3. Configure the skills actually used, and update the skill links in `collaboration.md` and `verification.md` to point to real, readable entry points. The relative paths in this library are valid only in its current layout. When distributing a skill, retain the entire package and its license rather than copying only `SKILL.md`. These integration instructions do not perform installation.
4. Replace project-material placeholders with links to real Markdown files. Fill in the actual constraints, check commands, and environment sources; remove unused placeholders rather than creating documents just to fill out the form. For architecture navigation, prefer links to existing overviews or subsystem documentation, and follow the entry-point guidance to read them. A new architecture page or embedded diagram is not required; follow maintenance-docs for diagram ownership and maintenance.
5. Check all links. Once the entry point leads to the companion rules, skill methods, and project materials, remove the template comments. When multiple tools share the guidance, maintain one source and reference it through mechanisms supported by each tool; avoid copying the complete rules into multiple files.

Ordinary Markdown links provide navigation but do not guarantee that files are automatically loaded into context; the entry point specifies when to read the relevant material. Reuse verified context that still applies instead of rereading every file for each operation.

## Ownership

| Content | Source of truth |
| --- | --- |
| Persistent constraints, reading timing, and real project entry points | Project Agent entry point |
| Autonomous judgment, document ownership, historical decision search triggers, and method navigation | [collaboration.md](collaboration.md) |
| Behavior verification, check evidence, review, and delivery coordination | [verification.md](verification.md) |
| Change ownership, indexes, parallel work, commit messages, and authorization | [git.md](git.md) |
| Specific methods for interviews, saving designs, engineering documentation, decisions, handoffs, TDD, and reviews | Their respective skill packages |

When rules change, update their owning source; in other locations, update only the activation guidance and links. This file only organizes the template and companion materials; it has not been installed as active instructions for any project.
