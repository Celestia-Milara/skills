import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import install as installer


class InstallationTransactions(unittest.TestCase):
    def test_projection_failure_preserves_active_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installer.install('codex', root)
            host = root / '.agents'
            before = installer.files(host)
            copy = installer.shutil.copytree

            def fail_projection(source, target, *args, **kwargs):
                destination = Path(target)
                if (destination.name == 'tdd' and destination.parent.name == 'skills'
                        and destination.is_relative_to(host)
                        and destination.parent.parent.name != 'pstack'):
                    raise OSError('injected projection failure')
                return copy(source, target, *args, **kwargs)

            with patch.object(installer.shutil, 'copytree', side_effect=fail_projection):
                with self.assertRaisesRegex(OSError, 'projection failure'):
                    installer.install('codex', root, replace=True)
            self.assertEqual(installer.files(host), before)

    def test_publish_failure_restores_old_version(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installer.install('codex', root)
            host = root / '.agents'
            before = installer.files(host)
            rename = Path.rename

            def fail_move(source, target):
                if Path(target) == host / 'skills/tdd' and source.parent.parent.name.startswith('.pstack-stage-'):
                    raise OSError('injected publish failure')
                return rename(source, target)

            with patch.object(Path, 'rename', new=fail_move):
                with self.assertRaisesRegex(OSError, 'publish failure'):
                    installer.install('codex', root, replace=True)
            self.assertEqual(installer.files(host), before)

    def test_installation_lock_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installer.install('codex', root)
            host = root / '.agents'
            before = installer.files(host)
            with installer.installation_lock(host):
                with self.assertRaisesRegex(FileExistsError, 'locked'):
                    installer.install('codex', root, replace=True)
            self.assertEqual(installer.files(host), before)

    def test_first_install_failure_leaves_no_active_partial_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            host = root / '.agents'
            rename = Path.rename

            def fail_move(source, target):
                if Path(target) == host / 'skills/tdd':
                    raise OSError('injected first install failure')
                return rename(source, target)

            with patch.object(Path, 'rename', new=fail_move):
                with self.assertRaisesRegex(OSError, 'first install failure'):
                    installer.install('codex', root)
            self.assertEqual(installer.files(host), {})
            installer.install('codex', root)
            self.assertTrue((host / 'skills/tdd/SKILL.md').is_file())

    def test_retirement_receipt_failure_preserves_project(self):
        with tempfile.TemporaryDirectory() as directory:
            root, home = Path(directory) / 'project', Path(directory) / 'home'
            installer.install('codex', root)
            installer.install('codex', scope='user', home=home)
            before = installer.files(root)
            write = Path.write_text

            def fail_receipt(path, *args, **kwargs):
                if path.name == 'RETIREMENT.json':
                    raise OSError('injected receipt failure')
                return write(path, *args, **kwargs)

            with patch.object(Path, 'write_text', new=fail_receipt):
                with self.assertRaisesRegex(OSError, 'receipt failure'):
                    installer.retire_project('codex', root, home)
            self.assertEqual(installer.files(root), before)

    def test_edits_during_preparation_are_preserved(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installer.install('codex', root)
            entry = root / '.agents/skills/tdd/SKILL.md'
            prepare = installer.project_packages

            def edit_after_prepare(*args):
                prepare(*args)
                entry.write_text('concurrent user edit', encoding='utf-8')

            with patch.object(installer, 'project_packages', side_effect=edit_after_prepare):
                with self.assertRaises(FileExistsError):
                    installer.install('codex', root, replace=True)
            self.assertEqual(entry.read_text(), 'concurrent user edit')
            self.assertFalse((root / '.agents/pstack-backups').exists())

    def test_backup_name_collision_preserves_earlier_backup(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installer.install('codex', root)
            host = root / '.agents'
            backup = host / 'pstack-backups/collision'
            backup.mkdir(parents=True)
            (backup / 'sentinel.txt').write_text('prior recovery data', encoding='utf-8')
            before = installer.files(host)
            with patch.object(installer, 'datetime') as clock:
                clock.now.return_value.strftime.return_value = 'collision'
                with self.assertRaises(FileExistsError):
                    installer.install('codex', root, replace=True)
            self.assertEqual(installer.files(host), before)

    def test_install_cannot_write_inside_source_package(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            with patch.object(installer, 'ROOT', source):
                for package in ('pstack', 'grilling'):
                    with self.subTest(package=package), self.assertRaisesRegex(ValueError, 'source packages'):
                        installer.install('codex', source / package)
            self.assertEqual(list(source.iterdir()), [])

    def test_damaged_staging_copy_does_not_replace_live_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installer.install('codex', root)
            host = root / '.agents'
            before = installer.files(host)
            copy = installer.shutil.copytree

            for part in ('bundle', 'skill'):
                def damage(source, target, *args, **kwargs):
                    result = copy(source, target, *args, **kwargs)
                    target = Path(target)
                    if target.is_relative_to(host):
                        if part == 'bundle' and target.name == 'pstack':
                            (target / 'README.md').write_text('copy damage', encoding='utf-8')
                        elif part == 'skill' and target.name == 'tdd' and target.parent.parent.name.startswith('.pstack-stage-'):
                            (target / 'LICENSE').unlink()
                    return result

                with self.subTest(part=part), patch.object(installer.shutil, 'copytree', side_effect=damage):
                    with self.assertRaisesRegex(ValueError, 'Staged'):
                        installer.install('codex', root, replace=True)
                self.assertEqual(installer.files(host), before)

    def test_damaged_claude_agent_copy_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installer.install('claude-code', root)
            host = root / '.claude'
            before = installer.files(host)
            copy = installer.shutil.copy2

            def damage(source, target, *args, **kwargs):
                result = copy(source, target, *args, **kwargs)
                target = Path(target)
                if (target.name == 'poteto-agent.md' and target.parent.name == 'agents'
                        and target.parent.parent.name.startswith('.pstack-stage-')):
                    target.write_text('copy damage', encoding='utf-8')
                return result

            with patch.object(installer.shutil, 'copy2', side_effect=damage):
                with self.assertRaisesRegex(ValueError, 'Staged agent'):
                    installer.install('claude-code', root, replace=True)
            self.assertEqual(installer.files(host), before)

    def test_failed_backup_move_restores_active_installation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installer.install('claude-code', root)
            host = root / '.claude'
            before = installer.files(host)
            rename = Path.rename

            def fail_move(source, target):
                if source == host / 'skills/tdd':
                    raise OSError('injected archive failure')
                return rename(source, target)

            with patch.object(Path, 'rename', new=fail_move):
                with self.assertRaisesRegex(OSError, 'archive failure'):
                    installer.install('claude-code', root, replace=True)
            self.assertEqual(installer.files(host), before)

    def test_removed_managed_skill_is_archived(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installer.install('codex', root)
            host = root / '.agents'
            removed = host / 'skills/retired-entry'
            removed.mkdir()
            (removed / 'SKILL.md').write_text('previous managed skill', encoding='utf-8')
            marker = host / 'pstack/.library-install.json'
            state = json.loads(marker.read_text(encoding='utf-8'))
            state['skills']['retired-entry'] = installer.files(removed)
            marker.write_text(json.dumps(state), encoding='utf-8')
            installer.install('codex', root, replace=True)
            self.assertFalse(removed.exists())
            backups = list((host / 'pstack-backups').iterdir())
            self.assertEqual((backups[0] / 'skills/retired-entry/SKILL.md').read_text(),
                             'previous managed skill')

    def test_manifest_cannot_register_paths_outside_skill_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            installer.install('codex', root)
            host = root / '.agents'
            other = host / 'other'
            other.mkdir()
            (other / 'personal.txt').write_text('preserve', encoding='utf-8')
            marker = host / 'pstack/.library-install.json'
            state = json.loads(marker.read_text(encoding='utf-8'))
            state['skills']['../other'] = installer.files(other)
            marker.write_text(json.dumps(state), encoding='utf-8')
            before = installer.files(host)
            with self.assertRaises(ValueError):
                installer.install('codex', root, replace=True)
            self.assertEqual(installer.files(host), before)


if __name__ == '__main__':
    unittest.main()
