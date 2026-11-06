import csv
import io
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'pstack/skills/poteto-mode/scripts/worktree-audit.sh'
GIT = shutil.which('git')


def bash_binary():
    if os.name != 'nt':
        return shutil.which('bash')
    if GIT:
        candidate = Path(GIT).resolve().parent.parent / 'bin/bash.exe'
        if candidate.is_file():
            return str(candidate)
    return None  # Do not mistake Windows' WSL launcher for Git Bash.


BASH = bash_binary()


def shell_path(path):
    value = Path(path).resolve().as_posix()
    return '/' + value[0].lower() + value[2:] if os.name == 'nt' else value


@unittest.skipUnless(GIT and BASH, 'requires Git and Bash (Git Bash on Windows)')
class WorktreeShellTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='worktree-shell-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / 'main repo'
        self.linked = self.root / 'linked folder [ü]'
        self.bin = self.root / 'offline bin'
        self.bin.mkdir()
        self.calls = self.root / 'external-calls.log'
        self.hooks = self.root / 'empty-hooks'
        self.hooks.mkdir()
        self.env = dict(os.environ)
        for key in ['BASH_ENV', 'ENV', 'GIT_DIR', 'GIT_WORK_TREE', 'GIT_INDEX_FILE',
                    'GIT_COMMON_DIR', 'GIT_OPTIONAL_LOCKS', 'GIT_CONFIG_COUNT']:
            self.env.pop(key, None)
        self.env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        AUDIT_CALLS=str(self.calls), AUDIT_FAIL='',
                        AUDIT_REAL_GIT=Path(GIT).resolve().as_posix())
        self.git('init', '-b', 'main', str(self.repo), cwd=self.root)
        (self.repo / 'item.txt').write_text('base\n', encoding='utf-8')
        (self.repo / '.gitignore').write_text('private/\n', encoding='utf-8')
        self.git('add', '.')
        self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-m', 'fixture')
        self.git('worktree', 'add', '-b', 'fixture-closed', str(self.linked), 'HEAD')
        self.script = self.root / 'worktree-audit.sh'
        shutil.copyfile(SCRIPT, self.script)
        # Block network commands even when this test runs against the old script.
        self.stub('git', '''for arg do
  case "$arg" in
    fetch|push|pull|ls-remote|clone)
      printf 'git %s\\n' "$arg" >> "$AUDIT_CALLS"; exit 97 ;;
  esac
  if [ -n "$AUDIT_FAIL" ] && [ "$arg" = "$AUDIT_FAIL" ]; then exit 9; fi
done
exec "$AUDIT_REAL_GIT" "$@"
''')
        self.stub('origin', 'printf "origin\\n" >> "$AUDIT_CALLS"\nexit 127\n')
        self.stub('gh', '''printf 'gh\\n' >> "$AUDIT_CALLS"
printf '%s\\n' '[{"number":7,"state":"CLOSED","headRefName":"fixture-closed"}]'
''')

    def stub(self, name, body):
        target = self.bin / name
        target.write_text('#!/bin/sh\n' + body, encoding='utf-8', newline='\n')
        target.chmod(0o755)

    def git(self, *args, cwd=None):
        return subprocess.run(
            [GIT, '-c', 'core.hooksPath=' + str(self.hooks), *args],
            cwd=cwd or self.repo, env=self.env, capture_output=True,
            check=True, text=True, encoding='utf-8', timeout=15,
        ).stdout.strip()

    def audit(self, base='main', fail=''):
        env = {**self.env, 'AUDIT_FAIL': fail}
        result = subprocess.run(
            [BASH, '--noprofile', '--norc', '-c',
             'export PATH="$1:$PATH"; exec bash "$2" -b "$3" "$4"',
             'audit-test', shell_path(self.bin), self.script.as_posix(), base,
             self.repo.as_posix()],
            cwd=self.root, env=env, capture_output=True, text=True,
            encoding='utf-8', timeout=20,
        )
        lines = '\n'.join(line for line in result.stdout.splitlines()
                          if line and not line.startswith('#'))
        rows = list(csv.DictReader(io.StringIO(lines), delimiter='\t'))
        return result, rows

    def test_space_and_unicode_paths_are_not_split_and_clean_is_not_safe(self):
        result, rows = self.audit()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(len(rows), 1, result.stdout)
        row = rows[0]
        self.assertEqual(row['WORKTREE'], self.linked.as_posix())
        self.assertEqual(row['MERGED'], 'YES')
        self.assertEqual(row['DIRTY'], 'clean')
        self.assertTrue(row['SIZE'])
        self.assertEqual(row['BUCKET'], 'review')
        self.assertEqual(row['PR'], 'unknown')
        self.assertEqual(row['LAST_CHAT'], 'unknown')

    def test_untracked_and_ignored_content_is_explicit_even_when_config_hides_it(self):
        self.git('config', 'status.showUntrackedFiles', 'no')
        (self.linked / 'user note.txt').write_text('keep', encoding='utf-8')
        (self.linked / 'private').mkdir()
        (self.linked / 'private/one.txt').write_text('keep', encoding='utf-8')
        (self.linked / 'private/two.txt').write_text('keep', encoding='utf-8')
        result, rows = self.audit()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(rows[0]['DIRTY'], 'tracked:0,untracked:1,ignored:2')
        self.assertEqual(rows[0]['BUCKET'], 'hold-local-content')
        self.assertEqual(self.git('config', '--get', 'status.showUntrackedFiles'), 'no')
        self.assertEqual((self.linked / 'user note.txt').read_text(), 'keep')

    def test_renames_and_tracked_edits_do_not_consume_other_status_entries(self):
        self.git('-C', str(self.linked), 'mv', 'item.txt', 'renamed item.txt')
        (self.linked / 'user note.txt').write_text('keep', encoding='utf-8')
        result, rows = self.audit()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(rows[0]['DIRTY'], 'tracked:1,untracked:1,ignored:0')
        self.assertEqual(rows[0]['BUCKET'], 'hold-wip')

    def test_no_fetch_pr_query_ref_update_or_index_refresh(self):
        self.git('remote', 'add', 'origin', str(self.repo))
        self.git('update-ref', 'refs/remotes/origin/main', 'HEAD')
        os.utime(self.linked / 'item.txt', (100, 100))
        index = Path(self.git('-C', str(self.linked), 'rev-parse', '--git-path', 'index'))
        before = (self.git('show-ref'), index.read_bytes(), index.stat().st_mtime_ns)
        result, _ = self.audit('origin/main')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertFalse(self.calls.exists(), self.calls.read_text() if self.calls.exists() else '')
        self.assertEqual((self.git('show-ref'), index.read_bytes(), index.stat().st_mtime_ns), before)
        self.assertFalse((self.repo / '.git/FETCH_HEAD').exists())

    def test_closed_pr_input_cannot_make_unmerged_work_safe(self):
        # The offline gh stub offers a closed PR; a local audit must not ask it.
        (self.linked / 'item.txt').write_text('branch change\n', encoding='utf-8')
        self.git('-C', str(self.linked), 'add', 'item.txt')
        self.git('-C', str(self.linked), '-c', 'user.name=Fixture',
                 '-c', 'user.email=fixture@example.invalid', 'commit', '-m', 'unmerged fixture')
        result, rows = self.audit()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(rows[0]['MERGED'], 'no')
        self.assertEqual(rows[0]['PR'], 'unknown')
        self.assertEqual(rows[0]['BUCKET'], 'review')
        self.assertFalse(self.calls.exists())

    def test_failed_status_is_unknown_and_fails_the_audit(self):
        result, rows = self.audit(fail='status')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(rows[0]['DIRTY'], 'unknown')
        self.assertEqual(rows[0]['BUCKET'], 'review-unknown')
        self.assertIn('status', result.stderr)

    def test_failed_merge_check_is_unknown_not_unmerged(self):
        result, rows = self.audit(fail='merge-base')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(rows[0]['MERGED'], 'unknown')
        self.assertEqual(rows[0]['BUCKET'], 'review-unknown')

    def test_failed_worktree_listing_does_not_report_success(self):
        result, rows = self.audit(fail='worktree')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(rows, [])
        self.assertIn('worktree', result.stderr)

    def test_missing_worktree_is_unknown_not_clean(self):
        moved = self.root / 'moved fixture'
        self.assertTrue(self.linked.resolve().is_relative_to(self.root.resolve()))
        self.assertTrue(moved.resolve().is_relative_to(self.root.resolve()))
        self.linked.rename(moved)
        result, rows = self.audit()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(rows[0]['WORKTREE'], self.linked.as_posix())
        self.assertEqual(rows[0]['DIRTY'], 'unknown')
        self.assertEqual(rows[0]['BUCKET'], 'review-unknown')

    @unittest.skipIf(os.name == 'nt', 'Windows filenames cannot contain tabs or newlines')
    def test_tab_and_newline_paths_are_inspected_and_escaped_in_the_table(self):
        unusual = self.root / 'linked\tline\nbreak'
        self.git('worktree', 'add', '--detach', str(unusual), 'HEAD')
        result, rows = self.audit()
        self.assertEqual(result.returncode, 0, result.stderr)
        escaped = unusual.as_posix().replace('\t', '\\t').replace('\n', '\\n')
        row = next(row for row in rows if row['WORKTREE'] == escaped)
        self.assertEqual(row['MERGED'], 'YES')
        self.assertEqual(row['DIRTY'], 'clean')


if __name__ == '__main__':
    unittest.main()
