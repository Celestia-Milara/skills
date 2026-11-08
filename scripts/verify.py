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
    lock = json.loads((root / 'source-lock.json').read_text(encoding='utf-8'))
    expected = lock['upstream']['files']
    actual = {p.relative_to(root / 'pstack').as_posix(): sha(p)
              for p in (root / 'pstack').rglob('*')
              if p.is_file() and not any(n in {'__pycache__', 'node_modules'} for n in p.relative_to(root / 'pstack').parts)}
    errors = []
    if actual != expected:
        errors.append('Official source path set or hashes differ from the pinned upstream.')
    for name in ['common', 'claude-code', 'codex', 'pi', 'dsh']:
        path = root / 'adapters' / (name + '.md')
        if not path.is_file():
            errors.append(f'Missing host adapter: {name}')
        else:
            # Source adapters link into the bundled layout; validate their links
            # against that layout in the projection tests.
            pass
    legacy = json.loads((root / 'legacy/manifest.json').read_text(encoding='utf-8'))
    if sha(root / 'legacy' / legacy['archive']) != legacy['sha256']:
        errors.append('Legacy archive hash mismatch')
    skills = list((root / 'pstack/skills').glob('*/SKILL.md'))
    if len(skills) != 58:
        errors.append(f'Expected 58 upstream entrypoints, got {len(skills)}')
    for path in [root / 'README.md', root / 'AGENTS.md', root / 'docs/adaptation.md', root / 'docs/composition.md']:
        errors.extend(links(path, root))
    print(json.dumps({'official_files': len(actual), 'pstack_skills': len(skills),
                      'upstream': lock['upstream']['commit'], 'errors': errors}, indent=2))
    return not errors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    raise SystemExit(0 if verify() else 1)
