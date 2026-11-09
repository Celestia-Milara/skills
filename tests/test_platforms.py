import csv
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from install import install
from package import ROOT, digest
from junction_install import remove_local_tree

RUNTIME = ROOT / 'adapters/platforms/runtime.py'
VALID_PLAN = '''# Platform verification

## How to read this
One box is one unit of work and names the evidence.
Check a box only when its evidence exists. See playbooks/.
Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.

## Program checklist
### Arm the program
### Spawn owners
### PR mechanics
### Verdict and merge
### Boot recipe
`git show origin/main:` /loop 1h status message

## PR 1
**Depends on.** None.
**Files.**
- [ ] Record the changed files.
**Build.**
- [ ] Generate the entries.
**You see.**
- [ ] Open the entries.
**Verify, unit.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.
- [ ] Save the unit results.
**Verify, live.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked. Ten lanes on `local-fixture` at the PR head
{lanes}
**Verify, perf.** Tests alone are not sufficient verification. A PR is verified only when its unit, live, and perf boxes are all checked.
- [ ] Metric. Run duration.
- [ ] Probe. Local command.
- [ ] Baseline. Previous result.
- [ ] Rule. No regression.
**Review gate.**
- [ ] The operator checks screenshot and video evidence.
**Merge.**
- [ ] Merge only when authorized.

## Close the program
Record the outcome.

## Appendix Prototype evidence
Local command output.
'''.replace('{lanes}', '\n'.join(f'- [ ] Lane {i}. Save `lane-{i}.txt`. Pass when evidence exists.' for i in range(1, 11)))
spec = importlib.util.spec_from_file_location('platform_runtime', RUNTIME)
runtime = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runtime)


