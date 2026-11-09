# Adaptation validation

## Native Windows statechart

The external Windows adapter invokes the unchanged official worker and its
checker/compiler. All 573 official source files still match source-lock. No
projection patch, WSL fallback, Java install or mise install was used. Existing
Node 24.20, Java 25 and the pinned TLC 1.7.4 jar supplied the runtime. A verified
copy of the existing jar was placed in the common user cache without changing
the source cache or ACLs. Codex could not read the original Claude-private cache.

The Windows Job guardian creates the worker inside its Job before execution.
Real process tests confirm worker/child/grandchild termination after timeout,
explicit cancellation and stdin EOF. The acceptance runner also kills the actual
runtime launcher during a TLC check and observes confirmed Job cleanup, no output
publication and removal of owned staging. It preserves occupied output folders
and rejects overlapping evidence paths and modified private production scripts.
Review exposed publication-before-cleanup, a new output junction being replaced,
and current-directory executable lookup. The guardian now clears private temporary
files before sending a publishable receipt. Output identity checks preserve newly
appeared directories and reparse points. Node and Java resolution uses `.exe`
files from explicit PATH entries, excluding the current directory. The plan
checker uses the same resolver. Cleanup after publication cannot change the
completed checker result into an execution error.

`scripts/check_statechart_windows.py` completed twelve scenarios. Codex, Claude
Code and Pi copy installs, plus a Codex Junction install, each ran the official
Login and MediaPlayer corpus examples. Both generated reports and charts match
the committed expected text. Login exits 0; MediaPlayer exits 1 with the expected
one-step LoudWhenStopped violation. Invalid input and timeout exit 2 without
publishing output. A Chinese output path with spaces and an ampersand succeeds
even when the parent requests an ASCII console encoding.

Two Windows format defects were reproduced before their external fixes. Java
CRLF prevented the pinned parser from recognizing TLC messages. An external Node
preload now adds LF and UTF-8 JVM arguments; no official parser changed. The earlier
JAVA_TOOL_OPTIONS probe fixed parsing but added diagnostic lines to TLC output,
so the final adapter uses direct JVM arguments. A legacy Python console
encoding could raise an error after a valid report was published to a Chinese
path. The adapter now emits UTF-8. Java preflight rejects a conflicting line
separator setting instead of accepting an unreadable result.

Codex, Claude Code and Pi native model calls each read their installed skill,
host adapter and platform contract, then executed `runtime.py run statechart`.
Their reports and charts match the MediaPlayer expected text. Each Job receipt
records checker exit 1, zero active processes and finalized cleanup. These native
runs used the current platform bytes. Codex retained workspace-write; Claude
pre-authorized Bash, and Pi supplied no sandbox. These have different isolation
properties. The initial Codex dependency-access failure remains a failed attempt.

Private source fingerprints, command/event streams and receipts are under
`.tmp/statechart-windows/`. Earlier attempts remain in `native-before-utf8/`
and `native-jto-after-utf8/`.
These examples validate checking, report generation and lifecycle boundaries;
they do not validate every upstream corpus case, every Java version or every
view module. PR monitoring remains deferred. dsh is outside this validation.

The final library run passed 92 tests. Claude Opus 5.5 independently accepted the
five execution-source fingerprints after replaying the adversarial cases and all
33 corpus examples. It checked the native event streams and the 92-test log; it
did not rerun that full library suite. The twelve-case installation matrix and
the final three native samples match the accepted execution files.

The accepted version was installed into the current Codex, Claude Code and Pi
copy installations. Full ownership checks passed for each bundle and entry;
the five execution-source hashes equal the accepted fingerprints. The installations
retain 63, 63 and 58 skills respectively, plus Claude's two named agents. Each
active installation also ran MediaPlayer using the common cached jar and produced
the expected report and chart. Three selected configuration files have equal
before/after/current hashes. Installer rollback backups and exact paths are in
the private rollout records. Acceptance used uncommitted working-tree files.
The recorded fingerprints bind those tested files, not the earlier HEAD or a
main-branch release.
The active checks were direct launcher calls. Native model calls used the isolated
acceptance-5 installs with the same execution files. Rollback backup contents were
verified; rollback itself was not exercised. Configuration preservation covers
only those three selected files. The host-owned `~/.claude.json` changed during
closeout; the actor was not observed, and that file is outside this claim.

Remaining limits include relative PATH entries, which still resolve against the
caller's directory. An explicitly configured `PATH=tools;...` can select a binary
under that project's `tools` directory. Use absolute PATH directories for the
validated execution setup. Forcibly killing the guardian, including a host tree
kill such as `taskkill /T`, can leave owned directories beside the output even
though the processes are gone. Those temporary files can reach gigabytes.
Long paths can fail earlier than the upstream CLI because of the additional
private staging path. Failure is reported without publishing a partial result.
The system code page here is UTF-8; console-encoding simulations do not validate
a non-UTF-8 Windows system code page. Native model cases cover copy storage;
Junction evidence comes from direct installed-command tests. Node 24.20 is the
tested Node version; the broader declared range follows the upstream wrapper.

