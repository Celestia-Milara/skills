"""Content-addressed shared resources and host-owned Junction projections."""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile

from package import ROOT, SUPPLEMENTS, build, digest
from projection import LINK, entry, invocation_metadata, project_agent, relocate
from urllib.parse import unquote, urlsplit

RECEIPT = '.pstack-install.json'
RUNTIME_CACHE_PATHS = {'poteto-mode': {'scripts/node_modules'}}


def junction(path):
    return getattr(path.lstat(), 'st_reparse_tag', 0) == 0xA0000003


def make_junction(link, target):
    if os.name != 'nt':
        raise ValueError('Junction storage requires native Windows CPython.')
    if os.path.lexists(link) or not target.is_dir():
        raise FileExistsError(f'Junction destination occupied or target missing: {link}')
    import _winapi
    _winapi.CreateJunction(str(target), str(link))
    if not junction(link) or link.resolve(strict=True) != target.resolve(strict=True):
        raise ValueError(f'Junction target verification failed: {link}')


def remove_local_tree(path):
    """Remove an owned staging tree without traversing any reparse point."""
    if not os.path.lexists(path):
        return
    info = path.lstat()
    if junction(path):
        path.rmdir()
    elif path.is_symlink():
        path.unlink()
    elif getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0):
        raise ValueError(f'Preserving unknown reparse point: {path}')
    elif path.is_dir():
        for child in path.iterdir():
            remove_local_tree(child)
        path.rmdir()
    else:
        path.unlink()


def local_inventory(root):
    result = {'files': {}, 'links': {}}
    def visit(path):
        relative = path.relative_to(root).as_posix()
        if relative in RUNTIME_CACHE_PATHS.get(root.name, set()):
            return
        info = path.lstat()
        if junction(path):
            result['links'][relative] = str(path.resolve(strict=True))
        elif path.is_symlink() or getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0):
            raise ValueError(f'Unrecognized managed link: {path}')
        elif path.is_dir():
            for child in sorted(path.iterdir()):
                visit(child)
        else:
            result['files'][relative] = digest(path)
    if not root.is_dir() or root.resolve() != root.absolute():
        raise ValueError(f'Expected a real generated entry directory: {root}')
    for child in sorted(root.iterdir()):
        visit(child)
    return result


def content_key(files):
    return hashlib.sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def shared_version(store):
    from install import files, installation_lock, is_link
    if store.resolve() != store.absolute():
        raise ValueError(f'Store path must not traverse links: {store}')
    if os.path.lexists(store) and (not store.is_dir() or is_link(store)):
        raise ValueError(f'Invalid store: {store}')
    with installation_lock(store):
        versions = store / 'versions'
        if os.path.lexists(versions) and (not versions.is_dir() or is_link(versions)):
            raise ValueError(f'Invalid version directory: {versions}')
        versions.mkdir(exist_ok=True)
        temporary = Path(tempfile.mkdtemp(prefix='.build-', dir=store))
        try:
            candidate = build(temporary / 'bundle', include_supplements=True)
            expected = files(candidate)
            key = content_key(expected)
            target = versions / key
            if os.path.lexists(target):
                if is_link(target) or not target.is_dir() or files(target) != expected:
                    raise ValueError(f'Occupied or modified shared version: {target}')
            else:
                candidate.rename(target)
            return target, expected
        finally:
            remove_local_tree(temporary)


def read_receipt(host, base, host_root, scope):
    from install import check_roots, files, is_link
    check_roots(host_root)
    path = host_root / RECEIPT
    if not path.is_file() or is_link(path):
        raise FileExistsError(f'Missing or linked Junction receipt: {path}')
    record = json.loads(path.read_text(encoding='utf-8'))
    if (record.get('format') != 1 or record.get('storage') != 'junction' or
            record.get('host') != host or record.get('scope') != scope or record.get('owner') != str(base)):
        raise ValueError('Junction installation ownership mismatch')
    for section in ['skills', 'agents']:
        values = record.get(section)
        if not isinstance(values, dict) or any(not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_.-]*', name) for name in values):
            raise ValueError('Invalid managed entry names')
    store = Path(record['store'])
    target = Path(record['version'])
    key = content_key(record['bundle_files'])
    if (not store.is_absolute() or store.resolve() != store.absolute() or
            target != store / 'versions' / key or is_link(target) or files(target) != record['bundle_files']):
        raise ValueError('Shared version content or identity changed')
    link = host_root / 'pstack'
    if not junction(link) or link.resolve(strict=True) != target:
        raise ValueError('Public resource Junction target changed')
    for name, expected in record['skills'].items():
        if local_inventory(host_root / 'skills' / name) != expected:
            raise FileExistsError(f'Preserving modified entry: {name}')
        for destination in expected['links'].values():
            if not Path(destination).is_relative_to(target):
                raise ValueError('Resource link leaves the recorded shared version')
    for name, expected in record['agents'].items():
        path = host_root / 'agents' / name
        if is_link(path) or not path.is_file() or digest(path) != expected:
            raise FileExistsError(f'Preserving modified agent: {name}')
    return record


