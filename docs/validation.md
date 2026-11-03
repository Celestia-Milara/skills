# Adaptation validation

Checked on Windows on 2026-11-03 against the local adaptation on
`codex/pstack-host-adaptation`, based on library commit `61c9e1f`, pstack 0.15.36,
Cursor snapshot `ae5650f`, and portable mirror `6c75f4e`.
Exact upstream hashes are in [source-lock.json](../pstack/source-lock.json).

## Results

| Check | Observed result |
| --- | --- |
| Legacy backup | All 47 files from eight packages match their archive and file hashes |
| Source completeness | All 573 original paths and 582 mirror files retained; adapted paths listed in the lock |
| Static package/reference checks | 63 unique active names; metadata, policies, licenses, Markdown links/anchors pass |
| Portable helpers and installer | 9 tests pass, no skips; includes actual local Git facts, TSV escaping, workspace filtering, installation collisions, managed update backup, changed-file refusal, and installed documentation references |
| Codex native discovery | CLI `0.166.0-alpha.5.1` app-server `skills/list`: all 63 project skills, no loader errors |
| Codex installed metadata | Skill Creator's `quick_validate.py`: all 63 normalized Codex copies pass |
| Claude project discovery | Claude Code `2.1.310` SDK initialization: all 63 local commands, two local agents; built-in `code-review` retained |
| Claude plugin discovery | SDK initialization: 63 `pstack:` commands and both namespaced agents |
| Claude plugin manifest | Native `plugin validate --strict --json`: success, no errors or warnings |
| Codex behavioral smoke | Direct tdd invocation reads shared/Codex adapters; regression fails with `30 != 0` before fix; all 3 tests pass afterward |
| Claude behavioral smoke | Direct tdd invocation reads shared/Claude adapters; regression fails with `30 != 0` before fix; all 3 tests pass afterward |
| Change formatting | `git diff --check` passes; new maintained Markdown also checked by the reference checker |
| Guidance projection | Template copied to a fixture root; three method-link files adapted to the installed Codex paths; all local links and anchors resolve |

Behavior tasks used isolated fixtures under `.tmp/host-codex` and
`.tmp/host-claude`. Each had a timeout parser and two existing tests. The request
required a zero-timeout regression, a failing-before run, a minimal fix, and a
passing-after run. It explicitly excluded delegation, Git writes, messages, PRs,
and settings changes. Actual file/tool events confirm adapter reads and the
red/green order. An independent local unittest run confirmed each final result.
These are representative integer-timeout checks, not a complete parser contract.

The behavior runs preceded final frontmatter projection and help-text cleanup.
Subsequent native discovery, metadata, installed-reference, and installer checks
cover those packaging changes. No model rerun was needed for unchanged tdd logic.

## Corrections found during validation

- Directory junctions did not preserve lexical `../../docs` resolution on Windows.
  Installation now copies active packages and redirects package-external docs.
- Claude's manifest requires explicit agent Markdown files when declaring agents;
  the bundle now lists both files.
- Cursor's `paths` header hid the TypeScript command in Claude project discovery.
  Project projections omit it, while its description retains the intended scope.
- The generic Skill Creator validator rejects Claude/Cursor header extensions.
  Codex projections remove them and keep explicit policy in `agents/openai.yaml`.
- Source locks now hash Git blobs, avoiding CRLF checkout differences.

## Scope and limits

The checked bundle is installed for `D:/03_work/skills` only, in its ignored
`.agents/` and `.claude/` project locations. This does not update global skills,
model settings, other projects, or already-running skill catalogs. Open a new
session to use the project entries. The five supplements retain their methods;
maintenance-docs now routes transfers to pstack when available.

We did not execute every playbook, the original Bun/TypeScript suites, formal
verification toolchains, Cursor Automations, cloud agents, Bugbot launch flows,
multi-day supervision, or cross-family review. Native discovery and two smokes
do not prove those integrations or general quality improvements. External
capabilities remain conditional and must not be reported as successful when absent.

Local raw inventory, runtime events, post-check output, and isolated fixtures are
under `.tmp/evidence/` and `.tmp/host-*`. They are excluded from publication. Raw
host logs can contain account context; publish only this scoped result summary.
Reproduction commands and boundary checks are in the root scripts/tests.

Earlier eight-skill results from 2026-10-17 and the controlled engineering run
from 2026-10-22 remain in Git at `61c9e1f:README.md`. They do not validate this
63-skill adaptation.
