# pstack adoption and adaptation

The user adopted pstack as the main workflow on 2026-11-03 and retained all five
supplements, including `grilling` and `grill-me`. The old eight-package source is
backed up before retiring its `tdd`, `review-code`, and `handoff` directories.

## Source ownership

| Material | Owning source |
| --- | --- |
| pstack workflows, principles, agents, resources | `pstack/`, imported from the complete portable mirror |
| Original/mirror revisions and hashes | [source-lock.json](../pstack/source-lock.json) |
| Common host boundaries and Windows substitutions | [host.md](../pstack/skills/poteto-mode/references/host.md) |
| Codex tools, role models, history, services | [Codex adapter](../pstack/skills/poteto-mode/references/codex.md) |
| Claude Code tools, roles, plugin names, history | [Claude adapter](../pstack/skills/poteto-mode/references/claude-code.md) |
| Five document/interview/decision methods | Root skill packages |
| Project-specific constraints and authorization | Each project's actual guidance |
| Installation and bundle assembly | `scripts/install.py` and `scripts/package.py` |

All imported skill entry points, including Benny's resource skills, read the host
router. Adapters are conditional references, not global instructions injected
into every task. Codex metadata preserves upstream explicit-only invocation;
Claude retains its invocation frontmatter. Codex's installed copies express
explicit-only policy in `agents/openai.yaml` and omit unsupported Claude/Cursor
header fields. Both project projections omit Cursor's `paths` field; TypeScript
scope remains in the description. Internal routing uses readable local files
when a host refuses programmatic explicit-only invocation.

## Intentional differences

The backnotprop baseline already makes many skill flows host-neutral and retains
all original file paths. Its Comment Sicko fix preserves uncertain outside-rule
comments for review instead of deleting them. Local adapters use live tool schemas,
avoid inventing model names, and distinguish same-model independent review from
cross-model evidence. They preserve project authorization over workflow defaults.

Windows gets a TSV logger, a metadata-scoped session selector, and a read-only Git
worktree audit. The audit deliberately does not claim remote PR or session safety.
On Windows, agents start the PR watcher through `bun` because Windows does not
read its `#!` line.
The original Bash and TypeScript tooling remains available. Cursor Automations,
cloud services, Bugbot launch controls, and persistent event supervision are not
silently recreated in another host.

The installer copies one complete bundle and the 63 discoverable active packages.
It redirects root documentation references to that bundle. A junction-based
prototype failed Windows relative-path resolution and was replaced. It checks
collisions before writing and does not overwrite
global skills, settings, or another project's guidance. Managed updates retain
the previous complete bundle. Unrecognized or modified files need reconciliation.

## Updating source

1. Read the locked original and mirror revisions, then inspect new upstream changes.
2. Compare old source, new source, and local adaptation. Keep complete resources.
3. Reapply relevant host changes and retain their reading triggers.
4. Update source hashes and the exact list of modified source paths.
5. Run static, portable-helper, installer, and affected host checks.
6. Record evidence in [validation](validation.md), with unrun integrations named.

Do not run the mirror's branch/push instructions in this library. A source update
does not authorize a Git commit or publication. A local install does not prove
that all hosts or project copies have adopted the change.
