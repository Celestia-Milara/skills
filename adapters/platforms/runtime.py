"""Check platform mappings and run the portable subset without a shell."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ADAPTERS = HERE.parent
BUNDLE = ADAPTERS.parent


def validate(source=None, directory=HERE):
    source = Path(source) if source else BUNDLE
    if not (source / 'skills').is_dir():
        source = source / 'pstack'
    record = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
    if record['format'] != 1:
        raise ValueError('Unsupported platform manifest format')
    for name, tool in record['tools'].items():
        for relative, expected in tool['sources'].items():
            path = source / relative
            if not path.resolve().is_relative_to(source.resolve()):
                raise ValueError(f'Platform source escapes bundle: {relative}')
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                raise ValueError(f'Platform mapping is stale: {name}: {relative}')
        helper = tool.get('helper')
        if helper:
            path = directory / helper
            if not path.resolve().is_relative_to(directory.parent.resolve()) or not path.is_file():
                raise ValueError(f'Invalid portable helper: {name}')
    return record


def report(record):
    environment = 'windows' if os.name == 'nt' else ('wsl' if sys.platform == 'linux' and os.environ.get('WSL_DISTRO_NAME') else sys.platform)
    tools = {}
    for name, tool in record['tools'].items():
        runnable = bool(tool.get('helper') or tool.get('entry'))
        missing = [dep for dep in tool['dependencies'] if not shutil.which(dep)]
        tools[name] = {'status': ('missing-dependencies' if missing else 'available') if runnable else 'unverified',
                       'missing_dependencies': missing if runnable else None, 'scope': tool['scope']}
    executables = {name: shutil.which(name) for name in ['git', 'node', 'bun', 'deno', 'java', 'mise', 'sh', 'bash']}
    git_bash = []
    if os.name == 'nt' and executables['git']:
        git_root = Path(executables['git']).parent.parent
        git_bash = [str(path) for path in [git_root / 'usr/bin/bash.exe', git_root / 'bin/bash.exe'] if path.is_file()]
    installed_bun = Path.home() / '.bun/bin/bun.exe'
    return {'execution_platform': environment, 'python': sys.executable, 'tools': tools,
            'executables': executables, 'git_bash': git_bash,
            'bun_user_install': str(installed_bun) if os.name == 'nt' and installed_bun.is_file() else None}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='action', required=True)
    sub.add_parser('check', help='Read hashes and dependency locations; execute no tools')
    run = sub.add_parser('run', help='Run a portable helper with unchanged arguments')
    run.add_argument('--skills-root', type=Path, help='Private host skill directory, required for native scripts')
    run.add_argument('tool')
    run.add_argument('arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args(argv)
    try:
        record = validate()
        if args.action == 'check':
            print(json.dumps(report(record), indent=2))
            return 0
        tool = record['tools'].get(args.tool)
        if not tool or not (tool.get('helper') or tool.get('entry')):
            raise ValueError(f'No verified portable mapping for {args.tool}; see platforms/README.md')
        missing = [dep for dep in tool['dependencies'] if not shutil.which(dep)]
        if missing:
            raise ValueError('Missing dependencies: ' + ', '.join(missing))
        if tool.get('helper'):
            command = [sys.executable, '-B', str(HERE / tool['helper'])]
        else:
            if not args.skills_root:
                raise ValueError('Native scripts require --skills-root pointing to private host entries')
            script = args.skills_root / tool['entry']
            expected = tool['sources']['skills/' + tool['entry']]
            if not script.resolve().is_relative_to(args.skills_root.resolve()) or hashlib.sha256(script.read_bytes()).hexdigest() != expected:
                raise ValueError('Private script differs from the pinned platform mapping')
            if (args.skills_root / 'poteto-mode/SKILL.md').resolve() == (BUNDLE / 'skills/poteto-mode/SKILL.md').resolve():
                raise ValueError('Use private host entries, not the public resource bundle')
            command = [shutil.which('node'), str(script.resolve())]
        return subprocess.call([*command, *args.arguments])
    except (OSError, ValueError, KeyError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
