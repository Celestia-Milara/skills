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

## Combined workflows on 2026-11-03

The user authorized composition fixes and behavioral validation, without committing.
Checks used the local working snapshot, including the prior installation changes.
They did not update either personal installation. Existing unrelated edits remain.

### Structural and host checks

- Source/reference verification passed with 63 unique active names, all 573 original
  paths and 582 mirror files retained, and no broken links or invocation-policy errors.
- All 18 Python tests passed. Three new tests follow the composition route from
  source, a standalone plugin bundle, and both installed host projections. The
  installed checks also cover a copied project-guidance link layout.
- The five changed skill entry points passed Skill Creator validation on their
  normalized Codex copies. Discovery found 63 project skills in Codex with no loader
  errors, and all 63 target commands in Claude Code 2.1.310.
- `git diff --check` passed. No files were staged or committed during the implementation checks.

### Native behavioral cases

Each case used a fresh temporary project outside this repository, complete project
packages, no optional project guidance, and the existing host account. Prompts named
the installed entry and excluded delegation, staging, commits, PRs, and external
actions. The local runner and reproduction steps are in
[validation methods](../agent-guidance/validation.md#combined-workflow-checks).

| Case | Checked outcome |
| --- | --- |
| Codex and Claude design-only `architect` | Updated the existing design; implementation and tests stayed unchanged |
| Codex and Claude approved implementation | Fixed the three approved timeout cases without another approval request; regression failed before the fix and passed afterward; the existing work plan held the evidence |
| Codex and Claude ordinary plan | Updated the existing two-phase plan; implementation stayed unchanged; no full-program checker, ten-lane requirement, or invented PR program |

Actual command/read events show the shared router, matching host adapter, and
composition guide in all six scenario combinations. Relevant history and document
methods were read where applicable; some reads used shell loops rather than a
separate tool call per file. Existing history was reused. Final artifacts and Git
state confirmed no new duplicate design/plan, no staging, and no commits. Installed
bundle and skill hashes remained intact. Model replies alone were not acceptance.

Two first-run scope defects required correction:

- Claude's initial ordinary plan treated an unapproved change to `False` as
  accepted because no caller was found. Artifact-only checks did not catch that
  semantic defect. Reviewing the plan did.
- Codex's initial implementation passed the three requested cases but changed
  `None`, `False`, and empty-string behavior. A separate compatibility probe failed.

The composition rule now prevents promoting adjacent behavior changes into accepted
scope. The runner retains a compatibility probe for these fixture inputs. Claude's
plan rerun preserved those behaviors and treated further changes as separate design
decisions. Codex's implementation rerun preserved them and passed the expanded probe.
Codex's ordinary-plan case also used the tightened rule and retained that boundary.

Eight native runs covered the six host/scenario combinations plus two corrective
reruns. The initial bundle manifest SHA-256 was
`5cf8b9e66e5b13c9440b6ccd2587c6e08a5de9586d63fb13706762f79ce0a740`.
The tightened guide used manifest SHA-256
`e4054997bdc956a6d89428a2276f24ebf68e9cd1bc0d9430ef8b0038b31bb156`.
Earlier design and successful Claude implementation evidence was reused; those
cases were not all rerun after the scope clarification. All eight processes exited
normally. Preserve the failed first-run evidence rather than calling all runs passes.

### Independent forward tests and limits

Two fresh-context agents performed separate disposable-fixture tasks under
Skill Creator's forward-testing method:

- `grill-me` loaded `grilling`, accepted already-confirmed understanding, and used
  `to-docs` to update the original design. It did not start implementation or reopen
  the interview.
- `poteto-mode` selected safe pause, kept implementation bytes unchanged, and wrote
  the resume checkpoint into the existing work plan without a commit.

Their reports identify the sources read. Parent checks verified the resulting
files, intact packages, empty indexes, and absent commits. These are independent
forward tests, not additional native Claude/Codex CLI runs or cross-family review.

Raw prompts, host events, artifact checks, bundle hashes, and inventories remain in
`.tmp/composition-round/`; disposable projects are identified by the fixture JSON
files. Raw host logs can contain account context and must not be published. The
small timeout fixture tests routing, authorization, and ownership, not general
parser correctness. Delegation was disabled in native runs, so they do not establish
multi-agent implementation or diverse-model review. Full-program execution,
shipping, tracker writes, and unattended supervision remain untested. Rules guide
model behavior; these checks do not establish a deterministic permission boundary.

### Branch publication snapshot

The user subsequently authorized a commit and push to the feature branch, without
merging into main. The earlier user-scope installation migration remains outside
this commit. The 18-test result above belongs to the full local working snapshot;
the selected publication snapshot passed its 12 tests and source/reference checks
in a separate directory. Its composition skills and packaged resources match the
behavior-tested versions. No native model cases were repeated for this publication
selection. Unrelated local changes and raw host evidence remain uncommitted.
