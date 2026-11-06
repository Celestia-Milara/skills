import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { test } from "node:test";
import { pathToFileURL } from "node:url";

const scripts = path.resolve(import.meta.dirname, "..");
const scratch = path.resolve(scripts, "../../../../.tmp/audit-host");

test("native Windows rejects the CLI before writes, workers, or tool installation", {
  skip: process.platform !== "win32",
}, () => {
  fs.mkdirSync(scratch, { recursive: true });
  const fixture = fs.mkdtempSync(path.join(scratch, "statechart-platform-"));
  try {
    const corpus = path.join(import.meta.dirname, "corpus/Login");
    for (const args of [[path.join(corpus, "Login.tla"), "--out", path.join(fixture, "out")], []]) {
      // The real Node permission boundary forbids writes and child creation. A
      // misplaced platform check therefore produces a permission error instead.
      const result = spawnSync(process.execPath, [
        "--permission", "--allow-fs-read=*", "--disable-warning=ExperimentalWarning",
        path.join(scripts, "statechart.ts"), ...args,
      ], {
        cwd: fixture,
        encoding: "utf8",
        timeout: 5_000,
        env: {
          ...process.env, NODE_OPTIONS: "", NODE_COMPILE_CACHE: "", NODE_DISABLE_COMPILE_CACHE: "1",
          TMPDIR: fixture, TMP: fixture, TEMP: fixture, TLA2TOOLS: "", JAVA: "",
        },
      });
      assert.ifError(result.error);
      assert.equal(result.signal, null);
      assert.equal(result.status, 2, result.stderr);
      assert.equal(result.stdout, "");
      assert.match(result.stderr, /statechart does not support native Windows/);
      assert.match(result.stderr, /POSIX/);
      assert.doesNotMatch(result.stderr, /ENOENT|Unhandled|ERR_ACCESS_DENIED|permission denied/i);
      assert.deepEqual(fs.readdirSync(fixture), []);
    }
  } finally {
    fs.rmSync(fixture, { recursive: true, force: true });
  }
});

test("POSIX argument validation still reports usage", { skip: process.platform === "win32" }, () => {
  const result = spawnSync(process.execPath, [path.join(scripts, "statechart.ts")], {
    encoding: "utf8", timeout: 5_000, env: { ...process.env, NODE_OPTIONS: "" },
  });
  assert.ifError(result.error);
  assert.equal(result.status, 2);
  assert.match(result.stderr, /Give one SPEC.tla/);
  assert.doesNotMatch(result.stderr, /does not support native Windows/);
});

test("killGroup rejects a missing shell without an unhandled error event", {
  skip: process.platform !== "win32" || fs.existsSync("/bin/sh"),
}, () => {
  const source = `
import assert from "node:assert/strict";
import { killGroup } from ${JSON.stringify(pathToFileURL(path.join(scripts, "run.ts")).href)};
await assert.rejects(killGroup(2147483647), { code: "ENOENT" });
console.log("missing shell rejected");
`;
  const result = spawnSync(process.execPath, ["--input-type=module", "--eval", source], {
    encoding: "utf8", timeout: 5_000, env: { ...process.env, NODE_OPTIONS: "" },
  });
  assert.ifError(result.error);
  assert.equal(result.status, 0, result.stderr);
  assert.equal(result.stdout.trim(), "missing shell rejected");
  assert.equal(result.stderr, "");
});
