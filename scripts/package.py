"""Build the complete local pstack bundle, including the five supplementary skills."""
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
    """Enumerate regular package files without following links or reparse points."""
    info = path.lstat()
    if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & getattr(stat, 'FILE_ATTRIBUTE_REPARSE_POINT', 0):
        raise ValueError(f'Package source must not contain links: {path}')
    if stat.S_ISDIR(info.st_mode):
        children = sorted(path.iterdir())
        ignored = IGNORED(path, [child.name for child in children])
        for child in children:
            if child.name not in ignored:
                yield from _source_files(child)
    elif stat.S_ISREG(info.st_mode):
        yield path
    else:
        raise ValueError(f'Package source must contain regular files: {path}')


def _inventory():
    """Check package completeness before the build creates its output directory."""
    sources = [(ROOT / 'pstack', Path('.'))]
    sources += [(ROOT / name, Path('skills') / name) for name in SUPPLEMENTS]
    files = {}
    for source, prefix in sources:
        if not source.is_dir():
            raise ValueError(f'Missing source package: {source}')
        for path in _source_files(source):
            name = (prefix / path.relative_to(source)).as_posix()
            if name in files:
                raise ValueError(f'Package paths collide: {name}')
            files[name] = path

    required = {'source-lock.json', 'LICENSE', 'ORIGIN.md', 'plugin.json', 'docs/composition.md',
                'agents/poteto-agent.md', 'agents/comment-sicko.md'}
    if 'source-lock.json' not in files:
        raise ValueError('Missing source file: source-lock.json')
    lock = json.loads(files['source-lock.json'].read_text(encoding='utf-8'))
    for section in ('upstream', 'portability_reference'):
        required.update(lock[section]['files'])
    missing = required - files.keys()
    if missing:
        raise ValueError(f'Missing source resources: {sorted(missing)}')

    skills = sorted(name.split('/')[1] for name in files
                    if re.fullmatch(r'skills/[^/]+/SKILL\.md', name))
    if len(skills) != 63 or not set(SUPPLEMENTS) <= set(skills):
        raise ValueError(f'Expected 63 active skills including all supplements, got {len(skills)}')
    entries = [name for name in files if name.endswith('/SKILL.md')]
    for entry in entries:
        directory = entry.rsplit('/', 1)[0]
        name = directory.rsplit('/', 1)[-1]
        resources = ['LICENSE', 'agents/openai.yaml']
        if directory not in {f'skills/{supplement}' for supplement in SUPPLEMENTS}:
            resources.append('ORIGIN.md')
        for resource in resources:
            if f'{directory}/{resource}' not in files:
                raise ValueError(f'Missing skill resource: {directory}/{resource}')
        value = files[entry].read_text(encoding='utf-8')
        header = re.match(r'^---\s*\n(.*?)\n---', value, re.S)
        declared = re.search(r'^name:\s*(.+)$', header[1], re.M) if header else None
        if not declared or declared[1].strip().strip('"\'') != name:
            raise ValueError(f'Skill name must match its directory: {name}')
    return files, skills


def _copy_file(source, target):
    copied = shutil.copy2(source, target)
    path = Path(copied)
    # Only the new copy needs to be writable for link relocation and cleanup.
    path.chmod(path.stat().st_mode | stat.S_IWUSR)
    return copied


def _remove_readonly(function, path, error):
    if not isinstance(error[1], PermissionError):
        raise error[1]
    os.chmod(path, os.stat(path).st_mode | stat.S_IWUSR)
    function(path)


def _assemble(output, skills, expected):
    shutil.copytree(ROOT / 'pstack', output, ignore=IGNORED, dirs_exist_ok=True, copy_function=_copy_file)
    for directory in (output, output / 'skills'):
        directory.chmod(directory.stat().st_mode | stat.S_IWUSR)
    for name in SUPPLEMENTS:
        shutil.copytree(ROOT / name, output / 'skills' / name, ignore=IGNORED, copy_function=_copy_file)
    copied = {p.relative_to(output).as_posix(): digest(p) for p in _source_files(output)}
    if copied != expected:
        raise ValueError('Copied package files differ from the source inventory.')
    composition = output / 'docs/composition.md'
    value = composition.read_text(encoding='utf-8')
    for name in SUPPLEMENTS:
        value = value.replace(f'../../{name}/SKILL.md', f'../skills/{name}/SKILL.md')
    composition.write_text(value, encoding='utf-8', newline='\n')
    # Relocate source-library links without changing the standalone source packages.
    for name in SUPPLEMENTS:
        for path in (output / 'skills' / name).rglob('*.md'):
            value = path.read_text(encoding='utf-8')
            value = value.replace('../pstack/skills/', '../')
            path.write_text(value, encoding='utf-8', newline='\n')
    agent_dir = output / '.claude-plugin'
    agent_dir.mkdir(exist_ok=True)
    manifest = {'name': 'pstack', 'version': '0.15.36-local.1',
                'description': 'Complete portable pstack with Codex and Claude Code adapters and five supplements.',
                'author': {'name': 'Lauren Tan and skills contributors'},
                'license': 'MIT', 'skills': './skills/',
                'agents': ['./agents/poteto-agent.md', './agents/comment-sicko.md']}
    (agent_dir / 'plugin.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    # BUNDLE.json describes the other files. A source copy of an older marker
    # must not become a stale hash of the marker we are about to replace.
    files = {p.relative_to(output).as_posix(): digest(p) for p in _source_files(output)
             if p != output / 'BUNDLE.json'}
    (output / 'BUNDLE.json').write_text(json.dumps({'format': 1, 'skills': skills, 'files': files}, indent=2) + '\n', encoding='utf-8')


def build(output):
    if os.path.lexists(output):
        raise FileExistsError(f'Output already exists: {output}')
    output = Path(output).resolve()
    if output == ROOT or ROOT in output.parents and output.parts[len(ROOT.parts)] not in ('.dist', '.tmp'):
        raise ValueError('Choose a new output outside source packages, or under .dist/.tmp.')
    if os.path.lexists(output):
        raise FileExistsError(f'Output already exists: {output}')
    sources, skills = _inventory()
    expected = {name: digest(path) for name, path in sources.items()}
    # Reserve the output before copying. If another build won the same path,
    # mkdir fails outside the cleanup block and its output remains untouched.
    output.mkdir(parents=True)
    try:
        _assemble(output, skills, expected)
    except BaseException:
        shutil.rmtree(output, onerror=_remove_readonly)
        raise
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = build(args.output)
    print(f'Built 63 skills and two agents: {output}')


if __name__ == '__main__':
    main()
