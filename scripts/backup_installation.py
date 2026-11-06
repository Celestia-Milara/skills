"""Back up host configuration and skill trees locally, materializing linked files."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import zipfile

CONFIG_FILES = (
    '.codex/config.toml', '.codex/config.json', '.codex/AGENTS.md',
    '.claude/settings.json', '.claude/settings.local.json', '.claude/CLAUDE.md',
    '.agents/pstack-models.md',
)
SKILL_TREES = (
    '.agents/skills', '.agents/pstack', '.codex/skills',
    '.claude/skills', '.claude/agents', '.claude/pstack', '.claude/rules',
)
PROJECT_TREES = ('.agents/skills', '.agents/pstack', '.claude/skills', '.claude/agents', '.claude/pstack')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def walk(path, ancestors=(), on_link=None, *, include_dirs=False):
    real = path.resolve()
    attributes = getattr(path.lstat(), 'st_file_attributes', 0)
    if on_link and (path.is_symlink() or attributes & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0)):
        on_link(path, real)
    if path.is_dir():
        if real in ancestors:
            raise ValueError(f'Directory-link cycle in backup source: {path}')
        if include_dirs:
            yield path
        for child in sorted(path.iterdir()):
            yield from walk(child, (*ancestors, real), on_link, include_dirs=include_dirs)
    elif path.is_file():
        yield path
    elif os.path.lexists(path):
        raise ValueError(f'Unreadable or broken link in backup source: {path}')


def snapshot(home, project, output):
    if os.path.lexists(output):
        raise FileExistsError(output)
    home, project, output = map(lambda p: Path(p).resolve(), (home, project, output))
    if os.path.lexists(output):
        raise FileExistsError(output)
    sources = [('user/' + rel, home / rel) for rel in (*CONFIG_FILES, *SKILL_TREES)]
    sources += [('project/' + rel, project / rel) for rel in PROJECT_TREES]
    sources = [(alias, path) for alias, path in sources if os.path.lexists(path)]
    manifest = {'created_utc': datetime.now(timezone.utc).isoformat(), 'home': str(home),
                'project': str(project), 'roots': {}, 'files': {}, 'directories': [],
                'links': {}, 'config_hashes': {}}
    entries = []
    for alias, source in sources:
        manifest['roots'][alias] = str(source)

        def record_link(candidate, real):
            name = alias + ('/' + candidate.relative_to(source).as_posix() if candidate != source else '')
            manifest['links'][name] = str(real)

        # Inventory every directory before creating the archive. A descendant
        # junction can reach the output even when the source root cannot.
        for path in walk(source, on_link=record_link, include_dirs=True):
            real = path.resolve()
            if output == real or real in output.parents:
                raise ValueError('Backup output must be outside all source trees.')
            name = alias if path == source else alias + '/' + path.relative_to(source).as_posix()
            is_directory = path.is_dir()
            entries.append((name, path, is_directory, alias, source))
            if is_directory:
                manifest['directories'].append(name + '/')

    output.mkdir(parents=True)
    archive = output / 'configuration-and-skills.zip'
    try:
        with zipfile.ZipFile(archive, 'w', zipfile.ZIP_DEFLATED) as zipped:
            for name, path, is_directory, alias, source in entries:
                if is_directory:
                    zipped.writestr(name + '/', b'')
                    continue
                data = path.read_bytes()
                zipped.writestr(name, data)
                manifest['files'][name] = digest(data)
                if alias.startswith('user/') and alias[5:] in CONFIG_FILES:
                    manifest['config_hashes'][str(source)] = digest(data)
        with zipfile.ZipFile(archive) as zipped:
            expected_names = set(manifest['files']) | set(manifest['directories'])
            if set(zipped.namelist()) != expected_names or len(zipped.namelist()) != len(expected_names):
                raise ValueError('Backup file set mismatch')
            for name, expected in manifest['files'].items():
                if digest(zipped.read(name)) != expected:
                    raise ValueError(f'Backup hash mismatch: {name}')
        manifest['archive_sha256'] = digest(archive.read_bytes())
        (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        (output / 'README.txt').write_text(
            'Local configuration and skills backup. Keep this directory private.\n'
            'The ZIP contains configuration files, directories, and materialized skill files.\n'
            'manifest.json maps archive roots to their original locations and records\n'
            'file hashes plus link targets. Authentication stores and chat history\n'
            'outside the selected configuration and skill roots are not included.\n'
            'Restore selected paths only; do not blindly extract over newer host state.\n'
            'Existing linked targets were not modified.\n', encoding='utf-8')
        return {'backup': str(output), 'files_verified': len(manifest['files']),
                'archive_bytes': archive.stat().st_size, 'links_recorded': len(manifest['links'])}
    except BaseException:
        # This directory was exclusively created by this call, not an old backup.
        shutil.rmtree(output)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--home', default=str(Path.home()))
    parser.add_argument('--project', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    print(json.dumps(snapshot(args.home, args.project, args.output), indent=2))


if __name__ == '__main__':
    main()
