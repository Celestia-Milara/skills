"""Read local Git worktree facts. This command never deletes or changes worktrees."""
import argparse
import json
from pathlib import Path
import subprocess


def git(repo, *args):
    return subprocess.run(['git', '-C', str(repo), *args], capture_output=True, text=True, encoding='utf-8')


def audit(repo, base=None):
    result = git(repo, 'worktree', 'list', '--porcelain', '-z')
    if result.returncode:
        raise RuntimeError(result.stderr.strip())
    records, row = [], {}
    for field in result.stdout.split('\0'):
        if not field:
            if row:
                records.append(row)
                row = {}
            continue
        key, _, value = field.partition(' ')
        row[key] = value or True
    if row:
        records.append(row)
    base = base or 'origin/HEAD'
    known_base = git(repo, 'rev-parse', '--verify', base).returncode == 0
    for row in records:
        path = row['worktree']
        status = git(path, 'status', '--porcelain') if Path(path).is_dir() else None
        row['clean'] = not bool(status.stdout) if status is not None and status.returncode == 0 else None
        row['base'] = base
        merge = git(repo, 'merge-base', '--is-ancestor', str(row.get('HEAD', '')), base) if known_base else None
        row['merged'] = (merge.returncode == 0 if merge.returncode in (0, 1) else None) if merge else None
        row['pr_state'] = 'UNKNOWN'
        row['transcript_activity'] = 'UNKNOWN'
        row['safe_to_delete'] = 'NOT_ESTABLISHED'
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('repo', nargs='?', default='.')
    parser.add_argument('--base')
    args = parser.parse_args()
    print(json.dumps(audit(args.repo, args.base), indent=2))


if __name__ == '__main__':
    main()
