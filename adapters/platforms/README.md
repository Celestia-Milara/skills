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
On Windows, executable discovery checks explicit PATH directories, excludes the
current directory and accepts `.exe` files. Statechart and check-plan use those
resolved binaries; a project-local `node.cmd` cannot become their runtime.

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
python -B "<bundle>/adapters/platforms/runtime.py" run --skills-root "<host-root>/skills" statechart "<Spec.tla>" --out "<new-output>"
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

## Statechart on Windows

The Windows adapter invokes the unchanged private `statechart/scripts/worker.ts`.
That worker owns model checking, rule reports and Mermaid generation. The adapter
owns the native process lifecycle and publication. It does not invoke the POSIX
shell wrapper or modify the official source. Other platforms use the official entry.
On native Windows, do not run `scripts/statechart` or `scripts/statechart.ts`
directly. Their POSIX cleanup can fail while detached Java processes keep running.
Use the mapped command above.

Use Python 3.10+, Node 22.18-22.x or 23.6+, Java 11+ and the pinned TLC 1.7.4 jar. The tested
combination is Python 3.12, Node 24.20, Java 25 and TLC 1.7.4. The adapter checks
runtime versions and the jar SHA256 before starting the check. It installs nothing.
`JAVA` and `TLA2TOOLS` select existing dependencies; `--java`, `--tlc` and `--node`
override paths for one command. Without `TLA2TOOLS`, the jar is read from
`~/.cache/pstack/tla2tools/1.7.4/tla2tools.jar`. Missing dependencies stop the command.

The command accepts the upstream `--config`, `--view` and `--out` options. For example:

```powershell
python -B "<bundle>/adapters/platforms/runtime.py" run --skills-root "<host-root>/skills" statechart "<Spec.tla>" --view "<view.mjs>" --out "<new-output>" --timeout-seconds 120 --evidence "<new-evidence-folder>"
```

The worker timeout defaults to zero, which means no time limit. Dependency probes,
file cleanup and output forwarding can take additional time. Evidence is optional;
its folder must be new and must not overlap the output folder. It retains worker
diagnostics and the cleanup receipt. Without this option, normal runs remove their
temporary evidence. Input models and view modules execute with the caller's
permissions; the Job contains processes and is not a security sandbox.

The worker starts inside a private kill-on-close Windows Job. Its Java descendants
remain in that Job. A separate guardian watches the launcher's stdin lifeline.
Timeout, cancellation or launcher death terminates the Job. Output is published
only after the worker exits 0 or 1, the guardian confirms zero active processes,
and private temporary files have been removed. Read-only files are handled with
bounded retries. An external file lock can prevent publication and returns 2 with
the retained diagnostic path. The guardian waits for publication or abandonment;
it does not delete staging on a fixed timer. Publication preserves a destination
that changes identity or becomes a new reparse point while the check runs.
Exit 0 means the configured rules hold; 1 means a rule breaks; 2 means execution
failed or timed out. A caught keyboard interrupt returns 130. Cleanup failures
before publication return an error. Cleanup failures after publication report a
warning and retain their paths; the completed checker result remains 0 or 1.
CLI text uses UTF-8, including when the parent requests a legacy console encoding.
Pipe output uses LF, and the worker's own stdout and stderr are forwarded.

For this worker only, an external Node `--import` module adds JVM arguments for
LF line separators and UTF-8 output to the checker's Java launches.
Windows Java otherwise emits CRLF that the pinned official message parser cannot
read correctly. This changes process arguments, not Java settings or source files.
It adds no `JAVA_TOOL_OPTIONS` diagnostic lines. This adapter supports Node;
Bun and Deno continue to belong to the official POSIX entry and are not Windows
fallbacks. The Node version range follows the upstream wrapper.

If the guardian itself is forcibly killed, closing its Job handle terminates the
worker tree. Staging and temporary files beside the output can remain and can be
large. Do not infer
directory cleanup from process termination. Windows does not expose POSIX signal
causes for external termination; an incomplete check returns 2. Missing dependencies
also return 2 instead of the shell wrapper's 127. No mise provisioning is attempted.
Ctrl+Break can terminate the launcher with Windows status `0xC000013A`; it is not
mapped to POSIX SIGTERM. The lifeline still stops the worker tree.

This adapter targets Windows 10/Server 2016 or newer. A host sandbox can still
deny Job creation or dependency execution. The adapter reports that failure and
does not change permissions, enter WSL, or disable the sandbox.

## Unverified workflows

`watch-pr` and `bootstrap` appear in the registry but the launcher
refuses to run them. The watcher can contact GitHub. Bootstrap installs dependencies
beside its source. Their native Windows lifecycle still needs separate verification.
PR monitoring is deferred. The original statechart POSIX entry can provision tools
through mise; the Windows adapter requires existing dependencies instead.

Historical Windows experiments do not certify these unchanged official scripts.
WSL is a possible future execution target, not an automatic fallback. Outside the
portable subset, use only an independently verified execution path with the task's
authorization. Writable tools must run from private host entries. Never use a
shared resource version as a tool working directory.
Run bundle Python tools with `-B`. Imports or tests that create `__pycache__` in a
managed bundle change its hashes and block later installation updates.
