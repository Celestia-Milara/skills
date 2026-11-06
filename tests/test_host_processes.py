"""Local fake hosts only. Never invoke an installed model CLI."""
import contextlib
import gc
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest
import warnings
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import check_composition_behavior as composition
import check_git_behavior as git_behavior
import check_host_inventory as host_inventory
import host_process

SCRATCH = ROOT / '.tmp/audit-host'


def stop_fixture(process):
    if os.name == 'nt':
        subprocess.run(['taskkill', '/PID', str(process.pid), '/T', '/F'], capture_output=True, timeout=5)
    else:
        import signal
        with contextlib.suppress(ProcessLookupError):
            os.killpg(process.pid, signal.SIGKILL)
    process.wait(timeout=5)


class HostProcesses(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, name, text):
        target = self.root / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
        return target

    def npm(self, host, bin_value):
        name, package = ('codex', '@openai/codex') if host == 'codex' else ('claude', '@anthropic-ai/claude-code')
        shim = self.write(f'bin with spaces/{name}.cmd', '@echo off\nexit /b 99\n')
        entry = self.write(f'bin with spaces/node_modules/{package}/cli.js', '// local fixture\n')
        self.write(f'bin with spaces/node_modules/{package}/package.json', json.dumps({'bin': bin_value}))
        return shim, entry

    def test_codex_npm_shim_resolves_to_declared_entry(self):
        shim, entry = self.npm('codex', {'codex': 'cli.js'})
        with patch('shutil.which', side_effect=lambda name: str(shim) if name == 'codex' else sys.executable):
            cmd = composition.command('codex', self.root, 'literal & prompt')
        self.assertEqual(cmd[:2], [sys.executable, str(entry)])
        self.assertEqual(cmd[-1], 'literal & prompt')

    def test_npm_string_bin_is_supported(self):
        shim, entry = self.npm('claude-code', 'cli.js')
        with patch('shutil.which', side_effect=lambda name: str(shim) if name == 'claude' else sys.executable):
            self.assertEqual(composition.command('claude-code', self.root, 'test')[:2], [sys.executable, str(entry)])

    def test_missing_node_has_actionable_error(self):
        shim, _ = self.npm('claude-code', {'claude': 'cli.js'})
        with patch('shutil.which', side_effect=lambda name: str(shim) if name == 'claude' else None):
            with self.assertRaisesRegex(FileNotFoundError, '[Nn]ode'):
                composition.command('claude-code', self.root, 'test')

    def fake_inventory(self, host, source, **options):
        script = self.write('fake_inventory.py', source)
        popen = subprocess.Popen
        def launch(_command, **kwargs):
            return popen([sys.executable, str(script)], **kwargs)
        with patch('shutil.which', return_value=sys.executable), patch.object(host_inventory.subprocess, 'Popen', side_effect=launch):
            return host_inventory.inventory(host, self.root, **options)

    def test_inventory_project_paths_use_boundaries_and_both_separators(self):
        root = self.root.resolve()
        result = {'result': {'data': [{'skills': [
            {'name': 'local', 'path': (root / 'skills/local/SKILL.md').as_posix(), 'scope': 'project'},
            {'name': 'sibling', 'path': str(root.with_name(root.name + '-other') / 'SKILL.md'), 'scope': 'user'},
        ]}]}}
        output = io.StringIO()
        with patch.object(host_inventory, 'inventory', return_value=result), patch.object(sys, 'argv',
                ['inventory', '--host', 'codex', '--project', str(root), '--output', str(root / 'inventory.json')]), contextlib.redirect_stdout(output):
            host_inventory.main()
        summary = json.loads(output.getvalue())
        self.assertEqual(summary['names'], ['local'])
        self.assertEqual(summary['skills_by_scope'], {'project': 1, 'user': 1})

    def test_inventory_loader_errors_exit_nonzero(self):
        result = {'result': {'data': [{'skills': [], 'errors': [{'message': 'fixture loader failure'}]}]}}
        output = io.StringIO()
        with patch.object(host_inventory, 'inventory', return_value=result), patch.object(sys, 'argv',
                ['inventory', '--host', 'codex', '--project', str(self.root), '--output', str(self.root / 'inventory.json')]), contextlib.redirect_stdout(output):
            with self.assertRaises(SystemExit) as stopped:
                host_inventory.main()
        self.assertNotEqual(stopped.exception.code, 0)
        self.assertIn('fixture loader failure', output.getvalue())
        self.assertEqual(json.loads((self.root / 'inventory.json').read_text()), result)

    @unittest.skipUnless(os.name == 'nt', 'Windows job cleanup failure')
    def test_job_close_failure_still_reaps_process_and_closes_streams(self):
        process = None
        close = host_process._WindowsJob.close
        def fail(job):
            close(job)
            raise RuntimeError('fixture close failure')
        with patch.object(host_process._WindowsJob, 'close', fail):
            with self.assertRaisesRegex(RuntimeError, 'fixture close failure'):
                with host_process.managed_process([sys.executable, '-c', 'import time; time.sleep(60)'],
                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                    pass
        try:
            self.assertIsNotNone(process.returncode, 'child was not reaped')
            self.assertTrue(all(stream.closed for stream in (process.stdin, process.stdout, process.stderr)))
        finally:
            process.wait(timeout=5)
            for stream in (process.stdin, process.stdout, process.stderr):
                stream.close()

    def test_codex_inventory_rpc_error_is_failure(self):
        with self.assertRaisesRegex(RuntimeError, 'fixture denied'):
            self.fake_inventory('codex', '''import json, sys
for line in sys.stdin:
    request = json.loads(line)
    if 'id' in request:
        response = {'id': request['id'], 'result': {}} if request['id'] == 1 else {'id': 2, 'error': {'message': 'fixture denied'}}
        print(json.dumps(response), flush=True)
''')

    def test_claude_inventory_control_error_is_failure(self):
        with self.assertRaisesRegex(RuntimeError, 'fixture denied'):
            self.fake_inventory('claude-code', '''import json, sys
sys.stdin.readline()
print(json.dumps({'type': 'control_response', 'response': {'request_id': 'inventory', 'subtype': 'error', 'error': 'fixture denied'}}), flush=True)
''')

    def test_inventory_ignores_json_noise(self):
        result = self.fake_inventory('codex', '''import json, sys
print('null', flush=True)
print('[]', flush=True)
for line in sys.stdin:
    request = json.loads(line)
    if 'id' in request:
        print(json.dumps({'id': request['id'], 'result': {'data': []}}), flush=True)
''')
        self.assertEqual(result['result']['data'], [])

    def test_inventory_closes_streams(self):
        with warnings.catch_warnings(record=True) as seen:
            warnings.simplefilter('always', ResourceWarning)
            self.fake_inventory('codex', '''import json, sys
for line in sys.stdin:
    request = json.loads(line)
    if 'id' in request:
        print(json.dumps({'id': request['id'], 'result': {'data': []}}), flush=True)
''')
            gc.collect()
        self.assertEqual([str(w.message) for w in seen if issubclass(w.category, ResourceWarning)], [])

    def test_inventory_timeout_is_bounded(self):
        start = time.monotonic()
        with self.assertRaisesRegex(RuntimeError, 'timed out'):
            self.fake_inventory('codex', 'import time\ntime.sleep(60)\n', timeout=0.2)
        self.assertLess(time.monotonic() - start, 3)

    def test_inventory_early_exit_retains_stderr(self):
        with self.assertRaisesRegex(RuntimeError, 'fixture failure'):
            self.fake_inventory('codex', 'import sys\nsys.stdin.readline()\nprint("fixture failure", file=sys.stderr, flush=True)\n')

    @unittest.skipUnless(os.name == 'nt', 'Windows cwd lock regression')
    def test_inventory_return_releases_descendant_cwd(self):
        locked = self.root / 'locked-cwd'
        locked.mkdir()
        child = self.write('cwd_child.py', 'import time\nfrom pathlib import Path\nPath("ready").touch()\ntime.sleep(60)\n')
        source = f'''import json, sys, subprocess, time
from pathlib import Path
subprocess.Popen([sys.executable, {str(child)!r}], cwd={str(locked)!r})
deadline = time.monotonic() + 5
while not Path({str(locked / 'ready')!r}).exists():
    if time.monotonic() > deadline:
        raise RuntimeError('child did not start')
    time.sleep(0.01)
for line in sys.stdin:
    request = json.loads(line)
    if 'id' in request:
        print(json.dumps({{'id': request['id'], 'result': {{'data': []}}}}), flush=True)
'''
        self.fake_inventory('codex', source)
        locked.rename(self.root / 'released-cwd')

    def composition_fixture(self):
        self.write('.agents/pstack/BUNDLE.json', '{}')
        self.write('settings.py', composition.CODE)
        self.write('test_settings.py', composition.TESTS)
        self.write('docs/timeout.md', composition.DESIGN)
        self.write('docs/work.md', composition.PLAN)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True, capture_output=True)
        output = self.root / 'results'
        output.mkdir()
        return output

    def test_composition_launch_failure_writes_result(self):
        output = self.composition_fixture()
        with patch.object(composition, 'prepare', return_value=(self.root, 'test')), patch.object(composition, 'command', return_value=[str(self.root / 'missing.exe')]), contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(composition.run('codex', output, 'design', 1))
        record = json.loads((output / 'design-result.json').read_text())
        self.assertTrue(record['error'])
        self.assertIsNone(record['exit_code'])

    def test_composition_missing_artifact_writes_failure(self):
        output = self.composition_fixture()
        (self.root / 'settings.py').unlink()
        with patch.object(composition, 'prepare', return_value=(self.root, 'test')), patch.object(composition, 'command', return_value=[sys.executable, '-c', 'pass']), contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(composition.run('codex', output, 'design', 1))
        record = json.loads((output / 'design-result.json').read_text())
        self.assertFalse(all(record['artifact_checks'].values()))

    def test_postchecks_are_bounded(self):
        self.composition_fixture()
        self.write('settings.py', 'import time\ntime.sleep(60)\n')
        code = (f'import sys; sys.path.insert(0, {str(ROOT / "scripts")!r}); '
                'import check_composition_behavior as c; from pathlib import Path; '
                f'c.CHECK_TIMEOUT = 0.2; checks, evidence = c.check(Path({str(self.root)!r}), "implement"); '
                'assert not checks["observable_contract"]; assert "timed out" in evidence.lower()')
        with subprocess.Popen([sys.executable, '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True, start_new_session=os.name != 'nt') as process:
            try:
                stdout, stderr = process.communicate(timeout=4)
            except subprocess.TimeoutExpired:
                stop_fixture(process)
                process.communicate(timeout=5)
                self.fail('postchecks exceeded their deadline')
        self.assertEqual(process.returncode, 0, stdout + stderr)

    def test_host_timeout_stops_descendants(self):
        output = self.composition_fixture()
        marker = self.root / 'child-survived.txt'
        child = self.write('child.py', f'import time\nfrom pathlib import Path\ntime.sleep(1.2)\nPath({str(marker)!r}).write_text("alive")\n')
        parent = self.write('parent.py', f'import subprocess, sys, time\nsubprocess.Popen([sys.executable, {str(child)!r}])\ntime.sleep(60)\n')
        with patch.object(composition, 'prepare', return_value=(self.root, 'test')), patch.object(composition, 'command', return_value=[sys.executable, str(parent)]), contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(composition.run('codex', output, 'design', 0.5))
        time.sleep(1.3)
        self.assertFalse(marker.exists(), 'child still executed after host timeout')

    def test_normal_host_exit_stops_descendants(self):
        output = self.composition_fixture()
        marker = self.root / 'child-survived.txt'
        child = self.write('child.py', f'import time\nfrom pathlib import Path\ntime.sleep(0.8)\nPath({str(marker)!r}).write_text("alive")\n')
        parent = self.write('parent.py', f'import subprocess, sys\nsubprocess.Popen([sys.executable, {str(child)!r}])\n')
        with patch.object(composition, 'prepare', return_value=(self.root, 'test')), patch.object(composition, 'command', return_value=[sys.executable, str(parent)]), contextlib.redirect_stdout(io.StringIO()):
            self.assertTrue(composition.run('codex', output, 'design', 2))
        time.sleep(1)
        self.assertFalse(marker.exists(), 'child still executed after host exit')

    def git_fixture(self):
        output = self.composition_fixture()
        git_behavior.git(self.root, 'config', 'user.name', 'Fixture')
        git_behavior.git(self.root, 'config', 'user.email', 'fixture@example.invalid')
        git_behavior.git(self.root, 'add', 'settings.py')
        tree = git_behavior.git(self.root, 'write-tree').strip().decode()
        seed = git_behavior.git(self.root, '-c', 'commit.gpgsign=false', 'commit-tree', tree, data=b'fixture\n').strip().decode()
        git_behavior.git(self.root, 'update-ref', 'HEAD', seed)
        before = {'head': git_behavior.git(self.root, 'rev-parse', 'HEAD'),
                  'index': git_behavior.git(self.root, 'ls-files', '--stage'),
                  'protected': {}, 'worktrees': git_behavior.git(self.root, 'worktree', 'list', '--porcelain')}
        return output, before

    def test_git_launch_failure_writes_result(self):
        output, before = self.git_fixture()
        with patch.object(git_behavior, 'prepare', return_value=(self.root, 'test', before, '.agents')), patch.object(git_behavior, 'command', return_value=[str(self.root / 'missing.exe')]), contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(git_behavior.run('codex', 'cleanup', output, 1))
        record = json.loads((output / 'cleanup-result.json').read_text())
        self.assertTrue(record['error'])
        self.assertIsNone(record['exit_code'])

    def test_git_timeout_writes_result(self):
        output, before = self.git_fixture()
        with patch.object(git_behavior, 'prepare', return_value=(self.root, 'test', before, '.agents')), patch.object(git_behavior, 'command', return_value=[sys.executable, '-c', 'import time; time.sleep(60)']), contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(git_behavior.run('codex', 'cleanup', output, 0.2))
        record = json.loads((output / 'cleanup-result.json').read_text())
        self.assertTrue(record['timed_out'])

    def test_git_probe_uses_current_interpreter_and_is_bounded(self):
        output, before = self.git_fixture()
        self.write('settings.py', 'import time\ntime.sleep(60)\n')
        calls = []
        original = git_behavior.probe
        def capture(command, **kwargs):
            calls.append(command)
            return original(command, **kwargs)
        with patch.object(git_behavior, 'probe', side_effect=capture), patch.object(git_behavior, 'CHECK_TIMEOUT', 0.2):
            checks = git_behavior.check(self.root, 'resume', output, before)
        self.assertEqual(calls[0][0], sys.executable)
        self.assertFalse(checks['current_behavior_verified'])
        self.assertIn('timed out', (output / 'resume-probe.txt').read_text())


if __name__ == '__main__':
    unittest.main()
