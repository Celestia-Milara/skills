import json
import os
from pathlib import Path
import re
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import install as installer
import junction_install as shared
from backup_installation import snapshot
from package import ROOT


@unittest.skipUnless(os.name == 'nt', 'Native Windows Junction checks')
class JunctionInstall(unittest.TestCase):
    def setUp(self):
        scratch = ROOT / '.tmp/junction-tests'
        scratch.mkdir(parents=True, exist_ok=True)
        self.base = Path(tempfile.mkdtemp(dir=scratch)).resolve()
        self.home, self.store = self.base / 'home', self.base / 'store'
        self.addCleanup(shared.remove_local_tree, self.base)

    def create(self, host='codex', **options):
        return installer.install(host, scope='user', home=self.home, storage='junction', store=self.store, **options)

    def receipt(self, host='codex'):
        owner, root, _ = installer.layout(host, scope='user', home=self.home)
        return root, shared.read_receipt(host, owner, root, 'user')

    def test_four_hosts_reuse_one_version_and_keep_separate_metadata(self):
        versions = []
        for host in ['codex', 'claude-code', 'pi', 'dsh']:
            result = self.create(host)
            versions.append(result['version'])
            root, record = self.receipt(host)
            self.assertTrue(shared.junction(root / 'pstack'))
            self.assertFalse((root / 'pstack/.library-install.json').exists())
            text = (root / 'skills/poteto-mode/SKILL.md').read_text(encoding='utf-8')
            self.assertIn(f'the {host} adapter', text)
            self.assertEqual('disable-model-invocation: true' in text, host != 'codex')
            self.assertFalse(shared.junction(root / 'skills/poteto-mode/scripts'))
            self.assertFalse(shared.junction(root / 'skills/statechart/scripts'))
            self.assertTrue(any(x['links'] for x in record['skills'].values()))
            if host == 'codex':
                self.assertIn('allow_implicit_invocation: false', (root / 'skills/poteto-mode/agents/openai.yaml').read_text())
            if host == 'claude-code':
                agent = (root / 'agents/poteto-agent.md').read_text()
                self.assertNotIn('.pstack-stage-', agent)
                self.assertIn((root / 'skills/poteto-mode/SKILL.md').as_posix(), agent)
        self.assertEqual(len(set(versions)), 1)
        self.assertEqual(len(list((self.store / 'versions').iterdir())), 1)

    def test_logical_and_real_resource_links_keep_their_targets(self):
        result = self.create()
        root, _ = self.receipt()
        version = Path(result['version'])
        checked = 0
        def documents(path):
            for child in path.iterdir():
                if child.is_dir():
                    yield from documents(child)
                elif child.suffix == '.md':
                    yield child
        for folder in (root / 'skills').iterdir():
            for logical in documents(folder):
                original = version / 'skills' / logical.relative_to(root / 'skills')
                before = re.findall(r'\]\(([^\s)]+)\)', original.read_text(encoding='utf-8'))
                text = re.sub(r'^Read \[the codex adapter\].*\n', '', logical.read_text(encoding='utf-8'), flags=re.M)
                after = re.findall(r'\]\(([^\s)]+)\)', text)
                self.assertEqual(len(before), len(after), logical)
                for old, new in zip(before, after):
                    if ':' in old or old.startswith(('#', '//')):
                        continue
                    old = old.split('#')[0]
                    new = new.split('#')[0]
                    if (original.parent / old).exists():
                        self.assertTrue((logical.parent / new).exists(), (logical, new))
                        self.assertTrue((logical.resolve().parent / new).exists(), (logical.resolve(), new))
                        checked += 1
        self.assertGreater(checked, 0)
        witness = root / 'skills/architect/references/rationale-template.md'
        self.assertTrue((witness.parent / '../../arena/SKILL.md').is_file())
        self.assertTrue((witness.resolve().parent / '../../arena/SKILL.md').is_file())
        self.assertEqual((witness.resolve().parent / '../../arena/SKILL.md').resolve(),
                         (root / 'skills/arena/SKILL.md').resolve())
        self.assertIn('the codex adapter', (witness.resolve().parent / '../../arena/SKILL.md').read_text(encoding='utf-8'))

    def test_repeat_install_is_stable_and_uninstall_keeps_shared_targets(self):
        first = self.create()
        version = Path(first['version'])
        before = installer.files(version)
        self.create(replace=True)
        result = shared.uninstall('codex', scope='user', home=self.home)
        self.assertFalse((self.home / '.codex/pstack').exists())
        archive = Path(result['archive'])
        shared.remove_local_tree(archive)
        self.assertEqual(installer.files(version), before)

    def test_dry_run_and_unmanaged_collision_have_no_writes(self):
        self.create(dry_run=True)
        self.assertFalse(self.home.exists())
        self.assertFalse(self.store.exists())
        target = self.home / '.codex/skills/tdd'
        target.mkdir(parents=True)
        (target / 'mine').write_text('keep')
        with self.assertRaises(FileExistsError):
            self.create()
        self.assertEqual((target / 'mine').read_text(), 'keep')
        self.assertFalse(self.store.exists())

    def test_modified_entry_and_retargeted_junction_are_preserved(self):
        self.create()
        root, _ = self.receipt()
        skill = root / 'skills/tdd/SKILL.md'
        before = skill.read_bytes()
        skill.write_bytes(b'my edit')
        with self.assertRaises(FileExistsError):
            self.create(replace=True)
        self.assertEqual(skill.read_bytes(), b'my edit')
        skill.write_bytes(before)
        link = root / 'pstack'
        link.rmdir()
        other = self.base / 'other'
        other.mkdir()
        shared.make_junction(link, other)
        with self.assertRaises(ValueError):
            self.create(replace=True)
        self.assertTrue(other.is_dir())

    def test_shared_mutation_is_not_overwritten(self):
        result = self.create()
        target = Path(result['version']) / 'README.md'
        target.write_text('local public edit')
        with self.assertRaises(ValueError):
            self.create(replace=True)
        self.assertEqual(target.read_text(), 'local public edit')

    def test_copy_migration_preserves_supplements_and_archives_old_bundle(self):
        installer.install('codex', scope='user', home=self.home, with_supplements=True)
        result = self.create(replace=True)
        _, record = self.receipt()
        self.assertEqual(len(record['skills']), 63)
        old = Path(result['backup']) / 'bundle/.library-install.json'
        self.assertTrue(old.is_file())

    def test_publish_failure_restores_the_previous_install(self):
        result = self.create()
        root, record = self.receipt()
        before = installer.files(Path(result['version']))
        rename = Path.rename
        def fail(source, target):
            if Path(target) == root / shared.RECEIPT and source.parent.name.startswith('.pstack-stage-'):
                raise OSError('injected receipt publish failure')
            return rename(source, target)
        with patch.object(Path, 'rename', new=fail):
            with self.assertRaisesRegex(OSError, 'injected receipt'):
                self.create(replace=True)
        self.assertEqual(self.receipt()[1], record)
        self.assertEqual(installer.files(Path(result['version'])), before)
        self.assertEqual(list(root.glob('.pstack-stage-*')), [])

    def test_first_link_failure_leaves_no_active_install(self):
        with patch.object(shared, 'make_junction', side_effect=OSError('injected link failure')):
            with self.assertRaisesRegex(OSError, 'injected link'):
                self.create()
        root = self.home / '.codex'
        self.assertFalse(os.path.lexists(root / 'pstack'))
        self.assertFalse((root / shared.RECEIPT).exists())
        self.assertEqual(list(root.glob('.pstack-stage-*')), [])
        self.create()

    def test_new_resource_version_can_restore_the_previous_version(self):
        first = self.create()
        build = shared.build
        def revised(output, **options):
            result = build(output, **options)
            adapter = result / 'adapters/common.md'
            adapter.write_text(adapter.read_text() + '\nTest resource revision.\n', encoding='utf-8')
            marker = result / 'BUNDLE.json'
            value = json.loads(marker.read_text())
            value['files']['adapters/common.md'] = installer.digest(adapter)
            marker.write_text(json.dumps(value, indent=2) + '\n', encoding='utf-8')
            return result
        with patch.object(shared, 'build', side_effect=revised):
            second = self.create(replace=True)
        self.assertNotEqual(first['version'], second['version'])
        restored = shared.restore('codex', second['backup'], scope='user', home=self.home)
        self.assertEqual(restored['restored_version'], first['version'])
        self.assertEqual(self.receipt()[1]['version'], first['version'])
        self.assertTrue(Path(second['version']).is_dir())
        self.assertEqual(len(list((self.store / 'versions').iterdir())), 2)

    def test_store_lock_conflict_does_not_publish_an_install(self):
        with installer.installation_lock(self.store):
            with self.assertRaises(FileExistsError):
                self.create()
        self.assertFalse((self.home / '.codex/pstack').exists())

    def test_backup_includes_the_external_receipt_and_shared_contents(self):
        self.create()
        output = self.base / 'snapshot'
        snapshot(self.home, self.base / 'project', output)
        marker = json.loads((output / 'manifest.json').read_text())
        self.assertIn('user/.codex/.pstack-install.json', marker['files'])
        self.assertIn('user/.codex/pstack/skills/how/SKILL.md', marker['files'])
        self.assertIn('user/.codex/pstack', marker['links'])

    def test_store_cannot_be_inside_a_source_package(self):
        with self.assertRaises(ValueError):
            installer.install('codex', scope='user', home=self.home, storage='junction',
                              store=ROOT / 'pstack/invalid-runtime-store', dry_run=True)

    def test_local_tool_writes_do_not_modify_public_resources(self):
        result = self.create()
        root, _ = self.receipt()
        before = installer.files(Path(result['version']))
        cache = root / 'skills/poteto-mode/scripts/node_modules'
        cache.mkdir()
        (cache / '.poteto-mode-tools-install-key').write_text('local cache')
        self.assertEqual(installer.files(Path(result['version'])), before)
        updated = self.create(replace=True)
        self.assertEqual((Path(updated['backup']) / 'skills/poteto-mode/scripts/node_modules/.poteto-mode-tools-install-key').read_text(), 'local cache')

    def test_uninstall_archive_can_be_restored_without_an_active_install(self):
        result = self.create()
        removed = shared.uninstall('codex', scope='user', home=self.home)
        shared.restore('codex', removed['archive'], scope='user', home=self.home)
        self.assertEqual(self.receipt()[1]['version'], result['version'])

    def test_cross_volume_store_and_special_characters(self):
        system_drive = Path(os.environ['USERPROFILE']).drive
        if Path(self.base).drive.casefold() == system_drive.casefold():
            self.skipTest('Fixture needs a second local volume')
        with tempfile.TemporaryDirectory(prefix='pstack-junction-') as directory:
            home = Path(directory) / 'home & [literal]'
            installer.install('codex', scope='user', home=home, storage='junction', store=self.store)
            link = home / '.codex/pstack'
            target = link.resolve()
            self.assertNotEqual(link.drive.casefold(), target.drive.casefold())
            self.assertTrue((link / 'skills/how/SKILL.md').is_file())
            shared.uninstall('codex', scope='user', home=home)
            shared.remove_local_tree(home)
            self.assertTrue(target.is_dir())


if __name__ == '__main__':
    unittest.main()
