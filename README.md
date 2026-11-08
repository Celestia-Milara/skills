# Official pstack with host adapters

This repository maintains the complete official pstack 0.15.36 source and small,
external adapters for Claude Code, Codex, Pi and DeepSeek Harness. The shared
workflow source stays unchanged. Host metadata and adapter prompts are generated
only in installed copies.

## Sources and maintenance

- [Official source](pstack/README.md) is pinned in [source-lock.json](source-lock.json).
- [Host adapters](adapters/common.md) own tool, model and installation mappings.
- [Adaptation rules](docs/adaptation.md) explain source ownership and host limits.
- [Validation](docs/validation.md) records real checks and unverified capabilities.
- [Project-only composition](docs/composition.md) coordinates the optional local supplements.

The five local supplements remain separate packages: grilling, grill-me, to-docs,
maintenance-docs and decision-notes. A clean install exposes 58 pstack skills.
Use `--with-supplements` to include the five, for 63 entries. Managed updates
preserve supplements already owned by that installation. They are not injected
into the official pstack workflow.

## Install

Use Python 3.10+. Installers do not download models, Java, Bun, WSL or other tools.
Back up before replacing existing installations:

```powershell
python -B scripts/backup_installation.py --project . --output D:/private-backups/before-pstack
python -B scripts/install.py --host codex --scope user --dry-run
python -B scripts/install.py --host codex --scope user
python -B scripts/install.py --host claude-code --scope user
python -B scripts/install.py --host pi --scope user
python -B scripts/install.py --host dsh --scope user
```

| Host | User skills | Resource bundle |
| --- | --- | --- |
| Codex | ~/.codex/skills | ~/.codex/pstack |
| Claude Code | ~/.claude/skills | ~/.claude/pstack |
| Pi | ~/.pi/agent/skills | ~/.pi/agent/pstack |
| DeepSeek Harness | ~/.dsh/skills | ~/.dsh/pstack |

Codex user scope uses its verified host-local directory so Pi and dsh do not read
Codex metadata from shared ~/.agents/skills. Project Codex scope still uses
.agents/skills. Do not place different host projections in a shared project
folder if another engine also reads it. Project scope uses `--project PATH`
instead of `--scope user`. `--home PATH` selects an isolated user root for testing.

This is a skill-directory install. Claude commands are `/poteto-mode`, not a
plugin namespace. Claude also receives two named agent files. Pi explicit commands
use `/skill:poteto-mode`. DeepSeek Harness supports `/poteto-mode` when its
filesystem skill provider is mounted. An installed file does not prove a live
session loaded it; check discovery and reload using that host's own controls.

Use `--replace-managed` only for an unchanged managed installation. Changes or
unrecognized collisions are refused. The installer checks ownership and hashes,
builds in staging, takes a lock, rechecks, and rolls back ordinary switch failures.
Crashes can leave staging or a lock; inspect retained paths before manual recovery.
User instructions, model configuration, credentials and permissions are not changed
by the installer. Model role setup is a separate operation.

## Reading and maintenance

```powershell
python -B scripts/verify.py
python -B -m unittest discover -s tests -v
python -B scripts/package.py --output .dist/pstack
```

Update the official source and its complete hash inventory together. Keep host
changes in adapters and projection code. Do not hand-edit installed generated
files. Use a three-way comparison when importing a new official revision.

## Windows

[Execution platforms](adapters/platforms/README.md) defines the common script layer
used by all four hosts. It includes a read-only dependency/hash check and portable
commands for logging, local worktree facts and plan checking. Platform mappings
are pinned to upstream hashes. The launcher refuses unverified workflows and does
not select WSL or install tools automatically. Current user installations are not
updated by a repository change; verify an isolated installation before migration.

### Shared resources with Junctions

Copy storage remains the default. On native Windows CPython, test the shared
layout with an isolated home before converting an existing installation:

```powershell
python -B scripts/install.py --host codex --scope user --home .tmp/junction-home --storage junction --store .tmp/junction-store --dry-run
python -B scripts/install.py --host codex --scope user --home .tmp/junction-home --storage junction --store .tmp/junction-store
```

Use the same home and store arguments for other host profiles. Each complete
public resource version is stored once under `store/versions/<content-hash>`.
Every version includes the 58 official skills and five supplement resources;
only the requested 58 or 63 host entries are exposed. The host's `pstack` is a
Junction. Host ownership is recorded in `.pstack-install.json` beside it, not
inside the shared target. UNC stores are not supported.

Entries and metadata stay host-specific. Read-only resource directories share
Junctions only when Markdown links retain correct host targets. Script directories
stay private because tools may install dependencies beside themselves. Documents
with cross-skill references also stay private to retain adapted entry targets
after realpath resolution. This saves repeated complete resource bundles but does
not claim zero copied files or shared writable dependency trees.

To convert an unchanged copy or update a Junction installation, add
`--replace-managed`. Preview first. Modified entries or public contents are refused.
Versions are verified and never overwritten; no automatic store garbage collection
is performed. A failed host switch restores old paths and retains published shared
versions. For a failed rollback, preserve the reported staging and backup paths.

Archive an installation with `--storage junction --uninstall`. This moves active
entries to a host-local backup. Restore an archived Junction version with
`--storage junction --restore <host-backup-path>`. Restore works after uninstall or
replaces a valid current Junction version, retaining that version as another backup.
Copy-install backups require manual recovery; they are not Junction receipts.

Cleanup unlinks Junctions rather than traversing targets. Public resources remain
available to other hosts and backups. Backups include the external receipt and
materialize linked contents. Inspect link records before restoring elsewhere.

The public resource tree is reference material, not a writable tool workspace.
It is hash-checked, not protected by filesystem ACLs. Running raw self-installing
scripts directly from that tree can invalidate it; use the host entry's private
scripts directory. No Bun dependency installation is part of installer validation.

The upstream tree includes POSIX scripts. Installation and discovery do not prove
those scripts work on Windows. Native script compatibility and WSL workflows are
separate acceptance work. No experimental Windows Job patch is included here.

## Publication scope

Publish maintained source, adapters, scripts, tests and project guidance. Private
installation backups, credentials, chat logs, generated installs, design scratch,
legacy working copies and local experiment evidence are not publication inputs.
Keep applicable licenses and source records with the distribution.

## License and upstream sources

Official pstack retains its [MIT license](pstack/LICENSE). Adapter origins are
recorded in [adapters/ORIGIN.md](adapters/ORIGIN.md). Supplement packages retain
individual licenses. Historical backups remain available under legacy.
