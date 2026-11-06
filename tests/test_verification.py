import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class Verification(unittest.TestCase):
    def test_dependency_docs_are_excluded_but_maintained_links_are_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            fixture = Path(directory) / 'library'
            shutil.copytree(ROOT, fixture, ignore=shutil.ignore_patterns(
                '.git', '.tmp', '.dist', '.cache', 'node_modules', '__pycache__',
                'design', 'zh-backup', '.agents', '.claude'))
            dependency = fixture / 'pstack/skills/poteto-mode/scripts/node_modules/example'
            dependency.mkdir(parents=True)
            (dependency / 'README.md').write_text('[Example](missing.md)', encoding='utf-8')
            command = [sys.executable, str(fixture / 'scripts/verify.py')]
            installed = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
            self.assertEqual(json.loads(installed.stdout)['errors'], [])

            (fixture / 'docs/broken.md').write_text('[Missing](missing.md)', encoding='utf-8')
            broken = subprocess.run(command, capture_output=True, text=True, check=False)
            self.assertEqual(broken.returncode, 1, broken.stdout + broken.stderr)
            self.assertTrue(any('broken.md' in error and 'missing.md' in error
                                for error in json.loads(broken.stdout)['errors']))


if __name__ == '__main__':
    unittest.main()