## Native Windows execution and copy rollout

Bun 1.4.4 was installed from its official pinned release and verified with
`--version` and `--revision`. Seven upstream plan-checker cases ran successfully
with Bun in a disposable private skill directory. The full library regression suite
passed 78 checks, followed by 8 platform checks after diagnostic-report changes.

Native CLI event streams show all four hosts reading the installed
skill, host adapter and platform contract, then invoking the mapped log command.
The resulting TSV retains the requested leading dash, literal quotes and field
values. An earlier generic request permitted manual output under the upstream
skill. The final request explicitly asks for its installed logging command.
Earlier failed runs remain in the private evidence directory; they are not passes.

The Codex, Claude Code and Pi native samples used a pre-commit platform build.
Their runtime `report()` fields, statechart scope text and diagnostic README
paragraph predate the committed build. They are not current-byte native samples.
Their validation function, command dispatcher and log helper are unchanged.
Only the dsh native sample used the committed platform bytes at bd04b21.
Per-workspace BUNDLE.json and platform-file SHA256 values are recorded in
`.tmp/platform-rollout/native-summary.json`. Independent direct checks of the
four current user installations used the committed bytes; these are distinct
from the native model-run samples.

Native Codex workspace-write initially failed to read skills because staging used
owner-only Windows temporary ACLs. A regression probe fails with the old staging
method and passes with parent inheritance, for both copy and new Junction versions.
The successful native rerun kept the same sandbox mode. No sandbox bypass or global
ACL change was used.

Official `log.sh` and the portable helper produced the same header and data cells
with a matching UTC timestamp format. Git Bash required its own `usr/bin` in the
child PATH to find `dirname`; its absolute executable path alone was insufficient.
This does not validate the networked worktree audit or statechart process cleanup.

The initial dsh headless invocation could not resolve its existing
`deepseek-official` credential. Passing the existing stored reference through the
documented child-process environment allowed the same route to serve the request.
No credential value was printed or persisted, and no account or provider settings
were changed. Its shell tool then failed before execution with
`SetNamedSecurityInfoW failed (Win32 5): grantWrite(...)`. A fresh workspace outside
this repository reproduced the failure. The tool refused full-access escalation
without an approval channel; no bypass was used.

Granting explicit FullControl only to the current owner of that disposable
workspace allowed its unchanged sandbox to start PowerShell. No global ACL,
SandboxUsers grant, real project ACL, or sandbox mode was changed. Within that
sandbox, Git Bash still failed to create its MSYS signal pipe with Win32 error 5.
The agent then used its existing bundled Python to run the installed platform
logger and produced the exact requested fields. dsh passed this logging-command
case with these environment prerequisites. Its default headless credential lookup
and other D-drive workspaces were not permanently repaired by this validation.

All four current user installations were updated with copy storage and verified
against their ownership receipts. Codex and Claude retain 63 managed skills;
Pi and dsh retain 58. Claude retains its two named agents. Native discovery confirms
the managed entries, with no loader diagnostics. Selected configuration hashes
match the verified pre-update backup. Each host has an installer rollback backup.
The native Codex CLI also refreshed two SDK-owned system-skill files at startup.
This was separate from the installer's managed-entry updates. Their previous
hashes and paths remain in the private backup and rollout evidence.

Local event streams, run requests, staging regression output and backup receipts
are in `.tmp/platform-rollout/`. These can contain local host information and stay
private. Installation and reviewer receipts are recorded there as rollout proceeds.

## Common platform layer on 2026-11-07

The platform registry and launcher are outside the official source. The source
verifier still finds 573 matching files and 58 official skills.

- The full regression run passed 74 tests. After the final review fixes, the
  affected suites passed again: 7 platform tests, 4 portable-helper tests and
  20 packaging tests. The focused tests include the added log regression case
  and script-coverage cases.
- All four host projections link to the same execution contract in copy and
  Junction storage. Tests execute the installed launcher in isolated copy and
  Junction homes, including paths with spaces. No current user install is changed.
- The portable log command appends sanitized TSV. Values beginning with `-h`,
  `-x` and `--foo` remain data. Literal quotes and UTC second timestamps match the
  shell log format. Claude Opus 5.5 review exposed the option-parsing defect;
  the parent reran the regression against the corrected helper.
- The unchanged private Node plan checker succeeds on a valid fixture, reports
  an invalid fixture and preserves exit codes. Public bundle execution is refused.
- The reduced worktree audit reports unknown merge/deletion facts without writing
  the repository. It is not the full upstream shell audit.
