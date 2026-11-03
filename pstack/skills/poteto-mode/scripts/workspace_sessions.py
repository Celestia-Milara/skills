"""Select local session files by workspace metadata, without returning content."""
import argparse
from datetime import datetime, timezone
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
            for index, line in enumerate(stream):
                if index >= (1 if host == 'codex' else 100):
                    break
                try:
                    row = json.loads(line)
                except (ValueError, TypeError):
                    continue
                cwd = row.get('payload', {}).get('cwd') if row.get('type') == 'session_meta' else row.get('cwd')
                if isinstance(cwd, str):
                    return cwd
    except (OSError, UnicodeError):
        pass
    return None


def select_sessions(host, workspace, home=None):
    isolated_home = home is not None
    home = Path(home) if isolated_home else Path.home()
    if host == 'codex':
        config = home / '.codex' if isolated_home else Path(os.environ.get('CODEX_HOME', home / '.codex'))
        candidates = (config / 'sessions').glob('*/*/*/rollout-*.jsonl')
    else:
        config = home / '.claude' if isolated_home else Path(os.environ.get('CLAUDE_CONFIG_DIR', home / '.claude'))
        # Encodings vary across host versions. Both candidate directories remain
        # workspace-scoped; recorded cwd is required before a file is selected.
        slugs = {re.sub(r'[^A-Za-z0-9]', '-', workspace), re.sub(r'[^A-Za-z0-9_-]', '-', workspace)}
        candidates = (path for slug in sorted(slugs) for path in (config / 'projects' / slug).glob('*.jsonl'))
    selected = []
    for path in candidates:
        cwd = recorded_workspace(path, host)
        if cwd and canonical(cwd) == canonical(workspace):
            stat = path.stat()
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
