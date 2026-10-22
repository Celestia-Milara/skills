# Agent Skills

A reusable collection of personal engineering conventions: eight skills for design discussions, engineering documentation, implementation, review, and handoff, plus project agent guidance. The root-level packages are the maintained English edition. `zh-backup/` is a local Chinese backup, excluded from publication; do not install it alongside the root packages because their skill names overlap.

| Skill | Purpose |
| --- | --- |
| [grilling](grilling/SKILL.md) | Stress-test an idea or design through questions grouped by settled prerequisites. |
| [grill-me](grill-me/SKILL.md) | Explicit entry point for the grilling interview; install with `grilling`. |
| [to-docs](to-docs/SKILL.md) | Turn discussion outcomes into human-readable design documents. |
| [maintenance-docs](maintenance-docs/SKILL.md) | Maintain subsystem documentation, change designs, plans, and their source relationships. |
| [decision-notes](decision-notes/SKILL.md) | Find and maintain long-term decisions, rationale, and rejected or superseded approaches. |
| [tdd](tdd/SKILL.md) | Develop behavior incrementally through discriminating failing tests, minimal implementation, and refactoring. |
| [review-code](review-code/SKILL.md) | Review requirements, project standards, and correctness against the actual change scope. |
| [handoff](handoff/SKILL.md) | Prepare a context transfer or verify a handoff before continuing work. |

The custom review skill uses `/review-code` to keep Claude Code's bundled `/code-review` available. A custom skill with the same name replaces the bundled command; see [Resolve skills that share a name](https://code.claude.com/docs/en/skills#resolve-skills-that-share-a-name).

## Install

