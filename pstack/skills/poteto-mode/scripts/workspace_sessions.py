"""Select local session files by workspace metadata, without returning content."""
import argparse
from datetime import datetime, timezone
from itertools import islice
import json
import ntpath
import os
from pathlib import Path
import re


def canonical(value):
    if re.match(r'^[A-Za-z]:[\\/]', value):
        return ntpath.normcase(ntpath.normpath(value))
    return os.path.normcase(os.path.realpath(os.path.expanduser(value)))


def recorded_workspace(path, host):
    try:
        with path.open(encoding='utf-8') as stream:
            for line in islice(stream, 1 if host == 'codex' else 100):
                try:
                    row = json.loads(line)
                except (ValueError, TypeError):
                    continue
                if not isinstance(row, dict):
                    continue
                metadata = row.get('payload') if row.get('type') == 'session_meta' else row
                if not isinstance(metadata, dict):
                    continue
                cwd = metadata.get('cwd')
                if isinstance(cwd, str):
                    return cwd
    except (OSError, UnicodeError):
        pass
    return None


def select_sessions(host, workspace, home=None):
    isolated_home = home is not None
    home = Path(home) if isolated_home else Path.home()
    normalized_workspace = canonical(workspace)
    if host == 'codex':
        config = home / '.codex' if isolated_home else Path(os.environ.get('CODEX_HOME', home / '.codex'))
        candidates = (config / 'sessions').glob('*/*/*/rollout-*.jsonl')
    else:
        config = home / '.claude' if isolated_home else Path(os.environ.get('CLAUDE_CONFIG_DIR', home / '.claude'))
        # Match directory names before opening sessions. Windows paths can have
        # different casing even when their archives are stored on another OS.
        slugs = {re.sub(r'[^A-Za-z0-9]', '-', normalized_workspace),
                 re.sub(r'[^A-Za-z0-9_-]', '-', normalized_workspace)}
        windows_workspace = os.name == 'nt' or bool(re.match(r'^[A-Za-z]:[\\/]', workspace))
        candidates = (path for project in (config / 'projects').glob('*')
                      if (project.name.lower() if windows_workspace else project.name) in slugs
                      for path in project.glob('*.jsonl'))
    selected = []
    for path in candidates:
        cwd = recorded_workspace(path, host)
        if cwd and canonical(cwd) == normalized_workspace:
            try:
                stat = path.stat()
            except FileNotFoundError:
                continue
            selected.append({'path': str(path.resolve()), 'cwd': cwd,
                             'modified_utc': datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                             'modified_ns': stat.st_mtime_ns})
    return sorted(selected, key=lambda item: item['modified_ns'], reverse=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=['codex', 'claude-code'], required=True)
    parser.add_argument('--workspace', required=True)
    parser.add_argument('--home', help='Alternate host home for isolated checks')
    args = parser.parse_args()
    print(json.dumps(select_sessions(args.host, args.workspace, args.home), indent=2))


if __name__ == '__main__':
    main()
