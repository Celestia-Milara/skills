import csv
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

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

    def test_codex_sessions_skip_invalid_record_and_payload_shapes(self):
        invalid = [None, [], 'text', 42, True, {},
                   {'type': 'session_meta', 'payload': None},
                   {'type': 'session_meta', 'payload': []},
                   {'type': 'session_meta', 'payload': 'text'},
                   {'type': 'session_meta', 'payload': {'cwd': 42}}]
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / '.codex/sessions/2026/11/06'
            folder.mkdir(parents=True)
            metadata = json.dumps({'type': 'session_meta', 'payload': {'cwd': 'D:/Repo'}})
            (folder / 'rollout-valid.jsonl').write_text(metadata + '\n', encoding='utf-8')
            for index, value in enumerate(invalid):
                (folder / f'rollout-invalid-{index}.jsonl').write_text(
                    json.dumps(value) + '\n' + metadata + '\n', encoding='utf-8')
            (folder / 'rollout-broken.jsonl').write_text('{\n' + metadata + '\n', encoding='utf-8')
            found = sessions.select_sessions('codex', 'D:/Repo', directory)
            self.assertEqual([Path(item['path']).name for item in found], ['rollout-valid.jsonl'])

    def test_codex_invalid_metadata_does_not_read_body(self):
        def metadata_only():
            yield '{}\n'
            self.fail('Read a session body before establishing its workspace')

        stream = mock.MagicMock()
        stream.__enter__.return_value = metadata_only()
        with mock.patch.object(Path, 'open', return_value=stream):
            self.assertIsNone(sessions.recorded_workspace(Path('rollout.jsonl'), 'codex'))

    def test_sessions_skip_files_removed_after_metadata_read(self):
        for host, relative in [('codex', '.codex/sessions/2026/11/06'),
                               ('claude-code', '.claude/projects/D--Repo')]:
            with self.subTest(host=host), tempfile.TemporaryDirectory() as directory:
                folder = Path(directory) / relative
                folder.mkdir(parents=True)
                record = ({'type': 'session_meta', 'payload': {'cwd': 'D:/Repo'}}
                          if host == 'codex' else {'type': 'user', 'cwd': 'D:/Repo'})
                gone = folder / 'rollout-gone.jsonl'
                kept = folder / 'rollout-kept.jsonl'
                for path in (gone, kept):
                    path.write_text(json.dumps(record) + '\n', encoding='utf-8')
                read_workspace = sessions.recorded_workspace

                def remove_after_read(path, selected_host):
                    cwd = read_workspace(path, selected_host)
                    if path == gone:
                        path.unlink()
                    return cwd

                with mock.patch.object(sessions, 'recorded_workspace', side_effect=remove_after_read):
                    found = sessions.select_sessions(host, 'D:/Repo', directory)
                self.assertFalse(gone.exists())
                self.assertEqual([Path(item['path']) for item in found], [kept.resolve()])

    def test_claude_sessions_skip_invalid_records_before_workspace(self):
        invalid = [None, [], 42, 'text', True,
                   {'type': 'session_meta', 'payload': None},
                   {'type': 'session_meta', 'payload': []},
                   {'type': 'session_meta', 'payload': 'text'}]
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / '.claude/projects/D--Repo'
            folder.mkdir(parents=True)
            rows = ['{', *map(json.dumps, invalid), json.dumps({'type': 'user', 'cwd': 'D:/Repo'})]
            (folder / 'valid.jsonl').write_text('\n'.join(rows) + '\n', encoding='utf-8')
            found = sessions.select_sessions('claude-code', 'D:/Repo', directory)
            self.assertEqual([Path(item['path']).name for item in found], ['valid.jsonl'])

    def test_claude_equivalent_paths_do_not_read_unrelated_projects(self):
        with tempfile.TemporaryDirectory() as directory:
            projects = Path(directory) / '.claude/projects'
            for slug in ['D--03_Work-Repo', 'd--03-work-repo', 'D--Other']:
                folder = projects / slug
                folder.mkdir(parents=True)
                (folder / 'session.jsonl').write_text(
                    json.dumps({'type': 'user', 'cwd': 'D:/03_Work/Repo'}) + '\n', encoding='utf-8')
            unrelated = projects / 'D--Other/session.jsonl'
            original_open = Path.open

            def scoped_open(path, *args, **kwargs):
                self.assertNotEqual(path, unrelated, 'Opened a session from an unrelated project')
                return original_open(path, *args, **kwargs)

            paths = ['D:/03_Work/Repo', 'D:/03_Work/Repo/', 'D:/03_Work/Repo/.',
                     'D:/03_Work/child/../Repo', r'd:\03_work\repo', 'd:/03_work/repo',
                     'D:\\03_Work\\Repo\\']
            with mock.patch.object(Path, 'open', scoped_open):
                for workspace in paths:
                    with self.subTest(workspace=workspace):
                        found = sessions.select_sessions('claude-code', workspace, directory)
                        self.assertEqual({Path(item['path']).parent.name for item in found},
                                         {'D--03_Work-Repo', 'd--03-work-repo'})
                        self.assertEqual(len(found), 2)

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
            git('config', 'status.showUntrackedFiles', 'no')
            untracked = repo / 'untracked.txt'
            untracked.write_text('user work', encoding='utf-8')
            self.assertEqual(git('status', '--porcelain').stdout, b'')
            self.assertFalse(audit.audit(repo, 'main')[0]['clean'])
            self.assertEqual(git('config', '--get', 'status.showUntrackedFiles').stdout.strip(), b'no')
            self.assertEqual(untracked.read_text(encoding='utf-8'), 'user work')
            untracked.unlink()
            (repo / 'item.txt').write_text('changed', encoding='utf-8')
            before = git('status', '--porcelain').stdout
            dirty = audit.audit(repo, 'not-a-ref')[0]
            self.assertFalse(dirty['clean'])
            self.assertIsNone(dirty['merged'])
            self.assertEqual(dirty['safe_to_delete'], 'NOT_ESTABLISHED')
            self.assertEqual(git('status', '--porcelain').stdout, before)

    def test_worktree_audit_does_not_refresh_index(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)

            def git(*args):
                return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, check=True)

            git('init', '-b', 'main')
            item = repo / 'item.txt'
            item.write_text('base', encoding='utf-8')
            git('add', 'item.txt')
            git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'fixture')
            timestamp = item.stat().st_mtime_ns + 2_000_000_000
            os.utime(item, ns=(timestamp, timestamp))
            index = repo / '.git/index'
            before = index.read_bytes()
            result = audit.audit(repo, 'main')[0]
            self.assertTrue(result['clean'])
            self.assertTrue(result['merged'])
            self.assertEqual(index.read_bytes(), before)
            self.assertEqual(item.read_text(encoding='utf-8'), 'base')


if __name__ == '__main__':
    unittest.main()
