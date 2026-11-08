"""Build official pstack with external host adapters and optional supplements."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat

ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENTS = ('grilling', 'grill-me', 'to-docs', 'maintenance-docs', 'decision-notes')
IGNORED = shutil.ignore_patterns('node_modules', '__pycache__', '*.pyc', '.git')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _source_files(path):
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0):
        raise ValueError(f'Package source must not contain links: {path}')
    if path.is_dir():
        children = sorted(path.iterdir())
        ignored = IGNORED(path, [child.name for child in children])
        for child in children:
            if child.name not in ignored:
                yield from _source_files(child)
    elif path.is_file():
        yield path
    else:
        raise ValueError(f'Package source must contain regular files: {path}')

def _inventory(include_supplements=False):
    lock = json.loads((ROOT / 'source-lock.json').read_text(encoding='utf-8'))
    upstream = {p.relative_to(ROOT / 'pstack').as_posix(): p for p in _source_files(ROOT / 'pstack')}
    if {name: digest(p) for name, p in upstream.items()} != lock['upstream']['files']:
        raise ValueError('Official pstack differs from source-lock.json; update the pinned source deliberately.')
    files = dict(upstream)
    for path in _source_files(ROOT / 'adapters'):
        files['adapters/' + path.relative_to(ROOT / 'adapters').as_posix()] = path
    if include_supplements:
        for name in SUPPLEMENTS:
            if not (ROOT / name / 'LICENSE').is_file():
                raise ValueError(f'Missing supplement license: {name}')
            for path in _source_files(ROOT / name):
                files[f'skills/{name}/' + path.relative_to(ROOT / name).as_posix()] = path
    skills = sorted(name.split('/')[1] for name in files if re.fullmatch(r'skills/[^/]+/SKILL\.md', name))
    expected = 63 if include_supplements else 58
    if len(skills) != expected:
        raise ValueError(f'Expected {expected} skill entrypoints, got {len(skills)}')
    for name in skills:
        text = files[f'skills/{name}/SKILL.md'].read_text(encoding='utf-8')
        header = re.match(r'^---\s*\n(.*?)\n---', text, re.S)
        declared = re.search(r'^name:\s*(.+)$', header[1], re.M) if header else None
        if not declared or declared[1].strip().strip('"\'') != name:
            raise ValueError(f'Skill name must match its directory: {name}')
    return files, skills

def _copy_file(source, target):
    copied = shutil.copy2(source, target)
    path = Path(copied)
    path.chmod(path.stat().st_mode | stat.S_IWUSR)
    return copied

def _remove_readonly(function, path, error):
    if not isinstance(error[1], PermissionError):
        raise error[1]
    os.chmod(path, os.stat(path).st_mode | stat.S_IWUSR)
    function(path)

def build(output, include_supplements=False):
    if os.path.lexists(output):
        raise FileExistsError(f'Output already exists: {output}')
    output = Path(output).resolve()
    if output == ROOT or ROOT in output.parents and output.parts[len(ROOT.parts)] not in ('.dist', '.tmp'):
        raise ValueError('Choose a new output outside source packages, or under .dist/.tmp.')
    sources, skills = _inventory(include_supplements)
    expected = {name: digest(path) for name, path in sources.items()}
    output.mkdir(parents=True)
    try:
        shutil.copytree(ROOT / 'pstack', output, dirs_exist_ok=True, ignore=IGNORED, copy_function=_copy_file)
        shutil.copytree(ROOT / 'adapters', output / 'adapters', ignore=IGNORED, copy_function=_copy_file)
        if include_supplements:
            for name in SUPPLEMENTS:
                shutil.copytree(ROOT / name, output / 'skills' / name, ignore=IGNORED, copy_function=_copy_file)
        copied = {p.relative_to(output).as_posix(): digest(p) for p in _source_files(output)}
        if copied != expected:
            raise ValueError('Copied package files differ from the source inventory.')
        adapter = output / 'adapters/claude-code.md'
        if adapter.is_file():
            adapter.write_text(adapter.read_text(encoding='utf-8').replace('../pstack/docs/', '../docs/'), encoding='utf-8', newline='\n')
        copied = {p.relative_to(output).as_posix(): digest(p) for p in _source_files(output)}
        marker = {'format': 2, 'skills': skills, 'files': copied,
                  'pstack_skills': [n for n in skills if n not in SUPPLEMENTS],
                  'supplements': [n for n in skills if n in SUPPLEMENTS],
                  'upstream': json.loads((ROOT / 'source-lock.json').read_text(encoding='utf-8'))['upstream']['commit']}
        (output / 'BUNDLE.json').write_text(json.dumps(marker, indent=2) + '\n', encoding='utf-8')
    except BaseException:
        shutil.rmtree(output, onerror=_remove_readonly)
        raise
    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    parser.add_argument('--with-supplements', action='store_true')
    args = parser.parse_args()
    output = build(args.output, args.with_supplements)
    print(f'Built {63 if args.with_supplements else 58} skills: {output}')
