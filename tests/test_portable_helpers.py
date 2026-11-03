import csv
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sessions = load('sessions', 'pstack/skills/poteto-mode/scripts/workspace_sessions.py')
logger = load('logger', 'pstack/skills/show-me-your-work/scripts/log.py')
audit = load('audit', 'pstack/skills/poteto-mode/scripts/worktree_audit.py')


class PortableHelpers(unittest.TestCase):
    def test_log_appends_rows_and_escapes_spreadsheet_formulas(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'decision log.tsv'
            logger.append(path, 'start', '=1+1', 'why\nnew', '@file', 'ok\tpass')
            logger.append(path, 'check', 'done', 'reason', 'file', 'green')
            with path.open(encoding='utf-8', newline='') as stream:
                rows = list(csv.reader(stream, delimiter='\t'))
            self.assertEqual(len(rows), 3)
            self.assertEqual(rows[0], ['ts', 'phase', 'decision', 'why', 'evidence', 'result'])
            self.assertEqual(rows[1][2:], ["'=1+1", 'why new', "'@file", 'ok pass'])
            self.assertTrue(all(len(row) == 6 for row in rows))

    def test_codex_sessions_filter_workspace_and_sort_by_modification(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / '.codex/sessions/2026/11/03'
            folder.mkdir(parents=True)
            for name, cwd, modified in [('rollout-z.jsonl', 'D:/Repo', 100), ('rollout-a.jsonl', 'd:\\repo', 200), ('rollout-other.jsonl', 'D:/Other', 300)]:
                path = folder / name
                path.write_text(json.dumps({'type': 'session_meta', 'payload': {'cwd': cwd}}) + '\nUNRELATED BODY IS NOT JSON\n', encoding='utf-8')
                os.utime(path, (modified, modified))
            found = sessions.select_sessions('codex', 'D:/Repo', directory)
            self.assertEqual([Path(item['path']).name for item in found], ['rollout-a.jsonl', 'rollout-z.jsonl'])

    def test_claude_sessions_check_cwd_inside_selected_project(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / '.claude/projects/D--03_work-repo'
            folder.mkdir(parents=True)
            for name, cwd in [('right', 'D:/03_work/repo'), ('wrong', 'D:/other')]:
                (folder / f'{name}.jsonl').write_text(json.dumps({'type': 'file-history-snapshot'}) + '\n' + json.dumps({'cwd': cwd, 'type': 'user'}) + '\n', encoding='utf-8')
            found = sessions.select_sessions('claude-code', 'D:/03_work/repo', directory)
            self.assertEqual([Path(item['path']).stem for item in found], ['right'])
            other_encoding = folder.parent / 'D--03-work-repo'
            other_encoding.mkdir()
            (other_encoding / 'also-right.jsonl').write_text(json.dumps({'cwd': 'D:/03_work/repo'}), encoding='utf-8')
            found = sessions.select_sessions('claude-code', 'D:/03_work/repo', directory)
            self.assertEqual({Path(item['path']).stem for item in found}, {'right', 'also-right'})

    def test_worktree_audit_distinguishes_dirty_and_unknown_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory) / 'repo with spaces'
            repo.mkdir()
            def git(*args):
                return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, check=True)
            git('init', '-b', 'main')
            (repo / 'item.txt').write_text('base', encoding='utf-8')
            git('add', 'item.txt')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'fixture')
            clean = audit.audit(repo, 'main')[0]
            self.assertTrue(clean['clean'])
            self.assertTrue(clean['merged'])
            (repo / 'item.txt').write_text('changed', encoding='utf-8')
            before = git('status', '--porcelain').stdout
            dirty = audit.audit(repo, 'not-a-ref')[0]
            self.assertFalse(dirty['clean'])
            self.assertIsNone(dirty['merged'])
            self.assertEqual(dirty['safe_to_delete'], 'NOT_ESTABLISHED')
            self.assertEqual(git('status', '--porcelain').stdout, before)


if __name__ == '__main__':
    unittest.main()
