from pathlib import Path
import json
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from install import install
from package import ROOT, SUPPLEMENTS, digest
from verify import links


class HostProjection(unittest.TestCase):
    def test_pristine_bundle_and_host_specific_entries(self):
        expected = json.loads((ROOT / 'source-lock.json').read_text())['upstream']['files']
        for host, folder in [('codex', '.agents'), ('claude-code', '.claude'), ('pi', '.pi/agent'), ('dsh', '.dsh')]:
            with self.subTest(host=host), tempfile.TemporaryDirectory() as directory:
                project = Path(directory)
                install(host, project)
                base = project / folder
                bundle = base / 'pstack'
                self.assertTrue(all(digest(bundle / rel) == sha for rel, sha in expected.items()))
                mode = base / 'skills/poteto-mode/SKILL.md'
                text = mode.read_text(encoding='utf-8')
                self.assertIn(f'the {host} adapter', text)
                self.assertIn('[the execution platform contract](../../pstack/adapters/platforms/README.md)', text)
                self.assertEqual(links(bundle / 'adapters/platforms/README.md', project), [])
                self.assertEqual('disable-model-invocation: true' in text, host != 'codex')
                for adapter in (bundle / 'adapters').glob('*.md'):
                    self.assertEqual(links(adapter, project), [], adapter)
                if host == 'codex':
                    policy = mode.parent / 'agents/openai.yaml'
                    self.assertIn('allow_implicit_invocation: false', policy.read_text())
                if host == 'claude-code':
                    agent = (base / 'agents/poteto-agent.md').read_text()
                    self.assertNotIn('is_background:', agent)
                    self.assertNotIn('.pstack-stage-', agent)
                    self.assertIn(str((base / 'pstack/skills/poteto-mode/SKILL.md')).replace('\\', '/'), agent)

    def test_explicit_supplements_survive_managed_update(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            install('codex', project, with_supplements=True)
            install('codex', project, replace=True)
            base = project / '.agents'
            marker = json.loads((base / 'pstack/.library-install.json').read_text())
            self.assertEqual(len(marker['pstack_skills']), 58)
            self.assertEqual(set(marker['preserved_supplements']), set(SUPPLEMENTS))
            for name in SUPPLEMENTS:
                self.assertTrue((base / 'skills' / name / 'SKILL.md').is_file())
                original = (ROOT / name / 'agents/openai.yaml').read_text(encoding='utf-8')
                projected = (base / 'skills' / name / 'agents/openai.yaml').read_text(encoding='utf-8')
                self.assertTrue(projected.startswith(original.split('policy:', 1)[0]))
            self.assertNotIn('Workflow composition', (base / 'skills/poteto-mode/SKILL.md').read_text())

    def test_user_codex_avoids_the_shared_skill_root(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory)
            install('codex', scope='user', home=home)
            self.assertTrue((home / '.codex/skills/poteto-mode/SKILL.md').is_file())
            self.assertFalse((home / '.agents/skills/poteto-mode/SKILL.md').exists())

    def test_model_setup_write_contract_is_mapped_for_each_non_cursor_host(self):
        for host in ['codex', 'pi', 'dsh']:
            value = (ROOT / 'adapters' / f'{host}.md').read_text(encoding='utf-8')
            self.assertIn('setup-pstack', value)
            self.assertIn('~/.agents/pstack-models.md', value)
            self.assertIn('write', value.lower())


if __name__ == '__main__':
    unittest.main()