class Platforms(unittest.TestCase):
    def call(self, launcher, *args):
        return subprocess.run([sys.executable, '-B', str(launcher), *map(str, args)],
                              capture_output=True, text=True, encoding='utf-8', timeout=30)

    def test_registry_binds_all_tool_families_to_the_pinned_source(self):
        record = runtime.validate()
        lock = json.loads((ROOT / 'source-lock.json').read_text())['upstream']
        self.assertEqual(record['upstream'], lock['commit'])
        self.assertEqual(set(record['tools']), {'log', 'worktree-audit', 'check-plan', 'statechart', 'watch-pr', 'bootstrap'})
        for tool in record['tools'].values():
            self.assertTrue(tool['sources'])
            self.assertTrue(all(lock['files'][p] == h for p, h in tool['sources'].items()))

    def test_changed_script_stops_mapping_before_any_helper_runs(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / 'pstack/skills', root / 'skills')
            (root / 'skills/show-me-your-work/scripts/log.sh').write_text('changed')
            with self.assertRaisesRegex(ValueError, 'mapping is stale: log'):
                runtime.validate(root)

    def test_unverified_and_unknown_commands_are_rejected(self):
        for name in ['watch-pr', 'bootstrap', 'unknown']:
            result = self.call(RUNTIME, 'run', name)
            self.assertEqual(result.returncode, 2)
            self.assertIn('No verified portable mapping', result.stderr)

    def test_doctor_is_read_only_and_distinguishes_unverified_tools(self):
        before = {p: digest(p) for p in (ROOT / 'adapters').rglob('*') if p.is_file()}
        result = self.call(RUNTIME, 'check')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(json.loads(result.stdout)['tools']['statechart']['status'],
                      ['available', 'missing-dependencies'] if os.name == 'nt' else ['unverified'])
        self.assertEqual(before, {p: digest(p) for p in (ROOT / 'adapters').rglob('*') if p.is_file()})

    def test_doctor_separates_missing_commands_from_unverified_requirements(self):
        with patch.object(runtime, 'find_executable', return_value=None):
            report = runtime.report(runtime.validate())
        self.assertIsNone(report['executables']['java'])
        if os.name == 'nt':
            self.assertIn('node', report['tools']['statechart']['missing_dependencies'])
            self.assertEqual(report['tools']['statechart']['status'], 'missing-dependencies')
        else:
            self.assertIsNone(report['tools']['statechart']['missing_dependencies'])
            self.assertEqual(report['tools']['statechart']['status'], 'unverified')
        self.assertEqual(report['tools']['check-plan']['missing_dependencies'], ['node'])

    def test_installed_launcher_preserves_arguments_and_native_exit_codes(self):
        for storage in ['copy'] + (['junction'] if os.name == 'nt' else []):
            with self.subTest(storage=storage):
                scratch = ROOT / '.tmp/platform-tests'
                scratch.mkdir(parents=True, exist_ok=True)
                base = Path(tempfile.mkdtemp(prefix='with spaces ', dir=scratch)).resolve()
                try:
                    install('codex', scope='user', home=base / 'home', storage=storage,
                            **({'store': base / 'store'} if storage == 'junction' else {}))
                    host = base / 'home/.codex'
                    launcher = host / 'pstack/adapters/platforms/runtime.py'
                    public_before = {p: digest(p) for p in (host / 'pstack').rglob('*') if p.is_file()}
                    logfile = base / 'log with spaces.tsv'
                    result = self.call(launcher, 'run', 'log', logfile, 'phase', '=formula', 'why\nnew', 'evidence & literal', 'done')
                    self.assertEqual(result.returncode, 0, result.stderr)
                    with logfile.open(encoding='utf-8', newline='') as stream:
                        rows = list(csv.reader(stream, delimiter='\t'))
                    self.assertEqual(rows[1][1:], ['phase', "'=formula", 'why new', 'evidence & literal', 'done'])
                    if shutil.which('node'):
                        plan = base / 'invalid plan.md'
                        plan.write_text('# Missing required sections\n', encoding='utf-8')
                        result = self.call(launcher, 'run', '--skills-root', host / 'skills', 'check-plan', plan)
                        self.assertEqual(result.returncode, 1, result.stderr)
                        self.assertIn('problems', result.stdout)
                        plan.write_text(VALID_PLAN, encoding='utf-8')
                        result = self.call(launcher, 'run', '--skills-root', host / 'skills', 'check-plan', plan)
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertIn('0 problems', result.stdout)
                        result = self.call(launcher, 'run', '--skills-root', host / 'skills', 'check-plan')
                        self.assertEqual(result.returncode, 2)
                        self.assertIn('Usage: node check-plan.mjs', result.stderr)
                        result = self.call(launcher, 'run', '--skills-root', host / 'pstack/skills', 'check-plan', plan)
                        self.assertEqual(result.returncode, 2)
                        self.assertIn('private host entries', result.stderr)
                    self.assertEqual(public_before, {p: digest(p) for p in (host / 'pstack').rglob('*') if p.is_file()})
                finally:
                    remove_local_tree(base)

    def test_worktree_audit_launcher_returns_local_facts_without_writing(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / 'repo with spaces'
            repo.mkdir()
            subprocess.run(['git', '-C', str(repo), 'init'], capture_output=True, check=True)
            before = {p.relative_to(repo): p.read_bytes() for p in repo.rglob('*') if p.is_file()}
            result = self.call(RUNTIME, 'run', 'worktree-audit', repo, '--base', 'missing-ref')
            self.assertEqual(result.returncode, 0, result.stderr)
            row = json.loads(result.stdout)[0]
            self.assertIsNone(row['merged'])
            self.assertEqual(row['safe_to_delete'], 'NOT_ESTABLISHED')
            self.assertEqual(before, {p.relative_to(repo): p.read_bytes() for p in repo.rglob('*') if p.is_file()})

    def test_log_treats_option_like_values_as_literal_data(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'log.tsv'
            for value in ['-x', '-h', '--foo']:
                result = self.call(RUNTIME, 'run', 'log', path, value, 'say "hi"', 'why', 'evidence', 'done')
                self.assertEqual(result.returncode, 0, result.stderr)
            rows = [line.split('\t') for line in path.read_text(encoding='utf-8').splitlines()]
            self.assertEqual([row[1] for row in rows[1:]], ["'-x", "'-h", "'--foo"])
            self.assertTrue(all(row[2] == 'say "hi"' for row in rows[1:]))
            self.assertRegex(rows[1][0], r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')


if __name__ == '__main__':
    unittest.main()
