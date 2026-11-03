from pathlib import Path
import re
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from install import install
from package import build, ROOT, SUPPLEMENTS
from verify import links


class CompositionReferences(unittest.TestCase):
    def composition_from(self, host_router):
        targets = re.findall(r'\]\(([^)]+)\)', host_router.read_text(encoding='utf-8'))
        target, = [value for value in targets if value.endswith('/composition.md')]
        return (host_router.parent / target).resolve()

    def check_companions(self, composition, skills, boundary):
        self.assertTrue(composition.is_file())
        self.assertEqual(links(composition, boundary), [])
        targets = re.findall(r'\]\(([^)]+)\)', composition.read_text(encoding='utf-8'))
        for name in SUPPLEMENTS:
            with self.subTest(skill=name):
                target, = [value for value in targets if value.endswith(f'/{name}/SKILL.md')]
                actual = (composition.parent / target).resolve()
                self.assertEqual(actual, (skills / name / 'SKILL.md').resolve())
                self.assertTrue(actual.with_name('LICENSE').is_file())

    def test_source_router_reaches_complete_supplements(self):
        router = ROOT / 'pstack/skills/poteto-mode/references/host.md'
        self.check_companions(self.composition_from(router), ROOT, ROOT)

    def test_plugin_bundle_routes_without_the_source_checkout(self):
        with tempfile.TemporaryDirectory() as directory:
            bundle = build(Path(directory) / 'bundle')
            router = bundle / 'skills/poteto-mode/references/host.md'
            self.check_companions(self.composition_from(router), bundle / 'skills', bundle)

    def test_both_host_projections_route_inside_the_installed_bundle(self):
        for host, folder in [('codex', '.agents'), ('claude-code', '.claude')]:
            with self.subTest(host=host), tempfile.TemporaryDirectory() as directory:
                project = Path(directory)
                install(host, project)
                base = project / folder
                router = base / 'skills/poteto-mode/references/host.md'
                composition = self.composition_from(router)
                self.assertEqual(composition, (base / 'pstack/docs/composition.md').resolve())
                self.check_companions(composition, base / 'pstack/skills', project)
                guidance = (ROOT / 'agent-guidance/collaboration.md').read_text(encoding='utf-8')
                guidance = guidance.replace('../pstack/skills/', f'../{folder}/skills/')
                guidance = guidance.replace('../pstack/docs/', f'../{folder}/pstack/docs/')
                for name in SUPPLEMENTS:
                    guidance = guidance.replace(f'../{name}/', f'../{folder}/skills/{name}/')
                target = project / 'agent-guidance/collaboration.md'
                target.parent.mkdir()
                target.write_text(guidance, encoding='utf-8')
                self.assertEqual(links(target, project), [])
                for name in ('architect', 'reflect', 'poteto-mode'):
                    for path in (base / 'skills' / name).rglob('*.md'):
                        self.assertEqual(links(path, project), [])


if __name__ == '__main__':
    unittest.main()
