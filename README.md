# Engineering Skills

Complete [pstack 0.15.36](pstack/README.md), adapted for Codex and Claude Code,
with five local supplements. pstack is the main engineering workflow. The
supplements retain design interviews, readable designs, document maintenance,
and long-term decisions without adding a second mandatory workflow.

The portable baseline is [backnotprop/pstack](https://github.com/backnotprop/pstack)
at `6c75f4e`. It preserves every file in Cursor's original pstack snapshot.
Exact revisions, hashes, and local changes are in [source-lock.json](pstack/source-lock.json)
and [ORIGIN.md](pstack/ORIGIN.md). See [adaptation](docs/adaptation.md) for ownership
and update rules.

## Packages

| Source | Role |
| --- | --- |
| [pstack/](pstack/README.md) | All 58 upstream skills, 24 principle skills included; 23 playbooks, agents, scripts, documentation, assets, and Benny automation resources |
| [grilling](grilling/SKILL.md) | Focused design/requirements interview |
| [grill-me](grill-me/SKILL.md) | Explicit interview entry; keep with grilling |
| [to-docs](to-docs/SKILL.md) | Preserve a discussion as a readable design |
| [maintenance-docs](maintenance-docs/SKILL.md) | Maintain current facts, designs, plans, and source ownership |
| [decision-notes](decision-notes/SKILL.md) | Retrieve and maintain durable decisions and their rationale |

The default bundle contains **63 skill names**. Benny's three automation-only
skills remain in their original resource tree; they are not global skill entries.
Installation does not create or enable automations.

The former local `tdd`, `review-code`, and `handoff` are retired from default
installation. All eight original complete packages are preserved in the verified
[legacy archive](legacy/README.md). Keep backups outside active skill directories.
`zh-backup/` remains a local, unmaintained backup.

## Install

Requirements: Python 3.10+ and Git. The source and adapters are plain files.
Individual upstream tools can require Node, Bun, Java/TLC, or Git Bash; check the
workflow before running it. Installing the bundle does not install these tools.

Install into a project, using the actual checkout path:

```powershell
python scripts/install.py --host codex --project D:/path/to/project --dry-run
python scripts/install.py --host codex --project D:/path/to/project
python scripts/install.py --host claude-code --project D:/path/to/project
```

The installer copies a complete bundle into `<project>/.agents/pstack/` or
`<project>/.claude/pstack/`. It copies the 63 active packages into the host's
`skills/` folder and redirects package-external documentation links to the full
bundle. It requires no symlink privileges. Claude Code also receives two agents.

Existing skills, agents, or unmanaged bundles cause a preflight failure. The
installer does not merge or overwrite them. `--replace-managed` updates a previous
managed install only when its recorded files remain unchanged; it retains the
previous bundle and active packages under `pstack-backups/`. Reconcile modified
installed files first. Keep the active packages and complete bundle together.

The installer leaves user settings, model files, permissions, `AGENTS.md`, and
`CLAUDE.md` unchanged. It does not install globally or update other projects.
Start a new host session after installation and inspect its skill inventory.

| Host | Entry | Adapter |
| --- | --- | --- |
| Codex project install | `$poteto-mode` | [Codex](pstack/docs/harness/codex.md) |
| Claude Code project install | `/poteto-mode` | [Claude Code](pstack/docs/harness/claude-code-local.md) |

Use the installed `setup-pstack` only when you want to configure role models.
Without configured, supported models, adapters inherit the session model and
disclose missing diversity. Skills cannot make an unavailable model/tool exist.
Project authorization still governs commits, PRs, messages, deployment, and data.

Installation alone does not activate `poteto-mode` for every request. Select it
for an engineering workflow, or select a leaf skill for a focused task. Its host
adapter reads the [composition rules](pstack/docs/composition.md) before combining
methods. These rules apply without optional project guidance: reuse prior decisions,
add interviews or documentation work only when needed, preserve authorization at
each handoff, and keep one owning design and plan. Saving a design does not start
implementation. Existing implementation approval does not need to be repeated.

### Native plugin bundle

Build a portable bundle that includes all five supplements:

```powershell
python scripts/package.py --output .dist/pstack
claude --plugin-dir D:/path/to/skills/.dist/pstack
```

Choose a new output directory for each rebuild; the packager never overwrites an
existing output. Generated bundles are local and are not included in the checkout.

For Claude plugin loading use `/pstack:poteto-mode`; for a project installation use
the unprefixed command. Choose one mode to avoid duplicates. The bundle contains
the root portable manifest and a Claude compatibility manifest. Codex can also
consume portable plugin packages through its supported plugin installation flow;
the project installer above is this library's directly tested local path.
Do not use an upstream marketplace command to install these local adaptations.

## Project agent guidance

[AGENTS.md](AGENTS.md) is this library's instruction entry. For other projects,
follow [integration instructions](agent-guidance/README.md) and the
[template](agent-guidance/AGENTS.template.md). Guidance is optional; skill packages
do not depend on installing project instructions.

Keep project constraints and resource navigation. pstack owns execution methods;
the five supplements own document and decision methods. Remove copied method
steps when adopting pstack, without discarding project-specific obligations.
Each project owns its guidance copy and explicitly adopts updates. Existing
project copies and unrelated user installations do not change with this checkout.

## Reading and maintenance

Read the applicable root guidance before changes. Every imported skill links to
the [host router](pstack/skills/poteto-mode/references/host.md), including standalone
leaf invocations. Host mappings take precedence over retained Cursor examples.
Keep complete packages, licenses, origins, and referenced resources together.

Run these checks from the repository root:

```powershell
python scripts/verify.py
python -m unittest discover -s tests -v
git diff --check
```

The [CI workflow](docs/ci.md) runs library checks on Windows and Linux. It also
tests the PR watcher and plan checker with Bun. The CI guide lists local commands,
coverage limits, dependency updates, and recommended merge rules.

For host/installation changes, also run actual host discovery and invocation
checks in isolated projects, following [validation methods](agent-guidance/validation.md).
Check file reads, covered paths, and side effects. Metadata validation does not
prove runtime behavior, model diversity, or Cursor-only integrations.
Use the staged file list and diff before any authorized commit.

## Verified host behavior

Current adaptation results and their limits are maintained in
[validation evidence](docs/validation.md). Earlier eight-skill discovery and
invocation results from 2026-10-17 and the controlled engineering run from
2026-10-22 apply to the old snapshot. They do not validate this adaptation.
The original descriptions remain in Git at `61c9e1f:README.md`.

## Publication scope

Public sources are `README.md`, `LICENSE`, `AGENTS.md`, `.gitignore`,
`.gitattributes`, `.github/`, `pstack/`, the five root supplement directories,
`agent-guidance/`, `docs/`, `scripts/`, `tests/`, and `legacy/`.
Keep the archive's licenses and origin files intact. `legacy/` is a backup,
not an installation source. Preserve the complete `pstack/` tree, including
upstream tests, assets, and automation resources.

Exclude `design/`, `zh-backup/`, local installations in `.agents/` and `.claude/`,
`.dist/`, `.tmp/`, caches, dependencies, and generated media. Git ignore rules do
not remove tracked files or filter web uploads. Inspect the actual publication
selection. No publication operation is implied by packaging or installing.

## License and upstream sources

Local work uses the root [MIT license](LICENSE). pstack retains
[Lauren Tan's MIT notice](pstack/LICENSE), its original source files, and
[mirror provenance](pstack/ORIGIN.md). Each installed pstack skill also carries
its license and origin notice. Five supplements retain their existing licenses
and applicable origin files. The legacy archive preserves those of all eight
old packages. Do not replace upstream copyright notices with the local notice.
