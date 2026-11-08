import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import package
from test_backup import SCRATCH, directory_link


class Packaging(unittest.TestCase):
    def setUp(self):
        SCRATCH.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=SCRATCH)
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.root = self.base / 'source'
        self.output = self.base / 'bundle'
        self.pstack = self.root / 'pstack'
        self.write('pstack/docs/composition.md', '[Grilling](../../grilling/SKILL.md)\n')
        self.write('pstack/LICENSE', 'upstream license')
        self.write('pstack/ORIGIN.md', 'adaptation origin')
        self.write('pstack/plugin.json', json.dumps({'name': 'pstack', 'version': '0.15.36'}))
        self.write('pstack/agents/poteto-agent.md', 'agent one')
        self.write('pstack/agents/comment-sicko.md', 'agent two')
        self.write('pstack/automations/benny/templates/configuration.example.yaml', 'resource: keep')
        for name in [f'skill-{n}' for n in range(58)]:
            self.skill('pstack/skills/' + name, name)
        for name in package.SUPPLEMENTS:
            self.skill(name, name)
        self.skill('pstack/automations/benny/skills/setup-benny', 'setup-benny')
        self.write('adapters/common.md', 'runtime contract')
        imported = {p.relative_to(self.pstack).as_posix(): package.digest(p)
                    for p in self.pstack.rglob('*') if p.is_file()}
        self.write('source-lock.json', json.dumps({'upstream': {'commit': 'fixture', 'files': imported}}))
        root_patch = patch.object(package, 'ROOT', self.root)
        root_patch.start()
        self.addCleanup(root_patch.stop)

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value, encoding='utf-8')

    def skill(self, directory, name):
        self.write(directory + '/SKILL.md', f'---\nname: {name}\ndescription: Test package\n---\n')
        self.write(directory + '/LICENSE', 'skill license')
        self.write(directory + '/ORIGIN.md', 'source evidence')
        self.write(directory + '/agents/openai.yaml', 'interface: {}\n')

    def test_complete_bundle_manifest_and_source_preservation(self):
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob('*') if p.is_file()}
        self.assertEqual(package.build(self.output, include_supplements=True), self.output)
        marker = json.loads((self.output / 'BUNDLE.json').read_text())
        actual = {p.relative_to(self.output).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in self.output.rglob('*') if p.is_file() and p != self.output / 'BUNDLE.json'}
        self.assertEqual(marker['files'], actual)
        self.assertEqual(len(marker['skills']), 63)
        self.assertEqual(before, {p.relative_to(self.root): p.read_bytes()
                                  for p in self.root.rglob('*') if p.is_file()})
        self.assertIn('../../grilling/SKILL.md', (self.output / 'docs/composition.md').read_text())
        self.assertEqual(marker['upstream'], 'fixture')

    def test_missing_required_resources_are_rejected_without_output(self):
        for relative in ('LICENSE', 'ORIGIN.md', 'skills/skill-0/LICENSE', 'skills/skill-0/agents/openai.yaml',
                         'skills/skill-0/ORIGIN.md', 'agents/poteto-agent.md',
                         'automations/benny/skills/setup-benny/LICENSE',
                         'automations/benny/skills/setup-benny/ORIGIN.md',
                         'automations/benny/skills/setup-benny/agents/openai.yaml',
                         'automations/benny/templates/configuration.example.yaml'):
            with self.subTest(resource=relative):
                path = self.pstack / relative
                data = path.read_bytes()
                path.unlink()
                try:
                    with self.assertRaises(ValueError):
                        package.build(self.output, include_supplements=True)
                    self.assertFalse(self.output.exists())
                finally:
                    path.write_bytes(data)
                    if self.output.exists():
                        shutil.rmtree(self.output)

    def test_missing_supplement_license_is_rejected(self):
        (self.root / 'grilling/LICENSE').unlink()
        with self.assertRaises(ValueError):
            package.build(self.output, include_supplements=True)
        self.assertFalse(self.output.exists())

    def test_skill_identity_must_match_its_directory(self):
        self.write('grilling/SKILL.md', '---\nname: grill-me\ndescription: duplicate\n---\n')
        with self.assertRaises(ValueError):
            package.build(self.output, include_supplements=True)
        self.assertFalse(self.output.exists())

    def test_skill_count_validation_is_not_an_assertion(self):
        (self.root / 'grilling/SKILL.md').unlink()
        with self.assertRaises(ValueError):
            package.build(self.output, include_supplements=True)
        self.assertFalse(self.output.exists())

    def test_dangling_output_link_is_not_followed(self):
        target = self.base / 'missing-target'
        target.mkdir()
        directory_link(self.output, target)
        target.rmdir()
        with self.assertRaises(FileExistsError):
            package.build(self.output, include_supplements=True)
        self.assertTrue(os.path.lexists(self.output))
        self.assertFalse(target.exists())

    def test_existing_output_bytes_are_preserved(self):
        self.output.mkdir()
        (self.output / 'mine').write_bytes(b'keep')
        with self.assertRaises(FileExistsError):
            package.build(self.output, include_supplements=True)
        self.assertEqual(list(self.output.iterdir()), [self.output / 'mine'])
        self.assertEqual((self.output / 'mine').read_bytes(), b'keep')

    def test_nested_link_to_output_parent_is_rejected_before_copy(self):
        external = self.base / 'external'
        external.mkdir()
        directory_link(self.pstack / 'docs/linked', external)
        output = external / 'bundle'
        original = shutil.copytree

        def bounded_copy(source, destination, *args, **kwargs):
            if str(destination).count('linked') > 1:
                raise RuntimeError('recursive copy reached its own output')
            return original(source, destination, *args, **kwargs)

        with patch.object(shutil, 'copytree', bounded_copy):
            with self.assertRaises(ValueError):
                package.build(output)
        self.assertFalse(output.exists())

    def test_linked_source_resource_is_rejected(self):
        external = self.base / 'external'
        external.mkdir()
        (external / 'private').write_bytes(b'not a package resource')
        directory_link(self.pstack / 'docs/linked', external)
        with self.assertRaises(ValueError):
            package.build(self.output, include_supplements=True)
        self.assertFalse(self.output.exists())
        self.assertEqual((external / 'private').read_bytes(), b'not a package resource')

    def test_copy_failure_removes_partial_output_and_allows_retry(self):
        original = shutil.copy2

        def fail_copy(source, destination, *args, **kwargs):
            if Path(source).name == 'composition.md':
                raise OSError('injected copy failure')
            return original(source, destination, *args, **kwargs)

        # copytree binds copy2 at definition time; patch the copytree entry to
        # inject a real file-copy failure while retaining traversal and writes.
        tree = shutil.copytree

        def failing_tree(source, destination, *args, **kwargs):
            if not args:
                kwargs['copy_function'] = fail_copy
            return tree(source, destination, *args, **kwargs)

        with patch.object(shutil, 'copytree', failing_tree):
            with self.assertRaises(OSError):
                package.build(self.output, include_supplements=True)
        self.assertFalse(self.output.exists())
        package.build(self.output, include_supplements=True)

    def test_manifest_write_failure_removes_partial_output(self):
        original = Path.write_text

        def fail_write(path, *args, **kwargs):
            if path.name == 'BUNDLE.json':
                raise OSError('injected manifest failure')
            return original(path, *args, **kwargs)

        with patch.object(Path, 'write_text', fail_write):
            with self.assertRaisesRegex(OSError, 'injected manifest failure'):
                package.build(self.output, include_supplements=True)
        self.assertFalse(self.output.exists())

    def test_existing_source_bundle_marker_does_not_hash_itself(self):
        self.write('pstack/BUNDLE.json', '{"stale": true}\n')
        with self.assertRaises(ValueError):
            package.build(self.output, include_supplements=True)
        self.assertFalse(self.output.exists())

    def test_copy_damage_is_not_certified_as_complete(self):
        tree = shutil.copytree

        def damaged_tree(source, destination, *args, **kwargs):
            result = tree(source, destination, *args, **kwargs)
            if Path(destination) == self.output:
                (self.output / 'agents/poteto-agent.md').write_bytes(b'damaged copy')
            return result

        with patch.object(shutil, 'copytree', damaged_tree):
            with self.assertRaises(ValueError):
                package.build(self.output, include_supplements=True)
        self.assertFalse(self.output.exists())
        self.assertEqual((self.pstack / 'agents/poteto-agent.md').read_text(), 'agent one')

    def test_readonly_source_can_be_packaged_without_changing_source_mode(self):
        source = self.pstack / 'docs/composition.md'
        source.chmod(stat.S_IREAD)
        self.addCleanup(source.chmod, stat.S_IREAD | stat.S_IWRITE)
        mode = source.stat().st_mode
        package.build(self.output, include_supplements=True)
        self.assertEqual(source.stat().st_mode, mode)
        self.assertIn('../../grilling/SKILL.md', (self.output / 'docs/composition.md').read_text())

    def test_readonly_copy_is_cleaned_up_after_write_failure(self):
        source = self.pstack / 'LICENSE'
        source.chmod(stat.S_IREAD)
        self.addCleanup(source.chmod, stat.S_IREAD | stat.S_IWRITE)
        original = Path.write_text

        def fail_write(path, *args, **kwargs):
            if path.name == 'BUNDLE.json':
                raise OSError('injected manifest failure')
            return original(path, *args, **kwargs)

        with patch.object(Path, 'write_text', fail_write):
            with self.assertRaisesRegex(OSError, 'injected manifest failure'):
                package.build(self.output, include_supplements=True)
        self.assertFalse(self.output.exists())

    def test_output_claimed_during_preflight_is_preserved(self):
        mkdir = Path.mkdir

        def racing_mkdir(path, *args, **kwargs):
            if path == self.output and not path.exists():
                mkdir(path)
                (path / 'competitor').write_bytes(b'keep')
            return mkdir(path, *args, **kwargs)

        with patch.object(Path, 'mkdir', racing_mkdir):
            with self.assertRaises(FileExistsError):
                package.build(self.output, include_supplements=True)
        self.assertEqual((self.output / 'competitor').read_bytes(), b'keep')


if __name__ == '__main__':
    unittest.main()
