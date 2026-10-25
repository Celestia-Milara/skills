# Agent Guidance Integration

[AGENTS.md](../AGENTS.md) is the active entry point for maintaining this library. [AGENTS.template.md](AGENTS.template.md) is the reusable entry template for other projects. This directory maintains the common operating rules; it is not a standalone skill. `design/` stores local discussion history for this library and is not an installation dependency.

## Integration steps

1. Copy [AGENTS.template.md](AGENTS.template.md), rather than this library's root entry, to the target project's instruction entry point under a name recognized by its tool, such as `AGENTS.md` or `CLAUDE.md`. Merge into an existing entry without overwriting project constraints. Do not assume that singular `AGENT.md` is loaded automatically.
2. Copy [collaboration.md](collaboration.md), [verification.md](verification.md), and [git.md](git.md) from this directory into the target project. By default, keep them in the root-level `agent-guidance/`. The template's three guidance links are relative to its source directory: when the entry is at the project root, change `(collaboration.md)`, `(verification.md)`, and `(git.md)` to `(agent-guidance/collaboration.md)`, `(agent-guidance/verification.md)`, and `(agent-guidance/git.md)`. If using another layout, resolve links from each destination file.
3. Configure the skills actually used, and update the skill links in `collaboration.md` and `verification.md` to point to real, readable entry points. The relative paths in this library are valid only in its current layout. When distributing a skill, retain the entire package and its license rather than copying only `SKILL.md`. These integration instructions do not perform installation.
4. Replace project-material placeholders with links to real Markdown files. Fill in the actual constraints, check commands, and environment sources; remove unused placeholders rather than creating documents just to fill out the form. For architecture navigation, prefer links to existing overviews or subsystem documentation, and follow the entry-point guidance to read them. A new architecture page or embedded diagram is not required; follow maintenance-docs for diagram ownership and maintenance.
5. Record the source revision and project customizations as described below. Check all destination links, including skill references. Once the entry point leads to the companion rules, skill methods, and project materials, remove integration comments and unused placeholders. When multiple tools share the guidance, maintain one project source and reference it through mechanisms supported by each tool; avoid copying the complete rules into multiple files.

Ordinary Markdown links provide navigation but do not guarantee that files are automatically loaded into context; the entry point specifies when to read the relevant material. Reuse verified context that still applies instead of rereading every file for each operation.

### Skill links in common layouts

Resolve paths from the copied guidance file, not the project root. For a file in root-level `agent-guidance/`, these are example targets:

| Installation | Example target for `decision-notes` |
| --- | --- |
| Codex project packages | `../.agents/skills/decision-notes/SKILL.md` |
| Claude Code project packages | `../.claude/skills/decision-notes/SKILL.md` |
| Personal packages | Use the host's actual readable installed location; do not assume `~` expands in Markdown links |

Apply the same adjustment to all method links. Verify targets and preserve each complete package. A skill name can aid discovery, but it does not replace a readable-source fallback when invocation is unavailable.

### Host loading and optional history

Keep one owning project instruction source. Preserve an existing `CLAUDE.md` when integrating shared guidance. On supported Claude Code versions, direct `AGENTS.md` loading depends on the file combination and Project instructions setting. An existing `CLAUDE.md` can import a neighboring shared source with `@AGENTS.md`. The [official loading rules](https://code.claude.com/docs/en/memory#agentsmd) describe version and configuration limits; do not infer loading from a filename alone.

Keep conditional history behind a task-specific reading trigger. Do not add a mandatory import of an optional lesson file. If the file does not exist, continue; if access fails, state the gap. Reuse the existing notes, subsystem, or verification source when it already owns the evidence. The `decision-notes` method owns candidate assessment and promotion.

Verify the chosen layout in a fresh session using the [validation procedure](validation.md#host-loading-and-behavior-checks). Record the host version, settings relevant to loading, actual sources read, and observed action. A discovered skill name or instruction filename alone does not prove behavioral reuse.

## Ownership

Keep the entry point focused on project sources, task-specific reading triggers, and concrete constraints needed before choosing an action. Apply the same standard to companion guidance: retain deliberate engineering conventions and rules addressing demonstrated failures; omit generic coaching about autonomy, clarification, or planning. Link to skill methods instead of restating their procedures. Moving generic prose out of the entry point does not reduce the total instruction burden.

| Content | Source of truth |
| --- | --- |
| Reusable entry structure and reading triggers | [AGENTS.template.md](AGENTS.template.md) |
| Effective constraints, reading timing, and real project resources | Each project's actual Agent entry point |
| Document ownership, historical decision search triggers, and method navigation | [collaboration.md](collaboration.md) |
| Behavior verification, check evidence, review, and delivery coordination | [verification.md](verification.md) |
| Change ownership, indexes, parallel work, commit messages, and authorization | [git.md](git.md) |
| Specific methods for interviews, saving designs, engineering documentation, decisions, handoffs, TDD, and reviews | Their respective skill packages |

When rules change, update their owning source; in other locations, update only the activation guidance and links. Skills remain independently installable and retain the minimum boundaries needed for standalone use. Single ownership avoids competing full procedures and contradictory facts; it does not require removing those standalone safeguards.

## Source Versions and Project Copies

This library owns the reusable template and common guidance. Each consuming project owns its installed copy, real resource paths, check commands, skill locations, and project-specific constraints. This library's root `AGENTS.md` is itself a project entry: when changing a baseline rule, update the template or owning companion first, then reconcile this entry within the same change.

Keep guidance copies in the target project so their effective contents can be reviewed and versioned with the project. Do not make projects depend on a live global guidance file or automatically overwrite their copies when this library changes. A source update becomes effective in another project only when that project's update is adopted; this preserves deliberate project customizations and makes changes reviewable.

At initial integration, record the source repository and exact commit or tag, copied guidance files, and intentional deviations in an existing project maintenance document or a short provenance comment in the entry point. If copying an uncommitted source, identify it as a local snapshot and retain its contents or patch; do not label it as the clean commit version. Record separately installed skill versions in their existing installation records where available; a guidance revision does not establish skill versions.

For an update, compare three sources: the previously adopted library revision, the new library revision, and the current project copy. Apply relevant upstream changes while preserving project paths and customizations. Investigate conflicting constraints and resolve important choices with the user; do not silently replace either side. Check links and affected reading triggers, then update the provenance and deviations to match the adopted content. If the old revision is unavailable, compare the available files and state that the upstream-versus-local origin of differences is uncertain.

Keep reusable improvements here and project-only constraints in their project. Do not automatically propagate a project's local customization back into the library. Updates follow the project's existing authorization and Git rules; copying or recording a version adds no commit or publication authorization. This workflow requires no new synchronization tool, global installation, or mandatory documentation hierarchy.
