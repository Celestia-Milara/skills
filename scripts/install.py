"""Install a complete bundle into one project without changing global settings."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import tempfile

from package import ROOT, SUPPLEMENTS, build, digest


def files(directory):
    return {p.relative_to(directory).as_posix(): digest(p) for p in directory.rglob('*') if p.is_file()}


def is_link(path):
    return path.is_symlink() or getattr(path, 'is_junction', lambda: False)() or path.resolve() != path.absolute()


def install(host, project, dry_run=False, replace=False):
    project = Path(project).resolve()
    host_root = project / ('.agents' if host == 'codex' else '.claude')
    bundle = host_root / 'pstack'
    for directory in (host_root, host_root / 'skills', host_root / 'agents'):
        if os.path.lexists(directory) and (is_link(directory) or not directory.is_dir()):
            raise ValueError(f'Installation directory must be a real local directory: {directory}')
    names = sorted([p.parent.name for p in (ROOT / 'pstack/skills').glob('*/SKILL.md')] + list(SUPPLEMENTS))
    agent_names = ['poteto-agent.md', 'comment-sicko.md'] if host == 'claude-code' else []
    existing = None
    if os.path.lexists(bundle):
        marker = bundle / '.library-install.json'
        if not replace or not marker.is_file() or is_link(bundle):
            raise FileExistsError(f'Existing bundle requires a recognized --replace-managed install: {bundle}')
        existing = json.loads(marker.read_text(encoding='utf-8'))
        if existing.get('project') != str(project) or existing.get('host') != host:
            raise ValueError('Existing bundle is not owned by this installation.')
        if files(bundle) != {**existing['bundle_files'], '.library-install.json': digest(marker)}:
            raise ValueError('Installed bundle changed; preserve and reconcile it first.')
    for name in names:
        path = host_root / 'skills' / name
        if os.path.lexists(path):
            expected = existing.get('skills', {}).get(name) if existing else None
            if path.resolve() != path.absolute() or not expected or files(path) != expected:
                raise FileExistsError(f'Preserving existing or modified skill: {path}')
    for name in agent_names:
        path = host_root / 'agents' / name
        if os.path.lexists(path) and (not existing or path.is_symlink() or digest(path) != existing.get('agents', {}).get(name)):
            raise FileExistsError(f'Preserving existing or modified agent: {path}')
    if dry_run:
        return {'host': host, 'project': str(project), 'skills': len(names), 'bundle': str(bundle), 'dry_run': True}
    host_root.mkdir(parents=True, exist_ok=True)
    # Preflight checks complete before any existing path moves. Build first, so a
    # packaging failure cannot disturb an existing installation.
    with tempfile.TemporaryDirectory(prefix='pstack-build-') as temporary:
        staged = build(Path(temporary) / 'bundle')
        if existing:
            backup = host_root / 'pstack-backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
            backup.mkdir(parents=True)
            assert bundle.resolve().parent == host_root.resolve()
            bundle.rename(backup / 'bundle')
            (backup / 'skills').mkdir()
            for name in names:
                path = host_root / 'skills' / name
                if path.exists():
                    assert path.resolve().parent == (host_root / 'skills').resolve()
                    path.rename(backup / 'skills' / name)
            if agent_names:
                (backup / 'agents').mkdir()
                for name in agent_names:
                    path = host_root / 'agents' / name
                    if path.exists():
                        path.rename(backup / 'agents' / name)
        shutil.copytree(staged, bundle)
    (host_root / 'skills').mkdir(exist_ok=True)
    registered = {}
    for name in names:
        target = host_root / 'skills' / name
        shutil.copytree(bundle / 'skills' / name, target)
        for path in target.rglob('*.md'):
            value = path.read_text(encoding='utf-8')
            value = value.replace('../../docs/', '../../pstack/docs/').replace('../../README.md', '../../pstack/README.md')
            if path.name == 'SKILL.md':
                match = re.match(r'^(---\s*\n)(.*?)(\n---)', value, re.S)
                if match:
                    fields = 'disable-model-invocation|icon|color|paths' if host == 'codex' else 'paths'
                    header = re.sub(r'^(?:' + fields + r'):[^\n]*\n?', '', match[2], flags=re.M)
                    value = match[1] + header.rstrip() + match[3] + value[match.end():]
            path.write_text(value, encoding='utf-8', newline='\n')
        registered[name] = files(target)
    if agent_names:
        (host_root / 'agents').mkdir(exist_ok=True)
        for name in agent_names:
            shutil.copy2(bundle / 'agents' / name, host_root / 'agents' / name)
    managed = {'host': host, 'project': str(project), 'bundle_files': files(bundle), 'skills': registered,
               'agents': {n: digest(host_root / 'agents' / n) for n in agent_names}}
    (bundle / '.library-install.json').write_text(json.dumps(managed, indent=2) + '\n', encoding='utf-8')
    return {'host': host, 'project': str(project), 'skills': len(names), 'bundle': str(bundle), 'dry_run': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=['codex', 'claude-code'], required=True)
    parser.add_argument('--project', required=True)
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--replace-managed', action='store_true')
    args = parser.parse_args()
    print(json.dumps(install(args.host, args.project, args.dry_run, args.replace_managed), indent=2))


if __name__ == '__main__':
    main()
