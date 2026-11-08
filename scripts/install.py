"""Install a complete bundle in project or user scope without changing host settings."""
import argparse
from contextlib import contextmanager, ExitStack
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile

from package import ROOT, SUPPLEMENTS, build, digest
from projection import HOST_ROOTS, project_skill, project_agent


def files(directory):
    result = {}
    for parent, directories, names in os.walk(directory):
        for name in directories + names:
            path = Path(parent) / name
            attributes = path.lstat()
            if stat.S_ISLNK(attributes.st_mode) or getattr(attributes, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0):
                raise ValueError(f'Managed trees cannot contain links: {path}')
            if path.is_file():
                result[path.relative_to(directory).as_posix()] = digest(path)
    return result


def is_link(path):
    return path.is_symlink() or getattr(path, 'is_junction', lambda: False)() or path.resolve() != path.absolute()


def layout(host, project=None, scope='project', home=None):
    if host not in HOST_ROOTS:
        raise ValueError('Unknown host profile.')
    if scope not in ('project', 'user'):
        raise ValueError('Scope must be project or user.')
    if scope == 'user' and project is not None:
        raise ValueError('User scope takes --home, not --project.')
    if scope == 'project' and project is None:
        raise ValueError('Project scope requires --project.')
    base = Path(home or Path.home()).resolve() if scope == 'user' else Path(project).resolve()
    host_root = base / ('.codex' if host == 'codex' and scope == 'user' else HOST_ROOTS[host])
    if any(host_root.is_relative_to(ROOT / source) for source in ('pstack', *SUPPLEMENTS)):
        raise ValueError('Installation output must be outside the source packages.')
    return base, host_root, host_root / 'pstack'


def managed(host, base, host_root, bundle, scope):
    marker = bundle / '.library-install.json'
    if not marker.is_file() or is_link(bundle):
        raise FileExistsError(f'Not a recognized managed installation: {bundle}')
    existing = json.loads(marker.read_text(encoding='utf-8'))
    for section in ('skills', 'agents'):
        entries = existing.get(section, {})
        if not isinstance(entries, dict) or any(
                not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.-]*', name) for name in entries):
            raise ValueError(f'Invalid managed {section} names in {marker}')
    owner_key = 'home' if scope == 'user' else 'project'
    if (existing.get(owner_key) != str(base) or existing.get('host') != host
            or existing.get('scope', 'project') != scope):
        raise ValueError('Existing bundle is not owned by this installation.')
    if files(bundle) != {**existing['bundle_files'], '.library-install.json': digest(marker)}:
        raise ValueError('Installed bundle changed; preserve and reconcile it first.')
    return existing


def check_roots(host_root):
    for directory in (host_root, host_root / 'skills', host_root / 'agents', host_root / 'pstack-backups'):
        if os.path.lexists(directory) and (is_link(directory) or not directory.is_dir()):
            raise ValueError(f'Installation directory must be a real local directory: {directory}')


def check_entries(host_root, existing, require_all=False):
    for name, expected in existing['skills'].items():
        path = host_root / 'skills' / name
        if not os.path.lexists(path) and not require_all:
            continue
        if not path.is_dir() or is_link(path) or files(path) != expected:
            raise FileExistsError(f'Preserving existing or modified skill: {path}')
    for name, expected in existing.get('agents', {}).items():
        path = host_root / 'agents' / name
        if not os.path.lexists(path) and not require_all:
            continue
        if not path.is_file() or is_link(path) or digest(path) != expected:
            raise FileExistsError(f'Preserving existing or modified agent: {path}')


def preflight(host, base, host_root, bundle, scope, replace, names, agent_names):
    check_roots(host_root)
    existing = None
    if os.path.lexists(bundle):
        if not replace:
            raise FileExistsError(f'Existing bundle requires a recognized --replace-managed install: {bundle}')
        existing = managed(host, base, host_root, bundle, scope)
        check_entries(host_root, existing)
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
    return existing


