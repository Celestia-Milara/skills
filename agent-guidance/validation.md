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

## Local gateway and isolated-test troubleshooting

If Claude Code uses a loopback gateway such as Magpie while inheriting `HTTP_PROXY` or `HTTPS_PROXY`, ensure `NO_PROXY` includes `localhost,127.0.0.1,::1`. Preserve existing exclusions when appending these entries; back up configuration before changing it. Claude Code can receive these values through the `env` object in its user settings. In the tested setup, adding both `NO_PROXY` and `no_proxy` resolved HTTP 502 responses without changing the model or gateway credentials. A direct gateway request alone does not establish that the CLI follows the same proxy path.

On Windows, an isolated Codex run using `--ignore-user-config` also discards the user's native sandbox configuration. In the tested setup, this caused a normal skill-file read to be rejected by command policy. Explicitly carrying over the configured `windows.sandbox` option restored file reads while retaining `--sandbox read-only`. Similarly, carry over the selected provider definition and explicitly select Magpie if the isolated test is meant to use that gateway. Keep credentials out of command arguments, reports, and repository files.

For read-only Claude Code invocation tests, retain `Glob` and `Grep` alongside `Read` and `Skill`; history and documentation workflows need to locate files as well as open them. Restricting the test to `Read,Skill` caused a history lookup to stall on guessed paths. With `dontAsk`, also grant access to the installed skills directory using `--add-dir` if bundled reference reads would otherwise require approval outside the working directory. The tested harness added only `~/.claude/skills` and retained its read-only tool set. See [Claude Code working directories](https://code.claude.com/docs/en/permissions#working-directories). These are test access constraints, not package-discovery failures.