def inspect(host, base, root, scope, replace, names, agents):
    from install import check_roots, preflight
    check_roots(root)
    if os.path.lexists(root / RECEIPT):
        if not replace:
            raise FileExistsError('Existing Junction installation requires --replace-managed')
        record = read_receipt(host, base, root, scope)
    else:
        record = preflight(host, base, root, root / 'pstack', scope, replace, names, agents)
    for section, entries in [('skills', names), ('agents', agents)]:
        for name in entries:
            if os.path.lexists(root / section / name) and (not record or name not in record.get(section, {})):
                raise FileExistsError(f'Preserving unmanaged entry: {root / section / name}')
    return record


def project_shared(host, base, staging, final_root, version, store, expected, names, agents, scope):
    from install import files
    bundle = staging / 'pstack'
    make_junction(bundle, version)
    generated = {}
    for name in names:
        original = version / 'skills' / name
        target = staging / 'skills' / name
        target.mkdir(parents=True)
        for child in original.iterdir():
            destination = target / child.name
            if child.is_dir():
                # Tool packages can install dependencies beside their source.
                share = child.name not in {'agents', 'scripts'}
                for source in child.rglob('*.md'):
                    text = source.read_text(encoding='utf-8')
                    for match in LINK.finditer(text):
                        href = match[1]
                        if urlsplit(href).scheme or href.startswith(('#', '//')):
                            continue
                        referenced = (source.parent / unquote(href.split('#')[0])).resolve()
                        if referenced.exists() and not referenced.is_relative_to(original):
                            share = False
                    relocated = relocate(text, source,
                                         target / source.relative_to(original), bundle, staging, names)
                    if relocated != text:
                        share = False
                        break
                if share:
                    make_junction(destination, child)
                    continue
                shutil.copytree(child, destination)
                for path in destination.rglob('*.md'):
                    source = original / path.relative_to(target)
                    path.write_text(relocate(path.read_text(encoding='utf-8'), source, path, bundle, staging, names),
                                    encoding='utf-8', newline='\n')
            else:
                shutil.copy2(child, destination)
                if child.suffix == '.md':
                    destination.write_text(relocate(child.read_text(encoding='utf-8'), child, destination,
                                                    bundle, staging, names), encoding='utf-8', newline='\n')
        skill = target / 'SKILL.md'
        value, explicit = entry(skill.read_text(encoding='utf-8'), host, f'../../pstack/adapters/{host}.md')
        skill.write_text(value, encoding='utf-8', newline='\n')
        if host == 'codex':
            metadata = target / 'agents/openai.yaml'
            metadata.parent.mkdir(exist_ok=True)
            value = metadata.read_text(encoding='utf-8') if metadata.exists() else ''
            metadata.write_text(invocation_metadata(value, explicit), encoding='utf-8')
        generated[name] = local_inventory(target)
    for name in agents:
        target = staging / 'agents' / name
        target.parent.mkdir(exist_ok=True)
        value = project_agent((version / 'agents' / name).read_text(encoding='utf-8'), host, final_root,
                              skill_root=final_root / 'skills')
        target.write_text(value, encoding='utf-8', newline='\n')
    if files(version) != expected:
        raise ValueError('Projection modified public resources')
    record = {'format': 1, 'storage': 'junction', 'host': host, 'scope': scope, 'owner': str(base),
              'store': str(store), 'version': str(version), 'bundle_files': expected,
              'skills': generated, 'agents': {n: digest(staging / 'agents' / n) for n in agents},
              'pstack_skills': [n for n in names if n not in SUPPLEMENTS],
              'preserved_supplements': [n for n in names if n in SUPPLEMENTS]}
    record['runtime_cache_paths'] = {n: sorted(paths) for n, paths in RUNTIME_CACHE_PATHS.items() if n in names}
    (staging / RECEIPT).write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')