@contextmanager
def installation_lock(host_root):
    host_root.mkdir(parents=True, exist_ok=True)
    path = host_root / '.pstack-install.lock'
    try:
        stream = path.open('x', encoding='utf-8')
    except FileExistsError:
        raise FileExistsError(f'Installation is locked: {path}. Check the owning process before recovery.') from None
    try:
        with stream:
            stream.write(f'{os.getpid()}\n')
        yield
    finally:
        path.unlink()


class RecoveryError(RuntimeError):
    """A failed rollback retained its files for manual recovery."""


def move_paths(pairs):
    moved = []
    try:
        for source, target in pairs:
            if os.path.lexists(target):
                raise FileExistsError(f'Preserving occupied destination: {target}')
            target.parent.mkdir(parents=True, exist_ok=True)
            source.rename(target)
            moved.append((source, target))
    except BaseException as failure:
        errors = []
        for source, target in reversed(moved):
            try:
                if os.path.lexists(source):
                    raise FileExistsError(f'Recovery destination is occupied: {source}')
                target.rename(source)
            except OSError as error:
                errors.append(str(error))
        if errors:
            raise RecoveryError('Rollback incomplete; retained recovery files: ' + '; '.join(errors)) from failure
        raise


def project_packages(host, base, host_root, names, agent_names, scope):
    bundle = host_root / 'pstack'
    with tempfile.TemporaryDirectory(prefix='pstack-build-') as temporary:
        source = build(Path(temporary) / 'bundle', include_supplements=bool(set(names) & set(SUPPLEMENTS)))
        expected = files(source)
        shutil.copytree(source, bundle)
        if files(bundle) != expected:
            raise ValueError('Staged bundle differs from the verified build.')
    (host_root / 'skills').mkdir(exist_ok=True)
    registered = {}
    for name in names:
        target = host_root / 'skills' / name
        shutil.copytree(bundle / 'skills' / name, target)
        if files(target) != files(bundle / 'skills' / name):
            raise ValueError(f'Staged skill differs from its source: {name}')
        project_skill(host, bundle, host_root, name, names)
        registered[name] = files(target)
    if agent_names:
        (host_root / 'agents').mkdir(exist_ok=True)
        for name in agent_names:
            shutil.copy2(bundle / 'agents' / name, host_root / 'agents' / name)
            if digest(host_root / 'agents' / name) != digest(bundle / 'agents' / name):
                raise ValueError(f'Staged agent differs from its source: {name}')
            final_root = base / HOST_ROOTS[host]
            agent = host_root / 'agents' / name
            agent.write_text(project_agent(agent.read_text(encoding='utf-8'), host, final_root), encoding='utf-8', newline='\n')
    marker = {'host': host, 'scope': scope, 'home' if scope == 'user' else 'project': str(base),
              'bundle_files': files(bundle), 'skills': registered,
              'pstack_skills': [n for n in names if n not in SUPPLEMENTS],
              'preserved_supplements': [n for n in names if n in SUPPLEMENTS],
              'agents': {n: digest(host_root / 'agents' / n) for n in agent_names}}
    (bundle / '.library-install.json').write_text(json.dumps(marker, indent=2) + '\n', encoding='utf-8')


