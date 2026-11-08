# Execution platforms

Host adapters map agent tools and models. This layer maps script execution.
The official files remain unchanged. Both copy and Junction installations include
this contract and the same platform registry. Generated skill entries link here.

Select the platform where the command runs. A Python process on Windows reports
Windows. Python inside WSL reports Linux or WSL. A Windows desktop alone does not
select the script platform. This layer does not enter WSL, translate paths, install
dependencies, or run an unverified fallback.

## Check without running workflows

Use Python 3.10+ and the absolute path to this directory:

```powershell
python -B "<bundle>/adapters/platforms/runtime.py" check
```

The command checks the pinned script hashes and executable locations. It does not
start Node, Bun, Java, Git, a watcher, or a model. `available` means the mapping and
dependency locations exist. It does not certify a complete workflow or a runtime
version. Missing or changed source files fail with exit code 2.
The report lists executable paths and Git Bash files beside the resolved Git
installation. It also identifies the standard per-user Bun binary when that
directory is not in the current process PATH. Unverified tools report
`missing_dependencies: null`; their complete requirements have not been assessed.
Finding Bash does not prove its Unix utilities are in PATH, or that a script's
process cleanup works on Windows. Shell discovery does not execute a shell.

The [registry](manifest.json) owns the tool inventory, source hashes, dependencies,
and scope. Packaging rejects mappings for a different pinned upstream revision or
file hash. Review mappings and their behavior tests when updating upstream. A
matching hash binds a mapping to its source; it is not compatibility evidence.
The registry hashes adaptation targets and critical launch/process files. The
complete upstream inventory stays in source-lock and is checked by packaging.
Every official `skills/*/scripts/` resource must belong to a hashed mapping target
or an explicit `coverage` entry. A trailing `/` covers one tool's directory,
including its tests and implementation files. Other entries cover one exact file.
New files inside a declared tool directory stay in that tool's scope; new script
paths outside all declared scopes stop packaging until assigned. Coverage does
not enable execution or claim Windows support.

## Run the portable subset

Use these commands in place of the corresponding shell commands on native Windows.
They also work in other Python environments. Quote each argument that contains
spaces. Arguments are passed as an array without a shell.

```powershell
python -B "<bundle>/adapters/platforms/runtime.py" run log "<log.tsv>" "<phase>" "<decision>" "<why>" "<evidence>" "<result>"
python -B "<bundle>/adapters/platforms/runtime.py" run worktree-audit "<repo>" --base "<ref>"
python -B "<bundle>/adapters/platforms/runtime.py" run --skills-root "<host-root>/skills" check-plan "<plan.md>"
```

`log` appends sanitized TSV rows through the existing Python helper. It takes the
six positional arguments of `show-me-your-work/scripts/log.sh`.

`worktree-audit` uses the existing Python helper. It returns local Git facts as JSON.
It does not fetch, contact GitHub, inspect transcripts, estimate sizes, or declare
a worktree safe to delete. This is a reduced audit, not a replacement for the
official shell report's table or its full cleanup procedure. Pass an explicit
`--base` for a known merge reference. Unknown facts remain unknown.

`check-plan` requires Node. It runs the unchanged official `check-plan.mjs` from
the explicit private skill directory. The launcher checks that script's hash and
returns its exit code. Use the host skill directory, not the raw bundled skills.
The explicit directory works with copy and Junction storage without deriving a
host path from a resolved shared resource path.

## Unverified workflows

`watch-pr`, `bootstrap`, and `statechart` appear in the registry but the launcher
refuses to run them. The watcher can contact GitHub. Bootstrap installs dependencies
beside its source. Statechart uses a POSIX janitor and process-group cleanup and
can provision TLC and Java. Their native Windows lifecycle still needs separate
verification against this pinned official source.

Historical Windows experiments do not certify these unchanged official scripts.
WSL is a possible future execution target, not an automatic fallback. Outside the
portable subset, use only an independently verified execution path with the task's
authorization. Writable tools must run from private host entries. Never use a
shared resource version as a tool working directory.
Run bundle Python tools with `-B`. Imports or tests that create `__pycache__` in a
managed bundle change its hashes and block later installation updates.
