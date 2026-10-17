# Agent Skills

Eight skills for design discussions, engineering documentation, implementation, review, and handoff. The root-level packages are the maintained English edition. `zh-backup/` is a local Chinese backup, excluded from publication; do not install it alongside the root packages because their skill names overlap.

| Skill | Purpose |
| --- | --- |
| [grilling](grilling/SKILL.md) | Stress-test an idea or design through questions grouped by settled prerequisites. |
| [grill-me](grill-me/SKILL.md) | Explicit entry point for the grilling interview; install with `grilling`. |
| [to-docs](to-docs/SKILL.md) | Turn discussion outcomes into human-readable design documents. |
| [maintenance-docs](maintenance-docs/SKILL.md) | Maintain subsystem documentation, change designs, plans, and their source relationships. |
| [decision-notes](decision-notes/SKILL.md) | Find and maintain long-term decisions, rationale, and rejected or superseded approaches. |
| [tdd](tdd/SKILL.md) | Develop behavior incrementally through discriminating failing tests, minimal implementation, and refactoring. |
| [code-review](code-review/SKILL.md) | Review requirements, project standards, and correctness against the actual change scope. |
| [handoff](handoff/SKILL.md) | Prepare a context transfer or verify a handoff before continuing work. |

## Install

1. Download or clone this collection from its actual repository location.
2. Locate the skill directory already configured for your host. Copy the selected **complete package directories** into it, with one directory per skill. For the full workflow, copy all eight packages listed above.
3. Preserve all bundled files, including `references/`, `agents/`, `ORIGIN.md`, and `LICENSE` where present. Copying only `SKILL.md` loses guidance or license notices. For a partial installation, also make the companion methods referenced by name available to the host.
4. Follow the host's own discovery or registration procedure, then verify that the expected skill names are available. Paths, tool names, and metadata support vary by host; `agents/openai.yaml` alone does not install or register a skill.

Expected layout, where `<configured-skill-directory>` is your host's actual configured location:

```text
<configured-skill-directory>/
  grilling/SKILL.md
  grill-me/SKILL.md
  to-docs/SKILL.md
  maintenance-docs/SKILL.md
  decision-notes/SKILL.md
  tdd/SKILL.md
  code-review/SKILL.md
  handoff/SKILL.md
  ...other files inside each complete package
```

Keep `grill-me` and `grilling` together. On a host with a `Skill` tool, the explicit `grill-me` entry delegates to `grilling`. If that tool is unavailable, open the installed `grilling/SKILL.md` through the host's supported file-reading mechanism and follow it directly, resolving any relative references from that package. Do not assume every host supports the same invocation or automatic discovery behavior. Installation and runtime behavior must be checked in the target host; this collection has not been behavior-tested across hosts.

## Project guidance template

[AGENT.example.md](AGENT.example.md) is an optional template, not an active project instruction file or a ninth skill. Follow [Agent Guidance Integration](agent-guidance/README.md) to place it under the name your tool recognizes, such as `AGENTS.md` or `CLAUDE.md`, and copy its three companion files from `agent-guidance/`. Replace placeholders with actual project resources and update skill links to the installed locations. Markdown links provide navigation; they do not automatically load the linked rules.

## Publication scope

Publish only these root entries, including all files inside the listed directories:

```text
README.md
LICENSE
AGENT.example.md
.gitignore
.gitattributes
agent-guidance/
grilling/
grill-me/
to-docs/
maintenance-docs/
decision-notes/
tdd/
code-review/
handoff/
```

`design/`, `zh-backup/`, the root `handoff.md`, `github-preupload-review.md`, `.claude/`, and local generated artifacts are internal working material and excluded by `.gitignore`. The `handoff/` skill directory is public; the root `handoff.md` working record is excluded.

`.gitignore` affects Git adding untracked files; it does not remove already tracked files, and GitHub's web upload does not apply it. For web uploads, explicitly select only the public entries listed above. Check the actual staged files or web upload selection before publishing, and retain package `LICENSE` and `ORIGIN.md` files.

## License and upstream sources

Locally authored material is licensed under the [MIT License](LICENSE), with Copyright (c) 2026 skills contributors. This covers the project template, companion guidance, this README, and the locally authored packages, which also retain their own copies: [decision-notes/LICENSE](decision-notes/LICENSE), [maintenance-docs/LICENSE](maintenance-docs/LICENSE), and [to-docs/LICENSE](to-docs/LICENSE).

The upstream and adapted packages retain Copyright (c) 2026 Matt Pocock and their original MIT notices: [grilling/LICENSE](grilling/LICENSE), [grill-me/LICENSE](grill-me/LICENSE), [tdd/LICENSE](tdd/LICENSE), [code-review/LICENSE](code-review/LICENSE), and [handoff/LICENSE](handoff/LICENSE). Their upstream is [mattpocock/skills](https://github.com/mattpocock/skills), using source revision [`c55ee46073ed923f86ce59a5eb3b6d895095d1b7`](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7). Local adaptations are documented in [grill-me/ORIGIN.md](grill-me/ORIGIN.md), [tdd/ORIGIN.md](tdd/ORIGIN.md), [code-review/ORIGIN.md](code-review/ORIGIN.md), and [handoff/ORIGIN.md](handoff/ORIGIN.md). Retain the applicable copyright, license, and origin notices when redistributing these packages; the root license does not replace their notices.