def install(host, project=None, dry_run=False, replace=False, *, scope='project', home=None, with_supplements=False):
    base, host_root, bundle = layout(host, project, scope, home)
    if (bundle / '.library-install.json').is_file():
        previous = json.loads((bundle / '.library-install.json').read_text(encoding='utf-8'))
        with_supplements = with_supplements or bool(set(previous.get('skills', {})) & set(SUPPLEMENTS))
    names = sorted([p.parent.name for p in (ROOT / 'pstack/skills').glob('*/SKILL.md')] + (list(SUPPLEMENTS) if with_supplements else []))
    agent_names = ['poteto-agent.md', 'comment-sicko.md'] if host == 'claude-code' else []
    preflight(host, base, host_root, bundle, scope, replace, names, agent_names)
    result = {'host': host, 'scope': scope, 'home' if scope == 'user' else 'project': str(base),
              'skills': len(names), 'bundle': str(bundle), 'dry_run': dry_run}
    if dry_run:
        return result
    with installation_lock(host_root):
        staging = Path(tempfile.mkdtemp(prefix='.pstack-stage-', dir=host_root))
        backup = None
        backup_created = False
        retain_staging = False
        try:
            project_packages(host, base, staging, names, agent_names, scope)
            existing = preflight(host, base, host_root, bundle, scope, replace, names, agent_names)
            pairs = []
            if existing:
                backup = host_root / 'pstack-backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                backup.mkdir(parents=True)
                backup_created = True
                pairs.append((bundle, backup / 'bundle'))
                for section in ('skills', 'agents'):
                    pairs.extend((host_root / section / name, backup / section / name)
                                 for name in existing.get(section, {})
                                 if (host_root / section / name).exists())
            pairs.append((staging / 'pstack', bundle))
            pairs.extend((staging / 'skills' / name, host_root / 'skills' / name) for name in names)
            pairs.extend((staging / 'agents' / name, host_root / 'agents' / name) for name in agent_names)
            move_paths(pairs)
        except RecoveryError as error:
            retain_staging = True
            raise RecoveryError(f'{error}. Staging: {staging}; backup: {backup}') from error
        except BaseException:
            if backup_created:
                shutil.rmtree(backup)
            raise
        finally:
            if not retain_staging:
                shutil.rmtree(staging)
        if backup:
            result['backup'] = str(backup)
    return result


def retire_project(host, project, home=None, dry_run=False):
    """Archive unchanged managed project copies after checking the user install."""
    user_base, user_root, user_bundle = layout(host, scope='user', home=home)
    base, host_root, bundle = layout(host, project)
    if base == user_base:
        raise ValueError('Project retirement cannot target the user installation.')
    check_roots(user_root)
    check_roots(host_root)
    user = managed(host, user_base, user_root, user_bundle, 'user')
    check_entries(user_root, user, require_all=True)
    existing = managed(host, base, host_root, bundle, 'project')
    check_entries(host_root, existing, require_all=True)
    if any(not set(existing.get(section, {})) <= set(user.get(section, {})) for section in ('skills', 'agents')):
        raise ValueError('The user install does not cover every project entry.')
    backup = host_root / 'pstack-backups' / ('project-to-user-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
    result = {'host': host, 'project': str(base), 'user_bundle': str(user_bundle),
              'skills_to_retire': len(existing['skills']), 'archive': str(backup), 'dry_run': dry_run}
    if dry_run:
        return result
    with ExitStack() as locks:
        for directory in sorted((host_root, user_root)):
            locks.enter_context(installation_lock(directory))
        # Recheck both installations after taking the locks.
        for owner, directory, target, target_scope, expected in (
                (base, host_root, bundle, 'project', existing),
                (user_base, user_root, user_bundle, 'user', user)):
            actual = managed(host, owner, directory, target, target_scope)
            if actual != expected:
                raise ValueError('Installation changed during retirement preflight.')
            check_entries(directory, actual, require_all=True)
        backup.mkdir(parents=True)
        pairs = [(bundle, backup / 'bundle')]
        pairs += [(host_root / 'skills' / name, backup / 'skills' / name) for name in existing['skills']]
        pairs += [(host_root / 'agents' / name, backup / 'agents' / name) for name in existing.get('agents', {})]
        try:
            (backup / 'RETIREMENT.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
            move_paths(pairs)
        except RecoveryError:
            raise
        except BaseException:
            shutil.rmtree(backup)
            raise
    for directory in (host_root / 'skills', host_root / 'agents'):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--host', choices=list(HOST_ROOTS), required=True)
    parser.add_argument('--scope', choices=['project', 'user'], default='project')
    parser.add_argument('--project')
    parser.add_argument('--home', help='User home; defaults to the current account')
    parser.add_argument('--retire-project', help='With user scope, archive this managed project install instead of installing')
    parser.add_argument('--with-supplements', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--replace-managed', action='store_true')
    args = parser.parse_args()
    if args.retire_project:
        if args.scope != 'user' or args.project or args.replace_managed:
            parser.error('--retire-project requires user scope and cannot combine with --project/--replace-managed')
        result = retire_project(args.host, args.retire_project, args.home, args.dry_run)
    else:
        result = install(args.host, args.project, args.dry_run, args.replace_managed, scope=args.scope, home=args.home, with_supplements=args.with_supplements)
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
