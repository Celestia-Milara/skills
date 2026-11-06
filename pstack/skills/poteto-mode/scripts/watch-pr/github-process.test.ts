import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { test } from "node:test";

function withoutCommands(program: string): unknown {
  const directory = mkdtempSync(join(tmpdir(), "watch-pr-missing-command-"));
  try {
    const probe = join(directory, "probe.mjs");
    writeFileSync(probe, program);
    const env = Object.fromEntries(
      Object.entries(process.env).filter(([key]) => key.toUpperCase() !== "PATH")
    );
    const child = spawnSync(process.execPath, [probe], {
      cwd: directory,
      env: { ...env, PATH: directory },
      encoding: "utf8",
      timeout: 10_000,
    });
    assert.ifError(child.error);
    assert.equal(child.status, 0, child.stderr);
    return JSON.parse(child.stdout);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
}

const github = JSON.stringify(new URL("./github.ts", import.meta.url).href);
const policy = JSON.stringify(new URL("./policy.ts", import.meta.url).href);

test("missing gh and git executables produce structured query failures", () => {
  const result = withoutCommands(`
    import { GhGitHubReader, WatcherQueryError } from ${github};
    const reader = new GhGitHubReader();
    const context = { owner: "offline", repo: "fixture", number: 1 };
    const errors = [];
    for (const request of [() => reader.pullRequest(context),
                          () => reader.checksFastPath(context),
                          () => reader.originRepo()]) {
      try { await request(); errors.push({ unexpectedSuccess: true }); }
      catch (error) { errors.push({ structured: error instanceof WatcherQueryError,
                                   failure: error.failure }); }
    }
    console.log(JSON.stringify(errors));
  `) as { structured: boolean; failure: { kind: string; code: number; detail: string } }[];
  assert.equal(result.length, 3);
  for (const [index, error] of result.entries()) {
    assert.equal(error.structured, true);
    assert.equal(error.failure.kind, "command-exit");
    assert.equal(error.failure.code, -1); // No process exit status exists.
    assert.match(error.failure.detail, /ENOENT/);
    assert.ok(error.failure.detail.includes(index === 2 ? "git" : "gh"));
  }
});

test("the watcher returns its status-query blocker when commands cannot start", () => {
  const result = withoutCommands(`
    import { GhGitHubReader } from ${github};
    import { runSimple } from ${policy};
    let now = 0;
    const events = [];
    const verdict = await runSimple({
      dependencies: {
        reader: new GhGitHubReader(),
        clock: { now: () => now, observedAt: () => new Date(0).toISOString(),
                 sleep: async (seconds) => { now += seconds; } },
        emit: (event) => events.push(event.kind),
      },
      contexts: [{ owner: "offline", repo: "fixture", number: 1 }],
      mode: "single", statusOnly: false,
      options: { interval: 1, sweepInterval: 1, timeout: 0,
                 maxQueryErrors: 2, allowDraft: false },
    });
    console.log(JSON.stringify({ verdict, events }));
  `) as { verdict: { kind: string; exitCode: number; blocker: { kind: string; failures: number } }; events: string[] };
  assert.equal(result.verdict.kind, "BLOCKER");
  assert.equal(result.verdict.exitCode, 7);
  assert.equal(result.verdict.blocker.kind, "status-query");
  assert.equal(result.verdict.blocker.failures, 2);
  assert.deepEqual(result.events, ["RETRY"]);
});
