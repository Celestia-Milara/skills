# Continuous integration

The [CI workflow](../.github/workflows/ci.yml) checks pull requests, pushes to
`main`, and manual runs. The jobs use GitHub-hosted runners and need no host
account or repository secret.

## Automated checks

| Job | Environment | Checks |
| --- | --- | --- |
| Library | Ubuntu with Python 3.10 and 3.12; Windows with Python 3.12 | Source completeness, source-lock changes, archive hashes, skill metadata, maintained Markdown links, packaging, installation, portable helpers, and patch whitespace |
| Tools | Ubuntu with Bun 1.3.14 and Node 24 | Complete PR watcher and plan-checker unit suites, type checks, CLI help, and statechart message tests |
| Tools | Windows with Bun 1.3.14 and Node 24 | CLI, policy, and plan-checker unit suites, type checks, CLI help, and statechart message tests |

The library suite uses Python's standard library and Git. Its installer tests
write to temporary fixture projects. They do not update personal installations.
The selected tool tests use fake GitHub responses. They do not merge PRs or send
messages. Windows excludes `watch-pr/github.test.ts` because its fake `gh`
program uses a POSIX shell and a colon-separated PATH. Ubuntu runs that entire
suite. Making the fixture portable is separate work.
The plan-checker tests start Node subprocesses, so the tool jobs install Node
explicitly as well as Bun.

Every job has a ten-minute timeout. A newer run cancels the previous run for the
same PR or branch. Actions use full commit hashes. Checkout does not retain Git
credentials, and the workflow token has only `contents: read` permission.

[Dependabot configuration](../.github/dependabot.yml) checks Actions monthly and
groups updates into one PR. Imported package dependencies remain under the
[source update procedure](adaptation.md#updating-source).

## Run the checks locally

Run the library checks from the repository root:

```powershell
python scripts/verify.py
python -m unittest discover -s tests -v
git diff --check
```

Run the tool checks from `pstack/skills/poteto-mode/scripts`:

```powershell
bun install --frozen-lockfile
bun run test
bun run typecheck
```

On Windows, replace `bun run test` with the selected portable suites:

```powershell
bun test watch-pr/cli.test.ts watch-pr/policy.test.ts check-plan.test.ts
```

Both systems also run `bun watch-pr/watch-pr --help` from that directory.
From the repository root, both run the statechart message tests with Node 24:

```powershell
node --disable-warning=ExperimentalWarning --test pstack/skills/statechart/scripts/test/messages.test.ts
```

These tests include CRLF parsing. They need no Java or TLC installation.

CI checks patch whitespace with `git diff --check HEAD^ HEAD`. For a pull request,
the default checkout is GitHub's merge commit. Its first parent is the base tip.

## Checks that remain separate

CI does not run native Codex or Claude tasks, personal installation migrations,
the full statechart toolchain, or external watcher acceptance. Those checks need
their own dependencies and side-effect review. Use the
[host validation methods](../agent-guidance/validation.md) and retain results in
[validation evidence](validation.md). A green CI run does not establish model
behavior, Windows process cleanup, or Java/TLC acceptance.

A live watcher needs an authenticated `gh` command with access to the repository.
Its first launch installs locked dependencies in the scripts directory and
restarts the command. That launch needs a writable directory and either cached
packages or registry access, including when you request help.

## Merge policy recommendation

After the first successful hosted run, require the Library and Tools checks in a
`main` branch ruleset. Require resolved review conversations and block force
pushes and branch deletion. Keep the check names in step with the workflow matrix.
Independent review remains necessary for behavior changes.

These are recommended settings. The workflow does not change repository rules,
enable automatic merges, deploy packages, or publish releases.

The configuration follows GitHub's
[workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
and [Dependabot options](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference).
