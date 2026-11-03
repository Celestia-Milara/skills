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
| Supplement routing, authorization handoffs, artifact roles, and plan scope | [Workflow composition](../pstack/docs/composition.md) |
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

The host router loads [workflow composition](../pstack/docs/composition.md) for
engineering and document tasks. This keeps the five supplements available without
optional project guidance. It defines when to route, how to retain authorization,
and which artifact owns each fact. Design-only work stops before implementation;
approved implementation does not need another approval. Ordinary plans use the
project's existing source and risk-based checks. The retained full-program template
and checker apply only when that format is adopted, with its required gates intact.

The packager relocates composition links to the bundled supplement copies. Host
projections resolve the composition guide through their complete resource bundle.
Source, plugin, and installed-path checks cover this route.

Windows gets a TSV logger, a metadata-scoped session selector, and a read-only Git
worktree audit. The audit deliberately does not claim remote PR or session safety.
The original Bash and TypeScript tooling remains available. Cursor Automations,
cloud services, Bugbot launch controls, and persistent event supervision are not
silently recreated in another host.

The installer copies one complete bundle and the 63 discoverable active packages.
It redirects root documentation references to that bundle. A junction-based
prototype failed Windows relative-path resolution and was replaced. It checks
collisions before writing and does not overwrite
global skills, settings, or another project's guidance. Managed updates retain
the previous complete bundle. Unrecognized or modified files need reconciliation.

## Original guidance conflict audit

The 2026-11-03 follow-up assigns Git methods to pstack. Project Git guidance now
retains only protection of existing work, authorization for destructive effects,
and the task's commit/push/PR/merge limits. The former feature-round commit unit
and new-commit default no longer compete with pstack's small ordered commits and
scoped amendments. Index and committed-version checks live in its Git playbook.

| Original guidance or supplement | Resolution with pstack |
| --- | --- |
| Git format, commit units, worktrees, and checks | pstack owns the method; project guidance links to it. Existing staged and mixed-file work stays protected. |
| Authorization reuse | Mode and the autonomy principle reuse permission for the same effects, while preserving explicit checkpoints. Workflow steps add no authority. |
| Cleanup and dirty worktrees | Remove automatic reset and throwaway-file assumptions. Untracked and ignored state needs ownership and deletion-scope evidence. |
| Verification and TDD | Compatible: practical failing-before checks, independent expectations, and risk-based evidence. Required project gates remain effective; test-first evidence does not require a separately failing delivery commit. |
| Static review and `interrogate` | Separate source-supported static findings from run-proven adversarial findings; neither substitutes for the other. |
| Decision history and session pickup | History informs continuation. Reuse applicable checks; recheck drift and missing evidence. Past notes do not grant new authority. |
| `grilling` and `grill-me` | One interview method with a wrapper; reuse settled understanding and implementation approval. No new conflict found. |
| `to-docs`, `maintenance-docs`, and collaboration guidance | Designs, progress, current facts, and rationale retain their owning sources. Saving adds no implementation or Git permission. No new conflict found. |
| `decision-notes` | Search relevant history and retain lasting rationale when warranted. No mandatory record for each task or imported workflow. |

The audit covers active project guidance and the five supplements, not retired
`legacy/` or `zh-backup/` editions. Local historical records retain rationale and
mark superseded choices; they are not runtime rules. See [validation](validation.md)
for observed host behavior and limits. Installed copies need a separate update.

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