1. Download or clone [Celestia-Milara/skills](https://github.com/Celestia-Milara/skills).
2. Choose a host location from the table below. Copy the selected **complete package directories** into it, with one directory per skill. For the full workflow, copy all eight packages listed above; copying this repository itself into a skills directory does not produce that layout.
3. Preserve all bundled files, including `references/`, `agents/`, `ORIGIN.md`, and `LICENSE` where present. Copying only `SKILL.md` loses guidance or license notices. For a partial installation, also make the companion methods referenced by name available to the host.
4. Start a new session and verify that the expected skill names are available. Paths, tool names, and metadata support vary by host; `agents/openai.yaml` alone does not install or register a skill.

| Host | Personal installation | Project installation | Explicit invocation |
| --- | --- | --- | --- |
| Codex | `~/.agents/skills/<name>/` | `.agents/skills/<name>/` | `$grilling`, `$grill-me`, or another installed name |
| Claude Code | `~/.claude/skills/<name>/` | `.claude/skills/<name>/` | `/grilling`, `/grill-me`, or another installed name |

`~` means your user home directory, such as `C:\Users\<user>` on Windows. Project paths are relative to the project directory. Choose one scope per host to avoid installing the same names twice. In Codex, open the skill picker with `$`; in Claude Code, use `/` and check the available commands. If an existing session still shows the old inventory, restart the host. See the official [Codex skills documentation](https://learn.chatgpt.com/docs/build-skills) and [Claude Code skills documentation](https://code.claude.com/docs/en/skills).

Expected layout, where `<configured-skill-directory>` is your host's actual configured location:

```text
<configured-skill-directory>/
  grilling/SKILL.md
  grill-me/SKILL.md
  to-docs/SKILL.md
  maintenance-docs/SKILL.md
  decision-notes/SKILL.md
  tdd/SKILL.md
  review-code/SKILL.md
  handoff/SKILL.md
  ...other files inside each complete package
```

Keep `grill-me` and `grilling` together. On a host with a `Skill` tool, the explicit `grill-me` entry delegates to `grilling`. If that tool is unavailable, open the installed `grilling/SKILL.md` through the host's supported file-reading mechanism and follow it directly, resolving any relative references from that package.

`grill-me` intentionally requires explicit invocation: Claude Code uses `disable-model-invocation: true`, and Codex uses `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. The other seven skills are eligible for automatic selection from their descriptions. Being discovered does not guarantee that the model will choose a skill for every related prompt or that its tools can read the package.

### Verified host behavior

Checked on Windows on 2026-10-17:

| Check | Codex CLI `0.163.0` / desktop CLI `0.163.0-alpha.10.2` | Claude Code `2.1.302` |
| --- | --- | --- |
| Project discovery with all eight complete packages | 8 names found; no loader errors | 8 commands found; bundled `/code-review` retained |
| Project discovery with only `decision-notes` | Standalone package found; no loader errors | Standalone command found; bundled `/code-review` retained |
| Personal installation in an empty project | Both CLIs found all 8 as enabled user skills | All 8 found as user commands |
| Natural-language design interview through Magpie | npm CLI automatically selected and read `grilling`, then returned questions and recommendations in a read-only sandbox | Automatically invoked `Skill(grilling)` and returned questions and recommendations |
| Explicit `grill-me` entry through Magpie | Loaded the installed `grilling` companion and completed the interview round | `/grill-me` invoked `Skill(grilling)` and completed the interview round |
| Explicit invocation of the other six workflow skills through Magpie | All six read the synthetic project and returned task-specific results | All six read the synthetic project and returned task-specific results |

The discovery checks used the hosts' actual initialization/skill-list interfaces. All eight skills completed invocation smoke checks on each host, with runtime requests confirmed in Magpie's local routing log with successful HTTP responses. The synthetic project exercised decision retrieval, design and maintenance-document previews, a TDD test-and-patch preview, an intentional review defect, and a handoff preview. Its files remained unchanged: these read-only checks do not establish full document-writing or red/green implementation workflows. Automatic selection was tested for `grilling`; these checks do not claim automatic selection was tested for every skill. Runtime Codex checks used the npm CLI; the desktop CLI was checked for discovery.

### Engineering task validation

On 2026-10-22, six fresh-context Agents worked in isolated Python/SQLite projects. Each had the complete skill packages and project guidance at `5555d0c`. Tasks covered an internal refactor, a contract defect, an authorized queued-save change, and a storage change. The other tasks addressed a fake that hid commit timing and a command that ran no tests.

Independent checks confirmed the requested behavior and real database effects. All 52 acceptance checks and 45 project tests passed, with no skips. All six starting projects failed their relevant acceptance checks. A shared Windows connection-cleanup defect was corrected before acceptance; original and corrected baselines were retained. Evidence includes fresh SQLite connections, concurrent retries, event visibility, the shipped client, CSV output, and actual test counts.

This was one controlled diagnostic run, not an old/new skills comparison or proof of general effectiveness. It does not cover production deployment, separate-process stress, crash recovery, or cross-host behavior. Fixtures, patches, commands, and results remain in the separate local test workspace; they are not package dependencies.

### Local gateway and isolated-test troubleshooting

If Claude Code uses a loopback gateway such as Magpie while inheriting `HTTP_PROXY` or `HTTPS_PROXY`, ensure `NO_PROXY` includes `localhost,127.0.0.1,::1`. Preserve existing exclusions when appending these entries; back up configuration before changing it. Claude Code can receive these values through the `env` object in its user settings. In the tested setup, adding both `NO_PROXY` and `no_proxy` resolved HTTP 502 responses without changing the model or gateway credentials. A direct gateway request alone does not establish that the CLI follows the same proxy path.

On Windows, an isolated Codex run using `--ignore-user-config` also discards the user's native sandbox configuration. In the tested setup, this caused a normal skill-file read to be rejected by command policy. Explicitly carrying over the configured `windows.sandbox` option restored file reads while retaining `--sandbox read-only`. Similarly, carry over the selected provider definition and explicitly select Magpie if the isolated test is meant to use that gateway. Keep credentials out of command arguments, reports, and repository files.

For read-only Claude Code invocation tests, retain `Glob` and `Grep` alongside `Read` and `Skill`; history and documentation workflows need to locate files as well as open them. Restricting the test to `Read,Skill` caused a history lookup to stall on guessed paths. With `dontAsk`, also grant access to the installed skills directory using `--add-dir` if bundled reference reads would otherwise require approval outside the working directory. The tested harness added only `~/.claude/skills` and retained its read-only tool set. See [Claude Code working directories](https://code.claude.com/docs/en/permissions#working-directories). These are test access constraints, not package-discovery failures.

## Project agent guidance

[AGENTS.md](AGENTS.md) is the active instruction entry point for maintaining this library. For other projects, start with [AGENTS.template.md](agent-guidance/AGENTS.template.md) and the three companion files in `agent-guidance/`; these are engineering conventions, not a ninth skill. [Agent Guidance Integration](agent-guidance/README.md) owns the setup, link adjustment, and source-version workflow. Each project keeps a reviewable copy with its own resources and constraints, adopting source updates explicitly rather than following a live global file. Markdown links provide navigation; they do not automatically load the linked rules.

## Reading and maintenance

Each package's `description` identifies when it applies; `SKILL.md` contains its main workflow and necessary defaults. Read bundled references under the conditions given in the entry point. The purpose table above is navigation, not an overriding policy. A standalone review reports by default; an authorized implementation task or explicit fix request may address confirmed defects within scope.

Project guidance is optional. Skill packages retain essential boundaries locally; where a commit step applies, the standalone fallback is: show checked work and ask by default, honor explicit authorization already given for the same scope, and do not treat saving a document as permission to publish. Companion skill names describe cooperating methods; use installed capabilities or readable configured guidance, state missing dependencies, and do not claim unavailable invocations.

For guidance-only changes, check Markdown links and anchors, reading triggers, source ownership, and the template after adapting its paths to a target project. Use `git diff --check` for tracked changes and include new files in the review. For package or installation changes, also check affected package metadata and references; use host checks when discovery or invocation behavior is affected, and report their limits separately from static checks. Preserve complete package contents and license/origin notices; keep publication selection within the scope below.

## Publication scope

Publish only these root entries, including all files inside the listed directories:

```text
README.md
LICENSE
AGENTS.md
.gitignore
.gitattributes
agent-guidance/
grilling/
grill-me/
to-docs/
maintenance-docs/
decision-notes/
tdd/
review-code/
handoff/
```

The repository contains installable skill packages, optional project guidance, and source/license information; install only the selected skill packages. Internal work and local backups or generated artifacts are excluded by `.gitignore` and are not installation candidates. The `handoff/` package is public; the root working record `handoff.md` is excluded.

`.gitignore` affects Git adding untracked files; it does not remove already tracked files, and GitHub's web upload does not apply it. For web uploads, explicitly select only the public entries listed above. Check the actual staged files or web upload selection before publishing, and retain package `LICENSE` and `ORIGIN.md` files.

## License and upstream sources

Locally authored material is licensed under the [MIT License](LICENSE), with Copyright (c) 2026 skills contributors. This covers the project template, companion guidance, this README, and the locally authored packages, which also retain their own copies: [decision-notes/LICENSE](decision-notes/LICENSE), [maintenance-docs/LICENSE](maintenance-docs/LICENSE), and [to-docs/LICENSE](to-docs/LICENSE).

The upstream and adapted packages retain Copyright (c) 2026 Matt Pocock and their original MIT notices: [grilling/LICENSE](grilling/LICENSE), [grill-me/LICENSE](grill-me/LICENSE), [tdd/LICENSE](tdd/LICENSE), [review-code/LICENSE](review-code/LICENSE), and [handoff/LICENSE](handoff/LICENSE). Their upstream is [mattpocock/skills](https://github.com/mattpocock/skills), using source revision [`c55ee46073ed923f86ce59a5eb3b6d895095d1b7`](https://github.com/mattpocock/skills/tree/c55ee46073ed923f86ce59a5eb3b6d895095d1b7). Local adaptations are documented in [grill-me/ORIGIN.md](grill-me/ORIGIN.md), [tdd/ORIGIN.md](tdd/ORIGIN.md), [review-code/ORIGIN.md](review-code/ORIGIN.md), and [handoff/ORIGIN.md](handoff/ORIGIN.md). Retain the applicable copyright, license, and origin notices when redistributing these packages; the root license does not replace their notices.
