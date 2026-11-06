import json
import os
import re
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from package import build, digest
from install import install, retire_project


class Distribution(unittest.TestCase):
    def test_bundle_retains_resources_licenses_and_all_names(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = build(Path(directory) / 'bundle')
            marker = json.loads((bundle / 'BUNDLE.json').read_text(encoding='utf-8'))
            self.assertEqual(len(marker['skills']), 63)
            for name in marker['skills']:
                self.assertTrue((bundle / 'skills' / name / 'LICENSE').is_file())
            self.assertTrue((bundle / 'docs/harness/codex.md').is_file())
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
            self.assertEqual(len(list((project / '.agents/skills').iterdir())), 63)
            linked = project / '.agents/skills/poteto-mode/SKILL.md'
            self.assertTrue(linked.is_file())
            self.assertNotIn('disable-model-invocation:', linked.read_text(encoding='utf-8'))
            policy = linked.parent / 'agents/openai.yaml'
            self.assertIn('allow_implicit_invocation: false', policy.read_text(encoding='utf-8'))
            help_path = project / '.agents/skills/poteto-help/SKILL.md'
            href = re.search(r'\[guide page 1\]\(([^)]+)\)', help_path.read_text(encoding='utf-8'))[1]
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
            self.assertEqual(plan['skills'], 63)
            self.assertFalse(project.exists())

    def test_user_scope_preserves_existing_config_and_unrelated_skills(self):
        with tempfile.TemporaryDirectory() as directory:
            home = Path(directory) / 'account'
            (home / '.codex').mkdir(parents=True)
            (home / '.agents/skills/personal').mkdir(parents=True)
            config = home / '.codex/config.toml'
            config.write_bytes(b'model = "keep-me"\r\n')
            personal = home / '.agents/skills/personal/SKILL.md'
            personal.write_text('personal method', encoding='utf-8')
            result = install('codex', scope='user', home=home)
            self.assertEqual(result['scope'], 'user')
            self.assertEqual(config.read_bytes(), b'model = "keep-me"\r\n')
            self.assertEqual(personal.read_text(), 'personal method')
            self.assertTrue((home / '.agents/skills/tdd/SKILL.md').is_file())
            self.assertFalse((home / '.codex/skills/tdd').exists())

    def test_retirement_keeps_user_skills_and_archives_only_managed_project_files(self):
        with tempfile.TemporaryDirectory() as directory:
            home, project = Path(directory) / 'account', Path(directory) / 'project'
            install('claude-code', project)
            original = (project / '.claude/skills/tdd/SKILL.md').read_bytes()
            (project / '.claude/skills/project-specific').mkdir()
            custom = project / '.claude/skills/project-specific/SKILL.md'
            custom.write_text('project-owned', encoding='utf-8')
            install('claude-code', scope='user', home=home)
            result = retire_project('claude-code', project, home)
            self.assertFalse((project / '.claude/pstack').exists())
            self.assertFalse((project / '.claude/skills/tdd').exists())
            self.assertEqual(custom.read_text(), 'project-owned')
            self.assertEqual((Path(result['archive']) / 'skills/tdd/SKILL.md').read_bytes(), original)
            self.assertTrue((home / '.claude/skills/tdd/SKILL.md').is_file())
            self.assertTrue((home / '.claude/agents/poteto-agent.md').is_file())

    def test_retirement_refuses_modified_project_and_missing_user_install(self):
        with tempfile.TemporaryDirectory() as directory:
            home, project = Path(directory) / 'account', Path(directory) / 'project'
            install('codex', project)
            with self.assertRaises(FileExistsError):
                retire_project('codex', project, home)
            install('codex', scope='user', home=home)
            modified = project / '.agents/skills/tdd/SKILL.md'
            modified.write_text('unrelated edit', encoding='utf-8')
            with self.assertRaises(FileExistsError):
                retire_project('codex', project, home)
            self.assertEqual(modified.read_text(), 'unrelated edit')
            self.assertTrue((project / '.agents/pstack').is_dir())

    def test_user_scope_rejects_a_project_argument(self):
        with self.assertRaises(ValueError):
            install('codex', '.', scope='user')


if __name__ == '__main__':
    unittest.main()
