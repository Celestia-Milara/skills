# Engineering skills for Codex and Claude Code

A complete [pstack 0.15.36](pstack/README.md) distribution, adapted for Codex and
Claude Code, with five local skills for requirements interviews, design documents,
documentation maintenance, and decision history.

Use pstack to guide engineering work. Use the supplements when you need to examine
requirements, save a design, or retain project knowledge. They work together without
adding a second mandatory workflow.

[Install](#install) · [Start using the skills](#start-using-the-skills) ·
[Packages](#packages) · [Validation evidence](docs/validation.md) ·
[Adaptation and sources](docs/adaptation.md)

## Install

You need Python 3.10+, Git, and the host you plan to use. Some pstack workflows
also need Node, Bun, Java/TLC, or Git Bash. The installer does not install those tools.

Clone this repository and run the commands from its root:

```powershell
git clone https://github.com/Celestia-Milara/skills.git
cd skills
```

Choose user scope for a personal workflow across projects. Choose project scope
when a project needs its own version. Install only for the hosts you use.

### Personal user installation

Before installation, back up existing configuration and skills. Replace the example
output path with a new private directory outside active skill directories:

```powershell
python scripts/backup_installation.py --project . --output D:/private-backups/before-pstack
```

The backup includes linked skill files and records their original link targets.
It does not select authentication stores or chat history as backup roots. Files
inside selected skill trees, including link targets, are included. Keep the archive
private. This is a file-content backup, not an atomic snapshot or ACL backup.

For Codex, preview the destination and package count, then install:

```powershell
python scripts/install.py --host codex --scope user --dry-run
python scripts/install.py --host codex --scope user
```

For Claude Code, use:

```powershell
python scripts/install.py --host claude-code --scope user --dry-run
python scripts/install.py --host claude-code --scope user
```

The installer copies the active packages and a complete resource bundle:

| Host | Active skills | Complete bundle | Agents |
| --- | --- | --- | --- |
| Codex | `~/.agents/skills/` | `~/.agents/pstack/` | No separate agent files |
| Claude Code | `~/.claude/skills/` | `~/.claude/pstack/` | Two files in `~/.claude/agents/` |

Here, `~` means your user home directory. Start a new host session and check its
skill inventory. The default bundle exposes 63 unique skill names.

### Project installation

Replace `D:/path/to/project` with the target project's path. For Codex, run:

```powershell
python scripts/install.py --host codex --project D:/path/to/project --dry-run
python scripts/install.py --host codex --project D:/path/to/project
```

For Claude Code, use:

```powershell
python scripts/install.py --host claude-code --project D:/path/to/project --dry-run
python scripts/install.py --host claude-code --project D:/path/to/project
```

Project scope uses `<project>/.agents/` for Codex and `<project>/.claude/` for
Claude Code. Each contains the active `skills/` packages and the complete `pstack/`
bundle. Claude Code also receives two `agents/` files. Start a new session in the
target project to check discovery.

Both scopes copy files without symlink privileges. The installer redirects
package-external documentation links to the complete bundle. Keep that bundle
with the active packages.

### Existing installations

The installer preserves unrelated skills and refuses unmanaged name collisions.
It leaves host settings, model configuration, permissions, `AGENTS.md`, and
`CLAUDE.md` unchanged. Project scope does not install globally or update other projects.

To update a managed installation, add `--replace-managed` to its installation
command. Preview the update with `--dry-run` first. Updates require unchanged
managed files and retain the previous bundle and active packages under the host's
`pstack-backups/`. Preserve and reconcile modified installed files before updating.

Updates prepare the complete host projection before switching active paths. A
failed move restores the previous paths when rollback succeeds. Removed managed
skills also go into the backup. Install and retirement operations use a host-local
`.pstack-install.lock` to prevent concurrent updates. If a process is forcibly
stopped, inspect its PID, staging directory, and backup before recovering the lock.
This is not an atomic switch for readers or a power-loss recovery system. See
[adaptation details](docs/adaptation.md) for the failure boundaries.

If you move from project scope to user scope, first install and verify the user
copy from outside the project. Then archive the managed project copy:

```powershell
python scripts/install.py --host codex --scope user --retire-project D:/path/to/project --dry-run
python scripts/install.py --host codex --scope user --retire-project D:/path/to/project
```

For Claude Code, replace `codex` with `claude-code` in both commands. Retirement
requires a complete, unchanged user installation covering every project entry.
It refuses modified project packages and archives only managed files under the
project host's `pstack-backups/`. Unrelated project skills remain active. Retirement
does not install or update the user copy. Check discovery again in a fresh session.

## Start using the skills

After a user or project installation, invoke the main entry in your host:

| Host | Main workflow | Help | Host guide |
| --- | --- | --- | --- |
| Codex | `$poteto-mode` | `$poteto-help` | [Codex adapter](pstack/docs/harness/codex.md) |
| Claude Code | `/poteto-mode` | `/poteto-help` | [Claude Code adapter](pstack/docs/harness/claude-code-local.md) |

Include the task after the skill name. For example, in Codex:

```text
$poteto-mode Fix the timeout parser so that zero remains a valid timeout.
```

You can also select a skill for a specific task. Use `$<name>` in Codex or
`/<name>` in Claude Code:

| Task | Skill |
| --- | --- |
| Examine an idea through focused questions | [grilling](grilling/SKILL.md) or the explicit [grill-me](grill-me/SKILL.md) entry |
| Save a requirements discussion as a readable design | [to-docs](to-docs/SKILL.md) |
| Keep project documents and plans accurate | [maintenance-docs](maintenance-docs/SKILL.md) |
| Find prior decisions and retain their rationale | [decision-notes](decision-notes/SKILL.md) |
| Develop a change through failing and passing tests | pstack [tdd](pstack/skills/tdd/SKILL.md) |

Use `setup-pstack` when you want to configure models for workflow roles. Without
configured, supported models, the adapters inherit the session model and disclose
missing model diversity. Skills do not provide unavailable models, tools, or services.
Project authorization still governs commits, PRs, messages, deployment, and data changes.

Installation alone does not activate `poteto-mode` for every request. Select it
for an engineering workflow, or select a leaf skill for a focused task. Its host
adapter reads the [composition rules](pstack/docs/composition.md) before combining
methods. These rules apply without optional project guidance: reuse prior decisions,
add interviews or documentation work only when needed, preserve authorization at
each handoff, and keep one owning design and plan. Saving a design does not start
implementation. Existing implementation approval does not need to be repeated.

### Context use

The bundle has 58 skills that require explicit invocation and five eligible for
implicit selection. Full skill bodies load when used. Installation scope controls
where skills are available, not how much of each body loads.

A broad workflow can load substantial guidance. The
[context measurements and limits](docs/validation.md#user-scope-migration-on-2026-11-03)
describe source metadata counts, not a prompt-token benchmark.

## Packages

The default installation combines 58 pstack skills with five local supplements:

| Package | Contents or purpose |
| --- | --- |
| [pstack/](pstack/README.md) | All 58 upstream skills, including 24 principle skills, plus 23 playbooks, agents, scripts, documentation, assets, and Benny resources |
| [grilling/](grilling/SKILL.md) | Focused requirements and design interviews |
| [grill-me/](grill-me/SKILL.md) | Explicit interview entry. Keep it with `grilling` |
| [to-docs/](to-docs/SKILL.md) | Readable designs from discussions |
| [maintenance-docs/](maintenance-docs/SKILL.md) | Current facts, designs, plans, and document ownership |
| [decision-notes/](decision-notes/SKILL.md) | Durable decisions, retrieval, and rationale |

Benny's three automation-only skills stay in their original resource tree. They
are outside the 63 active entries. Installation does not create or enable automations.

The former local `tdd`, `review-code`, and `handoff` packages are retired from
default installation. All eight original packages remain in the verified
[legacy archive](legacy/README.md). `legacy/` and the local `zh-backup/` directory
are backups, not active editions. Keep backups outside active skill directories.

### Native plugin bundle

For Claude Code plugin loading, build a portable bundle with all five supplements:

```powershell
python scripts/package.py --output .dist/pstack
claude --plugin-dir D:/path/to/skills/.dist/pstack
```

Replace the plugin path with the actual output path. Choose a new output directory
for each build. The packager refuses to overwrite an existing directory.

Plugin loading uses `/pstack:poteto-mode`. User and project installations use the
unprefixed entries above. Avoid loading the same skills through both the plugin
and a user or project installation.

The bundle includes a portable manifest and a Claude compatibility manifest.
For Codex, use the directly tested installer above. Do not use an upstream
marketplace command to install this repository's adaptations.

## Project agent guidance

Skill packages work without the optional project guidance. To adopt that guidance,
follow the [integration instructions](agent-guidance/README.md) and adapt the
[entry template](agent-guidance/AGENTS.template.md) to your project.

Keep the project's constraints, resource links, and authorization rules. pstack
owns execution methods. The supplements own interview, document, and decision
methods. Link to those methods instead of copying their full procedures.

Each project owns its guidance copy and explicitly adopts updates. Changes in
this checkout do not update other projects or existing user installations.
[AGENTS.md](AGENTS.md) is the instruction entry for maintaining this library.

## Reading and maintenance

Read the applicable [project guidance](AGENTS.md) before changes. For host behavior
or imported-source updates, read [adaptation and source ownership](docs/adaptation.md).
The [host router](pstack/skills/poteto-mode/references/host.md) applies to direct
skill invocation too. Host mappings take precedence over retained Cursor examples.

Run the library checks from the repository root:

```powershell
python scripts/verify.py
python -m unittest discover -s tests -v
git diff --check
```

The verifier checks source completeness, archive hashes, active skill names,
metadata, and maintained Markdown references. The tests cover portable helpers,
packaging, installation, and backup behavior.

For host or installation changes, also check native discovery and invocation in
isolated projects. Follow the [validation procedure](agent-guidance/validation.md)
and inspect actual file reads and side effects. Static checks alone do not prove
runtime behavior or external integrations. Review the complete staged file list
and diff before an authorized commit.

## Verified host behavior

[Validation evidence](docs/validation.md) records the checked host versions,
discovery results, representative invocations, and user-scope migration. It also
names untested workflows and integrations. Those checks do not establish every
playbook, cross-model review, or Cursor-only service.

Earlier eight-skill checks from 2026-10-17 and 2026-10-22 apply to the old snapshot.
They do not validate this adaptation. Their descriptions remain in Git at
`61c9e1f:README.md`.

## Publication scope

Public sources are `README.md`, `LICENSE`, `AGENTS.md`, `.gitignore`,
`.gitattributes`, `pstack/`, the five root supplement directories,
`agent-guidance/`, `docs/`, `scripts/`, `tests/`, and `legacy/`.

Preserve complete packages, referenced resources, licenses, and origin files.
Keep the complete `pstack/` tree, including upstream tests, assets, and automation
resources. `legacy/` remains an archive, not an installation source.

Exclude `design/`, `zh-backup/`, local installations in `.agents/` and `.claude/`,
`.dist/`, `.tmp/`, caches, dependencies, and generated media. Git ignore rules do
not remove tracked files or filter web uploads. Inspect the actual publication
selection. Packaging and installation do not authorize publication.

## License and upstream sources

Local work uses the root [MIT license](LICENSE). pstack retains
[Lauren Tan's MIT notice](pstack/LICENSE). This distribution uses the portable
[backnotprop/pstack](https://github.com/backnotprop/pstack) baseline at `6c75f4e`
and retains every file from the original Cursor snapshot.

[source-lock.json](pstack/source-lock.json) records exact revisions, hashes, and
adapted paths. [ORIGIN.md](pstack/ORIGIN.md) records provenance. Each installed
pstack skill also carries its license and origin notice.

The five supplements retain their existing licenses and applicable origin files.
The legacy archive retains those of all eight old packages. Preserve upstream
copyright notices when redistributing any package.