- Stale upstream/hash mappings and missing or escaped helper paths stop packaging.
  The runtime also refuses changed mapped source files and unverified workflows.
- New script paths outside mapped files or declared tool directories stop
  packaging even when source-lock already records their correct hashes. Tests
  show assignment allows the build and tool directories cover unhashed fixtures.

The manifest binds adaptation targets and critical launch/process files. It does
not duplicate the full source inventory or bind every upstream test fixture.
The complete official tree remains checked by source-lock and packaging.

The check command reports executable locations, not runtime compatibility proof.
No watcher, TLC/Java process lifecycle, WSL workflow, GitHub operation or model
business workflow was run for this validation. Those remain separate acceptance
work. See the [platform contract](../adapters/platforms/README.md) for commands
and the [platform tests](../tests/test_platforms.py) for the runnable checks.

## Junction installer sandbox validation

This earlier validation did not update current user installations. The later
copy rollout is recorded above. Junction mode remains opt-in. At this earlier
checkpoint, all four resource manifests, skill hashes and agent hashes were unchanged.
The official source still matches the same 573-file Git blob inventory.

- Full suite: 66 unittest checks pass, including 16 Junction-specific cases.
- Real Windows Junctions tested on one volume and across C: host entries to D: resources.
- Four isolated hosts share one content-addressed resource version while retaining
  host-specific invocation metadata and private script directories.
- Existing valid Markdown references are readable through logical and resolved
  paths. The architect-to-arena link resolves to the adapted host entry.
- Copy migration, repeated install, version update/restore, uninstall/restore,
  receipt publish failure, link creation failure, lock conflict and changed-target
  refusal pass. Cleanup removes links without deleting their shared targets.
- Backups include the external receipt and materialize shared resource contents.
- Codex app-server finds 58 isolated user skills with no loader errors. Claude SDK
  initialization lists 58 commands and the two named agents. Pi's installed loader
  and dsh's installed filesystem provider each read 58 entries without diagnostics.
  dsh also loads the projected how body. No model workflow/API call was made.

Review found that poteto-mode tools install dependencies beside bootstrap.ts.
All scripts directories therefore remain private. A fixture writes the expected
node_modules cache and verifies update archives it without changing public content.
This fixture does not run Bun or install dependencies. Cross-skill document
references remain private when sharing would change the resolved target.

The public store is hash-checked, not ACL-protected. Direct execution of mutable
raw bundled scripts is unsupported; use the private host entry paths. Public
versions are retained after uninstall and failed installs; there is no automatic GC.
Copy storage remains the default and no current user installation was converted.


## Official-source reset on 2026-11-07

The source now matches all 573 Git blobs from official cursor/plugins commit
6b0300214a09fd6029cfb7077043125758cd1fd2. The lock is external at
[source-lock.json](../source-lock.json). The mirror is a mapping reference only.
Earlier results below describe the former customized distribution, not this source.

| Check | Observed result |
| --- | --- |
| Repository tests | 50 unittest checks pass; backup checks rerun after expanding the selected host roots |
| Canonical source | All 573 paths and SHA256 hashes match; 58 entrypoints |
| Backup | 3,467 installation/configuration files verified before reset; repository Git bundle retained privately |
| Old install cleanup | 131 owned paths archived; four locally modified Claude statechart files retained |
| Protected files | 363 unrelated selected files unchanged after migration |
| Codex native discovery | app-server skills/list finds all 63 managed user skills in ~/.codex/skills, no loader errors |
| Claude native discovery | SDK initialization lists all 63 managed commands plus poteto-agent and comment-sicko |
| Pi native loader | Installed Pi loadSkills reads all 58 managed entries from default roots, zero diagnostics |
| dsh native provider | Installed filesystem provider reads all 58 managed entries, zero warnings; loads poteto-mode body with adapter |
| Installed integrity | All four managed skill/agent inventories match installation manifests |
| Model configuration | Two fresh role files use inherit-parent; no provider or model switched |

Codex and Claude retain five independent supplements. Pi and dsh are clean
58-skill installs. Each user host has a separate directory. The native Pi/dsh
checks exercise their installed parser/provider modules; they do not prove the
currently open application session has refreshed or that a model executed a
workflow. No model/API request was needed for discovery checks.

Native Windows scripts, WSL execution, model-specific delegation and diverse-model
review are not verified by this reset. No Windows Job experimental code or mirror
workflow-policy patch is included. Model roles intentionally inherit until setup
is run against the actual host schema.

## Historical validation of the previous distribution


