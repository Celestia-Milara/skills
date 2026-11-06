"""Check imported completeness, backup hashes, metadata, and maintained references."""
import argparse
import collections
import hashlib
import json
from pathlib import Path
import re
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENTS = ('grilling', 'grill-me', 'to-docs', 'maintenance-docs', 'decision-notes')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without_code(value):
    return re.sub(r'^```.*?^```[^\n]*$', '', value, flags=re.M | re.S)


def anchors(value):
    result, counts = set(), collections.Counter()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', without_code(value), re.M):
        heading = re.sub(r'\[([^]]+)\]\([^)]*\)', r'\1', heading).replace('`', '').lower()
        slug = ''.join(c for c in heading if c in '_- ' or unicodedata.category(c)[0] in 'LN').replace(' ', '-')
        result.add(slug + (f'-{counts[slug]}' if counts[slug] else ''))
        counts[slug] += 1
    return result


def links(path, base):
    errors = []
    for match in re.finditer(r'(?<!!)\[[^]\n]+\]\((<[^>]+>|[^\s)]+)(?:\s+"[^"]*")?\)', without_code(path.read_text(encoding='utf-8'))):
        target = match[1].strip('<>')
        if urlsplit(target).scheme or target.startswith('//'):
            continue
        name, _, fragment = unquote(target).partition('#')
        dest = (path.parent / name).resolve() if name else path
        if not dest.exists():
            errors.append(f'{path.relative_to(base)}: missing {target}')
        elif fragment and dest.suffix == '.md' and fragment not in anchors(dest.read_text(encoding='utf-8')):
            errors.append(f'{path.relative_to(base)}: missing anchor {target}')
    return errors


def verify(root=ROOT):
    root = Path(root)
    errors, warnings = [], []
    pstack = root / 'pstack'
    lock = json.loads((pstack / 'source-lock.json').read_text(encoding='utf-8'))
    upstream, mirror = lock['upstream']['files'], lock['portability_reference']['files']
    for rel in set(upstream) | set(mirror):
        if not (pstack / rel).is_file():
            errors.append(f'Missing source file: {rel}')
    changed = sorted(rel for rel, expected in mirror.items() if (pstack / rel).is_file() and sha(pstack / rel) != expected)
    if changed != sorted(lock['local_changes']):
        errors.append('source-lock local_changes differs from actual changes')
    manifest = json.loads((root / 'legacy/manifest.json').read_text(encoding='utf-8'))
    archive = root / 'legacy' / manifest['archive']
    if sha(archive) != manifest['sha256']:
        errors.append('Legacy archive hash mismatch')
    with zipfile.ZipFile(archive) as z:
        if set(z.namelist()) != set(manifest['files']):
            errors.append('Legacy archive file set differs')
        for rel, expected in manifest['files'].items():
            if hashlib.sha256(z.read(rel)).hexdigest() != expected:
                errors.append(f'Legacy file hash mismatch: {rel}')
    skills = list((pstack / 'skills').glob('*/SKILL.md')) + [root / n / 'SKILL.md' for n in SUPPLEMENTS]
    names = []
    for path in skills + list((pstack / 'automations').rglob('SKILL.md')):
        value = path.read_text(encoding='utf-8')
        header = re.match(r'^---\s*\n(.*?)\n---', value, re.S)
        if not header:
            errors.append(f'Missing frontmatter: {path}')
            continue
        name = re.search(r'^name:\s*(.+)$', header[1], re.M)
        description = re.search(r'^description:\s*\S', header[1], re.M)
        if not name or not description:
            errors.append(f'Missing name/description: {path}')
            continue
        if path in skills:
            names.append(name[1].strip().strip('"\''))
        metadata = path.parent / 'agents/openai.yaml'
        if not metadata.is_file() or not (path.parent / 'LICENSE').is_file():
            errors.append(f'Missing metadata/license: {path}')
        elif path.is_relative_to(pstack):
            ui = metadata.read_text(encoding='utf-8')
            short = re.search(r'^\s+short_description:\s*(.+)$', ui, re.M)
            if not short or not 25 <= len(json.loads(short[1])) <= 64:
                errors.append(f'Invalid short_description length: {metadata}')
            explicit = bool(re.search(r'^disable-model-invocation:\s*true\s*$', header[1], re.M))
            disabled = 'allow_implicit_invocation: false' in metadata.read_text(encoding='utf-8')
            if explicit != disabled:
                errors.append(f'Invocation policy mismatch: {path}')
            if '## Host adapter' not in value:
                errors.append(f'Missing host trigger: {path}')
    if len(names) != 63 or len(set(names)) != 63:
        errors.append(f'Expected 63 unique active names, got {len(names)}/{len(set(names))}')
    # Imported docs can contain existing sample links. Only known original failures
    # are warnings; every local/new broken link is an error.
    paths = [root / 'README.md', root / 'AGENTS.md']
    for directory in ['agent-guidance', 'docs', *SUPPLEMENTS, 'pstack', 'legacy']:
        paths.extend(path for path in (root / directory).rglob('*.md')
                     if 'node_modules' not in path.relative_to(root).parts)
    baseline_failures = set(lock.get('baseline_link_errors', []))
    for path in paths:
        for failure in links(path, root):
            if failure in baseline_failures:
                warnings.append(failure)
            else:
                errors.append(failure)
    print(json.dumps({'upstream_files': len(upstream), 'mirror_files': len(mirror), 'legacy_files': len(manifest['files']),
                      'active_skills': len(names), 'adapted_source_files': len(changed), 'errors': errors, 'upstream_link_warnings': warnings}, indent=2))
    return not errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    raise SystemExit(0 if verify() else 1)