def install(host, project=None, dry_run=False, replace=False, *, scope='project', home=None,
            with_supplements=False, store=None):
    from install import layout, installation_lock, move_paths, RecoveryError
    if os.name != 'nt':
        raise ValueError('Junction storage requires native Windows CPython.')
    base, root, bundle = layout(host, project, scope, home)
    store = Path(store).absolute() if store else base / '.pstack-store'
    if str(store).startswith('\\\\'):
        raise ValueError('Junction storage requires a local resource store, not a UNC path')
    protected = [ROOT / name for name in ('pstack', 'adapters', *SUPPLEMENTS)]
    if any(store.is_relative_to(path) for path in protected):
        raise ValueError('The resource store must be outside source packages')
    if (store.resolve() != store.absolute() or store.is_relative_to(root) or root.is_relative_to(store)):
        raise ValueError('Store must be a separate real directory outside the host installation')
    old_path = root / RECEIPT if os.path.lexists(root / RECEIPT) else bundle / '.library-install.json'
    if old_path.is_file():
        previous = json.loads(old_path.read_text(encoding='utf-8'))
        with_supplements |= bool(set(previous.get('skills', {})) & set(SUPPLEMENTS))
    names = sorted(p.parent.name for p in (ROOT / 'pstack/skills').glob('*/SKILL.md'))
    names += list(SUPPLEMENTS) if with_supplements else []
    names = sorted(names)
    agents = ['poteto-agent.md', 'comment-sicko.md'] if host == 'claude-code' else []
    inspect(host, base, root, scope, replace, names, agents)
    result = {'host': host, 'storage': 'junction', 'skills': len(names), 'store': str(store), 'dry_run': dry_run}
    if dry_run:
        return result
    with installation_lock(root):
        version, expected = shared_version(store)
        staging = Path(tempfile.mkdtemp(prefix='.pstack-stage-', dir=root))
        backup = None
        backup_created = False
        retain = False
        try:
            project_shared(host, base, staging, root, version, store, expected, names, agents, scope)
            old = inspect(host, base, root, scope, replace, names, agents)
            pairs = []
            if old:
                backup = root / 'pstack-backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                backup.mkdir(parents=True)
                backup_created = True
                pairs.append((bundle, backup / ('pstack' if old.get('storage') == 'junction' else 'bundle')))
                if os.path.lexists(root / RECEIPT):
                    pairs.append((root / RECEIPT, backup / RECEIPT))
                for section in ['skills', 'agents']:
                    pairs.extend((root / section / n, backup / section / n) for n in old.get(section, {})
                                 if os.path.lexists(root / section / n))
            pairs.append((staging / 'pstack', bundle))
            pairs += [(staging / 'skills' / n, root / 'skills' / n) for n in names]
            pairs += [(staging / 'agents' / n, root / 'agents' / n) for n in agents]
            pairs.append((staging / RECEIPT, root / RECEIPT))
            move_paths(pairs)
        except RecoveryError as error:
            retain = True
            raise RecoveryError(f'{error}. Staging: {staging}; backup: {backup}') from error
        except BaseException:
            if backup_created:
                remove_local_tree(backup)
            raise
        finally:
            if not retain:
                remove_local_tree(staging)
        result.update(version=str(version), receipt=str(root / RECEIPT))
        if backup:
            result['backup'] = str(backup)
    return result


def uninstall(host, project=None, *, scope='project', home=None, dry_run=False):
    from install import layout, installation_lock, move_paths
    base, root, bundle = layout(host, project, scope, home)
    record = read_receipt(host, base, root, scope)
    result = {'host': host, 'storage': 'junction', 'dry_run': dry_run, 'public_resources_retained': record['version']}
    if dry_run:
        return result
    with installation_lock(root):
        record = read_receipt(host, base, root, scope)
        archive = root / 'pstack-backups' / ('uninstall-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
        pairs = [(bundle, archive / 'pstack'), (root / RECEIPT, archive / RECEIPT)]
        pairs += [(root / section / n, archive / section / n) for section in ['skills', 'agents'] for n in record[section]]
        move_paths(pairs)
    result['archive'] = str(archive)
    return result


def restore(host, archive, project=None, *, scope='project', home=None, dry_run=False):
    from install import layout, installation_lock, move_paths
    base, root, _ = layout(host, project, scope, home)
    archive = Path(archive).absolute()
    if archive.resolve() != archive or archive.parent != root / 'pstack-backups':
        raise ValueError('Restore requires a direct local backup of this host')
    previous = read_receipt(host, base, archive, scope)
    current = inspect(host, base, root, scope, True, list(previous['skills']), list(previous['agents']))
    if current and current.get('storage') != 'junction':
        raise ValueError('Archive an existing copy installation before restoring a Junction version')
    result = {'host': host, 'restored_version': previous['version'], 'dry_run': dry_run}
    if dry_run:
        return result
    with installation_lock(root):
        previous = read_receipt(host, base, archive, scope)
        current = inspect(host, base, root, scope, True, list(previous['skills']), list(previous['agents']))
        if current and current.get('storage') != 'junction':
            raise ValueError('Cannot replace a copy install through Junction restore')
        retained = root / 'pstack-backups' / ('before-restore-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ'))
        pairs = []
        if current:
            pairs = [(root / 'pstack', retained / 'pstack'), (root / RECEIPT, retained / RECEIPT)]
            pairs += [(root / section / n, retained / section / n) for section in ['skills', 'agents'] for n in current[section]]
        pairs += [(archive / 'pstack', root / 'pstack')]
        pairs += [(archive / section / n, root / section / n) for section in ['skills', 'agents'] for n in previous[section]]
        pairs += [(archive / RECEIPT, root / RECEIPT)]
        move_paths(pairs)
    if current:
        result['backup'] = str(retained)
    return result
