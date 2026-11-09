import ctypes
from ctypes import wintypes as W
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch
from test_backup import directory_link
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
LAUNCHER = ROOT / 'adapters/platforms/statechart.py'
GUARDIAN = ROOT / 'adapters/platforms/windows_job.py'
spec = importlib.util.spec_from_file_location('windows_statechart', LAUNCHER)
statechart = importlib.util.module_from_spec(spec)
if LAUNCHER.is_file():
    spec.loader.exec_module(statechart)


@unittest.skipUnless(os.name == 'nt', 'Windows Job Objects require Windows')
class WindowsStatechart(unittest.TestCase):
    def call(self, *args, **kwargs):
        return subprocess.run([sys.executable, '-B', str(LAUNCHER), *map(str, args)],
                              capture_output=True, text=True, encoding='utf-8', timeout=30, **kwargs)

    def test_missing_config_and_occupied_output_write_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            spec = base / 'Model.tla'
            spec.write_text('---- MODULE Model ----\n====\n')
            result = self.call('--skills-root', ROOT / 'pstack/skills', spec)
            self.assertEqual(result.returncode, 2)
            self.assertIn('config', result.stderr.lower())
            (base / 'Model.cfg').write_text('INIT Init\nNEXT Next\n')
            out = base / 'out'
            out.mkdir()
            (out / 'user.txt').write_text('keep')
            result = self.call('--skills-root', ROOT / 'pstack/skills', spec, '--out', out)
            self.assertEqual(result.returncode, 2)
            self.assertEqual((out / 'user.txt').read_text(), 'keep')
            self.assertEqual(sorted(p.name for p in base.iterdir()), ['Model.cfg', 'Model.tla', 'out'])

    def test_job_timeout_kills_worker_and_grandchild(self):
        self.run_job('timeout')

    def test_job_stdin_eof_kills_worker_and_grandchild(self):
        self.run_job('parent-eof')

    def test_job_cancel_kills_worker_and_grandchild(self):
        self.run_job('cancelled')

    def test_readonly_temp_is_gone_before_a_publishable_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            evidence, stage, temp = [base / name for name in ['evidence', 'stage', 'temp']]
            for path in [evidence, stage, temp]:
                path.mkdir()
            code = ('from pathlib import Path; import sys,stat; '
                    'file=Path(sys.argv[1])/"readonly"; file.write_text("temp"); file.chmod(stat.S_IREAD); '
                    '(Path(sys.argv[2])/"done").mkdir()')
            request = dict(schema=1, runId='readonly', evidenceDir=str(evidence), cwd=str(base),
                           argv=[sys.executable, '-B', '-c', code, str(temp), str(stage)],
                           cleanupDirs=[str(stage), str(temp)], prepareCleanupDirs=[str(temp)], stageDir=str(stage))
            proc = subprocess.Popen([sys.executable, '-I', '-B', str(GUARDIAN)], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                proc.stdin.write((json.dumps(request) + '\n').encode())
                proc.stdin.flush()
                receipt = json.loads(proc.stdout.readline())
                self.assertEqual(receipt['exitCode'], 0)
                self.assertTrue(receipt['prepared'])
                self.assertFalse(temp.exists())
                self.assertTrue((stage / 'done').is_dir())
                _, errors = proc.communicate(input=b'{"op":"finish"}\n', timeout=12)
                self.assertEqual(proc.returncode, 0, errors)
                self.assertFalse(stage.exists())
            finally:
                if proc.poll() is None:
                    proc.stdin.close()
                    proc.stdin = None
                    proc.communicate(timeout=12)

    def test_error_paths_are_utf8_even_with_a_legacy_console_encoding(self):
        with tempfile.TemporaryDirectory() as directory:
            spec = Path(directory) / '\u6a21\u578b.tla'
            result = self.call('--skills-root', ROOT / 'pstack/skills', spec,
                               env={**os.environ, 'PYTHONIOENCODING': 'ascii'})
            self.assertEqual(result.returncode, 2)
            self.assertIn('\u6a21\u578b.cfg', result.stderr)
            self.assertNotIn('codec', result.stderr)

    def test_publication_preserves_files_created_during_the_check(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            done, dest = base / 'done', base / 'out'
            done.mkdir()
            (done / 'report.md').write_text('new report')
            self.assertEqual(statechart.output_path(dest), dest)
            dest.mkdir()
            (dest / 'user.txt').write_text('keep')
            with self.assertRaises(OSError):
                statechart.publish(done, dest)
            self.assertEqual((dest / 'user.txt').read_text(), 'keep')
            self.assertTrue((done / 'report.md').is_file())
            (dest / 'user.txt').unlink()
            statechart.publish(done, dest, statechart.directory_identity(dest))
            self.assertEqual((dest / 'report.md').read_text(), 'new report')

    def test_publication_restores_an_existing_empty_folder_after_rename_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            done, dest = base / 'done', base / 'out'
            done.mkdir()
            dest.mkdir()
            with patch.object(statechart.os, 'rename', side_effect=PermissionError('shared file')):
                with self.assertRaises(PermissionError):
                    statechart.publish(done, dest, statechart.directory_identity(dest))
            self.assertTrue(dest.is_dir())
            self.assertTrue(done.is_dir())

    def test_abbreviated_options_are_rejected(self):
        result = self.call('--skills-root', ROOT / 'pstack/skills', 'Model.tla', '--ou', 'out')
        self.assertEqual(result.returncode, 2)
        self.assertIn('unrecognized arguments', result.stderr)

    def test_new_output_junction_is_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            done, dest, target = base / 'done', base / 'out', base / 'target'
            done.mkdir()
            target.mkdir()
            (target / 'user.txt').write_text('keep')
            self.assertIsNone(statechart.directory_identity(dest))
            directory_link(dest, target)
            try:
                with self.assertRaises(FileExistsError):
                    statechart.publish(done, dest)
                self.assertTrue(dest.is_dir())
                self.assertTrue(done.is_dir())
                self.assertEqual((target / 'user.txt').read_text(), 'keep')
            finally:
                dest.rmdir()

    def test_dependency_search_ignores_cwd_cmd_scripts(self):
        node = shutil.which('node')
        if not node:
            self.skipTest('Requires an installed Node for the execution probe')
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            (base / 'node.cmd').write_text('@echo off\r\necho hijacked>HIJACKED\r\necho v24.20.0\r\n')
            env = {key: value for key, value in os.environ.items() if key.upper() != 'NODEFAULTCURRENTDIRECTORYINEXEPATH'}
            env['PATH'] = str(Path(node).parent)
            script = ('import sys,subprocess; sys.path.insert(0,sys.argv[1]); '
                      'from runtime import find_executable; '
                      'binary=find_executable("node"); assert binary and binary.lower().endswith(".exe"); '
                      'raise SystemExit(subprocess.call([binary,"--version"]))')
            result = subprocess.run([sys.executable, '-B', '-c', script, str(LAUNCHER.parent)],
                                    cwd=base, env=env, capture_output=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((base / 'HIJACKED').exists())

    def test_overlapping_evidence_is_rejected_before_creating_output(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            model = base / 'Model.tla'
            model.write_text('---- MODULE Model ----\n====\n')
            model.with_suffix('.cfg').write_text('INIT Init\nNEXT Next\n')
            result = self.call('--skills-root', ROOT / 'pstack/skills', model,
                               '--out', base / 'out', '--evidence', base / 'out/evidence')
            self.assertEqual(result.returncode, 2)
            self.assertIn('outside the output', result.stderr)
            self.assertFalse((base / 'out').exists())

    def test_private_dependency_tampering_and_missing_tlc_stop_before_staging(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            model = base / 'Model.tla'
            model.write_text('---- MODULE Model ----\n====\n')
            model.with_suffix('.cfg').write_text('INIT Init\nNEXT Next\n')
            skills = base / 'skills'
            sources = json.loads((ROOT / 'adapters/platforms/manifest.json').read_text())['tools']['statechart']['sources']
            for relative in sources:
                dest = skills / relative.removeprefix('skills/')
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / 'pstack' / relative, dest)
            result = self.call('--skills-root', skills, model, '--tlc', base / 'absent.jar')
            self.assertEqual(result.returncode, 2)
            self.assertIn('requires Node', result.stderr)
            changed = skills / 'statechart/scripts/frontends/messages.ts'
            changed.write_text('modified parser')
            result = self.call('--skills-root', skills, model)
            self.assertEqual(result.returncode, 2)
            self.assertIn('Private statechart source differs', result.stderr)
            self.assertFalse(list(base.glob('.*.statechart-*')))

    def run_job(self, action):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            evidence, stage, temp = [base / name for name in ['evidence', 'stage', 'temp']]
            for path in [evidence, stage, temp]:
                path.mkdir()
            fixture = base / 'tree.py'
            fixture.write_text("import subprocess, sys, os, time\nfrom pathlib import Path\n"
                               "base=Path(sys.argv[1]); depth=int(sys.argv[2])\n"
                               "(base / f'{depth}.pid').write_text(str(os.getpid()))\n"
                               "if depth < 2: subprocess.Popen([sys.executable, '-B', __file__, str(base), str(depth+1)])\n"
                               "time.sleep(60)\n", encoding='utf-8')
            request = dict(schema=1, runId='fixture', evidenceDir=str(evidence), cwd=str(base),
                           argv=[sys.executable, '-B', str(fixture), str(base), '0'],
                           cleanupDirs=[str(stage), str(temp)], timeoutMs=1800 if action == 'timeout' else 0)
            proc = subprocess.Popen([sys.executable, '-B', str(GUARDIAN)], stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            try:
                proc.stdin.write((json.dumps(request) + '\n').encode())
                proc.stdin.flush()
                deadline = time.monotonic() + 8
                while not (base / '2.pid').exists() and proc.poll() is None and time.monotonic() < deadline:
                    time.sleep(.02)
                self.assertTrue((base / '2.pid').exists(), 'Job must actually start all three processes')
                kernel = ctypes.WinDLL('kernel32', use_last_error=True)
                kernel.OpenProcess.argtypes = [W.DWORD, W.BOOL, W.DWORD]
                kernel.OpenProcess.restype = W.HANDLE
                kernel.WaitForSingleObject.argtypes = [W.HANDLE, W.DWORD]
                kernel.CloseHandle.argtypes = [W.HANDLE]
                handles = [kernel.OpenProcess(0x100000, False, int(p.read_text())) for p in sorted(base.glob('*.pid'))]
                self.assertTrue(all(handles))
                try:
                    if action == 'parent-eof':
                        proc.stdin.close()
                        proc.stdin = None
                    else:
                        if action == 'cancelled':
                            proc.stdin.write(b'{"op":"cancel"}\n')
                            proc.stdin.flush()
                        receipt = json.loads(proc.stdout.readline())
                        self.assertEqual(receipt['status'], action)
                        proc.stdin.write(b'{"op":"finish"}\n')
                        proc.stdin.flush()
                    stdout, stderr = proc.communicate(timeout=12)
                    self.assertEqual(proc.returncode, 0, stderr.decode())
                    receipt = json.loads((evidence / 'receipt.json').read_text())
                    self.assertEqual(receipt['status'], action)
                    self.assertTrue(receipt['cleanup']['confirmed'])
                    self.assertTrue(receipt['finalized'])
                    self.assertTrue(all(kernel.WaitForSingleObject(h, 0) == 0 for h in handles))
                    self.assertFalse(stage.exists())
                    self.assertFalse(temp.exists())
                finally:
                    for handle in handles:
                        if handle:
                            kernel.CloseHandle(handle)
            finally:
                if proc.poll() is None:
                    if proc.stdin:
                        proc.stdin.close()
                        proc.stdin = None
                    proc.communicate(timeout=12)


if __name__ == '__main__':
    unittest.main()
