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
