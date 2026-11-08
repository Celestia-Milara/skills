import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from backup_installation import snapshot

SCRATCH = Path(__file__).resolve().parents[1] / '.tmp/audit-backup'


def directory_link(link, target):
    if os.name == 'nt':
        subprocess.run(
            ['powershell', '-NoProfile', '-Command',
             'New-Item -ItemType Junction -Path $env:AUDIT_LINK '
             '-Target $env:AUDIT_TARGET -ErrorAction Stop | Out-Null'],
            env={**os.environ, 'AUDIT_LINK': str(link), 'AUDIT_TARGET': str(target)},
            check=True, capture_output=True, text=True)
    else:
        link.symlink_to(target, target_is_directory=True)


class InstallationBackup(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        self.temporary = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)
        self.home, self.project = self.base / 'home', self.base / 'project'
        self.skills = self.home / '.agents/skills'
        self.skills.mkdir(parents=True)
        self.output = self.base / 'backup'

    def test_backup_can_restore_config_and_skill_bytes_without_auth_or_history(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            base = Path(directory)
            home, project, output = base / 'user', base / 'project', base / 'backup'
            (home / '.codex/skills/custom').mkdir(parents=True)
            (project / '.claude/skills/custom').mkdir(parents=True)
            (home / '.codex/config.toml').write_text('model = "existing"\n', encoding='utf-8')
            (home / '.codex/auth.json').write_text('do not include', encoding='utf-8')
            (home / '.codex/skills/custom/SKILL.md').write_bytes(b'original skill\r\n')
            (project / '.claude/skills/custom/SKILL.md').write_bytes(b'project skill\n')
            result = snapshot(home, project, output)
            self.assertEqual(result['files_verified'], 3)
            manifest = json.loads((output / 'manifest.json').read_text(encoding='utf-8'))
            with zipfile.ZipFile(output / 'configuration-and-skills.zip') as archive:
                self.assertNotIn('user/.codex/auth.json', archive.namelist())
                self.assertEqual(archive.read('user/.codex/skills/custom/SKILL.md'), b'original skill\r\n')
                for name, expected in manifest['files'].items():
                    self.assertEqual(hashlib.sha256(archive.read(name)).hexdigest(), expected)

    def test_backup_refuses_recursive_output_and_overwrite(self):
        with tempfile.TemporaryDirectory(dir=SCRATCH) as directory:
            base = Path(directory)
            home, project = base / 'user', base / 'project'
            skills = home / '.agents/skills'
            skills.mkdir(parents=True)
            with self.assertRaises(ValueError):
                snapshot(home, project, skills / 'backup')
            existing = base / 'already'
            existing.mkdir()
            with self.assertRaises(FileExistsError):
                snapshot(home, project, existing)

    def test_output_inside_nested_link_target_is_rejected_before_writes(self):
        external = self.base / 'external'
        external.mkdir()
        directory_link(self.skills / 'linked', external)
        output = external / 'backup'
        with self.assertRaises(ValueError):
            snapshot(self.home, self.project, output)
        self.assertFalse(output.exists())
        self.assertEqual(list(external.iterdir()), [])

    def test_dangling_output_link_is_preserved(self):
        target = self.base / 'target'
        target.mkdir()
        directory_link(self.output, target)
        target.rmdir()
        with self.assertRaises(FileExistsError):
            snapshot(self.home, self.project, self.output)
        self.assertTrue(os.path.lexists(self.output))
        self.assertFalse(target.exists())

    def test_empty_directories_and_link_targets_survive_archive_restore(self):
        external = self.base / 'external'
        (external / 'empty/nested').mkdir(parents=True)
        (external / 'bytes.bin').write_bytes(b'\x00\xff\r\n')
        directory_link(self.skills / 'linked', external)
        snapshot(self.home, self.project, self.output)
        manifest = json.loads((self.output / 'manifest.json').read_text())
        self.assertEqual(manifest['links']['user/.agents/skills/linked'], str(external))
        with zipfile.ZipFile(self.output / 'configuration-and-skills.zip') as archive:
            archive.extractall(self.base / 'restored')
        restored = self.base / 'restored/user/.agents/skills/linked'
        self.assertTrue((restored / 'empty/nested').is_dir())
        self.assertEqual((restored / 'bytes.bin').read_bytes(), b'\x00\xff\r\n')
        self.assertEqual((external / 'bytes.bin').read_bytes(), b'\x00\xff\r\n')

    def test_cycle_is_rejected_without_partial_backup(self):
        directory_link(self.skills / 'cycle', self.skills)
        with self.assertRaises(ValueError):
            snapshot(self.home, self.project, self.output)
        self.assertFalse(self.output.exists())

    def test_read_failure_removes_partial_backup_and_allows_retry(self):
        source = self.skills / 'sample'
        source.write_bytes(b'preserve me')
        original = Path.read_bytes

        def fail_read(path):
            if path == source:
                raise OSError('injected read failure')
            return original(path)

        with patch.object(Path, 'read_bytes', fail_read):
            with self.assertRaisesRegex(OSError, 'injected read failure'):
                snapshot(self.home, self.project, self.output)
        self.assertFalse(self.output.exists())
        self.assertEqual(source.read_bytes(), b'preserve me')
        self.assertEqual(snapshot(self.home, self.project, self.output)['files_verified'], 1)

    def test_manifest_failure_removes_partial_backup(self):
        original = Path.write_text

        def fail_write(path, *args, **kwargs):
            if path.name == 'manifest.json':
                raise OSError('injected manifest failure')
            return original(path, *args, **kwargs)

        with patch.object(Path, 'write_text', fail_write):
            with self.assertRaisesRegex(OSError, 'injected manifest failure'):
                snapshot(self.home, self.project, self.output)
        self.assertFalse(self.output.exists())


if __name__ == '__main__':
    unittest.main()
