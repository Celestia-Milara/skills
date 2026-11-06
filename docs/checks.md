# Run repository checks

Run these checks manually from the repository root. The repository does not
configure GitHub Actions workflows or Dependabot updates.

## Check the library

The library checks need Python 3.10 or later and Git:

```powershell
python scripts/verify.py
python -m unittest discover -s tests -v
git diff --check
```

The verifier checks source completeness, source-lock changes, archive hashes,
skill metadata, and maintained Markdown links. The tests cover packaging,
installation, portable helpers, and dependency-document exclusion. Installer
tests write temporary fixture projects and leave personal installations intact.

## Check the portable tools

The checked tool versions are Bun 1.3.14 and Node 24. Run the following commands
from `pstack/skills/poteto-mode/scripts` on Linux:

```powershell
bun install --frozen-lockfile
bun run test
bun run typecheck
bun watch-pr/watch-pr --help
```

On Windows, replace `bun run test` with the portable suites:

```powershell
bun test watch-pr/cli.test.ts watch-pr/policy.test.ts check-plan.test.ts
```

The complete Windows suite has a known failure in `watch-pr/github.test.ts`.
Its fake `gh` program uses a POSIX shell and a colon-separated PATH. The Windows
selection excludes that file, including its otherwise portable parser tests.
Linux runs the full suite. The selected tests use fake GitHub responses and do
not merge PRs or send messages. Plan tests also start Node subprocesses.

From the repository root, check statechart message parsing with Node 24:

```powershell
node --disable-warning=ExperimentalWarning --test pstack/skills/statechart/scripts/test/messages.test.ts
```

These tests include CRLF parsing and need no Java or TLC installation.

## Check host and external behavior separately

The commands above do not establish native model behavior, personal installation
migrations, the full statechart toolchain, Windows process cleanup, or external
watcher acceptance. Use the [host validation methods](../agent-guidance/validation.md)
and record results in [validation evidence](validation.md).

A live watcher needs an authenticated `gh` command with repository access.
Its first launch installs locked dependencies in the scripts directory and
restarts the command. That launch needs a writable directory and either cached
packages or registry access, including when you request help.
