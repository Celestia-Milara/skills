"""Build the complete local pstack bundle, including the five supplementary skills."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
SUPPLEMENTS = ('grilling', 'grill-me', 'to-docs', 'maintenance-docs', 'decision-notes')
IGNORED = shutil.ignore_patterns('node_modules', '__pycache__', '*.pyc', '.git')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build(output):
    output = Path(output).resolve()
    if output == ROOT or ROOT in output.parents and output.parts[len(ROOT.parts)] not in ('.dist', '.tmp'):
        raise ValueError('Choose a new output outside source packages, or under .dist/.tmp.')
    if output.exists():
        raise FileExistsError(f'Output already exists: {output}')
    shutil.copytree(ROOT / 'pstack', output, ignore=IGNORED)
    for name in SUPPLEMENTS:
        shutil.copytree(ROOT / name, output / 'skills' / name, ignore=IGNORED)
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
    skills = sorted(p.parent.name for p in (output / 'skills').glob('*/SKILL.md'))
    assert len(skills) == 63 and len(set(skills)) == 63
    files = {p.relative_to(output).as_posix(): digest(p) for p in output.rglob('*') if p.is_file()}
    (output / 'BUNDLE.json').write_text(json.dumps({'format': 1, 'skills': skills, 'files': files}, indent=2) + '\n', encoding='utf-8')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    output = build(args.output)
    print(f'Built 63 skills and two agents: {output}')


if __name__ == '__main__':
    main()
