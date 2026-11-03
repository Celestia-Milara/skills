# Validation Methods and Environment Notes

The root [README](../README.md#verified-host-behavior) owns dated host results. This page owns validation procedures and environment troubleshooting. Past runs do not validate later package changes.

## Host loading and behavior checks

Use isolated fixture projects and complete package copies. Retain the source revision or exact local snapshot, request, artifacts, and output. Keep credentials and unrelated environment data out of retained evidence. Do not change the user's installed packages or host settings just to prepare a fixture.

Check discovery and behavior separately:

1. Record the host version, package scope, effective instruction files, and loading configuration.
2. Use the host's actual initialization or inventory interface to inspect names and loader errors. Check a standalone package and the full set when affected.
3. Run a fresh-context task and inspect actual file reads or skill invocations. Judge the output and side effects against the task's requirements.
4. For experience reuse, preserve evidence in one session, then give a later session a relevant task without supplying the expected answer. Check retrieval and action, not just file creation.
5. Include changed conditions, unrelated work, missing and inaccessible history, and existing authorization. Verify that changed conditions permit reassessment and existing permission does not trigger repeated approval.

For Claude Code instruction loading, check the actual `AGENTS.md` / `CLAUDE.md` combination and relevant settings against [official documentation](https://code.claude.com/docs/en/memory#agentsmd). Test direct loading, coexisting files, and an existing `CLAUDE.md` importing `@AGENTS.md` when those layouts are used. In an interactive session, inspect `/context` for loaded memory files; also retain observed reads and actions. Check an absent optional history file without adding a broken import. These are test cases, not claims that every layout has passed.

For Codex, verify the configured instruction entry and skill inventory through the installed host. Preserve project and personal scope differences. Native host discovery, model task execution, and separate-agent forward tests establish different evidence; report each precisely.

Real-service checks follow [verification authorization](verification.md). Isolated local checks do not need a new approval stage. A model call through an external provider must remain within the authorized account and call scope. Do not infer permission for charges, notifications, or production writes.

Report failed, unrun, and constrained cases. Static links, metadata, scenario walkthroughs, fresh-context model runs, and real host checks do not substitute for one another. One successful task is not proof of general reliability.

## Combined workflow checks

Run the bounded native-host scenarios against the current source with a fresh
output directory under `.tmp/` for each run:

```powershell
python scripts/check_composition_behavior.py --host codex --output .tmp/composition-codex
python scripts/check_composition_behavior.py --host claude-code --output .tmp/composition-claude
```

The runner installs complete project packages in fresh temporary projects outside
this repository. It uses the existing host account and no optional project guidance.
It does not update personal installations. The three cases cover design-only work,
approved implementation, and an ordinary plan. Each request excludes delegation and
Git writes. A manifest hash identifies the tested bundle; raw host logs stay local.

Review the event log as well as the artifact checks. Confirm reads of the project
entry, shared and matching host adapters, composition guide, and applicable history
or document methods. Check that implementation uses the existing approval, ordinary
plans do not run the full-program checker, and designs/plans keep their owning
paths. Inspect actual edits, test output, and Git state. A final reply claiming these
actions is not sufficient. Record missing capabilities and any skipped workflow
steps separately from the composition result.

Use separate fresh-context forward tests for interview-to-document and safe-pause
handoffs. Give each a realistic request and raw fixture, without the desired result
or implementation rationale. Verify the files and Git state afterward. These are
independent model tests, not native-host discovery evidence or cross-model review.

## Git protection and pickup checks

Run the native cases with fresh local output directories:

```powershell
python scripts/check_git_behavior.py --host codex --output .tmp/git-codex
python scripts/check_git_behavior.py --host claude-code --output .tmp/git-claude
```

The runner seeds local commits only inside disposable fixtures, then installs the
complete current bundle. The model tasks may not commit or publish. The resume
case combines a stale success report, current broken code, unrelated staged work,
and staged plus unstaged edits in the same file. Check that the host fixes current
behavior, preserves the index and user edits, and honors the latest local-only
scope. The cleanup case has an obsolete linked worktree with untracked and ignored
user files and unknown activity. Check that unsupported deletion stays pending.

Artifact checks do not prove the whole workflow. Inspect command events for actual
adapter and playbook reads, unauthorized Git or deletion operations, and repeated
approval requests. Retain process failures and timeouts. These cases do not test
authorized commits, amendments, remote PRs, or merges. For static-review separation,
use a fresh reviewer on source and requirements with remote execution unavailable;
check that it reports supported static findings without calling them run-proven.

## Local gateway and isolated-test troubleshooting

If Claude Code uses a loopback gateway such as Magpie while inheriting `HTTP_PROXY` or `HTTPS_PROXY`, ensure `NO_PROXY` includes `localhost,127.0.0.1,::1`. Preserve existing exclusions when appending these entries; back up configuration before changing it. Claude Code can receive these values through the `env` object in its user settings. In the tested setup, adding both `NO_PROXY` and `no_proxy` resolved HTTP 502 responses without changing the model or gateway credentials. A direct gateway request alone does not establish that the CLI follows the same proxy path.

On Windows, an isolated Codex run using `--ignore-user-config` also discards the user's native sandbox configuration. In the tested setup, this caused a normal skill-file read to be rejected by command policy. Explicitly carrying over the configured `windows.sandbox` option restored file reads while retaining `--sandbox read-only`. Similarly, carry over the selected provider definition and explicitly select Magpie if the isolated test is meant to use that gateway. Keep credentials out of command arguments, reports, and repository files.

For read-only Claude Code invocation tests, retain `Glob` and `Grep` alongside `Read` and `Skill`; history and documentation workflows need to locate files as well as open them. Restricting the test to `Read,Skill` caused a history lookup to stall on guessed paths. With `dontAsk`, also grant access to the installed skills directory using `--add-dir` if bundled reference reads would otherwise require approval outside the working directory. The tested harness added only `~/.claude/skills` and retained its read-only tool set. See [Claude Code working directories](https://code.claude.com/docs/en/permissions#working-directories). These are test access constraints, not package-discovery failures.