Checked on Windows on 2026-11-03 against the local adaptation on
`codex/pstack-host-adaptation`, based on library commit `61c9e1f`, pstack 0.15.36,
Cursor snapshot `ae5650f`, and portable mirror `6c75f4e`.
Exact upstream hashes are in [historical source lock](https://github.com/Celestia-Milara/skills/blob/cfd8c0f/pstack/source-lock.json).

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

## Statechart on Windows

Checked on Windows 11 on 2026-11-05 with Node 24.20, mise 2026.11.2, Temurin 25,
and TLC 1.7.4. The command found TLC and Java through mise, with no overrides.

| Check | Observed result |
| --- | --- |
| Real check | A 32-state spec with two broken rules exits 1 and draws the chart; repeated runs give the same `chart.mmd` |
| Stop mid-run | Killing the command stops TLC and removes its stage and temporary folders; nothing is written |
| Console windows | A hidden run opens no console window for its worker, janitor, mise, Java, or `taskkill` |
| CRLF output | The new `messages.test.ts` case fails before the fix and passes after it |
| Linux regression | WSL Ubuntu 24.04: the patched and original suites both fail only `render.test.ts`; 194 and 193 tests pass |

The suite's fake `java` is a `.ts` file. Windows cannot run it directly, so the
CLI and corpus tests fail there with `spawn EFTYPE` before and after this change.
The signal tests use POSIX signals and do not apply to Windows.

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

## Git workflow ownership follow-up on 2026-11-03

The user authorized rule changes and verification, with no commit this round.
The [adaptation audit](adaptation.md#original-guidance-conflict-audit) records the
active original-guidance comparison and resulting ownership. Pre-existing installer
and backup migration edits remain outside this round's changes.

- All 18 local tests passed after the route changes. The installed-guidance test
  now resolves collaboration, verification, and Git links on both hosts.
- Source checks passed with 63 active skills, 573 original paths, 582 mirror files,
  and 77 adapted source files. No broken references or invocation errors were found.
- The four changed skill entry points passed Skill Creator validation on normalized
  Codex copies. The later Interrogate wording clarification retains the same scope.
- Diff whitespace checks passed. The real repository index stayed empty and HEAD
  stayed at `c22500affd1ae57c15cf764b61ec6888b9ef966f`. No push or merge ran.

### Native behavior and independent review

[Git validation procedures](../agent-guidance/validation.md#git-protection-and-pickup-checks)
provide the runner commands. Four native runs used complete project installations
in separate temporary fixtures, with no optional project guidance or delegation.
Hosts were Codex CLI 0.166.0-alpha.5.1 and Claude Code 2.1.310. Seed history was
created only in those fixtures; model tasks were instructed not to commit or publish. Both hosts exited normally and all artifact assertions passed.

| Case | Observed result |
| --- | --- |
| Codex and Claude Code: pickup with stale success report | Read the current code, found the reported fix absent, reproduced and corrected zero handling without another implementation approval. Preserved adjacent behavior. |
| Same pickup fixtures: staged and mixed-file work | Retained HEAD, the complete index, unrelated user-file bytes, and staged plus unstaged comments in the edited file. Left the fix uncommitted. |
| Codex and Claude Code: obsolete worktree with user files | Inspected untracked and ignored files; held the candidate because disposal authority and active-use evidence were missing. Retained both files and worktree registrations. |
| Fresh-context independent static review | Reported a workflow event trigger that contradicted the fixture requirements in a separate static-evidence section. Reported no run-proven findings with GitHub execution unavailable; made no edits. |

Actual events show each native host reading its adapter, composition rules, and
matching pickup or cleanup playbook. Codex also read the Git method owner. Commands,
source changes, and post-run probes support the reported outcomes; final replies
alone were not treated as proof. Claude refreshed stat data in the cleanup
candidate's index, but did not change its tracked content or remove user files.

The first three cases used bundle manifest SHA-256
`4ef1621539a1d6e48a6ad252cf993f74f7a86e99b41634140ed9c44e09ab96fe`.
Codex cleanup used
`ae8ee2e1eb85f93f65d70b9a85bff24b41fca50dd4b9474d543c448c4ff28b06`.
The difference includes the delivery clarification that failing-before evidence
need not be a separately failing commit. That delivery choice was reviewed, not
executed in these local-only cases. The later Interrogate description clarification
also did not trigger another native run. Raw prompts, events, fixture locations,
and checks remain local under `.tmp/git-ownership-round/`; do not publish raw logs.

Authorized commit, amend, push, PR creation, shared-history rewrite, actual deletion,
and merge paths were not exercised. Independent review was a single fresh-context
pass, not a diverse-model panel. These cases test specific behaviors, not a
permission enforcement mechanism. Personal installations and other project copies
were not updated.

### Git ownership publication snapshot

The user subsequently authorized committing and pushing this round to the current
feature branch, without merging into main. The selected snapshot excludes the
previous installation migration. It passed all 12 tests available without that
migration and the source/reference verifier. The 18-test result above belongs to
the full local worktree. Native behavior evidence was reused; publication selection
did not change the tested workflow rules. Installation migration edits and raw
host logs remain outside this commit.
