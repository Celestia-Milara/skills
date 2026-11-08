import json
import os
import re
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from package import build, digest
from install import install


class Distribution(unittest.TestCase):
    def test_bundle_retains_resources_licenses_and_all_names(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = build(Path(directory) / 'bundle')
            marker = json.loads((bundle / 'BUNDLE.json').read_text(encoding='utf-8'))
            self.assertEqual(len(marker['skills']), 58)
            self.assertTrue((bundle / 'LICENSE').is_file())
            self.assertTrue((bundle / 'adapters/codex.md').is_file())
            self.assertTrue((bundle / 'automations/benny/templates/configuration.example.yaml').is_file())
            self.assertTrue(all(digest(bundle / rel) == expected for rel, expected in marker['files'].items()))

    def test_collision_is_detected_before_any_install_write(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            existing = project / '.agents/skills/tdd'
            existing.mkdir(parents=True)
            (existing / 'mine.txt').write_text('keep', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                install('codex', project)
            self.assertFalse((project / '.agents/pstack').exists())
            self.assertEqual((existing / 'mine.txt').read_text(), 'keep')

    def test_installed_references_and_managed_update_preserve_previous_bundle(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            install('codex', project)
            self.assertEqual(len(list((project / '.agents/skills').iterdir())), 58)
            linked = project / '.agents/skills/poteto-mode/SKILL.md'
            self.assertTrue(linked.is_file())
            self.assertNotIn('disable-model-invocation:', linked.read_text(encoding='utf-8'))
            policy = linked.parent / 'agents/openai.yaml'
            self.assertIn('allow_implicit_invocation: false', policy.read_text(encoding='utf-8'))
            help_path = project / '.agents/skills/poteto-help/SKILL.md'
            href = re.search(r'\]\(([^)]+adapters/codex.md)\)', help_path.read_text(encoding='utf-8'))[1]
            doc_link = (help_path.parent / href).resolve()
            self.assertTrue(doc_link.is_file())
            install('codex', project, replace=True)
            backups = list((project / '.agents/pstack-backups').iterdir())
            self.assertEqual(len(backups), 1)
            self.assertTrue(linked.is_file())
            self.assertTrue((backups[0] / 'bundle/BUNDLE.json').is_file())

    def test_modified_install_is_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            install('claude-code', project)
            path = project / '.claude/skills/tdd/SKILL.md'
            path.write_text('my modified method', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                install('claude-code', project, replace=True)
            self.assertEqual(path.read_text(), 'my modified method')
            self.assertTrue((project / '.claude/agents/poteto-agent.md').is_file())

    def test_dry_run_creates_nothing(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / 'new project'
            plan = install('codex', project, dry_run=True)
            self.assertEqual(plan['skills'], 58)
            self.assertFalse(project.exists())


if __name__ == '__main__':
    unittest.main()
